---
chapter: 1
---
## Q1 · C1.1 · 選擇 · basic · 2
Which list gives the layers of a computing system in this course from the innermost to the outermost?

- A. Hardware → Information → Programming → Operating systems → Applications → Communications
- B. Information → Hardware → Programming → Operating systems → Applications → Communications
- C. Information → Hardware → Operating systems → Programming → Applications → Communications
- D. Communications → Applications → Operating systems → Programming → Hardware → Information

### 答案
B

### 詳解
最裡層是資訊的表示(位元),接著是處理位元的硬體,然後是指揮硬體的程式,再來是管理程式的作業系統,應用程式建在作業系統之上,最外層是讓電腦彼此溝通的通訊層。

### 迷思對照
- **A** 以為硬體是最底層 → 回看 C1.1:硬體處理的是位元,所以「資訊怎麼表示」在更裡面
- **C** 把作業系統放在程式層之下 → 回看 C1.1:本課的程式層講的是語言與演算法,作業系統是用這些工具寫出來、再服務應用程式的
- **D** 方向顛倒 → 回看 C1.1:題目問的是由內而外

## Q2 · C1.1 · 選擇 · basic · 2
Which of the following is **data** rather than hardware or software?

- A. The Linux kernel
- B. A solid-state drive
- C. A CSV file of exam scores
- D. The Python interpreter

### 答案
C

### 詳解
成績檔是被程式讀寫、處理的資訊,屬於資料。Linux 核心與 Python 直譯器是軟體,SSD 是硬體。

### 迷思對照
- **A** 以為作業系統是資料 → 回看 C1.1:作業系統是指揮硬體的程式
- **B** 把儲存裝置和存在裡面的東西混為一談 → 回看 C1.1:SSD 本身是硬體
- **D** 以為直譯器只是「一個檔案」所以是資料 → 回看 C1.1:它被執行時扮演軟體的角色

## Q3 · C1.1 · 選擇 · mid · 3
When your program calls `scanf` to read a number typed on the keyboard, which layer actually receives the key presses from the device and hands the bytes to your program?

- A. The application layer
- B. The programming layer
- C. The operating systems layer
- D. The communications layer

### 答案
C

### 詳解
鍵盤是 I/O 裝置,由作業系統的驅動程式管理;`scanf` 最後透過系統呼叫向 OS 要資料,OS 再把位元組交給程式。

### 迷思對照
- **A** 以為使用者看得到的層就負責輸入 → 回看 C1.1:應用程式只是呼叫下層的服務
- **B** 以為 `scanf` 自己就能讀鍵盤 → 回看 C1.1:函式庫最後要靠作業系統存取裝置
- **D** 把「輸入輸出」和「網路通訊」混為一談 → 回看 C1.1:通訊層處理的是電腦之間的溝通

## Q4 · C1.1 · 選擇 · mid · 3
Which statement about layers is correct?

- A. A layer may use any other layer directly, in any order.
- B. Each layer uses the services of the layer below and provides services to the layer above.
- C. Layers describe the time order in which a program runs: first hardware, then software.
- D. Once a layer is designed, the layers below it can never be changed.

### 答案
B

### 詳解
分層的核心是「只和相鄰層打交道」:用下層的服務、提供服務給上層。正因為上層只依賴介面,下層才能被替換。

### 迷思對照
- **A** 以為分層沒有規則 → 回看 C1.1:跨層依賴會讓系統難以修改
- **C** 把分層當成時間順序 → 回看 C1.1:分層是看系統的角度,一個動作同時牽涉很多層
- **D** 以為分層讓系統僵化 → 回看 C1.2:分層正是讓下層可以替換的設計

## Q5 · C1.1 · 簡答 · mid · 6
You click "Send" on a chat app and your friend in another city sees the message. Describe what at least four different layers contribute to this action.

### 答案
參考:Application(聊天 App 介面與送出按鈕)、Programming(App 的程式邏輯:打包訊息、處理回應)、Operating systems(提供網路 socket、管理記憶體與行程)、Information(文字以 UTF-8 編碼成位元組)、Hardware(CPU 執行、網路卡送出電訊號)、Communications(TCP/IP 把封包送到伺服器與朋友的手機)。

### 詳解
重點是能說出每一層「在這個情境裡做了什麼」,而不是只列層名。通訊層在這題一定要出現。

### 評分要點
- 至少四層、每層都有具體說明(每層 1 分,最多 4 分)
- 有提到通訊層在跨城市傳送中的角色(1 分)
- 層與功能對應正確,沒有把 OS 說成硬體等錯誤(1 分)

## Q6 · C1.1 · 簡答 · hard · 6
A compiled program is stored on disk as bytes. Explain why the same bytes can be called software in one situation and data in another. Give one real tool for each situation.

### 答案
「軟體」或「資料」是角色,不是固有屬性。被 CPU 載入執行時,它是軟體(例:在 shell 執行 `./sum`);被另一個程式讀進來分析或轉換時,它是資料(例:`objdump -d sum` 反組譯它、防毒軟體掃描它)。

### 詳解
這題考的是分層觀點的彈性:同一串位元組,在不同層、不同情境扮演不同角色。

### 評分要點
- 說明「角色」的概念(2 分)
- 當作軟體的例子正確(2 分)
- 當作資料的例子正確(2 分)

## Q7 · C1.2 · 選擇 · basic · 2
Which best describes an abstraction?

- A. A vague description that leaves out important requirements
- B. A model that keeps only the details needed for a goal and hides the rest
- C. A piece of hardware that has no software
- D. A program written without any functions

### 答案
B

### 詳解
抽象是「只留下目前需要的細節」,介面本身必須精確。

### 迷思對照
- **A** 把抽象當成「模糊」 → 回看 C1.2:抽象的介面要精確,只是不談實作
- **C** 把抽象和「沒有軟體」連在一起 → 回看 C1.2:抽象是一種看待系統的方式,和有沒有軟體無關
- **D** 把抽象和程式寫法亂連 → 回看 C1.2:函式本身就是抽象的一種

## Q8 · C1.2 · 選擇 · mid · 3
A `KVStore` offers `put`, `get`, `delete`, and `keys`. Which method name would **leak** an implementation detail into its interface?

- A. `contains(key)`
- B. `get_block_index(key)`
- C. `size()`
- D. `clear()`

### 答案
B

### 詳解
區塊編號是底層儲存方式的細節;放進介面後,使用者就會依賴它,實作一換就壞。

### 迷思對照
- **A** 以為任何新方法都算洩漏 → 回看 C1.2:「有沒有這個 key」是使用者層級的問題
- **C** 以為大小是實作細節 → 回看 C1.2:存了幾筆資料是使用者關心的抽象資訊
- **D** 以為清空會洩漏實作 → 回看 C1.2:清空所有資料不涉及儲存方式

## Q9 · C1.2 · 選擇 · mid · 3
Program P uses a library only through its documented functions. The library's authors completely rewrite the internals but keep the same functions and behavior. What happens to P?

- A. P must be rewritten because the internals changed.
- B. P keeps working without changes (though its speed may differ).
- C. P stops compiling because function names changed.
- D. P works only if it was written in the same language as the library.

### 答案
B

### 詳解
P 只依賴介面;介面與行為不變,實作可以自由替換。效能可能不同,這是抽象唯一可能「透出來」的地方。

### 迷思對照
- **A** 以為使用者依賴實作 → 回看 C1.2:只透過介面使用就不受實作影響
- **C** 沒注意到題目說介面不變 → 回看 C1.2:名稱與參數屬於介面
- **D** 把抽象和語言綁在一起 → 回看 C1.2:介面可以跨語言,關鍵是約定不變

## Q10 · C1.2 · 選擇 · hard · 4
Which is the best example of a **leaky abstraction**?

- A. A function that returns the sum of a list
- B. Floating-point numbers that look like real numbers, but `0.1 + 0.2 == 0.3` is false
- C. A stack with `push` and `pop`
- D. A variable named `total`

### 答案
B

### 詳解
浮點數想呈現「實數」的抽象,但底層有限位元的二進位表示讓捨入誤差透了出來。第 3 章會詳細解釋。

### 迷思對照
- **A** 以為任何函式都會洩漏 → 回看 C1.2:加總函式的行為完全符合它的介面
- **C** 以為資料結構一定洩漏 → 回看 C1.2:stack 的介面與行為一致
- **D** 把命名和抽象混為一談 → 回看 C1.2:變數名稱不是抽象層

## Q11 · C1.2 · 簡答 · mid · 6
Choose one abstraction you use every day as a programmer (for example a file, a function, or a list). State its interface and two implementation details it hides.

### 答案
參考:檔案。介面:`open`、`read`、`write`、`close`,把檔案看成一串可讀寫的位元組。隱藏的細節:資料存在磁碟的哪些區塊、區塊是否連續、是否已被快取在記憶體、檔案系統種類。

### 詳解
好的答案要清楚區分「使用者能做什麼」與「背後怎麼做」。

### 評分要點
- 介面描述正確、完整(2 分)
- 兩個被隱藏的細節正確(各 2 分)

## Q12 · C1.2 · 簡答 · hard · 8
In Lab task 3, a hidden test runs the same client code on disks with block sizes 16, 64, and 512. Explain what property of your `KVStore` this checks, and describe a buggy implementation that would pass the public tests but fail this hidden test.

### 答案
它檢查 KVStore 的介面有沒有洩漏(或依賴)區塊大小:同一段使用者程式在不同的底層「硬體」上都應該正確運作。有 bug 的實作例:把 64 寫死在程式裡(例如每次切 64 位元組),在預設 64 的 disk 上通過公開測試,但 block_size = 16 時 `write_block` 會因長度不符而丟錯,或 512 時浪費空間、讀回錯的資料。

### 詳解
這題把「抽象讓實作可替換」落到具體測試上,也提醒學生:公開測試通過不代表正確。

### 評分要點
- 說出「檢查是否依賴區塊大小/底層細節」(3 分)
- 描述一個合理的 bug(3 分)
- 說明該 bug 在哪個大小下會怎麼壞(2 分)

## Q13 · C1.3 · 計算 · basic · 4
Using the course's definition of hardware generations (1: 1951–1958, 2: 1959–1964, 3: 1965–1970, 4: 1971 on; boundary years belong to the new generation), which generation does a machine from 1962 belong to? Answer with a single number.

### 答案
`2`

### 詳解
1962 介於 1959 與 1964 之間,屬於第 2 代(電晶體)。

### 驗算
```check
sum(1962 >= y for y in (1951, 1959, 1965, 1971)) == int(ANS)
```

## Q14 · C1.3 · 計算 · mid · 5
Using $N(t) = 2300 \cdot 2^{(t - 1971)/2}$, predict the number of transistors on a chip in 1991.

### 答案
`2355200`

### 詳解
1. 經過 1991 − 1971 = 20 年,加倍 10 次。
2. $2300 \times 2^{10} = 2300 \times 1024 = 2{,}355{,}200$。

### 驗算
```check
round(2300 * 2 ** ((1991 - 1971) / 2)) == int(ANS)
```

## Q15 · C1.3 · 計算 · mid · 6
A chip had 2,300 transistors in 1971 and another had 42,000,000 in 2000. What doubling period (in years, rounded to two decimal places) do these two data points imply?

### 答案
`2.05`

### 詳解
1. 經過 2000 − 1971 = 29 年。
2. 成長倍數 $42{,}000{,}000 / 2300 \approx 18260.87$。
3. 加倍次數 $\log_2 18260.87 \approx 14.156$。
4. 加倍週期 $= 29 / 14.156 \approx 2.0485$,四捨五入到小數兩位是 2.05 年,很接近「約兩年」。

### 驗算
```check
f"{29 / math.log2(42000000 / 2300):.2f}" == ANS
```

## Q16 · C1.3 · 計算 · hard · 6
If transistor counts double every 2 years, how many whole years are needed for the count to grow by at least a factor of 1,000,000? (Doubling happens continuously in the model; give the smallest whole number of years.)

### 答案
`40`

### 詳解
1. 需要 $2^{t/2} \ge 10^6$,即 $t \ge 2\log_2 10^6 \approx 39.86$。
2. 最小整數年數為 40。

### 驗算
```check
math.ceil(2 * math.log2(10**6)) == int(ANS)
```

## Q17 · C1.3 · 選擇 · basic · 2
Which switching technology characterizes the **third** hardware generation?

- A. Vacuum tubes
- B. Transistors
- C. Integrated circuits
- D. Microprocessors (VLSI)

### 答案
C

### 詳解
第 3 代(1965–1970)的特徵是積體電路:很多電晶體做在同一片矽晶片上。

### 迷思對照
- **A** 記成第 1 代 → 回看 C1.3 的世代表
- **B** 記成第 2 代 → 回看 C1.3 的世代表
- **D** 記成第 4 代 → 回看 C1.3:整顆 CPU 放在一片晶片上是 1971 年起的第 4 代

## Q18 · C1.3 · 選擇 · mid · 3
Which statement about Moore's law is correct?

- A. It is a law of physics that cannot be broken.
- B. It says CPU clock frequency doubles every two years.
- C. It is an empirical observation that transistor counts on a chip double roughly every two years.
- D. It says computers become twice as cheap every year.

### 答案
C

### 詳解
摩爾定律是對產業趨勢的經驗觀察,講的是電晶體數,而且近年已經放慢。

### 迷思對照
- **A** 以為是物理定律 → 回看 C1.3:它是經驗觀察,已經放慢
- **B** 把電晶體數和時脈混淆 → 回看 C1.3 的現代補充:時脈約 2005 年後就停滯了
- **D** 記錯對象與週期 → 回看 C1.3:講的是電晶體數、約每兩年

## Q19 · C1.3 · 選擇 · mid · 3
Who is often credited with writing the first program, for Babbage's Analytical Engine?

- A. Grace Hopper
- B. Ada Lovelace
- C. Alan Turing
- D. Herman Hollerith

### 答案
B

### 詳解
Ada Lovelace 為分析機寫下計算白努利數的步驟,被視為第一個程式。

### 迷思對照
- **A** 和 A-0 編譯器的作者混淆 → 回看 C1.4:Grace Hopper 是 1950 年代的編譯器先驅
- **C** 和計算理論混淆 → 回看 C1.3:Turing 在 1936 年提出抽象的計算模型
- **D** 和打孔卡製表機混淆 → 回看 C1.3:Hollerith 做的是 1890 年人口普查的製表機

## Q20 · C1.3 · 選擇 · hard · 4
Since about 2005, CPU clock speeds have stopped increasing much, yet chips keep getting more powerful. What is the main reason?

- A. Transistors stopped getting smaller.
- B. Extra transistors are used for more cores, larger caches, and specialized units such as GPUs.
- C. Programs became shorter.
- D. Operating systems were removed to save time.

### 答案
B

### 詳解
功耗與散熱限制了時脈,但電晶體數仍在增加(雖然變慢),於是用來做多核心、更大的快取與專用硬體。

### 迷思對照
- **A** 以為電晶體完全不再縮小 → 回看 C1.3 的現代補充:是放慢,不是停止
- **C** 以為效能來自程式變短 → 回看 C1.3:這題問的是硬體
- **D** 以為拿掉作業系統能提升效能 → 回看 C1.1:作業系統是必要的一層

## Q21 · C1.3 · 簡答 · mid · 6
Explain why exponential growth makes long-term predictions with Moore's law fragile. Use numbers: compare the growth over 40 years with a doubling period of 2 years versus 2.5 years.

### 答案
40 年、週期 2 年:$2^{20} \approx 1{,}048{,}576$ 倍;週期 2.5 年:$2^{16} = 65{,}536$ 倍。週期只差 0.5 年,結果差了 16 倍。指數模型對參數極度敏感,所以長期外推很不可靠。

### 詳解
這題練習把「指數成長」的直覺量化。

### 評分要點
- 兩個數字都算對(各 2 分)
- 說明「對參數敏感、所以不可靠」(2 分)

## Q22 · C1.3 · 簡答 · mid · 6
For each hardware generation, name its key technology and explain one practical consequence for users of that era (size, reliability, cost, or accessibility).

### 答案
參考:第 1 代真空管——機器佔滿房間、耗電大、真空管常燒壞;第 2 代電晶體——更小更可靠,商業公司開始買得起;第 3 代積體電路——更便宜,出現終端機與分時系統,很多人可以同時使用;第 4 代 VLSI 微處理器——個人電腦出現,一般人可以擁有電腦。

### 詳解
重點是把「技術」和「對使用者的影響」連起來。

### 評分要點
- 四代的技術都正確(2 分)
- 每代一個合理的影響(每代 1 分)

## Q23 · C1.4 · 計算 · basic · 4
Using the course's definition of software generations (1: 1951–1958, 2: 1959–1964, 3: 1965–1970, 4: 1971–1989, 5: 1990 on), which generation does the C language (1972) belong to? Answer with a single number.

### 答案
`4`

### 詳解
1972 介於 1971 與 1989 之間 → 第 4 代(結構化程式設計)。

### 驗算
```check
sum(1972 >= y for y in (1951, 1959, 1965, 1971, 1990)) == int(ANS)
```

## Q24 · C1.4 · 計算 · mid · 5
A class lists these milestones: A-0 system (1952), COBOL (1959), UNIX (1969), VisiCalc (1979), World Wide Web (1991), Docker (2013). Using the course's software generations, write the generation numbers in the same order, separated by commas without spaces.

### 答案
`1,2,3,4,5,5`

### 詳解
依起始年 1951、1959、1965、1971、1990 逐一判斷,邊界年份屬於新世代(COBOL 1959 → 第 2 代)。

### 驗算
```check
",".join(str(sum(y >= s for s in (1951, 1959, 1965, 1971, 1990))) for y in (1952, 1959, 1969, 1979, 1991, 2013)) == ANS
```

## Q25 · C1.4 · 選擇 · basic · 2
What does an assembler do?

- A. Translates a high-level language into machine code
- B. Translates assembly language into machine code
- C. Combines object files and libraries into an executable
- D. Executes a program one statement at a time

### 答案
B

### 詳解
組譯器把組合語言(助記符)一對一翻成機器碼。

### 迷思對照
- **A** 和編譯器混淆 → 回看 C1.4 的名詞對照
- **C** 和連結器混淆 → 回看 C1.4 的原理:連結是最後一步
- **D** 和直譯器混淆 → 回看 C1.4 的名詞對照

## Q26 · C1.4 · 選擇 · mid · 3
You run `gcc -c sum.c` and get `sum.o`. What kind of file is `sum.o`?

- A. A preprocessed C source file
- B. An assembly-language text file
- C. A relocatable object file that still needs linking
- D. A finished executable

### 答案
C

### 詳解
`-c` 做到組譯為止,產生目的檔;外部函式(如 `printf`)的位址要到連結時才填上。

### 迷思對照
- **A** 和 `gcc -E` 混淆 → 回看 C1.4 例 1
- **B** 和 `gcc -S` 混淆 → 回看 C1.4 例 1
- **D** 以為 `-c` 會連結 → 回看 C1.4 的應用練習:目的檔不能直接執行

## Q27 · C1.4 · 選擇 · mid · 3
Which statement about Python is most accurate?

- A. Python programs are compiled directly to machine code before running.
- B. Python source is first compiled to bytecode, which a virtual machine then interprets.
- C. Python has no translation step at all.
- D. Python programs must be linked with `ld` before running.

### 答案
B

### 詳解
CPython 把原始碼編譯成 bytecode(可用 `python3 -m dis` 查看),再由虛擬機直譯。

### 迷思對照
- **A** 以為 Python 和 C 一樣產生機器碼 → 回看 C1.4 的現代補充
- **C** 以為直譯器完全不翻譯 → 回看 C1.4 的現代補充:bytecode 也是一種翻譯
- **D** 把 C 的連結步驟套到 Python → 回看 C1.4 例 2

## Q28 · C1.4 · 選擇 · hard · 4
Which software generation first made the **operating system** a central piece of software, freeing programmers from loading programs and managing devices themselves?

- A. First
- B. Second
- C. Third
- D. Fifth

### 答案
C

### 詳解
第 3 代(1965–1970)的主角是系統軟體:載入器、連結器、作業系統與分時系統。

### 迷思對照
- **A** 第 1 代還在寫機器語言與組合語言 → 回看 C1.4 的世代表
- **B** 第 2 代的主角是高階語言與編譯器 → 回看 C1.4 的世代表
- **D** 第 5 代的特徵是 WWW 與物件導向 → 回看 C1.4 的世代表

## Q29 · C1.4 · 簡答 · mid · 6
List the four steps of the C toolchain from `sum.c` to an executable. For each step give the `gcc` option (or command) and the kind of file produced.

### 答案
1. 前處理 `gcc -E` → `.i`(展開後的 C 原始碼);2. 編譯 `gcc -S` → `.s`(組合語言);3. 組譯 `gcc -c` → `.o`(可重定位目的檔);4. 連結 `gcc x.o -o x` → 執行檔。

### 詳解
這就是 Lab 任務 2 的 `make pipeline`。

### 評分要點
- 四步順序正確(2 分)
- 每步的選項與產出正確(每步 1 分)

## Q30 · C1.4 · 簡答 · hard · 8
The chapter says each software generation "adds a layer between the user and the hardware". Pick two consecutive generations, describe the new layer that appeared, and explain what work it took away from which people.

### 答案
參考:第 1 → 2 代,新出現的是高階語言與編譯器這一層;程式設計師不必再選暫存器、記住指令編碼,編譯器替他們做。第 2 → 3 代,新出現的是作業系統這一層;程式設計師與操作員不必再手動載入程式、管理記憶體與 I/O 裝置、安排工作順序。

### 詳解
重點是具體說出「誰」省了「什麼工作」,而不是泛泛而談「更方便」。

### 評分要點
- 兩代選得連續且新層正確(3 分)
- 說明被省掉的具體工作(3 分)
- 說明受益的是哪一群人(2 分)

## Q31 · C1.5 · 選擇 · basic · 2
A biologist runs sequence-alignment software to study a virus but never writes code. Which group does she belong to?

- A. Systems designer
- B. Programmer
- C. Application user / specialist
- D. Hardware engineer

### 答案
C

### 詳解
她用現成的應用程式解決自己領域的問題。

### 迷思對照
- **A** 以為用技術性很高的軟體就是系統設計者 → 回看 C1.5:判斷依據是「使用」還是「建造」
- **B** 以為用電腦做研究就是程式設計師 → 回看 C1.5:她沒有為別人建造工具
- **D** 題目沒有涉及硬體 → 回看 C1.5 的三種角色

## Q32 · C1.5 · 選擇 · mid · 3
Which description of computer science as a discipline is best?

- A. The study of how to use office software efficiently
- B. The systematic study of algorithmic processes: their theory, analysis, design, efficiency, implementation, and application
- C. Writing programs in as many languages as possible
- D. Repairing computer hardware

### 答案
B

### 詳解
資訊科學的核心是演算法程序;寫程式是實作的一部分。

### 迷思對照
- **A** 把使用工具當成學科 → 回看 C1.5:那是把計算當工具
- **C** 把學科等同於寫程式 → 回看 C1.5 的易錯點
- **D** 把資訊科學等同於維修 → 回看 C1.5 的觀念

## Q33 · C1.5 · 選擇 · mid · 3
Why does this course run every Lab inside the same Docker image?

- A. Docker makes C programs run faster than native code.
- B. Everyone gets exactly the same OS, compiler, and library versions, so a Lab that works for the teacher works for every student.
- C. Docker is required to write Python code.
- D. It hides compile errors from students.

### 答案
B

### 詳解
容器固定了整個環境,消除「在我電腦上可以跑」的問題。

### 迷思對照
- **A** 以為容器是加速工具 → 回看 C1.5 的現代補充:容器的價值是環境一致
- **C** 以為 Python 需要 Docker → 回看 C1.5:本課用 Docker 是為了統一環境
- **D** 以為容器會改變編譯行為 → 回看 C1.5:錯誤一樣會出現,而且每個人看到的一樣

## Q34 · C1.5 · 選擇 · hard · 4
An AI assistant gives you a function that passes the two examples in your prompt. What is the most professional next step?

- A. Submit it immediately, since it passed the examples.
- B. Ask the AI whether it is correct and trust its answer.
- C. Read and understand it, then write more tests (including edge cases) and run them.
- D. Rewrite it in another language to be safe.

### 答案
C

### 詳解
兩個例子通過不代表正確;驗證責任在你,方法是讀懂程式並用更多測試(含邊界情況)檢查。

### 迷思對照
- **A** 以為通過範例就等於正確 → 回看 C1.5 的現代補充
- **B** 以為 AI 能自我驗證 → 回看 C1.5:AI 可能很有自信地犯錯
- **D** 以為換語言能解決正確性 → 回看 C1.5:問題在驗證,不在語言

## Q35 · C1.5 · 簡答 · mid · 6
Give one example each of how computer science uses the methods of mathematics, science, and engineering.

### 答案
參考:數學——證明某個演算法一定正確或一定在某個步數內結束,或證明停機問題不可解;科學——設計實驗量測程式的執行時間、建立效能模型;工程——在時間與預算限制下設計、建造並測試一個可靠的系統。

### 詳解
重點是三種方法的差別:證明、實驗、建造與取捨。

### 評分要點
- 三個例子各 2 分,方法要對應正確

## Q36 · C1.5 · 簡答 · hard · 8
List the seven big ideas of computing used in this course, and for any three of them give a concrete example from Chapter 1 or its Lab.

### 答案
Creative development、abstraction、data and information、algorithms、programming、computer systems and networks、impact of computing。例:abstraction——KVStore 把磁碟區塊藏起來;data and information——Lab 任務 4 把計算史當成 CSV 資料分析;programming——任務 1 用 C 與 Python 寫同一支程式;computer systems——任務 2 看到編譯器、作業系統、硬體各層。

### 詳解
七個大觀念是貫穿全課的視角。

### 評分要點
- 七項列對(4 分;少一項扣 1 分,最低 0 分)
- 三個例子具體且正確(4 分;缺一個或錯一個扣 1–2 分)
