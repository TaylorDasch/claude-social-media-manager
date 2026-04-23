# Skill: Thumbnail & Cover Image Brief

## Triggers
"thumbnail", "thumbnail for [video]", "cover image", "CTR image", "youtube thumbnail", "video thumbnail"

## Purpose
Generate a detailed thumbnail brief that Taylor (or a designer) can execute. Covers composition, text overlay, emotion/expression direction, color treatment, and A/B test variants. Optimized for YouTube CTR but applicable to any video platform.

## Parameters

| Parameter | Required | Source |
|-----------|----------|--------|
| Video title | Yes | Taylor provides |
| Video topic / angle | Yes | Taylor provides |
| Target persona | Yes | Taylor specifies or Claude infers |
| Platform | Optional | Default: YouTube. Also: TikTok cover, Instagram Reel cover |

## Execution

### Step 1 — Load Context
Read `reference/YOUTUBE-GROWTH-PLAYBOOK.md` for thumbnail best practices.
Read `social-media-config.json` for brand colors and current video series.

### Step 2 — Analyze Title
Parse the video title for:
- Primary keyword (what the viewer is searching)
- Emotional trigger (curiosity, fear, excitement, disbelief)
- Data point (if number-driven title)

### Step 3 — Generate Thumbnail Brief

### Step 4 — Save Output
Save to: `output/YYYY-WXX/thumbnails/[video-slug]-thumbnail.md`
If part of a `/yt-video` package, also save inside `yt-videos/[slug]/thumbnail-brief.md`

---

## Output Template

```markdown
# Thumbnail Brief — [Video Title]

## Concept (1 sentence)
[What the viewer should FEEL when they see this thumbnail]

## Composition

### Layout
- **Style:** [face + text | property + text | split screen | before/after | data callout]
- **Rule of thirds:** [where Taylor's face goes, where text goes, where property/data goes]
- **Background:** [property exterior | interior room | map | solid color gradient]

### Taylor's Expression / Pose
- **Expression:** [shocked | pointing | arms crossed | looking at property | analyzing data]
- **Eye direction:** [looking at camera | looking at text/arrow | looking at property]
- **Wardrobe note:** [if relevant — e.g., "professional for luxury, casual for neighborhood tour"]

### Text Overlay
- **Primary text:** "[EXACT TEXT — max 4 words, high contrast]"
- **Secondary text:** "[Optional supporting text — max 3 words]"
- **Font:** Bold sans-serif, readable at mobile size
- **Color:** [White on dark | Yellow on dark | Emerald (#059669) accent]
- **Placement:** [top-left | center-right | bottom with gradient bar]

### Color Treatment
- **Dominant:** [from brand palette or property colors]
- **Contrast element:** [red arrow, yellow highlight, emerald accent]
- **Saturation:** [boost slightly for scroll-stopping pop]
- **Border/outline:** [Taylor cutout with slight glow | no border | colored frame]

### Data Callout (if applicable)
- **Number:** [e.g., "$145K", "2.1% Cap Rate", "3 min to BSW"]
- **Style:** [large bold overlay | speech bubble | price tag graphic]

## A/B Test Variants

### Variant A — [Emotion-Led]
[Description: Taylor's face prominent, emotional expression, minimal text]

### Variant B — [Data-Led]
[Description: Property/data prominent, Taylor smaller or absent, bold number]

### Variant C — [Curiosity-Led]
[Description: Partial reveal, arrow pointing at something, "You won't believe..." energy without the clickbait words]

## CTR Optimization Checklist
- [ ] Readable at mobile size (thumbnail is 120x90px on mobile — text must be legible)
- [ ] Face visible (thumbnails with faces get 30%+ more clicks)
- [ ] Contrasts with YouTube's white/red UI (avoid pure red or white backgrounds)
- [ ] Does NOT duplicate the title — thumbnail complements, doesn't repeat
- [ ] Passes the "would I click this?" test at arm's length on a phone
- [ ] Consistent with channel branding (viewers should recognize it's Taylor's video)

## Platform-Specific Notes

### YouTube
- 1280x720px minimum (16:9)
- File size < 2MB
- Test both variants — swap at 48h if CTR < 4%

### Instagram Reel Cover
- Square crop version needed for grid (1:1)
- Must work WITHOUT text (text often hidden on grid)
- Pick the most visually striking freeze frame + add minimal text

### TikTok Cover
- 9:16 vertical
- Text at center (top/bottom get cut by UI)
- Bold, simple — 2 words max
```

## Reference: What Works for Taylor's Channel

Based on existing video performance data:
- **Affordable/price-specific titles WIN** (Cimmaron 3.1x, Lake Pointe 2.6x, South Pointe 2.6x)
- **Face + number + property = highest CTR combo**
- **Negative hooks outperform positive** ("Don't Buy Here" > "Best Place to Live")
- **Map/aerial shots work for neighborhood content**
- **Before/after works for investor content**

### Step 5 — Canva MCP (Optional — Generate Actual Thumbnail)
- After generating the brief, offer to create an actual thumbnail using Canva MCP
- Call `generate-design-structured` with: format "YouTubeThumbnail", title text, subtitle text, and style direction from the brief
- Call `export-design` to get the download URL
- Include the Canva design link in the output

## Quality Gate Checks
- [ ] No agent speak in text overlay
- [ ] Brand colors present (emerald #059669 or midnight #1e293b)
- [ ] At least 2 A/B variants provided
- [ ] Mobile-readable text check noted

## Dependencies
- Canva MCP tools: `generate-design-structured`, `export-design`
