# AgentFire Site-Fix Checklist — BSW Pages (verification audit)

Generated 2026-05-29. **No live edits were made to produce this — read-only verification only (HTTP GET).**

**Context:** CX-05 (Codex computer mode) reconciled **4** BSW pages live on 2026-05-29 and self-reported PASS. This checklist re-verifies each requested fix against the live site and — more importantly — surfaces what CX-05 did **not** cover. Do not treat "CX-05 PASS" as "all BSW pages clean."

Pages audited live: Match Day (**MD**), Relocation Hub (**HUB**), Childcare (**CHILD**), Commute (**COMMUTE**), Physician (**PHYS**), and **Resident→Attending Roadmap (ROADMAP — NOT in CX-05 scope)**.

Legend: ✅ done-live & verified · ⚠️ partial / follow-up needed · ❌ open

| # | Site-fix item | Status | Evidence (live, 2026-05-29) | Remaining action |
|---|---|---|---|---|
| 1 | Stale median price conflict | ⚠️ | MD / HUB / PHYS now ~$274K (verified live). **ROADMAP still shows `$250K` / `$246,538`.** | Fix ROADMAP median → "~$274K (median, MLS May 2026)". |
| 2 | Match Day date conflict | ✅ | "March 17" gone site-wide; PHYS now "March 20, 2026". ROADMAP carries no Match Day date. | None. |
| 3 | Tax-rate conflict | ⚠️ | MD / HUB / PHYS reframed to "~2% + verify Bell CAD". **ROADMAP still "2.2–2.5%" (11 references).** | Reframe ROADMAP tax → "roughly 2% of value, verify your parcel at Bell CAD". |
| 4 | Rent-vs-buy conflict | ⚠️ | MD + PHYS aligned to the residency-length rule (1–2yr rent / 3yr toss-up / 4–7yr buy). ROADMAP has its own "Should a BSW Resident Buy or Rent?" section ("it depends…") — not confirmed aligned. | Confirm ROADMAP's buy-vs-rent matches the length rule; re-align if it still leans pro-rent (it was the original contradiction vs the physician page). |
| 5 | Match Day canonical mismatch | ✅ | MD `rel=canonical` → self (`/match-day-2026-bsw-housing-timeline/`), **not** the `/bsw-temple-match-day-housing-timeline/` variant. All 6 pages self-canonical. | None. |
| 6 | Physician mortgage page reposition | ✅ | Title/meta live; Equal Housing present (×2); inbound links **MD→PHYS ×2, HUB→PHYS ×4**. The buried-whale now has real internal authority. | Optional boost: add COMMUTE→PHYS and CHILD→PHYS (both 0 today). |
| 7 | Internal links (MD ↔ commute ↔ childcare ↔ physician hub-and-spoke) | ⚠️ | See matrix below. Gaps: **HUB→MD = 0**, COMMUTE→PHYS = 0, CHILD→PHYS = 0, MD→CHILD = 0, COMMUTE→CHILD = 0. | Add the missing links (see "gaps to close"). |

---

## ❗ Highest-priority residual CX-05 missed — the Roadmap page

`/bsw-resident-attending-roadmap/` sat outside CX-05's 4-page scope and **reintroduces every conflict CX-05 was meant to kill.** Because Google and AI answer engines penalize cross-page self-contradiction, one unfixed page undercuts the four that were fixed. Verified still-live on the roadmap page:

- median `$250K` / `$246,538` (stale-low) → should be **~$274K (MLS May 2026)**
- property tax **"2.2–2.5%"** (11 refs) → should be **"roughly 2%, verify parcel at Bell CAD"**
- **"125+ accredited residency and fellowship programs"** → should be **"30+ accredited programs (verify on bswhealth.com)"** — "125+" wrongly conflates the VA's 125 affiliation agreements
- **"8,884 employees"** → soften to **"one of Bell County's largest employers"** unless BSW-confirmed
- hardcoded mortgage rate language (6–7% range) → date-stamp "(~6.5%, May 2026)" or remove
- Buy-or-Rent section → align to the residency-length rule

**Recommended:** a bounded **"CX-05b"** Codex job using the same guardrails as CX-05 (reversible/backup first, preview before publish, loan language category-level + Equal Housing, "agent" not "broker", skip-and-report any string not found, loan edits get Taylor's eyes first). Source of truth = `page-reconciliation-and-ctr-fixes.md` §1 canonical table.

---

## Internal-link matrix (live, 2026-05-29 — rows link OUT to columns)

```
from \ to     MD    HUB   CHILD COMMUTE  PHYS  ROADMAP
MD             —     2     0     1        2     0
HUB            0     —     3     6        4     3
CHILD          0     4     —     2        0     0
COMMUTE        0     5     0     —        0     0
PHYS           1     3     0     0        —     0
ROADMAP        0     3     0     0        0     —
```

### Hub-and-spoke gaps to close
- **HUB → Match Day = 0** — the hub links to commute, childcare, physician, and roadmap, but **not** the Match Day page. Add it (the reconciliation spec requires all spokes linked from the hub).
- **COMMUTE → PHYS = 0** — commute is a strong page (pos 6.4); linking it to the buried physician page passes real authority.
- **CHILD → PHYS = 0** — add a contextual physician-loan link.
- Optional: MD → CHILD, COMMUTE → CHILD for tighter spoke cross-linking.
- Inbound to MD is thin (only PHYS→MD = 1) but MD already ranks well (5.12% CTR), so this is low priority.

---

## What is already DONE (don't redo)
✅ Match Day date · ✅ Match Day canonical · ✅ Physician title/meta + inbound links + Equal Housing · ✅ median/tax/loan-language on MD/HUB/CHILD/PHYS · ✅ 3 cannibalizing slugs 301'd to the commute page. Rollback backup: `codex-jobs/agentfire-backups/cx-05-20260528-223946/prechange-backup.json`.

## Separate, larger page-data note (not a CX-05 item)
Per-neighborhood numbers on the COMMUTE and CHILD pages (Lake Pointe, Wyndham Hill, Bella Terra, Prairie Ridge, Hills of Westwood, Canyon Creek) were never reconciled — that's why social copy stays at the general/campus level and avoids per-neighborhood prices/minutes. Reconciling those tables is a deeper page-data task to route via `/temple-seo`, not part of this checklist.
