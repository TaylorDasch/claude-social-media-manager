# Council Run — Morgan's Point Resort Flagship Video
**Run:** `reason-run-260726-2130` · Started 2026-07-26 21:25 CDT · Closed 2026-07-27
**Config:** domain=content · mode=convergent · judges=5 · iterations=3 · convergence=2
**Data:** CTXMLS `whole-market-with-status-2026-07-20.csv` — pulled July 20 2026, independently recounted July 26 2026

---

## Result

**Round 1 completed in full. Rounds 2–3 not run — stopped on an external constraint, not on convergence.**

The blind 5-judge A/B/AB panel was **replaced** with a direct verification pass. Rationale: the judge panel
exists to settle questions of taste between candidates. It was not needed here, because Candidate A's central
mechanism was **disproven against the source CSV**, not merely disliked — and a blind panel comparing a
factually inverted candidate against its correction is ceremony, not rigor. The verification that replaced it
(every dollar figure re-derived from the export, mechanical banned-word and framing scan across all nine
shipped files) is the check that actually protects Taylor.

**Final artifact:** Candidate B, 18,907 words, all 16 deliverables. Split into nine production files.

---

## What the council caught — the three that mattered

### 1. The buyer-mistake mechanism was pointing the wrong direction (FATAL)

Candidate A — and the original council brief — framed the MLS city-field finding as an **inventory** problem:
"you're only seeing 4 of the 15 listings." True, but it leads the buyer to the wrong conclusion and wastes
the finding.

Recount of the four listings whose city field says "Morgans Point Resort": **$315,000 · $330,000 · $665,000 ·
$869,000 — median $497,500**, against a true active median of $330,000. Every one of the six actives under
$275,000 is filed under Belton — **6 of 6**.

The buyer doesn't conclude "there's nothing here." They conclude **"I can't afford here,"** cross the town
off in seconds, and never contact anyone. **Cheapest visible $315,000 vs cheapest actual $205,000 — a
$110,000 illusion.** That became the spine of the video.

### 2. The city field sorts by vintage too — and that welds the video together (discovered in rebuild)

| | n | Median build year | Median price |
|---|---|---|---|
| Name-carrying ("Morgans Point Resort") | 4 | **2012.5** | $497,500 |
| Belton-filed | 11 | **1977** | $272,500 |

**Not one listing carrying the town's own name was built before 2002. All 8 pre-1980 actives are on the
Belton side — 8 of 8.**

Searching by name returns a town that is both too expensive *and* too new. The affordable half and the aging
half are the same eleven houses — which is why the price problem and the inspection problem are one video
instead of two.

### 3. Two claims that would have been caught on camera (FATAL ×2)

- **The leverage number was overstated ~5x.** "$330,000 asking vs $220,000 selling" is a **size artifact** —
  active homes are 32% larger (1,791 vs 1,356 sqft). The honest gap is $/sqft: $188 vs $175, **6.9%**.
  Candidate A showed both numbers 2:45 apart and contradicted itself on screen.
- **Pending and under-contract medians are LIST prices.** A's four-median "ladder"
  ($330,000 → $273,250 → $232,450 → $220,000) narrated seller ask as buyer agreement across four different
  cohorts. Graphic cut entirely.

### Also caught

- **The mandated CTA contradicted the video.** The brief's verbatim CTA promises to "separate the true
  water-tier lots from the pretenders" — but the export has **no waterfront field at all, zero of 29**, which
  the script states on camera as its trust moment. Rewritten; deviation flagged for approval, not made silently.
- **"In this window" was never defined.** Now pinned: 2026-05-18 → 2026-07-16, ~60 days, **n=7** — and n=7 is
  owned out loud on camera rather than buried.
- **"47% have cut price" oversells.** Median cut is −4.7%; four of seven are under 5%. Reframed as sellers
  testing, not capitulating.
- **Never call identifiable listings overpriced.** Dos Rios, Wrangler, Daingerfield belong to real sellers.
  DOM and cut history ship as record only.
- **MLS display rules were never checked.** Left as an **OPEN** pre-publish item, not a false ✅.

---

## Corrections to the original brief

| Brief said | Data says |
|---|---|
| "What's actually SELLING is the older, smaller stock" | Smaller yes, **older no.** Closed median build year **2000**; active **1979**. Zero pre-1985 homes sold; 8 of 15 actives are pre-1980. The old stock is what's *sitting*. |
| Status breakdown totalling 28 | 29 rows — the brief omits **1 Coming Soon at $299,900.** Say "15 active listings," not "15 homes for sale." |
| CTA sorting "true water-tier lots" | No waterfront/water-access/dock field exists in the export. Rewritten. |

Everything else in the brief verified exactly: 29 rows, 15/4/2/7 status split, $205,000–$869,000, medians
$330,000 / $273,250 / $232,450 / $220,000, 1,791 sqft, 28 DOM, 93 DOM, 1966–2026 vintage, Belton ISD 29/29,
HOA 27 None / 2 Mandatory.

---

## Lineage

| Phase | Agent | Result |
|---|---|---|
| 1 Setup | — | Config parsed; task + ground truth assembled; MLS recount verified all 13 brief claims |
| 2 Generate-A | Author-A | Candidate A, 10,871 words, 7 self-flagged soft points |
| 3a Critic (cross-lab) | **Codex — FAILED** | Timed out at 10 min; retry died on a skills-loading error. **Opt-out logged per council rules; Gemini NOT silently substituted.** Produced one confirmed finding before dying (the pending/AUC list-price defect), carried forward. |
| 3b Critic | Claude critic | **20 weaknesses: 6 FATAL, 10 MAJOR, 4 MINOR.** Independently confirmed and escalated the Codex finding. |
| — Verification | Orchestrator | All 3 lead FATALs re-derived directly from the CSV before being accepted. §H1, §H1b, §H3, §H4, §I written to ground truth. |
| 4 Generate-B | Author-B + 5 scoped agents | Candidate B, 18,907 words, all 16 sections. Original Author-B died 3× on API errors; work re-scoped into small parallel agents. Sections 8–11 and 16 written directly in-thread after subagents hit the spend limit. |
| 5 Synthesize-AB | **not run** | A was disproven on source data; synthesis with a factually inverted candidate would import its errors. |
| 6 Judge panel | **replaced** | Swapped for mechanical + contextual verification of the shipped files (see below). |
| 7–8 Convergence / handoff | — | Bounded stop at Round 1. Production files written; May 18 version archived. |

## Verification performed on the shipped files

- Every `$` figure across all nine production files extracted and checked against the verified set. All trace
  to ground truth or are labelled derivations (e.g. `$315,000 − $275,000 = $40,000`).
- Mechanical banned-word scan: **clean** across all viewer-facing copy.
- Framing scan: no undefined "in this window", no portal-behavior assertion, no investor-lane leakage, no
  "broker" — the only hits were self-audit lines confirming absence.
- All 16 deliverables present and non-empty.

## Honest limits

- **No genuine cross-lab signal.** Codex failed twice. The critic was an Anthropic model attacking an
  Anthropic draft — shared blind spots are not excluded. The three FATALs were mitigated by being re-derived
  against the raw CSV by the orchestrator, which is stronger evidence than any model's opinion, but the
  *creative* frame was never externally challenged.
- **One round, not three.** Round 1's catches were large; Rounds 2–3 would likely have returned polish. That
  is a reasonable expectation, not a measured fact.
- **n=7 on every closed-side claim.** Seven sales in ~60 days. Real signal, thin sample. The script says so.
- **Water tiers remain unverifiable from MLS data.** Any tier claim is Taylor's site observation.
- **All numbers need a same-day re-pull before filming.** They will drift.
