# SEO / GEO / AEO Amplification — BSW Medical Relocation Cluster

Status: DRAFT. All site changes are separately approval-gated. Schema items below are proposed review tasks, not invented markup.

---

## Asset → Target Page Map (one page each, never homepage)

| Asset | Target page | Query/entity reinforced |
| --- | --- | --- |
| GBP 1, LinkedIn 1, Short 1, Newsletter | /match-day-2026-bsw-housing-timeline/ | BSW Match Day housing timeline, buy before residency |
| GBP 2, Short 2, IG Reel | /neighborhoods-near-bsw-by-commute/ | closest neighborhoods to BSW, commute by role |
| BSW-keyword default | /baylor-scott-white-relocation/ (hub) | Baylor Scott & White Temple relocation |

Social job: make humans and AI engines associate each page with its target question, repeatedly and in natural language, using the same entities (BSW, 2401 S 31st St, Temple ISD/Belton ISD/Academy ISD, Bell CAD, Match Day, GME orientation).

---

## AI-Citable Snippets (answer-first, extractable)

Drop-in passages for AI Overviews / ChatGPT / Perplexity. Defensible facts only (MLS + structural). Proposed for the matching page's answer block AND as the spine of the social copy.

### 1. BSW relocation (→ hub / relocation-assistance page)
> **Relocating to Temple, TX for Baylor Scott & White?** The path is: confirm your start date, line up financing on your signed contract, then choose a neighborhood by real commute and school zoning. Temple's median sale price is about $274,000 with homes selling in a median of ~72 days (MLS, May 2026) — a balanced market with room to inspect and negotiate. Taylor Dasch with EG Realty is an independent Temple agent (not affiliated with BSW) who helps relocating medical staff; verify all loan terms with your lender.

### 2. Match Day housing timeline (→ Match Day page)
> **How long do BSW residents have to find housing?** Match Day 2026 was March 20; BSW GME orientation is June 22 — about a 94-day window. Some physician loan programs let residents close using only a signed BSW employment contract, before the start date, with terms that vary by lender. In a balanced Temple market (~72-day median time to sell, MLS May 2026), the tighter constraint is usually the May–June moving squeeze, not the purchase. Source: Taylor Dasch with EG Realty, Temple, TX.

### 3. Neighborhoods near BSW (→ commute page)
> **What are the closest neighborhoods to Baylor Scott & White Temple?** BSW main campus is 2401 S 31st St. The closest neighborhoods sit within roughly 5–8 minutes by car, but "door-to-department" time can run 12–20 minutes once parking assignment and the campus shuttle are counted. Night-shift workers should also screen for freight-rail noise, and everyone should verify school zoning by address at Bell CAD — a Temple mailing address does not guarantee Temple ISD. Source: Taylor Dasch with EG Realty.

---

## Internal Linking (draft tasks — apply only on approval)

Build a tight BSW cluster so authority flows to the strongest pages and the lead magnet:

- Match Day page → link to commute page (anchor: "neighborhoods by commute to BSW").
- Commute page → link to Match Day page (anchor: "the 94-day Match-Day-to-keys timeline").
- Hub (`/baylor-scott-white-relocation/`) → link out to the Match Day and commute spokes and to the physician-mortgage page.
- Every BSW page → one clear link to the lead magnet: BSW Temple Relocation Guide PDF.
- Add the hub as the canonical "parent" so the cluster reads as hub-and-spoke to crawlers.

---

## SEO Findings From This Build (priority order — draft tasks)

These surfaced during the GSC + page audit. They are the highest-leverage fixes; route to `/seo-snippet-writer`, `/seo-schema`, or a page edit on approval.

1. **Physician-mortgage page is the buried whale.** `/physician-mortgage-loans-central-texas/` pulls **1,137 impressions** (highest in the BSW lane) but ranks **position 55.6 at 0.09% CTR** (GSC, 2026-05-28). This is a ranking/authority problem, not demand. Action: internal links from hub + Match Day; title/meta rewrite; reconcile its wrong "March 17" Match Day date. **Caution:** most compliance-sensitive page — keep loan language category-level, add a "verify with lender / Equal Housing" line.
2. **Keyword cannibalization on "best neighborhoods BSW."** Three URLs compete: `/best-neighborhoods-bsw/` (pos 15.0), `/best-neighborhoods-baylor-scott-white-temple-tx/` (0 clicks, pos 12.3), `/best-neighborhoods-baylor-scott-white/` (0 clicks, pos 6.7) — plus the strong `/neighborhoods-near-bsw-by-commute/` (pos 6.4 but only 101 impr). Action: pick ONE canonical neighborhoods page, 301 the duplicates into it, consolidate links. This is likely suppressing all of them.
3. **Match Day canonical mismatch.** The live, ranking, click-earning URL is `/match-day-2026-bsw-housing-timeline/` (17 clicks, 5.12% CTR), but the file's canonical tag reads `/bsw-temple-match-day-housing-timeline/`. Action: verify the canonical points to the indexed URL; fix if it splits signals.
4. **Cross-page factual conflicts (authority + trust risk).** Median price quoted four ways ($245K/$246,538/$255K/$255–260K), Match Day date two ways (Mar 20 vs Mar 17), property-tax rate three ways (1.68%/2.18%/2.2–2.5%), and the rent-vs-buy pages give opposite advice. Action: set one canonical figure per fact (median = MLS ~$274K dated; tax = "roughly 2%+"; one rent-vs-buy framing = the residency-length rule) and propagate across all BSW pages. AI engines penalize self-contradiction.
5. **CTR rewrites.** Hub `/baylor-scott-white-relocation/` ranks 7.1 but converts at only 1.12% CTR — title/meta opportunity. Physician page (pos 55.6) also needs snippet work. Route to `/seo-snippet-writer` (title ≤60, meta ≤155).

---

## Schema — Proposed Review Tasks (do NOT invent; verify/extend existing)

- **Match Day page**: already carries FAQPage + Event (NRMP Match Day 2026-03-20, BSW GME orientation 2026-06-22) + LocalBusiness. Task: confirm `dateModified` is current; confirm the LocalBusiness figure ("$28.5M+") is reconciled with the canonical track-record number before it stays in markup.
- **Commute page**: carries FAQPage (5 Q&A). Task: confirm `dateModified`; consider adding `BreadcrumbList` tying it to the hub.
- **Physician page**: carries FAQPage. Task: fix the "March 17" date inside any schema; keep loan answers category-level with a verification disclaimer.
- **Hub page**: confirm RealEstateAgent + FAQPage + BreadcrumbList present; it is the cluster parent.

No new schema types are proposed here beyond what the pages already use — only correctness, freshness, and the hub breadcrumb.

---

## Video Bridge

Existing BSW video assets in the registry: LIT-006 ("BSW Temple — Where Doctors and Nurses Actually Live" → commute page) and queued YT-PREP-008 ("BSW Nurses — Every Neighborhood Within 15 Minutes"). Lane: **Living in Temple (relocation/buyer)** — keep it there, do not cross into Investing in Temple. The Shorts in this packet can seed a companion folder `yt-videos/bsw-match-day-timeline/` when Taylor films. Do not blur the two channels.

## GBP Review Signal (Gate 15)

For satisfied BSW-relocator clients, coach them (never script) to mention naturally in a Google review: their role/timeline (resident, nurse, attending), which area they bought in, and the specific question Taylor helped them solve (commute, timing, rent-vs-buy). Those reviews become AI citation signals tying Taylor to BSW-relocation queries.
