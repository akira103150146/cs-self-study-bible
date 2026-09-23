# W4 觀念 6(Lay 1.10)的電路圖。這裡用 SVG 像素座標(y 向下),和其他圖的數學座標不同。
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))


class Circuit:
    def __init__(self, w, h, mid="ah-cir"):
        self.w, self.h, self.mid = w, h, mid
        self.p = []

    def wire(self, a, b):
        self.p.append(f'<line class="ax" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" style="stroke:currentColor;stroke-width:1.6"/>')

    def _split(self, a, b, size):
        """把線段中間讓出 size 的空間,回傳 (起點, 元件起點, 元件終點, 終點, 單位向量, 法向量)。"""
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        s = (m[0] - ux * size / 2, m[1] - uy * size / 2)
        e = (m[0] + ux * size / 2, m[1] + uy * size / 2)
        return s, e, (ux, uy), (nx, ny), m

    def resistor(self, a, b, label, side=1, dist=14):
        s, e, u, n, m = self._split(a, b, 26)
        self.wire(a, s); self.wire(e, b)
        pts = [s]
        for i in range(1, 7):
            t = (s[0] + u[0] * 26 * i / 7 - u[0] * 13 + 13 * u[0], s[1] + u[1] * 26 * i / 7)
            amp = 5 if i % 2 else -5
            pts.append((s[0] + u[0] * 26 * i / 7 + n[0] * amp, s[1] + u[1] * 26 * i / 7 + n[1] * amp))
        pts.append(e)
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.p.append(f'<polyline points="{d}" style="fill:none;stroke:currentColor;stroke-width:1.6"/>')
        self.p.append(f'<text class="m" x="{m[0] + n[0] * dist * side:.1f}" y="{m[1] + n[1] * dist * side + 4:.1f}" text-anchor="middle">{label}</text>')

    def battery(self, a, b, label, plus="start", side=1, dist=16):
        """電池:長板(+)與短板(−)。plus 指出 + 板靠近線段的哪一端。"""
        s, e, u, n, m = self._split(a, b, 12)
        self.wire(a, s); self.wire(e, b)
        long_at_start = (plus == "start")
        for (pt, half) in ((s, 9 if long_at_start else 5), (e, 5 if long_at_start else 9)):
            self.p.append(f'<line x1="{pt[0] + n[0] * half:.1f}" y1="{pt[1] + n[1] * half:.1f}" '
                          f'x2="{pt[0] - n[0] * half:.1f}" y2="{pt[1] - n[1] * half:.1f}" '
                          f'style="stroke:currentColor;stroke-width:{2.4 if half == 9 else 3.2}"/>')
        self.p.append(f'<text class="m" x="{m[0] + n[0] * dist * side:.1f}" y="{m[1] + n[1] * dist * side + 4:.1f}" text-anchor="middle">{label}</text>')

    def loop(self, c, r, label):
        """逆時針的迴路電流箭頭 + 標籤。"""
        a0, a1 = 1.2 * math.pi, -0.4 * math.pi        # 逆時針,箭頭收在右上(和課本的畫法一致)
        x0, y0 = c[0] + r * math.cos(a0), c[1] - r * math.sin(a0)
        x1, y1 = c[0] + r * math.cos(a1), c[1] - r * math.sin(a1)
        self.p.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 1 0 {x1:.1f},{y1:.1f}" '
                      f'style="fill:none;stroke:currentColor;stroke-width:1.4" marker-end="url(#{self.mid})"/>')
        self.p.append(f'<text class="t" x="{c[0]}" y="{c[1] + 5}" text-anchor="middle">{label}</text>')

    def node(self, c, label, dx=-10, dy=-6):
        self.p.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="3" style="fill:currentColor"/>')
        self.p.append(f'<text class="m" x="{c[0] + dx}" y="{c[1] + dy}" text-anchor="middle">{label}</text>')

    def svg(self, name, aria):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" role="img" aria-label="{aria}">'
                f'<defs><marker id="{self.mid}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
                f'markerWidth="10" markerHeight="10" orient="auto"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(head + "".join(self.p) + "</svg>\n")
