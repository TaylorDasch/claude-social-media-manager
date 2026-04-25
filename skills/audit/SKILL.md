# Skill: AEO Page Audit

## Trigger
User says: "audit", "score this page", "AEO check", "how optimized is this"

## Instructions

### Step 1: Identify Input
Accept one of:
- **Page URL** from templetxhomes.net — fetch and analyze the live page
- **Pasted HTML** — analyze the raw markup directly
- **Blog post draft** — analyze the draft content

If a URL is provided, fetch the page content. If HTML is pasted, use it directly.

### Step 2: Load References
- Load `research/AEO-DIRECTIVES.md` for entity consistency rules and AEO scoring criteria
- Load `VIDEO-TO-PAGE-MAP.md` to check if the correct video is embedded
- Load `reference/SCHEMA-LIBRARY.md` for exact schema templates to recommend
- Load `reference/LEAD-MAGNET-MATRIX.md` for persona-matched CTA recommendations
- Load banned word list: "turnkey", "dream home", "white glove", "nestled", "charming", "Fort Cavazos"

### Step 2.5: Pull Live Ranking Data (GSC + Playwright)

#### Google Search Console
- Call `query_search_analytics` with the page URL to get: impressions, clicks, CTR, avg position for the last 28 days
- Call `find_keyword_opportunities` for the page's target keywords
- Use this real data to inform scoring in categories 3 (Heading Hierarchy — are H2s matching actual search queries?), 7 (Internal Linking — is the page getting impressions?), and 8 (Freshness — is traffic trending up or down?)

#### Playwright (Competitor Comparison)
- Call `browser_navigate` to the top-ranking competitor for the page's primary keyword
- Call `browser_snapshot` to capture the competitor's page structure
- Compare: does competitor have video? FAQ schema? More internal links? Better heading structure?
- Include a "## Competitor Comparison" section in the audit output

### Step 3: Score the Page

Score across 10 categories (10 points each = 100 total):

1. **Entity Declaration (0-10)** — Is Taylor Dasch explicitly named with credentials ($27M+, 100+ transactions, EG Realty)? Is the entity consistent with other platforms (name, title, location, specialties)?
2. **BLUF / Answer-First Structure (0-10)** — Does the page answer the core question in the first 50 words? Would an AI engine extract a useful answer from paragraph 1?
3. **Heading Hierarchy (0-10)** — Are H2s phrased as questions matching search queries? Proper H2/H3 nesting? No skipped heading levels?
4. **Data Density (0-10)** — Specific numbers present (prices, rates, dates, percentages)? No "approximately" or rounded estimates? At least 5 concrete data points?
5. **Schema Markup (0-10)** — VideoObject present (if video embedded)? FAQPage present? Article/Person schema? Valid JSON-LD? Score 0 if no schema at all.
6. **Video Embed (0-10)** — Is a relevant YouTube video embedded? Does it match the mapping in VIDEO-TO-PAGE-MAP.md? Score 0 if no video, partial credit if video exists but wrong match.
7. **Internal Linking (0-10)** — Links to other templetxhomes.net pages? Hub-and-spoke structure? No orphan page? At least 3 internal links?
8. **Freshness (0-10)** — dateModified within 60 days? Data points current (not from previous year)? Year-stamped where needed?
9. **Scars & All / Information Gain (0-10)** — Does the page include honest negatives? Proprietary analysis not found elsewhere? Unique data or perspective that competitors lack?
10. **Lead Capture (0-10)** — Persona-matched CTA present (Military/Medical/Investor)? Lead magnet linked? Form with hidden attribution fields?

### Step 4: Generate the Scorecard

```
PAGE: [URL or title]
SCORE: [X]/100 — GRADE: [A/B/C/D/F]

BREAKDOWN:
1. Entity Declaration:     [X]/10 — [brief note]
2. BLUF Structure:         [X]/10 — [brief note]
3. Heading Hierarchy:      [X]/10 — [brief note]
4. Data Density:           [X]/10 — [brief note]
5. Schema Markup:          [X]/10 — [brief note]
6. Video Embed:            [X]/10 — [brief note]
7. Internal Linking:       [X]/10 — [brief note]
8. Freshness:              [X]/10 — [brief note]
9. Information Gain:       [X]/10 — [brief note]
10. Lead Capture:          [X]/10 — [brief note]

TOP 3 IMPROVEMENTS (highest point gain):
1. [Action] — would add [X] points
2. [Action] — would add [X] points
3. [Action] — would add [X] points

SPECIFIC CONTENT TO ADD:
[Exact text, schema, or elements needed to fill gaps]
```

### Grading Scale
- **90-100: A** — AEO-dominant, citation-ready
- **80-89: B** — Strong, minor gaps
- **70-79: C** — Decent but missing key signals
- **60-69: D** — Significant gaps, needs work
- **Below 60: F** — Not AEO-ready

### Step 5: Save Output
Save to `output/audits/[page-slug]-audit-YYYY-MM-DD.md`

## Rules
- Be specific about what is missing — do not just say "add schema," provide the exact template from reference/SCHEMA-LIBRARY.md
- Reference reference/LEAD-MAGNET-MATRIX.md for CTA recommendations matched to the page's target persona
- Reference VIDEO-TO-PAGE-MAP.md for video embed recommendations
- Flag any banned words found ("turnkey", "dream home", "white glove", "nestled", "charming", "Fort Cavazos")
- Flag any "approximately" or rounded numbers — recommend replacing with exact MLS/CAD data
- SPECIFIC CONTENT TO ADD must include copy-paste-ready text, schema blocks, or HTML elements
- If scoring a draft (not yet published), note which freshness/schema items are pre-publication and score accordingly

## Dependencies
- GSC MCP tools: `query_search_analytics`, `find_keyword_opportunities`
- Playwright MCP tools: `browser_navigate`, `browser_snapshot`
