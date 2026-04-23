# Internal Link Graph Audit

## Trigger
"internal link audit", "link graph", "orphan pages", "internal linking", "hub and spoke"

## Required Inputs
- None required — scans all HTML files in `real-estate-redefined/`
- Optional: specific page to audit for outgoing/incoming links

## Step-by-Step Execution

### Step 1 — Build Link Inventory
1. Scan all HTML files in `real-estate-redefined/` (Complete/ and active builds)
2. For each page, extract:
   - Page slug (from filename)
   - All `<a href="">` links
   - Classify each link: internal (templetxhomes.net), external, anchor, empty

3. Build adjacency list:
```
page-a → [page-b, page-c, page-d]
page-b → [page-a, page-e]
page-c → []  ← ORPHAN (no outgoing internal links)
```

### Step 2 — Identify Hub Pages
Hub pages should link to many spoke pages. Expected hubs:
- `/best-neighborhoods-temple-tx/` (should link to ALL neighborhood pages)
- `/investing-in-temple-tx/` (should link to investor pages)
- `/selling-your-home-temple-tx/` (should link to seller pages)
- `/` (home page — should link to top-level hubs)

Check: does each hub link to its expected spokes?

### Step 3 — Find Orphan Pages
Orphan = page with 0 incoming internal links from other pages.
```markdown
## Orphan Pages (0 incoming links)
| Page | Outgoing Links | Status |
|------|---------------|--------|
| [page] | X | 🔴 ORPHAN — needs links FROM hub pages |
```

### Step 4 — Find Dead Ends
Dead end = page with 0 outgoing internal links.
```markdown
## Dead End Pages (0 outgoing links)
| Page | Incoming Links | Status |
|------|---------------|--------|
| [page] | X | 🟡 DEAD END — add links TO related pages |
```

### Step 5 — Check Hidden Link Slots
Per CLAUDE.md, all neighborhood pages should have 5 hidden `<a>` slots in the Explore Neighborhoods section. Check:
- [ ] Do the slots exist in the HTML?
- [ ] Are any populated with actual links?
- [ ] Which slots are still empty?

### Step 6 — Link Quality Check
For each internal link:
- Does the target page exist? (flag broken links)
- Is the anchor text descriptive? (not "click here")
- Does the link context make sense topically?

### Step 7 — Generate Report

```markdown
# Internal Link Audit — [Date]

## Summary
- Total pages scanned: X
- Total internal links: X
- Average links per page: X.X
- Orphan pages: X
- Dead end pages: X
- Broken links: X

## Hub-and-Spoke Health
| Hub Page | Expected Spokes | Linked | Missing |
|----------|----------------|--------|---------|
| /best-neighborhoods/ | [list] | X/Y | [missing pages] |
| /investing/ | [list] | X/Y | [missing pages] |

## Orphan Pages
[table]

## Dead End Pages
[table]

## Broken Links
| Source Page | Broken Link | Expected Target |
|-----------|-------------|----------------|
| [page] | [href] | [what it should be] |

## Hidden Link Slot Status
| Page | Slots Present | Slots Filled | Empty Slots |
|------|--------------|-------------|------------|
| [page] | 5 | X | X |

## Recommended Link Additions
| From Page | To Page | Suggested Anchor Text | Priority |
|-----------|---------|----------------------|----------|
| [page] | [page] | [text] | 🔴 HIGH |

## Link Equity Flow Visualization
[Text-based diagram showing hub → spoke relationships]

Hub: /best-neighborhoods/
├── /canyon-creek/ ✅
├── /bella-terra/ ✅
├── /lake-pointe/ ✅
├── /prairie-ridge/ ✅
├── /alta-vista/ ✅
├── /legacy-ranch/ ✅
├── /windmill-farms/ ✅
├── /sage-meadows/ ❌ MISSING
└── /south-pointe/ ❌ MISSING
```

## Output Format
Save to `output/audits/internal-link-audit-YYYY-MM-DD.md`

## Quality Checks
- [ ] All HTML files in real-estate-redefined/ scanned
- [ ] Hub pages identified and spoke coverage checked
- [ ] Orphan pages flagged
- [ ] Dead end pages flagged
- [ ] Broken links identified
- [ ] Hidden link slots checked
- [ ] Recommended additions prioritized by SEO impact

## Brand Rules
- Anchor text should be descriptive ("homes in Canyon Creek" not "click here")
- Internal links should follow hub-and-spoke model
- Every neighborhood page should link to /best-neighborhoods/ hub
- Every neighborhood page should link to 2-3 related neighborhoods
