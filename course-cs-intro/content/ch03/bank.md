---
chapter: 3
---
## Q1 · C3.1 · 計算 · basic · 3
How many bits are needed to give each month of the year a distinct code?

### 答案
`4`

### 詳解
12 個月:$2^3 = 8 < 12 \le 16 = 2^4$ → 4 位元。

### 驗算
```check
bits_for(12) == int(ANS)
```

## Q2 · C3.1 · 計算 · mid · 4
A system must assign a unique ID to each of 1,000,000 users. What is the minimum number of bits?

### 答案
`20`

### 詳解
$2^{19} = 524{,}288 < 10^6 \le 1{,}048{,}576 = 2^{20}$ → 20 位元。

### 驗算
```check
bits_for(10**6) == int(ANS)
```

## Q3 · C3.1 · 計算 · mid · 4
A 0–5 V signal is digitized with 3 bits (8 evenly spaced levels, level 0 = 0 V, level 7 = 5 V), rounding to the nearest level. Which level represents 1.9 V?

### 答案
`3`

### 詳解
步長 $5/7 \approx 0.714$ V;$1.9 / 0.714 \approx 2.66$ → 四捨五入第 3 級。

### 驗算
```check
math.floor(1.9 / (5 / 7) + 0.5) == int(ANS)
```

## Q4 · C3.1 · 計算 · hard · 5
With 12 bits, a 0–5 V range is split into $2^{12}$ evenly spaced levels (level 0 = 0 V, top level = 5 V). What is the step between adjacent levels, in millivolts, rounded to two decimal places?

### 答案
`1.22`

### 詳解
$2^{12} = 4096$ 級,相鄰級差 $5 / 4095 \approx 0.0012210$ V ≈ 1.22 mV。

### 驗算
```check
f"{5 / (2**12 - 1) * 1000:.2f}" == ANS
```

## Q5 · C3.1 · 選擇 · basic · 2
Why do computers store data digitally rather than as analog signals?

- A. Digital signals never lose any strength.
- B. Digital signals can be regenerated: a receiver only needs to recognize high or low and can send a fresh, clean pulse.
- C. Analog signals cannot represent numbers.
- D. Digital signals use less electricity in every case.

### 答案
B

### 詳解
數位訊號只要判斷是哪一個等級,就能再生;誤差不會累積。

### 迷思對照
- **A** 以為數位訊號不會衰減 → 回看 C3.1:所有訊號都會衰減,數位的優勢是能再生
- **C** 以為類比不能表示數 → 回看 C3.1:溫度計就是類比表示
- **D** 把能耗當成主要理由 → 回看 C3.1 的原理

## Q6 · C3.1 · 選擇 · mid · 3
With 7 bits you can represent how many distinct things?

- A. 7
- B. 14
- C. 127
- D. 128

### 答案
D

### 詳解
$2^7 = 128$(這正是 ASCII 的大小)。

### 迷思對照
- **A** 以為一個位元一種 → 回看 C3.1
- **B** 以為是 2 × 7 → 回看 C3.1:是乘法原理
- **C** 和無號最大值混淆 → 回看 C2.6

## Q7 · C3.1 · 選擇 · hard · 4
Adding one bit to a representation…

- A. adds one more thing it can represent
- B. doubles the number of things it can represent
- C. squares the number of things it can represent
- D. has no effect unless the value is negative

### 答案
B

### 詳解
$2^{n+1} = 2 \cdot 2^n$。

### 迷思對照
- **A** 以為線性成長 → 回看 C3.1:是指數成長
- **C** 平方是位元數加倍時才發生 → 回看 C3.1
- **D** 和符號位元混淆 → 回看 C3.2

## Q8 · C3.1 · 簡答 · mid · 5
Explain why making 1000 copies of a digital file gives an identical file, while making 1000 generations of copies of an analog tape does not.

### 答案
數位複製每次讀出位元(判斷 0/1)再寫出,只要判斷正確,位元完全相同,誤差不累積。類比複製是把連續訊號放大後錄下,每次都加入雜訊,而且無法區分雜訊與原訊號,誤差一代代累積。

### 詳解
關鍵字:再生、門檻判斷、誤差累積。

### 評分要點
- 說明數位的再生與門檻判斷(3 分)
- 說明類比的誤差累積(2 分)

## Q9 · C3.2 · 計算 · basic · 3
Write $-1$ in 8-bit two's complement.

### 答案
`11111111`

### 詳解
$2^8 - 1 = 255$ → 全部是 1。

### 驗算
```check
twos(-1, 8) == ANS
```

## Q10 · C3.2 · 計算 · basic · 3
Write $-100$ in 8-bit two's complement.

### 答案
`10011100`

### 詳解
$100$ = `01100100` → 反轉 `10011011` → 加 1 → `10011100`。

### 驗算
```check
twos(-100, 8) == ANS
```

## Q11 · C3.2 · 計算 · mid · 4
Write $-5$ in 4-bit sign-magnitude, one's complement, and two's complement, separated by commas without spaces.

### 答案
`1101,1010,1011`

### 詳解
$5$ = `0101`;符號大小 `1101`;一補數 `1010`;二補數 `1011`。

### 驗算
```check
",".join([signmag(-5, 4), ones(-5, 4), twos(-5, 4)]) == ANS
```

## Q12 · C3.2 · 計算 · mid · 4
What decimal value does the 8-bit two's complement pattern `11100111` represent?

### 答案
`-25`

### 詳解
反轉加一:`00011000 + 1 = 00011001` = 25 → −25。或 $-128 + 64 + 32 + 4 + 2 + 1 = -25$。

### 驗算
```check
from_twos("11100111") == int(ANS)
```

## Q13 · C3.2 · 計算 · mid · 4
What is the smallest (most negative) value of a 16-bit two's complement integer?

### 答案
`-32768`

### 詳解
$-2^{15} = -32768$,位元 `1000000000000000`。

### 驗算
```check
from_twos("1" + "0" * 15) == int(ANS) == -2**15
```

## Q14 · C3.2 · 計算 · mid · 4
Sign-extend the 4-bit two's complement value `1011` to 8 bits.

### 答案
`11111011`

### 詳解
符號位元 1 複製到新的 4 個高位;值仍是 −5。

### 驗算
```check
twos(from_twos("1011"), 8) == ANS
```

## Q15 · C3.2 · 計算 · hard · 5
Using 3-digit ten's complement (like the book's decimal illustration), how is $-42$ stored?

### 答案
`958`

### 詳解
$10^3 - 42 = 958$。驗算:$42 + 958 = 1000$ → 丟掉進位 → 000。

### 驗算
```check
10**3 - 42 == int(ANS)
```

## Q16 · C3.2 · 計算 · hard · 5
In 8-bit two's complement, compute $-50 + 20$ by adding the bit patterns. Give the resulting 8-bit pattern.

### 答案
`11100010`

### 詳解
$-50$ = `11001110`,$20$ = `00010100`,相加 `11100010` = −30。

### 驗算
```check
twos(-50 + 20, 8) == ANS and format((int(twos(-50, 8), 2) + 20) % 256, "08b") == ANS
```

## Q17 · C3.2 · 選擇 · basic · 2
How do you negate a two's complement number?

- A. Flip the sign bit only
- B. Flip all the bits
- C. Flip all the bits and add 1
- D. Subtract 1 and flip the sign bit

### 答案
C

### 詳解
$-I = 2^n - I = (\text{反轉}) + 1$。

### 迷思對照
- **A** 那是符號大小表示法 → 回看 C3.2
- **B** 那是一補數 → 回看 C3.2
- **D** 步驟錯誤 → 回看 C3.2 的原理

## Q18 · C3.2 · 選擇 · mid · 3
Which representation has exactly one representation of zero?

- A. Sign-magnitude
- B. One's complement
- C. Two's complement
- D. All three

### 答案
C

### 詳解
符號大小與一補數都有 +0、−0。

### 迷思對照
- **A** 忘了 `1000…0` 是 −0 → 回看 C3.2
- **B** 忘了 `1111…1` 是 −0 → 回看 C3.2
- **D** 以為三種都一樣 → 回看 C3.2

## Q19 · C3.2 · 選擇 · hard · 4
Why do CPUs use two's complement?

- A. It uses fewer bits than other representations.
- B. The same adder works for signed and unsigned numbers, subtraction is addition of the negation, and there is only one zero.
- C. It can represent more positive numbers.
- D. It makes multiplication unnecessary.

### 答案
B

### 詳解
所有運算都是模 $2^n$,加法器不用分辨正負。

### 迷思對照
- **A** 位數相同 → 回看 C3.2
- **C** 正數範圍和另兩種一樣,二補數多出的是一個負數 → 回看 C3.2
- **D** 和乘法無關 → 回看 C3.2 的原理

## Q20 · C3.2 · 簡答 · mid · 6
Explain why "flip all bits and add 1" gives $2^n - I$ for an $n$-bit value $I$.

### 答案
$I$ 加上它的逐位反轉,每一位都是 1,總和 $2^n - 1$。所以反轉 $= 2^n - 1 - I$,再加 1 就是 $2^n - I$。

### 詳解
這是二補數定義與演算法之間的橋樑。

### 評分要點
- 說出 $I$ + 反轉 = 全 1 = $2^n - 1$(4 分)
- 推出結論(2 分)

## Q21 · C3.2 · 簡答 · hard · 8
Prove that sign extension preserves the value of a negative two's complement number when widening from $n$ to $m$ bits.

### 答案
負數 $x$ 在 $n$ 位元存成 $2^n + x$,在 $m$ 位元應存成 $2^m + x$。兩者相差 $2^m - 2^n = 2^n (2^{m-n} - 1)$,正好是「第 $n$ 到 $m-1$ 位全是 1」的值。所以把符號位元 1 複製到新的高位,得到的位元樣子就是 $2^m + x$,值不變。

### 詳解
正數時符號位是 0,補 0 顯然不變。

### 評分要點
- 寫出兩種寬度下的儲存值(3 分)
- 算出差值並對應到新高位全 1(4 分)
- 提到正數的情況(1 分)

## Q22 · C3.3 · 計算 · basic · 3
In 8-bit two's complement, $120 + 10$ overflows. What value is actually stored (in decimal)?

### 答案
`-126`

### 詳解
$130 - 256 = -126$。

### 驗算
```check
from_twos(format(130 % 256, "08b")) == int(ANS)
```

## Q23 · C3.3 · 計算 · basic · 3
In 8-bit unsigned arithmetic, what is stored for $200 + 100$?

### 答案
`44`

### 詳解
$300 - 256 = 44$。

### 驗算
```check
(200 + 100) % 256 == int(ANS)
```

## Q24 · C3.3 · 計算 · mid · 4
In 8-bit two's complement, $-120 + (-10)$ overflows. What value is stored?

### 答案
`126`

### 詳解
$-130 + 256 = 126$。兩負得正。

### 驗算
```check
from_twos(format((-130) % 256, "08b")) == int(ANS)
```

## Q25 · C3.3 · 計算 · mid · 4
What is the largest value of a signed 32-bit integer?

### 答案
`2147483647`

### 詳解
$2^{31} - 1$。

### 驗算
```check
2**31 - 1 == int(ANS)
```

## Q26 · C3.3 · 計算 · mid · 4
On hardware that wraps around, what signed 32-bit value results from adding 1 to the largest signed 32-bit integer?

### 答案
`-2147483648`

### 詳解
繞回到最小值 $-2^{31}$。(在 C 語言裡這是未定義行為,硬體層級的結果才是繞回。)

### 驗算
```check
from_twos(format((2**31 - 1 + 1) % 2**32, "032b")) == int(ANS)
```

## Q27 · C3.3 · 計算 · mid · 4
In 4-bit two's complement, list which of these additions overflow, by their letters without spaces: (a) $3 + 4$, (b) $4 + 4$, (c) $-5 + (-4)$, (d) $-5 + 7$, (e) $-8 + (-1)$.

### 答案
`bce`

### 詳解
範圍 −8 到 7:(a) 7 ✓;(b) 8 溢位;(c) −9 溢位;(d) 2 ✓;(e) −9 溢位。

### 驗算
```check
"".join(k for k, (a, b) in zip("abcde", ((3, 4), (4, 4), (-5, -4), (-5, 7), (-8, -1))) if not -8 <= a + b <= 7) == ANS
```

## Q28 · C3.3 · 計算 · hard · 5
For the 8-bit addition `10000000 + 10000000`, give the carry out (0 or 1) and whether there is signed overflow (yes/no), as `carry,overflow`.

### 答案
`1,yes`

### 詳解
$128 + 128 = 256$ → 有進位出去;有號 $-128 + (-128) = -256$ → 溢位(兩負得 `00000000` = 0)。

### 驗算
```check
ANS == f"{(128 + 128) >> 8},{'yes' if not -128 <= -256 <= 127 else 'no'}"
```

## Q29 · C3.3 · 計算 · hard · 5
A signed 32-bit variable stores a file size of 3,000,000,000 bytes after wrap-around. What negative value does it hold?

### 答案
`-1294967296`

### 詳解
$3{,}000{,}000{,}000 - 2^{32} = -1{,}294{,}967{,}296$。

### 驗算
```check
3000000000 - 2**32 == int(ANS)
```

## Q30 · C3.3 · 選擇 · basic · 2
When can the addition of two two's complement numbers overflow?

- A. Only when the numbers have opposite signs
- B. Only when the numbers have the same sign and the result has the opposite sign
- C. Whenever there is a carry out of the leftmost bit
- D. Never, because two's complement wraps around

### 答案
B

### 詳解
一正一負不可能溢位;同號相加得異號才是溢位。

### 迷思對照
- **A** 剛好相反 → 回看 C3.3
- **C** 那是無號溢位的判斷 → 回看 C3.3 例 2
- **D** 繞回就是溢位的結果,不代表沒有溢位 → 回看 C3.3

## Q31 · C3.3 · 選擇 · mid · 3
In C, what does the language standard say about `INT_MAX + 1` (signed `int`)?

- A. It equals `INT_MIN`.
- B. It equals 0.
- C. It is undefined behavior.
- D. It is a compile-time error.

### 答案
C

### 詳解
有號整數溢位是未定義行為;編譯器可以假設它不會發生並據此優化。無號整數才保證繞回。

### 迷思對照
- **A** 把硬體行為當成語言保證 → 回看 C3.3 的易錯點
- **B** 沒有任何規則如此 → 回看 C3.3
- **D** 多數情況編譯器無法在編譯時發現 → 回看 C3.3 的現代補充

## Q32 · C3.3 · 選擇 · hard · 4
Which hardware condition exactly detects signed overflow in an $n$-bit addition?

- A. The carry out of the sign bit is 1.
- B. The carry into the sign bit differs from the carry out of the sign bit.
- C. The result's sign bit is 1.
- D. Both operands are negative.

### 答案
B

### 詳解
$V = c_{n-1} \oplus c_n$。

### 迷思對照
- **A** 那是無號溢位(C 旗標) → 回看 C3.3
- **C** 負的結果完全可能是正確的 → 回看 C3.3
- **D** 兩個負數相加也常常沒有溢位 → 回看 C3.3

## Q33 · C3.3 · 簡答 · mid · 6
The same 8-bit addition `11111111 + 00000001` overflows as unsigned but not as signed. Explain, and name the two CPU flags that report each case.

### 答案
無號:255 + 1 = 256 超出 0–255,有進位出去 → 溢位,由 C(carry)旗標報告。有號:−1 + 1 = 0 在範圍內 → 沒有溢位,V(overflow)旗標為 0。同一組位元,解讀不同,溢位的判斷就不同。

### 詳解
這是 CPU 需要兩個旗標的原因。

### 評分要點
- 無號解讀與結論(2 分)
- 有號解讀與結論(2 分)
- 正確說出 C 與 V 旗標(2 分)

## Q34 · C3.3 · 簡答 · hard · 8
A program checks `if (len + 100 < len) { error(); }` to detect overflow, where `len` is a signed `int`. Explain why a C compiler may remove this check entirely, and give a correct alternative.

### 答案
有號溢位是未定義行為,編譯器可以假設 `len + 100` 不會溢位,那麼 `len + 100 < len` 在數學上永遠為假,整個 `if` 就能刪掉。正確做法:事先比較 `if (len > INT_MAX - 100)`,或用 `__builtin_add_overflow(len, 100, &r)`(C23 的 `ckd_add`),或改用無號型別並檢查繞回。

### 詳解
這是真實漏洞中出現過的模式。

### 評分要點
- 說出「有號溢位是 UB,編譯器可假設不發生」(4 分)
- 給出一個正確的替代寫法(4 分)

## Q35 · C3.4 · 計算 · basic · 3
Give the IEEE 754 single-precision bit pattern of $1.0$ in hexadecimal (8 uppercase hex digits).

### 答案
`3F800000`

### 詳解
$1.0 = 1.0 \times 2^0$;$E = 127$ = `01111111`;尾數 0 → `0 01111111 000…` = `0x3F800000`。

### 驗算
```check
format(int(f32_bits(1.0), 2), "08X") == ANS
```

## Q36 · C3.4 · 計算 · mid · 4
Encode $12.5$ in single precision; give the hexadecimal pattern.

### 答案
`41480000`

### 詳解
$12.5 = 1100.1_2 = 1.1001_2 \times 2^3$;$E = 130$;尾數 `1001` → `0 10000010 1001000…` = `0x41480000`。

### 驗算
```check
format(int(f32_bits(12.5), 2), "08X") == ANS
```

## Q37 · C3.4 · 計算 · mid · 4
Encode $-0.375$ in single precision; give the hexadecimal pattern.

### 答案
`BEC00000`

### 詳解
$0.375 = 0.011_2 = 1.1_2 \times 2^{-2}$;$s = 1$、$E = 125$ = `01111101`、尾數 `1` → `1 01111101 1000…` = `0xBEC00000`。

### 驗算
```check
format(int(f32_bits(-0.375), 2), "08X") == ANS
```

## Q38 · C3.4 · 計算 · mid · 4
Decode the single-precision pattern `0x42280000`.

### 答案
`42.0`

### 詳解
`0 10000100 0101000…`:$E = 132$ → $e = 5$;$1.0101_2 = 1.3125$;$1.3125 \times 32 = 42$。

### 驗算
```check
f32_from_bits(format(0x42280000, "032b")) == float(ANS)
```

## Q39 · C3.4 · 計算 · mid · 4
What is the value of the exponent field (as a decimal number) when $3.75$ is stored in single precision?

### 答案
`128`

### 詳解
$3.75 = 11.11_2 = 1.111_2 \times 2^1$ → $E = 1 + 127 = 128$。

### 驗算
```check
f32_fields(3.75)[1] == int(ANS)
```

## Q40 · C3.4 · 計算 · hard · 5
$0.1$ stored in single precision becomes the pattern `0x3DCCCCCD`. What is the exponent field (decimal), and what actual power of 2 does it represent? Answer as `E,e`.

### 答案
`123,-4`

### 詳解
$0.1 = 1.6 \times 2^{-4}$;$E = -4 + 127 = 123$。尾數 `1001 1001 … 1101`(最後一位因捨入進位)。

### 驗算
```check
ANS == f"{f32_fields(0.1)[1]},{f32_fields(0.1)[1] - 127}"
```

## Q41 · C3.4 · 計算 · hard · 5
What is the smallest positive **normal** single-precision number, as a power of 2? Answer like `2^-10`.

### 答案
`2^-126`

### 詳解
最小的正規指數欄是 $E = 1$ → $e = -126$,尾數 0 → $1.0 \times 2^{-126}$。

### 驗算
```check
f32_from_bits("0" + "00000001" + "0" * 23) == 2.0 ** int(ANS.split("^")[1])
```

## Q42 · C3.4 · 計算 · hard · 6
How many single-precision values lie in $[1, 2)$? (Hint: count the possible fraction fields.)

### 答案
`8388608`

### 詳解
指數固定 $e = 0$,尾數 23 位元的每一種都是不同的值:$2^{23} = 8{,}388{,}608$ 個。

### 驗算
```check
2**23 == int(ANS)
```

## Q43 · C3.4 · 選擇 · basic · 2
What is the bias of the exponent in IEEE 754 single precision?

- A. 0
- B. 127
- C. 128
- D. 1023

### 答案
B

### 詳解
$e = E - 127$。

### 迷思對照
- **A** 以為指數直接存 → 回看 C3.4 的原理
- **C** 差一 → 回看 C3.4:$2^{7} - 1 = 127$
- **D** 那是倍精度 → 回看 C3.4

## Q44 · C3.4 · 選擇 · mid · 3
What does an exponent field of all 1s with a nonzero fraction represent?

- A. The largest finite number
- B. Infinity
- C. NaN
- D. A denormal number

### 答案
C

### 詳解
指數全 1:尾數 0 是無限大,非 0 是 NaN。

### 迷思對照
- **A** 最大有限數的指數欄是 254 → 回看 C3.4 的特殊值表
- **B** 無限大的尾數要是 0 → 回看 C3.4
- **D** 非正規數的指數欄是 0 → 回看 C3.4

## Q45 · C3.4 · 選擇 · hard · 4
Why is the leading 1 of a normalized number not stored?

- A. Because it is always 1, storing it would waste a bit; omitting it gives one extra bit of precision.
- B. Because the leading 1 is stored in the exponent.
- C. Because IEEE 754 only stores integers.
- D. Because it is 0 for negative numbers.

### 答案
A

### 詳解
正規化後首位一定是 1,不存可以多一位精度(24 位有效位元)。

### 迷思對照
- **B** 指數存的是次方 → 回看 C3.4
- **C** 浮點數就是為了存非整數 → 回看 C3.4
- **D** 負號由符號位元表示 → 回看 C3.4

## Q46 · C3.4 · 簡答 · mid · 6
Explain why `0.1 + 0.2 == 0.3` is false in Python (double precision), and how you should compare floating-point numbers instead.

### 答案
三個數在二進位都是無限循環小數,只能存最接近的近似值;$0.1$ 與 $0.2$ 的近似值相加再捨入,得到 $0.30000000000000004$,不等於 $0.3$ 的近似值。應該比較差的絕對值是否小於容許誤差,例如 `abs(a - b) < 1e-9`,或 `math.isclose(a, b)`。

### 詳解
不要用 `==` 比較浮點數。

### 評分要點
- 說明二進位無法精確表示(3 分)
- 給出正確的比較方式(3 分)

## Q47 · C3.4 · 簡答 · hard · 8
Explain what denormal (subnormal) numbers are, why IEEE 754 includes them, and what their value formula is in single precision.

### 答案
指數欄為 0、尾數非 0 的數。值 $= (-1)^s \times 0.F_2 \times 2^{-126}$(首位是 0、指數固定 −126)。它們填補 0 與最小正規數 $2^{-126}$ 之間的空隙,讓 $x - y = 0$ 若且唯若 $x = y$(gradual underflow);代價是越接近 0 精度越低。

### 詳解
沒有非正規數時,兩個不相等的極小數相減可能變成 0。

### 評分要點
- 定義與公式正確(4 分)
- 說明填補空隙/gradual underflow 的目的(4 分)

## Q48 · C3.5 · 計算 · basic · 3
Give the UTF-8 bytes (uppercase hex, space-separated) of the euro sign € (U+20AC).

### 答案
`E2 82 AC`

### 詳解
U+0800–FFFF → 3 位元組。`0010 0000 1010 1100` → `1110 0010`、`10 000010`、`10 101100` → E2 82 AC。

### 驗算
```check
utf8_hex("€") == ANS
```

## Q49 · C3.5 · 計算 · basic · 3
Give the UTF-8 bytes of ñ (U+00F1).

### 答案
`C3 B1`

### 詳解
11 位元 `00011 110001` → `110 00011`、`10 110001` → C3 B1。

### 驗算
```check
utf8_hex("ñ") == ANS
```

## Q50 · C3.5 · 計算 · mid · 4
Give the UTF-8 bytes of あ (U+3042).

### 答案
`E3 81 82`

### 詳解
`0011 000001 000010` → `1110 0011`、`10 000001`、`10 000010` → E3 81 82。

### 驗算
```check
utf8_hex("あ") == ANS
```

## Q51 · C3.5 · 計算 · mid · 4
Give the UTF-8 bytes of 🎉 (U+1F389).

### 答案
`F0 9F 8E 89`

### 詳解
21 位元 `000 011111 001110 001001` → F0、9F、8E、89。

### 驗算
```check
utf8_hex("🎉") == ANS
```

## Q52 · C3.5 · 計算 · mid · 4
Decode the UTF-8 bytes `E4 B8 AD` to a code point. Answer like `U+1234`.

### 答案
`U+4E2D`

### 詳解
`1110 0100`、`10 111000`、`10 101101` → `0100 111000 101101` = 0x4E2D(中)。

### 驗算
```check
f"U+{ord(bytes.fromhex('E4B8AD').decode('utf-8')):04X}" == ANS
```

## Q53 · C3.5 · 計算 · mid · 4
How many bytes does the UTF-8 encoding of the string `Hi, 世界!` take?

### 答案
`11`

### 詳解
ASCII 字元 H、i、逗號、空白、驚嘆號共 5 個,各 1 位元組;世、界各 3 位元組。總共 $5 + 6 = 11$。



### 驗算
```check
len("Hi, 世界!".encode("utf-8")) == int(ANS)
```

## Q54 · C3.5 · 計算 · hard · 5
What is the ASCII code of `'a'` XOR `0x20`, and which character is it?  Answer as `code,char`.

### 答案
`65,A`

### 詳解
0x61 XOR 0x20 = 0x41 = 65 = 'A'。

### 驗算
```check
ANS == f"{ord('a') ^ 0x20},{chr(ord('a') ^ 0x20)}"
```

## Q55 · C3.5 · 計算 · hard · 5
What is the largest code point that can be encoded in 3 UTF-8 bytes? Answer like `U+1234`.

### 答案
`U+FFFF`

### 詳解
3 位元組樣板有 $4 + 6 + 6 = 16$ 個 x,最大 $2^{16} - 1$ = 0xFFFF。

### 驗算
```check
int(ANS[2:], 16) == 2**16 - 1
```

## Q56 · C3.5 · 選擇 · basic · 2
How many characters does the ASCII character set contain?

- A. 64
- B. 128
- C. 256
- D. 65,536

### 答案
B

### 詳解
ASCII 是 7 位元,$2^7 = 128$。

### 迷思對照
- **A** 少一位 → 回看 C3.5
- **C** 那是 8 位元的延伸 ASCII(Latin-1) → 回看 C3.5
- **D** 那是 16 位元 → 回看 C3.5

## Q57 · C3.5 · 選擇 · mid · 3
Which byte sequence is **invalid** UTF-8?

- A. `41`
- B. `C3 A9`
- C. `C0 80`
- D. `E4 B8 AD`

### 答案
C

### 詳解
`C0 80` 是 U+0000 的過長編碼,必須拒絕。

### 迷思對照
- **A** `41` 是 'A',合法 → 回看 C3.5
- **B** `C3 A9` 是 é,合法 → 回看 C3.5
- **D** `E4 B8 AD` 是中,合法 → 回看 C3.5

## Q58 · C3.5 · 選擇 · hard · 4
What is the difference between Unicode and UTF-8?

- A. They are two names for the same thing.
- B. Unicode assigns code points to characters; UTF-8 is one way of encoding those code points as bytes.
- C. UTF-8 is an older version of Unicode.
- D. Unicode is for Chinese, UTF-8 is for English.

### 答案
B

### 詳解
字元集 vs 編碼方式;同一個 Unicode 字元可以用 UTF-8、UTF-16、UTF-32 編碼。

### 迷思對照
- **A** 混淆字元集與編碼 → 回看 C3.5
- **C** 不是版本關係 → 回看 C3.5
- **D** Unicode 涵蓋所有文字,UTF-8 可編碼所有 Unicode → 回看 C3.5

## Q59 · C3.5 · 簡答 · mid · 6
Explain what makes UTF-8 "self-synchronizing" and why that matters when a program starts reading in the middle of a byte stream.

### 答案
開頭位元組(`0`、`110`、`1110`、`11110`)和延續位元組(`10`)的高位樣子不同。從中間開始讀時,跳過 `10` 開頭的位元組,就能找到下一個字元的開頭,最多只會壞掉一個字元,不會整段錯位。

### 詳解
對照:若用固定長度的雙位元組編碼,錯一個位元組會讓後面全部錯位。

### 評分要點
- 說明開頭/延續位元組的區別(3 分)
- 說明如何重新對齊與好處(3 分)

## Q60 · C3.5 · 簡答 · hard · 8
Explain why a UTF-8 decoder must reject overlong encodings, using a concrete security example.

### 答案
若允許過長編碼,同一個字元就有多種位元組表示。例:`/`(U+002F)正規編碼是 `2F`,過長形式 `C0 AF`。一個檢查「路徑中不得含 `../`」的程式若只比對位元組 `2E 2E 2F`,就擋不住 `2E 2E C0 AF`;之後解碼器把它解成 `../`,攻擊者便能存取上層目錄。規定只接受最短形式,讓「比較位元組」等於「比較字元」。

### 詳解
這是 2000 年前後 IIS 等伺服器的真實漏洞類型。

### 評分要點
- 說明過長編碼造成多種表示(3 分)
- 給出具體的繞過例子(3 分)
- 說明「唯一表示」的好處(2 分)

## Q61 · C3.6 · 計算 · basic · 3
Encode `ABBBBBBBBBBBBC` with this course's RLE.

### 答案
`A*B9BBBC`

### 詳解
12 個 B:切成 9(`*B9`)+ 3(照原樣 `BBB`)。

### 驗算
```check
rle("ABBBBBBBBBBBBC") == ANS
```

## Q62 · C3.6 · 計算 · basic · 3
Encode `XXXXYYYZZZZZZZZZZ` with this course's RLE.

### 答案
`*X4YYY*Z9Z`

### 詳解
4 個 X → `*X4`;3 個 Y 照原樣;10 個 Z → `*Z9` + `Z`。

### 驗算
```check
rle("XXXXYYYZZZZZZZZZZ") == ANS
```

## Q63 · C3.6 · 計算 · mid · 4
What is the compression ratio (compressed ÷ original) of Q62? Round to two decimal places.

### 答案
`0.59`

### 詳解
$10 / 17 \approx 0.588$ → 0.59。

### 驗算
```check
f"{len(rle('XXXXYYYZZZZZZZZZZ')) / 17:.2f}" == ANS
```

## Q64 · C3.6 · 計算 · mid · 4
Decode the RLE string `Q*R5ST*U4`.

### 答案
`QRRRRRSTUUUU`

### 詳解
Q;`*R5` → RRRRR;S;T;`*U4` → UUUU。

### 驗算
```check
rle(ANS) == "Q*R5ST*U4"
```

## Q65 · C3.6 · 計算 · mid · 5
For frequencies a:10, b:5, c:3, d:1, e:1, what is the total number of bits of the Huffman encoding?

### 答案
`37`

### 詳解
合併:d+e = 2;2+c = 5;5(b)+5 = 10;10(a)+10 = 20。總位元 $2 + 5 + 10 + 20 = 37$。

### 驗算
```check
huffman_bits({"a": 10, "b": 5, "c": 3, "d": 1, "e": 1}) == int(ANS)
```

## Q66 · C3.6 · 計算 · mid · 5
Four symbols each appear once. What is the total length of the Huffman encoding, and how does it compare to a fixed-length code? Give just the Huffman total.

### 答案
`8`

### 詳解
頻率相同時 Huffman 退化成每個 2 位元:$4 \times 2 = 8$,和固定長度一樣。

### 驗算
```check
huffman_bits({"w": 1, "x": 1, "y": 1, "z": 1}) == int(ANS)
```

## Q67 · C3.6 · 計算 · hard · 6
A file has 100 characters with frequencies a:45, b:13, c:12, d:16, e:9, f:5. What is the total length of its Huffman encoding in bits?

### 答案
`224`

### 詳解
合併:f5+e9 = 14;c12+b13 = 25;14+d16 = 30;25+30 = 55;a45+55 = 100。總位元 $14 + 25 + 30 + 55 + 100 = 224$(固定長度 3 位元需 300)。

### 驗算
```check
huffman_bits(dict(zip("abcdef", [45, 13, 12, 16, 9, 5]))) == int(ANS)
```

## Q68 · C3.6 · 計算 · hard · 6
With the codes A = `0`, B = `10`, C = `110`, D = `111`, decode `1100101110`.

### 答案
`CABDA`

### 詳解
`110` C、`0` A、`10` B、`111` D、`0` A。

### 驗算
```check
"".join({"A": "0", "B": "10", "C": "110", "D": "111"}[ch] for ch in ANS) == "1100101110"
```

## Q69 · C3.6 · 選擇 · basic · 2
Which statement about lossless compression is correct?

- A. The original data can be recovered exactly.
- B. It always makes the file smaller.
- C. It is used only for images.
- D. It discards details people cannot notice.

### 答案
A

### 詳解
無損 = 可完全還原。

### 迷思對照
- **B** 隨機資料壓縮後可能變大 → 回看 C3.6 的應用練習
- **C** 文字與程式一定要無損 → 回看 C3.6
- **D** 那是有損壓縮 → 回看 C3.6

## Q70 · C3.6 · 選擇 · mid · 3
Why does this course's RLE leave runs shorter than 4 unencoded?

- A. Because the encoding `*` + char + count uses 3 characters, so shorter runs would not get smaller.
- B. Because runs shorter than 4 are illegal.
- C. Because the count must be at least 4 bits.
- D. Because Huffman handles them.

### 答案
A

### 詳解
3 個字元的碼只對 4 個以上的連續字元有利。

### 迷思對照
- **B** 並非不合法,只是不划算 → 回看 C3.6
- **C** 個數是一個數字字元,不是位元 → 回看 C3.6
- **D** RLE 本身獨立運作 → 回看 C3.6

## Q71 · C3.6 · 選擇 · hard · 4
Why can a Huffman-encoded bit stream be decoded without separators between codes?

- A. Because every code has the same length
- B. Because it is a prefix code: no code is a prefix of another
- C. Because the decoder knows the original text
- D. Because the most frequent symbol is always 0

### 答案
B

### 詳解
前綴性質讓解碼器走到葉子就能確定一個字元。

### 迷思對照
- **A** Huffman 碼是變長的 → 回看 C3.6
- **C** 解碼器只知道編碼表 → 回看 C3.6
- **D** 和可解碼性無關 → 回看 C3.6 的原理

## Q72 · C3.6 · 簡答 · mid · 6
Explain why the total length of a Huffman encoding equals the sum of the weights of all merged nodes.

### 答案
每次合併兩個節點,它們子樹裡所有字元的碼都多了一位;多出的總位元數正好是這兩個節點的頻率和(新節點的權重)。把每次合併的權重加起來,就是每個字元「頻率 × 深度」的總和。

### 詳解
這個公式讓計算總長不必畫出整棵樹。

### 評分要點
- 說明合併讓子樹中每個字元深度加一(3 分)
- 推出總和等於合併權重的總和(3 分)

## Q73 · C3.6 · 簡答 · hard · 8
Why does compressing a file of random bytes usually make it larger? Answer with a counting argument.

### 答案
長度 $n$ 位元的檔案有 $2^n$ 種,而長度小於 $n$ 位元的檔案總共只有 $2^n - 1$ 種。無損壓縮必須是一對一的,所以不可能把所有 $n$ 位元的檔案都變短;至少有些會變長或不變。隨機資料沒有可利用的重複或偏頗,平均來說壓不下去,再加上必須儲存的編碼表與檔頭,結果就變大。

### 詳解
這是「鴿籠原理」的應用。

### 評分要點
- 正確的計數論證(5 分)
- 提到額外的編碼表/檔頭成本(3 分)

## Q74 · C3.7 · 計算 · basic · 3
How many bytes does one minute of mono audio at 22,050 Hz and 16 bits take uncompressed?

### 答案
`2646000`

### 詳解
$22050 \times 2 \times 1 \times 60 = 2{,}646{,}000$。

### 驗算
```check
pcm_bytes(22050, 16, 1, 60) == int(ANS)
```

## Q75 · C3.7 · 計算 · mid · 4
What is the bit rate (in bits per second) of uncompressed stereo audio at 96 kHz and 24 bits?

### 答案
`4608000`

### 詳解
$96000 \times 24 \times 2 = 4{,}608{,}000$ bps。

### 驗算
```check
pcm_bytes(96000, 24, 2, 1) * 8 == int(ANS)
```

## Q76 · C3.7 · 計算 · mid · 4
A 3-minute song on an audio CD (44.1 kHz, 16-bit, stereo) takes how many bytes?

### 答案
`31752000`

### 詳解
$176400 \times 180 = 31{,}752{,}000$ 位元組。

### 驗算
```check
pcm_bytes(44100, 16, 2, 180) == int(ANS)
```

## Q77 · C3.7 · 計算 · hard · 5
A 30 kHz tone is sampled at 48 kHz. What frequency (in Hz) is heard on playback?

### 答案
`18000`

### 詳解
超過 $r/2 = 24$ kHz;與最近的 $r$ 的倍數(48 kHz)距離 $|30 - 48| = 18$ kHz。

### 驗算
```check
abs(30000 - 48000) == int(ANS)
```

## Q78 · C3.7 · 選擇 · basic · 2
To capture frequencies up to 20 kHz, the sampling rate must be …

- A. more than 10 kHz
- B. exactly 20 kHz
- C. more than 40 kHz
- D. more than 400 kHz

### 答案
C

### 詳解
Nyquist:大於最高頻率的兩倍。

### 迷思對照
- **A** 除以 2 了 → 回看 C3.7
- **B** 忘了乘 2 → 回看 C3.7
- **D** 多乘了 10 → 回看 C3.7

## Q79 · C3.7 · 選擇 · mid · 3
Increasing the bit depth from 8 to 16 bits mainly…

- A. allows higher frequencies to be recorded
- B. reduces quantization noise by about 48 dB
- C. halves the file size
- D. changes the sampling rate

### 答案
B

### 詳解
每多一位元約 6 dB,多 8 位元約 48 dB。能錄的頻率由取樣率決定。

### 迷思對照
- **A** 頻率由取樣率決定 → 回看 C3.7
- **C** 檔案會變兩倍大 → 回看 C3.7
- **D** 位元深度與取樣率無關 → 回看 C3.7

## Q80 · C3.7 · 選擇 · hard · 4
How does MP3 achieve roughly 10:1 compression?

- A. By lowering the sampling rate to 4 kHz
- B. By using a psychoacoustic model to discard sounds humans cannot perceive, then Huffman-coding the rest
- C. By storing only every tenth sample
- D. By converting stereo to mono

### 答案
B

### 詳解
有損:丟掉聽不到的(太高、太小聲、被遮蔽的),再用 Huffman 做無損壓縮。

### 迷思對照
- **A** 會嚴重失真 → 回看 C3.7
- **C** 會產生混疊 → 回看 C3.7
- **D** MP3 仍然是立體聲 → 回看 C3.7

## Q81 · C3.7 · 簡答 · mid · 6
Explain aliasing: what happens when a tone above half the sampling rate is sampled, and how recording equipment prevents it.

### 答案
高於 $r/2$ 的頻率取樣後,樣本和某個較低頻率(與最近的 $r$ 的倍數之差)完全相同,播放時聽到一個原本不存在的低頻音。錄音設備在取樣前用低通(抗混疊)濾波器把高於 $r/2$ 的頻率濾掉。

### 詳解
混疊不是「消失」,而是「冒充」。

### 評分要點
- 說明高頻被摺成低頻(3 分)
- 說明抗混疊濾波器(3 分)

## Q82 · C3.8 · 計算 · basic · 3
How many bytes does an uncompressed 4000 × 3000 true-color (24-bit) photo take?

### 答案
`36000000`

### 詳解
$4000 \times 3000 \times 3 = 36{,}000{,}000$(約 34.3 MiB)。

### 驗算
```check
image_bytes(4000, 3000, 24) == int(ANS)
```

## Q83 · C3.8 · 計算 · mid · 4
A 1024 × 768 image uses 256-color indexed mode with a palette of 256 entries × 4 bytes. How many bytes do the pixels plus palette take?

### 答案
`787456`

### 詳解
像素 $1024 \times 768 = 786{,}432$ 位元組;調色盤 $1024$ 位元組;共 $787{,}456$。

### 驗算
```check
image_bytes(1024, 768, 8) + 256 * 4 == int(ANS)
```

## Q84 · C3.8 · 計算 · mid · 4
Convert the pixel $(R, G, B) = (10, 200, 60)$ to grayscale with $Y = 0.299R + 0.587G + 0.114B$, rounded to the nearest integer.

### 答案
`127`

### 詳解
$2.99 + 117.4 + 6.84 = 127.23$ → 127。

### 驗算
```check
math.floor(0.299 * 10 + 0.587 * 200 + 0.114 * 60 + 0.5) == int(ANS)
```

## Q85 · C3.8 · 計算 · hard · 5
A 24-bit BMP is 5 pixels wide and 4 pixels tall. How many bytes is the pixel array, including row padding?

### 答案
`64`

### 詳解
每列 $5 \times 3 = 15$ 位元組,補到 16;$16 \times 4 = 64$。

### 驗算
```check
math.ceil(5 * 3 / 4) * 4 * 4 == int(ANS)
```

## Q86 · C3.8 · 選擇 · basic · 2
Which format is best for a screenshot of text?

- A. JPEG
- B. PNG
- C. MP3
- D. GIF with 16 colors

### 答案
B

### 詳解
無損、保留銳利邊緣。

### 迷思對照
- **A** 有損壓縮會在文字周圍產生雜點 → 回看 C3.8
- **C** MP3 是聲音格式 → 回看 C3.7
- **D** 顏色太少,反鋸齒的灰階會失真 → 回看 C3.8

## Q87 · C3.8 · 選擇 · mid · 3
What is the main advantage of vector graphics over raster images?

- A. They are always smaller.
- B. They can be scaled to any size without becoming blocky.
- C. They are better for photographs.
- D. They do not need colors.

### 答案
B

### 詳解
向量圖存的是形狀描述,縮放時重新繪製。

### 迷思對照
- **A** 複雜影像畫成向量反而更大 → 回看 C3.8
- **C** 照片適合點陣 → 回看 C3.8
- **D** 向量圖一樣有顏色 → 回看 C3.8

## Q88 · C3.8 · 選擇 · hard · 4
A program reads a 24-bit BMP and the picture appears upside down with red and blue swapped. What two facts about BMP did it ignore?

- A. BMP is compressed with JPEG and uses CMYK.
- B. Rows are stored bottom-up, and pixels are stored in B, G, R order.
- C. BMP uses big-endian integers and 16-bit color.
- D. BMP stores only grayscale.

### 答案
B

### 詳解
由下而上的列、BGR 的順序。

### 迷思對照
- **A** 24 位元 BMP 通常未壓縮、用 RGB 色彩模型 → 回看 C3.8
- **C** BMP 是小端序 → 回看 C3.10
- **D** BMP 支援全彩 → 回看 C3.8

## Q89 · C3.8 · 簡答 · mid · 6
Explain the trade-off of indexed color: how it saves space, and what happens to an image with more colors than the palette holds.

### 答案
每個像素只存調色盤的編號(例如 8 位元而非 24 位元),空間約省 2/3,只多一個小調色盤。若影像顏色超過調色盤容量,必須用最接近的顏色代替,產生色帶(banding);可用抖色(dithering)以相鄰像素混合模擬缺少的顏色。

### 詳解
GIF 就是索引色格式。

### 評分要點
- 說明省空間的原理(3 分)
- 說明顏色不足時的結果與對策(3 分)

## Q90 · C3.9 · 計算 · basic · 3
How many bytes per second does uncompressed 720p video (1280 × 720, 24-bit, 24 fps) need?

### 答案
`66355200`

### 詳解
$1280 \times 720 \times 3 \times 24 = 66{,}355{,}200$。

### 驗算
```check
1280 * 720 * 3 * 24 == int(ANS)
```

## Q91 · C3.9 · 計算 · mid · 4
How many bytes per second does uncompressed 4K video (3840 × 2160, 24-bit, 60 fps) need?

### 答案
`1492992000`

### 詳解
$3840 \times 2160 \times 3 \times 60 = 1{,}492{,}992{,}000$ ≈ 1.39 GiB/s。

### 驗算
```check
3840 * 2160 * 3 * 60 == int(ANS)
```

## Q92 · C3.9 · 計算 · mid · 5
A 200 × 100 grayscale video (1 byte/pixel) has a key frame every 8 frames; each delta frame records 400 changed pixels at 3 bytes each. What is the average size per frame in bytes?

### 答案
`3550`

### 詳解
關鍵影格 20,000;差異影格 1,200;每 8 格 $20000 + 7 \times 1200 = 28{,}400$;平均 3,550。

### 驗算
```check
(200 * 100 + 7 * 400 * 3) / 8 == int(ANS)
```

## Q93 · C3.9 · 計算 · hard · 5
A 1080p stream (1920 × 1080, 24-bit, 30 fps) is delivered at 8 Mbps. What is its compression ratio (compressed ÷ original)? Round to four decimal places.

### 答案
`0.0054`

### 詳解
原始 $186{,}624{,}000$ 位元組/秒 = $1{,}492{,}992{,}000$ bps;$8 \times 10^6 / 1.492992 \times 10^9 \approx 0.00536$。

### 驗算
```check
f"{8e6 / (1920 * 1080 * 24 * 30):.4f}" == ANS
```

## Q94 · C3.9 · 選擇 · basic · 2
What is stored in a delta frame?

- A. The complete image
- B. Only the differences from the previous frame
- C. Only the audio track
- D. A lower-resolution copy of the key frame

### 答案
B

### 詳解
差異影格只記錄改變的部分。

### 迷思對照
- **A** 那是關鍵影格 → 回看 C3.9
- **C** 影格是影像 → 回看 C3.9
- **D** 和縮圖混淆 → 回看 C3.9

## Q95 · C3.9 · 選擇 · mid · 3
Why do video codecs insert key frames regularly instead of storing only one at the start?

- A. Key frames are smaller than delta frames.
- B. So playback can start or seek anywhere without decoding from the beginning, and errors do not propagate forever.
- C. Because the human eye needs full frames.
- D. Because delta frames cannot represent color.

### 答案
B

### 詳解
定期的關鍵影格限制了隨機存取的成本與錯誤傳播的範圍。

### 迷思對照
- **A** 通常相反 → 回看 C3.9
- **C** 播放出來的每一格本來就是完整的 → 回看 C3.9
- **D** 差異影格可以記錄任何像素值 → 回看 C3.9

## Q96 · C3.9 · 選擇 · hard · 4
Which is an example of spatial (not temporal) compression?

- A. Storing only the pixels that changed since the last frame
- B. Encoding a large blue sky in one frame compactly because neighboring pixels are similar
- C. Repeating a key frame every 2 seconds
- D. Recording motion vectors between frames

### 答案
B

### 詳解
空間壓縮利用同一格內的相似。

### 迷思對照
- **A** 那是時間壓縮 → 回看 C3.9
- **C** 那是關鍵影格的安排 → 回看 C3.9
- **D** 動作向量是影格之間的關係 → 回看 C3.9 的現代補充

## Q97 · C3.9 · 簡答 · mid · 6
Describe the trade-off in choosing how often to insert key frames.

### 答案
關鍵影格越密:跳轉快、錯誤影響範圍小,但檔案大(關鍵影格遠比差異影格大)。越疏:檔案小,但跳轉時要從前一張關鍵影格一路套用很多差異影格,錯誤也會延續更久。

### 詳解
串流服務通常每 1–2 秒一張。

### 評分要點
- 密的優缺點(3 分)
- 疏的優缺點(3 分)

## Q98 · C3.10 · 計算 · basic · 3
Write the bytes of `0xCAFEBABE` in little-endian order (uppercase, space-separated).

### 答案
`BE BA FE CA`

### 詳解
最低位位元組 `BE` 放在最低位址。

### 驗算
```check
(0xCAFEBABE).to_bytes(4, "little").hex(" ").upper() == ANS
```

## Q99 · C3.10 · 計算 · mid · 4
The bytes `00 00 01 00` are read as a 32-bit little-endian integer. What is the value?

### 答案
`65536`

### 詳解
$0 + 0 \cdot 2^8 + 1 \cdot 2^{16} + 0 = 65536$。

### 驗算
```check
int.from_bytes(bytes.fromhex("00000100"), "little") == int(ANS)
```

## Q100 · C3.10 · 計算 · mid · 4
The same bytes `00 00 01 00` are read as big-endian. What is the value?

### 答案
`256`

### 詳解
$0 \cdot 2^{24} + 0 \cdot 2^{16} + 1 \cdot 2^8 + 0 = 256$。

### 驗算
```check
int.from_bytes(bytes.fromhex("00000100"), "big") == int(ANS)
```

## Q101 · C3.10 · 計算 · hard · 5
A BMP header contains the width field (little-endian) `20 03 00 00`. What is the width in pixels?

### 答案
`800`

### 詳解
0x00000320 = 800。

### 驗算
```check
int.from_bytes(bytes.fromhex("20030000"), "little") == int(ANS)
```

## Q102 · C3.10 · 選擇 · basic · 2
On a little-endian machine, which byte of a multi-byte integer is stored at the lowest address?

- A. The most significant byte
- B. The least significant byte
- C. The sign byte
- D. It depends on the value

### 答案
B

### 詳解
小端:低位在低位址。

### 迷思對照
- **A** 那是大端 → 回看 C3.10
- **C** 沒有「符號位元組」這種規則 → 回看 C3.10
- **D** 順序由機器決定,與值無關 → 回看 C3.10

## Q103 · C3.10 · 選擇 · mid · 3
Which byte order do Internet protocols (TCP/IP headers) use?

- A. Little-endian
- B. Big-endian (network byte order)
- C. Whatever the sender's CPU uses
- D. Middle-endian

### 答案
B

### 詳解
網路位元組順序是大端序,主機要用 `htonl` 等函式轉換。

### 迷思對照
- **A** x86 是小端,但網路不是 → 回看 C3.10
- **C** 若如此,不同 CPU 無法溝通 → 回看 C3.10
- **D** 非標準 → 回看 C3.10

## Q104 · C3.10 · 選擇 · hard · 4
Why is `p[0] | p[1] << 8 | p[2] << 16 | (uint32_t)p[3] << 24` preferred over `*(uint32_t *)p` for reading a little-endian field from a file buffer?

- A. It is faster on every machine.
- B. It gives the same result on big- and little-endian machines and avoids misaligned access.
- C. It converts the value to big-endian.
- D. It is required by the C standard for all integer reads.

### 答案
B

### 詳解
移位組合只用算術,與主機順序無關;指標轉型依賴主機順序,也可能違反對齊。

### 迷思對照
- **A** 效能不是重點 → 回看 C3.10 的原理
- **C** 它組出的是正確的數值,不是轉換順序 → 回看 C3.10
- **D** 標準沒有這種規定 → 回看 C3.10

## Q105 · C3.10 · 簡答 · mid · 6
You write an `int` to a file on an x86 laptop with `fwrite(&x, 4, 1, f)` and read it on a big-endian machine with `fread`. What goes wrong, and how should a file format avoid it?

### 答案
x86 以小端序寫入,大端機器以大端序解讀,位元組順序顛倒,值錯誤(例如 1 變成 16,777,216)。檔案格式應規定固定的位元組順序,並在讀寫時用移位明確組合/拆解位元組,而不是直接 `fwrite` 記憶體內容。

### 詳解
BMP、WAV、PNG 都在規格中明訂位元組順序。

### 評分要點
- 說明順序不同造成錯誤(3 分)
- 給出正確做法(3 分)
