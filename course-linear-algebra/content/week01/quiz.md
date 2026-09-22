---
kind: 診斷考
when: 第 1 週實作課開頭
minutes: 10
---
## Q1 · 觀念 1
A system of two linear equations in $x_1, x_2$ describes two parallel lines that do not coincide. How many solutions does the system have?

- A. $0$
- B. $1$
- C. $2$
- D. infinitely many

### 答案
A

### 為什麼
平行又不重合的兩條線沒有共同點,所以無解。

### 迷思對照
- **B** 以為兩條線一定會相交在某一點 → 觀念 1 幾何意義的圖:三種情況
- **C** 以為「兩條方程式」就有兩個解 → 觀念 1 白話說:不可能剛好兩個解
- **D** 把「平行」和「重合」搞混 → 觀念 1 幾何意義的圖:平行 vs 重合

## Q2 · 觀念 2
Which of the following is **not** an elementary row operation?

- A. Swap row 1 and row 3.
- B. Multiply row 2 by $-\frac12$.
- C. Replace row 3 by (row 3) $- 4 \times$ (row 1).
- D. Multiply row 1 by $0$.

### 答案
D

### 為什麼
Scaling 必須乘一個**不為 0** 的數,乘 0 會讓方程式變成 $0 = 0$,沒辦法復原。A、B、C 分別是 interchange、scaling、replacement,都合法。

### 迷思對照
- **A** 以為交換方程式的順序會改變解 → 觀念 2:interchange 和證明時刻
- **B** 以為只能乘正整數,乘負數或分數不合法 → 觀念 2:scaling 只要求不為 0
- **C** 以為 replacement 只能用相鄰的列 → 觀念 2:replacement 可以用任何一列的倍數

## Q3 · 觀念 4
Which matrix is in reduced echelon form?

- A. $\begin{bmatrix} 1 & 2 & 0 \\ 0 & 0 & 1 \end{bmatrix}$
- B. $\begin{bmatrix} 1 & 2 & 3 \\ 0 & 1 & 4 \end{bmatrix}$
- C. $\begin{bmatrix} 0 & 1 & 2 \\ 1 & 0 & 3 \end{bmatrix}$
- D. $\begin{bmatrix} 2 & 0 & 1 \\ 0 & 1 & 3 \end{bmatrix}$

### 答案
A

### 為什麼
A 的首項都是 1、一列比一列靠右、所在的行其他位置都是 0。B 的第 2 個 pivot 上方是 2 不是 0;C 不是梯形(第 2 列的首項在左邊);D 的第 1 個首項是 2。

### 迷思對照
- **B** 忘了 pivot **上方**也必須是 0 → 觀念 4:RREF 多出來的條件 4、5
- **C** 沒檢查首項要一列比一列靠右 → 觀念 4:樓梯形狀(條件 2)
- **D** 忘了 RREF 的首項必須是 1 → 觀念 4:RREF 多出來的條件 4、5

## Q4 · 觀念 5
The reduced echelon form of an augmented matrix is $\left[\begin{array}{rrr|r} 1 & 0 & 2 & 3 \\ 0 & 1 & -1 & 4 \\ 0 & 0 & 0 & 0 \end{array}\right]$. How many solutions does the system have?

- A. none
- B. exactly one
- C. infinitely many
- D. cannot tell without the original matrix

### 答案
C

### 為什麼
最後一行沒有 pivot → 有解;$x_3$ 沒有 pivot,是自由變數 → 無限多解。

### 迷思對照
- **A** 把全 0 列 $[\,0 \;\; 0 \;\; 0 \mid 0\,]$ 當成「$0 = $ 非零數」 → 觀念 5 的流程圖第一個問題
- **B** 看到兩個 pivot 就以為唯一解,沒有去數自由變數 → 觀念 5:基本變數與自由變數
- **D** 不知道 RREF 和原矩陣的解集相同 → 證明時刻:列運算不改變解集

## Q5 · 觀念 3
For which value of $h$ is the system with augmented matrix $\left[\begin{array}{rr|r} 1 & 2 & h \\ 3 & 6 & 9 \end{array}\right]$ consistent?

### 答案
$h = 3$

### 為什麼
$R_2 \leftarrow R_2 - 3R_1$ 得 $[\,0 \;\; 0 \mid 9 - 3h\,]$。要有解,這一列必須是 $0 = 0$,所以 $h = 3$。

### 迷思對照
- **$h \neq 3$** 把條件寫反,以為最後一列不是 0 才有解 → 觀念 3:三角形式裡的 $0 = b$ 什麼時候矛盾
- **任何 $h$ 都可以** 沒化簡就判斷,以為兩條方程式一定有解 → 觀念 1:平行線無解

## 驗算
```check
Matrix([[1, 2, 0], [0, 0, 1]]).rref()[0] == Matrix([[1, 2, 0], [0, 0, 1]])
Matrix([[1, 2, 3], [0, 1, 4]]).rref()[0] != Matrix([[1, 2, 3], [0, 1, 4]])
Matrix([[1, 0, 2, 3], [0, 1, -1, 4], [0, 0, 0, 0]]).rref()[1] == (0, 1)
Matrix([[1, 2, h], [3, 6, 9]]).echelon_form()[1, 2] == 9 - 3*h
solve(9 - 3*h, h) == [3]
```
