---
kind: 診斷考
when: 第 3 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
For **any** matrix $A$, which statement about the homogeneous equation $A\mathbf{x} = \mathbf{0}$ is always true?

- A. It is consistent.
- B. It has a nontrivial solution.
- C. It has exactly one solution.
- D. Every nontrivial solution has all entries nonzero.

### 答案
A

### 為什麼
$\mathbf{x} = \mathbf{0}$ 永遠是解,所以齊次方程組一定相容。有沒有非平凡解、解是否唯一,要看有沒有自由變數,不是永遠成立。

### 迷思對照
- **B** 以為齊次方程組一定有非零解 → 觀念 1:有自由變數才有非平凡解
- **C** 以為齊次方程組只有 $\mathbf{0}$ 這個解 → 觀念 1 例 1:有自由變數時有無限多解
- **D** 以為非平凡解的每個分量都不能是 0 → 觀念 1 是非題 Exercise 28

## Q2 · 觀念 2
The reduced echelon form of an augmented matrix $[\,A \;\; \mathbf{b}\,]$ is $\left[\begin{array}{rrr|r} 1 & 0 & -2 & 3 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 0 & 0 \end{array}\right]$. Which is the general solution of $A\mathbf{x} = \mathbf{b}$ in parametric vector form?

- A. $\mathbf{x} = \begin{bmatrix} 3 \\ -1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} 2 \\ -1 \\ 1 \end{bmatrix}$
- B. $\mathbf{x} = \begin{bmatrix} 3 \\ -1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} -2 \\ 1 \\ 1 \end{bmatrix}$
- C. $\mathbf{x} = x_3\begin{bmatrix} 2 \\ -1 \\ 1 \end{bmatrix}$
- D. $\mathbf{x} = \begin{bmatrix} 2 \\ -1 \\ 1 \end{bmatrix} + x_3\begin{bmatrix} 3 \\ -1 \\ 0 \end{bmatrix}$

### 答案
A

### 為什麼
$x_1 - 2x_3 = 3$ 移項得 $x_1 = 3 + 2x_3$;$x_2 + x_3 = -1$ 得 $x_2 = -1 - x_3$。常數項 $(3, -1, 0)$ 是特解 $\mathbf{p}$,$x_3$ 的係數 $(2, -1, 1)$ 是齊次解的方向。

### 迷思對照
- **B** 移項時忘了變號,直接抄 RREF 的係數 → 觀念 2 例 1 的第 3 步:基本變數用自由變數表示
- **C** 漏掉特解 $\mathbf{p}$,只寫了齊次解 → 觀念 2:解 = 特解 + 齊次解
- **D** 把特解和方向向量的角色弄反 → 觀念 2 白話說:常數項才是 $\mathbf{p}$

## Q3 · 觀念 3
The columns of a matrix $A$ are linearly independent if and only if ...

- A. $A\mathbf{x} = \mathbf{0}$ has only the trivial solution.
- B. $A\mathbf{x} = \mathbf{0}$ has the trivial solution.
- C. $A$ has a pivot position in every row.
- D. $A\mathbf{x} = \mathbf{b}$ has a solution for every $\mathbf{b}$.

### 答案
A

### 為什麼
各行獨立 ⇔ $x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n = \mathbf{0}$ 只有全 0 的解 ⇔ $A\mathbf{x} = \mathbf{0}$ **只有**平凡解 ⇔ 每一**行**都是 pivot 行。

### 迷思對照
- **B** 漏了「只有」——平凡解永遠存在 → 觀念 3 是非題 Exercise 21
- **C** 把「看列」(生成)和「看行」(獨立)搞混 → 觀念 3 白話說的對照
- **D** 把線性獨立和上週的「生成 ℝᵐ」(Theorem 4)搞混 → 觀念 3 白話說的對照

## Q4 · 觀念 4
Which set is linearly **dependent**?

- A. $\left\{\begin{bmatrix} 1 \\ 2 \end{bmatrix}, \begin{bmatrix} 2 \\ 1 \end{bmatrix}\right\}$
- B. $\left\{\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}, \begin{bmatrix} -2 \\ -4 \\ -6 \end{bmatrix}\right\}$
- C. $\left\{\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}\right\}$
- D. $\left\{\begin{bmatrix} 2 \\ 4 \\ 6 \end{bmatrix}, \begin{bmatrix} 1 \\ 2 \\ 4 \end{bmatrix}\right\}$

### 答案
B

### 為什麼
兩個向量,看倍數:$(-2, -4, -6) = -2(1, 2, 3)$,是倍數,所以相依。D 的前兩個分量是 2 倍,第三個不是($4 \cdot 2 = 8 \neq 6$),不是倍數。

### 迷思對照
- **A** 看到分量用的是同樣的數字就以為相依 → 觀念 4 例 1:要看是不是**倍數**
- **C** 以為「向量個數比分量數少」就一定相依 → 觀念 4:兩個向量只看倍數
- **D** 只比了前兩個分量 → 觀念 4 易錯點:每個分量都要對得上才是倍數

## Q5 · 觀念 5
A set contains 4 vectors in $\mathbb{R}^3$, and no vector in the set is a multiple of another. What can you conclude?

- A. The set is linearly independent, because no two vectors are multiples.
- B. The set is linearly independent, as long as it does not contain the zero vector.
- C. The set is linearly dependent.
- D. Nothing, unless we row reduce.

### 答案
C

### 為什麼
4 個向量、每個只有 3 個分量,$4 > 3$,由 Theorem 8 一定相依,不用計算。

### 迷思對照
- **A** 把「兩個向量看倍數」用在四個向量上 → 觀念 5 例 1:兩兩不是倍數仍可能相依
- **B** 以為只要沒有零向量就獨立 → 觀念 5:Theorem 9 只說有零向量一定相依,反過來不成立
- **D** 不知道 Theorem 8 可以直接判斷 → 觀念 5 例 2 的檢查順序

## 驗算
```check
Matrix([[1, 0, -2, 3], [0, 1, 1, -1]]).rref()[0] == Matrix([[1, 0, -2, 3], [0, 1, 1, -1]])
Matrix([[1, 0, -2], [0, 1, 1]]) * Matrix([3, -1, 0]) == Matrix([3, -1])
Matrix([[1, 0, -2], [0, 1, 1]]) * Matrix([2, -1, 1]) == zeros(2, 1)
Matrix([[1, 2], [2, 1]]).rank() == 2
Matrix([[1, -2], [2, -4], [3, -6]]).rank() == 1
Matrix([[2, 1], [4, 2], [6, 4]]).rank() == 2
```
