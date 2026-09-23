---
title_en: Parametric Vector Form and Nonhomogeneous Systems
title_zh: 參數向量形式:Ax = b 的解 = 特解 + 齊次解
sub: The solution set of Ax = b is the solution set of Ax = 0, shifted by p
level: mid
source: Lay 1.5
lab_hook: '`A.gauss_jordan_solve(b)`:SymPy 直接回傳「特解 + 參數 × 方向」形式的一般解'
---
## 觀念
The original equation $10x_1 - 3x_2 - 2x_3 = 0$ for the plane in Example 2 of the previous concept is an *implicit* description of the plane. Solving this equation amounts to finding an *explicit* description of the plane as the set spanned by $\mathbf{u}$ and $\mathbf{v}$. The equation $\mathbf{x} = x_2\mathbf{u} + x_3\mathbf{v}$ is called a **parametric vector equation** of the plane. Sometimes such an equation is written as

$$\mathbf{x} = s\mathbf{u} + t\mathbf{v} \quad (s, t \text{ in } \mathbb{R})$$

to emphasize that the parameters vary over all real numbers. Whenever a solution set is described explicitly with vectors, we say that the solution is in **parametric vector form**.

When a nonhomogeneous linear system has many solutions, the general solution can be written in parametric vector form as one vector plus an arbitrary linear combination of vectors that satisfy the corresponding homogeneous system.

**Theorem 6.** Suppose the equation $A\mathbf{x} = \mathbf{b}$ is consistent for some given $\mathbf{b}$, and let $\mathbf{p}$ be a solution. Then the solution set of $A\mathbf{x} = \mathbf{b}$ is the set of all vectors of the form $\mathbf{w} = \mathbf{p} + \mathbf{v}_h$, where $\mathbf{v}_h$ is any solution of the homogeneous equation $A\mathbf{x} = \mathbf{0}$.

*Warning:* Theorem 6 applies only to an equation $A\mathbf{x} = \mathbf{b}$ that has at least one nonzero solution $\mathbf{p}$. When $A\mathbf{x} = \mathbf{b}$ has no solution, the solution set is empty.

**Writing a solution set (of a consistent system) in parametric vector form**

1. Row reduce the augmented matrix to reduced echelon form.
2. Express each basic variable in terms of any free variables appearing in an equation.
3. Write a typical solution $\mathbf{x}$ as a vector whose entries depend on the free variables, if any.
4. Decompose $\mathbf{x}$ into a linear combination of vectors (with numeric entries) using the free variables as parameters.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| implicit description | 隱式描述 | 用方程式描述集合:給一個點,代進去檢查 |
| explicit description | 顯式描述 | 直接列出集合裡的所有點:$\mathbf{x} = s\mathbf{u} + t\mathbf{v}$ |
| parametric vector equation | 參數向量方程式 | 把解寫成「向量 + 參數 × 向量」的式子 |
| parametric vector form | 參數向量形式 | 解集用參數向量方程式表示的樣子 |
| particular solution | 特解 | $A\mathbf{x} = \mathbf{b}$ 的某**一個**解,記作 $\mathbf{p}$ |
| translation | 平移 | 每一點都加上同一個向量 $\mathbf{p}$ |
| line through $\mathbf{p}$ parallel to $\mathbf{v}$ | 通過 $\mathbf{p}$、平行 $\mathbf{v}$ 的直線 | $\mathbf{x} = \mathbf{p} + t\mathbf{v}$ |

## 白話說
**一句話:$A\mathbf{x} = \mathbf{b}$ 的所有解 = 一個特解 + $A\mathbf{x} = \mathbf{0}$ 的所有解。**

寫成式子就是 $\mathbf{x} = \mathbf{p} + t\mathbf{v}$(一個自由變數)或 $\mathbf{x} = \mathbf{p} + s\mathbf{u} + t\mathbf{v}$(兩個自由變數):

- $\mathbf{p}$(特解):自由變數**全填 0** 時得到的那個解。它負責「滿足 $\mathbf{b}$」。
- $t\mathbf{v}$、$s\mathbf{u} + t\mathbf{v}$(齊次解):乘上 $A$ 會變成 $\mathbf{0}$,所以加多少都不影響結果。

打個比方:$\mathbf{p}$ 是「一個能到達目的地的走法」,齊次解是「原地繞圈、最後回到原點的走法」。先照 $\mathbf{p}$ 走、再隨便繞幾圈,終點還是一樣——所以解有無限多個。

**做法就是課本方框的四步**:化 RREF → 基本變數用自由變數表示 → 寫成向量 → 依自由變數拆開,常數的部分就是 $\mathbf{p}$。

## 幾何意義
向量加法可以看成**平移**:把 $A\mathbf{x} = \mathbf{0}$ 的解集(通過原點的直線或平面)整個搬動 $\mathbf{p}$,就得到 $A\mathbf{x} = \mathbf{b}$ 的解集。

![課本 Figure 5:Ax = 0 的解集是通過原點、方向為 v 的直線;Ax = b 的解集是把它平移 p 的平行線。直線上每一點都是 p + tv。](translate.svg)

兩個自由變數時是兩個**平行的平面**,只有 $A\mathbf{x} = \mathbf{0}$ 那個通過原點:

![課本 Figure 6:Ax = 0 與 Ax = b 的解集是兩個平行的平面。](parallel-planes.svg)

## 在資工哪裡用
- **欠定系統(underdetermined system)**:方程式比未知數少時,解有無限多個。機器學習的參數常常比資料點多,「所有讓訓練誤差為 0 的參數」就是 $\mathbf{p}$ + 一整個齊次解空間;演算法挑的是其中「最短」的那個(第 14 週的最小平方與第 16 週的偽逆)。
- **電腦圖學的直線與平面**:光線追蹤裡,一條光線寫成 $\mathbf{p} + t\mathbf{v}$(起點 + 參數 × 方向),正是參數向量形式;$t$ 就是光走的距離。
- **遊戲的移動**:物體沿直線移動,每一格的位置 $\mathbf{p} + t\mathbf{v}$,$t$ 是時間。

## 原理
**Theorem 6 的證明分兩半**(本週的證明時刻):

1. **$\mathbf{p} + \mathbf{v}_h$ 一定是解**(Practice Problem 3):$A(\mathbf{p} + \mathbf{v}_h) = A\mathbf{p} + A\mathbf{v}_h = \mathbf{b} + \mathbf{0} = \mathbf{b}$。
2. **每個解都長這樣**(Exercise 37):任取一個解 $\mathbf{w}$,令 $\mathbf{v}_h = \mathbf{w} - \mathbf{p}$,則 $A\mathbf{v}_h = A\mathbf{w} - A\mathbf{p} = \mathbf{b} - \mathbf{b} = \mathbf{0}$,所以 $\mathbf{w} = \mathbf{p} + \mathbf{v}_h$,而 $\mathbf{v}_h$ 是齊次解。

兩步都只用到上週的 Theorem 5($A\mathbf{x}$ 的線性)。

**為什麼要求相容?** 無解時根本沒有 $\mathbf{p}$ 可以拿來平移;解集是空集合,不是「平移過的直線」(Exercise 49)。

**推論:唯一解 ⇔ 齊次方程只有平凡解**(Exercise 38)。有解時,解的個數和齊次解一樣多:齊次只有 $\mathbf{0}$,就只有 $\mathbf{p}$ 一個。

## 老師講解
### 例 1 · Lay 1.5 Example 3
Describe all solutions of $A\mathbf{x} = \mathbf{b}$, where

$$A = \begin{bmatrix} 3 & 5 & -4 \\ -3 & -2 & 4 \\ 6 & 1 & -8 \end{bmatrix} \quad \text{and} \quad \mathbf{b} = \begin{bmatrix} 7 \\ -1 \\ -4 \end{bmatrix}.$$

1. **$A$ 就是觀念 1 例 1 的係數矩陣**,只是右邊換成 $\mathbf{b}$。化簡 $[\,A \;\; \mathbf{b}\,]$ 到 RREF:
   $$\left[\begin{array}{rrr|r} 3 & 5 & -4 & 7 \\ -3 & -2 & 4 & -1 \\ 6 & 1 & -8 & -4 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 0 & -\tfrac43 & -1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 0 & 0 \end{array}\right] \qquad \begin{aligned} x_1 - \tfrac43 x_3 &= -1 \\ x_2 &= 2 \end{aligned}$$
2. **先確認相容**:最後一行不是 pivot 行,有解。
3. **基本變數用自由變數表示**:$x_1 = -1 + \tfrac43 x_3$、$x_2 = 2$,$x_3$ 自由。
4. **寫成向量,再把常數項和含 $x_3$ 的項拆開**:
   $$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} -1 + \tfrac43 x_3 \\ 2 \\ x_3 \end{bmatrix} = \begin{bmatrix} -1 \\ 2 \\ 0 \end{bmatrix} + \begin{bmatrix} \tfrac43 x_3 \\ 0 \\ x_3 \end{bmatrix} = \underbrace{\begin{bmatrix} -1 \\ 2 \\ 0 \end{bmatrix}}_{\mathbf{p}} + x_3\underbrace{\begin{bmatrix} \tfrac43 \\ 0 \\ 1 \end{bmatrix}}_{\mathbf{v}}$$
5. **參數向量形式**:$\mathbf{x} = \mathbf{p} + t\mathbf{v}$($t$ 為任意實數)。
6. **和觀念 1 例 1 對照**:那一題的解集是 $\mathbf{x} = t\mathbf{v}$,**$\mathbf{v}$ 一模一樣**。所以 $A\mathbf{x} = \mathbf{b}$ 的解集,就是把 $A\mathbf{x} = \mathbf{0}$ 的解集(通過原點的直線)平移 $\mathbf{p}$ 得到的平行直線。
7. **驗算**:$A\mathbf{p} = (-3 + 10,\; 3 - 4,\; -6 + 2) = (7, -1, -4) = \mathbf{b}$ ✓;$A\mathbf{v} = \mathbf{0}$ 在觀念 1 驗過了。

### 例 2 · Lay 1.5(pp. 73–74,Reasonable Answers)
Let $A = \begin{bmatrix} 1 & -2 & 1 & 2 \\ 1 & -1 & 2 & 5 \\ 0 & 1 & 1 & 3 \end{bmatrix}$. Verify that $\mathbf{x} = \begin{bmatrix} 2 \\ 1 \\ 1 \\ 2 \end{bmatrix} + x_3\begin{bmatrix} -3 \\ -1 \\ 1 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} -8 \\ -3 \\ 0 \\ 1 \end{bmatrix}$ are solutions to $A\mathbf{x} = \begin{bmatrix} 5 \\ 13 \\ 8 \end{bmatrix}$.

1. **驗算的策略**:不用代一般解的每個 $x_3, x_4$,只要把 $A$ 乘上**每一個**向量:特解要得到 $\mathbf{b}$,其他的要得到 $\mathbf{0}$。
2. **特解**:$A\begin{bmatrix} 2 \\ 1 \\ 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 2 - 2 + 1 + 4 \\ 2 - 1 + 2 + 10 \\ 0 + 1 + 1 + 6 \end{bmatrix} = \begin{bmatrix} 5 \\ 13 \\ 8 \end{bmatrix}$ ✓。
3. **第一個齊次向量**:$A\begin{bmatrix} -3 \\ -1 \\ 1 \\ 0 \end{bmatrix} = \begin{bmatrix} -3 + 2 + 1 + 0 \\ -3 + 1 + 2 + 0 \\ 0 - 1 + 1 + 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$ ✓。
4. **第二個齊次向量**:$A\begin{bmatrix} -8 \\ -3 \\ 0 \\ 1 \end{bmatrix} = \begin{bmatrix} -8 + 6 + 0 + 2 \\ -8 + 3 + 0 + 5 \\ 0 - 3 + 0 + 3 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$ ✓。
5. **用線性性質合起來**:$A(\mathbf{p} + x_3\mathbf{u} + x_4\mathbf{v}) = A\mathbf{p} + x_3A\mathbf{u} + x_4A\mathbf{v} = \mathbf{b} + \mathbf{0} + \mathbf{0} = \mathbf{b}$。所有 $x_3, x_4$ 一次驗完。

#### 備註
這個驗算法學生考試時很實用:三次矩陣乘向量就能確認整個一般解,不用重算列化簡。

## 易錯點
- 把特解 $\mathbf{p}$ 當成齊次解的一部分,或反過來:常數項才是 $\mathbf{p}$,乘著自由變數的向量才是齊次解。
- 驗算時把 $A$ 乘上齊次向量,期待得到 $\mathbf{b}$。齊次向量乘出來要是 $\mathbf{0}$。
- 忘了 Theorem 6 要求**相容**。無解時解集是空集合,不能說「平移」(是非題 Exercises 35–36)。
- 把「通過 $\mathbf{p}$、平行 $\mathbf{v}$」說成「通過 $\mathbf{v}$、平行 $\mathbf{p}$」(是非題 Exercise 33)。
- 以為 $A\mathbf{x} = \mathbf{b}$($\mathbf{b} \neq \mathbf{0}$)的解集可以通過原點。$\mathbf{0}$ 代進去得 $\mathbf{0} \neq \mathbf{b}$,不可能(Exercise 40)。

## 教學提示
例 1 一定要和觀念 1 例 1 **並排寫**:同一個 $A$、同一個 $\mathbf{v}$,只多了 $\mathbf{p}$。然後畫平移的圖。學生看到「兩題的 $\mathbf{v}$ 一樣」時,Theorem 6 就不需要背了。

「原地繞圈」的比喻很有效:齊次解是「怎麼走都回到原點」的路線,加在任何一條到得了目的地的路線上,終點不變。

課堂建議做:Exercises 17、19、21;Practice Problem 2;是非 Exercises 33、35、36;Exercises 25 與 41–44 挑兩題。

## 練習
### 照做 · Lay 1.5 Exercises 17–18
Use vectors to describe the solution set as a line.

(17) Suppose the solution set of a certain system of linear equations can be described as $x_1 = 5 + 4x_3$, $x_2 = -2 - 7x_3$, with $x_3$ free. Use vectors to describe this set as a line in $\mathbb{R}^3$. (18) Suppose the solution set of a certain system of linear equations can be described as $x_1 = 3x_4$, $x_2 = 8 + x_4$, $x_3 = 2 - 5x_4$, with $x_4$ free. Use vectors to describe this set as a line in $\mathbb{R}^4$.

#### 解答
(17) $\mathbf{x} = \begin{bmatrix} 5 + 4x_3 \\ -2 - 7x_3 \\ x_3 \end{bmatrix} = \begin{bmatrix} 5 \\ -2 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} 4 \\ -7 \\ 1 \end{bmatrix} = \mathbf{p} + x_3\mathbf{q}$:通過 $(5, -2, 0)$、平行 $(4, -7, 1)$ 的直線(書後解答相同)。

(18) $\mathbf{x} = \begin{bmatrix} 3x_4 \\ 8 + x_4 \\ 2 - 5x_4 \\ x_4 \end{bmatrix} = \begin{bmatrix} 0 \\ 8 \\ 2 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} 3 \\ 1 \\ -5 \\ 1 \end{bmatrix}$:ℝ⁴ 中通過 $(0, 8, 2, 0)$、平行 $(3, 1, -5, 1)$ 的直線。

### 照做 · Lay 1.5 Exercises 19–20
Describe the solutions of the system in parametric vector form, and give a geometric comparison with the solution set of the homogeneous system with the same coefficients.

(19) Follow the method of Example 3 to describe the solutions of the following system in parametric vector form. Also, give a geometric description of the solution set and compare it to that in Exercise 5.
$$\begin{aligned} x_1 + 3x_2 + x_3 &= 1 \\ -4x_1 - 9x_2 + 2x_3 &= -1 \\ -3x_2 - 6x_3 &= -3 \end{aligned}$$

(20) As in Exercise 19, describe the solutions of the following system in parametric vector form, and provide a geometric comparison with the solution set in Exercise 6.
$$\begin{aligned} x_1 + 3x_2 - 5x_3 &= 4 \\ x_1 + 4x_2 - 8x_3 &= 7 \\ -3x_1 - 7x_2 + 9x_3 &= -6 \end{aligned}$$

#### 解答
(19) 化簡增廣矩陣:

$$\left[\begin{array}{rrr|r} 1 & 3 & 1 & 1 \\ -4 & -9 & 2 & -1 \\ 0 & -3 & -6 & -3 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 3 & 1 & 1 \\ 0 & 3 & 6 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 0 & -5 & -2 \\ 0 & 1 & 2 & 1 \\ 0 & 0 & 0 & 0 \end{array}\right]$$

$x_1 = -2 + 5x_3$、$x_2 = 1 - 2x_3$,所以 $\mathbf{x} = \begin{bmatrix} -2 \\ 1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix}$。幾何上:通過 $(-2, 1, 0)$ 的直線,平行於 Exercise 5 的解集(通過原點的直線 $\operatorname{Span}\{(5, -2, 1)\}$)(書後解答相同)。

(20) 化到 RREF $\left[\begin{array}{rrr|r} 1 & 0 & 4 & -5 \\ 0 & 1 & -3 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right]$,$x_1 = -5 - 4x_3$、$x_2 = 3 + 3x_3$,所以 $\mathbf{x} = \begin{bmatrix} -5 \\ 3 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} -4 \\ 3 \\ 1 \end{bmatrix}$:通過 $(-5, 3, 0)$、平行於 Exercise 6 解集的直線。

### 照做 · Lay 1.5 Exercises 21–22
Describe and compare the solution sets of the two equations.

(21) $x_1 + 9x_2 - 4x_3 = 0$ and $x_1 + 9x_2 - 4x_3 = -2$. (22) $x_1 - 3x_2 + 5x_3 = 0$ and $x_1 - 3x_2 + 5x_3 = 4$.

#### 解答
(21) 令 $\mathbf{u} = (-9, 1, 0)$、$\mathbf{v} = (4, 0, 1)$、$\mathbf{p} = (-2, 0, 0)$。齊次方程式的解是 $\mathbf{x} = x_2\mathbf{u} + x_3\mathbf{v}$,通過原點的平面;非齊次的解是 $\mathbf{x} = \mathbf{p} + x_2\mathbf{u} + x_3\mathbf{v}$,通過 $\mathbf{p}$、和前者平行的平面(書後解答相同)。

(22) 齊次:$x_1 = 3x_2 - 5x_3$,$\mathbf{x} = x_2\begin{bmatrix} 3 \\ 1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} -5 \\ 0 \\ 1 \end{bmatrix}$,通過原點的平面。非齊次:$\mathbf{x} = \begin{bmatrix} 4 \\ 0 \\ 0 \end{bmatrix} + x_2\begin{bmatrix} 3 \\ 1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} -5 \\ 0 \\ 1 \end{bmatrix}$,通過 $(4, 0, 0)$ 的平行平面。

### 照做 · Lay 1.5 Practice Problem 2
Write the general solution of $10x_1 - 3x_2 - 2x_3 = 7$ in parametric vector form, and relate the solution set to the one found in Example 2.

#### 解答
增廣矩陣 $[\,10 \;\; {-3} \;\; {-2} \;\; 7\,] \sim [\,1 \;\; {-.3} \;\; {-.2} \;\; .7\,]$,一般解 $x_1 = .7 + .3x_2 + .2x_3$,$x_2, x_3$ 自由:
$$\mathbf{x} = \begin{bmatrix} .7 \\ 0 \\ 0 \end{bmatrix} + x_2\begin{bmatrix} .3 \\ 1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} .2 \\ 0 \\ 1 \end{bmatrix} = \mathbf{p} + x_2\mathbf{u} + x_3\mathbf{v}$$
解集是平移過的平面 $\mathbf{p} + \operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$:通過 $\mathbf{p}$,平行於觀念 1 例 2 的齊次解集(課本 p. 77)。

### 是非 · Lay 1.5 Exercise 29
**(T/F)** The equation $A\mathbf{x} = \mathbf{0}$ gives an explicit description of its solution set.

#### 解答
**False.** $A\mathbf{x} = \mathbf{0}$ 是**隱式**描述(只能拿點去檢查);解出來寫成參數向量形式才是顯式描述。

### 是非 · Lay 1.5 Exercise 30
**(T/F)** The equation $\mathbf{x} = x_2\mathbf{u} + x_3\mathbf{v}$, with $x_2$ and $x_3$ free (and neither $\mathbf{u}$ nor $\mathbf{v}$ a multiple of the other), describes a plane through the origin.

#### 解答
**True.** 這就是 $\operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$,$\mathbf{u}$、$\mathbf{v}$ 不平行,是通過原點的平面(取 $x_2 = x_3 = 0$ 得原點)。

### 是非 · Lay 1.5 Exercise 33
**(T/F)** The equation $\mathbf{x} = \mathbf{p} + t\mathbf{v}$ describes a line through $\mathbf{v}$ parallel to $\mathbf{p}$.

#### 解答
**False.** 是通過 **$\mathbf{p}$**、平行 **$\mathbf{v}$** 的直線。反例:$\mathbf{p} = (1, 0)$、$\mathbf{v} = (0, 1)$,直線 $\{(1, t)\}$ 根本不經過 $\mathbf{v}$。

### 是非 · Lay 1.5 Exercise 34
**(T/F)** The effect of adding $\mathbf{p}$ to a vector is to move the vector in a direction parallel to $\mathbf{p}$.

#### 解答
**True.** $(\mathbf{v} + \mathbf{p}) - \mathbf{v} = \mathbf{p}$,$\mathbf{v}$ 被沿著 $\mathbf{p}$ 的方向搬動(課本對平移的描述)。

### 是非 · Lay 1.5 Exercise 35
**(T/F)** The solution set of $A\mathbf{x} = \mathbf{b}$ is the set of all vectors of the form $\mathbf{w} = \mathbf{p} + \mathbf{v}_h$, where $\mathbf{v}_h$ is any solution of the equation $A\mathbf{x} = \mathbf{0}$.

#### 解答
**False.** 這是 Theorem 6,但少了前提:$A\mathbf{x} = \mathbf{b}$ 要**相容**,而且 $\mathbf{p}$ 要是它的一個解。無解時解集是空集合,$\{\mathbf{p} + \mathbf{v}_h\}$ 卻不是空的。

### 是非 · Lay 1.5 Exercise 36
**(T/F)** The solution set of $A\mathbf{x} = \mathbf{b}$ is obtained by translating the solution set of $A\mathbf{x} = \mathbf{0}$.

#### 解答
**False**(作為一般敘述)。只有 $A\mathbf{x} = \mathbf{b}$ 相容時才成立(課本 Theorem 6 後的 Warning);無解時解集是空的,不是齊次解集平移的結果。

### 變化 · Lay 1.5 Exercises 23–24
Find the parametric equation of the line through $\mathbf{a}$ parallel to $\mathbf{b}$.

(23) $\mathbf{a} = \begin{bmatrix} -2 \\ 0 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} -5 \\ 3 \end{bmatrix}$  (24) $\mathbf{a} = \begin{bmatrix} 5 \\ -2 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} -4 \\ 9 \end{bmatrix}$

#### 解答
(23) $\mathbf{x} = \mathbf{a} + t\mathbf{b} = \begin{bmatrix} -2 \\ 0 \end{bmatrix} + t\begin{bmatrix} -5 \\ 3 \end{bmatrix}$,也可以寫成 $x_1 = -2 - 5t$、$x_2 = 3t$(書後解答相同)。

(24) $\mathbf{x} = \begin{bmatrix} 5 \\ -2 \end{bmatrix} + t\begin{bmatrix} -4 \\ 9 \end{bmatrix}$,也就是 $x_1 = 5 - 4t$、$x_2 = -2 + 9t$。

### 變化 · Lay 1.5 Exercises 25–26
Find a parametric equation of the line $M$ through $\mathbf{p}$ and $\mathbf{q}$. [*Hint:* $M$ is parallel to the vector $\mathbf{q} - \mathbf{p}$. See the figure below.]

(25) $\mathbf{p} = \begin{bmatrix} 2 \\ -5 \end{bmatrix}$, $\mathbf{q} = \begin{bmatrix} -3 \\ 1 \end{bmatrix}$  (26) $\mathbf{p} = \begin{bmatrix} -6 \\ 3 \end{bmatrix}$, $\mathbf{q} = \begin{bmatrix} 0 \\ -4 \end{bmatrix}$

![The line through p and q is parallel to q − p.](line-pq.svg)

#### 解答
(25) $\mathbf{q} - \mathbf{p} = \begin{bmatrix} -5 \\ 6 \end{bmatrix}$,所以 $\mathbf{x} = \mathbf{p} + t(\mathbf{q} - \mathbf{p}) = \begin{bmatrix} 2 \\ -5 \end{bmatrix} + t\begin{bmatrix} -5 \\ 6 \end{bmatrix}$。$t = 0$ 得 $\mathbf{p}$,$t = 1$ 得 $\mathbf{q}$(書後解答相同)。

(26) $\mathbf{q} - \mathbf{p} = \begin{bmatrix} 6 \\ -7 \end{bmatrix}$,所以 $\mathbf{x} = \begin{bmatrix} -6 \\ 3 \end{bmatrix} + t\begin{bmatrix} 6 \\ -7 \end{bmatrix}$。

#### 備註
課本的圖是示意圖,點的位置和兩題的數字不對應。這個「$\mathbf{p} + t(\mathbf{q} - \mathbf{p})$」就是動畫的線性內插,$t$ 從 0 走到 1。

### 變化 · Lay 1.5 Practice Problem 1
Each of the following equations determines a plane in $\mathbb{R}^3$. Do the two planes intersect? If so, describe their intersection.

$$\begin{aligned} x_1 + 4x_2 - 5x_3 &= 0 \\ 2x_1 - x_2 + 8x_3 &= 9 \end{aligned}$$

#### 解答
兩個平面的交點,就是同時滿足兩條方程式的點:
$$\left[\begin{array}{rrr|r} 1 & 4 & -5 & 0 \\ 2 & -1 & 8 & 9 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 4 & -5 & 0 \\ 0 & -9 & 18 & 9 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 0 & 3 & 4 \\ 0 & 1 & -2 & -1 \end{array}\right]$$
$x_1 = 4 - 3x_3$、$x_2 = -1 + 2x_3$,$x_3$ 自由:
$$\mathbf{x} = \begin{bmatrix} 4 \\ -1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} -3 \\ 2 \\ 1 \end{bmatrix} = \mathbf{p} + x_3\mathbf{v}$$
兩平面**相交**於通過 $\mathbf{p}$、方向為 $\mathbf{v}$ 的直線(課本 p. 77)。

### 變化 · Lay 1.5 Exercises 41–44
(a) Does the equation $A\mathbf{x} = \mathbf{0}$ have a nontrivial solution and (b) does the equation $A\mathbf{x} = \mathbf{b}$ have at least one solution for every possible $\mathbf{b}$?

(41) $A$ is a $3 \times 3$ matrix with three pivot positions. (42) $A$ is a $3 \times 3$ matrix with two pivot positions. (43) $A$ is a $3 \times 2$ matrix with two pivot positions. (44) $A$ is a $2 \times 4$ matrix with two pivot positions.

#### 解答
兩個問題看不同的東西:(a) 看**行**(有沒有自由變數),(b) 看**列**(Theorem 4:每一列有沒有 pivot)。

(41) (a) **否**:3 行都是 pivot 行,沒有自由變數。(b) **是**:3 列都有 pivot(書後解答相同;「possible」指 ℝ³ 中的 $\mathbf{b}$)。

(42) (a) **是**:3 行、2 個 pivot,有 1 個自由變數。(b) **否**:3 列只有 2 個 pivot。

(43) (a) **否**:2 行都是 pivot 行。(b) **否**:3 列只有 2 個 pivot(書後解答相同)。

(44) (a) **是**:4 行、2 個 pivot,有 2 個自由變數。(b) **是**:2 列都有 pivot。

#### 備註
四題並排,學生就會發現 (a)(b) 互不決定:(41) 否/是、(42) 是/否、(43) 否/否、(44) 是/是,四種組合都出現了。

### 挑戰 · Lay 1.5 Practice Problem 3
Prove the first part of Theorem 6: Suppose that $\mathbf{p}$ is a solution of $A\mathbf{x} = \mathbf{b}$, so that $A\mathbf{p} = \mathbf{b}$. Let $\mathbf{v}_h$ be any solution to the homogeneous equation $A\mathbf{x} = \mathbf{0}$, and let $\mathbf{w} = \mathbf{p} + \mathbf{v}_h$. Show that $\mathbf{w}$ is a solution to $A\mathbf{x} = \mathbf{b}$.

#### 解答
由上週的 Theorem 5:$A(\mathbf{p} + \mathbf{v}_h) = A\mathbf{p} + A\mathbf{v}_h = \mathbf{b} + \mathbf{0} = \mathbf{b}$,所以 $\mathbf{p} + \mathbf{v}_h$ 是 $A\mathbf{x} = \mathbf{b}$ 的解(課本 p. 77)。

### 挑戰 · Lay 1.5 Exercise 37
Prove the second part of Theorem 6: Let $\mathbf{w}$ be any solution of $A\mathbf{x} = \mathbf{b}$, and define $\mathbf{v}_h = \mathbf{w} - \mathbf{p}$. Show that $\mathbf{v}_h$ is a solution of $A\mathbf{x} = \mathbf{0}$. This shows that every solution of $A\mathbf{x} = \mathbf{b}$ has the form $\mathbf{w} = \mathbf{p} + \mathbf{v}_h$, with $\mathbf{p}$ a particular solution of $A\mathbf{x} = \mathbf{b}$ and $\mathbf{v}_h$ a solution of $A\mathbf{x} = \mathbf{0}$.

#### 解答
$A\mathbf{v}_h = A(\mathbf{w} - \mathbf{p}) = A\mathbf{w} - A\mathbf{p} = \mathbf{b} - \mathbf{b} = \mathbf{0}$(書後解答相同)。所以 $\mathbf{v}_h$ 是齊次解,而 $\mathbf{w} = \mathbf{p} + (\mathbf{w} - \mathbf{p}) = \mathbf{p} + \mathbf{v}_h$。

#### 備註
Practice Problem 3 與 Exercise 37 合起來就是 Theorem 6 的完整證明,也就是本週的證明時刻。

### 挑戰 · Lay 1.5 Exercises 38, 40
(38) Suppose $A\mathbf{x} = \mathbf{b}$ has a solution. Explain why the solution is unique precisely when $A\mathbf{x} = \mathbf{0}$ has only the trivial solution. (40) If $\mathbf{b} \neq \mathbf{0}$, can the solution set of $A\mathbf{x} = \mathbf{b}$ be a plane through the origin? Explain.

#### 解答
(38) 設 $\mathbf{p}$ 是一個解。由 Theorem 6,解集是 $\{\mathbf{p} + \mathbf{v}_h : A\mathbf{v}_h = \mathbf{0}\}$。若齊次只有 $\mathbf{v}_h = \mathbf{0}$,解集就只有 $\mathbf{p}$,唯一;若有非平凡的 $\mathbf{v}_h$,則 $\mathbf{p} + \mathbf{v}_h \neq \mathbf{p}$ 是第二個解,不唯一。

(40) **不能**。通過原點的平面包含 $\mathbf{0}$,但 $A\mathbf{0} = \mathbf{0} \neq \mathbf{b}$,$\mathbf{0}$ 不是解。


### 挑戰 · Lay 1.5 Exercise 49
Construct a $2 \times 2$ matrix $A$ such that the solution set of the equation $A\mathbf{x} = \mathbf{0}$ is the line in $\mathbb{R}^2$ through $(4, 1)$ and the origin. Then, find a vector $\mathbf{b}$ in $\mathbb{R}^2$ such that the solution set of $A\mathbf{x} = \mathbf{b}$ is *not* a line in $\mathbb{R}^2$ parallel to the solution set of $A\mathbf{x} = \mathbf{0}$. Why does this *not* contradict Theorem 6?

#### 解答
要 $A\mathbf{x} = \mathbf{0}$ ⇔ $x_1 = 4x_2$:取 $A = \begin{bmatrix} 1 & -4 \\ 1 & -4 \end{bmatrix}$(書後解答的答案之一),解集是 $x_2(4, 1)$。

取 $\mathbf{b} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$(不是第一行 $(1, 1)$ 的倍數):$\left[\begin{array}{rr|r} 1 & -4 & 1 \\ 1 & -4 & 0 \end{array}\right] \sim \left[\begin{array}{rr|r} 1 & -4 & 1 \\ 0 & 0 & -1 \end{array}\right]$,無解,解集是空集合,不是直線。

不矛盾:Theorem 6 只適用於**相容**的 $A\mathbf{x} = \mathbf{b}$。

#### 備註
書後解答這題最後一句印成「translating the solution set of $A\mathbf{x} = \mathbf{b}$」,應該是 $A\mathbf{x} = \mathbf{0}$(印刷錯誤)。

### 挑戰 · Lay 1.5 Exercise 50
Suppose $A$ is a $3 \times 3$ matrix and $\mathbf{y}$ is a vector in $\mathbb{R}^3$ such that the equation $A\mathbf{x} = \mathbf{y}$ does *not* have a solution. Does there exist a vector $\mathbf{z}$ in $\mathbb{R}^3$ such that the equation $A\mathbf{x} = \mathbf{z}$ has a unique solution? Discuss.

#### 解答
**不存在。** $A\mathbf{x} = \mathbf{y}$ 無解,由 Theorem 4,$A$ 不是每一列都有 pivot,最多 2 個 pivot。3 行中至少有一行不是 pivot 行,所以 $A\mathbf{x} = \mathbf{0}$ 有自由變數、有非平凡解。由 Theorem 6(或 Exercise 38),任何 $A\mathbf{x} = \mathbf{z}$ 不是無解,就是無限多解,不可能恰好一個。

#### 備註
這題把 Theorem 4(看列)和 Theorem 6(看行)接在一起:對**方陣**來說,「每個 $\mathbf{b}$ 都有解」和「解唯一」會同時成立或同時失敗——這是第 6 週可逆矩陣定理的第一道影子。

## 驗算
```check
Matrix([[3, 5, -4, 7], [-3, -2, 4, -1], [6, 1, -8, -4]]).rref()[0] == Matrix([[1, 0, Rational(-4, 3), -1], [0, 1, 0, 2], [0, 0, 0, 0]])
Matrix([[3, 5, -4], [-3, -2, 4], [6, 1, -8]]) * Matrix([-1, 2, 0]) == Matrix([7, -1, -4])
Matrix([[1, -2, 1, 2], [1, -1, 2, 5], [0, 1, 1, 3]]) * Matrix([2, 1, 1, 2]) == Matrix([5, 13, 8])
Matrix([[1, -2, 1, 2], [1, -1, 2, 5], [0, 1, 1, 3]]) * Matrix([-3, -1, 1, 0]) == zeros(3, 1)
Matrix([[1, -2, 1, 2], [1, -1, 2, 5], [0, 1, 1, 3]]) * Matrix([-8, -3, 0, 1]) == zeros(3, 1)
Matrix([5, -2, 0]) + x3 * Matrix([4, -7, 1]) == Matrix([5 + 4*x3, -2 - 7*x3, x3])
Matrix([0, 8, 2, 0]) + x4 * Matrix([3, 1, -5, 1]) == Matrix([3*x4, 8 + x4, 2 - 5*x4, x4])
Matrix([[1, 3, 1, 1], [-4, -9, 2, -1], [0, -3, -6, -3]]).rref()[0] == Matrix([[1, 0, -5, -2], [0, 1, 2, 1], [0, 0, 0, 0]])
Matrix([[1, 3, -5, 4], [1, 4, -8, 7], [-3, -7, 9, -6]]).rref()[0] == Matrix([[1, 0, 4, -5], [0, 1, -3, 3], [0, 0, 0, 0]])
Matrix([[1, 9, -4]]).nullspace() == [Matrix([-9, 1, 0]), Matrix([4, 0, 1])] and Matrix([[1, 9, -4]]) * Matrix([-2, 0, 0]) == Matrix([-2])
Matrix([[1, -3, 5]]).nullspace() == [Matrix([3, 1, 0]), Matrix([-5, 0, 1])] and Matrix([[1, -3, 5]]) * Matrix([4, 0, 0]) == Matrix([4])
Matrix([[10, -3, -2]]) * Matrix([Rational(7, 10), 0, 0]) == Matrix([7])
Matrix([-3, 1]) - Matrix([2, -5]) == Matrix([-5, 6])
Matrix([0, -4]) - Matrix([-6, 3]) == Matrix([6, -7])
Matrix([[1, 4, -5, 0], [2, -1, 8, 9]]).rref()[0] == Matrix([[1, 0, 3, 4], [0, 1, -2, -1]])
eye(3).nullspace() == [] and eye(3).rank() == 3
len(diag(1, 1, 0).nullspace()) == 1 and diag(1, 1, 0).rank() == 2
Matrix([[1, 0], [0, 1], [0, 0]]).nullspace() == [] and Matrix([[1, 0], [0, 1], [0, 0]]).rank() == 2
len(Matrix([[1, 0, 0, 0], [0, 1, 0, 0]]).nullspace()) == 2 and Matrix([[1, 0, 0, 0], [0, 1, 0, 0]]).rank() == 2
Matrix([[1, -4], [1, -4]]).nullspace() == [Matrix([4, 1])]
Matrix([[1, -4, 1], [1, -4, 0]]).rref()[1] == (0, 2)
```
