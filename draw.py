"""Draw the 25 November 2026 world-news image (1024x1024 PNG).

Build tool only: the graded entry is main.py, which copies the
entry.png this script writes. Run: python3 draw.py
Headlines verified 25 Nov 2026 from AP / Reuters / AFP / Nikkei /
The Guardian / Gulf News (all dated/published 25 November 2026).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (16, 42, 67)
NAVY2 = (24, 62, 96)
GOLD = (201, 162, 39)
PAPER = (247, 243, 232)
INK = (24, 28, 32)
MUTED = (84, 90, 96)
LINE = (205, 198, 184)
WHITE = (255, 255, 255)

PANELS = [
    ("US  •  HUAWEI", (14, 110, 110),
     "US jury convicts Huawei\nof trade-secret theft",
     "Brooklyn jury finds the Chinese tech\ngiant guilty on 10 of 12 counts -\ntrade secrets and bank fraud -\nbut acquits it of racketeering."),
    ("CHINA", (150, 66, 32),
     "China probes Shanghai\nparty chief Chen Jining",
     "Politburo member under investigation\nfor suspected serious violations\nof discipline and law, Beijing says."),
    ("COLOMBIA", (122, 32, 48),
     "Gunmen take 25 hostages\nat supermarket siege",
     "Armed men seize shoppers and staff\nat a supermarket; police surround\nthe store as talks begin."),
    ("MIDDLE EAST  •  HORMUZ", (32, 84, 150),
     "Iran warns ships in\nHormuz; US probes\n50 hacked vessels",
     "Tehran rules out US talks unless\nseven conditions are met; Washington\ninvestigates Iranian links to hacked ships."),
    ("US  •  THANKSGIVING", (88, 66, 130),
     "Trump pardons Thanksgiving\nturkeys at White House",
     "The annual ceremony goes ahead\ntwo days before the holiday,\nas the US heads into Thanksgiving."),
    ("UN  •  WOMEN", (36, 110, 62),
     "Five women killed every hour\nby relatives in 2025 - UN",
     "A new UN report counts a woman\nkilled by a partner or relative\nevery 12 minutes last year."),
]

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= width:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def icon(draw, kind, x, y, s, color):
    if kind == 0:  # globe
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.ellipse([x + s * 0.3, y, x + s * 0.7, y + s], outline=color, width=2)
        draw.line([x, y + s / 2, x + s, y + s / 2], fill=color, width=2)
    elif kind == 1:  # chip
        draw.rounded_rectangle([x, y, x + s, y + s], 6, outline=color, width=4)
        draw.rectangle([x + s * 0.28, y + s * 0.28, x + s * 0.72, y + s * 0.72], fill=color)
        for i in range(3):
            px = x + s * (0.25 + i * 0.25)
            draw.line([px, y - 8, px, y], fill=color, width=3)
            draw.line([px, y + s, px, y + s + 8], fill=color, width=3)
    elif kind == 2:  # ship
        draw.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55),
                      (x + s * 0.8, y + s * 0.95), (x + s * 0.2, y + s * 0.95)], fill=color)
        draw.rectangle([x + s * 0.42, y + s * 0.1, x + s * 0.58, y + s * 0.55], fill=color)
        draw.line([x, y + s * 1.05, x + s, y + s * 1.05], fill=color, width=3)
    elif kind == 3:  # ban
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.line([x + s * 0.15, y + s * 0.85, x + s * 0.85, y + s * 0.15], fill=color, width=4)
    elif kind == 4:  # cap / book
        draw.polygon([(x, y + s * 0.45), (x + s / 2, y + s * 0.15),
                      (x + s, y + s * 0.45), (x + s / 2, y + s * 0.75)], fill=color)
        draw.line([x + s * 0.2, y + s * 0.85, x + s * 0.8, y + s * 0.85], fill=color, width=3)
    else:  # flame
        draw.polygon([(x + s / 2, y), (x + s * 0.85, y + s * 0.55),
                      (x + s * 0.65, y + s), (x + s * 0.35, y + s),
                      (x + s * 0.15, y + s * 0.55)], fill=color)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((32, 22), "THE WORLD IN ONE IMAGE", font=font(SERIF_B, 44), fill=WHITE)
    d.text((32, 82), "WEDNESDAY, 25 NOVEMBER 2026", font=font(SANS_B, 26), fill=(232, 196, 90))
    d.text((32, 116), "Six stories that defined the day", font=font(SERIF, 22), fill=(205, 218, 232))
    cx, cy, r = 948, 74, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], outline=GOLD, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    gx, gy = 24, 172
    cw, ch, gap = 476, 222, 20
    for i, (kicker, color, headline, body) in enumerate(PANELS):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], 10, fill=WHITE, outline=LINE, width=2)
        d.rounded_rectangle([x, y, x + cw, y + 8], 4, fill=color)
        d.text((x + 18, y + 20), kicker, font=font(SANS_B, 17), fill=color)
        icon(d, [1, 3, 5, 2, 4, 0][i], x + cw - 62, y + 18, 36, color)
        hl = wrap(d, headline, font(SERIF_B, 27), cw - 36)
        yy = y + 48
        for line in hl:
            d.text((x + 18, yy), line, font=font(SERIF_B, 27), fill=INK)
            yy += 33
        bl = wrap(d, body, font(SANS, 18), cw - 36)
        for line in bl:
            d.text((x + 18, yy + 4), line, font=font(SANS, 18), fill=MUTED)
            yy += 24
    ty = gy + 3 * ch + 2 * gap + 14
    d.rounded_rectangle([24, ty, W - 24, ty + 48], 8, fill=NAVY2)
    d.text((40, ty + 12), "ALSO  Houthi strike hits Riyadh tower, 11 injured  •  NATO jets for Poland",
           font=font(SANS_B, 18), fill=WHITE)
    d.text((40, ty + 60), "Shein to pay $100M in FTC settlement  •  Nvidia shares fall  •  England beat Australia in 2nd T20I",
           font=font(SANS, 17), fill=MUTED)
    d.text((40, ty + 84), "25 NOVEMBER 2026  •  Sources: AP / Reuters / AFP / Nikkei / The Guardian  •  Original infographic",
           font=font(SANS, 15), fill=MUTED)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
