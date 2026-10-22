"""Print the nightly GitHub activity sheet (stats.svg) for the profile README.

Runs in GitHub Actions with the built-in token, no packages needed:
    GITHUB_TOKEN=... python3 .github/readme/stats.py --user AdnanSN --out dist/stats.svg
Preview without network:
    python3 .github/readme/stats.py --user AdnanSN --mock sample.json --out stats.svg
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from printshop import (  # noqa: E402
    BASE, CH, INK, INK_2, INK_3, LINE, MARGIN, QUIET, RULE, SERIES, X0, X1,
    Page, band_color, compact, fmt, nice_ticks, sheet, thousands,
)

# Notebooks store their outputs, which drowns out real code; leave them out.
EXCLUDE_LANGS = {"Jupyter Notebook"}
# Colour follows the language, not its rank, so a language keeps its colour
# from night to night. Anything else is folded into "Other".
LANG_SLOT = {"Python": 0, "TypeScript": 1, "JavaScript": 2, "HTML": 3,
             "CSS": 4, "Java": 5, "C++": 6, "C": 7}
TOP_LANGS = 5

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes {
        isPrivate
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(user, token):
    body = json.dumps({"query": QUERY, "variables": {"login": user}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.load(res)
    if data.get("errors"):
        raise SystemExit(f"GitHub API error: {data['errors']}")
    return data["data"]["user"]


def summarise(user):
    cc = user["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    weekly = [(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"]))
              for w in weeks if w["contributionDays"]]
    repos = user["repositories"]["nodes"]
    public = [r for r in repos if not r["isPrivate"]]
    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in EXCLUDE_LANGS:
                sizes[name] = sizes.get(name, 0) + e["size"]
    return {
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "stars": sum(r["stargazerCount"] for r in public),
        "repos": len(public),
        "followers": user["followers"]["totalCount"],
        "weekly": weekly,
        "languages": sorted(sizes.items(), key=lambda kv: -kv[1]),
    }


def render(user_login, s, today):
    top = origin = 14
    bottom = top + 19 * LINE + 2
    weekly = s["weekly"]
    peak_i = max(range(len(weekly)), key=lambda i: weekly[i][1]) if weekly else 0
    total_bytes = sum(v for _, v in s["languages"]) or 1
    langs = [(n, v) for n, v in s["languages"] if n in LANG_SLOT][:TOP_LANGS]
    other = total_bytes - sum(v for _, v in langs) if s["languages"] else 0
    if other:
        langs = langs + [("Other", other)]
    desc = (f"GitHub activity for {user_login}, printed {today}: {s['contributions']} contributions in the "
            f"last 12 months, {s['commits']} commits, {s['repos']} public repos, {s['stars']} stars. "
            "Languages by code size: " + ", ".join(f"{n} {pct(v / total_bytes)}" for n, v in langs) + ".")
    p = Page(bottom + MARGIN, f"{user_login} on GitHub", desc)
    sheet(p, top, bottom, edge_top="tear", edge_bottom="tear", origin=origin, seed=53)

    y = origin + LINE
    p.put(X0, y + BASE, f"$ gh-stats {user_login} --last 12mo", fill=INK_3)
    p.put(X1, y + BASE, f"printed {today}", fill=INK_3, anchor="end")

    # KPI tiles
    kpis = [
        (thousands(s["contributions"]), ["contributions in", "the last 12 months"]),
        (thousands(s["commits"]), ["commits", "in the same period"]),
        (thousands(s["repos"]), ["public repositories", "of my own"]),
        (thousands(s["stars"]), ["stars earned", "across them"]),
    ]
    tile_w = (X1 - X0) / len(kpis)
    ky = origin + 3 * LINE
    for i, (value, label) in enumerate(kpis):
        x = X0 + i * tile_w + (14 if i else 0)
        if i:
            p.add(f'<line x1="{fmt(X0 + i * tile_w)}" y1="{ky + 4}" x2="{fmt(X0 + i * tile_w)}" y2="{ky + 68}" stroke="{RULE}"/>')
        g, _ = p.text(x, ky + 30, value, font="mono-semi", size=30, fill=INK)
        p.add(f'<g style="animation:appear .3s ease-out {0.2 + 0.1 * i:.2f}s both">{g}</g>')
        for j, line in enumerate(label):
            p.put(x, ky + 50 + j * 16, line, size=13, fill=INK_3)

    # weekly contributions: one series, line + wash
    cy0 = origin + 7 * LINE
    p.put(X0, cy0 + BASE, "Contributions per week", font="mono-semi", size=14, fill=INK)
    plot_x0, plot_x1 = X0 + 34, X1 - 4
    plot_top, plot_bot = cy0 + 40, cy0 + 40 + 104
    vmax = max([c for _, c in weekly] + [1])
    ticks = nice_ticks(max(vmax, 4), 3, integer=True)
    ymax = ticks[-1]

    def sx(i):
        return plot_x0 + (plot_x1 - plot_x0) * (i / max(len(weekly) - 1, 1))

    def sy(v):
        return plot_bot - (plot_bot - plot_top) * v / ymax

    grid = []
    for tv in ticks:
        yv = sy(tv)
        grid.append(f'<line x1="{plot_x0}" y1="{fmt(yv)}" x2="{plot_x1}" y2="{fmt(yv)}"/>')
        p.put(plot_x0 - 8, yv + 4, compact(tv), size=12, fill=INK_3, anchor="end")
    p.add(f'<g stroke="{RULE}" stroke-width="1">{"".join(grid)}</g>')
    last_month = None
    for i, (date, _) in enumerate(weekly):
        d = dt.date.fromisoformat(date)
        if d.month != last_month and d.day <= 7:
            p.put(sx(i), plot_bot + 18, d.strftime("%b"), size=12, fill=INK_3, anchor="middle")
            last_month = d.month
    if weekly:
        pts = [(sx(i), sy(c)) for i, (_, c) in enumerate(weekly)]
        line = "M" + " L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)
        area = line + f" L{fmt(pts[-1][0])} {fmt(plot_bot)} L{fmt(pts[0][0])} {fmt(plot_bot)}Z"
        p.add(f'<path d="{area}" fill="{SERIES[0]}" fill-opacity="0.1" style="animation:appear .6s ease-out 1.4s both"/>')
        p.add(f'<path d="{line}" fill="none" stroke="{SERIES[0]}" stroke-width="2" stroke-linejoin="round" '
              f'stroke-linecap="round" pathLength="1" style="animation:ink 1.4s ease-in-out .3s both"/>')
        px, py = pts[peak_i]
        if weekly[peak_i][1] > 0:
            ring = band_color(origin + int((py - origin) // LINE) * LINE, origin)
            p.add(f'<circle cx="{fmt(px)}" cy="{fmt(py)}" r="6" fill="{ring}" style="animation:appear .3s 1.6s both"/>'
                  f'<circle cx="{fmt(px)}" cy="{fmt(py)}" r="4" fill="{SERIES[0]}" style="animation:appear .3s 1.6s both"/>')
            w0 = dt.date.fromisoformat(weekly[peak_i][0])
            w1 = w0 + dt.timedelta(days=6)
            span = (f"{w0.day}\u2013{w1.day} {w1:%b}" if w0.month == w1.month
                    else f"{w0.day} {w0:%b}\u2013{w1.day} {w1:%b}")
            label = f"busiest week: {weekly[peak_i][1]} ({span})"
            anchor = "end" if px > (plot_x0 + plot_x1) / 2 else "start"
            ly_ = max(py - 8, plot_top - 6)
            halo = band_color(origin + int((ly_ - 6 - origin) // LINE) * LINE, origin)
            lx_ = px + (-10 if anchor == "end" else 10)
            g, lw = p.text(lx_, ly_, label, size=12, fill=INK, anchor=anchor)
            bx = lx_ - lw if anchor == "end" else lx_
            p.add(f'<rect x="{fmt(bx - 4)}" y="{fmt(ly_ - 12)}" width="{fmt(lw + 8)}" height="16" fill="{halo}"/>', g)

    # languages: part-to-whole, one stacked bar with surface gaps
    ly = origin + 15 * LINE
    p.put(X0, ly + BASE, "Languages by code size", font="mono-semi", size=14, fill=INK)
    p.put(X1, ly + BASE, "public repos, notebooks excluded", size=12, fill=INK_3, anchor="end")
    bar_y, bar_h = ly + 32, 14
    if langs:
        x = X0
        full = X1 - X0
        segs = []
        for k, (name, v) in enumerate(langs):
            w = full * v / total_bytes
            color = SERIES[LANG_SLOT[name]] if name in LANG_SLOT else QUIET
            gap = 2 if k < len(langs) - 1 else 0
            r_left = 4 if k == 0 else 0
            r_right = 4 if k == len(langs) - 1 else 0
            segs.append(_seg(x, bar_y, max(w - gap, 0.5), bar_h, r_left, r_right, color))
            x += w
        p.add(f'<g class="swipe" style="animation:swipe .9s cubic-bezier(.2,.7,.2,1) .5s both">{"".join(segs)}</g>')
        lx = X0
        legend_y = bar_y + 40
        for name, v in langs:
            color = SERIES[LANG_SLOT[name]] if name in LANG_SLOT else QUIET
            label = f"{name} {pct(v / total_bytes)}"
            p.add(f'<circle cx="{fmt(lx + 5)}" cy="{fmt(legend_y - 4)}" r="4.5" fill="{color}"/>')
            lx += 16 + p.put(lx + 16, legend_y, label, size=13, fill=INK_2) + 22
    else:
        p.put(X0, bar_y + 12, "no public code yet", size=13, fill=INK_3)
    return p


def pct(share):
    return "<1%" if 0 < share < 0.005 else f"{share:.0%}"


def _seg(x, y, w, h, rl, rr, color):
    rl, rr = min(rl, w / 2), min(rr, w / 2)
    d = (f"M{fmt(x + rl)} {fmt(y)}H{fmt(x + w - rr)}"
         + (f"A{rr} {rr} 0 0 1 {fmt(x + w)} {fmt(y + rr)}V{fmt(y + h - rr)}A{rr} {rr} 0 0 1 {fmt(x + w - rr)} {fmt(y + h)}" if rr else f"H{fmt(x + w)}V{fmt(y + h)}")
         + f"H{fmt(x + rl)}"
         + (f"A{rl} {rl} 0 0 1 {fmt(x)} {fmt(y + h - rl)}V{fmt(y + rl)}A{rl} {rl} 0 0 1 {fmt(x + rl)} {fmt(y)}" if rl else f"H{fmt(x)}V{fmt(y)}")
         + "Z")
    return f'<path d="{d}" fill="{color}"/>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", default="stats.svg")
    ap.add_argument("--mock", help="read a saved API response instead of calling GitHub")
    a = ap.parse_args()
    if a.mock:
        with open(a.mock, encoding="utf-8") as fh:
            user = json.load(fh)
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("Set GITHUB_TOKEN")
        user = fetch(a.user, token)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    page = render(a.user, summarise(user), today)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    page.save(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
