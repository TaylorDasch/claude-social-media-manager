# CONTENT SYSTEM ACTION PLAN
## Synthesized from Claude Opus, Gemini Deep Research, ChatGPT Analysis
### Taylor Dasch | EG Realty | Created March 21, 2026

---

## THE BLUNT TRUTH

Your moat is NOT more content ideas. You have 94+ videos, 8 skills, a Telegram bot, and research most agencies would charge $10K for. **The gap is execution infrastructure.** Your output folder is empty. No schema on the site. No transcript-to-blog pipeline running. No AEO monitoring. 18 videos waiting to be embedded on pages they already match.

The fastest path to more leads: **convert the 94-video backlog into a structured, schema-rich local content library.**

---

# PHASE 1: FOUNDATION (This Week — 5-8 Hours Total)

These cost $0, require no code, and unlock everything downstream.

### 1.1 Wikidata Entity Creation (20 min)
- Go to wikidata.org → Create Item
- Properties: instance of: human, occupation: real estate broker, employer: EG Realty, location: Temple TX
- Link: website, both YouTube channels, BiggerPockets
- **Why:** #1 trigger for Google Knowledge Panel. AI models use Wikidata to verify you're a real entity.

### 1.2 Schema Markup on Homepage (2 hours)
- Deploy `RealEstateAgent + Person` JSON-LD on templetxhomes.net homepage
- Include `sameAs` array: Wikidata URL, YouTube channels, BiggerPockets, Zillow, LinkedIn
- Validate at validator.schema.org before publishing
- **Why:** Without schema, AI engines can't properly parse your entity. This is table stakes.

### 1.3 Embed 18 Tier-1 Videos (2 hours)
- Open VIDEO-TO-PAGE-MAP.md → Tier 1 list
- Embed each video on its matching page in AgentFire
- Add `VideoObject` schema to each page with an embed
- **Why:** A video embedded on a schema-rich page = 3 citation signals vs 1. These are ready NOW.

### 1.4 Pin Lead Magnets on Top 5 Videos (10 min)
- Your highest-traffic videos are getting views RIGHT NOW
- Pin a comment on each: persona-matched lead magnet + link
- Example: "Grab the DSCR calculator I used in this video: [link]"
- **Why:** Converts passive viewers into email leads. 10 minutes, immediate ROI.

### 1.5 YouTube Playlist Optimization (30 min)
- Create persona-based playlists: "For Out-of-State Investors," "Temple TX Neighborhood Tours," "BSW Relocation Guides"
- Pin best playlist to channel homepage
- **Why:** Playlists drive session time — YouTube's most important signal after CTR and retention.

### 1.6 AEO Monitoring Setup (30 min)
- Sign up for Otterly.AI ($29/mo) or Listable Labs
- Load 15 monitoring prompts from AEO-RESEARCH-2026.md
- **Why:** You can't improve what you don't measure. This tells you when AI engines start (or stop) recommending you.

---

# PHASE 2: CONTENT MULTIPLICATION ENGINE (This Month — Weeks 2-4)

### 2.1 Build `/transcript-to-blog` Skill (HIGH PRIORITY — #1 ROI tool)

**What it does:** Takes a YouTube URL or transcript → outputs a structured blog post with:
- BLUF (Bottom Line Up Front) — 50-word answer AI engines scrape first
- H2/H3 hierarchy matching search queries
- "Scars & All" callout block (honest negative, triggers Information Gain)
- FAQ section (3-5 Q&As from the video)
- VideoObject + FAQPage JSON-LD schema
- Internal link suggestions to templetxhomes.net pages
- Embed placeholder for the video

**Build as:** `skills/transcript-to-blog/SKILL.md` (Python script using yt-dlp for transcript pull)

**First run:** Feed it your top 10 performing videos. Deploy those 10 blog pages to AgentFire with video embedded + schema. Instantly creates 10 high-authority AEO assets.

### 2.2 Build Reference Docs That Make Every Skill Smarter

| Doc | Purpose | Impact |
|-----|---------|--------|
| `TEMPLE-TX-DATA-VAULT.md` | Single source for all recurring data (BAH, BSW salary, median price, tax rates, commutes). Every skill pulls from here instead of guessing. | Eliminates data inconsistency across content — a core AEO signal |
| `VIDEO-SCRIPT-FORMULAS.md` | 5 proven script structures (Deal Breakdown, Neighborhood Tour, Negative Hook, Explainer, Short). Claude uses the right formula instead of generating from scratch. | Better scripts, faster production |
| `SCHEMA-LIBRARY.md` | Pre-built JSON-LD templates (VideoObject, FAQPage, RealEstateAgent, Article, HowTo, LocalBusiness). Fill-in-the-blank for every page type. | Schema deployment goes from 30 min to 5 min per page |
| `LEAD-MAGNET-MATRIX.md` | Maps personas → lead magnets → CTAs. Investor → Deal Analyzer Spreadsheet. Military → BAH Commute Map. Medical → Zero-Down Physician Loan Guide. Luxury → Due Diligence Checklist. | Claude auto-appends the right CTA to every piece of content |
| `CONTENT-TO-LEAD-ATTRIBUTION.md` | FUB source tags, hidden form fields, weekly tracking questions. Standardizes how leads are attributed to content. | Finally answers "which content generates deals?" |

### 2.3 Transcript Backlog Blitz (20 videos in 4 weeks)
- Week 2: Top 5 "Investing in Temple" videos → blog pages
- Week 3: Top 5 "Living in Temple" videos → blog pages
- Week 4: Next 10 highest-traffic videos → blog pages
- Each page: transcript + embed + VideoObject + FAQPage schema + internal links
- **Target:** 20 structured pages in 3 weeks = massive AEO footprint

### 2.4 YouTube Chapter Markers on Top 20 Videos (2-3 hours)
- Add timestamp chapters to descriptions
- Format chapter titles as questions matching page H2s
- **Why:** Chapters appear in search results, increase CTR, AND create structured data AI models parse.

### 2.5 Build `/content-freshness-scanner` Skill
- Scans all pages for: data older than 60 days, missing video embeds, missing schema, outdated year references
- Outputs prioritized refresh queue
- **Why:** Stale content loses AI citations. Monthly freshness = monthly citations.

### 2.6 Enhance Existing Skills

**`/produce` additions:**
- Auto-include matching schema template (pre-filled from SCHEMA-LIBRARY)
- Suggest YouTube Community post for between this video and next
- Include transcript deployment checklist
- Auto-generate pinned comment with persona-matched lead magnet

**`/deal-of-the-week` additions:**
- One-sentence "AI citation trigger" (most quotable data point)
- Year-stamped Article schema (pre-filled)
- 3 Community post poll suggestions

**`/youtube-description` additions:**
- Auto-generate chapter markers from script sections
- Include matching page URL
- Auto-suggest 3 internal card placements

**`/repurpose` additions:**
- YouTube Community post version
- LinkedIn carousel outline (PDF format for investor/medical personas)
- BiggerPockets forum reply version

---

# PHASE 3: LEAD GENERATION INFRASTRUCTURE (Month 2)

### 3.1 ManyChat Auto-DM Strategy
- Set up ManyChat for TikTok/Instagram
- Update `/tiktok-script` to end with keyword triggers: "Comment TAXES and I'll DM you the calculator"
- **Why:** Spikes algorithmic engagement (comments) AND captures leads instantly via DM flow → FUB

### 3.2 FUB Database Scrub & Segmentation
- Tag all 607 contacts with persona (Military, Medical, Investor, Luxury)
- Remove bounced/unengaged contacts (protect sender reputation)
- Set up behavioral triggers: if contact views properties in specific ZIP/price range → auto-trigger relevant sequence

### 3.3 Launch BSW "Match Day" Micro-Campaign
- For all Medical-tagged contacts
- 90-day drip starting post-Match Day: physician loans, commute times, neighborhood guides
- **Why:** Known high-stress timeline, high-intent buyers, perfect targeting window

### 3.4 Build New Skills

**`/community-post` skill:**
- Input: video topic
- Output: 3 variations (data poll, "Scars & All" post, pop quiz)
- **Why:** Community posts reach NON-subscribers. Best free organic growth hack on YouTube in 2026.

**`/linkedin-carousel` skill:**
- Input: deal breakdown or market data
- Output: 5-7 slide outline for PDF carousel
- **Why:** LinkedIn document posts get 5.85% engagement — highest on the platform. BSW surgeons and OOS investors live here.

**`/audit` skill:**
- Input: page URL or content
- Output: AEO score (100-point rubric), grade, top 3 improvement actions
- **Why:** Makes the AEO rubric from your research into a callable one-command workflow

### 3.5 Build AI Engine Citation Monitor
- Python cron job querying ChatGPT, Perplexity, Gemini with 30 rotating prompts
- Tracks mentions of "Taylor Dasch," "EG Realty," "templetxhomes.net"
- Weekly report: citation rate, competitor citations, trending queries
- **Cost:** ~$5-15/mo in API calls
- **Why:** Your AEO scoreboard. Only agent in Central Texas tracking this.

---

# PHASE 4: STRATEGIC COMPOUNDING (Quarter 2)

### 4.1 Film 5 AEO Gap Videos (3-hour desk session)
All scripts and filming tips are ready in AEO-GAP-VIDEOS.md:
1. Bell County Property Taxes: The EXACT Formula
2. How to Analyze a Temple TX Buy-and-Hold (Live Spreadsheet)
3. The 1% Rule is Dead in Texas
4. Temple vs Killeen: The Data No One Shows You
5. BSW Residents: Buy a House BEFORE Your First Day

Batch film all 5 in one sitting (change shirt between every 2 videos).

### 4.2 Monthly Market Pulse Report
- Publish monthly on templetxhomes.net with Article schema
- Temple market snapshot + neighborhood breakdowns + investment yields + BAH implications
- **Why:** Becomes THE go-to citation source for AI engines on Temple real estate. Nothing else like it exists.

### 4.3 YouTube Premieres for Deal of the Week
- Set Deal of the Week as YouTube Premiere (scheduled live release)
- Premieres generate live chat → YouTube treats this like live stream engagement → algorithmic boost
- Zero extra effort

### 4.4 Podcast Guest Circuit
- Pitch: BP Podcast, On the Market, Rental Income Podcast, RE Rookie
- Hook: "I've personally done 100+ transactions in a market where cap rates still hit 6-8% — and I'll tell your audience exactly where NOT to invest too."
- **Why:** Podcast appearances drive the most qualified investor leads + show notes = backlinks (AEO signal)

### 4.5 TikTok Search Ads Test
- Small controlled test on high-intent queries: "temple tx homes," "investing in temple texas," "fort hood housing"
- Traffic + web conversion objectives
- Temple-only geo-targeting (zips 76501-76544)
- **Budget:** $50 every 5 days
- **Why:** TikTok Search Ads show incremental conversion lift when paired with organic. Worth testing.

### 4.6 Build Remaining Sub-Projects
- Video-to-Page Auto-Mapper (Python) — keeps mapping current automatically
- Entity Graph Tracker — weekly entity strength scoring vs competitors
- Competitor Content Gap Analyzer — find what they cover that you don't
- Internal Link Graph Builder — map and fix orphan pages

---

# WEEKLY OPERATING RHYTHM

Once the system is running, this is the weekly cadence:

| Day | Focus |
|-----|-------|
| **Monday** | Lead gen power block → AEO content block (page builds, transcript conversions, schema) → Prep Tuesday shot list |
| **Tuesday** | Film: primary video + 2-3 TikTok clips + B-roll → Upload to YouTube |
| **Wednesday** | Download transcript → clean → run `/transcript-to-blog` → deploy page + schema → AEO block continues |
| **Thursday** | Lead gen (investor outreach, BP engagement) → Community post → Source next Deal of the Week |
| **Friday** | Pipeline review in FUB → Weekly attribution review → Plan next week |
| **Saturday** | Website optimization: page audits, schema validation, freshness scanner |
| **Sunday** | TikTok review → content calendar → set Monday AEO queue |

---

# NEW REFERENCE DOCS TO CREATE

Priority order for building:

| # | Doc | Where | Effort | Impact |
|---|-----|-------|--------|--------|
| 1 | TEMPLE-TX-DATA-VAULT.md | claude-social-media-manager/ | 1 hour | Eliminates data drift across all content |
| 2 | SCHEMA-LIBRARY.md | claude-social-media-manager/ | 1 hour | Every page gets schema in 5 min |
| 3 | VIDEO-SCRIPT-FORMULAS.md | claude-social-media-manager/ | 30 min | Better scripts, proven structures |
| 4 | LEAD-MAGNET-MATRIX.md | claude-social-media-manager/ | 30 min | Auto CTAs matched to persona |
| 5 | CONTENT-TO-LEAD-ATTRIBUTION.md | claude-social-media-manager/ | 30 min | Track what generates deals |
| 6 | YOUTUBE-GROWTH-PLAYBOOK.md | claude-social-media-manager/ | 45 min | Algorithm mechanics reference |
| 7 | FILMING-STYLE-GUIDE.md | claude-social-media-manager/ | 20 min | Production quality standards |
| 8 | OPPORTUNITY-SCANNER-PROMPTS.md | claude-social-media-manager/ | 20 min | Weekly/monthly audit prompts |
| 9 | CONTENT-PRODUCTION-CHECKLIST.md | claude-social-media-manager/ | 15 min | Nothing falls through cracks |
| 10 | WEEKLY-CONTENT-BATCH-SOP.md | claude-social-media-manager/ | 15 min | Standardized weekly rhythm |

---

# SKILLS TO BUILD (Priority Order)

| # | Skill | Status | ROI |
|---|-------|--------|-----|
| 1 | `/transcript-to-blog` | NEW — #1 priority | Transformative |
| 2 | `/community-post` | NEW | High (free growth) |
| 3 | `/linkedin-carousel` | NEW | High (BSW + investor reach) |
| 4 | `/audit` (AEO scorer) | NEW | High (measurement) |
| 5 | `/produce` | ENHANCE (add schema, community post, checklist) | High |
| 6 | `/deal-of-the-week` | ENHANCE (add citation trigger, pinned comment) | High |
| 7 | `/youtube-description` | ENHANCE (add chapters, card suggestions) | Medium |
| 8 | `/repurpose` | ENHANCE (add community post, LinkedIn, BP versions) | Medium |
| 9 | `/content-freshness-scanner` | NEW | High (AEO protection) |
| 10 | `/schema-pack` | NEW | Medium (speeds up deployment) |

---

# PLATFORMS YOU'RE UNDERUSING

| Platform | Current | Opportunity |
|----------|---------|-------------|
| **YouTube Community Tab** | Not using | 2-3 posts/week between uploads. Polls, data drops, BTS photos. Reaches NON-subscribers. |
| **LinkedIn** | Not using | PDF carousels for investor/medical content. 5.85% engagement rate. OOS investors live here. |
| **GBP Video Posts** | Text only | Post 30-sec clips from latest video. Creates another citation signal for AI Overviews. |
| **YouTube Premieres** | Not using | Set Deal of the Week as Premiere. Live chat spikes engagement. Zero effort. |
| **Bluesky** | Not using | 41M users, extraordinary engagement. Early mover advantage for analytical RE content. |
| **Podcast Guest Circuit** | Not pitching | Highest-conversion tactic for qualified investor leads + backlinks. |

---

# WHAT NOT TO BUILD

- Full TypeScript CLI app (over-engineered for solo agent)
- Docker/Makefile/package.json infrastructure
- Daily site crawling crons
- Semantic embedding mappers
- Auto-posting tools (violates DRAFT ONLY rule)
- Video landing pages for EVERY video (creates thin content penalty)
- Wikipedia page (Wikidata is sufficient and more practical)

---

# CHATGPT'S BEST INSIGHT (Worth Highlighting)

> "Google's March 2026 guidance says AI Overviews do not require special optimization beyond normal SEO. Pages just need to be indexed, snippet-eligible, textually clear, internally linked, and supported by accurate structured data. Google also says these systems use query fan-out — a strong argument for building more narrow, intent-specific local pages instead of one giant 'Temple real estate' page."

Translation: Your neighborhood-specific, persona-specific pages are EXACTLY right. Build more of them, not fewer bigger ones.

---

# GEMINI'S BEST INSIGHT (Worth Highlighting)

> "A YouTube view without a Call-To-Action is wasted. 94+ videos sitting without persona-matched lead magnets = 94 missed conversion opportunities. Add the right CTA retroactively and your back catalog becomes an active lead capture net today."

Translation: Before building anything new, monetize what you already have by adding lead magnets to your existing 94 videos.

---

# CHATGPT'S CONTRARIAN TAKES (Consider These)

1. **Delay Wikidata** — ChatGPT argues entity consistency across your site/profiles/markup matters more than Wikidata specifically. (I disagree — do both, Wikidata takes 20 min.)
2. **FAQ rich results are restricted** — Google limits FAQ rich results to government/health sites. Use FAQ schema for machine readability, but don't treat it as a visibility lever. (Valid nuance.)
3. **Delay enhanced YouTube descriptions** — Fix the transcript/page/schema stack first, descriptions aren't the bottleneck. (Agree — do this after Phase 2.)

---

# SUCCESS METRICS

Track these monthly to know the system is working:

| Metric | Baseline (March 2026) | Target (June 2026) |
|--------|----------------------|---------------------|
| Structured blog pages from videos | 0 | 40+ |
| Pages with VideoObject schema | 0 | 30+ |
| Pages with FAQPage schema | ~5 | 30+ |
| Wikidata entity | No | Yes |
| AEO citation rate (Otterly.AI) | Unknown | Tracking, trending up |
| YouTube subscribers (Living) | [current] | +30% |
| YouTube subscribers (Investing) | [current] | +30% |
| FUB leads tagged to content source | ~35% | 50%+ |
| Revenue from content sources | 35% | 50%+ |
| Weekly content output (filled weeks) | 0 | Every week |

---

*This plan synthesizes the best recommendations from Claude Opus (sub-project ranking, Python-not-TypeScript, phased execution), Gemini Deep Research (AEO data, citation stats, entity strategy, ManyChat, community posts, lead magnets), and ChatGPT (transcript-to-blog priority, narrow intent pages, query fan-out, behavioral CRM triggers, contrarian takes on FAQ/Wikidata). Rejected: over-engineered TypeScript architecture, Docker infrastructure, auto-posting, thin content at scale.*
