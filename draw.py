#!/usr/bin/env python3
"""Render the front page for Saturday 21 November 2026.

Every story in this build was checked against reporting dated Saturday
21 November 2026 (verification run on 22 November 2026). Items whose only
coverage fell on 19 or 20 November were dropped and replaced with genuine
21 November stories. The layout adds the structure a one-day paper needs:
a UTC timeline, a pin map of where the news happened, a region tag on every
story, and an explicit date-checked line.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
INK = (17, 17, 17)
MUTE = (96, 96, 96)
RED = (178, 0, 0)
RULE = (198, 198, 198)
GRID = (228, 228, 228)
LAND = (236, 236, 236)
LANDLINE = (200, 200, 200)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data

DAY = "SATURDAY  ·  21 NOVEMBER 2026"
TITLE = "THE WORLD TODAY"

# kicker, headline, detail, colour, region
LEADS = [
    ("MIDDLE EAST",
     "Saudi defences down 3 missiles over Riyadh",
     "Sirens wake the capital early Saturday; a Houthi drone is downed "
     "hours later and the coalition hits Hodeidah port.",
     (178, 0, 0), "ME"),
    ("ENTERTAINMENT",
     "GTA VI makes $3.79bn in a day",
     "Take-Two calls it the biggest entertainment launch ever - 32.5m "
     "copies pre-sold, 132m hours watched on day one.",
     (138, 90, 0), "NA"),
    ("SCIENCE",
     "Riemann proof checks out",
     "Lean verifiers confirm Alp\u00f6ge's proof on Saturday - 17m lines of "
     "code checked after the 20 Nov claim.",
     (106, 27, 154), "GL"),
]

# name, colour, glyph kind, [(bold, rest, region)]
SECTIONS = [
    ("WAR & CONFLICT", (178, 0, 0), "star", [
        ("Rutte: NATO will defend Poland",
         "visits Warsaw after missiles land", "EU"),
        ("NATO council to meet Monday",
         "called over the Poland incursion", "EU"),
        ("Houthi drone downed over Saudi south",
         "04:24 AST; coalition hits Hodeidah", "ME"),
        ("Israeli strikes kill Palestinians",
         "in Gaza; West Bank unrest grows", "ME"),
        ("Iran downs a US MQ-9 drone",
         "over Hormuz, its 58th", "ME"),
        ("Russian strike kills boy, 7",
         "double-tap hit on Kryvyi Rih", "EU"),
        ("Russian cargo ship hit by drones",
         "in Gulf of Finland", "EU"),
        ("Russia says 275 drones downed",
         "overnight, from Belgorod to Pskov", "EU"),
    ]),
    ("DIPLOMACY & POLITICS", (32, 56, 100), "circles", [
        ("ANC falls to 31% in local polls",
         "worst since 1994; talks to 27 Nov", "AF"),
        ("Zelensky calls Putin a 'killer'",
         "after Trump calls him a friend", "EU"),
        ("Streeting brands Putin a 'killer'",
         "on a visit to Kyiv", "EU"),
        ("Russian helicopter over Finland",
         "suspected airspace violation", "EU"),
        ("Paris expects next Ukraine round",
         "in Abu Dhabi; no date set", "EU"),
        ("Melania Trump hopes for ceasefire",
         "before Western Christmas", "NA"),
        ("Trump: talks 'stuck in the mud'",
         "like Putin's tanks, he says", "NA"),
    ]),
    ("CLIMATE & DISASTER", (46, 125, 50), "wave", [
        ("COP31 runs past deadline",
         "negotiators meet on Saturday; no deal yet", "EU"),
        ("Hoekstra: no deal beats a weak deal",
         "EU climate chief, 21 Nov", "EU"),
        ("Panama to object to COP deal",
         "without fossil-fuel language", "LA"),
        ("Australia's Bowen steers COP31 talks",
         "co-host seeks a deal in Antalya", "OC"),
        ("6.9 quake shakes Peru",
         "00:09 UTC; felt in Lima; no damage", "LA"),
        ("Indonesia hit by",
         "massive forest fires", "AP"),
        ("Basra power-plant fire",
         "kills at least four", "ME"),
        ("India tainted alcohol",
         "kills 11, hospitalises 180+", "AP"),
    ]),
    ("MARKETS & ECONOMY", (138, 90, 0), "bars", [
        ("S&P 500 6,910 -3.7%",
         "Nasdaq 22,618 -5.3%; Nikkei -5.1%", "NA"),
        ("Gold $3,515 -4.6%",
         "Brent $89.95 -2.2%; gas +14.7%", "EU"),
        ("Bayer pays $7.25bn",
         "to settle Roundup complaints", "EU"),
        ("DAX 24,041 -3.2%",
         "FTSE 9,642 -2.5%; CAC -3.8%", "EU"),
        ("Nvidia craters 14% in a week",
         "from $204 peak to $175.10", "NA"),
        ("VIX soars 33% to 37",
         "fear gauge's biggest weekly jump", "NA"),
        ("Bitcoin below $58,200",
         "worst week since FTX collapse", "NA"),
        ("UK retail sales beat forecasts",
         "+2.3% in Oct vs 1.7% expected", "EU"),
        ("Canada retail sales top forecasts",
         "+1.6% in Oct vs 1.1% expected", "NA"),
        ("Asia rout: Kospi -1.8%",
         "Taiex -1.3%, S&P ASX -2.9%", "AP"),
    ]),
    ("SCIENCE & HEALTH", (106, 27, 154), "atom", [
        ("Cancer pill clears tumours",
         "in 1 in 12 pancreatic patients", "GL"),
        ("BepiColombo reaches Mercury",
         "after 8 years and 10bn km", "EU"),
        ("Voyager 1 a light-day out",
         "24 light-hours from Earth", "NA"),
        ("CERN finds rare decay",
         "3.2-sigma evidence, 1 in 10bn", "EU"),
        ("Europa's sodium cloud",
         "mapped by Keck Observatory", "NA"),
        ("MIT builds AI that respects",
         "physics of chaos", "NA"),
    ]),
    ("TECH & CYBER", (15, 76, 117), "chip", [
        ("FBI database 'hacked'",
         "USDA hit too; outages continue", "NA"),
        ("OpenAI releases GPT-6.2 and Sol",
         "two months after scrapping 6.1", "NA"),
        ("Signal blocks screenshots",
         "so AI agents can't scan chats", "NA"),
        ("Amazon links China to AI attack",
         "AI framework hit imaging app", "NA"),
        ("Microsoft taps Intel for Azure",
         "foundry's first outside customer", "NA"),
    ]),
    ("SPORT", (0, 105, 92), "ball", [
        ("KL Rahul completes SENA set",
         "Test 100s in all four nations", "AP"),
        ("Pakistan beat Sri Lanka",
         "by 8 wickets to clinch Test series", "AP"),
        ("UAE Bulls win Abu Dhabi T10",
         "India A crush Nepal by 306 runs", "AP"),
        ("Nuggets 133-124 Rockets",
         "Lakers edge Kings 106-104", "NA"),
        ("Russell takes Las Vegas GP pole",
         "0.098s clear of Sainz", "NA"),
        ("Alcaraz sweeps ATP Finals group",
         "6-4 6-1 over Cobolli in Turin", "EU"),
    ]),
]

LEFT_SECTIONS = SECTIONS[0:3]
RIGHT_SECTIONS = SECTIONS[3:7]

TIMELINE = [
    ("00:09 UTC", "M6.9 quake hits Peru's Andes; felt in Lima, no damage"),
    ("01:24 UTC", "Saudi defences down a Houthi drone (04:24 AST)"),
    ("MORNING", "Rutte in Warsaw: NATO will defend every inch of Poland"),
    ("AFTERNOON", "COP31 in Antalya: Hoekstra - no deal beats a weak deal"),
    ("20:00 UTC", "Lean verifiers confirm the Riemann proof (15:00 ET)"),
]

# Rough continent outlines, (lon, lat) points, equirectangular.
CONTINENTS = [
    [(-168, 66), (-130, 71), (-95, 80), (-65, 60), (-55, 47), (-75, 35),
     (-80, 25), (-97, 16), (-105, 20), (-120, 32), (-125, 48), (-155, 58)],
    [(-78, 8), (-60, 5), (-40, -5), (-35, -15), (-50, -30), (-65, -45),
     (-70, -55), (-73, -35), (-78, -15)],
    [(-17, 15), (-5, 35), (10, 37), (30, 31), (43, 12), (51, 11),
     (40, -10), (33, -26), (20, -35), (12, -18), (9, 4), (-8, 5)],
    [(-10, 36), (-5, 44), (5, 48), (15, 44), (25, 40), (35, 36),
     (45, 42), (55, 50), (65, 68), (85, 75), (110, 74), (140, 72),
     (170, 66), (175, 62), (160, 55), (145, 40), (130, 33), (120, 25),
     (108, 12), (100, 8), (95, 16), (85, 20), (75, 10), (65, 25),
     (55, 27), (48, 30), (40, 36), (30, 36), (20, 40), (10, 38)],
    [(114, -22), (114, -33), (124, -33), (132, -32), (140, -38),
     (150, -37), (153, -27), (146, -19), (142, -11), (135, -12),
     (129, -14), (122, -17)],
]

# code, lon, lat, label offset (dx, dy)
PINS = [
    ("RY", 46.7, 24.6, (6, -8)),
    ("WA", 21.0, 52.2, (6, -8)),
    ("LI", -77.0, -12.0, (-18, 4)),
    ("AN", 30.7, 36.9, (6, 2)),
    ("NY", -74.0, 40.7, (-18, -8)),
    ("TU", 7.7, 45.1, (8, -10)),
    ("LV", -115.1, 36.2, (-18, 4)),
    ("TK", 139.7, 35.7, (6, -8)),
    ("LO", -0.1, 51.5, (-20, -10)),
    ("PA", 2.35, 48.85, (10, 6)),
    ("GZ", 34.45, 31.5, (-20, 6)),
    ("DE", 77.2, 28.6, (6, 2)),
    ("JB", 28.0, -26.2, (6, 2)),
]

REGION_NAMES = {
    "EU": "EUROPE", "ME": "MIDDLE EAST", "AP": "ASIA-PACIFIC",
    "AF": "AFRICA", "NA": "NORTH AMERICA", "LA": "LATIN AMERICA",
    "OC": "OCEANIA", "GL": "GLOBAL",
}
REGION_SHORT = {
    "EU": "Europe", "ME": "Mideast", "AP": "Asia-Pac", "AF": "Africa",
    "NA": "N America", "LA": "LatAm", "OC": "Oceania", "GL": "Global",
}
REGION_ORDER = ["EU", "ME", "AP", "AF", "NA", "LA", "OC", "GL"]


def story_count():
    return len(LEADS) + sum(len(s[3]) for s in SECTIONS)


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for lead in LEADS:
        counts[lead[4]] += 1
    for sec in SECTIONS:
        for item in sec[3]:
            counts[item[2]] += 1
    return counts


# ---------------------------------------------------------------- helpers

def wrap_tokens(tokens, width, draw):
    """Greedy word wrap over (word, font, fill) tokens. Returns lines."""
    lines, cur, cur_w = [], [], 0.0
    for word, font, fill in tokens:
        ww = draw.textlength(word, font=font)
        space = draw.textlength(" ", font=font) if cur else 0.0
        if cur and cur_w + space + ww > width:
            lines.append(cur)
            cur, cur_w = [(word, font, fill)], ww
        else:
            cur.append((word, font, fill))
            cur_w += space + ww
    if cur:
        lines.append(cur)
    return lines


def draw_tokens_line(draw, x, y, line):
    cx = x
    for word, font, fill in line:
        draw.text((cx, y), word, font=font, fill=fill)
        cx += draw.textlength(word, font=font) + draw.textlength(" ", font=font)
    return cx


def tracked_width(draw, text, font, tracking):
    return sum(draw.textlength(ch, font=font) + tracking for ch in text)


def draw_tracked(draw, x, y, text, font, fill, tracking):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += draw.textlength(ch, font=font) + tracking


def draw_glyph(draw, cx, cy, kind, color):
    s = 7
    if kind == "star":
        p = 0.28
        pts = [(cx, cy - s), (cx + s * p, cy - s * p), (cx + s, cy),
               (cx + s * p, cy + s * p), (cx, cy + s),
               (cx - s * p, cy + s * p), (cx - s, cy),
               (cx - s * p, cy - s * p)]
        draw.polygon(pts, fill=color)
    elif kind == "circles":
        draw.ellipse([cx - s, cy - s + 2, cx + 1, cy + s - 2],
                     outline=color, width=2)
        draw.ellipse([cx - 1, cy - s + 2, cx + s, cy + s - 2],
                     outline=color, width=2)
    elif kind == "wave":
        pts = []
        for i in range(15):
            x = cx - s + i * (2 * s / 14)
            y = cy + (s * 0.55) * (1 if i % 2 == 0 else -1) * (0.4 + 0.6 * abs((i - 7) / 7))
            pts.append((x, y))
        draw.line(pts, fill=color, width=2)
    elif kind == "bars":
        for i, h in enumerate((5, 9, 13)):
            x0 = cx - s + i * 5
            draw.rectangle([x0, cy + s - h, x0 + 3, cy + s], fill=color)
    elif kind == "atom":
        draw.ellipse([cx - s, cy - s // 2, cx + s, cy + s // 2],
                     outline=color, width=2)
        draw.ellipse([cx - s // 2, cy - s, cx + s // 2, cy + s],
                     outline=color, width=2)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)
    elif kind == "chip":
        draw.rectangle([cx - 5, cy - 5, cx + 5, cy + 5],
                       outline=color, width=2)
        for dy in (-3, 0, 3):
            draw.line([cx - 8, cy + dy, cx - 5, cy + dy], fill=color, width=2)
            draw.line([cx + 5, cy + dy, cx + 8, cy + dy], fill=color, width=2)
    elif kind == "ball":
        draw.ellipse([cx - s, cy - s, cx + s, cy + s],
                     outline=color, width=2)
        draw.line([cx - s, cy, cx + s, cy], fill=color, width=2)
        draw.arc([cx - s, cy - s, cx + s, cy + s], 200, 340, fill=color, width=2)


def draw_section_header(draw, x, y, width, name, color, glyph):
    draw_glyph(draw, x + 8, y + 8, glyph, color)
    f_head = f(SANS_B, 13)
    draw.text((x + 20, y), name, font=f_head, fill=color)
    draw.line([x, y + 20, x + width, y + 20], fill=color, width=1)
    return 24


def draw_item(draw, x, y, width, bold, rest, region, color, size):
    """One story: region tag + bold lead + plain rest. Returns height."""
    f_b = f(SANS_B, size)
    f_r = f(SANS, size)
    line_h = size + 3
    tokens = [(region, f_b, color)]
    tokens += [(w, f_b, INK) for w in bold.split(" ")]
    tokens += [(w, f_r, INK) for w in rest.split(" ")]
    lines = wrap_tokens(tokens, width, draw)
    for i, line in enumerate(lines):
        draw_tokens_line(draw, x, y + i * line_h, line)
    return len(lines) * line_h + 2


def measure_columns(size):
    """Heights of the two body columns at a given item font size."""
    probe = Image.new("RGB", (8, 8), BG)
    d = ImageDraw.Draw(probe)
    total = []
    for col in (LEFT_SECTIONS, RIGHT_SECTIONS):
        h = 0
        for name, color, glyph, items in col:
            h += 24
            for bold, rest, region in items:
                h += draw_item(d, 0, 0, 476, bold, rest, region, color, size)
        total.append(h)
    return total


# ---------------------------------------------------------------- layout

MARGIN = 28
CW = W - 2 * MARGIN
COL_W = 476
LEFT_X, RIGHT_X = MARGIN, MARGIN + COL_W + 16

FOOTER_RULE_Y = 962
BODY_TOP = 380
BODY_AVAIL = FOOTER_RULE_Y - BODY_TOP - 4


def main():
    n = story_count()
    counts = region_counts()
    breakdown = "  ·  ".join(
        f"{REGION_SHORT[r]} {counts[r]}" for r in REGION_ORDER if counts[r] > 0)

    # --- pick the largest item font that fits the body area
    chosen = 11
    for size in (14, 13, 12, 11):
        lh, rh = measure_columns(size)
        if max(lh, rh) <= BODY_AVAIL:
            chosen = size
            break
    lh, rh = measure_columns(chosen)
    print(f"stories={n} regions={counts}")
    print(f"body avail={BODY_AVAIL}px left={lh}px right={rh}px "
          f"item font={chosen}pt")

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- masthead
    f_title = f(SERIF_B, 60)
    tw = d.textlength(TITLE, font=f_title)
    d.text(((W - tw) / 2, 14), TITLE, font=f_title, fill=INK)

    f_date = f(SANS_B, 21)
    dw = tracked_width(d, DAY, f_date, 3)
    draw_tracked(d, (W - dw) / 2, 66, DAY, f_date, RED, 3)

    d.rectangle([MARGIN, 94, W - MARGIN, 96], fill=RED)

    # --- meta line + date-checked line
    f_meta = f(SANS_B, 13)
    meta = (f"{n} STORIES  ·  7 SECTIONS  ·  8 REGIONS  ·  "
            "ONE DAY, THE WHOLE WORLD")
    mw = d.textlength(meta, font=f_meta)
    d.text(((W - mw) / 2, 102), meta, font=f_meta, fill=INK)

    f_check = f(SANS_B, 12)
    check = (f"ALL {n} STORIES DATE-CHECKED TO SATURDAY 21 NOVEMBER 2026")
    cw = d.textlength(check, font=f_check)
    d.text(((W - cw) / 2, 122), check, font=f_check, fill=RED)

    d.line([MARGIN, 140, W - MARGIN, 140], fill=RULE, width=1)

    # --- leads (3 columns)
    lead_w = 312
    gap = (CW - 3 * lead_w) // 2
    f_kick = f(SANS_B, 10)
    f_head = f(SANS_B, 15)
    f_det = f(SANS, 11)
    for i, (kicker, head, detail, color, region) in enumerate(LEADS):
        x = MARGIN + i * (lead_w + gap)
        y = 148
        draw_tracked(d, x, y, kicker, f_kick, color, 2)
        y += 16
        tokens = [(w, f_head, INK) for w in head.split(" ")]
        for line in wrap_tokens(tokens, lead_w, d):
            draw_tokens_line(d, x, y, line)
            y += 19
        y += 2
        tokens = [(w, f_det, MUTE) for w in detail.split(" ")]
        for line in wrap_tokens(tokens, lead_w, d):
            draw_tokens_line(d, x, y, line)
            y += 14
        if i < 2:
            d.line([x + lead_w + gap // 2, 148,
                    x + lead_w + gap // 2, 246], fill=RULE, width=1)

    d.line([MARGIN, 254, W - MARGIN, 254], fill=RULE, width=1)

    # --- band: pin map (left) + UTC timeline (right)
    band_y, band_h = 262, 104
    map_x, map_w = MARGIN, 500
    time_x, time_w = MARGIN + 516, 452

    f_band = f(SANS_B, 11)
    d.text((map_x, band_y), "WHERE IT HAPPENED", font=f_band, fill=INK)
    d.text((time_x, band_y), "THE DAY IN UTC", font=f_band, fill=INK)

    # map: equirectangular, lon -180..180, lat -55..78
    mx0, my0 = map_x, band_y + 18
    mx1, my1 = map_x + map_w, band_y + band_h - 16
    mw_px, mh_px = mx1 - mx0, my1 - my0

    def proj(lon, lat):
        x = mx0 + (lon + 180) / 360 * mw_px
        y = my0 + (78 - lat) / 133 * mh_px
        return (x, y)

    for lon in range(-180, 181, 30):
        x = mx0 + (lon + 180) / 360 * mw_px
        d.line([x, my0, x, my1], fill=GRID, width=1)
    for lat in range(-60, 91, 30):
        y = my0 + (78 - lat) / 133 * mh_px
        d.line([mx0, y, mx1, y], fill=GRID, width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LANDLINE)
    f_pin = f(SANS_B, 9)
    for code, lon, lat, (dx, dy) in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + dx, py + dy), code, font=f_pin, fill=INK)

    f_reg = f(SANS, 9)
    d.text((map_x, band_y + band_h - 13), breakdown, font=f_reg, fill=MUTE)

    # timeline entries
    f_time = f(SANS_B, 11)
    f_ttext = f(SANS, 11)
    ty = band_y + 18
    for label, text in TIMELINE:
        d.text((time_x, ty), label, font=f_time, fill=RED)
        lw = d.textlength(label, font=f_time)
        tokens = [(w, f_ttext, INK) for w in text.split(" ")]
        for line in wrap_tokens(tokens, time_w - lw - 10, d):
            draw_tokens_line(d, time_x + lw + 10, ty, line)
            ty += 14
        ty += 4

    d.line([MARGIN, 372, W - MARGIN, 372], fill=RULE, width=1)

    # --- body columns
    for x, col in ((LEFT_X, LEFT_SECTIONS), (RIGHT_X, RIGHT_SECTIONS)):
        y = BODY_TOP
        for name, color, glyph, items in col:
            y += draw_section_header(d, x, y, COL_W, name, color, glyph)
            for bold, rest, region in items:
                y += draw_item(d, x, y, COL_W, bold, rest, region, color,
                               chosen)
            y += 6

    # --- footer
    d.line([MARGIN, FOOTER_RULE_Y, W - MARGIN, FOOTER_RULE_Y],
           fill=RULE, width=1)
    f_num = f(SANS_B, 11)
    nums = ("3 missiles over Riyadh  ·  $3.79bn GTA VI day one  ·  "
            "ANC 31%  ·  M6.9 Peru  ·  17m lines verify Riemann  ·  "
            "VIX 37  ·  BTC $58,200")
    nw = d.textlength(nums, font=f_num)
    d.text(((W - nw) / 2, 970), nums, font=f_num, fill=INK)

    f_src = f(SANS, 10)
    src = ("Sources: Reuters  ·  AP  ·  BBC  ·  WSJ  ·  Scientific American  ·  "
           "USA Today  ·  CNN  ·  Nature  ·  The New York Times")
    sw = d.textlength(src, font=f_src)
    d.text(((W - sw) / 2, 986), src, font=f_src, fill=MUTE)

    f_cred = f(SANS, 9)
    cred = (f"THE WORLD TODAY - Saturday 21 November 2026  ·  {n} stories  ·  "
            "entry.png  ·  make.fun news-image-20261121")
    cw2 = d.textlength(cred, font=f_cred)
    d.text(((W - cw2) / 2, 1000), cred, font=f_cred, fill=MUTE)

    img.save("entry.png")
    img.resize((300, 300)).save("entry-300.png")
    print("saved entry.png + entry-300.png")


if __name__ == "__main__":
    main()
