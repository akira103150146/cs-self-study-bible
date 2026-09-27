---
chapter: 2
---
## Q1 · C2.1 · 計算 · basic · 3
Find the decimal value of $3021_4$.

### 答案
`201`

### 詳解
$3 \cdot 64 + 0 \cdot 16 + 2 \cdot 4 + 1 = 192 + 8 + 1 = 201$。

### 驗算
```check
int("3021", 4) == int(ANS)
```

## Q2 · C2.1 · 計算 · basic · 3
What is the decimal value of the digit pair $\text{1A}_{16}$?

### 答案
`26`

### 詳解
$1 \cdot 16 + 10 = 26$。

### 驗算
```check
int("1A", 16) == int(ANS)
```

## Q3 · C2.1 · 計算 · mid · 4
What is the largest two-digit numeral in base 36, and what is its decimal value? Give only the decimal value.

### 答案
`1295`

### 詳解
最大的兩位數是 ZZ:$35 \cdot 36 + 35 = 1295 = 36^2 - 1$。

### 驗算
```check
int("zz", 36) == int(ANS) == 36**2 - 1
```

## Q4 · C2.1 · 計算 · mid · 4
The largest three-digit octal numeral is $777_8$. What is its decimal value?

### 答案
`511`

### 詳解
$7 \cdot 64 + 7 \cdot 8 + 7 = 511 = 8^3 - 1$。

### 驗算
```check
int("777", 8) == int(ANS) == 8**3 - 1
```

## Q5 · C2.1 · 計算 · mid · 4
In some base $b$, the numeral $21_b$ equals $7_{10}$. Find $b$.

### 答案
`3`

### 詳解
$2b + 1 = 7$ → $b = 3$;數字 2 < 3,合法。

### 驗算
```check
int("21", int(ANS)) == 7
```

## Q6 · C2.1 · 計算 · hard · 5
In base $b$, the numeral $144_b$ equals $169_{10}$. Find $b$.

### 答案
`11`

### 詳解
$b^2 + 4b + 4 = (b + 2)^2 = 169$ → $b + 2 = 13$ → $b = 11$。檢查:數字 4 < 11,合法;$121 + 44 + 4 = 169$ ✓。

### 驗算
```check
int("144", int(ANS)) == 169
```

## Q7 · C2.1 · 選擇 · basic · 2
Which numeral is **not** valid in its stated base?

- A. $1101_2$
- B. $6078_8$
- C. $\text{FACE}_{16}$
- D. $2210_3$

### 答案
B

### 詳解
八進位只能用 0–7,8 不合法。

### 迷思對照
- **A** 以為二進位數長得像十進位就可疑 → 回看 C2.1:只要只有 0、1 就合法
- **C** 以為字母不能當數字 → 回看 C2.1:十六進位用 A–F 表示 10–15
- **D** 以為 2 在三進位不合法 → 回看 C2.1:基底 3 可用 0、1、2

## Q8 · C2.1 · 選擇 · mid · 3
In positional notation, what is the weight of the leftmost digit of a 5-digit base-$b$ numeral?

- A. $b^5$
- B. $b^4$
- C. $5b$
- D. $b^{-5}$

### 答案
B

### 詳解
位數從右邊的第 0 位開始,5 位數的最左邊是第 4 位,權重 $b^4$。

### 迷思對照
- **A** 忘了從 0 開始數 → 回看 C2.1 的易錯點
- **C** 把次方誤當成乘法 → 回看 C2.1:權重是 b 的次方
- **D** 和小數部分的負次方混淆 → 回看 C2.2

## Q9 · C2.1 · 選擇 · mid · 3
Which statement about bases is true?

- A. Base 16 needs 15 distinct digit symbols.
- B. In base $b$, the digit symbols range from 1 to $b$.
- C. In base $b$, the digit symbols range from 0 to $b - 1$.
- D. The base of a number system must be a power of 2.

### 答案
C

### 詳解
基底 b 恰好有 b 個數字:0、1、…、b−1。

### 迷思對照
- **A** 少算了 0 → 回看 C2.1:基底 16 有 0–F 共 16 個符號
- **B** 以為數字從 1 開始 → 回看 C2.1:一定包含 0
- **D** 以為只有 2 的冪次才能當基底 → 回看 C2.1:基底可以是任何 ≥ 2 的整數

## Q10 · C2.1 · 簡答 · mid · 5
Explain why every non-negative integer has exactly one representation in base $b$ (ignoring leading zeros).

### 答案
因為除法的商與餘數唯一:$N = q b + r$,$0 \le r < b$。最低位必須是 $r$(其他位的貢獻都是 b 的倍數),再對 $q$ 重複,每一步都唯一決定一位,直到商為 0。

### 詳解
這個證明本身就是「連除取餘數」演算法。

### 評分要點
- 提到除法的商與餘數唯一(2 分)
- 說明最低位必為餘數(2 分)
- 說明遞迴到商為 0(1 分)

## Q11 · C2.2 · 計算 · basic · 3
Convert $11011101_2$ to decimal.

### 答案
`221`

### 詳解
$128 + 64 + 16 + 8 + 4 + 1 = 221$。

### 驗算
```check
int("11011101", 2) == int(ANS)
```

## Q12 · C2.2 · 計算 · basic · 3
Convert $3721_8$ to decimal.

### 答案
`2001`

### 詳解
$3 \cdot 512 + 7 \cdot 64 + 2 \cdot 8 + 1 = 1536 + 448 + 16 + 1 = 2001$。

### 驗算
```check
int("3721", 8) == int(ANS)
```

## Q13 · C2.2 · 計算 · mid · 4
Convert $\text{C0DE}_{16}$ to decimal.

### 答案
`49374`

### 詳解
Horner:12 → $12 \cdot 16 + 0 = 192$ → $192 \cdot 16 + 13 = 3085$ → $3085 \cdot 16 + 14 = 49374$。

### 驗算
```check
int("C0DE", 16) == int(ANS)
```

## Q14 · C2.2 · 計算 · mid · 4
Convert $2102_3$ to decimal.

### 答案
`65`

### 詳解
$2 \cdot 27 + 1 \cdot 9 + 0 \cdot 3 + 2 = 65$。

### 驗算
```check
int("2102", 3) == int(ANS)
```

## Q15 · C2.2 · 計算 · mid · 4
Convert $0.1011_2$ to decimal.

### 答案
`0.6875`

### 詳解
$1/2 + 0 + 1/8 + 1/16 = 0.5 + 0.125 + 0.0625 = 0.6875$。

### 驗算
```check
0.5 + 0.125 + 0.0625 == float(ANS)
```

## Q16 · C2.2 · 計算 · hard · 6
Using Horner's rule on $\text{BEEF}_{16}$, list the intermediate values of $v$ after each digit, separated by commas without spaces.

### 答案
`11,190,3054,48879`

### 詳解
$v = 11$;$11 \cdot 16 + 14 = 190$;$190 \cdot 16 + 14 = 3054$;$3054 \cdot 16 + 15 = 48879$。

### 驗算
```check
",".join(str(int("BEEF"[:i], 16)) for i in range(1, 5)) == ANS
```

## Q17 · C2.2 · 計算 · hard · 5
What is the largest value an unsigned 64-bit integer can hold? A parser reading a decimal string must reject anything larger.

### 答案
`18446744073709551615`

### 詳解
$2^{64} - 1 = 18{,}446{,}744{,}073{,}709{,}551{,}615$。

### 驗算
```check
2**64 - 1 == int(ANS)
```

## Q18 · C2.2 · 選擇 · basic · 2
Applying Horner's rule to the digits of $231_4$, what is $v$ after the second digit?

- A. 2
- B. 11
- C. 45
- D. 9

### 答案
B

### 詳解
$v = 2$,讀 3 後 $v = 2 \cdot 4 + 3 = 11$;讀 1 後 $v = 45$。

### 迷思對照
- **A** 只讀了第一位 → 回看 C2.2 的 Horner 法步驟
- **C** 是讀完三位的最終值 → 回看 C2.2:題目問第二位之後
- **D** 用了錯的基底(例如 3)→ 回看 C2.2:每步乘的是 b = 4

## Q19 · C2.2 · 選擇 · mid · 3
Why is Horner's rule preferred for converting a long numeral to an integer?

- A. It gives a different, more accurate answer.
- B. It needs only one multiplication per digit and can process digits as they are read from left to right.
- C. It works only in binary.
- D. It avoids the need to check for overflow.

### 答案
B

### 詳解
Horner 法與展開法結果相同,但只要 n 次乘法,而且不需要事先知道位數。

### 迷思對照
- **A** 以為兩種方法結果不同 → 回看 C2.2 的原理:是同一個多項式
- **C** 以為只適用二進位 → 回看 C2.2:任何基底都適用
- **D** 以為 Horner 法不會溢位 → 回看 C2.2 的原理:仍要先檢查

## Q20 · C2.2 · 選擇 · hard · 4
A 64-bit parser computes `v = v * base + d` and then checks whether `v` got smaller. Why is this check unreliable?

- A. Unsigned overflow in C wraps around, so after `v * base` wraps the result can still look larger than before.
- B. The check is too slow.
- C. Overflow cannot happen with unsigned integers.
- D. The check works only in base 10.

### 答案
A

### 詳解
乘法溢位繞回後的值不一定比原本小(例如乘以 16 繞回後仍可能變大)。正確做法是事先檢查 $v > (\text{MAX} - d)/\text{base}$。

### 迷思對照
- **B** 把正確性問題當成效能問題 → 回看 C2.2 的原理
- **C** 以為無號整數不會溢位 → 回看 C2.2:它會繞回(模 $2^{64}$)
- **D** 以為基底會影響檢查的正確性 → 回看 C2.2:問題在於繞回

## Q21 · C2.2 · 簡答 · mid · 5
Explain why Horner's rule computes the same value as expanding by powers. Use $d_2 d_1 d_0$ in base $b$ as an example.

### 答案
$d_2 b^2 + d_1 b + d_0 = (d_2 \cdot b + d_1) \cdot b + d_0$。Horner 法先算 $v = d_2$,再 $v = v b + d_1$,再 $v = v b + d_0$,正好是右式由內往外計算。

### 詳解
提出公因數 b 就是 Horner 法的由來。

### 評分要點
- 寫出正確的因式分解(3 分)
- 對應到 Horner 的每一步(2 分)

## Q22 · C2.3 · 計算 · basic · 3
Convert $200_{10}$ to binary.

### 答案
`11001000`

### 詳解
200 → 100 r0 → 50 r0 → 25 r0 → 12 r1 → 6 r0 → 3 r0 → 1 r1 → 0 r1;倒著讀 $11001000_2$。

### 驗算
```check
to_base(200, 2) == ANS
```

## Q23 · C2.3 · 計算 · basic · 3
Convert $365_{10}$ to octal.

### 答案
`555`

### 詳解
365 → 45 r5 → 5 r5 → 0 r5 → $555_8$。

### 驗算
```check
to_base(365, 8) == ANS
```

## Q24 · C2.3 · 計算 · mid · 4
Convert $2024_{10}$ to hexadecimal (use lowercase letters).

### 答案
`7e8`

### 詳解
2024 → 126 r8 → 7 r14(e) → 0 r7 → $\text{7E8}_{16}$。

### 驗算
```check
to_base(2024, 16) == ANS.lower()
```

## Q25 · C2.3 · 計算 · mid · 4
Convert $100_{10}$ to base 3.

### 答案
`10201`

### 詳解
100 → 33 r1 → 11 r0 → 3 r2 → 1 r0 → 0 r1 → $10201_3$。

### 驗算
```check
to_base(100, 3) == ANS
```

## Q26 · C2.3 · 計算 · mid · 5
Convert $0.8125_{10}$ to binary (it terminates).

### 答案
`0.1101`

### 詳解
0.8125 × 2 = 1.625 → 1;0.625 × 2 = 1.25 → 1;0.25 × 2 = 0.5 → 0;0.5 × 2 = 1.0 → 1,剩 0 停止。

### 驗算
```check
ANS.startswith("0.") and int(ANS[2:], 2) / 2**len(ANS[2:]) == 0.8125
```

## Q27 · C2.3 · 計算 · hard · 5
Convert $0.6_{10}$ to binary, giving exactly 6 digits after the radix point (truncate, do not round).

### 答案
`0.100110`

### 詳解
0.6→1.2(1)→0.4(0)→0.8(0)→1.6(1)→1.2(1)→0.4(0);前 6 位 $0.100110_2$,其後循環($0.1\overline{0011}_2$)。

### 驗算
```check
ANS == "0." + "".join(str(int(0.6 * 2**k) % 2) for k in range(1, 7))
```

## Q28 · C2.3 · 計算 · hard · 5
Convert $1000_{10}$ to base 36 (lowercase letters).

### 答案
`rs`

### 詳解
1000 → 27 r28(s)→ 0 r27(r)→ `rs`。驗算:$27 \cdot 36 + 28 = 1000$。

### 驗算
```check
to_base(1000, 36) == ANS
```

## Q29 · C2.3 · 選擇 · basic · 2
When converting an integer by repeated division, in which order are the remainders written?

- A. In the order they were produced
- B. In reverse order: the last remainder is the leftmost digit
- C. Sorted from smallest to largest
- D. Only the last remainder matters

### 答案
B

### 詳解
第一個餘數是最低位,最後一個餘數是最高位,所以要倒著寫。

### 迷思對照
- **A** 和小數的連乘法混淆 → 回看 C2.3:小數才是順著讀
- **C** 以為要排序 → 回看 C2.3:順序由位置決定,不是大小
- **D** 以為只有最後一步重要 → 回看 C2.3:每個餘數都是一位

## Q30 · C2.3 · 選擇 · mid · 3
Which decimal fraction has a **finite** binary representation?

- A. 0.1
- B. 0.2
- C. 0.375
- D. 0.3

### 答案
C

### 詳解
$0.375 = 3/8$,分母只有質因數 2 → 有限($0.011_2$)。其他分母含 5。

### 迷思對照
- **A** 以為十進位有限就二進位有限 → 回看 C2.3 的原理
- **B** 同上:$0.2 = 1/5$ → 回看 C2.3 的原理
- **D** 同上:$0.3 = 3/10$ → 回看 C2.3 的原理

## Q31 · C2.3 · 選擇 · hard · 4
In Python, `0.1 + 0.2 == 0.3` is `False`. What is the root cause?

- A. Python has a bug in its addition.
- B. 0.1, 0.2 and 0.3 are infinite repeating fractions in binary, so each is stored as a nearby approximation.
- C. Python stores floats in decimal.
- D. The comparison operator rounds the numbers.

### 答案
B

### 詳解
這三個數的分母都含 5,在二進位是無限循環小數,只能存近似值;近似值相加與另一個近似值不一定相等。

### 迷思對照
- **A** 以為是語言的 bug → 回看 C2.3:所有用二進位浮點數的語言都一樣
- **C** 以為浮點數以十進位儲存 → 回看 C2.3(第 3 章 C3.4 詳談)
- **D** 以為比較會捨入 → 回看 C2.3:`==` 比較的是精確的位元

## Q32 · C2.3 · 簡答 · hard · 6
State the rule for when a fraction $p/q$ (in lowest terms) has a finite representation in base $b$, and apply it to $1/3$ in bases 2, 10, and 12.

### 答案
若且唯若 $q$ 的每個質因數都整除 $b$。$1/3$:3 不整除 2 → 二進位無限;3 不整除 10 → 十進位無限($0.333\ldots$);3 整除 12 → 十二進位有限($0.4_{12}$)。

### 詳解
直覺:要乘上 $b^k$ 之後變成整數,$b^k$ 必須含有 $q$ 的所有質因數。

### 評分要點
- 規則正確(3 分)
- 三個基底的判斷正確(各 1 分)

## Q33 · C2.4 · 計算 · basic · 3
Compute $10111_2 + 1101_2$ in binary.

### 答案
`100100`

### 詳解
23 + 13 = 36 = $100100_2$;逐欄相加共進位四次。

### 驗算
```check
to_base(int("10111", 2) + int("1101", 2), 2) == ANS
```

## Q34 · C2.4 · 計算 · mid · 4
Compute $5647_8 + 1234_8$ in octal.

### 答案
`7103`

### 詳解
7+4 = 11 = 8+3 → 寫 3 進 1;4+3+1 = 8 → 寫 0 進 1;6+2+1 = 9 → 寫 1 進 1;5+1+1 = 7。

### 驗算
```check
to_base(int("5647", 8) + int("1234", 8), 8) == ANS
```

## Q35 · C2.4 · 計算 · mid · 4
Compute $\text{B7}_{16} + \text{5C}_{16}$ in hexadecimal (lowercase).

### 答案
`113`

### 詳解
7 + C = 7 + 12 = 19 → 寫 3 進 1;B + 5 + 1 = 17 → 寫 1 進 1;寫下 1。

### 驗算
```check
to_base(int("B7", 16) + int("5C", 16), 16) == ANS.lower()
```

## Q36 · C2.4 · 計算 · mid · 4
Compute $11000_2 - 101_2$ in binary.

### 答案
`10011`

### 詳解
24 − 5 = 19 = $10011_2$;最右邊兩欄需要連續借位。

### 驗算
```check
to_base(int("11000", 2) - int("101", 2), 2) == ANS
```

## Q37 · C2.4 · 計算 · mid · 4
Compute $701_8 - 77_8$ in octal.

### 答案
`602`

### 詳解
1 − 7 不夠,向左借;左邊是 0,再向 7 借:各欄變成 6、7、9(= 1+8)。9 − 7 = 2;7 − 7 = 0;6 − 0 = 6。

### 驗算
```check
to_base(int("701", 8) - int("77", 8), 8) == ANS
```

## Q38 · C2.4 · 計算 · mid · 4
Compute $\text{C3}_{16} - \text{4F}_{16}$ in hexadecimal (lowercase).

### 答案
`74`

### 詳解
3 − F 不夠,借位:$3 + 16 - 15 = 4$;$C - 1 - 4 = 7$。

### 驗算
```check
to_base(int("C3", 16) - int("4F", 16), 16) == ANS.lower()
```

## Q39 · C2.4 · 計算 · hard · 5
Compute $1101_2 \times 101_2$ in binary using shift-and-add.

### 答案
`1000001`

### 詳解
$101$ 的第 0、2 位是 1:$1101 + 110100 = 1000001_2$(13 × 5 = 65)。

### 驗算
```check
to_base(int("1101", 2) * int("101", 2), 2) == ANS
```

## Q40 · C2.4 · 計算 · hard · 5
Compute $17_8 \times 5_8$ in octal.

### 答案
`113`

### 詳解
7 × 5 = 35 = 4·8 + 3 → 寫 3 進 4;1 × 5 + 4 = 9 = 8 + 1 → 寫 1 進 1;寫 1。結果 $113_8$(15 × 5 = 75)。

### 驗算
```check
to_base(int("17", 8) * int("5", 8), 8) == ANS
```

## Q41 · C2.4 · 選擇 · basic · 2
In binary addition, what do you write and carry for a column where $1 + 1 + 1$ (including a carry-in)?

- A. Write 1, carry 1
- B. Write 0, carry 1
- C. Write 1, carry 0
- D. Write 3, carry 0

### 答案
A

### 詳解
$1 + 1 + 1 = 3 = 11_2$:寫 1、進 1。

### 迷思對照
- **B** 把它當成 1 + 1 → 回看 C2.4 的觀念:還有進位進來
- **C** 忘了 3 ≥ 2 要進位 → 回看 C2.4:滿 b 進 1
- **D** 用十進位思考 → 回看 C2.4:二進位沒有數字 3

## Q42 · C2.4 · 選擇 · mid · 3
When you borrow in base-$b$ subtraction, how much does the current column gain?

- A. 10
- B. 1
- C. $b$
- D. $b - 1$

### 答案
C

### 詳解
左邊一欄的 1 相當於本欄的 b。

### 迷思對照
- **A** 用十進位的習慣 → 回看 C2.4:借來的是 b
- **B** 以為只借 1 → 回看 C2.4 的原理:左一欄的 1 值 b 個本欄單位
- **D** 和「最大數字」混淆 → 回看 C2.1:b − 1 是最大數字,不是借位值

## Q43 · C2.4 · 選擇 · hard · 4
Multiplying a binary number by $2^k$ is the same as …

- A. adding $k$ to it
- B. shifting it left by $k$ positions (appending $k$ zeros)
- C. shifting it right by $k$ positions
- D. flipping all its bits

### 答案
B

### 詳解
每左移一位,每個位元的權重乘以 2。

### 迷思對照
- **A** 把乘法和加法混淆 → 回看 C2.4
- **C** 方向相反:右移是除以 2 → 回看 C2.4
- **D** 翻轉位元和補數有關,不是乘法 → 回看第 3 章 C3.2

## Q44 · C2.4 · 簡答 · mid · 5
Explain why, when adding two base-$b$ numbers column by column, the carry into the next column is always 0 or 1.

### 答案
一欄最多是 $(b-1) + (b-1) + 1 = 2b - 1 < 2b$,所以商 $\lfloor s/b \rfloor$ 最多是 1。

### 詳解
用最壞情況界定欄和。

### 評分要點
- 寫出最大欄和 $2b - 1$(3 分)
- 推出進位 ≤ 1(2 分)

## Q45 · C2.5 · 計算 · basic · 3
Convert $110110101_2$ to octal.

### 答案
`665`

### 詳解
$110\ 110\ 101$ → 6、6、5。

### 驗算
```check
to_base(int("110110101", 2), 8) == ANS
```

## Q46 · C2.5 · 計算 · basic · 3
Convert $1011100111_2$ to hexadecimal (lowercase).

### 答案
`2e7`

### 詳解
從右邊 4 位一組:$10\ 1110\ 0111$ → 補成 $0010$ → 2、E、7。

### 驗算
```check
to_base(int("1011100111", 2), 16) == ANS.lower()
```

## Q47 · C2.5 · 計算 · basic · 3
Convert $\text{3B}_{16}$ to binary (no leading zeros).

### 答案
`111011`

### 詳解
3 = 0011、B = 1011 → $00111011$ → 去掉前導零 $111011$。

### 驗算
```check
to_base(int("3B", 16), 2) == ANS
```

## Q48 · C2.5 · 計算 · mid · 4
Convert $57_8$ to binary (no leading zeros).

### 答案
`101111`

### 詳解
5 = 101、7 = 111 → $101111$。

### 驗算
```check
to_base(int("57", 8), 2) == ANS
```

## Q49 · C2.5 · 計算 · mid · 4
Convert $\text{ACE}_{16}$ to octal.

### 答案
`5316`

### 詳解
A = 1010、C = 1100、E = 1110 → $101011001110$ → 3 位一組 $101\ 011\ 001\ 110$ → 5、3、1、6。

### 驗算
```check
to_base(int("ACE", 16), 8) == ANS
```

## Q50 · C2.5 · 計算 · mid · 4
Convert $1234_8$ to hexadecimal (lowercase).

### 答案
`29c`

### 詳解
$001\,010\,011\,100$ → 4 位一組 $0010\,1001\,1100$ → 2、9、C。

### 驗算
```check
to_base(int("1234", 8), 16) == ANS.lower()
```

## Q51 · C2.5 · 計算 · hard · 5
Convert $1011.011_2$ to hexadecimal. Write the answer like `b.6`.

### 答案
`b.6`

### 詳解
整數部分 $1011$ → B;小數部分從小數點往右分,右邊補零:$0110$ → 6。

### 驗算
```check
int("1011", 2) + int("011", 2) / 8 == int(ANS.split(".")[0], 16) + int(ANS.split(".")[1], 16) / 16
```

## Q52 · C2.5 · 選擇 · basic · 2
How many bits does one hexadecimal digit represent?

- A. 2
- B. 3
- C. 4
- D. 8

### 答案
C

### 詳解
$16 = 2^4$。

### 迷思對照
- **A** 和位元組/半位元組混淆 → 回看 C2.5
- **B** 和八進位混淆 → 回看 C2.5:八進位是 3 位元
- **D** 和位元組混淆 → 回看 C2.6:8 位元是一個位元組 = 兩位十六進位

## Q53 · C2.5 · 選擇 · mid · 3
Converting $1101001_2$ to octal, a student groups from the left: $110\ 100\ 1$ and gets $641_8$. What is the correct answer?

- A. $641_8$
- B. $151_8$
- C. $69_8$
- D. $1101_8$

### 答案
B

### 詳解
從右邊分組:$1\ 101\ 001$ → 補成 $001\ 101\ 001$ → 1、5、1。

### 迷思對照
- **A** 從左邊分組 → 回看 C2.5 的易錯點
- **C** 把十六進位(69)當成八進位,而且 9 在八進位不合法 → 回看 C2.5
- **D** 沒有做轉換 → 回看 C2.5

## Q54 · C2.5 · 選擇 · hard · 4
Why can binary be converted to base 16 by grouping, but not to base 10?

- A. Base 10 has too many digits.
- B. Because $16 = 2^4$, each group of 4 bits has weight $16^j$; powers of 10 do not line up with bit boundaries.
- C. Base 10 numbers cannot be stored in a computer.
- D. Grouping works for any base; people just prefer division for base 10.

### 答案
B

### 詳解
分組成立的關鍵是基底為 $2^k$,讓每組的權重剛好是 $(2^k)^j$。

### 迷思對照
- **A** 以為和數字個數有關 → 回看 C2.5 的原理
- **C** 以為電腦不能存十進位 → 回看 C2.6
- **D** 以為分組適用任何基底 → 回看 C2.5 的原理

## Q55 · C2.5 · 簡答 · mid · 5
Unix file permissions `rwxr-xr--` are stored as 9 bits. Write them in octal, and explain why octal (not hexadecimal) is the natural choice.

### 答案
rwx = 111 = 7,r-x = 101 = 5,r-- = 100 = 4 → `754`。權限自然分成三組、每組 3 個位元(讀、寫、執行),剛好一組一位八進位;用十六進位的話 4 位一組會把不同組的位元混在一起。

### 詳解
好的表示法會讓資料的結構一眼可見。

### 評分要點
- 八進位答案正確(2 分)
- 說明 3 位一組對應 rwx(3 分)

## Q56 · C2.6 · 計算 · basic · 3
What is the largest unsigned value that fits in 20 bits?

### 答案
`1048575`

### 詳解
$2^{20} - 1 = 1{,}048{,}575$。

### 驗算
```check
2**20 - 1 == int(ANS)
```

## Q57 · C2.6 · 計算 · basic · 3
How many bits are needed to give a distinct code to each of 50 US states?

### 答案
`6`

### 詳解
$2^5 = 32 < 50 \le 64 = 2^6$。

### 驗算
```check
bits_for(50) == int(ANS)
```

## Q58 · C2.6 · 計算 · mid · 4
How many bits does it take to write $300_{10}$ in binary?

### 答案
`9`

### 詳解
$\lfloor \log_2 300 \rfloor + 1 = 8 + 1 = 9$;$300 = 100101100_2$。

### 驗算
```check
len(to_base(300, 2)) == int(ANS)
```

## Q59 · C2.6 · 計算 · mid · 4
How many bytes are in 1 MiB?

### 答案
`1048576`

### 詳解
$1\ \text{MiB} = 2^{20} = 1{,}048{,}576$ 位元組。

### 驗算
```check
2**20 == int(ANS)
```

## Q60 · C2.6 · 計算 · mid · 4
A color uses 8 bits for each of red, green, and blue. How many different colors can it represent?

### 答案
`16777216`

### 詳解
共 24 位元 → $2^{24} = 16{,}777{,}216$(約 1670 萬色)。

### 驗算
```check
2**24 == int(ANS) == 256**3
```

## Q61 · C2.6 · 計算 · hard · 5
A disk is sold as 2 TB ($2 \times 10^{12}$ bytes). How many GiB will the operating system report? Round to two decimal places.

### 答案
`1862.65`

### 詳解
$2 \times 10^{12} / 2^{30} \approx 1862.645$ → 1862.65 GiB。

### 驗算
```check
f"{2 * 10**12 / 2**30:.2f}" == ANS
```

## Q62 · C2.6 · 選擇 · basic · 2
How many different patterns can 10 bits represent?

- A. 10
- B. 20
- C. 1023
- D. 1024

### 答案
D

### 詳解
$2^{10} = 1024$。

### 迷思對照
- **A** 以為每個位元代表一種 → 回看 C2.6:每多一位,種類加倍
- **B** 以為是 2 × 10 → 回看 C2.6 的原理:是乘法原理
- **C** 和最大無號值混淆 → 回看 C2.6 的易錯點

## Q63 · C2.6 · 選擇 · mid · 3
Which is the correct definition of a *word*?

- A. Exactly 16 bits on every computer
- B. The number of bits a particular CPU handles as a unit
- C. Four bytes of ASCII text
- D. Any group of 8 bits

### 答案
B

### 詳解
字組大小依 CPU 而定,今天多為 64 位元。

### 迷思對照
- **A** 以為字組大小固定 → 回看 C2.6
- **C** 把「word」和英文單字混淆 → 回看 C2.6
- **D** 和位元組混淆 → 回看 C2.6

## Q64 · C2.6 · 選擇 · hard · 4
In C, `uint64_t x = (uint64_t)1 << 64;` is …

- A. always $2^{64}$
- B. always 0
- C. undefined behavior, because the shift count must be less than the width of the type
- D. a compile error in every compiler

### 答案
C

### 詳解
C 標準規定移位量 ≥ 型別寬度是未定義行為;實際結果依硬體而異(x86 常得到 1)。

### 迷思對照
- **A** 以為 64 位元能存 $2^{64}$ → 回看 C2.6:最大只有 $2^{64}-1$
- **B** 以為溢位就變 0 → 回看 C2.6 的挑戰題
- **D** 以為編譯器一定會擋 → 回看 C2.6:多數只給警告,或完全不察覺

## Q65 · C2.6 · 簡答 · mid · 5
Explain why a 1 TB disk shows up as about 931 GiB in the operating system. Show the calculation.

### 答案
廠商用 SI 單位:1 TB = $10^{12}$ 位元組。作業系統用二進位前綴:1 GiB = $2^{30}$ 位元組。$10^{12} / 2^{30} \approx 931.3$。容量沒有少,只是單位不同。

### 詳解
兩套前綴並存是常見的混淆來源。

### 評分要點
- 說明兩種單位的定義(2 分)
- 算式正確(2 分)
- 結論「容量沒有少」(1 分)
