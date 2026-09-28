---
kind: 診斷考
when: 第 6 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
Let $A$ be a $5 \times 5$ matrix whose columns are linearly independent. Which statement must be **false**?

- A. The transformation $\mathbf{x} \mapsto A\mathbf{x}$ is onto $\mathbb{R}^5$.
- B. There is a $\mathbf{b}$ in $\mathbb{R}^5$ for which $A\mathbf{x} = \mathbf{b}$ has no solution.
- C. $A$ has 5 pivot positions.
- D. $A$ is row equivalent to $I_5$.

### 答案
B
### 為什麼
各行線性獨立是 IMT 的 (e),$A$ 又是方陣,所以十二條全部成立。特別是 (g):$A\mathbf{x} = \mathbf{b}$ 對**每個** $\mathbf{b}$ 都有解,所以 **B** 選項不可能成立。A、C、D 分別是 (i)、(c)、(b),都成立。

### 迷思對照
- **A** 以為一對一與映成在方陣上可以分開 → 觀念 1 的幾何意義:方陣時「不壓扁」與「不漏掉」同時發生
- **C** 以為獨立和樞軸數無關 → 觀念 1:(e) 與 (c) 是同一件事
- **D** 以為「化成 $I$」是更強的條件 → 觀念 1 的等價鏈:(c) ⇒ (b)

## Q2 · 觀念 2
$M$ is an $n \times n$ matrix and there is a matrix $D$ with $MD = I$. Which conclusion is correct, and which statement of the Invertible Matrix Theorem justifies it?

- A. Nothing follows: $MD = I$ is weaker than $DM = I$, so $M$ need not be invertible.
- B. $M$ is invertible by (k), and moreover $D = M^{-1}$, so $DM = I$ as well.
- C. $M$ is invertible by (j), because $D$ is a left inverse of $M$.
- D. $D$ is invertible by (k), but nothing follows about $M$.

### 答案
B

### 為什麼
條款 **(k)** 就是「存在 $D$ 使 $MD = I$」。對**方陣**而言它等價於可逆,所以 $M$ 可逆;再把 $MD = I$ 兩邊左乘 $M^{-1}$ 就得到 $D = M^{-1}$,因此 $DM = I$ 也成立。

### 迷思對照
- **A** 以為單邊的 $I$ 不夠 → 觀念 2:對**方陣**而言 (k) 就足夠;非方陣才需要兩邊都驗
- **C** 把 (j)(左反矩陣 $CA = I$)與 (k)(右反矩陣 $AD = I$)記反 → 觀念 1 的清單:$D$ 在 $M$ 的**右邊**
- **D** 只看到 $D$ 可逆就停住 → 觀念 2:(k) 講的是 $M$ 可逆,而且兩者互為反矩陣

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

- A. Compute $L^{-1}U^{-1}\mathbf{b}$.
- B. Compute $A^{-1}\mathbf{b}$, since $A^{-1} = L^{-1}U^{-1}$.
- C. Solve $L\mathbf{y} = \mathbf{b}$ first, then solve $U\mathbf{x} = \mathbf{y}$.
- D. Solve $U\mathbf{y} = \mathbf{b}$ first, then solve $L\mathbf{x} = \mathbf{y}$.

### 答案
C
### 為什麼
$A\mathbf{x} = (LU)\mathbf{x} = L(U\mathbf{x}) = \mathbf{b}$。令 $\mathbf{y} = U\mathbf{x}$,先由 $L\mathbf{y} = \mathbf{b}$ 前代解出 $\mathbf{y}$,再由 $U\mathbf{x} = \mathbf{y}$ 回代解出 $\mathbf{x}$。

### 迷思對照
- **A** 反矩陣的順序寫反 → 第 5 週 Theorem 6(b):$(LU)^{-1} = U^{-1}L^{-1}$
- **B** 又求反矩陣了 → 觀念 5 的成本表:LU 的重點就是**不要**算反矩陣
- **D** 兩個系統的順序弄反 → 觀念 5:$L$ 在左邊,所以先碰到 $\mathbf{b}$ 的是 $L$

## Q5 · 觀念 6
While row reducing $A$ to $U$, you use the operation "row 3 minus 2 times row 1." What is the $(3,1)$ entry of $L$?

- A. $-2$
- B. $1/2$
- C. $0$
- D. $2$

### 答案
D
### 為什麼
$L$ 記的是「怎麼**還原**」,所以乘數的符號和你做的運算相反:做「減 2 倍」,$L$ 的對應格就是 $+2$。等價的看法是「把該行標記的元素除以樞軸」,得到的就是 $+2$。

### 迷思對照
- **A** 直接把運算的係數抄進去 → 觀念 6:$L = (E_p \cdots E_1)^{-1}$,是反矩陣
- **B** 把「除以樞軸」誤解成「乘數取倒數」→ 觀念 6:除的是那一行的元素,不是乘數
- **C** 以為 $L$ 只有對角線 → 觀念 6:$L$ 的下三角記錄所有乘數
