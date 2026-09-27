---
title_en: Subspaces of Rⁿ
title_zh: 子空間:對加法與純量乘法封閉的集合
sub: Closed under addition and scalar multiplication
level: mid
source: Lay 2.8
lab_hook: '檢查一個集合是不是子空間,程式上就是檢查「組合完還在不在裡面」'
---
## 觀念
**Definition.** A **subspace** of $\mathbb{R}^n$ is any set $H$ in $\mathbb{R}^n$ that has three properties:

- **a.** The zero vector is in $H$.
- **b.** For each $\mathbf{u}$ and $\mathbf{v}$ in $H$, the sum $\mathbf{u} + \mathbf{v}$ is in $H$.
- **c.** For each $\mathbf{u}$ in $H$ and each scalar $c$, the vector $c\mathbf{u}$ is in $H$.

In words, a subspace is *closed* under addition and scalar multiplication.

If $\mathbf{v}_1, \dots, \mathbf{v}_p$ are in $\mathbb{R}^n$, then $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ is a subspace of $\mathbb{R}^n$. We call $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ the **subspace spanned (or generated) by $\mathbf{v}_1, \dots, \mathbf{v}_p$**.

The set consisting of only the zero vector in $\mathbb{R}^n$ is a subspace of $\mathbb{R}^n$, called the **zero subspace**.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| subspace | 子空間 | $\mathbb{R}^n$ 裡面「自成一個世界」的集合 |
| closed under addition | 對加法封閉 | 裡面兩個相加,結果還在裡面 |
| closed under scalar multiplication | 對純量乘法封閉 | 裡面的向量乘任何實數,結果還在裡面 |
| zero subspace | 零子空間 | 只含 $\mathbf{0}$ 的那個集合,寫成 $\{\mathbf{0}\}$ |
| spanned (generated) by | 由……張成(生成) | $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ |
| bounding line | 邊界線 | 區域的邊,習題 1–4 說「含邊界」 |

## 白話說
**一句話:子空間就是「你在裡面怎麼做加法與乘法,都跑不出去」的集合。**

三個條件不是隨便訂的,它們正好對應到我們一直在做的兩件事——**相加**與**乘倍數**,也就是「取線性組合」。子空間的意思就是:**對線性組合封閉**。

為什麼要有第一條(含 $\mathbf{0}$)?因為如果 $H$ 非空且對純量乘法封閉,取 $c = 0$ 就得到 $\mathbf{0} \in H$。所以第一條真正排除的是**空集合**,順便提供一個最快的否定判準:

> **看到不含原點,立刻判定不是子空間。**

**三個最常見的子空間:**

| 子空間 | 是什麼 |
|---|---|
| $\{\mathbf{0}\}$ | 只有原點。是子空間(三條都成立),維度 0 |
| $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ | 所有線性組合。**永遠是**子空間 |
| $\mathbb{R}^n$ 自己 | 整個空間也算自己的子空間 |

**怎麼證明「是」子空間?** 最省力的方法是**把它寫成某組向量的 Span**——因為 Span 一定是子空間,不必逐條驗。

**怎麼證明「不是」?** 只要找**一個反例**:一個 $\mathbf{u} \in H$ 和一個純量 $c$ 使 $c\mathbf{u} \notin H$,或兩個 $\mathbf{u}, \mathbf{v} \in H$ 使 $\mathbf{u} + \mathbf{v} \notin H$。**一個反例就夠了**,不必三條都破。

## 幾何意義
$\mathbb{R}^2$ 裡的子空間只有三種:$\{\mathbf{0}\}$、**通過原點的直線**、整個 $\mathbb{R}^2$。
$\mathbb{R}^3$ 裡多一種:$\{\mathbf{0}\}$、過原點的直線、**過原點的平面**、整個 $\mathbb{R}^3$。

**「過原點」這三個字是關鍵。** 不過原點的直線連第一條都不滿足。

下面四個區域都**不是**子空間,每一個壞在不同的地方——這正是課本 Exercises 1–4:

![四個區域:第一象限、第一與第三象限、沿 $x_2 = x_1$ 的帶狀區、過原點直線上方的半平面。](subspace-tests.svg)

- **(1) 第一象限**:加法沒問題,但乘 $-1$ 就跑到第三象限。
- **(2) 第一 + 第三象限**:乘純量沒問題(留在同一對象限),但跨象限相加會跑到第二象限。
- **(3) 帶狀區**:有「寬度上限」,把邊界上的點放大兩倍就撐出去了。加法與純量乘法**兩條都壞**。
- **(4) 半平面**:含原點、對加法封閉、對正數倍封閉,但乘 $-1$ 就掉到線的另一邊。

**注意 (3) 的陷阱**:帶狀區的**中線** $x_2 = x_1$ 本身是子空間,所以舉反例時**不能**挑中線上的點。

## 在資工哪裡用
- **子空間 = 系統的「可能狀態集合」**。一個線性系統所有可能的輸出、所有可能的解、所有合法的碼字,都是子空間。它們共同的性質就是「怎麼疊加都還合法」。
- **錯誤更正碼**:Hamming 碼的合法碼字集合是一個子空間(見本週補充觀念)。「兩個合法碼字相加還是合法碼字」正是線性碼(linear code)這個名字的由來。
- **資料的內在維度**:一堆資料點若落在某個子空間裡,表示它們的變化其實比看起來少——這是第 16 週 PCA 的核心。
- **不是子空間的東西也很多**:機率向量(各項非負且和為 1)、單位向量集合都不是子空間。搞清楚差別,才知道什麼時候能用線性代數的工具。

## 原理
**為什麼 Span 一定是子空間?**(課本 p. 180 Example 3)

設 $H = \operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$,逐條驗:

1. **含 $\mathbf{0}$**:取全部權重都是 0,$0\mathbf{v}_1 + \cdots + 0\mathbf{v}_p = \mathbf{0} \in H$。✓
2. **對加法封閉**:設 $\mathbf{u} = a_1\mathbf{v}_1 + \cdots + a_p\mathbf{v}_p$、$\mathbf{w} = b_1\mathbf{v}_1 + \cdots + b_p\mathbf{v}_p$,則
   $$\mathbf{u} + \mathbf{w} = (a_1 + b_1)\mathbf{v}_1 + \cdots + (a_p + b_p)\mathbf{v}_p$$
   還是同一組 $\mathbf{v}_j$ 的線性組合,所以在 $H$ 裡。✓
3. **對純量乘法封閉**:$c\mathbf{u} = (ca_1)\mathbf{v}_1 + \cdots + (ca_p)\mathbf{v}_p \in H$。✓

$\blacksquare$

這個證明很短,但它是本節最重要的工具:**以後要證明某個集合是子空間,最快的路就是把它寫成 Span。**

**為什麼「含 $\mathbf{0}$」不能省?** 邏輯上,若 $H$ **非空**且對純量乘法封閉,取 $c = 0$ 即得 $\mathbf{0} \in H$。課本仍然把它列為條件 (a),一來是為了排除空集合,二來是因為它是實務上最快的檢查——不含原點就直接出局。

## 老師講解
### 例 1 · Lay 2.8 Example 1 與 Exercises 1–2
Is the set $H$ of all vectors of the form $(a, b, 0)$ a subspace of $\mathbb{R}^3$? Then explain why the first quadrant of $\mathbb{R}^2$ is *not* a subspace, and why the union of the first and third quadrants is *not* either.

1. **第一個集合**:$H$ 裡的向量長成 $(a, b, 0)$,也就是 $xy$ 平面。
2. **最快的證法:寫成 Span。**
   $$\begin{bmatrix} a \\ b \\ 0 \end{bmatrix} = a\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} + b\begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}$$
   所以 $H = \operatorname{Span}\{\mathbf{e}_1, \mathbf{e}_2\}$,由上面的原理,**是**子空間。
3. **第一象限為什麼不是?** 先檢查它含不含原點——含。加法呢?兩個第一象限的向量相加還在第一象限,也沒問題。
4. **所以要找純量的反例**:取 $\mathbf{u} = (1, 1) \in H$,$(-1)\mathbf{u} = (-1, -1)$ 落在第三象限,$\notin H$。**條件 (c) 破了**,不是子空間。
5. **第一 + 第三象限呢?** 這次純量乘法沒問題:乘正數留在同一象限,乘負數跑到對面那個象限——**也還在 $H$ 裡**。
6. **所以要找加法的反例**:取 $\mathbf{u} = (1, 3)$(第一象限)、$\mathbf{v} = (-3, -1)$(第三象限),兩個都在 $H$ 裡,但
   $$\mathbf{u} + \mathbf{v} = (-2, 2)$$
   落在第二象限,$\notin H$。**條件 (b) 破了**。
7. **這兩題的教訓**:不是子空間的原因**不只一種**,要看清楚是哪一條壞掉。答題時必須寫出**具體的反例向量**,不能只說「不封閉」。

### 例 2 · Lay 2.8 Exercise 3
The set $H$ is a band of fixed width along the line $x_2 = x_1$ (including the two bounding lines). Give a specific reason why $H$ is *not* a subspace of $\mathbb{R}^2$.

1. **先看含不含原點**:原點在中線上,當然在帶子裡。第一條沒問題。
2. **這個集合的特徵是「有寬度上限」**。把離中線最遠的點再放大,就會撐出去。
3. **具體反例**:設帶子的條件是 $|x_2 - x_1| \le d$。取邊界上的 $\mathbf{u}$,也就是 $x_2 - x_1 = d$ 的點。那麼 $2\mathbf{u}$ 滿足
   $$x_2 - x_1 = 2d > d$$
   所以 $2\mathbf{u} \notin H$,**條件 (c) 破了**。
4. **加法也一樣壞**:$\mathbf{u} + \mathbf{u} = 2\mathbf{u} \notin H$,所以 (b) 也不成立。這題是**兩條都壞**的例子。
5. **最重要的陷阱**(書後解答特別提醒):帶子的**中線** $x_2 = x_1$ 本身是一個子空間。如果你挑中線上的點當反例,不管怎麼加、怎麼乘都還在帶子裡,**永遠舉不出反例**。
6. **所以答題時要強調**:反例必須用**不在中線上**的點。這一點是本題真正在考的東西。

### 例 3 · Lay 2.8 Exercises 35–37
Construct a nonzero $3 \times 3$ matrix $A$ and a nonzero vector $\mathbf{b}$ such that $\mathbf{b}$ is in $\operatorname{Col} A$ but $\mathbf{b}$ is not the same as any one of the columns of $A$. Then construct $A$ and $\mathbf{b}$ with $\mathbf{b}$ *not* in $\operatorname{Col} A$. Finally construct a nonzero $A$ and nonzero $\mathbf{b}$ with $\mathbf{b}$ in $\operatorname{Nul} A$.

1. **構造題的通則:挑最簡單的矩陣。** 不要隨便寫一個亂數矩陣再去算,而是**先想好要什麼性質,再挑一個明顯有那個性質的例子**。
2. **第一題**($\mathbf{b} \in \operatorname{Col} A$ 但不等於任何一行):取
   $$A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}, \qquad \mathbf{b} = \mathbf{a}_1 + \mathbf{a}_2 = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}$$
   $\mathbf{b}$ 是各行的線性組合(所以在 $\operatorname{Col} A$ 裡),但它不等於 $(1,0,0)$、$(0,1,0)$、$(0,0,0)$ 任何一個。
3. **關鍵在「係數不要只挑一個 1」**:只要用兩個以上的行去組合,答案就不會剛好等於某一行。
4. **第二題**($\mathbf{b} \notin \operatorname{Col} A$):同一個 $A$,它的行只張出 $xy$ 平面,所以取
   $$\mathbf{b} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$$
   就跑到平面外面去了。**做法是先讓 $A$ 的行張不滿 $\mathbb{R}^3$,再挑一個外面的點。**
5. **第三題**($\mathbf{b} \in \operatorname{Nul} A$):這次要讓 $A$ 的行**線性相依**,而相依關係的係數就是零空間的向量。取
   $$A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 1 & 0 \\ 1 & 1 & 0 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 1 \\ -1 \\ 0 \end{bmatrix}$$
   因為第 1 行減第 2 行等於零向量,所以 $A\mathbf{b} = \mathbf{0}$。
6. **三題的共同心法**:$\operatorname{Col} A$ 的題目去想「行張出什麼」,$\operatorname{Nul} A$ 的題目去想「行之間有什麼相依關係」。
7. 答案都**不唯一**,只要合乎條件都算對。

#### 備註
例 3 用到下一個觀念的 $\operatorname{Col} A$ 與 $\operatorname{Nul} A$,建議講完觀念 2 再回頭做,或只講第一、二題(它們其實就是「Span 裡面 / 外面」)。

## 易錯點
- **忘記檢查含不含 $\mathbf{0}$**。不過原點的直線、不含原點的任何區域,一律出局。
- **只驗一條就說是子空間**。要「是」必須三條都成立(或直接寫成 Span);要「不是」只需一個反例。
- **反例寫得不具體**。「對加法不封閉」不算答案,要寫出 $\mathbf{u} = ?$、$\mathbf{v} = ?$、$\mathbf{u} + \mathbf{v} = ?$。
- **Exercise 3 用中線上的點當反例**——那樣永遠舉不出反例。
- **以為「有邊界」就不是子空間**。過原點的直線也有「邊界」(它自己),照樣是子空間;問題在封閉性,不在形狀。
- 把「子空間」與「子集合」混為一談。任何子空間都是子集合,反過來不成立。

## 教學提示
這個觀念是全週的地基,但**定義本身 5 分鐘就講完**,時間要花在**判斷**上。

這個觀念 25 分鐘。建議節奏:定義 5 分鐘 → 「Span 一定是子空間」5 分鐘(含證明)→ 那張四格圖 10 分鐘(每一格問學生「壞在哪一條?」)→ 練習 5 分鐘。

**四格圖是本節的主角**,一定要一格一格問、讓學生自己講出反例。特別是第 (3) 格的中線陷阱,值得多花兩分鐘——它訓練的是「舉反例要挑對位置」這個能力。

課堂建議做:Exercises 1、3(四格圖裡的兩格);是非 Exercises 21、22(定義的量詞);Exercise 35。Exercises 2、4 當作業。

## 練習
### 照做 · Lay 2.8 Exercises 1–4
Exercises 1–4 display sets in $\mathbb{R}^2$. Assume the sets include the bounding lines. In each case, give a specific reason why the set $H$ is *not* a subspace of $\mathbb{R}^2$. (For instance, find two vectors in $H$ whose sum is *not* in $H$, or find a vector in $H$ with a scalar multiple that is not in $H$. Draw a picture.)

![Lay 2.8 Exercises 1–4 的四個區域(含邊界線)。](subspace-tests.svg)

(1) The first quadrant.

(2) The union of the first and the third quadrants.

(3) The band along the line $x_2 = x_1$.

(4) The half-plane above a line through the origin with negative slope.

#### 解答
- (1) 對加法封閉,但對**負純量**不封閉。取 $\mathbf{u} = \begin{bmatrix} 1 \\ 1 \end{bmatrix} \in H$,則 $(-1)\mathbf{u} = \begin{bmatrix} -1 \\ -1 \end{bmatrix} \notin H$。
- (2) 對純量乘法封閉,但對**加法**不封閉。取 $\mathbf{u} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}$、$\mathbf{v} = \begin{bmatrix} -3 \\ -1 \end{bmatrix}$,兩者都在 $H$ 裡,但 $\mathbf{u} + \mathbf{v} = \begin{bmatrix} -2 \\ 2 \end{bmatrix}$ 落在第二象限,$\notin H$。
- (3) **兩條都壞**。取邊界上的 $\mathbf{u}$(即 $x_2 - x_1 = d$),則 $2\mathbf{u}$ 的 $x_2 - x_1 = 2d > d$,$\notin H$;同樣 $\mathbf{u} + \mathbf{u} \notin H$。
- (4) 對加法與非負純量封閉,但對**負純量**不封閉。取 $\mathbf{u} = \begin{bmatrix} 0 \\ 1 \end{bmatrix} \in H$,則 $(-1)\mathbf{u} = \begin{bmatrix} 0 \\ -1 \end{bmatrix}$ 落在線的下方,$\notin H$。

#### 備註
(3) 的書後解答特別提醒:**帶子的中線 $x_2 = x_1$ 本身是子空間,所以任何反例至少要用一個不在這條線上的點**。這是本題真正的考點,批改時要看學生挑的點在哪裡。

四題都要求「畫圖」,建議要求學生在圖上**把反例的兩個(或三個)點標出來**。

### 是非 · Lay 2.8 Exercises 21–24
In Exercises 21–30, mark each statement True or False (T/F). Justify each answer.

(21) **(T/F)** A subspace of $\mathbb{R}^n$ is any set $H$ such that (i) the zero vector is in $H$, (ii) $\mathbf{u}$, $\mathbf{v}$, and $\mathbf{u} + \mathbf{v}$ are in $H$, and (iii) $c$ is a scalar and $c\mathbf{u}$ is in $H$.

(22) **(T/F)** A subset $H$ of $\mathbb{R}^n$ is a subspace if the zero vector is in $H$.

(23) **(T/F)** If $\mathbf{v}_1, \dots, \mathbf{v}_p$ are in $\mathbb{R}^n$, then $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ is the same as the column space of the matrix $[\,\mathbf{v}_1 \;\cdots\; \mathbf{v}_p\,]$.

(24) **(T/F)** Given vectors $\mathbf{v}_1, \dots, \mathbf{v}_p$ in $\mathbb{R}^n$, the set of all linear combinations of these vectors is a subspace of $\mathbb{R}^n$.

#### 解答
- (21) **False.** 敘述漏掉了「for each」這個量詞。定義要求對 $H$ 中**每一對** $\mathbf{u}, \mathbf{v}$ 都有 $\mathbf{u} + \mathbf{v} \in H$、對**每個** $\mathbf{u}$ 與**每個**純量 $c$ 都有 $c\mathbf{u} \in H$;題目只說「某些 $\mathbf{u}, \mathbf{v}, c$」,條件太弱。
- (22) **False.** 含 $\mathbf{0}$ 只是三條之一。反例:$H = \{(0,0), (1,0)\}$ 含 $\mathbf{0}$,但 $2(1,0) = (2,0) \notin H$。
- (23) **True.** $\operatorname{Col} A$ 依定義就是各行所有線性組合的集合;當 $A = [\,\mathbf{v}_1 \cdots \mathbf{v}_p\,]$ 時,它恰好等於 $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_p\}$。
- (24) **True.** 這就是上面「原理」證過的:Span 永遠是子空間。

#### 備註
書後對 Exercises 21–29 統一寫「Read the section carefully, and write your answers before checking the *Study Guide*.」,**沒有給 T/F 答案**;上面的答案是本講義判定的。

(21) 考的是**量詞**,學生很容易讀過去沒注意到少了「每一個」。建議課堂上把課本的定義與題目的敘述並排寫在黑板上比對。

另外課本 p. 185 這段前言把 True 印成「**Ture**」,是 Global Edition 的印刷錯誤。

### 變化 · Lay 2.8 Exercises 35–37
(35) Construct a nonzero $3 \times 3$ matrix $A$ and a nonzero vector $\mathbf{b}$ such that $\mathbf{b}$ is in $\operatorname{Col} A$, but $\mathbf{b}$ is not the same as any one of the columns of $A$.

(36) Construct a nonzero $3 \times 3$ matrix $A$ and a vector $\mathbf{b}$ such that $\mathbf{b}$ is *not* in $\operatorname{Col} A$.

(37) Construct a nonzero $3 \times 3$ matrix $A$ and a nonzero vector $\mathbf{b}$ such that $\mathbf{b}$ is in $\operatorname{Nul} A$.

#### 解答
(35) 取 $A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$、$\mathbf{b} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}$。$\mathbf{b} = \mathbf{a}_1 + \mathbf{a}_2$ 是線性組合,所以在 $\operatorname{Col} A$ 裡;但它不等於 $A$ 的任何一行。

(36) 同一個 $A$,取 $\mathbf{b} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$。$\operatorname{Col} A$ 只是 $xy$ 平面,$\mathbf{b}$ 不在裡面。

(37) 取 $A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 1 & 0 \\ 1 & 1 & 0 \end{bmatrix}$、$\mathbf{b} = \begin{bmatrix} 1 \\ -1 \\ 0 \end{bmatrix}$。第 1 行與第 2 行相同,所以 $A\mathbf{b} = \mathbf{a}_1 - \mathbf{a}_2 = \mathbf{0}$。

#### 備註
答案都**不唯一**。書後對 (35) 只說「construct $\mathbf{b}$ to be almost any convenient linear combination of the columns of $A$」,對 (37) 只給提示「You need a nonzero matrix whose columns are linearly dependent.」

三題的心法:$\operatorname{Col} A$ 的題目想「行張出什麼」,$\operatorname{Nul} A$ 的題目想「行之間有什麼相依關係」。建議課堂做 (35),另外兩題當作業。

## 驗算
```check
(lambda h: Matrix([1, 1]) in h and -Matrix([1, 1]) not in h)([Matrix([a, b]) for a in range(0, 3) for b in range(0, 3)])
Matrix([1, 3]) + Matrix([-3, -1]) == Matrix([-2, 2])
(lambda u: 2 * u == Matrix([0, 2]) and abs((2*u)[1] - (2*u)[0]) > abs(u[1] - u[0]))(Matrix([0, 1]))
Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]]) * Matrix([1, 1, 0]) == Matrix([1, 1, 0])
(lambda m, b: m.rank() == m.row_join(b).rank() and m.col(0) != b and m.col(1) != b and m.col(2) != b)(Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]]), Matrix([1, 1, 0]))
(lambda m, b: m.rank() < m.row_join(b).rank())(Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]]), Matrix([0, 0, 1]))
(lambda m, b: not m.is_zero_matrix and not b.is_zero_matrix and (m * b).is_zero_matrix)(Matrix([[1, 1, 0], [1, 1, 0], [1, 1, 0]]), Matrix([1, -1, 0]))
(lambda v1, v2: (0 * v1 + 0 * v2).is_zero_matrix)(Matrix([1, 0, 0]), Matrix([0, 1, 0]))
Matrix([[1, 0], [0, 1], [0, 0]]) * Matrix([a, b]) == Matrix([a, b, 0])
```
