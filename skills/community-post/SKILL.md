# Skill: YouTube Community Post Writer

## Trigger
User says: "community post", "community tab", "youtube post", or when `/produce` runs (auto-include)

## Instructions

### Step 1: Identify Parameters
Ask (or infer from context):
- **Topic**: A video topic, recent video title, or general Temple TX real estate subject
- **Target Persona**: Military / Medical / Investor / General (or mix for polls)
- **Linked Video/Page**: URL to a relevant YouTube video or templetxhomes.net page (if available)

### Step 2: Read Config & Data
- Load brand voice and persona details from `social-media-config.json`
- Check `reference/TEMPLE-TX-DATA-VAULT.md` for current local data points (prices, rates, tax figures, neighborhood stats)
- Check recent video titles for linking opportunities

### Step 3: Write 3 Variations

```
## YouTube Community Posts: [Topic]

**Topic**: [topic]
**Persona Focus**: [persona or "cross-persona"]
**Linked Content**: [video title or page URL if available]

---

### VARIATION 1: The Data Poll

[2-sentence context setting up the poll. Must include a specific number or data point.]

**POLL OPTIONS:**
A) [Option — specific to Temple/Bell County]
B) [Option — specific to Temple/Bell County]
C) [Option — specific to Temple/Bell County]
D) [Option — specific to Temple/Bell County]

**LINK**: [relevant video URL or templetxhomes.net page]

---

### VARIATION 2: The "Scars & All" Post

[2-3 sentences max. Lead with the hard truth. Back it with a real number. End with what it means for the reader.]

**SUGGESTED IMAGE/CHART**: [Describe a specific visual — screenshot of tax data, chart of price trends, MLS listing screenshot, etc.]

---

### VARIATION 3: The Pop Quiz

[Question with a surprising or counterintuitive answer baked in.]

[1-sentence teaser — "Drop your guess below" or "Most people get this wrong" style hook.]

**LINK**: [Full breakdown video URL or templetxhomes.net page]

---

### POSTING SCHEDULE
- [ ] Post 1: [suggested day — e.g., "Tuesday, between uploads"]
- [ ] Post 2: [suggested day]
- [ ] Post 3: [suggested day]

### PERFORMANCE NOTES
- Community posts reach NON-subscribers — treat these as top-of-funnel discovery
- Polls get 2-5x more impressions than text posts
- Questions that invite comments boost the channel in recommendations
- Always reply to poll/quiz comments within 24 hours to trigger the algorithm
```

### Step 4: Save Output
Save to `output/YYYY-WXX/community/[topic-slug].md`

## Rules
- Always include a templetxhomes.net link in at least one variation
- Use specific Temple TX data — never generic national stats
- Pull from `reference/TEMPLE-TX-DATA-VAULT.md` when available; flag when data needs refreshing
- Polls should map to the 4 personas (investor, military, medical, luxury) when possible
- Hook must be specific: a number, a neighborhood name, a tax figure, a price point
- No agent speak — no "dream home," "charming," "nestled," "white glove," "turnkey"
- Never use "Fort Cavazos" — always "Fort Hood" (name reverted July 2025)
- Never use "turnkey investors" — always "buy-and-hold"
- Post 2-3x per week between video uploads for maximum organic reach
- Community posts are the #1 free organic growth hack on YouTube — they surface to non-subscribers in Home and Explore feeds
- Keep text short and scannable — mobile-first formatting
- Every poll option should be defensible; no obvious joke answers
