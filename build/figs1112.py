"""Diagrams for sessions 11 and 12, drawn as inline SVG.

Every number and every path comes from running the classes in sparks_parallel.py,
plume.py and orbit.py, so the pictures cannot drift from the programs.
"""

import contextlib
import io
import math
import os
import random

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

_HERE = os.path.dirname(os.path.abspath(__file__))
# Same two layouts as crosscheck.py: programs in ./prog during development,
# or in the repo root, one level up, once shipped.
PROG = os.path.join(_HERE, "prog") if os.path.isdir(os.path.join(_HERE, "prog")) \
    else os.path.dirname(_HERE)

INK = "#17181B"
SOFT = "#4A4D53"
TEAL = "#0E4D52"
CLAY = "#9C2B22"
OCHRE = "#D99B12"
CARD = "#FFFDF7"
TINT = "#FBF2DC"
CLAY_TINT = "#F6DDD8"
RULE = "#B9AF96"
PLANET = "#C68E3C"
MONO = "'JetBrains Mono',monospace"


def _source(name):
    with open(os.path.join(PROG, name)) as f:
        return f.read()


def _namespace(name, stop):
    """Run a program up to the line that opens its window, and return its names."""
    ns = {"__name__": "figure"}
    exec(compile(_source(name).split(stop)[0], name, "exec"), ns)
    return ns


def _svg(w, h, label, parts):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" style="max-width:100%; height:auto; '
        f'display:block; margin:10px 0 8px" role="img" aria-label="{label}">'
        + "".join(parts)
        + "</svg>"
    )


def _head(mid, color):
    return (
        f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" '
        f'markerHeight="4.5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{color}"/>'
        "</marker>"
    )


def _arrow(x1, y1, x2, y2, color, mid, width=4, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
        f'stroke-width="{width}"{d} marker-end="url(#{mid})"/>'
    )


def _text(x, y, s, size=16, color=INK, anchor="start", weight=500, mono=False):
    fam = f' font-family="{MONO}"' if mono else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{weight}"{fam}>{s}</text>'
    )


def _cap(s):
    return f'<p style="margin:0 0 18px">{s}</p>'


def _num(v, places=2):
    """Format a number with a plain hyphen for minus."""
    return f"{v:.{places}f}"


# ---------------------------------------------------------------- session 11


def _spark_lists():
    """Return the five lists before and after the faulty removal."""
    src = _source("sparks_parallel.py")
    cut = 'print()\nprint("now remove'
    names = ["xs", "ys", "dxs", "dys", "colors"]
    out = []
    for piece in (src.split(cut)[0], src):
        ns = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(piece, "sparks_parallel.py", "exec"), ns)
        out.append([(n, list(ns[n])) for n in names])
    return out


def _grid(rows, bad, label):
    left, top, cw, ch = 130, 44, 118, 42
    parts = []
    for k in range(4):
        parts.append(_text(left + cw * k + cw / 2, 28, f"item {k}", 16, SOFT, "middle", 700))
    for r, (name, vals) in enumerate(rows):
        y = top + ch * r
        parts.append(_text(left - 14, y + 27, name, 18, INK, "end", 700, mono=True))
        for k, v in enumerate(vals):
            wrong = (r, k) in bad
            parts.append(
                f'<rect x="{left + cw * k}" y="{y}" width="{cw - 6}" height="{ch - 6}" '
                f'rx="4" fill="{CLAY_TINT if wrong else CARD}" '
                f'stroke="{CLAY if wrong else RULE}" stroke-width="{4 if wrong else 2}"/>'
            )
            shown = f'"{v}"' if isinstance(v, str) else str(v)
            parts.append(
                _text(left + cw * k + (cw - 6) / 2, y + 25, shown, 17,
                      CLAY if wrong else INK, "middle", 700, mono=True)
            )
    return parts, left, top, cw, ch


def fig_lists_before():
    before, _ = _spark_lists()
    parts, left, top, cw, ch = _grid(before, set(), "")
    parts.append(
        f'<rect x="{left + cw - 6}" y="{top - 8}" width="{cw + 6}" height="{ch * 5 + 10}" '
        f'rx="8" fill="none" stroke="{TEAL}" stroke-width="4"/>'
    )
    parts.append(_text(left + cw * 1.5 - 3, top + ch * 5 + 28, "spark 1", 18, TEAL, "middle", 700))
    return _svg(
        640, top + ch * 5 + 40,
        "The five lists as five rows after frame 2. Item 1 of every list is outlined: "
        "those five values together are spark 1.",
        parts,
    ) + _cap(
        "The five lists after frame 2. Read down a column to get one spark. "
        "Spark 1 is item 1 of <code>xs</code>, item 1 of <code>ys</code>, and so on "
        "through all five lists."
    )


def fig_lists_after():
    before, after = _spark_lists()
    old = before[4][1]
    bad = {(4, k) for k in range(1, 4)}
    parts, left, top, cw, ch = _grid(after, bad, "")
    x_now = after[0][1][1]
    y0 = top + ch * 5 + 24
    parts.append(_text(20, y0, f"Item 1 is now the spark at x={x_now}. It was {old[2]}.", 17))
    parts.append(
        _text(20, y0 + 26, f'<tspan font-family="{MONO}" font-weight="700">colors</tspan>'
              f" still has {len(after[4][1])} items, so item 1 reads {old[1]}.", 17)
    )
    parts.append(
        _text(20, y0 + 52, "The last colour has no spark above it.", 17)
    )
    return _svg(
        640, y0 + 64,
        "The five lists after the removal. Four lists have three items. The colors list "
        "still has four, so its items no longer line up with the others.",
        parts,
    ) + _cap(
        "After the four <code>pop(1)</code> calls. Four lists lost item 1 and their "
        "later items moved one place left. <code>colors</code> did not change, so each "
        "colour from item 1 on sits under the wrong spark."
    )


def _plume():
    return _namespace("plume.py", "random.seed(")


def fig_three_objects():
    ns = _plume()
    random.seed(20261209)
    ps = ns["make_plume"](120)[:3]
    for p in ps:
        p.step()
        p.step()
    parts = []
    cw = 236
    for k, p in enumerate(ps):
        x = 8 + k * (cw + 12)
        parts.append(
            f'<rect x="{x}" y="8" width="{cw}" height="234" rx="8" fill="{CARD}" '
            f'stroke="{TEAL}" stroke-width="4"/>'
        )
        parts.append(f'<rect x="{x}" y="8" width="{cw}" height="40" rx="8" fill="{TEAL}"/>')
        parts.append(_text(x + cw / 2, 35, f"particles[{k}]", 18, CARD, "middle", 700, mono=True))
        lines = [
            ("x", _num(p.x, 1)), ("y", _num(p.y, 1)),
            ("dx", _num(p.dx)), ("dy", _num(p.dy)),
            ("trail", f"{len(p.trail)} points"), ("alive", str(p.alive)),
        ]
        for i, (name, val) in enumerate(lines):
            y = 76 + i * 29
            parts.append(_text(x + 86, y, name, 17, TEAL, "end", 700, mono=True))
            parts.append(_text(x + 100, y, val, 17, INK, "start", 700, mono=True))
    return _svg(
        752, 250,
        "Three Particle objects side by side. Each one holds its own x, y, dx, dy, "
        "trail and alive values.",
        parts,
    ) + _cap(
        "The first three particles in <code>plume.py</code> after two calls to "
        "<code>step</code>. Each object holds its own six attributes. Remove one "
        "particle from the list and its six values leave together, so nothing can "
        "end up under the wrong particle."
    )


def fig_speed_split():
    ns = _plume()
    p = ns["Particle"](0, 0, 10, 60)
    s = 30
    ox, oy = 150, 300
    ax, uy = ox + p.dx * s, oy + p.dy * s
    parts = ["<defs>" + _head("s11i", INK) + _head("s11t", TEAL) + _head("s11c", CLAY) + "</defs>"]
    r = 46
    ex, ey = ox + r * math.cos(math.radians(60)), oy - r * math.sin(math.radians(60))
    parts.append(
        f'<path d="M{ox + r} {oy} A{r} {r} 0 0 0 {ex:.1f} {ey:.1f}" fill="none" '
        f'stroke="{SOFT}" stroke-width="3"/>'
    )
    parts.append(_text(ox + 56, oy - 14, "60 degrees", 15, SOFT))
    parts.append(_arrow(ox, oy, ax - 3, oy, TEAL, "s11t", 5))
    parts.append(_arrow(ax, oy, ax, uy + 5, CLAY, "s11c", 5))
    parts.append(_arrow(ox, oy, ax - 4, uy + 7, INK, "s11i", 5))
    parts.append(_text(ox + 52, oy - 150, "speed 10", 18, INK, "end", 700))
    parts.append(_text((ox + ax) / 2, oy + 28, f"{_num(p.dx, 1)} across", 18, TEAL, "middle", 700))
    parts.append(_text(ax + 14, (oy + uy) / 2, f"{_num(-p.dy)} up", 18, CLAY, "start", 700))
    tx = 440
    parts.append(_text(tx, 70, "What the program stores", 17, SOFT, "start", 700))
    parts.append(_text(tx, 102, f"self.dx = {_num(p.dx, 1)}", 19, TEAL, "start", 700, mono=True))
    parts.append(_text(tx, 132, f"self.dy = {_num(p.dy)}", 19, CLAY, "start", 700, mono=True))
    parts.append(_text(tx, 180, "The check", 17, SOFT, "start", 700))
    a2, b2 = p.dx * p.dx, p.dy * p.dy
    parts.append(_text(tx, 212, f"{_num(p.dx, 1)} x {_num(p.dx, 1)} = {a2:.0f}", 18, INK, "start", 700, mono=True))
    parts.append(_text(tx, 240, f"{_num(-p.dy)} x {_num(-p.dy)} = {b2:.0f}", 18, INK, "start", 700, mono=True))
    parts.append(_text(tx, 268, f"{a2:.0f} + {b2:.0f} = {a2 + b2:.0f}", 18, INK, "start", 700, mono=True))
    parts.append(_text(tx, 296, f"10 x 10 = {10 * 10}", 18, INK, "start", 700, mono=True))
    return _svg(
        760, 350,
        "A launch at speed 10 and 60 degrees drawn as a slanted arrow, with a "
        "horizontal arrow of 5.0 across and a vertical arrow of 8.66 up.",
        parts,
    ) + _cap(
        "Speed 10 at 60 degrees. <code>cos</code> gives the across amount and "
        "<code>sin</code> gives the up amount. <code>self.dy</code> is stored as a "
        "negative number because moving up the screen makes <code>y</code> smaller."
    )


def fig_one_path():
    ns = _plume()
    speed, angle = 10, 80
    p = ns["Particle"](ns["WIDTH"] // 2, ns["HEIGHT"] - 40, speed, angle)
    dys = [p.dy]
    while p.alive == 1:
        p.step()
        dys.append(p.dy)
    k = 0.6
    wx, wy = 20, 20
    W, H = ns["WIDTH"] * k, ns["HEIGHT"] * k

    def at(pt):
        return wx + pt[0] * k, wy + pt[1] * k

    top = min(range(len(p.trail)), key=lambda i: p.trail[i][1])
    last = len(p.trail) - 1
    parts = ["<defs>" + _head("p11s", SOFT) + "</defs>"]
    parts.append(
        f'<rect x="{wx}" y="{wy}" width="{W:.0f}" height="{H:.0f}" fill="{CARD}" '
        f'stroke="{INK}" stroke-width="3"/>'
    )
    gy = wy + (ns["HEIGHT"] - 40) * k
    parts.append(
        f'<rect x="{wx}" y="{gy:.0f}" width="{W:.0f}" height="{40 * k:.0f}" fill="{RULE}"/>'
    )
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in map(at, p.trail))
    parts.append(f'<polyline points="{pts}" fill="none" stroke="{OCHRE}" stroke-width="4"/>')
    for i in range(0, len(p.trail), 10):
        x, y = at(p.trail[i])
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{INK}"/>')
    for i in (0, top, last):
        x, y = at(p.trail[i])
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none" stroke="{CLAY}" '
            'stroke-width="4"/>'
        )
    x0, y0 = at(p.trail[0])
    parts.append(_text(x0 - 18, y0 - 58, "frame 0", 17, INK, "end", 700))
    parts.append(_text(x0 - 18, y0 - 36, f"dy = {_num(dys[0])}", 17, CLAY, "end", 700, mono=True))
    parts.append(_text(x0 - 18, y0 - 14, "moving up", 17, INK, "end"))
    xt, yt = at(p.trail[top])
    parts.append(_text(xt, yt - 64, f"frame {top}", 17, INK, "middle", 700))
    parts.append(_text(xt, yt - 42, f"dy = {_num(dys[top])}", 17, CLAY, "middle", 700, mono=True))
    parts.append(_text(xt, yt - 20, "the top of the path", 17, INK, "middle"))
    lx = wx + W + 16
    parts.append(_text(lx, gy - 58, f"frame {last}", 17, INK, "start", 700))
    parts.append(_text(lx, gy - 36, f"dy = {_num(dys[last])}", 17, CLAY, "start", 700, mono=True))
    parts.append(_text(lx, gy - 14, "moving down", 17))
    parts.append(_text(lx, gy + 12, f"trail: {len(p.trail)} points", 17, INK, "start", 700))
    parts.append(_arrow(wx + 34, wy + 30, wx + 34, wy + 110, SOFT, "p11s", 4))
    parts.append(_text(wx + 48, wy + 66, "y gets bigger", 16, SOFT))
    parts.append(_text(wx + 48, wy + 86, "going down", 16, SOFT))
    return _svg(
        720, H + 40,
        f"The path of one particle launched at speed {speed} and {angle} degrees. It "
        "rises, reaches a top, and falls to the ground. dy is negative at launch, "
        "close to zero at the top, and positive at landing.",
        parts,
    ) + _cap(
        f"One particle launched at speed {speed} and {angle} degrees, with a dot every "
        "10 frames. <code>step</code> adds <code>GRAVITY</code> to <code>dy</code> "
        f"every frame, so <code>dy</code> goes from {_num(dys[0])} up through 0 to "
        f"{_num(dys[last])}. <code>step</code> also appends one position to "
        f"<code>trail</code> every frame. After {last} frames the trail holds "
        f"{len(p.trail)} points: the starting position and {last} more."
    )


# ---------------------------------------------------------------- session 12


def _orbit():
    return _namespace("orbit.py", "screen = pygame.display")


def _fly(dx, dt=None, frames=1200):
    """Step one ship and return the namespace, the ship, and its speed and pull per frame."""
    ns = _orbit()
    if dt is not None:
        ns["DT"] = dt
    ship = ns["Ship"](400, 120, dx, 0.0)
    for i in range(frames):
        ship.step()
    return ns, ship


def fig_distance():
    ns = _orbit()
    ship = ns["Ship"](400, 120, 3.8, 0.0)
    r = ship.distance()
    parts = ["<defs>" + _head("d12c", CLAY) + "</defs>"]
    sx, sy = 230, 50
    py = sy + r
    parts.append(
        f'<line x1="{sx}" y1="{sy}" x2="{sx}" y2="{py}" stroke="{SOFT}" stroke-width="3" '
        'stroke-dasharray="7 6"/>'
    )
    parts.append(f'<circle cx="{sx}" cy="{py}" r="26" fill="{PLANET}"/>')
    parts.append(f'<circle cx="{sx}" cy="{sy}" r="7" fill="{INK}"/>')
    parts.append(_arrow(sx + 22, sy, sx + 22, sy + 64, CLAY, "d12c", 5))
    parts.append(_text(sx + 36, sy + 30, "gravity", 17, CLAY, "start", 700))
    parts.append(_text(sx - 16, sy + 6, "ship (400, 120)", 16, INK, "end", 700))
    parts.append(_text(sx - 40, py + 6, "planet (400, 300)", 16, INK, "end", 700))
    parts.append(_text(sx + 14, sy + r / 2 + 28, f"{r:.0f}", 19, INK, "start", 700))
    parts.append(_text(sx, py + 56, "Across gap 0, so the distance", 16, SOFT, "middle"))
    parts.append(_text(sx, py + 78, "is 300 - 120.", 16, SOFT, "middle"))

    a, b = 100, 80
    d = math.sqrt(a * a + b * b)
    s = 2
    x1, y1 = 480, 230
    x2, y2 = x1 + a * s, y1 - b * s
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y1}" stroke="{TEAL}" stroke-width="5"/>')
    parts.append(f'<line x1="{x2}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CLAY}" stroke-width="5"/>')
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="5"/>')
    parts.append(
        f'<path d="M{x2 - 16} {y1} v-16 h16" fill="none" stroke="{SOFT}" stroke-width="3"/>'
    )
    parts.append(f'<circle cx="{x1}" cy="{y1}" r="7" fill="{INK}"/>')
    parts.append(f'<circle cx="{x2}" cy="{y2}" r="7" fill="{INK}"/>')
    parts.append(_text((x1 + x2) / 2, y1 + 26, f"{a} across", 18, TEAL, "middle", 700))
    parts.append(_text(x2 + 12, (y1 + y2) / 2 + 6, f"{b} up", 18, CLAY, "start", 700))
    parts.append(_text((x1 + x2) / 2 - 22, (y1 + y2) / 2 - 12, f"about {d:.0f}", 18, INK, "end", 700))
    ty = y1 + 62
    parts.append(_text(x1, ty, f"{a} x {a} = {a * a}", 17, TEAL, "start", 700, mono=True))
    parts.append(_text(x1, ty + 26, f"{b} x {b} = {b * b}", 17, CLAY, "start", 700, mono=True))
    parts.append(
        _text(x1, ty + 52, f"square root of {a * a + b * b} = {d:.2f}", 17, INK, "start", 700, mono=True)
    )
    return _svg(
        800, 350,
        "Left: the ship directly above the planet, 180 apart, with gravity pointing "
        "down the screen. Right: a right triangle with sides 100 across and 80 up, "
        "and a slanted side of about 128.",
        parts,
    ) + _cap(
        "Left: the opener. The ship is directly above the planet, so the distance is "
        "the gap in <code>y</code>. Right: two points that are 100 apart across and "
        "80 apart up. The distance between them is the long side of the triangle."
    )


def fig_pull_split():
    ns = _orbit()
    ship = ns["Ship"](400, 120, 3.8, 0.0)
    frame = 0
    for frame in range(1, 1200):
        ship.step()
        gx, gy = ns["PLANET_X"] - ship.x, ns["PLANET_Y"] - ship.y
        if gx > 70 and gy > 70:
            break
    r = ship.distance()
    pull = ns["PULL"] / (r * r)
    k = 2.1
    cx, cy = 350, 250

    def at(x, y):
        return cx + (x - ns["PLANET_X"]) * k, cy + (y - ns["PLANET_Y"]) * k

    sx, sy = at(ship.x, ship.y)
    parts = ["<defs>" + _head("f12i", INK) + _head("f12t", TEAL) + _head("f12c", CLAY) + "</defs>"]
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{26 * k:.0f}" fill="{PLANET}"/>')
    parts.append(_text(cx, cy + 26 * k + 22, "planet", 17, INK, "middle", 700))
    parts.append(
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{cx}" y2="{sy:.1f}" stroke="{TEAL}" '
        'stroke-width="3" stroke-dasharray="7 6"/>'
    )
    parts.append(
        f'<line x1="{cx}" y1="{sy:.1f}" x2="{cx}" y2="{cy}" stroke="{CLAY}" '
        'stroke-width="3" stroke-dasharray="7 6"/>'
    )
    parts.append(
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{cx}" y2="{cy}" stroke="{SOFT}" '
        'stroke-width="3" stroke-dasharray="7 6"/>'
    )
    L = 120
    ux, uy = gx / r, gy / r
    parts.append(_arrow(sx, sy, sx + L * ux, sy, TEAL, "f12t", 6))
    parts.append(_arrow(sx, sy, sx, sy + L * uy, CLAY, "f12c", 6))
    parts.append(_arrow(sx, sy, sx + L * ux, sy + L * uy, INK, "f12i", 6))
    parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="8" fill="{INK}"/>')
    parts.append(_text(sx - 16, sy + 6, "ship", 17, INK, "end", 700))
    parts.append(_text((sx + cx) / 2 + 40, sy - 14, f"gap_x = {gx:.0f}", 17, TEAL, "middle", 700, mono=True))
    parts.append(_text(cx + 14, (sy + cy) / 2 - 10, f"gap_y = {gy:.0f}", 17, CLAY, "start", 700, mono=True))
    parts.append(_text((sx + cx) / 2 - 24, (sy + cy) / 2 + 50, f"r = {r:.0f}", 17, INK, "end", 700, mono=True))
    tx = 500
    rows = [
        (SOFT, f"frame {frame}", False),
        (INK, f"pull = PULL / (r * r) = {_num(pull)}", True),
        (TEAL, f"across part = {_num(pull * ux)}", True),
        (CLAY, f"down part   = {_num(pull * uy)}", True),
    ]
    for i, (color, s, mono) in enumerate(rows):
        parts.append(_text(tx, 210 + i * 30, s, 16, color, "start", 700, mono=mono))
    return _svg(
        830, 340,
        "The ship up and to the left of the planet. Dashed lines show gap_x across, "
        "gap_y down, and r straight to the planet. A black arrow from the ship points "
        "at the planet, with a teal arrow for its across part and a red arrow for its "
        "down part.",
        parts,
    ) + _cap(
        f"Frame {frame} of <code>orbit.py</code>. The black arrow is the pull. It "
        "points along <code>r</code>, straight at the planet. The teal arrow is "
        "<code>pull * (gap_x / r)</code>, the part that changes <code>dx</code>. The "
        "red arrow is <code>pull * (gap_y / r)</code>, the part that changes "
        "<code>dy</code>. The arrows are drawn longer than the real numbers so you "
        "can see them."
    )


def fig_pull_bars():
    ns = _orbit()
    parts = []
    scale = 300
    for i, r in enumerate([60, 120, 180]):
        pull = ns["PULL"] / (r * r)
        y = 20 + i * 54
        parts.append(_text(150, y + 26, f"{r} px away", 18, INK, "end", 700))
        parts.append(
            f'<rect x="166" y="{y}" width="{pull * scale:.0f}" height="38" fill="{CLAY}"/>'
        )
        parts.append(
            _text(166 + pull * scale + 14, y + 26, f"pull = {_num(pull)}", 18, CLAY, "start", 700, mono=True)
        )
    return _svg(
        760, 180,
        "Three bars. At 60 pixels from the planet the pull is 1.44. At 120 pixels it "
        "is 0.36. At 180 pixels it is 0.16.",
        parts,
    ) + _cap(
        "<code>pull = PULL / (r * r)</code> at three distances. Twice as far away "
        "gives a quarter of the pull. Three times as far gives a ninth."
    )


def _window(ns, k, wx, wy, clip):
    W, H = ns["WIDTH"] * k, ns["HEIGHT"] * k
    px, py = wx + ns["PLANET_X"] * k, wy + ns["PLANET_Y"] * k
    return [
        f'<clipPath id="{clip}"><rect x="{wx}" y="{wy}" width="{W:.0f}" height="{H:.0f}"/>'
        "</clipPath>",
        f'<rect x="{wx}" y="{wy}" width="{W:.0f}" height="{H:.0f}" fill="{CARD}" '
        f'stroke="{INK}" stroke-width="3"/>',
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{26 * k:.1f}" fill="{PLANET}"/>',
    ]


def _path(trail, k, wx, wy, clip, color=TEAL, width=3):
    pts = " ".join(f"{wx + x * k:.1f},{wy + y * k:.1f}" for x, y in trail)
    return (
        f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" clip-path="url(#{clip})"/>'
    )


def fig_orbit_arrows():
    ns = _orbit()
    ship = ns["Ship"](400, 120, 3.8, 0.0)
    marks = {}
    for frame in range(0, 201):
        if frame in (0, 60, 100, 150):
            r = ship.distance()
            marks[frame] = (ship.x, ship.y, ship.dx, ship.dy, r, ns["PULL"] / (r * r))
        ship.step()
    k = 0.9
    wx, wy = 20, 20
    parts = ["<defs>" + _head("o12t", TEAL) + _head("o12c", CLAY) + "</defs>"]
    parts += _window(ns, k, wx, wy, "o12clip")
    parts.append(_path(ship.trail, k, wx, wy, "o12clip", RULE, 4))
    offsets = {0: (0, -16, "middle"), 60: (16, -8, "start"), 100: (-14, 22, "end"), 150: (-16, 4, "end")}
    for frame, (x, y, dx, dy, r, pull) in marks.items():
        sx, sy = wx + x * k, wy + y * k
        parts.append(_arrow(sx, sy, sx + dx * 11, sy + dy * 11, TEAL, "o12t", 5))
        ux, uy = (ns["PLANET_X"] - x) / r, (ns["PLANET_Y"] - y) / r
        L = 14 + pull * 38
        parts.append(_arrow(sx, sy, sx + ux * L, sy + uy * L, CLAY, "o12c", 5))
        parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="7" fill="{INK}"/>')
        ox, oy, anchor = offsets[frame]
        parts.append(_text(sx + ox, sy + oy, f"frame {frame}", 16, INK, anchor, 700))
    lx = wx + ns["WIDTH"] * k - 250
    ly = wy + ns["HEIGHT"] * k - 62
    parts.append(_arrow(lx, ly, lx + 44, ly, TEAL, "o12t", 5))
    parts.append(_text(lx + 56, ly + 6, "the way the ship moves", 16, TEAL, "start", 700))
    parts.append(_arrow(lx, ly + 30, lx + 44, ly + 30, CLAY, "o12c", 5))
    parts.append(_text(lx + 56, ly + 36, "the pull of the planet", 16, CLAY, "start", 700))
    return _svg(
        ns["WIDTH"] * k + 40, ns["HEIGHT"] * k + 40,
        "The ship's path for the first 200 frames, an oval around the planet. At "
        "frames 0, 60, 100 and 150 a teal arrow shows the direction the ship is "
        "moving and a red arrow shows the pull toward the planet.",
        parts,
    ) + _cap(
        "The first 200 frames with <code>dx = 3.8</code>. At every frame the red "
        "arrow points at the planet, so the ship is always being pulled toward it. "
        "The ship is also moving sideways, along the teal arrow, so it goes past the "
        "planet and does not hit it. The red arrow is longer close "
        "to the planet because the pull is stronger there."
    )


def fig_four_speeds():
    k = 0.44
    parts = []
    cases = [2.0, 3.8, 6.5, 7.6]
    notes = []
    for i, dx in enumerate(cases):
        ns, ship = _fly(dx)
        wx = 16 + (i % 2) * 384
        wy = 44 + (i // 2) * 346
        W, H = ns["WIDTH"], ns["HEIGHT"]
        ds = [math.hypot(ns["PLANET_X"] - x, ns["PLANET_Y"] - y) for x, y in ship.trail]
        trail = ship.trail
        inside = [j for j, d in enumerate(ds) if d < 26]
        off = [j for j, (x, y) in enumerate(trail) if x < 0 or x > W or y < 0 or y > H]
        back = [j for j in range(off[0], len(trail)) if j not in set(off)] if off else []
        if inside:
            trail = trail[: inside[0] + 1]
            note = f"inside the planet at frame {inside[0]}"
        elif not off:
            note = "goes round"
        elif back:
            note = f"leaves at frame {off[0]}, back at frame {back[0]}"
        else:
            note = f"leaves at frame {off[0]}, not back by frame {len(trail) - 1}"
        notes.append(note)
        clip = f"s12clip{i}"
        parts += _window(ns, k, wx, wy, clip)
        parts.append(_path(trail, k, wx, wy, clip, TEAL, 3))
        sx, sy = wx + 400 * k, wy + 120 * k
        parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6" fill="{INK}"/>')
        if inside:
            ex, ey = wx + trail[-1][0] * k, wy + trail[-1][1] * k
            parts.append(
                f'<path d="M{ex - 9:.1f} {ey - 9:.1f} l18 18 m0 -18 l-18 18" stroke="{CLAY}" '
                'stroke-width="5" fill="none"/>'
            )
        parts.append(_text(wx, wy - 12, f"dx = {dx}", 18, INK, "start", 700, mono=True))
        parts.append(_text(wx, wy + H * k + 24, note, 17, CLAY if inside else INK, "start", 700))
    return _svg(
        768, 44 + 346 + 264 + 40,
        "Four small windows showing the ship's path for four starting speeds. "
        + " ".join(f"dx {dx}: {n}." for dx, n in zip(cases, notes)),
        parts,
    ) + _cap(
        "Four runs of <code>orbit.py</code>, 1200 frames each, with only "
        "<code>dx</code> changed. The dot is the start. The box is the window, so a "
        "path that reaches the edge of the box has left the screen."
    )


def fig_two_dts():
    k = 0.44
    parts = []
    for i, dt in enumerate([0.6, 3.0]):
        ns, ship = _fly(3.8, dt)
        wx, wy = 16 + i * 384, 44
        clip = f"t12clip{i}"
        parts += _window(ns, k, wx, wy, clip)
        parts.append(_path(ship.trail, k, wx, wy, clip, TEAL, 2))
        parts.append(_text(wx, wy - 12, f"DT = {dt}", 18, INK, "start", 700, mono=True))
    return _svg(
        768, 44 + 600 * k + 16,
        "Two windows. With DT 0.6 the path is one oval drawn over itself. With DT 3.0 "
        "the path is many overlapping ovals, each turned a little from the last.",
        parts,
    ) + _cap(
        "The same ship with <code>dx = 3.8</code> for 1200 frames at two values of "
        "<code>DT</code>. At 0.6 each loop lands almost on top of the last one. At "
        "3.0 each loop is turned a little from the one before."
    )
