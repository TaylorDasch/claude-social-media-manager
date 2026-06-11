# Pre-Publish Checklist

Run this before camera-on, and again before upload.

---

## Data freshness

- [ ] **MLS data re-pull within 24–48hr of filming.** Most-recent baseline: `~/market-monitor/05-14-2026-mls-templebelton.csv`. If headline numbers move >3 percentage points from 05-14, restate on camera.
- [ ] **Confirm 856 active / 147 sold last 30d / 53.6% price-drop rate / 84-day median DOM** still hold within ±3pp at filming date.
- [ ] **If any headline number has moved >3pp, update the script + lower-third + thumbnail before filming.**

## Verifications (CTAs and infrastructure)

- [ ] **VERIFY: Calendly URL exists.** Path `calendly.com/dealswithdasch/temple-market-read-call` may not be configured. If not, set up OR fall back to `calendly.com/dealswithdasch` root and update description + pinned comment accordingly.
- [ ] **CONFIRM: 48-hour email-response commitment.** The free-path CTA promises a Gmail draft within 48 hours on filtered MLS pulls. Either block 30 min/day for first 30 days post-publish OR remove the offer and replace with Calendly-only.
- [ ] **VERIFY: Buy-versus-rent calculator page** referenced in BSW section. If page does not exist, remove the line from description OR build the page before publish.
- [ ] **VERIFY: BAH-to-house calculator page is live** at templetxhomes.net/military/bah-calculator/ — UTM-tagged URL works in incognito.
- [ ] **VERIFY: Builder Incentive Scanner page is live** at templetxhomes.net/new-construction-buyers-agent-temple-tx/builder-incentives/ — UTM-tagged URL works in incognito.
- [ ] **GA4 UTM tracking active** for `utm_source=youtube` + `utm_campaign=may-2026-market-read`.
- [ ] **Email path inbox-readiness.** Verify `dealswithdasch@gmail.com` is the correct address. Gmail filters won't auto-archive incoming requests with zip codes / price bands. Consider a dedicated subject-line keyword (e.g., "TEMPLE MLS PULL — zip + price band").

## On-camera authority signals

- [ ] **VERIFY: $X+ closed volume and # closed transactions as of filming.** Pull live count from FUB + TC. Update "About Taylor Dasch" block in description.
- [ ] **VERIFY: BSW GME program count (~31 programs / 100-150 residents per June cohort).** Re-check BSW press releases at filming.
- [ ] **VERIFY: TREC license #0792553 displays correctly on camera + matches licensed name.**
- [ ] **VERIFY: BiggerPockets Featured agent status still current** at filming date.

## Voice + lane discipline

- [ ] **Banned-word audit on final transcript** — none of: dream, nestled, charming, vibrant, perfect, broker, turnkey, hidden gem, paradise, oasis, stunning, gorgeous, exclusive, insider.
- [ ] **Lane discipline audit on final transcript** — none of: cap rate, gross yield, BRRRR, 1% rule, cash-on-cash, ROI (singular use as "largest single financial decision" acceptable).
- [ ] **"Agent" not "broker"** in every spoken reference.

## Format rules (per brief)

- [ ] **Identity declaration in first 3 sentences but NOT first 15s.** Verify in final edit. Sentence 3 should land between 0:18 and 0:24 — re-cut if Taylor's delivery puts identity before 0:15.
- [ ] **ONE creative element rule.** Two-snapshot laptop reveal is THE element. No second physical-prop reveal. No second "watch this" moment.
- [ ] **Honest negatives present by minute 5.** Verify the Pool A / Pool B framing landed by 4:00 and that the BSW honest counter (buy-vs-rent math) lands by 5:30.
- [ ] **Lower-third date stamp visible from 1:00 onward.**
- [ ] **EHO + Fair Housing + TREC §531.19** disclaimer audible in hook block + visible in lower-third.

## File + folder hygiene

- [ ] **Save dated MLS CSV** referenced in description to `~/market-monitor/05-14-2026-mls-templebelton.csv` — confirm file still in place.
- [ ] **Deepmode lineage preserved** at `~/claude-social-media-manager/yt-videos/temple-market-read-may-2026/deepmode-run-260517-1620/`.
- [ ] **Anti-duplication check** against all 24 prior yt-videos folders — confirmed clean during Phase 1 anchor.
- [ ] **Folder name** consistent: `temple-market-read-may-2026/`. 30-day follow-up will go to `temple-market-read-jun-2026/`.

## Repurpose readiness

- [ ] **Short / Reels / TikTok-buyer-lane vertical edit** queued from same master footage.
- [ ] **GBP post draft** ready with thumbnail + link.
- [ ] **LinkedIn post draft** ready (300-400 words).
- [ ] **Temple Insider email teaser draft** ready (~200 words).
- [ ] **Cross-platform publish schedule** confirmed (T+0 YT + GBP; T+1 Short; T+2 LinkedIn; T+3 email).

## 30-day re-pull commitment

- [ ] **Cron entry or calendar reminder** set for 2026-06-15 to re-pull MLS data and produce follow-up video if anything moved materially.
- [ ] **Folder pre-created:** `~/claude-social-media-manager/yt-videos/temple-market-read-jun-2026/` (empty placeholder — fill on 06-15).

---

## Final go/no-go gates

Before hitting Publish:

1. **Have all data-freshness items been re-verified within 48 hours?**
2. **Has every URL in the description been tested in incognito?**
3. **Has the 48-hour email-response commitment been confirmed (or removed)?**
4. **Has the script been read aloud start-to-finish at speaking pace? Did it land at 10:00-11:00?**
5. **Has the thumbnail (Thumbnail 1 primary) been finalized at 1280x720 with the date stamp legible at grid size?**

If any of those is "no," do NOT publish. Fix first, then re-run the checklist.
