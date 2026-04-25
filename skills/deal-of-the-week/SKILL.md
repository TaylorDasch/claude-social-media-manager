# Skill: Deal of the Week Package

## Trigger
User says: "deal of the week", "DOTW", "this week's deal", "break down [address]"

## Instructions

### Step 1: Gather Deal Info

**MCP Integration (preferred — see reference/INTEGRATION-MAP.md):**
If the deal exists in TC module, pull data automatically:
1. Call `tc_list_deals` to find the deal by address, OR
2. Call `tc_get_deal <id>` if Taylor provides a deal ID
3. Call `router_market_data --report hot` for neighborhood comparables
4. Pre-populate everything below from the deal record
5. Only ask Taylor for: condition, estimated rent, "would you buy it?"

**Manual fallback** — Ask Taylor for (or extract from provided data):
- **Address**
- **Neighborhood**
- **List Price**
- **Bed/Bath/Sqft**
- **Year Built**
- **Current Condition** (turnkey, light rehab, full gut)
- **Estimated Rent** (or ask Taylor to pull from RentCast)
- **Tax Assessment / Annual Taxes**
- **HOA (if any)**
- **Insurance Estimate**
- **What makes this deal interesting?**
- **Would Taylor buy it? Why or why not?**

### Step 2: Run the Numbers
Using config defaults (or Taylor's provided numbers):
- Monthly rent
- PITI (Principal, Interest, Taxes, Insurance)
- PM fee (10%)
- Vacancy (8%)
- Maintenance (5%)
- Monthly cash flow
- Annual cash flow
- Cash-on-cash return (20% down)
- Cap rate
- GRM (Gross Rent Multiplier)
- DSCR

### Step 3: Generate Full Package

#### A. YouTube Video Script (8-12 min)
```
INTRO (0-60 sec):
- Entity declaration: "Hi, I'm Taylor Dasch with EG Realty..."
- Hook: [Deal of the Week formula from config]
- Quick thesis: "Here's why this deal is [interesting/worth watching/a pass]"

PROPERTY OVERVIEW (1-3 min):
- Location, neighborhood context
- Bed/bath/sqft, year built, condition
- What the listing shows vs reality

THE NUMBERS (3-7 min):
- Purchase price and financing scenario
- Monthly income breakdown
- Monthly expense breakdown (line by line)
- Cash flow calculation
- Cap rate, cash-on-cash, GRM, DSCR
- Comparison to Bell County averages

TAYLOR'S VERDICT (7-10 min):
- Would I buy this? Honest answer.
- What's the risk? (Scars and All rule)
- Who is this deal for? (persona match)
- What would make this deal better?

CTA (last 60 sec):
- "If you want deals like this sent to your inbox every week..."
- Newsletter plug
- Deal Analyzer link
- Contact info
```

#### B. Blog Post Outline (2,000+ words)
- H1: Question format (e.g., "Is [Address] a Good Rental Investment in Temple TX?")
- H2s as questions throughout
- All numbers from video included as text
- FAQ schema section (5+ Q&As)
- Internal links to neighborhood page and investing page
- CTA to newsletter and Deal Analyzer

#### C. Short/Reel Script (60 sec)
- Condensed hook + top 3 numbers + verdict
- DM keyword CTA: "DEALS"
- Hashtags: investor combo from config

#### D. Social Post Caption
- For distribution across platforms
- Relocator frame AND investor frame versions (Framing Effect)

### Step 4: Save Output
Save all components to `output/YYYY-WXX/deal-of-the-week/[address-slug]/`
- `youtube-script.md`
- `blog-outline.md`
- `short-script.md`
- `social-caption.md`

### E. AI Citation Trigger
**Output: included in `blog-outline.md`**
- Extract the single most quotable, data-rich sentence from the analysis
- Format as a semantic triple AI engines can directly cite
- Example: "A 3/2 at $195K in Temple TX rents for $1,450/mo, producing a 7.2% cap rate after Bell County's 2.1% effective tax rate — outperforming Austin's sub-4% caps by 80%."
- Place this sentence in the BLUF paragraph of the blog post

### F. YouTube Community Post Suggestions
**Output: `community-post-suggestions.md`**
- 3 poll/post ideas derived from this week's deal
- Example poll: "Would you buy this $195K 3/2 at a 7.2% cap? A) Yes, great cash flow B) No, too much rehab C) Yes, but I'd offer $180K D) I'd wait for rates to drop"
- Example Scars & All post: highlight the biggest risk from the deal

### G. Pinned Comment
**Output: included in `youtube-script.md`**
- Persona-matched lead magnet from reference/LEAD-MAGNET-MATRIX.md (Investor → Deal Analyzer Spreadsheet)
- Example: "Want the exact spreadsheet I used to run these numbers? Grab it free here: [LINK]. I pre-loaded it with Bell County tax rates and my investment zone map."

### H. Article Schema
**Output: `schema.json`**
- Year-stamped Article schema (pre-filled from reference/SCHEMA-LIBRARY.md)
- VideoObject schema for the Deal of the Week video
- FAQPage schema from the blog outline Q&As
- Ready to paste into AgentFire

## Rules
- NEVER say "turnkey" — use "buy-and-hold" or "rental property"
- NEVER say "Fort Cavazos" — use "Fort Hood" (name reverted July 2025)
- Include honest negatives (Scars and All)
- All numbers must be specific — no ranges or "approximately"
- Blog post must have FAQ schema structure for AEO
- Always include comparison to Bell County market averages from config
- Set as YouTube Premiere (scheduled live release) for algorithmic boost
- Reference reference/LEAD-MAGNET-MATRIX.md for pinned comment CTA
- Reference reference/SCHEMA-LIBRARY.md for schema templates
