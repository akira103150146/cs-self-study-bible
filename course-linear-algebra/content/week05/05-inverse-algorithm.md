---
title_en: Elementary Matrices and an Algorithm for Finding A⁻¹
title_zh: 基本矩陣與求反矩陣的演算法
sub: Row reduce [A I] to [I A⁻¹]
level: hard
source: Lay 2.2
lab_hook: '`Matrix.hstack(A, eye(n)).rref()` 就是課本的演算法;`np.linalg.inv` 內部做的是 LU'
---
## 觀念
An **elementary matrix** is one that is obtained by performing a single elementary row operation on an identity matrix.

If an elementary row operation is performed on an $m \times n$ matrix $A$, the resulting matrix can be written as $EA$, where the $m \times m$ matrix $E$ is created by performing the same row operation on $I_m$.

Each elementary matrix $E$ is invertible. The inverse of $E$ is the elementary matrix of the same type that transforms $E$ back into $I$.

**Theorem 7.** An $n \times n$ matrix $A$ is invertible if and only if $A$ is row equivalent to $I_n$, and in this case, any sequence of elementary row operations that reduces $A$ to $I_n$ also transforms $I_n$ into $A^{-1}$.

**Algorithm for finding $A^{-1}$.** Row reduce the augmented matrix $[\,A \;\; I\,]$. If $A$ is row equivalent to $I$, then $[\,A \;\; I\,]$ is row equivalent to $[\,I \;\; A^{-1}\,]$. Otherwise, $A$ does not have an inverse.

**Another view of matrix inversion.** Denote the columns of $I_n$ by $\mathbf{e}_1, \dots, \mathbf{e}_n$. Then row reduction of $[\,A \;\; I\,]$ to $[\,I \;\; A^{-1}\,]$ can be viewed as the simultaneous solution of the $n$ systems

$$A\mathbf{x} = \mathbf{e}_1, \quad A\mathbf{x} = \mathbf{e}_2, \quad \dots, \quad A\mathbf{x} = \mathbf{e}_n \tag{2}$$

The columns of $A^{-1}$ are precisely the solutions of the systems in (2). This observation is useful because some applied problems may require finding only one or two columns of $A^{-1}$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| elementary matrix | 基本矩陣 | 對 $I$ 做**一次**列運算得到的矩陣 |
| elementary row operation | 基本列運算 | 換列、某列乘非零數、某列加另一列的倍數 |
| row equivalent to $I_n$ | 與 $I_n$ 列等價 | 可以用列運算化成 $I_n$ |
| augmented matrix $[\,A \;\; I\,]$ | 增廣矩陣 | 把 $A$ 和 $I$ 並排成一個大矩陣 |
| simultaneous solution | 同時求解 | 一次列化簡解掉 $n$ 個方程組 |

## 白話說
**核心想法只有一句:每做一次列運算,等於左乘一個矩陣。**

把 $I$ 拿來做一次列運算(例如第 1、2 列互換),得到的矩陣就叫基本矩陣 $E$。神奇的是:**同一個 $E$ 左乘任何矩陣 $A$,效果就是對 $A$ 做同一次列運算**。

於是「把 $A$ 用列運算化成 $I$」這件事,可以寫成
$$E_p \cdots E_2E_1A = I.$$
也就是說 $E_p \cdots E_1$ 就是 $A^{-1}$!而 $A^{-1} = E_p \cdots E_1 = E_p \cdots E_1 I$——**同一串列運算作用在 $I$ 上,得到的就是 $A^{-1}$**。

這就是演算法的來源:把 $A$ 和 $I$ 並排寫成 $[\,A \;\; I\,]$,一邊化簡一邊「旁觀」右半邊:

$$[\,A \;\; I\,] \;\sim\; \cdots \;\sim\; [\,I \;\; A^{-1}\,]$$

**化不成 $I$ 怎麼辦**?那就表示 $A$ 不可逆,可以直接停手(左半邊出現全零列時就知道了)。

**另一種看法**:上面的過程其實是**同時解 $n$ 個方程組** $A\mathbf{x} = \mathbf{e}_j$。$A^{-1}$ 的第 $j$ 行就是第 $j$ 個方程組的解。所以如果只要 $A^{-1}$ 的某一行,只要解那一個方程組就好(Exercises 45–46)。

## 在資工哪裡用
- **只要一行的時候不必算整個反矩陣**。工程上常常只需要 $A^{-1}$ 的某一行(例如「只讓第 3 個點變形」需要哪些力),解一個方程組就夠,成本是 $1/n$。
- **基本矩陣 = 列運算的「程式化」**。把一連串人工操作變成矩陣乘法,就能交給電腦批次處理,也能分析它的數值性質。第 6 週的 LU 分解就是把這一串 $E$ 整理成兩個三角矩陣。
- **可逆 ⇔ 能化成 $I$**:這是「檢查一個系統能不能被還原」最實際的判準,而且是**可計算的**——不必知道公式,跑一次列化簡就知道。
- **`np.linalg.inv` 內部沒有在做這件事**。它用的是 LU 分解(第 6 週),但數學上等價。理解這個演算法之後,才看得懂為什麼算反矩陣比解方程組貴。

## 幾何意義
Theorem 7 把兩件事接起來:「可逆」(能倒回去)與「能化成 $I$」(化簡到最乾淨)。

想成拼圖:每一次列運算都是一個可逆的小動作。如果一連串小動作能把 $A$ 變成 $I$,那麼把這些動作**倒著做一遍**就能把 $I$ 變回 $A$;而這些動作的總和,正好就是 $A^{-1}$。

反過來,若 $A$ 怎麼化都化不到 $I$(中途出現全零列),表示 $A$ 在某個方向上把空間壓扁了,再也回不來。

## 原理
**為什麼「列運算 = 左乘 $E$」?**(課本 p. 139,Exercises 37–38)

關鍵是第 1 個觀念學過的列規則 $\operatorname{row}_i(EA) = \operatorname{row}_i(E) \cdot A$。$E$ 是把 $I$ 做一次列運算得到的,所以它的每一列就是 $I$ 的某幾列的組合;把那些組合套到 $A$ 上,自然得到對 $A$ 做同一次列運算的結果。

**Theorem 7 的證明**(課本 p. 140):

($\Rightarrow$)若 $A$ 可逆,則由 Theorem 5,$A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b}$ 都有解,所以 $A$ 每一列都有樞軸(第 2 週的 Theorem 4)。$A$ 是方陣,$n$ 個樞軸只能落在對角線上,所以 RREF 就是 $I_n$,即 $A \sim I_n$。

($\Leftarrow$)若 $A \sim I_n$,那麼存在基本矩陣 $E_1, \dots, E_p$ 使
$$E_p \cdots E_1 A = I_n \tag{1}$$
每個 $E_i$ 都可逆,乘積 $E_p \cdots E_1$ 也可逆(Theorem 6(b))。把 (1) 兩邊左乘 $(E_p \cdots E_1)^{-1}$:
$$A = (E_p \cdots E_1)^{-1}$$
可逆矩陣的反矩陣可逆,所以 $A$ 可逆,而且
$$A^{-1} = \left[(E_p \cdots E_1)^{-1}\right]^{-1} = E_p \cdots E_1 = E_p \cdots E_1 I_n$$
最後一個等號說的正是:**把 $A$ 化成 $I_n$ 的那串列運算,作用在 $I_n$ 上就得到 $A^{-1}$**。∎

## 老師講解
### 例 1 · Lay 2.2 Examples 5–6
Let

$$E_1 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ -4 & 0 & 1 \end{bmatrix}, \quad E_2 = \begin{bmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}, \quad E_3 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 5 \end{bmatrix}, \quad A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}$$

Compute $E_1A$, $E_2A$, and $E_3A$, and describe how these products can be obtained by elementary row operations on $A$. Then find the inverse of $E_1$.

1. **先看 $E_1$ 是怎麼來的**:把 $I_3$ 的第 3 列加上第 1 列的 $-4$ 倍,就得到 $E_1$。
2. **算 $E_1A$**:
   $$E_1A = \begin{bmatrix} a & b & c \\ d & e & f \\ g - 4a & h - 4b & i - 4c \end{bmatrix}$$
   前兩列沒動,第 3 列變成「原本的第 3 列 $-$ 4 倍的第 1 列」——**正是對 $A$ 做同一次列運算**。
3. **$E_2$ 是把 $I_3$ 的第 1、2 列互換**,所以
   $$E_2A = \begin{bmatrix} d & e & f \\ a & b & c \\ g & h & i \end{bmatrix}$$
   $A$ 的第 1、2 列也互換了。
4. **$E_3$ 是把 $I_3$ 的第 3 列乘 5**,所以 $E_3A$ 的第 3 列變成 $5g, 5h, 5i$。
5. **歸納出通則**:對 $A$ 做一次列運算 = 左乘「對 $I$ 做同一次列運算得到的矩陣」。
6. **$E_1$ 的反矩陣是什麼?** 問「哪一次列運算能把 $E_1$ 變回 $I$?」答案是「第 3 列加上第 1 列的 $+4$ 倍」,所以
   $$E_1^{-1} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 4 & 0 & 1 \end{bmatrix}$$
7. **驗證**:$E_1^{-1}E_1 = I$(先減 4 倍、再加 4 倍,等於沒做)。所有基本矩陣都可逆,因為**列運算都可以撤銷**。

### 例 2 · Lay 2.2 Example 7
Find the inverse of the matrix $A = \begin{bmatrix} 0 & 1 & 2 \\ 1 & 0 & 3 \\ 4 & -3 & 8 \end{bmatrix}$, if it exists.

1. **把 $A$ 和 $I_3$ 並排**:
   $$[\,A \;\; I\,] = \begin{bmatrix} 0 & 1 & 2 & 1 & 0 & 0 \\ 1 & 0 & 3 & 0 & 1 & 0 \\ 4 & -3 & 8 & 0 & 0 & 1 \end{bmatrix}$$
2. **第一行的樞軸是 0,先換列**(第 1、2 列互換):
   $$\sim \begin{bmatrix} 1 & 0 & 3 & 0 & 1 & 0 \\ 0 & 1 & 2 & 1 & 0 & 0 \\ 4 & -3 & 8 & 0 & 0 & 1 \end{bmatrix}$$
   **右半邊也要跟著換**——這是最常漏掉的一步。
3. **消去第 3 列的 4**(第 3 列 $-$ 4 倍第 1 列):
   $$\sim \begin{bmatrix} 1 & 0 & 3 & 0 & 1 & 0 \\ 0 & 1 & 2 & 1 & 0 & 0 \\ 0 & -3 & -4 & 0 & -4 & 1 \end{bmatrix}$$
4. **消去第 3 列的 $-3$**(第 3 列 $+$ 3 倍第 2 列):
   $$\sim \begin{bmatrix} 1 & 0 & 3 & 0 & 1 & 0 \\ 0 & 1 & 2 & 1 & 0 & 0 \\ 0 & 0 & 2 & 3 & -4 & 1 \end{bmatrix}$$
5. **把樞軸變成 1**(第 3 列 $\div$ 2),再往上消(第 1 列 $-$ 3 倍第 3 列、第 2 列 $-$ 2 倍第 3 列):
   $$\sim \begin{bmatrix} 1 & 0 & 0 & -9/2 & 7 & -3/2 \\ 0 & 1 & 0 & -2 & 4 & -1 \\ 0 & 0 & 1 & 3/2 & -2 & 1/2 \end{bmatrix}$$
6. **左半邊變成 $I_3$ 了,所以 $A$ 可逆**,右半邊就是答案:
   $$A^{-1} = \begin{bmatrix} -9/2 & 7 & -3/2 \\ -2 & 4 & -1 \\ 3/2 & -2 & 1/2 \end{bmatrix}$$
7. **一定要驗算**(課本的 Reasonable Answers 特別提醒):
   $$AA^{-1} = \begin{bmatrix} 0 & 1 & 2 \\ 1 & 0 & 3 \\ 4 & -3 & 8 \end{bmatrix}\begin{bmatrix} -9/2 & 7 & -3/2 \\ -2 & 4 & -1 \\ 3/2 & -2 & 1/2 \end{bmatrix} = I_3 \;\checkmark$$
   課本說明:因為 $A$ 已知可逆,驗一個方向就夠了。

### 例 3 · Lay 2.2 Practice Problem 2
Find the inverse of the matrix $A = \begin{bmatrix} 1 & -2 & -1 \\ -1 & 5 & 6 \\ 5 & -4 & 5 \end{bmatrix}$, if it exists.

1. **照樣並排 $[\,A \;\; I\,]$**,先用第 1 列消掉第 2、3 列的首項:
   $$\begin{bmatrix} 1 & -2 & -1 & 1 & 0 & 0 \\ -1 & 5 & 6 & 0 & 1 & 0 \\ 5 & -4 & 5 & 0 & 0 & 1 \end{bmatrix} \sim \begin{bmatrix} 1 & -2 & -1 & 1 & 0 & 0 \\ 0 & 3 & 5 & 1 & 1 & 0 \\ 0 & 6 & 10 & -5 & 0 & 1 \end{bmatrix}$$
2. **再用第 2 列消第 3 列**(第 3 列 $-$ 2 倍第 2 列):
   $$\sim \begin{bmatrix} 1 & -2 & -1 & 1 & 0 & 0 \\ 0 & 3 & 5 & 1 & 1 & 0 \\ 0 & 0 & 0 & -7 & -2 & 1 \end{bmatrix}$$
3. **左半邊出現一整列 0**。再怎麼做列運算,這一列都不可能變出樞軸,所以左半邊**永遠變不成 $I_3$**。
4. **由 Theorem 7,$A$ 不可逆**,計算到此為止——不必把右半邊做完。
5. **為什麼會這樣**:第 3 列的 $(6, 10)$ 恰好是第 2 列 $(3, 5)$ 的兩倍,表示 $A$ 的三列線性相依。
6. **對照組**:例 2 的矩陣化得出 $I_3$,這一題化不出來。**這就是判斷可逆與否最實際的方法**——不必算行列式,化簡一次就知道。

#### 備註
例 3 一定要講,學生才知道「什麼時候可以停手」。很多人會一路做到底,浪費時間還算出一堆沒有意義的數字。

三個例子的順序是有設計的:例 1 建立「列運算 = 左乘」,例 2 用演算法成功求出反矩陣,例 3 示範失敗的情況。

## 易錯點
- **右半邊忘了跟著做**。每一次列運算**整列**(包含右半邊)都要做,尤其換列時最容易漏。
- **左半邊出現全零列還硬做下去**。出現全零列就結束了,結論是「不可逆」。
- **把 $[\,I \;\; A^{-1}\,]$ 的左右讀反**。答案是**右半邊**。
- **以為只能用這個演算法**。只要 $A^{-1}$ 的某一行時,解 $A\mathbf{x} = \mathbf{e}_j$ 就好(Exercises 45–46)。
- **把基本矩陣乘在右邊**。列運算對應**左**乘;右乘做的是行運算。

## 教學提示
這是本週最花時間的計算,建議留 25 分鐘,其中例 2 至少寫 10 分鐘的板書——**每一步都要把右半邊一起寫出來**,不要省略。

例 1 的講法建議用問答:先給 $E_1$,問學生「這是對 $I$ 做了什麼?」再問「那 $E_1A$ 會是什麼?」讓他們自己發現規律,比直接講快。

$3 \times 3$ 的反矩陣算起來很長,可以讓學生兩兩一組:一人算、一人監督每一步右半邊有沒有跟著做。

課堂建議做:Exercises 39、41(一個 $2 \times 2$、一個 $3 \times 3$);Exercise 42(不可逆的情形,練習「什麼時候停手」);Practice Problem 2。是非 Exercises 18、19、20 可以口頭快問快答。Exercise 45(只求一行)一定要講,它連到實作課。

T 題 Exercises 46、51、52 放進實作課。

## 練習
### 照做 · Lay 2.2 Exercises 39–42
Find the inverses of the matrices in Exercises 39–42, if they exist. Use the algorithm introduced in this section.

(39) $\begin{bmatrix} 1 & 2 \\ 4 & 7 \end{bmatrix}$

(40) $\begin{bmatrix} 9 & 7 \\ 8 & 6 \end{bmatrix}$

(41) $\begin{bmatrix} 1 & 0 & -2 \\ -3 & 1 & 4 \\ 2 & -3 & 4 \end{bmatrix}$

(42) $\begin{bmatrix} 1 & -2 & 1 \\ 4 & -7 & 3 \\ -2 & 6 & -4 \end{bmatrix}$

#### 解答
(39) 化簡 $[\,A \;\; I\,]$:
$$\begin{bmatrix} 1 & 2 & 1 & 0 \\ 4 & 7 & 0 & 1 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 & 1 & 0 \\ 0 & -1 & -4 & 1 \end{bmatrix} \sim \begin{bmatrix} 1 & 0 & -7 & 2 \\ 0 & 1 & 4 & -1 \end{bmatrix}$$
所以 $A^{-1} = \begin{bmatrix} -7 & 2 \\ 4 & -1 \end{bmatrix}$。

(40) $A^{-1} = \begin{bmatrix} -3 & 7/2 \\ 4 & -9/2 \end{bmatrix}$。

(41) $A^{-1} = \begin{bmatrix} 8 & 3 & 1 \\ 10 & 4 & 1 \\ 7/2 & 3/2 & 1/2 \end{bmatrix}$(最後一列出現分母 2,因為最後的樞軸是 2)。

(42) **不可逆**。化簡到
$$\begin{bmatrix} 1 & -2 & 1 \\ 0 & 1 & -1 \\ 0 & 0 & 0 \end{bmatrix}$$
只有 2 個樞軸,$A$ 不與 $I_3$ 列等價,由 Theorem 7 不可逆。

#### 備註
(39)(40) 雖然可以直接套 $2 \times 2$ 公式,但題目明確要求用**演算法**,因為 $3 \times 3$ 以上沒有簡單公式可套。請要求學生照做。

(42) 是四題裡唯一不可逆的,放在最後,讓學生練習「發現全零列就停手」。

### 是非 · Lay 2.2 Exercises 18–20
In Exercises 11–20, mark each statement True or False (T/F). Justify each answer.

(18) **(T/F)** If $A$ can be row reduced to the identity matrix, then $A$ must be invertible.

(19) **(T/F)** Each elementary matrix is invertible.

(20) **(T/F)** If $A$ is invertible, then the elementary row operations that reduce $A$ to the identity $I_n$ also reduce $A^{-1}$ to $I_n$.

#### 解答
- (18) **True.** 這正是 Theorem 7 的一半:$n \times n$ 矩陣與 $I_n$ 列等價 ⇒ 可逆。
- (19) **True.** 每一次列運算都可以撤銷,做反向那一次列運算得到的基本矩陣 $F$ 就滿足 $FE = EF = I$。
- (20) **False.** 那串列運算的整體效果是**左乘 $A^{-1}$**(Theorem 7 說它把 $I_n$ 變成 $A^{-1}$)。作用在 $A^{-1}$ 上會得到 $A^{-1}A^{-1} = (A^{-1})^2$,一般不是 $I_n$。

  反例:$A = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$,列運算「第 1 列乘 $\tfrac12$」把 $A$ 化成 $I$;但同一個運算把 $A^{-1} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1 \end{bmatrix}$ 變成 $\begin{bmatrix} 1/4 & 0 \\ 0 & 1 \end{bmatrix} \ne I$。

#### 備註
(20) 是本節最容易答錯的一題,因為它和 Theorem 7 只差幾個字。正確的敘述是:「把 $A$ 化成 $I_n$ 的列運算,會把 $I_n$ 化成 $A^{-1}$。」建議把兩個句子並排寫在黑板上讓學生比對。

書後對 Exercises 18–20 沒有給 T/F(18、20 是偶數題,19 落在「先自己作答」那一段),上面的答案是本講義判定的。

### 變化 · Lay 2.2 Practice Problem 2
Find the inverse of the matrix $A = \begin{bmatrix} 1 & -2 & -1 \\ -1 & 5 & 6 \\ 5 & -4 & 5 \end{bmatrix}$, if it exists.

#### 解答
見上方「老師講解」的例 3:化簡到第二步時左半邊出現全零列,所以 $A$ **不可逆**($\det A = 0$)。

#### 備註
這題和老師講解的例 3 是同一題。學生版把它再列一次當練習,是刻意的——先看老師做一次,再自己從頭做一次,對「什麼時候可以停手」的印象最深。

### 變化 · Lay 2.2 Exercises 45–46
(45) Let $A = \begin{bmatrix} -2 & -7 & -9 \\ 2 & 5 & 6 \\ 1 & 3 & 4 \end{bmatrix}$. Find the third column of $A^{-1}$ without computing the other columns.

(46) **(T)** Let $A = \begin{bmatrix} -25 & -9 & -27 \\ 546 & 180 & 537 \\ 154 & 50 & 149 \end{bmatrix}$. Find the second and third columns of $A^{-1}$ without computing the first column.

#### 解答
(45) $A^{-1}$ 的第 3 行就是 $A\mathbf{x} = \mathbf{e}_3$ 的解。列化簡 $[\,A \;\; \mathbf{e}_3\,]$ 得
$$\mathbf{x} = \begin{bmatrix} 3 \\ -6 \\ 4 \end{bmatrix}$$
驗證:$A\begin{bmatrix} 3 \\ -6 \\ 4 \end{bmatrix} = \begin{bmatrix} -6 + 42 - 36 \\ 6 - 30 + 24 \\ 3 - 18 + 16 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$ ✓

(46) 一次列化簡 $[\,A \;\; \mathbf{e}_2 \;\; \mathbf{e}_3\,]$,得到
$$A^{-1}\text{ 的第 2 行} = \begin{bmatrix} 3/2 \\ -433/6 \\ 68/3 \end{bmatrix}, \qquad A^{-1}\text{ 的第 3 行} = \begin{bmatrix} -9/2 \\ 439/2 \\ -69 \end{bmatrix}$$

#### 備註
這兩題就是「另一種看法」的實戰:**$A^{-1}$ 的第 $j$ 行 = $A\mathbf{x} = \mathbf{e}_j$ 的解**。只要一行時,成本只有整個反矩陣的 $1/n$。

(46) 標 T,數字大又會出現分數,適合用電腦算;放進實作課。

### 變化 · Lay 2.2 Exercises 43–44
(43) Use the algorithm from this section to find the inverses of

$$\begin{bmatrix} 1 & 0 & 0 \\ 1 & 1 & 0 \\ 1 & 1 & 1 \end{bmatrix} \quad\text{and}\quad \begin{bmatrix} 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 1 & 1 & 1 & 0 \\ 1 & 1 & 1 & 1 \end{bmatrix}$$

Let $A$ be the corresponding $n \times n$ matrix, and let $B$ be its inverse. Guess the form of $B$, and then prove that $AB = I$ and $BA = I$.

(44) Repeat the strategy of Exercise 43 to guess the inverse of

$$A = \begin{bmatrix} 1 & 0 & 0 & \cdots & 0 \\ 1 & 2 & 0 & & 0 \\ 1 & 2 & 3 & & 0 \\ \vdots & & & \ddots & \vdots \\ 1 & 2 & 3 & \cdots & n \end{bmatrix}$$

Prove that your guess is correct.

#### 解答
(43)
$$\begin{bmatrix} 1 & 0 & 0 \\ 1 & 1 & 0 \\ 1 & 1 & 1 \end{bmatrix}^{-1} = \begin{bmatrix} 1 & 0 & 0 \\ -1 & 1 & 0 \\ 0 & -1 & 1 \end{bmatrix}, \qquad \begin{bmatrix} 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 1 & 1 & 1 & 0 \\ 1 & 1 & 1 & 1 \end{bmatrix}^{-1} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ -1 & 1 & 0 & 0 \\ 0 & -1 & 1 & 0 \\ 0 & 0 & -1 & 1 \end{bmatrix}$$

一般形:對角線是 1、次對角線 $b_{i,\,i-1}$ 是 $-1$、其餘是 0。

證明(用行向量):設 $\mathbf{a}_j$、$\mathbf{b}_j$、$\mathbf{e}_j$ 分別是 $A$、$B$、$I$ 的第 $j$ 行。$A$ 的第 $j$ 行從第 $j$ 列起全是 1,所以 $\mathbf{a}_j - \mathbf{a}_{j+1} = \mathbf{e}_j$($j < n$)、$\mathbf{a}_n = \mathbf{e}_n$;而 $\mathbf{b}_j = \mathbf{e}_j - \mathbf{e}_{j+1}$($j < n$)、$\mathbf{b}_n = \mathbf{e}_n$。於是
$$A\mathbf{b}_j = A(\mathbf{e}_j - \mathbf{e}_{j+1}) = \mathbf{a}_j - \mathbf{a}_{j+1} = \mathbf{e}_j$$
逐行成立,故 $AB = I$;同法可得 $BA = I$。

(44) 第 $i$ 列只有 $(i, i)$ 格是 $\tfrac1i$、$(i, i-1)$ 格是 $-\tfrac1i$(第 1 列只有一個 1):
$$A^{-1} = \begin{bmatrix} 1 & 0 & 0 & \cdots & 0 \\ -1/2 & 1/2 & 0 & & 0 \\ 0 & -1/3 & 1/3 & & 0 \\ \vdots & & \ddots & \ddots & \vdots \\ 0 & 0 & \cdots & -1/n & 1/n \end{bmatrix}$$
證明:$\operatorname{row}_i(A) = (1, 2, \dots, i, 0, \dots, 0)$,所以 $\operatorname{row}_i(A) - \operatorname{row}_{i-1}(A) = i\,\mathbf{e}_i^T$。於是對 $i \ge 2$,
$$\operatorname{row}_i(B)\,A = \tfrac1i\bigl(\operatorname{row}_i(A) - \operatorname{row}_{i-1}(A)\bigr) = \mathbf{e}_i^T$$
$i = 1$ 時 $\operatorname{row}_1(B)A = \operatorname{row}_1(A) = \mathbf{e}_1^T$。故 $BA = I$。

#### 備註
這兩題示範了一種常用的研究方法:**先算小例子、觀察規律、猜通式、再證明**。資工做演算法分析時常常這樣做。

(43) 的 $A$ 是「累加矩陣」($\mathbf{y} = A\mathbf{x}$ 的第 $i$ 格是前 $i$ 項的和),它的反矩陣是「差分矩陣」。積分與微分互逆的離散版,值得點一句。

### 應用 · Lay 2.2 Exercises 51–52(T 電腦題)
(51) Let $D = \begin{bmatrix} .0040 & .0030 & .0010 & .0005 \\ .0030 & .0050 & .0030 & .0010 \\ .0010 & .0030 & .0050 & .0030 \\ .0005 & .0010 & .0030 & .0040 \end{bmatrix}$ be a flexibility matrix for an elastic beam with four points at which force is applied. Units are centimeters per newton of force. Measurements at the four points show deflections of .08, .12, .16, and .12 cm. Determine the forces at the four points.

(52) With $D$ as in Exercise 51, determine the forces that produce a deflection of .24 cm at the second point on the beam, with zero deflections at the other three points. How is the answer related to the entries in $D^{-1}$? [*Hint:* First answer the question when the deflection is 1 cm at the second point.]

#### 解答
(51) $\mathbf{f} = D^{-1}\mathbf{y}$,其中 $\mathbf{y} = (.08, .12, .16, .12)$:
$$\mathbf{f} = \begin{bmatrix} 12 \\ 1.5 \\ 21.5 \\ 12 \end{bmatrix}$$
四點的力分別是 **12、1.5、21.5、12 牛頓**。

(52) $\mathbf{y} = (0, .24, 0, 0)$,所以 $\mathbf{f} = D^{-1}\mathbf{y} = .24 \times (D^{-1}$ 的第 2 行$)$:
$$\mathbf{f} = \begin{bmatrix} -104 \\ 167 \\ -113 \\ 56 \end{bmatrix} \text{ 牛頓}$$
**關係**:若第 2 點的撓度是 1 cm、其餘為 0,所需的力就正好是 $D^{-1}$ 的第 2 行;本題的 .24 cm 只是把那一行乘上 .24。

#### 備註
兩題都標 T,放進實作課。(52) 的提示「先想 1 cm 的情形」正是觀念 4 例 3 的解讀:**$D^{-1}$ 的第 $j$ 行 = 讓第 $j$ 點變形一單位、其餘不動所需的力**。

負號一樣要解釋:要讓變形只集中在第 2 點,第 1、3 點必須往上拉。

課本 p. 144 習題區有一張四點樑的圖(標示 #1–#4、撓度 .08/.12/.16/.12 與力 $f_1$–$f_4$),上課時可以畫在黑板上。

### 挑戰 · Lay 2.2 Exercises 31–34
(31) Explain why the columns of an $n \times n$ matrix $A$ are linearly independent when $A$ is invertible.

(32) Explain why the columns of an $n \times n$ matrix $A$ span $\mathbb{R}^n$ when $A$ is invertible. [*Hint:* Review Theorem 4 in Section 1.4.]

(33) Suppose $A$ is $n \times n$ and the equation $A\mathbf{x} = \mathbf{0}$ has only the trivial solution. Explain why $A$ has $n$ pivot columns and $A$ is row equivalent to $I_n$. By Theorem 7, this shows that $A$ must be invertible. (This exercise and Exercise 34 will be cited in Section 2.3.)

(34) Suppose $A$ is $n \times n$ and the equation $A\mathbf{x} = \mathbf{b}$ has a solution for each $\mathbf{b}$ in $\mathbb{R}^n$. Explain why $A$ must be invertible. [*Hint:* Is $A$ row equivalent to $I_n$?]

#### 解答
- (31) $A$ 可逆時,由 Theorem 5,$A\mathbf{x} = \mathbf{0}$ 有唯一解;而 $\mathbf{x} = \mathbf{0}$ 本來就是解,所以唯一解就是平凡解。齊次方程只有平凡解 ⇔ 各行線性獨立(第 3 週)。
- (32) 對任意 $\mathbf{b}$,$\mathbf{x} = A^{-1}\mathbf{b}$ 都是解,所以 $A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b}$ 都有解。由第 2 週的 Theorem 4,這等價於「$A$ 的行張成 $\mathbb{R}^n$」。
- (33) 只有平凡解 ⇒ 沒有自由變數 ⇒ 每一行都是樞軸行,共 $n$ 個樞軸。$A$ 是 $n \times n$,$n$ 個樞軸只能排在對角線上,所以 RREF 是 $I_n$,即 $A \sim I_n$;由 Theorem 7 得 $A$ 可逆。
- (34) 對每個 $\mathbf{b}$ 都有解 ⇒(第 2 週 Theorem 4)每一列都有樞軸,共 $n$ 個 ⇒ 每一行也都是樞軸行 ⇒ RREF 是 $I_n$ ⇒ 由 Theorem 7,$A$ 可逆。

#### 備註
這四題是**下週可逆矩陣定理(IMT)的零件**,課本自己在 Exercise 33 的括號裡說「這題和 Exercise 34 會在 2.3 節被引用」。

四題的共同套路是:可逆 → Theorem 5 → 解的存在或唯一 → 樞軸的位置 → 回到 Theorem 7。建議畫成一張小流程圖。

### 挑戰 · Lay 2.2 Exercises 37–38
Exercises 37 and 38 prove special cases of the facts about elementary matrices stated in the box following Example 5. Here $A$ is a $3 \times 3$ matrix and $I = I_3$. (A general proof would require slightly more notation.)

(37)

- **a.** Use equation (1) from Section 2.1 to show that $\operatorname{row}_i(A) = \operatorname{row}_i(I) \cdot A$, for $i = 1, 2, 3$.
- **b.** Show that if rows 1 and 2 of $A$ are interchanged, then the result may be written as $EA$, where $E$ is an elementary matrix formed by interchanging rows 1 and 2 of $I$.
- **c.** Show that if row 3 of $A$ is multiplied by 5, then the result may be written as $EA$, where $E$ is formed by multiplying row 3 of $I$ by 5.

(38) Show that if row 3 of $A$ is replaced by $\operatorname{row}_3(A) - 4\operatorname{row}_1(A)$, the result is $EA$, where $E$ is formed from $I$ by replacing $\operatorname{row}_3(I)$ by $\operatorname{row}_3(I) - 4\operatorname{row}_1(I)$.

#### 解答
(37) **a.** 列規則說「乘積的第 $i$ 列 = (左矩陣的第 $i$ 列)$\cdot$ 右矩陣」。$\operatorname{row}_i(I)$ 就是 $\mathbf{e}_i^T$,而 $\mathbf{e}_i^T A$ 把 $A$ 的各列依 $\mathbf{e}_i$ 的係數加權,結果正是 $\operatorname{row}_i(A)$。

**b.** 設 $E$ 由 $I$ 交換第 1、2 列得到,則 $\operatorname{row}_1(E) = \operatorname{row}_2(I)$、$\operatorname{row}_2(E) = \operatorname{row}_1(I)$、$\operatorname{row}_3(E) = \operatorname{row}_3(I)$。用 (a):
$$\operatorname{row}_1(EA) = \operatorname{row}_1(E)A = \operatorname{row}_2(I)A = \operatorname{row}_2(A)$$
同理 $\operatorname{row}_2(EA) = \operatorname{row}_1(A)$、$\operatorname{row}_3(EA) = \operatorname{row}_3(A)$。這正是把 $A$ 的第 1、2 列互換。

**c.** 設 $E$ 由 $I$ 的第 3 列乘 5 得到,則 $\operatorname{row}_3(EA) = 5\operatorname{row}_3(I)A = 5\operatorname{row}_3(A)$,其餘列不變。

(38) 設 $E = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ -4 & 0 & 1 \end{bmatrix}$(即把 $I$ 的第 3 列換成 $\operatorname{row}_3(I) - 4\operatorname{row}_1(I)$)。由 (37a),
$$\operatorname{row}_3(EA) = \bigl(\operatorname{row}_3(I) - 4\operatorname{row}_1(I)\bigr)A = \operatorname{row}_3(A) - 4\operatorname{row}_1(A)$$
第 1、2 列因為 $\operatorname{row}_i(E) = \operatorname{row}_i(I)$ 而保持不變。∎

#### 備註
這兩題證的就是本節最核心的那句話「列運算 = 左乘基本矩陣」,三種列運算各證一種。(38) 的 $E$ 正是老師講解例 1 的 $E_1$。

題幹說「equation (1) from Section 2.1」,但書後提示寫的是「the box following Example 6 in Section 2.1」——指的是同一條列規則,書上的引用位置不一致,備課時說一聲即可。

### 挑戰 · Lay 2.2 Exercises 47–48
(47) Let $A = \begin{bmatrix} 1 & 2 \\ 1 & 3 \\ 1 & 5 \end{bmatrix}$. Construct a $2 \times 3$ matrix $C$ (by trial and error) using only 1, $-1$, and 0 as entries, such that $CA = I_2$. Compute $AC$ and note that $AC \ne I_3$.

(48) Let $A = \begin{bmatrix} 1 & 1 & 1 & 0 \\ 0 & 1 & 1 & 1 \end{bmatrix}$. Construct a $4 \times 2$ matrix $D$ using only 1 and 0 as entries, such that $AD = I_2$. Is it possible that $CA = I_4$ for some $4 \times 2$ matrix $C$? Why or why not?

#### 解答
(47) 取
$$C = \begin{bmatrix} 1 & 1 & -1 \\ -1 & 1 & 0 \end{bmatrix}$$
檢查:$CA = \begin{bmatrix} 1 + 1 - 1 & 2 + 3 - 5 \\ -1 + 1 + 0 & -2 + 3 + 0 \end{bmatrix} = I_2$ ✓

但是
$$AC = \begin{bmatrix} -1 & 3 & -1 \\ -2 & 4 & -1 \\ -4 & 6 & -1 \end{bmatrix} \ne I_3$$
因為 $AC$ 的秩最多是 2,不可能等於 $I_3$。

(48) 取
$$D = \begin{bmatrix} 1 & 0 \\ 0 & 0 \\ 0 & 0 \\ 0 & 1 \end{bmatrix}$$
則 $A\mathbf{d}_1 = A$ 的第 1 行 $= \mathbf{e}_1$、$A\mathbf{d}_2 = A$ 的第 4 行 $= \mathbf{e}_2$,所以 $AD = I_2$ ✓

**不可能**存在 $4 \times 2$ 的 $C$ 使 $CA = I_4$:若成立,則 $A\mathbf{x} = \mathbf{0} \Rightarrow \mathbf{x} = CA\mathbf{x} = \mathbf{0}$,表示 $A$ 的 4 行線性獨立;但 $A$ 只有 2 列、最多 2 個樞軸,4 行必有自由變數,矛盾。

#### 備註
這兩題說明:**非方陣可能有單邊的「反矩陣」,但不可能兩邊都有**。這正好呼應觀念 3 的 Lay 2.1 Exercise 33(若左反與右反都存在,則必為方陣且兩者相同),也解釋了課本為什麼把反矩陣的定義限制在方陣上。

答案不唯一((47) 在「只用 1、$-1$、0」的限制下書上給這一組);(48) 在「只用 0 和 1」的限制下 $D$ 是唯一的。

## 驗算
```check
Matrix([[1, 0, 0], [0, 1, 0], [-4, 0, 1]]) * Matrix([[a, b, c], [d, f, g], [h, k, s]]) == Matrix([[a, b, c], [d, f, g], [h - 4*a, k - 4*b, s - 4*c]])
Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]]) * Matrix([[a, b, c], [d, f, g], [h, k, s]]) == Matrix([[d, f, g], [a, b, c], [h, k, s]])
Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 5]]) * Matrix([[a, b, c], [d, f, g], [h, k, s]]) == Matrix([[a, b, c], [d, f, g], [5*h, 5*k, 5*s]])
Matrix([[1, 0, 0], [0, 1, 0], [-4, 0, 1]]).inv() == Matrix([[1, 0, 0], [0, 1, 0], [4, 0, 1]])
Matrix([[0, 1, 2], [1, 0, 3], [4, -3, 8]]).inv() == Matrix([[Rational(-9,2), 7, Rational(-3,2)], [-2, 4, -1], [Rational(3,2), -2, Rational(1,2)]])
Matrix([[0, 1, 2], [1, 0, 3], [4, -3, 8]]) * Matrix([[Rational(-9,2), 7, Rational(-3,2)], [-2, 4, -1], [Rational(3,2), -2, Rational(1,2)]]) == eye(3)
Matrix.hstack(Matrix([[0, 1, 2], [1, 0, 3], [4, -3, 8]]), eye(3)).rref()[0] == Matrix.hstack(eye(3), Matrix([[Rational(-9,2), 7, Rational(-3,2)], [-2, 4, -1], [Rational(3,2), -2, Rational(1,2)]]))
Matrix([[1, -2, -1], [-1, 5, 6], [5, -4, 5]]).det() == 0
Matrix.hstack(Matrix([[1, -2, -1], [-1, 5, 6], [5, -4, 5]]), eye(3)).rref()[0][2, 0:3] == Matrix([[0, 0, 0]])
Matrix([[1, 2], [4, 7]]).inv() == Matrix([[-7, 2], [4, -1]])
Matrix([[9, 7], [8, 6]]).inv() == Matrix([[-3, Rational(7,2)], [4, Rational(-9,2)]])
Matrix([[1, 0, -2], [-3, 1, 4], [2, -3, 4]]).inv() == Matrix([[8, 3, 1], [10, 4, 1], [Rational(7,2), Rational(3,2), Rational(1,2)]])
Matrix([[1, -2, 1], [4, -7, 3], [-2, 6, -4]]).det() == 0
Matrix([[1, -2, 1], [4, -7, 3], [-2, 6, -4]]).rank() == 2
Matrix([[2, 0], [0, 1]]).inv() == Matrix([[Rational(1,2), 0], [0, 1]])
Matrix([[Rational(1,2), 0], [0, 1]]) * Matrix([[Rational(1,2), 0], [0, 1]]) != eye(2)
Matrix([[-2, -7, -9], [2, 5, 6], [1, 3, 4]]) * Matrix([3, -6, 4]) == Matrix([0, 0, 1])
Matrix([[-25, -9, -27], [546, 180, 537], [154, 50, 149]]).inv()[:, 1:3] == Matrix([[Rational(3,2), Rational(-9,2)], [Rational(-433,6), Rational(439,2)], [Rational(68,3), -69]])
Matrix([[1, 0, 0], [1, 1, 0], [1, 1, 1]]).inv() == Matrix([[1, 0, 0], [-1, 1, 0], [0, -1, 1]])
Matrix([[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]]).inv() == Matrix([[1, 0, 0, 0], [-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1]])
Matrix(5, 5, lambda i, j: j + 1 if j <= i else 0).inv() == Matrix(5, 5, lambda i, j: Rational(1, i + 1) if i == j else (Rational(-1, i + 1) if j == i - 1 else 0))
(Matrix([[40, 30, 10, 5], [30, 50, 30, 10], [10, 30, 50, 30], [5, 10, 30, 40]]) / 10000).inv() * Matrix([Rational(8,100), Rational(12,100), Rational(16,100), Rational(12,100)]) == Matrix([12, Rational(3,2), Rational(43,2), 12])
(Matrix([[40, 30, 10, 5], [30, 50, 30, 10], [10, 30, 50, 30], [5, 10, 30, 40]]) / 10000).inv() * Matrix([0, Rational(24,100), 0, 0]) == Matrix([-104, 167, -113, 56])
Matrix([[1, 1, -1], [-1, 1, 0]]) * Matrix([[1, 2], [1, 3], [1, 5]]) == eye(2)
Matrix([[1, 2], [1, 3], [1, 5]]) * Matrix([[1, 1, -1], [-1, 1, 0]]) == Matrix([[-1, 3, -1], [-2, 4, -1], [-4, 6, -1]])
Matrix([[1, 1, 1, 0], [0, 1, 1, 1]]) * Matrix([[1, 0], [0, 0], [0, 0], [0, 1]]) == eye(2)
Matrix([[1, 1, 1, 0], [0, 1, 1, 1]]).rank() == 2
```
