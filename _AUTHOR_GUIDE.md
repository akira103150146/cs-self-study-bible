# 作者指南 — CS 自學聖經(章節撰寫規範)

> 這份文件是給「撰寫章節的 AI 作者」看的。請在動筆前完整讀過,並參考兩篇**來源片段**
> `chapters/src/00-about.html` 與 `chapters/src/01-what-is-cs.html`(片段格式的真實範例),模仿它們的語氣、結構與元件用法。

## 0. 你的任務
你要產出**一個完整的 HTML 章節檔**,放在 `textbook/chapters/` 下。這本書是一本「由淺入深、
中英對照」的計算機科學自學教科書,風格仿 Medium 長文:像在讀一篇精彩、好讀、但又紮實的文章。

## 0.5 檔案結構與建置(務必遵守)
本書章節採「內容/版型分離」:
- **來源真相**是 `chapters/src/NN-slug.html`(內容片段:檔首 `<!--meta-->` 前置區含 `title`/`description`/選填 `scripts`,其後為 `<article>` 內文)。
- **不要直接編輯 `chapters/NN-slug.html`**(那是 `build.py` 的產出,會被覆寫)。
- 共用外殼(head/字型/CSS/包裹/book.js)在 `chapters/_layout.html`,**單一來源**;要改 head/字型就改這裡再 rebuild。
- 流程:寫/改 `chapters/src/NN-slug.html` → 在 `assets/book.js` 加章節條目(新章)→ 跑 `python build.py` 產生 HTML(驗證為選用,見下)。
- 單章重建:`python build.py NN-slug`;結構/跳脫自檢:`python build.py --check NN-slug`(驗證為選用 lint,不阻擋建置;既有部分舊章本就不符嚴格規則)。
- 改完 src 後可用 `python build.py --verify` 確認所有產出已重建(CI/送交前自檢)。

## 1. 寫作語氣與風格(最重要)
- **語言**:繁體中文為主,寫給台灣讀者。**中英對照**:每個重要術語第一次出現時用「中文(English)」格式,
  例如「遞迴(recursion)」「雜湊表(hash table)」。之後可只用中文或交替使用。
- **Medium 敘事風**:用故事、比喻、提問開場,帶讀者進入情境,而不是劈頭丟定義。多用「你」與讀者對話。
  避免教科書式的冷硬條列堆砌;要有節奏、有溫度、有「為什麼」。
- **由淺入深**:每個概念先講「為什麼需要它/它解決什麼問題」→「它是什麼(直覺)」→「精確定義」→
  「怎麼用/實作」→「常見陷阱」。**絕不**一上來就丟公式或術語。
- **誠實**:不誇大、不亂掰。不確定的東西不要硬寫。歷史與人名要正確。
- **篇幅**:不設上限,但要紮實完整。一章通常 8–20 個 `<h2>` 小節等級的份量,務求把該章主題講透。
  寧可深也不要淺。每個關鍵概念都要有「直覺說明 + 程式碼/圖 + 練習」。

## 2. 程式碼規範
- 每個抽象概念都要配**可執行**的程式碼。
- **Python** 用於快速表達想法與驗證直覺;**C / C++** 用於展示底層真相(記憶體、指標、效能、位元運算等)。
  數學/演算法章節以 Python 為主、關鍵處補 C;系統/底層章節多用 C/C++。
- 程式碼要能直接複製執行,加上**中文註解**。變數命名清楚。
- HTML 裡程式碼用 `<pre><code class="language-python">...</code></pre>`,語言可為
  `language-python` / `language-c` / `language-cpp` / `language-bash` / `language-sql` / `language-text` / `language-haskell` 等。
- **務必把 HTML 特殊字元跳脫**:`<` 寫成 `&lt;`,`>` 寫成 `&gt;`,`&` 寫成 `&amp;`。
  (例如 C 的 `#include <stdio.h>` 要寫成 `#include &lt;stdio.h&gt;`,`for (i=0; i<n; i++)` 的 `<` 要寫 `&lt;`。)這非常重要,否則畫面會壞掉。

## 3. 數學公式
- 需要數學時用 LaTeX:行內 `$...$`,獨立 `$$...$$`。系統會自動載入 MathJax 渲染。
- 例:時間複雜度 `$O(n \log n)$`、求和 `$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$`。

## 4. 必用的版型元件(class 已在 style.css 定義好,直接用)
- 章首固定結構(見下方骨架):`.eyebrow`(所屬部別)、`<h1>`、`.subtitle`(一句引人入勝的副標)、
  `.byline`(章次/閱讀時間/難度星等)、`.objectives`(學習目標清單)。
- 小節標題用 `<h2>`,子節 `<h3>`,更小用 `<h4>`。`book.js` 會自動抓 h2/h3 生成右側目錄,所以**標題要寫得好**。
- **提示框 callout**(語意化):
  ```html
  <div class="callout key"><div class="ico">🔑</div><div class="body"><span class="c-title">核心觀念</span><p>...</p></div></div>
  ```
  類型:`note`(ℹ️ 一般補充)、`tip`(💡 小技巧)、`warn`(⚠️ 常見陷阱)、`danger`(⛔ 嚴重警告)、
  `key`(🔑 核心觀念,每節最重要的一句)、`history`(📜 歷史小注)。每章請穿插數個,尤其多用 `key`。
- **練習題 exercise**(每章至少 3–6 題,難度遞增,**一定要附可展開解答**):
  ```html
  <div class="exercise">
    <div class="ex-head">✏️ 練習 X.Y <span class="badge">思考|實作|挑戰</span></div>
    <div class="ex-body">
      <p>題目...</p>
      <details class="solution"><summary>看解答</summary>
        <div class="sol-body"><p>解答...含程式碼</p></div>
      </details>
    </div>
  </div>
  ```
- **引言**:`<blockquote>`。**表格**:標準 `<table>`(可包 `<div class="table-wrap">`)。
- **圖**:盡量用**手繪內嵌 SVG** 放在 `<div class="diagram">...<figcaption>圖 X-Y:說明</figcaption></div>`。
  圖很重要(資料結構、流程、架構、記憶體配置等),請多畫。SVG 用 `font-family="Inter, 'Noto Sans TC', sans-serif"`,
  配色可用主色 `#2f6f6a`(藍綠)、`#b4541f`(磚紅)、`#8b5cf6`(紫)、灰 `#8a929b`、淺底 `#e3efed`。
- 章末請有一節「把這一章串起來」(總結重點),以及一個 `callout note` 指向對應的 OSSU 原始課程/延伸資源連結。

## 5. 檔案骨架(嚴格照抄,只改 title / 內容)

> **重要**:`<head>`、`.layout` 包裹、`book.js` script 全部由 `chapters/_layout.html` 提供。
> 你寫的 `chapters/src/NN.html` 是**內容片段**,只包含 `<!--meta-->` 前置區與 `<article>` 內文,
> **不要**寫 `<!DOCTYPE>`、`<html>`、`<head>`、`<body>`、`.layout`、`<script src=book.js>` 這些。
> 若章節需要額外 script,用 meta 的 `scripts:` 欄(逗號分隔檔名),`build.py` 會自動插入。

```html
<!--meta
title: 章節標題
description: 一句話描述本章。注意:title 與 description 內不要用半形雙引號 " 或角括號 < >。
-->
      <div class="eyebrow">第 X 部 · 部別名稱</div>
      <h1>章節標題</h1>
      <p class="subtitle">一句引人入勝的副標題。</p>
      <div class="byline">
        <span class="tag">第 N 章</span>
        <span>閱讀時間 ≈ NN 分鐘</span>
        <span>難度:★★★☆☆</span>
      </div>
      <div class="objectives">
        <div class="o-title">📌 讀完這一章,你會知道</div>
        <ul><li>...</li><li>...</li></ul>
      </div>

      <h2>...</h2>
      <p>...</p>

      <!-- 內文:由淺入深,穿插 callout / exercise / diagram / 程式碼 -->

      <h2>把這一章串起來</h2>
      <p>...總結...</p>
```

## 6. 不要做的事
- 不要自己加 `<nav>`、側邊欄、頂部列、上一章/下一章——這些由 `book.js` 自動生成。
- `<head>`、`.layout` 包裹、`../assets/style.css`、`<script src="../assets/book.js">` 這些都由 `chapters/_layout.html` 統一提供;要改 head/字型/CSS 路徑就改 `_layout.html` 再執行 `python build.py`,**不要**在片段裡寫這些。
- **不要直接編輯 `chapters/NN-slug.html`**(那是 `build.py` 的產出,會被覆寫);來源真相是 `chapters/src/NN-slug.html`。
- 不要在 HTML 裡寫 `<style>` 區塊或 inline style(SVG 內的 fill/stroke 等屬性可以)。
- 不要忘記跳脫程式碼裡的 `<`、`>`、`&`。

寫作時心裡想著一個讀者:一個聰明、好奇、但這個主題完全零基礎的人。你的工作是讓他讀完之後,
不只「知道」,而且「真的懂、而且想繼續學下去」。
