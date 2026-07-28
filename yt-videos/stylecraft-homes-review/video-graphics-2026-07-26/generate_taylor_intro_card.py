#!/usr/bin/env python3
"""Generate Taylor Dasch's reusable 16:9 video introduction card."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(
    "/Users/taylordasch_1/claude-social-media-manager/yt-videos/"
    "stylecraft-homes-review/video-graphics-2026-07-26"
)
HEADSHOT = Path(
    "/Users/taylordasch_1/claude-social-media-manager/templates/"
    "end-cards/taylor-headshot.jpg"
)
FULL_4K = ROOT / "fullframe-4k" / "G00-taylor-intro-card.png"
FULL_1080 = ROOT / "fullframe-1080" / "G00-taylor-intro-card.png"
PREVIEW = ROOT / "previews" / "G00-taylor-intro-card-preview.jpg"

W, H = 3840, 2160

INK = (6, 16, 34, 255)
INK_2 = (8, 34, 51, 255)
CARD = (20, 42, 61, 255)
EMERALD = (5, 150, 105, 255)
EMERALD_BRIGHT = (39, 211, 157, 255)
MINT = (126, 240, 202, 255)
SNOW = (248, 250, 252, 255)
SLATE = (183, 198, 219, 255)
SLATE_2 = (113, 135, 164, 255)

FONT_SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_SANS_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1),
        radius=radius,
        fill=255,
    )
    return mask


def fit_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_ratio = size[0] / size[1]
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        crop_w = round(image.height * target_ratio)
        left = round((image.width - crop_w) * 0.56)
        image = image.crop((left, 0, left + crop_w, image.height))
    else:
        crop_h = round(image.width / target_ratio)
        top = max(0, round((image.height - crop_h) * 0.25))
        image = image.crop((0, top, image.width, top + crop_h))
    return image.resize(size, Image.Resampling.LANCZOS)


def draw_letterspaced(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    spacing: int,
) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=face, fill=fill)
        x += draw.textlength(char, font=face) + spacing


def make_card() -> Image.Image:
    image = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(image)

    # Deep architectural background with a restrained drafting grid.
    for y in range(H):
        t = y / H
        color = (
            round(INK[0] * (1 - t) + INK_2[0] * t),
            round(INK[1] * (1 - t) + INK_2[1] * t),
            round(INK[2] * (1 - t) + INK_2[2] * t),
            255,
        )
        draw.line((0, y, W, y), fill=color)

    grid = (58, 88, 112, 44)
    for x in range(0, W, 192):
        draw.line((x, 0, x, H), fill=grid, width=2)
    for y in range(0, H, 192):
        draw.line((0, y, W, y), fill=grid, width=2)

    # Emerald stage mark and oversized ghost initials.
    draw.rectangle((0, 0, 42, H), fill=EMERALD_BRIGHT)
    ghost = font(FONT_SANS_BLACK, 830)
    draw.text((1090, 550), "TD", font=ghost, fill=(24, 61, 76, 72))

    # Portrait panel with shadow and a cinematic navy color wash.
    panel_box = (2300, 170, 3580, 1990)
    panel_size = (panel_box[2] - panel_box[0], panel_box[3] - panel_box[1])
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (
            panel_box[0] + 34,
            panel_box[1] + 42,
            panel_box[2] + 34,
            panel_box[3] + 42,
        ),
        radius=62,
        fill=(0, 0, 0, 160),
    )
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(35)))

    portrait = fit_cover(Image.open(HEADSHOT).convert("RGB"), panel_size).convert("RGBA")
    wash = Image.new("RGBA", panel_size, (4, 27, 43, 0))
    wash_alpha = Image.new("L", panel_size, 0)
    wash_draw = ImageDraw.Draw(wash_alpha)
    for x in range(panel_size[0]):
        alpha = max(0, round(85 * (1 - x / panel_size[0])))
        wash_draw.line((x, 0, x, panel_size[1]), fill=alpha)
    wash.putalpha(wash_alpha)
    portrait = Image.alpha_composite(portrait, wash)
    portrait.putalpha(rounded_mask(panel_size, 62))
    image.alpha_composite(portrait, (panel_box[0], panel_box[1]))

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(panel_box, radius=62, outline=(80, 240, 191, 175), width=6)
    draw.rectangle(
        (panel_box[0] - 14, panel_box[1] + 180, panel_box[0] + 2, panel_box[3] - 180),
        fill=EMERALD_BRIGHT,
    )

    # Small top-line identity.
    eyebrow_face = font(FONT_SANS_BOLD, 43)
    draw.rectangle((190, 178, 224, 212), fill=EMERALD_BRIGHT)
    draw_letterspaced(
        draw,
        (255, 163),
        "LIVING IN TEMPLE  /  CENTRAL TEXAS",
        eyebrow_face,
        MINT,
        4,
    )

    # Editorial name lockup.
    name_face = font(FONT_SERIF_BOLD, 270)
    draw.text((185, 445), "TAYLOR", font=name_face, fill=SNOW)
    draw.text((185, 710), "DASCH", font=name_face, fill=SNOW)

    role_face = font(FONT_SANS_BOLD, 54)
    draw_letterspaced(
        draw,
        (195, 1065),
        "REAL ESTATE AGENT  •  EG REALTY",
        role_face,
        EMERALD_BRIGHT,
        3,
    )

    tagline_face = font(FONT_SERIF_BOLD, 72)
    draw.text(
        (190, 1195),
        "HONEST BUILDER REVIEWS.",
        font=tagline_face,
        fill=SNOW,
    )
    draw.text(
        (190, 1285),
        "LOCAL DEAL GUIDANCE.",
        font=tagline_face,
        fill=SNOW,
    )

    # Contact card: readable on phones and television.
    contact_box = (185, 1510, 2100, 1910)
    draw.rounded_rectangle(contact_box, radius=44, fill=CARD, outline=(55, 91, 111, 255), width=3)
    draw.rounded_rectangle(
        (contact_box[0], contact_box[1], contact_box[0] + 26, contact_box[3]),
        radius=13,
        fill=EMERALD_BRIGHT,
    )

    label_face = font(FONT_SANS_BOLD, 36)
    value_face = font(FONT_SANS_BOLD, 69)
    email_face = font(FONT_SANS_BOLD, 51)

    draw_letterspaced(draw, (270, 1570), "CALL / TEXT", label_face, SLATE_2, 5)
    draw.text((270, 1632), "254-718-4249", font=value_face, fill=SNOW)
    draw.line((1115, 1570, 1115, 1848), fill=(72, 104, 124, 255), width=3)
    draw_letterspaced(draw, (1190, 1570), "EMAIL", label_face, SLATE_2, 5)
    draw.text((1190, 1660), "dealswithdasch@gmail.com", font=email_face, fill=SNOW)

    footer_face = font(FONT_SANS_BOLD, 35)
    draw.text((190, 2030), "TEMPLETXHOMES.NET", font=footer_face, fill=EMERALD_BRIGHT)
    footer_right = "TEMPLE  •  BELTON  •  KILLEEN  •  FORT CAVAZOS"
    right_w = draw.textlength(footer_right, font=footer_face)
    draw.text((W - right_w - 190, 2030), footer_right, font=footer_face, fill=SLATE)

    return image


def main() -> None:
    card = make_card().convert("RGB")
    FULL_4K.parent.mkdir(parents=True, exist_ok=True)
    FULL_1080.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    card.save(FULL_4K, quality=96)
    card.resize((1920, 1080), Image.Resampling.LANCZOS).save(FULL_1080, quality=96)
    card.resize((1280, 720), Image.Resampling.LANCZOS).save(PREVIEW, quality=92)
    print(FULL_4K)
    print(FULL_1080)
    print(PREVIEW)


if __name__ == "__main__":
    main()
