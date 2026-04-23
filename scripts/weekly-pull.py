#!/usr/bin/env python3
"""Weekly analytics pull — closes the self-improvement loop.

Pulls last 7 days of platform data directly from platform APIs (YouTube Data
v3, Beehiiv v2, FUB v1) using keys from ~/shared-keys.env. Appends rows to
data/performance-ledger.csv so /weekly-scorecard and /content-calendar can
read real numbers instead of asking Taylor.

Runs Sunday 6am via cron. Skips any platform whose API key is missing (logs
via warn() — never silent). Stdlib only; no pip install required.

Usage:
  python3 scripts/weekly-pull.py              # Run the pull
  python3 scripts/weekly-pull.py --dry-run    # Don't write to ledger

Rollback (this week's additions):
  git checkout -- data/performance-ledger.csv
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Optional

from common import (
    PERFORMANCE_LEDGER_PATH,
    info,
    warn,
)

NOW = datetime.now(timezone.utc)
WEEK_AGO = NOW - timedelta(days=7)

# Match existing ledger schema (from data/performance-ledger.csv header)
LEDGER_COLUMNS = [
    "date", "content_id", "platform", "impressions", "ctr_pct",
    "watch_time_hrs", "avg_view_duration_sec", "saves", "shares",
    "comments", "replies", "dms", "email_replies", "booked_calls",
    "page_visits", "ranking_notes", "deal_conversations",
    "taylor_rating", "taylor_notes",
]


def http_get_json(
    url: str, *, context: str, headers: Optional[dict] = None
) -> Optional[dict]:
    """GET a URL, return parsed JSON. Warns on failure, returns None."""
    try:
        req = urllib.request.Request(
            url, headers=headers or {"User-Agent": "weekly-pull/1.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        warn(f"HTTP {exc.code} on {url[:80]}: {exc.reason}", context=context)
        return None
    except Exception as exc:
        warn(f"HTTP GET failed ({url[:80]}): {exc}", context=context)
        return None


# ── YouTube ──
def pull_youtube() -> list[dict]:
    """Pull YouTube videos published in last 7 days + their stats."""
    api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    channel_id = os.environ.get("YOUTUBE_CHANNEL_ID", "").strip()
    if not api_key or not channel_id:
        warn(
            "YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID missing in ~/shared-keys.env; "
            "skipping YouTube pull",
            context="youtube",
        )
        return []

    published_after = WEEK_AGO.strftime("%Y-%m-%dT%H:%M:%SZ")
    search_url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?part=id&channelId={channel_id}"
        f"&publishedAfter={published_after}"
        f"&type=video&maxResults=25&key={api_key}"
    )
    search = http_get_json(search_url, context="youtube-search")
    if not search:
        return []

    video_ids = [
        item["id"]["videoId"]
        for item in search.get("items", [])
        if item.get("id", {}).get("videoId")
    ]
    if not video_ids:
        info("YouTube: no videos published in last 7 days")
        return []

    stats_url = (
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=statistics,snippet,contentDetails"
        f"&id={','.join(video_ids)}&key={api_key}"
    )
    stats = http_get_json(stats_url, context="youtube-videos")
    if not stats:
        return []

    today = NOW.strftime("%Y-%m-%d")
    rows: list[dict] = []
    for item in stats.get("items", []):
        video_id = item.get("id", "")
        s = item.get("statistics", {})
        title = (item.get("snippet", {}).get("title") or "")[:80]
        rows.append({
            "date": today,
            "content_id": video_id,
            "platform": "youtube",
            "impressions": s.get("viewCount", ""),
            "comments": s.get("commentCount", ""),
            "shares": s.get("likeCount", ""),  # likes as engagement proxy
            "ranking_notes": f"auto-pulled: {title}",
            "taylor_notes": "weekly-pull",
        })
    info(f"YouTube: {len(rows)} video(s) from last 7 days")
    return rows


# ── Beehiiv ──
def pull_beehiiv() -> list[dict]:
    """Pull Beehiiv posts sent in last 7 days across configured publications."""
    api_key = os.environ.get("BEEHIIV_API_KEY", "").strip()
    if not api_key:
        warn(
            "BEEHIIV_API_KEY missing in ~/shared-keys.env; skipping Beehiiv pull",
            context="beehiiv",
        )
        return []

    # Accept either a single or comma-separated list of publication IDs.
    # Temple Insider + Investor Brief each have their own. Set:
    #   BEEHIIV_PUBLICATION_IDS=pub_XXX,pub_YYY
    raw_ids = os.environ.get("BEEHIIV_PUBLICATION_IDS", "").strip()
    if not raw_ids:
        raw_ids = os.environ.get("BEEHIIV_PUBLICATION_ID", "").strip()
    if not raw_ids:
        warn(
            "BEEHIIV_PUBLICATION_IDS not set. Find yours with:\n"
            "  curl -H 'Authorization: Bearer $BEEHIIV_API_KEY' "
            "https://api.beehiiv.com/v2/publications\n"
            "Then add to ~/shared-keys.env:\n"
            "  BEEHIIV_PUBLICATION_IDS=pub_INSIDER_ID,pub_INVESTOR_ID",
            context="beehiiv",
        )
        return []

    pub_ids = [p.strip() for p in raw_ids.split(",") if p.strip()]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "weekly-pull/1.0",
    }
    rows: list[dict] = []
    today = NOW.strftime("%Y-%m-%d")
    week_ago_ts = int(WEEK_AGO.timestamp())

    for pub_id in pub_ids:
        posts_url = (
            f"https://api.beehiiv.com/v2/publications/{pub_id}/posts"
            f"?status=confirmed&limit=25&expand=stats"
        )
        data = http_get_json(posts_url, context="beehiiv", headers=headers)
        if not data:
            continue
        for post in data.get("data", []):
            published_at = post.get("publish_date") or 0
            if not isinstance(published_at, int) or published_at < week_ago_ts:
                continue
            stats = post.get("stats", {}) or {}
            email = stats.get("email", {}) or {}
            rows.append({
                "date": today,
                "content_id": post.get("id", ""),
                "platform": "beehiiv",
                "impressions": email.get("recipients", ""),
                "ctr_pct": email.get("click_rate", ""),
                "saves": email.get("open_rate", ""),  # repurpose col for open-rate
                "ranking_notes": f"auto-pulled: {post.get('title', '')[:80]}",
                "taylor_notes": "weekly-pull",
            })
    info(f"Beehiiv: {len(rows)} post(s) from last 7 days across {len(pub_ids)} pub(s)")
    return rows


# ── FUB (new leads by source, aggregated into one row per source) ──
def pull_fub() -> list[dict]:
    """Pull FUB new people created in last 7 days, aggregated by source tag."""
    api_key = os.environ.get("FUB_API_KEY", "").strip()
    if not api_key:
        warn(
            "FUB_API_KEY missing in ~/shared-keys.env; skipping FUB pull",
            context="fub",
        )
        return []

    system_key = os.environ.get("FUB_X_SYSTEM_KEY", "").strip()
    system_name = os.environ.get("FUB_X_SYSTEM", "TaylorDaschOps").strip()
    auth = base64.b64encode(f"{api_key}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "User-Agent": "weekly-pull/1.0",
    }
    if system_key:
        headers["X-System"] = system_name
        headers["X-System-Key"] = system_key

    created_after = WEEK_AGO.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (
        "https://api.followupboss.com/v1/people"
        f"?createdAfter={urllib.parse.quote(created_after)}&limit=100"
    )
    data = http_get_json(url, context="fub", headers=headers)
    if not data:
        return []

    by_source: dict[str, int] = {}
    for person in data.get("people", []):
        source = (person.get("source") or "unknown").strip().lower() or "unknown"
        by_source[source] = by_source.get(source, 0) + 1

    today = NOW.strftime("%Y-%m-%d")
    rows: list[dict] = []
    for source, count in sorted(by_source.items(), key=lambda kv: -kv[1]):
        rows.append({
            "date": today,
            "content_id": f"fub-{source}",
            "platform": "fub",
            "impressions": count,  # lead count as impressions-proxy
            "ranking_notes": f"new leads from {source} this week",
            "taylor_notes": "weekly-pull",
        })
    info(f"FUB: {sum(by_source.values())} new leads across {len(by_source)} sources")
    return rows


# ── Writer ──
def append_to_ledger(rows: list[dict], *, dry_run: bool = False) -> None:
    """Append rows to performance-ledger.csv, creating header if missing."""
    if not rows:
        return
    if dry_run:
        info(f"[DRY RUN] Would append {len(rows)} rows (skipping write)")
        for row in rows[:5]:
            info(f"  {row.get('platform')}: {row.get('content_id')} "
                 f"— impressions={row.get('impressions')}")
        return

    needs_header = not PERFORMANCE_LEDGER_PATH.exists()
    with PERFORMANCE_LEDGER_PATH.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LEDGER_COLUMNS)
        if needs_header:
            writer.writeheader()
        for row in rows:
            full = {col: row.get(col, "") for col in LEDGER_COLUMNS}
            writer.writerow(full)
    info(f"Appended {len(rows)} rows → {PERFORMANCE_LEDGER_PATH.name}")


# ── Main ──
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be added; don't write to the ledger."
    )
    args = parser.parse_args()

    info(f"Weekly analytics pull — {NOW.strftime('%Y-%m-%d %H:%M UTC')}")
    info(f"Window: {WEEK_AGO.strftime('%Y-%m-%d')} → {NOW.strftime('%Y-%m-%d')}")
    info("-" * 60)

    all_rows: list[dict] = []
    all_rows.extend(pull_youtube())
    all_rows.extend(pull_beehiiv())
    all_rows.extend(pull_fub())

    if not all_rows:
        warn(
            "weekly-pull returned 0 rows. Verify keys in ~/shared-keys.env "
            "and platform connectivity.",
            context="weekly-pull",
        )
        return 1

    append_to_ledger(all_rows, dry_run=args.dry_run)
    info(f"\n✓ Weekly pull complete — {len(all_rows)} row(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
