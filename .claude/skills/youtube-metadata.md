# YouTube Metadata Generator

## Trigger
"youtube metadata", "yt metadata", "video metadata", "title options", "youtube tags"

## Required Inputs
- Video topic OR transcript/script
- Target content pillar (Neighborhood Tour, Market Data, Investor Education, Relocation Guide, or Listing Showcase)
- Target persona (Military PCS, BSW Medical, Investor, Austin Refugee, General Relocator)
- Video length estimate (Long-form or Short)

## Step-by-Step Execution

### Step 1 — Research
1. Read `reference/YOUTUBE-GROWTH-PLAYBOOK.md` for title formulas and algorithm rules
2. Read `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt` to avoid title duplication
3. Run dedupe check against existing titles — flag any >70% word overlap
4. Read `reference/LEAD-MAGNET-MATRIX.md` for persona-matched CTA

### Step 2 — Generate 3 Title Options
Each title must follow these rules:
- Include "Temple TX" or "Temple Texas" (searchability)
- Under 60 characters (mobile truncation)
- Lead with the hook, not the location
- Never repeat the thumbnail text
- Use proven formulas from YOUTUBE-GROWTH-PLAYBOOK.md:
  - **Number Bomb:** "5 Neighborhoods Under $250K in Temple TX"
  - **Comparison:** "Temple vs Killeen — Which Is Better for Investors?"
  - **Negative Hook:** "Don't Buy in Temple TX Until You Watch This"
  - **Specific Price:** "$180K Homes in Temple TX — Full Tour"
  - **Question:** "Is Temple TX Still Worth It in 2026?"

Format:
```
TITLE A (primary recommendation): [title]
TITLE B (alternative angle): [title]
TITLE C (curiosity play): [title]
```

### Step 3 — Generate Description (7 Sections)

```markdown
[SECTION 1 — DIRECT ANSWER (first 2 lines, shown in search)]
Answer the video's core question in 1-2 sentences. Include "Temple TX" and primary keyword.

[SECTION 2 — ENTITY DECLARATION (lines 3-5)]
Taylor Dasch with EG Realty — Temple TX's #1 relocation specialist.
$27M+ in volume | 100+ transactions | 3-Year BiggerPockets Featured Agent
📞 254-718-4249 | 🌐 templetxhomes.net

[SECTION 3 — CHAPTERS (as questions)]
0:00 — [Hook question]
1:15 — [Topic question]
3:30 — [Data question]
... (match actual timestamps when available, use estimates if scripting)

[SECTION 4 — AREAS/NEIGHBORHOODS MENTIONED]
🏠 Neighborhoods in this video:
• [Name] — [1-line description + price range]
(Link to page if exists on templetxhomes.net)

[SECTION 5 — KEY DATA POINTS]
📊 Numbers from this video:
• Median home price: $XXX,XXX
• [Other relevant stats]

[SECTION 6 — ABOUT TAYLOR]
I'm Taylor Dasch with EG Realty — I help military families, BSW physicians, investors, and relocators buy smart in Temple, TX.

Whether you're PCSing to Fort Hood, starting at Baylor Scott & White, or building a buy-and-hold portfolio, I've got the data and the deals.

[SECTION 7 — CONTACT + KEYWORDS]
📞 Call/Text: 254-718-4249
📧 dealswithdasch@gmail.com
🌐 https://templetxhomes.net
📅 Book a call: [Calendly link]

#TempleTexas #TempleRealEstate #[pillar tag] #[persona tag] #[neighborhood tag]
```

### Step 4 — Generate Tags (30 max)
- First 5: exact-match high-volume (e.g., "temple tx homes for sale")
- Next 10: long-tail (e.g., "best neighborhoods in temple texas 2026")
- Next 10: persona-specific (e.g., "fort hood pcs housing", "bsw physician relocation")
- Last 5: brand (e.g., "taylor dasch", "eg realty", "templetxhomes")

### Step 5 — Generate Pinned Comment
```
📌 FREE [Lead Magnet Name] — [1-line description]
→ DM me "[KEYWORD]" or call 254-718-4249

Timestamps:
0:00 [chapter]
...

What questions do you have about [topic]? Drop them below 👇
```

### Step 6 — Card Placement Suggestions
- Card 1 at 25% mark: related video or playlist
- Card 2 at 50% mark: lead magnet or website link
- Card 3 at 75% mark: related neighborhood tour
- End screen: subscribe + best related video

## Output Format
Single markdown file with all sections clearly labeled. Save to `output/YYYY-WXX/youtube/[slug]-metadata.md`

## Quality Checks
- [ ] All 3 titles under 60 characters
- [ ] No title duplicates existing catalog entries (>70% overlap)
- [ ] Description entity block appears in lines 3-5
- [ ] "Temple TX" or "Temple Texas" in at least 2 of 3 titles
- [ ] Tags ≤ 30 total, ≤ 500 characters combined
- [ ] Pinned comment includes lead magnet + phone number
- [ ] No banned words (governance/QUALITY-GATES.md Gate 1)
- [ ] Chapter markers formatted as questions where possible
- [ ] Fort Hood (never Fort Cavazos)
- [ ] Buy-and-hold (never turnkey)

## Brand Rules
- Entity declaration exact: "Taylor Dasch with EG Realty"
- Phone: 254-718-4249
- Website: templetxhomes.net
- Email: dealswithdasch@gmail.com
- Never salesy, never FOMO, never generic agent language
