---
title_en: Vectors in R² and Rⁿ
title_zh: ℝ² 與 ℝⁿ 中的向量
sub: A vector is an ordered list of numbers — and also a point, and also an arrow
level: basic
source: Lay 1.3
lab_hook: "NumPy 的一維陣列 `np.array([3, -1])`;`u + v`、`4 * u` 都是逐分量運算"
---
## 觀念
A matrix with only one column is called a **column vector** or simply a **vector**. The set of all vectors with two entries is denoted by $\mathbb{R}^2$ (read "r-two"). Two vectors in $\mathbb{R}^2$ are **equal** if and only if their corresponding entries are equal. Given two vectors $\mathbf{u}$ and $\mathbf{v}$, their **sum** $\mathbf{u} + \mathbf{v}$ is obtained by adding corresponding entries. Given a vector $\mathbf{u}$ and a real number $c$, the **scalar multiple** $c\mathbf{u}$ is obtained by multiplying each entry of $\mathbf{u}$ by $c$; the number $c$ is called a **scalar**.

**Parallelogram Rule for Addition.** If $\mathbf{u}$ and $\mathbf{v}$ in $\mathbb{R}^2$ are represented as points in the plane, then $\mathbf{u} + \mathbf{v}$ corresponds to the fourth vertex of the parallelogram whose other vertices are $\mathbf{u}$, $\mathbf{0}$, and $\mathbf{v}$.

If $n$ is a positive integer, $\mathbb{R}^n$ denotes the collection of all lists (or *ordered $n$-tuples*) of $n$ real numbers, usually written as $n \times 1$ column matrices. The vector whose entries are all zero is the **zero vector** $\mathbf{0}$.

**Algebraic Properties of $\mathbb{R}^n$.** For all $\mathbf{u}, \mathbf{v}, \mathbf{w}$ in $\mathbb{R}^n$ and all scalars $c$ and $d$:

$$\begin{array}{ll} \text{(i)} \;\; \mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u} & \text{(v)} \;\; c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v} \\ \text{(ii)} \;\; (\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w}) & \text{(vi)} \;\; (c + d)\mathbf{u} = c\mathbf{u} + d\mathbf{u} \\ \text{(iii)} \;\; \mathbf{u} + \mathbf{0} = \mathbf{0} + \mathbf{u} = \mathbf{u} & \text{(vii)} \;\; c(d\mathbf{u}) = (cd)\mathbf{u} \\ \text{(iv)} \;\; \mathbf{u} + (-\mathbf{u}) = -\mathbf{u} + \mathbf{u} = \mathbf{0} & \text{(viii)} \;\; 1\mathbf{u} = \mathbf{u} \end{array}$$

where $-\mathbf{u}$ denotes $(-1)\mathbf{u}$. The vector $\mathbf{u} + (-1)\mathbf{v}$ is written $\mathbf{u} - \mathbf{v}$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| column vector / vector | 行向量 / 向量 | 只有一行(直的)的矩陣;課本說「向量」都是指行向量 |
| entry | 分量 | 向量裡的每一個數 |
| $\mathbb{R}^2$、$\mathbb{R}^n$ | ℝ²、ℝⁿ | 所有「有 2 個(或 $n$ 個)實數分量」的向量組成的集合 |
| equal vectors | 相等的向量 | 對應的分量全部相等(順序也要一樣) |
| sum | 和 | 對應分量相加 |
| scalar | 純量 | 一個普通的數,用來放大、縮小向量 |
| scalar multiple | 純量倍數 | 每個分量都乘上同一個數 |
| parallelogram rule | 平行四邊形法則 | $\mathbf{u} + \mathbf{v}$ 是以 $\mathbf{u}$、$\mathbf{0}$、$\mathbf{v}$ 為三頂點的平行四邊形的第四個頂點 |
| zero vector | 零向量 | 分量全是 0 的向量 $\mathbf{0}$ |
| ordered $n$-tuple | 有序 $n$ 元組 | 有順序的 $n$ 個數,$(3, -1)$ 和 $(-1, 3)$ 不一樣 |

## 白話說
**向量就是一串有順序的數**,直的寫成一行。$\begin{bmatrix} 3 \\ -1 \end{bmatrix}$ 是 ℝ² 的向量(兩個分量),$\begin{bmatrix} 2 \\ 3 \\ 4 \end{bmatrix}$ 是 ℝ³ 的向量。順序很重要:$\begin{bmatrix} 4 \\ 7 \end{bmatrix}$ 和 $\begin{bmatrix} 7 \\ 4 \end{bmatrix}$ 是不同的向量。

向量只有兩種基本運算,都是**逐個分量**做:

- **相加**:對應位置相加。$\begin{bmatrix} 1 \\ -2 \end{bmatrix} + \begin{bmatrix} 2 \\ 5 \end{bmatrix} = \begin{bmatrix} 3 \\ 3 \end{bmatrix}$。
- **純量倍數**:每個分量乘同一個數。$5\begin{bmatrix} 3 \\ -1 \end{bmatrix} = \begin{bmatrix} 15 \\ -5 \end{bmatrix}$。

這兩種運算滿足我們熟悉的所有運算律(交換律、結合律、分配律……),所以向量可以像數字一樣移項、合併同類項。

**寫法小提醒**:課本為了省空間,有時把行向量寫成 $(3, -1)$(用小括號和逗號)。這仍然是**直的**行向量,和 $1 \times 2$ 的橫列矩陣 $[\,3 \;\; -1\,]$(方括號、沒有逗號)不一樣。

## 幾何意義
ℝ² 的向量有兩種畫法:畫成平面上的**一個點** $(a, b)$,或畫成從原點指向那個點的**箭頭**。兩種看法都對,看哪個方便就用哪個。

**加法 = 平行四邊形的對角線**。以 $\mathbf{u}$、$\mathbf{v}$ 為兩邊畫平行四邊形,從原點出發的對角線就是 $\mathbf{u} + \mathbf{v}$:

![平行四邊形法則(課本 Example 2):u = (2, 2)、v = (−6, 1),u + v = (−4, 3)。](parallelogram.svg)

**純量倍數 = 沿同一條線伸縮**。$c\mathbf{u}$ 的長度是 $\mathbf{u}$ 的 $|c|$ 倍;$c > 0$ 同方向,$c < 0$ 反方向。所有的 $c\mathbf{u}$ 合起來,剛好是**一條通過原點的直線**:

![純量倍數(課本 Example 3):u、2u、−(2/3)u 都落在同一條通過原點的直線上。](multiples.svg)

**減法**:$\mathbf{u} - \mathbf{v} = \mathbf{u} + (-\mathbf{v})$,是以 $\mathbf{u}$、$\mathbf{0}$、$-\mathbf{v}$ 為三頂點的平行四邊形的第四個頂點(課本 Figure 7)。ℝ³ 的向量則是三維空間裡的點或箭頭(課本 Figure 6)。

## 在資工哪裡用
程式裡的向量就是**一維陣列**:NumPy 的 `np.array([3, -1])`。`u + v`、`4 * u` 在 NumPy 裡都是逐分量運算,和課本的定義一模一樣。

資工處處是向量:遊戲角色的位置與速度是 ℝ² 或 ℝ³ 的向量;一張 28×28 的灰階手寫數字圖片,攤平之後就是 ℝ⁷⁸⁴ 的向量;推薦系統把每個使用者表示成「對每部電影的評分」組成的向量。**ℝⁿ 的 $n$ 可以很大**,但加法和純量倍數的規則完全一樣。

## 原理
**為什麼運算律成立?** 因為向量的運算是逐分量定義的,每一個分量都只是普通的實數運算。例如交換律 (i):

$$\mathbf{u} + \mathbf{v} = (u_1 + v_1, \dots, u_n + v_n) = (v_1 + u_1, \dots, v_n + u_n) = \mathbf{v} + \mathbf{u},$$

中間那一步用的是「實數加法可交換」。其他七條運算律都是同一個模式(Practice Problem 1、Exercises 41–42)。

**為什麼平行四邊形法則成立?** 從原點走到 $\mathbf{u}$,再平移 $\mathbf{v}$ 的長度與方向,就到了 $\mathbf{u} + \mathbf{v}$;反過來先走 $\mathbf{v}$ 再走 $\mathbf{u}$ 也到同一點(交換律)。兩條路徑正好圍成平行四邊形。

**為什麼所有倍數是一條直線?** $c\mathbf{u} = (cu_1, cu_2)$,當 $c$ 跑遍所有實數,這些點都滿足 $u_2 x_1 - u_1 x_2 = 0$(一條通過原點的直線方程式),而且這條線上的每一點都能寫成某個 $c\mathbf{u}$($\mathbf{u} \neq \mathbf{0}$ 時)。

## 老師講解
### 例 1 · Lay 1.3 Example 1
Given $\mathbf{u} = \begin{bmatrix} 1 \\ -2 \end{bmatrix}$ and $\mathbf{v} = \begin{bmatrix} 2 \\ -5 \end{bmatrix}$, find $4\mathbf{u}$, $(-3)\mathbf{v}$, and $4\mathbf{u} + (-3)\mathbf{v}$.

1. **純量倍數是每個分量都乘同一個數**。$4\mathbf{u} = \begin{bmatrix} 4 \cdot 1 \\ 4 \cdot (-2) \end{bmatrix} = \begin{bmatrix} 4 \\ -8 \end{bmatrix}$。
2. 負數也一樣,只是要小心正負號:$(-3)\mathbf{v} = \begin{bmatrix} (-3) \cdot 2 \\ (-3) \cdot (-5) \end{bmatrix} = \begin{bmatrix} -6 \\ 15 \end{bmatrix}$。負負得正。
3. **相加是對應分量相加**,上面加上面、下面加下面:
   $$4\mathbf{u} + (-3)\mathbf{v} = \begin{bmatrix} 4 \\ -8 \end{bmatrix} + \begin{bmatrix} -6 \\ 15 \end{bmatrix} = \begin{bmatrix} 4 + (-6) \\ -8 + 15 \end{bmatrix} = \begin{bmatrix} -2 \\ 7 \end{bmatrix}.$$
4. 這種「先各自放大縮小、再相加」的組合,下一個觀念會正式命名為**線性組合**。

### 例 2 · Lay 1.3 Example 2
The vectors $\mathbf{u} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} -6 \\ 1 \end{bmatrix}$, and $\mathbf{u} + \mathbf{v}$ are displayed in the figure. Verify the parallelogram rule.

1. **先用代數算**:$\mathbf{u} + \mathbf{v} = \begin{bmatrix} 2 + (-6) \\ 2 + 1 \end{bmatrix} = \begin{bmatrix} -4 \\ 3 \end{bmatrix}$。
2. **再用圖驗證**:從 $\mathbf{u} = (2, 2)$ 出發,往 $\mathbf{v}$ 的方向走「左 6、上 1」,到達 $(2 - 6, 2 + 1) = (-4, 3)$。
3. 這一步走的,正好是平行四邊形中和 $\mathbf{v}$ 平行、等長的那條邊。所以 $(-4, 3)$ 是以 $\mathbf{0}$、$\mathbf{u}$、$\mathbf{v}$ 為三頂點的平行四邊形的第四個頂點(見「幾何意義」的圖)。
4. **結論**:代數(對應分量相加)和幾何(平行四邊形)得到同一個點。兩種看法互相印證,之後看到向量加法,腦中可以同時浮現這兩個畫面。

### 例 3 · Lay 1.3 Example 3
Let $\mathbf{u} = \begin{bmatrix} 3 \\ -1 \end{bmatrix}$. Display the vectors $\mathbf{u}$, $2\mathbf{u}$, and $-\tfrac23\mathbf{u}$ on a graph.

1. **先算座標**:$2\mathbf{u} = \begin{bmatrix} 6 \\ -2 \end{bmatrix}$;$-\tfrac23\mathbf{u} = \begin{bmatrix} -\tfrac23 \cdot 3 \\ -\tfrac23 \cdot (-1) \end{bmatrix} = \begin{bmatrix} -2 \\ 2/3 \end{bmatrix}$。
2. **看長度**:$2\mathbf{u}$ 的箭頭是 $\mathbf{u}$ 的 2 倍長、方向相同;$-\tfrac23\mathbf{u}$ 的箭頭是 $\mathbf{u}$ 的 $\tfrac23$ 長、方向**相反**。一般來說,$c\mathbf{u}$ 的長度是 $\mathbf{u}$ 的 $|c|$ 倍。
3. **課本提醒**:從 $(0, 0)$ 到 $(a, b)$ 的長度是 $\sqrt{a^2 + b^2}$。例如 $\mathbf{u}$ 的長度是 $\sqrt{9 + 1} = \sqrt{10}$,$2\mathbf{u}$ 的長度是 $\sqrt{36 + 4} = \sqrt{40} = 2\sqrt{10}$,剛好兩倍。
4. **看位置**:三個點都在同一條通過原點的直線上(見「幾何意義」的圖)。所有 $c\mathbf{u}$ 合起來就是這整條直線——這是下一個觀念「Span」的第一個例子。

## 易錯點
- 純量倍數只乘了第一個分量,或忘了負號(例 1 的 $(-3)(-5) = 15$)。
- 把 $(3, -1)$ 當成橫的列矩陣。課本的 $(3, -1)$ 是**行向量**的省略寫法。
- 分量順序寫反:$(4, 7) \neq (7, 4)$。
- 以為「向量一定要從原點出發畫箭頭」。向量也可以只畫成一個點;箭頭只是方便看方向。

## 教學提示
這個觀念對學生不難,重點是**建立兩種畫面**:數字清單和箭頭。每算完一題就問「畫出來在哪裡?」。例 2 一定要在黑板上畫平行四邊形,讓學生看到「代數答案 = 圖上的第四個頂點」。

ℝⁿ 可以用資工例子帶:「一張 28×28 的圖片,就是 ℝ⁷⁸⁴ 的一個向量」,學生會意識到 $n$ 不只是 2 或 3。

課堂建議做:照做 1–2;是非題口頭問;Exercises 3–4 的畫圖留作業。

## 練習
### 照做 · Lay 1.3 Exercises 1–2
Compute $\mathbf{u} + \mathbf{v}$ and $\mathbf{u} - 2\mathbf{v}$.

(1) $\mathbf{u} = \begin{bmatrix} -1 \\ 2 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} -3 \\ 3 \end{bmatrix}$  (2) $\mathbf{u} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}$

#### 解答
(1) $\mathbf{u} + \mathbf{v} = \begin{bmatrix} -4 \\ 5 \end{bmatrix}$;$\mathbf{u} - 2\mathbf{v} = \begin{bmatrix} -1 + 6 \\ 2 - 6 \end{bmatrix} = \begin{bmatrix} 5 \\ -4 \end{bmatrix}$(書後解答相同)。

(2) $\mathbf{u} + \mathbf{v} = \begin{bmatrix} 5 \\ 5 \end{bmatrix}$;$\mathbf{u} - 2\mathbf{v} = \begin{bmatrix} 3 - 4 \\ 2 - 6 \end{bmatrix} = \begin{bmatrix} -1 \\ -4 \end{bmatrix}$。

#### 備註
建議課堂做。$\mathbf{u} - 2\mathbf{v}$ 最常錯的是 $-2 \times (-3)$ 的正負號。

### 照做 · Lay 1.3 Exercises 3–4
Display the following vectors using arrows on an $xy$-graph: $\mathbf{u}$, $\mathbf{v}$, $-\mathbf{v}$, $-2\mathbf{v}$, $\mathbf{u} + \mathbf{v}$, $\mathbf{u} - \mathbf{v}$, and $\mathbf{u} - 2\mathbf{v}$. Notice that $\mathbf{u} - \mathbf{v}$ is the vertex of a parallelogram whose other vertices are $\mathbf{u}$, $\mathbf{0}$, and $-\mathbf{v}$.

(3) $\mathbf{u}$ and $\mathbf{v}$ as in Exercise 1  (4) $\mathbf{u}$ and $\mathbf{v}$ as in Exercise 2

#### 解答
(3) $\mathbf{u} = (-1, 2)$、$\mathbf{v} = (-3, 3)$、$-\mathbf{v} = (3, -3)$、$-2\mathbf{v} = (6, -6)$、$\mathbf{u} + \mathbf{v} = (-4, 5)$、$\mathbf{u} - \mathbf{v} = (2, -1)$、$\mathbf{u} - 2\mathbf{v} = (5, -4)$。

![Exercise 3 的七個向量。](ex3-vectors.svg)

(4) $\mathbf{u} = (3, 2)$、$\mathbf{v} = (2, 3)$、$-\mathbf{v} = (-2, -3)$、$-2\mathbf{v} = (-4, -6)$、$\mathbf{u} + \mathbf{v} = (5, 5)$、$\mathbf{u} - \mathbf{v} = (1, -1)$、$\mathbf{u} - 2\mathbf{v} = (-1, -4)$。

![Exercise 4 的七個向量。](ex4-vectors.svg)

檢查平行四邊形:$\mathbf{u} - \mathbf{v} = \mathbf{u} + (-\mathbf{v})$,以 $\mathbf{u}$、$\mathbf{0}$、$-\mathbf{v}$ 為三頂點的平行四邊形的第四個頂點就是它。

#### 備註
作業。先算座標再畫,可以用 Exercise 1–2 的答案。

### 是非 · Lay 1.3 Exercise 23
**(T/F)** Another notation for the vector $\begin{bmatrix} -4 \\ 3 \end{bmatrix}$ is $[\,-4 \;\; 3\,]$.

#### 解答
**False.** $[\,-4 \;\; 3\,]$ 是 $1 \times 2$ 的列矩陣(橫的),形狀不同。行向量的省略寫法是 $(-4, 3)$(小括號加逗號,課本 p. 51)。

### 是非 · Lay 1.3 Exercise 24
**(T/F)** Any list of five real numbers is a vector in $\mathbb{R}^5$.

#### 解答
**True.** ℝ⁵ 就是所有「5 個實數的有序清單」組成的集合(課本 p. 53)。

### 是非 · Lay 1.3 Exercise 26
**(T/F)** The vector $\mathbf{u}$ results when a vector $\mathbf{u} - \mathbf{v}$ is added to the vector $\mathbf{v}$.

#### 解答
**True.** $(\mathbf{u} - \mathbf{v}) + \mathbf{v} = \mathbf{u} + (-\mathbf{v} + \mathbf{v}) = \mathbf{u} + \mathbf{0} = \mathbf{u}$,用到運算律 (ii)、(iv)、(iii)。

### 挑戰 · Lay 1.3 Practice Problem 1
Prove that $\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$ for any $\mathbf{u}$ and $\mathbf{v}$ in $\mathbb{R}^n$.

#### 解答
取任意 $\mathbf{u} = (u_1, \dots, u_n)$、$\mathbf{v} = (v_1, \dots, v_n)$:

$$\begin{aligned} \mathbf{u} + \mathbf{v} &= (u_1 + v_1, \dots, u_n + v_n) && \text{向量加法的定義} \\ &= (v_1 + u_1, \dots, v_n + u_n) && \text{實數加法可交換} \\ &= \mathbf{v} + \mathbf{u} && \text{向量加法的定義} \end{aligned}$$

(課本 p. 60)

### 挑戰 · Lay 1.3 Exercises 41–42
(41) Use the vectors $\mathbf{u} = (u_1, \dots, u_n)$, $\mathbf{v} = (v_1, \dots, v_n)$, and $\mathbf{w} = (w_1, \dots, w_n)$ to verify the following algebraic properties of $\mathbb{R}^n$: (a) $(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})$; (b) $c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v}$ for each scalar $c$.

(42) Use the vector $\mathbf{u} = (u_1, \dots, u_n)$ to verify the following algebraic properties of $\mathbb{R}^n$: (a) $\mathbf{u} + (-\mathbf{u}) = (-\mathbf{u}) + \mathbf{u} = \mathbf{0}$; (b) $c(d\mathbf{u}) = (cd)\mathbf{u}$ for all scalars $c$ and $d$.

#### 解答
做法和 Practice Problem 1 相同:**展開成分量 → 用實數的運算律 → 收回成向量**。

(41a) 第 $i$ 個分量:$(u_i + v_i) + w_i = u_i + (v_i + w_i)$(實數加法結合律)。
(41b) 第 $i$ 個分量:$c(u_i + v_i) = cu_i + cv_i$(實數分配律)。
(42a) 第 $i$ 個分量:$u_i + (-1)u_i = 0$,且 $(-1)u_i + u_i = 0$。
(42b) 第 $i$ 個分量:$c(du_i) = (cd)u_i$(實數乘法結合律)。

每一個分量都相等,所以兩邊的向量相等。

#### 備註
書後只給提示。重點是寫法:每一步都要註明用了哪個定義或哪條實數運算律。

## 驗算
```check
4*Matrix([1, -2]) == Matrix([4, -8])
(-3)*Matrix([2, -5]) == Matrix([-6, 15])
4*Matrix([1, -2]) - 3*Matrix([2, -5]) == Matrix([-2, 7])
Matrix([2, 2]) + Matrix([-6, 1]) == Matrix([-4, 3])
[2*Matrix([3, -1]), Rational(-2, 3)*Matrix([3, -1])] == [Matrix([6, -2]), Matrix([-2, Rational(2, 3)])]
[Matrix([-1, 2]) + Matrix([-3, 3]), Matrix([-1, 2]) - 2*Matrix([-3, 3])] == [Matrix([-4, 5]), Matrix([5, -4])]
[Matrix([3, 2]) + Matrix([2, 3]), Matrix([3, 2]) - 2*Matrix([2, 3])] == [Matrix([5, 5]), Matrix([-1, -4])]
[Matrix([-1, 2]) - Matrix([-3, 3]), Matrix([3, 2]) - Matrix([2, 3])] == [Matrix([2, -1]), Matrix([1, -1])]
```
