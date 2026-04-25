# Fact Handling — Source Provenance & Certainty

> Every important number in output should be traceable.
> This file defines how Claude handles data certainty.

---

## Confidence Levels

| Level | Label | Meaning | Usage Rule |
|-------|-------|---------|-----------|
| 1 | VERIFIED | From authoritative source, confirmed within freshness window | Use freely, no annotation needed |
| 2 | DATED | From authoritative source, but older than freshness window | Use with date stamp: "(MLS, Jan 2026)" |
| 3 | ESTIMATED | Calculated or interpolated from verified data | Mark `[ESTIMATED]` in output |
| 4 | UNKNOWN | No source available | Mark `[NEEDS VERIFICATION]` — do not present as fact |
| 5 | BLOCKED | Required data missing, cannot proceed | Mark `[BLOCKED — need X]` — halt that section |

---

## Source Hierarchy

When multiple sources give different numbers, use this precedence:

1. **MLS pull** (date-stamped) — most authoritative for price/DOM/inventory
2. **Bell County CAD** — most authoritative for tax/assessed values
3. **TEMPLE-TX-DATA-VAULT.md** — canonical reference, use if source date within freshness window
4. **social-media-config.json** — business/performance data, Taylor-confirmed
5. **PropStream** — for equity/owner data
6. **Census/ACS** — for population/demographics
7. **DoD/VA** — for BAH rates, military population
8. **Claude's training data** — NEVER use as source. If no other source exists, mark UNKNOWN.

---

## Freshness Windows

| Data Type | Window | Primary Source |
|-----------|--------|---------------|
| Median home price | 90 days | MLS pull → TEMPLE-TX-DATA-VAULT.md |
| Active inventory count | 30 days | MLS pull |
| Days on market (avg) | 30 days | MLS pull |
| Rental rates | 90 days | MLS/Rentometer |
| BAH rates | Jan 1 annual update | DoD BAH calculator |
| Property tax rates | Annual (set by Oct) | Bell County CAD |
| BSW employee count | 180 days | BSW official / news |
| Fort Hood personnel | 180 days | DoD / AUSA |
| Population figures | 365 days | Census/ACS estimate |
| Builder incentives | 30 days | Direct verification only |
| Interest rates | 7 days | Freddie Mac PMMS |
| Taylor's deal count | Updated by Taylor | social-media-config.json |

---

## Conflict Resolution

When a stat appears differently in two sources:

1. **Check dates.** The more recent verified source wins.
2. **Check specificity.** "Temple 76502 median" beats "Temple median" beats "Bell County median."
3. **Check source authority.** MLS > Zillow > Redfin > training data.
4. **If still unclear:** Use the more conservative number and flag: `[Sourced from X — verify against Y]`.
5. **Never average two conflicting sources.** Pick one and cite it.

---

## Qualitative Claims

For non-numeric claims (e.g., "Temple has a small-town feel"):
- Acceptable if Taylor has said it in recorded content (BP posts, YT transcripts)
- Acceptable if it describes firsthand observation
- NOT acceptable if it's a generic descriptor that could apply to any town
- Must be specific: "Temple still has that 'wave at strangers' energy" > "Temple is a great place to live"

---

## How to Handle Missing Data

| Situation | Action |
|-----------|--------|
| Stat needed but not in TEMPLE-TX-DATA-VAULT.md | Check MLS CSVs in data/. If not there, mark [NEEDS VERIFICATION] |
| Number exists but is older than freshness window | Use it with date annotation: "($247K median, MLS Dec 2025)" |
| Number exists in config but contradicts MLS data | MLS wins. Flag conflict for Taylor. |
| Financial calculation needed | Compute it. Show formula. Never estimate cap rates or cash flow. |
| Competitor data needed | Mark [NEEDS LOOKUP] — do not fabricate competitor stats |
| National comparison needed | Only use if from verifiable source with date. No "national average" without citation. |
| Year-over-year change needed | Both endpoints must be verified. Never compute YoY from one data point. |

---

## Data Vault Update Protocol

When TEMPLE-TX-DATA-VAULT.md is refreshed:
1. Update the `last_verified` date at the top of the file
2. Note which sections were updated
3. Flag any number that changed by >10% — these need downstream content updates
4. Run freshness scanner to identify content using the old numbers
