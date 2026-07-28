#!/usr/bin/env python3
"""Generate drop-in Stylecraft review graphics in Taylor's video brand.

Outputs:
  fullframe-4k/  Opaque 3840x2160 cards for B-roll cutaways
  fullframe-1080/ Opaque 1920x1080 cards for the current CapCut timeline
  overlays-4k/   Transparent 3840x2160 lower-thirds
  overlays-1080/ Transparent 1920x1080 lower-thirds
  previews/      JPG previews and a contact sheet

The graphics intentionally use text and original geometric artwork only. Builder
logos are not reproduced.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(
    "/Users/taylordasch_1/claude-social-media-manager/yt-videos/"
    "stylecraft-homes-review/video-graphics-2026-07-26"
)
FULL_4K = ROOT / "fullframe-4k"
FULL_1080 = ROOT / "fullframe-1080"
OVERLAY_4K = ROOT / "overlays-4k"
OVERLAY_1080 = ROOT / "overlays-1080"
PREVIEWS = ROOT / "previews"
for folder in (FULL_4K, FULL_1080, OVERLAY_4K, OVERLAY_1080, PREVIEWS):
    folder.mkdir(parents=True, exist_ok=True)

W, H = 3840, 2160

# Taylor / Living in Temple tokens.
INK = (6, 16, 34, 255)
INK_2 = (8, 34, 51, 255)
MIDNIGHT = (30, 41, 59, 255)
CARD = (20, 42, 61, 246)
CARD_2 = (27, 55, 77, 246)
EMERALD = (5, 150, 105, 255)
EMERALD_BRIGHT = (39, 211, 157, 255)
MINT = (126, 240, 202, 255)
SNOW = (248, 250, 252, 255)
SLATE = (183, 198, 219, 255)
SLATE_2 = (113, 135, 164, 255)
AMBER = (251, 191, 36, 255)
RED = (248, 113, 113, 255)
BLACK_SOFT = (0, 0, 0, 105)

FONT_SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_SANS_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"


CARDS = [
    {
        "slug": "00-title",
        "eyebrow": "LIVING IN TEMPLE  /  BUILDER REVIEW",
        "title": "STYLECRAFT\nHOMES",
        "sub": "Great financing. Good materials. Read the fine print.",
        "kind": "title",
        "source": "Taylor Dasch  •  EG Realty  •  Temple–Belton–Killeen",
        "overlay_title": "STYLECRAFT HOMES REVIEW",
        "overlay_sub": "Great financing. Good materials. Read the fine print.",
    },
    {
        "slug": "G0-verdict-3-9",
        "eyebrow": "THE QUICK ANSWER",
        "title": "3.9 / 5",
        "sub": "Strong enough to recommend. Still inspect the exact house.",
        "kind": "rating",
        "source": "Taylor's editorial verdict  •  Independent; not sponsored",
        "overlay_title": "3.9 / 5  •  STYLECRAFT",
        "overlay_sub": "Strong financing  •  Good materials  •  Execution needs discipline",
    },
    {
        "slug": "G1-offer-choice",
        "eyebrow": "CURRENT STYLECRAFT OFFER",
        "title": "YOU PICK ONE",
        "sub": "Not combinable  •  Select qualifying homes",
        "kind": "choice",
        "left_big": "4.99%",
        "left_label": "30-YEAR FIXED",
        "left_note": "5.691% advertised FHA APR",
        "right_big": "UP TO\n$20,000",
        "right_label": "\"YOUR WAY\" FLEX",
        "right_note": "Closing costs, options or a custom buydown",
        "source": "Close by Aug 10, 2026  •  First-come rate pool  •  Verify current terms",
        "overlay_title": "4.99% FIXED  OR  UP TO $20K",
        "overlay_sub": "Not both  •  Close by Aug 10  •  Verify current availability",
    },
    {
        "slug": "G2-payment-compare",
        "eyebrow": "ILLUSTRATIVE PAYMENT COMPARISON",
        "title": "ABOUT $313 / MONTH",
        "sub": "The rate changes the monthly decision.",
        "kind": "compare",
        "left_big": "$1,690",
        "left_label": "P&I @ 4.99%",
        "left_note": "Official $315,185 loan example",
        "right_big": "$2,003",
        "right_label": "P&I @ 6.55%",
        "right_note": "Same loan; illustrative rate",
        "source": "Principal & interest only  •  Taxes, insurance and MIP are additional",
        "overlay_title": "$1,690  VS  $2,003",
        "overlay_sub": "Illustrative P&I  •  4.99% promo vs 6.55% comparison rate",
    },
    {
        "slug": "G3-five-year-line",
        "eyebrow": "RATE OR FLEX CASH?",
        "title": "JUST OVER 5 YEARS",
        "sub": "Make the lender model both choices on your actual home.",
        "kind": "equation",
        "steps": ["$20,000", "÷  ~$313 / MO", "≈  64 MONTHS"],
        "source": "Rough comparison, not lending advice  •  Selling/refinancing sooner can change the answer",
        "overlay_title": "$20K ÷ ~$313/MO ≈ 64 MONTHS",
        "overlay_sub": "Hold longer: rate may win  •  Exit sooner or cash-tight: flex may win",
    },
    {
        "slug": "G4-kangaroo-string",
        "eyebrow": "THE STRING ATTACHED",
        "title": "THE INCENTIVE REQUIRES\nKANGAROO HOME LENDING",
        "sub": "You may use another lender to buy—but the builder promotion goes away.",
        "kind": "key",
        "big": "REQUIRED",
        "big_label": "AFFILIATED PREFERRED LENDER",
        "source": "Shop one independent quote first  •  Then make the preferred lender earn the business",
        "overlay_title": "INCENTIVES REQUIRE KANGAROO",
        "overlay_sub": "Affiliated preferred lender  •  Outside financing = no builder promotion",
    },
    {
        "slug": "G5-review-snapshot",
        "eyebrow": "OWNER REVIEW SNAPSHOT",
        "title": "PEOPLE LIKE THE HOUSE\nMORE THAN THE PROCESS",
        "sub": "The split matters more than one blended score.",
        "kind": "metrics",
        "metrics": [
            ("4.5 / 5", "ELIANT", "1,000+ owners"),
            ("4.6", "WOULD REFER", "Owner survey"),
            ("3.9", "PURCHASE EXPERIENCE", "Owner survey"),
            ("A+", "BBB", "Accredited since 1996"),
        ],
        "source": "Eliant + BBB snapshot verified July 22, 2026  •  Read Texas-builder reviews only",
        "overlay_title": "4.5 OVERALL  •  4.6 REFER  •  3.9 PROCESS",
        "overlay_sub": "Eliant, 1,000+ owners  •  BBB A+ since 1996",
    },
    {
        "slug": "G6-complaint-record",
        "eyebrow": "FROM THE PUBLIC COMPLAINT RECORD",
        "title": "REPEATING ISSUES TO CHECK",
        "sub": "Not every home—and not Taylor's personal buyers—but documented often enough to inspect.",
        "kind": "bullets",
        "bullets": [
            "GRADING / DRAINAGE",
            "EARLY PLUMBING FAILURES",
            "LVP FLOORING LIFT",
        ],
        "source": "Complaint-record summary  •  Verify the exact home with independent inspections",
        "overlay_title": "PUBLIC COMPLAINT RECORD",
        "overlay_sub": "Grading/drainage  •  Early plumbing failures  •  LVP lift",
    },
    {
        "slug": "G7-warranty-timeline",
        "eyebrow": "STYLECRAFT WARRANTY",
        "title": "1  /  2  /  10",
        "sub": "The first deadline is the one buyers miss.",
        "kind": "timeline",
        "timeline": [
            ("1 YEAR", "WORKMANSHIP", EMERALD_BRIGHT),
            ("2 YEARS", "SYSTEMS", MINT),
            ("10 YEARS", "STRUCTURE", SLATE),
        ],
        "source": "DAY 365: workmanship coverage ends  •  Submit documented items before the cutoff",
        "overlay_title": "1-YEAR  /  2-YEAR  /  10-YEAR",
        "overlay_sub": "Workmanship  •  Systems  •  Structure  |  Day 365 is the hard first cutoff",
    },
    {
        "slug": "G8-month-eleven",
        "eyebrow": "THE MONTH-11 MOVE",
        "title": "INDEPENDENT INSPECTION",
        "sub": "Look before the workmanship door closes.",
        "kind": "checklist",
        "big": "$400–$500",
        "checklist": [
            "Book around month 11",
            "Document every finding",
            "Submit the list in writing before Day 365",
        ],
        "source": "Most of Taylor's Stylecraft inspections have come back clean  •  The value is deadline protection",
        "overlay_title": "MONTH 11  →  INDEPENDENT INSPECTION",
        "overlay_sub": "$400–$500  •  Submit every documented item before Day 365",
    },
    {
        "slug": "G9-contract-review",
        "eyebrow": "BEFORE YOU SIGN BUILDER PAPER",
        "title": "5 TERMS TO REVIEW",
        "sub": "Get the exact contract—not the sales-floor summary.",
        "kind": "numbered",
        "bullets": [
            "INSPECTION + TERMINATION RIGHTS",
            "MATERIAL-SUBSTITUTION RIGHTS",
            "CLOSING-DATE + TIMING RISK",
            "EARNEST-MONEY REFUND TERMS",
            "INCENTIVE + LENDER REQUIREMENTS",
        ],
        "source": "Contract language controls  •  Have your agent and appropriate professionals review the current form",
        "overlay_title": "5 BUILDER-CONTRACT TERMS TO REVIEW",
        "overlay_sub": "Inspection rights  •  Substitutions  •  Closing date  •  Deposits  •  Incentives",
    },
    {
        "slug": "G10-comparison-lanes",
        "eyebrow": "HOW STYLECRAFT FITS THE FIELD",
        "title": "THREE DIFFERENT BUYER LANES",
        "sub": "Don't compare builders on sticker price alone.",
        "kind": "lanes",
        "lanes": [
            ("TOTAL PAYMENT", "SAME-DAY LOAN ESTIMATES", "APR, fees and cash to close"),
            ("SPECS + CRAFT", "EXACT INVENTORY HOMES", "Finish, lot and inspection"),
            ("RISK + FIT", "CONTRACT / TAX / TIMELINE", "Score the buyer decision"),
        ],
        "source": "Offers rotate  •  Compare APR, cash to close, payment, contract and inspection history",
        "overlay_title": "COMPARE THE LANE—NOT JUST THE LOGO",
        "overlay_sub": "Total payment  •  Specs and craft  •  Contract, tax and timeline",
    },
    {
        "slug": "G11-total-payment",
        "eyebrow": "THE REAL MONTHLY PAYMENT",
        "title": "P&I IS ONLY THE START",
        "sub": "Underwrite the completed home—not the temporary lot assessment.",
        "kind": "bullets",
        "bullets": [
            "PRINCIPAL + INTEREST",
            "TAXES + DISTRICT CHARGES",
            "INSURANCE + MIP + HOA",
        ],
        "source": "Use the Loan Estimate and exact tax record  •  The first incomplete assessment can understate later escrow",
        "overlay_title": "PRICE THE FULL MONTHLY PAYMENT",
        "overlay_sub": "P&I  •  Taxes and districts  •  Insurance, MIP and HOA",
    },
    {
        "slug": "G12-registration-card",
        "eyebrow": "PROTECT YOUR REPRESENTATION",
        "title": "BRING YOUR AGENT\nTO THE FIRST VISIT",
        "sub": "Don't sign the builder's registration card before your agent is on record.",
        "kind": "warning",
        "source": "Builder registration policies vary  •  Get your representation documented before touring",
        "overlay_title": "DON'T REGISTER ALONE",
        "overlay_sub": "Have your agent on record before your first model-home visit",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def visual_bbox(f, text):
    box = f.getbbox(text)
    return box, box[2] - box[0], box[3] - box[1]


def draw_top_text(draw, xy, text, f, fill, anchor="la", spacing=12):
    draw.multiline_text(xy, text, font=f, fill=fill, anchor=anchor, spacing=spacing)


def fit_font(text, path, max_size, min_size, max_width, multiline=False):
    for size in range(max_size, min_size - 1, -4):
        f = font(path, size)
        if multiline:
            box = f.getbbox(max(text.splitlines(), key=len))
        else:
            box = f.getbbox(text)
        if box[2] - box[0] <= max_width:
            return f
    return font(path, min_size)


def rounded_shadow(canvas, box, radius=46, blur=38, offset=(0, 24), alpha=140):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    ox, oy = offset
    d.rounded_rectangle(
        (x0 + ox, y0 + oy, x1 + ox, y1 + oy),
        radius=radius,
        fill=(0, 0, 0, alpha),
    )
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def rounded_card(canvas, box, fill=CARD, outline=(45, 78, 104, 255), width=3, radius=44):
    rounded_shadow(canvas, box, radius)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient_background():
    im = Image.new("RGBA", (W, H), INK)
    pix = im.load()
    for x in range(W):
        t = x / (W - 1)
        r = round(INK[0] * (1 - t) + INK_2[0] * t)
        g = round(INK[1] * (1 - t) + INK_2[1] * t)
        b = round(INK[2] * (1 - t) + INK_2[2] * t)
        for y in range(H):
            v = 1.0 - 0.11 * (y / H)
            pix[x, y] = (round(r * v), round(g * v), round(b * v), 255)
    d = ImageDraw.Draw(im)
    # Restrained technical grid.
    for x in range(220, W, 320):
        d.line((x, 160, x, H - 140), fill=(62, 103, 125, 25), width=2)
    for y in range(220, H, 240):
        d.line((120, y, W - 120, y), fill=(62, 103, 125, 22), width=2)
    # Original house-line motif.
    x0, y0 = 2770, 300
    d.line((x0, y0 + 300, x0 + 360, y0, x0 + 720, y0 + 300), fill=(39, 211, 157, 42), width=18)
    d.line((x0 + 100, y0 + 255, x0 + 100, y0 + 620, x0 + 620, y0 + 620, x0 + 620, y0 + 255),
           fill=(39, 211, 157, 32), width=12)
    return im


def brand_header(canvas, eyebrow):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((190, 144, 222, 176), radius=8, fill=EMERALD_BRIGHT)
    f = font(FONT_SANS_BOLD, 46)
    d.text((254, 160), eyebrow, font=f, fill=EMERALD_BRIGHT, anchor="lm")
    f2 = font(FONT_SANS_BOLD, 36)
    d.text((3650, 160), "TAYLOR DASCH  •  EG REALTY", font=f2, fill=SLATE, anchor="rm")


def source_footer(canvas, source):
    d = ImageDraw.Draw(canvas)
    d.line((190, H - 170, W - 190, H - 170), fill=(63, 100, 126, 120), width=3)
    f = fit_font(source, FONT_SANS, 35, 27, W - 380)
    d.text((190, H - 106), source, font=f, fill=SLATE_2, anchor="lm")
    d.text((W - 190, H - 106), "templetxhomes.net", font=font(FONT_SANS_BOLD, 34),
           fill=EMERALD_BRIGHT, anchor="rm")


def title_block(canvas, card, top=320, max_width=3220):
    d = ImageDraw.Draw(canvas)
    title = card["title"]
    f_title = fit_font(title, FONT_SERIF_BOLD, 188, 110, max_width, multiline=True)
    d.multiline_text((190, top), title, font=f_title, fill=SNOW, anchor="la", spacing=10)
    bbox = d.multiline_textbbox((190, top), title, font=f_title, anchor="la", spacing=10)
    sub_y = bbox[3] + 42
    f_sub = fit_font(card.get("sub", ""), FONT_SANS_BOLD, 58, 38, max_width)
    d.text((190, sub_y), card.get("sub", ""), font=f_sub, fill=SLATE, anchor="la")
    return bbox, sub_y


def pill(draw, box, text, fill=EMERALD, color=SNOW, f=None):
    if f is None:
        f = font(FONT_SANS_BLACK, 42)
    draw.rounded_rectangle(box, radius=24, fill=fill)
    draw.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), text,
              font=f, fill=color, anchor="mm")


def draw_choice_or_compare(canvas, card, y0, compare=False):
    d = ImageDraw.Draw(canvas)
    left = (190, y0, 1755, y0 + 690)
    right = (2085, y0, 3650, y0 + 690)
    rounded_card(canvas, left, fill=CARD)
    rounded_card(canvas, right, fill=CARD_2)
    d = ImageDraw.Draw(canvas)
    f_big_l = fit_font(card["left_big"], FONT_SANS_BLACK, 168, 94, left[2] - left[0] - 150, True)
    f_big_r = fit_font(card["right_big"], FONT_SANS_BLACK, 168, 86, right[2] - right[0] - 150, True)
    d.multiline_text(((left[0] + left[2]) / 2, left[1] + 185), card["left_big"],
                     font=f_big_l, fill=EMERALD_BRIGHT, anchor="mm", align="center", spacing=0)
    d.multiline_text(((right[0] + right[2]) / 2, right[1] + 185), card["right_big"],
                     font=f_big_r, fill=SNOW if compare else AMBER, anchor="mm", align="center", spacing=0)
    label_f = fit_font(card["left_label"], FONT_SANS_BLACK, 54, 38, 1350)
    note_f = fit_font(card["left_note"], FONT_SANS_BOLD, 42, 30, 1350)
    d.text(((left[0] + left[2]) / 2, left[1] + 390), card["left_label"],
           font=label_f, fill=SNOW, anchor="mm")
    d.text(((left[0] + left[2]) / 2, left[1] + 495), card["left_note"],
           font=note_f, fill=SLATE, anchor="mm")
    label_f2 = fit_font(card["right_label"], FONT_SANS_BLACK, 54, 38, 1350)
    note_f2 = fit_font(card["right_note"], FONT_SANS_BOLD, 42, 30, 1350)
    d.text(((right[0] + right[2]) / 2, right[1] + 390), card["right_label"],
           font=label_f2, fill=SNOW, anchor="mm")
    d.text(((right[0] + right[2]) / 2, right[1] + 495), card["right_note"],
           font=note_f2, fill=SLATE, anchor="mm")
    circle = (1842, y0 + 265, 1998, y0 + 421)
    d.ellipse(circle, fill=INK, outline=EMERALD_BRIGHT, width=5)
    d.text((1920, y0 + 343), "VS" if compare else "OR",
           font=font(FONT_SANS_BLACK, 42), fill=SNOW, anchor="mm")
    if not compare:
        pill(d, (1350, y0 + 590, 2490, y0 + 672), "NOT COMBINABLE",
             fill=EMERALD, f=font(FONT_SANS_BLACK, 38))


def draw_rating(canvas, y0):
    d = ImageDraw.Draw(canvas)
    d.text((190, y0), "3.9", font=font(FONT_SANS_BLACK, 360),
           fill=EMERALD_BRIGHT, anchor="la")
    d.text((1120, y0 + 180), "/ 5", font=font(FONT_SERIF_BOLD, 152),
           fill=SNOW, anchor="lm")
    x0, y = 1950, y0 + 110
    seg_w, gap = 280, 28
    for idx in range(5):
        x = x0 + idx * (seg_w + gap)
        fill = EMERALD_BRIGHT if idx < 3 else MIDNIGHT
        d.rounded_rectangle((x, y, x + seg_w, y + 128), radius=28,
                            fill=fill, outline=(68, 102, 127, 255), width=4)
        if idx == 3:
            partial_w = round(seg_w * 0.9)
            d.rounded_rectangle((x, y, x + partial_w, y + 128), radius=28,
                                fill=EMERALD_BRIGHT)
            d.rectangle((x + partial_w - 28, y, x + partial_w, y + 128),
                        fill=EMERALD_BRIGHT)
    d.text((1950, y + 220), "FINANCING", font=font(FONT_SANS_BLACK, 50),
           fill=SNOW, anchor="la")
    d.text((1950, y + 300), "BUILD MATERIALS", font=font(FONT_SANS_BLACK, 50),
           fill=SNOW, anchor="la")
    d.text((1950, y + 380), "EXECUTION + WARRANTY", font=font(FONT_SANS_BLACK, 50),
           fill=SLATE, anchor="la")


def draw_equation(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    boxes = [(190, y0, 1150, y0 + 470), (1438, y0, 2402, y0 + 470), (2690, y0, 3650, y0 + 470)]
    colors = [SNOW, SLATE, EMERALD_BRIGHT]
    for idx, (box, step, color) in enumerate(zip(boxes, card["steps"], colors)):
        rounded_card(canvas, box, fill=CARD if idx != 2 else CARD_2)
        f = fit_font(step, FONT_SANS_BLACK, 102, 62, box[2] - box[0] - 90)
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), step,
               font=f, fill=color, anchor="mm")
        if idx < 2:
            d.text((box[2] + 144, (box[1] + box[3]) / 2), "→",
                   font=font(FONT_SANS_BLACK, 92), fill=EMERALD_BRIGHT, anchor="mm")
    pill(d, (1210, y0 + 545, 2630, y0 + 655), "ABOUT 5 YEARS 4 MONTHS",
         fill=EMERALD, f=font(FONT_SANS_BLACK, 46))


def draw_key(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    box = (190, y0, 3650, y0 + 610)
    rounded_card(canvas, box, fill=CARD)
    accent = (250, y0 + 80, 960, y0 + 530)
    d.rounded_rectangle(accent, radius=36, fill=(6, 92, 74, 255),
                        outline=EMERALD_BRIGHT, width=4)
    f_big = fit_font(card["big"], FONT_SANS_BLACK, 168, 74, 610, True)
    d.multiline_text(((accent[0] + accent[2]) / 2, accent[1] + 145), card["big"],
                     font=f_big, fill=EMERALD_BRIGHT, anchor="mm", align="center")
    f_label = fit_font(card["big_label"], FONT_SANS_BOLD, 42, 28, 620, True)
    d.multiline_text(((accent[0] + accent[2]) / 2, accent[1] + 325), card["big_label"],
                     font=f_label, fill=SNOW, anchor="mm", align="center", spacing=6)
    title = card["title"]
    f = fit_font(title, FONT_SERIF_BOLD, 108, 66, 2400, True)
    d.multiline_text((1120, y0 + 105), title, font=f, fill=SNOW,
                     anchor="la", spacing=8)
    bb = d.multiline_textbbox((1120, y0 + 105), title, font=f, anchor="la", spacing=8)
    f_sub = fit_font(card["sub"], FONT_SANS_BOLD, 46, 32, 2350)
    d.text((1120, bb[3] + 46), card["sub"], font=f_sub, fill=SLATE, anchor="la")


def draw_metrics(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    gap = 34
    total_w = 3460
    box_w = (total_w - gap * 3) // 4
    for idx, (metric, label, note) in enumerate(card["metrics"]):
        x0 = 190 + idx * (box_w + gap)
        box = (x0, y0, x0 + box_w, y0 + 520)
        rounded_card(canvas, box, fill=CARD if idx != 2 else CARD_2)
        metric_f = fit_font(metric, FONT_SANS_BLACK, 112, 66, box_w - 80)
        d.text(((box[0] + box[2]) / 2, y0 + 150), metric,
               font=metric_f, fill=EMERALD_BRIGHT if idx != 2 else AMBER, anchor="mm")
        label_f = fit_font(label, FONT_SANS_BLACK, 44, 28, box_w - 70)
        d.text(((box[0] + box[2]) / 2, y0 + 300), label,
               font=label_f, fill=SNOW, anchor="mm")
        note_f = fit_font(note, FONT_SANS_BOLD, 34, 24, box_w - 70)
        d.text(((box[0] + box[2]) / 2, y0 + 402), note,
               font=note_f, fill=SLATE, anchor="mm")


def draw_bullets(canvas, card, y0, numbered=False):
    d = ImageDraw.Draw(canvas)
    bullets = card["bullets"]
    if numbered:
        cols = 2
        box_w = 1675
        box_h = 210
        gap_x = 110
        gap_y = 34
        for idx, item in enumerate(bullets):
            col = idx % cols
            row = idx // cols
            x0 = 190 + col * (box_w + gap_x)
            yy = y0 + row * (box_h + gap_y)
            box = (x0, yy, x0 + box_w, yy + box_h)
            rounded_card(canvas, box, fill=CARD, radius=34)
            d.ellipse((x0 + 42, yy + 52, x0 + 146, yy + 156), fill=EMERALD)
            d.text((x0 + 94, yy + 104), str(idx + 1), font=font(FONT_SANS_BLACK, 42),
                   fill=SNOW, anchor="mm")
            f = fit_font(item, FONT_SANS_BLACK, 44, 30, box_w - 230)
            d.text((x0 + 190, yy + 105), item, font=f, fill=SNOW, anchor="lm")
    else:
        box_w = 1060
        gap = 140
        for idx, item in enumerate(bullets):
            x0 = 190 + idx * (box_w + gap)
            box = (x0, y0, x0 + box_w, y0 + 470)
            rounded_card(canvas, box, fill=CARD if idx != 1 else CARD_2)
            d.text((x0 + 80, y0 + 100), f"0{idx + 1}", font=font(FONT_SANS_BLACK, 62),
                   fill=EMERALD_BRIGHT, anchor="la")
            f = fit_font(item, FONT_SANS_BLACK, 54, 34, box_w - 160, True)
            d.multiline_text((x0 + 80, y0 + 230), item.replace(" / ", "\n"),
                             font=f, fill=SNOW, anchor="lm", spacing=8)


def draw_timeline(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    start_x, end_x = 300, 3540
    line_y = y0 + 280
    d.line((start_x, line_y, end_x, line_y), fill=(68, 105, 132, 255), width=18)
    positions = [start_x + 150, 1640, end_x - 150]
    for idx, ((years, label, color), x) in enumerate(zip(card["timeline"], positions)):
        d.ellipse((x - 54, line_y - 54, x + 54, line_y + 54),
                  fill=color, outline=INK, width=10)
        d.text((x, line_y - 130), years, font=font(FONT_SANS_BLACK, 62),
               fill=color, anchor="ms")
        d.text((x, line_y + 150), label, font=font(FONT_SANS_BLACK, 42),
               fill=SNOW, anchor="mm")
    marker_x = positions[0]
    d.line((marker_x, line_y - 78, marker_x, line_y + 185), fill=RED, width=10)
    pill(d, (marker_x - 270, line_y + 245, marker_x + 270, line_y + 340),
         "DAY 365 CUTOFF", fill=(148, 51, 62, 255), f=font(FONT_SANS_BLACK, 34))


def draw_checklist(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    big_box = (190, y0, 1420, y0 + 590)
    rounded_card(canvas, big_box, fill=CARD_2)
    f_big = fit_font(card["big"], FONT_SANS_BLACK, 170, 100, 1050)
    d.text(((big_box[0] + big_box[2]) / 2, y0 + 205), card["big"],
           font=f_big, fill=EMERALD_BRIGHT, anchor="mm")
    d.text(((big_box[0] + big_box[2]) / 2, y0 + 390), "TYPICAL INSPECTION RANGE",
           font=font(FONT_SANS_BLACK, 38), fill=SNOW, anchor="mm")
    list_box = (1510, y0, 3650, y0 + 590)
    rounded_card(canvas, list_box, fill=CARD)
    for idx, item in enumerate(card["checklist"]):
        yy = y0 + 115 + idx * 150
        d.rounded_rectangle((1580, yy - 36, 1660, yy + 44), radius=18,
                            fill=EMERALD)
        d.line((1602, yy + 2, 1622, yy + 22, 1645, yy - 16),
               fill=SNOW, width=10, joint="curve")
        f = fit_font(item, FONT_SANS_BOLD, 48, 32, 1850)
        d.text((1710, yy + 4), item, font=f, fill=SNOW, anchor="lm")


def draw_lanes(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    gap = 36
    box_w = (3460 - gap * 2) // 3
    for idx, (label, builders, note) in enumerate(card["lanes"]):
        x0 = 190 + idx * (box_w + gap)
        box = (x0, y0, x0 + box_w, y0 + 610)
        rounded_card(canvas, box, fill=CARD if idx != 1 else CARD_2)
        pill(d, (x0 + 60, y0 + 62, x0 + box_w - 60, y0 + 154), label,
             fill=EMERALD if idx == 0 else MIDNIGHT,
             f=fit_font(label, FONT_SANS_BLACK, 38, 26, box_w - 160))
        builders_f = fit_font(builders, FONT_SERIF_BOLD, 66, 42, box_w - 120, True)
        d.multiline_text((x0 + box_w / 2, y0 + 315), builders.replace(" / ", "\n"),
                         font=builders_f, fill=SNOW, anchor="mm", align="center", spacing=8)
        note_f = fit_font(note, FONT_SANS_BOLD, 36, 28, box_w - 130)
        d.text((x0 + box_w / 2, y0 + 515), note, font=note_f, fill=SLATE, anchor="mm")


def draw_warning(canvas, card, y0):
    d = ImageDraw.Draw(canvas)
    box = (190, y0, 3650, y0 + 670)
    rounded_card(canvas, box, fill=CARD)
    d.rounded_rectangle((255, y0 + 75, 750, y0 + 595), radius=44,
                        fill=(4, 95, 76, 255), outline=EMERALD_BRIGHT, width=5)
    # Original person + document pictogram.
    d.ellipse((390, y0 + 150, 610, y0 + 370), fill=EMERALD_BRIGHT)
    d.rounded_rectangle((330, y0 + 390, 670, y0 + 520), radius=56, fill=EMERALD_BRIGHT)
    d.rectangle((565, y0 + 335, 690, y0 + 500), fill=SNOW)
    d.line((592, y0 + 380, 663, y0 + 380), fill=INK, width=10)
    d.line((592, y0 + 420, 663, y0 + 420), fill=INK, width=10)
    f = fit_font(card["title"], FONT_SERIF_BOLD, 126, 74, 2650, True)
    d.multiline_text((900, y0 + 130), card["title"], font=f, fill=SNOW,
                     anchor="la", spacing=4)
    bb = d.multiline_textbbox((900, y0 + 130), card["title"], font=f, anchor="la", spacing=4)
    f_sub = fit_font(card["sub"], FONT_SANS_BOLD, 46, 30, 2600)
    d.text((900, bb[3] + 42), card["sub"], font=f_sub, fill=SLATE, anchor="la")


def render_fullframe(card):
    canvas = gradient_background()
    brand_header(canvas, card["eyebrow"])
    kind = card["kind"]
    if kind == "title":
        d = ImageDraw.Draw(canvas)
        f = fit_font(card["title"], FONT_SERIF_BOLD, 270, 170, 2380, True)
        d.multiline_text((190, 520), card["title"], font=f, fill=SNOW,
                         anchor="la", spacing=0)
        bb = d.multiline_textbbox((190, 520), card["title"], font=f, anchor="la", spacing=0)
        d.rectangle((190, bb[3] + 80, 480, bb[3] + 94), fill=EMERALD_BRIGHT)
        fsub = fit_font(card["sub"], FONT_SANS_BOLD, 64, 44, 2500)
        d.text((190, bb[3] + 170), card["sub"], font=fsub, fill=SLATE, anchor="la")
        pill(d, (190, 1580, 1160, 1700), "3.9 / 5 VERDICT", fill=EMERALD,
             f=font(FONT_SANS_BLACK, 48))
    else:
        title_block(canvas, card, top=300, max_width=3400)
        y0 = 1110
        if kind == "rating":
            draw_rating(canvas, y0)
        elif kind == "choice":
            draw_choice_or_compare(canvas, card, y0, compare=False)
        elif kind == "compare":
            draw_choice_or_compare(canvas, card, y0, compare=True)
        elif kind == "equation":
            draw_equation(canvas, card, y0)
        elif kind == "key":
            # Key cards carry their title inside the body to create contrast.
            canvas = gradient_background()
            brand_header(canvas, card["eyebrow"])
            draw_key(canvas, card, 500)
        elif kind == "metrics":
            draw_metrics(canvas, card, y0)
        elif kind == "bullets":
            draw_bullets(canvas, card, y0, numbered=False)
        elif kind == "timeline":
            draw_timeline(canvas, card, y0)
        elif kind == "checklist":
            draw_checklist(canvas, card, y0)
        elif kind == "numbered":
            draw_bullets(canvas, card, y0, numbered=True)
        elif kind == "lanes":
            draw_lanes(canvas, card, y0)
        elif kind == "warning":
            canvas = gradient_background()
            brand_header(canvas, card["eyebrow"])
            draw_warning(canvas, card, 570)
    source_footer(canvas, card["source"])
    return canvas


def render_overlay(card):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    title = card["overlay_title"]
    sub = card["overlay_sub"]
    # Taller card only when the simplified text still needs two lines.
    box = (170, 1480, 3500, 2040)
    rounded_card(canvas, box, fill=(16, 34, 52, 248), outline=(42, 86, 110, 255), width=4)
    d.rounded_rectangle((box[0], box[1], box[0] + 26, box[3]), radius=13,
                        fill=EMERALD_BRIGHT)
    pill_f = font(FONT_SANS_BLACK, 34)
    pill_w = min(1040, max(650, 30 * len(card["eyebrow"]) + 110))
    pill(d, (245, 1540, 245 + pill_w, 1630), card["eyebrow"],
         fill=EMERALD, f=pill_f)
    title_f = fit_font(title, FONT_SANS_BLACK, 72, 48, 3050)
    d.text((245, 1745), title, font=title_f, fill=SNOW, anchor="lm")
    sub_f = fit_font(sub, FONT_SANS_BOLD, 42, 29, 3050)
    d.text((245, 1885), sub, font=sub_f, fill=SLATE, anchor="lm")
    d.text((3415, 1990), "LIVING IN TEMPLE", font=font(FONT_SANS_BOLD, 30),
           fill=EMERALD_BRIGHT, anchor="rs")
    return canvas


def save_pair(image, folder_4k, folder_1080, filename):
    image.save(folder_4k / filename)
    image.resize((1920, 1080), Image.Resampling.LANCZOS).save(folder_1080 / filename)


def main():
    preview_images = []
    for card in CARDS:
        filename = f"{card['slug']}.png"
        full = render_fullframe(card)
        overlay = render_overlay(card)
        save_pair(full, FULL_4K, FULL_1080, filename)
        save_pair(overlay, OVERLAY_4K, OVERLAY_1080, filename)
        preview = full.resize((960, 540), Image.Resampling.LANCZOS).convert("RGB")
        preview_path = PREVIEWS / f"{card['slug']}-preview.jpg"
        preview.save(preview_path, quality=92)
        # Keep the original G0 filename as a 3.9 compatibility alias so an
        # existing CapCut import does not break when the editorial score changes.
        if card["slug"] == "G0-verdict-3-9":
            save_pair(full, FULL_4K, FULL_1080, "G0-verdict-3-5.png")
            save_pair(overlay, OVERLAY_4K, OVERLAY_1080, "G0-verdict-3-5.png")
            preview.save(PREVIEWS / "G0-verdict-3-5-preview.jpg", quality=92)
        preview_images.append((card["slug"], preview))

    thumb_w, thumb_h = 720, 405
    cols = 3
    rows = (len(preview_images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + 54)), (8, 17, 31))
    d = ImageDraw.Draw(sheet)
    label_f = font(FONT_SANS_BOLD, 24)
    for idx, (slug, preview) in enumerate(preview_images):
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + 54)
        sheet.paste(preview.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS), (x, y))
        d.text((x + 18, y + thumb_h + 27), slug, font=label_f,
               fill=(215, 226, 239), anchor="lm")
    sheet.save(PREVIEWS / "stylecraft-graphics-contact-sheet.jpg", quality=92)
    print(f"Generated {len(CARDS)} full-frame cards and {len(CARDS)} overlays in {ROOT}")


if __name__ == "__main__":
    main()
