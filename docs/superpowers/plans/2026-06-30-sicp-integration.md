# SICP 整合 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在既有 80 章的 HTML 教科書尾端新增「第十九部 · SICP:抽象的建構」5 章,涵蓋 SICP 8 個尚未涵蓋的核心概念,並在既有章節加輕量互連 callout。

**Architecture:** 每章為一個獨立 HTML 檔(`chapters/80–84-*.html`),由 `assets/book.js` 的 `BOOK.parts` 資料註冊;新增一個 part 物件即在側欄與導覽出現。每寫好一章就同步在 book.js 加該章條目(`done: true`),確保任一任務邊界都無斷連結。先建一支結構驗證腳本當「測試」,每章寫完跑它。

**Tech Stack:** 純靜態 HTML + CSS + 原生 JS(`assets/book.js`、`assets/style.css`);highlight.js 11.9.0(內建 `scheme`)、MathJax 3.2.2;驗證用 Python 3(repo 已有 `_build_toi_*.py` 慣例)、`node --check` 檢查 book.js 語法。

## Global Constraints

- 語言:繁體中文為主,術語首次出現用「中文(English)」並陳;Medium 長文敘事風,由淺入深(為什麼→直覺→精確→實作→陷阱)。
- 程式碼:**Scheme 為主**(`<pre><code class="language-scheme">`)+ 關鍵處 **Python 對照**(`language-python`);C 用 `language-c`。
- **跳脫**:所有 `<code>` 內的 `<`、`>`、`&` 必須寫成 `&lt;`、`&gt;`、`&amp;`。
- 嚴格依 `_AUTHOR_GUIDE.md` 骨架:`eyebrow`(固定「第十九部 · SICP:抽象的建構」)/ `h1` / `subtitle` / `byline` / `objectives` / 多個 `h2`(每章 ≥ 8)/ `callout` / `exercise`(每章 3–6 題,附 `<details class="solution">` 解答)/ `diagram`(內嵌 SVG)/ 章末「把這一章串起來」+ 一個指向 SICP 原著的延伸資源 `callout note`。
- 數學用 MathJax:行內 `$...$`,獨立 `$$...$$`。
- SVG 配色用主色盤:`#2f6f6a`、`#b4541f`、`#8b5cf6`、灰 `#8a929b`、淺底 `#e3efed`;`font-family="Inter, 'Noto Sans TC', sans-serif"`。
- **不要**:加 `<nav>`/側欄/上下一章(book.js 生成)、改 `<head>` CSS/JS 相對路徑、寫 `<style>` 區塊或 inline `style=`(SVG 屬性除外)。
- 編號:檔案 id `80-sicp-scheme`…`84-sicp-register-machines`;顯示 `num` `74`…`78`;`done: true`。
- 跨章連結用檔名:`href="80-sicp-scheme.html"`(用檔案 id,非章號)。
- 素材:`sicp.pdf`(883 頁 PDF)。各章標注的頁碼為 **PDF 頁**,用 `Read` 工具帶 `pages` 參數讀取對應段落,忠實取用 Scheme 範例。

---

## Task 1: 章節結構驗證腳本

**Files:**
- Create: `chapters/_validate_chapter.py`

**Interfaces:**
- Produces: 命令列工具 `python chapters/_validate_chapter.py <檔案...>`,全部通過回傳 exit 0、否則 1 並印出每個缺失。後續每個章節任務都用它當「測試」。

- [ ] **Step 1: 寫驗證腳本**

```python
#!/usr/bin/env python3
"""章節結構驗證:檢查章節是否符合 _AUTHOR_GUIDE.md 骨架與跳脫規範。
用法:python _validate_chapter.py <chapter.html> [more.html ...]"""
import sys, re, os

REQUIRED = [
    ('<!DOCTYPE html>', 'DOCTYPE'),
    ('class="eyebrow"', 'eyebrow 區塊'),
    ('class="subtitle"', 'subtitle'),
    ('class="byline"', 'byline'),
    ('class="objectives"', 'objectives 區塊'),
    ('把這一章串起來', '章末總結小節'),
    ('../assets/style.css', 'CSS 連結'),
    ('../assets/book.js', 'book.js 連結'),
]

def check(path):
    src = open(path, encoding='utf-8').read()
    errs = []
    for needle, label in REQUIRED:
        if needle not in src:
            errs.append(f'缺少 {label}({needle})')
    h1 = len(re.findall(r'<h1[ >]', src))
    if h1 != 1:
        errs.append(f'<h1> 應恰好 1 個,實際 {h1}')
    h2 = len(re.findall(r'<h2[ >]', src))
    if h2 < 8:
        errs.append(f'<h2> 至少 8 個,實際 {h2}')
    if re.search(r'<style[ >]', src):
        errs.append('不得使用 <style> 區塊')
    for i, code in enumerate(re.findall(r'<code[^>]*>(.*?)</code>', src, re.S)):
        stripped = re.sub(r'&(lt|gt|amp|quot|apos|#\d+|#x[0-9a-fA-F]+);', '', code)
        if '<' in stripped or '>' in stripped:
            snippet = code[:60].replace('\n', ' ')
            errs.append(f'第 {i+1} 個 <code> 內有未跳脫的 < 或 >:{snippet!r}')
    chdir = os.path.dirname(path) or '.'
    for href in re.findall(r'href="([0-9][^"]*\.html)"', src):
        if not os.path.exists(os.path.join(chdir, href)):
            errs.append(f'跨章連結目標不存在:{href}')
    return errs

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法:python _validate_chapter.py <chapter.html> ...'); sys.exit(2)
    bad = False
    for p in sys.argv[1:]:
        errs = check(p)
        if errs:
            bad = True
            print(f'✗ {p}')
            for e in errs:
                print(f'   - {e}')
        else:
            print(f'✓ {p}')
    sys.exit(1 if bad else 0)
```

- [ ] **Step 2: 對既有章節驗證,確認腳本對「合格章節」會通過**

Run: `python chapters/_validate_chapter.py chapters/06-functional-programming.html`
Expected: `✓ chapters/06-functional-programming.html`、exit 0。
(若失敗,代表 REQUIRED 名單與既有約定不符,調整腳本而非章節。)

- [ ] **Step 3: Commit**

```bash
git add chapters/_validate_chapter.py
git commit -m "chore(textbook): add chapter structure validator for SICP part"
```

---

## Task 2: 第 74 章「Scheme 導引與程序抽象」+ 註冊新部

**Files:**
- Modify: `assets/book.js`(在 CTF part 物件之後、附錄 part 物件之前插入新 part,先只含本章條目)
- Create: `chapters/80-sicp-scheme.html`
- Test: `chapters/_validate_chapter.py`

**Interfaces:**
- Consumes: Task 1 的驗證腳本。
- Produces: 新 part 物件 `第十九部 · SICP:抽象的建構`(`icon: "λ"`),其 `chapters` 陣列含第一筆 `{ id: "80-sicp-scheme", num: "74", ... done: true }`。後續 Task 3–6 會往同一 `chapters` 陣列追加條目。

**內容規格(對應 SICP 第 1 章,PDF 頁碼)**
- h2 ①「為什麼是 Lisp:程式即資料」— history callout:Lisp 1958、McCarthy;一句點出本部主線。
- h2 ②「Scheme 五分鐘」— 前綴記法、`(define ...)`、求值組合規則(PDF 35–43)。Scheme 範例:`(+ 1 2)`、`(define (square x) (* x x))`。
- h2 ③「代換模型(substitution model)」— applicative vs normal order 直覺(PDF 46–50);callout 連 `03-functions-recursion.html` 呼叫堆疊。
- h2 ④「條件、謂詞與牛頓法求平方根」— `cond`/`if`、`sqrt-iter`(PDF 50–60);callout 連 `55-numerical-methods.html`。
- h2 ⑤「程序產生的處理程序」— 線性遞迴/迭代、尾遞迴、樹狀遞迴(費氏)、成長量級(PDF 69–84);MathJax `$O(n)$`/`$\Theta(\phi^n)$`;連 `26-complexity.html`。
- h2 ⑥「用高階程序建立抽象」— 程序當參數(`sum`)、`lambda`、回傳程序、固定點(PDF 104–130);連 `06-functional-programming.html`。
- h2 ⑦「Python 對照」— 同一組抽象用 Python 高階函式表達。
- h2 ⑧「把這一章串起來」+ 延伸資源 callout(指向 SICP 第 1 章)。
- diagram:遞迴 vs 迭代的處理程序展開圖(SVG)。
- exercise:3–6 題(尾遞迴改寫、`sum` 推廣、固定點求 √x),附 Scheme 解答。

- [ ] **Step 1: 在 book.js 插入新 part(只含本章)**

在 `assets/book.js` 中,於「第十八部 · 實戰資安 CTF」物件的結尾 `},`(現約第 217 行)與「附錄 · 完整題庫」物件的開頭 `{`(現約第 218 行)之間,插入:

```js
    {
      part: "第十九部 · SICP:抽象的建構",
      icon: "λ",
      blurb: "從序對到自我直譯器——用 Scheme 重走經典《SICP》,看抽象如何層層長出一台會思考的機器。",
      chapters: [
        { id: "80-sicp-scheme", num: "74", title: "Scheme 導引與程序抽象", en: "Scheme & Procedural Abstraction", done: true },
      ],
    },
```

- [ ] **Step 2: 檢查 book.js 語法**

Run: `node --check assets/book.js`
Expected: 無輸出、exit 0。

- [ ] **Step 3: 撰寫 `chapters/80-sicp-scheme.html`**

依 `_AUTHOR_GUIDE.md` 骨架與上方「內容規格」撰寫完整章節。`eyebrow` 文字固定「第十九部 · SICP:抽象的建構」,`byline` 標「第 74 章」。先用 `Read sicp.pdf pages "35-60"` 與 `"69-130"` 取材,Scheme 範例忠實取自原著。所有 code 跳脫 `<`/`>`/`&`。

- [ ] **Step 4: 驗證結構**

Run: `python chapters/_validate_chapter.py chapters/80-sicp-scheme.html`
Expected: `✓ chapters/80-sicp-scheme.html`、exit 0。

- [ ] **Step 5: 瀏覽器檢查**

開 `index.html` →「第十九部」出現在第十八部 CTF 之後、附錄之前 → 點第 74 章可開 → 右側 TOC 由 h2/h3 生成 → Scheme 程式碼上色 → 切深/淺色主題上色同步 → 無破版。

- [ ] **Step 6: Commit**

```bash
git add assets/book.js chapters/80-sicp-scheme.html
git commit -m "feat(textbook): add ch74 Scheme & procedural abstraction (SICP part 1)"
```

---

## Task 3: 第 75 章「用資料建立抽象:從抽象屏障到資料導向」

**Files:**
- Modify: `assets/book.js`(往第十九部 `chapters` 陣列追加本章條目)
- Create: `chapters/81-sicp-data.html`
- Test: `chapters/_validate_chapter.py`

**Interfaces:**
- Consumes: Task 2 建立的第十九部 part 物件。
- Produces: book.js 條目 `{ id: "81-sicp-data", num: "75", ... done: true }`。

**內容規格(對應 SICP 第 2 章,PDF 頁碼)**
- h2 ① `cons`/`car`/`cdr` 與序對(PDF 140)。
- h2 ②「抽象屏障」— 有理數 `make-rat`/`numer`/`denom`(PDF 141–150)。
- h2 ③「用序對建構一切」— list、樹、closure property(PDF 160–180);diagram:box-and-pointer SVG。
- h2 ④「序列作為慣用介面」— `map`/`filter`/`accumulate` 訊號流(PDF 182–199);連 `06-functional-programming.html`;diagram:訊號流圖。
- h2 ⑤「符號資料與引用」— `quote`、符號微分 `deriv`(PDF 220–231);連 `12-calculus.html`。
- h2 ⑥「多重表示與標籤資料」— 複數直角/極座標、`attach-tag`(PDF 257–269)。
- h2 ⑦「資料導向程式設計與可加性」★ — `put`/`get` dispatch table(PDF 270–281)。
- h2 ⑧「帶泛型運算的系統」— 型別塔、強制轉型(PDF 282–300)。
- h2 ⑨「Python 對照」— dict dispatch / `functools.singledispatch`。
- h2 ⑩「把這一章串起來」+ 延伸資源 callout(SICP 第 2 章)+ callout 連 `10-design-patterns.html`(資料導向 vs 策略模式)。
- exercise:3–6 題(為 `make-rat` 化簡、加一種複數表示、用 data-directed 加新運算),附 Scheme 解答。

- [ ] **Step 1: 追加 book.js 條目**

在第十九部的 `chapters` 陣列、第 74 章那行之後加入:

```js
        { id: "81-sicp-data", num: "75", title: "用資料建立抽象:從抽象屏障到資料導向", en: "Building Abstractions with Data", done: true },
```

- [ ] **Step 2: 檢查語法** — Run: `node --check assets/book.js`;Expected: exit 0。
- [ ] **Step 3: 撰寫 `chapters/81-sicp-data.html`** — 依骨架與內容規格;`byline` 標「第 75 章」;取材 `Read sicp.pdf pages "140-180"`、`"182-200"`、`"220-300"`。
- [ ] **Step 4: 驗證** — Run: `python chapters/_validate_chapter.py chapters/81-sicp-data.html`;Expected: `✓`、exit 0。
- [ ] **Step 5: 瀏覽器檢查** — 第 75 章可開、TOC 正確、box-and-pointer / 訊號流 SVG 正常、上色正常、73→74→75 上下章串接正確。
- [ ] **Step 6: Commit**

```bash
git add assets/book.js chapters/81-sicp-data.html
git commit -m "feat(textbook): add ch75 data abstraction & data-directed programming (SICP part 2)"
```

---

## Task 4: 第 76 章「狀態、環境模型與串流」

**Files:**
- Modify: `assets/book.js`
- Create: `chapters/82-sicp-state-streams.html`
- Test: `chapters/_validate_chapter.py`

**Interfaces:**
- Consumes: Task 2 part 物件。
- Produces: book.js 條目 `{ id: "82-sicp-state-streams", num: "76", ... done: true }`。

**內容規格(對應 SICP 第 3 章,PDF 頁碼)**
- h2 ①「賦值與區域狀態」— 用閉包 + `set!` 造 `make-account`(PDF 324–332)。
- h2 ②「引入賦值的代價」— 同一性與變動、參照透明性破滅(PDF 333–347)。
- h2 ③「環境模型」★ — 框架、綁定、求值規則(PDF 348–360);diagram:環境框架 SVG(`make-account` 呼叫的框架鏈)。
- h2 ④「可變資料」— 佇列、表格(`set-car!`/`set-cdr!`)。
- h2 ⑤「並行:時間即本質」— serializer 直覺(輕量);connect callout `43-parallel.html`。
- h2 ⑥「串流:延遲串列」— `delay`/`force`、`cons-stream`(PDF 456–468)。
- h2 ⑦「無限串流」— 整數流、`sieve` 質數、費氏、近似 e(PDF 469–497)。
- h2 ⑧「串流 vs 物件」— 兩種模組化(PDF 498–514)。
- h2 ⑨「Python 對照」— generator/`yield` 就是串流;閉包計數器。
- h2 ⑩「把這一章串起來」+ 延伸資源 callout(SICP 第 3 章)+ callout 連 `44-haskell.html`(惰性)。
- exercise:3–6 題(`make-account` 加密碼、用串流產生質數、`integers-from`),附 Scheme 解答。

- [ ] **Step 1: 追加 book.js 條目**

```js
        { id: "82-sicp-state-streams", num: "76", title: "狀態、環境模型與串流", en: "State, Environments & Streams", done: true },
```

- [ ] **Step 2: 檢查語法** — Run: `node --check assets/book.js`;Expected: exit 0。
- [ ] **Step 3: 撰寫 `chapters/82-sicp-state-streams.html`** — `byline` 標「第 76 章」;取材 `Read sicp.pdf pages "324-360"`、`"456-514"`。環境模型 SVG 必畫。
- [ ] **Step 4: 驗證** — Run: `python chapters/_validate_chapter.py chapters/82-sicp-state-streams.html`;Expected: `✓`。
- [ ] **Step 5: 瀏覽器檢查** — 第 76 章可開、環境框架 SVG 正常、TOC、上色、上下章串接。
- [ ] **Step 6: Commit**

```bash
git add assets/book.js chapters/82-sicp-state-streams.html
git commit -m "feat(textbook): add ch76 state, environment model & streams (SICP part 3)"
```

---

## Task 5: 第 77 章「後設循環直譯器:用 Lisp 寫 Lisp」

**Files:**
- Modify: `assets/book.js`
- Create: `chapters/83-sicp-metacircular.html`
- Test: `chapters/_validate_chapter.py`

**Interfaces:**
- Consumes: Task 2 part 物件。
- Produces: book.js 條目 `{ id: "83-sicp-metacircular", num: "77", ... done: true }`。

**內容規格(對應 SICP 第 4 章,PDF 頁碼)**
- h2 ①「直譯器是什麼:eval 與 apply 的雙人舞」★ — 概念開場(PDF 515–521);diagram:eval/apply 互遞迴 SVG 環。
- h2 ②「求值器核心」— `eval`/`apply` 程式碼(PDF 522–528)。
- h2 ③「表示運算式」— `tagged-list?`、`self-evaluating?`、特殊形式(PDF 529–544)。
- h2 ④「求值器的資料結構:環境」— `lookup`/`extend-environment`(PDF 540–544)。
- h2 ⑤「把直譯器當程式跑」— driver loop、global env(PDF 545–553)。
- h2 ⑥「程式即資料」— data as programs、Halting/eval 哲學(PDF 550–561)。
- h2 ⑦「變體一:惰性求值」— normal vs applicative、`delay-it`/`force-it`(PDF 569–586)。
- h2 ⑧「變體二:非確定計算 amb」— `amb`、搜尋與回溯、八皇后/畢氏(PDF 587–621)。
- h2 ⑨ callout 連 `42-compilers.html`(直譯 vs 編譯)、`45-prolog.html`(amb/查詢系統)。
- h2 ⑩「把這一章串起來」+ 延伸資源 callout(SICP 第 4 章)。
- exercise:3–6 題(加一個特殊形式如 `let`、把求值器改惰性、用 `amb` 解邏輯謎題),附 Scheme 解答。實作型練習以「mini-evaluator」為高潮。

- [ ] **Step 1: 追加 book.js 條目**

```js
        { id: "83-sicp-metacircular", num: "77", title: "後設循環直譯器:用 Lisp 寫 Lisp", en: "The Metacircular Evaluator", done: true },
```

- [ ] **Step 2: 檢查語法** — Run: `node --check assets/book.js`;Expected: exit 0。
- [ ] **Step 3: 撰寫 `chapters/83-sicp-metacircular.html`** — `byline` 標「第 77 章」;取材 `Read sicp.pdf pages "515-561"`、`"569-621"`。eval/apply 互遞迴 SVG 必畫;`eval`/`apply` 核心碼忠實呈現並跳脫。
- [ ] **Step 4: 驗證** — Run: `python chapters/_validate_chapter.py chapters/83-sicp-metacircular.html`;Expected: `✓`。
- [ ] **Step 5: 瀏覽器檢查** — 第 77 章可開、eval/apply SVG 正常、長 Scheme 區塊上色正常、無未跳脫 `<`。
- [ ] **Step 6: Commit**

```bash
git add assets/book.js chapters/83-sicp-metacircular.html
git commit -m "feat(textbook): add ch77 the metacircular evaluator (SICP part 4)"
```

---

## Task 6: 第 78 章「暫存器機器與顯式控制求值器」

**Files:**
- Modify: `assets/book.js`
- Create: `chapters/84-sicp-register-machines.html`
- Test: `chapters/_validate_chapter.py`

**Interfaces:**
- Consumes: Task 2 part 物件。
- Produces: book.js 條目 `{ id: "84-sicp-register-machines", num: "78", ... done: true }`(第十九部最後一章)。

**內容規格(對應 SICP 第 5 章,PDF 頁碼)**
- h2 ①「從高階到機器:暫存器機器模型」(PDF 694–699);diagram:資料路徑 + 控制器 SVG。
- h2 ②「描述暫存器機器的語言;用堆疊實作遞迴」(PDF 700–723)。
- h2 ③「暫存器機器模擬器」— `make-machine`、assembler 概念(PDF 724–750)。
- h2 ④「儲存配置與垃圾回收」— mark-sweep / stop-and-copy(PDF 751–768);連 `24-operating-system.html`、`42-compilers.html`。
- h2 ⑤「顯式控制求值器」— 把 metacircular evaluator 降到暫存器層、尾遞迴(PDF 769–794);連 `83-sicp-metacircular.html`。
- h2 ⑥「編譯:把 Scheme 編成暫存器指令」(PDF 795–861);連 `42-compilers.html`、`21-cpu-machine-language.html`。
- h2 ⑦「大圖:從 NAND 到直譯器」— 全書串接(連 `19-boolean-logic.html`…`23-vm-compiler.html`)。
- h2 ⑧「把這一章串起來」+ 延伸資源 callout(SICP 第 5 章 + 全書收尾)。
- exercise:3–6 題(畫 GCD 暫存器機器、追蹤堆疊深度、stop-and-copy 推演),附解答。

- [ ] **Step 1: 追加 book.js 條目**

```js
        { id: "84-sicp-register-machines", num: "78", title: "暫存器機器與顯式控制求值器", en: "Register Machines & EC-Evaluator", done: true },
```

- [ ] **Step 2: 檢查語法** — Run: `node --check assets/book.js`;Expected: exit 0。
- [ ] **Step 3: 撰寫 `chapters/84-sicp-register-machines.html`** — `byline` 標「第 78 章」;取材 `Read sicp.pdf pages "694-768"`、`"769-861"`。資料路徑 SVG 必畫。
- [ ] **Step 4: 驗證** — Run: `python chapters/_validate_chapter.py chapters/84-sicp-register-machines.html`;Expected: `✓`。
- [ ] **Step 5: 瀏覽器檢查** — 第 78 章可開、SVG 正常、78 → 附A(74-bank-ap325)上下章串接正確。
- [ ] **Step 6: Commit**

```bash
git add assets/book.js chapters/84-sicp-register-machines.html
git commit -m "feat(textbook): add ch78 register machines & EC-evaluator (SICP part 5)"
```

---

## Task 7: 既有章節互連 callout

**Files:**
- Modify: `chapters/03-functions-recursion.html`、`chapters/06-functional-programming.html`、`chapters/10-design-patterns.html`、`chapters/44-haskell.html`、`chapters/42-compilers.html`、`chapters/45-prolog.html`(各加一個 callout,不改既有內文)

**Interfaces:**
- Consumes: Task 2–6 已建立的章節檔(連結目標必須存在)。
- Produces: 既有章節指向第十九部的 6 個互連 callout。

每個 callout 用 `note` 型樣式,放在相關小節結尾。模板(以 03 為例,其餘改連結與文案):

```html
<div class="callout note"><div class="ico">📚</div><div class="body">
<span class="c-title">想看另一種視角?</span><p>SICP 用代換模型與環境模型解釋「函式呼叫到底發生什麼事」,延伸閱讀
<a href="80-sicp-scheme.html">第 74 章 · Scheme 導引與程序抽象</a>。</p></div></div>
```

互連對照(連結用檔名 id):
| 檔案 | 連到 | 文案重點 |
|---|---|---|
| `03-functions-recursion.html` | `80-sicp-scheme.html` | 代換模型/環境模型看函式呼叫 |
| `06-functional-programming.html` | `80-sicp-scheme.html` | 高階程序與固定點的 Scheme 源頭 |
| `10-design-patterns.html` | `81-sicp-data.html` | 資料導向程式設計 vs 策略模式 |
| `44-haskell.html` | `82-sicp-state-streams.html` | 串流即惰性串列 |
| `42-compilers.html` | `83-sicp-metacircular.html` | metacircular vs 顯式控制求值器 |
| `45-prolog.html` | `83-sicp-metacircular.html` | amb / 查詢系統的實作 |

- [ ] **Step 1: 在 6 個既有章節各插入一個 callout**(依上表,放在語意相關的小節末尾)。
- [ ] **Step 2: 驗證 6 章連結目標都存在**

Run: `python chapters/_validate_chapter.py chapters/03-functions-recursion.html chapters/06-functional-programming.html chapters/10-design-patterns.html chapters/44-haskell.html chapters/42-compilers.html chapters/45-prolog.html`
Expected: 6 個 `✓`、exit 0。

- [ ] **Step 3: 瀏覽器檢查** — 隨機點 2–3 個新 callout 連結,確認跳到正確新章。
- [ ] **Step 4: Commit**

```bash
git add chapters/03-functions-recursion.html chapters/06-functional-programming.html chapters/10-design-patterns.html chapters/44-haskell.html chapters/42-compilers.html chapters/45-prolog.html
git commit -m "docs(textbook): cross-link existing chapters to new SICP part"
```

---

## Task 8: 全書整合驗收

**Files:** 無(僅驗證)

- [ ] **Step 1: 全 5 章一起跑驗證器**

Run: `python chapters/_validate_chapter.py chapters/80-sicp-scheme.html chapters/81-sicp-data.html chapters/82-sicp-state-streams.html chapters/83-sicp-metacircular.html chapters/84-sicp-register-machines.html`
Expected: 5 個 `✓`、exit 0。

- [ ] **Step 2: book.js 最終語法檢查** — Run: `node --check assets/book.js`;Expected: exit 0。

- [ ] **Step 3: 瀏覽器全流程驗收**(對照 spec §6)

1. 側欄「第十九部 · SICP:抽象的建構」在第十八部之後、附錄之前。
2. 第 74–78 章皆可開、右側 TOC 由 h2/h3 生成且層級正確。
3. Scheme 程式碼上色;切深/淺色主題上色同步。
4. 無未跳脫 `<` 破版。
5. 上下章串接:73 ↔ 74 … 78 ↔ 附A。
6. 既有章節互連 callout 連結正確。

- [ ] **Step 4: 更新記憶**

更新 `cs-textbook-project` 記憶:章數由 80 增為 85,新增「第十九部 · SICP」。

---

## Self-Review(計畫 vs spec 覆蓋檢查)

- spec §1.1 八個缺口:#1#5#8→Task 3;#2#6→Task 5;#3#4→Task 4(+#4 環境模型);#7→Task 6;#8 代換模型/符號資料分散於 Task 2/3。✅ 全覆蓋。
- spec §3.1 新 part 註冊→Task 2 Step 1;§3.2 編號規則→各任務條目;§3.4 互連→Task 7。✅
- spec §4 五章小節→Task 2–6 內容規格逐章對應。✅
- spec §5 慣例(跳脫/上色/MathJax/SVG/done)→Global Constraints + 驗證器。✅
- spec §6 驗收→Task 8。✅
- Placeholder 掃描:無 TBD/TODO;驗證器程式碼完整;每章內容規格給到「小節 + 範例 + PDF 頁 + 圖 + 練習」層級(章節 prose 為撰寫產出,非計畫佔位)。
- 型別/命名一致:檔名 id `80–84`、章號 `74–78`、跨章連結用檔名 id,全計畫一致。
