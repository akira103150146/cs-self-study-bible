# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W3(Lay 1.5、1.7)的圖。座標一律用數學座標(y 向上),由 Plot 換算成 SVG 像素。
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

    def axes(self, ticks=True):
        (ax0, ay), (ax1, _) = self.P(self.x0, 0), self.P(self.x1, 0)
        (bx, by0), (_, by1) = self.P(0, self.y0), self.P(0, self.y1)
        self.parts.append(f'<line class="ax" x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}"/>')
        self.parts.append(f'<line class="ax" x1="{bx}" y1="{by0}" x2="{bx}" y2="{by1}"/>')
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

    def poly(self, pts, cls="hl", opacity=0.55):
        s = " ".join(f"{x},{y}" for x, y in (self.P(*p) for p in pts))
        self.parts.append(f'<polygon class="{cls}" points="{s}" style="opacity:{opacity}"/>')

    def dot(self, p, cls="pt", r=4):
        x, y = self.P(*p)
        self.parts.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}"/>')

    def label(self, p, text, dx=6, dy=-6, cls="t", anchor="start"):
        x, y = self.P(*p)
        self.parts.append(f'<text class="{cls}" x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{sub(text)}</text>')

    def raw(self, s):
        self.parts.append(s)

    def body(self, dx=0):
        return f'<g transform="translate({dx},0)">' + "".join(self.parts) + "</g>"


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


def pair(name, aria, a, b, cap_a, cap_b, gap=30):
    w = a.w + gap + b.w
    h = max(a.h, b.h) + 24
    body = a.body() + b.body(a.w + gap)
    body += f'<text x="{a.w / 2}" y="{h - 6}" text-anchor="middle">{cap_a}</text>'
    body += f'<text x="{a.w + gap + b.w / 2}" y="{h - 6}" text-anchor="middle">{cap_b}</text>'
    svg(name, aria, w, h, body, [a.mid, b.mid])


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(c, a):
    return tuple(c * x for x in a)


# ---------- 三維斜投影(x1 往左下、x2 往右、x3 往上,和課本的立體圖一致)----------
def proj(X, o=(150, 150), s=38):
    x, y, z = X
    return (round(o[0] + s * (-0.62 * x + 1.0 * y), 1), round(o[1] + s * (0.42 * x - 1.0 * z), 1))


def axes3d(o, s=38, ends=((2.6, 0, 0), (0, 3.2, 0), (0, 0, 2.8))):
    out = []
    for end, lab in zip(ends, ("x1", "x2", "x3")):
        a, b = proj((0, 0, 0), o, s), proj(end, o, s)
        out.append(f'<line class="ax" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
        out.append(f'<text x="{b[0] + 4}" y="{b[1] + 4}">{sub(lab)}</text>')
    return out


def seg3d(A, B, o, cls="l1", arrow=None, s=38, extra=""):
    a, b = proj(A, o, s), proj(B, o, s)
    m = f' marker-end="url(#{arrow})"' if arrow else ""
    return f'<line class="{cls}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"{m}{extra}/>'


def plane3d(p0, u, v, a0, a1, b0, b1, o, cls="hl", opacity=0.5, s=38):
    corners = [add(p0, add(mul(a, u), mul(b, v))) for a, b in ((a0, b0), (a1, b0), (a1, b1), (a0, b1))]
    pts = " ".join("{},{}".format(*proj(c, o, s)) for c in corners)
    return f'<polygon class="{cls}" points="{pts}" style="opacity:{opacity}"/>', corners


def dot3d(X, o, lab=None, dx=6, dy=-6, s=38, r=3.5):
    q = proj(X, o, s)
    out = f'<circle class="pt" cx="{q[0]}" cy="{q[1]}" r="{r}"/>'
    if lab:
        out += f'<text class="t" x="{q[0] + dx}" y="{q[1] + dy}">{sub(lab)}</text>'
    return out


# ---------- 觀念 1:齊次方程組的解集 = 通過原點的直線或平面(Lay 1.5 Figures 1–2)----------
o1, o2 = (150, 150), (470, 150)
body = []
v = mul(1.5, (4 / 3, 0, 1))        # 課本 Example 1 的 v = (4/3, 0, 1),放大 1.5 倍畫
body += axes3d(o1)
body.append(seg3d(mul(-0.9, v), mul(1.6, v), o1, cls="l1"))
body.append(seg3d((0, 0, 0), v, o1, cls="l2", arrow="ah-3d"))
body.append(dot3d(v, o1, "v", -4, 18))
pe = proj(mul(1.6, v), o1)
body.append(f'<text class="t" x="{pe[0] - 4}" y="{pe[1] - 8}" text-anchor="middle">Span{{v}}</text>')
body.append(f'<text x="{o1[0]}" y="262" text-anchor="middle">one free variable: a line through 0</text>')
u, v = mul(1.8, (0.3, 1, 0)), mul(1.8, (0.2, 0, 1))   # 課本 Example 2 的 u、v,放大 1.8 倍畫
poly, corners = plane3d((0, 0, 0), u, v, -0.3, 1.5, -0.3, 1.4, o2)
body.append(poly)
body += axes3d(o2)
body.append(seg3d((0, 0, 0), u, o2, cls="l2", arrow="ah-3d"))
body.append(seg3d((0, 0, 0), v, o2, cls="l2", arrow="ah-3d"))
body.append(dot3d(u, o2, "u", 2, 18)); body.append(dot3d(v, o2, "v", -18, 2))
pc = proj(corners[2], o2)
body.append(f'<text class="t" x="{pc[0] + 6}" y="{pc[1]}">Span{{u, v}}</text>')
body.append(f'<text x="{o2[0]}" y="262" text-anchor="middle">two free variables: a plane through 0</text>')
svg("homog-line-plane.svg", "Solution set of Ax = 0: a line through 0 (one free variable) or a plane through 0 (two free variables)",
    640, 272, "".join(body), ["ah-3d"])

# ---------- 觀念 2:Ax = b 的解集 = 把 Ax = 0 的解集平移 p(Lay 1.5 Figure 5)----------
p = Plot(-3, 6.5, -1.2, 4.2, s=40, mid="ah-tr")
v, pp = (2, 0.5), (1, 2)
p.axes(ticks=False)
p.line(mul(-1.4, v), mul(3.1, v), cls="l1", extra=' style="stroke-width:2.5"')
p.line(add(pp, mul(-1.9, v)), add(pp, mul(2.6, v)), cls="l2", extra=' style="stroke-width:2.5"')
t = 1.6
p.arrow(pp, cls="l2")
p.arrow(mul(t, v), cls="l1")
p.arrow(add(pp, mul(t, v)), q=mul(t, v), cls="ax", dashed=True)
p.dot(pp); p.dot(mul(t, v)); p.dot(add(pp, mul(t, v))); p.dot((0, 0), r=3)
p.label(pp, "p", dx=-16, dy=-2)
p.label(mul(t, v), "tv", dx=2, dy=18)
p.label(add(pp, mul(t, v)), "p + tv", dx=-2, dy=-10, anchor="middle")
p.label(mul(3.1, v), "Ax = 0", dx=-4, dy=18, anchor="end")
p.label(add(pp, mul(2.6, v)), "Ax = b", dx=-4, dy=-8, anchor="end")
single("translate.svg", "The solution set of Ax = b is the solution set of Ax = 0 translated by p", p)

# ---------- 觀念 2:三維版,兩個平行平面(Lay 1.5 Figure 6)----------
o = (170, 175)
body = []
u, v = (1.1, 0.2, 0.0), (0.0, 1.3, 0.25)
pp = (0, 0, 1.3)
poly0, _ = plane3d((0, 0, 0), u, v, 0, 2.2, 0, 2.2, o, cls="hl", opacity=0.55)
poly1, c1 = plane3d(pp, u, v, 0, 2.2, 0, 2.2, o, cls="bad", opacity=0.35)
body += axes3d(o, ends=((3.2, 0, 0), (0, 3.6, 0), (0, 0, 3.2)))
body.append(poly0); body.append(poly1)
body.append(seg3d((0, 0, 0), pp, o, cls="l2", arrow="ah-3d6"))
body.append(dot3d(pp, o, "p", -16, 2))
q0 = proj(add((0, 0, 0), add(mul(2.2, u), mul(2.2, v))), o)
q1 = proj(c1[2], o)
body.append(f'<text class="t" x="{q0[0] + 6}" y="{q0[1] + 4}">Ax = 0</text>')
body.append(f'<text class="t" x="{q1[0] + 6}" y="{q1[1] + 4}">Ax = b</text>')
svg("parallel-planes.svg", "Parallel solution sets of Ax = b and Ax = 0: two parallel planes, one through the origin",
    380, 270, "".join(body), ["ah-3d6"])


# ---------- 觀念 4:兩個向量(Lay 1.7 Figure 1)----------
def two_vectors(v1, v2, mid):
    p = Plot(-0.5, 7, -0.5, 3, s=34, pad=20, mid=mid)
    p.axes(ticks=False)
    for q in (v2, v1):
        p.arrow(q); p.dot(q, r=3.5)
    p.label(v1, f"({v1[0]}, {v1[1]})", dx=-4, dy=-8, anchor="end")
    p.label(v2, f"({v2[0]}, {v2[1]})", dx=4, dy=-8)
    return p


a = two_vectors((3, 1), (6, 2), "ah-dep")
b = two_vectors((3, 2), (6, 2), "ah-ind")
pair("two-vectors.svg", "Left: (3, 1) and (6, 2) lie on one line, linearly dependent. Right: (3, 2) and (6, 2) do not, linearly independent",
     a, b, "linearly dependent", "linearly independent")

# ---------- 觀念 4:ℝ³ 中 w 在不在 Span{u, v} 裡(Lay 1.7 Figure 2)----------
o1, o2 = (150, 140), (470, 140)
u, v = (1.5, 0.5, 0), (0.5, 3, 0)
body = []
for o, w, cap in ((o1, (1.6, 1.8, 0), "dependent: w in Span{u, v}"),
                  (o2, (0.8, 2.0, 2.2), "independent: w not in Span{u, v}")):
    poly, _ = plane3d((0, 0, 0), u, v, -0.2, 1.4, -0.2, 1.25, o)
    body.append(poly)
    body += axes3d(o)
    body.append(seg3d((0, 0, 0), u, o, cls="l1", arrow="ah-3d7"))
    body.append(seg3d((0, 0, 0), v, o, cls="l1", arrow="ah-3d7"))
    body.append(seg3d((0, 0, 0), w, o, cls="l2", arrow="ah-3d7"))
    body.append(dot3d(u, o, "u", -14, 12)); body.append(dot3d(v, o, "v", 6, 12)); body.append(dot3d(w, o, "w", 6, -4))
    if w[2]:
        body.append(seg3d(w, (w[0], w[1], 0), o, cls="ax", extra=' stroke-dasharray="4 4"'))
    body.append(f'<text x="{o[0]}" y="262" text-anchor="middle">{cap}</text>')
svg("dep-in-r3.svg", "Left: w lies in the plane spanned by u and v, so {u, v, w} is linearly dependent. "
    "Right: w sticks out of the plane, so the set is linearly independent", 640, 272, "".join(body), ["ah-3d7"])

# ---------- 觀念 5:ℝ² 中三個向量一定相依(Lay 1.7 Figure 4)----------
p = Plot(-3, 5, -1.8, 3, s=40, mid="ah-thm8")
p.axes(ticks=True)
for q, dx, dy, anchor in (((2, 1), 4, -6, "start"), ((4, -1), 4, 16, "start"), ((-2, 2), -4, -6, "end")):
    p.arrow(q); p.dot(q, r=3.5)
    p.label(q, f"({q[0]}, {q[1]})", dx=dx, dy=dy, anchor=anchor)
single("three-in-r2.svg", "Three vectors (2, 1), (4, −1), (−2, 2) in the plane: a linearly dependent set", p)

# ---------- 觀念 2:通過 p、q 的直線 M(Lay 1.5 Exercises 25–26 的示意圖)----------
p = Plot(-6.5, 6, -2.4, 3, s=34, mid="ah-pq")
P, Q = (-5, 1.6), (-2.6, -0.8)
QP = (Q[0] - P[0], Q[1] - P[1])
p.poly([(0, 0), Q, QP, (-P[0], -P[1])], cls="hl", opacity=0.45)
p.axes(ticks=False)
p.line(add(P, mul(-0.45, QP)), add(P, mul(1.7, QP)), cls="l2", extra=' style="stroke-width:2.5"')
for X, lab, dx, dy, anc in ((P, "p", -8, 16, "end"), (Q, "q", -6, 16, "end"),
                            ((-P[0], -P[1]), "−p", 6, 14, "start")):
    p.arrow(X, cls="ax"); p.dot(X, r=3.5); p.label(X, lab, dx=dx, dy=dy, anchor=anc)
p.arrow(QP, cls="l1"); p.dot(QP, r=3.5); p.label(QP, "q − p", dx=6, dy=16)
p.label(add(P, mul(1.7, QP)), "M", dx=6, dy=4)
single("line-pq.svg", "The line M through p and q is parallel to the vector q minus p", p)

print("ok")
