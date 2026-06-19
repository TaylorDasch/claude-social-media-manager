# Temple Under-$250K — commute maps to Baylor Scott & White (2401 S 31st St).
# One route schematic per neighborhood + one master proximity map.
# Node positions on the master map use REAL geocoded compass bearings from BSW
# (Google Maps geocode, June 18 2026). Drive times = script's spoken times.
import os, math
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
body.gold{background:radial-gradient(1200px 760px at 50% -12%, rgba(227,199,137,.14), transparent 60%),
   linear-gradient(135deg,#141526 0%,#0d1120 50%,#070a12 100%)}
body:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 360px rgba(0,0,0,.55);pointer-events:none}
.eyebrow{font-family:'JB';font-weight:500;font-size:24px;letter-spacing:.42em;text-transform:uppercase;color:#34d399}
.gold .eyebrow{color:#e3c789}
.flourish{position:relative;white-space:nowrap}
.flourish:after{content:"";position:absolute;left:0;right:0;bottom:-.10em;height:5px;border-radius:3px;background:linear-gradient(90deg,#10b981,#34d399)}
.gold .flourish:after{background:linear-gradient(90deg,#b9974f,#e3c789)}
.bug{position:absolute;left:120px;bottom:54px;display:flex;align-items:center;gap:16px;
 font-family:'JB';font-size:20px;letter-spacing:.16em;color:#94a3b8;text-transform:uppercase}
.bug .mark{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#10b981,#059669);
 display:flex;align-items:center;justify-content:center;font-family:'CG';font-weight:700;color:#06210f;font-size:21px}
.gold .bug .mark{background:linear-gradient(135deg,#e3c789,#b9974f);color:#241a06}
.src{position:absolute;right:120px;bottom:56px;font-family:'JB';font-size:17px;letter-spacing:.06em;color:#64748b;text-align:right}
.tlabel{font-family:'CG';font-weight:600}.mono{font-family:'JB'}
"""

def doc(fn, body, gold=False):
    cls=' class="gold"' if gold else ''
    open(os.path.join(HTMLDIR,fn+".html"),"w").write(
      '<!doctype html><html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body'+cls+'>'+body+'</body></html>')

def bug():
    return '<div class="bug"><span class="mark">T</span>TEMPLETXHOMES.NET · TAYLOR DASCH · EG REALTY</div>'
def srcd(txt="Drive times: Google Maps · driving<br>Destination: Baylor Scott &amp; White · 2401 S 31st St"):
    return f'<div class="src">{txt}</div>'

def node(x,y,color,glyph,title,sub,hero=False,gs=None):
    r=48 if hero else 37
    glow=(f'<circle cx="{x}" cy="{y}" r="{r+36}" fill="{color}" opacity="0.12"/><circle cx="{x}" cy="{y}" r="{r+18}" fill="{color}" opacity="0.10"/>'
          if hero else f'<circle cx="{x}" cy="{y}" r="{r+15}" fill="{color}" opacity="0.10"/>')
    ring=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#0c1424" stroke="{color}" stroke-width="{4 if hero else 3}"/>'
    badge=f'<text x="{x}" y="{y-r-26}" text-anchor="middle" font-family="JB" font-weight="700" font-size="22" letter-spacing="3" fill="{color}">{gs}</text>' if gs else ""
    gfs=42 if glyph=="+" else (40 if hero else 32)
    return f"""<g>{glow}{ring}
  <text x="{x}" y="{y+(gfs*0.36):.0f}" text-anchor="middle" font-size="{gfs}" fill="{color}" font-family="JB" font-weight="700">{glyph}</text>
  {badge}
  <text x="{x}" y="{y+r+50}" text-anchor="middle" class="tlabel" font-size="{40 if hero else 33}" fill="#f8fafc">{title}</text>
  <text x="{x}" y="{y+r+84}" text-anchor="middle" font-family="JB" font-size="21" letter-spacing="2" fill="#94a3b8">{sub}</text>
</g>"""

def chip(x,y,big,small,color,w=320):
    h=104
    return f"""<g>
  <rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="20" fill="rgba(13,20,36,0.94)" stroke="{color}" stroke-opacity="0.55" stroke-width="2"/>
  <rect x="{x-w/2}" y="{y-h/2}" width="8" height="{h}" rx="4" fill="{color}"/>
  <text x="{x-w/2+34}" y="{y-2}" class="mono" font-weight="700" font-size="46" fill="#f8fafc">{big}</text>
  <text x="{x-w/2+34}" y="{y+34}" class="mono" font-size="22" letter-spacing="1.2" fill="#94a3b8">{small}</text>
</g>"""

EM="#34d399"; GOLD="#e3c789"; STEEL="#8fb3d6"

# ---------- DATA ----------
ROUTE = {  # neighborhood -> (drive, miles, compass blurb, gold?)
 "altavista": ("8 min","3.9 mi","South Temple",False),
 "oakridge":  ("11 min","5.1 mi","Northeast edge of town",False),
 "heritage":  ("9 min","4.0 mi","East side",False),
 "western":   ("8 min","3.5 mi","West Temple",False),
 "canyon":    ("5 min","1.7 mi","Just south of the hospital",True),
}
NAME={"altavista":"Alta Vista","oakridge":"Oak Ridge","heritage":"Heritage Place","western":"Western Hills","canyon":"Canyon Creek"}
RANK={"altavista":5,"oakridge":4,"heritage":3,"western":2,"canyon":1}

# ---------- PER-NEIGHBORHOOD ROUTE MAP (origin left -> BSW right) ----------
def route_map(key):
    drive,miles,blurb,gold=ROUTE[key]
    accent=GOLD if gold else EM
    closest = ' &nbsp;·&nbsp; <tspan>CLOSEST ON THE LIST</tspan>' if gold else ''
    OX,OY=470,560; BX,BY=1450,560
    # gentle road curve
    road=f'M{OX},{OY} C760,470 1160,470 {BX},{BY}'
    heromark = "YOU ARE HERE"
    svg=f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
 <defs>
   <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
   <pattern id="grid" width="58" height="58" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="rgba(255,255,255,0.05)"/></pattern>
 </defs>
 <rect x="120" y="330" width="1680" height="500" rx="28" fill="rgba(10,16,30,0.5)" stroke="rgba(255,255,255,0.08)"/>
 <rect x="120" y="330" width="1680" height="500" rx="28" fill="url(#grid)"/>
 <path d="{road}" fill="none" stroke="{accent}" stroke-width="18" opacity="0.16" filter="url(#soft)"/>
 <path d="{road}" fill="none" stroke="{accent}" stroke-width="6" stroke-dasharray="2 16" stroke-linecap="round"/>
 {chip(960,455,drive,miles+" · driving",accent,w=300)}
 {node(OX,OY,accent,"&#9650;",NAME[key],blurb.upper(),hero=True,gs=heromark)}
 {node(BX,BY,EM,"+","Baylor Scott &amp; White","MEDICAL DISTRICT")}
</svg>"""
    body=f"""
<div style="position:absolute;left:120px;top:90px">
  <div class="eyebrow">#{RANK[key]} {NAME[key]} · Commute</div>
  <div class="tlabel" style="font-family:'CG';font-weight:600;font-size:100px;line-height:.98;margin-top:14px">
     <span style="color:{accent}">{drive}</span> to Baylor <span class="flourish">Scott &amp; White</span>.</div>
  <div style="font-size:30px;color:#cbd5e1;margin-top:20px">{NAME[key]} sits {blurb[0].lower()+blurb[1:]} &mdash; {miles}, door to door.{(' The closest of all five.' if gold else '')}</div>
</div>
{svg}{bug()}{srcd()}"""
    doc(f"MAP_{key}", body, gold=gold)

for k in ROUTE: route_map(k)

# ---------- MASTER PROXIMITY MAP ----------
# Explicit positions, hand-spaced for legibility but laid out in each neighborhood's
# TRUE compass direction from BSW (geocoded Jun 18 2026). Radius loosely tracks minutes.
HUB=(960,548)
# key -> (x, y, drive_min, gold) — spread to panel edges, true-ish compass direction
PTS={
 "western":  (335, 350, 8, False),   # NW
 "oakridge": (1585, 345, 11, False), # NE (farthest)
 "heritage": (1690, 605, 9, False),  # E
 "altavista":(1210, 848, 8, False),  # S / SE
 "canyon":   (735, 852, 5, True),    # SSW (hero, closest)
 "cimarron": (300, 660, 7, False),   # WSW
}
MNAME={"canyon":"Canyon Creek","altavista":"Alta Vista","cimarron":"Cimarron","western":"Western Hills","heritage":"Heritage Place","oakridge":"Oak Ridge"}
MRANK={"canyon":"#1","altavista":"#5","cimarron":"HM","western":"#2","heritage":"#3","oakridge":"#4"}
MMED={"canyon":"MEDIAN $219K","altavista":"MEDIAN $228K","cimarron":"MEDIAN $197K","western":"MEDIAN $210K","heritage":"MEDIAN $220K","oakridge":"MEDIAN $237K"}

lines=""; chips=""; nodes=""
for key,(x,y,mins,gold) in PTS.items():
    acc=GOLD if gold else EM
    lines+=f'<path d="M{HUB[0]},{HUB[1]} L{x},{y}" stroke="{acc}" stroke-width="{7 if gold else 4}" stroke-dasharray="2 14" stroke-linecap="round" opacity="{0.95 if gold else 0.5}"/>'
    # time chip mid-spoke, in open field (nodes sit at edges)
    t=0.50; cx=HUB[0]+(x-HUB[0])*t; cy=HUB[1]+(y-HUB[1])*t
    chips+=chip(cx,cy,f"{mins} min","",acc,w=158)
    nodes+=node(x,y,acc,MRANK[key],MNAME[key],MMED[key],hero=gold,gs=("CLOSEST" if gold else None))

svg=f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
 <defs>
   <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
   <pattern id="grid" width="58" height="58" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="rgba(255,255,255,0.05)"/></pattern>
 </defs>
 <rect x="100" y="250" width="1720" height="720" rx="30" fill="rgba(10,16,30,0.45)" stroke="rgba(255,255,255,0.08)"/>
 <rect x="100" y="250" width="1720" height="720" rx="30" fill="url(#grid)"/>
 {lines}
 {nodes}
 {chips}
 <g>
   <circle cx="{HUB[0]}" cy="{HUB[1]}" r="118" fill="{EM}" opacity="0.10"/>
   <rect x="{HUB[0]-225}" y="{HUB[1]-66}" width="450" height="132" rx="22" fill="#0b1322" stroke="{EM}" stroke-width="3"/>
   <circle cx="{HUB[0]-150}" cy="{HUB[1]}" r="44" fill="#0c1424" stroke="{EM}" stroke-width="4"/>
   <text x="{HUB[0]-150}" y="{HUB[1]+17}" text-anchor="middle" font-size="46" fill="{EM}" font-family="JB" font-weight="700">+</text>
   <text x="{HUB[0]-78}" y="{HUB[1]-6}" class="tlabel" font-size="38" fill="#f8fafc">Baylor Scott &amp; White</text>
   <text x="{HUB[0]-78}" y="{HUB[1]+32}" font-family="JB" font-size="19" letter-spacing="2" fill="#94a3b8">MEDICAL DISTRICT · TEMPLE</text>
 </g>
 <text x="150" y="300" class="mono" font-size="22" letter-spacing="3" fill="#64748b">&#8593; NORTH</text>
</svg>"""
body=f"""
<div style="position:absolute;left:120px;top:84px">
  <div class="eyebrow">The whole map · Proximity to BSW</div>
  <div class="tlabel" style="font-family:'CG';font-weight:600;font-size:94px;line-height:.98;margin-top:12px">
     Every pick, <span class="flourish">5&ndash;11 minutes</span> from the hospital.</div>
</div>
{svg}{bug()}<div class="src">Positions = real geocoded bearings (Google Maps, Jun 18 2026)<br>Drive times → Baylor Scott &amp; White, 2401 S 31st St</div>"""
doc("MAP_master", body)

print("MAP HTML written:", len([f for f in os.listdir(HTMLDIR) if f.startswith('MAP')]), "map files")
