# Newsletter program

Taylor Dasch with EG Realty uses this newsletter system for two products. They share one conversational production process, but never share a recipient list.

## 1. The Leverage List

- **Publication:** Temple TX Insider
- **Audience:** buyers with a valid, scope-specific recurring-email permission record
- **Cadence:** every other Tuesday
- **Promise:** roughly five to eight current Temple/Belton homes where documented market signals may give a buyer negotiating room, with estimated payment context and one caution per property
- **Business goal:** give buyers a reason to return while creating private Current Fits conversations without padding the list or promising concessions
- **Authoring template:** `newsletter/issues/leverage-list.template.md`

The Leverage List is the rebrand/successor to the old Central Texas Market Update,
not a new publication, CRM, database, or automation. The old premium market-update
design may be used as a visual reference, but every issue still requires separate
property, audience, subject, content/link, staging, and send approval.

### Recurring issue structure

1. **Short market frame** — only the current context needed to interpret the list.
2. **Roughly five to eight properties** — current facts, estimated payment context,
   negotiation angle, and one caution each; use fewer when fewer qualify.
3. **One practical play** — a concise, assumption-backed buyer strategy.
4. **Private next step** — Current Fits, reply, or another approved buyer action.

On each due week, choose `CODEX/COMPUTER PICK` or `TAYLOR PICK`. Both modes use the
newest current-status MLS source, suppress Issue #1 selections by default, and
require a close-to-send status/facts recheck. Neither mode can publish or send.

## 2. Investor Deal Analysis

- **Publication:** Temple TX Investor Brief
- **Audience:** investors with a valid permission record
- **Cadence:** second and fourth Thursday of each month
- **Promise:** three active Central Texas opportunities screened under explicit assumptions, with the reason to look and the reason to walk
- **Business goal:** create serious underwriting conversations and demonstrate Taylor's ability to source, analyze, and pressure-test deals
- **Approved design:** Investor Desk Brief (`newsletter/design/temple-investor-brief-v1-desk-tech.html`), selected July 19, 2026

The approved design is the default starting point for every investor edition. Preserve its opportunity-scan framing, three-class shortlist, explicit underwriting assumptions, tabular deal metrics, break-point risk treatment, verification checklist, portfolio view, capital-conditions note, rotating investor extra, Taylor desk note, and reply-first CTA. The selection approves the design system only; every issue still requires separate copy, assumptions, recipient, staging, and send approval.

### The three deal classes

1. **Best multifamily** — duplex, triplex, fourplex, or small multifamily.
2. **Best single-family rental** — strongest conventional long-term rental candidate.
3. **Best specialty play** — the best current value-add, flip, mid-term rental, short-term rental, land, or unusual strategy candidate.

"Best" means best among the active listings screened for that edition under the published assumptions. It does not mean guaranteed returns. If a class has no defensible pick, publish **No buy this round** and explain why instead of manufacturing a winner.

### Required analysis for every selected deal

- Active-status verification timestamp
- Price and property class
- Rent, resale, or income assumption and its source
- Financing, tax, insurance, vacancy, management, maintenance, and rehab assumptions as applicable
- Simple return or margin range—not false precision
- Why it ranks first in its class
- The largest underwriting risk
- What Taylor would verify before an offer

For short-term rentals, verify city, deed, HOA, insurance, management, and platform assumptions. For flips, state the rehab, carrying-cost, resale-cost, and ARV assumptions. Never present either strategy as permissible or profitable without the supporting checks.

### Six-edition investor rotation

| Edition | Rotating extra |
|---|---|
| A | One underwriting tip |
| B | Investor or local-operator shoutout, with permission |
| C | Value-add idea with a rough scope and risk |
| D | Financing or rate scenario |
| E | Deal post-mortem: why Taylor passed |
| F | Property-management or tenant-demand observation |

## Operating calendar

| Timing | Product |
|---|---|
| Every other Tuesday | The Leverage List |
| Second Thursday | Investor Deal Analysis |
| Fourth Thursday | Investor Deal Analysis |

Issue #1 of The Leverage List was sent Thursday, August 6, 2026 and must not be
recreated. Issue #2 is targeted for Tuesday, August 18 at 10:00 AM America/Chicago,
subject to final approval. The Investor Brief keeps its separate calendar and
audience. The existing Monday Newsletter Desk workflow coordinates due weeks; do
not create a duplicate reminder.

## Evidence and compliance rules

- `/Users/taylordasch_1/market-monitor/` is the source of truth for MLS pulls.
- Date-stamp every market snapshot and recheck listing status before staging and again before sending.
- Use ranges when assumptions are uncertain and label estimates clearly.
- Do not expose confidential MLS remarks, showing instructions, or private client information.
- Shoutouts and client stories require permission.
- Keep a concise disclaimer on investor editions: information is educational, assumptions vary, and readers should verify financing, taxes, insurance, condition, rents, restrictions, and professional advice.
- One primary CTA per issue. A reply is the preferred conversion event.

## Production conversation

For each edition, Taylor only needs to answer the applicable prompts here:

1. For a Leverage List due week: `CODEX/COMPUTER PICK` or `TAYLOR PICK`?
2. If Taylor Pick: which MLS numbers/addresses or candidate-sheet rows?
3. For an Investor Brief: what strategy or question is timely right now?
4. What approved next action should the reader take, and what must not be mentioned?

Codex then pulls the supporting data, drafts the issue, produces the local preview,
and presents the property/deal set, exact eligible audience, subject, content,
links, and assumptions for approval. Staging and sending remain separate approvals.
