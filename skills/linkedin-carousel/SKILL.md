# Skill: LinkedIn Carousel Builder

## Trigger
User says: "linkedin", "carousel", "linkedin post", "linkedin carousel", or when `/repurpose` runs on investor/BSW content

## Instructions

### Step 1: Identify Parameters
Ask (or infer from context):
- **Content Type**: Deal Breakdown / Market Update / Property Analysis / Investor Education
- **Topic**: Specific subject (e.g., "Temple TX cap rate analysis", "BSW relocation BAH breakdown", "Bell County tax protest ROI")
- **Target Persona**: Investor / BSW Medical / Military Officer / High-Net-Worth Relocator
- **Source Material**: Existing content to repurpose (YouTube script, deal of the week, newsletter segment) or new topic

### Step 2: Read Config + Data
- Load brand voice and strategy from `social-media-config.json`
- Pull real data from `reference/TEMPLE-TX-DATA-VAULT.md`, MLS, or CAD sources
- Check `reference/LEAD-MAGNET-MATRIX.md` for persona-matched CTA
- Read `/Users/taylordasch_1/open-claw/feedback-log.md` for content feedback patterns

### Step 3: Build the Carousel Outline

```
## LinkedIn Carousel: [Title]

**Content Type**: [type]
**Target Persona**: [persona]
**Slide Count**: [5-7]

---

### SLIDE 1 — Contrarian Data Hook
[Bold statement with a specific number that stops the scroll. Must challenge conventional wisdom or reveal a non-obvious insight.]
HEADLINE: "[Hook — max 8 words]"
SUBTEXT: "[One sentence with the specific data point]"
VISUAL: [Dark background (#1e293b), large white number, emerald (#059669) accent]

### SLIDE 2 — Context / Setup
[Why this matters. Set the frame. One key data point that establishes credibility.]
HEADLINE: "[Framing statement]"
DATA POINT: [Exact number from real source]
VISUAL: [Chart/graph suggestion if applicable]

### SLIDE 3 — The Math (Part 1)
[First piece of the step-by-step analysis. Show your work.]
HEADLINE: "[Key insight]"
DATA POINT: [Exact number]
VISUAL: [Table, comparison, or calculation breakdown]

### SLIDE 4 — The Math (Part 2)
[Second piece of analysis. Build on Slide 3.]
HEADLINE: "[Key insight]"
DATA POINT: [Exact number]
VISUAL: [Chart/graph suggestion or side-by-side comparison]

### SLIDE 5 — The Math (Part 3) [Optional — use for complex topics]
[Third piece of analysis or the result/conclusion of the math.]
HEADLINE: "[Key insight]"
DATA POINT: [Exact number]
VISUAL: [Result visualization]

### SLIDE 6 — The Scars / Risks
[What could go wrong. Foundation issues, insurance costs, tax protest reality, market headwinds. This is Taylor's differentiator — sophisticated investors respect honesty.]
HEADLINE: "What Could Go Wrong"
RISK 1: [Specific risk with number]
RISK 2: [Specific risk with number]
RISK 3: [Specific risk with number]
VISUAL: [Warning/caution styling with emerald accent]

### SLIDE 7 — Lead Magnet CTA
[Persona-matched from reference/LEAD-MAGNET-MATRIX.md]
HEADLINE: "[Value offer]"
CTA: "Comment [KEYWORD] and I'll DM you the [deliverable]"
VISUAL: [Taylor's headshot, contact info, clean CTA design]

---

### LINKEDIN POST CAPTION
[Analytical, authoritative tone. NOT casual like TikTok. Open with the contrarian hook restated as a question or bold claim. 3-5 sentences max before "See the full breakdown" pointing to the carousel. End with a question to drive comments.]

### HASHTAGS
[3-5 hashtags — mix of broad + niche + local]
Examples: #RealEstateInvesting #TexasRealEstate #TempleTX #BellCounty #MilitaryPCS

### POSTING WINDOW
[Tue-Thu, 8-10 AM CST — peak professional LinkedIn engagement]

### DESIGN NOTES
- [ ] Brand colors: #1e293b (midnight background), #059669 (emerald accents), #f8fafc (snow text)
- [ ] Fonts: Cormorant Garamond (headlines), Outfit (body/data)
- [ ] Taylor's headshot on Slide 7: https://assets.agentfire3.com/uploads/sites/2128/2025/11/TaylorDaschImage.jpg
- [ ] Export as PDF for LinkedIn document post upload
- [ ] Each slide: one headline, one data point, minimal text (under 50 words)
- [ ] Include "Taylor Dasch | EG Realty" footer on every slide
```

### Step 4: Save Output
Save to `output/YYYY-WXX/linkedin/[day]-[content-type]-[topic-slug].md`

## Rules
- Every slide must contain at least one specific number — no vague claims
- Data must come from real sources (reference/TEMPLE-TX-DATA-VAULT.md, MLS, CAD, PropStream). Flag estimates clearly
- Never use agent speak ("dream home," "charming," "nestled," "white glove," "turnkey")
- Use "buy-and-hold investors" not "turnkey investors"
- Use "Fort Hood" not "Fort Cavazos" (name reverted July 2025)
- Include "Temple TX" or "Bell County" in the hook for local SEO signal
- Tone is analytical and authoritative — write for a room of analysts, not first-time buyers
- Slide 6 (Scars/Risks) is non-negotiable — never skip it
- CTA must use persona-matched lead magnet from reference/LEAD-MAGNET-MATRIX.md
- Hashtags follow three-tier system (1-2 broad, 1-2 niche, 1-2 local)
- LinkedIn document posts get 5.85% engagement rate — highest format on the platform. Optimize for saves and shares
