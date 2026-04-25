---
name: /weekly-retro
description: Sunday 5pm retro — scores the last 7 days of content, computes narrative-arc velocity, flags kill/double-down candidates, surfaces scatter-shot content, and writes a Cowork-Scribe-style coaching report. Optionally pushes to Telegram. Coach voice quotes Taylor verbatim from performance-ledger, scores moments 1-10, gives next-week scripts, names vulnerability/stress signals.
when-to-invoke: "weekly retro", "retro", "Sunday retro", "content retro", "arc velocity", "weekly coaching", "weekly review coaching", "push retro"
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. QUALITY-GATES overrides any quality check in this skill. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done
- `governance/MULTI-PASS-SYSTEM.md` — 5-pass pipeline integration points

# Skill: /weekly-retro — Weekly Retro + Arc Tracker Scorer

## Trigger
"weekly retro", "retro", "Sunday retro", "content retro", "arc velocity", "weekly coaching", "weekly review coaching", "push retro"

## What It Does
Once a week (Sunday 5pm), scores the last 7 days:

1. **Content shipped** — joined from `content-registry.csv` (publish_date in window)
2. **Arc velocity** — for each active arc in `narrative-arcs.json`, computes `interactions / content_count` using `community-memory.db` and the arc's `related_content_ids`
3. **Kill/double-down candidates** — bottom 20% of active arcs by velocity
4. **Scatter-shot risk** — content shipped this week not tagged to any arc
5. **Cowork-Scribe coaching report** — scored wins/slips, verbatim quotes from `taylor_notes`, scripts for next week, vulnerability/stress signals, BSW Next

Output: `data/weekly-retros/YYYY-MM-DD.md`. Optional Telegram push (auto-chunks at 4096 chars).

## Architecture

```
Inputs (READ-ONLY):
  data/performance-ledger.csv        ← Taylor's verbatim notes
  data/content-registry.csv          ← Content shipped this week
  data/community-memory.db           ← Interactions (direct sqlite3, ro mode)
  data/narrative-arcs.json           ← Arcs + related_content_ids[]

Output:
  data/weekly-retros/YYYY-MM-DD.md   ← Markdown retro
  Telegram                           ← Chunked at 4096 chars (Markdown mode)

Dependencies:
  ~/shared-keys.env                  ← ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
  Python 3 stdlib only               ← urllib, sqlite3, csv, json
  claude-sonnet-4-6                  ← The coach LLM
```

## Commands

### generate — Build the retro
```bash
# Dry-run: print to stdout, no write, no push
python3 ~/.hermes/scripts/weekly-retro.py generate --dry-run

# Default: writes to data/weekly-retros/YYYY-MM-DD.md
python3 ~/.hermes/scripts/weekly-retro.py generate

# Generate + push to Telegram
python3 ~/.hermes/scripts/weekly-retro.py generate --push

# Two-week lookback (useful if last week was missed)
python3 ~/.hermes/scripts/weekly-retro.py generate --weeks-back 2

# Dry-run the full generate + telegram-push flow
python3 ~/.hermes/scripts/weekly-retro.py generate --dry-run --push
```

### push — Send a previously-generated retro to Telegram
```bash
# Today's retro
python3 ~/.hermes/scripts/weekly-retro.py push

# Specific date
python3 ~/.hermes/scripts/weekly-retro.py push --date 2026-04-17

# Dry-run — print chunks, don't send
python3 ~/.hermes/scripts/weekly-retro.py push --dry-run --date 2026-04-17
```

### arc-scores — Just the arc velocity table (no LLM call, no cost)
```bash
python3 ~/.hermes/scripts/weekly-retro.py arc-scores
python3 ~/.hermes/scripts/weekly-retro.py arc-scores --weeks-back 2
```

## Cowork-Scribe Coaching Rules (baked into the system prompt)

The LLM is instructed to:
1. Score every moment 1-10 with a number. "8/10" beats "great work."
2. Quote Taylor verbatim from `taylor_notes`. Name his actual words.
3. Name both what went well AND what to tighten — never one side.
4. Always include a script for next time — exact words, ready to use.
5. Tie dollar or pipeline impact ($5,400 Arleene deal, BSW = 6-figure channel).
6. Spot vulnerability/stress signals (workload, consistency anxiety, overwhelm).
7. Propose root-fix habit, not band-aid.
8. Don't whitewash. Honest, kind, specific.
9. No generic real estate language. No emojis unless Taylor uses them.

## Integration

- **Reads `narrative-arcs.json`** directly (maintained by `/arc-tracker`)
- **Reads `content-registry.csv`** (managed by other SMM skills like `/produce`, `/deal-of-the-week`)
- **Reads `performance-ledger.csv`** (Taylor populates verbatim after each content drop)
- **Reads `community-memory.db`** (`interactions` table, populated by `engagement-queue.py` + collectors)
- **Called by cron on Sundays** (see below)

## Cron (document only — do NOT install unprompted)

```
0 17 * * 0 cd ~ && python3 ~/.hermes/scripts/weekly-retro.py generate --push >> ~/.hermes/logs/weekly-retro.log 2>&1
```

Sunday 5pm local time. Writes to `~/.hermes/logs/weekly-retro.log`. To install later:
```bash
( crontab -l 2>/dev/null; echo '0 17 * * 0 cd ~ && python3 ~/.hermes/scripts/weekly-retro.py generate --push >> ~/.hermes/logs/weekly-retro.log 2>&1' ) | crontab -
```

## Cost

- Sonnet 4.6: ~1500 input tokens + ~2400 output tokens per retro.
- Per retro: ≈ $0.03.
- 4 runs/month: ≈ $0.12/mo. Negligible.
- Dry-run still calls the LLM (it prints the generated markdown instead of writing/pushing). To preview structure without LLM cost, use `arc-scores`.

## Degradation / Fail-soft

- **Empty ledger this week** — the retro flags sparse data and asks Taylor to populate `taylor_notes` going forward.
- **No active arcs** — retro still runs; the arc-status table shows "(no active arcs to score)".
- **community-memory.db missing or empty** — interactions section shows "(no interactions recorded)".
- **Telegram HTTP error on Markdown parse** — automatic retry as plain text.
- **ANTHROPIC_API_KEY missing** — hard fail with clear error (no silent no-op).

## Sparse-data warning

Taylor's `performance-ledger.csv` is the quality lever for coaching voice. If rows lack `taylor_notes` or `taylor_rating`, the retro degrades to generic pattern commentary — still useful, but less pointed. The script can't invent verbatim quotes that don't exist. Populate `taylor_notes` after each publish and the retro sharpens immediately.

## Rollback
```bash
# Stop the scheduled run
crontab -l | grep -v weekly-retro.py | crontab -

# Remove the script
rm ~/.hermes/scripts/weekly-retro.py

# Optional — wipe generated retros
rm -rf ~/claude-social-media-manager/data/weekly-retros/

# Optional — remove the skill doc
rm -rf ~/claude-social-media-manager/skills/weekly-retro/
```

## Rules

- **Read-only sources.** Never write to performance-ledger.csv, content-registry.csv, or community-memory.db. Write only to `data/weekly-retros/`.
- **Stdlib only.** No `pip install`. Uses `urllib`, `sqlite3`, `csv`, `json`, `argparse`.
- **Chunk Telegram at 4096 chars.** Markdown mode with plain-text fallback on HTTP error.
- **The retro is coaching, not summary.** Don't let the LLM slip into "great week! you did X and Y" — the prompt explicitly demands scored wins, scored slips, and verbatim quotes.
- **BSW Next** section is mandatory — pulls from `BSW_Q2_2026` arc notes. If velocity slips, the retro escalates to the Matt Levant lender-channel doubling-down move.
