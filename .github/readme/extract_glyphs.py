"""Rebuild glyphs.json from font files (dev tool, needs `pip install fonttools brotli`).

The profile graphics draw text as glyph outlines instead of <text>, so they look
identical on every OS. Fonts (all SIL Open Font License 1.1, see OFL.txt):
  mono      IBM Plex Mono 400     (@fontsource/ibm-plex-mono)
  mono-semi IBM Plex Mono 600
  dot       Doto 900              (@fontsource/doto)
  hand      Caveat 600            (@fontsource/caveat)

Usage: python3 extract_glyphs.py <fonts_dir> [out.json]
"""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen

FONTS = {
    "mono": "ibm-plex-mono-latin-400-normal.woff2",
    "mono-semi": "ibm-plex-mono-latin-600-normal.woff2",
    "dot": "doto-latin-900-normal.woff2",
    "hand": "caveat-latin-600-normal.woff2",
}
ASCII = list(range(0x20, 0x7F))
EXTRA = [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x20AC]
CODEPOINTS = {
    "mono": ASCII + list(range(0xA0, 0x100)) + EXTRA + [0x2122, 0x2191, 0x2193, 0x2212],
    "mono-semi": ASCII + list(range(0xA0, 0x100)) + EXTRA + [0x2122, 0x2191, 0x2193, 0x2212],
    "dot": ASCII + EXTRA,
    "hand": ASCII + EXTRA,
}
DOT_RADIUS = 47  # Doto's square dots (90 units on a 100-unit grid) are redrawn as round printer dots

def num(v):
    r = round(v)
    return str(int(r)) if abs(v - r) < 0.05 else f"{v:.1f}"

def dot_centers(glyph, glyphset):
    """Centres of Doto's square dots (one contour per dot)."""
    rec = RecordingPen()
    glyph.draw(rec)
    centers, pts = {}, []
    for op, args in rec.value:
        if op in ("moveTo", "lineTo", "qCurveTo", "curveTo"):
            pts.extend(a for a in args if a is not None)
        elif op in ("closePath", "endPath") and pts:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            centers[(round((min(xs) + max(xs)) / 2), round((min(ys) + max(ys)) / 2))] = True
            pts = []
    return list(centers)

def round_dots(centers, r=DOT_RADIUS):
    """Redraw each dot as a circle of radius r (printer-pin look)."""
    return "".join(f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z" for cx, cy in centers)

def extract(path, codepoints, dots=False):
    f = TTFont(path)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    os2, hhea = f["OS/2"], f["hhea"]
    out = {
        "upm": f["head"].unitsPerEm,
        "ascender": hhea.ascent,
        "descender": hhea.descent,
        "capHeight": getattr(os2, "sCapHeight", 0),
        "xHeight": getattr(os2, "sxHeight", 0),
        "glyphs": {},
    }
    for cp in codepoints:
        name = cmap.get(cp)
        if not name:
            continue
        if dots:
            d = round_dots(dot_centers(gs[name], gs))
        else:
            pen = SVGPathPen(gs, ntos=num)
            gs[name].draw(pen)
            d = pen.getCommands()
        out["glyphs"][chr(cp)] = [f["hmtx"][name][0], d]
    return out

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "glyphs.json")
    data = {"fonts": {k: extract(os.path.join(src, v), CODEPOINTS[k], dots=(k == "dot")) for k, v in FONTS.items()}}
    with open(dst, "w") as fh:
        json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
    for k, v in data["fonts"].items():
        print(k, len(v["glyphs"]), "glyphs, upm", v["upm"], "asc", v["ascender"], "desc", v["descender"], "cap", v["capHeight"], "x", v["xHeight"], "adv(A)", v["glyphs"]["A"][0])
    print("wrote", dst, os.path.getsize(dst) // 1024, "KB")
