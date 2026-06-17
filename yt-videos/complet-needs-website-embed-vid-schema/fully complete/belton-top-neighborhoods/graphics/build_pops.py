# Stat-pop callouts — pre-baked, one PNG per stat (transparent, top-right corner).
# Dark-glass token (legible over any b-roll), emerald default / gold for lake luxury.
import os
HERE=os.path.dirname(os.path.abspath(__file__))
HTMLDIR=os.path.join(HERE,"html"); os.makedirs(HTMLDIR,exist_ok=True)

CSS=r"""
@font-face{font-family:'CG';src:url('../fonts/cg700.woff2') format('woff2');font-weight:700;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb500.woff2') format('woff2');font-weight:500;font-display:block}
@font-face{font-family:'JB';src:url('../fonts/jb700.woff2') format('woff2');font-weight:700;font-display:block}
@font-face{font-family:'IN';src:url('../fonts/in600.woff2') format('woff2');font-weight:600;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;background:transparent;overflow:hidden;font-family:'IN',sans-serif}
.anchor{position:absolute;right:128px;top:150px}
.pop{display:inline-flex;align-items:stretch;background:rgba(13,20,36,.90);
 border:1px solid rgba(255,255,255,.14);border-radius:22px;overflow:hidden;
 box-shadow:0 34px 80px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06)}
.bar{width:10px;background:linear-gradient(180deg,#34d399,#059669)}
.pop.gold .bar{background:linear-gradient(180deg,#e3c789,#b9974f)}
.body{padding:32px 46px 30px 38px}
.val{font-family:'JB';font-weight:700;letter-spacing:-.02em;line-height:.92;color:#f8fafc}
.pop.gold .val{color:#fbf3df}
.val .accent{color:#34d399} .pop.gold .val .accent{color:#e3c789}
.cap{font-family:'JB';font-weight:500;font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:#94a3b8;margin-top:16px}
.sub{font-family:'CG';font-weight:700;font-size:34px;color:#34d399;margin-top:6px}
.pop.gold .sub{color:#e3c789}
/* badge variant (ranking flex) */
.pop.badge{background:linear-gradient(135deg,#0f2a20,#0d1424);border-color:rgba(52,211,153,.4)}
.pop.badge .cap{color:#34d399}
.s-xl .val{font-size:128px}
.s-lg .val{font-size:104px}
.s-md .val{font-size:74px}
.s-sm .val{font-size:58px}
"""
HEAD='<!doctype html><html class="transparent"><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'

def pop(fn,val,cap,sub="",gold=False,badge=False,size="lg"):
    cls=" ".join(["pop","gold" if gold else "","badge" if badge else "","s-"+size]).strip()
    subhtml=f'<div class="sub">{sub}</div>' if sub else ""
    body=f'<div class="anchor"><div class="{cls}"><div class="bar"></div><div class="body"><div class="val">{val}</div><div class="cap">{cap}</div>{subhtml}</div></div></div>'
    open(os.path.join(HTMLDIR,fn+".html"),"w").write(HEAD+body+"</body></html>")

# ---- MORGAN'S POINT ----
pop("POP_morgans_median","$247K","Median price","Morgan&rsquo;s Point",size="lg")
pop("POP_morgans_psf","$179","Per sqft",size="xl")
pop("POP_morgans_range","$160K&ndash;$825K","Widest range in the area",size="md")
pop("POP_morgans_sales","36","Sales &middot; last 12 mo",size="xl")
# ---- BELL MEADOWS ----
pop("POP_bell_price","$232&ndash;300K","New from Stylecraft",size="md")
# ---- THREE CREEKS ----
pop("POP_threecreeks_sales","119","Closings",sub="#1 in Belton",badge=True,size="xl")
pop("POP_threecreeks_median","$316K","Median price",size="lg")
pop("POP_threecreeks_psf","$166","Per sqft",size="xl")
pop("POP_threecreeks_range","$215K&ndash;$499K","Price range",size="md")
# ---- DAWSON ----
pop("POP_dawson_sales","29","Sales &middot; last 12 mo",size="xl")
pop("POP_dawson_size","2,280 <span class='accent'>sf</span>","Median size",size="lg")
pop("POP_dawson_psf","$183","Per sqft",size="xl")
pop("POP_dawson_median","$400K","Median price",size="lg")
# ---- LAKE (gold) ----
pop("POP_lake_median","$765K","Median price",gold=True,size="lg")
pop("POP_lake_psf","$248","Per sqft",gold=True,size="xl")
pop("POP_lake_dom","96","Days on market",gold=True,size="xl")

print("pop html written")
