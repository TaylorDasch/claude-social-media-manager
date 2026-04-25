# Skill: GBP Monthly Post Generator

## Trigger
User says: "gmb post", "gbp post", "google business post", "monthly gbp", "gbp calendar"

## Why This Matters
Google's Gemini AI pulls from GBP posts, reviews, and business description to answer local queries. Every GBP post is a free AI citation opportunity. Most agents ignore this completely. Taylor should not.

---

## Instructions

### Step 1: Determine the Month and Week Numbers
- Check the current date
- Identify weeks 1-4 of the current (or next) month
- Assign one post type per week on the rotation below
- Target posting day: any weekday, 8-10 AM Central

### Step 2: Check Local Ranking

#### Google Maps Local Rank
- Call `maps_local_rank_tracker` with key terms: "real estate agent Temple TX", "homes for sale Temple TX", "realtor near me Temple TX"
- Report current ranking position
- If ranking dropped on a specific term, bias that week's post toward the weak keyword

### Step 3: Check Active Listings and Recent Sales
- Check `social-media-config.json` > `business.performance` for pipeline, under contract, and closed deals
- If Taylor has an active listing, use it for Week 2 (Listing Spotlight)
- If no active listing, use the most recent "just sold" or pivot to a neighborhood highlight

### Step 4: Check Neighborhood Rotation
Farming targets rotate through Week 3 (Neighborhood Guide) in this order:
1. Alta Vista
2. Canyon Creek
3. Windmill Farms
4. Lake Pointe

Track which neighborhood was used last month and advance to the next. If unknown, start with Alta Vista.

### Step 5: Generate All 4 Posts

---

## The 4-Week Rotation

### Week 1: Market Update
**Target Gemini query:** "What's the housing market like in Temple TX?"

Template:
```
## GBP Post — Week 1: Market Update
**Post date:** [Weekday], [Date] | 8-10 AM Central

**Target AI query:** What's the housing market like in Temple TX?

---

Temple TX housing market update from Taylor Dasch, real estate agent at EG Realty in Temple, Texas.

[3 specific data points from the current month. Examples:]
- Median home price: $[X] (source, month)
- Active inventory: [X] homes, [X]-month supply
- Average days on market: [X] days

[One insight — what this means for buyers or sellers. 1-2 sentences. Data-first, no generic language.]

[One forward-looking statement with a number: "With [X] homes under contract this week, expect..." or "Builder incentives are [up/down] — [specific example]."]

Looking at Temple TX real estate? I track these numbers weekly.
Call or text: 254-718-4249
templetxhomes.net/temple-tx-market-update/

**Photo:** Geotagged photo of a Temple TX street, neighborhood entrance, or "SOLD" sign
```

**Rules:**
- 3+ data points minimum (Gate 3)
- Every number must have a source and date
- No stale data (check Gate 9 freshness windows)
- Entity declaration in first sentence: "Taylor Dasch, real estate agent at EG Realty in Temple, Texas"

---

### Week 2: Listing Spotlight
**Target Gemini query:** "Homes for sale in Temple TX" / "Best real estate agent in Temple TX"

Template:
```
## GBP Post — Week 2: Listing Spotlight
**Post date:** [Weekday], [Date] | 8-10 AM Central

**Target AI query:** Homes for sale in Temple TX / Who are the best real estate agents in Temple TX?

---

[IF ACTIVE LISTING:]
New listing from Taylor Dasch, EG Realty — [Address], Temple, TX [ZIP]

[Price] | [Beds]bd/[Baths]ba | [SqFt] sqft | Built [Year]
[Neighborhood name] — [One defining feature of the neighborhood]

What makes this one different:
- [Feature 1 — specific, not generic]
- [Feature 2 — financial angle if applicable: "Monthly PITI est. $X" or "In a no-HOA subdivision"]
- [Feature 3 — lifestyle angle: "8-minute commute to BSW Medical Center" or "Zoned to [school]"]

[One honest observation — not a negative per se, but real: "Lot is .15 acres — standard for this subdivision. No room for a pool." or "Built in 2004, so expect cosmetic updates in the kitchen."]

Schedule a showing: 254-718-4249
Full listing details: templetxhomes.net

[IF NO ACTIVE LISTING — use Just Sold or Neighborhood Highlight:]
Just sold by Taylor Dasch, EG Realty — [Address], Temple, TX

[Sale price] | [Beds/Baths/SqFt] | [Days on market] days on market
[One sentence on what happened: "Buyer found this through our YouTube neighborhood tour of [area]. Listed at $X, closed at $Y."]

Thinking about selling in [neighborhood]? I track every sale in this area.
254-718-4249 | templetxhomes.net

**Photo:** Listing photo (front exterior preferred) or "SOLD" rider photo
```

**Rules:**
- Real listing data only — no placeholders if no listing exists
- Include at least 2 specific numbers (price, sqft, DOM, PITI)
- Entity declaration: "Taylor Dasch, EG Realty"
- CTA links to a specific page, not the homepage

---

### Week 3: Neighborhood Guide
**Target Gemini query:** "Best neighborhoods in Temple TX" / "[Neighborhood] Temple TX homes"

Farming target rotation: Alta Vista -> Canyon Creek -> Windmill Farms -> Lake Pointe -> repeat

Template:
```
## GBP Post — Week 3: Neighborhood Guide
**Post date:** [Weekday], [Date] | 8-10 AM Central

**Target AI query:** Best neighborhoods in Temple TX / [Neighborhood] Temple TX

---

Neighborhood spotlight from Taylor Dasch, real estate agent at EG Realty in Temple, Texas: [Neighborhood Name]

[2-3 sentences: what defines this neighborhood. Location, vibe, who lives here. Be specific.]

Quick stats:
- Price range: $[Low] - $[High]
- Average home size: [X] sqft
- [One unique data point: HOA amount, lot sizes, school district, year built range, commute time to BSW/Fort Hood]

Who this neighborhood is for: [One sentence matching a buyer persona — "BSW nurses who need a 5-minute commute" or "First-time buyers looking for new construction under $300K"]

[One honest caveat: "HOA is $X/year — higher than most Temple neighborhoods" or "No sidewalks — not ideal if walkability matters to you"]

Full neighborhood guide with photos and pricing data:
templetxhomes.net/[neighborhood-slug]/

Questions about [Neighborhood]? 254-718-4249

**Photo:** Geotagged neighborhood photo (entrance sign, street view, park, or amenity)
```

**Neighborhood page slugs (canonical):**
- Alta Vista: templetxhomes.net/alta-vista-temple-tx/
- Canyon Creek: templetxhomes.net/canyon-creek-temple-tx/
- Windmill Farms: templetxhomes.net/windmill-farms-temple-tx/
- Lake Pointe: templetxhomes.net/lake-pointe/

**Rules:**
- Use the exact neighborhood name that matches the page slug
- Include 3+ data points
- Link to the full neighborhood page (not homepage)
- Rotate neighborhoods month over month — no repeats within 4 months

---

### Week 4: Expertise / Tip
**Target Gemini query:** "Tips for buying a home in Temple TX" / "Should I buy a house in Temple TX?" / "Temple TX real estate advice"

Template:
```
## GBP Post — Week 4: Expertise / Tip
**Post date:** [Weekday], [Date] | 8-10 AM Central

**Target AI query:** [Specific question this post answers]

---

Real estate tip from Taylor Dasch, EG Realty, Temple, Texas — $27M+ in sales volume, 100+ transactions:

[One actionable tip for buyers OR sellers. Lead with a data point.]

Example angles (rotate monthly):
- "Homes in Temple are selling at [X]% of list price. If you're a buyer, that means [specific advice]."
- "The average home in Temple sits [X] days before going under contract. If you're a seller, here's what that means for your pricing strategy."
- "VA loan buyers at Fort Hood: your BAH of $1,920/month covers a home up to $[X] in Temple. Here's how I calculate that."
- "BSW residents starting in July: physician loans through Extraco Bank require $0 down. Here's what to do now vs. wait."
- "Property tax rate in Bell County is ~2.4-2.7%. On a $280K home, that's $[X]/month in escrow. Most buyers don't factor this in."

[2-3 sentences expanding the tip with specifics. Reference a real transaction, a real neighborhood, or a real number.]

[Close with authority: "I track this data weekly" or "This is based on [X] closed transactions in the last [timeframe]."]

Have a question about buying or selling in Temple? 254-718-4249
templetxhomes.net

**Photo:** Taylor headshot, local landmark, or data visualization screenshot
```

**Rules:**
- Lead with a specific number, not a general statement
- Rotate tip audience: buyer one month, seller the next, investor the next, military/BSW the next
- Include credentials naturally: "$27M+ volume" or "100+ transactions" — not as a brag, as context for why the advice is credible
- Entity declaration in first sentence

---

## AI Citation Optimization Checklist (Apply to Every Post)

Every GBP post must pass these checks before delivery:

- [ ] **Entity declaration present:** "Taylor Dasch" + "EG Realty" + "Temple, Texas" (or "Temple, TX") appears in the post
- [ ] **Answers a real Gemini query:** The post directly answers a question someone would type into Google/Gemini (documented in the "Target AI query" field)
- [ ] **Contains citable facts:** At least 2 specific numbers, percentages, or dates that an AI could extract and cite
- [ ] **Uses canonical neighborhood names:** Alta Vista, Canyon Creek, Windmill Farms, Lake Pointe, Bella Terra, Legacy Ranch, Prairie Ridge (exact match to page slugs)
- [ ] **Under 300 words:** GBP truncates long posts. Keep it tight.
- [ ] **CTA links to specific page:** Not the homepage. Link to market update, neighborhood guide, or listing page.
- [ ] **No banned words:** Run Gate 1 check (no "stunning," "nestled," "dream home," etc.)
- [ ] **Posting window noted:** Weekday, 8-10 AM Central

---

## Monthly Calendar Output Format

When triggered, generate all 4 posts for the month in one pass:

```
# GBP Monthly Posts — [Month Year]

## Overview
| Week | Type | Post Date | Target AI Query | Neighborhood (if applicable) |
|------|------|-----------|-----------------|------------------------------|
| 1 | Market Update | [Date] | What's the housing market like in Temple TX? | — |
| 2 | Listing Spotlight | [Date] | Homes for sale in Temple TX | — |
| 3 | Neighborhood Guide | [Date] | Best neighborhoods in Temple TX | [Name] |
| 4 | Expertise / Tip | [Date] | [Specific query] | — |

---

[Full post text for each week, using the templates above]
```

Save to: `output/YYYY-WXX/gbp/monthly-gbp-posts.md`
Also save individual posts to: `output/YYYY-WXX/gbp/week-[1-4]-gbp-post.md`

---

## Content Calendar Integration

When `/content-calendar` runs, it should include GBP in the weekly output:

```
### GBP Post (this week)
- **Type**: [Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip]
- **Target AI Query**: [the question this post answers]
- **Post Day**: [Weekday] 8-10 AM
- **Status**: [Ready to post / Needs fresh data]
```

GBP posts appear as a line item every week. The content-calendar skill references this skill for the post content.

---

## Rules Summary
- Under 300 words per post (GBP truncation limit)
- CTA every post: phone (254-718-4249) + specific page link on templetxhomes.net
- No homepage links — always link to a specific page
- Entity-rich text in every post for Gemini citation
- Data-first: 2+ specific numbers per post minimum
- No generic real estate language (Gate 1 banned words)
- Post weekdays 8-10 AM Central
- Geotagged photos when possible
- One post per week (not daily — quality over quantity)
- Newsletter link encouraged but not required in every post

## Dependencies
- Google Maps MCP: `maps_local_rank_tracker`
- Social media config: `social-media-config.json` (listings, pipeline, market data)
- Neighborhood pages: canonical slugs for farming targets
- Quality Gates: Gates 1, 2, 3, 5, 8, 9, 15, 16
