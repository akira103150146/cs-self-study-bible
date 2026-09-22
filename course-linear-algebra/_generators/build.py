# -*- coding: utf-8 -*-
"""content/(Markdown)+ _layout/templates/(Jinja2)→ weekNN/*.html、*.ipynb、index.html

用法(在課程資料夾底下):
    python _generators/build.py          # 所有有內容的週 + 首頁
    python _generators/build.py 1 2      # 只建指定週(首頁一律重建)

這支程式不含任何內容,也不含任何版面:內容在 content/,版面在 _layout/ 與 assets/。
"""
import json
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
from mdtools import ContentError

ROOT = C.ROOT
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "_layout", "templates")),
                  autoescape=False, undefined=StrictUndefined, keep_trailing_newline=True)
env.globals.update(
    ui=env.get_template("macros.html").module,
    LEVEL_ZH=C.LEVEL_ZH, TIER_ZH=C.TIER_ZH, STAGE_ZH=C.STAGE_ZH,
    trap_rows=lambda q: [[t.key, t.myth, t.lookback] for t in q.traps],
)

FONT_CELL = ("import matplotlib\n"
             "# 本課圖表標籤一律用英文,不裝中文字型也不會有豆腐字。\n"
             "matplotlib.rcParams['axes.unicode_minus'] = False\n")


# ---------------------------------------------------------------- 檔名與分頁

def fname(wk, suffix):
    return f"W{wk}-{suffix}"


def page_suffixes(week):
    """(檔名後綴, 分頁標籤),依一週實際的上課順序排。"""
    out = []
    if week.lesson:
        out.append(("理論教案", "理論教案"))
    if week.prereq:
        out += [("先備檢測-學生版", "先備·學生"), ("先備檢測-教師版", "先備·教師")]
    if week.concepts:
        out += [("例題-學生版", "例題·學生"), ("例題-教師版", "例題·教師")]
    if week.quiz:
        out += [("診斷考-學生版", "診斷·學生"), ("診斷考-教師版", "診斷·教師")]
    if week.lab:
        out.append(("實作", "實作"))
    return out


def tabs(week, active):
    return [{"href": fname(week.num, s) + ".html", "label": l, "current": s == active}
            for s, l in page_suffixes(week)]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def n_todo(week):
    return sum(1 for s in week.lab if s.todo.strip())


# ---------------------------------------------------------------- 各頁

def render_week(course, week):
    wk, d = week.num, os.path.join(ROOT, f"week{week.num:02d}")
    base = dict(course=course, week=week, up="../")

    def emit(suffix, template, desc, eyebrow, h1, subtitle, chips, **extra):
        html = env.get_template(template).render(
            **base, title=f"第 {wk} 週 {suffix} · {week.title}", desc=desc,
            tabs=tabs(week, suffix), eyebrow=eyebrow, h1=h1, subtitle=subtitle,
            chips=chips, **extra)
        write(os.path.join(d, fname(wk, suffix) + ".html"), html)

    if week.lesson:
        emit("理論教案", "lesson.html", "教學腳本:節奏、講法、迷思、檢核",
             f"第 {wk} 週 · 理論教案", week.title, week.lesson.hook,
             [("理論 3 小時", False), ("搭配實作 3 小時", False), (week.sections, False)]
             + [(c, True) for c in week.chips],
             L=week.lesson, n_todo=n_todo(week))

    if week.concepts:
        nc = len(week.concepts)
        nw = sum(len(c.walkthroughs) for c in week.concepts)
        nd = sum(len(c.drills) for c in week.concepts)
        for teacher, suffix in ((False, "例題-學生版"), (True, "例題-教師版")):
            who = "教師版" if teacher else "學生版"
            sub = ("同一份內容,另外加上原理、易錯點、教學提示與每題練習的解答。數字答案全部經 sympy 驗算。"
                   if teacher else
                   "每個觀念都是三步:① 觀念 → ② 老師講解 → ③ 換你練習。練習直接寫在作答區。")
            emit(suffix, "examples.html", f"例題·{who}:觀念 → 老師講解 → 學生練習",
                 f"第 {wk} 週 · 例題·{who}", week.title, sub,
                 [(who, True), (f"{nc} 個觀念", False), (f"{nw} 題老師講解", False),
                  (f"{nd} 題練習", False)] + ([("含證明時刻", False)] if week.proof else []),
                 teacher=teacher, glossary=C.week_glossary(week.concepts))

    for quiz, stem in ((week.prereq, "先備檢測"), (week.quiz, "診斷考")):
        if quiz is None:
            continue
        summary = [[f"Q{i}", q.ref, q.answer] for i, q in enumerate(quiz.items, 1)]
        for teacher in (False, True):
            who = "教師版" if teacher else "學生版"
            emit(f"{stem}-{who}", "quiz.html", f"{stem}·{who}",
                 f"第 {wk} 週 · {stem}·{who}", f"{stem}{'(附答案與迷思對照)' if teacher else ''}",
                 f"{quiz.when} · {week.title}",
                 [(who, True), (f"{len(quiz.items)} 題", False), (f"{quiz.minutes} 分鐘", False),
                  ("不計對錯", False)],
                 quiz=quiz, teacher=teacher, summary=summary)

    if week.lab:
        nb_name = f"W{wk}-lab.ipynb"
        emit("實作", "lab.html", "Python 實作:預測 → 計算 → 解讀 → 應用",
             f"第 {wk} 週 · 實作", week.title, week.subtitle,
             [("4 個階段", True), (f"{len(week.lab)} 個步驟", False),
              (f"{n_todo(week)} 題 TODO", False), ("Colab / Jupyter", False)],
             setup=course["lab_setup"].rstrip("\n"), nb_name=nb_name)
        write_notebook(os.path.join(d, nb_name), course, week)


def write_notebook(path, course, week):
    def md(src):
        return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

    def code(src, expected=""):
        # 預期輸出存在 metadata,run_notebooks.py 實跑時逐格比對(Jupyter 會忽略這個欄位)
        meta = {"expected_output": expected} if expected else {}
        return {"cell_type": "code", "execution_count": None, "metadata": meta, "outputs": [],
                "source": src.splitlines(keepends=True)}

    plain = re.sub(r"<[^>]+>", "", week.subtitle)
    cells = [md(f"# 第 {week.num} 週 實作｜{week.title}\n\n{plain}\n\n"
                "每一步都是:**① 預測 → ② 計算 → ③ 解讀 → ④ 應用**。遇到 `# TODO` 的格子換你寫。\n"),
             code(FONT_CELL), md("### 環境設定\n"), code(course["lab_setup"])]
    for s in week.lab:
        title = re.sub(r"<[^>]+>", "", s.title)
        cells.append(md(f"## {C.STAGE_ZH[s.stage]} · {title}\n\n{s.intro_md}\n"))
        if s.code:
            cells.append(code(s.code, s.expected))
        if s.seealso_md:
            cells.append(md(s.seealso_md + "\n"))
        if s.todo:
            cells.append(code(s.todo))
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python", "version": "3.12"}},
          "nbformat": 4, "nbformat_minor": 5}
    write(path, json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


def render_index(course, weeks):
    cards = []
    for num in range(1, 19):
        title, sub = course["outline"][num]
        week, links, topics = weeks.get(num), [], ""
        if week is not None:
            title, sub = week.title, week.subtitle
            for s, label in page_suffixes(week):
                rel = f"week{num:02d}/{fname(num, s)}.html"
                if os.path.exists(os.path.join(ROOT, rel)):
                    links.append((rel, label))
            topics = f"{week.sections} · {len(week.concepts)} 個觀念 · {len(week.lab)} 個實作步驟"
        cards.append({"num": num, "title": title, "sub": sub, "links": links, "topics": topics})
    ready = sum(1 for c in cards if c["links"])
    html = env.get_template("index.html").render(
        course=course, week=None, up="", tabs=[], title=f"{course['name']} · {course['audience']}",
        desc=f"{course['name']}:18 週,理論與 Python 實作並行。", eyebrow=course["audience"],
        h1=course["name"], subtitle=course["tagline"],
        chips=[("18 週 · 3hr 理論 + 3hr 實作", True), ("每週診斷考", False),
               ("15 個證明時刻", False), ("Capstone:用 NumPy 做 PCA", False)],
        cards=cards)
    write(os.path.join(ROOT, "index.html"), html)
    return ready


def main():
    try:
        course = C.load_course()
        wanted = [int(a) for a in sys.argv[1:]] or C.available_weeks()
        weeks = {}
        for wk in C.available_weeks():
            weeks[wk] = C.load_week(wk)          # 全部都解析一次:首頁需要,也順便擋格式錯誤
        for wk in wanted:
            render_week(course, weeks[wk])
            print(f"✅ W{wk} 產出完成")
        ready = render_index(course, weeks)
        print(f"✅ index.html:18 張週卡,其中 {ready} 週可用")
    except ContentError as e:
        print(f"❌ 內容格式錯誤:{e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
