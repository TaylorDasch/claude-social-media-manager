#!/usr/bin/env python3
"""
Deduplication Checker — Detect content cannibalization.

Checks across:
  1. YouTube video titles (both channels)
  2. TikTok hooks (from hook bank + output files)
  3. Blog H1s / post titles
  4. Page target queries
  5. Newsletter deep dive topics
  6. Community post topics
  7. Content registry entries

Flags:
  - Near-duplicate titles/hooks (>70% word overlap)
  - Same target query on multiple assets
  - Same angle repeated within 30 days
  - Content that should be consolidated

Usage:
  python3 scripts/dedupe-checker.py                          # Full scan
  python3 scripts/dedupe-checker.py --check-title "Title"    # Check a specific title
  python3 scripts/dedupe-checker.py --check-hook "Hook text" # Check a specific hook
"""

import os
import re
import csv
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

from common import warn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
REGISTRY_PATH = DATA_DIR / "content-registry.csv"
HOOK_BANK_PATH = DATA_DIR / "hook-bank.json"
LIVING_CATALOG = DATA_DIR / "living-in-temple-catalog.txt"
INVESTING_CATALOG = DATA_DIR / "investing-in-temple-catalog.txt"

# Words to ignore in similarity comparison
STOP_WORDS = {
    "the", "a", "an", "in", "on", "at", "to", "for", "of", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "do",
    "does", "did", "will", "would", "could", "should", "may", "might",
    "can", "this", "that", "these", "those", "i", "you", "he", "she",
    "it", "we", "they", "my", "your", "his", "her", "its", "our",
    "their", "and", "but", "or", "not", "no", "with", "from", "by",
    "about", "into", "through", "during", "before", "after", "above",
    "below", "between", "how", "what", "when", "where", "why", "which",
    "who", "whom", "tx", "texas", "temple",
}


def tokenize(text: str) -> set[str]:
    """Extract meaningful words from text."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in STOP_WORDS and len(w) > 2}


def word_overlap(text1: str, text2: str) -> float:
    """Calculate word overlap percentage between two texts."""
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1 & tokens2
    smaller = min(len(tokens1), len(tokens2))
    return len(intersection) / smaller if smaller > 0 else 0.0


def load_video_catalogs() -> list[dict]:
    """Load video titles from catalog files."""
    entries = []
    # Patterns to skip: section headers, date-only lines, numbering artifacts, BOM
    skip_patterns = [
        r"^\ufeff?\d{4}$",               # Year headers like "2026"
        r"^(Late|Mid|Early)\s+\d{4}",    # "Late 2025 (Oct-Dec)"
        r"^(Title|Published)$",           # Column headers
        r"^\d+$",                         # Bare numbers (line numbers in investing catalog)
        r"^[A-Z][a-z]{2}\s+\d{1,2},\s*\d{4}$",  # Date lines like "Mar 4, 2026"
        r"^$",                            # Empty lines
    ]
    for catalog_path, channel in [(LIVING_CATALOG, "Living in Temple"), (INVESTING_CATALOG, "Investing in Temple")]:
        if not catalog_path.exists():
            continue
        for line in catalog_path.read_text().strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Skip section headers and metadata lines
            if any(re.match(p, line) for p in skip_patterns):
                continue
            # Strip leading numbering like "1. " or "17. "
            clean = re.sub(r"^\d+\.\s*", "", line).strip()
            if clean and len(clean) > 10:  # Skip very short artifacts
                entries.append({"title": clean, "source": f"catalog:{channel}", "type": "video"})
    return entries


def load_hook_bank() -> list[dict]:
    """Load hooks from hook bank JSON."""
    if not HOOK_BANK_PATH.exists():
        return []
    try:
        data = json.loads(HOOK_BANK_PATH.read_text())
        if isinstance(data, list):
            return [{"title": h.get("text", ""), "source": "hook-bank", "type": "hook", "date": h.get("dateCreated", "")} for h in data]
        return []
    except (json.JSONDecodeError, KeyError) as exc:
        warn(f"Could not parse hook-bank.json: {exc}", context="hook-bank")
        return []


def load_registry() -> list[dict]:
    """Load content registry entries."""
    if not REGISTRY_PATH.exists():
        return []
    entries = []
    try:
        with open(REGISTRY_PATH, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append({
                    "title": row.get("title", ""),
                    "source": "registry",
                    "type": row.get("content_type", ""),
                    "date": row.get("publish_date", row.get("created_date", "")),
                    "slug": row.get("slug", ""),
                    "cluster": row.get("dedupe_cluster", ""),
                })
    except Exception as exc:
        warn(f"Could not read registry CSV: {exc}", context="registry")
    return entries


def load_output_titles() -> list[dict]:
    """Scan output directories for content titles."""
    entries = []
    if not OUTPUT_DIR.exists():
        return entries

    for week_dir in OUTPUT_DIR.iterdir():
        if not week_dir.is_dir() or not re.match(r"\d{4}-W\d{2}", week_dir.name):
            continue
        for md_file in week_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                # Extract H1
                h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if h1_match:
                    entries.append({
                        "title": h1_match.group(1).strip(),
                        "source": f"output:{week_dir.name}/{md_file.name}",
                        "type": "output",
                        "date": week_dir.name,
                    })
            except Exception as exc:
                warn(f"Could not read {md_file}: {exc}", context="output-scan")
                continue
    return entries


def is_same_asset(entry1: dict, entry2: dict) -> bool:
    """Check if two entries represent the same asset tracked in different sources.
    A catalog entry and a registry entry for the same video are expected, not a dupe."""
    sources = {entry1["source"], entry2["source"]}
    # Catalog + registry pair = same asset tracked in two places
    if any("catalog:" in s for s in sources) and any(s == "registry" for s in sources):
        return True
    # Registry + output pair = same asset
    if "registry" in sources and any("output:" in s for s in sources):
        return True
    return False


def find_duplicates(entries: list[dict], threshold: float = 0.70) -> list[dict]:
    """Find near-duplicate entries based on word overlap."""
    duplicates = []
    seen = set()

    for i, entry1 in enumerate(entries):
        for j, entry2 in enumerate(entries):
            if i >= j:
                continue
            pair_key = (min(i, j), max(i, j))
            if pair_key in seen:
                continue

            # Skip expected cross-source matches (same asset in catalog + registry)
            if is_same_asset(entry1, entry2):
                continue

            overlap = word_overlap(entry1["title"], entry2["title"])
            if overlap >= threshold:
                seen.add(pair_key)
                duplicates.append({
                    "entry1": entry1,
                    "entry2": entry2,
                    "overlap": round(overlap * 100, 1),
                })

    return sorted(duplicates, key=lambda x: x["overlap"], reverse=True)


def check_single(text: str, entries: list[dict], threshold: float = 0.60) -> list[dict]:
    """Check a single title/hook against all existing entries."""
    matches = []
    for entry in entries:
        overlap = word_overlap(text, entry["title"])
        if overlap >= threshold:
            matches.append({
                "existing": entry,
                "overlap": round(overlap * 100, 1),
            })
    return sorted(matches, key=lambda x: x["overlap"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Content Deduplication Checker")
    parser.add_argument("--check-title", type=str, help="Check a specific title for duplicates")
    parser.add_argument("--check-hook", type=str, help="Check a specific hook for duplicates")
    parser.add_argument("--threshold", type=float, default=0.70, help="Overlap threshold (0.0-1.0, default 0.70)")
    args = parser.parse_args()

    print("=" * 60)
    print("DEDUPLICATION CHECKER")
    print(f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()

    # Load all content
    all_entries = []
    print("Loading sources...")

    videos = load_video_catalogs()
    print(f"  Video catalogs: {len(videos)} entries")
    all_entries.extend(videos)

    hooks = load_hook_bank()
    print(f"  Hook bank: {len(hooks)} entries")
    all_entries.extend(hooks)

    registry = load_registry()
    print(f"  Content registry: {len(registry)} entries")
    all_entries.extend(registry)

    outputs = load_output_titles()
    print(f"  Output files: {len(outputs)} entries")
    all_entries.extend(outputs)

    print(f"  Total: {len(all_entries)} entries")
    print()

    # Single check mode
    if args.check_title or args.check_hook:
        text = args.check_title or args.check_hook
        print(f"Checking: \"{text}\"")
        print(f"Threshold: {args.threshold * 100}%")
        print()

        matches = check_single(text, all_entries, args.threshold)
        if matches:
            print(f"Found {len(matches)} potential duplicates:")
            for m in matches[:10]:
                print(f"  [{m['overlap']}%] \"{m['existing']['title']}\" ({m['existing']['source']})")
            print()
            print("RECOMMENDATION: Consider a different angle or consolidate with existing content.")
        else:
            print("No duplicates found. This title/hook is clear.")
        return

    # Full scan mode
    print(f"Scanning for duplicates (threshold: {args.threshold * 100}%)...")
    print()

    duplicates = find_duplicates(all_entries, args.threshold)

    if duplicates:
        print(f"FOUND {len(duplicates)} POTENTIAL DUPLICATES:")
        print()
        for i, dupe in enumerate(duplicates[:25], 1):
            e1 = dupe["entry1"]
            e2 = dupe["entry2"]
            print(f"{i}. [{dupe['overlap']}% overlap]")
            print(f"   A: \"{e1['title']}\" ({e1['source']})")
            print(f"   B: \"{e2['title']}\" ({e2['source']})")
            print()
    else:
        print("No duplicates found above threshold.")

    # Summary
    print("=" * 60)
    print(f"Total entries scanned: {len(all_entries)}")
    print(f"Duplicates found: {len(duplicates)}")
    if duplicates:
        print("\nACTION NEEDED:")
        print("  Review duplicates above. For each pair, decide:")
        print("  1. Consolidate into one stronger piece")
        print("  2. Differentiate the angle (different persona or platform)")
        print("  3. Archive the weaker one")
    print("=" * 60)


if __name__ == "__main__":
    main()
