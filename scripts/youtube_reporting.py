#!/usr/bin/env python3
"""YouTube Reporting API support for thumbnail impressions and CTR.

The targeted YouTube Analytics API does not expose thumbnail reach metrics.
This module uses the bulk Reporting API's ``channel_reach_basic_a1`` report,
which supplies daily video thumbnail impressions and impressions CTR.

The reporting job is provisioned explicitly and idempotently:

    python3 scripts/youtube_reporting.py ensure-job --live
    python3 scripts/youtube_reporting.py status --live

Scheduled analytics pulls only read an existing job. They never create or
delete Google-side resources. The existing Keychain credential supplies the
least-privilege ``yt-analytics.readonly`` scope required by this API.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Callable, Optional
from zoneinfo import ZoneInfo

from youtube_analytics_oauth import YouTubeOAuthError, get_access_token


REPORTING_API_ROOT = "https://youtubereporting.googleapis.com/v1"
REACH_REPORT_TYPE = "channel_reach_basic_a1"
REACH_JOB_NAME = "Taylor weekly thumbnail reach"
REPORT_TIMEZONE = ZoneInfo("America/Los_Angeles")
MAX_REPORT_BYTES = 10 * 1024 * 1024
REQUIRED_CSV_COLUMNS = {
    "date",
    "channel_id",
    "video_id",
    "video_thumbnail_impressions",
    "video_thumbnail_impressions_ctr",
}
USER_AGENT = "taylor-youtube-reporting/1.0"


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Keep bearer credentials on the validated Google download endpoint."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


_NO_REDIRECT_OPENER = urllib.request.build_opener(_RejectRedirects())


def _open_without_redirects(request, timeout=0):
    return _NO_REDIRECT_OPENER.open(request, timeout=timeout)


class YouTubeReportingError(RuntimeError):
    """Safe-to-display Reporting API failure without secret material."""

    def __init__(self, message: str, *, http_status: Optional[int] = None) -> None:
        super().__init__(message)
        self.http_status = http_status


@dataclass(frozen=True)
class ReachMetricsResult:
    """Owner reach metrics plus enough state to label unavailable data."""

    status: str
    metrics_by_video: dict[str, dict]
    report_count: int = 0
    coverage_start: Optional[date] = None
    coverage_end: Optional[date] = None


def _read_json_response(response) -> dict:
    try:
        parsed = json.load(response)
    except (json.JSONDecodeError, TypeError, ValueError):
        raise YouTubeReportingError(
            "YouTube Reporting returned invalid JSON."
        ) from None
    if not isinstance(parsed, dict):
        raise YouTubeReportingError(
            "YouTube Reporting returned an unexpected response format."
        )
    return parsed


def _api_json_request(
    method: str,
    path: str,
    *,
    access_token: str,
    payload: Optional[dict] = None,
    opener: Callable = _open_without_redirects,
) -> dict:
    if not path.startswith("/"):
        raise YouTubeReportingError("Invalid YouTube Reporting API path.")
    body = None
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if payload is not None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        f"{REPORTING_API_ROOT}{path}",
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with opener(request, timeout=20) as response:
            return _read_json_response(response)
    except urllib.error.HTTPError as exc:
        status = exc.code
        raise YouTubeReportingError(
            f"YouTube Reporting request failed with HTTP {status}.",
            http_status=status,
        ) from None
    except YouTubeReportingError:
        raise
    except Exception:
        raise YouTubeReportingError(
            "Could not reach the YouTube Reporting API."
        ) from None


def _list_all(
    path: str,
    result_key: str,
    *,
    access_token: str,
    opener: Callable = _open_without_redirects,
) -> list[dict]:
    items: list[dict] = []
    page_token = ""
    seen_tokens: set[str] = set()
    while True:
        query = {"pageSize": "100"}
        if page_token:
            query["pageToken"] = page_token
        separator = "&" if "?" in path else "?"
        data = _api_json_request(
            "GET",
            f"{path}{separator}{urllib.parse.urlencode(query)}",
            access_token=access_token,
            opener=opener,
        )
        page_items = data.get(result_key, [])
        if not isinstance(page_items, list):
            raise YouTubeReportingError(
                "YouTube Reporting returned an invalid paginated response."
            )
        items.extend(item for item in page_items if isinstance(item, dict))
        next_token = data.get("nextPageToken", "")
        if not next_token:
            return items
        if not isinstance(next_token, str) or next_token in seen_tokens:
            raise YouTubeReportingError(
                "YouTube Reporting returned an invalid pagination token."
            )
        seen_tokens.add(next_token)
        page_token = next_token


def _parse_timestamp(value: object, *, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise YouTubeReportingError(
            f"YouTube Reporting omitted required {field} metadata."
        )
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        raise YouTubeReportingError(
            f"YouTube Reporting returned invalid {field} metadata."
        ) from None
    if parsed.tzinfo is None:
        raise YouTubeReportingError(
            f"YouTube Reporting returned timezone-free {field} metadata."
        )
    return parsed


def _job_is_active(job: dict, *, now: Optional[datetime] = None) -> bool:
    expire_time = job.get("expireTime")
    if not expire_time:
        return True
    return _parse_timestamp(expire_time, field="job expiration") > (
        now or datetime.now(timezone.utc)
    )


def _find_reach_job(
    jobs: list[dict], *, now: Optional[datetime] = None
) -> Optional[dict]:
    matching = [
        job
        for job in jobs
        if job.get("reportTypeId") == REACH_REPORT_TYPE
        and job.get("id")
        and _job_is_active(job, now=now)
    ]
    if not matching:
        return None
    return max(matching, key=lambda job: str(job.get("createTime", "")))


def list_jobs(
    access_token: str, *, opener: Callable = _open_without_redirects
) -> list[dict]:
    return _list_all(
        "/jobs",
        "jobs",
        access_token=access_token,
        opener=opener,
    )


def list_reports(
    job_id: str,
    access_token: str,
    *,
    opener: Callable = _open_without_redirects,
) -> list[dict]:
    encoded_job_id = urllib.parse.quote(job_id, safe="")
    return _list_all(
        f"/jobs/{encoded_job_id}/reports",
        "reports",
        access_token=access_token,
        opener=opener,
    )


def ensure_reach_job(
    access_token: str, *, opener: Callable = _open_without_redirects
) -> tuple[dict, bool]:
    """Return the active reach job, creating it only when absent."""
    report_types = _list_all(
        "/reportTypes?includeSystemManaged=false",
        "reportTypes",
        access_token=access_token,
        opener=opener,
    )
    if REACH_REPORT_TYPE not in {item.get("id") for item in report_types}:
        raise YouTubeReportingError(
            "The channel reach report is not available for this YouTube account."
        )

    existing = _find_reach_job(list_jobs(access_token, opener=opener))
    if existing is not None:
        return existing, False

    try:
        created = _api_json_request(
            "POST",
            "/jobs",
            access_token=access_token,
            payload={"reportTypeId": REACH_REPORT_TYPE, "name": REACH_JOB_NAME},
            opener=opener,
        )
    except YouTubeReportingError as exc:
        if exc.http_status != 409:
            raise
        # A parallel setup may have won the race. Re-list before failing.
        existing = _find_reach_job(list_jobs(access_token, opener=opener))
        if existing is None:
            raise
        return existing, False
    if created.get("reportTypeId") != REACH_REPORT_TYPE or not created.get("id"):
        raise YouTubeReportingError(
            "YouTube created an unexpected reporting job."
        )
    return created, True


def _newest_report_per_period(reports: list[dict]) -> list[dict]:
    newest: dict[tuple[str, str], dict] = {}
    for report in reports:
        start_time = str(report.get("startTime", ""))
        end_time = str(report.get("endTime", ""))
        if not start_time or not end_time:
            raise YouTubeReportingError(
                "YouTube Reporting returned a report without a time period."
            )
        key = (start_time, end_time)
        current = newest.get(key)
        if current is None or str(report.get("createTime", "")) > str(
            current.get("createTime", "")
        ):
            newest[key] = report
    return list(newest.values())


def _report_local_date(report: dict) -> date:
    return _parse_timestamp(
        report.get("startTime"), field="report start time"
    ).astimezone(REPORT_TIMEZONE).date()


def _safe_download_url(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise YouTubeReportingError(
            "YouTube Reporting omitted a report download URL."
        )
    parsed = urllib.parse.urlsplit(value)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "youtubereporting.googleapis.com"
        or parsed.port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or not parsed.path.startswith("/v1/media/")
    ):
        raise YouTubeReportingError(
            "YouTube Reporting returned an unsafe report download URL."
        )
    return value


def _download_report_csv(
    download_url: object,
    *,
    access_token: str,
    opener: Callable = _open_without_redirects,
) -> str:
    safe_url = _safe_download_url(download_url)
    request = urllib.request.Request(
        safe_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "text/csv",
            "Accept-Encoding": "identity",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with opener(request, timeout=30) as response:
            raw = response.read(MAX_REPORT_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise YouTubeReportingError(
            f"YouTube report download failed with HTTP {exc.code}.",
            http_status=exc.code,
        ) from None
    except Exception:
        raise YouTubeReportingError(
            "Could not download a YouTube reach report."
        ) from None
    if len(raw) > MAX_REPORT_BYTES:
        raise YouTubeReportingError(
            "YouTube reach report exceeded the safe download limit."
        )
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise YouTubeReportingError(
            "YouTube reach report was not valid UTF-8 CSV."
        ) from None


def _parse_nonnegative_decimal(value: object, *, field: str) -> Decimal:
    try:
        parsed = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError):
        raise YouTubeReportingError(
            f"YouTube reach report contained invalid {field}."
        ) from None
    if not parsed.is_finite() or parsed < 0:
        raise YouTubeReportingError(
            f"YouTube reach report contained invalid {field}."
        )
    return parsed


def _parse_reach_csv(
    contents: str,
    *,
    expected_channel_id: str,
    requested_video_ids: set[str],
    start_date: date,
    end_date: date,
) -> tuple[list[tuple[date, str, int, Decimal]], set[date]]:
    reader = csv.DictReader(io.StringIO(contents))
    headers = set(reader.fieldnames or [])
    if not REQUIRED_CSV_COLUMNS.issubset(headers):
        raise YouTubeReportingError(
            "YouTube reach report is missing required CSV columns."
        )
    parsed_rows: list[tuple[date, str, int, Decimal]] = []
    covered_dates: set[date] = set()
    seen_keys: set[tuple[date, str]] = set()
    for row in reader:
        try:
            row_date = date.fromisoformat(str(row.get("date", "")))
        except ValueError:
            raise YouTubeReportingError(
                "YouTube reach report contained an invalid date."
            ) from None
        covered_dates.add(row_date)
        if not start_date <= row_date <= end_date:
            continue
        if str(row.get("channel_id", "")) != expected_channel_id:
            raise YouTubeReportingError(
                "YouTube reach report did not match the expected channel."
            )
        video_id = str(row.get("video_id", ""))
        if not video_id or video_id not in requested_video_ids:
            continue
        key = (row_date, video_id)
        if key in seen_keys:
            raise YouTubeReportingError(
                "YouTube reach report contained duplicate video-day rows."
            )
        seen_keys.add(key)

        impressions_decimal = _parse_nonnegative_decimal(
            row.get("video_thumbnail_impressions", ""), field="impressions"
        )
        if impressions_decimal != impressions_decimal.to_integral_value():
            raise YouTubeReportingError(
                "YouTube reach report contained non-integer impressions."
            )
        impressions = int(impressions_decimal)
        ctr_text = str(row.get("video_thumbnail_impressions_ctr", "")).strip()
        if impressions == 0 and not ctr_text:
            ctr = Decimal(0)
        else:
            ctr = _parse_nonnegative_decimal(ctr_text, field="CTR")
        if ctr > 100:
            raise YouTubeReportingError(
                "YouTube reach report contained CTR above 100 percent."
            )
        parsed_rows.append((row_date, video_id, impressions, ctr))
    return parsed_rows, covered_dates


def pull_reach_metrics(
    video_ids: list[str],
    *,
    expected_channel_id: str,
    start_date: date,
    end_date: date,
    access_token: Optional[str] = None,
    opener: Callable = _open_without_redirects,
) -> ReachMetricsResult:
    """Read and aggregate owner reach reports for requested videos."""
    if start_date > end_date:
        raise YouTubeReportingError("YouTube reach date window is invalid.")
    expected_channel_id = expected_channel_id.strip()
    if not expected_channel_id:
        raise YouTubeReportingError("An expected YouTube channel ID is required.")
    requested_video_ids = {video_id for video_id in video_ids if video_id}
    if not requested_video_ids:
        return ReachMetricsResult(status="ready", metrics_by_video={})

    token = access_token or get_access_token()
    job = _find_reach_job(list_jobs(token, opener=opener))
    if job is None:
        return ReachMetricsResult(status="not_provisioned", metrics_by_video={})

    reports = _newest_report_per_period(
        list_reports(str(job["id"]), token, opener=opener)
    )
    selected_by_date: dict[date, dict] = {}
    for report in reports:
        report_date = _report_local_date(report)
        if not start_date <= report_date <= end_date:
            continue
        if report_date in selected_by_date:
            raise YouTubeReportingError(
                "YouTube Reporting returned overlapping daily report periods."
            )
        selected_by_date[report_date] = report
    selected = list(selected_by_date.values())
    if not selected:
        return ReachMetricsResult(status="pending", metrics_by_video={})

    expected_dates = {
        date.fromordinal(ordinal)
        for ordinal in range(start_date.toordinal(), end_date.toordinal() + 1)
    }
    available_dates = set(selected_by_date)
    if available_dates != expected_dates:
        return ReachMetricsResult(
            status="partial",
            metrics_by_video={},
            report_count=len(selected),
            coverage_start=min(available_dates),
            coverage_end=max(available_dates),
        )

    totals: dict[str, dict[str, object]] = {}
    seen_across_reports: set[tuple[date, str]] = set()
    for report in sorted(selected, key=_report_local_date):
        report_date = _report_local_date(report)
        contents = _download_report_csv(
            report.get("downloadUrl"), access_token=token, opener=opener
        )
        parsed_rows, covered_dates = _parse_reach_csv(
            contents,
            expected_channel_id=expected_channel_id,
            requested_video_ids=requested_video_ids,
            start_date=start_date,
            end_date=end_date,
        )
        if covered_dates and covered_dates != {report_date}:
            raise YouTubeReportingError(
                "YouTube reach CSV did not match its report period."
            )
        for row_date, video_id, impressions, ctr in parsed_rows:
            key = (row_date, video_id)
            if key in seen_across_reports:
                raise YouTubeReportingError(
                    "YouTube reach reports overlapped the same video-day."
                )
            seen_across_reports.add(key)
            total = totals.setdefault(
                video_id,
                {"impressions": 0, "weighted_ctr": Decimal(0)},
            )
            total["impressions"] = int(total["impressions"]) + impressions
            total["weighted_ctr"] = Decimal(total["weighted_ctr"]) + (
                Decimal(impressions) * ctr
            )

    metrics_by_video: dict[str, dict] = {}
    for video_id in requested_video_ids:
        total = totals.get(
            video_id, {"impressions": 0, "weighted_ctr": Decimal(0)}
        )
        impressions = int(total["impressions"])
        metrics_by_video[video_id] = {
            "impressions": impressions,
            "ctr_pct": "",
        }
        if impressions > 0:
            ctr = Decimal(total["weighted_ctr"]) / Decimal(impressions)
            ctr_float = float(ctr)
            if not math.isfinite(ctr_float):
                raise YouTubeReportingError(
                    "YouTube reach aggregation produced invalid CTR."
                )
            metrics_by_video[video_id]["ctr_pct"] = round(ctr_float, 4)

    return ReachMetricsResult(
        status="ready",
        metrics_by_video=metrics_by_video,
        report_count=len(selected),
        coverage_start=start_date,
        coverage_end=end_date,
    )


def _require_live(args: argparse.Namespace, action: str) -> None:
    if not args.live:
        raise YouTubeReportingError(
            f"{action} makes live Google requests; re-run with --live."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command, help_text in (
        ("status", "Check whether the reach job and reports are ready."),
        ("ensure-job", "Create the daily reach job only if it is absent."),
    ):
        subparser = subparsers.add_parser(command, help=help_text)
        subparser.add_argument("--live", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        _require_live(args, "YouTube Reporting")
        access_token = get_access_token()
        if args.command == "ensure-job":
            job, created = ensure_reach_job(access_token)
            state = "created" if created else "already configured"
            print(f"YouTube thumbnail reach job: {state}")
            reports = list_reports(str(job["id"]), access_token)
            if reports:
                print(f"Generated reports available: {len(reports)}")
            else:
                print("Generated reports: pending (allow up to 48 hours)")
            return 0

        job = _find_reach_job(list_jobs(access_token))
        if job is None:
            print("YouTube thumbnail reach job: not configured")
            return 1
        reports = list_reports(str(job["id"]), access_token)
        print("YouTube thumbnail reach job: configured")
        if reports:
            print(f"Generated reports available: {len(reports)}")
        else:
            print("Generated reports: pending (allow up to 48 hours)")
        return 0
    except (YouTubeOAuthError, YouTubeReportingError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
