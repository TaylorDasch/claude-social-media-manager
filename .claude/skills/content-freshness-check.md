# Content Freshness Check

## Trigger
"freshness check", "stale pages", "content refresh", "what needs updating", "audit freshness"

## Required Inputs
- Optional: specific URL or page slug to check
- If no input: runs against all pages in `real-estate-redefined/`

## Step-by-Step Execution

### Step 1 — Scan Pages
1. Run `scripts/freshness-scanner.py` or `scripts/freshness-scanner-v2.py`
2. If script unavailable, manually scan `real-estate-redefined/` HTML files
3. For each page, check:
   - File modification date
   - `dateModified` in schema markup
   - Year references in content (e.g., "2025" when it's 2026)
   - Data references (median prices, BAH rates, tax rates, inventory numbers)
   - Video embeds (are they current?)

### Step 2 — Apply Freshness Windows

| Data Type | Freshness Window | Source |
|-----------|-----------------|--------|
| Median home price | 30 days | MLS data |
| Active inventory count | 14 days | MLS data |
| Days on market | 30 days | MLS data |
| BAH rates | Annual (January) | DoD tables |
| Property tax rates | Annual | Bell County CAD |
| Population/growth stats | 6 months | Census/local data |
| Interest rates | 7 days | Current market |
| Neighborhood descriptions | 90 days | Manual review |
| FAQ answers | 60 days | Verify accuracy |
| Schema markup | On any content update | Auto-update |

### Step 3 — Cross-Reference VIDEO-TO-PAGE-MAP
1. Read `VIDEO-TO-PAGE-MAP.md`
2. For each page: does it have the mapped video embedded?
3. For each video: does the corresponding page exist?
4. Flag any broken mappings

### Step 4 — Check Schema Completeness
For each page, verify presence of:
- [ ] `LocalBusiness` / `RealEstateAgent`
- [ ] `Article` (if blog/neighborhood page)
- [ ] `FAQPage` (if FAQ section exists)
- [ ] `VideoObject` (if video embed exists)
- [ ] `BreadcrumbList`
- [ ] `dateModified` current

### Step 5 — Generate Report

```markdown
# Content Freshness Report — [Date]

## Critical (>90 days stale or wrong data)
| Page | Last Updated | Issues | Priority |
|------|-------------|--------|----------|
| [page] | [date] | [issues] | 🔴 HIGH |

## Warning (60-90 days stale)
| Page | Last Updated | Issues | Priority |
|------|-------------|--------|----------|
| [page] | [date] | [issues] | 🟡 MEDIUM |

## Healthy (<60 days)
[count] pages current

## Video Embed Gaps
| Page | Expected Video | Status |
|------|---------------|--------|
| [page] | [video title] | ❌ Missing |

## Schema Gaps
| Page | Missing Schema Types |
|------|---------------------|
| [page] | [types] |

## Stale Data Patterns Found
| Pattern | Pages Affected | Current Value |
|---------|---------------|---------------|
| "2025 BAH rates" | [pages] | [should be 2026] |
| "median price $XXX" | [pages] | [current: $XXX] |

## Recommended Update Queue
1. [page] — [what to update] — [est. effort: 15m/30m/1h]
2. [page] — [what to update] — [est. effort]
...
```

### Step 6 — Generate Update Drafts (if requested)
For each flagged page, offer to:
- Update stale data references with current numbers
- Add missing video embeds
- Add missing schema markup
- Update dateModified
- Refresh FAQ answers

## Output Format
Save to `output/audits/freshness-scan-YYYY-MM-DD.md`

## Quality Checks
- [ ] All pages in real-estate-redefined/ scanned
- [ ] VIDEO-TO-PAGE-MAP cross-referenced
- [ ] Schema completeness checked per page
- [ ] Stale data patterns identified with correct current values
- [ ] Update queue prioritized by impact
- [ ] All "current values" sourced from data files, not estimated

## Brand Rules
- Use real MLS data for updated values — never estimate
- Flag any number you can't verify as `[VERIFY — need MLS pull]`
- Fort Hood (not Fort Cavazos)
- dateModified should reflect actual content update, not just schema update
