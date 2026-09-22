---
title_en: Reading Solutions from the RREF
title_zh: 從 RREF 讀出解
sub: Two questions decide everything — is the last column a pivot column? any free variables?
level: mid
lab_hook: "`rref()` 回傳的 pivots:最後一行的索引在不在裡面?"
figure: decide.svg
figure_caption: 每一題都照這兩個問題的順序判斷。
---
## 觀念
In the RREF of an augmented matrix, the variables that correspond to pivot columns are **basic variables**; the other variables are **free variables**. Solving each nonzero row for its basic variable, in terms of the free variables, gives the **general solution**.

**Existence and Uniqueness Theorem.** A linear system is consistent if and only if the rightmost column of the augmented matrix is *not* a pivot column — that is, no row has the form $[\,0 \;\cdots\; 0 \mid b\,]$ with $b \neq 0$. If the system is consistent, it has a unique solution when there are no free variables, and infinitely many solutions when there is at least one free variable.

## 白話說
化成 RREF 之後,解就寫在臉上。照順序問兩個問題:

1. **最後一行(常數那一行)有沒有 pivot?** 有的話代表出現了「$0 = $ 非零數」這種列,**無解**,直接收工。
2. **有沒有自由變數?** pivot 行對應的變數叫**基本變數**,其他的叫**自由變數**。自由變數可以任意取值,基本變數再跟著算出來。沒有自由變數 → **唯一解**;有任何一個 → **無限多解**。

一般解的寫法:把每個基本變數寫成「常數 + 自由變數的組合」,自由變數旁邊註明 is free。

## 在資工哪裡用
程式解方程組時,要先判斷是哪一種情況,再決定怎麼回報。未知數比方程式多的時候(例如模型的參數比資料點多),一定會有自由變數——這正是機器學習裡「參數太多、答案不唯一」的根源,第 14 週會再遇到。

## 原理
**證明存在與唯一性定理**(看 RREF 就夠了,因為列運算不改變解集)。

- **最後一行是 pivot 行**:那一列長得像 $[\,0 \;\cdots\; 0 \mid 1\,]$,代表方程式 $0x_1 + \cdots + 0x_n = 1$,也就是 $0 = 1$,沒有任何解。
- **最後一行不是 pivot 行**:每一個非零列都恰好有一個基本變數,而且它可以寫成「常數 + 自由變數的組合」。自由變數隨便給值(例如全給 0),基本變數就跟著確定,所以**至少有一個解**。
- 有解時,若**沒有自由變數**,每個變數都被直接決定,解唯一;若**有自由變數**,它的每一個取值都對應一個不同的解,所以有無限多解。

**pivot 個數的上限**:每一列最多一個 pivot,每一行也最多一個 pivot。所以 pivot 個數 $\le$ 列數,也 $\le$ 行數。這個觀察是「方程式比未知數少 → 一定有自由變數」的根據(見挑戰題)。

## 老師講解
### 例 1
Find the general solution of the system whose augmented matrix has been reduced to $\left[\begin{array}{rrr|r} 1 & 0 & -5 & 1 \\ 0 & 1 & 1 & 4 \\ 0 & 0 & 0 & 0 \end{array}\right]$.

1. **最後一行有沒有 pivot?** 沒有(第 3 列全是 0,代表 $0 = 0$,永遠成立,不是矛盾)。所以**有解**。
2. **找基本變數與自由變數**:pivot 在第 1、2 行,所以 $x_1$、$x_2$ 是基本變數;第 3 行沒有 pivot,$x_3$ 是**自由變數**。有自由變數 → **無限多解**。
3. 把每一個非零列寫回方程式:$x_1 - 5x_3 = 1$、$x_2 + x_3 = 4$。
4. 把基本變數移到左邊單獨放,其他全部移到右邊,得到一般解:
   $$x_1 = 1 + 5x_3,\qquad x_2 = 4 - x_3,\qquad x_3 \text{ is free.}$$
5. 驗證一個特例:取 $x_3 = 0$ 得 $(1, 4, 0)$;取 $x_3 = 1$ 得 $(6, 3, 1)$。代回原來兩條方程式都成立 ✓。

### 例 2
Each matrix is the RREF of an augmented matrix. Decide whether the system has no solution, exactly one, or infinitely many.
(a) $\left[\begin{array}{rrr|r} 1 & 0 & 2 & 3 \\ 0 & 1 & -1 & 1 \\ 0 & 0 & 0 & 4 \end{array}\right]$  (b) $\left[\begin{array}{rrr|r} 1 & 0 & 0 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 5 \end{array}\right]$  (c) $\left[\begin{array}{rrr|r} 1 & 3 & 0 & 2 \\ 0 & 0 & 1 & -4 \end{array}\right]$

1. (a) 第 3 列是 $[\,0 \;\; 0 \;\; 0 \mid 4\,]$,也就是 $0 = 4$。最後一行有 pivot → **無解**,不用再往下看。
2. (b) 最後一行沒有 pivot → 有解。三個變數各有 pivot,**沒有自由變數** → **唯一解** $(2, -1, 5)$。
3. (c) 最後一行沒有 pivot → 有解。pivot 在第 1、3 行,$x_2$ 沒有 pivot,是**自由變數** → **無限多解**:$x_1 = 2 - 3x_2$,$x_3 = -4$,$x_2$ is free。

## 易錯點
把全 0 列 $[\,0 \;\; 0 \;\; 0 \mid 0\,]$ 誤當成無解。$0 = 0$ 永遠成立,只是這條方程式沒提供資訊;真正的無解是 $[\,0 \;\cdots\; 0 \mid b\,]$ 而且 $b \neq 0$。

另一個常見錯:以為「有自由變數代表題目算錯了」。自由變數是很正常的結果,表示解有無限多個。

## 教學提示
把觀念的流程圖畫在黑板角落,整堂課都不要擦。每一題都照流程問兩句:「最後一行有沒有 pivot?」「有沒有自由變數?」數理弱的學生需要**固定的判斷順序**,而不是每一題重新想。

一般解寫完,一定要讓學生隨便代一個自由變數的值回去驗算。這會讓「自由變數真的可以隨便選」變得具體。

## 練習
### 照做
Find the general solution of the system whose augmented matrix has been reduced to $\left[\begin{array}{rrr|r} 1 & 0 & 2 & 5 \\ 0 & 1 & -3 & -1 \end{array}\right]$.

#### 解答
最後一行沒有 pivot → 有解。$x_3$ 是自由變數 → 無限多解:

$$x_1 = 5 - 2x_3,\qquad x_2 = -1 + 3x_3,\qquad x_3 \text{ is free.}$$

### 照做
Is the system with augmented matrix $\left[\begin{array}{rrr|r} 1 & 2 & 0 & 1 \\ 0 & 0 & 1 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right]$ consistent? If so, how many solutions does it have?

#### 解答
最後一行沒有 pivot → **有解**。pivot 在第 1、3 行,$x_2$ 是自由變數 → **無限多解**:$x_1 = 1 - 2x_2$,$x_3 = 3$,$x_2$ is free。

### 變化
Row reduce the augmented matrix and find the general solution of $x_1 + 3x_2 + 4x_3 = 7,\;\; 3x_1 + 9x_2 + 7x_3 = 6$.

#### 解答
$$\left[\begin{array}{rrr|r} 1 & 3 & 4 & 7 \\ 3 & 9 & 7 & 6 \end{array}\right] \xrightarrow{R_2 - 3R_1} \left[\begin{array}{rrr|r} 1 & 3 & 4 & 7 \\ 0 & 0 & -5 & -15 \end{array}\right]$$

$R_2 \leftarrow -\tfrac15 R_2$ 得 $x_3 = 3$;$R_1 \leftarrow R_1 - 4R_2$ 得 $[\,1 \;\; 3 \;\; 0 \mid {-5}\,]$。pivot 在第 1、3 行,$x_2$ 自由:

$$x_1 = -5 - 3x_2,\qquad x_2 \text{ is free},\qquad x_3 = 3.$$

### 變化
For what value of $h$ is the system with augmented matrix $\left[\begin{array}{rr|r} 1 & -3 & h \\ -2 & 6 & -5 \end{array}\right]$ consistent?

#### 解答
$R_2 \leftarrow R_2 + 2R_1$:第 2 列變成 $[\,0 \;\; 0 \mid 2h - 5\,]$。要有解,這一列不能是 $0 = $ 非零數,所以 $2h - 5 = 0$,$h = \tfrac52$。

### 挑戰
A system has 3 equations and 5 unknowns. Can it have a unique solution? Explain using pivots.

#### 解答
不可能。每一列最多一個 pivot,所以係數部分最多 3 個 pivot;但有 5 個變數,至少有 $5 - 3 = 2$ 個自由變數。如果有解,就一定是**無限多解**;也可能無解。無論如何都不會唯一。

## 驗算
```check
# 例 1 一般解代回兩條方程式,對任意 t 都成立
simplify(Matrix([[1, 0, -5], [0, 1, 1]]) * Matrix([1 + 5*t, 4 - t, t]) - Matrix([1, 4])) == zeros(2, 1)
Matrix([[1, 0, 2, 3], [0, 1, -1, 1], [0, 0, 0, 4]]).rref()[1] == (0, 1, 3)
Matrix([[1, 0, 2, 5], [0, 1, -3, -1]]) * Matrix([5 - 2*t, -1 + 3*t, t, -1]) == zeros(2, 1)
Matrix([[1, 2, 0, 1], [0, 0, 1, 3]]) * Matrix([1 - 2*t, t, 3, -1]) == zeros(2, 1)
Matrix([[1, 3, 4, 7], [3, 9, 7, 6]]).rref() == (Matrix([[1, 3, 0, -5], [0, 0, 1, 3]]), (0, 2))
simplify(Matrix([[1, 3, 4], [3, 9, 7]]) * Matrix([-5 - 3*t, t, 3]) - Matrix([7, 6])) == zeros(2, 1)
Matrix([[1, -3, h], [-2, 6, -5]]).echelon_form()[1, 2] == 2*h - 5
solve(2*h - 5, h) == [Rational(5, 2)]
```
