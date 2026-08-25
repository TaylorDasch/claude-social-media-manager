import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("weekly_pull", SCRIPTS / "weekly-pull.py")
weekly_pull = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(weekly_pull)


def _public_responses(url, *, context, headers=None):
    if "youtube/v3/search" in url:
        query = parse_qs(urlparse(url).query)
        assert query.get("publishedAfter")
        assert query.get("publishedBefore")
        return {"items": [{"id": {"videoId": "video-1"}}]}
    if "youtube/v3/videos" in url:
        return {
            "items": [{
                "id": "video-1",
                "statistics": {"viewCount": "100", "likeCount": "5", "commentCount": "3"},
                "snippet": {"title": "Temple test video"},
                "contentDetails": {"duration": "PT2M"},
            }]
        }
    raise AssertionError(f"unexpected URL: {url}")


def _authenticated_responses(url, *, context, headers=None):
    if "youtube/v3/" in url:
        return _public_responses(url, context=context, headers=headers)
    query = parse_qs(urlparse(url).query)
    metrics = query.get("metrics", [""])[0]
    assert headers["Authorization"] == "Bearer fixture-token"
    assert query["startDate"] == [weekly_pull.YOUTUBE_WINDOW_START.isoformat()]
    assert query["endDate"] == [weekly_pull.YOUTUBE_WINDOW_END.isoformat()]
    if metrics == weekly_pull.YOUTUBE_ANALYTICS_METRICS:
        return {
            "columnHeaders": [
                {"name": "video"},
                {"name": "engagedViews"},
                {"name": "estimatedMinutesWatched"},
                {"name": "averageViewDuration"},
                {"name": "averageViewPercentage"},
            ],
            "rows": [["video-1", 80, 120, 90, 50.0]],
        }
    if metrics == "audienceWatchRatio":
        return {
            "columnHeaders": [
                {"name": "elapsedVideoTimeRatio"},
                {"name": "audienceWatchRatio"},
            ],
            "rows": [[0.0, 1.0], [0.25, 0.75], [0.5, 0.6]],
        }
    raise AssertionError(f"unexpected Analytics query: {url}")


def _pending_reach():
    return weekly_pull.ReachMetricsResult(
        status="pending",
        metrics_by_video={},
    )


def test_public_view_count_is_labeled_and_never_written_as_impressions():
    env = {
        "YOUTUBE_API_KEY": "fixture-key",
        "YOUTUBE_CHANNEL_ID": "fixture-channel",
    }
    with patch.dict(os.environ, env, clear=True), patch.object(
        weekly_pull, "http_get_json", side_effect=_public_responses
    ), patch.object(
        weekly_pull,
        "get_access_token",
        side_effect=weekly_pull.YouTubeOAuthError("not connected"),
    ), patch.object(
        weekly_pull,
        "pull_youtube_reach_metrics",
        return_value=_pending_reach(),
    ):
        rows = weekly_pull.pull_youtube()

    assert len(rows) == 1
    row = rows[0]
    assert row["impressions"] == ""
    assert row["ctr_pct"] == ""
    assert "public_view_count=100" in row["ranking_notes"]
    assert "measurement_break=2026-08-24" in row["ranking_notes"]
    assert "public_views_non_comparable_across_break=true" in row["ranking_notes"]
    assert "engaged_views=unavailable" in row["ranking_notes"]
    assert "thumbnail_reach_status=pending" in row["ranking_notes"]
    assert "never public-view lift alone" in row["taylor_notes"]


def test_keychain_owner_metrics_are_kept_separate_from_public_starts():
    env = {
        "YOUTUBE_API_KEY": "fixture-key",
        "YOUTUBE_CHANNEL_ID": "fixture-channel",
    }
    with patch.dict(os.environ, env, clear=True), patch.object(
        weekly_pull, "http_get_json", side_effect=_authenticated_responses
    ), patch.object(weekly_pull, "get_access_token", return_value="fixture-token"):
        with patch.object(
            weekly_pull,
            "pull_youtube_reach_metrics",
            return_value=_pending_reach(),
        ):
            rows = weekly_pull.pull_youtube()

    row = rows[0]
    assert row["impressions"] == ""
    assert row["watch_time_hrs"] == 2.0
    assert row["avg_view_duration_sec"] == 90
    assert "public_view_count=100" in row["ranking_notes"]
    assert "engaged_views=80" in row["ranking_notes"]
    assert "retention_30s_pct=75.0" in row["ranking_notes"]
    assert "thumbnail_ctr=unavailable_do_not_infer" in row["ranking_notes"]


def test_reporting_reach_populates_impressions_and_weighted_ctr():
    env = {
        "YOUTUBE_API_KEY": "fixture-key",
        "YOUTUBE_CHANNEL_ID": "fixture-channel",
    }
    reach = weekly_pull.ReachMetricsResult(
        status="ready",
        metrics_by_video={
            "video-1": {"impressions": 1234, "ctr_pct": 6.75},
        },
        report_count=7,
        coverage_start=weekly_pull.YOUTUBE_WINDOW_START,
        coverage_end=weekly_pull.YOUTUBE_WINDOW_END,
    )
    with patch.dict(os.environ, env, clear=True), patch.object(
        weekly_pull, "http_get_json", side_effect=_authenticated_responses
    ), patch.object(
        weekly_pull, "get_access_token", return_value="fixture-token"
    ), patch.object(
        weekly_pull, "pull_youtube_reach_metrics", return_value=reach
    ):
        rows = weekly_pull.pull_youtube()

    row = rows[0]
    assert row["impressions"] == 1234
    assert row["ctr_pct"] == 6.75
    assert "thumbnail_reach_source=youtube_reporting_api_v1" in row["ranking_notes"]
    assert "thumbnail_ctr_aggregation=impression_weighted" in row["ranking_notes"]
    assert "thumbnail_ctr=unavailable_do_not_infer" not in row["ranking_notes"]


def test_main_requires_live_before_any_platform_pull():
    with patch.object(weekly_pull, "pull_youtube") as youtube, patch.object(
        weekly_pull, "pull_beehiiv"
    ) as beehiiv, patch.object(weekly_pull, "pull_fub") as fub, patch.object(
        sys, "argv", ["weekly-pull.py"]
    ):
        assert weekly_pull.main() == 2

    youtube.assert_not_called()
    beehiiv.assert_not_called()
    fub.assert_not_called()


def test_youtube_platform_selector_skips_unrelated_api_pulls():
    youtube_rows = [{"platform": "youtube", "content_id": "video-1"}]
    with patch.object(
        weekly_pull, "pull_youtube", return_value=youtube_rows
    ) as youtube, patch.object(
        weekly_pull, "pull_beehiiv"
    ) as beehiiv, patch.object(
        weekly_pull, "pull_fub"
    ) as fub, patch.object(
        weekly_pull, "append_to_ledger"
    ) as append, patch.object(
        sys,
        "argv",
        [
            "weekly-pull.py",
            "--live",
            "--dry-run",
            "--platform",
            "youtube",
        ],
    ):
        assert weekly_pull.main() == 0

    youtube.assert_called_once_with()
    beehiiv.assert_not_called()
    fub.assert_not_called()
    append.assert_called_once_with(youtube_rows, dry_run=True)


def test_platform_selector_defaults_to_all_pulls():
    youtube_rows = [{"platform": "youtube", "content_id": "video-1"}]
    beehiiv_rows = [{"platform": "beehiiv", "content_id": "post-1"}]
    fub_rows = [{"platform": "fub", "content_id": "lead-1"}]
    with patch.object(
        weekly_pull, "pull_youtube", return_value=youtube_rows
    ) as youtube, patch.object(
        weekly_pull, "pull_beehiiv", return_value=beehiiv_rows
    ) as beehiiv, patch.object(
        weekly_pull, "pull_fub", return_value=fub_rows
    ) as fub, patch.object(
        weekly_pull, "append_to_ledger"
    ) as append, patch.object(
        sys, "argv", ["weekly-pull.py", "--live", "--dry-run"]
    ):
        assert weekly_pull.main() == 0

    youtube.assert_called_once_with()
    beehiiv.assert_called_once_with()
    fub.assert_called_once_with()
    append.assert_called_once_with(
        youtube_rows + beehiiv_rows + fub_rows,
        dry_run=True,
    )
