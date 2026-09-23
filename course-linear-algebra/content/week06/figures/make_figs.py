# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W6(Lay 2.3、2.5)的圖。
import math
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))


def sub(s):
    """把 x1、b2 這類「字母 + 數字」畫成下標;x 用斜體。"""
    def rep(m):
        head = m.group(1)
        if head == "x":
            head = '<tspan style="font-family: var(--font-serif); font-style: italic">x</tspan>'
        return f'{head}<tspan dy="4" font-size="10">{m.group(2)}</tspan><tspan dy="-4">​</tspan>'
    return re.sub(r"(?<![A-Za-z])([a-z])(\d)(?!\d)", rep, s)


class Plot:
    """數學座標 → SVG。"""

    def __init__(self, x0, x1, y0, y1, s=34, pad=26, mid="ah"):
        self.x0, self.x1, self.y0, self.y1, self.s, self.pad, self.mid = x0, x1, y0, y1, s, pad, mid
        self.w = (x1 - x0) * s + 2 * pad
        self.h = (y1 - y0) * s + 2 * pad
        self.parts = []

    def P(self, x, y):
        return (round(self.pad + (x - self.x0) * self.s, 1), round(self.pad + (self.y1 - y) * self.s, 1))

    def axes(self, ticks=True, labels=True, names=("x1", "x2")):
        (ax0, ay), (ax1, _) = self.P(self.x0, 0), self.P(self.x1, 0)
        (bx, by0), (_, by1) = self.P(0, self.y0), self.P(0, self.y1)
        self.parts.append(f'<line class="ax" x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}"/>')
        self.parts.append(f'<line class="ax" x1="{bx}" y1="{by0}" x2="{bx}" y2="{by1}"/>')
        if labels:
            self.parts.append(f'<text x="{ax1 - 4}" y="{ay - 6}" text-anchor="end">{sub(names[0])}</text>')
            self.parts.append(f'<text x="{bx + 6}" y="{by1 + 12}">{sub(names[1])}</text>')
        if ticks:
            for t in range(math.ceil(self.x0), math.floor(self.x1) + 1):
                if t:
                    x, y = self.P(t, 0)
                    self.parts.append(f'<line class="ax" x1="{x}" y1="{y - 3}" x2="{x}" y2="{y + 3}"/>')
            for t in range(math.ceil(self.y0), math.floor(self.y1) + 1):
                if t:
                    x, y = self.P(0, t)
                    self.parts.append(f'<line class="ax" x1="{x - 3}" y1="{y}" x2="{x + 3}" y2="{y}"/>')

    def line(self, p, q, cls="ax", extra=""):
        (x1, y1), (x2, y2) = self.P(*p), self.P(*q)
        self.parts.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{extra}/>')

    def dot(self, p, cls="pt", r=4):
        x, y = self.P(*p)
        self.parts.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}"/>')

    def label(self, p, text, dx=6, dy=-6, cls="t", anchor="start"):
        x, y = self.P(*p)
        self.parts.append(f'<text class="{cls}" x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{sub(text)}</text>')

    def raw(self, s):
        self.parts.append(s)

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


# ---------- 觀念 1:可逆矩陣定理的等價鏈(改畫課本 2.3 Figure 1)----------
W, H = 620, 340
body = ""
node_r = 17


def circ(x, y, lab, cls="hl"):
    return (f'<circle cx="{x}" cy="{y}" r="{node_r}" class="{cls}" style="opacity:0.85"/>'
            f'<circle cx="{x}" cy="{y}" r="{node_r}" class="ax" style="fill:none"/>'
            f'<text class="m" x="{x}" y="{y + 5}" text-anchor="middle">{lab}</text>')


def arr(p, q, mid="ah-imt", cls="l1", bend=0):
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    x1, y1 = x1 + ux * (node_r + 3), y1 + uy * (node_r + 3)
    x2, y2 = x2 - ux * (node_r + 6), y2 - uy * (node_r + 6)
    if bend:
        mx, my = (x1 + x2) / 2 - uy * bend, (y1 + y2) / 2 + ux * bend
        d = f"M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}"
        return f'<path class="{cls}" d="{d}" style="fill:none" marker-end="url(#{mid})"/>'
    return (f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'marker-end="url(#{mid})"/>')


# 中央的圈:(a) → (j) → (d) → (c) → (b) → (a)
cx, cy, R = 250, 150, 92
ring = ["a", "j", "d", "c", "b"]
pos = {}
for i, lab in enumerate(ring):
    ang = math.pi / 2 - i * 2 * math.pi / 5
    pos[lab] = (cx + R * math.cos(ang), cy - R * math.sin(ang))
for i, lab in enumerate(ring):
    nxt = ring[(i + 1) % 5]
    body += arr(pos[lab], pos[nxt])
for lab in ring:
    body += circ(pos[lab][0], pos[lab][1], f"({lab})")

# 右邊掛上 (k) 與 (g)
pos["k"] = (470, 78)
pos["g"] = (470, 150)
body += circ(*pos["k"], "(k)")
body += circ(*pos["g"], "(g)")
body += arr(pos["a"], pos["k"])
body += arr(pos["k"], pos["g"])
body += arr(pos["g"], pos["a"])

# 等價的掛件:排成一列放在圈的下方,不要壓到節點
body += f'<text class="t" x="{cx}" y="{cy + 5}" text-anchor="middle">同真同假</text>'
body += '<line class="ax" x1="40" y1="272" x2="580" y2="272" stroke-dasharray="4 4"/>'
for x0, group in ((90, ["(g)", "(h)", "(i)"]), (290, ["(d)", "(e)", "(f)"]), (470, ["(a)", "(l)"])):
    for i, lab in enumerate(group):
        body += f'<text class="m" x="{x0 + i * 56}" y="{306}" text-anchor="middle">{lab}</text>'
        if i:
            body += f'<text x="{x0 + i * 56 - 28}" y="{307}" text-anchor="middle">⟺</text>'
body += '<text x="40" y="292" text-anchor="start">掛在圈上的其他等價敘述:</text>'
svg("imt-ring.svg",
    "The circle of implications a to j to d to c to b back to a, with k and g attached on the right",
    W, H, body, ["ah-imt"])

# ---------- 觀念 4:LU 的形狀(改畫課本 2.5 Figure 1)----------
W, H = 520, 190


def grid(x, y, rows, cols, cells, cw=26, ch=22):
    out = []
    w, h = cols * cw, rows * ch
    for i in range(rows):
        for j in range(cols):
            t = cells(i, j)
            if t:
                out.append(f'<text class="m" x="{x + (j + 0.5) * cw}" y="{y + (i + 0.72) * ch}" '
                           f'text-anchor="middle">{t}</text>')
    out.append(f'<path class="ax" d="M{x + 6},{y} L{x},{y} L{x},{y + h} L{x + 6},{y + h}" style="stroke:currentColor"/>')
    out.append(f'<path class="ax" d="M{x + w - 6},{y} L{x + w},{y} L{x + w},{y + h} L{x + w - 6},{y + h}" '
               f'style="stroke:currentColor"/>')
    return "".join(out), w, h


body = ""
gL, wL, hL = grid(150, 40, 4, 4, lambda i, j: "1" if i == j else ("*" if i > j else "0"))
gU, wU, hU = grid(150 + wL + 18, 40, 4, 5,
                  lambda i, j: ("■" if (i, j) in {(0, 0), (1, 1), (2, 3)} else
                                ("*" if (i == 0 and j > 0) or (i == 1 and j > 1) or (i == 2 and j > 3) else
                                 ("0" if i < 3 else "0"))))
body += f'<text class="t" x="110" y="{40 + hL / 2 + 5}" text-anchor="middle">A =</text>'
body += gL + gU
body += f'<text x="{150 + wL / 2}" y="{40 + hL + 20}" text-anchor="middle">L (unit lower triangular)</text>'
body += f'<text x="{150 + wL + 18 + wU / 2}" y="{40 + hU + 20}" text-anchor="middle">U (echelon form)</text>'
body += f'<text class="t" x="{150 + wL + 18 + wU / 2}" y="26" text-anchor="middle">■ = pivot</text>'
svg("lu-shape.svg",
    "A equals L times U, where L is unit lower triangular and U is an echelon form with pivots marked",
    W, H, body, [])

# ---------- 觀念 4:解兩個三角系統(改畫課本 2.5 Figure 2)----------
W, H = 600, 210


def plane(cx, cy, w=120, h=40, skew=28):
    pts = [(cx - w / 2 + skew, cy - h / 2), (cx + w / 2 + skew, cy - h / 2),
           (cx + w / 2 - skew, cy + h / 2), (cx - w / 2 - skew, cy + h / 2)]
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon class="hl" points="{s}" style="opacity:0.45"/>'


def curve(x1, y1, x2, y2, lift, mid, cls="l1"):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - lift
    return f'<path class="{cls}" d="M{x1},{y1} Q{mx},{my} {x2},{y2}" style="fill:none" marker-end="url(#{mid})"/>'


body = plane(90, 120) + plane(300, 150) + plane(510, 120)
pts = [(74, 124), (284, 154), (494, 124)]
for (x, y), lab in zip(pts, ["x", "y", "b"]):
    body += f'<circle class="pt" cx="{x}" cy="{y}" r="4"/>'
    body += f'<text class="t" x="{x - 8}" y="{y + 4}" text-anchor="end">{lab}</text>'
body += curve(pts[0][0] + 8, pts[0][1] + 8, pts[1][0] - 6, pts[1][1] - 4, -26, "ah-lu", cls="l2")
body += curve(pts[1][0] + 8, pts[1][1] - 4, pts[2][0] - 6, pts[2][1] + 8, 26, "ah-lu", cls="l2")
body += '<text x="190" y="196" text-anchor="middle">multiply by U</text>'
body += '<text x="410" y="196" text-anchor="middle">multiply by L</text>'
body += curve(pts[0][0] + 8, pts[0][1] - 10, pts[2][0] - 8, pts[2][1] - 10, 66, "ah-lu")
body += f'<text class="t" x="{W / 2}" y="34" text-anchor="middle">multiply by A = LU</text>'
svg("lu-solve.svg",
    "Multiplying x by U gives y and multiplying y by L gives b, the same as multiplying x by A",
    W, H, body, ["ah-lu"])

# ---------- 觀念 3:乘 A 出去、乘 A⁻¹ 回來(改畫課本 2.3 Figure 2)----------
W, H = 460, 190


def plane0(cx, cy, w=150, h=44, skew=34):
    pts = [(cx - w / 2 + skew, cy - h / 2), (cx + w / 2 + skew, cy - h / 2),
           (cx + w / 2 - skew, cy + h / 2), (cx - w / 2 - skew, cy + h / 2)]
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon class="hl" points="{s}" style="opacity:0.45"/>'


body = plane0(150, 100) + plane0(330, 100)
body += '<circle class="pt" cx="132" cy="104" r="4"/><text class="t" x="124" y="108" text-anchor="end">x</text>'
body += '<circle class="pt" cx="312" cy="104" r="4"/><text class="t" x="322" y="108">Ax</text>'
body += ('<path class="l1" d="M140,92 Q240,52 304,94" style="fill:none" marker-end="url(#ah-inv)"/>'
         '<text x="240" y="46" text-anchor="middle">multiply by A</text>')
body += ('<path class="l2" d="M308,116 Q240,152 136,114" style="fill:none" marker-end="url(#ah-inv)"/>'
         '<text x="240" y="172" text-anchor="middle">multiply by A⁻¹</text>')
svg("inverse-transform.svg",
    "Multiplying x by A moves it to Ax; multiplying by A inverse brings it back",
    W, H, body, ["ah-inv"])

# ---------- 觀念 3:病態 —— 兩條幾乎重合的線,交點沿線滑很遠 ----------
p = Plot(2.2, 4.8, -0.4, 2.8, s=92, pad=26, mid="ah-cond")
for (c1, c2, r), cls in (((4.5, 3.1, 19.249), "l1"), ((1.6, 1.1, 6.843), "l2")):
    ys = [(r - c1 * x) / c2 for x in (2.2, 4.8)]
    p.line((2.2, ys[0]), (4.8, ys[1]), cls=cls)
p.line((2.2, 0), (4.8, 0), cls="ax")
p.label((4.8, 0), "x1", dx=-6, dy=-8, anchor="end")
p.dot((3.94, 0.49)); p.label((3.94, 0.49), "(3.94, 0.49)", dx=10, dy=14)
p.dot((2.90, 2.00)); p.label((2.90, 2.00), "(2.90, 2.00)", dx=10, dy=-10)
p.line((2.90, 2.00), (3.94, 0.49), cls="ax", extra=' stroke-dasharray="5 4"')
p.label((3.42, 1.25), "solution moves", dx=-12, dy=-6, anchor="end")
single("ill-conditioned.svg",
       "Two lines that almost coincide; rounding the right-hand side moves the intersection point a long way along them",
       p, caption="兩條線幾乎重合:右端只動 0.05%,交點就滑到另一處")

# ---------- 觀念 6:梯形網路(改畫課本 2.5 Figure 4)----------
class Circuit:
    def __init__(self, w, h, mid="ah-cir"):
        self.w, self.h, self.mid = w, h, mid
        self.p = []

    def wire(self, a, b):
        self.p.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" '
                      f'style="stroke:currentColor;stroke-width:1.6"/>')

    def _split(self, a, b, size):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        s = (m[0] - ux * size / 2, m[1] - uy * size / 2)
        e = (m[0] + ux * size / 2, m[1] + uy * size / 2)
        return s, e, (ux, uy), (nx, ny), m

    def resistor(self, a, b, label, side=1, dist=15):
        s, e, u, n, m = self._split(a, b, 28)
        self.wire(a, s); self.wire(e, b)
        pts = [s]
        for i in range(1, 7):
            amp = 5 if i % 2 else -5
            pts.append((s[0] + u[0] * 28 * i / 7 + n[0] * amp, s[1] + u[1] * 28 * i / 7 + n[1] * amp))
        pts.append(e)
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.p.append(f'<polyline points="{d}" style="fill:none;stroke:currentColor;stroke-width:1.6"/>')
        self.p.append(f'<text class="m" x="{m[0] + n[0] * dist * side:.1f}" y="{m[1] + n[1] * dist * side + 4:.1f}" '
                      f'text-anchor="middle">{label}</text>')

    def arrow(self, a, b, label):
        self.p.append(f'<line class="l1" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" '
                      f'marker-end="url(#{self.mid})"/>')
        self.p.append(f'<text class="m" x="{(a[0]+b[0])/2:.0f}" y="{a[1] - 8:.0f}" text-anchor="middle">{label}</text>')

    def box(self, x, y, w, h, label):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="ax" '
                      f'style="fill:none;stroke-dasharray:5 4"/>')
        self.p.append(f'<text x="{x + w / 2}" y="{y + h + 16}" text-anchor="middle">{label}</text>')

    def term(self, c, label, dx=-14, dy=4):
        self.p.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="3.2" style="fill:currentColor"/>')
        self.p.append(f'<text class="m" x="{c[0] + dx}" y="{c[1] + dy}" text-anchor="middle">{label}</text>')

    def svg(self, name, aria):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'role="img" aria-label="{aria}"><defs>{marker(self.mid)}</defs>')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(head + "".join(self.p) + "</svg>\n")


c = Circuit(560, 210, mid="ah-lad")
TOP, BOT = 70, 150
c.box(120, 46, 150, 120, "a series circuit")
c.box(300, 46, 150, 120, "a shunt circuit")
c.wire((40, TOP), (130, TOP))
c.resistor((130, TOP), (260, TOP), sub("R1"), side=-1)
c.wire((260, TOP), (380, TOP))
c.wire((380, TOP), (520, TOP))
c.wire((40, BOT), (520, BOT))
c.resistor((380, TOP), (380, BOT), sub("R2"), side=-1, dist=18)
c.term((40, TOP), sub("v1"), dx=-16)
c.term((40, BOT), "", dx=0)
c.term((285, TOP), sub("v2"), dx=0, dy=22)
c.term((285, BOT), "", dx=0)
c.term((520, TOP), sub("v3"), dx=16)
c.term((520, BOT), "", dx=0)
c.arrow((60, 44), (110, 44), sub("i1"))
c.arrow((290, 44), (340, 44), sub("i2"))
c.arrow((460, 44), (510, 44), sub("i3"))
c.svg("ladder.svg",
      "A ladder network: a series circuit with resistance R1 followed by a shunt circuit with resistance R2")

# ---------- 實作課:8 個內部節點的平板(Lay 2.5 Exercise 31)----------
p = Plot(-0.8, 5.8, -0.8, 2.8, s=58, pad=26, mid="ah-plate")
_x0, _y0 = p.P(0.45, 2.35)
_x1, _y1 = p.P(4.55, 0.25)
p.raw(f'<rect x="{_x0}" y="{_y0}" width="{_x1 - _x0}" height="{_y1 - _y0}" class="hl" style="opacity:0.25"/>')
nodes = {1: (1, 1.8), 2: (1, 0.8), 3: (2, 1.8), 4: (2, 0.8), 5: (3, 1.8), 6: (3, 0.8), 7: (4, 1.8), 8: (4, 0.8)}
for n, q in nodes.items():
    x, y = p.P(*q)
    p.raw(f'<circle cx="{x}" cy="{y}" r="11" class="l1" style="fill:var(--card)"/>')
    p.raw(f'<text class="m" x="{x}" y="{y + 4}" text-anchor="middle">{n}</text>')
for aa, bb in ((1, 2), (3, 4), (5, 6), (7, 8), (1, 3), (3, 5), (5, 7), (2, 4), (4, 6), (6, 8)):
    p.line(nodes[aa], nodes[bb], cls="ax")
p.label((2.5, 2.35), "0°", dx=0, dy=-8, anchor="middle")
p.label((2.5, 0.25), "10°", dx=0, dy=18, anchor="middle")
p.label((0.45, 1.3), "5°", dx=-10, dy=4, anchor="end")
p.label((4.55, 1.3), "20°", dx=10, dy=4)
single("plate.svg",
       "A plate with eight interior nodes; the four edges are held at 0, 10, 5 and 20 degrees",
       p, caption="Lay 2.5 Exercise 31 的平板(節點 1–8)")

print("wrote:", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith(".svg"))))
