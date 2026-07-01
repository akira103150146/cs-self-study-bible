/* ==========================================================================
   CS 自學聖經 — 導覽引擎 / Navigation engine
   - 單一資料來源:章節清單 BOOK
   - 自動產生左側導覽、頁內目錄、上一章/下一章、進度條
   - 主題切換、程式碼複製、MathJax / highlight.js 載入
   ========================================================================== */

const BOOK = {
  title: "CS 自學聖經",
  parts: [
    {
      part: "序章 · Preface",
      icon: "✦",
      blurb: "為什麼學、怎麼學、如何使用這本書。",
      chapters: [
        { id: "00-about", num: "0", title: "如何使用本書與學習路線圖", en: "How to Use This Book", done: true },
      ],
    },
    {
      part: "第一部 · 計算機科學入門",
      icon: "🌱",
      blurb: "從零開始:計算是什麼?用 Python 寫出第一支程式。",
      chapters: [
        { id: "01-what-is-cs", num: "1", title: "什麼是計算、程式與演算法", en: "Computation, Programs & Algorithms", done: true },
        { id: "02-python-basics", num: "2", title: "Python 基礎與命令式程式設計", en: "Python & Imperative Programming", done: true },
        { id: "03-functions-recursion", num: "3", title: "函式、抽象與遞迴", en: "Functions, Abstraction & Recursion", done: true },
        { id: "04-data-structures-intro", num: "4", title: "基本資料結構與字串", en: "Built-in Data Structures", done: true },
        { id: "05-algorithmic-thinking", num: "5", title: "演算法思維、除錯與測試", en: "Algorithmic Thinking, Debugging & Testing", done: true },
      ],
    },
    {
      part: "第二部 · 程式設計核心",
      icon: "🧩",
      blurb: "函數式、系統化設計、物件導向、型別系統、設計模式與架構。",
      chapters: [
        { id: "06-functional-programming", num: "6", title: "函數式程式設計", en: "Functional Programming", done: true },
        { id: "07-design-recipe", num: "7", title: "系統化程式設計法", en: "Systematic Program Design", done: true },
        { id: "08-oop", num: "8", title: "物件導向設計", en: "Object-Oriented Design", done: true },
        { id: "09-types", num: "9", title: "靜態與動態型別系統", en: "Static & Dynamic Typing", done: true },
        { id: "10-design-patterns", num: "10", title: "設計模式與重構", en: "Design Patterns & Refactoring", done: true },
        { id: "11-software-architecture", num: "11", title: "軟體架構", en: "Software Architecture", done: true },
      ],
    },
    {
      part: "第三部 · 計算數學",
      icon: "📐",
      blurb: "微積分、離散數學、計數與機率、數論與圖論基礎。",
      chapters: [
        { id: "12-calculus", num: "12", title: "微積分精要", en: "Calculus for CS", done: true },
        { id: "13-discrete-math", num: "13", title: "離散數學:邏輯、證明與集合", en: "Discrete Math: Logic & Proofs", done: true },
        { id: "14-combinatorics-probability", num: "14", title: "計數、組合與離散機率", en: "Counting & Discrete Probability", done: true },
        { id: "15-number-theory-graphs", num: "15", title: "數論、圖論與遞迴關係", en: "Number Theory & Graph Theory", done: true },
      ],
    },
    {
      part: "第四部 · CS 工具",
      icon: "🛠️",
      blurb: "終端機、Shell、Vim、Git——專業開發者的日常兵器。",
      chapters: [
        { id: "16-shell", num: "16", title: "終端機與 Shell 指令稿", en: "Shell & Scripting", done: true },
        { id: "17-editors", num: "17", title: "Vim 與編輯器", en: "Vim & Editors", done: true },
        { id: "18-git", num: "18", title: "版本控制 Git", en: "Version Control with Git", done: true },
      ],
    },
    {
      part: "第五部 · 計算機系統",
      icon: "⚙️",
      blurb: "從一顆 NAND 閘到作業系統與網路:打造一台完整的電腦。",
      chapters: [
        { id: "19-boolean-logic", num: "19", title: "布林代數與邏輯閘", en: "Boolean Logic & Gates", done: true },
        { id: "20-combinational-sequential", num: "20", title: "組合邏輯、ALU 與記憶體", en: "ALU, Memory & Sequential Logic", done: true },
        { id: "21-cpu-machine-language", num: "21", title: "機器語言與 CPU 架構", en: "Machine Language & CPU", done: true },
        { id: "22-assembler", num: "22", title: "組譯器", en: "Assembler", done: true },
        { id: "23-vm-compiler", num: "23", title: "虛擬機與編譯器", en: "VM & Compiler", done: true },
        { id: "24-operating-system", num: "24", title: "作業系統:虛擬化、並行與持久化", en: "Operating Systems (OSTEP)", done: true },
        { id: "25-networking", num: "25", title: "計算機網路", en: "Computer Networking", done: true },
      ],
    },
    {
      part: "第六部 · 演算法與資料結構",
      icon: "🧠",
      blurb: "分治、排序、圖、貪婪、動態規劃,直到 NP 完備性。",
      chapters: [
        { id: "26-complexity", num: "26", title: "漸進複雜度與分析", en: "Asymptotic Analysis", done: true },
        { id: "27-divide-and-conquer", num: "27", title: "分治法與遞迴關係", en: "Divide & Conquer", done: true },
        { id: "28-sorting-searching", num: "28", title: "排序與搜尋", en: "Sorting & Searching", done: true },
        { id: "29-data-structures", num: "29", title: "進階資料結構", en: "Data Structures", done: true },
        { id: "30-graph-algorithms", num: "30", title: "圖演算法", en: "Graph Algorithms", done: true },
        { id: "31-greedy", num: "31", title: "貪婪演算法與最小生成樹", en: "Greedy Algorithms & MST", done: true },
        { id: "32-dynamic-programming", num: "32", title: "動態規劃", en: "Dynamic Programming", done: true },
        { id: "33-np-completeness", num: "33", title: "NP 完備性與計算難解", en: "NP-Completeness", done: true },
      ],
    },
    {
      part: "第七部 · 資訊安全",
      icon: "🔐",
      blurb: "CIA 三要素、密碼學、威脅模型與防禦性程式設計。",
      chapters: [
        { id: "34-security-fundamentals", num: "34", title: "資安基礎與威脅模型", en: "Security Fundamentals", done: true },
        { id: "35-cryptography", num: "35", title: "密碼學", en: "Cryptography", done: true },
        { id: "36-secure-coding", num: "36", title: "防禦性程式設計與漏洞辨識", en: "Secure Coding", done: true },
      ],
    },
    {
      part: "第八部 · 應用",
      icon: "🚀",
      blurb: "資料庫、機器學習、計算機圖學、軟體工程。",
      chapters: [
        { id: "37-databases", num: "37", title: "資料庫系統", en: "Databases", done: true },
        { id: "38-machine-learning", num: "38", title: "機器學習", en: "Machine Learning", done: true },
        { id: "39-computer-graphics", num: "39", title: "計算機圖學", en: "Computer Graphics", done: true },
        { id: "40-software-engineering", num: "40", title: "軟體工程", en: "Software Engineering", done: true },
      ],
    },
    {
      part: "第九部 · 倫理",
      icon: "⚖️",
      blurb: "技術的社會脈絡、專業倫理、智財與隱私。",
      chapters: [
        { id: "41-ethics", num: "41", title: "計算倫理、智財與隱私", en: "Ethics, IP & Privacy", done: true },
      ],
    },
    {
      part: "第十部 · 進階程式設計",
      icon: "🔬",
      blurb: "編譯器、平行運算、Haskell、Prolog、除錯與測試理論。",
      chapters: [
        { id: "42-compilers", num: "42", title: "編譯器原理", en: "Compilers", done: true },
        { id: "43-parallel", num: "43", title: "平行程式設計", en: "Parallel Programming", done: true },
        { id: "44-haskell", num: "44", title: "Haskell 與純函數式", en: "Haskell", done: true },
        { id: "45-prolog", num: "45", title: "邏輯程式設計 Prolog", en: "Logic Programming", done: true },
        { id: "46-debugging-testing", num: "46", title: "軟體除錯與測試理論", en: "Debugging & Testing Theory", done: true },
      ],
    },
    {
      part: "第十一部 · 進階系統",
      icon: "🏗️",
      blurb: "數位電路、CMOS、有限狀態機、快取、管線與虛擬記憶體。",
      chapters: [
        { id: "47-digital-circuits", num: "47", title: "數位電路與有限狀態機", en: "Digital Circuits & FSM", done: true },
        { id: "48-computer-architecture", num: "48", title: "計算機結構:快取與管線", en: "Computer Architecture", done: true },
      ],
    },
    {
      part: "第十二部 · 進階理論",
      icon: "🎓",
      blurb: "自動機、Turing 機、可計算性、計算幾何與賽局理論。",
      chapters: [
        { id: "49-theory-of-computation", num: "49", title: "計算理論", en: "Theory of Computation", done: true },
        { id: "50-computational-geometry", num: "50", title: "計算幾何", en: "Computational Geometry", done: true },
        { id: "51-game-theory", num: "51", title: "演算法賽局理論", en: "Algorithmic Game Theory", done: true },
      ],
    },
    {
      part: "第十三部 · 進階資安",
      icon: "🛡️",
      blurb: "Web 安全、數位鑑識、治理合規與安全開發生命週期。",
      chapters: [
        { id: "52-web-security", num: "52", title: "Web 安全", en: "Web Security", done: true },
        { id: "53-forensics-governance", num: "53", title: "數位鑑識與安全開發", en: "Forensics & Secure SDLC", done: true },
      ],
    },
    {
      part: "第十四部 · 進階數學",
      icon: "∑",
      blurb: "線性代數、數值方法、形式邏輯與機率論。",
      chapters: [
        { id: "54-linear-algebra", num: "54", title: "線性代數", en: "Linear Algebra", done: true },
        { id: "55-numerical-methods", num: "55", title: "數值方法", en: "Numerical Methods", done: true },
        { id: "56-formal-logic", num: "56", title: "形式邏輯", en: "Formal Logic", done: true },
        { id: "57-probability", num: "57", title: "機率論", en: "Probability", done: true },
      ],
    },
    {
      part: "第十五部 · 終極專案",
      icon: "🏆",
      blurb: "把所有知識整合成一個真實世界的作品。",
      chapters: [
        { id: "58-final-project", num: "58", title: "規劃與完成畢業專案", en: "The Final Project", done: true },
      ],
    },
    {
      part: "第十六部 · 競賽程式設計與 APCS",
      icon: "🥇",
      blurb: "專修軌道:用 C++/STL 與經典題型,打進 APCS、TOI 與程式競賽。",
      chapters: [
        { id: "59-cpp-stl", num: "59", title: "C++ 與 STL:競賽程式入門", en: "C++ & STL for Competitive", done: true },
        { id: "60-competitive-techniques", num: "60", title: "競賽必備技巧:前綴和、差分、二分搜答案", en: "Prefix Sums, Diff & Binary Search", done: true },
        { id: "61-competitive-ds", num: "61", title: "競賽資料結構:單調隊列、BIT、線段樹", en: "Competitive Data Structures", done: true },
        { id: "62-competitive-paradigms", num: "62", title: "競賽範式:暴搜、分治、貪心、DP 實戰", en: "Competitive Paradigms", done: true },
        { id: "63-graph-tree-advanced", num: "63", title: "圖論與樹上演算法", en: "Graph & Tree Algorithms", done: true },
        { id: "64-apcs-toi", num: "64", title: "APCS 與 TOI 實戰題庫", en: "APCS & TOI Problem Sets", done: true },
      ],
    },
    {
      part: "第十七部 · 電腦視覺與影像辨識",
      icon: "👁️",
      blurb: "專修軌道:從像素到 CNN、YOLO 與 AR——成果驅動的電腦視覺。",
      chapters: [
        { id: "65-cv-basics-processing", num: "65", title: "影像即資料與影像處理", en: "Image as Data & Processing", done: true },
        { id: "66-cv-features-classic", num: "66", title: "特徵與傳統視覺", en: "Features & Classic Vision", done: true },
        { id: "67-cv-deep-learning", num: "67", title: "深度學習視覺:CNN、YOLO、分割", en: "Deep Learning Vision", done: true },
        { id: "68-cv-graphics-ar", num: "68", title: "電腦圖學、3D 與擴增實境", en: "Graphics, 3D & AR", done: true },
      ],
    },
    {
      part: "第十八部 · 實戰資安 CTF",
      icon: "🚩",
      blurb: "專修軌道:從終端機尋寶到 Pwn 與自辦 CTF——動手做的攻防實戰。",
      chapters: [
        { id: "69-ctf-foundations", num: "69", title: "駭客工作台、終端機尋寶與編碼", en: "CTF Foundations & Encoding", done: true },
        { id: "70-ctf-crypto", num: "70", title: "古典與現代密碼破譯", en: "Classic & Modern Crypto Cracking", done: true },
        { id: "71-ctf-web-network-forensics", num: "71", title: "Web 攻防、封包分析與檔案鑑識", en: "Web, Packets & Forensics", done: true },
        { id: "72-ctf-pwn-reverse", num: "72", title: "逆向工程與二進位攻防", en: "Reverse Engineering & Pwn", done: true },
        { id: "73-ctf-compete", num: "73", title: "自動化、參賽與自辦 CTF", en: "Automation & Running a CTF", done: true },
      ],
    },
    {
      part: "第十九部 · SICP:抽象的建構",
      icon: "λ",
      blurb: "從序對到自我直譯器——用 Scheme 重走經典《SICP》,看抽象如何層層長出一台會思考的機器。",
      chapters: [
        { id: "80-sicp-scheme", num: "74", title: "Scheme 導引與程序抽象", en: "Scheme & Procedural Abstraction", done: true },
        { id: "81-sicp-data", num: "75", title: "用資料建立抽象:從抽象屏障到資料導向", en: "Building Abstractions with Data", done: true },
        { id: "82-sicp-state-streams", num: "76", title: "狀態、環境模型與串流", en: "State, Environments & Streams", done: true },
        { id: "83-sicp-metacircular", num: "77", title: "後設循環直譯器:用 Lisp 寫 Lisp", en: "The Metacircular Evaluator", done: true },
        { id: "84-sicp-register-machines", num: "78", title: "暫存器機器與顯式控制求值器", en: "Register Machines & EC-Evaluator", done: true },
      ],
    },
    {
      part: "第二十部 · Rust 系統程式設計",
      icon: "🦀",
      blurb: "從所有權到無懼並行,再到親手寫一顆會開機的核心——用一門「編譯器當你導師」的語言,重新理解記憶體、型別與系統。",
      chapters: [
        { id: "85-rust-ownership", num: "79", title: "所有權、借用與生命週期", en: "Ownership, Borrowing & Lifetimes", done: true },
        { id: "86-rust-types-errors", num: "80", title: "型別、trait、列舉與錯誤處理", en: "Types, Traits & Error Handling", done: true },
        { id: "87-rust-collections-ds", num: "81", title: "集合、迭代器與所有權視角的資料結構", en: "Collections & Ownership-Aware Data Structures", done: true },
        { id: "88-rust-concurrency", num: "82", title: "無懼並行與非同步", en: "Fearless Concurrency & Async", done: true },
        { id: "89-rust-project", num: "83", title: "Rust 實戰:CLI 工具與最小服務", en: "Building a CLI & Service in Rust", done: true },
        { id: "90-rust-os-kernel", num: "84", title: "用 Rust 手寫迷你作業系統核心", en: "A Minimal OS Kernel in Rust", done: true },
      ],
    },
    {
      part: "第二一部 · 容器、虛擬化與雲原生底層",
      icon: "📦",
      blurb: "一個程式如何「以為自己獨佔整台電腦」?從 chroot、namespaces、cgroups 到 hypervisor,再到 eBPF 與分散式——拆開魔法,還親手拼一個出來。",
      chapters: [
        { id: "91-virt-landscape", num: "85", title: "虛擬化全景:行程隔離→VM→容器", en: "The Virtualization Landscape", done: true },
        { id: "92-vm-hypervisor", num: "86", title: "虛擬機與 Hypervisor 底層", en: "Virtual Machines & Hypervisors", done: true },
        { id: "93-container-internals", num: "87", title: "容器的真相:namespaces / cgroups / OverlayFS", en: "How Containers Really Work", done: true },
        { id: "94-mini-docker", num: "88", title: "手寫迷你 Docker", en: "Build Your Own Mini Docker", done: true },
        { id: "95-docker-practice", num: "89", title: "Docker 實戰:映像、網路、Compose", en: "Docker in Practice", done: true },
        { id: "96-kubernetes", num: "90", title: "Kubernetes 編排與雲原生", en: "Kubernetes & Cloud Native", done: true },
        { id: "97-ebpf", num: "91", title: "eBPF:核心可程式化(觀測 / 網路 / 安全)", en: "eBPF: Programmable Kernel", done: true },
        { id: "98-distributed-systems", num: "92", title: "分散式系統與高可用架構", en: "Distributed Systems & High Availability", done: true },
      ],
    },
    {
      part: "第二二部 · 動手打造 LLM Agent",
      icon: "🤖",
      blurb: "不靠魔法框架,一步一步手刻——從會呼叫工具的迴圈,到能檢索、能用 MCP、會協作的自主 agent。",
      chapters: [
        { id: "99-gpt-from-scratch", num: "93", title: "從零打造 GPT(選修):看懂 agent 在跟誰說話", en: "Build GPT From Scratch (Optional)", done: true },
        { id: "100-llm-client", num: "94", title: "手刻你的 LLM client", en: "Hand-Building Your LLM Client", done: true },
        { id: "101-tool-react", num: "95", title: "工具呼叫與 ReAct", en: "Tool Calling & the ReAct Loop", done: true },
        { id: "102-rag-from-scratch", num: "96", title: "手刻最小 RAG", en: "Building Minimal RAG", done: true },
        { id: "103-mcp", num: "97", title: "MCP:可插拔的標準服務", en: "MCP: Pluggable Tools & Resources", done: true },
        { id: "104-agent-advanced", num: "98", title: "進階單代理:規劃、反思、自我改進", en: "Advanced Single-Agent Patterns", done: true },
        { id: "105-multi-agent", num: "99", title: "多代理協作系統", en: "Multi-Agent Systems", done: true },
        { id: "106-agent-production", num: "100", title: "從玩具到生產:框架、評估、可觀測性、部署", en: "From Toy to Production", done: true },
      ],
    },
    {
      part: "第二三部 · 進階補充:位元、資訊與最佳化",
      icon: "🔢",
      blurb: "整數有二補數,浮點呢?資訊的極限在哪?最佳化怎麼收成一門?補齊三塊承重的底層。",
      chapters: [
        { id: "107-floating-point", num: "101", title: "浮點數與 IEEE 754", en: "Floating Point & IEEE 754", done: true },
        { id: "108-information-theory", num: "102", title: "資訊理論與資料壓縮", en: "Information Theory & Compression", done: true },
        { id: "109-optimization", num: "103", title: "最佳化:線性規劃與凸優化", en: "Optimization: LP & Convex", done: true },
      ],
    },
    {
      part: "第二四部 · 進階人工智慧",
      icon: "🧠",
      blurb: "從符號 AI 的搜尋與規劃,到深度學習的數學、強化學習、生成式擴散模型,再到 AI 安全與高效部署。",
      chapters: [
        { id: "110-classical-ai", num: "104", title: "傳統/符號 AI:搜尋、CSP、規劃與知識表示", en: "Classical AI: Search, CSP & Planning", done: true },
        { id: "111-deep-learning-math", num: "105", title: "深度學習的數學", en: "The Math of Deep Learning", done: true },
        { id: "112-reinforcement-learning", num: "106", title: "強化學習與 RLHF", en: "Reinforcement Learning & RLHF", done: true },
        { id: "113-ai-security", num: "107", title: "AI/LLM 安全與紅隊", en: "AI/LLM Security & Red-Teaming", done: true },
        { id: "114-generative-ai", num: "108", title: "生成式 AI:擴散模型與多模態", en: "Generative AI: Diffusion & Multimodal", done: true },
        { id: "115-efficient-ml", num: "109", title: "高效 ML:量化、蒸餾、微調與部署", en: "Efficient ML: Quantization & Deployment", done: true },
      ],
    },
    {
      part: "第二五部 · 進階電腦圖學",
      icon: "🎨",
      blurb: "從經驗式 Phong 到物理正確的照片級渲染——渲染方程式、路徑追蹤,以及親手寫 GPU 著色器。",
      chapters: [
        { id: "116-pbr-path-tracing", num: "110", title: "物理渲染 PBR 與路徑追蹤", en: "Physically-Based Rendering & Path Tracing", done: true },
        { id: "117-gpu-shaders", num: "111", title: "GPU 著色器實作(GLSL)", en: "GPU Shaders (GLSL)", done: true },
      ],
    },
    {
      part: "第二六部 · 高效能運算、GPU 與 WASM",
      icon: "⚡",
      blurb: "現代運算的引擎:用 CUDA 手寫 GPU kernel、設計高效能平行演算法,並用 WebAssembly 讓程式跑在任何地方。",
      chapters: [
        { id: "118-cuda-gpu", num: "112", title: "GPU 架構與 CUDA 程式設計", en: "GPU Architecture & CUDA", done: true },
        { id: "119-parallel-algorithms", num: "113", title: "高效能平行演算法", en: "High-Performance Parallel Algorithms", done: true },
        { id: "120-wasm", num: "114", title: "WebAssembly(WASM/WASI)", en: "WebAssembly", done: true },
      ],
    },
    {
      part: "第二七部 · 動手實戰專案",
      icon: "🛠️",
      blurb: "把整本書學到的東西組裝起來:八個從零打造、整合多個章節的大型專案。",
      chapters: [
        { id: "121-capstone-os", num: "115", title: "實戰:手寫教學作業系統", en: "Capstone: Build a Teaching OS", done: true },
        { id: "122-capstone-database", num: "116", title: "實戰:自製關聯式資料庫", en: "Capstone: Build a Database", done: true },
        { id: "123-capstone-compiler", num: "117", title: "實戰:寫一個編譯器", en: "Capstone: Build a Compiler", done: true },
        { id: "124-capstone-container", num: "118", title: "實戰:手寫容器執行時", en: "Capstone: Build a Container Runtime", done: true },
        { id: "125-capstone-llm-agent", num: "119", title: "實戰:打造 LLM Agent 產品", en: "Capstone: Build an LLM Agent Product", done: true },
        { id: "126-capstone-search-engine", num: "120", title: "實戰:打造搜尋引擎", en: "Capstone: Build a Search Engine", done: true },
        { id: "127-capstone-renderer", num: "121", title: "實戰:物理渲染器", en: "Capstone: Build a Path Tracer", done: true },
        { id: "128-capstone-raft-kv", num: "122", title: "實戰:分散式 KV 與 Raft", en: "Capstone: Distributed KV with Raft", done: true },
      ],
    },
    {
      part: "附錄 · 完整題庫",
      icon: "📚",
      blurb: "依章節收錄 AP325、APCS、TOI 全部題目與解答,當你的刷題地圖。",
      chapters: [
        { id: "74-bank-ap325", num: "附A", title: "AP325 完整題單(依章)", en: "AP325 Problem List", done: true },
        { id: "75-bank-apcs-concept", num: "附B", title: "APCS 觀念題題庫(125 題)", en: "APCS Concept Questions", done: true },
        { id: "76-bank-apcs-impl-1", num: "附C", title: "APCS 實作題題庫(上)第 1–6 章", en: "APCS Implementation I", done: true },
        { id: "77-bank-apcs-impl-2", num: "附D", title: "APCS 實作題題庫(下)第 7–11 章", en: "APCS Implementation II", done: true },
        { id: "78-bank-apcs-mock", num: "附E", title: "APCS 模擬考卷(3 卷)", en: "APCS Mock Exams", done: true },
        { id: "79-bank-toi", num: "附F", title: "TOI 題庫(337 題,全文)", en: "TOI Problem Bank", done: true },
      ],
    },
  ],
};

// 攤平成線性章節序列(供上一章/下一章使用)
BOOK.flat = BOOK.parts.flatMap(p => p.chapters.map(c => ({ ...c, partTitle: p.part })));

/* ---------- 工具 ---------- */
function el(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  }
  for (const kid of kids) if (kid != null) e.append(kid.nodeType ? kid : document.createTextNode(kid));
  return e;
}
function currentId() {
  const m = location.pathname.match(/([^/\\]+)\.html$/);
  return m ? m[1] : "index";
}
const REL = () => (currentId() === "index" || location.pathname.endsWith("/")) ? "" : "";

/* ---------- 主題 ---------- */
function initTheme() {
  const saved = localStorage.getItem("cs-theme");
  const sys = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  document.documentElement.dataset.theme = saved || sys;
}
function toggleTheme() {
  const cur = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = cur;
  localStorage.setItem("cs-theme", cur);
  const b = document.getElementById("theme-icon"); if (b) b.textContent = cur === "dark" ? "☀️" : "🌙";
  // 同步切換 highlight.js 的配色主題
  const hl = document.getElementById("hljs-theme");
  if (hl) hl.href = HLJS_BASE + "styles/" + (cur === "dark" ? "atom-one-dark" : "atom-one-light") + ".min.css";
}

/* CDN 基底(集中管理,順便給 <link rel=preconnect> 用) */
const HLJS_BASE = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/";
const MJ_URL = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js";

/* ---------- 頂部列 ---------- */
function buildTopbar(prefix, hasSidebar) {
  const dark = document.documentElement.dataset.theme === "dark";
  const bar = el("div", { class: "topbar" },
    hasSidebar ? el("button", { class: "icon-btn menu-toggle", "aria-label": "選單", onclick: toggleSidebar }, "☰") : null,
    el("a", { class: "brand", href: prefix + "index.html" },
      el("span", { class: "logo" }, "CS"),
      el("span", {}, "CS 自學聖經")),
    el("span", { class: "spacer" }),
    el("button", { class: "icon-btn", "aria-label": "切換主題", onclick: toggleTheme, title: "切換深淺色" },
      el("span", { id: "theme-icon" }, dark ? "☀️" : "🌙")),
  );
  document.body.prepend(bar);
  document.body.prepend(el("div", { id: "progress-bar" }));
}

/* ---------- 左側導覽 ---------- */
function buildSidebar(prefix) {
  const cur = currentId();
  const nav = el("nav", { class: "sidebar", id: "sidebar" });
  for (const part of BOOK.parts) {
    nav.append(el("div", { class: "part-title" }, part.part));
    for (const c of part.chapters) {
      const href = c.done ? prefix + "chapters/" + c.id + ".html" : "javascript:void(0)";
      const a = el("a", {
        class: "nav-link" + (c.id === cur ? " active" : "") + (c.done ? "" : " todo"),
        href,
        title: c.en,
      }, el("span", { class: "ch-num" }, c.num), c.title);
      if (!c.done) { a.style.opacity = ".5"; a.title = "撰寫中 / Coming soon"; }
      nav.append(a);
    }
  }
  document.querySelector(".layout").prepend(nav);
  document.querySelector(".layout").prepend(el("div", { class: "sidebar-backdrop", id: "backdrop", onclick: toggleSidebar }));
}
function toggleSidebar() {
  document.getElementById("sidebar")?.classList.toggle("open");
  document.getElementById("backdrop")?.classList.toggle("show");
}

/* ---------- 右側頁內目錄 ---------- */
function buildTOC() {
  const content = document.querySelector(".content");
  if (!content) return;
  const heads = content.querySelectorAll("h2, h3");
  if (heads.length < 2) return;
  const toc = el("aside", { class: "toc" }, el("div", { class: "toc-title" }, "本章導覽"));
  heads.forEach((h, i) => {
    if (!h.id) h.id = "sec-" + i;
    toc.append(el("a", { href: "#" + h.id, class: h.tagName === "H3" ? "h3" : "" }, h.textContent));
  });
  document.querySelector(".layout").append(toc);

  const links = [...toc.querySelectorAll("a")];
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        links.forEach(l => l.classList.toggle("active", l.getAttribute("href") === "#" + en.target.id));
      }
    });
  }, { rootMargin: "-80px 0px -70% 0px" });
  heads.forEach(h => obs.observe(h));
}

/* ---------- 上一章 / 下一章 ---------- */
function buildPager(prefix) {
  const cur = currentId();
  const idx = BOOK.flat.findIndex(c => c.id === cur);
  if (idx < 0) return;
  const content = document.querySelector(".content");
  const pager = el("div", { class: "pager" });
  const prev = BOOK.flat.slice(0, idx).reverse().find(c => c.done);
  const next = BOOK.flat.slice(idx + 1).find(c => c.done);
  if (prev) pager.append(el("a", { href: prefix + "chapters/" + prev.id + ".html", class: "prev" },
    el("div", { class: "dir" }, "← 上一章"), el("div", { class: "ttl" }, prev.title)));
  else pager.append(el("a", { href: prefix + "index.html", class: "prev" },
    el("div", { class: "dir" }, "← 回到"), el("div", { class: "ttl" }, "首頁目錄")));
  if (next) pager.append(el("a", { href: prefix + "chapters/" + next.id + ".html", class: "next" },
    el("div", { class: "dir" }, "下一章 →"), el("div", { class: "ttl" }, next.title)));
  content.append(pager);
}

/* ---------- 進度條(rAF 節流 + 快取高度,避免每次捲動觸發版面重算) ---------- */
function initProgress() {
  const bar = document.getElementById("progress-bar");
  if (!bar) return;
  const h = document.documentElement;
  let max = 1, ticking = false;
  const recalc = () => { max = h.scrollHeight - h.clientHeight; };
  const paint = () => {
    bar.style.width = (max > 0 ? Math.min(h.scrollTop / max, 1) * 100 : 0) + "%";
    ticking = false;
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(paint); } };
  recalc();
  document.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", () => { recalc(); paint(); }, { passive: true });
  // 內容高度變動(TOI 卡片重繪、details 展開)時重新量測,但不在捲動熱路徑上
  if (window.ResizeObserver) new ResizeObserver(() => { recalc(); }).observe(document.body);
  paint();
}

/* ---------- 程式碼複製(委派事件,可重複套用到動態新增的 pre) ---------- */
function addCopyButtons(scope) {
  (scope || document).querySelectorAll("pre").forEach(pre => {
    if (pre.closest(".content, .toi-card") && !pre.querySelector(".copy-btn"))
      pre.append(el("button", { class: "copy-btn" }, "複製"));
  });
}
function initCopyButtons() {
  addCopyButtons(document);
  window.csAddCopy = addCopyButtons;
  document.addEventListener("click", (e) => {
    const btn = e.target.closest && e.target.closest(".copy-btn");
    if (!btn) return;
    const pre = btn.closest("pre"); if (!pre) return;
    const code = pre.querySelector("code") || pre;
    navigator.clipboard.writeText(code.innerText).then(() => {
      btn.textContent = "已複製 ✓";
      setTimeout(() => (btn.textContent = "複製"), 1600);
    });
  });
}

/* ---------- highlight.js:延遲上色(只在進入視窗 / 展開 details 時處理) ----------
   長頁面(題庫上百段、TOI 300+ 段 C++)不再於載入時一次上色全部,大幅縮短首次互動時間。 */
function loadHighlight() {
  if (!document.querySelector(".content pre code, .toi-card pre code")) return;
  const dark = document.documentElement.dataset.theme === "dark";
  document.head.append(el("link", { rel: "stylesheet", id: "hljs-theme",
    href: HLJS_BASE + "styles/" + (dark ? "atom-one-dark" : "atom-one-light") + ".min.css" }));
  const s = el("script", { src: HLJS_BASE + "highlight.min.js" });
  s.onload = () => {
    const hl = (code) => {
      if (!code || code.dataset.hl || !window.hljs) return;
      code.dataset.hl = "1";
      window.hljs.highlightElement(code);
    };
    const io = new IntersectionObserver((ents) => {
      ents.forEach(e => { if (e.isIntersecting) { hl(e.target); io.unobserve(e.target); } });
    }, { rootMargin: "300px" });
    const observeAll = (scope) => (scope || document).querySelectorAll("pre code").forEach(c => io.observe(c));
    observeAll(document);
    window.csObserveHL = observeAll;
    // 摺疊在 details 內的程式碼:展開時才上色(收合時不可見,不會被 IO 觸發)
    document.addEventListener("toggle", (e) => {
      if (e.target.tagName === "DETAILS" && e.target.open)
        e.target.querySelectorAll("pre code").forEach(hl);
    }, true);
  };
  document.head.append(s);
}

/* ---------- MathJax:一般頁面整頁排版;TOI 題庫頁因公式量大改為延遲(逐卡進視窗才排版) ---------- */
function loadMathJax() {
  const txt = document.body.textContent;
  if (txt.indexOf("$") < 0 && txt.indexOf("\\(") < 0 && txt.indexOf("\\[") < 0) return;
  const lazy = !!document.getElementById("toi-app");
  window.MathJax = {
    tex: { inlineMath: [["$", "$"], ["\\(", "\\)"]], displayMath: [["$$", "$$"], ["\\[", "\\]"]] },
    options: { skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"], enableMenu: false },
    startup: { typeset: !lazy },
  };
  const s = el("script", { src: MJ_URL, async: "" });
  if (lazy) s.onload = () => {
    window.MathJax.startup.promise.then(() => {
      const done = new WeakSet();
      const ts = (node) => { if (node && !done.has(node)) { done.add(node); window.MathJax.typesetPromise([node]).catch(() => {}); } };
      const io = new IntersectionObserver((ents) => {
        ents.forEach(e => { if (e.isIntersecting) { ts(e.target); io.unobserve(e.target); } });
      }, { rootMargin: "400px" });
      const observe = (nodes) => nodes.forEach(n => io.observe(n));
      window.csObserveMath = observe;
      observe(document.querySelectorAll(".content > *:not(#toi-app), #toi-app .toi-card"));
    });
  };
  document.head.append(s);
}

/* ---------- 啟動 ---------- */
function boot() {
  initTheme();
  const onChapter = !!document.querySelector(".layout .content");
  const prefix = location.pathname.includes("/chapters/") ? "../" : "";
  buildTopbar(prefix, onChapter);
  if (onChapter) {
    buildSidebar(prefix);
    buildTOC();
    buildPager(prefix);
  }
  initProgress();
  initCopyButtons();
  loadHighlight();
  loadMathJax();
}
document.addEventListener("DOMContentLoaded", boot);
