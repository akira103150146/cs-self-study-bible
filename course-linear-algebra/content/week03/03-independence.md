---
title_en: Linear Independence
title_zh: 線性獨立:Ax = 0 只有平凡解
sub: Independent means no vector is wasted
level: mid
source: Lay 1.7
lab_hook: '`np.linalg.matrix_rank(A) == A.shape[1]`:秩等於行數 ⇔ 各行線性獨立'
---
## 觀念
An indexed set of vectors $\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ in $\mathbb{R}^n$ is said to be **linearly independent** if the vector equation

$$x_1\mathbf{v}_1 + x_2\mathbf{v}_2 + \cdots + x_p\mathbf{v}_p = \mathbf{0}$$

has only the trivial solution. The set $\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ is said to be **linearly dependent** if there exist weights $c_1, \dots, c_p$, not all zero, such that

$$c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_p\mathbf{v}_p = \mathbf{0}.$$

This equation is called a **linear dependence relation** among $\mathbf{v}_1, \dots, \mathbf{v}_p$ when the weights are not all zero. An indexed set is linearly dependent if and only if it is not linearly independent.

**Linear independence of matrix columns.** Suppose that we begin with a matrix $A = [\,\mathbf{a}_1 \;\; \cdots \;\; \mathbf{a}_n\,]$ instead of a set of vectors. The matrix equation $A\mathbf{x} = \mathbf{0}$ can be written as $x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + \cdots + x_n\mathbf{a}_n = \mathbf{0}$. *Each linear dependence relation among the columns of $A$ corresponds to a nontrivial solution of $A\mathbf{x} = \mathbf{0}$.*

> The columns of a matrix $A$ are linearly independent if and only if the equation $A\mathbf{x} = \mathbf{0}$ has *only* the trivial solution.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| linearly independent | 線性獨立 | $x_1\mathbf{v}_1 + \cdots + x_p\mathbf{v}_p = \mathbf{0}$ **只有**全為 0 的解 |
| linearly dependent | 線性相依 | 存在不全為 0 的權重,讓組合等於 $\mathbf{0}$ |
| linear dependence relation | 線性相依關係 | 一條權重不全為 0、組合結果是 $\mathbf{0}$ 的等式,例如 $10\mathbf{v}_1 - 5\mathbf{v}_2 + 5\mathbf{v}_3 = \mathbf{0}$ |
| indexed set | 有編號的集合 | 課本的 $\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ 有順序,也可以有重複的向量 |
| pivot column | pivot 行 | 化簡後含 pivot 的行;各行獨立 ⇔ **每一行**都是 pivot 行 |

## 白話說
一組向量**線性獨立**,意思是「**沒有一個是多餘的**」:你沒辦法用其他幾個湊出其中一個。

判斷方法只有一個,而且就是上一個觀念的齊次方程組:

1. 把向量排成矩陣的行:$A = [\,\mathbf{v}_1 \;\; \cdots \;\; \mathbf{v}_p\,]$。
2. 問 $A\mathbf{x} = \mathbf{0}$ **有沒有自由變數**:
   - 沒有自由變數(**每一行都是 pivot 行**)→ 只有平凡解 → **線性獨立**。
   - 有自由變數 → 有非平凡解 → **線性相依**,而且那個非平凡解的分量就是一條相依關係的權重。

小心這兩個問題的差別:

- 上週的 **Span / 生成**:看**每一列**有沒有 pivot(Theorem 4)。
- 這週的**線性獨立**:看**每一行**有沒有 pivot。

## 幾何意義
線性相依就是「有向量沒帶來新方向」:

- ℝ³ 裡的三個向量如果**擠在同一個平面上**,第三個可以由前兩個組合出來,它們就相依(Example 1 的三個向量正是如此)。
- 三個向量**撐出整個空間**、不在同一個平面上,才是獨立。

觀念 4 會再用圖說明兩個向量與三個向量的情況。

## 在資工哪裡用
- **資料表的多餘欄位**:一張資料表若有「總分 = 國文 + 英文 + 數學」這種欄位,這幾欄就線性相依。機器學習的線性迴歸遇到相依的欄位,係數會解不出唯一的答案(這叫 **多重共線性**,multicollinearity)。實作課就用 `matrix_rank` 把它找出來。
- **One-hot 編碼的陷阱**:把「顏色 = 紅/綠/藍」編成三個 0/1 欄位,三欄加起來永遠是 1,和常數欄相依。資料科學課叫它「dummy variable trap」,解法是丟掉一欄。
- **錯誤更正碼**:第 7 週的 Hamming 碼,檢查矩陣的行必須兩兩獨立,才能定位出錯的位元。

## 原理
**為什麼「各行獨立 ⇔ $A\mathbf{x} = \mathbf{0}$ 只有平凡解」?** 這只是把定義換一種寫法。$A\mathbf{x} = x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n$(上週的 $A\mathbf{x}$ 定義),所以

$$A\mathbf{x} = \mathbf{0} \text{ 的非平凡解 } (c_1, \dots, c_n) \iff c_1\mathbf{a}_1 + \cdots + c_n\mathbf{a}_n = \mathbf{0} \text{ 且權重不全為 0} \iff \text{一條相依關係}.$$

**為什麼可以用「每一行都是 pivot 行」判斷?** $A\mathbf{x} = \mathbf{0}$ 一定相容;它只有平凡解 ⇔ 沒有自由變數 ⇔ 每個變數都是基本變數 ⇔ 每一行都是 pivot 行(Exercise 36)。

## 老師講解
### 例 1 · Lay 1.7 Example 1
Let $\mathbf{v}_1 = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix}$, and $\mathbf{v}_3 = \begin{bmatrix} 2 \\ 1 \\ 0 \end{bmatrix}$.

- **a.** Determine if the set $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ is linearly independent.
- **b.** If possible, find a linear dependence relation among $\mathbf{v}_1$, $\mathbf{v}_2$, and $\mathbf{v}_3$.

1. **翻成方程式**:要問 $x_1\mathbf{v}_1 + x_2\mathbf{v}_2 + x_3\mathbf{v}_3 = \mathbf{0}$ 除了全 0 之外還有沒有解。
2. **(a) 化簡增廣矩陣**:$R_2 \leftarrow R_2 - 2R_1$、$R_3 \leftarrow R_3 - 3R_1$,再 $R_3 \leftarrow R_3 - 2R_2$:
   $$\left[\begin{array}{rrr|r} 1 & 4 & 2 & 0 \\ 2 & 5 & 1 & 0 \\ 3 & 6 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 4 & 2 & 0 \\ 0 & -3 & -3 & 0 \\ 0 & -6 & -6 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 4 & 2 & 0 \\ 0 & -3 & -3 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right]$$
3. **(a) 判斷**:$x_1$、$x_2$ 是基本變數,$x_3$ 是自由變數。每個不為 0 的 $x_3$ 都給一個非平凡解,所以 $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$ **線性相依**。
4. **(b) 化到 RREF,寫出解**:$R_2 \leftarrow -\tfrac13 R_2$;$R_1 \leftarrow R_1 - 4R_2$:
   $$\left[\begin{array}{rrr|r} 1 & 0 & -2 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right] \qquad x_1 = 2x_3,\quad x_2 = -x_3,\quad x_3 \text{ free}$$
5. **(b) 挑一個不為 0 的 $x_3$**,例如 $x_3 = 5$:$x_1 = 10$、$x_2 = -5$。代回去得到一條相依關係
   $$10\mathbf{v}_1 - 5\mathbf{v}_2 + 5\mathbf{v}_3 = \mathbf{0}.$$
6. **驗算**:$10(1, 2, 3) - 5(4, 5, 6) + 5(2, 1, 0) = (10 - 20 + 10,\; 20 - 25 + 5,\; 30 - 30 + 0) = (0, 0, 0)$ ✓。
7. **相依關係不唯一**:任何不為 0 的 $x_3$ 都可以,例如 $x_3 = 1$ 給 $2\mathbf{v}_1 - \mathbf{v}_2 + \mathbf{v}_3 = \mathbf{0}$。從這條式子也看得出 $\mathbf{v}_3 = \mathbf{v}_2 - 2\mathbf{v}_1$:第三個向量是多餘的。

### 例 2 · Lay 1.7 Example 2
Determine if the columns of the matrix $A = \begin{bmatrix} 0 & 1 & 4 \\ 1 & 2 & -1 \\ 5 & 8 & 0 \end{bmatrix}$ are linearly independent.

1. **問題變成**:$A\mathbf{x} = \mathbf{0}$ 是不是只有平凡解。
2. **化簡**:左上角是 0,先交換第 1、2 列;再 $R_3 \leftarrow R_3 - 5R_1$;再 $R_3 \leftarrow R_3 + 2R_2$:
   $$\left[\begin{array}{rrr|r} 0 & 1 & 4 & 0 \\ 1 & 2 & -1 & 0 \\ 5 & 8 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 2 & -1 & 0 \\ 0 & 1 & 4 & 0 \\ 0 & -2 & 5 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 2 & -1 & 0 \\ 0 & 1 & 4 & 0 \\ 0 & 0 & 13 & 0 \end{array}\right]$$
3. **數 pivot**:三個行都是 pivot 行,**沒有自由變數**。
4. **結論**:$A\mathbf{x} = \mathbf{0}$ 只有平凡解,$A$ 的各行**線性獨立**。
5. **不用化到 RREF**:判斷獨立只要看梯形上每一行有沒有 pivot。只有題目要你寫出相依關係時,才需要化到 RREF 解出權重。

## 易錯點
- 以為「$A\mathbf{x} = \mathbf{0}$ 有平凡解」就代表獨立。**每一個**齊次方程組都有平凡解;獨立的條件是「**只有**平凡解」(是非題 Exercise 21)。
- 把判斷獨立(看**行**)和判斷生成(看**列**)搞混。
- 找到相依關係後忘了確認權重「不全為 0」;或以為相依關係只有一條。
- 寫增廣矩陣時,最後一行全是 0,化簡過程中不會變。可以省略不寫,但心裡要知道它在。

## 教學提示
一定要先強調「**平凡解永遠存在**」,再問「還有沒有別的?」。可以用例 1 讓學生猜:「三個向量,能不能挑權重讓它們加起來剛好抵消成 $\mathbf{0}$?」大多數人會猜不行,算出 $10\mathbf{v}_1 - 5\mathbf{v}_2 + 5\mathbf{v}_3 = \mathbf{0}$ 時很有驚喜感。

黑板上畫一個兩欄的對照表,整週保留:左欄「生成 ℝᵐ:看**列**」,右欄「線性獨立:看**行**」。

課堂建議做:Exercises 1–2、5–6;是非 Exercise 21;Exercises 9 與 11。T 題(Exercises 47–50)留給實作課。

## 練習
### 照做 · Lay 1.7 Exercises 1–2
Determine if the vectors are linearly independent. Justify each answer.

(1) $\begin{bmatrix} 5 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 7 \\ 2 \\ -6 \end{bmatrix}, \begin{bmatrix} -2 \\ -1 \\ 6 \end{bmatrix}$  (2) $\begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}, \begin{bmatrix} 0 \\ 5 \\ -8 \end{bmatrix}, \begin{bmatrix} -3 \\ 4 \\ 1 \end{bmatrix}$

#### 解答
(1) 排成矩陣化簡:
$$\begin{bmatrix} 5 & 7 & -2 \\ 1 & 2 & -1 \\ 0 & -6 & 6 \end{bmatrix} \sim \cdots \sim \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & -1 \\ 0 & 0 & 0 \end{bmatrix}$$
第三行不是 pivot 行,$x_3$ 自由 → **線性相依**(書後解答相同)。從 RREF 可讀出 $x_1 = -x_3$、$x_2 = x_3$,取 $x_3 = -1$ 得 $\mathbf{v}_1 - \mathbf{v}_2 - \mathbf{v}_3 = \mathbf{0}$,也就是 $\mathbf{v}_3 = \mathbf{v}_1 - \mathbf{v}_2$。

(2) 交換第 1、3 列就得到梯形 $\begin{bmatrix} 2 & -8 & 1 \\ 0 & 5 & 4 \\ 0 & 0 & -3 \end{bmatrix}$,三行都是 pivot 行,沒有自由變數 → **線性獨立**。

### 照做 · Lay 1.7 Exercises 5–6
Determine if the columns of the matrix form a linearly independent set. Justify each answer.

(5) $\begin{bmatrix} 0 & -8 & 5 \\ 3 & -7 & 4 \\ -1 & 5 & -4 \\ 1 & -3 & 2 \end{bmatrix}$  (6) $\begin{bmatrix} -4 & -3 & 0 \\ 0 & -1 & 4 \\ 1 & 0 & 3 \\ 5 & 4 & 6 \end{bmatrix}$

#### 解答
(5) 把第 4 列換到最上面當 pivot 列,依序消去:
$$\sim \begin{bmatrix} 1 & -3 & 2 \\ 0 & 2 & -2 \\ 0 & 2 & -2 \\ 0 & -8 & 5 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 2 \\ 0 & 2 & -2 \\ 0 & 0 & -3 \\ 0 & 0 & 0 \end{bmatrix}$$
三行都有 pivot,沒有自由變數 → **線性獨立**(書後解答相同)。

(6) 把第 3 列換到最上面:
$$\sim \begin{bmatrix} 1 & 0 & 3 \\ 0 & -1 & 4 \\ 0 & -3 & 12 \\ 0 & 4 & -9 \end{bmatrix} \sim \begin{bmatrix} 1 & 0 & 3 \\ 0 & -1 & 4 \\ 0 & 0 & 0 \\ 0 & 0 & 7 \end{bmatrix}$$
交換最後兩列後是梯形,三行都有 pivot → **線性獨立**。

#### 備註
這兩題是 $4 \times 3$ 矩陣:列比行多。獨立只看**行**,所以最多 3 個 pivot 就夠了;第 4 列是全 0 不影響結論。

### 是非 · Lay 1.7 Exercise 21
**(T/F)** The columns of a matrix $A$ are linearly independent if the equation $A\mathbf{x} = \mathbf{0}$ has the trivial solution.

#### 解答
**False.** $A\mathbf{x} = \mathbf{0}$ **永遠**有平凡解。各行獨立的條件是「**只有**平凡解」。反例:$A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ 有平凡解,但 $2\mathbf{a}_1 - \mathbf{a}_2 = \mathbf{0}$,各行相依。

### 變化 · Lay 1.7 Exercises 9–10
(a) For what values of $h$ is $\mathbf{v}_3$ in $\operatorname{Span}\{\mathbf{v}_1, \mathbf{v}_2\}$, and (b) for what values of $h$ is $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ linearly *dependent*? Justify each answer.

(9) $\mathbf{v}_1 = \begin{bmatrix} 1 \\ -3 \\ 2 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} -3 \\ 10 \\ -6 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} 2 \\ -7 \\ h \end{bmatrix}$  (10) $\mathbf{v}_1 = \begin{bmatrix} 1 \\ -5 \\ -3 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} -2 \\ 10 \\ 6 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} 2 \\ -10 \\ h \end{bmatrix}$

#### 解答
(9) 化簡 $[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]$($\mathbf{v}_3$ 放最後一行,可以同時回答兩小題):
$$\left[\begin{array}{rr|r} 1 & -3 & 2 \\ -3 & 10 & -7 \\ 2 & -6 & h \end{array}\right] \sim \left[\begin{array}{rr|r} 1 & -3 & 2 \\ 0 & 1 & -1 \\ 0 & 0 & h - 4 \end{array}\right]$$
- (a) 看成增廣矩陣:相容 ⇔ $h - 4 = 0$,所以 $\mathbf{v}_3 \in \operatorname{Span}\{\mathbf{v}_1, \mathbf{v}_2\}$ ⇔ $h = 4$。
- (b) 看成係數矩陣:第三行沒有 pivot(出現自由變數)⇔ $h = 4$。所以相依 ⇔ $h = 4$(書後解答:兩小題都是 $h = 4$)。

(10) $R_2 \leftarrow R_2 + 5R_1$ 得到全 0 列、$R_3 \leftarrow R_3 + 3R_1$ 得到 $[\,0 \;\; 0 \mid h + 6\,]$;把全 0 列換到最下面才是梯形:$\left[\begin{array}{rr|r} 1 & -2 & 2 \\ 0 & 0 & h + 6 \\ 0 & 0 & 0 \end{array}\right]$。
- (a) 相容 ⇔ $h = -6$(此時 $\mathbf{v}_3 = 2\mathbf{v}_1$)。
- (b) **不管 $h$ 是多少都相依**:$\mathbf{v}_2 = -2\mathbf{v}_1$,所以 $2\mathbf{v}_1 + \mathbf{v}_2 + 0\mathbf{v}_3 = \mathbf{0}$ 永遠是一條相依關係。

#### 備註
Exercise 10 很適合討論:(a) 和 (b) 的答案**不一樣**。$\mathbf{v}_3$ 不在 Span 裡,整組照樣可以相依——多餘的是 $\mathbf{v}_2$,不是 $\mathbf{v}_3$。

### 變化 · Lay 1.7 Exercises 11–14
Find the value(s) of $h$ for which the vectors are linearly *dependent*. Justify each answer.

(11) $\begin{bmatrix} 1 \\ -1 \\ 4 \end{bmatrix}, \begin{bmatrix} 3 \\ -5 \\ 7 \end{bmatrix}, \begin{bmatrix} -1 \\ 5 \\ h \end{bmatrix}$  (12) $\begin{bmatrix} 2 \\ -4 \\ 1 \end{bmatrix}, \begin{bmatrix} -6 \\ 7 \\ -3 \end{bmatrix}, \begin{bmatrix} 8 \\ h \\ 4 \end{bmatrix}$

(13) $\begin{bmatrix} 1 \\ 5 \\ -3 \end{bmatrix}, \begin{bmatrix} -2 \\ -9 \\ 6 \end{bmatrix}, \begin{bmatrix} 3 \\ h \\ -9 \end{bmatrix}$  (14) $\begin{bmatrix} 1 \\ -3 \\ 4 \end{bmatrix}, \begin{bmatrix} -6 \\ 8 \\ 7 \end{bmatrix}, \begin{bmatrix} 4 \\ -2 \\ h \end{bmatrix}$

#### 解答
(11) $\begin{bmatrix} 1 & 3 & -1 \\ -1 & -5 & 5 \\ 4 & 7 & h \end{bmatrix} \sim \begin{bmatrix} 1 & 3 & -1 \\ 0 & -2 & 4 \\ 0 & -5 & h + 4 \end{bmatrix} \sim \begin{bmatrix} 1 & 3 & -1 \\ 0 & -2 & 4 \\ 0 & 0 & h - 6 \end{bmatrix}$。第三行沒有 pivot ⇔ $h = 6$。相依 ⇔ $h = 6$(書後解答相同)。

(12) **所有 $h$ 都相依**。矩陣 $\begin{bmatrix} 2 & -6 & 8 \\ -4 & 7 & h \\ 1 & -3 & 4 \end{bmatrix}$ 的第 1 列是第 3 列的 2 倍,$R_1 \leftarrow R_1 - 2R_3$ 得到全 0 列,最多 2 個 pivot,3 行中一定有一行不是 pivot 行。

(13) **所有 $h$ 都相依**(書後解答相同)。第 3 列是第 1 列的 $-3$ 倍,$R_3 \leftarrow R_3 + 3R_1$ 得到全 0 列,理由同 (12)。

(14) $\begin{bmatrix} 1 & -6 & 4 \\ -3 & 8 & -2 \\ 4 & 7 & h \end{bmatrix} \sim \begin{bmatrix} 1 & -6 & 4 \\ 0 & -10 & 10 \\ 0 & 31 & h - 16 \end{bmatrix} \sim \begin{bmatrix} 1 & -6 & 4 \\ 0 & -10 & 10 \\ 0 & 0 & h + 15 \end{bmatrix}$。相依 ⇔ $h = -15$。

#### 備註
(12)(13) 的「所有 $h$」是陷阱:學生化簡後找不到含 $h$ 的 pivot 條件,常以為「沒有 $h$ 讓它相依」。提醒他們:**列成比例 → 一定有全 0 列 → 行數 3 大於 pivot 數**。

### 變化 · Lay 1.7 Exercises 29–32
Describe the possible echelon forms of the matrix. Use the notation of Example 1 in Section 1.2.

(29) $A$ is a $3 \times 3$ matrix with linearly independent columns. (30) $A$ is a $2 \times 2$ matrix with linearly dependent columns. (31) $A$ is a $4 \times 2$ matrix, $A = [\,\mathbf{a}_1 \;\; \mathbf{a}_2\,]$, and $\mathbf{a}_2$ is not a multiple of $\mathbf{a}_1$. (32) $A$ is a $4 \times 3$ matrix, $A = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_3\,]$, such that $\{\mathbf{a}_1, \mathbf{a}_2\}$ is linearly independent and $\mathbf{a}_3$ is not in $\operatorname{Span}\{\mathbf{a}_1, \mathbf{a}_2\}$.

#### 解答
■ 表示不為 0 的 pivot,$*$ 表示任意數。

(29) 各行獨立 ⇔ 每一行都是 pivot 行:$\begin{bmatrix} ■ & * & * \\ 0 & ■ & * \\ 0 & 0 & ■ \end{bmatrix}$(書後解答相同)。

(30) 相依 ⇔ 最多 1 個 pivot:$\begin{bmatrix} ■ & * \\ 0 & 0 \end{bmatrix}$、$\begin{bmatrix} 0 & ■ \\ 0 & 0 \end{bmatrix}$、$\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$。

(31) $\mathbf{a}_2$ 不是 $\mathbf{a}_1$ 的倍數,所以 $\mathbf{a}_2 \neq \mathbf{0}$。若 $\mathbf{a}_1 \neq \mathbf{0}$,兩行獨立:$\begin{bmatrix} ■ & * \\ 0 & ■ \\ 0 & 0 \\ 0 & 0 \end{bmatrix}$;若 $\mathbf{a}_1 = \mathbf{0}$(此時 $\mathbf{a}_2$ 仍然不是它的倍數):$\begin{bmatrix} 0 & ■ \\ 0 & 0 \\ 0 & 0 \\ 0 & 0 \end{bmatrix}$(書後解答列出這兩種)。

(32) $\mathbf{a}_1 \neq \mathbf{0}$、$\mathbf{a}_2$ 不是 $\mathbf{a}_1$ 的倍數、$\mathbf{a}_3$ 不在前兩個的 Span 裡,由觀念 4 的 Theorem 7,三行獨立:$\begin{bmatrix} ■ & * & * \\ 0 & ■ & * \\ 0 & 0 & ■ \\ 0 & 0 & 0 \end{bmatrix}$。

#### 備註
Exercise 31 的第二種形狀($\mathbf{a}_1 = \mathbf{0}$)幾乎沒有學生想到,是觀念 5 Theorem 9 的伏筆。

### 變化 · Lay 1.7 Exercises 33–34
(33) How many pivot columns must a $7 \times 5$ matrix have if its columns are linearly independent? Why? (34) How many pivot columns must a $5 \times 7$ matrix have if its columns span $\mathbb{R}^5$? Why?

#### 解答
(33) **5 個**,也就是每一行。否則 $A\mathbf{x} = \mathbf{0}$ 會有自由變數,各行就相依了(書後解答相同)。

(34) **5 個**。由上週的 Theorem 4,各行生成 ℝ⁵ ⇔ 每一**列**都有 pivot;5 列就是 5 個 pivot,也就是 5 個 pivot 行(另外 2 行是自由的)。

#### 備註
兩題並排,正好對照「獨立看行、生成看列」。

### 變化 · Lay 1.7 Exercises 35–36
(35) Construct $3 \times 2$ matrices $A$ and $B$ such that $A\mathbf{x} = \mathbf{0}$ has only the trivial solution and $B\mathbf{x} = \mathbf{0}$ has a nontrivial solution.

(36) Answer both parts.

- **a.** Fill in the blank in the following statement: "If $A$ is an $m \times n$ matrix, then the columns of $A$ are linearly independent if and only if $A$ has \_\_\_\_\_ pivot columns."
- **b.** Explain why the statement in (a) is true.

#### 解答
(35) 例如 $A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$(兩行都不為 0,也不是彼此的倍數 → 獨立)、$B = \begin{bmatrix} 1 & 2 \\ 1 & 2 \\ 1 & 2 \end{bmatrix}$(第二行是第一行的 2 倍,$B\begin{bmatrix} 2 \\ -1 \end{bmatrix} = \mathbf{0}$)。答案不唯一(書後解答:$A$ 取兩行都不為 0 且不成倍數;$B$ 取一行是另一行的倍數)。

(36) a. **$n$ 個**。b. 各行獨立 ⇔ $A\mathbf{x} = \mathbf{0}$ 只有平凡解 ⇔ 沒有自由變數 ⇔ $n$ 個變數全是基本變數 ⇔ $n$ 行全是 pivot 行。

### 變化 · Lay 1.7 Exercises 37–38
Exercises 37 and 38 should be solved *without performing row operations*. [*Hint:* Write $A\mathbf{x} = \mathbf{0}$ as a vector equation.]

(37) Given $A = \begin{bmatrix} 2 & 3 & 5 \\ -5 & 1 & -4 \\ -3 & -1 & -4 \\ 1 & 0 & 1 \end{bmatrix}$, observe that the third column is the sum of the first two columns. Find a nontrivial solution of $A\mathbf{x} = \mathbf{0}$.

(38) Given $A = \begin{bmatrix} 5 & 1 & 8 \\ -9 & 5 & 6 \\ 6 & -5 & -9 \end{bmatrix}$, observe that the first column plus three times the second column equals the third column. Find a nontrivial solution of $A\mathbf{x} = \mathbf{0}$.

#### 解答
(37) $\mathbf{a}_3 = \mathbf{a}_1 + \mathbf{a}_2$,移項得 $1\mathbf{a}_1 + 1\mathbf{a}_2 - 1\mathbf{a}_3 = \mathbf{0}$。權重就是解:$\mathbf{x} = \begin{bmatrix} 1 \\ 1 \\ -1 \end{bmatrix}$(書後解答相同)。

(38) $\mathbf{a}_1 + 3\mathbf{a}_2 = \mathbf{a}_3$,移項得 $1\mathbf{a}_1 + 3\mathbf{a}_2 - 1\mathbf{a}_3 = \mathbf{0}$,所以 $\mathbf{x} = \begin{bmatrix} 1 \\ 3 \\ -1 \end{bmatrix}$。

#### 備註
這兩題最能讓學生體會「$A\mathbf{x} = \mathbf{0}$ 的解 = 各行之間的相依關係」:看出行之間的關係,解就直接寫得出來,完全不用化簡。

### 應用 · Lay 1.7 Exercises 47–48
**[T]** In Exercises 47 and 48, use as many columns of $A$ as possible to construct a matrix $B$ with the property that the equation $B\mathbf{x} = \mathbf{0}$ has only the trivial solution. Solve $B\mathbf{x} = \mathbf{0}$ to verify your work.

(47) $A = \begin{bmatrix} 8 & -3 & 0 & -7 & 2 \\ -9 & 4 & 5 & 11 & -7 \\ 6 & -2 & 2 & -4 & 4 \\ 5 & -1 & 7 & 0 & 10 \end{bmatrix}$

(48) $A = \begin{bmatrix} 12 & 10 & -6 & -3 & 7 & 10 \\ -7 & -6 & 4 & 7 & -9 & 5 \\ 9 & 9 & -9 & -5 & 5 & -1 \\ -4 & -3 & 1 & 6 & -8 & 9 \\ 8 & 7 & -5 & -9 & 11 & -8 \end{bmatrix}$

#### 解答
做法:化簡 $A$,**挑出 pivot 行**。

(47) $A$ 的 RREF 是 $\begin{bmatrix} 1 & 0 & 3 & 1 & 0 \\ 0 & 1 & 8 & 5 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$,pivot 行是第 1、2、5 行。取 $B = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_5\,] = \begin{bmatrix} 8 & -3 & 2 \\ -9 & 4 & -7 \\ 6 & -2 & 4 \\ 5 & -1 & 10 \end{bmatrix}$;$B$ 化簡後三行都有 pivot,$B\mathbf{x} = \mathbf{0}$ 只有平凡解(書後解答相同,其他選法也可以)。

(48) $A$ 的 RREF 是 $\begin{bmatrix} 1 & 0 & 2 & 0 & 2 & 0 \\ 0 & 1 & -3 & 0 & -2 & 0 \\ 0 & 0 & 0 & 1 & -1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$,pivot 行是第 1、2、4、6 行。取 $B = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_4 \;\; \mathbf{a}_6\,]$。

#### 備註
課本標 T,實作課 ④ 用 `rref()` 做。

### 應用 · Lay 1.7 Exercises 49–50
**[T]** (49) With $A$ and $B$ as in Exercise 47 select a column $\mathbf{v}$ of $A$ that was not used in the construction of $B$ and determine if $\mathbf{v}$ is in the set spanned by the columns of $B$. (Describe your calculations.) (50) Repeat Exercise 49 with the matrices $A$ and $B$ from Exercise 48. Then give an explanation for what you discover, assuming that $B$ was constructed as specified.

#### 解答
(49) 取 $\mathbf{v} = \mathbf{a}_3 = (0, 5, 2, 7)$。化簡 $[\,B \;\; \mathbf{v}\,]$ 得相容的方程組,解出 $\mathbf{a}_3 = 3\mathbf{a}_1 + 8\mathbf{a}_2 + 0\mathbf{a}_5$,**在** Span 裡。同樣 $\mathbf{a}_4 = \mathbf{a}_1 + 5\mathbf{a}_2$。(書後解答:$A$ 中沒用到的每一行都在 $B$ 各行的 Span 裡。)這兩組權重其實就寫在 $A$ 的 RREF 第 3、4 行裡。

(50) 沒用到的是 $\mathbf{a}_3$、$\mathbf{a}_5$:$\mathbf{a}_3 = 2\mathbf{a}_1 - 3\mathbf{a}_2$,$\mathbf{a}_5 = 2\mathbf{a}_1 - 2\mathbf{a}_2 - \mathbf{a}_4$,都在 Span 裡。

**原因**:$B$ 已經用了「盡可能多」的行。如果某個沒用到的行 $\mathbf{v}$ 不在 $B$ 各行的 Span 裡,把 $\mathbf{v}$ 加進 $B$,各行仍然獨立(觀念 4 的 Theorem 7:沒有任何一個向量是前面的組合),這就和「盡可能多」矛盾。

### 挑戰 · Lay 1.7 Exercises 45–46
(45) Suppose $A$ is an $m \times n$ matrix with the property that for all $\mathbf{b}$ in $\mathbb{R}^m$ the equation $A\mathbf{x} = \mathbf{b}$ has at most one solution. Use the definition of linear independence to explain why the columns of $A$ must be linearly independent.

(46) Suppose an $m \times n$ matrix $A$ has $n$ pivot columns. Explain why for each $\mathbf{b}$ in $\mathbb{R}^m$ the equation $A\mathbf{x} = \mathbf{b}$ has at most one solution. [*Hint:* Explain why $A\mathbf{x} = \mathbf{b}$ cannot have infinitely many solutions.]

#### 解答
(45) 取 $\mathbf{b} = \mathbf{0}$。$A\mathbf{x} = \mathbf{0}$ 有平凡解 $\mathbf{x} = \mathbf{0}$,而依假設最多只有一個解,所以**只有**平凡解:$x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n = \mathbf{0}$ 迫使 $x_1 = \cdots = x_n = 0$。依定義,各行線性獨立。

(46) $n$ 個 pivot 行代表每一行都是 pivot 行,係數部分沒有自由變數。若 $A\mathbf{x} = \mathbf{b}$ 無解,解有 0 個;若有解,沒有自由變數就只有一個(第 1 週的 Theorem 2)。不可能無限多個,因為那需要自由變數。所以最多一個解。

#### 備註
書後解答對 Exercise 45 只寫「請先自己寫,再看 Study Guide」。這題是「線性獨立 ⇔ 唯一性」的關鍵連結,第 4 週的「一對一」會再用到。

## 驗算
```check
Matrix([[1, 4, 2], [2, 5, 1], [3, 6, 0]]).rref()[0] == Matrix([[1, 0, -2], [0, 1, 1], [0, 0, 0]])
10 * Matrix([1, 2, 3]) - 5 * Matrix([4, 5, 6]) + 5 * Matrix([2, 1, 0]) == zeros(3, 1)
Matrix([[0, 1, 4], [1, 2, -1], [5, 8, 0]]).rank() == 3
Matrix([[5, 7, -2], [1, 2, -1], [0, -6, 6]]).rref()[0] == Matrix([[1, 0, 1], [0, 1, -1], [0, 0, 0]])
Matrix([5, 1, 0]) - Matrix([7, 2, -6]) == Matrix([-2, -1, 6])
Matrix([[0, 0, -3], [0, 5, 4], [2, -8, 1]]).rank() == 3
Matrix([[0, -8, 5], [3, -7, 4], [-1, 5, -4], [1, -3, 2]]).rank() == 3
Matrix([[-4, -3, 0], [0, -1, 4], [1, 0, 3], [5, 4, 6]]).rank() == 3
Matrix([[1, 2], [2, 4]]).rank() < 2
solve(Matrix([[1, -3, 2], [-3, 10, -7], [2, -6, h]]).det(), h) == [4]
Matrix([[1, -3, 2], [-3, 10, -7], [2, -6, 4]]).rref()[1] == (0, 1)
Matrix([[1, -2, 2], [-5, 10, -10], [-3, 6, h]]).det() == 0
Matrix([[1, -2, 2], [-5, 10, -10], [-3, 6, -6]]).rank() == 1
solve(Matrix([[1, 3, -1], [-1, -5, 5], [4, 7, h]]).det(), h) == [6]
Matrix([[2, -6, 8], [-4, 7, h], [1, -3, 4]]).det() == 0
Matrix([[1, -2, 3], [5, -9, h], [-3, 6, -9]]).det() == 0
solve(Matrix([[1, -6, 4], [-3, 8, -2], [4, 7, h]]).det(), h) == [-15]
Matrix([[1, 0], [0, 1], [0, 0]]).nullspace() == [] and Matrix([[1, 2], [1, 2], [1, 2]]) * Matrix([2, -1]) == zeros(3, 1)
Matrix([[2, 3, 5], [-5, 1, -4], [-3, -1, -4], [1, 0, 1]]) * Matrix([1, 1, -1]) == zeros(4, 1)
Matrix([[5, 1, 8], [-9, 5, 6], [6, -5, -9]]) * Matrix([1, 3, -1]) == zeros(3, 1)
Matrix([[8, -3, 0, -7, 2], [-9, 4, 5, 11, -7], [6, -2, 2, -4, 4], [5, -1, 7, 0, 10]]).rref()[1] == (0, 1, 4)
Matrix([[8, -3, 2], [-9, 4, -7], [6, -2, 4], [5, -1, 10]]).nullspace() == []
Matrix([[12, 10, -6, -3, 7, 10], [-7, -6, 4, 7, -9, 5], [9, 9, -9, -5, 5, -1], [-4, -3, 1, 6, -8, 9], [8, 7, -5, -9, 11, -8]]).rref()[1] == (0, 1, 3, 5)
Matrix([[12, 10, -3, 10], [-7, -6, 7, 5], [9, 9, -5, -1], [-4, -3, 6, 9], [8, 7, -9, -8]]).nullspace() == []
Matrix([[8, -3, 2], [-9, 4, -7], [6, -2, 4], [5, -1, 10]]) * Matrix([3, 8, 0]) == Matrix([0, 5, 2, 7])
Matrix([[8, -3, 2], [-9, 4, -7], [6, -2, 4], [5, -1, 10]]) * Matrix([1, 5, 0]) == Matrix([-7, 11, -4, 0])
Matrix([[12, 10, -3, 10], [-7, -6, 7, 5], [9, 9, -5, -1], [-4, -3, 6, 9], [8, 7, -9, -8]]) * Matrix([2, -3, 0, 0]) == Matrix([-6, 4, -9, 1, -5])
Matrix([[12, 10, -3, 10], [-7, -6, 7, 5], [9, 9, -5, -1], [-4, -3, 6, 9], [8, 7, -9, -8]]) * Matrix([2, -2, -1, 0]) == Matrix([7, -9, 5, -8, 11])
```
