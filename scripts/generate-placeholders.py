#!/usr/bin/env python3
"""Generate placeholder artwork for the portfolio grid.

Each file is a hand-drawn UI mockup, not a screenshot of a real product.
The goal is that a card reads as "a screen from this kind of product"
rather than as an empty dark box.

Constraints learned the hard way:

* Output is 16:9 (800x450). The card CSS is ``aspect-ratio: 16/9`` plus
  ``object-fit: cover``, so a taller image gets its top and bottom cropped.
  An earlier 16:10 set lost its baked-in captions to exactly that crop.
* Contrast decides whether a card looks empty. A saturated colour below
  roughly 0.6 opacity over a dark panel composites to something the eye
  reads as background. Earlier versions used 0.05-0.16 fills and the cards
  looked blank.
* Text inside these files is texture. At grid size an 11px label renders
  around 5px, so structure and colour carry the meaning, not the words.
* The project title is rendered by the page, not baked in here.

Run from the repo root:  python3 scripts/generate-placeholders.py
"""

import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

W, H = 800, 450

CARD = "#17171a"   # page card background, for reference
APP = "#2c2c33"    # window surface
BAR = "#3a3a43"    # chrome / sidebar
PANEL = "#34343c"  # content panel
WELL = "#25252b"   # inset well

WHITE = "#ffffff"
RED = "#e05a4e"    # up / buy  (Chinese market convention)
GREEN = "#3fa87b"  # down / sell
GOLD = "#ffd95e"
BLUE = "#5f93d8"
PURPLE = "#9086d8"
ORANGE = "#e89044"


def R(x, y, w, h, fill=WHITE, op=0.15, rx=0, stroke=None, sw=1):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
         f'fill="{fill}" fill-opacity="{op}"')
    if stroke:
        s += f' stroke="{stroke[0]}" stroke-opacity="{stroke[1]}" stroke-width="{sw}"'
    return s + "/>"


def T(x, y, text, size=12, fill=WHITE, op=0.9, weight="400", anchor="start", ls=0):
    # Escape here rather than at every call site: a bare "&" in a label makes
    # the whole file unparseable and the card renders empty.
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" fill-opacity="{op}" '
            f'letter-spacing="{ls}">{escape(str(text))}</text>')


def LN(x1, y1, x2, y2, stroke=WHITE, op=0.22, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-opacity="{op}" stroke-width="{sw}"{d}/>')


def C(cx, cy, r, fill=WHITE, op=0.6):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" fill-opacity="{op}"/>'


def P(points, stroke, op=0.95, sw=3, dash=None):
    pts = " ".join(f"{x},{y}" for x, y in points)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-opacity="{op}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{d}/>')


def chrome(label):
    """Window bar with traffic lights so each card reads as a screen."""
    out = [R(12, 12, 776, 426, APP, 1, rx=12, stroke=(WHITE, 0.18)),
           LN(12, 48, 788, 48, WHITE, 0.16)]
    for i, col in enumerate((RED, GOLD, GREEN)):
        out.append(C(34 + i * 16, 30, 4.5, col, 0.9))
    out.append(T(140, 34, label, 11, WHITE, 0.42))
    return out


def sidebar(y0, items, active=0, x=24, w=132):
    out = []
    for i, label in enumerate(items):
        y = y0 + i * 27
        if i == active:
            out.append(R(x, y - 13, w, 23, WHITE, 0.16, rx=6))
        out.append(R(x + 13, y - 6, 11, 11, WHITE, 0.75 if i == active else 0.35, rx=3))
        out.append(T(x + 32, y + 3, label, 10.5, WHITE, 0.9 if i == active else 0.5))
    return out


def lines(x, y, widths, gap=15, h=7, op=0.24):
    return [R(x, y + i * gap, w, h, WHITE, op, rx=3.5) for i, w in enumerate(widths)]


def candles(x, y, w, h, n=24, seed=7, base=0.5):
    """Deterministic pseudo-random candle series."""
    out = [R(x, y, w, h, WELL, 1, rx=8)]
    step = w / n
    cw = max(3.0, step * 0.55)
    price = base
    state = seed
    for i in range(n):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        rnd = (state >> 16) % 1000 / 1000
        prev = price
        price = min(0.9, max(0.12, price + (rnd - 0.47) * 0.20))
        cx = x + step * (i + 0.5)
        col = RED if price >= prev else GREEN
        hi = y + h - max(price, prev) * h
        lo = y + h - min(price, prev) * h
        out.append(LN(cx, max(y + 4, hi - 7), cx, min(y + h - 4, lo + 7), col, 0.7, 1.4))
        out.append(R(cx - cw / 2, hi, cw, max(3, lo - hi), col, 0.98, rx=1.5))
    return out


def grid_lines(x, y, w, h, n=4, col=WHITE, op=0.09):
    return [LN(x, y + h * i / n, x + w, y + h * i / n, col, op) for i in range(1, n)]


# ------------------------------------------------------------ 15 scenes

def s_terminal():
    o = chrome("spot / futures terminal")
    o += [R(12, 48, 140, 390, BAR, 0.9)]
    o += sidebar(84, ["Markets", "Trade", "Orders", "Assets", "Wallet", "Settings"], 1)
    # header
    o += [T(170, 74, "BTC / USDT", 15, WHITE, 1, weight="600"),
          T(268, 74, "80,215.40", 15, RED, 1, weight="600"),
          R(350, 62, 62, 18, RED, 0.3, rx=9),
          T(381, 75, "+2.14%", 10, RED, 1, weight="600", anchor="middle")]
    o += candles(170, 88, 340, 178, 22, seed=11)
    # stats
    for i, (lab, val) in enumerate([("24h High", "81,420.0"), ("24h Low", "78,905.5"),
                                    ("24h Volume", "12,482 BTC"), ("Funding", "0.0107%")]):
        x = 170 + i * 86
        o += [T(x, 292, lab, 9, WHITE, 0.5),
              T(x, 310, val, 12, WHITE, 0.95, weight="500")]
    # depth rows
    o += [R(170, 326, 340, 100, WELL, 1, rx=8)]
    for i in range(5):
        ry = 342 + i * 18
        o += [T(182, ry + 10, f"{80.2 + i * 0.03:.2f}%", 9.5, WHITE, 0.55),
              R(246, ry + 2, 140 - i * 18, 9, RED if i < 2 else GREEN, 0.7, rx=4),
              T(498, ry + 10, f"{0.42 + i * 0.2:.2f}", 9.5, WHITE, 0.5, anchor="end")]
    # order book
    o += [R(524, 62, 252, 378, WELL, 1, rx=8),
          T(538, 82, "ORDER BOOK", 9.5, WHITE, 0.5, ls=0.6),
          T(538, 100, "PRICE (USDT)", 8.5, WHITE, 0.42),
          T(762, 100, "SIZE", 8.5, WHITE, 0.42, anchor="end")]
    for i in range(6):
        ry = 110 + i * 20
        o += [R(534, ry, 232 * (0.94 - i * 0.1), 18, GREEN, 0.55, rx=3),
              T(542, ry + 13, f"{80430 - i * 37}", 10, WHITE, 0.95),
              T(762, ry + 13, f"{1.2 + i * 0.3:.2f}", 10, WHITE, 0.65, anchor="end")]
    o += [R(534, 232, 232, 26, GOLD, 0.95, rx=5),
          T(542, 250, "80,215.40", 12, "#1a1a1f", 1, weight="600"),
          T(762, 250, "mid", 9, "#1a1a1f", 0.75, anchor="end")]
    for i in range(6):
        ry = 264 + i * 20
        o += [R(534, ry, 232 * (0.6 + i * 0.1), 18, RED, 0.55, rx=3),
              T(542, ry + 13, f"{80212 - i * 37}", 10, WHITE, 0.95),
              T(762, ry + 13, f"{0.9 + i * 0.35:.2f}", 10, WHITE, 0.65, anchor="end")]
    o += [R(534, 392, 232, 34, RED, 0.95, rx=8),
          T(650, 415, "BUY / LONG", 12, "#2a1210", 1, weight="600", anchor="middle")]
    return o


def s_orderbook():
    o = chrome("market depth")
    o += [R(12, 48, 776, 390, PANEL, 1)]
    o += [T(34, 76, "MARKET DEPTH  ·  BTC-USDT", 12, WHITE, 0.9, weight="600", ls=0.5),
          R(660, 62, 104, 22, RED, 0.28, rx=11),
          T(712, 77, "0.5 BTC", 10, RED, 1, weight="600", anchor="middle")]
    # ladder
    o += [R(34, 92, 306, 320, WELL, 1, rx=10)]
    for i in range(8):
        ry = 106 + i * 22
        o += [R(38, ry, 298 * (0.92 - i * 0.09), 19, GREEN, 0.5, rx=4),
              T(50, ry + 14, f"{80430 - i * 37}", 10.5, WHITE, 0.95),
              T(330, ry + 14, f"{0.8 + i * 0.29:.3f}", 10.5, WHITE, 0.6, anchor="end")]
    o += [R(38, 288, 298, 28, GOLD, 0.95, rx=5),
          T(50, 307, "80,215.4", 13, "#1a1a1f", 1, weight="600"),
          T(330, 307, "spread 0.19", 9.5, "#1a1a1f", 0.8, anchor="end")]
    for i in range(8):
        ry = 318 + i * 22
        o += [R(38, ry, 298 * (0.6 + i * 0.09), 19, RED, 0.5, rx=4),
              T(50, ry + 14, f"{80212 - i * 37}", 10.5, WHITE, 0.95),
              T(330, ry + 14, f"{0.6 + i * 0.33:.3f}", 10.5, WHITE, 0.6, anchor="end")]
    # depth curve
    o += [R(360, 92, 404, 190, WELL, 1, rx=10),
          T(376, 114, "CUMULATIVE DEPTH", 9.5, WHITE, 0.55, ls=0.6)]
    o += grid_lines(376, 126, 372, 140, 3)
    o += [P([(376, 252), (418, 224), (460, 236), (502, 194), (544, 208), (586, 166),
             (628, 180), (670, 140), (712, 152), (748, 122)], RED, 1, 3.5),
          P([(376, 162), (418, 182), (460, 170), (502, 198), (544, 186), (586, 212),
             (628, 200), (670, 226), (712, 214), (748, 240)], GREEN, 1, 3.5)]
    # summary bars
    for i in range(4):
        x = 360 + i * 103
        o += [R(x, 300, 92, 14, RED, 0.85, rx=3),
              R(x, 318, 92, 14, GREEN, 0.85, rx=3),
              T(x, 348, f"{80.4 - i * 0.1:.1f}k", 9.5, WHITE, 0.5)]
    o += [R(360, 362, 404, 50, WHITE, 0.06, rx=8),
          T(376, 384, "BID / ASK RATIO", 9.5, WHITE, 0.5, ls=0.5),
          R(376, 392, 372, 10, GREEN, 0.5, rx=5),
          R(376, 392, 226, 10, RED, 0.9, rx=5),
          T(748, 384, "61% / 39%", 10, WHITE, 0.8, anchor="end", weight="500")]
    return o


def s_charts():
    o = chrome("charting components")
    o += [R(12, 48, 776, 390, PANEL, 1)]
    o += [R(34, 64, 130, 26, WHITE, 0.16, rx=7),
          T(48, 81, "1m  5m  15m", 10, WHITE, 0.75)]
    for i, lab in enumerate(["MA", "EMA", "BOLL", "RSI", "MACD"]):
        x = 178 + i * 64
        o += [R(x, 64, 54, 26, WHITE, 0.26 if i == 0 else 0.1, rx=7),
              T(x + 27, 81, lab, 10, WHITE, 0.95 if i == 0 else 0.55, anchor="middle",
                weight="600" if i == 0 else "400")]
    o += candles(34, 102, 500, 206, 30, seed=23, base=0.45)
    o += grid_lines(34, 102, 500, 206, 4)
    o += [P([(34, 262), (150, 230), (266, 244), (382, 202), (534, 222)], BLUE, 0.95, 2.5),
          P([(34, 244), (150, 258), (266, 214), (382, 234), (534, 194)], PURPLE, 0.95, 2.5)]
    # volume
    o += [R(34, 320, 500, 92, WELL, 1, rx=8)]
    for i in range(22):
        x = 42 + i * 22
        hgt = 14 + ((i * 37) % 48)
        o += [R(x, 404 - hgt, 14, hgt, RED if i % 3 else GREEN, 0.75, rx=2)]
    o += [LN(34, 404, 534, 404, WHITE, 0.25)]
    # indicator rail
    o += [R(552, 64, 212, 350, WELL, 1, rx=10),
          T(568, 88, "INDICATORS", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (lab, val, col) in enumerate([("RSI (14)", "58.4", GOLD), ("MACD", "+182.6", GREEN),
                                          ("Stoch", "72.1", RED), ("ATR", "842.0", WHITE)]):
        y = 112 + i * 54
        o += [T(568, y, lab, 10, WHITE, 0.55),
              T(748, y, val, 14, col, 1, weight="600", anchor="end"),
              R(568, y + 12, 180, 7, WHITE, 0.14, rx=3.5),
              R(568, y + 12, 180 * (0.74 - i * 0.14), 7, col, 0.95, rx=3.5)]
    o += [R(568, 340, 180, 62, WHITE, 0.07, rx=8),
          T(580, 362, "DRAWING TOOLS", 9, WHITE, 0.45, ls=0.5)]
    for i in range(5):
        o += [R(580 + i * 34, 372, 27, 22, WHITE, 0.22, rx=5)]
    return o


def s_mobile():
    o = chrome("mobile app  ·  react native")
    o += [R(12, 48, 776, 390, PANEL, 1)]
    o += [R(306, 62, 192, 366, WELL, 1, rx=24, stroke=(WHITE, 0.28), sw=2),
          R(372, 70, 60, 6, WHITE, 0.3, rx=3)]
    o += [T(326, 102, "BTC / USDT", 11.5, WHITE, 0.95, weight="600"),
          T(478, 102, "+2.14%", 11.5, RED, 1, weight="600", anchor="end")]
    o += candles(322, 112, 160, 88, 13, seed=5)
    o += [T(326, 226, "80,215.40", 20, WHITE, 1, weight="600")]
    o += [R(322, 240, 160, 28, WHITE, 0.13, rx=7),
          T(334, 259, "Limit", 10.5, WHITE, 0.95),
          T(470, 259, "Market", 10.5, WHITE, 0.5, anchor="end")]
    for i in range(3):
        o += [R(322, 274 + i * 26, 160, 22, WHITE, 0.1, rx=6),
              R(332, 280 + i * 26, 60, 10, WHITE, 0.3, rx=5),
              R(412, 280 + i * 26, 60, 10, WHITE, 0.3, rx=5)]
    o += [R(322, 358, 76, 36, GREEN, 0.95, rx=9),
          T(360, 381, "SELL", 11.5, "#0e1f18", 1, weight="600", anchor="middle"),
          R(406, 358, 76, 36, RED, 1, rx=9),
          T(444, 381, "BUY", 11.5, "#2a1210", 1, weight="600", anchor="middle")]
    # watchlist
    o += [T(56, 80, "WATCHLIST", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (pair, pct) in enumerate([("BTC/USDT", "+2.14%"), ("ETH/USDT", "+1.02%"),
                                      ("SOL/USDT", "-0.84%"), ("WEEX/USDT", "+6.31%")]):
        y = 98 + i * 44
        col = GREEN if pct.startswith("-") else RED
        o += [R(56, y, 214, 36, WHITE, 0.09, rx=8),
              T(68, y + 23, pair, 11.5, WHITE, 0.92),
              T(258, y + 23, pct, 11.5, col, 1, anchor="end", weight="600")]
    # position
    o += [T(536, 80, "POSITION", 9.5, WHITE, 0.55, ls=0.6),
          R(536, 94, 228, 146, WHITE, 0.09, rx=10)]
    for i, (lab, val, col) in enumerate([("Entry", "79,120.0", WHITE), ("Mark", "80,215.4", WHITE),
                                          ("Liq.", "72,480.0", GREEN), ("Unrealised", "+1,340.2", RED),
                                          ("Margin", "18.4%", GOLD)]):
        y = 120 + i * 27
        o += [T(550, y, lab, 10, WHITE, 0.55),
              T(750, y, val, 11.5, col, 1, anchor="end", weight="500")]
    o += [R(536, 252, 228, 50, RED, 0.26, rx=10, stroke=(RED, 0.6)),
          T(550, 274, "Margin ratio high", 10.5, WHITE, 0.95),
          T(550, 292, "Add margin to reduce risk", 9.5, RED, 1)]
    o += [R(536, 316, 228, 106, WHITE, 0.07, rx=10),
          T(550, 340, "RECENT FILLS", 9, WHITE, 0.45, ls=0.5)]
    for i in range(3):
        y = 360 + i * 22
        o += [T(550, y, ["Buy", "Sell", "Buy"][i], 10, WHITE, 0.85),
              T(612, y, f"{80.1 + i * 0.1:.2f}k", 10, WHITE, 0.55),
              T(750, y, f"{0.12 + i * 0.06:.2f} BTC", 10, WHITE, 0.6, anchor="end")]
    return o


def s_wallet():
    o = chrome("wallet connect  ·  signing")
    o += [R(12, 48, 776, 390, PANEL, 1)]
    o += [T(34, 76, "SIGNING FLOW", 12, WHITE, 0.9, weight="600", ls=1)]
    steps = ["Connect", "Select", "Quote", "Confirm", "Sign", "Done"]
    for i, s in enumerate(steps):
        cx = 96 + i * 122
        done, cur = i < 4, i == 4
        col = GOLD if cur else (RED if done else WHITE)
        op = 1 if cur else (0.28 if done else 0.12)
        o += [R(cx - 40, 94, 80, 46, col, op, rx=10),
              T(cx, 123, s, 10.5, "#1a1a1f" if (cur or done) else WHITE,
                1 if (cur or done) else 0.6, weight="600" if cur else "400", anchor="middle")]
        if i < len(steps) - 1:
            o += [LN(cx + 42, 117, cx + 76, 117, WHITE, 0.35, 2),
                  P([(cx + 71, 112), (cx + 78, 117), (cx + 71, 122)], WHITE, 0.45, 2)]
    # tx detail
    o += [R(34, 162, 350, 252, WELL, 1, rx=10),
          T(52, 188, "TRANSACTION DETAIL", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (lab, val) in enumerate([("From", "0x7a3f…c21e"), ("To", "0x91bd…04fa"),
                                     ("Amount", "1.2400 ETH"), ("Network", "Ethereum"),
                                     ("Est. fee", "0.00182 ETH")]):
        y = 216 + i * 38
        o += [T(52, y, lab, 10, WHITE, 0.55),
              T(366, y, val, 12, WHITE, 0.95, anchor="end", weight="500"),
              LN(52, y + 13, 366, y + 13, WHITE, 0.1)]
    # confirm panel
    o += [R(400, 162, 364, 252, WELL, 1, rx=10),
          T(418, 188, "CONFIRMATION", 9.5, WHITE, 0.55, ls=0.6),
          C(582, 252, 44, GOLD, 0.22),
          C(582, 252, 28, GOLD, 1),
          T(582, 259, "5", 21, "#1a1a1f", 1, weight="600", anchor="middle"),
          T(582, 320, "Confirm in your wallet", 12, WHITE, 0.95, anchor="middle"),
          T(582, 342, "Waiting for signature…", 10.5, WHITE, 0.55, anchor="middle"),
          R(418, 366, 328, 34, GOLD, 1, rx=8),
          T(582, 389, "SIGN & BROADCAST", 11.5, "#1a1a1f", 1, weight="600", anchor="middle")]
    return o


def s_deposit():
    o = chrome("deposit / withdraw")
    o += [R(12, 48, 776, 390, PANEL, 1)]
    o += [R(34, 64, 124, 30, RED, 0.95, rx=8),
          T(96, 84, "Deposit", 11.5, "#2a1210", 1, weight="600", anchor="middle"),
          R(162, 64, 124, 30, WHITE, 0.12, rx=8),
          T(224, 84, "Withdraw", 11.5, WHITE, 0.6, anchor="middle")]
    # asset picker
    o += [R(34, 104, 404, 300, WELL, 1, rx=10),
          T(52, 128, "SELECT ASSET & NETWORK", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (sym, net, col) in enumerate([("USDT", "TRON · TRC20", GREEN),
                                          ("USDT", "Ethereum · ERC20", BLUE),
                                          ("BTC", "Bitcoin", ORANGE),
                                          ("ETH", "Ethereum", PURPLE)]):
        y = 144 + i * 46
        sel = i == 0
        o += [R(52, y, 368, 38, WHITE, 0.16 if sel else 0.06, rx=8,
                stroke=(RED, 0.75) if sel else None),
              C(76, y + 19, 12, col, 0.95),
              T(96, y + 24, sym, 11.5, WHITE, 0.95, weight="500"),
              T(408, y + 24, net, 10, WHITE, 0.5, anchor="end"),
              C(376, y + 19, 7, RED if sel else WHITE, 0.95 if sel else 0.25)]
    o += [R(34, 414, 404, 0, WHITE, 0)]
    o += [R(34, 414, 404, 0, WHITE, 0)]
    o += [R(34, 356, 404, 48, GOLD, 0.2, rx=10, stroke=(GOLD, 0.6)),
          T(52, 376, "Send USDT on TRON only", 10.5, GOLD, 1, weight="500"),
          T(52, 393, "Wrong network means permanent loss", 9.5, WHITE, 0.6)]
    # address
    o += [R(456, 104, 308, 300, WELL, 1, rx=10),
          T(474, 128, "YOUR DEPOSIT ADDRESS", 9.5, WHITE, 0.55, ls=0.6),
          R(474, 140, 272, 76, WHITE, 0.97, rx=8)]
    for r_ in range(5):
        for c_ in range(5):
            if (r_ * 3 + c_ * 5) % 3:
                o += [R(492 + c_ * 13, 156 + r_ * 13, 10, 10, "#1a1a1f", 0.92, rx=1.5)]
    o += [T(510, 232, "TXk9mQ…7fR2", 12.5, WHITE, 1, weight="600"),
          R(474, 246, 272, 32, WHITE, 0.14, rx=7),
          T(610, 267, "COPY ADDRESS", 10.5, WHITE, 0.95, weight="600", anchor="middle")]
    for i, (lab, val, col) in enumerate([("Network", "TRON (TRC20)", WHITE),
                                          ("Minimum", "1 USDT", WHITE),
                                          ("Credit after", "19 confirmations", GOLD)]):
        y = 302 + i * 32
        o += [T(474, y, lab, 10, WHITE, 0.55),
              T(746, y, val, 11, col, 0.95, anchor="end", weight="500")]
    o += [LN(474, 390, 746, 390, WHITE, 0.14)]
    return o


def s_ops():
    o = chrome("operations console")
    o += [R(12, 48, 776, 390, PANEL, 1)]

    def card(x, y, w, lab, val, delta, col):
        return [R(x, y, w, 86, WHITE, 0.08, rx=10, stroke=(WHITE, 0.12)),
                T(x + 14, y + 24, lab, 9, WHITE, 0.5, ls=0.5),
                T(x + 14, y + 52, val, 22, WHITE, 1, weight="600"),
                R(x + 14, y + 62, 62, 18, col, 0.4, rx=9),
                T(x + 22, y + 75, delta, 9.5, col, 1, weight="600")]

    o += card(34, 62, 176, "OPEN ALERTS", "14", "3 critical", RED)
    o += card(222, 62, 176, "NODES ONLINE", "212", "98.6%", GREEN)
    o += card(410, 62, 176, "24H WITHDRAWALS", "1,842", "+12.4%", GOLD)
    o += card(598, 62, 166, "PENDING REVIEW", "27", "queued", BLUE)
    # table
    o += [R(34, 162, 730, 256, WELL, 1, rx=10),
          T(52, 186, "ABNORMAL ACTIVITY", 9.5, WHITE, 0.55, ls=0.6)]
    cols = [52, 148, 292, 396, 512, 636]
    for i, h in enumerate(["TIME", "ACCOUNT", "TYPE", "AMOUNT", "SEVERITY", "STATUS"]):
        o += [T(cols[i], 210, h, 9, WHITE, 0.45, ls=0.5)]
    o += [LN(52, 220, 748, 220, WHITE, 0.18)]
    rows = [("11:04", "u_4821", "Withdrawal", "18.20 BTC", "High", RED, "Investigating"),
            ("10:58", "u_1174", "API key", "new IP", "Medium", ORANGE, "Flagged"),
            ("10:41", "u_9032", "Login", "4 regions", "High", RED, "Blocked"),
            ("10:22", "u_6650", "Transfer", "1,240 ETH", "Low", BLUE, "Cleared"),
            ("09:57", "u_3318", "Order", "wash pattern", "Medium", ORANGE, "Monitoring")]
    for r_, (t, acc, typ, amt, sev, col, st) in enumerate(rows):
        y = 244 + r_ * 34
        if r_ % 2 == 0:
            o += [R(44, y - 15, 710, 30, WHITE, 0.055, rx=6)]
        o += [T(cols[0], y, t, 10, WHITE, 0.65),
              T(cols[1], y, acc, 10.5, WHITE, 0.95),
              T(cols[2], y, typ, 10, WHITE, 0.65),
              T(cols[3], y, amt, 10.5, WHITE, 0.95, weight="500"),
              R(cols[4], y - 13, 72, 18, col, 0.4, rx=9),
              T(cols[4] + 10, y, sev, 9.5, col, 1, weight="600"),
              T(cols[5], y, st, 10, WHITE, 0.6)]
    return o


def s_audit():
    o = chrome("withdrawal approval")
    o += [R(12, 48, 776, 390, PANEL, 1),
          T(34, 76, "REQUESTS", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (who, amt, st, col) in enumerate([("u_4821", "18.20 BTC", "Awaiting", GOLD),
                                              ("u_9032", "2,400 ETH", "Approved", GREEN),
                                              ("u_1174", "940,000 USDT", "Rejected", RED),
                                              ("u_6650", "12.5 BTC", "Approved", GREEN)]):
        y = 94 + i * 72
        sel = i == 0
        o += [R(34, y, 258, 60, WHITE, 0.16 if sel else 0.06, rx=10,
                stroke=(GOLD, 0.7) if sel else None),
              T(50, y + 24, who, 11.5, WHITE, 0.95, weight="500"),
              T(50, y + 44, amt, 11, WHITE, 0.65),
              R(196, y + 14, 82, 20, col, 0.4, rx=10),
              T(208, y + 29, st, 9.5, col, 1, weight="600")]
    o += [R(306, 62, 464, 356, WELL, 1, rx=10),
          T(324, 88, "AUDIT TRAIL", 9.5, WHITE, 0.55, ls=0.6),
          R(324, 100, 428, 46, GOLD, 0.22, rx=8, stroke=(GOLD, 0.5)),
          T(340, 120, "18.20 BTC  —  high risk", 12, GOLD, 1, weight="600"),
          T(340, 138, "Requires 2 of 3 approvers", 10, WHITE, 0.7)]
    trail = [("09:12:04", "u_4821", "Request submitted", GOLD),
             ("09:14:22", "system", "Risk score 82 / 100", RED),
             ("09:16:10", "ops_zhou", "Approved (1 of 2)", GREEN),
             ("09:31:48", "ops_li", "Approved (2 of 2)", GREEN),
             ("09:32:02", "system", "Signature queued", BLUE)]
    for i, (t, actor, ev, col) in enumerate(trail):
        y = 176 + i * 46
        o += [LN(340, y, 340, y + 40, WHITE, 0.2),
              C(340, y + 10, 7, col, 1),
              T(358, y + 6, t, 9.5, WHITE, 0.5),
              T(358, y + 26, ev, 11.5, WHITE, 0.95, weight="500"),
              T(744, y + 26, actor, 9.5, WHITE, 0.55, anchor="end")]
    o += [R(324, 398, 428, 0, WHITE, 0)]
    return o


def s_design_system():
    o = chrome("design system")
    o += [R(12, 48, 776, 390, PANEL, 1),
          T(34, 76, "CORE COMPONENTS", 12, WHITE, 0.9, weight="600", ls=1),
          T(258, 76, "web  ·  h5  ·  app", 10, WHITE, 0.5)]
    # buttons
    o += [R(34, 96, 108, 36, RED, 1, rx=8),
          T(88, 119, "Primary", 11.5, "#2a1210", 1, weight="600", anchor="middle"),
          R(150, 96, 108, 36, WHITE, 0.16, rx=8),
          T(204, 119, "Secondary", 11.5, WHITE, 0.9, weight="500", anchor="middle"),
          R(266, 96, 108, 36, WHITE, 0.05, rx=8, stroke=(WHITE, 0.35)),
          T(320, 119, "Ghost", 11.5, WHITE, 0.65, anchor="middle")]
    # fields
    o += [T(34, 160, "Text field", 9.5, WHITE, 0.5),
          R(34, 170, 340, 38, WHITE, 0.09, rx=8, stroke=(WHITE, 0.18)),
          T(48, 194, "placeholder", 11, WHITE, 0.4),
          T(34, 230, "Focused", 9.5, WHITE, 0.5),
          R(34, 240, 340, 38, WHITE, 0.12, rx=8, stroke=(RED, 0.9), sw=2),
          T(48, 264, "entered value", 11, WHITE, 0.95)]
    # tags
    o += [T(34, 302, "Status tags", 9.5, WHITE, 0.5)]
    for i, (lab, col) in enumerate([("Filled", GREEN), ("Partial", GOLD), ("Canceled", WHITE),
                                     ("Failed", RED), ("Pending", BLUE)]):
        o += [R(34 + i * 69, 312, 63, 24, col, 0.35, rx=12),
              T(65 + i * 69, 328, lab, 9.5, col, 1, anchor="middle", weight="600")]
    # table
    ty = 352
    o += [R(34, ty, 340, 74, WELL, 1, rx=8),
          R(34, ty, 340, 26, WHITE, 0.1, rx=8)]
    for i, h in enumerate(["Market", "Price", "Change"]):
        o += [T(48 + i * 112, ty + 18, h, 9, WHITE, 0.5)]
    for r_ in range(2):
        y = ty + 44 + r_ * 22
        col = RED if r_ == 0 else GREEN
        o += [T(48, y, f"BTC-USDT", 10, WHITE, 0.9),
              T(160, y, f"{80 + r_ * 4}k", 10, WHITE, 0.6),
              T(272, y, f"{'+' if r_ == 0 else '-'}{1.2 + r_ * 0.4}%", 10, col, 1)]
    # library grid
    o += [T(400, 96, "COMPONENT LIBRARY", 9.5, WHITE, 0.55, ls=0.6)]
    for i in range(3):
        for j in range(3):
            x = 400 + j * 126
            y = 108 + i * 100
            hot = (i * 3 + j) % 4 == 0
            o += [R(x, y, 114, 86, WHITE, 0.09, rx=9, stroke=(WHITE, 0.16)),
                  C(x + 57, y + 32, 17, RED if hot else WHITE, 0.95 if hot else 0.25),
                  R(x + 22, y + 60, 70, 8, WHITE, 0.3, rx=4),
                  R(x + 22, y + 73, 46, 7, WHITE, 0.18, rx=3.5)]
    o += [T(400, 424, "48 components  ·  12 patterns  ·  3 platforms", 9.5, WHITE, 0.45)]
    return o


def s_tokens():
    o = chrome("tokens  ·  colour, type, motion")
    o += [R(12, 48, 776, 390, PANEL, 1),
          T(34, 76, "COLOUR", 10, WHITE, 0.55, ls=0.6)]
    swatches = [(RED, "brand/500"), (GOLD, "brand/200"), (GREEN, "up/500"),
                (BLUE, "info/500"), (PURPLE, "accent/500"), (ORANGE, "warn/500")]
    for i, (col, name) in enumerate(swatches):
        x = 34 + i * 76
        o += [R(x, 88, 68, 68, col, 1, rx=12),
              T(x, 172, name, 8.5, WHITE, 0.5)]
    o += [T(34, 200, "NEUTRAL RAMP", 10, WHITE, 0.55, ls=0.6)]
    for i in range(9):
        x = 34 + i * 50
        o += [R(x, 212, 44, 36, WHITE, 0.08 + i * 0.1, rx=7),
              T(x + 22, 264, f"{100 + i * 100}", 8.5, WHITE, 0.45, anchor="middle")]
    o += [T(34, 300, "TYPE SCALE", 10, WHITE, 0.55, ls=0.6)]
    for i, (label, size) in enumerate([("Display", 26), ("Heading", 19), ("Body", 14), ("Caption", 11)]):
        y = 322 + i * 30
        o += [T(34, y + 8, "Ag", size, WHITE, 0.95, weight="600"),
              T(106, y + 8, label, 10.5, WHITE, 0.6),
              R(184, y + 2, 200 - i * 30, 8, WHITE, 0.24, rx=4)]
    o += [T(430, 76, "MOTION", 10, WHITE, 0.55, ls=0.6)]
    for i, (name, col) in enumerate([("ease-out", RED), ("ease-in-out", GOLD), ("spring", BLUE)]):
        y = 94 + i * 72
        o += [R(430, y, 340, 60, WELL, 1, rx=9),
              T(444, y + 20, name, 10.5, WHITE, 0.9, weight="500"),
              T(756, y + 20, f"{120 + i * 80}ms", 9.5, WHITE, 0.5, anchor="end"),
              f'<path d="M444,{y + 46} C{506 + i * 18},{y + 46} {540},{y + 26} 600,{y + 26}" '
              f'fill="none" stroke="{col}" stroke-opacity="1" stroke-width="3" stroke-linecap="round"/>',
              f'<path d="M624,{y + 46} C{692},{y + 46} {702},{y + 26} 756,{y + 26}" '
              f'fill="none" stroke="{col}" stroke-opacity="0.45" stroke-width="3" '
              f'stroke-linecap="round" stroke-dasharray="5 5"/>']
    o += [T(430, 320, "LOTTIE  ·  RIVE", 10, WHITE, 0.55, ls=0.6)]
    for i, lab in enumerate(["Loading", "Success", "Error", "Empty"]):
        x = 430 + i * 86
        o += [R(x, 332, 78, 76, WHITE, 0.09, rx=10, stroke=(WHITE, 0.16)),
              C(x + 39, 360, 15, [GOLD, GREEN, RED, WHITE][i], 0.95),
              T(x + 39, 396, lab, 9.5, WHITE, 0.6, anchor="middle")]
    return o


def s_campaign():
    o = chrome("overseas campaign visuals")
    # hero
    o += [R(24, 62, 300, 364, "#141419", 1, rx=12, stroke=(RED, 0.55), sw=2),
          C(268, 116, 74, RED, 0.38),
          C(52, 344, 62, GOLD, 0.22),
          T(46, 122, "TRADE", 31, WHITE, 1, weight="600", ls=1),
          T(46, 160, "ANYWHERE", 31, GOLD, 1, weight="600", ls=1),
          R(46, 178, 190, 3, RED, 0.9),
          T(46, 208, "Zero-fee spot for new users", 11.5, WHITE, 0.8),
          R(46, 232, 132, 38, RED, 1, rx=9),
          T(112, 257, "Get started", 12, "#2a1210", 1, weight="600", anchor="middle"),
          R(192, 232, 100, 38, WHITE, 0.1, rx=9),
          T(242, 257, "Learn more", 11.5, WHITE, 0.7, anchor="middle"),
          T(46, 398, "EU  ·  US  ·  SEA", 10, WHITE, 0.5, ls=2)]
    # social set
    o += [T(352, 76, "SOCIAL SET", 9.5, WHITE, 0.55, ls=0.6)]
    for i in range(3):
        for j in range(2):
            x = 352 + j * 218
            y = 88 + i * 118
            col = [RED, GOLD, BLUE, GREEN, ORANGE, PURPLE][i * 2 + j]
            o += [R(x, y, 202, 104, WELL, 1, rx=10, stroke=(WHITE, 0.14)),
                  C(x + 42, y + 42, 23, col, 1),
                  R(x + 78, y + 26, 104, 12, WHITE, 0.8, rx=6),
                  R(x + 78, y + 46, 72, 10, WHITE, 0.45, rx=5),
                  R(x + 20, y + 76, 164, 8, WHITE, 0.25, rx=4)]
    return o


def s_identity():
    o = chrome("brand identity")
    o += [R(12, 48, 776, 390, PANEL, 1)]
    o += [R(34, 62, 296, 362, "#141419", 1, rx=12, stroke=(WHITE, 0.16)),
          C(182, 208, 78, RED, 0.3),
          C(182, 208, 50, RED, 1),
          T(182, 224, "W", 44, GOLD, 1, weight="600", anchor="middle"),
          T(182, 330, "PRIMARY LOCKUP", 9.5, WHITE, 0.5, ls=1.5, anchor="middle"),
          R(96, 350, 172, 2, WHITE, 0.14)]
    o += [T(352, 76, "VARIANTS", 9.5, WHITE, 0.55, ls=0.6)]
    for i, lab in enumerate(["Horizontal", "Stacked", "Monogram", "Inverted"]):
        x = 352 + i * 112
        inv = i == 3
        o += [R(x, 88, 100, 80, WHITE, 0.95 if inv else 0.08, rx=10,
                stroke=(WHITE, 0.16)),
              C(x + 33, 128, 15, "#141419" if inv else RED, 0.95),
              R(x + 55, 122, 33, 8, "#141419" if inv else WHITE, 0.55, rx=4),
              R(x + 55, 134, 22, 6, "#141419" if inv else WHITE, 0.35, rx=3),
              T(x + 50, 160, lab, 8.5, WHITE, 0.5, anchor="middle")]
    o += [T(352, 194, "PALETTE ROLES", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (col, pct) in enumerate([(RED, "60%"), (GOLD, "24%"), ("#141419", "12%"), (WHITE, "4%")]):
        x = 352 + i * 112
        o += [R(x, 206, 100, 56, col, 1 if col != WHITE else 0.95, rx=8),
              T(x, 278, pct, 10, WHITE, 0.55)]
    o += [T(352, 308, "APPLICATIONS", 9.5, WHITE, 0.55, ls=0.6),
          R(352, 320, 216, 102, WHITE, 0.08, rx=10, stroke=(WHITE, 0.14)),
          R(580, 320, 202, 102, WHITE, 0.08, rx=10, stroke=(WHITE, 0.14)),
          R(370, 340, 88, 9, WHITE, 0.35, rx=4.5),
          R(370, 358, 140, 8, WHITE, 0.2, rx=4),
          R(370, 374, 116, 8, WHITE, 0.2, rx=4),
          R(370, 390, 160, 8, WHITE, 0.2, rx=4),
          R(620, 340, 124, 62, RED, 1, rx=8),
          T(682, 380, "W", 26, GOLD, 1, weight="600", anchor="middle")]
    return o


def s_metaverse():
    o = chrome("metaverse space concept")
    o += [R(12, 48, 776, 390, "#121218", 1)]
    for i in range(9):
        y = 196 + i * i * 4.4
        o += [LN(50, y, 750, y, PURPLE, max(0.08, 0.34 - i * 0.025))]
    for i in range(-8, 9):
        o += [LN(400, 192, 400 + i * 98, 436, PURPLE, 0.26)]
    for x, y, w, col, lab in [(198, 262, 170, RED, "EXCHANGE"),
                               (400, 228, 200, GOLD, "MAIN STAGE"),
                               (614, 266, 158, BLUE, "GALLERY")]:
        o += [f'<polygon points="{x - w // 2},{y} {x + w // 2},{y} '
              f'{x + w // 2 - 28},{y + 36} {x - w // 2 + 28},{y + 36}" '
              f'fill="{col}" fill-opacity="0.42" stroke="{col}" stroke-opacity="0.95" stroke-width="1.5"/>',
              f'<ellipse cx="{x}" cy="{y + 38}" rx="{w // 2 - 26}" ry="8" fill="{col}" fill-opacity="0.6"/>',
              T(x, y + 24, lab, 9.5, WHITE, 0.95, weight="600", anchor="middle", ls=1)]
    for x, y, col in [(238, 236, GOLD), (330, 246, WHITE), (470, 204, GOLD), (556, 240, WHITE)]:
        o += [C(x, y, 14, col, 1), R(x - 10, y + 17, 20, 24, col, 0.8, rx=8)]
    o += [R(70, 88, 182, 90, WHITE, 0.12, rx=10, stroke=(PURPLE, 0.6)),
          T(88, 114, "PRESENCE", 9, WHITE, 0.6, ls=0.5),
          T(88, 140, "128 online", 19, WHITE, 1, weight="600"),
          T(88, 162, "in the exchange hall", 9.5, WHITE, 0.55)]
    o += [R(560, 84, 196, 82, WHITE, 0.12, rx=10, stroke=(PURPLE, 0.6)),
          T(578, 110, "SPATIAL LIGHTING", 9, WHITE, 0.6, ls=0.5),
          R(578, 122, 160, 9, PURPLE, 1, rx=4.5),
          R(578, 140, 112, 9, GOLD, 1, rx=4.5)]
    o += [T(400, 414, "BRAND PRESENCE BEYOND THE FLAT SCREEN", 10, WHITE, 0.45,
            anchor="middle", ls=2)]
    return o


def s_ai():
    o = chrome("knowledge assistant")
    o += [R(12, 48, 776, 390, PANEL, 1),
          R(12, 48, 178, 390, WELL, 1),
          T(32, 76, "SOURCES", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (name, cnt) in enumerate([("Q3 policy.pdf", "42"), ("Whitepaper.pdf", "18"),
                                      ("Meeting notes", "11"), ("Changelog.md", "7")]):
        y = 94 + i * 42
        o += [R(28, y, 146, 34, WHITE, 0.16 if i == 0 else 0.06, rx=8),
              C(46, y + 17, 9, BLUE, 0.95),
              T(60, y + 22, name, 10, WHITE, 0.9),
              T(164, y + 22, cnt, 9.5, WHITE, 0.5, anchor="end")]
    o += [R(28, 270, 146, 32, GOLD, 0.95, rx=8),
          T(101, 291, "+ Add source", 10.5, "#1a1a1f", 1, weight="600", anchor="middle")]
    o += [R(28, 320, 146, 100, WHITE, 0.06, rx=8),
          T(42, 342, "INDEXED", 8.5, WHITE, 0.45, ls=0.5),
          T(42, 366, "78 chunks", 13, WHITE, 0.95, weight="600"),
          T(42, 386, "last sync 4m ago", 9, WHITE, 0.5),
          R(42, 396, 118, 7, GREEN, 0.9, rx=3.5)]
    # conversation
    o += [R(206, 66, 296, 62, WHITE, 0.13, rx=12),
          T(222, 92, "What changed in the withdrawal", 10.5, WHITE, 0.95),
          T(222, 111, "limits for tier-2 accounts?", 10.5, WHITE, 0.95)]
    o += [R(272, 142, 318, 132, RED, 0.22, rx=12, stroke=(RED, 0.5)),
          T(288, 168, "Tier-2 daily limit moved from", 10.5, WHITE, 0.95),
          T(288, 187, "50k to 120k USDT on 2026-07-01.", 10.5, WHITE, 0.95),
          T(288, 206, "The change also added a 24h", 10.5, WHITE, 0.95),
          T(288, 225, "cool-down for new devices.", 10.5, WHITE, 0.95),
          R(288, 242, 98, 22, GOLD, 0.95, rx=6),
          T(337, 258, "[1]   [2]", 10, "#1a1a1f", 1, weight="600", anchor="middle")]
    o += [R(206, 288, 256, 50, WHITE, 0.07, rx=10),
          T(222, 310, "CITED", 8.5, WHITE, 0.45, ls=0.5),
          T(222, 330, "Q3 policy.pdf  ·  p.14, p.22", 10, GOLD, 1)]
    o += [R(206, 352, 384, 46, WHITE, 0.09, rx=23, stroke=(WHITE, 0.18)),
          T(228, 381, "Ask a follow-up…", 11, WHITE, 0.4),
          C(568, 375, 16, RED, 1),
          P([(562, 381), (574, 369)], "#2a1210", 1, 2),
          P([(574, 369), (574, 375)], "#2a1210", 1, 2)]
    # run rail
    o += [R(604, 66, 172, 332, WELL, 1, rx=10),
          T(620, 92, "RUN DETAIL", 9, WHITE, 0.5, ls=0.6)]
    for i, (lab, val, col) in enumerate([("Model", "in-house-70b", WHITE), ("Tokens", "2,418", WHITE),
                                          ("Latency", "1.24s", GREEN), ("Retrieved", "9 chunks", WHITE),
                                          ("Rerank", "top 3", GOLD), ("Confidence", "0.86", GREEN)]):
        y = 116 + i * 31
        o += [T(620, y, lab, 9.5, WHITE, 0.5),
              T(760, y, val, 10.5, col, 1, anchor="end", weight="500")]
    o += [LN(620, 308, 760, 308, WHITE, 0.18),
          T(620, 332, "STATES", 8.5, WHITE, 0.45, ls=0.5)]
    for i, lab in enumerate(["streaming", "tool call", "error"]):
        col = [GOLD, BLUE, RED][i]
        o += [C(626, 352 + i * 20, 5, col, 1),
              T(640, 356 + i * 20, lab, 9.5, WHITE, 0.65)]
    return o


def s_aigc():
    o = chrome("aigc exploration")
    o += [R(12, 48, 776, 390, PANEL, 1),
          T(34, 76, "PROMPT", 9.5, WHITE, 0.55, ls=0.6),
          R(34, 86, 344, 78, WELL, 1, rx=8, stroke=(WHITE, 0.18)),
          T(48, 110, "neon trading terminal, dark ui,", 10.5, WHITE, 0.95),
          T(48, 129, "cyan and amber accents, volumetric", 10.5, WHITE, 0.95),
          T(48, 148, "light, isometric, 16:9", 10.5, WHITE, 0.95),
          R(34, 174, 166, 32, RED, 1, rx=8),
          T(117, 195, "Generate x4", 10.5, "#2a1210", 1, weight="600", anchor="middle"),
          R(212, 174, 166, 32, WHITE, 0.14, rx=8),
          T(295, 195, "Refine seeds", 10.5, WHITE, 0.7, anchor="middle")]
    o += [T(34, 234, "SETTINGS", 9.5, WHITE, 0.55, ls=0.6)]
    for i, (lab, val) in enumerate([("Steps", "28"), ("CFG", "6.5"),
                                     ("Sampler", "dpm++"), ("Seed", "84120")]):
        y = 252 + i * 30
        o += [T(34, y, lab, 10, WHITE, 0.55),
              T(378, y, val, 10.5, WHITE, 0.95, anchor="end", weight="500"),
              LN(34, y + 11, 378, y + 11, WHITE, 0.1)]
    o += [R(34, 380, 344, 48, GOLD, 0.2, rx=8, stroke=(GOLD, 0.55)),
          T(48, 402, "Iterating direction 3 of 6", 10, GOLD, 1, weight="500"),
          R(48, 410, 316, 7, WHITE, 0.18, rx=3.5),
          R(48, 410, 168, 7, GOLD, 1, rx=3.5)]
    # variants
    o += [T(402, 76, "VARIANTS", 9.5, WHITE, 0.55, ls=0.6)]
    for i in range(3):
        for j in range(2):
            x = 402 + j * 192
            y = 86 + i * 116
            idx = i * 2 + j
            picked = idx == 1
            col = [RED, GOLD, BLUE, PURPLE, ORANGE, GREEN][idx]
            o += [R(x, y, 178, 104, WELL, 1, rx=10,
                    stroke=(GOLD, 1) if picked else (WHITE, 0.14), sw=2),
                  C(x + 56, y + 52, 32, col, 0.6),
                  C(x + 56, y + 52, 17, col, 1),
                  R(x + 106, y + 30, 56, 9, WHITE, 0.5, rx=4.5),
                  R(x + 106, y + 48, 42, 8, WHITE, 0.28, rx=4),
                  R(x + 106, y + 64, 50, 8, WHITE, 0.28, rx=4),
                  T(x + 14, y + 96, f"seed {84120 + idx * 7}", 8.5, WHITE, 0.5)]
            if picked:
                o += [R(x + 122, y + 78, 44, 20, GOLD, 1, rx=10),
                      T(x + 144, y + 93, "PICK", 9, "#1a1a1f", 1, weight="600", anchor="middle")]
    return o


SCENES = [
    ("proj-terminal", s_terminal),
    ("proj-orderbook", s_orderbook),
    ("proj-charts", s_charts),
    ("proj-mobile", s_mobile),
    ("proj-wallet", s_wallet),
    ("proj-deposit", s_deposit),
    ("proj-ops", s_ops),
    ("proj-audit", s_audit),
    ("proj-ds", s_design_system),
    ("proj-tokens", s_tokens),
    ("proj-campaign", s_campaign),
    ("proj-identity", s_identity),
    ("proj-metaverse", s_metaverse),
    ("proj-ai", s_ai),
    ("proj-aigc", s_aigc),
]


def build_svg(slug, fn):
    body = "\n  ".join(fn())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img" aria-label="{slug}">\n'
            f'  <rect width="{W}" height="{H}" fill="{CARD}"/>\n'
            f'  {body}\n</svg>\n')


def main():
    out = "assets/images/projects"
    os.makedirs(out, exist_ok=True)
    bad = []
    for slug, fn in SCENES:
        path = os.path.join(out, slug + ".svg")
        svg = build_svg(slug, fn)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        # Parse right away: an unescaped & or a repeated attribute produces a
        # file browsers refuse, which shows up as an empty card.
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            bad.append(slug)
            print("  INVALID  %-22s %s" % (slug, exc))
            continue
        print("  %-22s %6d bytes" % (slug, os.path.getsize(path)))
    print()
    if bad:
        raise SystemExit("%d file(s) failed XML validation" % len(bad))
    print("All %d files written and valid." % len(SCENES))


if __name__ == "__main__":
    main()
