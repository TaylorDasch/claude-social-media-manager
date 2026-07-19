from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import newsletter_desk  # noqa: E402


CONTACT_HEADER = [
    "email",
    "first_name",
    "last_name",
    "audience",
    "consent_status",
    "consent_source",
    "consent_date",
    "tags",
    "notes",
]


class NewsletterContactTests(unittest.TestCase):
    def write_contacts(self, rows: list[list[str]]) -> Path:
        temp_dir = Path(tempfile.mkdtemp())
        path = temp_dir / "contacts.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(CONTACT_HEADER)
            writer.writerows(rows)
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        return path

    def test_valid_contact_is_active(self) -> None:
        path = self.write_contacts(
            [["buyer@example.com", "Ava", "Buyer", "temple-insider", "subscribed", "website form", "2026-07-01", "buyer", ""]]
        )
        report = newsletter_desk.validate_contacts(path)
        self.assertEqual([], report.errors)
        self.assertEqual(1, len(report.active))
        self.assertEqual("buyer@example.com", report.active[0].email)

    def test_duplicate_is_case_insensitive(self) -> None:
        path = self.write_contacts(
            [
                ["Buyer@Example.com", "A", "B", "temple-insider", "subscribed", "form", "2026-07-01", "", ""],
                ["buyer@example.com", "A", "B", "temple-insider", "subscribed", "form", "2026-07-01", "", ""],
            ]
        )
        report = newsletter_desk.validate_contacts(path)
        self.assertTrue(any("duplicate email + audience" in error for error in report.errors))

    def test_inactive_contact_is_never_in_payload(self) -> None:
        path = self.write_contacts(
            [["old@example.com", "Old", "Contact", "investor-brief", "unsubscribed", "", "", "", ""]]
        )
        report = newsletter_desk.validate_contacts(path)
        payload = newsletter_desk.subscription_payload(report.active)
        self.assertEqual([], report.errors)
        self.assertEqual([], payload["subscriptions"])

    def test_active_contact_requires_consent_record(self) -> None:
        path = self.write_contacts(
            [["buyer@example.com", "A", "B", "temple-insider", "subscribed", "", "", "", ""]]
        )
        report = newsletter_desk.validate_contacts(path)
        self.assertEqual(2, len(report.errors[0].split(",")))
        self.assertIn("missing consent_source", report.errors[0])
        self.assertIn("missing consent_date", report.errors[0])


class NewsletterIssueTests(unittest.TestCase):
    def valid_source(self) -> str:
        return """---
newsletter: temple-insider
issue_type: market-update
subject: Temple vs Belton: what Zillow misses
preview_text: The same-priced house can carry a different tax bill, MUD layer, school zone, or commute.
send_date: 2026-07-23
data_sources: BellCAD 2025 rates; MLS 2026-07 pull
---

# The first number is not the last number

Taylor Dasch with EG Realty here in Temple. Here is the buyer decision in plain English.

## The honest comparison

Use the exact address, tax entities, commute, and insurance checks before deciding.

- Check the taxing entities.
- Check the parcel.

Read the [Temple vs Belton comparison](https://templetxhomes.net/temple-vs-belton/?utm_source=beehiiv).
"""

    def test_issue_build_writes_all_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            source = temp_path / "issue.md"
            output = temp_path / "built"
            source.write_text(self.valid_source(), encoding="utf-8")
            result = newsletter_desk.main(
                ["issue", "build", str(source), "--output-dir", str(output)]
            )
            self.assertEqual(0, result)
            self.assertEqual(
                {"email.html", "preview.html", "plain.txt", "manifest.json"},
                {path.name for path in output.iterdir()},
            )
            manifest = (output / "manifest.json").read_text(encoding="utf-8")
            self.assertIn('"delivery_status": "NOT_SENT"', manifest)
            self.assertIn("Do not mass-send", (output / "email.html").read_text(encoding="utf-8"))

    def test_subject_over_50_characters_is_blocked(self) -> None:
        metadata, body = newsletter_desk.parse_frontmatter(
            self.valid_source().replace(
                "Temple vs Belton: what Zillow misses",
                "This subject line is intentionally much longer than fifty characters total",
            )
        )
        errors = newsletter_desk.issue_errors(metadata, body)
        self.assertTrue(any("maximum is 50" in error for error in errors))

    def test_specific_site_link_is_required(self) -> None:
        metadata, body = newsletter_desk.parse_frontmatter(
            self.valid_source().replace(
                "https://templetxhomes.net/temple-vs-belton/?utm_source=beehiiv",
                "https://templetxhomes.net/",
            )
        )
        errors = newsletter_desk.issue_errors(metadata, body)
        self.assertTrue(any("specific templetxhomes.net page" in error for error in errors))

    def test_issue_type_cannot_use_the_wrong_audience(self) -> None:
        metadata, body = newsletter_desk.parse_frontmatter(
            self.valid_source().replace(
                "newsletter: temple-insider",
                "newsletter: investor-brief",
            )
        )
        errors = newsletter_desk.issue_errors(metadata, body)
        self.assertIn(
            "market-update issues must use the temple-insider audience",
            errors,
        )

    def test_unresolved_template_placeholder_is_blocked(self) -> None:
        metadata, body = newsletter_desk.parse_frontmatter(
            self.valid_source().replace(
                "Use the exact address",
                "Use the exact {{ADDRESS}}",
            )
        )
        errors = newsletter_desk.issue_errors(metadata, body)
        self.assertIn("Unresolved template placeholders remain", errors)

    def test_dedicated_templates_only_need_content_filled(self) -> None:
        for filename in (
            "market-update.template.md",
            "investor-analysis.template.md",
        ):
            with self.subTest(filename=filename):
                source = (PROJECT_ROOT / "newsletter" / "issues" / filename).read_text(
                    encoding="utf-8"
                )
                metadata, body = newsletter_desk.parse_frontmatter(source)
                self.assertEqual(
                    ["Unresolved template placeholders remain"],
                    newsletter_desk.issue_errors(metadata, body),
                )


class NewsletterFubTests(unittest.TestCase):
    def test_fub_classification_prioritizes_investor_signal(self) -> None:
        audience, reason = newsletter_desk.classify_fub_row(
            {
                "Tags": "_ai-outreach-ok, Buyer, Investor, BiggerPockets",
                "Stage": "Lead",
                "Lead Source": "BiggerPockets",
            }
        )
        self.assertEqual("investor-brief", audience)
        self.assertEqual("investor_signal", reason)

    def test_fub_suppression_blocks_candidate(self) -> None:
        audience, reason = newsletter_desk.classify_fub_row(
            {
                "Tags": "_ai-outreach-ok, Buyer, Bounced",
                "Stage": "Lead",
                "Lead Source": "Website",
            }
        )
        self.assertIsNone(audience)
        self.assertEqual("suppressed", reason)

    def test_pending_review_is_valid_but_not_importable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "contacts.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(CONTACT_HEADER)
                writer.writerow(
                    [
                        "buyer@example.com",
                        "A",
                        "B",
                        "temple-insider",
                        "pending_review",
                        "",
                        "",
                        "",
                        "",
                    ]
                )
            report = newsletter_desk.validate_contacts(path)
            self.assertEqual([], report.errors)
            self.assertEqual([], report.active)

    def test_reconcile_never_recommends_reimport_for_inactive(self) -> None:
        rows = [
            {
                "email": "old@example.com",
                "audience": "investor-brief",
                "consent_status": "pending_review",
            }
        ]
        reconciled, counts = newsletter_desk.reconcile_candidate_rows(
            rows,
            {
                "investor-brief": {"old@example.com": "inactive"},
                "temple-insider": {},
            },
        )
        self.assertEqual("do_not_import_existing_inactive", reconciled[0]["recommended_action"])
        self.assertEqual(1, counts["existing_inactive"])

    def test_relationship_priority_wins_over_cold_source(self) -> None:
        candidate = {
            "recommended_action": "review_permission_before_import",
            "tags": "Past Client, Buyer",
            "fub_stage": "Lead",
            "fub_lead_source": "Door Knocking",
            "fub_date_added": "2023-10-01",
        }
        tier, action, _ = newsletter_desk.filter_fub_candidate(
            candidate,
            {"Deal Close Date": "2024-02-01", "Is Contacted": "Yes"},
            date(2025, 7, 18),
        )
        self.assertEqual("relationship_priority", tier)
        self.assertEqual("review_permission", action)

    def test_recent_uncontacted_candidate_stays_in_review(self) -> None:
        candidate = {
            "recommended_action": "review_permission_before_import",
            "tags": "Buyer",
            "fub_stage": "Lead",
            "fub_lead_source": "templetxhomes.net",
            "fub_date_added": "2026-01-12",
        }
        tier, action, _ = newsletter_desk.filter_fub_candidate(
            candidate,
            {"Deal Close Date": "", "Is Contacted": "No"},
            date(2025, 7, 18),
        )
        self.assertEqual("recent_inbound_review", tier)
        self.assertEqual("review_permission", action)

    def test_old_uncontacted_candidate_is_held_out(self) -> None:
        candidate = {
            "recommended_action": "review_permission_before_import",
            "tags": "Buyer",
            "fub_stage": "Lead",
            "fub_lead_source": "Market Leader",
            "fub_date_added": "2023-10-01",
        }
        tier, action, _ = newsletter_desk.filter_fub_candidate(
            candidate,
            {"Deal Close Date": "", "Is Contacted": "No"},
            date(2025, 7, 18),
        )
        self.assertEqual("older_uncontacted_hold", tier)
        self.assertEqual("exclude_from_import", action)

    def test_existing_inactive_candidate_is_hard_excluded(self) -> None:
        candidate = {
            "recommended_action": "do_not_import_existing_inactive",
            "tags": "Investor",
            "fub_stage": "Lead",
            "fub_lead_source": "BiggerPockets",
            "fub_date_added": "2026-01-12",
        }
        tier, action, _ = newsletter_desk.filter_fub_candidate(
            candidate,
            {"Deal Close Date": "", "Is Contacted": "Yes"},
            date(2025, 7, 18),
        )
        self.assertEqual("hard_exclude_beehiiv", tier)
        self.assertEqual("exclude_from_import", action)

    def test_manual_curation_checks_row_identity_and_keeps_removal_recoverable(self) -> None:
        rows = [
            {"email": "keep@example.com", "fub_id": "1"},
            {"email": "remove@example.com", "fub_id": "2"},
        ]
        decisions = {
            "decision_date": "2026-07-18",
            "row_number_basis": "csv_header_is_row_1",
            "remove": [{"spreadsheet_row": 3, "expected_fub_id": "2"}],
            "add": [
                {
                    "email": "new@example.com",
                    "first_name": "New",
                    "last_name": "Buyer",
                    "audience": "temple-insider",
                    "source_id": "gmail:test",
                    "review_tier": "relationship_priority",
                }
            ],
        }
        curated, removed, additions = newsletter_desk.curate_review_rows(rows, decisions)
        self.assertEqual(["keep@example.com", "new@example.com"], [r["email"] for r in curated])
        self.assertEqual("remove@example.com", removed[0]["email"])
        self.assertEqual("3", removed[0]["original_spreadsheet_row"])
        self.assertEqual("pending_review", additions[0]["consent_status"])
        self.assertEqual("relationship_priority", additions[0]["review_tier"])

    def test_manual_curation_blocks_shifted_row_number(self) -> None:
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            newsletter_desk.curate_review_rows(
                [{"email": "buyer@example.com", "fub_id": "1"}],
                {
                    "row_number_basis": "csv_header_is_row_1",
                    "remove": [{"spreadsheet_row": 2, "expected_fub_id": "wrong"}],
                },
            )


if __name__ == "__main__":
    unittest.main()
