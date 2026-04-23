# Skill: Instagram Reel Prep Sheet

## Triggers
"instagram reel", "reel about", "instagram about [topic]", "IG reel", "film this for instagram"

## Purpose
Generate a Reel prep sheet optimized for Instagram's algorithm (not a TikTok repurpose — per feedback, each platform gets native content). Covers hook, shot sequence, text overlays, audio direction, and CTA. Designed for 30-60s vertical video.

## Parameters

| Parameter | Required | Source |
|-----------|----------|--------|
| Topic / property / angle | Yes | Taylor provides |
| Persona target | Yes | Taylor specifies or Claude infers from topic |
| Content pillar | Yes | Must map to one of the 5 pillars in social-media-config.json |
| Property details (if tour) | Conditional | Address, price, beds/baths/sqft if property content |

Valid personas:
- **BSW Medical** — commute, physician loans, professional lifestyle
- **Military** — BAH, Fort Hood proximity, PCS-friendly
- **General / Relocator** — schools, lifestyle, commute, value
- **Luxury Buyer** — $600K+, custom builds, acreage, privacy

NO investor content on Instagram (investors stay on YouTube + BiggerPockets).

## Execution

### Step 1 — Confirm Parameters
If Taylor drops a topic with no details, ask for persona + pillar. If property tour, need address + price + beds/baths/sqft.

### Step 2 — Load Config
Read `social-media-config.json` for:
- Instagram hashtag tiers
- Active CTA keywords
- Brand voice + banned words from governance/QUALITY-GATES.md

### Step 3 — Generate Reel Prep Sheet

Output the template below. Every section mandatory.

### Step 4 — Save Output
Save to: `output/YYYY-WXX/instagram/[topic-slug].md`

---

## Output Template

```markdown
# Instagram Reel Prep — [Topic/Address]

## Target
- **Persona:** [BSW Medical / Military / Relocator / Luxury]
- **Pillar:** [from config contentPillars]
- **Goal:** [awareness / engagement / lead capture]

## Hook (First 1.5 Seconds)
> [Text overlay + what's on screen — must stop the scroll]

**Why this hook works:** [1 sentence]

## Shot Sequence (30-60s)

| # | Time | Shot | Text Overlay | Audio Note |
|---|------|------|-------------|------------|
| 1 | 0-2s | [Hook shot — face/property/data] | [Hook text] | [Music drop / voiceover starts] |
| 2 | 2-8s | [Context establishing] | [Supporting text] | [Continue VO] |
| 3 | 8-18s | [Core value — the thing they came for] | [Key stat or insight] | [VO or trending audio] |
| 4 | 18-25s | [Proof / visual evidence] | [Data or before/after] | |
| 5 | 25-30s | [CTA shot — face to camera] | [CTA text overlay] | [Direct VO] |

## Text Overlays (exact copy)
1. Hook: "[exact text]"
2. Supporting: "[exact text]"
3. Key insight: "[exact text]"
4. CTA: "[exact text]"

## Audio Direction
- **Style:** [trending audio / original voiceover / VO + music bed]
- **Audio reference:** [specific trend or vibe if applicable]
- **Pacing:** [fast cuts / slow reveal / match-on-action]

## Caption
[150-300 words, micro-blog style. Front-load with searchable keywords (neighborhood name, "Temple TX", price range, buyer type). Write as if the caption IS the search result. Question or hot take to drive comments and DM shares. No agent speak.]

## Hashtags (3-5 total, 2026 algorithm)
Pick 3-5 most relevant: 1 broad, 1 niche, 1-3 local. Caption keywords do the discovery work now.

## CTA
- **In-video:** [what Taylor says/shows]
- **Caption:** [DM keyword or link-in-bio direction]
- **Story share:** [yes/no + story-specific hook if yes]

## Instagram-Specific Notes
- [ ] Thumbnail frame selected (not auto — pick the most scroll-stopping frame)
- [ ] Cover text added (for grid display)
- [ ] Alt text written (accessibility + SEO)
- [ ] Collab tag if featuring another creator/business
- [ ] Location tag: Temple, TX
```

## Differentiation from TikTok

| Aspect | TikTok | Instagram Reel |
|--------|--------|----------------|
| Length sweet spot | 15-45s | 30-60s |
| Hook window | 0.5s | 1.5s |
| Audio | Trending sounds critical | VO + music bed performs better |
| Hashtags | 3-5 | 3-5 (keyword-dense caption) |
| CTA | DM keyword | Link in bio + DM keyword |
| Caption length | Short + DM CTA | 150-300 words (micro-blog) |
| Grid appearance | N/A | Cover image matters for profile grid |
| Cross-post | NEVER repurpose to TikTok | NEVER repurpose from TikTok |
| Content | Original filming | Original filming |

## Instagram 2026 Algorithm Notes
- Caption keywords outperform hashtags for discovery — write keyword-dense captions
- DM shares are the #1 ranking signal for Reels (design for shareability)
- 3-second hold rate above 60% = viral distribution threshold
- Remove TikTok watermarks if cross-posting (algorithm penalizes them)
- Collab tags extend reach to both audiences — use when featuring local businesses

## Quality Gate Checks (inherited from governance/)
- [ ] No banned words (Gate 1)
- [ ] Entity declaration within first caption sentence (Gate 2)
- [ ] Data point sourced from TEMPLE-TX-DATA-VAULT.md (Gate 3)
- [ ] Honest negative included if property content (Gate 4)
- [ ] Not same pillar as last published Reel (Gate 12)
