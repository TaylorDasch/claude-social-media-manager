# Skill: Weekly Content Calendar Generator

## Trigger
User says: "content calendar", "plan this week", "what should I post", "weekly plan"

## Instructions

### Step 1: Determine the Week
- Check the current date
- Identify Monday-Sunday of the current (or next) week
- Note any special dates: holidays, seasonal content windows (Q2 migration, Q4 physician leads, etc.)

### Step 2: Read Config
- Load `social-media-config.json`
- Check current TikTok ramp phase (early growth = 5 videos/week)
- Check video series status (Deal of the Week = every Tuesday)
- Check pillar rotation — review last week's output to avoid repeating same pillar back-to-back

### Step 2.5: Pull Keyword + News Data

#### Google Search Console
- Call `find_keyword_opportunities` to find keywords where templetxhomes.net ranks positions 5-20 (striking distance)
- Call `get_top_pages` to see which pages are gaining/losing traffic
- Use opportunities to inform content topics — create content targeting keywords where the site is close to page 1

#### RSS Feeds
- Call `fetch_blogs` or `fetch_by_category` for real estate news feeds
- Scan headlines for timely hooks (rate changes, market data releases, local news)
- Suggest 1-2 "timely" content pieces based on current news

### Step 3: Generate Calendar

For each day Monday-Friday (+ optional Sat/Sun), output:

```
## [Day], [Date]

### TikTok
- **Pillar**: [pillar name]
- **Hook**: [specific hook from hook bank or new hook]
- **Format**: [talking head / property tour / walk-and-talk / etc.]
- **Posting Window**: [time from schedule]
- **CTA**: DM me "[KEYWORD]"
- **Hashtags**: [platform-specific set]

### Instagram Reels (repurposed)
- **Caption Style**: Story-style, longer format
- **Hashtag Adjustments**: [IG-specific swaps]

### YouTube Shorts (repurposed)
- **Title**: [search-optimized, includes "Temple TX"]

### Other Platforms
- **GBP Post**: [Post type from 4-week rotation: Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip] — Target AI query: [the Gemini question this post answers] — Post 8-10 AM weekday (see skills/gmb-post/SKILL.md for full templates)
- **BP/Reddit**: [if scheduled — topic and target sub/thread]
- **Newsletter**: [if newsletter day — section topics]
```

### Step 4: Tuesday Special — Deal of the Week
If Tuesday is in the week:
- Include Deal of the Week package plan
- YouTube video script outline (8-12 min)
- Blog post topic (2,000+ words)
- Short/Reel version (60 sec)
- Social post caption

### Step 5: Filming Day Prep
For filming days (Tuesday primary, Friday secondary):
- List all scripts/hooks to film
- Note outfit changes needed (different-day appearance)
- B-roll shot list (neighborhoods, streets, restaurants)
- Equipment reminders (4K, vertical crop, gimbal for tours)

### Step 6: Save Output
Save to `output/YYYY-WXX/content-calendar.md`

## Output Format
Markdown file with the full week laid out. Each day is a section. Include checkboxes so Taylor can track completion.

Append these sections at the end of the calendar output:

```
## Keyword Opportunities This Week
[List striking-distance keywords from GSC with current position, impressions, and suggested content angle]

## Timely Hooks (from RSS)
[1-2 news items with headline, source, and how to spin into content]
```

## Dependencies
- GSC MCP tools: `find_keyword_opportunities`, `get_top_pages`
- RSS MCP tools: `fetch_blogs`, `fetch_by_category`
