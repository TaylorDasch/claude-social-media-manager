# Transcript to Blog

Convert a YouTube .SRT transcript into an AEO-optimized blog post.

## Usage
`/transcript-to-blog [path-to-srt] [video-url]`

## Arguments
- `$1` — Path to the .SRT file (required)
- `$2` — YouTube video URL (required for embed and schema)

## Execution
1. First run the `srt-corrector` skill on the provided .SRT file
2. Read the corrected .SRT file
3. Read `skills/transcript-to-blog/SKILL.md` for the full blog generation workflow
4. Read `governance/QUALITY-GATES.md` for quality enforcement
5. Read `reference/SCHEMA-LIBRARY.md` for schema templates
6. Read `reference/LEAD-MAGNET-MATRIX.md` for persona-matched CTA
7. Execute the transcript-to-blog skill with the corrected transcript
8. Generate: blog markdown + schema JSON-LD + internal link suggestions
9. Run the 16-point quality gate checklist
10. Save outputs to `output/YYYY-WXX/blog/`
11. Update `data/content-registry.csv` with new entry
