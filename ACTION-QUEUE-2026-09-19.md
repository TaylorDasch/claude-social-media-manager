# Action Queue — 2026-09-19

Concrete items surfaced by the top-5 analysis and the tax consolidation, verified
individually. Ordered by effort-to-value.

---

## 1. Ship the physician-loan video — genuinely ~10 minutes

`yt-videos/physician-loan-temple/` contains an `.srt`, which means it was **filmed on
2026-03-29 and never published.** 6 minutes 24 seconds, fully shot.

**The only problem is one line.** At 0:03 Taylor says *"we just had Match Day."* Match Day
was March 20, 2026 — six months ago. Everything after that line is evergreen
physician-loan-vs-builder-incentives content.

**Fix:** cut that line in the edit, or re-record ~5 seconds of open during the weekend desk
shoot. Then publish.

**Do not** hold it for March 2027. The audience is not only matching residents — BSW hires
attendings, nurses and staff year-round, and the physician-loan question is asked year-round.

Pairs with `/buy-before-first-day-of-residency-bsw/`, which exists and has no video embedded.

---

## 2. DOTW-002 — DO NOT publish as-is

**This was previously listed as a ten-minute win. That was wrong; I checked the property.**

`output/2026-W16/deal-of-the-week/1807-s-11th-st/` is a Deal of the Week for a **specific
active listing**: 1807 S 11th St, Temple 76504, **MLS# 596895, listed $145,000**, written
2026-04-17. It has sat READY_TO_PUBLISH for 155 days.

A five-month-old listing is almost certainly sold or withdrawn. Publishing it would advertise
a dead deal and burn credibility with exactly the investor audience that produces the
channel's only tracked revenue.

**What is still good:** the *analysis*. The LTR-vs-MTR split on a sub-$150K Temple property
near BSW is a strong evergreen investor video:

> As an LTR: $1,200/mo, DSCR 0.76, negative cash flow.
> As an MTR (traveling nurses): $1,800/mo, 17.2% cash-on-cash.
> Same house. Two completely different investments.

**Recommended:** rebuild it as an evergreen strategy video — "Why the Same Temple House Loses
Money as a Rental and Prints as an MTR" — using a *current* listing, or anonymised as a worked
example with no MLS number. Kill the property-specific version.

**Also note:** Bell CAD assesses that parcel at **$103,598** (land $25,800 + improvement
$77,798) against a $145,000 list. Useful as a worked example of assessed-vs-list divergence,
which ties to the property-tax video.

**Registry action:** DOTW-002 and its three child assets should move off READY_TO_PUBLISH.
They are not publishable; they are salvageable source material.

---

## 3. Retitle the data-center video — 2 minutes, marginal but free

Current: *"Temple TX Is Getting $5 Billion in Data Centers — What the Housing Data Actually Shows"*
(video `3coe1mbneH0`, published 2026-09-01, 202 views)

| Title | VidIQ score |
|---|---|
| **$5 Billion Is Landing in This Texas Town — What It Does to Home Prices** | **97** |
| The Texas Housing Market Nobody Is Watching Right Now | 93 |
| *current title* | *91* |
| Data Centers Are Coming to Your Texas Town — What Happens to Home Values | 88 |
| $5 Billion Is Landing in This Texas Town (2026 Housing Data) | 86 |

**Set an honest expectation.** The current title already scores 91, so this is a **+6 CTR
change, not a rescue.** That video's problem is distribution, not clickability: it drew only
**15 suggested views and 33 search views**, with ~140 of its 217 views coming from subscriber
notifications. Every data-center keyword measures **under 750/mo**, so no title creates search
demand that doesn't exist.

Do it because it's free. Do not expect it to resurrect the video. Its real future is as the
local deep-dive that the statewide "County by County" video (slate #3) links to.

---

## 4. Channel name corrected across the repo — DONE

`data/content-registry.csv` and seven other files called the second channel
**"Investing in Temple."** The live channel is **"Invest Central Texas."**

Fixed in: `skills/yt-video/SKILL.md`, `skills/weekly-scorecard/SKILL.md`,
`skills/news-hijack/SKILL.md`, `skills/youtube-description/SKILL.md`, `BRAND_VOICE.md`,
`social-media-config.json`, `codex-jobs/cx-01-youtube-metadata.md`.

This mattered because several of those skills **branch on the channel name** when generating
metadata. Historical research docs were left as the record.

**Still Taylor's call:** the slate recommends abandoning that channel entirely (54 subs,
32 views/video, +1 sub in 90 days, zero attributable closings) and porting the topics to
the main channel, where the audience is already 95.7% male and 71% aged 25–54. The naming
fix is correct either way; the strategic change is not made.

---

## 5. Registry debt — flagged, not fixed

`data/content-registry.csv` covers **60 rows against ~258 live videos — about 23%.** That is
why it cannot currently answer "have I already covered this?", which is the question the
whole dedupe system depends on.

Also stale: LIT-007 and LIT-016 have been REFRESH_DUE for ~140 days, and six YT-PREP rows
have been QUEUED for ~167 days.

Not fixed here because backfilling 198 rows is its own task and needs decisions about what
counts as an asset worth tracking. Worth doing before the registry is trusted again.

---

## 6. Prepped folders that should not be filmed

From the slate's verification, three folders in `yt-videos/` would actively hurt:

- **`ranked-worst-to-best/`** and **`temple-map-tour/`** — ~90% query overlap with the
  14,727-view flagship. Filming either splits the channel's best asset. The map tour also
  contains wrong data: population 85,000 (vault says 96,267), Fort Hood at 20 minutes
  (it is 38 minutes / 36.4 miles), and "Fort Cavazos" throughout.
- **`pcs-fort-cavazos/`** — cannibalized by an already-published video that got 115 views,
  and "Fort Cavazos" appears in the README, the script, the HTML and the folder name.
- **`how-i-analyze-rental-property/script-and-prep.md:243`** still cites the **debunked
  5,101-unit housing deficit**. Per the vault this must not ship in any form.

---

## 7. Data hygiene sweep — DONE

Chasing the debunked housing-deficit stat surfaced that it and the wrong tax range were
**live in the files that generate content**, not just in archived research.

**`social-media-config.json`** — which `CLAUDE.md` declares "the single source of truth for
brand, personas, platforms" — carried both:

| Field | Was | Now |
|---|---|---|
| `countyTaxRateRange` | `"2.4%-2.7%"` | `templeCombinedTaxRate: 2.3877%` + all four city rates, with the "stacks differ by address" warning |
| `powerZip76502` | `"5,101 unit housing deficit, 24.1% population growth"` | 3.38% projected annual growth (World Population Review 2026) + Bell County 2030 projection (Texas Demographic Center) |
| `platforms[].powerZip` | same debunked stat | corrected |

**Also fixed:**
- `BRAND_VOICE.md` — an example answer quoting the 5,101 deficit, and the stat table's
  `~2.366%` entry
- `reference/TIKTOK-TO-NEWSLETTER-FUNNEL.md` — five instances across example captions and hooks
- `yt-videos/how-i-analyze-rental-property/script-and-prep.md` — the debunked stat, plus a
  tax claim of "2.4 to 2.7%" that flowed into the worked example. Recomputed at the verified
  2.3877%: monthly expense stack $2,061 → **$2,034**, cash flow −$411 → **−$384**,
  cash-on-cash −8.8% → **−8.2%**
- `reference/BP-ENGAGEMENT-PLAYBOOK.md` — four response templates quoting 2.25% to investors

JSON validity re-checked after editing the config.

**Left as the historical record:** `output/` artifacts, `research/` docs, and
`taylor-dasch-content-strategy-audit.md`. These are dated snapshots, not generators.

**Still carrying "Fort Cavazos":** `yt-videos/pcs-fort-cavazos/`, `temple-map-tour/` and
`ranked-worst-to-best/`. All three are on the do-not-film list in §6, so they were left
alone rather than cleaned. If any is ever revived, the name has to be fixed first.
