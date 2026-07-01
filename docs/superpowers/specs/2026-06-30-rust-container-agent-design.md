# Rust／容器虛擬化／LLM Agent 三部整合進「CS 自學聖經」— 設計文件

- 日期:2026-06-30
- 狀態:已核准設計,待寫實作計畫
- 來源素材:`textbook/reference/GitHubDaily/`(GitHubDaily 開源策展庫:主 `README.md` 約 455KB + `2018–2024.md` 年度檔)。**這是一份「項目名稱＋一句簡介＋連結」的發現地圖,不是教程全文**;它的作用是鎖定一流開源教程當作新章節的「課綱骨幹＋延伸閱讀」,章節內文仍依 `_AUTHOR_GUIDE.md` 原創撰寫。

---

## 1. 目標與範圍

在既有 19 部(顯示 1–78 章)＋附錄題庫的基礎上,新增 **3 個「部」、共 22 章**,讓資工系學生能:

1. 掌握 **Rust** 系統程式語言,直到能用它手寫一個迷你 OS 核心;
2. 拆開 **Docker／虛擬機** 的底層魔法(namespaces／cgroups／hypervisor),並親手拼一個迷你 container runtime;
3. **一步一步手刻自己的 LLM Agent**——從 ReAct 迴圈、RAG、MCP 到多代理協作,理解原理後再上主流框架。

- **做**:新增第二十~二二部共 22 章;在既有章節加雙向 callout 互連。
- **不做**:不重新編號既有 1–78 章與附錄;不把開源教程整段翻譯搬運(僅作課綱骨幹與延伸連結);不引入與三主題無關的工具型項目成章。
- **定位**:延續本書「由淺入深、中英對照、Medium 敘事、動手手刻」風格;每章都要有「直覺說明＋可跑程式碼／手繪 SVG＋練習題＋可展開解答」。

### 1.1 核心設計決策(來自需求釐清)

| 決策點 | 結論 |
|---|---|
| Agent 實作主軸 | **Python 從零手刻為主**;理解原理後,最後一章才對應到 LangGraph／OpenAI Agents SDK 等框架 |
| LLM 後端 | **手刻一個中立 `LLMClient` 介面**;預設接本地 **Ollama**(免金鑰、零成本、可離線),同介面切換 **Claude(Anthropic API)** 跑需要穩定 tool-calling 的 demo |
| LLM 底層前置 | 在**第 38 章機器學習**尾端加「通往大型語言模型」callout,雙向連到第二二部與 GPT 選修章;新部本身專注 agent 層 |
| 規模 | 均衡三部;加選 4 章後 = **22 章** |
| 三個擺放判斷 | ①「分散式與高可用」併入第二一部接在 Kubernetes 後;②「從零打造 GPT(選修)」當第二二部開場;③「用 Rust 手寫迷你 OS 核心」當第二十部 capstone |

---

## 2. 編號與插入機制(動手前必讀)

- **慣例**:本書「**顯示章號 ≠ 檔名 id**」。例如 SICP 部檔名 `80–84`,顯示卻是「第 74–78 章」;附錄檔名 `74–79`,顯示為「附A–附F」。
- 既有主線**顯示章號**最大為 **第 78 章**(SICP 暫存器機器,檔 `84-sicp-register-machines.html`)。
- **新內容**:顯示章號從 **第 79 章**接續;檔名 id 從 **85** 接續。新部在 `assets/book.js` 的 `BOOK.parts` 陣列中,**插在「第十九部 · SICP」之後、「附錄 · 完整題庫」之前**。
- 每個新章在 `BOOK.parts[].chapters[]` 加一筆 `{ id, num, title, en, done }`。**先 `done:false`**,該章 HTML 完成並通過自檢後再改 `done:true`,側欄與上下章連結才會啟用。

### 2.1 章號對照總表(檔名 id → 顯示章號)

| 檔名 id | 顯示章號 | slug | 部 |
|---|---|---|---|
| 85 | 79 | `85-rust-ownership` | 第二十部 Rust |
| 86 | 80 | `86-rust-types-errors` | 第二十部 Rust |
| 87 | 81 | `87-rust-collections-ds` | 第二十部 Rust |
| 88 | 82 | `88-rust-concurrency` | 第二十部 Rust |
| 89 | 83 | `89-rust-project` | 第二十部 Rust |
| 90 | 84 | `90-rust-os-kernel` | 第二十部 Rust(capstone) |
| 91 | 85 | `91-virt-landscape` | 第二一部 容器/虛擬化 |
| 92 | 86 | `92-vm-hypervisor` | 第二一部 容器/虛擬化 |
| 93 | 87 | `93-container-internals` | 第二一部 容器/虛擬化 |
| 94 | 88 | `94-mini-docker` | 第二一部 容器/虛擬化 |
| 95 | 89 | `95-docker-practice` | 第二一部 容器/虛擬化 |
| 96 | 90 | `96-kubernetes` | 第二一部 容器/虛擬化 |
| 97 | 91 | `97-ebpf` | 第二一部 容器/虛擬化 |
| 98 | 92 | `98-distributed-systems` | 第二一部 容器/虛擬化 |
| 99 | 93 | `99-gpt-from-scratch` | 第二二部 Agent(選修) |
| 100 | 94 | `100-llm-client` | 第二二部 Agent |
| 101 | 95 | `101-tool-react` | 第二二部 Agent |
| 102 | 96 | `102-rag-from-scratch` | 第二二部 Agent |
| 103 | 97 | `103-mcp` | 第二二部 Agent |
| 104 | 98 | `104-agent-advanced` | 第二二部 Agent |
| 105 | 99 | `105-multi-agent` | 第二二部 Agent |
| 106 | 100 | `106-agent-production` | 第二二部 Agent |

---

## 3. 第二十部 · Rust 系統程式設計(6 章 🦀)

> **部 blurb**:從所有權到無懼並行,再到親手寫一顆會開機的核心——用一門「編譯器當你導師」的語言,重新理解記憶體、型別與系統。

| 顯示章 | 標題 | 重點與手刻產物 | 範例語言 | 對照資源 |
|---|---|---|---|---|
| 79 | 所有權、借用與生命週期 | 為何 Rust(無 GC 的記憶體安全);**因書中無專章講 C 指標/手動記憶體(§02 僅輕帶),本章自己把「C 手動管理之痛」——懸空指標/double free/memory leak——講足當動機**;cargo、move/borrow、可變借用、生命週期初步;用 Rust 重寫書中小程式感受 borrow checker | Rust(對照 C) | `sunface/rust-course`、`mainmatter/100-exercises-to-learn-rust`、MS「Take your first steps with Rust」 |
| 80 | 型別、trait、列舉與錯誤處理 | **§09 型別 + §44 Haskell 已教 ADT/列舉/Option/泛型/模式比對 → 本章不重教,僅 callout 複習**;火力放在 Rust 新東西:**trait 系統(vs 介面)**、`Result` 錯誤處理的**所有權視角**、`?` 運算子、trait objects | Rust | `sunface/rust-by-practice`;callout→§09/§44 |
| 81 | 集合、迭代器與「所有權視角」的資料結構 | **§28–29 已教排序/BFS/DFS/DP 與各結構邏輯 → 本章不重講演算法本身**;改示範「所有權如何改造實現」:`Box` 鏈結 vs 裸指標、樹為何需 `Rc<RefCell<T>>`、圖遍歷的 `Arc<Mutex<T>>`、`unsafe` 邊界、內建 Vec/HashMap vs 手寫的權衡;迭代器與閉包 | Rust | `QMHTMY/RustBook`(**繁中版**);callout→§28/§29 |
| 82 | 無懼並行與非同步 | thread、`Send`/`Sync`、channel、`Arc`/`Mutex`、async/await、tokio 簡介 | Rust | `sunface/async-book` |
| 83 | Rust 實戰:CLI 工具與最小服務 | 模組/crate/測試/發佈;做一個 CLI 工具或最小 HTTP 服務(為「用 Rust 寫 MCP server」鋪路) | Rust | `LukeMathWalker/zero-to-production` |
| 84 | **(capstone)用 Rust 手寫迷你作業系統核心** | bare-metal、no_std、開機流程、VGA/序列輸出、中斷、分頁、簡單排程;誠實標示為「導引式重構」 | Rust(少量 asm) | `phil-opp/blog_os`、`LearningOS/rust-based-os-comp2022`(rCore) |

**雙向連結**:§9 型別→§79;§24 OS→§84;§28–32 演算法→§81;§43 平行→§82;§42 編譯器→§80;§84 ↔ 第二一部(系統底層動手三連發)。

---

## 4. 第二一部 · 容器、虛擬化與雲原生底層【進階】(8 章 📦)

> **部 blurb**:一個程式如何「以為自己獨佔整台電腦」?從 chroot、namespaces、cgroups 到 hypervisor,再到 eBPF 與分散式——拆開 Docker、VM 與雲原生的魔法,並親手拼一個出來。

| 顯示章 | 標題 | 重點與手刻產物 | 範例語言 | 對照資源 |
|---|---|---|---|---|
| 85 | 虛擬化全景:行程隔離→VM→容器 | 為何要隔離/虛擬化;隔離光譜(行程→容器→VM→unikernel);VM vs 容器架構(SVG:hypervisor vs 共享 kernel) | 概念為主 | `isno/theByteBook`、`leaningtech/webvm` |
| 86 | 虛擬機與 Hypervisor 底層 | **§48 只暗示 VT-x、無細節 → 本章補滿**:Type-1/2、硬體輔助虛擬化(VT-x/AMD-V)、KVM/QEMU、記憶體虛擬化(影子分頁/EPT)、virtio I/O;WASM 作為輕量 VM 旁支 | C/概念 | `theByteBook`、`webvm`;callout→§48 |
| 87 | 容器的真相:namespaces / cgroups / OverlayFS | chroot 歷史;6 大 namespace(pid/net/mnt/uts/ipc/user)、cgroups 資源限制、OverlayFS 分層映像、capabilities/seccomp(理論) | C/bash | `MintCN/linux-insides-zh`、`sysprog21/lkmpg` |
| 88 | **手寫迷你 Docker(動手)** | 從零拼一個 container runtime:`clone()`/`unshare` 開 namespace + `pivot_root` 換根 + cgroups 限資源 + overlayfs 掛載 + 簡單網路;不裝 Docker | C＋bash(或用 Rust,呼應第二十部;不引入 Go 以維持語言一致) | Liz Rice「containers from scratch」概念、`yeasy/docker_practice` |
| 89 | Docker 實戰:映像、網路、Compose | Dockerfile、映像分層與快取、容器生命週期、volume、bridge/host 網路、docker compose 多容器;把一個服務容器化 | bash/yaml | `yeasy/docker_practice`、`docker/getting-started` |
| 90 | Kubernetes 編排與雲原生 | 為何需要編排;Pod/Deployment/Service/Ingress、宣告式設定、自我修復與水平擴展;minikube/kind 跑一個服務 | yaml | `guangzhengli/k8s-tutorials`、`MichaelCade/90DaysOfDevOps` |
| 91 | eBPF:核心可程式化(觀測/網路/安全) | eBPF 是什麼、verifier、map、掛載點(kprobe/tracepoint/XDP);動手寫一支 eBPF 觀測程式;與容器/雲原生(Cilium)、資安的連結 | C＋libbpf/Python | `eunomia-bpf/bpf-developer-tutorial` |
| 92 | 分散式系統與高可用架構 | **§11 只講設計模式、§25 只講單點通訊 → 無 Raft/CAP 前置,本章須自成完整入門**:為何分散式難、共識(Raft 直覺)、複製、分片、CAP/一致性模型、服務網格、可觀測性 | 概念＋Python 小例 | `isno/theByteBook`;callout→§11/§25 |

**雙向連結**:§24 OS→§85/§87;§34–36 資安 & CTF 部→§87/§88/§91(隔離、最小權限、eBPF 安全);§11 架構 & §40 軟工→§90/§92;§43 平行→§92;第二十部 §84 ↔ §88(手刻系統底層)。

---

## 5. 第二二部 · 動手打造 LLM Agent(8 章 🤖)

> **部 blurb**:不靠魔法框架,一步一步手刻——從一個會呼叫工具的迴圈,到能檢索、能用 MCP、會協作的自主 agent。**手刻為主,最後一章才上框架。**

| 顯示章 | 標題 | 重點與手刻產物 | 範例語言 | 對照資源 |
|---|---|---|---|---|
| 93 | **從零打造 GPT(選修):看懂 agent 在跟誰說話** | 選修。**§38 已教反向傳播/梯度下降/激活函數(可複用),但缺 Softmax、tokenization、embedding、Transformer/注意力 → 本章自帶這些**;概念性手刻 mini-GPT;**明講「CNN(§67)是影像卷積、與 Transformer 文本處理不同」以免混淆**;標示為「想更深入才讀」 | Python(PyTorch) | `rasbt/LLMs-from-scratch`(+CN)、`karpathy/nn-zero-to-hero` |
| 94 | 手刻你的 LLM client | 半章複習(token/嵌入/取樣/溫度/context window/提示工程);**手刻中立 `LLMClient` 介面**:`.chat()`,預設接 Ollama、同介面切 Claude;結構化 JSON 輸出、系統提示、few-shot | Python | `chiphuyen/aie-book` |
| 95 | 工具呼叫與 ReAct | 工具呼叫原理(schema→模型產生呼叫→你執行→回填);**手刻 ReAct 迴圈(Thought→Action→Observation)**、工具註冊表/解析/分派;計算機、檔案、shell 工具(沙箱警告→§88) | Python | `liyuan24/nanoDeepResearch`、`ghuntley/how-to-build-a-coding-agent`、`agno-agi/agno` cookbook |
| 96 | 手刻最小 RAG | 為何 RAG;嵌入、cosine 相似度(**§54 線性代數已教餘弦相似度 → callout 過去,不重講數學**)、chunking;**先手刻 in-memory 向量庫,再上 sqlite/FAISS**;輕提「向量 vs §37 結構化資料」差異;retrieve→augment→generate;短期 vs 長期記憶;混合檢索/rerank/GraphRAG 概念 | Python | `NirDiamant/RAG_Techniques`、`microsoft/rag-time`、`bRAGAI/bRAG-langchain`、`1517005260/graph-rag-agent`;callout→§54/§37 |
| 97 | MCP:可插拔的標準服務 | 為何 MCP;協定架構(host/client/server、tools/resources/prompts、JSON-RPC over stdio/SSE);**手刻一個 MCP server＋client**,接到自己的 agent 與 Claude Desktop;安全(prompt injection、tool poisoning→`mcp-scan`、§87/§88 沙箱、CTF 部);可選用 Rust 寫 server(連第二十部) | Python(可選 Rust) | `microsoft/mcp-for-beginners`、`liaokongVFX/MCP-Chinese-Getting-Started-Guide`、`modelcontextprotocol/servers`、`mcp-use/mcp-use` |
| 98 | 進階單代理:規劃、反思、自我改進 | Plan-and-Execute、self-critique/reflection、記憶增強、子目標分解;單 agent 的能力上限與失敗模式 | Python | `FareedKhan-dev/all-agentic-architectures`、`ginobefun/agentic-design-patterns-cn` |
| 99 | 多代理協作系統 | 單 vs 多 agent;角色分工、協調者-工作者、辯論/投票、訊息傳遞與共享記憶;**用前面手刻的零件組一個「多代理研究 agent」**,對照 nanoDeepResearch | Python | `all-agentic-architectures`(17 架構)、`agentic-design-patterns-cn`(21 模式) |
| 100 | 從玩具到生產:框架、評估、可觀測性、部署 | 何時換上框架(把手刻概念對應到 LangGraph / OpenAI Agents SDK 元件);eval、追蹤/可觀測性、護欄與安全、成本與延遲、快取;**容器化部署 agent(連第二一部 §89/§90)** | Python | `ed-donner/agents`、`NirDiamant/agents-towards-production` |

**雙向連結**:§38 ML 尾端新增「通往大型語言模型」callout→§93/§94;§37 資料庫→§96(向量庫);§87/§88 容器沙箱→§95/§97;CTF 部→§97 MCP 安全;第二十部 §83→§97(Rust MCP server);§100→第二一部部署。

---

## 6. 既有章節要回補的雙向 callout(彙整)

| 既有章 | 加 callout 指向 |
|---|---|
| §9 型別、§28–32 演算法、§42 編譯器、§43 平行 | 第二十部 Rust 對應章 |
| §24 作業系統 | 第二一部 §85/§87/§88、第二十部 §84 |
| §11 軟體架構、§40 軟體工程 | 第二一部 §90/§92 |
| §34–36 資安、CTF 部(§69–73) | 第二一部 §87/§88/§91、第二二部 §97 |
| §37 資料庫 | 第二二部 §96 |
| **§38 機器學習(尾端)** | 第二二部 §93(GPT 選修)與 §94(動手打造 Agent) |

callout 一律輕量(`callout note`,一兩句＋連結),不改既有章主體敘事。

---

## 7. 撰寫規範與產製流程

> **建置系統(2026-06-30 已上線,務必遵守)**:本書採「內容/版型分離」。章節**來源**寫在 `chapters/src/NN-slug.html` 片段(檔首 `<!--meta-->` 含 `title`/`description`,其後為內文,從 `<div class="eyebrow">` 起);由 `python build.py NN-slug` 包進 `chapters/_layout.html` 產生 `chapters/NN-slug.html`。**不可直接編輯產出檔**。驗證器 `chapters/_validate_chapter.py` 已存在,用 `python build.py --check NN-slug` 呼叫。

- **動筆前**:每章撰寫者先讀 `_AUTHOR_GUIDE.md`(片段流程)與範本片段 `chapters/src/00-about.html`、`chapters/src/01-what-is-cs.html`,再參考同主題既有章(如 §24 OS、§38 ML、§43 平行)。
- **片段內容**:`.eyebrow` 寫部別、`.byline` 寫顯示章號/閱讀時間/難度、`.objectives`、**≥8 個 `<h2>`**、章末「把這一章串起來」＋延伸資源 callout(`<!DOCTYPE>`/`<head>`/`<article>`/`book.js` 由 `_layout.html` 提供,片段不要寫)。
- **程式碼**:可跑、中文註解;Python 表達想法、C/C++/Rust 展示底層;**務必跳脫 `<`→`&lt;`、`>`→`&gt;`、`&`→`&amp;`**(尤其 C/Rust 泛型 `Vec<T>`、`#include &lt;...&gt;`、shell 重導向)。
- **圖**:多畫手繪內嵌 SVG(虛擬化架構、namespace 隔離、ReAct 迴圈、RAG 流程、多代理拓樸、Raft 等),用指定配色與字型。
- **練習**:每章 3–6 題,難度遞增,附可展開解答。
- **完成後**:`python build.py NN-slug` 產生 → `python build.py --check NN-slug` 過驗證 → 把該章在 `book.js` 的 `done` 改為 `true` → commit(src 片段 + 產出 html + book.js)。
- **可跑性備註**:Agent 部以 Ollama 為預設後端,讀者無金鑰也能跑;需穩定 tool-calling 的範例附上 Claude 版設定。範例需註明所需套件與 `ollama pull` 指令。

---

## 8. 產製順序建議(供實作計畫參考)

1. 先在 `book.js` 一次補上三個新部與 22 個 `done:false` 章目(建立骨架與導覽)。
2. 平行 subagent 分批寫章(每章一個 agent,輸出 `chapters/src/NN-slug.html` 片段並 `python build.py`);建議批次:Rust 6 章 → 容器 8 章 → Agent 8 章。
3. 每章寫完即 `build` + `--check` + 翻 `done:true` + commit(src+產出+book.js)。
4. 最後統一補既有章的雙向 callout(§6 表),改其 `src/` 片段再 rebuild,並跑 `python build.py --verify` / `--check` 全量收尾。

---

## 9. 風險與注意

- **內容時效**:agent/MCP/RAG 生態變動快;章節以「原理與手刻」為主軸,框架/SDK 僅在 §100 點到,降低過時風險。
- **誠實標示**:§84 手寫 OS、§88 手寫 Docker、§93 手刻 GPT 均為「導引式精簡實作」,要明講「這是教學用最小版本,非生產級」。
- **不過度搬運**:reference 的開源教程僅作課綱骨幹與延伸連結,內文原創,避免版權與抄襲問題。
- **YAGNI**:reference 中大量工具型/應用型項目(AI 搜尋引擎平替、SaaS 模板、DevOps 清單等)不獨立成章,至多作延伸閱讀連結。

---

## 10. 完善度盤點(對照現有 1–78 章,2026-06-30)

以三組平行盤點代理實讀現有相關章節內文得出。**總評:三部設計完善且互補,補的是現有書真缺口,無重大重複教學。** 需落實的精修已併入上述各章列,彙整如下:

### 10.1 去重(現有章已教,新章不可重講)
- **§80**:§09 型別 + §44 Haskell 已教 ADT/列舉/Option/泛型/模式比對 → §80 不重教,改聚焦 trait 系統與 Result 的所有權視角。
- **§81**:§28–29 已教排序/BFS/DFS/DP 與各結構邏輯 → §81 不重講演算法,改「所有權視角重做實現」(Box/Rc/RefCell/Arc<Mutex>/unsafe/內建 vs 手寫權衡)。
- **§93**:須明講「CNN(§67)= 影像卷積,與 Transformer 文本處理不同」以免混淆;face embedding ≠ text embedding。

### 10.2 補前置/自帶(現有書沒有)
- **§79**:書中無專章講 C 指標/手動記憶體(§02 僅輕帶)→ §79 自帶「C 手動管理之痛」當所有權動機。
- **§86**:§48 只暗示 VT-x、無細節 → §86 補 VT-x/EPT/影子分頁/virtio。
- **§92**:§11 只講設計模式、§25 只講單點通訊 → §92 須自成完整分散式入門(Raft/CAP 不假設前置)。
- **§93/§94**:§38 缺 Softmax/tokenization/embedding/Transformer → 由 §93/§94 自帶(§38 的反向傳播/梯度下降/激活可複用)。

### 10.3 已挖出的互連點(現有章已有,連起來即可)
- **§54 線性代數已教餘弦相似度** → §96 RAG 直接 callout,不重講數學。
- **§24 OS 是樞紐**(行程/記憶體隔離、執行緒/鎖)→ §85/§86/§87 雙向連。
- **§43 並行(Python 視角)** → §82 Rust 無懼並行(safety 視角)互補。
- **§42 型別檢查** → §80 borrow checker。
- **§37 資料庫無向量搜尋** → §96 僅輕提「向量 vs 結構化」差異,不強連。
- callout 樣式比照 §24/§43 既有 🔑 關鍵概念框。

### 10.4 盤點發現的「現有書本身」可選補強(非本案範圍,記錄供日後)
- 書中無專章系統講「**C 指標與手動記憶體管理**」;目前由 §79 inline 處理足矣,日後若要可獨立補。
- 書中無專章講「**分散式系統**」;本案以 §92 一章覆蓋入門,日後若要可擴成獨立部。
