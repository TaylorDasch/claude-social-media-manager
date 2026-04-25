# Investor Deal Analysis

## Trigger
"deal analysis", "run the numbers", "analyze this deal", "investor numbers", "cash flow analysis", "cap rate"

## Required Inputs
- Property address
- List price (or purchase price if under contract)
- Estimated or actual rent (monthly)
- Optional: rehab estimate, down payment %, loan terms, HOA, property management %

## Step-by-Step Execution

### Step 1 — Pull Property Data
1. Check `data/` CSVs for MLS data on this property or comparable sales
2. Check `data/BELL_CAD_RESIDENTIAL.csv` for tax assessed value
3. If available, pull: square footage, year built, bedrooms, bathrooms, lot size
4. Note: if data isn't available in local files, mark as `[VERIFY — need MLS pull]`

### Step 2 — Set Assumptions
Use these defaults (override with actuals when provided):

| Parameter | Default | Notes |
|-----------|---------|-------|
| Down Payment | 20% | Conventional investor loan |
| Interest Rate | 7.0% | Current market — VERIFY before publishing |
| Loan Term | 30 years | Fixed |
| Property Tax Rate | 2.5% | Bell County average — check CAD |
| Insurance | $1,800/yr | Estimate for Temple — verify |
| Property Management | 10% | Standard for buy-and-hold |
| Vacancy Rate | 8% | ~1 month/year |
| Maintenance Reserve | 5% of rent | |
| CapEx Reserve | 5% of rent | |
| HOA | $0 | Most Temple neighborhoods — verify |
| Closing Costs | 3% of purchase | |

### Step 3 — Calculate PITI
```
Principal + Interest = monthly mortgage payment (amortization formula)
Property Tax = (assessed value × tax rate) / 12
Insurance = annual premium / 12
HOA = monthly amount

PITI = P&I + Tax + Insurance + HOA
```

### Step 4 — Calculate Cash Flow
```
Gross Monthly Rent = $X
- Vacancy (8%) = -$X
= Effective Gross Income

- PITI = -$X
- Property Management (10%) = -$X
- Maintenance Reserve (5%) = -$X
- CapEx Reserve (5%) = -$X

= Net Monthly Cash Flow: $X
= Net Annual Cash Flow: $X
```

### Step 5 — Calculate Returns
```
Cap Rate = (NOI / Purchase Price) × 100
  NOI = Annual Rent - Vacancy - Taxes - Insurance - Mgmt - Maintenance - CapEx (NO debt service)

Cash-on-Cash Return = (Annual Cash Flow / Total Cash Invested) × 100
  Total Cash Invested = Down Payment + Closing Costs + Rehab

DSCR = NOI / Annual Debt Service
  (Lenders want ≥ 1.2)

GRM = Purchase Price / Annual Gross Rent
  (Lower = better, Temple typical: 8-12)

1% Rule Test = Monthly Rent / Purchase Price
  (≥ 1% = passes)
```

### Step 6 — Equity Position
```
Purchase Price: $X
Estimated ARV (if rehab): $X
Instant Equity: $X (ARV - Purchase - Rehab)

5-Year Appreciation (3% annual): $X
5-Year Principal Paydown: $X
5-Year Total Equity Build: $X
```

### Step 7 — Risk Assessment
Rate each factor GREEN / YELLOW / RED:

| Factor | Rating | Notes |
|--------|--------|-------|
| Cash Flow | [G/Y/R] | Green ≥ $200/mo, Yellow $100-200, Red < $100 |
| Cap Rate | [G/Y/R] | Green ≥ 7%, Yellow 5-7%, Red < 5% |
| DSCR | [G/Y/R] | Green ≥ 1.3, Yellow 1.1-1.3, Red < 1.1 |
| 1% Rule | [G/Y/R] | Green ≥ 1%, Yellow 0.8-1%, Red < 0.8% |
| Location | [G/Y/R] | Near BSW/Fort Hood = green |
| Condition | [G/Y/R] | Based on year built, known issues |
| Exit Strategy | [G/Y/R] | Days on market for this price range |

### Step 8 — Verdict
```
VERDICT: [BUY / NEGOTIATE / PASS]
Best strategy: [LTR / MTR / BRRRR / Sub-To / Pass]
Target offer price: $X (for [target CoC return]%)
Key risk: [biggest concern]
Key upside: [biggest opportunity]
```

## Output Format
```markdown
# Deal Analysis — [Address]

## Property Overview
| Detail | Value |
|--------|-------|
| Address | [address] |
| List Price | $XXX,XXX |
| Sq Ft | X,XXX |
| Bed/Bath | X/X |
| Year Built | XXXX |
| Lot Size | X.XX acres |

## Financial Summary
| Metric | Value |
|--------|-------|
| Monthly PITI | $X,XXX |
| Monthly Cash Flow | $XXX |
| Annual Cash Flow | $X,XXX |
| Cap Rate | X.X% |
| CoC Return | X.X% |
| DSCR | X.XX |
| 1% Rule | X.XX% |

## Detailed Breakdown
[Full PITI and cash flow calculations]

## Risk Matrix
[Risk assessment table]

## Verdict
[Buy/Negotiate/Pass with reasoning]

## Assumptions Used
[All assumptions listed for transparency]
```

Save to `output/YYYY-WXX/deal-analysis/[address-slug].md`

## Quality Checks
- [ ] All math done by calculation, not estimated (NO hallucinated numbers)
- [ ] Tax rate verified against Bell County CAD data
- [ ] Interest rate reflects current market (flag if using default)
- [ ] All assumptions explicitly stated
- [ ] Price framing: $130K-$225K = investor-grade, $250K+ = owner-occupant
- [ ] Never frame $250K+ as investor opportunity unless exceptional cap rate
- [ ] DSCR calculated correctly (NOI / debt service, not cash flow / debt service)

## Brand Rules
- "Buy-and-hold" not "turnkey"
- MTR near BSW = best risk-adjusted return in Temple market
- Be honest about deals that don't work — Taylor's credibility depends on it
- If the deal doesn't pencil, say so clearly
- Fort Hood (not Fort Cavazos)
