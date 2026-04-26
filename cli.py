#!/usr/bin/env python3
"""cli.py — Social Media Manager operational CLI.

One entrypoint that wraps intake / draft / approval / export / compliance /
calendar / gaps. Generation still happens via Claude Code skills — this CLI
imports skill output as drafts, runs compliance, and exports approved posts.

Commands (see --help):
    intake add | list | show | close
    draft new | list | show | import | edit | approve | reject | revise |
          scheduled | posted | history | delete
    export approved
    compliance check
    calendar week | gaps | mix
    analytics template
    version

Hard rule: this CLI never publishes anything. Export = write a file.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from smm import AUDIENCES, DRAFT_STATUSES, FUNNEL_STAGES, PLATFORMS, __version__
from smm import approval, calendar, compliance, drafts, intake
from smm.db import db_path, init_db
from smm.exporters import export_approved_csv, export_approved_json
from smm.integrations import (
    push_ayrshare, push_buffer, push_csv, push_postiz,
)
from smm.integrations import postiz as postiz_integration
from smm.models import Draft, Intake

REPO_ROOT = Path(__file__).resolve().parent
ANALYTICS_TEMPLATE = REPO_ROOT / "analytics_template.csv"


# ---------- helpers ----------

def _print_json(obj):
    print(json.dumps(obj, indent=2, default=str))


def _print_draft_summary(d):
    flag_count = len(d.compliance_flags)
    hard = sum(1 for f in d.compliance_flags if f.get("severity") == "hard")
    soft = flag_count - hard
    sel = (d.selected_hook or "")[:60].replace("\n", " ")
    preview = d.body[:80].replace("\n", " ")
    print(f"{d.id}  [{d.status:<12}] {d.platform:<18} flags=H{hard}/S{soft}  {sel}  — {preview}")


def _print_intake_summary(i: dict):
    preview = (i.get("raw_input") or "")[:70].replace("\n", " ")
    print(f"{i['id']}  [{i['status']:<8}] {i['audience']:<18} {i['source_type']:<10} — {i['source_title'] or preview}")


# ---------- intake ----------

def cmd_intake_add(args):
    raw = args.body
    if not raw and not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    if not raw and not args.title:
        print("ERROR: provide --body or --title or pipe text via stdin", file=sys.stderr)
        return 2
    item = Intake(
        source_type=args.source_type,
        source_title=args.title,
        source_url=args.url,
        raw_input=raw or "",
        audience=args.audience,
        market=args.market or "Temple, TX",
        funnel_stage=args.funnel_stage,
        notes=args.notes,
    )
    if item.audience not in AUDIENCES:
        print(f"WARN: audience '{item.audience}' not in {AUDIENCES}", file=sys.stderr)
    if item.funnel_stage not in FUNNEL_STAGES:
        print(f"WARN: funnel_stage '{item.funnel_stage}' not in {FUNNEL_STAGES}", file=sys.stderr)
    intake.add_intake(item)
    print(item.id)
    return 0


def cmd_intake_list(args):
    rows = intake.list_intake(status=args.status, audience=args.audience, limit=args.limit)
    if args.json:
        _print_json(rows)
        return 0
    if not rows:
        print("(no intake rows)")
        return 0
    for r in rows:
        _print_intake_summary(r)
    return 0


def cmd_intake_show(args):
    r = intake.get_intake(args.id)
    if not r:
        print(f"ERROR: intake {args.id} not found", file=sys.stderr)
        return 2
    _print_json(r)
    return 0


def cmd_intake_close(args):
    ok = intake.update_intake_status(args.id, "closed")
    print("closed" if ok else "no-op")
    return 0 if ok else 2


# ---------- draft ----------

def cmd_draft_new(args):
    body = args.body
    if not body and not sys.stdin.isatty():
        body = sys.stdin.read()
    if not body:
        print("ERROR: --body required (or pipe body via stdin)", file=sys.stderr)
        return 2
    if args.platform not in PLATFORMS:
        print(f"WARN: platform '{args.platform}' not in {PLATFORMS}", file=sys.stderr)
    d = Draft(
        intake_id=args.intake,
        platform=args.platform,
        body=body,
        selected_hook=args.hook,
        cta=args.cta,
        hashtags=args.hashtags.split() if args.hashtags else [],
        suggested_asset=args.asset,
        status="needs_review",
    )
    draft_id = drafts.add_draft(d)
    stored = drafts.get_draft(draft_id)
    print(f"{draft_id} — compliance: {compliance.summarize(stored.compliance_flags)}")
    return 0


def cmd_draft_import(args):
    path = Path(args.path).expanduser().resolve()
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 2
    if args.platform not in PLATFORMS:
        print(f"WARN: platform '{args.platform}' not in {PLATFORMS}", file=sys.stderr)
    draft_id = drafts.import_file_as_draft(path, platform=args.platform, intake_id=args.intake)
    stored = drafts.get_draft(draft_id)
    print(f"{draft_id} — compliance: {compliance.summarize(stored.compliance_flags)}")
    return 0


# ---------- doctor ----------

def cmd_doctor(args):
    """Self-health-check: DB, voice rubric, registry, exports, compliance module, env."""
    import platform as _platform
    import sqlite3
    from smm import compliance as _comp

    ok = True

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal ok
        mark = "✓" if cond else "✗"
        if not cond:
            ok = False
        print(f"  {mark} {name}" + (f" — {detail}" if detail else ""))

    print(f"Python:      {_platform.python_version()} on {_platform.system()} {_platform.release()}")
    print(f"DB path:     {db_path()}")

    print("\n== database ==")
    db = db_path()
    check("db file exists", db.exists(), str(db))
    if db.exists():
        with sqlite3.connect(db) as c:
            tables = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            for t in ("intake", "drafts", "approval_events"):
                check(f"table '{t}' present", t in tables)
            intake_n = c.execute("SELECT COUNT(*) FROM intake").fetchone()[0]
            drafts_n = c.execute("SELECT COUNT(*) FROM drafts").fetchone()[0]
            events_n = c.execute("SELECT COUNT(*) FROM approval_events").fetchone()[0]
            print(f"  counts:   intake={intake_n}  drafts={drafts_n}  approval_events={events_n}")

    print("\n== voice + compliance ==")
    vr = REPO_ROOT / "data" / "voice-rubric.json"
    check("voice-rubric.json readable", vr.exists())
    if vr.exists():
        try:
            rubric = json.loads(vr.read_text())
            check("voice-rubric has banned_phrases", bool(rubric.get("banned_phrases")),
                  f"{len(rubric.get('banned_phrases', []))} entries")
        except Exception as e:
            check("voice-rubric.json parses", False, str(e))
    sample = _comp.check_text("This is a charming dream home!", platform="tiktok")
    check("compliance flags banned phrases", _comp.has_hard_violation(sample),
          _comp.summarize(sample))

    print("\n== content registry + market data ==")
    reg = REPO_ROOT / "data" / "content-registry.csv"
    check("content-registry.csv exists", reg.exists())
    if reg.exists():
        with reg.open() as f:
            rows = sum(1 for _ in f) - 1
        print(f"  registry rows: {rows}")
    mkt = REPO_ROOT / "market_data.json"
    check("market_data.json exists", mkt.exists())
    if mkt.exists():
        try:
            mdata = json.loads(mkt.read_text())
            check("market_data has cities", bool(mdata.get("cities")),
                  f"{len(mdata.get('cities', []))} cities")
        except Exception as e:
            check("market_data.json parses", False, str(e))

    print("\n== exports dir ==")
    exp = REPO_ROOT / "exports"
    check("exports/ exists", exp.exists())
    if exp.exists():
        files = [p for p in exp.rglob("*") if p.is_file()]
        print(f"  export files: {len(files)}")

    print("\n== env vars (optional) ==")
    for v in ("POSTIZ_API_URL", "POSTIZ_API_KEY", "AYRSHARE_API_KEY", "BUFFER_ACCESS_TOKEN", "SMM_DB_PATH"):
        present = bool(os.environ.get(v))
        print(f"  {'set' if present else 'unset':5} {v}")

    print(f"\nResult: {'OK' if ok else 'FAIL (see ✗ above)'}")
    return 0 if ok else 1


def cmd_draft_list(args):
    rows = drafts.list_drafts(status=args.status, platform=args.platform, limit=args.limit)
    if args.json:
        _print_json([{
            "id": d.id, "status": d.status, "platform": d.platform,
            "body": d.body, "selected_hook": d.selected_hook,
            "cta": d.cta, "hashtags": d.hashtags,
            "compliance_flags": d.compliance_flags,
            "created_at": d.created_at, "updated_at": d.updated_at,
        } for d in rows])
        return 0
    if not rows:
        print("(no drafts)")
        return 0
    for d in rows:
        _print_draft_summary(d)
    return 0


def cmd_draft_show(args):
    d = drafts.get_draft(args.id)
    if not d:
        print(f"ERROR: draft {args.id} not found", file=sys.stderr)
        return 2
    _print_json({
        "id": d.id, "intake_id": d.intake_id, "platform": d.platform,
        "status": d.status, "selected_hook": d.selected_hook,
        "cta": d.cta, "hashtags": d.hashtags, "body": d.body,
        "suggested_asset": d.suggested_asset,
        "suggested_broll": d.suggested_broll,
        "repurpose_ideas": d.repurpose_ideas,
        "compliance_flags": d.compliance_flags,
        "approval_notes": d.approval_notes,
        "source_path": d.source_path,
        "created_at": d.created_at, "updated_at": d.updated_at,
    })
    return 0


def cmd_draft_edit(args):
    updates = {}
    if args.body is not None:
        updates["body"] = args.body
    if args.platform is not None:
        updates["platform"] = args.platform
    if args.hook is not None:
        updates["selected_hook"] = args.hook
    if args.cta is not None:
        updates["cta"] = args.cta
    if args.hashtags is not None:
        updates["hashtags"] = args.hashtags.split()
    if args.asset is not None:
        updates["suggested_asset"] = args.asset
    if args.notes is not None:
        updates["approval_notes"] = args.notes
    if not updates:
        print("ERROR: nothing to update (pass at least one field)", file=sys.stderr)
        return 2
    ok = drafts.edit_draft(args.id, **updates)
    print("updated" if ok else "no-op")
    if ok:
        d = drafts.get_draft(args.id)
        print(f"compliance: {compliance.summarize(d.compliance_flags)}")
    return 0 if ok else 2


def cmd_draft_approve(args):
    ok, msg = approval.approve(args.id, note=args.note, force=args.force)
    print(msg)
    return 0 if ok else 2


def cmd_draft_reject(args):
    ok, msg = approval.reject(args.id, note=args.note)
    print(msg)
    return 0 if ok else 2


def cmd_draft_revise(args):
    ok, msg = approval.request_revision(args.id, note=args.note)
    print(msg)
    return 0 if ok else 2


def cmd_draft_scheduled(args):
    ok, msg = approval.mark_scheduled(args.id, note=args.note)
    print(msg)
    return 0 if ok else 2


def cmd_draft_posted(args):
    ok, msg = approval.mark_posted(args.id, note=args.note)
    print(msg)
    return 0 if ok else 2


def cmd_draft_history(args):
    h = drafts.approval_history(args.id)
    _print_json(h)
    return 0


def cmd_draft_delete(args):
    if not args.yes:
        print("ERROR: pass --yes to confirm deletion", file=sys.stderr)
        return 2
    ok = drafts.delete_draft(args.id)
    print("deleted" if ok else "no-op")
    return 0 if ok else 2


# ---------- export ----------

def cmd_export_approved(args):
    if args.target == "csv":
        p = export_approved_csv(platform=args.platform)
        print(f"exported CSV: {p}")
        return 0
    if args.target == "json":
        p = export_approved_json(platform=args.platform)
        print(f"exported JSON: {p}")
        return 0
    if args.target == "postiz":
        _print_json(push_postiz(
            platform=args.platform,
            dry_run=not args.live,
            post_type=args.type,
            when_iso=args.when,
        ))
        return 0
    if args.target == "ayrshare":
        _print_json(push_ayrshare(platform=args.platform, dry_run=not args.live))
        return 0
    if args.target == "buffer":
        _print_json(push_buffer(platform=args.platform, dry_run=not args.live))
        return 0
    print(f"ERROR: unknown target {args.target}", file=sys.stderr)
    return 2


# ---------- compliance ----------

def cmd_compliance_check(args):
    text = ""
    if args.path:
        text = Path(args.path).expanduser().read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("ERROR: pass --text, --path, or pipe stdin", file=sys.stderr)
        return 2
    flags = compliance.check_text(text, platform=args.platform)
    if args.json:
        _print_json([f.to_dict() for f in flags])
    else:
        print(compliance.summarize(flags))
        for f in flags:
            print(f"  [{f.severity.upper()}] {f.rule}: {f.message}")
    return 0 if not compliance.has_hard_violation(flags) else 1


# ---------- calendar ----------

def cmd_calendar_week(args):
    snap = calendar.weekly_snapshot()
    _print_json(snap) if args.json else _print_calendar(snap)
    return 0


def _print_calendar(snap: dict):
    print(f"Week: {snap['week']}")
    print(f"  pending: {snap['counts']['pending']}")
    print(f"  approved: {snap['counts']['approved']}")
    print(f"  scheduled: {snap['counts']['scheduled']}")
    print(f"  posted: {snap['counts']['posted']}")
    if snap["pending_by_platform"]:
        print("  pending platforms:")
        for p, n in sorted(snap["pending_by_platform"].items()):
            print(f"    {p}: {n}")
    if snap["output_files_this_week"]:
        print(f"  output files this week ({len(snap['output_files_this_week'])}):")
        for f in snap["output_files_this_week"][:10]:
            print(f"    {f}")


def cmd_calendar_gaps(args):
    gaps = calendar.content_registry_gaps()
    _print_json(gaps) if args.json else _print_gaps(gaps)
    return 0


def _print_gaps(gaps: dict):
    print(f"IDEA: {len(gaps['idea'])}")
    for g in gaps["idea"][:20]:
        print(f"  {g['id']}  {g.get('title','')}")
    print(f"DRAFT: {len(gaps['draft'])}")
    for g in gaps["draft"][:20]:
        print(f"  {g['id']}  {g.get('title','')}")
    print(f"REFRESH_DUE: {len(gaps['refresh_due'])}")
    for g in gaps["refresh_due"][:20]:
        print(f"  {g['id']}  due:{g.get('due','')}  {g.get('title','')}")


def cmd_calendar_mix(args):
    m = calendar.mix_vs_target()
    _print_json(m)
    return 0


# ---------- analytics ----------

def cmd_analytics_template(args):
    if not ANALYTICS_TEMPLATE.exists():
        print(f"ERROR: {ANALYTICS_TEMPLATE} not found", file=sys.stderr)
        return 2
    if args.out:
        out = Path(args.out).expanduser().resolve()
        out.write_text(ANALYTICS_TEMPLATE.read_text(), encoding="utf-8")
        print(f"copied template to {out}")
    else:
        print(ANALYTICS_TEMPLATE.read_text())
    return 0


# ---------- misc ----------

def cmd_version(args):
    print(f"smm cli v{__version__} — db={db_path()}")
    init_db()
    print("db initialized OK")
    return 0


def cmd_postiz_verify(args):
    result = postiz_integration.verify()
    _print_json(result)
    return 0 if result.get("ok") else 1


# ---------- parser ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cli.py", description="Social Media Manager CLI (Taylor Dasch / EG Realty)")
    sub = p.add_subparsers(dest="cmd")

    # intake
    pi = sub.add_parser("intake", help="Manage intake / content ideas")
    pi_sub = pi.add_subparsers(dest="sub")
    pia = pi_sub.add_parser("add", help="Register a new intake item")
    pia.add_argument("--source-type", default="manual",
                     choices=["manual", "youtube", "blog", "listing", "market_update",
                              "neighborhood", "buyer_question", "comment", "past_post",
                              "backlog"])
    pia.add_argument("--title")
    pia.add_argument("--url")
    pia.add_argument("--body", help="Raw input text (or pipe via stdin)")
    pia.add_argument("--audience", default="general_local")
    pia.add_argument("--market", default="Temple, TX")
    pia.add_argument("--funnel-stage", default="awareness")
    pia.add_argument("--notes")
    pia.set_defaults(func=cmd_intake_add)

    pil = pi_sub.add_parser("list")
    pil.add_argument("--status")
    pil.add_argument("--audience")
    pil.add_argument("--limit", type=int, default=50)
    pil.add_argument("--json", action="store_true")
    pil.set_defaults(func=cmd_intake_list)

    pis = pi_sub.add_parser("show")
    pis.add_argument("id")
    pis.set_defaults(func=cmd_intake_show)

    pic = pi_sub.add_parser("close")
    pic.add_argument("id")
    pic.set_defaults(func=cmd_intake_close)

    # draft
    pd = sub.add_parser("draft", help="Manage per-platform drafts")
    pd_sub = pd.add_subparsers(dest="sub")

    pdn = pd_sub.add_parser("new")
    pdn.add_argument("--intake")
    pdn.add_argument("--platform", required=True)
    pdn.add_argument("--body")
    pdn.add_argument("--hook")
    pdn.add_argument("--cta")
    pdn.add_argument("--hashtags")
    pdn.add_argument("--asset")
    pdn.set_defaults(func=cmd_draft_new)

    pdi = pd_sub.add_parser("import", help="Import a file (e.g. skill output) as a draft")
    pdi.add_argument("path")
    pdi.add_argument("--platform", required=True)
    pdi.add_argument("--intake")
    pdi.set_defaults(func=cmd_draft_import)

    pdl = pd_sub.add_parser("list")
    pdl.add_argument("--status", choices=list(DRAFT_STATUSES))
    pdl.add_argument("--platform")
    pdl.add_argument("--limit", type=int, default=100)
    pdl.add_argument("--json", action="store_true")
    pdl.set_defaults(func=cmd_draft_list)

    pds = pd_sub.add_parser("show")
    pds.add_argument("id")
    pds.set_defaults(func=cmd_draft_show)

    pde = pd_sub.add_parser("edit")
    pde.add_argument("id")
    pde.add_argument("--body")
    pde.add_argument("--platform")
    pde.add_argument("--hook")
    pde.add_argument("--cta")
    pde.add_argument("--hashtags")
    pde.add_argument("--asset")
    pde.add_argument("--notes")
    pde.set_defaults(func=cmd_draft_edit)

    pda = pd_sub.add_parser("approve")
    pda.add_argument("id")
    pda.add_argument("--note")
    pda.add_argument("--force", action="store_true",
                     help="Approve despite HARD compliance flags (requires deliberate override)")
    pda.set_defaults(func=cmd_draft_approve)

    pdr = pd_sub.add_parser("reject")
    pdr.add_argument("id")
    pdr.add_argument("--note")
    pdr.set_defaults(func=cmd_draft_reject)

    pdv = pd_sub.add_parser("revise")
    pdv.add_argument("id")
    pdv.add_argument("--note")
    pdv.set_defaults(func=cmd_draft_revise)

    pdsch = pd_sub.add_parser("scheduled")
    pdsch.add_argument("id")
    pdsch.add_argument("--note")
    pdsch.set_defaults(func=cmd_draft_scheduled)

    pdp = pd_sub.add_parser("posted")
    pdp.add_argument("id")
    pdp.add_argument("--note")
    pdp.set_defaults(func=cmd_draft_posted)

    pdh = pd_sub.add_parser("history")
    pdh.add_argument("id")
    pdh.set_defaults(func=cmd_draft_history)

    pdd = pd_sub.add_parser("delete")
    pdd.add_argument("id")
    pdd.add_argument("--yes", action="store_true", help="Confirm")
    pdd.set_defaults(func=cmd_draft_delete)

    # export
    pe = sub.add_parser("export")
    pe_sub = pe.add_subparsers(dest="sub")
    pea = pe_sub.add_parser("approved")
    pea.add_argument("--target", default="csv",
                     choices=["csv", "json", "postiz", "ayrshare", "buffer"])
    pea.add_argument("--platform")
    pea.add_argument("--live", action="store_true",
                     help="Actually push to scheduler. Default is dry-run for safety.")
    pea.add_argument("--type", default="schedule",
                     choices=["schedule", "now"],
                     help="Postiz only: 'schedule' (default, safe — needs --when), 'now' publishes immediately. 'draft' is unsupported (Postiz silently drops drafts with content; use schedule with future --when to get equivalent behavior — Taylor can cancel from Postiz UI before publish).")
    pea.add_argument("--when",
                     help="Postiz only, required for type=schedule. ISO 8601 UTC e.g. 2026-04-28T14:00:00Z. Tip: leave at least 24h to cancel from dashboard before auto-publish.")
    pea.set_defaults(func=cmd_export_approved)

    # compliance
    pc = sub.add_parser("compliance")
    pc_sub = pc.add_subparsers(dest="sub")
    pcc = pc_sub.add_parser("check")
    pcc.add_argument("--text")
    pcc.add_argument("--path")
    pcc.add_argument("--platform")
    pcc.add_argument("--json", action="store_true")
    pcc.set_defaults(func=cmd_compliance_check)

    # calendar
    pcal = sub.add_parser("calendar")
    pcal_sub = pcal.add_subparsers(dest="sub")
    pcw = pcal_sub.add_parser("week")
    pcw.add_argument("--json", action="store_true")
    pcw.set_defaults(func=cmd_calendar_week)
    pcg = pcal_sub.add_parser("gaps")
    pcg.add_argument("--json", action="store_true")
    pcg.set_defaults(func=cmd_calendar_gaps)
    pcm = pcal_sub.add_parser("mix")
    pcm.set_defaults(func=cmd_calendar_mix)

    # analytics
    pa = sub.add_parser("analytics")
    pa_sub = pa.add_subparsers(dest="sub")
    pat = pa_sub.add_parser("template")
    pat.add_argument("--out", help="Write to this path (otherwise prints)")
    pat.set_defaults(func=cmd_analytics_template)

    # version
    pv = sub.add_parser("version")
    pv.set_defaults(func=cmd_version)

    # doctor
    pdoc = sub.add_parser("doctor", help="Self-health-check")
    pdoc.set_defaults(func=cmd_doctor)

    # postiz
    pp = sub.add_parser("postiz", help="Postiz integration helpers")
    pp_sub = pp.add_subparsers(dest="sub")
    ppv = pp_sub.add_parser("verify", help="Confirm POSTIZ_API_URL+KEY work and list connected channels")
    ppv.set_defaults(func=cmd_postiz_verify)

    return p


def main(argv: list[str] | None = None) -> int:
    init_db()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
