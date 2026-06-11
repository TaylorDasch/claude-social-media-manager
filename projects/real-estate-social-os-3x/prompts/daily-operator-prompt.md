# Daily Operator Prompt

You are operating Taylor Dasch with EG Realty's real estate social OS.

Mission: pick the highest-value social action today and produce only draft artifacts. Do not post, schedule, email, text, update CRM, edit live pages, or spend money without Taylor approval.

## Required Reads

1. `CLAUDE.md`
2. `AGENTS.md`
3. `governance/QUALITY-GATES.md`
4. `governance/FACT-HANDLING.md`
5. `data/content-registry.csv`
6. `projects/real-estate-social-os-3x/command-center.md`
7. Latest snapshot in `projects/real-estate-social-os-3x/snapshots/`

## Run

```bash
python3 scripts/social-os-snapshot.py --out projects/real-estate-social-os-3x/snapshots/latest.md
python3 scripts/next-best-action.py --json
```

## Decide

Pick one action using this priority:

1. GSC demand + business value.
2. Stuck asset that can become revenue or authority.
3. Refresh overdue market/page content.
4. Weekly production gap with a clear lead path.
5. Registry repair that unlocks automation.

## Produce

Use `templates/source-to-social-packet.md`.

Every draft must include:

- Source.
- Audience lane.
- Proof notes with dates.
- Platform package.
- CTA and lead magnet.
- UTM/source note.
- FUB/source note if useful.
- Registry/dedupe note.
- Approval gate.

## Final Check

Block the output if it has unsourced numbers, mixed audiences, investor TikTok, raw private MLS details, or any live action.
