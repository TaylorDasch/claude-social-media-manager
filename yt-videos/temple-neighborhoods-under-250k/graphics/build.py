# Temple Neighborhoods Under $250K — premium graphics generator
# Channel: Living in Temple / templetxhomes.net / Taylor Dasch · EG Realty
# Renders 1920x1080 HTML -> PNG (4K via scale-factor 2) using headless Chrome.
# Design system lifted from the Belton "ranked" deck so the channel stays consistent.
# On-screen drive times = the SCRIPT's spoken times (video already filmed to these).
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HTMLDIR = os.path.join(HERE, "html"); os.makedirs(HTMLDIR, exist_ok=True)

# ---------- VERIFIED DATA (CTX MLS June 18 2026 pull, City=Temple, price <= $250K) ----------
NB = {
 "altavista": dict(rank=5, name="Alta Vista", sub="South Temple", tier="newer + a school surprise",
    median="$228,500", lo="$213K", hi="$244K", size="~1,600 sf", era="built ~2017",
    active="3", drive="8 min", miles="3.9 mi", isd="Academy ISD", hoa="No HOA",
    builders=["D.R. Horton","Ashford"],
    note="One of the newer pockets on the list &mdash; and it&rsquo;s Academy ISD, inside Temple&rsquo;s city limits.",
    best=["Newer (~2017 build)","Academy ISD schools","Inside Temple city limits"],
    watch="Thin under $250K &mdash; only 3 active when I pulled it. Most of the neighborhood now trades $250K&ndash;mid-$300s. A timing play.",
    streets=[]),
 "oakridge": dict(rank=4, name="Oak Ridge", sub="", tier="brand-new, zero projects",
    median="$236,675", lo="$219K", hi="$250K", size="~1,415 sf", era="built 2025 &middot; NEW",
    active="4", drive="11 min", miles="5.1 mi", isd="Temple ISD", hoa="Mandatory HOA",
    builders=["D.R. Horton","Flintrock"],
    note="Brand-new construction, 2022&ndash;2026 &mdash; warranties, modern layouts, nothing to fix on day one.",
    best=["Brand-new construction","Warranties &middot; zero projects","Modern open layouts"],
    watch="Mandatory HOA &middot; still filling in (construction, few mature trees) &middot; smallest median sqft for the money &mdash; you&rsquo;re paying for new, not big.",
    streets=["Cilantro","Saffron","Turmeric","Oregano"]),
 "heritage": dict(rank=3, name="Heritage Place", sub="", tier="the most homes to tour now",
    median="$220,000", lo="$195K", hi="$240K", size="~1,325 sf", era="built ~2014",
    active="15", drive="9 min", miles="4.0 mi", isd="Temple ISD", hoa="Mandatory HOA",
    builders=[],
    note="The most options on the board right now &mdash; 15 active under $250K. Red brick, white stone, open floor plans.",
    best=["Most homes to tour now (15)","Move-in ready","Red brick &amp; white stone"],
    watch="Smallest established homes (~1,325 sf) &middot; mandatory HOA &mdash; build the dues into your budget.",
    streets=["Roanoke","Jamestown","Vicksburg","Petersburg"]),
 "western": dict(rank=2, name="Western Hills", sub="West Temple", tier="most house &amp; land per $",
    median="$210,000", lo="$100K", hi="$250K", size="~1,734 sf", era="built ~1985",
    active="8", drive="8 min", miles="3.5 mi", isd="Temple ISD", hoa="No HOA",
    builders=[],
    note="Established west Temple, 1960s&ndash;90s &mdash; big lots, mature trees, the biggest square footage on the list.",
    best=["Biggest sqft on the list","Big lots &middot; mature trees","No HOA"],
    watch="Condition varies wildly &mdash; the $100K bottom is a fixer with foundation issues; the top is fully remodeled. Inspect carefully.",
    streets=["Apache","Comanche","Brazos","Chisholm"]),
 "canyon": dict(rank=1, name="Canyon Creek", sub="", tier="all-rounder &middot; closest to BSW",
    median="$219,000", lo="$190K", hi="$250K", size="~1,558 sf", era="built ~1985",
    active="15", drive="5 min", miles="1.7 mi", isd="Temple ISD", hoa="No HOA",
    builders=[], gold=True,
    note="Checks every box &mdash; 15 active, no HOA, mature trees since the &rsquo;70s, and the closest of all five to Baylor Scott &amp; White.",
    best=["Closest to BSW &mdash; 5 min","No HOA &middot; mature trees","Established since the &rsquo;70s"],
    watch="1980s core (some dated homes) &middot; no HOA = upkeep varies &middot; under $250K is the entry tier, not the Cliffs.",
    streets=["Bordeaux","Brighton","Chelsea","Kensington"]),
 "cimarron": dict(rank=0, name="Cimarron", sub="Honorable mention", tier="budget pick &middot; from $153K",
    median="$197,000", lo="$153K", hi="$249K", size="~1,150 sf", era="built ~1983",
    active="5", drive="7 min", miles="2.9 mi", isd="Temple ISD", hoa="No HOA",
    builders=[],
    note="If your budget&rsquo;s tighter &mdash; south Temple off 31st by Lions Junction water park. The most affordable on the list.",
    best=["From $153K &mdash; most affordable","Single-story &amp; twin homes","~7 min to BSW"],
    watch="Smallest / oldest homes (~1,150 sf, early &rsquo;80s) &middot; some are twin homes (attached).",
    streets=["Sam Houston","Bowie","Daniel Boone"]),
}
ORDER = ["altavista","oakridge","heritage","western","canyon"]

# ---------- DESIGN SYSTEM (shared with the channel's ranked deck) ----------
CSS = r"""
@font-face{font-family:'CG';src:url('../fonts/cg400.woff2') format('woff2');font-weight:400;font-display:block}
@font-face{font-family:'CG';src:url('../fonts/cg500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'CG';src:url('../fonts/cg600.woff2') format('woff2');font-weight:600;font-display:block}
@font-face{font-family:'CG';src:url('../fonts/cg700.woff2') format('woff2');font-weight:700;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb400.woff2') format('woff2');font-weight:400;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb700.woff2') format('woff2');font-weight:700;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in400.woff2') format('woff2');font-weight:400;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in600.woff2') format('woff2');font-weight:600;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in700.woff2') format('woff2');font-weight:700;font-display:block}
:root{
 --midnight:#0f172a;--deep:#080d18;--elev:#131e36;--card:#1a2d42;--cardh:#223656;
 --snow:#f8fafc;--muted:#e2e8f0;--subtle:#94a3b8;--faint:#64748b;
 --em:#10b981;--emd:#059669;--emb:#34d399;
 --gold:#e3c789;--goldd:#b9974f;
 --rose:#fb7185;--amber:#fbbf24;
 --hair:rgba(255,255,255,.07);--hair2:rgba(255,255,255,.12);
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden}
body{font-family:'IN',sans-serif;color:var(--snow);
 background:
   radial-gradient(1100px 700px at 18% -8%, rgba(16,185,129,.16), transparent 60%),
   radial-gradient(900px 700px at 108% 118%, rgba(52,211,153,.08), transparent 55%),
   linear-gradient(135deg,#10192e 0%,#0c1424 48%,#070c16 100%);
 position:relative}
body.tier-gold{background:
   radial-gradient(1100px 700px at 18% -8%, rgba(227,199,137,.16), transparent 60%),
   radial-gradient(900px 700px at 108% 118%, rgba(227,199,137,.07), transparent 55%),
   linear-gradient(135deg,#141526 0%,#0d1120 48%,#070a12 100%)}
body:before{content:"";position:absolute;inset:0;
 background-image:radial-gradient(rgba(255,255,255,.05) 1.1px, transparent 1.2px);
 background-size:46px 46px;opacity:.5;mask-image:linear-gradient(135deg,rgba(0,0,0,.9),transparent 70%)}
body:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 360px rgba(0,0,0,.55);pointer-events:none}
.transparent,.transparent body{background:transparent !important}
.transparent:before,.transparent:after,.transparent body:before,.transparent body:after{display:none !important}
.stage{position:absolute;inset:0;padding:96px 120px;display:flex;flex-direction:column}
.eyebrow{font-family:'JB';font-weight:500;font-size:24px;letter-spacing:.42em;text-transform:uppercase;color:var(--emb)}
.tier-gold .eyebrow{color:var(--gold)}
.serif{font-family:'CG';font-weight:600;line-height:.98;letter-spacing:-.01em}
.mono{font-family:'JB'}
.em{color:var(--emb)} .tier-gold .em{color:var(--gold)}
.flourish{position:relative;white-space:nowrap}
.flourish:after{content:"";position:absolute;left:0;right:0;bottom:-.12em;height:5px;border-radius:3px;
 background:linear-gradient(90deg,var(--em),var(--emb));opacity:.9}
.tier-gold .flourish:after{background:linear-gradient(90deg,var(--goldd),var(--gold))}
.bug{position:absolute;left:120px;bottom:60px;display:flex;align-items:center;gap:18px;
 font-family:'JB';font-size:21px;letter-spacing:.16em;color:var(--subtle);text-transform:uppercase}
.bug .mark{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--em),var(--emd));
 display:flex;align-items:center;justify-content:center;font-family:'CG';font-weight:700;color:#06210f;font-size:22px}
.tier-gold .bug .mark{background:linear-gradient(135deg,var(--gold),var(--goldd));color:#241a06}
.src{position:absolute;right:120px;bottom:62px;font-family:'JB';font-size:18px;letter-spacing:.08em;color:var(--faint);text-align:right}
.rankwm{position:absolute;font-family:'CG';font-weight:700;line-height:1;color:rgba(255,255,255,.05);
 font-size:760px;right:40px;top:-90px;user-select:none}
.tier-gold .rankwm{color:rgba(227,199,137,.08)}
.pill{display:inline-flex;align-items:center;gap:10px;padding:13px 22px;border-radius:999px;
 background:rgba(16,185,129,.10);border:1px solid rgba(16,185,129,.28);color:var(--emb);
 font-family:'IN';font-weight:600;font-size:26px}
.tier-gold .pill{background:rgba(227,199,137,.10);border-color:rgba(227,199,137,.30);color:var(--gold)}
.chip{display:inline-flex;align-items:center;padding:11px 20px;border-radius:10px;background:var(--card);
 border:1px solid var(--hair2);color:var(--muted);font-family:'JB';font-size:23px;font-weight:500}
.dot{width:8px;height:8px;border-radius:50%;background:var(--emb)} .tier-gold .dot{background:var(--gold)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--hair);
 border:1px solid var(--hair);border-radius:20px;overflow:hidden}
.stat{background:linear-gradient(180deg,rgba(26,45,66,.82),rgba(19,30,54,.82));padding:34px 34px 30px}
.stat .k{font-family:'JB';font-size:21px;letter-spacing:.14em;text-transform:uppercase;color:var(--subtle)}
.stat .v{font-family:'JB';font-weight:700;font-size:58px;color:var(--snow);margin-top:12px;letter-spacing:-.02em}
.tier-gold .stat .v{color:#fbf3df}
.stat .v.em{color:var(--emb)} .tier-gold .stat .v.em{color:var(--gold)}
.stat .u{font-family:'IN';font-size:21px;color:var(--faint);margin-top:6px}
.watch{display:flex;gap:18px;align-items:flex-start;padding:26px 30px;border-radius:16px;
 background:rgba(251,113,133,.07);border:1px solid rgba(251,113,133,.24)}
.watch .tag{font-family:'JB';font-size:21px;letter-spacing:.16em;color:var(--rose);text-transform:uppercase;white-space:nowrap;padding-top:4px}
.watch .txt{font-family:'IN';font-size:28px;line-height:1.45;color:#fecdd3}
"""

HEAD = """<!doctype html><html{rootcls}><head><meta charset="utf-8"><style>{css}</style></head><body class="{bodycls}">"""

def page(fn, body, bodycls="", transparent=False):
    rootcls = ' class="transparent"' if transparent else ""
    doc = HEAD.format(rootcls=rootcls, css=CSS, bodycls=bodycls) + body + "</body></html>"
    open(os.path.join(HTMLDIR, fn+".html"),"w").write(doc)

def bug():
    return ('<div class="bug"><span class="mark">T</span>'
            'TEMPLETXHOMES.NET&nbsp;&nbsp;·&nbsp;&nbsp;TAYLOR DASCH · EG REALTY</div>')

def src(txt="Source: Central TX MLS · June 18 2026 · active under $250K"):
    return f'<div class="src">{txt}</div>'

# ========== 01 TITLE (cold open) ==========
page("01_title", f"""
<div class="stage">
  <div class="eyebrow">Living in Temple &nbsp;·&nbsp; Relocation Guide</div>
  <div style="margin-top:auto"></div>
  <div class="serif" style="font-size:92px;color:var(--muted);font-weight:500">Temple, Texas</div>
  <div class="serif" style="font-size:172px;margin-top:6px">5 Best Neighborhoods<br><span class="flourish em">Under $250K.</span></div>
  <div style="font-size:38px;color:var(--muted);margin-top:50px;max-width:1180px;line-height:1.4">
    Real MLS numbers from this month &mdash; five neighborhoods where people are
    <b style="color:var(--snow)">genuinely closing under $250,000</b>, every one within
    <b style="color:var(--snow)">12 minutes of Baylor Scott &amp; White.</b></div>
  <div style="margin-top:auto"></div>
</div>
<div style="position:absolute;right:120px;top:150px;text-align:right;font-family:'JB'">
  <div style="font-size:26px;letter-spacing:.2em;color:var(--subtle)">COUNTDOWN&nbsp;&nbsp;#5&nbsp;&rarr;&nbsp;#1</div>
  <div style="font-family:'CG';font-weight:700;font-size:300px;line-height:.86;color:rgba(255,255,255,.06)">05<br>—<br>01</div>
</div>
{bug()}""")

# ========== 02 FRAMEWORK ($250K = NEW or ESTABLISHED) ==========
page("02_framework", f"""
<div class="stage">
  <div class="eyebrow">First, the honest framing</div>
  <div class="serif" style="font-size:120px;margin-top:14px">$250K in Temple buys you <span class="flourish em">one of two things.</span></div>
  <div style="display:flex;gap:34px;margin-top:72px">
    <div style="flex:1;background:linear-gradient(180deg,rgba(26,45,66,.7),rgba(19,30,54,.55));
       border:1px solid var(--hair2);border-radius:22px;padding:52px 48px;position:relative">
       <div class="mono em" style="font-size:30px;letter-spacing:.1em">OPTION A</div>
       <div class="serif" style="font-size:78px;margin-top:16px">Brand-new build</div>
       <div style="font-size:34px;color:var(--muted);margin-top:22px;line-height:1.45">
         Around <b style="color:var(--snow)">1,400 sqft</b> out on the edges of town. Warranties, modern layouts, zero projects.</div>
    </div>
    <div style="display:flex;align-items:center;font-family:'CG';font-weight:600;font-size:64px;color:var(--subtle)">or</div>
    <div style="flex:1;background:linear-gradient(180deg,rgba(26,45,66,.7),rgba(19,30,54,.55));
       border:1px solid var(--hair2);border-radius:22px;padding:52px 48px;position:relative">
       <div class="mono em" style="font-size:30px;letter-spacing:.1em">OPTION B</div>
       <div class="serif" style="font-size:78px;margin-top:16px">Bigger, established</div>
       <div style="font-size:34px;color:var(--muted);margin-top:22px;line-height:1.45">
         <b style="color:var(--snow)">1,600&ndash;2,000+ sqft</b>, &rsquo;80s through the 2010s, closer in. More room, more character.</div>
    </div>
  </div>
  <div style="font-size:30px;color:var(--subtle);margin-top:48px">Neither&rsquo;s wrong. It depends what you value.</div>
  <div style="margin-top:auto"></div>
</div>
{bug()}""")

# ========== NEIGHBORHOOD STAT CARDS ==========
def statcard(key, fileidx):
    d=NB[key]; gold=d.get("gold"); bodycls="tier-gold" if gold else ""
    is_hm = d["rank"]==0
    rn = "HM" if is_hm else f'{d["rank"]:02d}'
    # NB: no .upper() here — .eyebrow CSS already uppercases; .upper() would corrupt HTML entities
    eyebrow = ("Temple &nbsp;·&nbsp; Honorable mention" if is_hm
               else f'Temple &nbsp;·&nbsp; #{d["rank"]} of 5 &nbsp;·&nbsp; {d["tier"]}')
    statitems=[("Median price",d["median"],"closed under $250K",True),
               ("Active now",d["active"],"under $250K",False),
               ("Median size",d["size"],d["era"],False),
               ("To BSW",d["drive"],d["miles"],True)]
    stats="".join(f'<div class="stat"><div class="k">{k}</div><div class="v {"em" if em else ""}">{v}</div><div class="u">{u}</div></div>' for k,v,u,em in statitems)
    chips=[f'<span class="chip">{d["isd"]}</span>', f'<span class="chip">{d["hoa"]}</span>']
    for b in d["builders"]: chips.append(f'<span class="chip">{b}</span>')
    chiprow=f'<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px">{"".join(chips)}</div>'
    best="".join(f'<span class="pill"><span class="dot"></span>{b}</span>' for b in d["best"])
    subline = f'<div class="serif" style="font-size:44px;color:var(--subtle);font-weight:500;margin-top:2px">{d["sub"]}</div>' if d["sub"] else ''
    page(f"{fileidx:02d}_{key}", f"""
<div class="rankwm">{rn}</div>
<div class="stage">
  <div class="eyebrow">{eyebrow}</div>
  <div class="serif" style="font-size:142px;margin-top:12px">{d['name']}</div>
  {subline}
  <div style="font-size:30px;color:var(--muted);margin-top:18px;max-width:1320px;line-height:1.42">{d['note']}</div>
  <div class="stats" style="margin-top:38px">{stats}</div>
  <div style="display:flex;align-items:center;gap:18px;margin-top:28px">
     <span class="mono" style="font-size:22px;letter-spacing:.14em;color:var(--subtle)">RANGE</span>
     <span class="mono" style="font-size:40px;font-weight:700">{d['lo']} &ndash; {d['hi']}</span>
  </div>
  {chiprow}
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:30px">{best}</div>
  <div style="margin-top:auto"></div>
  <div class="watch" style="max-width:1520px"><div class="tag">Watch&nbsp;out</div><div class="txt">{d['watch']}</div></div>
</div>
{bug()}{src()}""", bodycls=bodycls)

for i,k in enumerate(ORDER): statcard(k, 3+i)   # 03..07
statcard("cimarron", 8)                           # 08

# ========== 09 RECAP — every pick by drive time to BSW ==========
# proximity is the unifying thread; bar length = drive minutes (shorter = better)
LB=[("canyon",5),("altavista",8),("western",8),("heritage",9),("oakridge",11)]
maxv=11.0
rows=""
for key,mins in sorted(LB,key=lambda x:x[1]):
    d=NB[key]; w=22+(mins/maxv)*70
    goldrow=d.get("gold")
    barcol="linear-gradient(90deg,#b9974f,#e3c789)" if goldrow else "linear-gradient(90deg,#059669,#34d399)"
    rankcol="var(--gold)" if goldrow else "var(--emb)"
    rows+=f"""
    <div style="display:flex;align-items:center;gap:30px;padding:20px 0;border-bottom:1px solid var(--hair)">
      <div class="serif" style="font-size:60px;width:80px;color:{rankcol};font-weight:700">#{d['rank']}</div>
      <div style="width:470px">
        <div class="serif" style="font-size:48px;line-height:1">{d['name']}</div>
        <div class="mono" style="font-size:20px;color:var(--subtle);letter-spacing:.04em;margin-top:8px">Median {d['median']} · {d['active']} active · {d['isd']}</div>
      </div>
      <div style="flex:1;height:28px;border-radius:16px;background:rgba(255,255,255,.05);position:relative;overflow:hidden">
        <div style="position:absolute;left:0;top:0;bottom:0;width:{w:.0f}%;border-radius:16px;background:{barcol}"></div>
      </div>
      <div class="mono" style="font-size:46px;font-weight:700;width:200px;text-align:right;color:{'#fbf3df' if goldrow else 'var(--snow)'}">{d['drive']}</div>
    </div>"""
page("09_recap", f"""
<div class="stage">
  <div class="eyebrow">The quick summary</div>
  <div class="serif" style="font-size:96px;margin-top:12px">All five, <span class="flourish em">minutes from BSW.</span></div>
  <div style="margin-top:40px">{rows}</div>
  <div style="margin-top:30px;font-size:26px;color:var(--subtle)">Bar = drive time to Baylor Scott &amp; White (shorter is closer). Canyon Creek wins it at 5 minutes.</div>
  <div style="margin-top:auto"></div>
</div>
{bug()}{src("Drive times: Google Maps driving → 2401 S 31st St")}""")

# ========== 10 CTA / END ==========
page("10_cta", f"""
<div class="stage" style="align-items:flex-start">
  <div style="margin-top:auto"></div>
  <div class="eyebrow">Moving to Temple?</div>
  <div class="serif" style="font-size:140px;margin-top:18px;line-height:.98">Tell me your budget &amp;<br><span class="flourish em">must-haves.</span></div>
  <div style="font-size:36px;color:var(--muted);margin-top:46px;max-width:1240px;line-height:1.45">
    Drop them in the comments and I&rsquo;ll tell you which of these I&rsquo;d point you toward first.
    Want to actually walk through one? Reach out &mdash; that&rsquo;s what I do.</div>
  <div style="display:flex;gap:18px;margin-top:50px;flex-wrap:wrap">
    <span class="pill" style="font-size:30px;padding:18px 30px"><span class="dot"></span>templetxhomes.net</span>
    <span class="pill" style="font-size:30px;padding:18px 30px"><span class="dot"></span>254&middot;718&middot;4249</span>
    <span class="pill" style="font-size:30px;padding:18px 30px"><span class="dot"></span>Taylor Dasch · EG Realty</span>
  </div>
  <div style="margin-top:46px;font-family:'JB';font-size:26px;color:var(--subtle);letter-spacing:.04em">
    Next up &rarr; <b style="color:var(--snow)">Best Belton Neighborhoods Under $300K</b></div>
  <div style="margin-top:auto"></div>
</div>
{bug()}""")

# ========== LOWER THIRDS (transparent) ==========
# A — name bug
page("LT_name", """
<div style="position:absolute;left:96px;bottom:120px">
  <div style="display:inline-flex;align-items:stretch;border-radius:16px;overflow:hidden;
     box-shadow:0 24px 60px rgba(0,0,0,.5)">
    <div style="background:linear-gradient(135deg,#10b981,#059669);display:flex;align-items:center;
       padding:0 26px;font-family:'CG';font-weight:700;font-size:52px;color:#06210f">T</div>
    <div style="background:rgba(15,23,42,.92);border:1px solid rgba(255,255,255,.12);border-left:none;padding:22px 40px">
      <div style="font-family:'CG';font-weight:600;font-size:52px;color:#f8fafc;line-height:1">Taylor Dasch</div>
      <div style="font-family:'JB';font-size:23px;letter-spacing:.18em;color:#34d399;margin-top:10px;text-transform:uppercase">Real Estate Agent · EG Realty · Temple, TX</div>
    </div>
  </div>
</div>""", transparent=True)

# B — neighborhood name bug (rank + median + drive + ISD)
def lt_neighborhood(key):
    d=NB[key]; gold=d.get("gold"); is_hm=d["rank"]==0
    em="#e3c789" if gold else "#34d399"
    ranklabel="HM" if is_hm else f'#{d["rank"]}'
    rankfs="92px" if is_hm else "150px"
    page(f"LT_{key}", f"""
<div style="position:absolute;left:96px;bottom:118px">
  <div style="display:flex;align-items:flex-end;gap:24px">
    <div style="font-family:'CG';font-weight:700;font-size:{rankfs};line-height:.8;color:{em};
       text-shadow:0 16px 40px rgba(0,0,0,.6)">{ranklabel}</div>
    <div style="background:rgba(15,23,42,.9);border:1px solid rgba(255,255,255,.12);border-radius:16px;
       padding:22px 36px;box-shadow:0 24px 60px rgba(0,0,0,.5)">
      <div style="font-family:'JB';font-size:22px;letter-spacing:.18em;color:{em};text-transform:uppercase">Temple · {d['isd']} · {d['hoa']}</div>
      <div style="font-family:'CG';font-weight:600;font-size:62px;color:#f8fafc;line-height:1.04;margin-top:6px">{d['name']}</div>
      <div style="font-family:'JB';font-size:29px;color:#e2e8f0;margin-top:10px">Median {d['median']} &nbsp;·&nbsp; {d['drive']} to BSW</div>
    </div>
  </div>
</div>""", transparent=True)
for k in NB: lt_neighborhood(k)

# C — street-theme strip
def lt_streets(key):
    d=NB[key]; gold=d.get("gold"); em="#e3c789" if gold else "#34d399"
    chips="".join(f'<span style="display:inline-flex;align-items:center;padding:12px 24px;border-radius:999px;background:rgba(15,23,42,.92);border:1px solid rgba(255,255,255,.14);font-family:\'JB\';font-size:30px;color:#f8fafc">{s}</span>' for s in d["streets"])
    page(f"ST_{key}", f"""
<div style="position:absolute;left:96px;bottom:120px;display:flex;flex-direction:column;gap:18px">
  <div style="font-family:'JB';font-size:24px;letter-spacing:.24em;text-transform:uppercase;color:{em}">The streets &mdash; {d['name']}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;max-width:1400px">{chips}</div>
</div>""", transparent=True)
for k in ["oakridge","heritage","western","canyon"]: lt_streets(k)

# D — ISD callouts
def isd_strip(fn, big, small, em="#34d399"):
    page(fn, f"""
<div style="position:absolute;left:96px;bottom:120px">
  <div style="display:inline-flex;align-items:stretch;border-radius:16px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.5)">
    <div style="background:linear-gradient(135deg,{em},#0d8a63 70%);display:flex;align-items:center;
       padding:0 30px;font-family:'JB';font-weight:700;font-size:34px;letter-spacing:.06em;color:#06210f">ISD</div>
    <div style="background:rgba(15,23,42,.92);border:1px solid rgba(255,255,255,.12);border-left:none;padding:22px 40px">
      <div style="font-family:'CG';font-weight:600;font-size:50px;color:#f8fafc;line-height:1">{big}</div>
      <div style="font-family:'JB';font-size:26px;color:#e2e8f0;margin-top:10px">{small}</div>
    </div>
  </div>
</div>""", transparent=True)
isd_strip("ISD_academy", "Academy ISD", "Smaller district, strong reputation &mdash; inside Temple&rsquo;s city limits", em="#e3c789")
isd_strip("ISD_oakchain", "Temple ISD", "Garcia Elementary &rarr; Lamar Middle &rarr; Temple High")
isd_strip("ISD_temple", "Temple ISD", "The zoned district for this neighborhood")

print("HTML written:", len([f for f in os.listdir(HTMLDIR) if f.endswith('.html')]), "files ->", HTMLDIR)
