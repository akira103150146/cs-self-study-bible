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
    return (f'<defs><marker id="{mid_id}" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" '
            f'markerHeight="9" orient="auto"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>')


def node(x, y, name, dx, dy):
    return (f'<circle class="pt" cx="{x}" cy="{y}" r="5"/>'
            f'<text class="t" x="{x + dx}" y="{y + dy}">{name}</text>')


def label(x, y, s, cls="m"):
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
print("ok")
