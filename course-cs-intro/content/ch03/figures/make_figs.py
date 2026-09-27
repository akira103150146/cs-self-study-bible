"""產生第 3 章的 SVG 圖。執行:python make_figs.py(在這個資料夾裡)。

圖內用 handout.css 的 .fig 樣式(.ax .l1 .l2 .pt .box .hl .bad .stair、text.t/.m/.pv)上色,
所以深淺主題都會跟著變。標籤一律英文。
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def save(name, w, h, label, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" role="img" '
           f'aria-label="{label}">\n{body}\n</svg>\n')
    with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def path(points):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)


# ---------------------------------------------------------------- 類比 vs 數位
def analog_digital():
    parts = []
    for gx, title in ((10, "Analog: continuous"), (340, "Digital: two levels")):
        parts.append(f'<g transform="translate({gx},0)">')
        parts.append(f'<text class="t" x="150" y="18" text-anchor="middle">{title}</text>')
        parts.append('<line class="ax" x1="10" y1="160" x2="300" y2="160"/>')
        parts.append('<line class="ax" x1="10" y1="30" x2="10" y2="165"/>')
        parts.append('<text x="300" y="178" text-anchor="end">time</text>')
        parts.append("</g>")
    wave = [(20 + x, 95 - 50 * math.sin(x / 28) - 12 * math.sin(x / 9)) for x in range(0, 280, 2)]
    parts.append(f'<path class="l1" transform="translate(10,0)" d="{path(wave)}"/>')
    bits = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0]
    pts, x = [], 20
    for b in bits:
        y = 55 if b else 140
        pts += [(x, y), (x + 28, y)]
        x += 28
    parts.append(f'<path class="stair" transform="translate(340,0)" d="{path(pts)}"/>')
    parts.append('<text x="345" y="60" text-anchor="end">1</text><text x="345" y="145" text-anchor="end">0</text>')
    for i, b in enumerate(bits):
        parts.append(f'<text class="m" x="{340 + 34 + 28 * i}" y="200" text-anchor="middle">{b}</text>')
    save("analog-digital.svg", 660, 210, "An analog signal varies continuously; a digital signal has only two levels",
         "\n".join(parts))


# ---------------------------------------------------------------- 4 位元二補數圓環
def twos_ring():
    cx, cy, r = 220, 190, 140
    parts = [f'<circle class="ax" cx="{cx}" cy="{cy}" r="{r}"/>']
    for k in range(16):
        ang = -math.pi / 2 + 2 * math.pi * k / 16
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        val = k if k < 8 else k - 16
        cls = "hl" if val >= 0 else "bad"
        parts.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="21"/>')
        parts.append(f'<text class="pv" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{val}</text>')
        lx, ly = cx + (r + 40) * math.cos(ang), cy + (r + 40) * math.sin(ang)
        parts.append(f'<text class="m" x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="middle">{k:04b}</text>')
    parts.append(f'<text class="t" x="{cx}" y="{cy - 8}" text-anchor="middle">4-bit two\'s complement</text>')
    parts.append(f'<text x="{cx}" y="{cy + 14}" text-anchor="middle">adding 1 = one step clockwise</text>')
    parts.append(f'<text x="{cx}" y="{cy + 32}" text-anchor="middle">0111 + 1 wraps to 1000 (overflow)</text>')
    save("twos-ring.svg", 440, 380, "Sixteen 4-bit patterns on a circle with their two's complement values",
         "\n".join(parts))


# ---------------------------------------------------------------- IEEE 754 三個欄位
def ieee754():
    bits = "11000000110010000000000000000000"   # -6.25
    x0, cw = 20, 19
    parts = []
    spans = [(0, 1, "sign", "hl"), (1, 9, "exponent (8 bits, bias 127)", "bad"), (9, 32, "fraction (23 bits)", "box")]
    for a, b, name, cls in spans:
        parts.append(f'<rect class="{cls}" x="{x0 + a * cw}" y="40" width="{(b - a) * cw}" height="34" rx="4"/>')
        ty = 14 if name == "sign" else 30
        parts.append(f'<text class="t" x="{x0 + (a + b) / 2 * cw}" y="{ty}" text-anchor="middle">{name}</text>')
    for i, ch in enumerate(bits):
        parts.append(f'<text class="m" x="{x0 + i * cw + cw / 2}" y="63" text-anchor="middle">{ch}</text>')
    parts.append(f'<text x="{x0}" y="102">-6.25 = -1.1001 (binary) x 2^2  →  sign 1, exponent 2 + 127 = 129 = 10000001, '
                 'fraction 1001 000…</text>')
    save("ieee754-fields.svg", 650, 115, "The sign, exponent and fraction fields of -6.25 in IEEE 754 single precision",
         "\n".join(parts))


# ---------------------------------------------------------------- Huffman 樹
def huffman():
    nodes = {"root": (300, 30, "9"), "n4": (400, 100, "4"), "n2": (460, 170, "2"),
             "A": (200, 100, "A:5"), "B": (340, 170, "B:2"), "C": (410, 240, "C:1"), "D": (510, 240, "D:1")}
    edges = [("root", "A", "0"), ("root", "n4", "1"), ("n4", "B", "0"), ("n4", "n2", "1"),
             ("n2", "C", "0"), ("n2", "D", "1")]
    parts = []
    for a, b, lab in edges:
        (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
        parts.append(f'<line class="arrow" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        parts.append(f'<text class="pv" x="{(x1 + x2) / 2 + (-12 if x2 < x1 else 10)}" y="{(y1 + y2) / 2}">{lab}</text>')
    for k, (x, y, lab) in nodes.items():
        leaf = len(k) == 1
        parts.append(f'<rect class="{"hl" if leaf else "box"}" x="{x - 26}" y="{y - 16}" width="52" height="30" rx="8"/>')
        parts.append(f'<text class="m" x="{x}" y="{y + 5}" text-anchor="middle">{lab}</text>')
    parts.append('<text x="20" y="200">codes:</text>')
    for i, (s, c) in enumerate((("A", "0"), ("B", "10"), ("C", "110"), ("D", "111"))):
        parts.append(f'<text class="m" x="20" y="{222 + 18 * i}">{s} = {c}</text>')
    save("huffman-tree.svg", 560, 290, "Huffman tree for frequencies A5 B2 C1 D1 and the resulting codes",
         "\n".join(parts))


# ---------------------------------------------------------------- 取樣與量化
def sampling():
    parts = ['<line class="ax" x1="40" y1="180" x2="620" y2="180"/>',
             '<line class="ax" x1="40" y1="20" x2="40" y2="185"/>']
    levels = 8
    for k in range(levels):
        y = 180 - k * 20
        parts.append(f'<line class="ax" x1="40" y1="{y}" x2="620" y2="{y}" style="opacity:.25"/>')
        parts.append(f'<text class="m" x="34" y="{y + 5}" text-anchor="end">{k:03b}</text>')

    def f(x):
        return 3.5 + 3.3 * math.sin(x / 70) * math.cos(x / 190)
    wave = [(40 + x, 180 - 20 * f(x)) for x in range(0, 581, 3)]
    parts.append(f'<path class="l1" d="{path(wave)}"/>')
    stair = []
    for i in range(0, 580, 40):
        q = round(f(i))
        stair += [(40 + i, 180 - 20 * q), (40 + i + 40, 180 - 20 * q)]
        parts.append(f'<circle class="pt" cx="{40 + i}" cy="{180 - 20 * f(i):.1f}" r="4"/>')
    parts.append(f'<path class="stair" d="{path(stair)}"/>')
    parts.append('<text x="620" y="198" text-anchor="end">time → one sample every 1/rate seconds</text>')
    parts.append('<text x="46" y="14">3-bit quantization: 8 levels</text>')
    save("sampling.svg", 640, 205, "Sampling a continuous wave at regular times and rounding each sample to one of 8 levels",
         "\n".join(parts))


# ---------------------------------------------------------------- key frame 與 delta frame
def keyframes():
    parts = []
    kinds = ["K", "Δ", "Δ", "Δ", "K", "Δ", "Δ"]
    for i, k in enumerate(kinds):
        x = 20 + i * 88
        cls = "hl" if k == "K" else "box"
        parts.append(f'<rect class="{cls}" x="{x}" y="30" width="72" height="54" rx="6"/>')
        parts.append(f'<text class="t" x="{x + 36}" y="63" text-anchor="middle">{"key" if k == "K" else "delta"}</text>')
        parts.append(f'<text class="m" x="{x + 36}" y="104" text-anchor="middle">f{i}</text>')
        if i:
            parts.append(f'<line class="arrow" x1="{x - 14}" y1="57" x2="{x}" y2="57"/>')
    parts.append('<text x="20" y="18">key frame = full image; delta frame = only the pixels that changed since the previous frame</text>')
    save("keyframe-delta.svg", 640, 115, "A video stream of key frames and delta frames", "\n".join(parts))


if __name__ == "__main__":
    for fn in (analog_digital, twos_ring, ieee754, huffman, sampling, keyframes):
        fn()
    print("ok")
