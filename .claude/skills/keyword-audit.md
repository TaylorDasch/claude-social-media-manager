# Keyword Density Auditor

## Trigger
"keyword audit", "keyword density", "transcript keywords", "spoken keyword check", "srt keyword analysis"

## Required Inputs
- .SRT file path or transcript text
- Target keyword list (or auto-generate from content pillar)

## Step-by-Step Execution

### Step 1 — Define Target Keywords
If no keyword list provided, generate from the content pillar:

**Neighborhood Tour:**
temple tx, temple texas, [neighborhood name], homes for sale, real estate, neighborhood tour, living in temple, [zip code], baylor scott and white, fort hood, belton isd, temple isd

**Market Data:**
temple tx real estate, housing market, median home price, days on market, inventory, market update, [year], appreciation, interest rates

**Investor Education:**
temple tx investing, buy and hold, rental property, cash flow, cap rate, roi, brrrr, dscr, section 8, fort hood rental, bah

**Relocation Guide:**
moving to temple tx, temple texas, cost of living, pcs fort hood, baylor scott and white, best neighborhoods, schools, things to do

**Listing Showcase:**
[address], temple tx, homes for sale, [neighborhood], [price point], [beds/baths], for sale, listing, tour

### Step 2 — Parse and Tokenize Transcript
1. Read the .SRT file, extract all text segments
2. Combine into full transcript text
3. Tokenize into words (lowercase, strip punctuation)
4. Calculate total word count and total duration

### Step 3 — Count Keyword Occurrences

For each target keyword (and multi-word phrases):
```markdown
| Keyword | Count | Density | First Mention | Mentions/Min |
|---------|-------|---------|---------------|--------------|
| temple tx | X | X.X% | 0:XX | X.X |
| [keyword] | X | X.X% | 0:XX | X.X |
```

### Step 4 — Analyze Distribution
Check WHERE keywords appear in the video timeline:
```
First 25% (hook + setup): X mentions
25-50% (body segment 1): X mentions
50-75% (body segment 2): X mentions
Last 25% (verdict + CTA): X mentions
```

Flag if keywords are front-loaded (good for SEO) or absent from early segments (bad).

### Step 5 — Gap Analysis
```markdown
## Missing Keywords
Keywords with 0 mentions that should appear:
- [keyword] — Why it matters: [context]
- [keyword] — Suggested insertion point: [timecode]

## Under-Represented Keywords
Keywords mentioned <3 times in a 10+ minute video:
- [keyword] (X mentions) — Target: X mentions

## Over-Represented Keywords
Keywords that may sound repetitive (>15 mentions):
- [keyword] (X mentions) — Consider synonyms: [alternatives]
```

### Step 6 — Entity Consistency Check
Verify these entities appear correctly:
- "Taylor Dasch" — at least 1 mention (entity declaration)
- "EG Realty" — at least 1 mention
- "Temple" or "Temple TX" or "Temple Texas" — at least 5 mentions in 10+ min video
- Neighborhood name — at least 3 mentions in a tour video
- "Fort Hood" (never "Fort Cavazos")

### Step 7 — Recommendations
```markdown
## Optimization Suggestions
1. Add "[keyword]" at [timecode] — currently a natural gap
2. Replace "[synonym]" with "[target keyword]" at [timecode]
3. Entity declaration missing — add "Taylor Dasch with EG Realty" before [timecode]
4. [Additional recommendations]
```

## Output Format
Save to `output/YYYY-WXX/keyword-audit/[video-slug]-keywords.md`

## Quality Checks
- [ ] All target keywords checked
- [ ] Distribution analysis covers full video timeline
- [ ] Entity consistency verified
- [ ] Gap analysis provides specific timecodes for insertions
- [ ] No recommendation to stuff keywords unnaturally
- [ ] Fort Hood check (never Fort Cavazos)
- [ ] "Buy-and-hold" not "turnkey" if investor content

## Brand Rules
- Keyword density is a diagnostic tool, not a stuffing guide
- Natural speech > keyword optimization
- Entity declaration (Taylor Dasch with EG Realty) should appear in first 60 seconds
- Temple TX must appear naturally — never forced
