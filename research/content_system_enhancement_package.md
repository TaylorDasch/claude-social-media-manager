# CONTENT SYSTEM ENHANCEMENT PACKAGE
## Claude Social Media Manager + Opus Project Upgrades
### Taylor Dasch | EG Realty | March 2026

---

## HOW TO USE THIS DOCUMENT

This package contains **3 categories** of additions:

1. **New docs/skills for your Claude Code content project** (`claude-social-media-manager/`) — reference files that make every skill smarter
2. **New docs for this Opus project** — strategic references that improve daily planning and content decisions
3. **Ideas that require execution** — YouTube growth levers, lead gen plays, and content format experiments ranked by ROI

Everything below is designed to either (a) make Claude produce better content faster, or (b) directly generate leads from your YouTube channels.

---

# PART 1: NEW DOCS FOR CLAUDE CODE CONTENT PROJECT

These go in your `claude-social-media-manager/` directory as reference files that any skill can pull from during execution.

---

## DOC 1: `VIDEO-SCRIPT-FORMULAS.md`

**What it does:** Gives Claude a library of proven script structures for every video type you film. Instead of generating scripts from scratch each time, Claude pulls the right formula and fills it with your data.

**Why it matters:** Right now your /produce and /deal-of-the-week skills generate scripts, but they don't have a codified library of what WORKS for Temple TX content specifically. This doc encodes your best-performing structures.

### CONTENTS TO BUILD:

```markdown
# VIDEO SCRIPT FORMULAS — Taylor Dasch Content Library

## FORMAT 1: DEAL BREAKDOWN (8-12 min)
Best for: Deal of the Week, property walkthroughs with numbers
Structure:
- 0:00-0:25 — NEGATIVE HOOK (state what's wrong or surprising about the deal)
- 0:25-1:30 — PROPERTY CONTEXT (neighborhood, year built, condition, why it matters)
- 1:30-4:00 — THE NUMBERS (purchase price → down payment → PITI → rent → cash flow)
- 4:00-6:00 — THE RISK SECTION (foundation age, HOA, insurance, what could go wrong)
- 6:00-8:00 — THE VERDICT (would I buy this? at what price? for which strategy?)
- 8:00-9:00 — COMPARISON CONTEXT (how this stacks vs your buy box, vs last week's deal)
- 9:00-end — CTA (specific: "if you want me to run numbers on a property like this...")
Filming style: Desk + screen share for numbers, cut to property B-roll during context
Retention lever: Put the verdict LAST — tease it in the hook ("I'll tell you if I'd buy this")

## FORMAT 2: NEIGHBORHOOD TOUR (10-15 min)
Best for: Living in Temple channel, relocation buyers, BSW/military
Structure:
- 0:00-0:20 — PROBLEM HOOK ("Moving to Temple and don't know where to live?")
- 0:20-1:00 — THE 3-SENTENCE VERDICT (give the answer immediately — don't make them wait)
- 1:00-3:00 — COMMUTE TEST (real-time drive to BSW or Fort Hood gate, show the clock)
- 3:00-5:00 — SCHOOLS (specific ratings, not just district name)
- 5:00-7:00 — PRICE RANGES + WHAT YOU GET (examples at low/mid/high end of neighborhood)
- 7:00-9:00 — THE NEGATIVES (mandatory — this is your differentiator)
- 9:00-11:00 — WHO THIS NEIGHBORHOOD IS FOR (persona match: investor? BSW resident? family?)
- 11:00-end — CTA + related video card
Filming style: Drive-through POV + walk-and-talk at key locations + desk for data
Retention lever: "Red flags" section — tease in hook, deliver at 7:00

## FORMAT 3: NEGATIVE HOOK / "TEMPLE TRAP" (5-8 min)
Best for: Both channels, algorithm boost, trust building
Structure:
- 0:00-0:15 — BOLD NEGATIVE STATEMENT ("Don't buy on south even streets in Temple")
- 0:15-1:00 — WHY (data-backed explanation of the problem)
- 1:00-3:00 — THE EVIDENCE (specific examples, addresses if appropriate, real numbers)
- 3:00-5:00 — WHAT TO DO INSTEAD (the alternative that works)
- 5:00-end — BROADER LESSON (what this teaches about Temple/investing in general)
Filming style: Desk with graphics, or on-location at the problem area
Retention lever: Controversy in the title + thumbnail drives clicks; substance retains

## FORMAT 4: EXPLAINER / EDUCATIONAL (6-10 min)
Best for: Physician loan, BAH calculator, tax protest, BRRRR explanation
Structure:
- 0:00-0:20 — OUTCOME HOOK ("This loan lets you buy a house with zero dollars down")
- 0:20-1:30 — WHO THIS IS FOR (specific persona)
- 1:30-4:00 — HOW IT WORKS (step-by-step, screen share if math involved)
- 4:00-6:00 — THE CATCH (what they don't tell you — again, your differentiator)
- 6:00-8:00 — REAL EXAMPLE (actual numbers from Temple market)
- 8:00-end — NEXT STEPS CTA
Filming style: Desk + screen share heavy, B-roll of relevant locations
Retention lever: "The catch" section — everyone clicks to hear what's wrong

## FORMAT 5: YOUTUBE SHORT / TIKTOK (21-45 sec)
Best for: Algorithm discovery, repurposed clips, quick data drops
Structure:
- 0:00-0:03 — PATTERN INTERRUPT (bold statement, visual change, or question)
- 0:03-0:20 — ONE SINGLE POINT (one stat, one fact, one tip — never two)
- 0:20-0:30 — RESTATE + IMPLICATION ("which means if you're investing in Temple...")
- 0:30-0:45 — SOFT CTA or loop back to hook
Filming style: Vertical, face-to-camera, fast cuts, text overlays for numbers
Retention lever: Loop structure — last sentence connects to first

## UNIVERSAL RULES FOR ALL FORMATS:
1. First sentence is NEVER "hey guys welcome back" — it's always a hook
2. Every script includes at least ONE specific number in the first 15 seconds
3. Every script includes at least ONE negative/honest moment
4. CTA is SPECIFIC not generic ("DM me your buy box" not "like and subscribe")
5. Temple-specific data beats generic advice — always localize
6. Tease the most interesting part early, deliver it late (retention architecture)
```

---

## DOC 2: `SCHEMA-LIBRARY.md`

**What it does:** Pre-built JSON-LD templates for every page and video type on templetxhomes.net. Claude grabs the right template and fills in the variables instead of building schema from scratch.

**Why it matters:** Schema markup is one of your biggest gaps (still not fully deployed site-wide). Having templates ready means every page build or video deployment includes schema automatically.

### CONTENTS TO BUILD:

```markdown
# SCHEMA-LIBRARY — Pre-Built JSON-LD Templates

## TEMPLATE 1: VideoObject (Every Video Embed)
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "[VIDEO_TITLE]",
  "description": "[2-3 sentence data-rich description]",
  "thumbnailUrl": "[YOUTUBE_THUMB_URL]",
  "uploadDate": "[YYYY-MM-DD]",
  "duration": "[PT#M#S]",
  "contentUrl": "[YOUTUBE_URL]",
  "embedUrl": "https://www.youtube.com/embed/[VIDEO_ID]",
  "publisher": {
    "@type": "RealEstateAgent",
    "name": "Taylor Dasch",
    "url": "https://templetxhomes.net"
  },
  "about": {
    "@type": "Place",
    "name": "[NEIGHBORHOOD or CITY]",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "[Temple/Belton/Killeen]",
      "addressRegion": "TX",
      "postalCode": "[ZIP]"
    }
  }
}

## TEMPLATE 2: FAQPage (Every Content Page)
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[H2 QUESTION TEXT]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[FIRST 2-3 SENTENCES AFTER H2 — data-rich answer]"
      }
    }
  ]
}

## TEMPLATE 3: RealEstateAgent (Homepage + About)
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Taylor Dasch",
  "alternateName": "Deals with Dasch",
  "url": "https://templetxhomes.net",
  "telephone": "+1-254-718-4249",
  "email": "dealswithdasch@gmail.com",
  "image": "[HEADSHOT_URL]",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Temple",
    "addressRegion": "TX",
    "postalCode": "76502",
    "addressCountry": "US"
  },
  "areaServed": [
    {"@type": "City", "name": "Temple", "sameAs": "https://en.wikipedia.org/wiki/Temple,_Texas"},
    {"@type": "City", "name": "Belton", "sameAs": "https://en.wikipedia.org/wiki/Belton,_Texas"},
    {"@type": "City", "name": "Killeen"},
    {"@type": "City", "name": "Harker Heights"}
  ],
  "knowsAbout": [
    "Buy-and-hold rental property investing",
    "Baylor Scott & White medical professional relocation",
    "Fort Hood military relocation",
    "Physician home loans",
    "BRRRR strategy",
    "Mid-term rentals",
    "Bell County property tax protest",
    "1031 exchange",
    "DSCR loans"
  ],
  "memberOf": {
    "@type": "Organization",
    "name": "EG Realty"
  },
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "license",
    "recognizedBy": {
      "@type": "Organization",
      "name": "Texas Real Estate Commission"
    }
  }
}

## TEMPLATE 4: LocalBusiness + Review Aggregate (Investing/BSW pillar pages)
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Taylor Dasch - EG Realty",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "[CURRENT_REVIEW_COUNT]",
    "bestRating": "5"
  }
}

## TEMPLATE 5: Article (Blog posts / Deal of the Week writeups)
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[H1 TITLE]",
  "author": {
    "@type": "Person",
    "name": "Taylor Dasch",
    "url": "https://templetxhomes.net",
    "jobTitle": "REALTOR & Real Estate Investor",
    "worksFor": {"@type": "Organization", "name": "EG Realty"}
  },
  "publisher": {
    "@type": "Organization",
    "name": "Temple TX Homes",
    "url": "https://templetxhomes.net"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "about": {
    "@type": "Place",
    "name": "[TOPIC LOCATION]"
  }
}

## TEMPLATE 6: HowTo (Calculator pages, guide pages)
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[HOW TO TITLE]",
  "step": [
    {
      "@type": "HowToStep",
      "name": "[STEP NAME]",
      "text": "[STEP DESCRIPTION]"
    }
  ]
}

## DEPLOYMENT RULES:
1. Every page gets AT LEAST FAQPage schema
2. Every page with video gets FAQPage + VideoObject
3. Homepage and about page get RealEstateAgent
4. Pillar pages (investing, BSW) get Article + FAQPage
5. All schema goes in AgentFire Spark/Coder blocks — NEVER paste into text blocks
6. Validate at validator.schema.org before publishing
7. Stack multiple schema types using @graph when a page needs 3+
```

---

## DOC 3: `TEMPLE-TX-DATA-VAULT.md`

**What it does:** A single-source reference for every recurring data point Claude needs when generating content. Eliminates the need to look up the same stats repeatedly and prevents conflicting numbers across content.

**Why it matters:** Data consistency across videos, pages, and social posts is a core AEO signal. If your BAH rate is $1,920 in one video and $1,950 in another, AI loses confidence.

### CONTENTS TO BUILD:

```markdown
# TEMPLE TX DATA VAULT — Single Source of Truth
# Last verified: [DATE]
# UPDATE PROTOCOL: Review monthly. Flag any data point older than 90 days.

## MILITARY / FORT HOOD
- BAH E-6 w/dependents: $[CURRENT] /mo
- BAH E-7 w/dependents: $[CURRENT] /mo
- BAH O-3 w/dependents: $[CURRENT] /mo
- BAH O-5 w/dependents: $[CURRENT] /mo
- Fort Hood total military population: ~[CURRENT]
- Fort Hood total economic impact: ~$[CURRENT] billion/yr
- Gate commute times: [North gate from Temple: X min, South gate from Killeen: X min]

## BSW MEDICAL
- BSW Temple campus total employees: 8,800+
- PGY-1 resident salary: $[CURRENT]/yr
- PGY-2 salary: $[CURRENT]/yr
- PGY-3 salary: $[CURRENT]/yr
- BSW Level 1 Trauma Center: Yes (one of X in Texas)
- Trauma surgeon 15-min OR mandate: Yes
- Match Day: Third Friday of March (typically March 20-21)
- Residency start date: Late June / early July
- Physician loan partner: Extraco Bank (0% down)

## MARKET DATA (update monthly)
- Median home price Temple: $[CURRENT]
- Median home price Belton: $[CURRENT]
- Median home price Killeen: $[CURRENT]
- Median home price Harker Heights: $[CURRENT]
- Average days on market: [CURRENT]
- Active inventory: [CURRENT] listings
- Investor buy box: $140K-$260K
- $140K = MTR entry point
- Target cap rate range: 6-8%
- Bell County effective tax rate: ~2.1% (estimated — do NOT display as exact)

## PROPERTY TAX
- Bell County CAD typically appraises below purchase price
- Homestead exemption: $100K off school taxes (state) + local exemptions vary
- Protest deadline: May 15 or 30 days after notice (whichever is later)
- Effective rate ~2.1% is more realistic than 2.4% for investor pro formas
- DO NOT hardcode specific tax rates in evergreen content

## POPULATION / GROWTH
- Temple population: ~[CURRENT]
- Bell County population: ~[CURRENT]
- Projected population growth: [CURRENT]% (cite source)
- ⚠️ DO NOT USE the 5,101-unit housing deficit stat — it's debunked (data scraping error)

## KEY EMPLOYERS
- Baylor Scott & White (8,800+)
- Fort Hood (largest active-duty armored post)
- McLane Company (HQ in Temple)
- Wilsonart International
- META/Rowan data center projects (emerging)

## SCHOOL DISTRICTS
- Temple ISD: [accountability rating]
- Belton ISD: [accountability rating]
- Killeen ISD: [accountability rating]

## DISTANCES / COMMUTES
- Temple to Austin: ~65 miles, ~1hr 10min
- Temple to Waco: ~35 miles, ~40min
- Temple to DFW: ~135 miles, ~2hr 15min
- BSW to Lake Pointe: 7.0 miles, ~14 min
- BSW to Dawson Ranch: [X] miles, ~[X] min
- BSW to Canyon Creek: [X] miles, ~[X] min

## CONTENT RULES (Reminders for Claude)
- Never use "turnkey" — say "buy-and-hold investors"
- Never use "Fort Hood" — always "Fort Hood"
- Never use "hidden gem" or "charming community"
- Never hardcode interest rates in evergreen content
- Never cite the 5,101-unit housing deficit
- Foundation issues: only mention on pages for Western Hills, River Oaks, or the dedicated foundation page
```

---

## DOC 4: `YOUTUBE-GROWTH-PLAYBOOK.md`

**What it does:** A reference doc Claude can pull from when generating YouTube metadata, planning content calendars, or suggesting video topics. Encodes YouTube algorithm mechanics specific to real estate.

### CONTENTS TO BUILD:

```markdown
# YOUTUBE GROWTH PLAYBOOK — Real Estate / Hyperlocal
# Updated: March 2026

## ALGORITHM FUNDAMENTALS (What Actually Drives Growth)
1. Click-through rate (CTR) — thumbnail + title are 80% of the game
2. Average view duration (AVD) — YouTube promotes videos that retain past 50%
3. Session time — videos that lead to MORE YouTube watching get boosted
4. Subscriber conversion — videos that convert viewers to subs signal quality

## TITLE FORMULAS THAT WORK FOR REAL ESTATE
- [NEGATIVE] + [LOCATION]: "Don't Buy a House in Temple TX Until You Watch This"
- [SPECIFIC NUMBER] + [OUTCOME]: "$187K Rental Property: Full Cash Flow Breakdown"
- [COMPARISON]: "Temple vs Belton TX — Which Is Better for Investors?"
- [QUESTION] + [ANSWER TEASE]: "Is Temple TX a Good Place to Invest? (I've Done 100+ Deals)"
- [YEAR] + [SPECIFIC TOPIC]: "Best Neighborhoods in Temple TX (2026 Update)"

## TITLE RULES
- Always include "Temple TX" or the specific city in the title
- Front-load the most interesting word (numbers, negatives, specifics)
- Under 60 characters for mobile display
- Never use ALL CAPS on more than 2 words
- Year-stamp time-sensitive content

## THUMBNAIL RULES
- High contrast (dark background + bright text works for your brand)
- Maximum 4-5 words on thumbnail
- Face showing emotion > no face (but NOT the "agent pointing at house" trope)
- Use emerald (#059669) for positive indicators, red for negative/warning
- Property photo + overlaid number = highest CTR for deal breakdowns
- Split-frame (before/after, vs comparison) = highest CTR for comparisons

## DESCRIPTION STRUCTURE (7 sections, every video)
1. Answer-first paragraph (data-rich, 2-3 sentences — this is what AI extracts)
2. Context paragraph (why this video matters, who it's for)
3. Timestamps (every section break)
4. Areas/neighborhoods mentioned (with links to templetxhomes.net pages)
5. Key data points repeated as text (redundant with video — intentional for AI)
6. About Taylor section (boilerplate with credentials)
7. Contact + links (templetxhomes.net, Calendly, social)

## RETENTION ARCHITECTURE
- Pattern interrupt every 60-90 seconds (visual change, topic shift, question)
- Tease upcoming section: "In a minute I'll show you the red flags..."
- Put your strongest content at the 40-60% mark (where most drop-off happens)
- End with curiosity for next video (drives session time): "Next week I'm breaking down..."

## WHAT TO FILM VS. WHAT TO SKIP
### HIGH ROI (film these):
- Deal of the Week (recurring, builds habit)
- Neighborhood tours with commute tests (evergreen, high search volume)
- "Where NOT to invest" negative hooks (algorithm boost + trust)
- BSW-specific relocation guides (timed to Q4 and Match Day)
- Investor strategy explainers with Temple numbers (attracts OOS investors)

### LOW ROI (skip these):
- "Day in the life" vlogs (low search intent, attracts wrong audience)
- Generic market updates without specific data
- Listing tours without analytical framing
- "Top 10" lists without original data
- Anything a Zillow listing page already answers

## YOUTUBE SHORTS STRATEGY
- Repurpose the single most interesting 30-sec clip from every long-form video
- Shorts title = search-optimized (YouTube Shorts IS a search engine)
- Shorts description includes "Full video: [LINK]" to drive traffic to long-form
- Post Shorts 24-48 hours AFTER the long-form video (gives long-form a head start)
- Best Shorts: one shocking stat, one bold opinion, one "did you know"

## COMMUNITY POSTS (Underutilized Growth Lever)
- Post 2-3x/week between video uploads
- Types: polls ("Which neighborhood should I break down next?"), 
  data drops (one stat + one sentence), behind-the-scenes (filming day photos)
- Community posts keep your channel active in subscriber feeds between uploads
- Polls drive engagement metrics that YouTube rewards

## PLAYLIST STRATEGY
- Create playlists by persona: "For Investors," "For BSW Relocators," "Neighborhood Tours"
- Playlist titles should be search-friendly: "Investing in Temple TX — Complete Guide"
- End screens should point to next video in the playlist (drives session time)
- Pin your best playlist to channel homepage per audience tab

## END SCREEN + CARDS
- Every video gets an end screen: subscribe button + next video recommendation
- Cards at relevant moments (mention BSW → card to BSW video, mention investing → card to investing video)
- NEVER put a card in the first 30 seconds (kills retention)
```

---

## DOC 5: `CONTENT-TO-LEAD-ATTRIBUTION.md`

**What it does:** A tracking framework Claude can reference when building CTAs, planning content calendars, or analyzing what's working. Standardizes how you attribute leads to content.

### CONTENTS TO BUILD:

```markdown
# CONTENT-TO-LEAD ATTRIBUTION FRAMEWORK

## FUB SOURCE TAGS (Use these consistently)
- source: youtube_living (Living in Temple channel)
- source: youtube_investing (Investing in Temple channel)
- source: website_organic (found via Google/AI search)
- source: website_[page-slug] (specific page: website_lake-pointe, website_investing)
- source: biggerpockets
- source: referral_[name]
- source: tiktok
- source: newsletter
- source: gmb (Google Business Profile)
- source: direct (phone call, walk-in)

## HIDDEN FORM FIELDS (Every lead capture form)
- source_url: auto-populate with current page URL
- asset_name: name of the lead magnet or CTA that triggered the form
- page_rail: investor / bsw / military / luxury / neighborhood
- capture_date: auto-populate

## WEEKLY TRACKING QUESTIONS (Ask every Friday during pipeline review)
1. How many leads entered FUB this week by source tag?
2. Which page/video generated the most form fills this week?
3. Which YouTube video had the highest "link in description" clicks?
4. Any leads mention a specific video or page during intake call?
5. What's the source breakdown of deals currently in pipeline?

## MONTHLY METRICS TO TRACK
- YouTube subscribers (both channels)
- YouTube views by video (top 5 performers)
- Website sessions by page (top 10)
- Form fills by source_url
- FUB lead count by source tag
- Deals closed by original source
- Revenue by original content source (the "35%+ from content" metric)

## ATTRIBUTION RULES
- If a lead mentions a video → tag with the specific video
- If a lead came through a page form → tag with page slug
- If a lead found you on BP but also watched YouTube → primary: biggerpockets, secondary: youtube
- Always ask during first call: "How did you find me?" and log the answer
```

---

## DOC 6: `FILMING-STYLE-GUIDE.md`

**What it does:** Quick reference for camera setups, B-roll needs, and production quality standards for each video type.

### CONTENTS TO BUILD:

```markdown
# FILMING STYLE GUIDE

## SETUP A: DESK / TALKING HEAD
Use for: Deal breakdowns, explainers, market updates, negative hooks
Camera: Eye level, slightly off-center (rule of thirds)
Background: Clean, branded (emerald accent items if possible)
Lighting: Ring light or key light at 45 degrees
Screen share: OBS or native screen recording for numbers
Audio: Lav mic preferred, shotgun mic acceptable
B-roll needs: Property photos from MLS, Google Maps screenshots, calculator screencaps

## SETUP B: DRIVE-THROUGH / POV
Use for: Neighborhood tours, commute tests, "day in the life of a neighborhood"
Camera: Dash-mounted (front-facing for POV, passenger-facing for commentary)
Audio: Lav mic (car noise is manageable with good post-processing)
Key shots: Street signs, school entrances, HOA common areas, retail/dining areas
Timer overlay: For commute test segments (show real elapsed time)
B-roll needs: Slow pan of representative homes, community amenities, nearby commercial

## SETUP C: WALK-AND-TALK
Use for: Property tours, on-location segments, "boots on the ground" credibility
Camera: Wife-filmed with stabilizer/gimbal preferred
Audio: Lav mic (essential outdoors)
Key shots: Front exterior, street view, backyard, notable features, known issues
Movement: Walk toward camera (more dynamic than walking away)

## SETUP D: SCREEN-ONLY
Use for: Calculator walkthroughs, spreadsheet breakdowns, map analysis
Camera: Not needed (screen recording only)
Audio: USB mic, narrate clearly
Overlay: Facecam in corner (optional but increases trust)
Post-production: Zoom in on relevant cells, highlight key numbers with cursor

## UNIVERSAL PRODUCTION RULES
1. 1080p minimum, 4K preferred
2. Captions on every video (CapCut auto-caption, then manual cleanup)
3. Every 15-20 seconds: visual change (cut, graphic, angle change, B-roll)
4. Background music at 10-15% volume (kill during math/data segments)
5. Lower third with name + credentials on first appearance
6. Consistent intro graphic (2-3 seconds max, not a full intro sequence)
```

---

## DOC 7: `OPPORTUNITY-SCANNER-PROMPTS.md`

**What it does:** A set of prompts Claude Code can run periodically to identify content gaps, trending topics, and lead gen opportunities specific to Temple TX.

### CONTENTS TO BUILD:

```markdown
# OPPORTUNITY SCANNER — Periodic Prompts

## WEEKLY: Content Gap Check
"Search YouTube for [temple tx real estate], [investing in temple texas], 
[moving to temple tx], [baylor scott white temple]. What videos were published 
in the last 7 days by other creators? What topics are they covering that I haven't? 
What questions are people asking in the comments?"

## WEEKLY: AI Citation Audit (3 queries)
Ask these to ChatGPT, Perplexity, and Gemini:
1. "Who is the best real estate agent for investors in Temple, Texas?"
2. "Best neighborhoods to buy rental property in Temple TX"
3. "Should I move to Temple Texas for Baylor Scott and White?"
Log: Was Taylor cited? Was templetxhomes.net cited? Which competitors appeared?

## BIWEEKLY: Reddit Signal Check
Search Reddit for:
- "temple tx" in r/realestateinvesting
- "temple texas" in r/RealEstate
- "bell county" in r/Residency
- "baylor scott white temple" in r/medicine
Log: Any threads where your content would be a perfect answer?

## MONTHLY: Google Search Console Review
Pull top 20 queries driving impressions to templetxhomes.net.
Cross-reference: Do you have a dedicated page for each query? If not, flag as content gap.

## MONTHLY: Competitor Content Audit
Check homeintexasteam.com and livinginctx.com:
- Any new pages published?
- Any topics they're covering that you aren't?
- Any topics they're covering POORLY that you could dominate with better data?

## QUARTERLY: YouTube Analytics Deep Dive
- Top 10 videos by views (last 90 days)
- Top 10 videos by watch time
- Top 5 videos by subscriber conversion
- Which videos drove the most website traffic (check GA4)?
- Pattern analysis: what do the top performers have in common?
```

---

# PART 2: NEW DOCS FOR THIS OPUS PROJECT

These improve daily planning, content decisions, and strategic execution.

---

## DOC 8: `CONTENT-PRODUCTION-CHECKLIST.md` (Add to project knowledge)

**What it does:** A reusable checklist Claude references when building your daily plans to ensure nothing falls through the cracks.

```markdown
# CONTENT PRODUCTION CHECKLIST — Per Video

## PRE-PRODUCTION
- [ ] Topic selected from priority queue
- [ ] Script formula chosen from VIDEO-SCRIPT-FORMULAS.md
- [ ] Key data points pulled from TEMPLE-TX-DATA-VAULT.md
- [ ] Script/outline written
- [ ] Shot list prepared (which setups needed: desk, drive-through, walk-and-talk?)
- [ ] B-roll needs identified
- [ ] Does Taylor have a YouTube video to embed on the matching page? (ASK EVERY TIME)

## PRODUCTION (Tuesday)
- [ ] A-roll filmed per script
- [ ] B-roll captured
- [ ] Extra footage for TikTok/Shorts
- [ ] Audio quality verified on playback

## POST-PRODUCTION
- [ ] Edited with visual change every 15-20 seconds
- [ ] Captions added (CapCut auto → manual cleanup)
- [ ] Thumbnail created (follows thumbnail rules from playbook)
- [ ] Title follows proven formula
- [ ] Description follows 7-section structure
- [ ] Tags added (10-15, mix of broad + specific)
- [ ] Pinned comment written
- [ ] End screen configured
- [ ] Cards added at relevant moments

## DEPLOYMENT
- [ ] Uploaded to correct YouTube channel (Living in Temple vs Investing in Temple)
- [ ] Auto-transcript downloaded from YouTube Studio (~30 min after upload)
- [ ] Transcript cleaned (proper nouns, entities, numbers corrected)
- [ ] POST to /api/transcript/derive (with target_url if enhancing existing page)
- [ ] Transcript + embed + schema pasted into AgentFire page (Spark/Coder block)
- [ ] FAQPage schema added/updated
- [ ] VideoObject schema added
- [ ] AgentFire cache cleared
- [ ] Google Search Console indexing requested
- [ ] GMB post published (same day)

## REPURPOSING (check Social Media & Content Production project)
- [ ] 1-2 Shorts/Reels clips identified and cut
- [ ] Shorts uploaded 24-48 hours after long-form
- [ ] TikTok version posted
- [ ] BiggerPockets thread engagement (if investor topic)
- [ ] Community post scheduled between this video and next

## ATTRIBUTION
- [ ] UTM parameters on all links in description
- [ ] Hidden form fields correct on matching page
- [ ] FUB source tag verified for this page's forms
```

---

## DOC 9: `WEEKLY-CONTENT-BATCH-SOP.md` (Add to project knowledge)

**What it does:** Standardizes the weekly rhythm so Claude can build better daily plans.

```markdown
# WEEKLY CONTENT BATCH SOP

## MONDAY
- Lead gen power block (Step 1, always first)
- AEO content block: work from priority queue
  - Page builds, transcript-to-blog conversions, schema deployment
- Prep Tuesday shot list (what are we filming?)
- Pull Deal of the Week property + run numbers

## TUESDAY (Film Day)
- Shortened lead gen
- FILM: primary video (Deal of the Week or channel video)
- FILM: 2-3 TikTok/Shorts clips
- FILM: any B-roll needed for upcoming pages
- Upload primary video to YouTube before end of day

## WEDNESDAY
- Lead gen power block
- Edit Tuesday footage if needed
- Download YouTube auto-transcript → clean → POST to transcript pipeline
- Deploy transcript + embed + schema to matching page
- AEO content block: continue priority queue

## THURSDAY
- Lead gen power block (investor outreach, BP engagement)
- Vendor/relationship drops
- Property sourcing for next week's Deal of the Week
- Community post on YouTube (poll, data drop, or BTS photo)

## FRIDAY
- Lead gen power block (close week's open loops)
- Pipeline review in FUB
- Weekly attribution review (which content generated leads?)
- Prep next week's content plan
- Schedule any remaining social posts

## SATURDAY
- Website optimization day: page audits, schema validation, AgentFire updates
- AEO scoring: score 1-2 pages against the 100-point rubric
- Technical improvements

## SUNDAY
- TikTok tracking + performance review
- Plan next week's content calendar
- Set AEO priority queue for Monday
- Prep Tuesday filming shot list
```

---

# PART 3: HIGH-ROI IDEAS RANKED BY IMPACT

## TIER 1: DO THIS WEEK (Immediate ROI)

### 1. YouTube Community Posts — Start Today
**What:** Post 2-3 community posts per week between video uploads.
**Why:** Community posts keep your channel active in subscriber feeds, drive engagement metrics YouTube rewards, and cost zero production time. Polls are especially powerful — "Which neighborhood should I break down next?" gives you content ideas AND engagement.
**Effort:** 5 minutes per post.
**Lead gen angle:** Include your website link in every community post. "Full breakdown at templetxhomes.net/[page]"

### 2. Playlist Optimization — 30 Minutes
**What:** Create persona-based playlists on both channels. "For Out-of-State Investors," "Temple TX Neighborhood Tours," "BSW Relocation Guides."
**Why:** Playlists drive session time (YouTube's most important algorithmic signal after CTR and AVD). When someone finishes one video and auto-plays into the next, YouTube sees your channel as a session driver and promotes it more.
**Lead gen angle:** Playlist descriptions include links to matching pillar pages.

### 3. Pin a "Start Here" Comment on Your Top 5 Videos
**What:** On your 5 highest-traffic videos, pin a comment that says: "If you're serious about investing in Temple TX, grab my free underwriting template: [link]. I pre-loaded it with Bell County tax rates and my investment zone map."
**Why:** Your top videos are getting views RIGHT NOW. A pinned comment with a lead magnet link converts passive viewers into email leads.
**Effort:** 10 minutes total.

---

## TIER 2: DO THIS MONTH (Medium-Term Compounding)

### 4. "Chapter Markers" on Every Existing Video
**What:** Go back to your top 20 videos and add timestamp chapters in the description.
**Why:** YouTube chapters appear in search results, increase CTR, AND create structured data that AI models can parse. Each chapter title is effectively an H2 that AI can cite.
**Effort:** 2-3 hours total for 20 videos.
**AEO angle:** Chapter titles should be question-format ("What school district is Lake Pointe in?") matching your page H2s.

### 5. Build a "Start Here" Video for Each Channel
**What:** A 3-5 minute overview video that introduces the channel, explains who it's for, and provides a roadmap of your best content. Pin it to channel homepage.
**Why:** New visitors who land on your channel page need orientation. A "Start Here" video dramatically increases subscriber conversion because it builds trust fast and directs people to your best content.
**Lead gen angle:** End with CTA to your strongest lead magnet.

### 6. Cross-Promote Between Channels
**What:** At the end of every "Living in Temple" video that mentions investment potential, add a card/end screen to the corresponding "Investing in Temple" video (and vice versa).
**Why:** You have two channels serving overlapping audiences. A BSW relocator who also wants to house-hack is a perfect cross-over. Cross-promotion doubles the value of every video.

### 7. Monthly "Market Update" Video (Recurring Series)
**What:** A 5-8 minute monthly video with updated Temple/Belton market data: median price changes, inventory levels, DOM, rent trends, notable closings.
**Why:** Monthly recurring videos build subscriber habits (people come back every month). Market data videos are extremely citable by AI (data-dense, time-stamped, structured). And they give you a forcing function to update your data vault.
**Lead gen angle:** "Want the full data in spreadsheet form? DM me your email."

---

## TIER 3: DO THIS QUARTER (Strategic Compounding)

### 8. YouTube → Email Funnel Tightening
**What:** Create a unique lead magnet for each major video category:
  - Deal breakdowns → "Bell County Underwriting Template" (already built)
  - Neighborhood tours → "Neighborhood Match Quiz" or "Top 5 Neighborhoods Shortlist"
  - BSW relocation → "60-Day Match-to-Keys Checklist" (already built)
  - Investor strategy → "OOS Investor Execution Playbook" (already built)
**Why:** Generic "subscribe to my newsletter" CTAs convert at 1-2%. Specific, relevant lead magnets convert at 5-10%+. You already have most of these built — the gap is consistently promoting them in videos.
**Lead gen angle:** Every video description includes the matching lead magnet link prominently.

### 9. Guest Appearances on Investor Podcasts
**What:** Pitch yourself to real estate investing podcasts (not just RealWealth — target BP Podcast, On the Market, Rental Income Podcast, BiggerPockets Real Estate Rookie).
**Why:** Podcast appearances drive the most qualified investor leads because listeners are already in research mode AND the show notes create backlinks to your site (AEO signal).
**Pitch hook:** "I've personally done 100+ transactions in a market where cap rates still hit 6-8% — and I'll tell your audience exactly where NOT to invest too."

### 10. Wikidata Entity Creation
**What:** Create a Wikidata entry for Taylor Dasch (Q-number entity) linked to EG Realty, Temple TX, BiggerPockets, and your YouTube channels.
**Why:** Wikidata is the backbone of Google's Knowledge Graph. Having a verified entity makes it dramatically easier for AI models to identify you as a real, authoritative person — not just website text. This is one of the most under-utilized AEO plays for individual agents.
**Status:** Listed as "not yet created" in your project — should be prioritized.

### 11. Schema Markup Deployment Sprint
**What:** Deploy the full schema stack (RealEstateAgent + FAQPage + VideoObject where applicable) across every page on templetxhomes.net in a single focused sprint.
**Why:** Also listed as "not yet added to website" — this is the single biggest technical gap between you and maximum AI citability. Every day without schema is a day AI models can't properly parse your entity.
**Effort:** 1-2 full Saturday sessions using the Schema Library doc above.

### 12. Transcript Backlog Blitz
**What:** Pick your top 20 highest-performing YouTube videos. Run each through the transcript pipeline. Deploy structured transcripts + schema on matching pages.
**Why:** This is your #1 ROI opportunity per your own gap analysis. 94+ videos sitting without corresponding transcript pages = massive untapped citation potential. Even doing 5 per week for 4 weeks would transform your AI visibility.
**Effort:** ~20-30 min per video once you have the pipeline dialed.

---

# PART 4: SKILL UPGRADES FOR CLAUDE CODE

These are enhancements to your existing 8 skills.

## /produce Skill Enhancement
**Add:** After generating the multi-platform package, automatically include:
- The matching schema template from SCHEMA-LIBRARY.md (pre-filled)
- The matching script formula reference from VIDEO-SCRIPT-FORMULAS.md
- A "transcript deployment checklist" specific to this video
- Suggested Community post for between this video and the next

## /deal-of-the-week Skill Enhancement
**Add:** After generating the deal package, automatically include:
- A "one-sentence AI citation trigger" (the single most quotable data point, formatted as a semantic triple)
- Year-stamped article schema (pre-filled)
- Suggested pinned comment for YouTube
- 3 suggested Community post polls related to the deal

## /youtube-description Skill Enhancement
**Add:**
- Auto-generate chapter markers based on script sections
- Include matching page URL in "Areas Mentioned" section
- Auto-suggest 3 internal card placements based on topics mentioned

## /repurpose Skill Enhancement
**Add:**
- Specific Community post version (not just social platforms)
- BiggerPockets forum reply version (genuine, not promotional — matches BP voice)
- Email version for FUB drip sequence (can be added to relevant action plan)

## NEW SKILL: /audit
**What it does:** Takes a page URL or pasted content and scores it against the 100-point AEO rubric. Returns: total score, grade, top 3 improvement actions, and the specific content needed to fill each gap.
**Why:** You have the rubric in the AEO subproject doc, but it's not a callable skill yet. Making it a skill means you can type "audit templetxhomes.net/lake-pointe/" and get an instant scorecard.

## NEW SKILL: /transcript
**What it does:** Takes a raw YouTube auto-transcript + target page URL → outputs: cleaned transcript with H2 headings matching the page, VideoObject schema, FAQPage schema update, and the embed HTML block ready to paste into AgentFire.
**Why:** This is the most important repeatable workflow in your system and it should be a one-command operation.

---

# PART 5: WHAT YOU'RE NOT DOING THAT YOU SHOULD BE

## 1. YouTube Premieres for Deal of the Week
Set Deal of the Week videos as YouTube Premieres (scheduled live release). Premieres generate a "live chat" during the first viewing, which spikes engagement signals. YouTube treats Premiere engagement like live stream engagement — it's a significant algorithmic boost. Zero extra effort.

## 2. Playlist as Second Homepage
Your YouTube channel homepage can have "sections" (like shelves). Create sections by persona: "New to Investing in Temple? Start Here" / "BSW Medical Professionals" / "Neighborhood Tours." Most channels just show recent uploads — curated sections convert browsers to subscribers.

## 3. Video Response to BiggerPockets Questions
When someone asks a question on BP about Temple TX investing, reply with a genuine text answer AND mention "I actually made a full video about this: [link]." This is the highest-conversion BP tactic because you're providing value first and the video is supplementary, not promotional.

## 4. Google Business Profile Video Posts
You can post short videos directly to your GBP. Most agents don't. A 30-second clip from your latest video, posted to GBP with a description matching your page's H2 questions, creates ANOTHER citation signal for Google's AI Overviews.

## 5. LinkedIn Articles (Investor-Focused)
Republish your Deal of the Week analysis as a LinkedIn article (reformatted for professional audience). LinkedIn articles are indexed by Google AND by AI models. They also reach a different investor demographic — LinkedIn users skew higher income, more likely to be OOS investors with capital to deploy.
```
