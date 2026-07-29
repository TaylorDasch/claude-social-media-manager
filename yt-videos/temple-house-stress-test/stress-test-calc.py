#!/usr/bin/env python3
"""Temple House Stress Test — verdict engine calculator.

Implements SERIES-BIBLE.md sections 3.2-3.4 and the 1.3 Tier-B display math.
Run in prep week with the real deal file; the demo block at the bottom is
ILLUSTRATIVE ONLY (slot-coherent example set from the bible) and every figure
in it must be replaced with documented numbers before anything goes on screen.

Usage: python3 stress-test-calc.py            # runs the illustrative demo
       import and call run_engine(...) with real file data for prep week.
"""

from dataclasses import dataclass, field

BUY_LINE = 1.5    # % of price — below: BUY (and zero S3)
WALK_LINE = 5.0   # % of price — above: WALK
SINGLE_FINDING_LINE = 1.0  # any single documented finding >= this % alone => NEGOTIATE
ANCHOR_STEP = 25_000       # Tier B rounded anchor granularity


@dataclass
class Finding:
    name: str
    category: str            # Foundation & Structure | Roof & Envelope | Water & Drainage | Big-Ticket Systems | Loan-Killer Flags (VA/FHA MPR)
    severity: str            # S1 | S2 | S3
    source: str = ""         # [inspection report] [option-period quote] [invoice] [closing statement] [current quote — MM/YYYY]
    cost_exact: float | None = None
    cost_range: tuple | None = None   # (low, high) -> midpoint used, method stated on screen
    leverage: str = ""       # R | C | P (S2/S3 only; S1 never generates an ask)
    s3_curable: bool = True  # S3 only: scoped+quoted+curable before closing?
    mpr_refused: bool = False  # VA/FHA MPR item seller refuses to cure

    @property
    def documented(self) -> float | None:
        if self.cost_exact is not None:
            return float(self.cost_exact)
        if self.cost_range is not None:
            return (self.cost_range[0] + self.cost_range[1]) / 2.0
        return None  # severity-only lane: "No document, no number."


def zone(pct: float, has_uncurable_s3: bool, mpr_refused: bool, any_single_ge_line: bool) -> tuple[str, str]:
    if has_uncurable_s3:
        return "WALK", "S3 that cannot be cured/verified before closing"
    if mpr_refused:
        return "WALK", "MPR item seller refuses to cure on a VA/FHA deal — the loan cannot close"
    if pct > WALK_LINE:
        return "WALK", f"TRE {pct:.1f}% > {WALK_LINE}% of price"
    if pct >= BUY_LINE or any_single_ge_line:
        why = f"TRE {pct:.1f}% in {BUY_LINE}–{WALK_LINE}%" if pct >= BUY_LINE else f"single finding ≥ {SINGLE_FINDING_LINE}% alone"
        return "NEGOTIATE", why
    return "BUY", f"TRE {pct:.1f}% < {BUY_LINE}% and zero S3 flags"


def run_engine(price: float, findings: list[Finding], tier: str = "B") -> None:
    print("=" * 66)
    print("TEMPLE HOUSE STRESS TEST — verdict engine")
    print("=" * 66)

    counter = 0.0
    any_single = False
    s3_uncurable = False
    mpr_refused = False
    mixed_vintage = False

    for i, f in enumerate(findings, 1):
        d = f.documented
        if f.severity == "S3" and not f.s3_curable:
            s3_uncurable = True
        if f.mpr_refused:
            mpr_refused = True
        if "current quote" in f.source:
            mixed_vintage = True
        if d is None:
            print(f"  #{i} {f.name} · {f.category} · {f.severity} · NO DOLLAR — severity-only lane "
                  f"('No document, no number.')")
            continue
        if f.severity == "S1":
            print(f"  #{i} {f.name} · {f.category} · S1 — logged, no ask, no tick")
            continue
        counter += d
        if d / price * 100 >= SINGLE_FINDING_LINE:
            any_single = True
        rng = (f" (${f.cost_range[0]:,.0f}–${f.cost_range[1]:,.0f} → midpoint)"
               if f.cost_range else "")
        print(f"  #{i} STAMP  {f.name} · {f.category} · {f.severity} · "
              f"${d:,.0f}{rng} {f.source} · leverage {f.leverage or '-'} · "
              f"counter ${counter:,.0f}")

    tre = counter
    true_pct = tre / price * 100
    verdict, why = zone(true_pct, s3_uncurable, mpr_refused, any_single)

    print("-" * 66)
    print(f"  TRE (documented): ${tre:,.0f}   Purchase price: ${price:,.0f}")
    print(f"  True math: {true_pct:.2f}% of price  →  VERDICT: {verdict}  ({why})")
    if mixed_vintage:
        print("  VINTAGE RULE: mixed-vintage TRE — use 'documented' framing everywhere;"
              " tally card carries the provenance note.")

    if tier.upper() == "E":
        print(f"  Display (Tier E — Exact): ${tre:,.0f} = {true_pct:.1f}% of ${price:,.0f}")
    else:
        anchor = round(price / ANCHOR_STEP) * ANCHOR_STEP
        disp_pct = round(tre / anchor * 100)
        d_verdict, _ = zone(float(disp_pct), s3_uncurable, mpr_refused, any_single)
        ok = d_verdict == verdict
        near_boundary = min(abs(disp_pct - BUY_LINE), abs(disp_pct - WALK_LINE)) < 0.5
        print(f"  Display (Tier B — Rounded Band): '${tre:,.0f} ≈ {disp_pct}% of about ${anchor:,.0f}'")
        print(f"  Zone-preservation: displayed reads {d_verdict} vs true {verdict} → "
              f"{'PASS' if ok and not near_boundary else 'FAIL — Tier B unavailable; owner elects Tier E or property fails Gate 6'}")
        if near_boundary and ok:
            print(f"  (boundary-adjacent whole percent — conservative fail per 1.3 zone-preservation rule)")
        recon = tre / (disp_pct / 100) if disp_pct else float("inf")
        inside = abs(recon - anchor) <= ANCHOR_STEP / 2
        print(f"  Reconstruction audit (QA row 13): TRE ÷ displayed % → ${recon:,.0f} — "
              f"{'inside' if inside else 'OUTSIDE'} the disclosed ±${ANCHOR_STEP/2:,.0f} band around the anchor.")
        print("  A viewer cannot distinguish the true price within that band from the on-screen math"
              if inside else
              "  FAIL: division escapes the disclosed band — re-check the display math before publish")
        print("  → still verify no OTHER on-screen figure (reduction-off-ask, totals) narrows it further.")
    print("=" * 66)


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # ILLUSTRATIVE DEMO ONLY — the bible's slot-coherent example set.
    # Every value below is a placeholder shape, NOT a real deal figure.
    # ------------------------------------------------------------------
    demo_price = 297_500
    demo = [
        Finding("Stair-step crack, brick veneer (rear corner)", "Foundation & Structure", "S2",
                "[option-period quote]", cost_range=(4_200, 5_400), leverage="P"),
        Finding("Soffit/fascia rot, north eave + patched shingles", "Roof & Envelope", "S2",
                "[invoice]", cost_exact=2_350, leverage="R"),
        Finding("Negative grade to slab + downspout discharge at foundation", "Water & Drainage", "S2",
                "[option-period quote]", cost_range=(1_150, 1_600), leverage="C"),
        Finding("Water heater past service life (age plate decode)", "Big-Ticket Systems", "S2",
                "[option-period quote]", cost_exact=1_685, leverage="C"),
        Finding("Peeling exterior paint — VA MPR item", "Loan-Killer Flags (VA/FHA MPR)", "S2",
                "[closing statement]", cost_exact=1_690, leverage="R"),
        Finding("Hairline slab crack, garage — age-appropriate", "Foundation & Structure", "S1"),
        Finding("Attic ductwork insulation thin in one run", "Big-Ticket Systems", "S2",
                ""),  # severity-only lane demo: no document, no number
    ]
    run_engine(demo_price, demo, tier="B")
