# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W7(Lay 2.8、2.9)的圖。座標一律用數學座標(y 向上),由 Plot 換算成 SVG 像素。
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
    extra = 26 if caption else 0
    body = p.body()
    if caption:
        # 圖說底下先鋪一塊底色:格線(虛線)會畫出圖框,不鋪的話字會被線穿過
        body += (f'<rect x="0" y="{p.h}" width="{p.w}" height="26" '
                 f'style="fill:var(--bg);stroke:none"/>')
        body += f'<text x="{p.w / 2}" y="{p.h + 16}" text-anchor="middle">{caption}</text>'
    svg(name, aria, p.w, p.h + extra, body, [p.mid])


def strip(name, aria, panels, captions, gap=18):
    w = sum(p.w for p in panels) + gap * (len(panels) - 1)
    h = max(p.h for p in panels) + 26
    body, x = "", 0
    for p, cap in zip(panels, captions):
        body += p.body(x, 0)
        body += f'<text x="{x + p.w / 2}" y="{h - 6}" text-anchor="middle">{cap}</text>'
        x += p.w + gap
    svg(name, aria, w, h, body, [p.mid for p in panels])


# ---------- 觀念 1:Lay 2.8 Exercises 1–4 的四個區域 ----------
R = 3.4
panels = []

# (1) 第一象限
p = Plot(-R, R, -R, R, s=26, pad=17, mid="ah-s1")
p.poly([(0, 0), (R, 0), (R, R), (0, R)], cls="hl", opacity=0.55)
p.axes(ticks=False, labels=False)
p.dot((1, 1), r=3.5); p.label((1, 1), "u", dx=7, dy=-4)
p.dot((-1, -1), r=3.5); p.label((-1, -1), "(−1)u", dx=7, dy=14)
panels.append(p)

# (2) 第一與第三象限
p = Plot(-R, R, -R, R, s=26, pad=17, mid="ah-s2")
p.poly([(0, 0), (R, 0), (R, R), (0, R)], cls="hl", opacity=0.55)
p.poly([(0, 0), (-R, 0), (-R, -R), (0, -R)], cls="hl", opacity=0.55)
p.axes(ticks=False, labels=False)
p.dot((1, 3), r=3.5); p.label((1, 3), "u", dx=7, dy=2)
p.dot((-3, -1), r=3.5); p.label((-3, -1), "v", dx=-6, dy=14, anchor="end")
p.dot((-2, 2), r=3.5); p.label((-2, 2), "u + v", dx=7, dy=-6)
panels.append(p)

# (3) 沿 x2 = x1 的帶狀區
p = Plot(-R, R, -R, R, s=26, pad=17, mid="ah-s3")
d = 1.0
p.poly([(-R, -R + d), (R, R + d), (R, R - d), (-R, -R - d)], cls="hl", opacity=0.55)
p.line((-R, -R), (R, R), cls="ax", extra=' stroke-dasharray="4 4"')
p.axes(ticks=False, labels=False)
p.dot((0, 1), r=3.5); p.label((0, 1), "u", dx=-6, dy=-6, anchor="end")
p.dot((0, 2), r=3.5); p.label((0, 2), "2u", dx=7, dy=0)
panels.append(p)

# (4) 過原點、斜率為負的直線上方的半平面
p = Plot(-R, R, -R, R, s=26, pad=17, mid="ah-s4")
m = 1.0
p.poly([(-R, R), (R, R), (R, -m * R), (-R, m * R)], cls="hl", opacity=0.55)
p.line((-R, m * R), (R, -m * R), cls="ax")
p.axes(ticks=False, labels=False)
p.dot((0, 1), r=3.5); p.label((0, 1), "u", dx=7, dy=-2)
p.dot((0, -1), r=3.5); p.label((0, -1), "(−1)u", dx=7, dy=12)
panels.append(p)

strip("subspace-tests.svg",
      "Four shaded regions of the plane: the first quadrant, the union of the first and third quadrants, "
      "a band along the line x2 = x1, and a half plane above a line through the origin",
      panels, ["(1) 第一象限", "(2) 第一 + 第三象限", "(3) 沿 x₂ = x₁ 的帶狀區", "(4) 直線上方的半平面"])

# ---------- 觀念 2:Col A 與 Nul A 住在不同的空間 ----------
W, H = 540, 210


def plane(cx, cy, w=170, h=54, skew=40, cls="hl", op=0.4):
    pts = [(cx - w / 2 + skew, cy - h / 2), (cx + w / 2 + skew, cy - h / 2),
           (cx + w / 2 - skew, cy + h / 2), (cx - w / 2 - skew, cy + h / 2)]
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon class="{cls}" points="{s}" style="opacity:{op}"/>'


body = plane(140, 120) + plane(400, 120)
body += '<text x="140" y="60" text-anchor="middle">ℝⁿ(輸入)</text>'
body += '<text x="400" y="60" text-anchor="middle">ℝᵐ(輸出)</text>'
body += ('<line class="l1" x1="212" y1="112" x2="330" y2="112" marker-end="url(#ah-cn)"/>'
         '<text x="271" y="102" text-anchor="middle">乘 A</text>')
body += '<circle class="pt" cx="120" cy="126" r="4"/><text class="t" x="112" y="130" text-anchor="end">Nul A</text>'
body += '<circle class="pt" cx="420" cy="126" r="4"/><text class="t" x="430" y="130">Col A</text>'
body += '<text x="140" y="176" text-anchor="middle">被壓成 0 的那些 x</text>'
body += '<text x="400" y="176" text-anchor="middle">到得了的那些 b</text>'
svg("col-nul.svg",
    "Nul A lives in R to the n on the input side; Col A lives in R to the m on the output side",
    W, H, body, ["ah-cn"])


# ---------- 觀念 4:B 座標的格線 ----------
def coord_grid(name, b1, b2, pts, rng, aria, caption, s=30, k=4):
    lo = min(rng[0], rng[2])
    p = Plot(rng[0], rng[1], rng[2], rng[3], s=s, pad=18, mid="ah-" + name)
    for i in range(-k, k + 1):
        a = (b1[0] * i - b2[0] * k, b1[1] * i - b2[1] * k)
        b = (b1[0] * i + b2[0] * k, b1[1] * i + b2[1] * k)
        p.line(a, b, cls="ax", extra=' stroke-dasharray="3 4" style="opacity:0.6"')
        a = (b2[0] * i - b1[0] * k, b2[1] * i - b1[1] * k)
        b = (b2[0] * i + b1[0] * k, b2[1] * i + b1[1] * k)
        p.line(a, b, cls="ax", extra=' stroke-dasharray="3 4" style="opacity:0.6"')
    p.axes(ticks=True, labels=True)
    p.arrow(b1, cls="l1"); p.label(b1, "b1", dx=8, dy=10)
    p.arrow(b2, cls="l1"); p.label(b2, "b2", dx=8, dy=-6)
    for q, lab in pts:
        p.dot(q); p.label(q, lab, dx=9, dy=-8)
    single(name, aria, p, caption=caption)


coord_grid("coord-pp2.svg", (1, 0.2), (0.2, 1), [((3.4, 2.6), "x"), ((-0.6, 1.8), "y")], (-1.5, 4.5, -1.5, 4.5),
           "A coordinate grid drawn from the basis vectors b1 and b2, with x at 3 units along b1 and 2 along b2",
           "課本 2.9 Practice Problem 2 的格線")

coord_grid("coord-ex7.svg", (3, 0), (-1, 2), [((7, -2), "w"), ((4, 1), "x")], (-3.5, 8.5, -3.5, 4.5),
           "A coordinate grid for the basis with b1 equal to three zero and b2 equal to minus one two, "
           "showing the points w and x",
           "Lay 2.9 Exercise 7 的格線")

coord_grid("coord-ex8.svg", (0, 2), (2, 1), [((-2, 3), "x"), ((2, 4), "y"), ((-1, -2.5), "z")],
           (-4.5, 4.5, -4.5, 5.5),
           "A coordinate grid for the basis with b1 equal to zero two and b2 equal to two one, "
           "showing the points x, y and z",
           "Lay 2.9 Exercise 8 的格線")

# ---------- 觀念 5:Rank Theorem 的長條圖 ----------
W, H = 520, 150
body = ""
x0, y0, cw, ch = 40, 46, 48, 44
for j in range(8):
    fill = "hl" if j < 5 else "l2"
    op = 0.75 if j < 5 else 0.3
    body += (f'<rect x="{x0 + j * cw}" y="{y0}" width="{cw}" height="{ch}" class="{fill}" '
             f'style="opacity:{op}"/>')
    body += (f'<rect x="{x0 + j * cw}" y="{y0}" width="{cw}" height="{ch}" class="ax" style="fill:none"/>')
    body += (f'<text class="m" x="{x0 + j * cw + cw / 2}" y="{y0 + ch / 2 + 5}" text-anchor="middle">'
             f'{"■" if j < 5 else "·"}</text>')
body += f'<text x="{x0 + 8 * cw / 2}" y="{y0 - 16}" text-anchor="middle">A 的 n 行</text>'
body += (f'<path class="l1" d="M{x0},{y0 + ch + 10} L{x0},{y0 + ch + 18} L{x0 + 5 * cw},{y0 + ch + 18} '
         f'L{x0 + 5 * cw},{y0 + ch + 10}" style="fill:none"/>')
body += f'<text class="t" x="{x0 + 5 * cw / 2}" y="{y0 + ch + 36}" text-anchor="middle">樞軸行 → rank A</text>'
body += (f'<path class="l2" d="M{x0 + 5 * cw},{y0 + ch + 10} L{x0 + 5 * cw},{y0 + ch + 18} '
         f'L{x0 + 8 * cw},{y0 + ch + 18} L{x0 + 8 * cw},{y0 + ch + 10}" style="fill:none"/>')
body += (f'<text class="t" x="{x0 + 6.5 * cw}" y="{y0 + ch + 36}" text-anchor="middle">'
         f'自由行 → dim Nul A</text>')
svg("rank-bar.svg",
    "The n columns of A split into pivot columns, which count the rank, and free columns, "
    "which count the dimension of the null space",
    W, H, body, [])

# ---------- 補充觀念:Hamming(7,4) 的三圈圖 ----------
# 位元的位置是算過的:每個位元離「它不該碰到」的那條圈弧至少 28px(位元半徑 15),
# 所以「這個位元在哪幾個圈裡」一眼可判。校驗位元畫成方形,灰階列印時也分得出來。
W, H = 380, 342
cx, cy, r = 190, 150, 92
offs = [(0, -46), (-42, 34), (42, 34)]
body = ""
for (dx, dy) in offs:
    body += (f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{r}" class="l1" '
             f'style="fill:none;stroke-width:1.6"/>')
spots = {
    "d1": (190, 155), "d2": (129, 123), "d3": (251, 123), "d4": (190, 227),
    "p1": (190, 55), "p2": (100, 202), "p3": (280, 202),
}
for lab, (x, y) in spots.items():
    data = lab.startswith("d")
    cls = "hl" if data else "bad"
    if data:
        body += f'<circle cx="{x}" cy="{y}" r="15" class="{cls}" style="opacity:0.85"/>'
        body += f'<circle cx="{x}" cy="{y}" r="15" class="ax" style="fill:none"/>'
    else:
        body += (f'<rect x="{x - 14}" y="{y - 14}" width="28" height="28" rx="3" '
                 f'class="{cls}" style="opacity:0.85"/>')
        body += (f'<rect x="{x - 14}" y="{y - 14}" width="28" height="28" rx="3" '
                 f'class="ax" style="fill:none"/>')
    body += f'<text class="m" x="{x}" y="{y + 5}" text-anchor="middle">{sub(lab)}</text>'
body += f'<text x="{cx}" y="{H - 30}" text-anchor="middle">每一圈裡的四個位元,1 的個數必須是偶數</text>'
body += (f'<text class="t" x="{cx}" y="{H - 10}" text-anchor="middle">'
         f'圓 = 資料位元 d₁–d₄,方 = 校驗位元 p₁–p₃</text>')
svg("hamming.svg",
    "Three overlapping circles: four data bits and three parity bits arranged so that each circle "
    "contains an even number of ones",
    W, H, body, [])

print("wrote:", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith(".svg"))))
