# Competitor Content Gap Analyzer

## Trigger
"competitor gap", "content gap", "what are competitors doing", "gap analysis", "competitor audit"

## Required Inputs
- Optional: specific competitor name or channel to analyze
- Optional: specific content pillar to focus on

## Default Competitor List
Monitor these Temple TX real estate competitors:

**YouTube Channels:**
1. [To be populated — Taylor to provide 3-5 competitor channel names/URLs]

**Websites:**
1. [To be populated — Taylor to provide 3-5 competitor website URLs]

**BiggerPockets:**
1. Search for "Temple TX" content from other agents

## Step-by-Step Execution

### Step 1 — Catalog Competitor Content
For each competitor, catalog their recent content (last 90 days):

```markdown
| Competitor | Platform | Title | Topic | Date | Est. Views/Engagement |
|-----------|----------|-------|-------|------|----------------------|
| [name] | YouTube | [title] | [topic] | [date] | [views] |
```

### Step 2 — Map to Content Pillars
Categorize each competitor piece into pillars:
- Neighborhood Tours
- Market Data / Updates
- Investor Education
- Relocation Guides
- Listing Showcases
- How-To / Process
- Personal Brand / Vlogs
- Comparison Videos

### Step 3 — Cross-Reference Against Taylor's Content
Compare competitor catalog against:
- `data/living-in-temple-catalog.txt`
- `data/investing-in-temple-catalog.txt`
- `data/content-registry.csv`

Identify:
```markdown
## Topics Competitors Cover That Taylor Doesn't
| Topic | Covered By | Taylor's Coverage | Gap Severity |
|-------|-----------|-------------------|-------------|
| [topic] | [competitor] | None | 🔴 HIGH |
| [topic] | [competitor] | Outdated (>6mo) | 🟡 MEDIUM |

## Topics Taylor Covers That Competitors Don't (MOAT)
| Topic | Taylor's Coverage | Competitor Coverage |
|-------|-------------------|-------------------|
| [topic] | [video/page] | None |

## Topics Both Cover (BATTLEGROUND)
| Topic | Taylor's Version | Competitor's Version | Who's Better? |
|-------|-----------------|---------------------|---------------|
| [topic] | [link] | [link] | [assessment] |
```

### Step 4 — Search Volume Estimation
For gap topics, estimate search demand:
- Check YouTube autocomplete for the topic
- Check Google autocomplete
- Note: we cannot pull exact search volume without API access — estimate as HIGH/MEDIUM/LOW based on autocomplete presence

### Step 5 — Gap-Fill Recommendations

```markdown
## Top 10 Content Gaps (Ranked by Impact)

### Gap 1: [Topic]
- **Covered by:** [competitor]
- **Search signal:** [HIGH/MEDIUM/LOW]
- **Recommended format:** [YouTube Long / Blog / TikTok / Newsletter]
- **Target persona:** [Military / BSW / Investor / Relocator]
- **Content pillar:** [pillar]
- **Suggested title:** [title]
- **Differentiation angle:** [how Taylor can do it better]
- **Effort estimate:** [LOW/MEDIUM/HIGH]
- **Priority score:** [1-10]

### Gap 2: [Topic]
...
```

### Step 6 — Competitive Advantages to Protect
List Taylor's content moats that competitors haven't touched:
- Data depth (MLS + CAD + PropStream)
- Investor-specific content (BRRRR, buy-and-hold analysis)
- Neighborhood-level granularity
- Honest negatives (Scars and All)
- Schema/AEO optimization
- BiggerPockets authority

## Output Format
Save to `output/audits/competitor-gap-YYYY-MM-DD.md`

## Quality Checks
- [ ] At least 3 competitors analyzed
- [ ] Cross-referenced against Taylor's full content catalog
- [ ] Gaps ranked by search demand × effort
- [ ] Each gap has a specific content recommendation
- [ ] Moats identified and flagged for protection
- [ ] No recommendations for content Taylor already covers well

## Brand Rules
- Never recommend copying competitor content — find Taylor's unique angle
- Data-first differentiation: Taylor has MLS/CAD/PropStream access
- Honesty differentiation: competitors avoid negatives, Taylor includes them
- Never salesy framing in recommendations
- Fort Hood (not Fort Cavazos)

## IMPORTANT: Manual Input Needed
This skill requires Taylor to provide:
1. 3-5 competitor YouTube channel names/URLs
2. 3-5 competitor website URLs
3. Any known competitor BiggerPockets profiles

Without this, the skill can only analyze based on YouTube/Google search results for "Temple TX real estate" related queries.
