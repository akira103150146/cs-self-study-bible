---
title_en: Linear Models in Business, Science, and Engineering
title_zh: 線性模型的應用:營養配方、電路、人口遷移
sub: Proportional and additive means linear
level: mid
source: Lay 1.10
supplement: true
lab_hook: 'Lab ④ 應用:遷移矩陣 `M**k * x0` 看長期趨勢(Lay 1.10 Exercises 11–13)'
---
## 觀念
The mathematical models in this section are all *linear*; that is, each describes a problem by means of a linear equation, usually in vector or matrix form. The first model concerns nutrition but actually is representative of a general technique in linear programming problems. The second model comes from electrical engineering. The third model introduces the concept of a *linear difference equation*, a powerful mathematical tool for studying dynamic processes in a wide variety of fields such as engineering, ecology, economics, telecommunications, and the management sciences.

**Kirchhoff's voltage law.** The algebraic sum of the $RI$ voltage drops in one direction around a loop equals the algebraic sum of the voltage sources in the same direction around the loop. (Ohm's law: the voltage drop across a resistor is $V = RI$, with $V$ in volts, $R$ in ohms and $I$ in amperes.)

**Difference equations.** If there is a matrix $A$ such that $\mathbf{x}_1 = A\mathbf{x}_0$, $\mathbf{x}_2 = A\mathbf{x}_1$, and, in general,

$$\mathbf{x}_{k+1} = A\mathbf{x}_k \quad \text{for } k = 0, 1, 2, \dots \tag{5}$$

then (5) is called a **linear difference equation** (or **recurrence relation**). Given such an equation, one can compute $\mathbf{x}_1$, $\mathbf{x}_2$, and so on, provided $\mathbf{x}_0$ is known.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| nutrient vector | 營養向量 | 一單位食材提供的各種營養,排成一個向量 |
| Ohm's law | 歐姆定律 | $V = RI$:電壓降 = 電阻 × 電流 |
| Kirchhoff's voltage law | 克希荷夫電壓定律 | 繞一圈,電壓降的總和 = 電壓源的總和 |
| loop current | 迴路電流 | 每個封閉迴路指定一個電流變數 $I_k$ |
| branch | 分支 | 兩個迴路共用的那一段線路 |
| difference equation / recurrence relation | 差分方程 / 遞迴關係 | $\mathbf{x}_{k+1} = A\mathbf{x}_k$ |
| migration matrix | 遷移矩陣 | 每一行是「從某地出發的人,去了哪裡」的比例 |
| state vector | 狀態向量 | $\mathbf{x}_k$:第 $k$ 期的系統狀態 |

## 白話說
這一個觀念用三個真實模型說明同一句話:**只要「成正比」而且「可以相加」,就是線性模型**。

1. **營養配方**:每 100 g 某食材提供的營養是一個向量;用 $x_1$ 單位就是 $x_1\mathbf{a}_1$(成正比),幾種食材加起來是總營養(可以相加)。要湊出指定的營養,就是解 $A\mathbf{x} = \mathbf{b}$。**注意解必須非負**才有物理意義。
2. **電路**:歐姆定律說電壓降和電流成正比,克希荷夫定律說一圈上的電壓降可以相加。迴路電流是未知數,寫出來就是 $R\mathbf{i} = \mathbf{v}$。
3. **人口遷移**:每年固定比例的人搬家,所以「明年的人口」是「今年的人口」乘上一個矩陣:$\mathbf{x}_{k+1} = M\mathbf{x}_k$。反覆乘下去就能推估未來。

第三個模型最重要:它把「時間」帶進線性代數。第 11、12 週會用特徵值算出「很多年以後會怎樣」,而 PageRank 也是這種模型。

## 幾何意義
遷移模型可以畫成一張圖:節點是地區,箭頭是每年搬遷的比例。

![課本 Figure 2:城市與郊區之間的年遷移比例。每年 5% 的市民搬到郊區、3% 的郊區居民搬進城市。](migration.svg)

矩陣的每一**行**代表「從某地出發的人去了哪裡」,所以每一行加起來是 1(人不會憑空消失)。這種矩陣叫 **Markov 矩陣**,第 12 週會再回來。

## 在資工哪裡用
- **PageRank**:網頁之間的連結就是一個遷移矩陣,$\mathbf{x}_{k+1} = M\mathbf{x}_k$ 反覆乘,收斂到的向量就是網頁排名(第 12 週)。
- **模擬與遊戲**:狀態每一格更新一次 $\mathbf{x}_{k+1} = A\mathbf{x}_k$,是最基本的離散動態系統。
- **電路模擬器**:SPICE 這類工具就是自動寫出 $R\mathbf{i} = \mathbf{v}$ 再解方程組。
- **推薦系統與使用者流失**:用戶在不同方案之間的轉換比例寫成矩陣,可以推估下一季各方案的人數。

## 原理
**為什麼這些模型是線性的?**

- 營養:每種食材提供的營養和用量**成正比**(純量倍數),幾種食材的營養**相加**(向量加法)。
- 電路:歐姆定律 $V = RI$ 是正比;克希荷夫定律是「相加」。所以把電壓源加倍,電流也會加倍;兩組電壓源的效果可以分開算再相加(**疊加原理**,觀念 2 的性質 5)。課本示範把 $R\mathbf{i} = \mathbf{v}$ 拆成三個只有單一電源的問題,解加起來就是原問題的解。
- 遷移:搬家人數和該地區人數成正比,各地搬來的人數相加。

**電路方程式怎麼寫**(課本 Example 2 的規則,所有迴路電流都取逆時針):

1. 對角線 $r_{kk}$ = 迴路 $k$ 上**所有**電阻的和。
2. 非對角線 $r_{kj}$ = 迴路 $k$ 與 $j$ **共用**的電阻,取**負號**(因為共用分支上兩個迴路的電流方向相反)。
3. 右邊 $v_k$ = 迴路 $k$ 上電壓源的代數和:電流從電池的負極流向正極時記正,反之記負。

## 老師講解
### 例 1 · Lay 1.10 Example 1
If possible, find some combination of nonfat milk, soy flour, and whey to provide the exact amounts of protein, carbohydrate, and fat supplied by the diet in one day.

| Nutrient | Nonfat milk | Soy flour | Whey | Amounts (g) supplied by the diet in one day |
|---|---|---|---|---|
| Protein | 36 | 51 | 13 | 33 |
| Carbohydrate | 52 | 34 | 74 | 45 |
| Fat | 0 | 7 | 1.1 | 3 |

1. **設變數**:$x_1, x_2, x_3$ 分別是三種食材的單位數(1 單位 = 100 g)。
2. **笨方法**:對蛋白質、碳水、脂肪各寫一條方程式。可行,但要寫三次。
3. **好方法(課本的做法)**:把每種食材的營養當成一個**向量**。$x_1$ 單位的脫脂奶粉提供 $x_1\mathbf{a}_1$,其中 $\mathbf{a}_1$ 是表格的第一行。
4. **寫成一條向量方程式**:
   $$x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + x_3\mathbf{a}_3 = \mathbf{b}$$
5. **列化簡**:
   $$\begin{bmatrix} 36 & 51 & 13 & 33 \\ 52 & 34 & 74 & 45 \\ 0 & 7 & 1.1 & 3 \end{bmatrix} \sim \cdots \sim \begin{bmatrix} 1 & 0 & 0 & .277 \\ 0 & 1 & 0 & .392 \\ 0 & 0 & 1 & .233 \end{bmatrix}$$
6. **讀答案**(取三位有效數字):.277 單位脫脂奶粉、.392 單位大豆粉、.233 單位乳清。
7. **檢查合理性**:三個數都是**正的**,才有物理意義。課本特別提醒:用 $-.233$ 單位的乳清是不可能的事;要找到非負解,常常需要更多種食材(Exercise 4 就會出現負數)。

### 例 2 · Lay 1.10 Example 2
Determine the loop currents in the network in Figure 1.

![課本 Figure 1:三個迴路,電壓源分別是 30 V(上)、5 V(中間分支)、20 V(下)。所有迴路電流都取逆時針。](circuit-fig1.svg)

1. **迴路 1 的電阻**:$I_1$ 流過 4 Ω、4 Ω、3 Ω 三個電阻,電壓降合計 $(4 + 4 + 3)I_1 = 11I_1$。
2. **扣掉共用分支**:分支 $AB$ 上的 3 Ω 也被迴路 2 流過,而且方向相反,所以要減 $3I_2$。迴路 1 的電壓源是 $+30$ V:
   $$11I_1 - 3I_2 = 30$$
3. **迴路 2**:自己的電阻總和 $6I_2$(3 + 1 + 1 + 1),減去和迴路 1 共用的 $3I_1$、和迴路 3 共用的 $1 \cdot I_3$;電壓源 $+5$ V:
   $$-3I_1 + 6I_2 - I_3 = 5$$
4. **迴路 3**:$-I_2 + 3I_3 = -25$。注意:5 V 電池同時屬於迴路 2 和 3,但對迴路 3 來說方向相反,記 $-5$;20 V 也同理記 $-20$,合計 $-25$。
5. **解方程組**:
   $$\begin{aligned} 11I_1 - 3I_2 &= 30 \\ -3I_1 + 6I_2 - I_3 &= 5 \\ -I_2 + 3I_3 &= -25 \end{aligned} \qquad \Longrightarrow \qquad I_1 = 3,\; I_2 = 1,\; I_3 = -8$$
6. **解讀負值**:$I_3 = -8$ 安培代表迴路 3 的實際電流方向和圖上畫的**相反**,大小 8 安培。
7. **分支電流**:$A$ 到 $B$ 這段是 $I_1 - I_2 = 2$ 安培(沿 $I_1$ 的方向);$C$ 到 $D$ 是 $I_2 - I_3 = 9$ 安培。
8. **矩陣形式**:$R\mathbf{i} = \mathbf{v}$,其中 $R$ 對稱、對角線是各迴路的總電阻、非對角線是共用電阻的負值。若把電壓加倍,電流也加倍——這就是線性。

### 例 3 · Lay 1.10 Example 3
Compute the population of the region just described for the years 2021 and 2022, given that the population in 2020 was 600,000 in the city and 400,000 in the suburbs. (Each year 5% of the city's population moves to the suburbs and 3% of the suburban population moves to the city.)

1. **寫出遷移矩陣**:每一行是「從哪裡出發」,每一列是「去了哪裡」:
   $$M = \begin{bmatrix} .95 & .03 \\ .05 & .97 \end{bmatrix} \begin{matrix} \text{To: City} \\ \text{To: Suburbs} \end{matrix}$$
2. **檢查**:每一行加起來是 1(.95 + .05 = 1、.03 + .97 = 1),人沒有消失。
3. **初始狀態**:$\mathbf{x}_0 = \begin{bmatrix} 600{,}000 \\ 400{,}000 \end{bmatrix}$。
4. **2021 年**:
   $$\mathbf{x}_1 = M\mathbf{x}_0 = \begin{bmatrix} .95(600000) + .03(400000) \\ .05(600000) + .97(400000) \end{bmatrix} = \begin{bmatrix} 582{,}000 \\ 418{,}000 \end{bmatrix}$$
5. **2022 年**:再乘一次,$\mathbf{x}_2 = M\mathbf{x}_1 = \begin{bmatrix} 565{,}440 \\ 434{,}560 \end{bmatrix}$。
6. **為什麼這是線性模型**:搬家人數和人口**成正比**,各地搬來的人數**相加**——所以 $\mathbf{x}_k \mapsto \mathbf{x}_{k+1}$ 是線性變換。
7. **往前看**:一直乘下去會怎樣?實作課會算 20 年(Exercise 13),你會看到人口趨向一個**穩定狀態**。第 12 週會用特徵值直接算出那個狀態。

## 易錯點
- 營養或配方問題解出**負數**還照樣寫答案。要檢查非負(Exercise 4 的答案就有負的,結論是「這個組合做不到」)。
- 電路題的非對角線忘了加負號,或把兩個迴路共用的電阻算成兩次。
- 電壓的正負號:電流從電池的負極流向正極才記正號。同一顆電池對相鄰兩個迴路通常一正一負(例 2 的 5 V)。
- 遷移矩陣寫成轉置:每一**行**加起來才是 1。寫反了會得到完全不同的答案。
- 把「兩天後」算成乘 2:要乘兩次,$\mathbf{x}_2 = M^2\mathbf{x}_0$。

## 教學提示
這個觀念是補充,**不在節奏表裡**。時間夠的話,例 2(電路)花 15 分鐘最值得講:學生在電子學也會遇到,看到「寫成矩陣就解完了」會很有感。

例 1 的重點不是算術,而是「向量化的思考方式」:一次處理三種營養,而不是寫三條方程式。

例 3 建議留到實作課,Exercise 13 用程式跑 20 年,看人口趨勢比手算三年有感覺得多。

課堂建議做:Exercise 1、Practice Problem;Exercises 5 與 9 各做一題。其餘 T 題(Exercises 3、4、6–8、11–14)留給實作課或當作業。

## 練習
### 照做 · Lay 1.10 Exercise 1
The container of a breakfast cereal usually lists the number of calories and the amounts of protein, carbohydrate, and fat contained in one serving of the cereal. The amounts for two common cereals are given below. Suppose a mixture of these two cereals is to be prepared that contains exactly 295 calories, 9 g of protein, 48 g of carbohydrate, and 8 g of fat.

| Nutrient | General Mills Cheerios | Quaker 100% Natural Cereal |
|---|---|---|
| Calories | 110 | 130 |
| Protein (g) | 4 | 3 |
| Carbohydrate (g) | 20 | 18 |
| Fat (g) | 2 | 5 |

- **a.** Set up a vector equation for this problem. Include a statement of what the variables in your equation represent.
- **b.** Write an equivalent matrix equation, and then determine if the desired mixture of the two cereals can be prepared.

#### 解答
(a) 設 $x_1$ = Cheerios 的份數、$x_2$ = 100% Natural 的份數:
$$x_1\begin{bmatrix} 110 \\ 4 \\ 20 \\ 2 \end{bmatrix} + x_2\begin{bmatrix} 130 \\ 3 \\ 18 \\ 5 \end{bmatrix} = \begin{bmatrix} 295 \\ 9 \\ 48 \\ 8 \end{bmatrix}$$

(b) 矩陣形式 $\begin{bmatrix} 110 & 130 \\ 4 & 3 \\ 20 & 18 \\ 2 & 5 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 295 \\ 9 \\ 48 \\ 8 \end{bmatrix}$。化簡增廣矩陣得 $\begin{bmatrix} 1 & 0 & 1.5 \\ 0 & 1 & 1 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$:相容,$x_1 = 1.5$、$x_2 = 1$。

**可以**:1.5 份 Cheerios 加 1 份 100% Natural(書後解答相同)。驗算:$165 + 130 = 295$ 卡、$6 + 3 = 9$ g 蛋白質、$30 + 18 = 48$ g 碳水、$3 + 5 = 8$ g 脂肪 ✓。

#### 備註
四條方程式、兩個未知數,本來很可能無解;這題剛好相容。多出來的兩條等於免費的驗算。

### 照做 · Lay 1.10 Practice Problem
Find a matrix $A$ and vectors $\mathbf{x}$ and $\mathbf{b}$ such that the problem in Example 1 amounts to solving the equation $A\mathbf{x} = \mathbf{b}$.

#### 解答
$$A = \begin{bmatrix} 36 & 51 & 13 \\ 52 & 34 & 74 \\ 0 & 7 & 1.1 \end{bmatrix}, \quad \mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 33 \\ 45 \\ 3 \end{bmatrix}$$
(課本 p. 117。$A$ 的每一行是一種食材的營養向量,$\mathbf{x}$ 是各用幾單位,$\mathbf{b}$ 是目標營養。)

### 變化 · Lay 1.10 Exercise 2
One serving of Post Shredded Wheat supplies 160 calories, 5 g of protein, 6 g of fiber, and 1 g of fat. One serving of Crispix supplies 110 calories, 2 g of protein, .1 g of fiber, and .4 g of fat.

- **a.** Set up a matrix $B$ and a vector $\mathbf{u}$ such that $B\mathbf{u}$ gives the amounts of calories, protein, fiber, and fat contained in a mixture of three servings of Shredded Wheat and two servings of Crispix.
- **b.** **[T]** Suppose that you want a cereal with more fiber than Crispix but fewer calories than Shredded Wheat. Is it possible for a mixture of the two cereals to supply 130 calories, 3.20 g of protein, 2.46 g of fiber, and .64 g of fat? If so, what is the mixture?

#### 解答
(a) $B = \begin{bmatrix} 160 & 110 \\ 5 & 2 \\ 6 & .1 \\ 1 & .4 \end{bmatrix}$(行:Shredded Wheat、Crispix;列:熱量、蛋白質、纖維、脂肪)、$\mathbf{u} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$。

$B\mathbf{u} = (700,\ 19,\ 18.2,\ 3.8)$:700 卡、19 g 蛋白質、18.2 g 纖維、3.8 g 脂肪。

(b) 解 $B\mathbf{x} = (130,\ 3.20,\ 2.46,\ .64)$:增廣矩陣化簡得 $\begin{bmatrix} 1 & 0 & .4 \\ 0 & 1 & .6 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$,**可以**:.4 份 Shredded Wheat 加 .6 份 Crispix。

### 變化 · Lay 1.10 Exercises 9–10
Set up a difference equation that describes the situation, where $\mathbf{x}_0$ is the initial population in 2020. Then estimate the populations two years later, in 2022. (Ignore other factors that might influence the population sizes.)

(9) In a certain region, about 7% of a city's population moves to the surrounding suburbs each year, and about 5% of the suburban population moves into the city. In 2020, there were 800,000 residents in the city and 500,000 in the suburbs.

(10) In a certain region, about 6% of a city's population moves to the surrounding suburbs each year, and about 4% of the suburban population moves into the city. In 2020, there were 10,000,000 residents in the city and 800,000 in the suburbs.

#### 解答
(9) $\mathbf{x}_{k+1} = M\mathbf{x}_k$,其中 $M = \begin{bmatrix} .93 & .05 \\ .07 & .95 \end{bmatrix}$、$\mathbf{x}_0 = \begin{bmatrix} 800{,}000 \\ 500{,}000 \end{bmatrix}$。

$\mathbf{x}_1 = (769{,}000,\ 531{,}000)$、$\mathbf{x}_2 = (741{,}720,\ 558{,}280)$:2022 年市區約 741,720 人、郊區約 558,280 人(書後解答相同)。

(10) $M = \begin{bmatrix} .94 & .04 \\ .06 & .96 \end{bmatrix}$、$\mathbf{x}_0 = \begin{bmatrix} 10{,}000{,}000 \\ 800{,}000 \end{bmatrix}$。

$\mathbf{x}_1 = (9{,}432{,}000,\ 1{,}368{,}000)$、$\mathbf{x}_2 = (8{,}920{,}800,\ 1{,}879{,}200)$。

#### 備註
注意矩陣的主對角線是「留下來的比例」:7% 搬走,對角線就是 .93。

### 應用 · Lay 1.10 Exercises 3–4
**[T]** (3) After taking a nutrition class, a big Annie's Mac and Cheese fan decides to improve the levels of protein and fiber in her favorite lunch by adding broccoli and canned chicken.

| Nutrient | Mac and Cheese | Broccoli | Chicken | Shells |
|---|---|---|---|---|
| Calories | 270 | 51 | 70 | 260 |
| Protein (g) | 10 | 5.4 | 15 | 9 |
| Fiber (g) | 2 | 5.2 | 0 | 5 |

- **a.** If she wants to limit her lunch to 400 calories but get 30 g of protein and 10 g of fiber, what proportions of servings of Mac and Cheese, broccoli, and chicken should she use?
- **b.** She found that there was too much broccoli in the proportions from part (a), so she decided to switch from classical Mac and Cheese to Annie's Whole Wheat Shells and White Cheddar. What proportions of servings of each food should she use to meet the same goals as in part (a)?

(4) The Cambridge Diet supplies .8 g of calcium per day, in addition to the nutrients listed in Table 1 for Example 1. The amounts of calcium per unit (100 g) supplied by the three ingredients in the Cambridge Diet are as follows: 1.26 g from nonfat milk, .19 g from soy flour, and .8 g from whey. Another ingredient in the diet mixture is isolated soy protein, which provides the following nutrients in each unit: 80 g of protein, 0 g of carbohydrate, 3.4 g of fat, and .18 g of calcium. **a.** Set up a matrix equation whose solution determines the amounts of nonfat milk, soy flour, whey, and isolated soy protein necessary to supply the precise amounts of protein, carbohydrate, fat, and calcium in the Cambridge Diet. State what the variables in the equation represent. **b.** **[T]** Solve the equation in (a) and discuss your answer.

#### 解答
(3) (a) 解 $\begin{bmatrix} 270 & 51 & 70 \\ 10 & 5.4 & 15 \\ 2 & 5.2 & 0 \end{bmatrix}\mathbf{x} = \begin{bmatrix} 400 \\ 30 \\ 10 \end{bmatrix}$,得 $\mathbf{x} \approx (.99,\ 1.54,\ .79)$:.99 份通心粉、1.54 份花椰菜、.79 份雞肉(書後解答相同)。

(b) 把第一行換成 Shells 那一行,得 $\mathbf{x} \approx (1.09,\ .88,\ 1.03)$:花椰菜的份量明顯變少了(書後解答也提到這點)。

(4) (a) 設 $x_1, \dots, x_4$ 是脫脂奶粉、大豆粉、乳清、分離大豆蛋白的單位數:
$$\begin{bmatrix} 36 & 51 & 13 & 80 \\ 52 & 34 & 74 & 0 \\ 0 & 7 & 1.1 & 3.4 \\ 1.26 & .19 & .8 & .18 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{bmatrix} = \begin{bmatrix} 33 \\ 45 \\ 3 \\ .8 \end{bmatrix}$$
(列依序是蛋白質、碳水化合物、脂肪、鈣,單位 g。)

(b) 唯一解約是 $(.641,\ .544,\ -.0926,\ -.208)$。**後兩個是負的**,物理上做不到——這四種食材沒辦法剛好湊出指定的營養,需要更多(或不同的)食材。

### 應用 · Lay 1.10 Exercises 5–6
**[T]** Write a matrix equation that determines the loop currents. If a matrix program is available, solve the system for the loop currents. (All loop currents are drawn counterclockwise.)

(5) ![Exercise 5 的電路:四個上下堆疊的迴路。](circuit-ex5.svg)

(6) ![Exercise 6 的電路:四個上下堆疊的迴路,電池都在左側。](circuit-ex6.svg)

#### 解答
(5) 各迴路的總電阻:11、10、9、10;共用電阻:迴路 1–2 的 5 Ω、2–3 的 1 Ω、3–4 的 2 Ω(都取負號)。電壓:$50, -40, 30, -30$。
$$\begin{bmatrix} 11 & -5 & 0 & 0 \\ -5 & 10 & -1 & 0 \\ 0 & -1 & 9 & -2 \\ 0 & 0 & -2 & 10 \end{bmatrix}\begin{bmatrix} I_1 \\ I_2 \\ I_3 \\ I_4 \end{bmatrix} = \begin{bmatrix} 50 \\ -40 \\ 30 \\ -30 \end{bmatrix}$$
解得 $\mathbf{i} \approx (3.68,\ -1.90,\ 2.57,\ -2.49)$ 安培(書後解答相同)。

(6) 總電阻 6、9、7、7;共用 1 Ω、4 Ω、2 Ω。四顆電池都在左側、正極在下,逆時針電流都是從負極流向正極,所以四個電壓都是正的:
$$\begin{bmatrix} 6 & -1 & 0 & 0 \\ -1 & 9 & -4 & 0 \\ 0 & -4 & 7 & -2 \\ 0 & 0 & -2 & 7 \end{bmatrix}\mathbf{i} = \begin{bmatrix} 30 \\ 20 \\ 40 \\ 10 \end{bmatrix}$$
解得 $\mathbf{i} \approx (6.36,\ 8.14,\ 11.73,\ 4.78)$ 安培。

### 應用 · Lay 1.10 Exercises 7–8
**[T]** Write a matrix equation that determines the loop currents. If a matrix program is available, solve the system for the loop currents. (All loop currents are drawn counterclockwise.)

(7) ![Exercise 7 的電路:2 × 2 的四個迴路。](circuit-ex7.svg)

(8) ![Exercise 8 的電路:正方形中間再放一個菱形,共五個迴路。](circuit-ex8.svg)

#### 解答
(7) 總電阻 12、15、14、13;共用:1–2 的 7 Ω、1–4 的 4 Ω、2–3 的 6 Ω、3–4 的 5 Ω。迴路 1 與 3、迴路 2 與 4 只在中央交會,沒有共用電阻,所以那兩格是 0:
$$\begin{bmatrix} 12 & -7 & 0 & -4 \\ -7 & 15 & -6 & 0 \\ 0 & -6 & 14 & -5 \\ -4 & 0 & -5 & 13 \end{bmatrix}\mathbf{i} = \begin{bmatrix} 40 \\ 30 \\ 20 \\ -10 \end{bmatrix}$$
解得 $\mathbf{i} \approx (11.43,\ 10.55,\ 8.04,\ 5.84)$ 安培(書後解答相同)。

(8) 總電阻 9、7、10、7、12;中央的迴路 5 和其他四個都有共用電阻(4、3、3、2 Ω):
$$\begin{bmatrix} 9 & -1 & 0 & -1 & -4 \\ -1 & 7 & -2 & 0 & -3 \\ 0 & -2 & 10 & -3 & -3 \\ -1 & 0 & -3 & 7 & -2 \\ -4 & -3 & -3 & -2 & 12 \end{bmatrix}\mathbf{i} = \begin{bmatrix} 50 \\ -30 \\ 20 \\ -40 \\ 0 \end{bmatrix}$$
解得 $\mathbf{i} \approx (4.00,\ -4.38,\ -.90,\ -5.80,\ -.96)$ 安培。中央迴路沒有電源,所以第五個分量是 0。

#### 備註
Exercise 8 的 $R$ 矩陣對稱、對角線最大,這種矩陣叫「對角優勢」,數值上特別好解——第 6 週談 LU 分解時會再提到。

### 應用 · Lay 1.10 Exercises 11–12
**[T]** (11) College Moving Truck Rental has a fleet of 20, 100, and 200 trucks in Pullman, Spokane, and Seattle, respectively. A truck rented at one location may be returned to any of the three locations. The various fractions of trucks returned to the three locations each month are shown in the matrix below. What will be the approximate distribution of the trucks after three months?

$$\begin{bmatrix} .30 & .15 & .05 \\ .30 & .70 & .05 \\ .40 & .15 & .90 \end{bmatrix}$$

(12) Budget Rent a Car in Wichita, Kansas, has a fleet of about 500 cars, at three locations. A car rented at one location may be returned to any of the three locations. The various fractions of cars returned to the three locations are shown in the matrix below. Suppose that on Monday there are 295 cars at the airport (or rented from there), 55 cars at the east side office, and 150 cars at the west side office. What will be the approximate distribution of cars on Wednesday?

$$\begin{bmatrix} .97 & .05 & .10 \\ .00 & .90 & .05 \\ .03 & .05 & .85 \end{bmatrix}$$

#### 解答
(11) $\mathbf{x}_0 = (20, 100, 200)$,$\mathbf{x}_3 = M^3\mathbf{x}_0 \approx (32.05,\ 75.86,\ 212.09)$:三個月後約 **32 輛在 Pullman、76 輛在 Spokane、212 輛在 Seattle**(書後解答相同,總數仍是 320)。

(12) 星期一到星期三是**兩步**:$\mathbf{x}_2 = M^2\mathbf{x}_0 \approx (311.5,\ 58.3,\ 130.2)$,約 **312 輛在機場、58 輛在東區、130 輛在西區**(總數 500)。

#### 備註
課本 Exercise 11 的矩陣把列標籤印成「Airport / East / West」,顯然是從 Exercise 12 複製過來的;依書後解答,應該是 Pullman / Spokane / Seattle。

### 應用 · Lay 1.10 Exercise 13
**[T]** Let $M$ and $\mathbf{x}_0$ be as in Example 3. **a.** Compute the population vectors $\mathbf{x}_k$ for $k = 1, \dots, 20$. Discuss what you find. **b.** Repeat part (a) with an initial population of 350,000 in the city and 650,000 in the suburbs. What do you find?

#### 解答
(a) 市區人口**逐年下降**:第 7 年(2027)兩邊差不多(500,515 vs 499,485),之後郊區超過市區;20 年後市區約 **417,456** 人。但每年的變化量越來越小(書後解答相同)。

(b) 這次反過來:市區人口**緩慢上升**、郊區下降,20 年後市區從 350,000 變成約 **370,000**。

**兩次都朝同一個地方靠近**:穩定狀態是 375,000 / 625,000(此時 $.05r = .03s$,搬出與搬入剛好抵消),而且 $M\begin{bmatrix} 375000 \\ 625000 \end{bmatrix} = \begin{bmatrix} 375000 \\ 625000 \end{bmatrix}$——這個「乘上矩陣後不動」的向量,第 10 週會叫它**特徵向量**。

### 應用 · Lay 1.10 Exercise 14
**[T]** Study how changes in boundary temperatures on a steel plate affect the temperatures at interior points on the plate.

![Exercise 14:兩塊鋼板,四個內部點與八個邊界溫度。](plates-ex14.svg)

- **a.** Begin by estimating the temperatures $T_1, T_2, T_3, T_4$ at each of the sets of four points on the steel plate shown in the figure. In each case, the value of $T_k$ is approximated by the average of the temperatures at the four closest points. See Exercises 43 and 44 in Section 1.1, where the values (in degrees) turn out to be $(20, 27.5, 30, 22.5)$. How is this list of values related to your results for the points in set (a) and set (b)?
- **b.** Without making any computations, guess the interior temperatures in (a) when the boundary temperatures are all multiplied by 3. Check your guess.
- **c.** Finally, make a general conjecture about the correspondence from the list of eight boundary temperatures to the list of four interior temperatures.

#### 解答
(a) 每個內部點的溫度是四個鄰居的平均,整理成 $4T_k = $ 四個鄰居的和,係數矩陣是
$$\begin{bmatrix} 4 & -1 & 0 & -1 \\ -1 & 4 & -1 & 0 \\ 0 & -1 & 4 & -1 \\ -1 & 0 & -1 & 4 \end{bmatrix}$$
- 板 (a):右邊是 $(20, 20, 20, 20)$,解得 $(10, 10, 10, 10)$。
- 板 (b):右邊是 $(10, 40, 50, 20)$,解得 $(10, 17.5, 20, 12.5)$。

**關係**:兩組答案相加 $(20, 27.5, 30, 22.5)$,正好是第 1 週 Exercises 43–44 的答案;而那題的邊界溫度也正好是兩塊板邊界溫度的和。**邊界相加 → 內部溫度相加。**

(b) 猜測:內部溫度也變成 3 倍,$(30, 30, 30, 30)$。驗證:右邊變成 $(60, 60, 60, 60)$,解確實是 $(30, 30, 30, 30)$ ✓。

(c) 推測:「8 個邊界溫度 $\mapsto$ 4 個內部溫度」這個對應是**線性變換**——邊界資料相加,內部溫度就相加;邊界乘上倍數,內部溫度就乘上同樣的倍數。

#### 備註
這題把本週的主題和第 1 週的熱傳導應用接起來:它其實是在問「這個對應是不是線性的」,答案是肯定的,而且這正是 PDE 數值解裡最重要的性質。

## 驗算
```check
[round(float(v), 3) for v in Matrix([[36, 51, 13], [52, 34, 74], [0, 7, Rational(11, 10)]]).solve(Matrix([33, 45, 3]))] == [0.277, 0.392, 0.233]
Matrix([[11, -3, 0], [-3, 6, -1], [0, -1, 3]]).solve(Matrix([30, 5, -25])) == Matrix([3, 1, -8])
(lambda i: (i[0] - i[1], i[1] - i[2]))(Matrix([[11, -3, 0], [-3, 6, -1], [0, -1, 3]]).solve(Matrix([30, 5, -25]))) == (2, 9)
Matrix([[Rational(95, 100), Rational(3, 100)], [Rational(5, 100), Rational(97, 100)]]) * Matrix([600000, 400000]) == Matrix([582000, 418000])
Matrix([[Rational(95, 100), Rational(3, 100)], [Rational(5, 100), Rational(97, 100)]])**2 * Matrix([600000, 400000]) == Matrix([565440, 434560])
Matrix([[110, 130], [4, 3], [20, 18], [2, 5]]) * Matrix([Rational(3, 2), 1]) == Matrix([295, 9, 48, 8])
Matrix([[36, 51, 13], [52, 34, 74], [0, 7, Rational(11, 10)]]) * Matrix([x1, x2, x3]) == x1 * Matrix([36, 52, 0]) + x2 * Matrix([51, 34, 7]) + x3 * Matrix([13, 74, Rational(11, 10)])
Matrix([[160, 110], [5, 2], [6, Rational(1, 10)], [1, Rational(2, 5)]]) * Matrix([3, 2]) == Matrix([700, 19, Rational(91, 5), Rational(19, 5)])
Matrix([[160, 110, 130], [5, 2, Rational(16, 5)], [6, Rational(1, 10), Rational(123, 50)], [1, Rational(2, 5), Rational(16, 25)]]).rref()[0] == Matrix([[1, 0, Rational(2, 5)], [0, 1, Rational(3, 5)], [0, 0, 0], [0, 0, 0]])
Matrix([[Rational(93, 100), Rational(5, 100)], [Rational(7, 100), Rational(95, 100)]])**2 * Matrix([800000, 500000]) == Matrix([741720, 558280])
Matrix([[Rational(94, 100), Rational(4, 100)], [Rational(6, 100), Rational(96, 100)]])**2 * Matrix([10000000, 800000]) == Matrix([8920800, 1879200])
[round(float(v), 2) for v in Matrix([[270, 51, 70], [10, Rational(27, 5), 15], [2, Rational(26, 5), 0]]).solve(Matrix([400, 30, 10]))] == [0.99, 1.54, 0.79]
[round(float(v), 2) for v in Matrix([[260, 51, 70], [9, Rational(27, 5), 15], [5, Rational(26, 5), 0]]).solve(Matrix([400, 30, 10]))] == [1.09, 0.88, 1.03]
[round(float(v), 3) for v in Matrix([[36, 51, 13, 80], [52, 34, 74, 0], [0, 7, Rational(11, 10), Rational(17, 5)], [Rational(63, 50), Rational(19, 100), Rational(4, 5), Rational(9, 50)]]).solve(Matrix([33, 45, 3, Rational(4, 5)]))] == [0.641, 0.544, -0.093, -0.208]
[round(float(v), 2) for v in Matrix([[11, -5, 0, 0], [-5, 10, -1, 0], [0, -1, 9, -2], [0, 0, -2, 10]]).solve(Matrix([50, -40, 30, -30]))] == [3.68, -1.90, 2.57, -2.49]
[round(float(v), 2) for v in Matrix([[6, -1, 0, 0], [-1, 9, -4, 0], [0, -4, 7, -2], [0, 0, -2, 7]]).solve(Matrix([30, 20, 40, 10]))] == [6.36, 8.14, 11.73, 4.78]
[round(float(v), 2) for v in Matrix([[12, -7, 0, -4], [-7, 15, -6, 0], [0, -6, 14, -5], [-4, 0, -5, 13]]).solve(Matrix([40, 30, 20, -10]))] == [11.43, 10.55, 8.04, 5.84]
[round(float(v), 2) for v in Matrix([[9, -1, 0, -1, -4], [-1, 7, -2, 0, -3], [0, -2, 10, -3, -3], [-1, 0, -3, 7, -2], [-4, -3, -3, -2, 12]]).solve(Matrix([50, -30, 20, -40, 0]))] == [4.00, -4.38, -0.90, -5.80, -0.96]
[round(float(v)) for v in Matrix([[Rational(30, 100), Rational(15, 100), Rational(5, 100)], [Rational(30, 100), Rational(70, 100), Rational(5, 100)], [Rational(40, 100), Rational(15, 100), Rational(90, 100)]])**3 * Matrix([20, 100, 200])] == [32, 76, 212]
[round(float(v)) for v in Matrix([[Rational(97, 100), Rational(5, 100), Rational(10, 100)], [0, Rational(90, 100), Rational(5, 100)], [Rational(3, 100), Rational(5, 100), Rational(85, 100)]])**2 * Matrix([295, 55, 150])] == [312, 58, 130]
round(float((Matrix([[Rational(95, 100), Rational(3, 100)], [Rational(5, 100), Rational(97, 100)]])**20 * Matrix([600000, 400000]))[0])) == 417456
Matrix([[Rational(95, 100), Rational(3, 100)], [Rational(5, 100), Rational(97, 100)]]) * Matrix([375000, 625000]) == Matrix([375000, 625000])
Matrix([[4, -1, 0, -1], [-1, 4, -1, 0], [0, -1, 4, -1], [-1, 0, -1, 4]]).solve(Matrix([20, 20, 20, 20])) == Matrix([10, 10, 10, 10])
Matrix([[4, -1, 0, -1], [-1, 4, -1, 0], [0, -1, 4, -1], [-1, 0, -1, 4]]).solve(Matrix([10, 40, 50, 20])) == Matrix([10, Rational(35, 2), 20, Rational(25, 2)])
Matrix([[4, -1, 0, -1], [-1, 4, -1, 0], [0, -1, 4, -1], [-1, 0, -1, 4]]).solve(Matrix([30, 60, 70, 40])) == Matrix([20, Rational(55, 2), 30, Rational(45, 2)])
Matrix([[4, -1, 0, -1], [-1, 4, -1, 0], [0, -1, 4, -1], [-1, 0, -1, 4]]).solve(3 * Matrix([20, 20, 20, 20])) == Matrix([30, 30, 30, 30])
```
