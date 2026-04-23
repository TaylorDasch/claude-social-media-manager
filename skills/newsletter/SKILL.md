# Skill: Newsletter (`/newsletter`)

## Trigger
User says: "newsletter", "temple insider", "investor brief", "write the brief", "next issue", "newsletter draft"

## Overview
Two biweekly newsletters on Beehiiv. **Never mix audiences.** Buyer content stays in Temple Insider. Investor content stays in Investor Brief.

| Newsletter | Audience | Cadence | Template |
|-----------|----------|---------|----------|
| **The Temple Insider** | Buyers, relocators, military families, BSW medical staff | Every other Tuesday | `templates/temple-insider-template.md` |
| **The Temple TX Investor Brief** | Investors evaluating deals or strategies | Every other Thursday | (inline below) |

## Routing

When Taylor says "newsletter" or "next issue," ask: **"Insider or Brief?"** If the topic makes it obvious (e.g., "cap rate analysis" = Brief, "neighborhood spotlight" = Insider), skip the question and route directly.

---

# PART 1: THE TEMPLE INSIDER

## Instructions

### Step 1: Gather Inputs
Ask Taylor for (or suggest based on recent market activity):
- **Home of the Week**: Which property? Need address, list price, bed/bath/sqft, neighborhood, ISD, DOM, and Taylor's honest read on it. Taylor selects this -- he knows what's worth featuring.
- **3 More Worth a Look**: Three additional listings with honest one-liners. Mix price points.
- **Rotating Feature direction**: Does Taylor have a specific comparison, trap, or strategy to cover? If not, Claude picks from current market conditions.
- **Any market data to highlight**: Fresh MLS pulls, rate changes, inventory shifts.

### Step 2: Check Previous Issue Performance (Beehiiv MCP)
Before writing, pull performance data from the last issue:
1. Call `list_posts` to find the previous Temple Insider issue
2. Call `newsletter_stats` to pull open rate, click rate, top-clicked link
3. Report to Taylor: previous issue performance + current subscriber count
4. Use insights to inform this issue: if open rate was low, suggest a stronger subject line; if a section got clicks, lean into that format again
5. Call `list_subscribers` to get subscriber count and recent growth

### Step 3: Pull Market Data
Before writing, check these sources for fresh data points:
- `real-estate-command-center/market_monitor.py` -- DOM trends, price reductions, inventory shifts
- `real-estate-command-center/market_brain.py` -- comps, neighborhood analytics, anomalies
- `reference/TEMPLE-TX-DATA-VAULT.md` -- verified recurring data points

Use real outputs from these sources. If scripts have not been run recently, flag it to Taylor and use the most recent data available. Never estimate or fabricate data points.

### Step 4: Write the Issue

Output a complete, Beehiiv-ready newsletter draft in this exact structure:

```
# The Temple Insider -- Issue #[N]
**[Date] | Taylor Dasch | EG Realty**

---

**Subject Line:** [under 50 characters]
**Preview Text:** [80-100 characters, teases the rotating feature -- never repeats the subject line]

---

## THE REAL NUMBER

# [The number, big and bold]

[One sentence: what this number is.]

[2-3 sentences: why it matters to buyers specifically. Context. Compare to last month, last year, or national average.]

[1 sentence: what to do with this information. Practical and direct.]

~150-200 words. Open casual. The number comes first. Always. Include the honest angle. No hedging.

---

## [ROTATING FEATURE TITLE]
Pick the format that fits this issue's content. Do NOT force a rigid rotation.

### Option A: Honest Comparison
Two neighborhoods, two price points, or two strategies compared head-to-head. Real pros AND cons for both. Use MLS data: SP/LP ratios, DOM, price per sqft. No winner declared unless the data is obvious.

### Option B: Trap Alert
Something that looks good but is not. A specific gotcha in this market. Name neighborhoods, price bands, builder issues. Be specific to Temple.

### Option C: Insider Move
A strategy working right now based on current conditions. Specific, actionable. "Here's exactly what I'm telling my buyers to do this week." Include numbered steps.

~200-300 words. This is the meat. Go deep on one thing. Use real numbers.

---

## HOME OF THE WEEK

[PHOTO SLOT: Property exterior -- full width hero image]
Recommended size: 600x400

**[Address] -- $[Price]**
[Beds]/[Baths], [SqFt] sqft | [Neighborhood] | [School District] | [DOM] days on market

[2-3 sentences: why this one stood out. What makes it worth your time. Be specific.]

**The Good:**
- [3 key features -- layout, location, finishes, lot, price per sqft vs neighborhood average]

**The Honest Truth:**
- [1-2 real negatives. Busy street, small yard, dated kitchen, low bedroom count, builder issues. Never skip this.]

**Taylor's Take:** [1-2 sentences. First person. Honest verdict. Who is this perfect for? Would you buy it?]

**Monthly Payment Estimate:** ~$[amount]/mo (assuming [X]% down, [X]% rate, taxes + insurance included)

[BUTTON: Schedule a Showing -- dealswithdasch@gmail.com]

~200-250 words. This is NOT a listing ad. It is Taylor's honest opinion. Always include the monthly payment -- that is what buyers actually care about. Always include at least one negative.

Rotate the HOTW buyer type each issue:
- First-time buyer (under $250K)
- Step-up buyer ($250K-$350K)
- Higher end ($350K-$500K)
- Luxury ($500K+)

---

## 3 MORE WORTH A LOOK

**[Address] -- $[Price]**
[Beds]/[Baths], [SqFt] sqft | [Neighborhood] | [DOM] days on market
Taylor's take: [One honest sentence. Include a negative if there is one.]

**[Address] -- $[Price]**
[Beds]/[Baths], [SqFt] sqft | [Neighborhood] | [DOM] days on market
Taylor's take: [One honest sentence. Include a negative if there is one.]

**[Address] -- $[Price]**
[Beds]/[Baths], [SqFt] sqft | [Neighborhood] | [DOM] days on market
Taylor's take: [One honest sentence. Include a negative if there is one.]

~100-150 words total. Mix price points. At least one under $250K if possible. These are NOT "featured listings." They are picks Taylor actually thinks are worth a look. The honest take is mandatory.

---

## MARKET PULSE

3-5 bullet points of local market data that matters to buyers. One sentence each with one specific number.

Required metrics (pick 3-5 each issue, rotate):
- Median days on market (current + trend direction)
- Active inventory count or months of supply
- SP/LP ratio (overall or by price band)
- Median sale price (current + YoY change)
- Price reductions (% of active listings with a cut)
- New construction permits or starts
- Mortgage rate snapshot (current + monthly change)
- Absorption rate by price band

Format:
- **[Metric]:** [Number]. [One sentence of what it means for buyers.]

End with one "so what" sentence that ties the data together into a buyer takeaway.

---

## NEIGHBORHOOD SPOTLIGHT: [Neighborhood Name]

[2-3 sentences: what this neighborhood is and who it is for.]

**The Numbers:**
| Metric | Value |
|--------|-------|
| Median Price | $XXX,XXX |
| Avg DOM | XX days |
| Price/Sqft | $XXX |
| School District | [ISD] |

[One data point that surprises. Frame it as a comparison: "Canyon Creek homes appreciated 8.2% last year -- 2x the Temple average." or "Legacy Ranch has the lowest DOM in Temple at 11 days. The next closest neighborhood is 23."]

[1 sentence: the honest thing nobody tells you about this neighborhood.]

[BUTTON: Read the full [Neighborhood] breakdown -- link to templetxhomes.net page]

Rotate through the neighborhood queue (see bottom of this file). Link to the page every time.

---

## TAYLOR'S CORNER

[3-5 sentences. First person. One observation about the market right now.]

This is where Taylor's analyst voice shines. Not salesy. Insightful. Could be:
- A hot take ("I think prices in [area] have another 5% to drop before they stabilize. Here's why.")
- A contrarian view ("Everyone is waiting for rates to drop. I think that is the wrong play right now.")
- A heads-up about something coming ("Watch the south side of Temple. Three projects just broke ground within a mile of each other.")
- A pattern he is seeing ("I've shown 8 houses this month. Every single buyer asked about the same thing: monthly payment, not list price. The market has shifted from price shopping to payment shopping.")

Rules: Lead with the insight, not a preamble. One paragraph. No filler.

---

## QUICK LINKS

- [Latest YouTube video title + link]
- [New page on templetxhomes.net + link]
- [Upcoming open house or event, if any]
- [Link to schedule a call or showing]

2-4 links. Only include items that actually exist. Do not pad with placeholder links.

---

That's it for this one. Hit reply if you want me to pull comps on anything specific. I read every email.

-- Taylor

Taylor Dasch | EG Realty
254-718-4249 | dealswithdasch@gmail.com
templetxhomes.net
```

### Step 5: Generate Subject Line Options
Provide 3 subject line options using different formulas:
1. **[Number] + What It Means** -- Lead with the hardest data point from The Real Number
2. **The Surprise** -- The counterintuitive stat from the issue
3. **The Question** -- A question the reader is already asking themselves

All subject lines under 50 characters. Also provide preview text (80-100 characters) for each option. The preview text teases the rotating feature, not The Real Number. Let Taylor pick.

### Step 6: The Creative Element
Every issue gets ONE creative or unexpected element. This is non-negotiable. Examples:
- A "what would happen if..." scenario using real data
- A comparison nobody has made before (e.g., "Your monthly payment on a Temple home buys you a parking spot in Austin")
- A mini data visualization described in text (e.g., a price-per-sqft ladder by neighborhood)
- An honest confession about the market

Tell Taylor what the creative element is and why you chose it.

### Step 7: Assign Issue Number and Save
Check `output/` for previous Temple Insider issues. Increment the issue number. File naming: `temple-insider-[NNN].md` (zero-padded to 3 digits). Save to `output/YYYY-WXX/newsletter/temple-insider-[NNN].md`.

## Temple Insider Content Rules

### Voice
- Casual (2/10 formal). Data-first. Honest. Short sentences. Contractions always.
- Taylor speaks like a smart friend who happens to be a real estate expert, not like a marketing email.
- Lead with the number, then explain why it matters.
- "Here's the deal..." / "So here's something wild." / "Let me hit you with a number."
- First person where Taylor is giving his take. Third person for market data.

### Banned Language
See `governance/QUALITY-GATES.md` Gate 1. Additionally for the Insider:
- No "dream home," "white glove," "nestled," "charming," "stunning," "sought-after," "boasts," "vibrant," "hidden gem"
- No em dashes
- No "whether you're a..." constructions
- No "in today's market" -- name the month/year
- No "amenities" -- name the actual things
- No "Fort Cavazos" -- use "Fort Hood" (name reverted July 2025)

### Data Rules
- Real MLS data only. Never estimate. Never fabricate.
- If data is unavailable, mark it `[DATA NEEDED -- Taylor to provide]` and continue.
- Always include at least one comparison (YoY, neighborhood vs neighborhood, price band vs price band).
- Monthly payment estimates must show assumptions (down payment %, rate, inclusion of taxes/insurance).

### Listing Rules
- Taylor selects the Home of the Week. He knows what is worth featuring.
- Always include at least one negative in "The Honest Truth." No exceptions.
- "3 More Worth a Look" must include honest takes with negatives where they exist.
- Mix price points across all 4 listings. Do not put four homes in the same range.
- No IDX widgets or search embeds.

### Platform Rules
- Beehiiv is the publishing platform. Format in clean markdown that translates to Beehiiv's editor.
- The output should be ready to paste directly into Beehiiv. No intermediate formatting steps needed.
- Subject line must follow one of the 5 formulas in `social-media-config.json`.
- Biweekly cadence: every other Tuesday.

### Success Metric
Success is NOT open rate. It is: "Did this issue lead to a conversation that turned into a showing or a deal?" One reply from a serious buyer beats 50% open rate on passive readers.

## Neighborhood Rotation Queue
Cycle through these (add new ones as pages are built):
1. Prairie Ridge (used in Issue #1)
2. Canyon Creek
3. Lake Pointe
4. Bella Terra
5. Legacy Ranch
6. Alta Vista
7. Windmill Farms
8. South Pointe
9. Gardens at Pendleton
10. Mesa Ridge

## Feature Rotation
Pick whichever fits best for the issue. No rigid cycle:
- **Honest Comparison** -- when there is a clear head-to-head to break down
- **Trap Alert** -- when there is a specific gotcha worth flagging
- **Insider Move** -- when current market conditions create a specific buyer strategy
Default to Insider Move or Trap Alert if no natural comparison exists.

---

# PART 2: THE TEMPLE TX INVESTOR BRIEF

## Instructions

### Step 1: Gather Inputs
Ask Taylor for (or suggest based on recent market activity):
- **Deep Dive topic**: What investor-focused analysis should we cover? (cap rates, DSCR, MTR strategy, equity analysis, rent growth, insurance/tax trends, financing environment, specific strategy breakdown)
- **Deal Autopsy property**: Which property are we dissecting? Need address, list price, bed/bath/sqft, condition, and Taylor's read on it.
- **Signal items**: Any market signals worth flagging?

### Step 2: Check Previous Issue Performance (Beehiiv MCP)
Before writing, pull performance data from the last issue:
1. Call `list_posts` to find the previous Investor Brief issue
2. Call `newsletter_stats` to pull performance data
3. Report to Taylor: previous issue open rate, click rate, top-clicked link
4. Use insights to inform this issue
5. Call `list_subscribers` to get current subscriber count and recent growth

### Step 3: Pull Signal Data
Before writing, check these command center scripts for fresh data points:
- `real-estate-command-center/market_monitor.py` -- DOM trends, price reductions, inventory shifts
- `real-estate-command-center/expired_sellers.py` -- expired/withdrawn listings, motivated seller signals
- `real-estate-command-center/market_brain.py` -- comps, neighborhood analytics, anomalies

Use real outputs from these scripts. If scripts have not been run recently, flag it to Taylor and use the most recent data available. Never estimate or fabricate data points.

### Step 4: Write the Issue

```
# The Temple TX Investor Brief -- Issue #[N]
**[Date] | Taylor Dasch | EG Realty**

---

**Subject Line:** [under 50 characters]
**Preview Text:** [80-100 characters]

---

## THE BRIEFING

[~100 words. Market snapshot for investors. One key stat, one trend, one "so what" for deal-making. Open with the hardest number you have. Close with what it means tactically.]

---

## NUMBERS THIS WEEK

3-5 key investor metrics in a scannable table:

| Metric | Value | Trend |
|--------|------:|-------|
| Median DOM | XX days | [up/down/flat] vs last month |
| Price Reductions | XX% of active | [context] |
| Avg Cap Rate (SFR) | X.X% | [price band or area] |
| DSCR Threshold | X.XX | at current rates |
| Inventory (months) | X.X | [buyer/seller/balanced] |

Pick the 3-5 metrics most relevant to this issue's Deep Dive. Include trend direction and brief context for each.

---

## THE DEEP DIVE: [Specific Analytical Headline]

[~500 words. One investor-focused analysis topic.]

Structure:
1. Open with the thesis -- a specific claim backed by a number
2. Build the case with 2-4 data points (MLS, tax records, rental comps, insurance quotes, loan scenarios)
3. Address the obvious objection ("but what about...")
4. Show the math -- use tables when the numbers are complex
5. Close with the actionable takeaway: what should an investor DO with this information?

---

## THE DEAL AUTOPSY: [Address]

**List Price:** $XXX,XXX
**Bed/Bath:** X/X | **Sqft:** X,XXX | **Built:** XXXX
**Condition:** [Honest assessment]
**Location:** [Distance to key demand drivers -- BSW, Fort Hood, industrial corridor]
**HOA:** [Yes/No + amount] | **Listing Agent:** [Name, Brokerage]

### The Numbers -- [Primary Strategy] Strategy

| Line Item | Amount |
|-----------|-------:|
| Purchase Price | $XX,XXX |
| Rehab ([quality level]) | $XX,XXX |
| Furnishing (if MTR) | $X,XXX |
| **All-In Basis** | **$XXX,XXX** |
| Down Payment (XX%) | $XX,XXX |
| Loan Amount | $XXX,XXX |
| **Total Cash In** | **$XX,XXX** |

| Income & Expenses | Monthly | Annual |
|-------------------|--------:|-------:|
| Gross Rent | $X,XXX | $XX,XXX |
| P&I | -$XXX | -$X,XXX |
| Property Tax | -$XXX | -$X,XXX |
| Insurance | -$XXX | -$X,XXX |
| Vacancy (X%) | -$XXX | -$X,XXX |
| Utilities (if MTR) | -$XXX | -$X,XXX |
| Maintenance + CapEx (X%) | -$XXX | -$X,XXX |
| **Monthly Cash Flow** | **$XXX** | **$X,XXX** |

| Metric | Value |
|--------|------:|
| **Cap Rate** | X.X% |
| **Cash-on-Cash Return** | X.X% |
| **DSCR** | X.XX |
| **1% Rule** | X.XX% |

### For Comparison -- MTR vs LTR (include when applicable)

| Metric | LTR | MTR | Difference |
|--------|----:|----:|----------:|
| Monthly Rent | $X,XXX | $X,XXX | +$XXX |
| Monthly Cash Flow | $XXX | $XXX | +$XXX |
| Cap Rate | X.X% | X.X% | +X.X% |
| DSCR | X.XX | X.XX | +X.XX |

### THE GOOD
- [3-5 bullets. Specific, data-backed reasons this deal works.]

### THE UGLY (Scars and All)
- [3-5 bullets. Real negatives. Foundation risk, floor plan limitations, appreciation constraints, management burden, plumbing age, neighborhood trajectory. Never skip. Never soften.]

### TAYLOR'S VERDICT: [Buy / Conditional Buy / Pass]

[~150 words. First-person. Start with "Here's the deal on [address]." State verdict clearly, then explain conditions. What would need to be true? What is the specific risk that could kill it? Who is this deal actually for?]

---

## THE SIGNAL

- [3-5 bullets. Market intelligence items. Each bullet is one sentence with one specific data point.]
- Sources: DOM on the autopsy listing, expired/withdrawn inventory, recent sold comps, rate movements, local development news, permit activity, employer announcements
- Pull from command center scripts when available

---

## ONE QUESTION

[2-3 sentences. Ask ONE specific, answerable question that ties to this issue's content. Purpose: drive reply-based engagement for deliverability + build real relationships.]

**[The question itself -- bolded, standalone line.]**

Reply and tell me [what you will do with their answer -- specific promise for next issue].

---

Taylor Dasch | EG Realty | 254-718-4249 | dealswithdasch@gmail.com
templetxhomes.net

*You're receiving this because you're an investor who wants real numbers on Temple TX deals, not marketing fluff. If that's not you, unsubscribe below -- no hard feelings.*
```

### Step 5: Generate Subject Line Options
Provide 3 subject line options:
1. **[Data Point] + What It Means** -- Lead with the hardest number from the issue
2. **The Number That Surprises** -- The counterintuitive stat from Deep Dive or Deal Autopsy
3. **The Honest Contrary Take** -- The insight that goes against conventional wisdom

Also provide preview text (80-100 characters) for each option. Let Taylor pick.

### Step 6: Assign Issue Number and Save
Check `output/` for previous issues. Increment the issue number. File naming: `temple-tx-investor-brief-[NNN].md` (zero-padded to 3 digits). Save to `output/YYYY-WXX/newsletter/temple-tx-investor-brief-[NNN].md`.

## Investor Brief Content Rules

### Voice
- Analytical, data-driven, honest. Taylor speaks like an investor-analyst who happens to be an agent.
- Lead with the number, then explain why it matters.
- Short punchy sentences. No filler.
- First person where Taylor is giving his take. Third person for market data.
- "Here's the deal..." / "Let me break it down..." / "The math works like this..."

### Content Rules
- **INVESTOR ONLY.** No relocation content. No "great schools." No lifestyle sections.
- **Scars and All.** The Deal Autopsy UGLY section is mandatory with real negatives. Never skip, never soften.
- **MTR vs LTR comparison** whenever the property could plausibly run either strategy.
- **Real data only.** MLS comps, CAD values, actual insurance quotes, real rental comps. Flag any estimate explicitly: "Estimated -- verify before underwriting."
- **Never say "turnkey."** Use "buy-and-hold" or "buy-and-hold investors."
- **Fort Hood** -- not "Fort Cavazos" (name reverted July 2025).

### Success Metric
Success is NOT open rate. It is: "Did this issue lead to a conversation that turned into a deal?" One reply from a serious investor beats 50% open rate on passive readers.

---

# SHARED RULES (BOTH NEWSLETTERS)

## Checklist Before Delivery
- [ ] Subject line under 50 characters
- [ ] Preview text 80-100 characters, does not repeat subject line
- [ ] All numbers sourced from real data (no estimates without explicit flags)
- [ ] No banned language (Gate 1 from QUALITY-GATES.md)
- [ ] Entity info correct: Taylor Dasch, EG Realty, 254-718-4249
- [ ] At least one honest negative in every listing/deal section
- [ ] One creative/unexpected element included (Insider only)
- [ ] Links to templetxhomes.net where applicable
- [ ] Voice check: would Taylor actually say this out loud?
- [ ] No content crossover (buyer content in Insider only, investor content in Brief only)
- [ ] Issue number incremented correctly
- [ ] Output is complete markdown ready to paste into Beehiiv

## Dependencies
- Beehiiv MCP tools: `list_posts`, `newsletter_stats`, `list_subscribers`
- Command center scripts for market data
- `social-media-config.json` for subject line formulas and brand info
- `reference/TEMPLE-TX-DATA-VAULT.md` for verified data points
- `governance/QUALITY-GATES.md` for banned language and quality checks
- Saves to `output/YYYY-WXX/newsletter/`
