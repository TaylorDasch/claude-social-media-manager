# Skill: /weekly-scorecard — Content Production Scorecard

## Trigger
"weekly scorecard", "scorecard", "what did I produce", "content review", "pipeline check", "weekly review", "/weekly-scorecard"

## What It Does
Scans your actual output folders and compares what was produced vs. the weekly content rhythm. Surfaces wins, gaps, streaks, and the single highest-impact thing to do next. This is your Friday afternoon 5-minute review.

## Instructions

### Step 1: Determine the Week
- Default to the current ISO week (YYYY-WXX format)
- If Taylor specifies a different week, use that instead
- Calculate the Monday-Sunday date range for display

### Step 2: Scan Output Folders
Read the contents of these directories:
```
output/YYYY-WXX/           # Main weekly output
output/YYYY-WXX/produced/  # /produce pipeline output
output/YYYY-WXX/blog/      # /transcript-to-blog output
output/YYYY-WXX/deal-of-the-week/
output/YYYY-WXX/community/
output/YYYY-WXX/linkedin/
output/YYYY-WXX/tiktok/
output/YYYY-WXX/youtube/
output/YYYY-WXX/newsletter/
output/YYYY-WXX/gmb/
output/YYYY-WXX/repurposed/
output/audits/              # AEO audits (check date in filename)
```

Also check:
- `yt-videos/` for any new video prep folders created this week (check file modification dates)

### Step 2.5: Pull Live Platform Data (MCP)

Before scoring, pull real-time data from connected platforms.

**YouTube** (both "Living in Temple" and "Investing in Temple" channels):
- Call `youtube_list_videos` to get recent uploads from each channel
- Call `youtube_get_video_stats` for each video published this week (views, likes, comments, watch time, CTR)
- Summarize: total views this week, top-performing video, avg CTR

**Newsletter (Beehiiv):**
- Call `newsletter_stats` to pull latest newsletter performance
- Call `list_subscribers` to get current subscriber count
- Report: open rate, click rate, subscriber count, growth since last week

**Leads (Follow Up Boss):**
- Call `list_people` with date filter for this week's new leads
- Cross-reference lead `source` field to count leads by content channel (YouTube, TikTok, Website, Newsletter, Referral, etc.)
- Report: total new leads this week, breakdown by source

If any MCP call fails or returns no data, mark that section `[MCP UNAVAILABLE]` and continue with file-based scoring.

### Step 3: Score Against the Weekly Rhythm
Reference `reference/CONTENT-PRODUCTION-CHECKLIST.md` weekly rhythm:

| Target | Expected | Status |
|--------|----------|--------|
| YouTube long-form script | 1/week | Check output/youtube/ or yt-videos/ |
| Deal of the Week package | 1/week | Check output/deal-of-the-week/ |
| TikTok scripts | 3-5/week | Check output/tiktok/ or produced/*/tiktok-clip-*.md |
| YouTube Short script | 1-2/week | Check produced/*/youtube-short.md |
| Blog post (transcript or original) | 1/week | Check output/blog/ |
| Newsletter segment | 1/week | Check output/newsletter/ or produced/*/newsletter-segment.md |
| GMB post | 3-5/week | Check output/gmb/ or produced/*/gmb-post.md |
| Community post | 2-3/week | Check output/community/ |
| Social captions (dual frame) | 1-2/week | Check produced/*/social-captions.md |
| LinkedIn carousel | 0-1/week | Check output/linkedin/ (only if investor/BSW content) |
| BiggerPockets engagement | 1-2/week | Not tracked in output — ask Taylor |
| AEO page audit | 1/week | Check output/audits/ |

### Step 4: Check Production Pipeline Status
Scan for incomplete work:
- Files in `yt-videos/` that have research but no script yet
- Deal of the Week packages missing components (script exists but no blog outline)
- `/produce` runs that generated partial output (e.g., TikTok clips but no schema pack)

### Step 5: Generate the Scorecard

```markdown
# Weekly Scorecard: YYYY-WXX (Mon Date - Sun Date)

## Production Score: X/12 targets hit

| Content Type | Target | Produced | Status |
|-------------|--------|----------|--------|
| YT Long-form | 1 | [count] | [check]/[X] |
| Deal of the Week | 1 | [count] | [check]/[X] |
| TikTok scripts | 3-5 | [count] | [check]/[X] |
| YT Short | 1-2 | [count] | [check]/[X] |
| Blog post | 1 | [count] | [check]/[X] |
| Newsletter | 1 | [count] | [check]/[X] |
| GMB posts | 3-5 | [count] | [check]/[X] |
| Community posts | 2-3 | [count] | [check]/[X] |
| Social captions | 1-2 | [count] | [check]/[X] |
| LinkedIn carousel | 0-1 | [count] | [check]/[X] |
| BP engagement | 1-2 | ? (ask) | [?] |
| AEO audit | 1 | [count] | [check]/[X] |

## Platform Performance (Live Data)

### YouTube
- Views this week: [X]
- Top video: "[title]" — [X] views, [X]% CTR
- Subscribers: [X] (+[X] this week)

### Newsletter (Beehiiv)
- Latest issue: "[subject]" — [X]% open, [X]% click
- Subscribers: [X] (+[X] since last issue)

### Leads (FUB)
- New leads this week: [X]
- By source: YouTube [X], TikTok [X], Website [X], Newsletter [X], Other [X]

## Wins This Week
- [List any content produced, with file paths]
- [Note any multi-platform /produce runs — these are high-value]

## Gaps
- [List what's missing, ranked by impact]
- [For each gap: suggest the fastest fix — e.g., "Run /produce on [existing script] to generate TikTok + GMB + newsletter in one pass"]

## Pipeline Status
- **In Progress:** [files in yt-videos/ or output/ that are partial]
- **Ready to Film:** [scripts that exist but no video recorded yet]
- **Ready to Deploy:** [content generated but not yet published]

## Streak Tracker
- Weeks with Deal of the Week: [count consecutive]
- Weeks with blog post: [count consecutive]
- Weeks with all targets hit: [count consecutive]

## #1 Highest-Impact Action for Next Week
[Single specific action that would produce the most downstream content. Usually: "Film [topic] on Tuesday, then run /produce to generate 10+ assets from it."]
```

### Step 6: Compare to Previous Weeks (if available)
If output folders exist for prior weeks, show trend:
```
W10: 4/12 | W11: 6/12 | W12: 8/12 | W13 (this week): X/12
```

### Step 7: Save Output
Save to `output/YYYY-WXX/scorecard.md`

## Rules
- Be honest about gaps — no "great job!" if half the targets were missed
- Always suggest the single highest-leverage action (usually filming + /produce)
- Count actual files, not intentions. A script that exists is produced. A plan to write one is not.
- If output/ folder for the week doesn't exist at all, say so clearly: "No output folder for this week. Either content wasn't generated through the skill system, or it was done outside Claude."
- BP engagement can't be tracked from output files — always mark it as "?" and ask Taylor
- Streak tracking only works when prior week scorecards exist. Start tracking from the first scorecard run.

## Dependencies
- Reads `output/` directory structure
- Reads `yt-videos/` for video prep status
- References `reference/CONTENT-PRODUCTION-CHECKLIST.md` for weekly targets
- Saves to `output/YYYY-WXX/scorecard.md`
- YouTube MCP tools: `youtube_list_videos`, `youtube_get_video_stats`
- Beehiiv MCP tools: `newsletter_stats`, `list_subscribers`
- FUB MCP tools: `list_people`
