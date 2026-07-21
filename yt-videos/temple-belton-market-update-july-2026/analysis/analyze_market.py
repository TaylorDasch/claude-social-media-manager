#!/usr/bin/env python3
"""Reproduce the Temple/Belton market-update calculations.

The script is intentionally read-only. It prints JSON to stdout and never copies
MLS rows into the video package. Public artifacts should use aggregates only.
"""

from __future__ import annotations

import csv
import glob
import json
import math
import statistics
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


MARKET_ROOT = Path("/Users/taylordasch_1/market-monitor")
CURRENT_PATH = MARKET_ROOT / "whole-market-with-status-2026-07-20.csv"
HISTORY_CURRENT_PATH = MARKET_ROOT / "whole-market-2026-07-19.csv"
MAY_PATH = MARKET_ROOT / "05-14-2026-mls-templebelton.csv"
CURRENT_AS_OF = date(2026, 7, 20)
CURRENT_CLOSE_THROUGH = date(2026, 7, 20)
YTD_CLOSE_THROUGH = date(2026, 7, 17)
MAY_AS_OF = date(2026, 5, 14)
CITIES = ("Temple", "Belton")
# The May export predates the clean Status/PropertyType pull. Its first Matrix
# block reproduces the active denominator used in the prior market update, so it
# remains an explicitly caveated historical comparison rather than being
# silently reinterpreted as an exact-status extract.
MAY_ACTIVE_END = 889
PRICE_BANDS = (
    ("under_200k", 0, 200_000),
    ("200k_to_299999", 200_000, 300_000),
    ("300k_to_399999", 300_000, 400_000),
    ("400k_to_499999", 400_000, 500_000),
    ("500k_plus", 500_000, math.inf),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def number(value: Any) -> float | None:
    if value is None:
        return None
    cleaned = str(value).strip().replace("$", "").replace(",", "").replace("%", "")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_date(value: Any) -> date | None:
    cleaned = str(value or "").strip()
    if not cleaned:
        return None
    for pattern in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(cleaned, pattern).date()
        except ValueError:
            pass
    return None


def rounded(value: float | None, digits: int = 1) -> float | None:
    return None if value is None else round(value, digits)


def median(values: Iterable[float | None]) -> float | None:
    clean = [value for value in values if value is not None]
    return statistics.median(clean) if clean else None


def mean(values: Iterable[float | None]) -> float | None:
    clean = [value for value in values if value is not None]
    return statistics.fmean(clean) if clean else None


def percentile(values: Iterable[float | None], fraction: float) -> float | None:
    clean = sorted(value for value in values if value is not None)
    if not clean:
        return None
    index = (len(clean) - 1) * fraction
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return clean[lower]
    return clean[lower] + (clean[upper] - clean[lower]) * (index - lower)


def pct(numerator: int | float, denominator: int | float) -> float | None:
    return None if not denominator else 100 * numerator / denominator


def city_rows(rows: list[dict[str, str]], city: str) -> list[dict[str, str]]:
    return [row for row in rows if str(row.get("City", "")).strip() == city]


def exact_status_rows(
    rows: list[dict[str, str]], status: str, property_type: str = "Residential"
) -> list[dict[str, str]]:
    """Return rows matching the source's explicit status and property type."""

    if rows:
        missing = {"Status", "PropertyType"} - rows[0].keys()
        if missing:
            fields = ", ".join(sorted(missing))
            raise ValueError(f"exact status filtering requires source fields: {fields}")
    return [
        row
        for row in rows
        if str(row.get("Status", "")).strip() == status
        and str(row.get("PropertyType", "")).strip() == property_type
    ]


def inferred_active_block(
    rows: list[dict[str, str]], block_end: int
) -> list[dict[str, str]]:
    """Return a legacy source's first Matrix status block.

    This is retained only for the May historical comparison, whose export omits
    Status and PropertyType. Current claims use :func:`exact_status_rows`.
    """

    return rows[:block_end]


def closed_rows(
    rows: list[dict[str, str]], start: date | None = None, end: date | None = None
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in rows:
        closed = parse_date(row.get("CloseDate"))
        if closed is None:
            continue
        if start is not None and closed < start:
            continue
        if end is not None and closed > end:
            continue
        result.append(row)
    return result


def is_builder(row: dict[str, str]) -> bool:
    condition = str(row.get("SpecialListingConditions", "")).strip().casefold()
    return "builder" in condition


def original_price(row: dict[str, str]) -> float | None:
    return number(row.get("OriginalListPrice"))


def current_price(row: dict[str, str]) -> float | None:
    return number(row.get("CurrentPrice")) or number(row.get("ListPrice"))


def final_list_price(row: dict[str, str]) -> float | None:
    return number(row.get("ListPrice"))


def close_price(row: dict[str, str]) -> float | None:
    return number(row.get("ClosePrice"))


def dom(row: dict[str, str]) -> float | None:
    return number(row.get("DOM"))


def has_cut(row: dict[str, str]) -> bool:
    original = original_price(row)
    current = current_price(row)
    return bool(original and current and current < original)


def cut_dollars(row: dict[str, str]) -> float | None:
    if not has_cut(row):
        return None
    return original_price(row) - current_price(row)  # type: ignore[operator]


def cut_percent(row: dict[str, str]) -> float | None:
    original = original_price(row)
    cut = cut_dollars(row)
    return None if not original or cut is None else 100 * cut / original


def price_band(value: float | None) -> str | None:
    if value is None:
        return None
    for label, low, high in PRICE_BANDS:
        if low <= value < high:
            return label
    return None


def active_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    priced = [row for row in rows if current_price(row) is not None]
    cuts = [row for row in priced if has_cut(row)]
    dom_values = [dom(row) for row in rows]
    builder_rows = [row for row in rows if is_builder(row)]
    unique_addresses = {
        " ".join(str(row.get("Address", "")).split()).casefold()
        for row in rows
        if str(row.get("Address", "")).strip()
    }
    return {
        "row_count": len(rows),
        "unique_address_count": len(unique_addresses),
        "price_coverage": len(priced),
        "dom_coverage": sum(value is not None for value in dom_values),
        "median_current_price": rounded(median(current_price(row) for row in priced), 0),
        "median_dom": rounded(median(dom_values), 1),
        "average_dom": rounded(mean(dom_values), 1),
        "dom_p25": rounded(percentile(dom_values, 0.25), 1),
        "dom_p75": rounded(percentile(dom_values, 0.75), 1),
        "price_cut_count": len(cuts),
        "price_cut_share_pct": rounded(pct(len(cuts), len(priced)), 1),
        "median_price_cut_dollars": rounded(median(cut_dollars(row) for row in cuts), 0),
        "median_price_cut_pct": rounded(median(cut_percent(row) for row in cuts), 1),
        "builder_count": len(builder_rows),
        "builder_share_pct": rounded(pct(len(builder_rows), len(rows)), 1),
    }


def sold_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    priced = [row for row in rows if close_price(row) is not None]
    ratios_final = [
        100 * close_price(row) / final_list_price(row)
        for row in priced
        if final_list_price(row) and close_price(row)
    ]
    ratios_original = [
        100 * close_price(row) / original_price(row)
        for row in priced
        if original_price(row) and close_price(row)
    ]
    below_current = [
        row
        for row in priced
        if final_list_price(row) is not None and close_price(row) < final_list_price(row)
    ]
    at_current = [
        row
        for row in priced
        if final_list_price(row) is not None and close_price(row) == final_list_price(row)
    ]
    above_current = [
        row
        for row in priced
        if final_list_price(row) is not None and close_price(row) > final_list_price(row)
    ]
    builder_rows = [row for row in rows if is_builder(row)]
    return {
        "sale_count": len(rows),
        "price_coverage": len(priced),
        "median_close_price": rounded(median(close_price(row) for row in priced), 0),
        "median_dom": rounded(median(dom(row) for row in rows), 1),
        "average_dom": rounded(mean(dom(row) for row in rows), 1),
        "median_close_to_final_list_pct": rounded(median(ratios_final), 2),
        "median_close_to_original_list_pct": rounded(median(ratios_original), 2),
        "sold_below_final_list_count": len(below_current),
        "sold_below_final_list_share_pct": rounded(pct(len(below_current), len(priced)), 1),
        "sold_at_final_list_count": len(at_current),
        "sold_above_final_list_count": len(above_current),
        "builder_sale_count": len(builder_rows),
        "builder_sale_share_pct": rounded(pct(len(builder_rows), len(rows)), 1),
    }


def segment_summary(rows: list[dict[str, str]], kind: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for segment in ("all", "builder", "resale"):
        segment_rows = rows
        if segment == "builder":
            segment_rows = [row for row in rows if is_builder(row)]
        elif segment == "resale":
            segment_rows = [row for row in rows if not is_builder(row)]
        result[segment] = (
            active_summary(segment_rows)
            if kind == "active"
            else sold_summary(segment_rows)
        )
    return result


def band_summaries(rows: list[dict[str, str]], kind: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    price_getter = current_price if kind == "active" else close_price
    for label, _, _ in PRICE_BANDS:
        group = [row for row in rows if price_band(price_getter(row)) == label]
        result[label] = active_summary(group) if kind == "active" else sold_summary(group)
    return result


def dom_cut_ladder(rows: list[dict[str, str]]) -> dict[str, Any]:
    buckets = (
        ("0_to_30", 0, 30),
        ("31_to_60", 31, 60),
        ("61_to_90", 61, 90),
        ("91_to_120", 91, 120),
        ("121_plus", 121, math.inf),
    )
    result: dict[str, Any] = {}
    for label, low, high in buckets:
        group = [
            row
            for row in rows
            if dom(row) is not None and dom(row) >= 0 and low <= dom(row) <= high
        ]
        cuts = [row for row in group if has_cut(row)]
        result[label] = {
            "row_count": len(group),
            "price_cut_count": len(cuts),
            "price_cut_share_pct": rounded(pct(len(cuts), len(group)), 1),
        }
    day_91_plus = [row for row in rows if dom(row) is not None and dom(row) >= 91]
    day_91_plus_cuts = [row for row in day_91_plus if has_cut(row)]
    result["91_plus"] = {
        "row_count": len(day_91_plus),
        "price_cut_count": len(day_91_plus_cuts),
        "price_cut_share_pct": rounded(pct(len(day_91_plus_cuts), len(day_91_plus)), 1),
    }
    return result


def relative_change(current: float | None, prior: float | None) -> float | None:
    if current is None or prior in (None, 0):
        return None
    return rounded(100 * (current - prior) / prior, 1)


def comparable_snapshot(
    sold_source_rows: list[dict[str, str]],
    active_rows: list[dict[str, str]],
    as_of: date,
    close_through: date,
) -> dict[str, Any]:
    start = close_through - timedelta(days=29)
    result: dict[str, Any] = {
        "as_of": as_of.isoformat(),
        "closed_window": [start.isoformat(), close_through.isoformat()],
        "cities": {},
    }
    for city in CITIES:
        active_scoped = [
            row
            for row in city_rows(active_rows, city)
            if current_price(row) and current_price(row) >= 25_000
        ]
        sold_scoped = [
            row
            for row in city_rows(sold_source_rows, city)
            if close_price(row) and close_price(row) >= 25_000
        ]
        sold = closed_rows(sold_scoped, start, close_through)
        result["cities"][city] = {
            "active": segment_summary(active_scoped, "active"),
            "active_by_price_band": band_summaries(active_scoped, "active"),
            "active_dom_cut_ladder": dom_cut_ladder(active_scoped),
            "sold_30d": segment_summary(sold, "sold"),
            "sold_30d_by_price_band": band_summaries(sold, "sold"),
        }
    active_combined = [
        row
        for row in active_rows
        if str(row.get("City", "")).strip() in CITIES
        and current_price(row)
        and current_price(row) >= 25_000
    ]
    sold_combined = [
        row
        for row in sold_source_rows
        if str(row.get("City", "")).strip() in CITIES
        and close_price(row)
        and close_price(row) >= 25_000
    ]
    sold = closed_rows(sold_combined, start, close_through)
    result["combined"] = {
        "active": segment_summary(active_combined, "active"),
        "active_by_price_band": band_summaries(active_combined, "active"),
        "active_dom_cut_ladder": dom_cut_ladder(active_combined),
        "sold_30d": segment_summary(sold, "sold"),
        "sold_30d_by_price_band": band_summaries(sold, "sold"),
    }
    return result


def dedupe_closed(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, float | None]] = set()
    result: list[dict[str, str]] = []
    for row in rows:
        city = str(row.get("City", "")).strip()
        closed = parse_date(row.get("CloseDate"))
        if city not in CITIES or closed is None:
            continue
        if close_price(row) is None or close_price(row) < 25_000:
            continue
        key = (
            city.casefold(),
            " ".join(str(row.get("Address", "")).split()).casefold(),
            closed.isoformat(),
            close_price(row),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(row)
    return result


def historical_closed() -> tuple[list[dict[str, str]], list[str]]:
    pattern = str(MARKET_ROOT / "temple-belton-historical-data/*.csv")
    source_paths = [Path(path) for path in sorted(glob.glob(pattern))]
    source_paths.extend(
        [
            MARKET_ROOT / "june-13-market-data.csv",
            MARKET_ROOT / "july-13-active-sold-pending-0-30.csv",
            HISTORY_CURRENT_PATH,
        ]
    )
    rows: list[dict[str, str]] = []
    for path in source_paths:
        rows.extend(closed_rows(read_csv(path)))
    return dedupe_closed(rows), [str(path) for path in source_paths]


def ytd_summary(
    rows: list[dict[str, str]], year: int, through_month_day: tuple[int, int]
) -> dict[str, Any]:
    start = date(year, 1, 1)
    end = date(year, through_month_day[0], through_month_day[1])
    scoped = closed_rows(rows, start, end)
    return {
        "window": [start.isoformat(), end.isoformat()],
        "combined": sold_summary(scoped),
        "cities": {city: sold_summary(city_rows(scoped, city)) for city in CITIES},
    }


def annual_ytd(rows: list[dict[str, str]]) -> dict[str, Any]:
    month_day = (YTD_CLOSE_THROUGH.month, YTD_CLOSE_THROUGH.day)
    return {
        str(year): ytd_summary(rows, year, month_day) for year in range(2010, 2027)
    }


def main() -> None:
    current_rows = read_csv(CURRENT_PATH)
    may_rows = read_csv(MAY_PATH)
    current_active = exact_status_rows(current_rows, "Active")
    current_closed = exact_status_rows(current_rows, "Closed")
    may_active = inferred_active_block(may_rows, MAY_ACTIVE_END)
    current = comparable_snapshot(
        current_closed, current_active, CURRENT_AS_OF, CURRENT_CLOSE_THROUGH
    )
    may = comparable_snapshot(may_rows, may_active, MAY_AS_OF, MAY_AS_OF)
    history, history_sources = historical_closed()

    changes: dict[str, Any] = {"cities": {}}
    for city in CITIES:
        current_city = current["cities"][city]
        may_city = may["cities"][city]
        changes["cities"][city] = {
            "active_row_count_pct": relative_change(
                current_city["active"]["all"]["row_count"], may_city["active"]["all"]["row_count"]
            ),
            "median_active_price_pct": relative_change(
                current_city["active"]["all"]["median_current_price"],
                may_city["active"]["all"]["median_current_price"],
            ),
            "median_active_dom_pct": relative_change(
                current_city["active"]["all"]["median_dom"], may_city["active"]["all"]["median_dom"]
            ),
            "price_cut_share_point_change": rounded(
                current_city["active"]["all"]["price_cut_share_pct"]
                - may_city["active"]["all"]["price_cut_share_pct"],
                1,
            ),
            "sold_30d_count_pct": relative_change(
                current_city["sold_30d"]["all"]["sale_count"],
                may_city["sold_30d"]["all"]["sale_count"],
            ),
            "median_sold_price_pct": relative_change(
                current_city["sold_30d"]["all"]["median_close_price"],
                may_city["sold_30d"]["all"]["median_close_price"],
            ),
        }
    current_combined = current["combined"]
    may_combined = may["combined"]
    changes["combined"] = {
        "active_row_count_pct": relative_change(
            current_combined["active"]["all"]["row_count"],
            may_combined["active"]["all"]["row_count"],
        ),
        "median_active_price_pct": relative_change(
            current_combined["active"]["all"]["median_current_price"],
            may_combined["active"]["all"]["median_current_price"],
        ),
        "median_active_dom_pct": relative_change(
            current_combined["active"]["all"]["median_dom"],
            may_combined["active"]["all"]["median_dom"],
        ),
        "price_cut_share_point_change": rounded(
            current_combined["active"]["all"]["price_cut_share_pct"]
            - may_combined["active"]["all"]["price_cut_share_pct"],
            1,
        ),
        "sold_30d_count_pct": relative_change(
            current_combined["sold_30d"]["all"]["sale_count"],
            may_combined["sold_30d"]["all"]["sale_count"],
        ),
        "median_sold_price_pct": relative_change(
            current_combined["sold_30d"]["all"]["median_close_price"],
            may_combined["sold_30d"]["all"]["median_close_price"],
        ),
    }

    result = {
        "method": {
            "scope": list(CITIES),
            "current_source": str(CURRENT_PATH),
            "current_source_mtime": datetime.fromtimestamp(
                CURRENT_PATH.stat().st_mtime
            ).isoformat(),
            "current_as_of": CURRENT_AS_OF.isoformat(),
            "current_close_through": CURRENT_CLOSE_THROUGH.isoformat(),
            "long_run_close_through": YTD_CLOSE_THROUGH.isoformat(),
            "long_run_current_source": str(HISTORY_CURRENT_PATH),
            "may_source": str(MAY_PATH),
            "may_source_mtime": datetime.fromtimestamp(MAY_PATH.stat().st_mtime).isoformat(),
            "active_definition": (
                "Current source rows with exact PropertyType = Residential and "
                "Status = Active, then exact City in {Temple, Belton} and a "
                "$25,000 current-price floor."
            ),
            "closed_definition": (
                "Current source rows with exact PropertyType = Residential and "
                "Status = Closed, then exact City in {Temple, Belton}, CloseDate "
                "in the 30-day window, and a $25,000 close-price floor."
            ),
            "may_active_definition": (
                "Legacy first Matrix status block (rows 0:889), then exact City "
                "in {Temple, Belton} and a $25,000 current-price floor; the May "
                "export lacks Status and PropertyType."
            ),
            "may_comparison_caveat": (
                "The July current snapshot uses explicit status/property fields "
                "while the May baseline uses the legacy inferred first block. "
                "Changes are directional and not a same-method trend comparison."
            ),
            "active_block_boundaries": {
                "may_first_exclusive_row": MAY_ACTIVE_END,
            },
            "builder_definition": (
                "SpecialListingConditions contains Builder. BuilderName and "
                "YearBuilt are intentionally ignored."
            ),
            "price_cut_definition": "CurrentPrice < OriginalListPrice among rows with both values.",
            "record_floor": (
                "$25,000 minimum current price for active rows and close price "
                "for sold rows to remove lease rows and obvious non-sale records."
            ),
            "dedupe_key_for_history": "city + normalized address + CloseDate + ClosePrice",
            "long_run_source_separation": (
                "The long-run series stays anchored to the July 19 export through "
                "July 17. The July 20 exact-status export is not merged into "
                "history because the files omit MLS number and cannot be "
                "deduplicated reliably across exports."
            ),
            "history_sources": history_sources,
            "privacy": (
                "Aggregates only; AgentRemarks and identifying row-level fields "
                "are not emitted."
            ),
        },
        "current": current,
        "may_comparison": may,
        "change_from_may": changes,
        "ytd_through_july_17": annual_ytd(history),
        "data_quality": {
            "current_source_row_count": len(current_rows),
            "current_city_counts": Counter(
                str(row.get("City", "")).strip() for row in current_rows
            ),
            "current_status_counts": Counter(
                str(row.get("Status", "")).strip() for row in current_rows
            ),
            "current_property_type_counts": Counter(
                str(row.get("PropertyType", "")).strip() for row in current_rows
            ),
            "current_special_listing_conditions": Counter(
                str(row.get("SpecialListingConditions", "")).strip() for row in current_rows
            ),
            "history_closed_rows_after_dedupe": len(history),
            "filming_gate": (
                "CLEARED: the July 20 source includes Status and PropertyType; "
                "current active and closed claims use exact Residential status "
                "filters before the Temple/Belton post-filter."
            ),
            "remaining_source_limits": (
                "The export still omits MLS number, CDOM, and seller credits; DOM "
                "buckets are cross-sectional and medians remain mix-sensitive."
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
