#!/usr/bin/env python3
"""Render every html/ file to png/ at 3840x2160 using headless Chrome."""
import subprocess
import time
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = Path(__file__).parent.resolve()
HTMLDIR = HERE / "html"
PNGDIR = HERE / "png"
PNGDIR.mkdir(exist_ok=True)

TRANSPARENT_PREFIXES = ("LT-",)


def is_transparent(stem: str) -> bool:
    return stem.startswith(TRANSPARENT_PREFIXES)


def render(html_path: Path) -> bool:
    stem = html_path.stem
    out = PNGDIR / f"{stem}.png"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        "--window-size=1920,1080",
    ]
    if is_transparent(stem):
        cmd.append("--default-background-color=00000000")
    cmd.extend([f"--screenshot={out}", f"file://{html_path.as_posix()}"])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    ok = out.exists() and out.stat().st_size > 2048
    size_kb = out.stat().st_size // 1024 if out.exists() else 0
    print(f"  {'OK ' if ok else 'FAIL'} {stem:<30} {size_kb:>5} KB")
    if not ok:
        print(result.stderr[:600])
    return ok


if __name__ == "__main__":
    files = sorted(HTMLDIR.glob("*.html"))
    print(f"Rendering {len(files)} files -> {PNGDIR}")
    ok = 0
    for html in files:
        if render(html):
            ok += 1
        time.sleep(0.2)
    print(f"\nRendered {ok}/{len(files)} PNGs.")
