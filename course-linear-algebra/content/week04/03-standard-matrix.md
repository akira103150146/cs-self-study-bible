---
title_en: The Matrix of a Linear Transformation
title_zh: 標準矩陣:看 T 把 e1、e2 送到哪裡就夠了
sub: A = [T(e1) ... T(en)]
level: mid
source: Lay 1.9
lab_hook: '`np.column_stack([T(e) for e in np.eye(n)])`:把 $T(\mathbf{e}_j)$ 排成行,就得到標準矩陣'
---
## 觀念
Whenever a linear transformation $T$ arises geometrically or is described in words, we usually want a "formula" for $T(\mathbf{x})$. The discussion that follows shows that every linear transformation from $\mathbb{R}^n$ to $\mathbb{R}^m$ is actually a matrix transformation $\mathbf{x} \mapsto A\mathbf{x}$. The key to finding $A$ is to observe that $T$ is completely determined by what it does to the columns of the $n \times n$ identity matrix $I_n$.

**Theorem 10.** Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation. Then there exists a unique matrix $A$ such that

$$T(\mathbf{x}) = A\mathbf{x} \quad \text{for all } \mathbf{x} \text{ in } \mathbb{R}^n$$

In fact, $A$ is the $m \times n$ matrix whose $j$th column is the vector $T(\mathbf{e}_j)$, where $\mathbf{e}_j$ is the $j$th column of the identity matrix in $\mathbb{R}^n$:

$$A = [\,T(\mathbf{e}_1) \;\; \cdots \;\; T(\mathbf{e}_n)\,] \tag{3}$$

The matrix $A$ in (3) is called the **standard matrix for the linear transformation $T$**.

We know now that every linear transformation from $\mathbb{R}^n$ to $\mathbb{R}^m$ can be viewed as a matrix transformation, and vice versa. The term *linear transformation* focuses on a property of a mapping, while *matrix transformation* describes how such a mapping is implemented.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| standard matrix | 標準矩陣 | $A = [\,T(\mathbf{e}_1) \;\cdots\; T(\mathbf{e}_n)\,]$,唯一代表 $T$ 的矩陣 |
| $\mathbf{e}_j$ | 第 $j$ 個標準向量 | 單位矩陣的第 $j$ 行:第 $j$ 格是 1、其餘是 0 |
| identity matrix $I_n$ | 單位矩陣 | 對角線是 1、其餘是 0 的 $n \times n$ 矩陣 |
| completely determined by | 完全由……決定 | 知道這些,就知道全部 |
| by inspection | 用看的 | 從公式直接讀出矩陣的每一格(例 3) |

## 白話說
**一句話:一台線性機器,只要知道它把 $\mathbf{e}_1, \dots, \mathbf{e}_n$ 送到哪裡,就完全知道它了。**

理由很短:任何 $\mathbf{x}$ 都能拆成
$$\mathbf{x} = x_1\mathbf{e}_1 + \cdots + x_n\mathbf{e}_n,$$
再用線性(上一個觀念的性質 5):
$$T(\mathbf{x}) = x_1T(\mathbf{e}_1) + \cdots + x_nT(\mathbf{e}_n).$$
右邊是「以 $T(\mathbf{e}_j)$ 為行、以 $x_j$ 為權重」的線性組合,也就是矩陣乘向量。所以

$$A = [\,T(\mathbf{e}_1) \;\; T(\mathbf{e}_2) \;\; \cdots \;\; T(\mathbf{e}_n)\,].$$

**做法**:題目給的是文字描述(旋轉、反射、剪切)?那就問兩件事——「$\mathbf{e}_1$ 跑到哪?」「$\mathbf{e}_2$ 跑到哪?」把答案直的排成兩行,矩陣就出來了。

## 幾何意義
以旋轉 $\varphi$ 角為例:$\mathbf{e}_1 = (1, 0)$ 轉到 $(\cos\varphi, \sin\varphi)$,$\mathbf{e}_2 = (0, 1)$ 轉到 $(-\sin\varphi, \cos\varphi)$。

![課本 Figure 1:旋轉 φ 角把 e1 送到 (cos φ, sin φ)、把 e2 送到 (−sin φ, cos φ)。](rotation-e1e2.svg)

把這兩個像直的排成兩行,就是旋轉矩陣
$$A = \begin{bmatrix} \cos\varphi & -\sin\varphi \\ \sin\varphi & \cos\varphi \end{bmatrix}.$$

## 在資工哪裡用
- **圖學的每一個矩陣都是這樣造出來的**:旋轉、縮放、鏡射、剪切,做法都是「看 $\mathbf{e}_1$、$\mathbf{e}_2$(3D 再加 $\mathbf{e}_3$)跑到哪」。
- **機器學習的權重矩陣**:$W$ 的第 $j$ 行就是「只有第 $j$ 個特徵是 1 時,模型的輸出」。想知道某個特徵的影響,看那一行就好。
- **測試一台黑盒子機器**:丟進 $\mathbf{e}_1, \dots, \mathbf{e}_n$,記錄輸出,就重建出整個矩陣——實作課會這樣做,訊號處理稱之為量測「脈衝響應」。

## 原理
**Theorem 10 的證明**(本週的證明時刻):把 $\mathbf{x}$ 寫成 $I_n\mathbf{x} = x_1\mathbf{e}_1 + \cdots + x_n\mathbf{e}_n$,再用線性把 $T$ 拆進去。

**唯一性**(Exercise 41):若還有一個矩陣 $B$ 滿足 $T(\mathbf{x}) = B\mathbf{x}$,那麼 $B$ 的第 $j$ 行 = $B\mathbf{e}_j = T(\mathbf{e}_j)$ = $A$ 的第 $j$ 行,所以 $A = B$。

**為什麼可以「用看的」寫出矩陣**(例 3、Exercises 15–20):$A\mathbf{x}$ 的第 $i$ 個分量 = 第 $i$ 列和 $\mathbf{x}$ 對應相乘再相加(第 2 週的列向量規則)。所以把 $T(\mathbf{x})$ 的第 $i$ 個分量裡 $x_1, \dots, x_n$ 的係數抄下來,就是第 $i$ 列。

## 老師講解
### 例 1 · Lay 1.9 Example 1
The columns of $I_2 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ are $\mathbf{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ and $\mathbf{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. Suppose $T$ is a linear transformation from $\mathbb{R}^2$ into $\mathbb{R}^3$ such that

$$T(\mathbf{e}_1) = \begin{bmatrix} 5 \\ -7 \\ 2 \end{bmatrix} \quad\text{and}\quad T(\mathbf{e}_2) = \begin{bmatrix} -3 \\ 8 \\ 0 \end{bmatrix}$$

With no additional information, find a formula for the image of an arbitrary $\mathbf{x}$ in $\mathbb{R}^2$.

1. **題目給的資訊看起來很少**:只知道兩個向量的像。但因為 $T$ 是**線性**的,這就夠了。
2. **把 $\mathbf{x}$ 拆開**:
   $$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = x_1\begin{bmatrix} 1 \\ 0 \end{bmatrix} + x_2\begin{bmatrix} 0 \\ 1 \end{bmatrix} = x_1\mathbf{e}_1 + x_2\mathbf{e}_2$$
3. **用線性把 $T$ 拆進去**(上一個觀念的性質 4):
   $$T(\mathbf{x}) = x_1T(\mathbf{e}_1) + x_2T(\mathbf{e}_2)$$
4. **代入已知的兩個像**:
   $$= x_1\begin{bmatrix} 5 \\ -7 \\ 2 \end{bmatrix} + x_2\begin{bmatrix} -3 \\ 8 \\ 0 \end{bmatrix} = \begin{bmatrix} 5x_1 - 3x_2 \\ -7x_1 + 8x_2 \\ 2x_1 + 0 \end{bmatrix}$$
5. **寫成矩陣**:右邊就是 $\begin{bmatrix} 5 & -3 \\ -7 & 8 \\ 2 & 0 \end{bmatrix}\mathbf{x}$,兩行正是 $T(\mathbf{e}_1)$、$T(\mathbf{e}_2)$。
6. **這就是 Theorem 10**:把 $T(\mathbf{e}_j)$ 排成行,就得到標準矩陣。$T : \mathbb{R}^2 \to \mathbb{R}^3$,所以矩陣是 $3 \times 2$(列數 = 對應域、行數 = 定義域)。

### 例 2 · Lay 1.9 Examples 2–3
Find the standard matrix $A$ for the dilation transformation $T(\mathbf{x}) = 3\mathbf{x}$, for $\mathbf{x}$ in $\mathbb{R}^2$. Then let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be the transformation that rotates each point in $\mathbb{R}^2$ about the origin through an angle $\varphi$, with counterclockwise rotation for a positive angle, and find the standard matrix $A$ of this transformation.

1. **伸張:先算兩個像**。$T(\mathbf{e}_1) = 3\mathbf{e}_1 = \begin{bmatrix} 3 \\ 0 \end{bmatrix}$,$T(\mathbf{e}_2) = 3\mathbf{e}_2 = \begin{bmatrix} 0 \\ 3 \end{bmatrix}$。
2. **排成行**:$A = \begin{bmatrix} 3 & 0 \\ 0 & 3 \end{bmatrix}$。
3. **旋轉:$\mathbf{e}_1$ 轉到哪?** 單位圓上、從 $(1, 0)$ 逆時針轉 $\varphi$,就是 $(\cos\varphi, \sin\varphi)$。
4. **$\mathbf{e}_2$ 轉到哪?** 從 $(0, 1)$ 再轉 $\varphi$,落在 $(-\sin\varphi, \cos\varphi)$(見「幾何意義」的圖)。
5. **排成行**:
   $$A = \begin{bmatrix} \cos\varphi & -\sin\varphi \\ \sin\varphi & \cos\varphi \end{bmatrix}$$
6. **檢查特例**:$\varphi = \pi/2$ 時 $\cos\varphi = 0$、$\sin\varphi = 1$,得 $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$——正是上一個觀念例 2 的旋轉 90°。
7. **這招最大的好處**:旋轉這種「文字描述」的變換,不必先猜公式;只要畫出 $\mathbf{e}_1$、$\mathbf{e}_2$ 轉到哪,矩陣自動出現。

## 易錯點
- 把 $T(\mathbf{e}_j)$ 橫著寫成列。它們是**行**。
- 標準矩陣的大小記反:$T : \mathbb{R}^n \to \mathbb{R}^m$ 的矩陣是 $m \times n$(列數 = 對應域維度)。
- 題目說「先做 A 再做 B」時,只做了一半。要把 $\mathbf{e}_j$ **依序**走完兩個步驟(Exercises 7–10)。
- 從公式讀矩陣時漏掉係數 0,例如 $T(x_1, x_2, x_3) = (2x_1 - 3x_3, \dots)$ 的第一列是 $[\,2 \;\; 0 \;\; {-3}\,]$,中間的 0 不能省(Exercise 15)。

## 教學提示
例 1 講完,立刻在黑板上寫下口訣:「**看 $\mathbf{e}_1$ 跑到哪、$\mathbf{e}_2$ 跑到哪,直的排好**」。整個觀念 4 都靠這句話。

旋轉矩陣要當場畫單位圓推導,不要直接抄。學生自己看出 $\mathbf{e}_2$ 的像是 $(-\sin\varphi, \cos\varphi)$ 時,印象最深。

Exercises 15–16(填空缺的矩陣)可以當快問快答;Exercises 17–20 是「證明線性」的標準寫法:找出矩陣就證完了。

課堂建議做:Exercises 1、3、15、17、21;是非 Exercises 23、26;Exercise 13 用圖做。

## 練習
### 照做 · Lay 1.9 Exercises 1–2
Assume that $T$ is a linear transformation. Find the standard matrix of $T$.

(1) $T : \mathbb{R}^2 \to \mathbb{R}^4$, $T(\mathbf{e}_1) = (2, 1, 2, 1)$ and $T(\mathbf{e}_2) = (-5, 2, 0, 0)$, where $\mathbf{e}_1 = (1, 0)$ and $\mathbf{e}_2 = (0, 1)$.

(2) $T : \mathbb{R}^3 \to \mathbb{R}^2$, $T(\mathbf{e}_1) = (1, 3)$, $T(\mathbf{e}_2) = (4, 2)$, and $T(\mathbf{e}_3) = (-5, 4)$, where $\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3$ are the columns of the $3 \times 3$ identity matrix.

#### 解答
把像直的排成行就好。

(1) $A = \begin{bmatrix} 2 & -5 \\ 1 & 2 \\ 2 & 0 \\ 1 & 0 \end{bmatrix}$($4 \times 2$:列數 4 = 對應域,行數 2 = 定義域)(書後解答相同)。

(2) $A = \begin{bmatrix} 1 & 4 & -5 \\ 3 & 2 & 4 \end{bmatrix}$($2 \times 3$)。

### 照做 · Lay 1.9 Exercises 15–16
Fill in the missing entries of the matrix, assuming that the equation holds for all values of the variables.

(15) $\begin{bmatrix} ? & ? & ? \\ ? & ? & ? \\ ? & ? & ? \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 2x_1 - 3x_3 \\ 4x_1 \\ x_1 - x_2 + x_3 \end{bmatrix}$  (16) $\begin{bmatrix} ? & ? \\ ? & ? \\ ? & ? \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} x_1 - 3x_2 \\ -2x_1 + x_2 \\ x_1 \end{bmatrix}$

#### 解答
每一**列**就是那個分量裡 $x_1, x_2, \dots$ 的係數(沒出現的變數係數是 0)。

(15) $\begin{bmatrix} 2 & 0 & -3 \\ 4 & 0 & 0 \\ 1 & -1 & 1 \end{bmatrix}$(書後解答相同)。

(16) $\begin{bmatrix} 1 & -3 \\ -2 & 1 \\ 1 & 0 \end{bmatrix}$。

### 照做 · Lay 1.9 Exercises 17–20
Show that $T$ is a linear transformation by finding a matrix that implements the mapping. Note that $x_1, x_2, \ldots$ are not vectors but are entries in vectors.

(17) $T(x_1, x_2, x_3, x_4) = (0,\ x_1 + x_2,\ x_2 + x_3,\ x_3 + x_4)$  (18) $T(x_1, x_2) = (2x_2 - 3x_1,\ x_1 - 4x_2,\ 0,\ x_2)$

(19) $T(x_1, x_2, x_3) = (x_1 - 5x_2 + 4x_3,\ x_2 - 6x_3)$  (20) $T(x_1, x_2, x_3, x_4) = 2x_1 + 3x_3 - 4x_4$ ($T : \mathbb{R}^4 \to \mathbb{R}$)

#### 解答
找到矩陣就證明了線性(矩陣變換一定線性)。

(17) $A = \begin{bmatrix} 0 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 1 \end{bmatrix}$(書後解答相同)。

(18) $A = \begin{bmatrix} -3 & 2 \\ 1 & -4 \\ 0 & 0 \\ 0 & 1 \end{bmatrix}$(注意第一個分量是 $2x_2 - 3x_1$,係數要照 $x_1, x_2$ 的順序寫)。

(19) $A = \begin{bmatrix} 1 & -5 & 4 \\ 0 & 1 & -6 \end{bmatrix}$(書後解答相同)。

(20) $A = [\,2 \;\; 0 \;\; 3 \;\; {-4}\,]$,是一個 $1 \times 4$ 的矩陣。

### 照做 · Lay 1.9 Exercises 21–22
(21) Let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be a linear transformation such that $T(x_1, x_2) = (x_1 + x_2,\ 4x_1 + 5x_2)$. Find $\mathbf{x}$ such that $T(\mathbf{x}) = (3, 8)$.

(22) Let $T : \mathbb{R}^2 \to \mathbb{R}^3$ be a linear transformation such that $T(x_1, x_2) = (x_1 - 2x_2,\ -x_1 + 3x_2,\ 3x_1 - 2x_2)$. Find $\mathbf{x}$ such that $T(\mathbf{x}) = (-1, 4, 9)$.

#### 解答
先寫出標準矩陣,再解 $A\mathbf{x} = \mathbf{b}$。

(21) $A = \begin{bmatrix} 1 & 1 \\ 4 & 5 \end{bmatrix}$;化簡 $\left[\begin{array}{rr|r} 1 & 1 & 3 \\ 4 & 5 & 8 \end{array}\right] \sim \left[\begin{array}{rr|r} 1 & 0 & 7 \\ 0 & 1 & -4 \end{array}\right]$,得 $\mathbf{x} = \begin{bmatrix} 7 \\ -4 \end{bmatrix}$(書後解答相同)。

(22) $A = \begin{bmatrix} 1 & -2 \\ -1 & 3 \\ 3 & -2 \end{bmatrix}$;化簡 $[\,A \;\; \mathbf{b}\,] \sim \begin{bmatrix} 1 & 0 & 5 \\ 0 & 1 & 3 \\ 0 & 0 & 0 \end{bmatrix}$,得 $\mathbf{x} = \begin{bmatrix} 5 \\ 3 \end{bmatrix}$。

### 是非 · Lay 1.9 Exercise 23
**(T/F)** A linear transformation $T : \mathbb{R}^n \to \mathbb{R}^m$ is completely determined by its effect on the columns of the $n \times n$ identity matrix.

#### 解答
**True.** 由 Theorem 10 的推導:$T(\mathbf{x}) = x_1T(\mathbf{e}_1) + \cdots + x_nT(\mathbf{e}_n)$。知道那 $n$ 個像,就知道所有 $\mathbf{x}$ 的像。

### 是非 · Lay 1.9 Exercise 26
**(T/F)** The columns of the standard matrix for a linear transformation from $\mathbb{R}^n$ to $\mathbb{R}^m$ are the images of the columns of the $n \times n$ identity matrix.

#### 解答
**True.** 這就是 Theorem 10 的式子 $A = [\,T(\mathbf{e}_1) \;\cdots\; T(\mathbf{e}_n)\,]$。

### 是非 · Lay 1.9 Exercise 28
**(T/F)** Not every linear transformation from $\mathbb{R}^n$ to $\mathbb{R}^m$ is a matrix transformation.

#### 解答
**False.** Theorem 10 說每個 $T : \mathbb{R}^n \to \mathbb{R}^m$ 的線性變換都是矩陣變換(標準矩陣就是那個矩陣)。

#### 備註
和上一個觀念的是非題 Exercise 27 對照著看:那題問的是**一般**的線性變換(含第 4、5 章的函數空間),答案是「不是每個都是矩陣變換」;這題限定 $\mathbb{R}^n \to \mathbb{R}^m$,答案就反過來了。

### 變化 · Lay 1.9 Exercises 13–14
(13) Let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be the linear transformation such that $T(\mathbf{e}_1)$ and $T(\mathbf{e}_2)$ are the vectors shown in the figure. Using the figure, sketch the vector $T(2, 1)$.

![Exercise 13 的圖:T(e1) 指向左上,T(e2) 指向右方。](ex13-vectors.svg)

(14) Let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be a linear transformation with standard matrix $A = [\,\mathbf{a}_1 \;\; \mathbf{a}_2\,]$, where $\mathbf{a}_1$ and $\mathbf{a}_2$ are shown in the figure. Using the figure, draw the image of $\begin{bmatrix} -1 \\ 3 \end{bmatrix}$ under the transformation $T$.

![Exercise 14 的圖:a1 指向右下,a2 指向右上。](ex14-vectors.svg)

#### 解答
(13) $(2, 1) = 2\mathbf{e}_1 + \mathbf{e}_2$,所以由線性
$$T(2, 1) = 2T(\mathbf{e}_1) + T(\mathbf{e}_2).$$
畫法:把 $T(\mathbf{e}_1)$ 延長一倍得到 $2T(\mathbf{e}_1)$,再和 $T(\mathbf{e}_2)$ 作平行四邊形;對角線就是 $T(2, 1)$,大約指向正上方、略偏右。

(14) $A\begin{bmatrix} -1 \\ 3 \end{bmatrix} = -\mathbf{a}_1 + 3\mathbf{a}_2$。畫出 $-\mathbf{a}_1$(把 $\mathbf{a}_1$ 反向)與 $3\mathbf{a}_2$,再用平行四邊形法則相加,結果落在第一象限、指向右上方而且相當高。

#### 備註
這兩題完全不用算矩陣:標準矩陣的行就是 $T(\mathbf{e}_j)$,而 $A\mathbf{x}$ 就是「用 $\mathbf{x}$ 的分量當權重,把各行組合起來」(第 2 週觀念 4)。

### 挑戰 · Lay 1.9 Exercise 41
Verify the uniqueness of $A$ in Theorem 10. Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation such that $T(\mathbf{x}) = B\mathbf{x}$ for some $m \times n$ matrix $B$. Show that if $A$ is the standard matrix for $T$, then $A = B$. [*Hint:* Show that $A$ and $B$ have the same columns.]

#### 解答
依標準矩陣的定義,$A$ 的第 $j$ 行是 $T(\mathbf{e}_j)$。另一方面 $T(\mathbf{e}_j) = B\mathbf{e}_j$,而 $B\mathbf{e}_j$ 就是 $B$ 的第 $j$ 行(權重只有第 $j$ 個是 1)。所以對每個 $j$,$A$ 與 $B$ 的第 $j$ 行相同,因此 $A = B$(書後提示相同)。

#### 備註
這題說明「標準矩陣」為什麼可以叫做**那個**矩陣:代表同一個線性變換的矩陣只有一個。

## 驗算
```check
Matrix([[5, -3], [-7, 8], [2, 0]]) * Matrix([x1, x2]) == Matrix([5*x1 - 3*x2, -7*x1 + 8*x2, 2*x1])
Matrix([[3, 0], [0, 3]]) * Matrix([x1, x2]) == 3 * Matrix([x1, x2])
Matrix([[cos(pi/2), -sin(pi/2)], [sin(pi/2), cos(pi/2)]]) == Matrix([[0, -1], [1, 0]])
Matrix.hstack(Matrix([2, 1, 2, 1]), Matrix([-5, 2, 0, 0])) == Matrix([[2, -5], [1, 2], [2, 0], [1, 0]])
Matrix([[1, 4, -5], [3, 2, 4]]) * Matrix([x1, x2, x3]) == x1 * Matrix([1, 3]) + x2 * Matrix([4, 2]) + x3 * Matrix([-5, 4])
Matrix([[2, 0, -3], [4, 0, 0], [1, -1, 1]]) * Matrix([x1, x2, x3]) == Matrix([2*x1 - 3*x3, 4*x1, x1 - x2 + x3])
Matrix([[1, -3], [-2, 1], [1, 0]]) * Matrix([x1, x2]) == Matrix([x1 - 3*x2, -2*x1 + x2, x1])
Matrix([[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]) * Matrix([x1, x2, x3, x4]) == Matrix([0, x1 + x2, x2 + x3, x3 + x4])
Matrix([[-3, 2], [1, -4], [0, 0], [0, 1]]) * Matrix([x1, x2]) == Matrix([2*x2 - 3*x1, x1 - 4*x2, 0, x2])
Matrix([[1, -5, 4], [0, 1, -6]]) * Matrix([x1, x2, x3]) == Matrix([x1 - 5*x2 + 4*x3, x2 - 6*x3])
Matrix([[2, 0, 3, -4]]) * Matrix([x1, x2, x3, x4]) == Matrix([2*x1 + 3*x3 - 4*x4])
Matrix([[1, 1], [4, 5]]).solve(Matrix([3, 8])) == Matrix([7, -4])
Matrix([[1, -2], [-1, 3], [3, -2]]) * Matrix([5, 3]) == Matrix([-1, 4, 9])
Matrix.hstack(Matrix([a, b]), Matrix([c, d])) * Matrix([2, 1]) == 2 * Matrix([a, b]) + Matrix([c, d])
Matrix.hstack(Matrix([a, b]), Matrix([c, d])) * Matrix([-1, 3]) == -Matrix([a, b]) + 3 * Matrix([c, d])
Matrix([[a, b, c], [d, f, g]]) * Matrix([0, 1, 0]) == Matrix([[a, b, c], [d, f, g]])[:, 1]
```
