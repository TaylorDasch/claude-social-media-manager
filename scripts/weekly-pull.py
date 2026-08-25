#!/usr/bin/env python3
"""Weekly analytics pull — closes the self-improvement loop.

Pulls a weekly platform window directly from platform APIs (YouTube Data v3,
optional YouTube Analytics v2 and Reporting v1, Beehiiv v2, FUB v1). Appends rows to
data/performance-ledger.csv so /weekly-scorecard and /content-calendar can
read real numbers instead of asking Taylor.

YouTube measurement boundary:
  Starting 2026-08-24, public ``viewCount`` includes first-frame/autoplay
  starts. It is kept as a labeled public surface signal only and is never
  written into the ledger's ``impressions`` field. If the read-only YouTube
  OAuth grant is available in macOS Keychain, the pull refreshes a short-lived
  token in memory and records engaged views, watch time, AVD, average
  percentage viewed, and 30-second retention. An explicitly provisioned
  YouTube Reporting reach job supplies registered thumbnail impressions and
  impressions CTR; those fields remain blank while its daily CSV is pending.
  YouTube owner metrics use the same seven completed Pacific days, ending
  three days before the run so delayed bulk reports are not silently partial.

Runs Sunday 6am via cron. Skips any platform whose API key is missing (logs
via warn() — never silent). Stdlib only; no pip install required.

Usage:
  python3 scripts/weekly-pull.py --live              # Run the pull
  python3 scripts/weekly-pull.py --live --dry-run    # Don't write to ledger
  python3 scripts/weekly-pull.py --live --dry-run --platform youtube
                                                      # Pull only YouTube

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
from datetime import date, datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

from common import (
    PERFORMANCE_LEDGER_PATH,
    info,
    warn,
)
from youtube_analytics_oauth import YouTubeOAuthError, get_access_token
from youtube_reporting import (
    ReachMetricsResult,
    YouTubeReportingError,
    pull_reach_metrics,
)

NOW = datetime.now(timezone.utc)
WEEK_AGO = NOW - timedelta(days=7)
YOUTUBE_REPORT_TIMEZONE = ZoneInfo("America/Los_Angeles")
YOUTUBE_REPORT_LAG_DAYS = 3
YOUTUBE_WINDOW_END = (
    NOW.astimezone(YOUTUBE_REPORT_TIMEZONE).date()
    - timedelta(days=YOUTUBE_REPORT_LAG_DAYS)
)
YOUTUBE_WINDOW_START = YOUTUBE_WINDOW_END - timedelta(days=6)
YOUTUBE_VIEW_COUNT_BREAK = date(2026, 8, 24)
YOUTUBE_ANALYTICS_METRICS = (
    "engagedViews,estimatedMinutesWatched,averageViewDuration,"
    "averageViewPercentage"
)

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
        parsed = urllib.parse.urlsplit(url)
        safe_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
        warn(f"HTTP {exc.code} on {safe_url}: {exc.reason}", context=context)
        return None
    except Exception as exc:
        parsed = urllib.parse.urlsplit(url)
        safe_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
        warn(f"HTTP GET failed ({safe_url}): {exc}", context=context)
        return None


# ── YouTube ──
def parse_iso8601_duration(value: str) -> int:
    """Parse the hour/minute/second subset returned by YouTube Data API."""
    import re

    match = re.fullmatch(
        r"P(?:\d+D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or ""
    )
    if not match:
        return 0
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def parse_result_table(data: Optional[dict]) -> list[dict]:
    """Convert a YouTube Analytics result table into named dictionaries."""
    if not data:
        return []
    names = [header.get("name", "") for header in data.get("columnHeaders", [])]
    if not names:
        return []
    return [dict(zip(names, row)) for row in data.get("rows", [])]


def pull_youtube_retention(
    video_id: str,
    duration_seconds: int,
    *,
    access_token: str,
    channel_id: str,
) -> Optional[float]:
    """Return the nearest available audienceWatchRatio at 30 seconds."""
    if duration_seconds < 30:
        return None
    query = urllib.parse.urlencode({
        "ids": f"channel=={channel_id}",
        "startDate": YOUTUBE_WINDOW_START.isoformat(),
        "endDate": YOUTUBE_WINDOW_END.isoformat(),
        "metrics": "audienceWatchRatio",
        "dimensions": "elapsedVideoTimeRatio",
        "filters": f"video=={video_id}",
        "sort": "elapsedVideoTimeRatio",
    })
    data = http_get_json(
        f"https://youtubeanalytics.googleapis.com/v2/reports?{query}",
        context=f"youtube-retention:{video_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "weekly-pull/1.1",
        },
    )
    rows = parse_result_table(data)
    if not rows:
        return None
    target_ratio = 30 / duration_seconds
    nearest = min(
        rows,
        key=lambda row: abs(float(row.get("elapsedVideoTimeRatio", 0)) - target_ratio),
    )
    try:
        return round(float(nearest["audienceWatchRatio"]) * 100, 2)
    except (KeyError, TypeError, ValueError):
        return None


def pull_youtube_private_metrics(
    video_ids: list[str], durations: dict[str, int], *, channel_id: str
) -> dict[str, dict]:
    """Pull owner-only metrics using the read-only Keychain OAuth grant."""
    try:
        access_token = get_access_token()
    except YouTubeOAuthError as exc:
        warn(
            f"{exc} Engaged views, watch time, AVD, and retention remain "
            "unavailable. Public viewCount will not be used as a substitute.",
            context="youtube-analytics",
        )
        return {}

    query = urllib.parse.urlencode({
        "ids": f"channel=={channel_id}",
        "startDate": YOUTUBE_WINDOW_START.isoformat(),
        "endDate": YOUTUBE_WINDOW_END.isoformat(),
        "metrics": YOUTUBE_ANALYTICS_METRICS,
        "dimensions": "video",
        "filters": f"video=={','.join(video_ids)}",
    })
    data = http_get_json(
        f"https://youtubeanalytics.googleapis.com/v2/reports?{query}",
        context="youtube-analytics",
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "weekly-pull/1.1",
        },
    )
    private_by_id = {
        str(row.get("video", "")): row
        for row in parse_result_table(data)
        if row.get("video")
    }
    for video_id, metrics in private_by_id.items():
        retention = pull_youtube_retention(
            video_id,
            durations.get(video_id, 0),
            access_token=access_token,
            channel_id=channel_id,
        )
        if retention is not None:
            metrics["retention30SecondsPct"] = retention
    return private_by_id


def pull_youtube_reach_metrics(
    video_ids: list[str], *, channel_id: str
) -> ReachMetricsResult:
    """Pull official registered thumbnail impressions and weighted CTR."""
    try:
        result = pull_reach_metrics(
            video_ids,
            expected_channel_id=channel_id,
            start_date=YOUTUBE_WINDOW_START,
            end_date=YOUTUBE_WINDOW_END,
        )
    except (YouTubeOAuthError, YouTubeReportingError) as exc:
        warn(
            f"{exc} Thumbnail impressions and CTR remain unavailable; "
            "no substitute will be inferred.",
            context="youtube-reporting",
        )
        return ReachMetricsResult(status="error", metrics_by_video={})

    if result.status == "not_provisioned":
        warn(
            "YouTube thumbnail reach job is not configured; run "
            "youtube_reporting.py ensure-job --live once.",
            context="youtube-reporting",
        )
    elif result.status == "pending":
        info(
            "YouTube thumbnail reach reports are pending; Google can take "
            "up to 48 hours after job creation."
        )
    elif result.status == "partial":
        info(
            "YouTube thumbnail reach window is incomplete; impressions and "
            "CTR stay blank until all seven daily reports are available."
        )
    elif result.status == "ready":
        info(
            f"YouTube reach: {result.report_count} daily report(s); "
            f"metrics available for {len(result.metrics_by_video)} video(s)"
        )
    return result


def pull_youtube() -> list[dict]:
    """Pull public stats plus authenticated owner metrics when available."""
    api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    channel_id = os.environ.get("YOUTUBE_CHANNEL_ID", "").strip()
    if not api_key or not channel_id:
        warn(
            "YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID missing in ~/shared-keys.env; "
            "skipping YouTube pull",
            context="youtube",
        )
        return []

    published_after = datetime.combine(
        YOUTUBE_WINDOW_START,
        datetime.min.time(),
        tzinfo=YOUTUBE_REPORT_TIMEZONE,
    ).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    published_before = datetime.combine(
        YOUTUBE_WINDOW_END + timedelta(days=1),
        datetime.min.time(),
        tzinfo=YOUTUBE_REPORT_TIMEZONE,
    ).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    info(
        "YouTube measurement window (7 closed Pacific days): "
        f"{YOUTUBE_WINDOW_START.isoformat()} → {YOUTUBE_WINDOW_END.isoformat()}"
    )
    search_url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?part=id&channelId={channel_id}"
        f"&publishedAfter={published_after}"
        f"&publishedBefore={published_before}"
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

    durations = {
        str(item.get("id", "")): parse_iso8601_duration(
            str(item.get("contentDetails", {}).get("duration", ""))
        )
        for item in stats.get("items", [])
        if item.get("id")
    }
    private_by_id = pull_youtube_private_metrics(
        video_ids, durations, channel_id=channel_id
    )
    reach_result = pull_youtube_reach_metrics(video_ids, channel_id=channel_id)
    today = NOW.strftime("%Y-%m-%d")
    rows: list[dict] = []
    for item in stats.get("items", []):
        video_id = item.get("id", "")
        s = item.get("statistics", {})
        private = private_by_id.get(video_id, {})
        reach = reach_result.metrics_by_video.get(video_id, {})
        title = (item.get("snippet", {}).get("title") or "")[:80]
        public_view_count = s.get("viewCount", "")
        estimated_minutes = private.get("estimatedMinutesWatched")
        watch_time_hours = ""
        if isinstance(estimated_minutes, (int, float)):
            watch_time_hours = round(float(estimated_minutes) / 60, 4)

        notes = [
            f"public_view_count={public_view_count}",
            "public_view_count_source=youtube_data_api_v3",
            f"measurement_break={YOUTUBE_VIEW_COUNT_BREAK.isoformat()}",
            "public_views_non_comparable_across_break=true",
            "public_view_lift_decision_signal=false",
        ]
        if private:
            notes.extend([
                f"engaged_views={private.get('engagedViews', '')}",
                "engaged_views_source=youtube_analytics_api_v2",
                f"average_view_percentage={private.get('averageViewPercentage', '')}",
                f"retention_30s_pct={private.get('retention30SecondsPct', '')}",
            ])
        else:
            notes.extend([
                "engaged_views=unavailable",
                "private_metrics=unavailable",
            ])
        if reach:
            notes.extend([
                "thumbnail_reach_source=youtube_reporting_api_v1",
                "thumbnail_impressions_definition=registered_youtube_surfaces",
                f"thumbnail_impressions={reach.get('impressions', '')}",
                f"thumbnail_ctr_pct={reach.get('ctr_pct', '')}",
                "thumbnail_ctr_aggregation=impression_weighted",
            ])
            if reach_result.coverage_start and reach_result.coverage_end:
                notes.append(
                    "thumbnail_reach_coverage="
                    f"{reach_result.coverage_start.isoformat()}.."
                    f"{reach_result.coverage_end.isoformat()}"
                )
        else:
            notes.extend([
                f"thumbnail_reach_status={reach_result.status}",
                "thumbnail_ctr=unavailable_do_not_infer",
            ])
        notes.append(f"title={title}")
        rows.append({
            "date": today,
            "content_id": video_id,
            "platform": "youtube",
            # viewCount is neither a thumbnail impression nor comparable across
            # the 2026-08-24 definition break. Keep it only in labeled notes.
            "impressions": reach.get("impressions", ""),
            "ctr_pct": reach.get("ctr_pct", ""),
            "watch_time_hrs": watch_time_hours,
            "avg_view_duration_sec": private.get("averageViewDuration", ""),
            "comments": s.get("commentCount", ""),
            "shares": s.get("likeCount", ""),  # likes as engagement proxy
            "ranking_notes": "; ".join(notes),
            "taylor_notes": (
                "weekly-pull; use engaged views + watch time + CTR + AVD + "
                "retention for decisions; never public-view lift alone"
            ),
        })
    private_count = sum(1 for row in rows if row.get("watch_time_hrs") != "")
    reach_count = sum(1 for row in rows if row.get("impressions") != "")
    info(
        f"YouTube: {len(rows)} video(s) from last 7 days; "
        f"private analytics available for {private_count}; "
        f"thumbnail reach available for {reach_count}"
    )
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
                 f"— impressions={row.get('impressions')}, "
                 f"ctr={row.get('ctr_pct')}")
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
    parser.add_argument(
        "--live", action="store_true",
        help="Required acknowledgement before any platform API request."
    )
    parser.add_argument(
        "--platform",
        choices=("all", "youtube", "beehiiv", "fub"),
        default="all",
        help="Pull one platform only (default: all).",
    )
    args = parser.parse_args()

    if not args.live:
        warn(
            "No platform requests made. Re-run with --live; combine with "
            "--dry-run to fetch without writing the ledger.",
            context="weekly-pull",
        )
        return 2

    info(f"Weekly analytics pull — {NOW.strftime('%Y-%m-%d %H:%M UTC')}")
    info(f"Window: {WEEK_AGO.strftime('%Y-%m-%d')} → {NOW.strftime('%Y-%m-%d')}")
    info("-" * 60)

    all_rows: list[dict] = []
    if args.platform in ("all", "youtube"):
        all_rows.extend(pull_youtube())
    if args.platform in ("all", "beehiiv"):
        all_rows.extend(pull_beehiiv())
    if args.platform in ("all", "fub"):
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
