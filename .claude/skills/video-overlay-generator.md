# Video Overlay Generator

## Trigger
"video overlay", "create graphic", "data overlay", "branded graphic", "overlay for", "b-roll graphic", "matplotlib graphic"

## Required Inputs
- Graphic type (see types below)
- Content/data to display
- Optional: specific style reference (e.g., "like the 109 Raven map" or "like the Canyon Creek pros/cons")

## Graphic Types

### 1. Stats Card
6 stat boxes in 2x3 grid. Each box: large value, label, sublabel.
Best for: neighborhood snapshots, market summaries.

### 2. Pros & Cons Split
Left panel (emerald) vs right panel (coral). Bullet points with icons.
Best for: honest neighborhood analysis, comparison videos.

### 3. Buyer Profile Card
3 boxes in a row showing ideal buyer types + "NOT ideal for" box.
Best for: neighborhood tours, targeting content.

### 4. Price Ladder / Gradient
Horizontal gradient bar showing price progression with callout boxes below.
Best for: streets with price diversity, market range videos.

### 5. Premium Location Map (Dark Ops Style)
Dark satellite grid background, glowing emerald route lines, neon pin markers with glow rings.
Reference: `listing-domination-os/active-listings/109-raven/listing-page/109-raven-map-premium.png`
Best for: commute analysis, location context.

### 6. Timeline
Horizontal timeline with era markers, description cards below.
Best for: build year ranges, market history, neighborhood evolution.

### 7. Comparison Table
Side-by-side columns with header, stats, and verdict.
Best for: Temple vs Killeen, neighborhood vs neighborhood, rent vs buy.

### 8. Radial Location
Center "YOU ARE HERE" badge with radiating connection lines to nearby amenities.
Best for: location context, what's nearby.

### 9. Summary / End Card
3-column layout summarizing property, deal, and ideal buyer.
Best for: video end screens, recap moments.

### 10. CTA Card
Split layout: avatar/credentials on left, pitch + process on right.
Best for: call-to-action moments, "reach out to me" segments.

### 11. Process Flow
3-4 step cards with arrows between them, numbered steps.
Best for: how-it-works explanations, funnel visualization.

### 12. School District Advisory
Two-panel: district info + alternative recommendation.
Best for: ISD callouts in neighborhood tours.

## Step-by-Step Execution

### Step 1 — Determine Type
Match the content to the best graphic type from above. If unclear, ask.

### Step 2 — Build with Matplotlib
All graphics use this technical spec:
```python
fig, ax = plt.subplots(1, 1, figsize=(19.20, 10.80), dpi=100)  # 1920x1080
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
```

### Brand Colors (MANDATORY):
```python
MIDNIGHT = '#1e293b'     # Primary background
EMERALD = '#059669'      # Accent, positive, CTA
SNOW = '#f8fafc'         # Text on dark
CORAL = '#ef4444'        # Negative, warnings, cons
AMBER = '#d97706'        # Money, deals, caution
SKY = '#0ea5e9'          # Secondary accent
VIOLET = '#8b5cf6'       # Tertiary accent
DARK_BG = '#0a0f1a'      # Ultra-dark for premium/map style
CARD_BG = '#0f1b2d'      # Card background
MUTED = '#94a3b8'        # Muted text
```

### Standard Layout Elements:
- **Top accent bar:** 50px high, full width, accent color
- **Title:** Serif font, 36-40pt, centered
- **Subtitle:** Sans-serif, 13pt, accent color, centered
- **Cards:** FancyBboxPatch with round corners, 2.5px border, card bg
- **Top stripe on cards:** 8px high accent color stripe
- **Bottom bar:** 80px high, #0f172a background, emerald line at top
- **Footer text:** "TAYLOR DASCH  •  EG REALTY  •  254-718-4249"

### Step 3 — Handle Dollar Signs
Matplotlib interprets `$` as LaTeX math mode. Always escape: `\\$` in f-strings, or use raw strings.

### Step 4 — Save
Save as PNG to `claude-social-media-manager/` or relevant output folder.
Filename convention: `[topic]_[type].png` (e.g., `canyon_creek_pros_cons.png`)

### Step 5 — Verify
Read the saved PNG back to visually confirm rendering.

## Output Format
- 1920x1080 PNG at 100 DPI
- Branded with all standard layout elements
- Filename follows convention

## Quality Checks
- [ ] Resolution is exactly 1920x1080
- [ ] All brand colors used correctly
- [ ] Dollar signs render properly (not eaten by LaTeX)
- [ ] Text is readable at YouTube video scale
- [ ] Bottom bar includes Taylor's contact info
- [ ] No typos in displayed text
- [ ] Fort Hood (not Fort Cavazos) if location appears
- [ ] No banned words

## Brand Rules
- Dark premium aesthetic — matches templetxhomes.net
- Fonts: serif for titles, sans-serif for body/labels
- Cards use CARD_BG (#0f1b2d) not pure black
- Emerald for positive/CTA, coral for negative, amber for money
- Every graphic must have the branded bottom bar
