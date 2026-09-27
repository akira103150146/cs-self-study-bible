---
title_en: Dimension and Rank
title_zh: 維度與 rank:一個矩陣的兩本帳
sub: rank A + dim Nul A = n
level: hard
source: Lay 2.9
lab_hook: '`np.linalg.matrix_rank` 用的是奇異值門檻,不是精確的樞軸計數'
---
## 觀念
**Definition.** The **dimension** of a nonzero subspace $H$, denoted by $\dim H$, is the number of vectors in any basis for $H$. The dimension of the zero subspace $\{\mathbf{0}\}$ is defined to be zero.

> 課本腳註:The zero subspace has *no* basis (because the zero vector by itself forms a linearly dependent set).

**Definition.** The **rank** of a matrix $A$, denoted by $\operatorname{rank} A$, is the dimension of the column space of $A$.

> Since the pivot columns of $A$ form a basis for $\operatorname{Col} A$, the rank of $A$ is just the number of pivot columns in $A$.

**Theorem 14 (The Rank Theorem).** If a matrix $A$ has $n$ columns, then

$$\operatorname{rank} A + \dim \operatorname{Nul} A = n$$

這個定理的證明就是本週的**證明時刻**,那裡會把「為什麼一定加起來剛好是 $n$」講完。

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| dimension | 維度 | 基底裡向量的個數;$\dim H$ |
| rank | 秩 | $\operatorname{rank} A = \dim \operatorname{Col} A = $ 樞軸行的個數 |
| the Rank Theorem | 秩定理 | $\operatorname{rank} A + \dim \operatorname{Nul} A = n$($n$ = **行**數) |
| nullity | 零度 | $\dim \operatorname{Nul} A$,自由變數的個數(2.9 節未用此詞,課本 4.6 節才引入) |
| zero subspace | 零子空間 | $\{\mathbf{0}\}$,維度定義為 0,且**沒有基底** |
| full rank | 滿秩 | $\operatorname{rank} A = \min(m, n)$,能有的最大秩 |

## 白話說
**維度 = 這個子空間裡有幾個「獨立的方向」。**

直線 1 維、平面 2 維、整個 $\mathbb{R}^3$ 是 3 維、只有原點是 0 維。要注意**維度算的是基底的個數,不是向量的分量個數**:$\mathbb{R}^4$ 裡的一個平面,向量有 4 個分量,但維度是 **2**。

**rank = 矩陣「真正提供了幾個獨立的方向」。**

一個 $5 \times 8$ 矩陣有 8 行,但這 8 行可能只張出一個 3 維空間——那 rank 就是 3,剩下的 5 行都是多餘的。

![A 的 n 行分成樞軸行(數 rank)與自由行(數零空間維度)](rank-bar.svg)

**Rank Theorem 就是一句帳:每一行只能當「樞軸行」或「自由行」,兩者相加就是全部的行。**

| 這一行是 | 貢獻給 | 個數 |
|---|---|---|
| 樞軸行 | $\operatorname{Col} A$ 的基底 | $\operatorname{rank} A$ |
| 非樞軸行(自由變數) | $\operatorname{Nul} A$ 的基底 | $\dim \operatorname{Nul} A$ |
| 合計 | — | $n$(行數) |

**這個定理最大的價值是「算一個、送一個」**:知道 rank 就知道零空間維度,反之亦然,不必真的把兩組基底都算出來。

**兩個最容易混的點:**

1. **Rank Theorem 用的是行數 $n$,不是列數 $m$。** $7 \times 6$ 的矩陣要用 6。
2. **$\operatorname{Col} A$ 住在 $\mathbb{R}^m$、$\operatorname{Nul} A$ 住在 $\mathbb{R}^n$**,所以「維度相同」不等於「就是同一個空間」(Exercises 15、16 專考這件事)。

## 幾何意義
維度就是**自由度**:在這個子空間裡移動時,有幾個方向可以獨立地調。

- $\dim \operatorname{Col} A$ = $A\mathbf{x}$ 走得到的「輸出集合」有幾維 ⇒ **這個線性變換的輸出有多豐富**。
- $\dim \operatorname{Nul} A$ = 有幾維的輸入被壓成 $\mathbf{0}$ ⇒ **這個變換損失了多少資訊**。

把兩件事合起來看:一個 $m \times n$ 矩陣把 $\mathbb{R}^n$ 送進 $\mathbb{R}^m$,其中

$$\underbrace{n}_{\text{進來的維度}} = \underbrace{\operatorname{rank} A}_{\text{活下來的維度}} + \underbrace{\dim \operatorname{Nul} A}_{\text{被壓扁的維度}}$$

**這就是為什麼 Rank Theorem 有時被稱為「維度守恆」**:輸入的維度不會消失,只會分成「留下」與「壓扁」兩部分。

例如 $3 \times 3$ 的投影矩陣把空間壓到一個平面上:$\operatorname{rank} = 2$(輸出是平面)、$\dim \operatorname{Nul} = 1$(垂直方向整條線被壓成原點),$2 + 1 = 3$ ✓。

## 在資工哪裡用
- **rank = 資料的「真實維度」**。一張 $1000 \times 1000$ 的表,若 rank 只有 10,表示所有欄位其實由 10 個因子決定——**推薦系統的低秩分解**(Netflix 那類)整個建立在這件事上。
- **rank 不足 = 有冗餘**。感測器裝了 20 個,量測矩陣 rank 只有 6,那有 14 個是白裝的。
- **$\dim \operatorname{Nul} A$ = 系統的自由度**:機械手臂的冗餘關節數、電路的獨立迴路數、線性碼的碼字維度(第 7 個觀念的 Hamming code 就是 $\dim \operatorname{Nul} H = 4$)。
- **判斷 rank 是數值計算的經典陷阱**:浮點下幾乎沒有矩陣是真正降秩的,實務上用**奇異值大小**判斷(見下面的數值筆記),這是第 16 週 SVD 的入口。
- **編譯器與最佳化**:相依分析中,迴圈的平行化程度與相依矩陣的 rank 直接相關。

## 原理
**為什麼「維度」這個定義說得通?**

定義說「$\dim H$ = **任何**一組基底裡向量的個數」——但同一個子空間有無限多組基底,憑什麼每組的**個數**都一樣?這件事必須先成立,維度才有意義。

證明就是 Exercises 35–36(排在下一個觀念):若 $\mathbf{b}_1, \dots, \mathbf{b}_p$ 張成 $W$,則 $W$ 裡任何超過 $p$ 個向量的集合必線性相依。於是兩組基底互相比較,各自都不能比對方多,只能一樣多。

**Rank Theorem 為什麼成立?**(完整證明見本週的證明時刻)

一句話版本:把 $A$ 化成最簡列梯形後,**每一行非此即彼**——

- 是**樞軸行**:它貢獻一個 $\operatorname{Col} A$ 的基底向量(Theorem 13)。
- 不是樞軸行:它對應一個**自由變數**,貢獻一個 $\operatorname{Nul} A$ 的基底向量(參數向量形式)。

沒有第三種可能,也沒有任何一行同時算兩次。所以兩邊的基底個數加起來正好是行數 $n$。$\blacksquare$

**為什麼要強調「行數」?** 因為列運算可以把列變成零列,列數 $m$ 不控制這件事;決定「有幾個變數」的是**行數**。$7 \times 6$ 的矩陣有 6 個變數,所以帳要對 6 記(Exercise 29)。

**IMT 的新條款**:當 $A$ 是 $n \times n$ 時,$\operatorname{rank} A = n \iff \dim \operatorname{Nul} A = 0 \iff A$ 可逆。這是下一個觀念要補進可逆矩陣定理的內容。

## 數值筆記
理論上 rank = 樞軸行的個數,但**浮點運算下這個定義不可用**。

考慮

$$A = \begin{bmatrix} 1 & 2 \\ 2 & 4.000000001 \end{bmatrix}$$

它的 rank 精確來說是 2,但實際上它幾乎是降秩的。反過來,一個數學上 rank 1 的矩陣經過浮點運算後,樞軸位置往往會出現 $10^{-17}$ 這樣的「假樞軸」,程式會誤報 rank 2。

**實務做法**:用奇異值(第 16 週)判斷。`np.linalg.matrix_rank(A)` 的做法是算出所有奇異值 $\sigma_1 \ge \sigma_2 \ge \cdots$,然後數「有幾個 $\sigma_i$ 大於某個門檻」,預設門檻約 $\sigma_1 \times \max(m,n) \times \varepsilon$。

| 工具 | 算的是什麼 | 適合 |
|---|---|---|
| `sympy` 的 `A.rank()` | 精確有理數運算 | 教材、課本習題 |
| `np.linalg.matrix_rank(A)` | 奇異值門檻 | 實際資料 |
| `np.linalg.matrix_rank(A, tol=...)` | 自訂門檻 | 有雜訊的量測資料 |

**Lab 會做一次對照**:同一個矩陣加上 $10^{-12}$ 的擾動,sympy 說 rank 變了、NumPy 說沒變——這不是誰錯了,是兩者回答的問題不同。

## 老師講解
### 例 1 · Lay 2.9 Practice Problem 1
Determine the dimension of the subspace $H$ of $\mathbb{R}^3$ spanned by the vectors $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$. (First, find a basis for $H$.)

$$\mathbf{v}_1 = \begin{bmatrix} 2 \\ -8 \\ 6 \end{bmatrix}, \quad \mathbf{v}_2 = \begin{bmatrix} 3 \\ -7 \\ -1 \end{bmatrix}, \quad \mathbf{v}_3 = \begin{bmatrix} -1 \\ 6 \\ -7 \end{bmatrix}$$

1. **「求 Span 的維度」要先把它變成一個矩陣的行空間**:令 $A = [\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]$,則 $H = \operatorname{Col} A$。
2. **列化簡找樞軸位置**:
   $$\begin{bmatrix} 2 & 3 & -1 \\ -8 & -7 & 6 \\ 6 & -1 & -7 \end{bmatrix} \sim \begin{bmatrix} 2 & 3 & -1 \\ 0 & 5 & 2 \\ 0 & -10 & -4 \end{bmatrix} \sim \begin{bmatrix} 2 & 3 & -1 \\ 0 & 5 & 2 \\ 0 & 0 & 0 \end{bmatrix}$$
3. **只有第 1、2 行是樞軸行**,所以 $\{\mathbf{v}_1, \mathbf{v}_2\}$ 是 $H$ 的基底(記得:取 **$A$ 自己**的行)。
4. **$\dim H = 2$**——基底有 2 個向量。$H$ 是 $\mathbb{R}^3$ 裡的一個**平面**。
5. **$\mathbf{v}_3$ 去哪了?** 它是 $\mathbf{v}_1, \mathbf{v}_2$ 的線性組合,是多餘的。三個向量只張出 2 維。
6. **不要把「3 個向量」當成「3 維」**。這是本節第一號錯誤:**維度看的是獨立的方向數,不是手上有幾個向量**。

### 例 2 · Lay 2.9 Exercise 9
The matrix $A$ and an echelon form of $A$ are shown. Find bases for $\operatorname{Col} A$ and $\operatorname{Nul} A$, and then state the dimensions of these subspaces.

$$A = \begin{bmatrix} 1 & -3 & 2 & -4 \\ -3 & 9 & -1 & 5 \\ 2 & -6 & 4 & -3 \\ -4 & 12 & 2 & 7 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 2 & -4 \\ 0 & 0 & 5 & -7 \\ 0 & 0 & 0 & 5 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

1. **先讀樞軸位置**:第 1 行有樞軸、**第 2 行沒有**(它整列都被消掉了)、第 3 行、第 4 行有。⇒ 樞軸在第 **1、3、4** 行。
2. **$\operatorname{Col} A$ 的基底 = $A$ 的第 1、3、4 行**:
   $$\left\{\begin{bmatrix} 1 \\ -3 \\ 2 \\ -4 \end{bmatrix}, \begin{bmatrix} 2 \\ -1 \\ 4 \\ 2 \end{bmatrix}, \begin{bmatrix} -4 \\ 5 \\ -3 \\ 7 \end{bmatrix}\right\}, \qquad \dim \operatorname{Col} A = 3$$
3. **自由變數只有 $x_2$**(唯一的非樞軸行)。⇒ 預告:$\dim \operatorname{Nul} A = 1$。
4. **回代求零空間**:由第三列 $5x_4 = 0 \Rightarrow x_4 = 0$;第二列 $5x_3 - 7x_4 = 0 \Rightarrow x_3 = 0$;第一列 $x_1 - 3x_2 + 2x_3 - 4x_4 = 0 \Rightarrow x_1 = 3x_2$。
5. **參數向量形式**:$\mathbf{x} = x_2(3, 1, 0, 0)$,所以
   $$\operatorname{Nul} A \text{ 的基底} = \left\{\begin{bmatrix} 3 \\ 1 \\ 0 \\ 0 \end{bmatrix}\right\}, \qquad \dim \operatorname{Nul} A = 1$$
6. **用 Rank Theorem 檢查**:$3 + 1 = 4 = $ 行數 ✓。**這一步一定要做**,它幾乎不花時間卻能抓到大部分錯誤。
7. **注意兩個空間住在不同地方**:$\operatorname{Col} A \subseteq \mathbb{R}^4$、$\operatorname{Nul} A \subseteq \mathbb{R}^4$——這題剛好都是 $\mathbb{R}^4$(因為 $A$ 是方陣),但它們是**不同的** 3 維與 1 維子空間。

### 例 3 · Lay 2.9 Exercises 15、27
**(Ex 15)** Suppose a $5 \times 8$ matrix $A$ has five pivot columns. Is $\operatorname{Col} A = \mathbb{R}^5$? Is $\operatorname{Nul} A = \mathbb{R}^3$? Explain your answers.

1. **先數形狀**:$m = 5$(列)、$n = 8$(行)、樞軸 5 個。
2. **第一問:$\operatorname{Col} A = \mathbb{R}^5$?** **是。** 5 個樞軸行表示每一**列**都有樞軸 ⇒ 各行張成 $\mathbb{R}^5$(第 3 週的定理)。用維度講也一樣:$\dim \operatorname{Col} A = 5$,而 $\mathbb{R}^5$ 裡唯一的 5 維子空間就是 $\mathbb{R}^5$ 自己。
3. **第二問:$\operatorname{Nul} A = \mathbb{R}^3$?** **不是**——但理由不是維度不對!$\operatorname{Nul} A$ 的向量有 **8** 個分量,它是 $\mathbb{R}^8$ 的子空間,**不可能等於** $\mathbb{R}^3$。
4. **然而它確實是 3 維的**:由 Rank Theorem,$\dim \operatorname{Nul} A = 8 - 5 = 3$。
5. **「3 維」與「$= \mathbb{R}^3$」的差別**就是這題的全部重點。課本原話:「$\operatorname{Nul} A$ *cannot* equal $\mathbb{R}^3$, because $\operatorname{Nul} A$ is a subspace of $\mathbb{R}^8$. It is true, however, that $\operatorname{Nul} A$ is three-dimensional.」

**(Ex 27)** If the subspace of all solutions of $A\mathbf{x} = \mathbf{0}$ has a basis consisting of three vectors and if $A$ is a $5 \times 7$ matrix, what is the rank of $A$?

6. **翻譯題目**:「$A\mathbf{x} = \mathbf{0}$ 的解集」就是 $\operatorname{Nul} A$;「基底有 3 個向量」就是 $\dim \operatorname{Nul} A = 3$。
7. **抓行數**:$5 \times 7$ ⇒ $n = 7$(**不是 5**)。
8. **套定理**:$\operatorname{rank} A = 7 - 3 = 4$。
9. **合理性檢查**:$\operatorname{rank} A \le \min(5, 7) = 5$,而 $4 \le 5$,沒有矛盾 ✓。
10. **這個檢查不是多餘的**——下一組題目裡的 Exercise 28 就是因為沒通過這個檢查而**無解**(見該題備註)。

#### 備註
例 3 的第 3 點請務必板書:學生最常見的錯是看到「$\dim = 3$」就寫「$= \mathbb{R}^3$」。反問一句「那些向量有幾個分量?」通常就能點破。

## 易錯點
- **把向量個數當維度**(例 1 的第 6 點):3 個向量可能只張出 2 維。
- **Rank Theorem 用錯數字**:要用**行數 $n$**。$7 \times 6$ 用 6、$5 \times 7$ 用 7。
- **「$\dim = k$」寫成「$= \mathbb{R}^k$」**(Exercises 15、16)。要先問「向量有幾個分量」。
- **忘了 $\operatorname{rank} A \le \min(m, n)$**。算出來的 rank 若超過列數就是錯了(或題目本身有問題,如 Exercise 28)。
- **$\{\mathbf{0}\}$ 的維度寫成 1**。零子空間維度是 **0**,而且它**沒有基底**(零向量自己就線性相依)。
- **把 rank 當成「非零列的個數」**去數原矩陣。必須先化成階梯形。

## 教學提示
這個觀念 25 分鐘,是本週的重心,也是期中考必考(Rank Theorem 的證明另外排 15 分鐘的證明時刻)。

建議先講維度(10 分鐘,用 PP1 立刻示範「3 個向量、2 維」),再講 rank(5 分鐘,強調它只是 $\dim \operatorname{Col} A$ 的別名),最後用長條圖把 Rank Theorem **講清楚結論**(5 分鐘)。**長條圖務必畫在黑板上**:$n$ 個格子,一部分塗色叫樞軸行、剩下叫自由行,學生看一眼就懂為什麼會加起來等於 $n$。剩下 5 分鐘做 Exercise 9 與 27。

**Exercises 15、16 這對題目建議一定要在課堂上做**,因為「3 維」與「$=\mathbb{R}^3$」的混淆若不當場打掉,期中考一定重演。

課堂建議做:Practice Problem 1、Exercise 9、Exercise 15、Exercise 27。Exercises 10–14 當作業。

**Exercise 28 的處理**:這題在 Global Edition 印錯了($3 \times 7$ 矩陣不可能有 3 維零空間),但**不要跳過**——把它當成「合理性檢查救了你一次」的教材,比正常題更有價值。我在該題備註寫了兩種改法。

Exercises 30–32 是構造與證明題,難度較高,列為挑戰;其中 32 書上把 rank 1 印成「rank l」,講義已改正。

## 練習
### 照做 · Lay 2.9 Exercises 9–12
Exercises 9–12 display a matrix $A$ and an echelon form of $A$. Find bases for $\operatorname{Col} A$ and $\operatorname{Nul} A$, and then state the dimensions of these subspaces.

(9) $A = \begin{bmatrix} 1 & -3 & 2 & -4 \\ -3 & 9 & -1 & 5 \\ 2 & -6 & 4 & -3 \\ -4 & 12 & 2 & 7 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 2 & -4 \\ 0 & 0 & 5 & -7 \\ 0 & 0 & 0 & 5 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

(10) $A = \begin{bmatrix} 1 & -2 & 9 & 5 & 4 \\ 1 & -1 & 6 & 5 & -3 \\ -2 & 0 & -6 & 1 & -2 \\ 4 & 1 & 9 & 1 & -9 \end{bmatrix} \sim \begin{bmatrix} 1 & -2 & 9 & 5 & 4 \\ 0 & 1 & -3 & 0 & -7 \\ 0 & 0 & 0 & 1 & -2 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

(11) $A = \begin{bmatrix} 1 & 2 & -5 & 0 & -1 \\ 2 & 5 & -8 & 4 & 3 \\ -3 & -9 & 9 & -7 & -2 \\ 3 & 10 & -7 & 11 & 7 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 & -5 & 0 & -1 \\ 0 & 1 & 2 & 4 & 5 \\ 0 & 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

(12) $A = \begin{bmatrix} 1 & 2 & -4 & 3 & 3 \\ 5 & 10 & -9 & -7 & 8 \\ 4 & 8 & -9 & -2 & 7 \\ -2 & -4 & 5 & 0 & -6 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 & -4 & 3 & 3 \\ 0 & 0 & 1 & -2 & 0 \\ 0 & 0 & 0 & 0 & -5 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

#### 解答
(9) 樞軸在第 1、3、4 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 1 \\ -3 \\ 2 \\ -4 \end{bmatrix}, \begin{bmatrix} 2 \\ -1 \\ 4 \\ 2 \end{bmatrix}, \begin{bmatrix} -4 \\ 5 \\ -3 \\ 7 \end{bmatrix}\right\} \; (\dim = 3), \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} 3 \\ 1 \\ 0 \\ 0 \end{bmatrix}\right\} \; (\dim = 1)$$

(10) 樞軸在第 1、2、4 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 1 \\ 1 \\ -2 \\ 4 \end{bmatrix}, \begin{bmatrix} -2 \\ -1 \\ 0 \\ 1 \end{bmatrix}, \begin{bmatrix} 5 \\ 5 \\ 1 \\ 1 \end{bmatrix}\right\} \; (\dim = 3), \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} -3 \\ 3 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 7 \\ 0 \\ 2 \\ 1 \end{bmatrix}\right\} \; (\dim = 2)$$

(11) 樞軸在第 1、2、4 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 1 \\ 2 \\ -3 \\ 3 \end{bmatrix}, \begin{bmatrix} 2 \\ 5 \\ -9 \\ 10 \end{bmatrix}, \begin{bmatrix} 0 \\ 4 \\ -7 \\ 11 \end{bmatrix}\right\} \; (\dim = 3), \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} 9 \\ -2 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} -5 \\ 3 \\ 0 \\ -2 \\ 1 \end{bmatrix}\right\} \; (\dim = 2)$$

(12) 樞軸在第 1、3、5 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 1 \\ 5 \\ 4 \\ -2 \end{bmatrix}, \begin{bmatrix} -4 \\ -9 \\ -9 \\ 5 \end{bmatrix}, \begin{bmatrix} 3 \\ 8 \\ 7 \\ -6 \end{bmatrix}\right\} \; (\dim = 3), \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} -2 \\ 1 \\ 0 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 5 \\ 0 \\ 2 \\ 1 \\ 0 \end{bmatrix}\right\} \; (\dim = 2)$$

#### 備註
(9)(11) 書後有解答;(10)(12) 書後無解答,答案為本講義計算並以 sympy 驗過。

四題都要用 Rank Theorem 自我檢查:(9) $3 + 1 = 4$;(10)(11)(12) 都是 $3 + 2 = 5$ ✓。

(9) 的第 2 行不是樞軸行(它是第 1 行的 $-3$ 倍),(12) 的第 2、4 行不是——這兩題刻意讓非樞軸行出現在中間,避免學生養成「取前 $k$ 行」的壞習慣。

### 照做 · Lay 2.9 Exercises 13–14 與 Practice Problem 1
In Exercises 13 and 14, find a basis for the subspace spanned by the given vectors. What is the dimension of the subspace?

(13) $\begin{bmatrix} 1 \\ -3 \\ 2 \\ -4 \end{bmatrix}$, $\begin{bmatrix} -3 \\ 9 \\ -6 \\ 12 \end{bmatrix}$, $\begin{bmatrix} 2 \\ -1 \\ 4 \\ 2 \end{bmatrix}$, $\begin{bmatrix} -4 \\ 5 \\ -3 \\ 7 \end{bmatrix}$

(14) $\begin{bmatrix} 1 \\ -1 \\ -2 \\ 5 \end{bmatrix}$, $\begin{bmatrix} 2 \\ -3 \\ -1 \\ 6 \end{bmatrix}$, $\begin{bmatrix} 0 \\ 2 \\ -6 \\ 8 \end{bmatrix}$, $\begin{bmatrix} -1 \\ 4 \\ -7 \\ 7 \end{bmatrix}$, $\begin{bmatrix} 3 \\ -8 \\ 9 \\ -5 \end{bmatrix}$

(Practice Problem 1) Determine the dimension of the subspace $H$ of $\mathbb{R}^3$ spanned by the vectors $\mathbf{v}_1 = \begin{bmatrix} 2 \\ -8 \\ 6 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 3 \\ -7 \\ -1 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} -1 \\ 6 \\ -7 \end{bmatrix}$. (First, find a basis for $H$.)

#### 解答
(13) 排成矩陣後樞軸在第 1、3、4 行,所以基底取**原來的**第 1、3、4 個向量,$\dim H = 3$。(第 2 個向量 $= -3 \times$ 第 1 個,被淘汰。)

(14) 樞軸在第 1、2 行,基底 $\left\{\begin{bmatrix} 1 \\ -1 \\ -2 \\ 5 \end{bmatrix}, \begin{bmatrix} 2 \\ -3 \\ -1 \\ 6 \end{bmatrix}\right\}$,$\dim H = 2$。其餘三個都是它們的組合:$\mathbf{v}_3 = 4\mathbf{v}_1 - 2\mathbf{v}_2$、$\mathbf{v}_4 = 5\mathbf{v}_1 - 3\mathbf{v}_2$、$\mathbf{v}_5 = -7\mathbf{v}_1 + 5\mathbf{v}_2$。

(PP1) 樞軸在第 1、2 行,基底 $\{\mathbf{v}_1, \mathbf{v}_2\}$,$\dim H = 2$:$H$ 是 $\mathbb{R}^3$ 裡的一個平面。

#### 備註
(13) 書後解答為「Columns 1, 3, and 4 of the original matrix form a basis for $H$, so $\dim H = 3$」;(14) 書後無解答。

(13) 的四個向量排成的矩陣**就是 Exercise 9 的 $A$**,可以直接沿用那裡的階梯形——值得提醒學生「兩題其實是同一題的兩種問法」。

(14) 有 5 個向量卻只有 2 維,是「向量個數 ≠ 維度」最誇張的例子。

PP1 的解答附在課本 p. 192,做法與 (13) 相同。

### 是非 · Lay 2.9 Exercises 21–24
In Exercises 21–24, mark each statement True or False. Justify each answer. Here $A$ is an $m \times n$ matrix.

(21) **(T/F)** The dimension of $\operatorname{Col} A$ is the number of pivot columns of $A$.

(22) **(T/F)** The dimension of $\operatorname{Nul} A$ is the number of variables in the equation $A\mathbf{x} = \mathbf{0}$.

(23) **(T/F)** The dimensions of $\operatorname{Col} A$ and $\operatorname{Nul} A$ add up to the number of columns of $A$.

(24) **(T/F)** The dimension of the column space of $A$ is $\operatorname{rank} A$.

#### 解答
- (21) **True.** 樞軸行構成 $\operatorname{Col} A$ 的基底(Theorem 13),所以 $\dim \operatorname{Col} A$ 就是樞軸行的個數。
- (22) **False.** 應該是**自由**變數的個數,不是全部變數的個數;$\dim \operatorname{Nul} A = n - \operatorname{rank} A$。
- (23) **True.** 這就是 Rank Theorem($\dim \operatorname{Col} A = \operatorname{rank} A$)。
- (24) **True.** 這是 rank 的定義本身(課本 p. 188)。

#### 備註
**書後對 Exercises 17–25 沒有給 T/F 答案**(只寫「See the *Study Guide*」),上面的答案是本講義判定的。

(22) 是本組唯一的 False,而且錯得很細:只差「自由」兩個字。批改時要求學生寫出正確版本,不能只打 F。

(21)(23)(24) 三題其實是「rank 的三種說法」:樞軸行個數 = $\dim \operatorname{Col} A$ = $\operatorname{rank} A$,而它們與 $\dim \operatorname{Nul} A$ 相加得 $n$。可以叫學生把這條等式鏈寫成一行。

### 變化 · Lay 2.9 Exercises 15–16 與 Practice Problem 3
(15) Suppose a $5 \times 8$ matrix $A$ has five pivot columns. Is $\operatorname{Col} A = \mathbb{R}^5$? Is $\operatorname{Nul} A = \mathbb{R}^3$? Explain your answers.

(16) Suppose a $5 \times 8$ matrix $A$ has two pivot columns. Is $\operatorname{Col} A = \mathbb{R}^2$? What is the dimension of $\operatorname{Nul} A$? Explain your answers.

(Practice Problem 3) Could $\mathbb{R}^3$ possibly contain a four-dimensional subspace? Explain.

#### 解答
(15) $\operatorname{Col} A = \mathbb{R}^5$:**是**。5 個樞軸行 ⇒ 每一列都有樞軸 ⇒ 各行張成 $\mathbb{R}^5$。$\operatorname{Nul} A = \mathbb{R}^3$:**否**,因為 $\operatorname{Nul} A$ 是 $\mathbb{R}^8$ 的子空間(解向量有 8 個分量);但它確實是 **3 維**的,因為 8 行中只有 5 個樞軸行,有 3 個自由變數。

(16) $\operatorname{Col} A = \mathbb{R}^2$:**否**。$\operatorname{Col} A$ 是 $\mathbb{R}^5$ 的子空間(行向量有 5 個分量),它只是「2 維的」,不是 $\mathbb{R}^2$。$\dim \operatorname{Nul} A = 8 - 2 = 6$(Rank Theorem)。

(PP3) **不可能。** 四維子空間的基底要有 4 個線性獨立向量,但 $\mathbb{R}^3$ 中任何線性獨立集最多 3 個向量。所以 $\mathbb{R}^3$ 的子空間維度最多是 3;唯一的 3 維子空間就是 $\mathbb{R}^3$ 本身,其餘子空間的維度是 2、1 或 0。

#### 備註
(15) 書後有解答;(16) 書後無解答。兩題是刻意配對的:**一題的「等於」成立、另一題不成立**,差別只在「$\dim$ 剛好等於所在空間的維度」與否。

課本對 (15) 的原話值得抄給學生:「$\operatorname{Nul} A$ *cannot* equal $\mathbb{R}^3$, because $\operatorname{Nul} A$ is a subspace of $\mathbb{R}^8$. It is true, however, that $\operatorname{Nul} A$ is three-dimensional.」

PP3 與這兩題是同一件事的不同方向:**維度受所在空間限制**。

### 變化 · Lay 2.9 Exercises 27–29
In Exercises 27–32, justify each answer or construction.

(27) If the subspace of all solutions of $A\mathbf{x} = \mathbf{0}$ has a basis consisting of three vectors and if $A$ is a $5 \times 7$ matrix, what is the rank of $A$?

(28) What is the rank of a $3 \times 7$ matrix whose null space is three-dimensional?

(29) If the rank of a $7 \times 6$ matrix $A$ is 4, what is the dimension of the solution space of $A\mathbf{x} = \mathbf{0}$?

#### 解答
(27) 解集就是 $\operatorname{Nul} A$,基底 3 個向量 ⇒ $\dim \operatorname{Nul} A = 3$。$A$ 有 7 **行**,由 Rank Theorem $\operatorname{rank} A = 7 - 3 = 4$。(檢查:$4 \le \min(5, 7) = 5$ ✓)

(28) **照定理算會得到 $\operatorname{rank} A = 7 - 3 = 4$,但這與 $3 \times 7$ 矩陣的形狀矛盾**:只有 3 列的矩陣最多 3 個樞軸,$\operatorname{rank} A \le 3 < 4$。所以**題目給的矩陣不存在**。事實上任何 $3 \times 7$ 矩陣都滿足 $\dim \operatorname{Nul} A = 7 - \operatorname{rank} A \ge 7 - 3 = 4$,零空間至少是 4 維。

(29) $A$ 有 6 **行**,$\dim \operatorname{Nul} A = 6 - \operatorname{rank} A = 6 - 4 = 2$。

#### 備註
(27)(29) 書後有解答且與上面一致;(28) 書後無解答。書上的共同指示涵蓋 27–32,本講義拆成兩張卡片:這裡做 27–29,30–32 放在下一張挑戰卡。

**(28) 的數字自相矛盾**(用 $\operatorname{rank} A \le \min(m, n)$ 一驗就知道),推測是改動題目數字時沒有重新檢查;手邊只有 Global Edition,無從比對美國版。

**建議照原樣出給學生**,把它當成「$\operatorname{rank} A \le \min(m,n)$ 這個合理性檢查什麼時候會救你」的教材;願意改題的話,改成「$4 \times 7$ 矩陣」(答案 4)或「零空間是**四**維」(答案 3)都可以。

(27) 與 (29) 的陷阱都是**用列數代替行數**:$5 \times 7$ 要用 7、$7 \times 6$ 要用 6。批改時先看學生用哪個數字。

### 挑戰 · Lay 2.9 Exercises 30–32
In Exercises 27–32, justify each answer or construction.

(30) Show that a set of vectors $\{\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_5\}$ in $\mathbb{R}^n$ is linearly dependent when $\dim \operatorname{Span}\{\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_5\} = 4$.

(31) If possible, construct a $3 \times 4$ matrix $A$ such that $\dim \operatorname{Nul} A = 2$ and $\dim \operatorname{Col} A = 2$.

(32) Construct a $4 \times 3$ matrix with rank 1.

#### 解答
(30) 令 $H = \operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_5\}$,已知 $\dim H = 4$。**反證**:若這 5 個向量線性獨立,則它們既獨立又張成 $H$,就是 $H$ 的一組基底,於是 $\dim H = 5$,與 $\dim H = 4$ 矛盾(維度的定義要求每組基底個數相同)。故它們必線性相依。

也可以直接算:把它們排成 $A$,$\operatorname{rank} A = \dim \operatorname{Col} A = 4 < 5$ ⇒ 有非樞軸行 ⇒ $A\mathbf{x} = \mathbf{0}$ 有自由變數、有非平凡解 ⇒ 相依。

(31) **可以。** $A$ 有 4 行,$2 + 2 = 4$ 正好滿足 Rank Theorem,所以不衝突;只要讓 $A$ 恰有 2 個樞軸行即可。例如
$$A = \begin{bmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
$\operatorname{rank} A = 2$,而 $\dim \operatorname{Nul} A = 4 - 2 = 2$(**由 Rank Theorem 自動成立,不必另外驗**)。

(32) 任何非零的秩 1 矩陣都行,例如把同一個行向量乘上不同倍數:
$$A = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 3 & 6 & 9 \\ 4 & 8 & 12 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 3 \\ 4 \end{bmatrix}\begin{bmatrix} 1 & 2 & 3 \end{bmatrix}$$
三個行都在同一條過原點的直線上,所以 $\dim \operatorname{Col} A = 1$。

#### 備註
本卡是上一張卡共同指示(27–32)的後半。(30)(32) 書後無解答;(31) 書後給的作法是「任取 $\mathbb{R}^3$ 中兩個明顯不成比例的向量,各複製一份湊成 4 行」,並特別指出「There is no need to worry about whether $\operatorname{Nul} A$ has the correct dimension, since this is guaranteed by the Rank Theorem」——**這句話就是本題的教學重點**:構造時只要顧 rank,零空間會自己對。

**(32) 書上印成「Construct a $4 \times 3$ matrix with rank l.」(小寫字母 L),應為數字 1**,講義已改正。

(31)(32) 是構造題,**答案不唯一**,批改看的是理由而非矩陣本身。若學生的 (32) 寫成零矩陣,那是 rank 0,不對。

(30) 建議要求寫「反證」版本,因為它直接用到維度的定義;第二種算法雖然也對,但繞回了樞軸。

## 驗算
```check
(lambda a: a.rank() == 2 and a.rref()[1] == (0, 1))(Matrix([[2, 3, -1], [-8, -7, 6], [6, -1, -7]]))
(lambda a: a.rref()[1] == (0, 2, 3) and a.nullspace() == [Matrix([3, 1, 0, 0])] and a.rank() + len(a.nullspace()) == a.cols)(Matrix([[1, -3, 2, -4], [-3, 9, -1, 5], [2, -6, 4, -3], [-4, 12, 2, 7]]))
(lambda a: a.rref()[1] == (0, 1, 3) and a.nullspace() == [Matrix([-3, 3, 1, 0, 0]), Matrix([0, 7, 0, 2, 1])] and a.rank() + len(a.nullspace()) == a.cols)(Matrix([[1, -2, 9, 5, 4], [1, -1, 6, 5, -3], [-2, 0, -6, 1, -2], [4, 1, 9, 1, -9]]))
(lambda a: a.rref()[1] == (0, 1, 3) and a.nullspace() == [Matrix([9, -2, 1, 0, 0]), Matrix([-5, 3, 0, -2, 1])] and a.rank() + len(a.nullspace()) == a.cols)(Matrix([[1, 2, -5, 0, -1], [2, 5, -8, 4, 3], [-3, -9, 9, -7, -2], [3, 10, -7, 11, 7]]))
(lambda a: a.rref()[1] == (0, 2, 4) and a.nullspace() == [Matrix([-2, 1, 0, 0, 0]), Matrix([5, 0, 2, 1, 0])] and a.rank() + len(a.nullspace()) == a.cols)(Matrix([[1, 2, -4, 3, 3], [5, 10, -9, -7, 8], [4, 8, -9, -2, 7], [-2, -4, 5, 0, -6]]))
(lambda a: a.rref()[1] == (0, 1) and a.rank() == 2)(Matrix([[1, 2, 0, -1, 3], [-1, -3, 2, 4, -8], [-2, -1, -6, -7, 9], [5, 6, 8, 7, -5]]))
4 * Matrix([1, -1, -2, 5]) - 2 * Matrix([2, -3, -1, 6]) == Matrix([0, 2, -6, 8])
5 * Matrix([1, -1, -2, 5]) - 3 * Matrix([2, -3, -1, 6]) == Matrix([-1, 4, -7, 7])
-7 * Matrix([1, -1, -2, 5]) + 5 * Matrix([2, -3, -1, 6]) == Matrix([3, -8, 9, -5])
-3 * Matrix([1, -3, 2, -4]) == Matrix([-3, 9, -6, 12])
8 - 5 == 3 and 8 - 2 == 6
7 - 3 == 4 and 4 <= min(5, 7)
7 - 3 == 4 and 4 > min(3, 7)
6 - 4 == 2
(lambda a: a.rank() == 2 and len(a.nullspace()) == 2 and a.rank() + len(a.nullspace()) == a.cols)(Matrix([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 0]]))
(lambda a: a.rank() == 1 and len(a.nullspace()) == 2)(Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9], [4, 8, 12]]))
Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9], [4, 8, 12]]) == Matrix([1, 2, 3, 4]) * Matrix([[1, 2, 3]])
```
