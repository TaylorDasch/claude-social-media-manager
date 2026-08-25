# YouTube Analytics read-only connection

## Purpose

This connection gives the weekly analytics pull owner-only performance data
without granting upload, edit, publish, delete, or revenue access.

The same grant also reads the YouTube Reporting API's basic reach report for
registered thumbnail impressions and impressions CTR. No additional OAuth
scope or second credential is required.

Approved scopes:

- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

Google now requires both scopes for `youtubeAnalytics.reports.query`.

## Security model

- Use a dedicated Google Cloud project so revocation or a client problem does
  not affect Taylor's Gmail, Drive, Search Console, or Google Business access.
- Use a Desktop OAuth client with loopback redirect, random port, state
  validation, and PKCE S256.
- Keep the desktop client JSON outside Git in
  `~/.config/taylor/youtube-analytics/client-secret.json`. The directory must
  be mode `0700` and the file mode `0600`.
- Store the refresh credential in macOS Keychain under service
  `com.taylordasch.youtube-analytics.readonly` and account
  `dealswithdasch@gmail.com`.
- Exchange the refresh credential for a short-lived access token in memory.
  Do not put tokens in `shared-keys.env`, command-line arguments, logs, or the
  repository.
- Keep the Google OAuth audience **In production**. An External app left in
  Testing expires YouTube refresh grants after seven days.

## Commands

Local status check; no network:

```bash
python3 scripts/youtube_analytics_oauth.py status
```

One-time connection or recovery:

```bash
python3 scripts/youtube_analytics_oauth.py connect \
  --client-secrets ~/.config/taylor/youtube-analytics/client-secret.json \
  --expected-channel-id "$YOUTUBE_CHANNEL_ID" \
  --live
```

Live verification without a ledger write:

```bash
python3 scripts/youtube_analytics_oauth.py verify \
  --expected-channel-id "$YOUTUBE_CHANNEL_ID" \
  --live

python3 scripts/weekly-pull.py --live --dry-run --platform youtube
```

The connector verifies that the authorized Google account owns the configured
channel and that private engaged-view, watch-time, average-view-duration, and
average-view-percentage columns are returned before it saves the refresh grant.

## Thumbnail reach setup

The dedicated Google project must have `youtubereporting.googleapis.com`
enabled. Provision the basic channel reach job once:

```bash
python3 scripts/youtube_reporting.py ensure-job --live
python3 scripts/youtube_reporting.py status --live
```

Setup is idempotent: it reuses the active `channel_reach_basic_a1` job and
creates one only when none exists. The Sunday pull never creates or deletes a
Google-side job.

Google generates these CSV reports asynchronously. Allow up to 48 hours for
the first files. A new job also normally receives the preceding 30 days of
historical reports within a couple of days. Until a matching daily report is
available, the ledger keeps `impressions` and `ctr_pct` blank and labels the
reach status `pending`; it does not write zero or infer either metric.

The weekly YouTube row uses seven completed Pacific-time dates ending three
days before the run. Targeted watch-time/retention queries and bulk reach data
use that same closed window. If even one of the seven daily reach files is
missing, reach status is `partial` and both reach fields stay blank rather than
mixing a partial CTR window with a full watch-time window. After all seven
files exist, a video omitted from every header-valid daily file is recorded as
zero registered impressions with blank CTR.

For multi-day rows, impressions are summed and CTR is weighted by daily
impressions. If Google replaces a day with a newer backfill, the importer uses
the newest report for that exact period. The importer validates the expected
channel, CSV headers, date window, download host, numeric fields, and a 10 MB
per-report size limit before accepting data.

## Scheduled use

The Sunday job must run the verified `main` worktree with a supported Python
runtime and an explicit live flag:

```text
/opt/homebrew/bin/python3 /Users/taylordasch_1/wt-smm-main-clean/scripts/weekly-pull.py --live --platform youtube
```

`--dry-run` suppresses ledger writes; it does not replace `--live`.
The scheduled job is explicitly YouTube-only so it does not call the legacy
Follow Up Boss integration or unrelated newsletter APIs.

## Metric boundary

The targeted YouTube Analytics API supplies engaged views, watch time, AVD,
average percentage viewed, and audience retention. The Reporting API basic
reach report supplies `video_thumbnail_impressions` and
`video_thumbnail_impressions_ctr`. A registered impression means YouTube
showed at least 50 percent of the thumbnail for more than one second on an
eligible YouTube surface; it is not the same as every view or every external
exposure. CTR is Google's reported percentage of those registered impressions
that produced a click to watch. The weekly pull must keep reach fields blank
when the report is missing and must never infer CTR from public view counts.

## Recovery and rollback

- If Google returns `invalid_grant`, run the one-time `connect --live` command
  again. Do not force consent on normal weekly runs.
- If the reach job is missing or expired, run
  `python3 scripts/youtube_reporting.py ensure-job --live`. Do not create a new
  job on every scheduled pull.
- Google retains normal bulk reports for 60 days and initial historical reports
  for 30 days. The weekly importer reads only the requested date window and
  does not persist downloaded CSV files.
- Local rollback removes only the Keychain item:

  ```bash
  /usr/bin/security delete-generic-password \
    -a dealswithdasch@gmail.com \
    -s com.taylordasch.youtube-analytics.readonly
  ```

- Google-side rollback is the Google Account **Third-party connections** page
  or OAuth revocation endpoint. Revocation is a separate confirmed action.
- Revert the cron command to stop scheduled pulls. Revert
  `scripts/weekly-pull.py` and remove `scripts/youtube_analytics_oauth.py` to
  roll back the code.
