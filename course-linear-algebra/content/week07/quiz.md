---
kind: 診斷考
when: 第 7 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
Which of the following sets is a subspace of $\mathbb{R}^2$?

- A. The set of all $(x, y)$ with $y = 2x$
- B. The set of all $(x, y)$ with $y = 2x + 1$
- C. The set of all $(x, y)$ with $x \ge 0$ and $y \ge 0$
- D. The set of all $(x, y)$ with $xy = 0$

### 答案
A

### 為什麼
A 是一條**過原點**的直線:含 $\mathbf{0}$、兩個解相加仍滿足 $y = 2x$、乘任何純量也滿足。三條性質全過。

### 迷思對照
- **B** 只看「是直線」就說是子空間 → 觀念 1:不過原點的直線不含 $\mathbf{0}$,第一條就掛了
- **C** 只驗加法、忘了純量乘法 → 觀念 1 的四格圖第 (1) 格:第一象限乘 $-1$ 就跑出去了
- **D** 只驗純量乘法、忘了加法 → 觀念 1 的四格圖第 (4) 格:兩軸的聯集,$(1,0) + (0,1) = (1,1)$ 不在裡面

## Q2 · 觀念 2
Let $A$ be a $3 \times 5$ matrix. Which statement is correct?

- A. $\operatorname{Nul} A$ is a subspace of $\mathbb{R}^5$ and $\operatorname{Col} A$ is a subspace of $\mathbb{R}^3$.
- B. $\operatorname{Nul} A$ is a subspace of $\mathbb{R}^3$ and $\operatorname{Col} A$ is a subspace of $\mathbb{R}^5$.
- C. Both $\operatorname{Nul} A$ and $\operatorname{Col} A$ are subspaces of $\mathbb{R}^5$.
- D. $\operatorname{Col} A = \mathbb{R}^3$, because $A$ has more columns than rows.

### 答案
A

### 為什麼
$\operatorname{Nul} A$ 的元素是**解向量**,有 5 個分量(行數)⇒ 在 $\mathbb{R}^5$ 裡。$\operatorname{Col} A$ 的元素是**行向量的組合**,有 3 個分量(列數)⇒ 在 $\mathbb{R}^3$ 裡。**先問「這個向量有幾個分量」,答案就出來了。**

### 迷思對照
- **B** 把兩個空間的家對調 → 觀念 2 的「兩個空間」圖:左 $\mathbb{R}^n$ 是零空間、右 $\mathbb{R}^m$ 是行空間
- **C** 以為兩者都住在同一個空間 → 觀念 2:只有方陣時兩者才都在 $\mathbb{R}^n$,而且仍是不同的子空間
- **D** 以為「行多於列」就一定張滿 → 觀念 5:$\operatorname{Col} A = \mathbb{R}^3$ 要 $\operatorname{rank} A = 3$,行多不保證樞軸多

## Q3 · 觀念 3
The matrix $A$ and an echelon form of $A$ are

$$A = \begin{bmatrix} 1 & 3 & 2 \\ 2 & 6 & 5 \end{bmatrix} \sim \begin{bmatrix} 1 & 3 & 2 \\ 0 & 0 & 1 \end{bmatrix}$$

Which set is a basis for $\operatorname{Col} A$?

- A. $\left\{\begin{bmatrix} 1 \\ 2 \end{bmatrix}, \begin{bmatrix} 2 \\ 5 \end{bmatrix}\right\}$
- B. $\left\{\begin{bmatrix} 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 2 \\ 1 \end{bmatrix}\right\}$
- C. $\left\{\begin{bmatrix} 1 \\ 2 \end{bmatrix}, \begin{bmatrix} 3 \\ 6 \end{bmatrix}\right\}$
- D. $\left\{\begin{bmatrix} 1 \\ 2 \end{bmatrix}, \begin{bmatrix} 3 \\ 6 \end{bmatrix}, \begin{bmatrix} 2 \\ 5 \end{bmatrix}\right\}$

### 答案
A

### 為什麼
階梯形顯示樞軸在第 **1、3** 行,所以要取 **$A$ 自己**的第 1、3 行:$(1,2)$ 與 $(2,5)$。

### 迷思對照
- **B** 拿階梯形的樞軸行當基底 → 觀念 3 的 Warning:列運算改變行本身,$(1,0)$ 不在 $\operatorname{Col} A$ 裡
- **C** 只會取「前兩行」→ 觀念 3:樞軸位置由階梯形決定,第 2 行是 $3 \times$ 第 1 行,不是樞軸行
- **D** 把所有行都放進去 → 觀念 3:基底不能有多餘的向量,三個 $\mathbb{R}^2$ 向量必相依

## Q4 · 觀念 4
Let $\mathbf{b}_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} 2 \\ -1 \end{bmatrix}$, $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2\}$, and $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$. What is $\mathbf{x}$?

- A. $\begin{bmatrix} 7 \\ 1 \end{bmatrix}$
- B. $\begin{bmatrix} 7/3 \\ 1/3 \end{bmatrix}$
- C. $\begin{bmatrix} 3 \\ 2 \end{bmatrix}$
- D. $\begin{bmatrix} 7 \\ 5 \end{bmatrix}$

### 答案
A

### 為什麼
給的是**座標**,要求的是**向量本身**,所以把座標當權重**乘進去**:$\mathbf{x} = 3\mathbf{b}_1 + 2\mathbf{b}_2 = (3 + 4, \; 3 - 2) = (7, 1)$。

### 迷思對照
- **B** 方向做反了,去解 $P_{\mathcal{B}}\mathbf{c} = (3,2)$ → 觀念 4 的兩方向表:給座標是乘、給向量才是解
- **C** 以為座標向量就是那個向量 → 觀念 4:$\mathbf{x}$ 與 $[\,\mathbf{x}\,]_{\mathcal{B}}$ 是同一點的兩種地址
- **D** $\mathbf{b}_2$ 的第二個分量漏了負號 → 逐分量算:$3(1) + 2(-1) = 1$

## Q5 · 觀念 5
Let $A$ be a $4 \times 9$ matrix with $\operatorname{rank} A = 3$. What is $\dim \operatorname{Nul} A$?

- A. 6
- B. 1
- C. 3
- D. 5

### 答案
A

### 為什麼
Rank Theorem 用的是**行數**:$\dim \operatorname{Nul} A = 9 - \operatorname{rank} A = 9 - 3 = 6$。

### 迷思對照
- **B** 用列數 4 代替行數 9 → 觀念 5:$\operatorname{Nul} A$ 住在 $\mathbb{R}^9$,帳要對 9 記
- **C** 以為零空間的維度等於 rank → 觀念 5:兩者相加才是行數,不是相等
- **D** 把 $\operatorname{rank}$ 與列數搞混($9 - 4$)→ 觀念 5:公式裡減掉的是 rank
