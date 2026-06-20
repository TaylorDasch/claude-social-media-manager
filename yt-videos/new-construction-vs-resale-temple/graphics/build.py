#!/usr/bin/env python3
"""New Construction vs Resale in Temple TX graphics generator.

Builds branded 1920x1080 HTML files for rendering into 4K PNGs.
Channel: Living in Temple TX / Taylor Dasch / EG Realty
"""
from pathlib import Path

HERE = Path(__file__).parent.resolve()
HTMLDIR = HERE / "html"
HTMLDIR.mkdir(exist_ok=True)

SOURCE_LABEL = "Temple MLS closed sales, Jun. 18, 2026 pull"
INCENTIVE_LABEL = "June 19 builder-incentive feed"
PAGE_URL = "templetxhomes.net/new-construction-vs-resale/"

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
  --ink:#111315;
  --forest:#13271f;
  --panel:#f7f4ed;
  --panel2:#ece4d5;
  --snow:#f8fafc;
  --muted:#cbd5d2;
  --subtle:#8fa29b;
  --faint:#6f7f79;
  --emerald:#059669;
  --emerald2:#34d399;
  --gold:#d4a853;
  --amber:#f2b84b;
  --blue:#4d87a8;
  --rose:#c95b55;
  --hair:rgba(255,255,255,.12);
  --hair2:rgba(17,19,21,.12);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;overflow:hidden}
body{
  font-family:'IN',sans-serif;
  color:var(--snow);
  background:
    linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px),
    linear-gradient(0deg,rgba(255,255,255,.026) 1px,transparent 1px),
    linear-gradient(135deg,#111315 0%,#13271f 52%,#181815 100%);
  background-size:72px 72px,72px 72px,auto;
  position:relative;
}
body:before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:
    linear-gradient(118deg,transparent 0 50%,rgba(212,168,83,.075) 50.1% 50.6%,transparent 50.7%),
    linear-gradient(22deg,transparent 0 61%,rgba(77,135,168,.07) 61.1% 61.6%,transparent 61.7%);
  opacity:.8;
}
body:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 300px rgba(0,0,0,.48);pointer-events:none}
html.transparent,html.transparent body{background:transparent!important}
html.transparent body:before,html.transparent body:after{display:none!important}
.stage{position:absolute;inset:0;padding:86px 112px;display:flex;flex-direction:column;z-index:1}
.eyebrow{font-family:'JB';font-size:22px;font-weight:500;letter-spacing:.32em;text-transform:uppercase;color:var(--emerald2)}
.eyebrow.gold{color:var(--gold)}
.serif{font-family:'CG';font-weight:600;line-height:.96;letter-spacing:0}
.mono{font-family:'JB'}
.em{color:var(--emerald2)}
.gold{color:var(--gold)}
.blue{color:var(--blue)}
.rose{color:var(--rose)}
.rule{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--hair),transparent)}
.brandbug{
  position:absolute;left:112px;bottom:54px;display:flex;align-items:center;gap:16px;
  font-family:'JB';font-size:19px;letter-spacing:.14em;color:var(--subtle);text-transform:uppercase;z-index:2;
}
.brandbug .mark{
  width:34px;height:34px;border-radius:8px;background:linear-gradient(135deg,var(--emerald2),var(--emerald));
  color:#052115;display:flex;align-items:center;justify-content:center;font-family:'CG';font-weight:700;font-size:22px;
}
.source{
  position:absolute;right:112px;bottom:58px;max-width:720px;text-align:right;
  font-family:'JB';font-size:17px;letter-spacing:.06em;color:var(--faint);z-index:2;
}
.panel{
  background:linear-gradient(180deg,var(--panel),var(--panel2));
  color:var(--ink);border:1px solid rgba(255,255,255,.36);border-radius:10px;
  box-shadow:0 26px 90px rgba(0,0,0,.28);
}
.darkpanel{
  background:rgba(17,19,21,.68);border:1px solid var(--hair);border-radius:10px;
  box-shadow:0 26px 90px rgba(0,0,0,.22);
}
.mini{font-family:'JB';font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
.big{font-family:'CG';font-size:132px;font-weight:700;line-height:.9;letter-spacing:0}
.num{font-family:'JB';font-weight:700;letter-spacing:-.03em}
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:rgba(17,19,21,.14);border-radius:8px;overflow:hidden}
.metric{background:rgba(255,255,255,.68);padding:30px 28px}
.metric .k{font-family:'JB';font-size:18px;letter-spacing:.12em;text-transform:uppercase;color:#69756f}
.metric .v{font-family:'JB';font-size:48px;font-weight:700;color:var(--ink);margin-top:10px;letter-spacing:-.03em}
.metric .s{font-size:19px;color:#68746f;margin-top:4px}
.pill{
  display:inline-flex;align-items:center;gap:10px;padding:12px 18px;border-radius:999px;
  background:rgba(5,150,105,.11);border:1px solid rgba(5,150,105,.28);color:#dffcef;
  font-family:'JB';font-size:22px;font-weight:500;
}
.pill.gold{background:rgba(212,168,83,.12);border-color:rgba(212,168,83,.34);color:#fee8ad}
.pill.blue{background:rgba(77,135,168,.14);border-color:rgba(77,135,168,.34);color:#d8effa}
.pill.rose{background:rgba(201,91,85,.14);border-color:rgba(201,91,85,.36);color:#ffd4d1}
.lightpill{
  display:inline-flex;align-items:center;gap:10px;padding:12px 18px;border-radius:999px;
  font-family:'JB';font-size:22px;font-weight:700;
  background:#eef5f0;border:1px solid rgba(17,19,21,.16);color:#143329;
}
.lightpill.gold{background:#f6ecd2;border-color:rgba(212,168,83,.38);color:#7a5515}
.lightpill.blue{background:#e4edf1;border-color:rgba(77,135,168,.36);color:#24566f}
.tag{
  display:inline-flex;align-items:center;padding:8px 14px;border-radius:7px;
  font-family:'JB';font-size:18px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  background:#102820;color:#bfffe5;border:1px solid rgba(5,150,105,.36);
}
.tag.gold{background:#302614;color:#ffe4a3;border-color:rgba(212,168,83,.46)}
.tag.rose{background:#321a18;color:#ffd7d4;border-color:rgba(201,91,85,.46)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:34px}
.column-title{font-family:'JB';font-size:26px;letter-spacing:.18em;text-transform:uppercase}
.bullet{display:flex;gap:16px;align-items:flex-start;font-size:28px;line-height:1.28;color:#24302c}
.bullet:before{content:"";width:10px;height:10px;border-radius:50%;margin-top:12px;background:var(--emerald)}
.bullet.gold:before{background:var(--gold)}
.lower{
  position:absolute;left:112px;bottom:76px;width:max-content;max-width:1320px;
  display:flex;align-items:center;gap:18px;padding:22px 28px;border-radius:10px;
  background:rgba(17,19,21,.88);border:1px solid rgba(255,255,255,.18);
  box-shadow:0 18px 60px rgba(0,0,0,.35);z-index:5;
}
.lower .label{font-family:'JB';font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.lower .text{font-family:'IN';font-size:31px;font-weight:700;color:var(--snow)}
.tiny{font-size:20px;line-height:1.35;color:var(--faint)}
"""


def page(name: str, body: str, transparent: bool = False) -> None:
    rootcls = ' class="transparent"' if transparent else ""
    doc = (
        f'<!doctype html><html{rootcls}><head><meta charset="utf-8">'
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )
    (HTMLDIR / f"{name}.html").write_text(doc, encoding="utf-8")


def bug() -> str:
    return (
        '<div class="brandbug"><span class="mark">T</span>'
        "Living in Temple TX&nbsp;&nbsp;|&nbsp;&nbsp;Taylor Dasch · EG Realty</div>"
    )


def source(text: str = SOURCE_LABEL) -> str:
    return f'<div class="source">{text}</div>'


def metric(k: str, v: str, s: str = "") -> str:
    return f'<div class="metric"><div class="k">{k}</div><div class="v">{v}</div><div class="s">{s}</div></div>'


# 01. Title / cold open stinger
page(
    "01-title-77-day-gap",
    f"""
<div class="stage">
  <div class="eyebrow">Living in Temple TX &nbsp;|&nbsp; Buyer intelligence</div>
  <div style="display:grid;grid-template-columns:1.05fr .95fr;gap:54px;align-items:center;flex:1">
    <div>
      <div class="serif" style="font-size:174px">New<br><span class="gold">vs</span> Resale</div>
      <div style="margin-top:32px;display:inline-flex;align-items:center;gap:18px" class="tag gold">Temple TX · 2026</div>
      <div style="margin-top:42px;font-size:39px;line-height:1.28;color:var(--muted);max-width:900px">
        Same price can mean two very different deals once taxes, incentives, fees, and leverage hit the monthly payment.
      </div>
    </div>
    <div class="panel" style="padding:54px 56px;min-height:700px;display:flex;flex-direction:column;justify-content:space-between">
      <div class="mini">The decision number</div>
      <div class="num" style="font-size:198px;color:var(--emerald);line-height:.82">77</div>
      <div class="serif" style="font-size:86px;color:var(--ink);line-height:.92">days<br>longer</div>
      <div style="height:1px;background:var(--hair2);margin:28px 0"></div>
      <div style="font-size:33px;line-height:1.25;color:#2b3632">
        New construction sat longer than resale in the latest Temple pull.
      </div>
    </div>
  </div>
</div>
{bug()}{source()}
""",
)


# 02. Main comparison
page(
    "02-main-comparison",
    f"""
<div class="stage">
  <div class="eyebrow">The frame</div>
  <div class="serif" style="font-size:116px;margin-top:18px">Do not compare only the list price.</div>
  <div class="split" style="margin-top:54px">
    <div class="panel" style="padding:42px">
      <div class="column-title" style="color:var(--emerald)">New construction</div>
      <div class="metric-grid" style="margin-top:30px">
        {metric("Median price", "$290,950", "n = 122")}
        {metric("Price / sqft", "$172", "per square foot")}
        {metric("Market time", "133", "days on market")}
        {metric("Signal", "Slow", "more leverage")}
      </div>
    </div>
    <div class="panel" style="padding:42px">
      <div class="column-title" style="color:var(--blue)">Resale</div>
      <div class="metric-grid" style="margin-top:30px">
        {metric("Median price", "$265,000", "n = 299")}
        {metric("Price / sqft", "$152", "per square foot")}
        {metric("Market time", "56", "days on market")}
        {metric("Signal", "Fast", "less leverage")}
      </div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:34px">
    <div class="darkpanel" style="padding:30px 34px"><div class="mini">Median gap</div><div class="num gold" style="font-size:72px;margin-top:6px">+$25,950</div></div>
    <div class="darkpanel" style="padding:30px 34px"><div class="mini">New premium / sqft</div><div class="num gold" style="font-size:72px;margin-top:6px">+13.2%</div></div>
    <div class="darkpanel" style="padding:30px 34px"><div class="mini">Market-time gap</div><div class="num em" style="font-size:72px;margin-top:6px">+77 days</div></div>
  </div>
</div>
{bug()}{source()}
""",
)


# 03. Price per square foot
page(
    "03-price-per-sqft",
    f"""
<div class="stage">
  <div class="eyebrow">Price per foot reality</div>
  <div class="serif" style="font-size:118px;margin-top:18px">New costs more per foot before the hidden costs.</div>
  <div class="panel" style="margin-top:66px;padding:58px 66px">
    <div style="display:grid;grid-template-columns:240px 1fr 240px;gap:34px;align-items:center">
      <div>
        <div class="mini">Resale</div>
        <div class="num" style="font-size:80px;color:var(--blue);margin-top:10px">$152</div>
      </div>
      <div style="height:54px;border-radius:8px;background:#d8ddda;position:relative;overflow:hidden">
        <div style="position:absolute;left:0;top:0;bottom:0;width:88%;background:var(--blue)"></div>
        <div style="position:absolute;left:88%;top:-20px;width:12%;height:94px;background:var(--emerald)"></div>
      </div>
      <div style="text-align:right">
        <div class="mini">New</div>
        <div class="num" style="font-size:80px;color:var(--emerald);margin-top:10px">$172</div>
      </div>
    </div>
    <div style="margin-top:56px;display:flex;justify-content:space-between;align-items:end">
      <div style="font-size:37px;line-height:1.25;color:#26322e;max-width:970px">
        Sometimes the premium is worth it. The question is whether the incentive, tax bill, and inspection risk still make the total deal work.
      </div>
      <div style="text-align:right">
        <div class="mini">Premium to buy new</div>
        <div class="num" style="font-size:116px;color:var(--gold);line-height:.88">+13.2%</div>
      </div>
    </div>
  </div>
</div>
{bug()}{source()}
""",
)


# 04. Tax example
page(
    "04-tax-line-buyers-miss",
    f"""
<div class="stage">
  <div class="eyebrow gold">The tax line buyers miss</div>
  <div class="serif" style="font-size:116px;margin-top:18px">A builder incentive can disappear inside the tax bill.</div>
  <div class="split" style="margin-top:58px">
    <div class="panel" style="padding:48px">
      <div class="column-title" style="color:var(--blue)">Normal Temple example</div>
      <div class="serif" style="font-size:62px;color:var(--ink);margin-top:24px">$280K home</div>
      <div style="margin-top:28px" class="metric-grid">
        {metric("Tax rate", "2.37%", "example rate")}
        {metric("Annual tax", "$6,636", "per year")}
        {metric("Monthly", "$553", "approx.")}
        {metric("District", "$0", "in this example")}
      </div>
    </div>
    <div class="panel" style="padding:48px;border-color:rgba(212,168,83,.8)">
      <div class="column-title" style="color:var(--rose)">With district-charge example</div>
      <div class="serif" style="font-size:62px;color:var(--ink);margin-top:24px">$280K home</div>
      <div style="margin-top:28px" class="metric-grid">
        {metric("Base + district", "~3.51%", "derived example")}
        {metric("Annual tax", "$9,836", "per year")}
        {metric("Monthly", "$820", "approx.")}
        {metric("Extra", "+$267", "per month")}
      </div>
    </div>
  </div>
  <div style="margin-top:24px;display:flex;align-items:center;justify-content:space-between;gap:30px">
    <div style="display:flex;align-items:center;gap:20px;max-width:1220px">
      <div class="tag rose">MUD / PID check</div>
      <div style="font-size:30px;line-height:1.18;color:var(--snow)">Do not assume yes. Do not assume no. Verify the exact parcel before comparing payments.</div>
    </div>
    <div class="num gold" style="font-size:64px;white-space:nowrap">+$3,200 / yr</div>
  </div>
</div>
{bug()}{source("Source: templetxhomes.net · district-charge example · verify exact parcel")}
""",
)


# 05. Leverage flip
page(
    "05-leverage-flip",
    f"""
<div class="stage" style="justify-content:center">
  <div class="eyebrow">The leverage flip</div>
  <div style="display:flex;align-items:center;gap:46px;margin-top:38px">
    <div class="panel" style="padding:54px 62px;text-align:center;min-width:500px">
      <div class="mini">Resale moved in</div>
      <div class="num" style="font-size:152px;color:var(--blue);line-height:.86">56</div>
      <div class="serif" style="font-size:64px;color:var(--ink)">days</div>
    </div>
    <div class="serif gold" style="font-size:98px">vs</div>
    <div class="panel" style="padding:54px 62px;text-align:center;min-width:500px;border-color:rgba(5,150,105,.7)">
      <div class="mini">New moved in</div>
      <div class="num" style="font-size:152px;color:var(--emerald);line-height:.86">133</div>
      <div class="serif" style="font-size:64px;color:var(--ink)">days</div>
    </div>
  </div>
  <div class="serif" style="font-size:126px;margin-top:56px;text-align:center"><span class="gold">+77</span> = your leverage</div>
  <div style="font-size:35px;color:var(--muted);line-height:1.28;text-align:center;max-width:1240px;margin:34px auto 0">
    Slow market time is not your problem. On finished spec homes, it may be the builder's pressure.
  </div>
</div>
{bug()}{source()}
""",
)


# 06. Incentive feed
page(
    "06-incentive-feed",
    f"""
<div class="stage">
  <div class="eyebrow gold">Proof of pressure</div>
  <div class="serif" style="font-size:118px;margin-top:18px">Builders may compete on monthly payment.</div>
  <div class="panel" style="margin-top:58px;padding:56px 64px;display:grid;grid-template-columns:.9fr 1.1fr;gap:54px;align-items:center">
    <div>
      <div class="mini">{INCENTIVE_LABEL}</div>
      <div class="num" style="font-size:184px;color:var(--emerald);line-height:.82;margin-top:18px">56</div>
      <div class="serif" style="font-size:70px;color:var(--ink);line-height:.92">detected Temple incentive cards</div>
    </div>
    <div>
      <div style="display:flex;gap:16px;flex-wrap:wrap">
        <span class="lightpill gold">4.99% language</span>
        <span class="lightpill gold">2.99% language</span>
        <span class="lightpill blue">price reductions</span>
        <span class="lightpill">closing-cost language</span>
      </div>
      <div style="font-size:34px;line-height:1.34;color:#27332f;margin-top:44px">
        The signal is not "free money." The signal is negotiation pressure. Verify the actual terms with the builder and lender.
      </div>
      <div style="margin-top:32px;padding:22px 24px;border-radius:8px;background:rgba(201,91,85,.1);border:1px solid rgba(201,91,85,.28);font-size:25px;line-height:1.32;color:#5b2825">
        Subject to lender terms, buyer qualification, fees, preferred-lender rules, and change.
      </div>
    </div>
  </div>
</div>
{bug()}{source("Source: June 19 builder-incentive feed · detected language, verify terms")}
""",
)


# 07. Model home trap
page(
    "07-model-home-registration",
    f"""
<div class="stage">
  <div class="eyebrow">Before you tour</div>
  <div class="serif" style="font-size:116px;margin-top:18px">Do not walk into the model home alone.</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;margin-top:72px">
    <div class="panel" style="padding:42px">
      <div class="tag">01</div>
      <div class="serif" style="font-size:58px;color:var(--ink);margin-top:28px">Ask first</div>
      <div style="font-size:30px;line-height:1.3;color:#26322e;margin-top:20px">How does buyer-agent registration work on this community?</div>
    </div>
    <div class="panel" style="padding:42px;border-color:rgba(212,168,83,.75)">
      <div class="tag gold">02</div>
      <div class="serif" style="font-size:58px;color:var(--ink);margin-top:28px">Register</div>
      <div style="font-size:30px;line-height:1.3;color:#26322e;margin-top:20px">Document your agent before the tour if the builder requires it.</div>
    </div>
    <div class="panel" style="padding:42px">
      <div class="tag">03</div>
      <div class="serif" style="font-size:58px;color:var(--ink);margin-top:28px">Confirm</div>
      <div style="font-size:30px;line-height:1.3;color:#26322e;margin-top:20px">Get buyer-agent compensation and representation rules in writing.</div>
    </div>
  </div>
  <div class="darkpanel" style="margin-top:42px;padding:34px 42px;display:flex;align-items:center;gap:28px">
    <div class="tag rose">Trap</div>
    <div style="font-size:34px;line-height:1.26;color:var(--snow)">Walking in alone usually does not save money. It usually removes the person negotiating for your side.</div>
  </div>
</div>
{bug()}{source("Builder registration rules vary · confirm in writing before touring")}
""",
)


# 08. Honest scars
page(
    "08-honest-scars",
    f"""
<div class="stage">
  <div class="eyebrow gold">Neutral decision check</div>
  <div class="serif" style="font-size:112px;margin-top:18px">Both sides have scars. Pick the ones you can live with.</div>
  <div class="split" style="margin-top:50px">
    <div class="panel" style="padding:42px">
      <div class="column-title" style="color:var(--emerald)">New construction scars</div>
      <div style="display:grid;gap:24px;margin-top:32px">
        <div class="bullet">13.2% per-square-foot premium in this pull</div>
        <div class="bullet">Possible MUD / PID costs by exact parcel</div>
        <div class="bullet">Incentives often tied to preferred lender terms</div>
        <div class="bullet">Independent inspection still required</div>
      </div>
    </div>
    <div class="panel" style="padding:42px">
      <div class="column-title" style="color:var(--gold)">Resale scars</div>
      <div style="display:grid;gap:24px;margin-top:32px">
        <div class="bullet gold">Older roof, HVAC, plumbing, and foundation risk</div>
        <div class="bullet gold">Repair budget depends on inspection</div>
        <div class="bullet gold">Fewer visible incentive stacks</div>
        <div class="bullet gold">Best homes can still draw competition</div>
      </div>
    </div>
  </div>
  <div style="font-size:35px;color:var(--muted);margin-top:42px;text-align:center">Neither path is the easy button. The right one is the total-payment fit.</div>
</div>
{bug()}{source()}
""",
)


# 09. Decision matrix
page(
    "09-decision-matrix",
    f"""
<div class="stage">
  <div class="eyebrow">Thirty-second decision framework</div>
  <div class="serif" style="font-size:114px;margin-top:18px">Which one fits you?</div>
  <div class="split" style="margin-top:48px">
    <div class="panel" style="padding:40px">
      <div class="column-title" style="color:var(--emerald)">Choose new if...</div>
      <div style="display:grid;gap:18px;margin-top:28px">
        <div class="bullet">You want lower early maintenance</div>
        <div class="bullet">You want a modern layout</div>
        <div class="bullet">Your timeline can handle the builder process</div>
        <div class="bullet"><span><span class="tag rose">Must pass</span>&nbsp;&nbsp;Budget works after any MUD / PID cost</span></div>
        <div class="bullet"><span><span class="tag rose">Must pass</span>&nbsp;&nbsp;Incentive still wins after fees and long-term payment</span></div>
      </div>
    </div>
    <div class="panel" style="padding:40px">
      <div class="column-title" style="color:var(--gold)">Choose resale if...</div>
      <div style="display:grid;gap:18px;margin-top:28px">
        <div class="bullet gold">You want an established street or mature lot</div>
        <div class="bullet gold">You need a shorter closing timeline</div>
        <div class="bullet gold">You want freedom to shop lenders</div>
        <div class="bullet gold">You are comfortable budgeting repairs by inspection</div>
        <div class="bullet gold">The total payment beats the builder deal</div>
      </div>
    </div>
  </div>
</div>
{bug()}{source()}
""",
)


# 10. CTA
page(
    "10-mudcheck-cta",
    f"""
<div class="stage" style="justify-content:center;text-align:center">
  <div class="eyebrow gold">Before you sign</div>
  <div class="serif" style="font-size:150px;margin-top:24px">Comment or DM<br><span class="em">MUDCHECK</span></div>
  <div style="font-size:38px;line-height:1.34;color:var(--muted);max-width:1260px;margin:46px auto 0">
    I will send the checklist for verifying MUD / PID status, what to ask the builder in writing, and how to compare the tax math before you sign.
  </div>
  <div class="panel" style="margin:56px auto 0;padding:28px 42px;width:max-content;max-width:1320px">
    <div class="mini">Full breakdown</div>
    <div class="mono" style="font-size:38px;color:var(--ink);font-weight:700;margin-top:6px">{PAGE_URL}</div>
  </div>
</div>
{bug()}{source("MUD / PID status varies by exact address · verify before contract")}
""",
)


# Transparent lower-thirds / edit helpers
page(
    "LT-data-label",
    f"""
<div class="lower">
  <div class="label">Data source</div>
  <div class="text">{SOURCE_LABEL}</div>
</div>
""",
    transparent=True,
)

page(
    "LT-tax-caveat",
    """
<div class="lower">
  <div class="label">Tax check</div>
  <div class="text">MUD / PID costs vary by parcel. Verify the exact address.</div>
</div>
""",
    transparent=True,
)

page(
    "LT-incentive-caveat",
    """
<div class="lower">
  <div class="label">Incentives</div>
  <div class="text">Detected language only. Terms, fees, qualification, and availability can change.</div>
</div>
""",
    transparent=True,
)

page(
    "LT-agent-registration",
    """
<div class="lower">
  <div class="label">Builder tour</div>
  <div class="text">Register your agent before you tour. Confirm in writing.</div>
</div>
""",
    transparent=True,
)

page(
    "LT-mudcheck",
    """
<div class="lower">
  <div class="label">Checklist</div>
  <div class="text">Comment or DM MUDCHECK for the MUD / PID tax checklist.</div>
</div>
""",
    transparent=True,
)

print(f"Built {len(list(HTMLDIR.glob('*.html')))} HTML files in {HTMLDIR}")
