---
id: C3.3
title_en: Overflow
title_zh: 溢位
sub: When the true result does not fit in n bits
level: mid
lab_hook: "任務 2:`add_overflows()`、`wrap_add()`"
---
## 觀念
**Overflow** occurs when the value we compute cannot fit into the number of bits we have allocated for the result.

- For **unsigned** addition, overflow shows up as a **carry out** of the leftmost bit: in 8 bits, $200 + 100 = 300 > 255$, and the stored result is $300 - 256 = 44$.
- For **two's complement** (signed) addition, the carry out is **not** the test. Overflow happens exactly when **two numbers of the same sign produce a result of the opposite sign**: positive + positive → negative, or negative + negative → positive. Adding numbers of opposite signs can never overflow.

When overflow happens in fixed-width hardware, the result **wraps around** modulo $2^n$: in 8-bit two's complement, $127 + 1$ becomes $-128$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| overflow | 溢位 | 正確結果超出 n 位元的表示範圍 |
| carry out | 最高位進位 | 最左邊一位相加後產生的進位 |
| wrap around | 繞回 | 超出範圍後從另一端重新開始(模 $2^n$) |
| undefined behavior (UB) | 未定義行為 | C 標準沒有規定結果,編譯器可以任意處理 |
| overflow flag (V) | 溢位旗標 | CPU 記錄有號加法是否溢位的位元 |

## 白話說
里程表是 999999 時再開 1 公里,會變成 000000——這就是繞回。對無號數來說,「有進位跑出去」就是溢位。

有號數比較狡猾:$-1 + 1$(`11111111 + 00000001`)也會有進位跑出去,但答案 0 是對的。真正的判斷是「兩個正數加起來變負數」或「兩個負數加起來變正數」——結果的符號不合理,才是溢位。

## 後面會用到
- **計算機組織**:CPU 有兩個旗標:C(進位,給無號數看)與 V(溢位,給有號數看);第 4 章的 ALU 要算出這兩個旗標。
- **程式設計**:C 的**有號**整數溢位是未定義行為(編譯器可能據此把你的 `if` 優化掉),**無號**整數則保證繞回。
- **資訊安全**:整數溢位造成配置的緩衝區太小,是經典漏洞(第 17、18 章)。

## 現代補充
- 編譯時加 `-fsanitize=undefined`,有號溢位會在執行時被抓到(本課 Lab 預設就開)。
- GCC/Clang 提供 `__builtin_add_overflow(a, b, &r)`,C23 標準化為 `ckd_add`,可以安全地檢查。
- Rust 在除錯模式下溢位直接中止程式;Python 的整數沒有位數上限,所以不會溢位(但 NumPy 的陣列會)。

## 原理
**為什麼「同號相加得異號」恰好是溢位?** 設 $a, b$ 都在 $[-2^{n-1}, 2^{n-1}-1]$。

- 若一正一負,$a + b$ 介於兩者之間,一定在範圍內,不會溢位。
- 若兩者都 ≥ 0,真實和在 $[0, 2^n - 2]$。溢位 ⇔ 和 ≥ $2^{n-1}$,而此時繞回後的位元樣子最高位是 1,被讀成負數。
- 若兩者都 < 0,真實和在 $[-2^n, -2]$。溢位 ⇔ 和 < $-2^{n-1}$,加上 $2^n$ 繞回後落在 $[0, 2^{n-1}-1]$,被讀成非負數。

等價的硬體判斷:**進入最高位的進位 ≠ 離開最高位的進位**,即 $V = c_{n-1} \oplus c_n$。

## 老師講解
### 例 1
In 8-bit two's complement, compute $100 + 50$ and $-100 + (-50)$. Do they overflow? What values are stored?

1. 範圍是 $-128$ 到 $127$。
2. $100 + 50 = 150 > 127$ → **溢位**。位元:`01100100 + 00110010 = 10010110`,最高位是 1,被讀成 $150 - 256 = -106$。兩正得負,符合判斷規則。
3. $-100 + (-50) = -150 < -128$ → **溢位**。`10011100 + 11001110 = 1 01101010`,丟掉進位得 `01101010` = 106。兩負得正。
4. 結論:硬體照樣算出一個位元樣子,但它的意義錯了;程式必須自己檢查(或靠 V 旗標)。

### 例 2
For each 8-bit addition, decide whether (a) unsigned overflow (carry out) and (b) signed overflow occur: `11111111 + 00000001`, `01111111 + 00000001`.

1. `11111111 + 00000001 = 1 00000000`:最高位有進位出去 → **無號溢位**(255 + 1 = 256 > 255)。
2. 有號解讀:$-1 + 1 = 0$,結果正確 → **沒有有號溢位**(一負一正相加不可能溢位)。
3. `01111111 + 00000001 = 10000000`:沒有進位出去 → **沒有無號溢位**(127 + 1 = 128 ≤ 255)。
4. 有號解讀:$127 + 1$ 得到 −128,兩正得負 → **有號溢位**。
5. 同一組位元,無號與有號的溢位判斷完全不同——這就是 CPU 需要 C、V 兩個旗標的原因。

## 易錯點
- 用「最高位有進位」判斷有號溢位:錯,`-1 + 1` 就是反例。
- 以為一正一負相加可能溢位:不可能。
- 以為 C 裡 `INT_MAX + 1` 一定等於 `INT_MIN`:有號溢位是未定義行為,不能依賴。

## 教學提示
例 2 是這個觀念最好的考題,也是 C 與 V 旗標的動機。Lab 任務 2 的 `add_overflows()` 要學生用「同號相加得異號」實作,並用 `wrap_add()` 模擬繞回的結果。

## 練習
### 照做
Is there signed overflow when computing $64 + 64$ in 8-bit two's complement? What value is stored?

#### 解答
是,$128 > 127$;位元 `10000000`,被讀成 −128。

### 是非
True or false: Adding a positive and a negative two's complement number can never overflow.

#### 解答
True。結果一定介於兩個加數之間。

### 變化
In 4-bit two's complement, which of these overflow: $5 + 2$, $5 + 3$, $-8 + (-1)$, $-8 + 7$?

#### 解答
範圍 −8 到 7。$5+2 = 7$ 不溢位;$5+3 = 8$ 溢位(得 −8);$-8 + (-1) = -9$ 溢位(得 7);$-8 + 7 = -1$ 不溢位。

### 應用
A program stores a file size in a signed 32-bit integer. A file is 3,000,000,000 bytes. What goes wrong?

#### 解答
有號 32 位元最大 $2^{31} - 1 = 2{,}147{,}483{,}647$,3,000,000,000 超過範圍;存進去會繞回成負數($3{,}000{,}000{,}000 - 2^{32} = -1{,}294{,}967{,}296$),程式可能把檔案大小當成負值而出錯。

### 挑戰
Show that signed overflow in an $n$-bit addition happens if and only if the carry into the sign bit differs from the carry out of the sign bit.

#### 解答
設兩數的符號位 $a, b$,進入符號位的進位 $c_{in}$,結果符號位 $s = a \oplus b \oplus c_{in}$,出去的進位 $c_{out} = \text{maj}(a, b, c_{in})$。逐一檢查:$a = b = 0$ 時 $c_{out} = 0$,溢位 ⇔ $s = 1$ ⇔ $c_{in} = 1$ ⇔ $c_{in} \ne c_{out}$。$a = b = 1$ 時 $c_{out} = 1$,溢位 ⇔ $s = 0$ ⇔ $c_{in} = 0$ ⇔ $c_{in} \ne c_{out}$。$a \ne b$ 時不可能溢位,而 $c_{out} = c_{in}$。三種情況都相符。

## 驗算
```check
(100 + 50) - 256 == -106 and twos(-106, 8) == "10010110"
(-100 - 50) + 256 == 106
from_twos(format((127 + 1) % 256, "08b")) == -128
[(-8 <= a + b <= 7) for a, b in ((5, 2), (5, 3), (-8, -1), (-8, 7))] == [True, False, False, True]
3000000000 - 2**32 == -1294967296
```
