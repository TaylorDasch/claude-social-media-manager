# Belton — Top 5 Neighborhoods, Ranked
## Edit Decision List + Graphics Placement
*Source video: `0614 (1)(1).srt` · Channel: Living in Temple · Taylor Dasch / EG Realty*
*Graphics: `graphics/png/` (4K PNG, brand system) · Data verified vs Central TX MLS (belton-only, trailing 12-mo closed sales)*

---

## PART 1 — EDITS NEEDED (do these first)

### A. Hard cuts (remove from final)
| # | Where (spoken) | ~Time | Why |
|---|----------------|-------|-----|
| A1 | "vamos a voy a caminar hacia ti okay" | ~7:58 | Spanish aside to videographer — not for audience |
| A2 | "okay vamos a hacer cambiarlo otra vez" | ~8:24 | Spanish camera direction — cut |
| A3 | "for a quick summary… for a quick summary here… we're going to go over for a quick summary here" | ~13:06–13:12 | Says "quick summary" 3× — trim to ONE clean line |

### B. Factual fixes (correct on screen — graphics already carry the right numbers)
| # | He said | Reality (MLS / geography) | Fix |
|---|---------|---------------------------|-----|
| B1 ⚠️ | "shoot the other way to the military base **Corpus Christi** Killeen area" | The base by Killeen is **Fort Cavazos (Fort Hood)**; the town is **Copperas Cove**. Corpus Christi is a coast city ~200 mi south. | **Trim the word "Corpus Christi"** (likely meant Copperas Cove). If kept, overlay a text correction "Fort Cavazos · Killeen." This is the one real error. |
| B2 | Three Creeks builders incl. "**Omega**" | Omega has **0 closed sales** in Three Creeks in the data. Verified builders: **D.R. Horton, Stylecraft, Tippit, Carothers**. | Builder chip graphic shows the verified 4 (no Omega). Optional: trim "Omega" mention. |
| B3 | Dawson "all the way up to **$700,000**" | Closed-sale max = **$580K**; $700K = active/anecdotal. | Graphic range shows $283K–$580K + "anecdotal ceiling ~$700K." Soft — leave audio, let graphic govern. |
| B4 | Lake "**$238**/sqft … **$720K** … **92 days**" | MLS = **$248/sqft · $765K median · 96 days**. | Graphic uses corrected figures. Directionally right; optional 1-line VO patch (ElevenLabs "Dasch YT Voice") if you want audio to match. |
| B5 | Morgan's "**$242K**" / recap "$240K" | MLS median = **$246.5K** (range $160K–$825K). | No fix needed — graphic shows $247K and is the on-screen authority. |

> **Transcription-only artifacts — NO edit needed (audio is correct):** "12/22 square feet" = 1,200–2,200 sf; "18 square foot home" = 1,800 sf; "1 79 per square foot" = $179. These are .srt mis-renders; your spoken audio is fine. Graphics carry the correct numbers.

### C. Pace tightening (optional, channel "change every 7s" rule)
- Morgan's Point: you say "so keep that in mind" ~4× in 90s — trim to 2.
- ~9:19–9:21 dead "okay / alright" — tighten.
- ~5:16–5:22 second builder list partly repeats the first — trim one pass.
- Every neighborhood hand-off is a hard location cut → **drop the full-frame stat card on the cut** (covers the jump + resets attention).

---

## PART 2 — GRAPHICS PLACEMENT (after edits)
*Placements key off the spoken line so they survive re-cutting. File = `graphics/png/<name>.png`.*

| Cue (spoken) | ~Raw time | Graphic | Type | Hold |
|--------------|-----------|---------|------|------|
| "Stylecraft, Tippit, D.R. Horton… Carothers" | ~4:25 | *(builder chips visible on `05`)* | hold/zoom card | — |
| "most sales in Belton for the last year" | ~4:45 | `POP_threecreeks_sales` | Stat pop (pre-made) | 2s |
| Walking Three Creeks | 4:15–6:00 | `LT_threecreeks` | Lower-third | as needed |
| "shoot over to Baylor Scott & White… or the military base… right in the middle" | ~5:35–5:58 | `11_threecreeks_map` | Full-frame commute map | hold 6–8s (also corrects the Corpus Christi slip, B1) |
| "quick pit stop… property taxes" | 6:06 | `08_tax` | Full-frame explainer | hold 6:06–7:13 |
| "Dawson Ranch and… Dawson Ridge" (cut) | 7:14 | `06_dawson` | Full-frame stat card | 4–6s |
| "outgrown the home… relocating here to Temple" | ~7:18 / 8:33 | `12_dawson_map` | Full-frame convenience hub | hold 6–8s |
| "29 sales… 2,280 sq ft… $180/sf" | 7:28 / 8:05 | `POP_dawson_sales` / `POP_dawson_size` | Stat pop (pre-made) | 2s each |
| Walking Dawson | 7:20–10:30 | `LT_dawson` | Lower-third | as needed |
| "what separates Belton from Temple… lake neighborhoods" (cut) | 10:39 | `07_lake` | Full-frame (gold tier) | 4–6s |
| "homes on the lake… watch out for the flood zones" | ~10:48 / 11:35 | `13_lake_map` | Full-frame lake map (gold) | hold 6–8s |
| Walking the lake streets | 10:45–13:00 | `LT_lake` | Lower-third | as needed |
| "for a quick summary" (cleaned) | 13:06 | `09_recap` | Full-frame leaderboard (HERO) | hold ~13:06–14:40 |
| "reach out to me… private conversation… plan to relocate" | 14:55–end | `10_cta` | Full-frame end card | 5–8s |

### Stat-pop callouts (all pre-made — drop in, no editing)
*Transparent PNGs, top-right corner anchored. Use 1–2s as the number leaves your mouth.*

| Pop file | Shows | Use when you say |
|----------|-------|------------------|
| `POP_morgans_median` | $247K · Median | "median price… around $242K" (~0:38) |
| `POP_morgans_psf` | $179 · per sqft | "$179 per square foot" (~0:43) |
| `POP_morgans_range` | $160K–$825K · widest range | "you can get them very cheap… up to $800K" (~1:48–1:59) |
| `POP_morgans_sales` | 36 · sales/12mo | optional, over Morgan's b-roll |
| `POP_bell_price` | $232–300K · new from Stylecraft | "price range from 232 up to 300" (~2:43) |
| `POP_threecreeks_sales` | 119 · #1 in Belton (badge) | "most sales in Belton… last year" (~4:45) |
| `POP_threecreeks_range` | $215K–$499K · range | "215,000 all the way up to ~500,000" (~5:00) |
| `POP_threecreeks_median` | $316K · Median | optional |
| `POP_threecreeks_psf` | $166 · per sqft | optional |
| `POP_dawson_sales` | 29 · sales/12mo | "29 sales in the past year" (~7:28) |
| `POP_dawson_size` | 2,280 sf · median size | "2,280 square feet" (~8:05) |
| `POP_dawson_psf` | $183 · per sqft | "around 180 per square foot" (~8:08) |
| `POP_dawson_median` | $400K · Median | "median of around 400,000" (~7:35) |
| `POP_lake_median` | $765K · Median (gold) | "median price… seven hundred twenty" (~11:23) |
| `POP_lake_psf` | $248 · per sqft (gold) | "around $238 per square foot" (~11:23) |
| `POP_lake_dom` | 96 · days on market (gold) | "average days on market is around 92" (~12:38) |

---

## ASSET INDEX (36 files)
**Full-frame (4K, opaque) — 13:** `01_title` · `02_framework` · `03_morgans` · `04_bellmeadows` · `05_threecreeks` · `06_dawson` · `07_lake` · `08_tax` · `09_recap` · `10_cta` · `11_threecreeks_map` · `12_dawson_map` · `13_lake_map`
**Lower-thirds (transparent PNG) — 6:** `LT_name` · `LT_morgans` · `LT_bellmeadows` · `LT_threecreeks` · `LT_dawson` · `LT_lake`
**Stat-pop callouts (transparent PNG) — 16:** `POP_morgans_median/_psf/_range/_sales` · `POP_bell_price` · `POP_threecreeks_sales/_median/_psf/_range` · `POP_dawson_sales/_size/_psf/_median` · `POP_lake_median/_psf/_dom` *(plus legacy `POP_stat`)*

**Re-render / edit:** full-frames + lower-thirds = `python3 build.py`; stat-pops = `python3 build_pops.py`; maps = `python3 build_map.py` (Three Creeks) + `python3 build_map2.py` (Dawson + Lake); then the Chrome render loop (see chat). Card numbers live in the `NB` dict in `build.py`; pop numbers in `build_pops.py`. Brand: midnight `#0f172a`, emerald `#10b981`, gold tier `#e3c789`; fonts Cormorant Garamond / JetBrains Mono / Inter (local in `graphics/fonts/`).

## DATA PROVENANCE
All medians, $/sqft, counts, DOM, and ranges = `market-monitor/belton-only-data-0-365.csv`, rows with a populated ClosePrice, trailing 12 mo. **Exception:** Ridge at Bell Meadows = Stylecraft builder pricing (new community; not in MLS resale pull) — flagged on the card and recap (`*`).
