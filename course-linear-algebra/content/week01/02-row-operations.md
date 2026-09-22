---
title_en: Augmented Matrices and Row Operations
title_zh: 增廣矩陣與列運算
sub: Drop the variable names, keep the numbers, operate on rows
level: basic
lab_hook: "`B[2] = B[2] - 5 * B[0]`(對 NumPy 陣列做一次列運算,就是例 2 的第一步)"
---
## 觀念
Record a linear system as its **augmented matrix**: each row is one equation, each column holds one variable's coefficients, and the last column holds the constants. Three **elementary row operations** are allowed:

1. **Replacement** — add a multiple of one row to another row.
2. **Interchange** — swap two rows.
3. **Scaling** — multiply a row by a *nonzero* constant.

Two matrices connected by a sequence of row operations are **row equivalent**. Row-equivalent augmented matrices describe systems with **the same solution set**.

## 白話說
解方程組的時候,變數名稱 $x_1, x_2, x_3$ 其實只是在佔位子。把它們拿掉,只留係數和常數,排成一張長方形的數字表,就是**增廣矩陣**:一列是一條方程式,最後一行是等號右邊的常數,中間畫一條直線隔開。

原本對方程式做的消去動作,現在變成對「列」做三種操作:把某列的倍數加到另一列、兩列對調、某列乘上一個**不是 0** 的數。這三招都**可以復原**,所以做完之後解不會變——這正是本週證明時刻要證的事。

## 在資工哪裡用
在程式裡,矩陣就是一個二維陣列(NumPy 的 `np.array`)。列運算就是對陣列的某一列做運算,例如 `A[2] = A[2] - 5 * A[0]`。實作課第一步就做這件事,而且你會看到它和手算的每一步一模一樣。

## 原理
三種列運算分別對應到解方程組時本來就在做的三件事:

- **Replacement**:「第 3 式減去第 1 式的 5 倍」——加減消去法。
- **Interchange**:把方程式換個順序寫——不影響任何一條方程式本身。
- **Scaling**:整條方程式兩邊同乘一個數——例如把 $2x_2 - 8x_3 = 8$ 除以 2。

為什麼 scaling 要求**不為 0**?乘 0 會把方程式變成 $0 = 0$,原本的限制條件就消失了,解集可能變大,而且沒辦法復原(除以 0 沒有意義)。另外兩種運算天生就能復原:replacement 加了 $c$ 倍就減回 $c$ 倍,interchange 再換一次就回來。

**記號**:$R_3 \leftarrow R_3 - 5R_1$ 讀作「把第 3 列換成『第 3 列減 5 倍第 1 列』」。只有箭頭左邊那一列會被改寫,第 1 列保持不動。

## 老師講解
### 例 1
Write the augmented matrix of the system $x_1 - 2x_2 + x_3 = 0,\;\; 2x_2 - 8x_3 = 8,\;\; 5x_1 - 5x_3 = 10$.

1. 一條方程式變成一列,每一行固定對應一個未知數:第 1 行放 $x_1$ 的係數,第 2 行放 $x_2$,第 3 行放 $x_3$,最後一行放常數。
2. 缺少的未知數,係數就填 $0$:第 2 式沒有 $x_1$,第 3 式沒有 $x_2$。
3. 寫出來並在常數前畫一條直線:
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 2 & -8 & 8 \\ 5 & 0 & -5 & 10 \end{array}\right]$$

### 例 2
Solve the system in Example 1 using row operations.

1. 目標是讓左下角變成 0。先用第 1 列消掉第 3 列開頭的 5:$R_3 \leftarrow R_3 - 5R_1$,第 3 列變成 $[\,0 \;\; 10 \;\; {-10} \mid 10\,]$。
2. 第 2 列全部可以被 2 整除,先化簡:$R_2 \leftarrow \tfrac12 R_2$,第 2 列變成 $[\,0 \;\; 1 \;\; {-4} \mid 4\,]$。
3. 用第 2 列消掉第 3 列的 10:$R_3 \leftarrow R_3 - 10R_2$,第 3 列變成 $[\,0 \;\; 0 \;\; 30 \mid {-30}\,]$。
4. $R_3 \leftarrow \tfrac{1}{30} R_3$,第 3 列變成 $[\,0 \;\; 0 \;\; 1 \mid {-1}\,]$,也就是 $x_3 = -1$。現在矩陣是
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 1 & -4 & 4 \\ 0 & 0 & 1 & -1 \end{array}\right]$$
5. 由下往上代回:第 2 列說 $x_2 - 4x_3 = 4$,所以 $x_2 = 4 + 4(-1) = 0$;第 1 列說 $x_1 - 2x_2 + x_3 = 0$,所以 $x_1 = 0 + 0 + 1 = 1$。
6. 驗算原方程組:$1 - 0 + (-1) = 0$ ✓;$0 - 8(-1) = 8$ ✓;$5 - 5(-1) = 10$ ✓。解是 $(1, 0, -1)$。

## 易錯點
做 replacement 時改錯列:$R_3 \leftarrow R_3 - 5R_1$ 是改寫**第 3 列**,第 1 列保持不動。學生常把兩列都改掉,或把結果寫到第 1 列去。

另一個常見錯:缺少的未知數沒有補 0,導致係數跑到錯的行。

## 教學提示
每一步都在右邊寫出操作記號($R_3 \leftarrow R_3 - 5R_1$),並要求學生照做。記號寫出來,錯了才找得到是哪一步;這也正是實作課程式碼的寫法(`A[2] = A[2] - 5 * A[0]`),先在紙上養成習慣,實作課就很順。

例 2 做完一定要驗算。讓學生看到「代回原題」是確認答案的唯一方法,不是可有可無的步驟。

## 練習
### 照做
Write the augmented matrix for the system $x_1 + 5x_2 = 7,\;\; -2x_1 - 7x_2 = -5$.

#### 解答
$$\left[\begin{array}{rr|r} 1 & 5 & 7 \\ -2 & -7 & -5 \end{array}\right]$$

### 照做
Solve the system in the previous exercise using row operations. Write the operation next to each step.

#### 解答
$R_2 \leftarrow R_2 + 2R_1$:第 2 列變成 $[\,0 \;\; 3 \mid 9\,]$,所以 $x_2 = 3$。代回第 1 列:$x_1 = 7 - 5 \cdot 3 = -8$。

驗算:$-2(-8) - 7(3) = 16 - 21 = -5$ ✓。解是 $(-8, 3)$。

### 變化
Solve the system whose augmented matrix is $\left[\begin{array}{rrr|r} 1 & -3 & 4 & -4 \\ 0 & 1 & -2 & 1 \\ 0 & 0 & 1 & 3 \end{array}\right]$. (It is already triangular — start from the bottom row.)

#### 解答
由下往上:$x_3 = 3$;$x_2 - 2x_3 = 1 \Rightarrow x_2 = 7$;$x_1 - 3x_2 + 4x_3 = -4 \Rightarrow x_1 = -4 + 21 - 12 = 5$。解是 $(5, 7, 3)$。

### 變化
Which row operation turns $\begin{bmatrix} 0 & 2 & 4 \\ 1 & 3 & 5 \end{bmatrix}$ into $\begin{bmatrix} 1 & 3 & 5 \\ 0 & 2 & 4 \end{bmatrix}$? Which operation undoes it?

#### 解答
Interchange:$R_1 \leftrightarrow R_2$。要復原,再做一次同樣的 $R_1 \leftrightarrow R_2$ 即可。

### 挑戰
Explain why "multiply a row by $0$" is not allowed as a row operation. Use the equation $x_1 + x_2 = 3$ as an example.

#### 解答
$x_1 + x_2 = 3$ 乘 0 之後變成 $0 = 0$,任何 $(x_1, x_2)$ 都滿足,原本的限制條件消失,解集會變大;而且沒辦法復原(除以 0 沒有意義)。列運算必須可以復原,才能保證解集不變。

## 驗算
```check
Matrix([[1, -2, 1, 0], [0, 2, -8, 8], [5, 0, -5, 10]]).rref()[0] == Matrix([[1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, -1]])
Matrix([[1, 5, 7], [-2, -7, -5]]).rref()[0] == Matrix([[1, 0, -8], [0, 1, 3]])
Matrix([[1, -3, 4, -4], [0, 1, -2, 1], [0, 0, 1, 3]]).rref()[0] == Matrix([[1, 0, 0, 5], [0, 1, 0, 7], [0, 0, 1, 3]])
# 例 2 中間步驟:R3 - 5R1、(1/2)R2、R3 - 10R2
Matrix([[5, 0, -5, 10]]) - 5*Matrix([[1, -2, 1, 0]]) == Matrix([[0, 10, -10, 10]])
Matrix([[0, 10, -10, 10]]) - 10*Matrix([[0, 1, -4, 4]]) == Matrix([[0, 0, 30, -30]])
```
