# Week-0 Daily Execution Plan — Facebook Ads Launch

**Created:** 2026-04-13
**Source:** EXECUTION-PLAN.md Section 14 (40 tasks) broken into 10 working days
**Total estimated effort:** 35-45 hours
**Rule:** Do not spend $1 on ads until Phase 1 (Days 1-2) is complete.

---

## BLOCKERS — RESOLVE BEFORE DAY 1

These must be cleared before you start. If any are unresolved, you cannot begin.

| # | Blocker | Status | Action |
|---|---------|--------|--------|
| B1 | **Facebook Developer / Business Manager access** | BLOCKED (per TODO.md) | Fix account issue. Try "skip business portfolio" option. Cannot proceed without this. |
| B2 | **TX real estate attorney consult on SB 140** | NOT SCHEDULED | Schedule 60-min consult ($300-500). Determines whether FUB auto-text is legal or needs email-only fallback. Call 2-3 attorneys this week to find availability. |
| B3 | **Landing page decision** | UNDECIDED | Decide: build dedicated `/bsw-relocation` and `/pcs-temple` pages (recommended, 2-5x conversion lift) OR temporarily use existing pages. Dedicated pages are the plan — just confirm. |

**If B1 is stuck:** Days 1-2 are blocked. Skip to Day 3-6 tasks (lead magnets, ad copy, FUB config) and come back to Days 1-2 when access is resolved.

---

## DAY 1 (Monday) — Account & Pixel Foundation

**Focus:** Get Meta Business Manager live, domain verified, pixel installed.
**Estimated time:** 2-2.5 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 1 | Create Meta Business Manager account (or verify existing access works) | Taylor | 30 min | business.facebook.com. If the KW business portfolio issue from TODO.md is still blocking, use "skip portfolio" option. |
| 2 | Add `templetxhomes.net` as verified domain in Business Manager | Taylor | 20 min | Settings > Brand Safety > Domains. Requires adding a meta-tag or DNS TXT record. |
| 3 | Install Meta Pixel on templetxhomes.net | Taylor or web dev | 30 min | Options: (a) paste header code manually, (b) WP plugin (PixelYourSite or official Meta plugin). Header code is more reliable. |
| 4 | Verify pixel firing with Meta Pixel Helper Chrome extension | Taylor | 15 min | Install extension, visit 3-4 pages on templetxhomes.net, confirm PageView events appear in Pixel Helper. |
| 5 | Create ad account in Business Manager + add billing (credit card) | Taylor | 20 min | Business Settings > Ad Accounts > Add. Set currency to USD, timezone to CST. |
| 6 | Set up Conversions API (CAPI) via Zapier: FUB lead creation triggers Lead event to Meta | Taylor | 60 min | Zapier: Trigger = FUB new person created. Action = Meta Conversions API Lead event. This gives Meta server-side data in addition to browser pixel. |

**Day 1 done-check:** Open Meta Events Manager. Navigate to templetxhomes.net. See "PageView" events appearing. Ad account shows "Active" with payment method attached.

**Claude can pre-do:** Nothing on Day 1 — all tasks require Taylor's login credentials and browser access.

---

## DAY 2 (Tuesday) — Audience Infrastructure

**Focus:** Build the custom audiences that feed your campaigns.
**Estimated time:** 1.5-2 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 7 | Export FUB contacts as CSV (name, email, phone) | Taylor | 10 min | FUB > People > Export. Include all contacts, not just active. This becomes your suppression list. |
| 8 | Upload FUB contacts to Meta Audiences as Customer List — **SUPPRESSION ONLY** | Taylor | 20 min | Audiences > Create > Custom Audience > Customer List. Upload CSV. Label it "FUB Suppression — Do Not Target." This prevents showing ads to people already in your CRM. |
| 9 | Build Video Viewers Custom Audience | Taylor | 15 min | Audiences > Custom > Video. Select YouTube tour videos (if connected) or FB/IG videos. Set: 25%+ view, 365-day retention. |
| 10 | Build Website Visitors Custom Audience | Taylor | 10 min | Audiences > Custom > Website. Rule: All website visitors, 180-day window. Populates retroactively from pixel data. |
| 11 | Build Social Engagers Custom Audience | Taylor | 10 min | Audiences > Custom > Facebook Page + Instagram Account. Set: anyone who engaged, 365-day window. |

**Day 2 done-check:** 4 custom audiences visible in Audiences Manager (Suppression, Video Viewers, Website Visitors, Social Engagers). All show "Populating" or have a size estimate.

**Claude can pre-do:** Nothing — requires Ads Manager access.

---

## DAY 3 (Wednesday) — FUB Configuration + Legal

**Focus:** Wire up the CRM so leads get instant follow-up. Start legal consult.
**Estimated time:** 2.5-3 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 12 | Create FUB lead source tags: `BSW-META`, `MILITARY-META`, `BSW-CHATBOT`, `MILITARY-CHATBOT` | Taylor | 10 min | FUB > Admin > Lead Sources. These tags auto-sort incoming leads so you know exactly where they came from. |
| 13 | Configure BSW Medical Meta action plan | Taylor | 45 min | See EXECUTION-PLAN.md Section 8 for exact sequence: auto-text at min 0, email #1 with lead magnet PDF, call task at min 5, Day 3 text, Day 7 email, Week 2+ nurture. |
| 14 | Configure Military Meta action plan | Taylor | 45 min | Same structure as BSW but military-specific messaging. "When are orders dated for?" as opening text. BAH guide as lead magnet. |
| 15 | Test FUB integration end-to-end | Taylor | 20 min | Submit a test lead with your own email. Verify: auto-text fires, email #1 delivers with PDF, call task appears in FUB. If any step fails, fix before moving on. |
| 16 | Schedule TX real estate attorney consult on SB 140 | Taylor | 30 min | Call 2-3 TX RE attorneys. Ask specifically about: "Does my FUB auto-text response to an opt-in form submission require SB 140 registration?" Budget $300-500. If you cannot get an appointment before launch, use email-only auto-response as interim. |

**Day 3 done-check:** Test lead in FUB shows correct source tag, auto-text sent, email delivered, call task created. Attorney consult scheduled (or email-only fallback decided).

**Claude can pre-do:**
- Draft the auto-text copy for both action plans (already in EXECUTION-PLAN.md Section 8)
- Draft the email nurture sequence copy
- Draft the FUB task descriptions

---

## DAY 4 (Thursday) — Lead Magnets + Compliance

**Focus:** Produce the two PDF lead magnets that make the ads work.
**Estimated time:** 5-7 hours (heaviest day)

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 19 | Produce "Temple Physician Relocation Brief" PDF | Taylor + Claude | 3-4 hrs | 6-8 pages: commute map to BSW, school district table (TEA ratings), physician mortgage math (0% down, no PMI), 3 neighborhood profiles (Alta Vista, Canyon Creek, Windmill Farms), current market data ($265K median, 6.9 mo supply). Use brand colors (#1e293b / #059669 / white). |
| 20 | Produce "Fort Hood BAH 2026 + VA Buyer Guide" PDF | Taylor + Claude | 2-3 hrs | Contents: BAH table all pay grades (w/ and w/o dependents), VA loan myth busters (340+ Bell County closings), PCS 60-day timeline (orders to keys), commute cards (Fort Hood gate to each neighborhood), $500 rebate disclosure. |
| 17 | Verify TREC license number displayed in footer of templetxhomes.net | Taylor | 10 min | Check site footer. Must show license number. |
| 18 | Draft and publish TREC Consumer Protection Notice link on FB/IG business profiles | Taylor | 15 min | Link to official TREC notice. Must be on both Facebook business page and Instagram profile. 12-point font minimum. |

**Day 4 done-check:** Two PDFs complete and saved. TREC links live on FB/IG profiles. Site footer shows license number.

**Claude can pre-do:**
- **Draft both lead magnet PDFs** — Claude can write all the content, data tables, and copy. Taylor reviews and drops into Canva/design tool.
- Research current TREC Consumer Protection Notice URL

---

## DAY 5 (Friday) — Ad Copy + Fair Housing Review

**Focus:** Finalize all ad copy. Run compliance checks.
**Estimated time:** 2-3 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 29 | Write finalized ad copy: BSW-1 "The HR Gap" + MIL-1 "The BAH Math" | Taylor + Claude | 45 min | Copy already drafted in EXECUTION-PLAN.md Section 6. Review, personalize, finalize. Remember Correction 1: reframe HR gap as practical ("HR focuses on employment logistics") not legal ("BSW can't legally recommend"). |
| 30 | Fair Housing compliance review | Taylor | 20 min | Read ALL ad copy against Correction 3 checklist. No "perfect for physicians," no "great for families," no "safe neighborhood." Describe properties and facts, not people. Every ad must show "EG Realty" at 50%+ of largest font. |
| -- | Draft 2-3 additional ad copy variants per audience | Claude (pre-draft) | -- | BSW-2 through BSW-5 and MIL-2 through MIL-5 are already written in EXECUTION-PLAN.md. Review and approve your top 2 per audience for launch. |

**Day 5 done-check:** 2 finalized ad copy sets (1 BSW, 1 Military) that pass Fair Housing review. "EG Realty" broker name visible in every ad. No banned language.

**Claude can pre-do:**
- **All ad copy is already drafted** in EXECUTION-PLAN.md Section 6 (5 BSW variants, 5 Military variants)
- Run a Fair Housing language audit on each variant
- Flag any copy that needs reframing per Correction 1 (Stark Law) or Correction 3 (Fair Housing)

---

## DAY 6 (Saturday) — Creative Production: Static Images

**Focus:** Design the ad images in Canva.
**Estimated time:** 3-4 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 27 | Design BSW static image ad | Taylor (Canva) | 60-90 min | Neighborhood commute data visualization. Brand colors: #1e293b dark navy / #059669 emerald / white. Show: "Alta Vista: 6 min to BSW. Canyon Creek: 10 min." Clean data table format — physicians are analytical, data visuals beat lifestyle photos. |
| 28 | Design Military static image ad | Taylor (Canva) | 60-90 min | BAH comparison table as clean graphic. Show pay grades vs Temple home payments. Same brand colors. Lead with the number: "O-3 BAH: $2,340/mo. This home: $2,180/mo." |

**Day 6 done-check:** 2 static ad images exported at 1080x1080 (feed) and 1080x1920 (stories). Saved and ready for upload.

**Claude can pre-do:**
- Provide exact data tables and copy for each image
- Specify layout recommendations (data placement, font hierarchy, color codes)
- Generate Canva design briefs with exact dimensions and text

---

## DAY 7 (Monday) — Landing Page Build: BSW

**Focus:** Build the BSW dedicated landing page.
**Estimated time:** 3.5-5 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 21 | Build BSW landing page at `templetxhomes.net/bsw-relocation` | Taylor or web dev | 3-4 hrs | Use wireframe from EXECUTION-PLAN.md Section 7. Key elements: no navigation (logo only), hero with "BSW Recruited You — Here's What HR Can't Tell You", form above fold (first name + email only), neighborhood cards, school district table, physician mortgage section, market data, chatbot trigger at 15 sec. Mobile-first. Load < 2 sec. |
| 23a | Install lead form on BSW page with FUB webhook | Taylor | 30 min | Form submits to FUB via webhook. Must pass: first name, email, source tag = `BSW-META`. Test submission. |
| 24a | Add TREC license + EG Realty broker name to BSW page footer | Taylor | 10 min | Required for compliance. |
| 25a | Deploy Temple Concierge chatbot on BSW page | Taylor | 30 min | Custom opener: "Welcome — BSW physicians and staff are one of my specialties. Are you relocating for a new position, or exploring options?" |

**Day 7 done-check:** `/bsw-relocation` is live. Form submits create a lead in FUB tagged `BSW-META`. Action plan fires. Chatbot opens with BSW-specific greeting. Page loads < 2 sec on mobile.

**Claude can pre-do:**
- **Build the full landing page HTML** per the wireframe in Section 7
- Write all page copy (hero, neighborhoods, school district table, physician mortgage, market data)
- Generate the chatbot qualifying question flow

---

## DAY 8 (Tuesday) — Landing Page Build: Military + Mobile QA

**Focus:** Build the Military PCS landing page and QA both pages.
**Estimated time:** 4-5 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 22 | Build Military PCS page at `templetxhomes.net/pcs-temple` | Taylor or web dev | 3-4 hrs | Wireframe in Section 7. Key elements: hero with "Fort Hood PCS? Here's the VA Buyer's Playbook", BAH table above fold, form (first name + email + optional pay grade dropdown), VA myth section, PCS 60-day timeline, commute cards, $500 rebate section, chatbot. |
| 23b | Install lead form on Military page with FUB webhook | Taylor | 30 min | Source tag = `MILITARY-META`. |
| 24b | Add TREC + EG Realty to Military page footer | Taylor | 10 min | |
| 25b | Deploy Temple Concierge chatbot on Military page | Taylor | 30 min | Opener: "PCS-ing to Hood or separating from service? Different situations — which applies?" |
| 26 | Mobile test BOTH landing pages (iPhone Chrome + Safari) | Taylor | 30 min | Checklist: form fields work, CTA above fold on 375px width, no horizontal scroll, load < 2 sec on 4G, font >= 16px on form inputs (prevents iOS zoom). |

**Day 8 done-check:** Both landing pages live, forms working, chatbots deployed, mobile QA passed. Test leads appearing in FUB with correct tags and action plans firing.

**Claude can pre-do:**
- **Build the full Military landing page HTML** per wireframe
- Write all copy and data tables
- Create the mobile QA checklist

---

## DAY 9 (Wednesday) — Video Creative Production

**Focus:** Cut existing YouTube tours into Reels and produce Stage 1 awareness content.
**Estimated time:** 6-10 hours (can be split across Days 9-10)

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 31 | Cut 8 YouTube neighborhood tours into 15s and 30s vertical Reels (9:16) | Taylor or VA | 6 hrs | Add data text overlay in first 3 seconds (not scenery). Example first frame: "O-3 BAH: $2,340/mo. This home: $2,180/mo." Add captions (85% watched with sound off). Brand colors on text. Never start with "Hi, I'm Taylor Dasch." |
| 32 | Produce 3 Stage 1 (non-SAC) video content pieces | Taylor | 4-6 hrs | Three videos: (1) "Living in Temple for BSW Physicians" (2) "Fort Hood to Temple Commute Reality" (3) "2026 Temple Market Data." These are educational/lifestyle — NOT housing ads — so they get full Meta targeting. This is the strategic advantage. |

**Day 9 done-check:** 8 Reels cut and exported. At least 1 of 3 Stage 1 videos filmed or in post-production. (Stage 1 videos can trickle in — they feed the awareness campaigns, not the launch-day lead gen.)

**Claude can pre-do:**
- **Write scripts for all 3 Stage 1 videos** (hooks, data points, talking points, CTAs)
- Provide exact text overlay copy for each Reel
- Create a shot list / editing checklist for the VA

**Note:** Video production is the most time-consuming block. If you need to split this across two days, push some of Task 32 to Day 10. The Stage 1 awareness campaigns can launch a few days after the Stage 2 lead gen campaigns without hurting performance.

---

## DAY 10 (Thursday) — Campaign Build + Launch

**Focus:** Build all 4 campaigns in Ads Manager, submit for review, go live.
**Estimated time:** 3-4 hours

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 33 | Create Campaign 1: BSW Medical Cold | Taylor | 30 min | Objective: Leads. SAC: Housing. Budget: $20/day. Advantage+ Audience. 15-mile radius from BSW campus (2401 S 31st St). Creative: BSW-1 "The HR Gap" static + long copy. Destination: /bsw-relocation. |
| 34 | Create Campaign 2: Military Cold | Taylor | 30 min | Objective: Leads. SAC: Housing. Budget: $15/day. Advantage+ Audience. 15-mile radius from Fort Hood main gate. Creative: MIL-1 "The BAH Math" static + long copy. Destination: /pcs-temple. |
| 35 | Create Campaign 3: Stage 1 Awareness (non-SAC) | Taylor | 30 min | Objective: Video Views. **Do NOT declare Special Ad Category** (educational content). Budget: $10/day split BSW/Military. Full interest targeting per Sections 4-5: healthcare interests (28-55), military interests (20-48). Use Reel content from Task 31. |
| 36 | Create Campaign 4: Retargeting | Taylor | 20 min | Objective: Leads. Audience: Video Viewers + Website Visitors custom audiences. Budget: $5/day. Alternate lead magnet angle from cold campaigns. |
| 37 | Exclude FUB suppression list from Campaigns 1, 2, 3 | Taylor | 10 min | In each campaign's ad set, add FUB Customer List as exclusion audience. Campaign 4 (retargeting) does NOT exclude — retargeting known visitors is the point. |
| 38 | Submit all ads for Meta review | Taylor | 5 min | Hit "Publish" on all 4 campaigns. Meta reviews in 24-48 hours. |

**Day 10 budget check:**
| Campaign | Daily | Monthly |
|----------|-------|---------|
| BSW Medical Cold (SAC) | $20 | $600 |
| Military Cold (SAC) | $15 | $450 |
| Stage 1 Awareness (non-SAC) | $10 | $300 |
| Retargeting | $5 | $150 |
| **Total** | **$50/day** | **$1,500/mo** |

**Day 10 done-check:** All 4 campaigns submitted. Status shows "In Review" or "Learning." Budget totals $50/day.

**Claude can pre-do:**
- Provide exact campaign settings (objective, budget, audience, placement) as a copy-paste reference sheet
- Create UTM parameters for each campaign: `utm_source=meta&utm_medium=paid&utm_campaign=bsw-cold` etc.

---

## POST-LAUNCH (Day 11-12, Friday-Saturday)

| # | Task | Who | Time | Notes |
|---|------|-----|------|-------|
| 39 | Verify ads in "Learning" status, not "Rejected" | Taylor | 10 min | Check Ads Manager 24-48 hrs after submission. If rejected, read rejection reason and fix. Most common: missing SAC declaration on housing ads, or disapproved ad copy. |
| 40 | Day 2 post-launch: verify Lead events firing in Meta Events Manager | Taylor | 10 min | Events Manager > Data Sources > Pixel. Look for "Lead" events on form submissions. If only "PageView" shows, the form-to-Meta connection (CAPI via Zapier) is broken — fix immediately. |
| -- | Set up Monday monitoring routine | Taylor | 15 min | Create FUB Smart List: "Source = BSW-META or MILITARY-META + Last Contact > 7 days." This is your "about to go cold" list. Review every Monday morning. |

**Post-launch rule:** Do NOT change anything in the campaigns for 14 days. The algorithm is in learning phase. Any modification resets it. Watch CPM ($20-$35 healthy), CTR (>0.5% healthy), and whether leads arrive. Note, don't act.

---

## SUMMARY: What Claude Can Pre-Build Before Day 1

These tasks do not require platform access. Claude can complete them now so Taylor only handles the login/click/approval work.

| Deliverable | Status | Time Saved |
|-------------|--------|------------|
| BSW Physician Relocation Brief (full draft) | Claude can draft all content | 2-3 hrs |
| Fort Hood BAH + VA Buyer Guide (full draft) | Claude can draft all content | 1.5-2 hrs |
| BSW landing page HTML (per Section 7 wireframe) | Claude can build full page | 2-3 hrs |
| Military landing page HTML (per Section 7 wireframe) | Claude can build full page | 2-3 hrs |
| All ad copy (already written in EXECUTION-PLAN.md Section 6) | Done — needs Taylor review | 1 hr |
| Fair Housing compliance audit on all copy | Claude can run check | 30 min |
| FUB action plan copy (auto-texts, emails, task descriptions) | Claude can draft all | 1 hr |
| Stage 1 video scripts (3 scripts) | Claude can write | 1-2 hrs |
| Reel text overlay copy for 8 cut videos | Claude can write | 30 min |
| Canva design brief for BSW + Military static images | Claude can specify | 30 min |
| UTM parameter reference sheet for all campaigns | Claude can create | 15 min |
| Campaign settings reference sheet (copy-paste into Ads Manager) | Claude can create | 30 min |

**Potential time savings: 13-17 hours** if Claude pre-builds everything Taylor approves.

---

## CALENDAR VIEW

| Day | Date (suggested) | Focus | Hours |
|-----|-------------------|-------|-------|
| 1 | Monday | Account + Pixel setup | 2-2.5 |
| 2 | Tuesday | Audience building | 1.5-2 |
| 3 | Wednesday | FUB config + Legal | 2.5-3 |
| 4 | Thursday | Lead magnets + Compliance | 5-7 |
| 5 | Friday | Ad copy + Fair Housing review | 2-3 |
| 6 | Saturday | Static image design (Canva) | 3-4 |
| 7 | Monday | Landing page: BSW | 3.5-5 |
| 8 | Tuesday | Landing page: Military + QA | 4-5 |
| 9 | Wednesday | Video production (Reels + Stage 1) | 6-10 |
| 10 | Thursday | Campaign build + Launch | 3-4 |
| 11-12 | Fri-Sat | Post-launch verification | 0.5 |
| **Total** | | | **34-46 hrs** |

---

## FIRST 14 DAYS POST-LAUNCH: DO NOT TOUCH

After Day 10 launch, the algorithm enters learning phase. The single most important rule:

**Do not change audiences, budgets, creative, or targeting for 14 days.**

What to do instead:
- Monitor CPM, CTR, and lead volume (note, don't act)
- Respond to every lead within 5 minutes (the highest-leverage action)
- Score leads in FUB using the rubric in Section 9
- Review the "about to go cold" Smart List every Monday
- Prepare your next 2 ad variants for the Day 15 optimization window
