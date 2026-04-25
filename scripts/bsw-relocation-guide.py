#!/usr/bin/env python3
"""BSW Temple Relocation Guide — 6-page branded PDF lead magnet."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

# ─── Brand Colors ───
MIDNIGHT = HexColor("#1e293b")
DEEP = HexColor("#0f172a")
EMERALD = HexColor("#059669")
EMERALD_DARK = HexColor("#047857")
EMERALD_LIGHT = HexColor("#10b981")
SNOW = HexColor("#f8fafc")
CREAM = HexColor("#e2e8f0")
SLATE = HexColor("#94a3b8")
CARD_BG = HexColor("#1a2d42")
CARD_BORDER = HexColor("#2d4a6b")
WHITE = HexColor("#ffffff")
BLACK = HexColor("#000000")
LIGHT_EMERALD_BG = HexColor("#f0fdf4")
EMERALD_BORDER = HexColor("#bbf7d0")
SOFT_BG = HexColor("#f8fafc")
TABLE_HEADER_BG = HexColor("#059669")
TABLE_ALT_ROW = HexColor("#f0fdf4")
TABLE_BORDER = HexColor("#d1d5db")
DARK_TEXT = HexColor("#1e293b")
BODY_TEXT = HexColor("#334155")
MUTED_TEXT = HexColor("#64748b")
AMBER = HexColor("#d97706")
AMBER_BG = HexColor("#fffbeb")
AMBER_BORDER = HexColor("#fde68a")

# ─── Page Setup ───
PAGE_W, PAGE_H = letter
MARGIN = 0.65 * inch

# ─── Styles ───
def make_styles():
    s = {}
    s['title'] = ParagraphStyle(
        'Title', fontName='Helvetica-Bold', fontSize=26, leading=30,
        textColor=MIDNIGHT, alignment=TA_LEFT, spaceAfter=4
    )
    s['subtitle'] = ParagraphStyle(
        'Subtitle', fontName='Helvetica', fontSize=12, leading=16,
        textColor=EMERALD_DARK, spaceAfter=16
    )
    s['h1'] = ParagraphStyle(
        'H1', fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=MIDNIGHT, spaceBefore=6, spaceAfter=8
    )
    s['h2'] = ParagraphStyle(
        'H2', fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=MIDNIGHT, spaceBefore=12, spaceAfter=6
    )
    s['h3'] = ParagraphStyle(
        'H3', fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=EMERALD_DARK, spaceBefore=8, spaceAfter=4
    )
    s['body'] = ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=BODY_TEXT, spaceAfter=6
    )
    s['body_small'] = ParagraphStyle(
        'BodySmall', fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=BODY_TEXT, spaceAfter=4
    )
    s['label'] = ParagraphStyle(
        'Label', fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=EMERALD, spaceAfter=2
    )
    s['callout'] = ParagraphStyle(
        'Callout', fontName='Helvetica-Oblique', fontSize=9.5, leading=14,
        textColor=EMERALD_DARK, spaceAfter=8, leftIndent=12, rightIndent=12
    )
    s['footer'] = ParagraphStyle(
        'Footer', fontName='Helvetica', fontSize=7, leading=9,
        textColor=MUTED_TEXT, alignment=TA_CENTER
    )
    s['table_header'] = ParagraphStyle(
        'TableHeader', fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=WHITE
    )
    s['table_cell'] = ParagraphStyle(
        'TableCell', fontName='Helvetica', fontSize=8, leading=11,
        textColor=DARK_TEXT
    )
    s['table_cell_bold'] = ParagraphStyle(
        'TableCellBold', fontName='Helvetica-Bold', fontSize=8, leading=11,
        textColor=DARK_TEXT
    )
    s['bullet'] = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=BODY_TEXT, spaceAfter=3, leftIndent=18, bulletIndent=6,
        bulletFontName='Helvetica', bulletFontSize=9.5
    )
    s['contact_name'] = ParagraphStyle(
        'ContactName', fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=MIDNIGHT, spaceAfter=2
    )
    s['contact_role'] = ParagraphStyle(
        'ContactRole', fontName='Helvetica', fontSize=10, leading=14,
        textColor=EMERALD_DARK, spaceAfter=8
    )
    return s

# ─── Helper: Emerald divider ───
def emerald_divider():
    return HRFlowable(
        width="100%", thickness=2, color=EMERALD,
        spaceBefore=8, spaceAfter=8
    )

def thin_divider():
    return HRFlowable(
        width="100%", thickness=0.5, color=TABLE_BORDER,
        spaceBefore=6, spaceAfter=6
    )

# ─── Helper: Callout box ───
def callout_box(text, styles, bg=LIGHT_EMERALD_BG, border=EMERALD_BORDER):
    p = Paragraph(text, styles['callout'])
    t = Table([[p]], colWidths=[PAGE_W - 2*MARGIN - 24])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1, border),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

# ─── Helper: Section label ───
def section_label(text, styles):
    return Paragraph(text.upper(), styles['label'])

# ─── Page background + footer ───
class PDFTemplate:
    def __init__(self):
        self.page_num = 0

    def on_page(self, canvas_obj, doc):
        self.page_num += 1
        canvas_obj.saveState()
        # Top emerald bar
        canvas_obj.setFillColor(EMERALD)
        canvas_obj.rect(0, PAGE_H - 4, PAGE_W, 4, fill=1, stroke=0)
        # Footer
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.setFillColor(MUTED_TEXT)
        canvas_obj.drawString(MARGIN, 22,
            "Taylor Dasch | EG Realty | 254-718-4249 | dealswithdasch@gmail.com | templetxhomes.net")
        canvas_obj.drawRightString(PAGE_W - MARGIN, 22, f"Page {self.page_num}")
        # Bottom emerald line
        canvas_obj.setStrokeColor(EMERALD)
        canvas_obj.setLineWidth(1)
        canvas_obj.line(MARGIN, 34, PAGE_W - MARGIN, 34)
        canvas_obj.restoreState()

    def on_first_page(self, canvas_obj, doc):
        self.page_num += 1
        canvas_obj.saveState()
        # Top emerald bar (thicker on cover)
        canvas_obj.setFillColor(EMERALD)
        canvas_obj.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
        # Footer
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.setFillColor(MUTED_TEXT)
        canvas_obj.drawCentredString(PAGE_W/2, 22,
            "Taylor Dasch | EG Realty | templetxhomes.net | 254-718-4249")
        canvas_obj.restoreState()


def build_pdf(output_path):
    styles = make_styles()
    tmpl = PDFTemplate()
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 8, bottomMargin=MARGIN + 20
    )
    story = []
    usable_w = PAGE_W - 2*MARGIN

    # ════════════════════════════════════════════
    # PAGE 1: COVER + WELCOME TIMELINE
    # ════════════════════════════════════════════
    story.append(Spacer(1, 40))
    story.append(section_label("BSW Relocation Guide", styles))
    story.append(Paragraph(
        "BSW Temple<br/>Relocation Guide",
        styles['title']
    ))
    story.append(Paragraph(
        "Neighborhoods, Commute Times &amp; Physician Loan Calculator",
        styles['subtitle']
    ))
    story.append(emerald_divider())
    story.append(Paragraph(
        "Built for Baylor Scott &amp; White medical professionals relocating to Temple, Texas. "
        "This guide covers neighborhoods by commute time, physician loan math, school districts, "
        "and the honest tradeoffs of living here. No sales pitch \u2014 just the data you need to make a fast, informed decision.",
        styles['body']
    ))
    story.append(Spacer(1, 6))
    story.append(callout_box(
        "<b>Who this is for:</b> Residents (PGY-1 through PGY-6), fellows, attending physicians, "
        "nurses, and medical staff starting at BSW Temple. Whether you're arriving July 1 or planning "
        "months ahead, this guide works backward from your start date.",
        styles
    ))
    story.append(Spacer(1, 10))

    # Timeline
    story.append(Paragraph("Match Day \u2192 July 1: Your Relocation Timeline", styles['h2']))
    timeline_data = [
        [Paragraph("<b>When</b>", styles['table_header']),
         Paragraph("<b>What to Do</b>", styles['table_header']),
         Paragraph("<b>Why It Matters</b>", styles['table_header'])],
        [Paragraph("Match Day<br/>(March)", styles['table_cell_bold']),
         Paragraph("Get pre-approved for a physician loan. Call a lender who does 0% down physician loans in TX.", styles['table_cell']),
         Paragraph("Physician loans require specific lenders. Not every bank offers them. Start here.", styles['table_cell'])],
        [Paragraph("March-April", styles['table_cell_bold']),
         Paragraph("Pick 2-3 neighborhoods from this guide. Schedule virtual tours or a visit.", styles['table_cell']),
         Paragraph("Inventory moves fast in spring. Waiting until June means fewer options.", styles['table_cell'])],
        [Paragraph("April-May", styles['table_cell_bold']),
         Paragraph("Make an offer. Lock rate. Order inspection.", styles['table_cell']),
         Paragraph("30-45 day close means an April offer closes by June. That's your target.", styles['table_cell'])],
        [Paragraph("June", styles['table_cell_bold']),
         Paragraph("Close. Set up utilities (Temple Water Dept, Oncor Electric). Get keys.", styles['table_cell']),
         Paragraph("Temple Water requires in-person or online signup. Budget $150 deposit.", styles['table_cell'])],
        [Paragraph("July 1", styles['table_cell_bold']),
         Paragraph("Start residency. Your commute is under 15 minutes.", styles['table_cell']),
         Paragraph("You're already home. No apartment limbo, no temporary housing stress.", styles['table_cell'])],
    ]
    t = Table(timeline_data, colWidths=[usable_w*0.15, usable_w*0.45, usable_w*0.40])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('BACKGROUND', (0,1), (-1,1), TABLE_ALT_ROW),
        ('BACKGROUND', (0,3), (-1,3), TABLE_ALT_ROW),
        ('BACKGROUND', (0,5), (-1,5), TABLE_ALT_ROW),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Pro tip:</b> If you're renting first, most Temple apartments do 6-month leases. "
        "But you'll pay 15-20% more in rent than a mortgage payment on the same square footage. "
        "Buying on a physician loan is almost always the smarter move if you're staying 3+ years.",
        styles['body_small']
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════
    # PAGES 2-3: NEIGHBORHOOD GUIDE BY COMMUTE
    # ════════════════════════════════════════════
    story.append(section_label("Neighborhood Guide", styles))
    story.append(Paragraph("Top 8 Neighborhoods by BSW Commute", styles['h1']))
    story.append(Paragraph(
        "Every neighborhood below is within 15 minutes of BSW Main Campus (2401 S 31st St). "
        "Commute times are peak-hour actuals, not Google Maps optimistic estimates. "
        "All price ranges reflect Q1 2026 MLS data.",
        styles['body']
    ))
    story.append(Spacer(1, 4))

    # Compact cell styles for the big table
    hood_cell = ParagraphStyle(
        'HoodCell', fontName='Helvetica', fontSize=7.5, leading=9.5,
        textColor=DARK_TEXT
    )
    hood_cell_bold = ParagraphStyle(
        'HoodCellBold', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
        textColor=DARK_TEXT
    )
    hood_header_style = ParagraphStyle(
        'HoodHeader', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
        textColor=WHITE
    )

    neighborhoods = [
        ["Wyndham Hill", "7 min", "$250K-$375K", "Belton ISD", "2005-2015 builds. Highest BSW staff concentration. Walking distance to retail on W Adams.", "BSW residents, medical couples"],
        ["Prairie Ridge", "10 min", "$210K-$300K", "Temple ISD", "2003-2010 builds. Solid brick, 1,400-2,200 sqft. Best value per sqft in West Temple.", "PGY-1/PGY-2, first-time buyers"],
        ["Canyon Creek", "10 min", "$240K-$340K", "Temple ISD", "2008-2020 builds. Mix of builders. Strong resale history. Larger lots.", "Families, mid-career professionals"],
        ["Lake Pointe", "10 min", "$275K-$400K", "Belton ISD", "2015-2024 builds. Modern open-concept floor plans. Community pool and amenities.", "Families wanting newer + Belton ISD"],
        ["Bella Terra", "11 min", "$260K-$370K", "Temple ISD", "2016-2023 builds. Energy-efficient newer construction. Still adding inventory.", "Young families, move-up buyers"],
        ["Windmill Farms", "12 min", "$280K-$420K", "Belton ISD", "Active HOA. Pool, park, walking trails. 2012-2022 builds. Strong identity.", "Families wanting amenities + BISD"],
        ["Belton Proper", "13 min", "$230K-$380K", "Belton ISD", "Small-town feel, historic downtown. Mix of new and established. UMHB nearby.", "Small-town character, BISD priority"],
        ["Legacy Ranch", "14 min", "$320K-$500K", "Belton ISD", "Premium/executive. 2018-2024 builds. Larger lots, higher-end finishes.", "Attending physicians, executives"],
    ]

    # Main comparison table
    hood_header = [
        Paragraph("<b>Neighborhood</b>", hood_header_style),
        Paragraph("<b>BSW</b>", hood_header_style),
        Paragraph("<b>Price Range</b>", hood_header_style),
        Paragraph("<b>District</b>", hood_header_style),
        Paragraph("<b>Character</b>", hood_header_style),
        Paragraph("<b>Best For</b>", hood_header_style),
    ]
    hood_rows = [hood_header]
    for i, n in enumerate(neighborhoods):
        row = [
            Paragraph(f"<b>{n[0]}</b>", hood_cell_bold),
            Paragraph(n[1], hood_cell),
            Paragraph(n[2], hood_cell),
            Paragraph(n[3], hood_cell),
            Paragraph(n[4], hood_cell),
            Paragraph(n[5], hood_cell),
        ]
        hood_rows.append(row)

    t = Table(hood_rows, colWidths=[
        usable_w*0.13, usable_w*0.07, usable_w*0.14,
        usable_w*0.10, usable_w*0.34, usable_w*0.22
    ])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]
    # Alternating row colors
    for i in range(1, len(hood_rows)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), TABLE_ALT_ROW))
    t.setStyle(TableStyle(style_cmds))
    story.append(t)

    story.append(Spacer(1, 6))
    story.append(callout_box(
        "<b>School district matters for resale.</b> Belton ISD neighborhoods command a 5-10% "
        "premium over comparable Temple ISD homes. If you're only staying 3-4 years for residency, "
        "Belton ISD protects your equity better. If you're staying long-term and want lower entry price, "
        "Temple ISD neighborhoods like Canyon Creek and Prairie Ridge are strong picks.",
        styles
    ))
    story.append(Spacer(1, 6))

    # Quick-pick guide
    quick_pick_elements = []
    quick_pick_elements.append(Paragraph("Quick Pick by Situation", styles['h2']))
    picks = [
        ["PGY-1 on a budget", "Prairie Ridge", "$210K-$300K, Temple ISD, lowest entry in West Temple"],
        ["BSW couple, no kids yet", "Wyndham Hill", "7-min commute, walkable retail, under $375K"],
        ["Family, schools matter most", "Lake Pointe or Windmill Farms", "Belton ISD, newer builds, community amenities"],
        ["Attending physician", "Legacy Ranch", "Executive homes $320K-$500K, space, privacy, Belton ISD"],
        ["Want to rent it out later", "Canyon Creek or Prairie Ridge", "Strong rental demand, good price-to-rent ratios"],
    ]
    pick_header = [
        Paragraph("<b>Your Situation</b>", styles['table_header']),
        Paragraph("<b>Start Here</b>", styles['table_header']),
        Paragraph("<b>Why</b>", styles['table_header']),
    ]
    pick_rows = [pick_header]
    for p in picks:
        pick_rows.append([
            Paragraph(p[0], styles['table_cell_bold']),
            Paragraph(p[1], styles['table_cell_bold']),
            Paragraph(p[2], styles['table_cell']),
        ])
    t = Table(pick_rows, colWidths=[usable_w*0.25, usable_w*0.30, usable_w*0.45])
    style_cmds2 = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]
    for i in range(1, len(pick_rows)):
        if i % 2 == 0:
            style_cmds2.append(('BACKGROUND', (0,i), (-1,i), TABLE_ALT_ROW))
    t.setStyle(TableStyle(style_cmds2))
    quick_pick_elements.append(t)
    story.append(KeepTogether(quick_pick_elements))

    story.append(PageBreak())

    # ════════════════════════════════════════════
    # PAGE 4: PHYSICIAN LOAN BREAKDOWN
    # ════════════════════════════════════════════
    story.append(section_label("Physician Loan Calculator", styles))
    story.append(Paragraph("Physician Loan Breakdown", styles['h1']))
    story.append(Paragraph(
        "A physician mortgage loan lets you buy a home with 0% down and no private mortgage insurance (PMI). "
        "This is the single biggest financial advantage you have as a medical professional. Here's how it works "
        "and what you can actually afford at each training level.",
        styles['body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("How Physician Loans Work", styles['h2']))
    loan_features = [
        "<bullet>&bull;</bullet><b>0% down payment</b> \u2014 No savings drain before residency starts",
        "<bullet>&bull;</bullet><b>No PMI</b> \u2014 Saves $150-$350/month vs conventional loans with <20% down",
        "<bullet>&bull;</bullet><b>Residency income accepted</b> \u2014 Lenders use your contract salary, not your current income",
        "<bullet>&bull;</bullet><b>Student debt excluded or reduced</b> \u2014 Most lenders use IBR payment (not full balance) for DTI",
        "<bullet>&bull;</bullet><b>Closing costs can be rolled in</b> \u2014 Some lenders offer this; ask specifically",
        "<bullet>&bull;</bullet><b>Available to: MD, DO, DDS, DMD, OD, DPM, PharmD, DVM</b> (varies by lender)",
    ]
    for item in loan_features:
        story.append(Paragraph(item, styles['bullet']))
    story.append(Spacer(1, 6))

    story.append(callout_box(
        "<b>Lender tip:</b> Not every bank offers physician loans. In Temple, Extraco Bank is the go-to local "
        "option for physician mortgage products. National lenders like Flagstar and Truist also write them in TX. "
        "Get quotes from at least two \u2014 rates can vary 0.25-0.5% between lenders.",
        styles
    ))
    story.append(Spacer(1, 8))

    # Budget table
    story.append(Paragraph("What You Can Afford: PGY-1 Through PGY-6", styles['h2']))
    story.append(Paragraph(
        "Based on physician loan qualifying at 0% down, 6.75% rate, 30-year fixed. "
        "Max purchase assumes 33% DTI with IBR student loan payment. Your actual max may vary by lender and debt load.",
        styles['body_small']
    ))

    budget_header = [
        Paragraph("<b>Level</b>", styles['table_header']),
        Paragraph("<b>Annual Salary</b>", styles['table_header']),
        Paragraph("<b>Monthly Gross</b>", styles['table_header']),
        Paragraph("<b>Max Purchase</b>", styles['table_header']),
        Paragraph("<b>Monthly PITI</b>", styles['table_header']),
        Paragraph("<b>Best Neighborhoods</b>", styles['table_header']),
    ]
    budget_rows = [budget_header]
    budget_data = [
        ["PGY-1", "$65,000", "$5,417", "~$274,000", "~$1,787", "Prairie Ridge, Canyon Creek"],
        ["PGY-2", "$67,000", "$5,583", "~$283,000", "~$1,846", "Prairie Ridge, Canyon Creek"],
        ["PGY-3", "$69,500", "$5,792", "~$294,000", "~$1,917", "Canyon Creek, Wyndham Hill"],
        ["PGY-4", "$72,000", "$6,000", "~$306,000", "~$1,996", "Wyndham Hill, Bella Terra"],
        ["PGY-5", "$74,500", "$6,208", "~$317,000", "~$2,067", "Lake Pointe, Windmill Farms"],
        ["PGY-6", "$77,000", "$6,417", "~$328,000", "~$2,139", "Lake Pointe, Windmill Farms"],
        ["Attending", "$250K-$450K+", "$20K-$37K+", "$600K-$1M+", "Varies", "Legacy Ranch, custom builds"],
    ]
    for row in budget_data:
        budget_rows.append([Paragraph(cell, styles['table_cell_bold'] if i == 0 else styles['table_cell'])
                           for i, cell in enumerate(row)])

    t = Table(budget_rows, colWidths=[
        usable_w*0.10, usable_w*0.14, usable_w*0.14,
        usable_w*0.14, usable_w*0.14, usable_w*0.34
    ])
    style_cmds3 = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]
    for i in range(1, len(budget_rows)):
        if i % 2 == 0:
            style_cmds3.append(('BACKGROUND', (0,i), (-1,i), TABLE_ALT_ROW))
    # Highlight attending row
    style_cmds3.append(('BACKGROUND', (0, len(budget_rows)-1), (-1, len(budget_rows)-1), HexColor("#ecfdf5")))
    t.setStyle(TableStyle(style_cmds3))
    story.append(t)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Reality check:</b> A PGY-1 making $65K can qualify for ~$274K on a physician loan. "
        "That puts Prairie Ridge ($210K-$300K) and parts of Canyon Creek ($240K-$340K) squarely in range. "
        "You're not stuck renting. You're building equity from day one while your co-residents pay a landlord.",
        styles['body']
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════
    # PAGE 5: SCHOOL DISTRICTS + HONEST TRUTH
    # ════════════════════════════════════════════
    story.append(section_label("Schools + Honest Truth", styles))
    story.append(Paragraph("School District Comparison", styles['h1']))
    story.append(Paragraph(
        "Temple has two main school districts that affect both daily life and resale value. "
        "Where you buy determines your district \u2014 you can't choose.",
        styles['body']
    ))

    school_header = [
        Paragraph("<b></b>", styles['table_header']),
        Paragraph("<b>Belton ISD</b>", styles['table_header']),
        Paragraph("<b>Temple ISD</b>", styles['table_header']),
    ]
    school_data = [
        school_header,
        [Paragraph("<b>Reputation</b>", styles['table_cell_bold']),
         Paragraph("Higher rated overall. Lake Belton HS (7/10 GreatSchools). More suburban feel.", styles['table_cell']),
         Paragraph("Improving rapidly. Strong magnet programs. More diverse student body.", styles['table_cell'])],
        [Paragraph("<b>Key High School</b>", styles['table_cell_bold']),
         Paragraph("Lake Belton High School", styles['table_cell']),
         Paragraph("Temple High School", styles['table_cell'])],
        [Paragraph("<b>Neighborhoods</b>", styles['table_cell_bold']),
         Paragraph("Wyndham Hill, Lake Pointe, Windmill Farms, Legacy Ranch, Belton, Sage Meadows", styles['table_cell']),
         Paragraph("Canyon Creek, Prairie Ridge, Bella Terra, parts of central Temple", styles['table_cell'])],
        [Paragraph("<b>Resale Impact</b>", styles['table_cell_bold']),
         Paragraph("5-10% price premium over comparable Temple ISD homes", styles['table_cell']),
         Paragraph("Lower entry price = better value per sqft. Growing demand.", styles['table_cell'])],
        [Paragraph("<b>Bottom Line</b>", styles['table_cell_bold']),
         Paragraph("Pay more upfront, protect resale. Best if staying <5 years.", styles['table_cell']),
         Paragraph("Lower cost, more house for the money. Best if staying long-term or investing.", styles['table_cell'])],
    ]
    t = Table(school_data, colWidths=[usable_w*0.18, usable_w*0.41, usable_w*0.41])
    style_cmds4 = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]
    for i in range(1, len(school_data)):
        if i % 2 == 0:
            style_cmds4.append(('BACKGROUND', (0,i), (-1,i), TABLE_ALT_ROW))
    t.setStyle(TableStyle(style_cmds4))
    story.append(t)

    story.append(Spacer(1, 10))
    story.append(emerald_divider())
    story.append(Spacer(1, 4))

    # The Honest Truth
    story.append(Paragraph("The Honest Truth About Living in Temple", styles['h1']))
    story.append(Paragraph(
        "I'm not going to pretend Temple is Austin. It's not. Here's what you're actually signing up for \u2014 "
        "the good and the bad.",
        styles['body']
    ))

    # Use a compact bullet style for this page to fit everything
    compact_bullet = ParagraphStyle(
        'CompactBullet', fontName='Helvetica', fontSize=9, leading=12.5,
        textColor=BODY_TEXT, spaceAfter=2, leftIndent=18, bulletIndent=6,
        bulletFontName='Helvetica', bulletFontSize=9
    )

    # Negatives
    story.append(Paragraph("What You Should Know", styles['h2']))
    negatives = [
        "<bullet>&bull;</bullet><b>Summers are brutal.</b> June-September averages 95-100\u00b0F. Triple digits are normal. Electric bill: $250-$400/month in peak summer.",
        "<bullet>&bull;</bullet><b>I-35 construction is ongoing.</b> Expansion runs through 2028. North-south commutes add 5-10 minutes during construction windows.",
        "<bullet>&bull;</bullet><b>Nightlife is limited.</b> Good restaurants but no real bar scene. Austin is 70 min south, Waco 35 min north. Quiet town by design.",
        "<bullet>&bull;</bullet><b>Property taxes are high.</b> Effective rate: 2.18-2.50%. On a $300K home: $6,500-$7,500/year. No state income tax offsets this \u2014 but the sticker shock is real.",
        "<bullet>&bull;</bullet><b>Limited specialists outside BSW.</b> Most colleagues will also be your neighbors. The medical community is tight-knit, for better and worse.",
    ]
    for neg in negatives:
        story.append(Paragraph(neg, compact_bullet))

    story.append(Spacer(1, 4))

    # Positives
    story.append(Paragraph("Why People Love It Anyway", styles['h2']))
    positives = [
        "<bullet>&bull;</bullet><b>Your commute is under 15 minutes.</b> Every neighborhood in this guide. No highway, no traffic. That's 1-2 hours of your life back every day.",
        "<bullet>&bull;</bullet><b>No state income tax.</b> On a $300K attending salary, that's $15K-$25K/year you keep vs California, New York, or Illinois.",
        "<bullet>&bull;</bullet><b>Cost of living is 18% below national average.</b> Your dollar stretches further on housing, food, childcare, and daily expenses.",
        "<bullet>&bull;</bullet><b>You can actually afford a home.</b> A PGY-1 can buy a 3-bed brick home here. Try that in Houston or Dallas.",
        "<bullet>&bull;</bullet><b>Community is real.</b> Temple is 82,000 people. Your neighbors know your name. Your kids play in the cul-de-sac. Most BSW staff who come for residency end up staying.",
    ]
    for pos in positives:
        story.append(Paragraph(pos, compact_bullet))

    story.append(PageBreak())

    # ════════════════════════════════════════════
    # PAGE 6: NEXT STEPS + CONTACT
    # ════════════════════════════════════════════
    story.append(section_label("Next Steps", styles))
    story.append(Paragraph("Ready to Find Your Place in Temple?", styles['h1']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "I specialize in BSW relocations. I've helped dozens of residents, fellows, and attending "
        "physicians find the right home in Temple \u2014 and I do it differently than most agents.",
        styles['body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Here's What We Do First", styles['h2']))
    steps = [
        ["1", "15-minute call", "You tell me your start date, budget, must-haves, and deal-breakers. I tell you which 2-3 neighborhoods fit and why."],
        ["2", "Physician loan intro", "I connect you with a lender who does physician loans in Texas. You get pre-approved in 48 hours."],
        ["3", "Custom property list", "I send you 5-10 homes that match your criteria \u2014 not a Zillow dump. Each one with my notes on condition, value, and commute."],
        ["4", "Virtual or in-person tours", "If you're out of state, I do video walkthroughs on FaceTime/Zoom. You see everything I see, including the stuff the listing photos don't show."],
        ["5", "Offer through close", "I handle negotiations, inspection coordination, and closing logistics. You focus on orientation \u2014 I handle the house."],
    ]
    steps_header = [
        Paragraph("<b>#</b>", styles['table_header']),
        Paragraph("<b>Step</b>", styles['table_header']),
        Paragraph("<b>What Happens</b>", styles['table_header']),
    ]
    steps_rows = [steps_header]
    for s in steps:
        steps_rows.append([
            Paragraph(s[0], styles['table_cell_bold']),
            Paragraph(s[1], styles['table_cell_bold']),
            Paragraph(s[2], styles['table_cell']),
        ])
    t = Table(steps_rows, colWidths=[usable_w*0.06, usable_w*0.20, usable_w*0.74])
    style_cmds5 = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]
    for i in range(1, len(steps_rows)):
        if i % 2 == 0:
            style_cmds5.append(('BACKGROUND', (0,i), (-1,i), TABLE_ALT_ROW))
    t.setStyle(TableStyle(style_cmds5))
    story.append(t)

    story.append(Spacer(1, 16))
    story.append(emerald_divider())
    story.append(Spacer(1, 12))

    # Contact card
    story.append(Paragraph("Taylor Dasch", styles['contact_name']))
    story.append(Paragraph("REALTOR &amp; Real Estate Investor | EG Realty | Temple, TX", styles['contact_role']))

    contact_data = [
        [Paragraph("<b>Phone/Text</b>", styles['table_cell_bold']),
         Paragraph("254-718-4249", styles['table_cell'])],
        [Paragraph("<b>Email</b>", styles['table_cell_bold']),
         Paragraph("dealswithdasch@gmail.com", styles['table_cell'])],
        [Paragraph("<b>Website</b>", styles['table_cell_bold']),
         Paragraph("templetxhomes.net", styles['table_cell'])],
        [Paragraph("<b>Book a Call</b>", styles['table_cell_bold']),
         Paragraph("calendly.com/dealswithdasch/housing-strategy-call", styles['table_cell'])],
        [Paragraph("<b>Credentials</b>", styles['table_cell_bold']),
         Paragraph("$27M+ in transactions | 100+ investment deals | 3-year BiggerPockets Featured Agent", styles['table_cell'])],
    ]
    t = Table(contact_data, colWidths=[usable_w*0.20, usable_w*0.80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_EMERALD_BG),
        ('GRID', (0,0), (-1,-1), 0.5, TABLE_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)

    story.append(Spacer(1, 16))
    story.append(callout_box(
        "<b>One last thing:</b> I'm not going to add you to a drip campaign or spam your inbox. "
        "I answer my phone. I respond to texts within an hour. And I'll tell you if a house is a bad deal \u2014 "
        "even if it means I don't get paid. That's how I've built my business, and it's how I'll help you.",
        styles
    ))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Data sources: MLS, BellCAD, Belton ISD, Temple ISD, GreatSchools, BSW GME office. "
        "All data requires property-specific verification. Guide current as of April 2026.",
        styles['footer']
    ))

    # ─── Build ───
    doc.build(story, onFirstPage=tmpl.on_first_page, onLaterPages=tmpl.on_page)
    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    output = os.path.expanduser("~/Downloads/BSW-Temple-Relocation-Guide.pdf")
    build_pdf(output)
