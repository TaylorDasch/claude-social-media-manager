#!/usr/bin/env python3
"""Regression checks for the public Temple/Belton market-update claims."""

from __future__ import annotations

import unittest
from collections import Counter

import analyze_market as market


class MarketUpdateAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        current_rows = market.read_csv(market.CURRENT_PATH)
        may_rows = market.read_csv(market.MAY_PATH)
        cls.current_rows = current_rows
        cls.current_active = market.exact_status_rows(current_rows, "Active")
        cls.current_closed = market.exact_status_rows(current_rows, "Closed")
        cls.current = market.comparable_snapshot(
            cls.current_closed,
            cls.current_active,
            market.CURRENT_AS_OF,
            market.CURRENT_CLOSE_THROUGH,
        )
        cls.may = market.comparable_snapshot(
            may_rows,
            market.inferred_active_block(may_rows, market.MAY_ACTIVE_END),
            market.MAY_AS_OF,
            market.MAY_AS_OF,
        )
        history, cls.history_sources = market.historical_closed()
        cls.ytd = market.annual_ytd(history)

    def test_active_denominator_and_duplicate(self) -> None:
        summary = self.current["combined"]["active"]["all"]
        self.assertEqual(summary["row_count"], 870)
        self.assertEqual(summary["unique_address_count"], 869)
        self.assertEqual(summary["median_current_price"], 299440)
        self.assertEqual(summary["median_dom"], 69.5)
        self.assertEqual(summary["price_cut_count"], 486)
        self.assertEqual(summary["price_cut_share_pct"], 55.9)
        self.assertEqual(summary["median_price_cut_dollars"], 15000)
        self.assertEqual(summary["median_price_cut_pct"], 4.7)

    def test_dom_price_cut_hook(self) -> None:
        ladder = self.current["combined"]["active_dom_cut_ladder"]
        self.assertEqual(ladder["0_to_30"], {
            "row_count": 204,
            "price_cut_count": 28,
            "price_cut_share_pct": 13.7,
        })
        self.assertEqual(ladder["31_to_60"], {
            "row_count": 185,
            "price_cut_count": 84,
            "price_cut_share_pct": 45.4,
        })
        self.assertEqual(ladder["61_to_90"], {
            "row_count": 114,
            "price_cut_count": 76,
            "price_cut_share_pct": 66.7,
        })
        self.assertEqual(ladder["91_plus"], {
            "row_count": 367,
            "price_cut_count": 298,
            "price_cut_share_pct": 81.2,
        })
        self.assertEqual(ladder["121_plus"], {
            "row_count": 268,
            "price_cut_count": 218,
            "price_cut_share_pct": 81.3,
        })

    def test_may_comparison(self) -> None:
        summary = self.may["combined"]["active"]["all"]
        self.assertEqual(summary["row_count"], 889)
        self.assertEqual(summary["unique_address_count"], 888)
        self.assertEqual(summary["median_current_price"], 309900)
        self.assertEqual(summary["median_dom"], 71)
        self.assertEqual(summary["price_cut_share_pct"], 54.1)
        current = self.current["combined"]["active"]["all"]
        self.assertEqual(
            market.relative_change(current["row_count"], summary["row_count"]), -2.1
        )
        self.assertEqual(
            market.relative_change(
                current["median_current_price"], summary["median_current_price"]
            ),
            -3.4,
        )
        self.assertEqual(
            market.relative_change(current["median_dom"], summary["median_dom"]), -2.1
        )
        self.assertEqual(
            market.rounded(
                current["price_cut_share_pct"] - summary["price_cut_share_pct"], 1
            ),
            1.8,
        )

    def test_latest_closings_use_exact_closed_status(self) -> None:
        sold = self.current["combined"]["sold_30d"]["all"]
        self.assertEqual(sold["sale_count"], 200)
        self.assertEqual(sold["median_close_price"], 278670)
        self.assertEqual(sold["median_dom"], 50)
        self.assertEqual(sold["median_close_to_final_list_pct"], 99.76)
        self.assertEqual(sold["median_close_to_original_list_pct"], 97.01)
        self.assertEqual(sold["sold_below_final_list_count"], 103)
        self.assertEqual(sold["sold_below_final_list_share_pct"], 51.5)
        self.assertEqual(sold["sold_at_final_list_count"], 70)
        self.assertEqual(sold["sold_above_final_list_count"], 27)
        self.assertEqual(
            sold["sold_below_final_list_count"]
            + sold["sold_at_final_list_count"]
            + sold["sold_above_final_list_count"],
            sold["sale_count"],
        )

        segments = self.current["combined"]["sold_30d"]
        self.assertEqual(segments["builder"]["sale_count"], 54)
        self.assertEqual(segments["builder"]["median_dom"], 54.5)
        self.assertEqual(segments["resale"]["sale_count"], 146)
        self.assertEqual(segments["resale"]["median_dom"], 48)
        self.assertEqual(sold["builder_sale_share_pct"], 27.0)

    def test_builder_definition_and_share(self) -> None:
        active = self.current["combined"]["active"]
        self.assertEqual(active["builder"]["row_count"], 222)
        self.assertEqual(active["builder"]["median_dom"], 110)
        self.assertEqual(active["builder"]["price_cut_share_pct"], 44.1)
        self.assertEqual(active["resale"]["row_count"], 648)
        self.assertEqual(active["resale"]["median_dom"], 64)
        self.assertEqual(active["resale"]["price_cut_share_pct"], 59.9)
        self.assertEqual(active["all"]["builder_share_pct"], 25.5)

    def test_broad_source_has_required_fields_and_exact_filter(self) -> None:
        self.assertEqual(market.CURRENT_AS_OF.isoformat(), "2026-07-20")
        self.assertEqual(market.CURRENT_CLOSE_THROUGH.isoformat(), "2026-07-20")
        self.assertEqual(market.YTD_CLOSE_THROUGH.isoformat(), "2026-07-17")
        self.assertEqual(
            self.current["closed_window"], ["2026-06-21", "2026-07-20"]
        )
        self.assertEqual(len(self.current_rows), 3502)
        self.assertTrue({"Status", "PropertyType"}.issubset(self.current_rows[0]))
        self.assertEqual(
            Counter(row["PropertyType"].strip() for row in self.current_rows),
            Counter({"Residential": 3502}),
        )
        self.assertEqual(
            Counter(row["Status"].strip() for row in self.current_rows),
            Counter({
                "Coming Soon": 14,
                "Active": 1944,
                "Active Under Contract": 173,
                "Pending": 387,
                "Closed": 984,
            }),
        )
        cities = {row.get("City", "").strip() for row in self.current_rows}
        self.assertTrue(set(market.CITIES) < cities)
        self.assertTrue({"Killeen", "Salado", "Harker Heights"}.issubset(cities))
        self.assertEqual(len(self.current_active), 1944)
        self.assertEqual(len(self.current_closed), 984)
        target = [
            row
            for row in self.current_active
            if row.get("City", "").strip() in market.CITIES
        ]
        self.assertEqual(len(target), 870)
        self.assertTrue(all(row["Status"].strip() == "Active" for row in target))
        self.assertTrue(
            all(row["PropertyType"].strip() == "Residential" for row in target)
        )

    def test_city_active_summaries_and_ladders(self) -> None:
        expected = {
            "Temple": (618, 617, 285000, 69, 351, 56.8, 156, 25.2),
            "Belton": (252, 252, 349900, 73.5, 135, 53.6, 66, 26.2),
        }
        for city, values in expected.items():
            summary = self.current["cities"][city]["active"]["all"]
            self.assertEqual(
                (
                    summary["row_count"],
                    summary["unique_address_count"],
                    summary["median_current_price"],
                    summary["median_dom"],
                    summary["price_cut_count"],
                    summary["price_cut_share_pct"],
                    summary["builder_count"],
                    summary["builder_share_pct"],
                ),
                values,
            )
        self.assertEqual(
            tuple(
                self.current["cities"]["Temple"]["active_dom_cut_ladder"][key][
                    "price_cut_share_pct"
                ]
                for key in ("0_to_30", "31_to_60", "61_to_90", "91_plus")
            ),
            (14.9, 44.9, 68.9, 82.5),
        )
        self.assertEqual(
            tuple(
                self.current["cities"]["Belton"]["active_dom_cut_ladder"][key][
                    "price_cut_share_pct"
                ]
                for key in ("0_to_30", "31_to_60", "61_to_90", "91_plus")
            ),
            (11.1, 46.9, 58.3, 78.4),
        )

    def test_city_closing_summaries(self) -> None:
        temple = self.current["cities"]["Temple"]["sold_30d"]["all"]
        self.assertEqual(
            (
                temple["sale_count"],
                temple["median_close_price"],
                temple["median_dom"],
                temple["median_close_to_final_list_pct"],
                temple["median_close_to_original_list_pct"],
            ),
            (143, 273000, 52, 100.0, 96.99),
        )
        belton = self.current["cities"]["Belton"]["sold_30d"]["all"]
        self.assertEqual(
            (
                belton["sale_count"],
                belton["median_close_price"],
                belton["median_dom"],
                belton["median_close_to_final_list_pct"],
                belton["median_close_to_original_list_pct"],
            ),
            (57, 304335, 40, 99.59, 97.01),
        )

    def test_active_price_bands_and_temple_300s(self) -> None:
        bands = self.current["combined"]["active_by_price_band"]
        expected = {
            "under_200k": (96, 79, 62.5),
            "200k_to_299999": (348, 53.5, 55.2),
            "300k_to_399999": (204, 91.5, 56.9),
            "400k_to_499999": (87, 84, 48.3),
            "500k_plus": (135, 88, 56.3),
        }
        for label, values in expected.items():
            summary = bands[label]
            self.assertEqual(
                (
                    summary["row_count"],
                    summary["median_dom"],
                    summary["price_cut_share_pct"],
                ),
                values,
            )

        temple_active = self.current["cities"]["Temple"]["active_by_price_band"][
            "300k_to_399999"
        ]
        self.assertEqual(
            (
                temple_active["row_count"],
                temple_active["median_dom"],
                temple_active["price_cut_share_pct"],
            ),
            (133, 86, 60.9),
        )
        temple_sold = self.current["cities"]["Temple"]["sold_30d_by_price_band"][
            "300k_to_399999"
        ]
        self.assertEqual(
            (
                temple_sold["sale_count"],
                temple_sold["median_dom"],
                temple_sold["median_close_to_original_list_pct"],
            ),
            (31, 37, 99.73),
        )

    def test_long_run_series_stays_on_july_17_benchmark(self) -> None:
        self.assertIn(str(market.HISTORY_CURRENT_PATH), self.history_sources)
        self.assertNotIn(str(market.CURRENT_PATH), self.history_sources)
        prior = self.ytd["2025"]["combined"]
        current = self.ytd["2026"]["combined"]
        self.assertEqual(
            (prior["sale_count"], prior["median_close_price"], prior["median_dom"]),
            (1162, 289000, 66),
        )
        self.assertEqual(
            (
                current["sale_count"],
                current["median_close_price"],
                current["median_dom"],
            ),
            (1152, 285000, 69),
        )
        self.assertEqual(
            market.relative_change(current["sale_count"], prior["sale_count"]), -0.9
        )
        self.assertEqual(
            market.relative_change(
                current["median_close_price"], prior["median_close_price"]
            ),
            -1.4,
        )


if __name__ == "__main__":
    unittest.main()
