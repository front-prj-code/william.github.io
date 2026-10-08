#!/usr/bin/env python3
"""Generate dark-theme placeholder SVGs for the portfolio grid.

These are abstract UI wireframes, not screenshots of real products.
Replace with real exports when available.
"""
import os
from xml.sax.saxutils import escape

BG1, BG2 = "#202024", "#17171a"
GOLD = "#ffe071"
W, H = 800, 500

# slug, title, category label, accent, layout
ITEMS = [
    ("proj-terminal",  "Spot & Futures Trading Terminal",   "TRADING UI",      "#c2453e", "trading"),
    ("proj-orderbook", "Order Book & Depth Visualisation",  "TRADING UI",      "#c2453e", "orderbook"),
    ("proj-charts",    "Candlestick & Market Data Components", "TRADING UI",   "#c2453e", "charts"),
    ("proj-mobile",    "Mobile Trading App",                "MOBILE",          "#c2453e", "mobile"),
    ("proj-wallet",    "Wallet Connect & Signing Flow",     "WALLET & ASSETS", "#b8892e", "flow"),
    ("proj-deposit",   "Deposit / Withdrawal Centre",       "WALLET & ASSETS", "#b8892e", "table"),
    ("proj-ops",       "Operations & Risk Console",         "ADMIN & RISK",    "#a2603a", "admin"),
    ("proj-audit",     "Withdrawal Approval & Audit Trail", "ADMIN & RISK",    "#a2603a", "audit"),
    ("proj-ds",        "Exchange Design System",            "DESIGN SYSTEM",   "#7a6fbf", "system"),
    ("proj-tokens",    "Tokens, Type Scale & Motion Specs", "DESIGN SYSTEM",   "#7a6fbf", "tokens"),
    ("proj-campaign",  "Overseas Campaign Visuals",         "BRAND & VISUAL",  "#d4713a", "brand"),
    ("proj-identity",  "Brand Identity & Marketing Kit",    "BRAND & VISUAL",  "#d4713a", "brand2"),
    ("proj-metaverse", "Metaverse Space Concept",           "BRAND & VISUAL",  "#d4713a", "metaverse"),
    ("proj-ai",        "AI Knowledge Assistant UI",          "AI PRODUCTS",    "#3f7d8c", "chat"),
    ("proj-aigc",      "AIGC Visual Exploration Pipeline",  "AI PRODUCTS",    "#3f7d8c", "aigc"),
]


def r(x, y, w, h, op, fill="#ffffff", rx=0, stroke=None):
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
         f'fill="{fill}" fill-opacity="{op}"')
    if stroke:
        s += f' stroke="{stroke[0]}" stroke-opacity="{stroke[1]}"'
    return s + '/>'


def txt(x, y, s, size=11, fill="#ffffff", op=0.62, weight="400", ls=0):
    return (f'  <text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" fill-opacity="{op}" '
            f'letter-spacing="{ls}">{escape(s)}</text>')


def bars(x, y, widths, gap=13, h=6, op=0.16):
    return "\n".join(r(x, y + i * gap, w, h, op, rx=3) for i, w in enumerate(widths))


def shell(inner, accent, frame=True):
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">',
        '  <defs>',
        '    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        f'      <stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG2}"/>',
        '    </linearGradient>',
        '    <radialGradient id="glow" cx="0.5" cy="0.35" r="0.72">',
        f'      <stop offset="0%" stop-color="{accent}" stop-opacity="0.22"/>',
        f'      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>',
        '    </radialGradient>',
        '  </defs>',
        f'  <rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'  <rect width="{W}" height="{H}" fill="url(#glow)"/>',
    ]
    if frame:
        s += [
            r(60, 46, 680, 352, 0.035, rx=12,
              stroke=("#ffffff", 0.10)),
            '  <line x1="60" y1="80" x2="740" y2="80" stroke="#ffffff" stroke-opacity="0.10"/>',
            '  <circle cx="82" cy="63" r="4" fill="#ffffff" fill-opacity="0.18"/>',
            '  <circle cx="98" cy="63" r="4" fill="#ffffff" fill-opacity="0.18"/>',
            '  <circle cx="114" cy="63" r="4" fill="#ffffff" fill-opacity="0.18"/>',
        ]
    s.append(inner)
    s.append('</svg>')
    return "\n".join(s)


def trading(a):
    p = [bars(88, 108, [92, 74, 86, 66, 80, 58, 88, 70], 22, 7),
         r(212, 104, 300, 150, 0.05, rx=8),
         f'  <polyline points="226,224 258,196 286,208 316,168 346,186 376,142 406,158 436,124 466,138 496,112" '
         f'fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>',
         r(212, 266, 300, 12, 0.06, rx=4),
         r(212, 266, 188, 12, 0.35, a, rx=4),
         bars(212, 296, [300, 244, 268], 18, 7),
         bars(534, 104, [150, 172, 150, 172, 150, 172, 150], 21, 7, 0.13),
         r(534, 272, 158, 40, 0.28, a, rx=8)]
    return "\n".join(p)


def orderbook(a):
    p = [txt(212, 104, "ASKS", 10, "#ffffff", 0.4, ls=2)]
    for i in range(5):
        y = 116 + i * 20
        w = 210 - i * 26
        p += [r(212, y, w, 13, 0.14, a, rx=3), r(560, y, 90 - i * 8, 8, 0.13, rx=3)]
    p += [r(212, 262, 300, 3, 0.12, a, rx=1), txt(212, 282, "BIDS", 10, "#ffffff", 0.4, ls=2)]
    for i in range(5):
        y = 294 + i * 20
        w = 140 + i * 26
        p += [r(212, y, w, 13, 0.14, a, rx=3), r(560, y, 90 + i * 8, 8, 0.13, rx=3)]
    p += [bars(88, 108, [92, 74, 86, 66, 80, 58, 88], 22, 7)]
    return "\n".join(p)


def charts(a):
    p = [bars(88, 108, [130], 0, 8)]
    d = "M104,232 L152,196 L200,214 L248,164 L296,186 L344,138 L392,158 L440,112 L488,132 L536,96 L584,118 L632,86"
    p += [r(88, 132, 624, 190, 0.04, rx=8),
          f'  <polyline points="{d}" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>']
    for i in range(6):
        p.append(r(104 + i * 104, 132, 1, 190, 0.07))
    p += [f'  <line x1="88" y1="348" x2="712" y2="348" stroke="#ffffff" stroke-opacity="0.10"/>',
          bars(104, 362, [70, 54, 84, 62, 48], 0, 7, 0.13)]
    for i, (cx, cy) in enumerate([(200, 214), (440, 112), (632, 86)]):
        p += [f'  <circle cx="{cx}" cy="{cy}" r="6" fill="{a}" fill-opacity="0.85"/>',
              f'  <circle cx="{cx}" cy="{cy}" r="13" fill="{a}" fill-opacity="0.20"/>']
    return "\n".join(p)


def mobile(a):
    p = [r(330, 98, 150, 272, 0.045, rx=16).replace('/>', ' stroke="#ffffff" stroke-opacity="0.12"/>'),
         r(386, 104, 38, 5, 0.2, rx=2.5),
         bars(350, 130, [110, 66, 90], 16, 6),
         f'  <polyline points="350,224 374,200 396,212 420,178 442,190 462,162" fill="none" '
         f'stroke="{a}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>',
         r(350, 240, 112, 26, 0.26, a, rx=6),
         bars(350, 282, [112, 92, 112, 74], 16, 6, 0.13),
         bars(88, 128, [116, 92, 108, 84, 110, 96], 20, 7),
         bars(586, 128, [116, 96, 110, 88, 104, 92], 20, 7)]
    return "\n".join(p)


def flow(a):
    steps = ["Connect", "Select", "Quote", "Confirm", "Sign", "Broadcast", "Recover"]
    p = []
    for i, s in enumerate(steps):
        cx = 132 + i * 90
        fill = (f'fill="{a}" fill-opacity="0.30"', 0.62) if i % 2 == 0 else ('fill="#ffffff" fill-opacity="0.07"', 0.55)
        p.append(f'  <rect x="{cx-34}" y="176" width="68" height="46" rx="9" {fill[0]} '
                 f'stroke="#ffffff" stroke-opacity="0.10"/>')
        p.append(txt(cx, 204, s, 10.5, "#ffffff", fill[1]))
        if i < len(steps) - 1:
            p += [f'  <line x1="{cx+36}" y1="199" x2="{cx+52}" y2="199" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1.5"/>',
                  f'  <polyline points="{cx+47},195 {cx+52},199 {cx+47},203" fill="none" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1.5"/>']
    p += [bars(88, 264, [624], 0, 7, 0.06), bars(88, 292, [300, 220], 18, 7, 0.13),
          r(88, 340, 150, 36, 0.26, a, rx=8)]
    return "\n".join(p)


def _rows(a, n=5, status=True):
    p = []
    for i in range(n):
        y = 134 + i * 42
        p += [r(88, y, 624, 34, 0.055 if i % 2 == 0 else 0.03, rx=7),
              r(102, y + 13, 86, 8, 0.16, rx=4),
              r(220, y + 13, 140, 8, 0.10, rx=4),
              r(392, y + 13, 70, 8, 0.10, rx=4)]
        if status:
            p.append(r(500, y + 10, 62, 15, 0.30, a, rx=7.5))
        p.append(r(600 if status else 520, y + 13, 96, 8, 0.10, rx=4))
    return p


def table(a):
    return "\n".join([bars(88, 108, [130], 0, 8)] + _rows(a))


def audit(a):
    p = [bars(88, 108, [180], 0, 8)]
    for i in range(4):
        y = 140 + i * 52
        p += [f'  <line x1="104" y1="{y}" x2="104" y2="{y+40}" stroke="#ffffff" stroke-opacity="0.12"/>',
              f'  <circle cx="104" cy="{y+8}" r="6" fill="{a}" fill-opacity="0.75"/>',
              r(126, y + 2, 150, 8, 0.17, rx=4),
              r(126, y + 20, 330, 7, 0.09, rx=3.5),
              r(600, y + 4, 112, 16, 0.22, a, rx=8)]
    p += [r(88, 356, 624, 1, 0.08)]
    return "\n".join(p)


def admin(a):
    p = [bars(88, 108, [150], 0, 8)]
    for i in range(4):
        x = 88 + i * 158
        p += [r(x, 132, 146, 76, 0.05, rx=9, stroke=("#ffffff", 0.09)),
              r(x + 16, 150, 58, 7, 0.13, rx=3.5),
              r(x + 16, 170, 92, 14, 0.42, a, rx=4)]
    for i in range(3):
        y = 226 + i * 46
        p += [r(88, y, 624, 38, 0.045 if i % 2 == 0 else 0.028, rx=7),
              r(104, y + 15, 12, 12, 0.55, a, rx=3) if i == 0 else r(104, y + 15, 12, 12, 0.16, rx=3),
              r(130, y + 16, 210, 8, 0.12, rx=4),
              r(370, y + 16, 90, 8, 0.09, rx=4),
              r(492, y + 12, 60, 15, 0.28, a, rx=7.5),
              r(600, y + 16, 96, 8, 0.09, rx=4)]
    return "\n".join(p)


def system(a):
    p = [bars(88, 118, [120], 0, 8)]
    for row in range(2):
        for col in range(5):
            x = 88 + col * 128
            y = 142 + row * 96
            hot = (row * 5 + col) % 3 == 0
            p += [r(x, y, 110, 78, 0.05, rx=9).replace('/>', ' stroke="#ffffff" stroke-opacity="0.09"/>'),
                  f'  <circle cx="{x+44}" cy="{y+22}" r="12" fill="{"#ffffff" if not hot else a}" fill-opacity="{0.16 if not hot else 0.62}"/>',
                  r(x + 16, y + 46, 78, 7, 0.15, rx=3.5),
                  r(x + 16, y + 59, 52, 6, 0.09, rx=3)]
    p.append(txt(400, 378, "TOKENS  ·  COMPONENTS  ·  STATES  ·  PLATFORMS", 11, "#ffffff", 0.3, ls=1.5))
    return "\n".join(p)


def tokens(a):
    p = [bars(88, 112, [110], 0, 8)]
    for i in range(6):
        p.append(r(88 + i * 68, 138, 58, 58, 0.85 if i < 3 else 0.55,
                   a if i < 3 else "#ffffff", rx=12))
    p += [bars(88, 220, [140], 0, 7)]
    sizes = [22, 18, 14, 11, 9]
    for i, s in enumerate(sizes):
        y = 252 + i * 30
        p += [r(88, y - 12, 24, 24, 0.07, rx=5),
              txt(100, y + 5, "Aa", s, "#ffffff", 0.55),
              r(130, y - 6, 150 - i * 16, 9, 0.12, rx=4.5)]
    for i in range(3):
        y = 250 + i * 40
        p += [f'  <path d="M470,{y+12} C510,{y-8} 570,{y+30} 620,{y+6}" fill="none" stroke="{a}" '
              f'stroke-width="2" opacity="0.6" stroke-linecap="round"/>',
              r(650, y, 62, 26, 0.10, rx=6)]
    return "\n".join(p)


def brand(a):
    p = [r(60, 60, 340, 380, 0.05, rx=14, stroke=(a, 0.35)),
         r(96, 104, 150, 10, 0.28, rx=5),
         r(96, 128, 96, 10, 0.14, rx=5),
         f'  <circle cx="230" cy="290" r="72" fill="none" stroke="{a}" stroke-opacity="0.55" stroke-width="2"/>',
         f'  <circle cx="230" cy="290" r="44" fill="{a}" fill-opacity="0.22"/>',
         txt(230, 296, "W", 44, GOLD, 0.9, weight="600"),
         r(430, 60, 310, 178, 0.05, rx=14),
         r(430, 262, 310, 178, 0.05, rx=14)]
    for i in range(3):
        p.append(r(452, 84 + i * 46, 200 - i * 30, 9, 0.14, rx=4.5))
    for i in range(3):
        p.append(r(452 + i * 96, 286, 84, 60, 0.30 if i == 1 else 0.10, a if i == 1 else "#ffffff", rx=9))
    p += [r(452, 366, 236, 8, 0.11, rx=4), r(452, 386, 180, 8, 0.08, rx=4)]
    return "\n".join(p)


def brand2(a):
    p = [r(60, 46, 680, 352, 0.04, rx=12)]
    p += [r(88, 78, 180, 8, 0.16, rx=4)]
    for i in range(3):
        x = 88 + i * 212
        p += [r(x, 110, 190, 130, 0.06, rx=10).replace('/>', ' stroke="#ffffff" stroke-opacity="0.09"/>'),
              f'  <circle cx="{x+50}" cy="{150}" r="22" fill="{a}" fill-opacity="{0.55 - i*0.14}"/>',
              r(x + 24, 190, 120, 8, 0.13, rx=4),
              r(x + 24, 206, 82, 7, 0.09, rx=3.5)]
    p += [r(88, 262, 190, 116, 0.06, rx=10),
          r(300, 262, 412, 50, 0.05, rx=10),
          r(300, 328, 412, 50, 0.05, rx=10),
          r(320, 280, 160, 13, 0.22, a, rx=6),
          r(320, 346, 120, 13, 0.12, rx=6)]
    return "\n".join(p)


def metaverse(a):
    p = [r(60, 46, 680, 352, 0.03, rx=12)]
    for i in range(5):
        y = 300 - i * 18
        w = 480 - i * 62
        p.append(f'  <polygon points="{400-w//2},{y} {400+w//2},{y} {400+w//2-40},{y+40} {400-w//2+40},{y+40}" '
                 f'fill="{a}" fill-opacity="{0.05 + i*0.045}" stroke="{a}" stroke-opacity="0.28"/>')
    for i, (x, y, s) in enumerate([(220, 196, 26), (300, 164, 34), (400, 140, 46), (500, 164, 34), (580, 196, 26)]):
        p += [r(x - s // 2, y, s, s, 0.30 if i == 2 else 0.16, a, rx=6),
              r(x - s // 2 + 6, y + s + 8, s - 12, 5, 0.10, rx=2.5)]
    p += [r(60, 340, 680, 1, 0.08),
          r(88, 364, 120, 8, 0.13, rx=4),
          r(640, 364, 72, 8, 0.13, rx=4),
          txt(400, 368, "SPATIAL  LAYOUT  ·  LIGHTING  ·  AVATAR  PRESENCE", 10, "#ffffff", 0.3, ls=1.6)]
    return "\n".join(p)


def chat(a):
    return "\n".join([
        r(88, 108, 176, 252, 0.04, rx=9).replace('/>', ' stroke="#ffffff" stroke-opacity="0.09"/>'),
        bars(104, 128, [110, 84, 120, 92, 104, 116], 22, 7, 0.14),
        r(284, 108, 428, 252, 0.03, rx=9).replace('/>', ' stroke="#ffffff" stroke-opacity="0.08"/>'),
        r(304, 132, 252, 44, 0.07, rx=9),
        bars(318, 148, [196, 140], 15, 6, 0.15),
        r(392, 192, 300, 66, 0.20, a, rx=9),
        bars(408, 210, [244, 200, 168], 15, 6, 0.2),
        r(304, 274, 170, 30, 0.30, a, rx=8),
        r(304, 318, 380, 26, 0.05, rx=13).replace('/>', ' stroke="#ffffff" stroke-opacity="0.10"/>'),
    ])


def aigc(a):
    p = [bars(88, 112, [148], 0, 8)]
    for row in range(2):
        for col in range(5):
            x = 88 + col * 128
            y = 140 + row * 88
            p += [r(x, y, 112, 72, 0.05 + ((row * 5 + col) % 4) * 0.016, rx=8),
                  f'  <circle cx="{x+56}" cy="{y+36}" r="{18 + (col % 3) * 5}" '
                  f'fill="{a}" fill-opacity="{0.10 + (col % 4) * 0.045}"/>']
    p += [f'  <line x1="88" y1="322" x2="712" y2="322" stroke="{a}" stroke-opacity="0.3" stroke-dasharray="5 5"/>',
          r(88, 344, 624, 8, 0.07, rx=4),
          r(88, 344, 396, 8, 0.30, a, rx=4),
          txt(400, 380, "PROMPT  ·  EXPLORE  ·  SELECT  ·  REFINE", 10, "#ffffff", 0.3, ls=1.6)]
    return "\n".join(p)


LAYOUTS = {
    "trading": trading, "orderbook": orderbook, "charts": charts, "mobile": mobile,
    "flow": flow, "table": table, "admin": admin, "audit": audit,
    "system": system, "tokens": tokens, "brand": brand, "brand2": brand2,
    "metaverse": metaverse, "chat": chat, "aigc": aigc,
}


def main():
    out = "assets/images/projects"
    os.makedirs(out, exist_ok=True)
    for slug, title, cat, accent, layout in ITEMS:
        inner = LAYOUTS[layout](accent)
        svg = shell(inner, accent, frame=layout not in ("brand", "metaverse"))
        svg = svg.replace("</svg>",
            txt(400, 438, title, 24, "#ffffff", 1, weight="600") + "\n"
            + txt(400, 466, cat, 12, GOLD, 0.8, ls=2) + "\n</svg>")
        path = os.path.join(out, slug + ".svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("%-44s %6d bytes" % (path, os.path.getsize(path)))
    print("\n共 %d 张" % len(ITEMS))


if __name__ == "__main__":
    main()
