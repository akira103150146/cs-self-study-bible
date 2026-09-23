---
kind: 診斷考
when: 第 6 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
Let $A$ be a $5 \times 5$ matrix whose columns are linearly independent. Which statement must be **false**?

- A. There is a $\mathbf{b}$ in $\mathbb{R}^5$ for which $A\mathbf{x} = \mathbf{b}$ has no solution.
- B. $A$ has 5 pivot positions.
- C. $A$ is row equivalent to $I_5$.
- D. The transformation $\mathbf{x} \mapsto A\mathbf{x}$ is onto $\mathbb{R}^5$.

### 答案
A

### 為什麼
各行線性獨立是 IMT 的 (e),$A$ 又是方陣,所以十二條全部成立。特別是 (g):$A\mathbf{x} = \mathbf{b}$ 對**每個** $\mathbf{b}$ 都有解,所以 A 選項不可能成立。B、C、D 分別是 (c)、(b)、(i),都成立。

### 迷思對照
- **B** 以為獨立和樞軸數無關 → 觀念 1:(e) 與 (c) 是同一件事
- **C** 以為「化成 $I$」是更強的條件 → 觀念 1 的等價鏈:(c) ⇒ (b)
- **D** 以為一對一與映成在方陣上可以分開 → 觀念 1 的幾何意義:方陣時「不壓扁」與「不漏掉」同時發生

## Q2 · 觀念 1
$A$ is a $4 \times 3$ matrix whose columns are linearly independent. What can you conclude about the equation $A\mathbf{x} = \mathbf{b}$?

- A. Nothing about existence of solutions; but if a solution exists it is unique.
- B. It has a unique solution for every $\mathbf{b}$ in $\mathbb{R}^4$.
- C. It has at least one solution for every $\mathbf{b}$ in $\mathbb{R}^4$.
- D. It has infinitely many solutions.

### 答案
A

### 為什麼
$A$ **不是方陣**,不能用可逆矩陣定理。各行獨立只告訴我們 $A\mathbf{x} = \mathbf{0}$ 只有零解(第 3 週),也就是「有解時解唯一」;**存在性要另外判斷**($4 \times 3$ 最多 3 個樞軸,不可能每一列都有樞軸,所以一定有某些 $\mathbf{b}$ 無解)。

### 迷思對照
- **B** 把 IMT 套在非方陣上 → 觀念 1:IMT applies only to square matrices
- **C** 同上,把「獨立」當成「張成」→ 觀念 1 的幾何意義:非方陣時兩者是不同的事
- **D** 把「獨立」記反成「相依」→ 第 3 週:獨立 ⇒ 沒有自由變數 ⇒ 不會有無窮多解

## Q3 · 觀念 4
A square matrix $A$ satisfies $\det A = 1$ and $\operatorname{cond}(A) \approx 10^4$. Using double precision (about 16 significant digits), roughly how many digits of the computed solution of $A\mathbf{x} = \mathbf{b}$ can be trusted?

- A. About 12
- B. All 16, because $\det A = 1$ is far from 0
- C. About 4
- D. None, because the matrix is singular

### 答案
A

### 為什麼
損失的位數大約是 $\log_{10}\operatorname{cond}(A) = 4$,所以 $16 - 4 = 12$ 位左右可信。**行列式的大小和數值穩定性沒有關係**——課本 Exercise 9 的矩陣正是 $\det = 1$ 但條件數約 23,000。

### 迷思對照
- **B** 用行列式判斷穩定性 → 觀念 4:$\det = 1$ 的矩陣條件數可以上萬
- **C** 把「損失的位數」當成「剩下的位數」→ 觀念 4 的估算法則:剩下 $16 - k$ 位
- **D** 把條件數大當成奇異 → 觀念 4:奇異矩陣的條件數是無限大,$10^4$ 還差得遠

## Q4 · 觀念 5
Given $A = LU$, how do you solve $A\mathbf{x} = \mathbf{b}$?

- A. Solve $L\mathbf{y} = \mathbf{b}$ first, then solve $U\mathbf{x} = \mathbf{y}$.
- B. Solve $U\mathbf{y} = \mathbf{b}$ first, then solve $L\mathbf{x} = \mathbf{y}$.
- C. Compute $L^{-1}U^{-1}\mathbf{b}$.
- D. Compute $A^{-1}\mathbf{b}$, since $A^{-1} = L^{-1}U^{-1}$.

### 答案
A

### 為什麼
$A\mathbf{x} = (LU)\mathbf{x} = L(U\mathbf{x}) = \mathbf{b}$。令 $\mathbf{y} = U\mathbf{x}$,先由 $L\mathbf{y} = \mathbf{b}$ 前代解出 $\mathbf{y}$,再由 $U\mathbf{x} = \mathbf{y}$ 回代解出 $\mathbf{x}$。

### 迷思對照
- **B** 兩個系統的順序弄反 → 觀念 5:$L$ 在左邊,所以先碰到 $\mathbf{b}$ 的是 $L$
- **C** 反矩陣的順序寫反 → 第 5 週 Theorem 6(b):$(LU)^{-1} = U^{-1}L^{-1}$
- **D** 又求反矩陣了 → 觀念 5 的成本表:LU 的重點就是**不要**算反矩陣

## Q5 · 觀念 6
While row reducing $A$ to $U$, you use the operation "row 3 minus 2 times row 1." What is the $(3,1)$ entry of $L$?

- A. $2$
- B. $-2$
- C. $1/2$
- D. $0$

### 答案
A

### 為什麼
$L$ 記的是「怎麼**還原**」,所以乘數的符號和你做的運算相反:做「減 2 倍」,$L$ 的對應格就是 $+2$。等價的看法是「把該行標記的元素除以樞軸」,得到的就是 $+2$。

### 迷思對照
- **B** 直接把運算的係數抄進去 → 觀念 6:$L = (E_p \cdots E_1)^{-1}$,是反矩陣
- **C** 把「除以樞軸」誤解成「乘數取倒數」→ 觀念 6:除的是那一行的元素,不是乘數
- **D** 以為 $L$ 只有對角線 → 觀念 6:$L$ 的下三角記錄所有乘數
