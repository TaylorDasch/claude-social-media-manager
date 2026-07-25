# Evidence integrity cross-check

**Checked:** 2026-07-24, offline only  
**Inputs:** `master-findings-adjudicated.csv`, `final-report-draft.md`, `authenticated-video-catalog.json`, `root-channel-catalog.csv/json`, `search-results.csv/json`, and parseable individual non-authenticated `raw/**/*.info.json` records. Playlist metadata was excluded. This check compares the evidence package as it exists now; it does not decide whether a historical YouTube title was renamed after collection.

## Bottom line

Two **final-report high-priority NMLS examples have a material current title/ID ambiguity**. The report labels point to valid Stephen Harris URLs, but the current root catalog assigns those IDs unrelated titles. The source report also contains a third title/date inconsistency in the same NMLS cluster. Do not silently relabel the examples and assume the description evidence follows: recover the contemporaneous description capture or re-retrieve the live pages before distributing that finding.

The master file also has two date vectors in the wrong ID order. All cited `watch?v=` URLs are syntactically valid and agree with their paired `video_id`; no confirmed Taylor-channel citation was found among inventory-verifiable records. Most other title differences are shortened display titles or possible title changes, not proof of an ID error.

## Coverage and method

| Surface | Result |
|---|---:|
| Master findings rows | 84 |
| Master video references / unique IDs | 85 / 82 |
| Master unique IDs found in available video inventory | 49 |
| Master unique IDs absent from all supplied inventories/raw non-auth `.info.json` | 33 |
| Master channel/profile references | 17 |
| Final report `watch?v=` links / unique IDs | 26 / 26 |
| Final IDs found in supplied inventory | 12 |
| Final IDs absent from supplied inventory | 14 |

An ID was treated as verified only when it appeared in at least one of the listed inventories or a non-authenticated individual `.info.json` record. Search data does not reliably carry upload dates, so date corrections below rely only on records that do. Raw dates in `YYYYMMDD` form were normalized before comparison.

## P0 — final-report examples requiring evidence recovery

The following labels appear in `final-report-draft.md` line 42 and in source finding `SH-02`. Each URL is well-formed and resolves to the listed current inventory ID, but the current catalog title is materially unrelated to the cited label. This could be a title change, a historical collection mismatch, or a source-report link mismatch; the offline package cannot distinguish those explanations.

| Current ID / report URL | Report/source title | Current catalog title and date | Exact safe correction | Confidence |
|---|---|---|---|---|
| `-CpNohOpgaw` / `https://www.youtube.com/watch?v=-CpNohOpgaw` | `Market Update: Why Selling Your Home in Central Texas Is Harder Than Ever` | `You Won’t Believe What $340K Buys in Belton, TX!` — 2025-07-23 | Do **not** use the current title as a substitute for the NMLS evidence. Mark the cited historical title/description as unverified; recover the contemporaneous `.info.json`/description capture or re-retrieve the page before retaining this example. If the current page is the intended evidence, label it with the current title and re-check the NMLS text. | High |
| `18WLFA46NT4` / `https://www.youtube.com/watch?v=18WLFA46NT4` | `Thinking About Moving to Fort Cavazos? Here’s What You Need to Know` (final report uses a shortened form) | `Texas Home Sales CRASH 20% - Austin, Dallas, San Antonio, Houston, Killeen -Temple Housing Report` — 2025-05-06 | Same treatment: hold the example as title/description-ambiguous until the contemporaneous description is recovered or the current page is rechecked. | High |

The third `SH-02` source-only URL has the same issue and should be reconciled with the two final examples before any NMLS conclusion is distributed:

| ID | Source-report title | Current catalog title/date | Required correction | Confidence |
|---|---|---|---|---|
| `z7GOddPjiio` | `Fort Cavazos PCS Guide: 5 Things I Wish I Knew` | `Mortgage Payment Went From $2500 to $7500 A MONTH` — 2024-09-19 | Treat the source title and its asserted two-number description as unverified pending a preserved capture or live recheck. | High |

## Exact date corrections in `master-findings-adjudicated.csv`

These are metadata-order errors, not a conclusion that the underlying speech/description did or did not occur.

| Finding / ID | Master date | Current authoritative date | Correction | Confidence |
|---|---|---|---|---|
| `SH-02` / `-CpNohOpgaw` | 2024-09-20 | 2025-07-23 | Set the first `SH-02` date to `2025-07-23`. | High |
| `SH-02` / `z7GOddPjiio` | 2025-07-23 | 2024-09-19 | Set the third `SH-02` date to `2024-09-19`. The source report says September 20, so preserve a one-day date/timezone note if its original capture is retained. | High for current-catalog date; medium for reconciling the source’s one-day difference |
| `SH-04` / `9rv_Mx_ptug` | 2025-01-25 | 2026-04-19 | Set the first `SH-04` date to `2026-04-19`. | High |
| `SH-04` / `YVThYKqdxW8` | 2026-04-19 | 2026-02-14 | Set the fifth `SH-04` date to `2026-02-14`. | High |

The source report’s narrative puts `QdF070z89d0` at 2025-01-25, but no supplied current inventory record carries an upload date for that ID. Do not present `2026-02-14` (the date currently paired to that third ID in the master row) as verified. Re-fetch its metadata before changing it; the source report is a useful lead, not an independent current-inventory confirmation.

The intended corrected date ordering for `SH-02`, based on current catalog metadata, is:

`2025-07-23; 2025-05-06; 2024-09-19; current About`

The intended `SH-04` ordering is:

`2026-04-19; 2025-12-19; [re-verify QdF070z89d0]; 2026-02-21; 2026-02-14`

## Title variance: not an ID mismatch by itself

Ten of the twelve inventory-verified final-report video examples have the same URL/ID and subject but a shorter report label or a current expanded marketing title. Examples include:

- `uyDO9TayGyE`: report `How Soldiers Build Million-Dollar Portfolios With Their VA Loan`; current catalog appends `| Fort Hood Real Estate Investing`.
- `MtKBGJCzjzM`, `wUTbACQP_iU`, and `eG-Ncxh5B_U`: the report uses short Aundrea Dudik labels; non-auth raw metadata contains longer current titles.
- `dGjB7gjDPHk`: report `Single-Story 4 Bedroom Home Layout Tour`; catalog appends `| Belton Texas`.
- `9rv_Mx_ptug`: report shortens `Harker Heights vs Killeen vs Copperas Cove: Best Place to Live Near Fort Hood?`.

Those are best recorded as title variants/possible title edits. There is no reason in the supplied metadata to replace the IDs or to characterize them as misconduct. If precise archival citation is required, use the exact title from the source capture that supplied the quote, not merely the current catalog title.

At master level, Aundrea and other records show the same short-title pattern. Their IDs, paired URLs, and available channel attribution agree. Rows such as `SH-02` and `SH-04` use a finding-level phrase in `video_title` for multi-video evidence rather than a literal title; that field should not be treated as canonical per-video metadata.

## Verification gaps — no correction asserted

The following final-report IDs are absent from every supplied current inventory and all parseable non-auth individual `.info.json` records. Their URL syntax is valid, but their current title, channel, date, duration, and the claimed timestamp cannot be independently verified from this package:

`XTIn4-nXAZg`, `4knnkLiSO_k`, `biq0haoCeiM`, `MtSaZ_wLYkM`, `mmGVWB_fako`, `U7Cb3fVDSXo`, `nL3hyLo6_hw`, `SEnO3JedXcg`, `uUkY_pvzyxE`, `vo-XdLuZAJo`, `ys6_k7DqvlI`, `Fks5Vr6nQHo`, `83phZrxwie8`, `4yooPsq8qio`.

This is an evidence-coverage limitation, not a finding that any of those links is wrong. Before final publication, collect a current metadata record or preserved contemporaneous record for each high-priority example (`XTIn4-nXAZg`, `4knnkLiSO_k`, `biq0haoCeiM`, `MtSaZ_wLYkM`, and `mmGVWB_fako` are especially prominent in the draft).

## URL, timestamp, and Taylor-channel checks

- **URLs:** All 85 master `watch?v=` references contain a valid 11-character video ID matching the corresponding `video_id` field. All 26 final-report video links have valid matching IDs. The additional final `@PRCPropertiesGroup/about` link is a valid channel/About URL, not a malformed video URL.
- **Timestamps:** For every final-report timestamp whose video has a supplied duration, the cited end time falls within the duration. The same maximum-duration check found no master timestamp that obviously exceeds the duration of all video IDs in its finding row. Timestamp accuracy for the 14 unavailable final examples remains unverified.
- **Taylor exclusion:** None of the 49 inventory-verified master video IDs or 12 inventory-verified final-report IDs has either excluded Taylor channel ID: `UCqrLPGPR9eV7QUfK02dwtpQ` or `UCKuVz8ytHECKEAyRacDpm1g`. The 33 master IDs / 14 final IDs absent from the supplied inventories cannot receive that channel-attribution check; this is a coverage gap, not confirmed contamination.

## Recommended disposition

1. Block distribution of the NMLS row until its three historical title/description pairings are reverified. The current catalog does not support the labels as written.
2. Correct the four high-confidence master dates above, then re-fetch `QdF070z89d0` before finalizing the `SH-04` date vector.
3. Preserve shortened titles as variants when the ID/URL and subject agree; do not convert normal marketing-title differences into a compliance allegation.
4. Add a current or preserved metadata record for each unavailable final-report example before treating its title/date/timestamp attribution as final.

## Main-agent authenticated recheck

After this offline comparison was delivered, the main audit pass completed an
authenticated, current `.info.json` recheck for all three `SH-02` video IDs.
Each current description contains `NMLS 2453024`. The public-number conflict is
therefore supported independently of the obsolete/mismatched source-report
titles. The final report should use the current titles and dates:

| ID | Current authenticated title | Upload date | Description result |
|---|---|---|---|
| `-CpNohOpgaw` | `You Won’t Believe What $340K Buys in Belton, TX!` | 2025-07-23 | Contains `NMLS 2453024` |
| `18WLFA46NT4` | `Texas Home Sales CRASH 20% - Austin, Dallas, San Antonio, Houston, Killeen -Temple Housing Report` | 2025-05-06 | Contains `NMLS 2453024` |
| `z7GOddPjiio` | `Mortgage Payment Went From $2500 to $7500 A MONTH` | 2024-09-20 | Contains `NMLS 2453024` |

The same authenticated recheck supplies the complete `SH-04` date vector:
`2026-04-19; 2025-12-19; 2025-01-25; 2026-02-21; 2026-02-14`.
This resolves the earlier `QdF070z89d0` coverage gap. These rechecks resolve the
distribution blocks in recommendations 1 and 2, provided the final report uses
the corrected titles/date order and retains the ordinary caveat that the audit
does not establish which NMLS number is correct.
