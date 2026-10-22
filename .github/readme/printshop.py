"""printshop: green-bar printer paper, dot-matrix type and small charts, as SVG.

Every graphic on the profile is built with this module. Text is set as glyph
outlines from glyphs.json, so the images look the same on every machine and
need no web fonts. Standard library only (the GitHub Action runs it as-is).
"""
import hashlib
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

# Paper and ink ---------------------------------------------------------------
PAPER = "#FDFDF8"      # the sheet
BAND = "#E2EFDD"       # green bar
INK = "#1E232B"        # ribbon black
INK_2 = "#3F4851"      # secondary text
INK_3 = "#56605A"      # muted text, still >= 4.5:1 on the green bar
RULE = "#C6CFC1"       # hairlines and perforations
RED_PEN = "#C8352B"    # hand annotations only, never data
HILITE = "#FFE45C"     # highlighter

# Data colours: a colour-blind-validated categorical palette, used in fixed
# order and never cycled. Text never wears these; marks do.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
TRACK = "#b7d3f6"      # lighter step of the blue ramp (meter track)
QUIET = "#A3AAA0"      # de-emphasised marks

# Page geometry shared by every sheet ----------------------------------------
W = 904                # viewBox width
MARGIN = 12            # transparent room around the sheet for its shadow
STRIP = 40             # tractor-feed strip
X0 = MARGIN + STRIP + 16   # first text column (68)
COLS = 80              # an 80-column printout
CH = 9.6               # advance of 16px IBM Plex Mono
X1 = X0 + COLS * CH    # right edge of the text area (836)
LINE = 24              # line pitch; the green bars are three lines tall
BASE = 17              # baseline offset inside a 24px line


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def short_hash(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:7]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


class Type:
    """Glyph outlines plus metrics, loaded from glyphs.json."""

    def __init__(self, path=None):
        with open(path or os.path.join(HERE, "glyphs.json"), encoding="utf-8") as fh:
            self.fonts = json.load(fh)["fonts"]

    def glyph(self, font, ch):
        g = self.fonts[font]["glyphs"]
        return g.get(ch) or g["?"]

    def width(self, text, font="mono", size=16, track=0.0):
        f = self.fonts[font]
        units = sum(self.glyph(font, c)[0] for c in text)
        return units * size / f["upm"] + track * max(len(text) - 1, 0)


class Page:
    """One SVG document: glyph defs, CSS, and body markup."""

    def __init__(self, height, title, desc, typ=None):
        self.h = height
        self.title = title
        self.desc = desc
        self.t = typ or Type()
        self.used = {}
        self.defs = []
        self.css = []
        self.body = []
        self._ids = 0

    # ids -------------------------------------------------------------------
    def uid(self, stem="i"):
        self._ids += 1
        return f"{stem}{self._ids}"

    def _gid(self, font, ch):
        key = (font, ch)
        if key not in self.used:
            self.used[key] = f"g{len(self.used):x}"
        return self.used[key]

    # text ------------------------------------------------------------------
    def text(self, x, y, s, font="mono", size=16, fill=INK, anchor="start",
             track=0.0, sx=1.0, cls=None, style=None):
        """Markup for one run of text with its baseline at y. Returns (svg, width)."""
        f = self.t.fonts[font]
        k = size / f["upm"]
        w = self.t.width(s, font, size, track) * sx
        if anchor == "end":
            x -= w
        elif anchor == "middle":
            x -= w / 2
        uses, cx = [], 0.0
        for ch in s:
            adv, d = self.t.glyph(font, ch)
            if ch.strip() and d:
                uses.append(f'<use href="#{self._gid(font, ch if ch in f["glyphs"] else "?")}" x="{fmt(cx)}"/>')
            cx += adv + track / k
        attrs = f' fill="{fill}"'
        if cls:
            attrs += f' class="{cls}"'
        if style:
            attrs += f' style="{style}"'
        g = (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({k * sx:.5f} {-k:.5f})"{attrs}>'
             + "".join(uses) + "</g>")
        return g, w

    def add(self, *parts):
        self.body.extend(parts)

    def put(self, *args, **kw):
        """Add a run of text to the page; returns its width."""
        g, w = self.text(*args, **kw)
        self.body.append(g)
        return w

    # output ----------------------------------------------------------------
    def svg(self):
        glyph_defs = []
        for (font, ch), gid in self.used.items():
            d = self.t.glyph(font, ch)[1]
            glyph_defs.append(f'<path id="{gid}" d="{d}"/>')
        css = BASE_CSS + "".join(self.css)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {fmt(self.h)}" '
            f'width="{W}" height="{fmt(self.h)}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc)}</desc>'
            f"<style>{css}</style>"
            f'<defs>{"".join(glyph_defs)}{"".join(self.defs)}</defs>'
            + "".join(self.body) + "</svg>"
        )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.svg())
        return path


# Motion: one short print sequence per sheet, then everything holds still.
# Base states are the finished picture, so a viewer without CSS animation (or
# with reduced motion) simply sees the final sheet.
BASE_CSS = (
    "@keyframes unprint{from{transform:scaleX(1)}to{transform:scaleX(0)}}"
    "@keyframes swipe{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    "@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
    "@keyframes ink{from{stroke-dasharray:1;stroke-dashoffset:1}to{stroke-dasharray:1;stroke-dashoffset:0}}"
    "@keyframes appear{from{opacity:0}to{opacity:1}}"
    "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
    ".cover{transform-box:fill-box;transform-origin:100% 50%}"
    ".swipe{transform-box:fill-box;transform-origin:0 50%}"
    ".rise{transform-box:fill-box;transform-origin:50% 100%}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def cover(x, y, w, h, color, delay, dur, steps, pad=CH + 2):
    """A strip of paper-coloured cover that withdraws left to right, so the
    text under it appears to print one character at a time. The strip runs
    one blank character past the text, so a rounding sliver left at the end
    of the animation lands on empty paper."""
    return (f'<rect class="cover" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w + pad)}" height="{fmt(h)}" '
            f'fill="{color}" transform="scale(0 1)" '
            f'style="animation:unprint {dur:.2f}s steps({max(int(steps), 2)},jump-none) {delay:.2f}s both"/>')


# Paper -------------------------------------------------------------------------
def _edge(x_from, x_to, y, kind, rng):
    """Points along a horizontal edge. kind: 'tear' (perforation), 'rough', 'flat'."""
    pts = []
    if kind == "flat":
        return [(x_from, y), (x_to, y)]
    step = 3.0 if kind == "tear" else 5.0
    n = int((x_to - x_from) / step)
    for i in range(n + 1):
        x = x_from + (x_to - x_from) * i / n
        if kind == "tear":
            dy = (0.7 if i % 2 else -0.7) + rng.uniform(-0.45, 0.45)
        else:
            dy = 1.6 * math.sin(i * 0.9 + rng.uniform(0, 0.8)) + rng.uniform(-1.1, 1.1)
        pts.append((x, y + dy))
    return pts


def band_color(y_top, origin):
    """Colour of the paper at a given line top (bars are 3 lines, starting green)."""
    idx = int(round((y_top - origin) / LINE))
    return BAND if (idx // 3) % 2 == 0 else PAPER


def sheet(page, top, bottom, edge_top="tear", edge_bottom="tear", origin=None, seed=3,
          holes=True):
    """Draw a sheet of continuous green-bar paper between top and bottom.

    origin: y where the line grid (and the first green bar) starts.
    Returns the origin used.
    """
    rng = random.Random(seed)
    origin = top if origin is None else origin
    xl, xr = MARGIN, W - MARGIN
    top_pts = _edge(xl, xr, top, edge_top, rng)
    bot_pts = list(reversed(_edge(xl, xr, bottom, edge_bottom, rng)))
    d = "M" + " L".join(f"{fmt(x)} {fmt(y)}" for x, y in top_pts)
    d += " L" + " L".join(f"{fmt(x)} {fmt(y)}" for x, y in bot_pts) + "Z"
    hole_d = ""
    if holes:
        r = 5.2
        y = origin + LINE / 2
        while y < bottom - 8:
            if y > top + 8:
                for cx in (MARGIN + STRIP / 2, W - MARGIN - STRIP / 2):
                    hole_d += (f"M{fmt(cx - r)} {fmt(y)}a{r} {r} 0 1 0 {2 * r} 0"
                               f"a{r} {r} 0 1 0 {-2 * r} 0Z")
            y += LINE
    sid, cid, fid = page.uid("sheet"), page.uid("clip"), page.uid("shadow")
    page.defs.append(
        f'<filter id="{fid}" x="-3%" y="-6%" width="106%" height="114%">'
        f'<feDropShadow dx="0" dy="1.6" stdDeviation="2.4" flood-color="#000" flood-opacity="0.22"/></filter>'
        f'<path id="{sid}" d="{d}{hole_d}" fill-rule="evenodd"/>'
        f'<clipPath id="{cid}"><use href="#{sid}"/></clipPath>'
    )
    bars = []
    y = origin
    i = 0
    while y < bottom:
        if i % 2 == 0:
            bars.append(f'<rect x="{MARGIN + STRIP}" y="{fmt(y)}" width="{W - 2 * (MARGIN + STRIP)}" height="{LINE * 3}"/>')
        y += LINE * 3
        i += 1
    y = origin - LINE * 3
    i = -1
    while y + LINE * 3 > top:
        if i % 2 == 0:
            bars.append(f'<rect x="{MARGIN + STRIP}" y="{fmt(y)}" width="{W - 2 * (MARGIN + STRIP)}" height="{LINE * 3}"/>')
        y -= LINE * 3
        i -= 1
    perf = "".join(
        f'<line x1="{x}" y1="{fmt(top)}" x2="{x}" y2="{fmt(bottom)}"/>'
        for x in (MARGIN + STRIP, W - MARGIN - STRIP)
    )
    page.add(
        f'<use href="#{sid}" fill="{PAPER}" filter="url(#{fid})"/>',
        f'<g clip-path="url(#{cid})">'
        f'<g fill="{BAND}">{"".join(bars)}</g>'
        f'<g stroke="{RULE}" stroke-width="1" stroke-dasharray="2 3">{perf}</g>'
        f"</g>",
    )
    return origin


# Hand-drawn marks -------------------------------------------------------------
def _smooth(points, closed=False):
    """Catmull-Rom spline through points, as an SVG path."""
    if closed:
        pts = points[-1:] + points + points[:2]
    else:
        pts = points[:1] + points + points[-1:]
    d = f"M{fmt(pts[1][0])} {fmt(pts[1][1])}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d


def pen_loop(cx, cy, rx, ry, seed=1, turns=1.12, tilt=-4):
    """A loose hand-drawn ellipse that overshoots its start, like a pen circle."""
    rng = random.Random(seed)
    pts = []
    n = 26
    a0 = math.radians(200)
    for i in range(n + 1):
        t = a0 + 2 * math.pi * turns * i / n
        wob = 1 + rng.uniform(-0.05, 0.05) + 0.04 * i / n
        x, y = rx * wob * math.cos(t), ry * wob * math.sin(t)
        a = math.radians(tilt)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return _smooth(pts)


def pen_curve(points, seed=2, jitter=0.8):
    rng = random.Random(seed)
    pts = [(x + rng.uniform(-jitter, jitter), y + rng.uniform(-jitter, jitter)) for x, y in points]
    return _smooth(pts)


def arrow_head(tip, frm, size=9, spread=26):
    ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    pts = []
    for s in (-spread, spread):
        a = ang + math.radians(180 + s)
        pts.append((tip[0] + size * math.cos(a), tip[1] + size * math.sin(a)))
    return (f"M{fmt(pts[0][0])} {fmt(pts[0][1])}L{fmt(tip[0])} {fmt(tip[1])}"
            f"L{fmt(pts[1][0])} {fmt(pts[1][1])}")


def marker_stroke(x, y, w, h, seed=4):
    """A highlighter swipe: flat ends, slightly uneven edges."""
    rng = random.Random(seed)
    top = [(x + w * i / 8, y + rng.uniform(-1.0, 1.0)) for i in range(9)]
    bot = [(x + w * i / 8, y + h + rng.uniform(-1.0, 1.0)) for i in reversed(range(9))]
    d = f"M{fmt(x - 2)} {fmt(y + 2)}"
    for px, py in top:
        d += f"L{fmt(px)} {fmt(py)}"
    d += f"L{fmt(x + w + 3)} {fmt(y + h / 2)}"
    for px, py in bot:
        d += f"L{fmt(px)} {fmt(py)}"
    return d + "Z"


def ink_path(d, color=RED_PEN, width=2.2, delay=0.0, dur=0.6, extra=""):
    anim = f' style="animation:ink {dur:.2f}s ease-out {delay:.2f}s both"' if dur else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" pathLength="1"{anim}{extra}/>')


# Charts ------------------------------------------------------------------------
def rounded_bar_h(x, y, length, thick, r=4):
    """Horizontal bar: square at the baseline (left), 4px rounded data end."""
    r = min(r, length / 2, thick / 2)
    if length <= 0:
        return ""
    return (f"M{fmt(x)} {fmt(y)}H{fmt(x + length - r)}"
            f"A{r} {r} 0 0 1 {fmt(x + length)} {fmt(y + r)}V{fmt(y + thick - r)}"
            f"A{r} {r} 0 0 1 {fmt(x + length - r)} {fmt(y + thick)}H{fmt(x)}Z")


def rounded_bar_v(x, base_y, height, thick, r=4):
    """Vertical column: square at the baseline (bottom), 4px rounded data end."""
    r = min(r, height / 2, thick / 2)
    if height <= 0:
        return ""
    top = base_y - height
    return (f"M{fmt(x)} {fmt(base_y)}V{fmt(top + r)}"
            f"A{r} {r} 0 0 1 {fmt(x + r)} {fmt(top)}H{fmt(x + thick - r)}"
            f"A{r} {r} 0 0 1 {fmt(x + thick)} {fmt(top + r)}V{fmt(base_y)}Z")


def nice_ticks(vmax, n=4, integer=False):
    """Round tick values from 0 to at least vmax (whole numbers only if integer)."""
    if vmax <= 0:
        return [0, 1]
    raw = vmax / n
    mag = 10 ** math.floor(math.log10(raw))
    step = 10 * mag
    for m in (1, 2, 2.5, 5, 10):
        cand = m * mag
        if integer and (cand < 1 or cand != int(cand)):
            continue
        if cand >= raw:
            step = cand
            break
    top = math.ceil(vmax / step) * step
    ticks, v = [], 0.0
    while v <= top + 1e-9:
        ticks.append(v)
        v += step
    return ticks


def compact(v):
    """1,284 -> 1.3K, 4,747,963 -> 4.7M (axis ticks)."""
    v = float(v)
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(v) >= div:
            s = f"{v / div:.1f}".rstrip("0").rstrip(".")
            return s + suf
    return f"{int(v)}" if v == int(v) else f"{v:.1f}"


def thousands(v):
    return f"{int(round(v)):,}"
