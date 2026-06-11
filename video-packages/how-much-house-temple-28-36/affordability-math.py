#!/usr/bin/env python3
"""28/36 affordability + Temple PITI worked examples.
Real math for the templetxhomes.net page. No hardcoded rate in evergreen copy —
rate is a labeled EXAMPLE here (6.5%) and an editable field in the page calculator.
Tax = Temple effective 2.25% (Bell CAD 2025). Insurance = $2,000/yr est.
"""
def pmt(loan, apr, years=30):
    r = apr/12; n = years*12
    return loan/n if r == 0 else loan*r/(1-(1+r)**-n)

def piti(price, down_pct, apr, tax=0.0225, ins=2000, mi_rate=0.0):
    loan = price*(1-down_pct)
    pi  = pmt(loan, apr)
    t   = price*tax/12
    i   = ins/12
    mi  = loan*mi_rate/12
    return dict(loan=loan, pi=pi, tax=t, ins=i, mi=mi, total=pi+t+i+mi)

print("="*64)
print("28/36 RULE — income $7,000/mo (= $84,000/yr)")
print("="*64)
inc = 7000
print(f"  28% housing ceiling : ${inc*0.28:,.0f}/mo  (PITI target)")
print(f"  36% total-debt ceil : ${inc*0.36:,.0f}/mo")
print(f"  room for car/cards  : ${inc*0.36 - inc*0.28:,.0f}/mo")
print(f"  32% = house-poor line: ${inc*0.32:,.0f}/mo")

print("\n" + "="*64)
print("FORWARD: PITI at Temple price points (example rate 6.5%, tax 2.25%)")
print("="*64)
print(f"{'Price':>8} {'Down':>6} {'Loan':>9} {'P&I':>7} {'Tax':>6} {'Ins':>5} {'MI':>5} {'PITI':>8}")
for price in (260000, 270000, 280000):
    for dp, mi in ((0.20,0.0),(0.10,0.005),(0.05,0.005),(0.035,0.0055)):
        x = piti(price, dp, 0.065, mi_rate=mi)
        print(f"${price/1000:>5.0f}K {dp*100:>4.1f}% ${x['loan']/1000:>6.1f}K "
              f"${x['pi']:>6.0f} ${x['tax']:>5.0f} ${x['ins']:>4.0f} ${x['mi']:>4.0f} ${x['total']:>7.0f}")
    print()

print("="*64)
print("REVERSE: max price that keeps PITI <= $1,960 (20% down, no PMI)")
print("="*64)
for apr in (0.060, 0.065, 0.070):
    lo, hi = 100000, 500000
    for _ in range(60):
        mid = (lo+hi)/2
        if piti(mid, 0.20, apr)['total'] > 1960: hi = mid
        else: lo = mid
    print(f"  @ {apr*100:.2f}% example rate -> max price ${lo:,.0f}")

print("\n" + "="*64)
print("CALCULATOR DEFAULTS: income -> 28% housing budget -> ~price (20% dn, 6.5%)")
print("="*64)
def maxprice(budget, apr=0.065, dp=0.20):
    lo, hi = 50000, 900000
    for _ in range(60):
        mid=(lo+hi)/2
        if piti(mid, dp, apr)['total'] > budget: hi=mid
        else: lo=mid
    return lo
for mo in (5000,6000,7000,8000,10000,12000):
    b = mo*0.28
    print(f"  ${mo:>6,}/mo income -> ${b:>5,.0f}/mo housing -> ~${maxprice(b):,.0f} home")
