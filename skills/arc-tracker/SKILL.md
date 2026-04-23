---
name: /arc-tracker
description: Maintain narrative-arcs.json — the strategic content arc tracker. Arcs are multi-piece narratives (BSW Q2 Push, Temple Insider Spring Countdown, etc.). Tagging content to an arc is what lets /weekly-retro score whether we are compounding toward a named objective or scattering.
when-to-invoke: "arc", "arcs", "narrative arc", "tag to arc", "kill arc", "retire arc", "new arc", "arc tracker", "which arcs", "show arc", "list arcs"
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. QUALITY-GATES overrides any quality check in this skill. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done
- `governance/MULTI-PASS-SYSTEM.md` — 5-pass pipeline integration points

# Skill: /arc-tracker — Narrative Arc Tracker

## Trigger
"arc", "arcs", "narrative arc", "tag to arc", "kill arc", "retire arc", "new arc", "arc tracker", "which arcs", "show arc", "list arcs"

## What It Does
Owns `~/claude-social-media-manager/data/narrative-arcs.json`. Provides CLI to list, show, add, update, retire arcs and tag content to arcs. Read by `/weekly-retro` to compute arc velocity and surface kill/double-down candidates.

## Architecture

```
data/narrative-arcs.json          ← Canonical arc list. Stdlib JSON read/write.
  └── arcs[]                      ← id, name, description, audience,
                                    start_date, status, kill_date, kill_reason,
                                    target_content_count, related_content_ids[], notes

data/content-registry.csv         ← Read-only. Arc-tracker validates content_ids
                                    against this and joins on `show` command.

~/.hermes/scripts/arc-tracker.py  ← Python stdlib only. No pip installs.
```

Fail-soft: if `narrative-arcs.json` is missing or malformed, the tool starts with an empty arc list and warns on stderr.

## Commands

All commands dispatch through `python3 ~/.hermes/scripts/arc-tracker.py`.

### list — Human-readable arc table
```bash
python3 ~/.hermes/scripts/arc-tracker.py list
python3 ~/.hermes/scripts/arc-tracker.py list --status active
python3 ~/.hermes/scripts/arc-tracker.py list --status killed
```

### show — Full detail for one arc (joins against content-registry.csv)
```bash
python3 ~/.hermes/scripts/arc-tracker.py show --id BSW_Q2_2026
```

### add — Create a new arc
```bash
python3 ~/.hermes/scripts/arc-tracker.py add \
  --id MILITARY_PCS_Q2 \
  --name "Military PCS Q2 2026" \
  --audience military \
  --description "Fort Hood inbound PCS content block — Killeen vs Temple comparisons, VA loan education." \
  --target 8 \
  --notes "Peak PCS season May-August. Tie to bsw-domination/priority-todos."
```

### update — Modify fields or add/remove content tags
```bash
python3 ~/.hermes/scripts/arc-tracker.py update --id BSW_Q2_2026 \
  --add-content LIT-018 \
  --notes "Matt Levant lender channel activated 2026-04-10."

python3 ~/.hermes/scripts/arc-tracker.py update --id BSW_Q2_2026 \
  --status paused
```

### retire — Kill an arc with a reason (sets status=killed + kill_date + kill_reason)
```bash
python3 ~/.hermes/scripts/arc-tracker.py retire \
  --id MILITARY_PCS_Q2 \
  --reason "Pivoted — military content rolled into BSW_Q2 arc since 60% overlap."
```

### tag-content — Fast append of a content_id to an arc
```bash
python3 ~/.hermes/scripts/arc-tracker.py tag-content \
  --content-id LIT-018 \
  --arc-id BSW_Q2_2026
```
Warns (does not block) if content_id is not in content-registry.csv.

## Integration

- **Called by `/weekly-retro`:** `weekly-retro.py` reads `narrative-arcs.json` directly (no subprocess) and computes arc velocity (interactions / content_count) for each active arc.
- **Content registry is read-only:** Arc-tracker never writes to `content-registry.csv`. It only reads content_ids and titles to validate tags and render `show`.
- **Manual workflow:** Taylor invokes this skill when starting a new content block (e.g., a Q2 push) or retiring one (e.g., post-mortem after killing a seasonal arc).

## Seed arcs (already in place)

- `BSW_Q2_2026` — BSW Q2 Push — lender-channel content (Matt Levant / Acre Mortgage). Stark Law lock on hospital-employed gatekeepers.
- `TEMPLE_INSIDER_SPRING` — Temple Insider Spring Countdown — biweekly Tuesday buyer newsletter + 48-72hr blog conversion.

## Cost
Zero. No API calls. Pure local JSON + CSV reads.

## Rollback
```bash
# Reset to two seed arcs
cat > ~/claude-social-media-manager/data/narrative-arcs.json <<'JSON'
{"arcs":[{"id":"BSW_Q2_2026","name":"BSW Q2 Push","audience":"bsw","status":"active","start_date":"2026-04-01","target_content_count":12,"related_content_ids":[],"notes":"Lender channel only","description":"BSW push","kill_date":null,"kill_reason":null},{"id":"TEMPLE_INSIDER_SPRING","name":"Temple Insider Spring Countdown","audience":"buyer","status":"active","start_date":"2026-04-01","target_content_count":6,"related_content_ids":[],"notes":"Biweekly Tue","description":"Buyer newsletter","kill_date":null,"kill_reason":null}]}
JSON
```

Or to remove the skill entirely:
```bash
rm ~/.hermes/scripts/arc-tracker.py && rm -rf ~/claude-social-media-manager/skills/arc-tracker/
```

## Rules

- `id` values are SCREAMING_SNAKE_CASE, stable identifiers. Don't rename — retire and create new.
- Status transitions: `active` ↔ `paused` freely. `killed` is terminal — use `retire` for this and require a reason.
- Audience values: `bsw`, `buyer`, `investor`, `military`, `general`, `seller`. Unknown values warn but are accepted.
- Don't bulk-write the JSON file by hand when the CLI covers the operation — arc-tracker uses atomic write (tmp → replace) to avoid corrupt partial writes.
- When an arc's velocity falls into the bottom 20% on the weekly retro, read `notes` — kill/double-down triggers live there.
