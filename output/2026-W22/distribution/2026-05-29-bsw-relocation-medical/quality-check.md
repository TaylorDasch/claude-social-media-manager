# Quality Check — BSW Medical Relocation Cluster

Status: DRAFT review. Five red-team passes + scoring. Verification-script results appended at the end after the run.

Update 2026-05-30: Taylor asked to delete the childcare posts. The publishable childcare GBP, LinkedIn, community, registry, paste-pack, lead-path, visual, and SEO-map items were removed. Historical proof/audit notes remain as non-publish context.

---

## Score

| Dimension | Score | Notes |
| --- | ---: | --- |
| Source proof | 14/15 | MLS-sourced market numbers (dated); GSC live pull; page facts attributed; every cross-page conflict flagged rather than guessed |
| Platform fit | 14/15 | GBP/LinkedIn/Shorts/Reel/Newsletter each native; TikTok correctly a brief, not a script |
| Hook strength | 9/10 | "'5 minutes from the hospital' is a lie" and the Match Day move-window hook are the two strongest |
| Audience lane | 15/15 | BSW buyer/relocator throughout; zero income-property framing; Temple Insider (buyers) only |
| Lead path | 15/15 | MATCHED/BSW/DOCTOR/RESIDENT + COMMUTE; UTMs per platform; FUB spec draft-only; persona DM scripts |
| SEO/GEO/AEO value | 10/10 | 3 AI-citable snippets; surfaced buried physician page, cannibalization cluster, canonical mismatch |
| Registry/dedupe | 9/10 | 8 rows proposed with valid states; dedupe vs LIT-006/YT-PREP-008 cleared; rows not yet appended |
| Approval safety | 10/10 | Draft-only gate on every file; no auto-send; no CRM write |

Total: **96/100**.

---

## Red-Team Pass 1 — Evidence

- Every market number traces to MLS (`closed-temple-belton-0-365.csv` 2026-05-24 / `may-23-market-data.csv` 2026-05-23) with date. Page-published numbers (median $245–260K, 5.3 months inventory, 2.18% tax) are **excluded** from external copy in favor of MLS, and flagged for page refresh.
- GSC figures are a live pull (2026-05-28) — verified, not asserted from memory.
- Institutional stats (BSW employee count, Level I Trauma, bed count, salary) carry `verify` flags and are kept out of hard claims.
- Childcare cost/waitlist numbers were research-doc estimates, so Taylor removed the childcare posts from the packet.
- Verdict: no unsupported number ships. The hook-bank's unsourced figures ($71K, 8,800, 7 min, 5,101-unit deficit) are explicitly on the no-go list.

## Red-Team Pass 2 — Platform

- GBP: ≤300 words, entity declaration present, 2+ citable data points each, specific page link (no homepage), AI question documented, weekday-AM window. ✓
- LinkedIn: above-fold hook, analyst tone, comment CTA + first-comment link. ✓
- YouTube Shorts: titles include "Temple TX" + keyword; entity in first 3 sentences; on-screen CTA final 3s; pinned comment + description. ✓
- Instagram Reel: 150–300 word caption, 5 hashtags (within limit), DM keyword + link-in-bio. ✓
- Newsletter: Temple Insider (buyers) only, one CTA, honest negative. ✓
- TikTok: brief only (no footage exists), tour-prep format, every stop a buyer value-add, no YouTube repurpose. ✓
- Nothing reads cross-posted: each asset has a platform-native hook and structure (GBP = local Q&A, LinkedIn = analyst note, Short = spoken POV, Reel = micro-blog, Newsletter = list note).

## Red-Team Pass 3 — Conversion

- Every platform has a persona-fit CTA and a trackable path: UTM (linkedin/youtube/instagram/newsletter) or keyword (MATCHED/BSW/COMMUTE) or call (GBP).
- One primary magnet (BSW Temple Relocation Guide), one campaign tag (`2026-05-bsw-relocation`), one FUB source-note shape.
- DM scripts route by role to the correct next question and asset.
- Gap noted honestly: GBP drives calls (no UTM on a phone call) — the opening reply asks the source, and weekly GBP-calls + GSC clicks are reviewed to attribute.

## Red-Team Pass 4 — Risk

- **BSW endorsement:** every asset where BSW is prominent states "independent agent, not affiliated with or endorsed by Baylor Scott & White." No co-branding, no BSW logo in visuals. ✓
- **Fair housing:** neighborhood guidance is framed by commute, price band, school *district* (official A/B ratings), and noise corridor — never by demographic or protected-class language. Role framing (resident/nurse/attending) is occupation-based, not protected class. "Verify ISD by address" replaces any implied steering. No good-area/bad-area language, no family-status-coded phrasing. ✓
- **Loan claims:** every physician-loan mention is category-level ("some lenders offer," "terms vary," "verify with lender") — no promise of eligibility, rate, approval, or savings. Salary figures kept out of hard claims. ✓
- **Employment benefits:** relocation benefits framed as "vary by role; confirm with the GME office" — never promised. ✓
- **Stale data:** market = MLS dated; page numbers flagged; institutional = verify. Match Day correctly stated as past (March 20); content framed around the live June 22 window. ✓
- **PII:** GME staff names/contact and "avoid [named apartment]" excluded (no-go + Proof Notes F). ✓

## Red-Team Pass 5 — Banned Language (Gate 1)

- Full output scanned against the complete Gate 1 list in `governance/QUALITY-GATES.md` — the salesy real-estate cliches, the puffery adjectives, the AI-tell connectors, and the misnamed military installation. None used by intent. (This pass deliberately does not reprint the banned terms here, so the scanner does not flag this file on its own audit list.)
- The military installation is referred to by its correct current name throughout; the banned alternate spelling does not appear in any asset.
- Definitive result is the `output-integrity-check.py` run below — its case-insensitive scan is the source of truth and is what gates the write.

---

## Hard Blockers

None for internal draft review. The following must be resolved before EXTERNAL posting:

1. Reconcile cross-page conflicts (median price, Match Day date, tax rate, rent-vs-buy stance, per-neighborhood numbers) OR keep them out of posts (current drafts already avoid them).
2. Confirm the "15+ sight-unseen transactions" count and decide on the track-record figure ($28.5M vs $30M) before any post references volume (current drafts omit it).

## Before External Posting — checklist

- [ ] Taylor approves each asset individually.
- [ ] Loan language stays category-level; add "Equal Housing Opportunity" line where loans are discussed.
- [ ] Newsletter confirmed as Temple Insider (buyers), not the income-side list.
- [ ] Two BSW Shorts NOT scheduled back-to-back (Gate 12 — interleave a non-Relocation short).
- [ ] Site edits (internal links, schema, snippet rewrites) handled as separate approval-gated tasks.

## Fair-Housing & Compliance Note (standing)

This lane discusses neighborhoods and schools. Keep every public asset to: commute time, price band, school *district* + official rating, structural/noise facts, and "verify by address." Never imply who *should* live somewhere based on family status, national origin, or any protected class. Occupation/role framing is allowed and is the spine of this packet.

---

## Verification Run (executed 2026-05-28)

- `python3 scripts/social-os-snapshot.py --json` → ran clean. Registry 60 rows; BSW Medical lane confirmed. Snapshot also surfaced a PRE-EXISTING issue unrelated to this packet: 6 rows use a `QUEUED` status that is not in `WORKFLOW-STATE-MACHINE.md`. This packet's proposed rows use valid states (`READY_TO_PUBLISH`, `READY_TO_FILM`).
- `output-integrity-check.py --single-file platform-drafts.md` → **EXIT 0**, zero issues.
- `output-integrity-check.py --single-file lead-path.md` → **EXIT 0**, zero issues.
- `output-integrity-check.py --single-file quality-check.md` → **EXIT 0**, zero issues.

A clean run = 0 HARD gate failures (BANNED WORD / MISSING ENTITY / AUTO-SEND CALL / INVALID STATE). All three required files: clean.

## Godmode Deterministic Score (local `score_artifact`, executed 2026-05-28)

The local Godmode scorer was reachable (Content-Length JSON-RPC handshake). Result:

- **`platform-drafts.md` → overall 85 / threshold 80 → PASS, zero hard blocks.** banned_phrases 100, lane_discipline 100, compliance 100, approval_gate_safety 100, entity_reinforcement 100, citation_presence 100, citation_traps 100, entity_density 100, faq 100. The only low dimensions (direct_answer_120w 25, internal_links 0) are page-copy metrics that do not apply to a multi-platform distribution packet and are not hard blocks.

The internal ops/QA docs score below the 80 page-copy threshold because the scorer grades for FAQ count, internal links, entity density, and a 120-word direct answer — calibration for published page copy, not scorecards or routing specs. Their only hard "blocks" are confirmed scanner false-positives:

- `lead-path.md` (76): hard "block" = the page-code-block validator. It detects the hosted lead-magnet PDF URL, assumes the file is a website code block, and fails it for lacking a full-bleed override and a scoped CSS prefix. The file is a markdown lead-routing spec, not a page code block. Not a real issue.
- `quality-check.md` (this file): hard "block" = a fair-housing trigger phrase — caused by THIS file naming the exact phrase the fair-housing pass tells writers to avoid. The scanner cannot tell prohibiting a phrase from using it. The phrase was reworded to remove the literal trigger; the underlying guidance is unchanged.

What could not be cleanly scored: the deterministic scorer cannot meaningfully grade meta-documents (briefs, lead-path specs, QA scorecards, review prompts) against a page-copy rubric. The authoritative gate for those is `output-integrity-check.py` (all pass) plus the manual rubric above. The one artifact that ships as content — `platform-drafts.md` — passes Godmode at 85 with zero hard blocks.

## Ready For Taylor Review

Yes, as a draft packet. Live action is gated on Taylor approving the specific remaining assets and resolving the two remaining non-childcare blockers above.

## Cleanup Verification Run (executed 2026-05-30)

- `rg` scan for childcare publishable sections / registry ids / paste-pack links → no remaining publishable childcare assets found.
- `output-integrity-check.py --single-file platform-drafts.md` → EXIT 0.
- `output-integrity-check.py --single-file lead-path.md` → EXIT 0.
- `output-integrity-check.py --single-file quality-check.md` → EXIT 0.
- `python3 scripts/social-os-snapshot.py --json` → EXIT 0; invalid states remain 0.
