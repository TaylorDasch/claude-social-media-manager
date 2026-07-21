# Critique and Revision Record

## Critical failure found during data audit

The first analysis treated every blank-CloseDate row as live inventory. That blended active, contract/pending, and another open group. An interim block-based correction improved the denominator but still lacked explicit current status and property-type fields.

### Fix implemented

- Replaced the field-incomplete current source with the July 20 export containing explicit `Status` and `PropertyType`.
- Filtered `Residential` + `Status = Active`, then post-filtered the multi-city export to Temple/Belton: 870 rows / 869 unique addresses.
- Cleared the current Active-data filming gate while preserving the May-status continuity caveat.
- Updated regression coverage.
- Rebuilt active price, DOM, price-cut, price-band, and builder metrics.

## Hook critique

The initial `lower closed DOM / 54% cut` system was understandable but repeated the May premise. Grouping explicit Active Residential records by DOM confirmed the more buyer-useful `14% / 45% / 67% / 81%` staircase.

### Fix implemented

- Promoted the listing-age staircase to title, thumbnail, hook, script spine, graphics, and derivatives.
- Kept `83→50` as the early counterpoint that prevents blanket lowball advice.
- Added cross-sectional/survivorship caveat without front-loading method.

## Builder critique

The first build used `BuilderName` as a fallback and produced a 37.1% builder share. Builder metadata can persist on resales.

### Fix implemented

- Builder now means `SpecialListingConditions contains Builder` only.
- Correct current Active share: 222/870 = 25.5%.
- Correct median active DOM: 110 builder vs 64 non-builder.
- May-to-July builder trend removed because the May source lacks a reliable classifier.

## Closed-data critique

A $1,900 Temple lease row appears in the closing block and can inflate n by one.

### Fix implemented

- Retained a $25,000 sale-record floor.
- Latest qualifying combined close count remains 200; median close is $278,670, median DOM is 50, and median close-to-final-list is 99.76%.

## Independent red-team findings accepted

- Replaced deterministic `Your Offer Changes After Day 60` language with `The 60-Day Listing Test`.
- Replaced an unlabeled arrow thumbnail with `14% vs 81%` and mandatory endpoint labels, avoiding a longitudinal implication.
- Rewrote the opening to name the exact `0–30`, `61–90`, and `91+` groups and say explicitly that age is not automatic permission to offer less.
- Replaced every unsupported sales-speed formulation with `33-day lower median DOM in this sample` language.
- Compressed the repeated early staircase explanation and synchronized the timing map.
- Added Central Texas MLS and covered-period attribution to public graphics and derivative copy.
- Added dedicated two-period notices for the May–July Active continuity graphic and the April/May-versus-June/July Closed-sample graphic.
- Replaced `Why closed-listing median DOM fell` with `The 83 vs 50 closing-sample guardrail` so chapter copy does not imply a marketwide speed trend.
- Changed the CTA to a concrete Calendly action.
- Advanced status to `READY_TO_FILM`: the current export includes explicit Status/Property Type fields, and the multi-city Temple/Belton post-filter is documented. Taylor approval is still required before filming, upload, or publication.
