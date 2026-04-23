---
name: reply-drafter
description: Draft contextual, voice-checked replies to unreplied social comments and DMs using community memory history. Pulls unreplied interactions from community-memory.db, surfaces handle history as context, drafts via Claude Sonnet, scores via voice-guardian (80+ threshold), pushes batch to Telegram for Taylor approval. Approve marks replied in DB and logs pattern to learning-journal. Runs automatically 3x/day via cron.
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done

## Validator Gate

Every reply draft is automatically scored by voice-guardian (threshold: 80/100).
- **80-100:** Push to Telegram as-is
- **<80:** Flag with ⚠️ in Telegram message — Taylor reviews before using
- **Always:** Taylor approves before the reply goes live anywhere

## When to invoke

- Watchdog flags unreplied handles in sm-brief output
- You see age >24h on any comment/DM in community-memory `unreplied` list
- Before the weekly retro to clear the backlog
- Proactively at session start when community-memory shows unreplied count

## Architecture

- **Script:** `~/.hermes/scripts/reply-drafter.py`
- **DB:** `~/claude-social-media-manager/data/community-memory.db` (reads unreplied, writes replied status)
- **Drafts:** `~/claude-social-media-manager/data/reply-drafts.json`
- **Model:** `claude-sonnet-4-6` (context-aware drafting, handles nuance)
- **Voice threshold:** 80/100 (lower than content threshold — replies are shorter/conversational)

## Commands

```bash
# Draft replies for oldest 5 unreplied interactions
python3 ~/.hermes/scripts/reply-drafter.py draft

# Draft + push to Telegram immediately
python3 ~/.hermes/scripts/reply-drafter.py draft --push-telegram

# Draft reply for one specific interaction (by ID from community-memory)
python3 ~/.hermes/scripts/reply-drafter.py draft-one --id 42 --push-telegram

# Show all pending drafts
python3 ~/.hermes/scripts/reply-drafter.py status

# Approve a draft (marks replied in DB, logs to learning-journal)
python3 ~/.hermes/scripts/reply-drafter.py approve --id 3

# Approve with edited text (Taylor's version wins)
python3 ~/.hermes/scripts/reply-drafter.py approve --id 3 --reply "Thanks — DM me and I'll send the comps"

# Reject and regenerate
python3 ~/.hermes/scripts/reply-drafter.py reject --id 3
python3 ~/.hermes/scripts/reply-drafter.py draft-one --id 42 --push-telegram
```

## Cron schedule

```
# Reply Drafter — draft unreplied after fresh community-memory ingest
10 8,14,20 * * * cd /Users/taylordasch_1 && /usr/bin/python3 /Users/taylordasch_1/.hermes/scripts/reply-drafter.py draft -n 5 --push-telegram >> /Users/taylordasch_1/.hermes/logs/reply-drafter.log 2>&1
```

3x/day. ~$0.10-0.30/day (5 drafts × Sonnet 4.6 = ~$0.02/draft). <$9/month.

## Reply voice rules

- Under 80 words for comments, under 150 words for DMs
- If relocation question → anchor to Fort Hood, BSW proximity, or specific neighborhood
- If market/property question → answer with data, or offer to send comps
- If just engagement → 1-2 sentences, warm, genuine
- No hashtags in replies
- No emojis unless original had them
- Never say "broker" — Taylor is an agent
- Soft next-step only when natural (DM me, happy to send comps)

## Integration chain

```
community-memory ingest-yt (7:45am)
  → engagement-queue build (8:00am)
  → reply-drafter draft --push-telegram (8:10am)
  → Taylor reviews Telegram batch
  → reply-drafter approve --id N (marks replied + logs to learning-journal)
```

## Learning loop

On every `approve`:
- If voice score ≥ 80: logs the handle context + approved reply to `learning-journal.py`
- Learning journal distills reply patterns into `learned-exemplars.json`
- Voice-check loads those exemplars next run → replies improve over time

## Rollback

`rm ~/claude-social-media-manager/data/reply-drafts.json` — clears all pending drafts.
Approved replies are already written to community-memory.db (use `mark-replied` to manually correct).
Remove cron line to stop automated drafting.
