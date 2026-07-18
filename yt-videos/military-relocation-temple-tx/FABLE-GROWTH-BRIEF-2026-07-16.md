# Fort Hood PCS Video — Fable Growth Brief
**Video:** https://www.youtube.com/watch?v=39Y6UpSFqu0 · Published 2026-06-30 · 18:08
**Brief date:** 2026-07-16 (evening CT). All live-state claims independently verified today unless marked otherwise.
**Rule honored:** no website edits published, no YouTube metadata altered, no messages sent, nothing distributed. Everything below is implementation-ready and gated on Taylor's review.

---

## 1. Executive verdict

The video's content core is strong — mid-video relative retention peaks at 0.83 vs similar videos at the 6:57 scorecard — but the asset is being strangled at three points that packaging tests cannot fix:

1. **The new thumbnail (live ~July 16) is factually wrong.** It labels the six pins KILLEEN / HARKER HEIGHTS / BELTON / TEMPLE / **GEORGETOWN / WACO**. Georgetown and Waco are not in the video; Copperas Cove and Nolanville are missing. Every click it earns from a Georgetown/Waco searcher is a guaranteed bounce, and any CTR data collected on it is unusable. This meets the mission's "factual/severe trust" exception to the 7-day hold — fix it once, immediately, then start the clean 7-day window.
2. **The intro is the retention leak, not the topic.** Audience slides from 85% at 0:22 to 45% by 1:49 — exactly across the "Why I'm NOT the typical military agent" credibility block (0:24–1:22). The towns, scorecard, disabled-vet tax lever, and sell-vs-rent close all hold or spike. One Studio trim decision (pre-committed below) is worth more than any title change.
3. **The website side of the funnel is structurally broken.** The description/pinned links send viewers to a hub whose H1 reads "Fort Hood / Fort Hood", a second competing hub at `/fort-hood/` opens with literal gibberish ("officially redesignated from Fort Hood in July 2025"), the buy-vs-rent calculator page ships 31KB of orphaned HTML after `</html>` including a second footer, `/terms-of-use/` in the sitewide footer is a 404, zero lead/calculator events exist in GA4, and the whole cluster carries Fair Housing exposure ("lowest crime", "best schools", "fastest resale") plus an unsupported 5.0/50 aggregateRating on every page.

**The highest-leverage path:** (a) correct the thumbnail + replace description/pinned/tags/cards/end-screen in one approved pass, then hold 7 days; (b) crown `/where-to-live-fort-hood/` as the single primary companion (it already has the early embed, verbatim FAQ schema, and exact content fit) and strip its compliance risks; (c) consolidate the two competing hubs into one; (d) fix the BAH calculator's snippet — it has 4,197 impressions at 0.33% CTR sitting at position ~8.6 on "fort hood bah" (1,300/mo), the single cheapest traffic win in the entire cluster; (e) install the missing GA4 event layer so the 30-day verdict is measured in qualified PCS conversations, not views.

---

## 2. Confirmed current state (all verified 2026-07-16)

**YouTube package**
- Title: `PCS to Fort Hood (2026): 6 Towns Compared by BAH & Commute` (set 2026-07-14 in Studio)
- Thumbnail: "SAME BAH / 6 OUTCOMES" concept, E-5 BAH card $1,695, six labeled pins — **two towns wrong** (Georgetown, Waco), Copperas Cove and Nolanville missing (pulled live maxresdefault today)
- Description: still the June 30 block. Contains: "THE RULE: BAH × 0.95 = your max monthly PITI" (rigid ceiling framing), chapter "9:42 Copperas Cove — best schools + Coryell County", chapter "7:17 Killeen — cheapest sticker, fastest exit", undated six-town price snapshot, primary link to `/military-relocation-temple-tx/` with `utm_campaign=military-relocation-temple-tx` while deeper links each carry their own campaign names (no unified campaign)
- Tags: 22 tags, already the post-retitle set — acceptable
- Comments: **two** owner comments (June 30 + July 2). The June 30 one asks viewers for **VA disability %** — prohibited ask; the July 2 one is the pinned CTA. One real comment asks "What area has the lowest crime rate?… West Temple" with 1 reply whose text is not API-retrievable — must be checked in Studio against the Fair Housing playbook (§4)
- Playlist "Military PCS To Fort Hood Guides" exists on the channel
- Cards/end-screen state: **not API-visible** — verify in Studio before applying §4
- PDF guide link: 200 OK (258KB, last-modified 2026-06-17)

**Analytics (YouTube Analytics API, 2026-06-30 → 2026-07-14 — i.e., the OLD packaging era; ~2-day lag means post-reset data does not exist yet)**
- 74 views (79 public counter), 314 min watch time, AVD 4:15, **avg % viewed 23.45%** vs channel long-form norm of 38–50% (jIMtBf32NDo 41.9%, cAxYKEcYGiE 44.8%, ZdKKZ8RRy4M 50.3%) — underperformance is real, not channel-wide
- First-30s retention ≈ **70%** (at 0:33 it is 69.9%) — the opening technically "lands" at the gate boundary; the collapse happens at 0:24–1:49 (85% → 45%)
- Biggest single drop: 0:22→0:33 (−15.1 pts). Spikes: 3:48 (Mistake #2), plateau + relative-retention peak 0.79–0.83 across 6:10–7:04 (scorecard), bumps at 14:52–15:25 (disabled-vet exemption, rel. 0.33→0.54) and 16:52–17:15 (sell-vs-rent close)
- Traffic sources: Suggested 26 views / 5:33 AVD (best), Subscribers 23 / 4:00, **YouTube Search 15 / 1:22 AVD** (old-title search clickers bounced), External 2, Notification 1
- Historical Studio export (07-02): 377 impressions, 3.71% CTR, AVD 5:55 — treated as context only
- **Impressions/CTR and search terms are NOT exposed by the local API tooling.** They must be pulled manually in Studio (Reach tab) — exact pull list in §10

**Funnel (GA4 property 454804009, 2026-06-30 → 2026-07-16)**
- Sessions attributed to this video's UTMs: **2** (1 description, 1 pinned), 0 engaged
- Cluster pageviews (all sources, 17 days): BAH calc 19 · hub 9 · where-to-live 2 · buy-vs-rent 1 · off-post 0 · (fort-hood-relocation n/a, redirects)
- **Zero** generate_lead / calculator / phone / Calendly events on any cluster path — only default page_view/scroll events exist. The measurement architecture in §8 does not exist yet

**Search (GSC service account, 90d 2026-04-15 → 2026-07-14; 28d spot-checks)**
- `/fort-hood-bah-calculator/` — 4,197 impressions / 14 clicks (0.33% CTR), avg pos 8.6; owns every "fort hood bah" variant
- `/military-relocation-temple-tx/` — 800 impr / 1 click (0.13% CTR), pos ~9.3; top queries "fort hood pcs housing guide temple tx" (58i), Temple↔Fort Hood commute queries
- `/fort-hood-off-post-housing/` — 274 impr / 2 clicks
- `/where-to-live-fort-hood/` — 35 impr / 0 clicks, pos 8.3 (young; lastmod 07-13)
- `/military-buy-vs-rent-pcs-calculator/` — 17 impr / 0 clicks, pos 19.1
- `/fort-cavazos-housing/` → 301 → `/fort-hood/` — 24 residual impressions; `/fort-hood/` **cannibalizes** the hub on "fort hood pcs housing guide temple tx" (10i pos 5.1 vs hub 58i pos 8.1)
- Site ranks for **nothing** on "pcs to fort hood", "moving to fort hood", "where to live near fort hood" (zero impressions)
- Google Ads demand (DataForSEO, June 2026): fort hood housing **1,900/mo** · fort hood bah **1,300/mo** · nolanville homes for sale 590 · killeen tx real estate 480 · on post housing 260 (rising) · fort cavazos housing 210 (collapsing, was 720) · harker heights tx homes 210 · off post housing 40 · best places to live near fort hood 20 · pcs to fort hood / where to live near fort hood / moving to fort hood ≈ 10 each. **The demand engine is "fort hood housing" + "fort hood bah" — everything the video title targets is browse/suggested demand, not Google search demand.**

**Live page state (each fetched and parsed today)**
| URL | Status | Reality |
|---|---|---|
| /where-to-live-fort-hood/ | 200, self-canonical | The real six-town companion. 3,719 words, video embedded immediately after hero, FAQ schema verbatim-matches 10 visible questions, form wired to Railway relay. Stale VideoObject/iframe titles, conflicting duplicate breadcrumbs, aggregateRating 5.0/50, "Best schools" labels ×3, "fastest resale/exit" ×4, "best/strongest rental pool" ×4, "$400K will not cash-flow" as fact, zero outbound citation links |
| /military-relocation-temple-tx/ | 200, self-canonical | The real hub (4,151 words, video embedded). **H1 = "Fort Hood / Fort Hood — Real estate, decided by data."** (unfilled template token, also baked into Article schema headline). Stale "UPDATED MAY 19 2026" ticker, best-schools FAQ in schema, "Killeen-volatility… Buy selectively or skip" steering, 5–6.5% appreciation claims, stale VideoObject name, dup breadcrumbs, aggregateRating |
| /fort-hood-off-post-housing/ | 200, self-canonical | 4,538 words, no video, no VideoObject, zero outbound links. **Worst Fair Housing page on the site**: "Killeen (5–10 min commute, lowest prices, highest crime)", "Is Killeen safe… violent crime 32% higher than Temple's", "crime rate is manageable with careful neighborhood selection", "West & NW Temple: Lowest crime", Belton "Best Schools" card, "best resale". Data "verified April 2026" (stale) |
| /fort-hood-relocation/ | 301 → hub | Correct; not in sitemap (correct) |
| /fort-hood-bah-calculator/ | 200, self-canonical | The SEO asset. Dated BAH figures with DoD source (good), Dataset schema (good). No video. Dup breadcrumbs, aggregateRating, **uncited Niche-style school letter grades (C+/B+/B−)** on city cards, undated 5.75% rate assumption. Title/meta not winning the click at pos 8.6 |
| /military-buy-vs-rent-pcs-calculator/ | 200, self-canonical | **Broken document**: `</html>` at 76% of the file, then ~31KB orphaned fragment — bare `<tr>` rows, hub-template "mr-*" sections, a companion-video *placeholder*, a 12-question FAQ with no schema, a second full footer. VideoObject claims a video the page never embeds. Two overlapping FAQ sections with slightly different answers. Best-schools + "Is Killeen or Temple better for a family" (family-status steering) in FAQ |
| /fort-cavazos-housing/ → **/fort-hood/** | 301 → 200 | A second, competing hub. Hero: "Relocating to Fort Hood (officially redesignated from Fort Hood in July 2025)" — botched Cavazos→Hood find/replace, repeated in FAQ Q1 *and* FAQPage schema. Best-schools rankings, "avoid oversaturated Killeen subdivisions", 5–6.5% appreciation as fact, unsourced "79% of protests" stat, tenant-pool demographics table, three conflicting date stamps, no video |
| /terms-of-use/ | **404** | Site-wide footer link target does not exist; /privacy-policy/ is 200 |

**Official data verified:** 2026 BAH, Fort Hood MHA TX286, E-5 w/dep = **$1,695** (effective 2026-01-01; +7.2% YoY; without-dep $1,530). Sources: garrisonledger.com/bah/fort-hood, milpaytools.com/bah/fort-hood; canonical lookup = DTMO (travel.dod.mil). The description's full table (E-4 $1,662 … O-4 $2,577) matches these sources.

**Fresh MLS (CTXMLS pull `july-13-active-sold-pending-0-30.csv`, statuses blended: active+pending+sold last 30 days, as of 2026-07-13):**
| Town | Median price | Median DOM | Median sqft | n |
|---|---|---|---|---|
| Killeen | $245,000 | 56 | 1,733 | 981 |
| Harker Heights | $315,000 | 59 | 2,149 | 186 |
| Copperas Cove | $249,999 | 55 | 1,658 | 367 |
| Nolanville | $370,900 | 55 | 2,272 | 111 |
| Belton | $335,000 | 62 | 1,976 | 387 |
| Temple | $279,000 | 62 | 1,796 | 945 |

---

## 3. Critical findings (severity-ranked)

| # | Severity | Finding | Evidence | Impact | Exact fix |
|---|---|---|---|---|---|
| 1 | CRITICAL / trust | Live thumbnail names Georgetown + Waco; video covers neither; Cove + Nolanville missing | maxresdefault pulled 07-16 | Wrong-intent clicks, guaranteed bounces, poisoned CTR test, credibility hit if a viewer calls it out | Regenerate via the existing Pikzels Prompt 1 with correct town labels — or, per the original prompt's own instruction, omit labels entirely. One change, today; 7-day clock starts after |
| 2 | CRITICAL / compliance | Owner comment collects **VA disability %** | June 30 comment, live | Collecting disability status in public comments = discrimination-adjacent optics + against mission rules | Delete that comment. One pinned comment only (§4) |
| 3 | CRITICAL / Fair Housing | Off-post page ranks cities by crime ("highest crime", "lowest crime", "Is Killeen safe", "32% higher"), neighborhoods by crime, towns by "best schools" | Live page text + FAQ | Steering exposure on a page with 274 GSC impressions; also poisons AI-answer citations | Strip/replace per §5 companion rules: neutral data + official-source pointers (Temple PD dashboard, TX DPS, TEA) |
| 4 | CRITICAL / integrity | `/fort-hood/` hero + FAQ + FAQPage schema contain "redesignated from Fort Hood back to Fort Hood" gibberish | Live page | First paragraph a PCS family reads is broken English; schema ships it to Google | Consolidate: 301 `/fort-hood/` → hub after porting its unique gate-matrix/REAL ID content (§6). Kills the bug, the duplicate hub, and the cannibalization in one move |
| 5 | HIGH / technical | Buy-vs-rent calculator serves ~31KB of orphaned HTML after `</html>` incl. second footer, placeholder video section, un-marked 12-question FAQ, VideoObject with no embed | Live fetch | Parser-dependent rendering, duplicate content, schema violation (video not on page) | Remove the fragment; keep ONE FAQ section with matching schema; delete VideoObject (video is not embedded there) |
| 6 | HIGH / schema | Unsupported `aggregateRating 5.0 / reviewCount 50` on RealEstateAgent on **every** cluster page; zero visible reviews | All 6 live pages | Self-serving review markup on LocalBusiness subtype = ineligible + manual-action risk | Remove the AggregateRating node from the sitewide identity schema template (one template fix) |
| 7 | HIGH / funnel | Hub H1 renders "Fort Hood / Fort Hood — Real estate, decided by data." and Article schema headline repeats it | Live fetch (verified twice) | The primary destination of the video's current description looks broken to every arriving viewer | H1 → "The Fort Hood Relocation & Housing Guide"; fix Article headline in the same pass |
| 8 | HIGH / revenue | `/fort-hood-bah-calculator/`: 4,197 impressions, 14 clicks, pos 8.6 | GSC 90d | ~35× more search demand than the rest of the cluster combined, and the snippet loses the click | Retitle + meta per §6 (promise the full rate table, then the calculator) |
| 9 | HIGH / measurement | Zero lead/calculator/contact events in GA4 on cluster pages; video drove 2 sessions | GA4 07-16 | 30-day success cannot be measured; "qualified PCS conversations" is currently unknowable | Install §8 event layer (one JS include + relay-form event) |
| 10 | MEDIUM / schema | VideoObject name on companion + hub = stale pre-retitle title; iframe title attributes stale | Live fetch | Video rich-result signal mismatched to live video; weakens the "one synchronized VideoObject" rule | Sync name/description to live title on the companion; delete VideoObject from hub (keep iframe) |
| 11 | MEDIUM / schema | Conflicting duplicate BreadcrumbLists (AIOSEO 2-item vs hand-built 3-item) + duplicate/inconsistent WebPage nodes on companion, calculators, hub | Live fetch | Google picks unpredictably; entity graph split | Keep ONE breadcrumb per page (recommend: drop the hand-built block, configure AIOSEO parent), point Article.mainEntityOfPage at the existing `#webpage` @id |
| 12 | MEDIUM / trust | `/terms-of-use/` footer link = 404 sitewide | curl 07-16 | E-E-A-T/trust gap on every page | Publish a terms page or repoint the footer link |
| 13 | MEDIUM / packaging | Description: BAH×0.95 framed as "THE RULE… your max", "best schools" + "fastest exit" chapter labels, undated town snapshot, split UTM campaigns | Live description | Compliance + attribution noise | Replace wholesale with §4 block |
| 14 | LOW / freshness | Hub ticker "UPDATED MAY 19 2026", off-post "verified April 2026", buy-vs-rent "May 19 2026" rail — all ~2–3 months stale while schema says dateModified 07-13 | Live fetches | Contradictory freshness signals | Refresh markers when §5/§6 edits land, with July 13 MLS table |

Also flagged: the reply to the live crime-rate comment could not be read via API — verify it in Studio against §4's model reply before doing anything else in the comment section.

---

## 4. YouTube package (implementation-ready)

### Title
**Verdict on current title (`PCS to Fort Hood (2026): 6 Towns Compared by BAH & Commute`, 58 chars): KEEP through the 7-day window.** Honest, mobile-safe (payoff lands by char ~40), matches the SAME-BAH thumbnail concept and the cold open. Known weakness: neutral "compared" framing historically underperforms in this niche for Browse (vidiq pool: neutral 66–76 vs $1,695/"mistake" framings 82–86), and Browse/Suggested — not search — is this video's quality traffic (Suggested AVD 5:33 vs Search 1:22). Google-side search demand for "pcs to fort hood" is ~10/mo; the title's job is browse clarity, which it does adequately but not maximally.

**Challengers (evaluate now, implement only per switch rules):**
1. `PCS to Fort Hood? The $1,695 Mistake Most Soldiers Make in 2026` — 63ch, vidiq 86. Best Browse/mixed. Honestly paid off (the video is literally structured around 4 mistakes).
2. `Fort Hood Housing 2026: What $1,695 BAH Buys in All 6 Towns` — 58ch, vidiq 82. Best Search (leads the 1,900/mo head term). Zero clickbait risk.
3. `The $1,695 BAH Mistake Most Soldiers Make Near Fort Hood (6 Towns)` — 65ch, vidiq 85. Browse variant surfacing the six-town moat.

Overpromise check: none of the three promises anything the video doesn't deliver ($1,695 is the verified E-5 w/dep BAH; the four mistakes are at 2:23/3:46/5:43/14:50; all six towns are covered).

**Switch rules (exact):**
- Day 0 = corrected thumbnail live. No packaging changes for 7 full days after.
- Day 9 (7 days + 2-day lag): pull Studio Reach data for the window.
  - ≥1,000 impressions AND CTR <4% → change **title only**: #1 if Browse+Suggested ≥60% of impressions, #2 if Search ≥40%.
  - CTR 4–6% → hold; re-check day 14 with watch-time share. CTR up + watch-time share down = wrong-audience thumbnail → revert thumbnail before touching title.
  - CTR >6% → lock the package; scale distribution only.
  - <1,000 impressions by day 14 → the constraint is impressions, not packaging. Do NOT churn the title; feed Suggested (Shorts, cards from sibling videos, playlist) and revisit at day 30.
- Never change title and thumbnail together again (today's factual thumbnail correction is the one exception).

**Rollback record (maintain in this file):**
| Date | Change | Data at change |
|---|---|---|
| 2026-06-30 | Published: title "PCS to Fort Hood: Don't Move Here Until You Watch This" + winner/loser thumbnail | — |
| 2026-07-14 | Title → "PCS to Fort Hood (2026): 6 Towns Compared by BAH & Commute" | 377 imp, 3.71% CTR, AVD 5:55 (07-02 export); 74 views |
| ~2026-07-16 | Thumbnail → "SAME BAH / 6 OUTCOMES" (DEFECTIVE: Georgetown/Waco labels) | 79 views |
| **2026-07-16 (late)** | Thumbnail → corrected six towns LIVE (verified on maxresdefault); old owner comments deleted; new CTA comment posted | **DAY 0 of the 7-day window. Day-9 pull: 2026-07-25. Day-14 trim gate: 2026-07-30** |

### Replacement description (exact paste block)

```
Where should you live when you PCS to Fort Hood? This video compares all six corridor towns — Killeen, Harker Heights, Copperas Cove, Nolanville, Belton, and Temple — by 2026 BAH, gate commute, monthly cost, tour length, and your exit plan when orders change.
Start here → the full 6-town breakdown with current numbers: https://templetxhomes.net/where-to-live-fort-hood/?utm_source=youtube&utm_medium=description&utm_campaign=fort-hood-pillar&utm_content=39Y6UpSFqu0

I'm Taylor Dasch, a real estate agent with EG Realty in Temple, TX. I've never served in the military — my edge is that I read the MLS for all six of these towns every week and I've closed deals in every one of them, so I have no reason to steer you toward any single town. This is a neutral comparison built on data, not a pitch.

FREE Fort Hood PCS Housing Guide (PDF):
https://templetxhomes.net/wp-content/uploads/2026/06/04__fort-hood-pcs-housing-guide.pdf?utm_source=youtube&utm_medium=description&utm_campaign=fort-hood-pillar&utm_content=39Y6UpSFqu0

RUN YOUR NUMBERS
2026 Fort Hood BAH calculator: https://templetxhomes.net/fort-hood-bah-calculator/?utm_source=youtube&utm_medium=description&utm_campaign=fort-hood-pillar&utm_content=39Y6UpSFqu0
Buy vs rent, by tour length: https://templetxhomes.net/military-buy-vs-rent-pcs-calculator/?utm_source=youtube&utm_medium=description&utm_campaign=fort-hood-pillar&utm_content=39Y6UpSFqu0
Full Fort Hood relocation hub: https://templetxhomes.net/military-relocation-temple-tx/?utm_source=youtube&utm_medium=description&utm_campaign=fort-hood-pillar&utm_content=39Y6UpSFqu0

CHAPTERS
0:00 One BAH, six different outcomes
0:24 Who I am and why I use the data
1:22 The 4 factors that decide your town
2:23 Buy vs rent — run it as a formula
3:46 Plan around your BAH, not your pre-approval
5:43 The gate-commute mistake
6:57 The 6-town scorecard (screenshot it)
7:17 Killeen
8:47 Harker Heights
9:42 Copperas Cove
10:55 Nolanville
12:02 Belton
13:01 Temple
14:13 On-post vs off-post
14:50 The Texas disabled-veteran property-tax exemption
16:40 Decide your exit before you buy
17:35 Build your shortlist

DATA + DISCLAIMER
2026 BAH, Fort Hood MHA (TX286), with dependents: E-4 $1,662 · E-5 $1,695 · E-6 $1,920 · E-7 $2,070 · O-1 $1,731 · O-2 $1,917 · O-3 $2,340 · O-4 $2,577. Effective Jan 1, 2026 — confirm YOUR exact rate at the official Defense Travel Management Office BAH lookup.
Town-by-town prices and market stats in this video are the June 2026 MLS snapshot from filming; the companion page above carries the current table. The BAH-based budget shown is one conservative planning scenario — not a lending rule and not a limit on what you qualify for. Prices, taxes, insurance, school assignment, flood status, HOA/MUD/PID costs, and commute times change and are address-specific: verify the exact address through official sources (county appraisal district, school district lookup, FEMA flood maps) before deciding. Nothing here is legal, tax, lending, or financial advice.

CONTACT
Taylor Dasch · Real Estate Agent · EG Realty
Call/Text: 254-718-4249
dealswithdasch@gmail.com
https://calendly.com/dealswithdasch
https://templetxhomes.net

#FortHood #PCSMove #MilitaryRelocation
```

What changed vs live: single primary destination in line 2 (companion page, not hub); one unified `utm_campaign=fort-hood-pillar` on every link; volatile city medians removed from the description (dated table lives on the page); "THE RULE / your max PITI" → "one conservative planning scenario"; "best schools" and "cheapest sticker, fastest exit" chapter labels neutralized; disclaimer covers address-level verification; hashtags cut to 3.

### Replacement pinned comment (delete BOTH existing owner comments; post + pin + heart this one)

```
Building your shortlist? Give me these five and I'll tell you which TWO towns to compare first: (1) the gate you'll report through or your work location, (2) rough monthly budget, (3) the second place you drive to most — spouse's job, school, gym, (4) your move month, (5) expected tour length. Drop them below — no pitch, I'll answer right here. Full 6-town breakdown + current numbers: https://templetxhomes.net/where-to-live-fort-hood/?utm_source=youtube&utm_medium=pinned&utm_campaign=fort-hood-pillar&utm_content=39Y6UpSFqu0
```

Deliberately does **not** ask for VA disability %, pay grade, or dependency status in public.

### Tags (replace once, then stop touching — low leverage vs title/thumbnail/satisfaction)

`fort hood housing, pcs to fort hood, moving to fort hood, where to live near fort hood, fort hood bah 2026, fort hood bah, fort hood off post housing, fort hood relocation, fort cavazos housing, moving to killeen texas, killeen tx homes, killeen vs harker heights, harker heights tx, copperas cove tx, nolanville tx, belton tx, temple tx, buy or rent fort hood, military relocation texas, va loan texas, bell county real estate, moving to temple texas, living in temple texas`

### Cards (max 3, placed at measured dips — verify existing card state in Studio first)
| Time | Why | Card |
|---|---|---|
| 3:00 | post-cliff re-engagement zone | Video: `6lyWBgezEXk` "How Much House Can You Afford in Temple, TX? (28/36 Rule)" |
| 9:50 | measured dip at 9:37 | Playlist: "Military PCS To Fort Hood Guides" |
| 12:10 | Belton/Temple chapters | Video: `eE7r32oTacg` "Temple vs Belton TX: Which Should You ACTUALLY Move To? (2026)" |

### End screen (17:48–18:08)
1. Video: `eE7r32oTacg` Temple vs Belton (2026) — freshest decision-intent sibling
2. Playlist: "Military PCS To Fort Hood Guides"
3. Subscribe element

### In-video edit decision (pre-committed, not executed now)
The 0:24–1:22 credibility block is the leak (85%→45% across 0:24–1:49; the drop was predicted in the July 13 audit before this data existed). n=74 is directional, not proof. **Gate:** at day 14 of the corrected package, if cumulative views ≥150 AND the 0:24–1:22 segment still shows a ≥25-point absolute retention drop, trim 0:24–1:22 in the Studio editor (chapter-boundary cut, URL/comments preserved), then rebuild chapter timestamps (−58s on everything after 0:24). If views <150, defer — impressions are the constraint, not the intro.

### Comment-reply playbook
1. SLA: reply within 4h for days 0–7 after the reset, daily thereafter.
2. Qualifying comment (gate/paygrade/tour/town): answer ONE concrete thing publicly with a real dated number, then invite the 5-input shortlist from the pinned comment. Never promise a payment, school assignment, tax outcome, commute time, or availability in-thread.
3. Crime/safety questions — model reply for the live West Temple comment (and template for all future ones):
   > "Crime is one thing I don't rank — it's block-by-block and it changes. The right sources are the Temple PD public crime dashboard and the Texas DPS crime data portal, plus driving the specific streets at different times. What I can run for you is inventory, price per square foot, and the commute from West Temple to your gate — want me to pull that?"
   Check Taylor's existing reply to that comment in Studio; edit or delete it if it ranks areas.
4. School questions → point to TEA txschools.gov + district address-lookup tools; never "best schools for your family."
5. Heart substantive comments; once a well-qualified thread develops, consider pinning it *below* the CTA comment period (one pinned at a time — CTA stays pinned for the first 30 days).

---

## 5. Primary companion page blueprint — `/where-to-live-fort-hood/`

**Decision: this is the primary companion.** Evidence: exact content fit (six-town comparison = the video's 1-1-1 decision), video already embedded immediately after the hero, FAQ schema verbatim-matches visible FAQ, lead form wired to the Railway relay, and its 35 impressions sit at position 8.3 (young page, upside). The hub keeps its embed as a secondary surface but gives up VideoObject markup (one canonical video page). The prior recommendation survives fresh evidence.

Keep (already right): URL, early embed placement, question-based H2 set, 10-question FAQ with verbatim schema, form-first hero CTA, "no single best town" defensive framing.

**Metadata (title/meta essentially sound — one compliance edit each):**
- SEO title (keep): `Where to Live Near Fort Hood 2026: All 6 Towns Compared` (55ch)
- Meta description (replace — removes "schools" as a selling axis): `Killeen, Harker Heights, Copperas Cove, Nolanville, Belton & Temple compared — 2026 BAH math, July 2026 MLS medians, gate commutes, and the disabled-veteran tax exemption.`
- H1 (keep): `Where to Live Near Fort Hood: All 6 Towns, by the Numbers`

**Opening direct-answer block (replace first paragraph under H1):**
> There is no single best town near Fort Hood — there is a best town for your reporting gate, your budget, your second daily destination, your tour length, and your exit plan. As of July 2026, the six corridor towns split roughly like this: Killeen and Copperas Cove carry the lowest medians ($245,000 and $249,999), Temple sits mid-band ($279,000) with the Baylor Scott & White medical economy, Harker Heights trades commute for space ($315,000 median, 2,149 sq ft median), and Belton ($335,000) and Nolanville ($370,900) price the newest stock. Source: CTXMLS, July 13, 2026 pull (active + pending + sold, last 30 days). The 18-minute video below walks the whole decision; the table further down carries the current numbers.

**Video block:** keep position; update `<iframe title>` AND VideoObject `name` to `PCS to Fort Hood (2026): 6 Towns Compared by BAH & Commute`; fix duration to `PT18M8S`; keep uploadDate 2026-06-30, contentUrl, embedUrl, maxres thumbnail. Caption stays.

**Six-town comparison table (replace current figures; add method line):**
| Town | Median price (Jul '26) | Median DOM | Median sqft | County | ISD (verify address) | Gate note |
|---|---|---|---|---|---|---|
| Killeen | $245,000 | 56 | 1,733 | Bell | Killeen ISD | closest to most gates |
| Harker Heights | $315,000 | 59 | 2,149 | Bell | Killeen ISD | east side, short run to East Range Rd |
| Copperas Cove | $249,999 | 55 | 1,658 | Coryell | Copperas Cove ISD | west gate side |
| Nolanville | $370,900 | 55 | 2,272 | Bell | Belton ISD (verify) | between Killeen & Belton |
| Belton | $335,000 | 62 | 1,976 | Bell | Belton ISD | I-14 corridor |
| Temple | $279,000 | 62 | 1,796 | Bell | Temple ISD / Belton ISD by address | longest commute of the six |
Method line under table: *CTXMLS pull July 13, 2026 — median across active, pending, and closed listings from the last 30 days. Numbers move; treat as a snapshot and verify the exact address.*

**Compliance rewrites (exact):**
- Scorecard label `Best schools · Coryell County` (×3) → `Coryell County · Cove ISD rated B (TEA 2025)`
- `the highest-rated district in the greater Fort Hood area` → `rated B in TEA's 2025 accountability ratings — check the zoned campus for any address at txschools.gov`
- FAQ Q6 `Which Fort Hood-area school district is rated highest?` → `How do I check school ratings and zoning for a specific address near Fort Hood?` with answer: TEA txschools.gov + each district's address-lookup tool + "ratings describe districts, not your address's campus; zoning changes." (Update FAQPage schema in the same edit — keep verbatim sync.)
- `stronger schools, newer homes, and a more diverse rental pool` → `newer housing stock and a tenant base that includes the BSW medical workforce, not just PCS cycles`
- `fastest resale / fastest exit / cheapest sticker` (×4) → `shortest median days-on-market in the July 2026 snapshot (56 days)` — describe the past, promise nothing
- `best/strongest long-term rental pool` (×4) → `a rental market that draws on the medical economy as well as the base (see the rental-market page for current data)`
- `do not buy a property over $400,000 in Bell County — at that price it will not cash-flow` → `in the July 2026 rent data, homes above roughly $400,000 rarely penciled as rentals — run the exact address before assuming either way`
- BAH math block: keep, but replace "ceiling" phrasing with: `Treat BAH × 0.95 as one conservative planning scenario — it is not a lending rule, and lenders may qualify you for more. Deciding to use less than your maximum is a choice, not a requirement.` Date the rate assumption: `illustration uses ~7.00% APR as of July 2026 — rates move weekly.`
- Commute table: add `off-peak estimates, July 2026 — verify against your actual gate and shift time; ask your unit which gate you'll report through.`

**Outbound citations to add (place next to the claims they support):**
- DTMO BAH lookup — https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/ (BAH table)
- Texas Comptroller, Tax Code §11.131 100% disabled-veteran exemption — comptroller.texas.gov (exemption section)
- Bell CAD — bellcad.org and Coryell CAD — coryellcad.org (tax + parcel verification steps)
- TEA txschools.gov (school-ratings FAQ)
- FEMA Map Service Center — msc.fema.gov (address-verification checklist)
- TxDOT project tracker (commute caveat)

**Address-verification checklist section (new, short — the AEO gem):** 6 steps: (1) confirm gate with your unit → (2) drive it at your shift time, (3) parcel on Bell/Coryell CAD for actual tax rate + exemptions, (4) school zoning via district lookup (not the district average), (5) FEMA flood zone + insurance quote before option period ends, (6) HOA/MUD/PID docs. This section answers the questions GSC shows people actually asking (commute + tax queries).

**Schema plan for this page (see §7 for JSON-LD):** one BreadcrumbList (3-item hierarchy), one WebPage @id referenced by Article.mainEntityOfPage, VideoObject synced, AggregateRating removed, FAQPage updated with the two rewritten Q&As.

**CRO:**
- Keep hero CTA "Get my custom short list" (form anchor) — it's correctly placed before the video.
- ADD a second CTA card immediately after the scorecard table: "Want this table run against your BAH and gate? Send me the five inputs — I'll send back your two-town shortlist." → same form anchor. (Primary conversion = shortlist form; secondary = call/text link. No third action.)
- Add `tel:` and Calendly links to the closing block; wire all CTA elements with the §8 events.
- Mobile/CWV: lazy-load the iframe (already `loading=lazy` ✓); re-run PageSpeed when quota resets (blocked July 13 run) and log LCP for the hero.

---

## 6. Military SEO cluster map (one row per URL)

| URL | Primary query (vol/mo) | Intent | Unique job | Title / meta / H1 action | Content action | Video? | Primary CTA | Canonical/index |
|---|---|---|---|---|---|---|---|---|
| `/where-to-live-fort-hood/` | where to live near fort hood (10) + best places to live near fort hood (20) + long-tail town comparisons | where-to-live decision | THE six-town comparison + video companion; owns the shortlist funnel | Keep title/H1; meta per §5 | §5 rewrites; July 13 table; citations | **YES — primary; the only VideoObject** | Shortlist form | index, self-canonical ✓ |
| `/military-relocation-temple-tx/` | fort hood housing (1,900) + moving/pcs to fort hood (~30) + "fort hood pcs housing guide temple tx" brand queries | hub / guide | The one relocation+housing hub; on-post vs off-post overview section (260/mo rising term lives here as a section); routes to all tools | Title → `Fort Hood Housing & Relocation Guide (2026): BAH, Towns, Taxes` (59ch); meta → `The Fort Hood housing hub: 2026 BAH by paygrade, six corridor towns, on-post vs off-post, property taxes, and the PCS timeline — updated July 2026.`; **H1 → `The Fort Hood Relocation & Housing Guide`** (kills the "Fort Hood / Fort Hood" bug) | Fix Article headline; absorb `/fort-hood/` gate matrix + REAL ID section; strip steering ("Killeen-volatility", "skip", "smart-money", best-schools FAQ → address-lookup FAQ); date/refresh ticker; appreciation claims → dated historical MLS statements or delete | Keep iframe, **remove VideoObject** | Guide download (PDF) | index, self-canonical ✓ |
| `/fort-hood/` | (cannibal — 24 residual impressions) | duplicate hub | None that the hub can't do | — | **Port unique content to hub, then 301 → `/military-relocation-temple-tx/`** via Rocket mu-plugin `10-templetx-redirects.php`; remove from any internal links (off-post page "Parent Hub" link → hub) | — | — | 301 |
| `/fort-hood-off-post-housing/` | fort hood off post housing (40) + on post housing fort hood (260, rising — section here until hub owns it) | on/off-post decision | The honest on-post vs off-post tradeoff + off-post area profiles | Title → `Fort Hood Off-Post Housing (2026): On-Post vs Off, Costs, Areas` (62ch→ trim to `Fort Hood Off-Post Housing Guide (2026): Costs & Commutes` 57ch); keep H1 minus "The Honest Guide" only if desired | **Fair Housing strip is the job**: delete every crime ranking/label, "Is Killeen safe" FAQ → "How do I research an area before a PCS?" (official sources), "Best Schools" card labels → TEA-cited facts, "best resale" → dated DOM; add outbound citations (currently zero); refresh April→July data | Embed iframe mid-page in the on-post-vs-off-post section, **no VideoObject** | BAH breakdown form (existing) | index, self-canonical ✓ |
| `/fort-hood-bah-calculator/` | fort hood bah (1,300) + fort hood bah 2026 + calculator variants | BAH data + tool | The rate table + BAH-to-price tool. **Highest-ROI snippet fix on the site** | Title → `Fort Hood BAH Rates 2026: Full Table by Rank + Calculator` (57ch); meta → `Every 2026 Fort Hood (TX286) BAH rate — E-1 to O-7, with and without dependents — plus a calculator that turns your BAH into a home-price range. Updated July 2026.` H1 keep | Source or drop the C+/B+/B− school grades (they're not TEA's scale — cite Niche + date, or delete from the comparison cards; recommend delete); date the 5.75% rate assumption; keep Dataset schema | No embed (tool page) — optional text link to video | Calculator itself; secondary: shortlist form | index, self-canonical ✓ |
| `/military-buy-vs-rent-pcs-calculator/` | buy or rent fort hood / military buy vs rent (long-tail; validate via GSC) | buy-vs-rent decision tool | The tour-length break-even tool | Title/H1 fine; fix H1 markup space (`Rent<span>` → renders "RentPCS") | **Remove the 31KB orphaned fragment after `</html>`** (second footer, placeholder video section, unmarked FAQ); ONE FAQ section, schema matching verbatim; delete best-schools + "better for a family" FAQ answers (replace per §5 pattern); date tax rates + 5.75% assumption; "watched Temple homes triple" → delete or restate as dated MLS fact | **No embed for now** (placeholder removed); revisit when a buy-vs-rent-specific video exists | Calculator → recommendation form | index, self-canonical ✓ |
| `/fort-hood-relocation/` | — | legacy URL | — | — | Keep 301 → hub ✓ (already correct, out of sitemap) | — | — | 301 ✓ |
| `/terms-of-use/` | — | trust | — | — | Publish a standard terms page (or repoint the sitewide footer link to /privacy-policy/ until one exists) | — | — | 404 → 200 |

**Cannibalization verdicts on the mission's query list:** pcs to fort hood / moving to fort hood / fort hood housing → hub. where to live near fort hood → companion. fort hood off-post housing → off-post page. fort hood bah 2026 → BAH calculator. military buy vs rent → buy-vs-rent calculator. killeen vs harker heights → currently unowned; cover as a section on the companion (scorecard already juxtaposes them); build a standalone comparison page only if GSC shows impressions after 60 days. Temple/Belton commute queries → hub's commute section (GSC already sends them there). The only true cannibal pair is hub vs `/fort-hood/` — resolved by the 301.

**Optional 30-day expansions (real search demand, buyer lane):** `nolanville tx homes for sale` (590/mo) and `killeen tx real estate` (480/mo) city pages — only after the core fixes land; keep investor framing out.

---

## 7. Exact schema plan

**A. Sitewide identity template (all cluster pages):** delete this node from the RealEstateAgent block:
```json
"aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "50", "bestRating": "5", "worstRating": "1" }
```
Re-add only if/when a page shows the actual reviews (with count and source) visibly on that page.

**B. `/where-to-live-fort-hood/` VideoObject (replace name/description/duration; rest unchanged):**
```json
{
  "@type": "VideoObject",
  "@id": "https://templetxhomes.net/where-to-live-fort-hood/#video",
  "name": "PCS to Fort Hood (2026): 6 Towns Compared by BAH & Commute",
  "description": "Taylor Dasch (EG Realty) compares Killeen, Harker Heights, Copperas Cove, Nolanville, Belton, and Temple for a Fort Hood PCS — 2026 BAH by paygrade, gate commutes, buy-vs-rent by tour length, the Texas disabled-veteran property-tax exemption, and how to decide your exit before you buy.",
  "thumbnailUrl": ["https://i.ytimg.com/vi/39Y6UpSFqu0/maxresdefault.jpg"],
  "uploadDate": "2026-06-30",
  "duration": "PT18M8S",
  "contentUrl": "https://www.youtube.com/watch?v=39Y6UpSFqu0",
  "embedUrl": "https://www.youtube.com/embed/39Y6UpSFqu0",
  "publisher": { "@id": "https://templetxhomes.net/#organization" }
}
```
Also update the `<iframe title="...">` attribute to the same name.

**C. Breadcrumbs (companion + both calculators + off-post):** keep exactly one BreadcrumbList per page. Recommended: delete the hand-built block and let AIOSEO emit it; if the 3-item hierarchy matters (it does for the cluster), configure AIOSEO's breadcrumb parent to the hub — otherwise keep the hand-built 3-item list and suppress AIOSEO's crumb JSON via its filter. Target trail for the companion: `Home > Fort Hood Relocation & Housing Guide > Where to Live Near Fort Hood`.

**D. WebPage/Article stitching (companion, buy-vs-rent):** Article.mainEntityOfPage must reference the existing `{"@id": "<url>#webpage"}` — no second WebPage node, no null-dated duplicates (the buy-vs-rent page currently ships `datePublished: null` on its duplicate).

**E. Hub:** fix `Article.headline` → `The Fort Hood Relocation & Housing Guide (2026)`; delete the VideoObject node (iframe stays); FAQPage: replace the best-schools Q&A with the address-lookup Q&A (§5 pattern) and re-sync the two near-miss questions the audit found (on-post/off-post wording, Killeen-or-Temple question — which should be removed entirely, not just synced).

**F. `/fort-hood/`:** no schema work — the page 301s away. Its FAQPage (with the gibberish Q1) disappears with it.

**G. Buy-vs-rent calculator:** delete the orphaned-fragment VideoObject (video not embedded); after the fragment removal, one FAQPage matching the single remaining visible FAQ verbatim.

**H. BAH calculator:** keep Dataset + WebApplication (good work — rare and AEO-valuable); dedupe to one BreadcrumbList; keep FAQPage but move the 3 out-of-block Q&As into the visible FAQ section (strictest-reading safety).

Validate every page in Rich Results Test after edits; re-run `tools/contrast_fix.py audit` after any publish (standing lint gate).

---

## 8. Internal-link + conversion map

**Internal links to ADD (anchor → destination):**
- Off-post page: `compare all six corridor towns side by side` → /where-to-live-fort-hood/ (currently zero links to it)
- Off-post page "Parent Hub" link → /military-relocation-temple-tx/ (currently → /fort-hood/, which will 301)
- Buy-vs-rent calculator: `which of the six towns fits your BAH` → /where-to-live-fort-hood/ (currently zero)
- Companion: in the on-post/off-post section, `full on-post vs off-post guide` → /fort-hood-off-post-housing/
- Companion: in the buy-vs-rent section, `run your tour-length break-even` → /military-buy-vs-rent-pcs-calculator/
- Hub: restore/add `off-post housing guide` → /fort-hood-off-post-housing/ (currently missing)
- /temple-tx-property-taxes/ (existing traffic magnet): contextual `where to live near Fort Hood` → companion
- /moving-to-temple-tx/: contextual `PCSing to Fort Hood? Start with the six-town comparison` → companion
Keep: hub hero → companion ✓; BAH calc → companion, off-post, buy-vs-rent ✓; companion → hub, BAH calc, Belton/taxes/BSW pages ✓. Do NOT link every page to everything — the spine is hub ⇄ companion ⇄ tools.

**UTM taxonomy (external → site only; internal links carry no UTMs):**
- `utm_source=youtube`
- `utm_medium=description | pinned | card | end_screen | community | shorts`
- `utm_campaign=fort-hood-pillar` (one name, everywhere, from now on)
- `utm_content=39Y6UpSFqu0`
Email uses `utm_source=newsletter&utm_medium=email&utm_campaign=fort-hood-pillar`; GBP uses `utm_source=gbp&utm_medium=post&utm_campaign=fort-hood-pillar`.

**GA4 events to implement (none exist today; small JS include on the 5 live cluster pages + relay form hook):**
| Event | Trigger | Params |
|---|---|---|
| `guide_download` | click on the PCS-guide PDF link | page_path |
| `bah_calc_start` | first input interaction on BAH calculator | — |
| `bah_calc_result` | result render | paygrade_band (E/O only — no PII) |
| `rentbuy_calc_start` / `rentbuy_calc_result` | same pattern on buy-vs-rent | tour_length_band |
| `phone_click` / `text_click` | `tel:`/`sms:` clicks | page_path |
| `calendly_click` | Calendly link click | page_path |
| `form_start` | first field focus on shortlist/lead forms | form_id |
| `generate_lead` | relay form success (exists on other pages — wire these forms the same way) | form_id, campaign |
Mark `generate_lead`, `bah_calc_result`, and `calendly_click` as key events. CRM side: tag inbound from this funnel `Fort Hood YT` (existing convention), no auto-FUB push of comment data — only real inbound with contact info, human-written follow-up.

**The one clean path:** YouTube impression → qualified watch → `/where-to-live-fort-hood/` (utm fort-hood-pillar) → shortlist form / BAH calc / buy-vs-rent → `generate_lead` tagged Fort Hood YT → source-attributed conversation.

---

## 9. Amplification calendar (no link-dumping, no unsolicited DMs, no fabricated engagement)

**First 48 hours (after Taylor approves the package):**
1. Thumbnail correction live (day 0 of the clean test window).
2. Description + tags + pinned comment replaced; old owner comments deleted; cards + end screen set; verify crime-comment reply.
3. Short #1 — **Gate-commute mistake** (source 5:43–6:40): hook "Same house. Ten extra minutes. Every day for three years." → YT Short + IG Reel. Caption CTA: "Full 6-town breakdown on the channel." (Never fully answer — the video completes it.)
4. Confirm video sits in "Military PCS To Fort Hood Guides" + "Relocating to Temple & Belton" playlists.

**Days 3–7:**
5. Short #2 — **Disabled-vet tax lever** (source 14:50–15:45, the measured retention spike): hook "Texas wipes the property-tax line to $0 for 100% disabled vets — here's what that does to a monthly payment." Include on-screen "verify eligibility: Texas Comptroller §11.131." TikTok + IG Reel (respect 3/wk TikTok cadence, never 2 same CT day).
6. Community post #1 — scorecard image + poll: "You get orders to Fort Hood tomorrow. What actually decides your town?" [ Gate commute / Monthly payment / Tour length / Exit plan ]
7. Temple Insider email — **DRAFT ONLY, gated**: subject `Same BAH. Six different outcomes.` — 150 words: the one-paycheck-six-towns premise, the July 13 medians table (3 rows), one link to the companion page (newsletter UTMs). No investor framing.
8. GBP post — **DRAFT via Postiz, gated**: "PCSing to Fort Hood? We compared all six corridor towns by 2026 BAH, commute, and exit plan — with July 2026 MLS medians." Link: companion page (GBP UTMs). Educational tone, no superlatives, entity declaration.

**Days 8–30:**
9. Short #3 — **Scorecard walkthrough** (source 6:57–7:15, the relative-retention peak): "Screenshot this before you book a single showing." YT Short.
10. Community post #2 — answer a real viewer question (anonymized): "Someone asked how to research an area before a PCS without ever visiting. Here's the 4-source method…" (official sources; models compliant behavior; links companion).
11. Admin-approved community sharing: identify 2–3 military-spouse/PCS Facebook groups + r/army-adjacent spaces; message admins first, offer the PDF guide as a pinned resource, post only with permission and only the guide (not the video).
12. Collaboration (one, credible): invite a **military spouse who has done a Fort Hood PCS** (or a veteran now living in the corridor) for a "what I wish I knew before our PCS" conversation — their story, Taylor's data, explicit "not affiliated with or endorsed by the Army" disclosure. Cut a Short from it pointing at this pillar.
13. Follow-up videos (each end-screens back to this pillar): (a) "Killeen vs Temple for a Fort Hood PCS" — already the planned next film after Salado; (b) "Buy or rent at Fort Hood: the tour-length math" (expands 2:23–5:43); (c) "On-post vs off-post at Fort Hood" (expands 14:13). These create the Suggested-traffic lattice this video lacks.

**Evergreen cadence:** BAH refresh every January (rate release) — description block, BAH calc, companion table; MLS table refresh monthly from market-monitor pulls (stamp the date); quarterly: retention re-check + GSC query review + this brief's rollback table updated.

---

## 10. Measurement dashboard

**Manual Studio pulls required (API cannot see these):** impressions + CTR by traffic source (Reach tab, custom range from day 0), YouTube search terms, end-screen CTR, card CTR, returning vs new viewers. Log them into the tracking table below at each gate.

| Gate | Metric | Baseline (old package) | Target | Minimum sample | Rule |
|---|---|---|---|---|---|
| 24h | Thumbnail corrected, comments cleaned, events live | — | done | — | binary checklist |
| Day 7 (+2 lag) | CTR | 3.71% (07-02) | ≥4% | ≥1,000 impressions | <4% → title switch per §4; <1,000 impressions → feed Suggested, don't churn |
| Day 7 | First-30s retention | ~70% | ≥70% | ≥75 new views | <60% → schedule the §4 intro trim immediately |
| Day 14 | 0:24–1:22 segment drop | −40 pts | <−25 pts | ≥150 cumulative views | ≥25-pt drop persists → execute Studio trim |
| Day 14 | Avg % viewed | 23.45% | ≥30% | ≥150 views | trending to channel norm (38%+) = content confirmed |
| Day 30 | Companion sessions from YT | 2 (17 days) | ≥25 | — | <10 → description/pinned placement problem, not page problem |
| Day 30 | Calculator starts (both tools) | unmeasured (0 instrumented) | ≥15 | — | events must exist by day 3 |
| Day 30 | `generate_lead` + qualified comment threads tagged Fort Hood YT | 0 | ≥2 qualified PCS conversations | — | ≥1 appointment → commit to monthly military video; 0 with good views → tighten in-video CTA + pinned, not the topic |
| Day 30 | GSC: companion impressions | 35/90d | ≥150/28d | — | reindex request after page edits; check "where to live near fort hood" coverage |

**Winner/loser calls:** package wins on watch-time share and downstream actions, never CTR alone. Views without conversations by day 30 = fix the funnel; conversations without views = scale distribution; neither = the lane's demand is on the website side (fort hood housing/BAH) — let the pages carry it and keep the video evergreen.

---

## 11. Prioritized implementation backlog

**DO NOW (single approval batch — YouTube + comments):**
1. Regenerate + swap thumbnail with correct six towns (Pikzels Prompt 1, labels correct or omitted) — factual exception to the hold.
2. Delete both existing owner comments (one collects VA disability %); post + pin + heart the §4 pinned comment.
3. Replace description + tags (§4 blocks, verbatim).
4. Set cards (3:00 / 9:50 / 12:10) + end screen (Temple vs Belton + playlist + subscribe) — after checking current state in Studio.
5. Verify/repair the reply on the crime-rate comment (§4 model).
6. Studio manual pull: impressions/CTR by source since 07-14 → log as pre-reset baseline.

**DO NOW (website batch — ready to execute on Taylor's go; every change reversible, rollback = restore prior page revision in Rocket WP + remove redirect line):**
7. Hub H1 + Article headline fix ("Fort Hood / Fort Hood" bug).
8. Fair Housing strip: off-post page (crime/school/resale), hub (Killeen-volatility/skip/best-schools FAQ), companion (§5 rewrites), buy-vs-rent FAQ, BAH-calc school grades.
9. Remove aggregateRating from the sitewide identity schema template.
10. Buy-vs-rent: delete orphaned post-`</html>` fragment; single FAQ + matching schema; drop unembedded VideoObject.
11. `/fort-hood/` → port gate matrix + REAL ID section into hub → 301 via `10-templetx-redirects.php`; update off-post "Parent Hub" link.
12. Companion: July 13 table + §5 direct answer + VideoObject/iframe title sync + breadcrumb/WebPage dedupe + outbound citations + second CTA.
13. `/terms-of-use/`: publish page or repoint footer.
14. GA4 event layer (§8) on the five live cluster pages.
15. GSC: request indexing on companion + hub after edits.

**AFTER 7-DAY PACKAGING DATA (day 9–14):**
16. Title switch decision per §4 rules (challenger #1 or #2 by impression mix).
17. Intro-trim decision per §4 gate (0:24–1:22, chapter timestamps rebuilt).
18. BAH-calculator retitle/meta (§6) — deliberately held out of the day-0 batch so its CTR effect is measurable on its own (its GSC baseline is clean).
19. Shorts #2–3 land per calendar; Temple Insider + GBP drafts go/no-go.

**WITHIN 30 DAYS:**
20. Follow-up video #1: Killeen vs Temple for a Fort Hood PCS (already queued after Salado).
21. Military-spouse/veteran collaboration episode.
22. Community posts #1–2; admin-approved group resource placement.
23. Evaluate: nolanville-homes (590/mo) and killeen-real-estate (480/mo) pages; killeen-vs-harker-heights page only if GSC shows demand.
24. Re-run PageSpeed/CWV on companion + hub (quota blocked the July 13 attempt).

**DO NOT DO:**
- Re-upload or reshoot the video (protect URL, comments, watch history).
- Change title and thumbnail simultaneously (after today's factual correction).
- Restate volatile city medians inside the YouTube description.
- Build a separate Fort Cavazos page (term collapsing: 720→90/mo).
- Build new pages for 10/mo queries (pcs-to-fort-hood standalone, commute pages).
- Ask for VA disability % (or any protected/medical detail) in public comments.
- Link-dump in military groups, DM strangers, buy engagement, or imply Army endorsement.
- Add investor framing to any page or video in this lane.

---

## 12. Sources, assumptions, unresolved risks

**Sources checked (2026-07-16):** YouTube Analytics API (views/retention curve/traffic sources/AVD, 06-30→07-14); YouTube Data API (live title/tags/description/comments/playlists via watch-page parse); live maxresdefault thumbnail; GA4 property 454804009; GSC via service account (28d + 90d); DataForSEO Google Ads volumes (June 2026 data month); live HTML of all 7 URLs + robots.txt + sitemap + /terms-of-use/ + PDF link (curl, Chrome UA); CTXMLS july-13 pull via market-monitor; BAH cross-check: garrisonledger.com, milpaytools.com (DTMO = canonical); local artifacts (FINAL.md beastmode run, POST-PUBLISH-OPTIMIZATION-2026-07-13.md, PIKZELS-RETITLE-2026-07-14.md, PUBLISH-titles.md, PUBLISH-traction-plan.md).

**Assumptions:** thumbnail change date ~07-16 (per mission; not API-verifiable); the July 2 owner comment is the currently pinned one (API does not flag pinned status); vidiq title scores are June 30 relative scores, not re-pulled; MLS medians blend active+pending+sold (stated wherever used).

**Unresolved risks / unverifiable today:**
1. Impressions/CTR since the reset — not exposed by local tooling; Studio manual pull required (the brief's gates depend on it).
2. Cards/end-screen current state — not API-visible; check before overwriting.
3. The reply text on the crime-rate comment — unread; could itself be a Fair Housing exposure until verified.
4. Retention curve is n=74 — shape is unambiguous but every retention decision carries a minimum-sample gate for this reason.
5. Core Web Vitals unverified (PageSpeed quota exhausted July 13; not retried).
6. YouTube search terms for the video — Studio-only; needed before concluding anything about search-title fit.
7. The 07-13 "hub premium sweep" appears to be the proximate cause of the buy-vs-rent orphaned fragment and possibly the hub H1 token bug — worth a quick check of the sweep's other ~28 pages for the same paste/template failure class (separate task; flagged).

---

## EXECUTION RECORD — 2026-07-16 evening (Taylor approved YouTube + website batches)

### YouTube (live)
- Description replaced (§4 block verbatim) + tags replaced via API — title untouched.
- New CTA comment posted (commentId UgzLWegd-d1MdTFbjXN4AaABAg) — **Taylor: pin it + delete the two old owner comments in Studio** (API cannot pin/delete).
- Corrected thumbnail generated (Gemini edit of live thumbnail; all six towns verified: Killeen/Harker Heights/Belton/Temple/Copperas Cove/Nolanville; face identity preserved): `thumbnail-corrected-2026-07-16.jpg` (1280×720, 244KB) — **Taylor: upload in Studio = day 0 of the 7-day window.**
- Cards/end screen: Studio-only — set per §4 (3:00 / 9:50 / 12:10; end screen: eE7r32oTacg + "Military PCS To Fort Hood Guides" + subscribe).

### Website (live, all verified by fresh curl + browser render)
| Change | Where | Rollback |
|---|---|---|
| aggregateRating removed sitewide (identity graph intact) | mu-plugin `00-templetx-identity-schema.php` | server `.bak-20260716` |
| GA4 events: phone/text/email/calendly clicks + guide_download sitewide | NEW mu-plugin `25-templetx-ga4-events.php` | delete file |
| `/fort-hood/` + `/fort-cavazos-housing/` + `/fort-hood-housing/` → 301 hub; page 56 drafted | mu-plugin `10-templetx-redirects.php` | server `.bak-20260716` + republish page 56 |
| Companion rebuilt: July 13 table, compliance rewrites, VideoObject/iframe synced to live title (PT18M8S), citations (DTMO/Comptroller/CADs/TEA/FEMA/TxDOT), new Ch.08 verification checklist, mid CTA band, design polish (numbered town cards, hovers, screenshot tag), form_start event, breadcrumb/WebPage deduped | page 2550 | WP revision |
| Hub: H1 token bug fixed → "The Fort Hood Relocation & Housing Guide", Article headline fixed, steering stripped (zone takes, school table→verification-first, FAQ sync incl. schema), ticker → JULY 13 2026 + $335K Belton + DOM 55-62, REAL ID/HSO/VA-appraisal section ported from /fort-hood/, off-post link added, VideoObject removed (companion = canonical video page), iframe title synced, crumb → /moving-to-temple-tx/ | page 30 | WP revision |
| Hub retitled: "Fort Hood Housing & Relocation Guide (2026): BAH, Towns, Taxes" + new meta (AIOSEO REST + post_title; old title purged live) | AIOSEO + WP | re-set old title via same endpoints |
| Off-post: ALL crime rankings/labels removed (incl. "Is Killeen safe" FAQ → official-source method), "Best Schools"/"Best Resale" tags → neutral, "Who belongs here" → "Best fit" (rank/budget-based), resale-risk table → demand-mix facts + July DOM, July 13 medians, video embedded at Ch. IV (start=853, no VideoObject), parent-hub link → real hub, dates April→July, breadcrumb deduped | page 219 | WP revision |
| BAH calc: uncited C+/B+/B− school grades removed (static + JS template), 5.75% rate dated "as of July 2026", hand breadcrumb (with stale /fort-hood/ crumb) removed, bah_calc_start/result events | page 1471 | WP revision |
| Buy-vs-rent: H1 spacing fixed, duplicate WebPage (null dates) + hand breadcrumb removed, tax rates dated + bellcad.org pointer (visible + schema), rentbuy_calc_start/result events | page 1717 | WP revision |
| `/terms-of-use/` created + published (fixes sitewide footer 404) | new page | set to draft |

### Verified post-deploy (2026-07-16 ~21:35 CT)
- All 5 cluster pages + terms: exactly one H1, exactly one BreadcrumbList (AIOSEO), zero steering-language flags, all JSON-LD parses, aggregateRating = 0 sitewide.
- 301s: /fort-hood/, /fort-cavazos-housing/, /fort-hood-housing/, /fort-hood-relocation/ → hub (direct, no chains).
- Companion visual render verified (hero + scorecard paint correctly; July medians on-page).

### Still held (by design)
- BAH-calc retitle → after the 7-day window (clean CTR measurement on its 4,197 impressions).
- Title switch + intro trim → day-9 / day-14 gates.
- Shorts #1–3, community posts, Temple Insider draft, GBP draft → amplification calendar (sends gated).

### Pre-reset baseline logged (Studio via Codex, window Jul 14–16 = new title + DEFECTIVE thumbnail era)
- 87 impressions (~29/day) · **CTR 6.9%** (~6 clicks — noise-level n, but up from 3.71% lifetime under the old title) · 10 views · unique viewers 7 (2 days still processing)
- By source (impressions / CTR / AVD): Suggested 34 / 8.8% / **8:59** · Search 25 / 4.0% / 0:24 · Browse 19 / 5.3% / 1:02 · Channel pages 9 / 11.1% / 18:38. Search terms report: insufficient traffic. External + Direct not shown.
- End screens: 0 clicks / 0.0% (window predates the July 16 end-screen setup). Watch time 94.2% non-subscribed.
- **Reading:** Suggested remains the quality channel (8:59 AVD) and search clicks still bounce (0:24) — consistent with the diagnosis. CTR is already above the 6% "strong" bar but the sample is 1/11th of the 1,000-impression minimum. **Impressions velocity is the binding constraint:** at ~29/day the 7-day window lands ~200 impressions, far under the gate. Unless the corrected thumbnail + amplification lift velocity ~5x, the day-9 call will fall in the pre-committed "<1,000 impressions → do NOT churn the title; feed Suggested (Shorts, cards, playlist, sibling videos)" branch. Day-9 pull (Jul 17–23 window) decides.
