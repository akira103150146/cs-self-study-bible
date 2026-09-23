---
kind: 診斷考
when: 第 2 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
Let $\mathbf{u} = \begin{bmatrix} 1 \\ -2 \end{bmatrix}$ and $\mathbf{v} = \begin{bmatrix} 3 \\ 1 \end{bmatrix}$. Compute $\mathbf{u} - 2\mathbf{v}$.

- A. $\begin{bmatrix} -5 \\ -4 \end{bmatrix}$
- B. $\begin{bmatrix} -5 \\ -3 \end{bmatrix}$
- C. $\begin{bmatrix} -2 \\ -3 \end{bmatrix}$
- D. $[\,-5 \;\; -4\,]$

### 答案
A

### 為什麼
$2\mathbf{v} = (6, 2)$,每個分量都乘 2。$\mathbf{u} - 2\mathbf{v} = (1 - 6,\ -2 - 2) = (-5, -4)$。

### 迷思對照
- **B** 純量倍數只乘了第一個分量,$2\mathbf{v}$ 寫成 $(6, 1)$,得 $(1 - 6, -2 - 1)$ → 觀念 1:純量倍數是**每個**分量都乘
- **C** 忘了乘 2,算成 $\mathbf{u} - \mathbf{v}$ → 觀念 1 例 1:先算純量倍數再相減
- **D** 數字對,但寫成橫的列矩陣 → 觀念 1:$(a, b)$ 是**直的**行向量的省略寫法,和 $1 \times 2$ 的列矩陣不同(是非題 23)

## Q2 · 觀念 2
Which augmented matrix has the same solution set as the vector equation
$$x_1\begin{bmatrix} 1 \\ 4 \end{bmatrix} + x_2\begin{bmatrix} 2 \\ 5 \end{bmatrix} = \begin{bmatrix} 3 \\ 6 \end{bmatrix}?$$

- A. $\left[\begin{array}{rr|r} 1 & 4 & 3 \\ 2 & 5 & 6 \end{array}\right]$
- B. $\left[\begin{array}{rr|r} 1 & 2 & 3 \\ 4 & 5 & 6 \end{array}\right]$
- C. $\left[\begin{array}{rr|r} 1 & 2 & 0 \\ 4 & 5 & 0 \end{array}\right]$
- D. $\left[\begin{array}{rr|r} 3 & 1 & 2 \\ 6 & 4 & 5 \end{array}\right]$

### 答案
B

### 為什麼
向量要**直的**放成一行:第一行是 $\mathbf{a}_1 = (1, 4)$、第二行是 $\mathbf{a}_2 = (2, 5)$、最後一行是 $\mathbf{b} = (3, 6)$,也就是 $[\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{b}\,]$。

### 迷思對照
- **A** 把向量橫著放成列 → 觀念 2 易錯點:向量要直的放成一行
- **C** 漏掉右邊的 $\mathbf{b}$,右邊寫成 0 → 觀念 2 例 2:增廣矩陣的最後一行就是 $\mathbf{b}$
- **D** 把 $\mathbf{b}$ 放到最前面 → 觀念 2 的方框:$[\,\mathbf{a}_1 \;\; \cdots \;\; \mathbf{a}_n \;\; \mathbf{b}\,]$,$\mathbf{b}$ 在最後

## Q3 · 觀念 3
Let $\mathbf{v}$ be a nonzero vector in $\mathbb{R}^3$. Which best describes $\operatorname{Span}\{\mathbf{v}\}$?

- A. the single vector $\mathbf{v}$
- B. the line through $\mathbf{0}$ and $\mathbf{v}$
- C. a plane through $\mathbf{0}$
- D. all of $\mathbb{R}^3$

### 答案
B

### 為什麼
$\operatorname{Span}\{\mathbf{v}\}$ 是 $\mathbf{v}$ 的**所有**純量倍數 $c\mathbf{v}$,包括 $c = 0$(原點)和負數,排起來是一條通過原點的直線。

### 迷思對照
- **A** 以為 Span 只是向量本身 → 觀念 3 易錯點:Span 是**所有**線性組合
- **C** 把一個向量的 Span 和兩個向量的 Span 搞混 → 觀念 3 例 1 的圖:一個向量是直線、兩個是平面
- **D** 以為「所有倍數」就能走到任何地方 → 觀念 3 例 1:純量倍數只能在同一條線上前後走

## Q4 · 觀念 4
Compute $\begin{bmatrix} 1 & 2 \\ 0 & 1 \\ 3 & 4 \end{bmatrix}\begin{bmatrix} 1 \\ -1 \end{bmatrix}$.

- A. $\begin{bmatrix} -1 \\ -1 \\ -1 \end{bmatrix}$
- B. Not defined, because the matrix has 3 rows but the vector has 2 entries.
- C. $\begin{bmatrix} 3 \\ 1 \\ 7 \end{bmatrix}$
- D. $\begin{bmatrix} 1 & -2 \\ 0 & -1 \\ 3 & -4 \end{bmatrix}$

### 答案
A

### 為什麼
$A$ 有 2 行、$\mathbf{x}$ 有 2 個分量,乘積有定義,結果有 3 個分量($A$ 的列數)。照定義:$1 \cdot (1, 0, 3) + (-1) \cdot (2, 1, 4) = (-1, -1, -1)$。

### 迷思對照
- **B** 拿 $A$ 的**列數**去和 $\mathbf{x}$ 比 → 觀念 4:要比的是 $A$ 的**行數**
- **C** 漏了 $-1$ 的負號,算成每一列直接相加,也就是 $A(1, 1)$ → 觀念 4 例 4:列向量規則要**對應相乘**再相加
- **D** 逐元素相乘,沒有加起來(就像 NumPy 的 `A * x`) → 觀念 4 在資工哪裡用:`A * x` 不是 $A\mathbf{x}$

## Q5 · 觀念 5
A $3 \times 4$ matrix $A$ has exactly 2 pivot positions. What can you conclude about $A\mathbf{x} = \mathbf{b}$?

- A. It is consistent for every $\mathbf{b}$ in $\mathbb{R}^3$, because $A$ has more columns than rows.
- B. It is inconsistent for every $\mathbf{b}$ in $\mathbb{R}^3$.
- C. It is inconsistent for some $\mathbf{b}$ in $\mathbb{R}^3$.
- D. Nothing, unless we also look at the augmented matrix $[\,A \;\; \mathbf{b}\,]$.

### 答案
C

### 為什麼
3 列只有 2 個 pivot,一定有一列沒有 pivot。由 Theorem 4,$A$ 的行不能生成 ℝ³,所以**存在**某個 $\mathbf{b}$ 讓方程式無解。但 $\mathbf{b} = \mathbf{0}$ 一定有解,所以不是對每個 $\mathbf{b}$ 都無解。

### 迷思對照
- **A** 以為行比列多就一定能生成 ℝᵐ → 觀念 5 易錯點:要看每一列有沒有 pivot
- **B** 把「不是每個都有解」誤讀成「每個都無解」 → 觀念 5 例 1:有些 $\mathbf{b}$(平面上的)有解
- **D** 不知道 Theorem 4 只需要看係數矩陣 → 觀念 5 的 Warning 與證明時刻

## 驗算
```check
Matrix([1, -2]) - 2 * Matrix([3, 1]) == Matrix([-5, -4])
Matrix([1, -2]) - Matrix([6, 1]) == Matrix([-5, -3])
Matrix([1, -2]) - Matrix([3, 1]) == Matrix([-2, -3])
Matrix([[1, 2], [0, 1], [3, 4]]) * Matrix([1, -1]) == Matrix([-1, -1, -1])
Matrix([[1, 2], [0, 1], [3, 4]]) * Matrix([1, 1]) == Matrix([3, 1, 7])
Matrix([[1, 2, 3], [4, 5, 6]]).rref()[0] == Matrix([[1, 0, -1], [0, 1, 2]])
-1 * Matrix([1, 4]) + 2 * Matrix([2, 5]) == Matrix([3, 6])
```
