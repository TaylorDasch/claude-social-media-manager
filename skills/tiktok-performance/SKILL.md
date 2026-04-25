# Skill: /tiktok-performance — TikTok Trend Intelligence

## Trigger
"tiktok trends", "tiktok performance", "trending hashtags", "what's trending on tiktok", "/tiktok-performance"

## What It Does
Pulls trending hashtags and topics relevant to Temple TX real estate, cross-references against your content registry to find gaps and opportunities, and generates trend-aligned content suggestions that feed into /content-calendar.

## Instructions

### Step 1: Pull Trending Data (TrendsMCP)
Use TrendsMCP.ai tools to pull:
- Trending hashtags in category: Real Estate
- Trending hashtags in location: Texas / Temple TX area
- Trending sounds/audio relevant to home tours, lifestyle, relocation
- Rising trends (not just peak trends — catch them on the way up)

Key search terms to check trends for:
- "Temple TX homes"
- "moving to Texas"
- "first time home buyer"
- "military relocation"
- "house tour"
- "home for sale"
- "real estate agent"
- "BSW Temple" / "medical professional relocation"

> **Note:** TrendsMCP is not currently connected. When available, discover tools via `ToolSearch("trend")`. Until then, flag that trend data is unavailable and use manual research or skip to Step 2 with registry-only analysis.

### Step 2: Cross-Reference Content Registry
Read `data/content-registry.csv` and check:
- Which trending topics have NO matching content in the registry?
- Which trending topics have content that's >30 days old (opportunity to refresh)?
- Which trending hashtags are NOT in the current hashtag tiers in `social-media-config.json`?

### Step 3: Score Opportunities
For each gap, score 1-10 based on:
- **Trend velocity** (5 pts): How fast is it growing? Rising > peak > declining
- **Audience match** (3 pts): Does it match Taylor's personas (BSW Medical, Military, Relocator)?
- **Content readiness** (2 pts): Can Taylor film this in the next 7 days? Does he have a property that fits?

### Step 4: Generate Output

```markdown
# TikTok Trend Intelligence — [Date]

## Trending Now (Real Estate + Local)

### Hashtags
| Hashtag | Volume | Velocity | In Our Rotation? |
|---------|--------|----------|-----------------|
| #[hashtag] | [X] views | Rising/Peak/Declining | Yes/No |

### Trending Audio
| Audio | Usage Count | Fit for Taylor? | Content Idea |
|-------|-------------|-----------------|-------------|
| [audio name] | [X] uses | Yes/Maybe/No | [idea] |

## Content Gaps (No Registry Match)
| Trend | Score | Suggested Content | Persona | Format |
|-------|-------|-------------------|---------|--------|
| [trend] | [X]/10 | [specific content idea] | [persona] | [property tour / talking head / etc.] |

## Refresh Opportunities (Existing Content + Trending Again)
| Existing Content | Published | Trend Match | Suggested Action |
|-----------------|-----------|-------------|-----------------|
| [title] | [date] | [trend] | Re-film / Update / Remix |

## Hashtag Rotation Update
Suggested additions to `social-media-config.json` hashtag tiers:
- **Broad**: [new hashtags to add]
- **Niche**: [new hashtags to add]
- **Local**: [new hashtags to add]

## Top 3 TikToks to Film This Week
1. **[Topic]** — [Why: trend + persona match + property available]
   - Hook: "[hook line]"
   - Property: [suggest type or specific if obvious]
   - Persona: [target]
2. ...
3. ...
```

### Step 5: Save Output
Save to `output/YYYY-WXX/tiktok-trends.md`

### Step 6: Feed into Content Calendar
If a content calendar for this week already exists (`output/YYYY-WXX/content-calendar.md`), suggest amendments. If not, note that the top 3 TikToks should be included when `/content-calendar` is next run.

## Rules
- TikTok = original property tours ONLY. Never suggest repurposing YouTube content.
- NO investor content on TikTok. No cap rates, no cash-on-cash, no "great investment." If a trend is investor-focused, skip it or find the owner-occupant angle.
- Trend data must be real — if TrendsMCP returns no data for a query, say so. Don't fabricate trend volumes.
- Always include "Top 3 TikToks to Film This Week" — this is the actionable output Taylor acts on.
- Cross-referencing the content registry is mandatory — don't suggest content that already exists unless it's a deliberate refresh.
- Use "Fort Hood" not "Fort Cavazos"

## Dependencies
- TrendsMCP tools (check available tools via ToolSearch — not yet connected)
- Reads `data/content-registry.csv` for existing content
- Reads `social-media-config.json` for hashtag tiers and personas
- Saves to `output/YYYY-WXX/tiktok-trends.md`
- Feeds into `/content-calendar`
