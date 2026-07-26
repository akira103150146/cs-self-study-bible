# -*- coding: utf-8 -*-
"""ExamPaper → WN-<name>-考卷版.html + WN-<name>-詳解版.html

兩個設計決定(來自銜接課 review 的發現):
1. 作答區高度<strong>依配分</strong>決定,不是一律 132px。
   4 分題寫不下 12 分題的內容。
2.「對應第 N 週」只印在<strong>詳解版</strong>。考卷版印出來等於告訴學生
   該用哪一週的招式,模擬考就失去意義了。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, page, masthead

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配分 → 作答區高度(px)
HEIGHT = {4: 140, 5: 165, 6: 200, 8: 260, 10: 320, 12: 380}


def _height(p):
    if p.needs_graph:
        return 460
    if p.pts in HEIGHT:
        return HEIGHT[p.pts]
    # 沒列到的配分:線性內插,每分約 33px,下限 140
    return max(140, int(p.pts * 33))


def _tabs(wk, name):
    return [(f"{name}-考卷版", "考卷"), (f"{name}-詳解版", "詳解")]


def render(exam, with_solutions):
    wk = exam.week
    total = sum(p.pts for g in exam.groups for p in g.problems)
    assert total == 100, f"W{wk} {exam.name} 總分 {total},必須是 100"

    parts = []
    for g in exam.groups:
        gpts = sum(p.pts for p in g.problems)
        # origin(對應週次)只在詳解版顯示
        sub = f"{g.origin} · {gpts} pts" if with_solutions else f"{gpts} pts"
        parts.append(f'  <div class="qtype"><div class="badge">{g.num}</div><div>'
                     f'<h3 class="qtype-title">{g.title}</h3>'
                     f'<span class="qtype-sub">{sub}</span></div></div>')
        for p in g.problems:
            if with_solutions:
                tail = (f'<div class="sol"><span class="sol-label">Solution · {p.pts} pts</span>'
                        f'{p.sol}</div>')
            else:
                tail = (f'<div class="workspace" style="min-height:{_height(p)}px">'
                        f'<span class="ws-label">Answer</span></div>')
            parts.append(f'  <div class="ex"><div class="ex-head">'
                         f'<span class="ex-tag">Problem {p.label}</span>'
                         f'<span class="level {p.level}">{p.pts} pts</span></div>'
                         f'<p class="problem">{p.stem}</p>{tail}</div>')

    kind = "詳解版" if with_solutions else "考卷版"
    chips = [chip(f"Total {total} pts", True), chip(f"{len(exam.groups)} problems"),
             chip(f"Time {exam.minutes} min"), chip("No calculator")]

    if with_solutions:
        subtitle = ("同一份考卷的解答本:每題重印英文題目,附中文解題敘述與配分切點。"
                    "所有答案已用 sympy 驗證,可直接當標準答案批改。")
        body_head = callout("key", "🧮", "給批改老師",
                            "<p>每題詳解都標了配分切點。改題時<strong>看步驟不只看答案</strong>:"
                            "方法對、只是最後代錯數字,給大部分分數;方法錯則整段扣。</p>"
                            "<p>題組標題旁的「對應第 N 週」只印在這一版——"
                            "考卷版刻意不印,以免學生直接對照到該用哪一招。</p>")
    else:
        subtitle = ("題目全為英文原文;請把每題的<strong>完整解題過程</strong>寫在作答區。"
                    "只寫答案不給過程者,即使答案正確也只能拿部分分數。")
        body_head = callout("note", "📄", "Instructions",
                            "<ul>"
                            "<li>Show all work in the answer space; a correct final answer with "
                            "no work receives partial credit only.</li>"
                            f"<li>There are <strong>{len(exam.groups)} problems</strong> worth a "
                            f"total of <strong>{total} points</strong>; point values are marked "
                            "on each part.</li>"
                            "<li>Give exact values where possible; decimals are acceptable for "
                            "estimation problems.</li>"
                            "<li>Calculators and notes are not allowed.</li>"
                            "</ul>")

    mh = masthead(f"第 {wk} 週 · {exam.name}{kind}",
                  f"Calculus I — {exam.name_en}", subtitle, chips)
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)
    fname = f"W{wk}-{exam.name}-{kind}.html"
    with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
        f.write(page(f"第 {wk} 週 {exam.name}·{kind}", f"{exam.name}{kind}", wk,
                     f"{exam.name}-{kind}", mh, body_head + "\n\n" + "\n".join(parts),
                     tabs=_tabs(wk, exam.name)))
