"""Smoke + unit tests for the SMM CLI.

Runs in an isolated temp DB so real `data/drafts.db` is never touched.
No external APIs. stdlib + unittest only.

Usage:
    cd ~/claude-social-media-manager
    python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Put repo root on sys.path so `smm` and `cli` are importable.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


class SmmTestBase(unittest.TestCase):
    """Base that points SMM_DB_PATH at a throwaway temp dir."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="smm-test-"))
        self.db_path = self.tmpdir / "drafts.db"
        os.environ["SMM_DB_PATH"] = str(self.db_path)

        # Reset any cached db modules so they pick up SMM_DB_PATH
        for mod in list(sys.modules):
            if mod.startswith("smm"):
                del sys.modules[mod]

        from smm.db import init_db
        init_db()

    def tearDown(self):
        os.environ.pop("SMM_DB_PATH", None)
        shutil.rmtree(self.tmpdir, ignore_errors=True)


# ---------- DB / intake ----------

class TestIntake(SmmTestBase):

    def test_add_and_list(self):
        from smm import intake
        from smm.models import Intake
        item = Intake(source_type="manual", source_title="Test Idea",
                      raw_input="BSW residents need a commute map.",
                      audience="bsw_relocation", funnel_stage="education")
        ident = intake.add_intake(item)
        self.assertTrue(ident.startswith("intk_"))
        rows = intake.list_intake()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["audience"], "bsw_relocation")
        self.assertEqual(rows[0]["source_title"], "Test Idea")

    def test_filter_by_status(self):
        from smm import intake
        from smm.models import Intake
        a = Intake(source_type="manual", raw_input="a", audience="investor")
        b = Intake(source_type="manual", raw_input="b", audience="investor")
        intake.add_intake(a)
        intake.add_intake(b)
        intake.update_intake_status(a.id, "closed")
        new_only = intake.list_intake(status="new")
        closed_only = intake.list_intake(status="closed")
        self.assertEqual(len(new_only), 1)
        self.assertEqual(len(closed_only), 1)


# ---------- Compliance ----------

class TestCompliance(SmmTestBase):

    def test_banned_phrase_hard(self):
        from smm import compliance
        flags = compliance.check_text(
            "Welcome home to this charming dream home!",
            platform="instagram_caption",
        )
        self.assertTrue(compliance.has_hard_violation(flags))
        rules = {f.rule for f in flags}
        self.assertIn("banned_phrase", rules)

    def test_fort_cavazos_hard(self):
        from smm import compliance
        flags = compliance.check_text(
            "Great option for buyers PCS-ing to Fort Cavazos.",
            platform="facebook_business",
        )
        self.assertTrue(compliance.has_hard_violation(flags))
        self.assertTrue(any(f.match == "fort cavazos" for f in flags))

    def test_tiktok_investor_leak_hard(self):
        from smm import compliance
        flags = compliance.check_text(
            "Here's the cap rate math on a Temple rental (DSCR 1.15).",
            platform="tiktok",
        )
        self.assertTrue(compliance.has_hard_violation(flags))
        self.assertTrue(any(f.rule == "audience_lane_leak" for f in flags))

    def test_tiktok_investor_leak_allowed_on_linkedin(self):
        from smm import compliance
        flags = compliance.check_text(
            "Here's the cap rate math on a Temple rental (DSCR 1.15).",
            platform="linkedin",
        )
        rules = {f.rule for f in flags}
        self.assertNotIn("audience_lane_leak", rules)

    def test_newsletter_temple_insider_lane_gate(self):
        from smm import compliance
        flags = compliance.check_text(
            "Temple Insider subscribers — here's the cap rate math on a rental comp.",
            platform="newsletter_temple_insider",
        )
        self.assertTrue(compliance.has_hard_violation(flags))
        self.assertTrue(any(f.rule == "audience_lane_leak" for f in flags))

    def test_newsletter_investor_brief_allows_investor_terms(self):
        from smm import compliance
        flags = compliance.check_text(
            "Investor Brief — here's the cap rate math (verify current rate).",
            platform="newsletter_investor_brief",
        )
        rules = {f.rule for f in flags}
        self.assertNotIn("audience_lane_leak", rules)

    def test_broker_rule_hard(self):
        from smm import compliance
        flags = compliance.check_text(
            "Taylor is a broker at EG Realty.",
            platform="linkedin",
        )
        self.assertTrue(any(f.rule == "broker_rule" for f in flags))

    def test_guaranteed_return_hard(self):
        from smm import compliance
        flags = compliance.check_text(
            "This property has guaranteed appreciation and guaranteed return.",
            platform="linkedin",
        )
        self.assertTrue(compliance.has_hard_violation(flags))
        self.assertTrue(any(f.rule == "guaranteed_return" for f in flags))

    def test_steering_soft(self):
        from smm import compliance
        flags = compliance.check_text(
            "This is the perfect neighborhood for families.",
            platform="facebook_business",
        )
        soft = [f for f in flags if f.severity == "soft"]
        self.assertTrue(any(f.rule == "fair_housing_steering" for f in soft))

    def test_school_claim_soft(self):
        from smm import compliance
        flags = compliance.check_text(
            "This area has great schools and everyone loves it.",
            platform="instagram_caption",
        )
        self.assertTrue(any(f.rule == "school_claim_unverified" for f in flags))

    def test_school_claim_ok_with_disclaimer(self):
        from smm import compliance
        flags = compliance.check_text(
            "This area has great schools — verify by address since boundaries change.",
            platform="instagram_caption",
        )
        self.assertFalse(any(f.rule == "school_claim_unverified" for f in flags))

    def test_tax_claim_soft(self):
        from smm import compliance
        flags = compliance.check_text(
            "Bell County effective property tax is ~2.18%.",
            platform="linkedin",
        )
        self.assertTrue(any(f.rule == "tax_claim_unverified" for f in flags))

    def test_tax_claim_ok_with_disclaimer(self):
        from smm import compliance
        flags = compliance.check_text(
            "Bell County effective property tax is ~2.18% (verify current rate).",
            platform="linkedin",
        )
        self.assertFalse(any(f.rule == "tax_claim_unverified" for f in flags))

    def test_clean_copy_zero_flags(self):
        from smm import compliance
        flags = compliance.check_text(
            "Temple's 76502 Power Zip ranks 753/1000. Taylor Dasch with EG Realty.",
            platform="linkedin",
            public_facing=False,  # skip entity check for short form
        )
        self.assertEqual(len(flags), 0)


# ---------- Drafts + approval ----------

class TestDraftFlow(SmmTestBase):

    def _make_clean_draft(self):
        from smm import drafts
        from smm.models import Draft
        d = Draft(
            platform="linkedin",
            body="Temple median is $247K; Bell County effective tax is ~2.18% (verify current rate). Underwrite conservatively. Taylor Dasch with EG Realty.",
            selected_hook="Temple math that kills lazy investor analysis",
            cta="DM for deal analyzer.",
            status="needs_review",
        )
        return drafts.add_draft(d)

    def _make_hard_violation_draft(self):
        from smm import drafts
        from smm.models import Draft
        d = Draft(
            platform="facebook_business",
            body="Welcome home to this charming gem nestled in Fort Cavazos. Taylor is a broker.",
            status="needs_review",
        )
        return drafts.add_draft(d)

    def test_draft_created_and_compliance_run(self):
        draft_id = self._make_clean_draft()
        from smm import drafts
        d = drafts.get_draft(draft_id)
        self.assertIsNotNone(d)
        self.assertEqual(d.platform, "linkedin")
        # compliance ran
        self.assertIsInstance(d.compliance_flags, list)

    def test_approve_blocked_on_hard_violation(self):
        draft_id = self._make_hard_violation_draft()
        from smm import approval
        ok, msg = approval.approve(draft_id)
        self.assertFalse(ok)
        self.assertIn("Blocked", msg)

    def test_approve_force_override(self):
        draft_id = self._make_hard_violation_draft()
        from smm import approval
        ok, _ = approval.approve(draft_id, force=True, note="forced in test")
        self.assertTrue(ok)
        from smm.drafts import get_draft
        d = get_draft(draft_id)
        self.assertEqual(d.status, "approved")

    def test_approve_clean_draft(self):
        draft_id = self._make_clean_draft()
        from smm import approval
        ok, _ = approval.approve(draft_id)
        self.assertTrue(ok)

    def test_reject_and_history(self):
        draft_id = self._make_clean_draft()
        from smm import approval, drafts
        approval.reject(draft_id, note="wrong audience")
        d = drafts.get_draft(draft_id)
        self.assertEqual(d.status, "rejected")
        hist = drafts.approval_history(draft_id)
        self.assertEqual(len(hist), 2)  # created + rejected
        self.assertEqual(hist[-1]["to_status"], "rejected")

    def test_edit_reruns_compliance(self):
        draft_id = self._make_clean_draft()
        from smm import drafts
        drafts.edit_draft(draft_id, body="Welcome home to this charming dream home!")
        d = drafts.get_draft(draft_id)
        self.assertGreater(len(d.compliance_flags), 0)
        hard = [f for f in d.compliance_flags if f.get("severity") == "hard"]
        self.assertTrue(hard)

    def test_scheduled_and_posted_transitions(self):
        draft_id = self._make_clean_draft()
        from smm import approval, drafts
        approval.approve(draft_id)
        approval.mark_scheduled(draft_id, note="scheduled in Postiz")
        approval.mark_posted(draft_id, note="live")
        d = drafts.get_draft(draft_id)
        self.assertEqual(d.status, "posted")
        hist = drafts.approval_history(draft_id)
        states = [h["to_status"] for h in hist]
        self.assertEqual(states, ["needs_review", "approved", "scheduled", "posted"])

    def test_import_file_as_draft(self):
        tmp_file = Path(os.environ["SMM_DB_PATH"]).parent / "skill-output.md"
        tmp_file.write_text(
            "Temple's 76502 median is $247K. Taylor Dasch with EG Realty.\n",
            encoding="utf-8",
        )
        from smm import drafts
        draft_id = drafts.import_file_as_draft(tmp_file, platform="linkedin")
        d = drafts.get_draft(draft_id)
        self.assertEqual(d.platform, "linkedin")
        self.assertEqual(d.source_path, str(tmp_file))


# ---------- Exporters ----------

class TestExporters(SmmTestBase):

    def test_csv_export(self):
        from smm import approval, drafts
        from smm.models import Draft
        from smm.exporters import export_approved_csv
        d = Draft(platform="linkedin", body="Clean copy. Taylor Dasch with EG Realty.",
                  status="needs_review")
        drafts.add_draft(d)
        approval.approve(d.id, force=True)
        out = self.tmpdir / "out.csv"
        path = export_approved_csv(out_path=out)
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn(d.id, content)
        self.assertIn("linkedin", content)

    def test_json_export(self):
        from smm import approval, drafts
        from smm.models import Draft
        from smm.exporters import export_approved_json
        d = Draft(platform="gmb", body="Temple data point.", status="needs_review")
        drafts.add_draft(d)
        approval.approve(d.id, force=True)
        out = self.tmpdir / "out.json"
        path = export_approved_json(out_path=out)
        payload = json.loads(path.read_text())
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["platform"], "gmb")


# ---------- Integrations (stubs) ----------

class TestIntegrations(SmmTestBase):

    def test_postiz_no_creds(self):
        os.environ.pop("POSTIZ_API_URL", None)
        os.environ.pop("POSTIZ_API_KEY", None)
        from smm.integrations.postiz import push
        r = push()
        self.assertFalse(r["ok"])
        self.assertIn("reason", r)

    def test_ayrshare_no_creds(self):
        os.environ.pop("AYRSHARE_API_KEY", None)
        from smm.integrations.ayrshare import push
        r = push()
        self.assertFalse(r["ok"])

    def test_buffer_no_creds(self):
        os.environ.pop("BUFFER_ACCESS_TOKEN", None)
        from smm.integrations.buffer import push
        r = push()
        self.assertFalse(r["ok"])

    def test_csv_integration(self):
        from smm import approval, drafts
        from smm.models import Draft
        from smm.integrations.csv_export import push
        d = Draft(platform="linkedin", body="Clean copy.", status="needs_review")
        drafts.add_draft(d)
        approval.approve(d.id, force=True)
        r = push(out_path=self.tmpdir / "int.csv")
        self.assertTrue(r["ok"])
        self.assertEqual(r["mode"], "csv")
        self.assertTrue(Path(r["path"]).exists())


# ---------- Calendar ----------

class TestCalendar(SmmTestBase):

    def test_weekly_snapshot_shape(self):
        from smm.calendar import weekly_snapshot
        snap = weekly_snapshot()
        self.assertIn("week", snap)
        self.assertIn("counts", snap)
        for k in ("pending", "approved", "scheduled", "posted"):
            self.assertIn(k, snap["counts"])

    def test_registry_gaps_shape(self):
        from smm.calendar import content_registry_gaps
        gaps = content_registry_gaps()
        for k in ("idea", "draft", "refresh_due"):
            self.assertIn(k, gaps)
            self.assertIsInstance(gaps[k], list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
