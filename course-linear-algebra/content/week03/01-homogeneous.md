---
title_en: Homogeneous Linear Systems
title_zh: 齊次方程組:Ax = 0 什麼時候有非零解
sub: A free variable means a nontrivial solution
level: basic
source: Lay 1.5
lab_hook: '`Matrix(A).nullspace()`:直接給出 $A\mathbf{x} = \mathbf{0}$ 解集的生成向量'
---
## 觀念
A system of linear equations is said to be **homogeneous** if it can be written in the form $A\mathbf{x} = \mathbf{0}$, where $A$ is an $m \times n$ matrix and $\mathbf{0}$ is the zero vector in $\mathbb{R}^m$. Such a system $A\mathbf{x} = \mathbf{0}$ *always* has at least one solution, namely $\mathbf{x} = \mathbf{0}$ (the zero vector in $\mathbb{R}^n$). This zero solution is usually called the **trivial solution**. For a given equation $A\mathbf{x} = \mathbf{0}$, the important question is whether there exists a **nontrivial solution**, that is, a nonzero vector $\mathbf{x}$ that satisfies $A\mathbf{x} = \mathbf{0}$.

> The homogeneous equation $A\mathbf{x} = \mathbf{0}$ has a nontrivial solution if and only if the equation has at least one free variable.

The solution set of a homogeneous equation $A\mathbf{x} = \mathbf{0}$ can always be expressed explicitly as $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ for suitable vectors $\mathbf{v}_1, \dots, \mathbf{v}_p$. If the only solution is the zero vector, then the solution set is $\operatorname{Span}\{\mathbf{0}\}$. If the equation $A\mathbf{x} = \mathbf{0}$ has only one free variable, the solution set is a line through the origin. A plane through the origin provides a good mental image for the solution set of $A\mathbf{x} = \mathbf{0}$ when there are two or more free variables.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| homogeneous system | 齊次方程組 | 右邊全是 0 的方程組,寫成 $A\mathbf{x} = \mathbf{0}$ |
| nonhomogeneous system | 非齊次方程組 | 右邊 $\mathbf{b} \neq \mathbf{0}$ 的方程組 |
| trivial solution | 平凡解 | $\mathbf{x} = \mathbf{0}$;齊次方程組一定有這個解 |
| nontrivial solution | 非平凡解 | 不全為 0 的解(可以有某些分量是 0) |
| zero vector | 零向量 | 每個分量都是 0 的向量,記作 $\mathbf{0}$ |
| solution set | 解集 | 所有解收集起來的集合 |

## 白話說
右邊全是 0 的方程組叫**齊次**。它一定有解:全部未知數都填 0,每條式子都是 $0 = 0$。這個解太理所當然,所以叫「平凡解」。

真正的問題是:**除了全填 0,還有沒有別的解?**

答案只要看一件事——**有沒有自由變數**:

- 沒有自由變數 → 解唯一,只能是 $\mathbf{0}$。
- 有自由變數 → 自由變數隨便填一個不是 0 的數,就得到一個非平凡解,而且有無限多個。

而且齊次方程組的解集一定是一個 **Span**:一個自由變數是一條通過原點的直線,兩個自由變數是一個通過原點的平面。

## 幾何意義
![課本 1.5 Figures 1–2:一個自由變數時,解集是通過原點的直線 Span{v};兩個自由變數時,是通過原點的平面 Span{u, v}。](homog-line-plane.svg)

解集**一定通過原點**,因為 $\mathbf{0}$ 永遠是解。這點和下一個觀念的非齊次方程組不同。

## 在資工哪裡用
- **資料有沒有多餘的欄位**:把資料的每一欄當成 $A$ 的一行。如果 $A\mathbf{x} = \mathbf{0}$ 有非平凡解,就代表某些欄位可以由其他欄位算出來(例如「總分 = 國文 + 英文」),這正是實作課要找的東西。
- **電路與網路流的迴路**:流量守恆的方程組是齊次的。非平凡解代表網路裡有「繞一圈」的流量,這在網路流演算法裡叫做 circulation。
- **化學配平**:第 1 週的化學配平就是齊次方程組;我們要的正是非平凡解(係數全 0 沒有意義)。

## 原理
**為什麼「有自由變數 ⇔ 有非平凡解」?** 齊次方程組一定相容(最後一行全是 0,不可能出現 $0 = $ 非零數)。依第 1 週的存在與唯一性定理(Theorem 2):相容的方程組,沒有自由變數就唯一解,有自由變數就無限多解。唯一解只能是平凡解 $\mathbf{0}$;無限多解裡當然有非零的。

**為什麼解集是 Span?** 把基本變數用自由變數表示、寫成向量,再依自由變數拆開(例 1 的做法),每個解都寫成 $x_{j_1}\mathbf{v}_1 + \cdots + x_{j_p}\mathbf{v}_p$ 的形式,自由變數就是權重。所有這種組合,正是 $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$。

## 老師講解
### 例 1 · Lay 1.5 Example 1
Determine if the following homogeneous system has a nontrivial solution. Then describe the solution set.

$$\begin{aligned} 3x_1 + 5x_2 - 4x_3 &= 0 \\ -3x_1 - 2x_2 + 4x_3 &= 0 \\ 6x_1 + x_2 - 8x_3 &= 0 \end{aligned}$$

1. **寫增廣矩陣** $[\,A \;\; \mathbf{0}\,]$,化成梯形:$R_2 \leftarrow R_2 + R_1$、$R_3 \leftarrow R_3 - 2R_1$,再 $R_3 \leftarrow R_3 + 3R_2$:
   $$\left[\begin{array}{rrr|r} 3 & 5 & -4 & 0 \\ -3 & -2 & 4 & 0 \\ 6 & 1 & -8 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 3 & 5 & -4 & 0 \\ 0 & 3 & 0 & 0 \\ 0 & -9 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 3 & 5 & -4 & 0 \\ 0 & 3 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right]$$
2. **判斷**:pivot 在第 1、2 行,$x_3$ 是自由變數。有自由變數 → **有非平凡解**(每個不為 0 的 $x_3$ 都給一個)。
3. **要描述解集,繼續化到 RREF**:$R_2 \leftarrow \tfrac13 R_2$;$R_1 \leftarrow R_1 - 5R_2$;$R_1 \leftarrow \tfrac13 R_1$:
   $$\left[\begin{array}{rrr|r} 1 & 0 & -\tfrac43 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right] \qquad \begin{aligned} x_1 - \tfrac43 x_3 &= 0 \\ x_2 &= 0 \end{aligned}$$
4. **解出基本變數**:$x_1 = \tfrac43 x_3$,$x_2 = 0$,$x_3$ 自由。
5. **寫成向量,把 $x_3$ 提出來**:
   $$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} \tfrac43 x_3 \\ 0 \\ x_3 \end{bmatrix} = x_3\begin{bmatrix} \tfrac43 \\ 0 \\ 1 \end{bmatrix} = x_3\mathbf{v}, \qquad \text{where } \mathbf{v} = \begin{bmatrix} \tfrac43 \\ 0 \\ 1 \end{bmatrix}.$$
6. **幾何**:每個解都是 $\mathbf{v}$ 的倍數,解集是 $\operatorname{Span}\{\mathbf{v}\}$——ℝ³ 中通過原點的一條直線。$x_3 = 0$ 給出平凡解。
7. **驗算**:$A\mathbf{v} = (3 \cdot \tfrac43 - 4,\; -3 \cdot \tfrac43 + 4,\; 6 \cdot \tfrac43 - 8) = (0, 0, 0)$ ✓。注意非平凡解 $\mathbf{v}$ 裡有一個分量是 0,這沒關係,只要**不是全部**為 0。

### 例 2 · Lay 1.5 Example 2
A single linear equation can be treated as a very simple system of equations. Describe all solutions of the homogeneous "system"

$$10x_1 - 3x_2 - 2x_3 = 0$$

1. **不用寫矩陣**:只有一條方程式,第一個係數 10 就是 pivot。$x_1$ 是基本變數,$x_2$、$x_3$ 都是自由變數。
2. **解出基本變數**:$x_1 = .3x_2 + .2x_3$。
3. **寫成向量**:
   $$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} .3x_2 + .2x_3 \\ x_2 \\ x_3 \end{bmatrix}$$
4. **依自由變數拆成兩個向量**,把含 $x_2$ 的放一起、含 $x_3$ 的放一起:
   $$\mathbf{x} = \begin{bmatrix} .3x_2 \\ x_2 \\ 0 \end{bmatrix} + \begin{bmatrix} .2x_3 \\ 0 \\ x_3 \end{bmatrix} = x_2\begin{bmatrix} .3 \\ 1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} .2 \\ 0 \\ 1 \end{bmatrix} = x_2\mathbf{u} + x_3\mathbf{v}.$$
5. **幾何**:解集是 $\operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$。$\mathbf{u}$、$\mathbf{v}$ 不是彼此的倍數,所以這是 ℝ³ 中通過原點的**平面**。
6. **對照**:原本的方程式 $10x_1 - 3x_2 - 2x_3 = 0$ 是平面的**隱式**描述(給一個點,代進去檢查);$\mathbf{x} = x_2\mathbf{u} + x_3\mathbf{v}$ 是**顯式**描述(直接列出平面上所有點)。下一個觀念會正式命名。

#### 備註
第 4 步「依自由變數拆開」是這週最常用的一招,學生第一次會卡在「為什麼可以拆」。提醒他們:這只是向量加法反過來寫,每個分量都是兩項相加。

## 易錯點
- 以為「有平凡解」就代表「有非平凡解」。平凡解**永遠**存在,要問的是有沒有**別的**解(是非題 Exercise 31)。
- 以為非平凡解的每個分量都不能是 0。只要**不全為** 0 就好(是非題 Exercise 28)。
- 寫一般解時漏掉自由變數本身那一列,例如忘了寫 $x_3 = x_3$,向量少一個分量。
- 自由變數所在的行全是 0 時(例如 Exercise 11 的 $x_4$),忘了它也是自由變數。

## 教學提示
開場先問:「右邊全是 0 的方程組,可能無解嗎?」讓學生自己說出「全填 0 就是解」,再追問「還有沒有別的?」。

例 2 的第 4 步「依自由變數拆開」要慢慢做,黑板上用兩種顏色標出含 $x_2$ 和含 $x_3$ 的項。這一招下一個觀念、下週都會一直用。

課堂建議做:Exercises 1–2、5;是非 Exercises 27、28、31、32;Exercises 7 與 11(提醒 $x_4$ 的陷阱)。

## 練習
### 照做 · Lay 1.5 Exercises 1–4
Determine if the system has a nontrivial solution. Try to use as few row operations as possible.

(1) $\begin{aligned} 2x_1 - 5x_2 + 8x_3 &= 0 \\ -2x_1 - 7x_2 + x_3 &= 0 \\ 4x_1 + 2x_2 + 7x_3 &= 0 \end{aligned}$  (2) $\begin{aligned} x_1 - 3x_2 + 7x_3 &= 0 \\ -2x_1 + x_2 - 4x_3 &= 0 \\ x_1 + 2x_2 + 9x_3 &= 0 \end{aligned}$

(3) $\begin{aligned} -3x_1 + 5x_2 - 7x_3 &= 0 \\ -6x_1 + 7x_2 + x_3 &= 0 \end{aligned}$  (4) $\begin{aligned} -5x_1 + 7x_2 + 9x_3 &= 0 \\ x_1 - 2x_2 + 6x_3 &= 0 \end{aligned}$

#### 解答
右邊全是 0,只化簡係數矩陣就好,化到梯形就能數自由變數。

(1) $R_2 \leftarrow R_2 + R_1$、$R_3 \leftarrow R_3 - 2R_1$,再 $R_3 \leftarrow R_3 + R_2$:
$$\begin{bmatrix} 2 & -5 & 8 \\ -2 & -7 & 1 \\ 4 & 2 & 7 \end{bmatrix} \sim \begin{bmatrix} 2 & -5 & 8 \\ 0 & -12 & 9 \\ 0 & 12 & -9 \end{bmatrix} \sim \begin{bmatrix} 2 & -5 & 8 \\ 0 & -12 & 9 \\ 0 & 0 & 0 \end{bmatrix}$$
只有兩個 pivot,$x_3$ 自由 → **有**非平凡解(書後解答相同)。例如 $\mathbf{x} = (-17, 6, 8)$。

(2) $R_2 \leftarrow R_2 + 2R_1$、$R_3 \leftarrow R_3 - R_1$,再 $R_3 \leftarrow R_3 + R_2$,得 $\begin{bmatrix} 1 & -3 & 7 \\ 0 & -5 & 10 \\ 0 & 0 & 12 \end{bmatrix}$。三個 pivot,沒有自由變數 → **只有**平凡解。

(3) $R_2 \leftarrow R_2 - 2R_1$ 得 $\begin{bmatrix} -3 & 5 & -7 \\ 0 & -3 & 15 \end{bmatrix}$,$x_3$ 自由 → **有**非平凡解(書後解答相同),例如 $(6, 5, 1)$。

(4) **不用化簡**:2 條方程式、3 個未知數,最多 2 個 pivot,一定至少有一個自由變數 → **有**非平凡解,例如 $(20, 13, 1)$。

#### 備註
(3)(4) 是「方程式比未知數少」的齊次方程組,一定有非平凡解。這是觀念 5 Theorem 8 的伏筆。

### 照做 · Lay 1.5 Exercises 5–6
Follow the method of Examples 1 and 2 to write the solution set of the given homogeneous system in parametric vector form.

(5) $\begin{aligned} x_1 + 3x_2 + x_3 &= 0 \\ -4x_1 - 9x_2 + 2x_3 &= 0 \\ -3x_2 - 6x_3 &= 0 \end{aligned}$  (6) $\begin{aligned} x_1 + 3x_2 - 5x_3 &= 0 \\ x_1 + 4x_2 - 8x_3 &= 0 \\ -3x_1 - 7x_2 + 9x_3 &= 0 \end{aligned}$

#### 解答
(5) 化簡增廣矩陣:

$$\left[\begin{array}{rrr|r} 1 & 3 & 1 & 0 \\ -4 & -9 & 2 & 0 \\ 0 & -3 & -6 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 3 & 1 & 0 \\ 0 & 3 & 6 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 0 & -5 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right]$$

$x_1 = 5x_3$、$x_2 = -2x_3$、$x_3$ 自由,所以 $\mathbf{x} = x_3\begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix}$:通過原點的直線(書後解答相同)。

(6) $R_2 \leftarrow R_2 - R_1$、$R_3 \leftarrow R_3 + 3R_1$,再 $R_3 \leftarrow R_3 - 2R_2$,化到 RREF $\begin{bmatrix} 1 & 0 & 4 \\ 0 & 1 & -3 \\ 0 & 0 & 0 \end{bmatrix}$。$x_1 = -4x_3$、$x_2 = 3x_3$,所以 $\mathbf{x} = x_3\begin{bmatrix} -4 \\ 3 \\ 1 \end{bmatrix}$。

### 是非 · Lay 1.5 Exercise 27
**(T/F)** A homogeneous equation is always consistent.

#### 解答
**True.** $\mathbf{x} = \mathbf{0}$(平凡解)永遠滿足 $A\mathbf{x} = \mathbf{0}$。

### 是非 · Lay 1.5 Exercise 28
**(T/F)** If $\mathbf{x}$ is a nontrivial solution of $A\mathbf{x} = \mathbf{0}$, then every entry in $\mathbf{x}$ is nonzero.

#### 解答
**False.** 非平凡解只要**有一個**分量不是 0。例 1 的 $\mathbf{v} = (\tfrac43, 0, 1)$ 就是一個有 0 分量的非平凡解。

### 是非 · Lay 1.5 Exercise 31
**(T/F)** The homogeneous equation $A\mathbf{x} = \mathbf{0}$ has the trivial solution if and only if the equation has at least one free variable.

#### 解答
**False.** 平凡解**永遠**存在;「⇔ 至少一個自由變數」是**非平凡解**的條件。例如 $I_2\mathbf{x} = \mathbf{0}$ 沒有自由變數,照樣有平凡解。

### 是非 · Lay 1.5 Exercise 32
**(T/F)** The equation $A\mathbf{x} = \mathbf{b}$ is homogeneous if the zero vector is a solution.

#### 解答
**True.** 若 $\mathbf{0}$ 是解,則 $\mathbf{b} = A\mathbf{0} = \mathbf{0}$,方程式就是 $A\mathbf{x} = \mathbf{0}$。

### 變化 · Lay 1.5 Exercises 7–8
Describe all solutions of $A\mathbf{x} = \mathbf{0}$ in parametric vector form, where $A$ is row equivalent to the given matrix.

(7) $\begin{bmatrix} 1 & 3 & -3 & 7 \\ 0 & 1 & -4 & 5 \end{bmatrix}$  (8) $\begin{bmatrix} 1 & -2 & -9 & 5 \\ 0 & 1 & 2 & -6 \end{bmatrix}$

#### 解答
題目給的是**係數矩陣**的等價矩陣(右邊的 0 省略了)。先化到 RREF。

(7) $R_1 \leftarrow R_1 - 3R_2$ 得 $\begin{bmatrix} 1 & 0 & 9 & -8 \\ 0 & 1 & -4 & 5 \end{bmatrix}$,所以 $x_1 = -9x_3 + 8x_4$、$x_2 = 4x_3 - 5x_4$,$x_3, x_4$ 自由:
$$\mathbf{x} = x_3\begin{bmatrix} -9 \\ 4 \\ 1 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} 8 \\ -5 \\ 0 \\ 1 \end{bmatrix}$$
(書後解答相同)。

(8) $R_1 \leftarrow R_1 + 2R_2$ 得 $\begin{bmatrix} 1 & 0 & -5 & -7 \\ 0 & 1 & 2 & -6 \end{bmatrix}$,所以 $x_1 = 5x_3 + 7x_4$、$x_2 = -2x_3 + 6x_4$:
$$\mathbf{x} = x_3\begin{bmatrix} 5 \\ -2 \\ 1 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} 7 \\ 6 \\ 0 \\ 1 \end{bmatrix}$$

### 變化 · Lay 1.5 Exercises 9–10
Describe all solutions of $A\mathbf{x} = \mathbf{0}$ in parametric vector form, where $A$ is row equivalent to the given matrix.

(9) $\begin{bmatrix} 2 & -8 & 6 \\ -1 & 4 & -3 \end{bmatrix}$  (10) $\begin{bmatrix} 1 & 3 & 0 & -4 \\ 2 & 6 & 0 & -8 \end{bmatrix}$

#### 解答
(9) 第 1 列是第 2 列的 $-2$ 倍,RREF 是 $\begin{bmatrix} 1 & -4 & 3 \\ 0 & 0 & 0 \end{bmatrix}$:$x_1 = 4x_2 - 3x_3$,$x_2, x_3$ 自由:
$$\mathbf{x} = x_2\begin{bmatrix} 4 \\ 1 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} -3 \\ 0 \\ 1 \end{bmatrix}$$
通過原點的平面(書後解答相同)。

(10) $R_2 \leftarrow R_2 - 2R_1$ 得全 0 列,RREF 是 $\begin{bmatrix} 1 & 3 & 0 & -4 \\ 0 & 0 & 0 & 0 \end{bmatrix}$:$x_1 = -3x_2 + 4x_4$,$x_2, x_3, x_4$ 都自由:
$$\mathbf{x} = x_2\begin{bmatrix} -3 \\ 1 \\ 0 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} 0 \\ 0 \\ 1 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} 4 \\ 0 \\ 0 \\ 1 \end{bmatrix}$$

#### 備註
(10) 的第三行全是 0,$x_3$ 不出現在任何方程式裡,但它仍然是自由變數,一般解要寫出 $x_3$ 那一項。

### 變化 · Lay 1.5 Exercises 11–12
Describe all solutions of $A\mathbf{x} = \mathbf{0}$ in parametric vector form, where $A$ is row equivalent to the given matrix.

(11) $\begin{bmatrix} 1 & -4 & -2 & 0 & 3 & -5 \\ 0 & 0 & 1 & 0 & 0 & -1 \\ 0 & 0 & 0 & 0 & 1 & -4 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$  (12) $\begin{bmatrix} 1 & 5 & 2 & -6 & 9 & 0 \\ 0 & 0 & 1 & -7 & 4 & -8 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

#### 解答
(11) 先化到 RREF($R_1 \leftarrow R_1 + 2R_2 - 3R_3$):
$$\begin{bmatrix} 1 & -4 & 0 & 0 & 0 & 5 \\ 0 & 0 & 1 & 0 & 0 & -1 \\ 0 & 0 & 0 & 0 & 1 & -4 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$$
基本變數 $x_1, x_3, x_5$;自由變數 $x_2, x_4, x_6$。$x_1 = 4x_2 - 5x_6$、$x_3 = x_6$、$x_5 = 4x_6$:
$$\mathbf{x} = x_2\begin{bmatrix} 4 \\ 1 \\ 0 \\ 0 \\ 0 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \\ 0 \\ 0 \end{bmatrix} + x_6\begin{bmatrix} -5 \\ 0 \\ 1 \\ 0 \\ 4 \\ 1 \end{bmatrix}$$
(書後解答給的是 RREF 對應的方程組,並提醒基本變數是 $x_1, x_3, x_5$。)

(12) $R_2 \leftarrow R_2 + 8R_3$,再 $R_1 \leftarrow R_1 - 2R_2$,得 RREF
$$\begin{bmatrix} 1 & 5 & 0 & 8 & 1 & 0 \\ 0 & 0 & 1 & -7 & 4 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$$
基本變數 $x_1, x_3, x_6$;$x_1 = -5x_2 - 8x_4 - x_5$、$x_3 = 7x_4 - 4x_5$、$x_6 = 0$:
$$\mathbf{x} = x_2\begin{bmatrix} -5 \\ 1 \\ 0 \\ 0 \\ 0 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} -8 \\ 0 \\ 7 \\ 1 \\ 0 \\ 0 \end{bmatrix} + x_5\begin{bmatrix} -1 \\ 0 \\ -4 \\ 0 \\ 1 \\ 0 \end{bmatrix}$$

#### 備註
書後解答只寫到「基本變數是 $x_1, x_3, x_5$,其餘是自由變數」,並說 Study Guide 討論了這類題常見的兩個錯,但沒有寫出是哪兩個。依經驗最常見的是:忘了 $x_4$ 是自由變數(它的行全是 0),以及 (12) 忘了 $x_6 = 0$ 也要寫進向量。

### 變化 · Lay 1.5 Exercises 13–16
You may find it helpful to review the information in the Reasonable Answers box from this section before answering Exercises 13–16. (13) Verify that the solutions you found to Exercise 9 are indeed homogeneous solutions. (14) Verify that the solutions you found to Exercise 10 are indeed homogeneous solutions. (15) Verify that the solutions you found to Exercise 11 are indeed homogeneous solutions. (16) Verify that the solutions you found to Exercise 12 are indeed homogeneous solutions.

#### 解答
方法(課本 Reasonable Answers):把矩陣乘上一般解裡的**每一個**向量,都要得到 $\mathbf{0}$;再用 $A\mathbf{x}$ 的線性性質(上週的 Theorem 5)推到整個組合。

(13) $A = \begin{bmatrix} 2 & -8 & 6 \\ -1 & 4 & -3 \end{bmatrix}$:$A\begin{bmatrix} 4 \\ 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 8 - 8 \\ -4 + 4 \end{bmatrix} = \mathbf{0}$,$A\begin{bmatrix} -3 \\ 0 \\ 1 \end{bmatrix} = \begin{bmatrix} -6 + 6 \\ 3 - 3 \end{bmatrix} = \mathbf{0}$。所以 $A(x_2\mathbf{u} + x_3\mathbf{v}) = x_2A\mathbf{u} + x_3A\mathbf{v} = \mathbf{0}$(書後解答相同)。

(14) $A(-3, 1, 0, 0) = (-3 + 3,\ -6 + 6) = \mathbf{0}$;$A(0, 0, 1, 0) = \mathbf{0}$(第三行全是 0);$A(4, 0, 0, 1) = (4 - 4,\ 8 - 8) = \mathbf{0}$。

(15) 矩陣乘上 $(4, 1, 0, 0, 0, 0)$、$(0, 0, 0, 1, 0, 0)$、$(-5, 0, 1, 0, 4, 1)$ 都得到 $\mathbf{0}$。例如第三個:第 1 列 $-5 - 2 + 12 - 5 = 0$、第 2 列 $1 - 1 = 0$、第 3 列 $4 - 4 = 0$。

(16) 矩陣乘上 $(-5, 1, 0, 0, 0, 0)$、$(-8, 0, 7, 1, 0, 0)$、$(-1, 0, -4, 0, 1, 0)$ 都得到 $\mathbf{0}$。例如第二個:第 1 列 $-8 + 14 - 6 = 0$、第 2 列 $7 - 7 = 0$。

#### 備註
注意驗算要用**原本的**矩陣(題目給的那個),不是 RREF——兩者列等價、解集相同,用哪個都對,但用原矩陣才抓得到化簡時算錯的地方。

### 變化 · Lay 1.5 Exercise 39
Suppose $A$ is the $3 \times 3$ *zero* matrix (with all zero entries). Describe the solution set of the equation $A\mathbf{x} = \mathbf{0}$.

#### 解答
每個 $\mathbf{x}$ 都滿足 $0\mathbf{x} = \mathbf{0}$(三個變數全是自由變數),解集是**整個** ℝ³(書後解答相同)。用參數式寫就是 $x_1\mathbf{e}_1 + x_2\mathbf{e}_2 + x_3\mathbf{e}_3$。

### 變化 · Lay 1.5 Exercises 45–46
Find one nontrivial solution of $A\mathbf{x} = \mathbf{0}$ by inspection. [*Hint:* Think of the equation $A\mathbf{x} = \mathbf{0}$ written as a vector equation.]

(45) $A = \begin{bmatrix} -2 & -6 \\ 7 & 21 \\ -3 & -9 \end{bmatrix}$  (46) $A = \begin{bmatrix} 4 & -6 \\ -8 & 12 \\ 6 & -9 \end{bmatrix}$

#### 解答
(45) 第二行是第一行的 3 倍:$\mathbf{a}_2 = 3\mathbf{a}_1$,移項得 $3\mathbf{a}_1 - \mathbf{a}_2 = \mathbf{0}$,所以 $\mathbf{x} = \begin{bmatrix} 3 \\ -1 \end{bmatrix}$(書後解答相同;它的任何非零倍數也對)。

(46) 第二行是第一行的 $-\tfrac32$ 倍,也就是 $3\mathbf{a}_1 + 2\mathbf{a}_2 = \mathbf{0}$,所以 $\mathbf{x} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$。

### 挑戰 · Lay 1.5 Exercises 47–48
(47) Construct a $3 \times 3$ nonzero matrix $A$ such that the vector $\begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$ is a solution of $A\mathbf{x} = \mathbf{0}$. (48) Construct a $3 \times 3$ nonzero matrix $A$ such that the vector $\begin{bmatrix} 1 \\ -2 \\ 1 \end{bmatrix}$ is a solution of $A\mathbf{x} = \mathbf{0}$.

#### 解答
(47) $A(1, 1, 1)$ 的每個分量就是 $A$ 那一列的**列和**,所以只要每一列加起來是 0 就行(書後解答的提示)。例如 $A = \begin{bmatrix} 1 & -1 & 0 \\ 0 & 1 & -1 \\ 1 & 0 & -1 \end{bmatrix}$。

(48) 每一列 $(r_1, r_2, r_3)$ 要滿足 $r_1 - 2r_2 + r_3 = 0$。例如 $A = \begin{bmatrix} 1 & 1 & 1 \\ 2 & 1 & 0 \\ 0 & 1 & 2 \end{bmatrix}$;更簡單的是每一列都取 $(1, 1, 1)$。

### 挑戰 · Lay 1.5 Exercises 51–52
(51) Let $A$ be an $m \times n$ matrix and let $\mathbf{u}$ be a vector in $\mathbb{R}^n$ that satisfies the equation $A\mathbf{x} = \mathbf{0}$. Show that for any scalar $c$, the vector $c\mathbf{u}$ also satisfies $A\mathbf{x} = \mathbf{0}$. [That is, show that $A(c\mathbf{u}) = \mathbf{0}$.]

(52) Let $A$ be an $m \times n$ matrix, and let $\mathbf{u}$ and $\mathbf{v}$ be vectors in $\mathbb{R}^n$ with the property that $A\mathbf{u} = \mathbf{0}$ and $A\mathbf{v} = \mathbf{0}$. Explain why $A(\mathbf{u} + \mathbf{v})$ must be the zero vector. Then explain why $A(c\mathbf{u} + d\mathbf{v}) = \mathbf{0}$ for each pair of scalars $c$ and $d$.

#### 解答
(51) 由上週的 Theorem 5(b):$A(c\mathbf{u}) = c(A\mathbf{u}) = c\mathbf{0} = \mathbf{0}$(書後解答相同)。

(52) 由 Theorem 5(a):$A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v} = \mathbf{0} + \mathbf{0} = \mathbf{0}$。再合併 (a)(b):$A(c\mathbf{u} + d\mathbf{v}) = cA\mathbf{u} + dA\mathbf{v} = c\mathbf{0} + d\mathbf{0} = \mathbf{0}$。

#### 備註
兩題合起來說的是:**齊次方程組的解,任意線性組合還是解**。這就是為什麼它的解集一定是一個 Span,也是第 7 週「零空間(Nul $A$)是子空間」的核心。

## 驗算
```check
Matrix([[3, 5, -4], [-3, -2, 4], [6, 1, -8]]).rref()[0] == Matrix([[1, 0, Rational(-4, 3)], [0, 1, 0], [0, 0, 0]])
Matrix([[3, 5, -4], [-3, -2, 4], [6, 1, -8]]) * Matrix([Rational(4, 3), 0, 1]) == zeros(3, 1)
Matrix([[10, -3, -2]]).nullspace() == [Matrix([Rational(3, 10), 1, 0]), Matrix([Rational(1, 5), 0, 1])]
Matrix([[2, -5, 8], [-2, -7, 1], [4, 2, 7]]).rref()[1] == (0, 1)
Matrix([[2, -5, 8], [-2, -7, 1], [4, 2, 7]]) * Matrix([-17, 6, 8]) == zeros(3, 1)
Matrix([[1, -3, 7], [-2, 1, -4], [1, 2, 9]]).nullspace() == []
Matrix([[-3, 5, -7], [-6, 7, 1]]) * Matrix([6, 5, 1]) == zeros(2, 1)
Matrix([[-5, 7, 9], [1, -2, 6]]) * Matrix([20, 13, 1]) == zeros(2, 1)
Matrix([[1, 3, 1], [-4, -9, 2], [0, -3, -6]]).nullspace() == [Matrix([5, -2, 1])]
Matrix([[1, 3, -5], [1, 4, -8], [-3, -7, 9]]).nullspace() == [Matrix([-4, 3, 1])]
Matrix([[1, 3, -3, 7], [0, 1, -4, 5]]).nullspace() == [Matrix([-9, 4, 1, 0]), Matrix([8, -5, 0, 1])]
Matrix([[1, -2, -9, 5], [0, 1, 2, -6]]).nullspace() == [Matrix([5, -2, 1, 0]), Matrix([7, 6, 0, 1])]
Matrix([[2, -8, 6], [-1, 4, -3]]).nullspace() == [Matrix([4, 1, 0]), Matrix([-3, 0, 1])]
Matrix([[1, 3, 0, -4], [2, 6, 0, -8]]).nullspace() == [Matrix([-3, 1, 0, 0]), Matrix([0, 0, 1, 0]), Matrix([4, 0, 0, 1])]
Matrix([[1, -4, -2, 0, 3, -5], [0, 0, 1, 0, 0, -1], [0, 0, 0, 0, 1, -4], [0, 0, 0, 0, 0, 0]]).nullspace() == [Matrix([4, 1, 0, 0, 0, 0]), Matrix([0, 0, 0, 1, 0, 0]), Matrix([-5, 0, 1, 0, 4, 1])]
Matrix([[1, 5, 2, -6, 9, 0], [0, 0, 1, -7, 4, -8], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]).nullspace() == [Matrix([-5, 1, 0, 0, 0, 0]), Matrix([-8, 0, 7, 1, 0, 0]), Matrix([-1, 0, -4, 0, 1, 0])]
(Matrix([[2, -8, 6], [-1, 4, -3]]) * (x2 * Matrix([4, 1, 0]) + x3 * Matrix([-3, 0, 1]))).expand() == zeros(2, 1)
len(zeros(3, 3).nullspace()) == 3
Matrix([[-2, -6], [7, 21], [-3, -9]]) * Matrix([3, -1]) == zeros(3, 1)
Matrix([[4, -6], [-8, 12], [6, -9]]) * Matrix([3, 2]) == zeros(3, 1)
Matrix([[1, -1, 0], [0, 1, -1], [1, 0, -1]]) * Matrix([1, 1, 1]) == zeros(3, 1)
Matrix([[1, 1, 1], [2, 1, 0], [0, 1, 2]]) * Matrix([1, -2, 1]) == zeros(3, 1)
(Matrix([[a, b], [c, d]]) * (h * Matrix([x1, x2]) + k * Matrix([x3, x4])) - h * (Matrix([[a, b], [c, d]]) * Matrix([x1, x2])) - k * (Matrix([[a, b], [c, d]]) * Matrix([x3, x4]))).expand() == zeros(2, 1)
```
