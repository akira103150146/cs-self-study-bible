# -*- coding: utf-8 -*-
"""[Concept] → WN-例題-學生版.html + WN-例題-教師版.html

不變式:兩版的 .problem 與 .drill 題幹逐字相同。
差別只在 學生版=.guide+.workspace,教師版=.deep+.sol+.misstep+.ans-body。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, page, masthead
from weekdata import LEVEL_ZH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _qtype(i, c):
    return (f'  <div class="qtype"><div class="badge">{i}</div><div>'
            f'<h3 class="qtype-title">{c.title_en}｜{c.title_zh}</h3>'
            f'<span class="qtype-sub">{c.sub}</span></div></div>')


def _ex_head(c):
    return (f'<div class="ex-head"><span class="ex-tag">示範</span>'
            f'<span class="level {c.level}">{LEVEL_ZH[c.level]}</span></div>')


def student_body(week):
    out = []
    for i, c in enumerate(week.concepts, 1):
        guide = "\n".join(f"<li>{g}</li>" for g in c.guide)
        out.append(_qtype(i, c))
        out.append(f'  <div class="idea"><div class="ico">🧭</div><div>'
                   f'<span class="lbl">引導推導</span>'
                   f'<p>跟著老師一步步想,自己把道理推出來:</p>\n'
                   f'<ol class="guide">\n{guide}\n</ol></div></div>')
        out.append('  <div class="block-label teach">一起做 · 示範</div>')
        out.append(f'  <div class="ex">{_ex_head(c)}'
                   f'<p class="problem">{c.demo}</p>'
                   f'<p class="hint"><b>一起想</b>:{c.demo_hint}</p>'
                   f'<div class="workspace"><span class="ws-label">作答區</span></div></div>')
        out.append('  <div class="block-label">換你練習</div>')
        stems = "\n".join(f"    <li>{q}</li>" for q, _ in c.drills)
        out.append(f'  <ol class="drill">\n{stems}\n  </ol>\n')
    return "\n".join(out)


def teacher_body(week):
    out = []
    for i, c in enumerate(week.concepts, 1):
        out.append(_qtype(i, c))
        out.append(f'  <div class="idea"><div class="ico">💡</div><div>'
                   f'<span class="lbl">觀念</span><p>{c.idea}</p></div></div>')
        out.append(f'  <div class="deep"><div class="deep-head"><span class="tag">原理</span>'
                   f'為什麼成立 · 推導與證明</div><div class="deep-body">\n{c.deep}\n</div></div>')
        out.append('  <div class="block-label teach">示範 · 老師講</div>')
        out.append(f'  <div class="ex">{_ex_head(c)}'
                   f'<p class="problem">{c.demo}</p>'
                   f'<div class="sol"><span class="sol-label">詳解</span>{c.demo_sol}</div>'
                   f'<div class="misstep"><b>易錯點</b>　{c.misstep}</div></div>')
        out.append('  <div class="block-label">換你練習 · 附解答</div>')
        items = "\n".join(f'    <li>{q}<div class="ans-body">{a}</div></li>' for q, a in c.drills)
        out.append(f'  <ol class="drill">\n{items}\n  </ol>\n')
    return "\n".join(out)


def render(week):
    wk = week.num
    nc = len(week.concepts)
    nd = sum(len(c.drills) for c in week.concepts)
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)

    chips_s = [chip("學生版 · 引導推導", True), chip(f"{nc} 個觀念"),
               chip(f"{nc} 題示範"), chip(f"{nd} 題變形練習")]
    mh_s = masthead(f"第 {wk} 週 · 例題·學生版", f"{week.title} · 引導推導",
                    "這份不直接給公式。每個觀念用一串<strong>引導問題與填空</strong>,"
                    "讓你跟著老師把原理親手推出來——而不是死背。空白處自己填,練習在筆記本上作答。",
                    chips_s)
    body_s = (callout("note", "🧭", "怎麼用這份學生版",
                      "<p>每個觀念先跟著<strong>引導推導</strong>把道理想出來(空白處填答),"
                      "再看<strong>示範</strong>一起做一題,最後<strong>換你練習</strong>在筆記本上動手。"
                      "想對答案或看原理證明,翻老師版。</p>")
              + "\n\n" + student_body(week))
    open(os.path.join(d, f"W{wk}-例題-學生版.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 例題·學生版 · {week.title}", "引導式推導,帶學生理解原理而非死背",
             wk, "例題-學生版", mh_s, body_s))

    chips_t = [chip("教師版 · 原理與證明", True), chip(f"{nc} 個觀念"),
               chip(f"{nc} 題示範"), chip(f"{nd} 題附解答")]
    mh_t = masthead(f"第 {wk} 週 · 例題·教師版", f"{week.title} · 原理與證明",
                    "每個觀念附完整推導與證明,示範題有詳解與易錯點,練習題附解答。"
                    "答案全部經 sympy 驗算。", chips_t)
    body_t = (callout("key", "🎯", "兩版怎麼搭配",
                      "<p>你看這份的<strong>原理</strong>區塊,帶學生用學生版的<strong>引導推導</strong>"
                      "自己把它推出來。示範題先讓他們試,再對詳解。</p>")
              + "\n\n" + teacher_body(week))
    open(os.path.join(d, f"W{wk}-例題-教師版.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 例題·教師版 · {week.title}", "含原理證明與完整解答",
             wk, "例題-教師版", mh_t, body_t))
