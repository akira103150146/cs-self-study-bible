---
id: C2.2
title_en: Converting from Base b to Decimal
title_zh: 從 b 進位轉成十進位
sub: Expand by powers — or use Horner's rule
level: basic
lab_hook: "任務 2:`parse_base()`"
---
## 觀念
To convert a numeral from base $b$ to decimal, multiply each digit by its positional weight and add:

$$d_{n-1} \dots d_1 d_0\ (\text{base } b) = \sum_{i=0}^{n-1} d_i\, b^i.$$

**Horner's rule** computes the same value from left to right with only one multiplication per digit:

$$v \leftarrow 0; \quad \text{for each digit } d \text{ from left to right:}\ v \leftarrow v \cdot b + d.$$

Digits to the right of the radix point have negative powers: $0.d_{-1} d_{-2} \dots = d_{-1} b^{-1} + d_{-2} b^{-2} + \cdots$. For example $0.101_2 = 1/2 + 0/4 + 1/8 = 0.625$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| positional weight | 位值權重 | 第 i 位的權重 $b^i$ |
| Horner's rule | Horner 法 | 由左到右「乘 b 再加下一位」的求值法 |
| radix point | 小數點(基底點) | 分隔整數與小數部分的點 |
| overflow | 溢位 | 結果超出可表示的範圍 |

## 白話說
展開法很直觀,但要先算好每個 $b^i$。Horner 法更像「一邊讀一邊算」:讀到下一位,就把目前的值乘上 b(整體往左移一位)再加上新的一位。電腦讀字串轉數字(例如 C 的 `strtol`)就是這樣做的,Lab 任務 2 你要自己實作它。

## 後面會用到
- **程式設計**:把使用者輸入的字串變成數字,就是 Horner 法。
- **演算法**:Horner 法也是多項式求值的標準方法,乘法次數從 $O(n^2)$ 降到 $O(n)$。
- **資訊安全**:忘了檢查溢位的字串轉整數,是真實世界漏洞的常見來源。

## 原理
**Horner 法為什麼對?** 把多項式一層層提出 $b$:

$$d_3 b^3 + d_2 b^2 + d_1 b + d_0 = ((d_3 \cdot b + d_2) \cdot b + d_1) \cdot b + d_0.$$

由內往外算,就是「$v = v \cdot b + d$」重複 $n$ 次。總共 $n$ 次乘法、$n$ 次加法;展開法若每個 $b^i$ 都從頭算,需要約 $n^2/2$ 次乘法。

**溢位怎麼事先檢查?** 64 位元無號整數的上限是 $2^{64}-1$。要做 $v \cdot b + d$ 之前,先檢查 $v > (\text{MAX} - d) / b$;成立就代表結果會超過上限。先檢查再算,避免溢位已經發生才發現。

## 老師講解
### 例 1
Convert $101101_2$ to decimal twice: by expansion and by Horner's rule.

1. **展開法**:$1 \cdot 32 + 0 \cdot 16 + 1 \cdot 8 + 1 \cdot 4 + 0 \cdot 2 + 1 \cdot 1 = 32 + 8 + 4 + 1 = 45$。
2. **Horner 法**,由左到右,$v$ 從 0 開始:
3. 讀 1:$v = 0 \cdot 2 + 1 = 1$;讀 0:$v = 2$;讀 1:$v = 5$;讀 1:$v = 11$;讀 0:$v = 22$;讀 1:$v = 45$。
4. 兩種方法都得到 45。Horner 法不需要事先知道有幾位,適合一邊讀字串一邊算。

### 例 2
Convert $\text{B2F}_{16}$ and $0.11_2$ to decimal.

1. $\text{B2F}_{16}$:B = 11、2、F = 15。
2. Horner:$v = 11$;$v = 11 \cdot 16 + 2 = 178$;$v = 178 \cdot 16 + 15 = 2863$。
3. $0.11_2 = 1 \cdot 2^{-1} + 1 \cdot 2^{-2} = 0.5 + 0.25 = 0.75$。
4. 檢查合理性:$\text{B2F}_{16}$ 有三位,應介於 $16^2 = 256$ 與 $16^3 = 4096$ 之間,2863 合理。

## 易錯點
- Horner 法最後一位**不用**再乘 b。
- 小數部分的權重是 $b^{-1}, b^{-2}, \dots$,不是 $b^{1}, b^{2}$。
- 實作時先乘後檢查溢位就來不及了:必須先檢查。

## 教學提示
可以讓學生計時比較兩種方法手算 $777777_8$ 的速度,感受 Horner 法的好處。Lab 任務 2 的隱藏測試包含剛好 $2^{64}-1$ 與超過一點點的輸入,提醒學生溢位檢查要精確到邊界。

## 練習
### 照做
Convert $110011_2$ to decimal.

#### 解答
$32 + 16 + 2 + 1 = 51$。

### 是非
True or false: Using Horner's rule on the digits of $754_8$ gives $v = 7$, then $v = 7 \cdot 8 + 5 = 61$, then $v = 61 \cdot 8 + 4 = 492$.

#### 解答
True。$754_8 = 7 \cdot 64 + 5 \cdot 8 + 4 = 492$。

### 變化
Convert $\text{3E8}_{16}$ and $1210_3$ to decimal.

#### 解答
$\text{3E8}_{16} = 3 \cdot 256 + 14 \cdot 16 + 8 = 1000$;$1210_3 = 27 + 2 \cdot 9 + 3 + 0 = 48$。

### 應用
A 64-bit parser reads the hexadecimal string `10000000000000000`. What should happen, and why?

#### 解答
這個數是 $16^{16} = 2^{64}$,超過 64 位元無號整數的最大值 $2^{64} - 1$,應回報溢位(Lab 裡回傳 -2),而不是默默算出錯誤的值(繞回 0)。

### 挑戰
Is $12.101_2$ a valid binary numeral? Explain, then convert $10.101_2$ to decimal.

#### 解答
$12.101_2$ 含有數字 2,不是合法的二進位數。$10.101_2 = 2 + 0.5 + 0 + 0.125 = 2.625$。

## 驗算
```check
int("101101", 2) == 45
int("B2F", 16) == 2863
int("110011", 2) == 51
int("754", 8) == 492
int("3E8", 16) == 1000 and int("1210", 3) == 48
16**16 == 2**64
2 + 0.5 + 0.125 == 2.625
```
