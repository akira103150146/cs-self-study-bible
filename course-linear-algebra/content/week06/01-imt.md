---
title_en: The Invertible Matrix Theorem
title_zh: 可逆矩陣定理:十二種說法,同一件事
sub: Twelve equivalent statements about a square matrix
level: hard
source: Lay 2.3
lab_hook: '`Matrix.rank()`、`det()`、`rref()`:三種判斷可逆的方式,答案必須一致'
---
## 觀念
This section provides a review of most of the concepts introduced in Chapter 1, in relation to systems of $n$ linear equations in $n$ unknowns and to *square* matrices.

**Theorem 8 — The Invertible Matrix Theorem.** Let $A$ be a square $n \times n$ matrix. Then the following statements are equivalent. That is, for a given $A$, the statements are either all true or all false.

- **a.** $A$ is an invertible matrix.
- **b.** $A$ is row equivalent to the $n \times n$ identity matrix.
- **c.** $A$ has $n$ pivot positions.
- **d.** The equation $A\mathbf{x} = \mathbf{0}$ has only the trivial solution.
- **e.** The columns of $A$ form a linearly independent set.
- **f.** The linear transformation $\mathbf{x} \mapsto A\mathbf{x}$ is one-to-one.
- **g.** The equation $A\mathbf{x} = \mathbf{b}$ has at least one solution for each $\mathbf{b}$ in $\mathbb{R}^n$.
- **h.** The columns of $A$ span $\mathbb{R}^n$.
- **i.** The linear transformation $\mathbf{x} \mapsto A\mathbf{x}$ maps $\mathbb{R}^n$ onto $\mathbb{R}^n$.
- **j.** There is an $n \times n$ matrix $C$ such that $CA = I$.
- **k.** There is an $n \times n$ matrix $D$ such that $AD = I$.
- **l.** $A^T$ is an invertible matrix.

Because of Theorem 5 in Section 2.2, statement (g) in Theorem 8 could also be written as "The equation $A\mathbf{x} = \mathbf{b}$ has a *unique* solution for each $\mathbf{b}$ in $\mathbb{R}^n$."

The Invertible Matrix Theorem divides the set of all $n \times n$ matrices into two disjoint classes: the invertible (nonsingular) matrices, and the noninvertible (singular) matrices. It should be emphasized, however, that the Invertible Matrix Theorem *applies only to square matrices*.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| equivalent statements | 等價敘述 | 同真同假:一個成立,全部成立 |
| pivot position | 樞軸位置 | 階梯形裡每一列的首項所在的位置 |
| row equivalent to $I_n$ | 與 $I_n$ 列等價 | 可以用列運算化成單位矩陣 |
| linearly independent | 線性獨立 | 各行沒有多餘的(第 3 週) |
| one-to-one | 一對一 | 不同的輸入給不同的輸出(第 4 週) |
| onto | 映成 | 每個目標都有人對應到(第 4 週) |
| nonsingular / singular | 非奇異 / 奇異 | 可逆 / 不可逆 |
| disjoint classes | 互斥的兩類 | 方陣只有「可逆」與「不可逆」兩種,沒有中間 |

## 白話說
**這個定理不是新知識,而是一張清單。** 它把第 1 章到現在學過的東西——樞軸、線性獨立、張成、一對一、映成、反矩陣——全部串成一句話:

> 對**方陣**而言,這十二件事要嘛全對,要嘛全錯。

![課本 2.3 Figure 1:證明走的那個圈,以及掛在圈上的其他敘述。](imt-ring.svg)

**怎麼用?** 兩個方向:

1. **想證明可逆**:挑一個最好驗證的條件去檢查。$3 \times 3$ 以上通常是數樞軸((c)),$2 \times 2$ 就看行列式或兩行是否成比例。
2. **已知不可逆**:那麼**每一條都不成立**。例如知道 $A\mathbf{x} = \mathbf{b}$ 對某個 $\mathbf{b}$ 無解,就可以立刻斷定「各行線性相依」「$A\mathbf{x} = \mathbf{0}$ 有非零解」「不是一對一」。

**最重要的警告:只對方陣成立。** $4 \times 3$ 矩陣的行線性獨立時,**不能**用這個定理推出任何關於 $A\mathbf{x} = \mathbf{b}$ 有沒有解的結論。非方陣的世界裡,「獨立」和「張成」是兩件不同的事(第 3、4 週學過)。

**為什麼十二條可以這樣串?** 因為它們兩兩之間都有第 1 章與前兩週的定理連起來:

| 兩條 | 靠什麼接起來 |
|---|---|
| (d) ⟺ (e) ⟺ (f) | 第 3、4 週:齊次解、線性獨立、一對一本來就是同一件事(任何矩陣都成立) |
| (g) ⟺ (h) ⟺ (i) | 第 2、4 週:有解、張成、映成本來就是同一件事(任何矩陣都成立) |
| (a) ⟺ (l) | 第 5 週 Theorem 6(c):$(A^T)^{-1} = (A^{-1})^T$ |
| 其餘 | 本週的證明時刻 |

## 幾何意義
用第 4 週的眼光看:$A$ 可逆 ⟺ $\mathbf{x} \mapsto A\mathbf{x}$ 這台機器**既不壓扁、也不漏掉**。

- **不壓扁**(一對一、獨立、只有零解):兩個不同的輸入不會變成同一個輸出。
- **不漏掉**(映成、張成、恆有解):輸出可以覆蓋整個 $\mathbb{R}^n$。

對**方陣**而言,這兩件事會同時發生或同時不發生——這就是可逆矩陣定理最令人驚訝的地方。直覺上:輸入與輸出的維度一樣,若壓扁了一個方向,輸出就少了一個方向,自然覆蓋不滿。

非方陣就不是這樣了:$\mathbb{R}^2 \to \mathbb{R}^3$ 可以一對一但絕不可能映成;$\mathbb{R}^3 \to \mathbb{R}^2$ 可以映成但絕不可能一對一。

## 在資工哪裡用
- **一次檢查取代很多次**:寫程式檢查一個系統能不能解,不必試遍所有 $\mathbf{b}$,只要檢查方陣的秩。`np.linalg.matrix_rank(A) == n` 一行搞定。
- **設計系統時的自我檢查**:做電腦圖學的變換矩陣、做編碼的生成矩陣、做濾波器的係數矩陣時,「這個矩陣可逆嗎」等於在問「這個操作能不能還原」。
- **等價條件是演算法選擇的依據**:同樣一件事有十二種檢查方式,成本差很多。數樞軸是 $O(n^3)$、算行列式用餘因子展開是 $O(n!)$——第 8 週會看到這個對比。
- **資料的多餘欄位**:資料表的欄位線性相依((e) 不成立)⟺ 對應的方陣不可逆 ⟺ 模型的參數無法唯一決定。這正是第 3 週 Lab 做過的事,現在有了統一的說法。

## 原理
**課本怎麼證這十二條?**(p. 145)不是兩兩互證(那要 $12 \times 11$ 次),而是**排成一個圈**:

$$\text{(a)} \Rightarrow \text{(j)} \Rightarrow \text{(d)} \Rightarrow \text{(c)} \Rightarrow \text{(b)} \Rightarrow \text{(a)}$$

繞完一圈,這五條就互相等價了。接著再把其他敘述「掛」上去:

- $\text{(a)} \Rightarrow \text{(k)} \Rightarrow \text{(g)} \Rightarrow \text{(a)}$,把 (k)、(g) 接進圈裡。
- (g)、(h)、(i) 對**任何**矩陣都等價(第 2 週 Theorem 4、第 4 週 Theorem 12(a)),所以 (h)、(i) 透過 (g) 連上。
- (d)、(e)、(f) 對**任何**矩陣都等價(第 3 週、第 4 週 Theorem 12(b)),所以透過 (d) 連上。
- 最後 (a) ⟺ (l) 由第 5 週 Theorem 6(c)。

每一步用到的都是前面學過的定理,詳細的鏈條見本週的[證明時刻](W6-例題-教師版.html)。

**一個重要推論**(課本 p. 146 的方框):

> Let $A$ and $B$ be square matrices. If $AB = I$, then $A$ and $B$ are both invertible, with $B = A^{-1}$ and $A = B^{-1}$.

也就是說,**對方陣而言,只要驗一個方向就夠了**。這解釋了第 5 週例 1 的疑問:定義雖然要求 $CA = I$ 且 $AC = I$,但方陣只要驗一邊。(非方陣就不行——第 5 週 Exercises 47–48 給過反例。)

## 老師講解
### 例 1 · Lay 2.3 Example 1
Use the Invertible Matrix Theorem to decide if $A$ is invertible:

$$A = \begin{bmatrix} 1 & 0 & -2 \\ 3 & 1 & -2 \\ -5 & -1 & 9 \end{bmatrix}$$

1. **先問:哪一條最好驗?** 這是 $3 \times 3$,算行列式要展開三項;數樞軸只要列化簡兩步。選 (c)。
2. **列化簡**(第 2 列減 3 倍第 1 列、第 3 列加 5 倍第 1 列):
   $$A \sim \begin{bmatrix} 1 & 0 & -2 \\ 0 & 1 & 4 \\ 0 & -1 & -1 \end{bmatrix}$$
3. **再消一次**(第 3 列加第 2 列):
   $$\sim \begin{bmatrix} 1 & 0 & -2 \\ 0 & 1 & 4 \\ 0 & 0 & 3 \end{bmatrix}$$
4. **數樞軸**:1、1、3,共三個,等於 $n = 3$。由 (c) ⇒ (a),**$A$ 可逆**。
5. **注意我們沒做的事**:沒有求 $A^{-1}$、沒有算行列式、沒有化到最簡列梯形。**題目只問可不可逆,就做到能判斷為止**。
6. **順便讀出更多資訊**:既然 (a) 成立,十二條全成立——各行線性獨立、$A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b}$ 恰有一解、$\mathbf{x} \mapsto A\mathbf{x}$ 一對一且映成。一次列化簡換到這麼多結論。

### 例 2 · Lay 2.3 Exercises 3–4
Determine which of the following matrices are invertible. Use as few calculations as possible. Justify your answers.

$$\begin{bmatrix} 5 & 0 & 0 \\ -3 & -7 & 0 \\ 8 & 5 & -1 \end{bmatrix} \qquad\text{and}\qquad \begin{bmatrix} -7 & 0 & 4 \\ 3 & 0 & -1 \\ 2 & 0 & 9 \end{bmatrix}$$

1. **第一個矩陣是下三角**(主對角線上方全是 0)。這種矩陣不必動手消,對角線上的 $5$、$-7$、$-1$ 就是三個樞軸的位置。
2. **三個樞軸 = $n$**,由 (c) ⇒ **可逆**。(順帶一提 $\det = 5(-7)(-1) = 35$,但不必算。)
3. **第二個矩陣的第二行整行是 0**。一整行是零向量時,取 $\mathbf{x} = \mathbf{e}_2$ 就有 $A\mathbf{x} = \mathbf{0}$——這是非零解。
4. **(d) 不成立** ⇒ 十二條全部不成立 ⇒ **不可逆**。不必列化簡,一眼就看得出來。
5. **這題在訓練什麼?** 題目說「Use as few calculations as possible」。可逆矩陣定理的價值就在這裡:**挑最省力的那一條去驗**。
6. **常見的一眼判準**:某一行(或某一列)全是 0、兩行相同或成比例、某行是其他行的和——這些都直接違反 (e),不必計算。

### 例 3 · Lay 2.3 Practice Problem 1 與 Exercise 23
Determine if $A = \begin{bmatrix} 2 & 3 & 4 \\ 2 & 3 & 4 \\ 2 & 3 & 4 \end{bmatrix}$ is invertible. Then answer: can a square matrix with two identical columns be invertible? Why or why not?

1. **先看 $A$ 的行**:第 2 行是第 1 行的 $\tfrac32$ 倍,第 3 行是第 1 行的 2 倍。
2. **所以各行線性相依**,(e) 不成立 ⇒ **不可逆**。
3. **也可以看列**:三列完全一樣,列化簡後一定出現兩列全零,樞軸只有 1 個,(c) 不成立。兩條路殊途同歸。
4. **一般的問題:兩行相同的方陣可逆嗎?** 設第 $i$ 行與第 $j$ 行相同($i \ne j$)。
5. **造一個非零解**:取 $\mathbf{x} = \mathbf{e}_i - \mathbf{e}_j$,則
   $$A\mathbf{x} = \mathbf{a}_i - \mathbf{a}_j = \mathbf{0}$$
   而 $\mathbf{x} \ne \mathbf{0}$。(d) 不成立 ⇒ **不可逆**。
6. **答題的寫法**:「兩行相同 ⇒ 各行線性相依 ⇒ 由 IMT 的 (e),$A$ 不可逆。」一句話,清楚指出用了哪一條。
7. **這就是本週寫證明的標準格式**:先說觀察到哪一條(不)成立,再說由 IMT 推到哪一條。

#### 備註
例 3 的第 6 步要板書出來當範本。本週的寫作題幾乎全部是這個格式,學生只要學會「引用條款編號」就能寫出合格的答案。

## 易錯點
- **用在非方陣上**。這是本節第一名的錯誤。$4 \times 3$ 矩陣的行獨立,推不出任何關於 $A\mathbf{x} = \mathbf{b}$ 的事。
- **把「有平凡解」當成 (d)**。(d) 是「**只有**平凡解」。任何齊次方程都有平凡解,那句話沒有資訊(Exercise 32 就在考這個)。
- **把 into 當成 onto**。(i) 是 **onto**;「maps $\mathbb{R}^n$ into $\mathbb{R}^n$」對任何 $n \times n$ 矩陣都成立(Exercise 18 的陷阱)。
- **以為「$A$ 是方陣」就能推出 (g)**。IMT 的條件是「$A$ 可逆」,不是「$A$ 是方陣」(Exercise 15)。
- **寫答案時不說理由**。本節的題目幾乎都要求 Justify;只寫「可逆」沒有分數,要寫出引用的是哪一條。
- 一看到題目就開始求反矩陣。多數題目只問可不可逆,數樞軸就夠了。

## 教學提示
這是本週最重要的 30 分鐘,但**不要把十二條逐條唸過去**——學生會睡著。建議這樣做:

1. 先在黑板上寫「$A$ 可逆」,然後問:「我們學過哪些事情等價於這件事?」讓學生回想第 1–5 週,把他們講出來的寫在旁邊。通常能湊出六七條。
2. 再打開課本補齊,並指出「原來我們早就學過大半」。
3. **把那張圈的圖畫在黑板上**(不要只貼講義),邊畫邊說每條箭頭靠哪個定理。
4. 強調兩件事:**只對方陣**、**挑最省力的條件驗**。

例 2 的「一眼判準」要整理成一個小清單寫在黑板角落:整行為 0、兩行相同、兩行成比例、某行是其他行的和。

課堂建議做:Exercises 1、3、4、5(判斷可逆,練「最少計算」);是非 Exercises 15、18、32(三個典型陷阱);Exercise 23、Practice Problem 1。Exercises 21–22(三角矩陣)很適合當作業,它們的結論後面一直會用到。

T 題 Exercises 9、10 放進實作課,和條件數一起做。

## 練習
### 照做 · Lay 2.3 Exercises 1–6
Unless otherwise specified, assume that all matrices in these exercises are $n \times n$. Determine which of the matrices in Exercises 1–10 are invertible. Use as few calculations as possible. Justify your answers.

(1) $\begin{bmatrix} 5 & 7 \\ -3 & -6 \end{bmatrix}$

(2) $\begin{bmatrix} -4 & 6 \\ 6 & -9 \end{bmatrix}$

(3) $\begin{bmatrix} 5 & 0 & 0 \\ -3 & -7 & 0 \\ 8 & 5 & -1 \end{bmatrix}$

(4) $\begin{bmatrix} -7 & 0 & 4 \\ 3 & 0 & -1 \\ 2 & 0 & 9 \end{bmatrix}$

(5) $\begin{bmatrix} 0 & 4 & 7 \\ 1 & 0 & 5 \\ -5 & 8 & -2 \end{bmatrix}$

(6) $\begin{bmatrix} 1 & -5 & -4 \\ 0 & 3 & 4 \\ -3 & 6 & 0 \end{bmatrix}$

#### 解答
- (1) **可逆**。兩行互不成比例 ⇒ 線性獨立 ⇒ IMT (e)。($\det = -30 + 21 = -9 \ne 0$。)
- (2) **不可逆**。第 2 行 $= -\tfrac32 \times$ 第 1 行 ⇒ 行相依 ⇒ (e) 不成立。($\det = 36 - 36 = 0$。)
- (3) **可逆**。下三角、對角線 $5, -7, -1$ 全非零 ⇒ 三個樞軸 ⇒ (c)。
- (4) **不可逆**。第 2 行整行是 0 ⇒ 行相依 ⇒ (e) 不成立(取 $\mathbf{x} = \mathbf{e}_2$ 就是非零解)。
- (5) **可逆**。先換列再消,得 $\begin{bmatrix} 1 & 0 & 5 \\ 0 & 4 & 7 \\ 0 & 0 & 9 \end{bmatrix}$,三個樞軸 ⇒ (c)。
- (6) **不可逆**。列化簡後只有 2 個樞軸,(c) 不成立。($\det = -24 + 60 - 36 = 0$。)

#### 備註
(1)(2)(4) 都是「一眼題」,(3) 靠三角形狀,只有 (5)(6) 真的要動手。批改時要看學生有沒有寫出**引用的條款**。

(5) 書後給的是階梯形 $\begin{bmatrix} 1 & 0 & 5 \\ 0 & 4 & 7 \\ 0 & 0 & 9 \end{bmatrix}$;注意換過一次列,所以原矩陣的行列式是 $-36$ 而不是 $+36$——這不影響可逆性,但值得跟學生說一句。

### 照做 · Lay 2.3 Exercises 7–10
(7) $\begin{bmatrix} -1 & 0 & 2 & 1 \\ -5 & -3 & 9 & 3 \\ 3 & 0 & 1 & -3 \\ 0 & 3 & 1 & 2 \end{bmatrix}$

(8) $\begin{bmatrix} 1 & 3 & 7 & 4 \\ 0 & 5 & 9 & 6 \\ 0 & 0 & 2 & 8 \\ 0 & 0 & 0 & 10 \end{bmatrix}$

(9) **(T)** $\begin{bmatrix} 4 & 0 & -7 & -7 \\ -6 & 1 & 11 & 9 \\ 7 & -5 & 10 & 19 \\ -1 & 2 & 3 & -1 \end{bmatrix}$

(10) **(T)** $\begin{bmatrix} 5 & 3 & 1 & 7 & 9 \\ 6 & 4 & 2 & 8 & -8 \\ 7 & 5 & 3 & 10 & 9 \\ 9 & 6 & 4 & -9 & -5 \\ 8 & 5 & 2 & 11 & 4 \end{bmatrix}$

#### 解答
- (7) **不可逆**。列化簡得
  $$\begin{bmatrix} -1 & 0 & 2 & 1 \\ 0 & -3 & -1 & -2 \\ 0 & 0 & 7 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
  只有 3 個樞軸(少於 4),不與 $I_4$ 列等價 ⇒ (b)(c) 不成立。
- (8) **可逆**。已經是上三角的階梯形,對角線 $1, 5, 2, 10$ 全非零 ⇒ 4 個樞軸 ⇒ (c)。
- (9) **可逆**。用矩陣程式列化簡得 4 個樞軸 ⇒ (c)。($\det = 1$。)
- (10) **可逆**。列化簡得 5 個樞軸 ⇒ (c)。($\det = 2$。)

#### 備註
(9)(10) 標 T,放進實作課用 `Matrix.rank()` 或 `rref()` 算。

這兩題還有後續:實作課會算它們的**條件數**(Exercises 50–51),(9) 的行列式明明是 1,條件數卻高達兩萬多——這正是觀念 4 要講的「可逆」與「好算」是兩回事。

### 是非 · Lay 2.3 Exercises 11–20
In Exercises 11–20, the matrices are all $n \times n$. Each part of the exercises is an *implication* of the form "If 'statement 1', then 'statement 2'." Mark an implication as True if the truth of "statement 2" *always* follows whenever "statement 1" happens to be true. An implication is False if there is an instance in which "statement 2" is false but "statement 1" is true. Justify each answer.

(11) **(T/F)** If the equation $A\mathbf{x} = \mathbf{0}$ has only the trivial solution, then $A$ is row equivalent to the $n \times n$ identity matrix.

(12) **(T/F)** If there is an $n \times n$ matrix $D$ such that $AD = I$, then there is also an $n \times n$ matrix $C$ such that $CA = I$.

(13) **(T/F)** If the columns of $A$ span $\mathbb{R}^n$, then the columns are linearly independent.

(14) **(T/F)** If the columns of $A$ are linearly independent, then the columns of $A$ span $\mathbb{R}^n$.

(15) **(T/F)** If $A$ is an $n \times n$ matrix, then the equation $A\mathbf{x} = \mathbf{b}$ has at least one solution for each $\mathbf{b}$ in $\mathbb{R}^n$.

(16) **(T/F)** If the equation $A\mathbf{x} = \mathbf{b}$ has at least one solution for each $\mathbf{b}$ in $\mathbb{R}^n$, then the solution is unique for each $\mathbf{b}$.

(17) **(T/F)** If the equation $A\mathbf{x} = \mathbf{0}$ has a nontrivial solution, then $A$ has fewer than $n$ pivot positions.

(18) **(T/F)** If the linear transformation $\mathbf{x} \mapsto A\mathbf{x}$ maps $\mathbb{R}^n$ *into* $\mathbb{R}^n$, then $A$ has $n$ pivot positions.

(19) **(T/F)** If $A^T$ is not invertible, then $A$ is not invertible.

(20) **(T/F)** If there is a $\mathbf{b}$ in $\mathbb{R}^n$ such that the equation $A\mathbf{x} = \mathbf{b}$ is inconsistent, then the transformation $\mathbf{x} \mapsto A\mathbf{x}$ is not one-to-one.

#### 解答
- (11) **True.** 前件是 (d)、後件是 (b),IMT 直接給出。
- (12) **True.** 前件是 (k)、後件是 (j);而且可以直接取 $C = D = A^{-1}$。
- (13) **True.** (h) ⇒ (a) ⇒ (e)。
- (14) **True.** (e) ⇒ (a) ⇒ (h)。與 (13) 互為反向,兩題合起來說的是「方陣時獨立與張成等價」。
- (15) **False.** 後件是 (g),但前件只說「$A$ 是方陣」,沒有保證可逆。反例:$A = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$、$\mathbf{b} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ 無解。
- (16) **True.** (g) ⇒ (a),再由第 5 週 Theorem 5 得唯一解 $\mathbf{x} = A^{-1}\mathbf{b}$。
- (17) **True.** 逆否命題就是 (c) ⇒ (d)。直接說也行:有非零解 ⇒ 有自由變數 ⇒ 至少一行不是樞軸行。
- (18) **False.** 「maps $\mathbb{R}^n$ **into** $\mathbb{R}^n$」對任何 $n \times n$ 矩陣都成立,前件沒有資訊。反例:$A = O$,它把 $\mathbb{R}^n$ 映進 $\mathbb{R}^n$,卻有 0 個樞軸。把 into 換成 **onto**(即 (i))才會是 True。
- (19) **True.** (l) 說 $A$ 可逆 ⟺ $A^T$ 可逆;取逆否即得。
- (20) **True.** 某個 $\mathbf{b}$ 不相容 ⇒ (g) 不成立 ⇒ 全部不成立 ⇒ 特別是 (f) 不成立。

#### 備註
書後對 Exercises 11–19 只寫「The *Study Guide* will help, but first try to answer the questions based on your careful reading of the text.」,**沒有給 T/F**;上面的答案是本講義判定的。

(15) 和 (18) 是兩個必考的陷阱:一個把「方陣」誤當「可逆」,一個玩 into / onto 一字之差。建議課堂上先讓學生舉手投票,再公布答案。

### 變化 · Lay 2.3 Exercises 21–22
(21) An $m \times n$ **upper triangular matrix** is one whose entries *below* the main diagonal are 0's (as in Exercise 8). When is a square upper triangular matrix invertible? Justify your answer.

(22) An $m \times n$ **lower triangular matrix** is one whose entries *above* the main diagonal are 0's (as in Exercise 3). When is a square lower triangular matrix invertible? Justify your answer.

#### 解答
兩題的答案一樣:**主對角線上的元素全都非零時可逆,否則不可逆。**

(21) 上三角方陣本身已經是階梯形。若對角元全非零,每個對角元就是一個樞軸,共 $n$ 個 ⇒ IMT (c) ⇒ 可逆。反之若某個對角元是 0,那一行不會有樞軸,樞軸少於 $n$ 個 ⇒ 不可逆。(等價說法:$\det = a_{11}a_{22}\cdots a_{nn} \ne 0$。)

(22) $A$ 是下三角 ⟺ $A^T$ 是上三角,而且兩者對角線相同。由 IMT 的 (l)($A$ 可逆 ⟺ $A^T$ 可逆)與 (21) 的結論立刻得證。

#### 備註
(22) 用轉置是最省力的寫法,正好練習 (l) 這一條。也可以直接列化簡,從左上往右下逐行消去。

這兩題的結論在下一個觀念(LU 分解)一直會用到:$L$ 的對角線全是 1、$U$ 的對角線是樞軸,所以兩者都可逆。

### 變化 · Lay 2.3 Exercises 23–24 與 Practice Problem 1
(23) Can a square matrix with two identical columns be invertible? Why or why not?

(24) Is it possible for a $5 \times 5$ matrix to be invertible when its columns do not span $\mathbb{R}^5$? Why or why not?

(Practice Problem 1) Determine if $A = \begin{bmatrix} 2 & 3 & 4 \\ 2 & 3 & 4 \\ 2 & 3 & 4 \end{bmatrix}$ is invertible.

#### 解答
(23) **不能。** 若 $\mathbf{a}_i = \mathbf{a}_j$($i \ne j$),取 $\mathbf{x} = \mathbf{e}_i - \mathbf{e}_j \ne \mathbf{0}$,則 $A\mathbf{x} = \mathbf{a}_i - \mathbf{a}_j = \mathbf{0}$。(d) 不成立(或直接說各行線性相依,(e) 不成立)⇒ 不可逆。

(24) **不可能。** 「各行不張成 $\mathbb{R}^5$」就是 (h) 不成立;IMT 說十二條同真同假,所以 (a) 也不成立。

(Practice Problem 1) **不可逆。** 第 2、3 行分別是第 1 行的 $\tfrac32$ 倍與 2 倍,各行線性相依 ⇒ (e) 不成立。

#### 備註
Practice Problem 1 的矩陣三列完全相同,也可以從「列」的角度說:列化簡後必出現兩列全零,樞軸只有 1 個。書後解答只講行,課堂上可以補這一句。

這三題是本節寫作題的入門款,務必讓學生寫出「引用哪一條」。

## 驗算
```check
Matrix([[1, 0, -2], [3, 1, -2], [-5, -1, 9]]).rref()[0] == eye(3)
Matrix([[1, 0, -2], [3, 1, -2], [-5, -1, 9]]).rank() == 3
Matrix([[5, 7], [-3, -6]]).det() == -9
Matrix([[-4, 6], [6, -9]]).det() == 0
Matrix([[5, 0, 0], [-3, -7, 0], [8, 5, -1]]).det() == 35
Matrix([[-7, 0, 4], [3, 0, -1], [2, 0, 9]]) * Matrix([0, 1, 0]) == zeros(3, 1)
Matrix([[0, 4, 7], [1, 0, 5], [-5, 8, -2]]).det() == -36
Matrix([[1, -5, -4], [0, 3, 4], [-3, 6, 0]]).det() == 0
Matrix([[-1, 0, 2, 1], [-5, -3, 9, 3], [3, 0, 1, -3], [0, 3, 1, 2]]).rank() == 3
Matrix([[1, 3, 7, 4], [0, 5, 9, 6], [0, 0, 2, 8], [0, 0, 0, 10]]).det() == 100
Matrix([[4, 0, -7, -7], [-6, 1, 11, 9], [7, -5, 10, 19], [-1, 2, 3, -1]]).det() == 1
Matrix([[5, 3, 1, 7, 9], [6, 4, 2, 8, -8], [7, 5, 3, 10, 9], [9, 6, 4, -9, -5], [8, 5, 2, 11, 4]]).det() == 2
Matrix([[1, 1], [1, 1]]).rank() < 2 and Matrix([[1, 1], [1, 1], [1, 0]]).rank() == 2
expand(Matrix([[a, b, c], [0, d, f], [0, 0, g]]).det()) == a*d*g
expand(Matrix([[a, 0, 0], [b, d, 0], [c, f, g]]).det()) == a*d*g
Matrix([[a, a], [b, b]]).det() == 0
Matrix([[1, 1, 5], [2, 2, 6], [3, 3, 7]]) * (Matrix([1, 0, 0]) - Matrix([0, 1, 0])) == zeros(3, 1)
Matrix([[2, 3, 4], [2, 3, 4], [2, 3, 4]]).rank() == 1
Matrix(5, 5, lambda t, s: t + s).rank() < 5
zeros(3, 3).rank() == 0
```
