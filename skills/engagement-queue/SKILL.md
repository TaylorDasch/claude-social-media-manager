---
name: engagement-queue
description: Pull unreplied social interactions from community-memory.db, draft voice-guarded replies with Sonnet, push a batch to Telegram for Taylor's approval, and mark items replied on approval. Runs on cron 3x daily (8am/2pm/8pm). Use when you want to scale engagement on YouTube/IG/LinkedIn/FB/TikTok/GMB without losing voice discipline. Trigger phrases — "engagement queue", "draft replies", "reply to comments", "eq-build", "approve reply".
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. QUALITY-GATES overrides any quality check in this skill. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done
- `governance/MULTI-PASS-SYSTEM.md` — 5-pass pipeline integration points

# Engagement Queue Skill

## When to invoke

- Automated on cron — Taylor approves from phone via Telegram three times a day.
- On-demand when a fresh batch of interactions lands (YouTube ingest, IG import, DM burst).
- Before posting events where reply latency matters (BSW physician newsletter drop, Matt Levant co-posts).

## Architecture

```
community-memory.db  (unreplied interactions)
         |
         v
  engagement-queue.py build      <-- Sonnet drafts reply using handle's
         |                            prior 5 interactions + post title
         v
  voice-check.py --json           <-- score 0-100; flag banned phrases,
         |                            wrong audience, hallucinated numbers
         v
  engagement-queue-state.json     <-- {id, platform, handle, draft,
         |                            voice_score, status: pending}
         v
  engagement-queue.py push-telegram
         |                        --> Taylor's phone: formatted card +
         v                            /eq-approve /eq-skip /eq-edit
  approve/skip                    --> approve: post (or MANUAL POST
                                      REQUIRED) + mark-replied in DB
                                  --> skip: leave unreplied in DB
```

- **Script:** `~/.hermes/scripts/engagement-queue.py` (stdlib only)
- **State:** `~/claude-social-media-manager/data/engagement-queue-state.json`
- **Archive:** `~/claude-social-media-manager/data/engagement-queue-archive/`
- **Logs:** `~/.hermes/logs/engagement-queue.log`
- **Draft model:** `claude-sonnet-4-6` via `https://api.anthropic.com/v1/messages`
- **Voice gate:** `voice-check.py --json` — threshold 85

## Commands

### build — draft replies for unreplied items

```bash
# Default (limit 20, all platforms)
python3 ~/.hermes/scripts/engagement-queue.py build

# Narrow to YouTube + Instagram, limit 5
python3 ~/.hermes/scripts/engagement-queue.py build --limit 5 --platforms yt,ig
```

Short codes: `yt`→youtube, `ig`→instagram, `li`→linkedin, `tt`→tiktok, `fb`→facebook. Long forms accepted too.

For each unreplied item (not already in state): pulls handle's last 5 interactions, calls Sonnet to draft, pipes draft through voice-check.py, stores result in state.json with status=`pending`.

### push-telegram — send batch to Taylor's phone

```bash
python3 ~/.hermes/scripts/engagement-queue.py push-telegram
python3 ~/.hermes/scripts/engagement-queue.py push-telegram --dry-run
```

One Telegram message per `pending` item:
- Queue ID + voice flag (OK / LOW nn)
- Platform + handle
- Post title (if any)
- Original comment (truncated 500 chars)
- Draft reply in code block + voice score
- Top issue if score <85
- Command line: `/eq-approve N  /eq-skip N  /eq-edit N <text>`

Marks item `status=pushed` on success. `--dry-run` prints to stdout, no state mutation.

### approve — post + mark replied

```bash
# Use drafted reply as-is
python3 ~/.hermes/scripts/engagement-queue.py approve --id 7

# Override with edited reply (re-runs voice-check — aborts if score <85)
python3 ~/.hermes/scripts/engagement-queue.py approve --id 7 --override-reply "Your edited text..."
```

On approve:
1. If `--override-reply`, re-score via voice-check. Score <85 → abort, state preserved.
2. Post to platform (see "Platform posting caveats" — MVP stubs all).
3. Call `community-memory.py mark-replied --id N --reply "..."`.
4. Set `status=posted`, persist `final_reply`, `posted_at`.

### skip — dismiss without replying

```bash
python3 ~/.hermes/scripts/engagement-queue.py skip --id 7
```

Marks state `status=skipped`. Does NOT mark-replied in DB — item stays in unreplied queue for future passes (or manual ignore).

### status — queue counts

```bash
python3 ~/.hermes/scripts/engagement-queue.py status
```

Prints total tracked + counts by status + age of oldest pending item in hours. Good for cron health checks.

### clear — archive state, reset

```bash
python3 ~/.hermes/scripts/engagement-queue.py clear
```

Moves `engagement-queue-state.json` → `engagement-queue-archive/engagement-queue-state-YYYYMMDD-HHMMSS.json`. Start fresh. Run after each fully-processed batch to keep state lean.

## Daily workflow

**Cron (document only — do NOT auto-install)**

```cron
# Build drafts 3x daily
0 8,14,20 * * * cd ~ && python3 ~/.hermes/scripts/engagement-queue.py build --limit 20 >> ~/.hermes/logs/engagement-queue.log 2>&1

# Push to Telegram 5 min after build
5 8,14,20 * * * cd ~ && python3 ~/.hermes/scripts/engagement-queue.py push-telegram >> ~/.hermes/logs/engagement-queue.log 2>&1
```

**Approval loop (Taylor, from phone)**

1. Telegram DM lands with 5-20 draft cards.
2. Review voice score + draft + issue note per card.
3. For each: tap command at bottom — `/eq-approve N` ships the draft, `/eq-skip N` dismisses, `/eq-edit N <text>` hands a corrected version.
4. End-of-day: one `clear` pass to archive state. Next cron cycle builds fresh.

The `/eq-*` commands are human-readable; current MVP doesn't auto-parse them from Telegram — Taylor runs the matching `approve`/`skip` CLI command from any terminal (or via Claude Desktop). Next iteration: wire into the `@taylordaschbot` Railway bot for true one-tap approval.

## Platform posting caveats (honest MVP scope)

| Platform | Auto-post? | Why |
|----------|-----------|-----|
| YouTube | No — manual paste | `commentThreads.insert` requires OAuth2 user consent, not just API key |
| Instagram | No — manual paste | No stable public reply API; Graph API requires Meta app review |
| LinkedIn | No — manual paste | Comment reply API gated, personal profiles especially |
| Facebook | No — manual paste | Page reply requires Page access token, not wired |
| TikTok | No — manual paste | Reply API not exposed for creators |
| GMB | No — manual paste | Reviews reply available via Business Profile API, not wired |

For every approve, the script prints:

```
============================================================
MANUAL POST REQUIRED — <platform>/<handle>
URL: <content_url>

Reply to paste:
<text>
============================================================
```

...then calls `community-memory.py mark-replied` so the DB reflects the commitment. Taylor copy-pastes on phone, DB is already consistent. Future iteration: wire OAuth for YouTube first (highest reply volume).

## Integration

### Community Memory

- `community-memory.py unreplied` = source-of-truth input for `build`.
- `community-memory.py lookup <handle>` equivalent = used in prompt context (last 5 interactions via direct sqlite read).
- `community-memory.py mark-replied --id N --reply "..."` = invoked on approve (shells out, not direct SQL, so any future DB triggers stay wired).

### Voice Guardian

- Every draft piped through `voice-check.py --json --platform X --audience Y` before landing in state.
- Every override reply re-scored; score <85 aborts approve with issues printed.
- Platform-to-voice mapping lives in `PLATFORM_MAP` in the script (youtube → youtube_living/buyer, instagram → instagram/buyer, etc.).

### FUB / downstream

Not wired in MVP. Future: on approve, if handle has `fub_id`, append note "replied to <platform> comment" to FUB person record.

## Cost estimate

- Sonnet 4.6 draft: ~1.5K input + 200 output tokens ≈ $0.01/draft
- Voice-check (Haiku 4.5): ~$0.003/score
- 20 drafts/day × 3 cycles × $0.013 ≈ **$0.78/day ≈ $23/month** — below spec's $6/mo because cycles aren't all full.
- Conservative cap: 20 drafts × 3 × $0.013 = $23/mo at worst. Spec's $6/mo assumes ~20 drafts/day total (one cycle active). Actual usage depends on unreplied backlog.

## Rollback

One command:

```bash
rm -f ~/.hermes/scripts/engagement-queue.py && rm -rf ~/claude-social-media-manager/skills/engagement-queue ~/claude-social-media-manager/data/engagement-queue-state.json ~/claude-social-media-manager/data/engagement-queue-archive
```

DB untouched — any items already marked-replied stay marked.

## Verification (post-build test run)

Tested end-to-end with 2 seeded interactions (eqtest1 YouTube, eqtest2 Instagram):

- `build --limit 5 --platforms yt,ig` → 2 drafts, scores 78/78 (both flagged minor issues, correctly)
- `push-telegram --dry-run` → clean formatting, commands rendered
- `approve --id 5 --override-reply "<bad text>"` → correctly aborted at voice score 62
- `approve --id 5` (no override) → manual-post warning fired, `community-memory.py mark-replied` invoked, DB row `replied=1` confirmed
- `skip --id 4` → state skipped, DB `replied=0` preserved (correct — skip ≠ reply)
- `status` → pending 0 / posted 1 / skipped 1 / pushed 0
- `clear` → archived to `engagement-queue-state-20260417-060151.json`, state.json removed
- Test rows deleted: `DELETE FROM interactions WHERE handle LIKE 'eqtest%'`
