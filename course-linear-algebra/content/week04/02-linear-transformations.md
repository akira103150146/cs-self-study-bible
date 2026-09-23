---
title_en: Linear Transformations
title_zh: 線性變換:保持加法與純量倍數的機器
sub: T(cu + dv) = cT(u) + dT(v)
level: mid
source: Lay 1.8
lab_hook: '檢查 `T(0)` 是不是 0、`T(2*x) == 2*T(x)`:一眼看出不是線性的變換'
---
## 觀念
**Definition.** A transformation (or mapping) $T$ is **linear** if

- **(i)** $T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$ for all $\mathbf{u}, \mathbf{v}$ in the domain of $T$;
- **(ii)** $T(c\mathbf{u}) = cT(\mathbf{u})$ for all scalars $c$ and all $\mathbf{u}$ in the domain of $T$.

Every matrix transformation is a linear transformation. Important examples of linear transformations that are not matrix transformations will be discussed in Chapters 4 and 5. Linear transformations *preserve the operations of vector addition and scalar multiplication*.

If $T$ is a linear transformation, then

$$T(\mathbf{0}) = \mathbf{0} \tag{3}$$

and

$$T(c\mathbf{u} + d\mathbf{v}) = cT(\mathbf{u}) + dT(\mathbf{v}) \tag{4}$$

for all vectors $\mathbf{u}$, $\mathbf{v}$ in the domain of $T$ and all scalars $c$, $d$. Observe that *if a transformation satisfies* (4) *for all* $\mathbf{u}, \mathbf{v}$ *and* $c, d$, *it must be linear.* Repeated application of (4) produces a useful generalization:

$$T(c_1\mathbf{v}_1 + \cdots + c_p\mathbf{v}_p) = c_1T(\mathbf{v}_1) + \cdots + c_pT(\mathbf{v}_p) \tag{5}$$

In engineering and physics, (5) is referred to as a *superposition principle*. Think of $\mathbf{v}_1, \dots, \mathbf{v}_p$ as signals that go into a system and $T(\mathbf{v}_1), \dots, T(\mathbf{v}_p)$ as the responses of that system to the signals. The system satisfies the superposition principle if whenever an input is expressed as a linear combination of such signals, the system's response is *the same* linear combination of the responses to the individual signals.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| linear transformation | 線性變換 | 滿足 (i)(ii) 兩個條件的變換 |
| preserve | 保持 | 先運算再變換 = 先變換再運算 |
| superposition principle | 疊加原理 | 工程與物理對 (5) 的叫法:輸入疊加,輸出也疊加 |
| contraction / dilation | 收縮 / 伸張 | $T(\mathbf{x}) = r\mathbf{x}$,$0 \le r \le 1$ 是收縮,$r > 1$ 是伸張 |
| affine transformation | 仿射變換 | $T(\mathbf{x}) = A\mathbf{x} + \mathbf{b}$;$\mathbf{b} \neq \mathbf{0}$ 時**不是**線性的 |

## 白話說
線性變換就是「**先算再變 = 先變再算**」的機器:

- 兩個向量先相加再丟進去,和分別丟進去再相加,結果一樣。
- 先放大 $c$ 倍再丟進去,和丟進去再放大 $c$ 倍,結果一樣。

合起來就是最好用的那一條:
$$T(c\mathbf{u} + d\mathbf{v}) = cT(\mathbf{u}) + dT(\mathbf{v}).$$

**檢查是不是線性的捷徑**:先算 $T(\mathbf{0})$。線性的話一定得到 $\mathbf{0}$;只要 $T(\mathbf{0}) \neq \mathbf{0}$,馬上就知道不是線性(Exercises 38、41)。注意反過來不成立:$T(\mathbf{0}) = \mathbf{0}$ 不保證線性(Exercise 40 的絕對值)。

**為什麼重要**:有了 (5),只要知道 $T$ 對「幾個基本向量」做了什麼,就知道它對**所有**向量做了什麼——這正是下一個觀念 Theorem 10 的關鍵。

## 幾何意義
伸張 $T(\mathbf{x}) = 3\mathbf{x}$:每個向量方向不變、長度變三倍。

![課本 Figure 5:伸張變換把每個向量拉長為三倍,方向不變。](dilation.svg)

旋轉 90°:平行四邊形整個轉過去,形狀不變——這正是 $T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$ 的圖像:左邊的平行四邊形轉成右邊的平行四邊形。

![課本 Figure 6:逆時針旋轉 90°。u、v 決定的平行四邊形,轉成 T(u)、T(v) 決定的平行四邊形。](rotation.svg)

## 在資工哪裡用
- **訊號處理的疊加原理**:把訊號拆成幾個簡單成分,各自算出系統的反應,再加起來就是總反應。整個傅立葉分析與濾波器設計都靠這一句(實作課的移動平均濾波)。
- **圖學的座標變換**:旋轉、縮放是線性的;**平移不是**(平移是 $\mathbf{x} + \mathbf{b}$,$T(\mathbf{0}) \neq \mathbf{0}$)。這就是為什麼圖學要用「齊次座標」把平移也塞成矩陣乘法(第 5 週 2.7)。
- **深度學習為什麼需要非線性**:多層線性變換疊起來仍然是線性(Exercise 44),表現力不會增加。所以每層之間要插入非線性的活化函數(ReLU)。

## 原理
**(3) 的證明**:由條件 (ii),$T(\mathbf{0}) = T(0\mathbf{u}) = 0T(\mathbf{u}) = \mathbf{0}$。

**(4) 的證明**:同時用 (i)(ii),$T(c\mathbf{u} + d\mathbf{v}) = T(c\mathbf{u}) + T(d\mathbf{v}) = cT(\mathbf{u}) + dT(\mathbf{v})$。

**(4) 也可以反過來當定義**:若 $T$ 對所有 $\mathbf{u}, \mathbf{v}, c, d$ 都滿足 (4),取 $c = d = 1$ 得 (i),取 $d = 0$ 得 (ii)。所以驗證線性時,證 (4) 一次就夠(例 1 的做法)。

**為什麼矩陣變換一定線性?** 因為第 2 週的 Theorem 5:$A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}$、$A(c\mathbf{u}) = cA\mathbf{u}$。

## 老師講解
### 例 1 · Lay 1.8 Example 4
Given a scalar $r$, define $T : \mathbb{R}^2 \to \mathbb{R}^2$ by $T(\mathbf{x}) = r\mathbf{x}$. $T$ is called a **contraction** when $0 \le r \le 1$ and a **dilation** when $r > 1$. Let $r = 3$, and show that $T$ is a linear transformation.

1. **要證的是什麼**:證 (4) 一次就夠——對任意 $\mathbf{u}, \mathbf{v}$ 與任意純量 $c, d$,都有 $T(c\mathbf{u} + d\mathbf{v}) = cT(\mathbf{u}) + dT(\mathbf{v})$。
2. **從定義出發**:$T(c\mathbf{u} + d\mathbf{v}) = 3(c\mathbf{u} + d\mathbf{v})$。
3. **用向量運算律展開**:$= 3c\mathbf{u} + 3d\mathbf{v}$。
4. **重新分組**:$= c(3\mathbf{u}) + d(3\mathbf{v})$。
5. **換回 $T$ 的寫法**:$= cT(\mathbf{u}) + dT(\mathbf{v})$。
6. **結論**:$T$ 滿足 (4),所以是線性變換。$r = 3 > 1$,這是伸張(見「幾何意義」的圖)。
7. **注意證明的樣子**:每一步都只用「定義」或「向量運算律」。以後要證明某個變換線性,都照這個模板寫。

### 例 2 · Lay 1.8 Example 5
Define a linear transformation $T : \mathbb{R}^2 \to \mathbb{R}^2$ by

$$T(\mathbf{x}) = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} -x_2 \\ x_1 \end{bmatrix}$$

Find the images under $T$ of $\mathbf{u} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}$, and $\mathbf{u} + \mathbf{v} = \begin{bmatrix} 6 \\ 4 \end{bmatrix}$.

1. **逐一計算**:$T(\mathbf{u}) = \begin{bmatrix} -1 \\ 4 \end{bmatrix}$、$T(\mathbf{v}) = \begin{bmatrix} -3 \\ 2 \end{bmatrix}$、$T(\mathbf{u} + \mathbf{v}) = \begin{bmatrix} -4 \\ 6 \end{bmatrix}$。
2. **檢查 (i)**:$T(\mathbf{u}) + T(\mathbf{v}) = (-1 - 3,\ 4 + 2) = (-4, 6) = T(\mathbf{u} + \mathbf{v})$ ✓。
3. **看出幾何意義**:$(x_1, x_2) \mapsto (-x_2, x_1)$ 就是**逆時針旋轉 90°**。$\mathbf{u} = (4, 1)$ 轉到 $(-1, 4)$。
4. **整個平行四邊形一起轉**:$T$ 把 $\mathbf{u}$、$\mathbf{v}$ 決定的平行四邊形,轉成 $T(\mathbf{u})$、$T(\mathbf{v})$ 決定的平行四邊形(課本 Figure 6)。
5. **這就是線性的圖像**:「先相加再轉」和「先轉再相加」得到同一個點,所以平行四邊形的形狀才保得住。

### 例 3 · Lay 1.8 Example 6
A company manufactures two products, B and C. Using data from Example 7 in Section 1.3, we construct a "unit cost" matrix, $U = [\,\mathbf{b} \;\; \mathbf{c}\,]$, whose columns describe the "costs per dollar of output" for the products:

$$U = \begin{bmatrix} .45 & .40 \\ .25 & .30 \\ .15 & .15 \end{bmatrix} \begin{matrix} \text{Materials} \\ \text{Labor} \\ \text{Overhead} \end{matrix}$$

Let $\mathbf{x} = (x_1, x_2)$ be a "production" vector, corresponding to $x_1$ dollars of product B and $x_2$ dollars of product C, and define $T : \mathbb{R}^2 \to \mathbb{R}^3$ by $T(\mathbf{x}) = U\mathbf{x}$.

1. **讀懂矩陣**:第一行是產品 B 每一元的成本 $(.45, .25, .15)$,第二行是產品 C 的 $(.40, .30, .15)$;三列分別是材料、人工、管理費。
2. **$T$ 在做什麼**:把「產量清單」$(x_1, x_2)$ 變成「成本清單」(材料、人工、管理費三項的總額):
   $$T(\mathbf{x}) = U\mathbf{x} = x_1\begin{bmatrix} .45 \\ .25 \\ .15 \end{bmatrix} + x_2\begin{bmatrix} .40 \\ .30 \\ .15 \end{bmatrix}$$
3. **線性表現在兩件事上(課本的兩句話)**:產量變 4 倍,成本也變 4 倍——$T(4\mathbf{x}) = 4T(\mathbf{x})$。
4. **第二件**:兩張訂單合併生產的總成本,等於兩張訂單各自成本相加——$T(\mathbf{x} + \mathbf{y}) = T(\mathbf{x}) + T(\mathbf{y})$。
5. **重點**:線性變換不一定是幾何的。這裡它把一種資料(產量)變成另一種資料(成本)。

#### 備註
這一題和第 2 週觀念 6 的 Example 7 是同一組數字,可以直接回顧:當時只算「乘出來多少」,現在多了「這個對應是線性的」這個觀點。

## 易錯點
- 以為「$T(\mathbf{0}) = \mathbf{0}$」就足以保證線性。它只是必要條件(Exercise 40:$T(x_1, x_2) = (4x_1 - 2x_2, 3|x_2|)$ 滿足 $T(\mathbf{0}) = \mathbf{0}$ 卻不線性)。
- 忘記檢查**負的**純量。絕對值、平方這類運算對正數看起來沒問題,對負數就破功。
- 以為平移是線性的。$T(\mathbf{x}) = \mathbf{x} + \mathbf{b}$($\mathbf{b} \neq \mathbf{0}$)**不是**線性(Exercise 38)。
- 把「線性函數 $f(x) = mx + b$」的用法帶進來。微積分說它線性是因為圖形是直線;線代的線性要求 $b = 0$(Exercise 37)。

## 教學提示
先示範捷徑:給三四個變換,只算 $T(\mathbf{0})$,馬上刷掉不是線性的。再說明「$T(\mathbf{0}) = \mathbf{0}$ 不夠」,用 Exercise 40 的絕對值當反例。

例 1 的五個步驟是整學期「證明線性」的模板,建議抄在黑板上不要擦,之後 Exercises 43、44 直接套。

「深度學習為什麼要 ReLU」這個問題很吸引學生:Exercise 44 說兩個線性變換合起來還是線性,所以疊再多層也沒用。

課堂建議做:Exercises 17、19;是非 Exercises 21、22、27、30;Exercises 40 與 41(找出哪裡違反);Exercise 44 當討論題。

## 練習
### 照做 · Lay 1.8 Exercises 17, 19, 20
(17) Let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be a linear transformation that maps $\mathbf{u} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$ into $\begin{bmatrix} 3 \\ 4 \end{bmatrix}$ and maps $\mathbf{v} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$ into $\begin{bmatrix} 1 \\ -5 \end{bmatrix}$. Use the fact that $T$ is linear to find the images under $T$ of $5\mathbf{u}$, $4\mathbf{v}$, and $5\mathbf{u} + 4\mathbf{v}$.

(19) Let $\mathbf{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$, $\mathbf{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $\mathbf{y}_1 = \begin{bmatrix} 2 \\ 5 \end{bmatrix}$, and $\mathbf{y}_2 = \begin{bmatrix} -1 \\ 6 \end{bmatrix}$, and let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be a linear transformation that maps $\mathbf{e}_1$ into $\mathbf{y}_1$ and maps $\mathbf{e}_2$ into $\mathbf{y}_2$. Find the images of $\begin{bmatrix} 5 \\ -3 \end{bmatrix}$ and $\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$.

(20) Let $\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$, $\mathbf{v}_1 = \begin{bmatrix} -3 \\ 5 \end{bmatrix}$, and $\mathbf{v}_2 = \begin{bmatrix} 2 \\ -9 \end{bmatrix}$, and let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be a linear transformation that maps $\mathbf{x}$ into $x_1\mathbf{v}_1 + x_2\mathbf{v}_2$. Find a matrix $A$ such that $T(\mathbf{x})$ is $A\mathbf{x}$ for each $\mathbf{x}$.

#### 解答
(17) 用 (5):$T(5\mathbf{u}) = 5T(\mathbf{u}) = \begin{bmatrix} 15 \\ 20 \end{bmatrix}$;$T(4\mathbf{v}) = 4T(\mathbf{v}) = \begin{bmatrix} 4 \\ -20 \end{bmatrix}$;$T(5\mathbf{u} + 4\mathbf{v}) = 5T(\mathbf{u}) + 4T(\mathbf{v}) = \begin{bmatrix} 19 \\ 0 \end{bmatrix}$(書後解答相同)。

(19) $\begin{bmatrix} 5 \\ -3 \end{bmatrix} = 5\mathbf{e}_1 - 3\mathbf{e}_2$,所以像是 $5\mathbf{y}_1 - 3\mathbf{y}_2 = \begin{bmatrix} 13 \\ 7 \end{bmatrix}$;一般的 $\mathbf{x}$:$x_1\mathbf{y}_1 + x_2\mathbf{y}_2 = \begin{bmatrix} 2x_1 - x_2 \\ 5x_1 + 6x_2 \end{bmatrix}$(書後解答相同)。

(20) $T(\mathbf{x}) = x_1\mathbf{v}_1 + x_2\mathbf{v}_2 = [\,\mathbf{v}_1 \;\; \mathbf{v}_2\,]\mathbf{x}$,所以 $A = \begin{bmatrix} -3 & 2 \\ 5 & -9 \end{bmatrix}$。

#### 備註
Exercise 19、20 已經是下一個觀念 Theorem 10 的雛形:知道 $T(\mathbf{e}_1)$、$T(\mathbf{e}_2)$,就知道 $T$ 的全部。課本 Exercise 20 把第二個向量也印成 $\mathbf{v}_1$,顯然是 $\mathbf{v}_2$ 的誤植。

### 是非 · Lay 1.8 Exercise 21
**(T/F)** A linear transformation is a special type of function.

#### 解答
**True.** 變換就是函數;線性變換是額外滿足 (i)(ii) 的那一種。

### 是非 · Lay 1.8 Exercise 22
**(T/F)** Every matrix transformation is a linear transformation.

#### 解答
**True.** 由第 2 週的 Theorem 5,$A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}$、$A(c\mathbf{u}) = cA\mathbf{u}$,正是 (i)(ii)(課本 p. 94)。

### 是非 · Lay 1.8 Exercise 27
**(T/F)** Every linear transformation is a matrix transformation.

#### 解答
**False**(就本節的一般情形而言)。課本明說:第 4、5 章會看到**不是**矩陣變換的重要線性變換(例如多項式的微分)。

#### 備註
但要小心:若把範圍限定在 $T : \mathbb{R}^n \to \mathbb{R}^m$,下一個觀念的 Theorem 10 會說每個線性變換**都是**矩陣變換。這題問的是一般的線性變換,所以答案是 False。

### 是非 · Lay 1.8 Exercise 28
**(T/F)** A linear transformation preserves the operations of vector addition and scalar multiplication.

#### 解答
**True.** 這正是定義裡 (i)(ii) 兩個條件的白話說法(課本 p. 94)。

### 是非 · Lay 1.8 Exercise 29
**(T/F)** A transformation $T$ is linear if and only if $T(c_1\mathbf{v}_1 + c_2\mathbf{v}_2) = c_1T(\mathbf{v}_1) + c_2T(\mathbf{v}_2)$ for all $\mathbf{v}_1$ and $\mathbf{v}_2$ in the domain of $T$ and for all scalars $c_1$ and $c_2$.

#### 解答
**True.** 線性 ⇒ 性質 (4);反過來,取 $c_1 = c_2 = 1$ 得 (i),取 $c_2 = 0$ 得 (ii)(課本 p. 94)。

### 是非 · Lay 1.8 Exercise 30
**(T/F)** The superposition principle is a physical description of a linear transformation.

#### 解答
**True.** 工程與物理把性質 (5) 叫做疊加原理:輸入是幾個訊號的線性組合時,反應就是各自反應的同一個線性組合(課本 p. 95)。

### 變化 · Lay 1.8 Exercise 18
The figure shows vectors $\mathbf{u}$, $\mathbf{v}$, and $\mathbf{w}$, along with the images $T(\mathbf{u})$ and $T(\mathbf{v})$ under the action of a linear transformation $T : \mathbb{R}^2 \to \mathbb{R}^2$. Copy this figure carefully, and draw the image $T(\mathbf{w})$ as accurately as possible. [*Hint:* First, write $\mathbf{w}$ as a linear combination of $\mathbf{u}$ and $\mathbf{v}$.]

![Exercise 18:左圖是 u、v、w,右圖是 T(u) 與 T(v)。](ex18-vectors.svg)

#### 解答
先把 $\mathbf{w}$ 寫成組合:從圖上看,$\mathbf{u}$ 的水平部分剛好是 $|\mathbf{v}|$ 的兩倍、$\mathbf{w}$ 和 $\mathbf{u}$ 一樣高,所以
$$\mathbf{w} = \mathbf{u} + 2\mathbf{v}.$$
由線性(性質 4):
$$T(\mathbf{w}) = T(\mathbf{u}) + 2T(\mathbf{v}).$$
畫法:在右圖畫出 $2T(\mathbf{v})$(把 $T(\mathbf{v})$ 延長一倍),再以 $T(\mathbf{u})$ 和 $2T(\mathbf{v})$ 作平行四邊形,對角線就是 $T(\mathbf{w})$——一個指向右上方、比 $T(\mathbf{v})$ 更遠的向量。

#### 備註
這題的重點是「**先在左圖找組合,再把同樣的權重用到右圖**」,不需要知道 $T$ 的矩陣。

### 變化 · Lay 1.8 Exercise 31
Let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be the linear transformation that reflects each point through the $x_1$-axis. (See Practice Problem 2.) Make two sketches similar to Figure 6 that illustrate properties (i) and (ii) of a linear transformation.

#### 解答
$T(x_1, x_2) = (x_1, -x_2)$,矩陣是 $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$。

**圖 1(性質 (i))**:取 $\mathbf{u} = (1, 2)$、$\mathbf{v} = (3, 1)$,則 $\mathbf{u} + \mathbf{v} = (4, 3)$;畫出 $\mathbf{0}, \mathbf{u}, \mathbf{u} + \mathbf{v}, \mathbf{v}$ 的平行四邊形。它對 $x_1$ 軸的鏡像 $\mathbf{0}, (1, -2), (4, -3), (3, -1)$ 仍是平行四邊形,所以 $T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$。

**圖 2(性質 (ii))**:取 $\mathbf{u} = (1, 2)$ 與 $2\mathbf{u} = (2, 4)$ 在同一條通過原點的直線上;它們的像 $(1, -2)$、$(2, -4)$ 也在一條通過原點的直線上,而且 $T(2\mathbf{u}) = 2T(\mathbf{u})$。

### 變化 · Lay 1.8 Exercises 40–41
Column vectors are written as rows, such as $\mathbf{x} = (x_1, x_2)$, and $T(\mathbf{x})$ is written as $T(x_1, x_2)$.

(40) Show that the transformation $T$ defined by $T(x_1, x_2) = (4x_1 - 2x_2,\ 3|x_2|)$ is not linear.

(41) Show that the transformation $T$ defined by $T(x_1, x_2) = (2x_1 - 3x_2,\ x_1 + 4,\ 5x_2)$ is not linear.

#### 解答
(40) 取 $c = -1$、$\mathbf{u} = (0, 1)$:$T(\mathbf{u}) = (-2, 3)$,所以 $-T(\mathbf{u}) = (2, -3)$;但 $T(-\mathbf{u}) = T(0, -1) = (2, 3) \neq (2, -3)$。條件 (ii) 不成立,**不是**線性。(絕對值遇到負數就破功。)

(41) $T(0, 0) = (0, 4, 0) \neq \mathbf{0}$,但線性變換一定把 $\mathbf{0}$ 送到 $\mathbf{0}$(性質 3),所以**不是**線性(書後解答用的正是這個理由)。

#### 備註
兩題示範兩種拆解法:(41) 用 $T(\mathbf{0})$ 一秒判斷;(40) 的 $T(\mathbf{0}) = \mathbf{0}$,必須找負數的反例。

### 變化 · Lay 1.8 Exercises 43–44
(43) Let $T : \mathbb{R}^3 \to \mathbb{R}^3$ be the transformation that reflects each vector $\mathbf{x} = (x_1, x_2, x_3)$ through the plane $x_3 = 0$ onto $T(\mathbf{x}) = (x_1, x_2, -x_3)$. Show that $T$ is a linear transformation. [See Example 4 for ideas.]

(44) Let $T : \mathbb{R}^3 \to \mathbb{R}^3$ be the transformation that projects each vector $\mathbf{x} = (x_1, x_2, x_3)$ onto the plane $x_2 = 0$, so $T(\mathbf{x}) = (x_1, 0, x_3)$. Show that $T$ is a linear transformation.

#### 解答
兩題都照例 1 的模板:取 $\mathbf{u}, \mathbf{v}$ 與純量 $c, d$,直接算 $T(c\mathbf{u} + d\mathbf{v})$。

(43) $c\mathbf{u} + d\mathbf{v} = (cu_1 + dv_1,\ cu_2 + dv_2,\ cu_3 + dv_3)$,所以
$$T(c\mathbf{u} + d\mathbf{v}) = (cu_1 + dv_1,\ cu_2 + dv_2,\ -(cu_3 + dv_3)) = c(u_1, u_2, -u_3) + d(v_1, v_2, -v_3) = cT(\mathbf{u}) + dT(\mathbf{v})$$
滿足 (4),所以線性(書後解答相同)。也可以直接說:$T(\mathbf{x}) = \operatorname{diag}(1, 1, -1)\mathbf{x}$ 是矩陣變換。

(44) 同樣地 $T(c\mathbf{u} + d\mathbf{v}) = (cu_1 + dv_1,\ 0,\ cu_3 + dv_3) = cT(\mathbf{u}) + dT(\mathbf{v})$,線性。矩陣是 $\operatorname{diag}(1, 0, 1)$。

### 挑戰 · Lay 1.8 Practice Problem 3
The line segment from $\mathbf{0}$ to a vector $\mathbf{u}$ is the set of points of the form $t\mathbf{u}$, where $0 \le t \le 1$. Show that a linear transformation $T$ maps this segment into the segment between $\mathbf{0}$ and $T(\mathbf{u})$.

#### 解答
設 $\mathbf{x} = t\mathbf{u}$,$0 \le t \le 1$。由線性,$T(t\mathbf{u}) = tT(\mathbf{u})$,而 $0 \le t \le 1$ 沒有變,所以像落在 $\mathbf{0}$ 與 $T(\mathbf{u})$ 之間的線段上(課本 p. 99)。

### 挑戰 · Lay 1.8 Exercises 32–34
(32) Suppose vectors $\mathbf{v}_1, \dots, \mathbf{v}_p$ span $\mathbb{R}^n$, and let $T : \mathbb{R}^n \to \mathbb{R}^n$ be a linear transformation. Suppose $T(\mathbf{v}_i) = \mathbf{0}$ for $i = 1, \dots, p$. Show that $T$ is the zero transformation. That is, show that if $\mathbf{x}$ is any vector in $\mathbb{R}^n$, then $T(\mathbf{x}) = \mathbf{0}$.

(33) Given $\mathbf{v} \neq \mathbf{0}$ and $\mathbf{p}$ in $\mathbb{R}^n$, the line through $\mathbf{p}$ in the direction of $\mathbf{v}$ has the parametric equation $\mathbf{x} = \mathbf{p} + t\mathbf{v}$. Show that a linear transformation $T : \mathbb{R}^n \to \mathbb{R}^n$ maps this line onto another line or onto a single point (a *degenerate line*).

(34) Let $\mathbf{u}$ and $\mathbf{v}$ be linearly independent vectors in $\mathbb{R}^3$, and let $P$ be the plane through $\mathbf{u}$, $\mathbf{v}$, and $\mathbf{0}$. The parametric equation of $P$ is $\mathbf{x} = s\mathbf{u} + t\mathbf{v}$ (with $s, t$ in $\mathbb{R}$). Show that a linear transformation $T : \mathbb{R}^3 \to \mathbb{R}^3$ maps $P$ onto a plane through $\mathbf{0}$, or onto a line through $\mathbf{0}$, or onto just the origin in $\mathbb{R}^3$. What must be true about $T(\mathbf{u})$ and $T(\mathbf{v})$ in order for the image of the plane $P$ to be a plane?

#### 解答
(32) 任取 $\mathbf{x}$。因為 $\mathbf{v}_1, \dots, \mathbf{v}_p$ 生成 ℝⁿ,可以寫 $\mathbf{x} = c_1\mathbf{v}_1 + \cdots + c_p\mathbf{v}_p$。由 (5),$T(\mathbf{x}) = c_1T(\mathbf{v}_1) + \cdots + c_pT(\mathbf{v}_p) = \mathbf{0}$。

(33) $T(\mathbf{p} + t\mathbf{v}) = T(\mathbf{p}) + tT(\mathbf{v})$。若 $T(\mathbf{v}) \neq \mathbf{0}$,像是通過 $T(\mathbf{p})$、方向為 $T(\mathbf{v})$ 的直線;若 $T(\mathbf{v}) = \mathbf{0}$,整條線都被送到單一點 $T(\mathbf{p})$(書後提示:證明像可以寫成直線的參數式)。

(34) $T(s\mathbf{u} + t\mathbf{v}) = sT(\mathbf{u}) + tT(\mathbf{v})$,所以 $P$ 的像是 $\operatorname{Span}\{T(\mathbf{u}), T(\mathbf{v})\}$:兩者線性獨立時是通過 $\mathbf{0}$ 的平面;相依但不全為 $\mathbf{0}$ 時是通過 $\mathbf{0}$ 的直線;兩者都是 $\mathbf{0}$ 時只剩原點。要成為平面的條件就是 $\{T(\mathbf{u}), T(\mathbf{v})\}$ **線性獨立**。

### 挑戰 · Lay 1.8 Exercises 35–36
(35) **a.** Show that the line through vectors $\mathbf{p}$ and $\mathbf{q}$ in $\mathbb{R}^n$ may be written in the parametric form $\mathbf{x} = (1 - t)\mathbf{p} + t\mathbf{q}$. (Refer to the figure with Exercises 25 and 26 in Section 1.5.) **b.** The line segment from $\mathbf{p}$ to $\mathbf{q}$ is the set of points of the form $(1 - t)\mathbf{p} + t\mathbf{q}$ for $0 \le t \le 1$. Show that a linear transformation $T$ maps this line segment onto a line segment or onto a single point.

(36) Let $\mathbf{u}$ and $\mathbf{v}$ be vectors in $\mathbb{R}^n$. It can be shown that the set $P$ of all points in the parallelogram determined by $\mathbf{u}$ and $\mathbf{v}$ has the form $a\mathbf{u} + b\mathbf{v}$, for $0 \le a \le 1$, $0 \le b \le 1$. Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation. Explain why the image of a point in $P$ under the transformation $T$ lies in the parallelogram determined by $T(\mathbf{u})$ and $T(\mathbf{v})$.

#### 解答
(35) a. 通過 $\mathbf{p}$、方向 $\mathbf{q} - \mathbf{p}$ 的直線是 $\mathbf{x} = \mathbf{p} + t(\mathbf{q} - \mathbf{p})$,展開整理得 $\mathbf{x} = (1 - t)\mathbf{p} + t\mathbf{q}$(書後解答相同)。

b. 由線性,$T((1 - t)\mathbf{p} + t\mathbf{q}) = (1 - t)T(\mathbf{p}) + tT(\mathbf{q})$。若 $T(\mathbf{p}) \neq T(\mathbf{q})$,依 (a) 這就是 $T(\mathbf{p})$ 到 $T(\mathbf{q})$ 的線段;若相等,則所有像都等於 $T(\mathbf{p})$,是一個點。

(36) $P$ 中的點是 $\mathbf{x} = a\mathbf{u} + b\mathbf{v}$($0 \le a, b \le 1$)。由 (4),$T(\mathbf{x}) = aT(\mathbf{u}) + bT(\mathbf{v})$,權重 $a, b$ **沒有改變**,依定義這正是 $T(\mathbf{u})$、$T(\mathbf{v})$ 決定的平行四邊形裡的點。

#### 備註
Exercise 35 正是觀念 1 例 2 裡「剪切把正方形變成平行四邊形」的理由:線段對應到線段,所以只要看四個頂點。

### 挑戰 · Lay 1.8 Exercises 37–38
(37) Define $f : \mathbb{R} \to \mathbb{R}$ by $f(x) = mx + b$. **a.** Show that $f$ is a linear transformation when $b = 0$. **b.** Find a property of a linear transformation that is violated when $b \neq 0$. **c.** Why is $f$ called a linear function?

(38) An *affine transformation* $T : \mathbb{R}^n \to \mathbb{R}^m$ has the form $T(\mathbf{x}) = A\mathbf{x} + \mathbf{b}$, with $A$ an $m \times n$ matrix and $\mathbf{b}$ in $\mathbb{R}^m$. Show that $T$ is *not* a linear transformation when $\mathbf{b} \neq \mathbf{0}$. (Affine transformations are important in computer graphics.)

#### 解答
(37) a. $b = 0$ 時 $f(x) = mx$,而 $f(cx + dy) = m(cx + dy) = c(mx) + d(my) = cf(x) + df(y)$,滿足 (4),所以線性(書後解答相同)。
b. $b \neq 0$ 時 $f(0) = b \neq 0$,違反 $T(\mathbf{0}) = \mathbf{0}$(性質 3)。
c. 微積分把它叫「線性函數」是因為**圖形是一條直線**,不是因為它是線性變換。

(38) $T(\mathbf{0}) = A\mathbf{0} + \mathbf{b} = \mathbf{b} \neq \mathbf{0}$,違反性質 (3),所以不是線性變換。(也可以看 $T(2\mathbf{x}) = 2A\mathbf{x} + \mathbf{b}$,但 $2T(\mathbf{x}) = 2A\mathbf{x} + 2\mathbf{b}$,兩者不同。)

#### 備註
仿射變換在圖學非常重要:平移就是 $\mathbf{x} \mapsto \mathbf{x} + \mathbf{b}$。因為它不是線性的,圖學才發明「齊次座標」,把平移也寫成矩陣乘法(第 5 週的 2.7)。

### 挑戰 · Lay 1.8 Exercises 39, 42
(39) Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation, and let $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ be a linearly dependent set in $\mathbb{R}^n$. Explain why the set $\{T(\mathbf{v}_1), T(\mathbf{v}_2), T(\mathbf{v}_3)\}$ is linearly dependent.

(42) Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation. Show that if $T$ maps two linearly independent vectors onto a linearly dependent set, then the equation $T(\mathbf{x}) = \mathbf{0}$ has a nontrivial solution. [*Hint:* Suppose $\mathbf{u}$ and $\mathbf{v}$ in $\mathbb{R}^n$ are linearly independent and yet $T(\mathbf{u})$ and $T(\mathbf{v})$ are linearly dependent. Then $c_1T(\mathbf{u}) + c_2T(\mathbf{v}) = \mathbf{0}$ for some weights $c_1$ and $c_2$, not both zero. Use this equation.]

#### 解答
(39) 相依代表存在不全為 0 的 $c_1, c_2, c_3$ 使 $c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + c_3\mathbf{v}_3 = \mathbf{0}$。兩邊作用 $T$,由 (5) 與 (3):
$$c_1T(\mathbf{v}_1) + c_2T(\mathbf{v}_2) + c_3T(\mathbf{v}_3) = T(\mathbf{0}) = \mathbf{0}$$
權重還是那組不全為 0 的數,所以像也相依。

(42) 由假設有不全為 0 的 $c_1, c_2$ 使 $c_1T(\mathbf{u}) + c_2T(\mathbf{v}) = \mathbf{0}$。由線性,$T(c_1\mathbf{u} + c_2\mathbf{v}) = \mathbf{0}$。令 $\mathbf{x} = c_1\mathbf{u} + c_2\mathbf{v}$;因為 $\mathbf{u}, \mathbf{v}$ 獨立且 $c_1, c_2$ 不全為 0,$\mathbf{x} \neq \mathbf{0}$。所以 $T(\mathbf{x}) = \mathbf{0}$ 有非平凡解。

#### 備註
Exercise 42 是下一週(觀念 5)Theorem 11 的預告:$T$ 一對一 ⇔ $T(\mathbf{x}) = \mathbf{0}$ 只有平凡解。

## 驗算
```check
expand(3 * (c * Matrix([x1, x2]) + d * Matrix([x3, x4])) - (c * 3 * Matrix([x1, x2]) + d * 3 * Matrix([x3, x4]))) == zeros(2, 1)
Matrix([[0, -1], [1, 0]]) * Matrix([4, 1]) == Matrix([-1, 4])
Matrix([[0, -1], [1, 0]]) * Matrix([2, 3]) == Matrix([-3, 2])
Matrix([[0, -1], [1, 0]]) * Matrix([6, 4]) == Matrix([-1, 4]) + Matrix([-3, 2])
Matrix([[Rational(45, 100), Rational(40, 100)], [Rational(25, 100), Rational(30, 100)], [Rational(15, 100), Rational(15, 100)]]) * Matrix([x1, x2]) == x1 * Matrix([Rational(45, 100), Rational(25, 100), Rational(15, 100)]) + x2 * Matrix([Rational(40, 100), Rational(30, 100), Rational(15, 100)])
5 * Matrix([3, 4]) + 4 * Matrix([1, -5]) == Matrix([19, 0])
5 * Matrix([2, 5]) - 3 * Matrix([-1, 6]) == Matrix([13, 7])
x1 * Matrix([2, 5]) + x2 * Matrix([-1, 6]) == Matrix([2*x1 - x2, 5*x1 + 6*x2])
Matrix([[-3, 2], [5, -9]]) * Matrix([x1, x2]) == x1 * Matrix([-3, 5]) + x2 * Matrix([2, -9])
(lambda T: T(Matrix([0, -1])) == Matrix([2, 3]) and -T(Matrix([0, 1])) == Matrix([2, -3]))(lambda v: Matrix([4*v[0] - 2*v[1], 3*Abs(v[1])]))
(lambda T: T(Matrix([0, 0])))(lambda v: Matrix([2*v[0] - 3*v[1], v[0] + 4, 5*v[1]])) == Matrix([0, 4, 0])
Matrix([[1, 0], [0, -1]]) * Matrix([4, 3]) == Matrix([[1, 0], [0, -1]]) * Matrix([1, 2]) + Matrix([[1, 0], [0, -1]]) * Matrix([3, 1])
(lambda T: expand(T(c * Matrix([x1, x2, x3]) + d * Matrix([x4, x5, x6])) - (c * T(Matrix([x1, x2, x3])) + d * T(Matrix([x4, x5, x6])))) == zeros(3, 1))(lambda v: Matrix([v[0], v[1], -v[2]]))
diag(1, 0, 1) * Matrix([x1, x2, x3]) == Matrix([x1, 0, x3])
(lambda T: T(zeros(2, 1)))(lambda v: Matrix([[a, b], [c, d]]) * v + Matrix([1, 2])) == Matrix([1, 2])
expand(Matrix([[a, b], [c, d]]) * ((1 - t) * Matrix([x1, x2]) + t * Matrix([x3, x4])) - ((1 - t) * Matrix([[a, b], [c, d]]) * Matrix([x1, x2]) + t * Matrix([[a, b], [c, d]]) * Matrix([x3, x4]))) == zeros(2, 1)
expand(Matrix([x1, x2]) + t * (Matrix([x3, x4]) - Matrix([x1, x2])) - ((1 - t) * Matrix([x1, x2]) + t * Matrix([x3, x4]))) == zeros(2, 1)
expand(2 * Matrix([[a, b], [c, d]]) * Matrix([x1, x2]) + 3 * Matrix([[a, b], [c, d]]) * Matrix([x3, x4]) - Matrix([[a, b], [c, d]]) * (2 * Matrix([x1, x2]) + 3 * Matrix([x3, x4]))) == zeros(2, 1)
Matrix([[1, 1], [1, 1]]) * (Matrix([1, 0]) - Matrix([0, 1])) == zeros(2, 1)
Matrix([1, 0]) - Matrix([0, 1]) != zeros(2, 1)
```
