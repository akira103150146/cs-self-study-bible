---
id: C3.4
title_en: Representing Real Numbers
title_zh: 實數的表示(浮點數)
sub: Sign, exponent, and fraction — IEEE 754 single precision
level: hard
lab_hook: "任務 3:`f32_decode()`、`f32_encode()`、`f32_binary_sci()`"
---
## 觀念
A real number has a whole part and a fractional part separated by a **radix point**. Computers store reals in **floating-point** form, like scientific notation: $\text{sign} \times \text{mantissa} \times \text{base}^{\text{exponent}}$. In binary, every nonzero number can be **normalized** to $\pm 1.xxxx_2 \times 2^{e}$.

**IEEE 754 single precision** (32 bits, C `float`) has three fields:

| Field | Bits | Meaning |
|---|---|---|
| sign $s$ | 1 | 0 = positive, 1 = negative |
| exponent $E$ | 8 | stored with a **bias** of 127: actual exponent $e = E - 127$ |
| fraction $F$ | 23 | the bits after the radix point; the leading 1 is **implicit** (hidden bit) |

Value of a **normal** number ($1 \le E \le 254$): $(-1)^s \times 1.F_2 \times 2^{E - 127}$.

Special cases:

| $E$ | $F$ | Meaning |
|---|---|---|
| 0 | 0 | $\pm 0$ (there are two zeros) |
| 0 | ≠ 0 | **denormal** (subnormal): $(-1)^s \times 0.F_2 \times 2^{-126}$ — tiny numbers near 0 |
| 255 | 0 | $\pm\infty$ |
| 255 | ≠ 0 | **NaN** (not a number), e.g. $0/0$ |

Double precision (64 bits, C `double`) uses 1 + 11 + 52 bits with bias 1023.

![The three fields of −6.25 in IEEE 754 single precision.](ieee754-fields.svg)

Because only 23 fraction bits are stored, most decimal fractions (such as 0.1) are **rounded** to the nearest representable value, and results like `0.1 + 0.2 == 0.3` can be false.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| floating point | 浮點數 | 小數點位置由指數決定的實數表示 |
| normalized | 正規化 | 寫成 $1.xxx \times 2^e$,首位固定是 1 |
| sign / exponent / fraction | 符號/指數/尾數 | IEEE 754 的三個欄位(fraction 也常稱 mantissa) |
| bias | 偏移量 | 指數存成 $e + 127$,讓欄位永遠是非負數 |
| hidden bit | 隱藏位元 | 正規化後首位的 1 不存,省下一個位元 |
| denormal / subnormal | 非正規數 | 指數欄為 0,用來表示非常接近 0 的數 |
| NaN | 非數值 | 無意義的結果,例如 0/0、sqrt(−1) |
| rounding error | 捨入誤差 | 無法精確表示時,取最接近的可表示值造成的誤差 |

## 白話說
浮點數就是**二進位的科學記號**:$-6.25 = -1.1001_2 \times 2^2$。IEEE 754 把它拆成三格存:符號(1 位)、指數(8 位,存成 $2 + 127 = 129$)、小數點後的位元(23 位,前面那個 1 不用存,因為正規化後一定是 1)。

指數要加 127 才存,是為了讓指數欄是無號數,比大小比較方便。全 0 與全 1 的指數被保留下來表示特殊值:零、非常小的數、無限大、NaN。

## 後面會用到
- **計算機組織**:浮點運算單元(FPU)、單精度與倍精度的效能差異。
- **數值方法**、**機器學習**:捨入誤差、累加誤差、為什麼 GPU 訓練模型可以用 16 位元浮點數(第 18 章會做浮點誤差實驗)。
- **程式設計**:永遠不要用 `==` 比較兩個浮點數,要比較差是否小於某個容許值。

## 現代補充
AI 加速器大量使用更短的浮點格式:**FP16**(1 + 5 + 10)、**bfloat16**(1 + 8 + 7,指數範圍和 float 相同但精度低)、甚至 **FP8**。原理和本節完全相同,只是欄位寬度不同——學會拆 float,就會拆它們。

## 原理
**為什麼要偏移量而不是二補數?** 用偏移量存指數,兩個同號浮點數的大小順序,剛好等於把它們的 32 位元當成無號整數比大小的順序(因為指數在高位、尾數在低位,而且都是無號的)。硬體比較浮點數就能直接用整數比較器。

**非正規數解決了什麼?** 最小的正規數是 $1.0 \times 2^{-126}$。若沒有非正規數,0 和它之間是一個大洞,$x - y = 0$ 卻可能 $x \ne y$。非正規數把指數固定在 $-126$、首位改成 0,填滿這個洞(代價是精度逐漸降低,稱為 gradual underflow)。

**精度有多少?** 23 個尾數位元加上隱藏位元是 24 位有效二進位數字,約 $24 \log_{10} 2 \approx 7.2$ 位十進位有效數字。`double` 是 53 位,約 15.9 位。

## 老師講解
### 例 1
Encode $-6.25$ in IEEE 754 single precision.

1. **轉二進位**:$6 = 110_2$,$0.25 = 0.01_2$,所以 $6.25 = 110.01_2$。
2. **正規化**:$110.01_2 = 1.1001_2 \times 2^2$。
3. **三個欄位**:符號 $s = 1$(負);指數 $E = 2 + 127 = 129 = 10000001_2$;尾數取小數點後的位元 $1001$,右邊補 0 到 23 位。
4. 組合:`1 10000001 10010000000000000000000`。
5. 寫成十六進位:`1100 0000 1100 1000 0000 …` → `0xC0C80000`。

### 例 2
Decode the single-precision patterns `0x3F400000` and `0x00000001`.

1. `0x3F400000` = `0 01111110 10000000000000000000000`。
2. 符號 0;$E = 126$ → $e = -1$;尾數 $1.1_2 = 1.5$。值 $= 1.5 \times 2^{-1} = 0.75$。
3. `0x00000001` = `0 00000000 00000000000000000000001`:$E = 0$ 且 $F \ne 0$ → **非正規數**。
4. 值 $= 0.F_2 \times 2^{-126} = 2^{-23} \times 2^{-126} = 2^{-149} \approx 1.4 \times 10^{-45}$——這是 float 能表示的最小正數。

## 易錯點
- 忘了加偏移量 127,或解碼時忘了減。
- 把隱藏位元也存進尾數欄(多存一個 1,後面全部錯一位)。
- 以為非正規數的指數是 $0 - 127 = -127$:規定是 $-126$。
- 以為 NaN 等於 NaN:`NaN == NaN` 是 false。

## 教學提示
例 1 的每一步都要寫出來;學生最常錯在正規化時小數點移動的方向。可以在 Python 用 `struct.pack('>f', x).hex()` 當場驗證。Lab 任務 3 的 `floatdump` 工具正好讓學生自己探索各種特殊值。

## 練習
### 照做
Encode $5.0$ in IEEE 754 single precision (give the 32 bits).

#### 解答
$5 = 101_2 = 1.01_2 \times 2^2$;$s = 0$、$E = 129$ = `10000001`、尾數 `01` 補零 → `0 10000001 01000000000000000000000`(`0x40A00000`)。

### 是非
True or false: In IEEE 754 single precision, the exponent field `11111111` with a nonzero fraction represents infinity.

#### 解答
False。指數全 1、尾數非 0 是 NaN;尾數為 0 才是無限大。

### 變化
Decode `0xC1200000`.

#### 解答
`1 10000010 01000000000000000000000`:負號;$E = 130$ → $e = 3$;$1.01_2 = 1.25$;值 $= -1.25 \times 8 = -10.0$。

### 應用
Why does `0.1f + 0.2f == 0.3f` in C not necessarily hold, even though each is written exactly in the source code?

#### 解答
0.1、0.2、0.3 在二進位都是無限循環小數,存成 float 時各自被捨入到最接近的可表示值;兩個近似值相加再捨入一次,不一定剛好等於 0.3 的近似值。(在 float 下這個例子剛好相等,在 double 下不相等——所以不要依賴 `==`。)

### 挑戰
What is the largest finite single-precision value? Give its bit pattern in hexadecimal and its value as a power expression.

#### 解答
指數欄最大的非特殊值是 254($e = 127$),尾數全 1:`0 11111110 111…1` = `0x7F7FFFFF`,值 $= (2 - 2^{-23}) \times 2^{127} \approx 3.4028 \times 10^{38}$。

## 驗算
```check
f32_bits(-6.25) == "1" + "10000001" + "1001" + "0" * 19
format(int(f32_bits(-6.25), 2), "08X") == "C0C80000"
f32_from_bits(format(0x3F400000, "032b")) == 0.75
f32_from_bits("0" * 31 + "1") == 2.0 ** -149
f32_bits(5.0) == format(0x40A00000, "032b")
f32_from_bits(format(0xC1200000, "032b")) == -10.0
f32_from_bits(format(0x7F7FFFFF, "032b")) == (2 - 2**-23) * 2.0**127
round(24 * math.log10(2), 1) == 7.2
```
