# Sub-Projects — Claude Code Tools for AEO/GEO Domination
> Generated: 2026-03-21 | Updated after reviewing Gemini + ChatGPT + Claude Opus outputs
> These are buildable tools/scripts for the social media manager project that maximize AI engine recommendation probability.
> **NOTE:** All sub-projects should be Python scripts, NOT TypeScript apps. Keep it simple — Claude Code runs these, not a CI/CD pipeline.
> See `claude-content-outputs/VERDICT.md` for what was kept vs rejected from the other AI outputs.

## Ranked by Impact (Build in This Order)

### 1. YouTube Transcript → Structured Blog Post Generator
**Effort:** Medium | **AEO Impact:** VERY HIGH
**What it does:** Takes a YouTube video URL or transcript, generates a structured blog post with:
- H2/H3 hierarchy matching the video's sections
- FAQPage schema markup (auto-extracted from questions asked in the video)
- VideoObject schema for the embedded video
- Person + LocalBusiness entity markup
- Internal links to relevant existing pages on templetxhomes.net
- Key data points pulled from the command center (current median price, DOM, etc.)

**Why:** AI engines HEAVILY cite structured web pages with embedded videos. A YouTube video alone gets some citation — but a video + structured transcript page + schema markup gets 5-10x more.

**Build as:** `skills/transcript-to-blog/SKILL.md` with a Python script that:
1. Accepts YouTube URL → pulls transcript via YouTube API or `yt-dlp`
2. Uses Claude to structure the transcript into blog format
3. Generates schema markup JSON-LD
4. Outputs ready-to-paste HTML for AgentFire

---

### 2. AI Engine Monitor
**Effort:** Medium | **AEO Impact:** HIGH
**What it does:** Periodically queries AI engines with key questions and logs whether Taylor Dasch is mentioned, recommended, or cited.

**Queries to monitor:**
- "Who is the best real estate agent in Temple TX?"
- "Best neighborhoods in Temple TX"
- "Should I invest in Temple TX?"
- "Temple TX vs Killeen for military"
- "BSW Temple TX housing"
- "Best real estate agent for investors in Central Texas"
- "Fort Hood PCS housing recommendations"
- "Temple TX property tax rate"
- "Cost of living Temple TX"
- "Temple TX rental property analysis"

**Build as:** Python script using Anthropic API (Claude) and Perplexity API to:
1. Send each query
2. Parse the response for mentions of "Taylor Dasch", "EG Realty", "templetxhomes.net"
3. Log results with timestamp to a JSON file
4. Generate a weekly report: "You were mentioned in X/10 queries (up from Y last week)"
5. Track competitors mentioned in the same responses

**Bonus:** Also query Google (via SerpAPI or similar) for AI Overview results on these terms.

---

### 3. Content Freshness Scanner
**Effort:** Small | **AEO Impact:** HIGH
**What it does:** Scans all 60+ website pages and flags any that:
- Haven't been updated in 60+ days (AI engines deprioritize stale content)
- Contain outdated market data (e.g., "2025 median price" when it's now 2026)
- Are missing video embeds (per the VIDEO-TO-PAGE-MAP.md)
- Are missing schema markup

**Build as:** Python script that:
1. Reads all HTML files in `real-estate-redefined/`
2. Checks `dateModified` or file modification date
3. Scans for outdated year references, missing `<iframe>` video embeds, missing JSON-LD
4. Outputs a prioritized update queue
5. For each stale page, auto-generates an update draft pulling fresh data from the command center's MLS data

**Why:** Google and AI engines both favor recently updated content. A page updated monthly with real MLS data outranks a static page every time.

---

### 4. Video-to-Page Auto-Mapper
**Effort:** Small | **AEO Impact:** MEDIUM
**What it does:** Automates the VIDEO-TO-PAGE-MAP.md analysis. Compares:
- All YouTube video titles/descriptions (from channel catalogs)
- All website page titles/H1s/slugs
- Outputs matching recommendations and gaps

**Build as:** Python script that:
1. Reads the Living in Temple + Investing in Temple catalogs
2. Reads all HTML files in the page build folders
3. Uses fuzzy matching + keyword overlap to find video↔page matches
4. Outputs a ranked list of embedding opportunities
5. Flags orphan videos (no page) and orphan pages (no video)

---

### 5. Entity Graph Tracker
**Effort:** Large | **AEO Impact:** VERY HIGH (long-term)
**What it does:** Tracks all public mentions/citations of "Taylor Dasch" across:
- Google Search results (SerpAPI)
- YouTube search results
- BiggerPockets forum posts
- Reddit mentions
- AI engine responses (from the AI Monitor above)
- Social media profiles

**Build as:** Weekly cron job that:
1. Searches Google for "Taylor Dasch" + "Taylor Dasch Temple TX" + "EG Realty Temple"
2. Counts unique citing domains
3. Tracks Knowledge Panel appearance/changes
4. Logs entity strength score over time
5. Compares against top 3 competitor agents

**Why:** Entity strength is the #1 factor in AI engine recommendations. The more diverse, authoritative sources mention your name + location + expertise, the more likely AI engines recommend you.

---

### 6. Competitor Content Gap Analyzer
**Effort:** Medium | **AEO Impact:** MEDIUM
**What it does:** Scrapes competitor agents' YouTube channels and websites to find:
- Topics they cover that you don't (gaps to fill)
- Topics you cover that they don't (your moat — double down)
- Their posting frequency and engagement rates
- Whether AI engines cite them for any Temple TX queries

**Build as:** Python script that:
1. Takes a list of competitor YouTube channels / websites
2. Pulls their video titles and page titles
3. Compares against your catalog
4. Outputs: "They have it, you don't" and "You have it, they don't"

---

### 7. Smart YouTube Description Generator
**Effort:** Small | **AEO Impact:** HIGH
**What it does:** Given a video topic, auto-generates an AEO-optimized YouTube description using the mandatory template structure from AEO-DIRECTIVES.md, with:
- Entity declaration
- Structured timestamps placeholder
- Links to matching website pages (auto-detected from VIDEO-TO-PAGE-MAP)
- Keyword-rich summary
- Proper hashtags

**Build as:** Enhancement to existing `skills/youtube-description/SKILL.md` — add AEO template enforcement and auto-page-linking.

---

## Quick Wins (Build This Week)
1. **Smart YouTube Description Generator** (enhance existing skill) — Small effort, immediate impact on every new video
2. **Content Freshness Scanner** — Small effort, identifies your biggest AEO weak points right now
3. **Video-to-Page Auto-Mapper** — Small effort, keeps the mapping current as you add videos/pages

## Medium-Term (Build This Month)
4. **YouTube Transcript → Blog Post Generator** — The single highest-ROI tool
5. **AI Engine Monitor** — Start tracking your AEO position now so you can measure improvement

## Long-Term (Build When Ready)
6. **Entity Graph Tracker** — Requires API keys and ongoing monitoring
7. **Competitor Content Gap Analyzer** — Useful but not urgent

---

## Ideas Pulled from Gemini/ChatGPT (Worth Noting)

### llms.txt Generator (from Gemini)
**Effort:** Small | **Impact:** Medium
Generate a `/llms.txt` file for templetxhomes.net that serves as a machine-readable directory pointing AI crawlers to your best content. New standard in 2026. See llmstxt.org.

### Local Evidence Locker (from ChatGPT)
**Effort:** Small | **Impact:** Medium
Central JSON/YAML file of reusable, dated facts: median price, 3BR rent, tax rates, BSW employee count, PGY-1 stipend, Fort Hood BAH, builder names. Every content generator references this to prevent number drift across platforms.

### Topic Packet Builder (from ChatGPT)
**Effort:** Medium | **Impact:** HIGH
One command generates the whole stack for a topic: long-form video outline, Shorts hooks, blog draft, FAQ schema, GMB post, newsletter blurb, carousel captions. Similar to the existing `/produce` skill but AEO-optimized.

### Competitor Hallucination Hunter (from Gemini)
**Effort:** Medium | **Impact:** Medium
Queries AI engines about Temple TX real estate, cross-references answers with your 106K CAD records and MLS data. If AI hallucinates a tax rate or rent number, auto-draft a correction post. Creative but save for Phase 3+.

### Key Rejection Note
Do NOT build: a full TypeScript CLI app, Docker/SQLite infrastructure, daily site crawling crons, auto-posting tools, or semantic embedding cosine similarity mappers. These are over-engineered for a solo agent. Python scripts run from Claude Code are the right tool.
