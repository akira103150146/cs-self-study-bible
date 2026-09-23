---
title_en: When Does Ax = b Have a Solution for Every b?
title_zh: 何時每個 b 都有解:Theorem 4 與 Ax 的線性性質
sub: Look for a pivot in every row of the coefficient matrix
level: hard
source: Lay 1.4
lab_hook: "`len(Matrix(A).rref()[1]) == A.shape[0]`:pivot 個數是否等於列數"
---
## 觀念
The sentence "the columns of $A$ span $\mathbb{R}^m$" means that *every* $\mathbf{b}$ in $\mathbb{R}^m$ is a linear combination of the columns of $A$. In general, a set of vectors $\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ in $\mathbb{R}^m$ **spans** (or **generates**) $\mathbb{R}^m$ if every vector in $\mathbb{R}^m$ is a linear combination of $\mathbf{v}_1, \dots, \mathbf{v}_p$ — that is, if $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\} = \mathbb{R}^m$.

**Theorem 4.** Let $A$ be an $m \times n$ matrix. Then the following statements are logically equivalent. That is, for a particular $A$, either they are all true statements or they are all false.

- **a.** For each $\mathbf{b}$ in $\mathbb{R}^m$, the equation $A\mathbf{x} = \mathbf{b}$ has a solution.
- **b.** Each $\mathbf{b}$ in $\mathbb{R}^m$ is a linear combination of the columns of $A$.
- **c.** The columns of $A$ span $\mathbb{R}^m$.
- **d.** $A$ has a pivot position in every row.

*Warning:* Theorem 4 is about a **coefficient matrix**, not an augmented matrix. If an augmented matrix $[\,A \;\; \mathbf{b}\,]$ has a pivot position in every row, then the equation $A\mathbf{x} = \mathbf{b}$ may or may not be consistent.

**Theorem 5.** If $A$ is an $m \times n$ matrix, $\mathbf{u}$ and $\mathbf{v}$ are vectors in $\mathbb{R}^n$, and $c$ is a scalar, then:

- **a.** $A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}$;
- **b.** $A(c\mathbf{u}) = c(A\mathbf{u})$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| span $\mathbb{R}^m$ | 生成 ℝᵐ | 這些向量的 Span 就是整個 ℝᵐ,每個向量都組合得出來 |
| logically equivalent | 邏輯等價 | 幾句話「同真同假」:一句成立,全部成立 |
| pivot position in every row | 每一列都有 pivot | Theorem 4 的 (d),用列化簡就能檢查 |
| coefficient matrix vs augmented matrix | 係數矩陣 vs 增廣矩陣 | Theorem 4 只講**係數矩陣** $A$ |
| linearity | 線性性質 | Theorem 5:$A$ 對加法、純量倍數「可以分開算」 |

## 白話說
上一個觀念問「**這個** $\mathbf{b}$ 有沒有解」。這個觀念問更強的問題:「**每一個** $\mathbf{b}$ 都有解嗎?」

Theorem 4 說,下面四句話是同一件事,只要檢查最容易的第 (d) 句:

- (a) 每個 $\mathbf{b}$,$A\mathbf{x} = \mathbf{b}$ 都有解。
- (b) 每個 $\mathbf{b}$ 都能由 $A$ 的行組合出來。
- (c) $A$ 的行生成整個 ℝᵐ。
- (d) **$A$ 的每一列都有 pivot。** ← 化簡一次就知道

直覺:如果 $A$ 化簡後有一列全是 0,那麼只要挑一個 $\mathbf{b}$ 讓那一列右邊不是 0,就會出現「$0 = $ 非零數」,無解。反過來,每一列都有 pivot 時,右邊不管是什麼都不會矛盾。

**立刻可以用的推論**:$A$ 的**行數比列數少**(例如 $3 \times 2$)時,pivot 最多和行數一樣多,不可能每一列都有——所以這種 $A$ 的行**不可能生成** ℝᵐ。

Theorem 5 則是 $A\mathbf{x}$ 最重要的性質:**先加再乘 = 先乘再加**,**先放大再乘 = 先乘再放大**。這個性質叫「線性」,是第 4 週線性變換的定義來源。

## 幾何意義
課本 Example 3 的 $A$ 是 $3 \times 3$,但化簡後只有 2 個 pivot。它的三行只張成 ℝ³ 裡的一個**平面**(滿足 $b_1 - \tfrac12 b_2 + b_3 = 0$ 的那些點)。$\mathbf{b}$ 在平面上就有解,不在就無解——所以不是每個 $\mathbf{b}$ 都有解。

「$A$ 的行生成 ℝᵐ」在幾何上就是「$A$ 的行張出的空間塞滿整個 ℝᵐ」,沒有漏掉任何方向。

## 在資工哪裡用
- **機器學習的輸出層**:一個線性層 $W\mathbf{x}$ 能不能產生**任意**的目標輸出?就是問 $W$ 的行能不能生成輸出空間,也就是 $W$ 的每一列有沒有 pivot。輸出維度比輸入維度大時(行比列少),一定做不到。
- **控制與機器人**:「用這幾個馬達(行向量),能不能把機械手臂推到任何位置(每個 $\mathbf{b}$)?」就是 Theorem 4。
- **Theorem 5 = 疊加原理,讓大問題可以拆開算**:$A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}$,所以一個很大的輸入可以切成幾段($\mathbf{x} = \mathbf{x}_1 + \mathbf{x}_2 + \cdots$,每段只留自己那幾個分量、其餘補 0),各台機器算自己那一段的 $A\mathbf{x}_i$,最後**加起來**就是答案。這正是分散式矩陣乘向量的做法。訊號處理也用同一招:輸入訊號拆成幾個成分,各自算出反應再相加。

## 原理
**Theorem 4 的 (a)(b)(c) 為什麼等價?** 依 $A\mathbf{x}$ 的定義,「$A\mathbf{x} = \mathbf{b}$ 有解」⇔「$\mathbf{b}$ 是 $A$ 各行的線性組合」,所以 (a)⇔(b)。(b)⇔(c) 則是「生成 ℝᵐ」的定義。

**(a)⇔(d)** 是本週的證明時刻(接在本觀念後面)。

**Theorem 5 的證明**(課本 p. 65,$n = 3$ 的情形,一般情形相同):見例 2。

**Warning 的反例**:$[\,A \;\; \mathbf{b}\,] = \left[\begin{array}{rr|r} 1 & 0 & 0 \\ 0 & 0 & 1 \end{array}\right]$ 每一列都有 pivot,但第二列是 $0 = 1$,無解。增廣矩陣「每列都有 pivot」不保證有解;要看的是係數矩陣。

## 老師講解
### 例 1 · Lay 1.4 Example 3
Let $A = \begin{bmatrix} 1 & 3 & 4 \\ -4 & 2 & -6 \\ -3 & -2 & -7 \end{bmatrix}$ and $\mathbf{b} = \begin{bmatrix} b_1 \\ b_2 \\ b_3 \end{bmatrix}$. Is the equation $A\mathbf{x} = \mathbf{b}$ consistent for all possible $b_1, b_2, b_3$?

1. **把 $\mathbf{b}$ 留成符號**,照樣化簡增廣矩陣。$R_2 \leftarrow R_2 + 4R_1$、$R_3 \leftarrow R_3 + 3R_1$:
   $$\left[\begin{array}{rrr|l} 1 & 3 & 4 & b_1 \\ -4 & 2 & -6 & b_2 \\ -3 & -2 & -7 & b_3 \end{array}\right] \sim \left[\begin{array}{rrr|l} 1 & 3 & 4 & b_1 \\ 0 & 14 & 10 & b_2 + 4b_1 \\ 0 & 7 & 5 & b_3 + 3b_1 \end{array}\right]$$
2. **再消第三列**:$R_3 \leftarrow R_3 - \tfrac12 R_2$,係數部分 $7 - 7 = 0$、$5 - 5 = 0$ 全消掉了:
   $$\sim \left[\begin{array}{rrr|l} 1 & 3 & 4 & b_1 \\ 0 & 14 & 10 & b_2 + 4b_1 \\ 0 & 0 & 0 & b_3 + 3b_1 - \tfrac12(b_2 + 4b_1) \end{array}\right]$$
3. **整理最後一格**:$b_3 + 3b_1 - \tfrac12 b_2 - 2b_1 = b_1 - \tfrac12 b_2 + b_3$。
4. **判斷**:第三列左邊全是 0。只要選的 $\mathbf{b}$ 讓 $b_1 - \tfrac12 b_2 + b_3 \neq 0$(例如 $\mathbf{b} = (1, 0, 0)$),就得到 $0 = $ 非零數,無解。所以**不是**每個 $\mathbf{b}$ 都有解。
5. **有解的 $\mathbf{b}$ 長什麼樣?** 必須滿足 $b_1 - \tfrac12 b_2 + b_3 = 0$——這是 ℝ³ 中一個**通過原點的平面**,也就是 $A$ 三行的 Span。
6. **和 Theorem 4 對照**:失敗的原因是係數矩陣的 echelon form 有一整列 0(第三列沒有 pivot)。如果 $A$ 每一列都有 pivot,就根本不用管最後一行算出什麼。

### 例 2 · Lay 1.4 Theorem 5(p. 65 的證明)
Prove Theorem 5 for $n = 3$: if $A = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_3\,]$ and $\mathbf{u}, \mathbf{v}$ are in $\mathbb{R}^3$, then $A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}$ and $A(c\mathbf{u}) = c(A\mathbf{u})$.

1. **只用兩樣工具**:$A\mathbf{x}$ 的定義(行的線性組合),以及觀念 1 的向量運算律。
2. **(a)** $\mathbf{u} + \mathbf{v}$ 的分量是 $u_i + v_i$,依定義把它們當權重:
   $$A(\mathbf{u} + \mathbf{v}) = (u_1 + v_1)\mathbf{a}_1 + (u_2 + v_2)\mathbf{a}_2 + (u_3 + v_3)\mathbf{a}_3.$$
3. 用分配律拆開、再重新分組:
   $$= (u_1\mathbf{a}_1 + u_2\mathbf{a}_2 + u_3\mathbf{a}_3) + (v_1\mathbf{a}_1 + v_2\mathbf{a}_2 + v_3\mathbf{a}_3) = A\mathbf{u} + A\mathbf{v}.$$
4. **(b)** $c\mathbf{u}$ 的分量是 $cu_i$:
   $$A(c\mathbf{u}) = (cu_1)\mathbf{a}_1 + (cu_2)\mathbf{a}_2 + (cu_3)\mathbf{a}_3 = c(u_1\mathbf{a}_1 + u_2\mathbf{a}_2 + u_3\mathbf{a}_3) = c(A\mathbf{u}).$$
5. **意義**:Theorem 5 說 $\mathbf{x} \mapsto A\mathbf{x}$ 這個對應「保持加法與純量倍數」。第 4 週會把這種對應命名為**線性變換**。

## 易錯點
- 對**增廣矩陣** $[\,A \;\; \mathbf{b}\,]$ 數 pivot,然後用 Theorem 4。Theorem 4 只講**係數矩陣**(課本的 Warning,是非題 27、34)。
- 以為行數夠多(行數 $\ge$ 列數)就一定生成 ℝᵐ。行夠多只是**有機會**,還是要看每一列有沒有 pivot:Exercise 17 的 $4 \times 4$ 方陣行不比列少,只有 3 個 pivot,照樣不行。
- 問「$B$ 的行能不能生成 ℝ³」,但 $B$ 的行在 ℝ⁴ 裡——問題本身就不成立(Exercise 20)。
- 化簡時把 $b_1, b_2, b_3$ 的符號算錯。建議每一步都把 $\mathbf{b}$ 那一欄完整寫出來。

## 教學提示
Theorem 4 的四句話寫成一個框,整個學期會一直擴充(第 6 週的可逆矩陣定理)。**強調只有 (d) 是能「算」的**,其他三句都靠 (d) 來判斷。

例 1 一定要把 $b_1, b_2, b_3$ 帶著走完,並停在第 4 步問學生:「你能挑一個讓它無解的 $\mathbf{b}$ 嗎?」學生自己挑出 $(1, 0, 0)$,就真的懂了。

課堂建議做:Exercises 15、17–18;是非 Exercises 27、28、31、33、34(尤其 27、34);Exercises 41–42 很適合當討論題。T 題(Exercises 47–52)留給實作課。

## 練習
### 照做 · Lay 1.4 Exercises 15–16
(15) Let $A = \begin{bmatrix} 3 & -4 \\ -6 & 8 \end{bmatrix}$ and $\mathbf{b} = \begin{bmatrix} b_1 \\ b_2 \end{bmatrix}$. Show that the equation $A\mathbf{x} = \mathbf{b}$ does not have a solution for all possible $\mathbf{b}$, and describe the set of all $\mathbf{b}$ for which $A\mathbf{x} = \mathbf{b}$ *does* have a solution.

(16) Repeat Exercise 15: $A = \begin{bmatrix} 1 & -3 & -4 \\ -3 & 2 & 6 \\ 5 & -1 & -8 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} b_1 \\ b_2 \\ b_3 \end{bmatrix}$.

#### 解答
(15) $R_2 \leftarrow R_2 + 2R_1$:$[\,0 \;\; 0 \mid b_2 + 2b_1\,]$。只要 $2b_1 + b_2 \neq 0$ 就無解,所以不是每個 $\mathbf{b}$ 都有解。有解的 $\mathbf{b}$ 滿足 $b_2 = -2b_1$:**一條通過原點的直線**(書後解答相同)。

(16) $R_2 \leftarrow R_2 + 3R_1$ 得 $[\,0 \;\; {-7} \;\; {-6} \mid b_2 + 3b_1\,]$;$R_3 \leftarrow R_3 - 5R_1$ 得 $[\,0 \;\; 14 \;\; 12 \mid b_3 - 5b_1\,]$;$R_3 \leftarrow R_3 + 2R_2$ 得 $[\,0 \;\; 0 \;\; 0 \mid b_1 + 2b_2 + b_3\,]$。有解 ⇔ $b_1 + 2b_2 + b_3 = 0$:**一個通過原點的平面**。

### 照做 · Lay 1.4 Exercises 17–20
Exercises 17–20 refer to the matrices $A$ and $B$ below. Make appropriate calculations that justify your answers and mention an appropriate theorem.

$$A = \begin{bmatrix} 1 & 3 & 0 & 3 \\ -1 & -1 & -1 & 1 \\ 0 & -4 & 2 & -8 \\ 2 & 0 & 3 & -1 \end{bmatrix}, \qquad B = \begin{bmatrix} 1 & 3 & -2 & 2 \\ 0 & 1 & 1 & -5 \\ 1 & 2 & -3 & 7 \\ -2 & -8 & 2 & -1 \end{bmatrix}$$

(17) How many rows of $A$ contain a pivot position? Does the equation $A\mathbf{x} = \mathbf{b}$ have a solution for each $\mathbf{b}$ in $\mathbb{R}^4$? (18) Do the columns of $B$ span $\mathbb{R}^4$? Does the equation $B\mathbf{x} = \mathbf{y}$ have a solution for each $\mathbf{y}$ in $\mathbb{R}^4$? (19) Can each vector in $\mathbb{R}^4$ be written as a linear combination of the columns of the matrix $A$ above? Do the columns of $A$ span $\mathbb{R}^4$? (20) Can every vector in $\mathbb{R}^4$ be written as a linear combination of the columns of the matrix $B$ above? Do the columns of $B$ span $\mathbb{R}^3$?

#### 解答
(17) 化簡 $A$:$R_2 \leftarrow R_2 + R_1$ 得 $[\,0 \;\; 2 \;\; {-1} \;\; 4\,]$;$R_4 \leftarrow R_4 - 2R_1$ 得 $[\,0 \;\; {-6} \;\; 3 \;\; {-7}\,]$;$R_3 \leftarrow R_3 + 2R_2$ 得全 0;$R_4 \leftarrow R_4 + 3R_2$ 得 $[\,0 \;\; 0 \;\; 0 \;\; 5\,]$。交換第 3、4 列後是梯形,**只有 3 列有 pivot**。由 Theorem 4,$A\mathbf{x} = \mathbf{b}$ **不是**對每個 $\mathbf{b}$ 都有解(書後解答相同)。

(18) 化簡 $B$:$R_3 \leftarrow R_3 - R_1$ 得 $[\,0 \;\; {-1} \;\; {-1} \;\; 5\,]$;$R_4 \leftarrow R_4 + 2R_1$ 得 $[\,0 \;\; {-2} \;\; {-2} \;\; 3\,]$;$R_3 \leftarrow R_3 + R_2$ 得全 0;$R_4 \leftarrow R_4 + 2R_2$ 得 $[\,0 \;\; 0 \;\; 0 \;\; {-7}\,]$。同樣**只有 3 個 pivot**,所以 $B$ 的行**不能**生成 ℝ⁴,$B\mathbf{x} = \mathbf{y}$ 也**不是**對每個 $\mathbf{y}$ 都有解。

(19) 由 (17),Theorem 4 的 (d) 不成立,所以 (a)–(c) 全部不成立:**不是**每個向量都能寫成 $A$ 各行的組合,$A$ 的行**不能**生成 ℝ⁴(書後解答相同)。

(20) 由 (18),**不能**。後半題是陷阱:$B$ 的行是 **ℝ⁴** 的向量,根本不在 ℝ³ 裡,「生成 ℝ³」這個問題不成立。

#### 備註
Exercise 20 後半題很適合拿來討論「問題本身合不合理」。

### 是非 · Lay 1.4 Exercise 27
**(T/F)** The equation $A\mathbf{x} = \mathbf{b}$ is consistent if the augmented matrix $[\,A \;\; \mathbf{b}\,]$ has a pivot position in every row.

#### 解答
**False.** 課本 p. 64 的 Warning:增廣矩陣每列都有 pivot,可能是因為最後一行有 pivot(矛盾)。反例:$\left[\begin{array}{rr|r} 1 & 0 & 0 \\ 0 & 0 & 1 \end{array}\right]$。

### 是非 · Lay 1.4 Exercise 28
**(T/F)** If $A$ is an $m \times n$ matrix whose columns do not span $\mathbb{R}^m$, then the equation $A\mathbf{x} = \mathbf{b}$ is inconsistent for some $\mathbf{b}$ in $\mathbb{R}^m$.

#### 解答
**True.** Theorem 4:(c) 不成立 ⇔ (a) 不成立,也就是存在某個 $\mathbf{b}$ 使方程式無解。

### 是非 · Lay 1.4 Exercise 31
**(T/F)** If the columns of an $m \times n$ matrix $A$ span $\mathbb{R}^m$, then the equation $A\mathbf{x} = \mathbf{b}$ is consistent for each $\mathbf{b}$ in $\mathbb{R}^m$.

#### 解答
**True.** Theorem 4 的 (c) ⇒ (a)。

### 是非 · Lay 1.4 Exercise 33
**(T/F)** If $A$ is an $m \times n$ matrix and if the equation $A\mathbf{x} = \mathbf{b}$ is inconsistent for some $\mathbf{b}$ in $\mathbb{R}^m$, then $A$ cannot have a pivot position in every row.

#### 解答
**True.** 若 $A$ 每列都有 pivot,由 Theorem 4 每個 $\mathbf{b}$ 都有解;現在有某個 $\mathbf{b}$ 無解,所以 $A$ 不可能每列都有 pivot。

### 是非 · Lay 1.4 Exercise 34
**(T/F)** If the augmented matrix $[\,A \;\; \mathbf{b}\,]$ has a pivot position in every row, then the equation $A\mathbf{x} = \mathbf{b}$ is inconsistent.

#### 解答
**False.** 也可能相容。例如 $A = I_2$、$\mathbf{b} = (1, 1)$:$[\,I \;\; \mathbf{b}\,]$ 每列都有 pivot(在前兩行),方程式有解 $\mathbf{x} = (1, 1)$。要看的是 pivot 在不在**最後一行**。

### 變化 · Lay 1.4 Exercises 21–22
(21) Let $\mathbf{v}_1 = \begin{bmatrix} 1 \\ 0 \\ -1 \\ 0 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 0 \\ -1 \\ 0 \\ 1 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} 1 \\ 0 \\ 0 \\ -1 \end{bmatrix}$. Does $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ span $\mathbb{R}^4$? Why or why not?

(22) Let $\mathbf{v}_1 = \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 0 \\ -3 \\ 8 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} 4 \\ -1 \\ -5 \end{bmatrix}$. Does $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ span $\mathbb{R}^3$? Why or why not?

#### 解答
(21) **不能**。$[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]$ 是 $4 \times 3$ 矩陣,只有 3 行,最多 3 個 pivot,不可能 4 列都有 pivot。由 Theorem 4 不能生成 ℝ⁴(書後解答相同;這題**不用化簡**就能判斷)。

(22) **能**。$[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,] = \begin{bmatrix} 0 & 0 & 4 \\ 0 & -3 & -1 \\ -2 & 8 & -5 \end{bmatrix}$,交換第 1、3 列就成了梯形 $\begin{bmatrix} -2 & 8 & -5 \\ 0 & -3 & -1 \\ 0 & 0 & 4 \end{bmatrix}$,3 列都有 pivot,所以生成 ℝ³。

### 變化 · Lay 1.4 Practice Problem 2
Let $A = \begin{bmatrix} 2 & 5 \\ 3 & 1 \end{bmatrix}$, $\mathbf{u} = \begin{bmatrix} 4 \\ -1 \end{bmatrix}$, and $\mathbf{v} = \begin{bmatrix} -3 \\ 5 \end{bmatrix}$. Verify Theorem 5(a) in this case by computing $A(\mathbf{u} + \mathbf{v})$ and $A\mathbf{u} + A\mathbf{v}$.

#### 解答
$\mathbf{u} + \mathbf{v} = \begin{bmatrix} 1 \\ 4 \end{bmatrix}$,$A(\mathbf{u} + \mathbf{v}) = \begin{bmatrix} 2 + 20 \\ 3 + 4 \end{bmatrix} = \begin{bmatrix} 22 \\ 7 \end{bmatrix}$。

$A\mathbf{u} = \begin{bmatrix} 3 \\ 11 \end{bmatrix}$、$A\mathbf{v} = \begin{bmatrix} 19 \\ -4 \end{bmatrix}$,相加 $\begin{bmatrix} 22 \\ 7 \end{bmatrix}$。兩邊相同 ✓(課本 p. 69)。

### 變化 · Lay 1.4 Practice Problem 3
Construct a $3 \times 3$ matrix $A$ and vectors $\mathbf{b}$ and $\mathbf{c}$ in $\mathbb{R}^3$ so that $A\mathbf{x} = \mathbf{b}$ has a solution, but $A\mathbf{x} = \mathbf{c}$ does not.

#### 解答
要讓有些 $\mathbf{b}$ 有解、有些沒有,$A$ 就不能每列都有 pivot。直接取已經是 RREF、最後一列全 0 的矩陣最簡單:

$$A = \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 0 \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 3 \\ 2 \\ 0 \end{bmatrix}, \quad \mathbf{c} = \begin{bmatrix} 3 \\ 2 \\ 1 \end{bmatrix}.$$

$[\,A \;\; \mathbf{b}\,]$ 的最後一列是 $0 = 0$,有解;$[\,A \;\; \mathbf{c}\,]$ 的最後一列是 $0 = 1$,無解(課本 p. 69;答案不唯一)。

### 應用 · Lay 1.4 Exercises 47–50
**[T]** Determine if the columns of the matrix span $\mathbb{R}^4$.

(47) $\begin{bmatrix} 7 & 2 & -5 & 8 \\ -5 & -3 & 4 & -9 \\ 6 & 10 & -2 & 7 \\ -7 & 9 & 2 & 15 \end{bmatrix}$  (48) $\begin{bmatrix} 5 & -7 & -4 & 9 \\ 6 & -8 & -7 & 5 \\ 4 & -4 & -9 & -9 \\ -9 & 11 & 16 & 7 \end{bmatrix}$

(49) $\begin{bmatrix} 12 & -7 & 11 & -9 & 5 \\ -9 & 4 & -8 & 7 & -3 \\ -6 & 11 & -7 & 3 & -9 \\ 4 & -6 & 10 & -5 & 12 \end{bmatrix}$  (50) $\begin{bmatrix} 8 & 11 & -6 & -7 & 13 \\ -7 & -8 & 5 & 6 & -9 \\ 11 & 7 & -7 & -9 & -6 \\ -3 & 4 & 1 & 8 & 7 \end{bmatrix}$

#### 解答
用電腦化簡,數每一列有沒有 pivot:

- (47) 只有 3 個 pivot(第 1、2、3 行)→ **不能**生成 ℝ⁴(書後解答相同)。
- (48) 只有 3 個 pivot → **不能**。
- (49) 4 個 pivot(第 1、2、3、5 行)→ **能**(書後解答相同)。
- (50) 4 個 pivot(第 1、2、4、5 行)→ **能**。

#### 備註
課本標 T,實作課 ④ 用 `rref()` 做。

### 應用 · Lay 1.4 Exercises 51–52
**[T]** (51) Find a column of the matrix in Exercise 49 that can be deleted and yet have the remaining matrix columns still span $\mathbb{R}^4$. (52) Find a column of the matrix in Exercise 50 that can be deleted and yet have the remaining matrix columns still span $\mathbb{R}^4$. Can you delete more than one column?

#### 解答
(51) 最自然的選擇是刪掉**不是 pivot 行**的第 4 行:剩下的四行仍有 4 個 pivot(書後解答:刪第 4 行,也可以刪第 3 行)。

實際檢查:刪掉第 1、2、3、4 行中的任一行,剩下四行都還能生成 ℝ⁴;只有第 5 行不能刪。

(52) 刪掉不是 pivot 行的第 3 行即可(刪第 1 或第 2 行也可以;刪第 4 或第 5 行就不行)。**不能刪超過一行**:剩下 3 行最多 3 個 pivot,不可能 4 列都有。

#### 備註
書後解答 Exercise 51 只列出「第 4 行或第 3 行」,沒有列全;實際上刪第 1、2 行也可以(實作課會用程式逐一檢查)。背後的原因要到第 3 週的「線性相依」才能完整說明。

### 挑戰 · Lay 1.4 Exercises 39–40
(39) Construct a $3 \times 3$ matrix, not in echelon form, whose columns span $\mathbb{R}^3$. Show that the matrix you construct has the desired property.

(40) Construct a $3 \times 3$ matrix, not in echelon form, whose columns do *not* span $\mathbb{R}^3$. Show that the matrix you construct has the desired property.

#### 解答
(39) 書後提示是「從一個有 3 個 pivot 的梯形矩陣 $B$ 出發」;接著做一次列運算把它打亂(這一步書上沒寫)。例如把 $I_3$ 的第 1、3 列交換:$\begin{bmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix}$。它不是梯形,但換回來就是 $I_3$,3 列都有 pivot,所以生成 ℝ³。

(40) 讓某一列是另一列的倍數:$\begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{bmatrix}$。不是梯形;$R_2 \leftarrow R_2 - 2R_1$ 得全 0 列,最多 2 個 pivot,所以不能生成 ℝ³。

### 挑戰 · Lay 1.4 Exercises 41–42
(41) Let $A$ be a $3 \times 2$ matrix. Explain why the equation $A\mathbf{x} = \mathbf{b}$ cannot be consistent for all $\mathbf{b}$ in $\mathbb{R}^3$. Generalize your argument to the case of an arbitrary $A$ with more rows than columns.

(42) Could a set of three vectors in $\mathbb{R}^4$ span all of $\mathbb{R}^4$? Explain. What about $n$ vectors in $\mathbb{R}^m$ when $n$ is less than $m$?

#### 解答
(41) 每一行最多一個 pivot,所以 $3 \times 2$ 的 $A$ 最多 2 個 pivot,3 列中至少有一列沒有 pivot。由 Theorem 4,不是每個 $\mathbf{b}$ 都有解。一般地:$m > n$ 時 pivot 最多 $n$ 個 $< m$,一定有列沒有 pivot。

(42) **不能**。三個向量排成 $4 \times 3$ 矩陣,最多 3 個 pivot,4 列不可能都有。一般地:$n < m$ 個向量**不可能**生成 ℝᵐ。

### 挑戰 · Lay 1.4 Exercises 43–44
(43) Suppose $A$ is a $4 \times 3$ matrix and $\mathbf{b}$ is a vector in $\mathbb{R}^4$ with the property that $A\mathbf{x} = \mathbf{b}$ has a unique solution. What can you say about the reduced echelon form of $A$? Justify your answer.

(44) Suppose $A$ is a $3 \times 3$ matrix and $\mathbf{b}$ is a vector in $\mathbb{R}^3$ with the property that $A\mathbf{x} = \mathbf{b}$ has a unique solution. Explain why the columns of $A$ must span $\mathbb{R}^3$.

#### 解答
(43) 唯一解 ⇒ 沒有自由變數 ⇒ 3 行都是 pivot 行 ⇒ $A$ 有 3 個 pivot,分別在前 3 列。所以 $A$ 的 RREF 是 $\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$(書後提示:$A$ 有幾個 pivot 行?)。

(44) 唯一解 ⇒ 沒有自由變數 ⇒ 3 行都是 pivot 行 ⇒ 3 個 pivot。$A$ 只有 3 列,每列最多一個 pivot,所以**每一列都有 pivot**。由 Theorem 4,$A$ 的行生成 ℝ³。

### 挑戰 · Lay 1.4 Exercises 45–46
(45) Let $A$ be a $3 \times 4$ matrix, let $\mathbf{y}_1$ and $\mathbf{y}_2$ be vectors in $\mathbb{R}^3$, and let $\mathbf{w} = \mathbf{y}_1 + \mathbf{y}_2$. Suppose $\mathbf{y}_1 = A\mathbf{x}_1$ and $\mathbf{y}_2 = A\mathbf{x}_2$ for some vectors $\mathbf{x}_1$ and $\mathbf{x}_2$ in $\mathbb{R}^4$. What fact allows you to conclude that the system $A\mathbf{x} = \mathbf{w}$ is consistent? (*Note:* $\mathbf{x}_1$ and $\mathbf{x}_2$ denote vectors, not scalar entries in vectors.)

(46) Let $A$ be a $5 \times 3$ matrix, let $\mathbf{y}$ be a vector in $\mathbb{R}^3$, and let $\mathbf{z}$ be a vector in $\mathbb{R}^5$. Suppose $A\mathbf{y} = \mathbf{z}$. What fact allows you to conclude that the system $A\mathbf{x} = 4\mathbf{z}$ is consistent?

#### 解答
(45) **Theorem 5(a)**:$\mathbf{w} = A\mathbf{x}_1 + A\mathbf{x}_2 = A(\mathbf{x}_1 + \mathbf{x}_2)$,所以 $\mathbf{x} = \mathbf{x}_1 + \mathbf{x}_2$ 就是 $A\mathbf{x} = \mathbf{w}$ 的一個解(書後解答相同)。

(46) **Theorem 5(b)**:$A(4\mathbf{y}) = 4(A\mathbf{y}) = 4\mathbf{z}$,所以 $\mathbf{x} = 4\mathbf{y}$ 是一個解。

## 驗算
```check
Matrix([[1, Rational(-1, 2), 1]]) * Matrix([[1, 3, 4], [-4, 2, -6], [-3, -2, -7]]) == zeros(1, 3)
Matrix([[1, 3, 4], [-4, 2, -6], [-3, -2, -7]]).rank() == 2
Matrix([[2, 1]]) * Matrix([[3, -4], [-6, 8]]) == zeros(1, 2) and Matrix([[3, -4], [-6, 8]]).rank() == 1
Matrix([[1, 2, 1]]) * Matrix([[1, -3, -4], [-3, 2, 6], [5, -1, -8]]) == zeros(1, 3) and Matrix([[1, -3, -4], [-3, 2, 6], [5, -1, -8]]).rank() == 2
len(Matrix([[1, 3, 0, 3], [-1, -1, -1, 1], [0, -4, 2, -8], [2, 0, 3, -1]]).rref()[1]) == 3
len(Matrix([[1, 3, -2, 2], [0, 1, 1, -5], [1, 2, -3, 7], [-2, -8, 2, -1]]).rref()[1]) == 3
len(Matrix([[0, 0, 4], [0, -3, -1], [-2, 8, -5]]).rref()[1]) == 3
Matrix([[2, 5], [3, 1]]) * (Matrix([4, -1]) + Matrix([-3, 5])) == Matrix([[2, 5], [3, 1]]) * Matrix([4, -1]) + Matrix([[2, 5], [3, 1]]) * Matrix([-3, 5])
Matrix([[2, 5], [3, 1]]) * Matrix([1, 4]) == Matrix([22, 7])
3 in Matrix([[1, 0, 1, 3], [0, 1, 1, 2], [0, 0, 0, 1]]).rref()[1]
len(Matrix([[7, 2, -5, 8], [-5, -3, 4, -9], [6, 10, -2, 7], [-7, 9, 2, 15]]).rref()[1]) == 3
len(Matrix([[5, -7, -4, 9], [6, -8, -7, 5], [4, -4, -9, -9], [-9, 11, 16, 7]]).rref()[1]) == 3
Matrix([[12, -7, 11, -9, 5], [-9, 4, -8, 7, -3], [-6, 11, -7, 3, -9], [4, -6, 10, -5, 12]]).rref()[1] == (0, 1, 2, 4)
Matrix([[8, 11, -6, -7, 13], [-7, -8, 5, 6, -9], [11, 7, -7, -9, -6], [-3, 4, 1, 8, 7]]).rref()[1] == (0, 1, 3, 4)
[Matrix([[12, -7, 11, -9, 5], [-9, 4, -8, 7, -3], [-6, 11, -7, 3, -9], [4, -6, 10, -5, 12]])[:, [c for c in range(5) if c != j]].rank() for j in range(5)] == [4, 4, 4, 4, 3]
[Matrix([[8, 11, -6, -7, 13], [-7, -8, 5, 6, -9], [11, 7, -7, -9, -6], [-3, 4, 1, 8, 7]])[:, [c for c in range(5) if c != j]].rank() for j in range(5)] == [4, 4, 4, 3, 3]
Matrix([[1, 2, 3], [2, 4, 6], [1, 1, 1]]).rank() == 2
```
