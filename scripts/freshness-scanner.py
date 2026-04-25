#!/usr/bin/env python3
"""
Content Freshness Scanner — templetxhomes.net Page Audit
Scans all HTML page files for:
  1. Stale dates (not updated in 60+ days)
  2. Missing video embeds (per VIDEO-TO-PAGE-MAP.md)
  3. Missing schema markup (VideoObject, FAQPage, Article)
  4. Outdated year references
  5. Missing key SEO elements

Outputs a prioritized update queue as Markdown.

Usage:
  python3 scripts/freshness-scanner.py
  python3 scripts/freshness-scanner.py --days 30        # stricter freshness threshold
  python3 scripts/freshness-scanner.py --output report  # save to output/ folder
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = PROJECT_ROOT.parent / "real-estate-redefined"
PAGE_QUEUE = SITE_ROOT / "page-build-queue" / "temple-tx-homes"
COMPLETE_DIR = SITE_ROOT / "Complete"
VIDEO_MAP_PATH = PROJECT_ROOT / "VIDEO-TO-PAGE-MAP.md"
OUTPUT_DIR = PROJECT_ROOT / "output"

CURRENT_YEAR = datetime.now().year
STALE_THRESHOLD_DAYS = 60

# Directories to skip
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv"}

# Schema types we check for
SCHEMA_TYPES = {
    "VideoObject": "Video embed schema — helps AI engines parse video content",
    "FAQPage": "FAQ schema — enables rich results and AI citation",
    "Article": "Article schema — establishes authorship and publish date",
    "RealEstateAgent": "Agent schema — entity declaration for AEO",
    "Person": "Person schema — Taylor Dasch entity markup",
}

# Key SEO elements
SEO_CHECKS = {
    "canonical": r'<link\s+rel=["\']canonical["\']',
    "meta_description": r'<meta\s+name=["\']description["\']',
    "og_title": r'<meta\s+property=["\']og:title["\']',
    "h1_tag": r"<h1[^>]*>",
}


def find_html_files() -> list[Path]:
    """Find all HTML files in the site directories, skipping node_modules etc."""
    html_files = []
    search_dirs = [COMPLETE_DIR, PAGE_QUEUE]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for root, dirs, files in os.walk(search_dir):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f.endswith(".html"):
                    html_files.append(Path(root) / f)

    return html_files


def parse_video_map() -> dict[str, dict]:
    """Parse VIDEO-TO-PAGE-MAP.md to get expected video embeds per page slug."""
    video_map = {}
    if not VIDEO_MAP_PATH.exists():
        return video_map

    content = VIDEO_MAP_PATH.read_text()

    # Parse Tier 1 table rows: | `/slug/` | "Video Title" | Channel |
    tier1_pattern = r"\|\s*`(/[^`]+/)`\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|"
    for match in re.finditer(tier1_pattern, content):
        slug = match.group(1).strip("/")
        video_title = match.group(2).strip().strip('"')
        channel = match.group(3).strip()
        video_map[slug] = {
            "title": video_title,
            "channel": channel,
            "tier": 1,
            "needs_filming": "FILM" in video_title.upper(),
        }

    # Parse Tier 2 table rows: | `/slug/` | "Video Needed" | Priority |
    tier2_section = content.split("Tier 2")[-1].split("Tier 3")[0] if "Tier 2" in content else ""
    for match in re.finditer(tier1_pattern, tier2_section):
        slug = match.group(1).strip("/")
        video_title = match.group(2).strip().strip('"')
        priority = match.group(3).strip()
        video_map[slug] = {
            "title": video_title,
            "channel": "TBD",
            "tier": 2,
            "needs_filming": True,
            "priority": priority,
        }

    return video_map


def analyze_html(filepath: Path, stale_days: int) -> dict:
    """Analyze a single HTML file for freshness issues."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {"error": str(e), "path": str(filepath)}

    issues = []
    info = {
        "path": str(filepath),
        "filename": filepath.name,
        "size_kb": round(filepath.stat().st_size / 1024, 1),
        "file_modified": datetime.fromtimestamp(filepath.stat().st_mtime),
        "issues": issues,
        "schemas_found": [],
        "has_video_embed": False,
        "severity_score": 0,  # Higher = more urgent
    }

    # --- Check 1: File modification date ---
    days_since_modified = (datetime.now() - info["file_modified"]).days
    if days_since_modified > stale_days:
        issues.append({
            "type": "stale_file",
            "severity": "high" if days_since_modified > 90 else "medium",
            "message": f"File not modified in {days_since_modified} days (threshold: {stale_days})",
        })
        info["severity_score"] += 3 if days_since_modified > 90 else 2

    # --- Check 2: Outdated year references ---
    previous_years = []
    for year in range(2024, CURRENT_YEAR):
        year_str = str(year)
        # Look for year in content context (not in URLs or version strings)
        year_refs = re.findall(
            rf"(?:Updated|updated|copyright|Copyright|\b{year_str}\s+(?:median|price|data|market|report|guide|playbook))",
            content,
        )
        if year_refs:
            previous_years.append(year_str)

    # Also check HTML comment headers like "Updated: March 2025"
    header_dates = re.findall(r"Updated:\s*\w+\s+(\d{4})", content)
    for hd in header_dates:
        if int(hd) < CURRENT_YEAR:
            if hd not in previous_years:
                previous_years.append(hd)

    if previous_years:
        issues.append({
            "type": "outdated_year",
            "severity": "high",
            "message": f"Contains references to outdated year(s): {', '.join(previous_years)}",
        })
        info["severity_score"] += 3

    # --- Check 3: Schema markup ---
    schemas_found = []
    for schema_type in SCHEMA_TYPES:
        if re.search(rf'"@type"\s*:\s*"{schema_type}"', content):
            schemas_found.append(schema_type)

    info["schemas_found"] = schemas_found

    missing_critical = []
    # Every page should have RealEstateAgent or Person
    if "RealEstateAgent" not in schemas_found and "Person" not in schemas_found:
        missing_critical.append("RealEstateAgent/Person (entity declaration)")
    # Pages with content should have Article
    if "Article" not in schemas_found and len(content) > 5000:
        missing_critical.append("Article")

    if missing_critical:
        issues.append({
            "type": "missing_schema",
            "severity": "medium",
            "message": f"Missing schema: {', '.join(missing_critical)}",
        })
        info["severity_score"] += 2

    # --- Check 4: Video embed ---
    has_iframe = bool(re.search(r"<iframe[^>]*youtube", content, re.IGNORECASE))
    has_video_embed = bool(re.search(r"youtube\.com/embed", content, re.IGNORECASE))
    info["has_video_embed"] = has_iframe or has_video_embed

    if not info["has_video_embed"]:
        # Check if VideoObject schema exists without an actual embed
        if "VideoObject" in schemas_found:
            issues.append({
                "type": "schema_no_embed",
                "severity": "low",
                "message": "VideoObject schema present but no YouTube iframe embed found",
            })
        else:
            issues.append({
                "type": "no_video",
                "severity": "medium",
                "message": "No YouTube video embed — pages with video get 3x more AI citations",
            })
            info["severity_score"] += 2

    # --- Check 5: SEO elements ---
    missing_seo = []
    for element, pattern in SEO_CHECKS.items():
        if not re.search(pattern, content, re.IGNORECASE):
            missing_seo.append(element)

    if missing_seo:
        issues.append({
            "type": "missing_seo",
            "severity": "low" if len(missing_seo) <= 1 else "medium",
            "message": f"Missing SEO elements: {', '.join(missing_seo)}",
        })
        info["severity_score"] += len(missing_seo)

    # --- Check 6: FAQ section ---
    has_faq = bool(re.search(r"FAQ|Frequently Asked|FAQPage", content, re.IGNORECASE))
    if not has_faq and len(content) > 10000:
        issues.append({
            "type": "no_faq",
            "severity": "low",
            "message": "No FAQ section found — FAQPage schema is a high-value AEO signal",
        })
        info["severity_score"] += 1

    # --- Check 7: dateModified in schema ---
    has_date_modified = bool(re.search(r'"dateModified"', content))
    if schemas_found and not has_date_modified:
        issues.append({
            "type": "no_date_modified",
            "severity": "medium",
            "message": "Schema exists but no dateModified — AI engines deprioritize undated content",
        })
        info["severity_score"] += 2

    return info


def match_video_map(results: list[dict], video_map: dict) -> list[dict]:
    """Cross-reference scan results with VIDEO-TO-PAGE-MAP.md."""
    for result in results:
        filepath = result["path"].lower()
        for slug, video_info in video_map.items():
            slug_parts = slug.strip("/").split("/")
            # Check if any slug part appears in the filepath
            if any(part in filepath for part in slug_parts if len(part) > 3):
                if not result["has_video_embed"] and not video_info.get("needs_filming"):
                    result["issues"].append({
                        "type": "video_map_mismatch",
                        "severity": "high",
                        "message": f"VIDEO-TO-PAGE-MAP says embed: \"{video_info['title']}\" ({video_info['channel']}) — but no video found on page",
                    })
                    result["severity_score"] += 3
                result["mapped_video"] = video_info
                break
    return results


def extract_page_slug(filepath: Path) -> str:
    """Extract a readable page identifier from the file path."""
    parts = filepath.parts
    # Try to find a meaningful folder name
    for i, part in enumerate(parts):
        if part in ("Complete", "completed", "output", "Completed -2000+ words"):
            if i + 1 < len(parts):
                return parts[i + 1]
    return filepath.stem


def generate_report(results: list[dict], stale_days: int) -> str:
    """Generate a Markdown report from scan results."""
    # Sort by severity (highest first)
    results.sort(key=lambda x: x.get("severity_score", 0), reverse=True)

    total = len(results)
    with_issues = sum(1 for r in results if r.get("issues"))
    high_severity = sum(1 for r in results if r.get("severity_score", 0) >= 5)
    no_video = sum(1 for r in results if not r.get("has_video_embed"))
    no_schema = sum(1 for r in results if not r.get("schemas_found"))

    report = []
    report.append("# Content Freshness Scanner Report")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Freshness threshold:** {stale_days} days")
    report.append(f"**Pages scanned:** {total}")
    report.append("")
    report.append("## Summary")
    report.append(f"- **Pages with issues:** {with_issues}/{total}")
    report.append(f"- **High severity (score 5+):** {high_severity}")
    report.append(f"- **No video embed:** {no_video}/{total}")
    report.append(f"- **No schema markup:** {no_schema}/{total}")
    report.append("")

    # --- Priority Update Queue ---
    report.append("## Priority Update Queue")
    report.append("Ranked by severity score (highest = most urgent).")
    report.append("")

    for i, result in enumerate(results[:20], 1):  # Top 20
        if not result.get("issues"):
            continue

        slug = extract_page_slug(Path(result["path"]))
        score = result.get("severity_score", 0)
        severity_label = "CRITICAL" if score >= 7 else "HIGH" if score >= 5 else "MEDIUM" if score >= 3 else "LOW"
        schemas = ", ".join(result.get("schemas_found", [])) or "None"
        video = "Yes" if result.get("has_video_embed") else "No"
        modified = result.get("file_modified", datetime.now()).strftime("%Y-%m-%d")

        report.append(f"### {i}. {slug} [{severity_label} — score {score}]")
        report.append(f"- **File:** `{result['path']}`")
        report.append(f"- **Last modified:** {modified}")
        report.append(f"- **Schema:** {schemas}")
        report.append(f"- **Video embed:** {video}")

        if result.get("mapped_video"):
            mv = result["mapped_video"]
            report.append(f"- **Mapped video:** \"{mv['title']}\" ({mv['channel']})")

        report.append("- **Issues:**")
        for issue in result["issues"]:
            severity_icon = {"high": "!!!", "medium": "!!", "low": "!"}.get(issue["severity"], "!")
            report.append(f"  - [{severity_icon}] {issue['message']}")
        report.append("")

    # --- Schema Coverage ---
    report.append("## Schema Coverage")
    schema_counts = defaultdict(int)
    for r in results:
        for s in r.get("schemas_found", []):
            schema_counts[s] += 1

    for schema_type, description in SCHEMA_TYPES.items():
        count = schema_counts.get(schema_type, 0)
        pct = round(count / total * 100) if total > 0 else 0
        bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
        report.append(f"- **{schema_type}:** {count}/{total} ({pct}%) [{bar}] — {description}")
    report.append("")

    # --- Clean Pages ---
    clean = [r for r in results if not r.get("issues")]
    if clean:
        report.append("## Clean Pages (no issues found)")
        for r in clean:
            slug = extract_page_slug(Path(r["path"]))
            schemas = ", ".join(r.get("schemas_found", [])) or "None"
            report.append(f"- {slug} — Schema: {schemas}, Video: {'Yes' if r.get('has_video_embed') else 'No'}")
        report.append("")

    # --- Recommendations ---
    report.append("## Top 3 Recommended Actions")
    actions = []

    if high_severity > 0:
        actions.append(f"1. **Fix {high_severity} high-severity pages** — These have outdated data or missing video embeds that VIDEO-TO-PAGE-MAP.md says should exist. Highest AEO impact per minute spent.")

    if no_schema > total * 0.3:
        actions.append(f"2. **Add RealEstateAgent + Article schema to {no_schema} pages** — Copy the schema block from any Complete/ page and update the slug/title. 5 min per page, massive AEO signal.")

    if no_video > total * 0.5:
        actions.append(f"3. **Embed videos on {no_video} pages** — Cross-reference VIDEO-TO-PAGE-MAP.md. Pages with embedded video get 3x more AI engine citations.")

    if len(actions) < 3:
        actions.append(f"{len(actions)+1}. **Run /transcript-to-blog on your most-viewed videos** — Convert YouTube watch time into citable, indexable blog pages.")

    report.extend(actions)
    report.append("")
    report.append("---")
    report.append("*Run this scanner weekly (Saturday per the content rhythm) to catch drift before it compounds.*")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Content Freshness Scanner for templetxhomes.net pages")
    parser.add_argument("--days", type=int, default=STALE_THRESHOLD_DAYS, help=f"Freshness threshold in days (default: {STALE_THRESHOLD_DAYS})")
    parser.add_argument("--output", choices=["print", "report"], default="print", help="Output mode: print to stdout or save report to output/")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of Markdown")
    args = parser.parse_args()

    print(f"Scanning pages in {SITE_ROOT}...")
    print(f"Freshness threshold: {args.days} days")
    print()

    # Find all HTML files
    html_files = find_html_files()
    if not html_files:
        print("No HTML files found. Check that real-estate-redefined/ exists.")
        return

    print(f"Found {len(html_files)} HTML files.")

    # Parse video map
    video_map = parse_video_map()
    print(f"Loaded {len(video_map)} video-to-page mappings.")
    print()

    # Analyze each file
    results = []
    for filepath in html_files:
        result = analyze_html(filepath, args.days)
        if "error" not in result:
            results.append(result)

    # Cross-reference with video map
    results = match_video_map(results, video_map)

    if args.json:
        # JSON output for programmatic use
        output = json.dumps(results, indent=2, default=str)
        print(output)
        return

    # Generate Markdown report
    report = generate_report(results, args.days)

    if args.output == "report":
        # Save to output folder
        today = datetime.now().strftime("%Y-%m-%d")
        report_dir = OUTPUT_DIR / "audits"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"freshness-scan-{today}.md"
        report_path.write_text(report)
        print(f"Report saved to: {report_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
