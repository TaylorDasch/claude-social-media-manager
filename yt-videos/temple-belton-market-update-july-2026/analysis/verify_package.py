#!/usr/bin/env python3
"""Verify the local Temple/Belton market-update production package."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


REPO = Path("/Users/taylordasch_1/claude-social-media-manager")
PACKAGE = REPO / "yt-videos/temple-belton-market-update-july-2026"
OUTPUT = REPO / "output/2026-W30/produced/temple-belton-market-update-july-2026"
TITLE = "Temple & Belton Housing Market: The 60-Day Listing Test"
GATE_MARKER = "FILMING GATE — CLEARED"
UNCLEARED_GATE_MARKER = "FILMING GATE — NOT CLEARED"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    required_package = [
        "README.md",
        "RESEARCH.md",
        "PRODUCTION-BIBLE.md",
        "HOOK-LAB.md",
        "PACKAGING-LAB.md",
        "THUMBNAIL-BRIEF.md",
        "SCRIPT.md",
        "SHOT-LIST.md",
        "FILM-DAY-CHECKLIST.md",
        "SHORTS-PLAN.md",
        "QUALITY-REVIEW.md",
        "COMPANION-PAGE-REFRESH-BRIEF.md",
        "council-prompt.md",
        "analysis/analyze_market.py",
        "analysis/test_analysis.py",
        "analysis/verify_package.py",
    ]
    required_output = [
        "youtube-description.md",
        "youtube-tags.md",
        "pinned-comment.md",
        "youtube-short.md",
        "instagram-reel.md",
        "social-captions.md",
        "blog-outline.md",
        "newsletter-segment.md",
        "gmb-post.md",
        "community-post.md",
        "PRODUCTION-CHECKLIST.md",
    ]
    for relative in required_package:
        assert (PACKAGE / relative).is_file(), f"missing package file: {relative}"
    for relative in required_output:
        assert (OUTPUT / relative).is_file(), f"missing output file: {relative}"

    for relative in (
        "README.md",
        "PRODUCTION-BIBLE.md",
        "PACKAGING-LAB.md",
        "THUMBNAIL-BRIEF.md",
        "SCRIPT.md",
        "council-prompt.md",
    ):
        assert TITLE in read(PACKAGE / relative), f"title drift: {relative}"

    for relative in ("README.md", "PRODUCTION-BIBLE.md", "SCRIPT.md", "HOOK-LAB.md"):
        assert GATE_MARKER in read(PACKAGE / relative), f"missing filming gate: {relative}"

    public_data_assets = (
        "youtube-description.md",
        "youtube-short.md",
        "instagram-reel.md",
        "social-captions.md",
        "blog-outline.md",
        "newsletter-segment.md",
        "gmb-post.md",
        "community-post.md",
        "pinned-comment.md",
    )
    for relative in public_data_assets:
        assert "Central Texas MLS" in read(OUTPUT / relative), f"missing MLS notice: {relative}"

    comparison_notice_package = (
        "RESEARCH.md",
        "PRODUCTION-BIBLE.md",
        "SCRIPT.md",
        "QUALITY-REVIEW.md",
        "COMPANION-PAGE-REFRESH-BRIEF.md",
        "council-prompt.md",
    )
    for relative in comparison_notice_package:
        content = read(PACKAGE / relative)
        assert "as of May 14 and July 20, 2026" in content, (
            f"missing May–July Active notice: {relative}"
        )
        assert "April 15–May 14 and June 21–July 20, 2026" in content, (
            f"missing Closed-sample comparison notice: {relative}"
        )
    for relative in ("youtube-description.md", "blog-outline.md"):
        content = read(OUTPUT / relative)
        assert "as of May 14 and July 20, 2026" in content, (
            f"missing public May–July Active notice: {relative}"
        )
        assert "April 15–May 14 and June 21–July 20, 2026" in content, (
            f"missing public Closed-sample comparison notice: {relative}"
        )
    assert "02:06 The 83 vs 50 closing-sample guardrail" in read(
        OUTPUT / "youtube-description.md"
    ), "chapter wording implies a marketwide speed trend"

    all_package_and_output = "\n".join(
        read(PACKAGE / relative)
        for relative in required_package
        if Path(relative).suffix == ".md"
    ) + "\n" + "\n".join(read(OUTPUT / relative) for relative in required_output)
    # Research/audit docs preserve rejected wording and old-source notes for
    # traceability. Apply stale-claim patterns to the assets that actually guide
    # narration, graphics, filming, or distribution, then validate source/gate
    # metadata in the audit docs separately below.
    claim_bearing_package = (
        "README.md",
        "PRODUCTION-BIBLE.md",
        "HOOK-LAB.md",
        "PACKAGING-LAB.md",
        "THUMBNAIL-BRIEF.md",
        "SCRIPT.md",
        "SHOT-LIST.md",
        "FILM-DAY-CHECKLIST.md",
        "SHORTS-PLAN.md",
        "COMPANION-PAGE-REFRESH-BRIEF.md",
    )
    package_and_output = "\n".join(
        read(PACKAGE / relative) for relative in claim_bearing_package
    ) + "\n" + "\n".join(read(OUTPUT / relative) for relative in required_output)
    forbidden = (
        r"sold\s+faster",
        r"got there\s+\d+\s+days faster",
        r"Your Offer Changes After Day 60",
        r"under 30 days had cut",
        r"after day 60 it was two in three",
        r"29-day versus 103-day",
        r"Taylor Dasch Market Monitor analysis of local MLS exports",
        r"calendly\.com/taylordasch",
        r"FILMING GATE\s+—\s+NOT CLEARED",
        r"as of July 19, 2026",
        r"Data cutoff:[^\n]*2026-07-19",
        r"(?:current pull|current snapshot|active snapshot)[^\n]*(?:2026-07-19|July 19)",
        (
            r"(?:2026-07-19|July 19)[^\n]*(?:current active|"
            r"active (?:section|snapshot|inventory)|recent closings)"
        ),
        r"June 18(?:, 2026)?\s+(?:through|to|–|-)\s+July 17",
        r"active status (?:is )?inferred from the first stable Matrix block",
        r"July (?:first|inferred active) Matrix block",
        r"11%\s+vs\s+81%",
        r"11\.4%",
        r"48\.6%",
        r"66\.1%",
        r"80\.9%",
        r"99\.83%",
        r"\b881\s+(?:active|inferred|rows)",
        r"\b880\s+unique",
        r"\b488\s*/\s*881\b",
        r"\b227\s+(?:of|/)\s*881\b",
        r"\b55\.4%",
        r"\b25\.8%",
        r"\b109\s+(?:vs|versus)\s+65\b",
        r"\b90\+\s+DAYS\b",
    )
    for pattern in forbidden:
        assert not re.search(pattern, package_and_output, re.IGNORECASE), (
            f"stale phrase: {pattern}"
        )

    script = read(PACKAGE / "SCRIPT.md")
    spoken_sections = script.split("## 0:00–0:28", 1)[1].split("## Editor source footer", 1)[0]
    spoken = re.sub(r"(?s)\[[^\]]*\]", " ", spoken_sections)
    spoken = re.sub(r"(?m)^#{1,6}.*$", " ", spoken)
    spoken = re.sub(r"(?m)^`.*$", " ", spoken)
    spoken = re.sub(r"(?m)^\*\*.*$", " ", spoken)
    word_count = len(re.findall(r"[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*", spoken))
    # At the intended 150 wpm delivery, 1,500 spoken words is 10:00 exactly.
    assert 1_350 <= word_count <= 1_500, f"script word count drift: {word_count}"

    expected_sections = (
        "0:00–0:28",
        "0:28–0:58",
        "0:58–1:23",
        "1:23–2:06",
        "2:06–2:52",
        "2:52–3:40",
        "3:40–4:25",
        "4:25–5:24",
        "5:24–6:51",
        "6:51–7:56",
        "7:56–8:35",
        "8:35–9:11",
    )
    for timing in expected_sections:
        assert timing in script, f"missing script timing: {timing}"
        assert timing in read(PACKAGE / "PRODUCTION-BIBLE.md"), f"bible timing drift: {timing}"

    with (REPO / "data/content-registry.csv").open(newline="", encoding="utf-8-sig") as handle:
        registry = list(csv.DictReader(handle))
    ids = Counter(row["content_id"] for row in registry)
    assert not [key for key, count in ids.items() if count > 1], "duplicate registry IDs"
    record = next(row for row in registry if row["content_id"] == "YT-PREP-017")
    assert record["title"] == TITLE
    assert record["status"] == "READY_TO_FILM"

    hook_bank = json.loads(read(REPO / "data/hook-bank.json"))
    hook_ids = Counter(item["id"] for item in hook_bank)
    assert not [key for key, count in hook_ids.items() if count > 1], "duplicate hook IDs"
    hook = next(item for item in hook_bank if item["id"] == "HK-021")
    assert "0-to-30-day group" in hook["text"]

    assert "https://calendly.com/dealswithdasch" in script
    assert "Taylor Dasch with EG Realty" in script
    assert UNCLEARED_GATE_MARKER not in all_package_and_output
    for relative in ("RESEARCH.md", "QUALITY-REVIEW.md", "council-prompt.md"):
        audit_text = read(PACKAGE / relative)
        assert "whole-market-with-status-2026-07-20.csv" in audit_text, (
            f"current source metadata missing: {relative}"
        )
        assert "2026-07-20" in audit_text or "July 20, 2026" in audit_text, (
            f"current source date missing: {relative}"
        )
        assert "Status" in audit_text and "PropertyType" in audit_text, (
            f"explicit-field method missing: {relative}"
        )
    assert "whole-market-with-status-2026-07-20.csv" in package_and_output
    assert "as of July 20, 2026" in package_and_output
    assert "14% vs 81%" in read(PACKAGE / "THUMBNAIL-BRIEF.md")
    assert "0–30 DAYS" in read(PACKAGE / "THUMBNAIL-BRIEF.md")
    assert "91+ DAYS" in read(PACKAGE / "THUMBNAIL-BRIEF.md")

    print(json.dumps({
        "status": "PASS",
        "required_package_files": len(required_package),
        "required_output_files": len(required_output),
        "public_assets_with_mls_notice": len(public_data_assets),
        "script_word_count": word_count,
        "title_characters": len(TITLE),
        "registry_id": record["content_id"],
        "filming_gate": "CLEARED",
    }, indent=2))


if __name__ == "__main__":
    main()
