# -*- coding: utf-8 -*-
"""LessonPlan → WN-理論教案.html

節奏表下 assert:總長必須剛好 180 分。教案數字對不上就在產出前爆掉
(銜接課的教訓:教案寫「四個 Lab」但實際有六個,沒有任何機制擋得住)。
"""
import os, sys, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, page, masthead, table

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _minutes(span):
    """'00:15–00:45' → 30。接受半形 - 或全形 –。"""
    a, b = re.split(r"[–\-—]", span)
    ah, am = (int(x) for x in a.split(":"))
    bh, bm = (int(x) for x in b.split(":"))
    return (bh * 60 + bm) - (ah * 60 + am)


def render(week):
    wk, L = week.num, week.lesson
    total = sum(_minutes(t) for t, _, _ in L.clock)
    assert total == 180, f"W{wk} 節奏表合計 {total} 分,必須剛好 180"

    n_lab = len(week.labs)
    n_todo = sum(1 for lab in week.labs if lab.todo.strip())

    parts = ["<h2>哪些能快轉,哪些要踩煞車</h2>",
             table(["內容", "對學生是", "建議節奏"], L.fastforward),
             "<h2>下課鐘響時,學生要能做到</h2><ul>"
             + "".join(f"<li>{o}</li>" for o in L.outcomes) + "</ul>",
             "<h2>三小時怎麼切</h2>",
             table(["時間", "段落", "對應觀念"], L.clock, cls="clock"),
             callout("key", "🎯", "本週的證明時刻",
                     f"<p>{L.proof_moment}</p>"
                     "<p>教師版寫完整推導,學生版留引導填空。筆試不考「請證明」,"
                     "考三種變形:<strong>哪一步違反前提</strong>、<strong>舉一個反例</strong>、"
                     "<strong>用在沒看過的情境</strong>。</p>"),
             "<h2>逐段怎麼上</h2>"]
    for h, b in L.script:
        parts.append(f"<h3>{h}</h3>\n{b}")
    parts.append(callout("warn", "🧠", "學生最常翻的車",
                         "<ul>" + "".join(f"<li>{m}</li>" for m in L.myths) + "</ul>"))
    parts.append("<h2>出門檢核(下課前 5 分鐘)</h2>"
                 "<p>三題快問快答,當場收、當場知道誰卡住:</p><ol>"
                 + "".join(f"<li>{q}</li>" for q, _ in L.exit_check) + "</ol>")
    parts.append(callout("tip", "✅", "參考答案",
                         "<ol>" + "".join(f"<li>{a}</li>" for _, a in L.exit_check) + "</ol>"))
    suffix = getattr(week, "lab_suffix", "實作")
    unit = "Part" if suffix == "Capstone" else "Lab"
    hw = list(L.homework)
    if n_lab:                      # 沒有 Lab 的週(如 W18 總整理)就不加這一條
        hw.append(f'<strong>動手</strong>:到 <a href="W{wk}-{suffix}.html">{suffix}頁</a> '
                  f'把 {n_lab} 個 {unit} 跑完(頁內可下載 notebook)'
                  + (f",{n_todo} 題 TODO 自己填。" if n_todo else "。"))
    parts.append("<h2>作業與預習</h2><ul>" + "".join(f"<li>{h}</li>" for h in hw) + "</ul>")

    chips = ([chip("理論 3 小時"), chip("搭配實作 3 小時"), chip("對應本書第 12 章")]
             + [chip(c, True) for c in week.chips])
    mh = masthead(f"第 {wk} 週 · 理論教案", week.title, L.hook, chips)
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)
    # 分頁只列「這一週真的有產出」的頁面,避免死連結
    tabs = [("理論教案", "理論教案")]
    if week.concepts:
        tabs += [("例題-學生版", "例題·學生"), ("例題-教師版", "例題·教師")]
    if week.labs:
        tabs.append((suffix, suffix))
    if getattr(week, "exam_name", None):   # W9/W18 的考卷週
        tabs += [(f"{week.exam_name}-考卷版", "考卷"), (f"{week.exam_name}-詳解版", "詳解")]
    open(os.path.join(d, f"W{wk}-理論教案.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 理論教案 · {week.title}", "教學腳本:節奏、講法、迷思、檢核",
             wk, "理論教案", mh, "\n".join(parts), tabs=tabs))
