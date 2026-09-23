---
kind: 診斷考
when: 第 4 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
Let $A$ be a $4 \times 7$ matrix and define $T(\mathbf{x}) = A\mathbf{x}$. What are the domain and the codomain of $T$?

- A. domain $\mathbb{R}^7$, codomain $\mathbb{R}^4$
- B. domain $\mathbb{R}^4$, codomain $\mathbb{R}^7$
- C. domain $\mathbb{R}^7$, codomain $\mathbb{R}^7$
- D. Cannot tell without knowing the range of $T$.

### 答案
A

### 為什麼
$A\mathbf{x}$ 要有定義,$\mathbf{x}$ 必須有 7 個分量($A$ 的**行數**),所以定義域是 ℝ⁷;乘出來有 4 個分量($A$ 的**列數**),所以對應域是 ℝ⁴。

### 迷思對照
- **B** 把行數與列數的角色弄反 → 觀念 1:定義域看行數、對應域看列數
- **C** 以為定義域和對應域一樣 → 觀念 1 例 1:$3 \times 2$ 的矩陣給的是 $T : \mathbb{R}^2 \to \mathbb{R}^3$
- **D** 把對應域和值域混為一談 → 觀念 1:對應域由形狀決定,值域才需要算

## Q2 · 觀念 2
Which of the following transformations is **not** linear?

- A. $T(x_1, x_2) = (x_1 + x_2,\ x_1 - x_2)$
- B. $T(\mathbf{x}) = 3\mathbf{x}$
- C. $T(x_1, x_2) = (x_1 + 1,\ x_2)$
- D. $T(x_1, x_2) = (0,\ 0)$

### 答案
C

### 為什麼
$T(0, 0) = (1, 0) \neq \mathbf{0}$,違反線性變換必有的 $T(\mathbf{0}) = \mathbf{0}$(性質 3)。這是平移,屬於仿射變換。A、B、D 都可以寫成矩陣乘法,所以都線性。

### 迷思對照
- **A** 以為有減法就不線性 → 觀念 2:$(x_1 + x_2, x_1 - x_2)$ 的矩陣是 $\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$
- **B** 以為乘上常數就不線性 → 觀念 2 例 1:伸張是線性的
- **D** 以為「全部送到 $\mathbf{0}$」太特別所以不算 → 零變換的矩陣是零矩陣,仍然線性

## Q3 · 觀念 3
A linear transformation $T : \mathbb{R}^2 \to \mathbb{R}^2$ satisfies $T(\mathbf{e}_1) = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$ and $T(\mathbf{e}_2) = \begin{bmatrix} -3 \\ 0 \end{bmatrix}$. What is the standard matrix of $T$?

- A. $\begin{bmatrix} 1 & -3 \\ 2 & 0 \end{bmatrix}$
- B. $\begin{bmatrix} 1 & 2 \\ -3 & 0 \end{bmatrix}$
- C. $\begin{bmatrix} -3 & 1 \\ 0 & 2 \end{bmatrix}$
- D. $\begin{bmatrix} 1 & -3 \\ 0 & 2 \end{bmatrix}$

### 答案
A

### 為什麼
Theorem 10:$A = [\,T(\mathbf{e}_1) \;\; T(\mathbf{e}_2)\,]$,把兩個像**直的**放成第一、第二行。

### 迷思對照
- **B** 把像橫著放成列 → 觀念 3:$T(\mathbf{e}_j)$ 是第 $j$ **行**
- **C** 行的順序放反 → 觀念 3:第一行是 $T(\mathbf{e}_1)$
- **D** 兩行的分量混在一起抄 → 觀念 3 例 1:整個 $T(\mathbf{e}_1)$ 一起放進第一行

## Q4 · 觀念 4
What does the transformation with standard matrix $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ do to the plane?

- A. It reflects points through the $x_1$-axis.
- B. It reflects points through the $x_2$-axis.
- C. It rotates points through $90°$.
- D. It projects points onto the $x_1$-axis.

### 答案
A

### 為什麼
$\mathbf{e}_1 \mapsto \mathbf{e}_1$(不動)、$\mathbf{e}_2 \mapsto -\mathbf{e}_2$(上下翻),也就是 $(x_1, x_2) \mapsto (x_1, -x_2)$:對 $x_1$ 軸的反射。

### 迷思對照
- **B** 對 $x_2$ 軸反射是 $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$(變號的是第一個分量)→ 觀念 4 的表格
- **C** 旋轉 90° 是 $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$,不是對角矩陣 → 觀念 3 例 2
- **D** 投影會把某個分量變成 0,矩陣是 $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ → 觀念 4 的表格

## Q5 · 觀念 5
Let $A$ be the $5 \times 3$ standard matrix of a linear transformation $T$, and suppose $A$ has 3 pivot positions. Which is true?

- A. $T$ is one-to-one but not onto $\mathbb{R}^5$.
- B. $T$ is onto $\mathbb{R}^5$ but not one-to-one.
- C. $T$ is both one-to-one and onto $\mathbb{R}^5$.
- D. $T$ is neither one-to-one nor onto $\mathbb{R}^5$.

### 答案
A

### 為什麼
3 行都有 pivot → 各行線性獨立 → 一對一(Theorem 12(b))。但 5 列只有 3 個 pivot → 各行不生成 ℝ⁵ → 不是映成(Theorem 12(a))。

### 迷思對照
- **B** 映成看行、一對一看列(弄反了)→ 觀念 5 的對照表:映成看**列**、一對一看**行**
- **C** 以為 pivot 數等於行數就兩者都成立 → 觀念 5 Exercise 43:映成還需要 pivot 數等於**列數**
- **D** 以為「瘦高」的矩陣兩者都不行 → 觀念 5 例 2:$3 \times 2$ 的矩陣可以是一對一

## 驗算
```check
(zeros(4, 7) * zeros(7, 1)).shape == (4, 1)
Matrix([[1, 1], [1, -1]]) * Matrix([x1, x2]) == Matrix([x1 + x2, x1 - x2])
(lambda T: T(zeros(2, 1)))(lambda v: Matrix([v[0] + 1, v[1]])) == Matrix([1, 0])
Matrix.hstack(Matrix([1, 2]), Matrix([-3, 0])) == Matrix([[1, -3], [2, 0]])
Matrix([[1, 0], [0, -1]]) * Matrix([x1, x2]) == Matrix([x1, -x2])
Matrix([[-1, 0], [0, 1]]) * Matrix([x1, x2]) == Matrix([-x1, x2])
Matrix.vstack(eye(3), zeros(2, 3)).rank() == 3 and Matrix.vstack(eye(3), zeros(2, 3)).nullspace() == []
```
