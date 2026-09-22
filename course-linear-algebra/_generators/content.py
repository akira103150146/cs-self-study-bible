# -*- coding: utf-8 -*-
"""content/ 底下的 Markdown → 結構化資料(已轉好的 HTML 片段)。

這一層只管「內容長什麼樣、有沒有缺」,不管排版。
格式不合就丟 ContentError(帶檔名),在產出任何 HTML 之前擋下來。
各檔的寫法見 content/README.md。
"""
import glob
import os
import re
from dataclasses import dataclass, field

import yaml

from mdtools import (ContentError, fenced_blocks, list_items, pipe_table, render,
                     render_inline, split_front_matter, split_sections, strip_fences)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

LEVEL_ZH = {"basic": "基礎", "mid": "進階", "hard": "挑戰"}
TIER_OF = {"照做": "do", "是非": "tf", "變化": "vary", "應用": "app", "挑戰": "challenge"}
TIER_ZH = {v: k for k, v in TIER_OF.items()}
TIER_RANK = {"do": 1, "tf": 2, "vary": 3, "app": 4, "challenge": 5}
TIER_ORDER_ZH = " → ".join(TIER_OF)
STAGE_OF = {"①": "predict", "②": "compute", "③": "interpret", "④": "apply"}
STAGE_ZH = {"predict": "① 預測", "compute": "② 計算", "interpret": "③ 解讀", "apply": "④ 應用"}
STAGE_RANK = {"predict": 1, "compute": 2, "interpret": 3, "apply": 4}


# ---------------------------------------------------------------- 資料結構

@dataclass
class Walkthrough:
    label: str         # 「例 1」
    source: str        # 出處,例如 Lay 1.1 Example 1;空字串 = 沒標
    stem: str          # 英文題幹 HTML
    steps: str         # 中文逐步講解 HTML(<ol>)
    note: str = ""     # 教師備註(只在教師版)


@dataclass
class Drill:
    tier: str          # do / tf / vary / app / challenge
    source: str
    stem: str
    sol: str
    note: str = ""     # 教師備註(只在教師版)


@dataclass
class Concept:
    slug: str
    title_en: str
    title_zh: str
    sub: str
    level: str
    source: str        # 課本節次,例如 Lay 1.1
    supplement: bool   # 補充觀念(可略、可自學)
    lab_hook: str
    idea: str
    glossary: list     # [[英文, 中文, 說明]](HTML)
    plain: str
    geometry: str      # 選填
    cs_use: str
    applications: str  # 選填
    numerical: str     # 選填:數值筆記(Numerical Note)
    reasonable: str    # 選填:合理性檢查(Reasonable Answers)
    deep: str
    walkthroughs: list
    misstep: str
    teach_tip: str
    drills: list
    checks: list = field(default_factory=list)   # [(標籤, 運算式)]


@dataclass
class ProofMoment:
    after: int
    title_zh: str
    statement: str
    why: str
    key_idea: str
    proof: str
    checks: list = field(default_factory=list)


@dataclass
class Choice:
    letter: str
    text: str


@dataclass
class Trap:
    key: str           # 選擇題:錯誤選項字母;簡答:常見錯答(HTML)
    myth: str
    lookback: str


@dataclass
class QuizItem:
    ref: str           # 「觀念 1」或「先備」
    stem: str
    choices: list      # [Choice];空 = 簡答
    answer: str        # 選擇題:字母;簡答:答案 HTML
    why: str
    traps: list        # [Trap]


@dataclass
class Quiz:
    kind: str          # 診斷考 / 先備檢測
    when: str
    minutes: int
    items: list
    checks: list = field(default_factory=list)


@dataclass
class LabStep:
    stage: str
    title: str
    intro: str
    code: str
    expected: str
    seealso: str
    todo: str
    intro_md: str = ""      # notebook 用原始 Markdown(Jupyter 自己渲染數學式)
    seealso_md: str = ""


@dataclass
class Lesson:
    hook: str
    fastforward: tuple  # (表頭, 列)
    outcomes: list
    clock: tuple
    proof_moment: str
    script: list        # [(小節標題, HTML)]
    myths: list
    exit_check: list    # [(問題, 答案)]
    homework: list


@dataclass
class Week:
    num: int
    title: str
    subtitle: str
    sections: str
    pages: str
    chips: list
    concepts: list
    proof: object
    lesson: object
    quiz: object
    prereq: object
    lab: list
    lab_checks: list


# ---------------------------------------------------------------- 共用

def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def _sections(body, path, allowed, required):
    """'## 標題' 切段 → dict。拼錯或多出來的標題直接報錯(避免內容悄悄消失)。"""
    got = {}
    for title, text in split_sections(body, 2):
        if title is None:
            if text.strip():
                raise ContentError(f"{path}: 第一個 ## 標題之前有文字,不知道要放哪:{text.strip()[:40]}")
            continue
        if title not in allowed:
            raise ContentError(f"{path}: 不認得的段落「## {title}」,可用的有:{'、'.join(allowed)}")
        if title in got:
            raise ContentError(f"{path}: 段落「## {title}」出現兩次")
        got[title] = text
    missing = [t for t in required if not got.get(t, "").strip()]
    if missing:
        raise ContentError(f"{path}: 缺少段落 {'、'.join('## ' + t for t in missing)}")
    return got


def _need(meta, keys, path):
    missing = [k for k in keys if not str(meta.get(k, "")).strip()]
    if missing:
        raise ContentError(f"{path}: front matter 缺 {', '.join(missing)}")


def _checks(text, path):
    """## 驗算 段落裡 ```check 區塊的每一行 → [(標籤, 運算式)]。# 開頭是註解。"""
    out = []
    for info, code in fenced_blocks(text or ""):
        if info != "check":
            raise ContentError(f"{path}: 「## 驗算」裡的程式區塊要標成 ```check,得到 ```{info}")
        for n, line in enumerate(code.split("\n"), 1):
            line = line.strip()
            if line and not line.startswith("#"):
                out.append((f"{_rel(path)} · {line[:70]}", line))
    return out


# ---------------------------------------------------------------- 觀念

CONCEPT_SECTIONS = ["觀念", "名詞對照", "白話說", "幾何意義", "在資工哪裡用", "實際應用",
                    "數值筆記", "合理性檢查", "原理", "老師講解", "易錯點", "教學提示", "練習", "驗算"]
CONCEPT_REQUIRED = ["觀念", "名詞對照", "白話說", "在資工哪裡用", "原理", "老師講解",
                    "易錯點", "教學提示", "練習"]


def _title_source(title):
    """'照做 · Lay 1.1 Exercise 1' → ('照做', 'Lay 1.1 Exercise 1')。"""
    head, _, src = title.partition("·")
    return head.strip(), src.strip()


def _subparts(body, path, where, allowed):
    """#### 小節切段 → {None: 本文, '解答': …, '備註': …}。"""
    parts = {}
    for t, b in split_sections(body, 4):
        if t is not None and t not in allowed:
            raise ContentError(f"{path}: 「### {where}」底下只能有 "
                               f"{'、'.join('#### ' + a for a in allowed)},得到「#### {t}」")
        parts[t] = b
    return parts


def _walkthroughs(text, path, figdir):
    out = []
    for title, body in split_sections(text, 3):
        if title is None:
            if body.strip():
                raise ContentError(f"{path}: 「## 老師講解」要用 ### 例 1、### 例 2 分題")
            continue
        label, source = _title_source(title)
        parts = _subparts(body, path, title, ["備註"])
        main = parts.get(None, "")
        m = re.search(r"^1\.\s", main, re.M)
        if not m:
            raise ContentError(f"{path}: 「### {title}」沒有逐步講解(1. 2. 3. 的編號清單)")
        stem, steps = main[:m.start()], main[m.start():]
        if not stem.strip():
            raise ContentError(f"{path}: 「### {title}」缺題幹(寫在編號清單之前)")
        if len(re.findall(r"^\d+\.\s", steps, re.M)) < 2:
            raise ContentError(f"{path}: 「### {title}」的講解至少要兩步")
        out.append(Walkthrough(label, source, render(stem, figdir), render(steps, figdir),
                               render(parts.get("備註", ""))))
    if not out:
        raise ContentError(f"{path}: 「## 老師講解」至少要有一題 ### 例")
    return out


def _glossary(text, path):
    head, rows = pipe_table(text, path, "名詞對照")
    if len(head) != 3:
        raise ContentError(f"{path}: 「名詞對照」表格要三欄:English | 中文 | 說明")
    return [[render_inline(c) for c in r] for r in rows]


def _drills(text, path, figdir):
    out = []
    for title, body in split_sections(text, 3):
        if title is None:
            if body.strip():
                raise ContentError(f"{path}: 「## 練習」要用 ### 照做 / 是非 / 變化 / 應用 / 挑戰 分題")
            continue
        tier, source = _title_source(title)
        if tier not in TIER_OF:
            raise ContentError(f"{path}: 練習標題開頭只能是 {'/'.join(TIER_OF)},得到「### {title}」")
        parts = _subparts(body, path, title, ["解答", "備註"])
        stem, sol = parts.get(None, ""), parts.get("解答", "")
        if not stem.strip() or not sol.strip():
            raise ContentError(f"{path}: 「### {title}」要有題幹與 #### 解答")
        out.append(Drill(TIER_OF[tier], source, render(stem, figdir), render(sol, figdir),
                         render(parts.get("備註", ""))))
    if not out:
        raise ContentError(f"{path}: 「## 練習」至少要有一題")
    if out[0].tier != "do":
        raise ContentError(f"{path}: 練習第一題必須是「照做」")
    for a, b in zip(out, out[1:]):
        if TIER_RANK[b.tier] < TIER_RANK[a.tier]:
            raise ContentError(f"{path}: 練習順序必須是 {TIER_ORDER_ZH},"
                               f"出現 {TIER_ZH[a.tier]} → {TIER_ZH[b.tier]}")
    return out


def load_concept(path, figures_dir):
    try:
        return _load_concept(path, figures_dir)
    except ContentError as e:           # mdtools 丟出的錯誤不帶檔名,這裡補上
        msg = str(e)
        raise ContentError(msg if msg.startswith(path) else f"{path}: {msg}")


def _load_concept(path, figdir):
    meta, body = split_front_matter(_read(path), path)
    _need(meta, ["title_en", "title_zh", "level"], path)
    if meta["level"] not in LEVEL_ZH:
        raise ContentError(f"{path}: level 只能是 basic/mid/hard,得到 {meta['level']!r}")
    if "figure" in meta:
        raise ContentError(f"{path}: front matter 的 figure 已停用,改在段落裡寫 ![圖說](檔名.svg)")
    s = _sections(body, path, CONCEPT_SECTIONS, CONCEPT_REQUIRED)

    def r(name):
        return render(s.get(name, ""), figdir)

    return Concept(
        slug=os.path.splitext(os.path.basename(path))[0],
        title_en=meta["title_en"], title_zh=meta["title_zh"],
        sub=render_inline(meta.get("sub", "")), level=meta["level"],
        source=str(meta.get("source", "")), supplement=bool(meta.get("supplement", False)),
        lab_hook=render_inline(meta.get("lab_hook", "")),
        idea=r("觀念"), glossary=_glossary(s["名詞對照"], path), plain=r("白話說"),
        geometry=r("幾何意義"), cs_use=r("在資工哪裡用"), applications=r("實際應用"),
        numerical=r("數值筆記"), reasonable=r("合理性檢查"), deep=r("原理"),
        walkthroughs=_walkthroughs(s["老師講解"], path, figdir),
        misstep=r("易錯點"), teach_tip=r("教學提示"),
        drills=_drills(s["練習"], path, figdir), checks=_checks(s.get("驗算"), path))


def week_glossary(concepts):
    """整週的名詞對照:依出現順序,英文相同只留第一次,並附上出自哪個觀念。"""
    seen, out = set(), []
    for i, c in enumerate(concepts, 1):
        for en, zh, note in c.glossary:
            key = re.sub(r"<[^>]+>", "", en).strip().lower()
            if key not in seen:
                seen.add(key)
                out.append([en, zh, note, f"觀念 {i}"])
    return out


# ---------------------------------------------------------------- 證明時刻

def load_proof(path, n_concepts):
    meta, body = split_front_matter(_read(path), path)
    _need(meta, ["after", "title_zh"], path)
    if not (isinstance(meta["after"], int) and 1 <= meta["after"] <= n_concepts):
        raise ContentError(f"{path}: after 必須是 1–{n_concepts} 的整數(接在第幾個觀念之後)")
    names = ["定理", "為什麼值得證", "關鍵想法", "證明", "驗算"]
    s = _sections(body, path, names, names[:-1])
    return ProofMoment(meta["after"], meta["title_zh"], render(s["定理"]), render(s["為什麼值得證"]),
                       render(s["關鍵想法"]), render(s["證明"]), _checks(s.get("驗算"), path))


# ---------------------------------------------------------------- 診斷考 / 先備檢測

def _traps(text, path, where):
    out = []
    for it in list_items(text):
        m = re.match(r"\*\*(.+?)\*\*\s*(.+?)\s*→\s*(.+)$", it, re.S)
        if not m:
            raise ContentError(f"{path}: {where} 的迷思對照格式是「- **選項或錯答** 迷思 → 回去看哪裡」,"
                               f"得到:{it[:50]}")
        out.append(Trap(m.group(1).strip(), render_inline(m.group(2)), render_inline(m.group(3))))
    return out


def load_quiz(path, n_concepts):
    meta, body = split_front_matter(_read(path), path)
    _need(meta, ["kind", "when", "minutes"], path)
    items, checks = [], []
    for title, text in split_sections(body, 2):
        if title is None:
            continue
        if title == "驗算":
            checks = _checks(text, path)
            continue
        m = re.fullmatch(r"Q(\d+)\s*·\s*(觀念\s*(\d+)|先備)", title)
        if not m:
            raise ContentError(f"{path}: 題目標題要寫成「## Q1 · 觀念 1」或「## Q1 · 先備」,得到「## {title}」")
        where = f"Q{m.group(1)}"
        if m.group(3) and not 1 <= int(m.group(3)) <= n_concepts:
            raise ContentError(f"{path}: {where} 對應的觀念 {m.group(3)} 不存在(本週只有 {n_concepts} 個)")
        subs = dict(split_sections(text, 3))
        extra = set(subs) - {None, "答案", "為什麼", "迷思對照"}
        if extra:
            raise ContentError(f"{path}: {where} 底下只能有 ### 答案 / 為什麼 / 迷思對照,多了 {extra}")
        for need in ("答案", "為什麼", "迷思對照"):
            if not subs.get(need, "").strip():
                raise ContentError(f"{path}: {where} 缺 ### {need}")
        head = subs.get(None, "")
        choices, stem_lines = [], []
        for line in head.split("\n"):
            c = re.match(r"^-\s+([A-F])\.\s+(.*)", line)
            if c:
                choices.append(Choice(c.group(1), render_inline(c.group(2))))
            else:
                stem_lines.append(line)
        if not "\n".join(stem_lines).strip():
            raise ContentError(f"{path}: {where} 缺題幹")
        traps = _traps(subs["迷思對照"], path, where)
        answer = subs["答案"].strip()
        if choices:
            letters = [c.letter for c in choices]
            if letters != [chr(ord("A") + i) for i in range(len(letters))]:
                raise ContentError(f"{path}: {where} 選項要從 A 依序排,得到 {letters}")
            if answer not in letters:
                raise ContentError(f"{path}: {where} 的答案 {answer!r} 不是選項之一")
            wrong = set(letters) - {answer}
            keys = {t.key for t in traps}
            if keys != wrong:
                raise ContentError(f"{path}: {where} 每個錯誤選項都要對應一個迷思:"
                                   f"缺 {sorted(wrong - keys)},多 {sorted(keys - wrong)}")
            traps.sort(key=lambda t: t.key)
        else:
            answer = render_inline(answer)
            for t in traps:
                t.key = render_inline(t.key)
        items.append(QuizItem(re.sub(r"\s+", " ", m.group(2)), render("\n".join(stem_lines)),
                              choices, answer, render(subs["為什麼"]), traps))
    if not items:
        raise ContentError(f"{path}: 沒有任何題目")
    return Quiz(meta["kind"], meta["when"], int(meta["minutes"]), items, checks)


# ---------------------------------------------------------------- 理論教案

LESSON_SECTIONS = ["開場鉤子", "快轉表", "學習目標", "節奏表", "證明時刻",
                   "逐段講法", "迷思清單", "出門檢核", "作業與預習"]


def _minutes(span, path):
    m = re.fullmatch(r"(\d+):(\d+)\s*[–\-—]\s*(\d+):(\d+)", span.strip())
    if not m:
        raise ContentError(f"{path}: 節奏表的時間要寫成 00:15–00:45,得到 {span!r}")
    a, b, c, d = map(int, m.groups())
    return (c * 60 + d) - (a * 60 + b)


def load_lesson(path):
    _, body = split_front_matter(_read(path), path)
    s = _sections(body, path, LESSON_SECTIONS, LESSON_SECTIONS)
    ff_head, ff = pipe_table(s["快轉表"], path, "快轉表")
    ck_head, ck = pipe_table(s["節奏表"], path, "節奏表")
    total = sum(_minutes(r[0], path) for r in ck)
    if total != 180:
        raise ContentError(f"{path}: 節奏表合計 {total} 分,必須剛好 180")
    script = [(render_inline(t), render(b)) for t, b in split_sections(s["逐段講法"], 3) if t]
    exit_check = [(render_inline(t), render(b)) for t, b in split_sections(s["出門檢核"], 3) if t]
    if not script or not exit_check:
        raise ContentError(f"{path}: 「逐段講法」與「出門檢核」都要用 ### 分小節")
    cells = lambda rows: [[render_inline(c) for c in r] for r in rows]
    return Lesson(
        hook=render_inline(s["開場鉤子"]),
        fastforward=([render_inline(h) for h in ff_head], cells(ff)),
        outcomes=[render_inline(i) for i in list_items(s["學習目標"])],
        clock=([render_inline(h) for h in ck_head], cells(ck)),
        proof_moment=render(s["證明時刻"]), script=script,
        myths=[render_inline(i) for i in list_items(s["迷思清單"])],
        exit_check=exit_check,
        homework=[render_inline(i) for i in list_items(s["作業與預習"])])


# ---------------------------------------------------------------- 實作

def load_lab(path):
    _, body = split_front_matter(_read(path), path)
    steps, checks = [], []
    for title, text in split_sections(body, 2):
        if title is None:
            continue
        if title == "驗算":
            checks = _checks(text, path)
            continue
        m = re.fullmatch(r"([①②③④])\s*\S*\s*·\s*(.+)", title)
        if not m:
            raise ContentError(f"{path}: 步驟標題要寫成「## ① 預測 · 標題」(①②③④ 對應 預測/計算/解讀/應用),"
                               f"得到「## {title}」")
        stage = STAGE_OF[m.group(1)]
        code = todo = expected = ""
        for info, src in fenced_blocks(text):
            if info == "python":
                if code:
                    raise ContentError(f"{path}: 「{title}」只能有一個 ```python 區塊(練習放 ```python todo)")
                code = src.rstrip("\n")
            elif info == "python todo":
                todo = src.rstrip("\n")
                n = sum(1 for l in todo.split("\n") if l.strip().startswith("# TODO"))
                if n != 1:
                    raise ContentError(f"{path}: 「{title}」的 todo 區塊要剛好一行 # TODO 開頭,得到 {n} 行")
            elif info in ("text", "text expected"):
                expected = src.rstrip("\n")
            else:
                raise ContentError(f"{path}: 「{title}」不認得的程式區塊 ```{info}")
        if not code and not todo:
            raise ContentError(f"{path}: 「{title}」沒有程式區塊")
        # 第一個程式區塊之前的文字是引言,之後的文字是「會看到」
        first = re.search(r"^(```|~~~)", text, re.M)
        intro_md = text[:first.start()] if first else text
        after_md = strip_fences(text[first.start():]) if first else ""
        steps.append(LabStep(stage, render_inline(m.group(2)), render(intro_md), code,
                             expected, render(after_md), todo, intro_md.strip(), after_md.strip()))
    if not steps:
        raise ContentError(f"{path}: 沒有任何步驟")
    for a, b in zip(steps, steps[1:]):
        if STAGE_RANK[b.stage] < STAGE_RANK[a.stage]:
            raise ContentError(f"{path}: 步驟順序必須是 ① → ② → ③ → ④,「{b.title}」放錯位置")
    missing = set(STAGE_RANK) - {s.stage for s in steps}
    if missing:
        raise ContentError(f"{path}: 缺少階段 {'、'.join(STAGE_ZH[x] for x in sorted(missing, key=STAGE_RANK.get))}")
    return steps, checks


# ---------------------------------------------------------------- 週 / 課程

def load_course():
    path = os.path.join(CONTENT, "course.yaml")
    with open(path, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    for k in ("name", "dot", "book", "audience", "lab_setup", "outline"):
        if k not in c:
            raise ContentError(f"{_rel(path)}: 缺 {k}")
    intro = os.path.join(CONTENT, "index.md")
    c["intro"] = render(_read(intro)) if os.path.exists(intro) else ""
    return c


def week_dir(wk):
    return os.path.join(CONTENT, f"week{wk:02d}")


def load_week(wk):
    d = week_dir(wk)
    wp = os.path.join(d, "week.md")
    meta, _ = split_front_matter(_read(wp), wp)
    _need(meta, ["num", "title", "subtitle", "sections"], wp)
    if meta["num"] != wk:
        raise ContentError(f"{_rel(wp)}: num 是 {meta['num']},但資料夾是第 {wk} 週")
    figs = os.path.join(d, "figures")
    concepts = [load_concept(p, figs) for p in sorted(glob.glob(os.path.join(d, "[0-9][0-9]-*.md")))]
    opt = lambda name: os.path.join(d, name) if os.path.exists(os.path.join(d, name)) else None
    proof = load_proof(opt("proof.md"), len(concepts)) if opt("proof.md") else None
    lab, lab_checks = load_lab(opt("lab.md")) if opt("lab.md") else ([], [])
    return Week(
        num=wk, title=meta["title"], subtitle=render_inline(meta["subtitle"]),
        sections=meta["sections"], pages=str(meta.get("pages", "")),
        chips=list(meta.get("chips", [])), concepts=concepts, proof=proof,
        lesson=load_lesson(opt("lesson.md")) if opt("lesson.md") else None,
        quiz=load_quiz(opt("quiz.md"), len(concepts)) if opt("quiz.md") else None,
        prereq=load_quiz(opt("prereq.md"), len(concepts)) if opt("prereq.md") else None,
        lab=lab, lab_checks=lab_checks)


def available_weeks():
    return sorted(int(m.group(1)) for p in glob.glob(os.path.join(CONTENT, "week*"))
                  if (m := re.search(r"week(\d+)$", p)) and os.path.exists(os.path.join(p, "week.md")))


def all_checks(week):
    out = [x for c in week.concepts for x in c.checks]
    for part in (week.proof, week.quiz, week.prereq):
        if part is not None:
            out += part.checks
    return out + week.lab_checks
