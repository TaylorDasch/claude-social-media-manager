# PCS to Fort Cavazos — Production Package

**Video #2 in the "New 20" priority list** · ⭐⭐⭐⭐⭐ impact (zero-competition lane per SERP audit)

## Files

| File | Purpose |
|---|---|
| `pcs-fort-cavazos.html` | Click-through 3D map tour. 24 steps. Starts over Fort Cavazos gate, shows commute path to Temple, walks through 4 military-friendly zones, includes BAH math card. |
| `voiceover-script.md` | Teleprompter-ready 12-15 min script synced to the HTML steps. |
| `README.md` | This file. |

## Before Filming — VERIFY THESE NUMBERS

The BAH and school-district numbers in the HTML and script are 2026 approximations. **Verify current values on the day you film:**

1. **Fort Cavazos BAH rates** — https://www.defensetravel.dod.mil/site/bahCalc.cfm (use zip 76544)
2. **Killeen median home price** — Redfin/Zillow Killeen market report
3. **Temple + Killeen ISD current ratings** — TEA or schooldigger
4. **Bell County non-homestead tax rate** — Bell CAD website

Update the HTML's `bah` overlay step (search for `bahValue` in the SEQUENCE) and the script's Step 6 if any number is materially off.

## How to Use During Filming

1. Open `pcs-fort-cavazos.html` in Chrome
2. Wait for "READY — Click NEXT to begin" in the HUD
3. Click `NEXT →` or press `Space` to advance each step
4. The HTML has **24 steps** — pace them against the script sections
5. Step 6 (BAH MATH) is the retention peak — do NOT rush past it

## Production Workflow

Same as Temple Map Tour — see `../temple-map-tour/README.md` for the Mac screen-record instructions and CapCut edit flow. Key differences:

- **Title:** "PCS to Fort Cavazos? Why Smart Military Families Skip Killeen and Live in Temple (2026)"
- **Thumbnail text options:**
  - "SKIP KILLEEN"
  - "YOUR BAH GOES FURTHER"
  - "20 MIN FROM THE GATE"
- **Tags:** pcs to fort cavazos, fort cavazos housing, moving to fort cavazos, military relocation temple tx, temple tx military, va loan temple, fort hood housing 2026
- **Chapters:**
  ```
  0:00 Hook
  0:30 The Framework
  1:00 The Commute (Gate → Temple)
  2:00 The BAH Math
  3:00 Killeen Reality
  4:00 Lake Pointe (Belton ISD)
  5:15 Sage Meadows (Entry Tier)
  6:15 Hillside Village (Tax Hack)
  7:30 Groves at Lakewood Ranch
  8:15 School District Edge
  9:30 The Killeen Default Mistake
  10:30 VA Loan Playbook
  11:30 CTA
  ```
- **Pinned comment:** "Current rank and BAH? Drop it below and I'll tell you exactly which of these 4 zones fits your number. Free PCS guide link in bio."
- **End screen:** Point to `ranked-worst-to-best` (Video #3) for compounding watch time.

## Honest Limits

- I have not verified every coordinate for 100% accuracy. The Fort Cavazos gate at `[-97.7590, 31.1350]` is the **main gate (Marvin Leath)** approximation. If you want the camera to center over a different gate (Clarke, Chaffee, Tank Destroyer), update `COORDS.cavazosGate` in the HTML.
- Killeen "old neighborhoods" coord is a stand-in — the camera just needs to pan over *some* of the older Killeen housing stock. If you want a specific neighborhood shown, update `COORDS.killeenOld`.
- BAH numbers WILL change. Do not ship this video with 2024 or 2025 data — verify current-year first.

## Rollback

```
rm -rf /Users/taylordasch_1/claude-social-media-manager/yt-videos/pcs-fort-cavazos/
```
