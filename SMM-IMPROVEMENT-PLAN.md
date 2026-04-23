# Social Media Manager — Improvement Plan
**Created:** 2026-04-13
**Status:** Complete (Claude tasks 100% — 2026-04-13. Taylor manual tasks remain.)

See [CODEX-BACKLOG.md](CODEX-BACKLOG.md) for the Codex-only execution queue: one bounded job per worktree, led by `/youtube-metadata`, `/keyword-audit`, Postiz hardening, and performance-ledger automation.

---

## 1. WIRE EXISTING MCP TOOLS INTO SKILLS (Claude Does This)

These MCP tools are already connected but the skills don't use them yet.

- [x] **YouTube MCP** → `/weekly-scorecard` (pull video stats, views, CTR)
- [ ] **YouTube MCP** → `/youtube-metadata` (auto-update titles/descriptions/tags) — Requires building a new `/youtube-metadata` skill. Deferred.
- [x] **YouTube MCP** → `/produce` (auto-pin persona-matched comments)
- [x] **Beehiiv MCP** → `/newsletter` (check previous issue performance before writing)
- [x] **Beehiiv MCP** → `/weekly-scorecard` (pull open rate, click rate, subscriber count)
- [x] **Canva MCP** → `/thumbnail-brief` (generate actual thumbnail designs, not just briefs)
- [ ] **Google Search Console** → `/keyword-audit` (real ranking data, not just transcript density) — Requires building a new `/keyword-audit` skill. Deferred.
- [x] **Google Search Console** → `/content-calendar` (plan content around keyword opportunities)
- [x] **Google Search Console** → `/audit` (track which pages gain/lose traffic)
- [x] **Google Maps** → `/gmb-post` (track local rank for key terms)
- [x] **RSS Feeds** → `/content-calendar` (pull real estate news + competitor posts for ideas)
- [x] **FUB MCP** → `/weekly-scorecard` (count new leads by content source)
- [x] **Playwright** → `/audit` (screenshot + compare competitor pages)

---

## 2. MCP SERVERS TO INSTALL (Taylor Does This)

### Already Done
- [x] **Claude-SEO Skill** — Installed v1.8.2 (20 new /seo skills available)
- [x] **TrendsMCP.ai** — Added to local config (restart to activate)
- [x] **Apify MCP** — Added to local config (restart to activate)

### Install This Week
- [ ] **Reddit MCP** — Zero config, no API keys needed
  ```bash
  claude mcp add reddit-mcp -- npx -y @eliasbiondo/reddit-mcp-server
  ```
  Why: Completes the `/reddit-bp` skill with monitoring + thread discovery

### Install This Month
- [ ] **Google Analytics MCP** — Official Google project
  ```bash
  claude mcp add google-analytics -- npx -y @google-analytics/mcp-server
  ```
  Why: Track which social channels drive traffic to templetxhomes.net

- [x] ~~**Apify MCP**~~ — Installed (restart to activate)

- [ ] **Postiz (Self-Hosted Social Scheduler)** — Deploy on Railway (~$5/month)
  Supports 17+ platforms: X, Instagram, LinkedIn, Facebook, Reddit, Threads, TikTok, YouTube
  Has built-in MCP endpoint at `/api/mcp/{API_KEY}` (Streamable HTTP transport)
  ```bash
  # 1. Deploy on Railway
  railway init
  railway link
  railway up
  # 2. Get your Postiz API key from the dashboard
  # 3. Connect to Claude Code
  claude mcp add postiz -- curl http://your-postiz-url/api/mcp/YOUR_API_KEY
  ```
  Why: Single biggest workflow improvement. Stops copy-paste-to-every-platform bottleneck.

### Install This Quarter
- [ ] **vidIQ MCP** — YouTube intelligence (135M+ channels of keyword data)
  Why: Data-driven keyword research, competitor analysis, content gap identification

---

## 3. NEW SKILLS TO BUILD (Claude Does This)

- [x] **`/weekly-analytics-pull`** — Sunday auto-consolidation skill
  Pulls: YouTube stats + Beehiiv stats + GSC top queries + FUB lead counts + Google Maps rank
  Outputs: Single weekly performance snapshot that feeds `/weekly-scorecard`

- [x] **`/tiktok-performance`** — TikTok trend integration skill
  Pulls: Trending local hashtags from TrendsMCP (NOTE: TrendsMCP not yet connected — skill built with graceful fallback)
  Cross-references against content-registry.csv for gaps
  Feeds results into `/content-calendar`

---

## 4. PLATFORM STRATEGY UPDATES (Claude Updates Skills)

- [x] **Instagram**: Update `/repurpose` and `/instagram-reel` — shift from hashtag-heavy to keyword-dense captions (3-5 hashtags max). Instagram 2026 algorithm weights caption text over hashtags.
- [x] **TikTok**: Wire TrendsMCP data into `/tiktok-performance` skill (TrendsMCP not yet connected — skill ready when it is)
- [x] **YouTube**: Wire YouTube MCP into `/produce` for auto comment pinning + stats pull
- [x] **GMB**: Add Google Maps `maps_local_rank_tracker` to `/gmb-post`
- [ ] **Reddit/BP**: Install Reddit MCP to enable monitoring (not just post generation)
- [ ] **LinkedIn**: Schedule via Postiz when deployed

---

## 5. AUTOMATION FIXES (Claude Does This)

- [x] Verify `scripts/freshness-scanner.py` runs without errors — 102 pages scanned, 92 issues found
- [x] Verify `scripts/output-integrity-check.py` runs without errors — 12 issues (3 banned words, 9 incomplete preps)
- [x] Verify `scripts/dedupe-checker.py` runs without errors — 185 entries, 7 potential dupes
- [x] Verify `scripts/next-best-action.py` runs without errors — 17 actions queued, top: complete Buy and Hold Spreadsheet video
- [ ] Set up cron jobs — crontab file ready at `/tmp/cron_combined.txt`, Taylor must run `crontab /tmp/cron_combined.txt` (macOS TCC permission needed)

---

## 6. TAYLOR'S MANUAL TASKS (Taylor Does This)

### This Week
- [ ] Restart Claude Code to activate TrendsMCP + Apify
- [ ] Update `data/content-registry.csv` with recent content (15 min)
- [ ] Update `data/performance-ledger.csv` with CRUSH/SOLID/MEH/MISS ratings
- [ ] Run `python3 scripts/freshness-scanner.py` to test if it works
- [ ] Install Reddit MCP (command above — one line, zero config)

### This Month
- [ ] Deploy Postiz on Railway for social media scheduling
- [ ] Enable Beehiiv Recommendations widget (free on Launch plan, organic growth)
- [ ] Start tagging leads in FUB with content source (YouTube, TikTok, Newsletter, etc.)
- [ ] Install Google Analytics MCP (command above)
- [ ] Install Apify MCP for competitor monitoring (command above)

### This Quarter
- [ ] Evaluate vidIQ MCP for YouTube intelligence
- [ ] Coach clients to mention specific neighborhoods in Google reviews (feeds GBP AI citations)
- [ ] Watch for Beehiiv MCP V2 release (will enable direct draft push from Claude)

---

## 7. KEY FACTS (For Reference)

### Best Posting Times (2026 Data)
| Platform | Best Days | Best Times (Central) |
|---|---|---|
| TikTok | Tue-Fri | 2-6 PM |
| Instagram | Tue-Wed | 10 AM-2 PM, 5-9 PM |
| YouTube Long | Thu-Sat | 2-4 PM (publish 2hrs early) |
| YouTube Shorts | Any day | Less time-sensitive |
| GMB | Weekdays | 8-10 AM |
| LinkedIn | Tue-Thu | 7-9 AM |
| BP/Reddit | Tue-Wed | 10 AM-12 PM |

### Instagram 2026 Algorithm Change
- Caption keywords now outperform hashtags for discovery
- DM shares are the #1 ranking signal for Reels
- 3-second hold rate above 60% = viral distribution threshold
- Remove TikTok watermarks (algorithm penalizes them)

### GBP + Gemini AI
- Google's Gemini now pulls from GBP posts, reviews, and description to answer local queries
- Every GMB post is an AI citation opportunity
- Reviews mentioning neighborhoods/transaction types become AI signals
