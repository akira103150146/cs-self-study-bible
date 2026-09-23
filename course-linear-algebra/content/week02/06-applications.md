---
title_en: Linear Combinations in Applications
title_zh: 線性組合的應用:成本、產量、污染、質心
sub: Quantity times per-unit vector, summed up
level: mid
source: Lay 1.3
supplement: true
lab_hook: "Lab ④ 應用:礦場產量與電廠燃煤(Lay 1.3 Exercises 35–36,用 `rref()` 解)"
---
## 觀念
Scalar multiples and linear combinations arise when a quantity such as "cost" is broken down into several categories. The basic principle for the example concerns the cost of producing several units of an item when the cost per unit is known:

$$\{\text{number of units}\} \cdot \{\text{cost per unit}\} = \{\text{total cost}\}$$

When each unit has a whole *list* of costs (materials, labor, overhead), the "cost per unit" is a **vector**, and the total cost is a **scalar multiple** of that vector. When several products are made, the total cost is a **linear combination** of the per-unit vectors, with the numbers of units as the weights.

Asking "how many units of each product give this total?" is then a vector equation $x_1\mathbf{v}_1 + \cdots + x_p\mathbf{v}_p = \mathbf{b}$ — a linear system.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| cost per dollar of income | 每一元營收的成本 | Example 7 的向量:做 1 元產品要花多少材料、人工、管理費 |
| materials / labor / overhead | 材料 / 人工 / 管理費 | 成本向量的三個分量 |
| output per day | 每日產量 | Exercise 35 的向量:一天挖出多少銅、多少銀 |
| metric ton | 公噸 | 1000 公斤 |
| Btu (British thermal unit) | 英熱單位 | 熱量單位 |
| sulfur dioxide | 二氧化硫 | 燃煤產生的污染物 |
| particulate matter | 懸浮微粒 | 固體顆粒污染物 |
| point mass | 質點 | 把物體看成集中在一點的質量 |
| center of mass / center of gravity | 質心 / 重心 | 各點位置以質量為權重的加權平均 |
| alpha blending | Alpha 混色 | 電腦繪圖把兩個顏色依比例混合(補充) |

## 白話說
只要題目長這樣,就是線性組合:

> **每一份**會產生一整串數字(一個向量),做了**好幾份**,把全部加起來。

- 每 1 元產品 B 要花 (材料, 人工, 管理費) = $(.45, .25, .15)$;做 100 元就是 $100\mathbf{b}$。
- 礦場 1 每天挖出 (銅, 銀) = $(20, 550)$;挖 $x_1$ 天就是 $x_1\mathbf{v}_1$。
- 兩種產品、兩座礦場 → 把兩個向量各自乘上份數再相加。

反過來問「要做幾份才能剛好得到這個總量?」就是解向量方程式——也就是這週一直在做的事。

## 幾何意義
以 Exercise 35 為例,向量 $\mathbf{v}_1 = (20, 550)$、$\mathbf{v}_2 = (30, 500)$ 是平面上兩個不平行的箭頭。任何 (銅, 銀) 的目標都在 $\operatorname{Span}\{\mathbf{v}_1, \mathbf{v}_2\} = \mathbb{R}^2$ 裡,所以權重(天數)一定解得出來。

但現實有額外限制:天數**不能是負的**。所以真正做得到的目標只是 $x_1, x_2 \ge 0$ 的那一塊——夾在兩個箭頭之間的扇形區域。這種「權重非負」的組合叫**錐組合**(conic combination),是線性規劃(Lay 第 9 章)的起點。

質心公式 $\bar{\mathbf{v}} = \frac{m_1}{m}\mathbf{v}_1 + \cdots + \frac{m_k}{m}\mathbf{v}_k$ 的權重非負而且加起來是 1,這種組合叫**凸組合**,結果一定落在這些點圍成的形狀裡面(Exercise 39 的質心落在三角形內)。

## 在資工哪裡用
- **Alpha 混色**:畫面上半透明的視窗、遊戲裡的淡入淡出,每個像素的顏色都是 $\alpha\,\text{前景} + (1 - \alpha)\,\text{背景}$,兩個 RGB 向量的線性組合(例 2)。$\alpha$ 是前景的**不透明度**,和 RGBA 的 A、CSS 的 `opacity` 是同一個東西:$\alpha = 1$ 完全蓋住背景、$\alpha = 0$ 完全透明。
- **動畫內插**:角色從位置 $\mathbf{p}$ 移到 $\mathbf{q}$,中間每一格是 $(1 - t)\mathbf{p} + t\mathbf{q}$。
- **資源規劃**:雲端服務每台 A 型主機提供 (CPU, 記憶體, 頻寬) = 某個向量,B 型主機是另一個向量;要湊出需求量,就是解向量方程式。
- **遊戲物理**:剛體的重心就是各部件位置以質量為權重的組合(Exercises 37–39)。

## 實際應用
- 會計與成本分析:Example 7 的「成本向量」就是製造業的單位成本表。
- 環保:Exercise 36 的電廠排放,每噸煤產生 (熱量, SO₂, 微粒) 一個向量,環保單位可以從總排放量反推燒了多少煤。
- 工程:橋樑、飛機設計都要算重心;Exercise 39 的三角板就是最小的例子。

## 原理
全部都建立在兩條觀念上:

1. **比例關係 → 純量倍數**:每單位產生 $\mathbf{v}$,做 $x$ 單位就產生 $x\mathbf{v}$(每個分量都乘 $x$)。
2. **可以相加 → 向量加法**:兩種來源的總量是各自的總量相加。

所以總量 $= x_1\mathbf{v}_1 + x_2\mathbf{v}_2 + \cdots$,正是線性組合。

**什麼時候不能用?** 如果「每單位的成本」會隨數量改變(例如大量採購打折、工廠產能滿了要加班費),比例關係不成立,就不再是線性模型。課本的例子都假設比例固定。

## 老師講解
### 例 1 · Lay 1.3 Example 7
A company manufactures two products. For \$1.00 worth of product B, the company spends \$.45 on materials, \$.25 on labor, and \$.15 on overhead. For \$1.00 worth of product C, the company spends \$.40 on materials, \$.30 on labor, and \$.15 on overhead. Let

$$\mathbf{b} = \begin{bmatrix} .45 \\ .25 \\ .15 \end{bmatrix} \quad \text{and} \quad \mathbf{c} = \begin{bmatrix} .40 \\ .30 \\ .15 \end{bmatrix}.$$

Then $\mathbf{b}$ and $\mathbf{c}$ represent the "costs per dollar of income" for the two products.

- **a.** What economic interpretation can be given to the vector $100\mathbf{b}$?
- **b.** Suppose the company wishes to manufacture $x_1$ dollars worth of product B and $x_2$ dollars worth of product C. Give a vector that describes the various costs the company will have (for materials, labor, and overhead).

1. **先讀懂向量的三個分量**:$\mathbf{b}$ 的第 1、2、3 個分量分別是材料、人工、管理費。$\mathbf{b}$ 的意思是「做出 1 元的產品 B,三種成本各花多少」。
2. **(a) 計算純量倍數**:每個分量都乘 100,
   $$100\mathbf{b} = 100\begin{bmatrix} .45 \\ .25 \\ .15 \end{bmatrix} = \begin{bmatrix} 45 \\ 25 \\ 15 \end{bmatrix}.$$
3. **(a) 解讀**:做出 \$100 的產品 B,要花 \$45 材料、\$25 人工、\$15 管理費。
4. **(b) 各自算**:做 $x_1$ 元的 B,成本是 $x_1\mathbf{b}$;做 $x_2$ 元的 C,成本是 $x_2\mathbf{c}$。
5. **(b) 相加**:總成本向量是
   $$x_1\mathbf{b} + x_2\mathbf{c} = \begin{bmatrix} .45x_1 + .40x_2 \\ .25x_1 + .30x_2 \\ .15x_1 + .15x_2 \end{bmatrix}.$$
   第一個分量是總材料費,第二個是總人工費,第三個是總管理費。
6. **反問一題**:如果已知總成本是 $(\text{材料}, \text{人工}, \text{管理費}) = (85, 55, 30)$,兩種產品各做了多少?這就是向量方程式 $x_1\mathbf{b} + x_2\mathbf{c} = (85, 55, 30)$,列化簡得 $x_1 = 100$、$x_2 = 100$。

#### 備註
第 6 步不是課本的內容,是補上的「反問」,讓學生看到應用題的兩個方向:已知份數求總量(乘法)、已知總量求份數(解方程組)。

### 例 2 · 補充:Alpha 混色
In computer graphics a color is a vector $(R, G, B)$ with entries from 0 to 255. Drawing a semi-transparent foreground color $\mathbf{f}$ over a background color $\mathbf{g}$ gives the pixel color $\alpha\mathbf{f} + (1 - \alpha)\mathbf{g}$, where $\alpha$ is the **opacity** of the foreground, $0 \le \alpha \le 1$. Let $\mathbf{f} = (255, 0, 0)$ (red) and $\mathbf{g} = (0, 0, 255)$ (blue).

- **a.** Compute the pixel color when $\alpha = 0.25$.
- **b.** Which $\alpha$ gives the color $(102, 0, 153)$?
- **c.** Can the color $(100, 100, 100)$ (gray) be obtained as a linear combination of $\mathbf{f}$ and $\mathbf{g}$?

1. **(a) 代入權重**:$\alpha = 0.25$ 代表前景只有四分之一的不透明度,權重是 $0.25$(前景)和 $0.75$(背景),
   $$0.25\begin{bmatrix} 255 \\ 0 \\ 0 \end{bmatrix} + 0.75\begin{bmatrix} 0 \\ 0 \\ 255 \end{bmatrix} = \begin{bmatrix} 63.75 \\ 0 \\ 191.25 \end{bmatrix}.$$
   偏藍的紫色(螢幕實際顯示時會四捨五入成整數)。$\alpha$ 越大,前景的紅色越強。
2. **(b) 列出向量方程式**:$\alpha(255, 0, 0) + (1 - \alpha)(0, 0, 255) = (102, 0, 153)$。
3. **(b) 逐分量解**:R 分量 $255\alpha = 102$,得 $\alpha = 0.4$;B 分量 $255(1 - \alpha) = 153$,也得 $\alpha = 0.4$;G 分量 $0 = 0$ 自動成立。三個分量一致,所以 $\alpha = 0.4$。
4. **(c) 問的是 Span**:$\mathbf{f}$ 和 $\mathbf{g}$ 的 G 分量都是 0,所以任何組合 $x_1\mathbf{f} + x_2\mathbf{g}$ 的 G 分量都是 0。灰色的 G 分量是 100,**不在** $\operatorname{Span}\{\mathbf{f}, \mathbf{g}\}$ 裡。
5. **用列化簡確認**:$\left[\begin{array}{rr|r} 255 & 0 & 100 \\ 0 & 0 & 100 \\ 0 & 255 & 100 \end{array}\right]$ 的第二列是 $0 = 100$,無解。
6. **結論**:只用紅、藍兩種光,永遠混不出含綠色的顏色。這就是螢幕需要**三種**子像素的原因——三個不共面的向量才能生成 ℝ³。

#### 備註
這題把本週的「Span」和學生天天看的螢幕連起來。可以請學生打開任何一個繪圖軟體的調色盤,調 RGB 滑桿驗證。

## 易錯點
- 把單位混在一起:Exercise 35 的銅用「公噸」、銀用「公斤」,向量的每個分量要各自保持同一個單位,不能換算後相加。
- 列方程式時把向量擺成列(橫的),結果係數矩陣轉置了。**每一種來源的向量要當成一行**。
- 解出負的天數、負的噸數還照樣寫答案。應用題解完要檢查是否合理(Exercise 36 的答案是正的,合理)。
- 質心公式忘了除以總質量 $m$。

## 教學提示
這個觀念是補充,**不在節奏表裡**。時間夠的話,例 1 花 10 分鐘、例 2 花 5 分鐘;否則留作自學。

Exercises 35–36 的 (c) 標 T,留給實作課 ④ 用 `rref()` 做;課堂只要求 (a)(b) 列出向量方程式。Exercise 39 的 (b) 有點難,適合當加分題。

## 練習
### 照做 · Lay 1.3 Exercise 35
A mining company has two mines. One day's operation at mine 1 produces ore that contains 20 metric tons of copper and 550 kilograms of silver, while one day's operation at mine 2 produces ore that contains 30 metric tons of copper and 500 kilograms of silver. Let $\mathbf{v}_1 = \begin{bmatrix} 20 \\ 550 \end{bmatrix}$ and $\mathbf{v}_2 = \begin{bmatrix} 30 \\ 500 \end{bmatrix}$. Then $\mathbf{v}_1$ and $\mathbf{v}_2$ represent the "output per day" of mine 1 and mine 2, respectively.

- **a.** What physical interpretation can be given to the vector $5\mathbf{v}_1$?
- **b.** Suppose the company operates mine 1 for $x_1$ days and mine 2 for $x_2$ days. Write a vector equation whose solution gives the number of days each mine should operate in order to produce 150 tons of copper and 2825 kilograms of silver. Do not solve the equation.
- **c.** **[T]** Solve the equation in (b).

#### 解答
(a) $5\mathbf{v}_1 = \begin{bmatrix} 100 \\ 2750 \end{bmatrix}$:礦場 1 運作 5 天,產出 100 公噸銅和 2750 公斤銀(書後解答相同)。

(b) $x_1\begin{bmatrix} 20 \\ 550 \end{bmatrix} + x_2\begin{bmatrix} 30 \\ 500 \end{bmatrix} = \begin{bmatrix} 150 \\ 2825 \end{bmatrix}$。

(c) 化簡 $\left[\begin{array}{rr|r} 20 & 30 & 150 \\ 550 & 500 & 2825 \end{array}\right]$ 得 $x_1 = 1.5$、$x_2 = 4$:礦場 1 運作 1.5 天、礦場 2 運作 4 天(書後解答相同)。驗算:$1.5 \cdot 20 + 4 \cdot 30 = 150$ ✓,$1.5 \cdot 550 + 4 \cdot 500 = 2825$ ✓。

### 照做 · Lay 1.3 Exercise 37
Let $\mathbf{v}_1, \dots, \mathbf{v}_k$ be points in $\mathbb{R}^3$ and suppose that for $j = 1, \dots, k$ an object with mass $m_j$ is located at point $\mathbf{v}_j$. Physicists call such objects *point masses*. The total mass of the system of point masses is $m = m_1 + \cdots + m_k$. The *center of mass* (or *center of gravity*) of the system is

$$\bar{\mathbf{v}} = \frac{1}{m}\left[m_1\mathbf{v}_1 + \cdots + m_k\mathbf{v}_k\right].$$

Compute the center of gravity of the system consisting of the following point masses:

| Point | Mass |
|---|---|
| $\mathbf{v}_1 = (5, -4, 3)$ | 2 g |
| $\mathbf{v}_2 = (4, 3, -2)$ | 5 g |
| $\mathbf{v}_3 = (-4, -3, -1)$ | 2 g |
| $\mathbf{v}_4 = (-9, 8, 6)$ | 1 g |

#### 解答
總質量 $m = 2 + 5 + 2 + 1 = 10$。

$2\mathbf{v}_1 = (10, -8, 6)$,$5\mathbf{v}_2 = (20, 15, -10)$,$2\mathbf{v}_3 = (-8, -6, -2)$,$1\mathbf{v}_4 = (-9, 8, 6)$,相加得 $(13, 9, 0)$。

$\bar{\mathbf{v}} = \frac{1}{10}(13, 9, 0) = (1.3,\ 0.9,\ 0)$(書後解答相同)。

#### 備註
課本這題附了一張立體圖標出四個質點的位置,講義沒有重畫——表格已經把座標寫全,不影響作答。

### 變化 · Lay 1.3 Exercise 36
A steam plant burns two types of coal: anthracite (A) and bituminous (B). For each ton of A burned, the plant produces 27.6 million Btu of heat, 3100 grams (g) of sulfur dioxide, and 250 g of particulate matter (solid-particle pollutants). For each ton of B burned, the plant produces 30.2 million Btu, 6400 g of sulfur dioxide, and 360 g of particulate matter.

- **a.** How much heat does the steam plant produce when it burns $x_1$ tons of A and $x_2$ tons of B?
- **b.** Suppose the output of the steam plant is described by a vector that lists the amounts of heat, sulfur dioxide, and particulate matter. Express this output as a linear combination of two vectors, assuming that the plant burns $x_1$ tons of A and $x_2$ tons of B.
- **c.** **[T]** Over a certain time period, the steam plant produced 162 million Btu of heat, 23,610 g of sulfur dioxide, and 1623 g of particulate matter. Determine how many tons of each type of coal the steam plant must have burned. Include a vector equation as part of your solution.

#### 解答
(a) $27.6x_1 + 30.2x_2$ 百萬 Btu。

(b) $x_1\begin{bmatrix} 27.6 \\ 3100 \\ 250 \end{bmatrix} + x_2\begin{bmatrix} 30.2 \\ 6400 \\ 360 \end{bmatrix}$(分量依序是熱量、SO₂、微粒)。

(c) 向量方程式 $x_1\begin{bmatrix} 27.6 \\ 3100 \\ 250 \end{bmatrix} + x_2\begin{bmatrix} 30.2 \\ 6400 \\ 360 \end{bmatrix} = \begin{bmatrix} 162 \\ 23610 \\ 1623 \end{bmatrix}$。化簡得 $x_1 = 3.9$、$x_2 = 1.8$:燒了 3.9 噸無煙煤、1.8 噸煙煤。

驗算三個分量:$27.6(3.9) + 30.2(1.8) = 107.64 + 54.36 = 162$ ✓;$3100(3.9) + 6400(1.8) = 12090 + 11520 = 23610$ ✓;$250(3.9) + 360(1.8) = 975 + 648 = 1623$ ✓。

#### 備註
三個方程式、兩個未知數,本來可能無解;這題剛好相容(第三個分量是「多出來的檢查」)。可以問學生:如果量測到的微粒是 1700 g,會發生什麼事?(無解,代表量測有誤差——這就是第 14 週(Lay 第 6 章)最小平方法要處理的情況。)

### 變化 · Lay 1.3 Exercise 38
Let $\mathbf{v}$ be the center of mass of a system of point masses located at $\mathbf{v}_1, \dots, \mathbf{v}_k$ as in Exercise 37. Is $\mathbf{v}$ in $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_k\}$? Explain.

#### 解答
**是。** 把質心公式拆開:
$$\mathbf{v} = \frac{m_1}{m}\mathbf{v}_1 + \frac{m_2}{m}\mathbf{v}_2 + \cdots + \frac{m_k}{m}\mathbf{v}_k,$$
這是 $\mathbf{v}_1, \dots, \mathbf{v}_k$ 的線性組合,權重是 $m_j / m$。依 Span 的定義,$\mathbf{v}$ 在 $\operatorname{Span}\{\mathbf{v}_1, \dots, \mathbf{v}_k\}$ 裡。

### 應用 · Lay 1.3 Exercise 39
A thin triangular plate of uniform density and thickness has vertices at $\mathbf{v}_1 = (0, 1)$, $\mathbf{v}_2 = (8, 1)$, and $\mathbf{v}_3 = (2, 4)$, as in the figure below, and the mass of the plate is 3 g.

![三角板的三個頂點 v1 = (0, 1)、v2 = (8, 1)、v3 = (2, 4)。](ex39-plate.svg)

- **a.** Find the $(x, y)$-coordinates of the center of mass of the plate. This "balance point" of the plate coincides with the center of mass of a system consisting of three 1-gram point masses located at the vertices of the plate.
- **b.** Determine how to distribute an additional mass of 6 g at the three vertices of the plate to move the balance point of the plate to $(2, 2)$. [*Hint:* Let $w_1$, $w_2$, and $w_3$ denote the masses added at the three vertices, so that $w_1 + w_2 + w_3 = 6$.]

#### 解答
(a) 三個 1 克質點,總質量 3:
$$\bar{\mathbf{v}} = \frac{1}{3}\left[(0, 1) + (8, 1) + (2, 4)\right] = \frac{1}{3}(10, 6) = \left(\tfrac{10}{3},\ 2\right)$$
(書後解答相同)。

(b) 加上重量後,三個頂點的質量是 $1 + w_1$、$1 + w_2$、$1 + w_3$,總質量 $3 + 6 = 9$。要求
$$\frac{1}{9}\left[(1 + w_1)(0, 1) + (1 + w_2)(8, 1) + (1 + w_3)(2, 4)\right] = (2, 2).$$
兩邊乘 9 並展開,連同 $w_1 + w_2 + w_3 = 6$,得到
$$\begin{aligned} 8w_2 + 2w_3 &= 8 \\ w_1 + w_2 + 4w_3 &= 12 \\ w_1 + w_2 + w_3 &= 6 \end{aligned}$$
第 2 式減第 3 式得 $3w_3 = 6$,$w_3 = 2$;代入第 1 式得 $w_2 = 0.5$;再得 $w_1 = 3.5$。

所以在 $\mathbf{v}_1$ 加 3.5 g、$\mathbf{v}_2$ 加 0.5 g、$\mathbf{v}_3$ 加 2 g。三個都非負,做得到。

#### 備註
(b) 適合當加分題。關鍵是想到「平板 = 三個 1 克質點」之後,加重量就只是改變權重。

## 驗算
```check
100 * Matrix([Rational(45, 100), Rational(25, 100), Rational(15, 100)]) == Matrix([45, 25, 15])
Matrix([[Rational(45, 100), Rational(40, 100), 85], [Rational(25, 100), Rational(30, 100), 55], [Rational(15, 100), Rational(15, 100), 30]]).rref()[0] == Matrix([[1, 0, 100], [0, 1, 100], [0, 0, 0]])
Rational(1, 4) * Matrix([255, 0, 0]) + Rational(3, 4) * Matrix([0, 0, 255]) == Matrix([Rational(255, 4), 0, Rational(765, 4)])
Rational(2, 5) * Matrix([255, 0, 0]) + Rational(3, 5) * Matrix([0, 0, 255]) == Matrix([102, 0, 153])
2 in Matrix([[255, 0, 100], [0, 0, 100], [0, 255, 100]]).rref()[1]
Matrix([[20, 30, 150], [550, 500, 2825]]).rref()[0] == Matrix([[1, 0, Rational(3, 2)], [0, 1, 4]])
(2 * Matrix([5, -4, 3]) + 5 * Matrix([4, 3, -2]) + 2 * Matrix([-4, -3, -1]) + Matrix([-9, 8, 6])) / 10 == Matrix([Rational(13, 10), Rational(9, 10), 0])
Matrix([[Rational(276, 10), Rational(302, 10), 162], [3100, 6400, 23610], [250, 360, 1623]]).rref()[0] == Matrix([[1, 0, Rational(39, 10)], [0, 1, Rational(9, 5)], [0, 0, 0]])
(Matrix([0, 1]) + Matrix([8, 1]) + Matrix([2, 4])) / 3 == Matrix([Rational(10, 3), 2])
Matrix([[0, 8, 2, 8], [1, 1, 4, 12], [1, 1, 1, 6]]).rref()[0] == Matrix([[1, 0, 0, Rational(7, 2)], [0, 1, 0, Rational(1, 2)], [0, 0, 1, 2]])
(Rational(9, 2) * Matrix([0, 1]) + Rational(3, 2) * Matrix([8, 1]) + 3 * Matrix([2, 4])) / 9 == Matrix([2, 2])
```
