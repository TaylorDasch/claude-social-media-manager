# Stylecraft Review — Video Graphics v2

Built 2026-07-28 against the **actual filmed transcript** (`~/Downloads/0727.srt`), not the
prepared script. Replaces nothing — this pack lives in its own `F##`/`O##` namespace and does
not collide with the earlier `G##` pack in `../video-graphics-2026-07-26/`.

## What's here

```
fullframe-1080/   9 opaque 1920×1080 PNGs  (F1–F9)  — cutaway cards
overlays-1080/   19 alpha  1920×1080 PNGs  (O1–O19) — lower-thirds over Taylor
previews/         contact sheets (overlays composited over a bright test backdrop)
build/            stylecraft-graphics.html + render.js + brand assets
PLACEMENT-MAP.md  ← every graphic with its IN/OUT timecode and spoken anchor
```

Start with **PLACEMENT-MAP.md**. That's the drop-in sheet.

## Why this pack is overlay-heavy

19 of 28 graphics are transparent overlays that sit in the lower third so Taylor's face stays
on screen. Full-frame cutaways are reserved for the nine moments that genuinely earn the
screen — the offer fork, the payment math, the warranty timeline, the tax trap, the verdict.

## Design system

Taylor's locked premium look: **Cormorant Garamond** headlines and numerals, **JetBrains Mono**
eyebrows and labels, **Outfit** body, on **midnight #0f172a** tiers over a faint Temple twilight
aerial. Emerald `#10b981` used sparingly, slate-azure `#8fb3d4` for the comparison side, amber
`#f59e0b` only for caution and tax. Brand mark bottom-left, attribution bottom-right. Fonts are
bundled locally in `build/assets/fonts/` — no network needed to re-render.

## Re-render

```bash
cd build && node render.js
```

Single card: `node render.js F2-payment-math O5-kangaroo`

Drives the system Chrome (Playwright's bundled chromium isn't installed on this machine).

**Do not remove the `background: transparent` line in `render.js`.** Without it every overlay
silently renders opaque and blacks out the frame — see `bug-2235` in `.wolf/buglog.json`.

## Numbers on screen

The payment card is computed, not estimated — $315,000 loan, 30-yr fixed, P&I only:

| Rate | Payment | vs 4.99% |
|---|---|---|
| 4.99% | $1,689.06 | — |
| 6.50% | $1,991.01 | +$301.95/mo → $18,117 / 5yr |
| 6.80% | $2,053.56 | +$364.50/mo → $21,870 / 5yr |

The card shows the **range** rather than a single figure, which keeps it true across the whole
6.5–6.8% band Taylor quotes on camera — and keeps his spoken "$300/month" and "$20,000 over
five years" both inside the printed numbers.
