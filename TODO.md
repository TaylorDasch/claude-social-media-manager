# TODO — Content OS System Health

> Generated: 2026-04-15
> Source: 8-persona swarm audit (40 findings) + fix execution pass

---

## Immediate (This Session / Next Session)

- [ ] **DOTW-002 publish (HARD DEADLINE):** Status READY_TO_PUBLISH (11 days stale). 1807 S 11th St is the centerpiece for Investor Brief Issue #2 shipping 2026-04-17. Publish today or Issue #2 has no centerpiece.
- [ ] **Omega page paste workflow:** Paste 2 ready-to-go sections into `/Users/taylordasch_1/real-estate-redefined/page-build-queue/temple-tx-homes/Buying Pages/new-construction/new-construction-complete/zOmega/Omega/omega-builders.html`:
  1. `yt-videos/omega-builders-deep-dive/omega-video-embed-section.html` → after hero, before verdict box
  2. `yt-videos/omega-builders-deep-dive/omega-floor-plan-section.html` → after photo gallery, before construction quality
  3. Swap `XXXXXXXXXXX` → real YouTube ID (9 instances, find/replace) post-upload
  4. Date refresh: "March 8, 2026" → "April 16, 2026", schema dateModified → 2026-04-16
- [ ] **Omega BSW Cottage Series blog (NEW):** Draft blog post "Omega Cottage Series: The Best Starter Home Option for BSW Medical Residents in Temple." Ties Cottage Series ($249K-$290K) at Hartrick Ranch + North Point → Extraco physician loan terms (0% down, no PMI, 3% seller concessions). Ride the Omega page update + BSW ad audience. Stage for post-filming publish.
- [ ] **Omega page [DATA NEEDED] backfill:** Fill placeholders on existing omega-builders.html:
  - Hartrick Ranch HOA
  - Hillside Village HOA (verify ~1.70% tax rate per Perplexity)
  - North Point HOA
  - Stylecraft warranty / HVAC / BBB data in 5-builder comparison
- [ ] **Omega page BSW angle section:** Add Medical Resident / BSW section to omega-builders.html. Call out Cottage Series plans qualifying for Extraco physician-loan terms. Omega has /medical-residents page — link to it.
- [ ] **BSW content scripting (BSW-001 to BSW-004):** 4 IDEA-state registry entries need research/scripting pass. Priority: BSW-001 Resident Housing Guide (PGY-1 to PGY-5 timeline). Leverages new `reference_physician_loan_terms.md` memory + existing /buy-before-first-day-of-residency-bsw/ page.
- [ ] **Tomorrow's filming lineup (2026-04-17):** 3 videos confirmed:
  - Market Report (Living in Temple) — easiest, lots of on-screen data
  - Temple vs Waco Investing (Investing in Temple) — needs I-35 dashcam hyper-lapse
  - Top 3 Luxury Neighborhoods (Living in Temple) — heaviest production, 2.5hr on-site
- [ ] **Filming prep (today):** B-roll route Caladium Dr (Hills of Westwood) → Oak Ridge → Pecan Creek → BSW. Charge drone + camera batteries. Confirm builder model home access (Legacy Ranch, Cliffs of Canyon Creek).
- [ ] **Market update videos stale:** LIT-007 (Feb update) and LIT-016 (Jan update) both REFRESH_DUE. Either refresh with April data or archive and create new monthly update.
- [ ] **Deal data freshness:** Verify closedDeals/pipeline in social-media-config.json is current (last updated 2026-04-13).

## Short-Term (This Week)

- [ ] **Skill governance headers:** Add `## Governance: Read governance/QUALITY-GATES.md before generating` to all 21 skill SKILL.md files that don't already reference it. Batch job: `grep -L "QUALITY-GATES" skills/*/SKILL.md`
- [ ] **Multi-pass reference:** Ensure all content-generating skills reference `governance/MULTI-PASS-SYSTEM.md` and specify which passes they use.
- [ ] **Lead magnet builds:** 5 of 8 lead magnets in LEAD-MAGNET-MATRIX.md are unbuilt (Deal Analyzer, Investment Playbook, PCS Checklist, BSW Commute Map, Relocation Guide). Prioritize: Deal Analyzer (investor persona, highest lead value) and Relocation Guide (general persona, widest reach).
- [ ] **TikTok performance baseline:** Pull TikTok analytics manually and seed performance-ledger.csv with TikTok entries. Current ledger has YouTube + newsletter only.
- [ ] **Video embed execution — 8 Tier 1 pages missing embeds (SEO bleed daily):** Only 2/13 Tier 1 pages have embeds (property-management-guide, sell-house-by-owner done). Need embeds on: best-neighborhoods, neighborhoods-near-bsw, cost-of-living, temple-vs-belton, living-in-belton, market-report, best-areas-long-term-rentals, assumable-loans. Batch after market-report video publishes.
- [ ] **2 × 404 pages on VIDEO-TO-PAGE-MAP:** Decide fate of investing-in-temple-tx-2026-playbook + out-of-state-investor-execution-playbook. Either build the pages or remove from map.
- [ ] **Hook bank refresh:** Check hook-bank.json for staleness. Some hooks are >30 days old. Run `/hook-bank` to generate fresh hooks for any pillar with <5 fresh entries.

## Medium-Term (This Month)

- [ ] **Performance ledger automation:** Build a weekly MCP pull that auto-populates performance-ledger.csv from YouTube, Beehiiv, and FUB data. Currently manual entry only.
- [ ] **Registry derivative tracking:** Many PUBLISHED videos still show 0 derivatives in registry. Run `/repurpose` audit: which videos have blog posts, which have TikTok clips, which have been embedded on pages?
- [ ] **Tier 3 page builds:** VIDEO-TO-PAGE-MAP.md Tier 3 lists 6 videos with no matching page. These are high-AEO-value pages: `/investing/out-of-state-mistakes/`, `/investing/foreclosure-auctions-temple-tx/`, `/temple-vs-killeen/`, `/investing/brrrr-strategy-temple-tx/`, `/temple-vs-austin-investing/`, `/investing/pre-foreclosures-temple-tx/`.
- [ ] **GBP post cadence:** No GBP posts tracked in registry. Start 4-week rotation per Gate 8: Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip.
- [ ] **Content calendar automation:** Make `/content-calendar` skill auto-pull from registry gaps, filming day queue, and production rhythm instead of generating from scratch each week.
- [ ] **Schema audit:** Run freshness-scanner.py with schema checks on all published pages. Many Tier 1 pages likely missing VideoObject schema.

## Long-Term (Next Quarter)

- [ ] **Cron-free architecture:** All automation runs inline via Claude at session start (SESSION-LOOP.md Step 0). Consider whether any background automation (Railway, Dispatch) should supplement the inline checks.
- [ ] **Performance-driven content planning:** When performance-ledger.csv has 30+ entries, build a model: which pillars/personas/formats produce CRUSH ratings? Weight content calendar toward proven winners.
- [ ] **Newsletter subscriber funnel tracking:** Connect Beehiiv subscriber growth to content events (video publish → subscriber spike?). Requires weekly analytics pull consistency.
- [ ] **AI citation monitoring:** Track whether GBP posts, blog posts, and pages are being cited by Google AI Overviews. DataForSEO MCP has AI optimization tools for this.
- [ ] **Content velocity target recalibration:** Current weekly target is 16 types. Actual production averages 1-3/week. Either reduce targets to achievable (film 1 video + produce pipeline = 8+ assets) or document the gap as intentional stretch.
- [ ] **Cross-project content triggers:** When TC module detects a new deal closing, auto-queue "Just Sold" content package. When listing-domination-os gets a new listing, auto-queue social launch sequence.

## System Health Rules (Always Enforce)

1. **Every session starts with Step 0** (SESSION-LOOP.md): run 4 scripts inline, check registry drift, check data vault freshness.
2. **No content ships without quality gates passing** (QUALITY-GATES.md): 16 gates, HARD gates block output, SOFT gates warn.
3. **Registry is the system of record**: every piece of content gets a row. No orphan files in output/ without a registry entry.
4. **Data vault is single source**: market stats live in TEMPLE-TX-DATA-VAULT.md, not duplicated in social-media-config.json or skill files.
5. **Performance feedback closes the loop**: CRUSH/SOLID/MEH/MISS ratings from Taylor go into performance-ledger.csv. Winners get expanded. Misses get diagnosed.
6. **Freshness is non-negotiable**: data older than its freshness window gets flagged before reuse (Gate 9). Pages older than staleness threshold auto-transition to REFRESH_DUE.
7. **No investor content on TikTok** (Gate 14). No YouTube repurposing to TikTok. No desk scripts. TikTok = original property tours only.
8. **NEVER send, always draft** (Gate 11). Emails = create_draft. Social posts = save to file. Nothing goes live without Taylor's explicit approval.
