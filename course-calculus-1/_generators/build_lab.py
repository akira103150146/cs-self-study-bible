# -*- coding: utf-8 -*-
"""[Lab] → WN-實作.html(可讀版) + WN-lab.ipynb(可執行)

兩者同源:HTML 的程式碼區塊與 notebook 的 code cell 來自同一個 Lab.code,
所以「頁面實印的 TODO 數」與「notebook 的 TODO 數」必然一致(verify.py 會查)。
capstone=True 時檔名改 WN-Capstone.html / WN-capstone.ipynb,分頁標籤同步改。
"""
import os, sys, json, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, page, masthead

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETUP = ("import math\n"
         "import numpy as np\n"
         "import sympy as sp\n"
         "import matplotlib.pyplot as plt\n")

FONT_CELL = ("import matplotlib\n"
             "# Colab 想顯示中文: !apt-get -qq install fonts-noto-cjk\n"
             "# 再設 matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']\n"
             "# 本課圖表標籤一律用英文,不裝字型也不會有豆腐字。\n"
             "matplotlib.rcParams['axes.unicode_minus'] = False\n")


def _pre(code):
    return f"<pre><code>{html.escape(code, quote=True)}</code></pre>"


def _tabs(suffix, has_examples=True):
    if not has_examples:           # capstone 週沒有例題雙版
        return [("理論教案", "理論教案"), (suffix, suffix)]
    return [("理論教案", "理論教案"), ("例題-學生版", "例題·學生"),
            ("例題-教師版", "例題·教師"), (suffix, suffix)]


def render(week, capstone=False):
    wk = week.num
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)
    n_todo = sum(1 for lab in week.labs if lab.todo.strip())
    stem = getattr(week, "lab_suffix", "Capstone" if capstone else "實作")
    unit = "Part" if stem == "Capstone" else "Lab"
    nb_name = f"W{wk}-{'capstone' if capstone else 'lab'}.ipynb"

    # ---------- HTML 可讀版 ----------
    parts = [callout("note", "💻", "怎麼跑",
                     "<p>這頁是<strong>可讀版</strong>;程式要實際執行,請下載 notebook,上傳到 "
                     '<a href="https://colab.research.google.com/" target="_blank" '
                     'rel="noopener">Google Colab</a>(或用本機 Jupyter),由上往下逐格執行。</p>'
                     f'<p style="margin-top:10px"><a class="dl" href="{nb_name}" download>'
                     f'⬇ 下載 {nb_name}</a></p>'),
             "<h2>環境設定</h2><p>先跑這格,把套件載進來。</p>",
             _pre(SETUP)]
    for lab in week.labs:
        parts.append(f"<h2>{lab.title}</h2><p>{lab.intro}</p>{_pre(lab.code)}")
        if lab.expected:
            parts.append(f'<div class="out"><span class="out-label">預期輸出</span>'
                         f'{html.escape(lab.expected)}</div>')
        if lab.seealso:
            parts.append(f"<p><b>會看到</b>:{lab.seealso}</p>")
        if lab.todo.strip():
            parts.append(f"<p>換你試:</p>{_pre(lab.todo)}")

    chips = [chip(f"{len(week.labs)} 個 {unit}", True),
             chip(f"{n_todo} 題 TODO"), chip("Colab / Jupyter")]
    mh = masthead(f"第 {wk} 週 · {stem}", week.title, week.subtitle, chips)
    open(os.path.join(d, f"W{wk}-{stem}.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 {stem} · {week.title}", "Python 實作:把概念跑出來、畫出來",
             wk, stem, mh, "\n".join(parts), tabs=_tabs(stem, bool(week.concepts))))

    # ---------- ipynb ----------
    def md(src):
        return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

    def code(src):
        return {"cell_type": "code", "execution_count": None, "metadata": {},
                "outputs": [], "source": src.splitlines(keepends=True)}

    cells = [md(f"# 第 {wk} 週 {stem}｜{week.title}\n\n{week.subtitle}\n"),
             md("### (選用)讓圖表顯示中文\n"),
             code(FONT_CELL),
             md("### 環境設定\n"),
             code(SETUP)]
    for lab in week.labs:
        cells.append(md(f"## {lab.title}\n\n{lab.intro}\n"))
        cells.append(code(lab.code))
        if lab.todo.strip():
            cells.append(code(lab.todo))
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                      "name": "python3"},
                       "language_info": {"name": "python", "version": "3.12"}},
          "nbformat": 4, "nbformat_minor": 5}
    with open(os.path.join(d, nb_name), "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
