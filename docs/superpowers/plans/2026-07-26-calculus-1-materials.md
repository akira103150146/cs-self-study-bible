# 微積分(一) 18 週教材 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 依 `docs/superpowers/specs/2026-07-26-calculus-1-course-design.md` 產出微積分(一) 18 週完整教材（每週理論教案／例題師生雙版／實作 notebook＋可讀頁），全部由版控中的產生器輸出。

**Architecture:** 內容與排版分離。每週的教學內容寫成純 Python 資料模組（`_generators/weeks/wNN.py`），三支 renderer（`build_lesson` / `build_examples` / `build_lab`）把資料轉成 HTML 與 ipynb。三支驗證腳本先行：`verify.py`（結構）、`verify_math.py`（sympy 驗算）、`run_notebooks.py`（headless 執行）。W1 做完即凍結為範本，W2–W18 只改資料不改 renderer。

**Tech Stack:** Python 3.12（標準庫 + sympy + numpy + matplotlib + scipy）、原生 HTML/CSS、MathJax 3（CDN）、Jupyter notebook 格式 v4。無前端框架、無建置工具。

## Global Constraints

- **產生器必須版控**：所有 `build_*.py` 放 `course-calculus-1/_generators/`，與產出一起 commit。禁止手改產出的 HTML/ipynb——要改內容改資料模組後重生。（銜接課的教訓：產生器遺失導致教材只能手改）
- **雙語規則**：觀念名稱用 `English｜中文` 格式、觀念核心陳述（idea）與**所有題目**（示範 `.ex` 與練習 `.drill`）用英文；原理證明 `.deep`、引導 `.guide`、提示 `.hint`、易錯點 `.misstep`、詳解 `.sol` / `.ans-body` 用中文。教案主體中文＋英文術語。
- **每個數值答案先用 sympy 驗過才寫**。
- **HTML 數學式的 `<` `>` `&` 一律跳脫**為 `&lt;` `&gt;` `&amp;`（用 `html.escape`）。
- **標點半形**：CJK 後接 `,` `:` `;` `?` `!`，與《CS 自學聖經》全書一致（本書 chapters 半形 9208 : 全形 1195）。
- **圖表標籤用英文**避免中文豆腐字；notebook 另附選用的中文字型設定格。
- **作答區高度**：教學講義 `.workspace` `min-height: 130px`；考卷依配分——4 分 132px、5 分 180px、6 分 240px、12 分 340–460px。
- **每週實作必須用到當週理論的核心結果**；找不到對應就用上週理論的深化應用，不硬湊。
- **證明時刻**：W1–W8、W10–W16 每週一個（共 15 個）；W9 期中考、W17 capstone、W18 總整理無。
- 檔名一律 `WN-*`，週資料夾 `week01`–`week18`（補零，與銜接課的 `week1` 不同，因為要排到 18）。

**參考範本**：`course-calculus-bridge/` 是同一套設計系統的已完成實例。`assets/handout.css`、`index.html`、`week1/W1-*.html` 是排版與語氣的黃金範例，實作時直接對照。

---

## File Structure

```
course-calculus-1/
  index.html                      # 課程首頁:18 張週卡（由 build_index.py 產出）
  assets/handout.css              # 從銜接課複製 + 本計畫的修正
  _generators/
    common.py                     # HTML 骨架、nav、masthead、escape、chip、callout
    weekdata.py                   # 資料類別定義(Concept/Drill/Lab/LessonPlan)
    build_lesson.py               # LessonPlan → WN-理論教案.html
    build_examples.py             # [Concept] → WN-例題-學生版.html + 教師版
    build_lab.py                  # [Lab] → WN-實作.html + WN-lab.ipynb
    build_exam.py                 # ExamPaper → 考卷版 + 詳解版(W9/W18 用)
    build_index.py                # 全部週資料 → index.html
    build_all.py                  # 一鍵重生所有週
    weeks/
      w01.py … w18.py             # 每週內容資料(唯一要編輯的地方)
    verify.py                     # 結構稽核
    verify_math.py                # sympy 驗算
    run_notebooks.py              # headless 執行所有 notebook
  week01/ … week18/
    WN-理論教案.html
    WN-例題-學生版.html
    WN-例題-教師版.html
    WN-實作.html
    WN-lab.ipynb
```

**責任邊界**：`weeks/wNN.py` 只有內容、零排版；`common.py` 只有排版、零內容；`build_*.py` 只做轉換。任何一週的內容改動都不該碰到 renderer。

---

### Task 1: 驗證工具先行

先有檢查器，才有內容。這三支腳本是後續每一個 task 的驗收閘門。

**Files:**
- Create: `course-calculus-1/_generators/verify.py`
- Create: `course-calculus-1/_generators/verify_math.py`
- Create: `course-calculus-1/_generators/run_notebooks.py`

**Interfaces:**
- Produces: `verify.py` 可用 `python _generators/verify.py [week...]` 執行，回傳 exit code 0/1，印出 `🔴`/`🟡` 問題清單。`verify_math.py` 提供 `check(expr_str, expected_str) -> bool`。`run_notebooks.py` 逐 cell exec 所有 ipynb，任一失敗回傳 exit 1。

- [ ] **Step 1: 寫 verify.py**

```python
# -*- coding: utf-8 -*-
"""結構稽核。用法: python _generators/verify.py [週次...]  (不給則全查)"""
import io, os, re, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISSUES = []

def add(sev, where, msg):
    ISSUES.append((sev, where, msg))

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()

def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

def concepts(s):
    return [b for b in re.split(r'(?=<div class="qtype">)', s) if b.startswith('<div class="qtype">')]

def titles(s):
    return re.findall(r'<h3 class="qtype-title">(.*?)</h3>', s)

def problems(b):
    return [strip_tags(x) for x in re.findall(r'<p class="problem">(.*?)</p>', b, re.S)]

def drills(b):
    m = re.search(r'<ol class="drill">(.*?)</ol>', b, re.S)
    if not m:
        return []
    out = []
    for it in re.split(r"<li>", m.group(1))[1:]:
        it = re.sub(r'<div class="ans-body">.*', "", it, flags=re.S).replace("</li>", "")
        out.append(strip_tags(it))
    return out

def check_pair(wk):
    """學生版 vs 教師版:題幹逐字相同、教師版每題有解答、學生版不洩答案。"""
    sp = f"week{wk:02d}/W{wk}-例題-學生版.html"
    tp = f"week{wk:02d}/W{wk}-例題-教師版.html"
    if not os.path.exists(os.path.join(ROOT, sp)):
        return
    S, T = rd(sp), rd(tp)
    cs, ct = concepts(S), concepts(T)
    if len(cs) != len(ct):
        add("RED", f"W{wk}", f"觀念數不一致 學生{len(cs)} vs 教師{len(ct)}")
    if titles(S) != titles(T):
        add("RED", f"W{wk}", "觀念標題兩版不一致")
    if S.count('class="ans-body"') or S.count('class="sol"'):
        add("RED", f"W{wk}", "學生版洩答案(出現 ans-body 或 sol)")
    for i, (a, b) in enumerate(zip(cs, ct), 1):
        if problems(a) != problems(b):
            add("RED", f"W{wk}", f"觀念{i} 示範題幹兩版不同")
        da, db = drills(a), drills(b)
        if da != db:
            add("RED", f"W{wk}", f"觀念{i} 練習題幹兩版不同({len(da)} vs {len(db)})")
        m = re.search(r'<ol class="drill">(.*?)</ol>', b, re.S)
        if m and m.group(1).count('class="ans-body"') != len(db):
            add("RED", f"W{wk}", f"觀念{i} 教師版解答數 != 題數")
        lv = re.findall(r'<span class="level (\w+)"', a)
        order = {"basic": 1, "mid": 2, "hard": 3}
        seq = [order.get(x, 0) for x in lv]
        if seq != sorted(seq):
            add("YEL", f"W{wk}", f"觀念{i} 難度非遞增: {lv}")

def check_bilingual(wk):
    """題幹必須全英文;觀念標題必須 English｜中文。"""
    sp = f"week{wk:02d}/W{wk}-例題-學生版.html"
    if not os.path.exists(os.path.join(ROOT, sp)):
        return
    S = rd(sp)
    cjk = re.compile(r"[\u4e00-\u9fff]")
    for i, b in enumerate(concepts(S), 1):
        for x in problems(b) + drills(b):
            if cjk.search(x):
                add("YEL", f"W{wk}", f"觀念{i} 題幹含中文: {x[:60]}")
    for t in titles(S):
        if "｜" not in t:
            add("YEL", f"W{wk}", f"qtype-title 未用 English｜中文: {t}")

def check_html(path):
    s = rd(path)
    body = s.split("<body>", 1)[-1]
    for m in re.finditer(r"(?<!\$)\$([^$\n]{1,300})\$(?!\$)", body):
        if "<" in m.group(1) or ">" in m.group(1):
            add("RED", path, f"數學式內未跳脫的 < 或 >: ${m.group(1)[:60]}$")
    for i, line in enumerate(body.split("\n"), 1):
        if re.sub(r"\$\$", "", line).count("$") % 2:
            add("YEL", path, f"第 {i} 行 $ 數量為奇數")
    d = os.path.dirname(os.path.join(ROOT, path))
    for h in re.findall(r'(?:href|src)="([^"#:]+\.(?:html|css|ipynb))"', s):
        if not os.path.exists(os.path.normpath(os.path.join(d, h))):
            add("RED", path, f"連結壞掉: {h}")
    if "例題-學生版" in path:
        if "min-height" not in rd("assets/handout.css").split(".workspace")[1][:200]:
            add("RED", "assets/handout.css", ".workspace 缺 min-height,學生印出來沒有作答空間")

def check_counts(wk):
    """實作頁 chip 宣稱的 Lab/TODO 數 == 頁面實印 == notebook。"""
    hp = f"week{wk:02d}/W{wk}-實作.html"
    nbp = f"week{wk:02d}/W{wk}-lab.ipynb"
    if not os.path.exists(os.path.join(ROOT, hp)):
        return
    import html as _html
    s = rd(hp)
    nb = json.loads(rd(nbp))
    page = sum(1 for p in re.findall(r"<pre[^>]*>(.*?)</pre>", s, re.S)
               for l in _html.unescape(re.sub("<[^>]+>", "", p)).split("\n")
               if l.strip().startswith("# TODO"))
    nbt = sum(1 for c in nb["cells"] if c["cell_type"] == "code"
              for l in "".join(c["source"]).split("\n") if l.strip().startswith("# TODO"))
    claim = re.search(r"(\d+)\s*題\s*TODO", s)
    if claim and int(claim.group(1)) != page:
        add("YEL", f"W{wk}", f"chip 宣稱 {claim.group(1)} 題 TODO,頁面實印 {page}")
    if page != nbt:
        add("YEL", f"W{wk}", f"實作頁 TODO {page} != notebook {nbt}")
    labs_page = len(re.findall(r"<h2[^>]*>Lab ", s))
    claim_lab = re.search(r"(\d+)\s*個\s*Lab", s)
    if claim_lab and int(claim_lab.group(1)) != labs_page:
        add("YEL", f"W{wk}", f"chip 宣稱 {claim_lab.group(1)} 個 Lab,頁面實有 {labs_page}")

def main():
    weeks = [int(a) for a in sys.argv[1:]] or list(range(1, 19))
    for wk in weeks:
        check_pair(wk)
        check_bilingual(wk)
        check_counts(wk)
    for p in sorted(glob.glob(os.path.join(ROOT, "week*", "*.html"))) + \
             ([os.path.join(ROOT, "index.html")] if os.path.exists(os.path.join(ROOT, "index.html")) else []):
        check_html(os.path.relpath(p, ROOT).replace("\\", "/"))
    for sev, where, msg in sorted(ISSUES, key=lambda x: (x[0] != "RED", x[1])):
        print(f"{'🔴' if sev == 'RED' else '🟡'} [{where}] {msg}")
    red = sum(1 for i in ISSUES if i[0] == "RED")
    print(f"\n共 {red} 紅 / {len(ISSUES) - red} 黃")
    return 1 if red else 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 跑 verify.py 確認它在空專案上正確通過（沒有檔案 = 沒有問題）**

```bash
cd course-calculus-1 && python _generators/verify.py
```
Expected: `共 0 紅 / 0 黃`，exit 0。

- [ ] **Step 3: 寫 verify_math.py**

```python
# -*- coding: utf-8 -*-
"""用 sympy 驗算答案。每週資料模組在 answers 欄位登記 (描述, 算式, 期望值)。"""
import sys, importlib, sympy as sp

def check(expr, expected, label=""):
    """expr/expected 為 sympy 可解析字串或 sympy 物件。相等回 True。"""
    a = sp.sympify(expr) if isinstance(expr, str) else expr
    b = sp.sympify(expected) if isinstance(expected, str) else expected
    ok = sp.simplify(a - b) == 0
    if not ok:
        try:
            ok = abs(complex(a) - complex(b)) < 1e-9
        except (TypeError, ValueError):
            ok = False
    print(f"  {'✅' if ok else '❌'} {label or expr}  ->  got {a}, want {b}")
    return ok

def main():
    weeks = [int(a) for a in sys.argv[1:]] or list(range(1, 19))
    bad = 0
    for wk in weeks:
        try:
            mod = importlib.import_module(f"weeks.w{wk:02d}")
        except ModuleNotFoundError:
            continue
        checks = getattr(mod, "ANSWER_CHECKS", [])
        print(f"=== W{wk}: {len(checks)} 項驗算 ===")
        for label, expr, expected in checks:
            if not check(expr, expected, label):
                bad += 1
    print(f"\n驗算失敗 {bad} 項")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 寫 run_notebooks.py**

```python
# -*- coding: utf-8 -*-
"""逐 cell 執行所有 notebook(Agg backend),任一失敗回傳 exit 1。"""
import io, os, sys, json, glob, traceback, warnings
import matplotlib
matplotlib.use("Agg")
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(path):
    nb = json.load(io.open(path, encoding="utf-8"))
    g = {"__name__": "__main__"}
    buf, old = io.StringIO(), sys.stdout
    for i, c in enumerate(nb["cells"], 1):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if src.strip().startswith("!") or "input(" in src:
            continue
        try:
            sys.stdout = buf
            exec(compile(src, f"{path}#cell{i}", "exec"), g)
        except Exception:
            sys.stdout = old
            print(f"❌ {os.path.relpath(path, ROOT)} cell {i} 失敗")
            print(traceback.format_exc(limit=3))
            return False
        finally:
            sys.stdout = old
    print(f"✅ {os.path.relpath(path, ROOT)}")
    return True

if __name__ == "__main__":
    nbs = sorted(glob.glob(os.path.join(ROOT, "week*", "*.ipynb")))
    sys.exit(0 if all([run(p) for p in nbs]) else 1)
```

- [ ] **Step 5: 跑兩支確認在空專案上乾淨通過**

```bash
cd course-calculus-1/_generators && python verify_math.py && python run_notebooks.py
```
Expected: 兩者都 exit 0（無週資料、無 notebook 時分別印出 `驗算失敗 0 項` 與無輸出）。

- [ ] **Step 6: Commit**

```bash
git add course-calculus-1/_generators/verify.py course-calculus-1/_generators/verify_math.py course-calculus-1/_generators/run_notebooks.py
git commit -m "feat(calc1): 驗證工具先行 — 結構稽核 / sympy 驗算 / notebook headless 執行"
```

---

### Task 2: 共用骨架與資料模型

**Files:**
- Create: `course-calculus-1/assets/handout.css`（從 `course-calculus-bridge/assets/handout.css` 複製）
- Create: `course-calculus-1/_generators/common.py`
- Create: `course-calculus-1/_generators/weekdata.py`

**Interfaces:**
- Consumes: Task 1 的 `verify.py`。
- Produces: `common.py` 提供 `page(title, desc, wk, active, body) -> str`（完整 HTML）、`esc(s)`、`chip(text, accent=False)`、`callout(kind, ico, title, body)`。`weekdata.py` 提供 dataclass `Concept`、`Lab`、`LessonPlan`、`Week`。

- [ ] **Step 1: 複製 CSS 並確認 workspace 修正已在**

```bash
mkdir -p course-calculus-1/assets course-calculus-1/_generators/weeks
cp course-calculus-bridge/assets/handout.css course-calculus-1/assets/handout.css
grep -A3 "^.workspace {" course-calculus-1/assets/handout.css
```
Expected: 看到 `min-height: 130px; box-sizing: border-box;`（銜接課 review 已修）。若沒有就手動補上。

- [ ] **Step 2: 寫 weekdata.py**

```python
# -*- coding: utf-8 -*-
"""每週內容的資料模型。weeks/wNN.py 只填這些結構,不碰排版。"""
from dataclasses import dataclass, field

@dataclass
class Concept:
    title_en: str          # "Integration by Parts"
    title_zh: str          # "分部積分"
    sub: str               # 英文一句副標
    idea: str              # 英文核心陳述(.idea)
    deep: str              # 中文原理與證明 HTML 片段(.deep,教師版)
    guide: list            # 中文引導問題 list[str],可含 <span class="blank"></span>(學生版)
    demo: str              # 英文示範題幹
    demo_sol: str          # 中文詳解 HTML
    demo_hint: str         # 中文提示(學生版)
    misstep: str           # 中文易錯點
    level: str             # basic / mid / hard
    drills: list           # list[(英文題幹, 中文解答 HTML)]

@dataclass
class Lab:
    title: str             # "Lab 1｜手刻積分器"
    intro: str             # 中文一段說明
    code: str              # Python 原始碼(會同時進 HTML 與 ipynb)
    expected: str          # 預期輸出文字
    seealso: str = ""      # 中文「會看到」說明
    todo: str = ""         # 以 "# TODO 學生練習:" 開頭的練習碼,空字串表示沒有

@dataclass
class LessonPlan:
    hook: str              # 開場鉤子(中文)
    fastforward: list      # [(內容, 對學生是, 建議節奏)]
    outcomes: list         # 出門時學生要能做到(中文 list)
    clock: list            # [(時間, 段落, 對應觀念)] 必須加總 180 分
    proof_moment: str      # 該週證明時刻的名稱
    script: list           # [(小節標題, HTML 內文)] 逐段講法
    myths: list            # 迷思清單
    exit_check: list       # [(題目, 參考答案)]
    homework: list         # 作業與預習

@dataclass
class Week:
    num: int
    title: str             # "分部積分"
    subtitle: str
    concepts: list = field(default_factory=list)
    labs: list = field(default_factory=list)
    lesson: LessonPlan = None
    chips: list = field(default_factory=list)
```

- [ ] **Step 3: 寫 common.py**

```python
# -*- coding: utf-8 -*-
"""HTML 骨架與零件。只管排版,不含任何教學內容。"""
import html

FONTS = ("https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700"
         "&family=Noto+Sans+TC:wght@400;700&family=Lora:ital,wght@0,400;0,600;0,700;1,400"
         "&family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap")

TABS = [("理論教案", "理論教案"), ("例題-學生版", "例題·學生"),
        ("例題-教師版", "例題·教師"), ("實作", "實作")]

def esc(s):
    """數學式與內文的 < > & 跳脫。"""
    return html.escape(s, quote=False)

def chip(text, accent=False):
    return f'<span class="chip{" accent" if accent else ""}">{text}</span>'

def callout(kind, ico, title, body):
    return (f'<div class="callout {kind}"><div class="ico">{ico}</div>'
            f'<div><span class="c-title">{title}</span>{body}</div></div>')

def nav(wk, active):
    parts = [f'<a class="home" href="../index.html"><span class="dot">∫</span>微積分(一) · 第 {wk} 週</a>']
    for suffix, label in TABS:
        cur = ' aria-current="page"' if suffix == active else ''
        parts.append(f'<a class="tab" href="W{wk}-{suffix}.html"{cur}>{label}</a>')
    parts.append('<span class="spacer"></span>')
    parts.append('<button class="theme-toggle" title="切換深淺色" aria-label="切換主題">☾</button>')
    return '<nav class="packet-nav">\n  ' + "\n  ".join(parts) + '\n</nav>'

THEME_JS = """<script>
(function(){var b=document.querySelector('.theme-toggle'),r=document.documentElement;
function e(){return r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');}
b.textContent=e()==='dark'?'☀':'☾';
b.addEventListener('click',function(){var n=e()==='dark'?'light':'dark';r.setAttribute('data-theme',n);
try{localStorage.setItem('handout-theme',n);}catch(x){}b.textContent=n==='dark'?'☀':'☾';});})();
</script>"""

def page(title, desc, wk, active, masthead, body, depth=1):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<script>(function(){{try{{var t=localStorage.getItem('handout-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/handout.css">
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }}, svg: {{ fontCache: 'global' }} }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
{nav(wk, active)}

<main class="sheet">
{masthead}
{body}
  <footer class="foot">微積分(一) · 第 {wk} 週　|　風格延續《CS 自學聖經》設計系統</footer>
</main>
{THEME_JS}
</body>
</html>
"""

def masthead(eyebrow, h1, subtitle, chips):
    return (f'  <header class="masthead">\n'
            f'    <div class="eyebrow">{eyebrow}</div>\n'
            f'    <h1>{h1}</h1>\n'
            f'    <p class="subtitle">{subtitle}</p>\n'
            f'    <div class="chips">{"".join(chips)}</div>\n'
            f'  </header>')
```

- [ ] **Step 4: 冒煙測試 common.py**

```bash
cd course-calculus-1/_generators && python -c "
import common
h = common.page('t','d',1,'實作', common.masthead('e','h','s',[common.chip('x',True)]), '<p>body</p>')
assert '<title>t</title>' in h and 'aria-current' in h and 'handout.css' in h
open('../_smoke.html','w',encoding='utf-8').write(h); print('ok')
"
cd .. && python _generators/verify.py && rm _smoke.html
```
Expected: `ok` 後 verify 印 `共 0 紅 / 0 黃`。

- [ ] **Step 5: Commit**

```bash
git add course-calculus-1/assets course-calculus-1/_generators/common.py course-calculus-1/_generators/weekdata.py
git commit -m "feat(calc1): 共用 HTML 骨架與週資料模型"
```

---

### Task 3: 三支 renderer + W1 教材（範本週）

W1 做完就凍結為範本。W2–W18 只寫資料，不再動 renderer。

**W1 內容規格**（依 spec 2.3）：診斷考＋回顧；ε-δ 一次講透。證明時刻：用 ε-δ 證 $\lim_{x\to a}x^2=a^2$。實作：浮點數 × 極限——為什麼電腦算不出真極限（接《CS 自學聖經》第 107 章浮點數）。

**W1 的 10 個觀念**（`title_en｜title_zh`，level）：
1. `Diagnostic Review｜銜接課回顧`（basic）— 極限四招決策樹複習
2. `Formal Definition of a Limit｜極限的正式定義`（mid）— ε-δ 語意
3. `Building δ from ε｜由 ε 反推 δ`（hard）— 線性函數的 δ 建構
4. `Why ε-δ Matters｜為什麼需要嚴格定義`（mid）— 直覺失效的例子
5. `One-Sided Formal Limits｜單邊極限的正式定義`（mid）
6. `Infinite Limits, Formally｜無窮極限的正式定義`（hard）
7. `Limits at Infinity, Formally｜趨向無窮的正式定義`（hard）
8. `Continuity Revisited｜用正式定義看連續`（mid）
9. `Floating-Point Reality｜浮點數下的極限`（mid）— 機器 epsilon 與消去誤差
10. `Catastrophic Cancellation｜災難性消去`（hard）— $\frac{\sqrt{1+x}-1}{x}$ 在 $x$ 極小時的數值崩潰

**W1 的 4 個 Lab**：
1. 數值探極限 vs 真極限——把 $h$ 一路縮到 $10^{-16}$，看差商先變準再變爛
2. 機器 epsilon 與浮點間距（`np.spacing`、`sys.float_info`）
3. 災難性消去實例：$\frac{\sqrt{1+x}-1}{x}$ 直算 vs 有理化後算，畫誤差曲線
4. ε-δ 視覺化：互動式挑 ε，程式找出對應 δ 並畫出方框

**Files:**
- Create: `course-calculus-1/_generators/build_examples.py`
- Create: `course-calculus-1/_generators/build_lesson.py`
- Create: `course-calculus-1/_generators/build_lab.py`
- Create: `course-calculus-1/_generators/build_all.py`
- Create: `course-calculus-1/_generators/weeks/__init__.py`（空檔）
- Create: `course-calculus-1/_generators/weeks/w01.py`
- Generates: `course-calculus-1/week01/W1-*.html`、`W1-lab.ipynb`

**Interfaces:**
- Consumes: `common.page/masthead/chip/callout/esc`、`weekdata.Concept/Lab/LessonPlan/Week`。
- Produces: 每支 renderer 提供 `render(week) -> None`（直接寫檔）。`build_all.py` 提供 `python build_all.py [週次...]`。

- [ ] **Step 1: 寫 build_examples.py（同時產學生版與教師版）**

關鍵不變式：**兩版的 `.problem` 與 `.drill` 題幹逐字相同**，差別只在學生版用 `.guide`＋`.workspace`、教師版用 `.deep`＋`.sol`＋`.ans-body`。

```python
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from common import chip, callout, page, masthead

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _qtype(i, c):
    return (f'  <div class="qtype"><div class="badge">{i}</div><div>'
            f'<h3 class="qtype-title">{c.title_en}｜{c.title_zh}</h3>'
            f'<span class="qtype-sub">{c.sub}</span></div></div>')

def _drill_stems(c):
    return "\n".join(f"    <li>{q}</li>" for q, _ in c.drills)

def _drill_with_ans(c):
    return "\n".join(f'    <li>{q}<div class="ans-body">{a}</div></li>' for q, a in c.drills)

def student_body(week):
    out = []
    for i, c in enumerate(week.concepts, 1):
        guide = "\n".join(f"<li>{g}</li>" for g in c.guide)
        out.append(_qtype(i, c))
        out.append(f'  <div class="idea"><div class="ico">🧭</div><div><span class="lbl">引導推導</span>'
                   f'<p>跟著老師一步步想,自己把道理推出來:</p>\n<ol class="guide">\n{guide}\n</ol></div></div>')
        out.append('  <div class="block-label teach">一起做 · 示範</div>')
        out.append(f'  <div class="ex"><div class="ex-head"><span class="ex-tag">示範</span>'
                   f'<span class="level {c.level}">{ {"basic":"基礎","mid":"進階","hard":"挑戰"}[c.level] }</span></div>'
                   f'<p class="problem">{c.demo}</p><p class="hint"><b>一起想</b>:{c.demo_hint}</p>'
                   f'<div class="workspace"><span class="ws-label">作答區</span></div></div>')
        out.append('  <div class="block-label">換你練習</div>')
        out.append(f'  <ol class="drill">\n{_drill_stems(c)}\n  </ol>\n')
    return "\n".join(out)

def teacher_body(week):
    out = []
    for i, c in enumerate(week.concepts, 1):
        out.append(_qtype(i, c))
        out.append(f'  <div class="idea"><div class="ico">💡</div><div><span class="lbl">觀念</span>'
                   f'<p>{c.idea}</p></div></div>')
        out.append(f'  <div class="deep"><div class="deep-head"><span class="tag">原理</span>'
                   f'為什麼成立 · 推導與證明</div><div class="deep-body">\n{c.deep}\n</div></div>')
        out.append('  <div class="block-label teach">示範 · 老師講</div>')
        out.append(f'  <div class="ex"><div class="ex-head"><span class="ex-tag">示範</span>'
                   f'<span class="level {c.level}">{ {"basic":"基礎","mid":"進階","hard":"挑戰"}[c.level] }</span></div>'
                   f'<p class="problem">{c.demo}</p>'
                   f'<div class="sol"><span class="sol-label">詳解</span>{c.demo_sol}</div>'
                   f'<div class="misstep"><b>易錯點</b>　{c.misstep}</div></div>')
        out.append('  <div class="block-label">換你練習 · 附解答</div>')
        out.append(f'  <ol class="drill">\n{_drill_with_ans(c)}\n  </ol>\n')
    return "\n".join(out)

def render(week):
    wk = week.num
    nd = sum(len(c.drills) for c in week.concepts)
    nc = len(week.concepts)
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)

    chips_s = [chip("學生版 · 引導推導", True), chip(f"{nc} 個觀念"), chip(f"{nc} 題示範"), chip(f"{nd} 題變形練習")]
    mh_s = masthead(f"第 {wk} 週 · 例題·學生版", f"{week.title} · 引導推導",
                    "這份不直接給公式。每個觀念用一串<strong>引導問題與填空</strong>,讓你跟著老師把原理親手推出來——而不是死背。",
                    chips_s)
    body_s = (callout("note", "🧭", "怎麼用這份學生版",
                      "<p>每個觀念先跟著<strong>引導推導</strong>把道理想出來,再看<strong>示範</strong>一起做一題,"
                      "最後<strong>換你練習</strong>在筆記本上動手。想對答案或看原理證明,翻老師版。</p>")
              + "\n\n" + student_body(week))
    open(os.path.join(d, f"W{wk}-例題-學生版.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 例題·學生版 · {week.title}", "引導式推導,帶學生理解原理而非死背",
             wk, "例題-學生版", mh_s, body_s))

    chips_t = [chip("教師版 · 原理與證明", True), chip(f"{nc} 個觀念"), chip(f"{nc} 題示範"), chip(f"{nd} 題附解答")]
    mh_t = masthead(f"第 {wk} 週 · 例題·教師版", f"{week.title} · 原理與證明",
                    "每個觀念附完整推導與證明,示範題有詳解與易錯點,練習題附解答。", chips_t)
    open(os.path.join(d, f"W{wk}-例題-教師版.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 例題·教師版 · {week.title}", "含原理證明與完整解答",
             wk, "例題-教師版", mh_t, teacher_body(week)))
```

- [ ] **Step 2: 寫 build_lab.py（HTML 可讀版 + ipynb 同源）**

```python
# -*- coding: utf-8 -*-
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from common import chip, callout, page, masthead

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _pre(code):
    return f"<pre><code>{html.escape(code, quote=True)}</code></pre>"

def render(week):
    wk = week.num
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)
    n_todo = sum(1 for lab in week.labs if lab.todo.strip())

    # ---- HTML 可讀版 ----
    parts = [callout("note", "💻", "怎麼跑",
                     "<p>這頁是<strong>可讀版</strong>;程式要實際執行,請下載 notebook,上傳到 "
                     '<a href="https://colab.research.google.com/" target="_blank" rel="noopener">Google Colab</a>'
                     "(或用本機 Jupyter),由上往下逐格執行。</p>"
                     f'<p style="margin-top:10px"><a class="dl" href="W{wk}-lab.ipynb" download>⬇ 下載 W{wk}-lab.ipynb</a></p>")]
    for lab in week.labs:
        parts.append(f"<h2>{lab.title}</h2><p>{lab.intro}</p>{_pre(lab.code)}")
        if lab.expected:
            parts.append(f'<div class="out"><span class="out-label">預期輸出</span>{html.escape(lab.expected)}</div>')
        if lab.seealso:
            parts.append(f"<p><b>會看到</b>:{lab.seealso}</p>")
        if lab.todo.strip():
            parts.append(f"<p>換你試:</p>{_pre(lab.todo)}")
    chips = [chip(f"{len(week.labs)} 個 Lab", True), chip(f"{n_todo} 題 TODO"), chip("Colab / Jupyter")]
    mh = masthead(f"第 {wk} 週 · 實作", week.subtitle, week.lesson.hook if week.lesson else "", chips)
    open(os.path.join(d, f"W{wk}-實作.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 實作 · {week.title}", "Python 實作:把概念跑出來、畫出來",
             wk, "實作", mh, "\n".join(parts)))

    # ---- ipynb ----
    def md(src):
        return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

    def code(src):
        return {"cell_type": "code", "execution_count": None, "metadata": {},
                "outputs": [], "source": src.splitlines(keepends=True)}

    cells = [md(f"# 第 {wk} 週 實作｜{week.title}(Colab notebook)\n\n{week.subtitle}\n"),
             md("### (選用)讓圖表顯示中文\n"),
             code("import matplotlib\n"
                  "# Colab: !apt-get -qq install fonts-noto-cjk 後改用 'Noto Sans CJK TC'\n"
                  "matplotlib.rcParams['axes.unicode_minus'] = False\n")]
    for lab in week.labs:
        cells.append(md(f"## {lab.title}\n\n{lab.intro}\n"))
        cells.append(code(lab.code))
        if lab.todo.strip():
            cells.append(code(lab.todo))
    nb = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"}},
        "nbformat": 4, "nbformat_minor": 5}
    json.dump(nb, open(os.path.join(d, f"W{wk}-lab.ipynb"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
```

- [ ] **Step 3: 寫 build_lesson.py**

```python
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, page, masthead

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _table(headers, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<div class="tbl-wrap"><table{f" class={cls}" if cls else ""}>'
            f"<thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>")

def render(week):
    wk, L = week.num, week.lesson
    total = sum(int(t.split("–")[1].split(":")[0]) * 60 + int(t.split("–")[1].split(":")[1])
                - int(t.split("–")[0].split(":")[0]) * 60 - int(t.split("–")[0].split(":")[1])
                for t, _, _ in L.clock)
    assert total == 180, f"W{wk} 節奏表合計 {total} 分,必須是 180"

    parts = [f"<h2>哪些能快轉,哪些要踩煞車</h2>",
             _table(["內容", "對學生是", "建議節奏"], L.fastforward),
             "<h2>下課鐘響時,學生要能做到</h2><ul>" + "".join(f"<li>{o}</li>" for o in L.outcomes) + "</ul>",
             "<h2>三小時怎麼切</h2>",
             _table(["時間", "段落", "對應觀念"], L.clock, cls='"clock"'),
             callout("key", "🎯", "本週的證明時刻",
                     f"<p>{L.proof_moment}——教師版寫完整推導,學生版留引導填空。"
                     f"筆試不考「請證明」,考「哪一步違反前提」「舉反例」「用在新情境」。</p>"),
             "<h2>逐段怎麼上</h2>"]
    for h, b in L.script:
        parts.append(f"<h3>{h}</h3>{b}")
    parts.append(callout("warn", "🧠", "學生最常翻的車",
                         "<ul>" + "".join(f"<li>{m}</li>" for m in L.myths) + "</ul>"))
    parts.append("<h2>出門檢核(下課前 5 分鐘)</h2><ol>"
                 + "".join(f"<li>{q}</li>" for q, _ in L.exit_check) + "</ol>")
    parts.append(callout("tip", "✅", "參考答案",
                         "<ol>" + "".join(f"<li>{a}</li>" for _, a in L.exit_check) + "</ol>"))
    parts.append("<h2>作業與預習</h2><ul>" + "".join(f"<li>{h}</li>" for h in L.homework) + "</ul>")

    chips = [chip("理論 3 小時"), chip("搭配實作 3 小時"), chip("對應本書第 12 章")] + \
            [chip(c, True) for c in week.chips]
    mh = masthead(f"第 {wk} 週 · 理論教案", week.title, L.hook, chips)
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"W{wk}-理論教案.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 理論教案 · {week.title}", "教學腳本:節奏、講法、迷思、檢核",
             wk, "理論教案", mh, "\n".join(parts)))
```

**注意**：`assert total == 180` 讓節奏表對不上就直接爆掉——這是防止銜接課那種「教案數字與現實不符」的最便宜手段。

- [ ] **Step 4: 寫 build_all.py**

```python
# -*- coding: utf-8 -*-
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_lesson, build_examples, build_lab

def main():
    weeks = [int(a) for a in sys.argv[1:]] or list(range(1, 19))
    for wk in weeks:
        try:
            mod = importlib.import_module(f"weeks.w{wk:02d}")
        except ModuleNotFoundError:
            print(f"跳過 W{wk}(尚無資料)")
            continue
        w = mod.WEEK
        if w.lesson:
            build_lesson.render(w)
        if w.concepts:
            build_examples.render(w)
        if w.labs:
            build_lab.render(w)
        print(f"✅ W{wk} 產出完成")

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 寫 weeks/w01.py（依上方 W1 內容規格，10 觀念 × 3 練習 + 4 Lab）**

每個觀念的 `drills` 三題，難度由 basic 排到 hard。**所有數值答案先進 `ANSWER_CHECKS`** 供 sympy 驗算，格式：

```python
ANSWER_CHECKS = [
    ("觀念3 示範 δ=ε/5", "Rational(1,5)*eps", "eps/5"),
    ("觀念10 有理化後極限", "limit((sqrt(1+x)-1)/x, x, 0)", "Rational(1,2)"),
    # …每個有數值答案的示範與練習都要一行
]
```

模組結尾必須是 `WEEK = Week(num=1, title="極限的嚴格定義與浮點數現實", subtitle=..., concepts=[...], labs=[...], lesson=LessonPlan(...), chips=["學期地基"])`。

- [ ] **Step 6: 產出 W1 並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 1
cd .. && python _generators/verify.py 1
cd _generators && python verify_math.py 1 && python run_notebooks.py
```
Expected: 產出四個檔；verify `共 0 紅 / 0 黃`；驗算 `失敗 0 項`；notebook 全部 `✅`。任一失敗就修 `w01.py` 後重生，**不要手改 HTML**。

- [ ] **Step 7: 視覺驗收（headless 截圖）**

```bash
"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --no-sandbox \
  --hide-scrollbars --user-data-dir="$TMP/cdp" --virtual-time-budget=25000 --window-size=1000,1800 \
  --screenshot="$TMP/w01.png" "file:///c:/我的筆記/cs-textbook/course-calculus-1/week01/W1-例題-學生版.html"
```
用 Read 看圖，確認：MathJax 有渲染、作答區約 130px（4 行）、深色主題可讀、觀念標題是 `English｜中文`。

- [ ] **Step 8: Commit**

```bash
git add course-calculus-1/_generators course-calculus-1/week01
git commit -m "feat(calc1): W1 極限的嚴格定義與浮點數現實 + 三支 renderer(範本週)"
```

---

### Task 4: W2–W3 導數的補完

**W2**（反函數微分、反三角、雙曲函數）：證明時刻＝反函數微分公式 $\left(f^{-1}\right)'(b)=\dfrac{1}{f'(a)}$。9 觀念、3 Lab（用數值微分驗反三角導數、雙曲函數與懸鏈線、反函數圖形對稱性）。
**W3**（Cauchy MVT → L'Hôpital 的證明、泰勒多項式不談收斂）：證明時刻＝L'Hôpital 為何成立。10 觀念、4 Lab（泰勒近似 sin/exp 誤差曲線、看 math 函式庫怎麼算 sin、Cauchy MVT 幾何視覺化、餘項估計）。

**注意**：W3 必須修掉銜接課的循環論證問題——**不要**用 L'Hôpital 當 $\lim\frac{\sin x}{x}$ 的示範。改用 $\lim\frac{e^x-1-x}{x^2}$，並在教師版 `deep` 明寫「用 L'Hôpital 算 $\frac{\sin x}{x}$ 是循環論證，因為 $(\sin x)'=\cos x$ 本身就靠這個極限推出來」。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w02.py`、`w03.py`
- Generates: `week02/W2-*`、`week03/W3-*`

**Interfaces:**
- Consumes: Task 3 的 `Week/Concept/Lab/LessonPlan` 與三支 renderer（不修改）。
- Produces: `weeks.w02.WEEK`、`weeks.w03.WEEK`、各自的 `ANSWER_CHECKS`。

- [ ] **Step 1: 寫 weeks/w02.py**（9 觀念 × 3 練習、3 Lab、LessonPlan 節奏表合計 180 分、ANSWER_CHECKS 涵蓋所有數值答案）
- [ ] **Step 2: 寫 weeks/w03.py**（10 觀念 × 3 練習、4 Lab、同上；含循環論證的說明）
- [ ] **Step 3: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 2 3
cd .. && python _generators/verify.py 2 3
cd _generators && python verify_math.py 2 3 && python run_notebooks.py
```
Expected: verify `0 紅`；驗算 `失敗 0 項`；notebook 全 `✅`。

- [ ] **Step 4: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week02 course-calculus-1/week03
git commit -m "feat(calc1): W2-W3 反函數與雙曲函數、Cauchy MVT 與泰勒多項式"
```

---

### Task 5: W4–W6 積分技巧 I

**W4** 分部積分（含遞迴式）：證明時刻＝分部＝乘積法則反過來。8 觀念、2 Lab（$\int x^n e^x$ 遞迴公式跑成程式、SymPy 對照）。
**W5** 三角積分與三角代換：證明時刻＝三角代換為何合法（需單調可逆）。10 觀念、2 Lab（符號積分 vs 手算、代換前後的定義域檢查）。
**W6** 部分分式分解：證明時刻＝分解定理為何可行。8 觀念、2 Lab（**手刻部分分式分解器**：解線性方程組求係數，作為線代預告；`sympy.apart` 對照）。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w04.py`、`w05.py`、`w06.py`

**Interfaces:**
- Consumes: Task 3 的資料模型與 renderer。
- Produces: `weeks.w04/w05/w06` 的 `WEEK` 與 `ANSWER_CHECKS`。

- [ ] **Step 1: 寫 w04.py**
- [ ] **Step 2: 寫 w05.py**
- [ ] **Step 3: 寫 w06.py**
- [ ] **Step 4: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 4 5 6
cd .. && python _generators/verify.py 4 5 6
cd _generators && python verify_math.py 4 5 6 && python run_notebooks.py
```

- [ ] **Step 5: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week04 course-calculus-1/week05 course-calculus-1/week06
git commit -m "feat(calc1): W4-W6 分部積分、三角代換、部分分式"
```

---

### Task 6: W7–W8 數值積分與瑕積分

**W7** 技巧總整理＋數值積分（Simpson／Gauss）：證明時刻＝Simpson 誤差為何是 $O(h^4)$（用泰勒展開，呼應 W3）。10 觀念、3 Lab（手刻 trapezoid/Simpson/Gauss、與 `scipy.integrate.quad` 對照、誤差 vs $h$ 的 log-log 圖）。
**W8** 瑕積分與收斂判定：證明時刻＝比較審斂法。9 觀念、3 Lab（機率密度歸一化、softmax 的歸一化常數、$\int_0^\infty e^{-x^2}dx$ 數值 vs $\frac{\sqrt\pi}{2}$）。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w07.py`、`w08.py`

**Interfaces:**
- Consumes: Task 3 的資料模型與 renderer。
- Produces: `weeks.w07/w08` 的 `WEEK` 與 `ANSWER_CHECKS`。

- [ ] **Step 1: 寫 w07.py**
- [ ] **Step 2: 寫 w08.py**
- [ ] **Step 3: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 7 8
cd .. && python _generators/verify.py 7 8
cd _generators && python verify_math.py 7 8 && python run_notebooks.py
```

- [ ] **Step 4: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week07 course-calculus-1/week08
git commit -m "feat(calc1): W7-W8 數值積分與瑕積分"
```

---

### Task 7: W9 期中考（考卷版＋詳解版）

**規格**（依 spec 3.1）：範圍 W1–W8。總分 100，題型配比 計算 60／概念與前提判斷 25／應用 15。ε-δ 只考直覺與「哪一步違反前提」。

**作答區高度必須依配分**：4 分 132px、5 分 180px、6 分 240px、12 分 340–460px（畫圖題取 460px）。這是銜接課 review 抓到的實際缺陷，不可重蹈。

**Files:**
- Create: `course-calculus-1/_generators/build_exam.py`
- Create: `course-calculus-1/_generators/weeks/w09.py`
- Generates: `week09/W9-期中考-考卷版.html`、`W9-期中考-詳解版.html`

**Interfaces:**
- Consumes: `common.page/masthead/chip`。
- Produces: `build_exam.render(exam)`；`weeks.w09.EXAM` 為 `ExamPaper(problems=[Problem(label, pts, stem_en, sol_zh, level)])`。

- [ ] **Step 1: 在 weekdata.py 加 ExamPaper / Problem dataclass**

```python
@dataclass
class Problem:
    label: str      # "1(a)"
    pts: int
    stem: str       # 英文題幹
    sol: str        # 中文詳解 HTML
    level: str      # basic/mid/hard(只影響徽章顏色)

@dataclass
class ExamGroup:
    num: int
    title: str      # "Problem 1 · Limits & the Formal Definition"
    origin: str     # "對應第 1 週"
    problems: list

@dataclass
class ExamPaper:
    week: int
    name: str       # "期中考"
    minutes: int
    groups: list
```

- [ ] **Step 2: 寫 build_exam.py**

```python
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, page, masthead

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEIGHT = {4: 132, 5: 180, 6: 240, 12: 460}

def _height(pts, needs_graph=False):
    if pts >= 12:
        return 460 if needs_graph else 340
    return HEIGHT.get(pts, 132)

def _group_head(g, total):
    return (f'  <div class="qtype"><div class="badge">{g.num}</div><div>'
            f'<h3 class="qtype-title">{g.title}</h3>'
            f'<span class="qtype-sub">{g.origin} · {total} pts</span></div></div>')

def render(exam, with_solutions):
    wk = exam.week
    parts = []
    for g in exam.groups:
        parts.append(_group_head(g, sum(p.pts for p in g.problems)))
        for p in g.problems:
            tail = (f'<div class="sol"><span class="sol-label">Solution · {p.pts} pts</span>{p.sol}</div>'
                    if with_solutions else
                    f'<div class="workspace" style="min-height:{_height(p.pts, "sketch" in p.stem.lower())}px">'
                    f'<span class="ws-label">Answer</span></div>')
            parts.append(f'  <div class="ex"><div class="ex-head">'
                         f'<span class="ex-tag">Problem {p.label}</span>'
                         f'<span class="level {p.level}">{p.pts} pts</span></div>'
                         f'<p class="problem">{p.stem}</p>{tail}</div>')
    total = sum(p.pts for g in exam.groups for p in g.problems)
    assert total == 100, f"總分 {total},必須是 100"
    kind = "詳解版" if with_solutions else "考卷版"
    chips = [chip(f"Total {total} pts", True), chip(f"{len(exam.groups)} problems"),
             chip(f"Time {exam.minutes} min"), chip("No calculator")]
    mh = masthead(f"第 {wk} 週 · {exam.name}{kind}", f"Calculus I — {exam.name}",
                  "題目全為英文原文;請把每題的解題過程寫在作答區。" if not with_solutions
                  else "同一份考卷的解答本:每題重印英文題目,附中文解題敘述與配分。答案已全部用 sympy 驗證。",
                  chips)
    d = os.path.join(ROOT, f"week{wk:02d}")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"W{wk}-{exam.name}-{kind}.html"), "w", encoding="utf-8").write(
        page(f"第 {wk} 週 {exam.name}·{kind}", f"{exam.name}{kind}", wk,
             f"{exam.name}-{kind}", mh, "\n".join(parts)))
```

- [ ] **Step 3: 寫 weeks/w09.py**（6 大題／100 分，配比 計算 60／概念 25／應用 15，每題答案進 `ANSWER_CHECKS`）
- [ ] **Step 4: 產出並驗證兩版題幹逐字相同**

```bash
cd course-calculus-1/_generators && python -c "
import sys; sys.path.insert(0,'.')
import build_exam, weeks.w09 as w
build_exam.render(w.EXAM, False); build_exam.render(w.EXAM, True); print('ok')"
cd .. && python - <<'PY'
import io,re
q=io.open("week09/W9-期中考-考卷版.html",encoding="utf-8").read()
a=io.open("week09/W9-期中考-詳解版.html",encoding="utf-8").read()
f=lambda s:[re.sub(r"\s+"," ",re.sub("<[^>]+>","",x)).strip() for x in re.findall(r'<p class="problem">(.*?)</p>',s,re.S)]
assert f(q)==f(a), "考卷與詳解題幹不一致"
assert 'class="sol"' not in q, "考卷版洩答案"
print("題數",len(f(q)),"兩版逐字相同 ✓")
PY
python _generators/verify.py 9
cd _generators && python verify_math.py 9
```

- [ ] **Step 5: Commit**

```bash
git add course-calculus-1/_generators course-calculus-1/week09
git commit -m "feat(calc1): W9 期中考(考卷版+詳解版,作答區依配分)"
```

---

### Task 8: W10–W11 積分的應用 I

**W10** 面積、體積（切片／殼層）：證明時刻＝體積公式來自黎曼和。9 觀念、2 Lab（數值算旋轉體體積對照解析解、切片動畫式視覺化）。
**W11** 弧長、旋轉曲面：證明時刻＝弧長公式的推導。7 觀念、2 Lab（曲線的弧長參數化、離散折線長度收斂到弧長）。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w10.py`、`w11.py`

**Interfaces:**
- Consumes: Task 3 的資料模型與 renderer。
- Produces: `weeks.w10/w11` 的 `WEEK` 與 `ANSWER_CHECKS`。

- [ ] **Step 1: 寫 w10.py**
- [ ] **Step 2: 寫 w11.py**
- [ ] **Step 3: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 10 11
cd .. && python _generators/verify.py 10 11
cd _generators && python verify_math.py 10 11 && python run_notebooks.py
```

- [ ] **Step 4: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week10 course-calculus-1/week11
git commit -m "feat(calc1): W10-W11 面積體積與弧長"
```

---

### Task 9: W12–W13 期望值與參數式

**W12** 功、質心、期望值與變異數：證明時刻＝期望值＝積分。9 觀念、3 Lab（從積分算期望值與變異數、**loss 是期望損失的估計：mini-batch 為何能近似**、蒙地卡羅 vs 解析積分）。
**W13** 參數式曲線、極座標：證明時刻＝極座標面積 $\frac12\int r^2d\theta$ 的來源。9 觀念、2 Lab（畫參數曲線與極座標玫瑰線、參數式弧長）。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w12.py`、`w13.py`

**Interfaces:**
- Consumes: Task 3 的資料模型與 renderer。
- Produces: `weeks.w12/w13` 的 `WEEK` 與 `ANSWER_CHECKS`。

- [ ] **Step 1: 寫 w12.py**
- [ ] **Step 2: 寫 w13.py**
- [ ] **Step 3: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 12 13
cd .. && python _generators/verify.py 12 13
cd _generators && python verify_math.py 12 13 && python run_notebooks.py
```

- [ ] **Step 4: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week12 course-calculus-1/week13
git commit -m "feat(calc1): W12-W13 期望值與參數式極座標"
```

---

### Task 10: W14–W15 微分方程入門

**W14** 一階可分離變數 ODE、成長衰減：證明時刻＝分離變數為何合法。8 觀念、3 Lab（**Euler 法**手刻、指數成長衰減擬合、步長 $h$ 與誤差）。
**W15** 一階線性 ODE、積分因子：證明時刻＝積分因子怎麼被想出來。8 觀念、3 Lab（**RK4** 手刻、Euler vs RK4 誤差階數 log-log、`scipy.integrate.solve_ivp` 對照）。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w14.py`、`w15.py`

**Interfaces:**
- Consumes: Task 3 的資料模型與 renderer。
- Produces: `weeks.w14/w15` 的 `WEEK` 與 `ANSWER_CHECKS`；Lab 需匯出 `euler(f, y0, t0, t1, h)` 與 `rk4(f, y0, t0, t1, h)` 兩個函式簽章供 W16–W17 沿用。

- [ ] **Step 1: 寫 w14.py**
- [ ] **Step 2: 寫 w15.py**
- [ ] **Step 3: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 14 15
cd .. && python _generators/verify.py 14 15
cd _generators && python verify_math.py 14 15 && python run_notebooks.py
```

- [ ] **Step 4: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week14 course-calculus-1/week15
git commit -m "feat(calc1): W14-W15 一階 ODE 與數值解法(Euler/RK4)"
```

---

### Task 11: W16–W17 梯度流與 Capstone

**W16** 方向場、平衡點與穩定性：證明時刻＝平衡點穩定性判準。8 觀念、3 Lab（方向場繪製、**梯度流 $\dot\theta=-\nabla L$ 是最佳化的連續極限**、平衡點吸引/排斥視覺化）。
**W17** Capstone「最佳化即動力學」：無例題雙版，改出 `W17-Capstone.html` + `W17-capstone.ipynb`。

**Capstone 四個 Part**：
1. 梯度下降 = 梯度流的 Euler 法（用 W14 的 `euler`）
2. momentum = 帶阻尼的二階 ODE $\ddot\theta+\gamma\dot\theta+\nabla L=0$
3. 用 RK4 解同一個梯度流，比較軌跡
4. 用泰勒展開解釋 Euler 誤差 $O(h^2)$、RK4 $O(h^4)$，並把 learning rate 對應到步長 $h$

**保底版本**（進度落後時）：只做 Part 1 + Part 3，Part 2 降為進階徽章。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w16.py`、`w17.py`
- Modify: `course-calculus-1/_generators/build_lab.py`（加 `capstone=True` 參數，改檔名為 `W{wk}-Capstone.html` / `W{wk}-capstone.ipynb`，nav 分頁標籤改「Capstone」）

**Interfaces:**
- Consumes: W14–W15 的 `euler(f, y0, t0, t1, h)`、`rk4(f, y0, t0, t1, h)`。
- Produces: `weeks.w16/w17` 的 `WEEK`。

- [ ] **Step 1: 改 build_lab.py 支援 capstone 檔名與分頁**
- [ ] **Step 2: 寫 w16.py**
- [ ] **Step 3: 寫 w17.py（四個 Part，每個 Part 都要能收斂並印出數字）**
- [ ] **Step 4: 產出並跑三道閘門**

```bash
cd course-calculus-1/_generators && python build_all.py 16 17
cd .. && python _generators/verify.py 16 17
cd _generators && python verify_math.py 16 17 && python run_notebooks.py
```
Expected: capstone notebook 跑完印出 GD / momentum / RK4 三條軌跡的最終誤差，且 momentum 收斂步數明顯少於純 GD。

- [ ] **Step 5: Commit**

```bash
git add course-calculus-1/_generators course-calculus-1/week16 course-calculus-1/week17
git commit -m "feat(calc1): W16-W17 梯度流與 Capstone「最佳化即動力學」"
```

---

### Task 12: W18 總整理與期末考

**W18**：證明總整理（把 15 個證明時刻串成一張地圖）＋期末複習。另出期末考卷版與詳解版（範圍以 W10–W17 為主，應用題自然用到 W4–W8 的技巧）。

**Files:**
- Create: `course-calculus-1/_generators/weeks/w18.py`
- Generates: `week18/W18-理論教案.html`（含證明地圖表）、`W18-期末考-考卷版.html`、`W18-期末考-詳解版.html`

**Interfaces:**
- Consumes: `build_lesson.render`、`build_exam.render`。
- Produces: `weeks.w18.WEEK`、`weeks.w18.EXAM`。

- [ ] **Step 1: 寫 w18.py**（證明地圖表格：15 列 = 週次／定理／一句話為什麼／考法變形）
- [ ] **Step 2: 產出並驗證期末考兩版一致、總分 100**

```bash
cd course-calculus-1/_generators && python build_all.py 18 && python -c "
import sys; sys.path.insert(0,'.')
import build_exam, weeks.w18 as w
build_exam.render(w.EXAM, False); build_exam.render(w.EXAM, True); print('ok')"
cd .. && python _generators/verify.py 18
cd _generators && python verify_math.py 18
```

- [ ] **Step 3: Commit**

```bash
git add course-calculus-1/_generators/weeks course-calculus-1/week18
git commit -m "feat(calc1): W18 證明總整理與期末考"
```

---

### Task 13: 課程首頁與全站最終驗收

**Files:**
- Create: `course-calculus-1/_generators/build_index.py`
- Generates: `course-calculus-1/index.html`

**Interfaces:**
- Consumes: 全部 `weeks.wNN.WEEK`。
- Produces: 18 張週卡，每張含週次、標題、副標、觀念數、Lab 數與四個分頁連結。

- [ ] **Step 1: 寫 build_index.py**

```python
# -*- coding: utf-8 -*-
import os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chip, callout, FONTS, THEME_JS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def card(w):
    links = []
    for suffix, label in [("理論教案", "理論教案"), ("例題-學生版", "例題·學生"),
                          ("例題-教師版", "例題·教師"), ("實作", "實作")]:
        p = f"week{w.num:02d}/W{w.num}-{suffix}.html"
        if os.path.exists(os.path.join(ROOT, p)):
            links.append(f'<a href="{p}">{label}</a>')
    for extra in ("期中考-考卷版", "期末考-考卷版", "Capstone"):
        p = f"week{w.num:02d}/W{w.num}-{extra}.html"
        if os.path.exists(os.path.join(ROOT, p)):
            links.append(f'<a href="{p}">{extra}</a>')
    status = "done" if links else "soon"
    return (f'    <article class="week-card"><div class="week-head">'
            f'<span class="week-num">{w.num:02d}</span>'
            f'<div><h3>{w.title}</h3><p class="week-sub">{w.subtitle}</p></div>'
            f'<span class="week-status {status}">{"可用" if links else "準備中"}</span></div>'
            f'<p class="week-topics">{len(w.concepts)} 觀念 · {len(w.labs)} Lab</p>'
            f'<div class="week-links">{"".join(links)}</div></article>')

def main():
    cards = []
    for wk in range(1, 19):
        try:
            cards.append(card(importlib.import_module(f"weeks.w{wk:02d}").WEEK))
        except ModuleNotFoundError:
            continue
    body = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>微積分(一) · 資工系大一</title>
<meta name="description" content="資工系大一微積分(一):18 週,理論與 Python 實作並行,收斂到「最佳化即動力學」capstone。">
<script>(function(){{try{{var t=localStorage.getItem('handout-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/handout.css">
</head>
<body>
<nav class="packet-nav"><span class="home"><span class="dot">∫</span>微積分(一) · 課程首頁</span>
<span class="spacer"></span><button class="theme-toggle" title="切換深淺色" aria-label="切換主題">☾</button></nav>
<main class="sheet">
  <header class="masthead">
    <div class="eyebrow">資工系 · 大一上</div>
    <h1>微積分(一)</h1>
    <p class="subtitle">18 週,理論 3hr + 實作 3hr 並行。從極限的嚴格定義走到微分方程,
    實作主線一路滾到最後那句話:<strong>梯度下降其實是在解微分方程</strong>。</p>
    <div class="chips">{chip("18 週 · 108 小時", True)}{chip("3hr 理論 + 3hr 實作")}{chip("15 個證明時刻")}{chip("Capstone:最佳化即動力學")}</div>
  </header>
  <div class="week-list">
{chr(10).join(cards)}
  </div>
  <footer class="foot">微積分(一) · 資工系大一　|　風格延續《CS 自學聖經》設計系統</footer>
</main>
{THEME_JS}
</body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(body)
    print(f"✅ index.html:{len(cards)} 張週卡")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 全站重生並跑完整驗收**

```bash
cd course-calculus-1/_generators && python build_all.py && python build_index.py
cd .. && python _generators/verify.py
cd _generators && python verify_math.py && python run_notebooks.py
```
Expected: verify `共 0 紅 / 0 黃`；驗算 `失敗 0 項`；18 個 notebook 全 `✅`。

- [ ] **Step 3: 連結完整性檢查**

```bash
cd course-calculus-1 && python - <<'PY'
import os,re,glob
bad=0
for f in glob.glob("index.html")+glob.glob("week*/*.html"):
    d=os.path.dirname(f) or "."
    for h in re.findall(r'href="([^"#:]+\.(?:html|ipynb|css))"', open(f,encoding="utf-8").read()):
        if not os.path.exists(os.path.normpath(os.path.join(d,h))):
            print("壞連結",f,"->",h); bad+=1
print("壞連結數:",bad)
PY
```
Expected: `壞連結數: 0`

- [ ] **Step 4: 視覺抽驗三頁（首頁、任一學生版、期中考卷）**

用 headless Chrome 截圖後以 Read 檢視，確認 MathJax 渲染、作答區高度、深色主題、週卡連結齊全。

- [ ] **Step 5: Commit**

```bash
git add course-calculus-1
git commit -m "feat(calc1): 課程首頁與全站最終驗收(18 週教材完成)"
```

---

## Self-Review

**Spec 覆蓋檢查**

| Spec 章節 | 對應 Task |
|---|---|
| 1.2 四件式交付物 | Task 3（三支 renderer） |
| 1.2 雙語規則 | Task 1（`check_bilingual`）＋ Global Constraints |
| 1.3 理論↔實作咬合 | Task 4–12 每週的 Lab 規格 |
| 1.4 證明時刻（15 個） | Task 3–11 每週 `LessonPlan.proof_moment`；Task 12 總整理 |
| 1.5 評量比重 | Task 7（期中）、Task 12（期末）；實作兩級制寫在教案 |
| 2.3 18 週大綱 | Task 3–12 逐週對應 |
| 2.4 ML 螺旋 v2 | W3 泰勒（Task 4）、W8 瑕積分（Task 6）、W12 期望值（Task 9）、W14–17 ODE（Task 10–11） |
| 2.5 Capstone | Task 11 |
| 3.1 期中配比 | Task 7 |
| 3.2 期末範圍 | Task 12 |
| 5.1 產生器版控 | Global Constraints ＋ 每個 Task 的 commit 都含 `_generators/` |
| 6 檔案佈局 | File Structure 一節 |

**未被 Task 覆蓋的 spec 項目**：4.1／4.2 跨課接口是給微二與線代的 spec 用的，本計畫不實作，但 W16–W17 的內容已為線代預埋鉤子（Task 11）。

**型別一致性**：`Concept` 的欄位在 `build_examples` 全部被使用；`Lab.todo` 空字串代表無 TODO，`build_lab` 與 `verify.check_counts` 都以 `# TODO` 開頭判定，一致。`euler/rk4` 簽章在 Task 10 定義、Task 11 消費，名稱一致。`ExamPaper/ExamGroup/Problem` 在 Task 7 定義、Task 12 重用。
