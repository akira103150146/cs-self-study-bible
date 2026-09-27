---
id: C2.4
title_en: Arithmetic in Other Bases
title_zh: 各進位的四則運算
sub: Same long-hand methods — carry and borrow b instead of 10
level: mid
lab_hook: "任務 4:`add_in_base()`、`sub_in_base()`、`mul_in_base()`"
---
## 觀念
The pencil-and-paper methods you learned for decimal work in **any** base; only the number at which you **carry** or **borrow** changes.

- **Addition**: add column by column from the right. If a column sum $s \ge b$, write $s - b$ and carry 1 to the next column.
- **Subtraction**: subtract column by column from the right. If the top digit is smaller, **borrow** one from the next column: the current column gains $b$.
- **Multiplication**: multiply by each digit of the multiplier, shift, and add the partial products — all in base $b$.

In binary the tables are tiny: $0+0=0$, $0+1=1$, $1+1=10_2$ (write 0, carry 1), and $1+1+1=11_2$ (write 1, carry 1). Binary multiplication is just "shift and add".

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| carry | 進位 | 一欄的和 ≥ b 時,往左一欄加 1 |
| borrow | 借位 | 被減數不夠減時,向左一欄借 1(相當於本欄加 b) |
| partial product | 部分積 | 直式乘法中每一列的乘積 |
| shift | 移位 | 往左移一位 = 乘以 b |

## 白話說
十進位的直式加法,是「滿 10 進 1」;八進位就是「滿 8 進 1」,二進位就是「滿 2 進 1」。減法借位時,借來的不是 10,而是 b。

二進位乘法特別簡單:乘數的某一位是 1 就把被乘數**左移**到那一位抄下來,是 0 就跳過,最後全部加起來。CPU 的乘法器就是這樣做的。

## 後面會用到
- **數位邏輯**:加法器電路(第 4 章)就是把二進位直式加法做成硬體。
- **計算機組織**:乘法器用「移位與相加」;減法用二補數加法(第 3 章)實現。
- **資料結構**:大數運算(延伸專案)就是在陣列上做直式運算。

## 原理
**為什麼直式加法在任何基底都對?** 設兩個數在第 $i$ 欄的數字是 $a_i, c_i$,進位 $k_i \in \{0, 1\}$。這一欄貢獻的值是 $(a_i + c_i + k_i) b^i$。寫下 $s_i = (a_i + c_i + k_i) \bmod b$、進位 $k_{i+1} = \lfloor (a_i + c_i + k_i)/b \rfloor$,則

$$(a_i + c_i + k_i) b^i = s_i b^i + k_{i+1} b^{i+1}$$

所以把進位移到下一欄不改變總和。由於 $a_i, c_i \le b - 1$、$k_i \le 1$,欄和最多 $2b - 1$,進位永遠只有 0 或 1。乘法的一欄可能很大,進位就不只 1,但同一個等式仍成立。

## 老師講解
### 例 1
Compute $1011_2 + 111_2$ and $\text{8A}_{16} + \text{F9}_{16}$.

1. **二進位,由右往左**:1+1 = 10 → 寫 0 進 1;1+1+1 = 11 → 寫 1 進 1;0+1+1 = 10 → 寫 0 進 1;1+0+1 = 10 → 寫 0 進 1;最後寫下進位 1。結果 $10010_2$。
2. 驗算:$11 + 7 = 18 = 10010_2$ ✓。
3. **十六進位**:A + 9 = 10 + 9 = 19 ≥ 16 → 寫 19 − 16 = 3,進 1;8 + F + 1 = 8 + 15 + 1 = 24 → 寫 8,進 1;寫下進位 1。結果 $\text{183}_{16}$。
4. 驗算:$138 + 249 = 387 = 1 \cdot 256 + 8 \cdot 16 + 3$ ✓。

### 例 2
Compute $1000_2 - 11_2$ and $101_2 \times 11_2$.

1. **減法**:最右欄 0 − 1 不夠,向左借;但左邊都是 0,要一路借到最高位的 1。借完後各位變成 $0\,1\,1\,(10)_2$。
2. 逐欄相減:$10_2 - 1 = 1$;$1 - 1 = 0$;$1 - 0 = 1$;$0$。結果 $101_2$。驗算:$8 - 3 = 5$ ✓。
3. **乘法**:$101 \times 11$:乘數最右位 1 → 抄 $101$;下一位 1 → 左移一位抄 $1010$。
4. 相加:$101 + 1010 = 1111_2 = 15$。驗算:$5 \times 3 = 15$ ✓。

## 易錯點
- 十六進位相加時忘了把 A–F 當成 10–15。
- 借位時忘了「借來的是 b 不是 10」。
- 二進位的 $1 + 1 + 1$ 是 $11_2$(寫 1 進 1),不是寫 1 進 0。

## 教學提示
學生最常錯在連續借位(例 2 的減法),建議在黑板上把每一欄借位後的值寫出來。Lab 任務 4 要求直接在字串上做直式運算、不能轉整數,隱藏測試有 40 位數的大數,可以順便提到這就是大數運算的起點。

## 練習
### 照做
Compute $1101_2 + 1011_2$.

#### 解答
$11000_2$(13 + 11 = 24)。

### 是非
True or false: $777_8 + 1_8 = 1000_8$.

#### 解答
True。7 + 1 = 8 → 寫 0 進 1,連續進位三次:$1000_8 = 512 = 511 + 1$。

### 變化
Compute $\text{1000}_{16} - 1_{16}$ and $\text{FF}_{16} \times \text{FF}_{16}$.

#### 解答
$\text{FFF}_{16}$;$\text{FE01}_{16}$($255^2 = 65025$)。

### 應用
A CPU has only an adder and a shifter. Show how it computes $13 \times 6$ in binary using shift-and-add.

#### 解答
$6 = 110_2$:第 1 位是 1 → $1101$ 左移 1 = $11010$;第 2 位是 1 → 左移 2 = $110100$;第 0 位是 0 → 跳過。$11010 + 110100 = 1001110_2 = 78$ ✓。

### 挑戰
In base $b$, the sum of two single-digit numbers can produce a carry of at most 1. Prove it, and explain why the carry in a multiplication column can be larger.

#### 解答
兩個一位數最大都是 $b - 1$,加上進位最多 1:$(b-1) + (b-1) + 1 = 2b - 1 < 2b$,所以進位 $\lfloor (2b-1)/b \rfloor = 1$。乘法中一位乘一位最大 $(b-1)^2$,再加上舊的累加值與進位,可以遠大於 $2b$,所以進位可以大於 1。

## 驗算
```check
to_base(int("1011", 2) + int("111", 2), 2) == "10010"
to_base(int("8A", 16) + int("F9", 16), 16) == "183"
to_base(int("1000", 2) - int("11", 2), 2) == "101"
to_base(int("101", 2) * int("11", 2), 2) == "1111"
to_base(int("1101", 2) + int("1011", 2), 2) == "11000"
to_base(0xFF * 0xFF, 16) == "fe01"
to_base(13 * 6, 2) == "1001110"
```
