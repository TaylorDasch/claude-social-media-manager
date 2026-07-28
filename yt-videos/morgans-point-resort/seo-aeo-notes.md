# SEO / GEO / AEO Targets & Quotable Passages

> **Morgan's Point Resort — council rebuild, SEO / GEO / AEO Targets & Quotable Passages**
> Council run `reason-run-260726-2130` · Data: CTXMLS `whole-market-with-status-2026-07-20.csv`, pulled July 20 2026, recounted July 26 2026
> Ground truth: `GROUND-TRUTH-2026-07-20.md` · Supersedes the May 18 2026 version (archived in `archive-2026-05-18/`)

# 15. SEO / GEO / AEO TARGETS + QUOTABLE ANSWER PASSAGES

## 15a. Keyword targets — and an honest labeling of what is measured versus estimated

**PRIMARY TERM**

| Term | Volume | Provenance |
|---|---|---|
| `morgans point resort tx` | 3,600 / mo | **`[THIRD-PARTY EST.]`** — DataForSEO (Google Ads source), pulled 2026-07-26 |

**Two binding constraints on that number.**

1. **It is a third-party estimate, not a measurement.** Google Ads-sourced volumes are modeled, rounded to buckets, and aggregate close variants. It is directionally useful for deciding what to build and worthless as a precise figure. Every internal reference to it in this package carries the `[THIRD-PARTY EST.]` label.
2. **It never goes on camera and never appears in a graphic.** Section 1's provenance-chip design has exactly four states and none of them can carry a vendor keyword estimate — that exclusion is precisely what keeps the label set honest. A search-volume figure spoken on camera would be the one number in the video a viewer cannot verify against the MLS export, which is the entire credibility architecture of the package.

**SECONDARY TERMS — NO VOLUME PULLED**

The DataForSEO pull on 2026-07-26 covered the primary term only. **No search volume, CPC, or difficulty figure was retrieved for any term below.** These are ranked by strategic judgment — intent match, specificity, and the presence of the phrasing in the script — **not by measured or estimated demand.** No figure is asserted for them because none exists in this package's evidence, and inventing one would fail Hard Rule 1.

| # | Term | Volume | Intent | Where it is earned in the asset |
|---|---|---|---|---|
| 1 | `morgans point resort tx homes for sale` | **not pulled** | Transactional | Description Q-block, page link |
| 2 | `living in morgans point resort tx` | **not pulled** | Research / relocation | Title alternate 6, chapter 13 |
| 3 | `is morgans point resort a city` | **not pulled** | Definitional / AEO | Passage 1, script 1:10 segment |
| 4 | `morgans point resort vs belton tx` | **not pulled** | Comparison | Title alternate 8, chapter 4 |
| 5 | `morgans point resort belton lake` | **not pulled** | Geographic | Description, drone segments |
| 6 | `morgans point resort tx hoa` | **not pulled** | Verification | Passage 4, pinned comment |
| 7 | `morgans point resort schools` / `morgans point resort isd` | **not pulled** | Verification | Passage 5, chapter 12 |
| 8 | `belton lake homes for sale` | **not pulled** | Broader lake intent | Description tail |
| 9 | `morgans point resort tx real estate market` | **not pulled** | Market research | Passages 2, 8, 9 |
| 10 | `moving to morgans point resort tx` | **not pulled** | Relocation | Description "who this is for" |
| 11 | `morgans point resort tx lake access` | **not pulled** | High-risk verification | Passage 6, pinned comment |
| 12 | `bell county tx lake towns` | **not pulled** | Discovery / top-funnel | Hashtags, description tail |

**If volumes are wanted before publish:** re-run DataForSEO across the full list in one batch and record the pull date in this file. Until then the column reads "not pulled" and stays that way. DataForSEO has standing approval as the keyword/SERP source; the constraint here is that it has not been run for these terms, not that it is unavailable.

---

## 15b. The page reclaim play — `https://templetxhomes.net/morgans-point-resort/`

**Current measured state (Google Search Console):** average position **~18.7**, **712 impressions / 90 days**.

**Read that correctly.** GSC exports a **rolling 90-day window**, not a period-over-period delta. 712 impressions is the state of a trailing window, not a trend, and it must not be reported later as growth or decline unless it is compared against a stored snapshot of the same window length. Position 18.7 is page two — the page is indexed and understood, and it is losing to something, not invisible.

**The diagnosis this package supports `[OPINION]`:** a page sitting at 18.7 against a term with meaningful demand is usually not a technical failure — it is a **differentiation failure**. Everything ranking above it can say the same things: it's on Belton Lake, here are some listings, here's the school district. This video produces the one thing none of those pages have — a verifiable, town-specific, buyer-actionable finding recounted from a dated MLS export.

**The reclaim sequence, in order of leverage:**

1. **Embed the video at the top of the page**, above the listing grid, with the finished transcript published as visible on-page text (not only a caption track). The passages in 15c are written to survive being lifted out of that transcript.
2. **Add an FAQ block using the 10 passages in 15c verbatim**, marked up with `FAQPage` JSON-LD. Answer-first, date-stamped, entity-attributed — the passages are built to be excerpted without becoming dishonest.
3. **Add `VideoObject` schema** with `name`, `description`, `uploadDate`, `duration`, `thumbnailUrl`, `contentUrl`/`embedUrl`, and `hasPart` `Clip` entries mirroring the §13 chapters. Chapter titles are question-shaped specifically so Key Moments and AI answer engines can lift them.
4. **Rewrite the page's opening 50 words to answer "is this a separate city"** before anything else on the page. That is the definitional query the page is closest to owning and the one competitors handle worst.
5. **Add the verification block** (City of Morgan's Point Resort · USACE Belton Lake Resource Manager's Office · Belton ISD · per-property HOA) as a persistent on-page module. It is a genuine trust signal, it is compliance, and it is exactly the kind of specific-entity content AI answer engines cite.
6. **Internal links in, not just out:** link from the Belton page, the Temple-vs-Belton comparison, and the lake/waterfront content into this page using the phrasing "Morgan's Point Resort, TX" as anchor text.
7. **Do not touch the title tag or meta description after this change lands.** Standing rule: set once, then let it climb. Measure at 30 and 90 days against a stored GSC snapshot of the same window length.
8. **Date the page visibly** — "Market data: CTXMLS, July 20, 2026" — and re-pull on a set cadence. A dated page that is current outranks an undated page that is stale, and it is the single strongest AEO signal available for a market page.

**Success measure, defined in advance so it cannot be moved later:** a stored GSC 90-day snapshot taken at publish, re-pulled at 90 days, compared on impressions, average position, and clicks for the primary term. Any claim of improvement that is not backed by both snapshots is not a claim.

---

## 15c. Quotable answer passages — 10 passages, each ≤60 words

**Construction rules applied to every passage below.** Answer first, in the opening clause — no throat-clearing, because AI answer engines truncate the tail. **The date stamp and the entity attribution live inside the passage itself**, not in surrounding page furniture, so the passage stays honest and attributable after it is excerpted out of context. No passage asserts portal behavior. No passage promises lake access. No passage states HOA or schools as universal. No passage presents the active-vs-closed median gap as negotiating room. No passage says "in this window."

**These are for the page and the transcript. They are written to be excerpted. Word counts are exact.**

---

**P1 — "What is Morgan's Point Resort, TX?"** *(52 words)*

> Morgan's Point Resort is its own incorporated city on Belton Lake in Bell County, Texas — not a Belton subdivision. Taylor Dasch, an agent with EG Realty in Temple, Texas, notes that in the July 20, 2026 CTXMLS records, most listings physically in Morgan's Point Resort carry Belton in the MLS city field.

---

**P2 — "How much do homes cost in Morgan's Point Resort, TX?"** *(54 words)*

> As of July 20, 2026, the 15 active listings in Morgan's Point Resort, Texas ranged from $205,000 to $869,000, with a median list price of $330,000 and median size 1,791 square feet. Taylor Dasch, an agent with EG Realty, notes that median is a weak anchor — the range reflects different developments, not one market.

---

**P3 — "Why can't I find the affordable homes when I search Morgan's Point Resort?"** *(59 words)*

> It's a filing pattern. In the July 20, 2026 CTXMLS records, 11 of the 15 active Morgan's Point Resort listings have their MLS city field set to Belton — including all six actives under $275,000. Taylor Dasch, an agent with EG Realty, recommends searching by map area or ZIP, then confirming against the map.

---

**P4 — "Does Morgan's Point Resort, TX have an HOA?"** *(54 words)*

> Mostly no HOA, but not universally. Of the 29 Morgan's Point Resort MLS records dated July 20, 2026, 27 show HOA "None" and 2 show "Mandatory." Taylor Dasch, an agent with EG Realty in Temple, Texas, says to verify HOA status, dues, and restrictions on the specific property rather than assuming the town-wide pattern.

---

**P5 — "What school district is Morgan's Point Resort, TX in?"** *(50 words)*

> All 29 Morgan's Point Resort MLS records dated July 20, 2026 show Belton ISD. Taylor Dasch, an agent with EG Realty in Temple, Texas, notes attendance zones are assigned by address and change over time — verify your exact address directly with Belton ISD before relying on any listing's school field.

---

**P6 — "Do homes in Morgan's Point Resort, TX come with lake access?"** *(56 words)*

> Not automatically, and the MLS cannot answer it. The July 20, 2026 CTXMLS export for Morgan's Point Resort contains no waterfront, water-access, dock, or shoreline field. Taylor Dasch, an agent with EG Realty, directs buyers to the City of Morgan's Point Resort and the USACE Belton Lake Resource Manager's Office to confirm any lot's lake rights.

---

**P7 — "How old are the homes in Morgan's Point Resort, TX?"** *(54 words)*

> Older than buyers expect. The 15 active Morgan's Point Resort listings dated July 20, 2026 have a median build year of 1979, and 8 were built before 1980. Taylor Dasch, an agent with EG Realty, notes the 7 homes that closed May 18 to July 16, 2026 had a median build year of 2000.

---

**P8 — "Is Morgan's Point Resort, TX a fast-moving market?"** *(57 words)*

> No. Across the 15 active Morgan's Point Resort listings on July 20, 2026, median days on market was 28, but the 7 homes that closed between May 18 and July 16, 2026 took a median 93 days, and both pending homes had sat 206 and 239 days. Taylor Dasch, EG Realty. Seven sales is a small sample.

---

**P9 — "How much do sellers come down in Morgan's Point Resort, TX?"** *(58 words)*

> Some, but not dramatically. The 7 Morgan's Point Resort homes that closed between May 18 and July 16, 2026 sold near 91% of original list price. Of the 15 actives on July 20, 2026, 7 had cut price, median cut 4.7%. Taylor Dasch, EG Realty: that reads as sellers testing, not capitulating. Seven closings is thin evidence.

---

**P10 — "What is the price per square foot in Morgan's Point Resort, TX?"** *(57 words)*

> Price per square foot separates the tiers better than list price. Across the 15 active Morgan's Point Resort listings on July 20, 2026, $/sqft ran $151 to $310, median $188. Taylor Dasch, an agent with EG Realty, notes the two highest sit in Rancho Del Lago and Campus At Lakewood Ranch — newer developments, not MPR Sections 1–9.

---

### Passage-level provenance and compliance audit

| # | Words | Every figure traced to | Date stamp inside | Entity inside | Risk checks |
|---|---|---|---|---|---|
| P1 | 52 | GT §C, §A | ✅ | ✅ | Field value stated, not portal behavior ✅ |
| P2 | 54 | GT §A, §E | ✅ | ✅ | Median explicitly de-anchored (Rubric 6) ✅ |
| P3 | 59 | GT §C, §H1 | ✅ | ✅ | §H2-safe phrasing; instruction is map/ZIP ✅ |
| P4 | 54 | GT §A | ✅ | ✅ | Rule 5 — never universal ✅ |
| P5 | 50 | GT §A | ✅ | ✅ | Rule 4 wording preserved ✅ |
| P6 | 56 | GT §F | ✅ | ✅ | Rule 6 — City + USACE named ✅ |
| P7 | 54 | GT §B, §E, §I | ✅ | ✅ | §I window named, not "this window" ✅ |
| P8 | 57 | GT §A, §D, §I | ✅ | ✅ | n=7 named; no listing identified ✅ |
| P9 | 58 | GT §D, §I | ✅ | ✅ | §H3 — no median-gap leverage claim ✅ |
| P10 | 57 | GT §E | ✅ | ✅ | Subdivisions named as fact, no verdict on price ✅ |

**Passages written: 10. All ≤60 words. All answer-first. All date-stamped and entity-attributed internally.**

**Cross-check against §H4:** no passage uses the Pending median ($232,450) or the AUC median ($273,250). Both are seller ask, not agreed price, and no passage sequences them into a price ladder. ✅

**Cross-check against the description (W-17):** P7, P8, P9, and P10 contain findings deliberately withheld from the YouTube description. That is correct and intentional — the **page** should hold the full answer set for AI retrieval, while the **description** preserves the reason to watch. The two surfaces have different jobs and must not be made identical.

---
