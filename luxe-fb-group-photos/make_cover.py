"""Facebook Group cover: 1640x856, two photos side-by-side."""
from PIL import Image, ImageDraw, ImageFont
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(FOLDER, "fb-group-cover.png")
W, H = 1640, 856

PICKS = [
    "luxe-twilight.jpeg",           # left — exterior
    "lux-lake-backdrop-front.jpeg", # right — waterfront
]

def crop_fill(img, tw, th):
    scale = max(tw / img.width, th / img.height)
    r = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    l = (r.width - tw) // 2
    t = (r.height - th) // 2
    return r.crop((l, t, l + tw, t + th))

canvas = Image.new("RGB", (W, H), (0, 0, 0))

# Two photos side by side, full height
half_w = W // 2
for i, fname in enumerate(PICKS):
    img = Image.open(os.path.join(FOLDER, fname))
    cropped = crop_fill(img, half_w, H)
    canvas.paste(cropped, (i * half_w, 0))

# Thin center divider
ImageDraw.Draw(canvas).line([(W // 2, 0), (W // 2, H)], fill=(20, 20, 20), width=2)

# Gradient overlay bottom 45%
canvas = canvas.convert("RGBA")
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
gs = int(H * 0.50)
for y in range(gs, H):
    a = int(210 * ((y - gs) / (H - gs)))
    od.line([(0, y), (W, y)], fill=(15, 15, 15, a))
canvas = Image.alpha_composite(canvas, overlay)

# Emerald top accent
acc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(acc).rectangle([(0, 0), (W, 4)], fill=(5, 150, 105, 200))
canvas = Image.alpha_composite(canvas, acc)

# Fonts
def get_font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            pass
    return ImageFont.load_default()

bold = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]
reg = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"]

draw = ImageDraw.Draw(canvas)

# Main text — inside safe zone (y 97–759)
main = "Unique Listings | Temple & Belton Real Estate"
f1 = get_font(bold, 52)
bb = draw.textbbox((0, 0), main, font=f1)
tx = (W - (bb[2] - bb[0])) // 2
ty = 560
draw.text((tx + 2, ty + 2), main, font=f1, fill=(0, 0, 0, 180))
draw.text((tx, ty), main, font=f1, fill=(255, 255, 255))

# Emerald divider
ly = ty + (bb[3] - bb[1]) + 15
draw.line([(W // 2 - 120, ly), (W // 2 + 120, ly)], fill=(5, 150, 105), width=3)

# Branding
brand = "Taylor Dasch  •  EG Realty"
f2 = get_font(reg, 24)
bb2 = draw.textbbox((0, 0), brand, font=f2)
bx = (W - (bb2[2] - bb2[0])) // 2
by = ly + 16
draw.text((bx + 1, by + 1), brand, font=f2, fill=(0, 0, 0, 150))
draw.text((bx, by), brand, font=f2, fill=(200, 200, 200))

canvas.convert("RGB").save(OUTPUT, "PNG", quality=95)
print(f"Saved: {OUTPUT} ({W}x{H})")
