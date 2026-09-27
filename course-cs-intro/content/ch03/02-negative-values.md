---
id: C3.2
title_en: Representing Negative Values
title_zh: 負數的表示
sub: Sign-magnitude, one's complement, and two's complement
level: mid
lab_hook: "任務 2:`to_signmag()`、`to_ones()`、`to_twos()`、`from_twos()`、`sign_extend()`"
---
## 觀念
With a fixed number of bits $n$, there are three classic ways to include negative integers:

- **Sign-magnitude**: the leftmost bit is the sign (0 = +, 1 = −), the other $n-1$ bits are the magnitude. Range $-(2^{n-1}-1) \dots 2^{n-1}-1$. It has two zeros (+0 and −0), and addition needs special cases.
- **One's complement**: a negative number is formed by flipping every bit of its positive counterpart. Same range as sign-magnitude, and it also has two zeros.
- **Two's complement**: a negative number $-I$ is stored as $2^n - I$. Equivalently: **flip all the bits and add 1**. Range $-2^{n-1} \dots 2^{n-1}-1$ (one more negative value), only **one zero**, and ordinary binary addition works for signed numbers — just discard the carry out of the leftmost bit.

The book introduces the idea with **ten's complement** in decimal: with $k$ digits, $-I$ is represented by $10^k - I$ (for $k = 2$, $-3$ is stored as $97$, and $5 + 97 = 102$ → drop the carry → $02$). Two's complement is the same idea in base 2, and it is what every modern CPU uses.

**Sign extension**: to widen a two's complement number from $n$ bits to $m > n$ bits, copy the sign bit into the new high-order positions (`1011` in 4 bits = −5 becomes `11111011` in 8 bits).

![Sixteen 4-bit patterns arranged on a circle: adding 1 moves one step clockwise.](twos-ring.svg)

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| sign-magnitude | 符號大小表示法 | 最高位當符號,其餘是絕對值 |
| one's complement | 一補數 | 負數 = 正數逐位元反轉 |
| two's complement | 二補數 | 負數 = $2^n$ 減絕對值 = 反轉加一 |
| ten's complement | 十補數 | 十進位版的補數:$10^k - I$ |
| sign bit | 符號位元 | 最高位元;二補數中為 1 代表負數 |
| sign extension | 符號延伸 | 加寬位數時,把符號位元複製到新的高位 |

## 白話說
想像一個只有兩位數的里程表:從 00 倒退一格是 99。所以「99」可以當成 −1、「98」當 −2……這就是十補數。二補數完全一樣,只是在二進位:8 位元時,`11111111` 是 −1,`10000000` 是 −128。

二補數的好處是**加法器不用知道數字是正是負**:照一般二進位加法做,丟掉最左邊溢出的進位,答案自動就對。這讓 CPU 只需要一個加法器,減法就是「加上負數」。

## 後面會用到
- **計算機組織**:ALU 的加減法、旗標(N、Z、V、C)全部建立在二補數上(第 4 章的 ALU)。
- **程式設計**:C 的 `int8_t`、`int32_t` 都是二補數;`(int8_t)200` 為什麼是 −56。
- **資訊安全**:有號/無號混用造成的漏洞(例如長度檢查被負數繞過)。

## 原理
**為什麼「反轉加一」等於 $2^n - I$?** 反轉 $I$ 的每一位,等於 $(2^n - 1) - I$(因為 $I$ 加上它的反轉是 $n$ 個 1)。再加 1 就是 $2^n - I$。

**為什麼二補數加法可以直接用?** 在 $n$ 位元裡,所有運算都是模 $2^n$ 的。$-I$ 存成 $2^n - I$,而 $2^n - I \equiv -I \pmod{2^n}$。所以 $A + (-B)$ 存成 $A + 2^n - B \equiv A - B$,丟掉溢出的進位(就是減去 $2^n$)後,只要真正的結果在可表示範圍內,位元樣子就正確。

**為什麼符號延伸是對的?** 負數 $x$ 在 $n$ 位元是 $2^n + x$,在 $m$ 位元是 $2^m + x$。兩者相差 $2^m - 2^n$,正好是第 $n$ 到 $m-1$ 位全為 1 的值——也就是把符號位元 1 複製到新的高位。正數的符號位是 0,補 0 即可。

## 老師講解
### 例 1
Represent $-37$ in 8 bits using sign-magnitude, one's complement, and two's complement.

1. 先寫 $+37$:$37 = 32 + 4 + 1$ → `00100101`。
2. **符號大小**:符號位改成 1,其餘不變 → `10100101`。
3. **一補數**:全部反轉 → `11011010`。
4. **二補數**:一補數再加 1 → `11011011`。
5. 驗算二補數:$2^8 - 37 = 219 = 128 + 64 + 16 + 8 + 2 + 1$ → `11011011` ✓。

### 例 2
Compute $5 + (-3)$ and $-4 + (-2)$ using 4-bit two's complement, and convert `1010` to decimal.

1. $5$ = `0101`;$-3$:`0011` 反轉 `1100` 加 1 → `1101`。
2. `0101 + 1101 = 10010`,丟掉第 5 位的進位 → `0010` = 2 ✓。
3. $-4$ = `1100`,$-2$ = `1110`。`1100 + 1110 = 11010` → 丟掉進位 → `1010`。
4. **`1010` 的值**:最高位是 1 → 負數。反轉加一 `0101 + 1 = 0110` = 6,所以 `1010` = −6 ✓。
5. 另一種讀法:最高位的權重當成 $-2^{n-1}$:$-8 + 2 = -6$。

## 易錯點
- 以為二補數「只要反轉」:那是一補數,還要加 1。
- 以為 8 位元二補數最小是 −127:是 −128(`10000000`),而且它沒有對應的正數。
- 符號延伸時補 0:負數要補 1。
- 符號大小與一補數有 +0、−0 兩個零。

## 教學提示
用圓環圖(二補數的「里程表」)解釋溢位與「丟掉進位」,比公式直觀。可以現場在 C 裡印 `(int8_t)200`、`(uint8_t)-1`,讓學生看到位元沒變、解讀變了。

## 練習
### 照做
Write $-12$ in 8-bit two's complement.

#### 解答
$12$ = `00001100` → 反轉 `11110011` → 加 1 → `11110100`。

### 是非
True or false: In 8-bit two's complement, both `00000000` and `10000000` represent zero.

#### 解答
False。二補數只有一個零 `00000000`;`10000000` 是 −128。(有兩個零的是符號大小與一補數。)

### 變化
What decimal values do these 8-bit two's complement numbers represent: `11111111`, `10000001`, `01111111`?

#### 解答
−1、−127、127。

### 應用
A 4-bit two's complement value `1101` is loaded into an 8-bit register with sign extension. What is the 8-bit pattern, and what value does it represent?

#### 解答
`11111101`,仍然是 −3。

### 挑戰
Prove that for any $n$-bit pattern $b_{n-1} \dots b_0$, its two's complement value equals $-b_{n-1} 2^{n-1} + \sum_{i=0}^{n-2} b_i 2^i$.

#### 解答
若 $b_{n-1} = 0$,那是一般無號值,式子成立。若 $b_{n-1} = 1$,無號值是 $U = 2^{n-1} + R$($R$ 是其餘位的值),而二補數定義這個樣子代表 $U - 2^n = 2^{n-1} + R - 2^n = -2^{n-1} + R$,正是式子的值。

## 驗算
```check
signmag(-37, 8) == "10100101" and ones(-37, 8) == "11011010" and twos(-37, 8) == "11011011"
twos(-3, 4) == "1101" and from_twos("1010") == -6
twos(-12, 8) == "11110100"
[from_twos(s) for s in ("11111111", "10000001", "01111111")] == [-1, -127, 127]
twos(from_twos("1101"), 8) == "11111101"
(5 + (-3)) % 16 == int("0010", 2)
```
