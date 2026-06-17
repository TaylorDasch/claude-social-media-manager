# Dawson Ranch (radial convenience hub) + Lake neighborhoods (water-forward) maps.
# Drive times: Google Maps distance matrix, off-peak.
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
body{font-family:'IN',sans-serif;color:#f8fafc;position:relative}
body.em{background:radial-gradient(1200px 760px at 50% -12%, rgba(16,185,129,.14), transparent 60%),
   linear-gradient(135deg,#10192e 0%,#0c1424 50%,#070c16 100%)}
body.gold{background:radial-gradient(1200px 760px at 70% -12%, rgba(227,199,137,.13), transparent 60%),
   linear-gradient(135deg,#121627 0%,#0c1322 50%,#070b13 100%)}
body:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 360px rgba(0,0,0,.55);pointer-events:none}
.eyebrow{font-family:'JB';font-weight:500;font-size:24px;letter-spacing:.42em;text-transform:uppercase}
.bug{position:absolute;left:120px;bottom:54px;display:flex;align-items:center;gap:16px;
 font-family:'JB';font-size:20px;letter-spacing:.16em;color:#94a3b8;text-transform:uppercase}
.bug .mark{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;
 font-family:'CG';font-weight:700;font-size:21px}
.src{position:absolute;right:120px;bottom:56px;font-family:'JB';font-size:17px;letter-spacing:.06em;color:#64748b;text-align:right}
text{font-family:'IN'} .tlabel{font-family:'CG';font-weight:600} .mono{font-family:'JB'}
"""

def node(x,y,color,glyph,title,sub,hero=False,gsz=34):
    r=46 if hero else 34
    glow=f'<circle cx="{x}" cy="{y}" r="{r+30}" fill="{color}" opacity="0.12"/><circle cx="{x}" cy="{y}" r="{r+14}" fill="{color}" opacity="0.10"/>' if hero else f'<circle cx="{x}" cy="{y}" r="{r+12}" fill="{color}" opacity="0.10"/>'
    ring=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#0c1424" stroke="{color}" stroke-width="{4 if hero else 3}"/>'
    badge=f'<text x="{x}" y="{y-r-24}" text-anchor="middle" font-family="JB" font-weight="700" font-size="22" letter-spacing="3" fill="{color}">YOU ARE HERE</text>' if hero else ""
    return f"""<g>{glow}{ring}
  <text x="{x}" y="{y+(gsz//2)-2}" text-anchor="middle" font-size="{42 if hero else gsz}" fill="{color}" font-family="JB" font-weight="700">{glyph}</text>
  {badge}
  <text x="{x}" y="{y+r+48}" text-anchor="middle" class="tlabel" font-size="{38 if hero else 32}" fill="#f1f5f9">{title}</text>
  <text x="{x}" y="{y+r+80}" text-anchor="middle" font-family="JB" font-size="21" letter-spacing="2" fill="#94a3b8">{sub}</text>
</g>"""

def chip(x,y,big,small,color,w=270):
    h=98
    return f"""<g>
  <rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="18" fill="rgba(13,20,36,0.94)" stroke="{color}" stroke-opacity="0.55" stroke-width="2"/>
  <rect x="{x-w/2}" y="{y-h/2}" width="8" height="{h}" rx="4" fill="{color}"/>
  <text x="{x-w/2+30}" y="{y-4}" class="mono" font-weight="700" font-size="42" fill="#f8fafc">{big}</text>
  <text x="{x-w/2+30}" y="{y+30}" class="mono" font-size="21" letter-spacing="1.4" fill="#94a3b8">{small}</text>
</g>"""

EM="#34d399"; STEEL="#8fb3d6"; GOLD="#e3c789"; WATER="#2f6f9e"

# ================= DAWSON RANCH — radial convenience hub =================
def snode(x,y,color,glyph,title,cat,time):
    r=34
    return f"""<g>
  <circle cx="{x}" cy="{y}" r="{r+12}" fill="{color}" opacity="0.10"/>
  <circle cx="{x}" cy="{y}" r="{r}" fill="#0c1424" stroke="{color}" stroke-width="3"/>
  <text x="{x}" y="{y+14}" text-anchor="middle" font-size="30" fill="{color}" font-family="JB" font-weight="700">{glyph}</text>
  <text x="{x}" y="{y+r+44}" text-anchor="middle" class="tlabel" font-size="34" fill="#f1f5f9">{title}</text>
  <text x="{x}" y="{y+r+74}" text-anchor="middle" font-family="JB" font-size="20" letter-spacing="2" fill="#94a3b8">{cat}</text>
  <text x="{x}" y="{y+r+106}" text-anchor="middle" font-family="JB" font-weight="700" font-size="30" fill="{color}">{time}</text>
</g>"""
DC=(980,576)  # center
spokes=[  # (x,y,color,glyph,title,category,time)
 (300,548, STEEL,"&#9733;","Fort Cavazos","MILITARY BASE","&#8776; 26 min"),
 (715,372, EM,"&#9650;","UMHB","UNIVERSITY","&#8776; 10 min"),
 (660,742, "#8fb3d6","&#9650;","Belton Lake","RECREATION","&#8776; 13 min"),
 (1605,536, EM,"&#9632;","Downtown Belton","SHOPS · DINING","&#8776; 13 min"),
 (1360,742, EM,"+","Baylor Scott &amp; White","MEDICAL","&#8776; 24 min"),
]
lines=""; nodes=""
for x,y,c,g,t,cat,tm in spokes:
    lines+=f'<path d="M{DC[0]},{DC[1]} L{x},{y}" stroke="{c}" stroke-width="5" stroke-dasharray="2 15" stroke-linecap="round" opacity="0.65"/>'
    nodes+=snode(x,y,c,g,t,cat,tm)
dawson=f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
 <defs><pattern id="grid" width="58" height="58" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="rgba(255,255,255,0.05)"/></pattern></defs>
 <rect x="120" y="300" width="1680" height="600" rx="28" fill="rgba(10,16,30,0.5)" stroke="rgba(255,255,255,0.08)"/>
 <rect x="120" y="300" width="1680" height="600" rx="28" fill="url(#grid)"/>
 {lines}{nodes}
 {node(DC[0],DC[1],EM,"&#9650;","Dawson Ranch &amp; Ridge","BELTON · BIG LOTS",hero=True)}
</svg>"""
dawson_body=f"""
<div style="position:absolute;left:120px;top:92px">
  <div class="eyebrow" style="color:#34d399">Dawson Ranch &amp; Ridge · Location</div>
  <div style="font-family:'CG';font-weight:600;font-size:100px;line-height:.98;margin-top:12px">
     Minutes to <span style="color:#34d399;position:relative">everything<span style="position:absolute;left:0;right:0;bottom:-.1em;height:5px;border-radius:3px;background:linear-gradient(90deg,#10b981,#34d399)"></span></span>.</div>
  <div style="font-size:31px;color:#cbd5e1;margin-top:20px;max-width:1480px;line-height:1.4">
     The established, big-lot side of Belton — close to the university, the lake, downtown, the hospital and the base.</div>
</div>
{dawson}
<div class="bug"><span class="mark" style="background:linear-gradient(135deg,#10b981,#059669);color:#06210f">T</span>TEMPLETXHOMES.NET · TAYLOR DASCH · EG REALTY</div>
<div class="src">Drive times: Google Maps · off-peak<br>Origin: Dawson Ranch, Belton TX</div>
"""
open(os.path.join(HTMLDIR,"12_dawson_map.html"),"w").write(
 '<!doctype html><html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body class="em">'+dawson_body+'</body></html>')

# ================= LAKE NEIGHBORHOODS — water-forward =================
# big lake shape upper-right; shoreline curves; subdivisions on land (lower-left); flood band along shore.
lake=f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
 <defs>
   <linearGradient id="wg" x1="0" y1="0" x2="1" y2="1">
     <stop offset="0" stop-color="#3a82b3"/><stop offset="1" stop-color="#1f4e74"/></linearGradient>
   <pattern id="wave" width="46" height="20" patternUnits="userSpaceOnUse">
     <path d="M0,12 Q11,4 23,12 T46,12" fill="none" stroke="rgba(255,255,255,0.10)" stroke-width="2"/></pattern>
   <pattern id="grid2" width="58" height="58" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="rgba(255,255,255,0.05)"/></pattern>
   <pattern id="flood" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
     <line x1="0" y1="0" x2="0" y2="22" stroke="#fbbf24" stroke-width="3" stroke-opacity="0.5"/></pattern>
 </defs>
 <rect x="120" y="300" width="1680" height="600" rx="28" fill="rgba(10,16,30,0.5)" stroke="rgba(255,255,255,0.08)"/>
 <rect x="120" y="300" width="1680" height="600" rx="28" fill="url(#grid2)"/>
 <clipPath id="panel"><rect x="120" y="300" width="1680" height="600" rx="28"/></clipPath>
 <g clip-path="url(#panel)">
   <!-- lake body (dendritic reservoir, NW-SE) -->
   <path d="M540,300 C760,360 980,330 1180,400 C1420,485 1640,440 1800,520 L1800,300 Z" fill="url(#wg)"/>
   <path d="M540,300 C720,470 980,470 1130,560 C1330,675 1560,610 1800,690 L1800,520 C1640,440 1420,485 1180,400 C980,330 760,360 540,300 Z" fill="url(#wg)"/>
   <path d="M540,300 C720,470 980,470 1130,560 C1330,675 1560,610 1800,690 L1800,520 C1640,440 1420,485 1180,400 C980,330 760,360 540,300 Z" fill="url(#wave)"/>
   <!-- flood band hugging the shoreline -->
   <path d="M540,300 C720,470 980,470 1130,560 C1330,675 1560,610 1800,690 L1800,742 C1560,662 1330,727 1130,612 C980,522 720,522 540,352 Z" fill="url(#flood)"/>
   <path d="M540,300 C720,470 980,470 1130,560 C1330,675 1560,610 1800,690" fill="none" stroke="#bfe0ff" stroke-width="3" stroke-opacity="0.5"/>
 </g>
 <text x="1500" y="430" class="tlabel" font-size="40" fill="#cfe6f7" opacity="0.9" font-style="italic">Belton Lake</text>
 <text x="1280" y="372" class="mono" font-size="20" letter-spacing="2" fill="#9fc4dd" opacity="0.8">MORGAN'S POINT &#8594;</text>

 <!-- subdivision pins on the land/shore (gold) -->
 {node(560,690,GOLD,"&#9650;","Rancho Del Lago","WATERFRONT",gsz=30)}
 {node(950,770,GOLD,"&#9650;","Colinas Del Lago","CUSTOM HOMES",gsz=30)}
 {node(1330,800,GOLD,"&#9650;","Lago Terra","LARGE LOTS",gsz=30)}

 <!-- flood caution -->
 <g>
   <rect x="1140" y="470" width="560" height="92" rx="16" fill="rgba(251,191,36,0.10)" stroke="rgba(251,191,36,0.45)" stroke-width="2"/>
   <text x="1168" y="510" font-family="JB" font-weight="700" font-size="26" fill="#fbbf24">&#9888; FEMA FLOOD ZONES</text>
   <text x="1168" y="542" font-size="23" fill="#fde9c0">Near the shore — verify before you buy (insurance jumps).</text>
 </g>

 <!-- commute chips -->
 {chip(300,470,"&#8776;19 min","to BSW · 10 mi", GOLD, w=290)}
 {chip(300,580,"&#8776;17 min","to Belton · 8 mi", GOLD, w=290)}
</svg>"""
lake_body=f"""
<div style="position:absolute;left:120px;top:92px;z-index:5">
  <div class="eyebrow" style="color:#e3c789">The Lake Neighborhoods · Belton Lake</div>
  <div style="font-family:'CG';font-weight:600;font-size:92px;line-height:.98;margin-top:12px">
     What separates Belton <span style="color:#e3c789;position:relative">from Temple<span style="position:absolute;left:0;right:0;bottom:-.1em;height:5px;border-radius:3px;background:linear-gradient(90deg,#b9974f,#e3c789)"></span></span>.</div>
  <div style="font-size:30px;color:#cbd5e1;margin-top:18px;max-width:980px;line-height:1.4">
     Custom homes on the water — Rancho Del Lago, Colinas Del Lago &amp; Lago Terra. ~$765K median · $248/sf.</div>
</div>
{lake}
<div class="bug"><span class="mark" style="background:linear-gradient(135deg,#e3c789,#b9974f);color:#241a06">T</span>TEMPLETXHOMES.NET · TAYLOR DASCH · EG REALTY</div>
<div class="src">Drive times: Google Maps · off-peak · Origin: Rancho Del Lago<br>Lake outline illustrative</div>
"""
open(os.path.join(HTMLDIR,"13_lake_map.html"),"w").write(
 '<!doctype html><html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body class="gold">'+lake_body+'</body></html>')

print("dawson + lake map html written")
