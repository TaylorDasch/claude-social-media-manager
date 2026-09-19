# YouTube Channel Metadata Audit — 2026-09-19

> Source: live YouTube metadata for the 100 most recent **long-form** videos on
> Living In Temple, TX (UCqrLPGPR9eV7QUfK02dwtpQ), pulled via the authenticated
> vidIQ connection 2026-09-19. Covers uploads from 2025-07-31 to 2026-09-16.
> Shorts were excluded deliberately — they are derivatives without a lifecycle.

Found while backfilling the content registry. These are live-on-YouTube issues, not
repo issues, and several are fixable in minutes.

---

## 1. A BROKEN VIDEO IS PUBLIC ON THE CHANNEL

| Field | Value |
|---|---|
| Video ID | `53_aqbqB0cI` |
| Title | **"unknown"** |
| Upload status | `uploaded` — **never finished processing** |
| Duration | `P0D` — zero |
| Privacy | **public** |
| Published | 2025-10-14 |
| Views | 0 |

A zero-length video titled "unknown" has been publicly listed on the channel for
**11 months.** It is reachable from the channel's video tab.

**Fix: delete it or set it private. Two minutes.** This is the single fastest cleanup
on the list.

---

## 2. BANNED WORDS ARE LIVE IN TITLES AND TAGS

`governance/QUALITY-GATES.md` Gate 1 bans "turnkey", "dream home", "charming",
"nestled", "white glove". They are published on YouTube right now.

### In a title
- `V_iAabnTZJU` — **"See Inside This Dream Home in Temple Texas!"** (2025-11-21, 110 views)

### In tags — `turnkey rental texas` on 15 long-form videos
`YLVcUgn_-FA` (The $50,000 Mistake — the channel's highest-AVD video) · `jIMtBf32NDo` ·
`3cBph19Qs7Y` · `wvpGgYOCVHM` · `6lyWBgezEXk` · `pph_QEB7E-E` · `ONENKUJtEfA` ·
`HEkDFljstqs` · `RKhlZmDcL74` · `0JabES-lN-8` · `cQzNXV9Y7NM` · `ZmB4WR5a5yk` ·
`0Wyw4bcAUGU` · `e8u9AlPxsbo` · `xVUN9zYCHpw`

### In tags — `dream home` / `Charming Curb Appeal`
`ujckUXi5oGQ` · `49ug2MHV9MI` · `OddA_A4vivw` · `KuUXHhrwVIo`

### In tags — `fort cavazos` (the base reverted to Fort Hood in 2025)
`acesZNhFiZM` · `3cBph19Qs7Y` · `jIMtBf32NDo` · `wvpGgYOCVHM` · `6lyWBgezEXk` ·
`pph_QEB7E-E` · `ONENKUJtEfA` · `HEkDFljstqs` · `RKhlZmDcL74` · `YLVcUgn_-FA` ·
`0JabES-lN-8` · `cQzNXV9Y7NM` · `ZmB4WR5a5yk` · `0Wyw4bcAUGU` · `e8u9AlPxsbo` ·
`xVUN9zYCHpw` · `muMJpnjq35c` · `Em2b_LIdKSQ`

**Worth calibrating:** tags carry far less ranking weight than they used to, so this is a
brand-consistency issue more than a discovery one. The **title** on `V_iAabnTZJU` is the
one that actually matters. The `fort cavazos` tags are arguably defensible as a legacy
search term people still type — but that is a decision to make deliberately, not by
accident, and the repo currently says never to use it.

---

## 3. SIXTEEN LONG-FORM VIDEOS HAVE NO TAGS AT ALL

`gea30sKmbJE` · `-uDu3WKyJxk` · `QZCXy4T3bmg` · `WLILSKqt2HU` · `g9_rpIERRcM` ·
`aX6xllHrcjk` · `PwwfJn5rxxk` · `mg4U_wrsucg` · `JDvbzuhT3tY` · `0Tdk4vNTOjU` ·
`JcETQPlzXB4` · `dNclgtSwoAY` · `xfLTEYBBze0` · `2HmCFR7y0Ew` · `zjGwgfMj85Y` ·
`53_aqbqB0cI`

And `4T5Vv_qBntk` has exactly one tag: **`$184`** — clearly a truncated mistake.

Several of these are among the better performers — `dNclgtSwoAY` has 321 views,
`WLILSKqt2HU` 219, `l3TgaZaFyik` 240 — so they are earning views with no metadata help
at all.

---

## 4. TWO INVESTOR VIDEOS ARE SET TO PRIVATE

| Video | Title | Views before going private |
|---|---|---|
| `Mm3bi8qgd3o` | $150K Flip Opportunity in Temple TX: Investment Numbers Breakdown | 86 |
| `Y-uDhkhPGsE` | Bought for $70k, Worth $150k: Temple TX Mid-Term Rental Rehab Tour | 77 |

Both accumulated views, so both were public at some point and were later hidden.

**This is worth a deliberate decision, because investor content is the only category with
tracked revenue attached to it** — both YouTube-attributed deals ($5,400 closed, $2,100
under contract) came from investor videos. If these were pulled for a fixable reason
(a stale price, a since-sold property, a client's privacy), consider whether an edited
description or a pinned correction would let them go back up.

**I do not know why they were made private, so this is a question, not a recommendation.**

---

## 5. A DUPLICATE UPLOAD

`mZHSp85IoYE` (public, 2026-09-16, 138 views) and `iW4GwKzzVEw` (private, 2026-09-13,
0 views) share the identical title *"Temple TX New Construction: What to Check Before You
Buy"* and identical duration (8:03).

This looks like a deliberate re-upload with the old copy hidden, which is fine. Noting it
so it is not mistaken for two assets. The private copy can be deleted.

---

## 6. WHAT THE CATALOGS ARE MISSING

`data/living-in-temple-catalog.txt` and the content registry are both significantly behind
the live channel. Long-form videos published since the catalogs were written and tracked
nowhere include:

Living in Harker Heights TX (2026) · Retiring in Temple TX: The Honest Georgetown
Alternative · Living in Troy TX · BSW Residency in Temple TX: Rent or Buy for Three Years? ·
How Much House Can You Afford in Temple, TX? (The 28/36 Rule) · Temple, Texas Market
Forecast · Inside Fryers Bend · The Truth About "Lake Homes" in Morgan's Point Resort TX ·
New Construction vs Resale in Temple TX: The 77-Day Difference · Temple TX New
Construction: What to Check Before You Buy · Where BSW Staff Live in Temple TX ·
Hillside Village Temple TX · The Cliffs at Canyon Creek · Omega Builders Temple TX

The registry holds **60 rows against 217 live videos on this channel alone** (~100 of them
long-form). That is why it cannot currently answer "have I already covered this?"

---

## Recommended order

1. **Delete or unlist `53_aqbqB0cI`** — the broken public video. 2 minutes.
2. **Retitle `V_iAabnTZJU`** to remove "Dream Home". 2 minutes.
3. **Decide on the two private investor videos.** Highest potential value on this list.
4. **Delete the duplicate private `iW4GwKzzVEw`.** 1 minute.
5. **Add tags to the 16 untagged videos**, prioritising the ones already earning views
   (`dNclgtSwoAY` 321, `l3TgaZaFyik` 240, `WLILSKqt2HU` 219).
6. **Strip the banned tags** — batch job, low urgency, do it when touching each video anyway.

## Scope note

This covers the 100 most recent **long-form** videos on the main channel. Not audited:
the remaining long-form back-catalogue beyond 2025-07-31, all ~117 Shorts, and all 41
videos on Invest Central Texas. Say the word and I'll extend it.
