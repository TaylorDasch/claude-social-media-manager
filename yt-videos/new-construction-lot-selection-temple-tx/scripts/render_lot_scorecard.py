#!/usr/bin/env python3
"""Render Taylor Dasch's one-page Temple new-build lot scorecard."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "temple-new-build-lot-scorecard.pdf"

PAGE_W, PAGE_H = letter
MARGIN = 32
NAVY = HexColor("#0D1B2A")
INK = HexColor("#17212B")
MUTED = HexColor("#5E6B75")
EMERALD = HexColor("#0A7B60")
PALE_EMERALD = HexColor("#EAF5F1")
PALE_BLUE = HexColor("#F3F6F8")
BORDER = HexColor("#CBD5DC")


def wrap(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, max_width, font="Helvetica", size=8, leading=10, color=INK, max_lines=None):
    lines = wrap(text, font, size, max_width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def line(c, x1, y1, x2, y2, color=BORDER, width=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    c.setTitle("Temple New-Build Lot Scorecard")
    c.setAuthor("Taylor Dasch | EG Realty")
    c.setSubject("Five-check buyer worksheet for comparing Temple-area new-build lots")

    # Header
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 96, PAGE_W, 96, fill=1, stroke=0)
    c.setFillColor(EMERALD)
    c.rect(MARGIN, PAGE_H - 78, 5, 48, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Times-Bold", 23)
    c.drawString(MARGIN + 16, PAGE_H - 48, "TEMPLE NEW-BUILD")
    c.drawString(MARGIN + 16, PAGE_H - 72, "LOT SCORECARD")
    c.setFont("Helvetica-Bold", 8.5)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 43, "TAYLOR DASCH | EG REALTY")
    c.setFont("Helvetica", 8)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 58, "254-718-4249 | templetxhomes.net")
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 72, "Version 2026-07-19")

    # Boundary callout
    y_top = PAGE_H - 108
    c.setFillColor(PALE_EMERALD)
    c.roundRect(MARGIN, y_top - 43, PAGE_W - 2 * MARGIN, 43, 7, fill=1, stroke=0)
    c.setFillColor(EMERALD)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN + 10, y_top - 14, "USE TWO RESULTS - DO NOT TURN MISSING PROOF INTO A PASS")
    draw_wrapped(
        c,
        "Buyer fit: FITS / TRADEOFF / CONFLICTS.  Proof: VERIFIED / NEEDS DOCUMENT / NEEDS PROFESSIONAL.",
        MARGIN + 10,
        y_top - 28,
        PAGE_W - 2 * MARGIN - 20,
        size=8,
        leading=9,
    )

    # Priorities
    y = y_top - 57
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "YOUR THREE LOT PRIORITIES")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - MARGIN, y, "Use your stated preferences - never a universal lot ranking")
    y -= 13
    for idx in range(1, 4):
        c.setFillColor(EMERALD)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(MARGIN, y, str(idx))
        line(c, MARGIN + 15, y - 1, PAGE_W - MARGIN, y - 1)
        y -= 17

    # Comparison grid
    y -= 2
    grid_left = MARGIN
    grid_right = PAGE_W - MARGIN
    check_w = 198
    lot_w = (grid_right - grid_left - check_w) / 3
    xs = [grid_left, grid_left + check_w, grid_left + check_w + lot_w, grid_left + check_w + 2 * lot_w, grid_right]
    header_h = 24
    row_h = 55

    c.setFillColor(NAVY)
    c.rect(grid_left, y - header_h, grid_right - grid_left, header_h, fill=1, stroke=0)
    headers = ["FIVE CHECKS", "LOT A", "LOT B", "LOT C"]
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    for i, label in enumerate(headers):
        left = xs[i]
        right = xs[i + 1]
        if i == 0:
            c.drawString(left + 8, y - 16, label)
        else:
            c.drawCentredString((left + right) / 2, y - 16, label)
    y -= header_h

    checks = [
        ("1  WATER + GRADE QUESTIONS", "Visible grading, swales, curbs and inlets; records show intended design."),
        ("2  ORIENTATION + EXPOSURE", "Use the north arrow and confirmed house placement; phone compass is secondary."),
        ("3  DOCUMENTED CONSTRAINTS", "Shown building lines, easements and apparent area around the fixed placement."),
        ("4  STREET POSITION + ACCESS", "Date/time-labeled observations; not a traffic study or guarantee."),
        ("5  FUTURE EDGE + ADJACENCY", "Identify the exact plan/document type, status and date; plans can change."),
    ]

    for row_index, (title, note) in enumerate(checks):
        fill = white if row_index % 2 == 0 else PALE_BLUE
        c.setFillColor(fill)
        c.rect(grid_left, y - row_h, grid_right - grid_left, row_h, fill=1, stroke=0)
        line(c, grid_left, y, grid_right, y)
        for x in xs:
            line(c, x, y, x, y - row_h)

        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7.6)
        c.drawString(grid_left + 7, y - 15, title)
        draw_wrapped(c, note, grid_left + 7, y - 29, check_w - 14, size=7, leading=8, color=MUTED, max_lines=3)

        for col in range(1, 4):
            x = xs[col] + 7
            cell_w = xs[col + 1] - xs[col] - 14
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(x, y - 14, "FIT:")
            line(c, x + 21, y - 15, x + cell_w, y - 15, color=MUTED, width=0.45)
            c.drawString(x, y - 29, "PROOF:")
            line(c, x + 31, y - 30, x + cell_w, y - 30, color=MUTED, width=0.45)
            c.setFont("Helvetica", 6.5)
            c.setFillColor(MUTED)
            c.drawString(x, y - 43, "Note:")
            line(c, x + 20, y - 44, x + cell_w, y - 44, color=MUTED, width=0.45)
        y -= row_h
    line(c, grid_left, y, grid_right, y)

    # Document timing
    y -= 12
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(MARGIN, y, "DOCUMENT TIMING")
    y -= 9
    box_h = 112
    gap = 10
    col_w = (PAGE_W - 2 * MARGIN - gap) / 2

    for idx, (box_title, bullets) in enumerate([
        (
            "BEFORE A RESERVATION FEE",
            [
                "Recorded phase plat",
                "Exact builder plot/site plan + confirmed placement",
                "Recorded restrictions + written easement/utility answers",
                "Current adjoining phase/road record",
                "Refundability, deadlines, lot-change rights + documents provided",
            ],
        ),
        (
            "WHEN ISSUED LATER",
            [
                "Title commitment + Schedule B/exceptions review",
                "Final survey + legal-description comparison",
                "Updated plans, restrictions or drainage documents",
                "Right professional for engineering, title, survey or legal meaning",
                "Tell Taylor if you visited, registered, reserved, signed or have an agent",
            ],
        ),
    ]):
        x = MARGIN + idx * (col_w + gap)
        c.setFillColor(PALE_EMERALD if idx == 0 else PALE_BLUE)
        c.roundRect(x, y - box_h, col_w, box_h, 6, fill=1, stroke=0)
        c.setFillColor(EMERALD if idx == 0 else NAVY)
        c.setFont("Helvetica-Bold", 7.8)
        c.drawString(x + 9, y - 15, box_title)
        bullet_y = y - 31
        for bullet in bullets:
            c.setFillColor(EMERALD)
            c.circle(x + 12, bullet_y + 2, 1.5, fill=1, stroke=0)
            bullet_y = draw_wrapped(c, bullet, x + 19, bullet_y + 5, col_w - 28, size=6.7, leading=7.6, color=INK, max_lines=2) - 3

    # Footer
    footer_y = 24
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, 42, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, footer_y, "TEXT LOT TO 254-718-4249")
    c.setFont("Helvetica", 7.2)
    c.drawRightString(PAGE_W - MARGIN, footer_y, "Community + up to 3 lot numbers | Do not post an address publicly")
    c.setFont("Helvetica", 5.8)
    c.drawCentredString(
        PAGE_W / 2,
        9,
        "Question-and-document worksheet only. It does not clear engineering, survey, title, flood, tax, insurance, HOA or construction issues.",
    )

    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
