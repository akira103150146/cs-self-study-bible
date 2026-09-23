---
title_en: Sets of One or Two Vectors, and Theorem 7
title_zh: 一兩個向量的判斷,與 Theorem 7:相依 ⇔ 有一個是其他的組合
sub: Dependent means some vector is a linear combination of the others
level: mid
source: Lay 1.7
lab_hook: '`Matrix.hstack(u, v, w).rank()`:秩小於向量個數 ⇔ 相依'
---
## 觀念
**Sets of one vector.** A set containing only one vector—say, $\mathbf{v}$—is linearly independent if and only if $\mathbf{v}$ is not the zero vector. This is because the vector equation $x_1\mathbf{v} = \mathbf{0}$ has only the trivial solution when $\mathbf{v} \neq \mathbf{0}$. The zero vector is linearly dependent because $x_1\mathbf{0} = \mathbf{0}$ has many nontrivial solutions.

**Sets of two vectors.**

> A set of two vectors $\{\mathbf{v}_1, \mathbf{v}_2\}$ is linearly dependent if at least one of the vectors is a multiple of the other. The set is linearly independent if and only if neither of the vectors is a multiple of the other.

In geometric terms, two vectors are linearly dependent if and only if they lie on the same line through the origin.

**Theorem 7 (Characterization of Linearly Dependent Sets).** An indexed set $S = \{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ of two or more vectors is linearly dependent if and only if at least one of the vectors in $S$ is a linear combination of the others. In fact, if $S$ is linearly dependent and $\mathbf{v}_1 \neq \mathbf{0}$, then some $\mathbf{v}_j$ (with $j > 1$) is a linear combination of the preceding vectors, $\mathbf{v}_1, \dots, \mathbf{v}_{j-1}$.

*Warning:* Theorem 7 does *not* say that *every* vector in a linearly dependent set is a linear combination of the preceding vectors. A vector in a linearly dependent set may fail to be a linear combination of the other vectors.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| by inspection | 用看的 | 不做列化簡,直接觀察(例如一個是另一個的倍數) |
| scalar multiple | 純量倍數 | $c\mathbf{v}$;兩個向量相依 ⇔ 其中一個是另一個的倍數 |
| characterization | 刻畫(等價描述) | 換一種說法、但意思完全相同的條件 |
| preceding vectors | 前面的向量 | $\mathbf{v}_1, \dots, \mathbf{v}_{j-1}$,排在 $\mathbf{v}_j$ 之前的 |
| (T/F-C) | 是非題 + 反例 | 課本對 Exercises 39–44 的標記:判斷真假,**假的要造一個具體反例**(C = counterexample) |

## 白話說
**一個向量**:只要不是 $\mathbf{0}$ 就獨立。

**兩個向量**:**看是不是倍數**。其中一個是另一個的倍數 → 相依;不是 → 獨立。不用列化簡(課本說「by inspection」)。

**三個以上**:Theorem 7 說,相依就是「**有人是多餘的**」——至少有一個向量可以由其他的組合出來。但要小心:

- 不是**每一個**都多餘。例如 $\{\mathbf{e}_1, 2\mathbf{e}_1, \mathbf{e}_2\}$ 相依(前兩個是倍數),但 $\mathbf{e}_2$ 不能由另外兩個組出來。
- 所以判斷相依時,**不要只挑一個向量去檢查**它是不是其他的組合;要檢查整組的 $A\mathbf{x} = \mathbf{0}$(Practice Problem 1(c))。

**「兩兩獨立」不代表整組獨立**:三個向量兩兩都不是倍數,整組照樣可以相依(下一個觀念的 Example 5)。倍數檢查**只適用於兩個向量**。

## 幾何意義
**兩個向量**相依 ⇔ 在同一條通過原點的直線上:

![課本 1.7 Figure 1:(3, 1) 與 (6, 2) 在同一條直線上,相依;(3, 2) 與 (6, 2) 不在同一條直線上,獨立。](two-vectors.svg)

**三個向量**(ℝ³ 中,$\mathbf{u}$、$\mathbf{v}$ 獨立):$\{\mathbf{u}, \mathbf{v}, \mathbf{w}\}$ 相依 ⇔ $\mathbf{w}$ 落在 $\mathbf{u}$、$\mathbf{v}$ 張成的平面上。

![課本 1.7 Figure 2:左圖 w 在 Span{u, v} 平面上,三個向量相依;右圖 w 伸出平面外,三個向量獨立。](dep-in-r3.svg)

## 在資工哪裡用
- **特徵選取**:資料裡如果有一欄可以由其他欄組合出來(Theorem 7 說的「多餘」),它不提供新資訊,可以直接丟掉。實作課就是用 pivot 行找出該留哪些欄位。
- **網路的冗餘連線**:若某條訊號路徑可以由其他路徑組合,它就是備援,不是新容量。
- **3D 建模**:三個點決定一個平面的前提是兩個邊向量**獨立**(不共線);若共線,三點在一直線上,決定不了平面——遊戲引擎算法向量時要先檢查這件事,否則會除以 0。

## 原理
**兩個向量的規則怎麼來?** 設 $c\mathbf{v}_1 + d\mathbf{v}_2 = \mathbf{0}$,$c, d$ 不全為 0。若 $c \neq 0$,可解出 $\mathbf{v}_1 = (-d/c)\mathbf{v}_2$,$\mathbf{v}_1$ 是 $\mathbf{v}_2$ 的倍數;若 $c = 0$,則 $d \neq 0$,同理 $\mathbf{v}_2 = \mathbf{0}$ 是 $\mathbf{v}_1$ 的倍數($0\mathbf{v}_1$)。反過來,若 $\mathbf{v}_2 = k\mathbf{v}_1$,則 $k\mathbf{v}_1 - \mathbf{v}_2 = \mathbf{0}$ 就是一條相依關係(例 1)。

**Theorem 7 的證明**(課本 p. 88):

- **(⇐)** 若 $\mathbf{v}_j$ 是其他向量的組合,移項後 $\mathbf{v}_j$ 的權重是 $-1 \neq 0$,就是一條相依關係。
- **(⇒)** 若 $S$ 相依,**先分兩種情況**(課本就是這樣分的,少了這一步只證到定理的後半句):
  - **$\mathbf{v}_1 = \mathbf{0}$**:那麼 $\mathbf{v}_1$ 本身就是其他向量的(平凡)線性組合 $0\mathbf{v}_2 + \cdots + 0\mathbf{v}_p$,已經符合「至少有一個是其他的組合」。
  - **$\mathbf{v}_1 \neq \mathbf{0}$**:取一條相依關係 $c_1\mathbf{v}_1 + \cdots + c_p\mathbf{v}_p = \mathbf{0}$,令 $j$ 是 $c_j \neq 0$ 的**最大**下標。$j = 1$ 不可能(那會變成 $c_1\mathbf{v}_1 = \mathbf{0}$,與 $\mathbf{v}_1 \neq \mathbf{0}$ 矛盾),所以 $j > 1$。把 $c_j\mathbf{v}_j$ 以外的項移到右邊再除以 $c_j$:
    $$\mathbf{v}_j = \left(-\frac{c_1}{c_j}\right)\mathbf{v}_1 + \cdots + \left(-\frac{c_{j-1}}{c_j}\right)\mathbf{v}_{j-1}.$$
    這一段同時證出定理的後半句:**$\mathbf{v}_1 \neq \mathbf{0}$ 時,那個「多餘的」向量可以挑在前面向量的組合裡**。

## 老師講解
### 例 1 · Lay 1.7 Example 3
Determine if the following sets of vectors are linearly independent.

- **a.** $\mathbf{v}_1 = \begin{bmatrix} 3 \\ 1 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 6 \\ 2 \end{bmatrix}$
- **b.** $\mathbf{v}_1 = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 6 \\ 2 \end{bmatrix}$

1. **(a) 找倍數關係**:$\mathbf{v}_2 = 2\mathbf{v}_1$(兩個分量都是 2 倍)。
2. **(a) 寫成相依關係**:$-2\mathbf{v}_1 + \mathbf{v}_2 = \mathbf{0}$,權重 $-2, 1$ 不全為 0,所以 $\{\mathbf{v}_1, \mathbf{v}_2\}$ **相依**。
3. **(b) 檢查倍數**:$6 / 3 = 2$ 但 $2 / 2 = 1$,兩個分量的比不一樣,**不是倍數**。
4. **(b) 為什麼「不是倍數」就夠?** 假設 $c\mathbf{v}_1 + d\mathbf{v}_2 = \mathbf{0}$。若 $c \neq 0$,就能解出 $\mathbf{v}_1 = (-d/c)\mathbf{v}_2$,和「不是倍數」矛盾,所以 $c = 0$;同理 $d = 0$。只有平凡解,所以 $\{\mathbf{v}_1, \mathbf{v}_2\}$ **獨立**。
5. **幾何**:(a) 的兩個向量在同一條通過原點的直線上;(b) 的不在(見「幾何意義」的圖)。
6. **提醒**:這個「看倍數」的方法**只適用於兩個向量**。

### 例 2 · Lay 1.7 Example 4
Let $\mathbf{u} = \begin{bmatrix} 3 \\ 1 \\ 0 \end{bmatrix}$ and $\mathbf{v} = \begin{bmatrix} 1 \\ 6 \\ 0 \end{bmatrix}$. Describe the set spanned by $\mathbf{u}$ and $\mathbf{v}$, and explain why a vector $\mathbf{w}$ is in $\operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$ if and only if $\{\mathbf{u}, \mathbf{v}, \mathbf{w}\}$ is linearly dependent.

1. **$\mathbf{u}$、$\mathbf{v}$ 獨立**:兩個向量都不是對方的倍數。
2. **描述 Span**:兩個獨立向量在 ℝ³ 中張成一個平面。它們的第三個分量都是 0,所以 $\operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$ 就是 $x_1x_2$-平面($x_3 = 0$)。
3. **(⇒)** 若 $\mathbf{w}$ 在 $\operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$ 裡,$\mathbf{w}$ 是 $\mathbf{u}$、$\mathbf{v}$ 的組合,由 Theorem 7,$\{\mathbf{u}, \mathbf{v}, \mathbf{w}\}$ 相依。
4. **(⇐)** 若 $\{\mathbf{u}, \mathbf{v}, \mathbf{w}\}$ 相依,因為 $\mathbf{u} \neq \mathbf{0}$,由 Theorem 7 的後半句,某個向量是**它前面**向量的組合。
5. **是誰?** 不可能是 $\mathbf{v}$($\mathbf{v}$ 不是 $\mathbf{u}$ 的倍數),所以只能是 $\mathbf{w}$:$\mathbf{w}$ 是 $\mathbf{u}$、$\mathbf{v}$ 的組合,也就是 $\mathbf{w} \in \operatorname{Span}\{\mathbf{u}, \mathbf{v}\}$。
6. **推廣**:ℝ³ 中若 $\mathbf{u}$、$\mathbf{v}$ 獨立,則 $\{\mathbf{u}, \mathbf{v}, \mathbf{w}\}$ 相依 ⇔ $\mathbf{w}$ 落在 $\mathbf{u}$、$\mathbf{v}$ 張成的平面上。

## 易錯點
- 對三個以上的向量用「兩兩檢查倍數」。兩兩都不是倍數,整組仍可能相依。
- 以為相依集合裡**每個**向量都是其他的組合(是非題 Exercise 23)。
- 忘了 $\mathbf{0}$ 是任何向量的倍數($\mathbf{0} = 0\mathbf{v}$),所以 $\{\mathbf{v}, \mathbf{0}\}$ 一定相依(Exercise 41)。
- 檢查倍數時只比了一個分量:$(-8, 12, -4)$ 和 $(2, -3, -1)$ 前兩個分量是 $-4$ 倍,第三個不是(Exercise 19)。

## 教學提示
「看倍數」這招學生會非常喜歡,**一定要馬上接反例**:ℝ² 中的 $(2, 1)$、$(4, -1)$、$(-2, 2)$ 兩兩不是倍數,卻相依(下一個觀念的例 1)。

例 2 讓學生用手比:兩支筆當 $\mathbf{u}$、$\mathbf{v}$ 平放在桌上,第三支筆 $\mathbf{w}$ 平放在桌上 → 相依;立起來 → 獨立。

課堂建議做:Exercises 3–4、16、19;是非 Exercises 22、23、26、27;Exercise 41 當討論題。

## 練習
### 照做 · Lay 1.7 Exercises 3–4
Determine if the vectors are linearly independent. Justify each answer.

(3) $\begin{bmatrix} 1 \\ -3 \end{bmatrix}, \begin{bmatrix} -3 \\ 6 \end{bmatrix}$  (4) $\begin{bmatrix} -1 \\ 4 \end{bmatrix}, \begin{bmatrix} -2 \\ 8 \end{bmatrix}$

#### 解答
兩個向量,看倍數就好。

(3) 若第二個是第一個的 $k$ 倍,第一個分量給 $k = -3$,但 $-3 \cdot (-3) = 9 \neq 6$。不是倍數 → **獨立**(書後解答相同)。

(4) $\begin{bmatrix} -2 \\ 8 \end{bmatrix} = 2\begin{bmatrix} -1 \\ 4 \end{bmatrix}$,是倍數 → **相依**,$2\mathbf{v}_1 - \mathbf{v}_2 = \mathbf{0}$。

### 照做 · Lay 1.7 Exercises 16, 19
Determine by inspection whether the vectors are linearly *independent*. Justify each answer.

(16) $\begin{bmatrix} 4 \\ -2 \\ 6 \end{bmatrix}, \begin{bmatrix} 6 \\ -3 \\ 9 \end{bmatrix}$  (19) $\begin{bmatrix} -8 \\ 12 \\ -4 \end{bmatrix}, \begin{bmatrix} 2 \\ -3 \\ -1 \end{bmatrix}$

#### 解答
(16) $\begin{bmatrix} 6 \\ -3 \\ 9 \end{bmatrix} = \tfrac32\begin{bmatrix} 4 \\ -2 \\ 6 \end{bmatrix}$,是倍數 → **相依**(不是獨立)。

(19) $-4\begin{bmatrix} 2 \\ -3 \\ -1 \end{bmatrix} = \begin{bmatrix} -8 \\ 12 \\ 4 \end{bmatrix}$,前兩個分量對得上,第三個是 $4 \neq -4$。不是倍數 → **獨立**(書後解答相同)。

#### 備註
Exercises 15、17、18、20 屬於同一組題目,放在觀念 5(它們要用 Theorem 8、9)。

### 是非 · Lay 1.7 Exercise 22
**(T/F)** Two vectors are linearly dependent if and only if they lie on a line through the origin.

#### 解答
**True.** 兩個向量相依 ⇔ 一個是另一個的倍數 ⇔ 兩個都在同一條通過原點的直線上($\mathbf{0}$ 在每一條這樣的直線上)。

### 是非 · Lay 1.7 Exercise 23
**(T/F)** If $S$ is a linearly dependent set, then each vector is a linear combination of the other vectors in $S$.

#### 解答
**False.** 見 Theorem 7 後的 Warning 與 Practice Problem 1(c):$\{\mathbf{u}, \mathbf{v}, \mathbf{w}, \mathbf{z}\}$ 相依,但 $\mathbf{w}$ 不是 $\mathbf{u}, \mathbf{v}, \mathbf{z}$ 的組合。

### 是非 · Lay 1.7 Exercise 26
**(T/F)** If $\mathbf{x}$ and $\mathbf{y}$ are linearly independent, and if $\mathbf{z}$ is in $\operatorname{Span}\{\mathbf{x}, \mathbf{y}\}$, then $\{\mathbf{x}, \mathbf{y}, \mathbf{z}\}$ is linearly dependent.

#### 解答
**True.** $\mathbf{z} = c_1\mathbf{x} + c_2\mathbf{y}$ 移項得 $c_1\mathbf{x} + c_2\mathbf{y} - \mathbf{z} = \mathbf{0}$,$\mathbf{z}$ 的權重 $-1 \neq 0$,是一條相依關係(Theorem 7)。

### 是非 · Lay 1.7 Exercise 27
**(T/F)** If $\mathbf{x}$ and $\mathbf{y}$ are linearly independent, and if $\{\mathbf{x}, \mathbf{y}, \mathbf{z}\}$ is linearly dependent, then $\mathbf{z}$ is in $\operatorname{Span}\{\mathbf{x}, \mathbf{y}\}$.

#### 解答
**True.** $\mathbf{x} \neq \mathbf{0}$(獨立集合不含 $\mathbf{0}$),由 Theorem 7,某個向量是它前面向量的組合;不可能是 $\mathbf{y}$($\mathbf{y}$ 不是 $\mathbf{x}$ 的倍數),所以是 $\mathbf{z}$。這正是例 2 的推廣。

### 挑戰 · Lay 1.7 Exercise 39
Each statement is either true (in all cases) or false (for at least one example). If false, construct a specific example to show that the statement is not always true. Such an example is called a *counterexample* to the statement. If a statement is true, give a justification.

**(T/F-C)** If $\mathbf{v}_1, \dots, \mathbf{v}_4$ are in $\mathbb{R}^4$ and $\mathbf{v}_3 = 2\mathbf{v}_1 + \mathbf{v}_2$, then $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4\}$ is linearly dependent.

#### 解答
**True**,由 Theorem 7(書後解答相同)。具體的相依關係:$2\mathbf{v}_1 + \mathbf{v}_2 - \mathbf{v}_3 + 0\mathbf{v}_4 = \mathbf{0}$,$\mathbf{v}_3$ 的權重 $-1 \neq 0$。

### 挑戰 · Lay 1.7 Exercise 41
Each statement is either true (in all cases) or false (for at least one example). If false, construct a counterexample. If true, give a justification.

**(T/F-C)** If $\mathbf{v}_1$ and $\mathbf{v}_2$ are in $\mathbb{R}^4$ and $\mathbf{v}_2$ is not a scalar multiple of $\mathbf{v}_1$, then $\{\mathbf{v}_1, \mathbf{v}_2\}$ is linearly independent.

#### 解答
**False.** $\mathbf{v}_1$ 可能是零向量(書後解答相同)。反例:$\mathbf{v}_1 = \mathbf{0}$、$\mathbf{v}_2 = (1, 0, 0, 0)$。$\mathbf{v}_2$ 不是 $\mathbf{0}$ 的倍數,但 $1\mathbf{v}_1 + 0\mathbf{v}_2 = \mathbf{0}$ 是相依關係。

#### 備註
這就是課本那句「at least one of the vectors is a multiple of the other」為什麼要說「**至少一個**」:這裡 $\mathbf{v}_1 = 0\mathbf{v}_2$ 是倍數,但 $\mathbf{v}_2$ 不是 $\mathbf{v}_1$ 的倍數。

### 挑戰 · Lay 1.7 Exercise 42
Each statement is either true (in all cases) or false (for at least one example). If false, construct a counterexample. If true, give a justification.

**(T/F-C)** If $\mathbf{v}_1, \dots, \mathbf{v}_4$ are in $\mathbb{R}^4$ and $\mathbf{v}_3$ is *not* a linear combination of $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_4$, then $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4\}$ is linearly independent.

#### 解答
**False.** 反例:$\mathbf{v}_1 = \mathbf{v}_2 = \mathbf{e}_1$、$\mathbf{v}_3 = \mathbf{e}_2$、$\mathbf{v}_4 = \mathbf{e}_3$。$\mathbf{v}_3 = \mathbf{e}_2$ 不在 $\operatorname{Span}\{\mathbf{e}_1, \mathbf{e}_3\}$ 裡,但 $\mathbf{v}_1 - \mathbf{v}_2 = \mathbf{0}$,整組相依。

#### 備註
和是非題 Exercise 23 是同一個陷阱:只檢查**一個**向量不夠。

## 驗算
```check
Matrix([6, 2]) == 2 * Matrix([3, 1])
Matrix([[3, 6], [2, 2]]).rank() == 2
Matrix([[3, 1, 0], [1, 6, 0]]).T.rank() == 2
Matrix([[3, 1, 5], [1, 6, 3], [0, 0, 0]]).rank() == 2
Matrix([[1, -3], [-3, 6]]).rank() == 2
Matrix([-2, 8]) == 2 * Matrix([-1, 4])
Matrix([6, -3, 9]) == Rational(3, 2) * Matrix([4, -2, 6])
Matrix([[-8, 2], [12, -3], [-4, -1]]).rank() == 2
Matrix([[3, -6, 3], [2, 1, 7], [-4, 7, -5]]).rank() == 2 and Matrix([[3, -6, 3, 0], [2, 1, 7, -5], [-4, 7, -5, 2]]).rank() == 3
Matrix.hstack(zeros(4, 1), Matrix([1, 0, 0, 0])).rank() < 2
Matrix([[1, 1, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]]).rank() == 2 and Matrix([[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]).rank() == 3
Matrix([[1, 0, 2], [0, 1, 1], [0, 0, 0], [0, 0, 0]]) * Matrix([2, 1, -1]) == zeros(4, 1)
```
