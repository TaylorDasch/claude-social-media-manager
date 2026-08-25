# Skill: /weekly-analytics-pull — Weekly Platform Data Consolidation

## Trigger
"analytics pull", "pull analytics", "weekly data", "platform stats", "sunday pull", "/weekly-analytics-pull"

## What It Does
Consolidates live platform data from all connected MCP tools into a single weekly performance snapshot. Run this Sunday evening — the output feeds Monday's /weekly-scorecard with real numbers.

## Instructions

### Step 1: Determine the Week
- Default to the current ISO week (YYYY-WXX)
- Calculate the Monday-Sunday date range

### Step 2: Pull YouTube Data
- Call `youtube_list_videos` for both channels and filter to videos published this week.
- Treat Data API `viewCount` as **Public starts** only. Starting `2026-08-24`, it counts first-frame/autoplay starts and is not comparable to the earlier public-view definition. Never label it impressions, engaged views, or qualified views.
- For Taylor's owned channel, use authenticated YouTube Analytics data when available:
  - `engagedViews`
  - `estimatedMinutesWatched` (convert to watch-time hours)
  - `averageViewDuration`
  - `averageViewPercentage`
  - audience-retention curve / 30-second retention
  - thumbnail CTR by traffic source from an authenticated MCP, Studio export, or Reporting API source
- If private access is unavailable, write `Private analytics unavailable` for each missing metric. Never backfill CTR, retention, watch time, AVD, or engaged views from public counts.
- Calculate best/worst performance from engaged views, watch time, CTR, AVD, and retention. Public-view lift alone cannot produce a winner/loser call or content recommendation.
- Pull stats for YouTube Shorts separately

**Transition requirement:** snapshots `2026-W36` and `2026-W37` must display Public starts and Engaged views as separate rows and carry the `2026-08-24 measurement break` note. Do not calculate a week-over-week percentage for Public starts when the comparison crosses the break.

### Step 3: Pull Beehiiv Data
- Call `list_posts` to find newsletters sent this week
- Call `newsletter_stats` for each issue sent
- Call `list_subscribers` to get current count
- Calculate: open rate, click rate, top-clicked link, subscriber growth

### Step 4: Pull GSC Data
- Call `query_search_analytics` for templetxhomes.net, last 7 days
- Call `get_top_pages` to identify top 10 pages by clicks
- Call `find_keyword_opportunities` for striking-distance keywords (positions 5-20)
- Calculate: total impressions, total clicks, avg CTR, avg position

### Step 5: Pull FUB Lead Data
- Call `list_people` filtered to this week's new leads
- Cross-reference source tags to count by channel
- Calculate: total new leads, leads by source (YouTube, TikTok, Website, Newsletter, Referral, Walk-in, Other)

### Step 6: Pull Google Maps Data
- Call `maps_local_rank_tracker` for key terms:
  - "real estate agent Temple TX"
  - "homes for sale Temple TX"
  - "realtor near me Temple TX"
  - "Temple TX homes"
- Record ranking position for each term

### Step 7: Generate Weekly Snapshot

Output format:
```markdown
# Weekly Analytics Snapshot — YYYY-WXX (Mon Date - Sun Date)
Generated: [timestamp]

## YouTube
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Public starts (Data API; non-comparable across 2026-08-24) | [X] | [X] | [N/A across break] |
| Engaged views (owner analytics) | [X or unavailable] | [X or unavailable] | [+/-X% or unavailable] |
| Watch time (hours) | [X or unavailable] | [X or unavailable] | [+/-X% or unavailable] |
| New subscribers | [X] | [X] | [+/-X] |
| Thumbnail CTR | [X]% | [X]% | [+/-X%] |
| Average view duration | [M:SS] | [M:SS] | [+/-S sec] |
| 30-second retention | [X]% | [X]% | [+/-X pp] |
| Videos published | [X] | [X] | |

> **Measurement break — 2026-08-24:** Public starts use the first-frame/autoplay definition and are not comparable with the earlier public-view definition. Strategy decisions below use owner-only engaged views, watch time, CTR, AVD, and retention; never public-view lift alone.

### Top Videos This Week
1. "[title]" — [X] public starts, [X] engaged views, [X]% CTR, [X] min avg watch
2. "[title]" — [X] public starts, [X] engaged views, [X]% CTR, [X] min avg watch

### Shorts Performance
| Short | Public starts | Engaged views | Likes | Comments |
|-------|---------------|---------------|-------|----------|
| "[title]" | [X] | [X or unavailable] | [X] | [X] |

## Newsletter (Beehiiv)
| Metric | Latest Issue | Previous | Change |
|--------|-------------|----------|--------|
| Open rate | [X]% | [X]% | [+/-X%] |
| Click rate | [X]% | [X]% | [+/-X%] |
| Subscribers | [X] | [X] | +[X] |

## Website (GSC)
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Impressions | [X] | [X] | [+/-X%] |
| Clicks | [X] | [X] | [+/-X%] |
| Avg CTR | [X]% | [X]% | [+/-X%] |
| Avg position | [X] | [X] | [+/-X] |

### Top Pages by Clicks
1. /[slug]/ — [X] clicks, position [X]
2. /[slug]/ — [X] clicks, position [X]
3. /[slug]/ — [X] clicks, position [X]

### Keyword Opportunities (Striking Distance)
| Keyword | Position | Impressions | Page |
|---------|----------|-------------|------|
| [keyword] | [X] | [X] | /[slug]/ |

## Leads (FUB)
| Source | Count | % of Total |
|--------|-------|-----------|
| YouTube | [X] | [X]% |
| TikTok | [X] | [X]% |
| Website | [X] | [X]% |
| Newsletter | [X] | [X]% |
| Referral | [X] | [X]% |
| Other | [X] | [X]% |
| **Total** | **[X]** | |

## Local Ranking (Google Maps)
| Search Term | Position | Change |
|-------------|----------|--------|
| real estate agent Temple TX | [X] | [+/-X] |
| homes for sale Temple TX | [X] | [+/-X] |
| realtor near me Temple TX | [X] | [+/-X] |
| Temple TX homes | [X] | [+/-X] |

## Key Takeaways
1. [Biggest win this week]
2. [Biggest concern or drop]
3. [Recommended action for next week]
```

### Step 8: Save Output
Save to `output/YYYY-WXX/analytics-snapshot.md`
Also save raw data as `output/YYYY-WXX/analytics-raw.json` for historical comparison.

### Step 9: Compare to Previous Week
If previous week's analytics-raw.json exists, calculate all "Change" columns.
If not, mark Change columns as "N/A (first pull)".

## Rules
- Only report real data from MCP tools — never estimate or fabricate
- If an MCP tool fails or returns no data, note it as "[tool] unavailable" and continue
- Never use Data API `viewCount` as a proxy for impressions, CTR, engaged views, watch time, AVD, or retention.
- Never recommend a topic, title, thumbnail, or publishing change from Public starts lift alone.
- Always include the "Key Takeaways" section with 3 specific, actionable insights
- Save raw JSON alongside the markdown for week-over-week comparison
- This skill feeds /weekly-scorecard — format data so scorecard can reference it directly

## Dependencies
- YouTube public MCP/Data API: `youtube_list_videos`, `youtube_get_video_stats`
- YouTube owner analytics: authenticated channel analytics / retention / traffic-source tools or Studio export. API metric names: `engagedViews`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, and `audienceWatchRatio`.
- Beehiiv MCP: `list_posts`, `newsletter_stats`, `list_subscribers`
- GSC MCP: `query_search_analytics`, `get_top_pages`, `find_keyword_opportunities`
- FUB MCP: `list_people`
- Google Maps MCP: `maps_local_rank_tracker`
- Saves to `output/YYYY-WXX/analytics-snapshot.md` and `output/YYYY-WXX/analytics-raw.json`
