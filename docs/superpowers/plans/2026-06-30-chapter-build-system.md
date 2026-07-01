# 章節建置系統(內容/版型分離) 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把章節的共用外殼(head/wrapper/script)抽成單一模板 `chapters/_layout.html`,章節內容改存為 `chapters/src/*.html` 片段,由 `build.py` 產生 `chapters/*.html`;一次性遷移現有 85 章,且(除 3 處刻意修正外)產出與原檔 byte-identical。

**Architecture:** 三層——`_layout.html`(共用外殼,含 `{{TITLE}}`/`{{DESCRIPTION}}`/`{{SCRIPTS}}`/`{{CONTENT}}` 佔位)、`chapters/src/NN.html`(內容片段 + `<!--meta-->` 前置區,來源真相)、`build.py`(字面字串代入 + 跑驗證器)。模板由既有章 `01-what-is-cs.html` 程式化派生以保證 byte-fidelity。遷移用一次性 `migrate.py`。

**Tech Stack:** Python 3(專案已有 `_build_toi_*.py`、`_validate_chapter.py` 慣例);Git Bash 可用 `cmp`/`diff`;`node --check` 不涉及。無 pytest——以 byte 比對與往返測試為「測試」。

## Global Constraints

- **行尾全程保留 CRLF**:所有讀寫一律 `open(..., encoding='utf-8', newline='')`,不做行尾翻譯(F2)。
- **字面字串代入**(非 `str.format`/`%`),`{{CONTENT}}` 最後代入、不再掃描(避免內容含 `{`/`}` 出錯)。
- **模板派生自 `01-what-is-cs.html`**,不手打 head,確保與既有章逐字一致。
- **遷移 diff 只允許 3 類刻意修正**:(a)`82/83/84-sicp-*.html` 補上 4 行標準字型連結(F1);(b)`74-bank-ap325.html` 標題後綴正規化為「 · CS 自學聖經」(原本 `·` 前無空格,F3);其餘 82 章必須 byte-identical。
- 不改 `book.js`/`index.html`/`style.css`/`assets/`/輸出檔名;`index.html` 不納入(非章節)。
- 唯一特例章 `79-bank-toi.html`:額外 3 支 TOI script(`toi/toi-index.js, toi/toi-statements.js, toi/toi-render.js`)經 meta `scripts:` + 模板 `{{SCRIPTS}}` 還原。
- 產出 `chapters/*.html` 照舊 commit;不加 GENERATED 提示行;來源真相靠 `chapters/src/` 目錄 + `_AUTHOR_GUIDE.md` 說明。
- **驗證為選用(advisory),非建置閘門**:現有 85 章中約 27 章不符嚴格驗證器規則(短章 h2 不足、序章無「串起來」、題庫章資料驅動、舊章程式碼寬鬆跳脫)。**為過驗證而改動這些章的內容會破壞 byte-identical,絕對禁止**。故 `build.py` 只組裝(永遠 exit 0),驗證改由 `build.py --check [章]` 明確執行,供新章作者自檢。
- 工作目錄:`C:\我的筆記\computer-science\textbook`。

---

## Task 1: `_layout.html` 模板 + `build.py` 產生器核心

**Files:**
- Create: `chapters/_layout.html`(由 `01-what-is-cs.html` 派生)
- Create: `build.py`

**Interfaces:**
- Produces:
  - `build.py` 可被匯入的函式:`read(path)->str`、`write(path,text)`、`parse_fragment(text,name)->(meta:dict, content:str)`、`scripts_html(meta)->str`、`render(layout,meta,content)->str`、`build_one(src_path,layout)->out_path`。
  - CLI:`python build.py`(建全部 src)、`python build.py NN-slug`(建單章)、`python build.py --check`(只對 `chapters/*.html` 跑驗證器)。
  - 模板佔位:`{{TITLE}}`、`{{DESCRIPTION}}`、`{{SCRIPTS}}`、`{{CONTENT}}`。

- [ ] **Step 1:派生 `_layout.html`(以 01 為基準,保證 byte-fidelity)**

執行下列腳本(產生模板後即可丟棄此腳本):

```bash
python - <<'PY'
import re
src = open('chapters/01-what-is-cs.html', encoding='utf-8', newline='').read()
t = re.sub(r'(<title>).*?( · CS 自學聖經</title>)', r'\1{{TITLE}}\2', src, count=1, flags=re.S)
t = re.sub(r'(<meta name="description" content=").*?(">)', r'\1{{DESCRIPTION}}\2', t, count=1, flags=re.S)
t = re.sub(r'(<article class="content">).*(</article>)', r'\1{{CONTENT}}\2', t, count=1, flags=re.S)
t = t.replace('<script src="../assets/book.js"></script>',
              '{{SCRIPTS}}<script src="../assets/book.js"></script>', 1)
open('chapters/_layout.html', 'w', encoding='utf-8', newline='').write(t)
print('OK, placeholders:', [p for p in ('{{TITLE}}','{{DESCRIPTION}}','{{SCRIPTS}}','{{CONTENT}}') if p in t])
PY
```
Expected:`OK, placeholders: ['{{TITLE}}', '{{DESCRIPTION}}', '{{SCRIPTS}}', '{{CONTENT}}']`(四個佔位都在)。

- [ ] **Step 2:寫 `build.py`**

```python
#!/usr/bin/env python3
"""由 chapters/src/*.html 片段 + chapters/_layout.html 模板,產生 chapters/*.html。
行尾全程 newline='' 不翻譯(保留 CRLF);字面代入,{{CONTENT}} 最後代入。
用法:
  python build.py             產生全部 src/*.html
  python build.py 01-what-is-cs   只產生該章
  python build.py --check     對 chapters/*.html 跑驗證器,不寫檔
"""
import sys, os, re, glob, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(ROOT, 'chapters')
SRC = os.path.join(CH, 'src')
LAYOUT_PATH = os.path.join(CH, '_layout.html')
VALIDATOR = os.path.join(CH, '_validate_chapter.py')

META_RE = re.compile(r'\A<!--meta\r?\n(.*?)\r?\n-->\r?\n', re.S)

def read(path):
    with open(path, encoding='utf-8', newline='') as f:
        return f.read()

def write(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)

def parse_fragment(text, name):
    m = META_RE.match(text)
    if not m:
        raise ValueError(f'{name}: 片段開頭缺少 <!--meta ... --> 前置區')
    meta = {}
    for line in m.group(1).split('\n'):
        line = line.rstrip('\r')
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    for key in ('title', 'description'):
        if key not in meta:
            raise ValueError(f'{name}: meta 缺少必填欄位 {key}')
    return meta, text[m.end():]

def scripts_html(meta):
    raw = meta.get('scripts', '').strip()
    if not raw:
        return ''
    parts = [p.strip() for p in raw.split(',') if p.strip()]
    return ''.join(f'<script src="../assets/{p}"></script>\r\n' for p in parts)

def render(layout, meta, content):
    out = layout
    out = out.replace('{{TITLE}}', meta['title'])
    out = out.replace('{{DESCRIPTION}}', meta['description'])
    out = out.replace('{{SCRIPTS}}', scripts_html(meta))
    out = out.replace('{{CONTENT}}', content)  # 最後代入,不再掃描
    return out

def build_one(src_path, layout):
    name = os.path.basename(src_path)
    meta, content = parse_fragment(read(src_path), name)
    out_path = os.path.join(CH, name)
    write(out_path, render(layout, meta, content))
    return out_path

def validate(paths):
    return subprocess.run([sys.executable, VALIDATOR, *paths]).returncode

def main(argv):
    if argv and argv[0] == '--check':         # 選用的 lint;接受指定章或全部
        names = argv[1:]
        if names:
            outs = [os.path.join(CH, n if n.endswith('.html') else n + '.html') for n in names]
        else:
            outs = [p for p in sorted(glob.glob(os.path.join(CH, '*.html')))
                    if not os.path.basename(p).startswith('_')]
        sys.exit(validate(outs))
    layout = read(LAYOUT_PATH)
    if argv:
        srcs = [os.path.join(SRC, a if a.endswith('.html') else a + '.html') for a in argv]
    else:
        srcs = sorted(glob.glob(os.path.join(SRC, '*.html')))
    if not srcs:
        print('沒有找到任何 src 片段。'); sys.exit(0)
    outs = []
    for s in srcs:
        if not os.path.exists(s):
            print(f'找不到片段:{s}'); sys.exit(2)
        outs.append(build_one(s, layout))
    # 驗證為「選用」,不阻擋組裝:現有 85 章有 27 章不符嚴格規則(短章 h2 不足、
    # 序章無「串起來」、題庫章資料驅動、舊章程式碼寬鬆跳脫),強修會破壞 byte-identical。
    print(f'已產生 {len(outs)} 章。(結構/跳脫自檢為選用:python build.py --check [章])')
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
```

- [ ] **Step 3:寫 in-memory 往返測試(此刻應「失敗」前先確認核心可跑)**

建立暫時測試腳本驗證「模板 + parse + render」對 01 章 byte-identical:

```bash
python - <<'PY'
import re, build
orig = build.read('chapters/01-what-is-cs.html')
layout = build.read('chapters/_layout.html')
title = re.search(r'<title>(.*?) · CS 自學聖經</title>', orig, re.S).group(1)
desc  = re.search(r'<meta name="description" content="(.*?)">', orig, re.S).group(1)
content = re.search(r'<article class="content">(.*)</article>', orig, re.S).group(1)
out = build.render(layout, {'title': title, 'description': desc}, content)
assert out == orig, '往返不一致!長度 %d vs %d' % (len(out), len(orig))
print('PASS:01 章 in-memory 往返 byte-identical')
PY
```
Expected:`PASS:01 章 in-memory 往返 byte-identical`(`import build` 需在 textbook 根目錄執行)。
若 AssertionError,代表模板派生有空白/行尾偏差,回 Step 1 檢查(通常是行尾或 article 邊界)。

- [ ] **Step 4:確認 CLI 行為(無 src 時不爆)**

Run:`python build.py`
Expected:印出 `沒有找到任何 src 片段。`、exit 0(此時 `chapters/src/` 尚未建立)。

- [ ] **Step 5:Commit**

```bash
git add build.py chapters/_layout.html
git commit -m "feat(textbook): add _layout.html template and build.py generator"
```

---

## Task 2: `migrate.py` 一次性遷移腳本

**Files:**
- Create: `migrate.py`
- Test:(往返)`chapters/src/01-what-is-cs.html` → `build.py` → 與原 01 byte 比對

**Interfaces:**
- Consumes: Task 1 的 `build.py`(往返驗證)。
- Produces:`migrate.py` 函式 `extract(html,name)->(title,description,scripts:list,content)`、`to_fragment(title,description,scripts,content)->str`、`migrate_one(html_path)->name`;CLI `python migrate.py [NN-slug ...]`。寫出 `chapters/src/NN.html`。

- [ ] **Step 1:寫 `migrate.py`**

```python
#!/usr/bin/env python3
"""一次性:把現有 chapters/NN.html 拆成 chapters/src/NN.html 內容片段。
保留 CRLF;標題去後綴容錯(F3);偵測額外 script(僅 79-bank-toi)。
用法:python migrate.py              遷移全部 chapters/*.html(排除 _layout.html)
      python migrate.py 01-what-is-cs   只遷移單章
"""
import sys, os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(ROOT, 'chapters')
SRC = os.path.join(CH, 'src')

TITLE_RE = re.compile(r'<title>(.*?)\s*·\s*CS 自學聖經\s*</title>', re.S)
DESC_RE = re.compile(r'<meta name="description" content="(.*?)">', re.S)
ARTICLE_RE = re.compile(r'<article class="content">(.*)</article>', re.S)
SCRIPT_RE = re.compile(r'<script src="\.\./assets/([^"]+)"></script>')

def read(path):
    with open(path, encoding='utf-8', newline='') as f:
        return f.read()

def write(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)

def extract(html, name):
    mt = TITLE_RE.search(html)
    if not mt:
        raise ValueError(f'{name}: 找不到符合格式的 <title>')
    md = DESC_RE.search(html)
    if not md:
        raise ValueError(f'{name}: 找不到 <meta name="description">')
    ma = ARTICLE_RE.search(html)
    if not ma:
        raise ValueError(f'{name}: 找不到 <article class="content">…</article>')
    scripts = [s for s in SCRIPT_RE.findall(html) if s != 'book.js']
    return mt.group(1), md.group(1), scripts, ma.group(1)

def to_fragment(title, description, scripts, content):
    meta = [f'title: {title}', f'description: {description}']
    if scripts:
        meta.append('scripts: ' + ', '.join(scripts))
    return '<!--meta\r\n' + '\r\n'.join(meta) + '\r\n-->\r\n' + content

def migrate_one(html_path):
    name = os.path.basename(html_path)
    title, description, scripts, content = extract(read(html_path), name)
    write(os.path.join(SRC, name), to_fragment(title, description, scripts, content))
    return name

def main(argv):
    os.makedirs(SRC, exist_ok=True)
    if argv:
        paths = [os.path.join(CH, a if a.endswith('.html') else a + '.html') for a in argv]
    else:
        paths = [p for p in sorted(glob.glob(os.path.join(CH, '*.html')))
                 if os.path.basename(p) != '_layout.html']
    for p in paths:
        print('遷移', migrate_one(p))

if __name__ == '__main__':
    main(sys.argv[1:])
```

- [ ] **Step 2:測試抽取正確性(含 F3 標題異例與 79 額外 script)**

```bash
python - <<'PY'
import migrate
# 一般章
t,d,s,c = migrate.extract(migrate.read('chapters/01-what-is-cs.html'), '01')
assert t == '什麼是計算、程式與演算法', repr(t)
assert s == [], s
assert c.strip().startswith('<div class="eyebrow"'), c[:60]
# F3:AP325 標題「(依章)· …」無空格
t2,_,_,_ = migrate.extract(migrate.read('chapters/74-bank-ap325.html'), '74')
assert t2 == 'AP325 完整題單(依章)', repr(t2)
# 79:三支 TOI script
_,_,s3,_ = migrate.extract(migrate.read('chapters/79-bank-toi.html'), '79')
assert s3 == ['toi/toi-index.js','toi/toi-statements.js','toi/toi-render.js'], s3
print('PASS:抽取(含 F3、79 script)正確')
PY
```
Expected:`PASS:抽取(含 F3、79 script)正確`。

- [ ] **Step 3:往返測試——遷移 01 → build → 與原檔 byte 比對**

```bash
cp chapters/01-what-is-cs.html /tmp/01.orig.html
python migrate.py 01-what-is-cs
python build.py 01-what-is-cs
cmp chapters/01-what-is-cs.html /tmp/01.orig.html && echo "PASS:01 往返 byte-identical"
git checkout chapters/01-what-is-cs.html   # 還原(此 task 不真正改章節)
rm -f chapters/src/01-what-is-cs.html
```
Expected:`cmp` 無輸出(相同)、印 `PASS:01 往返 byte-identical`。
(`cmp` 比對磁碟實際 bytes,對 git autocrlf 免疫——F2 的正確驗法。)

- [ ] **Step 4:Commit**

```bash
git add migrate.py
git commit -m "chore(textbook): add one-time migrate.py to split chapters into src fragments"
```

---

## Task 3: 全面遷移 85 章 + 無損驗收

**Files:**
- Create:`chapters/src/*.html`(85 個內容片段)
- Modify:`chapters/*.html`(85 個產出,其中 82/83/84/74 為刻意修正)

**Interfaces:**
- Consumes: Task 1 `build.py`、Task 2 `migrate.py`。

- [ ] **Step 1:備份現有 85 章(供 autocrlf-免疫的 byte 比對)**

```bash
BK="$LOCALAPPDATA/Temp/claude/chbk"; mkdir -p "$BK"
cp chapters/*.html "$BK"/
ls "$BK" | wc -l   # 應 85
```
(若 `$LOCALAPPDATA` 不可用,改用 `/tmp/chbk`。記住此備份路徑供 Step 4。)

- [ ] **Step 2:遷移全部 + 重新產生**

```bash
python migrate.py
ls chapters/src/*.html | wc -l    # 應 85
python build.py                   # 產生 85 章(不自動驗證,見下)
```
Expected:`migrate.py` 印 85 行「遷移 …」;`build.py` 印「已產生 85 章。(結構/跳脫自檢為選用…)」、exit 0。
**注意**:`build.py` 不再把驗證當閘門(現有 85 章中約 27 章不符嚴格規則:短章 h2 不足、序章無「串起來」、題庫章資料驅動、舊章程式碼寬鬆跳脫——這些是既有狀態,**不可為過驗證而改動內容,否則破壞 byte-identical**)。本任務的正確性以 Step 3–5 的 byte 比對為準,非驗證器。

- [ ] **Step 3:byte 比對——找出所有差異章(應只有 4 章)**

```bash
BK="$LOCALAPPDATA/Temp/claude/chbk"   # 或 /tmp/chbk
for f in chapters/*.html; do
  b="$BK/$(basename "$f")"
  cmp -s "$f" "$b" || echo "DIFF: $(basename "$f")"
done
```
Expected:**只列出 4 個檔**:`82-sicp-state-streams.html`、`83-sicp-metacircular.html`、`84-sicp-register-machines.html`、`74-bank-ap325.html`。
若出現其他章,代表遷移非無損——逐一 `diff "$BK/那章" 那章` 找原因(多半是行尾或 article 邊界的空白),修 `migrate.py`/`_layout.html` 後重跑 Step 2–3,直到只剩這 4 章。

- [ ] **Step 4:逐一確認那 4 章的差異「只是刻意修正」**

```bash
BK="$LOCALAPPDATA/Temp/claude/chbk"
for f in 82-sicp-state-streams 83-sicp-metacircular 84-sicp-register-machines; do
  echo "=== $f(應只多 4 行字型連結)==="; diff "$BK/$f.html" "chapters/$f.html"
done
echo "=== 74-bank-ap325(應只差標題 · 前一個空格)==="; diff "$BK/74-bank-ap325.html" chapters/74-bank-ap325.html
```
Expected:
- 三個 SICP 章:diff 僅顯示「新增 3 行 `<link rel="preconnect" …>` + 1 行 Google Fonts `<link>`」。
- AP325:diff 僅顯示 `<title>` 一行,差異是 `)·` → `) ·`(補一個空格)。
任何超出此範圍的差異都要回 Step 3 排查。

- [ ] **Step 5:冪等性——再 build 一次應無變化**

```bash
python build.py >/dev/null
git diff --stat chapters/*.html | tail -1   # 第二次 build 不應新增任何變動
```
Expected:相對 Step 2 後的狀態,第二次 `build.py` 不改變任何檔(冪等)。

- [ ] **Step 6:瀏覽器抽查(人工)**

開 `index.html`,抽查:
1. 任一般章(如第 1 章)畫面與遷移前一致。
2. `82/83/84`(SICP 第 76–78 章)現在字型正確(Noto/Inter,非系統 fallback)。
3. `79-bank-toi` 題庫頁正常載入(TOI 過濾/搜尋可用)——證明 3 支 script 還原成功。

- [ ] **Step 7:Commit**

```bash
git add chapters/src chapters/*.html
git commit -m "refactor(textbook): migrate all 85 chapters to src fragments + build output

內容片段移入 chapters/src/,由 _layout.html + build.py 產生。
除刻意修正外 byte-identical:82/83/84 補回標準字型連結(原漏)、
74-bank-ap325 標題後綴正規化。"
```

---

## Task 4: 作者指南更新 + .gitattributes + 收尾

**Files:**
- Create:`textbook/.gitattributes`(把章節檔釘成 CRLF,避免 autocrlf 行尾飄移)
- Modify:`_AUTHOR_GUIDE.md`(新增建置流程說明)
- Delete(可選):`migrate.py`(任務已完成)

**Interfaces:**
- Consumes: Task 1–3 的成品。

- [ ] **Step 0:建立 `textbook/.gitattributes`**

執行中發現 `80/81` 原為 LF、其餘 CRLF;git 已統一成 CRLF,但須釘住以免不同環境的 autocrlf 再造成飄移。建立 `textbook/.gitattributes`,內容(LF 檔本身、UTF-8):

```gitattributes
# 章節 HTML 與其來源片段、模板一律 CRLF,避免不同環境 autocrlf 造成行尾飄移
chapters/*.html        text eol=crlf
chapters/src/*.html    text eol=crlf
chapters/_layout.html  text eol=crlf
```
驗證:`git check-attr eol chapters/80-sicp-scheme.html` → 應印 `...: eol: crlf`。
(不做 `--renormalize`,避免大量無謂 churn;現有工作樹已是 CRLF。)

- [ ] **Step 1:在 `_AUTHOR_GUIDE.md` 開頭「0. 你的任務」區塊後,插入建置流程說明**

讀 `_AUTHOR_GUIDE.md` 確認 `## 0. 你的任務` 段落位置後,在其結尾插入:

```markdown

## 0.5 檔案結構與建置(務必遵守)
本書章節採「內容/版型分離」:
- **來源真相**是 `chapters/src/NN-slug.html`(內容片段:檔首 `<!--meta-->` 前置區含 `title`/`description`/選填 `scripts`,其後為 `<article>` 內文)。
- **不要直接編輯 `chapters/NN-slug.html`**(那是 `build.py` 的產出,會被覆寫)。
- 共用外殼(head/字型/CSS/包裹/book.js)在 `chapters/_layout.html`,**單一來源**;要改 head/字型就改這裡再 rebuild。
- 流程:寫/改 `chapters/src/NN-slug.html` → 在 `assets/book.js` 加章節條目(新章)→ 跑 `python build.py`(自動產生 HTML 並對全書跑 `chapters/_validate_chapter.py`)。
- 單章重建:`python build.py NN-slug`;只驗證:`python build.py --check`。
```

- [ ] **Step 2:健檢——build 仍可運作、--check 為選用 lint**

Run:`python build.py 06-functional-programming && python build.py --check 06-functional-programming`
Expected:build 印「已產生 1 章…」、exit 0;`--check 06-functional-programming` 印 `✓ chapters/06-functional-programming.html`、exit 0(以一個符合規則的章確認 lint 管線正常)。
(註:對全部 `--check` 會列出約 27 個既有章的警告——這是預期的既有狀態,非本系統的缺陷;新章作者應對自己的章跑 `--check`。)

- [ ] **Step 3:(可選)移除一次性 `migrate.py`**

```bash
git rm migrate.py
```
(其職責已完成;若想保留作紀錄可略過此步。)

- [ ] **Step 4:Commit**

```bash
git add textbook/.gitattributes textbook/_AUTHOR_GUIDE.md
git commit -m "chore(textbook): pin chapter line endings (.gitattributes) + document build workflow"
```
(若已於 Step 3 `git rm migrate.py`,該刪除一併納入本 commit 或另開 commit。)

---

## Self-Review(計畫 vs spec 覆蓋)

- spec §2 三層架構 → Task 1(layout+build)、Task 3(src 片段)。✅
- spec §3.1 模板/佔位/字型固定 → Task 1 Step 1(派生)。✅
- spec §3.2 片段 meta 格式 → Task 2 `to_fragment`。✅
- spec §3.3 build(字面代入、CRLF、跑驗證器、CLI)→ Task 1 `build.py`。✅
- spec §3.4 migrate(F3 容錯、CRLF、79 script)→ Task 2。✅
- spec §0/§5 驗收(只允許 F1 字型 + F3 標題兩類差異、autocrlf-免疫 byte 比對)→ Task 3 Step 3–5。✅
- spec §0 F2 CRLF → Global Constraints + 全程 `newline=''`。✅
- spec §6 新章流程、§9 來源真相說明 → Task 4 作者指南。✅
- spec §8 測試(無損/行尾/F1 修正/冪等)→ Task 3 Step 3–6。✅
- Placeholder 掃描:無 TBD;build.py/migrate.py 完整;每步有具體指令與預期輸出。
- 型別/命名一致:`read/write/parse_fragment/scripts_html/render/build_one`(build)、`extract/to_fragment/migrate_one`(migrate)跨 task 一致;佔位符 `{{TITLE/DESCRIPTION/SCRIPTS/CONTENT}}` 一致。
