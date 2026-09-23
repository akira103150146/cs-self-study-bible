---
title_en: Matrix Notation, Sums, and Scalar Multiples
title_zh: 矩陣的記號、加法與純量乘法
sub: Same size, entry by entry
level: basic
source: Lay 2.1
lab_hook: '`A + B`、`2 * B`、`A.shape`:NumPy 的加法與純量乘法就是逐格做'
---
## 觀念
If $A$ is an $m \times n$ matrix—that is, a matrix with $m$ rows and $n$ columns—then the scalar entry in the $i$th row and $j$th column of $A$ is denoted by $a_{ij}$ and is called the $(i, j)$-entry of $A$. Each column of $A$ is a list of $m$ real numbers, which identifies a vector in $\mathbb{R}^m$. Often, these columns are denoted by $\mathbf{a}_1, \dots, \mathbf{a}_n$, and the matrix $A$ is written as

$$A = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \cdots \;\; \mathbf{a}_n\,]$$

The **diagonal entries** in an $m \times n$ matrix $A = [\,a_{ij}\,]$ are $a_{11}, a_{22}, a_{33}, \dots$, and they form the **main diagonal** of $A$. A **diagonal matrix** is a square $n \times n$ matrix whose nondiagonal entries are zero. An example is the $n \times n$ identity matrix, $I_n$. An $m \times n$ matrix whose entries are all zero is a **zero matrix** and is written as 0.

We say that two matrices are **equal** if they have the same size (i.e., the same number of rows and the same number of columns) and if their corresponding columns are equal. If $A$ and $B$ are $m \times n$ matrices, then the **sum** $A + B$ is the $m \times n$ matrix whose columns are the sums of the corresponding columns in $A$ and $B$. The sum $A + B$ is defined only when $A$ and $B$ are the same size.

If $r$ is a scalar and $A$ is a matrix, then the **scalar multiple** $rA$ is the matrix whose columns are $r$ times the corresponding columns in $A$.

**Theorem 1.** Let $A$, $B$, and $C$ be matrices of the same size, and let $r$ and $s$ be scalars.

- **a.** $A + B = B + A$
- **b.** $(A + B) + C = A + (B + C)$
- **c.** $A + 0 = A$
- **d.** $r(A + B) = rA + rB$
- **e.** $(r + s)A = rA + sA$
- **f.** $r(sA) = (rs)A$

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| $m \times n$ matrix | $m \times n$ 矩陣 | $m$ 列 $n$ 行;**列在前、行在後**,永遠這個順序 |
| $(i, j)$-entry | 第 $(i, j)$ 格 | 第 $i$ 列、第 $j$ 行那個數,寫成 $a_{ij}$ |
| diagonal entries | 對角元素 | $a_{11}, a_{22}, \dots$,左上到右下那一條 |
| main diagonal | 主對角線 | 對角元素連成的那條線 |
| diagonal matrix | 對角矩陣 | 只有主對角線可以不是 0 的方陣 |
| identity matrix $I_n$ | 單位矩陣 | 對角線全是 1 的對角矩陣,乘法裡的「1」 |
| zero matrix | 零矩陣 | 每一格都是 0,加法裡的「0」 |
| scalar multiple | 純量倍數 | 一個數乘整個矩陣,每格都乘 |

## 白話說
**矩陣就是一張數字表格。** 這一節只有兩件事:怎麼稱呼表格裡的位置,以及「同樣大小的兩張表可以逐格相加」。

- $a_{ij}$ 的兩個下標**先列後行**。$a_{32}$ 是第 3 列第 2 行那一格。整本書都用這個順序,包括 NumPy 的 `A[2, 1]`(注意 Python 從 0 開始數)。
- 加法要求**大小完全一樣**:$2 \times 3$ 只能加 $2 \times 3$。大小不同就是「沒有定義」,不是算出 0,而是這個算式根本不成立。
- 純量乘法就是每一格都乘上同一個數。$-A$ 是 $(-1)A$,$A - B$ 是 $A + (-1)B$。

Theorem 1 的六條看起來很囉嗦,但它說的事很單純:**加法與純量乘法,和你熟悉的數字運算規則一模一樣**,所以可以放心移項、合併、提出公因數。真正和數字不同的地方在下一個觀念(乘法)。

## 幾何意義
把矩陣看成「一排行向量」,加法就是**每一行各自做向量加法**(第 2 週學過的平行四邊形)。所以矩陣加法沒有新東西——它只是好幾個向量加法同時做。

這也是課本定義矩陣加法的方式:「$A + B$ 的每一行,就是 $A$、$B$ 對應行的和」。

## 在資工哪裡用
- **影像就是矩陣**:一張灰階圖是 $m \times n$ 的亮度表。兩張圖相加是疊圖,乘 $0.5$ 是調暗一半——就是這裡的加法與純量乘法。
- **NumPy 的 shape**:`A.shape` 回傳 `(m, n)`,順序和課本一致。寫程式時 90% 的錯誤訊息都在抱怨 shape 對不上。
- **批次資料表**:機器學習裡一批 32 筆、每筆 784 維的資料就是 $32 \times 784$ 的矩陣;把兩批資料的平均相減,做的就是矩陣減法。
- **稀疏矩陣**:社群網路的關聯表大多是 0,實務上不會真的存整張表(`scipy.sparse`),但加法與純量乘法的規則不變。

## 數值筆記
電腦裡的矩陣加法是**逐格獨立**的運算,可以完全平行化——GPU 之所以快,就是因為這種「每一格互不相干」的運算可以幾千格同時做。下一個觀念的乘法就不是這樣了,它每一格都要一整列乘一整行。

## 原理
**Theorem 1 為什麼成立?**(課本 p. 124)每一條都用同一招證明:先確認兩邊大小一樣,再確認**對應的行相等**。

以 (b) 為例:設 $A$、$B$、$C$ 的第 $j$ 行分別是 $\mathbf{a}_j$、$\mathbf{b}_j$、$\mathbf{c}_j$。那麼 $(A + B) + C$ 的第 $j$ 行是 $(\mathbf{a}_j + \mathbf{b}_j) + \mathbf{c}_j$,而 $A + (B + C)$ 的第 $j$ 行是 $\mathbf{a}_j + (\mathbf{b}_j + \mathbf{c}_j)$。這兩個向量相等(第 2 週向量加法的結合律),對每個 $j$ 都成立,所以兩個矩陣相等。

因為有結合律,可以直接寫 $A + B + C$ 不加括號;四個以上的和也一樣。

## 老師講解
### 例 1 · Lay 2.1 Example 1
Let

$$A = \begin{bmatrix} 4 & 0 & 5 \\ -1 & 3 & 2 \end{bmatrix}, \quad B = \begin{bmatrix} 1 & 1 & 1 \\ 3 & 5 & 7 \end{bmatrix}, \quad C = \begin{bmatrix} 2 & -3 \\ 0 & 1 \end{bmatrix}$$

Find $A + B$ and $A + C$.

1. **先看大小**。$A$ 是 $2 \times 3$、$B$ 是 $2 \times 3$——一樣大,可以加。$C$ 是 $2 \times 2$,和 $A$ 不一樣大。
2. **逐格相加**:$4 + 1 = 5$、$0 + 1 = 1$、$5 + 1 = 6$(第一列);$-1 + 3 = 2$、$3 + 5 = 8$、$2 + 7 = 9$(第二列)。
   $$A + B = \begin{bmatrix} 5 & 1 & 6 \\ 2 & 8 & 9 \end{bmatrix}$$
3. **$A + C$ 沒有定義**。不是等於 0、也不是「把 $C$ 補一行 0」——這個算式在矩陣代數裡根本不成立,寫出來就是錯的。
4. **檢查**:答案的大小一定和加數相同,還是 $2 \times 3$。

### 例 2 · Lay 2.1 Example 2
If $A$ and $B$ are the matrices in Example 1, find $2B$ and $A - 2B$.

1. **純量乘法:每一格乘 2**。
   $$2B = 2\begin{bmatrix} 1 & 1 & 1 \\ 3 & 5 & 7 \end{bmatrix} = \begin{bmatrix} 2 & 2 & 2 \\ 6 & 10 & 14 \end{bmatrix}$$
2. **減法就是加上負的**:$A - 2B = A + (-1)2B$,但不必真的這樣拆——直接逐格相減比較快。
   $$A - 2B = \begin{bmatrix} 4 & 0 & 5 \\ -1 & 3 & 2 \end{bmatrix} - \begin{bmatrix} 2 & 2 & 2 \\ 6 & 10 & 14 \end{bmatrix} = \begin{bmatrix} 2 & -2 & 3 \\ -7 & -7 & -12 \end{bmatrix}$$
3. **為什麼可以直接減?** 因為 Theorem 1 保證矩陣的加法與純量乘法遵守一般代數規則(課本在例 2 後面特別說明了這件事)。
4. **注意符號**:$-1 + (-2)\cdot 3 = -7$,負號最容易在這裡掉。逐格寫出算式,不要心算。

#### 備註
例 1 的 $A + C$ 一定要講。學生最常犯的錯就是「大小不合硬加」,尤其在 NumPy 裡 `A + C` 有時候不會報錯(broadcasting 會自作主張補齊),算出一個數學上沒有意義的東西。實作課的第一個陷阱就是這個。

## 易錯點
- **下標順序記反**:$a_{ij}$ 是「第 $i$ **列**、第 $j$ **行**」。看到 $a_{23}$ 要唸「第二列第三行」。
- **大小不同硬加**。加法只在同大小時有定義(Exercises 1–2 就是在練這件事)。
- **把 $rA$ 算成「只有第一行乘 $r$」**。是**每一格**都乘。
- **對角矩陣 ≠ 單位矩陣**:對角線可以是任何數,全都是 1 才是 $I_n$。
- NumPy 的索引從 0 開始:課本的 $a_{32}$ 是 `A[2, 1]`。抄答案時很容易差一格。

## 教學提示
這個觀念是全章最簡單的,不要花太多時間——10 分鐘講完、5 分鐘做練習就夠,把時間留給下一個觀念的乘法。

但有兩件事一定要在黑板上寫清楚並要求學生跟著唸一次:「**列在前、行在後**」、「**加法要同大小**」。後面整章(尤其乘法的 $m \times n$ 與 $n \times p$)都建立在這兩句話上。

課堂建議做:Exercises 3、4(和 $I_n$ 有關的加減與純量倍),當場對答案。Exercises 1、2 有加法也有乘法,等觀念 2 講完再一起做。

T 題 Exercises 43、44 是「怎麼用程式一次產生零矩陣、單位矩陣、對角矩陣、隨機矩陣」,不必在理論課做,直接留到實作課的暖身。

## 練習
### 照做 · Lay 2.1 Exercises 3–4
(3) Let $A = \begin{bmatrix} 4 & -1 \\ 5 & -2 \end{bmatrix}$. Compute $3I_2 - A$ and $(3I_2)A$.

(4) Compute $A - 5I_3$ and $(5I_3)A$, when

$$A = \begin{bmatrix} 9 & -1 & 3 \\ -8 & 7 & -3 \\ -4 & 1 & 8 \end{bmatrix}$$

#### 解答
(3) $3I_2 = \begin{bmatrix} 3 & 0 \\ 0 & 3 \end{bmatrix}$,所以
$$3I_2 - A = \begin{bmatrix} -1 & 1 \\ -5 & 5 \end{bmatrix}, \qquad (3I_2)A = 3A = \begin{bmatrix} 12 & -3 \\ 15 & -6 \end{bmatrix}$$

(4) $5I_3$ 只改對角線:
$$A - 5I_3 = \begin{bmatrix} 4 & -1 & 3 \\ -8 & 2 & -3 \\ -4 & 1 & 3 \end{bmatrix}, \qquad (5I_3)A = 5A = \begin{bmatrix} 45 & -5 & 15 \\ -40 & 35 & -15 \\ -20 & 5 & 40 \end{bmatrix}$$

#### 備註
這兩題讓學生第一次看到 $I_n$ 在矩陣代數裡扮演「1」的角色:乘上 $cI_n$ 等於整個矩陣乘 $c$。觀念 2 會再用到這件事。

建議課堂做 (3),(4) 留作業。

### 應用 · Lay 2.1 Exercises 43–44(T 電腦題)
(43) Use a web search engine such as Google to find documentation for your matrix program, and write the commands that will produce the following matrices (without keying in each entry of the matrix).

- **a.** A $5 \times 6$ matrix of zeros
- **b.** A $3 \times 5$ matrix of ones
- **c.** The $6 \times 6$ identity matrix
- **d.** A $5 \times 5$ diagonal matrix, with diagonal entries $3, 5, 7, 2, 4$

(44) Write the command(s) that will create a $6 \times 4$ matrix with random entries. In what range of numbers do the entries lie? Tell how to create a $3 \times 3$ matrix with random integer entries between $-9$ and $9$. [*Hint:* If $x$ is a random number such that $0 < x < 1$, then $-9.5 < 19(x - .5) < 9.5$.]

#### 解答
(43) 答案依軟體而定。本課用 Python:

- NumPy:`np.zeros((5, 6))`、`np.ones((3, 5))`、`np.eye(6)`、`np.diag([3, 5, 7, 2, 4])`
- SymPy:`zeros(5, 6)`、`ones(3, 5)`、`eye(6)`、`diag(3, 5, 7, 2, 4)`

(44) `np.random.rand(6, 4)`,元素落在開區間 $(0, 1)$、均勻分布。

要產生 $-9$ 到 $9$ 的隨機整數:`np.round(19 * (np.random.rand(3, 3) - 0.5)).astype(int)`。理由就是題目的提示:$0 < x < 1$ 時 $-9.5 < 19(x - .5) < 9.5$,四捨五入後恰好落在 $-9, -8, \dots, 9$。

#### 備註
書上寫的是 MATLAB 的 `zeros`、`ones`、`eye`、`diag`、`rand`,本課改用 Python;函式名稱幾乎一樣,可以順便說明這些名字是跨語言的慣例。

這兩題**直接放進實作課**當暖身,理論課不必做。第 44 題的隨機矩陣在實作課還有一個用途:用隨機矩陣測試一個恆等式到底成不成立(Exercises 45–46)。

## 驗算
```check
Matrix([[4, 0, 5], [-1, 3, 2]]) + Matrix([[1, 1, 1], [3, 5, 7]]) == Matrix([[5, 1, 6], [2, 8, 9]])
Matrix([[4, 0, 5], [-1, 3, 2]]) - 2 * Matrix([[1, 1, 1], [3, 5, 7]]) == Matrix([[2, -2, 3], [-7, -7, -12]])
2 * Matrix([[1, 1, 1], [3, 5, 7]]) == Matrix([[2, 2, 2], [6, 10, 14]])
3 * eye(2) - Matrix([[4, -1], [5, -2]]) == Matrix([[-1, 1], [-5, 5]])
(3 * eye(2)) * Matrix([[4, -1], [5, -2]]) == Matrix([[12, -3], [15, -6]])
Matrix([[9, -1, 3], [-8, 7, -3], [-4, 1, 8]]) - 5 * eye(3) == Matrix([[4, -1, 3], [-8, 2, -3], [-4, 1, 3]])
(5 * eye(3)) * Matrix([[9, -1, 3], [-8, 7, -3], [-4, 1, 8]]) == Matrix([[45, -5, 15], [-40, 35, -15], [-20, 5, 40]])
zeros(5, 6).shape == (5, 6) and eye(6).shape == (6, 6) and diag(3, 5, 7, 2, 4).shape == (5, 5)
{round(19 * (Rational(u, 1000) - Rational(1, 2))) for u in range(1, 1000)} == set(range(-9, 10))
```

