# Three Creeks commute map — branded, geographically-directional schematic.
# Medical lane EAST (BSW, emerald) · Military lane WEST (Fort Cavazos/Copperas Cove, steel).
# Drive times: Google Maps distance matrix, off-peak (origin Three Creeks, Belton TX).
import os
HERE=os.path.dirname(os.path.abspath(__file__))
HTMLDIR=os.path.join(HERE,"html"); os.makedirs(HTMLDIR,exist_ok=True)

CSS=r"""
@font-face{font-family:'CG';src:url('../fonts/cg500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'CG';src:url('../fonts/cg600.woff2') format('woff2');font-weight:600;font-display:block}
@font-face{font-family:'CG';src:url('../fonts/cg700.woff2') format('woff2');font-weight:700;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb700.woff2') format('woff2');font-weight:700;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in600.woff2') format('woff2');font-weight:600;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden}
body{font-family:'IN',sans-serif;color:#f8fafc;position:relative;
 background:radial-gradient(1200px 760px at 50% -12%, rgba(16,185,129,.14), transparent 60%),
   linear-gradient(135deg,#10192e 0%,#0c1424 50%,#070c16 100%)}
body:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 360px rgba(0,0,0,.55);pointer-events:none}
.eyebrow{font-family:'JB';font-weight:500;font-size:24px;letter-spacing:.42em;text-transform:uppercase;color:#34d399}
.bug{position:absolute;left:120px;bottom:54px;display:flex;align-items:center;gap:16px;
 font-family:'JB';font-size:20px;letter-spacing:.16em;color:#94a3b8;text-transform:uppercase}
.bug .mark{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#10b981,#059669);
 display:flex;align-items:center;justify-content:center;font-family:'CG';font-weight:700;color:#06210f;font-size:21px}
.src{position:absolute;right:120px;bottom:56px;font-family:'JB';font-size:17px;letter-spacing:.06em;color:#64748b;text-align:right}
text{font-family:'IN'}
.tlabel{font-family:'CG';font-weight:600}
.mono{font-family:'JB'}
"""

# node helper (SVG group)
def node(x,y,color,glyph,title,sub,hero=False):
    r = 46 if hero else 36
    glow = f'<circle cx="{x}" cy="{y}" r="{r+34}" fill="{color}" opacity="0.12"/><circle cx="{x}" cy="{y}" r="{r+16}" fill="{color}" opacity="0.10"/>' if hero else f'<circle cx="{x}" cy="{y}" r="{r+14}" fill="{color}" opacity="0.10"/>'
    ring = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#0c1424" stroke="{color}" stroke-width="{4 if hero else 3}"/>'
    badge = f'<text x="{x}" y="{y-r-26}" text-anchor="middle" font-family="JB" font-weight="700" font-size="22" letter-spacing="3" fill="{color}">YOU ARE HERE</text>' if hero else ""
    tcolor = "#f8fafc" if hero else "#e2e8f0"
    return f"""<g>{glow}{ring}
  <text x="{x}" y="{y+ (16 if glyph!='+' else 17)}" text-anchor="middle" font-size="{42 if hero else 34}" fill="{color}" font-family="JB" font-weight="700">{glyph}</text>
  {badge}
  <text x="{x}" y="{y+r+50}" text-anchor="middle" class="tlabel" font-size="{40 if hero else 34}" fill="{tcolor}">{title}</text>
  <text x="{x}" y="{y+r+84}" text-anchor="middle" font-family="JB" font-size="22" letter-spacing="2" fill="#94a3b8">{sub}</text>
</g>"""

def chip(x,y,big,small,color):
    w=300; h=104
    return f"""<g>
  <rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="20" fill="rgba(13,20,36,0.92)" stroke="{color}" stroke-opacity="0.5" stroke-width="2"/>
  <rect x="{x-w/2}" y="{y-h/2}" width="8" height="{h}" rx="4" fill="{color}"/>
  <text x="{x-w/2+34}" y="{y-2}" class="mono" font-weight="700" font-size="46" fill="#f8fafc">{big}</text>
  <text x="{x-w/2+34}" y="{y+34}" class="mono" font-size="23" letter-spacing="1.5" fill="#94a3b8">{small}</text>
</g>"""

EM="#34d399"; STEEL="#8fb3d6"; STEEL2="#b9cfe6"; HERO="#34d399"
# coords (west -> east). Copperas far west, Cavazos west, Three Creeks center, BSW east.
COVE=(330,548); CAV=(640,532); TC=(975,600); BSW=(1530,532)
svg=f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
 <defs>
   <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
   <pattern id="grid" width="58" height="58" patternUnits="userSpaceOnUse">
     <circle cx="2" cy="2" r="1.3" fill="rgba(255,255,255,0.05)"/></pattern>
 </defs>
 <!-- map panel -->
 <rect x="120" y="300" width="1680" height="560" rx="28" fill="rgba(10,16,30,0.5)" stroke="rgba(255,255,255,0.08)"/>
 <rect x="120" y="300" width="1680" height="560" rx="28" fill="url(#grid)"/>
 <text x="1006" y="346" class="mono" font-size="22" fill="#64748b" letter-spacing="2">I&#8209;35</text>
 <path d="M990,300 V860" stroke="rgba(255,255,255,0.05)" stroke-width="2"/>

 <!-- WEST military lane (steel) : Copperas <- Cavazos <- Three Creeks -->
 <path d="M{TC[0]},{TC[1]} Q800,505 {CAV[0]},{CAV[1]}" fill="none" stroke="{STEEL}" stroke-width="14" opacity="0.18" filter="url(#soft)"/>
 <path d="M{TC[0]},{TC[1]} Q800,505 {CAV[0]},{CAV[1]}" fill="none" stroke="{STEEL}" stroke-width="6" stroke-dasharray="2 16" stroke-linecap="round"/>
 <path d="M{CAV[0]},{CAV[1]} Q490,548 {COVE[0]},{COVE[1]}" fill="none" stroke="{STEEL2}" stroke-width="5" stroke-dasharray="2 15" stroke-linecap="round" opacity="0.85"/>
 <!-- EAST medical lane (emerald): Three Creeks -> BSW -->
 <path d="M{TC[0]},{TC[1]} Q1260,525 {BSW[0]},{BSW[1]}" fill="none" stroke="{EM}" stroke-width="16" opacity="0.20" filter="url(#soft)"/>
 <path d="M{TC[0]},{TC[1]} Q1260,525 {BSW[0]},{BSW[1]}" fill="none" stroke="{EM}" stroke-width="6" stroke-dasharray="2 16" stroke-linecap="round"/>

 <!-- drive chips (only the two primary lanes; Copperas time sits on its node) -->
 {chip(1245,455,"≈15 min","13 mi · to BSW", EM)}
 {chip(720,438,"≈24 min","21 mi · Fort Cavazos", STEEL)}

 <!-- nodes -->
 {node(COVE[0],COVE[1],STEEL2,"&#9733;","Copperas Cove","&#8776; 29 MIN · 28 MI")}
 {node(CAV[0],CAV[1],STEEL,"&#9733;","Fort Cavazos","MILITARY BASE")}
 {node(TC[0],TC[1],HERO,"&#9650;","Three Creeks","BELTON · MASTER-PLAN",hero=True)}
 {node(BSW[0],BSW[1],EM,"+","Baylor Scott &amp; White","MEDICAL DISTRICT")}

 <!-- compass -->
 <text x="160" y="832" class="mono" font-size="24" letter-spacing="3" fill="#8fb3d6">&#8592; WEST · MILITARY</text>
 <text x="1760" y="832" text-anchor="end" class="mono" font-size="24" letter-spacing="3" fill="#34d399">MEDICAL · EAST &#8594;</text>
</svg>"""

body=f"""
<div style="position:absolute;left:120px;top:88px">
  <div class="eyebrow">Three Creeks · Location</div>
  <div style="font-family:'CG';font-weight:600;font-size:104px;line-height:.98;margin-top:14px">
     Right in the <span style="color:#34d399;position:relative">middle<span style="position:absolute;left:0;right:0;bottom:-.12em;height:5px;border-radius:3px;background:linear-gradient(90deg,#10b981,#34d399)"></span></span>.</div>
  <div style="font-size:32px;color:#cbd5e1;margin-top:22px;max-width:1500px;line-height:1.4">
     One master-plan community sitting between the <b style="color:#34d399">medical district</b> and the <b style="color:#8fb3d6">military base</b> — an easy commute either direction.</div>
</div>
{svg}
<div class="bug"><span class="mark">T</span>TEMPLETXHOMES.NET · TAYLOR DASCH · EG REALTY</div>
<div class="src">Drive times: Google Maps · off-peak<br>Origin: Three Creeks, Belton TX</div>
"""
open(os.path.join(HTMLDIR,"11_threecreeks_map.html"),"w").write(
  '<!doctype html><html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+body+'</body></html>')
print("map html written")
