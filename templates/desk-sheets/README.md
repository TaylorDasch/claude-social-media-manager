# Desk Sheets

Three one-page, print-ready sheets for daily activity, weekly scoring, and annual goals.

| File | Print cadence | Purpose |
|------|---------------|---------|
| `01-daily-power-sheet.pdf` | 5 per week (or laminate + dry-erase) | Big 3, lead gen tally by persona, pipeline touches, today's SOP block, content shipped, end-of-day review |
| `02-weekly-scorecard.pdf` | 1 per week | Mon-Sun activity grid, content production vs targets, lead sources by FUB tag, Friday review checklist, DM keyword cheat sheet |
| `03-goals-pipeline-board.pdf` | 1 per year, update monthly | GCI goal to closings, funnel math to a daily conversation number, closings by persona, monthly scoreboard, pipeline snapshot |

Targets and checklists are pulled from `reference/WEEKLY-CONTENT-BATCH-SOP.md`, `skills/weekly-scorecard/SKILL.md`, `reference/CONTENT-TO-LEAD-ATTRIBUTION.md`, and `reference/LEAD-MAGNET-MATRIX.md`.

## Rebuild after editing the HTML

```
node templates/desk-sheets/build.js
```

Requires Playwright with Chromium. Each HTML file links `sheet.css`; per-sheet size tweaks live in a `<style>` block in the file head.
