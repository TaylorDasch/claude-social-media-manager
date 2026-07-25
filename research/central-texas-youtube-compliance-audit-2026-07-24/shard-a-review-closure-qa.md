# Shard-A review closure QA

**QA rerun:** 2026-07-24  
**Scope:** Final strict-window reconciliation of the completed shard-A manifest/status ledger, recovered raw artifacts, and the three A review packets. The strict inclusive window is 2024-07-24 through 2026-07-24, calculated from each raw JSON `upload_date`; caption counts are linked only to an included video ID. No review or finding CSV was edited.

## Findings first

### No publication-blocking finding remains

The corrected coverage notes reconcile exactly to strict-window raw evidence:

- The heavy packet reports **873 public uploads** (633 Shelly + 240 i35Group) and **473 captions** (294 + 179). Raw count agrees after excluding i35’s 2024-07-23 metadata/caption artifact.
- The Sujin/Sandee packet reports **415 public uploads** and **216 captions** (Sujin 400/205; Sandee 15/11). Raw count agrees after excluding Sujin’s 2024-07-23 metadata/caption artifact.
- The remaining packet reports **321 public uploads**, **216 captions**, and **four separately identified non-upload/profile artifacts**: Hood Homes Blog, Frank Adams, Alberto Lopez, and Elizabeth Thomas. Raw count agrees.

No row should be merged, downgraded, or removed.

### Coverage reconciliation — pass

The manifest has 42 terminal tab URLs for 21 unique channel IDs: 31 `cutoff_complete`, 8 `no_tab`, and 3 `complete`. Review coverage is exact and non-overlapping:

- Heavy packet: Shelly Salas and i35Group (2).
- Sujin/Sandee packet: Sujin Park Henson and Sandee Payne (2).
- Remaining packet: the other 17 manifest channels.

Completed raw directories contain 1,616 `.info.json` records. Five `NA_*.info.json` records are non-upload channel/profile artifacts (one Shelly artifact plus the four remaining-packet artifacts). Two dated uploads are outside the strict window and excluded from both upload and caption coverage: i35 `vIwCJGhoSCU` (`2024-07-23`) and Sujin `K2szWebEl90` (`2024-07-23`). The resulting strict public in-window inventory is **1,609 uploads**. Packet totals match: 873 heavy + 415 Sujin/Sandee + 321 remaining = 1,609. Caption-to-included-video linkage also matches: 473 + 216 + 216 = **905**.

The seven remaining channels with zero recovered public in-window uploads are explicitly recorded as reviewed-with-zero, not inferred clean.

### Finding-row evidence and mapping — pass

All three CSVs have the exact 13-column schema. They contain 17 finding rows and 54 video-artifact references. Every referenced video ID resolves to a recovered public, in-window raw record; no `NA_` profile artifact appears in a finding row. Every URL is canonical `https://www.youtube.com/watch?v=<id>` and correctly position-maps to its semicolon-positioned video ID.

### Taylor/nonpublic exclusion — pass

The collector’s two excluded Taylor IDs are absent from the shard-A manifest and no finding row references either ID. No nonpublic/profile-only item is used as finding evidence.

### Duplicate screen — pass

No substantive duplicate exists across the three packets, the adjudicated master, or other supplemental review records. The two repeated video IDs inside the A packets are purposefully distinct:

- `ZKlf6dyDImI`: family/school suitability wording versus rate/incentive terms.
- `Oe_oexTKVB0`: familial-status wording versus market-statistic/location recommendation.

`gd8C2EtH98I` is already in the master for a separate profile-path check; its A-packet family wording is a distinct public-copy issue. Aggregate `final-findings.csv` overlap is expected and is not a second incremental source finding.

### Conservative legal posture — pass

The packets use verification/review language rather than violation conclusions. They do not infer a Fair Housing violation from age, military, school, crime, safety, or location language alone; do not infer RESPA without thing-of-value/agreement/referral evidence; do not infer FTC material connection; do not infer Regulation Z failure from a rate alone; do not infer stale status; and distinguish measurable claims from puffery. High priority is limited to direct familial-status suitability wording, while rate/incentive items remain broker/lender material-terms review.

## Publication gate

**PASS — shard-A closure packet is internally reconciled and may proceed to publication.**

Residual limits remain normal audit limits: automated captions and public metadata do not establish visual disclosures, authorization, compensation, current listing status, factual accuracy, intent, or liability. Those limits do not block publication because they are consistently stated in the review packets and classifications.
