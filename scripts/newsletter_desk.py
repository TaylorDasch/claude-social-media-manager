#!/usr/bin/env python3
"""Chat-first Newsletter Desk for Taylor Dasch.

The local workspace is the authoring and review surface. Beehiiv remains the
delivery layer for consent state, unsubscribe handling, bounces, and analytics.

Safety defaults:
- Contact operations validate only unless ``sync --live`` is explicit.
- A live import requires the exact confirmation phrase.
- Existing unsubscribes are never reactivated.
- This tool never sends or publishes an issue.
- Generated HTML is for Beehiiv staging, not direct Gmail mass sends.

Examples:
  python3 scripts/newsletter_desk.py contacts validate newsletter/private/contacts.csv
  python3 scripts/newsletter_desk.py issue build newsletter/issues/weekly.template.md
  python3 scripts/newsletter_desk.py status --live

Live contact import (after Taylor reviews the validation report):
  python3 scripts/newsletter_desk.py contacts sync newsletter/private/contacts.csv \
    --audience temple-insider --live --confirm IMPORT_CONSENTED_CONTACTS
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

from common import PROJECT_ROOT, load_banned_words, warn


AUDIENCES = {
    "temple-insider": {
        "name": "Temple TX Insider",
        "publication_env": "BEEHIIV_TEMPLE_TX_INSIDER_PUBLICATION_ID",
    },
    "investor-brief": {
        "name": "Temple TX Investor Brief",
        "publication_env": "BEEHIIV_INVESTOR_BRIEF_PUBLICATION_ID",
    },
}
ISSUE_TYPES = {
    "market-update": "temple-insider",
    "leverage-list": "temple-insider",
    "investor-analysis": "investor-brief",
}
ISSUE_TYPE_NAMES = {
    "leverage-list": "The Leverage List",
}
LEVERAGE_SELECTION_MODES = {"codex-pick", "taylor-pick"}
LEVERAGE_APPROVAL_STATUSES = {
    "awaiting_taylor_final_approval",
    "taylor_final_approval_recorded",
}
LEVERAGE_SUPPRESSION_STATE = "verified-issue-01-excluded"
LEVERAGE_CADENCE_ANCHOR = date(2026, 8, 18)
LEVERAGE_SEND_TIME_LOCAL = "10:00"
LEVERAGE_TIMEZONE = "America/Chicago"
CONTACT_COLUMNS = {
    "email",
    "first_name",
    "last_name",
    "audience",
    "consent_status",
    "consent_source",
    "consent_date",
    "tags",
    "notes",
}
ACTIVE_CONSENT_STATUS = "subscribed"
KNOWN_CONSENT_STATUSES = {
    "pending_review",
    "subscribed",
    "unsubscribed",
    "bounced",
    "complained",
}
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
CONFIRM_IMPORT = "IMPORT_CONSENTED_CONTACTS"
CONFIRM_CURATION = "APPLY_CONTACT_CURATION"
USER_AGENT = "taylor-newsletter-desk/1.0"
FUB_DIRECT_SOURCES = {
    "calendly",
    "google",
    "kw app/site",
    "market leader",
    "open house",
    "opcity",
    "realtor.com",
    "sphere",
    "templetxhomes.net",
    "website",
    "youtube",
    "zillow",
}
FUB_SUPPRESSION_SIGNALS = {
    "_no-ai-outreach",
    "bad email",
    "bounced",
    "complained",
    "deceased",
    "dnc-do-not-call",
    "spam",
    "unsubscrib",
}
FUB_INVESTOR_SIGNALS = {
    "bigger pockets",
    "biggerpockets",
    "buy-and-hold",
    "duplex-buyer",
    "investor",
    "loopnet",
    "midterm rental",
    "mtr",
    "oos_investor",
}
FUB_BUYER_SIGNALS = {
    "bsw",
    "buyer",
    "military",
    "open house",
    "past client",
    "pcs-plan",
    "relocation",
}
FUB_RELATIONSHIP_SIGNALS = {
    "_past-client-nurture",
    "past client",
    "sphere",
}
FUB_COLD_SOURCE_SIGNALS = {
    "door knocking",
    "expired listing",
    "propstream",
    "tax delinquent",
    "withdrawn",
}
FUB_REVIEW_TIERS = {
    "relationship_priority",
    "contacted_lead_review",
    "recent_inbound_review",
}


@dataclass(frozen=True)
class Contact:
    email: str
    first_name: str
    last_name: str
    audience: str
    consent_status: str
    consent_source: str
    consent_date: str
    tags: str
    notes: str
    line_number: int


@dataclass
class ContactReport:
    contacts: list[Contact]
    errors: list[str]
    warnings: list[str]

    @property
    def active(self) -> list[Contact]:
        return [c for c in self.contacts if c.consent_status == ACTIVE_CONSENT_STATUS]


def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE entries without printing or overwriting secrets."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value[:1] in {'"', "'"} and value[-1:] == value[:1]:
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


def validate_contacts(path: Path, audience: str | None = None) -> ContactReport:
    errors: list[str] = []
    warnings: list[str] = []
    contacts: list[Contact] = []
    seen: set[tuple[str, str]] = set()

    if not path.exists():
        return ContactReport([], [f"File not found: {path}"], [])

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        actual_columns = set(reader.fieldnames or [])
        missing = sorted(CONTACT_COLUMNS - actual_columns)
        if missing:
            return ContactReport([], [f"Missing CSV columns: {', '.join(missing)}"], [])

        for line_number, row in enumerate(reader, start=2):
            email_value = (row.get("email") or "").strip().lower()
            row_audience = (row.get("audience") or "").strip().lower()
            status = (row.get("consent_status") or "").strip().lower()
            consent_source = (row.get("consent_source") or "").strip()
            consent_date = (row.get("consent_date") or "").strip()
            row_errors: list[str] = []

            if not EMAIL_RE.fullmatch(email_value):
                row_errors.append("invalid email")
            if row_audience not in AUDIENCES:
                row_errors.append("invalid audience")
            if audience and row_audience != audience:
                continue
            if status not in KNOWN_CONSENT_STATUSES:
                row_errors.append("invalid consent_status")
            if status == ACTIVE_CONSENT_STATUS:
                if not consent_source:
                    row_errors.append("missing consent_source")
                if not consent_date:
                    row_errors.append("missing consent_date")
                else:
                    try:
                        parsed = date.fromisoformat(consent_date)
                        if parsed > date.today():
                            row_errors.append("consent_date is in the future")
                    except ValueError:
                        row_errors.append("consent_date must be YYYY-MM-DD")

            key = (email_value, row_audience)
            if email_value and row_audience and key in seen:
                row_errors.append("duplicate email + audience")
            seen.add(key)

            if row_errors:
                errors.append(f"Line {line_number}: {', '.join(row_errors)}")
                continue

            contacts.append(
                Contact(
                    email=email_value,
                    first_name=(row.get("first_name") or "").strip(),
                    last_name=(row.get("last_name") or "").strip(),
                    audience=row_audience,
                    consent_status=status,
                    consent_source=consent_source,
                    consent_date=consent_date,
                    tags=(row.get("tags") or "").strip(),
                    notes=(row.get("notes") or "").strip(),
                    line_number=line_number,
                )
            )

    inactive = len(contacts) - len([c for c in contacts if c.consent_status == ACTIVE_CONSENT_STATUS])
    if inactive:
        warnings.append(f"{inactive} pending/inactive/suppressed contact(s) will not be imported")
    if not contacts and not errors:
        warnings.append("Contact file has headers but no rows")
    return ContactReport(contacts, errors, warnings)


def print_contact_report(report: ContactReport) -> None:
    by_audience = {
        slug: len([c for c in report.active if c.audience == slug]) for slug in AUDIENCES
    }
    print("Newsletter contact validation")
    print(f"  Valid active contacts: {len(report.active)}")
    for slug, count in by_audience.items():
        print(f"  {slug}: {count}")
    print(f"  Errors: {len(report.errors)}")
    for message in report.errors:
        print(f"  ERROR {message}")
    for message in report.warnings:
        print(f"  WARN  {message}")


def beehiiv_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }


def request_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    payload: dict | None = None,
) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        # Beehiiv bulk errors may echo submitted addresses. Never place the
        # response body in stderr, logs, or a release artifact.
        code = exc.code
        exc.close()
        raise RuntimeError(f"Beehiiv HTTP {code}; response details suppressed") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Beehiiv connection failed: {exc.reason}") from exc


def subscription_payload(contacts: Iterable[Contact]) -> dict:
    return {
        "subscriptions": [
            {
                "email": contact.email,
                "reactivate_existing": False,
                "send_welcome_email": False,
                "utm_source": "codex-newsletter-desk",
                "utm_medium": "consented-contact-import",
                "utm_campaign": f"newsletter-list-{date.today().isoformat()}",
            }
            for contact in contacts
        ]
    }


def split_fub_tags(value: str) -> set[str]:
    return {
        tag.strip().lower()
        for tag in value.replace(";", ",").split(",")
        if tag.strip()
    }


def has_signal(tags: set[str], signals: set[str]) -> bool:
    blob = " | ".join(tags)
    return any(signal in blob for signal in signals)


def classify_fub_row(row: dict[str, str]) -> tuple[str | None, str]:
    """Return a proposed audience and a non-sensitive classification reason.

    This produces candidates only. It does not infer newsletter consent and
    deliberately leaves every candidate in pending_review state.
    """
    tags = split_fub_tags(row.get("Tags") or "")
    tag_blob = " | ".join(tags)
    stage = (row.get("Stage") or "").strip().lower()
    source = (row.get("Lead Source") or "").strip().lower()

    if has_signal(tags, FUB_SUPPRESSION_SIGNALS):
        return None, "suppressed"

    permission_signal = (
        "_ai-outreach-ok" in tags
        or "past client" in tags
        or stage in {"active client", "hot prospect", "sphere"}
        or source in FUB_DIRECT_SOURCES
    )
    if not permission_signal:
        return None, "no_permission_signal"

    investor = has_signal(tags, FUB_INVESTOR_SIGNALS)
    buyer = has_signal(tags, FUB_BUYER_SIGNALS)
    seller = (
        "seller" in tags
        or "_expired-seller" in tags
        or "expired listing" in tags
    )
    if investor:
        return "investor-brief", "investor_signal"
    if buyer:
        return "temple-insider", "buyer_or_relationship_signal"
    if seller:
        return None, "seller_only"
    if source in FUB_DIRECT_SOURCES:
        return "temple-insider", "direct_inbound_source"
    if "_ai-outreach-ok" in tags and any(
        source_fragment in source
        for source_fragment in (
            "facebook",
            "har.com",
            "market leder",
            "phone inquiry",
            "referral",
            "website",
        )
    ):
        return "temple-insider", "approved_inbound_source"
    return None, "unclassified"


def first_valid_fub_email(row: dict[str, str]) -> str:
    for key in ("Email 1", "Email 2", "Email 3"):
        candidate = (row.get(key) or "").strip().lower()
        if EMAIL_RE.fullmatch(candidate):
            return candidate
    return ""


def prepare_fub_candidates(source_path: Path, output_path: Path) -> dict[str, int]:
    if not source_path.exists():
        raise ValueError(f"FUB export not found: {source_path}")
    with source_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"Date Added", "First Name", "Last Name", "Stage", "Lead Source", "Tags", "Email 1", "ID"}
        missing = sorted(required - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"FUB export is missing columns: {', '.join(missing)}")
        rows = list(reader)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {
        "rows": len(rows),
        "candidates": 0,
        "temple-insider": 0,
        "investor-brief": 0,
        "no_valid_email": 0,
        "duplicate_email": 0,
        "suppressed": 0,
        "no_permission_signal": 0,
        "seller_only": 0,
        "unclassified": 0,
    }
    seen_emails: set[str] = set()
    candidate_rows: list[dict[str, str]] = []

    for row in rows:
        email_value = first_valid_fub_email(row)
        if not email_value:
            counts["no_valid_email"] += 1
            continue
        if email_value in seen_emails:
            counts["duplicate_email"] += 1
            continue
        seen_emails.add(email_value)

        audience, reason = classify_fub_row(row)
        if not audience:
            counts[reason] = counts.get(reason, 0) + 1
            continue

        counts["candidates"] += 1
        counts[audience] += 1
        candidate_rows.append(
            {
                "email": email_value,
                "first_name": (row.get("First Name") or "").strip(),
                "last_name": (row.get("Last Name") or "").strip(),
                "audience": audience,
                "consent_status": "pending_review",
                "consent_source": "",
                "consent_date": "",
                "tags": (row.get("Tags") or "").strip(),
                "notes": "FUB candidate only; confirm permission before import",
                "fub_id": (row.get("ID") or "").strip(),
                "fub_date_added": (row.get("Date Added") or "").strip(),
                "fub_stage": (row.get("Stage") or "").strip(),
                "fub_lead_source": (row.get("Lead Source") or "").strip(),
                "classification_reason": reason,
            }
        )

    fieldnames = [
        "email",
        "first_name",
        "last_name",
        "audience",
        "consent_status",
        "consent_source",
        "consent_date",
        "tags",
        "notes",
        "fub_id",
        "fub_date_added",
        "fub_stage",
        "fub_lead_source",
        "classification_reason",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidate_rows)
    return counts


def command_contacts_validate(args: argparse.Namespace) -> int:
    report = validate_contacts(args.path, args.audience)
    print_contact_report(report)
    return 1 if report.errors else 0


def command_contacts_sync(args: argparse.Namespace) -> int:
    report = validate_contacts(args.path, args.audience)
    print_contact_report(report)
    if report.errors:
        print("Import blocked until every validation error is fixed.", file=sys.stderr)
        return 1

    selected = [c for c in report.active if c.audience == args.audience]
    if not selected:
        print(f"No active {args.audience} contacts to import.")
        return 0

    payload = subscription_payload(selected)
    if args.payload_out:
        args.payload_out.parent.mkdir(parents=True, exist_ok=True)
        args.payload_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Private payload written: {args.payload_out}")

    if not args.live:
        print(
            f"DRY RUN: {len(selected)} consented contact(s) are ready for "
            f"{AUDIENCES[args.audience]['name']}."
        )
        print(f"Use --live --confirm {CONFIRM_IMPORT} only after reviewing this report.")
        return 0

    if args.confirm != CONFIRM_IMPORT:
        print(f"Live import blocked. Required confirmation: {CONFIRM_IMPORT}", file=sys.stderr)
        return 1

    load_env_file(Path.home() / "shared-keys.env")
    api_key = os.environ.get("BEEHIIV_API_KEY", "").strip()
    publication_id = os.environ.get(AUDIENCES[args.audience]["publication_env"], "").strip()
    if not api_key or not publication_id:
        print("Beehiiv API key or publication ID is missing.", file=sys.stderr)
        return 1

    endpoint = (
        f"https://api.beehiiv.com/v2/publications/{publication_id}/bulk_subscriptions"
    )
    result = request_json(
        endpoint,
        method="POST",
        headers=beehiiv_headers(api_key),
        payload=payload,
    )
    print(f"Beehiiv accepted {len(selected)} contact(s) for validation/import.")
    if result.get("import_id"):
        print(f"Import ID: {result['import_id']}")
    return 0


def fetch_beehiiv_subscriptions(api_key: str, publication_id: str) -> dict[str, str]:
    subscriptions: dict[str, str] = {}
    cursor = ""
    while True:
        query = {"limit": "100"}
        if cursor:
            query["cursor"] = cursor
        url = (
            f"https://api.beehiiv.com/v2/publications/{publication_id}/subscriptions?"
            + urllib.parse.urlencode(query)
        )
        response = request_json(url, headers=beehiiv_headers(api_key))
        for item in response.get("data", []):
            email_value = (item.get("email") or "").strip().lower()
            if email_value:
                subscriptions[email_value] = (item.get("status") or "unknown").strip().lower()
        if not response.get("has_more"):
            break
        cursor = (response.get("next_cursor") or "").strip()
        if not cursor:
            raise RuntimeError("Beehiiv indicated more subscriptions but returned no cursor")
    return subscriptions


def reconcile_candidate_rows(
    rows: list[dict[str, str]],
    subscriptions_by_audience: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    counts = {
        "already_active": 0,
        "existing_inactive": 0,
        "existing_invalid": 0,
        "not_in_beehiiv": 0,
    }
    reconciled: list[dict[str, str]] = []
    for original in rows:
        row = dict(original)
        audience = (row.get("audience") or "").strip()
        email_value = (row.get("email") or "").strip().lower()
        status = subscriptions_by_audience.get(audience, {}).get(email_value, "not_found")
        if status == "active":
            action = "already_active"
            counts["already_active"] += 1
        elif status == "inactive":
            action = "do_not_import_existing_inactive"
            counts["existing_inactive"] += 1
        elif status == "invalid":
            action = "do_not_import_existing_invalid"
            counts["existing_invalid"] += 1
        else:
            action = "review_permission_before_import"
            counts["not_in_beehiiv"] += 1
        row["beehiiv_status"] = status
        row["recommended_action"] = action
        reconciled.append(row)
    return reconciled, counts


def parse_fub_date(value: str) -> date | None:
    try:
        return date.fromisoformat((value or "").strip()[:10])
    except ValueError:
        return None


def filter_fub_candidate(
    candidate: dict[str, str],
    source_row: dict[str, str] | None,
    recent_since: date,
) -> tuple[str, str, str]:
    """Return review tier, action, and a non-sensitive filtering reason."""
    beehiiv_action = (candidate.get("recommended_action") or "").strip()
    if beehiiv_action == "already_active":
        return "already_active", "keep_existing_subscription", "already active in Beehiiv"
    if beehiiv_action.startswith("do_not_import"):
        return (
            "hard_exclude_beehiiv",
            "exclude_from_import",
            "existing inactive or invalid Beehiiv subscription",
        )
    if source_row is None:
        return "source_row_missing_hold", "exclude_from_import", "FUB source row not found"

    tags = split_fub_tags(candidate.get("tags") or "")
    stage = (candidate.get("fub_stage") or "").strip().lower()
    source = (candidate.get("fub_lead_source") or "").strip().lower()
    closed_deal = bool((source_row.get("Deal Close Date") or "").strip())
    relationship = bool(tags & FUB_RELATIONSHIP_SIGNALS) or closed_deal or stage in {
        "active client",
        "hot prospect",
        "sphere",
    }
    if relationship:
        return (
            "relationship_priority",
            "review_permission",
            "past-client, closed-deal, sphere, or active-relationship signal",
        )
    if any(signal in source for signal in FUB_COLD_SOURCE_SIGNALS):
        return "cold_source_hold", "exclude_from_import", "cold prospecting source"
    if (source_row.get("Is Contacted") or "").strip().lower() == "yes":
        return "contacted_lead_review", "review_permission", "FUB marks lead as contacted"

    added = parse_fub_date(candidate.get("fub_date_added") or "")
    if added and added >= recent_since:
        return (
            "recent_inbound_review",
            "review_permission",
            f"inbound candidate added on or after {recent_since.isoformat()}",
        )
    return (
        "older_uncontacted_hold",
        "exclude_from_import",
        "older lead without relationship or contact evidence",
    )


def filter_fub_candidates(
    candidate_rows: list[dict[str, str]],
    source_by_id: dict[str, dict[str, str]],
    recent_since: date,
) -> tuple[dict[str, list[dict[str, str]]], dict[str, int]]:
    groups: dict[str, list[dict[str, str]]] = {
        "temple-insider": [],
        "investor-brief": [],
        "held-out": [],
    }
    counts: dict[str, int] = {}
    tier_order = {
        "relationship_priority": 0,
        "contacted_lead_review": 1,
        "recent_inbound_review": 2,
    }
    for original in candidate_rows:
        row = dict(original)
        tier, action, reason = filter_fub_candidate(
            row,
            source_by_id.get((row.get("fub_id") or "").strip()),
            recent_since,
        )
        row["review_tier"] = tier
        row["filter_action"] = action
        row["filter_reason"] = reason
        row["review_decision"] = ""
        counts[tier] = counts.get(tier, 0) + 1
        audience = (row.get("audience") or "").strip()
        if tier in FUB_REVIEW_TIERS and audience in AUDIENCES:
            groups[audience].append(row)
        else:
            groups["held-out"].append(row)

    for audience in AUDIENCES:
        groups[audience].sort(
            key=lambda row: (
                tier_order.get(row["review_tier"], 99),
                (row.get("last_name") or "").lower(),
                (row.get("first_name") or "").lower(),
            )
        )
    groups["held-out"].sort(
        key=lambda row: (
            row["review_tier"],
            (row.get("audience") or "").lower(),
            (row.get("last_name") or "").lower(),
        )
    )
    return groups, counts


def write_contact_rows(path: Path, rows: list[dict[str, str]], base_fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    extra_fields = [
        field
        for field in ("review_tier", "filter_action", "filter_reason", "review_decision")
        if field not in base_fields
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=base_fields + extra_fields)
        writer.writeheader()
        writer.writerows(rows)


def curate_review_rows(
    rows: list[dict[str, str]],
    decisions: dict,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    if decisions.get("row_number_basis") != "csv_header_is_row_1":
        raise ValueError("row_number_basis must be csv_header_is_row_1")
    removals = decisions.get("remove") or []
    if not isinstance(removals, list):
        raise ValueError("remove must be a list")

    remove_by_row: dict[int, dict] = {}
    for item in removals:
        if not isinstance(item, dict):
            raise ValueError("each remove item must be an object")
        spreadsheet_row = item.get("spreadsheet_row")
        if not isinstance(spreadsheet_row, int) or spreadsheet_row < 2:
            raise ValueError("remove spreadsheet_row must be an integer of 2 or greater")
        if spreadsheet_row in remove_by_row:
            raise ValueError(f"duplicate removal row: {spreadsheet_row}")
        remove_by_row[spreadsheet_row] = item

    kept: list[dict[str, str]] = []
    removed: list[dict[str, str]] = []
    for spreadsheet_row, original in enumerate(rows, start=2):
        decision = remove_by_row.get(spreadsheet_row)
        if not decision:
            kept.append(dict(original))
            continue
        expected_fub_id = str(decision.get("expected_fub_id") or "").strip()
        actual_fub_id = (original.get("fub_id") or "").strip()
        if not expected_fub_id or actual_fub_id != expected_fub_id:
            raise ValueError(
                f"row {spreadsheet_row} identity mismatch; expected FUB ID "
                f"{expected_fub_id or '(missing)'}, found {actual_fub_id or '(missing)'}"
            )
        row = dict(original)
        row["review_tier"] = "manual_removal"
        row["filter_action"] = "exclude_from_import"
        row["filter_reason"] = (
            f"Taylor requested removal on {decisions.get('decision_date') or date.today().isoformat()}; "
            f"original spreadsheet row {spreadsheet_row}"
        )
        row["review_decision"] = "remove"
        row["original_spreadsheet_row"] = str(spreadsheet_row)
        removed.append(row)

    missing_rows = sorted(set(remove_by_row) - {int(r["original_spreadsheet_row"]) for r in removed})
    if missing_rows:
        raise ValueError(f"removal rows are outside the review file: {missing_rows}")

    additions: list[dict[str, str]] = []
    known_emails = {
        (row.get("email") or "").strip().lower()
        for row in rows
        if (row.get("email") or "").strip()
    }
    for item in decisions.get("add") or []:
        if not isinstance(item, dict):
            raise ValueError("each add item must be an object")
        email_value = (item.get("email") or "").strip().lower()
        audience = (item.get("audience") or "").strip().lower()
        review_tier = (item.get("review_tier") or "contacted_lead_review").strip()
        if not EMAIL_RE.fullmatch(email_value):
            raise ValueError(f"invalid addition email: {email_value or '(missing)'}")
        if audience not in AUDIENCES:
            raise ValueError(f"invalid addition audience for {email_value}")
        if review_tier not in FUB_REVIEW_TIERS:
            raise ValueError(f"invalid addition review tier for {email_value}: {review_tier}")
        if email_value in known_emails:
            raise ValueError(f"addition already exists in review data: {email_value}")
        known_emails.add(email_value)
        additions.append(
            {
                "email": email_value,
                "first_name": (item.get("first_name") or "").strip(),
                "last_name": (item.get("last_name") or "").strip(),
                "audience": audience,
                "consent_status": "pending_review",
                "consent_source": "",
                "consent_date": "",
                "tags": (item.get("tags") or "").strip(),
                "notes": (item.get("notes") or "").strip(),
                "fub_id": (item.get("source_id") or "").strip(),
                "fub_date_added": (item.get("source_date") or "").strip(),
                "fub_stage": "",
                "fub_lead_source": (item.get("lead_source") or "Manual review").strip(),
                "classification_reason": "direct_buyer_correspondence",
                "beehiiv_status": "pending_live_check",
                "recommended_action": "review_permission_before_import",
                "review_tier": review_tier,
                "filter_action": "review_permission",
                "filter_reason": (item.get("filter_reason") or "direct buyer correspondence").strip(),
                "review_decision": "",
            }
        )
    return kept + additions, removed, additions


def command_fub_curate(args: argparse.Namespace) -> int:
    if not args.review.exists() or not args.decisions.exists() or not args.held_out.exists():
        print("Review, decisions, or held-out file is missing.", file=sys.stderr)
        return 1
    try:
        decisions = json.loads(args.decisions.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read curation decisions: {exc}", file=sys.stderr)
        return 1

    with args.review.open(newline="", encoding="utf-8-sig") as handle:
        review_reader = csv.DictReader(handle)
        fields = list(review_reader.fieldnames or [])
        rows = list(review_reader)
    try:
        curated, removed, additions = curate_review_rows(rows, decisions)
    except ValueError as exc:
        print(f"Curation blocked: {exc}", file=sys.stderr)
        return 1

    print("Newsletter review curation")
    print(f"  Current review rows: {len(rows)}")
    print(f"  Manual removals: {len(removed)}")
    print(f"  Manual additions: {len(additions)}")
    print(f"  Resulting review rows: {len(curated)}")
    if not args.apply:
        print(f"DRY RUN: add --apply --confirm {CONFIRM_CURATION} to write private files.")
        return 0
    if args.confirm != CONFIRM_CURATION:
        print(f"Curation blocked. Required confirmation: {CONFIRM_CURATION}", file=sys.stderr)
        return 1

    args.archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup = args.archive_dir / f"before-curation-{timestamp}.csv"
    write_contact_rows(backup, rows, fields)

    archive_fields = fields + (["original_spreadsheet_row"] if "original_spreadsheet_row" not in fields else [])
    removals_archive = args.archive_dir / f"manual-removals-{timestamp}.csv"
    write_contact_rows(removals_archive, removed, archive_fields)

    with args.held_out.open(newline="", encoding="utf-8-sig") as handle:
        held_reader = csv.DictReader(handle)
        held_fields = list(held_reader.fieldnames or [])
        held_rows = list(held_reader)
    held_emails = {(row.get("email") or "").strip().lower() for row in held_rows}
    for original in removed:
        row = {key: value for key, value in original.items() if key in held_fields}
        email_value = (row.get("email") or "").strip().lower()
        if email_value not in held_emails:
            held_rows.append(row)
            held_emails.add(email_value)

    write_contact_rows(args.review, curated, fields)
    write_contact_rows(args.held_out, held_rows, held_fields)
    print(f"  Backup: {backup}")
    print(f"  Removal archive: {removals_archive}")
    print("No FUB or Beehiiv record was changed.")
    return 0


def command_fub_filter(args: argparse.Namespace) -> int:
    if not args.candidates.exists():
        print(f"Candidate file not found: {args.candidates}", file=sys.stderr)
        return 1
    if not args.source.exists():
        print(f"FUB export not found: {args.source}", file=sys.stderr)
        return 1

    with args.candidates.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        base_fields = list(reader.fieldnames or [])
        candidate_rows = list(reader)
    required_candidates = {"email", "audience", "fub_id", "recommended_action"}
    missing_candidates = sorted(required_candidates - set(base_fields))
    if missing_candidates:
        print(
            f"Candidate file is missing columns: {', '.join(missing_candidates)}",
            file=sys.stderr,
        )
        return 1

    with args.source.open(newline="", encoding="utf-8-sig") as handle:
        source_reader = csv.DictReader(handle)
        source_fields = set(source_reader.fieldnames or [])
        required_source = {"ID", "Is Contacted", "Deal Close Date"}
        missing_source = sorted(required_source - source_fields)
        if missing_source:
            print(
                f"FUB export is missing columns: {', '.join(missing_source)}",
                file=sys.stderr,
            )
            return 1
        source_by_id = {
            (row.get("ID") or "").strip(): row
            for row in source_reader
            if (row.get("ID") or "").strip()
        }

    groups, counts = filter_fub_candidates(candidate_rows, source_by_id, args.recent_since)
    files = {
        "temple-insider": args.output_dir / "temple-insider-review.csv",
        "investor-brief": args.output_dir / "investor-brief-review.csv",
        "held-out": args.output_dir / "held-out.csv",
    }
    for group, path in files.items():
        write_contact_rows(path, groups[group], base_fields)

    print(f"Private filtered review lists written: {args.output_dir}")
    print(f"  temple-insider review: {len(groups['temple-insider'])}")
    print(f"  investor-brief review: {len(groups['investor-brief'])}")
    print(f"  held out / already handled: {len(groups['held-out'])}")
    print("  Review tiers:")
    for tier in (
        "relationship_priority",
        "contacted_lead_review",
        "recent_inbound_review",
        "already_active",
        "hard_exclude_beehiiv",
        "cold_source_hold",
        "older_uncontacted_hold",
        "source_row_missing_hold",
    ):
        if counts.get(tier):
            print(f"    {tier}: {counts[tier]}")
    print("No FUB or Beehiiv record was deleted, imported, reactivated, or changed.")
    return 0


def command_contacts_reconcile(args: argparse.Namespace) -> int:
    if not args.live:
        print("DRY RUN: reconcile makes no network call. Add --live for a read-only Beehiiv comparison.")
        return 0
    if not args.path.exists():
        print(f"Candidate file not found: {args.path}", file=sys.stderr)
        return 1

    load_env_file(Path.home() / "shared-keys.env")
    api_key = os.environ.get("BEEHIIV_API_KEY", "").strip()
    if not api_key:
        print("BEEHIIV_API_KEY is missing.", file=sys.stderr)
        return 1
    subscriptions: dict[str, dict[str, str]] = {}
    for audience, config in AUDIENCES.items():
        publication_id = os.environ.get(config["publication_env"], "").strip()
        if not publication_id:
            print(f"Publication ID missing for {audience}.", file=sys.stderr)
            return 1
        subscriptions[audience] = fetch_beehiiv_subscriptions(api_key, publication_id)

    with args.path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if not {"email", "audience", "consent_status"}.issubset(fieldnames):
        print("Candidate file is missing email, audience, or consent_status.", file=sys.stderr)
        return 1

    reconciled, counts = reconcile_candidate_rows(rows, subscriptions)
    output = args.output or args.path.with_name(args.path.stem + "-reconciled.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    output_fields = fieldnames + [
        field for field in ("beehiiv_status", "recommended_action") if field not in fieldnames
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(reconciled)
    print(f"Private Beehiiv reconciliation written: {output}")
    print(f"  already_active: {counts['already_active']}")
    print(f"  existing_inactive: {counts['existing_inactive']}")
    print(f"  existing_invalid: {counts['existing_invalid']}")
    print(f"  review_permission_before_import: {counts['not_in_beehiiv']}")
    print("No contact was imported, reactivated, or changed.")
    return 0


def command_fub_prepare(args: argparse.Namespace) -> int:
    try:
        counts = prepare_fub_candidates(args.source, args.output)
    except (OSError, ValueError) as exc:
        print(f"FUB preparation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Private review file written: {args.output}")
    print(f"  FUB rows read: {counts['rows']}")
    print(f"  Pending candidates: {counts['candidates']}")
    print(f"  temple-insider: {counts['temple-insider']}")
    print(f"  investor-brief: {counts['investor-brief']}")
    print("  Held out:")
    for key in (
        "no_valid_email",
        "duplicate_email",
        "suppressed",
        "no_permission_signal",
        "seller_only",
        "unclassified",
    ):
        print(f"    {key}: {counts[key]}")
    print("No candidate is importable until pending_review is replaced with a confirmed consent record.")
    return 0


def parse_frontmatter(source: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(source)
    if not match:
        raise ValueError("Issue source must start with --- frontmatter")
    metadata: dict[str, str] = {}
    for line_number, raw_line in enumerate(match.group(1).splitlines(), start=2):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            raise ValueError(f"Invalid frontmatter on line {line_number}")
        key, value = raw_line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, match.group(2).strip()


def issue_errors(metadata: dict[str, str], body: str) -> list[str]:
    errors: list[str] = []
    required = {
        "newsletter",
        "issue_type",
        "subject",
        "preview_text",
        "send_date",
        "data_sources",
    }
    for key in sorted(required):
        if not metadata.get(key):
            errors.append(f"Missing frontmatter field: {key}")

    newsletter = metadata.get("newsletter", "")
    if newsletter and newsletter not in AUDIENCES:
        errors.append(f"newsletter must be one of: {', '.join(AUDIENCES)}")
    issue_type = metadata.get("issue_type", "")
    if issue_type and issue_type not in ISSUE_TYPES:
        errors.append(f"issue_type must be one of: {', '.join(ISSUE_TYPES)}")
    if issue_type in ISSUE_TYPES and newsletter in AUDIENCES:
        expected_newsletter = ISSUE_TYPES[issue_type]
        if newsletter != expected_newsletter:
            errors.append(
                f"{issue_type} issues must use the {expected_newsletter} audience"
            )
    subject = metadata.get("subject", "")
    if len(subject) > 50:
        errors.append(f"Subject is {len(subject)} characters; maximum is 50")
    preview = metadata.get("preview_text", "")
    if preview and not 80 <= len(preview) <= 100:
        errors.append(f"Preview text is {len(preview)} characters; target is 80-100")
    send_date = metadata.get("send_date", "")
    parsed_send_date: date | None = None
    if send_date:
        try:
            parsed_send_date = date.fromisoformat(send_date)
        except ValueError:
            errors.append("send_date must be YYYY-MM-DD")

    if issue_type == "market-update" and parsed_send_date is not None and parsed_send_date >= date(2026, 8, 6):
        errors.append(
            "Temple TX Insider market-update is retired as of 2026-08-06; "
            "use leverage-list and never recreate Issue #1"
        )

    if issue_type == "leverage-list":
        leverage_required = {
            "issue_number",
            "selection_mode",
            "prior_issue_suppression",
            "approval_status",
            "send_time_local",
            "timezone",
        }
        for key in sorted(leverage_required):
            if not metadata.get(key):
                errors.append(f"Missing Leverage List frontmatter field: {key}")

        issue_number = metadata.get("issue_number", "")
        if issue_number and not PLACEHOLDER_RE.search(issue_number):
            try:
                parsed_issue_number = int(issue_number)
            except ValueError:
                errors.append("Leverage List issue_number must be an integer of 2 or greater")
            else:
                if parsed_issue_number < 2:
                    errors.append("Leverage List Issue #1 is historical and cannot be rebuilt")

        selection_mode = metadata.get("selection_mode", "")
        if (
            selection_mode
            and not PLACEHOLDER_RE.search(selection_mode)
            and selection_mode not in LEVERAGE_SELECTION_MODES
        ):
            errors.append(
                "Leverage List selection_mode must be codex-pick or taylor-pick"
            )

        suppression = metadata.get("prior_issue_suppression", "")
        if (
            suppression
            and not PLACEHOLDER_RE.search(suppression)
            and suppression != LEVERAGE_SUPPRESSION_STATE
        ):
            errors.append(
                "Leverage List prior_issue_suppression must confirm "
                f"{LEVERAGE_SUPPRESSION_STATE}"
            )

        approval_status = metadata.get("approval_status", "")
        if (
            approval_status
            and not PLACEHOLDER_RE.search(approval_status)
            and approval_status not in LEVERAGE_APPROVAL_STATUSES
        ):
            errors.append(
                "Leverage List approval_status must remain awaiting Taylor's final "
                "approval or record that approval separately"
            )

        send_time_local = metadata.get("send_time_local", "")
        if (
            send_time_local
            and not PLACEHOLDER_RE.search(send_time_local)
            and send_time_local != LEVERAGE_SEND_TIME_LOCAL
        ):
            errors.append(
                f"Leverage List send_time_local must be {LEVERAGE_SEND_TIME_LOCAL}"
            )
        timezone = metadata.get("timezone", "")
        if (
            timezone
            and not PLACEHOLDER_RE.search(timezone)
            and timezone != LEVERAGE_TIMEZONE
        ):
            errors.append(f"Leverage List timezone must be {LEVERAGE_TIMEZONE}")

        if parsed_send_date is not None:
            cadence_offset = (parsed_send_date - LEVERAGE_CADENCE_ANCHOR).days
            if cadence_offset < 0 or cadence_offset % 14 != 0:
                errors.append(
                    "Leverage List send_date must follow the every-other-Tuesday "
                    "cadence anchored on 2026-08-18"
                )

    combined = f"{subject}\n{body}".lower()
    banned = [term for term in load_banned_words() if term != "fort hood"]
    for term in banned:
        if term and term in combined:
            errors.append(f"Banned language found: {term}")
    if "taylor dasch" not in body.lower() or "eg realty" not in body.lower():
        errors.append("Body must identify Taylor Dasch and EG Realty")
    specific_site_link = re.search(
        r"https?://(?:www\.)?templetxhomes\.net/(?!\s|\)|>|$)[^\s\)>]+", body
    )
    if not specific_site_link:
        errors.append("Body needs a link to a specific templetxhomes.net page")
    if not body.strip():
        errors.append("Issue body is empty")
    if PLACEHOLDER_RE.search("\n".join(metadata.values()) + "\n" + body):
        errors.append("Unresolved template placeholders remain")
    return list(dict.fromkeys(errors))


def render_inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s\)]+)\)",
        lambda m: (
            f'<a href="{html.escape(m.group(2), quote=True)}" '
            'style="color:#047857;text-decoration:underline;">{}</a>'.format(m.group(1))
        ),
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def markdown_to_email_html(markdown: str) -> str:
    """Render the deliberately small Markdown subset used by newsletter drafts."""
    output: list[str] = []
    paragraph: list[str] = []
    list_mode: str | None = None
    table_rows: list[list[str]] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph)
            output.append(
                '<p style="margin:0 0 18px;font-size:16px;line-height:1.65;color:#253047;">'
                f"{render_inline(text)}</p>"
            )
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_mode
        if list_mode:
            output.append(f"</{list_mode}>")
            list_mode = None

    def flush_table() -> None:
        if not table_rows:
            return
        rows = [row for row in table_rows if not all(re.fullmatch(r":?-{3,}:?", c) for c in row)]
        if rows:
            output.append('<table role="presentation" width="100%" style="border-collapse:collapse;margin:8px 0 22px;font-size:14px;">')
            for row_index, row in enumerate(rows):
                tag = "th" if row_index == 0 else "td"
                output.append("<tr>")
                for cell in row:
                    output.append(
                        f'<{tag} style="padding:9px 8px;border-bottom:1px solid #dfe4ea;text-align:left;vertical-align:top;">'
                        f"{render_inline(cell.strip())}</{tag}>"
                    )
                output.append("</tr>")
            output.append("</table>")
        table_rows.clear()

    for raw_line in markdown.splitlines() + [""]:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            table_rows.append([cell.strip() for cell in stripped.strip("|").split("|")])
            continue
        flush_table()

        if not stripped:
            flush_paragraph()
            flush_list()
            continue
        if stripped in {"---", "***"}:
            flush_paragraph()
            flush_list()
            output.append('<hr style="border:0;border-top:1px solid #dfe4ea;margin:28px 0;">')
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1)) + 1
            size = {2: 28, 3: 22, 4: 18}[level]
            output.append(
                f'<h{level} style="margin:28px 0 12px;font-family:Georgia,serif;font-size:{size}px;line-height:1.2;color:#14251f;">'
                f"{render_inline(heading.group(2))}</h{level}>"
            )
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if bullet or ordered:
            flush_paragraph()
            desired = "ul" if bullet else "ol"
            if list_mode != desired:
                flush_list()
                list_mode = desired
                output.append(f'<{desired} style="margin:0 0 20px;padding-left:22px;color:#253047;">')
            item = (bullet or ordered).group(1)
            output.append(
                '<li style="margin:0 0 9px;font-size:16px;line-height:1.55;">'
                f"{render_inline(item)}</li>"
            )
            continue
        if stripped.startswith("> "):
            flush_paragraph()
            flush_list()
            output.append(
                '<blockquote style="margin:18px 0;padding:14px 18px;border-left:3px solid #059669;background:#f1f6f3;color:#31443c;">'
                f"{render_inline(stripped[2:])}</blockquote>"
            )
            continue
        paragraph.append(stripped)

    return "\n".join(output)


def email_document(metadata: dict[str, str], body_html: str) -> str:
    preview = html.escape(metadata["preview_text"])
    subject = html.escape(metadata["subject"])
    publication = html.escape(
        ISSUE_TYPE_NAMES.get(
            metadata["issue_type"], AUDIENCES[metadata["newsletter"]]["name"]
        )
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{subject}</title></head>
<body style="margin:0;background:#edf0ed;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">{preview}</div>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#edf0ed;"><tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:620px;background:#fbfaf7;border:1px solid #dde2de;">
<tr><td style="padding:18px 28px;border-bottom:1px solid #dde2de;font-size:11px;letter-spacing:1.7px;text-transform:uppercase;color:#597066;">{publication} · Taylor Dasch · EG Realty</td></tr>
<tr><td style="padding:34px 28px 28px;">
{body_html}
<hr style="border:0;border-top:1px solid #dfe4ea;margin:30px 0 18px;">
<p style="margin:0;font-size:12px;line-height:1.55;color:#6b7280;">Unsubscribe, mailing-address, and preference links are inserted by Beehiiv at delivery. Do not mass-send this HTML directly through Gmail.</p>
</td></tr></table>
</td></tr></table>
</body></html>
"""


def preview_document(metadata: dict[str, str], email_html: str) -> str:
    banner = (
        '<div style="position:sticky;top:0;z-index:3;padding:10px 14px;background:#fff4dc;'
        'border-bottom:1px solid #e8c97b;text-align:center;font:600 12px Arial;color:#76510b;">'
        f"PREVIEW ONLY · NOT SENT · Proposed {html.escape(metadata['send_date'])} · "
        f"Subject: {html.escape(metadata['subject'])}</div>"
    )
    return re.sub(r"(<body[^>]*>)", lambda match: match.group(1) + banner, email_html, count=1)


def plain_text_from_markdown(body: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)", r"\1: \2", body)
    text = re.sub(r"[*_`#>]", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def default_issue_output(metadata: dict[str, str]) -> Path:
    send = date.fromisoformat(metadata["send_date"])
    year, week, _ = send.isocalendar()
    slug = re.sub(r"[^a-z0-9]+", "-", metadata["subject"].lower()).strip("-")[:54]
    return PROJECT_ROOT / "output" / f"{year}-W{week:02d}" / "newsletter" / f"{metadata['newsletter']}-{slug}"


def command_issue_build(args: argparse.Namespace) -> int:
    try:
        metadata, body = parse_frontmatter(args.source.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Issue build failed: {exc}", file=sys.stderr)
        return 1
    errors = issue_errors(metadata, body)
    if errors:
        print("Issue build blocked:", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1

    output_dir = args.output_dir or default_issue_output(metadata)
    output_dir.mkdir(parents=True, exist_ok=True)
    body_html = markdown_to_email_html(body)
    email_html = email_document(metadata, body_html)
    files = {
        "email.html": email_html,
        "preview.html": preview_document(metadata, email_html),
        "plain.txt": plain_text_from_markdown(body),
        "manifest.json": json.dumps(
            {
                **metadata,
                "built_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "delivery_status": "NOT_SENT",
                "delivery_platform": "beehiiv",
                "approval_required": True,
                "gmail_mass_send_allowed": False,
            },
            indent=2,
        )
        + "\n",
    }
    for name, content in files.items():
        (output_dir / name).write_text(content, encoding="utf-8")
    print(f"Issue built: {output_dir}")
    for name in files:
        print(f"  {name}")
    print("Delivery status: NOT_SENT (Beehiiv staging and explicit approval still required)")
    return 0


def command_status(args: argparse.Namespace) -> int:
    if not args.live:
        print("DRY RUN: status makes no network call. Add --live for a read-only Beehiiv check.")
        return 0
    load_env_file(Path.home() / "shared-keys.env")
    api_key = os.environ.get("BEEHIIV_API_KEY", "").strip()
    if not api_key:
        print("BEEHIIV_API_KEY is missing.", file=sys.stderr)
        return 1

    for slug, config in AUDIENCES.items():
        publication_id = os.environ.get(config["publication_env"], "").strip()
        if not publication_id:
            print(f"{config['name']}: publication ID missing", file=sys.stderr)
            continue
        publication = request_json(
            f"https://api.beehiiv.com/v2/publications/{publication_id}?expand=stats",
            headers=beehiiv_headers(api_key),
        ).get("data", {})
        posts = request_json(
            f"https://api.beehiiv.com/v2/publications/{publication_id}/posts?limit=50&order_by=publish_date&direction=desc",
            headers=beehiiv_headers(api_key),
        ).get("data", [])
        confirmed = [post for post in posts if post.get("status") == "confirmed"]
        drafts = [post for post in posts if post.get("status") == "draft"]
        latest = max(confirmed, key=lambda p: p.get("publish_date") or 0, default=None)
        stats = publication.get("stats", {}) or {}
        print(config["name"])
        print(f"  Active subscribers: {stats.get('active_subscriptions', 0)}")
        print(f"  Confirmed issues: {len(confirmed)}")
        print(f"  Drafts: {len(drafts)}")
        if latest:
            sent_at = datetime.fromtimestamp(latest["publish_date"]).astimezone().date()
            print(f"  Latest send: {sent_at} — {latest.get('subject_line') or latest.get('title')}")
        else:
            print("  Latest send: none")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Taylor's chat-first Newsletter Desk")
    groups = parser.add_subparsers(dest="group", required=True)

    contacts = groups.add_parser("contacts", help="Validate or import consented contacts")
    contact_commands = contacts.add_subparsers(dest="command", required=True)
    validate = contact_commands.add_parser("validate", help="Validate a private contact CSV")
    validate.add_argument("path", type=Path)
    validate.add_argument("--audience", choices=sorted(AUDIENCES))
    validate.set_defaults(func=command_contacts_validate)

    sync = contact_commands.add_parser("sync", help="Prepare or run a Beehiiv contact import")
    sync.add_argument("path", type=Path)
    sync.add_argument("--audience", choices=sorted(AUDIENCES), required=True)
    sync.add_argument("--payload-out", type=Path)
    sync.add_argument("--live", action="store_true")
    sync.add_argument("--confirm")
    sync.set_defaults(func=command_contacts_sync)

    reconcile = contact_commands.add_parser(
        "reconcile", help="Compare a private candidate CSV with Beehiiv without importing"
    )
    reconcile.add_argument("path", type=Path)
    reconcile.add_argument("--output", type=Path)
    reconcile.add_argument("--live", action="store_true")
    reconcile.set_defaults(func=command_contacts_reconcile)

    issue = groups.add_parser("issue", help="Build an email-safe issue preview")
    issue_commands = issue.add_subparsers(dest="command", required=True)
    build = issue_commands.add_parser("build", help="Build HTML, preview, plain text, and manifest")
    build.add_argument("source", type=Path)
    build.add_argument("--output-dir", type=Path)
    build.set_defaults(func=command_issue_build)

    fub = groups.add_parser("fub", help="Prepare a private review list from a FUB export")
    fub_commands = fub.add_subparsers(dest="command", required=True)
    prepare = fub_commands.add_parser("prepare", help="Classify FUB contacts without importing them")
    prepare.add_argument("source", type=Path)
    prepare.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "newsletter" / "private" / "fub-newsletter-candidates.csv",
    )
    prepare.set_defaults(func=command_fub_prepare)

    filter_candidates = fub_commands.add_parser(
        "filter", help="Create conservative private review lists from reconciled FUB candidates"
    )
    filter_candidates.add_argument("candidates", type=Path)
    filter_candidates.add_argument("source", type=Path)
    filter_candidates.add_argument(
        "--recent-since",
        type=date.fromisoformat,
        default=date.today() - timedelta(days=365),
        help="Treat uncontacted inbound candidates added on or after YYYY-MM-DD as recent",
    )
    filter_candidates.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "newsletter" / "private" / "fub-filtered",
    )
    filter_candidates.set_defaults(func=command_fub_filter)

    curate = fub_commands.add_parser(
        "curate", help="Apply an audited manual review decision file to private contact lists"
    )
    curate.add_argument("review", type=Path)
    curate.add_argument("decisions", type=Path)
    curate.add_argument("--held-out", type=Path, required=True)
    curate.add_argument(
        "--archive-dir",
        type=Path,
        default=PROJECT_ROOT / "newsletter" / "private" / "fub-filtered" / "archive",
    )
    curate.add_argument("--apply", action="store_true")
    curate.add_argument("--confirm")
    curate.set_defaults(func=command_fub_curate)

    status = groups.add_parser("status", help="Read Beehiiv list and issue status")
    status.add_argument("--live", action="store_true")
    status.set_defaults(func=command_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except RuntimeError as exc:
        warn(str(exc), context="newsletter-desk")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
