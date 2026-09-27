---
id: C1.1
title_en: Layers of a Computing System
title_zh: 計算系統的分層
sub: Hardware, software, and data — organized as layers
level: basic
lab_hook: "任務 1:`sum.c` / `sum.py`;任務 2:`make pipeline` 與 `layers.md`"
---
## 觀念
A **computing system** is a dynamic entity made of **hardware** (the physical elements: chips, boards, wires, storage, I/O devices), **software** (the programs that give instructions to the hardware), and **data** (the information the system manages and manipulates).

The book organizes a computing system as **layers**, like an onion. From the inside out:

| Layer | What it is about | Chapters |
|---|---|---|
| Information | how numbers, text, images, audio, video are represented in binary | 2–3 |
| Hardware | gates, circuits, CPU, memory, I/O | 4–5 |
| Programming | machine language → assembly → high-level languages, algorithms, data structures | 6–9 |
| Operating systems | managing memory, processes, files; letting programs share the machine | 10–11 |
| Applications | spreadsheets, databases, AI, simulation, graphics, games | 12–14 |
| Communications | networks, the Web, security | 15–17 |

Each layer uses the services of the layer below it and offers services to the layer above it. Chapters 1 and 18 look at the system as a whole.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| computing system | 計算系統 | 硬體 + 軟體 + 資料,合起來完成工作的整體 |
| hardware | 硬體 | 摸得到的實體元件:晶片、主機板、記憶體、硬碟、鍵盤螢幕 |
| software | 軟體 | 指揮硬體做事的程式 |
| data | 資料 | 系統處理、儲存的資訊 |
| layer | 層 | 一組功能;只和相鄰的上下層打交道 |
| application | 應用程式 | 使用者直接操作的程式 |
| operating system (OS) | 作業系統 | 管理硬體資源、讓多個程式共用機器的軟體 |

## 白話說
電腦不是一個「東西」,而是很多層疊起來的系統。你按下 Enter 讓程式算出答案,這件事從上到下經過:應用程式 → 你寫的高階語言程式 → 編譯器翻成的機器碼 → 作業系統把程式載入、幫它讀鍵盤 → CPU 真正執行指令 → 最底下全部是 0 與 1。

分層的好處是**每一層只要懂自己和隔壁**。寫網頁的人不必懂電晶體,設計 CPU 的人也不必懂 HTML。這門課就是一層一層往外走,讓你每一層都看過一次。

## 後面會用到
這張分層圖就是整個資工系課程的地圖:資訊層 → **計算機組織**、**數位邏輯**;硬體層 → **計算機組織**;程式層 → **程式設計**、**資料結構**、**演算法**、**編譯器**;作業系統層 → **作業系統**;應用層 → **資料庫**、**人工智慧**、**電腦圖學**;通訊層 → **計算機網路**、**資訊安全**。

## 現代補充
今天的「一台電腦」可能是手機、雲端上的一台虛擬機,或一個容器(container)。層還是那些層,只是中間多了**虛擬化**:雲端上你看到的「硬體」其實是另一層軟體模擬出來的。第 10 章會再談。

## 原理
分層之所以有效,是因為每一層都對上層提供一個**介面**(interface),並把自己的實作細節藏起來。只要介面不變,下層可以整個換掉,上層完全不用改——例如同一支 C 程式可以在 Intel 和 ARM 的 CPU 上重新編譯執行,因為編譯器這一層吸收了兩種機器語言的差異。這個性質就是下一個觀念「抽象」的具體表現。

分層也有代價:每多一層就多一點開銷(翻譯、檢查、資料搬移)。效能要求極高的地方(例如作業系統核心、遊戲引擎)有時會刻意跨層,直接利用下層的細節。

## 老師講解
### 例 1
A user types `echo "1 2 3" | ./sum` and sees `6`. List, from top to bottom, the layers involved and what each one does in this scenario.

1. **Application(應用層)**:使用者看到的是一個「加總數字」的小工具;他只關心輸入 1 2 3、輸出 6。
2. **Programming(程式層)**:`sum` 是用 C 寫的;一行 `while (scanf(...) == 1) total += x;` 描述了整個演算法。編譯器把它翻成組合語言、再翻成機器碼。
3. **Operating system(作業系統層)**:shell 請 OS 建立兩個行程(`echo` 與 `sum`),用管線(pipe)把前者的輸出接到後者的輸入;`scanf` 最後透過系統呼叫向 OS 要資料。
4. **Hardware(硬體層)**:CPU 依序抓取、解碼、執行機器指令;加法由 ALU 完成,變數放在暫存器或記憶體。
5. **Information(資訊層)**:鍵盤送進來的是字元 `'1'`、`' '`、`'2'`(ASCII 碼),`scanf` 把它們轉成二進位整數才能相加;印出時再轉回字元 `'6'`。
6. **Communications(通訊層)**:這個例子在單機上完成,沒有用到網路;若改成在遠端伺服器上執行(例如透過 ssh),就會多經過這一層。

### 例 2
Classify each item as hardware, software, or data: (a) the CPU, (b) a spreadsheet file `grades.xlsx`, (c) the Excel program, (d) the Linux kernel, (e) an SSD, (f) the text of an email.

1. **看它是不是摸得到的實體**:CPU、SSD 是實體元件 → (a)、(e) 是 **hardware**。
2. **看它是不是「指令」**:Excel 與 Linux 核心都是一串指揮硬體做事的指令 → (c)、(d) 是 **software**。其中 Linux 核心屬於作業系統層,Excel 屬於應用層。
3. **看它是不是被處理的資訊**:`grades.xlsx` 與郵件內文是被程式讀寫的內容 → (b)、(f) 是 **data**。
4. 注意:程式本身存在硬碟上時也是一串位元組;「是軟體還是資料」要看它扮演的角色——被 CPU 執行時是軟體,被編譯器讀進來處理時就是資料。

## 易錯點
- 把作業系統當成「硬體的一部分」:OS 是軟體,只是離硬體最近。
- 以為分層是「由外往內」依序執行:其實每個動作都會同時用到很多層,分層是**看系統的角度**,不是時間順序。
- 「程式 vs 資料」不是物品的固有屬性,而是角色;例 2 的第 4 步常被忽略。

## 教學提示
開場可以現場打 `echo "1 2 3" | ./sum`,再問「這一行按下 Enter 之後發生了哪些事?」讓學生七嘴八舌補,最後對應到六層。Lab 任務 2 的 `layers.md` 就是這個活動的書面版,建議課堂先示範一段。

## 練習
### 照做
List the six layers of a computing system used in this course, from the innermost to the outermost.

#### 解答
Information → Hardware → Programming → Operating systems → Applications → Communications。

### 是非
True or false: The operating system is part of the hardware layer.

#### 解答
False。作業系統是軟體,屬於作業系統層;它管理硬體,但本身不是硬體。

### 變化
For each of the following, name the layer that is mainly responsible: (a) deciding which program gets the CPU next, (b) representing the letter `A` as `01000001`, (c) sending a web page from a server to your phone, (d) adding two numbers in the ALU.

#### 解答
(a) Operating systems;(b) Information;(c) Communications;(d) Hardware。

### 應用
You open a photo on your phone and apply a filter. Describe what each of at least four layers contributes to this action.

#### 解答
參考答案:Application(相簿 App 的濾鏡按鈕與顯示)、Programming(濾鏡演算法:對每個像素做運算)、Operating systems(讀取照片檔、分配記憶體、把結果交給螢幕驅動程式)、Information(照片以 RGB 數值、JPEG 壓縮格式儲存)、Hardware(CPU/GPU 真正執行運算、螢幕顯示)。任四層、說明合理即可。

### 挑戰
A program is stored on disk as bytes. Explain when those bytes should be called "software" and when they should be called "data". Give one real tool that treats a program as data.

#### 解答
被 CPU 載入並執行時,它扮演的是軟體;被另一個程式讀進來分析、轉換時,它就是資料。例:編譯器把原始碼當資料讀入;`objdump` 把執行檔當資料讀入並反組譯;防毒軟體掃描執行檔也是把它當資料。
