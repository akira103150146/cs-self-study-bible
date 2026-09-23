---
title_en: The Matrix Equation Ax = b
title_zh: 矩陣方程式 Ax = b
sub: Ax is the linear combination of the columns of A using the entries of x as weights
level: mid
source: Lay 1.4
lab_hook: "`A @ x`(矩陣乘向量);注意 `A * x` 是另一回事"
---
## 觀念
**Definition.** If $A$ is an $m \times n$ matrix, with columns $\mathbf{a}_1, \dots, \mathbf{a}_n$, and if $\mathbf{x}$ is in $\mathbb{R}^n$, then the **product of $A$ and $\mathbf{x}$**, denoted by $A\mathbf{x}$, is **the linear combination of the columns of $A$ using the corresponding entries in $\mathbf{x}$ as weights**; that is,

$$A\mathbf{x} = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \cdots \;\; \mathbf{a}_n\,]\begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix} = x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + \cdots + x_n\mathbf{a}_n.$$

$A\mathbf{x}$ is defined only if the number of columns of $A$ equals the number of entries in $\mathbf{x}$. An equation of the form $A\mathbf{x} = \mathbf{b}$ is called a **matrix equation**.

**Theorem 3.** If $A$ is an $m \times n$ matrix, with columns $\mathbf{a}_1, \dots, \mathbf{a}_n$, and if $\mathbf{b}$ is in $\mathbb{R}^m$, the matrix equation $A\mathbf{x} = \mathbf{b}$ has the same solution set as the vector equation $x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + \cdots + x_n\mathbf{a}_n = \mathbf{b}$, which, in turn, has the same solution set as the system of linear equations whose augmented matrix is $[\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \cdots \;\; \mathbf{a}_n \;\; \mathbf{b}\,]$.

**Existence of solutions.** The equation $A\mathbf{x} = \mathbf{b}$ has a solution if and only if $\mathbf{b}$ is a linear combination of the columns of $A$.

**Row–Vector Rule for Computing $A\mathbf{x}$.** If the product $A\mathbf{x}$ is defined, then the $i$th entry in $A\mathbf{x}$ is the sum of the products of corresponding entries from row $i$ of $A$ and from the vector $\mathbf{x}$.

The matrix with 1's on the diagonal and 0's elsewhere is called an **identity matrix** and is denoted by $I$ (or $I_n$). $I_n\mathbf{x} = \mathbf{x}$ for every $\mathbf{x}$ in $\mathbb{R}^n$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| product $A\mathbf{x}$ | 矩陣乘向量 | $A$ 各行的線性組合,權重是 $\mathbf{x}$ 的分量 |
| matrix equation | 矩陣方程式 | $A\mathbf{x} = \mathbf{b}$ 這種寫法 |
| row–vector rule | 列向量規則 | 第 $i$ 個分量 = 第 $i$ 列和 $\mathbf{x}$ 對應相乘再相加 |
| dot product | 內積(點積) | 兩串數對應相乘再相加;列向量規則的每一格就是一個內積 |
| identity matrix $I_n$ | 單位矩陣 | 對角線是 1、其餘是 0;$I\mathbf{x} = \mathbf{x}$ |
| defined / undefined | 有定義 / 沒有定義 | $A$ 的**行數**要等於 $\mathbf{x}$ 的分量數 |

## 白話說
這週最重要的一句話:**$A\mathbf{x}$ 就是 $A$ 各行的線性組合,權重是 $\mathbf{x}$ 的分量**。

$$\begin{bmatrix} 1 & 2 & -1 \\ 0 & -5 & 3 \end{bmatrix}\begin{bmatrix} 4 \\ 3 \\ 7 \end{bmatrix} = 4\begin{bmatrix} 1 \\ 0 \end{bmatrix} + 3\begin{bmatrix} 2 \\ -5 \end{bmatrix} + 7\begin{bmatrix} -1 \\ 3 \end{bmatrix} = \begin{bmatrix} 3 \\ 6 \end{bmatrix}$$

$\mathbf{x}$ 的第 1 個數乘 $A$ 的第 1 行、第 2 個數乘第 2 行……再全部加起來。所以:

- **形狀規則**:$A$ 有幾行,$\mathbf{x}$ 就要有幾個分量;結果的分量數等於 $A$ 的列數。$(m \times n)$ 乘 $(n \text{ 個分量})$ 得到 $(m \text{ 個分量})$。
- **三種寫法是同一件事**(Theorem 3):方程組、向量方程式、矩陣方程式 $A\mathbf{x} = \mathbf{b}$,解法都是化簡增廣矩陣 $[\,A \;\; \mathbf{b}\,]$。

手算時通常用**列向量規則**比較快:結果的第 $i$ 格 = $A$ 的第 $i$ 列和 $\mathbf{x}$「對應相乘再相加」。兩種算法答案一定一樣。

## 幾何意義
$A\mathbf{x} = \mathbf{b}$ 有沒有解,幾何上就是在問:**$\mathbf{b}$ 在不在 $A$ 各行的 Span 裡?**

- 若 $A$ 的兩行在 ℝ³ 中不平行,它們的 Span 是一個平面。$\mathbf{b}$ 在平面上就有解,不在就無解(Exercise 13)。
- 所以「解方程組」有兩種圖像:**列的觀點**(第 1 週:幾條直線、幾個平面的交點)和**行的觀點**(這週:用 $A$ 的行去組合出 $\mathbf{b}$)。兩種都對,之後的觀念大多用行的觀點。

## 在資工哪裡用
- **神經網路的一層就是 $W\mathbf{x} + \mathbf{b}$**:輸入向量 $\mathbf{x}$ 乘上權重矩陣 $W$。用行的觀點看,輸出是 $W$ 各行的線性組合,每個輸入特徵各自貢獻一行。
- **NumPy 寫 `A @ x`**。千萬不要寫成 `A * x`:那是逐元素相乘(broadcasting),不會報錯,但算的不是 $A\mathbf{x}$——實作課會親眼看到這個陷阱。
- **資料的存法影響速度**(課本的數值筆記):Fortran 把矩陣一行一行存,適合用「行的線性組合」算;C 語言(以及 NumPy 預設)一列一列存,適合用列向量規則。這就是**記憶體連續存取(cache)**的問題。

## 數值筆記
為了讓電腦算 $A\mathbf{x}$ 更快,運算順序應該配合資料在記憶體中**連續存放**的方式。最廣泛使用的專業矩陣運算程式是用 Fortran 寫的,Fortran 把矩陣**一行一行**存,所以這些演算法把 $A\mathbf{x}$ 當成 $A$ 各行的線性組合來算。相反地,如果程式是用 C 語言寫的(C 把矩陣**一列一列**存),$A\mathbf{x}$ 就應該用列向量規則來算。(改寫自 Lay 1.4 Numerical Note)

## 原理
**為什麼列向量規則和定義一樣?** 照定義 $A\mathbf{x} = x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n$,這個向量的第 $i$ 個分量,是每個 $x_j\mathbf{a}_j$ 的第 $i$ 個分量相加:

$$x_1a_{i1} + x_2a_{i2} + \cdots + x_na_{in},$$

而 $a_{i1}, a_{i2}, \dots, a_{in}$ 正是 $A$ 的第 $i$ 列。所以「第 $i$ 格 = 第 $i$ 列和 $\mathbf{x}$ 對應相乘再相加」。兩種算法只是加法的順序不同。

**為什麼 Theorem 3 成立?** 依定義,$A\mathbf{x} = \mathbf{b}$ 就是 $x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n = \mathbf{b}$(左邊一字不差);而觀念 2 已經說明向量方程式和增廣矩陣 $[\,\mathbf{a}_1 \;\cdots\; \mathbf{a}_n \;\; \mathbf{b}\,]$ 的方程組等價。

**為什麼 $I\mathbf{x} = \mathbf{x}$?** $I$ 的第 $j$ 行是 $\mathbf{e}_j$(第 $j$ 格是 1、其餘是 0)。$I\mathbf{x} = x_1\mathbf{e}_1 + \cdots + x_n\mathbf{e}_n$,第 $j$ 格剛好是 $x_j$。

## 老師講解
### 例 1 · Lay 1.4 Example 1
Compute (a) $\begin{bmatrix} 1 & 2 & -1 \\ 0 & -5 & 3 \end{bmatrix}\begin{bmatrix} 4 \\ 3 \\ 7 \end{bmatrix}$ and (b) $\begin{bmatrix} 2 & -3 \\ 8 & 0 \\ -5 & 2 \end{bmatrix}\begin{bmatrix} 4 \\ 7 \end{bmatrix}$ using the definition of $A\mathbf{x}$.

1. **先檢查形狀**:(a) $A$ 是 $2 \times 3$,有 3 行,$\mathbf{x}$ 有 3 個分量 ✓,結果會有 2 個分量。(b) $A$ 是 $3 \times 2$,有 2 行,$\mathbf{x}$ 有 2 個分量 ✓,結果有 3 個分量。
2. **(a) 照定義**:$\mathbf{x}$ 的 4、3、7 分別當 $A$ 三行的權重:
   $$4\begin{bmatrix} 1 \\ 0 \end{bmatrix} + 3\begin{bmatrix} 2 \\ -5 \end{bmatrix} + 7\begin{bmatrix} -1 \\ 3 \end{bmatrix} = \begin{bmatrix} 4 \\ 0 \end{bmatrix} + \begin{bmatrix} 6 \\ -15 \end{bmatrix} + \begin{bmatrix} -7 \\ 21 \end{bmatrix} = \begin{bmatrix} 3 \\ 6 \end{bmatrix}$$
3. **(b) 照定義**:權重 4、7 乘上兩行:
   $$4\begin{bmatrix} 2 \\ 8 \\ -5 \end{bmatrix} + 7\begin{bmatrix} -3 \\ 0 \\ 2 \end{bmatrix} = \begin{bmatrix} 8 \\ 32 \\ -20 \end{bmatrix} + \begin{bmatrix} -21 \\ 0 \\ 14 \end{bmatrix} = \begin{bmatrix} -13 \\ 32 \\ -6 \end{bmatrix}$$
4. **重點**:結果的大小由 $A$ 的**列數**決定,不是由 $\mathbf{x}$ 決定。

### 例 2 · Lay 1.4 Example 2
For $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$ in $\mathbb{R}^m$, write the linear combination $3\mathbf{v}_1 - 5\mathbf{v}_2 + 7\mathbf{v}_3$ as a matrix times a vector.

1. **反過來用定義**:定義說「矩陣乘向量 = 行的線性組合,權重放在向量裡」。
2. 所以把 $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$ **當成矩陣的三行**,把權重 $3, -5, 7$ **放進向量**:
   $$3\mathbf{v}_1 - 5\mathbf{v}_2 + 7\mathbf{v}_3 = [\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]\begin{bmatrix} 3 \\ -5 \\ 7 \end{bmatrix} = A\mathbf{x}.$$
3. **意義**:任何線性組合都能寫成 $A\mathbf{x}$(是非題 30)。這讓我們可以用一個精簡的符號,處理任意多個向量的組合。

### 例 3 · Lay 1.4(p. 62,方程組 → 矩陣方程式)
Write the system $x_1 + 2x_2 - x_3 = 4,\;\; -5x_2 + 3x_3 = 1$ as a vector equation and then as a matrix equation.

1. **向量方程式**:把每個未知數的係數直的收集成一個向量(第一條沒寫的地方係數是 0):
   $$x_1\begin{bmatrix} 1 \\ 0 \end{bmatrix} + x_2\begin{bmatrix} 2 \\ -5 \end{bmatrix} + x_3\begin{bmatrix} -1 \\ 3 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$$
2. **矩陣方程式**:左邊是線性組合,依例 2 寫成矩陣乘向量:
   $$\begin{bmatrix} 1 & 2 & -1 \\ 0 & -5 & 3 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$$
3. **觀察**:這個矩陣正是方程組的**係數矩陣**。所以任何方程組都能直接寫成 $A\mathbf{x} = \mathbf{b}$:$A$ 是係數矩陣,$\mathbf{x}$ 是未知數,$\mathbf{b}$ 是常數。
4. 三種寫法(方程組、向量方程式、矩陣方程式)的解集都一樣,解法都是化簡 $[\,A \;\; \mathbf{b}\,]$——這就是 Theorem 3。

### 例 4 · Lay 1.4 Examples 4–5
Compute $A\mathbf{x}$, where $A = \begin{bmatrix} 2 & 3 & 4 \\ -1 & 5 & -3 \\ 6 & -2 & 8 \end{bmatrix}$ and $\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}$. Then use the row–vector rule to compute $\begin{bmatrix} 1 & 2 & -1 \\ 0 & -5 & 3 \end{bmatrix}\begin{bmatrix} 4 \\ 3 \\ 7 \end{bmatrix}$ and $I_3\begin{bmatrix} r \\ s \\ t \end{bmatrix}$.

1. **照定義展開**:$x_1\begin{bmatrix} 2 \\ -1 \\ 6 \end{bmatrix} + x_2\begin{bmatrix} 3 \\ 5 \\ -2 \end{bmatrix} + x_3\begin{bmatrix} 4 \\ -3 \\ 8 \end{bmatrix} = \begin{bmatrix} 2x_1 + 3x_2 + 4x_3 \\ -x_1 + 5x_2 - 3x_3 \\ 6x_1 - 2x_2 + 8x_3 \end{bmatrix}$。
2. **觀察第一格**:$2x_1 + 3x_2 + 4x_3$ 正好是 $A$ 的**第一列** $(2, 3, 4)$ 和 $\mathbf{x}$ 對應相乘再相加。第二格、第三格也一樣。這就是**列向量規則**:不用寫出中間的三個向量,直接一列一列算。
3. **用列向量規則算例 1(a)**:第一格 $1 \cdot 4 + 2 \cdot 3 + (-1) \cdot 7 = 3$;第二格 $0 \cdot 4 + (-5) \cdot 3 + 3 \cdot 7 = 6$。答案 $(3, 6)$,和例 1 用定義算的一樣。
4. **單位矩陣**:$I_3\begin{bmatrix} r \\ s \\ t \end{bmatrix} = \begin{bmatrix} 1 \cdot r + 0 \cdot s + 0 \cdot t \\ 0 \cdot r + 1 \cdot s + 0 \cdot t \\ 0 \cdot r + 0 \cdot s + 1 \cdot t \end{bmatrix} = \begin{bmatrix} r \\ s \\ t \end{bmatrix}$。$I$ 乘任何向量都不改變它,像數字的 1。

## 易錯點
- 用 $A$ 的**列數**去和 $\mathbf{x}$ 的分量數比。要比的是 $A$ 的**行數**(Exercises 1–2)。
- 以為結果和 $\mathbf{x}$ 一樣大。結果的分量數是 $A$ 的**列數**。
- 把 $\mathbf{x}$ 的分量乘到 $A$ 的**列**上(把行和列搞混)。定義是乘在**行**上;列向量規則則是「列和 $\mathbf{x}$ 內積」。
- 在 NumPy 寫 `A * x`。那是逐元素相乘,不是 $A\mathbf{x}$。

## 教學提示
把「$A\mathbf{x}$ = 行的線性組合」寫成黑板上的標語,整學期都用得到(第 16 週的 SVD、PCA 都靠這一句)。

例 1 和例 4 要**同一題用兩種方法各算一次**,讓學生看到答案一樣,再說明:「定義讓我們**理解**,列向量規則讓我們**算得快**。」

課堂建議做:Exercises 1–4(含兩題「沒有定義」)、5–6;是非 Exercises 23–26、29–30、32 口頭問;再挑 Exercise 11 或 13。

## 練習
### 照做 · Lay 1.4 Exercises 1–2
Compute the product using (a) the definition, as in Example 1, and (b) the row–vector rule for computing $A\mathbf{x}$. If a product is undefined, explain why.

(1) $\begin{bmatrix} -4 & 2 \\ 1 & 6 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 3 \\ 1 \\ 7 \end{bmatrix}$  (2) $\begin{bmatrix} 2 \\ 6 \\ -1 \end{bmatrix}\begin{bmatrix} 1 \\ -1 \end{bmatrix}$

#### 解答
(1) **沒有定義**:矩陣是 $3 \times 2$,有 **2 行**,但向量有 **3 個**分量,數不合(書後解答相同)。

(2) **沒有定義**:左邊是 $3 \times 1$ 矩陣,只有 **1 行**,但向量有 2 個分量。

#### 備註
兩題都是「沒有定義」的陷阱。學生常比錯:(1) 的矩陣有 3 **列**、向量有 3 個分量,看起來「對得上」,其實要比的是**行**。

### 照做 · Lay 1.4 Exercises 3–4
Compute the product using (a) the definition and (b) the row–vector rule. If a product is undefined, explain why.

(3) $\begin{bmatrix} 6 & 5 \\ -4 & -3 \\ 7 & 6 \end{bmatrix}\begin{bmatrix} 1 \\ -3 \end{bmatrix}$  (4) $\begin{bmatrix} 8 & 3 & 1 \\ 5 & 1 & 2 \end{bmatrix}\begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$

#### 解答
(3) 定義:$1\begin{bmatrix} 6 \\ -4 \\ 7 \end{bmatrix} - 3\begin{bmatrix} 5 \\ -3 \\ 6 \end{bmatrix} = \begin{bmatrix} 6 - 15 \\ -4 + 9 \\ 7 - 18 \end{bmatrix} = \begin{bmatrix} -9 \\ 5 \\ -11 \end{bmatrix}$。

列向量規則:$6(1) + 5(-3) = -9$、$(-4)(1) + (-3)(-3) = 5$、$7(1) + 6(-3) = -11$。兩種方法答案相同(書後解答相同)。

(4) 定義:$1\begin{bmatrix} 8 \\ 5 \end{bmatrix} + 1\begin{bmatrix} 3 \\ 1 \end{bmatrix} + 1\begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 12 \\ 8 \end{bmatrix}$;列向量規則:$8 + 3 + 1 = 12$、$5 + 1 + 2 = 8$。

(乘上全是 1 的向量,等於把每一列加總。)

### 照做 · Lay 1.4 Exercises 5–6
Use the definition of $A\mathbf{x}$ to write the matrix equation as a vector equation.

(5) $\begin{bmatrix} 7 & 2 & -9 & 3 \\ -4 & -5 & 7 & -2 \end{bmatrix}\begin{bmatrix} 6 \\ -9 \\ 1 \\ -8 \end{bmatrix} = \begin{bmatrix} -9 \\ 44 \end{bmatrix}$  (6) $\begin{bmatrix} 7 & -3 \\ 2 & 1 \\ 9 & -6 \\ -3 & 2 \end{bmatrix}\begin{bmatrix} -2 \\ -5 \end{bmatrix} = \begin{bmatrix} 1 \\ -9 \\ 12 \\ -4 \end{bmatrix}$

#### 解答
把 $\mathbf{x}$ 的分量當權重,乘在 $A$ 的各行上:

(5) $6\begin{bmatrix} 7 \\ -4 \end{bmatrix} - 9\begin{bmatrix} 2 \\ -5 \end{bmatrix} + 1\begin{bmatrix} -9 \\ 7 \end{bmatrix} - 8\begin{bmatrix} 3 \\ -2 \end{bmatrix} = \begin{bmatrix} -9 \\ 44 \end{bmatrix}$(書後解答相同)

(6) $-2\begin{bmatrix} 7 \\ 2 \\ 9 \\ -3 \end{bmatrix} - 5\begin{bmatrix} -3 \\ 1 \\ -6 \\ 2 \end{bmatrix} = \begin{bmatrix} 1 \\ -9 \\ 12 \\ -4 \end{bmatrix}$

### 照做 · Lay 1.4 Exercises 7–8
Use the definition of $A\mathbf{x}$ to write the vector equation as a matrix equation.

(7) $x_1\begin{bmatrix} 4 \\ -1 \\ 7 \\ -4 \end{bmatrix} + x_2\begin{bmatrix} -5 \\ 3 \\ -5 \\ 1 \end{bmatrix} + x_3\begin{bmatrix} 7 \\ -8 \\ 0 \\ 2 \end{bmatrix} = \begin{bmatrix} 6 \\ -8 \\ 0 \\ -7 \end{bmatrix}$  (8) $z_1\begin{bmatrix} 4 \\ -2 \end{bmatrix} + z_2\begin{bmatrix} -4 \\ 5 \end{bmatrix} + z_3\begin{bmatrix} -5 \\ 4 \end{bmatrix} + z_4\begin{bmatrix} 3 \\ 0 \end{bmatrix} = \begin{bmatrix} 4 \\ 13 \end{bmatrix}$

#### 解答
把各個向量當成矩陣的行,權重收進未知向量:

(7) $\begin{bmatrix} 4 & -5 & 7 \\ -1 & 3 & -8 \\ 7 & -5 & 0 \\ -4 & 1 & 2 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 6 \\ -8 \\ 0 \\ -7 \end{bmatrix}$(書後解答相同)

(8) $\begin{bmatrix} 4 & -4 & -5 & 3 \\ -2 & 5 & 4 & 0 \end{bmatrix}\begin{bmatrix} z_1 \\ z_2 \\ z_3 \\ z_4 \end{bmatrix} = \begin{bmatrix} 4 \\ 13 \end{bmatrix}$

### 照做 · Lay 1.4 Exercises 9–10
Write the system first as a vector equation and then as a matrix equation.

(9) $4x_1 + x_2 - 7x_3 = 8,\;\; x_2 + 6x_3 = 0$  (10) $8x_1 - x_2 = 4,\;\; 5x_1 + 4x_2 = 1,\;\; x_1 - 3x_2 = 2$

#### 解答
(9) $x_1\begin{bmatrix} 4 \\ 0 \end{bmatrix} + x_2\begin{bmatrix} 1 \\ 1 \end{bmatrix} + x_3\begin{bmatrix} -7 \\ 6 \end{bmatrix} = \begin{bmatrix} 8 \\ 0 \end{bmatrix}$,以及 $\begin{bmatrix} 4 & 1 & -7 \\ 0 & 1 & 6 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 8 \\ 0 \end{bmatrix}$(書後解答相同)。

(10) $x_1\begin{bmatrix} 8 \\ 5 \\ 1 \end{bmatrix} + x_2\begin{bmatrix} -1 \\ 4 \\ -3 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \\ 2 \end{bmatrix}$,以及 $\begin{bmatrix} 8 & -1 \\ 5 & 4 \\ 1 & -3 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \\ 2 \end{bmatrix}$。

### 照做 · Lay 1.4 Practice Problem 1
Let $A = \begin{bmatrix} 1 & 5 & -2 & 0 \\ -3 & 1 & 9 & -5 \\ 4 & -8 & -1 & 7 \end{bmatrix}$, $\mathbf{p} = \begin{bmatrix} 3 \\ -2 \\ 0 \\ -4 \end{bmatrix}$, and $\mathbf{b} = \begin{bmatrix} -7 \\ 9 \\ 0 \end{bmatrix}$. It can be shown that $\mathbf{p}$ is a solution of $A\mathbf{x} = \mathbf{b}$. Use this fact to exhibit $\mathbf{b}$ as a specific linear combination of the columns of $A$.

#### 解答
$A\mathbf{p} = \mathbf{b}$,依定義 $A\mathbf{p}$ 就是 $A$ 的行以 $\mathbf{p}$ 的分量為權重的組合:

$$3\begin{bmatrix} 1 \\ -3 \\ 4 \end{bmatrix} - 2\begin{bmatrix} 5 \\ 1 \\ -8 \end{bmatrix} + 0\begin{bmatrix} -2 \\ 9 \\ -1 \end{bmatrix} - 4\begin{bmatrix} 0 \\ -5 \\ 7 \end{bmatrix} = \begin{bmatrix} -7 \\ 9 \\ 0 \end{bmatrix}$$

(課本 p. 68–69。不用做任何列運算。)

### 是非 · Lay 1.4 Exercise 23
**(T/F)** The equation $A\mathbf{x} = \mathbf{b}$ is referred to as a *vector equation*.

#### 解答
**False.** $A\mathbf{x} = \mathbf{b}$ 叫**矩陣方程式**;向量方程式是 $x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n = \mathbf{b}$(課本 p. 62)。

### 是非 · Lay 1.4 Exercise 24
**(T/F)** Every matrix equation $A\mathbf{x} = \mathbf{b}$ corresponds to a vector equation with the same solution set.

#### 解答
**True.** Theorem 3。

### 是非 · Lay 1.4 Exercise 25
**(T/F)** If the equation $A\mathbf{x} = \mathbf{b}$ is inconsistent, then $\mathbf{b}$ is not in the set spanned by the columns of $A$.

#### 解答
**True.** $A\mathbf{x} = \mathbf{b}$ 有解 ⇔ $\mathbf{b}$ 是 $A$ 各行的線性組合(課本 p. 63 方框);無解就代表 $\mathbf{b}$ 不在這些行的 Span 裡。

### 是非 · Lay 1.4 Exercise 26
**(T/F)** A vector $\mathbf{b}$ is a linear combination of the columns of a matrix $A$ if and only if the equation $A\mathbf{x} = \mathbf{b}$ has at least one solution.

#### 解答
**True.** 課本 p. 63 方框的敘述。

### 是非 · Lay 1.4 Exercise 29
**(T/F)** The first entry in the product $A\mathbf{x}$ is a sum of products.

#### 解答
**True.** 列向量規則:第一格是 $A$ 的第一列和 $\mathbf{x}$ 對應相乘再相加(課本 p. 64)。

### 是非 · Lay 1.4 Exercise 30
**(T/F)** Any linear combination of vectors can always be written in the form $A\mathbf{x}$ for a suitable matrix $A$ and vector $\mathbf{x}$.

#### 解答
**True.** 把那些向量當 $A$ 的行、權重當 $\mathbf{x}$(例 2)。

### 是非 · Lay 1.4 Exercise 32
**(T/F)** The solution set of a linear system whose augmented matrix is $[\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_3 \;\; \mathbf{b}\,]$ is the same as the solution set of $A\mathbf{x} = \mathbf{b}$, if $A = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_3\,]$.

#### 解答
**True.** Theorem 3。

### 變化 · Lay 1.4 Exercises 11–12
Given $A$ and $\mathbf{b}$, write the augmented matrix for the linear system that corresponds to the matrix equation $A\mathbf{x} = \mathbf{b}$. Then solve the system and write the solution as a vector.

(11) $A = \begin{bmatrix} 1 & 2 & 4 \\ 0 & 1 & 5 \\ -2 & -4 & -3 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} -2 \\ 2 \\ 9 \end{bmatrix}$  (12) $A = \begin{bmatrix} 1 & 2 & 1 \\ -3 & -1 & 2 \\ 0 & 5 & 3 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} 0 \\ 1 \\ -1 \end{bmatrix}$

#### 解答
(11) $[\,A \;\; \mathbf{b}\,] = \left[\begin{array}{rrr|r} 1 & 2 & 4 & -2 \\ 0 & 1 & 5 & 2 \\ -2 & -4 & -3 & 9 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 1 \end{array}\right]$,所以 $\mathbf{x} = \begin{bmatrix} 0 \\ -3 \\ 1 \end{bmatrix}$(書後解答相同)。

(12) $[\,A \;\; \mathbf{b}\,] \sim \left[\begin{array}{rrr|r} 1 & 0 & 0 & 3/5 \\ 0 & 1 & 0 & -4/5 \\ 0 & 0 & 1 & 1 \end{array}\right]$,所以 $\mathbf{x} = \begin{bmatrix} 3/5 \\ -4/5 \\ 1 \end{bmatrix}$。驗算第二列:$-3 \cdot \tfrac35 + \tfrac45 + 2 = 1$ ✓。

### 變化 · Lay 1.4 Exercises 13–14
(13) Let $\mathbf{u} = \begin{bmatrix} 0 \\ 4 \\ 4 \end{bmatrix}$ and $A = \begin{bmatrix} 3 & -5 \\ -2 & 6 \\ 1 & 1 \end{bmatrix}$. Is $\mathbf{u}$ in the plane in $\mathbb{R}^3$ spanned by the columns of $A$? Why or why not?

(14) Let $\mathbf{u} = \begin{bmatrix} 2 \\ -3 \\ 2 \end{bmatrix}$ and $A = \begin{bmatrix} 5 & 8 & 7 \\ 0 & 1 & -1 \\ 1 & 3 & 0 \end{bmatrix}$. Is $\mathbf{u}$ in the subset of $\mathbb{R}^3$ spanned by the columns of $A$? Why or why not?

#### 解答
(13) 化簡 $[\,A \;\; \mathbf{u}\,] \sim \left[\begin{array}{rr|r} 1 & 0 & 5/2 \\ 0 & 1 & 3/2 \\ 0 & 0 & 0 \end{array}\right]$,相容,**是**:$\mathbf{u} = \tfrac52\mathbf{a}_1 + \tfrac32\mathbf{a}_2$(書後解答:Yes)。

(14) 化簡 $[\,A \;\; \mathbf{u}\,]$,最後一行是 pivot 行(出現 $0 = $ 非零數)→ **不是**。原因是 $A$ 的三行其實只張成一個平面:第三行 $\mathbf{a}_3 = 3\mathbf{a}_1 - \mathbf{a}_2$ 沒有帶來新方向,而 $\mathbf{u}$ 不在這個平面上。

#### 備註
課本 Exercise 13 附了一張圖($A$ 兩行張出的平面與 $\mathbf{u}$),講義沒有重畫;這題用列化簡判斷即可,不需要看圖。

Exercise 14 的 $A$ 三行線性相依:$3\mathbf{a}_1 - \mathbf{a}_2 = (7, -1, 0) = \mathbf{a}_3$,所以 Span 只是平面。這是第 3 週「線性相依」的伏筆。

### 變化 · Lay 1.4 Exercises 35–36
(35) Note that $\begin{bmatrix} 3 & -4 & 2 \\ 6 & -3 & 4 \\ -8 & 9 & -5 \end{bmatrix}\begin{bmatrix} -4 \\ -1 \\ 3 \end{bmatrix} = \begin{bmatrix} -2 \\ -9 \\ 8 \end{bmatrix}$. Use this fact (and no row operations) to find scalars $c_1, c_2, c_3$ such that $\begin{bmatrix} -2 \\ -9 \\ 8 \end{bmatrix} = c_1\begin{bmatrix} 3 \\ 6 \\ -8 \end{bmatrix} + c_2\begin{bmatrix} -4 \\ -3 \\ 9 \end{bmatrix} + c_3\begin{bmatrix} 2 \\ 4 \\ -5 \end{bmatrix}$.

(36) Let $\mathbf{u} = \begin{bmatrix} 7 \\ 2 \\ 5 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} 3 \\ 1 \\ 3 \end{bmatrix}$, and $\mathbf{w} = \begin{bmatrix} 6 \\ 1 \\ 0 \end{bmatrix}$. It can be shown that $3\mathbf{u} - 5\mathbf{v} - \mathbf{w} = \mathbf{0}$. Use this fact (and no row operations) to find $x_1$ and $x_2$ that satisfy the equation $\begin{bmatrix} 7 & 3 \\ 2 & 1 \\ 5 & 3 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 6 \\ 1 \\ 0 \end{bmatrix}$.

#### 解答
(35) 矩陣乘向量就是行的線性組合,權重是向量的分量,所以 **$c_1 = -4$、$c_2 = -1$、$c_3 = 3$**(書後解答相同)。

(36) 由 $3\mathbf{u} - 5\mathbf{v} - \mathbf{w} = \mathbf{0}$ 得 $\mathbf{w} = 3\mathbf{u} - 5\mathbf{v}$。矩陣的兩行正是 $\mathbf{u}$、$\mathbf{v}$,右邊是 $\mathbf{w}$,所以 **$x_1 = 3$、$x_2 = -5$**。

### 變化 · Lay 1.4 Exercises 37–38
(37) Let $\mathbf{q}_1, \mathbf{q}_2, \mathbf{q}_3$, and $\mathbf{v}$ represent vectors in $\mathbb{R}^5$, and let $x_1, x_2$, and $x_3$ denote scalars. Write the following vector equation as a matrix equation. Identify any symbols you choose to use: $x_1\mathbf{q}_1 + x_2\mathbf{q}_2 + x_3\mathbf{q}_3 = \mathbf{v}$.

(38) Rewrite the (numerical) matrix equation below in symbolic form as a vector equation, using symbols $\mathbf{v}_1, \mathbf{v}_2, \dots$ for the vectors and $c_1, c_2, \dots$ for scalars. Define what each symbol represents, using the data given in the matrix equation.

$$\begin{bmatrix} -3 & 5 & -4 & 9 & 7 \\ 5 & 8 & 1 & -2 & -4 \end{bmatrix}\begin{bmatrix} -3 \\ 2 \\ 4 \\ -1 \\ 2 \end{bmatrix} = \begin{bmatrix} 8 \\ -1 \end{bmatrix}$$

#### 解答
(37) $Q\mathbf{x} = \mathbf{v}$,其中 $Q = [\,\mathbf{q}_1 \;\; \mathbf{q}_2 \;\; \mathbf{q}_3\,]$($5 \times 3$ 矩陣)、$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}$(書後解答相同;若寫成 $A\mathbf{x} = \mathbf{b}$ 要交代 $A$、$\mathbf{b}$ 是什麼)。

(38) $c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + c_3\mathbf{v}_3 + c_4\mathbf{v}_4 + c_5\mathbf{v}_5 = \mathbf{b}$,其中 $\mathbf{v}_1 = \begin{bmatrix} -3 \\ 5 \end{bmatrix}$、$\mathbf{v}_2 = \begin{bmatrix} 5 \\ 8 \end{bmatrix}$、$\mathbf{v}_3 = \begin{bmatrix} -4 \\ 1 \end{bmatrix}$、$\mathbf{v}_4 = \begin{bmatrix} 9 \\ -2 \end{bmatrix}$、$\mathbf{v}_5 = \begin{bmatrix} 7 \\ -4 \end{bmatrix}$,$c_1 = -3$、$c_2 = 2$、$c_3 = 4$、$c_4 = -1$、$c_5 = 2$,$\mathbf{b} = \begin{bmatrix} 8 \\ -1 \end{bmatrix}$。

## 驗算
```check
Matrix([[1, 2, -1], [0, -5, 3]]) * Matrix([4, 3, 7]) == Matrix([3, 6])
Matrix([[2, -3], [8, 0], [-5, 2]]) * Matrix([4, 7]) == Matrix([-13, 32, -6])
Matrix([[2, 3, 4], [-1, 5, -3], [6, -2, 8]]) * Matrix([x1, x2, x3]) == Matrix([2*x1 + 3*x2 + 4*x3, -x1 + 5*x2 - 3*x3, 6*x1 - 2*x2 + 8*x3])
eye(3) * Matrix([s, t, h]) == Matrix([s, t, h])
Matrix([[6, 5], [-4, -3], [7, 6]]) * Matrix([1, -3]) == Matrix([-9, 5, -11])
Matrix([[8, 3, 1], [5, 1, 2]]) * Matrix([1, 1, 1]) == Matrix([12, 8])
Matrix([[7, 2, -9, 3], [-4, -5, 7, -2]]) * Matrix([6, -9, 1, -8]) == Matrix([-9, 44])
Matrix([[7, -3], [2, 1], [9, -6], [-3, 2]]) * Matrix([-2, -5]) == Matrix([1, -9, 12, -4])
Matrix([[1, 5, -2, 0], [-3, 1, 9, -5], [4, -8, -1, 7]]) * Matrix([3, -2, 0, -4]) == Matrix([-7, 9, 0])
Matrix([[1, 2, 4, -2], [0, 1, 5, 2], [-2, -4, -3, 9]]).rref()[0][:, 3] == Matrix([0, -3, 1])
Matrix([[1, 2, 1, 0], [-3, -1, 2, 1], [0, 5, 3, -1]]).rref()[0][:, 3] == Matrix([Rational(3, 5), Rational(-4, 5), 1])
Matrix([[3, -5, 0], [-2, 6, 4], [1, 1, 4]]).rref()[0][:2, 2] == Matrix([Rational(5, 2), Rational(3, 2)])
3 in Matrix([[5, 8, 7, 2], [0, 1, -1, -3], [1, 3, 0, 2]]).rref()[1]
3*Matrix([5, 0, 1]) - Matrix([8, 1, 3]) == Matrix([7, -1, 0])
Matrix([[3, -4, 2], [6, -3, 4], [-8, 9, -5]]) * Matrix([-4, -1, 3]) == Matrix([-2, -9, 8])
3*Matrix([7, 2, 5]) - 5*Matrix([3, 1, 3]) == Matrix([6, 1, 0])
Matrix([[-3, 5, -4, 9, 7], [5, 8, 1, -2, -4]]) * Matrix([-3, 2, 4, -1, 2]) == Matrix([8, -1])
```
