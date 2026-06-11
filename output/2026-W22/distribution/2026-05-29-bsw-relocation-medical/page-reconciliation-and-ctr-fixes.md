# BSW Page Reconciliation + CTR Fixes — paste-ready

Status: DRAFT / research. No live site edits made. This resolves the packet's #1 blocker (cross-page data conflicts) and turns the GSC findings into deployable page fixes. Deploy path at the bottom — approval-gated.

Why this exists: the BSW pages contradict each other (AI engines and Google penalize self-contradiction), and the highest-impression BSW page is buried. Fixing both directly serves page rankings + AI citation + unblocks every social asset in this packet.

Verification done 2026-05-28 with live sources (Freddie Mac/FRED, Ownwell, Bell County, bswhealth.com, Texas Higher Ed GME report) + MLS.

---

## 1. Canonical Facts (one value per fact — use everywhere, retire the rest)

| Fact | CANONICAL value to standardize on | Source + date | Pages to fix |
| --- | --- | --- | --- |
| Temple median sale price | **~$274,000** (median, closed, trailing ~12 mo) | MLS `closed-temple-belton-0-365.csv`, 2026-05-24 | relocation ($245K), roadmap ($246,538), physician ($255–260K) — all stale-low |
| Days on market | **~72 days median** (balanced market) | MLS, 2026-05-24 | add where "5.3 months inventory" is used |
| Match Day 2026 | **March 20, 2026, 11:00 AM CT** | NRMP / schema Event | **physician page says "March 17" — WRONG, fix** |
| GME orientation | **June 22, 2026** (residents arrive late May–mid June) | page schema Event | consistent — keep |
| Property tax | **~2% of assessed value combined (city+ISD+county+college); ~1.46% county median effective after exemptions. Verify by parcel at Bell CAD.** | Ownwell 2025 (1.46% effective); Bell County FY26 county-only 0.3327% | relocation (1.68%), roadmap (2.2–2.5%), physician (2.18%) — replace all with the framed version |
| 30-yr mortgage rate | **~6.5%** (Freddie Mac PMMS 6.51%, 2026-05-21; FRED 6.53%, 2026-05-28) | Freddie Mac / FRED | physician/roadmap hardcode 6.5–7% — either date-stamp "(~6.5%, May 2026)" or remove; keep OFF social |
| Physician loan | **0% down / no PMI is available through some lenders; residents can qualify on a signed contract before start; terms vary — verify with lender** | pages (Extraco, BMO, Texell CU, First Financial, First Horizon) | keep category-level; never promise eligibility/rate/approval/savings |
| GME program count | **Do not state a precise number** — sources conflict (Texas report "17", relocation page "31", roadmap "125+"). Say "30+ accredited programs (verify on bswhealth.com)" or omit | Texas Higher Ed GME report; bswhealth.com | roadmap "125+" is wrong (conflates VA's 125 affiliation agreements) — remove |
| Hospital scale | **~640-bed Level I Trauma Center, the only Level I between Dallas and Austin; one of Bell County's largest employers** | relocation page (verify vs BSW) | "636/640" + "8,884" — keep "~640-bed", soften employee count to "one of the largest" unless BSW-confirmed |
| On-site childcare | **At the Temple campus, BSW does not appear to run a dedicated on-site employee daycare** (its on-site/Bright Horizons childcare is at the Fort Worth campus). BSW does offer childcare *benefits/support* system-wide — confirm Temple specifics with BSW HR | bswhealth.com benefits; Bright Horizons (Fort Worth All Saints); Star-Telegram | scope childcare claims to "Temple campus"; don't say "BSW has no childcare" |
| Rent vs buy | **Residency-length rule: 1–2 yr prelim = rent; 3 yr = genuine toss-up; 4–7 yr / fellowship-to-attending = buying usually wins. Run your number.** | synthesis | physician page (pro-buy) and roadmap (pro-rent) contradict — align both to this |
| Track record | **Reconcile before publishing any figure** ($28.5M on pages vs $30M+/100+/#28-of-2,013 in CLAUDE.md) | — | omit until Taylor confirms one number |

---

## 2. Per-Page Edit List (draft tasks)

### `/physician-mortgage-loans-central-texas/` — the buried whale (pos 55.6, 1,137 impr, 0.09% CTR)
The big lever here is NOT the title alone — at position 55.6 the page lacks topical authority and internal links. Do all four:
1. **Fix the Match Day date** "March 17" → "March 20, 2026" (factual error).
2. **Add internal links IN** from the hub and Match Day page (anchor: "physician mortgage loans"). The page has almost no internal links pointing to it — that's why it's buried.
3. **Date-stamp or remove** the hardcoded rate; keep loan claims category-level + add "Equal Housing Opportunity" near any loan language.
4. **Title/meta rewrite** (section 3) for the 0.09% CTR.

### `/baylor-scott-white-relocation/` (hub, pos 7.1, 1.12% CTR — weak for the position)
- Replace median ($245K → ~$274K MLS-dated), tax (1.68% → framed ~2%), program count (drop precise / "30+").
- Title/meta rewrite (section 3) — pos 7 with 1.12% CTR is leaving clicks on the table.
- Confirm it links OUT to all three spokes (Match Day, commute, childcare) + physician page = hub-and-spoke.

### `/bsw-temple-childcare-daycare-guide/` (pos 9.8, 1.85%)
- Scope the on-site claim to "Temple campus"; add "BSW offers childcare benefits/support system-wide — confirm Temple specifics with HR."
- Keep cost/waitlist figures labeled as estimates; verify the one extended-hours center by phone before it stays named.
- Title/meta rewrite (section 3).

### Match Day page canonical
- The ranking URL is `/match-day-2026-bsw-housing-timeline/` (5.12% CTR). Confirm the canonical tag points there, not to `/bsw-temple-match-day-housing-timeline/`. Fix if split.
- Refresh median to MLS ~$274K; align rent-vs-buy to the length rule.

### Cannibalization consolidation (do once)
Four URLs chase "best neighborhoods BSW": `/neighborhoods-near-bsw-by-commute/` (pos 6.4 — **keep as canonical**), `/best-neighborhoods-bsw/` (pos 15), `/best-neighborhoods-baylor-scott-white-temple-tx/` (pos 12.3, 0 clicks), `/best-neighborhoods-baylor-scott-white/` (pos 6.7, 0 clicks). → 301 the three losers into the commute page; consolidate their links. This likely lifts all of them.

---

## 3. CTR Title + Meta Rewrites (paste-ready; `/seo-snippet-writer` gates: title ≤60, meta ≤155)

### Physician page
Titles (pick one):
- `Physician Mortgage Loans in Central Texas | Temple TX` — 53 ✓
- `Doctor Home Loans in Temple TX: 0% Down, No PMI` — 47 ✓
- `Physician Loans Temple TX: How Residents Buy at 0% Down` — 55 ✓

Metas (pick one):
- `How physician mortgage loans work in Central Texas — the 0%-down, no-PMI options some lenders offer doctors and residents. By Temple agent Taylor Dasch.` — 150 ✓
- `Doctor & resident home loans in Temple, TX: how 0% down and no PMI work, who qualifies, and the real tradeoffs. Verify terms with your lender.` — 141 ✓
- `What physician loans are, how residents qualify on a signed contract, and where they fall short — from a Temple, TX agent. Not lender advice.` — 142 ✓

### BSW relocation hub
Titles:
- `Baylor Scott & White Temple Relocation Guide (2026)` — 51 ✓
- `Moving to Temple for BSW? Neighborhoods, Commute, Timeline` — 57 ✓
- `BSW Temple Relocation: Where to Live & When to Buy` — 50 ✓

Metas:
- `Relocating to Temple, TX for Baylor Scott & White? Neighborhoods by commute, the buying timeline, and honest tradeoffs from agent Taylor Dasch, EG Realty.` — 154 ✓
- `A local agent's Baylor Scott & White Temple relocation guide: commute-ranked neighborhoods, school zoning, and the Match-Day-to-keys timeline.` — 141 ✓
- `Moving to Temple for BSW? Median ~$274K, balanced market. Neighborhoods, commute, and buying timeline from agent Taylor Dasch, EG Realty.` — 137 ✓

### Childcare page
Titles:
- `Childcare for BSW Temple Medical Families | Waitlists` — 53 ✓
- `Temple TX Daycare for Medical Shift Workers | BSW Guide` — 55 ✓
- `BSW Temple Childcare: Shift Hours, Waitlists & Cost (2026)` — 58 ✓

Metas:
- `Childcare near Baylor Scott & White Temple for medical families: shift-hour reality, waitlist timing vs your start date, and how to bridge the gap.` — 147 ✓
- `Why medical families should start the Temple childcare search before housing: 6–6 daycare hours, waitlists, and shift-friendly options near BSW.` — 144 ✓
- `A Temple agent's childcare guide for BSW shift workers: hours, waitlist reality, and the centers that fit medical schedules. Estimates — verify locally.` — 153 ✓

All titles ≤60, metas ≤155. Lane: BSW buyer/relocator. No banned words. No loan promises. Entity present.

---

## 4. Deploy Path (one approval, low effort)

Pick one and reply:
- **"Codex it"** → route the title/meta + reconciliation edits to Codex Computer (AgentFire/Yoast UI) per your standard workflow. I'll hand Codex this exact file as the change spec. (Loan page edits I'd flag for your eyes first.)
- **"I'll paste"** → you paste the titles/metas into Yoast and apply the reconciliation values; takes ~15 min.
- **"Just the date + cannibalization"** → smallest safe first move: fix the physician page's wrong Match Day date and 301 the duplicate neighborhood URLs. Lowest risk, real ranking upside.

Nothing here is live yet. Loan-claim language on the physician page should get your eyes before it ships regardless of who applies it.
