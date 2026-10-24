"""Sharp physics diagrams rendered to PNG bytes. Every instrument drawing is computed from the reading,
so the picture and the answer can never disagree. Adapted from the paper-setting toolkit (phys_figs.py)."""
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

plt.rcParams["font.family"] = ["DejaVu Sans"]
DPI = 170


def _fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _png(fig, pad=0.05):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, bbox_inches="tight", pad_inches=pad, facecolor="white")
    plt.close(fig)
    return buf.getvalue()


# ------------------------------------------------------------------ micrometer
def micrometer(reading_mm, show_numbers=True):
    main = int(reading_mm * 2 + 1e-9) / 2.0
    div = round((reading_mm - main) * 100)
    fig, ax = _fig(6.2, 2.4)
    S = 0.8
    xe = 8.0
    ax.add_patch(Rectangle((xe - 8.0, -0.55), 8.0, 1.1, fc="white", ec="black", lw=1.4))
    ax.plot([xe - 8.0, xe], [0, 0], color="black", lw=1.3)
    for m in np.arange(0, main + 0.001, 0.5):
        x = xe - (main - m) * S - 0.3          # last visible mark sits clear of the thimble edge
        if x < xe - 7.9:
            continue
        if abs(m - round(m)) < 1e-9:
            ax.plot([x, x], [0, 0.4], color="black", lw=1.2)
            if int(round(m)) % 5 == 0 and show_numbers:
                ax.text(x, 0.5, str(int(round(m))), ha="center", va="bottom", fontsize=9)
        else:
            ax.plot([x, x], [0, -0.4], color="black", lw=1.2)
    ax.add_patch(Rectangle((xe, -1.35), 3.2, 2.7, fc="white", ec="black", lw=1.4))
    step = 0.11
    for d in range(-12, 13):
        n = (div + d) % 50
        y = -d * step
        if abs(y) > 1.25:
            continue
        ax.plot([xe, xe + (0.5 if n % 5 == 0 else 0.28)], [y, y], color="black", lw=1.1)
        if n % 5 == 0 and show_numbers:
            ax.text(xe + 0.62, y, str(n), ha="left", va="center", fontsize=8)
    ax.plot([xe, xe + 3.2], [0, 0], color="black", lw=0.6, ls=":")
    ax.add_patch(Rectangle((xe - 9.9, -0.9), 0.8, 1.8, fc="white", ec="black", lw=1.4))
    ax.add_patch(Rectangle((xe - 9.1, -0.22), 1.1, 0.44, fc="white", ec="black", lw=1.2))
    ax.set_xlim(xe - 10.2, xe + 3.8)
    ax.set_ylim(-1.6, 1.6)
    return _png(fig)


# ------------------------------------------------------------------ vernier calipers
def vernier(reading_mm, show_numbers=True):
    main = int(reading_mm + 1e-9)
    fig, ax = _fig(7.2, 2.2)
    lo = max(0, main - 6)
    hi = lo + 22
    ax.add_patch(Rectangle((lo - 0.5, 0.0), hi - lo + 1, 1.15, fc="white", ec="black", lw=1.4))
    for m in range(lo, hi + 1):
        L = 0.62 if m % 10 == 0 else (0.45 if m % 5 == 0 else 0.3)
        ax.plot([m, m], [1.15, 1.15 - L], color="black", lw=1.1)
        if m % 10 == 0 and show_numbers:
            ax.text(m, 1.25, str(m // 10), ha="center", va="bottom", fontsize=9)
    ax.text(hi + 0.6, 1.25, "cm", ha="left", va="bottom", fontsize=8)
    x0 = reading_mm
    ax.add_patch(Rectangle((x0 - 1.0, -1.05), 9.0 + 2.0, 1.05, fc="white", ec="black", lw=1.4))
    for k in range(0, 11):
        x = x0 + 0.9 * k
        L = 0.62 if k in (0, 5, 10) else 0.4
        ax.plot([x, x], [0, -L], color="black", lw=1.1)
        if k in (0, 5, 10) and show_numbers:
            ax.text(x, -0.72, str(k), ha="center", va="top", fontsize=8)
    ax.plot([lo - 0.5, hi + 0.5], [0, 0], color="black", lw=1.0)
    ax.set_xlim(lo - 1.0, hi + 1.5)
    ax.set_ylim(-1.6, 2.1)
    return _png(fig)


# ------------------------------------------------------------------ stopwatch
def stopwatch(text="0:45.60"):
    fig, ax = _fig(2.2, 2.6)
    ax.add_patch(Circle((0, 0), 1.0, fc="white", ec="black", lw=2.2))
    ax.add_patch(Rectangle((-0.12, 1.0), 0.24, 0.22, fc="white", ec="black", lw=1.6))
    ax.add_patch(FancyBboxPatch((-0.78, -0.22), 1.56, 0.56, boxstyle="round,pad=0.02", fc="white", ec="black", lw=1.6))
    ax.text(0, 0.06, text, ha="center", va="center", fontsize=17, family="monospace", fontweight="bold")
    ax.text(0, -0.6, "min : s", ha="center", va="center", fontsize=8)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.3)
    return _png(fig)


# ------------------------------------------------------------------ measuring cylinders
def _cylinder(ax, x0, level_ml, max_ml=100, step_ml=10, minor_ml=2, label=None, stone=False):
    H = 10.0
    ax.add_patch(Rectangle((x0, 0), 1.6, H, fc="white", ec="black", lw=1.6))
    ax.add_patch(Rectangle((x0 - 0.5, -0.3), 2.6, 0.3, fc="white", ec="black", lw=1.6))
    y_of = lambda ml: 0.6 + ml / max_ml * (H - 1.4)
    ly = y_of(level_ml)
    ax.add_patch(Rectangle((x0 + 0.02, 0.02), 1.56, ly, fc="#d9d9d9", ec="none"))
    for ml in np.arange(0, max_ml + 0.001, minor_ml):
        y = y_of(ml)
        L = 0.55 if abs(ml % step_ml) < 1e-9 else 0.28
        ax.plot([x0 + 1.6 - L, x0 + 1.6], [y, y], color="black", lw=1.0)
        if abs(ml % step_ml) < 1e-9:
            ax.text(x0 + 1.75, y, str(int(ml)), va="center", ha="left", fontsize=8.5)
    xs = np.linspace(x0 + 0.02, x0 + 1.58, 30)
    ax.plot(xs, ly + 0.1 * (np.cos(np.linspace(-np.pi, np.pi, 30)) + 1) / 2 * -1 + 0.1, color="black", lw=1.4)
    if stone:
        ax.add_patch(Polygon([(x0 + 0.4, 0.3), (x0 + 1.2, 0.25), (x0 + 1.3, 0.9), (x0 + 0.8, 1.2), (x0 + 0.3, 0.9)], fc="#777777", ec="black", lw=1.0))
    if label:
        ax.text(x0 + 0.8, -0.8, label, ha="center", va="top", fontsize=9)
    ax.text(x0 + 1.75, H + 0.1, "cm³", va="bottom", ha="left", fontsize=8)


def measuring_cylinder(level_ml, max_ml=100, step_ml=10, minor_ml=2):
    fig, ax = _fig(2.0, 4.2)
    _cylinder(ax, 0, level_ml, max_ml, step_ml, minor_ml)
    ax.set_xlim(-0.7, 2.9)
    ax.set_ylim(-0.6, 11.0)
    return _png(fig)


def two_cylinders(level_before, level_after, max_ml=100, step_ml=10, minor_ml=2):
    fig, ax = _fig(4.6, 4.4)
    _cylinder(ax, 0, level_before, max_ml, step_ml, minor_ml, label="before")
    _cylinder(ax, 4.2, level_after, max_ml, step_ml, minor_ml, label="after", stone=True)
    ax.set_xlim(-0.7, 7.1)
    ax.set_ylim(-1.6, 11.0)
    return _png(fig)


# ------------------------------------------------------------------ force diagram
def force_diagram(arrows, label_body=None, ground=True, scale=1.0):
    """arrows: list of (label, direction, length); direction in {'up','down','left','right'} or degrees."""
    fig, ax = _fig(4.2, 3.4)
    w, h = 1.6, 1.0
    ax.add_patch(Rectangle((-w / 2, -h / 2), w, h, fc="white", ec="black", lw=1.8))
    if label_body:
        ax.text(0, 0, label_body, ha="center", va="center", fontsize=11)
    if ground:
        ax.plot([-3.0, 3.0], [-h / 2, -h / 2], color="black", lw=1.4)
        for x in np.arange(-3.0, 3.0, 0.25):
            ax.plot([x, x - 0.18], [-h / 2, -h / 2 - 0.2], color="black", lw=0.8)
    dirs = {"up": 90, "down": 270, "left": 180, "right": 0}
    for label, d, L in arrows:
        ang = np.deg2rad(dirs[d] if isinstance(d, str) else d)
        dx, dy = np.cos(ang), np.sin(ang)
        t = min(((w / 2) / abs(dx)) if abs(dx) > 1e-9 else 1e9, ((h / 2) / abs(dy)) if abs(dy) > 1e-9 else 1e9)
        p0 = (dx * t, dy * t)
        p1 = (p0[0] + dx * L * scale, p0[1] + dy * L * scale)
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=16, lw=2.0, color="black"))
        ax.text(p1[0] + dx * 0.45, p1[1] + dy * 0.35, label, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-2.4, 2.8)
    return _png(fig)


# ------------------------------------------------------------------ graphs
def graph(pts, xmax, ymax, xstep, ystep, xlabel="time / s", ylabel="speed / m/s", labels=None, shade=None, size=(4.6, 3.0)):
    fig, ax = plt.subplots(figsize=size, dpi=DPI)
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="black", lw=2.2)
    if shade:
        xx = np.linspace(shade[0], shade[1], 200)
        yy = np.interp(xx, xs, ys)
        ax.fill_between(xx, 0, yy, color="#cccccc", zorder=0)
    for (x, y, text, dx, dy) in (labels or []):
        ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=11, fontweight="bold", ha="center", va="center",
                    bbox=dict(boxstyle="circle,pad=0.12", fc="white", ec="none"))
        ax.plot([x], [y], "o", color="black", markersize=4)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xticks(np.arange(0, xmax + 1e-9, xstep))
    ax.set_yticks(np.arange(0, ymax + 1e-9, ystep))
    ax.set_xticks(np.arange(0, xmax + 1e-9, xstep / 5), minor=True)
    ax.set_yticks(np.arange(0, ymax + 1e-9, ystep / 5), minor=True)
    ax.grid(which="major", color="#666666", linewidth=0.8)
    ax.grid(which="minor", color="#BBBBBB", linewidth=0.4)
    ax.tick_params(labelsize=9, width=1.2)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    for s in ax.spines.values():
        s.set_linewidth(1.4)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, facecolor="white")
    plt.close(fig)
    return buf.getvalue()


# ------------------------------------------------------------------ displacement path
def path_figure(north, east):
    fig, ax = _fig(3.8, 3.6)
    k = 3.0 / max(north, east)
    a, b = north * k, east * k
    ax.add_patch(FancyArrowPatch((0, 0), (0, a), arrowstyle="-|>", mutation_scale=16, lw=2.0, color="black"))
    ax.add_patch(FancyArrowPatch((0, a), (b, a), arrowstyle="-|>", mutation_scale=16, lw=2.0, color="black"))
    ax.plot([0, b], [0, a], color="black", lw=1.2, ls="--")
    ax.plot([0], [0], "o", color="black", markersize=5)
    ax.text(-0.25, a / 2, f"{north} m", ha="right", va="center", fontsize=11)
    ax.text(b / 2, a + 0.25, f"{east} m", ha="center", va="bottom", fontsize=11)
    ax.text(-0.15, -0.15, "start", ha="right", va="top", fontsize=10)
    ax.text(b + 0.15, a - 0.1, "finish", ha="left", va="top", fontsize=10)
    # compass
    cx, cy = b + 0.9, 0.3
    ax.add_patch(FancyArrowPatch((cx, cy), (cx, cy + 0.9), arrowstyle="-|>", mutation_scale=12, lw=1.4, color="black"))
    ax.text(cx, cy + 1.0, "N", ha="center", va="bottom", fontsize=10)
    ax.set_xlim(-1.2, b + 1.8)
    ax.set_ylim(-0.7, a + 0.9)
    return _png(fig)


# ------------------------------------------------------------------ labelled block
def labelled_block(a, b, c, unit="cm"):
    """Oblique drawing of a cuboid: width a, depth b, height c."""
    fig, ax = _fig(4.0, 3.4)
    k = 3.0 / max(a, b, c)
    w, d, h = a * k, b * k, c * k
    ox, oy = d * 0.5, d * 0.35
    ax.add_patch(Rectangle((0, 0), w, h, fc="white", ec="black", lw=1.8))
    ax.add_patch(Polygon([(0, h), (ox, h + oy), (w + ox, h + oy), (w, h)], fc="#eeeeee", ec="black", lw=1.6))
    ax.add_patch(Polygon([(w, 0), (w + ox, oy), (w + ox, h + oy), (w, h)], fc="#dddddd", ec="black", lw=1.6))
    ax.text(w / 2, -0.25, f"{a} {unit}", ha="center", va="top", fontsize=11)
    ax.text(-0.2, h / 2, f"{c} {unit}", ha="right", va="center", fontsize=11)
    ax.text(w + ox / 2 + 0.25, oy / 2 - 0.05, f"{b} {unit}", ha="left", va="center", fontsize=11)
    ax.set_xlim(-1.3, w + ox + 1.6)
    ax.set_ylim(-0.8, h + oy + 0.5)
    return _png(fig)
