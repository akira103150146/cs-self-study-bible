---
title_en: Linear Systems and Their Solution Sets
title_zh: 線性方程組與解的三種情況
sub: No solution, exactly one, or infinitely many — nothing else
level: basic
lab_hook: "`np.linalg.solve(A, b)`(只在唯一解時能用)"
figure: three-cases.svg
figure_caption: 兩個未知數時,每條方程式是一條直線;解就是兩條線的共同點。
---
## 觀念
A **linear equation** in $x_1, \dots, x_n$ has the form $a_1x_1 + a_2x_2 + \cdots + a_nx_n = b$: each variable appears only to the first power, and variables are never multiplied together. A **linear system** is a collection of such equations, and its **solution set** is every list $(x_1, \dots, x_n)$ that satisfies *all* of them at once. A system is **consistent** if it has at least one solution and **inconsistent** if it has none.

Every linear system has **no solution, exactly one solution, or infinitely many solutions**.

## 白話說
線性方程式就是「每個未知數只出現一次方、未知數之間不互乘」的等式。一組方程式要**同時**成立,解就是讓每一條都成立的那些數。

兩個未知數的時候,每條方程式在平面上是一條直線,解就是所有直線的共同點。兩條直線只有三種關係:相交在一點(唯一解)、平行不相交(無解)、完全重合(無限多解)。**不可能剛好兩個解**——兩條直線只要有兩個共同點,就是同一條線。

有解叫 consistent(一致),無解叫 inconsistent(不一致)。

## 在資工哪裡用
遊戲判斷子彈有沒有打中牆、圖學算光線和平面的交點,都是在解方程組。程式遇到「無解」或「無限多解」時要能分辨並回報,而不是算出一個錯的數字或直接當掉。

## 原理
**為什麼只有三種情況?** 關鍵是:只要有兩個不同的解,就一定有無限多個。

設 $\mathbf{p}$、$\mathbf{q}$ 都是解,也就是每一條方程式 $a_1x_1 + \cdots + a_nx_n = b$ 代入 $\mathbf{p}$ 和 $\mathbf{q}$ 都成立。對任意實數 $t$,考慮 $\mathbf{r} = \mathbf{p} + t(\mathbf{q} - \mathbf{p})$。把 $\mathbf{r}$ 代入同一條方程式,左邊是

$$(\text{代入 } \mathbf{p} \text{ 的值}) + t\big[(\text{代入 } \mathbf{q}) - (\text{代入 } \mathbf{p})\big] = b + t(b - b) = b.$$

所以每一個 $t$ 都給出一個解,$t$ 有無限多個,解就有無限多個。這個論證只用到「方程式是線性的」,和未知數的個數無關。

幾何上,$\mathbf{p} + t(\mathbf{q} - \mathbf{p})$ 正是通過 $\mathbf{p}$、$\mathbf{q}$ 的那條直線——兩個解之間連線上的每一點都是解。

## 老師講解
### 例 1
Decide whether each equation is linear: (a) $3x_1 - 2x_2 = 7$  (b) $x_1x_2 + x_3 = 4$  (c) $2x_1 + \sqrt{5}\,x_2 = 1$  (d) $x_1^2 - x_2 = 0$.

1. 判斷準則只看**未知數**:有沒有次方、有沒有互乘、有沒有被放進根號或函數裡。係數是什麼數都沒關係。
2. (a) 每個未知數都是一次方,沒有互乘 → **是**線性方程式。
3. (b) 出現 $x_1x_2$,兩個未知數相乘 → **不是**。
4. (c) $\sqrt{5}$ 是係數(一個固定的數,約 2.236),開根號的不是未知數 → **是**。
5. (d) 出現 $x_1^2$,未知數有平方 → **不是**。

### 例 2
Solve each system and describe it geometrically.
(a) $x_1 - 2x_2 = -1,\;\; -x_1 + 3x_2 = 3$  (b) $x_1 - 2x_2 = -1,\;\; -x_1 + 2x_2 = 3$

1. (a) 兩式相加,$x_1$ 被消掉:$(x_1 - x_1) + (-2x_2 + 3x_2) = -1 + 3$,得 $x_2 = 2$。
2. 把 $x_2 = 2$ 代回第一式:$x_1 - 4 = -1$,得 $x_1 = 3$。
3. 驗算第二式:$-3 + 3 \cdot 2 = 3$ ✓。解是 $(3, 2)$,**唯一解**:兩條直線相交在點 $(3, 2)$。
4. (b) 同樣兩式相加:$(x_1 - x_1) + (-2x_2 + 2x_2) = -1 + 3$,左邊全部消光,得 $0 = 2$。
5. $0 = 2$ 永遠不成立,所以沒有任何 $(x_1, x_2)$ 能同時滿足兩式——**無解**。兩條線斜率相同但截距不同,是平行線。

## 易錯點
看到 $\sqrt{5}\,x_2$ 就說不是線性。開根號的是係數 5,不是未知數。判斷時只看未知數:有沒有次方、有沒有互乘、有沒有被放進函數裡。

另一個常見錯:算到 $0 = 2$ 以為自己算錯、回頭重算。$0 = $ 非零數正是「無解」的訊號,要能認出來。

## 教學提示
先畫圖再算。每一題解完都追問一句:「這在圖上是哪一種?」讓三種情況變成反射。數理弱的學生對「兩條線」的圖像比對符號有感,圖一定要畫在黑板上,不要只指講義。

「不可能剛好兩個解」用反問帶:「兩條直線有兩個共同點,會是什麼情況?」讓學生自己說出「那就是同一條線」。

## 練習
### 照做
Solve the system $x_1 + x_2 = 5,\;\; x_1 - x_2 = 1$ and state how many solutions it has.

#### 解答
兩式相加:$2x_1 = 6$,$x_1 = 3$;代回得 $x_2 = 2$。解是 $(3, 2)$,**唯一解**(兩線相交於一點)。

### 照做
Is $4x_1 - 5x_2 + 2 = x_1$ a linear equation? If so, rewrite it in the form $a_1x_1 + a_2x_2 = b$.

#### 解答
是。未知數都是一次方、沒有互乘。移項:$4x_1 - x_1 - 5x_2 = -2$,即 $3x_1 - 5x_2 = -2$。

### 變化
Without solving completely, decide whether the system $2x_1 + 4x_2 = 6,\;\; x_1 + 2x_2 = 3$ has no solution, exactly one, or infinitely many.

#### 解答
第一式正好是第二式的 2 倍,兩條方程式描述**同一條直線**,所以有**無限多解**(例如 $(3, 0)$、$(1, 1)$、$(-1, 2)$ 都是)。

### 變化
Find the value of $h$ for which the system $x_1 + hx_2 = 4,\;\; 3x_1 + 6x_2 = 8$ has no solution.

#### 解答
第二式減去第一式的 3 倍:$(6 - 3h)x_2 = 8 - 12 = -4$。

當 $6 - 3h = 0$,也就是 $h = 2$ 時,這一式變成 $0 = -4$,矛盾,**無解**。(此時兩條線斜率相同、截距不同,是平行線。)

### 挑戰
Can a system of two linear equations in two variables have exactly two solutions? Explain using the picture of two lines.

#### 解答
不可能。如果有兩個不同的解,兩條直線就同時通過這兩個點;但通過兩個不同點的直線只有一條,所以兩條方程式其實是同一條線,解會有**無限多個**。(一般情形見原理:兩個解之間連線上的每一點都是解。)

## 驗算
```check
# 例 2(a) 唯一解 (3, 2);例 2(b) 最後一行是 pivot → 無解
Matrix([[1, -2, -1], [-1, 3, 3]]).rref()[0] == Matrix([[1, 0, 3], [0, 1, 2]])
Matrix([[1, -2, -1], [-1, 2, 3]]).rref()[1] == (0, 2)
Matrix([[1, 1, 5], [1, -1, 1]]).rref()[0] == Matrix([[1, 0, 3], [0, 1, 2]])
expand(4*x1 - 5*x2 + 2 - x1) == 3*x1 - 5*x2 + 2
Matrix([[2, 4, 6], [1, 2, 3]]).rank() == 1
Matrix([[1, h, 4], [3, 6, 8]]).echelon_form()[1, :] == Matrix([[0, 6 - 3*h, -4]])
solve(6 - 3*h, h) == [2]
```
