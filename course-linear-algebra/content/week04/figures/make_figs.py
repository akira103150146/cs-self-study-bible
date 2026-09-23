# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W4(Lay 1.8–1.10)的圖。座標一律用數學座標(y 向上),由 Plot 換算成 SVG 像素。
import math
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))


def sub(s):
    """把 x1、v2、e1 這類「字母 + 數字」畫成下標(和題幹的 $x_1$ 一致);x 軸變數用斜體。"""
    def rep(m):
        head = m.group(1)
        if head == "x":
            head = '<tspan style="font-family: var(--font-serif); font-style: italic">x</tspan>'
        return f'{head}<tspan dy="4" font-size="10">{m.group(2)}</tspan><tspan dy="-4">​</tspan>'
    return re.sub(r"(?<![A-Za-z])([a-z])(\d)(?!\d)", rep, s)


class Plot:
    """數學座標 → SVG。x ∈ [x0, x1]、y ∈ [y0, y1],每單位 s 像素,四周留 pad。"""

    def __init__(self, x0, x1, y0, y1, s=34, pad=26, mid="ah"):
        self.x0, self.x1, self.y0, self.y1, self.s, self.pad, self.mid = x0, x1, y0, y1, s, pad, mid
        self.w = (x1 - x0) * s + 2 * pad
        self.h = (y1 - y0) * s + 2 * pad
        self.parts = []

    def P(self, x, y):
        return (round(self.pad + (x - self.x0) * self.s, 1), round(self.pad + (self.y1 - y) * self.s, 1))

    def axes(self, ticks=True, labels=True):
        (ax0, ay), (ax1, _) = self.P(self.x0, 0), self.P(self.x1, 0)
        (bx, by0), (_, by1) = self.P(0, self.y0), self.P(0, self.y1)
        self.parts.append(f'<line class="ax" x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}"/>')
        self.parts.append(f'<line class="ax" x1="{bx}" y1="{by0}" x2="{bx}" y2="{by1}"/>')
        if labels:
            self.parts.append(f'<text x="{ax1 - 4}" y="{ay - 6}" text-anchor="end">{sub("x1")}</text>')
            self.parts.append(f'<text x="{bx + 6}" y="{by1 + 12}">{sub("x2")}</text>')
        if ticks:
            for t in range(math.ceil(self.x0), math.floor(self.x1) + 1):
                if t:
                    x, y = self.P(t, 0)
                    self.parts.append(f'<line class="ax" x1="{x}" y1="{y - 3}" x2="{x}" y2="{y + 3}"/>')
            for t in range(math.ceil(self.y0), math.floor(self.y1) + 1):
                if t:
                    x, y = self.P(0, t)
                    self.parts.append(f'<line class="ax" x1="{x - 3}" y1="{y}" x2="{x + 3}" y2="{y}"/>')

    def arrow(self, p, q=(0, 0), cls="l1", dashed=False):
        (x1, y1), (x2, y2) = self.P(*q), self.P(*p)
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        self.parts.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{dash} '
                          f'marker-end="url(#{self.mid})"/>')

    def line(self, p, q, cls="ax", extra=""):
        (x1, y1), (x2, y2) = self.P(*p), self.P(*q)
        self.parts.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{extra}/>')

    def poly(self, pts, cls="hl", opacity=0.55, extra=""):
        s = " ".join(f"{x},{y}" for x, y in (self.P(*p) for p in pts))
        self.parts.append(f'<polygon class="{cls}" points="{s}" style="opacity:{opacity}"{extra}/>')

    def polyline(self, pts, cls="l2", extra=""):
        s = " ".join(f"{x},{y}" for x, y in (self.P(*p) for p in pts))
        self.parts.append(f'<polyline class="{cls}" points="{s}" style="fill:none"{extra}/>')

    def dot(self, p, cls="pt", r=4):
        x, y = self.P(*p)
        self.parts.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}"/>')

    def label(self, p, text, dx=6, dy=-6, cls="t", anchor="start"):
        x, y = self.P(*p)
        self.parts.append(f'<text class="{cls}" x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{sub(text)}</text>')

    def body(self, dx=0, dy=0):
        return f'<g transform="translate({dx},{dy})">' + "".join(self.parts) + "</g>"


def marker(mid):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
            f'markerWidth="11" markerHeight="11" orient="auto"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker>')


def svg(name, aria, w, h, body, mids):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{aria}">'
            f'<defs>{"".join(marker(m) for m in mids)}</defs>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(head + body + "</svg>\n")


def single(name, aria, p, caption=None):
    extra = 22 if caption else 0
    body = p.body()
    if caption:
        body += f'<text x="{p.w / 2}" y="{p.h + 12}" text-anchor="middle">{caption}</text>'
    svg(name, aria, p.w, p.h + extra, body, [p.mid])


def pair(name, aria, a, b, cap_a, cap_b, gap=30, mid_text=None):
    w = a.w + gap + b.w
    h = max(a.h, b.h) + 24
    body = a.body() + b.body(a.w + gap)
    body += f'<text x="{a.w / 2}" y="{h - 6}" text-anchor="middle">{cap_a}</text>'
    body += f'<text x="{a.w + gap + b.w / 2}" y="{h - 6}" text-anchor="middle">{cap_b}</text>'
    if mid_text:
        body += (f'<text x="{a.w + gap / 2}" y="{h / 2 - 8}" text-anchor="middle" class="t">{mid_text}</text>'
                 f'<text x="{a.w + gap / 2}" y="{h / 2 + 6}" text-anchor="middle">→</text>')
    svg(name, aria, w, h, body, [a.mid, b.mid])


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(c, a):
    return tuple(c * x for x in a)


def apply(M, p):
    return (M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1])


# ---------- 觀念 1:剪切(Lay 1.8 Example 3,Figure 4)----------
a = Plot(-0.5, 3, -0.5, 2.8, s=40, pad=20, mid="ah-sh1")
b = Plot(-0.5, 7, -0.5, 2.8, s=40, pad=20, mid="ah-sh2")
sq = [(0, 0), (2, 0), (2, 2), (0, 2)]
S = ((1, 2), (0, 1))
a.poly(sq); a.axes(); a.label((2, 0), "2", dx=-4, dy=16, cls=""); a.label((0, 2), "2", dx=-14, dy=4, cls="")
a.dot((0, 2)); a.label((0, 2), "u = (0, 2)", dx=8, dy=18)
b.poly([apply(S, q) for q in sq]); b.axes()
b.line((2, 2), (6, 2), cls="ax", extra=' stroke-dasharray="4 4"')
b.dot((4, 2)); b.label((4, 2), "T(u) = (4, 2)", dx=-4, dy=-8, anchor="end")
b.dot((6, 2)); b.label((6, 2), "(6, 2)", dx=4, dy=-8)
b.label((2, 0), "2", dx=-4, dy=16, cls=""); b.label((6, 0), "6", dx=-4, dy=16, cls="")
pair("shear.svg", "Shear transformation: the 2-by-2 square is mapped to a parallelogram; the top edge slides right while the base stays fixed",
     a, b, "the 2 × 2 square", "its image under T(x) = Ax", mid_text="T")

# ---------- 觀念 2:伸縮 T(x) = 3x(Lay 1.8 Example 4,Figure 5)----------
vs = [(0.6, 0.5), (1.0, 0.2), (0.5, -0.6), (-0.6, -0.5), (-0.4, 0.55)]
a = Plot(-3.4, 3.4, -2.2, 2.2, s=32, pad=16, mid="ah-dil1")
b = Plot(-3.4, 3.4, -2.2, 2.2, s=32, pad=16, mid="ah-dil2")
a.axes(ticks=False); b.axes(ticks=False)
for q in vs:
    a.arrow(q); a.dot(q, r=3)
    b.arrow(mul(3, q), cls="l2"); b.dot(mul(3, q), r=3)
a.label(vs[4], "u", dx=-10, dy=-6); b.label(mul(3, vs[4]), "T(u)", dx=-6, dy=-6, anchor="end")
pair("dilation.svg", "Dilation T(x) = 3x: every vector keeps its direction and becomes three times as long",
     a, b, "vectors x", "images T(x) = 3x", mid_text="T")

# ---------- 觀念 2:旋轉 90°(Lay 1.8 Example 5)----------
R = ((0, -1), (1, 0))
u, v = (4, 1), (2, 3)
p = Plot(-5, 7, -0.8, 7, s=30, mid="ah-rot")
p.poly([(0, 0), u, add(u, v), v], cls="hl", opacity=0.45)
p.poly([(0, 0), apply(R, u), apply(R, add(u, v)), apply(R, v)], cls="bad", opacity=0.35)
p.axes()
for q, lab, dx, dy, anc in ((u, "u", 6, 4, "start"), (v, "v", 4, -6, "start"), (add(u, v), "u + v", 6, 4, "start")):
    p.arrow(q); p.dot(q, r=3); p.label(q, lab, dx=dx, dy=dy, anchor=anc)
for q, lab, dx, dy, anc in ((apply(R, u), "T(u)", -6, -6, "end"), (apply(R, v), "T(v)", -6, 14, "end"),
                            (apply(R, add(u, v)), "T(u + v)", -6, -6, "end")):
    p.arrow(q, cls="l2"); p.dot(q, r=3); p.label(q, lab, dx=dx, dy=dy, anchor=anc)
svg("rotation.svg", "Rotation through 90 degrees counterclockwise: the parallelogram of u and v turns into the parallelogram of T(u) and T(v)",
    p.w, p.h, p.body(), [p.mid])

# ---------- 觀念 2:Lay 1.8 Exercise 18 的兩張圖 ----------
a = Plot(-2, 3, -1.5, 3, s=42, pad=18, mid="ah-e18a")
b = Plot(-1, 3, -1.5, 3, s=42, pad=18, mid="ah-e18b")
a.axes(ticks=False)
for q, lab, dx, dy, anc in (((2, 2), "u", 8, -4, "start"), ((0, 2), "w", -8, -6, "end"), ((-1, 0), "v", -6, 16, "end")):
    a.arrow(q); a.dot(q, r=3.5); a.label(q, lab, dx=dx, dy=dy, anchor=anc)
b.axes(ticks=False)
for q, lab, dx, dy, anc in (((1.58, 1.68), "T(v)", 8, -4, "start"), ((1.96, -0.93), "T(u)", 8, 4, "start")):
    b.arrow(q, cls="l2"); b.dot(q, r=3.5); b.label(q, lab, dx=dx, dy=dy, anchor=anc)
pair("ex18-vectors.svg", "Exercise 18: on the left the vectors u, v and w; on the right the images T(u) and T(v)",
     a, b, "u, v, w", "T(u), T(v)")

# ---------- 觀念 3:旋轉 φ 時 e1、e2 的像(Lay 1.9 Figure 1)----------
phi = math.radians(28)
p = Plot(-1.5, 1.6, -0.3, 1.45, s=120, pad=20, mid="ah-rphi")
p.axes(ticks=False)
arc = [(math.cos(t), math.sin(t)) for t in [i * math.pi / 60 for i in range(0, 61)]]
p.polyline(arc, cls="ax", extra=' stroke-dasharray="4 4"')
c, s_ = math.cos(phi), math.sin(phi)
p.arrow((1, 0), cls="l1"); p.arrow((0, 1), cls="l1")
p.arrow((c, s_), cls="l2"); p.arrow((-s_, c), cls="l2")
p.dot((1, 0), r=3); p.dot((0, 1), r=3); p.dot((c, s_), r=3); p.dot((-s_, c), r=3)
p.label((1, 0), "e1 = (1, 0)", dx=-4, dy=18)
p.label((0, 1), "e2 = (0, 1)", dx=6, dy=-6)
p.label((c, s_), "(cos φ, sin φ)", dx=8, dy=0)
p.label((-s_, c), "(−sin φ, cos φ)", dx=-8, dy=-6, anchor="end")
p.label((0.34 * math.cos(phi / 2), 0.34 * math.sin(phi / 2)), "φ", dx=0, dy=6, cls="")
p.label((-0.34 * math.sin(phi / 2), 0.34 * math.cos(phi / 2)), "φ", dx=-8, dy=4, cls="")
svg("rotation-e1e2.svg", "Rotation through angle phi sends e1 to (cos phi, sin phi) and e2 to (minus sin phi, cos phi)",
    p.w, p.h, p.body(), [p.mid])

# ---------- 觀念 3:Lay 1.9 Exercises 13、14 的圖 ----------
a = Plot(-3, 5.5, -1.2, 3, s=42, pad=18, mid="ah-e13")
a.axes(ticks=False)
for q, lab, dx, dy, anc in (((-2.1, 0.8), "T(e1)", -4, -8, "end"), ((4.7, 1.0), "T(e2)", -4, -8, "end")):
    a.arrow(q, cls="l2"); a.dot(q, r=3.5); a.label(q, lab, dx=dx, dy=dy, anchor=anc)
single("ex13-vectors.svg", "Exercise 13: the images T(e1) pointing up-left and T(e2) pointing right", a)

b = Plot(-1.5, 5, -2.5, 2.5, s=42, pad=18, mid="ah-e14")
b.axes(ticks=False)
for q, lab, dx, dy, anc in (((3.9, -1.4), "a1", 6, 12, "start"), ((2.1, 1.25), "a2", 8, -4, "start")):
    b.arrow(q, cls="l2"); b.dot(q, r=3.5); b.label(q, lab, dx=dx, dy=dy, anchor=anc)
single("ex14-vectors.svg", "Exercise 14: the columns a1 pointing down-right and a2 pointing up-right", b)

# ---------- 觀念 4:平面上的幾何線性變換(Lay 1.9 Tables 1–4)----------
# 單位正方形裡放一個不對稱的 F 字,才看得出翻面、轉向。
F_SHAPE = [(0.25, 0.12), (0.25, 0.88), (0.75, 0.88)]
F_BAR = [(0.25, 0.52), (0.6, 0.52)]
UNIT = [(0, 0), (1, 0), (1, 1), (0, 1)]


def fmt(v):
    if isinstance(v, str):
        return v
    return "−" + fmt(-v) if v < 0 else (str(int(v)) if float(v).is_integer() else str(v))


def matrix_svg(x, y, M):
    """在 (x, y) 畫一個 2×2 矩陣(置中),回傳 SVG 字串。"""
    cells = [[fmt(M[i][j]) for j in range(2)] for i in range(2)]
    widest = max(len(c) for row in cells for c in row)
    cw, rh = 16 + 8 * widest, 18
    out = []
    for i in range(2):
        for j in range(2):
            out.append(f'<text class="m" x="{x + (j - 0.5) * cw}" y="{y + i * rh}" text-anchor="middle">{cells[i][j]}</text>')
    L, Rr, T, B = x - cw - 4, x + cw + 4, y - 14, y + rh + 5
    out.append(f'<path class="ax" d="M{L + 5},{T} L{L},{T} L{L},{B} L{L + 5},{B}" style="stroke:currentColor"/>')
    out.append(f'<path class="ax" d="M{Rr - 5},{T} L{Rr},{T} L{Rr},{B} L{Rr - 5},{B}" style="stroke:currentColor"/>')
    return "".join(out)


def panel(M, title, sub_, mid, extra_line=None):
    p = Plot(-1.35, 2.35, -1.35, 2.35, s=38, pad=10, mid=mid)
    p.poly(UNIT, cls="ax", opacity=1, extra=' stroke-dasharray="3 3"')
    img = [apply(M, q) for q in UNIT]
    p.poly(img, cls="hl", opacity=0.6)
    if extra_line:
        p.line(*extra_line, cls="ax", extra=' stroke-dasharray="6 3"')
    p.axes(ticks=False, labels=False)
    p.polyline([apply(M, q) for q in F_SHAPE], cls="l2", extra=' style="stroke-width:3"')
    p.polyline([apply(M, q) for q in F_BAR], cls="l2", extra=' style="stroke-width:3"')
    p.arrow(apply(M, (1, 0)), cls="l1"); p.arrow(apply(M, (0, 1)), cls="l1")
    return p, title, sub_, M


def table_fig(name, aria, panels, cols):
    pw, ph = panels[0][0].w, panels[0][0].h
    cw, ch = pw + 16, ph + 96
    rows = (len(panels) + cols - 1) // cols
    body = []
    for i, (p, title, sub_, M) in enumerate(panels):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        body.append(f'<text class="t" x="{x0 + pw / 2}" y="{y0 + 14}" text-anchor="middle">{sub(title)}</text>')
        if sub_:
            body.append(f'<text x="{x0 + pw / 2}" y="{y0 + 30}" text-anchor="middle">{sub_}</text>')
        body.append(p.body(x0, y0 + 36))
        body.append(matrix_svg(x0 + pw / 2, y0 + 36 + ph + 24, M))
    svg(name, aria, cols * cw, rows * ch, "".join(body), [p.mid for p, *_ in panels])


table_fig("reflections.svg", "Reflections of the unit square: through the x1-axis, the x2-axis, the line x2 = x1, the line x2 = −x1, and the origin", [
    panel(((1, 0), (0, -1)), "through the x1-axis", "", "ah-rf1"),
    panel(((-1, 0), (0, 1)), "through the x2-axis", "", "ah-rf2"),
    panel(((0, 1), (1, 0)), "through x2 = x1", "", "ah-rf3", extra_line=((-1.3, -1.3), (2.3, 2.3))),
    panel(((0, -1), (-1, 0)), "through x2 = −x1", "", "ah-rf4", extra_line=((-1.3, 1.3), (1.3, -1.3))),
    panel(((-1, 0), (0, -1)), "through the origin", "", "ah-rf5"),
], cols=3)

table_fig("contractions.svg", "Horizontal and vertical contractions and expansions of the unit square", [
    panel(((0.5, 0), (0, 1)), "horizontal", "k = 0.5 (contraction)", "ah-ce1"),
    panel(((2, 0), (0, 1)), "horizontal", "k = 2 (expansion)", "ah-ce2"),
    panel(((1, 0), (0, 0.5)), "vertical", "k = 0.5 (contraction)", "ah-ce3"),
    panel(((1, 0), (0, 2)), "vertical", "k = 2 (expansion)", "ah-ce4"),
], cols=4)

table_fig("shears.svg", "Horizontal and vertical shears of the unit square", [
    panel(((1, -0.8), (0, 1)), "horizontal shear", "k = −0.8", "ah-sr1"),
    panel(((1, 0.8), (0, 1)), "horizontal shear", "k = 0.8", "ah-sr2"),
    panel(((1, 0), (-0.8, 1)), "vertical shear", "k = −0.8", "ah-sr3"),
    panel(((1, 0), (0.8, 1)), "vertical shear", "k = 0.8", "ah-sr4"),
], cols=4)

table_fig("projections.svg", "Projections of the unit square onto the x1-axis and onto the x2-axis", [
    panel(((1, 0), (0, 0)), "onto the x1-axis", "", "ah-pj1"),
    panel(((0, 0), (0, 1)), "onto the x2-axis", "", "ah-pj2"),
], cols=2)


# ---------- 觀念 5:映成與一對一(Lay 1.9 Figures 3–4 的示意)----------
def blob(cx, cy, rx, ry, cls="hl", op=0.45):
    return f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" style="opacity:{op}"/>'


def mapping_panel(x0, title, pairs, range_r, note):
    out = [f'<text class="t" x="{x0 + 120}" y="16" text-anchor="middle">{title}</text>']
    out.append(blob(x0 + 50, 110, 38, 70))
    out.append(blob(x0 + 190, 110, 42, 78, cls="ax", op=1))
    out.append(blob(x0 + 190, 110, 32, range_r, cls="bad", op=0.35))
    out.append(f'<text x="{x0 + 50}" y="198" text-anchor="middle">domain R^n</text>')
    out.append(f'<text x="{x0 + 190}" y="206" text-anchor="middle">codomain R^m</text>')
    for (ya, yb) in pairs:
        out.append(f'<circle class="pt" cx="{x0 + 50}" cy="{ya}" r="3.5"/>')
        out.append(f'<circle class="pt" cx="{x0 + 190}" cy="{yb}" r="3.5"/>')
        out.append(f'<line class="l1" x1="{x0 + 56}" y1="{ya}" x2="{x0 + 182}" y2="{yb}" marker-end="url(#ah-map)"/>')
    out.append(f'<text x="{x0 + 120}" y="228" text-anchor="middle">{note}</text>')
    return "".join(out)


body = (mapping_panel(0, "not onto", [(70, 90), (110, 110), (150, 130)], 30, "some b is never hit")
        + mapping_panel(260, "not one-to-one", [(70, 100), (100, 100), (150, 135)], 64, "two x's share one image")
        + mapping_panel(520, "one-to-one and onto", [(60, 55), (110, 110), (160, 165)], 76, "every b hit exactly once"))
svg("onto-one-to-one.svg", "Three mappings: not onto (the range is smaller than the codomain), not one-to-one (two inputs share an image), "
    "and one-to-one and onto", 780, 238, body, ["ah-map"])

print("ok")
