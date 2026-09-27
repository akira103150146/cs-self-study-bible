---
id: C2.5
title_en: Power-of-2 Number Systems
title_zh: 2 的冪次進位
sub: Octal groups 3 bits, hexadecimal groups 4 — no arithmetic needed
level: basic
lab_hook: "任務 5:`regroup()`"
---
## 觀念
When the base is a power of 2, $b = 2^k$, each digit corresponds to exactly **$k$ bits**. So conversion between binary and base $2^k$ needs no division — just **grouping**:

- Binary → octal ($8 = 2^3$): group bits in threes **starting from the right** (from the radix point), pad the leftmost group with zeros, and replace each group by one octal digit.
- Binary → hexadecimal ($16 = 2^4$): group in fours.
- Octal or hexadecimal → binary: replace each digit by its 3-bit or 4-bit pattern.
- Octal ↔ hexadecimal: go through binary.

For fractions, group from the radix point **to the right**, padding the rightmost group with zeros.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| octal | 八進位 | 基底 8,每位對應 3 個位元 |
| hexadecimal | 十六進位 | 基底 16,每位對應 4 個位元 |
| nibble | 半位元組 | 4 個位元,剛好一位十六進位 |
| grouping | 分組 | 每 k 個位元換成一位 $2^k$ 進位數字 |
| padding | 補零 | 位元數不是 k 的倍數時在前(或後)面補 0 |

## 白話說
十六進位之所以在電腦界這麼常見,是因為它是二進位的**縮寫**:一位十六進位剛好是 4 個位元,一個位元組(8 位元)剛好寫成兩位十六進位。`11010110` 很難一眼看清,寫成 `D6` 就清楚多了。

轉換只要記住 0–F 的 4 位元樣子,不必做任何除法。唯一要小心的是**從哪一邊開始分組**:一定從小數點(整數的最右邊)往外分。

## 後面會用到
- **計算機組織**:記憶體位址、機器碼、顏色(`#FF8800`)都用十六進位。
- **作業系統**:Unix 檔案權限用八進位(`chmod 755`),因為每 3 個位元是一組 rwx。
- **資訊安全與網路**:Base64(6 位元一組)、IPv6(16 位元一組)都是同一個分組的想法;延伸專案 2 會實作 Base64。

## 原理
**為什麼分組就能換基底?** 把二進位數從右每 $k$ 位分一組,第 $j$ 組的值是 $g_j \in [0, 2^k - 1]$,它所在的權重是 $2^{kj} = (2^k)^j$。所以

$$N = \sum_j g_j \cdot (2^k)^j$$

這正是基底 $2^k$ 的展開式,每組的值 $g_j$ 就是一位 $2^k$ 進位數字。若 $b$ 不是 2 的冪次(例如 10),$b^j$ 不會落在位元的整數邊界上,就沒有這種捷徑。

## 老師講解
### 例 1
Convert $10101011_2$ to octal and hexadecimal.

1. **八進位,3 位一組,從右邊開始**:$10\ 101\ 011$;最左組只有 2 位,補成 $010$。
2. 各組換成數字:$010 = 2$、$101 = 5$、$011 = 3$ → $253_8$。
3. **十六進位,4 位一組**:$1010\ 1011$ → A、B → $\text{AB}_{16}$。
4. 驗算:$\text{AB}_{16} = 171$;$253_8 = 2 \cdot 64 + 5 \cdot 8 + 3 = 171$ ✓。

### 例 2
Convert $\text{3F7}_{16}$ to octal, and $1011.1_2$ to hexadecimal.

1. **十六進位 → 二進位**:3 = $0011$、F = $1111$、7 = $0111$ → $0011\,1111\,0111$。
2. **重新 3 位一組**:$001\ 111\ 110\ 111$ → 1、7、6、7 → $1767_8$。
3. **含小數**:$1011.1_2$,整數部分從小數點往左分:$1011$ → B;小數部分從小數點往右分,不足 4 位在**右邊**補零:$1000$ → 8。
4. 結果 $\text{B.8}_{16}$。驗算:$11 + 8/16 = 11.5$,而 $1011.1_2 = 11.5$ ✓。

## 易錯點
- 從左邊開始分組:$10101011$ 從左 3 位一組會得到錯的答案。
- 小數部分在左邊補零:小數要在**右邊**補。
- 八進位 ↔ 十六進位想直接換:要先經過二進位。

## 教學提示
請學生背熟 0–F 的 4 位元樣子(至少 8 = 1000、A = 1010、F = 1111)。Lab 任務 5 要求用分組完成、不得轉整數,隱藏測試有 k = 5(基底 32),確認學生真的懂「k 位一組」而不是只背了 3 和 4。

## 練習
### 照做
Convert $11110000_2$ to hexadecimal.

#### 解答
$1111\ 0000$ → $\text{F0}_{16}$。

### 是非
True or false: $1011_2$ grouped in threes from the left gives $101\ 1$, so it equals $54_8$.

#### 解答
False。分組要從右邊開始:$001\ 011$ → $13_8$(= 11)。

### 變化
Convert $725_8$ to hexadecimal.

#### 解答
$725_8$ → $111\,010\,101$ → 重組 4 位:$0001\,1101\,0101$ → $\text{1D5}_{16}$(= 469)。

### 應用
The Unix permission `rwxr-x---` is written as three groups of 3 bits (r = 4, w = 2, x = 1). Write it in octal, as used by `chmod`.

#### 解答
rwx = 111 = 7;r-x = 101 = 5;--- = 000 = 0 → `750`。

### 挑戰
Base64 encodes binary data in groups of 6 bits. How many Base64 characters are needed for 3 bytes, and why is 3 bytes a natural block size?

#### 解答
3 位元組 = 24 位元 = 4 組 6 位元 → 4 個 Base64 字元。24 是 8 與 6 的最小公倍數,所以 3 個位元組剛好切成整數個 6 位元組,不需要補齊。

## 驗算
```check
int("10101011", 2) == int("253", 8) == int("AB", 16) == 171
int("3F7", 16) == int("1767", 8)
int("725", 8) == int("1D5", 16) == 469
int("1011", 2) == int("13", 8)
int("111101000", 2) == int("750", 8)
```
