---
id: C1.3
title_en: History of Computing Hardware
title_zh: 計算硬體的歷史
sub: From the abacus to VLSI — and Moore's law
level: basic
lab_hook: "任務 4:`hardware_generation()`、`moore()`"
---
## 觀念
**Early history.** Devices to help people compute are old: the **abacus**; Blaise **Pascal**'s mechanical adding machine (1642); Joseph **Jacquard**'s loom controlled by punched cards (1801); Charles **Babbage**'s Difference Engine and the design of the **Analytical Engine**, which already had a memory, an arithmetic unit, input and output; **Ada Lovelace**, who wrote what is considered the first program for it; Herman **Hollerith**'s punched-card tabulating machine for the 1890 US census. In 1936 Alan **Turing** described an abstract machine that defines what can be computed. ENIAC (1946) was one of the first large electronic general-purpose computers.

**Generations of hardware** (the definition used in this course; a boundary year belongs to the new generation):

| Generation | Years | Key technology |
|---|---|---|
| 1 | 1951–1958 | **vacuum tubes**; magnetic drum memory; punched cards and magnetic tape |
| 2 | 1959–1964 | **transistors**; magnetic core memory; magnetic disks |
| 3 | 1965–1970 | **integrated circuits (IC)**; terminals; more memory |
| 4 | 1971– | **LSI / VLSI**: a whole CPU on one chip (the microprocessor); personal computers |

After the fourth generation, progress is described less by component technology and more by **parallel computing** (many processors working together) and **networking** (Ethernet in the 1970s, the Internet).

**Moore's law**: Gordon Moore observed (1965; revised 1975) that the number of transistors on a chip doubles roughly every two years. As a model:

$$N(t) = N_0 \cdot 2^{(t - t_0)/2}$$

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| vacuum tube | 真空管 | 第一代電子計算機的開關元件,體積大、耗電、易壞 |
| transistor | 電晶體 | 第二代起的開關元件,小、省電、可靠 |
| integrated circuit (IC) | 積體電路 | 很多電晶體做在同一塊矽晶片上 |
| LSI / VLSI | 大型/超大型積體電路 | 一顆晶片上有上萬到上億個電晶體 |
| microprocessor | 微處理器 | 整顆 CPU 做在一顆晶片上(Intel 4004,1971) |
| Moore's law | 摩爾定律 | 晶片上的電晶體數約每兩年加倍的經驗法則 |
| parallel computing | 平行計算 | 多個處理器同時處理同一個問題 |

## 白話說
硬體的歷史就是「開關越做越小」的歷史:真空管(拇指大)→ 電晶體(米粒大)→ 積體電路(一片晶片上很多個)→ VLSI(一片晶片上幾十億個)。開關越小,就能放越多、跑越快、越省電,電腦也就從一整個房間縮到你的口袋裡。

摩爾定律是這股趨勢的量化說法:每兩年電晶體數翻倍。翻倍很可怕——20 年就是 $2^{10} \approx 1000$ 倍。

## 後面會用到
- **計算機組織**:為什麼 CPU 有快取(cache)、為什麼改成多核心,都要從「電晶體越來越多但時脈上不去」說起(第 5 章)。
- **數位邏輯**:電晶體如何組成邏輯閘(第 4 章)。
- **演算法**:指數成長的直覺——$2^{n}$ 長得多快——在分析演算法時一直出現(第 18 章)。

## 現代補充
摩爾定律在 2010 年代後明顯放慢:電晶體已經小到只有幾十個原子寬,再縮小很困難,而且時脈大約從 2005 年就停在幾 GHz(功耗與散熱的限制)。業界的回應是**多核心**、**GPU**(大量簡單核心做平行運算,也是今天 AI 訓練的主力)以及**專用晶片**(例如 AI 加速器)。

## 原理
**為什麼翻倍模型用 $2^{(t-t_0)/2}$?** 每過 2 年乘以 2,過了 $t - t_0$ 年就乘了 $(t - t_0)/2$ 次 2。取對數可以把指數成長變成直線:

$$\log_2 N(t) = \log_2 N_0 + \frac{t - t_0}{2}$$

所以在半對數座標(y 軸取 log)上畫實際晶片的電晶體數,若大致落在一條斜率 1/2 的直線上,就符合摩爾定律。反過來,用兩個資料點就能估計「實際的加倍週期」:

$$T = \frac{t_1 - t_0}{\log_2(N_1 / N_0)}$$

## 老師講解
### 例 1
Using the model $N(t) = 2300 \cdot 2^{(t-1971)/2}$ (the Intel 4004 had about 2,300 transistors in 1971), predict the transistor count in 1991, and compare with the Intel 80486 (1989, about 1.2 million transistors).

1. 1991 − 1971 = 20 年,加倍 20 / 2 = 10 次。
2. $N(1991) = 2300 \times 2^{10} = 2300 \times 1024 = 2{,}355{,}200$。
3. 同一個模型預測 1989 年:$2300 \times 2^{9} = 1{,}177{,}600$。
4. 實際 80486 約 1,200,000,和預測只差不到 2%——在 18 年、9 次加倍之後還這麼準,這就是摩爾定律驚人的地方。

### 例 2
Assign each machine to a hardware generation using this course's definition: UNIVAC I (1951), IBM 7090 (1959), Apollo Guidance Computer (1966), Intel 4004 (1971), ENIAC (1946).

1. 先記住四個起始年:1951、1959、1965、1971;邊界年份屬於新的世代,1951 之前算第 0 代(早期)。
2. UNIVAC I(1951)→ 第 1 代(真空管)。IBM 7090(1959)→ 第 2 代(電晶體化)。
3. Apollo Guidance Computer(1966)→ 第 3 代(使用積體電路)。Intel 4004(1971)→ 第 4 代(微處理器)。
4. ENIAC(1946)早於 1951 → 第 0 代(早期電子計算機)。
5. 提醒:「世代」是用來整理歷史的框架,真實機器的技術常跨世代;考試與 Lab 一律用上面的年份定義。

## 易錯點
- 邊界年份算錯:1959 是第 2 代,不是第 1 代。
- 以為摩爾定律是物理定律:它是**經驗觀察**,而且近年已經放慢。
- 把「每兩年加倍」誤算成「每兩年加 2 倍」或「每年加倍」。

## 教學提示
可以讓學生在半對數座標上畫出 Lab 資料集的 5 顆 CPU,看它們是否大致在一條直線上;這比背年份更有感。

## 練習
### 照做
Name the key switching technology of each of the four hardware generations.

#### 解答
第 1 代真空管;第 2 代電晶體;第 3 代積體電路;第 4 代 LSI/VLSI(微處理器)。

### 是非
True or false: Moore's law says that CPU clock speed doubles every two years.

#### 解答
False。摩爾定律講的是晶片上的**電晶體數**,不是時脈;時脈大約從 2005 年起就沒有大幅提升。

### 變化
Using $N(t) = 2300 \cdot 2^{(t-1971)/2}$, predict the transistor count in 2001.

#### 解答
2001 − 1971 = 30 年 → 加倍 15 次;$2300 \times 2^{15} = 2300 \times 32768 = 75{,}366{,}400$。

### 應用
A chip had 29,000 transistors in 1978 and one had 42,000,000 in 2000. Estimate the doubling period implied by these two data points.

#### 解答
$T = (2000 - 1978) / \log_2(42{,}000{,}000 / 29{,}000) = 22 / \log_2(1448.3) \approx 22 / 10.50 \approx 2.10$ 年,和「約兩年」一致。

### 挑戰
If transistor counts double every 2 years, how many years does it take to grow by a factor of 1,000,000? Explain why exponential growth makes long-term predictions fragile.

#### 解答
$10^6 \approx 2^{19.93}$,需要約 19.93 次加倍 ≈ 39.9 年。指數模型對加倍週期非常敏感:若實際週期是 2.5 年而不是 2 年,同樣 40 年只會成長 $2^{16} \approx 65{,}536$ 倍,差了 15 倍左右。所以長期預測只要參數差一點點,結果就差很多。

## 驗算
```check
2300 * 2**10 == 2355200
2300 * 2**15 == 75366400
round(22 / math.log2(42000000 / 29000), 2) == 2.10
round(2 * math.log2(10**6), 1) == 39.9
```
