# Thumbnail Briefs — Video #1: Data Center

**A/B Test Setup:** Upload all 3 to YouTube Studio → Content → select video → Test & Compare. Let run 14 days minimum. Log winner pattern to `data/thumbnail-winners.csv`.

**Anatomy rules (all 3 must pass):**
- Face ~33% of frame · clear emotion matching title · NOT smiling for this video
- 3–5 word text overlay · BIG and BOLD · readable at 200px mobile
- Text DIFFERENT from title ("Don't Buy a House in Temple Because of Meta — Here's Why")
- High contrast · saturated colors · no Canva script fonts
- Bell County recognizable visual · year stamp present

---

## THUMBNAIL A — "$1.5B / 150 JOBS?"

**Concept:** Carry the Capital-to-Jobs Ratio Meter (the killer page graphic) directly into the thumbnail. The number contrast is the curiosity engine.

**Layout:**
- Aspect: 1280 × 720 (16:9)
- Background: aerial / wide shot of Meta site (cranes visible, scale visible) — capture during Tuesday drive loop. If aerial not feasible, ground-level "looking up at construction" angle works.
- Background color treatment: dark navy filter, slight desaturation, green grass crop visible
- Text overlay: `$1.5B / 150 JOBS?` — top-left, Outfit Bold or similar sans-serif, white with emerald-green underline accent, 200px text height
- Taylor's face: right 1/3 of frame, eyes-to-camera, "skeptical eyebrow raised" — analytical disbelief (NOT angry, NOT happy)
- Year stamp: small `2026` badge bottom-right corner, white on emerald
- Optional micro-element: a small "?" icon at the end of the text overlay in red

**Color palette (hex):**
- Background base: `#1e293b` (dc-midnight)
- Text: `#f8fafc` (dc-snow)
- Accent: `#10b981` (dc-emerald-glow)
- Question mark accent: `#ef4444` (red)

**AI image-gen prompt (for nano-banana-pro or similar):**
> Wide-aspect 16:9 thumbnail composition. Left 60%: cinematic aerial photograph of a massive data center construction site in a Texas plain, multiple yellow cranes silhouetted against an early-evening sky, ground torn up showing scale, dark navy color grade. Right 40%: realistic photographic portrait of Taylor Dasch (use uploaded reference photo), professional male real estate agent in his 30s, light-colored shirt, eyes fixed direct-to-camera, one eyebrow slightly raised conveying analytical skepticism (NOT angry, NOT smiling). Massive bold sans-serif text overlay top-left reading "$1.5B / 150 JOBS?" — white text with emerald-green underline accent. Bottom-right small white "2026" badge on emerald-green background. Mobile-optimized at 200px width. High contrast. Cinematic editorial quality.

**Hypothesis:** Wins on the curiosity-driven viewer who needs to know what the ratio means. Best for the analytical relocator persona (BSW physicians).

---

## THUMBNAIL B — "DON'T"

**Concept:** Single-word thumbnails dominate mobile CTR. The word "DON'T" with a visual cue to the topic creates maximum pattern interrupt.

**Layout:**
- Aspect: 1280 × 720
- Background: Meta data center crane silhouette against a dusk-orange sky (or use stock Texas construction site if direct capture not available). Dramatic lighting.
- Text overlay: `DON'T` — giant, centered-left, white text, drop shadow, ~320px text height
- Sub-element: small `Buy?` badge under the DON'T (white text on red), with a red prohibited slash through the word
- Taylor's face: right side, looking direct-camera, finger pointing across the frame toward the construction site, "warning / no-go" emotion (concerned, not angry)
- Year stamp: `TEMPLE TX 2026` small white-on-red badge bottom-right

**Color palette:**
- Background gradient: dusk orange-amber to dark gray
- Text: pure white with subtle drop shadow
- Accent: bright red `#dc2626` for the slash/badge

**AI image-gen prompt:**
> Wide 16:9 thumbnail. Background: silhouette of a yellow construction crane against dusk orange-to-dark-gray sky over a Texas industrial site, dramatic lighting. Foreground left-center: massive bold sans-serif white text "DON'T" with subtle drop shadow filling 40% of the frame width. Below the DON'T, a small white text "Buy?" with a bright red diagonal slash through it. Right 30%: realistic photographic portrait of Taylor Dasch from uploaded reference, professional 30s male agent, light shirt, looking direct-to-camera with concerned-but-controlled expression, right index finger pointing left across the frame toward the construction site. Bottom-right corner: small "TEMPLE TX 2026" badge in white on bright red background. Mobile-readable at 200px wide. High contrast.

**Hypothesis:** Wins on raw CTR — single-word pattern interrupt. Best for cold algorithm sampling (Browse / Home recommendations).

---

## THUMBNAIL C — "1.5B vs. 150"

**Concept:** Pure-numbers framing for the search-driven viewer. Different psychological hook than A and B.

**Layout:**
- Aspect: 1280 × 720
- Background: split graphic
  - Left half: stylized stack of dollar bills / hundred-dollar-bill texture
  - Right half: vast empty open-plan office space with a single tiny stick figure (visual rep of the ratio)
  - Center: subtle vertical division
- Text overlay top: `1.5B vs. 150` — gold/yellow `#fbbf24`, BIG, bold, top-third of frame
- Taylor's face: bottom-right, bust shot, professional explaining gesture (palms-up open hands), neutral analytical look
- Year stamp: top-right `TEMPLE TX 2026` badge

**Color palette:**
- Background: matte black `#0f172a`
- Numbers: gold/yellow `#fbbf24`
- Accents: white
- Money texture: green-tinted hundred-dollar-bill green

**AI image-gen prompt:**
> Wide 16:9 thumbnail with matte black background. Vertical split composition: left half shows stylized photographic stack of US one-hundred dollar bills filling the space, slight green tint. Right half shows a vast empty open-plan office with bright white fluorescent lighting and a single tiny stick-figure silhouette of one person in the center, conveying scale and emptiness. Top of frame: massive bold gold-yellow sans-serif text "1.5B vs. 150" filling 60% of the frame width. Bottom-right quadrant: realistic photographic portrait of Taylor Dasch from uploaded reference, professional male agent in his 30s, light shirt, neutral analytical expression with open explaining-hands gesture. Top-right corner: small white "TEMPLE TX 2026" badge. Mobile-readable at 200px wide.

**Hypothesis:** Wins on long-watch retention — pulls the analytical viewer who clicks for the data and stays for the explainer. Best for suggested-video traffic (where viewers self-select for analytical content).

---

## SUMMARY MATRIX

| Variant | Best For | Hypothesis |
|---------|----------|------------|
| A — $1.5B / 150 Jobs? | Analytical relocators (BSW physicians) | Curiosity-driven CTR + high engagement |
| B — DON'T | Cold algorithm sampling | Raw CTR / pattern interrupt |
| C — 1.5B vs. 150 | Suggested videos / long retention | Analytical viewer, longest AVD |

## PRODUCTION

- Generate via `nano-banana-pro` skill, OR
- Brief a designer with the layouts above, OR
- Build in Figma using AgentPrompt-style AI persona model (Taylor's likeness, already established for prior thumbnails)
- File names: `thumb-01-DC-A-ratio.png`, `thumb-01-DC-B-dont.png`, `thumb-01-DC-C-numbers.png`
- Save to `thumbnails/` folder at project root

## REJECT (do not produce)

- "Smiling Taylor + construction site + thumbs up" — wrong emotion for hook
- "IT'S COMING!" caption with drone shot — replicates every other agent's data center thumbnail
- Any thumbnail with a generic stock building/office photo — needs Bell County identity
- Any thumbnail with text in dainty script fonts — fails mobile readability
