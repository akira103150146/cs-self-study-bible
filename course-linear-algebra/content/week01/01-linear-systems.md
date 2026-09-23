---
title_en: Systems of Linear Equations
title_zh: 線性方程組與解集
sub: No solution, exactly one, or infinitely many — nothing else
level: basic
source: Lay 1.1
lab_hook: "`np.linalg.solve(A, b)`(只在唯一解時能用)"
---
## 觀念
A **linear equation** in the variables $x_1, \dots, x_n$ is an equation that can be written in the form

$$a_1x_1 + a_2x_2 + \cdots + a_nx_n = b$$

where $b$ and the **coefficients** $a_1, \dots, a_n$ are real or complex numbers, usually known in advance.

A **system of linear equations** (or a **linear system**) is a collection of one or more linear equations involving the same variables. A **solution** of the system is a list $(s_1, s_2, \dots, s_n)$ of numbers that makes each equation a true statement when the values $s_1, \dots, s_n$ are substituted for $x_1, \dots, x_n$. The set of all possible solutions is called the **solution set**. Two linear systems are **equivalent** if they have the same solution set.

A system of linear equations has

1. no solution, or
2. exactly one solution, or
3. infinitely many solutions.

A system is **consistent** if it has either one solution or infinitely many solutions; it is **inconsistent** if it has no solution.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| linear equation | 線性方程式 | 每個未知數都是一次方、未知數之間不相乘 |
| coefficient | 係數 | 未知數前面乘的那個數,例如 $3x_1$ 的 3 |
| system of linear equations / linear system | 線性方程組 | 一組共用同一批未知數的線性方程式 |
| solution | 解 | 一組數 $(s_1, \dots, s_n)$,代進去**每一條**都成立 |
| solution set | 解集 | **所有**解收集起來的集合(可能是空集合) |
| equivalent systems | 等價的方程組 | 兩個方程組的解集完全相同 |
| consistent | 相容(有解) | 至少有一個解;也有書譯作「一致」 |
| inconsistent | 不相容(無解) | 一個解都沒有 |

## 白話說
**線性方程式**就是「每個未知數只出現一次方、未知數之間不互乘、也沒有被放進根號或函數裡」的等式。係數可以是任何數,包括 $\sqrt{6}$ 這種看起來很複雜的數。

一組方程式要**同時**成立,**解**就是讓每一條都成立的那一組數。「解」是一組數(例如 $(3, 2)$),「解集」是所有解放在一起的集合——這兩個詞課本分得很清楚,是非題常常考。

整門課最重要的一個事實:**方程組的解只有三種情況——無解、剛好一個、無限多個**。不會剛好兩個,也不會剛好一百個。

## 幾何意義
兩個未知數時,每條方程式在平面上是一條**直線**;一組數 $(x_1, x_2)$ 同時滿足兩條方程式,等於這個點同時落在兩條線上。所以「解方程組」就是「找兩條線的交點」:

![兩條直線只有三種關係:相交於一點、平行、重合。](three-cases.svg)

- 相交於一點 → 唯一解
- 平行不相交 → 無解
- 完全重合 → 無限多解(線上每一點都是解)

三個未知數時,每條方程式是空間中的一個**平面**。三個平面可能交於一點(唯一解)、交於一條線(無限多解),或沒有共同點(無解)。課本 p. 30、p. 32 有立體圖可以對照。

## 在資工哪裡用
遊戲判斷子彈有沒有打中牆、圖學算光線和平面的交點,都是在解方程組;路線規劃、電路模擬、機器學習的模型訓練,背後也是成千上萬條方程式。程式遇到「無解」或「無限多解」時要能分辨並回報,而不是算出一個錯的數字或直接當掉。

## 原理
**為什麼只有三種情況?** 關鍵是:只要有兩個不同的解,就一定有無限多個。

設 $\mathbf{p} = (p_1, \dots, p_n)$、$\mathbf{q} = (q_1, \dots, q_n)$ 都是解。對任意實數 $t$,考慮 $\mathbf{r} = \mathbf{p} + t(\mathbf{q} - \mathbf{p})$,也就是 $r_i = p_i + t(q_i - p_i)$。把 $\mathbf{r}$ 代入任何一條方程式 $a_1x_1 + \cdots + a_nx_n = b$:

$$\sum a_i r_i = \sum a_i p_i + t\Big(\sum a_i q_i - \sum a_i p_i\Big) = b + t(b - b) = b.$$

所以每一個 $t$ 都給出一個解,$t$ 有無限多個,解就有無限多個。這個論證只用到「方程式是線性的」,和未知數的個數無關。幾何上,$\mathbf{p} + t(\mathbf{q} - \mathbf{p})$ 就是通過 $\mathbf{p}$、$\mathbf{q}$ 的直線——兩個解之間的連線上每一點都是解。

課本把這個事實留到 1.2 用 pivot 證明(Theorem 2);這裡的論證比較直接,可以當課堂上的補充。

## 老師講解
### 例 1 · Lay 1.1(p. 26)
The equations $4x_1 - 5x_2 + 2 = x_1$ and $x_2 = 2(\sqrt{6} - x_1) + x_3$ are both linear, while $4x_1 - 5x_2 = x_1x_2$ and $x_2 = 2\sqrt{x_1} - 6$ are not. Explain why, and rewrite the linear ones in the form $a_1x_1 + \cdots + a_nx_n = b$.

1. **判斷準則只看未知數**:未知數有沒有次方、有沒有互乘、有沒有被放進根號或函數裡。係數是什麼數都沒關係。
2. $4x_1 - 5x_2 + 2 = x_1$:每個未知數都是一次方 → **線性**。把 $x_1$ 移到左邊、常數 2 移到右邊:$4x_1 - x_1 - 5x_2 = -2$,整理成 $3x_1 - 5x_2 = -2$。
3. $x_2 = 2(\sqrt{6} - x_1) + x_3$:先展開,$x_2 = 2\sqrt{6} - 2x_1 + x_3$。$\sqrt{6}$ 只是一個**固定的數**(約 2.449),不是未知數開根號 → **線性**。把未知數都移到左邊:$2x_1 + x_2 - x_3 = 2\sqrt{6}$。
4. $4x_1 - 5x_2 = x_1x_2$:右邊 $x_1x_2$ 是兩個未知數相乘 → **不是線性**。
5. $x_2 = 2\sqrt{x_1} - 6$:$\sqrt{x_1}$ 是對**未知數**開根號 → **不是線性**。
6. 結論:判斷時先把式子整理好,再逐項看未知數的樣子;$\sqrt{6}$ 和 $\sqrt{x_1}$ 看起來很像,意義完全不同。

### 例 2 · Lay 1.1(p. 27)
Verify that $(5, 6.5, 3)$ is a solution of the system $2x_1 - x_2 + 1.5x_3 = 8,\;\; x_1 - 4x_3 = -7$.

1. 「是不是解」只要**代入檢查**:把 $x_1 = 5$、$x_2 = 6.5$、$x_3 = 3$ 代進**每一條**方程式。
2. 第一條:$2(5) - 6.5 + 1.5(3) = 10 - 6.5 + 4.5 = 8$,等於右邊的 8 ✓。
3. 第二條:這條沒有 $x_2$(係數是 0),所以 $5 - 4(3) = 5 - 12 = -7$,等於右邊的 $-7$ ✓。
4. 兩條都成立,所以 $(5, 6.5, 3)$ 是一個解。注意:這只說明它是**一個**解,不代表它是唯一的解——這個方程組其實有無限多解(兩條方程式、三個未知數,之後的觀念會解釋)。

### 例 3 · Lay 1.1(p. 27,Figures 1–2)
Solve each system and describe its graph. (a) $x_1 - 2x_2 = -1,\;\; -x_1 + 3x_2 = 3$ [Figure 1]  (b) $x_1 - 2x_2 = -1,\;\; -x_1 + 2x_2 = 3$ [Figure 2(a)]  (c) $x_1 - 2x_2 = -1,\;\; -x_1 + 2x_2 = 1$ [Figure 2(b)]

1. (a) 兩式相加,$x_1$ 被消掉:$(x_1 - x_1) + (-2x_2 + 3x_2) = -1 + 3$,得 $x_2 = 2$。
2. 把 $x_2 = 2$ 代回第一式:$x_1 - 4 = -1$,得 $x_1 = 3$。驗算第二式:$-3 + 3 \cdot 2 = 3$ ✓。**唯一解** $(3, 2)$:兩條直線相交在點 $(3, 2)$(課本 Figure 1)。
3. (b) 同樣兩式相加:$(x_1 - x_1) + (-2x_2 + 2x_2) = -1 + 3$,左邊全部消光,得 $0 = 2$。
4. $0 = 2$ 永遠不成立,所以沒有任何 $(x_1, x_2)$ 能同時滿足兩式——**無解**(不相容)。把兩式都改寫成 $x_2 = \frac12 x_1 + \cdots$ 的形式會看到:斜率都是 $\frac12$,截距不同,是兩條平行線(課本 Figure 2(a))。
5. (c) 兩式相加:$0 = 0$,永遠成立。這表示第二式其實就是第一式乘以 $-1$,兩條方程式描述**同一條直線**。
6. 所以 (c) 的解就是這條線上的每一個點,**無限多解**(課本 Figure 2(b))。例如 $(-1, 0)$、$(1, 1)$、$(3, 2)$ 都是解。
7. 三小題合起來就是課本方框裡的事實:解只有「無解、唯一、無限多」三種。

## 易錯點
- 看到 $\sqrt{6}$ 就說不是線性。開根號的是**係數**,不是未知數。
- 把「解」和「解集」混為一談:解是一組數,解集是所有解的集合。Lay 1.1 的是非題 31 就是考這個。
- 算到 $0 = 2$ 以為自己算錯、回頭重算。$0 = $ 非零數正是「無解」的訊號。
- 驗算只代一條方程式。解必須讓**每一條**都成立(見 Practice Problem 3:$(3, 4, -2)$ 滿足前兩條,卻不滿足第三條)。

## 教學提示
先畫圖再算。例 3 的三小題一定要在黑板上畫出三張圖,每解完一題就問「這在圖上是哪一種?」。數理弱的學生對「兩條線」的圖像比對符號有感。

「不可能剛好兩個解」用反問帶:「兩條直線有兩個共同點,會是什麼情況?」讓學生自己說出「那就是同一條線」。有時間再用原理區塊的 $\mathbf{p} + t(\mathbf{q} - \mathbf{p})$ 講一般情形。

課堂建議做:Exercises 3–4、Practice Problem 3;是非題 31、32;其餘當作業。

## 練習
### 照做 · Lay 1.1 Exercise 3
Find the point $(x_1, x_2)$ that lies on the line $x_1 + 5x_2 = 7$ and on the line $x_1 - 2x_2 = -2$.

#### 解答
兩式相減(第一式減第二式):$7x_2 = 9$,$x_2 = \frac97$。代回第二式:$x_1 = -2 + 2 \cdot \frac97 = \frac47$。所求的點是 $\left(\frac47, \frac97\right)$(書後解答相同)。

驗算第一式:$\frac47 + 5 \cdot \frac97 = \frac{4 + 45}{7} = 7$ ✓。

#### 備註
建議課堂做。答案是分數,正好練習「答案不漂亮也不代表算錯」,重點是驗算。

### 照做 · Lay 1.1 Exercise 4
Find the point of intersection of the lines $x_1 - 5x_2 = 1$ and $3x_1 - 7x_2 = 5$.

#### 解答
第二式減去第一式的 3 倍:$(-7 + 15)x_2 = 5 - 3$,即 $8x_2 = 2$,$x_2 = \frac14$。代回第一式:$x_1 = 1 + \frac54 = \frac94$。交點是 $\left(\frac94, \frac14\right)$。

驗算第二式:$3 \cdot \frac94 - 7 \cdot \frac14 = \frac{27 - 7}{4} = 5$ ✓。

### 照做 · Lay 1.1 Practice Problem 3
Is $(3, 4, -2)$ a solution of the following system?

$$\begin{aligned} 5x_1 - x_2 + 2x_3 &= 7 \\ -2x_1 + 6x_2 + 9x_3 &= 0 \\ -7x_1 + 5x_2 - 3x_3 &= -7 \end{aligned}$$

#### 解答
逐條代入(負數記得加括號):

- $5(3) - (4) + 2(-2) = 15 - 4 - 4 = 7$ ✓
- $-2(3) + 6(4) + 9(-2) = -6 + 24 - 18 = 0$ ✓
- $-7(3) + 5(4) - 3(-2) = -21 + 20 + 6 = 5 \neq -7$ ✗

第三條不成立,所以 $(3, 4, -2)$ **不是**解。幾何上,這個點落在前兩個平面的交線上,卻不在第三個平面上(課本 p. 37 的圖)。

#### 備註
建議課堂做。重點是「每一條都要代」,很多學生代完前兩條就收工。

### 是非 · Lay 1.1 Exercise 31
**(T/F)** The solution set of a linear system involving variables $x_1, \dots, x_n$ is a list of numbers $(s_1, \dots, s_n)$ that makes each equation in the system a true statement when the values $s_1, \dots, s_n$ are substituted for $x_1, \dots, x_n$, respectively.

#### 解答
**False.** 這句話描述的是**一個解**(a solution)的定義,不是解集。解集是「所有可能的解」組成的集合(課本 p. 27)。

### 是非 · Lay 1.1 Exercise 32
**(T/F)** An inconsistent system has more than one solution.

#### 解答
**False.** Inconsistent(不相容)的定義就是**沒有解**(課本 p. 28)。

### 是非 · Lay 1.1 Exercise 34
**(T/F)** Two linear systems are equivalent if they have the same solution set.

#### 解答
**True.** 這正是等價方程組的定義(課本 p. 27)。

### 變化 · Lay 1.1 Exercise 21
Do the three lines $x_1 - 4x_2 = 1$, $2x_1 - x_2 = -3$, and $-x_1 - 3x_2 = 4$ have a common point of intersection? Explain.

#### 解答
先用前兩條找交點:第一式得 $x_1 = 1 + 4x_2$,代入第二式:$2 + 8x_2 - x_2 = -3$,$x_2 = -\frac57$,$x_1 = 1 - \frac{20}{7} = -\frac{13}{7}$。

再檢查這個點在不在第三條線上:$-\left(-\frac{13}{7}\right) - 3\left(-\frac57\right) = \frac{13 + 15}{7} = 4$ ✓。

所以**有**,三條線交於同一點 $\left(-\frac{13}{7}, -\frac57\right)$(書後解答:the three lines have one point in common)。

#### 備註
三條方程式、兩個未知數(方程式比未知數多)通常無解,這題剛好有解,可以順便預告第 14 週的「超定系統」。

### 變化 · Lay 1.1 Exercise 22
Do the three planes $x_1 + 2x_2 + x_3 = 4$, $x_2 - x_3 = 1$, and $x_1 + 3x_2 = 0$ have at least one common point of intersection? Explain.

#### 解答
寫成增廣矩陣並化簡:

$$\left[\begin{array}{rrr|r} 1 & 2 & 1 & 4 \\ 0 & 1 & -1 & 1 \\ 1 & 3 & 0 & 0 \end{array}\right] \xrightarrow{R_3 - R_1} \left[\begin{array}{rrr|r} 1 & 2 & 1 & 4 \\ 0 & 1 & -1 & 1 \\ 0 & 1 & -1 & -4 \end{array}\right] \xrightarrow{R_3 - R_2} \left[\begin{array}{rrr|r} 1 & 2 & 1 & 4 \\ 0 & 1 & -1 & 1 \\ 0 & 0 & 0 & -5 \end{array}\right]$$

最後一列代表 $0 = -5$,矛盾。所以**沒有**共同點——三個平面沒有同時交於任何一點。

#### 備註
這題用到觀念 2 的列運算,可以留到觀念 2 之後再做。

### 挑戰 · 補充
Can a system of two linear equations in two variables have exactly two solutions? Explain using the picture of two lines.

#### 解答
不可能。如果有兩個不同的解,兩條直線就同時通過這兩個點;但通過兩個不同點的直線只有一條,所以兩條方程式其實是同一條線,解會有**無限多個**。(一般情形見原理:兩個解之間連線上的每一點都是解。)

#### 備註
非課本原題。適合當下課前的討論題。

## 驗算
```check
expand(4*x1 - 5*x2 + 2 - x1) == 3*x1 - 5*x2 + 2
expand(x2 - (2*(sqrt(6) - x1) + x3)) == expand(2*x1 + x2 - x3 - 2*sqrt(6))
[2*5 - Rational(13, 2) + Rational(3, 2)*3, 5 - 4*3] == [8, -7]
Matrix([[1, -2, -1], [-1, 3, 3]]).rref()[0] == Matrix([[1, 0, 3], [0, 1, 2]])
Matrix([[1, -2, -1], [-1, 2, 3]]).rref()[1] == (0, 2)
Matrix([[1, -2, -1], [-1, 2, 1]]).rank() == 1
Matrix([[1, 5, 7], [1, -2, -2]]).rref()[0] == Matrix([[1, 0, Rational(4, 7)], [0, 1, Rational(9, 7)]])
Matrix([[1, -5, 1], [3, -7, 5]]).rref()[0] == Matrix([[1, 0, Rational(9, 4)], [0, 1, Rational(1, 4)]])
[5*3 - 4 + 2*(-2), -2*3 + 6*4 + 9*(-2), -7*3 + 5*4 - 3*(-2)] == [7, 0, 5]
Matrix([[1, -4, 1], [2, -1, -3], [-1, -3, 4]]).rref()[0] == Matrix([[1, 0, Rational(-13, 7)], [0, 1, Rational(-5, 7)], [0, 0, 0]])
Matrix([[1, 2, 1, 4], [0, 1, -1, 1], [1, 3, 0, 0]]).rref()[1] == (0, 1, 3)
```
