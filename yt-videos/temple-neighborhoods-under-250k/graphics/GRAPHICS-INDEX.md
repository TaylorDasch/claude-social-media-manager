# Graphics & Cards — "5 Best Temple Neighborhoods Under $250K"
Built 2026-06-18 · 30 PNGs @ 3840×2160 (4K) · drop into CapCut over the matching VO line.

- **Full-frame** (`01`–`10`, `MAP_*`): opaque, fill the frame. Per the overlay rule, full-screen is OK here (data/maps).
- **Overlays** (`LT_*`, `ST_*`, `ISD_*`): **transparent PNG**, sit bottom-left lower-third. Keep your talking head visible.
- Re-render anytime: `cd graphics && python3 build.py && python3 build_maps.py && python3 render.py`
- Source HTML is in `html/` — edit text there or in `build*.py`, then re-render.

## Cue sheet (in script order)

| Script cue | File | Type | Notes |
|---|---|---|---|
| COLD OPEN — "TEMPLE, TX — 5 NEIGHBORHOODS UNDER $250K" | `01_title.png` | full-frame | Cold-open title |
| INTRO lower-third "Taylor Dasch · Real Estate Agent · EG Realty" | `LT_name.png` | overlay | Name bug, first 25s |
| INTRO card "$250K = NEW or ESTABLISHED" | `02_framework.png` | full-frame | The two-option framing |
| #5 Alta Vista — on-screen card | `03_altavista.png` | full-frame | Stat card |
| #5 — "Alta Vista is **Academy ISD**" | `ISD_academy.png` | overlay | The school differentiator (gold) |
| #5 — walk/talk name bug (optional) | `LT_altavista.png` | overlay | Rank + median + drive |
| #5 — MAP: Alta Vista → BSW · 8 min | `MAP_altavista.png` | full-frame | Route map |
| #4 Oak Ridge — on-screen card | `04_oakridge.png` | full-frame | Stat card |
| #4 — "Streets: Cilantro · Saffron · Turmeric · Oregano" | `ST_oakridge.png` | overlay | Spice streets |
| #4 — MAP: Oak Ridge → BSW · 11 min | `MAP_oakridge.png` | full-frame | Route map |
| #4 — "Temple ISD — Garcia Elem → Lamar MS → Temple High" | `ISD_oakchain.png` | overlay | School chain |
| #4 — walk/talk name bug (optional) | `LT_oakridge.png` | overlay | |
| #3 Heritage Place — on-screen card | `05_heritage.png` | full-frame | Stat card |
| #3 — "Streets: Roanoke · Jamestown · Vicksburg · Petersburg" | `ST_heritage.png` | overlay | Colonial streets |
| #3 — MAP: Heritage Place → BSW · 9 min | `MAP_heritage.png` | full-frame | Route map |
| #3 — "Temple ISD" | `ISD_temple.png` | overlay | Generic ISD chip |
| #3 — walk/talk name bug (optional) | `LT_heritage.png` | overlay | |
| #2 Western Hills — on-screen card | `06_western.png` | full-frame | Stat card |
| #2 — "Streets: Apache · Comanche · Brazos · Chisholm" | `ST_western.png` | overlay | Native/river streets |
| #2 — MAP: Western Hills → BSW · 8 min | `MAP_western.png` | full-frame | Route map |
| #2 — walk/talk name bug (optional) | `LT_western.png` | overlay | |
| #1 Canyon Creek — on-screen card | `07_canyon.png` | full-frame | **Gold "crown" tier** |
| #1 — "Streets: Bordeaux · Brighton · Chelsea · Kensington" | `ST_canyon.png` | overlay | French/English streets |
| #1 — MAP: Canyon Creek → BSW · 5 min · CLOSEST | `MAP_canyon.png` | full-frame | **Gold route map** |
| #1 — walk/talk name bug (optional) | `LT_canyon.png` | overlay | Gold |
| HONORABLE MENTION — Cimarron card | `08_cimarron.png` | full-frame | Stat card (HM) |
| HM — walk/talk name bug (optional) | `LT_cimarron.png` | overlay | |
| RECAP — "all five, minutes from BSW" | `09_recap.png` | full-frame | Leaderboard by drive time |
| Anytime you say "all within 12 min of BSW" | `MAP_master.png` | full-frame | **Hero proximity map** — great B-roll / pinned-comment image |
| CLOSE / CTA | `10_cta.png` | full-frame | Budget + must-haves CTA |

## Data notes
- All on-screen drive times = the **script's spoken times** (video already filmed). Independently re-verified on Google Maps Jun 18 2026: **Canyon Creek 5 min and Heritage 9 min match exactly.** Alta Vista (8), Western (8), Oak Ridge (11) are kept as you said them on camera; my fresh pull from the subdivision centroids came back a touch longer (likely a different representative address) — flagged, not changed, so graphics match your VO.
- `MAP_master.png` node positions = real geocoded compass bearings from BSW (Google Maps, Jun 18 2026), hand-spaced for legibility. Canyon Creek is correctly the closest.
- Prices/sqft/era/active counts = CTX MLS June 18 2026 pull, City=Temple, ≤ $250K.
