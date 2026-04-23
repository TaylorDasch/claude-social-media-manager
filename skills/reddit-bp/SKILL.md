# Skill: Reddit & BiggerPockets Post

## Triggers
"reddit post", "BP post", "biggerpockets post", "forum post", "reddit about [topic]", "BP thread"

## Purpose
Draft data-heavy forum posts for Reddit (r/realestateinvesting, r/RealEstate, r/FirstTimeHomeBuyer, r/MilitaryFinance) and BiggerPockets forums. These platforms reward genuine insight — NOT marketing. Taylor's edge is real Temple data and active investor experience.

## Parameters

| Parameter | Required | Source |
|-----------|----------|--------|
| Platform | Yes | Reddit or BiggerPockets (different formats) |
| Subreddit / BP forum | Yes | Taylor specifies or Claude recommends based on topic |
| Topic / angle | Yes | Taylor provides |
| Data points to include | Optional | Claude pulls from TEMPLE-TX-DATA-VAULT.md |

## Platform Rules

### Reddit
- **NO links in body for first 30 days of posting** in a new sub
- Lead with personal experience or hard data — never promotional
- Match the sub's tone: r/realestateinvesting is analytical, r/FirstTimeHomeBuyer is supportive
- Flair selection matters — recommend the right one
- Comments > Posts for building karma early

### BiggerPockets
- **NO video links** (per Taylor's feedback — BP penalizes video drops)
- **NO outbound links for Month 1-2** — pure value
- Personal deal experience is gold: "$27M+ in transactions, 100+ deals"
- Month 3+: soft newsletter link in signature/bio only
- BP Pro members respond better to data-backed analysis
- 4 closed deals already attributed to BP — this channel works

## Execution

### Step 1 — Identify Target
Confirm platform + subreddit/forum + topic. If Taylor just says "post about Temple investing," recommend the best sub/forum for that angle.

### Step 2 — Load Data
Read `reference/TEMPLE-TX-DATA-VAULT.md` for relevant market data.
Read `reference/BP-ENGAGEMENT-PLAYBOOK.md` for BiggerPockets-specific rules.

### Step 3 — Generate Post

### Step 4 — Save Output
Save to: `output/YYYY-WXX/forum/[platform]-[topic-slug].md`

---

## Output Template — Reddit

```markdown
# Reddit Post Draft

**Subreddit:** r/[subreddit]
**Flair:** [recommended flair]
**Title:** [Question or data-hook format — NOT clickbait]

---

**Post Body:**

[Opening — personal experience or surprising data point, 1-2 sentences]

[Core content — 3-5 paragraphs with specific numbers, real deal examples, honest negatives. Structure as numbered list or clear sections if >300 words]

[Closing — open-ended question to invite discussion, NOT a CTA]

---

**Engagement plan:**
- Reply to every comment within 24h
- If asked for more detail → DM (never public link drop)
- If asked about agent services → "DM me, happy to chat" (not promotional)
```

## Output Template — BiggerPockets

```markdown
# BiggerPockets Forum Post Draft

**Forum:** [Buying & Selling / Real Estate Investing / Market Trends / etc.]
**Title:** [Data-forward, analytical — BP audience expects depth]

---

**Post Body:**

[Personal credibility hook — "I've done [X] deals in Temple, TX and here's what the numbers actually look like..."]

[Core analysis — multiple data points, real cap rates/cash flow/ARV numbers from Taylor's experience. Use tables for comparisons. Include honest negatives.]

[Insight that can't be Googled — something only an active local investor would know]

[Discussion prompt — NOT a CTA. "Curious if anyone else is seeing this in their market?"]

---

**Do NOT include:**
- Video links
- Website links (Month 1-2)
- "DM me for more" in the post itself
- Generic advice available on any real estate blog

**Engagement plan:**
- Reply with additional data when asked
- Reference specific deals (anonymized) as proof points
- If asked about Temple specifically → this is the funnel moment, offer to chat via DM
```

## Quality Gate Checks
- [ ] No banned words (Gate 1)
- [ ] No outbound links (if Month 1-2 on the platform)
- [ ] At least 3 specific data points from TEMPLE-TX-DATA-VAULT.md or personal deals
- [ ] At least 1 honest negative / risk / downside included
- [ ] No promotional language — reads like a peer sharing experience
- [ ] Entity declaration: "I'm an agent/investor in Temple, TX" (disclosure, not pitch)
- [ ] Closing is a discussion question, not a CTA
