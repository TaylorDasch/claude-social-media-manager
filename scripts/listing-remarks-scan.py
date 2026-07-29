#!/usr/bin/env python3
"""
listing-remarks-scan.py — mine competitors' MLS listing remarks for what THEY volunteer
about a neighborhood, so lifestyle claims in a video are sourced instead of asserted.

WHY THIS EXISTS
---------------
On 2026-07-28, a Morgan's Point Resort video draft claimed "13 of 29 listings mention a boat"
as evidence of storage freedom. Taylor caught it. Eleven of those thirteen hits were the
standardized NeighborhoodAmenities picklist ("Boat Ramp", "Boat Dock") or generic lake-lifestyle
prose. Only two referenced boat parking on the property.

    A KEYWORD HIT IS A LEAD, NOT A FINDING.

So this tool REFUSES to print a bare count. Every match is printed with its surrounding sentence
and its source field, and counts are only ever reported per-field with an explicit
"classify before quoting" banner. The human (or the model) reads the context and decides what
the number actually means before it goes on camera.

USAGE
-----
  python3 listing-remarks-scan.py <csv> --city "Morgans Point Resort" --sub Morgan
  python3 listing-remarks-scan.py <csv> --sub "Pecan Creek" --kw septic,foundation
  python3 listing-remarks-scan.py <csv> --city Salado --json out.json

WHAT'S TRUSTWORTHY, IN ORDER
----------------------------
  1. PublicRemarks / AgentRemarks  — agent PROSE. An agent chose to write this. High signal.
  2. NeighborhoodAmenities         — a PICKLIST. Agent ticked a box, often about the wider area,
                                     frequently copy-pasted between listings. LOW signal.
                                     Never quote a picklist count as if agents "mentioned" something.
"""

import csv, re, sys, json, argparse
from collections import defaultdict

PROSE_FIELDS = ["PublicRemarks", "AgentRemarks"]
PICKLIST_FIELDS = ["NeighborhoodAmenities"]

# category -> regexes. Word-bounded on purpose; substring matching is what caused the original error.
CATEGORIES = {
    "lifestyle":     [r"\btrees?\b", r"\boaks?\b", r"\bpecans?\b", r"\bdeer\b", r"\bwildlife\b",
                      r"\bquiet\b", r"\bsecluded\b", r"\bprivacy\b", r"\bmature\b"],
    "land_use":      [r"\bRV\b", r"\bworkshop\b", r"\bshop\b", r"\bboat\b", r"\bacres?\b",
                      r"\bextra lot\b", r"\badditional lot\b", r"\bcorner lot\b", r"\bshed\b"],
    "infrastructure":[r"\bseptic\b", r"\baerobic\b", r"\bwell water\b", r"\bcity sewer\b",
                      r"\bcity water\b", r"\bpropane\b", r"\bfiber\b", r"\bsolar\b"],
    "water":         [r"\bwaterfront\b", r"\blake ?front\b", r"\blake view\b", r"\blake access\b",
                      r"\bdock\b", r"\bboat ramp\b", r"\bmarina\b", r"\bshoreline\b", r"\bcorps\b"],
    "restrictions":  [r"\bHOA\b", r"\brestrictions?\b", r"\bdeed restrict", r"\bunrestricted\b",
                      r"\bno restrictions?\b", r"\bSUP\b", r"\bshort[- ]term rental\b", r"\bairbnb\b"],
    "condition":     [r"\bfoundation\b", r"\bas[- ]is\b", r"\bupdated\b", r"\bremodel",
                      r"\bnew roof\b", r"\bneeds? work\b", r"\bTLC\b", r"\bfixer\b", r"\bnew HVAC\b"],
    "schools":       [r"\bISD\b", r"\bschool\b"],
}


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        hdr = [h.strip() for h in next(r)]
        seen, H = {}, []
        for h in hdr:                       # CSV has duplicate column names (Address x2)
            if h in seen:
                seen[h] += 1; H.append(f"{h}_{seen[h]}")
            else:
                seen[h] = 0; H.append(h)
        for line in r:
            if len(line) < len(H):
                line += [""] * (len(H) - len(line))
            rows.append(dict(zip(H, line)))
    return rows


def subset(rows, city, sub):
    out = []
    for d in rows:
        c = str(d.get("City", "")).strip().lower()
        s = str(d.get("subdivisionNAME", "")).lower()
        if (city and c == city.lower()) or (sub and sub.lower() in s):
            out.append(d)
    return out


def sentence_around(text, idx, width=110):
    """Return the sentence containing idx, else a window. Sentences beat windows for judging intent."""
    left = max(text.rfind(". ", 0, idx), text.rfind("! ", 0, idx), text.rfind("? ", 0, idx))
    right_candidates = [p for p in (text.find(". ", idx), text.find("! ", idx), text.find("? ", idx)) if p != -1]
    right = min(right_candidates) if right_candidates else -1
    if left != -1 and right != -1 and right - left < 400:
        return text[left + 2:right + 1].strip()
    return text[max(0, idx - width):idx + width].strip()


def scan(listings, cats):
    """hits[category][pattern] = list of (field_kind, field, sentence, street)"""
    hits = defaultdict(lambda: defaultdict(list))
    for d in listings:
        street = str(d.get("StreetName", "")).strip() or "(no street)"
        for kind, fields in (("PROSE", PROSE_FIELDS), ("PICKLIST", PICKLIST_FIELDS)):
            for fld in fields:
                blob = str(d.get(fld, "") or "")
                if not blob.strip():
                    continue
                for cat, pats in cats.items():
                    for pat in pats:
                        for m in re.finditer(pat, blob, re.I):
                            hits[cat][pat].append(
                                (kind, fld, sentence_around(blob, m.start()), street))
    return hits


def main():
    ap = argparse.ArgumentParser(description="Scan MLS listing remarks for neighborhood claims.")
    ap.add_argument("csv")
    ap.add_argument("--city", default=None, help='exact City field match, e.g. "Morgans Point Resort"')
    ap.add_argument("--sub", default=None, help="substring match on subdivisionNAME, e.g. Morgan")
    ap.add_argument("--kw", default=None, help="comma-separated extra keywords -> category 'custom'")
    ap.add_argument("--cat", default=None, help="limit to these categories, comma-separated")
    ap.add_argument("--json", default=None, help="also write structured output here")
    a = ap.parse_args()

    if not a.city and not a.sub:
        sys.exit("Need --city and/or --sub.")

    cats = dict(CATEGORIES)
    if a.cat:
        want = {c.strip() for c in a.cat.split(",")}
        cats = {k: v for k, v in cats.items() if k in want}
    if a.kw:
        cats["custom"] = [rf"\b{re.escape(k.strip())}\b" for k in a.kw.split(",") if k.strip()]

    rows = load(a.csv)
    listings = subset(rows, a.city, a.sub)
    n = len(listings)
    if not n:
        sys.exit("No listings matched that filter.")

    print("=" * 78)
    print(f"LISTING-REMARKS SCAN — {n} listings")
    print(f"  source : {a.csv}")
    print(f"  filter : city={a.city!r} sub={a.sub!r}")
    print("=" * 78)
    print("""
⚠️  A KEYWORD HIT IS A LEAD, NOT A FINDING.
    Read the sentence before any count goes on camera.
    PROSE    = an agent chose to write this. Usable as "N listings mention X".
    PICKLIST = a ticked amenity box, often about the wider area and copy-pasted.
               NEVER report picklist hits as agents "mentioning" something.
""")

    out = {}
    for cat in cats:
        if not hits_present(cats, cat):
            pass
    hits = scan(listings, cats)

    for cat in cats:
        if cat not in hits:
            continue
        print(f"\n{'─'*78}\n## {cat.upper()}\n{'─'*78}")
        for pat, entries in sorted(hits[cat].items(), key=lambda kv: -len(kv[1])):
            prose = [e for e in entries if e[0] == "PROSE"]
            pick = [e for e in entries if e[0] == "PICKLIST"]
            prose_listings = len({e[3] for e in prose})
            label = re.sub(r"\\b|\\", "", pat)
            print(f"\n  ▸ {label!r}")
            print(f"      PROSE: {len(prose)} match(es) across ~{prose_listings} listing(s)"
                  f"   |   PICKLIST: {len(pick)} match(es)  ← do not quote as 'mentions'")
            for kind, fld, sent, street in prose[:6]:
                print(f"        · [{street}] {sent[:190]}")
            if len(prose) > 6:
                print(f"        · … {len(prose)-6} more prose match(es)")
            if pick and not prose:
                print(f"        · (picklist only — likely an area amenity, not a property feature)")
            out.setdefault(cat, {})[label] = {
                "prose_matches": len(prose),
                "prose_listings_approx": prose_listings,
                "picklist_matches": len(pick),
                "total_listings_scanned": n,
                "examples": [{"street": s, "field": f, "text": t} for _, f, t, s in prose[:10]],
            }

    print(f"\n{'='*78}")
    print("REPORTING RULE — copy this into the video's ground-truth file:")
    print('  ✅ "11 of 29 listings mention mature trees" — if 11 PROSE listings matched.')
    print('  ❌ "13 of 29 mention a boat"                — if most hits were picklist/lifestyle prose.')
    print("  When prose and picklist disagree, quote prose and footnote the picklist.")
    print("=" * 78)

    if a.json:
        with open(a.json, "w") as f:
            json.dump({"listings_scanned": n, "filter": {"city": a.city, "sub": a.sub},
                       "categories": out}, f, indent=2)
        print(f"\nStructured output → {a.json}")


def hits_present(cats, cat):
    return cat in cats


if __name__ == "__main__":
    main()
