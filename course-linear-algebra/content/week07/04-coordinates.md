---
title_en: Coordinate Systems
title_zh: 座標:在新格線下的地址
sub: A basis turns a subspace into R^p
level: mid
source: Lay 2.9
lab_hook: 'Lab 會把同一個向量在標準基底與 B 基底下的兩組座標並排畫出來'
---
## 觀念
**Definition.** Suppose the set $\mathcal{B} = \{\mathbf{b}_1, \dots, \mathbf{b}_p\}$ is a basis for a subspace $H$. For each $\mathbf{x}$ in $H$, the **coordinates of $\mathbf{x}$ relative to the basis $\mathcal{B}$** are the weights $c_1, \dots, c_p$ such that $\mathbf{x} = c_1\mathbf{b}_1 + \cdots + c_p\mathbf{b}_p$, and the vector in $\mathbb{R}^p$

$$[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} c_1 \\ \vdots \\ c_p \end{bmatrix}$$

is called the **coordinate vector of $\mathbf{x}$ (relative to $\mathcal{B}$)** or the **$\mathcal{B}$-coordinate vector of $\mathbf{x}$**.

> 課本腳註:It is important that the elements of $\mathcal{B}$ are numbered because the entries in $[\,\mathbf{x}\,]_{\mathcal{B}}$ depend on the order of the vectors in $\mathcal{B}$.

因為 $\mathcal{B}$ 線性獨立,這組權重是**唯一**的——這正是上一個觀念裡「基底沒有多餘向量」的實際好處。若 $\mathcal{B}$ 是 $H$ 的基底而 $\dim H = p$,則對應

$$\mathbf{x} \longmapsto [\,\mathbf{x}\,]_{\mathcal{B}}$$

是 $H$ 與 $\mathbb{R}^p$ 之間保持線性組合的一對一對應;課本說這使得 $H$「looks and acts the same as $\mathbb{R}^p$」(p. 188)。

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| coordinate vector | 座標向量 | $[\,\mathbf{x}\,]_{\mathcal{B}}$:$\mathbf{x}$ 在基底 $\mathcal{B}$ 下的「地址」 |
| coordinates relative to $\mathcal{B}$ | 相對於 $\mathcal{B}$ 的座標 | 那組唯一的權重 $c_1, \dots, c_p$ |
| $\mathcal{B}$-coordinate vector | $\mathcal{B}$ 座標向量 | 同上,較短的講法 |
| change-of-coordinates matrix | 座標轉換矩陣 | $P_{\mathcal{B}} = [\,\mathbf{b}_1 \; \cdots \; \mathbf{b}_p\,]$,滿足 $\mathbf{x} = P_{\mathcal{B}}[\,\mathbf{x}\,]_{\mathcal{B}}$ |
| isomorphism | 同構 | 兩個空間「長得一樣、運算也一樣」的一對一對應 |
| estimate from the figure | 由圖估計 | 從格線上數格子讀出座標(Ex 7、8) |

## 白話說
**座標 = 在新格線下的地址。**

標準基底 $\mathbf{e}_1, \mathbf{e}_2$ 給的是「橫走幾格、豎走幾格」;換一組基底 $\mathbf{b}_1, \mathbf{b}_2$,就是把方格紙換成**斜的格線**,地址變成「沿 $\mathbf{b}_1$ 走幾步、沿 $\mathbf{b}_2$ 走幾步」。

**同一個點,兩種地址**:向量本身沒有變,只是**報路的方式**變了。

兩個方向的操作,難度完全不同:

| 要求 | 給什麼 | 怎麼做 | 難度 |
|---|---|---|---|
| 找 $\mathbf{x}$ | 座標 $[\,\mathbf{x}\,]_{\mathcal{B}}$ | **乘進去**:$\mathbf{x} = c_1\mathbf{b}_1 + \cdots + c_p\mathbf{b}_p$ | 加減乘,一行算完 |
| 找 $[\,\mathbf{x}\,]_{\mathcal{B}}$ | 向量 $\mathbf{x}$ | **解方程**:$P_{\mathcal{B}}\,\mathbf{c} = \mathbf{x}$ | 要列化簡 |

其中 $P_{\mathcal{B}} = [\,\mathbf{b}_1 \; \cdots \; \mathbf{b}_p\,]$ 就是把基底向量排成的矩陣,課本稱它**座標轉換矩陣**。

$$\mathbf{x} = P_{\mathcal{B}}\,[\,\mathbf{x}\,]_{\mathcal{B}} \qquad \Longleftrightarrow \qquad [\,\mathbf{x}\,]_{\mathcal{B}} = P_{\mathcal{B}}^{-1}\mathbf{x} \;\;(\text{$P_{\mathcal{B}}$ 可逆時})$$

**注意向量的長度會變**:$H$ 是 $\mathbb{R}^4$ 裡的 2 維子空間時,$\mathbf{x}$ 有 4 個分量,但 $[\,\mathbf{x}\,]_{\mathcal{B}}$ 只有 **2** 個。用 2 個數字就足以記住那個 4 維向量——這就是「$H$ 跟 $\mathbb{R}^2$ 一樣」的意思,也是壓縮的原理。

## 幾何意義
![用 b1、b2 畫出的座標格線,x 在 b1 方向 3 格、b2 方向 2 格](coord-pp2.svg)

這是課本 2.9 Practice Problem 2 的圖:基底 $\mathcal{B} = \left\{\begin{bmatrix} 1 \\ .2 \end{bmatrix}, \begin{bmatrix} .2 \\ 1 \end{bmatrix}\right\}$ 把平面鋪成一片**略微歪斜的格線**。

- 虛線就是「新的方格紙」:一組平行於 $\mathbf{b}_1$、一組平行於 $\mathbf{b}_2$。
- $[\,\mathbf{x}\,]_{\mathcal{B}} = (3, 2)$ 的意思是:從原點出發,**沿 $\mathbf{b}_1$ 方向走 3 格、沿 $\mathbf{b}_2$ 方向走 2 格**。
- 走到的點在標準座標下是 $(3.4, 2.6)$。兩組數字描述**同一個點**。
- 基底越接近互相垂直、長度越接近 1,新格線就越像原來的方格紙。上圖的 $\mathbf{b}_1, \mathbf{b}_2$ 幾乎垂直,所以看起來只是「稍微歪」。

**Exercises 7、8 就是反過來讀這張圖**:圖上已經畫好格線與點,要你**數格子**把座標讀出來,再用代數驗證。

## 在資工哪裡用
- **換基底 = 換表示法**。同一張影像在像素基底下要 $1024^2$ 個數字,在 DCT(JPEG)或小波基底下,少數幾個座標就能重建大部分內容。**壓縮就是「挑一組好基底,然後丟掉小座標」**。
- **PCA / 嵌入向量**:機器學習把資料投到主成分基底上,座標向量就是「特徵」。word embedding 的 300 維向量,就是某個詞在 300 個基底方向上的座標。
- **顏色空間**:RGB、YCbCr、HSV 是同一個顏色的不同座標。JPEG 先把 RGB 換成 YCbCr,正是因為在那組基底下可以少存一些座標。
- **繪圖與遊戲的區域座標**:模型有自己的 local basis,世界有 world basis;每一次 `transform` 都是座標轉換 $\mathbf{x} = P_{\mathcal{B}}[\,\mathbf{x}\,]_{\mathcal{B}}$。
- **第 13 週的正交基底**會讓「找座標」從「解方程」變成「算內積」,那是這個觀念最重要的續集。

## 原理
**為什麼座標是唯一的?**(課本 p. 186 的推導)

設 $\mathcal{B} = \{\mathbf{b}_1, \dots, \mathbf{b}_p\}$ 是 $H$ 的基底,而同一個 $\mathbf{x}$ 有兩種寫法:

$$\mathbf{x} = c_1\mathbf{b}_1 + \cdots + c_p\mathbf{b}_p = d_1\mathbf{b}_1 + \cdots + d_p\mathbf{b}_p$$

兩式相減:

$$\mathbf{0} = (c_1 - d_1)\mathbf{b}_1 + \cdots + (c_p - d_p)\mathbf{b}_p$$

因為 $\mathcal{B}$ **線性獨立**,這個組合等於 $\mathbf{0}$ 的唯一方式是所有權重為 0,即 $c_j = d_j$ 對每個 $j$ 成立。所以兩種寫法其實是同一種。$\blacksquare$

**注意這裡用到的是「獨立」而不是「張成」**:張成保證「寫得出來」,獨立保證「只有一種寫法」。**基底兩條件各管一件事**,這是本節最值得記住的一句話。

**為什麼 $\mathbf{x} \mapsto [\,\mathbf{x}\,]_{\mathcal{B}}$ 是同構?**

$\mathbf{x} = P_{\mathcal{B}}[\,\mathbf{x}\,]_{\mathcal{B}}$ 這個式子說明兩件事:

1. **每個座標向量對應唯一的 $\mathbf{x}$**(乘進去就得到)。
2. **每個 $\mathbf{x} \in H$ 對應唯一的座標向量**(上面剛證完)。

而且它保持運算:$[\,\mathbf{x} + \mathbf{y}\,]_{\mathcal{B}} = [\,\mathbf{x}\,]_{\mathcal{B}} + [\,\mathbf{y}\,]_{\mathcal{B}}$、$[\,c\mathbf{x}\,]_{\mathcal{B}} = c[\,\mathbf{x}\,]_{\mathcal{B}}$(直接由唯一性得到)。所以在 $H$ 裡做線性代數,和在 $\mathbb{R}^p$ 裡做**完全一樣**。

**這件事的實用價值**:$\mathbb{R}^4$ 裡的一個 2 維平面,雖然向量寫起來有 4 個分量,但它的「內部世界」就是一張紙($\mathbb{R}^2$)。我們可以只用 2 個數字工作,算完再乘回 $P_{\mathcal{B}}$ 回到 $\mathbb{R}^4$。

## 老師講解
### 例 1 · Lay 2.9 Practice Problem 2
Consider the basis $\mathcal{B} = \left\{\begin{bmatrix} 1 \\ .2 \end{bmatrix}, \begin{bmatrix} .2 \\ 1 \end{bmatrix}\right\}$ for $\mathbb{R}^2$. If $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$, what is $\mathbf{x}$?

1. **先看清楚給的是哪一邊**:給的是**座標**,要求的是**向量本身**。這是「乘進去」的方向,不必解方程。
2. **座標就是權重**:第 1 個分量 3 配 $\mathbf{b}_1$,第 2 個分量 2 配 $\mathbf{b}_2$。
3. **算出來**:
   $$\mathbf{x} = 3\mathbf{b}_1 + 2\mathbf{b}_2 = 3\begin{bmatrix} 1 \\ .2 \end{bmatrix} + 2\begin{bmatrix} .2 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 + .4 \\ .6 + 2 \end{bmatrix} = \begin{bmatrix} 3.4 \\ 2.6 \end{bmatrix}$$
4. **用矩陣寫同一件事**(之後都會這樣寫):
   $$\mathbf{x} = P_{\mathcal{B}}[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 1 & .2 \\ .2 & 1 \end{bmatrix}\begin{bmatrix} 3 \\ 2 \end{bmatrix} = \begin{bmatrix} 3.4 \\ 2.6 \end{bmatrix}$$
5. **對照上面的格線圖**:$\mathbf{x}$ 在 $\mathbf{b}_1$ 方向 3 格、在 $\mathbf{b}_2$ 方向 2 格。課本原話:「Note how $\mathbf{x}$ is 3 units in the $\mathbf{b}_1$-direction and 2 units in the $\mathbf{b}_2$-direction.」
6. **兩組數字都對**:$(3.4, 2.6)$ 是標準基底下的地址,$(3, 2)$ 是 $\mathcal{B}$ 下的地址,**同一個點**。

### 例 2 · Lay 2.9 Exercises 3、5
The vector $\mathbf{x}$ is in a subspace $H$ with a basis $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2\}$. Find the $\mathcal{B}$-coordinate vector of $\mathbf{x}$.

**(Ex 3)** $\mathbf{b}_1 = \begin{bmatrix} 1 \\ -4 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -2 \\ 7 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} -3 \\ 7 \end{bmatrix}$

1. **這次是反方向**:給向量、求座標 ⇒ **要解方程** $c_1\mathbf{b}_1 + c_2\mathbf{b}_2 = \mathbf{x}$。
2. **寫成方程組**:$c_1 - 2c_2 = -3$、$-4c_1 + 7c_2 = 7$。
3. **解**:第一式 $c_1 = -3 + 2c_2$,代入第二式 $-4(-3 + 2c_2) + 7c_2 = 7 \Rightarrow 12 - c_2 = 7 \Rightarrow c_2 = 5$,回代 $c_1 = 7$。
4. **答案要寫成向量**:$[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 7 \\ 5 \end{bmatrix}$。不是 $c_1 = 7, c_2 = 5$ 兩個數字散著寫。
5. **驗算**:$7\begin{bmatrix} 1 \\ -4 \end{bmatrix} + 5\begin{bmatrix} -2 \\ 7 \end{bmatrix} = \begin{bmatrix} 7 - 10 \\ -28 + 35 \end{bmatrix} = \begin{bmatrix} -3 \\ 7 \end{bmatrix}$ ✓

**(Ex 5)** $\mathbf{b}_1 = \begin{bmatrix} 1 \\ 5 \\ -3 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -3 \\ -7 \\ 5 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 4 \\ 10 \\ -7 \end{bmatrix}$

6. **這裡有 3 條方程式、只有 2 個未知數**——超定系統。做法一樣:先用其中兩式解出 $c_1, c_2$,再用第三式**檢查**。
7. **用前兩列**:$c_1 - 3c_2 = 4$、$5c_1 - 7c_2 = 10$。由第一式 $c_1 = 4 + 3c_2$,代入得 $20 + 8c_2 = 10 \Rightarrow c_2 = -\tfrac54$,$c_1 = 4 - \tfrac{15}{4} = \tfrac14$。
8. **第三式檢查**:$-3(\tfrac14) + 5(-\tfrac54) = -\tfrac34 - \tfrac{25}{4} = -7$ ✓ 相容,所以 $\mathbf{x}$ 真的在 $H = \operatorname{Span}\{\mathbf{b}_1, \mathbf{b}_2\}$ 裡。
9. $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 1/4 \\ -5/4 \end{bmatrix}$。**注意分量數變了**:$\mathbf{x}$ 有 3 個分量,座標只有 2 個——因為 $\dim H = 2$。
10. **如果第三式不成立**呢?那表示 $\mathbf{x} \notin H$,題目就沒有答案。題幹已經保證 $\mathbf{x} \in H$,所以第三式一定會過;但**電腦題 37、38 就是要自己驗這件事**。

### 例 3 · Lay 2.9 Exercise 7
Let $\mathbf{b}_1 = \begin{bmatrix} 3 \\ 0 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -1 \\ 2 \end{bmatrix}$, $\mathbf{w} = \begin{bmatrix} 7 \\ -2 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$, and $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2\}$. Use the figure to estimate $[\,\mathbf{w}\,]_{\mathcal{B}}$ and $[\,\mathbf{x}\,]_{\mathcal{B}}$.

![由 b1 = (3,0)、b2 = (-1,2) 畫出的座標格線,上面標出 w 與 x](coord-ex7.svg)

1. **先看懂格線**:兩組虛線分別平行於 $\mathbf{b}_1$ 與 $\mathbf{b}_2$。要讀 $\mathbf{w}$ 的座標,就看它落在**哪兩條線的交點上**。
2. **讀 $\mathbf{w}$**:從原點沿 $\mathbf{b}_1$ 走 2 格、再沿 $\mathbf{b}_2$ **倒退** 1 格,就到 $\mathbf{w}$。所以估計 $[\,\mathbf{w}\,]_{\mathcal{B}} = \begin{bmatrix} 2 \\ -1 \end{bmatrix}$。
3. **代數驗證**:$2\mathbf{b}_1 - \mathbf{b}_2 = \begin{bmatrix} 6 + 1 \\ 0 - 2 \end{bmatrix} = \begin{bmatrix} 7 \\ -2 \end{bmatrix}$ ✓
4. **讀 $\mathbf{x}$**:它不在格線交點上,落在**格子中間**——沿 $\mathbf{b}_1$ 約 1.5 格、沿 $\mathbf{b}_2$ 約 0.5 格。$[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 1.5 \\ .5 \end{bmatrix}$。
5. **題目要求確認**:$1.5\mathbf{b}_1 + 0.5\mathbf{b}_2 = \begin{bmatrix} 4.5 - 0.5 \\ 0 + 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$ ✓
6. **這題也可以純代數做**:$\mathbf{b}_1$ 的第二分量是 0,所以 $2c_2 = x_2$ 直接給出 $c_2$,再回第一式求 $c_1$。**遇到有 0 的基底,先從那一列下手。**
7. **為什麼要練「讀圖」?** 因為座標的意義是幾何的。只會解方程的學生,下學期看到特徵向量基底、正交基底時會完全沒有畫面。

#### 備註
例 3 的圖是自繪的,與課本 p. 191 的圖同一組數據。課堂上可先只給圖不給數字,讓學生猜 $[\,\mathbf{w}\,]_{\mathcal{B}}$,再公布 $\mathbf{b}_1, \mathbf{b}_2$ 驗算。

## 易錯點
- **把兩個方向搞反**:給座標求向量是**乘**,給向量求座標是**解**。看到 $[\,\mathbf{x}\,]_{\mathcal{B}}$ 出現在題目的「已知」還是「未知」,決定要做哪件事。
- **混淆 $\mathbf{x}$ 與 $[\,\mathbf{x}\,]_{\mathcal{B}}$**。兩者連**分量個數都不一樣**($n$ 對 $p$)。
- **答案沒寫成向量**,或把 $c_1, c_2$ 的順序寫反。基底是**有序**的(課本腳註特別強調)。
- **超定系統(Ex 5、6)忘了用第三列檢查**。雖然題目保證 $\mathbf{x} \in H$,少了這一步就沒驗證過。
- **讀圖時把「沿 $\mathbf{b}_2$ 倒退」讀成正的**。負座標在圖上是往反方向走。
- **以為座標一定是整數**。Ex 7 的 $\mathbf{x}$、Ex 8 的 $\mathbf{z}$ 都是半格。

## 教學提示
這個觀念 20 分鐘。**核心是一句話:座標 = 在新格線下的地址。**

建議的教學順序:先畫標準方格紙上的一個點 $(3.4, 2.6)$,再在同一張圖上疊一組**歪的格線**,問學生「在新格線下這個點的地址是什麼?」——學生自己數出 $(3, 2)$ 之後,再給定義。**先有畫面,再有符號。**

兩個方向務必分開講清楚(白話說的那張表建議抄在黑板上留著),因為期中考最常見的錯就是方向搞反。

課堂建議做:Practice Problem 2(乘進去);Exercise 3(解方程);Exercise 5(超定 + 檢查);Exercise 7(讀圖)。Exercises 1、2 要求學生自己畫格線圖,很適合當作業——**畫過一次圖的學生,才真的懂座標**。

是非 Exercises 17–20 可以口頭快問快答,其中 19(直線)與 20(同構)最有價值。

T 題 Exercises 37、38 放進實作課:$\mathbf{x}$ 有 4 個分量、座標只有 2 或 3 個,正好示範「維度壓縮」的感覺;同時它們要先驗證 $\mathbf{x} \in H$,是本節唯一會遇到「可能不相容」的題型。

## 練習
### 照做 · Lay 2.9 Exercises 1–2
In Exercises 1 and 2, find the vector $\mathbf{x}$ determined by the given coordinate vector $[\,\mathbf{x}\,]_{\mathcal{B}}$ and the given basis $\mathcal{B}$. Illustrate your answer with a figure, as in the solution of Practice Problem 2.

(1) $\mathcal{B} = \left\{\begin{bmatrix} 1 \\ 1 \end{bmatrix}, \begin{bmatrix} 2 \\ -1 \end{bmatrix}\right\}$, $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$

(2) $\mathcal{B} = \left\{\begin{bmatrix} -2 \\ 1 \end{bmatrix}, \begin{bmatrix} 3 \\ 1 \end{bmatrix}\right\}$, $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} -1 \\ 3 \end{bmatrix}$

#### 解答
- (1) $\mathbf{x} = 3\mathbf{b}_1 + 2\mathbf{b}_2 = 3\begin{bmatrix} 1 \\ 1 \end{bmatrix} + 2\begin{bmatrix} 2 \\ -1 \end{bmatrix} = \begin{bmatrix} 7 \\ 1 \end{bmatrix}$。圖:畫兩組平行虛線(一組平行 $\mathbf{b}_1$、一組平行 $\mathbf{b}_2$),標出 $\mathbf{b}_1, 2\mathbf{b}_1, 3\mathbf{b}_1$ 與 $\mathbf{b}_2, 2\mathbf{b}_2$,$\mathbf{x}$ 落在「$\mathbf{b}_1$ 方向 3 格、$\mathbf{b}_2$ 方向 2 格」的交點。
- (2) $\mathbf{x} = -1\begin{bmatrix} -2 \\ 1 \end{bmatrix} + 3\begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} 2 + 9 \\ -1 + 3 \end{bmatrix} = \begin{bmatrix} 11 \\ 2 \end{bmatrix}$。圖同上,注意第一個座標是**負**的,要往 $-\mathbf{b}_1$ 方向走一格。

#### 備註
(1) 書後有解答與格線圖;(2) 書後無解答,答案為本講義計算。

批改重點在**圖**而非數字:格線是否真的平行於兩個基底向量、負座標是否畫成反方向。學生常畫成標準方格紙加一個箭頭,那就沒抓到重點。

### 照做 · Lay 2.9 Exercises 3–6
In Exercises 3–6, the vector $\mathbf{x}$ is in a subspace $H$ with a basis $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2\}$. Find the $\mathcal{B}$-coordinate vector of $\mathbf{x}$.

(3) $\mathbf{b}_1 = \begin{bmatrix} 1 \\ -4 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -2 \\ 7 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} -3 \\ 7 \end{bmatrix}$

(4) $\mathbf{b}_1 = \begin{bmatrix} 1 \\ -3 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -4 \\ 7 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} -8 \\ 9 \end{bmatrix}$

(5) $\mathbf{b}_1 = \begin{bmatrix} 1 \\ 5 \\ -3 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -3 \\ -7 \\ 5 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 4 \\ 10 \\ -7 \end{bmatrix}$

(6) $\mathbf{b}_1 = \begin{bmatrix} -2 \\ 1 \\ 2 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -6 \\ 7 \\ 8 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 4 \\ 0 \\ -3 \end{bmatrix}$

#### 解答
- (3) $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 7 \\ 5 \end{bmatrix}$。由 $c_1 - 2c_2 = -3$、$-4c_1 + 7c_2 = 7$ 解得。
- (4) $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 4 \\ 3 \end{bmatrix}$。由 $c_1 - 4c_2 = -8$、$-3c_1 + 7c_2 = 9$ 解得。
- (5) $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 1/4 \\ -5/4 \end{bmatrix}$。前兩列解出後,第三列 $-3(\tfrac14) + 5(-\tfrac54) = -7$ ✓。
- (6) $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} -7/2 \\ 1/2 \end{bmatrix}$。第二列 $c_1 + 7c_2 = 0$ 最好下手,得 $c_1 = -7c_2$;代入第一列 $-2c_1 - 6c_2 = 4$ 得 $c_2 = \tfrac12$;第三列 $2(-\tfrac72) + 8(\tfrac12) = -3$ ✓。

#### 備註
(3)(5) 書後有解答;(4)(6) 書後無解答,答案為本講義計算。

(5)(6) 是**三列、兩未知數**的超定系統:用兩列解、用第三列驗。學生若三列一起硬解,容易在化簡時搞混;提醒他們「先挑最好算的兩列」。

(6) 的第二列有 $c_1$ 的係數 1、且右邊是 0,是最省力的入手處——值得當成解題習慣強調。

### 是非 · Lay 2.9 Exercises 17–20
In Exercises 17–20, mark each statement True or False. Justify each answer. Here $A$ is an $m \times n$ matrix.

(17) **(T/F)** If $\mathcal{B} = \{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ is a basis for a subspace $H$ and if $\mathbf{x} = c_1\mathbf{v}_1 + \cdots + c_p\mathbf{v}_p$, then $c_1, \dots, c_p$ are the coordinates of $\mathbf{x}$ relative to the basis $\mathcal{B}$.

(18) **(T/F)** If $\mathcal{B}$ is a basis for a subspace $H$, then each vector in $H$ can be written in only one way as a linear combination of the vectors in $\mathcal{B}$.

(19) **(T/F)** Each line in $\mathbb{R}^n$ is a one-dimensional subspace of $\mathbb{R}^n$.

(20) **(T/F)** If $\mathcal{B} = \{\mathbf{v}_1, \dots, \mathbf{v}_p\}$ is a basis for a subspace $H$ of $\mathbb{R}^n$, then the correspondence $\mathbf{x} \mapsto [\,\mathbf{x}\,]_{\mathcal{B}}$ makes $H$ look and act the same as $\mathbb{R}^p$.

#### 解答
- (17) **True.** 這就是課本 p. 187 座標的定義;因為 $\mathcal{B}$ 線性獨立,這組權重還是唯一的。
- (18) **True.** 唯一性的證明:兩種寫法相減得到 $\mathbf{0}$ 的一個線性組合,由獨立性所有權重差為 0。
- (19) **False.** 只有**通過原點**的直線才是子空間;不過原點的直線連 $\mathbf{0}$ 都不含,不是子空間,更談不上「1 維子空間」。
- (20) **True.** 課本 p. 188 明文:這個對應是保持線性組合的一對一對應(同構)。

#### 備註
**書後對 Exercises 17–25 只寫「See the *Study Guide* after you write your justifications.」,完全沒給 T/F 答案**,上面的答案是本講義判定的。

(19) 是本組唯一的 False,幾乎每年都有人答錯。教學時把「直線」與「過原點的直線」並排寫在黑板上。

(17) 與 (18) 看起來像同一句話,其實 (17) 是定義、(18) 是定義的**推論**(唯一性)。要讓學生說出差別。

### 變化 · Lay 2.9 Exercises 7–8
(7) Let $\mathbf{b}_1 = \begin{bmatrix} 3 \\ 0 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} -1 \\ 2 \end{bmatrix}$, $\mathbf{w} = \begin{bmatrix} 7 \\ -2 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$, and $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2\}$. Use the figure to estimate $[\,\mathbf{w}\,]_{\mathcal{B}}$ and $[\,\mathbf{x}\,]_{\mathcal{B}}$. Confirm your estimate of $[\,\mathbf{x}\,]_{\mathcal{B}}$ by using it and $\{\mathbf{b}_1, \mathbf{b}_2\}$ to compute $\mathbf{x}$.

![由 b1 = (3,0)、b2 = (-1,2) 畫出的座標格線,上面標出 w 與 x](coord-ex7.svg)

(8) Let $\mathbf{b}_1 = \begin{bmatrix} 0 \\ 2 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}$, $\mathbf{y} = \begin{bmatrix} 2 \\ 4 \end{bmatrix}$, $\mathbf{z} = \begin{bmatrix} -1 \\ -2.5 \end{bmatrix}$, and $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2\}$. Use the figure to estimate $[\,\mathbf{x}\,]_{\mathcal{B}}$, $[\,\mathbf{y}\,]_{\mathcal{B}}$, and $[\,\mathbf{z}\,]_{\mathcal{B}}$. Confirm your estimates of $[\,\mathbf{y}\,]_{\mathcal{B}}$ and $[\,\mathbf{z}\,]_{\mathcal{B}}$ by using them and $\{\mathbf{b}_1, \mathbf{b}_2\}$ to compute $\mathbf{y}$ and $\mathbf{z}$.

![由 b1 = (0,2)、b2 = (2,1) 畫出的座標格線,上面標出 x、y 與 z](coord-ex8.svg)

#### 解答
- (7) $[\,\mathbf{w}\,]_{\mathcal{B}} = \begin{bmatrix} 2 \\ -1 \end{bmatrix}$、$[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 1.5 \\ .5 \end{bmatrix}$。確認:$1.5\mathbf{b}_1 + 0.5\mathbf{b}_2 = \begin{bmatrix} 4.5 - 0.5 \\ 0 + 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$ ✓
- (8) $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 2 \\ -1 \end{bmatrix}$、$[\,\mathbf{y}\,]_{\mathcal{B}} = \begin{bmatrix} 1.5 \\ 1 \end{bmatrix}$、$[\,\mathbf{z}\,]_{\mathcal{B}} = \begin{bmatrix} -1 \\ -0.5 \end{bmatrix}$。確認:$1.5\mathbf{b}_1 + 1\mathbf{b}_2 = \begin{bmatrix} 0 + 2 \\ 3 + 1 \end{bmatrix} = \begin{bmatrix} 2 \\ 4 \end{bmatrix} = \mathbf{y}$ ✓;$-1\mathbf{b}_1 - 0.5\mathbf{b}_2 = \begin{bmatrix} 0 - 1 \\ -2 - 0.5 \end{bmatrix} = \begin{bmatrix} -1 \\ -2.5 \end{bmatrix} = \mathbf{z}$ ✓

#### 備註
(7) 書後給的正是 $\begin{bmatrix} 2 \\ -1 \end{bmatrix}$ 與 $\begin{bmatrix} 1.5 \\ .5 \end{bmatrix}$;(8) 書後無解答。

圖是本講義自繪的,數據與課本 p. 191 相同。**題目說「估計」,但這些數字剛好是整數或半整數,讀圖與代數解會完全一致**——正好讓學生確認自己讀圖沒讀錯。

(8) 的 $\mathbf{b}_1 = (0, 2)$ 第一分量是 0,所以純代數解時「第一列直接給出 $c_2$」;這一組數字設計得很好,可以用來對比「讀圖」與「代數」兩條路。

### 應用 · Lay 2.9 Exercises 37–38(T 電腦題)
(37) Let $H = \operatorname{Span}\{\mathbf{v}_1, \mathbf{v}_2\}$ and $\mathcal{B} = \{\mathbf{v}_1, \mathbf{v}_2\}$. Show that $\mathbf{x}$ is in $H$, and find the $\mathcal{B}$-coordinate vector of $\mathbf{x}$, when $\mathbf{v}_1 = \begin{bmatrix} 12 \\ -4 \\ 9 \\ 5 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 15 \\ -7 \\ 12 \\ 8 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 19 \\ -11 \\ 16 \\ 12 \end{bmatrix}$

(38) Let $H = \operatorname{Span}\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ and $\mathcal{B} = \{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$. Show that $\mathcal{B}$ is a basis for $H$ and $\mathbf{x}$ is in $H$, and find the $\mathcal{B}$-coordinate vector of $\mathbf{x}$, when $\mathbf{v}_1 = \begin{bmatrix} -5 \\ 4 \\ -3 \\ 2 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 7 \\ -5 \\ 3 \\ -3 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} -8 \\ 6 \\ -4 \\ 3 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} -7 \\ 8 \\ -9 \\ 1 \end{bmatrix}$

#### 解答
(37) 把 $[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{x}\,]$ 化為最簡列梯形:
$$\begin{bmatrix} 1 & 0 & -4/3 \\ 0 & 1 & 7/3 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$$
最後一行沒有樞軸 ⇒ 系統相容 ⇒ $\mathbf{x} \in H$,且 $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} -4/3 \\ 7/3 \end{bmatrix}$。

(38) $[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]$ 的 rank 為 3,三行都是樞軸行 ⇒ 線性獨立;又依定義張成 $H$,故 $\mathcal{B}$ 是 $H$ 的基底($\dim H = 3$)。再化 $[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3 \;\; \mathbf{x}\,]$:
$$\begin{bmatrix} 1 & 0 & 0 & 5 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 1 & 3 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
相容 ⇒ $\mathbf{x} \in H$,且 $[\,\mathbf{x}\,]_{\mathcal{B}} = \begin{bmatrix} 5 \\ 6 \\ 3 \end{bmatrix}$。

#### 備註
書後對 (37) 的說法是「Your calculations should show that the matrix $[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{x}\,]$ corresponds to a consistent system. The $\mathcal{B}$-coordinate vector of $\mathbf{x}$ is $(-4/3, 7/3)$.」;(38) 書後無解答。

兩題都標 T,放進實作課。它們是本節唯一「要先證明 $\mathbf{x} \in H$」的題型:**判斷相容性靠的是增廣矩陣的最後一行有沒有樞軸**(第 2 週的舊觀念)。

注意 (38) 多要求一件事:先證 $\mathcal{B}$ **是基底**(rank 3)。這一步不能跳——若 $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$ 相依,座標就不唯一,題目的答案也就沒有意義。

$\mathbf{x}$ 有 4 個分量,座標只有 2 或 3 個,正是「用較少的數字記住較長的向量」的具體例子。

## 驗算
```check
Matrix([[1, Rational(1,5)], [Rational(1,5), 1]]) * Matrix([3, 2]) == Matrix([Rational(17,5), Rational(13,5)])
Matrix([[1, 2], [1, -1]]) * Matrix([3, 2]) == Matrix([7, 1])
Matrix([[-2, 3], [1, 1]]) * Matrix([-1, 3]) == Matrix([11, 2])
Matrix([[1, -2], [-4, 7]]).solve(Matrix([-3, 7])) == Matrix([7, 5])
Matrix([[1, -4], [-3, 7]]).solve(Matrix([-8, 9])) == Matrix([4, 3])
Matrix([[1, -3], [5, -7], [-3, 5]]) * Matrix([Rational(1,4), Rational(-5,4)]) == Matrix([4, 10, -7])
Matrix([[-2, -6], [1, 7], [2, 8]]) * Matrix([Rational(-7,2), Rational(1,2)]) == Matrix([4, 0, -3])
(lambda p: p.solve(Matrix([7, -2])) == Matrix([2, -1]) and p.solve(Matrix([4, 1])) == Matrix([Rational(3,2), Rational(1,2)]))(Matrix([[3, -1], [0, 2]]))
(lambda p: (p.solve(Matrix([-2, 3])), p.solve(Matrix([2, 4])), p.solve(Matrix([-1, Rational(-5,2)]))) == (Matrix([2, -1]), Matrix([Rational(3,2), 1]), Matrix([-1, Rational(-1,2)])))(Matrix([[0, 2], [2, 1]]))
Rational(-4,3) * Matrix([12, -4, 9, 5]) + Rational(7,3) * Matrix([15, -7, 12, 8]) == Matrix([19, -11, 16, 12])
Matrix([[12, 15], [-4, -7], [9, 12], [5, 8]]).rank() == 2
5 * Matrix([-5, 4, -3, 2]) + 6 * Matrix([7, -5, 3, -3]) + 3 * Matrix([-8, 6, -4, 3]) == Matrix([-7, 8, -9, 1])
Matrix([[-5, 7, -8], [4, -5, 6], [-3, 3, -4], [2, -3, 3]]).rank() == 3
Matrix([[1, Rational(1,5)], [Rational(1,5), 1]]).det() != 0
```
