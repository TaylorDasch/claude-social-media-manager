# CX-05 — BSW Page Reconciliation + CTR Fixes (Codex Computer / AgentFire)

Operator role: AgentFire Autonomous Site Operator (see `~/.agents/relay/prompts/agentfire-autonomous-site-operator.md`). Entity, brand voice, colors, and the Gate 1 banned-word list there apply. This is a BOUNDED job: make ONLY the edits listed below. Do not redesign, do not invent content, do not touch other pages.

Approved by Taylor 2026-05-28 ("all of it"). Source of truth for every value: `claude-social-media-manager/output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/page-reconciliation-and-ctr-fixes.md`.

## Hard guardrails (do not violate)
1. **Reversible:** before editing any page, save/duplicate the current AgentFire revision (or copy the existing title/meta/body block into the change log) so every edit can be rolled back.
2. **Preview before publish:** per the operator design, prepare each change and produce a preview/change-log. Push live only the four NON-loan items in Group A. For the loan page (Group B), STOP at preview and hand Taylor the approval packet — do not publish loan-page edits without his explicit go.
3. **No loan promises:** never add or strengthen any promise of eligibility, rate, approval, or savings. Keep loan language category-level ("some lenders offer," "terms vary, verify with lender"). Add "Equal Housing Opportunity" near loan content.
4. **No banned words** (Gate 1 list in QUALITY-GATES.md / the operator prompt). Say "agent," never "broker." Entity: Taylor Dasch with EG Realty, Temple, TX.
5. If any target text isn't found as written, SKIP that edit and report it — do not improvise a replacement.
6. Log every change (page, field, before, after) to a change log and report it back.

---

## GROUP A — publish after preview (low-risk, high-certainty)

### A1. Match Day page — fix factual error + refresh
- Page: `/match-day-2026-bsw-housing-timeline/`
- Confirm the canonical tag points to THIS url (not `/bsw-temple-match-day-housing-timeline/`); fix if split.
- Replace any "March 17" Match Day reference with **"March 20, 2026"** (only where it refers to Match Day 2026).
- Replace median price mentions ("$255K"/"$245K") with **"~$274K (median, MLS May 2026)"**.
- Align rent-vs-buy language to the length rule: 1–2 yr prelim = rent; 3 yr = toss-up; 4–7 yr = buying usually wins.

### A2. Cannibalization — consolidate "best neighborhoods BSW"
- In AgentFire Redirect Manager (Site Settings → AgentFire Settings → Redirects), add 301s:
  - `/best-neighborhoods-bsw/` → `/neighborhoods-near-bsw-by-commute/`
  - `/best-neighborhoods-baylor-scott-white-temple-tx/` → `/neighborhoods-near-bsw-by-commute/`
  - `/best-neighborhoods-baylor-scott-white/` → `/neighborhoods-near-bsw-by-commute/`
- Repoint internal links that pointed to the three retired URLs to the commute page.

### A3. Hub page — title/meta + reconciliation
- Page: `/baylor-scott-white-relocation/`
- Meta title → `Baylor Scott & White Temple Relocation Guide (2026)`
- Meta description → `Relocating to Temple, TX for Baylor Scott & White? Neighborhoods by commute, the buying timeline, and honest tradeoffs from agent Taylor Dasch, EG Realty.`
- Replace median ("$245K" → "~$274K, MLS May 2026"); replace tax "1.68%" with "roughly 2% of value (verify your parcel at Bell CAD)"; remove the precise GME program count or change to "30+ accredited programs."
- Confirm it links out to all 3 spokes (Match Day, commute, childcare) + the physician page.

### A4. Childcare page — title/meta + scope correction
- Page: `/bsw-temple-childcare-daycare-guide/`
- Meta title → `BSW Temple Childcare: Shift Hours, Waitlists & Cost (2026)`
- Meta description → `Why medical families should start the Temple childcare search before housing: 6–6 daycare hours, waitlists, and shift-friendly options near BSW.`
- Scope the on-site claim: "At the Temple campus, BSW does not run a dedicated on-site employee daycare (its on-site/Bright Horizons childcare is at the Fort Worth campus); BSW does offer childcare benefits system-wide — confirm Temple specifics with HR." Keep cost/waitlist numbers labeled as estimates.

---

## GROUP B — PREVIEW ONLY, do not publish without Taylor's go (compliance-sensitive)

### B1. Physician mortgage page — the buried whale (pos 55.6, 1,137 impr, 0.09% CTR)
- Page: `/physician-mortgage-loans-central-texas/`
- Fix the wrong Match Day date "March 17" → "March 20, 2026".
- Meta title → `Physician Mortgage Loans in Central Texas | Temple TX`
- Meta description → `How physician mortgage loans work in Central Texas — the 0%-down, no-PMI options some lenders offer doctors and residents. By Temple agent Taylor Dasch.`
- Add internal links INTO this page from the hub and Match Day page (anchor: "physician mortgage loans") — this is the main reason it's buried.
- Date-stamp or remove the hardcoded interest rate; add "Equal Housing Opportunity" near loan content; keep all loan claims category-level.
- Replace median "$255–260K" with "~$274K (MLS May 2026)".
- Prepare a preview + change log and hand Taylor the approval packet. Do NOT publish until he approves.

---

## Report back
A single change log: per page → fields changed, before/after, published vs preview-only, and any skipped edits with the reason. Confirm all rollbacks are available (AgentFire revisions + Redirect Manager rows).
