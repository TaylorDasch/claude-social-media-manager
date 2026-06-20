#!/usr/bin/env python3
"""Headless-Chrome renderer: every html/ file -> png/ at 3840x2160 (2x).
Transparent assets (lower thirds / street strips / ISD) get an alpha background."""
import subprocess, time, os
from pathlib import Path

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE=Path(__file__).parent.resolve()
HTMLDIR=HERE/"html"; PNGDIR=HERE/"png"; PNGDIR.mkdir(exist_ok=True)

# transparent overlays: filename prefixes that should keep an alpha background
TRANSPARENT_PREFIXES=("LT_","ST_","ISD_")

def is_transparent(stem): return stem.startswith(TRANSPARENT_PREFIXES)

def render(html_path):
    stem=html_path.stem
    out=PNGDIR/f"{stem}.png"
    url=f"file://{html_path.as_posix()}"
    cmd=[CHROME,"--headless=new","--disable-gpu","--no-sandbox","--hide-scrollbars",
         "--force-device-scale-factor=2","--window-size=1920,1080"]
    if is_transparent(stem):
        cmd+=["--default-background-color=00000000"]
    cmd+=[f"--screenshot={out}",url]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
    ok=out.exists() and out.stat().st_size>2048
    print(f"  {'OK ' if ok else 'FAIL'} {stem:<20} {out.stat().st_size//1024 if out.exists() else 0} KB")
    if not ok and r.stderr: print("     ",r.stderr[:200])
    return ok

if __name__=="__main__":
    files=sorted(HTMLDIR.glob("*.html"))
    print(f"Rendering {len(files)} files -> {PNGDIR}")
    ok=0
    for f in files:
        if render(f): ok+=1
        time.sleep(0.25)
    print(f"\nRendered {ok}/{len(files)} PNGs.")
