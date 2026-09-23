---
title_en: Onto and One-to-One Mappings
title_zh: 映成與一對一:存在性與唯一性的新說法
sub: Onto = pivot in every row; one-to-one = pivot in every column
level: hard
source: Lay 1.9
lab_hook: '`A.rank()` 和列數、行數比一比:等於列數 → 映成;等於行數 → 一對一'
---
## 觀念
**Definition (onto).** A mapping $T : \mathbb{R}^n \to \mathbb{R}^m$ is said to be **onto** $\mathbb{R}^m$ if each $\mathbf{b}$ in $\mathbb{R}^m$ is the image of *at least one* $\mathbf{x}$ in $\mathbb{R}^n$.

Equivalently, $T$ is onto $\mathbb{R}^m$ when the range of $T$ is all of the codomain $\mathbb{R}^m$. "Does $T$ map $\mathbb{R}^n$ onto $\mathbb{R}^m$?" is an existence question.

**Definition (one-to-one).** A mapping $T : \mathbb{R}^n \to \mathbb{R}^m$ is said to be **one-to-one** if each $\mathbf{b}$ in $\mathbb{R}^m$ is the image of *at most one* $\mathbf{x}$ in $\mathbb{R}^n$.

Equivalently, $T$ is one-to-one if, for each $\mathbf{b}$ in $\mathbb{R}^m$, the equation $T(\mathbf{x}) = \mathbf{b}$ has either a unique solution or none at all. "Is $T$ one-to-one?" is a uniqueness question.

**Theorem 11.** Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation. Then $T$ is one-to-one if and only if the equation $T(\mathbf{x}) = \mathbf{0}$ has only the trivial solution.

**Theorem 12.** Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation, and let $A$ be the standard matrix for $T$. Then:

- **a.** $T$ maps $\mathbb{R}^n$ onto $\mathbb{R}^m$ if and only if the columns of $A$ span $\mathbb{R}^m$;
- **b.** $T$ is one-to-one if and only if the columns of $A$ are linearly independent.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| onto | 映成(滿射) | 每個 $\mathbf{b}$ **至少**是一個 $\mathbf{x}$ 的像;值域 = 對應域 |
| one-to-one | 一對一(單射) | 每個 $\mathbf{b}$ **至多**是一個 $\mathbf{x}$ 的像 |
| at least one / at most one | 至少一個 / 至多一個 | 存在性用「至少」,唯一性用「至多」 |
| existence question | 存在性問題 | 映成問的是有沒有解 |
| uniqueness question | 唯一性問題 | 一對一問的是解唯不唯一 |

## 白話說
兩個詞,兩個老問題:

- **映成**:對應域裡的每個目標,**都打得到**(至少一個 $\mathbf{x}$ 打得到它)。這是第 2 週 Theorem 4 的說法換了一個名字。
- **一對一**:不同的輸入不會撞成同一個輸出(每個目標**至多**被打到一次)。這是「唯一性」。

翻成 pivot 的語言,兩句話就結束了($A$ 是 $m \times n$ 的標準矩陣):

| 問題 | 條件 | 怎麼檢查 |
|---|---|---|
| $T$ 映成 ℝᵐ 嗎? | $A$ 的行生成 ℝᵐ | **每一列**都有 pivot(第 2 週 Theorem 4) |
| $T$ 一對一嗎? | $A$ 的行線性獨立 | **每一行**都有 pivot(第 3 週) |

**立刻得到的兩個推論**(Exercise 43):

- 要**映成**,列不能比行多 → $m \le n$。
- 要**一對一**,行不能比列多 → $n \le m$。
- 兩個都要,就必須 $m = n$(方陣)。

## 幾何意義
![三種情況:左邊不是映成(值域比對應域小),中間不是一對一(兩個輸入撞在一起),右邊又一對一又映成。](onto-one-to-one.svg)

用第 3、4 個觀念的變換來看:

- **投影**到 $x_1$ 軸:不是映成(打不到 $x_1$ 軸以外的點),也不是一對一($(1, 3)$ 和 $(1, 7)$ 都被壓到 $(1, 0)$)。
- **反射、剪切、伸縮**(表 1–3):既是一對一、也是映成 ℝ²。

## 在資工哪裡用
- **雜湊函數**:理想的雜湊要「盡量一對一」(不同資料不要撞在一起,撞到叫 collision)。線性的情況下,一對一 ⇔ 各行獨立。
- **編碼與壓縮**:編碼器 $\mathbb{R}^n \to \mathbb{R}^m$ 若一對一,就表示編碼後**沒有資訊損失**,可以解回來;$n > m$ 時不可能一對一,一定有損失——這就是有損壓縮的數學理由。
- **神經網路的輸出層**:要能輸出任意目標向量,就要映成,也就是權重矩陣每一列都有 pivot。
- **可逆**:既一對一又映成的線性變換才有「反變換」,對應到第 6 週的可逆矩陣。

## 原理
**Theorem 11 的證明**(課本 p. 105)。$T$ 線性,所以 $T(\mathbf{0}) = \mathbf{0}$。

- 若 $T$ 一對一:$T(\mathbf{x}) = \mathbf{0}$ 至多一個解,而 $\mathbf{0}$ 已經是解,所以只有平凡解。
- 若 $T$ **不**一對一:有某個 $\mathbf{b}$ 是兩個不同向量 $\mathbf{u} \neq \mathbf{v}$ 的像。由線性,
  $$T(\mathbf{u} - \mathbf{v}) = T(\mathbf{u}) - T(\mathbf{v}) = \mathbf{b} - \mathbf{b} = \mathbf{0},$$
  而 $\mathbf{u} - \mathbf{v} \neq \mathbf{0}$,所以 $T(\mathbf{x}) = \mathbf{0}$ 有非平凡解。

兩個條件同真同假,得證。(課本的 Remark 提醒:證「若且唯若」可以用「$P$ 真 ⇒ $Q$ 真」加上「$P$ 假 ⇒ $Q$ 假」,後者叫**逆否推理**。)

**Theorem 12 的證明**(課本 p. 106)。

- **(a)** 由第 2 週 Theorem 4:各行生成 ℝᵐ ⇔ 每個 $\mathbf{b}$ 都讓 $A\mathbf{x} = \mathbf{b}$ 相容 ⇔ 每個 $\mathbf{b}$ 都是某個 $\mathbf{x}$ 的像 ⇔ $T$ 映成。
- **(b)** $T(\mathbf{x}) = \mathbf{0}$ 和 $A\mathbf{x} = \mathbf{0}$ 是同一條式子。由 Theorem 11,$T$ 一對一 ⇔ 只有平凡解 ⇔ 各行線性獨立(第 3 週)。

## 老師講解
### 例 1 · Lay 1.9 Example 4
Let $T$ be the linear transformation whose standard matrix is

$$A = \begin{bmatrix} 1 & -4 & 8 & 1 \\ 0 & 2 & -1 & 3 \\ 0 & 0 & 0 & 5 \end{bmatrix}$$

Does $T$ map $\mathbb{R}^4$ onto $\mathbb{R}^3$? Is $T$ a one-to-one mapping?

1. **先看形狀**:$A$ 是 $3 \times 4$,所以 $T : \mathbb{R}^4 \to \mathbb{R}^3$。
2. **$A$ 剛好已經是梯形**,可以直接數 pivot:第 1、2、4 行各有一個,共 3 個。
3. **映成?看列**:3 列都有 pivot,由第 2 週 Theorem 4,各行生成 ℝ³ → $T$ **映成** ℝ³。
4. **一對一?看行**:4 行只有 3 個 pivot,第 3 行沒有 → 有自由變數 → $A\mathbf{x} = \mathbf{0}$ 有非平凡解 → 由 Theorem 11,$T$ **不是**一對一。
5. **用「至多/至少」再講一次**:每個 $\mathbf{b}$ 都打得到(至少一個),但每個 $\mathbf{b}$ 其實被**無限多個** $\mathbf{x}$ 打到,所以不是一對一。
6. **形狀先天的限制**:定義域 ℝ⁴ 比對應域 ℝ³ 「大」,擠進去一定會有人撞在一起($n > m$ 不可能一對一)。

### 例 2 · Lay 1.9 Example 5
Let $T(x_1, x_2) = (3x_1 + x_2,\ 5x_1 + 7x_2,\ x_1 + 3x_2)$. Show that $T$ is a one-to-one linear transformation. Does $T$ map $\mathbb{R}^2$ onto $\mathbb{R}^3$?

1. **用看的寫出標準矩陣**(觀念 3 的方法):把每個分量裡 $x_1, x_2$ 的係數抄成一列:
   $$T(\mathbf{x}) = \begin{bmatrix} 3x_1 + x_2 \\ 5x_1 + 7x_2 \\ x_1 + 3x_2 \end{bmatrix} = \begin{bmatrix} 3 & 1 \\ 5 & 7 \\ 1 & 3 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$$
2. **找到矩陣就證明了線性**(矩陣變換一定線性)。
3. **一對一?** 兩行不是彼此的倍數 → 線性獨立(第 3 週:兩個向量看倍數)→ 由 Theorem 12(b),$T$ **是**一對一。
4. **映成 ℝ³?** 要各行生成 ℝ³,由 Theorem 4 需要 3 個 pivot;但 $A$ 只有 **2 行**,最多 2 個 pivot。
5. **結論**:$T$ **不是**映成 ℝ³。幾何上,$T$ 把整個平面送到 ℝ³ 裡的一個平面 $\operatorname{Span}\{\mathbf{a}_1, \mathbf{a}_2\}$ 上,平面外的點永遠打不到(課本 p. 106 的邊圖)。
6. **對照例 1**:例 1 是「胖」矩陣($3 \times 4$):映成、不一對一;這裡是「瘦」矩陣($3 \times 2$):一對一、不映成。**形狀就先決定了一半的答案**。

## 易錯點
- 把「每個 $\mathbf{x}$ 都有唯一的像」當成一對一。**每個**函數都這樣;一對一講的是反過來:每個**像**至多來自一個 $\mathbf{x}$(是非題 Exercise 24)。
- 把「每個 $\mathbf{x}$ 都被送到某處」當成映成(是非題 Exercise 29)。映成講的是**對應域**裡每個 $\mathbf{b}$ 都被打到。
- 映成看行、一對一看列(弄反)。正確是:**映成看每一列有沒有 pivot、一對一看每一行有沒有 pivot**。
- 以為 $3 \times 2$ 的矩陣不可能一對一(是非題 Exercise 31)。它不可能**映成** ℝ³,但很可能是一對一。

## 教學提示
先用「打靶」比喻:對應域是整面靶,值域是實際打到的區域。**映成** = 整面靶都打得到;**一對一** = 沒有兩箭射在同一點。

把這張對照表寫在黑板上,整學期沿用:

| | 看哪裡 | 第幾週學的 |
|---|---|---|
| 映成 | 每一**列**有 pivot | 第 2 週 Theorem 4 |
| 一對一 | 每一**行**有 pivot | 第 3 週線性獨立 |

例 1、例 2 要並排:一個是胖矩陣、一個是瘦矩陣,答案剛好相反。

課堂建議做:Exercises 33、35、37;是非 Exercises 24、29、31、32;Practice Problem 2。T 題(Exercises 45–48)留給實作課。

## 練習
### 照做 · Lay 1.9 Exercises 33–35
Determine if the specified linear transformation is (a) one-to-one and (b) onto. Justify each answer.

(33) The transformation in Exercise 17: $T(x_1, x_2, x_3, x_4) = (0,\ x_1 + x_2,\ x_2 + x_3,\ x_3 + x_4)$.

(34) The transformation in Exercise 2: $T : \mathbb{R}^3 \to \mathbb{R}^2$ with $T(\mathbf{e}_1) = (1, 3)$, $T(\mathbf{e}_2) = (4, 2)$, $T(\mathbf{e}_3) = (-5, 4)$.

(35) The transformation in Exercise 19: $T(x_1, x_2, x_3) = (x_1 - 5x_2 + 4x_3,\ x_2 - 6x_3)$.

#### 解答
(33) $A = \begin{bmatrix} 0 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 1 \end{bmatrix}$,只有 3 個 pivot。(a) **不是**一對一:4 行只有 3 個 pivot,例如 $T(1, -1, 1, -1) = \mathbf{0}$。(b) **不是**映成 ℝ⁴:第一列沒有 pivot(第一個分量永遠是 0),$(1, 0, 0, 0)$ 打不到(書後解答相同)。

(34) $A = \begin{bmatrix} 1 & 4 & -5 \\ 3 & 2 & 4 \end{bmatrix}$,2 個 pivot。(a) **不是**一對一:3 個行向量在 ℝ² 裡,必相依(第 3 週 Theorem 8)。(b) **是**映成 ℝ²:兩列都有 pivot。

(35) $A = \begin{bmatrix} 1 & -5 & 4 \\ 0 & 1 & -6 \end{bmatrix}$ 已是梯形,2 個 pivot。(a) **不是**一對一($x_3$ 自由,例如 $T(26, 6, 1) = \mathbf{0}$)。(b) **是**映成 ℝ²(每列都有 pivot)(書後解答相同)。

### 照做 · Lay 1.9 Practice Problem 2
Suppose $A$ is a $7 \times 5$ matrix with 5 pivots. Let $T(\mathbf{x}) = A\mathbf{x}$ be a linear transformation from $\mathbb{R}^5$ into $\mathbb{R}^7$. Is $T$ a one-to-one linear transformation? Is $T$ onto $\mathbb{R}^7$?

#### 解答
$A$ 有 5 行、5 個 pivot → 每一行都有 pivot → 各行線性獨立 → 由 Theorem 12,$T$ **是一對一**。

$A$ 有 7 列但只有 5 個 pivot → 不是每一列都有 pivot → 各行不生成 ℝ⁷ → 由 Theorem 12,$T$ **不是映成**(課本 p. 109)。

### 是非 · Lay 1.9 Exercise 24
**(T/F)** A mapping $T : \mathbb{R}^n \to \mathbb{R}^m$ is one-to-one if each vector in $\mathbb{R}^n$ maps onto a unique vector in $\mathbb{R}^m$.

#### 解答
**False.** 每個**函數**都把每個 $\mathbf{x}$ 送到唯一一個像。一對一要求的是反方向:每個 $\mathbf{b}$ **至多**來自一個 $\mathbf{x}$。反例:投影到 $x_1$ 軸把 $(1, 0)$ 和 $(1, 5)$ 送到同一點。

### 是非 · Lay 1.9 Exercise 29
**(T/F)** A mapping $T : \mathbb{R}^n \to \mathbb{R}^m$ is onto $\mathbb{R}^m$ if every vector $\mathbf{x}$ in $\mathbb{R}^n$ maps onto some vector in $\mathbb{R}^m$.

#### 解答
**False.** 那是每個函數都會做的事。映成要求**對應域**裡每個 $\mathbf{b}$ 都被打到。反例:投影到 $x_1$ 軸,$(0, 1)$ 永遠打不到。

### 是非 · Lay 1.9 Exercise 31
**(T/F)** $A$ is a $3 \times 2$ matrix, then the transformation $\mathbf{x} \mapsto A\mathbf{x}$ cannot be one-to-one.

#### 解答
**False.** $3 \times 2$ 的矩陣只要兩行線性獨立就是一對一,例如 $A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$,或例 2 的矩陣。

#### 備註
課本這句話開頭漏了「If」,照原文收錄。

### 是非 · Lay 1.9 Exercise 32
**(T/F)** $A$ is a $3 \times 2$ matrix, then the transformation $\mathbf{x} \mapsto A\mathbf{x}$ cannot map $\mathbb{R}^2$ onto $\mathbb{R}^3$.

#### 解答
**True.** $3 \times 2$ 最多 2 個 pivot,3 列不可能都有 pivot,所以各行不可能生成 ℝ³(Theorem 12(a) 與第 2 週 Theorem 4)。

#### 備註
和 Exercise 31 並排看:同一個形狀的矩陣,**可能**一對一,但**不可能**映成。

### 變化 · Lay 1.9 Exercise 36
Determine if the linear transformation in Exercise 14 is (a) one-to-one and (b) onto. Justify each answer.

![Exercise 14 的圖:標準矩陣的兩行 a1 與 a2。](ex14-vectors.svg)

#### 解答
圖上 $\mathbf{a}_1$ 指向右下、$\mathbf{a}_2$ 指向右上,方向不同也不相反,所以**不是彼此的倍數** → 兩行線性獨立。

(a) 由 Theorem 12(b),$T$ **是**一對一。
(b) $A$ 是 $2 \times 2$ 且兩行獨立 → 2 個 pivot,每一列都有 → 由 Theorem 12(a),$T$ **是**映成 ℝ²。

### 變化 · Lay 1.9 Exercises 37–38
Describe the possible echelon forms of the standard matrix for a linear transformation $T$. Use the notation of Example 1 in Section 1.2.

(37) $T : \mathbb{R}^3 \to \mathbb{R}^4$ is one-to-one. (38) $T : \mathbb{R}^4 \to \mathbb{R}^3$ is onto.

#### 解答
■ 是不為 0 的 pivot,$*$ 是任意數。

(37) $A$ 是 $4 \times 3$,一對一 ⇔ 3 行都是 pivot 行:
$$\begin{bmatrix} ■ & * & * \\ 0 & ■ & * \\ 0 & 0 & ■ \\ 0 & 0 & 0 \end{bmatrix}$$
只有這一種(書後解答相同)。

(38) $A$ 是 $3 \times 4$,映成 ⇔ 3 列都有 pivot。pivot 可能落在第 1-2-3、1-2-4、1-3-4 或 2-3-4 行:
$$\begin{bmatrix} ■ & * & * & * \\ 0 & ■ & * & * \\ 0 & 0 & ■ & * \end{bmatrix},\quad \begin{bmatrix} ■ & * & * & * \\ 0 & ■ & * & * \\ 0 & 0 & 0 & ■ \end{bmatrix},\quad \begin{bmatrix} ■ & * & * & * \\ 0 & 0 & ■ & * \\ 0 & 0 & 0 & ■ \end{bmatrix},\quad \begin{bmatrix} 0 & ■ & * & * \\ 0 & 0 & ■ & * \\ 0 & 0 & 0 & ■ \end{bmatrix}$$

### 變化 · Lay 1.9 Exercises 39–40
(39) Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation, with $A$ its standard matrix. Complete the following statement to make it true: "$T$ is one-to-one if and only if $A$ has \_\_\_\_\_ pivot columns." Explain why the statement is true. [*Hint:* Look in the exercises for Section 1.7.]

(40) Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation, with $A$ its standard matrix. Complete the following statement to make it true: "$T$ maps $\mathbb{R}^n$ onto $\mathbb{R}^m$ if and only if $A$ has \_\_\_\_\_ pivot columns." Find some theorems that explain why the statement is true.

#### 解答
(39) **$n$ 個**(書後解答相同)。理由:$T$ 一對一 ⇔ 各行獨立(Theorem 12(b))⇔ $A\mathbf{x} = \mathbf{0}$ 只有平凡解 ⇔ 沒有自由變數 ⇔ $n$ 行全是 pivot 行。

(40) **$m$ 個**。理由:$T$ 映成 ⇔ 各行生成 ℝᵐ(Theorem 12(a))⇔ $A$ 的每一**列**都有 pivot(第 2 週 Theorem 4)⇔ 有 $m$ 個 pivot,而每個 pivot 各佔一行,所以有 $m$ 個 pivot 行。

#### 備註
兩題並排,正好把「一對一數行、映成數列」變成同一句話:**pivot 行的個數**等於 $n$ 就一對一,等於 $m$ 就映成。

### 應用 · Lay 1.9 Exercises 45–46
**[T]** Let $T$ be the linear transformation whose standard matrix is given. Decide if $T$ is a one-to-one mapping. Justify your answer.

(45) $\begin{bmatrix} -5 & 10 & -5 & 4 \\ 8 & 3 & -4 & 7 \\ 4 & -9 & 5 & -3 \\ -3 & -2 & 5 & 4 \end{bmatrix}$  (46) $\begin{bmatrix} 7 & 5 & 4 & -9 \\ 10 & 6 & 16 & -4 \\ 12 & 8 & 12 & 7 \\ -8 & -6 & -2 & 5 \end{bmatrix}$

#### 解答
(45) 化簡後只有 3 個 pivot 行(第 1、2、3 行),第 4 行沒有 → 各行相依 → **不是**一對一(書後解答:No)。具體的非平凡解:$A(-44, -79, -86, 35) = \mathbf{0}$。

(46) 同樣只有 3 個 pivot(pivot 行是第 1、2、4 行)→ **不是**一對一。具體關係:$-7\mathbf{a}_1 + 9\mathbf{a}_2 + \mathbf{a}_3 = \mathbf{0}$。

#### 備註
課本標 T,實作課 ④ 用 `rank()` 與 `nullspace()` 做。

### 應用 · Lay 1.9 Exercises 47–48
**[T]** Let $T$ be the linear transformation whose standard matrix is given. Decide if $T$ maps $\mathbb{R}^5$ onto $\mathbb{R}^5$. Justify your answer.

(47) $\begin{bmatrix} 4 & -7 & 3 & 7 & 5 \\ 6 & -8 & 5 & 12 & -8 \\ -7 & 10 & -8 & -9 & 14 \\ 3 & -5 & 4 & 2 & -6 \\ -5 & 6 & -6 & -7 & 3 \end{bmatrix}$  (48) $\begin{bmatrix} 9 & 13 & 5 & 6 & -1 \\ 14 & 15 & -7 & -6 & 4 \\ -8 & -9 & 12 & -5 & -9 \\ -5 & -6 & -8 & 9 & 8 \\ 13 & 14 & 15 & 2 & 11 \end{bmatrix}$

#### 解答
(47) 只有 4 個 pivot(pivot 行是第 1、2、3、5 行),5 列中有一列沒有 pivot → 各行不生成 ℝ⁵ → **不是**映成(書後解答:No)。

(48) 同樣只有 4 個 pivot(第 1–4 行)→ **不是**映成 ℝ⁵。

#### 備註
兩題都是方陣:方陣一旦不是映成,也一定不是一對一(pivot 少於 5 就兩邊都缺)——這正是第 6 週可逆矩陣定理的內容。

### 挑戰 · Lay 1.9 Exercises 42–43
(42) Why is the question "Is the linear transformation $T$ onto?" an existence question?

(43) If a linear transformation $T : \mathbb{R}^n \to \mathbb{R}^m$ maps $\mathbb{R}^n$ *onto* $\mathbb{R}^m$, can you give a relation between $m$ and $n$? If $T$ is one-to-one, what can you say about $m$ and $n$?

#### 解答
(42) $T$ 映成的意思是:對**每個** $\mathbf{b}$,方程式 $T(\mathbf{x}) = \mathbf{b}$(也就是 $A\mathbf{x} = \mathbf{b}$)**至少有一個解**。問的是解存不存在,所以是存在性問題。

(43) 標準矩陣 $A$ 是 $m \times n$,pivot 最多 $\min(m, n)$ 個。

- 映成需要每一列都有 pivot,共 $m$ 個 → 需要 $m \le n$。
- 一對一需要每一行都有 pivot,共 $n$ 個 → 需要 $n \le m$。
- 兩者都成立時 $m = n$(書後提示:$m > n$ 可能嗎?$m < n$ 呢?)。

#### 備註
這一題的結論很好記:**「矮胖」的矩陣可能映成、不可能一對一;「瘦高」的可能一對一、不可能映成。**

## 驗算
```check
Matrix([[1, -4, 8, 1], [0, 2, -1, 3], [0, 0, 0, 5]]).rank() == 3
len(Matrix([[1, -4, 8, 1], [0, 2, -1, 3], [0, 0, 0, 5]]).nullspace()) == 1
Matrix([[3, 1], [5, 7], [1, 3]]) * Matrix([x1, x2]) == Matrix([3*x1 + x2, 5*x1 + 7*x2, x1 + 3*x2])
Matrix([[3, 1], [5, 7], [1, 3]]).rank() == 2 and Matrix([[3, 1], [5, 7], [1, 3]]).nullspace() == []
Matrix([[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]).rank() == 3
Matrix([[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]) * Matrix([1, -1, 1, -1]) == zeros(4, 1)
Matrix([[1, 4, -5], [3, 2, 4]]).rank() == 2 and len(Matrix([[1, 4, -5], [3, 2, 4]]).nullspace()) == 1
Matrix([[1, -5, 4], [0, 1, -6]]) * Matrix([26, 6, 1]) == zeros(2, 1)
Matrix.vstack(eye(5), zeros(2, 5)).rank() == 5
Matrix([[1, 0], [0, 0]]) * Matrix([1, 0]) == Matrix([[1, 0], [0, 0]]) * Matrix([1, 5])
Matrix([[1, 0], [0, 0]]).rank() < 2
Matrix([[1, 0], [0, 1], [0, 0]]).nullspace() == []
Matrix([[1, 2], [3, 4], [5, 6]]).rank() < 3
Matrix([[Rational(391, 10), Rational(212, 10)], [Rational(-143, 10), Rational(125, 10)]]).rank() == 2
Matrix([[2, 5, -1], [0, 3, 7], [0, 0, -4], [0, 0, 0]]).nullspace() == []
all(Matrix(M).rank() == 3 for M in [[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], [[1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]])
Matrix([[-5, 10, -5, 4], [8, 3, -4, 7], [4, -9, 5, -3], [-3, -2, 5, 4]]).rank() == 3
Matrix([[-5, 10, -5, 4], [8, 3, -4, 7], [4, -9, 5, -3], [-3, -2, 5, 4]]) * Matrix([-44, -79, -86, 35]) == zeros(4, 1)
Matrix([[7, 5, 4, -9], [10, 6, 16, -4], [12, 8, 12, 7], [-8, -6, -2, 5]]) * Matrix([-7, 9, 1, 0]) == zeros(4, 1)
Matrix([[4, -7, 3, 7, 5], [6, -8, 5, 12, -8], [-7, 10, -8, -9, 14], [3, -5, 4, 2, -6], [-5, 6, -6, -7, 3]]).rank() == 4
Matrix([[9, 13, 5, 6, -1], [14, 15, -7, -6, 4], [-8, -9, 12, -5, -9], [-5, -6, -8, 9, 8], [13, 14, 15, 2, 11]]).rank() == 4
```
