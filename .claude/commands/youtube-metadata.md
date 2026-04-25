# YouTube Metadata

Generate complete YouTube metadata package: 3 title options, 7-section description, tags, pinned comment, and card placements.

## Usage
`/youtube-metadata [topic] [channel]`

## Arguments
- `$1` — Video topic or title (required)
- `$2` — Channel: "living" (Living in Temple) or "investing" (Investing in Temple). Default: "living"

## Execution
1. Read `.claude/skills/youtube-metadata.md` for full workflow
2. Read `reference/YOUTUBE-GROWTH-PLAYBOOK.md` for title formulas
3. Read `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt` for dedup check
4. Read `reference/LEAD-MAGNET-MATRIX.md` for CTA matching
5. Determine content pillar and target persona from topic
6. Generate 3 title options (under 60 chars each, no catalog duplicates)
7. Generate 7-section description with entity declaration in lines 3-5
8. Generate 30 tags (≤500 chars total)
9. Generate pinned comment with lead magnet + phone
10. Suggest card placements at 25%, 50%, 75%, end screen
11. Save to `output/YYYY-WXX/youtube/[slug]-metadata.md`
