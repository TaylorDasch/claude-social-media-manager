# Supplemental root-shard-B C21, Robert Herrings Jr, and Stephen Harris incremental review

**Review date:** 2026-07-24  
**Scope:** Direct review of every public, in-window metadata record and recovered caption artifact in the three authenticated raw roots below. Every recovered upload was in scope regardless of city, property type, or topic. The shared catalog and screen were not rebuilt or amended.

- `raw/authenticated-root/UCZvWg96vLbA3eGHCwnf3RRQ` — Century 21 Premier Realtors
- `raw/authenticated-root/UCGEXUfJdSCBPtgWeF8Dl4lw` — Robert Herrings Jr
- `raw/authenticated-root/UCJs_jBKFIBm0o4HZg1mLMKQ` — Stephen Harris - Selling Central Texas

This is a public-content screen under `compliance-review-matrix.md` and `adjudication-notes.md`, not legal advice, an agency determination, or a conclusion that a person or channel violated a law or rule.

## Coverage and validation ledger

| Channel | Public in-window metadata reviewed | Caption-bearing uploads read | Focused cue videos | New groups |
|---|---:|---:|---:|---:|
| Century 21 Premier Realtors | 690 | 399 | 84 | 1 |
| Robert Herrings Jr | 251 | 35 | 16 | 0 |
| Stephen Harris - Selling Central Texas | 194 | 193 | 62 | 1 |
| **Total** | **1,135** | **627** | **162** | **2** |

The cue pass used direct-family/children suitability, investment-return, material rate/incentive/loan, and explicit crime/avoid/demographic-composition terms to identify records for manual adjudication. A cue is not itself a finding. Empty/music-only captions were retained as coverage limits rather than treated as substantive evidence.

Validation of the CSV passed: it has the exact required 13-column header; both public `watch?v=` URLs positionally match their video IDs; every cited video ID has the cited public raw metadata file; and the pre-integration dedupe check found no matching existing reportable finding ID. The two finding groups are limited to three video artifacts.

## New groups

### ROOTB-C21-01 — Seller-concession, rate-buydown, and assumption terms

- [4411 Secretariat Drive](https://www.youtube.com/watch?v=ZiHCtOvzsWU) — 2024-08-08, `description`, `raw/authenticated-root/UCZvWg96vLbA3eGHCwnf3RRQ/20240808_ZiHCtOvzsWU.info.json`: “$15,000 in SELLER CONCESSIONS!!!! You can use it for closing costs, rate buy downs or any improvements.”
- [109 Kaki Cove](https://www.youtube.com/watch?v=f5w-wHlt2XY) — 2024-12-03, description and `00:00:45-00:00:47`, `raw/authenticated-root/UCZvWg96vLbA3eGHCwnf3RRQ/20241203_f5w-wHlt2XY.info.json` and `raw/authenticated-root/UCZvWg96vLbA3eGHCwnf3RRQ/20241203_f5w-wHlt2XY.en.json3`: “Seller is open to Assumption (VA Loan …)”; captions say “to assumption via loan.”

The two public promotions express material financing/concession possibilities but not the terms needed to assess their current availability or consumer applicability. The CSV correctly treats this as broker/lender verification, not as a Regulation Z, RESPA, VA, or legal-violation conclusion.

### ROOTB-SH-01 — Demographic-composition/deal linkage

- [Texas Housing Market August 2025: These 3 Factors are Having a MASSIVE Impact on Values](https://www.youtube.com/watch?v=xZYC7HfH81o) — 2025-08-10, `00:01:03-00:02:58`, `raw/authenticated-root/UCJs_jBKFIBm0o4HZg1mLMKQ/20250810_xZYC7HfH81o.info.json` and `raw/authenticated-root/UCJs_jBKFIBm0o4HZg1mLMKQ/20250810_xZYC7HfH81o.en.json3`.

The video recounts reports about South Asian immigrants/neighbors and purported “white flight,” rejects racist views, but then describes the related area as a possible source of “really good real estate deals” because people are “running away.” The narrow flag is the protected-class-adjacent demographic-composition/market-opportunity linkage. It is not characterized as a Fair Housing or steering violation; the public record does not establish intent, targeting, or differential treatment.

## Dedupe and rejection ledger

### Century 21 Premier Realtors

- The many direct family/children phrases, including older 5705 Bald Ridge, 906 Northern Dancer, 3041 FM 1113, 2004 Clairidge, 501 Mesquite, and 1770 Dryden variants, were not recreated. They are encompassed by `BPM-01` through `BPM-04`, `ROOT-AUTH-01`, and canonical `S-AUTH-01` family/children groups.
- Commercial/investment-copy cues, including the 1101 W Business 190 duplicate promotions, were not recreated. `S-AUTH-02` is the canonical ROI/outcome group. Generic “investment opportunity,” passive-income, rental, and sweat-equity wording without a separate measurable promise was also not elevated.
- Ordinary references to family gatherings, schools, military/base proximity, price, listing availability, or a future/current listing status were rejected under the matrix. They do not independently establish a familial-status, school/steering, financing, stale-status, or legal finding.

### Robert Herrings Jr

- The 16 cue-bearing records comprise C21 feed variants/previews of the same family/investment listing copy (for example 5705 Bald Ridge, 906 Northern Dancer, 3105 Yaupon, and 4205 Primrose). They add no distinct wording or topic beyond the C21 groups above and existing C21 findings.
- The empty/About-profile observation is already accounted for by `DL-01`; it was not recharacterized as a missing-disclosure violation. All other property-video metadata/captions supplied no independently reportable concern.

### Stephen Harris - Selling Central Texas

- Existing Stephen groups were not recreated: profile/direct-link and NMLS material (`SH-02`); rebate (`SH-01`); family/children (`SH-04`, `ROOT-AUTH-03`); rate/incentive (`SH-05`); seller/statistic and performance claims (`SH-03`, `ROOT-AUTH-05`, `S-AUTH-03`, and `S-AUTH-04`); and the prior school/crime/avoidance pattern (`SH-04`).
- In particular, `lm4O5aKVG14`, `Z-Bzxha-hG0`, and `E4EM8w1O4IY` are canonical `S-AUTH-03`, while `FoqcCQKYqAc`, `1CD8PoAc0C8`, and `CVLV8qWusGQ` are already represented in `ROOT-AUTH-04`, `ROOT-AUTH-03`, and `ROOT-AUTH-05` respectively.
- General loan education, ordinary market commentary, title/description boilerplate, rate discussion without a distinct offer, schools/crime language, and a short clip repeating the anti-racism discussion without the Prosper “deals” linkage were rejected as duplicative, contextual, or insufficient for a separate group.

## Residual limits

The raw captions may be automatic or incomplete, and neither this review nor the CSV determines visual overlays, broker authorization, compensation, listing status, loan availability, lender/servicer approval, underlying market data, or liability. Frame-level review, source documentation, and broker/lender/counsel review remain required before changing or reusing material advertising.
