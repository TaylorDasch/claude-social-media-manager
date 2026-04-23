# SRT Corrector

## Trigger
"fix srt", "correct srt", "clean transcript", "srt corrector", or any .SRT file path provided for cleanup.
Auto-fires via hook when any file is written to a directory containing .srt files.

## Required Inputs
- Path to .SRT file (auto-generated from YouTube, DaVinci Resolve, or Whisper)
- Optional: topic context (e.g., "neighborhood tour of Canyon Creek") to improve correction accuracy

## Step-by-Step Execution

### Step 1 — Load and Parse
1. Read the .SRT file completely
2. Parse into segments: sequence number, timecode (start --> end), text content
3. Count total segments and note duration

### Step 2 — Apply Proper Noun Corrections
Run find-and-replace across ALL text segments for these known corrections:

**Locations & Neighborhoods:**
- baylor scott and white → Baylor Scott & White
- b.s.w. / bsw / BSW → Baylor Scott & White (first mention), BSW (subsequent)
- fort cavazos → Fort Hood (name reverted July 2025)
- fort hood → Fort Hood
- temple texas → Temple, Texas / Temple, TX
- belton → Belton
- canyon creek → Canyon Creek
- pecan ridge → Pecan Ridge
- prairie ridge → Prairie Ridge
- alta vista → Alta Vista
- bella terra → Bella Terra
- lake pointe → Lake Pointe
- windmill farms → Windmill Farms
- legacy ranch → Legacy Ranch
- sage meadows → Sage Meadows
- parks at westfield → Parks at Westfield
- south pointe → South Pointe

**Builders:**
- dr horton / d.r. horton → DR Horton
- stylecraft → StyleCraft
- centex → Centex
- ashton woods → Ashton Woods
- gehan → Gehan Homes
- pulte → Pulte Homes
- scott felder → Scott Felder Homes
- castlerock → CastleRock Communities

**Real Estate Terms:**
- mls → MLS
- bah → BAH (Basic Allowance for Housing)
- pcs → PCS (Permanent Change of Station)
- dscr → DSCR
- brrrr / burr → BRRRR
- cap rate → cap rate (keep lowercase in mid-sentence)
- roi → ROI
- arv → ARV
- coc → CoC (Cash-on-Cash)
- hoa → HOA
- piti → PITI
- isd → ISD
- bigger pockets → BiggerPockets
- zillow → Zillow
- realtor.com → Realtor.com

**People & Entities:**
- taylor dash / taylor dasch → Taylor Dasch
- eg realty → EG Realty
- temple tx homes → templetxhomes.net (when referring to website)

**Numbers & Formatting:**
- Spell out dollar amounts consistently: "$250,000" not "250000" or "two hundred fifty thousand"
- Fix split numbers across subtitle segments (e.g., "two fifty" → "$250,000" when context is price)
- Fix "seventy six five oh two" → "76502"
- Fix phone number: "two five four seven one eight four two four nine" → "254-718-4249"

### Step 3 — Fix Common Speech-to-Text Errors
- "gonna" → "going to" (keep in casual sections, fix in data sections)
- "wanna" → "want to"
- "kinda" → "kind of"
- Remove filler words: "um", "uh", "like" (when filler, not comparison), "you know" (when filler)
- Fix homophones: "their/there/they're", "your/you're", "its/it's"
- Fix "per say" → "per se"
- Fix "real-a-tor" → "realtor"

### Step 4 — Preserve Timecodes
- NEVER modify timecodes — only text content
- Maintain exact SRT format: sequence number, timecode line, text line(s), blank line separator
- Do not merge or split segments

### Step 5 — Output
1. Write corrected .SRT to same directory with `-corrected` suffix (e.g., `video.srt` → `video-corrected.srt`)
2. Write a `corrections-log.md` listing every change made with line numbers
3. Report summary: total segments, corrections made, categories of corrections

## Output Format

### Corrected SRT (exact SRT format preserved)
```
1
00:00:00,000 --> 00:00:03,500
Taylor Dasch here with EG Realty.

2
00:00:03,500 --> 00:00:07,200
Today we're touring Canyon Creek in Temple, Texas.
```

### Corrections Log
```markdown
# SRT Corrections Log — [filename]
Date: YYYY-MM-DD
Total segments: XX
Total corrections: XX

## Corrections
| Line | Original | Corrected | Category |
|------|----------|-----------|----------|
| 14 | baylor scott and white | Baylor Scott & White | Proper Noun |
| 23 | fort cavazos | Fort Hood | Proper Noun |
| 47 | gonna | going to | Speech Cleanup |
```

## Quality Checks
- [ ] All proper nouns match the correction dictionary above
- [ ] No timecodes were modified
- [ ] SRT format is valid (can be reimported into DaVinci Resolve)
- [ ] Dollar amounts are formatted consistently
- [ ] Phone number appears as 254-718-4249
- [ ] "Fort Cavazos" → "Fort Hood" everywhere (ZERO exceptions)
- [ ] No "turnkey" — must be "buy-and-hold"
- [ ] No banned words from governance/QUALITY-GATES.md Gate 1

## Brand Rules
- Fort Hood, never Fort Cavazos
- Buy-and-hold, never turnkey
- EG Realty (exact capitalization)
- Taylor Dasch (exact spelling)
- Baylor Scott & White (full name first mention, BSW after)
