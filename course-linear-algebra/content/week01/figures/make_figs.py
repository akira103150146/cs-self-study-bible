# 用法:python make_figs.py(在任何目錄執行皆可)
# 產生 W1 觀念 6 的三張圖(網路流 × 2、熱傳導板)。每條分支在中點畫箭頭,方向 = 流向。
import os

OUT = os.path.dirname(os.path.abspath(__file__))   # 就是這個 figures/ 資料夾


def arrow_branch(x1, y1, x2, y2, mid_id):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    # 前半段帶箭頭(箭頭落在中點),後半段不帶
    return (f'<line class="l1" x1="{x1}" y1="{y1}" x2="{mx:.1f}" y2="{my:.1f}" marker-end="url(#{mid_id})"/>'
            f'<line class="l1" x1="{mx:.1f}" y1="{my:.1f}" x2="{x2}" y2="{y2}"/>')


def marker(mid_id):
    # userSpaceOnUse:箭頭固定 12 單位,不跟線寬(2.4)放大,否則會壓到旁邊的 x1、x3 標籤
    return (f'<defs><marker id="{mid_id}" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" '
            f'markerWidth="12" markerHeight="12" orient="auto"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>')


def node(x, y, name, dx, dy):
    return (f'<circle class="pt" cx="{x}" cy="{y}" r="5"/>'
            f'<text class="t" x="{x + dx}" y="{y + dy}">{name}</text>')


def label(x, y, s, cls="m"):
    # 流量變數 x1…x6 畫成斜體 x 加下標,和題幹的 $x_1$ 一致;數字與溫度照原樣
    if len(s) == 2 and s[0] == "x" and s[1].isdigit():
        s = f'<tspan style="font-family: var(--font-serif); font-style: italic">x</tspan><tspan dy="4" font-size="11">{s[1]}</tspan>'
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="middle">{s}</text>'


# ---------- Baltimore(Lay 1.6 Example 2)----------
B, C, A, D = (180, 90), (380, 90), (180, 200), (380, 200)
parts = [marker("ah-balt")]
branches = [
    ((540, 90), C, "400", (520, 80)),          # Lombard 由東流入 C
    (C, B, "x4", (280, 80)),                   # C → B
    (B, (20, 90), "300", (40, 80)),            # B → 西邊流出
    ((20, 200), A, "300", (40, 190)),          # Pratt 由西流入 A
    (A, D, "x1", (280, 222)),                  # A → D
    (D, (540, 200), "600", (520, 190)),        # D → 東邊流出
    ((180, 290), A, "500", (205, 285)),        # Calvert 由南流入 A
    (A, B, "x2", (158, 150)),                  # A → B
    (B, (180, 12), "x3", (200, 24)),           # B → 北邊流出
    ((380, 12), C, "100", (402, 24)),          # South 由北流入 C
    (C, D, "x5", (402, 150)),                  # C → D
]
for (p, q, lab, (lx, ly)) in branches:
    parts.append(arrow_branch(*p, *q, "ah-balt"))
    parts.append(label(lx, ly, lab))
parts += [node(*A, "A", -22, 20), node(*B, "B", -22, -8), node(*C, "C", 10, -8), node(*D, "D", 10, 20)]
parts += ['<text x="60" y="108">Lombard St.</text>', '<text x="60" y="218">Pratt St.</text>',
          '<text x="172" y="262" text-anchor="end">Calvert St.</text>', '<text x="392" y="262">South St.</text>']
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 300" width="560" role="img" '
       'aria-label="Traffic flow in downtown Baltimore: four intersections A, B, C, D">'
       + "".join(parts) + "</svg>\n")
open(os.path.join(OUT, "baltimore.svg"), "w", encoding="utf-8").write(svg)

# ---------- Lay 1.6 Exercise 11 ----------
A, C, B = (140, 50), (140, 170), (260, 110)
parts = [marker("ah-net11")]
branches = [
    (A, (30, 50), "20", (50, 42)),             # A → 西邊流出 20
    ((30, 170), C, "80", (50, 162)),           # 80 由西流入 C
    (C, A, "x1", (122, 115)),                  # C → A
    (B, A, "x3", (205, 70)),                   # B → A
    (C, B, "x2", (205, 160)),                  # C → B
    (B, (360, 110), "x4", (330, 102)),         # B → 東邊流出
]
for (p, q, lab, (lx, ly)) in branches:
    parts.append(arrow_branch(*p, *q, "ah-net11"))
    parts.append(label(lx, ly, lab))
parts += [node(*A, "A", -6, -12), node(*C, "C", -6, 26), node(*B, "B", 0, -12)]
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" width="380" role="img" '
       'aria-label="Network for Lay 1.6 Exercise 11 with junctions A, B, C">'
       + "".join(parts) + "</svg>\n")
open(os.path.join(OUT, "network-ex11.svg"), "w", encoding="utf-8").write(svg)

# ---------- 熱傳導板(Lay 1.1 Exercises 43–44)----------
n1, n2, n3, n4 = (200, 80), (280, 80), (280, 160), (200, 160)
parts = ['<rect class="box" x="160" y="40" width="160" height="160"/>']
for x in (200, 280):
    parts.append(f'<line class="ax" x1="{x}" y1="40" x2="{x}" y2="200"/>')
for y in (80, 160):
    parts.append(f'<line class="ax" x1="160" y1="{y}" x2="320" y2="{y}"/>')
for (x, y), name in ((n1, "1"), (n2, "2"), (n3, "3"), (n4, "4")):
    parts.append(f'<rect class="hl" x="{x - 13}" y="{y - 13}" width="26" height="26" rx="5"/>')
    parts.append(f'<text class="pv" x="{x}" y="{y + 5}" text-anchor="middle">{name}</text>')
for x in (200, 280):
    parts.append(label(x, 30, "20°", "t"))
    parts.append(label(x, 220, "30°", "t"))
for y in (80, 160):
    parts.append(f'<text class="t" x="150" y="{y + 5}" text-anchor="end">10°</text>')
    parts.append(f'<text class="t" x="330" y="{y + 5}">40°</text>')
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 235" width="480" role="img" '
       'aria-label="Metal plate with four interior nodes and boundary temperatures">'
       + "".join(parts) + "</svg>\n")
open(os.path.join(OUT, "heat-plate.svg"), "w", encoding="utf-8").write(svg)


def write_network(name, w, h, aria, mid_id, nodes, branches, extra=()):
    """nodes: {名稱: (x, y, 標籤dx, 標籤dy)};branches: [(起點, 終點, 流量標籤, 標籤位置)]。"""
    pos = {k: (v[0], v[1]) for k, v in nodes.items()}
    parts = [marker(mid_id)]
    for p, q, lab, (lx, ly) in branches:
        p, q = pos.get(p, p), pos.get(q, q)
        parts.append(arrow_branch(*p, *q, mid_id))
        parts.append(label(lx, ly, lab))
    parts += list(extra)
    parts += [node(x, y, k, dx, dy) for k, (x, y, dx, dy) in nodes.items()]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" role="img" '
           f'aria-label="{aria}">' + "".join(parts) + "</svg>\n")
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg)


# ---------- Lay 1.6 Exercise 12(高速公路網,cars/minute)----------
write_network(
    "network-ex12.svg", 500, 270, "Freeway network for Lay 1.6 Exercise 12", "ah-net12",
    {"A": (120, 140, -20, -8), "B": (200, 60, 10, -6), "C": (400, 140, 6, -10), "D": (260, 200, 8, 22)},
    [((200, 8), "B", "200", (218, 22)),       # 200 由上方流入 B
     ("A", (30, 140), "40", (52, 132)),       # A → 西邊流出 40
     ("C", (480, 140), "100", (458, 132)),    # C → 東邊流出 100
     ("D", (260, 262), "60", (276, 252)),     # D → 南邊流出 60
     ("B", "A", "x1", (146, 94)),             # B → A
     ("B", "C", "x2", (312, 88)),             # B → C
     ("A", "C", "x3", (262, 132)),            # A → C
     ("A", "D", "x4", (176, 186)),            # A → D
     ("C", "D", "x5", (344, 186))])           # C → D

# ---------- Lay 1.6 Exercise 13 ----------
write_network(
    "network-ex13.svg", 460, 230, "Network for Lay 1.6 Exercise 13 with junctions A to E", "ah-net13",
    {"A": (120, 80, -20, -8), "E": (120, 150, -20, 22), "B": (230, 115, -5, -12),
     "C": (340, 80, 8, -10), "D": (340, 150, 8, 22)},
    [((120, 12), "A", "30", (136, 24)),       # 30 由上方流入 A
     ("A", (20, 80), "80", (42, 72)),         # A → 西邊流出 80
     ((20, 150), "E", "60", (42, 142)),       # 60 由西流入 E
     ("E", (120, 218), "20", (136, 210)),     # E → 南邊流出 20
     ("C", (340, 12), "40", (356, 24)),       # C → 北邊流出 40
     ((440, 80), "C", "100", (418, 72)),      # 100 由東流入 C
     ("D", (440, 150), "90", (418, 142)),     # D → 東邊流出 90
     ((340, 218), "D", "40", (356, 210)),     # 40 由南流入 D
     ("A", "E", "x1", (104, 120)),            # A → E
     ("B", "A", "x2", (176, 84)),             # B → A
     ("E", "B", "x3", (176, 150)),            # E → B
     ("B", "D", "x4", (286, 150)),            # B → D
     ("C", "B", "x5", (286, 84)),             # C → B
     ("D", "C", "x6", (356, 120))])           # D → C

# ---------- Lay 1.6 Exercise 14(環形交叉路口,順時針行駛)----------
import math

cx, cy, r = 240, 150, 90


def on_circle(deg):
    t = math.radians(deg)
    return (round(cx + r * math.cos(t), 1), round(cy - r * math.sin(t), 1))


angle = {"A": 200, "B": 160, "C": 105, "D": 75, "E": 20, "F": -20}
P = {k: on_circle(a) for k, a in angle.items()}
arcs = []
for a, b, lab, (lx, ly) in [("F", "A", "x1", (240, 262)), ("A", "B", "x2", (132, 154)),
                            ("B", "C", "x3", (162, 84)), ("C", "D", "x4", (240, 84)),
                            ("D", "E", "x5", (312, 80)), ("E", "F", "x6", (350, 154))]:
    a0, a1 = angle[a], angle[b]
    if a1 > a0:                               # 順時針(螢幕上)= 數學角度遞減
        a1 -= 360
    mid = on_circle((a0 + a1) / 2)
    # SVG 弧線 sweep-flag=1 是螢幕上的順時針;前半段帶箭頭,後半段不帶
    arcs.append(f'<path class="l1" d="M{P[a][0]},{P[a][1]} A{r},{r} 0 0 1 {mid[0]},{mid[1]}" '
                f'marker-end="url(#ah-net14)"/>')
    arcs.append(f'<path class="l1" d="M{mid[0]},{mid[1]} A{r},{r} 0 0 1 {P[b][0]},{P[b][1]}"/>')
    arcs.append(label(lx, ly, lab))
write_network(
    "roundabout-ex14.svg", 480, 280, "Roundabout for Lay 1.6 Exercise 14", "ah-net14",
    {"A": (*P["A"], -20, 14), "B": (*P["B"], -20, -6), "C": (*P["C"], -20, -4),
     "D": (*P["D"], 8, -4), "E": (*P["E"], 8, -6), "F": (*P["F"], 8, 16)},
    [("A", (50, P["A"][1]), "100", (72, P["A"][1] - 8)),     # A → 西邊流出 100
     ((50, P["B"][1]), "B", "50", (72, P["B"][1] - 8)),      # 50 由西流入 B
     ("C", (P["C"][0], 12), "120", (P["C"][0] - 20, 24)),    # C → 北邊流出 120
     ((P["D"][0], 12), "D", "150", (P["D"][0] + 22, 24)),    # 150 由北流入 D
     ("E", (430, P["E"][1]), "80", (410, P["E"][1] - 8)),    # E → 東邊流出 80
     ((430, P["F"][1]), "F", "100", (408, P["F"][1] - 8))],  # 100 由東流入 F
    extra=arcs)
print("ok")
