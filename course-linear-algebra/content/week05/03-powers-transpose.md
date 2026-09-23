---
title_en: Powers and the Transpose of a Matrix
title_zh: 冪次與轉置:$A^k$ 和 $A^T$
sub: Transposing a product reverses the order
level: mid
source: Lay 2.1
lab_hook: '`A @ A @ A` 或 `np.linalg.matrix_power(A, 3)`;轉置是 `A.T`'
---
## 觀念
**Powers of a matrix.** If $A$ is an $n \times n$ matrix and if $k$ is a positive integer, then $A^k$ denotes the product of $k$ copies of $A$:

$$A^k = \underbrace{A \cdots A}_{k}$$

If $A$ is nonzero and if $\mathbf{x}$ is in $\mathbb{R}^n$, then $A^k\mathbf{x}$ is the result of left-multiplying $\mathbf{x}$ by $A$ repeatedly $k$ times. If $k = 0$, then $A^0\mathbf{x}$ should be $\mathbf{x}$ itself. Thus $A^0$ is interpreted as the identity matrix.

**The transpose of a matrix.** Given an $m \times n$ matrix $A$, the **transpose** of $A$ is the $n \times m$ matrix, denoted by $A^T$, whose columns are formed from the corresponding rows of $A$.

**Theorem 3.** Let $A$ and $B$ denote matrices whose sizes are appropriate for the following sums and products.

- **a.** $(A^T)^T = A$
- **b.** $(A + B)^T = A^T + B^T$
- **c.** For any scalar $r$, $(rA)^T = rA^T$
- **d.** $(AB)^T = B^TA^T$

The transpose of a product of matrices equals the product of their transposes in the *reverse* order.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| power $A^k$ | 冪次 | $k$ 個 $A$ 連乘;只有方陣才有 |
| transpose $A^T$ | 轉置 | 列變成行、行變成列;$m \times n$ 變 $n \times m$ |
| reverse order | 反序 | $(AB)^T = B^TA^T$,順序要倒過來 |
| scalar product / inner product | 內積 | $\mathbf{u}^T\mathbf{v}$,$1 \times 1$,就是一個數 |
| outer product | 外積 | $\mathbf{u}\mathbf{v}^T$,$n \times n$ 矩陣 |
| nilpotent | 冪零 | 某次方之後變成零矩陣(Exercise 47 的 $S$) |

## 白話說
**冪次**:$A^k$ 就是「同一台機器連做 $k$ 次」。只有**方陣**能取冪次,因為輸出要能再餵回輸入(輸入輸出維度得一樣)。

$A^0 = I$ 的理由很直接:做 0 次等於什麼都沒做,而「什麼都沒做」那台機器就是 $I$。

**轉置**:把矩陣沿主對角線翻過來,第 $i$ 列變成第 $i$ 行。$2 \times 3$ 轉置後是 $3 \times 2$。

**最容易記錯的一條**:
$$(AB)^T = B^TA^T \quad(\text{不是 } A^TB^T)$$
順序要**倒過來**。理由用尺寸就能看出來:$A$ 是 $m \times n$、$B$ 是 $n \times p$,轉置後 $A^T$ 是 $n \times m$、$B^T$ 是 $p \times n$。要相乘,只有 $B^TA^T$($p \times n$ 乘 $n \times m$)接得起來;$A^TB^T$ 的中間是 $m$ 和 $p$,一般根本沒有定義。

**向量也是矩陣**:$\mathbb{R}^n$ 的向量就是 $n \times 1$ 矩陣,所以轉置的規則對向量一樣適用。於是有兩個常見組合:

| 寫法 | 大小 | 結果 |
|---|---|---|
| $\mathbf{u}^T\mathbf{v}$(內積) | $1 \times n$ 乘 $n \times 1$ | 一個數 |
| $\mathbf{u}\mathbf{v}^T$(外積) | $n \times 1$ 乘 $1 \times n$ | $n \times n$ 矩陣 |

兩個寫法只差一個轉置的位置,結果卻天差地遠。這一組在第 13 週(內積與正交)和第 16 週(SVD 的秩一展開)會是主角。

## 在資工哪裡用
- **$A^k$ 看長期行為**:遷移矩陣、Markov 鏈、PageRank 都在算 $A^k\mathbf{x}$ 會收斂到哪裡(第 11、12 週)。Exercise 48 就是一個會收斂到均勻分布的例子。
- **圖的 $k$ 步路徑數**:鄰接矩陣的 $k$ 次方,第 $(i,j)$ 格就是「從 $i$ 走 $k$ 步到 $j$ 的走法數」(見本週補充觀念)。
- **轉置在程式裡無所不在**:`X.T @ X`(共變異數矩陣、最小平方的正規方程)、`A.T` 換資料排列方向。深度學習框架裡反向傳播的梯度就是 $W^T\delta$——前向乘 $W$、反向乘 $W^T$。
- **$\mathbf{x}^TM\mathbf{x}$(二次型)**:一個數,用來衡量「這個向量有多符合某個模式」。Exercises 49–50 用它判斷色塊圖樣,第 15 週會正式學。
- **記憶體佈局**:NumPy 的 `A.T` 不搬資料,只改讀取方式(view)。所以轉置本身極快,但之後的存取可能變慢——這是第 2 週計時實驗看過的 row-major / column-major 問題。

## 數值筆記
`A.T` 在 NumPy 裡是**視圖(view)**,不複製資料;要真的複製得寫 `A.T.copy()`。這有個實務後果:對轉置後的矩陣做大量逐列運算,快取命中率會變差,速度可能掉幾倍(第 2 週量過)。

另外,算 $A^k\mathbf{x}$ 時**不要先算 $A^k$**。先算 $A\mathbf{x}$、再反覆左乘 $A$,成本是 $O(kn^2)$;先算 $A^k$ 再乘向量是 $O(kn^3)$。Practice Problem 2 就在算這筆帳。

## 原理
**Theorem 3(d) 的證明**(Exercise 41):設 $A$ 是 $m \times n$、$B$ 是 $n \times p$。

$(AB)^T$ 的 $(i, j)$ 格 = $AB$ 的 $(j, i)$ 格 = $\displaystyle\sum_{k=1}^{n} a_{jk}b_{ki}$。

$B^TA^T$ 的 $(i, j)$ 格 = ($B^T$ 的第 $i$ 列)·($A^T$ 的第 $j$ 行) = $\displaystyle\sum_{k=1}^{n} b_{ki}a_{jk}$。

兩式的每一項都是同樣兩個數相乘(實數乘法可交換),所以相等。逐格相等 ⇒ 兩矩陣相等。∎

**為什麼順序會倒過來?** 因為 $B^T$ 的第 $i$ **列**來自 $B$ 的第 $i$ **行**,$A^T$ 的第 $j$ **行**來自 $A$ 的第 $j$ **列**。轉置把「列」和「行」對調,自然也把左右對調。

**推廣**:$(ABC)^T = C^TB^TA^T$,任意多個都一樣,順序完全顛倒(Exercise 42)。

**$\mathbf{u}^T\mathbf{v} = \mathbf{v}^T\mathbf{u}$ 為什麼成立**(Exercise 36):$\mathbf{u}^T\mathbf{v}$ 是 $1 \times 1$ 矩陣,而 $1 \times 1$ 矩陣等於自己的轉置,所以
$$\mathbf{u}^T\mathbf{v} = (\mathbf{u}^T\mathbf{v})^T = \mathbf{v}^T(\mathbf{u}^T)^T = \mathbf{v}^T\mathbf{u}.$$

## 老師講解
### 例 1 · Lay 2.1 Example 8
Let

$$A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \quad B = \begin{bmatrix} -5 & 2 \\ 1 & -3 \\ 0 & 4 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 1 & 1 & 1 \\ -3 & 5 & -2 & 7 \end{bmatrix}$$

Find $A^T$, $B^T$, and $C^T$.

1. **做法只有一句話**:第 1 列抄成第 1 行、第 2 列抄成第 2 行,依此類推。
2. $A$ 是 $2 \times 2$,轉置後還是 $2 \times 2$,但 $b$ 和 $c$ 交換位置:
   $$A^T = \begin{bmatrix} a & c \\ b & d \end{bmatrix}$$
3. $B$ 是 $3 \times 2$,轉置後變 $2 \times 3$:
   $$B^T = \begin{bmatrix} -5 & 1 & 0 \\ 2 & -3 & 4 \end{bmatrix}$$
4. $C$ 是 $2 \times 4$,轉置後變 $4 \times 2$:
   $$C^T = \begin{bmatrix} 1 & -3 \\ 1 & 5 \\ 1 & -2 \\ 1 & 7 \end{bmatrix}$$
5. **檢查**:主對角線上的元素($a$、$d$)位置不動,這是轉置的固定特徵。大小則一定是「列行互換」。

### 例 2 · Lay 2.1 Practice Problem 1
Since vectors in $\mathbb{R}^n$ may be regarded as $n \times 1$ matrices, the properties of transposes in Theorem 3 apply to vectors, too. Let

$$A = \begin{bmatrix} 1 & -3 \\ -2 & 4 \end{bmatrix} \quad\text{and}\quad \mathbf{x} = \begin{bmatrix} 5 \\ 3 \end{bmatrix}$$

Compute $(A\mathbf{x})^T$, $\mathbf{x}^TA^T$, $\mathbf{x}\mathbf{x}^T$, and $\mathbf{x}^T\mathbf{x}$. Is $A^T\mathbf{x}^T$ defined?

1. **先算 $A\mathbf{x}$**:$\begin{bmatrix} 1(5) + (-3)(3) \\ -2(5) + 4(3) \end{bmatrix} = \begin{bmatrix} -4 \\ 2 \end{bmatrix}$,所以 $(A\mathbf{x})^T = [\,-4 \;\; 2\,]$(一個 $1 \times 2$ 的列向量)。
2. **另一條路**:$\mathbf{x}^TA^T = [\,5 \;\; 3\,]\begin{bmatrix} 1 & -2 \\ -3 & 4 \end{bmatrix} = [\,-4 \;\; 2\,]$。
3. **兩個答案一樣,不是巧合**:這正是 Theorem 3(d) 的 $(A\mathbf{x})^T = \mathbf{x}^TA^T$(把向量當成矩陣用)。
4. **外積**:$\mathbf{x}\mathbf{x}^T = \begin{bmatrix} 5 \\ 3 \end{bmatrix}[\,5 \;\; 3\,] = \begin{bmatrix} 25 & 15 \\ 15 & 9 \end{bmatrix}$——$2 \times 1$ 乘 $1 \times 2$,得到 $2 \times 2$。
5. **內積**:$\mathbf{x}^T\mathbf{x} = [\,5 \;\; 3\,]\begin{bmatrix} 5 \\ 3 \end{bmatrix} = 25 + 9 = 34$——$1 \times 2$ 乘 $2 \times 1$,得到 $1 \times 1$,習慣上直接寫成數字 34。
6. **$A^T\mathbf{x}^T$ 沒有定義**:$A^T$ 是 $2 \times 2$、$\mathbf{x}^T$ 是 $1 \times 2$,中間是 2 和 1,對不上。
7. **這題的教訓**:同樣兩個東西,轉置擺左邊或右邊,可能得到一個數、一個矩陣,或什麼都得不到。**寫下尺寸再動手**。

### 例 3 · Lay 2.1 Example 9(本週的資工例子)
In order to feed a $2 \times 2$ colored block into the computer, it first gets converted into a $4 \times 1$ vector by assigning a 1 to each block that is blue and a 0 to each block that is white. Then, the computer converts the block of numbers into a vector by placing the numbers in each column below the numbers in the column to its left. Let

$$M = \begin{bmatrix} 1 & 0 & 0 & -1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ -1 & 0 & 0 & 1 \end{bmatrix}$$

Show how $\mathbf{x}^TM\mathbf{x}$ tells whether or not a $2 \times 2$ block matches the chosen checkerboard pattern.

1. **先看編碼**。$2 \times 2$ 的色塊(藍 = 1、白 = 0)按**行**串成 $4 \times 1$ 向量:$\mathbf{x} = (x_1, x_2, x_3, x_4)$ 對應方格 $\begin{bmatrix} x_1 & x_3 \\ x_2 & x_4 \end{bmatrix}$。
2. **算 $\mathbf{x}^TM\mathbf{x}$ 是什麼形狀**:$1 \times 4$ 乘 $4 \times 4$ 乘 $4 \times 1$ = $1 \times 1$,**一個數**。這種「向量 · 矩陣 · 同一個向量」的寫法叫二次型,第 15 週會正式學。
3. **試棋盤格**:$\mathbf{v} = (1, 0, 0, 1)$(左上、右下是藍)。$M\mathbf{v} = \mathbf{0}$,所以 $\mathbf{v}^TM\mathbf{v} = 0$。
4. **試全白**:$\mathbf{w} = (0,0,0,0)$,當然也得到 $\mathbf{w}^TM\mathbf{w} = 0$。
5. **所以還要第二個條件**:$\mathbf{x}^T\mathbf{x}$ 是各分量平方和,只有在 $\mathbf{x} = \mathbf{0}$ 時才是 0。要判定是棋盤格,必須 $\mathbf{x}^TM\mathbf{x} = 0$ **且** $\mathbf{x}^T\mathbf{x} \ne 0$。
6. **試一個不合的圖樣**:$\mathbf{x} = (1, 1, 0, 1)$,算出 $\mathbf{x}^TM\mathbf{x} = 1 \ne 0$,所以不是棋盤格。
7. **這就是 AI 辨識的雛形**:把圖樣編碼成向量,用一個矩陣算出一個數,看那個數是不是 0。真正的影像辨識做的事情更複雜,但骨架是一樣的——**矩陣乘法 + 一個判準**。

#### 備註
例 3 是課本 2.1 少見的資工例子,值得講。若時間不夠,可以只講到第 5 步(兩個條件),第 6 步留給練習(Exercises 49–50)。

## 易錯點
- **$(AB)^T$ 寫成 $A^TB^T$**。這是本節第一名的錯誤。用尺寸檢查:$A^TB^T$ 通常根本沒有定義。
- **$A^k$ 用在非方陣上**。$3 \times 2$ 的矩陣沒有 $A^2$。
- **把 $\mathbf{u}^T\mathbf{v}$ 和 $\mathbf{u}\mathbf{v}^T$ 搞混**:一個是數、一個是矩陣。寫下尺寸最保險。
- **以為 $(A + B)^T = B^T + A^T$ 是「反序」的例子**。加法沒有順序問題,反序只發生在乘法。
- 算 $A^k\mathbf{x}$ 時先把 $A^k$ 乘出來,浪費大量計算(Practice Problem 2)。

## 教學提示
轉置本身 3 分鐘就能講完,重點全在 **Theorem 3(d) 的反序**。建議用尺寸論證帶過一次(比背公式有效):「$A^TB^T$ 接得起來嗎?接不起來,所以只能是 $B^TA^T$。」

$\mathbf{u}^T\mathbf{v}$ 與 $\mathbf{u}\mathbf{v}^T$ 這一組一定要講,並在黑板上寫下兩者的大小。第 13 週(cosine similarity)與第 16 週(SVD)都會回來用。

課堂建議做:Practice Problem 1(整題,含「$A^T\mathbf{x}^T$ 有沒有定義」);是非題 Exercises 22、23(反序);Exercise 35(符號版的內積與外積)。Exercises 47、48 是 T 題,放進實作課看 $A^k$ 的長期行為。

Exercises 31–34 比較抽象($CA = I$ 推出什麼),數理弱的班級可以只講 Exercise 31,其餘標為選做。

## 練習
### 照做 · Lay 2.1 Exercises 35–36
In Exercises 35 and 36, view vectors in $\mathbb{R}^n$ as $n \times 1$ matrices. For $\mathbf{u}$ and $\mathbf{v}$ in $\mathbb{R}^n$, the matrix product $\mathbf{u}^T\mathbf{v}$ is a $1 \times 1$ matrix, called the **scalar product**, or **inner product**, of $\mathbf{u}$ and $\mathbf{v}$. It is usually written as a single real number without brackets. The matrix product $\mathbf{u}\mathbf{v}^T$ is an $n \times n$ matrix, called the **outer product** of $\mathbf{u}$ and $\mathbf{v}$. The products $\mathbf{u}^T\mathbf{v}$ and $\mathbf{u}\mathbf{v}^T$ will appear later in the text.

(35) Let $\mathbf{u} = \begin{bmatrix} -2 \\ 3 \\ -4 \end{bmatrix}$ and $\mathbf{v} = \begin{bmatrix} a \\ b \\ c \end{bmatrix}$. Compute $\mathbf{u}^T\mathbf{v}$, $\mathbf{v}^T\mathbf{u}$, $\mathbf{u}\mathbf{v}^T$, and $\mathbf{v}\mathbf{u}^T$.

(36) If $\mathbf{u}$ and $\mathbf{v}$ are in $\mathbb{R}^n$, how are $\mathbf{u}^T\mathbf{v}$ and $\mathbf{v}^T\mathbf{u}$ related? How are $\mathbf{u}\mathbf{v}^T$ and $\mathbf{v}\mathbf{u}^T$ related?

#### 解答
(35)
$$\mathbf{u}^T\mathbf{v} = \mathbf{v}^T\mathbf{u} = -2a + 3b - 4c$$
$$\mathbf{u}\mathbf{v}^T = \begin{bmatrix} -2a & -2b & -2c \\ 3a & 3b & 3c \\ -4a & -4b & -4c \end{bmatrix}, \qquad \mathbf{v}\mathbf{u}^T = \begin{bmatrix} -2a & 3a & -4a \\ -2b & 3b & -4b \\ -2c & 3c & -4c \end{bmatrix}$$

(36) $\mathbf{u}^T\mathbf{v} = \mathbf{v}^T\mathbf{u}$(**相等**,因為 $1 \times 1$ 矩陣等於自己的轉置);$\mathbf{u}\mathbf{v}^T$ 與 $\mathbf{v}\mathbf{u}^T$ **互為轉置**($(\mathbf{u}\mathbf{v}^T)^T = \mathbf{v}\mathbf{u}^T$,Theorem 3(d))。

#### 備註
(35) 算完要讓學生**比對兩個外積**:它們長得很像,但一個是「每列同一個字母」、另一個是「每行同一個字母」——互為轉置。這比口頭說明有效。

### 是非 · Lay 2.1 Exercises 19–24
Exercises 15–24 concern arbitrary matrices $A$, $B$, and $C$ for which the indicated sums and products are defined. Mark each statement True or False (T/F). Justify each answer.

(19) **(T/F)** $AB + AC = A(B + C)$

(20) **(T/F)** $A^T + B^T = (A + B)^T$

(21) **(T/F)** $(AB)C = (AC)B$

(22) **(T/F)** $(AB)^T = A^TB^T$

(23) **(T/F)** The transpose of a product of matrices equals the product of their transposes in the same order.

(24) **(T/F)** The transpose of a sum of matrices equals the sum of their transposes.

#### 解答
- (19) **True.** 左分配律,Theorem 2(b)。
- (20) **True.** Theorem 3(b)。
- (21) **False.** 結合律只允許移動**括號**($(AB)C = A(BC)$),不允許調換 $B$、$C$ 的**順序**。反例:取 $A = I$、$B = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$、$C = \begin{bmatrix} 0 & 0 \\ 1 & 0 \end{bmatrix}$,則 $BC \ne CB$。
- (22) **False.** Theorem 3(d) 是 $(AB)^T = B^TA^T$,順序要反過來。
- (23) **False.** 應該是 **reverse order**(反序),見課本 p. 129 的方框。
- (24) **True.** Theorem 3(b);加法沒有順序問題。

#### 備註
書後解答對 Exercises 15–23 只寫「Answer the questions before looking in the *Study Guide*.」,沒有給 T/F;Exercise 24 是偶數題,書後也沒有。上面六題的答案是本講義判定的。

(21) 是最容易答錯的一題:學生把「結合律」誤讀成「可以任意搬動」。(22)(23) 是同一件事的符號版與文字版,放在一起做,印象最深。

### 變化 · Lay 2.1 Exercises 41–42
(41) Prove Theorem 3(d). [*Hint:* Consider the $j$th row of $(AB)^T$.]

(42) Give a formula for $(AB\mathbf{x})^T$, where $\mathbf{x}$ is a vector and $A$ and $B$ are matrices of appropriate sizes.

#### 解答
(41) 見上方「原理」的完整證明:兩邊的 $(i, j)$ 格都等於 $\sum_k a_{jk}b_{ki}$。

(42)
$$(AB\mathbf{x})^T = \mathbf{x}^TB^TA^T$$
做法是把 $AB\mathbf{x}$ 看成 $(AB)\mathbf{x}$,連用兩次 Theorem 3(d):$((AB)\mathbf{x})^T = \mathbf{x}^T(AB)^T = \mathbf{x}^TB^TA^T$。順序完全顛倒。

#### 備註
(42) 是很好的口頭練習:三個東西相乘,轉置後倒過來寫。可以順便問「$(ABCD)^T$ 呢?」

### 變化 · Lay 2.1 Exercises 47–48(T 電腦題)
(47) Let

$$S = \begin{bmatrix} 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$$

Compute $S^k$ for $k = 2, \dots, 6$.

(48) Describe in words what happens when you compute $A^5$, $A^{10}$, $A^{20}$, and $A^{30}$ for

$$A = \begin{bmatrix} 1/6 & 1/2 & 1/3 \\ 1/2 & 1/4 & 1/4 \\ 1/3 & 1/4 & 5/12 \end{bmatrix}$$

#### 解答
(47) $S$ 把向量 $(a, b, c, d, e)$ 往左推成 $(b, c, d, e, 0)$。每乘一次,那條 1 的對角線就往右上移一格:
$$S^2 = \begin{bmatrix} 0&0&1&0&0 \\ 0&0&0&1&0 \\ 0&0&0&0&1 \\ 0&0&0&0&0 \\ 0&0&0&0&0 \end{bmatrix}, \quad S^3 = \begin{bmatrix} 0&0&0&1&0 \\ 0&0&0&0&1 \\ 0&0&0&0&0 \\ 0&0&0&0&0 \\ 0&0&0&0&0 \end{bmatrix}, \quad S^4 = \begin{bmatrix} 0&0&0&0&1 \\ 0&0&0&0&0 \\ 0&0&0&0&0 \\ 0&0&0&0&0 \\ 0&0&0&0&0 \end{bmatrix}$$
推 5 次之後所有分量都被推出去了,所以 $S^5 = S^6 = O$(零矩陣)。這種矩陣叫**冪零矩陣**。

(48) 冪次越高,$A^k$ 越接近**每一格都是 $1/3$** 的矩陣:$A^{10}$ 已經每格都是 $.33333\ldots$,$A^{20}$、$A^{30}$ 在小數點後 8 位內看不出差別。

原因:$A$ 的每一列、每一行加起來都是 1(雙隨機矩陣),所以反覆相乘會把一切「抹平」成均勻分布。這是第 11、12 週(Markov 鏈的穩態向量)的預告。

#### 備註
這兩題標 T,放進實作課。(47) 的位移矩陣是資工的老朋友——它就是「把資料往左移一格」的運算,訊號處理和 FIFO 佇列都在做這件事。

(48) 最好在課堂上口頭預測一次再跑:先問「你覺得乘 30 次會發生什麼事?」大多數學生會猜「數字越來越大」或「越來越小」,實際上是**趨於一致**。

### 應用 · Lay 2.1 Exercises 49–50(T 電腦題)
(49) The matrix $M$ can detect a particular $2 \times 2$ colored pattern like in Example 9. Create a nonzero $4 \times 1$ vector $\mathbf{x}$ by choosing each entry to be a zero or one. Test to see if $\mathbf{x}$ corresponds to the right pattern by calculating $\mathbf{x}^TM\mathbf{x}$. If $\mathbf{x}^TM\mathbf{x} = 0$, then $\mathbf{x}$ is the pattern identified by $M$. If $\mathbf{x}^TM\mathbf{x} \ne 0$, try a different nonzero vector of zeros and ones. You may want to be systematic in the way that you choose each $\mathbf{x}$ in order to avoid testing the same vector twice. You are using "guess and check" to determine which pattern of $2 \times 2$ colored squares the matrix $M$ detects.

$$M = \begin{bmatrix} 1 & 0 & -1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

(50) Repeat Exercise 49 with the matrix

$$M = \begin{bmatrix} 1 & 0 & 0 & -1 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 0 \\ -1 & -1 & 0 & 2 \end{bmatrix}$$

#### 解答
(49) 答案是 $\mathbf{x} = (1, 0, 1, 0)$:此時 $M\mathbf{x} = \mathbf{0}$,所以 $\mathbf{x}^TM\mathbf{x} = 0$,而且 $\mathbf{x}^T\mathbf{x} = 2 \ne 0$。把 15 個非零的 0/1 向量都試過,只有這一個成立。

依 Example 9 的編碼($\mathbf{x} = (x_1,x_2,x_3,x_4)$ 對應方格 $\begin{bmatrix} x_1 & x_3 \\ x_2 & x_4 \end{bmatrix}$),這個向量代表**上排兩格藍、下排兩格白**。

(50) 答案是 $\mathbf{x} = (1, 1, 0, 1)$:$\mathbf{x}^TM\mathbf{x} = 0$ 且 $\mathbf{x}^T\mathbf{x} = 3 \ne 0$,同樣是 15 個候選裡唯一的一個。對應的圖樣是 $\begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}$:**左上、左下、右下三格藍,右上一格白**。

#### 備註
兩題都標 T,放進實作課用迴圈窮舉 15 個向量——這正好示範「用電腦把 15 種可能全試一遍」比用眼睛猜快。

書後 Exercise 49 的解答除了向量之外還附了一張 $2 \times 2$ 配色圖(上排藍、下排白),講義這裡改用文字描述。編碼慣例要回頭看課本 p. 130 的 Example 9 與 Figure 4。

### 挑戰 · Lay 2.1 Exercises 31–34
(31) Suppose $CA = I_n$ (the $n \times n$ identity matrix). Show that the equation $A\mathbf{x} = \mathbf{0}$ has only the trivial solution. Explain why $A$ cannot have more columns than rows.

(32) Suppose $AD = I_m$ (the $m \times m$ identity matrix). Show that for any $\mathbf{b}$ in $\mathbb{R}^m$, the equation $A\mathbf{x} = \mathbf{b}$ has a solution. [*Hint:* Think about the equation $AD\mathbf{b} = \mathbf{b}$.] Explain why $A$ cannot have more rows than columns.

(33) Suppose $A$ is an $m \times n$ matrix and there exist $n \times m$ matrices $C$ and $D$ such that $CA = I_n$ and $AD = I_m$. Prove that $m = n$ and $C = D$. [*Hint:* Think about the product $CAD$.]

(34) Suppose $A$ is a $3 \times n$ matrix whose columns span $\mathbb{R}^3$. Explain how to construct an $n \times 3$ matrix $D$ such that $AD = I_3$.

#### 解答
- (31) 設 $A\mathbf{x} = \mathbf{0}$。左乘 $C$:一方面 $C(A\mathbf{x}) = (CA)\mathbf{x} = I_n\mathbf{x} = \mathbf{x}$,另一方面 $C\mathbf{0} = \mathbf{0}$,所以 $\mathbf{x} = \mathbf{0}$,只有平凡解。沒有自由變數 ⇒ 每一行都是樞軸行 ⇒ 樞軸數 $= n$;又樞軸數 $\le$ 列數 $m$,故 $n \le m$。
- (32) 取 $\mathbf{x} = D\mathbf{b}$,則 $A\mathbf{x} = A(D\mathbf{b}) = (AD)\mathbf{b} = I_m\mathbf{b} = \mathbf{b}$,所以恆有解。對所有 $\mathbf{b}$ 都有解 ⇒ 每一列都有樞軸(第 2 週的 Theorem 4)⇒ 樞軸數 $= m \le$ 行數 $n$。
- (33) 由 (31) 得 $n \le m$,由 (32) 得 $m \le n$,所以 $m = n$。再看 $CAD$ 的兩種括法:
  $$C = CI_m = C(AD) = (CA)D = I_nD = D$$
- (34) 因為 $A$ 的行張成 $\mathbb{R}^3$,方程 $A\mathbf{x} = \mathbf{e}_i$ 對 $i = 1, 2, 3$ 都有解;各取一組解 $\mathbf{d}_i$,令 $D = [\,\mathbf{d}_1 \;\; \mathbf{d}_2 \;\; \mathbf{d}_3\,]$,則 $AD = [\,A\mathbf{d}_1 \;\; A\mathbf{d}_2 \;\; A\mathbf{d}_3\,] = [\,\mathbf{e}_1 \;\; \mathbf{e}_2 \;\; \mathbf{e}_3\,] = I_3$。

#### 備註
這四題是下一個觀念(反矩陣)的伏筆:(33) 說的是「若左反與右反都存在,矩陣必為方陣,而且兩者相同」——正是課本定義反矩陣時要求 $CA = I$ **且** $AC = I$ 的理由。

數理弱的班級建議只做 (31),把 (33) 留到觀念 4 講完再回頭看。

### 挑戰 · Lay 2.1 Exercise 46(T)與 Practice Problem 2
(46) Use at least three pairs of random $4 \times 4$ matrices $A$ and $B$ to test the equalities $(A + B)^T = A^T + B^T$ and $(AB)^T = A^TB^T$. (See Exercise 45.) Report your conclusions. [*Note:* Most matrix programs use $A'$ for $A^T$.]

(Practice Problem 2) Let $A$ be a $4 \times 4$ matrix and let $\mathbf{x}$ be a vector in $\mathbb{R}^4$. What is the fastest way to compute $A^2\mathbf{x}$? Count the multiplications.

#### 解答
(46) 第一條 $(A + B)^T = A^T + B^T$ **恆成立**(Theorem 3(b)),三組隨機矩陣的差都是零矩陣。

第二條 $(AB)^T = A^TB^T$ **一般不成立**,正確的是 $(AB)^T = B^TA^T$。隨機矩陣測試會得到非零的差。

(Practice Problem 2) 最快的做法是 $A(A\mathbf{x})$:$A\mathbf{x}$ 要 16 次乘法(每個分量 4 次),再乘一次 $A$ 又 16 次,**共 32 次**。

若先算 $A^2$ 要 64 次乘法($A^2$ 有 16 格、每格 4 次),再乘 $\mathbf{x}$ 又 16 次,**共 80 次**。

所以「先乘向量、再乘矩陣」快得多,而且矩陣越大差距越誇張($O(kn^2)$ vs $O(kn^3)$)。

#### 備註
Practice Problem 2 是全節最有實務價值的一題,實作課會實際計時。深度學習的推論之所以能跑在手機上,靠的就是「永遠讓矩陣去乘向量,不要先把矩陣乘起來」。

## 驗算
```check
Matrix([[-5, 2], [1, -3], [0, 4]]).T == Matrix([[-5, 1, 0], [2, -3, 4]])
Matrix([[1, 1, 1, 1], [-3, 5, -2, 7]]).T == Matrix([[1, -3], [1, 5], [1, -2], [1, 7]])
Matrix([[a, b], [c, d]]).T == Matrix([[a, c], [b, d]])
(Matrix([[1, -3], [-2, 4]]) * Matrix([5, 3])).T == Matrix([5, 3]).T * Matrix([[1, -3], [-2, 4]]).T == Matrix([[-4, 2]])
Matrix([5, 3]) * Matrix([5, 3]).T == Matrix([[25, 15], [15, 9]])
(Matrix([5, 3]).T * Matrix([5, 3]))[0] == 34
(Matrix([1, 0, 0, 1]).T * Matrix([[1, 0, 0, -1], [0, 1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 1]]) * Matrix([1, 0, 0, 1]))[0] == 0
(Matrix([1, 1, 0, 1]).T * Matrix([[1, 0, 0, -1], [0, 1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 1]]) * Matrix([1, 1, 0, 1]))[0] == 1
(Matrix([-2, 3, -4]).T * Matrix([a, b, c]))[0] == (Matrix([a, b, c]).T * Matrix([-2, 3, -4]))[0] == -2*a + 3*b - 4*c
Matrix([-2, 3, -4]) * Matrix([a, b, c]).T == Matrix([[-2*a, -2*b, -2*c], [3*a, 3*b, 3*c], [-4*a, -4*b, -4*c]])
Matrix([a, b, c]) * Matrix([-2, 3, -4]).T == (Matrix([-2, 3, -4]) * Matrix([a, b, c]).T).T
(Matrix([[a, b], [c, d]]) * Matrix([[x1, x2], [x3, x4]])).T == Matrix([[x1, x2], [x3, x4]]).T * Matrix([[a, b], [c, d]]).T
expand((Matrix([[a, b], [c, d]]) * Matrix([[x1, x2], [x3, x4]]) * Matrix([s, t])).T) == expand(Matrix([s, t]).T * Matrix([[x1, x2], [x3, x4]]).T * Matrix([[a, b], [c, d]]).T)
(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6], [7, 8]])).T != Matrix([[1, 2], [3, 4]]).T * Matrix([[5, 6], [7, 8]]).T
(Matrix([[1, 2], [3, 4]]) + Matrix([[5, 6], [7, 8]])).T == Matrix([[1, 2], [3, 4]]).T + Matrix([[5, 6], [7, 8]]).T
Matrix([[0, 1], [0, 0]]) * Matrix([[0, 0], [1, 0]]) != Matrix([[0, 0], [1, 0]]) * Matrix([[0, 1], [0, 0]])
Matrix([[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0]])**2 == Matrix([[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0],[0,0,0,0,0]])
Matrix([[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0]])**4 == Matrix([[0,0,0,0,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
Matrix([[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0]])**5 == zeros(5, 5) == Matrix([[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0]])**6
Matrix([[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0]]) * Matrix([a, b, c, d, f]) == Matrix([b, c, d, f, 0])
bool((Matrix([[Rational(1,6), Rational(1,2), Rational(1,3)], [Rational(1,2), Rational(1,4), Rational(1,4)], [Rational(1,3), Rational(1,4), Rational(5,12)]])**30 - ones(3, 3) / 3).norm() < Rational(1, 10**12))
Matrix([[Rational(1,6), Rational(1,2), Rational(1,3)], [Rational(1,2), Rational(1,4), Rational(1,4)], [Rational(1,3), Rational(1,4), Rational(5,12)]]) * ones(3, 1) == ones(3, 1)
(Matrix([1, 0, 1, 0]).T * Matrix([[1, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 1]]) * Matrix([1, 0, 1, 0]))[0] == 0
(Matrix([1, 0, 1, 0]).T * Matrix([1, 0, 1, 0]))[0] == 2
(Matrix([1, 1, 0, 1]).T * Matrix([[1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, 0], [-1, -1, 0, 2]]) * Matrix([1, 1, 0, 1]))[0] == 0
(Matrix([1, 1, 0, 1]).T * Matrix([1, 1, 0, 1]))[0] == 3
len([1 for u in range(1, 16) if (lambda v: (v.T * Matrix([[1, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 1]]) * v)[0] == 0)(Matrix([(u >> 3) & 1, (u >> 2) & 1, (u >> 1) & 1, u & 1]))]) == 1
Matrix([[1, 0], [0, 1], [0, 0]]).nullspace() == []
Matrix([[1, 0, 0], [0, 1, 0]]) * Matrix([[1, 0], [0, 1], [0, 0]]) == eye(2)
Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]) * Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]) == eye(3)
2 * 4 * 4 == 32 and 4 * 4 * 4 + 4 * 4 == 80 and 32 < 80
```
