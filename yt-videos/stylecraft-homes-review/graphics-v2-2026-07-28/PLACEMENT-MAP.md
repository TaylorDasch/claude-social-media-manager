# Stylecraft Review — Graphics v2 · Placement Map

**Source transcript:** `~/Downloads/0727.srt` (235 cues · runtime 9:52.7)
**Built:** 2026-07-28 · **Namespace:** `F##` / `O##` — no collision with Codex's `G##` pack
**Assets:** `fullframe-1080/` (9 opaque) · `overlays-1080/` (19 alpha PNG)

Every graphic below is anchored to a line Taylor actually says in *this* cut. Timestamps are
lifted from the SRT cue boundaries, so they drop straight onto the CapCut timeline.

---


**F3, F5 and F2 are long holds by design** — they're multi-element cards. If you want the
face back sooner, reveal the elements in sequence rather than trimming the card.

---

## Transparent overlays (19) — sit over Taylor, face stays on screen

| # | File | IN | OUT | Hold | Spoken anchor |
|---|------|----|----
|
| O4 | `O4-flex-uses` | **1:30.3** | 1:36.4 | 6.1s | "spend on upgrades / buying down the rate / closing cost covered" |
| O5 | `O5-kangaroo` | **2:27.8** | 2:36.5 | 8.7s | "you have to use the Stylecraft lender… Stylecraft owns 49% of that company" |
| O6 | `O6-lender-fork` | **2:42.9** | 2:51.3 | 8.4s | "welcome to use your own lender… they're going to give you flex cash" |
| O7 | `O7-not-only` | **2:53.4** | 3:01.9 | 8.5s | "Stylecraft is not the only builder in Bell County who's offering the 4.99%" |
| O8 | `O8-location` | **3:38.4** | 3:44.4 | 6.0s | "this is Hartrick Ranch… brick siding and then you have James Hardie" |
|
=
| O14 | `O14-insurance` | **6:47.3** | 6:54.0 | 6.7s | "whenever you buy a new construction home the insurance is significantly cheaper" |
| O15 | `O15-right-for` | **6:59.1** | 7:14.3 | 15.2s | "one of the number one value builders in Temple… you know $220,000" |
| O16 | `O16-not-for` | **7:47.2** | 8:02.0 | 14.8s | "if you want to make a bunch of customizations… or the more premium side" |
| O17 | `O17-comps` | **8:30.2** | 8:52.3 | 22.1s | "closest comparison would be Omega Homes… not the Kiella finishes… not the D.R. Horton price point" |
| O18 | `O18-floorplan` | **9:04.8** | 9:11.0 | 6.2s | "1818 floor plan right here, this is my favorite floor plan" |
| O19 | `O19-endcard` | **9:46.7** | 9:52.7 | 6.0s | "full link to everything… right down below in the description" |

**O17 holds 22s** — reveal the three chips in sequence (Omega at 8:30, Kiella at 8:43,
D.R. Horton at 8:46) rather than popping all three at once.

---

## CapCut handling

- **Overlays** — track above A-roll, fitted default, centered. 6-frame fade in/out.
- **Full-frame** — hard cut or 4-frame dissolve. Don't fade; it reads as a mistake.
- **O1** is the only top-anchored graphic. Everything else lives in the lower third.
- Nothing is branded before **0:11** — the cold open stays clean per the hook rule.

---

## Claim controls

- **F1 / F2 / O1 / O2** carry the time-sensitive financing offer. Terms verified July 26, 2026.
  Re-check before export; if the promo rotates, re-render those four.
- **O11** attributes plumbing/drainage to the **published complaint record** and carries Taylor's
  clean-closings disclosure. It is not a firsthand defect claim. Keep it that way.
- **F8** is Taylor's own category judgment, not an average of public review scores — the source
  line says so on the card. **O12** sets up why.
- No builder logos anywhere. All original Living in Temple graphics.

---

## Re-render

```bash
cd ~/claude-social-media-manager/yt-videos/stylecraft-homes-review/graphics-v2-2026-07-28/build && node render.js
```

Single card: `node render.js F2-payment-math`. Edit `stylecraft-graphics.html`, re-run, done.
