# -*- coding: utf-8 -*-
"""全部週資料 → index.html(18 張週卡)。尚未產出的週顯示「準備中」。"""
import os, sys, importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, FONTS, THEME_JS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 週次 → (標題, 副標)。內容週的資料由 weeks/wNN.py 覆蓋,這裡是尚未製作時的預告文案。
OUTLINE = {
    1: ("極限的嚴格定義與浮點數現實", "ε-δ 一次講透,外加電腦為什麼算不出真極限"),
    2: ("反函數微分與雙曲函數", "反三角、雙曲函數,以及反函數微分公式的來源"),
    3: ("Cauchy MVT 與泰勒多項式", "L'Hôpital 為何成立;用泰勒多項式做近似與誤差估計"),
    4: ("分部積分", "乘積法則反過來走,含遞迴式"),
    5: ("三角積分與三角代換", "什麼時候能換、換完定義域怎麼變"),
    6: ("部分分式分解", "拆式子＝解線性方程組,線代的第一個伏筆"),
    7: ("積分技巧總整理與數值積分", "Simpson 與 Gauss 求積,誤差為何是 O(h⁴)"),
    8: ("瑕積分與收斂判定", "機率密度與 softmax 歸一化常數的數學根據"),
    9: ("期中考", "範圍 W1–W8,計算 60／概念 25／應用 15"),
    10: ("面積與體積", "切片法與殼層法,公式全部回到黎曼和"),
    11: ("弧長與旋轉曲面", "折線長度如何收斂到弧長"),
    12: ("功、質心與期望值", "期望值就是積分——loss 到底在算什麼"),
    13: ("參數式曲線與極座標", "面積與弧長的極座標版本"),
    14: ("一階可分離變數 ODE", "成長衰減模型,實作 Euler 法"),
    15: ("一階線性 ODE 與積分因子", "實作 RK4,比較誤差階數"),
    16: ("方向場、平衡點與穩定性", "梯度流:最佳化的連續極限"),
    17: ("Capstone:最佳化即動力學", "梯度下降＝解微分方程;momentum＝帶阻尼的二階 ODE"),
    18: ("證明總整理與期末考", "15 個證明時刻串成一張地圖"),
}


def card(wk, week):
    d = os.path.join(ROOT, f"week{wk:02d}")
    links = []
    for suffix, label in [("理論教案", "理論教案"), ("例題-學生版", "例題·學生"),
                          ("例題-教師版", "例題·教師"), ("實作", "實作"),
                          ("Capstone", "Capstone"),
                          ("期中考-考卷版", "考卷"), ("期中考-詳解版", "詳解"),
                          ("期末考-考卷版", "考卷"), ("期末考-詳解版", "詳解")]:
        rel = f"week{wk:02d}/W{wk}-{suffix}.html"
        if os.path.exists(os.path.join(ROOT, rel)):
            links.append(f'<a href="{rel}">{label}</a>')
    title, sub = OUTLINE[wk]
    if week is not None:
        title, sub = week.title, week.subtitle
    done = bool(links)
    topics = (f"{len(week.concepts)} 觀念 · {len(week.labs)} Lab"
              if week is not None and (week.concepts or week.labs) else "準備中")
    return (f'    <article class="week-card">\n'
            f'      <div class="week-head">\n'
            f'        <span class="week-num">{wk:02d}</span>\n'
            f'        <div><h3>{title}</h3><p class="week-sub">{sub}</p></div>\n'
            f'        <span class="week-status {"done" if done else "soon"}">'
            f'{"可用" if done else "準備中"}</span>\n'
            f'      </div>\n'
            f'      <p class="week-topics">{topics}</p>\n'
            f'      <div class="week-links">{"".join(links)}</div>\n'
            f'    </article>')


def main():
    cards, ready = [], 0
    for wk in range(1, 19):
        try:
            week = importlib.import_module(f"weeks.w{wk:02d}").WEEK
        except (ModuleNotFoundError, AttributeError):
            week = None
        c = card(wk, week)
        if 'week-status done' in c:
            ready += 1
        cards.append(c)

    chips = "".join([chip("18 週 · 108 小時", True), chip("3hr 理論 + 3hr 實作"),
                     chip("15 個證明時刻"), chip("Capstone:最佳化即動力學")])
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>微積分(一) · 資工系大一</title>
<meta name="description" content="資工系大一微積分(一):18 週,理論與 Python 實作並行,收斂到「最佳化即動力學」capstone。">
<script>(function(){{try{{var t=localStorage.getItem('handout-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/handout.css">
</head>
<body>

<nav class="packet-nav">
  <span class="home"><span class="dot">∫</span>微積分(一) · 課程首頁</span>
  <span class="spacer"></span>
  <button class="theme-toggle" title="切換深淺色" aria-label="切換主題">☾</button>
</nav>

<main class="sheet">

  <header class="masthead">
    <div class="eyebrow">資工系 · 大一上</div>
    <h1>微積分(一)</h1>
    <p class="subtitle">18 週,理論 3 小時 + 實作 3 小時並行。從極限的嚴格定義一路走到微分方程,
    實作主線最後收在那句話:<strong>梯度下降其實是在解微分方程</strong>。</p>
    <div class="chips">{chips}</div>
  </header>

  <p class="course-intro">每週三件式:<strong>理論教案</strong>(老師的教學腳本)、<strong>例題</strong>
  (觀念導向,分教師版含原理證明 / 學生版引導推導)、<strong>實作</strong>(Python,把概念跑出來、畫出來)。
  接續 6 週暑期銜接課,不重教計算,補的是嚴謹度與整套積分技巧。</p>

  <div class="week-list">

{chr(10).join(cards)}

  </div>

  <div class="callout key">
    <div class="ico">🎯</div>
    <div><span class="c-title">貫穿全學期的實作主線</span>
      <p>銜接課教的是<strong>離散步驟</strong>——一步一步走梯度下降。這學期把它接到<strong>連續數學</strong>:
      泰勒近似(W3)解釋為什麼一階近似夠用,積分與期望值(W8、W12)解釋 loss 到底在算什麼,
      微分方程(W14–17)最後揭穿——<em>梯度下降就是在解 ODE,learning rate 就是步長</em>。</p>
    </div>
  </div>

  <footer class="foot">微積分(一) · 資工系大一　|　風格延續《CS 自學聖經》設計系統</footer>
</main>
{THEME_JS}
</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ index.html:18 張週卡,其中 {ready} 週可用")


if __name__ == "__main__":
    main()
