---
title_en: Automatic Linear Dependence (Theorems 8 and 9)
title_zh: 一定相依的兩種情況:向量太多,或含零向量
sub: More vectors than entries, or a zero vector, means dependent
level: mid
source: Lay 1.7
lab_hook: '`A.shape[1] > A.shape[0]`:行比列多,不用算就知道各行相依'
---
## 觀念
The next two theorems describe special cases in which the linear dependence of a set is automatic.

**Theorem 8.** If a set contains more vectors than there are entries in each vector, then the set is linearly dependent. That is, any set $\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ in $\mathbb{R}^n$ is linearly dependent if $p > n$.

*Proof.* Let $A = [\,\mathbf{v}_1 \;\; \cdots \;\; \mathbf{v}_p\,]$. Then $A$ is $n \times p$, and the equation $A\mathbf{x} = \mathbf{0}$ corresponds to a system of $n$ equations in $p$ unknowns. If $p > n$, there are more variables than equations, so there must be a free variable. Hence $A\mathbf{x} = \mathbf{0}$ has a nontrivial solution, and the columns of $A$ are linearly dependent.

*Warning:* Theorem 8 says nothing about the case in which the number of vectors in the set does *not* exceed the number of entries in each vector.

**Theorem 9.** If a set $S = \{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ in $\mathbb{R}^n$ contains the zero vector, then the set is linearly dependent.

*Proof.* By renumbering the vectors, we may suppose $\mathbf{v}_1 = \mathbf{0}$. Then the equation $1\mathbf{v}_1 + 0\mathbf{v}_2 + \cdots + 0\mathbf{v}_p = \mathbf{0}$ shows that $S$ is linearly dependent.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| entries | 分量 | 向量裡的數字個數;ℝⁿ 的向量有 $n$ 個分量 |
| more variables than equations | 未知數比方程式多 | 一定有自由變數 |
| renumbering | 重新編號 | 把零向量換到第一個,不影響是否相依 |
| counterexample | 反例 | 一個讓敘述不成立的具體例子 |

## 白話說
兩種情況**不用算**就知道相依:

1. **向量太多**(Theorem 8):ℝⁿ 裡放超過 $n$ 個向量,一定相依。ℝ² 裡三個向量、ℝ³ 裡四個向量,必有多餘的。
2. **含零向量**(Theorem 9):$\mathbf{0}$ 本身就是多餘的——給它權重 1、其他全 0,就是一條相依關係。

**反過來不成立**:

- 向量個數 $\le n$ 時,Theorem 8 **什麼都沒說**,可能獨立、也可能相依,要自己算(是非題 Exercises 24、28)。
- 沒有零向量也可能相依。

所以判斷「by inspection(用看的)」的檢查順序:**有零向量嗎?個數比分量多嗎?只有兩個的話是倍數嗎?** 三個都不成立,才需要列化簡。

## 幾何意義
ℝ² 是平面,最多只能有兩個「真正不同方向」的向量。第三個向量一定落在前兩個張成的平面(就是整個 ℝ²)裡:

![課本 Figure 4:ℝ² 中的三個向量 (2, 1)、(4, −1)、(−2, 2) 兩兩都不是倍數,但整組相依。](three-in-r2.svg)

同理,ℝ³ 最多三個獨立的方向;第四個向量一定可以由前面的組出來。

## 在資工哪裡用
- **特徵比資料多**:一張資料表若欄位(特徵)數比資料列數多,把每一列當成一個向量看,這些欄向量就「太多」了。例如 100 筆資料、1000 個特徵:1000 個欄向量在 ℝ¹⁰⁰ 裡,由 Theorem 8 一定相依。線性迴歸在這種情況下解不唯一,需要正規化(regularization)。
- **資料有全 0 的欄**:某個感測器壞了、整欄都是 0,由 Theorem 9,這組欄位相依。前處理時要先把這種欄刪掉。
- **維度與容量**:一個 $n$ 維的線性模型最多只能「分辨」$n$ 個獨立方向——這是第 7 週「維度」觀念的起點。

## 原理
**Theorem 8 的關鍵**:$n \times p$ 的矩陣最多 $n$ 個 pivot(每列最多一個)。$p > n$ 時,$p$ 行裡至少有 $p - n$ 行不是 pivot 行 → 自由變數 → 非平凡解。

**矩陣的樣子**(課本 Figure 3):一個「矮胖」的矩陣(行比列多),各行一定相依。
$$\underbrace{\begin{bmatrix} * & * & * & * & * \\ * & * & * & * & * \\ * & * & * & * & * \end{bmatrix}}_{p = 5 \text{ columns in } \mathbb{R}^3}$$

**子集與超集**(Practice Problem 2、Exercises 43–44):

- 相依的集合再加入向量,仍然相依(新向量權重給 0)。
- 獨立的集合拿掉向量,仍然獨立(拿掉後若相依,放回去也相依,矛盾)。

## 老師講解
### 例 1 · Lay 1.7 Example 5
The vectors $\begin{bmatrix} 2 \\ 1 \end{bmatrix}, \begin{bmatrix} 4 \\ -1 \end{bmatrix}, \begin{bmatrix} -2 \\ 2 \end{bmatrix}$ are linearly dependent by Theorem 8, because there are three vectors in the set and there are only two entries in each vector. Notice, however, that none of the vectors is a multiple of one of the other vectors.

1. **數一數**:3 個向量,每個有 2 個分量。$p = 3 > n = 2$,由 Theorem 8 **相依**,不用計算。
2. **倍數檢查會騙人**:$(2, 1)$ 和 $(4, -1)$ 不是倍數;$(2, 1)$ 和 $(-2, 2)$ 不是;$(4, -1)$ 和 $(-2, 2)$ 也不是。兩兩都「看起來獨立」。
3. **找出相依關係**(驗證 Theorem 8 沒騙人):化簡 $\begin{bmatrix} 2 & 4 & -2 \\ 1 & -1 & 2 \end{bmatrix} \sim \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & -1 \end{bmatrix}$,$x_3$ 自由,$x_1 = -x_3$、$x_2 = x_3$。
4. **取 $x_3 = 1$**:$-\begin{bmatrix} 2 \\ 1 \end{bmatrix} + \begin{bmatrix} 4 \\ -1 \end{bmatrix} + \begin{bmatrix} -2 \\ 2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$ ✓。
5. **結論**:「兩兩不是倍數」不能推出獨立;三個以上的向量要看整體。

#### 備註
第 3、4 步不是課本的內容,是補上的驗證,讓學生親眼看到那條相依關係。

### 例 2 · Lay 1.7 Example 6
Determine by inspection if the given set is linearly dependent.

- **a.** $\begin{bmatrix} 1 \\ 7 \\ 6 \end{bmatrix}, \begin{bmatrix} 2 \\ 0 \\ 9 \end{bmatrix}, \begin{bmatrix} 3 \\ 1 \\ 5 \end{bmatrix}, \begin{bmatrix} 4 \\ 1 \\ 8 \end{bmatrix}$
- **b.** $\begin{bmatrix} 2 \\ 3 \\ 5 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 1 \\ 1 \\ 8 \end{bmatrix}$
- **c.** $\begin{bmatrix} -2 \\ 4 \\ 6 \\ 10 \end{bmatrix}, \begin{bmatrix} 3 \\ -6 \\ -9 \\ 15 \end{bmatrix}$

1. **(a) 數個數**:4 個向量,每個只有 3 個分量,由 Theorem 8 **相依**。
2. **(b) 先數個數**:3 個向量、3 個分量,Theorem 8 **不適用**。
3. **(b) 看零向量**:集合裡有 $\mathbf{0}$,由 Theorem 9 **相依**。
4. **(c) 兩個向量,看倍數**:比較對應分量,第二個看起來是第一個的 $-\tfrac32$ 倍:$-2 \cdot (-\tfrac32) = 3$ ✓、$4 \cdot (-\tfrac32) = -6$ ✓、$6 \cdot (-\tfrac32) = -9$ ✓,但 $10 \cdot (-\tfrac32) = -15 \neq 15$ ✗。
5. **(c) 結論**:不是倍數,所以**獨立**。只要有一個分量對不上,就不是倍數。
6. **檢查順序總結**:零向量?個數太多?兩個的話是倍數嗎?這三招都用不上時,才需要列化簡。

## 易錯點
- 把 Theorem 8 反過來用:「向量個數 $\le$ 分量數 ⇒ 獨立」。錯,Theorem 8 對這種情況**什麼都沒說**(是非題 Exercise 24)。
- 以為相依就一定是「向量太多」。$\{\mathbf{e}_1, 2\mathbf{e}_1\}$ 在 ℝ³ 只有 2 個向量,照樣相依(是非題 Exercise 28)。
- 數錯:Theorem 8 比的是「向量個數」和「每個向量的分量數」,也就是矩陣的**行數**和**列數**。$3 \times 5$ 的矩陣,5 個行向量在 ℝ³ 裡,相依;$5 \times 3$ 的矩陣,不能用 Theorem 8 判斷。
- 看到零向量還去做列化簡。直接用 Theorem 9。

## 教學提示
例 1 是整週最好的「反直覺」時刻:先讓學生兩兩檢查倍數,全班都會說「獨立」,再亮出 Theorem 8。

把「檢查順序」寫成黑板角落的流程:①有 $\mathbf{0}$? ②個數 > 分量數? ③兩個的話是倍數? ④都不是 → 列化簡看每行有沒有 pivot。

課堂建議做:Exercises 7–8、15、17;是非 Exercises 24、25、28;Practice Problem 1 當整合題。

## 練習
### 照做 · Lay 1.7 Exercises 7–8
Determine if the columns of the matrix form a linearly independent set. Justify each answer.

(7) $\begin{bmatrix} 1 & 4 & -3 & 0 \\ -2 & -7 & 5 & 1 \\ -4 & -5 & 7 & 5 \end{bmatrix}$  (8) $\begin{bmatrix} 1 & -3 & 3 & -2 \\ -3 & 7 & -1 & 2 \\ 0 & 1 & -4 & 3 \end{bmatrix}$

#### 解答
兩題都是 $3 \times 4$:4 個行向量在 ℝ³ 裡,由 Theorem 8 **相依**,不用化簡。

(7) **相依**(書後解答相同)。若要寫出相依關係:RREF 是 $\begin{bmatrix} 1 & 0 & 0 & -3 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -1 \end{bmatrix}$,取 $x_4 = 1$ 得 $3\mathbf{a}_1 + \mathbf{a}_3 + \mathbf{a}_4 = \mathbf{0}$。

(8) **相依**。RREF 是 $\begin{bmatrix} 1 & 0 & -9 & 0 \\ 0 & 1 & -4 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$,取 $x_3 = 1$ 得 $9\mathbf{a}_1 + 4\mathbf{a}_2 + \mathbf{a}_3 = \mathbf{0}$。

### 照做 · Lay 1.7 Exercises 15, 17, 18, 20
Determine by inspection whether the vectors are linearly *independent*. Justify each answer.

(15) $\begin{bmatrix} 5 \\ 1 \end{bmatrix}, \begin{bmatrix} 2 \\ 8 \end{bmatrix}, \begin{bmatrix} 1 \\ 3 \end{bmatrix}, \begin{bmatrix} -1 \\ 7 \end{bmatrix}$  (17) $\begin{bmatrix} 3 \\ 5 \\ -1 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} -6 \\ 5 \\ 4 \end{bmatrix}$

(18) $\begin{bmatrix} 4 \\ 4 \end{bmatrix}, \begin{bmatrix} -1 \\ 3 \end{bmatrix}, \begin{bmatrix} 2 \\ 5 \end{bmatrix}, \begin{bmatrix} 8 \\ 1 \end{bmatrix}$  (20) $\begin{bmatrix} 1 \\ 4 \\ -7 \end{bmatrix}, \begin{bmatrix} -2 \\ 5 \\ 3 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$

#### 解答
四題都**不是**獨立(都相依):

(15) ℝ² 中 4 個向量,$4 > 2$,Theorem 8(書後解答:相依)。

(17) 含零向量,Theorem 9(書後解答:相依)。

(18) ℝ² 中 4 個向量,Theorem 8。

(20) 含零向量,Theorem 9。

#### 備註
同組的 Exercises 16、19 只有兩個向量,放在觀念 4 用倍數判斷。

### 是非 · Lay 1.7 Exercise 24
**(T/F)** If a set contains fewer vectors than there are entries in the vectors, then the set is linearly independent.

#### 解答
**False.** Theorem 8 對 $p \le n$ 什麼都沒說(課本的 Warning)。反例:ℝ³ 中的 $\left\{\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 2 \\ 0 \\ 0 \end{bmatrix}\right\}$ 只有 2 個向量,卻相依。

### 是非 · Lay 1.7 Exercise 25
**(T/F)** The columns of any $4 \times 5$ matrix are linearly dependent.

#### 解答
**True.** 5 個行向量在 ℝ⁴ 裡,$5 > 4$,由 Theorem 8 相依。

### 是非 · Lay 1.7 Exercise 28
**(T/F)** If a set in $\mathbb{R}^n$ is linearly dependent, then the set contains more vectors than there are entries in each vector.

#### 解答
**False.** 這是 Theorem 8 的**逆敘述**,不成立。反例:例 2(b) 的 $\left\{\begin{bmatrix} 2 \\ 3 \\ 5 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 1 \\ 1 \\ 8 \end{bmatrix}\right\}$ 相依,但 $p = n = 3$。

### 變化 · Lay 1.7 Practice Problem 1
Let $\mathbf{u} = \begin{bmatrix} 3 \\ 2 \\ -4 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} -6 \\ 1 \\ 7 \end{bmatrix}$, $\mathbf{w} = \begin{bmatrix} 0 \\ -5 \\ 2 \end{bmatrix}$, and $\mathbf{z} = \begin{bmatrix} 3 \\ 7 \\ -5 \end{bmatrix}$.

- **a.** Are the sets $\{\mathbf{u}, \mathbf{v}\}$, $\{\mathbf{u}, \mathbf{w}\}$, $\{\mathbf{u}, \mathbf{z}\}$, $\{\mathbf{v}, \mathbf{w}\}$, $\{\mathbf{v}, \mathbf{z}\}$, and $\{\mathbf{w}, \mathbf{z}\}$ each linearly independent? Why or why not?
- **b.** Does the answer to Part (a) imply that $\{\mathbf{u}, \mathbf{v}, \mathbf{w}, \mathbf{z}\}$ is linearly independent?
- **c.** To determine if $\{\mathbf{u}, \mathbf{v}, \mathbf{w}, \mathbf{z}\}$ is linearly dependent, is it wise to check if, say, $\mathbf{w}$ is a linear combination of $\mathbf{u}$, $\mathbf{v}$, and $\mathbf{z}$?
- **d.** Is $\{\mathbf{u}, \mathbf{v}, \mathbf{w}, \mathbf{z}\}$ linearly dependent?

#### 解答
(a) **是**。每一對都不是彼此的倍數,所以每一對都獨立。

(b) **否**。(a) 的觀察本身,對整組 $\{\mathbf{u}, \mathbf{v}, \mathbf{w}, \mathbf{z}\}$ 是否獨立什麼都沒說。

(c) **否**。只挑一個向量檢查通常不是好方法:可能挑中的向量不是其他的組合,但整組照樣相依。這一題正是如此——$\mathbf{w}$ 不是 $\mathbf{u}, \mathbf{v}, \mathbf{z}$ 的組合。

(d) **是**,由 Theorem 8:4 個向量、每個只有 3 個分量(課本 p. 90)。

事實上 $\mathbf{z} = 3\mathbf{u} + \mathbf{v}$,所以 $\operatorname{Span}\{\mathbf{u}, \mathbf{v}, \mathbf{z}\}$ 只是一個平面,而 $\mathbf{w}$ 在平面外。

#### 備註
這題把本週三個觀念串在一起:兩兩檢查(觀念 4)不夠、Theorem 7 的 Warning、Theorem 8。

### 挑戰 · Lay 1.7 Exercise 40
Each statement is either true (in all cases) or false (for at least one example). If false, construct a counterexample. If true, give a justification.

**(T/F)** If $\mathbf{v}_1, \dots, \mathbf{v}_4$ are in $\mathbb{R}^4$ and $\mathbf{v}_3 = \mathbf{0}$, then $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4\}$ is linearly dependent.

#### 解答
**True**,由 Theorem 9:$0\mathbf{v}_1 + 0\mathbf{v}_2 + 1\mathbf{v}_3 + 0\mathbf{v}_4 = \mathbf{0}$ 是一條相依關係。

### 挑戰 · Lay 1.7 Practice Problem 2
Suppose that $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ is a linearly dependent set of vectors in $\mathbb{R}^n$ and $\mathbf{v}_4$ is a vector in $\mathbb{R}^n$. Show that $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4\}$ is also a linearly dependent set.

#### 解答
由相依的定義,存在不全為 0 的 $c_1, c_2, c_3$,使 $c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + c_3\mathbf{v}_3 = \mathbf{0}$。兩邊加上 $0\mathbf{v}_4 = \mathbf{0}$:
$$c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + c_3\mathbf{v}_3 + 0\mathbf{v}_4 = \mathbf{0}.$$
$c_1, c_2, c_3, 0$ 不全為 0,所以 $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4\}$ 符合相依的定義(課本 p. 91)。

### 挑戰 · Lay 1.7 Exercises 43–44
Each statement is either true (in all cases) or false (for at least one example). If false, construct a counterexample. If true, give a justification.

(43) **(T/F)** If $\mathbf{v}_1, \dots, \mathbf{v}_4$ are in $\mathbb{R}^4$ and $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ is linearly dependent, then $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4\}$ is also linearly dependent.

(44) **(T/F)** If $\mathbf{v}_1, \dots, \mathbf{v}_4$ are linearly independent vectors in $\mathbb{R}^4$, then $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ is also linearly independent. [*Hint:* Think about $x_1\mathbf{v}_1 + x_2\mathbf{v}_2 + x_3\mathbf{v}_3 + 0 \cdot \mathbf{v}_4 = \mathbf{0}$.]

#### 解答
(43) **True.** $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$ 之間的相依關係,在 $\mathbf{v}_4$ 前面放權重 0,就成為 $\mathbf{v}_1, \dots, \mathbf{v}_4$ 之間的相依關係(書後解答相同;就是 Practice Problem 2)。

(44) **True.** 若 $x_1\mathbf{v}_1 + x_2\mathbf{v}_2 + x_3\mathbf{v}_3 = \mathbf{0}$ 有非平凡解,則 $x_1\mathbf{v}_1 + x_2\mathbf{v}_2 + x_3\mathbf{v}_3 + 0 \cdot \mathbf{v}_4 = \mathbf{0}$ 也是非平凡解,與 $\mathbf{v}_1, \dots, \mathbf{v}_4$ 獨立矛盾。(這是 Exercise 43 的逆否敘述。)

#### 備註
兩題合起來的口訣:**相依的加東西還是相依;獨立的拿掉東西還是獨立。**反過來(獨立的加東西、相依的拿掉東西)都不一定。

## 驗算
```check
Matrix([[2, 4, -2], [1, -1, 2]]).rref()[0] == Matrix([[1, 0, 1], [0, 1, -1]])
-Matrix([2, 1]) + Matrix([4, -1]) + Matrix([-2, 2]) == zeros(2, 1)
Matrix([[1, 2, 3, 4], [7, 0, 1, 1], [6, 9, 5, 8]]).rank() < 4
Matrix([[2, 0, 1], [3, 0, 1], [5, 0, 8]]).rank() < 3
Matrix([[-2, 3], [4, -6], [6, -9], [10, 15]]).rank() == 2
Matrix([[1, 4, -3, 0], [-2, -7, 5, 1], [-4, -5, 7, 5]]).rref()[0] == Matrix([[1, 0, 0, -3], [0, 1, 0, 0], [0, 0, 1, -1]])
Matrix([[1, 4, -3, 0], [-2, -7, 5, 1], [-4, -5, 7, 5]]) * Matrix([3, 0, 1, 1]) == zeros(3, 1)
Matrix([[1, -3, 3, -2], [-3, 7, -1, 2], [0, 1, -4, 3]]) * Matrix([9, 4, 1, 0]) == zeros(3, 1)
Matrix([[5, 2, 1, -1], [1, 8, 3, 7]]).rank() < 4
Matrix([[3, 0, -6], [5, 0, 5], [-1, 0, 4]]).rank() < 3
Matrix([[4, -1, 2, 8], [4, 3, 5, 1]]).rank() < 4
Matrix([[1, -2, 0], [4, 5, 0], [-7, 3, 0]]).rank() < 3
Matrix([[1, 2], [0, 0], [0, 0]]).rank() < 2
3 * Matrix([3, 2, -4]) + Matrix([-6, 1, 7]) == Matrix([3, 7, -5])
Matrix([[3, -6, 3], [2, 1, 7], [-4, 7, -5]]).rank() == 2 and Matrix([[3, -6, 0, 3], [2, 1, -5, 7], [-4, 7, 2, -5]]).rank() == 3
Matrix([[3, -6, 0], [2, 1, -5], [-4, 7, 2]]).rank() == 3
Matrix.hstack(Matrix([1, 0, 0, 0]), Matrix([0, 1, 0, 0]), zeros(4, 1), Matrix([0, 0, 0, 1])).rank() < 4
Matrix([[1, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]) * Matrix([2, -1, 0, 0]) == zeros(4, 1)
```
