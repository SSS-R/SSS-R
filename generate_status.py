#!/usr/bin/env python3
"""Render profile stat cards as self-hosted SVG.

Third-party card services (github-readme-stats and friends) rate-limit and go
down; this writes SVGs into the repo instead, so the README never shows a red
ERROR box to whoever is reading your profile.

Usage:  python scripts/generate_stats.py            # no token: skips heatmap
        GITHUB_TOKEN=... python scripts/generate_stats.py
"""
import json, os, sys, urllib.request
from collections import defaultdict
from datetime import datetime

USER = os.environ.get("STATS_USER", "SSS-R")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

W, PAD = 840, 26

THEMES = {
    "dark":  dict(bg="#0d1117", border="#30363d", text="#e6edf3", muted="#7d8590",
                  heat=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e",
                  heat=["#ebedf0", "#aceebb", "#4ac26b", "#2da44e", "#116329"]),
}

LANG_COLOR = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "Jupyter Notebook": "#DA5B0B", "Java": "#b07219", "C": "#555555",
    "CSS": "#663399", "HTML": "#e34c26", "Shell": "#89e051", "Other": "#8b949e",
}


def api(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "profile-stats", "Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"User-Agent": "profile-stats", "Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = api("https://api.github.com/users/%s" % USER)

    repos, page = [], 1
    while True:
        batch = api("https://api.github.com/users/%s/repos?per_page=100&page=%d" % (USER, page))
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]

    # Count repos per primary language, not bytes.
    #
    # Byte counts look more precise but lie here: .ipynb files embed their own
    # output (base64 images), so notebooks alone read as 68% of this account.
    # Repo `size` is worse still - it counts video and 3D assets. Repo counts
    # are what GitHub shows on the profile, and nothing about them is gameable
    # by checking in a large file.
    langs = defaultdict(int)
    for r in own:
        if r.get("language"):
            langs[r["language"]] += 1

    weeks, total_contrib = [], None
    if TOKEN:
        q = ("query($login:String!){user(login:$login){contributionsCollection{"
             "contributionCalendar{totalContributions weeks{contributionDays{contributionCount}}}}}}")
        try:
            cal = graphql(q, {"login": USER})["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            total_contrib = cal["totalContributions"]
            weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
        except Exception as e:
            print("  ! contributions unavailable: %s" % e, file=sys.stderr)

    longest = run = 0
    for n in [n for w in weeks for n in w]:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)

    return dict(user=user, repos=own, langs=dict(langs), weeks=weeks,
                total_contrib=total_contrib, longest=longest,
                stars=sum(r["stargazers_count"] for r in own))


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(d, theme):
    t = THEMES[theme]
    total = sum(d["langs"].values()) or 1
    ranked = sorted(d["langs"].items(), key=lambda kv: -kv[1])
    langs = ranked[:6]
    # Percentages are of ALL languages, not just the ones shown, so the numbers
    # on the card match reality. Whatever is left over gets one grey segment.
    rest = total - sum(v for _, v in langs)

    inner = W - PAD * 2
    by = 166                       # language bar
    hy = by + 66                   # heatmap label

    heat = bool(d["weeks"])
    gap, cell, heat_h = 3.0, 0.0, 0
    if heat:
        nw = len(d["weeks"])
        cell = (inner - gap * (nw - 1)) / nw
        heat_h = 7 * cell + 6 * gap          # cells fill the width; height follows
    H = int(hy + 16 + heat_h + 30) if heat else 208
    o = []

    o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
             'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">' % (W, H, W, H))
    o.append('<rect width="%d" height="%d" rx="12" fill="%s" stroke="%s"/>' % (W, H, t["bg"], t["border"]))

    o.append('<text x="%d" y="36" fill="%s" font-size="10.5" letter-spacing="2">BUILD LOG // %s</text>'
             % (PAD, t["muted"], esc(USER).upper()))
    o.append('<text x="%d" y="36" fill="%s" font-size="9.5" text-anchor="end">self-generated · %s</text>'
             % (W - PAD, t["muted"], datetime.utcnow().strftime("%Y-%m-%d")))
    o.append('<line x1="%d" y1="50" x2="%d" y2="50" stroke="%s"/>' % (PAD, W - PAD, t["border"]))

    c = d["total_contrib"]
    stats = [("{:,}".format(c) if c is not None else "—", "contributions / yr"),
             (str(len(d["repos"])), "public repos"),
             (str(d["longest"] or "—"), "longest streak"),
             (str(len(d["langs"])), "languages used")]
    col = inner / len(stats)
    for i, (val, label) in enumerate(stats):
        x = PAD + col * i
        o.append('<text x="%.0f" y="96" fill="%s" font-size="30" font-weight="600">%s</text>'
                 % (x, t["text"], esc(val)))
        o.append('<text x="%.0f" y="115" fill="%s" font-size="10.5">%s</text>' % (x, t["muted"], esc(label)))

    o.append('<text x="%d" y="%d" fill="%s" font-size="10.5" letter-spacing="2">LANGUAGES BY REPO</text>'
             % (PAD, by - 16, t["muted"]))
    segments = langs + ([("Other", rest)] if rest > 0 else [])
    o.append('<clipPath id="bar-%s"><rect x="%d" y="%d" width="%d" height="10" rx="5"/></clipPath>'
             % (theme, PAD, by, inner))
    o.append('<g clip-path="url(#bar-%s)">' % theme)
    x = float(PAD)
    for name, val in segments:
        seg = inner * val / total
        o.append('<rect x="%.2f" y="%d" width="%.2f" height="10" fill="%s"/>'
                 % (x, by, seg + 0.6, LANG_COLOR.get(name, LANG_COLOR["Other"])))
        x += seg
    o.append('</g>')

    ly, lx = by + 36, float(PAD)
    for name, val in segments:
        pct = 100.0 * val / total
        o.append('<circle cx="%.1f" cy="%d" r="3.6" fill="%s"/>'
                 % (lx + 4, ly - 4, LANG_COLOR.get(name, LANG_COLOR["Other"])))
        o.append('<text x="%.1f" y="%d" fill="%s" font-size="10.5">%s <tspan fill="%s">%.0f%%</tspan></text>'
                 % (lx + 14, ly, t["text"], esc(name), t["muted"], pct))
        lx += 14 + len("%s %.0f%%" % (name, pct)) * 6.3 + 26

    if heat:
        o.append('<text x="%d" y="%d" fill="%s" font-size="10.5" letter-spacing="2">LAST 12 MONTHS</text>'
                 % (PAD, hy, t["muted"]))
        peak = max((max(w) for w in d["weeks"] if w), default=0) or 1
        for wi, week in enumerate(d["weeks"]):
            for di, n in enumerate(week):
                lvl = 0 if n == 0 else min(4, 1 + int(3 * n / peak))
                o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2" fill="%s"/>'
                         % (PAD + wi * (cell + gap), hy + 16 + di * (cell + gap), cell, cell, t["heat"][lvl]))

    o.append('</svg>')
    return "\n".join(o)


def main():
    print("fetching %s ..." % USER)
    d = collect()
    print("  repos=%d stars=%d contrib=%s streak=%s langs=%d weeks=%d"
          % (len(d["repos"]), d["stars"], d["total_contrib"], d["longest"],
             len(d["langs"]), len(d["weeks"])))
    tot = sum(d["langs"].values()) or 1
    for n, v in sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]:
        print("    %-18s %5.1f%%" % (n, 100.0 * v / tot))
    os.makedirs(OUT, exist_ok=True)
    for name in THEMES:
        p = os.path.join(OUT, "stats-%s.svg" % name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(render(d, name))
        print("  wrote assets/stats-%s.svg" % name)


if __name__ == "__main__":
    main()
