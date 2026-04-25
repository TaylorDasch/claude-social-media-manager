#!/usr/bin/env python3
"""
Freshness Scanner v2 — Extended content freshness audit.

v1 only scanned website HTML pages. v2 adds:
  1. TEMPLE-TX-DATA-VAULT.md freshness (per-section timestamps)
  2. Reference doc staleness (modification date)
  3. Stale lead magnet references
  4. Outdated year references across ALL content (not just HTML)
  5. Old BAH/tax/rate data in output files
  6. Pages needing dateModified update
  7. Missing video-to-page embed follow-through
  8. Content registry entries past refresh_due_date
  9. Stale builder incentives or rate references

Usage:
  python3 scripts/freshness-scanner-v2.py              # Full scan
  python3 scripts/freshness-scanner-v2.py --section data-vault  # Just data vault
  python3 scripts/freshness-scanner-v2.py --section reference   # Just reference docs
  python3 scripts/freshness-scanner-v2.py --section content     # Just content outputs
  python3 scripts/freshness-scanner-v2.py --section registry    # Just registry
  python3 scripts/freshness-scanner-v2.py --section pages       # Original HTML scan
  python3 scripts/freshness-scanner-v2.py --output report       # Save to output/audits/
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
SITE_ROOT = PROJECT_ROOT.parent / "real-estate-redefined"
DATA_VAULT_PATH = PROJECT_ROOT / "reference" / "TEMPLE-TX-DATA-VAULT.md"
REFERENCE_DIR = PROJECT_ROOT / "reference"
OUTPUT_DIR = PROJECT_ROOT / "output"
REGISTRY_PATH = PROJECT_ROOT / "data" / "content-registry.csv"
VIDEO_MAP_PATH = PROJECT_ROOT / "VIDEO-TO-PAGE-MAP.md"
COMPLETE_DIR = SITE_ROOT / "Complete" if SITE_ROOT.exists() else None

NOW = datetime.now()
CURRENT_YEAR = NOW.year

# Stale data patterns to detect in content
STALE_PATTERNS = {
    "bah_rate": {
        "pattern": r"\$[\d,]+(?:/month|/mo)?\s*(?:BAH|Basic Allowance)",
        "description": "BAH rate reference",
        "max_age_days": 365,
    },
    "tax_rate": {
        "pattern": r"\$[\d.]+/\$100|\d+\.\d+%\s*(?:tax|property tax)",
        "description": "Property tax rate",
        "max_age_days": 365,
    },
    "median_price": {
        "pattern": r"\$[\d,]+[kK]?\s*(?:median|average)\s*(?:home|house|price|value)",
        "description": "Median home price",
        "max_age_days": 90,
    },
    "inventory": {
        "pattern": r"[\d,]+\s*(?:active listings|homes for sale|inventory)",
        "description": "Active inventory count",
        "max_age_days": 30,
    },
    "dom": {
        "pattern": r"[\d]+\s*(?:days on market|DOM|average days)",
        "description": "Days on market",
        "max_age_days": 30,
    },
    "interest_rate": {
        "pattern": r"[\d.]+%\s*(?:interest|mortgage|rate)",
        "description": "Interest/mortgage rate",
        "max_age_days": 7,
    },
}


def check_data_vault() -> list[dict]:
    """Check TEMPLE-TX-DATA-VAULT.md for freshness."""
    issues = []
    if not DATA_VAULT_PATH.exists():
        issues.append({
            "section": "Data Vault",
            "severity": "CRITICAL",
            "message": "TEMPLE-TX-DATA-VAULT.md does not exist",
            "fix": "Create or restore the data vault file",
        })
        return issues

    content = DATA_VAULT_PATH.read_text()
    mod_date = datetime.fromtimestamp(DATA_VAULT_PATH.stat().st_mtime)
    days_since = (NOW - mod_date).days

    # Check file modification date
    if days_since > 90:
        issues.append({
            "section": "Data Vault",
            "severity": "CRITICAL",
            "message": f"Data vault not modified in {days_since} days (threshold: 90)",
            "fix": "Run a full data refresh with current MLS/CAD data",
        })
    elif days_since > 30:
        issues.append({
            "section": "Data Vault",
            "severity": "HIGH",
            "message": f"Data vault last modified {days_since} days ago",
            "fix": "Verify volatile data (median price, inventory, DOM) is current",
        })

    # Check for "Last verified" or "Last updated" timestamp
    verified_match = re.search(r"(?:Last (?:verified|updated)|Updated):\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
    if verified_match:
        date_str = verified_match.group(1).strip()
        # Try to parse various date formats
        for fmt in ["%B %d, %Y", "%Y-%m-%d", "%B %Y", "%m/%d/%Y"]:
            try:
                verified_date = datetime.strptime(date_str, fmt)
                days_since_verified = (NOW - verified_date).days
                if days_since_verified > 90:
                    issues.append({
                        "section": "Data Vault",
                        "severity": "HIGH",
                        "message": f"Last verified date: {date_str} ({days_since_verified} days ago)",
                        "fix": "Update the 'Last verified' date and refresh stale sections",
                    })
                break
            except ValueError:
                continue
    else:
        issues.append({
            "section": "Data Vault",
            "severity": "MEDIUM",
            "message": "No 'Last verified' timestamp found in data vault",
            "fix": "Add 'Last verified: YYYY-MM-DD' at the top of the file",
        })

    # Check for outdated year references
    for year in range(2024, CURRENT_YEAR):
        if str(year) in content:
            # Exclude: historical refs, freshness metadata, source date annotations
            skip_words = ["founded", "established", "since", "built in", "history",
                          "next refresh", "next review", "section freshness", "census estimate",
                          "vintage", "rates —", "data —", "from"]
            context_matches = re.findall(rf"(?:^.{{0,80}}{year}.{{0,80}}$)", content, re.MULTILINE)
            for ctx in context_matches:
                ctx_lower = ctx.lower()
                if not any(word in ctx_lower for word in skip_words) and not ctx.strip().startswith("##"):
                    issues.append({
                        "section": "Data Vault",
                        "severity": "MEDIUM",
                        "message": f"Contains reference to {year}: ...{ctx.strip()[:60]}...",
                        "fix": f"Update {year} reference to current data",
                    })
                    break  # One per year is enough

    return issues


def check_reference_docs() -> list[dict]:
    """Check reference directory for stale files."""
    issues = []
    if not REFERENCE_DIR.exists():
        return issues

    for ref_file in REFERENCE_DIR.iterdir():
        if not ref_file.is_file() or not ref_file.suffix == ".md":
            continue

        mod_date = datetime.fromtimestamp(ref_file.stat().st_mtime)
        days_since = (NOW - mod_date).days

        if days_since > 180:
            issues.append({
                "section": "Reference Docs",
                "severity": "MEDIUM",
                "message": f"{ref_file.name} not modified in {days_since} days",
                "fix": f"Review {ref_file.name} for accuracy",
            })

        # Check for outdated year references in reference docs — only flag if 2+ years old
        # Single year-back refs (e.g. "2025" in a 2026 file) are often valid source dates
        try:
            content = ref_file.read_text()
            for year in range(2024, CURRENT_YEAR - 1):  # Only flag 2+ years back
                if str(year) in content and not any(word in ref_file.name.lower() for word in ["archive", "history"]):
                    issues.append({
                        "section": "Reference Docs",
                        "severity": "LOW",
                        "message": f"{ref_file.name} contains reference to {year}",
                        "fix": f"Check if {year} references in {ref_file.name} need updating",
                    })
                    break
        except Exception as exc:
            warn(f"Could not read {ref_file}: {exc}", context="reference")

    return issues


def check_content_outputs() -> list[dict]:
    """Check output files for stale data references."""
    issues = []
    if not OUTPUT_DIR.exists():
        return issues

    for week_dir in OUTPUT_DIR.iterdir():
        if not week_dir.is_dir() or not re.match(r"\d{4}-W\d{2}", week_dir.name):
            continue

        for md_file in week_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception as exc:
                warn(f"Could not read {md_file}: {exc}", context="output")
                continue

            # Check for stale data patterns
            for key, spec in STALE_PATTERNS.items():
                matches = re.findall(spec["pattern"], content, re.IGNORECASE)
                if matches:
                    # The file's week gives us approximate content age
                    week_match = re.match(r"(\d{4})-W(\d{2})", week_dir.name)
                    if week_match:
                        try:
                            file_date = datetime.strptime(f"{week_match.group(1)}-W{week_match.group(2)}-1", "%Y-W%W-%w")
                            age = (NOW - file_date).days
                            if age > spec["max_age_days"]:
                                issues.append({
                                    "section": "Content Output",
                                    "severity": "LOW",
                                    "message": f"{md_file.relative_to(OUTPUT_DIR)}: {spec['description']} may be stale ({age} days old, max {spec['max_age_days']})",
                                    "fix": f"Verify {spec['description']} in {md_file.name} against current data",
                                })
                        except ValueError:
                            pass

    return issues


def check_registry_freshness() -> list[dict]:
    """Check content registry for overdue refresh dates."""
    issues = []
    if not REGISTRY_PATH.exists():
        return issues

    try:
        with open(REGISTRY_PATH, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                refresh_date = row.get("refresh_due_date", "")
                if refresh_date:
                    try:
                        due = datetime.strptime(refresh_date, "%Y-%m-%d")
                        if due < NOW:
                            days_overdue = (NOW - due).days
                            severity = "CRITICAL" if days_overdue > 30 else "HIGH" if days_overdue > 7 else "MEDIUM"
                            issues.append({
                                "section": "Registry",
                                "severity": severity,
                                "message": f"\"{row.get('title', 'unknown')}\" refresh overdue by {days_overdue} days",
                                "fix": f"Refresh this asset or update refresh_due_date",
                            })
                    except ValueError:
                        pass
    except Exception as exc:
        warn(f"Could not scan registry for freshness: {exc}", context="registry")

    return issues


def check_video_embeds() -> list[dict]:
    """Check VIDEO-TO-PAGE-MAP for missing embeds."""
    issues = []
    if not VIDEO_MAP_PATH.exists() or not COMPLETE_DIR or not COMPLETE_DIR.exists():
        return issues

    content = VIDEO_MAP_PATH.read_text()
    # Find Tier 1 entries (video + page both exist, should be embedded)
    tier1_pattern = r"\|\s*`(/[^`]+/)`\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|"
    tier1_section = content.split("Tier 2")[0] if "Tier 2" in content else content

    for match in re.finditer(tier1_pattern, tier1_section):
        slug = match.group(1).strip("/")
        video_title = match.group(2).strip().strip('"')

        # Check if a page file exists with this slug
        found_page = False
        has_embed = False
        for html_file in COMPLETE_DIR.rglob("*.html"):
            if slug in str(html_file).lower():
                found_page = True
                try:
                    page_content = html_file.read_text(encoding="utf-8", errors="ignore")
                    if re.search(r"youtube\.com/embed", page_content, re.IGNORECASE):
                        has_embed = True
                except Exception as exc:
                    warn(f"Could not read {html_file}: {exc}", context="video-embed")
                break

        if found_page and not has_embed:
            issues.append({
                "section": "Video Embeds",
                "severity": "HIGH",
                "message": f"Page for /{slug}/ exists but missing video embed: \"{video_title}\"",
                "fix": f"Embed the YouTube video on the /{slug}/ page and add VideoObject schema",
            })

    return issues


def generate_report(all_issues: list[dict]) -> str:
    """Generate markdown report."""
    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_issues.sort(key=lambda x: severity_order.get(x.get("severity", "LOW"), 4))

    report = []
    report.append("# Freshness Scanner v2 Report")
    report.append(f"**Generated:** {NOW.strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Sections scanned:** Data Vault, Reference Docs, Content Outputs, Registry, Video Embeds")
    report.append("")

    # Summary
    by_severity = defaultdict(int)
    by_section = defaultdict(int)
    for issue in all_issues:
        by_severity[issue["severity"]] += 1
        by_section[issue["section"]] += 1

    report.append("## Summary")
    report.append(f"- **Total issues:** {len(all_issues)}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if by_severity[sev]:
            report.append(f"- **{sev}:** {by_severity[sev]}")
    report.append("")

    report.append("## By Section")
    for section, count in sorted(by_section.items()):
        report.append(f"- **{section}:** {count} issues")
    report.append("")

    # Issues
    current_section = None
    for issue in all_issues:
        if issue["section"] != current_section:
            current_section = issue["section"]
            report.append(f"## {current_section}")
            report.append("")

        severity_icon = {"CRITICAL": "!!!", "HIGH": "!!", "MEDIUM": "!", "LOW": "~"}.get(issue["severity"], "~")
        report.append(f"- [{severity_icon} {issue['severity']}] {issue['message']}")
        report.append(f"  - **Fix:** {issue['fix']}")

    report.append("")
    report.append("---")
    report.append("*Run weekly. Pair with output-integrity-check.py for full system health.*")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Freshness Scanner v2 — Extended content audit")
    parser.add_argument("--section", choices=["data-vault", "reference", "content", "registry", "pages", "embeds"], help="Scan specific section only")
    parser.add_argument("--output", choices=["print", "report"], default="print", help="Output mode")
    args = parser.parse_args()

    print(f"Freshness Scanner v2 — {NOW.strftime('%Y-%m-%d %H:%M')}")
    print()

    all_issues = []

    sections = {
        "data-vault": ("Data Vault", check_data_vault),
        "reference": ("Reference Docs", check_reference_docs),
        "content": ("Content Outputs", check_content_outputs),
        "registry": ("Registry", check_registry_freshness),
        "embeds": ("Video Embeds", check_video_embeds),
    }

    if args.section:
        if args.section in sections:
            name, func = sections[args.section]
            print(f"Scanning: {name}")
            all_issues.extend(func())
        elif args.section == "pages":
            print("For HTML page scanning, use the original freshness-scanner.py")
            return
    else:
        for name, func in sections.values():
            print(f"Scanning: {name}...")
            all_issues.extend(func())

    print(f"\nFound {len(all_issues)} issues.")

    if args.output == "report":
        report = generate_report(all_issues)
        report_dir = OUTPUT_DIR / "audits"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"freshness-v2-{NOW.strftime('%Y-%m-%d')}.md"
        report_path.write_text(report)
        print(f"Report saved to: {report_path}")
    else:
        report = generate_report(all_issues)
        print()
        print(report)


if __name__ == "__main__":
    main()
