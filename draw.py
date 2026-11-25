"""Draw the 25 November 2026 world-news infographic.

Writes entry.png (1024x1024) beside this file. Pillow only, no network,
no randomness, no timestamps: the same input always yields the same bytes.
Run:  python3 draw.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

PAPER = (246, 241, 231)
NAVY = (20, 38, 62)
GOLD = (217, 164, 65)
INK = (24, 32, 44)
BODY_GREY = (74, 74, 68)
FAINT = (201, 210, 222)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width pixels."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(text, start_size, min_size, width, max_lines, bold_serif):
    """Largest size in [min_size, start_size] whose wrap fits max_lines."""
    size = start_size
    while size > min_size:
        fnt = SERIF_BOLD(size) if bold_serif else SANS(size)
        lines = wrap(text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = SERIF_BOLD(min_size) if bold_serif else SANS(min_size)
    return fnt, wrap(text, fnt, width)[:max_lines]


def draw_mark(draw, cx, cy, kind, color):
    """Small geometric mark drawn left of a card's kicker."""
    if kind == "chip":
        draw.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=color, width=2)
        draw.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)
        for dx in (-9, 0, 9):
            draw.line([cx + dx, cy - 10, cx + dx, cy - 6], fill=color, width=2)
            draw.line([cx + dx, cy + 6, cx + dx, cy + 10], fill=color, width=2)
    elif kind == "ban":
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=color, width=3)
        draw.line([cx - 6, cy + 6, cx + 6, cy - 6], fill=color, width=3)
    elif kind == "diamond":
        draw.polygon([(cx, cy - 9), (cx + 8, cy), (cx, cy + 9), (cx - 8, cy)],
                     fill=color)
    elif kind == "ship":
        draw.polygon([(cx - 9, cy + 2), (cx + 9, cy + 2), (cx + 6, cy + 8),
                      (cx - 6, cy + 8)], fill=color)
        draw.line([cx, cy - 9, cx, cy + 2], fill=color, width=2)
    elif kind == "feather":
        draw.ellipse([cx - 5, cy - 9, cx + 5, cy + 5], fill=color)
        draw.line([cx, cy + 5, cx + 3, cy + 10], fill=color, width=2)
    else:  # globe
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=color, width=2)
        draw.ellipse([cx - 3, cy - 8, cx + 3, cy + 8], outline=color, width=1)
        draw.line([cx - 8, cy, cx + 8, cy], fill=color, width=1)


def draw_globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
                 outline=color, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    draw.line([cx - r + 8, cy - r + 14, cx + r - 8, cy - r + 14],
              fill=color, width=2)
    draw.line([cx - r + 8, cy + r - 14, cx + r - 8, cy + r - 14],
              fill=color, width=2)


def draw_card(draw, box, story):
    x0, y0, x1, y1 = box
    color = story["color"]
    draw.rounded_rectangle(box, radius=10, fill=WHITE)
    draw.rounded_rectangle([x0, y0, x1, y0 + 18], radius=8, fill=color)
    draw.rectangle([x0, y0 + 9, x1, y0 + 18], fill=color)
    pad = 20
    inner_w = (x1 - x0) - 2 * pad
    kx, ky = x0 + pad, y0 + 30
    draw_mark(draw, kx + 5, ky + 8, story["mark"], color)
    draw.text((kx + 20, ky), story["kicker"], font=SANS_BOLD(16), fill=color)
    head_fnt, head_lines = fit_lines(story["headline"], 28, 24, inner_w, 3, True)
    hy = y0 + 58
    for line in head_lines:
        draw.text((x0 + pad, hy), line, font=head_fnt, fill=INK)
        hy += int(head_fnt.size * 1.22)
    body_fnt, body_lines = fit_lines(story["body"], 17, 15, inner_w, 4, False)
    by = hy + 6
    for line in body_lines:
        draw.text((x0 + pad, by), line, font=body_fnt, fill=BODY_GREY)
        by += int(body_fnt.size * 1.32)


STORIES = [
    {
        "kicker": "US  \u2022  HUAWEI", "mark": "chip", "color": (15, 118, 110),
        "headline": "Huawei found guilty of trade-secret theft by US jury",
        "body": "A Brooklyn jury finds the Chinese tech giant guilty on 10 of "
                "12 counts \u2014 trade secrets and bank fraud \u2014 but clears "
                "it of racketeering.",
    },
    {
        "kicker": "CHINA", "mark": "ban", "color": (154, 52, 18),
        "headline": "China opens probe into Shanghai party chief Chen Jining",
        "body": "The Politburo member is under investigation for suspected "
                "serious violations of discipline and law, Beijing says.",
    },
    {
        "kicker": "COLOMBIA", "mark": "diamond", "color": (159, 18, 57),
        "headline": "Gunmen seize 25 hostages in supermarket siege",
        "body": "Armed men take shoppers and staff hostage at a supermarket; "
                "police surround the store as talks begin.",
    },
    {
        "kicker": "MIDDLE EAST  \u2022  HORMUZ", "mark": "ship",
        "color": (29, 78, 216),
        "headline": "Iran warns ships in Hormuz as US probes 50 hacked vessels",
        "body": "Tehran rules out talks with the US unless seven conditions "
                "are met; Washington investigates Iranian links to the "
                "hacked ships.",
    },
    {
        "kicker": "US  \u2022  THANKSGIVING", "mark": "feather",
        "color": (107, 33, 168),
        "headline": "Trump pardons the Thanksgiving turkeys at the White House",
        "body": "The annual ceremony goes ahead two days before the holiday, "
                "as the US heads into Thanksgiving.",
    },
    {
        "kicker": "UN  \u2022  WOMEN", "mark": "globe", "color": (22, 101, 52),
        "headline": "Five women killed every hour by relatives in 2025, UN says",
        "body": "A new UN report counts a woman killed by a partner or "
                "relative every 12 minutes last year.",
    },
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Header band.
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    draw.rectangle([0, 148, W, 152], fill=GOLD)
    draw.text((28, 16), "THE WORLD IN ONE IMAGE",
              font=SERIF_BOLD(44), fill=WHITE)
    draw.text((28, 74), "WEDNESDAY, 25 NOVEMBER 2026",
              font=SANS_BOLD(25), fill=GOLD)
    draw.text((28, 110), "Six stories that defined the day",
              font=SERIF(20), fill=FAINT)
    draw_globe(draw, 940, 74, 42, GOLD)

    # Six story cards: two columns, three rows.
    margin, gutter = 22, 14
    card_w = (W - 2 * margin - gutter) // 2
    card_h, row_gap = 236, 14
    top = 166
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (card_w + gutter)
        y0 = top + row * (card_h + row_gap)
        draw_card(draw, (x0, y0, x0 + card_w, y0 + card_h), story)

    # "Also" strip.
    draw.rounded_rectangle([22, 916, W - 22, 954], radius=8, fill=NAVY)
    draw.text((40, 926),
              "ALSO   Houthi strike hits Riyadh tower, 11 injured   "
              "\u2022   NATO jets for Poland",
              font=SANS_BOLD(19), fill=WHITE)

    # Footer ticker and source line.
    draw.text((22, 966),
              "Shein to pay $100M in FTC settlement   \u2022   Nvidia shares "
              "fall   \u2022   England beat Australia in 2nd T20I",
              font=SANS(15), fill=BODY_GREY)
    draw.text((22, 990),
              "25 NOVEMBER 2026   \u2022   Sources: AP / Reuters / AFP / "
              "Nikkei / The Guardian   \u2022   Original infographic",
              font=SANS(15), fill=BODY_GREY)

    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
