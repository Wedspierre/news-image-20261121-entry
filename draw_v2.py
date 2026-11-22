# draw_v2.py — renders entry.png for news-image-20261121 v2 from scratch.
# Front-page design: masthead + market ticker + COP31 lead + 6 story cards
# + 28 one-line briefs = 35 dated stories, 6 continents. All facts verified
# against wire/news reporting of Saturday 21 November 2026 (see README.md).
# Run: python3 draw_v2.py  -> writes entry.png (1024x1024, < 1 MiB).

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (20, 50, 79)
GREY = (90, 88, 82)
RULE = (60, 58, 52)

F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
def icon_globe_sun(d, x, y, s, ink, accent):
    # globe: circle + meridians, sun rays upper right
    d.ellipse([x, y, x + s, y + s], outline=ink, width=4)
    d.ellipse([x + s * 0.30, y + 4, x + s * 0.70, y + s - 4], outline=ink, width=3)
    d.line([x + 4, y + s * 0.5, x + s - 4, y + s * 0.5], fill=ink, width=3)
    d.arc([x + s * 0.12, y + s * 0.18, x + s * 0.88, y + s * 0.82], 200, 340, fill=ink, width=3)
    cx, cy, r = x + s * 0.80, y + s * 0.16, s * 0.11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1, y1 = cx + math.cos(a) * r * 1.45, cy + math.sin(a) * r * 1.45
        x2, y2 = cx + math.cos(a) * r * 1.95, cy + math.sin(a) * r * 1.95
        d.line([x1, y1, x2, y2], fill=accent, width=3)


def icon_chart(d, x, y, s, ink, accent):
    d.line([x + 4, y + s - 6, x + s - 4, y + s - 6], fill=ink, width=3)
    pts = [(x + 8, y + s * 0.22), (x + s * 0.35, y + s * 0.38),
           (x + s * 0.55, y + s * 0.30), (x + s * 0.80, y + s * 0.72)]
    d.line(pts, fill=accent, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 14, ey - 2), (ex - 4, ey - 14)], fill=accent)


def icon_bridge(d, x, y, s, ink, accent):
    d.line([x + 4, y + s * 0.62, x + s - 4, y + s * 0.62], fill=ink, width=4)
    for i, cx in enumerate([x + s * 0.22, x + s * 0.5, x + s * 0.78]):
        d.arc([cx - s * 0.16, y + s * 0.62, cx + s * 0.16, y + s * 0.94],
              180, 360, fill=ink, width=3)
    # explosion starburst above the middle arch
    cx, cy, r = x + s * 0.5, y + s * 0.28, s * 0.10
    import math
    for k in range(8):
        a = math.radians(k * 45)
        d.line([cx + math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6,
                cx + math.cos(a) * r * 1.7, cy + math.sin(a) * r * 1.7],
               fill=accent, width=3)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=accent)


def icon_skyline(d, x, y, s, ink, accent):
    # towers + intercept dome arc
    d.rectangle([x + 6, y + s * 0.45, x + s * 0.28, y + s - 6], fill=ink)
    d.rectangle([x + s * 0.34, y + s * 0.25, x + s * 0.58, y + s - 6], fill=ink)
    d.rectangle([x + s * 0.64, y + s * 0.55, x + s * 0.88, y + s - 6], fill=ink)
    d.polygon([(x + s * 0.34, y + s * 0.25), (x + s * 0.46, y + s * 0.12),
               (x + s * 0.58, y + s * 0.25)], fill=ink)
    d.arc([x + s * 0.05, y - s * 0.05, x + s * 0.95, y + s * 0.75],
          200, 340, fill=accent, width=4)


def icon_mountain(d, x, y, s, ink, accent):
    d.polygon([(x + 4, y + s - 8), (x + s * 0.38, y + s * 0.30),
               (x + s * 0.62, y + s - 8)], fill=ink)
    d.polygon([(x + s * 0.42, y + s - 8), (x + s * 0.72, y + s * 0.48),
               (x + s - 4, y + s - 8)], fill=ink)
    for yy in (y + s * 0.72, y + s * 0.84):
        pts = []
        for i in range(9):
            px = x + 4 + i * (s - 8) / 8
            py = yy + (6 if i % 2 == 0 else -6)
            pts.append((px, py))
        d.line(pts, fill=accent, width=3)


def icon_badge(d, x, y, s, ink, accent):
    d.polygon([(x + s * 0.5, y + 4), (x + s - 4, y + s * 0.22),
               (x + s * 0.82, y + s - 6), (x + s * 0.5, y + s * 0.82),
               (x + s * 0.18, y + s - 6), (x + 4, y + s * 0.22)],
              outline=ink, width=4)
    cx, cy, r = x + s * 0.5, y + s * 0.46, s * 0.16
    import math
    star = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.45
        star.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(star, fill=accent)


def icon_scales(d, x, y, s, ink, accent):
    cx = x + s * 0.5
    d.line([cx, y + s * 0.12, cx, y + s * 0.85], fill=ink, width=4)
    d.line([x + s * 0.14, y + s * 0.28, x + s * 0.86, y + s * 0.28], fill=ink, width=4)
    d.line([x + s * 0.18, y + s * 0.88, x + s * 0.82, y + s * 0.88], fill=ink, width=4)
    for px in (x + s * 0.14, x + s * 0.86):
        d.line([px, y + s * 0.28, px - s * 0.10, y + s * 0.52], fill=ink, width=3)
        d.line([px, y + s * 0.28, px + s * 0.10, y + s * 0.52], fill=ink, width=3)
        d.arc([px - s * 0.11, y + s * 0.44, px + s * 0.11, y + s * 0.62],
              0, 180, fill=accent, width=3)
    d.ellipse([cx - 5, y + s * 0.07, cx + 5, y + s * 0.07 + 10], fill=accent)


ICONS = {"globe": icon_globe_sun, "chart": icon_chart, "bridge": icon_bridge,
         "skyline": icon_skyline, "mountain": icon_mountain,
         "badge": icon_badge, "scales": icon_scales}

# ---------------------------------------------------------------- content
LEAD = {
    "kicker": "CLIMATE  ·  ANTALYA, TURKEY",
    "headline": "COP31 IN OVERTIME",
    "summary": ("Climate talks run past their Friday deadline as the draft drops "
                "all fossil-fuel language; Panama vows to object."),
    "accent": (30, 107, 58),
    "icon": "globe",
}

CARDS = [
    {"kicker": "MARKETS  ·  NEW YORK", "headline": "WALL STREET MELTDOWN",
     "summary": "S&P 500 −3.7%, Nasdaq −5.3%; Nvidia −14% as the SEC probes its accounts.",
     "accent": (163, 22, 33), "icon": "chart"},
    {"kicker": "WAR  ·  KYIV, UKRAINE", "headline": "RUSSIA HITS KYIV BRIDGES",
     "summary": "110+ missiles and 400 drones strike three bridges; a hit on Kryvyi Rih kills 2.",
     "accent": (58, 58, 58), "icon": "bridge"},
    {"kicker": "MIDDLE EAST  ·  RIYADH", "headline": "MISSILES OVER RIYADH",
     "summary": "Saudi defences down three Houthi missiles aimed at the capital; a tower is hit.",
     "accent": (154, 107, 18), "icon": "skyline"},
    {"kicker": "QUAKE  ·  JUNÍN, PERU", "headline": "PERU SHAKEN BY M6.7 QUAKE",
     "summary": "A deep quake rattles the Andes and is felt in Lima; no deaths reported.",
     "accent": (15, 107, 107), "icon": "mountain"},
    {"kicker": "CRIME  ·  SINALOA, MEXICO", "headline": "MEXICO NABS CARTEL BOSS",
     "summary": "FBI most-wanted Fausto Isidro Meza Flores captured in Guasave; violence follows.",
     "accent": (20, 50, 79), "icon": "badge"},
    {"kicker": "JUSTICE  ·  THE HAGUE", "headline": "MYANMAR GUILTY OF GENOCIDE",
     "summary": "World court finds Myanmar committed genocide against the Rohingya; Myanmar objects.",
     "accent": (91, 45, 142), "icon": "scales"},
]

# (region tag, one line, <= 60 chars) — 28 briefs; 7 lead stories + 28 = 35.
BRIEFS = [
    ("UK–EU", "Food, carbon and youth-mobility deals signed"),
    ("SPACE", "BepiColombo reaches Mercury orbit at last"),
    ("HEALTH", "Cancer pill leaves tumours undetectable in 1 in 12"),
    ("EUROPE", "Gen Z walkouts in 25 countries on Youth Day"),
    ("DENMARK", "Parliament backs US–Greenland deal, 109–0"),
    ("N. KOREA", "IAEA: uranium enrichment expanding at Yongbyon"),
    ("MARKETS", "Anthropic shares slide on day two to $88.91"),
    ("HORMUZ", "Tankers hit; six attacks on shipping in a week"),
    ("GAZA", "Strike kills three in World Central Kitchen vehicle"),
    ("FINLAND", "Drones hit Russian cargo ship; crew evacuated"),
    ("YEMEN", "Houthis: coalition carried out 71 strikes in a day"),
    ("GENEVA", "Autonomous-weapons talks end, no binding rules"),
    ("INDIA", "Akvan aftermath: 300,000 evacuated before landfall"),
    ("BRAZIL", "Mosquitoes with bacterium cut dengue cases 69%"),
    ("USA", "Loses measles elimination status"),
    ("CERN", "First evidence of an ultra-rare particle decay"),
    ("LONDON", "Princess of Wales announces she is in remission"),
    ("ETHIOPIA", "700,000 displaced in the south"),
    ("USA", "Trump curbs contractors' disclosures to Congress"),
    ("USA", "Washington presses Kyiv for January peace deal"),
    ("EU", "€1bn more military aid for Ukraine approved"),
    ("FRANCE", "Police sentenced over racist beating of Zecler"),
    ("USA", "Man convicted of starting deadly Palisades fire"),
    ("USA", "Indian man sentenced over plot to kill Sikh leader"),
    ("CRYPTO", "Bitcoin dips to $55,326, recovers past $60,000"),
    ("USA", "Fed: markets price near-certain December rate rise"),
    ("SAMOA", "US offers first deep-sea mining licences near Samoa"),
    ("USA", "Senate Democrats move to cut Iran-operation funds"),
]

TICKER = "S&P 500  −3.7%      NASDAQ  −5.3%      NIKKEI  −5.1%      KOSPI  −5.2%      BITCOIN  above $60,000"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double border
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([15, 15, W - 16, H - 16], outline=RULE, width=1)

    # ---- masthead
    f_title = font(F_SERIF_B, 58)
    text_center(d, W // 2, 30, "THE WORLD IN ONE DAY", f_title, INK)
    f_date = font(F_SANS_B, 28)
    text_center(d, W // 2, 96, "SATURDAY  21  NOVEMBER  2026", f_date, RED)
    f_sub = font(F_SANS_B, 16)
    text_center(d, W // 2, 130, "35 STORIES  ·  6 CONTINENTS  ·  ONE DAY", f_sub, NAVY)
    d.line([28, 152, W - 28, 152], fill=INK, width=2)

    # ---- ticker band
    d.rectangle([28, 160, W - 28, 188], fill=NAVY)
    f_tick = font(F_SANS_B, 15)
    text_center(d, W // 2, 166, TICKER, f_tick, (255, 255, 255))

    # ---- lead story
    lx, ly, lw, lh = 28, 198, W - 56, 148
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 28], fill=LEAD["accent"])
    f_kick = font(F_SANS_B, 14)
    d.text((lx + 12, ly + 6), LEAD["kicker"], font=f_kick, fill=(255, 255, 255))
    f_h1 = font(F_SERIF_B, 40)
    d.text((lx + 12, ly + 38), LEAD["headline"], font=f_h1, fill=INK)
    f_sum = font(F_SANS, 17)
    lines = wrap(d, LEAD["summary"], f_sum, 620)
    yy = ly + 92
    for ln in lines:
        d.text((lx + 12, yy), ln, font=f_sum, fill=INK)
        yy += 22
    # lead icon, right side
    ix, iy, isz = lx + lw - 132, ly + 34, 108
    d.rounded_rectangle([ix - 8, iy - 6, ix + isz + 8, iy + isz + 6],
                        radius=10, outline=LEAD["accent"], width=2)
    ICONS[LEAD["icon"]](d, ix, iy, isz, INK, LEAD["accent"])

    # ---- six cards, 2 rows x 3 cols
    cw, ch, gap = 312, 150, 16
    f_ch = font(F_SERIF_B, 21)
    f_cs = font(F_SANS, 14)
    for idx, c in enumerate(CARDS):
        col, row = idx % 3, idx // 3
        x = 28 + col * (cw + gap)
        y = 360 + row * (ch + 14)
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=2)
        d.rectangle([x, y, x + cw, y + 26], fill=c["accent"])
        d.text((x + 10, y + 5), c["kicker"], font=f_kick, fill=(255, 255, 255))
        # icon top-right of headline zone
        isz = 46
        ICONS[c["icon"]](d, x + cw - isz - 10, y + 34, isz, INK, c["accent"])
        hl_lines = wrap(d, c["headline"], f_ch, cw - isz - 24)
        hy = y + 34
        for ln in hl_lines[:2]:
            d.text((x + 10, hy), ln, font=f_ch, fill=INK)
            hy += 25
        sl_lines = wrap(d, c["summary"], f_cs, cw - 20)
        sy = y + 34 + 50
        for ln in sl_lines[:3]:
            d.text((x + 10, sy), ln, font=f_cs, fill=(40, 40, 40))
            sy += 18

    # ---- brief section
    by = 688
    f_bh = font(F_SANS_B, 17)
    d.text((28, by), "THE DAY IN BRIEF", font=f_bh, fill=INK)
    d.line([28, by + 24, W - 28, by + 24], fill=INK, width=2)
    f_bt = font(F_SANS_B, 14)
    f_bl = font(F_SANS, 14)
    col_w = 468
    ly0 = by + 34
    for i, (tag, line) in enumerate(BRIEFS):
        col = i // 14
        row = i % 14
        x = 28 + col * (col_w + 24)
        y = ly0 + row * 19
        tag_txt = tag + " — "
        d.text((x, y), tag_txt, font=f_bt, fill=RED)
        tw = d.textlength(tag_txt, font=f_bt)
        d.text((x + tw, y), line, font=f_bl, fill=INK)

    # ---- footer
    f_ft = font(F_SANS_I, 12)
    text_center(d, W // 2, 992,
                "Events of Saturday 21 November 2026, as reported that day",
                f_ft, GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
