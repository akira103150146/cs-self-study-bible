# SICP 整合進「CS 自學聖經」— 設計文件

- 日期:2026-06-30
- 狀態:已核准設計,待寫實作計畫
- 來源素材:`textbook/sicp.pdf`(*Structure and Interpretation of Computer Programs*, 2nd ed., Unofficial Texinfo Format,883 頁,Abelson & Sussman)

---

## 1. 目標與範圍

把 SICP 中**書中尚未涵蓋**的代表性概念,以忠於原著的方式整合進這本既有 80 章的中英對照 HTML 教科書。

- **做**:新增一個專屬「部」共 5 章,涵蓋盤點出的 8 個缺口;在既有章節加輕量 callout 互連。
- **不做**:不重新編號既有章節;不全譯 600 頁;不重寫既有 42/21–23 等章。
- **定位**:誠實標示為「**SICP 導讀與重構**」,每個概念選代表性範例講透,而非逐頁翻譯。

### 1.1 缺口盤點結論(❌ = SICP 獨有、書中完全缺席)

按教學價值排序的 8 塊缺口:

1. 資料導向程式設計 + 標籤資料 + 泛型運算(SICP 2.4–2.5)
2. 後設循環直譯器 eval/apply(4.1)— SICP 的靈魂
3. 串流與延遲求值(3.5)
4. 環境模型 + 閉包即物件 + 區域狀態(3.1–3.2)
5. 資料抽象與抽象屏障 + 用序對建構一切(2.1–2.2)
6. 非確定計算 amb(4.3)
7. 暫存器機器 + 顯式控制求值器(5.1–5.4)
8. 代換模型 / 符號資料與引用(1.1、2.3)

結構性缺口:書中有 Haskell、Prolog,卻無 Lisp/Scheme 語言本身——上述 8 塊都依賴 Scheme 語法直覺。

🟡 已部分涵蓋、只需互連不需重寫:牛頓法/固定點(55/12)、霍夫曼(31)、邏輯程式設計/統一/回溯(45)、並行 serializer(43)、垃圾回收(24/42)、編譯(42)、map/filter/reduce(06)。

---

## 2. 編排決定

- **策略**:A — 新增專屬「部」5 章 + 既有章節輕量互連。(備選 B 單章導讀、C 全併入既有章,均否決:B 會壓扁 metacircular evaluator,C 會打散 SICP 敘事並使 42、21–23 膨脹失焦。)
- **語言**:Scheme 為主 + Python 對照。忠於原著,關鍵處附 Python 對照助直覺;與既有第 6 章「嚐一口 Racket/Scheme」一致。

---

## 3. 整合架構(技術機制)

### 3.1 新「部」

在 `assets/book.js` 的 `BOOK.parts` 陣列中,於「第十八部 · 實戰資安 CTF」物件之後、「附錄 · 完整題庫」物件之前(現約第 217–218 行之間)插入新 part 物件:

```js
{
  part: "第十九部 · SICP:抽象的建構",
  icon: "λ",
  blurb: "從序對到自我直譯器——用 Scheme 重走經典《SICP》,看抽象如何層層長出一台會思考的機器。",
  chapters: [
    { id: "80-sicp-scheme",            num: "74", title: "Scheme 導引與程序抽象",         en: "Scheme & Procedural Abstraction", done: true },
    { id: "81-sicp-data",              num: "75", title: "用資料建立抽象:從抽象屏障到資料導向", en: "Building Abstractions with Data", done: true },
    { id: "82-sicp-state-streams",     num: "76", title: "狀態、環境模型與串流",            en: "State, Environments & Streams",   done: true },
    { id: "83-sicp-metacircular",      num: "77", title: "後設循環直譯器:用 Lisp 寫 Lisp",   en: "The Metacircular Evaluator",      done: true },
    { id: "84-sicp-register-machines", num: "78", title: "暫存器機器與顯式控制求值器",        en: "Register Machines & EC-Evaluator", done: true },
  ],
},
```

### 3.2 編號規則(重要)

- **檔名 id 用 80–84**:74–79 已被附錄題庫的檔案占用,故新檔案必須從 80 起。
- **顯示章號 num 用 74–78**:目前主章號到 73,接續最自然。閱讀順序為 …第 73 章(CTF)→ 第 74–78 章(SICP)→ 附 A–F(題庫)。
- 檔名≠章號的情形題庫已有先例(檔案 74–79、章號附A–附F),故一致、不破壞既有約定。

### 3.3 章節檔

5 個新 HTML 檔放在 `textbook/chapters/`,嚴格依 `_AUTHOR_GUIDE.md` 骨架:`eyebrow`(第十九部 · SICP:抽象的建構)/ `h1` / `subtitle` / `byline` / `objectives` / 多個 `h2` 小節 / `callout` / `exercise` / `diagram` / 「把這一章串起來」+ 指向 SICP 原著的延伸資源 callout。不自行加 nav/側欄(由 book.js 生成),不改 CSS 路徑,不寫 inline style。

### 3.4 既有章節互連(只加 callout,不重寫內文)

| 既有章 | 加 callout 指向 | 主題 |
|---|---|---|
| 03 函式與遞迴、06 函數式 | ch74 | 代換模型、環境模型深化 |
| 10 設計模式 | ch75 | 資料導向程式設計 |
| 44 Haskell | ch76 | 串流即 generator/惰性 |
| 42 編譯器 | ch77、ch78 | metacircular vs 顯式控制求值器 |
| 45 Prolog | ch77 | amb / 查詢系統 |
| 21–23(機器語言/VM/編譯器)、42 | ch78 | 暫存器機器另一種視角 |

---

## 4. 章節內容設計

每章另含 3–6 題難度遞增、附可展開解答的練習。

### 第 74 章 — Scheme 導引與程序抽象(對應 SICP 第 1 章)
① 為什麼是 Lisp:程式即資料(history callout) ② Scheme 五分鐘:前綴記法、`define`、求值規則 ③ **代換模型**(連 03 呼叫堆疊) ④ 條件、謂詞與牛頓法求平方根(連 55) ⑤ 遞迴 vs 迭代、尾遞迴、樹狀遞迴(連 03) ⑥ 高階程序:程序作為參數/回傳值、`lambda`、固定點(連 06) ⑦ Python 對照 ⑧ 把這一章串起來

### 第 75 章 — 用資料建立抽象:從抽象屏障到資料導向(SICP 第 2 章)
① `cons`/`car`/`cdr` 與序對 ② **抽象屏障**(有理數運算) ③ 用序對建構一切:list/樹/closure property ④ 序列作為慣用介面:`map`/`filter`/`accumulate` 訊號流觀(連 06) ⑤ 符號資料與引用(`quote`)、符號微分(連 12) ⑥ 多重表示與**標籤資料**(複數兩種表示) ⑦ **資料導向程式設計與可加性**(dispatch table)★核心 ⑧ 帶泛型運算的系統(型別塔、強制轉型) ⑨ Python 對照(dict dispatch / `singledispatch`) ⑩ 把這一章串起來

### 第 76 章 — 狀態、環境模型與串流(SICP 第 3 章)
① 賦值與區域狀態:用閉包造一個 bank account ② 引入賦值的代價:同一性與變動 ③ **環境模型**:框架、綁定、求值規則 ★核心(SVG 框架圖) ④ 可變資料:佇列與表格 ⑤ 並行:時間即本質、serializer(連 43,輕量) ⑥ **串流**:延遲串列、`delay`/`force` ⑦ 無限串流與串流範式(費氏、篩法、e) ⑧ 串流 vs 物件:兩種模組化 ⑨ Python 對照(generator 就是串流) ⑩ 把這一章串起來

### 第 77 章 — 後設循環直譯器:用 Lisp 寫 Lisp(SICP 第 4 章)
① 直譯器是什麼:`eval` 與 `apply` 的雙人舞 ★皇冠 ② 核心:eval/apply 互遞迴 ③ 表示運算式:語法抽象 ④ 求值器的資料結構:環境 ⑤ 跑起來:把直譯器當程式執行 ⑥ 程式即資料(data as programs) ⑦ 變體一:**惰性求值**(normal vs applicative order) ⑧ 變體二:**非確定計算 amb** 與搜尋 ⑨ 連 42 編譯器、45 Prolog 查詢系統(callout) ⑩ 把這一章串起來(練習:實作一個 mini-evaluator)

### 第 78 章 — 暫存器機器與顯式控制求值器(SICP 第 5 章)
① 從高階到機器:暫存器機器模型 ② 描述暫存器機器的語言;用堆疊實作遞迴 ③ 暫存器機器模擬器 ④ 儲存配置與**垃圾回收**(mark-sweep / stop-and-copy,連 24/42) ⑤ **顯式控制求值器**:把 metacircular evaluator 降到暫存器層 ⑥ 編譯:把 Scheme 編成暫存器機器指令(連 42、21–23) ⑦ 大圖:從 NAND 到直譯器,全書在此交會(連 19–23) ⑧ 把這一章串起來

---

## 5. 慣例與品質把關

- **HTML 跳脫**:所有 Scheme/C 程式碼中的 `<`、`>`、`&` 一律跳脫(`&lt;`/`&gt;`/`&amp;`)。
- **程式碼上色**:Scheme 用 `<pre><code class="language-scheme">`;highlight.js 11.9.0 完整版(cdnjs `highlight.min.js`)內建 `scheme`,可正常上色。Python 對照用 `language-python`。
- **數學**:成長量級等用 MathJax(行內 `$...$`,獨立 `$$...$$`)。
- **圖**:環境模型框架圖、串流訊號流圖、暫存器機器資料路徑圖用內嵌 SVG,配色用主色盤,加 `<figcaption>`。
- **語氣**:繁中為主、術語中英並陳、Medium 敘事風,由淺入深(為什麼→直覺→精確→實作→陷阱)。
- **`done` 旗標**:目前未被渲染邏輯使用(純 metadata);新章寫完設 `done: true`。

---

## 6. 驗收標準

於瀏覽器開 `textbook/index.html`:

1. 「第十九部 · SICP:抽象的建構」出現在側欄,位置在第十八部 CTF 之後、附錄題庫之前。
2. 5 章皆可開啟,右側 TOC 由各章 `h2`/`h3` 自動生成且層級正確。
3. Scheme 程式碼正常語法上色;切換深/淺色主題上色同步。
4. 無未跳脫的 `<` 造成破版。
5. 上一章/下一章串接正確(73 ↔ 74…78 ↔ 附A)。
6. 既有章節新增的互連 callout 連結正確指向新章 id。

---

## 7. 後續

設計核准後,以 writing-plans 技能產出逐章、逐檔的實作計畫(含每章撰寫順序、book.js 編輯、互連 callout 清單、驗收檢查)。
