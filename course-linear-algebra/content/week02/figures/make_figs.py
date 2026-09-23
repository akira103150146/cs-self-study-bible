# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W2(Lay 1.3–1.4)的圖。座標一律用數學座標(y 向上),由 Plot 換算成 SVG 像素。
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))


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
        self.parts.append(f'<text x="{ax1 - 4}" y="{ay - 6}" text-anchor="end">x1</text>')
        self.parts.append(f'<text x="{bx + 6}" y="{by1 + 12}">x2</text>')
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
        self.parts.append(f'<text class="{cls}" x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{text}</text>')

    def out_label(self, q, text, dist=16, cls="t", perp=False):
        """標籤放在箭頭尖端的外側(沿 q 的方向);perp=True 改放在垂直方向。
        固定放右上角會被往左下指的箭頭壓到(−v、−2v 的負號會不見),所以依方向決定。"""
        n = math.hypot(*q) or 1
        d = (-q[1] / n, q[0] / n) if perp else (q[0] / n, q[1] / n)
        if perp and d[1] < 0:                      # 垂直方向一律取偏上的那一側
            d = (-d[0], -d[1])
        dx, dy = d[0] * dist, -d[1] * dist + 4     # SVG 的 y 軸向下
        anchor = "start" if d[0] > 0.25 else ("end" if d[0] < -0.25 else "middle")
        self.label(q, text, dx=dx + (3 if anchor == "start" else -3 if anchor == "end" else 0),
                   dy=dy, cls=cls, anchor=anchor)

    def svg(self, aria, extra_w=0):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w + extra_w} {self.h}" '
                f'width="{self.w + extra_w}" role="img" aria-label="{aria}">'
                f'<defs><marker id="{self.mid}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
                f'markerWidth="11" markerHeight="11" orient="auto"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>')
        return head + "".join(self.parts) + "</svg>\n"


def save(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(c, a):
    return (c * a[0], c * a[1])


# ---------- 觀念 1:平行四邊形法則(Lay 1.3 Example 2)----------
p = Plot(-7, 3, -1, 4, s=34, mid="ah-par")
u, v = (2, 2), (-6, 1)
p.poly([(0, 0), u, add(u, v), v])
p.axes()
p.arrow(u); p.arrow(v); p.arrow(add(u, v), cls="l2")
p.dot(u); p.dot(v); p.dot(add(u, v))
p.label(u, "u (2, 2)"); p.label(v, "v (−6, 1)", dx=0, dy=20, anchor="middle")
p.label(add(u, v), "u + v (−4, 3)", dx=-6, dy=-8, anchor="end")
save("parallelogram.svg", p.svg("Parallelogram rule: u + v is the fourth vertex of the parallelogram with vertices u, 0, v"))

# ---------- 觀念 1:純量倍數(Lay 1.3 Example 3)----------
p = Plot(-4, 7, -3, 2, s=34, mid="ah-mul")
u = (3, -1)
p.line((-4, 4 / 3), (7, -7 / 3), cls="l1", extra=' style="opacity:.35;stroke-width:6"')
p.axes()
p.arrow(mul(2, u), cls="l2"); p.arrow(u); p.arrow(mul(-2 / 3, u))
for c, name, dx, dy in [(1, "u", 0, -10), (2, "2u", 0, -10), (-2 / 3, "−(2/3)u", -6, -10)]:
    p.dot(mul(c, u)); p.label(mul(c, u), name, dx=dx, dy=dy, anchor="middle" if c > 0 else "end")
p.label((6.2, -2.1), "all multiples of u: a line through 0", dx=0, dy=22, cls="", anchor="end")
save("multiples.svg", p.svg("Scalar multiples of u lie on a line through the origin"))


# ---------- 格線:v1、v2 的線性組合 ----------
def grid(name, aria, a, b, rng, pts, labels_ab, win, s=30, mid="ah-grid"):
    """a、b 兩個方向的格線;pts = [(係數 ca, cb, 標籤)]。win = (x0, x1, y0, y1)。"""
    p = Plot(*win, s=s, mid=mid)
    x0, x1, y0, y1 = win
    # 把一條無限直線截在視窗內(參數式 P + t d)
    def clip(P, d):
        ts = []
        for (lo, hi, i) in ((x0, x1, 0), (y0, y1, 1)):
            if abs(d[i]) < 1e-12:
                if not lo <= P[i] <= hi:
                    return None
                continue
            ts.append(sorted(((lo - P[i]) / d[i], (hi - P[i]) / d[i])))
        t0 = max(t[0] for t in ts); t1 = min(t[1] for t in ts)
        return None if t0 >= t1 else ((P[0] + t0 * d[0], P[1] + t0 * d[1]), (P[0] + t1 * d[0], P[1] + t1 * d[1]))
    for k in rng:
        for P, d in ((mul(k, a), b), (mul(k, b), a)):
            seg = clip(P, d)
            if seg:
                cls = "l1" if k == 0 else "ax"
                p.line(*seg, cls=cls, extra=' style="opacity:.9"' if k == 0 else ' style="opacity:.55"')
    p.dot((0, 0)); p.label((0, 0), "0", dx=-12, dy=16, cls="")
    for (la, pa) in labels_ab:
        p.dot(pa, cls="pt", r=3);
    for ca, cb, lab, dx, dy in pts:
        q = add(mul(ca, a), mul(cb, b))
        p.dot(q, r=4.5); p.label(q, lab, dx=dx, dy=dy)
    for la, pa in labels_ab:
        p.out_label(pa, la, dist=14, cls="", perp=True)   # 垂直於格線放,才不會被格線穿過
    save(name, p.svg(aria))


v1, v2 = (-1, 1), (2, 1)
grid("lincomb-grid.svg", "Linear combinations of v1 and v2 drawn as a grid", v1, v2, range(-4, 5),
     [(3, -2, "u", 6, -6), (2.5, -0.5, "w", 6, -6)],
     [("v1", v1), ("v2", v2), ("2v1", mul(2, v1)), ("3v1", mul(3, v1)), ("2v2", mul(2, v2)),
      ("−v1", mul(-1, v1)), ("−v2", mul(-1, v2)), ("−2v2", mul(-2, v2))],
     (-8, 6, -4, 5), s=30, mid="ah-grid1")

# Lay 1.3 Exercises 7–8:u 陡、v 緩(和課本圖的樣子相近)
u, v = (0.5, 1.0), (1.05, 0.4)
grid("ex7-8-grid.svg", "Grid of linear combinations of u and v with points a, b, c, d, w, x, y, z", u, v, range(-5, 6),
     [(1, -2, "a", 6, 14), (2, -2, "b", 6, -6), (2, -3.5, "c", -14, -6), (3, -4, "d", -14, -6),
      (-1, 2, "w", 6, 14), (-2, 2, "x", 6, 14), (-2, 3.5, "y", 6, -6), (-3, 4, "z", 6, 14)],
     [("u", u), ("v", v), ("2v", mul(2, v)), ("−u", mul(-1, u)), ("−v", mul(-1, v)), ("−2v", mul(-2, v))],
     (-4.5, 4.5, -3.2, 3.2), s=40, mid="ah-grid2")


# ---------- Span{v} 是直線、Span{u, v} 是平面(三維示意,斜投影)----------
def proj(X, o=(150, 150), s=38):
    """(x1, x2, x3) → 螢幕:x1 往左下、x2 往右、x3 往上(和課本的立體圖一致)。"""
    x, y, z = X
    return (round(o[0] + s * (-0.62 * x + 1.0 * y), 1), round(o[1] + s * (0.42 * x - 1.0 * z), 1))


def svg3d(name, aria, body, w=330, h=270):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{aria}">'
            '<defs><marker id="ah-3d" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" '
            'orient="auto"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>')
    save(name, head + body + "</svg>\n")


def axes3d(o):
    out = []
    for end, lab in (((2.6, 0, 0), "x1"), ((0, 3.2, 0), "x2"), ((0, 0, 2.8), "x3")):
        a, b = proj((0, 0, 0), o), proj(end, o)
        out.append(f'<line class="ax" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
        out.append(f'<text x="{b[0] + 4}" y="{b[1] + 4}">{lab}</text>')
    return out


def seg3d(A, B, o, cls="l1", arrow=False):
    a, b = proj(A, o), proj(B, o)
    m = ' marker-end="url(#ah-3d)"' if arrow else ""
    return f'<line class="{cls}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"{m}/>'


o1, o2 = (150, 150), (470, 150)
body = []
# 左:Span{v}
v = (0.6, 1.0, 1.6)
body += axes3d(o1)
body.append(seg3d(tuple(-1.2 * c for c in v), tuple(1.6 * c for c in v), o1, cls="l1"))
body.append(seg3d((0, 0, 0), v, o1, cls="l2", arrow=True))
pv = proj(v, o1)
body.append(f'<text class="t" x="{pv[0] + 8}" y="{pv[1] + 4}">v</text>')
pe = proj(tuple(1.6 * c for c in v), o1)
body.append(f'<text class="t" x="{pe[0] + 6}" y="{pe[1] + 6}">Span{{v}}</text>')
body.append(f'<text x="{o1[0]}" y="258" text-anchor="middle">a line through 0</text>')
# 右:Span{u, v}
u, v = (1.4, 0.3, 0.9), (-0.2, 1.6, 0.5)
corners = [tuple(a * uu + b * vv for uu, vv in zip(u, v)) for a, b in ((-1.3, -1.1), (1.5, -1.1), (1.5, 1.5), (-1.3, 1.5))]
pts = " ".join("{},{}".format(*proj(c, o2)) for c in corners)
body.append(f'<polygon class="hl" points="{pts}" style="opacity:.5"/>')
body += axes3d(o2)
body.append(seg3d((0, 0, 0), u, o2, cls="l2", arrow=True))
body.append(seg3d((0, 0, 0), v, o2, cls="l2", arrow=True))
uv = tuple(a + b for a, b in zip(u, v))
body.append(seg3d(u, uv, o2, cls="ax")); body.append(seg3d(v, uv, o2, cls="ax"))
# u + v 原本放右下、v 放右上,兩個標籤會疊在一起;改成 u + v 往左上(靠右對齊)、v 往右下
for X, lab, dx, dy, anchor in ((u, "u", -12, 12, "end"), (v, "v", 10, 16, "start"), (uv, "u + v", -10, -8, "end")):
    q = proj(X, o2)
    body.append(f'<circle class="pt" cx="{q[0]}" cy="{q[1]}" r="3.5"/>'
                f'<text class="t" x="{q[0] + dx}" y="{q[1] + dy}" text-anchor="{anchor}">{lab}</text>')
pc = proj(corners[2], o2)
body.append(f'<text class="t" x="{pc[0] - 4}" y="{pc[1] - 8}" text-anchor="end">Span{{u, v}}</text>')
body.append(f'<text x="{o2[0]}" y="258" text-anchor="middle">a plane through 0</text>')
svg3d("span-line-plane.svg", "Span of one nonzero vector is a line; span of two non-parallel vectors is a plane", "".join(body), w=640)


# ---------- 解答用:Lay 1.3 Exercises 3–4 ----------
def ex34(name, u, v, win):
    p = Plot(*win, s=20, pad=22, mid="ah-" + name[:5])
    p.axes(ticks=True)
    items = [(u, "u", "l1"), (v, "v", "l1"), (mul(-1, v), "−v", "ax"), (mul(-2, v), "−2v", "ax"),
             (add(u, v), "u+v", "l2"), (add(u, mul(-1, v)), "u−v", "l2"), (add(u, mul(-2, v)), "u−2v", "l2")]
    for q, lab, cls in items:
        p.arrow(q, cls=cls)
        p.dot(q, r=3)
        p.out_label(q, lab)
    save(name, p.svg("Vectors u, v, −v, −2v, u+v, u−v, u−2v drawn as arrows"))


ex34("ex3-vectors.svg", (-1, 2), (-3, 3), (-7, 7, -7, 7))
ex34("ex4-vectors.svg", (3, 2), (2, 3), (-7, 7, -7, 7))

# ---------- Lay 1.3 Exercise 40 ----------
p = Plot(-0.5, 4.8, -0.6, 2.9, s=60, pad=24, mid="ah-ex40")
for q, lab in (((1.0, -0.12), "v1"), ((0.9, 0.9), "v2"), ((0.8, 2.6), "v3")):
    p.arrow(q); p.dot(q, r=3.5); p.out_label(q, lab)
p.arrow((4.1, 1.45), cls="l2"); p.dot((4.1, 1.45), r=4); p.out_label((4.1, 1.45), "b")
p.dot((0, 0), r=2.5); p.label((0, 0), "0", dx=-12, dy=4, cls="")
save("ex40.svg", p.svg("Vectors v1, v2, v3 and b in the plane"))

# ---------- Lay 1.3 Exercise 39:三角形平板 ----------
p = Plot(-0.5, 9, -0.5, 4.8, s=34, pad=22, mid="ah-ex39")
p.poly([(0, 1), (8, 1), (2, 4)], cls="hl", opacity=0.6)
p.axes()
for q, lab, dx, dy in (((0, 1), "v1", -22, -4), ((8, 1), "v2", 6, 14), ((2, 4), "v3", 4, -8)):
    p.dot(q, r=4); p.label(q, lab, dx=dx, dy=dy)
p.label((8, 0), "8", dx=-4, dy=16, cls=""); p.label((0, 4), "4", dx=-16, dy=4, cls="")
save("ex39-plate.svg", p.svg("Triangular plate with vertices v1 = (0, 1), v2 = (8, 1), v3 = (2, 4)"))

print("ok")
