# Skill: Unique Listings — Weekly FB Group Content

## Trigger
User says: "unique listings", "FB group listings", "pull listings", "group posts this week"

## Purpose
Every Saturday, Taylor pulls 5 standout listings from MLS for his Facebook group "Unique Listings | Temple & Belton Real Estate." This skill takes those listings and produces 5 ready-to-post packages — one per weekday (Mon–Fri).

## What Makes a Listing "Unique"
Not every listing qualifies. Look for at least ONE of these:
- **Architecture** — Barndominium, mid-century, A-frame, custom build, historic
- **Land** — Acreage, waterfront, ranch, unrestricted, ag-exempt
- **Lifestyle** — Pool, shop/barn, guest house, views, gated
- **Price story** — Way under market, estate sale, auction, creative financing possible
- **Location play** — Backs to greenbelt, lakefront, cul-de-sac on acreage
- **Unusual feature** — Wine cellar, home theater, airplane hangar, storm shelter, solar

Generic 3/2 tract homes do NOT qualify unless the price is a clear outlier.

## Input
Taylor provides 5 listings with:
- MLS # or address
- List price
- Bed / bath / sqft
- Lot size (if notable)
- Year built
- What makes it unique (1-2 sentences)
- 1-3 photo URLs or descriptions

If Taylor doesn't provide the "what makes it unique" — identify it from the listing data yourself.

## Output Per Listing (5 total)

### 1. Facebook Group Post Caption
```
📍 [Address] — [City], TX
💰 [Price]
🏠 [Bed]bd / [Bath]ba • [Sqft] sqft
🔑 [One-line unique hook]

[2-3 sentences: what makes this one stand out. Be specific — not "beautiful home" but "1,200 sqft detached shop with full electrical on 2.5 acres, ag-exempt." Include honest context — DOM, price history, or condition notes if relevant.]

[Taylor's angle — who this is for: "First-time buyer looking for land without leaving city limits" or "Investor: run the numbers on this one as an MTR near BSW"]

📩 Want details or a showing? Drop a comment or DM me.
Taylor Dasch • EG Realty • 254-718-4249
```

**Rules for captions:**
- Lead with the address and price — no clickbait
- The hook line should be the single most interesting fact
- Include honest negatives if obvious (high DOM, price cuts, known issues)
- NO banned words (dream home, stunning, nestled, perfect, gorgeous, charming)
- Vary the unique hook across the 5 — don't repeat patterns
- Tag the city if in Belton, Salado, Troy, or other non-Temple locations

### 2. Posting Schedule
Assign each listing to a weekday:
- **Monday** — Strongest/most eye-catching listing (sets the week's tone)
- **Tuesday** — Land or acreage play (if available)
- **Wednesday** — Best value / price story
- **Thursday** — Lifestyle / luxury feature
- **Friday** — Wildcard / most unusual

If categories don't fit perfectly, just distribute for variety.

### 3. Repurpose Flags
For each listing, flag if it's strong enough to also become:
- [ ] TikTok drive-by video
- [ ] Instagram Reel
- [ ] YouTube Shorts
- [ ] Newsletter feature (Temple Insider or Investor Brief)
- [ ] Full YouTube video tour request

Only check boxes where the listing genuinely warrants it. Most will get 0-1 flags.

## Output Format
Save to: `output/YYYY-WXX/unique-listings/`
- `weekly-lineup.md` — All 5 posts with schedule and repurpose flags
- Individual files NOT needed — the lineup doc is the deliverable

## Saturday Workflow
1. Taylor pulls 5 listings from MLS (or gives addresses/MLS #s)
2. Run `/unique-listings` with the data
3. Claude produces the 5-post lineup with M-F schedule
4. Taylor copies each post to Facebook group on the assigned day
5. If any listing gets strong engagement, flag for deeper content (video, blog)

## Quality Gates (inherited from governance)
- Gate 1: No banned words
- Gate 2: Entity declaration in every post (Taylor Dasch • EG Realty)
- Gate 4: Honest negatives where applicable
- Gate 8: Platform format (Facebook — no hashtag spam, conversational tone)
- All prices and stats must come from MLS data Taylor provides — never estimate
