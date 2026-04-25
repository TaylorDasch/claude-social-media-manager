---
name: community-memory
description: Query Hermes community memory — interaction history per handle across all platforms (YouTube, Instagram, LinkedIn, Facebook, Beehiiv). Invoke before drafting any reply to a commenter, DM, or mention to surface prior conversations, FUB linkage, unreplied backlog, and engagement patterns. Core primitive for Voice Guardian, Engagement Queue, and weekly retros.
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. QUALITY-GATES overrides any quality check in this skill. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done
- `governance/MULTI-PASS-SYSTEM.md` — 5-pass pipeline integration points

# Community Memory Skill

## When to invoke

Before drafting any reply (comment/DM/mention) → always lookup the handle first. Also invoke when:
- Building the weekly engagement queue
- Deciding whether to tag a commenter into FUB
- Answering "who is @handle" / "did we talk to them before"
- Weekly retro: top engagers, unreplied backlog, platform split

## Architecture

- **CLI:** `~/.hermes/scripts/community-memory.py`
- **DB:** `~/claude-social-media-manager/data/community-memory.db` (SQLite, two tables: `interactions`, `handles`)
- **Ingesters:** YouTube (built-in, `ingest-yt`). Instagram, LinkedIn, Facebook, Beehiiv replies → coming next.
- **Writers:** any script can call `record` to log an interaction. Engagement Queue marks replies via `mark-replied`.

## Commands

```bash
# History for one handle (primary use: before drafting reply)
python3 ~/.hermes/scripts/community-memory.py lookup <handle>

# Last N interactions globally or per-platform
python3 ~/.hermes/scripts/community-memory.py recent -n 20
python3 ~/.hermes/scripts/community-memory.py recent --platform youtube

# Unreplied queue, age-sorted (drives Engagement Queue)
python3 ~/.hermes/scripts/community-memory.py unreplied

# Top engagers + platform split
python3 ~/.hermes/scripts/community-memory.py stats

# Pull fresh YouTube comments (idempotent, dedups by URL)
python3 ~/.hermes/scripts/community-memory.py ingest-yt --videos 20 --max 100

# Log an interaction manually (for DMs, IG comments until ingesters exist)
python3 ~/.hermes/scripts/community-memory.py record \
  --platform instagram --handle @username --type dm \
  --content "moving to temple in june" --post-title "109 Raven listing"

# Mark replied
python3 ~/.hermes/scripts/community-memory.py mark-replied \
  --id 42 --reply "DM'd you the details"

# Export full CSV (for analysis / backup)
python3 ~/.hermes/scripts/community-memory.py export-csv \
  --out ~/claude-social-media-manager/data/community-memory-export.csv
```

## Output format when surfacing for reply drafting

Return to Claude:
- Handle + display name + platform
- FUB linkage status
- Total interactions + first/last seen
- Last 3-5 interactions verbatim (content quoted)
- Any unreplied from this handle
- Notes field

## Voice rules when drafting from this context

- Reference prior interactions naturally ("good to see you back", "you asked about BSW area last time")
- Never mechanically ("per our system, you have 3 interactions")
- Match prior tone — casual if their comments were casual, detailed if they asked data questions
- Never reveal that we're tracking — memory is for us, reply is for them
- If handle has FUB ID, check FUB status before offering stuff they already got (action plans, drip)

## Schema

**interactions:** `id, platform, handle, handle_display, interaction_type, content, content_url, post_ref, post_title, sentiment, timestamp, fub_id, replied, reply_content, reply_timestamp, notes, raw_json`

**handles:** `handle, display_name, platform, fub_id, first_seen, last_seen, total_interactions, notes`

## Interaction types
`comment, dm, mention, like, subscribe, share, question`

## Rollback
`rm ~/claude-social-media-manager/data/community-memory.db` — nukes everything. Script is idempotent, auto-creates schema on next run. No cron dependency yet (ingesters will be added to crontab in Component #3).
