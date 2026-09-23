# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W5(Lay 2.1、2.2、2.7)的圖。座標一律用數學座標(y 向上),由 Plot 換算成 SVG 像素。
import math
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))


def sub(s):
    """把 x1、b2、e1 這類「字母 + 數字」畫成下標(和題幹的 $x_1$ 一致);x 軸變數用斜體。"""
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

    def origin(self):
        x, y = self.P(0, 0)
        self.parts.append(f'<circle class="pt" cx="{x}" cy="{y}" r="2.5"/>')

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


def strip(name, aria, panels, captions, gap=18):
    """一排 n 張小圖,每張下面一行說明。"""
    w = sum(p.w for p in panels) + gap * (len(panels) - 1)
    h = max(p.h for p in panels) + 24
    body, x = "", 0
    for p, cap in zip(panels, captions):
        body += p.body(x, 0)
        body += f'<text x="{x + p.w / 2}" y="{h - 6}" text-anchor="middle">{cap}</text>'
        x += p.w + gap
    svg(name, aria, w, h, body, [p.mid for p in panels])


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(c, a):
    return tuple(c * x for x in a)


def apply(M, p):
    """2×2 矩陣乘 2 維點,或 3×3 齊次矩陣乘 (x, y, 1)。"""
    if len(M) == 2:
        return (M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1])
    q = (p[0], p[1], 1)
    return tuple(sum(M[i][j] * q[j] for j in range(3)) for i in range(2))


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


# ---------- 觀念 2:乘法 = 兩台機器接起來(改畫課本 2.1 Figure 2–3)----------
def plane(cx, cy, w=118, h=40, skew=28):
    """畫一塊傾斜的平面(表示 R^n)。"""
    pts = [(cx - w / 2 + skew, cy - h / 2), (cx + w / 2 + skew, cy - h / 2),
           (cx + w / 2 - skew, cy + h / 2), (cx - w / 2 - skew, cy + h / 2)]
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon class="hl" points="{s}" style="opacity:0.45"/>'


def curve(x1, y1, x2, y2, lift, mid, cls="l1"):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - lift
    return f'<path class="{cls}" d="M{x1},{y1} Q{mx},{my} {x2},{y2}" style="fill:none" marker-end="url(#{mid})"/>'


W, H = 640, 250
cx = [95, 320, 545]
cy = 125
body = "".join(plane(c, cy) for c in cx)
pts = [(c - 18, cy + 4) for c in cx]
for (x, y) in pts:
    body += f'<circle class="pt" cx="{x}" cy="{y}" r="4"/>'
labels = ["x", "Bx", "A(Bx)"]
for (x, y), lab in zip(pts, labels):
    body += f'<text class="t" x="{x - 8}" y="{y + 4}" text-anchor="end">{lab}</text>'
body += curve(pts[0][0] + 10, pts[0][1] - 10, pts[1][0] - 6, pts[1][1] - 12, 46, "ah-cmp")
body += curve(pts[1][0] + 10, pts[1][1] - 10, pts[2][0] - 6, pts[2][1] - 12, 46, "ah-cmp")
body += f'<text x="{(pts[0][0] + pts[1][0]) / 2}" y="{cy - 58}" text-anchor="middle">multiply by B</text>'
body += f'<text x="{(pts[1][0] + pts[2][0]) / 2}" y="{cy - 58}" text-anchor="middle">multiply by A</text>'
body += curve(pts[0][0] + 6, pts[0][1] + 14, pts[2][0] - 10, pts[2][1] + 12, -62, "ah-cmp", cls="l2")
body += f'<text class="t" x="{W / 2}" y="{cy + 108}" text-anchor="middle">multiply by AB (one step)</text>'
svg("compose.svg", "Multiplying x by B and then by A has the same effect as multiplying x by the single matrix AB",
    W, H, body, ["ah-cmp"])


# ---------- 觀念 2:尺寸要對得上(改畫課本 2.1 Example 4 的圖)----------
def grid(x, y, rows, cols, cw=17, ch=17, star="*"):
    out = []
    w, h = cols * cw, rows * ch
    for i in range(rows):
        for j in range(cols):
            out.append(f'<text class="m" x="{x + (j + 0.5) * cw}" y="{y + (i + 0.72) * ch}" '
                       f'text-anchor="middle">{star}</text>')
    out.append(f'<path class="ax" d="M{x + 5},{y} L{x},{y} L{x},{y + h} L{x + 5},{y + h}" style="stroke:currentColor"/>')
    out.append(f'<path class="ax" d="M{x + w - 5},{y} L{x + w},{y} L{x + w},{y + h} L{x + w - 5},{y + h}" '
               f'style="stroke:currentColor"/>')
    return "".join(out), w, h


W, H = 520, 210
body = ""
gA, wA, hA = grid(40, 40, 3, 5)
gB, wB, hB = grid(40 + wA + 24, 40, 5, 2)
gC, wC, hC = grid(40 + wA + 24 + wB + 52, 40, 3, 2)
body += gA + gB + gC
xA, xB, xC = 40 + wA / 2, 40 + wA + 24 + wB / 2, 40 + wA + 24 + wB + 52 + wC / 2
body += f'<text class="t" x="{xA}" y="30">A</text>'
body += f'<text class="t" x="{xB}" y="30">B</text>'
body += f'<text class="t" x="{xC}" y="30">AB</text>'
body += f'<text x="{40 + wA + 24 + wB + 26}" y="{40 + hB / 2 + 4}" text-anchor="middle">=</text>'
body += f'<text x="{xA}" y="{40 + hB + 22}" text-anchor="middle">3 × 5</text>'
body += f'<text x="{xB}" y="{40 + hB + 22}" text-anchor="middle">5 × 2</text>'
body += f'<text x="{xC}" y="{40 + hB + 22}" text-anchor="middle">3 × 2</text>'
y1, y2 = 40 + hB + 36, 40 + hB + 62
body += (f'<path class="l2" d="M{xA + 16},{y1 - 10} L{xA + 16},{y1} L{xB - 16},{y1} L{xB - 16},{y1 - 10}" '
         f'style="fill:none"/>')
body += f'<text class="t" x="{(xA + xB) / 2}" y="{y1 + 17}" text-anchor="middle">must match</text>'
body += (f'<path class="l1" d="M{xA - 18},{y1 - 10} L{xA - 18},{y2} L{xC + 18},{y2} L{xC + 18},{y1 - 10}" '
         f'style="fill:none"/>')
body += f'<text class="t" x="{(xA + xC) / 2}" y="{y2 + 17}" text-anchor="middle">size of AB</text>'
svg("size-match.svg", "The inner dimensions of A and B must match; the outer dimensions give the size of AB",
    W, H, body, [])

# ---------- 觀念 6:字母 N 的資料矩陣與兩次變換(課本 2.7 Examples 1–3)----------
D = [(0, 0), (0.5, 0), (0.5, 6.42), (6, 0), (6, 8), (5.5, 8), (5.5, 1.58), (0, 8)]
OUTLINE = [D[0], D[1], D[2], D[3], D[4], D[5], D[6], D[7]]
SHEAR = ((1, 0.25), (0, 1))
SCALE = ((0.75, 0), (0, 1))


def letter(M, mid):
    p = Plot(-0.6, 8.4, -0.6, 8.8, s=17, pad=12, mid=mid)
    p.poly([apply(M, q) for q in OUTLINE], cls="hl", opacity=0.5)
    p.polyline([apply(M, q) for q in OUTLINE] + [apply(M, OUTLINE[0])], cls="l1")
    return p


strip("letter-n.svg",
      "The letter N drawn from its eight vertices, then sheared, then sheared and narrowed",
      [letter(((1, 0), (0, 1)), "ah-n1"), letter(SHEAR, "ah-n2"), letter(matmul(SCALE, SHEAR), "ah-n3")],
      ["D (the data matrix)", "AD (shear by .25)", "(SA)D (shear, then narrow)"])

# ---------- 觀念 6:齊次座標 = 把平面搬到 z = 1 ----------
W, H = 560, 250


def para(cx, cy, w=170, h=54, skew=44, cls="hl", op=0.35):
    pts = [(cx - w / 2 + skew, cy - h / 2), (cx + w / 2 + skew, cy - h / 2),
           (cx + w / 2 - skew, cy + h / 2), (cx - w / 2 - skew, cy + h / 2)]
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon class="{cls}" points="{s}" style="opacity:{op}"/>'


body = para(180, 190) + para(180, 80, cls="l2", op=0.28)
body += '<circle class="pt" cx="164" cy="192" r="4"/>'
body += '<circle class="pt" cx="164" cy="82" r="4"/>'
body += '<line class="ax" x1="164" y1="192" x2="164" y2="82" stroke-dasharray="5 4"/>'
body += '<text class="t" x="156" y="212" text-anchor="end">(x, y)</text>'
body += '<text class="t" x="156" y="76" text-anchor="end">(x, y, 1)</text>'
body += '<text x="548" y="222" text-anchor="end">the xy-plane (z = 0)</text>'
body += '<text x="548" y="42" text-anchor="end">the plane z = 1</text>'
body += '<line class="l1" x1="262" y1="188" x2="262" y2="88" marker-end="url(#ah-hom)"/>'
body += '<text class="t" x="272" y="142">one unit up</text>'
svg("homogeneous.svg",
    "Every point of the xy-plane is lifted to the plane one unit above it, so (x, y) becomes (x, y, 1)",
    W, H, body, ["ah-hom"])

# ---------- 觀念 6:合成變換的管線(課本 2.7 Example 6)----------
TRI = [(0, 2.4), (-1.2, -0.8), (1.2, -0.8)]
S3 = [[0.3, 0, 0], [0, 0.3, 0], [0, 0, 1]]
R90 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
TR = [[1, 0, -0.5], [0, 1, 2], [0, 0, 1]]
steps = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], S3, matmul(R90, S3), matmul(TR, matmul(R90, S3))]
panels = []
for i, M in enumerate(steps):
    p = Plot(-2.6, 2.6, -1.6, 2.8, s=25, pad=10, mid=f"ah-pipe{i}")
    p.axes(ticks=False, labels=False)
    p.poly([apply(M, q) for q in TRI], cls="hl", opacity=0.6)
    p.polyline([apply(M, q) for q in TRI] + [apply(M, TRI[0])], cls="l1")
    p.origin()
    panels.append(p)
strip("pipeline.svg",
      "A triangle is scaled by .3, then rotated 90 degrees about the origin, then translated by minus .5 and 2",
      panels, ["original", "scale by .3", "rotate 90°", "translate (−.5, 2)"])

# ---------- 觀念 6:透視投影的相似三角形(改畫課本 2.7 Figure 6(b))----------
p = Plot(-2.8, 12.6, -0.9, 5.2, s=42, pad=20, mid="ah-persp")
p.line((0, -0.7), (0, 5), cls="ax")
p.line((-0.8, 0), (11, 0), cls="ax")
p.label((0, 5), "screen (z = 0)", dx=10, dy=2)
p.label((11, 0), "z", dx=-2, dy=18, anchor="end")
p.line((10, 0), (0, 4), cls="l1")
p.dot((10, 0)); p.label((10, 0), "eye (0, 0, d)", dx=10, dy=-8)
p.dot((4, 2.4)); p.label((4, 2.4), "(x, y, z)", dx=10, dy=-8)
p.dot((0, 4)); p.label((0, 4), "(x*, y*, 0)", dx=-8, dy=4, anchor="end")
p.line((4, 0), (4, 2.4), cls="ax", extra=' stroke-dasharray="4 4"')
p.line((0, 2.4), (4, 2.4), cls="ax", extra=' stroke-dasharray="4 4"')
p.label((2, 2.4), "x", dx=0, dy=-8, anchor="middle")
p.label((0, 2), "x*", dx=-8, dy=4, anchor="end")
p.line((4, -0.5), (10, -0.5), cls="l2")
p.label((7, -0.5), "d − z", dx=0, dy=17, anchor="middle")
single("perspective.svg",
       "A ray from the eye through the point meets the screen; similar triangles give x-star equals d times x over d minus z",
       p)

# ---------- 補充觀念:圖的鄰接矩陣 ----------
NODES = {1: (0.0, 2.0), 2: (2.2, 2.0), 3: (0.0, 0.0), 4: (2.2, 0.0)}
EDGES = [(1, 2), (1, 3), (2, 3), (3, 4)]
p = Plot(-0.6, 2.8, -0.6, 2.6, s=58, pad=18, mid="ah-graph")
for a_, b_ in EDGES:
    p.line(NODES[a_], NODES[b_], cls="l1")
for n, q in NODES.items():
    x, y = p.P(*q)
    p.raw(f'<circle cx="{x}" cy="{y}" r="15" class="hl" style="opacity:0.85"/>')
    p.raw(f'<circle cx="{x}" cy="{y}" r="15" class="ax" style="fill:none"/>')
    p.raw(f'<text class="m" x="{x}" y="{y + 5}" text-anchor="middle">{n}</text>')
single("graph-adj.svg",
       "A network with four nodes: 1 joins 2 and 3, 2 joins 3, and 3 joins 4",
       p, caption="A small network (Nodes 1–4)")

print("wrote:", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith(".svg"))))
