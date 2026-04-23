# YOUTUBE IN-FEED VIDEO ADS — Monday Setup Guide
## Taylor Dasch | EG Realty | Temple TX Real Estate
### Target Launch: Monday, March 30, 2026

---

## TABLE OF CONTENTS

1. [Pre-Setup Checklist](#1-pre-setup-checklist)
2. [Campaign Structure](#2-campaign-structure)
3. [Targeting Settings](#3-targeting-settings)
4. [Ad Creative](#4-ad-creative)
5. [Optimization Schedule](#5-optimization-schedule-weeks-1-4)
6. [Retargeting Setup](#6-retargeting-setup)
7. [Budget Scaling Plan](#7-budget-scaling-plan)
8. [Expected Results](#8-expected-results)
9. [Monday Morning Checklist](#9-monday-morning-checklist)

---

## 1. PRE-SETUP CHECKLIST

Complete these before touching Google Ads on Monday.

### A. Link YouTube Channel to Google Ads

**IMPORTANT UPDATE (April 2026):** Google is auto-linking YouTube channels to Google Ads accounts on April 11, 2026. You may already be linked or have a pending notification. Check first before manually linking.

**Check if already linked:**
1. Open Google Ads (ads.google.com)
2. Click the **Tools** icon (wrench) in the top nav
3. Under **Setup**, click **Linked accounts**
4. Look for **YouTube** — if your channel appears, you are already linked. Skip to Section B.

**If NOT linked — Link from Google Ads (recommended):**
1. In Google Ads, go to **Tools > Setup > Linked accounts**
2. Click **YouTube**
3. Click **+ Link**
4. Search for your YouTube channel name or paste the channel URL
5. Select your channel from results
6. Choose permissions: select **All** (you want full access for remarketing + conversion tracking)
7. Click **Link**
8. Go to YouTube Studio and **approve** the pending link request:
   - YouTube Studio > Settings (gear icon) > Channel > Advanced settings
   - Scroll to **Google Ads account linking** — approve the pending request

**Alternative — Link from YouTube Studio:**
1. Sign in to YouTube Studio (studio.youtube.com)
2. Click **Settings** (left menu) > **Channel** > **Advanced settings**
3. Scroll to **Google Ads account linking**
4. Click **Link Account**
5. Enter a link name (e.g., "Taylor Dasch Google Ads")
6. Enter your Google Ads customer ID (10-digit number, formatted XXX-XXX-XXXX — find it at top-right of your Google Ads dashboard)
7. Click **Done**
8. Go to Google Ads and approve the link under Tools > Linked accounts > YouTube

### B. Verify Channel Eligibility

Your videos must meet these requirements to run as In-Feed ads:
- [ ] Videos are set to **Public** (not Private or Unlisted)
- [ ] Videos comply with YouTube ad policies (no restricted content)
- [ ] Videos are uploaded to the channel you are linking (not someone else's)
- [ ] Video resolution is at least 720p (1080p recommended)
- [ ] Videos are longer than 11 seconds (needed for remarketing list building)

**Confirm these 3 videos are public on your channel:**
1. "Living in Temple TX" (relocation overview)
2. "Pros and Cons of Temple TX" (trust builder)
3. "Top 5 Neighborhoods Temple TX" (comprehensive tour)

### C. Set Up Conversion Tracking

You need 3 types of conversion tracking:

**1. YouTube Engagement Conversions (automatic once linked):**
- After linking your channel + Google Ads, YouTube automatically creates conversion actions for:
  - **Subscribers** — tracks when ad viewers subscribe
  - **Follow-on video views** — tracks when someone watches another video after the ad
- These appear automatically in Google Ads under **Tools > Measurement > Conversions**
- Verify they appear. If not, wait 24 hours after linking.

**2. Website Visit Tracking (Google Ads tag):**
- Go to **Tools > Measurement > Conversions** in Google Ads
- Click **+ New conversion action**
- Select **Website**
- Enter `templetxhomes.net`
- Google will scan your site. If the Google tag is not installed:
  - Copy the Global Site Tag (gtag.js) snippet
  - Install it in your AgentFire site header (AgentFire Dashboard > Settings > Header Scripts)
- Create a conversion action for "Page visit" on key pages:
  - `/contact/` (contact page visits)
  - `/schedule/` or Calendly booking confirmation (if you have one)
  - Any lead capture thank-you page

**3. Google Analytics 4 Integration (if not already done):**
- In GA4, go to **Admin > Google Ads Links** > click **Link**
- Select your Google Ads account and confirm
- In Google Ads, go to **Tools > Measurement > Conversions > Import**
- Select **Google Analytics 4 properties** and import relevant goals

**Enable auto-tagging:**
- Google Ads > **Admin** (gear icon) > **Account settings** > **Auto-tagging** > Turn ON
- This adds `gclid` parameters to URLs so GA4 can attribute visits to your YouTube ads

---

## 2. CAMPAIGN STRUCTURE

### Campaign Setup — Step by Step in Google Ads

1. Log into Google Ads (ads.google.com)
2. Click **+ New campaign** (blue button)
3. **Campaign objective:** Select **"Brand awareness and reach"** — OR for more engagement-focused: select **"Product and brand consideration"** then **"Influence consideration"**
   - **Recommended for you:** Select **"Video views"** as the goal. This optimizes for people who actually watch your content (not just impressions). You pay per view.
4. **Campaign subtype:** Select **"Video views"** (this enables In-Feed ad format)
5. **Campaign name:** `Temple TX Real Estate — Video Discovery`

### Bid Strategy

6. **Bid strategy:** Select **"Maximum CPV"** (cost per view)
   - Set maximum CPV bid: **$0.10** to start
   - This means you pay up to $0.10 when someone clicks your thumbnail and watches
   - At $0.10 CPV, your $10/day budget gets ~100 views/day
   - Real estate CPV typically ranges $0.05-$0.15 for In-Feed; start at $0.10 and adjust after Week 1

### Budget

7. **Budget:** $10.00/day
8. **Delivery method:** Standard (spread throughout the day)
9. **Start date:** March 30, 2026
10. **End date:** Leave open (you will manually pause/adjust)

### Networks

11. **Networks:** Uncheck everything EXCEPT:
    - [x] YouTube search results
    - [x] YouTube videos (watch page)
    - [ ] Video partners on the Display Network — **UNCHECK THIS** (wastes budget on random sites)

### Ad Groups (Create 3)

**Ad Group 1: "Living in Temple TX — Relocation"**
- Video: Select your "Living in Temple TX" video
- Daily budget share: ~$3.33/day
- This is your broadest appeal video — targets anyone considering Temple

**Ad Group 2: "Pros and Cons — Trust Builder"**
- Video: Select your "Pros and Cons of Temple TX" video
- Daily budget share: ~$3.33/day
- Negative/honest angle builds trust and drives longer watch time

**Ad Group 3: "Top 5 Neighborhoods — Deep Dive"**
- Video: Select your "Top 5 Neighborhoods Temple TX" video
- Daily budget share: ~$3.33/day
- Most purchase-intent; people searching neighborhoods are further in the funnel

**Note on budget split:** Google distributes budget at the campaign level. To control per-ad-group spend, you have two options:
- **Option A (simpler):** Create ONE campaign with 3 ad groups. Google will auto-allocate budget to the best performers. Less control but lets Google optimize.
- **Option B (more control):** Create 3 separate campaigns at $3.33/day each. Full control over each video's spend. More management work.
- **Recommendation:** Start with Option A (one campaign, 3 ad groups). Easier to manage and Google's optimization is decent for discovery campaigns.

---

## 3. TARGETING SETTINGS

### Geographic Targeting

For each ad group, set location targeting:

**Primary target:**
- Temple, TX + **50-mile radius** (covers Belton, Killeen, Fort Hood, Harker Heights, Copperas Cove, Salado, Troy, Rogers)

**Secondary targets (people searching FROM these cities about Temple):**
- Austin, TX (metro area) — BSW medical workers, investors
- Dallas-Fort Worth, TX (metro area) — investors, remote workers
- San Antonio, TX (metro area) — military families, investors
- Houston, TX (metro area) — investors, relocators

**Location option (CRITICAL):**
- Select **"People in or regularly in your targeted locations"** AND **"People searching for your targeted locations"**
- This captures someone in Houston Googling "Temple TX homes" — exactly who you want

### Audience Segments

Add these audience segments to each ad group (layer them with OR logic, not AND):

**In-Market Audiences:**
- Real Estate > Residential Properties (For Sale)
- Real Estate > Real Estate Listings
- Moving & Relocation Services
- Home Improvement > Home Building & Renovation (catches new build buyers)

**Life Events:**
- Recently moved
- Getting married (trigger for home purchase)
- Starting a new job (relocation trigger)
- Retiring soon (downsizers + investors)

**Affinity Audiences:**
- Home & Garden > Home Decor Enthusiasts
- Lifestyles & Hobbies > Family-Focused
- Banking & Finance > Avid Investors (catches real estate investors)
- News & Politics > Avid News Readers (higher-intent audiences)

**Custom Segments (create these — highest ROI):**
- **Custom Segment 1: "Temple TX Home Buyers"**
  - Keywords: temple tx homes for sale, temple texas real estate, homes in temple tx, move to temple tx, living in temple texas, temple tx neighborhoods
- **Custom Segment 2: "Military Relocation"**
  - Keywords: PCS Fort Hood, Fort Hood housing, military move Texas, BAH Fort Hood 2026, Fort Hood base housing
- **Custom Segment 3: "Texas Real Estate Investors"**
  - Keywords: texas investment property, rental property texas, BRRRR Texas, DSCR loan Texas, cash flow rental property, temple tx rental market
- **Custom Segment 4: "BSW Medical Relocation"**
  - Keywords: Baylor Scott White jobs, BSW Temple TX, medical jobs Temple Texas, BSW relocation, healthcare jobs central Texas

### Keyword Targeting (Per Ad Group)

**Ad Group 1 — "Living in Temple TX":**
- living in temple tx
- moving to temple texas
- temple tx relocation
- is temple tx a good place to live
- temple texas cost of living
- pros and cons temple tx
- fort hood area homes

**Ad Group 2 — "Pros and Cons":**
- temple tx pros and cons
- should I move to temple texas
- temple tx honest review
- is temple tx safe
- temple tx things to know before moving
- central texas places to live

**Ad Group 3 — "Top 5 Neighborhoods":**
- temple tx neighborhoods
- best neighborhoods temple texas
- where to live in temple tx
- temple tx new construction
- temple tx homes for sale
- best areas temple tx for families

### Exclusions (Prevent Wasted Spend)

**Audience exclusions:**
- Real estate agents / brokers (they are not your customers)
- Real estate professionals (Google has this as an affinity segment)
- People who already subscribed to your channel (they already found you)

**Content exclusions:**
- Embedded videos
- Live streaming videos
- Below-the-fold placements (if option available)

**Topic exclusions:**
- Sensitive social issues
- Tragedy and conflict
- Gambling

### Device Targeting

- **All devices** — leave default (mobile + desktop + tablet + TV)
- Mobile will likely get 60-70% of views — that is normal and fine
- Do NOT exclude any device at this budget level; you need the data

### Age/Demographic Targeting

- **Age:** 25-65+ (exclude 18-24 — very few home buyers)
- **Gender:** All
- **Parental status:** All (parents and non-parents both buy homes)
- **Household income:** If available, select Top 50% (upper and middle income). If this reduces reach too much at $10/day, leave it open.

---

## 4. AD CREATIVE

### How In-Feed Ads Display

Your In-Feed ad shows as:
- **Thumbnail image** (auto-generated from your video OR custom)
- **Headline** (up to 100 characters, but first 25 show on most placements)
- **Description** (2 lines, up to 35 characters each)
- User clicks thumbnail → video plays on its YouTube watch page (counts as a view)

### Thumbnail Strategy

YouTube auto-selects 3 thumbnail options from your video. You can also use your custom thumbnail if already set on the video.

**Best practices for ad thumbnails:**
- Use your existing custom thumbnails (they are already optimized for CTR)
- Resolution: 1280x720 px minimum (16:9 ratio)
- Accepted formats: JPG, GIF, PNG
- Include your face (builds recognition across multiple ad impressions)
- Text overlay should be readable at small sizes (mobile search results)
- High contrast — stands out in search results feed

**Do NOT create separate ad thumbnails.** Your organic thumbnails are already designed for clicks. Consistency between ad thumbnail and video builds trust.

### Headline Writing (Per Ad Group)

In-Feed ad headlines can differ from your organic video title. Use this to test angles:

**Ad Group 1 — Living in Temple TX:**
- Headline: `Thinking About Moving to Temple TX? Watch This First`
- Description Line 1: `$27M+ in local transactions.`
- Description Line 2: `Real data. No hype.`

**Ad Group 2 — Pros and Cons:**
- Headline: `The Truth About Living in Temple TX (Honest Review)`
- Description Line 1: `What most agents won't tell you.`
- Description Line 2: `From a local investor & REALTOR.`

**Ad Group 3 — Top 5 Neighborhoods:**
- Headline: `Top 5 Neighborhoods in Temple TX (2026 Guide)`
- Description Line 1: `Prices, schools, commutes, red flags.`
- Description Line 2: `Data from 100+ local transactions.`

### Headline Tips

- Front-load the location ("Temple TX") — viewers scanning search results need to see relevance immediately
- Keep the first 25 characters punchy — that is all that shows on mobile
- Use parentheses for credibility markers: (2026 Guide), (Honest Review), (Full Breakdown)
- Ad headlines CAN differ from your organic titles — use this to A/B test angles
- Do not use ALL CAPS on more than 2 words

---

## 5. OPTIMIZATION SCHEDULE (Weeks 1-4)

### Week 1 (March 30 - April 5): Data Collection

**Do:**
- Launch all 3 ad groups simultaneously
- Set maximum CPV at $0.10
- Let them run untouched for 7 full days
- Check metrics on Day 3 and Day 7 (do not change anything)

**Track these metrics daily (Google Ads > Campaigns > Video):**

| Metric | Where to Find | What Good Looks Like |
|--------|---------------|---------------------|
| Views | Campaign dashboard | 80-120/day at $10 budget |
| View rate | Ad group level | Above 10% (In-Feed avg is 8-15%) |
| Avg. watch time | Video analytics | Above 60 seconds |
| CTR | Ad group level | Above 2% for In-Feed |
| Cost per view | Ad group level | $0.04-$0.12 |
| Subscribers gained | YouTube Studio > Analytics | Any at all is a win in Week 1 |

**Do NOT:**
- Change bids
- Pause any ad group
- Adjust targeting
- Panic if numbers look low — $10/day is a test budget

### Week 2 (April 6-12): Identify Winner and Loser

**Monday April 6 — Review meeting with yourself:**

Pull 7-day data for each ad group. Rank them by:

1. **View rate** (most important — are people clicking your thumbnail?)
2. **Average watch time** (are they actually watching?)
3. **Cost per view** (are you paying a fair price?)
4. **Subscriber conversions** (bonus metric at this stage)

**Decision matrix:**

| Scenario | Action |
|----------|--------|
| Clear winner (2x better view rate than others) | Increase winner's bid by $0.02, decrease loser's by $0.02 |
| All 3 performing similarly | Keep running, but add a second headline variant to each |
| Clear loser (view rate under 5%, avg watch time under 30 sec) | Reduce loser's bid to $0.05 (starve it, don't kill it yet) |
| All 3 performing poorly (view rate under 5%) | Review targeting — probably too broad or wrong keywords |

**Also check:**
- YouTube Studio > Analytics > Traffic sources — look for "YouTube advertising" and check watch time from ads
- Check if ad viewers are watching other videos on your channel (follow-on views)

### Week 3 (April 13-19): Kill and Redistribute

**Monday April 13 — Cut the loser:**

- Pause the worst-performing ad group entirely
- Redistribute its ~$3.33/day to the remaining two ($5/day each)
- If one is clearly dominant, go $6.50 winner / $3.50 runner-up

**Also this week:**
- Create remarketing audiences (see Section 6)
- Test a second headline on your winning ad group (Google allows multiple ad variants)
- Check YouTube Studio for organic lift — are your non-ad videos getting more impressions?

### Week 4 (April 20-26): Scale Winner + Retargeting

**Monday April 20:**

- If top performer maintains view rate above 10%:
  - Increase total campaign budget to $15/day
  - Allocate $10/day to winner, $5/day to runner-up
- Launch retargeting campaign (see Section 6) at $5/day
- Total new daily spend: $20/day

**Winner metrics that justify scaling:**

| Metric | Scale Threshold |
|--------|----------------|
| View rate | Above 10% sustained |
| Avg watch time | Above 90 seconds |
| Cost per view | Below $0.10 |
| Cost per subscriber | Below $2.00 |
| Follow-on views | Positive (any) |

---

## 6. RETARGETING SETUP

### A. Create Remarketing Lists from YouTube Viewers

**Step by step:**
1. Google Ads > **Tools** (wrench icon) > **Shared library** > **Audience manager**
2. Click the **+** button > Select **"YouTube users"**
3. Create these lists:

**List 1: "Watched Any Video — 30 Days"**
- List type: YouTube users
- List members: Viewed any video from a channel
- Channel: [Your channel]
- Membership duration: 30 days
- Click **Create segment**

**List 2: "Watched 50%+ of Video 1 (Living in Temple)"**
- List type: YouTube users
- List members: Viewed certain videos as ads
- Select your "Living in Temple TX" video
- Membership duration: 60 days
- Click **Create segment**

**List 3: "Watched 50%+ of Video 2 (Pros and Cons)"**
- Same as above but select "Pros and Cons" video
- Duration: 60 days

**List 4: "Channel Subscribers"**
- List members: Subscribed to a channel
- Duration: 540 days (max)

**Note:** Lists need at least 1,000 users to serve ads. At $10/day, you will likely hit this threshold after 10-14 days.

### B. Sequential Retargeting (Video 1 → Video 2)

The play: Someone watches "Living in Temple TX" → show them "Top 5 Neighborhoods" as their next ad. This creates a content journey.

**Setup:**
1. Create a new campaign: `Temple TX Retargeting — Sequential`
2. Budget: $5/day
3. Ad Group 1: "Saw Living in Temple → Show Neighborhoods"
   - Audience: Target List 2 ("Watched 50%+ of Living in Temple")
   - Exclusion: Exclude List 3 ("Already watched Neighborhoods")
   - Ad: Your "Top 5 Neighborhoods" video
4. Ad Group 2: "Saw Neighborhoods → Show Pros and Cons"
   - Audience: Target people who watched 50%+ of Neighborhoods
   - Ad: Your "Pros and Cons" video

### C. Website Visitor Retargeting

**Prerequisite:** Google Ads tag installed on templetxhomes.net (from Section 1C).

**Create website visitor list:**
1. Google Ads > **Tools** > **Audience manager**
2. Click **+** > **"Website visitors"**
3. **List name:** "templetxhomes.net Visitors — 90 Days"
4. **Visited pages:** Rule = URL contains `templetxhomes.net`
5. **Membership duration:** 90 days
6. Click **Create segment**

**Create a campaign targeting these visitors:**
- Show your best-performing video to people who visited your site but did not convert
- This is the warmest audience — they already know your website
- Budget: $2-3/day (small list, highly targeted)

---

## 7. BUDGET SCALING PLAN

### Phase 1: Test ($10/day for 14 days)

| Detail | Value |
|--------|-------|
| Daily budget | $10 |
| Duration | March 30 - April 12 (14 days) |
| Total spend | $140 |
| Expected views | 1,000-1,400 total |
| Goal | Identify winning video and targeting combo |
| Ad groups | 3 (equal split) |

### Phase 2: Optimize ($15-20/day for 14 days)

| Detail | Value |
|--------|-------|
| Daily budget | $15-20 |
| Duration | April 13-26 (14 days) |
| Total spend | $210-280 |
| Expected views | 1,500-2,800 total |
| Goal | Scale winner, cut loser, build remarketing lists |
| Ad groups | 2 (weighted toward winner) |

### Phase 3: Add Retargeting ($20-25/day ongoing)

| Detail | Value |
|--------|-------|
| Daily budget | $20-25 ($15-20 discovery + $5 retargeting) |
| Duration | April 27+ (ongoing) |
| Monthly spend | $600-750 |
| Expected views | 4,000-6,000/month |
| Goal | Compound channel growth + warm audience nurturing |

### When to Increase Budget

| Signal | Action |
|--------|--------|
| Cost per subscriber consistently below $1.50 | Increase budget 25% |
| View rate above 15% | Increase budget 25% |
| Organic views increasing alongside paid | Budget is working — scale |
| Cost per view rising above $0.15 | Do NOT increase — optimize targeting first |
| View rate below 5% | Pause, retarget, or test new creative |

### CPA Benchmarks for Real Estate YouTube Ads

| Metric | Average | Good | Excellent |
|--------|---------|------|-----------|
| Cost per view | $0.08-$0.15 | $0.05-$0.08 | Below $0.05 |
| Cost per subscriber | $1.00-$3.00 | $0.50-$1.00 | Below $0.50 |
| Cost per website visit | $1.50-$4.00 | $0.75-$1.50 | Below $0.75 |
| Cost per lead (form fill) | $15-$50 | $10-$15 | Below $10 |

---

## 8. EXPECTED RESULTS

### Realistic View Counts at $10/Day

| Timeframe | Views (Conservative) | Views (Optimistic) |
|-----------|---------------------|-------------------|
| Week 1 | 500-700 | 700-1,000 |
| Week 2 | 500-700 | 700-1,000 |
| Month 1 total | 2,000-2,800 | 2,800-4,000 |
| Month 2 ($15-20/day) | 3,000-5,000 | 5,000-7,000 |

**Math:** At average CPV of $0.07-$0.10, $10/day = 100-143 views/day = 700-1,000 views/week.

### Expected Cost Per View

- **In-Feed ads for local real estate content:** $0.05-$0.15 per view
- **Temple TX specifically** (small market, less competition): likely on the lower end, $0.05-$0.10
- In-Feed ads typically cost less than In-Stream (skippable pre-roll) because the viewer actively chooses to click

### Expected Subscriber Growth from Ads

- Subscriber conversion rate from In-Feed ad views: 1-5%
- At 100 views/day with 2% conversion: **2 new subscribers/day from ads**
- Month 1 estimate: **40-80 new subscribers** from ads alone
- Month 2 (scaled): **80-150 new subscribers**
- Organic lift (ads driving more recommendations): additional 20-40% on top

### Timeline to Monetization Eligibility

YouTube Partner Program requires: **1,000 subscribers + 4,000 watch hours** (in trailing 12 months)

| Current Subs | Monthly Ad Subs | Monthly Organic Subs | Time to 1,000 |
|-------------|----------------|---------------------|---------------|
| 100 | 60 | 30 | ~10 months |
| 250 | 60 | 30 | ~8 months |
| 500 | 80 | 40 | ~4 months |

**Watch hours note:** YouTube ad views do NOT count toward the 4,000 watch hour requirement for monetization. Only organic views count. However, ads drive subscribers who then watch future videos organically — creating a flywheel.

### The Real Value (Not Just Subs)

Do not measure success purely on subscriber count. For a real estate agent, the value chain is:

1. **Ad view** → viewer learns you exist
2. **Watch time** → viewer trusts your expertise
3. **Subscribe** → viewer enters your orbit permanently
4. **Organic views** → subscriber watches your new uploads
5. **Website visit** → subscriber hits templetxhomes.net
6. **Lead** → fills out contact form or books Calendly
7. **Client** → closes a transaction

One closed deal from YouTube ads = $5,000-$15,000+ commission. That pays for years of $10/day ad spend.

### Effect on Organic Algorithm

Based on current YouTube algorithm behavior (2026):
- **Ads DO NOT hurt organic reach.** The algorithm ranks on watch time, CTR, engagement, and satisfaction — not on whether a video was promoted.
- **Ads CAN boost organic reach** if ad viewers engage well (high watch time, likes, comments, subscribes). This sends positive signals.
- **New subscribers from ads** become part of your notification and home feed audience, increasing organic views on ALL future uploads.
- **YouTube now separates organic and paid metrics** in YouTube Studio analytics, so you can track each independently.
- **Best practice:** Keep your ad videos public (not unlisted). In-Feed ad watch time on public videos contributes positive signals. Only In-Stream (pre-roll) ads should use unlisted videos to avoid dragging down average watch time.

---

## 9. MONDAY MORNING CHECKLIST

Print this. Do these in order on March 30, 2026.

### Before 9:00 AM — Pre-Flight

- [ ] Log into Google Ads (ads.google.com)
- [ ] Confirm YouTube channel is linked (Tools > Linked accounts > YouTube)
- [ ] Confirm all 3 videos are PUBLIC on your channel
- [ ] Confirm Google Ads conversion tag is on templetxhomes.net
- [ ] Check that YouTube engagement conversions (subscribers, follow-on views) appear under Tools > Conversions

### 9:00 - 9:30 AM — Create Campaign

- [ ] Click **+ New campaign**
- [ ] Select goal: **Video views**
- [ ] Campaign subtype: **Video views**
- [ ] Campaign name: `Temple TX Real Estate — Video Discovery`
- [ ] Budget: **$10/day**, Standard delivery
- [ ] Bid strategy: **Maximum CPV** at **$0.10**
- [ ] Networks: YouTube search results + YouTube videos ONLY (uncheck Display Network)
- [ ] Start date: Today (March 30, 2026)
- [ ] No end date

### 9:30 - 10:00 AM — Build Ad Group 1

- [ ] Ad group name: `Living in Temple TX — Relocation`
- [ ] Location: Temple TX + 50mi radius AND Austin, Dallas, San Antonio, Houston metros
- [ ] Location option: "People in or searching for your targeted locations"
- [ ] Age: 25-65+
- [ ] Audiences: In-Market (Real Estate, Moving/Relocation) + Custom Segment "Temple TX Home Buyers" + Life Events (Recently moved, Starting new job)
- [ ] Keywords: living in temple tx, moving to temple texas, temple tx relocation, is temple tx a good place to live, temple texas cost of living, fort hood area homes
- [ ] Exclude: Real estate agents/brokers audience
- [ ] Select video: "Living in Temple TX"
- [ ] Headline: `Thinking About Moving to Temple TX? Watch This First`
- [ ] Description 1: `$27M+ in local transactions.`
- [ ] Description 2: `Real data. No hype.`

### 10:00 - 10:30 AM — Build Ad Group 2

- [ ] Ad group name: `Pros and Cons — Trust Builder`
- [ ] Copy location + age + audience targeting from Ad Group 1
- [ ] Keywords: temple tx pros and cons, should I move to temple texas, temple tx honest review, is temple tx safe, temple tx things to know before moving, central texas places to live
- [ ] Select video: "Pros and Cons of Temple TX"
- [ ] Headline: `The Truth About Living in Temple TX (Honest Review)`
- [ ] Description 1: `What most agents won't tell you.`
- [ ] Description 2: `From a local investor & REALTOR.`

### 10:30 - 11:00 AM — Build Ad Group 3

- [ ] Ad group name: `Top 5 Neighborhoods — Deep Dive`
- [ ] Copy location + age targeting from Ad Group 1
- [ ] Add audience: Custom Segment "Texas Real Estate Investors" + "BSW Medical Relocation"
- [ ] Keywords: temple tx neighborhoods, best neighborhoods temple texas, where to live in temple tx, temple tx new construction, temple tx homes for sale, best areas temple tx for families
- [ ] Select video: "Top 5 Neighborhoods Temple TX"
- [ ] Headline: `Top 5 Neighborhoods in Temple TX (2026 Guide)`
- [ ] Description 1: `Prices, schools, commutes, red flags.`
- [ ] Description 2: `Data from 100+ local transactions.`

### 11:00 AM — Launch

- [ ] Review all 3 ad groups one more time
- [ ] Click **Publish campaign**
- [ ] Ads enter Google review (typically approved within 1-4 hours)
- [ ] Set a calendar reminder for April 2 (Day 3 check) and April 6 (Week 1 review)
- [ ] Do NOT touch anything for 7 days

### After Launch — Weekly Review Schedule

| Day | Task |
|-----|------|
| Day 3 (April 2) | Quick metrics check — are ads running? Any disapprovals? |
| Day 7 (April 6) | Full Week 1 review (see Section 5) |
| Day 14 (April 13) | Kill loser, redistribute budget |
| Day 21 (April 20) | Scale winner, launch retargeting |
| Day 28 (April 27) | Full Month 1 report, decide Phase 2 budget |

---

## SOURCES

- [Google Ads Help: In-Feed Video Ads](https://support.google.com/google-ads/answer/6227733?hl=en)
- [Google Ads Help: Link YouTube Channel](https://support.google.com/google-ads/answer/3063482?hl=en)
- [Google Ads Help: YouTube Remarketing](https://support.google.com/google-ads/answer/2545661?hl=en)
- [Google Ads Help: YouTube Engagement Goals](https://support.google.com/google-ads/answer/12301500?hl=en)
- [Google Ads Help: Create a Video Campaign](https://support.google.com/google-ads/answer/2375497?hl=en)
- [LocaliQ: YouTube Advertising Cost 2026](https://localiq.com/blog/youtube-advertising-cost/)
- [Strike Social: Complete Guide to YouTube Advertising 2026](https://strikesocial.com/blog/complete-guide-to-youtube-advertising-in-2025/)
- [ALM Corp: Google Ads Automatic YouTube Channel Linking April 2026](https://almcorp.com/blog/google-ads-automatic-youtube-channel-linking/)
- [ALM Corp: YouTube Interest-Based Ad Targeting 2026](https://almcorp.com/blog/youtube-interest-based-ad-targeting-guide-2026/)
- [AgentFire: YouTube Ads for Real Estate](https://agentfire.com/blog/optimizing-youtube-ads-for-real-estate-agents-strategies-and-tips/)
- [Sierra Interactive: YouTube Advertising for Real Estate](https://www.sierrainteractive.com/insights/blog/how-to-use-youtube-advertising-for-real-estate/)
- [Vireo Video: YouTube Ads Impact on Organic Growth](https://www.vireovideo.com/the-surprising-impact-of-youtube-advertising-on-organic-growth/)
- [AdOutreach: YouTube Ads and Channel Growth](https://adoutreach.com/the-truth-about-youtube-ads-and-your-channels-growth/)
- [Search Engine Journal: YouTube Separates Organic and Paid Metrics](https://www.searchenginejournal.com/youtube-separates-organic-paid-metrics-in-channel-analytics/560045/)
- [MarTech: Google Auto-Linking YouTube and Google Ads](https://martech.org/google-to-auto-link-youtube-channels-and-google-ads-accounts/)
