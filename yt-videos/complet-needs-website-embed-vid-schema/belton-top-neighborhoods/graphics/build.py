# Belton Top Neighborhoods — premium graphics generator
# Brand: templetxhomes.net / Taylor Dasch / "Living in Temple"
# Renders 1920x1080 HTML -> 4K PNG via headless Chrome.
import os, html
HERE = os.path.dirname(os.path.abspath(__file__))
HTMLDIR = os.path.join(HERE, "html"); os.makedirs(HTMLDIR, exist_ok=True)

# ---------- VERIFIED DATA (Central TX MLS, trailing 12-mo CLOSED sales, Belton) ----------
# n = closed-sale count in trailing 12 mo from belton-only-data-0-365.csv
NB = {
 "morgans": dict(rank=1, tier="cheapest", name="Morgan&rsquo;s Point", sub="Resort",
    median="$247K", psf="$179", n="36", dom="64", lo="$160K", hi="$825K", size="1,400 sf · built ~1997",
    best=["Lake &amp; marina access","Lowest entry into Belton","Land / acreage feel"],
    watch="Mid-90s homes, septic, foundation &amp; manufactured homes nearby — inspect everything.",
    note="Belton address &amp; Belton ISD · its own little resort city · widest price range in the area",
    builders=[]),
 "bellmeadows": dict(rank=2, tier="cheapest new build", name="The Ridge at Bell Meadows", sub="",
    median="$232&ndash;300K", psf="builder", n="NEW", dom="—", lo="$232K", hi="$300K", size="~1,200&ndash;2,200 sf · new",
    best=["First-time buyers","Right-size / downsizing","New build, Belton ISD"],
    watch="Smaller homes &amp; lots, basic&ndash;mid finishes, farther west. Numbers are builder pricing.",
    note="Stylecraft Homes · cheapest new construction in Belton",
    builders=["Stylecraft"], src_override="Builder price sheet (Stylecraft) — limited MLS resale history"),
 "threecreeks": dict(rank=3, tier="top pick", name="Three Creeks", sub="",
    median="$316K", psf="$166", n="119", dom="53", lo="$215K", hi="$499K", size="1,950 sf · built ~2025",
    best=["First-time &rarr; luxury buyers","Master-plan amenities","Builder incentives"],
    watch="Farther from Temple shopping — but ~12&ndash;15 min to Baylor Scott &amp; White.",
    note="MOST sales of any Belton neighborhood this year · trails, ponds, dark skies",
    builders=["D.R. Horton","Stylecraft","Tippit Homes","Carothers"]),
 "dawson": dict(rank=4, tier="step-up / premium", name="Dawson Ranch &amp; Ridge", sub="",
    median="$400K", psf="$183", n="29", dom="50", lo="$283K", hi="$580K", size="2,280 sf · built ~2016",
    best=["Step-up buyers","Out-of-state relocations","Bigger lots &amp; mature trees"],
    watch="Competes with new builds &amp; lake homes — layout has to be right. (Anecdotal ceiling ~$700K.)",
    note="Newer + older sections · higher finishes · sells fast for the price point",
    builders=["Carothers Executive"]),
 "lake": dict(rank=5, tier="luxury / lakefront", name="The Lake Neighborhoods", sub="Rancho · Colinas · Del Lago",
    median="$765K", psf="$248", n="15&ndash;19", dom="96", lo="$600K", hi="$970K", size="2,900 sf · custom",
    best=["Lakefront luxury buyers","Equity relocations","Custom, 4-side stone"],
    watch="Flood zones spike insurance — verify before you buy. ~96 days on market = buyer leverage.",
    note="&ldquo;Lago&rdquo; = lake · the homes that separate Belton from Temple · rarely come up",
    builders=[], gold=True),
}
ORDER = ["morgans","bellmeadows","threecreeks","dawson","lake"]

# ---------- DESIGN SYSTEM ----------
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
 --snow:#f8fafc;--muted:#cbd5e1;--subtle:#94a3b8;--faint:#64748b;
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
/* faint dot grid + vignette */
body:before{content:"";position:absolute;inset:0;
 background-image:radial-gradient(rgba(255,255,255,.05) 1.1px, transparent 1.2px);
 background-size:46px 46px;opacity:.5;mask-image:linear-gradient(135deg,rgba(0,0,0,.9),transparent 70%)}
body:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 360px rgba(0,0,0,.55);pointer-events:none}
.transparent,.transparent body{background:transparent !important}
.transparent:before,.transparent:after{display:none}
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
/* brand bug */
.bug{position:absolute;left:120px;bottom:60px;display:flex;align-items:center;gap:18px;
 font-family:'JB';font-size:21px;letter-spacing:.16em;color:var(--subtle);text-transform:uppercase}
.bug .mark{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--em),var(--emd));
 display:flex;align-items:center;justify-content:center;font-family:'CG';font-weight:700;color:#06210f;font-size:22px}
.tier-gold .bug .mark{background:linear-gradient(135deg,var(--gold),var(--goldd));color:#241a06}
.src{position:absolute;right:120px;bottom:62px;font-family:'JB';font-size:18px;letter-spacing:.08em;color:var(--faint);text-align:right}
.rankwm{position:absolute;font-family:'CG';font-weight:700;line-height:1;color:rgba(255,255,255,.045);
 font-size:760px;right:40px;top:-90px;user-select:none}
.tier-gold .rankwm{color:rgba(227,199,137,.07)}
/* pills + chips */
.pill{display:inline-flex;align-items:center;gap:10px;padding:13px 22px;border-radius:999px;
 background:rgba(16,185,129,.10);border:1px solid rgba(16,185,129,.28);color:var(--emb);
 font-family:'IN';font-weight:600;font-size:26px}
.tier-gold .pill{background:rgba(227,199,137,.10);border-color:rgba(227,199,137,.30);color:var(--gold)}
.chip{display:inline-flex;align-items:center;padding:11px 20px;border-radius:10px;background:var(--card);
 border:1px solid var(--hair2);color:var(--muted);font-family:'JB';font-size:23px;font-weight:500}
.dot{width:8px;height:8px;border-radius:50%;background:var(--emb)} .tier-gold .dot{background:var(--gold)}
/* stat grid */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--hair);
 border:1px solid var(--hair);border-radius:20px;overflow:hidden}
.stat{background:linear-gradient(180deg,rgba(26,45,66,.82),rgba(19,30,54,.82));padding:34px 34px 30px}
.stat .k{font-family:'JB';font-size:21px;letter-spacing:.14em;text-transform:uppercase;color:var(--subtle)}
.stat .v{font-family:'JB';font-weight:700;font-size:62px;color:var(--snow);margin-top:12px;letter-spacing:-.02em}
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

def bug(gold=False):
    return ('<div class="bug"><span class="mark">T</span>'
            'TEMPLETXHOMES.NET&nbsp;&nbsp;·&nbsp;&nbsp;TAYLOR DASCH · EG REALTY</div>')

def src(txt="Source: Central TX MLS · trailing 12-mo closed sales"):
    return f'<div class="src">{txt}</div>'

# ---------- G1 TITLE ----------
page("01_title", f"""
<div class="stage">
  <div class="eyebrow">Living in Temple &nbsp;·&nbsp; Market Intelligence</div>
  <div style="margin-top:auto"></div>
  <div class="serif" style="font-size:96px;color:var(--muted);font-weight:500">Belton, Texas</div>
  <div class="serif" style="font-size:188px;margin-top:6px">The 5 Best Neighborhoods,<br><span class="flourish em">Ranked.</span></div>
  <div style="font-size:38px;color:var(--muted);margin-top:54px;max-width:1180px;line-height:1.4">
    I pulled <b style="color:var(--snow)">every home sale from the last 12 months</b> &mdash; ranked cheapest to most expensive,
    with who each one fits and the catch nobody tells you.</div>
  <div style="margin-top:auto"></div>
</div>
<div style="position:absolute;right:120px;top:150px;text-align:right;font-family:'JB'">
  <div style="font-size:26px;letter-spacing:.2em;color:var(--subtle)">CHEAPEST&nbsp;&rarr;&nbsp;PRICIEST</div>
  <div style="font-family:'CG';font-weight:700;font-size:300px;line-height:.86;color:rgba(255,255,255,.06)">01<br>—<br>05</div>
</div>
{bug()}""")

# ---------- G2 FRAMEWORK ----------
crit = [("01","What it costs","Real median price, $/sqft &amp; the true range from MLS closings."),
        ("02","Who it&rsquo;s for","The exact buyer each neighborhood actually fits."),
        ("03","The catch","The downside I&rsquo;d flag before you write an offer.")]
cards = "".join(f"""
 <div style="flex:1;background:linear-gradient(180deg,rgba(26,45,66,.7),rgba(19,30,54,.55));
   border:1px solid var(--hair2);border-radius:22px;padding:48px 44px;position:relative">
   <div class="mono em" style="font-size:30px;letter-spacing:.1em">{n}</div>
   <div class="serif" style="font-size:62px;margin-top:18px">{t}</div>
   <div style="font-size:29px;color:var(--muted);margin-top:20px;line-height:1.45">{d}</div>
 </div>""" for n,t,d in crit)
page("02_framework", f"""
<div class="stage">
  <div class="eyebrow">For every neighborhood</div>
  <div class="serif" style="font-size:118px;margin-top:18px">Three things, <span class="flourish em">every time.</span></div>
  <div style="display:flex;gap:34px;margin-top:72px">{cards}</div>
  <div style="margin-top:auto"></div>
</div>
{bug()}""")

# ---------- NEIGHBORHOOD STAT CARDS ----------
def statcard(key):
    d=NB[key]; gold = d.get("gold"); bodycls="tier-gold" if gold else ""
    rn=f'{d["rank"]:02d}'
    builders = ""
    if d["builders"]:
        chips="".join(f'<span class="chip">{b}</span>' for b in d["builders"])
        builders=f'<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px"><span class="mono" style="font-size:21px;letter-spacing:.14em;color:var(--subtle);align-self:center">BUILDERS&nbsp;&nbsp;</span>{chips}</div>'
    best="".join(f'<span class="pill"><span class="dot"></span>{b}</span>' for b in d["best"])
    statitems=[("Median price",d["median"],"closed, 12 mo",True),
               ("Price / sqft",d["psf"],"",False),
               ("Closed sales",d["n"],"last 12 mo",False),
               ("Days on market",d["dom"],"median",False)]
    stats="".join(f'<div class="stat"><div class="k">{k}</div><div class="v {"em" if em else ""}">{v}</div><div class="u">{u}</div></div>' for k,v,u,em in statitems)
    srcline = d.get("src_override") and f"Source: {d['src_override']}" or "Source: Central TX MLS · trailing 12-mo closed sales"
    return page(f"{2+d['rank']:02d}_{key}", f"""
<div class="rankwm">{rn}</div>
<div class="stage">
  <div class="eyebrow">Belton &nbsp;·&nbsp; Ranked #{d['rank']} &nbsp;·&nbsp; {d['tier'].upper()}</div>
  <div class="serif" style="font-size:142px;margin-top:14px">{d['name']}</div>
  {f'<div class="serif" style="font-size:46px;color:var(--subtle);font-weight:500;margin-top:2px">{d["sub"]}</div>' if d['sub'] else ''}
  <div style="font-size:28px;color:var(--muted);margin-top:18px;max-width:1300px;line-height:1.4">{d['note']}</div>
  <div class="stats" style="margin-top:40px">{stats}</div>
  <div style="display:flex;align-items:center;gap:18px;margin-top:30px">
     <span class="mono" style="font-size:22px;letter-spacing:.14em;color:var(--subtle)">RANGE</span>
     <span class="mono" style="font-size:40px;font-weight:700">{d['lo']} &ndash; {d['hi']}</span>
     <span style="width:1px;height:34px;background:var(--hair2)"></span>
     <span class="mono" style="font-size:28px;color:var(--muted)">{d['size']}</span>
  </div>
  {builders}
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:32px">{best}</div>
  <div style="margin-top:auto"></div>
  <div class="watch" style="max-width:1480px"><div class="tag">Watch&nbsp;out</div><div class="txt">{d['watch']}</div></div>
</div>
{bug(gold)}{src(srcline)}""", bodycls=bodycls)

for k in ORDER: statcard(k)

# ---------- P1 PROPERTY TAX ----------
page("08_tax", f"""
<div class="stage">
  <div class="eyebrow">Quick pit stop &nbsp;·&nbsp; Before the luxury homes</div>
  <div class="serif" style="font-size:120px;margin-top:16px">The tax line nobody <span class="flourish em">checks.</span></div>
  <div style="margin-top:64px;background:linear-gradient(180deg,rgba(26,45,66,.65),rgba(19,30,54,.5));
     border:1px solid var(--hair2);border-radius:22px;padding:54px 60px">
     <div style="display:flex;justify-content:space-between;font-family:'JB';font-size:26px;letter-spacing:.1em;color:var(--muted)">
        <span>INSIDE BELTON CITY LIMITS</span><span>OUT IN THE COUNTY</span></div>
     <div style="height:26px;border-radius:14px;margin:26px 0 14px;
        background:linear-gradient(90deg,#fb7185,#fbbf24 50%,#10b981)"></div>
     <div style="display:flex;justify-content:space-between;font-family:'IN';font-size:30px;color:var(--snow)">
        <span><b>Highest</b> tax rate</span><span><b>Lower</b> base rate</span></div>
  </div>
  <div style="display:flex;gap:34px;margin-top:40px">
     <div style="flex:1;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.28);border-radius:18px;padding:38px 40px">
       <div class="mono" style="font-size:24px;letter-spacing:.12em;color:var(--amber)">+ MUD DISTRICTS</div>
       <div style="font-size:31px;color:#fde9c0;margin-top:16px;line-height:1.4">Can add a whole price range to your payment &mdash; without you even knowing it.</div>
     </div>
     <div style="flex:1;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.26);border-radius:18px;padding:38px 40px">
       <div class="mono em" style="font-size:24px;letter-spacing:.12em">THE RULE</div>
       <div style="font-size:31px;color:#c9f3e3;margin-top:16px;line-height:1.4">Confirm the exact rate <b>before</b> you go under contract. Work with me &mdash; I&rsquo;ll get you the real monthly number.</div>
     </div>
  </div>
  <div style="margin-top:auto"></div>
</div>
{bug()}""")

# ---------- S1 RECAP LEADERBOARD (hero) ----------
LB=[("morgans","$247K",247),("bellmeadows","$266K*",266),("threecreeks","$316K",316),("dawson","$400K",400),("lake","$765K",765)]
maxv=765.0
rows=""
for key,label,val in LB:
    d=NB[key]; w=18+ (val/maxv)*78  # bar width %
    goldrow = d.get("gold")
    barcol = "linear-gradient(90deg,#b9974f,#e3c789)" if goldrow else "linear-gradient(90deg,#059669,#34d399)"
    tag=d["best"][0]
    rows+=f"""
    <div style="display:flex;align-items:center;gap:30px;padding:22px 0;border-bottom:1px solid var(--hair)">
      <div class="serif" style="font-size:64px;width:90px;color:{'var(--gold)' if goldrow else 'var(--emb)'};font-weight:700">{d['rank']}</div>
      <div style="width:520px">
        <div class="serif" style="font-size:50px;line-height:1">{d['name']}</div>
        <div class="mono" style="font-size:20px;color:var(--subtle);letter-spacing:.06em;margin-top:8px">{tag}</div>
      </div>
      <div style="flex:1;height:30px;border-radius:16px;background:rgba(255,255,255,.05);position:relative;overflow:hidden">
        <div style="position:absolute;left:0;top:0;bottom:0;width:{w:.0f}%;border-radius:16px;background:{barcol}"></div>
      </div>
      <div class="mono" style="font-size:50px;font-weight:700;width:230px;text-align:right;color:{'#fbf3df' if goldrow else 'var(--snow)'}">{label}</div>
    </div>"""
page("09_recap", f"""
<div class="stage">
  <div class="eyebrow">The quick summary</div>
  <div class="serif" style="font-size:104px;margin-top:14px">Belton, <span class="flourish em">ranked.</span></div>
  <div style="margin-top:48px">{rows}</div>
  <div style="margin-top:auto"></div>
</div>
<div style="position:absolute;right:120px;bottom:62px;font-family:'JB';font-size:18px;color:var(--faint);text-align:right">
   Median closed price, trailing 12 mo · Central TX MLS<br>*Bell Meadows = Stylecraft builder pricing</div>
{bug()}""")

# ---------- S2 CTA END ----------
page("10_cta", f"""
<div class="stage" style="align-items:flex-start">
  <div style="margin-top:auto"></div>
  <div class="eyebrow">Relocating to Temple &amp; Belton?</div>
  <div class="serif" style="font-size:150px;margin-top:18px;line-height:.98">Let&rsquo;s build your<br><span class="flourish em">shortlist.</span></div>
  <div style="font-size:36px;color:var(--muted);margin-top:48px;max-width:1240px;line-height:1.45">
    Every home I send you comes with a full <b style="color:var(--snow)">neighborhood video</b> &mdash; so you know the
    streets, the taxes and the catch before you ever fly in.</div>
  <div style="display:flex;gap:18px;margin-top:52px;flex-wrap:wrap">
    <span class="pill" style="font-size:30px;padding:18px 30px"><span class="dot"></span>templetxhomes.net</span>
    <span class="pill" style="font-size:30px;padding:18px 30px"><span class="dot"></span>254&middot;718&middot;4249</span>
    <span class="pill" style="font-size:30px;padding:18px 30px"><span class="dot"></span>Taylor Dasch · EG Realty</span>
  </div>
  <div style="margin-top:auto"></div>
</div>
{bug()}""")

# ---------- LOWER THIRDS (transparent) ----------
# LT-A name bug
page("LT_name", """
<div style="position:absolute;left:96px;bottom:120px">
  <div style="display:inline-flex;align-items:stretch;border-radius:16px;overflow:hidden;
     box-shadow:0 24px 60px rgba(0,0,0,.5);backdrop-filter:blur(2px)">
    <div style="background:linear-gradient(135deg,#10b981,#059669);display:flex;align-items:center;
       padding:0 26px;font-family:'CG';font-weight:700;font-size:52px;color:#06210f">T</div>
    <div style="background:rgba(15,23,42,.92);border:1px solid rgba(255,255,255,.12);border-left:none;padding:22px 40px">
      <div style="font-family:'CG';font-weight:600;font-size:52px;color:#f8fafc;line-height:1">Taylor Dasch</div>
      <div style="font-family:'JB';font-size:24px;letter-spacing:.18em;color:#34d399;margin-top:10px;text-transform:uppercase">EG Realty &nbsp;·&nbsp; Temple&ndash;Belton, TX</div>
    </div>
  </div>
</div>""", transparent=True)

# LT-B neighborhood name + median (for walk-and-talk)
def lt_neighborhood(key):
    d=NB[key]; gold=d.get("gold")
    em = "#e3c789" if gold else "#34d399"
    page(f"LT_{key}", f"""
<div style="position:absolute;left:96px;bottom:118px">
  <div style="display:flex;align-items:flex-end;gap:24px">
    <div style="font-family:'CG';font-weight:700;font-size:150px;line-height:.8;color:{em};
       text-shadow:0 16px 40px rgba(0,0,0,.6)">{d['rank']}</div>
    <div style="background:rgba(15,23,42,.9);border:1px solid rgba(255,255,255,.12);border-radius:16px;
       padding:22px 36px;box-shadow:0 24px 60px rgba(0,0,0,.5)">
      <div style="font-family:'JB';font-size:22px;letter-spacing:.2em;color:{em};text-transform:uppercase">Belton · {d['tier']}</div>
      <div style="font-family:'CG';font-weight:600;font-size:64px;color:#f8fafc;line-height:1.04;margin-top:6px">{d['name']}</div>
      <div style="font-family:'JB';font-size:30px;color:#cbd5e1;margin-top:10px">Median {d['median']} &nbsp;·&nbsp; {d['psf']}{'/sf' if d['psf'].startswith('$') else ''}</div>
    </div>
  </div>
</div>""", transparent=True)
for k in ORDER: lt_neighborhood(k)

# stat pop token
page("POP_stat", """
<div style="position:absolute;right:130px;top:160px">
  <div style="background:linear-gradient(135deg,#10b981,#059669);border-radius:22px;padding:30px 46px;
     box-shadow:0 30px 70px rgba(5,150,105,.35);text-align:center">
    <div style="font-family:'JB';font-weight:700;font-size:104px;color:#fff;line-height:.9">$179</div>
    <div style="font-family:'JB';font-size:30px;letter-spacing:.22em;color:#06210f;margin-top:10px">PER SQFT</div>
  </div>
</div>""", transparent=True)

print("HTML written:", len(os.listdir(HTMLDIR)), "files ->", HTMLDIR)
