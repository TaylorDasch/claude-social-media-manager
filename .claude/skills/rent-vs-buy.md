# Rent vs Buy Comparison

## Trigger
"rent vs buy", "rent versus buy", "should I rent or buy", "true cost comparison", "renting vs buying"

## Required Inputs
- Target home price (or price range)
- Current rent amount (or typical rent for the area/size)
- Zip code (76502, 76504, or 76513)
- Optional: specific neighborhood, buyer profile (Military BAH, BSW physician, first-time)

## Step-by-Step Execution

### Step 1 — Gather Data
1. Check `data/[zipcode]/` for MLS data on purchase prices and comps
2. Check `data/temple-belton-rentals-0-90.csv` for rental comps
3. Read `reference/TEMPLE-TX-DATA-VAULT.md` for: tax rates, insurance estimates, BAH rates
4. Read `data/2025-Tax-Rate-Chart.pdf` for exact tax rates by jurisdiction

### Step 2 — Calculate Buying Costs

**Monthly costs:**
```
Principal & Interest: [amortization at current rate]
Property Tax: [assessed value × rate / 12]
Homeowner's Insurance: [$150-180/mo typical]
HOA: [$0-50/mo — most Temple neighborhoods have none]
PMI (if <20% down): [$X/mo]
Maintenance Reserve: [1% of home value / 12]

Total Monthly Cost of Ownership: $X,XXX
```

**Upfront costs:**
```
Down Payment: $X (X%)
Closing Costs: ~3% = $X
Home Inspection: ~$500
Appraisal: ~$500-600
Total Cash Needed: $X,XXX
```

### Step 3 — Calculate Renting Costs

```
Monthly Rent: $X,XXX
Renter's Insurance: ~$25/mo
Annual Rent Increase: 3-5% (Temple market avg)
Security Deposit: 1 month rent (upfront)
```

### Step 4 — Build Comparison Table (2/3/5 Year)

```markdown
## True Cost Comparison

| | Renting | Buying |
|---|---------|--------|
| **Year 1** | | |
| Monthly payment | $X,XXX | $X,XXX |
| Annual total | $XX,XXX | $XX,XXX |
| Equity built | $0 | $X,XXX |
| Tax benefit (est.) | $0 | $X,XXX |
| Net cost Year 1 | $XX,XXX | $XX,XXX |
| | | |
| **Year 2** | | |
| Monthly (with increase) | $X,XXX | $X,XXX (fixed) |
| Cumulative spent | $XX,XXX | $XX,XXX |
| Cumulative equity | $0 | $XX,XXX |
| | | |
| **Year 3** | | |
| Monthly (with increase) | $X,XXX | $X,XXX (fixed) |
| Cumulative spent | $XX,XXX | $XX,XXX |
| Cumulative equity | $0 | $XX,XXX |
| | | |
| **Year 5** | | |
| Monthly (with increase) | $X,XXX | $X,XXX (fixed) |
| Cumulative spent | $XXX,XXX | $XXX,XXX |
| Cumulative equity | $0 | $XX,XXX |
| Home appreciation (3%) | N/A | +$XX,XXX |
| **Net position** | **-$XXX,XXX** | **+$XX,XXX** |
```

### Step 5 — Breakeven Analysis
```
Months to breakeven: [when buying becomes cheaper than renting, accounting for equity]
Breakeven home price: [if renting at $X, buying makes sense above/below $X]
```

### Step 6 — Persona-Specific Notes

**Military (BAH):**
- Current BAH for E-5 with dependents at Fort Hood: $X,XXX/mo
- BAH covers: [X%] of PITI at this price point
- VA loan advantage: $0 down, no PMI
- If PCSing in <3 years: [rent vs buy recommendation]

**BSW Physician:**
- Physician loan available: 0-10% down, no PMI on jumbo
- Starting salary consideration: [typical resident vs attending]
- If still in residency: [rent recommendation]
- If attending: [buy recommendation with physician loan terms]

**First-Time Buyer:**
- FHA option: 3.5% down = $X total
- Texas first-time buyer programs: [mention TSAHC if applicable]
- Student loan impact on DTI: [note if relevant]

### Step 7 — Verdict
```
RECOMMENDATION: [BUY / RENT / DEPENDS]

Buy if: [specific conditions]
Rent if: [specific conditions]
The math: [1-2 sentence summary of the numbers]
```

## Output Format
Save to `output/YYYY-WXX/rent-vs-buy/[price-point]-[zip].md`

Include a clean data table that can be screenshotted or turned into a video overlay.

## Quality Checks
- [ ] All numbers calculated, never estimated or hallucinated
- [ ] Tax rate matches the specific jurisdiction (Temple ISD vs Belton ISD matters)
- [ ] Rent escalation assumption stated explicitly (3-5%)
- [ ] Appreciation assumption stated explicitly (3% default for Temple)
- [ ] BAH rates verified against current DoD tables if military scenario
- [ ] Interest rate reflects current market — flag if using a default
- [ ] Breakeven calculation included
- [ ] Persona-specific notes if buyer profile provided

## Brand Rules
- Never pressure to buy — present the data honestly
- If renting makes more sense, say so
- "The math works like this..." framing
- Fort Hood (not Fort Cavazos)
- Include real negatives: property taxes are high in Texas, maintenance costs, etc.
