---
id: C2.3
title_en: Converting from Decimal to Base b
title_zh: 從十進位轉成 b 進位
sub: Divide for the integer part, multiply for the fraction
level: mid
lab_hook: "任務 3:`to_base()`、`frac_to_base()`"
---
## 觀念
**Integer part — repeated division.** Divide the number by $b$; the remainder is the rightmost digit. Divide the quotient by $b$ again; the remainder is the next digit to the left. Continue until the quotient is 0. Read the remainders **from the last to the first**.

**Fractional part — repeated multiplication.** Multiply the fraction by $b$; the integer part of the result is the first digit after the radix point. Keep the fractional part and repeat. Stop when the fraction becomes 0 or when you have enough digits.

Some fractions that are finite in decimal are **infinite repeating** in binary. For example

$$0.1_{10} = 0.0\overline{0011}_2 = 0.000110011001100\ldots_2$$

so $0.1$ cannot be stored exactly in a binary computer.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| quotient | 商 | 除法的結果 |
| remainder | 餘數 | 除不盡剩下的部分,$0 \le r < b$ |
| repeated division | 連除法 | 一直除以 b、收集餘數 |
| repeated multiplication | 連乘法 | 小數一直乘以 b、收集整數部分 |
| repeating fraction | 循環小數 | 小數部分無限重複 |

## 白話說
整數部分:每除一次 b,就把「最右邊那一位」剝下來(就是餘數)。因為先剝下來的是最低位,所以最後要**倒過來讀**。

小數部分:每乘一次 b,就把「小數點後第一位」推到整數部分,把它拿走,剩下的繼續。這次是**順著讀**。

十進位的 0.1 在二進位是無限循環小數——這就是為什麼程式裡 `0.1 + 0.2` 不會剛好等於 `0.3`(第 3 章詳談)。

## 後面會用到
- **計算機組織**:浮點數表示(IEEE 754)的第一步就是把十進位小數轉成二進位。
- **數值方法**:捨入誤差的來源。
- **程式設計**:`printf("%x")`、`bin()` 背後就是連除法;Lab 任務 3 你要自己寫。

## 原理
**為什麼餘數要倒著讀?** 設 $N = d_k b^k + \cdots + d_1 b + d_0$。除以 $b$:商是 $d_k b^{k-1} + \cdots + d_1$,餘數是 $d_0$——第一個餘數是**最低位**。對商重複,依序得到 $d_1, d_2, \dots$,所以寫出來時要從最後一個餘數寫起。

**為什麼小數要乘?** 設 $F = d_{-1} b^{-1} + d_{-2} b^{-2} + \cdots$。乘以 $b$:$bF = d_{-1} + (d_{-2} b^{-1} + \cdots)$,整數部分正好是 $d_{-1}$,剩下的又是一個同樣形式的小數。

**什麼時候會有限?** 最簡分數 $p/q$ 在基底 $b$ 下是有限小數,若且唯若 $q$ 的每個質因數都整除 $b$。$0.1 = 1/10$,$10 = 2 \times 5$,而 5 不整除 2,所以在二進位是無限小數;但 $0.625 = 5/8$,分母只有 2,所以是有限的 $0.101_2$。

## 老師講解
### 例 1
Convert $179_{10}$ to binary and to hexadecimal.

1. **二進位,連除 2**:179 ÷ 2 = 89 餘 1;89 ÷ 2 = 44 餘 1;44 ÷ 2 = 22 餘 0;22 ÷ 2 = 11 餘 0;11 ÷ 2 = 5 餘 1;5 ÷ 2 = 2 餘 1;2 ÷ 2 = 1 餘 0;1 ÷ 2 = 0 餘 1。
2. **倒著讀餘數**:$10110011_2$。
3. **十六進位,連除 16**:179 ÷ 16 = 11 餘 3;11 ÷ 16 = 0 餘 11(B)。倒著讀:$\text{B3}_{16}$。
4. **驗算**:$\text{B3}_{16} = 11 \cdot 16 + 3 = 179$ ✓;$10110011_2 = 128 + 32 + 16 + 2 + 1 = 179$ ✓。

### 例 2
Convert $0.1_{10}$ to binary, showing the first 8 digits, and explain the pattern.

1. $0.1 \times 2 = 0.2$ → 取 **0**,剩 0.2。
2. $0.2 \times 2 = 0.4$ → **0**;$0.4 \times 2 = 0.8$ → **0**;$0.8 \times 2 = 1.6$ → **1**,剩 0.6。
3. $0.6 \times 2 = 1.2$ → **1**,剩 0.2——回到第 1 步之後的狀態,開始循環。
4. 接著:0.2 → **0**、0.4 → **0**、0.8 → **1**。前 8 位:$0.00011001_2$。
5. 餘下的小數在 0.2 → 0.4 → 0.8 → 0.6 之間永遠打轉,所以是無限循環小數 $0.0\overline{0011}_2$。

## 易錯點
- 連除法的餘數忘了倒過來讀。
- 連乘法把整數部分留在下一輪繼續乘(應該先拿掉)。
- 以為所有十進位有限小數在二進位也有限。

## 教學提示
例 2 做完可以現場在 Python 打 `0.1 + 0.2`,看到 `0.30000000000000004`,讓學生自己把兩件事連起來。Lab 任務 3 的公開測試就是 $0.1$ 轉 8 位二進位。

## 練習
### 照做
Convert $45_{10}$ to binary using repeated division.

#### 解答
45 → 22 餘 1 → 11 餘 0 → 5 餘 1 → 2 餘 1 → 1 餘 0 → 0 餘 1;倒著讀:$101101_2$。

### 是非
True or false: $0.625_{10}$ has a finite binary representation.

#### 解答
True。$0.625 = 5/8$,分母是 2 的冪次;$0.625_{10} = 0.101_2$。

### 變化
Convert $1000_{10}$ to octal and to hexadecimal.

#### 解答
八進位:1000 → 125 餘 0 → 15 餘 5 → 1 餘 7 → 0 餘 1 → $1750_8$。十六進位:1000 → 62 餘 8 → 3 餘 14(E)→ 0 餘 3 → $\text{3E8}_{16}$。

### 應用
Convert $0.3_{10}$ to binary with 8 digits after the radix point. Is it exact?

#### 解答
0.3→0.6(0)→1.2(1,剩 0.2)→0.4(0)→0.8(0)→1.6(1,剩 0.6)→1.2(1,剩 0.2)→0.4(0)→0.8(0):$0.01001100_2$。不精確;$0.3 = 3/10$,分母含 5,是無限循環小數 $0.0\overline{1001}_2$。

### 挑戰
Which of these fractions have a finite representation in base 12: $1/3$, $1/8$, $1/5$? Justify with prime factors.

#### 解答
$12 = 2^2 \times 3$。$1/3$:分母質因數 3 整除 12 → 有限($0.4_{12}$)。$1/8$:質因數只有 2 → 有限($1/8 = 18/144$,即 $0.16_{12}$)。$1/5$:5 不整除 12 → 無限循環。

## 驗算
```check
to_base(179, 2) == "10110011" and to_base(179, 16) == "b3"
to_base(45, 2) == "101101"
to_base(1000, 8) == "1750" and to_base(1000, 16) == "3e8"
0.625 == 0.5 + 0.125
(1/8) * 144 == 18
```
