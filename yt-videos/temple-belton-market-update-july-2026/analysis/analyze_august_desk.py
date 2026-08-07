#!/usr/bin/env python3
"""Reproduce the August 2026 desk-video aggregates.

This module reuses the reviewed July market-analysis functions while keeping the
original July package intact. It is read-only and emits aggregates only.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

import analyze_market as market


SOURCE = Path(
    "/Users/taylordasch_1/market-monitor/temple-belton-0-365-2026-08-05.csv"
)
AS_OF = date(2026, 8, 5)
CLOSE_THROUGH = date(2026, 8, 5)
YTD_THROUGH = date(2026, 8, 5)


def build() -> dict[str, Any]:
    rows = market.read_csv(SOURCE)
    active = market.exact_status_rows(rows, "Active")
    closed = market.exact_status_rows(rows, "Closed")
    snapshot = market.comparable_snapshot(
        closed,
        active,
        AS_OF,
        CLOSE_THROUGH,
    )

    # The historical function deduplicates overlapping exports using city,
    # normalized address, close date, and close price. Point it at the newest
    # Temple/Belton file so the same-period 2025/2026 read reaches August 5.
    prior_history_source = market.HISTORY_CURRENT_PATH
    prior_ytd_through = market.YTD_CLOSE_THROUGH
    try:
        market.HISTORY_CURRENT_PATH = SOURCE
        market.YTD_CLOSE_THROUGH = YTD_THROUGH
        history, history_sources = market.historical_closed()
        ytd = market.annual_ytd(history)
    finally:
        market.HISTORY_CURRENT_PATH = prior_history_source
        market.YTD_CLOSE_THROUGH = prior_ytd_through

    ytd_2025 = ytd["2025"]["combined"]
    ytd_2026 = ytd["2026"]["combined"]

    return {
        "method": {
            "source": str(SOURCE),
            "as_of": AS_OF.isoformat(),
            "active_definition": (
                "City in {Temple, Belton}; PropertyType = Residential; "
                "Status = Active; CurrentPrice >= $25,000."
            ),
            "price_cut_definition": "CurrentPrice < OriginalListPrice.",
            "closed_definition": (
                "City in {Temple, Belton}; PropertyType = Residential; "
                "Status = Closed; CloseDate 2026-07-07 through 2026-08-05; "
                "ClosePrice >= $25,000."
            ),
            "history_sources": history_sources,
            "limits": (
                "The export omits MLS number, CDOM, and seller credits. DOM "
                "buckets are cross-sectional listing-record groups, not a "
                "cohort of the same properties followed through time."
            ),
        },
        "source_quality": {
            "row_count": len(rows),
            "city_counts": Counter(row["City"].strip() for row in rows),
            "status_counts": Counter(row["Status"].strip() for row in rows),
            "property_type_counts": Counter(
                row["PropertyType"].strip() for row in rows
            ),
        },
        "snapshot": snapshot,
        "ytd": {
            "2025": ytd["2025"],
            "2026": ytd["2026"],
            "combined_change": {
                "sale_count_pct": market.relative_change(
                    ytd_2026["sale_count"], ytd_2025["sale_count"]
                ),
                "median_close_price_pct": market.relative_change(
                    ytd_2026["median_close_price"],
                    ytd_2025["median_close_price"],
                ),
                "median_dom_days": (
                    ytd_2026["median_dom"] - ytd_2025["median_dom"]
                ),
            },
        },
    }


def main() -> None:
    print(json.dumps(build(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
