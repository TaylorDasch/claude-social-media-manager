import importlib.util
import io
import json
import sys
import urllib.error
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "youtube_reporting", SCRIPTS / "youtube_reporting.py"
)
reporting = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reporting
SPEC.loader.exec_module(reporting)


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def _json_response(payload):
    return _Response(json.dumps(payload).encode("utf-8"))


class _RouteOpener:
    def __init__(self, routes):
        self.routes = routes
        self.requests = []

    def __call__(self, request, timeout=0):
        self.requests.append(request)
        key = (request.get_method(), request.full_url)
        response = self.routes.get(key)
        if response is None:
            raise AssertionError(f"unexpected request: {key}")
        return response(request) if callable(response) else response


def _jobs_url(page_token=""):
    suffix = f"&pageToken={page_token}" if page_token else ""
    return f"{reporting.REPORTING_API_ROOT}/jobs?pageSize=100{suffix}"


def _reports_url(job_id="reach-job"):
    return (
        f"{reporting.REPORTING_API_ROOT}/jobs/{job_id}/reports?pageSize=100"
    )


def _report_types_url():
    return (
        f"{reporting.REPORTING_API_ROOT}/reportTypes"
        "?includeSystemManaged=false&pageSize=100"
    )


def _reach_job():
    return {
        "id": "reach-job",
        "reportTypeId": reporting.REACH_REPORT_TYPE,
        "name": reporting.REACH_JOB_NAME,
        "createTime": "2026-08-24T18:00:00Z",
    }


def test_list_jobs_follows_pagination_once():
    opener = _RouteOpener({
        ("GET", _jobs_url()): _json_response({
            "jobs": [{"id": "first"}],
            "nextPageToken": "second-page",
        }),
        ("GET", _jobs_url("second-page")): _json_response({
            "jobs": [{"id": "second"}],
        }),
    })

    jobs = reporting.list_jobs("fixture-token", opener=opener)

    assert [job["id"] for job in jobs] == ["first", "second"]
    assert len(opener.requests) == 2
    assert all(
        request.headers["Authorization"] == "Bearer fixture-token"
        for request in opener.requests
    )


def test_ensure_job_reuses_existing_job_without_post():
    opener = _RouteOpener({
        ("GET", _report_types_url()): _json_response({
            "reportTypes": [{"id": reporting.REACH_REPORT_TYPE}],
        }),
        ("GET", _jobs_url()): _json_response({"jobs": [_reach_job()]}),
    })

    job, created = reporting.ensure_reach_job("fixture-token", opener=opener)

    assert job["id"] == "reach-job"
    assert created is False
    assert all(request.get_method() == "GET" for request in opener.requests)


def test_ensure_job_creates_only_the_exact_reach_report():
    def created_response(request):
        assert json.loads(request.data.decode("utf-8")) == {
            "reportTypeId": reporting.REACH_REPORT_TYPE,
            "name": reporting.REACH_JOB_NAME,
        }
        return _json_response(_reach_job())

    opener = _RouteOpener({
        ("GET", _report_types_url()): _json_response({
            "reportTypes": [{"id": reporting.REACH_REPORT_TYPE}],
        }),
        ("GET", _jobs_url()): _json_response({"jobs": []}),
        ("POST", f"{reporting.REPORTING_API_ROOT}/jobs"): created_response,
    })

    job, created = reporting.ensure_reach_job("fixture-token", opener=opener)

    assert created is True
    assert job["reportTypeId"] == reporting.REACH_REPORT_TYPE
    assert [request.get_method() for request in opener.requests] == [
        "GET", "GET", "POST"
    ]


def test_pull_reach_uses_newest_backfill_and_impression_weighted_ctr():
    reports = [
        {
            "id": "old-day-1",
            "startTime": "2026-08-20T07:00:00Z",
            "endTime": "2026-08-21T07:00:00Z",
            "createTime": "2026-08-22T10:00:00Z",
            "downloadUrl": (
                "https://youtubereporting.googleapis.com/v1/media/old-day-1"
            ),
        },
        {
            "id": "new-day-1",
            "startTime": "2026-08-20T07:00:00Z",
            "endTime": "2026-08-21T07:00:00Z",
            "createTime": "2026-08-23T10:00:00Z",
            "downloadUrl": (
                "https://youtubereporting.googleapis.com/v1/media/new-day-1"
            ),
        },
        {
            "id": "day-2",
            "startTime": "2026-08-21T07:00:00Z",
            "endTime": "2026-08-22T07:00:00Z",
            "createTime": "2026-08-23T11:00:00Z",
            "downloadUrl": (
                "https://youtubereporting.googleapis.com/v1/media/day-2"
            ),
        },
    ]
    header = (
        "date,channel_id,video_id,video_thumbnail_impressions,"
        "video_thumbnail_impressions_ctr\n"
    )
    opener = _RouteOpener({
        ("GET", _jobs_url()): _json_response({"jobs": [_reach_job()]}),
        ("GET", _reports_url()): _json_response({"reports": reports}),
        (
            "GET",
            "https://youtubereporting.googleapis.com/v1/media/new-day-1",
        ): _Response((header + "2026-08-20,fixture-channel,video-1,100,2\n").encode()),
        (
            "GET",
            "https://youtubereporting.googleapis.com/v1/media/day-2",
        ): _Response((header + "2026-08-21,fixture-channel,video-1,900,8\n").encode()),
    })

    result = reporting.pull_reach_metrics(
        ["video-1"],
        expected_channel_id="fixture-channel",
        start_date=date(2026, 8, 20),
        end_date=date(2026, 8, 21),
        access_token="fixture-token",
        opener=opener,
    )

    assert result.status == "ready"
    assert result.report_count == 2
    assert result.coverage_start == date(2026, 8, 20)
    assert result.coverage_end == date(2026, 8, 21)
    assert result.metrics_by_video == {
        "video-1": {"impressions": 1000, "ctr_pct": 7.4}
    }
    called_urls = [request.full_url for request in opener.requests]
    assert not any("old-day-1" in url for url in called_urls)


def test_no_generated_reports_is_pending_not_zero():
    opener = _RouteOpener({
        ("GET", _jobs_url()): _json_response({"jobs": [_reach_job()]}),
        ("GET", _reports_url()): _json_response({"reports": []}),
    })

    result = reporting.pull_reach_metrics(
        ["video-1"],
        expected_channel_id="fixture-channel",
        start_date=date(2026, 8, 20),
        end_date=date(2026, 8, 21),
        access_token="fixture-token",
        opener=opener,
    )

    assert result.status == "pending"
    assert result.metrics_by_video == {}


def test_incomplete_seven_day_window_stays_partial_and_blank():
    reports = []
    for day in range(20, 26):
        reports.append({
            "id": f"day-{day}",
            "startTime": f"2026-08-{day:02d}T07:00:00Z",
            "endTime": f"2026-08-{day + 1:02d}T07:00:00Z",
            "createTime": "2026-08-27T10:00:00Z",
            "downloadUrl": (
                "https://youtubereporting.googleapis.com/v1/media/"
                f"day-{day}"
            ),
        })
    opener = _RouteOpener({
        ("GET", _jobs_url()): _json_response({"jobs": [_reach_job()]}),
        ("GET", _reports_url()): _json_response({"reports": reports}),
    })

    result = reporting.pull_reach_metrics(
        ["video-1"],
        expected_channel_id="fixture-channel",
        start_date=date(2026, 8, 20),
        end_date=date(2026, 8, 26),
        access_token="fixture-token",
        opener=opener,
    )

    assert result.status == "partial"
    assert result.report_count == 6
    assert result.metrics_by_video == {}
    assert all("/v1/media/" not in request.full_url for request in opener.requests)


def test_complete_header_only_window_is_known_zero_impressions():
    header = (
        "date,channel_id,video_id,video_thumbnail_impressions,"
        "video_thumbnail_impressions_ctr\n"
    )
    reports = []
    routes = {
        ("GET", _jobs_url()): _json_response({"jobs": [_reach_job()]}),
    }
    for day in range(20, 27):
        url = f"https://youtubereporting.googleapis.com/v1/media/day-{day}"
        reports.append({
            "id": f"day-{day}",
            "startTime": f"2026-08-{day:02d}T07:00:00Z",
            "endTime": f"2026-08-{day + 1:02d}T07:00:00Z",
            "createTime": "2026-08-28T10:00:00Z",
            "downloadUrl": url,
        })
        routes[("GET", url)] = _Response(header.encode("utf-8"))
    routes[("GET", _reports_url())] = _json_response({"reports": reports})
    opener = _RouteOpener(routes)

    result = reporting.pull_reach_metrics(
        ["video-1"],
        expected_channel_id="fixture-channel",
        start_date=date(2026, 8, 20),
        end_date=date(2026, 8, 26),
        access_token="fixture-token",
        opener=opener,
    )

    assert result.status == "ready"
    assert result.report_count == 7
    assert result.coverage_start == date(2026, 8, 20)
    assert result.coverage_end == date(2026, 8, 26)
    assert result.metrics_by_video == {
        "video-1": {"impressions": 0, "ctr_pct": ""}
    }


def test_csv_channel_mismatch_is_rejected():
    contents = (
        "date,channel_id,video_id,video_thumbnail_impressions,"
        "video_thumbnail_impressions_ctr\n"
        "2026-08-20,wrong-channel,video-1,100,5\n"
    )

    with pytest.raises(reporting.YouTubeReportingError, match="expected channel"):
        reporting._parse_reach_csv(
            contents,
            expected_channel_id="fixture-channel",
            requested_video_ids={"video-1"},
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 20),
        )


def test_csv_missing_reach_columns_is_rejected():
    with pytest.raises(reporting.YouTubeReportingError, match="required CSV"):
        reporting._parse_reach_csv(
            "date,channel_id,video_id\n2026-08-20,fixture-channel,video-1\n",
            expected_channel_id="fixture-channel",
            requested_video_ids={"video-1"},
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 20),
        )


def test_download_url_must_stay_on_the_reporting_host():
    with pytest.raises(reporting.YouTubeReportingError, match="unsafe"):
        reporting._safe_download_url(
            "https://example.com/steal-report?access_token=fixture-secret"
        )


def test_authenticated_downloads_reject_redirects_by_default():
    assert (
        reporting._download_report_csv.__kwdefaults__["opener"]
        is reporting._open_without_redirects
    )
    assert reporting._RejectRedirects().redirect_request(
        None, None, 302, "redirect", {}, "https://example.com/"
    ) is None


def test_cli_requires_live_before_refreshing_or_creating():
    with patch.object(reporting, "get_access_token") as token:
        assert reporting.main(["ensure-job"]) == 2
    token.assert_not_called()


def test_http_error_message_does_not_disclose_token_or_url():
    def forbidden(request, timeout=0):
        raise urllib.error.HTTPError(
            request.full_url,
            403,
            "fixture-token https://secret.invalid",
            {},
            None,
        )

    with pytest.raises(reporting.YouTubeReportingError) as caught:
        reporting.list_jobs("fixture-token", opener=forbidden)

    message = str(caught.value)
    assert "fixture-token" not in message
    assert "secret.invalid" not in message
    assert "HTTP 403" in message
