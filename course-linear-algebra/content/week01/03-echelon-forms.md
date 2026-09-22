---
title_en: Echelon Forms, RREF and Pivots
title_zh: 梯形、簡化梯形與 pivot
sub: Row reduction always aims at the same staircase
level: mid
lab_hook: "`Matrix(A).rref()` 回傳 `(RREF, pivot 所在的行)`"
figure: staircase.svg
figure_caption: 梯形只要求樓梯形狀;簡化梯形再要求 pivot 是 1、而且 pivot 所在的行其他位置都是 0。
---
## 觀念
A matrix is in **echelon form** if

1. all nonzero rows are above any rows of all zeros;
2. each **leading entry** (the leftmost nonzero entry of a row) is in a column to the right of the leading entry of the row above it;
3. all entries below a leading entry are zero.

It is in **reduced echelon form (RREF)** if, in addition, every leading entry is $1$ and is the only nonzero entry in its column. Each matrix is row equivalent to **exactly one** RREF. A **pivot position** is a location that holds a leading 1 in the RREF, and a **pivot column** is a column that contains a pivot position.

## 白話說
列化簡的目標永遠是同一個形狀:**像樓梯一樣往右下走**。

- **梯形**(echelon form):每一列第一個非零的數叫「領頭數」,它必須比上一列的領頭數更靠右,而且領頭數底下全是 0。全是 0 的列放最下面。
- **簡化梯形**(RREF):再多兩個要求——領頭數都是 1,而且領頭數所在的那一行,其他位置全部是 0。

同一個矩陣,化簡的路線不同,梯形可能長得不一樣;但 **RREF 只有一種**。所以「pivot 在哪幾行」是矩陣本身的性質,不管誰來化簡、怎麼化簡,答案都一樣。

## 在資工哪裡用
SymPy 的 `Matrix(A).rref()` 會直接回傳 RREF 和 pivot 所在的行號。之後判斷方程組有沒有解、有幾個自由變數(觀念 4)、資料表有哪些欄位重複(第 3 週),全都是在「讀 pivot」。

## 原理
**列化簡演算法**分成兩個階段:

- **往前(forward phase)**:從最左邊不全為 0 的行開始,選一個非 0 的數當 pivot(需要時先換列),用 replacement 把 pivot **底下**全部消成 0;然後蓋住這一列,對剩下的子矩陣重複。做完得到梯形。
- **往回(backward phase)**:從**最下面**的 pivot 開始往上,先把 pivot 縮放成 1,再把 pivot **上方**全部消成 0。做完得到 RREF。

往回階段從下往上做,是因為下面的列 0 比較多,拿它去消上面的列,計算量最少。

**RREF 為什麼唯一**:證明在 Lay 附錄 A,本課只陳述不證明。它的意義是讓「pivot 位置」有明確定義。

**電腦怎麼選 pivot**:手算時挑好算的數;電腦則挑該行**絕對值最大**的數(partial pivoting),因為用很小的數當 pivot 會放大捨入誤差。實作課的「解讀」階段會親眼看到這件事。

## 老師講解
### 例 1
Which of the following matrices are in echelon form? Which are in reduced echelon form?
(a) $\begin{bmatrix} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 0 & 0 & 0 & 5/2 \end{bmatrix}$  (b) $\begin{bmatrix} 1 & 0 & 0 & 29 \\ 0 & 1 & 0 & 16 \\ 0 & 0 & 1 & 3 \end{bmatrix}$  (c) $\begin{bmatrix} 0 & 1 & 2 \\ 1 & 0 & 3 \end{bmatrix}$

1. 先找每一列的領頭數(最左邊的非 0 數),再檢查它們是不是一列比一列靠右。
2. (a) 領頭數是 $2$(第 1 行)、$1$(第 2 行)、$5/2$(第 4 行),一路往右,底下都是 0 → **是梯形**。但領頭數 $2$ 和 $5/2$ 不是 1 → **不是 RREF**。
3. (b) 領頭數都是 1,分別在第 1、2、3 行,而且各自所在的行其他位置都是 0 → **是 RREF**(當然也是梯形)。
4. (c) 第 1 列的領頭數在第 2 行,第 2 列的領頭數卻在第 1 行,**往左退了** → **不是梯形**。交換兩列就會是。

### 例 2
Row reduce $A = \begin{bmatrix} 1 & 2 & -1 & 3 \\ 2 & 4 & 1 & 0 \\ 3 & 6 & 2 & 1 \end{bmatrix}$ to echelon form, then to reduced echelon form, and identify the pivot columns.

1. **往前**:第 1 行不全為 0,用左上角的 1 當 pivot。$R_2 \leftarrow R_2 - 2R_1$、$R_3 \leftarrow R_3 - 3R_1$:
   $$\begin{bmatrix} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & -6 \\ 0 & 0 & 5 & -8 \end{bmatrix}$$
2. 蓋住第 1 列,看剩下的部分:第 2 行底下全是 0,**沒辦法當 pivot,跳過**,往右找到第 3 行。用 $3$ 當 pivot:$R_3 \leftarrow R_3 - \tfrac53 R_2$,第 3 列變成 $[\,0 \;\; 0 \;\; 0 \;\; 2\,]$。現在是梯形:
   $$\begin{bmatrix} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & -6 \\ 0 & 0 & 0 & 2 \end{bmatrix}$$
3. **往回**,從最下面開始:$R_3 \leftarrow \tfrac12 R_3$ 得 $[\,0 \;\; 0 \;\; 0 \;\; 1\,]$;用它消上方:$R_2 \leftarrow R_2 + 6R_3$、$R_1 \leftarrow R_1 - 3R_3$。
4. 第 2 列變成 $[\,0 \;\; 0 \;\; 3 \;\; 0\,]$,$R_2 \leftarrow \tfrac13 R_2$;再用它消上方:$R_1 \leftarrow R_1 + R_2$。得到 RREF:
   $$\begin{bmatrix} 1 & 2 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
5. pivot 位置在 $(1,1)$、$(2,3)$、$(3,4)$,所以 **pivot 行是第 1、3、4 行**。第 2 行不是 pivot 行——樓梯在那裡一次跨了兩格。

## 易錯點
在**原矩陣**上圈 pivot。pivot 位置要看化簡**之後**的梯形;原矩陣的左上角甚至可能是 0(這時要先換列)。

另一個常見錯:往前階段遇到「某一行底下全是 0」就卡住,或硬拿 0 當 pivot。正確做法是跳過這一行、往右找下一行。

## 教學提示
用「樓梯」比喻:每下一階至少往右一格,可以一次跨好幾格(像例 2 的第 2 行被跨過去)。學生最常卡在「某一行底下都是 0 時要跳過它」,例 2 就是專門示範這件事,請放慢速度做。

往前、往回兩個階段在黑板上分兩種顏色寫,學生比較記得住「先消下面、再消上面」的順序。

## 練習
### 照做
Is $\begin{bmatrix} 1 & 0 & 3 \\ 0 & 1 & -2 \\ 0 & 0 & 0 \end{bmatrix}$ in reduced echelon form? Which columns are pivot columns?

#### 解答
是 RREF:領頭數都是 1、一列比一列靠右、所在的行其他位置都是 0,全 0 列在最下面。pivot 行是**第 1、2 行**。

### 照做
Row reduce $\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}$ to reduced echelon form.

#### 解答
$R_2 \leftarrow R_2 - 4R_1$:$[\,0 \;\; {-3} \;\; {-6}\,]$;$R_2 \leftarrow -\tfrac13 R_2$:$[\,0 \;\; 1 \;\; 2\,]$;$R_1 \leftarrow R_1 - 2R_2$:$[\,1 \;\; 0 \;\; {-1}\,]$。

$$\text{RREF} = \begin{bmatrix} 1 & 0 & -1 \\ 0 & 1 & 2 \end{bmatrix}$$

### 變化
Row reduce $\begin{bmatrix} 1 & 3 & 5 & 7 \\ 3 & 5 & 7 & 9 \\ 5 & 7 & 9 & 1 \end{bmatrix}$ to reduced echelon form, and list the pivot columns.

#### 解答
往前:$R_2 \leftarrow R_2 - 3R_1$ 得 $[\,0 \;\; {-4} \;\; {-8} \;\; {-12}\,]$;$R_3 \leftarrow R_3 - 5R_1$ 得 $[\,0 \;\; {-8} \;\; {-16} \;\; {-34}\,]$;$R_3 \leftarrow R_3 - 2R_2$ 得 $[\,0 \;\; 0 \;\; 0 \;\; {-10}\,]$。

往回:$R_3 \leftarrow -\tfrac{1}{10}R_3$、$R_2 \leftarrow -\tfrac14 R_2$ 得 $[\,0 \;\; 1 \;\; 2 \;\; 3\,]$,再消掉第 4 行上方的數,最後 $R_1 \leftarrow R_1 - 3R_2$:

$$\text{RREF} = \begin{bmatrix} 1 & 0 & -1 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

pivot 行是**第 1、2、4 行**(第 3 行被跨過去)。

### 變化
Two students row reduce the same matrix using different sequences of row operations. Can their echelon forms be different? Can their reduced echelon forms be different? Can their pivot columns be different?

#### 解答
梯形**可能不同**(例如某一列多乘了一個倍數)。RREF **不可能不同**,因為每個矩陣的 RREF 唯一。pivot 行由 RREF 決定,所以也**一定相同**。

### 挑戰
Describe all possible echelon forms of a $2 \times 2$ matrix. Use $\blacksquare$ for a leading entry (nonzero) and $*$ for any value.

#### 解答
依 pivot 個數分四種:

$$\begin{bmatrix} \blacksquare & * \\ 0 & \blacksquare \end{bmatrix},\quad \begin{bmatrix} \blacksquare & * \\ 0 & 0 \end{bmatrix},\quad \begin{bmatrix} 0 & \blacksquare \\ 0 & 0 \end{bmatrix},\quad \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$$

兩個 pivot 一種、一個 pivot 兩種(pivot 在第 1 行或第 2 行)、零矩陣一種。

## 驗算
```check
Matrix([[1, 2, -1, 3], [2, 4, 1, 0], [3, 6, 2, 1]]).rref() == (Matrix([[1, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]), (0, 2, 3))
# 例 2 中間步驟
Matrix([[0, 0, 5, -8]]) - Rational(5, 3)*Matrix([[0, 0, 3, -6]]) == Matrix([[0, 0, 0, 2]])
Matrix([[1, 0, 3], [0, 1, -2], [0, 0, 0]]).rref() == (Matrix([[1, 0, 3], [0, 1, -2], [0, 0, 0]]), (0, 1))
Matrix([[1, 2, 3], [4, 5, 6]]).rref()[0] == Matrix([[1, 0, -1], [0, 1, 2]])
Matrix([[1, 3, 5, 7], [3, 5, 7, 9], [5, 7, 9, 1]]).rref() == (Matrix([[1, 0, -1, 0], [0, 1, 2, 0], [0, 0, 0, 1]]), (0, 1, 3))
Matrix([[5, 7, 9, 1]]) - 5*Matrix([[1, 3, 5, 7]]) - 2*Matrix([[0, -4, -8, -12]]) == Matrix([[0, 0, 0, -10]])
# 例 1(b) 已經是 RREF
Matrix([[1, 0, 0, 29], [0, 1, 0, 16], [0, 0, 1, 3]]).rref()[0] == Matrix([[1, 0, 0, 29], [0, 1, 0, 16], [0, 0, 1, 3]])
```
