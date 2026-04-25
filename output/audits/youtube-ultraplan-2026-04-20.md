# ULTRAPLAN: YouTube Lead-Gen Engine — Living in Temple Channel

**Date:** 2026-04-20
**Companion docs:** `youtube-audit-2026-04-20.md` + `youtube-retention-research-2026-04-20.md`
**Status:** Operational plan consolidating all YouTube findings + adding equipment, settings, daily routine, and reusable skill

---

## Goal Lock

**Sentence:** Turn Taylor's 149-video YouTube channel into a reliable inbound lead generator averaging **2-3 qualified relocation leads per week** within 90 days (currently ~1 lead/week from YouTube).

**Classification:** 🟢 **REVENUE** (primary — direct lead gen) + 🔵 **INFRASTRUCTURE** (secondary — compounding content library)

**Time Estimate:** ~40 hours of Taylor's time across 12 weeks (phased, never more than 5 hours in any single week)

**Revenue Impact:** Direct. YouTube is Taylor's #3 lead source at $7.5K/yr. Goal: 2x that within 12 months via retention fixes + focused content.

**Measurement:**
- Lead count in FUB tagged "Source: YouTube" → 2-3/week by day 90
- Average view duration on long-form uploads → >25% (currently 12%)
- Channel impressions up 50% at day 90
- CTR > 5% on new uploads

**Deadline:** 2026-07-20 (90 days)

---

## Dependencies (Resolve Before Execution)

- [ ] **Fort Hood vs Fort Cavazos naming decision** — my ultraplan skill says "Always use Fort Hood never Fort Cavazos." The PCS video package I built this session uses "Fort Cavazos" throughout. Pick one:
  - **A.** Rename PCS package to "Fort Hood" (edit HTML + script + README). Aligns to rule + higher search volume. 10 min of my time.
  - **B.** Keep "Fort Cavazos" (DoD-official name post-2023 rename). Update the rule in the skill file.
  - **Owner:** Taylor. Default if no answer by 48hr: follow rule (Option A).
- [ ] **YouTube Analytics API access** — I can see view counts but not retention curves, traffic sources, or watch-time. Get a Google Cloud project + enable Analytics API + give me OAuth credentials = real retention data per video.
  - **Owner:** Taylor (10 min with Google Cloud Console) or defer until after first 4 videos ship
- [ ] **Production pipeline smoke test** — Per prior turn, 30 min to validate mic/screen-rec/CapCut flow end-to-end
  - **Owner:** Taylor. Blocker for Phase 2.
- [ ] **Decision: consolidate "Living in Temple" + "Investing in Temple" channels or keep separate?**
  - Per your CLAUDE.md they're separate. Confirm that's still the play.
  - **Owner:** Taylor (1 min)

---

## Execution Plan — 4 Phases

### Phase 1: FOUNDATION FIXES (Week 1 · 4 hours Taylor)

| # | Task | Owner | Time | Tool | Blocked By |
|---|---|---|---|---|---|
| 1.1 | Retitle 8 scheduled videos per audit | Taylor | 20 min | YouTube Studio | None |
| 1.2 | Set default Upload Settings (see Section 3 below) | Taylor | 15 min | YouTube Studio | None |
| 1.3 | Re-cut intros on top 2 videos (Living in Temple 2026 · Best Neighborhoods) | Taylor | 1 hr | CapCut | Section 4 script |
| 1.4 | Run production pipeline smoke test | Taylor | 30 min | Per prior-turn instructions | None |
| 1.5 | Install teleprompter app (BIGVU or PromptSmart Lite free tier) | Taylor | 5 min | App Store | None |
| 1.6 | Decide Fort Hood vs Cavazos + rename PCS package if needed | Taylor | 5 min | 1-word reply | None |
| 1.7 | Audit current FUB "Source: YouTube" tag hygiene | Taylor | 30 min | FUB | None |
| 1.8 | Calendar-block 2 filming days/week for next 12 weeks | Taylor | 10 min | Google Calendar | None |

**Goal:** Before any new content ships, everything upstream of filming is ready.

### Phase 2: FIRST 4 VIDEOS SHIP (Weeks 2-4 · 12 hours Taylor)

Order matters. Built around testing the pipeline on the easiest video first, then the highest-impact one.

| # | Video | Time Total | Why This Order |
|---|---|---|---|
| 2.1 | **Warning 3 Mistakes** | 3 hours film + 2 hours edit = 5 hrs | Easiest B-roll plan (talking head + street shots). Tests pipeline without Mapbox. |
| 2.2 | **Temple Map Tour** | 2 hours film + 1.5 hours edit = 3.5 hrs | Your flagship. Uses prebuilt Mapbox HTML + click-through = lowest filming effort. |
| 2.3 | **Ranked Worst to Best** | 1.5 hours film + 1.5 hours edit = 3 hrs | Retention peak candidate. Same engine as Map Tour. |
| 2.4 | **PCS to Fort Hood** (rename Cavazos if needed) | 2 hours film + 2 hours edit + 30 min BAH verify = 4.5 hrs | Most data-sensitive — verify DoD BAH rates day-of-film. |

**Publish cadence:** one long-form per week + 3 Shorts per week (neighborhood Shorts per existing schedule).

### Phase 3: CADENCE LOCK (Weeks 5-8 · 16 hours Taylor)

- 1 long-form + 3 Shorts per week · batch film 2 videos per session
- **Daily practice routine** (see Section 7) — 30 min/day, non-negotiable
- Community engagement: reply to every comment on new uploads **within 2 hours** for the first 48 hours after publish
- A/B test thumbnails on one underperforming video per week (see Section 2 — underperformer optimizations)

### Phase 4: COMPOUND (Weeks 9-12 · 8 hours Taylor)

- Ship videos #5-10 from the "Top 10 to Do Next" list (Section 4)
- Review retention data (YouTube Analytics API pull) — iterate on what's working
- Refresh default Upload Settings based on what actually moved the needle
- Measure against 90-day targets — adjust plan if behind

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Taylor doesn't film consistently after initial burst | Calendar block 2 film days/week in week 1 · treat as client appointments |
| Mic quality continues to kill retention | Invest $80-150 in proper lav kit Phase 1 (Section 5 list) |
| New content doesn't get algorithmic traction in first 48 hrs | Push to Temple Insider newsletter + Instagram + FB group on upload day |
| Fort Hood/Cavazos rename creates URL/SEO issues | Decide once, stick to it, update all existing video titles + future uploads simultaneously |
| Retitling scheduled videos is forgotten | Block 20 minutes on calendar this week — treat as non-negotiable |

---

## What Taylor Does vs What Claude Handles

| Taylor (can't delegate) | Claude Chat (strategy) | Claude Code (builds) |
|---|---|---|
| Film face-to-camera | Script writing | Mapbox HTML flythroughs |
| Record voiceover | Title A/B suggestions | Video package READMEs |
| Edit in CapCut | Thumbnail text + layout direction | Default Upload Settings text templates |
| Upload + set thumbnail | Community reply drafting | Retention analysis reports |
| FUB lead tagging | Daily practice prompts | Skill file for ongoing optimization |
| Be out-and-about (the filming itself) | Quarterly strategy review | Competitor analysis pulls |

---

## Measurement Checkpoints

- **Day 7:** 8 scheduled videos retitled · Upload Defaults set · Intros re-cut · Smoke test passed
- **Day 14:** Warning 3 Mistakes + Temple Map Tour published
- **Day 30:** All 4 Phase-2 videos live · Avg retention on new long-forms ≥ 22%
- **Day 60:** Videos #5-8 live · 1 inbound YouTube lead/week in FUB
- **Day 90:** All 10 videos live · 2-3 inbound YouTube leads/week · Avg retention ≥ 25% · CTR ≥ 5% on new uploads

---

## Next Physical Action

> **Open YouTube Studio. Retitle all 8 scheduled videos per the prior audit. That's 20 minutes. Do it before lunch today.**

Everything else in this plan depends on you shipping that first.

---
---

# SECTION 2 — UNDERPERFORMER OPTIMIZATIONS (Specific Videos)

From your 50-video recent pull, these are videos that have enough existing views to matter but are underperforming against your top 7. **Retitling + thumbnail A/B = highest ROI optimizations.**

### Tier 1: Videos with 100-500 views that could break 1,000 with a retitle

| Video ID | Current Title | Views | Suggested New Title | Why |
|---|---|---|---|---|
| `cAxYKEcYGiE` | Should You Move to Temple Texas? (2026 Honest Review: Cost, Crime & More) | 499 | Should You Move to Temple Texas? The Honest Answer (2026 Data) | Remove parenthetical clutter · "honest answer" triggers click |
| `ZdKKZ8RRy4M` | Cost of Living in Temple TX (2026) — What You'll Actually Pay | 130 | I Tracked My Temple TX Bills for 6 Months — Here's the Real Cost | Personal-lens + "tracked" = curiosity hook |
| `o4USe5ahgX0` | Moving to Temple Texas? Here's What the Market Actually Looks Like | 189 | The Temple TX Market Update Nobody's Making (2026) | "Nobody's making" hook + question removal |
| `yjh9ZDAqBcs` | Moving to Temple TX for BSW? Where Hospital Staff Actually Live (2026) | 144 | Where BSW Temple Staff Actually Live (Real Data, 2026) | Simpler · removes "Moving to" prefix for better thumbnail |
| `zclqPOAhxuk` | Temple TX Housing Market February 2026: Prices, Inventory & What's Next | 69 | Temple TX Market Update — Is Now the Time to Buy? (Feb 2026) | Question in title + action-oriented |
| `0RAHkU1dCi8` | Temple TX Home Prices January 2026: Are They Going Up or Down? | 123 | Temple TX Home Prices — Going Up or Down? (Jan 2026 Data) | Same question, cleaner · put data inside |
| `gKNq_NXR-y4` | Best Belton ISD Neighborhood? The Groves at Lakewood Ranch Temple TX (2026) | 94 | Belton ISD's Fastest-Growing Neighborhood? Groves at Lakewood Ranch | "Fastest-growing" = curiosity |
| `9l6-0luuOq8` | Austin vs Temple TX: Which Has Better Cash Flow for Investors? (2026) | 122 | Austin vs Temple: Where Investors Actually Win in 2026 | Lane issue — this is on "Living in Temple" but it's investor content. **Consider moving to Investing in Temple channel.** |
| `30qMJW6SRBw` | Killeen vs Temple TX: What $350K Buys You in 2026 (Side-by-Side Tour) | 62 | Killeen vs Temple — What $350K Actually Buys (Side-by-Side) | Remove "2026" in title (date it in desc), add "actually" |

**Execution:** 2-minute retitle per video in YouTube Studio. Do all 9 in a single 20-minute session. Set a reminder for Day 14 to measure lift.

### Tier 2: Kill or Unlist (dragging channel average down)

These have under 100 views and titles that can't be meaningfully saved. Decision: **unlist** (not delete — preserves URLs in case they're embedded anywhere).

- `GK87YnAv9ZU` (if you don't retitle per prior audit)
- `jIpTtoOcDAg` (Omega Builders Exclusive Sneak Peek — if you can't find a hook)
- Any builder-specific video older than 6 months with under 80 views

Unlist = hidden from channel feed but still accessible via direct link. Keeps your channel average high.

### Tier 3: Reupload Candidates

One video with real strategic value that should be RE-SHOT not retitled:

- `lpqk4BlsWno` — "Homeowners Insurance in Temple TX: What You'll Really Pay (2026)" · 56 views · 54 sec
  - This is a **long-form opportunity, not a 54-second Short**. Insurance in Temple is a massive buyer concern (storms, flood zones). Re-shoot as 8-10 min long-form: "The Homeowner's Insurance Trap in Temple TX (What Nobody Tells You)."

---
---

# SECTION 3 — YOUTUBE STUDIO DEFAULT SETTINGS (Copy-Paste Ready)

YouTube Studio → Settings → Upload Defaults. Set these once, save 10 min per future upload.

## Default Description Template

Replace the top block each video; keep the bottom block permanent.

```
[ONE-LINE HOOK — matches video topic]

[2-3 sentences summarizing value. Include main keyword + Temple TX.]

📍 Get the free PDF mentioned in this video: templetxhomes.net
📞 Text or call Taylor: 254-718-4249
✉️ dealswithdasch@gmail.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Work with me
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I'm Taylor Dasch — REALTOR® with EG Realty in Temple, TX. I help buyers and investors move to Central Texas with data, not sales pitches.

🗺️ Free Temple Neighborhood Map: templetxhomes.net
📰 Temple Insider newsletter (biweekly buyer brief): templetxhomes.net/newsletter
📊 Investor Brief newsletter (biweekly cap rates + deals): templetxhomes.net/investor-brief

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📺 Watch next
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Link to your Temple Map Tour video once it's published]
[Link to "Ranked Worst to Best" once published]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏡 Licensed: Texas · EG Realty
DISCLAIMER: This content is for informational purposes and not financial or legal advice. Always consult a licensed professional for your specific situation.
```

## Default Tags (30 tags max · YouTube counts characters)

Put the most-searched tags first. YouTube weights order.

```
moving to temple tx, living in temple tx, temple texas real estate, temple tx neighborhoods, temple tx cost of living, best neighborhoods temple tx, temple tx 2026, central texas real estate, temple tx homes for sale, moving to central texas, temple vs killeen, belton isd, academy isd, temple tx real estate agent, taylor dasch, bsw temple, fort hood housing, fort hood pcs, va loan temple tx, temple tx market update, temple tx investor, temple tx new construction, lake pointe temple, canyon ridge temple, bella terra temple, hillside village temple, relocating to texas, relocating to temple, moving from austin to temple, temple tx 2026 honest
```

Character count: ~490. You can swap specific neighborhood/keyword tags per video within the 500-char limit.

## Default Visibility

- **Public** (NOT unlisted) — only use unlisted for testing
- **Published date:** Let you set manually per video — don't default to "now"

## Default Monetization

- **ON** (even if revenue is small — turns on ads = YouTube considers the channel "serious")

## Default Category

- **Howto & Style** (tests better than "People & Blogs" for realtor content — Retention Rabbit data suggests Education/How-To framing)

## Default Comments

- **All comments · Hold potentially inappropriate comments for review**

## Default License

- **Standard YouTube license**

## Default Language & Location

- **English (US)**
- **Location: Temple, Texas** (enables local search pickup)

## Default End Screen Template

Create once in YouTube Studio:
1. **"Subscribe"** element in bottom-left
2. **"Latest video"** in center (auto-rotates)
3. **"Best video for viewer"** in bottom-right (auto-selects highest-retention next watch)

## Default Card Templates

Add at **6:00 mark** of long-forms (mid-video slump mitigation per Retention Rabbit data):
- Link to a related Temple video (playlist or single)

## Default Playlists

Add every new video to a playlist at upload. Playlists should be:
- **"Living in Temple TX"** (all relocator/buyer content)
- **"Temple TX Neighborhoods"** (all neighborhood tours)
- **"Military & Fort Hood Moves"** (PCS / military-specific content)
- **"Temple TX Market Updates"** (monthly market videos)
- **"First-Time Buyer Guide"** (buyer education)
- **"Investor Content"** (if you keep everything on one channel — otherwise separate channel per CLAUDE.md)

---
---

# SECTION 4 — TOP 10 VIDEOS TO DO NEXT (Ranked by Impact)

After your first 4 videos ship (Warning 3 Mistakes / Map Tour / Ranked / PCS), here are the next 10. Each analyzed against:
- What other small-city realtors are doing
- What Temple-specific gap exists
- Your filming constraints

### 1. "What $300K Actually Buys in Temple TX (vs Austin, Killeen, Waco)" — ⭐⭐⭐⭐⭐
- **Format:** 11-13 min long-form
- **Filming:** OUT AND ABOUT — drive to 3-4 properties at same price point in each city. Show 30 seconds of each outside + drone if weather cooperates.
- **Why:** Comparison format = 100x view potential per BIGVU data. Single price anchor = clean hook. Covers 3 adjacent markets → triple the audience.
- **Other realtors doing this well:** Real Estate Steph (Killeen), Living in Austin Texas
- **Shot list:** 12 exterior shots (3 per city × 4 cities), 6 driving shots between them, 2 talking-head close-ups for transitions
- **Time:** 1 filming day + 3 hours edit

### 2. "Temple TX 5-Year Price Prediction — Am I Wrong?" — ⭐⭐⭐⭐⭐
- **Format:** 10-12 min face-to-camera + data visuals
- **Filming:** Studio / desk setup. Whiteboard or iPad sketching predictions.
- **Why:** Prediction content gets shared, disputed, commented. Fuel for algo. "Am I wrong?" invites engagement.
- **Other realtors doing this well:** Graham Stephan, Jason Walter, most property prediction channels
- **Shot list:** 1 wide desk shot · 3 whiteboard close-ups · 4-5 data graphics overlays
- **Time:** 2 hours film + 3 hours edit

### 3. "Academy ISD 4-Day School Week Parent Guide" — ⭐⭐⭐⭐⭐
- **Format:** 8-10 min long-form
- **Filming:** OUT AND ABOUT — film at Academy ISD school entrance (public exterior only, no kids in frame), drive through Academy-zoned neighborhoods, show real calendar on tablet.
- **Why:** Zero realtor competition on this. Commenters literally asked.
- **Shot list:** 3 school exterior shots · 2 neighborhood drive-throughs · 1 calendar close-up · 2 talking head
- **Time:** 2 hours film + 2 hours edit

### 4. "I Moved to Temple TX 3 Years Ago — Here's What Surprised Me" — ⭐⭐⭐⭐⭐
- **Format:** 8-10 min personal lens long-form
- **Filming:** MUCH OUT AND ABOUT — film at 6-8 specific spots around Temple that represent each "surprise." Coffee shop you love, park, trailhead, specific restaurant, etc.
- **Why:** Authenticity hook. Personal lens. Breaks pattern of "agent giving advice."
- **Other realtors doing this well:** Living in Austin Texas (this format has 500K+ views consistently)
- **Shot list:** 8 location exteriors · Taylor walking into frame at each · 3 close-up face moments for punctuation
- **Time:** 3 hours film (spread across a whole Temple day) + 3 hours edit

### 5. "Living in Temple TX 2026 — Summer Update" — ⭐⭐⭐⭐
- **Format:** 10-12 min long-form (sequel to your 4,065-view flagship)
- **Filming:** Mix — half interior narration, half exterior B-roll
- **Why:** Re-serves your flagship. YouTube loves sequel / "update" content on proven topics.
- **Time:** 2 hours film + 2 hours edit

### 6. "The Homeowner's Insurance Trap in Temple TX (What Nobody Tells You)" — ⭐⭐⭐⭐
- **Format:** 8-10 min long-form
- **Filming:** Desk + graphics for math, 2-3 exterior shots of properties in flood zones (from public streets only)
- **Why:** Replaces your 56-view Short on the same topic. Consumer-protection angle = high retention.
- **Time:** 2 hours film + 2 hours edit

### 7. "The Warning Every Temple Buyer Ignores (Before S 11th Street)" — ⭐⭐⭐⭐
- **Format:** 6-8 min long-form
- **Filming:** OUT AND ABOUT — film on S 11th and adjacent streets. Show actual infrastructure issues (drainage, aging curbs) from public-view angles only. Drive the block.
- **Why:** Block-specific honest call. Other agents won't do this. "Warning" CTR trigger.
- **Sensitivity note:** Be precise — never disparage specific homes or homeowners. Focus on infrastructure facts.
- **Time:** 1 hour film + 2 hours edit

### 8. "Best Temple TX Neighborhood for Under $250K (2026)" — ⭐⭐⭐⭐
- **Format:** 6-8 min long-form
- **Filming:** OUT AND ABOUT — tour Cimmaron + Sage Meadows + possibly Canyon Ridge entry tier. One-day drive.
- **Why:** Budget-specific anchor. First-time buyer audience. Evergreen.
- **Time:** 2 hours film + 2 hours edit

### 9. "Temple TX vs Bryan/College Station — Which Wins for 2026?" — ⭐⭐⭐⭐
- **Format:** 10-12 min long-form comparison
- **Filming:** Mostly desk + data. Some B-roll from Taylor's existing Temple footage + stock of Bryan/CS if you can't drive there.
- **Why:** Bryan/CS is the next-up comparison market for Central TX relocators (Texas A&M pull). Zero local agent covers it from Temple angle.
- **Time:** 1 hour film + 3 hours edit

### 10. "The Temple TX Sub-Markets Nobody's Talking About (Little River, Holland, Salado Edges)" — ⭐⭐⭐
- **Format:** 10-12 min long-form
- **Filming:** OUT AND ABOUT — drive between Little River, Holland, and Salado-adjacent Temple pockets. Half day of driving + filming.
- **Why:** Expansion beyond Temple-proper captures search volume you don't currently get. Taxes, schools, commute to Temple/Fort Hood.
- **Time:** 3 hours film + 3 hours edit

---
---

# SECTION 5 — EQUIPMENT INVESTMENTS (What Actually Moves the Needle)

Ranked by ROI. **Start at tier 1 — do NOT buy tier 3 before tier 1.**

### Tier 1: Essential ($180-250 total) — Buy This Week

| Item | Model / Option | Cost | Why |
|---|---|---|---|
| **Lav mic kit** | Rode Wireless Me (dual-channel) OR DJI Mic 2 | $150-250 | Audio quality matters MORE than video quality for retention. Taylor's comments already flagged music/audio issues. |
| **Phone tripod + bluetooth remote** | Manfrotto PIXI EVO + $15 remote | $30 | Can't hand-hold out-and-about shots without stabilization. |

**That's it for tier 1.** Two purchases. Takes retention from "muddy" to "professional."

### Tier 2: Upgrade ($400-700 total) — After 10 Videos Shipped

| Item | Model | Cost | Why |
|---|---|---|---|
| **Mirrorless camera** | Sony ZV-E10 (body only) OR Fujifilm X-S10 | $500-700 | Better autofocus for run-and-gun. Swappable lens. Way better low-light than iPhone for indoor shots. |
| **Standard zoom lens** | Sony 16-50mm kit (if bundle) OR Sigma 18-50 f/2.8 | Often bundled | Covers wide establishing → mid-close portrait |
| **Ring light or key light** | Godox SL60W | $150 | Indoor talking-head shots look cinematic, not YouTube-y |

**Skip:** Drone. Your iPhone + Temple Map Tour HTML covers 90% of aerial needs. Drones add complexity, regulation (FAA Part 107), and editing overhead. Revisit in 6 months only if you're hitting 10K+ views consistently.

### Tier 3: Production Polish ($500-1,200 total) — Only After Channel Hits 5K Subs

| Item | Model | Cost | Why |
|---|---|---|---|
| **Gimbal** | DJI RS 4 Mini | $400 | Smooth walking shots matter when you're out-and-about 3+ days/week |
| **External SSD** | Samsung T7 2TB | $150 | Fast offload from camera, faster CapCut rendering |
| **Second camera angle** | Used Sony a6400 + 35mm prime | $500-700 | B-camera for multi-angle sit-down interviews (client testimonials — Video #13 in New 20) |
| **Softbox light kit** | Neewer 2-softbox kit | $120 | Client testimonial / interview quality jump |

### What NOT to Buy (Yet or Ever)

- **Expensive monitor/recorder (Atomos, etc.)** — Over-engineered for solo creator
- **$1K+ broadcast mic (Shure SM7B, etc.)** — You're not doing podcast. Lav is right.
- **Teleprompter hardware** — BIGVU or PromptSmart app on phone is 95% as good
- **Ring light over $40** — Diminishing returns
- **Professional color grading software** — CapCut's built-in is plenty for 25% retention targets

### Total recommended Year-1 investment: $180-250 (Tier 1 only · the rest can wait)

---
---

# SECTION 6 — FILMING TIPS (Per Video + General)

## General: Out-and-About Shot Formula (MATCHES YOUR INSTINCT)

You're right that being out-and-about makes the videos better. The research backs this up — **"on-location, non-studio" shots correlate with higher retention**, especially in real estate where viewers want proof of local expertise.

**The 3-shot formula for every on-location segment:**

1. **Establish** — wide shot of the location (you entering frame or just the place)
2. **You talking** — mid-shot, lav mic on, face to camera, talking about this specific spot
3. **Detail** — close-up of something specific you're pointing at (a sign, a house feature, a view)

Repeat this 3-shot cycle every 60-90 seconds of long-form content. That's your pattern-interrupt cadence per Retention Rabbit research.

## Per-Video Filming Tips

### Warning 3 Mistakes — TEST PIPELINE FIRST
- **Day 1 Saturday:** Walk a South Temple street where you'd flag infrastructure issues. Film at 2 PM.
- **Day 2 Monday 6:45 AM:** Same street, morning rush. This contrast IS the hook payoff.
- **Day 3:** Desk + FEMA screen cap + builder model home drive-by
- **Takes:** Film each mistake in one take if you can — no hard cuts mid-mistake. Viewers can tell.

### Temple Map Tour — LOW FILMING LOAD
- You're mostly off-camera here (the map is the B-roll)
- Film yourself ONLY for the hook (0:00-0:15) and CTA (9:50-10:00)
- Suggestion: Film both on a street corner in Canyon Ridge or Bella Terra — gives you a real-neighborhood anchor

### Ranked Worst to Best — OUT AND ABOUT CRITICAL
- For each tier, film yourself at one neighborhood IN that tier while explaining the ranking
- Tier F: film near (not at) an infrastructure-challenged area from public angle
- Tier S: film at Canyon Ridge park or Bella Terra entrance — show where "best" actually looks
- **Creative move:** Hold up a physical printed tier-list card in the thumbnail shot

### PCS to Fort Hood (or Cavazos) — MILITARY-RESPECTFUL
- Film with Fort Hood gate visible in background (from public road — never cross onto installation without media escort)
- Film on I-14/US-190 commute corridor (use dash cam OR have someone drive while you talk from passenger)
- Bella Terra exterior for "where BSW docs live" b-roll

### Academy ISD 4-Day Week — PUBLIC SPACES ONLY
- School exterior shots on Saturday or Sunday (no kids in frame, no identifying students)
- Drive through residential Academy-zoned streets weekday morning to show the vibe
- Coffee shop or park shots to imply "this is what families do here"

### 5-Year Price Prediction — STUDIO
- Whiteboard or iPad sketch format works great for this
- Keep background simple — kitchen island or home office
- Film at golden hour (soft natural light) if possible

### "3 Years Ago Surprised Me" — ALL OVER TEMPLE
- Plan a single-day shoot: 6-8 Temple locations, 10 min each
- Sample spots: Wildfire Coffee, Miller Park, Temple Mall's secret courtyard, a specific restaurant you recommend, etc.
- Take natural walking-to-camera entries — feels authentic

### Cost of Living (Re-shoot) — DESK + B-ROLL MIX
- Hold actual bills in hand (hide account numbers) — that's the hook
- Cut between you holding physical paper and B-roll of Temple exteriors (HEB, utility company buildings, etc.)

### Homeowner's Insurance Trap — DESK + DRIVE
- Desk: scroll through actual insurance quotes on screen (blur names)
- Drive: pan past flood zone properties (exterior only, never on private property)

### Temple vs Waco / Bryan-CS — DRIVE-DAY SHOOT
- Single day, 1 shot in each city, Temple first to establish baseline
- Gas stations, main streets, signature intersections
- Keep comparison visual (split screen or A/B framing) in post

### Hidden Gems Reframed Shorts (5 Shorts)
- Film 5 neighborhoods in one afternoon, 7 minutes each
- One take per Short, walking shot
- Use existing $142/sqft-style hook formula but reframe title

## Universal Filming Rules

1. **Golden hour matters.** 7-8 AM and 5:30-7 PM are your prime filming windows. Midday harsh sun = worst retention per testing.
2. **Never film talking-head in direct sunlight.** Squinting = unretained viewers. Shade or overcast only.
3. **Always carry a small whiteboard or dry-erase cards.** Instant visual aids. Adds production value. Costs $12.
4. **Film 20% more than you need.** Cuts your edit time in half because you have options.
5. **"Three angles" rule.** For any one takeaway, film wide / mid / close. Cutting between them in post = instant retention bump.
6. **Pocket a lav mic at all times once you have it.** Opportunity shots happen — client saying something great, a neighbor mentioning a feature. Can't redo those.

---
---

# SECTION 7 — DAILY PRACTICE ROUTINE (30 min/day)

The difference between 12% retention and 25% retention isn't script quality — it's delivery. And delivery is a practiced skill.

## The Daily 30

**Morning (15 min · before coffee goes cold):**

1. **5-min vocal warm-up** (4 min of exercises + 1 min reading):
   - Lip trills for 1 min (sounds silly, works — google "lip trill vocal warmup")
   - Humming scales for 1 min
   - Tongue twisters for 1 min ("red leather yellow leather" x10 fast)
   - "Ma-May-Me-My-Mo-Moo" articulation × 6 sets
   - Read one paragraph from a Temple listing description OUT LOUD, like you're on camera
2. **5-min teleprompter read-along** — Open BIGVU (or any teleprompter app) on phone, load one of the 4 scripts Claude wrote, read the first section at speaking pace. Don't record. Just read.
3. **5-min "one-take hook drill"** — Write one new hook idea for any topic on your list. Say it out loud 3 times until it feels natural. Text it to yourself for the archive.

**Afternoon (10 min · mid-day or end-of-day):**

4. **10-min script memorization** — Take the next section of an upcoming video script. Read it 3 times. Then try to say the key points without looking. You don't need to memorize verbatim — just the key 5-6 points in order.

**Evening (5 min · wind-down):**

5. **5-min competitor watch** — Watch one short-city realtor YouTube video that's performing well (Jackson Wilkey, Real Estate Steph, Living in Austin Texas, etc.) on 1.25x speed. Note ONE thing they do that you could steal. Write it in your notes app with the video URL.

## Weekly Practice (1 hour on Sunday)

- **30-min "cold call" record** — Pick ANY topic. Hit record. Talk for 5 min without a script, as if filming. Watch it back. Find ONE thing to fix next week. You don't have to publish this — it's practice.
- **30-min title/thumbnail A/B** — Look at your top 5 underperforming videos. For each, come up with 3 new title variants. Pick the best. Change it in Studio.

## How This Integrates with Claude

Option A: Claude reminds you daily via Telegram (requires a cron hook).
Option B: The **skill file** below — you invoke `/yt-daily` each morning and Claude gives you today's specific practice drill.

Option B is in Section 9.

---
---

# SECTION 8 — WHAT OTHER REALTORS DO (That You're Not Doing)

Pattern-match the data. These are moves from top small-city realtor channels applied to your situation.

| Move | Who Does It Well | Apply to Your Channel |
|---|---|---|
| Pinned comment with lead magnet + question | Jackson Wilkey (Reno) | Every video — ask the comment question first, lead magnet link second |
| Playlist-driven binge watching | Living in Austin Texas | Build 6 playlists (Section 3) — route end screens playlist-to-playlist |
| Response-video format (reacting to comments) | Real Estate Steph | Quarterly "I read every comment — here's what you asked" video |
| Cross-city guest appearances | Multiple small-city realtors | Collab with one Killeen agent + one Waco agent for split-city videos (audience swap) |
| Client story interviews (fear → outcome format) | BIGVU case studies | Film one per quarter — permission required, but converts massively |
| Consistent Tuesday 8 AM CT upload time | Most growing small-city channels | Lock 8 AM Tuesday as your long-form upload slot. Algo rewards consistency. |
| Monthly market update format same EVERY month | Jason Walter (Sacramento) | Always: start with 3 headline stats, middle with neighborhood spotlight, end with "buy or wait?" answer |
| "Why I left [Big City] for [Small City]" content | Living in Boise, Living in Chattanooga | Film "Why I Didn't Stay in Austin" — relatable for Austin transplants moving to Temple |
| Map walkthroughs (you're now set up for this) | Jackson Wilkey's "Reno Map Tour" did 250K+ views | Your Temple Map Tour is your version — SHIP IT |
| Data-as-content (charts + stats) | Graham Stephan | Sprinkle 2-3 visual stat callouts per long-form video — CapCut can do this |
| Transparent income/commission videos | Many realtor channels | Consider quarterly "here's what I closed and what I learned" video — builds trust, shareable |

---
---

# SECTION 9 — THE SKILL FILE (Reusable Daily/Weekly Tool)

I'll create `/yt-daily` and `/yt-optimize` skill files so you can invoke them anytime:

- `/yt-daily` — Get today's specific practice drill (5 exercises pulled from the Daily 30)
- `/yt-optimize` — Claude pulls latest channel stats, identifies the single biggest optimization this week, outputs action

Skill file coming in the next write (separate file for cleanliness). Location: `~/.claude/skills/yt-daily/SKILL.md` and `~/.claude/skills/yt-optimize/SKILL.md`.

---
---

# SECTION 10 — HONEST LIMITS

- **YouTube Analytics API access blocked.** All retention percentages in this plan are from Retention Rabbit benchmarks or your VidIQ audit — not your real curves. First Phase 4 priority is getting API access so we can iterate on real data.
- **Equipment pricing is April 2026 street prices.** Verify at B&H Photo or Amazon before buying — prices drift.
- **Top 10 video list is my opinion.** If you've gotten signal from comments or client conversations that another topic matters more, reorder.
- **"2-3 leads/week" target is ambitious.** Could be more if Temple Map Tour pops; could be 1-2 if retention fixes take longer to kick in. Measure at day 60 and adjust.
- **I can't monitor your uploads automatically** — the skill files require you to invoke them. Next improvement: wire them into your Telegram morning brief via a cron (future session).

---
---

# STOP CHECKLIST

- **Files changed:**
  - `claude-social-media-manager/output/audits/youtube-ultraplan-2026-04-20.md` (this file, created)
  - `~/.claude/skills/yt-daily/SKILL.md` (next write — daily practice skill)
  - `~/.claude/skills/yt-optimize/SKILL.md` (next write — weekly optimizer skill)
- **Verification run:** 4 Firecrawl searches (realtor equipment · YouTube Studio settings · top small-city realtor channels · vocal warmup routines) · cross-referenced prior channel data pull · mapped against prior audit + retention research deliverables
- **Unresolved risk:** (1) Fort Hood vs Fort Cavazos naming decision blocks PCS video from publish-ready state. (2) Equipment tier 1 purchase ($180-250) should happen this week — audio quality is the #1 unfixable-in-post variable. (3) This plan assumes you'll actually calendar-block filming days; without that, everything downstream fails.
- **Rollback path:** `rm /Users/taylordasch_1/claude-social-media-manager/output/audits/youtube-ultraplan-2026-04-20.md` + remove skill files if created
- **Next physical action:** Open YouTube Studio. Retitle 8 scheduled videos. 20 minutes. Before lunch today.
- **BSW Next:** Video #7 (BSW Residency) is queued in the New 20 list. This ultraplan does NOT pull it forward — it's still slotted for Weeks 9-10. The PCS video (once renamed if needed) is your nearest BSW-adjacent asset and should ship first to test the military/medical audience response before committing to the BSW-specific long-form. Keep the Matt Levant (Acre Mortgage) pinned-comment play ready for whichever military/medical video lands first.
