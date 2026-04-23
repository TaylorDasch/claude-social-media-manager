---
name: sm-brief
description: Use when Taylor wants a single-pane-of-glass status on Hermes SM (engagement, news-hijack, arcs, content, performance) AND/OR to surface items slipping past staleness thresholds. Triggers: "sm status", "hermes status", "what's stale", "watchdog", "sm brief", or the two daily cron firings. This is the "always on" layer of Hermes SM component #8 — brief aggregates, watchdog proactively nags.
---

# Hermes SM Brief + Watchdog (Component #8)

Single Python CLI at `~/.hermes/scripts/sm-brief.py`. Stdlib only — no pip dependencies.

## Subcommands

| Command | Purpose |
|---------|---------|
| `brief` | Aggregate current Hermes SM state into `~/.hermes/data/hermes-sm-brief.md` |
| `watch` | Run staleness checks → update `hermes-sm-alerts.json`, dedupe vs seen cache, optionally push NEW alerts |
| `full` | Brief + Watch back-to-back in a single Telegram message |
| `status` | Print last brief write + alert counts by severity |

All three action commands accept `--push-telegram` and `--dry-run`.

## Brief format (Telegram-friendly, ≤2000 chars)

```
🔸 HERMES SM — [YYYY-MM-DD HH:MM CT]

📨 Engagement
  {pending}/{pushed}/{posted}/{skipped} queue state
  {n} unreplied in community-memory (oldest: {age}h — @{handle})

📰 News-Hijack
  Queue: {pending} pending / {total} total | Top score: {s} — "{title}" ({pillar})
  Today claimed: {n} | This week: {n}

🎬 Content
  Arcs active: {n} | Flagged: {quiet_arc_names}
  New content last 7d: {n} | Missing arc tag: {n}
  Last weekly-retro: {date} (exec score {x}/10)

📊 Performance
  Ledger rows last 7d: {n}
  CRUSH-rated this week: {content_ids}
```

Missing or empty sources degrade gracefully to `—` or `no data yet`.

## Watchdog alerts (7 checks)

| # | Alert type | Trigger | Severity | Dedup key |
|---|------------|---------|----------|-----------|
| 1 | `unreplied` | community-memory `replied=0` AND `interaction_type IN ('comment','dm','mention','question')` AND age > 48h | high | interaction id |
| 2 | `arc_quiet` | Active arc with no content-registry row in last 7d matching its `related_content_ids` | medium | arc id |
| 3 | `orphan_content` | Content-registry rows with publish_date in last 7d not in any arc's `related_content_ids` | medium | sorted orphan IDs |
| 4 | `listing_stale` | content-registry pillar ∈ {Property Tours, Listings, Listing Spotlight} AND `last_reviewed` > 7d ago | low | content_id |
| 5 | `retro_missing` | Today > Sunday 19:00 CT AND no `weekly-retros/{last_sunday}.md` | medium | expected Sunday stem |
| 6 | `hijack_stale` | hijack-queue item `status=pending` AND `first_seen` > 48h old | low | hijack id |
| 7 | `engagement_idle` | `engagement-queue-state.json` mtime > 12h (no cycles) | medium | mtime 6h bucket |

Each alert: `{id, type, severity, message, created_at, context}`. `id = sha1("{type}|{dedup_key}")[:16]`.

## Dedup

- `hermes-sm-alerts.json` holds the CURRENT snapshot (written every watch run).
- `sm-brief-seen.json` maps `{alert_id: last_pushed_iso}`.
- Alert is "NEW" if never seen OR last push > 6h ago.
- Only NEW alerts are pushed to Telegram. Full snapshot still written to `hermes-sm-alerts.json`.

## Telegram output

Uses `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` from `~/shared-keys.env`. Text is chunked at 3,900 chars (safely below the 4,096 Telegram limit).

- `brief --push-telegram` pushes the brief body.
- `watch --push-telegram` pushes only NEW alerts (`"🔸 HERMES WATCHDOG [HH:MM CT] — N new alert(s)"` + message list).
- `full --push-telegram` pushes brief body followed by `NEW ALERTS (N):` + messages.

## Files

Created/overwritten by this skill:

| File | Role |
|------|------|
| `~/.hermes/data/hermes-sm-brief.md` | Latest aggregated status (overwritten every brief run) |
| `~/.hermes/data/hermes-sm-alerts.json` | Current alert snapshot (overwritten every watch run) |
| `~/.hermes/data/sm-brief-seen.json` | Dedup cache `{alert_id: last_pushed_iso}` |
| `~/.hermes/logs/sm-brief.log` | Cron output (stdout + stderr) |

Read-only sources (never modified):

- `~/claude-social-media-manager/data/community-memory.db` (interactions, handles)
- `~/claude-social-media-manager/data/hijack-queue.json`, `hijack-claimed.csv`
- `~/claude-social-media-manager/data/narrative-arcs.json`
- `~/claude-social-media-manager/data/content-registry.csv`
- `~/claude-social-media-manager/data/performance-ledger.csv`
- `~/claude-social-media-manager/data/engagement-queue-state.json`
- `~/claude-social-media-manager/data/weekly-retros/*.md` (latest)
- `~/shared-keys.env` (Telegram token + chat id)

## Cron (do NOT install — document only)

```cron
# SM Brief aggregator — twice daily (post-morning + mid-afternoon)
32 6 * * * cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/sm-brief.py full --push-telegram >> /Users/taylordasch_1/.hermes/logs/sm-brief.log 2>&1
0 16 * * * cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/sm-brief.py brief >> /Users/taylordasch_1/.hermes/logs/sm-brief.log 2>&1

# Watchdog — every 2 hours during active hours (with 6h dedup)
0 8,10,12,14,16,18,20 * * * cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/sm-brief.py watch --push-telegram >> /Users/taylordasch_1/.hermes/logs/sm-brief.log 2>&1
```

Rationale: 6:32 am lands 2 min after the existing 6:30 am morning-briefing — layered stack. 4:00 pm refreshes the brief before Taylor's afternoon block. Watchdog runs 7× during active hours with the 6h dedup preventing re-push of the same alert.

## BSW linkage

`arc_quiet` alert for arc id `BSW_Q2_2026` is the trip-wire for BSW velocity slipping. Kill-or-double-down prompt maps directly to the lender-channel doubling-down playbook at `bsw-domination/BSW-DOMINATION-MASTER-PLAN.md` — Matt Levant (Acre Mortgage) is the only legal BSW pipeline under Stark Law, so a quiet arc = push more Matt Levant content, not pivot.

## Manual usage

```bash
# Aggregated status → stdout + hermes-sm-brief.md
/usr/bin/python3 ~/.hermes/scripts/sm-brief.py brief

# Dry-run watch (no writes, no push) — shows which alerts would fire
/usr/bin/python3 ~/.hermes/scripts/sm-brief.py watch --dry-run

# Combined push to Telegram (overrides 6h dedup only for new alerts)
/usr/bin/python3 ~/.hermes/scripts/sm-brief.py full --push-telegram

# Counts + last-write
/usr/bin/python3 ~/.hermes/scripts/sm-brief.py status
```

## Extension points

- Add check #8+: new threshold → extend `compute_alerts()` in `sm-brief.py`, append to the table above.
- Loosen/tighten thresholds: edit constants at the top of `sm-brief.py` (`UNREPLIED_HOURS_THRESHOLD`, `ARC_QUIET_DAYS_THRESHOLD`, etc.).
- Swap Telegram for Slack: replace `telegram_send()` — signature is `(text: str, env: dict) -> (ok, msg)`.
