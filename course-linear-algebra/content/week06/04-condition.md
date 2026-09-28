---
title_en: Ill-Conditioned Matrices and the Condition Number
title_zh: 病態矩陣:可逆不代表算得準
sub: Invertible in theory, unreliable in floating point
level: mid
source: Lay 2.3(Numerical Notes)
lab_hook: '`np.linalg.cond(A)`:條件數愈大,答案的可信位數愈少'
---
## 觀念
**Numerical Notes**(Lay 2.3, p. 147)

In practical work, you might occasionally encounter a "nearly singular" or **ill-conditioned** matrix—an invertible matrix that can become singular if some of its entries are changed ever so slightly. In this case, row reduction may produce fewer than $n$ pivot positions, as a result of roundoff error. Also, roundoff error can sometimes make a singular matrix appear to be invertible.

Some matrix programs will compute a **condition number** for a square matrix. The larger the condition number, the closer the matrix is to being singular. The condition number of the identity matrix is 1. A singular matrix has an infinite condition number. In extreme cases, a matrix program may not be able to distinguish between a singular matrix and an ill-conditioned matrix.

Exercises 49–53 show that matrix computations can produce substantial error when a condition number is large.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| ill-conditioned | 病態的 | 可逆,但「差一點就不可逆」 |
| nearly singular | 幾乎奇異 | 同上的另一種說法 |
| condition number | 條件數 | 量「有多接近不可逆」的數;$I$ 是 1,奇異矩陣是無限大 |
| roundoff error | 捨入誤差 | 電腦只存有限位數造成的誤差 |
| percentage error | 百分比誤差 | $\dfrac{\lvert \text{近似值} - \text{真值} \rvert}{\lvert \text{真值} \rvert} \times 100\%$ |
| digits of accuracy | 可信位數 | 答案有幾位數字可以相信 |

## 白話說
**上兩個觀念說的是「可不可逆」——這是一個是非題。這個觀念要說的是:可逆的矩陣裡,也有「好算」和「難算」之分。**

想像兩條直線求交點:

- 兩條線**接近垂直**:哪怕把線稍微移動一點,交點也只動一點點。好算。
- 兩條線**幾乎平行**:線只要動一點點,交點就滑到很遠的地方。難算。

![兩條幾乎重合的直線:右端只動 0.05%,解就從 (3.94, 0.49) 跑到 (2.90, 2.00)。](ill-conditioned.svg)

課本 Exercise 49 就是這個例子:

$$\begin{aligned} 4.5x_1 + 3.1x_2 &= 19.249 \\ 1.6x_1 + 1.1x_2 &= 6.843 \end{aligned} \qquad\text{解是 } (3.94,\; 0.49)$$

把右端四捨五入到小數兩位(只動了不到 $0.05\%$):

$$\begin{aligned} 4.5x_1 + 3.1x_2 &= 19.25 \\ 1.6x_1 + 1.1x_2 &= 6.84 \end{aligned} \qquad\text{解變成 } (2.90,\; 2.00)$$

$x_1$ 錯了 $26\%$,$x_2$ 錯了 $308\%$。**輸入只動萬分之幾,答案卻面目全非。**

**為什麼?** 因為這個係數矩陣的 $\det = 4.5(1.1) - 3.1(1.6) = 4.95 - 4.96 = -0.01$,非常接近 0——兩條線幾乎平行。

**條件數**就是把這件事量化成一個數:

| 條件數 | 意思 |
|---|---|
| $1$ | 最好的情況(單位矩陣、正交矩陣) |
| $10^3$ | 大約損失 3 位精度 |
| $10^{16}$ 以上 | 雙精度浮點(約 16 位)已經全軍覆沒 |
| $\infty$ | 奇異(不可逆) |

**實用的估算法則**:雙精度浮點大約有 16 位有效數字;若 $\operatorname{cond}(A) \approx 10^k$,答案大約只能相信 $16 - k$ 位。

## 在資工哪裡用
- **「跑得出答案」不等於「答案可信」**。`np.linalg.solve` 幾乎永遠會回傳一個向量,不會警告你這個答案只有 3 位可信。要自己檢查條件數。
- **機器學習的特徵共線**:兩個特徵高度相關(例如「身高公分」與「身高公尺」),設計矩陣就接近奇異,學出來的係數會亂跳——這就是為什麼要做特徵篩選或正則化(ridge regression 本質上就是在把條件數壓下來)。
- **圖學與模擬的累積誤差**:連續乘很多個變換矩陣時,病態的矩陣會把誤差放大。
- **選演算法的依據**:條件數大時,要改用更穩定的方法(第 14 週的 QR 分解就是為此而生),或提高精度。
- **不要用行列式判斷「好不好算」**:課本 Exercise 9 的矩陣 $\det = 1$(看起來很健康),條件數卻高達兩萬多。**行列式大小和數值穩定性沒有直接關係。**

## 數值筆記
三件實務上的注意事項:

1. **捨入誤差可能讓奇異矩陣看起來可逆**,也可能讓可逆矩陣在列化簡時少掉樞軸。所以程式裡不要用 `det(A) == 0` 判斷奇異——浮點數幾乎不可能剛好是 0。
2. **Hilbert 矩陣**($a_{ij} = 1/(i + j - 1)$)是最著名的病態例子。$5$ 階的條件數已經約 $4.8 \times 10^5$,$12$ 階以上超過 $10^{16}$,用浮點求反矩陣完全不可信(Exercises 52–53)。
3. **NumPy 的對應函式**:`np.linalg.cond(A)`。SymPy 用精確算術時不受捨入影響,可以拿來當「正確答案」對照——實作課就是這樣做的。

## 合理性檢查
算完一個線性系統,可以這樣自我檢查:

- **殘差**:算 $A\mathbf{x} - \mathbf{b}$,看它有多接近 $\mathbf{0}$。但要小心:**殘差小不保證解準**,病態矩陣的錯誤解也可能有很小的殘差。
- **擾動測試**:把 $\mathbf{b}$ 改動 $0.01\%$ 再解一次,看答案動多少。動很多就是病態。
- **條件數**:最直接的指標。

## 原理
**條件數在量什麼?** 直觀地說,它是「輸出的相對變動」與「輸入的相對變動」的最大比值。**嚴格的不等式要用範數來量**:

$$\frac{\lVert \delta\mathbf{x} \rVert / \lVert \mathbf{x} \rVert}{\lVert \delta\mathbf{b} \rVert / \lVert \mathbf{b} \rVert} \;\le\; \operatorname{cond}(A)$$

用 Exercise 49 的數字驗一下:範數版的比值是 $2983 \le 3363$ ✓。**但如果改用「哪一個分量錯最多」這種逐分量的百分比**,比值會到約 $7000$,**比條件數還大**——所以條件數是「誤差放大倍率的量級指標」,不是逐分量百分比的上界。課本自己也只說 same order of magnitude:$\mathbf{b}$ 的相對變動約 $0.04\%$、解的相對變動約 $308\%$,比值約 $7700$,和條件數 $3363$ 同一個數量級。書後解答說的就是這件事:

> The percentage change in the solution from (3) to (4) is about 7700 times the percentage change in the right side of the equation. This is the same order of magnitude as the condition number. The condition number gives a rough measure of how sensitive the solution of $A\mathbf{x} = \mathbf{b}$ can be to changes in $\mathbf{b}$.

**為什麼幾何上是「幾乎平行」?** 兩行(或兩列)幾乎成比例時,行列式接近 0,對應的兩條直線幾乎重合。解是交點,而兩條幾乎重合的線,交點的位置對線的位置極端敏感——它會沿著那條「共同的方向」滑很遠。

第 16 週學 SVD 之後會看到條件數的精確定義($\sigma_{\max}/\sigma_{\min}$),現在只要有這個直覺就夠了。

## 老師講解
### 例 1 · 補充:兩條幾乎重合的線
Solve $\begin{bmatrix} 1 & 1 \\ 1 & 1.0001 \end{bmatrix}\mathbf{x} = \begin{bmatrix} 2 \\ 2.0001 \end{bmatrix}$. Then solve the same system with the right side changed to $(2,\; 2.0002)$, and compare.

1. **先解原系統**。第二式減第一式:
   $$0.0001\,x_2 = 0.0001 \quad \Longrightarrow \quad x_2 = 1, \quad x_1 = 2 - 1 = 1$$
   所以 $\mathbf{x} = (1, 1)$。
2. **再解擾動後的系統**(右端第二格從 $2.0001$ 改成 $2.0002$,只動了 **0.005%**):
   $$0.0001\,x_2 = 0.0002 \quad \Longrightarrow \quad x_2 = 2, \quad x_1 = 2 - 2 = 0$$
   所以 $\mathbf{x} = (0, 2)$。
3. **對照兩個答案**:$(1, 1)$ 變成 $(0, 2)$。$x_1$ 錯了 **100%**、$x_2$ 錯了 **100%**。
4. **輸入動 0.005%、輸出動 100%** ⇒ 放大了約 **2 萬倍**。
5. **但這個矩陣可逆嗎?** $\det = 1.0001 - 1 = 0.0001 \ne 0$ ⇒ **可逆**,IMT 十二條全部成立。
6. **所以「可逆」與「算得準」是兩件事**。這就是本節唯一要講的觀念。
7. **幾何上**:兩條直線的斜率是 $-1$ 與 $-1/1.0001$,**幾乎平行**。交點是兩線相交處,而兩條幾乎重合的線,交點會沿著線滑很遠。
8. **程式上的警告**:換一個更好的演算法救不了這件事。`numpy.linalg.solve` 對這個系統算出來的其實是精確的 $(1,1)$——**被放大的是資料本身的誤差**,而右端的 $2.0001$ 在真實世界往往就是量出來的近似值。問題出在矩陣,不是演算法。

### 例 2 · 補充:條件數與損失的位數
For the matrix $A = \begin{bmatrix} 1 & 1 \\ 1 & 1.0001 \end{bmatrix}$ in Example 1, a matrix program reports $\operatorname{cond}(A) \approx 4 \times 10^4$. Using double precision (about 16 significant digits), how many digits of the computed solution can you trust?

1. **先讀條件數的量級**:$4 \times 10^4$,也就是 $\log_{10}(4 \times 10^4) \approx 4.6$。
2. **估算法則**:$\operatorname{cond}(A) \approx 10^k$ 時,大約**損失 $k$ 位**精度。
3. **所以這題損失約 4.6 位**,$16 - 4.6 \approx 11$ ⇒ **大約 11 位可信**。
4. **和例 1 對照**:例 1 的誤差放大約 2 萬倍($\approx 10^{4.3}$),和條件數 $4 \times 10^4$ **同一個數量級** ✓ 這正是條件數的意義。
5. **注意行列式完全不是指標**:這個 $A$ 的 $\det = 10^{-4}$ 很小,看起來「快要奇異」;但把 $A$ 整個乘以 100,$\det$ 會變成 $10^{-4} \times 100^2 = 1$,**條件數卻一點都沒變**。
6. **為什麼?** 條件數是**比值**(奇異值之比),對整體縮放免疫;行列式是**乘積**,會被縮放放大或縮小。
7. **一句結論**:**要判斷「這個系統算不算得準」,看條件數,不要看行列式。**

### 例 3 · 補充:Hilbert 矩陣,教科書等級的壞矩陣
Let $H = \begin{bmatrix} 1 & 1/2 & 1/3 \\ 1/2 & 1/3 & 1/4 \\ 1/3 & 1/4 & 1/5 \end{bmatrix}$ (the $3 \times 3$ Hilbert matrix). Its inverse is $H^{-1} = \begin{bmatrix} 9 & -36 & 30 \\ -36 & 192 & -180 \\ 30 & -180 & 180 \end{bmatrix}$, and $\operatorname{cond}(H) \approx 524$. What does this tell you?

1. **先看 $H$ 本身**:每一格都是 $1/(i+j-1)$,數字都很小、很溫和,**看不出有什麼問題**。
2. **再看 $H^{-1}$**:出現了 $192$、$-180$ 這種大數字。**原矩陣除了左上角的 1 以外每一格都小於 1,反矩陣卻到上百**——這就是病態的徵兆。
3. **條件數 $\approx 524$**,而這才只是**三階**。階數再往上會壞到什麼程度?練習的 T 題與實作課會讓你自己量——先猜一下。
4. **為什麼要在意?** 雙精度只有約 16 位;條件數每多一個數量級就吃掉一位。**條件數一旦逼近 $10^{16}$,算出來的答案一位都不能信。**
5. **為什麼 Hilbert 矩陣這麼壞?** 因為相鄰兩列的**方向很接近**($1/2, 1/3, 1/4$ 與 $1/3, 1/4, 1/5$ 的夾角很小),就像例 1 那兩條幾乎重合的線;階數越高,列與列之間越靠近。
6. **實務上會遇到嗎?** 會。多項式擬合時,若直接用 $1, t, t^2, \dots$ 當基底,得到的正規方程矩陣就是 Hilbert 型的——這是第 14 週要改用正交多項式的原因。
7. **驗算方式**:$H \cdot H^{-1}$ 應該得到 $I$。用精確分數算會剛好;用浮點算(三階)會看到 $10^{-15}$ 量級的殘渣,而 $\varepsilon \cdot \operatorname{cond}(H) \approx 10^{-13}$ 是這個殘渣的**上界**。階數拉高時殘渣會往上界靠——高到某個程度就完全不能信了。

## 易錯點
- **以為「可逆」就代表「算得準」**。這是本節唯一要打破的迷思。
- **用行列式判斷穩定性**。$\det = 1$ 的矩陣可能條件數上萬;$\det$ 很小也不一定病態(整個矩陣乘上 $0.001$,$\det$ 會變很小,但條件數不變)。
- **在程式裡寫 `det(A) == 0`**。浮點數幾乎不可能剛好是 0,要用 `cond` 或 `matrix_rank`(它有容差)。
- **把「殘差小」當成「解準」**。病態時錯誤的解也可能有很小的殘差。
- **在 Hilbert 矩陣裡用浮點輸入**。輸入本身就先錯了。

## 教學提示
這個觀念只要 15 分鐘,但**不要跳過**——它是本週唯一「數值」的內容,也是資工學生最需要的那種警覺。

講法:先在黑板上畫兩條幾乎平行的線,用手比一比「線動一點,交點跑很遠」,再把 Exercise 49 的數字丟出來。數字比抽象說明有效得多(26% 和 308% 這兩個數會讓學生記住一輩子)。

**條件數不要講定義**(要等第 16 週的 SVD),只講它的用法與量級的意義。

課堂建議做:Exercise 49 的 a、b 小題(用分數算,10 分鐘);其餘 T 題 Exercises 50–53 全部放進實作課。

## 練習
### 照做 · Lay 2.3 Exercise 49(T 電腦題)
Suppose an experiment leads to the following system of equations:

$$\begin{aligned} 4.5x_1 + 3.1x_2 &= 19.249 \\ 1.6x_1 + 1.1x_2 &= 6.843 \end{aligned} \tag{3}$$

- **a.** Solve system (3), and then solve system (4), below, in which the data on the right have been rounded to two decimal places. In each case, find the *exact* solution.

$$\begin{aligned} 4.5x_1 + 3.1x_2 &= 19.25 \\ 1.6x_1 + 1.1x_2 &= 6.84 \end{aligned} \tag{4}$$

- **b.** The entries in (4) differ from those in (3) by less than .05%. Find the percentage error when using the solution of (4) as an approximation for the solution of (3).
- **c.** Use your matrix program to produce the condition number of the coefficient matrix in (3).

#### 解答
**a.** 係數矩陣的 $\det = 4.95 - 4.96 = -0.01$。用分數精確求解:

系統 (3):$x_1 = 3.94$、$x_2 = 0.49$。
系統 (4):$x_1 = 2.90$、$x_2 = 2.00$。

**b.** $x_1$ 的相對誤差 $= \dfrac{|2.90 - 3.94|}{3.94} \approx 26\%$;$x_2$ 的相對誤差 $= \dfrac{|2.00 - 0.49|}{0.49} \approx 308\%$。

右端只動了不到 $0.05\%$,解卻變動 26% 與 308%。

**c.** $\operatorname{cond}(A) \approx 3363$。解的相對變動約是右端相對變動的 7700 倍,和條件數同一個數量級。

#### 備註
**一定要用分數(或精確算術)解**,用小數會看不出 $\det = -0.01$ 這個關鍵。$3.94 = \tfrac{197}{50}$、$0.49 = \tfrac{49}{100}$、$2.90 = \tfrac{29}{10}$。

a、b 兩小題手算即可,c 小題放進實作課。書後解答的 7700 倍是把 308% 除以 0.04% 得到的。

### 變化 · Lay 2.3 Exercises 50–51(T 電腦題)
(50) Find the condition number of the matrix $A$ in Exercise 9. Construct a random vector $\mathbf{x}$ in $\mathbb{R}^4$ and compute $\mathbf{b} = A\mathbf{x}$. Then use your matrix program to compute the solution $\mathbf{x}_1$ of $A\mathbf{x} = \mathbf{b}$. To how many digits do $\mathbf{x}$ and $\mathbf{x}_1$ agree? Find out the number of digits your matrix program stores accurately, and report how many digits of accuracy are lost when $\mathbf{x}_1$ is used in place of the exact solution $\mathbf{x}$.

(51) Repeat Exercise 50 for the matrix in Exercise 10.

#### 解答
(50) 觀念 1 的 Exercise 9 那個 $4 \times 4$ 矩陣:$\operatorname{cond}_2(A) \approx 2.37 \times 10^4$(實算 $23683$)。雙精度約存 16 位,$k \approx 4$,所以大約**損失 4–5 位**,$\mathbf{x}$ 與 $\mathbf{x}_1$ 約吻合到第 11–12 位。

(51) Exercise 10 那個 $5 \times 5$ 矩陣:$\operatorname{cond}_2(A) \approx 6.86 \times 10^4$(書後說約 69,000)。同樣介於 $10^4$ 與 $10^5$ 之間,**損失 4–5 位**,吻合到 11–12 位。

#### 備註
兩題都標 T,放進實作課。實際數字會因隨機向量而略有不同,重點是**損失的位數 $\approx \log_{10}\operatorname{cond}(A)$** 這個法則。

Exercise 9 的矩陣 $\det = 1$ 卻條件數上萬,是本節最好的教材:**行列式不是穩定性的指標**。

### 應用 · Lay 2.3 Exercises 52–53(T 電腦題)
(52) Solve an equation $A\mathbf{x} = \mathbf{b}$ for a suitable $\mathbf{b}$ to find the last column of the inverse of the *fifth-order Hilbert matrix*

$$A = \begin{bmatrix} 1 & 1/2 & 1/3 & 1/4 & 1/5 \\ 1/2 & 1/3 & 1/4 & 1/5 & 1/6 \\ 1/3 & 1/4 & 1/5 & 1/6 & 1/7 \\ 1/4 & 1/5 & 1/6 & 1/7 & 1/8 \\ 1/5 & 1/6 & 1/7 & 1/8 & 1/9 \end{bmatrix}$$

How many digits in each entry of $\mathbf{x}$ do you expect to be correct? Explain. [*Note:* The exact solution is $(630,\ -12600,\ 56700,\ -88200,\ 44100)$.]

(53) Some matrix programs, such as MATLAB, have a command to create Hilbert matrices of various sizes. If possible, use an inverse command to compute the inverse of a twelfth-order or larger Hilbert matrix, $A$. Compute $AA^{-1}$. Report what you find.

#### 解答
(52) 取 $\mathbf{b} = \mathbf{e}_5 = (0, 0, 0, 0, 1)$ 解 $A\mathbf{x} = \mathbf{e}_5$,解就是 $A^{-1}$ 的第 5 行:
$$\mathbf{x} = (630,\; -12600,\; 56700,\; -88200,\; 44100)$$

$\operatorname{cond}_2(A) \approx 4.8 \times 10^5$,即 $k \approx 5$–$6$;雙精度約 16 位,所以每個分量大約只能相信**前 10–11 位**。

(53) 12 階以上的 Hilbert 矩陣條件數超過 $10^{16}$,已經超出雙精度的能力。實際跑會看到:

1. 程式可能發出「matrix is close to singular」之類的警告;
2. $AA^{-1}$ **不是**單位矩陣——非對角線會出現離 0 很遠的數值,對角線也不會剛好是 1。

若看起來還算乾淨,就換更大的階數再試。

#### 備註
(52) 在程式裡**一定要用 `Rational`**,直接寫 `1/3` 會從輸入就開始錯。

(53) 是整個觀念的收尾,也是實作課最後一個畫面:**「可逆」是代數性質,「算得準」是另一回事。**

## 驗算
```check
Matrix([[Rational(9,2), Rational(31,10)], [Rational(8,5), Rational(11,10)]]).det() == Rational(-1,100)
Matrix([[Rational(9,2), Rational(31,10)], [Rational(8,5), Rational(11,10)]]).solve(Matrix([Rational(19249,1000), Rational(6843,1000)])) == Matrix([Rational(197,50), Rational(49,100)])
Matrix([[Rational(9,2), Rational(31,10)], [Rational(8,5), Rational(11,10)]]).solve(Matrix([Rational(77,4), Rational(171,25)])) == Matrix([Rational(29,10), 2])
abs(Rational(29,10) - Rational(197,50)) / Rational(197,50) > Rational(1,4)
abs(2 - Rational(49,100)) / Rational(49,100) > 3
round(float(Matrix([[4.5, 3.1], [1.6, 1.1]]).condition_number())) == 3363
float(Matrix([Rational(29,10) - Rational(197,50), 2 - Rational(49,100)]).norm() / Matrix([Rational(197,50), Rational(49,100)]).norm()) / float(Matrix([Rational(77,4) - Rational(19249,1000), Rational(171,25) - Rational(6843,1000)]).norm() / Matrix([Rational(19249,1000), Rational(6843,1000)]).norm()) < 3363
round(float(Matrix([[4.0, 0.0, -7.0, -7.0], [-6.0, 1.0, 11.0, 9.0], [7.0, -5.0, 10.0, 19.0], [-1.0, 2.0, 3.0, -1.0]]).condition_number())) == 23683
round(float(Matrix([[5, 3, 1, 7, 9], [6, 4, 2, 8, -8], [7, 5, 3, 10, 9], [9, 6, 4, -9, -5], [8, 5, 2, 11, 4]]).condition_number()) / 1000) == 69
Matrix(5, 5, lambda t, s: Rational(1, t + s + 1)).inv()[:, 4] == Matrix([630, -12600, 56700, -88200, 44100])
Matrix(5, 5, lambda t, s: Rational(1, t + s + 1)).solve(Matrix([0, 0, 0, 0, 1])) == Matrix([630, -12600, 56700, -88200, 44100])
Matrix(5, 5, lambda t, s: Rational(1, t + s + 1)).det() == Rational(1, 266716800000)
eye(4).condition_number() == 1
(lambda a: a.solve(Matrix([2, Rational(20001,10000)])) == Matrix([1, 1]) and a.solve(Matrix([2, Rational(20002,10000)])) == Matrix([0, 2]))(Matrix([[1, 1], [1, Rational(10001,10000)]]))
Matrix(3, 3, lambda i, j: Rational(1, i + j + 1)).inv() == Matrix([[9, -36, 30], [-36, 192, -180], [30, -180, 180]])
```
