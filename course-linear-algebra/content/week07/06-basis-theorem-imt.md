---
title_en: The Basis Theorem and the IMT
title_zh: 基底定理:數量對了,只驗一半
sub: Five more clauses for the Invertible Matrix Theorem
level: mid
source: Lay 2.9
lab_hook: 'Lab 用 rank 判斷可逆,而不是算行列式'
---
## 觀念
**Theorem 15 (The Basis Theorem).** Let $H$ be a $p$-dimensional subspace of $\mathbb{R}^n$. Any linearly independent set of exactly $p$ elements in $H$ is automatically a basis for $H$. Also, any set of $p$ elements of $H$ that spans $H$ is automatically a basis for $H$.

**The Invertible Matrix Theorem (continued).** Let $A$ be an $n \times n$ matrix. Then the following statements are each equivalent to the statement that $A$ is an invertible matrix.

> (m) The columns of $A$ form a basis of $\mathbb{R}^n$.
>
> (n) $\operatorname{Col} A = \mathbb{R}^n$
>
> (o) $\operatorname{rank} A = n$
>
> (p) $\dim \operatorname{Nul} A = 0$
>
> (q) $\operatorname{Nul} A = \{\mathbf{0}\}$

課本說明這五條「are presented below to follow the statements in the original theorem in Section 2.3」——也就是**直接接在上週那 12 條 (a)–(l) 後面**,清單現在有 17 條。

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| the Basis Theorem | 基底定理 | 個數剛好 $p$ 時,獨立與張成只要驗一個 |
| exactly $p$ elements | 恰好 $p$ 個元素 | 「恰好」是關鍵,多一個或少一個都不能用 |
| automatically | 自動 | 不必再驗另一個條件 |
| (continued) | (續) | 接在 2.3 節 IMT 的 (a)–(l) 之後 |
| chain of implications | 推論鏈 | $(\text{g}) \Rightarrow (\text{n}) \Rightarrow (\text{o}) \Rightarrow (\text{p}) \Rightarrow (\text{q}) \Rightarrow (\text{d})$ |
| equivalent | 等價 | 要嘛全對、要嘛全錯,沒有中間狀態 |

## 白話說
**基底定理 = 數量對了就只驗一半。**

基底的定義要兩個條件:**線性獨立 + 張成**。但如果你手上的向量**個數剛好等於維度**,那兩個條件會**互相蘊含**——驗一個就好。

| 已知 $\dim H = p$,手上有 | 只要再驗 | 結論 |
|---|---|---|
| **恰好 $p$ 個**、線性獨立 | 不必驗張成 | 是基底 |
| **恰好 $p$ 個**、張成 $H$ | 不必驗獨立 | 是基底 |
| 少於 $p$ 個 | — | 一定張不滿 |
| 多於 $p$ 個 | — | 一定相依 |

**「恰好 $p$ 個」這五個字不能省。** 3 維子空間裡的 4 個向量就算張成 $H$,也不是基底(必定相依);2 個獨立向量也不是基底(張不滿)。

**IMT 新增的五條,其實都是同一句話的變裝。**

| 條款 | 說法 | 白話 |
|---|---|---|
| (m) | 各行是 $\mathbb{R}^n$ 的基底 | 剛剛好夠用,不多不少 |
| (n) | $\operatorname{Col} A = \mathbb{R}^n$ | 想要什麼輸出都做得到 |
| (o) | $\operatorname{rank} A = n$ | 沒有一行是多餘的 |
| (p) | $\dim \operatorname{Nul} A = 0$ | 沒有自由度 |
| (q) | $\operatorname{Nul} A = \{\mathbf{0}\}$ | 只有 $\mathbf{0}$ 被壓成 $\mathbf{0}$ |

看出來了嗎?**由 Rank Theorem,$\operatorname{rank} A = n \iff \dim \operatorname{Nul} A = 0$**,所以 (o) 與 (p) 是硬幣的兩面;(n) 與 (o) 只差一個「維度」的定義;(q) 與 (p) 只差「0 維子空間就是 $\{\mathbf{0}\}$」這句話。

**實務上最常用的是 (o)**:算 rank 比算行列式穩定得多(見上一個觀念的數值筆記),所以程式裡判斷可逆幾乎都看 rank 或奇異值,不看 $\det$。

## 在資工哪裡用
- **判斷一組特徵是否「剛好夠」**:若目標空間是 $p$ 維,而你有 $p$ 個線性獨立的特徵,那就不用再檢查「能不能表示所有資料」——基底定理保證可以。
- **用 rank 取代 det**:`np.linalg.det` 在大矩陣上會溢位或失去精度($\det$ 是 $n$ 個數的乘積),`matrix_rank` 用奇異值,穩定得多。**條款 (o) 就是這個做法的理論依據。**
- **可解性判斷**:(n) 說 $\operatorname{Col} A = \mathbb{R}^n$,等價於「對任何右手邊 $\mathbf{b}$,$A\mathbf{x} = \mathbf{b}$ 都有解」;(q) 說解是唯一的。**線性系統求解器的兩個保證,就是這兩條。**
- **編碼理論**:一個 $[n, k]$ 線性碼的生成矩陣有 $k$ 行且 rank $= k$,基底定理保證那 $k$ 行就是碼空間的基底——第 7 個觀念的 Hamming code 會用到。

## 原理
**為什麼基底定理成立?**(定理的敘述在課本 p. 189,課本註明它「proved in Section 4.5」——第 4 章本課程不教,所以以下是本講義寫的證明)

設 $\dim H = p$,先看第一半:$S$ 是 $H$ 中**恰好 $p$ 個**線性獨立的向量。

若 $S$ **不**張成 $H$,那存在某個 $\mathbf{v} \in H$ 不在 $\operatorname{Span} S$ 裡。把 $\mathbf{v}$ 加進 $S$,得到 $p + 1$ 個向量——而且**仍然線性獨立**(新向量不是舊向量的組合,舊向量本來就獨立)。但 $H$ 是 $p$ 維的,$H$ 裡任何超過 $p$ 個向量的集合必定相依(這正是 Exercise 35 要證的事)。矛盾。所以 $S$ 一定張成 $H$,故為基底。

第二半:$S$ 是 $H$ 中**恰好 $p$ 個**張成 $H$ 的向量。

若 $S$ 線性**相依**,那其中某個向量是其他向量的組合,把它刪掉,剩下的 $p - 1$ 個**仍然張成** $H$(第 3 週的生成集刪減定理)。重複這個動作直到獨立,就得到一組不到 $p$ 個向量的基底,於是 $\dim H < p$,矛盾。所以 $S$ 線性獨立,故為基底。$\blacksquare$

**兩半的證法是對稱的**:一半用「不能再加」、一半用「不能再刪」。**維度就是那個「剛好」的數字。**

**IMT 新五條怎麼證?** 課本用一條推論鏈:

$$(\text{g}) \Rightarrow (\text{n}) \Rightarrow (\text{o}) \Rightarrow (\text{p}) \Rightarrow (\text{q}) \Rightarrow (\text{d})$$

1. **(g) $\Rightarrow$ (n)**:(g) 說 $A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b} \in \mathbb{R}^n$ 都有解;而 $\operatorname{Col} A$ 正好就是「所有讓方程相容的 $\mathbf{b}$」的集合。所以 $\operatorname{Col} A = \mathbb{R}^n$。
2. **(n) $\Rightarrow$ (o)**:$\operatorname{Col} A = \mathbb{R}^n$ ⇒ $\dim \operatorname{Col} A = n$ ⇒ $\operatorname{rank} A = n$(維度與 rank 的定義)。
3. **(o) $\Rightarrow$ (p)**:由 Rank Theorem,$\dim \operatorname{Nul} A = n - \operatorname{rank} A = n - n = 0$。
4. **(p) $\Rightarrow$ (q)**:維度 0 的子空間就是 $\{\mathbf{0}\}$。
5. **(q) $\Rightarrow$ (d)**:$\operatorname{Nul} A = \{\mathbf{0}\}$ 就是「$A\mathbf{x} = \mathbf{0}$ 只有平凡解」,那正是 (d)。
6. **(d) 與 (g) 上週已證等價於可逆**,所以整條鏈首尾相接,五條全部等價。$\blacksquare$

至於 **(m)**,課本說它「is logically equivalent to statements (e) and (h)」:(e) 是各行線性獨立、(h) 是各行張成 $\mathbb{R}^n$,兩條合起來就是基底的定義。

**注意這條鏈的走法**:它不是一條一條與「可逆」對證,而是**串成一圈**——這是上週證明時刻用過的技巧,這裡只是把圈接得更長。

## 老師講解
### 例 1 · 補充:用 (m)–(q) 判斷可逆
Decide whether each matrix is invertible, using only statements (m)–(q) of the Invertible Matrix Theorem:

$$P = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}, \qquad Q = \begin{bmatrix} 1 & 5 & 1 \\ 2 & 7 & 2 \\ 3 & 9 & 3 \end{bmatrix}$$

1. **先看 $P$**:它的三行分別是 $\mathbf{e}_3, \mathbf{e}_1, \mathbf{e}_2$——**就是單位矩陣的三行換了順序**。
2. **換順序不影響「是不是基底」**:$\{\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3\}$ 是 $\mathbb{R}^3$ 的標準基底,重排之後還是同一組向量 ⇒ 條款 **(m)** 成立 ⇒ **$P$ 可逆**。
3. **交叉確認其他三條**:$\operatorname{rank} P = 3$ ⇒ (o) ✓;$\dim \operatorname{Nul} P = 3 - 3 = 0$ ⇒ (p) ✓;$\operatorname{Col} P = \mathbb{R}^3$ ⇒ (n) ✓。**四條同時成立**,這就是「等價」的意思。
4. **這種矩陣叫置換矩陣**,它做的事是把座標重新排列——第 6 週 `scipy.linalg.lu` 回傳的那個 $P$ 正是它。
5. **再看 $Q$**:第 3 行和第 1 行**一模一樣**。
6. **兩行相同 ⇒ 線性相依 ⇒ 不是基底** ⇒ (m) 不成立 ⇒ **$Q$ 不可逆**。
7. **其他條款也同時倒**:$\operatorname{rank} Q = 2 \ne 3$ ⇒ (o) 倒;$\dim \operatorname{Nul} Q = 1 \ne 0$ ⇒ (p) 倒;$\mathbf{x} = (1, 0, -1)$ 滿足 $Q\mathbf{x} = \mathbf{0}$ ⇒ (q) 倒;$\operatorname{Col} Q$ 只有 2 維 ⇒ (n) 倒。
8. **注意第 7 步的 $\mathbf{x}$ 怎麼來的**:「第 1 行減第 3 行 $= \mathbf{0}$」這個相依關係,**係數直接就是零空間的向量**,不必解方程。

### 例 2 · 補充:在一個具體的子空間裡用基底定理
Let $H = \operatorname{Span}\left\{\begin{bmatrix} 1 \\ 0 \\ 1 \\ 2 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 1 \\ -1 \end{bmatrix}, \begin{bmatrix} 2 \\ 3 \\ 5 \\ 1 \end{bmatrix}\right\}$ in $\mathbb{R}^4$, and suppose you are told that $\dim H = 2$. Are the first two vectors a basis for $H$? Are all three?

1. **先確認「數量」**:題目直接給了 $\dim H = 2$,所以**恰好 2 個**的集合才有資格套基底定理。
2. **前兩個向量獨立嗎?** $\mathbf{v}_2$ 不是 $\mathbf{v}_1$ 的倍數(看第 2 格:一個是 0、一個是 1)⇒ **獨立** ✓
3. **個數 2 = 維度 2、而且獨立** ⇒ 由基底定理的**第一半**,它們**自動**是 $H$ 的基底。
4. **注意我們沒有驗「張成」**——那正是基底定理省掉的工作。不用定理的話,就得證明 $\mathbf{v}_3$ 也組得出來。
5. **三個向量呢?** 個數 3 > 維度 2 ⇒ **必定線性相依** ⇒ **不是基底**,不必計算。
6. **實際確認一下**:$\mathbf{v}_3 = 2\mathbf{v}_1 + 3\mathbf{v}_2$(逐格驗:$2 + 0 = 2$、$0 + 3 = 3$、$2 + 3 = 5$、$4 - 3 = 1$)✓ 果然多餘。
7. **但它們仍然張成 $H$**——生成集可以有多餘的向量,基底不行。**「張成」與「基底」差的就是這件事。**
8. **一句話收尾**:$p$ 維子空間裡,**少於 $p$ 個張不滿、多於 $p$ 個必相依、恰好 $p$ 個只要驗一個條件**。

#### 備註
觀念裡新增的 (m)–(q) 五條,例 1 一次把四條都用上了;而且那個置換矩陣在第 6 週的 LU 分解出現過,學生看到「原來那個 $P$ 是可逆的」會把兩週接起來。

例 2 的第 5、6 步是關鍵:**先用數量刷掉,再實際找出相依關係**。練習卡的 Exercises 33、34 是同一個定理的抽象版(沒有具體數字),做完這兩例再去寫會順很多。

## 易錯點
- **忘了「恰好 $p$ 個」**。3 維子空間裡 4 個張成的向量不是基底;2 個獨立的也不是。**基底定理只在個數等於維度時可用。**
- **拿基底定理當成「不必檢查任何事」**。仍然要驗其中一個條件(獨立或張成),只是不必驗兩個。
- **在 Exercise 34 裡改用「樞軸行是基底」**。題目明說那 4 行不一定是樞軸行,這條路走不通。
- **以為 $\operatorname{Col} A$ 的基底唯一**。樞軸行只是最容易算的一組。
- **把 (n) 寫成 $\operatorname{Col} A = \mathbb{R}^m$**。IMT 只談方陣,$m = n$,但寫的時候要清楚那是**行向量所在的空間**。
- **把新五條用在非方陣上**。IMT 從第一條到第 17 條,前提都是 $n \times n$。

## 教學提示
這個觀念 20 分鐘,是本週的收束點:**把 2.8、2.9 學到的東西接回上週的 IMT。**

建議這樣開場:把上週 (a)–(l) 的清單投影出來,問「現在我們多學了 Col、Nul、rank、基底,能不能再加幾條?」讓學生自己提,通常會提出 (o) 與 (q),再補齊五條。**學生自己想出來的條款,記得比抄來的牢。**

基底定理最有效的教法是**反面示範**:在黑板上畫 $\mathbb{R}^3$ 裡的一個平面($p = 2$),然後問

- 平面上 2 個不平行的向量是基底嗎?(是)
- 平面上 3 個向量、確定張成這個平面,是基底嗎?(**不是**,必相依)
- 平面上 1 個向量,是基底嗎?(不是,張不滿)

**三問下來,「恰好 $p$ 個」就記住了。**

課堂建議做:補充的可逆判斷題、Exercise 33、Exercise 34。是非 Exercises 25–26 口頭快問。Exercises 35–36 是本節最難的兩題(維度定義的理論基礎),建議只在課堂上講 Exercise 35 的 (a)(b)(c) 三步骨架,完整寫作當作業;若時間不足,可只講 (c) 的 $A = BC$ 那一步。

## 練習
### 照做 · 補充
In each part, decide the answer and name the statement of the Invertible Matrix Theorem or the theorem you used.

(1) Let $A = \begin{bmatrix} 1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0 \end{bmatrix}$. Find $\operatorname{rank} A$ and $\dim \operatorname{Nul} A$. Is $A$ invertible?

(2) Let $B = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$. Find $\operatorname{rank} B$ and $\dim \operatorname{Nul} B$. Is $B$ invertible?

(3) Let $H$ be a three-dimensional subspace of $\mathbb{R}^5$ and let $S$ be a set of three linearly independent vectors in $H$. Must $S$ be a basis for $H$?

(4) Let $H$ be a three-dimensional subspace of $\mathbb{R}^5$ and let $S$ be a set of four vectors in $H$ that spans $H$. Must $S$ be a basis for $H$?

#### 解答
- (1) 列化簡有 3 個樞軸,$\operatorname{rank} A = 3$、$\dim \operatorname{Nul} A = 3 - 3 = 0$。⇒ 由條款 **(o)**(或 (p))**$A$ 可逆**。(順帶:$\det A = 1$。)
- (2) $\operatorname{rank} B = 2$、$\dim \operatorname{Nul} B = 1$。⇒ (o) 不成立 ⇒ **$B$ 不可逆**。非零零空間向量例如 $(1, -2, 1)$,由條款 **(q)** 也得到同樣結論。
- (3) **是。** $\dim H = 3$、恰好 3 個獨立向量 ⇒ 由**基底定理**第一半自動是基底,不必再驗張成。
- (4) **不是。** 基底定理要求「**恰好** $p$ 個」,這裡是 4 個。$H$ 只有 3 維,裡面任 4 個向量必線性相依,所以 $S$ 不可能是基底(雖然它確實張成 $H$)。

#### 備註
(1)(2) 練「用 rank 判斷可逆」;(3)(4) 練基底定理的「恰好 $p$ 個」。

**(4) 是本組的陷阱題**:很多學生看到「張成 $H$」就套基底定理。要他們先數個數,再決定能不能套。

若學生在 (1) 直接寫 $\det A = 1 \ne 0$,答案對但沒練到新條款;請要求補上「哪一條」。

### 是非 · Lay 2.9 Exercises 25–26
In Exercises 25 and 26, mark each statement True or False. Justify each answer. Here $A$ is an $m \times n$ matrix.

(25) **(T/F)** If a set of $p$ vectors spans a $p$-dimensional subspace $H$ of $\mathbb{R}^n$, then these vectors form a basis for $H$.

(26) **(T/F)** If $H$ is a $p$-dimensional subspace of $\mathbb{R}^n$, then a linearly independent set of $p$ vectors in $H$ is a basis for $H$.

#### 解答
- (25) **True.** 基底定理的第二半:$p$ 維子空間裡恰好 $p$ 個張成 $H$ 的向量,自動是基底。
- (26) **True.** 基底定理的第一半:$p$ 維子空間裡恰好 $p$ 個線性獨立的向量,自動是基底。

#### 備註
**書後對 Exercises 17–25 沒有給 T/F 答案**(只寫「See the *Study Guide*」),(26) 是偶數題也沒有;上面兩個答案是本講義判定的。

這兩題就是把 Theorem 15 的兩半各抄成一句話。**批改時不接受「因為定理這樣說」**,要學生指出「哪一半、為什麼個數重要」。

延伸問法(值得口頭追問):把 (25) 的 $p$ 個改成 $p + 1$ 個會怎樣?(必相依,不是基底。)

### 變化 · Lay 2.9 Exercises 33–34
In Exercises 33 and 34, justify each answer.

(33) Let $A$ be an $n \times p$ matrix whose column space is $p$-dimensional. Explain why the columns of $A$ must be linearly independent.

(34) Suppose columns 1, 3, 5, and 6 of a matrix $A$ are linearly independent (but are not necessarily pivot columns) and the rank of $A$ is 4. Explain why the four columns mentioned must be a basis for the column space of $A$.

#### 解答
(33) $A$ 的 $p$ 個行依定義張成 $\operatorname{Col} A$,而 $\dim \operatorname{Col} A = p$。個數($p$)與維度($p$)相同 ⇒ 由基底定理第二半,這組行自動是 $\operatorname{Col} A$ 的基底 ⇒ 基底必線性獨立。$\blacksquare$

(34) 這 4 行都屬於 $\operatorname{Col} A$,且線性獨立;而 $\dim \operatorname{Col} A = \operatorname{rank} A = 4$。恰好 4 個獨立向量在 4 維空間裡 ⇒ 由基底定理第一半,它們自動是 $\operatorname{Col} A$ 的基底。$\blacksquare$

#### 備註
(33) 書後有解答且與上面一致;(34) 書後無解答。

兩題剛好各用基底定理的一半:(33) 用「張成 + 個數對」,(34) 用「獨立 + 個數對」。**建議要求學生寫出用了哪一半**。

(34) 的括號「not necessarily pivot columns」是刻意設計的,目的就是讓「樞軸行是基底」那條路走不通,逼學生用定理。順便可以強調:**$\operatorname{Col} A$ 的基底不唯一**。

### 挑戰 · Lay 2.9 Exercises 35–36
(35) Suppose vectors $\mathbf{b}_1, \dots, \mathbf{b}_p$ span a subspace $W$, and let $\{\mathbf{a}_1, \dots, \mathbf{a}_q\}$ be any set in $W$ containing more than $p$ vectors. Fill in the details of the following argument to show that $\{\mathbf{a}_1, \dots, \mathbf{a}_q\}$ must be linearly dependent. First, let $B = [\,\mathbf{b}_1 \;\cdots\; \mathbf{b}_p\,]$ and $A = [\,\mathbf{a}_1 \;\cdots\; \mathbf{a}_q\,]$.

- **a.** Explain why for each vector $\mathbf{a}_j$, there exists a vector $\mathbf{c}_j$ in $\mathbb{R}^p$ such that $\mathbf{a}_j = B\mathbf{c}_j$.
- **b.** Let $C = [\,\mathbf{c}_1 \;\cdots\; \mathbf{c}_q\,]$. Explain why there is a nonzero vector $\mathbf{u}$ such that $C\mathbf{u} = \mathbf{0}$.
- **c.** Use $B$ and $C$ to show that $A\mathbf{u} = \mathbf{0}$. This shows that the columns of $A$ are linearly dependent.

(36) Use Exercise 35 to show that if $\mathcal{A}$ and $\mathcal{B}$ are bases for a subspace $W$ of $\mathbb{R}^n$, then $\mathcal{A}$ cannot contain more vectors than $\mathcal{B}$, and, conversely, $\mathcal{B}$ cannot contain more vectors than $\mathcal{A}$.

#### 解答
(35)

**a.** $\mathbf{b}_1, \dots, \mathbf{b}_p$ 張成 $W$,而每個 $\mathbf{a}_j$ 都在 $W$ 裡,所以 $\mathbf{a}_j$ 是這些 $\mathbf{b}_i$ 的某個線性組合。把那組權重排成一個向量就得到 $\mathbf{c}_j$,滿足 $\mathbf{a}_j = B\mathbf{c}_j$;因為 $B$ 有 $p$ 行,權重有 $p$ 個,所以 $\mathbf{c}_j \in \mathbb{R}^p$。

**b.** $C$ 是 $p \times q$ 矩陣,且 $q > p$:**行數多於列數** ⇒ $C\mathbf{x} = \mathbf{0}$ 的未知數比方程式多 ⇒ 必有自由變數 ⇒ 存在非零 $\mathbf{u}$ 使 $C\mathbf{u} = \mathbf{0}$(第 3 週的定理)。

**c.** 由 a. 逐行比對可知 $A = BC$($BC$ 的第 $j$ 行 $= B\mathbf{c}_j = \mathbf{a}_j = A$ 的第 $j$ 行,這正是上週矩陣乘法的行觀點)。於是

$$A\mathbf{u} = (BC)\mathbf{u} = B(C\mathbf{u}) = B\mathbf{0} = \mathbf{0}$$

而 $\mathbf{u} \ne \mathbf{0}$,所以 $A$ 的行線性相依。$\blacksquare$

(36) 設 $\mathcal{B}$ 有 $p$ 個向量、$\mathcal{A}$ 有 $q$ 個向量。因 $\mathcal{B}$ 是基底,它張成 $W$;而 $\mathcal{A} \subseteq W$。若 $q > p$,由 Exercise 35 得 $\mathcal{A}$ 線性相依,與「$\mathcal{A}$ 是基底」矛盾,故 $q \le p$。把兩者角色對調(改用 $\mathcal{A}$ 張成 $W$),同理得 $p \le q$。因此 $p = q$:**任兩組基底的向量個數相同**。$\blacksquare$

#### 備註
書後對 (35) 只給三個提示(「*Hint:* The columns of $B$ span $W$ …」「*Hint:* What is the size of $C$?」「*Hint:* How are $B$ and $C$ related to $A$?」),完整論證要學生自己寫;(36) 書後無解答。

**這兩題是整章的地基**:課本 p. 188 說「任何兩組基底的向量個數相同」時,引用的就是 Exercises 35 and 36。**沒有這件事,「維度」這個詞根本沒有定義**。上課時值得說明這一點,學生才知道為什麼要做這麼抽象的題目。

(35c) 的關鍵一步是認出 $A = BC$。若學生卡住,提示「$BC$ 的第 $j$ 行是什麼?」——回到上週矩陣乘法的行觀點就通了。

(35b) 用的是「行數 > 列數 ⇒ 有非平凡解」,這是第 3 週的結論,不必重證。

## 驗算
```check
(lambda a: a.rank() == 3 and len(a.nullspace()) == 0 and a.det() == 1)(Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]]))
(lambda a: a.rank() == 2 and len(a.nullspace()) == 1 and a.det() == 0)(Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) * Matrix([1, -2, 1]) == Matrix([0, 0, 0])
(lambda a: a.rank() + len(a.nullspace()) == a.cols)(Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
(lambda b, c: (b * c) == Matrix([[1, 3], [2, 6]]) and (c.rank() < c.cols))(Matrix([[1, 0], [2, 0]]), Matrix([[1, 3], [0, 0]]))
(lambda b, c, u: ((b * c) * u).is_zero_matrix and (c * u).is_zero_matrix and not u.is_zero_matrix)(Matrix([[1, 0], [2, 0]]), Matrix([[1, 3], [0, 0]]), Matrix([3, -1]))
Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]]).rref()[1] == (0, 1, 2)
Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).rref()[1] == (0, 1)
Matrix([[1, 2, 0], [0, 1, 1], [2, 0, -1], [1, 1, 0]]).rank() == 3
(lambda p: p.det() == 1 and p.rank() == 3 and p.nullspace() == [])(Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]]))
(lambda q: q.rank() == 2 and (q * Matrix([1, 0, -1])).is_zero_matrix and q.cols - q.rank() == 1)(Matrix([[1, 5, 1], [2, 7, 2], [3, 9, 3]]))
(lambda a, b, c: 2 * a + 3 * b == c and Matrix.hstack(a, b, c).rank() == 2)(Matrix([1, 0, 1, 2]), Matrix([0, 1, 1, -1]), Matrix([2, 3, 5, 1]))
```
