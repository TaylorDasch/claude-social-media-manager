#!/usr/bin/env python3
"""
Temple TX Investor Buy-Box Cash-Flow Model
Source of truth: MLS acquisition data (june-13-market-data.csv, pulled 2026-06-13)
Underwriting anchors from Taylor's published pages (brain): tax 2.2%, insurance $3,400/yr,
CoC target 6-9%. Rents = Taylor's operator numbers (MLS has no lease data) + external triangulation.

Run:  python3 cashflow_model.py [RATE_PCT]   (default rate placeholder = 7.5)
Numbers are formatted by Claude; all math is computed here.
"""
import sys

# ---- GLOBAL ASSUMPTIONS (edit when research verifies) ----
RATE = float(sys.argv[1]) / 100 if len(sys.argv) > 1 else 0.07375  # investor 30yr fixed ~25% down (VERIFIED June 2026: 7.1-7.6%, ~7.375% typ)
DOWN = 0.25            # investor conventional down payment
TERM_MONTHS = 360
TAX_RATE = 0.020       # EFFECTIVE on purchase: statutory 2.0-2.35% but assessed value runs ~10% under purchase when owner protests + stays on it (Taylor 2026-06-13)
INSURANCE_YR = 2400    # landlord/DP3 older Temple SFR (VERIFIED June 2026: $1,800-$2,500 typ; pier-and-beam upper-mid)
CLOSING_PCT = 0.03     # acquisition closing costs (for cash-invested denominator)

def pmt(principal, annual_rate, n=TERM_MONTHS):
    r = annual_rate / 12
    if r == 0: return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

def model(name, price, rehab, monthly_rent, strategy="LTR",
          vacancy=None, pm=None, maint=None, tax_rate=TAX_RATE, ins=INSURANCE_YR,
          hoa_mo=0, note=""):
    # strategy defaults — Taylor's reality (set 2026-06-13): PM 7% (his fee) on LTR; MTR self-managed; capex 5% rehabbed / 10% turnkey-older
    if strategy == "MTR":
        vacancy = 0.10 if vacancy is None else vacancy   # MTR gap/turnover
        pm = 0.0 if pm is None else pm                   # SELF-MANAGED (Furnished Finder, Taylor runs his own)
        maint = 0.05 if maint is None else maint         # rehabbed
        extra_mo = 250  # utilities + furnishing amortization + supplies for MTR
    else:
        vacancy = 0.05 if vacancy is None else vacancy
        pm = 0.07 if pm is None else pm                  # Taylor's 7% management fee (market 3rd-party = 10%)
        maint = 0.05 if maint is None else maint         # rehabbed home yrs 1-5; turnkey/as-is older overridden to 0.10
        extra_mo = 0

    loan = price * (1 - DOWN)
    mortgage = pmt(loan, RATE)
    gross = monthly_rent
    eff = gross * (1 - vacancy)
    op = (eff * pm) + (eff * maint) + (price * tax_rate / 12) + (ins / 12) + hoa_mo + extra_mo
    noi_mo = eff - op
    cf = noi_mo - mortgage
    cash_in = price * DOWN + price * CLOSING_PCT + rehab
    coc = (cf * 12) / cash_in if cash_in else 0
    # cap rate on all-in (price+rehab)
    cap = (noi_mo * 12) / (price + rehab) if (price + rehab) else 0
    grm = (price + rehab) / (gross * 12) if gross else 0
    rtp = gross / (price + rehab) if (price + rehab) else 0  # gross rent-to-price (monthly)
    return dict(name=name, strategy=strategy, price=price, rehab=rehab, allin=price+rehab,
                rent=gross, mortgage=mortgage, opex_mo=op, noi_mo=noi_mo, cf=cf,
                cash_in=cash_in, coc=coc, cap=cap, rtp=rtp, note=note)

# ---- BUY BOXES — acquisition from MLS june-13 SOLD; rents now MLS-VERIFIED from rental-data-bell.csv (432 Temple, mostly leased) ----
boxes = [
    # 1. 2-1 full rehab -> MTR. MTR $1,900 verified vs Furnished Finder (FF Temple median $2,000). The winner.
    model("2-1 full rehab -> MTR (hospital)", price=120000, rehab=45000, monthly_rent=1900,
          strategy="MTR", note="2BR pre-1975 median $129K; MTR $1,900 = ~4% below FF Temple median"),
    # 2a. 3-2 hospital AS-IS: MLS hospital 3BR 800-1300sf leased median $1,395
    model("3-2 hospital AS-IS rent $1,395", price=150000, rehab=5000, monthly_rent=1395,
          strategy="LTR", maint=0.10, note="MLS hospital 3BR 800-1300sf leased median $1,395 (un-rehabbed, old systems)"),
    # 2b. 3-2 hospital RENOVATED: rehab lifts rent to ~$1,650 (MLS 3BR 1300-1800sf median $1,675) -> breakeven
    model("3-2 hospital RENOVATED rent $1,650", price=150000, rehab=30000, monthly_rent=1650,
          strategy="LTR", note="MLS 3BR 1300-1800sf leased median $1,675; rehab IS the $255/mo rent lever"),
    # 3. Turnkey 3-2 <$180K (no rehab, RARE: only 6 truly turnkey in a year)
    model("Turnkey 3-2 <$180K (rare)", price=175000, rehab=5000, monthly_rent=1550,
          strategy="LTR", maint=0.10, note="Turnkey subset rare (6 of 62 sold); rent~hospital top10% $1,550; old systems = 10% capex"),
    # 4. 76502 Cimarron/older slab, light CF. MLS-supported LTR ~$1,500
    model("76502 Cimarron/older (light CF)", price=185000, rehab=20000, monthly_rent=1500,
          strategy="LTR", note="Cimarron median $169.5K; LTR ~$1,500"),
    # 4b. Canyon Creek (76502 premium slab). MLS Canyon Creek leased median $1,595
    model("Canyon Creek 76502", price=300000, rehab=15000, monthly_rent=1595,
          strategy="LTR", maint=0.10, hoa_mo=45, note="MLS sold median $330K; MLS leased median $1,595; retail/older = 10% capex"),
    # 5. West Temple (Western Hills). MLS Western Hills leased median $1,650
    model("West Temple (Western Hills)", price=237000, rehab=10000, monthly_rent=1650,
          strategy="LTR", maint=0.10, note="MLS sold median $237K; leased median $1,650; sells fast (27 DOM); retail/older = 10% capex"),
    # 6. Morgan's Point (Belton-addressed lake; rent est conservative LTR)
    model("Morgan's Point (Belton lake)", price=235000, rehab=10000, monthly_rent=1650,
          strategy="LTR", maint=0.10, note="MLS sold median $246.5K; rare deals; LTR est $1,650 (appreciation play); retail/older = 10% capex"),
    # 7. Older duplex LTR -> $1,300/side EXACT MLS match (duplex per-side leased median $1,300)
    model("Older duplex LTR ($1,300/side)", price=275000, rehab=20000, monthly_rent=2600,
          strategy="LTR", note="MLS duplex per-side leased median $1,300 (81 recs); 2x$1,300=$2,600"),
]

print(f"=== TEMPLE INVESTOR BUY-BOX CASH FLOW ===  rate={RATE*100:.2f}%  down={DOWN*100:.0f}%  tax={TAX_RATE*100:.1f}%  ins=${INSURANCE_YR}/yr")
print(f"{'BOX':<46}{'Strat':<5}{'AllIn':>9}{'Rent':>7}{'Mtg':>7}{'OpEx':>7}{'CF/mo':>8}{'CoC':>7}{'Cap':>6}{'RtP':>7}")
for b in boxes:
    print(f"{b['name'][:45]:<46}{b['strategy']:<5}{b['allin']:>9,.0f}{b['rent']:>7,.0f}"
          f"{b['mortgage']:>7,.0f}{b['opex_mo']:>7,.0f}{b['cf']:>+8,.0f}{b['coc']*100:>6.1f}%{b['cap']*100:>5.1f}%{b['rtp']*100:>6.2f}%")
print("\nNote: CF/mo = monthly cash flow after debt service. CoC = cash-on-cash on (down+closing+rehab). RtP = gross monthly rent / all-in.")
print("RtP >= ~0.8% monthly is the rough cash-flow line in a 7%+ rate world.")
