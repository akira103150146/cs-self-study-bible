# 章節內容/版型分離 + 建置期產生器 — 設計文件

- 日期:2026-06-30
- 狀態:已核准設計,待寫實作計畫
- 背景:`textbook/` 下的中英對照 HTML 教科書目前有 85 個章節檔(`chapters/*.html`)。每章是完整 HTML,其 `<head>`(meta/字型/CSS)、`.layout>.main>.content` 包裹、`book.js` script **幾乎全部逐字複製**在 85 個檔案裡。共用結構靠「複製貼上 + 作者自律」維持,沒有單一來源,未來新增章節有飄移/不一致風險。

## 0. 設計檢視(實證)發現 — 已併入本 spec

動工前以實證壓力測試「重新產生 = byte-identical」此一命脈,得到 4 個發現,均已反映在下文:
- **F1(已是現存 bug)**:head **並非全章一致**——`82/83/84-sicp-*.html`(第 76/77/78 章,本專案上一輪新增)**漏掉字型 preconnect + Google Fonts 連結**,只剩 `style.css`,目前以 fallback 字型顯示。這正是「新增章節飄移」的活證據。**對策**:遷移時**順手補正**這 3 章的字型(視為刻意修正,非保留 bug)。因此驗收基準改為:遷移 diff **只應出現「82/83/84 補上標準字型連結」**,其餘 82 章 byte-identical。
- **F2(行尾)**:現有章節檔為 **CRLF**。`migrate.py`/`build.py` 必須**明確以 CRLF 寫出**,否則 `git diff` 會整檔每行變動或被 autocrlf 遮蔽,使 byte-identical 驗收失真。
- **F3(標題異例)**:`74-bank-ap325` 標題為「…(依章)· CS 自學聖經」(`·` 前無空格)。去後綴須容錯(regex `\s*·\s*CS 自學聖經$`)。
- **F4(已排除風險)**:每章 `</article>` 剛好 1 次、`<article class="content">` 寫法 85 章統一,內容抽取安全。
- **設計調整**:**取消 GENERATED 提示行**(原 §3.3),讓遷移 diff 僅含 F1 的刻意修正、losslessness 證明最純粹。來源關係改以 `chapters/src/` 目錄結構 + 本 spec/README 表達。

---

## 1. 目標與範圍

把「章節內容」與「網頁版型外殼」分離,讓共用外殼有**單一資料來源**,新增章節只需寫內容、由模板保證一致。

- **做**:抽出共用外殼成一份模板;每章內容改存為「內容片段」;用 `build.py` 產生獨立 HTML;一次性遷移現有 85 章;產出與現況畫面零差異。
- **不做**:不改 `book.js`、`index.html`、`style.css`、既有 nav/TOC/上下章機制;不改輸出檔名;不引入 Markdown(本案選用「純內容 HTML 片段」為來源);不改變「直接開檔(file://)」的使用習慣。
- **範圍**:全面遷移 85 章(84 章格式一致;`79-bank-toi` 為唯一特例,多載 3 支 TOI 資料腳本)。

### 1.1 決策紀錄(brainstorming 結論)
- 內容來源格式:**純內容 HTML 片段**(富元件零損失;不引入 Markdown 引擎)。備選 Markdown+directive / 混合,均否決(455 內嵌 SVG + 923 可摺疊練習轉換成本高、且使用者要的是「一致性與好維護」而非可攜)。
- 外殼套用方式:**建置期產生器**。備選「執行期 JS 注入」否決(FOUC 閃爍、檔案結構非標準、book.js 變複雜、SEO/分頁標題弱)。技術硬限制:純靜態 HTML 無原生 include,單一來源只能靠 build 或執行期 JS 二擇一。
- 範圍:**全面遷移 85 章**。備選「只給新章」「保留題庫章」否決(無法達成真正單一來源)。

---

## 2. 架構:三層,各司其職

| 檔案 | 職責 | 數量 |
|---|---|---|
| `chapters/_layout.html` | **共用外殼**:整段 head(meta/字型 preconnect/Google Fonts/CSS)、`<body>` 的 `.layout>.main>.content` 包裹、`book.js` script。含 `{{TITLE}}`/`{{DESCRIPTION}}`/`{{SCRIPTS}}`/`{{CONTENT}}` 佔位符 | 1 |
| `chapters/src/NN-slug.html` | **每章內容片段(來源真相)**:頂部 `<!--meta ... -->` 前置區 + `<article>` 內的完整內容(eyebrow 到最後一節) | 85 |
| `build.py` | **組裝**:讀 `_layout.html` + 每個片段 → 解析 meta、填模板 → 寫出 `chapters/NN-slug.html`,並對產出跑 `_validate_chapter.py` 把關 | 1 |
| `migrate.py` | **一次性遷移**:從現有 `chapters/NN.html` 抽出 content/title/description/scripts → 寫成 `chapters/src/NN.html`。用完即刪 | 1(暫時) |

`_validate_chapter.py`(已存在)維持不變,由 `build.py` 呼叫。

---

## 3. 元件設計

### 3.1 `chapters/_layout.html`(模板)
逐字對齊「現有章節的 head 與包裹格式」,確保重新產生的輸出與原檔 **byte-identical**。結構:

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}} · CS 自學聖經</title>
<meta name="description" content="{{DESCRIPTION}}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&family=Noto+Sans+TC:wght@400;700&family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<div class="layout">
  <main class="main">
    <article class="content">
{{CONTENT}}
    </article>
  </main>
</div>
{{SCRIPTS}}<script src="../assets/book.js"></script>
</body>
</html>
```

- `{{TITLE}}`:章節標題(模板自動補 ` · CS 自學聖經` 後綴)。
- `{{DESCRIPTION}}`:meta description 內容。
- `{{CONTENT}}`:片段的 `<article>` 內文,**原封不動逐字插入**(含原縮排/空白),保證無損。
- `{{SCRIPTS}}`:額外 script 槽,預設為空字串;`79-bank-toi` 在此補 3 支 TOI script(每支一行,與現況同位置)。一般章此處不產生任何字元。
- **字型連結固定寫在模板**(對所有章一致輸出)。據 F1,`82/83/84` 原本缺字型,經此模板後會**補回**標準字型連結——這是預期中的修正,也是遷移 diff 唯一允許出現的差異。

> byte-identical 要求:上方模板為**示意排版**。實作時 `{{CONTENT}}` 必須以「原 `<article class="content">` 與 `</article>` 之間的逐字 bytes(含其原有的前後換行/縮排)」原樣代入,模板**不得在 `{{CONTENT}}` 周圍另加換行或縮排**;head、字型 URL、包裹標籤的縮排換行一律以某既有章(如 `01-what-is-cs.html`)為基準逐字對齊。最終以 §5 的 `git diff` 乾淨為準。

### 3.2 `chapters/src/NN-slug.html`(內容片段)
```html
<!--meta
title: 用資料建立抽象:從抽象屏障到資料導向
description: 從 cons/car/cdr 到資料導向程式設計——跟著 SICP 第二章理解抽象屏障……
-->
      <div class="eyebrow">第十九部 · SICP:抽象的建構</div>
      <h1>用資料建立抽象:從抽象屏障到資料導向</h1>
      …其餘 callout / exercise / 內嵌 SVG / 程式碼,全部照舊…
```
- `<!--meta ... -->`:位於檔首的前置區,`key: value` 逐行。必填 `title`、`description`;選填 `scripts`(逗號分隔,相對 `../assets/` 的路徑,如 `toi/toi-index.js, toi/toi-statements.js, toi/toi-render.js`)。
- meta 區之後即 `<article>` 內文,逐字保留(含縮排),build 時原樣填入 `{{CONTENT}}`。

### 3.3 `build.py`
- 讀 `chapters/_layout.html`。
- 對每個 `chapters/src/*.html`:
  1. 解析檔首 `<!--meta ... -->`,取 `title`/`description`/`scripts`;其後內容為 `CONTENT`。
  2. `SCRIPTS` = 把 `scripts` 每個路徑組成 `<script src="../assets/<path>"></script>` 各一行(無 scripts 則為空字串)。
  3. 以**字面字串取代**(非 `str.format`,避免內容中的 `{`/`}` 出錯)把四個佔位符代入模板;`{{CONTENT}}` 最後代入、不再掃描。**不加任何 GENERATED 提示行**(見 §0)。
  4. 寫出 `chapters/NN-slug.html`,**UTF-8、CRLF(`\r\n`)行尾**(對齊現有檔,見 F2);明確以 `newline='\r\n'` 或二進位寫出,不依賴平台預設。
- 全部產生後,對所有產出檔跑 `_validate_chapter.py`;任何 ✗ 即以非零結束並印出。
- 介面:`python build.py`(全建)、`python build.py chapters/src/NN-slug.html`(只建單章)、`python build.py --check`(只驗證不寫)。
- 冪等:重複執行產出位元相同。

### 3.4 `migrate.py`(一次性)
- 對每個現有 `chapters/NN.html`:
  1. 取 `<title>`,以容錯 regex `\s*·\s*CS 自學聖經\s*$` 去後綴 → `title`(F3:處理 `74-bank-ap325` 的「(依章)· …」無空格異例)。
  2. 取 `<meta name="description" content="...">` → `description`。
  3. 取 `<body>` 中 `<article class="content">` 與 `</article>` 之間的內容(逐字、含空白;F4 已確認每章僅 1 個 `</article>`,安全)→ `CONTENT`。
  4. 偵測 body 內 book.js 之前的額外 `<script src="../assets/...">` → `scripts`(僅 `79-bank-toi` 會有)。
  5. 寫 `chapters/src/NN.html`:`<!--meta ...-->` + `CONTENT`,**保留 CRLF**。
- 不修改原 `chapters/NN.html`(交給 build 之後一次覆寫)。
- `82/83/84` 的片段**不含任何字型資訊**;字型由模板統一補上(F1 的修正)。

---

## 4. 資料流

```
撰寫/編輯  →  chapters/src/NN.html (來源真相)
                       │
                  build.py  ←  chapters/_layout.html (共用外殼)
                       │            └→ _validate_chapter.py (把關)
                       ▼
            chapters/NN.html (產出,committed,可直接開檔)
                       │
                  book.js (執行期注入 nav/TOC/上下章,維持不變)
```

---

## 5. 遷移與驗收(無損證明)

1. 跑 `migrate.py` 產生 85 個 `chapters/src/*.html`。
2. 跑 `build.py` 重新覆寫 85 個 `chapters/*.html`。
3. **關鍵驗收**:`git diff chapters/*.html`
   - 允許出現的差異**只有一種**:`82/83/84-sicp-*.html` 各補上 4 行標準字型連結(F1 的刻意修正)。
   - **其餘 82 章必須 byte-identical(diff 完全空)**。任何內容/結構/渲染/空白/行尾差異都視為遷移失敗,須調整模板與抽取邏輯直到只剩 F1 的差異。
   - 因 F2(CRLF),驗收時須留意 git autocrlf 可能遮蔽行尾差異:除 `git diff` 外,另對「未變動的某章」做一次原始位元比對(如 `cmp` 原檔備份 vs 產出)確認行尾保留。
4. 通過後 `migrate.py` 即可刪除(其職責已完成;保留也無妨)。

---

## 6. 今後新增章節流程(本案的核心效益)

1. 寫 `chapters/src/NN-slug.html`(meta + 內容)。
2. 在 `book.js` 的 `BOOK` 加一筆章節條目。
3. `python build.py` → 自動產出 HTML 並通過驗證器。

共用外殼永遠來自那**一份 `_layout.html`**;結構由 `_validate_chapter.py` 強制。日後要換字型、改 CDN、調整 head——**改模板一次、`build.py` 全部到位**。

---

## 7. 錯誤處理
- `build.py`:片段缺 `title`/`description` → 明確報錯(指出檔名與缺哪個 key)。`scripts` 指向不存在的檔 → 警告但續建。產出未通過 `_validate_chapter.py` → 非零結束、列出問題章。
- `migrate.py`:某章找不到 `<article class="content">` 或 `<title>` → 報錯該章,不靜默略過。
- 產出檔頂部 GENERATED 提示,避免有人誤改產出而被下次 build 覆蓋。

---

## 8. 測試/驗證
- **遷移無損**(主驗收):§5 的 `git diff` 只剩 `82/83/84` 的字型修正,其餘 82 章完全空。
- **行尾保留**(F2):任取一未變動章,原檔備份與產出做位元比對(`cmp`),確認仍為 CRLF、無行尾翻動。
- **F1 修正確認**:`82/83/84` 產出含 4 行標準字型連結;瀏覽器看這 3 章字型已正確(Noto/Inter 而非 fallback)。
- **build 冪等**:連跑兩次 `build.py`,第二次 `git diff` 完全空。
- **往返測試**:改某章 `src` 片段一處 → rebuild → 該變化出現在產出、且只有該處變。
- **新章流程**:新增一個最小 `src` 片段 + book.js 條目 → build → 章節可開、驗證器通過。
- **特例**:`79-bank-toi` 產出仍含 3 支 TOI script 且題庫頁正常(於瀏覽器確認)。
- **驗證器整合**:`build.py --check` 對 85 章全 ✓。

---

## 9. 取捨與邊界
- 產出 `chapters/*.html` **照舊 commit**(維持直接開檔);來源真相是 `chapters/src/` + `_layout.html`,以**目錄結構 + `_AUTHOR_GUIDE.md`/README 的明確說明**表達(不在產出檔加 GENERATED 提示行,以維持 §5 的乾淨 diff)。應在 `_AUTHOR_GUIDE.md` 補一句「改章節請改 `chapters/src/` 後跑 `build.py`,勿直接改 `chapters/*.html`」。(備選:gitignore 產出、build on demand——否決,因會破壞「clone 後直接開檔」。)
- `title` 放片段 meta(自足),與 book.js 的 nav 標題各司其職(輕微重複,可接受;避免 build 解析 JS 物件的脆弱性)。
- `index.html` 非章節(`.home` 結構),不納入本系統。
- 本案是「內容/版型分離」的骨架;未來若要 Markdown 化,只需把 `src` 片段換成 `.md` + 在 build 加 Markdown 引擎,模板與流程可沿用。
