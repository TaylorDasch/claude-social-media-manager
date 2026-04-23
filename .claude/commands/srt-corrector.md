# SRT Corrector

Clean up an auto-generated .SRT transcript: fix proper nouns, real estate terms, numbers, and filler words.

## Usage
`/srt-corrector [path-to-srt]`

## Arguments
- `$1` — Path to the .SRT file (required)

## Execution
1. Read `.claude/skills/srt-corrector.md` for the full correction dictionary
2. Read the .SRT file completely
3. Parse into segments (sequence number, timecode, text)
4. Apply proper noun corrections (Baylor Scott & White, Fort Hood, neighborhoods, builders)
5. Apply real estate term corrections (MLS, BAH, DSCR, BRRRR, etc.)
6. Fix number formatting (dollar amounts, zip codes, phone number)
7. Clean speech-to-text errors (filler words, homophones)
8. NEVER modify timecodes — text only
9. Save corrected .SRT with `-corrected` suffix
10. Save `corrections-log.md` with every change documented
11. Report summary: total segments, total corrections, correction categories
