---
name: learning-journal
description: Daily feedback loop that turns engagement-queue approvals, edits, and skips into patterns that auto-improve Voice Guardian. Extracts voice deltas from archived drafts vs. Taylor's edits (via Haiku), harvests CRUSH/SOLID signals from the performance-ledger, counts hijack-feed claim rates, and grows a learned-exemplars.json bank that voice-check.py auto-loads. Writes a daily markdown journal and a Sunday weekly rollup. Trigger phrases — "learning journal", "what did we learn", "learnings today", "lj-scan", "lj-journal".
---

## Governance

Read `governance/QUALITY-GATES.md` before interpreting patterns — quality rules still override. This skill proposes patterns; the rubric editor or Taylor applies them.

# Learning Journal Skill

Hermes SM Component #7. This is the "learning" in "always on / learning / improving." Every approval, edit, and skip becomes training signal. Over time the voice-check exemplar bank grows, the rubric sharpens, and the news-hijack weights self-correct.

## Architecture

```
read-only sources                         learning-journal.py scan
---------------------------------------------------------------
engagement-queue-state.json        ───┐       (Haiku distillation)
engagement-queue-archive/*.json    ───┼──→   voice_delta patterns
performance-ledger.csv             ───┤      crush_pattern rows
hijack-claimed.csv                 ───┤      hijack_claim rows
community-memory.db                ───┤      (context only)
voice-rubric.json                  ───┘      (rubric state reference)

writable outputs
---------------------------------------------------------------
learning-journal/learnings.db        (patterns table + scan_state)
learning-journal/YYYY-MM-DD.md       (daily markdown)
learning-journal/weekly-YYYY-MM-DD.md (Sunday rollup)
learned-exemplars.json               (auto-grown exemplar bank —
                                      voice-check.py auto-loads)
```

- **Script:** `~/.hermes/scripts/learning-journal.py` (stdlib only)
- **Log:** `~/.hermes/logs/learning-journal.log`
- **Distillation model:** `claude-haiku-4-5-20251001` (cheap — voice delta only)
- **Exemplar threshold:** voice_score ≥ 90 (posted) or CRUSH ledger tier

## What gets extracted

### 1. Voice delta patterns

For every posted engagement-queue item where `override_reply` differs from
the original `draft`, Haiku distills a one-line pattern:

> "In youtube_living / buyer / school questions, Taylor replaces generic 'good schools' with specific school name + GreatSchools rating."

Stored in `patterns` with `pattern_type='voice_delta'`. Evidence JSON records
the before/after.

### 2. CRUSH / SOLID / MEH signals

New rows in `performance-ledger.csv` (since last scan) are grouped by
platform. CRUSH rows generate a `crush_pattern` row plus seed the exemplar
bank (title + ranking_notes pulled in as a learned exemplar at proxy score
95).

### 3. Hijack-feed claim rates

`hijack-claimed.csv` rows since last scan are bucketed by pillar. Claim rate
drives a verdict:

- ≥60% claimed → "keep feed weight ≥ 1.5"
- 20-60% → "hold feed weight"
- ≤20% → "lower feed weight"

Stored as `hijack_claim` pattern.

### 4. Skip-reason patterns

If an engagement-queue archive item has a populated `skip_reason` field
(Taylor feeds this via `/eq-skip <id> <reason>`), it's stored as
`skip_reason` pattern. Repeated skip signals surface anti-patterns.

### 5. Exemplar harvesting

Two sources grow `learned-exemplars.json` (capped at 500, newest-first):

1. `engagement-queue-archive` items with `status=posted` AND
   `voice_score_override >= 90` — the final posted reply becomes an
   exemplar with `source: "engagement-queue"`.
2. `performance-ledger.csv` rows with `taylor_rating=CRUSH` — the
   `ranking_notes` or `taylor_notes` becomes an exemplar with proxy
   voice_score 95, `source: "performance-ledger-crush"`.

`voice-check.py` auto-loads this file and merges with `hook-bank.json`.
Effective exemplar pool grows from 10 (pre-learning) to up to 15 per call.

## learnings.db schema

```sql
CREATE TABLE patterns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,                   -- YYYY-MM-DD extraction date
  pattern_type TEXT NOT NULL,           -- voice_delta | crush_pattern |
                                        -- hijack_claim | skip_reason | general
  context TEXT,                         -- 'platform:X/audience:Y/topic:Z'
  pattern TEXT NOT NULL,                -- one-line reusable pattern
  evidence TEXT,                        -- JSON blob with diff/notes
  confidence REAL DEFAULT 0.5,          -- 0..1 Haiku-reported
  source_ref TEXT,                      -- archive file + item id
  applied INTEGER DEFAULT 0             -- 1 if Taylor marked applied
);

CREATE TABLE scan_state (
  key TEXT PRIMARY KEY,
  value TEXT
);

-- scan_state keys:
--   eq_last_archive   last archive filename scanned
--   ledger_last_ts    last performance-ledger date
--   hijack_last_ts    last hijack-claimed timestamp
--   scan_summary_YYYY-MM-DD   JSON stats bundle for journal reuse
```

## Commands

### scan — incremental extraction

```bash
python3 ~/.hermes/scripts/learning-journal.py scan
python3 ~/.hermes/scripts/learning-journal.py scan --since 2026-04-10
```

- Walks archives newer than `eq_last_archive`.
- For each `posted` item where draft != final_reply, calls Haiku to extract
  voice delta (~ $0.005 each).
- For each `posted` item with voice_score ≥ 90, seeds exemplar.
- Walks new ledger rows (by date) and new hijack-claimed rows (by timestamp).
- Updates watermarks in `scan_state`.
- Stores a same-day summary for `journal` to reuse.

Safe to re-run; watermarks prevent double-processing.

### journal — render daily markdown

```bash
python3 ~/.hermes/scripts/learning-journal.py journal
python3 ~/.hermes/scripts/learning-journal.py journal --date 2026-04-17
python3 ~/.hermes/scripts/learning-journal.py journal --push-telegram
python3 ~/.hermes/scripts/learning-journal.py journal --push-telegram --dry-run
```

Writes `~/claude-social-media-manager/data/learning-journal/YYYY-MM-DD.md`
(~15-25 lines). Sections:

- **Yesterday's haul** — archive / queue / ledger / hijack counts.
- **What I learned** — top patterns grouped by type, with confidence.
- **Anti-patterns caught** — skip reasons from archives.
- **Meta** — totals, apply-pattern command reminder.

`--push-telegram` DMs Taylor. `--dry-run` prints without writing or pushing.

### weekly-summary — Sunday 7-day rollup

```bash
python3 ~/.hermes/scripts/learning-journal.py weekly-summary --push-telegram
```

Writes `learning-journal/weekly-YYYY-MM-DD.md` and optionally pushes. Runs
1 hr after Sunday weekly-retro (17:00 CT retro → 18:00 CT summary). Feeds
retro with the week's extracted patterns but does not re-run the retro.

### stats — counts + scan watermarks

```bash
python3 ~/.hermes/scripts/learning-journal.py stats
```

Prints total patterns, counts per type, exemplar count, and scan state.
Use for cron health checks.

### apply-pattern — mark a pattern as reflected in rubric

```bash
python3 ~/.hermes/scripts/learning-journal.py apply-pattern --id 12
```

Flips `applied=1` after Taylor edits `voice-rubric.json` or
`hook-bank.json` to reflect the pattern. Unapplied high-confidence
patterns bubble up in future journals as reminders.

## Voice-check integration (already wired)

`voice-check.py` now loads both `hook-bank.json` AND
`learned-exemplars.json`:

```python
LEARNED_EXEMPLARS = SM / "data" / "learned-exemplars.json"

def load_exemplars(platform=None):
    items = []
    # 1. seeded hook-bank
    if HOOK_BANK.exists():
        ...
    # 2. learned exemplars (auto-grown)
    if LEARNED_EXEMPLARS.exists():
        try:
            learned = json.load(LEARNED_EXEMPLARS.open())
            if isinstance(learned, list):
                if platform:
                    learned = [e for e in learned
                               if isinstance(e, dict)
                               and e.get('platform') == platform]
                seen = {json.dumps(e, sort_keys=True) for e in items}
                for e in learned:
                    key = json.dumps(e, sort_keys=True)
                    if key not in seen:
                        items.append(e)
                        seen.add(key)
        except Exception:
            pass
    return items[:15]   # raised from 10 → 15
```

Effective pool per voice check: 15 exemplars (was 10), mixed seeded +
learned. The exemplar block in the Haiku prompt auto-picks up Taylor's
actual language over time.

## Cron (document only — do NOT auto-install)

Add to `crontab -e` when ready:

```cron
# Hermes learning journal — daily scan + push
30 5 * * * cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/learning-journal.py scan >> /Users/taylordasch_1/.hermes/logs/learning-journal.log 2>&1
45 5 * * * cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/learning-journal.py journal --push-telegram >> /Users/taylordasch_1/.hermes/logs/learning-journal.log 2>&1

# Sunday weekly rollup — 18:00 CT, 1 hr after existing weekly-retro (17:00)
0 18 * * 0 cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/learning-journal.py weekly-summary --push-telegram >> /Users/taylordasch_1/.hermes/logs/learning-journal.log 2>&1
```

**Timing rationale:** scan at 05:30 CT (after overnight engagement-queue
archive clears), journal at 05:45 CT (before 06:00 morning brief).

## Cost estimate

- Haiku voice-delta distillation: ~$0.005 per edited item.
- Typical: 1-5 edited replies/day → $0.005-0.025/day → $0.15-0.75/month.
- Weekly summary: no LLM call (just SQL rollup).
- Cap at $2/month under any reasonable use.

## BSW channel integration

Any BSW-related draft Taylor edits (handle matches Matt Levant / Acre
Mortgage / @baylorscottandwhite / other BSW keywords) feeds back into voice
delta patterns. Over the next quarter this should produce a dedicated
BSW-lender-channel pattern cluster the rubric can bake in.

## Rollback

One command:

```bash
rm -f ~/.hermes/scripts/learning-journal.py && \
  rm -rf ~/claude-social-media-manager/skills/learning-journal \
         ~/claude-social-media-manager/data/learning-journal \
         ~/claude-social-media-manager/data/learned-exemplars.json
```

`voice-check.py` degrades gracefully when `learned-exemplars.json` is
absent (the else-branch is a no-op). No DB touched outside
`learnings.db`, which lives entirely under the learning-journal dir.

## Verification (post-build test run)

Tested end-to-end against real state 2026-04-17:

- `scan --since 2026-04-10` → 1 archive, 1 posted item, 10 new ledger rows
  (2 CRUSH), 1 hijack row. Extracted 1 crush_pattern + 1 hijack_claim
  pattern. 2 exemplars seeded from CRUSH tier.
- `journal --date 2026-04-17` → wrote 26-line markdown at
  `data/learning-journal/2026-04-17.md` with all sections populated.
- `journal --push-telegram --dry-run` → 1 chunk, 1010 chars, valid
  Markdown.
- `stats` → 2 total patterns, 2 learned exemplars, watermarks set.
- `weekly-summary --dry-run` → coherent rollup, pattern counts, exemplar
  bank by platform.
- `voice-check.py --help` → still parses.
- Live voice-check with a test draft → returns valid JSON score,
  `load_exemplars('youtube')` now returns 15 mixed exemplars including 1
  CRUSH-tier learned item.

## Future iterations

- Wire voice-rubric auto-update: high-confidence patterns (≥0.85, applied
  manually 3x) auto-append to `voice-rubric.json` banned phrases or
  required elements.
- Promote confident voice-deltas to `hook-bank.json` formulas.
- Send BSW-specific patterns to the BSW Domination plan feedback loop.
- Track exemplar influence: when a voice-check call cites a learned
  exemplar in the rewrite, log which one so we can see which learnings
  actually change outputs.
