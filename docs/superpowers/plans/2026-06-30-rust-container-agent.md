# Rust／容器虛擬化／LLM Agent 三部 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在「CS 自學聖經」既有 19 部之後新增第二十~二二部、共 22 章(顯示第 79–100 章),教資工系學生 Rust、容器/虛擬化底層、與手刻 LLM Agent。

**Architecture:** 本書採「**內容/版型分離**」建置系統(2026-06-30 已上線):章節**來源**是 `chapters/src/NN-slug.html` 片段(檔首 `<!--meta-->` + `<article>` 內文),由 `build.py` 包進 `chapters/_layout.html` 產生 `chapters/NN-slug.html`。導覽由 `assets/book.js` 注入。**作者只改 `src/` 片段,不直接改產出檔。**

**Tech Stack:** HTML 片段 + `chapters/_layout.html` + `assets/style.css` + `assets/book.js`;`build.py`(產生器/--verify/--check)+ `chapters/_validate_chapter.py`(結構/跳脫驗證);章內程式碼 Python / C / C++ / Rust / bash / yaml。

**來源文件:** 設計 spec `docs/superpowers/specs/2026-06-30-rust-container-agent-design.md`(逐章大綱、完善度盤點 §10)。作者規範 `_AUTHOR_GUIDE.md`(片段流程)。

## Global Constraints

- **建置系統(最關鍵,別寫錯地方)**:章節寫在 `chapters/src/NN-slug.html`;**絕不**直接寫/改 `chapters/NN-slug.html`(那是產物,會被覆寫)。寫完跑 `python build.py NN-slug` 產生。
- **片段格式**:檔案開頭必須是 `<!--meta`(頂格,前面無空白),內含 `title:`(章標題,**不加**「· CS 自學聖經」,layout 會加)、`description:`(一句話);一般章節**不需** `scripts:`(book.js 已由 layout 注入)。meta 結束 `-->` 後接內文,內文從 `      <div class="eyebrow">…</div>` 起(縮排比照既有片段),**不要**寫 `<!DOCTYPE>`/`<head>`/`<article>`/`book.js`(都在 layout)。
- **顯示章號 ≠ 檔名 id**:檔名/slug 從 `85` 起、`.byline` 的顯示章號從 `79` 起。見對照表。
- **驗證器硬規則(`chapters/_validate_chapter.py`,務必全過)**:有 `class="eyebrow"`/`subtitle`/`byline`/`objectives`、章末「把這一章串起來」;`<h1>` **恰 1 個**;`<h2>` **至少 8 個**;無 `<style>`;`<code>` 內 `<`→`&lt;`、`>`→`&gt;`、`&`→`&amp;` 全跳脫;`href="N….html"` 跨章連結目標檔須存在(否則 --check 報錯)。
- **done 旗標**:新章先 `done:false`(Task 2 一次建好);該章 src 寫完並 build 後再改 `done:true`。
- **跨章連結時序**:新章互連/連既有章時,目標 `chapters/*.html` 須已存在 --check 才綠;建置不被 --check 阻擋(advisory),但每批結束跑一次全量 `--check` 收尾。
- **語氣/語言**:繁中為主、中英對照(術語首見「中文(English)」)、Medium 敘事、由淺入深。
- **語言一致**:不引入 Go;`手寫迷你 Docker` 用 C＋bash(或 Rust)。
- **Agent 後端**:手刻中立 `LLMClient`,預設本地 Ollama(附 `ollama pull`)、同介面可切 Claude。
- **去重鐵則(spec §10.1)**:§80 不重教 ADT/Option/泛型/模式比對(§09/§44 已教);§81 不重講演算法邏輯(§28–29 已教),只談所有權視角實現;§93 明確區隔 CNN(§67,影像)vs Transformer(文本)。
- **誠實標示**:§84 手寫 OS、§88 手寫 Docker、§93 手刻 GPT 皆標「教學用最小版本,非生產級」。
- **元件下限**:`.objectives` 1、`callout` 數個(多用 🔑)、`.exercise` ≥ 3(附 `<details class="solution">`)、`.diagram` 內嵌 SVG ≥ 1、章末總結 + 延伸 `callout note`。

### 章號對照表(slug → 顯示章號 → 部)

| slug | 顯示 | 部 |
|---|---|---|
| 85-rust-ownership | 79 | 二十 Rust |
| 86-rust-types-errors | 80 | 二十 Rust |
| 87-rust-collections-ds | 81 | 二十 Rust |
| 88-rust-concurrency | 82 | 二十 Rust |
| 89-rust-project | 83 | 二十 Rust |
| 90-rust-os-kernel | 84 | 二十 Rust |
| 91-virt-landscape | 85 | 二一 容器 |
| 92-vm-hypervisor | 86 | 二一 容器 |
| 93-container-internals | 87 | 二一 容器 |
| 94-mini-docker | 88 | 二一 容器 |
| 95-docker-practice | 89 | 二一 容器 |
| 96-kubernetes | 90 | 二一 容器 |
| 97-ebpf | 91 | 二一 容器 |
| 98-distributed-systems | 92 | 二一 容器 |
| 99-gpt-from-scratch | 93 | 二二 Agent |
| 100-llm-client | 94 | 二二 Agent |
| 101-tool-react | 95 | 二二 Agent |
| 102-rag-from-scratch | 96 | 二二 Agent |
| 103-mcp | 97 | 二二 Agent |
| 104-agent-advanced | 98 | 二二 Agent |
| 105-multi-agent | 99 | 二二 Agent |
| 106-agent-production | 100 | 二二 Agent |

### 部別 eyebrow / blurb / icon

- eyebrow 字串(寫進片段)= **`第二十部 · Rust 系統程式設計`** / **`第二一部 · 容器、虛擬化與雲原生底層`** / **`第二二部 · 動手打造 LLM Agent`**。
- book.js `part` 同上;icon 依序 `🦀` / `📦` / `🤖`;blurb 見 Task 2。

---

## Chapter Authoring Protocol(每個章節任務 Task 3–24 共用步驟)

撰寫前先讀 `_AUTHOR_GUIDE.md` 與範本片段 `chapters/src/00-about.html`、`chapters/src/01-what-is-cs.html`,並參考同主題既有章。對某章(slug = `<slug>`,部 eyebrow = `<PART>`,顯示章號 = `<N>`),5 步如下(各任務已填具體值):

1. **寫 `chapters/src/<slug>.html` 片段**:`<!--meta-->`(title/description)+ 內文(`<div class="eyebrow"><PART></div>`、`<h1>`、`.subtitle`、`.byline`(`第 <N> 章`)、`.objectives`、**≥8 個 `<h2>`** 內文穿插 callout/exercise/diagram/escaped code、章末「把這一章串起來」+ 延伸 `callout note`)。
2. **產生**:`python build.py <slug>` → 期望 `已產生 1 章。`
3. **驗證**:`python build.py --check <slug>` → 期望 `✓ chapters/<slug>.html`;若報錯(h2<8、未跳脫、缺區塊、連結缺檔)**必須修到過**(連結目標尚未建者除外,記下待收尾)。
4. **啟用**:`assets/book.js` 將該章 `done: false`→`done: true`。
5. **commit**:`git add chapters/src/<slug>.html chapters/<slug>.html assets/book.js && git commit -m "feat(textbook): add ch<N> <slug>"`。

> 並行:src 片段互不相依可平行寫;但步驟 4 都改 `book.js`,**book.js 翻轉須序列化**(逐任務 review 天然保證)。

---

## Task 1: 建置管線冒煙測試(驗證器已存在,不需新建)

**Files:** 無新增(確認既有 `build.py` / `chapters/_validate_chapter.py` / `chapters/_layout.html` 可用)

- [ ] **Step 1: 確認全量產出與 src 同步**

Run: `python build.py --verify`
Expected: `所有產出與 src 同步(NN 章)。`(若報不同步,先 `python build.py` 重建既有章再續。)

- [ ] **Step 2: 確認驗證器可跑**

Run: `python build.py --check 01-what-is-cs`
Expected: 驗證器執行並輸出報告。**注意:既有部分舊章(含 01)本就不符嚴格規則(<8 h2、舊碼未跳脫);`--check` 為 advisory、不阻擋建置。新章則須寫到 `--check` 全綠(≥8 h2、跳脫齊全);新章間的前向連結在目標建成前會報「跨章連結目標不存在」,屬預期,於每批收尾全量 `--check` 時消除。**

- [ ] **Step 3: 無需 commit**(未改檔)。記錄結論於 ledger。

---

## Task 2: 在 `book.js` 建三部 22 章 `done:false` 骨架

**Files:** Modify `assets/book.js`(在「第十九部 · SICP」part 物件之後、「附錄 · 完整題庫」part 物件之前插入三個 part 物件)

**Interfaces — Produces:** 首頁目錄/側欄顯示三新部 22 章(灰色未啟用)。

- [ ] **Step 1: 插入三個 part 物件**(`num` 用顯示章號;`id` 用 slug)

```javascript
    {
      part: "第二十部 · Rust 系統程式設計",
      icon: "🦀",
      blurb: "從所有權到無懼並行,再到親手寫一顆會開機的核心——用一門「編譯器當你導師」的語言,重新理解記憶體、型別與系統。",
      chapters: [
        { id: "85-rust-ownership", num: "79", title: "所有權、借用與生命週期", en: "Ownership, Borrowing & Lifetimes", done: false },
        { id: "86-rust-types-errors", num: "80", title: "型別、trait、列舉與錯誤處理", en: "Types, Traits & Error Handling", done: false },
        { id: "87-rust-collections-ds", num: "81", title: "集合、迭代器與所有權視角的資料結構", en: "Collections & Ownership-Aware Data Structures", done: false },
        { id: "88-rust-concurrency", num: "82", title: "無懼並行與非同步", en: "Fearless Concurrency & Async", done: false },
        { id: "89-rust-project", num: "83", title: "Rust 實戰:CLI 工具與最小服務", en: "Building a CLI & Service in Rust", done: false },
        { id: "90-rust-os-kernel", num: "84", title: "用 Rust 手寫迷你作業系統核心", en: "A Minimal OS Kernel in Rust", done: false },
      ],
    },
    {
      part: "第二一部 · 容器、虛擬化與雲原生底層",
      icon: "📦",
      blurb: "一個程式如何「以為自己獨佔整台電腦」?從 chroot、namespaces、cgroups 到 hypervisor,再到 eBPF 與分散式——拆開魔法,還親手拼一個出來。",
      chapters: [
        { id: "91-virt-landscape", num: "85", title: "虛擬化全景:行程隔離→VM→容器", en: "The Virtualization Landscape", done: false },
        { id: "92-vm-hypervisor", num: "86", title: "虛擬機與 Hypervisor 底層", en: "Virtual Machines & Hypervisors", done: false },
        { id: "93-container-internals", num: "87", title: "容器的真相:namespaces / cgroups / OverlayFS", en: "How Containers Really Work", done: false },
        { id: "94-mini-docker", num: "88", title: "手寫迷你 Docker", en: "Build Your Own Mini Docker", done: false },
        { id: "95-docker-practice", num: "89", title: "Docker 實戰:映像、網路、Compose", en: "Docker in Practice", done: false },
        { id: "96-kubernetes", num: "90", title: "Kubernetes 編排與雲原生", en: "Kubernetes & Cloud Native", done: false },
        { id: "97-ebpf", num: "91", title: "eBPF:核心可程式化(觀測 / 網路 / 安全)", en: "eBPF: Programmable Kernel", done: false },
        { id: "98-distributed-systems", num: "92", title: "分散式系統與高可用架構", en: "Distributed Systems & High Availability", done: false },
      ],
    },
    {
      part: "第二二部 · 動手打造 LLM Agent",
      icon: "🤖",
      blurb: "不靠魔法框架,一步一步手刻——從會呼叫工具的迴圈,到能檢索、能用 MCP、會協作的自主 agent。",
      chapters: [
        { id: "99-gpt-from-scratch", num: "93", title: "從零打造 GPT(選修):看懂 agent 在跟誰說話", en: "Build GPT From Scratch (Optional)", done: false },
        { id: "100-llm-client", num: "94", title: "手刻你的 LLM client", en: "Hand-Building Your LLM Client", done: false },
        { id: "101-tool-react", num: "95", title: "工具呼叫與 ReAct", en: "Tool Calling & the ReAct Loop", done: false },
        { id: "102-rag-from-scratch", num: "96", title: "手刻最小 RAG", en: "Building Minimal RAG", done: false },
        { id: "103-mcp", num: "97", title: "MCP:可插拔的標準服務", en: "MCP: Pluggable Tools & Resources", done: false },
        { id: "104-agent-advanced", num: "98", title: "進階單代理:規劃、反思、自我改進", en: "Advanced Single-Agent Patterns", done: false },
        { id: "105-multi-agent", num: "99", title: "多代理協作系統", en: "Multi-Agent Systems", done: false },
        { id: "106-agent-production", num: "100", title: "從玩具到生產:框架、評估、可觀測性、部署", en: "From Toy to Production", done: false },
      ],
    },
```

- [ ] **Step 2: 語法檢查** — Run: `node --check assets/book.js` → 無輸出(通過)。
- [ ] **Step 3: 目錄計數** — Run: `grep -c 'id: "' assets/book.js` → 比插入前多 22。
- [ ] **Step 4: commit** — `git add assets/book.js && git commit -m "feat(textbook): scaffold parts 20-22 (22 chapters) in book.js"`

---

# 章節任務群 A:第二十部 · Rust(Tasks 3–8)

> 每任務照《Chapter Authoring Protocol》5 步;以下為該章專屬內容大綱。eyebrow 一律 `第二十部 · Rust 系統程式設計`。

## Task 3: ch79 所有權、借用與生命週期 — src `85-rust-ownership.html`(顯示第 79 章,★★★☆☆)
**Cross-links:** callout→§9 型別、§24 OS、§42 編譯器。
**大綱:** 目標——理解所有權動機、move/borrow、可變借用、生命週期初步、borrow checker 擋掉哪些 bug。h2(≥8):① C 記憶體之痛(懸空指標/double free/leak,附 C 例,**因書無 C 指標專章,本章自建動機**);② 為何 Rust(無 GC 安全);③ cargo 與第一支程式;④ 所有權三規則與 move(SVG:stack/heap);⑤ 借用 `&` 與 `&mut`(別名 XOR 可變,SVG);⑥ 生命週期初步;⑦ borrow checker 實戰(故意寫錯);⑧ 何時 clone/何時借;⑨ 把這一章串起來+延伸。手刻:把一段 C 字串處理用 Rust 重寫。圖≥2、練習≥4。
- [ ] 1 寫 `chapters/src/85-rust-ownership.html`(meta:title「所有權、借用與生命週期」)
- [ ] 2 `python build.py 85-rust-ownership` → 已產生 1 章
- [ ] 3 `python build.py --check 85-rust-ownership` → ✓
- [ ] 4 book.js:`85-rust-ownership` done→true
- [ ] 5 `git add chapters/src/85-rust-ownership.html chapters/85-rust-ownership.html assets/book.js && git commit -m "feat(textbook): add ch79 rust ownership & borrowing"`

## Task 4: ch80 型別、trait、列舉與錯誤處理 — src `86-rust-types-errors.html`(第 80 章,★★★☆☆)
**Cross-links:** callout→§9 型別、§44 Haskell(複習不重教)、§42 編譯器。
**去重鐵則:** ADT/列舉/Option/泛型/模式比對 §09+§44 已教 → 僅 callout 一句複習,火力放新東西。h2(≥8):① 一分鐘複習(callout→§09/§44);② trait 是什麼(vs OOP 介面、trait bound、預設方法,SVG);③ 泛型與單型化;④ `Result&lt;T,E&gt;` 與 `?`(錯誤即值);⑤ 自訂錯誤型別與 `From`;⑥ trait objects(`dyn`)動態分派;⑦ 慣用錯誤處理模式;⑧ 串起來+延伸。手刻:回傳 `Result` 的表示式求值器。圖≥1、練習≥4。
- [ ] 1 寫 `chapters/src/86-rust-types-errors.html`
- [ ] 2 `python build.py 86-rust-types-errors`
- [ ] 3 `python build.py --check 86-rust-types-errors` → ✓
- [ ] 4 book.js:`86-rust-types-errors` done→true
- [ ] 5 `git add chapters/src/86-rust-types-errors.html chapters/86-rust-types-errors.html assets/book.js && git commit -m "feat(textbook): add ch80 rust traits & error handling"`

## Task 5: ch81 集合、迭代器與所有權視角的資料結構 — src `87-rust-collections-ds.html`(第 81 章,★★★★☆)
**Cross-links:** callout→§28 排序搜尋、§29 資料結構、§43(預告 §82)。
**去重鐵則:** §28–29 已教演算法邏輯 → **不重講演算法**,改談所有權如何改造實現。h2(≥8):① Vec/HashMap 與迭代器/閉包;② 單向鏈結:`Box` 擁有鏈 vs 裸指標(SVG);③ 樹與多重所有權:`Rc&lt;RefCell&lt;T&gt;&gt;`(內部可變性);④ 圖遍歷與 `Arc&lt;Mutex&lt;T&gt;&gt;`;⑤ `unsafe` 邊界與安全抽象;⑥ 內建 vs 手寫權衡;⑦ 決策表(Vec/LinkedList);⑧ 串起來+延伸。手刻:用所有權視角重寫 BST,示範 borrow 衝突與解法。圖≥2、練習≥4。
- [ ] 1 寫 `chapters/src/87-rust-collections-ds.html`
- [ ] 2 `python build.py 87-rust-collections-ds`
- [ ] 3 `python build.py --check 87-rust-collections-ds` → ✓
- [ ] 4 book.js:`87-rust-collections-ds` done→true
- [ ] 5 `git add chapters/src/87-rust-collections-ds.html chapters/87-rust-collections-ds.html assets/book.js && git commit -m "feat(textbook): add ch81 rust ownership-aware data structures"`

## Task 6: ch82 無懼並行與非同步 — src `88-rust-concurrency.html`(第 82 章,★★★★☆)
**Cross-links:** callout→§43 平行(本章補 safety 視角)、§24 OS。
**大綱:** h2(≥8):① 為何並行難(資料競爭,對比 §43);② `thread::spawn` 與 move 閉包;③ `Send`/`Sync`:型別系統如何在編譯期擋資料競爭(SVG);④ 訊息傳遞 channel;⑤ 共享狀態 `Arc&lt;Mutex&lt;T&gt;&gt;`;⑥ async/await 心智模型;⑦ tokio 並發抓取小例;⑧ 串起來+延伸。手刻:多執行緒計數器(先被擋→Arc/Mutex 修正)+ async demo。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/88-rust-concurrency.html`
- [ ] 2 `python build.py 88-rust-concurrency`
- [ ] 3 `python build.py --check 88-rust-concurrency` → ✓
- [ ] 4 book.js:`88-rust-concurrency` done→true
- [ ] 5 `git add chapters/src/88-rust-concurrency.html chapters/88-rust-concurrency.html assets/book.js && git commit -m "feat(textbook): add ch82 rust fearless concurrency & async"`

## Task 7: ch83 Rust 實戰:CLI 工具與最小服務 — src `89-rust-project.html`(第 83 章,★★★☆☆)
**Cross-links:** 預告→§97 MCP(Rust server)、§84 OS。
**大綱:** h2(≥8):① 專案結構與模組;② cargo 生態;③ 解析參數做 CLI(檔案統計);④ 單元/整合測試;⑤ 錯誤處理整合(承 §80);⑥ 最小 HTTP 端點(預告 MCP server);⑦ 發佈;⑧ 串起來+延伸。手刻:可 `cargo run` 的 CLI 或最小 HTTP 服務。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/89-rust-project.html`
- [ ] 2 `python build.py 89-rust-project`
- [ ] 3 `python build.py --check 89-rust-project` → ✓
- [ ] 4 book.js:`89-rust-project` done→true
- [ ] 5 `git add chapters/src/89-rust-project.html chapters/89-rust-project.html assets/book.js && git commit -m "feat(textbook): add ch83 rust hands-on project"`

## Task 8: ch84 用 Rust 手寫迷你作業系統核心 — src `90-rust-os-kernel.html`(第 84 章,★★★★★)
**Cross-links:** callout→§21 CPU、§24 OS、§94 手寫迷你 Docker(系統底層動手三連發)。
**誠實標示:** 導引式精簡核心。h2(≥8):① 從 main 到 bare-metal(`no_std`);② freestanding binary 與開機(SVG);③ VGA/序列輸出印 "Hello kernel";④ 中斷與例外;⑤ 分頁與虛擬記憶體(呼應 §24,SVG);⑥ 玩具排程器概念;⑦ 在 QEMU 跑;⑧ 串起來+延伸(blog_os/rCore)。手刻:能印字的最小核心(節錄關鍵碼,完整指外部教程)。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/90-rust-os-kernel.html`
- [ ] 2 `python build.py 90-rust-os-kernel`
- [ ] 3 `python build.py --check 90-rust-os-kernel` → ✓
- [ ] 4 book.js:`90-rust-os-kernel` done→true
- [ ] 5 `git add chapters/src/90-rust-os-kernel.html chapters/90-rust-os-kernel.html assets/book.js && git commit -m "feat(textbook): add ch84 minimal OS kernel in rust"`

---

# 章節任務群 B:第二一部 · 容器/虛擬化(Tasks 9–16)

> eyebrow 一律 `第二一部 · 容器、虛擬化與雲原生底層`。

## Task 9: ch85 虛擬化全景 — src `91-virt-landscape.html`(第 85 章,★★★☆☆)
**Cross-links:** callout→§24 OS。
**大綱:** h2(≥8):① 為何隔離/虛擬化;② 隔離光譜:行程→容器→VM→unikernel(SVG);③ VM vs 容器架構(SVG:hypervisor 各跑 OS vs 共享 kernel);④ 取捨(啟動/隔離/開銷);⑤ 現代生態一覽;⑥ WASM 與 unikernel 旁支;⑦ 情境選型;⑧ 串起來+延伸(webvm)。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/91-virt-landscape.html`
- [ ] 2 `python build.py 91-virt-landscape`
- [ ] 3 `python build.py --check 91-virt-landscape` → ✓
- [ ] 4 book.js:`91-virt-landscape` done→true
- [ ] 5 `git add chapters/src/91-virt-landscape.html chapters/91-virt-landscape.html assets/book.js && git commit -m "feat(textbook): add ch85 virtualization landscape"`

## Task 10: ch86 虛擬機與 Hypervisor 底層 — src `92-vm-hypervisor.html`(第 86 章,★★★★☆)
**Cross-links:** callout→§48 計算機架構(補 VT-x 細節)、§24 OS。
**前置鐵則:** §48 只暗示 VT-x → 本章補滿。h2(≥8):① Type-1 vs Type-2(SVG);② trap-and-emulate 為何難;③ VT-x/AMD-V(root/non-root);④ 影子分頁→EPT/NPT(SVG:GVA→GPA→HPA);⑤ I/O 虛擬化與 virtio;⑥ KVM/QEMU 合作;⑦ WASM 作為輕量 VM;⑧ 串起來+延伸。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/92-vm-hypervisor.html`
- [ ] 2 `python build.py 92-vm-hypervisor`
- [ ] 3 `python build.py --check 92-vm-hypervisor` → ✓
- [ ] 4 book.js:`92-vm-hypervisor` done→true
- [ ] 5 `git add chapters/src/92-vm-hypervisor.html chapters/92-vm-hypervisor.html assets/book.js && git commit -m "feat(textbook): add ch86 vm & hypervisor internals"`

## Task 11: ch87 容器的真相 — src `93-container-internals.html`(第 87 章,★★★★☆)
**Cross-links:** callout→§24 OS、§34–36 資安、預告 §94。
**大綱:** h2(≥8):① chroot 歷史與不足;② 六大 namespace(SVG:隔離視圖);③ cgroups 資源限制;④ OverlayFS 分層(SVG:lower/upper/merged);⑤ capabilities;⑥ seccomp;⑦ 組起來就是容器;⑧ 串起來+延伸。範例 bash/C(`unshare`、`/proc`、cgroup fs,跳脫 `&lt;`)。圖≥2、練習≥3(用 `unshare` 觀察 pid namespace)。
- [ ] 1 寫 `chapters/src/93-container-internals.html`
- [ ] 2 `python build.py 93-container-internals`
- [ ] 3 `python build.py --check 93-container-internals` → ✓
- [ ] 4 book.js:`93-container-internals` done→true
- [ ] 5 `git add chapters/src/93-container-internals.html chapters/93-container-internals.html assets/book.js && git commit -m "feat(textbook): add ch87 container internals"`

## Task 12: ch88 手寫迷你 Docker — src `94-mini-docker.html`(第 88 章,★★★★★)
**Cross-links:** callout→§87、§84 OS、§90 Rust(可選 Rust 版)、CTF 部(沙箱)。
**誠實標示:** 教學用最小 runtime。h2(≥8):① 目標 `mydocker run`;② `clone()`/`unshare` 開 namespaces(C,跳脫 `&lt;`);③ `pivot_root`/`chroot` 換根;④ 掛 `/proc`、設 hostname;⑤ cgroups 限 CPU/記憶體;⑥ overlayfs 可寫層;⑦ (選)veth 網路;⑧ 這就是 Docker 的骨;⑨ 串起來+延伸。範例 C＋bash(或標 Rust)。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/94-mini-docker.html`
- [ ] 2 `python build.py 94-mini-docker`
- [ ] 3 `python build.py --check 94-mini-docker` → ✓
- [ ] 4 book.js:`94-mini-docker` done→true
- [ ] 5 `git add chapters/src/94-mini-docker.html chapters/94-mini-docker.html assets/book.js && git commit -m "feat(textbook): add ch88 build your own mini docker"`

## Task 13: ch89 Docker 實戰 — src `95-docker-practice.html`(第 89 章,★★★☆☆)
**Cross-links:** callout→§88(原理)、預告 §106(容器化 agent)。
**大綱:** h2(≥8):① 映像 vs 容器;② Dockerfile 與分層快取(SVG);③ 容器生命週期;④ volume;⑤ bridge/host 網路與埠對應;⑥ docker compose 多容器;⑦ 把一個服務容器化;⑧ 串起來+延伸。範例 bash/yaml/Dockerfile。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/95-docker-practice.html`
- [ ] 2 `python build.py 95-docker-practice`
- [ ] 3 `python build.py --check 95-docker-practice` → ✓
- [ ] 4 book.js:`95-docker-practice` done→true
- [ ] 5 `git add chapters/src/95-docker-practice.html chapters/95-docker-practice.html assets/book.js && git commit -m "feat(textbook): add ch89 docker in practice"`

## Task 14: ch90 Kubernetes 編排與雲原生 — src `96-kubernetes.html`(第 90 章,★★★★☆)
**Cross-links:** callout→§11 架構、§40 軟工、預告 §92。
**大綱:** h2(≥8):① 多容器之後的問題;② 宣告式 vs 命令式;③ Pod;④ Deployment;⑤ Service/Ingress(SVG:物件關係);⑥ 自我修復與水平擴展;⑦ minikube/kind 跑服務(yaml);⑧ 串起來+延伸。範例 yaml/bash。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/96-kubernetes.html`
- [ ] 2 `python build.py 96-kubernetes`
- [ ] 3 `python build.py --check 96-kubernetes` → ✓
- [ ] 4 book.js:`96-kubernetes` done→true
- [ ] 5 `git add chapters/src/96-kubernetes.html chapters/96-kubernetes.html assets/book.js && git commit -m "feat(textbook): add ch90 kubernetes & cloud native"`

## Task 15: ch91 eBPF:核心可程式化 — src `97-ebpf.html`(第 91 章,★★★★★)
**Cross-links:** callout→§87、§34–36 資安、CTF 部、§90(Cilium)。
**大綱:** h2(≥8):① 問題:安全地在核心跑使用者程式;② eBPF 程式+verifier+map(SVG:載入到執行);③ 掛載點 kprobe/tracepoint/XDP;④ 動手:libbpf 或 Python(bcc)寫觀測程式(統計系統呼叫);⑤ 安全/沙箱意義;⑥ 在雲原生的角色(Cilium);⑦ 與容器/資安連結;⑧ 串起來+延伸。範例 C＋libbpf/Python。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/97-ebpf.html`
- [ ] 2 `python build.py 97-ebpf`
- [ ] 3 `python build.py --check 97-ebpf` → ✓
- [ ] 4 book.js:`97-ebpf` done→true
- [ ] 5 `git add chapters/src/97-ebpf.html chapters/97-ebpf.html assets/book.js && git commit -m "feat(textbook): add ch91 ebpf programmable kernel"`

## Task 16: ch92 分散式系統與高可用架構 — src `98-distributed-systems.html`(第 92 章,★★★★☆)
**Cross-links:** callout→§11 架構、§25 網路。
**前置鐵則:** 書中無 Raft/CAP 前置 → 本章自含完整入門。h2(≥8):① 為何分散式難(部分失效);② 複製;③ 一致性模型;④ CAP 直覺(SVG);⑤ 共識:Raft 的 leader/log/選舉(SVG);⑥ 分片與負載;⑦ 服務網格與可觀測性;⑧ 串起來+延伸。範例 概念+Python 小例(簡化 quorum)。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/98-distributed-systems.html`
- [ ] 2 `python build.py 98-distributed-systems`
- [ ] 3 `python build.py --check 98-distributed-systems` → ✓
- [ ] 4 book.js:`98-distributed-systems` done→true
- [ ] 5 `git add chapters/src/98-distributed-systems.html chapters/98-distributed-systems.html assets/book.js && git commit -m "feat(textbook): add ch92 distributed systems & HA"`

---

# 章節任務群 C:第二二部 · LLM Agent(Tasks 17–24)

> eyebrow 一律 `第二二部 · 動手打造 LLM Agent`。後章沿用前章介面:§94 定義 `LLMClient.chat(messages)->str` / `.complete(prompt)->str`;§95 `Tool`/`ToolRegistry`/`run_react(...)`;§96 `VectorStore`/`rag_answer(...)`,名稱跨章一致。

## Task 17: ch93 從零打造 GPT(選修)— src `99-gpt-from-scratch.html`(第 93 章,★★★★★)
**Cross-links:** callout→§38 ML(複用反向傳播)、§54 線性代數、§67 CV(明確區隔)。
**去重/前置鐵則:** §38 已教反向傳播/梯度下降/激活(複用);缺 Softmax/tokenization/embedding/Transformer → 本章自帶;**明講 CNN(§67)影像 vs Transformer 文本**。標「選修」。h2(≥8):① 語言模型在做什麼;② tokenization;③ embedding;④ 注意力直覺 Q/K/V(SVG);⑤ Softmax(補 §38 缺口);⑥ Transformer block;⑦ 預訓練 vs 微調;⑧ 概念性手刻 mini-GPT(節錄,指 nanoGPT/Raschka);⑨ 與 CNN 的差異;⑩ 串起來+延伸。範例 Python(PyTorch)。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/99-gpt-from-scratch.html`
- [ ] 2 `python build.py 99-gpt-from-scratch`
- [ ] 3 `python build.py --check 99-gpt-from-scratch` → ✓
- [ ] 4 book.js:`99-gpt-from-scratch` done→true
- [ ] 5 `git add chapters/src/99-gpt-from-scratch.html chapters/99-gpt-from-scratch.html assets/book.js && git commit -m "feat(textbook): add ch93 build gpt from scratch (optional)"`

## Task 18: ch94 手刻你的 LLM client — src `100-llm-client.html`(第 94 章,★★★☆☆)
**Cross-links:** callout→§93(選修底層)、§38 ML。
**大綱:** h2(≥8):① 半章複習:token/嵌入/取樣/溫度/context window/提示工程(callout→§93/§38);② 設計中立介面 `LLMClient`;③ 接本地 Ollama(附 `ollama pull`);④ 同介面接 Claude(需金鑰);⑤ 結構化 JSON 輸出;⑥ 系統提示與 few-shot;⑦ 串起來+延伸。**Produces:** `LLMClient.chat(messages)->str`、`.complete(prompt)->str`。範例 Python。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/100-llm-client.html`
- [ ] 2 `python build.py 100-llm-client`
- [ ] 3 `python build.py --check 100-llm-client` → ✓
- [ ] 4 book.js:`100-llm-client` done→true
- [ ] 5 `git add chapters/src/100-llm-client.html chapters/100-llm-client.html assets/book.js && git commit -m "feat(textbook): add ch94 hand-build your llm client"`

## Task 19: ch95 工具呼叫與 ReAct — src `101-tool-react.html`(第 95 章,★★★★☆)
**Cross-links:** callout→§94(用其 `LLMClient`)、§87/§88 沙箱。
**大綱:** h2(≥8):① 為何 LLM 需要工具;② tool calling 原理(schema→呼叫→執行→回填,SVG);③ 手刻工具註冊表;④ 手刻 ReAct 迴圈(Thought→Action→Observation,SVG);⑤ 工具:計算機;⑥ 工具:讀檔與 shell(⚠️ 沙箱,連 §88);⑦ 失敗處理與迴圈上限;⑧ 串起來+延伸。**Consumes:** `LLMClient.chat`。**Produces:** `Tool`/`ToolRegistry`/`run_react(client,registry,task)->str`。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/101-tool-react.html`
- [ ] 2 `python build.py 101-tool-react`
- [ ] 3 `python build.py --check 101-tool-react` → ✓
- [ ] 4 book.js:`101-tool-react` done→true
- [ ] 5 `git add chapters/src/101-tool-react.html chapters/101-tool-react.html assets/book.js && git commit -m "feat(textbook): add ch95 tool calling & react loop"`

## Task 20: ch96 手刻最小 RAG — src `102-rag-from-scratch.html`(第 96 章,★★★★☆)
**Cross-links:** callout→§54 線性代數(餘弦相似度,不重講)、§37 資料庫(向量 vs 結構化)、§94。
**互連鐵則:** 餘弦相似度 §54 已教 → callout;§37 無向量搜尋 → 輕提差異。h2(≥8):① 為何 RAG;② 嵌入與向量空間;③ 餘弦相似度(callout→§54);④ chunking;⑤ 手刻 in-memory 向量庫;⑥ 升級 sqlite/FAISS;⑦ retrieve→augment→generate;⑧ 短期 vs 長期記憶;⑨ 混合檢索/rerank/GraphRAG 概念;⑩ 串起來+延伸。**Consumes:** `LLMClient`。**Produces:** `VectorStore.add/search`、`rag_answer(client,store,query)->str`。範例 Python。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/102-rag-from-scratch.html`
- [ ] 2 `python build.py 102-rag-from-scratch`
- [ ] 3 `python build.py --check 102-rag-from-scratch` → ✓
- [ ] 4 book.js:`102-rag-from-scratch` done→true
- [ ] 5 `git add chapters/src/102-rag-from-scratch.html chapters/102-rag-from-scratch.html assets/book.js && git commit -m "feat(textbook): add ch96 build minimal rag"`

## Task 21: ch97 MCP:可插拔的標準服務 — src `103-mcp.html`(第 97 章,★★★★☆)
**Cross-links:** callout→§95 工具、§87/§88 沙箱、CTF 部(MCP 安全)、§89 Rust(可選 Rust server)。
**大綱:** h2(≥8):① 為何需要 MCP;② 協定架構 host/client/server、tools/resources/prompts、JSON-RPC over stdio/SSE(SVG);③ 手刻 MCP server(Python 官方 SDK);④ 手刻 MCP client 接 §95 agent;⑤ 接 Claude Desktop;⑥ 安全:prompt injection/tool poisoning/權限(連 mcp-scan、§88、CTF);⑦ (選)Rust server;⑧ 串起來+延伸。範例 Python(可選 Rust)。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/103-mcp.html`
- [ ] 2 `python build.py 103-mcp`
- [ ] 3 `python build.py --check 103-mcp` → ✓
- [ ] 4 book.js:`103-mcp` done→true
- [ ] 5 `git add chapters/src/103-mcp.html chapters/103-mcp.html assets/book.js && git commit -m "feat(textbook): add ch97 mcp pluggable tools"`

## Task 22: ch98 進階單代理:規劃、反思、自我改進 — src `104-agent-advanced.html`(第 98 章,★★★★☆)
**Cross-links:** callout→§95 ReAct、預告 §99。
**大綱:** h2(≥8):① ReAct 的侷限;② Plan-and-Execute(SVG);③ reflection/self-critique 迴圈;④ 記憶增強(把 §96 RAG 當長期記憶);⑤ 子目標分解;⑥ 失敗模式(迴圈/幻覺/工具誤用);⑦ 護欄;⑧ 串起來+延伸。範例 Python(用前面零件)。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/104-agent-advanced.html`
- [ ] 2 `python build.py 104-agent-advanced`
- [ ] 3 `python build.py --check 104-agent-advanced` → ✓
- [ ] 4 book.js:`104-agent-advanced` done→true
- [ ] 5 `git add chapters/src/104-agent-advanced.html chapters/104-agent-advanced.html assets/book.js && git commit -m "feat(textbook): add ch98 advanced single-agent patterns"`

## Task 23: ch99 多代理協作系統 — src `105-multi-agent.html`(第 99 章,★★★★☆)
**Cross-links:** callout→§98、§97 MCP。
**大綱:** h2(≥8):① 單 vs 多代理取捨;② 拓樸:協調者-工作者;③ 流水線;④ 辯論/投票(SVG);⑤ 代理間通訊與共享記憶;⑥ 17 架構/21 模式精選導覽;⑦ 動手:用前面零件組「多代理研究 agent」(對照 nanoDeepResearch);⑧ 串起來+延伸。範例 Python。圖≥2、練習≥3。
- [ ] 1 寫 `chapters/src/105-multi-agent.html`
- [ ] 2 `python build.py 105-multi-agent`
- [ ] 3 `python build.py --check 105-multi-agent` → ✓
- [ ] 4 book.js:`105-multi-agent` done→true
- [ ] 5 `git add chapters/src/105-multi-agent.html chapters/105-multi-agent.html assets/book.js && git commit -m "feat(textbook): add ch99 multi-agent systems"`

## Task 24: ch100 從玩具到生產 — src `106-agent-production.html`(第 100 章,★★★★☆)
**Cross-links:** callout→§95–§99(對應框架)、§89/§90 容器/k8s(部署)。
**大綱:** h2(≥8):① 何時換框架(手刻零件↔LangGraph/OpenAI Agents SDK 對應表);② 評估(eval);③ 追蹤與可觀測性;④ 護欄與安全(連 §97);⑤ 成本/延遲/快取;⑥ 部署:容器化 agent(連 §89/§90);⑦ 收尾:包成服務 + 全書收束;⑧ 串起來+延伸。範例 Python/yaml/Dockerfile。圖≥1、練習≥3。
- [ ] 1 寫 `chapters/src/106-agent-production.html`
- [ ] 2 `python build.py 106-agent-production`
- [ ] 3 `python build.py --check 106-agent-production` → ✓
- [ ] 4 book.js:`106-agent-production` done→true
- [ ] 5 `git add chapters/src/106-agent-production.html chapters/106-agent-production.html assets/book.js && git commit -m "feat(textbook): add ch100 from toy to production"`

---

## Task 25: 回補既有章雙向 callout + 全量驗證

**Files:** Modify 既有章的 **src 片段**(`chapters/src/NN-*.html`),各加一個 `callout note`(置於章末「把這一章串起來」附近,輕量一句＋連結,不改主體),再 rebuild:
- `src/38-machine-learning.html` → §93、§94
- `src/24-operating-system.html` → §85/§86/§87、§84
- `src/43-parallel.html` → §82
- `src/28-sorting-searching.html`、`src/29-data-structures.html` → §81
- `src/09-types.html` → §79/§80
- `src/48-computer-architecture.html` → §86
- `src/11-software-architecture.html`、`src/25-networking.html` → §92
- `src/37-databases.html` → §96
- `src/34-security-fundamentals.html`(或既有資安/CTF 章)→ §87/§88/§91/§97

callout 樣式(連結用相對 `href`,例 `93-container-internals.html`):
```html
<div class="callout note"><div class="ico">🧭</div><div class="body">
<span class="c-title">延伸:新軌道</span>
<p>想知道作業系統的「行程/記憶體隔離」如何長成 Docker?見<a href="93-container-internals.html">第 87 章 容器的真相</a>;想親手寫一顆核心?見<a href="90-rust-os-kernel.html">第 84 章 用 Rust 手寫迷你 OS</a>。</p>
</div></div>
```

- [ ] **Step 1** 逐一改既有章 src 片段加入對應 callout。
- [ ] **Step 2** Rebuild 受影響章:`python build.py 38-machine-learning 24-operating-system 43-parallel 28-sorting-searching 29-data-structures 09-types 48-computer-architecture 11-software-architecture 25-networking 37-databases 34-security-fundamentals`
- [ ] **Step 3** 全量同步與驗證:`python build.py --verify` → 全部同步;`python build.py --check`(全章)→ 既有章維持原狀態、22 新章 ✓、新章間/對既有章的跨連結目標皆存在。
- [ ] **Step 4** commit:`git add chapters/src/*.html chapters/*.html && git commit -m "feat(textbook): cross-link existing chapters to parts 20-22"`

---

## Self-Review(寫計畫者自查)

- **建置系統對齊**:已改為 `chapters/src/*.html` 片段 + `build.py`;移除多餘的「自建驗證器」任務(`chapters/_validate_chapter.py` 已存在),Task 1 改為管線冒煙測試。
- **Spec 覆蓋**:三部 22 章 → Task 3–24 一一對應;§10 去重/前置/互連 → 落到各任務鐵則與 Task 25;book.js → Task 2。
- **驗證器硬規則**:已寫進 Global Constraints(≥8 h2、1 h1、跳脫、無 style、必備區塊、跨連結存在);各章大綱均列 ≥8 個 h2。
- **Placeholder 掃描**:無 TBD;各章給具體 h2 骨架、手刻產物、圖/練習下限、build/check/commit 指令。
- **介面一致**:§94 `LLMClient.chat/complete` → §95 `run_react`、§96 `rag_answer`/`VectorStore` 沿用;名稱跨任務一致。
- **時序風險**:新章互連的 --check 連結檢查需目標已建 → Task 25 Step 3 做全量收尾驗證;個別章 --check 對未建連結報錯屬預期(advisory,不阻擋)。
- **行尾**:`.gitattributes` 已釘 CRLF,`build.py` 以 `newline=''` 保留,作者照常寫即可。
