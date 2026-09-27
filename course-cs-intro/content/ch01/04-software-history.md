---
id: C1.4
title_en: History of Computing Software
title_zh: 計算軟體的歷史
sub: Each generation puts another layer between the programmer and the machine
level: basic
lab_hook: "任務 2:`make pipeline`;任務 4:`software_generation()`"
---
## 觀念
**Generations of software** (the definition used in this course; a boundary year belongs to the new generation):

| Generation | Years | What appeared |
|---|---|---|
| 1 | 1951–1958 | programs written in **machine language**; then **assembly language** and **assemblers** that translate it |
| 2 | 1959–1964 | **high-level languages** (FORTRAN, COBOL, Lisp) and **compilers**; programmers no longer think in machine instructions |
| 3 | 1965–1970 | **systems software**: utility programs, loaders, linkers, and **operating systems** that manage the machine; time-sharing |
| 4 | 1971–1989 | **structured programming** (C, Pascal); **application packages** (spreadsheets, word processors, database systems) for non-programmers |
| 5 | 1990– | object-oriented design, the **World Wide Web**, open source, a huge user base; software everywhere |

The long-term trend: **each generation adds a layer of software between the user and the hardware**. The programmer moves further from the machine, and the user of an application may never write a program at all.

**Translators.** An **assembler** translates assembly language into machine code. A **compiler** translates a high-level language program into machine code (or into assembly first). An **interpreter** executes a high-level program directly, one statement at a time, without producing a separate machine-code program. Today's C toolchain shows the layers explicitly: preprocess (`gcc -E`) → compile to assembly (`gcc -S`) → assemble to an object file (`gcc -c`) → link to an executable.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| machine language | 機器語言 | CPU 直接執行的二進位指令 |
| assembly language | 組合語言 | 用助記符(`add`、`mov`)寫機器指令 |
| assembler | 組譯器 | 把組合語言翻成機器碼 |
| high-level language | 高階語言 | 接近人類思考的語言,如 C、Python |
| compiler | 編譯器 | 把高階語言整個翻成機器碼(或組合語言) |
| interpreter | 直譯器 | 一句一句讀、一句一句執行,不產生獨立的執行檔 |
| linker / loader | 連結器/載入器 | 把多個目的檔合成執行檔/把執行檔放進記憶體執行 |
| systems software | 系統軟體 | 服務程式設計師與機器的軟體:OS、編譯器、連結器 |

## 白話說
最早的程式設計師要直接寫 0 和 1。之後有人想:「用 `ADD` 代替 `0110` 吧」,於是有了組合語言和組譯器。再後來:「能不能直接寫 `total = total + x`?」於是有了高階語言和編譯器。然後又有人寫了作業系統,讓大家不用自己管記憶體和印表機……

每一代都是**把前一代的苦工自動化**,在程式設計師和機器之間多蓋一層。到今天,多數使用者只用應用程式,根本不寫程式——他們和硬體之間隔了好多層。

## 後面會用到
- **系統程式**與**計算機組織**:組譯器、連結器、載入器怎麼運作(本課第 6 章)。
- **編譯器**:高階語言怎麼一步步變成機器碼(第 9 章)。
- **作業系統**:第三代的主角(第 10、11 章)。

## 現代補充
直譯與編譯的界線今天很模糊:Python 先把原始碼「編譯」成 bytecode(`.pyc`),再由虛擬機直譯;Java 與 JavaScript 引擎會在執行時把熱門的程式碼 **JIT 編譯**成機器碼。Lab 任務 2 會讓你同時看到 C 的機器碼與 Python 的 bytecode。

## 原理
**為什麼要分成前處理、編譯、組譯、連結四步?** 每一步解決不同的問題:

1. 前處理:把 `#include`、`#define` 展開,讓編譯器只需要面對純粹的 C。
2. 編譯:把 C 的結構(迴圈、變數、函式)翻成某種 CPU 的組合語言——這一步和 CPU 種類有關。
3. 組譯:把組合語言一對一翻成機器碼,產生**目的檔**;此時呼叫 `printf` 的位址還不知道。
4. 連結:把自己的目的檔和函式庫(例如 libc 的 `printf`)接起來,填上真正的位址,產生執行檔。

拆開的好處是**分工與重用**:改一個 `.c` 檔只要重新編譯它自己,再重新連結即可;組譯器與連結器可以給很多種語言共用。這正是第三代「系統軟體」的精神。

## 老師講解
### 例 1
Starting from `sum.c`, list the four steps of the C toolchain, the command for each, and the kind of file each step produces.

1. **前處理**:`gcc -E sum.c -o sum.i` → `sum.i`,仍是 C 原始碼,但 `#include <stdio.h>` 已被展開成數百行宣告。
2. **編譯**:`gcc -S sum.i -o sum.s` → `sum.s`,組合語言文字檔,可以看到 `main:` 標籤與 `call` 指令。
3. **組譯**:`gcc -c sum.s -o sum.o` → `sum.o`,可重定位的**目的檔**(`file` 指令顯示 relocatable),是二進位,但還不能執行。
4. **連結**:`gcc sum.o -o sum` → 執行檔(`file` 顯示 executable),`printf` 等外部函式的位址在這一步接上。
5. 對照世代:組譯器(第 1 代)、編譯器(第 2 代)、連結器與載入器(第 3 代)全部在這一條管線裡。

### 例 2
Classify each as a compiler, an interpreter, or an assembler (or a combination), and justify: (a) `gcc`, (b) `python3` running a script, (c) `as`, (d) a web browser running JavaScript.

1. (a) `gcc`:**編譯器**(其實是整條工具鏈的指揮者,會依序呼叫前處理器、編譯器、`as` 組譯器與 `ld` 連結器)。
2. (b) `python3`:先把原始碼編譯成 bytecode,再由虛擬機**直譯**執行 → 編譯 + 直譯的組合;不產生獨立的機器碼執行檔。
3. (c) `as`:**組譯器**,組合語言 → 機器碼(目的檔)。
4. (d) 瀏覽器的 JavaScript 引擎:一開始直譯,熱門程式碼再 JIT **編譯**成機器碼 → 組合。
5. 重點:判斷依據是「有沒有先把整個程式翻成另一種語言(特別是機器碼)再執行」。

## 易錯點
- 以為「編譯 = 直接產生執行檔」:中間其實還有組譯與連結。
- 以為 Python 完全沒有編譯步驟:有,只是編譯成 bytecode 而不是機器碼。
- 世代邊界:1959 是第 2 代、1990 是第 5 代。

## 教學提示
現場跑一次 `gcc -E`、`-S`、`-c`、連結,並用 `file` 看每個產出的種類,比任何投影片都有說服力。這正好是 Lab 任務 2。

## 練習
### 照做
Match each tool with what it translates: assembler, compiler, linker.

#### 解答
組譯器:組合語言 → 機器碼(目的檔)。編譯器:高階語言 → 組合語言或機器碼。連結器:多個目的檔與函式庫 → 一個執行檔。

### 是非
True or false: An interpreter translates the whole program into a machine-code executable before running it.

#### 解答
False。那是編譯器的做法;直譯器是一邊讀一邊執行,不產生獨立的機器碼執行檔。

### 變化
Assign each to a software generation (1–5) using this course's definition: COBOL (1959), UNIX (1969), VisiCalc (1979), the World Wide Web (1991), the A-0 system (1952).

#### 解答
COBOL → 2;UNIX → 3;VisiCalc → 4;WWW → 5;A-0 → 1。

### 應用
After `gcc -c sum.c`, running `./sum.o` fails. Explain why, and what step is missing.

#### 解答
`sum.o` 是目的檔(relocatable),還沒有和 C 函式庫連結、也沒有程式進入點的最終配置,作業系統無法把它當執行檔載入。缺少**連結**:`gcc sum.o -o sum`。

### 挑戰
The chapter says each software generation "adds a layer between the user and the hardware". Pick two generations and describe exactly what new layer appeared and what work it took away from people.

#### 解答
參考:第 1→2 代:高階語言與編譯器這一層出現,程式設計師不再需要手動選擇暫存器、記住機器指令的編碼,改由編譯器負責。第 2→3 代:作業系統這一層出現,程式設計師不再需要自己載入程式、管理記憶體與 I/O 裝置、排程多個工作。第 3→4 代:應用程式套件出現,一般使用者不必寫程式就能做表格、文書與資料庫。任兩代、說清楚「新層是什麼」與「省掉誰的哪些工作」即可。
