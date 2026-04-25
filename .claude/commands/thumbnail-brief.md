# Thumbnail Brief

Generate a thumbnail composition brief with text, layout, expression, and brand colors.

## Usage
`/thumbnail-brief [video-title]`

## Arguments
- `$1` — Video title or topic (required)

## Execution
1. Read `.claude/skills/thumbnail-brief.md` for full workflow
2. Analyze the title to determine hook word and emotional angle
3. Apply 60-30-10 color rule with brand colors
4. Select best layout (Split Frame / Taylor Foreground / Comparison / Data Overlay)
5. Write thumbnail text (max 3-4 words, NEVER repeat the title)
6. Specify Taylor's expression and gaze direction
7. Include mobile readability check (168x94px test)
8. Provide A/B variant suggestion
9. Save to `output/YYYY-WXX/thumbnails/[slug]-thumbnail-brief.md`
