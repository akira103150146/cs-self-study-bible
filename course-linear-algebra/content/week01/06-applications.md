---
title_en: Applications of Linear Systems
title_zh: 線性方程組的應用:經濟、化學、網路流、熱傳導、內插
sub: Balances and conservation laws turn into linear equations
level: mid
source: Lay 1.6、1.1、1.2
supplement: true
lab_hook: "Lab ④ 應用:內插多項式(Lay 1.2 Exercises 45–46)、化學配平(Lay 1.6 Exercises 9–10)"
---
## 觀念
Many applied problems lead to linear systems because something **balances** or is **conserved**. Several of them lead to systems with many solutions.

- **A homogeneous system in economics (Leontief exchange model).** Suppose a nation's economy is divided into sectors, and we know how each sector's total output is divided, or "exchanged," among the sectors. Let the total dollar value of a sector's output be called the **price** of that output. Leontief proved that *there exist equilibrium prices that can be assigned to the total outputs of the various sectors in such a way that the income of each sector exactly balances its expenses.*
- **Balancing chemical equations.** Atoms are neither destroyed nor created in a reaction, so for each element the number of atoms on the left must equal the number on the right. Each element gives one linear equation.
- **Network flow.** A *network* consists of *junctions* (or *nodes*) connected by *branches*. The total flow into the network equals the total flow out of the network, and the total flow into a junction equals the total flow out of the junction. Each junction gives one linear equation.
- **Steady-state heat flow.** On a mesh, the temperature at an interior node is approximately equal to the average of the temperatures at the four nearest nodes.
- **Interpolating polynomials.** A polynomial whose graph passes through every given data point can be found by solving a linear system for its coefficients.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| sector | 部門 | 經濟體的一個產業,例如煤、電力、鋼鐵 |
| output / price | 產出 / 價格 | 課本把「一個部門全年產出的總值」叫做它的價格 |
| exchange table | 交換表 | 每一行寫一個部門的產出怎麼分給各部門;每一行加起來是 1 |
| equilibrium prices | 均衡價格 | 讓每個部門「收入 = 支出」的一組價格 |
| homogeneous system | 齊次方程組 | 右邊全是 0 的方程組;一定有 $0$ 這個解 |
| balance a chemical equation | 化學方程式配平 | 找整數係數讓每種原子左右數量相同 |
| network | 網路 | 由節點和分支組成 |
| junction / node | 節點 | 分支交會的地方 |
| branch | 分支 | 連接節點的線,有方向與流量 |
| flow conservation | 流量守恆 | 流進 = 流出 |
| steady-state temperature | 穩態溫度 | 溫度不再隨時間變化時的分布 |
| mesh | 網格 | 把區域切成格子點 |
| interpolating polynomial | 內插多項式 | 圖形剛好通過每一個資料點的多項式 |

## 白話說
這一個觀念只有一個重點:**「平衡」或「守恆」會變成線性方程式**。

- 經濟:每個部門「賺進來的錢 = 花出去的錢」。
- 化學反應:反應前的碳原子 = 反應後的碳原子,氫、氧也一樣。
- 路口:流進來的車 = 流出去的車。
- 熱平衡:每個點的溫度 = 上下左右四個點的平均。
- 內插:曲線通過某個點,就等於「把這個點代進去成立」。

把每一條「平衡」寫下來,就得到一組線性方程式;接下來就是觀念 2–5 的工作:列化簡、找 pivot、寫一般解。**應用題最難的部分通常不是解,而是把方程式列出來。**

課本特別強調:這些應用常常**有無限多解**(有自由變數)。這不是壞事——經濟學只在乎價格的**比例**,化學只要**最小的整數**係數,網路流則要再配上「流量不能是負的」這種現實限制。

## 幾何意義
網路流 Example 2 有一個自由變數 $x_5$,所以解集是一條「線」;但單行道的流量不能是負的,這些**不等式**把線截成一段**線段**。這是第一次看到「方程式 + 不等式」的問題,到了最佳化(線性規劃)會成為主角。

經濟模型的解集也是一條通過原點的線:把一組均衡價格全部乘以 2,還是均衡價格。所以真正有意義的是「方向」(價格比例),不是長度。

內插的幾何很直觀:兩個點決定一條直線(一次多項式),三個點決定一條拋物線(二次多項式)。$k$ 個 $x$ 座標不同的點,剛好決定一個次數不超過 $k-1$ 的多項式——「不超過」是因為三個點如果剛好共線,得到的就是一條直線($t^2$ 的係數是 0)。

## 在資工哪裡用
- **經濟交換表**:「每一行加起來是 1、表示東西怎麼分出去」的矩陣,和第 12 週 Google **PageRank** 用的矩陣是同一種結構——網頁把自己的重要性「分給」它連出去的網頁,均衡時每個網頁的重要性就是它的排名。
- **網路流**:電腦網路的頻寬分配、路由,跟街道車流是同一個模型;「最大流量」問題是演算法課的經典題目。
- **熱傳導**:「每個點等於周圍的平均」和影像處理裡的**模糊(blur)**、**補洞(inpainting)**是同一件事——照片缺了一塊,就用周圍像素的平均把它補起來。
- **內插**:動畫的關鍵影格、字型的曲線、遊戲裡的平滑移動,都要一條曲線剛好通過指定的點。
- **化學配平**:大型係數(Exercise 10 的係數到 374)要用**精確分數**運算,這是符號運算(SymPy)和浮點運算(NumPy)的差別。

## 實際應用
**一台電腦跑了 56 小時。** 1949 年,Leontief 把美國經濟分成 500 個部門,每個部門一條方程式,得到 500 個方程式、500 個未知數的方程組。當時哈佛的 Mark II 電腦解不動這麼大的方程組,他只好把問題濃縮成 42 個方程式、42 個未知數;光是替 Mark II 寫程式就花了好幾個月,機器還是跑了 56 小時才算出答案。他後來因此獲得 1973 年諾貝爾經濟學獎(課本第 1 章開頭)。今天一台筆電用 `np.linalg.solve` 解 500 × 500 的方程組不用一秒——實作課會量給你看,計算量怎麼隨 $n$ 長大。

課本 2.6 有完整的 Leontief 投入產出模型,1.10 還有營養配方、電路等應用;本課不在課堂上教,有興趣可以自己讀。

## 原理
**為什麼經濟模型一定有無限多解?** 方程組是**齊次**的(右邊全是 0),而交換表每一行加起來是 1,代表「把所有方程式加起來」會得到 $0 = 0$——有一條方程式是多餘的,所以一定有自由變數。

**為什麼化學配平一定有無限多解?** 配平方程組也是齊次的,而且只要 $(x_1, \dots, x_n)$ 是解,乘上任何倍數也是解。化學家要的是「最小的正整數解」,所以把自由變數取成讓所有係數都變整數的最小值。

**為什麼網路流方程式一定是線性的?** 每個節點「流進 = 流出」,流量只是加加減減,沒有相乘。負的流量代表實際方向和圖上相反;單行道不允許反向,所以得到 $x_i \ge 0$ 的限制。

**為什麼內插多項式唯一?** $x$ 座標互不相同時,係數矩陣(Vandermonde 矩陣)的每一行都是 pivot 行,所以解唯一。第 8 週學行列式時可以再證明一次。

## 老師講解
### 例 1 · Lay 1.6 Example 1
Suppose an economy consists of the Coal, Electric (power), and Steel sectors, and the output of each sector is distributed among the various sectors as shown in the table, where the entries in a column represent the fractional parts of a sector's total output.

| Coal | Electric | Steel | Purchased by |
|---|---|---|---|
| .0 | .4 | .6 | Coal |
| .6 | .1 | .2 | Electric |
| .4 | .5 | .2 | Steel |

Denote the prices (in dollar values) of the total annual outputs of the Coal, Electric, and Steel sectors by $p_C$, $p_E$, and $p_S$, respectively. If possible, find equilibrium prices that make each sector's income match its expenditures.

1. **讀表的方法**:一個部門**往下看一行**,是自己的產出分到哪裡去;**往右看一列**,是自己要買進什麼。例如第二行說:Electric 的產出 40% 給 Coal、10% 自己用、50% 給 Steel。每一行加起來都是 1,因為產出全部都要分出去。
2. **Coal 的收入 = 支出**:看第一列,Coal 買了 Electric 產出的 40%、Steel 產出的 60%,所以支出是 $.4p_E + .6p_S$;收入就是自己產出的總值 $p_C$。所以 $p_C = .4p_E + .6p_S$。
3. **Electric、Steel 同理**(看第二、三列):$p_E = .6p_C + .1p_E + .2p_S$、$p_S = .4p_C + .5p_E + .2p_S$。
4. **把未知數全部移到左邊**(例如 $p_E - .1p_E = .9p_E$):
   $$\begin{aligned} p_C - .4p_E - .6p_S &= 0 \\ -.6p_C + .9p_E - .2p_S &= 0 \\ -.4p_C - .5p_E + .8p_S &= 0 \end{aligned}$$
   右邊全是 0,這是一個**齊次**方程組。
5. **列化簡**(課本把小數四捨五入到兩位):$R_2 \leftarrow R_2 + .6R_1$、$R_3 \leftarrow R_3 + .4R_1$,第 2、3 列變成 $[\,0 \;\; .66 \;\; {-.56} \mid 0\,]$ 與 $[\,0 \;\; {-.66} \;\; .56 \mid 0\,]$;再 $R_3 \leftarrow R_3 + R_2$ 得到全 0 列。
   $$\left[\begin{array}{rrr|r} 1 & -.4 & -.6 & 0 \\ 0 & .66 & -.56 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & -.4 & -.6 & 0 \\ 0 & 1 & -.85 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 0 & -.94 & 0 \\ 0 & 1 & -.85 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right]$$
6. **一般解**:$p_S$ 是自由變數,$p_C = .94p_S$、$p_E = .85p_S$。(精確值是 $p_C = \tfrac{31}{33}p_S$、$p_E = \tfrac{28}{33}p_S$。)
7. **解讀**:任何非負的 $p_S$ 都給出一組均衡價格。例如 $p_S = 100$(百萬美元),則 $p_C = 94$、$p_E = 85$:煤產值 9400 萬、電力 8500 萬、鋼鐵 1 億時,每個部門的收支剛好平衡。**只有比例有意義**。

### 例 2 · Lay 1.6(p. 79–80)
When propane gas burns, the propane ($\mathrm{C_3H_8}$) combines with oxygen ($\mathrm{O_2}$) to form carbon dioxide ($\mathrm{CO_2}$) and water ($\mathrm{H_2O}$):

$$(x_1)\,\mathrm{C_3H_8} + (x_2)\,\mathrm{O_2} \rightarrow (x_3)\,\mathrm{CO_2} + (x_4)\,\mathrm{H_2O}$$

Balance the equation.

1. **每一種原子寫一條「左邊 = 右邊」**。先數每個分子裡有幾個原子:$\mathrm{C_3H_8}$ 有 3 個 C、8 個 H;$\mathrm{O_2}$ 有 2 個 O;$\mathrm{CO_2}$ 有 1 個 C、2 個 O;$\mathrm{H_2O}$ 有 2 個 H、1 個 O。
2. 碳:$3x_1 = x_3$;氫:$8x_1 = 2x_4$;氧:$2x_2 = 2x_3 + x_4$。
3. **全部移到左邊**(右邊變 0):$3x_1 - x_3 = 0$、$8x_1 - 2x_4 = 0$、$2x_2 - 2x_3 - x_4 = 0$。
4. **增廣矩陣化簡**:
   $$\left[\begin{array}{rrrr|r} 3 & 0 & -1 & 0 & 0 \\ 8 & 0 & 0 & -2 & 0 \\ 0 & 2 & -2 & -1 & 0 \end{array}\right] \sim \left[\begin{array}{rrrr|r} 1 & 0 & 0 & -\tfrac14 & 0 \\ 0 & 1 & 0 & -\tfrac54 & 0 \\ 0 & 0 & 1 & -\tfrac34 & 0 \end{array}\right]$$
5. **一般解**:$x_1 = \tfrac14 x_4$、$x_2 = \tfrac54 x_4$、$x_3 = \tfrac34 x_4$,$x_4$ is free。
6. **化學係數要是整數**:取讓所有分母消失的最小值 $x_4 = 4$,得 $x_1 = 1$、$x_2 = 5$、$x_3 = 3$:
   $$\mathrm{C_3H_8} + 5\,\mathrm{O_2} \rightarrow 3\,\mathrm{CO_2} + 4\,\mathrm{H_2O}.$$
7. **驗算**:C 左 3 右 3;H 左 8 右 8;O 左 10 右 $6 + 4 = 10$ ✓。係數全部加倍也平衡,但化學家習慣用最小的整數。

#### 備註
課本是用向量方程式(1.3)來列式;這裡改成「每種原子一條方程式」,W1 就能做。第 2 週學完向量方程式後,可以回頭對照課本的寫法(習題 6、8 的提示也是用向量)。

### 例 3 · Lay 1.6 Example 2
The network in the figure shows the traffic flow (in vehicles per hour) over several one-way streets in downtown Baltimore during a typical early afternoon. Determine the general flow pattern for the network.

![Baltimore 市中心的單行道。每條分支的箭頭是車流方向;$x_1, \dots, x_5$ 是未知的流量。](baltimore.svg)

1. **標出節點與未知數**:四個路口 A、B、C、D,五條內部分支的流量 $x_1, \dots, x_5$(圖上已標好)。
2. **每個路口寫「流進 = 流出」**:
   - A:流進 $300 + 500$,流出 $x_1 + x_2$ → $x_1 + x_2 = 800$
   - B:流進 $x_2 + x_4$,流出 $300 + x_3$ → $x_2 - x_3 + x_4 = 300$
   - C:流進 $100 + 400$,流出 $x_4 + x_5$ → $x_4 + x_5 = 500$
   - D:流進 $x_1 + x_5$,流出 $600$ → $x_1 + x_5 = 600$
3. **整個網路也要守恆**:流進 $500 + 300 + 100 + 400 = 1300$,流出 $300 + x_3 + 600$,所以 $x_3 = 400$。這是第五條方程式。
4. **寫成增廣矩陣並化簡**(細節和觀念 4 一樣,這裡只列結果):
   $$\left[\begin{array}{rrrrr|r} 1 & 1 & 0 & 0 & 0 & 800 \\ 0 & 1 & -1 & 1 & 0 & 300 \\ 0 & 0 & 0 & 1 & 1 & 500 \\ 1 & 0 & 0 & 0 & 1 & 600 \\ 0 & 0 & 1 & 0 & 0 & 400 \end{array}\right] \sim \left[\begin{array}{rrrrr|r} 1 & 0 & 0 & 0 & 1 & 600 \\ 0 & 1 & 0 & 0 & -1 & 200 \\ 0 & 0 & 1 & 0 & 0 & 400 \\ 0 & 0 & 0 & 1 & 1 & 500 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{array}\right]$$
5. **讀出一般解**:pivot 在第 1–4 行,$x_5$ 是自由變數:
   $$x_1 = 600 - x_5, \quad x_2 = 200 + x_5, \quad x_3 = 400, \quad x_4 = 500 - x_5, \quad x_5 \text{ is free.}$$
6. **解讀**:有一條方程式是多餘的(化簡後出現全 0 列),所以只知道進出量,無法唯一決定每條街的車流——需要再量一條街(例如 $x_5$)才能全部決定。
7. **加上現實限制**:單行道的流量不能是負的。$x_4 = 500 - x_5 \ge 0$ 推出 $x_5 \le 500$;加上 $x_5 \ge 0$,所以 $0 \le x_5 \le 500$。

## 易錯點
- 經濟模型把「行」和「列」看反:**行**是一個部門的產出分到哪裡,**列**是一個部門買進什麼。
- 經濟模型得到全 0 列、有自由變數,以為算錯了。齊次方程組本來就可能有無限多解,這裡正是如此。
- 化學配平只數一種原子就停,或忘了分子前的係數要乘上原子數(例如 $x_2\,\mathrm{O_2}$ 有 $2x_2$ 個 O、$\mathrm{Ba(NO_3)_2}$ 有 6 個 O)。
- 化學配平得到分數就以為算錯。一般解本來就有自由變數,再取適當的值讓係數變整數。
- 網路流漏寫「整個網路的總流量守恆」那一條,或把流進、流出寫反;看錯箭頭方向。
- 熱傳導的節點方程式把「四個鄰居」數錯:邊界上的溫度是已知數,要移到右邊。

## 教學提示
這是**補充觀念**,不在 3 小時的節奏表裡。建議用法:時間夠時,挑例 3(網路流)花 15 分鐘上;否則留作自學,當成「觀念 2–5 學完之後的綜合練習」。經濟模型(例 1)對資工生比較遠,但可以用「這就是第 12 週 PageRank 的原型」來引起興趣。

應用題的關鍵是「列式」,不是「解」。課堂上可以只讓學生列出方程組、寫成增廣矩陣,化簡交給實作課的 `rref()`。課本標 **T** 的題目(Exercises 3c、4b、9、10)設計給電腦算,建議直接在實作課做。

## 練習
### 照做 · Lay 1.6 Practice Problem 1
Suppose an economy has three sectors: Agriculture, Mining, and Manufacturing. Agriculture sells 5% of its output to Mining and 30% to Manufacturing, and retains the rest. Mining sells 20% of its output to Agriculture and 70% to Manufacturing, and retains the rest. Manufacturing sells 20% of its output to Agriculture and 30% to Mining, and retains the rest. Determine the exchange table for this economy, where the columns describe how the output of each sector is exchanged among the three sectors.

#### 解答
百分比寫成小數;「retains the rest」要自己補,讓每一行加起來等於 1(課本 p. 82–83):

| Agriculture | Mining | Manufacturing | Purchased by |
|---|---|---|---|
| .65 | .20 | .20 | Agriculture |
| .05 | .10 | .30 | Mining |
| .30 | .70 | .50 | Manufacturing |

### 照做 · Lay 1.6 Practice Problem 2
Consider the network flow studied in Example 2. Determine the possible range of values of $x_1$ and $x_2$. [*Hint:* The example showed that $x_5 \le 500$. What does this imply about $x_1$ and $x_2$? Also, use the fact that $x_5 \ge 0$.]

#### 解答
$0 \le x_5 \le 500$。$x_1 = 600 - x_5$,所以 $100 \le x_1 \le 600$;$x_2 = 200 + x_5$,所以 $200 \le x_2 \le 700$(課本 p. 84)。

#### 備註
Example 2 是本講義的例 3(Baltimore)。

### 照做 · Lay 1.6 Exercise 1
Suppose an economy has only two sectors, Goods and Services. Each year, Goods sells 80% of its output to Services and keeps the rest, while Services sells 70% of its output to Goods and retains the rest. Find equilibrium prices for the annual outputs of the Goods and Services sectors that make each sector's income match its expenditures.

#### 解答
交換表(每一行加起來是 1):

| Goods | Services | Purchased by |
|---|---|---|
| .2 | .7 | Goods |
| .8 | .3 | Services |

收入 = 支出:$p_G = .2p_G + .7p_S$、$p_S = .8p_G + .3p_S$。移項得 $.8p_G - .7p_S = 0$ 與 $-.8p_G + .7p_S = 0$(兩式其實相同)。一般解:$p_G = .875p_S$,$p_S$ is free。

例如 $p_S = 1000$、$p_G = 875$;或用分數 $p_G = \tfrac78 p_S$,取 $p_S = 80$、$p_G = 70$。**只有價格的比例重要**(書後解答相同)。

### 照做 · Lay 1.6 Exercise 11
Find the general flow pattern of the network shown in the figure. Assuming that the flows are all nonnegative, what is the largest possible value for $x_3$?

![Lay 1.6 Exercise 11 的網路。注意 $x_3$ 的方向是從 B 流向 A。](network-ex11.svg)

#### 解答
每個節點「流進 = 流出」:

- A:$x_1 + x_3 = 20$
- B:$x_2 = x_3 + x_4$
- C:$80 = x_1 + x_2$

整個網路:流進 80、流出 $20 + x_4$,所以 $x_4 = 60$。解得

$$x_1 = 20 - x_3, \quad x_2 = 60 + x_3, \quad x_3 \text{ is free}, \quad x_4 = 60.$$

流量不能是負的:$x_1 = 20 - x_3 \ge 0$ 推出 $x_3 \le 20$。**$x_3$ 最大是 20**(書後解答相同)。

#### 備註
圖上 $x_3$ 的箭頭是 B → A,學生很容易看成 A → B。先請學生把每條分支的方向說一遍再列式。

### 變化 · Lay 1.6 Exercise 2
Find another set of equilibrium prices for the economy in Example 1. Suppose the same economy used Japanese yen instead of dollars to measure the value of the various sectors' outputs. Would this change the problem in any way? Discuss.

#### 解答
一般解是 $p_C = .94p_S$、$p_E = .85p_S$,任取 $p_S$ 都可以,例如 $p_S = 200$ 得 $p_C = 188$、$p_E = 170$。

改用日圓,等於把所有價格乘上同一個匯率 $r$。方程組是齊次的,$(rp_C, rp_E, rp_S)$ 仍然是解,**問題本質完全不變**:均衡只決定價格之間的比例,不決定用什麼單位。

### 變化 · Lay 1.6 Exercise 3
Consider an economy with three sectors, Chemicals & Metals, Fuels & Power, and Machinery. Chemicals sells 30% of its output to Fuels and 50% to Machinery and retains the rest. Fuels sells 80% of its output to Chemicals and 10% to Machinery and retains the rest. Machinery sells 40% to Chemicals and 40% to Fuels and retains the rest.

(a) Construct the exchange table for this economy. (b) Develop a system of equations that leads to prices at which each sector's income matches its expenses. Then write the augmented matrix that can be row reduced to find these prices. (c) **[T]** Find a set of equilibrium prices when the price for the Machinery output is 100 units.

#### 解答
(a)

| C&M | F&P | Mach. | Purchased by |
|---|---|---|---|
| .2 | .8 | .4 | C&M |
| .3 | .1 | .4 | F&P |
| .5 | .1 | .2 | Mach. |

(b) $p_C = .2p_C + .8p_F + .4p_M$、$p_F = .3p_C + .1p_F + .4p_M$、$p_M = .5p_C + .1p_F + .2p_M$,移項後的增廣矩陣:

$$\left[\begin{array}{rrr|r} .8 & -.8 & -.4 & 0 \\ -.3 & .9 & -.4 & 0 \\ -.5 & -.1 & .8 & 0 \end{array}\right]$$

(c) 化簡得 $p_C = \tfrac{17}{12}p_M$、$p_F = \tfrac{11}{12}p_M$。$p_M = 100$ 時,$p_C \approx 141.7$、$p_F \approx 91.7$;取兩位有效數字約為 $140$、$92$、$100$(書後解答相同)。

#### 備註
(c) 標 T,建議在實作課用 `rref()` 算;SymPy 會直接給出 $\tfrac{17}{12}$、$\tfrac{11}{12}$ 這種精確分數。

### 變化 · Lay 1.6 Exercise 4
Suppose an economy has four sectors, Agriculture (A), Energy (E), Manufacturing (M), and Transportation (T). Sector A sells 10% of its output to E and 25% to M and retains the rest. Sector E sells 30% of its output to A, 35% to M, and 25% to T and retains the rest. Sector M sells 30% of its output to A, 15% to E, and 40% to T and retains the rest. Sector T sells 20% of its output to A, 10% to E, and 30% to M and retains the rest.

(a) Construct the exchange table for this economy. (b) **[T]** Find a set of equilibrium prices for the economy.

#### 解答
(a) 「retains the rest」分別是 65%、10%、15%、40%:

| A | E | M | T | Purchased by |
|---|---|---|---|---|
| .65 | .30 | .30 | .20 | A |
| .10 | .10 | .15 | .10 | E |
| .25 | .35 | .15 | .30 | M |
| 0 | .25 | .40 | .40 | T |

(b) 列式後化簡,$p_T$ 是自由變數:$p_A = \tfrac{728}{359}p_T \approx 2.03p_T$、$p_E = \tfrac{572}{1077}p_T \approx .53p_T$、$p_M = \tfrac{1258}{1077}p_T \approx 1.17p_T$。例如 $p_T = 100$ 時,$p_A \approx 202.8$、$p_E \approx 53.1$、$p_M \approx 116.8$。

#### 備註
偶數題,書後沒有答案;上面的分數由 SymPy 精確計算。四個未知數用手算很容易出錯,建議在實作課做。

### 變化 · Lay 1.6 Exercise 5
Boron sulfide reacts violently with water to form boric acid and hydrogen sulfide gas (the smell of rotten eggs). The unbalanced equation is $\mathrm{B_2S_3} + \mathrm{H_2O} \rightarrow \mathrm{H_3BO_3} + \mathrm{H_2S}$. Balance the equation. [For each compound, construct a vector that lists the numbers of atoms of boron, sulfur, hydrogen, and oxygen.]

#### 解答
設 $x_1\,\mathrm{B_2S_3} + x_2\,\mathrm{H_2O} \rightarrow x_3\,\mathrm{H_3BO_3} + x_4\,\mathrm{H_2S}$。每種原子一條方程式(和提示說的「向量」是同一件事):

- B:$2x_1 = x_3$
- S:$3x_1 = x_4$
- H:$2x_2 = 3x_3 + 2x_4$
- O:$x_2 = 3x_3$

一般解 $x_1 = \tfrac13 x_4$、$x_2 = 2x_4$、$x_3 = \tfrac23 x_4$。取 $x_4 = 3$:

$$\mathrm{B_2S_3} + 6\,\mathrm{H_2O} \rightarrow 2\,\mathrm{H_3BO_3} + 3\,\mathrm{H_2S}$$

(書後解答相同。驗算 H:左 12、右 $6 + 6 = 12$ ✓。)

#### 備註
課本在 Exercises 5–10 前有一句共用的指示:「Balance the chemical equations in Exercises 5–10 using the vector equation approach discussed in this section.」W1 還沒教向量方程式(W2 才教),所以講義在 Exercises 5–8 的題幹各補一句「Balance the equation.」,用例 2 的「每種原子一條方程式」來做;題目裡「construct a vector」的提示,現階段當成「把每種原子的個數列成一串數字」即可。Exercises 9–10 題幹本身就有指示,沒有改。

### 變化 · Lay 1.6 Exercise 6
When solutions of sodium phosphate and barium nitrate are mixed, the result is barium phosphate (as a precipitate) and sodium nitrate. The unbalanced equation is $\mathrm{Na_3PO_4} + \mathrm{Ba(NO_3)_2} \rightarrow \mathrm{Ba_3(PO_4)_2} + \mathrm{NaNO_3}$. Balance the equation. [For each compound, construct a vector that lists the numbers of atoms of sodium (Na), phosphorus, oxygen, barium, and nitrogen. For instance, barium nitrate corresponds to $(0, 0, 6, 1, 2)$.]

#### 解答
設係數 $x_1, x_2, x_3, x_4$(依序)。注意括號:$\mathrm{Ba(NO_3)_2}$ 有 2 個 N、6 個 O;$\mathrm{Ba_3(PO_4)_2}$ 有 2 個 P、8 個 O。

- Na:$3x_1 = x_4$
- P:$x_1 = 2x_3$
- O:$4x_1 + 6x_2 = 8x_3 + 3x_4$
- Ba:$x_2 = 3x_3$
- N:$2x_2 = x_4$

一般解 $x_1 = 2x_3$、$x_2 = 3x_3$、$x_4 = 6x_3$。取 $x_3 = 1$:

$$2\,\mathrm{Na_3PO_4} + 3\,\mathrm{Ba(NO_3)_2} \rightarrow \mathrm{Ba_3(PO_4)_2} + 6\,\mathrm{NaNO_3}$$

驗算 O:左 $8 + 18 = 26$、右 $8 + 18 = 26$ ✓。

### 變化 · Lay 1.6 Exercise 7
Alka-Seltzer contains sodium bicarbonate ($\mathrm{NaHCO_3}$) and citric acid ($\mathrm{H_3C_6H_5O_7}$). When a tablet is dissolved in water, the following reaction produces sodium citrate, water, and carbon dioxide (gas): $\mathrm{NaHCO_3} + \mathrm{H_3C_6H_5O_7} \rightarrow \mathrm{Na_3C_6H_5O_7} + \mathrm{H_2O} + \mathrm{CO_2}$. Balance the equation.

#### 解答
設係數 $x_1, \dots, x_5$(依序)。

- Na:$x_1 = 3x_3$
- H:$x_1 + 8x_2 = 5x_3 + 2x_4$
- C:$x_1 + 6x_2 = 6x_3 + x_5$
- O:$3x_1 + 7x_2 = 7x_3 + x_4 + 2x_5$

一般解 $x_1 = x_5$、$x_2 = \tfrac13 x_5$、$x_3 = \tfrac13 x_5$、$x_4 = x_5$。取 $x_5 = 3$:

$$3\,\mathrm{NaHCO_3} + \mathrm{H_3C_6H_5O_7} \rightarrow \mathrm{Na_3C_6H_5O_7} + 3\,\mathrm{H_2O} + 3\,\mathrm{CO_2}$$

(書後解答相同。)

### 變化 · Lay 1.6 Exercise 8
The following reaction between potassium permanganate ($\mathrm{KMnO_4}$) and manganese sulfate in water produces manganese dioxide, potassium sulfate, and sulfuric acid: $\mathrm{KMnO_4} + \mathrm{MnSO_4} + \mathrm{H_2O} \rightarrow \mathrm{MnO_2} + \mathrm{K_2SO_4} + \mathrm{H_2SO_4}$. Balance the equation. [For each compound, construct a vector that lists the numbers of atoms of potassium (K), manganese, oxygen, sulfur, and hydrogen.]

#### 解答
設係數 $x_1, \dots, x_6$(依序)。

- K:$x_1 = 2x_5$
- Mn:$x_1 + x_2 = x_4$
- O:$4x_1 + 4x_2 + x_3 = 2x_4 + 4x_5 + 4x_6$
- S:$x_2 = x_5 + x_6$
- H:$2x_3 = 2x_6$

列化簡後只有一個自由變數;取讓係數都是最小正整數的值,得

$$2\,\mathrm{KMnO_4} + 3\,\mathrm{MnSO_4} + 2\,\mathrm{H_2O} \rightarrow 5\,\mathrm{MnO_2} + \mathrm{K_2SO_4} + 2\,\mathrm{H_2SO_4}$$

驗算 O:左 $8 + 12 + 2 = 22$、右 $10 + 4 + 8 = 22$ ✓。

### 變化 · Lay 1.6 Exercise 12
(a) Find the general traffic pattern in the freeway network shown in the figure. (Flow rates are in cars/minute.) (b) Describe the general traffic pattern when the road whose flow is $x_4$ is closed. (c) When $x_4 = 0$, what is the minimum value of $x_1$?

![Lay 1.6 Exercise 12 的高速公路網。](network-ex12.svg)

#### 解答
(a) 每個節點「流進 = 流出」:

- A:$x_1 = 40 + x_3 + x_4$
- B:$200 = x_1 + x_2$
- C:$x_2 + x_3 = 100 + x_5$
- D:$x_4 + x_5 = 60$

(整個網路:流進 200 = 流出 $40 + 100 + 60$,不提供新資訊。)化簡得

$$x_1 = 100 + x_3 - x_5, \quad x_2 = 100 - x_3 + x_5, \quad x_3 \text{ is free}, \quad x_4 = 60 - x_5, \quad x_5 \text{ is free.}$$

(b) 路封閉就是 $x_4 = 0$,於是 $x_5 = 60$:$x_1 = 40 + x_3$、$x_2 = 160 - x_3$、$x_3$ is free、$x_4 = 0$、$x_5 = 60$。

(c) $x_4 = 0$ 時 $x_1 = 40 + x_3$,而 $x_3 \ge 0$,所以 **$x_1$ 最小是 40**。

#### 備註
偶數題,書後沒有答案。這題有兩個自由變數,解集是「平面」;(b) 加上一條限制後剩一個自由變數,是很好的「加條件、減維度」例子。

### 變化 · Lay 1.6 Exercise 13
(a) Find the general flow pattern in the network shown in the figure. (b) Assuming that the flow must be in the directions indicated, find the minimum flows in the branches denoted by $x_2$, $x_3$, $x_4$, and $x_5$.

![Lay 1.6 Exercise 13 的網路。注意 $x_2$ 是 B → A、$x_5$ 是 C → B。](network-ex13.svg)

#### 解答
(a) 五個節點:

- A:$30 + x_2 = 80 + x_1$
- B:$x_3 + x_5 = x_2 + x_4$
- C:$100 + x_6 = 40 + x_5$
- D:$x_4 + 40 = 90 + x_6$
- E:$60 + x_1 = 20 + x_3$

化簡得

$$x_1 = x_3 - 40, \quad x_2 = x_3 + 10, \quad x_3 \text{ is free}, \quad x_4 = x_6 + 50, \quad x_5 = x_6 + 60, \quad x_6 \text{ is free.}$$

(b) 所有流量 $\ge 0$。$x_1 = x_3 - 40 \ge 0$ 推出 $x_3 \ge 40$;$x_6 \ge 0$。所以最小值是 **$x_2 = 50$、$x_3 = 40$、$x_4 = 50$、$x_5 = 60$**(書後解答相同)。

### 變化 · Lay 1.6 Exercise 14
Intersections in England are often constructed as one-way "roundabouts," such as the one shown in the figure. Assume that traffic must travel in the directions shown. Find the general solution of the network flow. Find the smallest possible value for $x_6$.

![Lay 1.6 Exercise 14 的環形交叉路口,車子順時針行駛。](roundabout-ex14.svg)

#### 解答
六個節點(沿著圓環 A → B → C → D → E → F → A):

- A:$x_1 = 100 + x_2$
- B:$50 + x_2 = x_3$
- C:$x_3 = 120 + x_4$
- D:$150 + x_4 = x_5$
- E:$x_5 = 80 + x_6$
- F:$100 + x_6 = x_1$

化簡(用最後一個未知數 $x_6$ 當參數):

$$x_1 = 100 + x_6, \quad x_2 = x_6, \quad x_3 = 50 + x_6, \quad x_4 = x_6 - 70, \quad x_5 = 80 + x_6, \quad x_6 \text{ is free.}$$

流量不能是負的:$x_4 = x_6 - 70 \ge 0$ 推出 $x_6 \ge 70$。**$x_6$ 最小是 70**。

#### 備註
偶數題,書後沒有答案。這題的六條方程式加起來是 $0 = 0$(環狀網路一定有一條多餘),所以一定有一個自由變數。

### 應用 · Lay 1.1 Exercises 43–44
An important concern in the study of heat transfer is to determine the steady-state temperature distribution of a thin plate when the temperature around the boundary is known. Assume the plate shown in the figure represents a cross section of a metal beam, with negligible heat flow in the direction perpendicular to the plate. Let $T_1, \dots, T_4$ denote the temperatures at the four interior nodes of the mesh. The temperature at a node is approximately equal to the average of the four nearest nodes — to the left, above, to the right, and below. For instance, $T_1 = (10 + 20 + T_2 + T_4)/4$, or $4T_1 - T_2 - T_4 = 30$.

![四個內部節點與邊界溫度。](heat-plate.svg)

(43) Write a system of four equations whose solution gives estimates for the temperatures $T_1, \dots, T_4$. (44) Solve the system. [*Hint:* To speed up the calculations, interchange rows 1 and 4 before starting "replace" operations.]

#### 解答
(43) 每個節點的四個鄰居(邊界是已知溫度,移到右邊):

$$\begin{aligned} 4T_1 - T_2 - T_4 &= 30 \\ -T_1 + 4T_2 - T_3 &= 60 \\ -T_2 + 4T_3 - T_4 &= 70 \\ -T_1 - T_3 + 4T_4 &= 40 \end{aligned}$$

(書後解答相同。)

(44) 列化簡得 $T_1 = 20$、$T_2 = 27.5$、$T_3 = 30$、$T_4 = 22.5$。

合理性檢查:$T_1$ 旁邊是 10°、20° 的邊界,本來就該最冷;$T_3$ 旁邊是 40°、30°,該最熱。答案符合直覺。

#### 備註
這題的「每點等於鄰居平均」正是影像補洞的原理,很適合和資工連結。手算 4×4 很花時間,可以只要求列式,解交給實作課的 `rref()`。

### 應用 · Lay 1.2 Exercise 45
Find the interpolating polynomial $p(t) = a_0 + a_1t + a_2t^2$ for the data $(1, 11)$, $(2, 16)$, $(3, 19)$. That is, find $a_0$, $a_1$, and $a_2$ such that

$$\begin{aligned} a_0 + a_1(1) + a_2(1)^2 &= 11 \\ a_0 + a_1(2) + a_2(2)^2 &= 16 \\ a_0 + a_1(3) + a_2(3)^2 &= 19 \end{aligned}$$

#### 解答
$$\left[\begin{array}{rrr|r} 1 & 1 & 1 & 11 \\ 1 & 2 & 4 & 16 \\ 1 & 3 & 9 & 19 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 1 & 1 & 11 \\ 0 & 1 & 3 & 5 \\ 0 & 2 & 8 & 8 \end{array}\right] \sim \left[\begin{array}{rrr|r} 1 & 1 & 1 & 11 \\ 0 & 1 & 3 & 5 \\ 0 & 0 & 2 & -2 \end{array}\right]$$

$a_2 = -1$、$a_1 = 5 - 3(-1) = 8$、$a_0 = 11 - 8 + 1 = 4$。所以 $p(t) = 4 + 8t - t^2$(書後解答相同)。

驗算:$p(1) = 11$、$p(2) = 4 + 16 - 4 = 16$、$p(3) = 4 + 24 - 9 = 19$ ✓。

#### 備註
實作課 ④ 應用第一步就是這一題。

### 應用 · Lay 1.2 Exercise 46
**[T]** In a wind tunnel experiment, the force on a projectile due to air resistance was measured at different velocities:

| Velocity (100 ft/sec) | 0 | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| Force (100 lb) | 0 | 2.90 | 14.8 | 39.6 | 74.3 | 119 |

Find an interpolating polynomial for these data and estimate the force on the projectile when the projectile is traveling at 750 ft/sec. Use $p(t) = a_0 + a_1t + a_2t^2 + a_3t^3 + a_4t^4 + a_5t^5$. What happens if you try to use a polynomial of degree less than 5? (Try a cubic polynomial, for instance.)

#### 解答
六個點、六個係數,解 $6 \times 6$ 方程組得 $a_0 = 0$、$a_1 = 1.7125$、$a_2 \approx -1.19479$、$a_3 \approx 0.66146$、$a_4 \approx -0.07005$、$a_5 \approx 0.0026$。

750 ft/sec 就是 $t = 7.5$:$p(7.5) \approx 64.84$,也就是**約 6484 磅**。

改用三次多項式:六條方程式、只有四個未知數,增廣矩陣的最後一行是 pivot 行 → **無解**,沒有三次多項式能剛好通過六個點。要找「最接近」的曲線,要等第 14 週的最小平方法。

#### 備註
實作課 ④ 應用的第二步就是這一題,數字由 NumPy 算出並經閘門核對。

### 應用 · Lay 1.6 Exercise 9
**[T]** If possible, use exact arithmetic or rational format for calculations in balancing the following chemical reaction: $\mathrm{PbN_6} + \mathrm{CrMn_2O_8} \rightarrow \mathrm{Pb_3O_4} + \mathrm{Cr_2O_3} + \mathrm{MnO_2} + \mathrm{NO}$.

#### 解答
設係數 $x_1, \dots, x_6$(依序)。

- Pb:$x_1 = 3x_3$
- N:$6x_1 = x_6$
- Cr:$x_2 = 2x_4$
- Mn:$2x_2 = x_5$
- O:$8x_2 = 4x_3 + 3x_4 + 2x_5 + x_6$

用精確分數化簡:$x_1 = \tfrac16 x_6$、$x_2 = \tfrac{22}{45}x_6$、$x_3 = \tfrac{1}{18}x_6$、$x_4 = \tfrac{11}{45}x_6$、$x_5 = \tfrac{44}{45}x_6$。分母的最小公倍數是 90,取 $x_6 = 90$:

$$15\,\mathrm{PbN_6} + 44\,\mathrm{CrMn_2O_8} \rightarrow 5\,\mathrm{Pb_3O_4} + 22\,\mathrm{Cr_2O_3} + 88\,\mathrm{MnO_2} + 90\,\mathrm{NO}$$

(書後解答相同。)

#### 備註
實作課 ④ 應用的最後一步就是這一題:SymPy 的 `rref()` 直接給出分數。如果用浮點數,$\tfrac{22}{45} = 0.4888\ldots$ 會被截斷,很難看出正確的整數比。

### 應用 · Lay 1.6 Exercise 10
**[T]** The chemical reaction below can be used in some industrial processes, such as the production of arsene ($\mathrm{AsH_3}$). Use exact arithmetic or rational format for calculations to balance this equation: $\mathrm{MnS} + \mathrm{As_2Cr_{10}O_{35}} + \mathrm{H_2SO_4} \rightarrow \mathrm{HMnO_4} + \mathrm{AsH_3} + \mathrm{CrS_3O_{12}} + \mathrm{H_2O}$.

#### 解答
設係數 $x_1, \dots, x_7$(依序)。

- Mn:$x_1 = x_4$
- S:$x_1 + x_3 = 3x_6$
- As:$2x_2 = x_5$
- Cr:$10x_2 = x_6$
- O:$35x_2 + 4x_3 = 4x_4 + 12x_6 + x_7$
- H:$2x_3 = x_4 + 3x_5 + 2x_7$

用精確分數化簡,取最小的正整數解:

$$16\,\mathrm{MnS} + 13\,\mathrm{As_2Cr_{10}O_{35}} + 374\,\mathrm{H_2SO_4} \rightarrow 16\,\mathrm{HMnO_4} + 26\,\mathrm{AsH_3} + 130\,\mathrm{CrS_3O_{12}} + 327\,\mathrm{H_2O}$$

#### 備註
偶數題,書後沒有答案。係數大到 374,手算幾乎不可能;這正是課本要求「用精確算術」的原因。實作課 Lab 的 TODO 就是這一題。

## 驗算
```check
Matrix([[1, Rational(-4, 10), Rational(-6, 10), 0], [Rational(-6, 10), Rational(9, 10), Rational(-2, 10), 0], [Rational(-4, 10), Rational(-5, 10), Rational(8, 10), 0]]).rref()[0][:2, 2] == Matrix([Rational(-31, 33), Rational(-28, 33)])
Matrix([[3, 0, -1, 0, 0], [8, 0, 0, -2, 0], [0, 2, -2, -1, 0]]).rref()[0] == Matrix([[1, 0, 0, Rational(-1, 4), 0], [0, 1, 0, Rational(-5, 4), 0], [0, 0, 1, Rational(-3, 4), 0]])
Matrix([[3, 0, -1, 0], [8, 0, 0, -2], [0, 2, -2, -1]]) * Matrix([1, 5, 3, 4]) == zeros(3, 1)
Matrix([[1, 1, 0, 0, 0, 800], [0, 1, -1, 1, 0, 300], [0, 0, 0, 1, 1, 500], [1, 0, 0, 0, 1, 600], [0, 0, 1, 0, 0, 400]]).rref()[0][:4, :] == Matrix([[1, 0, 0, 0, 1, 600], [0, 1, 0, 0, -1, 200], [0, 0, 1, 0, 0, 400], [0, 0, 0, 1, 1, 500]])
Matrix([[Rational(8, 10), Rational(-7, 10)], [Rational(-8, 10), Rational(7, 10)]]) * Matrix([Rational(7, 8), 1]) == zeros(2, 1)
Matrix([[Rational(8, 10), Rational(-8, 10), Rational(-4, 10)], [Rational(-3, 10), Rational(9, 10), Rational(-4, 10)], [Rational(-5, 10), Rational(-1, 10), Rational(8, 10)]]) * Matrix([Rational(17, 12), Rational(11, 12), 1]) == zeros(3, 1)
(eye(4) - Matrix([[Rational(65, 100), Rational(30, 100), Rational(30, 100), Rational(20, 100)], [Rational(10, 100), Rational(10, 100), Rational(15, 100), Rational(10, 100)], [Rational(25, 100), Rational(35, 100), Rational(15, 100), Rational(30, 100)], [0, Rational(25, 100), Rational(40, 100), Rational(40, 100)]])) * Matrix([Rational(728, 359), Rational(572, 1077), Rational(1258, 1077), 1]) == zeros(4, 1)
Matrix([[2, 0, -1, 0], [3, 0, 0, -1], [0, 2, -3, -2], [0, 1, -3, 0]]) * Matrix([1, 6, 2, 3]) == zeros(4, 1)
Matrix([[3, 0, 0, -1], [1, 0, -2, 0], [4, 6, -8, -3], [0, 1, -3, 0], [0, 2, 0, -1]]) * Matrix([2, 3, 1, 6]) == zeros(5, 1)
Matrix([[1, 0, -3, 0, 0], [1, 8, -5, -2, 0], [1, 6, -6, 0, -1], [3, 7, -7, -1, -2]]) * Matrix([3, 1, 1, 3, 3]) == zeros(4, 1)
Matrix([[1, 0, 0, 0, -2, 0], [1, 1, 0, -1, 0, 0], [4, 4, 1, -2, -4, -4], [0, 1, 0, 0, -1, -1], [0, 0, 2, 0, 0, -2]]) * Matrix([2, 3, 2, 5, 1, 2]) == zeros(5, 1)
Matrix([[1, 0, -3, 0, 0, 0], [6, 0, 0, 0, 0, -1], [0, 1, 0, -2, 0, 0], [0, 2, 0, 0, -1, 0], [0, 8, -4, -3, -2, -1]]) * Matrix([15, 44, 5, 22, 88, 90]) == zeros(5, 1)
Matrix([[1, 0, 0, -1, 0, 0, 0], [1, 0, 1, 0, 0, -3, 0], [0, 2, 0, 0, -1, 0, 0], [0, 10, 0, 0, 0, -1, 0], [0, 35, 4, -4, 0, -12, -1], [0, 0, 2, -1, -3, 0, -2]]) * Matrix([16, 13, 374, 16, 26, 130, 327]) == zeros(6, 1)
Matrix([[1, 0, 1, 0, 20], [0, 1, -1, -1, 0], [1, 1, 0, 0, 80]]).rref()[0] == Matrix([[1, 0, 1, 0, 20], [0, 1, -1, 0, 60], [0, 0, 0, 1, 60]])
Matrix([[1, 0, -1, -1, 0, 40], [1, 1, 0, 0, 0, 200], [0, 1, 1, 0, -1, 100], [0, 0, 0, 1, 1, 60]]).rref()[0][:3, :] == Matrix([[1, 0, -1, 0, 1, 100], [0, 1, 1, 0, -1, 100], [0, 0, 0, 1, 1, 60]])
Matrix([[1, -1, 0, 0, 0, 0, -50], [0, 1, -1, 1, -1, 0, 0], [0, 0, 0, 0, 1, -1, 60], [0, 0, 0, 1, 0, -1, 50], [1, 0, -1, 0, 0, 0, -40]]).rref()[0][:4, :] == Matrix([[1, 0, -1, 0, 0, 0, -40], [0, 1, -1, 0, 0, 0, 10], [0, 0, 0, 1, 0, -1, 50], [0, 0, 0, 0, 1, -1, 60]])
Matrix([[1, -1, 0, 0, 0, 0, 100], [0, 1, -1, 0, 0, 0, -50], [0, 0, 1, -1, 0, 0, 120], [0, 0, 0, 1, -1, 0, -150], [0, 0, 0, 0, 1, -1, 80], [-1, 0, 0, 0, 0, 1, -100]]).rref()[0][:5, 5:] == Matrix([[-1, 100], [-1, 0], [-1, 50], [-1, -70], [-1, 80]])
Matrix([[4, -1, 0, -1, 30], [-1, 4, -1, 0, 60], [0, -1, 4, -1, 70], [-1, 0, -1, 4, 40]]).rref()[0][:, 4] == Matrix([20, Rational(55, 2), 30, Rational(45, 2)])
Matrix([[1, 1, 1, 11], [1, 2, 4, 16], [1, 3, 9, 19]]).rref()[0][:, 3] == Matrix([4, 8, -1])
```
