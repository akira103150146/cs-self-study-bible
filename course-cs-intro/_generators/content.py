# -*- coding: utf-8 -*-
"""content/ 底下的 Markdown → 結構化資料(已轉好的 HTML 片段)。

這一層只管「內容長什麼樣、有沒有缺」,不管排版。
格式不合就丟 ContentError(帶檔名),在產出任何 HTML 之前擋下來。
各檔的寫法見 content/README.md。所有函式的第一個參數 root 是課程資料夾。
"""
import glob
import os
import re
from dataclasses import dataclass, field

import yaml

from mdtools import (ContentError, fenced_blocks, list_items, pipe_table, render,
                     render_inline, split_front_matter, split_sections)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LEVEL_ZH = {"basic": "基礎", "mid": "進階", "hard": "挑戰"}
QTYPES = ("計算", "選擇", "簡答")
TIER_OF = {"照做": "do", "是非": "tf", "變化": "vary", "應用": "app", "挑戰": "challenge"}
TIER_ZH = {v: k for k, v in TIER_OF.items()}
TIER_RANK = {"do": 1, "tf": 2, "vary": 3, "app": 4, "challenge": 5}
TIER_ORDER_ZH = " → ".join(TIER_OF)
LANGS = ("c", "python", "mixed")

CID = r"C\d+\.\d+"
QHEAD = re.compile(r"Q(\d+)\s*·\s*(" + CID + r")\s*·\s*(計算|選擇|簡答)\s*·\s*(basic|mid|hard)\s*·\s*(\d+)")
TASKHEAD = re.compile(r"任務\s*(\d+)\s*·\s*(.+?)\s*·\s*(" + CID + r"(?:\s*,\s*" + CID + r")*)")
PROJHEAD = re.compile(r"專案\s*(\d+)\s*·\s*(.+?)\s*·\s*(" + CID + r"(?:\s*,\s*" + CID + r")*)")


# ---------------------------------------------------------------- 資料結構

@dataclass
class Check:
    label: str
    expr: str
    answer: object = None   # 題庫計算題:### 答案 的純文字;觀念檔:None


@dataclass
class Walkthrough:
    label: str
    stem: str
    steps: str
    note: str = ""


@dataclass
class Drill:
    tier: str
    stem: str
    sol: str
    note: str = ""
    parts: int = 1


@dataclass
class Concept:
    id: str
    slug: str
    title_en: str
    title_zh: str
    sub: str
    level: str
    supplement: bool
    lab_hook: str
    idea: str
    glossary: list
    plain: str
    followup: str
    modern: str
    deep: str
    walkthroughs: list
    misstep: str
    teach_tip: str
    drills: list
    checks: list = field(default_factory=list)


@dataclass
class Choice:
    letter: str
    text: str


@dataclass
class Trap:
    key: str
    myth: str
    lookback: str


@dataclass
class BankItem:
    qid: int
    concept: str
    qtype: str
    level: str
    points: int
    stem: str
    choices: list
    answer: str
    answer_text: str
    explain: str
    traps: list
    rubric: str
    checks: list = field(default_factory=list)


@dataclass
class LabTask:
    num: int
    title: str
    concepts: list
    body: str


@dataclass
class Lab:
    lang: str
    dir: str
    overview: str
    env: str
    tasks: list
    submit: str


@dataclass
class Project:
    num: int
    title: str
    concepts: list
    goal: str
    spec: str
    rubric: tuple
    extend: str


@dataclass
class Chapter:
    num: int
    title: str
    title_zh: str
    subtitle: str
    part: str
    book: str
    lang: str
    followups: list
    concepts: list
    bank: list
    lab: object
    projects: list


# ---------------------------------------------------------------- 共用

def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _rel(root, path):
    return os.path.relpath(path, root).replace("\\", "/")


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


def _subsections(body, path, where, allowed, required):
    """### 小節切段 → {None: 本文, 標題: 內文}。"""
    got = {}
    for t, b in split_sections(body, 3):
        if t is not None and t not in allowed:
            raise ContentError(f"{path}: {where} 底下只能有 {'、'.join('### ' + a for a in allowed)},"
                               f"得到「### {t}」")
        got[t] = b
    for need in required:
        if not got.get(need, "").strip():
            raise ContentError(f"{path}: {where} 缺 ### {need}")
    return got


def _need(meta, keys, path):
    missing = [k for k in keys if not str(meta.get(k, "")).strip()]
    if missing:
        raise ContentError(f"{path}: front matter 缺 {', '.join(missing)}")


def _checks(text, label_prefix, path, answer=None):
    """## 驗算 / ### 驗算 裡 ```check 區塊的每一行 → [Check]。# 開頭是註解。"""
    out = []
    for info, code in fenced_blocks(text or ""):
        if info != "check":
            raise ContentError(f"{path}: 驗算的程式區塊要標成 ```check,得到 ```{info}")
        for line in code.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                out.append(Check(f"{label_prefix} · {line[:70]}", line, answer))
    return out


def _ids(s):
    return [x.strip() for x in s.split(",")]


# ---------------------------------------------------------------- 觀念

CONCEPT_SECTIONS = ["觀念", "名詞對照", "白話說", "後面會用到", "現代補充", "原理",
                    "老師講解", "易錯點", "教學提示", "練習", "驗算"]
CONCEPT_REQUIRED = ["觀念", "名詞對照", "白話說", "後面會用到", "原理", "老師講解",
                    "易錯點", "教學提示", "練習"]

# 小題標號(沿用線代):行內 (a)、(15);清單 - **a.** …
LABEL = r"(\d{1,2}[a-z]?|[a-h])"
SUBPART = re.compile(r"(?:^|\s)\(" + LABEL + r"\)(?=\s)")
SUBPART_LIST = re.compile(r"(?m)^\s*[-*]\s+\*\*" + LABEL + r"\.\*\*"
                          r"|<li>\s*(?:<p>\s*)?<strong>" + LABEL + r"\.</strong>")


def count_parts(src):
    """題幹(Markdown 或 HTML)裡有幾個不同的小題標號;沒有就是 1。verify.py 也用這個。"""
    src = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", " ", src, flags=re.S)
    labels = {a or b for a, b in SUBPART_LIST.findall(src)}
    prose = re.sub(r"<[^>]+>", " ", src)
    labels |= set(SUBPART.findall(prose))
    return max(1, len(labels))


def _parts4(body, path, where, allowed):
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
        parts = _parts4(body, path, title, ["備註"])
        main = parts.get(None, "")
        m = re.search(r"^1\.\s", main, re.M)
        if not m:
            raise ContentError(f"{path}: 「### {title}」沒有逐步講解(1. 2. 3. 的編號清單)")
        stem, steps = main[:m.start()], main[m.start():]
        if not stem.strip():
            raise ContentError(f"{path}: 「### {title}」缺題幹(寫在編號清單之前)")
        if len(re.findall(r"^\d+\.\s", steps, re.M)) < 2:
            raise ContentError(f"{path}: 「### {title}」的講解至少要兩步")
        out.append(Walkthrough(title.strip(), render(stem, figdir), render(steps, figdir),
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
        tier = title.split("·")[0].strip()
        if tier not in TIER_OF:
            raise ContentError(f"{path}: 練習標題開頭只能是 {'/'.join(TIER_OF)},得到「### {title}」")
        parts = _parts4(body, path, title, ["解答", "備註"])
        stem, sol = parts.get(None, ""), parts.get("解答", "")
        if not stem.strip() or not sol.strip():
            raise ContentError(f"{path}: 「### {title}」要有題幹與 #### 解答")
        out.append(Drill(TIER_OF[tier], render(stem, figdir), render(sol, figdir),
                         render(parts.get("備註", "")), count_parts(stem)))
    if not out:
        raise ContentError(f"{path}: 「## 練習」至少要有一題")
    if out[0].tier != "do":
        raise ContentError(f"{path}: 練習第一題必須是「照做」")
    for a, b in zip(out, out[1:]):
        if TIER_RANK[b.tier] < TIER_RANK[a.tier]:
            raise ContentError(f"{path}: 練習順序必須是 {TIER_ORDER_ZH},"
                               f"出現 {TIER_ZH[a.tier]} → {TIER_ZH[b.tier]}")
    return out


def load_concept(root, path, num, figdir):
    rel = _rel(root, path)
    try:
        return _load_concept(rel, path, num, figdir)
    except ContentError as e:           # mdtools 丟出的錯誤不帶檔名,這裡補上
        msg = str(e)
        raise ContentError(msg if msg.startswith(rel) else f"{rel}: {msg}")


def _load_concept(rel, path, num, figdir):
    meta, body = split_front_matter(_read(path), rel)
    _need(meta, ["id", "title_en", "title_zh", "level", "lab_hook"], rel)
    seq = int(os.path.basename(path)[:2])
    if meta["id"] != f"C{num}.{seq}":
        raise ContentError(f"{rel}: id 是 {meta['id']!r},依檔名與章號應該是 'C{num}.{seq}'")
    if meta["level"] not in LEVEL_ZH:
        raise ContentError(f"{rel}: level 只能是 basic/mid/hard,得到 {meta['level']!r}")
    s = _sections(body, rel, CONCEPT_SECTIONS, CONCEPT_REQUIRED)

    def r(name):
        return render(s.get(name, ""), figdir)

    return Concept(
        id=meta["id"], slug=os.path.splitext(os.path.basename(path))[0],
        title_en=meta["title_en"], title_zh=meta["title_zh"],
        sub=render_inline(meta.get("sub", "")), level=meta["level"],
        supplement=bool(meta.get("supplement", False)),
        lab_hook=render_inline(meta["lab_hook"]),
        idea=r("觀念"), glossary=_glossary(s["名詞對照"], rel), plain=r("白話說"),
        followup=r("後面會用到"), modern=r("現代補充"), deep=r("原理"),
        walkthroughs=_walkthroughs(s["老師講解"], rel, figdir),
        misstep=r("易錯點"), teach_tip=r("教學提示"),
        drills=_drills(s["練習"], rel, figdir),
        checks=_checks(s.get("驗算"), rel, rel))


def chapter_glossary(concepts):
    """整章的名詞對照:依出現順序,英文相同只留第一次,並附上出自哪個觀念。"""
    seen, out = set(), []
    for c in concepts:
        for en, zh, note in c.glossary:
            key = re.sub(r"<[^>]+>", "", en).strip().lower()
            if key not in seen:
                seen.add(key)
                out.append([en, zh, note, c.id])
    return out


# ---------------------------------------------------------------- 題庫

def _traps(text, path, where):
    out = []
    for it in list_items(text):
        m = re.match(r"\*\*(.+?)\*\*\s*(.+?)\s*→\s*(.+)$", it, re.S)
        if not m:
            raise ContentError(f"{path}: {where} 的迷思對照格式是「- **B** 迷思 → 回看 C3.2」,得到:{it[:50]}")
        out.append(Trap(m.group(1).strip(), render_inline(m.group(2)), render_inline(m.group(3))))
    return out


def _load_bank(root, path, concept_ids, figdir):
    rel = _rel(root, path)
    _, body = split_front_matter(_read(path), rel)
    items = []
    for title, text in split_sections(body, 2):
        if title is None:
            if text.strip():
                raise ContentError(f"{rel}: 第一題之前有文字:{text.strip()[:40]}")
            continue
        m = QHEAD.fullmatch(title.strip())
        if not m:
            raise ContentError(f"{rel}: 題目標題要寫成「## Q1 · C3.2 · 計算 · basic · 4」,得到「## {title}」")
        qid, cid, qtype, level, points = int(m.group(1)), m.group(2), m.group(3), m.group(4), int(m.group(5))
        where = f"Q{qid}"
        if qid != len(items) + 1:
            raise ContentError(f"{rel}: 題號要從 Q1 連號,{where} 應該是 Q{len(items) + 1}")
        if cid not in concept_ids:
            raise ContentError(f"{rel}: {where} 的觀念 {cid} 不存在(本章有 {', '.join(concept_ids)})")
        if not 1 <= points <= 20:
            raise ContentError(f"{rel}: {where} 配分要在 1–20 之間,得到 {points}")
        required = {"計算": ["答案", "詳解", "驗算"], "選擇": ["答案", "詳解", "迷思對照"],
                    "簡答": ["答案", "詳解", "評分要點"]}[qtype]
        subs = _subsections(text, rel, where, ["答案", "詳解", "迷思對照", "評分要點", "驗算"], required)
        head = subs.get(None, "")
        choices, stem_lines = [], []
        for line in head.split("\n"):
            c = re.match(r"^-\s+([A-F])\.\s+(.*)", line)
            if c:
                choices.append(Choice(c.group(1), render_inline(c.group(2))))
            else:
                stem_lines.append(line)
        if not "\n".join(stem_lines).strip():
            raise ContentError(f"{rel}: {where} 缺題幹")
        answer_md = subs["答案"].strip()
        answer_text = re.sub(r"`", "", answer_md).strip()
        traps = []
        if qtype == "選擇":
            letters = [c.letter for c in choices]
            if len(letters) < 2 or letters != [chr(ord("A") + i) for i in range(len(letters))]:
                raise ContentError(f"{rel}: {where} 選擇題的選項要從 A 依序排,至少兩個,得到 {letters}")
            if answer_text not in letters:
                raise ContentError(f"{rel}: {where} 的答案 {answer_text!r} 不是選項之一")
            traps = _traps(subs["迷思對照"], rel, where)
            wrong, keys = set(letters) - {answer_text}, {t.key for t in traps}
            if keys != wrong:
                raise ContentError(f"{rel}: {where} 每個錯誤選項都要對應一個迷思:"
                                   f"缺 {sorted(wrong - keys)},多 {sorted(keys - wrong)}")
            traps.sort(key=lambda t: t.key)
            answer = answer_text
        else:
            if choices:
                raise ContentError(f"{rel}: {where} 是{qtype}題,不能有 - A. 選項")
            answer = render(answer_md, figdir)
        checks = _checks(subs.get("驗算"), f"{rel} {where}", rel,
                         answer_text if qtype == "計算" else None)
        if qtype == "計算" and not any(re.search(r"\bANS\b", c.expr) for c in checks):
            raise ContentError(f"{rel}: {where} 計算題的驗算要至少一行用到 ANS(拿題目印的答案來比對)")
        items.append(BankItem(qid, cid, qtype, level, points, render("\n".join(stem_lines), figdir),
                              choices, answer, answer_text, render(subs["詳解"], figdir), traps,
                              render(subs.get("評分要點", "")), checks))
    if not items:
        raise ContentError(f"{rel}: 題庫沒有任何題目")
    return items


# ---------------------------------------------------------------- Lab / 專案

def _load_lab(root, path, concept_ids):
    rel = _rel(root, path)
    meta, body = split_front_matter(_read(path), rel)
    _need(meta, ["lang", "dir"], rel)
    if meta["lang"] not in LANGS:
        raise ContentError(f"{rel}: lang 只能是 {'/'.join(LANGS)}")
    fixed, tasks = {}, []
    for title, text in split_sections(body, 2):
        if title is None:
            if text.strip():
                raise ContentError(f"{rel}: 第一個 ## 之前有文字")
            continue
        if title in ("概要", "環境", "繳交"):
            fixed[title] = text
            continue
        m = TASKHEAD.fullmatch(title.strip())
        if not m:
            raise ContentError(f"{rel}: 不認得的段落「## {title}」;任務標題要寫成「## 任務 1 · 標題 · C3.2, C3.3」")
        num, ids = int(m.group(1)), _ids(m.group(3))
        if num != len(tasks) + 1:
            raise ContentError(f"{rel}: 任務要從 1 連號,「{title}」應該是任務 {len(tasks) + 1}")
        bad = [i for i in ids if i not in concept_ids]
        if bad:
            raise ContentError(f"{rel}: 任務 {num} 的觀念 {bad} 不存在")
        if not any(info in ("c interface", "python interface") for info, _ in fenced_blocks(text)):
            raise ContentError(f"{rel}: 任務 {num} 要有一個 ```c interface 或 ```python interface 區塊")
        body_md = re.sub(r"^(```|~~~)(c|python) interface[ \t]*$", r"\1\2", text, flags=re.M)
        tasks.append(LabTask(num, render_inline(m.group(2)), ids, render(body_md)))
    for need in ("概要", "環境", "繳交"):
        if not fixed.get(need, "").strip():
            raise ContentError(f"{rel}: 缺少段落 ## {need}")
    if not tasks:
        raise ContentError(f"{rel}: 至少要有一個 ## 任務")
    return Lab(meta["lang"], meta["dir"], render(fixed["概要"]), render(fixed["環境"]), tasks,
               render(fixed["繳交"]))


def _load_projects(root, path, concept_ids):
    rel = _rel(root, path)
    _, body = split_front_matter(_read(path), rel)
    out = []
    for title, text in split_sections(body, 2):
        if title is None:
            if text.strip():
                raise ContentError(f"{rel}: 第一個專案之前有文字")
            continue
        m = PROJHEAD.fullmatch(title.strip())
        if not m:
            raise ContentError(f"{rel}: 專案標題要寫成「## 專案 1 · 標題 · C3.6」,得到「## {title}」")
        num, ids = int(m.group(1)), _ids(m.group(3))
        where = f"專案 {num}"
        if num != len(out) + 1:
            raise ContentError(f"{rel}: 專案要從 1 連號")
        bad = [i for i in ids if i not in concept_ids]
        if bad:
            raise ContentError(f"{rel}: {where} 的觀念 {bad} 不存在")
        subs = _subsections(text, rel, where, ["目標", "規格", "評分規準", "延伸方向"],
                            ["目標", "規格", "評分規準"])
        head, rows = pipe_table(subs["評分規準"], rel, f"{where} 評分規準")
        if head != ["項目", "配分", "通過標準"]:
            raise ContentError(f"{rel}: {where} 的評分規準表頭要是 項目 | 配分 | 通過標準")
        out.append(Project(num, render_inline(m.group(2)), ids, render(subs["目標"]), render(subs["規格"]),
                           (head, [[render_inline(c) for c in r] for r in rows]),
                           render(subs.get("延伸方向", ""))))
    return out


# ---------------------------------------------------------------- 章 / 課程

def load_course(root=ROOT):
    path = os.path.join(root, "content", "course.yaml")
    with open(path, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    for k in ("name", "dot", "book", "audience", "tagline", "parts", "outline"):
        if k not in c:
            raise ContentError(f"{_rel(root, path)}: 缺 {k}")
    for n, entry in c["outline"].items():
        if not (isinstance(entry, list) and len(entry) == 2):
            raise ContentError(f"{_rel(root, path)}: outline 第 {n} 章要寫成 [英文標題, 中文說明],得到 {entry!r}"
                               "(標題裡有逗號時要加引號)")
    intro = os.path.join(root, "content", "index.md")
    c["intro"] = render(_read(intro)) if os.path.exists(intro) else ""
    return c


def chapter_dir(root, num):
    return os.path.join(root, "content", f"ch{num:02d}")


def available_chapters(root=ROOT):
    return sorted(int(m.group(1)) for p in glob.glob(os.path.join(root, "content", "ch*"))
                  if (m := re.search(r"ch(\d+)$", p)) and os.path.exists(os.path.join(p, "chapter.md")))


def load_chapter(root, num):
    d = chapter_dir(root, num)
    cp = os.path.join(d, "chapter.md")
    rel = _rel(root, cp)
    meta, _ = split_front_matter(_read(cp), rel)
    _need(meta, ["num", "title", "title_zh", "subtitle", "part", "book", "lang", "followups"], rel)
    if meta["num"] != num:
        raise ContentError(f"{rel}: num 是 {meta['num']},但資料夾是第 {num} 章")
    if meta["lang"] not in LANGS:
        raise ContentError(f"{rel}: lang 只能是 {'/'.join(LANGS)}")
    figs = os.path.join(d, "figures")
    concepts = [load_concept(root, p, num, figs)
                for p in sorted(glob.glob(os.path.join(d, "[0-9][0-9]-*.md")))]
    ids = [c.id for c in concepts]
    opt = lambda name: os.path.join(d, name) if os.path.exists(os.path.join(d, name)) else None
    return Chapter(
        num=num, title=meta["title"], title_zh=meta["title_zh"],
        subtitle=render_inline(meta["subtitle"]), part=meta["part"], book=meta["book"],
        lang=meta["lang"], followups=list(meta["followups"]), concepts=concepts,
        bank=_load_bank(root, opt("bank.md"), ids, figs) if opt("bank.md") else [],
        lab=_load_lab(root, opt("lab.md"), ids) if opt("lab.md") else None,
        projects=_load_projects(root, opt("projects.md"), ids) if opt("projects.md") else [])


def all_checks(ch):
    out = [x for c in ch.concepts for x in c.checks]
    return out + [x for b in ch.bank for x in b.checks]
