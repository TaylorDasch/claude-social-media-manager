#!/usr/bin/env python3
"""
build_deck.py — assemble a fully self-contained editorial deck with REAL FEATURED IMAGES.

9 cards, each in a magazine-spread layout: full-bleed hero, 60/40 split, or
two-photo grid. All photos resized to 1280-wide JPEG (quality 78) and inlined
as base64 data URIs. Zero external image fetches.
"""
from __future__ import annotations
import base64
import subprocess
from pathlib import Path

GRAPHICS = Path("/Users/taylordasch_1/claude-social-media-manager/yt-videos/omega-builders-deep-dive/graphics")
OUT_HTML = GRAPHICS / "14-lower-thirds-deck.html"
TMP = Path("/tmp/omega-deck"); TMP.mkdir(exist_ok=True)

# ============ IMAGE SOURCES ============
# Each key is referenced by HTML below as {img['key']}.
IMG_SOURCES = {
    "aerial":       "11-aerial-broll.png",
    "cottage":      "img-cottage-home.png",
    "family":       "img-family-home.png",
    "kitchen":      "12-premium-kitchen-broll.png",
    "quartz":       "img-quartz-detail.png",
    "topo":         "bg-05-topo.png",
    "calculator":   "img-calculator.png",
    "vintage":      "img-vintage-home.png",
    "doorway":      "img-doorway.png",
    "twilight":     "bg-09-twilight.png",
    "marble":       "bg-08-marble.png",
}

def encode(key: str, src_name: str) -> str:
    src = GRAPHICS / src_name
    if not src.exists(): raise FileNotFoundError(src)
    jpg = TMP / f"{key}.jpg"
    subprocess.run(
        ["sips", "-Z", "1400",
         "-s", "format", "jpeg",
         "-s", "formatOptions", "78",
         str(src), "--out", str(jpg)],
        check=True, capture_output=True,
    )
    raw = jpg.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    print(f"  {key:<12} {src_name:<35} → {len(raw)//1024:>4}KB raw / {len(b64)//1024:>4}KB base64")
    return b64

print("Encoding photos…")
B64 = {k: encode(k, v) for k, v in IMG_SOURCES.items()}
total = sum(len(v) for v in B64.values())
print(f"Total embedded: {total/1024/1024:.2f}MB base64")

def img(k: str) -> str:
    return f"data:image/jpeg;base64,{B64[k]}"

# ============ HTML ============
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Omega Builders — Editorial Deck</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Outfit:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{
  --midnight:#0b1220;--midnight-2:#0f172a;--midnight-3:#1e293b;
  --emerald:#059669;--emerald-bright:#10b981;
  --gold:#d4af37;--amber:#f59e0b;
  --cream:#f8fafc;--cream-2:#e2e8f0;--cream-dim:#94a3b8;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden;background:#000;font-family:'Outfit',sans-serif;color:var(--cream);-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}
body{{display:grid;place-items:center}}

.stage{{position:relative;width:100vw;height:100vh;max-width:calc(100vh*16/9);max-height:calc(100vw*9/16);background:var(--midnight);overflow:hidden;box-shadow:0 0 80px rgba(0,0,0,.85)}}

/* CARDS */
.card{{position:absolute;inset:0;opacity:0;visibility:hidden;transition:opacity .9s cubic-bezier(.6,.05,.2,1),visibility 0s linear .9s;background:var(--midnight);overflow:hidden}}
.card.show{{opacity:1;visibility:visible;transition:opacity .9s cubic-bezier(.6,.05,.2,1),visibility 0s linear 0s}}

/* PHOTO CELLS — ken burns motion */
.photo{{position:absolute;background-size:cover;background-position:center;filter:saturate(.92) contrast(1.05);overflow:hidden}}
.photo .ph-img{{position:absolute;inset:0;background-size:cover;background-position:center;transform:scale(1.04);transition:transform 14s linear}}
.card.show .photo .ph-img{{transform:scale(1.18) translate(-1.5%, 1%)}}

/* LAYOUT TYPES */
.type-hero .photo{{inset:0}}
.type-hero .panel{{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:flex-start;padding:120px}}
.type-hero.center .panel{{align-items:center;justify-content:center;text-align:center;padding:120px 160px}}

.type-split-text-photo .photo{{top:0;right:0;bottom:0;width:42%;border-left:1px solid rgba(212,175,55,.25)}}
.type-split-text-photo .panel{{position:absolute;top:0;left:0;bottom:0;width:58%;display:flex;align-items:center;padding:120px 100px 120px 200px;text-align:left;justify-content:flex-start}}

.type-split-photo-text .photo{{top:0;left:0;bottom:0;width:42%;border-right:1px solid rgba(212,175,55,.25)}}
.type-split-photo-text .panel{{position:absolute;top:0;right:0;bottom:0;width:58%;display:flex;align-items:center;padding:120px 200px 120px 100px;text-align:left;justify-content:flex-start}}

.type-grid-2 .photo.left{{top:120px;left:140px;bottom:340px;width:calc(50% - 180px);border:1px solid rgba(212,175,55,.3)}}
.type-grid-2 .photo.right{{top:120px;right:140px;bottom:340px;width:calc(50% - 180px);border:1px solid rgba(212,175,55,.3)}}
.type-grid-2 .panel{{position:absolute;left:0;right:0;bottom:80px;top:auto;display:flex;justify-content:center;align-items:flex-start;padding:0 140px}}
.type-grid-2 .grid-2-spec{{display:grid;grid-template-columns:1fr 1px 1fr;gap:80px;width:100%;max-width:1200px;align-items:start}}
.type-grid-2 .grid-2-spec .div{{background:linear-gradient(180deg,transparent,var(--emerald),transparent);height:140px;align-self:center;box-shadow:0 0 8px rgba(5,150,105,.4)}}
.type-grid-2 .col{{text-align:center}}
.type-grid-2 .col-name{{font-family:'Cormorant Garamond';font-weight:600;font-size:46px;color:var(--gold);line-height:1;margin-bottom:6px;text-shadow:0 4px 16px rgba(0,0,0,.7)}}
.type-grid-2 .col-tag{{font-family:'Outfit';font-size:11px;letter-spacing:.4em;color:var(--cream-dim);text-transform:uppercase;margin-bottom:18px}}
.type-grid-2 .col-price{{font-family:'Cormorant Garamond';font-weight:700;font-size:60px;color:var(--emerald-bright);line-height:1;margin-bottom:14px;text-shadow:0 4px 20px rgba(0,0,0,.7)}}
.type-grid-2 .col-spec{{font-family:'Outfit';font-size:12px;letter-spacing:.32em;color:var(--cream);text-transform:uppercase;font-weight:500;margin-bottom:6px;text-shadow:0 2px 8px rgba(0,0,0,.7)}}

.type-hero-full .photo{{inset:0}}
.type-hero-full .panel{{position:absolute;left:0;right:0;bottom:0;padding:80px 140px 100px;background:linear-gradient(180deg,transparent 0%,rgba(11,18,32,.4) 30%,rgba(11,18,32,.92) 100%);display:flex;align-items:flex-end;justify-content:space-between}}

/* SHADE OVERLAYS */
.shade-photo{{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(11,18,32,.15) 0%,rgba(11,18,32,.55) 100%)}}
.shade-panel{{position:absolute;inset:0;pointer-events:none}}
.shade-panel.left-text{{background:linear-gradient(90deg,rgba(11,18,32,.94) 0%,rgba(11,18,32,.85) 50%,rgba(11,18,32,.4) 100%)}}
.shade-panel.right-text{{background:linear-gradient(270deg,rgba(11,18,32,.94) 0%,rgba(11,18,32,.85) 50%,rgba(11,18,32,.4) 100%)}}
.shade-panel.bottom{{background:linear-gradient(180deg,rgba(11,18,32,.2) 0%,rgba(11,18,32,.45) 50%,rgba(11,18,32,.92) 100%)}}
.shade-panel.heavy{{background:radial-gradient(ellipse at center,rgba(11,18,32,.55) 0%,rgba(11,18,32,.92) 100%)}}

.grain{{position:absolute;inset:0;z-index:3;opacity:.07;mix-blend-mode:overlay;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='1.8' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")}}

/* CHROME */
.chrome-frame{{position:absolute;inset:36px;border:1px solid rgba(248,250,252,.06);pointer-events:none;z-index:5}}
.corner{{position:absolute;width:16px;height:16px;border:1.5px solid var(--gold)}}
.corner.tl{{top:-1px;left:-1px;border-right:0;border-bottom:0}}
.corner.tr{{top:-1px;right:-1px;border-left:0;border-bottom:0}}
.corner.bl{{bottom:-1px;left:-1px;border-right:0;border-top:0}}
.corner.br{{bottom:-1px;right:-1px;border-left:0;border-top:0}}
.chapter{{position:absolute;left:62px;top:50%;transform:translateY(-50%) rotate(-90deg);transform-origin:left center;z-index:6;font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:13px;letter-spacing:.55em;color:var(--gold);text-transform:uppercase;white-space:nowrap}}
.chapter::after{{content:"";display:inline-block;width:56px;height:1px;background:var(--gold);margin-left:20px;vertical-align:middle}}
.monogram{{position:absolute;top:54px;right:54px;z-index:6;font-family:'Cormorant Garamond';font-style:italic;font-weight:600;font-size:17px;color:var(--gold);letter-spacing:.05em;display:flex;align-items:center;gap:12px}}
.monogram::before{{content:"";width:24px;height:1px;background:var(--gold)}}
.page-index{{position:absolute;bottom:54px;right:54px;z-index:6;font-family:'Outfit';font-size:10px;letter-spacing:.4em;color:var(--cream-dim);text-transform:uppercase}}
.page-index strong{{color:var(--cream);font-weight:500}}
.shot-badge{{position:absolute;top:54px;right:54px;z-index:7;background:rgba(245,158,11,.18);border:1px solid var(--amber);padding:11px 20px;font-family:'Outfit';font-size:10px;letter-spacing:.5em;color:var(--amber);text-transform:uppercase;font-weight:600;display:none;backdrop-filter:blur(8px)}}
.card.warn .shot-badge{{display:block}}
.card.warn .monogram{{display:none}}

/* PANEL CONTENT */
.panel{{z-index:10}}
.panel-content{{max-width:760px}}
.panel-content.wide{{max-width:1100px}}

/* TYPE */
.fade-in{{opacity:0;transform:translateY(20px);transition:opacity 1.1s cubic-bezier(.4,0,.2,1),transform 1.1s cubic-bezier(.4,0,.2,1)}}
.card.show .fade-in{{opacity:1;transform:translateY(0)}}
.card.show .fade-in.d1{{transition-delay:.22s}}
.card.show .fade-in.d2{{transition-delay:.44s}}
.card.show .fade-in.d3{{transition-delay:.66s}}
.card.show .fade-in.d4{{transition-delay:.88s}}
.card.show .fade-in.d5{{transition-delay:1.1s}}
.eyebrow{{font-family:'Outfit';font-size:11px;letter-spacing:.55em;color:var(--gold);text-transform:uppercase;font-weight:500;margin-bottom:24px;text-shadow:0 2px 10px rgba(0,0,0,.7)}}
.eyebrow.amber{{color:var(--amber)}}
.headline{{font-family:'Cormorant Garamond';font-weight:600;font-size:96px;line-height:.95;color:var(--cream);letter-spacing:.005em;text-shadow:0 4px 20px rgba(0,0,0,.7)}}
.headline.med{{font-size:78px}}
.headline.sml{{font-size:60px}}
.subhead{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:30px;color:var(--emerald-bright);letter-spacing:.01em;line-height:1.3;margin-top:14px;text-shadow:0 2px 12px rgba(0,0,0,.6)}}
.rule{{width:64px;height:2px;background:var(--emerald);margin:24px 0;box-shadow:0 0 8px rgba(5,150,105,.5)}}
.type-hero.center .rule, .type-hero-full .rule{{margin-left:auto;margin-right:auto}}
.stat-row{{display:flex;gap:44px;margin-top:34px;flex-wrap:wrap}}
.type-hero.center .stat-row{{justify-content:center}}
.stat{{font-family:'Outfit';font-size:13px;letter-spacing:.32em;color:var(--cream);text-transform:uppercase;font-weight:500;text-shadow:0 2px 8px rgba(0,0,0,.7)}}
.stat .em{{color:var(--emerald-bright);font-weight:700}}
.stat .gold{{color:var(--gold);font-weight:700}}
.stat .lg{{font-family:'Cormorant Garamond';font-weight:600;font-size:30px;letter-spacing:.02em;display:block;margin-bottom:6px}}
.caption{{font-family:'Cormorant Garamond';font-style:italic;font-weight:400;font-size:22px;color:var(--cream-2);line-height:1.45;margin-top:30px;max-width:680px;text-shadow:0 2px 12px rgba(0,0,0,.6)}}
.big-num{{font-family:'Cormorant Garamond';font-weight:700;font-size:240px;line-height:.85;color:var(--emerald-bright);letter-spacing:-.025em;text-shadow:0 8px 40px rgba(0,0,0,.7)}}
.big-num.gold{{color:var(--gold)}}
.big-num.amber{{color:var(--amber)}}
.range{{font-family:'Cormorant Garamond';font-weight:600;font-size:140px;line-height:1;color:var(--emerald-bright);letter-spacing:-.01em;display:flex;align-items:baseline;gap:32px;text-shadow:0 6px 30px rgba(0,0,0,.7)}}
.range .dash{{color:var(--gold);font-weight:400}}

/* COMM-LIST */
.comm-list{{display:flex;flex-direction:column;width:100%;max-width:920px;margin:24px auto 0}}
.comm-row{{display:grid;grid-template-columns:50px 1fr auto auto;align-items:baseline;gap:22px;padding:14px 0;border-bottom:1px solid rgba(212,175,55,.22)}}
.comm-row:last-child{{border-bottom:0}}
.comm-row .rn{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:30px;color:var(--emerald-bright);text-align:right;text-shadow:0 2px 8px rgba(0,0,0,.7)}}
.comm-row .name{{font-family:'Cormorant Garamond';font-weight:600;font-size:34px;color:var(--cream);text-align:left;text-shadow:0 2px 12px rgba(0,0,0,.7)}}
.comm-row .isd{{font-family:'Outfit';font-size:11px;letter-spacing:.3em;color:var(--cream-dim);text-transform:uppercase}}
.comm-row .tier{{font-family:'Outfit';font-size:11px;letter-spacing:.3em;color:var(--gold);text-transform:uppercase;border-left:1px solid rgba(212,175,55,.4);padding-left:18px;min-width:120px;text-align:right}}
.comm-row.amber-row .tier{{color:var(--amber)}}
.comm-row.gold-row .tier{{color:var(--gold)}}

/* CTA */
.cta-strip{{display:flex;gap:34px;align-items:center;margin-top:34px;flex-wrap:wrap}}
.type-hero.center .cta-strip{{justify-content:center}}
.cta-strip .cta-item{{font-family:'Outfit';font-size:13px;letter-spacing:.35em;color:var(--emerald-bright);text-transform:uppercase;font-weight:500;text-shadow:0 2px 10px rgba(0,0,0,.7)}}
.cta-strip .cta-sep{{color:var(--gold);opacity:.6}}

/* PAYMENT BREAKDOWN GRID */
.pay-num{{font-family:'Cormorant Garamond';font-weight:700;font-size:200px;line-height:.85;color:var(--gold);letter-spacing:-.02em;text-shadow:0 8px 40px rgba(0,0,0,.7);display:flex;align-items:baseline;justify-content:center;gap:4px}}
.pay-num .mo{{font-family:'Outfit';font-size:32px;color:var(--cream-dim);font-weight:300;letter-spacing:.12em;text-transform:uppercase;text-shadow:0 2px 10px rgba(0,0,0,.7)}}
.pay-grid{{display:grid;grid-template-columns:1fr auto;gap:18px 80px;max-width:760px;margin:36px auto 0;text-align:left;align-items:baseline}}
.pay-grid .label{{font-family:'Outfit';font-size:15px;letter-spacing:.18em;color:var(--cream-2);text-transform:uppercase;font-weight:400;text-shadow:0 2px 8px rgba(0,0,0,.7)}}
.pay-grid .label .small{{font-size:11px;color:var(--cream-dim);letter-spacing:.22em;display:block;margin-top:3px}}
.pay-grid .val{{font-family:'Cormorant Garamond';font-weight:600;font-size:30px;color:var(--emerald-bright);text-align:right;text-shadow:0 2px 10px rgba(0,0,0,.7)}}
.pay-grid .total-label{{padding-top:18px;margin-top:6px;border-top:1px solid rgba(212,175,55,.4);color:var(--gold);font-weight:600}}
.pay-grid .total-val{{padding-top:18px;margin-top:6px;border-top:1px solid rgba(212,175,55,.4);color:var(--gold);font-weight:700}}
.pay-spec{{display:flex;justify-content:center;gap:42px;margin-top:24px;flex-wrap:wrap}}
.pay-spec .stat{{font-family:'Outfit';font-size:11px;letter-spacing:.32em;color:var(--cream-dim);text-transform:uppercase;font-weight:500;text-shadow:0 2px 8px rgba(0,0,0,.7)}}
.pay-spec .stat .em{{color:var(--gold);font-weight:600}}

/* HUD / NAV */
.hud{{position:fixed;top:14px;left:14px;z-index:100;background:rgba(15,23,42,.92);border:1px solid rgba(5,150,105,.4);padding:8px 14px;font-family:'Outfit';font-size:10px;letter-spacing:.25em;color:var(--emerald-bright);text-transform:uppercase;font-weight:500}}
.nav{{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);z-index:100;display:flex;gap:6px;background:rgba(15,23,42,.92);border:1px solid rgba(5,150,105,.35);padding:6px}}
.nav button{{background:transparent;border:1px solid transparent;color:var(--cream);font-family:'Outfit';font-size:11px;letter-spacing:.18em;padding:8px 14px;cursor:pointer;text-transform:uppercase;transition:all .15s}}
.nav button:hover{{border-color:var(--emerald);color:var(--emerald-bright)}}
.nav button.active{{background:var(--emerald);color:var(--midnight)}}
.help{{position:fixed;bottom:14px;right:14px;z-index:100;font-family:'Outfit';font-size:9px;letter-spacing:.22em;color:var(--cream-dim);text-transform:uppercase;background:rgba(15,23,42,.85);padding:8px 12px;border:1px solid rgba(248,250,252,.08)}}
body.clean .hud,body.clean .nav,body.clean .help,body.clean .progress{{display:none !important}}
.progress{{position:absolute;top:0;left:0;height:2px;width:0%;background:linear-gradient(90deg,var(--emerald),var(--gold));z-index:50;transition:width .1s linear}}
</style>
</head>
<body>
<div class="stage">

<!-- ================================================================ -->
<!-- I — TITLE (Hero full-bleed: aerial drone)                         -->
<!-- ================================================================ -->
<div class="card show type-hero-full" data-card="1">
  <div class="photo"><div class="ph-img" style="background-image:url({img('aerial')})"></div></div>
  <div class="shade-panel bottom"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter I</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>01</strong> / 11</div>
  <div class="panel">
    <div class="panel-content wide">
      <div class="eyebrow fade-in">Omega Builders · Temple, Texas · 2026</div>
      <div class="headline fade-in d1">A Deep Dive</div>
      <div class="rule fade-in d2"></div>
      <div class="subhead fade-in d3">into the most-asked-about builder in Bell County</div>
    </div>
    <div class="fade-in d4" style="font-family:'Outfit';font-size:13px;letter-spacing:.45em;text-transform:uppercase;font-weight:300;color:var(--cream-dim);text-align:right">Episode<br>Living in Temple</div>
  </div>
</div>

<!-- ================================================================ -->
<!-- II — PRICE RANGE (text left, quartz-detail photo right)           -->
<!-- ================================================================ -->
<div class="card type-split-text-photo" data-card="2">
  <div class="photo"><div class="ph-img" style="background-image:url({img('quartz')})"></div></div>
  <div class="shade-panel left-text"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter II</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>02</strong> / 11</div>
  <div class="panel"><div class="panel-content">
    <div class="eyebrow fade-in">Starting Price Range</div>
    <div class="range fade-in d1"><span>$230K</span><span class="dash">—</span><span>$350K</span></div>
    <div class="rule fade-in d2"></div>
    <div class="subhead fade-in d3" style="color:var(--cream)">10 floor plans · 6 series</div>
    <div class="caption fade-in d4">From the Cottage Series Riley to the Medallion III — the widest tier ladder of any builder in Temple.</div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- III — COTTAGE LADDER (two-photo grid: Riley + Finley)             -->
<!-- ================================================================ -->
<div class="card type-grid-2" data-card="3">
  <div class="photo left"><div class="ph-img" style="background-image:url({img('cottage')})"></div></div>
  <div class="photo right"><div class="ph-img" style="background-image:url({img('family')})"></div></div>
  <div class="shade-panel" style="background:linear-gradient(180deg,rgba(11,18,32,0) 0%,rgba(11,18,32,0) 50%,rgba(11,18,32,.6) 75%,rgba(11,18,32,.95) 100%)"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter III</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>03</strong> / 11</div>
  <!-- header strip -->
  <div style="position:absolute;top:48px;left:0;right:0;text-align:center;z-index:10">
    <div class="eyebrow fade-in" style="margin-bottom:8px">The Cottage Series Ladder</div>
  </div>
  <div class="panel">
    <div class="grid-2-spec fade-in d2">
      <div class="col">
        <div class="col-name">Riley</div>
        <div class="col-tag">Day-One House</div>
        <div class="col-price">$249,900</div>
        <div class="col-spec">3 Bed · 2 Bath</div>
        <div class="col-spec">~1,400 SQ FT</div>
      </div>
      <div class="div"></div>
      <div class="col">
        <div class="col-name">Finley</div>
        <div class="col-tag">Year-Five House</div>
        <div class="col-price">$360,900</div>
        <div class="col-spec">4 Bed · 2 Bath</div>
        <div class="col-spec">~1,800 SQ FT</div>
      </div>
    </div>
  </div>
</div>

<!-- ================================================================ -->
<!-- IV — THREE CREEKS (Hero full-bleed: kitchen)                      -->
<!-- ================================================================ -->
<div class="card type-hero center" data-card="4">
  <div class="photo"><div class="ph-img" style="background-image:url({img('kitchen')})"></div></div>
  <div class="shade-panel heavy"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter IV</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>04</strong> / 11</div>
  <div class="panel"><div class="panel-content">
    <div class="eyebrow fade-in">Community 02 · Premium Tier</div>
    <div class="headline fade-in d1">Three Creeks</div>
    <div class="rule fade-in d2" style="background:var(--gold);box-shadow:0 0 8px rgba(212,175,55,.5)"></div>
    <div class="subhead fade-in d3">Where Omega's craft actually shows up.</div>
    <div class="stat-row fade-in d4">
      <div class="stat"><span class="lg em">Quartz</span>Counters</div>
      <div class="stat"><span class="lg em">Tray</span>Ceilings</div>
      <div class="stat"><span class="lg em">Floor-to-Ceiling</span>Windows</div>
    </div>
    <div class="fade-in d5" style="margin-top:38px;font-family:'Outfit';font-size:13px;letter-spacing:.45em;text-transform:uppercase;font-weight:300;color:var(--gold)">Belton ISD  ·  Premium Tier</div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- V — FIVE COMMUNITIES (Hero full-bleed topo + list overlay)        -->
<!-- ================================================================ -->
<div class="card type-hero center" data-card="5">
  <div class="photo"><div class="ph-img" style="background-image:url({img('topo')})"></div></div>
  <div class="shade-panel heavy"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter V</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>05</strong> / 11</div>
  <div class="panel"><div class="panel-content wide" style="text-align:center">
    <div class="eyebrow fade-in">The Footprint</div>
    <div class="headline med fade-in d1">Five Communities</div>
    <div class="rule fade-in d2"></div>
    <div class="comm-list fade-in d3">
      <div class="comm-row amber-row"><div class="rn">i.</div><div class="name">North Pointe</div><div class="isd">Belton ISD</div><div class="tier">+0.14% PID</div></div>
      <div class="comm-row"><div class="rn">ii.</div><div class="name">Hartrick Ranch</div><div class="isd">Academy ISD</div><div class="tier">Cottage Series</div></div>
      <div class="comm-row"><div class="rn">iii.</div><div class="name">Hills of Westwood</div><div class="isd">Temple ISD</div><div class="tier">Mid-Tier</div></div>
      <div class="comm-row"><div class="rn">iv.</div><div class="name">Hillside Village</div><div class="isd">Temple ISD</div><div class="tier">Mid-Tier</div></div>
      <div class="comm-row gold-row"><div class="rn">v.</div><div class="name">Three Creeks</div><div class="isd">Belton ISD</div><div class="tier">Premium</div></div>
    </div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- VI — PID WARNING (calculator photo left, text right)              -->
<!-- ================================================================ -->
<div class="card warn type-split-photo-text" data-card="6">
  <div class="photo"><div class="ph-img" style="background-image:url({img('calculator')})"></div></div>
  <div class="shade-panel right-text"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl" style="border-color:var(--amber)"></div><div class="corner tr" style="border-color:var(--amber)"></div><div class="corner bl" style="border-color:var(--amber)"></div><div class="corner br" style="border-color:var(--amber)"></div></div>
  <div class="chapter" style="color:var(--amber)">Chapter VI · Tax Trap</div>
  <div class="shot-badge">Screenshot This</div>
  <div class="page-index"><strong>06</strong> / 11</div>
  <div class="panel"><div class="panel-content">
    <div class="eyebrow amber fade-in">North Pointe · Public Improvement District</div>
    <div class="big-num amber fade-in d1" style="font-size:200px">+0.14%</div>
    <div class="rule fade-in d2" style="background:var(--amber);box-shadow:0 0 8px rgba(245,158,11,.5)"></div>
    <div class="subhead fade-in d3" style="color:var(--cream)">PID add-on — on top of standard property tax</div>
    <div class="caption fade-in d4">On a $300,000 home — roughly <span style="color:var(--amber);font-weight:600;font-style:normal">$420 / year</span> extra. Verify before you offer.</div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- VII — 55 YEARS (Hero full-bleed vintage brick home)                -->
<!-- ================================================================ -->
<div class="card type-hero center" data-card="7">
  <div class="photo"><div class="ph-img" style="background-image:url({img('vintage')})"></div></div>
  <div class="shade-panel heavy"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter VII · Track Record</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>07</strong> / 11</div>
  <div class="panel"><div class="panel-content">
    <div class="eyebrow fade-in">Omega Builders · In Temple Since 1971</div>
    <div class="big-num gold fade-in d1">55</div>
    <div class="rule fade-in d2" style="background:var(--gold);box-shadow:0 0 8px rgba(212,175,55,.5)"></div>
    <div class="fade-in d3" style="font-family:'Outfit';font-size:16px;letter-spacing:.4em;text-transform:uppercase;font-weight:300;color:var(--cream);margin-top:6px;text-shadow:0 2px 10px rgba(0,0,0,.7)">Years Building in Temple, Texas</div>
    <div class="caption fade-in d4">Subcontractors locked. Process dialed.<br><span style="color:var(--gold);font-weight:500;font-style:normal;font-family:'Outfit';letter-spacing:.2em;text-transform:uppercase;font-size:13px">The same trade crews on every job.</span></div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- VIII — RESIDENT PROGRAM (text left, doorway photo right)           -->
<!-- ================================================================ -->
<div class="card type-split-text-photo" data-card="8">
  <div class="photo"><div class="ph-img" style="background-image:url({img('doorway')})"></div></div>
  <div class="shade-panel left-text"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter VIII · Financing</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>08</strong> / 11</div>
  <div class="panel"><div class="panel-content">
    <div class="eyebrow fade-in">Incoming to Temple for Residency</div>
    <div class="headline med fade-in d1">Specialty Financing</div>
    <div class="rule fade-in d2"></div>
    <div class="stat-row fade-in d3" style="margin-top:36px">
      <div class="stat"><span class="lg em">0%</span>Down</div>
      <div class="stat"><span class="lg em">No</span>PMI</div>
      <div class="stat"><span class="lg em">3%</span>Concessions</div>
    </div>
    <div class="caption fade-in d4">Programs designed for medical professionals starting their careers.<br><span style="color:var(--gold);font-family:'Outfit';font-weight:500;letter-spacing:.28em;text-transform:uppercase;font-size:12px;font-style:normal">Lender introduction available on request.</span></div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- IX — $240K MONTHLY PAYMENT (financial statement layout)            -->
<!-- ================================================================ -->
<div class="card type-hero center" data-card="9">
  <div class="photo"><div class="ph-img" style="background-image:url({img('marble')})"></div></div>
  <div class="shade-panel heavy"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter IX · Buying Power</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>09</strong> / 11</div>
  <div class="panel"><div class="panel-content wide">
    <div class="eyebrow fade-in">Resident Loan Estimate · $240,000 Purchase</div>
    <div class="pay-num fade-in d1"><span>$1,857</span><span class="mo">/ month</span></div>
    <div class="rule fade-in d2" style="background:var(--gold);box-shadow:0 0 8px rgba(212,175,55,.5)"></div>
    <div class="pay-spec fade-in d2">
      <div class="stat"><span class="em">4.99%</span> · Rate</div>
      <div class="stat"><span class="em">$0</span> · Down</div>
      <div class="stat"><span class="em">30</span> · Year Fixed</div>
      <div class="stat"><span class="em">$0</span> · Out of Pocket</div>
    </div>
    <div class="pay-grid fade-in d3">
      <div class="label">Principal &amp; Interest <span class="small">$240K @ 4.99% / 360 mo</span></div><div class="val">$1,287</div>
      <div class="label">Property Tax <span class="small">Bell County homestead ~2.1%</span></div><div class="val">$420</div>
      <div class="label">Homeowner's Insurance <span class="small">est. Texas standard</span></div><div class="val">$150</div>
      <div class="label total-label">Estimated Monthly Payment</div><div class="val total-val">$1,857</div>
    </div>
    <div class="caption fade-in d4" style="font-size:18px;margin-top:28px;text-align:center">$0 out of pocket via DPA + builder incentives.<br><span style="color:var(--gold);font-style:normal;font-family:'Outfit';font-size:11px;letter-spacing:.35em;text-transform:uppercase;font-weight:500">Estimate · Depends on Current Incentives</span></div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- X — $275K MONTHLY PAYMENT (financial statement layout)             -->
<!-- ================================================================ -->
<div class="card type-hero center" data-card="10">
  <div class="photo"><div class="ph-img" style="background-image:url({img('marble')})"></div></div>
  <div class="shade-panel heavy"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter X · Buying Power</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>10</strong> / 11</div>
  <div class="panel"><div class="panel-content wide">
    <div class="eyebrow fade-in">Resident Loan Estimate · $275,000 Purchase</div>
    <div class="pay-num fade-in d1"><span>$2,121</span><span class="mo">/ month</span></div>
    <div class="rule fade-in d2" style="background:var(--gold);box-shadow:0 0 8px rgba(212,175,55,.5)"></div>
    <div class="pay-spec fade-in d2">
      <div class="stat"><span class="em">4.99%</span> · Rate</div>
      <div class="stat"><span class="em">$0</span> · Down</div>
      <div class="stat"><span class="em">30</span> · Year Fixed</div>
      <div class="stat"><span class="em">$0</span> · Out of Pocket</div>
    </div>
    <div class="pay-grid fade-in d3">
      <div class="label">Principal &amp; Interest <span class="small">$275K @ 4.99% / 360 mo</span></div><div class="val">$1,475</div>
      <div class="label">Property Tax <span class="small">Bell County homestead ~2.1%</span></div><div class="val">$481</div>
      <div class="label">Homeowner's Insurance <span class="small">est. Texas standard</span></div><div class="val">$165</div>
      <div class="label total-label">Estimated Monthly Payment</div><div class="val total-val">$2,121</div>
    </div>
    <div class="caption fade-in d4" style="font-size:18px;margin-top:28px;text-align:center">$0 out of pocket via DPA + builder incentives.<br><span style="color:var(--gold);font-style:normal;font-family:'Outfit';font-size:11px;letter-spacing:.35em;text-transform:uppercase;font-weight:500">Estimate · Depends on Current Incentives</span></div>
  </div></div>
</div>

<!-- ================================================================ -->
<!-- XI — CTA (Hero full-bleed twilight aerial)                         -->
<!-- ================================================================ -->
<div class="card type-hero center" data-card="11">
  <div class="photo"><div class="ph-img" style="background-image:url({img('twilight')})"></div></div>
  <div class="shade-panel heavy"></div>
  <div class="grain"></div>
  <div class="chrome-frame"><div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div></div>
  <div class="chapter">Chapter XI · Next Step</div><div class="monogram">EG · Realty</div><div class="page-index"><strong>11</strong> / 11</div>
  <div class="panel"><div class="panel-content">
    <div class="eyebrow fade-in">For the Omega Incentive Sheet</div>
    <div class="headline med fade-in d1">Reach Out.</div>
    <div class="rule fade-in d2"></div>
    <div class="cta-strip fade-in d3">
      <span class="cta-item">Call</span><span class="cta-sep">·</span>
      <span class="cta-item">Text</span><span class="cta-sep">·</span>
      <span class="cta-item">Email</span><span class="cta-sep">·</span>
      <span class="cta-item">Schedule</span>
    </div>
    <div class="fade-in d4" style="margin-top:46px;font-family:'Outfit';font-size:13px;letter-spacing:.32em;text-transform:uppercase;font-weight:300;color:var(--cream-dim)">Taylor Dasch · EG Realty · Temple, TX<br><span style="color:var(--gold);letter-spacing:.45em;display:inline-block;margin-top:6px">templetxhomes.net</span></div>
  </div></div>
</div>

<div class="progress" id="progress"></div>
</div><!-- /.stage -->

<div class="hud" id="hud">CARD <span id="cur">1</span> / 11</div>
<div class="nav">
  <button data-nav="1">I</button><button data-nav="2">II</button>
  <button data-nav="3">III</button><button data-nav="4">IV</button>
  <button data-nav="5">V</button><button data-nav="6">VI</button>
  <button data-nav="7">VII</button><button data-nav="8">VIII</button>
  <button data-nav="9">IX</button><button data-nav="10">X</button>
  <button data-nav="11">XI</button>
  <button id="auto" style="border-left:1px solid var(--emerald);margin-left:6px">▶ Auto</button>
</div>
<div class="help">← → Navigate · 1-9 Jump · F Fullscreen · C Clean Mode · Space Auto</div>

<script>
const cards=[...document.querySelectorAll('.card')];
const navBtns=[...document.querySelectorAll('.nav button[data-nav]')];
const cur=document.getElementById('cur');
const progress=document.getElementById('progress');
let idx=0;let autoTimer=null;let progressTimer=null;
const HOLD=7000;
if(new URLSearchParams(location.search).get('clean')==='1')document.body.classList.add('clean');
function show(i){{if(i<0)i=cards.length-1;if(i>=cards.length)i=0;cards.forEach(c=>c.classList.remove('show'));cards[i].classList.add('show');navBtns.forEach((b,j)=>b.classList.toggle('active',j===i));cur.textContent=i+1;idx=i;cards[i].querySelectorAll('.fade-in').forEach(el=>{{el.style.transition='none';el.style.opacity='0';el.style.transform='translateY(20px)';void el.offsetWidth;el.style.transition='';}});}}
document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key===' '){{e.preventDefault();show(idx+1);resetAuto()}}else if(e.key==='ArrowLeft'){{show(idx-1);resetAuto()}}else if(/^[1-9]$/.test(e.key)){{show(parseInt(e.key)-1);resetAuto()}}else if(e.key==='f'||e.key==='F'){{toggleFullscreen()}}else if(e.key==='c'||e.key==='C'){{document.body.classList.toggle('clean')}}else if(e.key==='Escape'){{stopAuto()}}}});
navBtns.forEach((b,j)=>b.addEventListener('click',()=>{{show(j);resetAuto()}}));
document.getElementById('auto').addEventListener('click',()=>{{if(autoTimer)stopAuto();else startAuto()}});
function startAuto(){{document.getElementById('auto').textContent='■ Stop';document.getElementById('auto').style.color='var(--amber)';tickAuto()}}
function stopAuto(){{clearInterval(autoTimer);clearInterval(progressTimer);autoTimer=null;progress.style.width='0%';document.getElementById('auto').textContent='▶ Auto';document.getElementById('auto').style.color=''}}
function resetAuto(){{if(autoTimer){{stopAuto();startAuto()}}}}
function tickAuto(){{let elapsed=0;progress.style.width='0%';progressTimer=setInterval(()=>{{elapsed+=100;progress.style.width=(elapsed/HOLD*100)+'%';}},100);autoTimer=setTimeout(()=>{{clearInterval(progressTimer);show(idx+1);tickAuto();}},HOLD);}}
function toggleFullscreen(){{if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}}
show(0);
</script>
</body>
</html>
"""

OUT_HTML.write_text(HTML)
print(f"\nWrote: {OUT_HTML}")
print(f"Final HTML size: {OUT_HTML.stat().st_size/1024/1024:.2f}MB")
