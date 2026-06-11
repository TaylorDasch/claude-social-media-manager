# Repurpose Map — Top 3 Temple TX Under $250K

**Source asset:** Main YouTube video (11:00) + 5 Shorts already drafted.
**Goal:** Extract 8–10 derivative assets per video so the production cost amortizes across the entire content calendar.
**Lane discipline:** Living in Temple (BUYER lane) only — never cross-post to investor channels (BiggerPockets investor sub-forums, Investing in Temple YT, Investor Brief newsletter). Lake angles are LIFESTYLE not STR.

---

## DERIVATIVE ASSET PIPELINE

### 1. Temple Insider newsletter section (Buyer audience)
**Target send:** Same week as video publish.
**Format:** ~250-word section + visual.
**Headline:** "The 3 neighborhoods that came back from the MLS under $250K"
**Body:** Lead with the decision matrix from the script's closing. Anchor on the three velocity stats (17 active in Pecan Creek, 2 active in Westfield, 20-day median DOM in Morgans Point Resort). Embed the main YouTube link as the primary CTA, secondary link to the CSV download.
**Owner:** Taylor (Postiz scheduled or manual ESP send).

### 2. AEO content page on templetxhomes.net
**URL slug:** `/best-temple-tx-neighborhoods-under-250k`
**Page type:** Question-Hook → Answer-First → MLS Data → Decision Frame → FAQ
**Why this page:** Already a high-intent search query Taylor is not currently ranking for. Pull the script's structure into a long-form page with FAQ schema for AI Overviews.
**Schema stack:** RealEstateListing references + FAQPage + LocalBusiness + Place (each neighborhood as a separate Place entity).
**CTA placement:** Newsletter signup + buyer consult form + embedded YouTube video.
**Owner:** Use the `/aeo-page-builder` skill — feed it this video's script.md + ground-truth-pack.md as source.

### 3. BiggerPockets forum thread (Texas Real Estate sub-forum)
**Target sub:** Texas Real Estate · Bell County / Temple thread (if it exists; otherwise start one).
**Format:** Long-form data post — NOT a "watch my video" plug.
**Hook:** "I pulled the May 15 Temple MLS for everything under $250K. Here's what the data says about the three best neighborhoods for buyers."
**Body:** ~400 words. Lead with the numbers, link the CSV (NOT just the YouTube). Soft-link the YouTube at the end as "if you want this in video form."
**Value:** Adds Bell County data to BP forums where Temple is under-covered. Earns featured-agent reputation, drives organic profile views.
**Owner:** Use `biggerpockets-harvester` agent to draft, Taylor approves and posts.

### 4. LinkedIn analyst post (BSW relocator + medical recruiter audience)
**Format:** Single-image post with key stats + ~150-word commentary.
**Image:** Static version of the decision-matrix graphic.
**Hook:** "For BSW physicians and medical staff relocating to Temple under a $250K target, the MLS pulled three names this week."
**CTA:** "Full breakdown in video — link in comments."
**Owner:** Taylor manual, or `/linkedin-content` skill draft → Taylor publishes.

### 5. Instagram / Reels reels-format reposts
**Source:** Same 5 Shorts already drafted (`shorts.md`).
**Format:** Repost each Short to IG Reels with 1-line caption + 3 hashtags.
**Hashtags:** #TempleTX #TempleTexasRealEstate #LivingInTemple (channel-consistent).
**Schedule:** Stagger 1 per day for 5 days starting day-of-publish.
**Owner:** Postiz scheduling.

### 6. Facebook (Temple/Bell County community groups)
**Format:** Single-post with main YouTube link + 2-sentence framing.
**Target groups:** Temple Texas community groups, Bell County groups, BSW Family/relocation groups (Taylor is already in these).
**Caveat:** Some groups don't allow agent self-promo — drop the "I'm an agent" framing and lead with "I pulled the MLS data." Comply with each group's rules.
**Owner:** Taylor manual (sensitive to community-group etiquette).

### 7. Postiz scheduled cross-channel posts (Threads, Bluesky, X if active)
**Format:** Single tweet/post with key stat + video link.
**Suggested copy options:**
- "Pulled the May 15 Temple-Belton MLS. 1,223 listings under $250K. 358 different neighborhoods. Three came back clearly: Pecan Creek, Westfield, Morgans Point Resort. Different houses, different buyers. Breakdown: [link]"
- "Cheapest brand-new home in Temple TX right now: $189,185. Pecan Creek. 1,156 sqft. The only neighborhood with 17 active brand-new under $250K. [link]"
- "9 days from listing to under contract — $235K on Belton Lake's Morgans Point Resort peninsula. Median DOM there: 20 days. Why the lake moves faster than the suburbs: [link]"
**Owner:** Postiz schedule via Hermes.

### 8. FUB drip — buyer-prospect follow-up touch
**Audience:** Existing FUB buyer leads in $200K–$280K bracket that haven't been touched in 30+ days.
**Format:** Email drip (drafted in FUB, sent manually after Taylor approval).
**Subject:** "Pulled the MLS for everyone shopping under $250K in Temple"
**Body:** ~150 words. Lead with the three neighborhood names. Embed YouTube as the primary CTA. Soft signature.
**Compliance:** DRAFTS ONLY — no auto-send. Taylor reviews list before queue.
**Owner:** Taylor manual / `/cold-email` skill draft.

### 9. Blog post on templetxhomes.net (long-form, SEO play)
**URL slug:** `/blog/best-neighborhoods-temple-tx-under-250k-may-2026`
**Format:** ~1,500-word blog post = the script's transcript + embedded video + Mortgage math sidebar + Neighborhood-comparison table.
**Schema:** Article + FAQPage + RealEstateListing references.
**Internal linking:** Link to the AEO page from #2, link to monthly market read, link to individual neighborhood pages if they exist.
**Owner:** Use `/transcript-to-blog` skill on the script.

### 10. Telegram channel post
**Audience:** Taylor's personal Telegram alert channel (where he gets dashboard pings).
**Format:** Short note acknowledging "video published" + link.
**Frequency:** One-time, day-of-publish.
**Owner:** Postiz or manual.

---

## SCHEDULING TEMPLATE

| Day | Asset | Channel | Owner |
|---|---|---|---|
| Day 0 (publish day) | Main video | YouTube | Taylor |
| Day 0 | Pinned comment | YouTube | Taylor |
| Day 0 | Short #1 (Pecan Creek) | YouTube Shorts + IG Reels | Postiz |
| Day 0 | Postiz tweet thread (X/Threads/Bluesky) | Multiple | Postiz |
| Day 0 | Telegram alert | Personal | Manual |
| Day 1 | Temple Insider newsletter | Email (ESP) | Taylor |
| Day 1 | LinkedIn analyst post | LinkedIn | Taylor |
| Day 2 | Short #2 (Westfield) | YouTube + IG | Postiz |
| Day 2 | BiggerPockets thread | BP forum | Taylor (with biggerpockets-harvester draft) |
| Day 3 | Short #3 (Morgans Point Resort) | YouTube + IG | Postiz |
| Day 4 | Facebook community groups | FB | Taylor manual |
| Day 5 | Short #4 (Decision frame) | YouTube + IG | Postiz |
| Day 5 | Blog post + AEO page goes live | templetxhomes.net | Use `/transcript-to-blog` + `/aeo-page-builder` |
| Day 6 | FUB buyer drip (reviewed by Taylor) | Email (FUB drafts) | Taylor |
| Day 7 | Short #5 (The one I'd skip) | YouTube + IG | Postiz |
| Day 7 | Postiz repeat tweet variant | X/Threads/Bluesky | Postiz |
| Day 14 | Performance review check | All | Taylor / `/performance-reporter` skill |

---

## LANE / VOICE GUARDRAILS FOR REPURPOSING

- **No investor framing** anywhere. Lake = lifestyle, not Airbnb income.
- **No "broker"** language. "Agent" only.
- **No banned voice words** — re-check each derivative for "dream," "perfect," "nestled," "charming," "hidden gem."
- **No auto-send to client lists** — every email draft requires Taylor approval before send.
- **No FUB action-plan auto-enrollment** based on this content alone — manual queue only.
- **MLS data is publicly licensed** — okay to embed in newsletter and blog. Always include "data pulled [date]" attribution.
- **Cross-post to investor channels = NO.** Living in Temple lane only.

---

## SUCCESS METRICS

| Metric | 7-day target | 30-day target |
|---|---|---|
| Main video views | 1,500 | 5,000 |
| Average view duration | ≥ 55% | ≥ 50% |
| Shorts impressions (5 Shorts combined) | 25,000 | 75,000 |
| Newsletter open rate | ≥ 35% (analyst-tier audience) | — |
| BiggerPockets thread engagement | 10+ replies | featured if >25 replies |
| AEO page indexed in GSC | within 7 days | top-10 ranking for primary query by Day 30 |
| Inbound buyer leads (FUB, form, comment DM) | 5+ direct | 15+ |
| Comment count on main video | 25+ in first 48 hours | — |
