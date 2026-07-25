# Pre-final adversarial legal-language QA

**QA date:** 2026-07-24  
**Scope:** `final-report-reconciled-draft.md`, `final-findings.csv`, and every current `supplemental-*.csv`. This is a read-only adversarial screen; it does not alter the final report or findings.

## Findings first

### Resolved P1 — `ROOTB-W-01` provenance is now exact

The patched `ROOTB-W-01` location field names all eight raw metadata artifacts in URL/ID order, with no wildcard:

- `20241012_zYAdcRcWozw.info.json`
- `20241013_MCxuCPkuw-4.info.json`
- `20241014_--1tAH-ums0.info.json`
- `20241016_rCneXuyAotM.info.json`
- `20241017_K5Pptrq66PE.info.json`
- `20241018_AV27XoaPV5g.info.json`
- `20241021_SeaD_IZk9tg.info.json`
- `20260427_DCeb2udl3Bs.info.json`, plus its cited caption path/timestamp.

All eight files exist in `raw/authenticated-root/UCKC2Qfjps_rzW0-lUQIP7KA`, each maps to the corresponding positional video ID, and the aggregate `final-findings.csv` `ROOTB-W-01` row carries the same exact provenance. No classification change is needed.

### No other adversarial defect found

The remaining checks pass:

- The reconciled draft consistently says the audit records apparent concerns and verification items, not adjudicated violations.
- Age-oriented language and military/PCS/VA references are explicitly not treated as FHA/TREC protected-class conclusions. Familial-status review is limited to distinct family/children suitability wording.
- Builder, lender, affiliate, and title references are not treated as RESPA findings without a thing of value, agreement/understanding, referral, and covered-service evidence.
- The one affiliate row, `ROOTB-RHEA-01`, is framed as a potential material-connection disclosure-path review; it does not infer an FTC violation and records the missing visual/relationship facts.
- Rate, APR, payment, and down-payment rows are framed as lender/frame/material-terms verification; they do not infer a Regulation Z breach without the complete final ad, advertiser role, trigger terms, and prominence/proximity evidence.
- Historical listing titles are expressly not characterized as stale, unauthorized, or privacy-invasive from age/title alone.
- Strict date parsing found no explicit ISO date outside 2024-07-24 through 2026-07-24 in `final-findings.csv` or the supplemental CSVs. Current-profile rows are verification-only profile observations rather than dated uploads.
- The repeated video IDs in final findings resolve either to expected aggregate/source duplication or to distinct issues on the same video (for example `ZKlf6dyDImI`, `Oe_oexTKVB0`, and `MCxuCPkuw-4`); none is a duplicate substantive group requiring a merge.
- No nonpublic/profile-only `NA_` artifact was found in an A finding row; the final report’s cited public items use public YouTube URLs.

## Publication gate

**PASS.**

The only pending provenance issue was corrected exactly. The adversarial legal-language QA supports final publication without a new finding, severity change, or more conclusive legal wording.
