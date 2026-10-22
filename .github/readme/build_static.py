"""Build the static profile graphics in assets/ (header, journey, exhibit, footer).

Edit the text in the CONTENT sections below, then run:
    python3 .github/readme/build_static.py
Every line of the printout is 80 columns wide; the script stops with an error
if a line would run off the paper.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from printshop import (  # noqa: E402
    BAND, CH, COLS, HILITE, INK, INK_2, INK_3, LINE, MARGIN, PAPER, QUIET, RED_PEN,
    RULE, SERIES, STRIP, TRACK, W, X0, X1, BASE, Page, arrow_head, band_color,
    compact, cover, fmt, ink_path, marker_stroke, nice_ticks, pen_curve, pen_loop,
    rounded_bar_h, rounded_bar_v, sheet, short_hash, thousands,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS = os.path.join(ROOT, "assets")


def check_cols(text, cols=COLS, where=""):
    if len(text) > cols:
        raise SystemExit(f"Line too long ({len(text)} > {cols} cols) {where}: {text!r}")


def row_top(origin, i):
    return origin + i * LINE


# ============================================================================
# CONTENT: header (adnan.log)
# ============================================================================
TAGLINE = [
    "AI engineer & full-stack developer, building LLM systems that show their work.",
    "MSc CS & Software Engineering @ Constructor University Bremen. From Chennai.",
]
# (date, level, message) oldest first, the way a log reads
LOG = [
    ("2025", "INFO", "2 papers: real-time vision chatbot, RL traffic-signal control"),
    ("2025", "INFO", "began freelancing: e-shop, quotation SaaS, architecture PM tool"),
    ("2026-02", "INFO", "shipped LLM pipelines on AWS as a Forward Deployed AI Engineer"),
    ("2026-05", "INFO", "graduated B.Tech in AI & Data Science, CGPA 8.36/10"),
    ("2026-09", "INFO", "moved MAA -> BRE, started MSc at Constructor University Bremen"),
    ("2026-10", "INFO", "won the SereneDB challenge at the schubKI National AI Hackathon"),
    ("now", "NOTICE", "open to Werkstudent roles in AI/ML, full-stack, data or cloud"),
]
HIGHLIGHT_ROW = 5   # which LOG entry gets the highlighter
END_OF_JOB = "-- end of job: 7 entries, 0 errors, 1 trophy --"


def header():
    top, origin = 14, 14
    bottom = row_top(origin, 22) + 2
    p = Page(bottom + MARGIN,
             "adnan.log",
             "A sheet of green-bar printer paper. Hi, I'm Adnan: " + " ".join(TAGLINE) + " Log: "
             + "; ".join(f"{d} {m}" for d, _, m in LOG) + ".")
    sheet(p, top, bottom, edge_top="rough", edge_bottom="tear", origin=origin, seed=11)

    t = 0.15   # running clock for the print sequence (seconds)

    def print_row(i, runs, speed=0.006, gap=0.05):
        """runs: list of (text, x, font, fill). Prints left to right."""
        nonlocal t
        y = row_top(origin, i)
        x_end = X0
        n = 0
        for text, x, font, fill in runs:
            w = p.put(x, y + BASE, text, font=font, fill=fill)
            x_end = max(x_end, x + w)
            n += len(text)
        dur = max(0.18, n * speed)
        p.add(cover(X0 - 2, y, x_end - X0 + 4, LINE, band_color(y, origin), t, dur, n))
        start = t
        t += dur + gap
        return start, dur

    # row 1: the print command
    cmd, page_no = "$ lpr adnan.log", "page 1"
    check_cols(cmd + "  " + page_no)
    y = row_top(origin, 1)
    p.put(X0, y + BASE, cmd, fill=INK_3)
    p.put(X1, y + BASE, page_no, fill=INK_3, anchor="end")
    p.add(cover(X0 - 2, y, X1 - X0 + 4, LINE, band_color(y, origin), t, 0.25, len(cmd) + 8))
    t += 0.35

    # the name, in dot-matrix capitals and lower case, printed column by column
    name_size = 120
    name_base = row_top(origin, 7) + 10
    w = p.put(X0 - 4, name_base, "Adnan", font="dot", size=name_size, fill=INK)
    for band_start in (3, 6):
        yb = row_top(origin, band_start)
        yt = max(yb, name_base - 92)
        ye = min(row_top(origin, band_start + 3), name_base + 6)
        p.add(cover(X0 - 6, yt, w + 10, ye - yt, band_color(yb, origin), t, 0.9, 25))
    t += 1.0

    # handwritten greeting above the name
    g, _ = p.text(0, 0, "hi, I'm", font="hand", size=30, fill=RED_PEN)
    p.add(f'<g transform="translate({X0 + 2} {row_top(origin, 3) + 2}) rotate(-4)">'
          f'<g style="animation:appear .5s ease-out {t:.2f}s both">{g}</g></g>')
    t += 0.3

    # tagline
    for k, line in enumerate(TAGLINE):
        check_cols(line, where="tagline")
        print_row(9 + k, [(line, X0, "mono", INK_2)], speed=0.005)

    t += 0.1
    # log entries
    win_row = None
    for k, (date, level, msg) in enumerate(LOG):
        prefix = f"{date:<9}{level:<8}"
        check_cols(prefix + msg, where="log")
        i = 12 + k
        y = row_top(origin, i)
        if k == HIGHLIGHT_ROW:
            win_row = (i, X0 + len(prefix) * CH, len(msg) * CH)
            # the highlighter goes under the text; it swipes in after the line prints
            hx, hw = win_row[1] - 3, win_row[2] + 6
            p.add(f'<path d="{marker_stroke(hx, y + 3, hw, LINE - 6, seed=5)}" fill="{HILITE}" '
                  f'style="mix-blend-mode:multiply;animation:swipe .55s ease-out {t + 0.55:.2f}s both" '
                  f'class="swipe" opacity="0.85"/>')
        font_msg = "mono-semi" if level == "NOTICE" else "mono"
        start, dur = print_row(i, [(prefix, X0, "mono", INK_3), (msg, X0 + len(prefix) * CH, font_msg, INK)],
                               speed=0.0055, gap=0.1)
        if level == "NOTICE":
            # a block cursor that keeps blinking after the job finishes
            cx = X0 + (len(prefix) + len(msg) + 1) * CH
            p.add(f'<g style="animation:appear .01s linear {t:.2f}s both">'
                  f'<rect x="{fmt(cx)}" y="{y + 4}" width="{CH:.1f}" height="16" fill="{INK}" '
                  f'style="animation:blink 1.1s steps(1,end) {t:.2f}s infinite"/></g>')

    # end of job
    t += 0.2
    check_cols(END_OF_JOB)
    print_row(20, [(END_OF_JOB, X0, "mono", INK_3)], speed=0.004)

    # rubber stamp: the latest win, thumped on at the end
    stamp(p, cx=X1 - 150, cy=row_top(origin, 5) + 2, delay=t + 0.1)
    return p


def stamp(p, cx, cy, delay):
    w, h = 270, 116
    x, y = -w / 2, -h / 2
    rng = random.Random(21)
    mid = p.uid("wear")
    specks = "".join(
        f'<circle cx="{fmt(rng.uniform(x, x + w))}" cy="{fmt(rng.uniform(y, y + h))}" r="{fmt(rng.uniform(0.4, 1.5))}"/>'
        for _ in range(240)
    )
    scratches = "".join(
        f'<path d="M{fmt(a)} {fmt(b)}l{fmt(rng.uniform(6, 22))} {fmt(rng.uniform(-2, 2))}" stroke-width="{fmt(rng.uniform(0.6, 1.4))}"/>'
        for a, b in ((rng.uniform(x, x + w), rng.uniform(y, y + h)) for _ in range(14))
    )
    p.defs.append(
        f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}">'
        f'<rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" fill="#fff"/>'
        f'<g fill="#000">{specks}</g><g stroke="#000" stroke-linecap="round">{scratches}</g></mask>'
    )
    t1, _ = p.text(0, -6, "Winner", font="mono-semi", size=38, fill=RED_PEN, anchor="middle")
    t2, _ = p.text(0, 22, "SereneDB challenge", font="mono-semi", size=15, fill=RED_PEN, anchor="middle")
    t3, _ = p.text(0, 42, "schubKI National AI Hackathon '26", font="mono", size=11.5, fill=RED_PEN, anchor="middle")
    p.css.append(
        "@keyframes thump{0%{opacity:0;transform:scale(1.6)}70%{opacity:1;transform:scale(.96)}100%{opacity:1;transform:scale(1)}}"
        ".thump{transform-box:fill-box;transform-origin:50% 50%}"
    )
    p.add(
        f'<g transform="translate({fmt(cx)} {fmt(cy)}) rotate(-7)" opacity="0.88">'
        f'<g class="thump" style="animation:thump .45s cubic-bezier(.2,.8,.3,1) {delay:.2f}s both">'
        f'<g mask="url(#{mid})">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="{RED_PEN}" stroke-width="4"/>'
        f'<rect x="{x + 8}" y="{y + 8}" width="{w - 16}" height="{h - 16}" rx="5" fill="none" stroke="{RED_PEN}" stroke-width="1.5"/>'
        f"{t1}{t2}{t3}</g></g></g>"
    )


# ============================================================================
# CONTENT: journey (git log --graph)
# ============================================================================
LANES = ["main", "work", "freelance", "research", "hackathons"]
# newest first, like git log: (lane, decoration, message, date)
COMMITS = [
    (0, "HEAD -> main", "wip: open to Werkstudent roles in Germany", "now"),
    (4, "tag: winner", "won the SereneDB challenge at schubKI 2026", "2026-10"),
    (0, "", "move MAA -> BRE, start MSc at Constructor University", "2026-09"),
    (0, "", "Merge branch 'freelance'", "2026-09"),
    (2, "", "build Archivio, a project tracker for an architecture firm", "2026"),
    (0, "tag: b.tech", "graduate B.Tech AI & Data Science, CGPA 8.36", "2026-05"),
    (2, "", "ship AI quotation SaaS: RFQ -> line items -> quote", "2026"),
    (1, "", "join SARAEdx Foundry as Forward Deployed AI Engineer", "2026-02"),
    (2, "", "launch Morrick's Keep Coffee store (Next.js, Supabase)", "2026"),
    (0, "", "pass IELTS (band 8.0) and Oracle OCI AI Foundations", "2025"),
    (3, "", "publish hybrid edge-based RL traffic-signal control", "2025"),
    (2, "", "start freelancing as a full-stack developer", "2025"),
    (4, "", "place top 5 of 60 teams at SRM Hackforge '25", "2025"),
    (3, "", "present real-time vision chatbot paper at NCAIBIA 2025", "2025"),
    (1, "", "intern full-stack (React, Spring Boot) at Scrapify Ecotech", "2024-12"),
    (1, "", "intern as data analyst at National Trading Co.", "2024-05"),
    (0, "", "lead Youth Red Cross as department coordinator", "2023-10"),
    (0, "", "init B.Tech AI & DS at Velammal Engineering College", "2022-08"),
]
# merges into main: row of the merge commit -> lanes merged there
MERGES = {3: [2], 5: [3, 1]}


def journey():
    top = origin = 14
    first = 4                      # grid row of the newest commit
    n = len(COMMITS)
    bottom = row_top(origin, first + n + 1) + 2
    p = Page(bottom + MARGIN, "git log --graph adnan",
             "My history as a git graph, newest first: "
             + "; ".join(f"{d}: {m}" for _, _, m, d in COMMITS) + ".")
    sheet(p, top, bottom, edge_top="tear", edge_bottom="tear", origin=origin, seed=23)

    size, ch = 15, 9.0             # this sheet prints at 12 cpi for more columns
    cols = int((X1 - X0) / ch)     # 85
    lane_dx, lane_x0 = 18, X0 + 9
    hash_col, msg_col = 11, 19

    def lane_x(l):
        return lane_x0 + l * lane_dx

    def cy(r):
        return row_top(origin, first + r) + LINE / 2

    # header rows
    y = row_top(origin, 1)
    p.put(X0, y + BASE, "$ git log --graph --oneline --decorate", fill=INK_3)
    p.put(X1, y + BASE, "page 3", fill=INK_3, anchor="end")
    y = row_top(origin, 2)
    x = X0
    for i, name in enumerate(LANES):
        p.add(f'<circle cx="{fmt(x + 5)}" cy="{fmt(y + 12)}" r="4.5" fill="{SERIES[i]}"/>')
        x += 16
        x += p.put(x, y + BASE - 1, name, size=14, fill=INK_2) + 22

    # which lanes are alive between rows r and r+1 (r newer)
    first_row = {}
    last_row = {}
    for r, (l, *_rest) in enumerate(COMMITS):
        first_row[l] = max(first_row.get(l, -1), r)     # oldest commit (largest r)
        last_row.setdefault(l, r)                        # newest commit (smallest r)
    merged_at = {l: r for r, ls in MERGES.items() for l in ls}

    paths = {l: [] for l in range(len(LANES))}
    for l in range(len(LANES)):
        if l == 0:
            paths[0].append(f"M{fmt(lane_x(0))} {fmt(cy(n - 1))}V{fmt(cy(0))}")
            continue
        lo, hi = first_row[l], last_row[l]
        # fork: the branch's oldest commit sits one row above where it leaves main
        x_l, x_m = lane_x(l), lane_x(0)
        y_a, y_b = cy(lo), cy(lo + 1)
        paths[l].append(f"M{fmt(x_m)} {fmt(y_b)}C{fmt(x_m)} {fmt(y_b - 9)} {fmt(x_l)} {fmt(y_a + 9)} {fmt(x_l)} {fmt(y_a)}")
        # trunk of the branch
        end_r = merged_at[l] + 1 if l in merged_at else hi
        if end_r < lo:
            paths[l].append(f"M{fmt(x_l)} {fmt(cy(lo))}V{fmt(cy(end_r))}")
        if l in merged_at:
            y_a, y_b = cy(end_r), cy(merged_at[l])
            paths[l].append(f"M{fmt(x_l)} {fmt(y_a)}C{fmt(x_l)} {fmt(y_a - 9)} {fmt(x_m)} {fmt(y_b + 9)} {fmt(x_m)} {fmt(y_b)}")

    graph = []
    for l in reversed(range(len(LANES))):   # main on top of the crossings
        graph.append(f'<path d="{"".join(paths[l])}" fill="none" stroke="{SERIES[l]}" stroke-width="2" '
                     f'stroke-linecap="round"/>')
    for r, (l, deco, msg, date) in enumerate(COMMITS):
        ring = band_color(row_top(origin, first + r), origin)
        x, yc = lane_x(l), cy(r)
        if deco.startswith("HEAD"):
            graph.append(f'<circle cx="{fmt(x)}" cy="{fmt(yc)}" r="6.5" fill="{ring}"/>'
                         f'<circle cx="{fmt(x)}" cy="{fmt(yc)}" r="4.6" fill="{ring}" stroke="{SERIES[l]}" '
                         f'stroke-width="2" stroke-dasharray="2.4 1.8"/>')
        else:
            graph.append(f'<circle cx="{fmt(x)}" cy="{fmt(yc)}" r="6.5" fill="{ring}"/>'
                         f'<circle cx="{fmt(x)}" cy="{fmt(yc)}" r="4.5" fill="{SERIES[l]}"/>')
    p.add("<g>" + "".join(graph) + "</g>")

    # growth: the graph area is uncovered from the oldest row up to HEAD
    gx0, gx1 = X0 - 2, X0 + hash_col * ch - 6
    for r in range(n):
        rt = row_top(origin, first + r)
        delay = 0.25 + (n - 1 - r) * 0.13
        p.add(f'<rect x="{fmt(gx0)}" y="{fmt(rt)}" width="{fmt(gx1 - gx0)}" height="{LINE}" '
              f'fill="{band_color(rt, origin)}" opacity="0" '
              f'style="animation:appear .2s linear {delay:.2f}s both reverse"/>')

    # text columns
    for r, (l, deco, msg, date) in enumerate(COMMITS):
        line = (f"({deco}) " if deco else "") + msg
        if hash_col + 8 + len(line) + len(date) + 1 > cols:
            raise SystemExit(f"journey row too long: {line!r}")
        yb = row_top(origin, first + r) + BASE
        p.put(X0 + hash_col * ch, yb, short_hash(msg + date), size=size, fill=INK_3)
        x = X0 + msg_col * ch
        if deco:
            x += p.put(x, yb, f"({deco}) ", font="mono-semi", size=size, fill=INK)
        p.put(x, yb, msg, size=size, fill=INK)
        p.put(X1, yb, date, size=size, fill=INK_3, anchor="end")
    return p


# ============================================================================
# CONTENT: exhibit (the SereneDB challenge win, by the numbers)
# All figures come from the team's pitch and repo; each is re-runnable SQL.
# ============================================================================
EXHIBIT_LINES = [
    "Role-aware log intelligence over SereneDB, built in 48 hours",
    "by team Logging off Early: @Arnie1x and me.",
]
EXHIBIT_RULE = "SQL computes, the LLM explains: every number comes with its query."
KPIS = [
    ("15/15", ["eval questions match", "golden SQL"]),
    ("13 ms", ["phrase + facet search", "over 5.28M rows"]),
    ("~20 s", ["full rebuild from", "raw logs"]),
    ("48 h", ["team of two,", "200+ participants"]),
]
VOLUME = [("OTel slice", 5_275_597), ("BGL", 4_747_963), ("OpenStack", 207_812)]
VOLUME_NOTE = "OTel: a 10-s slice of a 1B-row file"
GAPS = [("1 min", 132), ("5 min", 117), ("60 min", 57)]
GAP_FOCUS = 1
SIGNATURE = ("data TLB error interrupt", 152_734, 152_182)   # lines, lines on the busiest node
EVIDENCE = ['> verify_evidence("E-55EF08")', "MATCH: 19,250 rows recorded, 19,250 now"]
EXHIBIT_REPO = "github.com/Arnie1x/exhibit"

TROPHY = [
    "...XXXXXXXXX...",
    "XXXXXXXXXXXXXXX",
    "X..XXXXXXXXX..X",
    "X..XXXXXXXXX..X",
    ".X.XXXXXXXXX.X.",
    "..XXXXXXXXXXX..",
    "....XXXXXXX....",
    "......XXX......",
    "......XXX......",
    ".....XXXXX.....",
    "...XXXXXXXXX...",
    "...XXXXXXXXX...",
]


def exhibit():
    top = origin = 14
    bottom = row_top(origin, 29) + 2
    alt = ("Exhibit, our winning project at the schubKI National AI Hackathon 2026. "
           + " ".join(EXHIBIT_LINES) + " " + EXHIBIT_RULE + " "
           + " ".join(f"{v} {' '.join(l)}." for v, l in KPIS)
           + " Log lines parsed and indexed: " + ", ".join(f"{k} {thousands(v)}" for k, v in VOLUME)
           + f" ({VOLUME_NOTE}). Incidents found at an episode gap of "
           + ", ".join(f"{k}: {v}" for k, v in GAPS)
           + f". {thousands(SIGNATURE[1])} '{SIGNATURE[0]}' lines, {SIGNATURE[2] / SIGNATURE[1]:.2%} of them from one node.")
    p = Page(bottom + MARGIN, "Exhibit: SereneDB challenge winner", alt)
    sheet(p, top, bottom, edge_top="tear", edge_bottom="tear", origin=origin, seed=31)
    t = 0.2

    y = row_top(origin, 1)
    p.put(X0, y + BASE, "$ lpr exhibit-results.txt", fill=INK_3)
    p.put(X1, y + BASE, "page 2", fill=INK_3, anchor="end")

    # title block
    name_base = row_top(origin, 5) + 2
    p.put(X0 - 4, name_base, "Exhibit", font="dot", size=66, fill=INK, track=-5)
    for k, line in enumerate(EXHIBIT_LINES):
        check_cols(line, cols=60, where="exhibit")
        p.put(X0, row_top(origin, 6 + k) + BASE, line, fill=INK if k == 0 else INK_2)
    check_cols(EXHIBIT_RULE)
    p.put(X0, row_top(origin, 9) + BASE, EXHIBIT_RULE, font="mono-semi", fill=INK)

    # trophy, printed as a dot bitmap, with a pen note
    pitch, r = 7.4, 3.0
    tx = X1 - len(TROPHY[0]) * pitch - 6
    ty = row_top(origin, 3) + 4
    for j, row in enumerate(TROPHY):
        dots = "".join(f'<circle cx="{fmt(tx + i * pitch)}" cy="{fmt(ty + j * pitch)}" r="{r}"/>'
                       for i, c in enumerate(row) if c == "X")
        p.add(f'<g fill="{INK}" style="animation:appear .08s linear {t + 0.05 * j:.2f}s both">{dots}</g>')
    tcx = tx + (len(TROPHY[0]) - 1) * pitch / 2
    tcy = ty + (len(TROPHY) - 1) * pitch / 2
    note_t = t + 0.05 * len(TROPHY) + 0.2
    p.add(ink_path(pen_loop(tcx, tcy, 72, 54, seed=7, tilt=-6), delay=note_t, dur=0.7))
    g, gw = p.text(0, 0, "we won!", font="hand", size=30, fill=RED_PEN)
    nx, ny = tcx - 190, row_top(origin, 5) + 6
    p.add(f'<g transform="translate({fmt(nx)} {fmt(ny)}) rotate(-5)">'
          f'<g style="animation:appear .4s ease-out {note_t + 0.6:.2f}s both">{g}</g></g>')
    tip = (tcx - 76, tcy - 4)
    p.add(ink_path(pen_curve([(nx + gw + 6, ny - 10), (nx + gw + 26, ny - 22), tip], seed=3),
                   delay=note_t + 0.8, dur=0.35))
    p.add(ink_path(arrow_head(tip, (nx + gw + 26, ny - 22), size=9),
                   delay=note_t + 1.1, dur=0.15))

    # KPI tiles
    tile_w = (X1 - X0) / len(KPIS)
    ky = row_top(origin, 11)
    for i, (value, label) in enumerate(KPIS):
        x = X0 + i * tile_w + (14 if i else 0)
        if i:
            p.add(f'<line x1="{fmt(X0 + i * tile_w)}" y1="{ky + 4}" x2="{fmt(X0 + i * tile_w)}" y2="{ky + 68}" '
                  f'stroke="{RULE}" stroke-width="1"/>')
        g, _ = p.text(x, ky + 30, value, font="mono-semi", size=30, fill=INK)
        p.add(f'<g style="animation:appear .3s ease-out {t + 0.3 + 0.12 * i:.2f}s both">{g}</g>')
        for j, line in enumerate(label):
            p.put(x, ky + 50 + j * 16, line, size=13, fill=INK_3)

    # chart 1: volumes (horizontal bars, one series)
    cy0 = row_top(origin, 15)
    p.put(X0, cy0 + BASE, "Log lines parsed and indexed", font="mono-semi", size=14, fill=INK)
    label_w, bar_x = 100, X0 + 100
    bar_max = 168
    vmax = max(v for _, v in VOLUME)
    for i, (name, v) in enumerate(VOLUME):
        by = cy0 + 34 + i * 30
        p.put(X0, by + 11, name, size=13, fill=INK_2)
        length = bar_max * v / vmax
        p.add(f'<path class="swipe" d="{rounded_bar_h(bar_x, by, max(length, 2), 14)}" fill="{SERIES[0]}" '
              f'style="animation:swipe .7s cubic-bezier(.2,.7,.2,1) {t + 0.9 + 0.12 * i:.2f}s both"/>')
        p.put(bar_x + length + 8, by + 11, thousands(v), size=13, fill=INK)
    p.add(f'<line x1="{bar_x}" y1="{cy0 + 28}" x2="{bar_x}" y2="{cy0 + 28 + 30 * len(VOLUME)}" stroke="{RULE}"/>')
    p.put(X0, cy0 + 34 + 30 * len(VOLUME) + 14, VOLUME_NOTE, size=12, fill=INK_3)

    # chart 2: incidents vs episode gap (columns, one in focus)
    px0 = X0 + 420
    p.put(px0, cy0 + BASE, "Incidents found vs. episode gap", font="mono-semi", size=14, fill=INK)
    base_y = cy0 + 30 + 104
    col_w, col_gap = 22, 56
    gmax = max(v for _, v in GAPS)
    for i, (name, v) in enumerate(GAPS):
        x = px0 + 18 + i * (col_w + col_gap)
        h = 88 * v / gmax
        color = SERIES[0] if i == GAP_FOCUS else QUIET
        p.add(f'<path class="rise" d="{rounded_bar_v(x, base_y, h, col_w)}" fill="{color}" '
              f'style="animation:rise .6s cubic-bezier(.2,.7,.2,1) {t + 1.2 + 0.12 * i:.2f}s both"/>')
        p.put(x + col_w / 2, base_y - h - 7, str(v), size=13, fill=INK, anchor="middle")
        p.put(x + col_w / 2, base_y + 17, name, size=13, fill=INK_2, anchor="middle")
    cols_end = px0 + 18 + len(GAPS) * (col_w + col_gap) - col_gap
    p.add(f'<line x1="{px0}" y1="{base_y}" x2="{fmt(cols_end + 18)}" y2="{base_y}" stroke="{RULE}"/>')
    for j, line in enumerate(["every answer", "states the gap", "it counted with"]):
        p.put(cols_end + 34, base_y - 66 + 16 * j, line, size=12, fill=INK_3)

    # meter: one machine, not the fleet
    my = row_top(origin, 22)
    sig, total, top_node = SIGNATURE
    p.put(X0, my + BASE, "One machine, not the fleet", font="mono-semi", size=14, fill=INK)
    p.put(X1, my + BASE, f'{thousands(total)} "{sig}" lines', size=13, fill=INK_2, anchor="end")
    bar_y = my + 32
    full = X1 - X0
    p.add(f'<path d="{rounded_bar_h(X0, bar_y, full, 14)}" fill="{TRACK}"/>')
    share = top_node / total
    p.add(f'<path class="swipe" d="{rounded_bar_h(X0, bar_y, full * share, 14)}" fill="{SERIES[0]}" '
          f'style="animation:swipe 1.1s cubic-bezier(.2,.7,.2,1) {t + 1.6:.2f}s both"/>')
    p.put(X0, bar_y + 34, f"1 node: {thousands(top_node)} lines ({share:.2%})", size=13, fill=INK)
    p.put(X1, bar_y + 34, f"every other node: {thousands(total - top_node)}", size=13, fill=INK_2, anchor="end")

    # evidence footer
    ey = row_top(origin, 26)
    p.put(X0, ey + BASE, EVIDENCE[0], fill=INK_2)
    p.put(X0, ey + LINE + BASE, EVIDENCE[1], fill=INK)
    p.put(X1, ey + LINE + BASE, EXHIBIT_REPO, fill=INK_3, anchor="end")
    return p


# ============================================================================
# CONTENT: footer
# ============================================================================
FOOTER_LINES = ["$ exit", "logout", "", "[Process completed]"]


def footer():
    top = origin = 14
    bottom = row_top(origin, 6) + 4
    p = Page(bottom + MARGIN, "end of adnan.log", "The end of the printout: exit, logout, process completed. Thanks for reading!")
    sheet(p, top, bottom, edge_top="tear", edge_bottom="rough", origin=origin, seed=41)
    for k, line in enumerate(FOOTER_LINES):
        if line:
            p.put(X0, row_top(origin, 1 + k) + BASE, line, fill=INK_3 if k else INK_2)
    g, gw = p.text(0, 0, "thanks for reading, say hi!", font="hand", size=30, fill=RED_PEN)
    p.add(f'<g transform="translate({fmt(X1 - gw - 10)} {row_top(origin, 3) + 14}) rotate(-4)">{g}</g>')
    return p


# ============================================================================
# main
# ============================================================================
BUILDERS = {"header": header, "exhibit": exhibit, "journey": journey, "footer": footer}

if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    names = sys.argv[1:] or list(BUILDERS)
    for name in names:
        page = BUILDERS[name]()
        path = page.save(os.path.join(ASSETS, f"{name}.svg"))
        print(f"{path}  {os.path.getsize(path) // 1024} KB")
