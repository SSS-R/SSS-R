#!/usr/bin/env python3
"""Render the profile header banner as SVG, dark and light.

Static content, so this is run by hand rather than on a schedule:
    python scripts/generate_banner.py

Deliberately not a shields.io / capsule-render banner. Those are the same
assets on thousands of profiles; this one only exists here.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

W, H = 840, 208
PAD = 34

NAME = "SULTAN RAFI"
ROLE = "HARNESS   ENGINEER"
# The role label already says what I am, so this says how I move instead.
LINES = (
    "New stacks, used before the tutorials exist.",
)
META = "CS UNDERGRAD  /  BRAC UNIVERSITY  /  DHAKA, BANGLADESH"

THEMES = {
    "dark":  dict(bg="#0d1117", grid="#161b22", border="#30363d", text="#e6edf3",
                  muted="#7d8590", accent="#58a6ff", glow="#1f6feb"),
    "light": dict(bg="#ffffff", grid="#f2f4f7", border="#d0d7de", text="#1f2328",
                  muted="#59636e", accent="#0969da", glow="#54aeff"),
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def render(theme):
    t = THEMES[theme]
    o = []
    o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
             'font-family="%s">' % (W, H, W, H, MONO))

    # soft accent bloom behind the name
    o.append('<defs><radialGradient id="glow-%s" cx="50%%" cy="50%%" r="50%%">'
             '<stop offset="0%%" stop-color="%s" stop-opacity="0.20"/>'
             '<stop offset="100%%" stop-color="%s" stop-opacity="0"/></radialGradient>'
             '<clipPath id="card-%s"><rect width="%d" height="%d" rx="12"/></clipPath></defs>'
             % (theme, t["glow"], t["glow"], theme, W, H))

    o.append('<rect width="%d" height="%d" rx="12" fill="%s" stroke="%s"/>' % (W, H, t["bg"], t["border"]))
    o.append('<g clip-path="url(#card-%s)">' % theme)

    # faint engineering grid
    for x in range(0, W, 28):
        o.append('<line x1="%d" y1="0" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (x, x, H, t["grid"]))
    for y in range(0, H, 28):
        o.append('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (y, W, y, t["grid"]))

    o.append('<ellipse cx="%d" cy="%d" rx="330" ry="150" fill="url(#glow-%s)"/>' % (W // 2, H // 2, theme))

    # corner registration ticks
    for cx, cy, dx, dy in ((PAD, PAD, 1, 1), (W - PAD, PAD, -1, 1),
                           (PAD, H - PAD, 1, -1), (W - PAD, H - PAD, -1, -1)):
        o.append('<path d="M%d %d h%d M%d %d v%d" stroke="%s" stroke-width="1.5" fill="none"/>'
                 % (cx, cy, 14 * dx, cx, cy, 14 * dy, t["accent"]))

    o.append('</g>')

    cx = W // 2
    o.append('<text x="%d" y="74" fill="%s" font-size="40" font-weight="700" letter-spacing="7" '
             'text-anchor="middle">%s</text>' % (cx, t["text"], NAME))

    o.append('<line x1="%d" y1="92" x2="%d" y2="92" stroke="%s"/>' % (cx - 150, cx - 92, t["border"]))
    o.append('<text x="%d" y="97" fill="%s" font-size="11.5" font-weight="600" letter-spacing="4" '
             'text-anchor="middle">%s</text>' % (cx, t["accent"], ROLE))
    o.append('<line x1="%d" y1="92" x2="%d" y2="92" stroke="%s"/>' % (cx + 92, cx + 150, t["border"]))

    # Centre the tagline block between the role rule and the meta line, so
    # the banner stays balanced whether it carries one line or three.
    top = 140 - (len(LINES) - 1) * 10.5
    for i, line in enumerate(LINES):
        o.append('<text x="%d" y="%.1f" fill="%s" font-size="14" text-anchor="middle">%s</text>'
                 % (cx, top + i * 21, t["muted"], line))

    o.append('<text x="%d" y="186" fill="%s" font-size="9.5" letter-spacing="2.5" '
             'text-anchor="middle">%s</text>' % (cx, t["muted"], META))

    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in THEMES:
        p = os.path.join(OUT, "banner-%s.svg" % name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(render(name))
        print("wrote assets/banner-%s.svg" % name)
