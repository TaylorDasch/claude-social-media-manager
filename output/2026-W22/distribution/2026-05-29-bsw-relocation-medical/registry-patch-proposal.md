# Registry Patch Proposal — BSW Medical Relocation Cluster

Status: DRAFT PROPOSAL. These rows are NOT written to `data/content-registry.csv`. Append them only after Taylor approves the content. State = `READY_TO_PUBLISH` (written, awaiting publish approval — there is no `DRAFT` state in the state machine; `READY_TO_PUBLISH` is the accurate valid state). Childcare rows were removed at Taylor's request.

---

## Dedupe & Registry Check (Gate 13)

Existing BSW-lane registry entries reviewed for overlap:

| Existing | Title | Overlap risk | Verdict |
| --- | --- | --- | --- |
| LIT-006 | "BSW Temple — Where Doctors and Nurses Actually Live" (video → commute page) | Shares commute page + BSW persona | DISTINCT — this packet is distribution of pages, not a new video; Short 2 angle is "door-to-department gap," not "where they live" |
| YT-PREP-003 | "Physician Loan Temple TX" (video prep) | Shares loan topic | DISTINCT — no loan-promo asset in this packet; loan referenced only as category w/ verify |
| YT-PREP-008 | "BSW Nurses — Every Neighborhood Within 15 Minutes" (queued video) | Shares commute/role angle | DISTINCT but ADJACENT — when filmed, reuse this packet's commute footage; do not duplicate the Short 2 hook |

Hook-bank check: HK-002 and HK-011 (BSW hooks) carry **unsourced numbers** ($71K salary, 8,800 employees, 7 minutes). This packet does NOT reuse those hooks or assert those numbers. No hook collision.

Verdict: **No dedupe block.** Proposed rows use a new dedupe cluster `bsw-relocation-2026-05` to keep this distribution campaign distinct from the `bsw-content` video cluster.

---

## Proposed rows (CSV-ready — append only on approval)

```csv
BSW-DIST-001,"GBP — BSW Match Day Move Window",gbp-bsw-match-day-move-window,Relocation,BSW Medical,gmb,gbp_post,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/match-day-2026-bsw-housing-timeline/,,BSW Relocation Guide,BSW,"Match Day timing; supports highest-CTR BSW page (5.12%)",bsw-relocation-2026-05,
BSW-DIST-003,"GBP — 5 Minutes From BSW Is a Lie",gbp-bsw-commute-reality,Relocation,BSW Medical,gmb,gbp_post,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/neighborhoods-near-bsw-by-commute/,,BSW Relocation Guide,COMMUTE,"Door-to-department gap; commute page pos 6.4",bsw-relocation-2026-05,
BSW-DIST-004,"LinkedIn — BSW Match Day Move Window",li-bsw-match-day-move-window,Relocation,BSW Medical,linkedin,linkedin_post,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/match-day-2026-bsw-housing-timeline/,,BSW Relocation Guide,MATCHED,"Timing + rent-vs-buy length rule",bsw-relocation-2026-05,
BSW-DIST-006,"YT Short — Buy Before BSW Residency Starts",short-bsw-buy-before-residency,Relocation,BSW Medical,youtube,short_script,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/match-day-2026-bsw-housing-timeline/,,BSW Relocation Guide,MATCHED,"Short-form; do not publish back-to-back with BSW-DIST-007",bsw-relocation-2026-05,
BSW-DIST-007,"YT Short — 5 Minutes From BSW Is a Lie",short-bsw-commute-lie,Relocation,BSW Medical,youtube,short_script,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/neighborhoods-near-bsw-by-commute/,,BSW Relocation Guide,BSW,"Short-form; interleave a non-Relocation short before this",bsw-relocation-2026-05,
BSW-DIST-008,"IG Reel — BSW Commute Reality",reel-bsw-commute-reality,Relocation,BSW Medical,instagram,instagram_reel,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/neighborhoods-near-bsw-by-commute/,,BSW Relocation Guide,COMMUTE,"Caption micro-post; pairs with filming brief footage",bsw-relocation-2026-05,
BSW-DIST-009,"Temple Insider — BSW Move Window Block",nl-temple-insider-bsw-move-window,Relocation,BSW Medical,newsletter,newsletter,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_PUBLISH,2026-05-29,,,2026-05-29,/match-day-2026-bsw-housing-timeline/,,BSW Relocation Guide,BSW,"Temple Insider (buyers) ONLY — never Investor Brief",bsw-relocation-2026-05,
BSW-DIST-011,"TikTok Filming Brief — Neighborhoods Near BSW",tiktok-brief-bsw-neighborhoods,Relocation,BSW Medical,tiktok,tiktok_brief,,output/2026-W22/distribution/2026-05-29-bsw-relocation-medical/platform-drafts.md,READY_TO_FILM,2026-05-29,,,2026-05-29,/neighborhoods-near-bsw-by-commute/,,BSW Relocation Guide,BSW,"Brief only — needs on-site footage before any TikTok exists (Gate 14)",bsw-relocation-2026-05,
```

Notes on the rows:
- `BSW-DIST-011` (TikTok) is `READY_TO_FILM`, not `READY_TO_PUBLISH` — there is no TikTok yet, only a filming brief (Gate 14).
- `platform = gmb` is used for GBP rows to match the existing registry convention.
- `source_material_path` points to an existing file, so the integrity check's REGISTRY ORPHAN test passes.
- No row is `content_type = video`, so the "published video needs related_page_slug" check does not apply.
- All states are valid per `WORKFLOW-STATE-MACHINE.md` (`READY_TO_PUBLISH`, `READY_TO_FILM`).

## Optional follow-on registry edits (separate approval)

- Fill `related_page_slug` on `YT-PREP-008` → `/neighborhoods-near-bsw-by-commute/` (currently blank in the `related_video_id` column position — looks misfiled).
- Create one SEO-fix tracking entry for the physician-mortgage page reposition (pos 55.6) and the best-neighborhoods cannibalization consolidation — these are pages tasks, route via `/temple-seo`, not social rows.

## After-publish automation hooks (per project CLAUDE.md)

- On publish of any CRUSH-rated asset here: suggest 3 derivatives + 1 page update.
- Short-form: enforce Gate 12 at schedule time — `BSW-DIST-006` and `BSW-DIST-007` are both Relocation pillar; interleave a non-Relocation short between them.
