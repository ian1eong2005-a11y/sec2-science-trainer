"""Generic science sketches rendered to PNG bytes (black on white, labelled). Each drawer takes the numbers or
labels from the question, so the picture always matches the answer. Physics instrument drawings live in figs.py."""
import io
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Wedge

plt.rcParams["font.family"] = ["DejaVu Sans"]
DPI = 170
GREY = "#d9d9d9"


def _fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _png(fig, pad=0.06):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, bbox_inches="tight", pad_inches=pad, facecolor="white")
    plt.close(fig)
    return buf.getvalue()


def _arrow(ax, p0, p1, lw=1.8, ms=14, color="black", ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color, linestyle=ls, shrinkA=0, shrinkB=0))


def _box(ax, x, y, w, h, text, fs=10, fc="white", lw=1.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=fc, ec="black", lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", wrap=True)


# ------------------------------------------------------------------ charts
def bar_chart(labels, values, ylabel, xlabel="", ymax=None, ystep=None, size=(4.6, 3.0), hatch=None, title=None):
    fig, ax = plt.subplots(figsize=size, dpi=DPI)
    xs = np.arange(len(labels))
    bars = ax.bar(xs, values, width=0.6, color=GREY, edgecolor="black", linewidth=1.3)
    if hatch:
        for b, hch in zip(bars, hatch):
            b.set_hatch(hch)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=9)
    top = ymax or (max(values) * 1.25 if max(values) > 0 else 1)
    ax.set_ylim(0, top)
    if ystep:
        ax.set_yticks(np.arange(0, top + 1e-9, ystep))
        ax.set_yticks(np.arange(0, top + 1e-9, ystep / 5), minor=True)
    ax.grid(axis="y", which="major", color="#777777", linewidth=0.7)
    ax.grid(axis="y", which="minor", color="#cccccc", linewidth=0.4)
    ax.set_axisbelow(True)
    ax.set_ylabel(ylabel, fontsize=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if title:
        ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    return _png(fig, pad=0.03)


def xy_graph(series, xlabel, ylabel, xmax, ymax, xstep, ystep, xmin=0, ymin=0, labels=None, size=(4.8, 3.1), legend=True, markers=False):
    """series: list of (name, [(x, y), ...]) drawn black with different line styles. labels: (x, y, text, dx, dy)."""
    fig, ax = plt.subplots(figsize=size, dpi=DPI)
    styles = ["-", "--", ":", "-."]
    for (name, pts), ls in zip(series, styles * 3):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color="black", lw=2.0, ls=ls, label=name, marker="o" if markers else None, markersize=4)
    for (x, y, text, dx, dy) in (labels or []):
        ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=10, fontweight="bold", ha="center", va="center",
                    bbox=dict(boxstyle="circle,pad=0.12", fc="white", ec="none"))
        ax.plot([x], [y], "o", color="black", markersize=4)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(xmin, xmax + 1e-9, xstep))
    ax.set_yticks(np.arange(ymin, ymax + 1e-9, ystep))
    ax.set_xticks(np.arange(xmin, xmax + 1e-9, xstep / 5), minor=True)
    ax.set_yticks(np.arange(ymin, ymax + 1e-9, ystep / 5), minor=True)
    ax.grid(which="major", color="#666666", linewidth=0.8)
    ax.grid(which="minor", color="#BBBBBB", linewidth=0.4)
    ax.tick_params(labelsize=9, width=1.2)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    if legend and len(series) > 1:
        ax.legend(fontsize=8, frameon=True)
    for s in ax.spines.values():
        s.set_linewidth(1.3)
    fig.tight_layout()
    return _png(fig, pad=0.03)


def pie_chart(labels, values, size=(3.6, 3.0)):
    fig, ax = plt.subplots(figsize=size, dpi=DPI)
    hatches = ["", "//", "..", "xx", "\\\\", "oo"]
    wedges, _ = ax.pie(values, startangle=90, counterclock=False, colors=["white", GREY, "#bfbfbf", "#f0f0f0", "#a6a6a6", "#e0e0e0"],
                       wedgeprops=dict(edgecolor="black", linewidth=1.3))
    for w, h in zip(wedges, hatches):
        w.set_hatch(h)
    ax.legend(wedges, labels, fontsize=8, loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False)
    ax.set_aspect("equal")
    fig.tight_layout()
    return _png(fig, pad=0.03)


# ------------------------------------------------------------------ chains, webs, flows
def flow_boxes(labels, arrow_labels=None, size=None, fs=10, vertical=False):
    """Boxes joined by arrows: food chains, energy conversions, paths through the body."""
    n = len(labels)
    bw, bh, gap = 2.2, 0.9, 0.9
    if vertical:
        fig, ax = _fig(3.2, n * (bh + gap))
        for i, lab in enumerate(labels):
            y = (n - 1 - i) * (bh + gap)
            _box(ax, 0, y, bw, bh, lab, fs=fs)
            if i < n - 1:
                _arrow(ax, (bw / 2, y), (bw / 2, y - gap + 0.02))
                if arrow_labels:
                    ax.text(bw / 2 + 0.15, y - gap / 2, arrow_labels[i], fontsize=8, va="center")
        ax.set_xlim(-0.3, bw + 1.6)
        ax.set_ylim(-0.3, n * (bh + gap))
    else:
        fig, ax = _fig(size[0] if size else min(1.2 + n * (bw + gap), 11), 1.6)
        for i, lab in enumerate(labels):
            x = i * (bw + gap)
            _box(ax, x, 0, bw, bh, lab, fs=fs)
            if i < n - 1:
                _arrow(ax, (x + bw, bh / 2), (x + bw + gap - 0.02, bh / 2))
                if arrow_labels:
                    ax.text(x + bw + gap / 2, bh / 2 + 0.2, arrow_labels[i], fontsize=8, ha="center")
        ax.set_xlim(-0.3, n * (bw + gap) - gap + 0.3)
        ax.set_ylim(-0.4, bh + 0.6)
    return _png(fig)


def food_web(nodes, edges, size=(5.6, 3.8)):
    """nodes: {name: (x, y)} on a 0-10 grid; edges: [(from, to)] with the arrow pointing to the feeder."""
    fig, ax = _fig(*size)
    bw, bh = 1.9, 0.7
    for name, (x, y) in nodes.items():
        _box(ax, x - bw / 2, y - bh / 2, bw, bh, name, fs=9)
    for a, b in edges:
        (x0, y0), (x1, y1) = nodes[a], nodes[b]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        # leave the boxes
        tx = (bw / 2) / abs(ux) if abs(ux) > 1e-9 else 1e9
        ty = (bh / 2) / abs(uy) if abs(uy) > 1e-9 else 1e9
        t = min(tx, ty) + 0.05
        _arrow(ax, (x0 + ux * t, y0 + uy * t), (x1 - ux * t, y1 - uy * t), lw=1.5, ms=12)
    xs = [p[0] for p in nodes.values()]
    ys = [p[1] for p in nodes.values()]
    ax.set_xlim(min(xs) - bw / 2 - 0.3, max(xs) + bw / 2 + 0.3)
    ax.set_ylim(min(ys) - bh / 2 - 0.3, max(ys) + bh / 2 + 0.3)
    return _png(fig)


def pyramid(labels, counts=None, size=(4.2, 3.0)):
    """Pyramid of numbers / energy: widest bar at the bottom, labels inside, optional values on the right."""
    n = len(labels)
    fig, ax = _fig(*size)
    for i, lab in enumerate(labels):
        w = 6.0 * (1 - 0.22 * i)
        ax.add_patch(Rectangle((-w / 2, i), w, 0.9, fc=GREY if i % 2 else "white", ec="black", lw=1.4))
        ax.text(0, i + 0.45, lab, ha="center", va="center", fontsize=9)
        if counts:
            ax.text(3.3, i + 0.45, str(counts[i]), ha="left", va="center", fontsize=9)
    ax.set_xlim(-3.4, 5.2)
    ax.set_ylim(-0.2, n + 0.1)
    return _png(fig)


# ------------------------------------------------------------------ electricity
def _cell(ax, x, y, horizontal=True, n=1):
    """Cell symbol centred at (x, y): long thin line = positive, short thick = negative."""
    for k in range(n):
        off = (k - (n - 1) / 2) * 0.35
        if horizontal:
            ax.plot([x + off - 0.08, x + off - 0.08], [y - 0.32, y + 0.32], color="black", lw=1.6)
            ax.plot([x + off + 0.08, x + off + 0.08], [y - 0.16, y + 0.16], color="black", lw=4)
        else:
            ax.plot([x - 0.32, x + 0.32], [y + off + 0.08, y + off + 0.08], color="black", lw=1.6)
            ax.plot([x - 0.16, x + 0.16], [y + off - 0.08, y + off - 0.08], color="black", lw=4)


def _component(ax, kind, x, y, label=None, horizontal=True):
    """Draw one component centred at (x, y) on a wire running horizontally (or vertically). Returns half-width."""
    hw = 0.45
    if kind == "lamp":
        ax.add_patch(Circle((x, y), 0.3, fc="white", ec="black", lw=1.5))
        d = 0.3 / math.sqrt(2)
        ax.plot([x - d, x + d], [y - d, y + d], color="black", lw=1.3)
        ax.plot([x - d, x + d], [y + d, y - d], color="black", lw=1.3)
        hw = 0.3
    elif kind in ("resistor", "variable"):
        if horizontal:
            ax.add_patch(Rectangle((x - 0.5, y - 0.18), 1.0, 0.36, fc="white", ec="black", lw=1.5))
        else:
            ax.add_patch(Rectangle((x - 0.18, y - 0.5), 0.36, 1.0, fc="white", ec="black", lw=1.5))
        if kind == "variable":
            _arrow(ax, (x - 0.5, y - 0.42), (x + 0.5, y + 0.42), lw=1.3, ms=10)
        hw = 0.5
    elif kind in ("ammeter", "voltmeter"):
        ax.add_patch(Circle((x, y), 0.32, fc="white", ec="black", lw=1.5))
        ax.text(x, y, "A" if kind == "ammeter" else "V", ha="center", va="center", fontsize=10, fontweight="bold")
        hw = 0.32
    elif kind == "switch_open":
        ax.plot([x - 0.45], [y], "o", color="black", markersize=4)
        ax.plot([x + 0.45], [y], "o", color="black", markersize=4)
        ax.plot([x - 0.45, x + 0.35], [y, y + 0.4], color="black", lw=1.6)
        hw = 0.45
    elif kind == "switch_closed":
        ax.plot([x - 0.45], [y], "o", color="black", markersize=4)
        ax.plot([x + 0.45], [y], "o", color="black", markersize=4)
        ax.plot([x - 0.45, x + 0.45], [y, y], color="black", lw=1.6)
        hw = 0.45
    elif kind == "cell":
        _cell(ax, x, y, horizontal)
        hw = 0.2
    elif kind == "battery":
        _cell(ax, x, y, horizontal, n=2)
        hw = 0.4
    elif kind == "heater":
        if horizontal:
            ax.add_patch(Rectangle((x - 0.5, y - 0.18), 1.0, 0.36, fc="white", ec="black", lw=1.5))
            for k in range(1, 4):
                ax.plot([x - 0.5 + k * 0.25, x - 0.5 + k * 0.25], [y - 0.18, y + 0.18], color="black", lw=1.0)
        hw = 0.5
    if label:
        if horizontal:
            ax.text(x, y - 0.55, label, ha="center", va="top", fontsize=9)
        else:
            ax.text(x + 0.45, y, label, ha="left", va="center", fontsize=9)
    return hw


def circuit(bottom, top=("cell",), parallel=None, voltmeter_across=None, size=(5.0, 3.4), labels=None):
    """Rectangular circuit. top: components along the top wire (usually the cell / battery, switch).
    bottom: components along the bottom wire in series, e.g. ["lamp", "resistor", "ammeter"].
    parallel: list of branches (each a list of components) drawn as a parallel block in the middle of the bottom wire,
    replacing the bottom list if given. voltmeter_across: index of the bottom component (or branch block, -1) to put a voltmeter across.
    labels: list of labels for the bottom components / branches (None to skip)."""
    fig, ax = _fig(*size)
    W, H = 8.0, 4.0
    ax.plot([0, 0, W, W], [H, 0, 0, H], color="black", lw=1.6)
    ax.plot([0, W], [H, H], color="black", lw=1.6)
    # top wire components
    n = len(top)
    for i, kind in enumerate(top):
        x = W * (i + 1) / (n + 1)
        hw = _component(ax, kind, x, H, label=None)
        ax.add_patch(Rectangle((x - hw, H - 0.02), 2 * hw, 0.04, fc="white", ec="none"))
        if kind in ("cell", "battery"):
            ax.add_patch(Rectangle((x - hw - 0.02, H - 0.4), 2 * hw + 0.04, 0.8, fc="white", ec="none", zorder=1.5))
            _cell(ax, x, H, True, n=2 if kind == "battery" else 1)
            ax.text(x, H + 0.45, "+" if kind == "cell" else "", ha="center", va="bottom", fontsize=9)
    comp_pos = []
    labels = labels or []
    if parallel:
        # parallel block in the centre of the bottom wire
        bl, br = W * 0.3, W * 0.7
        k = len(parallel)
        ys = [-(i - (k - 1) / 2) * 1.1 for i in range(k)]
        ax.plot([bl, bl], [min(ys), max(ys)], color="black", lw=1.6)
        ax.plot([br, br], [min(ys), max(ys)], color="black", lw=1.6)
        ax.add_patch(Rectangle((bl + 0.01, -0.05), br - bl - 0.02, 0.1, fc="white", ec="none", zorder=1.5))  # hide base wire inside block
        for y, branch in zip(ys, parallel):
            ax.plot([bl, br], [y, y], color="black", lw=1.6)
            m = len(branch)
            for j, kind in enumerate(branch):
                x = bl + (br - bl) * (j + 1) / (m + 1)
                ax.add_patch(Rectangle((x - 0.55, y - 0.03), 1.1, 0.06, fc="white", ec="none", zorder=1.5))
                _component(ax, kind, x, y)
        for lab, y in zip(labels, ys):
            if lab:
                ax.text(br + 0.25, y, lab, ha="left", va="center", fontsize=9)
        comp_pos = [(bl, br, min(ys), max(ys))]
    else:
        n = len(bottom)
        for i, kind in enumerate(bottom):
            x = W * (i + 1) / (n + 1)
            ax.add_patch(Rectangle((x - 0.55, -0.03), 1.1, 0.06, fc="white", ec="none", zorder=1.5))
            hw = _component(ax, kind, x, 0, label=labels[i] if i < len(labels) else None)
            comp_pos.append((x - hw, x + hw, 0, 0))
    if voltmeter_across is not None:
        if parallel:
            x0, x1 = comp_pos[0][0], comp_pos[0][1]
        else:
            x0, x1, _, _ = comp_pos[voltmeter_across]
            x0, x1 = x0 - 0.25, x1 + 0.25
        yv = 1.3
        ax.plot([x0, x0, x1, x1], [0, yv, yv, 0], color="black", lw=1.4)
        xm = (x0 + x1) / 2
        ax.add_patch(Rectangle((xm - 0.35, yv - 0.03), 0.7, 0.06, fc="white", ec="none", zorder=1.5))
        _component(ax, "voltmeter", xm, yv)
    ax.set_xlim(-0.6, W + 1.4)
    ax.set_ylim(-1.8 if parallel else -1.1, H + 0.9)
    return _png(fig)


def plug_wiring(fault=None, size=(4.0, 3.0)):
    """Three-pin plug schematic with live (brown), neutral (blue), earth (green/yellow) labelled by words."""
    fig, ax = _fig(*size)
    ax.add_patch(FancyBboxPatch((0, 0), 6, 4.2, boxstyle="round,pad=0.05", fc="white", ec="black", lw=1.6))
    pins = {"E": (3.0, 3.4), "N": (1.0, 1.0), "L": (5.0, 1.0)}
    names = {"E": "earth (green/yellow)", "N": "neutral (blue)", "L": "live (brown)"}
    for p, (x, y) in pins.items():
        ax.add_patch(Rectangle((x - 0.3, y - 0.25), 0.6, 0.5, fc=GREY, ec="black", lw=1.3))
        ax.text(x, y, p, ha="center", va="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((3.6, 2.0), 0.6, 1.0, fc="white", ec="black", lw=1.3))
    ax.text(3.9, 2.5, "fuse", ha="center", va="center", fontsize=8, rotation=90)
    ax.plot([3.0, 3.0, 3.3], [0 - 0.0, 2.6, 3.4 - 0.25], color="black", lw=1.2)
    ax.plot([1.0, 1.0, 3.0 - 0.0], [1.25, 0.4, 0.4], color="black", lw=1.2)
    ax.plot([5.0, 5.0, 3.9, 3.9], [1.25, 1.6, 1.6, 2.0], color="black", lw=1.2)
    ax.plot([3.9, 3.9, 3.0], [3.0, 3.3, 3.3], color="black", lw=1.2, alpha=0)  # spacer
    ax.plot([3.0], [-0.2], color="black")
    ax.text(3.0, -0.35, "cable", ha="center", va="top", fontsize=9)
    for p, t in names.items():
        x, y = pins[p]
        ax.text(x, y + 0.5 if p != "E" else y + 0.55, t, ha="center", va="bottom", fontsize=7.5)
    if fault:
        ax.text(3.0, 4.5, fault, ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.7, 5.0)
    return _png(fig)


def electromagnet(turns=6, core=True, label=None, size=(4.4, 2.6)):
    fig, ax = _fig(*size)
    if core:
        ax.add_patch(Rectangle((0.5, 0.6), 5.0, 0.8, fc=GREY, ec="black", lw=1.5))
        ax.text(3.0, 1.0, "iron core", ha="center", va="center", fontsize=8)
    x0, x1 = 1.0, 5.0
    xs = np.linspace(x0, x1, turns * 20)
    ys = 1.0 + 0.75 * np.sin(np.linspace(0, turns * 2 * np.pi, turns * 20))
    ax.plot(xs, ys, color="black", lw=1.4)
    ax.plot([x0 - 0.8, x0], [1.0, 1.0], color="black", lw=1.4)
    ax.plot([x1, x1 + 0.8], [1.0, 1.0], color="black", lw=1.4)
    ax.text(x0 - 0.9, 1.0, "to cell", ha="right", va="center", fontsize=8)
    if label:
        ax.text(3.0, 2.2, label, ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-1.4, 7.0)
    ax.set_ylim(-0.1, 2.8)
    return _png(fig)


# ------------------------------------------------------------------ chemistry
UI_COLOURS = {0: "#c0392b", 1: "#d35400", 2: "#e67e22", 3: "#f39c12", 4: "#f1c40f", 5: "#d4e157", 6: "#9ccc65", 7: "#2e7d32",
              8: "#26a69a", 9: "#00838f", 10: "#1976d2", 11: "#283593", 12: "#4527a0", 13: "#6a1b9a", 14: "#4a148c"}


def ph_scale(mark=None, label=None, size=(6.2, 1.6)):
    """Universal Indicator strip 0-14 with optional arrow at pH `mark`."""
    fig, ax = _fig(*size)
    for p in range(15):
        ax.add_patch(Rectangle((p, 0), 1, 0.8, fc=UI_COLOURS[p], ec="black", lw=0.8))
        ax.text(p + 0.5, -0.15, str(p), ha="center", va="top", fontsize=8)
    ax.text(3.5, 1.0, "acidic", ha="center", fontsize=9)
    ax.text(7.5, 1.0, "neutral", ha="center", fontsize=9)
    ax.text(11.5, 1.0, "alkaline", ha="center", fontsize=9)
    if mark is not None:
        _arrow(ax, (mark + 0.5, 2.0), (mark + 0.5, 0.9), lw=1.8)
        if label:
            ax.text(mark + 0.5, 2.1, label, ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-0.3, 15.3)
    ax.set_ylim(-0.7, 2.8 if mark is not None else 1.5)
    return _png(fig)


def test_tubes(labels, contents=None, fills=None, bubbles=None, size=None):
    """Row of test tubes with labels under them; contents text inside; fills 0-1; bubbles True/False."""
    n = len(labels)
    fig, ax = _fig(size[0] if size else 1.4 * n + 0.6, 3.2)
    for i, lab in enumerate(labels):
        x = i * 1.6
        f = (fills or [0.6] * n)[i]
        ax.add_patch(Rectangle((x, 0.6), 0.8, 2.4 * f, fc=GREY, ec="none"))
        ax.plot([x, x, x + 0.8, x + 0.8], [3.0, 0.6, 0.6, 3.0], color="black", lw=1.5)
        ax.add_patch(Ellipse((x + 0.4, 0.6), 0.8, 0.3, fc=GREY, ec="black", lw=1.5))
        if bubbles and bubbles[i]:
            for (bx, by) in [(0.2, 1.0), (0.5, 1.4), (0.3, 1.9), (0.6, 0.8)]:
                ax.add_patch(Circle((x + bx, by), 0.06, fc="white", ec="black", lw=0.8))
        if contents and contents[i]:
            ax.text(x + 0.4, 3.15, contents[i], ha="center", va="bottom", fontsize=7.5)
        ax.text(x + 0.4, 0.2, lab, ha="center", va="top", fontsize=9, fontweight="bold")
    ax.set_xlim(-0.4, 1.6 * n - 0.4)
    ax.set_ylim(-0.4, 3.9)
    return _png(fig)


def balance(left_label, right_label, reading=None, size=(4.6, 2.4)):
    """Electronic balance with a container on the pan and a reading."""
    fig, ax = _fig(*size)
    ax.add_patch(Rectangle((0, 0), 6, 0.9, fc="white", ec="black", lw=1.6))
    ax.add_patch(Rectangle((0.6, 0.9), 4.8, 0.12, fc="black", ec="black"))
    ax.add_patch(Rectangle((3.9, 0.25), 1.7, 0.45, fc="white", ec="black", lw=1.2))
    ax.text(4.75, 0.47, reading or "", ha="center", va="center", fontsize=10, family="monospace")
    ax.add_patch(Polygon([(1.4, 1.02), (3.0, 1.02), (2.8, 2.6), (1.6, 2.6)], fc=GREY, ec="black", lw=1.4))
    ax.text(2.2, 1.7, left_label, ha="center", va="center", fontsize=8)
    if right_label:
        ax.text(2.2, 2.75, right_label, ha="center", va="bottom", fontsize=8)
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.2, 3.4)
    return _png(fig)


def particles(state, size=(2.6, 2.6), label=None, spacing=None):
    """Particle diagram of a solid (ordered, touching), liquid (random, touching) or gas (few, far apart)."""
    fig, ax = _fig(*size)
    ax.add_patch(Rectangle((0, 0), 4, 4, fc="white", ec="black", lw=1.5))
    rng = np.random.default_rng(3)
    if state == "solid":
        s = spacing or 0.75
        for i in range(5):
            for j in range(5):
                ax.add_patch(Circle((0.5 + i * s, 0.5 + j * s), 0.3, fc=GREY, ec="black", lw=1.0))
    elif state == "liquid":
        pts = [(0.5, 0.5), (1.2, 0.6), (1.9, 0.45), (2.6, 0.6), (3.3, 0.5), (0.7, 1.2), (1.5, 1.3), (2.3, 1.15), (3.1, 1.3), (3.5, 1.1),
               (0.5, 1.9), (1.2, 2.0), (1.9, 1.9), (2.7, 1.95), (3.4, 1.85), (0.9, 2.6), (1.7, 2.7), (2.5, 2.6), (3.2, 2.65)]
        for (x, y) in pts:
            ax.add_patch(Circle((x, y), 0.3, fc=GREY, ec="black", lw=1.0))
    else:
        for (x, y) in [(0.6, 0.8), (2.0, 0.5), (3.4, 1.0), (1.2, 2.2), (2.8, 2.4), (0.7, 3.4), (2.2, 3.3), (3.5, 3.5)]:
            ax.add_patch(Circle((x, y), 0.3, fc=GREY, ec="black", lw=1.0))
            _arrow(ax, (x, y), (x + rng.uniform(-0.6, 0.6), y + rng.uniform(-0.6, 0.6)), lw=1.0, ms=8)
    if label:
        ax.text(2, -0.25, label, ha="center", va="top", fontsize=9)
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-0.8, 4.2)
    return _png(fig)


# ------------------------------------------------------------------ heat
def thermometer(temp, tmin=-10, tmax=110, size=(1.6, 4.2)):
    fig, ax = _fig(*size)
    H = 8.0
    ax.add_patch(FancyBboxPatch((-0.3, 0), 0.6, H, boxstyle="round,pad=0.05", fc="white", ec="black", lw=1.5))
    ax.add_patch(Circle((0, -0.3), 0.55, fc="#777777", ec="black", lw=1.5))
    y_of = lambda t: 0.6 + (t - tmin) / (tmax - tmin) * (H - 1.2)
    ax.add_patch(Rectangle((-0.12, -0.3), 0.24, y_of(temp) + 0.3, fc="#777777", ec="none"))
    for t in range(tmin, tmax + 1, 10):
        y = y_of(t)
        ax.plot([0.3, 0.55], [y, y], color="black", lw=1.0)
        ax.text(0.65, y, str(t), ha="left", va="center", fontsize=7.5)
        for k in range(1, 5):
            yy = y_of(t + 2 * k)
            if t + 2 * k <= tmax:
                ax.plot([0.3, 0.42], [yy, yy], color="black", lw=0.6)
    ax.text(0, H + 0.2, "°C", ha="center", va="bottom", fontsize=8)
    ax.set_xlim(-1.0, 1.6)
    ax.set_ylim(-1.0, H + 0.7)
    return _png(fig)


def cans(labels, surfaces, size=(5.0, 2.8), heater=False):
    """Two or three cans side by side with different surfaces ('dull black', 'shiny silver', 'white'), each with a thermometer."""
    n = len(labels)
    fig, ax = _fig(*size)
    fc = {"dull black": "#222222", "shiny silver": "#e8e8e8", "white": "white", "dull grey": "#999999", "shiny black": "#444444"}
    for i, (lab, surf) in enumerate(zip(labels, surfaces)):
        x = i * 2.6
        ax.add_patch(Rectangle((x, 0), 1.6, 2.2, fc=fc.get(surf, GREY), ec="black", lw=1.5, hatch="///" if "dull" in surf and "black" not in surf else None))
        ax.add_patch(Rectangle((x + 0.7, 1.2), 0.2, 1.6, fc="white", ec="black", lw=1.0))
        ax.text(x + 0.8, -0.2, f"{lab}\n{surf}", ha="center", va="top", fontsize=8.5)
    if heater:
        ax.add_patch(Rectangle((-0.6, 2.9 + 0.3), 2.6 * n - 1.0 + 1.2, 0.3, fc="#444444", ec="black", lw=1.2))
        ax.text(1.3 * (n - 1) + 0.8, 3.6, "heater (same distance from each can)", ha="center", va="bottom", fontsize=8)
    ax.set_xlim(-0.8, 2.6 * n - 0.4)
    ax.set_ylim(-1.1, 4.2 if heater else 3.0)
    return _png(fig)


def bimetallic(bend="none", top="brass", bottom="iron", size=(4.6, 2.2), heated=True):
    """Bimetallic strip: straight, or bending 'up' / 'down' after heating."""
    fig, ax = _fig(*size)
    xs = np.linspace(0, 6, 60)
    k = {"none": 0, "up": 0.09, "down": -0.09}[bend]
    ys = k * xs ** 2 / 2
    ax.fill_between(xs, ys, ys + 0.3, color="#bbbbbb", edgecolor="black", linewidth=1.3)
    ax.fill_between(xs, ys - 0.3, ys, color="#eeeeee", edgecolor="black", linewidth=1.3)
    ax.text(-0.2, 0.15, top, ha="right", va="center", fontsize=9)
    ax.text(-0.2, -0.15, bottom, ha="right", va="center", fontsize=9)
    ax.add_patch(Rectangle((-0.6, -0.8), 0.4, 1.6, fc="#777777", ec="black", lw=1.2))
    if heated:
        for i in range(3):
            x = 2.0 + i * 1.3
            ax.add_patch(Polygon([(x - 0.25, -1.6), (x + 0.25, -1.6), (x, -0.9)], fc="#999999", ec="black", lw=1.0))
        ax.text(3.3, -1.9, "heat", ha="center", va="top", fontsize=9)
    ax.set_xlim(-2.0, 6.6)
    ax.set_ylim(-2.4, 2.4)
    return _png(fig)


def rod_conduction(materials, drop_positions=None, size=(5.4, 2.2)):
    """Rods of different materials heated at one end; a wax-held pin on each shows when heat arrives."""
    n = len(materials)
    fig, ax = _fig(*size)
    for i, m in enumerate(materials):
        y = (n - 1 - i) * 1.0
        ax.add_patch(Rectangle((0, y), 6, 0.4, fc=GREY, ec="black", lw=1.3))
        ax.text(6.2, y + 0.2, m, ha="left", va="center", fontsize=9)
        if drop_positions:
            ax.plot([drop_positions[i]], [y + 0.55], "v", color="black", markersize=6)
    ax.add_patch(Polygon([(-0.9, -0.6), (-0.1, -0.6), (-0.5, 0.4 + (n - 1) * 1.0 + 0.5)], fc="#999999", ec="black", lw=1.0))
    ax.text(-0.5, -0.8, "heat", ha="center", va="top", fontsize=9)
    ax.set_xlim(-1.3, 9.5)
    ax.set_ylim(-1.3, n * 1.0 + 0.6)
    return _png(fig)


def room_heater(heater_pos="floor", size=(4.4, 3.0), show_current=True):
    """Side view of a room with a heater or air-conditioner and a convection current."""
    fig, ax = _fig(*size)
    ax.add_patch(Rectangle((0, 0), 7, 4.5, fc="white", ec="black", lw=1.6))
    if heater_pos == "floor":
        ax.add_patch(Rectangle((0.4, 0.1), 1.2, 0.6, fc="#777777", ec="black", lw=1.2))
        ax.text(1.0, 0.9, "heater", ha="center", va="bottom", fontsize=8)
        pts = [(1.0, 1.4), (1.0, 3.8), (6.0, 3.8), (6.0, 0.6), (1.8, 0.6)]
    else:
        ax.add_patch(Rectangle((0.4, 3.8), 1.6, 0.5, fc="#777777", ec="black", lw=1.2))
        ax.text(1.2, 3.65, "air-conditioner", ha="center", va="top", fontsize=8)
        pts = [(1.2, 3.2), (1.2, 0.6), (6.0, 0.6), (6.0, 3.8), (2.2, 3.8)]
    if show_current:
        for (a, b) in zip(pts[:-1], pts[1:]):
            _arrow(ax, a, b, lw=1.3, ms=11, ls="--")
    ax.set_xlim(-0.3, 7.3)
    ax.set_ylim(-0.3, 5.0)
    return _png(fig)


def sea_breeze(day=True, size=(5.2, 2.8)):
    fig, ax = _fig(*size)
    ax.add_patch(Rectangle((0, 0), 4, 1.0, fc="#bfbfbf", ec="black", lw=1.3))
    ax.add_patch(Rectangle((4, 0), 4, 1.0, fc="#e8e8e8", ec="black", lw=1.3, hatch="..."))
    ax.text(2, 0.5, "sea", ha="center", va="center", fontsize=9)
    ax.text(6, 0.5, "land", ha="center", va="center", fontsize=9)
    ax.add_patch(Circle((7.2, 3.6) if day else (0.8, 3.6), 0.35, fc="white", ec="black", lw=1.2))
    ax.text(7.2 if day else 0.8, 4.1, "day" if day else "night", ha="center", va="bottom", fontsize=9)
    if day:
        pts = [(2, 1.3), (6, 1.3), (6, 3.0), (2, 3.0), (2, 1.5)]
    else:
        pts = [(6, 1.3), (2, 1.3), (2, 3.0), (6, 3.0), (6, 1.5)]
    for a, b in zip(pts[:-1], pts[1:]):
        _arrow(ax, a, b, lw=1.3, ms=11, ls="--")
    ax.set_xlim(-0.3, 8.3)
    ax.set_ylim(-0.3, 4.6)
    return _png(fig)


def flask(label_parts=True, size=(3.0, 3.6)):
    """Cross-section of a vacuum flask with letters P-S on the key parts."""
    fig, ax = _fig(*size)
    ax.add_patch(Rectangle((0, 0), 4, 6, fc="white", ec="black", lw=1.6))
    ax.add_patch(Rectangle((0.5, 0.5), 3, 5.0, fc=GREY, ec="black", lw=1.2))
    ax.add_patch(Rectangle((0.9, 0.9), 2.2, 4.6, fc="white", ec="black", lw=1.2))
    ax.add_patch(Rectangle((0.9, 5.5), 2.2, 0.7, fc="#bbbbbb", ec="black", lw=1.2))
    ax.add_patch(Rectangle((1.0, 1.0), 2.0, 3.0, fc="#dddddd", ec="none"))
    if label_parts:
        for t, (x, y) in {"P": (2.0, 5.85), "Q": (0.7, 3.0), "R": (2.0, 2.3), "S": (3.5, 0.25)}.items():
            ax.text(x, y, t, ha="center", va="center", fontsize=10, fontweight="bold",
                    bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="black"))
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(-0.3, 6.5)
    return _png(fig)


# ------------------------------------------------------------------ forces
def lever(pivot_frac=0.5, load=("load", 0.2), effort=("effort", 0.9), size=(5.2, 2.4), distances=None):
    """Bar on a pivot; load and effort arrows at fractions along the bar; optional distance labels."""
    fig, ax = _fig(*size)
    L = 8.0
    ax.add_patch(Rectangle((0, 1.0), L, 0.3, fc=GREY, ec="black", lw=1.5))
    px = L * pivot_frac
    ax.add_patch(Polygon([(px - 0.4, 0.0), (px + 0.4, 0.0), (px, 1.0)], fc="#777777", ec="black", lw=1.3))
    for (lab, frac), down in ((load, True), (effort, True)):
        x = L * frac
        _arrow(ax, (x, 2.4), (x, 1.35), lw=2.0)
        ax.text(x, 2.5, lab, ha="center", va="bottom", fontsize=9)
    if distances:
        for (frac, text) in distances:
            x = L * frac
            ax.plot([min(px, x), max(px, x)], [0.5, 0.5], color="black", lw=1.0)
            ax.plot([x, x], [0.4, 0.6], color="black", lw=1.0)
            ax.plot([px, px], [0.4, 0.6], color="black", lw=1.0)
            ax.text((px + x) / 2, 0.35, text, ha="center", va="top", fontsize=8.5)
    ax.set_xlim(-0.5, L + 0.5)
    ax.set_ylim(-0.6, 3.4)
    return _png(fig)


def block_area(a, b, force_label, unit="cm", size=(4.0, 3.2)):
    """Block pressing on a surface: oblique cuboid with its base dimensions and a downward force arrow."""
    fig, ax = _fig(*size)
    k = 3.0 / max(a, b, 1)
    w, d, h = a * k, b * k * 0.6, 1.4
    ox, oy = d * 0.6, d * 0.45
    ax.plot([-1.0, w + ox + 1.0], [0, 0], color="black", lw=1.4)
    ax.add_patch(Rectangle((0, 0), w, h, fc="white", ec="black", lw=1.6))
    ax.add_patch(Polygon([(0, h), (ox, h + oy), (w + ox, h + oy), (w, h)], fc="#eeeeee", ec="black", lw=1.4))
    ax.add_patch(Polygon([(w, 0), (w + ox, oy), (w + ox, h + oy), (w, h)], fc="#dddddd", ec="black", lw=1.4))
    ax.text(w / 2, -0.15, f"{a} {unit}", ha="center", va="top", fontsize=10)
    ax.text(w + ox / 2 + 0.2, oy / 2 - 0.05, f"{b} {unit}", ha="left", va="center", fontsize=10)
    _arrow(ax, (w / 2 + ox / 2, h + oy + 1.5), (w / 2 + ox / 2, h + oy + 0.05), lw=2.0)
    ax.text(w / 2 + ox / 2 + 0.2, h + oy + 1.0, force_label, ha="left", va="center", fontsize=10)
    ax.set_xlim(-1.2, w + ox + 1.6)
    ax.set_ylim(-0.7, h + oy + 1.9)
    return _png(fig)


def spring_balance(reading, max_n=10, size=(1.8, 4.4), label=None):
    fig, ax = _fig(*size)
    H = 7.0
    ax.add_patch(Rectangle((-0.5, 0), 1.0, H, fc="white", ec="black", lw=1.5))
    y_of = lambda n: H - 0.5 - n / max_n * (H - 1.0)
    step = max_n / 10
    for i in range(11):
        n = i * step
        y = y_of(n)
        ax.plot([0.5, 0.2], [y, y], color="black", lw=1.0)
        ax.text(-0.35, y, f"{n:g}", ha="left", va="center", fontsize=7)
        for k in range(1, 5):
            yy = y_of(n + k * step / 5)
            if n + k * step / 5 <= max_n:
                ax.plot([0.5, 0.35], [yy, yy], color="black", lw=0.6)
    ax.plot([-0.5, 0.5], [y_of(reading), y_of(reading)], color="black", lw=2.2)
    ax.text(0.95, y_of(reading), "pointer", ha="left", va="center", fontsize=7.5)
    ax.plot([0, 0], [H, H + 0.6], color="black", lw=1.3)
    ax.plot([0, 0], [0, -0.6], color="black", lw=1.3)
    ax.add_patch(Rectangle((-0.45, -1.5), 0.9, 0.9, fc=GREY, ec="black", lw=1.3))
    if label:
        ax.text(0, -1.05, label, ha="center", va="center", fontsize=8)
    ax.text(0, H + 0.7, "N", ha="center", va="bottom", fontsize=8)
    ax.set_xlim(-1.2, 2.4)
    ax.set_ylim(-1.8, H + 1.1)
    return _png(fig)


def magnets(pairs, size=(5.0, 1.8)):
    """pairs: list of (left_pole, right_pole) letters for two bar magnets facing each other, e.g. ('N','S')."""
    fig, ax = _fig(*size)
    for i, (a, b) in enumerate(pairs):
        y = -i * 1.4
        ax.add_patch(Rectangle((0, y), 2.4, 0.8, fc="white", ec="black", lw=1.4))
        ax.add_patch(Rectangle((1.2, y), 1.2, 0.8, fc=GREY, ec="black", lw=1.4))
        ax.text(0.6, y + 0.4, "S" if a == "N" else "N", ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(1.8, y + 0.4, a, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.add_patch(Rectangle((3.6, y), 2.4, 0.8, fc="white", ec="black", lw=1.4))
        ax.add_patch(Rectangle((3.6, y), 1.2, 0.8, fc=GREY, ec="black", lw=1.4))
        ax.text(4.2, y + 0.4, b, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(5.4, y + 0.4, "S" if b == "N" else "N", ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(-0.3, y + 0.4, "PQRS"[i] if len(pairs) > 1 else "", ha="right", va="center", fontsize=10, fontweight="bold")
    ax.set_xlim(-1.0, 6.3)
    ax.set_ylim(-1.4 * (len(pairs) - 1) - 0.3, 1.1)
    return _png(fig)


def bounce(heights, size=(4.8, 2.8)):
    """Ball bounce heights as vertical bars with the ball on top and the ground line."""
    fig, ax = _fig(*size)
    top = max(heights)
    for i, h in enumerate(heights):
        x = i * 1.5
        y = 4.0 * h / top
        ax.plot([x, x], [0, y], color="black", lw=1.0, ls=":")
        ax.add_patch(Circle((x, y + 0.25), 0.25, fc=GREY, ec="black", lw=1.2))
        ax.text(x, y + 0.65, f"{h:g} cm", ha="center", va="bottom", fontsize=8.5)
        ax.text(x, -0.25, "drop" if i == 0 else f"bounce {i}", ha="center", va="top", fontsize=8)
    ax.plot([-0.8, 1.5 * len(heights) - 0.7], [0, 0], color="black", lw=1.6)
    ax.set_xlim(-1.0, 1.5 * len(heights) - 0.5)
    ax.set_ylim(-0.8, 5.4)
    return _png(fig)


# ------------------------------------------------------------------ biology
def digestive_schematic(letters=("P", "Q", "R", "S", "T"), size=(3.2, 4.6)):
    """Simplified digestive tract as a vertical chain: mouth, gullet, stomach, small intestine, large intestine, rectum/anus.
    Letters are placed on five parts in order: gullet, stomach, small intestine, large intestine, rectum."""
    fig, ax = _fig(*size)
    ax.add_patch(Ellipse((2.0, 8.4), 1.4, 0.8, fc="white", ec="black", lw=1.5))
    ax.text(2.0, 8.4, "mouth", ha="center", va="center", fontsize=8)
    ax.add_patch(Rectangle((1.8, 6.4), 0.4, 1.6, fc="white", ec="black", lw=1.5))                 # gullet
    ax.add_patch(Ellipse((2.3, 5.6), 2.0, 1.4, fc=GREY, ec="black", lw=1.5))                      # stomach
    xs = np.linspace(0.8, 3.4, 200)
    ys = 3.6 + 0.45 * np.sin(xs * 6.0)
    ax.plot(xs, ys, color="black", lw=6, solid_capstyle="round")
    ax.plot(xs, ys, color="white", lw=3.5, solid_capstyle="round")                                 # small intestine
    ax.plot([0.5, 0.5, 3.6, 3.6], [1.6, 4.6, 4.6, 1.6], color="black", lw=10, solid_capstyle="round")
    ax.plot([0.5, 0.5, 3.6, 3.6], [1.6, 4.6, 4.6, 1.6], color=GREY, lw=7, solid_capstyle="round")  # large intestine
    ax.add_patch(Rectangle((3.35, 0.6), 0.5, 1.0, fc="white", ec="black", lw=1.5))                 # rectum
    pos = [(1.3, 7.2), (3.5, 6.0), (0.3, 3.1), (4.1, 4.6), (4.3, 1.0)]
    for t, (x, y) in zip(letters, pos):
        ax.text(x, y, t, ha="center", va="center", fontsize=10, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="black"))
    ax.set_xlim(-0.3, 4.9)
    ax.set_ylim(0.2, 9.0)
    return _png(fig)


def circulation(letters=("P", "Q", "R"), size=(4.6, 3.4)):
    """Heart (pump) with lungs above and body below; arrows show direction of flow. Letters on three vessels:
    P = vessel from heart to body (artery), Q = vessel from body to heart (vein), R = capillaries in the body."""
    fig, ax = _fig(*size)
    _box(ax, 2.5, 2.0, 2.0, 1.2, "heart", fs=10, fc=GREY)
    _box(ax, 2.5, 4.4, 2.0, 0.9, "lungs", fs=9)
    _box(ax, 2.2, -0.6, 2.6, 0.9, "body cells", fs=9)
    _arrow(ax, (4.0, 3.2), (4.0, 4.4))          # heart -> lungs
    _arrow(ax, (3.0, 4.4), (3.0, 3.2))          # lungs -> heart
    _arrow(ax, (3.0, 2.0), (3.0, 0.3))          # heart -> body  (artery) P
    _arrow(ax, (4.0, 0.3), (4.0, 2.0))          # body -> heart  (vein)   Q
    for t, (x, y) in zip(letters, [(2.55, 1.15), (4.45, 1.15), (5.2, -0.15)]):
        ax.text(x, y, t, ha="center", va="center", fontsize=10, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="black"))
    ax.set_xlim(1.6, 5.9)
    ax.set_ylim(-0.9, 5.6)
    return _png(fig)


def cell_concentration(inside, outside, label_in="inside cell", label_out="outside cell", arrow=None, size=(4.0, 2.8)):
    """A cell (rounded box) with dots: inside/outside counts show relative concentration. arrow: 'in' | 'out' | None."""
    fig, ax = _fig(*size)
    rng = np.random.default_rng(7)
    ax.add_patch(Rectangle((0, 0), 7, 4.5, fc="white", ec="black", lw=1.2))
    ax.add_patch(FancyBboxPatch((2.2, 0.9), 2.6, 2.7, boxstyle="round,pad=0.1", fc="#f4f4f4", ec="black", lw=1.8))
    for _ in range(inside):
        ax.plot(rng.uniform(2.4, 4.6), rng.uniform(1.1, 3.4), "o", color="black", markersize=4)
    for _ in range(outside):
        side = rng.integers(0, 2)
        x = rng.uniform(0.2, 1.9) if side == 0 else rng.uniform(5.1, 6.8)
        ax.plot(x, rng.uniform(0.2, 4.3), "o", color="black", markersize=4)
    ax.text(3.5, 3.9, label_in, ha="center", va="center", fontsize=8.5, bbox=dict(fc="white", ec="none", pad=1))
    ax.text(3.5, 4.75, label_out, ha="center", va="bottom", fontsize=8.5)
    if arrow == "in":
        _arrow(ax, (5.6, 2.2), (4.9, 2.2), lw=2.2, ms=16)
    elif arrow == "out":
        _arrow(ax, (4.9, 2.2), (5.6, 2.2), lw=2.2, ms=16)
    ax.set_xlim(-0.2, 7.2)
    ax.set_ylim(-0.2, 5.3)
    return _png(fig)


def potato_strips(before, after, size=(4.6, 2.6)):
    """Potato strip lengths before and after soaking (cm), drawn to scale."""
    fig, ax = _fig(*size)
    k = 6.0 / max(before, after)
    for i, (lab, L) in enumerate((("before", before), ("after", after))):
        y = 1.6 - i * 1.3
        ax.add_patch(Rectangle((0, y), L * k, 0.6, fc=GREY, ec="black", lw=1.4))
        ax.text(-0.2, y + 0.3, lab, ha="right", va="center", fontsize=9)
        ax.text(L * k + 0.2, y + 0.3, f"{L:g} cm", ha="left", va="center", fontsize=9)
    ax.set_xlim(-1.6, 8.3)
    ax.set_ylim(-0.2, 2.6)
    return _png(fig)


def plant_transport(dye_in="xylem", size=(3.4, 4.2)):
    """Celery / stem cross-section in a beaker of coloured water with labelled tissues."""
    fig, ax = _fig(*size)
    ax.add_patch(Rectangle((0, 0), 4, 2.4, fc="white", ec="black", lw=1.5))
    ax.add_patch(Rectangle((0.05, 0.05), 3.9, 1.6, fc="#bbbbbb", ec="none"))
    ax.text(2.0, 0.8, "coloured water", ha="center", va="center", fontsize=8)
    ax.add_patch(Rectangle((1.6, 0.3), 0.8, 6.0, fc="white", ec="black", lw=1.5))
    ax.add_patch(Rectangle((1.75, 0.3), 0.18, 6.0, fc="#555555" if dye_in == "xylem" else "white", ec="black", lw=0.8))
    ax.add_patch(Rectangle((2.07, 0.3), 0.18, 6.0, fc="#555555" if dye_in == "phloem" else "white", ec="black", lw=0.8))
    ax.text(1.5, 5.6, "X", ha="right", va="center", fontsize=10, fontweight="bold")
    ax.text(2.5, 5.6, "Y", ha="left", va="center", fontsize=10, fontweight="bold")
    ax.add_patch(Ellipse((2.0, 6.8), 2.2, 1.0, fc="white", ec="black", lw=1.4))
    ax.text(2.0, 6.8, "leaves", ha="center", va="center", fontsize=8)
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(-0.2, 7.6)
    return _png(fig)


def cycle_bar(period_days=5, ovulation=14, length=28, marks=None, size=(6.4, 1.9)):
    """Menstrual cycle as a day bar: shaded menstruation days, a marker at ovulation, optional extra day markers {day: label}."""
    fig, ax = _fig(*size)
    for d in range(1, length + 1):
        fc = "#777777" if d <= period_days else ("#dddddd" if abs(d - ovulation) <= 1 else "white")
        ax.add_patch(Rectangle((d - 1, 0), 1, 0.8, fc=fc, ec="black", lw=0.6))
        if d % 7 == 1 or d == length:
            ax.text(d - 0.5, -0.15, str(d), ha="center", va="top", fontsize=8)
    ax.text(period_days / 2, 1.0, "menstruation", ha="center", va="bottom", fontsize=8)
    _arrow(ax, (ovulation - 0.5, 2.1), (ovulation - 0.5, 0.9), lw=1.6)
    ax.text(ovulation - 0.5, 2.2, "ovulation", ha="center", va="bottom", fontsize=8)
    for d, lab in (marks or {}).items():
        _arrow(ax, (d - 0.5, -1.4), (d - 0.5, -0.5), lw=1.4)
        ax.text(d - 0.5, -1.5, lab, ha="center", va="top", fontsize=8)
    ax.text(length + 0.4, 0.4, "day", ha="left", va="center", fontsize=8)
    ax.set_xlim(-0.3, length + 1.6)
    ax.set_ylim(-2.3 if marks else -0.7, 3.0)
    return _png(fig)


def month_calendar(month_name, days_in_month, first_weekday, shaded=None, circled=None, size=(5.0, 3.4)):
    """A month grid (Mon-Sun). shaded: set of day numbers (e.g. period days); circled: {day: label}."""
    fig, ax = _fig(*size)
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, nm in enumerate(names):
        ax.text(i + 0.5, 6.35, nm, ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(3.5, 7.0, month_name, ha="center", va="center", fontsize=10, fontweight="bold")
    row, col = 5, first_weekday
    for d in range(1, days_in_month + 1):
        fc = "#bbbbbb" if shaded and d in shaded else "white"
        ax.add_patch(Rectangle((col, row), 1, 1, fc=fc, ec="black", lw=0.8))
        ax.text(col + 0.5, row + 0.5, str(d), ha="center", va="center", fontsize=8.5)
        if circled and d in circled:
            ax.add_patch(Circle((col + 0.5, row + 0.5), 0.42, fc="none", ec="black", lw=1.8))
            ax.text(col + 0.5, row - 0.02, circled[d], ha="center", va="top", fontsize=6.5)
        col += 1
        if col == 7:
            col, row = 0, row - 1
    ax.set_xlim(-0.2, 7.2)
    ax.set_ylim(-0.4, 7.4)
    return _png(fig)


def labelled_parts(title, parts, size=(4.4, 3.0)):
    """Generic schematic: a list of (letter, name-hidden) boxes arranged in a column with connecting lines, titled.
    Used when a real anatomical drawing is not needed: the letter stands for a part named in the question."""
    n = len(parts)
    fig, ax = _fig(*size)
    for i, (letter, text) in enumerate(parts):
        y = (n - 1 - i) * 1.1
        _box(ax, 1.0, y, 3.4, 0.8, text, fs=9)
        ax.text(0.5, y + 0.4, letter, ha="center", va="center", fontsize=10, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="black"))
        if i < n - 1:
            ax.plot([2.7, 2.7], [y, y - 0.3], color="black", lw=1.3)
    ax.text(2.7, n * 1.1 + 0.1, title, ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_xlim(-0.2, 4.8)
    ax.set_ylim(-0.3, n * 1.1 + 0.8)
    return _png(fig)


def energy_arrows(stages, values, unit="J", size=(5.6, 2.4)):
    """Energy passing along a chain: boxes with the energy value, a 'lost as heat' arrow down from each."""
    n = len(stages)
    fig, ax = _fig(*size)
    for i, (s, v) in enumerate(zip(stages, values)):
        x = i * 2.9
        _box(ax, x, 1.0, 2.2, 0.9, f"{s}\n{v:g} {unit}", fs=8.5)
        if i < n - 1:
            _arrow(ax, (x + 2.2, 1.45), (x + 2.9, 1.45))
            _arrow(ax, (x + 1.1, 1.0), (x + 1.1, 0.2), lw=1.2, ms=10, ls="--")
            ax.text(x + 1.25, 0.45, "heat", ha="left", va="center", fontsize=7.5)
    ax.set_xlim(-0.3, 2.9 * n - 0.4)
    ax.set_ylim(-0.1, 2.3)
    return _png(fig)
