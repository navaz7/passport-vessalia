#!/usr/bin/env python3
"""Build a 1024x1024 open passport spread for the invented Republic of Vessalia."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_SANS = "DejaVuSans.ttf"
F_BOLD = "DejaVuSans-Bold.ttf"
F_MONO = "DejaVuSansMono.ttf"
F_SERIF = "DejaVuSerif.ttf"
F_SERIFB = "DejaVuSerif-Bold.ttf"

CREAM = (246, 240, 222)
CREAM_D = (238, 229, 203)
INK = (38, 42, 58)
INK_SOFT = (70, 74, 88)
NAVY = (28, 52, 96)
GOLD = (150, 118, 52)
BLUE_INK = (52, 84, 150)
RED_INK = (168, 62, 62)
GREEN_INK = (44, 110, 88)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img, "RGBA")

# --- page backgrounds ---
d.rectangle([0, 0, 512, H], fill=(241, 234, 210))
d.rectangle([512, 0, W, H], fill=CREAM)
# outer border
d.rectangle([14, 14, W - 14, H - 14], outline=(190, 178, 145), width=2)
d.rectangle([22, 22, W - 22, H - 22], outline=(205, 195, 160), width=1)

# --- guilloche: faint concentric circles + fine lines ---
for cx, cy in [(256, 512), (768, 512), (256, 120), (768, 880)]:
    for r in range(30, 320, 22):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(210, 200, 165, 70), width=1)
for x in range(40, W - 40, 26):
    d.line([(x, 30), (x, H - 30)], fill=(215, 206, 175, 45), width=1)

# --- center spine shadow ---
for i in range(46):
    alpha = int(90 * (1 - i / 46))
    d.line([(512 - i, 0), (512 - i, H)], fill=(90, 80, 55, alpha), width=1)
    d.line([(512 + i, 0), (512 + i, H)], fill=(90, 80, 55, alpha), width=1)
d.line([(512, 0), (512, H)], fill=(120, 108, 78), width=2)

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def hline(x0, x1, y, color=(170, 158, 122), wdt=1):
    d.line([(x0, y), (x1, y)], fill=color, width=wdt)

# ================= LEFT PAGE: VISAS =================
text(256, 48, "VISAS", font(F_SERIFB, 30), NAVY, "ma")
hline(70, 442, 92)
text(256, 100, "Entries and departures recorded by", font(F_SANS, 11), INK_SOFT, "ma")
text(256, 118, "the competent authorities", font(F_SANS, 11), INK_SOFT, "ma")

def stamp(cx, cy, radius, color, lines, angle, oval=False):
    """Draw a rotated circular/oval stamp on its own layer and paste it."""
    size = radius * 2 + 40
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    c = size // 2
    box = [c - radius, c - int(radius * 0.72), c + radius, c + int(radius * 0.72)] if oval else \
          [c - radius, c - radius, c + radius, c + radius]
    ld.ellipse(box, outline=color + (205,), width=4)
    inner = [box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8]
    ld.ellipse(inner, outline=color + (150,), width=1)
    n = len(lines)
    for i, (s, sz) in enumerate(lines):
        yy = c - (n - 1) * sz * 0.62 + i * sz * 1.24
        ld.text((c, yy), s, font=font(F_BOLD, sz), fill=color + (215,), anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (int(cx - size / 2), int(cy - size / 2)), layer)

stamp(190, 250, 105, BLUE_INK,
      [("KORDAVIA", 17), ("ARRIVED", 13), ("17 SEP 2023", 14)], -8, oval=True)
stamp(330, 420, 100, RED_INK,
      [("KORDAVIA", 17), ("DEPARTED", 13), ("29 SEP 2023", 14)], 6, oval=True)
stamp(180, 580, 102, GREEN_INK,
      [("SAN MERAL", 17), ("ARRIVED", 13), ("03 MAY 2024", 14)], 4, oval=True)
stamp(335, 735, 108, BLUE_INK,
      [("HELVION REPUBLIC", 14), ("ARRIVED", 13), ("21 NOV 2024", 14)], -5, oval=True)
stamp(185, 875, 104, RED_INK,
      [("VESSALIA · PORT ANSELM", 12), ("DEPARTED", 13), ("09 JAN 2025", 14)], 7, oval=True)

# --- rectangular fee stamp (telling detail) ---
fee = Image.new("RGBA", (300, 96), (0, 0, 0, 0))
fd = ImageDraw.Draw(fee)
fd.rectangle([3, 3, 296, 92], outline=RED_INK + (215,), width=4)
fd.rectangle([10, 10, 289, 85], outline=RED_INK + (140,), width=1)
fd.text((150, 22), "TIDE FEE PAID", font=font(F_BOLD, 22), fill=RED_INK + (225,), anchor="ma")
fd.text((150, 54), "40 KR · PORT ANSELM", font=font(F_BOLD, 15), fill=RED_INK + (215,), anchor="ma")
fee = fee.rotate(-4, resample=Image.BICUBIC, expand=True)
img.paste(fee, (242, 292), fee)
d = ImageDraw.Draw(img, "RGBA")

text(70, 950, "Visa pages 4–5 · This passport contains 32 pages", font(F_SANS, 10), INK_SOFT)

# ================= RIGHT PAGE: DATA PAGE =================
# emblem: circle, star above waves
ex, ey = 768, 92
d.ellipse([ex - 34, ey - 34, ex + 34, ey + 34], outline=NAVY, width=3)
for k in range(3):
    yy = ey + 8 + k * 9
    pts = [(ex - 20 + i * 5, yy + (3 if i % 2 else -3)) for i in range(9)]
    d.line(pts, fill=NAVY, width=2)
# star
sx, sy, r1, r2 = ex, ey - 14, 13, 5
star = []
for i in range(10):
    ang = -math.pi / 2 + i * math.pi / 5
    rr = r1 if i % 2 == 0 else r2
    star.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
d.polygon(star, fill=GOLD)

text(768, 138, "REPUBLIC OF VESSALIA", font(F_SERIFB, 25), NAVY, "ma")
text(768, 172, "PASSPORT", font(F_SERIFB, 19), GOLD, "ma")
hline(560, 976, 204)
text(768, 212, "Passeport · Pas · Pasaporte", font(F_SANS, 10), INK_SOFT, "ma")

# --- portrait box ---
px0, py0, px1, py1 = 560, 250, 716, 452
d.rectangle([px0, py0, px1, py1], fill=(232, 224, 200), outline=NAVY, width=2)
for r in range(14, 150, 16):  # portrait background pattern
    d.ellipse([638 - r, 350 - r, 638 + r, 350 + r], outline=(200, 190, 158), width=1)
# stylized portrait: shoulders + head silhouette
d.pieslice([592, 330, 684, 470], 180, 360, fill=(74, 80, 98))
d.ellipse([606, 282, 670, 356], fill=(96, 102, 120))
d.arc([606, 268, 670, 330], 180, 360, fill=(60, 64, 80), width=7)  # hair arc
d.line([(592, 400), (684, 400)], fill=(60, 64, 80), width=2)
text(638, 458, "ILVES · MARA", font(F_MONO, 11), INK_SOFT, "ma")

# --- data fields ---
def field(x, y, label, value, vf=None):
    text(x, y, label, font(F_SANS, 10), (120, 108, 74))
    text(x, y + 14, value, vf or font(F_BOLD, 16), INK)

fx = 736
field(fx, 252, "Type / Type", "P")
field(fx, 296, "Country code", "VES")
field(fx, 340, "Passport No.", "VS0482137")
field(fx, 384, "Sex / Sexe", "F")
hline(560, 976, 486)

field(560, 498, "Surname / Nom", "ILVES")
field(760, 498, "Given names / Prénoms", "MARA")
field(560, 552, "Nationality / Nationalité", "VESSALIAN")
field(760, 552, "Date of birth", "14 MAR 1989")
field(560, 606, "Place of birth / Lieu de naissance", "PORT ANSELM")
field(760, 606, "Date of issue", "02 JUN 2021")
field(560, 660, "Date of expiry", "02 JUN 2031")
field(760, 660, "Authority / Autorité", "Min. of the Interior", font(F_BOLD, 13))
text(760, 692, "Port Anselm", font(F_BOLD, 13), INK)
hline(560, 976, 724)

# telling detail: visa condition + language column
text(560, 736, "Languages: Vessalian / English", font(F_BOLD, 13), NAVY)
text(560, 762, "Visa condition:", font(F_SANS, 11), (120, 108, 74))
text(560, 780, "Bearer must carry the current tide tables when", font(F_SANS, 12), INK)
text(560, 798, "travelling north of the Anselm Light.", font(F_SANS, 12), INK)
text(560, 824, "Signature of bearer:  Mara Ilves", font(F_SANS, 12), INK_SOFT)
hline(560, 976, 852)

# --- machine-readable zone ---
mrz1 = "P<VESILVES<<MARA<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
mrz2 = "VS0482137<8VES8903142F3106027<<<<<<<<<<<<<<06"
text(560, 866, mrz1, font(F_MONO, 17), INK)
text(560, 894, mrz2, font(F_MONO, 17), INK)
text(768, 936, "This passport is the property of the Republic of Vessalia.", font(F_SANS, 10), INK_SOFT, "ma")
text(768, 954, "If found, return to the Ministry of the Interior, Port Anselm.", font(F_SANS, 10), INK_SOFT, "ma")

out = os.path.join(BASE, "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
