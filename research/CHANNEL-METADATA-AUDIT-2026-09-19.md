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

---

# ADDENDUM — Invest Central Texas (Channel B), audited 2026-09-19

Source: live metadata for the 41 most recent videos on UCKuVz8ytHECKEAyRacDpm1g.

## 7. YOU ALREADY DECIDED TO SHUT THIS CHANNEL DOWN

| Field | Value |
|---|---|
| Video ID | `1HNwJy8RxkQ` |
| Title | **"URGENT: I'm Shutting Down This Channel (Moving Here 👇)"** |
| Published | **2026-01-11** |
| Views | 121 |
| Privacy | **private** |

A shutdown announcement was filmed, published, watched 121 times, and then **set to
private** — and the channel kept publishing afterwards (four more long-form videos through
2026-08-07).

**This matters for the slate's "abandon Channel B" recommendation: it is not a new idea.**
You reached that conclusion in January, told your audience, and then reversed it. Before
acting on the recommendation a second time, the useful question is what changed your mind
in January — because that reason probably still exists.

## 8. THE CHANNEL'S BEST CONTENT IS HIDDEN

Nine videos are private. They hold **2,342 views between them** — against the channel's
1,312 public lifetime views.

| Video | Type | Views | Title |
|---|---|---|---|
| `Zg5JfvW1I7E` | Short | **844** | $125K Temple TX Property Tour |
| `Lgg-cp2hchk` | Short | **780** | Brandon Turner Investment Strategy |
| `dlO6C6ewpSI` | Short | **445** | Move. Buy. Repeat. |
| `1HNwJy8RxkQ` | Short | 121 | the shutdown announcement above |
| `d5iq1fIpmOM` | Short | 57 | Temple TX Mixed-Use Flip |
| `l7J-CfwI9QM` | long | 34 | $185K Temple TX w/ Extra Unit |
| `NK1Q1sn9lnw` | long | 31 | Pre-Foreclosure to Profit (Killeen) |
| `T4iN35Tod2E` | long | 30 | Best Starter Investment $95K |
| `AMlpFNCpCzg` | Short | 0 | LARGEST Home In Lake Pointe |

**The best public video on this channel has 88 views** (`m0CPhoHJy0E`). The top private
Short has **844 — 9.6x more.** The three best-performing pieces of content this channel
ever produced are all hidden.

This reframes the channel's story. It did not fail to find an audience; **its best
performers were taken down.** Whatever the reason (a sold property, a stale price, a
rights issue with the Brandon Turner content), it is worth knowing before writing the
channel off — and worth checking whether any of them could be re-published, or re-cut for
the main channel where the audience actually is.

**Again: I do not know why these were made private. This is a question, not a
recommendation.**

## 9. ALL 41 VIDEOS SHARE ONE COPY-PASTED TAG BLOCK

Nearly every video on this channel carries the identical ~28-tag block: *real estate,
real estate investor, investors, property, rental property, estate, investing in real
estate, temple Texas real estate, flipping homes, real estate investing, wholesaling,
investment property, flip, flipping houses, how to invest…*

There is **no per-video keyword targeting anywhere on the channel.** A video about
foreclosure auctions, one about property managers and one about house hacking all carry
the same generic block. Combined with the tag `InvestingInTempleTX` — which is the wrong
channel name — this is a channel with no discovery signal at the video level.

Worth weighing honestly against §2: tags are a weak ranking factor now, so this is
unlikely to be the *cause* of 32 views per video. But it is consistent with a channel
that was published to without a distribution plan.

## What this addendum changes

The slate recommended abandoning this channel on the numbers: 54 subs, 32 views/video,
+1 sub in 90 days, zero attributable closings. **Those numbers are still right.** But two
facts complicate the picture:

1. You already made and then unmade this decision once, in January.
2. The channel's three best-performing assets are private, so the public view counts
   understate what the content actually did.

That does not overturn the recommendation — the main channel still has 100x the
distribution and the same audience profile. It does mean the decision deserves your
actual reasoning rather than a fresh look at the same numbers.
