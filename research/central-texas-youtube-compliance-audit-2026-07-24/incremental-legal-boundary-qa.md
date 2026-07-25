# Incremental legal-boundary and deduplication QA

**Checked:** 2026-07-24  
**Scope:** Provisional `final-findings.csv` only; no evidence files, findings CSVs, scripts, or report content were edited. The file read for this QA contains **115** rows (rather than the stated 114), including the subsequently integrated `ROOTB-RHEA-01` row.

> **Resolution note:** After this QA, `S-AUTH-01` was corrected to 11 canonical watch URLs positionally matching its 11 video IDs, and `S-AUTH-02` was corrected to two canonical watch URLs matching its two duplicate-upload IDs. `build-final-findings.mjs` now fails if any future video-ID/watch-URL count or positional mapping disagrees. The publication gate identified below is therefore resolved, subject to the final rebuild and validation pass.

## Findings and required dispositions

| Priority | Exact finding ID(s) | Recommended disposition | Basis / legal-boundary effect |
|---|---|---|---|
| P0 | `S-AUTH-01` | **Correct and re-map before publication. Retain the substantive group, but do not rely on its individual quotations until each is re-traceable.** | The row has 11 video IDs but 8 URLs. After the fifth item, its positional URL-to-ID mapping is shifted: `Ey6hxvjPaZQ` is paired with the `JOooF3rH33U` URL, later entries are likewise offset, and `3GYggDnQ6pE` / `zIYA3bxI_nI` have no URL. This is a provenance defect, not evidence of a legal violation. Rebuild canonical `youtube.com/watch?v=<ID>` links and re-associate every excerpt/timestamp. |
| P1 | `S-AUTH-02` | **Correct before publication. Retain pending canonical re-mapping.** | The row lists `KviQyVloxXU; fFxMhIMkgq4`, but supplies only the URL for `KviQyVloxXU`. Add the canonical URL for `fFxMhIMkgq4` and associate the quoted evidence with its actual video before relying on the group. |
| P1 | `P-02` | **Remove from active findings/totals; retain only in the resolved QA ledger.** | The current final treatment says the direct PRC disclosure-path check resolved the concern. It should not be presented as an active compliance concern or counted in active findings. |
| P1 | `V-01; V-03; V-02; PF-06; BPM-05; PF-12; LB-03; DL-04; DL-01; RL-04; DL-02; DL-06` | **Keep as `verification_only` and exclude from active issue counts, rankings, and legal-risk language.** | Their current classifications are appropriately limited; the presentation must preserve that limit. They identify a missing video/frame, linked-page, relationship, price, or claim-context check—not a demonstrated violation. |
| P1 | `BG-03` | **Split in presentation: retain the direct “family-oriented” wording as high-priority copy remediation; move retiree / empty-nester / senior-center material to low optional copy cleanup.** | Age-oriented language is not, by itself, an FHA/HOPA violation or a protected-class advertising conclusion. The only high-priority component is the direct familial-status wording. Do not present the age material as part of a high legal finding. |
| P1 | `A-10; A-11; PF-01; PF-09; SH-04` | **Keep direct family-suitability wording as copy remediation; separate school, crime, and safety statements into medium source/neutrality review.** | Schools, crime, and safety claims alone do not establish steering or an FHA violation. `SH-04` particularly mixes direct family language with school/crime/safety claims. The high-priority display should quote only the direct family-suitability wording, with the remaining claims treated as independently qualified source/neutral-review items. |
| P2 | `A-06; A-08; A-09; BPM-04; DL-03` | **Keep only as low optional cleanup; do not characterize military or age references as protected-class violations.** | Military/veteran status and age are not FHA protected classes. Where a phrase also independently targets families, only that independently supported familial-status wording should be elevated. |
| P2 | `C-01; J-03; BPM-07; RL-05` | **Keep only in an optional cleanup appendix, if retained at all.** | These are subjective puffery / broad value language, not substantiated legal or advertising violations on the current record. They should not affect compliance-risk totals or headline conclusions. |
| Pass — no merge | `BG-02` / `BG-03`; `ROOTA-H-03` / `ROOTA-H-04`; `LB-02` / `LB-03`; `LB-05` / `LB-09` | **Do not merge. Cross-link only if the final report benefits from it.** | Each pair shares a video ID but addresses a distinct statement and rule path (for example, family wording versus school source review, or family wording versus rate/loan framing). No improperly duplicated substantive finding was identified. |
| Pass — legal boundary | `ROOTB-RHEA-01` | **Retain as medium FTC disclosure-placement / material-connection verification; do not describe it as an FTC violation.** | The record supports reviewing affiliate relationship disclosure and in-video placement. Caption evidence cannot establish that an unseen visual disclosure was absent. Rheajane Taylor is not Taylor Dasch. |

## Boundary review result

No active row reviewed makes an adjudicated conclusion that a creator **violated** FHA, TREC, RESPA, Regulation Z, or FTC rules. The high and medium treatments consistently use conditional language such as copy remediation, source/assumptions review, disclosure verification, or “not a legal conclusion.” That boundary should be retained in any narrative summary:

- Direct family/children suitability wording can support high-priority copy remediation without asserting intent, exclusion, or liability.
- School, crime, and safety content warrants sourcing and neutral-presentation review unless there is independently supported protected-class tailoring or avoidance language.
- Rate, lender, incentive, and loan content requires frame/lender/assumption review; the present evidence does not establish a Regulation Z conclusion.
- Affiliate material connection and compensation disclosures warrant placement/relationship verification; captions cannot prove what was or was not displayed in the video.
- No RESPA conclusion should be drawn without evidence of a thing of value, referral arrangement, and the other required elements.

## Integrity, creator, and publication checks

- **Master coverage:** all 84 rows in `master-findings-adjudicated.csv` are represented in the provisional final index.
- **Current status mix:** 52 high, 41 medium, 9 low, 12 verification-only, and 1 resolved. Active reporting should exclude the 12 verification-only rows, `P-02`, and low optional-cleanup rows from compliance-risk totals.
- **Taylor-content check:** no final-row creator/channel, title, URL, ID, or excerpt matched Taylor Dasch, `dealswithdasch`, `templetxhomes`, or Living in Temple with Taylor. The similar surname in `ROOTB-RHEA-01` is a different creator.
- **Non-public check:** among the 104 final video references that mapped to currently retained raw metadata, none was private or unlisted.
- **Date check:** no mismatch was found between a final-row date and currently mapped raw video metadata.
- **URL/ID check:** the only material mapping failures found were `S-AUTH-01` and `S-AUTH-02` above.
- **Deduplication check:** no duplicate substantive group was found. The four shared-video-ID pairs above are topic-separable; the remaining excerpt-overlap scan did not reveal a merge candidate.

## Residual verification gaps

Of 155 final video references (151 unique video IDs), 104 could be matched to retained raw metadata. The remaining **51 references** are supported by the legacy source artifacts but lack a current raw `.info.json` capture in this audit tree. Their public availability and date therefore could not be independently revalidated in this QA. Re-capture or open those canonical URLs before external publication, especially where a group combines multiple video IDs or dates.

Seventeen profile/channel references also do not have comparable raw video metadata. Direct disclosure-path or profile-link assertions should continue to be presented as the result of a recorded browser/frame check, not inferred from a channel identifier alone.

## Publish gate

Do not publish active-risk totals or individual evidence excerpts until `S-AUTH-01` and `S-AUTH-02` are re-mapped. When the final report is assembled, segregate resolved, verification-only, and low optional-cleanup material from active high/medium findings and preserve the qualified legal language above.
