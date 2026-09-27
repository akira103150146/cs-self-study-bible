# 計算機概論 課程設計 · 資工系大學部

**日期**:2026-09-27
**狀態**:方向(兩條主線 + 各章起始碼)、每章模組結構、18 章實作內容已確認;檔案佈局、環境、閘門、分批為預設值,待使用者審 spec 時確認
**範圍**:Dale & Lewis《Computer Science Illuminated》7e 全書 18 章,**每章做成獨立完整的模組,不做取捨**;老師自行挑章、排週次。

---

## 1. 教材來源

Nell Dale & John Lewis,*Computer Science Illuminated*,7th Edition(Jones & Bartlett),約 680 頁。

- 手上只有 **62 頁試閱版**:`C:\Users\Akira\Downloads\電子檔-20260922T043601Z-1-001\大學的書電子檔\計算機概論\計算機概論 英.pdf`
  (目錄在 PDF p8–20、第 1 章內文到書頁 29;掃描圖,無文字層)。
- **決定:只用目錄當大綱,講解與題目全部自編**(使用者 2026-09-27)。課本是參考書,教材不引用原題、不標原書頁碼。
- 全書架構是「洋蔥分層」:Information → Hardware → Programming → Operating Systems → Applications → Communications,
  前後各一章總論(第 1 章 The Big Picture、第 18 章 Limitations of Computing)。

---

## 2. 已確認的前提

| 項目 | 決定 |
|---|---|
| 學生 | **大學資工系學生**。數學課的「高職背景」前提**不套用**到計概 |
| 程式基礎 | **已具備**(老師自行確保)。計概不教語法,C/C++ 與 Python 直接當工具 |
| 目標 | 練習紮實、**銜接後續必修**、符合現代需求、盡可能打穩基礎 |
| 範圍 | 18 章全做,老師自己挑 |
| 練習方式 | 每章先做**重要/必考觀念的筆試練習**,再做**紮實的實作/專案** |
| 專案要求 | **完全涵蓋該章教學觀念**,並**盡量延伸**;題數、任務數不設上限 |
| 語言分工 | 以「要不要看見機器內部」決定:位元、記憶體、指標、系統呼叫、效能 → **C/C++**;應用、資料、實驗、出圖 → **Python** |

---

## 3. 主線:兩條主線 + 每章起始碼(方案 C)

- **系統主線(C/C++)**:第 1–11、18 章。從位元一路往上蓋,終點是「自訂語言 → 自寫組譯器 → 自寫 CPU 模擬器上執行」。
- **應用主線(Python)**:第 12–17 章。資料庫、AI、模擬與圖學、網路、Web、資安。
- **每章的起始碼內含前面各章的參考解**,跳過任何一章都接得上;學生做過前面的章,也可以換成自己的版本。
- 每章分**核心 Lab**(必做,完全涵蓋觀念,附自動測試)與**延伸專案**(選做,盡量延伸,可累積成期末專題)。

否決的方案:A(每章獨立、互不相關)看不到分層、做不大;B(單一貫穿專案)跳一章就斷,和「老師自己挑章」衝突。

### 3.1 教學用 ISA:CSI-16

系統主線第 4–6、9、10 章共用一個自訂指令集 **CSI-16**。設計參考書上第 6 章的 Pep/9(16 位元、累加器架構、直接/立即定址、記憶體對映 I/O),但**精簡到學生一章寫得完**:

- 16 位元字組、64 KiB 位元組定址記憶體、累加器 `A` + 索引暫存器 `X` + `PC` + `SP` + 旗標 N Z V C
- 約 24 個指令:載入/儲存、加減、AND/OR/NOT、移位、比較、條件與無條件分支、`CALL`/`RET`、`PUSH`/`POP`、`STOP`
- 定址模式:立即、直接、索引、堆疊相對
- I/O:兩個記憶體對映位址(字元輸入、字元輸出)

完整規格在 Batch 2 寫成 `labs/common/csi16-spec.md`,是第 5、6、9、10 章的共同依據。課堂上可以拿它和書上的 Pep/9 對照。

---

## 4. 每章模組的組成

| 交付物 | 內容 | 學生版/教師版 |
|---|---|---|
| **① 觀念講義** | 只挑重要/必考觀念。每個觀念走「觀念 → 講解(圖、例題)→ 隨堂練習」三步;結尾一行「**後面哪門必修會再用到**」與「**Lab 會用到**」 | 學生版無答案;教師版附答案、易錯點、教學備註 |
| **② 筆試題庫** | 每個觀念都要有足夠的題目,題數不設上限。題型:**計算/追蹤約 50%、觀念選擇約 30%(錯誤選項對應迷思)、簡答/比較約 20%** | 教師版附詳解 |
| **③ 核心 Lab** | 規格書 + 起始碼 + 公開測試;**每個任務標出它涵蓋的觀念 ID** | 教師版另有參考解、隱藏測試 |
| **④ 延伸專案** | 往深處與現代應用延伸,數量不限;每個附評分規準 | 同上 |

### 4.1 觀念 ID 與涵蓋度

每章的觀念編號為 `C{章}.{序}`(例如 `C3.4` = IEEE 754 浮點表示)。講義、題庫、Lab 任務、測試全部用同一套 ID 標註。
**涵蓋度閘門**:每個觀念至少要有 1 個筆試題、1 個核心 Lab 任務、1 個測試;少一個就不算完成。

### 4.2 題庫與組卷

題目不寫成固定考卷,每題帶 `chapter / concept / type / difficulty / points` 標籤。
`build_exam.py --chapters 2,3,5` 依老師選的章節與配分自動組出期中、期末的 A/B 兩版(考卷版 + 詳解版;沿用「對應第 N 章只印詳解版」)。

### 4.3 語言規則

中文敘述;**術語、觀念名、程式識別字用英文**,第一次出現附中文對照(例如 two's complement 二補數)。圖表標籤用英文。

---

## 5. 各章內容

「觀念重點」是筆試的必考範圍。「現代補充」是書上沒有或已過時、本課補進或替換的部分。

### 5.1 系統主線(C/C++)

| 章 | 觀念重點(筆試) | 核心 Lab | 延伸專案 | 現代補充 | 銜接必修 |
|---|---|---|---|---|---|
| 1 The Big Picture | 系統分層、抽象、硬體/軟體世代、計算作為工具與學科 | **開發環境**:Linux(Docker/WSL)、git、gcc、make、gdb;同一支程式寫成 C 與 Python,用 `objdump`、`gcc -S` 逐層往下看 | 用 `strace`/`ltrace` 畫出一支程式穿過的所有層 | 容器、雲端、AI 輔助寫程式與驗證 | 全部 |
| 2 Binary Values | 位值記數、2/8/16 進位互轉、各進位運算、2 的冪次進位 | **`baseconv`**:2–36 進位互轉與四則運算,只准用位元運算與自寫的字串處理 | 任意精度整數函式庫(加減乘、十進位輸出) | — | 計算機組織 |
| 3 Data Representation | 符號大小/一補數/二補數、溢位、定點與浮點(IEEE 754)、ASCII/Unicode/UTF-8、RLE/Huffman/關鍵字壓縮、取樣與量化、RGB 與色深、點陣/向量圖、影片編碼 | **`floatdump`**(含 denormal、±Inf、NaN)、溢位偵測、endianness、UTF-8 編解碼、**`hzip` Huffman 壓縮器**(位元層級 I/O,可實際壓縮檔案)、BMP 讀寫與影像處理、WAV 產生與量化失真 | LZ77、影格 delta 編碼、點陣轉 SVG 描邊 | UTF-8 與 emoji、現代影音編碼概念 | 計算機組織、演算法 |
| 4 Gates and Circuits | 各種閘與真值表、布林式、電晶體概念、組合電路、半加/全加器、多工器、latch/flip-flop、IC | **只用 NAND 蓋出一切**:所有閘 → 全加器 → 16 位元 ALU(含 NZVC)→ 時脈模擬 SR latch、D flip-flop、暫存器 | 讀 netlist 文字檔的通用電路模擬器;選做 Verilog 對照 | — | 數位邏輯、計算機組織 |
| 5 Computing Components | von Neumann 架構、fetch-execute 週期、RAM/ROM、次級儲存、觸控、嵌入式、平行架構分類 | **CSI-16 CPU 模擬器**:fetch-decode-execute、記憶體對映 I/O、追蹤模式;**pthread 平行加總**並用 Amdahl 定律驗證加速比 | cache 模擬器(命中率實驗)、RISC-V RV32I 子集模擬器 | 記憶體階層與 cache、多核心、GPU、RISC-V | 計算機組織 |
| 6 Low-Level Languages | 機器語言、組合語言、組譯、虛擬碼、測試 | **CSI-16 兩階段組譯器**(符號表、錯誤訊息)與反組譯器;用 CSI-16 組語寫迴圈、陣列、乘法;閱讀 `gcc -S` 的輸出 | 巨集、呼叫慣例與堆疊框架 | x86-64/RISC-V 實機組語閱讀 | 系統程式、計算機組織 |
| 7 Problem Solving and Algorithms | 解題策略、選擇與重複、陣列與記錄、循序/二分搜尋、選擇/泡沫/插入/快速排序、遞迴 | C 手刻全部搜尋與排序(**函式指標泛型化**、計比較次數),Python 畫實測時間 vs 理論曲線 | merge sort、隨機化 pivot、對抗最壞情況的輸入 | — | 資料結構、演算法 |
| 8 ADTs and Subprograms | ADT、stack、queue、list、二元樹與 BST、圖與走訪、傳值/傳參考 | **`libds`**:stack、queue(環狀陣列版與鏈結版)、list、BST(含刪除)、graph(BFS、DFS、Dijkstra),**Valgrind 零洩漏**;應用:括號匹配、後序式求值、迷宮最短路徑 | AVL 樹、hash table | — | 資料結構 |
| 9 OOD and High-Level Languages | 物件導向設計、編譯/直譯、典範、布林運算式、型別、I/O、控制結構、封裝/繼承/多型、程序式與物件導向比較 | **小語言直譯器**:tokenizer → 遞迴下降 parser → AST → 執行;AST 用 **C++ 類別階層 + virtual** 實作 | **把小語言編譯成 CSI-16 組語,在第 5 章的 CPU 上執行**(系統主線在此接通) | 型別推論、現代語言特性概覽 | 編譯器、物件導向 |
| 10 Operating Systems | OS 角色、批次與分時、記憶體管理(連續/分割/分頁)、行程狀態與 PCB、CPU 排程(FCFS、SJN、RR) | **排程模擬器**(甘特圖、等待/周轉時間)、**分頁模擬器**(位址轉換、FIFO/LRU 置換)、`fork`/`exec`/`wait` **迷你 shell** | 管線與重導向、在 CSI-16 上做時間片多工 | 虛擬化與容器、thread | 作業系統 |
| 11 File Systems | 文字/二進位檔、檔案類型與操作、存取方式、保護、目錄樹、路徑、磁碟排程(FCFS、SSTF、SCAN) | **磁碟映像檔上的簡易檔案系統**(目錄樹、路徑解析、配置表、權限位元)、磁碟排程模擬、用系統呼叫自寫 `ls -l` 與 `find` | journaling 與當機復原 | SSD 與 FTL 概念 | 作業系統 |
| 18 Limitations of Computing | 算術極限、元件與通訊極限、軟體複雜度與品質、Big-O、圖靈機、停機問題、P/NP | 浮點誤差累積 vs Kahan summation、整數溢位漏洞重現、**圖靈機模擬器**、停機問題對角化的程式示範、指數時間 vs DP 實驗 | 用 SAT/子集和說明「驗證容易、求解困難」 | 知名軟體事故案例 | 演算法、計算理論 |

### 5.2 應用主線(Python)

| 章 | 觀念重點(筆試) | 核心 Lab | 延伸專案 | 現代補充 | 銜接必修 |
|---|---|---|---|---|---|
| 12 Information Systems | 試算表公式與循環參照、關聯式模型、關聯、SQL、資料庫設計、電子商務、大數據 | **試算表引擎**(公式解析、相依圖、**拓樸排序偵測循環參照**);SQLite 正規化 schema 與 SQL 查詢;pandas 資料分析 | 迷你關聯式引擎(select、project、join) | NoSQL 概念、資料管線 | 資料庫 |
| 13 Artificial Intelligence | 圖靈測試、知識表示、語意網路、搜尋樹、專家系統、類神經網路、NLP、機器人 | BFS/A* 解 8-puzzle、語意網路推論、規則式專家系統、**NumPy 手刻神經網路訓練 MNIST**、n-gram 文字生成、格子世界 sense-plan-act | embedding 與 LLM API;如何驗證 LLM 的輸出 | 深度學習、LLM | AI、機器學習 |
| 14 Simulation, Graphics, Gaming | 複雜系統與模型、排隊系統、電腦圖學光照與形狀、動畫、遊戲開發 | **離散事件排隊模擬**(對照 M/M/1 理論值)、**光線追蹤器**(輸出 PPM)、2D 遊戲(game loop、碰撞偵測) | 粒子系統、簡化天氣模型 | GPU 渲染管線概念 | 電腦圖學、機率 |
| 15 Networks | 網路類型、連線方式、封包交換、開放系統與協定、TCP/IP、高階協定、MIME、防火牆、位址與 DNS、雲端、區塊鏈 | TCP 聊天室、UDP 對照、手寫 HTTP client/server、DNS 封包解析、subnet 計算、Wireshark 觀察、**proof-of-work 區塊鏈** | Docker 部署到雲端 | HTTPS/TLS、IPv6、CDN | 計算機網路 |
| 16 The World Wide Web | 搜尋引擎、cookie、網站分析、HTML/CSS、互動網頁、XML、社群網路 | HTML/CSS/JS 前端;**Flask REST API 接資料庫**;cookie 與 session;JSON 與 XML 對照 | 爬蟲 + 倒排索引 + 簡化 PageRank 的迷你搜尋引擎 | 以 JavaScript/REST **取代**書上的 Java Applet、JSP | Web、資料庫 |
| 17 Computer Security | CIA、密碼與驗證、CAPTCHA、生物辨識、惡意程式、攻擊類型、密碼學、線上資訊保護 | 古典密碼與頻率分析破解、hash 加鹽與暴力破解、小數字 RSA、C 的 **buffer overflow** 與防護、**對第 16 章 app 做 SQL injection 再修補** | TLS 握手流程模擬 | 雙因素驗證、密碼管理器 | 資訊安全 |

### 5.3 起始碼的依賴關係

| 章 | 起始碼內附的參考解 |
|---|---|
| 5 | 第 4 章 ALU(選用;CPU 也可用 C 運算子) |
| 6 | 第 5 章 CPU |
| 9 | 第 5 章 CPU、第 6 章組譯器(延伸專案用) |
| 10 | 第 5 章 CPU(延伸專案用) |
| 17 | 第 16 章 Flask app |

其他章不依賴前章。

---

## 6. Lab 與測試

- **統一環境**:repo 附 `env/Dockerfile`(Ubuntu 24.04 + gcc/g++、make、gdb、valgrind、python3、pytest、numpy、matplotlib、pandas、flask、pygame),學生與閘門都在同一個映像檔跑。本機 WSL 只當備案。
- **C**:自寫、零依賴的測試標頭 `labs/common/ctest.h`;`make test` 以 `-Wall -Wextra -fsanitize=address,undefined` 編譯。第 8 章另跑 Valgrind。
- **Python**:pytest。
- **繳交**:git;測試全過 + 一段中文說明(設計取捨、遇到的錯)= 通過,否則需修正(沿用骨架的兩級制)。
- **每個任務**在規格書與測試名稱上都標出觀念 ID,供涵蓋度閘門檢查。

---

## 7. 評量(預設,老師自行調整)

沿用骨架:筆試 60(期中 25 + 期末 35)/實作 30/平時 10。筆試考卷由 `build_exam.py` 依選定章節組卷。

---

## 8. 檔案佈局與品質閘門

沿用線代「內容與排版分離、內容用 Markdown」的架構。

```
course-cs-intro/
  index.html                  # 產出:課程首頁(18 張章卡)
  content/                    # 內容(Markdown),寫法見 content/README.md
    course.yaml  index.md  README.md
    ch01/ … ch18/
      chapter.md              # 章資訊、觀念清單(ID)
      01-*.md …               # 一個觀念一個檔:觀念 → 講解 → 隨堂練習(+ ## 驗算)
      bank.md                 # 筆試題庫(每題帶標籤與 ## 驗算)
      lab.md  projects.md     # 核心 Lab、延伸專案的規格書
      figures/*.svg
  labs/
    common/  ctest.h  csi16-spec.md
    ch01/ … ch18/
      starter/                # 學生拿到的(內含前章參考解)
      solution/               # 參考解(只在教師版)
      tests/public/  tests/hidden/
  env/Dockerfile
  _layout/templates/          # Jinja2
  assets/handout.css          # 沿用設計系統
  _generators/                # 必須版控
  ch01/ … ch18/               # 產出,不要手改
    CN-講義-學生版.html / CN-講義-教師版.html
    CN-題庫-學生版.html / CN-題庫-教師版.html
    CN-Lab.html  CN-專案.html
    CN-starter.zip            # 不含 solution/ 與 tests/hidden/
  exams/                      # build_exam.py 的產出
```

四道閘門,每批全過才算完成:

1. **`verify.py`(結構)**:兩版題幹一致、學生版不洩答案、每題有作答區、數學式與 HTML 跳脫、學生 zip 不含參考解與隱藏測試。
2. **`verify_answers.py`**:執行每個計算/追蹤題的 `## 驗算`(Python 算出答案並與題目答案比對,例如二補數、Huffman 編碼長度、甘特圖時間)。
3. **`run_labs.py`(在 Docker 裡)**:參考解通過全部公開與隱藏測試、sanitizer 無錯;**起始碼能編譯且在 TODO 對應的測試上失敗**(證明測試真的在測東西)。
4. **`verify_coverage.py`**:每個觀念 ID 至少有 1 題筆試、1 個核心 Lab 任務、1 個測試。

沿用鐵律:圖表標籤用英文、學生版作答區 `min-height: 130px`、考卷作答區依配分給高度、段落與題幹不跨頁切開;寫內容檔一律用 Write 工具(Bash heredoc 會吃掉 `\\`)。

---

## 9. 分批建置

每批使用者審過再做下一批。

| 批次 | 範圍 | 另外要建的共用件 |
|---|---|---|
| 1 | 第 1–3 章(總論 + 資訊層)— **已完成 2026-09-27**:21 個觀念、206 題筆試、3 個 Lab(共 146 個測試)、11 個延伸專案;四道閘門全過 | `_generators/` 骨架、四道閘門、`env/Dockerfile`、`ctest.h`、`build_exam.py` |
| 2 | 第 4–6 章(硬體層 + 低階語言) | `csi16-spec.md` |
| 3 | 第 7–9 章(程式層) | — |
| 4 | 第 10–11、18 章(OS + 極限) | — |
| 5 | 第 12–14 章(應用層) | — |
| 6 | 第 15–17 章(通訊層) | — |

---

## 10. 待討論清單

1. 評量比重與考卷題型比重(第 7 節)——第一批只需要 `build_exam.py` 能動,比重可以後定。
2. 是否比照線代加做**理論教案**與**每章診斷考**——目前不做,使用者要時再加。
3. 繳交平台(GitHub Classroom 或學校系統)——影響起始碼的包裝方式,不影響內容。
