---
id: C2.6
title_en: Binary Values and Computers
title_zh: 二進位與電腦
sub: Bits, bytes, words — and what n bits can represent
level: basic
lab_hook: "任務 6:`bits_needed()`、`max_unsigned()`"
---
## 觀念
Computers use binary because their basic components have two stable states (for example, a voltage is high or low). A **binary digit** is called a **bit**.

- A **byte** is 8 bits. A **nibble** is 4 bits.
- A **word** is the group of bits a particular CPU handles as a unit; its size (for example 32 or 64 bits) is the **word length**.

With $n$ bits we can represent $2^n$ different patterns. Interpreted as an **unsigned** integer, they range from $0$ to $2^n - 1$. Conversely, to give a distinct pattern to each of $k$ things we need at least $\lceil \log_2 k \rceil$ bits, and to write a number $N > 0$ in binary we need $\lfloor \log_2 N \rfloor + 1$ bits.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| bit | 位元 | binary digit,0 或 1 |
| byte | 位元組 | 8 個位元 |
| word | 字組 | CPU 一次處理的位元數,如 64 位元 |
| unsigned integer | 無號整數 | 沒有負數,範圍 $0$ 到 $2^n-1$ |
| KB / KiB | 千位元組 | KB = 1000 位元組(SI);KiB = 1024 位元組(二進位前綴) |

## 白話說
一個位元只能說「是/否」;兩個位元可以說 4 種話(00、01、10、11);每多一個位元,能說的話就**加倍**。所以 8 位元 = 256 種,32 位元約 43 億種,64 位元約 $1.8 \times 10^{19}$ 種。

反過來問「要表示 k 種東西要幾個位元?」就是問「2 的幾次方才 ≥ k」。表示 26 個英文字母要 5 位元($2^5 = 32 \ge 26$,但 $2^4 = 16$ 不夠)。

## 後面會用到
- **計算機組織**:暫存器寬度、位址匯流排寬度決定了可定址的記憶體大小(32 位元位址最多 4 GiB)。
- **資料結構**:用幾個位元存狀態(bit set、bitmask)。
- 本課第 3 章:負數、浮點數、字元、顏色都建立在「n 位元有 $2^n$ 種」上。

## 現代補充
容量單位有兩套:**SI 前綴**(KB = 1000、MB = $10^6$、GB = $10^9$)與 **IEC 二進位前綴**(KiB = 1024、MiB = $2^{20}$、GiB = $2^{30}$)。硬碟廠商用 GB,作業系統常用 GiB,所以「1 TB」的硬碟在電腦上顯示約「931 GiB」——不是被偷了容量。

## 原理
**為什麼 $n$ 位元剛好 $2^n$ 種?** 每一位獨立地有 2 種選擇,$n$ 位就是 $2 \times 2 \times \cdots \times 2 = 2^n$(乘法原理)。

**為什麼表示 $N$ 需要 $\lfloor \log_2 N \rfloor + 1$ 位?** 若 $N$ 需要恰好 $m$ 位(最高位是 1),則 $2^{m-1} \le N \le 2^m - 1 < 2^m$。取對數得 $m - 1 \le \log_2 N < m$,所以 $m = \lfloor \log_2 N \rfloor + 1$。$N = 0$ 時通常也寫成 1 位(`0`)。

## 老師講解
### 例 1
How many different values can a 16-bit unsigned integer hold, and what is its largest value? How many bits are needed to give each of 1000 students a distinct ID?

1. 16 位元 → $2^{16} = 65{,}536$ 種值。
2. 無號整數從 0 開始,所以最大值是 $2^{16} - 1 = 65{,}535$。
3. 1000 個學生:找最小的 $n$ 使 $2^n \ge 1000$。$2^9 = 512$ 不夠,$2^{10} = 1024$ 夠。
4. 需要 **10 位元**。等價地,$\lceil \log_2 1000 \rceil = \lceil 9.97 \rceil = 10$。

### 例 2
A disk is sold as 1 TB. How many GiB does the operating system report?

1. 1 TB(SI)$= 10^{12}$ 位元組。
2. 1 GiB $= 2^{30} = 1{,}073{,}741{,}824$ 位元組。
3. $10^{12} / 2^{30} \approx 931.32$。
4. 所以作業系統顯示約 931 GiB。兩個數字都對,只是單位不同。

## 易錯點
- 把「$n$ 位元有 $2^n$ 種」和「最大值 $2^n$」混淆:最大值是 $2^n - 1$。
- 表示 k 種東西用 $\log_2 k$ 但忘了**無條件進位**。
- KB 與 KiB 混用。

## 教學提示
可以問學生「IPv4 位址是 32 位元,全世界最多幾個位址?」($2^{32} \approx 43$ 億,不夠用 → IPv6)。Lab 任務 6 的隱藏測試檢查 `max_unsigned(64)`:在 C 裡 `1 << 64` 是未定義行為,這是很好的機會提到 UBSan。

## 練習
### 照做
What is the largest unsigned value that fits in 12 bits?

#### 解答
$2^{12} - 1 = 4095$。

### 是非
True or false: To represent the 26 letters of the English alphabet, 4 bits are enough.

#### 解答
False。$2^4 = 16 < 26$;需要 5 位元($2^5 = 32$)。

### 變化
How many bits are needed to write $1000_{10}$ in binary? Check by converting.

#### 解答
$\lfloor \log_2 1000 \rfloor + 1 = 9 + 1 = 10$ 位。$1000 = 1111101000_2$,確實 10 位。

### 應用
A 32-bit address can refer to one byte per address. What is the maximum amount of memory, in GiB, that it can address?

#### 解答
$2^{32}$ 位元組 $= 4 \times 2^{30}$ = 4 GiB。

### 挑戰
Explain why `(uint64_t)1 << 64` is a bug in C even though you only want $2^{64} - 1$, and give a correct way to compute the maximum 64-bit unsigned value.

#### 解答
C 標準規定移位量必須小於型別的位元數,移 64 位是未定義行為(在 x86 上常常實際只移 0 位,得到 1)。正確做法:直接用 `UINT64_MAX`,或 `~(uint64_t)0`,或寫成 `bits == 64 ? UINT64_MAX : ((uint64_t)1 << bits) - 1`。

## 驗算
```check
2**16 == 65536 and 2**12 - 1 == 4095
bits_for(1000) == 10 and bits_for(26) == 5
len(to_base(1000, 2)) == 10
round(10**12 / 2**30, 2) == 931.32
2**32 // 2**30 == 4
```
