---
kind: 診斷考
when: 第 5 週實作課開頭
minutes: 10
---
## Q1 · 觀念 2
Let $A$ be a $3 \times 5$ matrix and let $B$ be a $5 \times 2$ matrix. Which statement is correct?

- A. $AB$ is $3 \times 2$, and $BA$ is not defined.
- B. $AB$ is $5 \times 5$, and $BA$ is $2 \times 3$.
- C. Both $AB$ and $BA$ are defined, and $AB = BA$.
- D. $AB$ is not defined, because $A$ and $B$ have different sizes.

### 答案
A

### 為什麼
$(3 \times 5)(5 \times 2)$:中間兩個數都是 5,對得上,所以 $AB$ 有定義,大小是外側兩個數 $3 \times 2$。反過來 $(5 \times 2)(3 \times 5)$ 的中間是 2 和 3,對不上,所以 $BA$ 沒有定義。

### 迷思對照
- **B** 把「內側相消、外側留下」記反了 → 觀念 2 的尺寸圖
- **C** 以為乘法可交換 → 觀念 2 例 3:$AB$ 有定義不代表 $BA$ 有定義
- **D** 以為兩個矩陣要一樣大才能相乘(那是**加法**的規則)→ 觀念 1 的加法 vs 觀念 2 的乘法

## Q2 · 觀念 2
Let $A = \begin{bmatrix} 2 & 3 \\ 1 & -5 \end{bmatrix}$ and $B = \begin{bmatrix} 4 & 3 \\ 1 & -2 \end{bmatrix}$. What is the entry in row 2, column 1 of $AB$?

- A. $-1$
- B. $8$
- C. $11$
- D. $4$

### 答案
A

### 為什麼
列乘行規則:拿 $A$ 的**第 2 列** $[\,1 \;\; {-5}\,]$ 乘 $B$ 的**第 1 行** $\begin{bmatrix} 4 \\ 1 \end{bmatrix}$,得到 $1(4) + (-5)(1) = -1$。

### 迷思對照
- **B** 把 $A$ 的第 2 列乘 $B$ 的第 2 列(拿錯方向)→ 觀念 2:左**列**乘右**行**
- **C** 算成第 1 列第 1 行 $= 2(4) + 3(1) = 11$(位置記反)→ 觀念 1:$(i, j)$ 是「第 $i$ 列、第 $j$ 行」
- **D** 逐格相乘 $1 \times 4 = 4$ → 觀念 2 的數值筆記:`A * B` 不是矩陣乘法

## Q3 · 觀念 3
Which formula is correct for all matrices $A$ and $B$ of appropriate sizes?

- A. $(AB)^T = B^TA^T$
- B. $(AB)^T = A^TB^T$
- C. $(A + B)^T = B^T - A^T$
- D. $(A^T)^T = A^T$

### 答案
A

### 為什麼
Theorem 3(d):轉置乘積要**反序**。用尺寸檢查最快——$A$ 是 $m \times n$、$B$ 是 $n \times p$,轉置後 $B^T$ 是 $p \times n$、$A^T$ 是 $n \times m$,只有 $B^TA^T$ 接得起來。

### 迷思對照
- **B** 忘了反序 → 觀念 3:$A^TB^T$ 通常根本沒有定義
- **C** 把加法也想成要反序、還多加了負號 → 觀念 3:$(A + B)^T = A^T + B^T$,加法沒有順序問題
- **D** 以為轉置兩次還是轉置 → 觀念 3:$(A^T)^T = A$,轉回來了

## Q4 · 觀念 4
For which value of $k$ is the matrix $\begin{bmatrix} 3 & 6 \\ 2 & k \end{bmatrix}$ **not** invertible?

- A. $k = 4$
- B. $k = 0$
- C. $k = 9$
- D. It is invertible for every $k$.

### 答案
A

### 為什麼
$\det = 3k - 6(2) = 3k - 12$。不可逆 $\iff \det = 0 \iff k = 4$。(此時兩行成比例:$\begin{bmatrix} 6 \\ 4 \end{bmatrix} = 2\begin{bmatrix} 3 \\ 2 \end{bmatrix}$。)

### 迷思對照
- **B** 以為對角線出現 0 就不可逆 → 觀念 4:$k = 0$ 時 $\det = -12 \ne 0$,仍然可逆
- **C** 把 $\det$ 算成 $ab - cd = 3(6) - 2k$ → 觀念 4 的易錯點:公式是 $ad - bc$
- **D** 以為所有方陣都可逆 → 觀念 4:$\det = 0$ 的方陣不可逆

## Q5 · 觀念 6
To rotate a figure about the origin by $\varphi$ and **then** translate it by $(h, k)$, which product of homogeneous-coordinate matrices is correct? Write $R$ for the rotation matrix and $T$ for the translation matrix.

- A. $TR$
- B. $RT$
- C. $T + R$
- D. Either order gives the same result.

### 答案
A

### 為什麼
齊次座標下,點寫在最右邊:$TR\mathbf{x}$ 表示 $\mathbf{x}$ 先碰到 $R$(旋轉),再碰到 $T$(平移)。**先做的寫右邊。**

### 迷思對照
- **B** 照「先旋轉後平移」的閱讀順序由左往右寫 → 觀念 6 例 2 的第 4 步:右邊先做
- **C** 以為合成是相加 → 觀念 2:合成變換對應矩陣**相乘**
- **D** 以為順序無所謂 → 觀念 6 的 Exercises 5–6:兩種順序算出來的矩陣不同
