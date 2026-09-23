# 用法:python make_circuits.py
# 產生 W4 觀念 6(Lay 1.10)的電路圖、遷移圖與鋼板圖。畫圖工具在 circuits.py。
from circuits import Circuit


def II(k):
    """迴路電流的標籤:斜體 I 加下標。"""
    return (f'<tspan style="font-family: var(--font-serif); font-style: italic">I</tspan>'
            f'<tspan dy="4" font-size="10">{k}</tspan><tspan dy="-4">​</tspan>')


# ---------- 課本 Figure 1(Lay 1.10 Example 2)----------
L, R = 70, 260
ys = [40, 115, 190, 265]
c = Circuit(340, 305, mid="ah-c1")
c.battery((L, ys[0]), (R, ys[0]), "30 volts", plus="start", side=1, dist=20)
c.resistor((L, ys[0]), (L, ys[1]), "4 Ω", side=-1, dist=18)
c.resistor((R, ys[0]), (R, ys[1]), "4 Ω", side=1, dist=18)
c.resistor((L, ys[1]), (R, ys[1]), "3 Ω", side=-1, dist=14)
c.resistor((L, ys[1]), (L, ys[2]), "1 Ω", side=-1, dist=18)
c.resistor((R, ys[1]), (R, ys[2]), "1 Ω", side=1, dist=18)
M = ((L + R) / 2, ys[2])
c.battery((L, ys[2]), M, "5 volts", plus="end", side=1, dist=20)
c.resistor(M, (R, ys[2]), "1 Ω", side=-1, dist=14)
c.resistor((L, ys[2]), (L, ys[3]), "1 Ω", side=-1, dist=18)
c.resistor((R, ys[2]), (R, ys[3]), "1 Ω", side=1, dist=18)
c.battery((L, ys[3]), (R, ys[3]), "20 volts", plus="start", side=1, dist=22)
for i in range(3):
    c.loop(((L + R) / 2, (ys[i] + ys[i + 1]) / 2), 20, II(i + 1))
c.node((L, ys[1]), "A", dx=-16, dy=4)
c.node((R, ys[1]), "B", dx=16, dy=4)
c.node((L, ys[2]), "C", dx=-16, dy=4)
c.node((R, ys[2]), "D", dx=16, dy=4)
c.svg("circuit-fig1.svg", "The network of Example 2: three stacked loops with 30, 5 and 20 volt batteries")

# ---------- Exercise 5:四個堆疊迴路 ----------
L, R = 80, 250
ys = [35, 110, 185, 260, 335]
Mx = (L + R) / 2
c = Circuit(330, 380, mid="ah-c5")
c.battery((L, ys[0]), (Mx, ys[0]), "20 V", plus="start", side=-1, dist=16)
c.resistor((Mx, ys[0]), (R, ys[0]), "1 Ω", side=-1, dist=14)
for i, (lft, rgt) in enumerate([("1 Ω", "4 Ω"), ("3 Ω", "1 Ω"), ("4 Ω", "2 Ω"), ("1 Ω", "3 Ω")]):
    c.resistor((L, ys[i]), (L, ys[i + 1]), lft, side=-1, dist=18)
    c.resistor((R, ys[i]), (R, ys[i + 1]), rgt, side=1, dist=18)
    c.loop((Mx, (ys[i] + ys[i + 1]) / 2), 20, II(i + 1))
mids = [(("R", "5 Ω"), ("B", "30 V", "end")),
        (("B", "10 V", "start"), ("R", "1 Ω")),
        (("R", "2 Ω"), ("B", "20 V", "end"))]
for i, (left_el, right_el) in enumerate(mids, start=1):
    y = ys[i]
    for (x0, x1), el in (((L, Mx), left_el), ((Mx, R), right_el)):
        a, b = (x0, y), (x1, y)
        if el[0] == "R":
            c.resistor(a, b, el[1], side=-1, dist=14)
        else:
            c.battery(a, b, el[1], plus=el[2], side=-1, dist=16)
c.battery((L, ys[4]), (Mx, ys[4]), "10 V", plus="start", side=1, dist=18)
c.resistor((Mx, ys[4]), (R, ys[4]), "4 Ω", side=1, dist=16)
c.svg("circuit-ex5.svg", "Exercise 5: four stacked loops, each branch carrying a battery or a resistor")

# ---------- Exercise 6:四個堆疊迴路,電池都在左側 ----------
L, R = 95, 250
ys = [35, 110, 185, 260, 335]
Mx = (L + R) / 2
c = Circuit(330, 380, mid="ah-c6")
c.resistor((L, ys[0]), (R, ys[0]), "3 Ω", side=-1, dist=14)
for i, (bat, rgt) in enumerate([("30 V", "2 Ω"), ("20 V", "4 Ω"), ("40 V", "1 Ω"), ("10 V", "2 Ω")]):
    c.battery((L, ys[i]), (L, ys[i + 1]), bat, plus="end", side=-1, dist=24)
    c.resistor((R, ys[i]), (R, ys[i + 1]), rgt, side=1, dist=18)
    c.loop((Mx, (ys[i] + ys[i + 1]) / 2), 20, II(i + 1))
for i, lab in enumerate(["1 Ω", "4 Ω", "2 Ω"], start=1):
    c.resistor((L, ys[i]), (R, ys[i]), lab, side=-1, dist=14)
c.resistor((L, ys[4]), (R, ys[4]), "3 Ω", side=1, dist=16)
c.svg("circuit-ex6.svg", "Exercise 6: four stacked loops with all four batteries on the left side")

# ---------- Exercise 7:2 × 2 的迴路 ----------
xs, ys = [70, 215, 360], [45, 165, 285]
c = Circuit(430, 330, mid="ah-c7")
c.battery((xs[0], ys[0]), (xs[1], ys[0]), "40 V", plus="start", side=-1, dist=18)
c.resistor((xs[1], ys[0]), (xs[2], ys[0]), "4 Ω", side=-1, dist=16)
c.resistor((xs[0], ys[0]), (xs[0], ys[1]), "1 Ω", side=-1, dist=20)
c.resistor((xs[1], ys[0]), (xs[1], ys[1]), "4 Ω", side=-1, dist=16)
c.battery((xs[2], ys[0]), (xs[2], ys[1]), "10 V", plus="end", side=-1, dist=24)
c.resistor((xs[0], ys[1]), (xs[1], ys[1]), "7 Ω", side=1, dist=16)
c.resistor((xs[1], ys[1]), (xs[2], ys[1]), "5 Ω", side=1, dist=16)
c.battery((xs[0], ys[1]), (xs[0], ys[2]), "30 V", plus="end", side=-1, dist=26)
c.resistor((xs[1], ys[1]), (xs[1], ys[2]), "6 Ω", side=-1, dist=16)
c.resistor((xs[2], ys[1]), (xs[2], ys[2]), "3 Ω", side=1, dist=18)
c.resistor((xs[0], ys[2]), (xs[1], ys[2]), "2 Ω", side=1, dist=18)
c.battery((xs[1], ys[2]), (xs[2], ys[2]), "20 V", plus="end", side=1, dist=20)
c.loop(((xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2), 24, II(1))
c.loop(((xs[1] + xs[2]) / 2, (ys[0] + ys[1]) / 2), 24, II(4))
c.loop(((xs[0] + xs[1]) / 2, (ys[1] + ys[2]) / 2), 24, II(2))
c.loop(((xs[1] + xs[2]) / 2, (ys[1] + ys[2]) / 2), 24, II(3))
c.svg("circuit-ex7.svg", "Exercise 7: a two by two grid of four loops")

# ---------- Exercise 8:正方形中間再放一個菱形,共五個迴路 ----------
c = Circuit(430, 410, mid="ah-c8")
TL, TR, BL, BR = (65, 50), (365, 50), (65, 360), (365, 360)
TM, BM, LM, RM = (215, 50), (215, 360), (65, 205), (365, 205)
DT, DB, DL, DR = (215, 135), (215, 275), (145, 205), (285, 205)
c.battery(TL, TM, "50 V", plus="start", side=-1, dist=16)
c.battery(TM, TR, "40 V", plus="end", side=-1, dist=16)
c.resistor(TL, LM, "3 Ω", side=-1, dist=18)
c.resistor(LM, BL, "1 Ω", side=-1, dist=18)
c.resistor(TR, RM, "1 Ω", side=1, dist=18)
c.resistor(RM, BR, "2 Ω", side=1, dist=18)
c.battery(BL, BM, "30 V", plus="start", side=1, dist=18)
c.battery(BM, BR, "20 V", plus="end", side=1, dist=18)
c.resistor(TM, DT, "1 Ω", side=1, dist=16)
c.resistor(LM, DL, "1 Ω", side=-1, dist=14)
c.resistor(DR, RM, "3 Ω", side=-1, dist=14)
c.resistor(DB, BM, "2 Ω", side=1, dist=16)
c.resistor(DL, DT, "4 Ω", side=1, dist=14)
c.resistor(DT, DR, "2 Ω", side=-1, dist=14)
c.resistor(DL, DB, "3 Ω", side=-1, dist=14)
c.resistor(DB, DR, "3 Ω", side=1, dist=14)
c.loop((138, 115), 22, II(1))
c.loop((138, 300), 22, II(2))
c.loop((292, 300), 22, II(3))
c.loop((292, 115), 22, II(4))
c.loop((215, 205), 20, II(5))
c.svg("circuit-ex8.svg", "Exercise 8: a square with a diamond inside it, giving five loops")

# ---------- 課本 Figure 2:城市與郊區的年遷移比例 ----------
c = Circuit(440, 195, mid="ah-mig")
for (x, lab) in ((105, "City"), (315, "Suburbs")):
    c.p.append(f'<rect class="hl" x="{x - 55}" y="62" width="110" height="60" rx="8" style="opacity:.55"/>')
    c.p.append(f'<text class="t" x="{x}" y="98" text-anchor="middle">{lab}</text>')
c.p.append('<path d="M163,77 C215,57 215,57 257,77" style="fill:none;stroke:currentColor;stroke-width:1.6" '
           'marker-end="url(#ah-mig)"/>')
c.p.append('<text class="m" x="210" y="52" text-anchor="middle">.05</text>')
c.p.append('<path d="M257,110 C215,130 215,130 163,110" style="fill:none;stroke:currentColor;stroke-width:1.6" '
           'marker-end="url(#ah-mig)"/>')
c.p.append('<text class="m" x="210" y="152" text-anchor="middle">.03</text>')
c.p.append('<path d="M48,77 C10,92 10,97 48,110" style="fill:none;stroke:currentColor;stroke-width:1.6" '
           'marker-end="url(#ah-mig)"/>')
c.p.append('<text class="m" x="22" y="44" text-anchor="middle">.95</text>')
c.p.append('<path d="M372,110 C412,97 412,92 372,77" style="fill:none;stroke:currentColor;stroke-width:1.6" '
           'marker-end="url(#ah-mig)"/>')
c.p.append('<text class="m" x="400" y="44" text-anchor="middle">.97</text>')
c.svg("migration.svg", "Annual percentage migration between city and suburbs: .05 leaves the city, .03 leaves the suburbs")

# ---------- Exercise 14:兩塊鋼板的邊界溫度 ----------
c = Circuit(580, 260, mid="ah-plate")


def plate(x0, y0, s, top, left, right, bottom, tag):
    for i in range(4):
        c.p.append(f'<line x1="{x0}" y1="{y0 + i * s}" x2="{x0 + 3 * s}" y2="{y0 + i * s}" '
                   f'style="stroke:currentColor;stroke-width:1;opacity:.6"/>')
        c.p.append(f'<line x1="{x0 + i * s}" y1="{y0}" x2="{x0 + i * s}" y2="{y0 + 3 * s}" '
                   f'style="stroke:currentColor;stroke-width:1;opacity:.6"/>')
    pts = {1: (x0 + s, y0 + s), 2: (x0 + 2 * s, y0 + s), 3: (x0 + 2 * s, y0 + 2 * s), 4: (x0 + s, y0 + 2 * s)}
    for k, (px, py) in pts.items():
        c.p.append(f'<circle cx="{px}" cy="{py}" r="4" style="fill:currentColor"/>')
        c.p.append(f'<text class="m" x="{px + 12}" y="{py - 8}" text-anchor="middle">{k}</text>')
    labels = [(x0 + s, y0 - 10, top[0]), (x0 + 2 * s, y0 - 10, top[1]),
              (x0 - 18, y0 + s + 4, left[0]), (x0 - 18, y0 + 2 * s + 4, left[1]),
              (x0 + 3 * s + 18, y0 + s + 4, right[0]), (x0 + 3 * s + 18, y0 + 2 * s + 4, right[1]),
              (x0 + s, y0 + 3 * s + 18, bottom[0]), (x0 + 2 * s, y0 + 3 * s + 18, bottom[1])]
    for px, py, t in labels:
        c.p.append(f'<text class="m" x="{px}" y="{py}" text-anchor="middle">{t}</text>')
    c.p.append(f'<text class="t" x="{x0 + 1.5 * s}" y="{y0 + 3 * s + 44}" text-anchor="middle">{tag}</text>')


plate(80, 55, 45, ["20°", "20°"], ["0°", "0°"], ["0°", "0°"], ["20°", "20°"], "(a)")
plate(385, 55, 45, ["0°", "0°"], ["10°", "10°"], ["40°", "40°"], ["10°", "10°"], "(b)")
c.svg("plates-ex14.svg", "Exercise 14: two steel plates, each with four interior points and eight boundary temperatures")

print("ok")
