# Spark Ads Performance Tracker

## Trigger
"spark ads", "ads review", "ad performance", "sunday measurement", "boost recommendations", "tiktok ads"

## Required Inputs
- This week's Spark Ads data (Taylor provides from TikTok Ads Manager):
  - Video title / content
  - Spend
  - Impressions
  - Clicks (profile visits + website clicks)
  - Video views (2s, 6s, full)
  - Follows gained
  - Leads generated (DMs with keyword)
  - Cost per result

## Step-by-Step Execution

### Step 1 — Record This Week's Data

```markdown
## Spark Ads Report — Week of [Date]

### Active Campaigns
| Video | Spend | Impressions | Clicks | 6s Views | Follows | Leads | CPL |
|-------|-------|-------------|--------|----------|---------|-------|-----|
| [title] | $XX | X,XXX | XX | X,XXX | X | X | $X.XX |
| [title] | $XX | X,XXX | XX | X,XXX | X | X | $X.XX |
| **TOTAL** | **$XX** | **X,XXX** | **XX** | **X,XXX** | **X** | **X** | **$X.XX** |
```

### Step 2 — Calculate Key Metrics

```markdown
### Performance Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Total Spend | $XX | $XX | ↑/↓ X% |
| Cost per Click | $X.XX | $X.XX | ↑/↓ |
| Cost per 6s View | $X.XX | $X.XX | ↑/↓ |
| Cost per Follow | $X.XX | $X.XX | ↑/↓ |
| Cost per Lead | $X.XX | $X.XX | ↑/↓ |
| Click-Through Rate | X.X% | X.X% | ↑/↓ |
| 6s View Rate | X.X% | X.X% | ↑/↓ |
| Follow Rate | X.X% | X.X% | ↑/↓ |
```

### Step 3 — Content Performance Ranking
Rank all boosted videos by cost efficiency:

```markdown
### Top Performers (lowest cost per result)
1. "[title]" — $X.XX/lead, $X.XX/follow
2. "[title]" — $X.XX/lead, $X.XX/follow

### Underperformers (consider pausing)
1. "[title]" — $X.XX/lead (above $X.XX threshold)
```

### Step 4 — Budget Analysis

```markdown
### Budget Status
- Weekly budget: $XX ($XX/day)
- Spent this week: $XX (XX% of budget)
- Monthly total: $XXX
- Monthly budget remaining: $XXX
- Projected monthly spend: $XXX

### ROI Indicator
- Leads this month: X
- If 1 lead converts (avg commission $3,369): [ROI calculation]
- Break-even: X leads per month at current spend
```

### Step 5 — Next Week Recommendations

```markdown
### Boost Recommendations — Next Week

**CONTINUE (performing well):**
- "[title]" — Increase daily budget to $X
  Reason: [why it's working]

**PAUSE (underperforming):**
- "[title]" — Pause and replace
  Reason: [CPL above threshold, low engagement, etc.]

**NEW BOOST CANDIDATES:**
From this week's organic content, recommend 1-2 videos to test:
- "[title]" — Why: [organic engagement signals, topic relevance]
  Suggested daily budget: $X
  Target audience: [demographic + interest]

**CREATIVE REFRESH:**
- Any videos running >2 weeks with declining performance should get new hooks or be replaced

### Audience Targeting Notes
- Current targeting: [demographic, location, interests]
- Suggested adjustment: [any changes based on performance data]
```

### Step 6 — Monthly Summary (run on last Sunday of month)

```markdown
### Monthly Summary — [Month Year]
| Metric | Total | Avg/Week |
|--------|-------|----------|
| Spend | $XXX | $XX |
| Impressions | XX,XXX | X,XXX |
| Leads | X | X.X |
| Follows | XX | X |
| Best performer | "[title]" | $X.XX CPL |
| Worst performer | "[title]" | $X.XX CPL |

### Learnings
- Content types that perform: [patterns]
- Content types that don't: [patterns]
- Best posting times: [if data available]
- Audience insights: [demographics that engage]
```

## Output Format
Save to `output/YYYY-WXX/spark-ads-review.md`

## Quality Checks
- [ ] All numbers match Taylor's provided data (no estimates)
- [ ] Week-over-week comparison included
- [ ] At least 1 new boost candidate recommended
- [ ] Underperformers flagged for pause
- [ ] Budget status accurate
- [ ] ROI calculation based on real commission average ($3,369)

## Brand Rules
- Spark Ads = TikTok only (not YouTube ads — those are separate)
- Budget context: $10/day baseline (started 2026-03-29)
- Lead = DM with keyword, not just a profile visit
- TikTok audience = buyers/relocators only, never investor content
- Track but don't over-optimize — organic content quality comes first
