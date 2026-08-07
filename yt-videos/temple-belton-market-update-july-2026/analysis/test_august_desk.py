#!/usr/bin/env python3
"""Regression checks for the August desk-film packet."""

from __future__ import annotations

import unittest
from pathlib import Path
import re

import analyze_august_desk as august


PACKAGE_ROOT = Path(__file__).resolve().parent.parent


class AugustDeskAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = august.build()
        cls.combined = cls.result["snapshot"]["combined"]

    def test_source_reconciliation(self) -> None:
        quality = self.result["source_quality"]
        self.assertEqual(quality["row_count"], 3250)
        self.assertEqual(quality["city_counts"], {"Temple": 2275, "Belton": 975})
        self.assertEqual(
            quality["status_counts"],
            {
                "Closed": 2145,
                "Active": 883,
                "Pending": 155,
                "Active Under Contract": 62,
                "Coming Soon": 5,
            },
        )
        self.assertEqual(quality["property_type_counts"], {"Residential": 3250})

    def test_active_snapshot(self) -> None:
        active = self.combined["active"]["all"]
        self.assertEqual(active["row_count"], 883)
        self.assertEqual(active["unique_address_count"], 882)
        self.assertEqual(active["median_current_price"], 299000)
        self.assertEqual(active["median_dom"], 68)
        self.assertEqual(active["price_cut_count"], 485)
        self.assertEqual(active["price_cut_share_pct"], 54.9)

    def test_listing_age_price_cut_staircase(self) -> None:
        ladder = self.combined["active_dom_cut_ladder"]
        expected = {
            "0_to_30": (233, 32, 13.7),
            "31_to_60": (162, 83, 51.2),
            "61_to_90": (141, 93, 66.0),
            "91_plus": (347, 277, 79.8),
        }
        for key, values in expected.items():
            item = ladder[key]
            self.assertEqual(
                (
                    item["row_count"],
                    item["price_cut_count"],
                    item["price_cut_share_pct"],
                ),
                values,
            )

    def test_latest_closing_guardrail(self) -> None:
        sold = self.combined["sold_30d"]["all"]
        self.assertEqual(sold["sale_count"], 168)
        self.assertEqual(sold["median_dom"], 55.5)
        self.assertEqual(sold["median_close_to_original_list_pct"], 95.73)
        self.assertEqual(sold["median_close_to_final_list_pct"], 99.48)
        self.assertEqual(sold["sold_below_final_list_share_pct"], 53.0)

    def test_ytd_guardrail(self) -> None:
        change = self.result["ytd"]["combined_change"]
        self.assertEqual(change["sale_count_pct"], 0.7)
        self.assertEqual(change["median_close_price_pct"], -1.3)
        self.assertEqual(change["median_dom_days"], 3)

    def test_packet_claims_and_copy(self) -> None:
        packet = (PACKAGE_ROOT / "DESK-FILM-PACKET-2026-08-06.md").read_text()
        for claim in (
            "233 | 32 | 13.7%",
            "162 | 83 | 51.2%",
            "141 | 93 | 66.0%",
            "347 | 277 | 79.8%",
            "median close/original-list relationship: 95.73%",
            "median close/final-list relationship: 99.48%",
            "Taylor Dasch with EG Realty",
            "https://calendly.com/dealswithdasch",
        ):
            self.assertIn(claim, packet)
        self.assertNotIn("July 20, 2026", packet)
        self.assertNotIn("81.2%", packet)
        banned = re.compile(
            r"\b(turnkey|dream home|white glove|nestled|charming|stunning|"
            r"sought-after|boasts|utilize|comprehensive|furthermore|moreover|"
            r"unparalleled|vibrant community|hidden gem|welcome home|"
            r"perfect neighborhood|must-see)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(banned.search(packet))


if __name__ == "__main__":
    unittest.main()
