# -*- coding: utf-8 -*-
"""content/(Markdown)+ _layout/templates/(Jinja2)→ chNN/*.html、chNN/CN-starter.zip、index.html

用法(在課程資料夾底下):
    python _generators/build.py          # 所有有內容的章 + 首頁
    python _generators/build.py 1 3      # 只建指定章(首頁一律重建)

這支程式不含任何內容,也不含任何版面:內容在 content/ 與 labs/,版面在 _layout/ 與 assets/。
"""
import os
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402
from mdtools import ContentError  # noqa: E402

try:
    import labkit  # noqa: E402
except ImportError:          # Task 6 之前還沒有 labkit
    labkit = None


def make_env(root):
    env = Environment(loader=FileSystemLoader(os.path.join(root, "_layout", "templates")),
                      autoescape=False, undefined=StrictUndefined, keep_trailing_newline=True)
    env.globals.update(
        ui=env.get_template("macros.html").module,
        LEVEL_ZH=C.LEVEL_ZH, TIER_ZH=C.TIER_ZH,
        trap_rows=lambda q: [[t.key, t.myth, t.lookback] for t in q.traps],
    )
    return env


# ---------------------------------------------------------------- 檔名與分頁

def fname(num, suffix):
    return f"C{num}-{suffix}"


def page_suffixes(ch):
    """(檔名後綴, 分頁標籤),依上課順序:講義 → 題庫 → Lab → 專案。"""
    out = []
    if ch.concepts:
        out += [("講義-學生版", "講義·學生"), ("講義-教師版", "講義·教師")]
    if ch.bank:
        out += [("題庫-學生版", "題庫·學生"), ("題庫-教師版", "題庫·教師")]
    if ch.lab:
        out.append(("Lab", "Lab"))
    if ch.projects:
        out.append(("專案", "專案"))
    return out


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def bank_groups(ch):
    return [{"concept": c, "qs": [q for q in ch.bank if q.concept == c.id]}
            for c in ch.concepts if any(q.concept == c.id for q in ch.bank)]


# ---------------------------------------------------------------- 各頁

def render_chapter(root, env, course, ch):
    num, d, written = ch.num, os.path.join(root, f"ch{ch.num:02d}"), []
    tabs_all = page_suffixes(ch)
    zip_name = fname(num, "starter.zip")

    def emit(suffix, template, desc, eyebrow, h1, subtitle, chips, **extra):
        tabs = [{"href": fname(num, s) + ".html", "label": l, "current": s == suffix} for s, l in tabs_all]
        html = env.get_template(template).render(
            course=course, chapter=ch, up="../", title=f"第 {num} 章 {suffix} · {ch.title}",
            desc=desc, tabs=tabs, eyebrow=eyebrow, h1=h1, subtitle=subtitle, chips=chips, **extra)
        written.append(write(os.path.join(d, fname(num, suffix) + ".html"), html))

    h1 = f"{ch.title}｜{ch.title_zh}"
    if ch.concepts:
        nd = sum(len(c.drills) for c in ch.concepts)
        for teacher in (False, True):
            who = "教師版" if teacher else "學生版"
            sub = ("同一份內容,另外加上原理、易錯點、教學提示與每題練習的解答。" if teacher else
                   "每個觀念都是三步:① 觀念 → ② 老師講解 → ③ 換你練習。練習直接寫在作答區。")
            emit(f"講義-{who}", "notes.html", f"觀念講義·{who}", f"第 {num} 章 · 觀念講義·{who}", h1, sub,
                 [(who, True), (f"{len(ch.concepts)} 個觀念", False), (f"{nd} 題隨堂練習", False),
                  (ch.part, False)],
                 teacher=teacher, glossary=C.chapter_glossary(ch.concepts))
    if ch.bank:
        counts = {t: sum(1 for q in ch.bank if q.qtype == t) for t in C.QTYPES}
        for teacher in (False, True):
            who = "教師版" if teacher else "學生版"
            emit(f"題庫-{who}", "bank.html", f"筆試題庫·{who}", f"第 {num} 章 · 筆試題庫·{who}",
                 f"{ch.title}｜筆試題庫", ch.subtitle,
                 [(who, True), (f"{len(ch.bank)} 題", False)]
                 + [(f"{t} {n}", False) for t, n in counts.items() if n],
                 teacher=teacher, groups=bank_groups(ch))
    if ch.lab:
        emit("Lab", "lab.html", "核心 Lab 規格書", f"第 {num} 章 · 核心 Lab", f"{ch.title}｜核心 Lab",
             ch.subtitle, [({"c": "C", "python": "Python", "mixed": "C + Python"}[ch.lab.lang], True),
                           (f"{len(ch.lab.tasks)} 個任務", False), ("make test", False)],
             zip_name=zip_name)
        lab_dir = os.path.join(root, "labs", f"ch{num:02d}")
        if labkit is not None and os.path.isdir(lab_dir):
            zp = os.path.join(d, zip_name)
            labkit.make_zip(root, num, zp)
            written.append(zp)
    if ch.projects:
        emit("專案", "projects.html", "延伸專案", f"第 {num} 章 · 延伸專案", f"{ch.title}｜延伸專案",
             ch.subtitle, [(f"{len(ch.projects)} 個專案", True), ("選做", False)])
    return written


def render_index(root, env, course, chapters):
    parts = []
    for num_, name, nums in course["parts"]:
        cards = []
        for n in nums:
            title, sub = course["outline"][n]
            ch, links, topics = chapters.get(n), [], ""
            if ch is not None:
                title, sub = f"{ch.title}｜{ch.title_zh}", ch.subtitle
                for s, label in page_suffixes(ch):
                    rel = f"ch{n:02d}/{fname(n, s)}.html"
                    if os.path.exists(os.path.join(root, rel)):
                        links.append((rel, label))
                topics = (f"{len(ch.concepts)} 個觀念 · {len(ch.bank)} 題筆試 · "
                          f"{len(ch.lab.tasks) if ch.lab else 0} 個 Lab 任務 · {len(ch.projects)} 個專案")
            cards.append({"num": n, "title": title, "sub": sub, "links": links, "topics": topics})
        parts.append({"num": num_, "name": name, "cards": cards})
    html = env.get_template("index.html").render(
        course=course, chapter=None, up="", tabs=[], title=f"{course['name']} · {course['audience']}",
        desc=f"{course['name']}:18 章,觀念講義、筆試題庫、核心 Lab、延伸專案。", eyebrow=course["audience"],
        h1=course["name"], subtitle=course["tagline"],
        chips=[("18 章 · 每章四件", True), ("系統主線 C", False), ("應用主線 Python", False),
               ("Docker 統一環境", False)],
        parts=parts)
    return write(os.path.join(root, "index.html"), html)


def build_all(root=C.ROOT, chapters=None):
    course = C.load_course(root)
    env = make_env(root)
    loaded = {n: C.load_chapter(root, n) for n in C.available_chapters(root)}   # 全部解析一次,順便擋格式錯誤
    written = []
    for n in chapters or sorted(loaded):
        written += render_chapter(root, env, course, loaded[n])
    written.append(render_index(root, env, course, loaded))
    return written


def main():
    try:
        wanted = [int(a) for a in sys.argv[1:]] or None
        out = build_all(C.ROOT, wanted)
        print(f"✅ 產出 {len(out)} 個檔案")
    except ContentError as e:
        print(f"❌ 內容格式錯誤:{e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
