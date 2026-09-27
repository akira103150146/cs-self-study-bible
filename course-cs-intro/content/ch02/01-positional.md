---
id: C2.1
title_en: Numbers and Positional Notation
title_zh: 數字與位值記數
sub: The value of a digit depends on its position
level: basic
lab_hook: "任務 1:`digit_value()`、`digit_char()`"
---
## 觀念
A **number** is a unit of an abstract mathematical system. We use **natural numbers** (0, 1, 2, …), **integers** (…, −2, −1, 0, 1, 2, …), and **rational numbers** (an integer or the quotient of two integers, such as $-1/3$ or $5/2$).

In **positional notation**, the value of a digit depends on its **position**. The **base** (or **radix**) $b$ tells how many digits the system has: base $b$ uses the digits $0, 1, \dots, b-1$. A number with digits $d_{n-1} \dots d_1 d_0$ in base $b$ means

$$d_{n-1} b^{n-1} + \cdots + d_1 b^1 + d_0 b^0.$$

For bases larger than 10 we borrow letters: A = 10, B = 11, …, F = 15 in hexadecimal, and up to Z = 35 in base 36. We write the base as a subscript when it is not obvious: $943_{10}$, $1011_2$, $\text{FF}_{16}$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| natural number | 自然數 | 0、1、2、…(本課從 0 開始) |
| integer | 整數 | 包含負數與 0 |
| rational number | 有理數 | 可以寫成兩個整數相除的數 |
| positional notation | 位值記數法 | 數字的值由它所在的位置決定 |
| base / radix | 基底 | 每一位可用的數字個數,也是位與位之間的倍數 |
| digit | 數字、位數 | 0 到 b−1 其中之一 |
| hexadecimal | 十六進位 | 基底 16,用 0–9 與 A–F |

## 白話說
$943$ 的 9 之所以代表九百,是因為它在「百位」。換個基底,每一位的**權重**就從 $10^i$ 換成 $b^i$,道理完全一樣。

最容易犯的錯是忘記「基底 b 只能用 0 到 b−1」:二進位沒有 2,八進位沒有 8、9。看到 $1021_2$ 就要馬上說「這不是合法的二進位數」。

## 後面會用到
- **計算機組織**:記憶體位址、機器指令幾乎都用十六進位寫(例如 `0x7ffd…`)。
- **資料結構與演算法**:雜湊、Base64、進位轉換都是位值記數的應用。
- 本課第 3 章:所有資料的表示都建立在「位元 + 位值」上。

## 原理
**為什麼每個非負整數在基底 $b$ 下的表示法是唯一的?** 因為除法有唯一的商與餘數:$N = q \cdot b + r$,$0 \le r < b$。最低位 $d_0$ 必須是 $r$(其他位都是 $b$ 的倍數),剩下的 $q$ 再用同樣的方法決定 $d_1$……一路到商為 0。每一步都沒有選擇的餘地,所以表示法唯一(不計前導零)。

這個證明其實就是「連除取餘數」的轉換演算法(C2.3)。

## 老師講解
### 例 1
Write $943_{10}$ and $2013_{8}$ in expanded positional form, and compute the decimal value of $2013_8$.

1. **找出每一位的權重**:最右邊是第 0 位,權重 $b^0 = 1$,往左依序是 $b^1, b^2, \dots$。
2. $943_{10} = 9 \times 10^2 + 4 \times 10^1 + 3 \times 10^0 = 900 + 40 + 3$。
3. $2013_8 = 2 \times 8^3 + 0 \times 8^2 + 1 \times 8^1 + 3 \times 8^0$。
4. 計算:$2 \times 512 + 0 + 8 + 3 = 1024 + 11 = 1035$,所以 $2013_8 = 1035_{10}$。

### 例 2
Which of the following are valid numerals in the given base? (a) $1021_2$, (b) $778_8$, (c) $\text{1AF}_{16}$, (d) $\text{G1}_{16}$.

1. **規則**:基底 b 只能出現 0 到 b−1。
2. (a) 二進位只有 0、1,出現 2 → **不合法**。
3. (b) 八進位只有 0–7,出現 8 → **不合法**。
4. (c) 十六進位 0–9、A–F(15)都合法 → **合法**,值為 $1 \times 256 + 10 \times 16 + 15 = 431$。
5. (d) G 代表 16,超過 15 → **不合法**。

## 易錯點
- 位數從右邊數、而且從 **0** 開始:最右邊是 $b^0$ 不是 $b^1$。
- 大寫與小寫字母代表同一個值:`A` 和 `a` 都是 10。
- 把「基底 b」和「最大數字 b」搞混:基底 16 的最大數字是 F(15)。

## 教學提示
可以先讓學生用「鐘錶」(基底 60)或「一打」(基底 12)建立直覺,再進入二進位。Lab 任務 1 的 `digit_value` 是所有後續任務的地基,提醒學生處理大小寫與非法字元。

## 練習
### 照做
Write $5302_{10}$ in expanded positional form.

#### 解答
$5 \times 10^3 + 3 \times 10^2 + 0 \times 10^1 + 2 \times 10^0$。

### 是非
True or false: $123_4$ is a valid base-4 numeral.

#### 解答
True。基底 4 可用 0、1、2、3,題目只用到 1、2、3。

### 變化
What is the decimal value of the digit `Z` in base 36, and of the digit `c` in base 16?

#### 解答
Z = 35;c = 12。

### 應用
A programmer writes the byte value $\text{0x1F}$. Explain what the prefix `0x` means and give the decimal value.

#### 解答
`0x` 是 C 與許多語言表示十六進位的前綴。$\text{1F}_{16} = 1 \times 16 + 15 = 31$。

### 挑戰
In base $b$, the numeral $121_b$ equals $49_{10}$. Find $b$.

#### 解答
$1 \cdot b^2 + 2b + 1 = (b + 1)^2 = 49$ → $b + 1 = 7$ → $b = 6$。檢查:數字 2 小於 6,合法。

## 驗算
```check
int("2013", 8) == 1035
int("1AF", 16) == 431
int("121", 6) == 49
int("1F", 16) == 31
```
