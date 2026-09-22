---
title_en: Applications of Linear Systems
title_zh: 線性方程組的應用:網路流、化學配平、熱傳導、內插
sub: Conservation laws turn into linear equations
level: mid
source: Lay 1.6、1.1、1.2
supplement: true
lab_hook: "Lab ④ 應用:內插多項式(Lay 1.2 Exercises 45–46)"
---
## 觀念
Many applied problems lead to linear systems because something is **conserved**.

- **Network flow.** A *network* consists of *junctions* (or *nodes*) connected by *branches*. The basic assumption of network flow is that the total flow into the network equals the total flow out of the network, and the total flow into a junction equals the total flow out of the junction. Each junction gives one linear equation.
- **Balancing chemical equations.** Atoms are neither destroyed nor created in a reaction, so for each element, the number of atoms on the left must equal the number on the right. Each element gives one linear equation.
- **Steady-state heat flow.** On a mesh, the temperature at an interior node is approximately equal to the average of the temperatures at the four nearest nodes. Each interior node gives one linear equation.
- **Interpolating polynomials.** A polynomial whose graph passes through every given data point can be found by solving a linear system for its coefficients.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| network | 網路 | 由節點和分支組成 |
| junction / node | 節點 | 分支交會的地方 |
| branch | 分支 | 連接節點的線,有方向與流量 |
| flow conservation | 流量守恆 | 流進 = 流出 |
| balance a chemical equation | 化學方程式配平 | 找整數係數讓每種原子左右數量相同 |
| steady-state temperature | 穩態溫度 | 溫度不再隨時間變化時的分布 |
| mesh | 網格 | 把區域切成格子點 |
| interpolating polynomial | 內插多項式 | 圖形剛好通過每一個資料點的多項式 |

## 白話說
這一個觀念只有一個重點:**「守恆」會變成線性方程式**。

- 路口:流進來的車 = 流出去的車。
- 化學反應:反應前的碳原子 = 反應後的碳原子,氫、氧也一樣。
- 熱平衡:每個點的溫度 = 上下左右四個點的平均。
- 內插:曲線通過某個點,就等於「把這個點代進去成立」。

把每一條「守恆」寫下來,就得到一組線性方程式;接下來就是觀念 2–5 的工作:列化簡、找 pivot、寫一般解。**應用題最難的部分通常不是解,而是把方程式列出來。**

## 幾何意義
網路流的例 1 有一個自由變數 $x_5$,所以解集是一條「線」;但車流量不能是負的(單行道),這些**不等式**把線截成一段**線段**。這是第一次看到「方程式 + 不等式」的問題,到了最佳化(線性規劃)會成為主角。

內插的幾何很直觀:兩個點決定一條直線(一次多項式),三個點決定一條拋物線(二次多項式)。$k$ 個 $x$ 座標不同的點,剛好決定一個 $k-1$ 次多項式。

## 在資工哪裡用
- **網路流**:電腦網路的頻寬分配、路由,跟街道車流是同一個模型;「最大流量」問題是演算法課的經典題目。
- **熱傳導**:「每個點等於周圍的平均」和影像處理裡的**模糊(blur)**、**補洞(inpainting)**是同一件事——照片缺了一塊,就用周圍像素的平均把它補起來,背後就是在解這種方程組。
- **內插**:動畫的關鍵影格、字型的曲線、遊戲裡的平滑移動,都要一條曲線剛好通過指定的點。實作課會用 NumPy 做。

## 實際應用
課本 1.6 還有經濟學的均衡價格(Leontief 交換模型),以及 1.10 的營養配方、電路等應用;第 5 週的 2.6 會再回到 Leontief 投入產出模型。本觀念挑的是和資工最接近、也最不需要額外背景知識的幾個。

## 原理
**為什麼網路流方程式一定是線性的?** 每個節點「流進 = 流出」,流量只是加加減減,沒有相乘,所以是線性。

**為什麼化學配平一定有無限多解?** 配平方程組是**齊次**的(右邊全是 0),$x = 0$ 永遠是解;而且只要 $(x_1, \dots, x_n)$ 是解,乘上任何倍數也是解。化學家要的是「最小的正整數解」,所以通常把自由變數取成讓所有係數都變整數的最小值。

**為什麼內插多項式唯一?** 課本在 1.2 Exercise 45 只要求解出來;一般結論是:$x$ 座標互不相同時,係數矩陣(稱為 Vandermonde 矩陣)的每一行都是 pivot 行,所以解唯一。第 8 週學行列式時可以再證明一次。

**負流量的意義**:網路模型裡,負的流量代表實際方向和圖上畫的相反。單行道不允許反向,所以得到 $x_i \ge 0$ 的限制。

## 老師講解
### 例 1 · Lay 1.6 Example 2
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
課本是用向量方程式(1.3)來列式;這裡改成「每種原子一條方程式」,W1 就能做。第 2 週學完向量方程式後,可以回頭對照課本的寫法。

## 易錯點
- 網路流漏寫「整個網路的總流量守恆」那一條,或把流進、流出寫反。
- 化學配平只數一種原子就停,或忘了分子前的係數要乘上原子數(例如 $x_2\,\mathrm{O_2}$ 有 $2x_2$ 個 O)。
- 化學配平得到分數就以為算錯。一般解本來就有自由變數,再取適當的值讓係數變整數。
- 熱傳導的節點方程式把「四個鄰居」數錯:邊界上的溫度是已知數,要移到右邊。

## 教學提示
這是**補充觀念**,不在 3 小時的節奏表裡。建議用法:時間夠時,挑例 1(網路流)花 15 分鐘上;否則留作自學,當成「觀念 2–5 學完之後的綜合練習」。

應用題的關鍵是「列式」,不是「解」。課堂上可以只讓學生列出方程組、寫成增廣矩陣,化簡交給實作課的 `rref()`。

## 練習
### 照做 · Lay 1.6 Practice Problem 2
Consider the network flow studied in Example 1. Determine the possible range of values of $x_1$ and $x_2$. [*Hint:* The example showed that $x_5 \le 500$. What does this imply about $x_1$ and $x_2$? Also, use the fact that $x_5 \ge 0$.]

#### 解答
$0 \le x_5 \le 500$。$x_1 = 600 - x_5$,所以 $100 \le x_1 \le 600$;$x_2 = 200 + x_5$,所以 $200 \le x_2 \le 700$。

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

### 變化 · Lay 1.6 Exercise 5
Boron sulfide reacts violently with water to form boric acid and hydrogen sulfide gas (the smell of rotten eggs). The unbalanced equation is $\mathrm{B_2S_3} + \mathrm{H_2O} \rightarrow \mathrm{H_3BO_3} + \mathrm{H_2S}$. Balance the equation.

#### 解答
設 $x_1\,\mathrm{B_2S_3} + x_2\,\mathrm{H_2O} \rightarrow x_3\,\mathrm{H_3BO_3} + x_4\,\mathrm{H_2S}$。

- B:$2x_1 = x_3$
- S:$3x_1 = x_4$
- H:$2x_2 = 3x_3 + 2x_4$
- O:$x_2 = 3x_3$

一般解 $x_1 = \tfrac13 x_4$、$x_2 = 2x_4$、$x_3 = \tfrac23 x_4$。取 $x_4 = 3$:

$$\mathrm{B_2S_3} + 6\,\mathrm{H_2O} \rightarrow 2\,\mathrm{H_3BO_3} + 3\,\mathrm{H_2S}$$

(書後解答相同。驗算 H:左 12、右 $6 + 6 = 12$ ✓。)

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
實作課 ④ 應用就是這一題,再加上 Exercise 46(風洞資料,需要電腦)。

## 驗算
```check
Matrix([[1, 1, 0, 0, 0, 800], [0, 1, -1, 1, 0, 300], [0, 0, 0, 1, 1, 500], [1, 0, 0, 0, 1, 600], [0, 0, 1, 0, 0, 400]]).rref()[0][:4, :] == Matrix([[1, 0, 0, 0, 1, 600], [0, 1, 0, 0, -1, 200], [0, 0, 1, 0, 0, 400], [0, 0, 0, 1, 1, 500]])
Matrix([[3, 0, -1, 0, 0], [8, 0, 0, -2, 0], [0, 2, -2, -1, 0]]).rref()[0] == Matrix([[1, 0, 0, Rational(-1, 4), 0], [0, 1, 0, Rational(-5, 4), 0], [0, 0, 1, Rational(-3, 4), 0]])
Matrix([[3, 0, -1, 0], [8, 0, 0, -2], [0, 2, -2, -1]]) * Matrix([1, 5, 3, 4]) == zeros(3, 1)
Matrix([[1, 0, 1, 0, 20], [0, 1, -1, -1, 0], [1, 1, 0, 0, 80]]).rref()[0] == Matrix([[1, 0, 1, 0, 20], [0, 1, -1, 0, 60], [0, 0, 0, 1, 60]])
Matrix([[2, 0, -1, 0], [3, 0, 0, -1], [0, 2, -3, -2], [0, 1, -3, 0]]) * Matrix([1, 6, 2, 3]) == zeros(4, 1)
Matrix([[1, 0, -3, 0, 0], [1, 8, -5, -2, 0], [1, 6, -6, 0, -1], [3, 7, -7, -1, -2]]) * Matrix([3, 1, 1, 3, 3]) == zeros(4, 1)
Matrix([[4, -1, 0, -1, 30], [-1, 4, -1, 0, 60], [0, -1, 4, -1, 70], [-1, 0, -1, 4, 40]]).rref()[0][:, 4] == Matrix([20, Rational(55, 2), 30, Rational(45, 2)])
Matrix([[1, 1, 1, 11], [1, 2, 4, 16], [1, 3, 9, 19]]).rref()[0][:, 3] == Matrix([4, 8, -1])
```
