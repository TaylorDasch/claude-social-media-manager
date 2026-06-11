#!/usr/bin/env python3
"""Headless Chrome renderer for May Market Read screen-capture b-roll.

Output modes:
  - video   : 1920x1080 PNG for video b-roll (full-frame cards)
  - doc-png : 816x1056 @ 2x = 1632x2112 PNG of an 8.5x11 print doc for CapCut overlay
  - letter  : 8.5x11 letter-size PDF (printable / emailable)
"""
import subprocess, time
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = Path(__file__).parent.resolve()

ASSETS = [
    # (html, kind, output, mode)
    ("01-mls-dashboard.html",        "png", "01-mls-dashboard.png",                "video"),
    ("02-payment-math.html",         "png", "02-payment-math.png",                 "video"),
    ("03-comp-sheet-helm-lane.html", "pdf", "03-comp-sheet-helm-lane.pdf",         "letter"),
    ("03-comp-sheet-helm-lane.html", "png", "03-comp-sheet-helm-lane.png",         "doc-png"),
    ("04-comp-sheet-high-bluff.html","pdf", "04-comp-sheet-high-bluff.pdf",        "letter"),
    ("04-comp-sheet-high-bluff.html","png", "04-comp-sheet-high-bluff.png",        "doc-png"),
    ("05-comp-sheet-capstan.html",   "pdf", "05-comp-sheet-capstan.pdf",           "letter"),
    ("05-comp-sheet-capstan.html",   "png", "05-comp-sheet-capstan.png",           "doc-png"),
    ("06-disclosure-sellers.html",   "pdf", "06-disclosure-sellers.pdf",           "letter"),
    ("06-disclosure-sellers.html",   "png", "06-disclosure-sellers.png",           "doc-png"),
    ("07-disclosure-lead-paint.html","pdf", "07-disclosure-lead-paint.pdf",        "letter"),
    ("07-disclosure-lead-paint.html","png", "07-disclosure-lead-paint.png",        "doc-png"),
    ("08-disclosure-trec-condo.html","pdf", "08-disclosure-trec-sex-offender.pdf", "letter"),
    ("08-disclosure-trec-condo.html","png", "08-disclosure-trec-sex-offender.png", "doc-png"),
    ("09-end-card.html",             "png", "09-end-card.png",                     "video"),
    ("09-end-card-vintage.html",     "png", "09-end-card-vintage.png",             "video"),
    ("09-end-card-headshot.html",    "png", "09-end-card-headshot.png",            "video"),
    ("10-military-services.html",    "png", "10-military-services.png",            "video"),
    ("11-bah-rates-chart.html",      "png", "11-bah-rates-chart.png",              "video"),
]

def render(html_file, kind, out_file, mode):
    src = HERE / html_file
    dst = HERE / out_file
    url = f"file://{src.as_posix()}"
    base = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars"]
    if kind == "png" and mode == "video":
        cmd = base + ["--window-size=1920,1080", f"--screenshot={dst}", url]
    elif kind == "png" and mode == "doc-png":
        cmd = base + ["--force-device-scale-factor=2",
                      "--window-size=816,1056",
                      f"--screenshot={dst}", url]
    else:  # letter PDF
        cmd = base + ["--no-pdf-header-footer", f"--print-to-pdf={dst}", url]
    print(f"  rendering {html_file} -> {out_file} [{mode}]")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    ok = dst.exists() and dst.stat().st_size > 1024
    print(f"    {'OK' if ok else 'FAIL'} ({dst.stat().st_size if dst.exists() else 0} bytes)")
    if not ok and r.stderr:
        print(f"    stderr: {r.stderr[:300]}")
    return ok

if __name__ == "__main__":
    print(f"Output dir: {HERE}")
    ok = 0
    for html, kind, out, mode in ASSETS:
        if render(html, kind, out, mode):
            ok += 1
        time.sleep(0.3)
    print(f"\nRendered {ok}/{len(ASSETS)} assets.")
