---
title_en: The Inverse of a Matrix
title_zh: 反矩陣:把動作倒回去
sub: AA⁻¹ = I and A⁻¹A = I
level: mid
source: Lay 2.2
lab_hook: '`np.linalg.inv(A)`、`Matrix.inv()`;但解方程組要用 `solve`,不要先求反矩陣'
---
## 觀念
Matrix algebra provides tools for manipulating matrix equations and creating various useful formulas in ways similar to doing ordinary algebra with real numbers. This section investigates the matrix analogue of the reciprocal, or multiplicative inverse, of a nonzero number.

An $n \times n$ matrix $A$ is said to be **invertible** if there is an $n \times n$ matrix $C$ such that

$$CA = I \quad\text{and}\quad AC = I$$

where $I = I_n$, the $n \times n$ identity matrix. In this case, $C$ is an **inverse** of $A$. In fact, $C$ is uniquely determined by $A$, because if $B$ were another inverse of $A$, then $B = BI = B(AC) = (BA)C = IC = C$. This unique inverse is denoted by $A^{-1}$, so that

$$A^{-1}A = I \quad\text{and}\quad AA^{-1} = I$$

A matrix that is *not* invertible is sometimes called a **singular matrix**, and an invertible matrix is called a **nonsingular matrix**.

**Theorem 4.** Let $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$. If $ad - bc \ne 0$, then $A$ is invertible and

$$A^{-1} = \frac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

If $ad - bc = 0$, then $A$ is not invertible.

The quantity $ad - bc$ is called the **determinant** of $A$, and we write $\det A = ad - bc$.

**Theorem 5.** If $A$ is an invertible $n \times n$ matrix, then for each $\mathbf{b}$ in $\mathbb{R}^n$, the equation $A\mathbf{x} = \mathbf{b}$ has the unique solution $\mathbf{x} = A^{-1}\mathbf{b}$.

**Theorem 6.**

- **a.** If $A$ is an invertible matrix, then $A^{-1}$ is invertible and $(A^{-1})^{-1} = A$.
- **b.** If $A$ and $B$ are $n \times n$ invertible matrices, then so is $AB$, and the inverse of $AB$ is the product of the inverses of $A$ and $B$ in the reverse order. That is, $(AB)^{-1} = B^{-1}A^{-1}$.
- **c.** If $A$ is an invertible matrix, then so is $A^T$, and the inverse of $A^T$ is the transpose of $A^{-1}$. That is, $(A^T)^{-1} = (A^{-1})^T$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| invertible | 可逆 | 存在 $C$ 使 $CA = I$ 且 $AC = I$ |
| inverse $A^{-1}$ | 反矩陣 | 唯一的那個 $C$;讀作「A inverse」 |
| singular matrix | 奇異矩陣 | 不可逆的矩陣 |
| nonsingular matrix | 非奇異矩陣 | 可逆的矩陣(同一件事的另一個說法) |
| determinant $\det A$ | 行列式 | $2 \times 2$ 時是 $ad - bc$;為 0 就不可逆 |
| reverse order | 反序 | $(AB)^{-1} = B^{-1}A^{-1}$ |
| flexibility matrix | 柔度矩陣 | 課本 Example 3:施力 → 變形 |
| stiffness matrix | 剛度矩陣 | 柔度矩陣的反矩陣:變形 → 需要的力 |

## 白話說
**反矩陣就是「把動作倒回去」的那台機器。** 先做 $A$ 再做 $A^{-1}$,等於什麼都沒做($I$)。

數字的世界裡,$5$ 的倒數是 $1/5$,因為 $5 \times \tfrac15 = 1$。矩陣的世界要小心三件事:

1. **不能寫成除法**。沒有 $\dfrac{B}{A}$ 這種寫法,因為乘法不可交換,「除以 $A$」到底是左乘還是右乘 $A^{-1}$ 會得到不同答案。
2. **兩個方向都要驗**:定義要求 $CA = I$ **而且** $AC = I$。
3. **只有方陣才可能可逆**。$3 \times 2$ 的矩陣沒有反矩陣(最多只有單邊的,見觀念 5 的 Exercises 47–48)。

**$2 \times 2$ 的公式怎麼記**:主對角線兩個數**對調**,副對角線兩個數**變號**,最後除以 $ad - bc$。

$$\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

**$ad - bc = 0$ 代表什麼**?代表兩行成比例(相依),那台機器把整個平面壓到一條線上——壓扁之後資訊就丟失了,當然倒不回去。

**Theorem 5 是本節的用途**:$A$ 可逆時,$A\mathbf{x} = \mathbf{b}$ 有唯一解 $\mathbf{x} = A^{-1}\mathbf{b}$。注意這只是「理論上的公式」,實務上解方程組不會真的去算反矩陣(見下面的數值筆記)。

**Theorem 6(b) 的反序**:$(AB)^{-1} = B^{-1}A^{-1}$。用穿衣服想:先穿襪子($B$)再穿鞋子($A$);要脫的時候,先脫鞋子($A^{-1}$)再脫襪子($B^{-1}$)。**後做的先解開**。

## 幾何意義
上週把矩陣看成變換:$A$ 是旋轉,$A^{-1}$ 就是轉回來;$A$ 是放大兩倍,$A^{-1}$ 就是縮小一半。

**什麼時候倒不回去?** 當 $A$ 把平面壓扁成一條線(或壓成一個點)的時候。投影矩陣就是典型的例子:一旦投影下去,原本的高度資訊就沒了,不可能還原——所以投影矩陣永遠不可逆。

$\det A$ 正好量了「面積被放大幾倍」($\det$ 的這個意義第 8 週會正式學)。$\det A = 0$ 表示面積被壓成 0,也就是壓扁了。

## 在資工哪裡用
- **解方程組的理論基礎**:$\mathbf{x} = A^{-1}\mathbf{b}$ 是所有「已知輸出反推輸入」問題的統一寫法——電路反推電流、動畫反推關節角度、機器學習的正規方程。
- **圖學的反向變換**:滑鼠點在螢幕上,要知道對應世界座標的哪個位置,就得把整條變換管線倒回去,也就是乘上 $M^{-1}$。遊戲引擎裡的 `Matrix4x4.Inverse()` 就在做這件事。
- **顏色空間互換**:RGB → YIQ 是乘一個矩陣,YIQ → RGB 就是乘它的反矩陣(觀念 6 的 Exercises 21–22)。
- **密碼學的直覺**:可逆 = 能解密。把訊息乘上 $A$ 加密,收件人乘 $A^{-1}$ 解密(古典的 Hill cipher 正是這樣做的)。
- **$(AB)^{-1} = B^{-1}A^{-1}$ 在程式裡的意義**:撤銷一串操作時,要**反著撤**。這和 undo stack 是同一個道理。

## 實際應用
課本 Example 3 的**彈性樑**:$\mathbf{y} = D\mathbf{f}$,其中 $\mathbf{f}$ 是三個點上施的力、$\mathbf{y}$ 是三個點的變形量。$D$ 叫柔度矩陣(flexibility matrix),它的第 $j$ 行是「只在第 $j$ 點施一單位力時,三個點各自變形多少」。

反過來,$D^{-1}$ 叫剛度矩陣(stiffness matrix),它的第 $j$ 行是「想讓第 $j$ 點恰好變形一單位、其他點完全不動,三個點各要施多少力」。這一行裡通常有負數——代表某些點必須**往上拉**,才能讓變形只集中在一個點。土木、機械的有限元素分析就是這樣算的(練習 Exercises 49–52)。

## 數值筆記
課本 2.2 的 Numerical Note 說得很直接:

> 實務上很少真的去算 $A^{-1}$,除非你就是需要 $A^{-1}$ 的每一格。算出 $A^{-1}$ 再算 $A^{-1}\mathbf{b}$,所需的運算量大約是**直接用列化簡解 $A\mathbf{x} = \mathbf{b}$ 的三倍**,而且列化簡通常更準確。

所以程式裡的規矩是:**要解方程組就用 `np.linalg.solve(A, b)`,不要寫 `np.linalg.inv(A) @ b`。** 這是本週實作課要驗證的重點之一,第 6 週講 LU 分解時會看到更深的理由。

## 合理性檢查
算完 $A^{-1}$ 之後,**乘回去檢查**(課本 2.2 的 Reasonable Answers):

$$AA^{-1} \stackrel{?}{=} I$$

課本特別說明:對可逆方陣而言,驗一個方向就夠了,不必兩邊都乘。

$2 \times 2$ 還有個更快的檢查法:看 $\det A^{-1}$ 是不是 $\dfrac{1}{\det A}$。

## 原理
**反矩陣為什麼唯一?**(課本 p. 135)假設 $B$ 和 $C$ 都是 $A$ 的反矩陣,那麼
$$B = BI = B(AC) = (BA)C = IC = C.$$
中間只用到結合律。所以「$A$ 的反矩陣」這種說法才合法,可以寫成 $A^{-1}$。

**Theorem 5 的證明**(課本 p. 136):
*存在性*:把 $A^{-1}\mathbf{b}$ 代進去,$A(A^{-1}\mathbf{b}) = (AA^{-1})\mathbf{b} = I\mathbf{b} = \mathbf{b}$,確實是解。
*唯一性*:若 $A\mathbf{u} = \mathbf{b}$,兩邊左乘 $A^{-1}$ 得 $A^{-1}A\mathbf{u} = A^{-1}\mathbf{b}$,即 $\mathbf{u} = A^{-1}\mathbf{b}$。所以任何解都等於這一個。∎

**Theorem 6(b) 的證明**(課本 p. 138):要證 $B^{-1}A^{-1}$ 是 $AB$ 的反矩陣,就**照定義驗**:
$$(AB)(B^{-1}A^{-1}) = A(BB^{-1})A^{-1} = AIA^{-1} = AA^{-1} = I$$
同樣可算出 $(B^{-1}A^{-1})(AB) = I$。∎

課本在這裡加了一段很值得唸給學生聽的提醒:**定理只是宣稱 $B^{-1}A^{-1}$ 是反矩陣,證明的方式就是去驗證它滿足「反矩陣」的定義**。這是「用定義證明」的標準示範。

**Theorem 4 的證明**(Exercises 35–36):若 $ad - bc \ne 0$,直接把公式乘開驗證即可;若 $ad - bc = 0$,取 $\mathbf{x} = \begin{bmatrix} -b \\ a \end{bmatrix}$(或 $a = b = 0$ 時取 $\begin{bmatrix} -d \\ c \end{bmatrix}$),可以算出 $A\mathbf{x} = \mathbf{0}$ 而 $\mathbf{x} \ne \mathbf{0}$,於是 $A\mathbf{x} = \mathbf{0}$ 有不只一個解,由 Theorem 5 知 $A$ 不可逆。

## 老師講解
### 例 1 · Lay 2.2 Examples 1–2
If $A = \begin{bmatrix} 2 & 5 \\ -3 & -7 \end{bmatrix}$ and $C = \begin{bmatrix} -7 & -5 \\ 3 & 2 \end{bmatrix}$, show that $C = A^{-1}$. Then find the inverse of $A = \begin{bmatrix} 3 & 4 \\ 5 & 6 \end{bmatrix}$.

1. **驗證第一組:兩個方向都乘**。
   $$AC = \begin{bmatrix} 2 & 5 \\ -3 & -7 \end{bmatrix}\begin{bmatrix} -7 & -5 \\ 3 & 2 \end{bmatrix} = \begin{bmatrix} -14 + 15 & -10 + 10 \\ 21 - 21 & 15 - 14 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$
2. 同樣算出 $CA = I$。兩式都成立,所以 $C = A^{-1}$。
3. **第二組用公式**。先算行列式:$\det A = 3(6) - 4(5) = 18 - 20 = -2$。不是 0,所以可逆。
4. **套公式**:主對角線對調(3 和 6 交換)、副對角線變號(4 和 5 變 $-4$、$-5$),再除以 $-2$:
   $$A^{-1} = \frac{1}{-2}\begin{bmatrix} 6 & -4 \\ -5 & 3 \end{bmatrix} = \begin{bmatrix} -3 & 2 \\ 5/2 & -3/2 \end{bmatrix}$$
5. **檢查**:$\begin{bmatrix} 3 & 4 \\ 5 & 6 \end{bmatrix}\begin{bmatrix} -3 & 2 \\ 5/2 & -3/2 \end{bmatrix} = \begin{bmatrix} -9 + 10 & 6 - 6 \\ -15 + 15 & 10 - 9 \end{bmatrix} = I$。✓
6. **常見錯誤提醒**:$-2$ 是分母,所以每一格都要除;學生常常只除第一格。

### 例 2 · Lay 2.2 Example 4
Use the inverse of the matrix $A = \begin{bmatrix} 3 & 4 \\ 5 & 6 \end{bmatrix}$ in Example 2 to solve the system

$$\begin{aligned} 3x_1 + 4x_2 &= 3 \\ 5x_1 + 6x_2 &= 7 \end{aligned}$$

1. **先寫成矩陣方程**:$A\mathbf{x} = \mathbf{b}$,其中 $\mathbf{b} = \begin{bmatrix} 3 \\ 7 \end{bmatrix}$。
2. **$A$ 可逆(例 1 算過),用 Theorem 5**:$\mathbf{x} = A^{-1}\mathbf{b}$。
3. **代進去**:
   $$\mathbf{x} = \begin{bmatrix} -3 & 2 \\ 5/2 & -3/2 \end{bmatrix}\begin{bmatrix} 3 \\ 7 \end{bmatrix} = \begin{bmatrix} -9 + 14 \\ 7.5 - 10.5 \end{bmatrix} = \begin{bmatrix} 5 \\ -3 \end{bmatrix}$$
4. **代回原方程檢查**:$3(5) + 4(-3) = 15 - 12 = 3$ ✓、$5(5) + 6(-3) = 25 - 18 = 7$ ✓。
5. **但要講清楚**:這招在 $2 \times 2$ 時很方便(可以心算),$3 \times 3$ 以上就不划算了。課本明說「這個公式在數值計算上很少用,因為列化簡 $[\,A \;\; \mathbf{b}\,]$ 幾乎總是比較快,而且更準」。
6. **第 6 週會看到真正的做法**(LU 分解):把 $A$ 拆成兩個三角矩陣,解一次拆解、解很多個 $\mathbf{b}$。

### 例 3 · Lay 2.2 Example 3
A horizontal elastic beam is supported at each end and is subjected to forces at points 1, 2, and 3. Let $\mathbf{f}$ in $\mathbb{R}^3$ list the forces at these points, and let $\mathbf{y}$ in $\mathbb{R}^3$ list the amounts of deflection (that is, movement) of the beam at the three points. Using Hooke's law from physics, it can be shown that

$$\mathbf{y} = D\mathbf{f}$$

where $D$ is a *flexibility matrix*. Its inverse is called the *stiffness matrix*. Describe the physical significance of the columns of $D$ and $D^{-1}$.

1. **先問「行是什麼意思」**。用上週的老招:$D = DI_3 = [\,D\mathbf{e}_1 \;\; D\mathbf{e}_2 \;\; D\mathbf{e}_3\,]$。
2. **解讀 $\mathbf{e}_1$**:$\mathbf{e}_1 = (1, 0, 0)$ 代表「只在第 1 點施一單位力,其他點不施力」。那麼 $D\mathbf{e}_1$(也就是 $D$ 的第一行)就是**在第 1 點施一單位力時,三個點各自的變形量**。
3. 第二、三行同理。所以**柔度矩陣的每一行 = 一個施力點造成的變形分布**。
4. **反過來看 $D^{-1}$**。因為 $\mathbf{f} = D^{-1}\mathbf{y}$,同樣的技巧:$D^{-1} = [\,D^{-1}\mathbf{e}_1 \;\; D^{-1}\mathbf{e}_2 \;\; D^{-1}\mathbf{e}_3\,]$。
5. **這次把 $\mathbf{e}_1$ 讀成變形**:「第 1 點變形一單位、其他兩點完全不動」。那麼 $D^{-1}$ 的第一行就是**要達成這種變形所需的三個力**。
6. **為什麼會有負數**:要讓變形只集中在一個點、旁邊兩點紋風不動,旁邊必須有力**往上拉**住。所以每一行裡通常有一兩個負數。
7. **這題的價值**:它示範了「把矩陣的行解讀成物理意義」這個通用技巧——先問「$\mathbf{e}_j$ 在這個情境裡是什麼意思」,再問「$M\mathbf{e}_j$ 是什麼意思」。

#### 備註
例 3 沒有算式,全部是解讀,很適合當作「數學在工程裡怎麼用」的示範。時間不夠時可以只講到第 5 步。

練習 Exercises 49–52 都是這個模型的數值版,建議至少做 Exercise 49。

## 易錯點
- **寫出「除以矩陣」**。矩陣代數裡沒有除法,只能左乘或右乘反矩陣,而且左右不同。
- **$(AB)^{-1}$ 寫成 $A^{-1}B^{-1}$**。順序要反過來(Exercises 12–13 就是在考這個)。
- **$2 \times 2$ 公式只除了一格**。$\dfrac{1}{ad-bc}$ 要乘進**整個**矩陣。
- **把 $ad - bc$ 記成 $ab - cd$**。Exercise 15 故意設了這個陷阱。
- **以為 $\det A = 0$ 時「反矩陣是 0」**。不是 0,是**不存在**。
- 在程式裡用 `inv(A) @ b` 解方程組:慢三倍而且比較不準,應該用 `solve(A, b)`。

## 教學提示
這個觀念要講 25 分鐘,建議這樣配:定義與唯一性 5 分鐘、$2 \times 2$ 公式與 $\det$ 10 分鐘(含例 1)、Theorem 5 與例 2 五分鐘、Theorem 6 的反序 5 分鐘。

**$\det$ 這個字第一次出現**,只講 $2 \times 2$ 的情形就好,告訴學生「第 8 週會正式學,現在只要知道它是一個判斷可不可逆的數」。

「穿鞋脫鞋」的比喻對 $(AB)^{-1} = B^{-1}A^{-1}$ 非常有效,建議用。

課堂建議做:Exercises 1、5、7(同一個矩陣從求反、驗證到解方程組,一條龍);是非 Exercises 13、15(兩個典型陷阱);Practice Problem 1(用行列式快速判斷)。Exercises 21–30 是矩陣代數的移項練習,適合當作業,可以挑 25、27、29 三題。

T 題 Exercise 50 與觀念 5 的 Exercises 51–52 放進實作課,連同 `inv` 與 `solve` 的計時比較。

## 練習
### 照做 · Lay 2.2 Exercises 1–4
Find the inverses of the matrices in Exercises 1–4.

(1) $\begin{bmatrix} 8 & 3 \\ 5 & 2 \end{bmatrix}$

(2) $\begin{bmatrix} 5 & 4 \\ 9 & 7 \end{bmatrix}$

(3) $\begin{bmatrix} 8 & 3 \\ -7 & -3 \end{bmatrix}$

(4) $\begin{bmatrix} 3 & -2 \\ 7 & -4 \end{bmatrix}$

#### 解答
(1) $\det = 16 - 15 = 1$,所以 $A^{-1} = \begin{bmatrix} 2 & -3 \\ -5 & 8 \end{bmatrix}$。

(2) $\det = 35 - 36 = -1$,所以 $A^{-1} = \dfrac{1}{-1}\begin{bmatrix} 7 & -4 \\ -9 & 5 \end{bmatrix} = \begin{bmatrix} -7 & 4 \\ 9 & -5 \end{bmatrix}$。

(3) $\det = -24 + 21 = -3$,所以 $A^{-1} = \dfrac{1}{-3}\begin{bmatrix} -3 & -3 \\ 7 & 8 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ -7/3 & -8/3 \end{bmatrix}$。

(4) $\det = -12 + 14 = 2$,所以 $A^{-1} = \dfrac{1}{2}\begin{bmatrix} -4 & 2 \\ -7 & 3 \end{bmatrix} = \begin{bmatrix} -2 & 1 \\ -7/2 & 3/2 \end{bmatrix}$。

#### 備註
四題都是純套公式,但 (3)(4) 的分母是負數或會產生分數,正是學生最容易出錯的地方。建議課堂做 (1)(3),另外兩題當作業。

### 照做 · Lay 2.2 Exercises 5–6
(5) Verify that the inverse you found in Exercise 1 is correct.

(6) Verify that the inverse you found in Exercise 2 is correct.

#### 解答
(5) $\begin{bmatrix} 8 & 3 \\ 5 & 2 \end{bmatrix}\begin{bmatrix} 2 & -3 \\ -5 & 8 \end{bmatrix} = \begin{bmatrix} 16 - 15 & -24 + 24 \\ 10 - 10 & -15 + 16 \end{bmatrix} = I_2$ ✓(反向相乘同樣得 $I_2$)。

(6) $\begin{bmatrix} 5 & 4 \\ 9 & 7 \end{bmatrix}\begin{bmatrix} -7 & 4 \\ 9 & -5 \end{bmatrix} = \begin{bmatrix} -35 + 36 & 20 - 20 \\ -63 + 63 & 36 - 35 \end{bmatrix} = I_2$ ✓。

#### 備註
書後解答只印一個方向的乘積。對方陣來說驗一個方向就足夠(這件事要到第 6 週的可逆矩陣定理才嚴格成立),但本節的定義要求兩式都成立,所以建議要求學生兩邊都乘一次。

這正是課本「合理性檢查」的標準動作:**算完反矩陣一定要乘回去看**。

### 是非 · Lay 2.2 Exercises 11–17
In Exercises 11–20, mark each statement True or False (T/F). Justify each answer.

(11) **(T/F)** In order for a matrix $B$ to be the inverse of $A$, both equations $AB = I$ and $BA = I$ must be true.

(12) **(T/F)** A product of invertible $n \times n$ matrices is invertible, and the inverse of the product is the product of their inverses in the same order.

(13) **(T/F)** If $A$ and $B$ are $n \times n$ and invertible, then $A^{-1}B^{-1}$ is the inverse of $AB$.

(14) **(T/F)** If $A$ is invertible, then the inverse of $A^{-1}$ is $A$ itself.

(15) **(T/F)** If $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ and $ab - cd \ne 0$, then $A$ is invertible.

(16) **(T/F)** If $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ and $ad = bc$, then $A$ is not invertible.

(17) **(T/F)** If $A$ is an invertible $n \times n$ matrix, then the equation $A\mathbf{x} = \mathbf{b}$ is consistent for *each* $\mathbf{b}$ in $\mathbb{R}^n$.

#### 解答
- (11) **True.** 這就是課本 p. 135 的定義,兩式缺一不可。
- (12) **False.** 乘積確實可逆,但反矩陣是**反序**的乘積:$(AB)^{-1} = B^{-1}A^{-1}$。
- (13) **False.** 同上,應該是 $B^{-1}A^{-1}$。
- (14) **True.** Theorem 6(a):$(A^{-1})^{-1} = A$。
- (15) **False.** 條件應該是 $ad - bc \ne 0$。反例:$A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$,此時 $ab - cd = 2 - 8 = -6 \ne 0$,但 $ad - bc = 4 - 4 = 0$,$A$ 不可逆。
- (16) **True.** $ad = bc \iff \det A = 0$,由 Theorem 4 的後半句知不可逆。
- (17) **True.** Theorem 5 保證 $\mathbf{x} = A^{-1}\mathbf{b}$ 一定是解(而且唯一)。

#### 備註
書後解答對 Exercises 11–19 只寫「Write out your answers before checking the *Study Guide*.」,沒有給 T/F;上面的答案是本講義判定的。

(12) 和 (13) 是同一個陷阱的兩種問法(文字版與符號版),(15) 是把下標順序動手腳。這三題最值得當堂做。

### 變化 · Lay 2.2 Exercises 7–8
(7) Use the inverse found in Exercise 1 to solve the system

$$\begin{aligned} 8x_1 + 3x_2 &= 2 \\ 5x_1 + 2x_2 &= -1 \end{aligned}$$

(8) Use the inverse found in Exercise 2 to solve the system

$$\begin{aligned} 5x_1 + 4x_2 &= -3 \\ 9x_1 + 7x_2 &= -5 \end{aligned}$$

#### 解答
(7) $\mathbf{x} = A^{-1}\mathbf{b} = \begin{bmatrix} 2 & -3 \\ -5 & 8 \end{bmatrix}\begin{bmatrix} 2 \\ -1 \end{bmatrix} = \begin{bmatrix} 7 \\ -18 \end{bmatrix}$,即 $x_1 = 7$、$x_2 = -18$。

(8) $\mathbf{x} = \begin{bmatrix} -7 & 4 \\ 9 & -5 \end{bmatrix}\begin{bmatrix} -3 \\ -5 \end{bmatrix} = \begin{bmatrix} 1 \\ -2 \end{bmatrix}$,即 $x_1 = 1$、$x_2 = -2$。

#### 備註
算完一定要代回原方程檢查——這兩題的數字不大,檢查只要 10 秒。

### 變化 · Lay 2.2 Exercise 9
Let $A = \begin{bmatrix} 1 & 2 \\ 5 & 12 \end{bmatrix}$, $\mathbf{b}_1 = \begin{bmatrix} -1 \\ 3 \end{bmatrix}$, $\mathbf{b}_2 = \begin{bmatrix} 1 \\ -5 \end{bmatrix}$, $\mathbf{b}_3 = \begin{bmatrix} 2 \\ 6 \end{bmatrix}$, and $\mathbf{b}_4 = \begin{bmatrix} 3 \\ 5 \end{bmatrix}$.

- **a.** Find $A^{-1}$, and use it to solve the four equations $A\mathbf{x} = \mathbf{b}_1$, $A\mathbf{x} = \mathbf{b}_2$, $A\mathbf{x} = \mathbf{b}_3$, $A\mathbf{x} = \mathbf{b}_4$
- **b.** The four equations in part (a) can be solved by the same set of row operations, since the coefficient matrix is the same in each case. Solve the four equations in part (a) by row reducing the augmented matrix $[\,A \;\; \mathbf{b}_1 \;\; \mathbf{b}_2 \;\; \mathbf{b}_3 \;\; \mathbf{b}_4\,]$

#### 解答
$\det A = 12 - 10 = 2$,所以 $A^{-1} = \dfrac12\begin{bmatrix} 12 & -2 \\ -5 & 1 \end{bmatrix} = \begin{bmatrix} 6 & -1 \\ -5/2 & 1/2 \end{bmatrix}$。

**a.** 四個解依序是
$$\begin{bmatrix} -9 \\ 4 \end{bmatrix}, \quad \begin{bmatrix} 11 \\ -5 \end{bmatrix}, \quad \begin{bmatrix} 6 \\ -2 \end{bmatrix}, \quad \begin{bmatrix} 13 \\ -5 \end{bmatrix}$$

**b.** 把四個右端並排,一次列化簡:
$$\begin{bmatrix} 1 & 2 & -1 & 1 & 2 & 3 \\ 5 & 12 & 3 & -5 & 6 & 5 \end{bmatrix} \sim \begin{bmatrix} 1 & 0 & -9 & 11 & 6 & 13 \\ 0 & 1 & 4 & -5 & -2 & -5 \end{bmatrix}$$
最後四行就是四個解,和 (a) 相同。

#### 備註
這題是本節最重要的一題:**同一個係數矩陣、很多個右端向量時,把它們並排一次消去,比算反矩陣快**。這正是第 6 週 LU 分解的動機,也是 Numerical Note 那句「算反矩陣大約要三倍運算量」的具體版本。

一定要讓學生兩種方法都做一次,再問「哪一種比較省事?」

### 變化 · Lay 2.2 Practice Problem 1
Use determinants to determine which of the following matrices are invertible.

- **a.** $\begin{bmatrix} 3 & -9 \\ 2 & 6 \end{bmatrix}$
- **b.** $\begin{bmatrix} 4 & -9 \\ 0 & 5 \end{bmatrix}$
- **c.** $\begin{bmatrix} 6 & -9 \\ -4 & 6 \end{bmatrix}$

#### 解答
- **a.** $\det = 3(6) - (-9)(2) = 18 + 18 = 36 \ne 0$ → **可逆**
- **b.** $\det = 4(5) - (-9)(0) = 20 \ne 0$ → **可逆**
- **c.** $\det = 6(6) - (-9)(-4) = 36 - 36 = 0$ → **不可逆**

#### 備註
(c) 的兩行成比例($\begin{bmatrix} 6 \\ -4 \end{bmatrix}$ 與 $\begin{bmatrix} -9 \\ 6 \end{bmatrix}$ 差 $-\tfrac32$ 倍),所以行線性相依。可以順便把「$\det = 0$ ⇔ 兩行成比例」講一次,替第 8 週鋪路。

### 應用 · Lay 2.2 Exercises 49–50
(49) Let $D = \begin{bmatrix} .005 & .002 & .001 \\ .002 & .004 & .002 \\ .001 & .002 & .005 \end{bmatrix}$ be a flexibility matrix, with flexibility measured in inches per pound. Suppose that forces of 30, 50, and 20 lb are applied at points 1, 2, and 3, respectively, in Figure 1 of Example 3. Find the corresponding deflections.

(50) **(T)** Compute the stiffness matrix $D^{-1}$ for $D$ in Exercise 49. List the forces needed to produce a deflection of .04 in. at point 3, with zero deflections at the other points.

#### 解答
(49) $\mathbf{y} = D\mathbf{f}$,$\mathbf{f} = (30, 50, 20)$:
$$y_1 = .005(30) + .002(50) + .001(20) = .27$$
$$y_2 = .002(30) + .004(50) + .002(20) = .30$$
$$y_3 = .001(30) + .002(50) + .005(20) = .23$$
三點的撓度分別是 **.27、.30、.23 英吋**。

(50) 剛度矩陣
$$D^{-1} = \begin{bmatrix} 250 & -125 & 0 \\ -125 & 375 & -125 \\ 0 & -125 & 250 \end{bmatrix} \quad (\text{lb per inch})$$
所需的力是 $\mathbf{f} = D^{-1}\mathbf{y}$,其中 $\mathbf{y} = (0, 0, .04)$,也就是 $D^{-1}$ 第 3 行的 $.04$ 倍:
$$\mathbf{f} = .04\begin{bmatrix} 0 \\ -125 \\ 250 \end{bmatrix} = \begin{bmatrix} 0 \\ -5 \\ 10 \end{bmatrix}$$
第 1 點不施力、第 2 點 $-5$ lb(**向上拉** 5 磅)、第 3 點 10 lb(向下壓)。

#### 備註
(49) 的題幹提到「Figure 1 of Example 3」,那張圖在課本 p. 137(習題頁沒有重印),備課時要自己翻回去或畫在黑板上:一根兩端支撐的水平樑,三個點各有一個向下的力 $f_i$ 與對應的撓度 $y_i$。

(50) 的負號是重點:要讓變形只出現在第 3 點,第 2 點必須被往上拉住。這正好印證例 3 第 6 步的解讀。

(50) 標 T,放進實作課算。

### 挑戰 · Lay 2.2 Exercises 10、21–24
(10) Use matrix algebra to show that if $A$ is invertible and $D$ satisfies $AD = I$, then $D = A^{-1}$.

(21) Let $A$ be an invertible $n \times n$ matrix, and let $B$ be an $n \times p$ matrix. Show that the equation $AX = B$ has a unique solution $A^{-1}B$.

(22) Let $A$ be an invertible $n \times n$ matrix, and let $B$ be an $n \times p$ matrix. Explain why $A^{-1}B$ can be computed by row reduction: If $[\,A \;\; B\,] \sim \cdots \sim [\,I \;\; X\,]$, then $X = A^{-1}B$. If $A$ is larger than $2 \times 2$, then row reduction of $[\,A \;\; B\,]$ is much faster than computing both $A^{-1}$ and $A^{-1}B$.

(23) Suppose $AB = AC$, where $B$ and $C$ are $n \times p$ matrices and $A$ is invertible. Show that $B = C$. Is this true, in general, when $A$ is not invertible?

(24) Suppose $(B - C)D = 0$, where $B$ and $C$ are $m \times n$ matrices and $D$ is invertible. Show that $B = C$.

#### 解答
- (10) 兩邊左乘 $A^{-1}$:$A^{-1}(AD) = A^{-1}I$,左邊 $= (A^{-1}A)D = ID = D$,所以 $D = A^{-1}$。
- (21) *存在*:$A(A^{-1}B) = (AA^{-1})B = B$。*唯一*:若 $AX = B$,左乘 $A^{-1}$ 得 $X = A^{-1}B$。證法與 Theorem 5 完全平行,只是把向量換成矩陣。
- (22) 把 $[\,A \;\; B\,]$ 化到 $[\,I \;\; X\,]$ 的那串列運算,相當於左乘某個矩陣 $E$(一串基本矩陣的乘積,見觀念 5)。由左半塊得 $EA = I$,所以 $E = A^{-1}$;同一個 $E$ 作用在右半塊就得 $X = EB = A^{-1}B$。
- (23) $AB = AC$ 左乘 $A^{-1}$ 得 $B = C$。$A$ **不可逆時不成立**:第 1 個觀念的 Lay 2.1 Exercise 10 就是反例($AB = AC$ 但 $B \ne C$)。
- (24) 兩邊**右**乘 $D^{-1}$:$(B - C)DD^{-1} = 0$,得 $B - C = 0$,即 $B = C$。注意這次要右乘,因為 $D$ 在右邊。

#### 備註
這五題練的是同一件事:**移項時要分清楚左乘還是右乘**。(24) 特別重要——學生很容易習慣性地左乘,但 $D$ 在右邊就必須右乘。

(22) 是 Numerical Note 的理論說明,也是觀念 5 那個 $[\,A \;\; I\,]$ 演算法的一般版。

### 挑戰 · Lay 2.2 Exercises 25–30
(25) Suppose $A$, $B$, and $C$ are invertible $n \times n$ matrices. Show that $ABC$ is also invertible by producing a matrix $D$ such that $(ABC)D = I$ and $D(ABC) = I$.

(26) Suppose $A$ and $B$ are $n \times n$, $B$ is invertible, and $AB$ is invertible. Show that $A$ is invertible. [*Hint:* Let $C = AB$, and solve this equation for $A$.]

(27) Solve the equation $AB = BC$ for $A$, assuming that $A$, $B$, and $C$ are square and $B$ is invertible.

(28) Suppose $P$ is invertible and $A = PBP^{-1}$. Solve for $B$ in terms of $A$.

(29) If $A$, $B$, and $C$ are $n \times n$ invertible matrices, does the equation $C^{-1}(A + X)B^{-1} = I_n$ have a solution, $X$? If so, find it.

(30) Suppose $A$, $B$, and $X$ are $n \times n$ matrices with $A$, $X$, and $A - AX$ invertible, and suppose

$$(A - AX)^{-1} = X^{-1}B \tag{3}$$

- **a.** Explain why $B$ is invertible.
- **b.** Solve (3) for $X$. If you need to invert a matrix, explain why that matrix is invertible.

#### 解答
- (25) 取 $D = C^{-1}B^{-1}A^{-1}$(反序!)。則 $(ABC)(C^{-1}B^{-1}A^{-1}) = AB(CC^{-1})B^{-1}A^{-1} = A(BB^{-1})A^{-1} = AA^{-1} = I$,另一個方向同理。
- (26) 令 $C = AB$。右乘 $B^{-1}$ 得 $A = CB^{-1}$,是兩個可逆矩陣的乘積,由 Theorem 6(b) 可逆,且 $A^{-1} = B(AB)^{-1}$。
- (27) 右乘 $B^{-1}$:$A = BCB^{-1}$。
- (28) 左乘 $P^{-1}$、右乘 $P$:$B = P^{-1}AP$。
- (29) 有解。左乘 $C$、右乘 $B$ 得 $A + X = CB$,所以 $X = CB - A$。驗證:$C^{-1}(A + CB - A)B^{-1} = C^{-1}CBB^{-1} = I_n$ ✓
- (30) **a.** 由 (3) 左乘 $X$ 得 $B = X(A - AX)^{-1}$,是兩個可逆矩陣的乘積,故 $B$ 可逆。
  **b.** 對 (3) 兩邊取反矩陣:$A - AX = (X^{-1}B)^{-1} = B^{-1}X$。移項得 $A = AX + B^{-1}X = (A + B^{-1})X$。由此式與 $A$、$X$ 可逆,知 $A + B^{-1} = AX^{-1}$ 是可逆矩陣的乘積,故可逆。於是
  $$X = (A + B^{-1})^{-1}A$$

#### 備註
這六題是「矩陣版的移項練習」,難度遞增。(28) 的 $A = PBP^{-1}$ 就是第 11 週「相似矩陣」的樣子,現在先當代數練習。

(30) 明確要求說明「被反的那個矩陣為什麼可逆」——這是嚴謹度的訓練,不能省略。數理弱的班級可以只做 (25)(27)(28)。

### 挑戰 · Lay 2.2 Exercises 35–36 與 Practice Problem 3
Exercises 35 and 36 prove Theorem 4 for $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$.

(35) Show that if $ad - bc = 0$, then the equation $A\mathbf{x} = \mathbf{0}$ has more than one solution. Why does this imply that $A$ is not invertible? [*Hint:* First, consider $a = b = 0$. Then, if $a$ and $b$ are not both zero, consider the vector $\mathbf{x} = \begin{bmatrix} -b \\ a \end{bmatrix}$.]

(36) Show that if $ad - bc \ne 0$, the formula for $A^{-1}$ works.

(Practice Problem 3) If $A$ is an invertible matrix, prove that $5A$ is an invertible matrix.

#### 解答
(35) **情形一:$a = b = 0$。** 此時 $A = \begin{bmatrix} 0 & 0 \\ c & d \end{bmatrix}$。若 $c = d = 0$,任何 $\mathbf{x}$ 都是解;否則取 $\mathbf{x} = \begin{bmatrix} -d \\ c \end{bmatrix} \ne \mathbf{0}$,算得 $A\mathbf{x} = \mathbf{0}$。

**情形二:$a$、$b$ 不全為零。** 取 $\mathbf{x} = \begin{bmatrix} -b \\ a \end{bmatrix} \ne \mathbf{0}$,則
$$A\mathbf{x} = \begin{bmatrix} a(-b) + b(a) \\ c(-b) + d(a) \end{bmatrix} = \begin{bmatrix} 0 \\ ad - bc \end{bmatrix} = \mathbf{0}$$
(最後一步用了 $ad - bc = 0$)。

兩種情形都找到非零解,加上 $\mathbf{x} = \mathbf{0}$ 本身,解不只一個。若 $A$ 可逆,Theorem 5 說 $A\mathbf{x} = \mathbf{0}$ 只有唯一解,矛盾。所以 $A$ 不可逆。

(36) 令 $C = \dfrac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$,直接乘開:
$$AC = \frac{1}{ad-bc}\begin{bmatrix} a & b \\ c & d \end{bmatrix}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix} = \frac{1}{ad-bc}\begin{bmatrix} ad - bc & 0 \\ 0 & ad - bc \end{bmatrix} = I_2$$
同理 $CA = I_2$,所以 $A$ 可逆且 $A^{-1} = C$。

(Practice Problem 3) 設 $C = A^{-1}$,取 $D = \tfrac15 C$。則
$$(5A)\left(\tfrac15 C\right) = 5 \cdot \tfrac15 (AC) = I, \qquad \left(\tfrac15 C\right)(5A) = I$$
所以 $5A$ 可逆,且 $(5A)^{-1} = \tfrac15 A^{-1}$。

#### 備註
Exercises 35–36 合起來就是 Theorem 4 的完整證明,而且兩半用的是完全不同的招數:(36) 直接驗證公式,(35) 用反證(找到非零解 ⇒ 不可能可逆)。適合當「證明的兩種典型寫法」的示範。

Practice Problem 3 很短,可以當堂做,重點是**純量可以搬到乘積外面**(第 1 個觀念的 Theorem 2(d))。

## 驗算
```check
Matrix([[2, 5], [-3, -7]]) * Matrix([[-7, -5], [3, 2]]) == eye(2) == Matrix([[-7, -5], [3, 2]]) * Matrix([[2, 5], [-3, -7]])
Matrix([[3, 4], [5, 6]]).det() == -2
Matrix([[3, 4], [5, 6]]).inv() == Matrix([[-3, 2], [Rational(5,2), Rational(-3,2)]])
Matrix([[-3, 2], [Rational(5,2), Rational(-3,2)]]) * Matrix([3, 7]) == Matrix([5, -3])
Matrix([[8, 3], [5, 2]]).inv() == Matrix([[2, -3], [-5, 8]])
Matrix([[5, 4], [9, 7]]).inv() == Matrix([[-7, 4], [9, -5]])
Matrix([[8, 3], [-7, -3]]).inv() == Matrix([[1, 1], [Rational(-7,3), Rational(-8,3)]])
Matrix([[3, -2], [7, -4]]).inv() == Matrix([[-2, 1], [Rational(-7,2), Rational(3,2)]])
Matrix([[8, 3], [5, 2]]) * Matrix([[2, -3], [-5, 8]]) == eye(2) == Matrix([[2, -3], [-5, 8]]) * Matrix([[8, 3], [5, 2]])
Matrix([[5, 4], [9, 7]]) * Matrix([[-7, 4], [9, -5]]) == eye(2) == Matrix([[-7, 4], [9, -5]]) * Matrix([[5, 4], [9, 7]])
Matrix([[2, -3], [-5, 8]]) * Matrix([2, -1]) == Matrix([7, -18])
Matrix([[-7, 4], [9, -5]]) * Matrix([-3, -5]) == Matrix([1, -2])
Matrix([[1, 2], [5, 12]]).inv() == Matrix([[6, -1], [Rational(-5,2), Rational(1,2)]])
Matrix([[1, 2], [5, 12]]).inv() * Matrix([[-1, 1, 2, 3], [3, -5, 6, 5]]) == Matrix([[-9, 11, 6, 13], [4, -5, -2, -5]])
Matrix([[1, 2, -1, 1, 2, 3], [5, 12, 3, -5, 6, 5]]).rref()[0] == Matrix([[1, 0, -9, 11, 6, 13], [0, 1, 4, -5, -2, -5]])
[Matrix([[3, -9], [2, 6]]).det(), Matrix([[4, -9], [0, 5]]).det(), Matrix([[6, -9], [-4, 6]]).det()] == [36, 20, 0]
Matrix([[1, 2], [2, 4]]).det() == 0 and 1 * 2 - 2 * 4 != 0
Matrix([[5, 2, 1], [2, 4, 2], [1, 2, 5]]) / 1000 * Matrix([30, 50, 20]) == Matrix([Rational(27,100), Rational(3,10), Rational(23,100)])
(Matrix([[5, 2, 1], [2, 4, 2], [1, 2, 5]]) / 1000).inv() == Matrix([[250, -125, 0], [-125, 375, -125], [0, -125, 250]])
(Matrix([[5, 2, 1], [2, 4, 2], [1, 2, 5]]) / 1000).inv() * Matrix([0, 0, Rational(4,100)]) == Matrix([0, -5, 10])
(lambda p, q, r: (p*q*r) * (r.inv()*q.inv()*p.inv()) == eye(2) and (r.inv()*q.inv()*p.inv()) * (p*q*r) == eye(2))(Matrix([[1, 2], [3, 7]]), Matrix([[2, 1], [1, 1]]), Matrix([[0, 1], [1, 1]]))
(lambda q, r: (q*r*q.inv()) * q == q * r)(Matrix([[1, 2], [3, 7]]), Matrix([[0, 1], [1, 1]]))
(lambda p, q: p * (p.inv()*q*p) * p.inv() == q)(Matrix([[1, 2], [3, 7]]), Matrix([[0, 1], [1, 1]]))
(lambda p, q, r: simplify(r.inv() * (p + (r*q - p)) * q.inv()) == eye(2))(Matrix([[0, 1], [1, 1]]), Matrix([[1, 2], [3, 7]]), Matrix([[2, 1], [1, 1]]))
(lambda p, q: (lambda u: (p - p*u).inv() == u.inv()*q)((p + q.inv()).inv() * p))(Matrix([[1, 2], [3, 7]]), Matrix([[2, 0], [0, 3]]))
simplify(Matrix([[a, b], [c, d]]) * Matrix([-b, a]) - Matrix([0, a*d - b*c])) == zeros(2, 1)
simplify(Matrix([[a, b], [c, d]]) * Matrix([[d, -b], [-c, a]]) / (a*d - b*c)) == eye(2)
(5 * Matrix([[3, 4], [5, 6]])).inv() == Matrix([[3, 4], [5, 6]]).inv() / 5
```
