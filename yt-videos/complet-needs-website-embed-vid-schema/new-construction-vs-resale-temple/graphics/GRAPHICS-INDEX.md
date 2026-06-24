# Graphics Package - New Construction vs Resale in Temple TX

Built for `New vs Resale in Temple TX: The 77-Day Gap (2026)`.

- PNG exports: `png/`
- Source HTML: `html/`
- Build command: `cd graphics && python3 build.py && python3 render.py`
- Output size: 3840x2160 PNGs from 1920x1080 HTML at 2x scale
- Full-frame cards: opaque, use as cutaways or over A-roll.
- Lower-thirds: transparent PNGs, drop over talking head.

## Data Lock

Use these numbers only unless the video data is re-pulled:

| Metric | New | Resale | Gap |
|---|---:|---:|---:|
| Median price | $290,950 | $265,000 | +$25,950 |
| Price/sqft | $172 | $152 | +13.2% |
| Days on market | 133 | 56 | +77 days |
| Sample | n=122 | n=299 | - |

Main source label: `Temple MLS closed sales, Jun. 18, 2026 pull`

Incentive label: `June 19 builder-incentive feed: 56 detected Temple incentive cards. Terms can change. Verify with builder/lender.`

Tax-card wording intentionally says `district-charge example` and `verify exact parcel`; do not call it typical.

## Cue Sheet

| Script cue | File | Type | Edit note |
|---|---|---|---|
| Cold open / first data interruption | `png/01-title-77-day-gap.png` | Full-frame | Use after "which house it is" or as the first punch-in after the hook. |
| Section 1 - $290,950 vs $265,000 | `png/02-main-comparison.png` | Full-frame | Put on screen before 0:45. |
| Section 2 - price/sqft premium | `png/03-price-per-sqft.png` | Full-frame | Use while saying `$172` vs `$152` and `13.2% premium`. |
| Section 3 - MUD/PID tax math | `png/04-tax-line-buyers-miss.png` | Full-frame | Use during the `$6,636` vs `$9,836` example. |
| Section 4 - leverage payoff | `png/05-leverage-flip.png` | Full-frame | Hard cut / sound hit at the midpoint. This is the hero data card. |
| Section 4 - builder incentives | `png/06-incentive-feed.png` | Full-frame | Use while saying 56 detected Temple incentive cards. |
| Section 5 - model home registration | `png/07-model-home-registration.png` | Full-frame | Use over the builder sales rep / model home trap section. |
| Section 5 - honest scars | `png/08-honest-scars.png` | Full-frame | Use when listing the real tradeoffs on both sides. |
| Section 6 - decision framework | `png/09-decision-matrix.png` | Full-frame | Use for "choose new if / choose resale if." |
| CTA / end screen setup | `png/10-mudcheck-cta.png` | Full-frame | Use under the final MUDCHECK CTA or as the last full-screen card. |
| Anytime data is on screen | `png/LT-data-label.png` | Lower-third | Transparent source label overlay. |
| Tax section support | `png/LT-tax-caveat.png` | Lower-third | Use on A-roll when explaining MUD/PID. |
| Incentive section support | `png/LT-incentive-caveat.png` | Lower-third | Use if showing any builder incentive screen recording. |
| Model-home trap support | `png/LT-agent-registration.png` | Lower-third | Use while saying register your agent before touring. |
| CTA support | `png/LT-mudcheck.png` | Lower-third | Use during final direct-to-camera CTA. |

## Editing Notes

- Use `05-leverage-flip.png` as the big midpoint interruption.
- Keep `04-tax-line-buyers-miss.png` up long enough for viewers to see `$267/mo`.
- Pair `06-incentive-feed.png` with a clear spoken caveat. The graphic already says detected language and terms can change.
- For lower-thirds, place over desk/talking-head footage. They already sit bottom-left inside safe margins.
- If you change the script data, edit `build.py`, run `python3 build.py`, then render again.

