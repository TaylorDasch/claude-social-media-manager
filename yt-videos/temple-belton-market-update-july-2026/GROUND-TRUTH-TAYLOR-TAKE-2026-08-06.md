# Ground Truth — Taylor’s Showing Take

**Captured:** 2026-08-06

**Use:** August desk refresh of the Temple–Belton listing-age video
**Provenance:** `[OBSERVATION — Taylor, buyer showings]`

## Taylor’s observation

Taylor reports that older listings often sit because the photography is weak or
the property started above the price buyers support. When the listing media
fails to show something important, it is often a smaller condition clue found in
person: a settling crack, an older roof, or similar deferred-maintenance detail.

This is firsthand showing experience. It is not a measured MLS claim.

## Remarks check

The current source was filtered to Temple and Belton listings with:

- `Status = Active`
- `PropertyType = Residential`
- `DOM >= 61`

The filtered set contained 355 Temple records and 133 Belton records. The
project’s `scripts/listing-remarks-scan.py` review found prose examples that
explicitly referenced roof age or repair, foundation work or settling, as-is
terms, and other repair needs.

Safe conclusion:

- condition and major-system questions belong in the investigation;
- the remarks do not prove that condition caused the extended market time;
- the remarks cannot verify weak photography or what a photo failed to show;
- no remark count should be presented as a cause-of-DOM statistic.

## Safe on-camera wording

> Here’s something I see in person—not something this export measures.
> Sometimes the photos are weak, or the price started ahead of the condition.
> Then I walk the house and notice a small clue: a settling crack I want an
> inspector to look at, or an older roof where I want the age and insurability
> verified. That doesn’t prove those things made the house sit. It tells me what
> I need to investigate before I call it negotiating room.

## Guardrails

- A crack is not a foundation diagnosis.
- An older roof is not automatically a failed roof.
- Do not diagnose structure, roof condition, insurance eligibility, or repair
  cost on camera.
- Do not show an identifiable MLS photo or private remark without usage rights.
- Keep the on-screen label visible: `TAYLOR’S SHOWING OBSERVATION · NOT MLS-MEASURED`.

## Sources

- `/Users/taylordasch_1/market-monitor/temple-belton-0-365-2026-08-05.csv`
- `/Users/taylordasch_1/claude-social-media-manager/scripts/listing-remarks-scan.py`
