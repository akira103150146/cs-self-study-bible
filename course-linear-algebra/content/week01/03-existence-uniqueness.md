---
title_en: Existence and Uniqueness Questions
title_zh: 存在性與唯一性:兩個基本問題
sub: Decide the size of the solution set without solving completely
level: mid
source: Lay 1.1
lab_hook: "`M.rref()` 回傳的 pivots 裡有沒有最後一行的索引"
---
## 觀念
Two fundamental questions about a linear system:

1. Is the system consistent; that is, does at least one solution **exist**?
2. If a solution exists, is it the *only* one; that is, is the solution **unique**?

These questions can be answered by row operations on the augmented matrix, often *without solving the system completely*. Row reduce until the matrix is in **triangular form** (all entries below the "staircase" are zero) and go back to equation notation.

- A row such as $[\,0 \;\; 0 \;\; 0 \mid 15\,]$ stands for $0x_1 + 0x_2 + 0x_3 = 15$, that is, $0 = 15$. A system containing such an equation has **no solution** — it is inconsistent.
- If there is no such contradiction and each variable is determined in turn from the bottom equation upward, a solution **exists** and it is **unique**.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| existence | 存在性 | 至少有一個解嗎? |
| uniqueness | 唯一性 | 如果有解,是不是只有一個? |
| triangular form | 三角形式 | 左下角全是 0 的形狀;1.2 會換成精確的「梯形」 |
| contradiction | 矛盾 | 例如 $0 = 15$,永遠不成立的方程式 |

## 白話說
很多時候我們不需要真的把解算出來,只想知道兩件事:**有沒有解?有的話是不是只有一個?** 這就是存在性和唯一性,是整門課反覆出現的兩個問題。

做法:列運算做到**三角形式**就停下來,然後把矩陣翻回方程式來讀。

- 最下面出現「$0 = $ 非零數」→ 矛盾 → **無解**。
- 沒有矛盾,而且從最下面一條開始,每一條都能決定一個新的未知數 → **有解而且唯一**。

## 幾何意義
三個未知數時,每條方程式是一個平面。

- 例 1:三個平面剛好交於一點 → 唯一解。
- 例 2:三個平面兩兩相交,但沒有任何一點同時在三個平面上 → 無解。在三角形式裡,這個「沒有共同點」就表現成 $0 = 15$。

課本 p. 30(唯一解)與 p. 32(無解)的立體圖正好是這兩種情況,上課可以直接翻給學生看。

## 在資工哪裡用
寫程式前先問「有沒有解、解是不是唯一」,是很重要的工程習慣:

- **沒有解**:設定互相矛盾,例如排課系統的限制條件彼此衝突,程式要回報「無法滿足」。
- **不唯一**:資訊不夠,例如從太少的量測資料反推模型參數,任何答案都只是「其中一個」。

資料庫的完整性檢查、排程系統的限制檢查,背後都是存在性的問題。

## 原理
**為什麼三角形式就能判斷?** 列運算不改變解集(本週證明時刻),所以三角形式和原方程組有同樣的解集。

- 若某一列是 $[\,0 \;\cdots\; 0 \mid b\,]$ 且 $b \neq 0$,它代表 $0 = b$,沒有任何數能滿足,所以原方程組無解。
- 若沒有這種列,而且三角形式的對角線上每一格都不是 0,那麼最下面一條直接決定最後一個未知數,往上每一條恰好多決定一個未知數——每個未知數都只有一個可能值,所以有解而且唯一。

(對角線上出現 0、但沒有矛盾的情況,就是「無限多解」,要到觀念 5 才完整處理。)

## 老師講解
### 例 1 · Lay 1.1 Example 2
Determine if the following system is consistent: $x_1 - 2x_2 + x_3 = 0,\;\; 2x_2 - 8x_3 = 8,\;\; 5x_1 - 5x_3 = 10$.

1. 這是觀念 2 例 2 的方程組。我們已經用列運算把它化成三角形式:
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 1 & -4 & 4 \\ 0 & 0 & 1 & -1 \end{array}\right]$$
2. 翻回方程式:$x_1 - 2x_2 + x_3 = 0$、$x_2 - 4x_3 = 4$、$x_3 = -1$。
3. **存在性**:第三條直接告訴我們 $x_3 = -1$;把它代進第二條,可以算出 $x_2$;再代進第一條,可以算出 $x_1$。每一步都算得下去,所以**解存在**,方程組相容。
4. **唯一性**:$x_3$ 只有一個可能值;第二條讓 $x_2$ 也只有一個可能值;第一條讓 $x_1$ 只有一個可能值。所以**解唯一**。
5. 注意:我們**不必真的算出** $x_1$、$x_2$ 的數值就能回答這兩個問題。這就是本觀念的重點。

### 例 2 · Lay 1.1 Example 3
Determine if the following system is consistent: $x_2 - 4x_3 = 8,\;\; 2x_1 - 3x_2 + 2x_3 = 1,\;\; 4x_1 - 8x_2 + 12x_3 = 1$.

1. 寫出增廣矩陣:
   $$\left[\begin{array}{rrr|r} 0 & 1 & -4 & 8 \\ 2 & -3 & 2 & 1 \\ 4 & -8 & 12 & 1 \end{array}\right]$$
2. 第一列沒有 $x_1$(係數是 0),沒辦法拿它去消別列的 $x_1$。**交換第 1、2 列**,讓有 $x_1$ 的式子到最上面:
   $$\left[\begin{array}{rrr|r} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 4 & -8 & 12 & 1 \end{array}\right]$$
3. 消掉第 3 列的 $4x_1$:第 1 列的 $x_1$ 係數是 2,所以 $R_3 \leftarrow R_3 + (-2)R_1$,第 3 列變成 $[\,0 \;\; {-2} \;\; 8 \mid {-1}\,]$。
4. 用第 2 列的 $x_2$ 消掉第 3 列的 $-2x_2$:$R_3 \leftarrow R_3 + 2R_2$,第 3 列變成 $[\,0 \;\; 0 \;\; 0 \mid 15\,]$:
   $$\left[\begin{array}{rrr|r} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 0 & 0 & 0 & 15 \end{array}\right]$$
5. 現在是三角形式。**翻回方程式來讀**:最後一條是 $0x_1 + 0x_2 + 0x_3 = 15$,也就是 $0 = 15$。
6. 不管 $x_1, x_2, x_3$ 取什麼值,$0 = 15$ 都不成立。這個三角形式和原方程組有同樣的解集,所以原方程組**不相容(無解)**。
7. 記住最後一列的樣子 $[\,0 \;\; 0 \;\; 0 \mid 15\,]$:這是**不相容方程組在三角形式裡的典型長相**。

## 易錯點
- 看到最後一列有 0 就說無解。要看的是「左邊全是 0、右邊**不是** 0」;$[\,0 \;\; 0 \;\; 0 \mid 0\,]$ 只是 $0 = 0$,不矛盾。
- 例 2 第一步沒有先換列,硬拿 0 去消別人。
- 以為要把解完整算出來才能回答存在性。三角形式就夠了。

## 教學提示
把課本 p. 31 的「兩個基本問題」方框抄在黑板上,整學期都會回來用(第 5、6 週的可逆矩陣定理就是這兩個問題的延伸)。

例 2 做完後,給學生看課本 p. 32 的立體圖:三個平面兩兩相交成三條平行的線,但沒有共同點。「$0 = 15$」在圖上就是「找不到三個平面的共同點」。

課堂建議做:Practice Problem 2、Exercises 7–10;是非題 33;變化挑 Exercises 23–26 其中兩題;挑戰題(Exercises 35、37–38)留作業。

## 練習
### 照做 · Lay 1.1 Practice Problem 2
The augmented matrix of a linear system has been transformed by row operations into the form below. Determine if the system is consistent.

$$\left[\begin{array}{rrr|r} 1 & 5 & 2 & -6 \\ 0 & 4 & -7 & 2 \\ 0 & 0 & 5 & 0 \end{array}\right]$$

#### 解答
翻回方程式:$x_1 + 5x_2 + 2x_3 = -6$、$4x_2 - 7x_3 = 2$、$5x_3 = 0$。第三條給出 $x_3 = 0$——這是完全合法的值,不是矛盾。代回可以依序求出唯一的 $x_2$、$x_1$。所以**相容,而且解唯一**。和例 2 的 $0 = 15$ 對照:這裡是 $5x_3 = 0$,左邊不是全 0。(課本 p. 36)

### 照做 · Lay 1.1 Exercises 7–8
In each case, the augmented matrix of a linear system has been reduced by row operations to the form shown. Continue the appropriate row operations and describe the solution set of the original system.

(7) $\left[\begin{array}{rrr|r} 1 & 7 & 3 & -4 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & -2 \end{array}\right]$  (8) $\left[\begin{array}{rrr|r} 1 & 1 & 5 & 0 \\ 0 & 1 & 9 & 0 \\ 0 & 0 & 7 & -7 \end{array}\right]$

#### 解答
(7) 第 3 列是 $[\,0 \;\; 0 \;\; 0 \mid 1\,]$,即 $0 = 1$,矛盾。**解集是空集合**(書後解答:the solution set is empty)。不用再做任何列運算。

(8) 已是三角形式。$R_3 \leftarrow \tfrac17 R_3$ 得 $x_3 = -1$;往上:$x_2 = -9x_3 = 9$;$x_1 = -x_2 - 5x_3 = -9 + 5 = -4$。**唯一解** $(-4, 9, -1)$。

### 照做 · Lay 1.1 Exercises 9–10
In each case, the augmented matrix of a linear system has been reduced by row operations to the form shown. Continue the appropriate row operations and describe the solution set of the original system.

(9) $\left[\begin{array}{rrrr|r} 1 & -1 & 0 & 0 & -4 \\ 0 & 1 & -3 & 0 & -7 \\ 0 & 0 & 1 & -3 & -1 \\ 0 & 0 & 0 & 0 & 4 \end{array}\right]$  (10) $\left[\begin{array}{rrrr|r} 1 & -2 & 0 & 3 & 0 \\ 0 & 1 & 0 & -4 & 0 \\ 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 \end{array}\right]$

#### 解答
(9) 最後一列是 $0 = 4$,**無解**(書後解答:No solutions)。

(10) 三角形式,對角線都是 1,沒有矛盾。由下往上:$x_4 = 0$、$x_3 = 0$、$x_2 = 4x_4 = 0$、$x_1 = 2x_2 - 3x_4 = 0$。**唯一解** $(0, 0, 0, 0)$。

### 照做 · Lay 1.1 Exercises 19–20
Determine if the systems are consistent. Do not completely solve the systems.

(19) $x_1 + 3x_3 = 2,\;\; x_2 - 3x_4 = 3,\;\; -2x_2 + 3x_3 + 2x_4 = 1,\;\; 3x_1 + 7x_4 = -5$

(20) $x_1 - 2x_4 = -3,\;\; 2x_2 + 2x_3 = 0,\;\; x_3 + 3x_4 = 1,\;\; -2x_1 + 3x_2 + 2x_3 + x_4 = 5$

#### 解答
(19) $R_3 \leftarrow R_3 + 2R_2$:$[\,0 \;\; 0 \;\; 3 \;\; {-4} \mid 7\,]$;$R_4 \leftarrow R_4 - 3R_1$:$[\,0 \;\; 0 \;\; {-9} \;\; 7 \mid {-11}\,]$;$R_4 \leftarrow R_4 + 3R_3$:$[\,0 \;\; 0 \;\; 0 \;\; {-5} \mid 10\,]$。三角形式、對角線都不是 0、沒有矛盾 → **相容**(而且唯一;書後解答:Consistent)。

(20) $R_4 \leftarrow R_4 + 2R_1$:$[\,0 \;\; 3 \;\; 2 \;\; {-3} \mid {-1}\,]$;$R_2 \leftarrow \tfrac12 R_2$:$[\,0 \;\; 1 \;\; 1 \;\; 0 \mid 0\,]$;$R_4 \leftarrow R_4 - 3R_2$:$[\,0 \;\; 0 \;\; {-1} \;\; {-3} \mid {-1}\,]$;$R_4 \leftarrow R_4 + R_3$:$[\,0 \;\; 0 \;\; 0 \;\; 0 \mid 0\,]$。最後一列是 $0 = 0$,沒有矛盾 → **相容**。(但對角線出現 0,$x_4$ 可以自由取值,所以有無限多解;這要到觀念 5 才完整說明。)

#### 備註
第 20 題是很好的伏筆:相容但「不唯一」。可以先讓學生注意到最後一列 $0 = 0$,觀念 5 再回收。

### 是非 · Lay 1.1 Exercise 33
**(T/F)** Two fundamental questions about a linear system involve existence and uniqueness.

#### 解答
**True.** 課本 p. 31 的方框:解存在嗎?存在的話唯一嗎?

### 變化 · Lay 1.1 Exercises 23–24
Determine the value(s) of $h$ such that the matrix is the augmented matrix of a consistent linear system.

(23) $\left[\begin{array}{rr|r} 1 & h & 4 \\ 3 & 6 & 8 \end{array}\right]$  (24) $\left[\begin{array}{rr|r} 1 & h & -3 \\ -2 & 4 & 6 \end{array}\right]$

#### 解答
(23) $R_2 \leftarrow R_2 - 3R_1$:$[\,0 \;\; 6 - 3h \mid {-4}\,]$。若 $6 - 3h = 0$(即 $h = 2$),這列是 $0 = -4$,矛盾;否則可以解出 $x_2$。所以 **$h \neq 2$**(書後解答相同)。

(24) $R_2 \leftarrow R_2 + 2R_1$:$[\,0 \;\; 4 + 2h \mid 0\,]$。右邊是 0,就算 $4 + 2h = 0$ 也只是 $0 = 0$,不會矛盾。所以**所有 $h$** 都相容。

### 變化 · Lay 1.1 Exercises 25–26
Determine the value(s) of $h$ such that the matrix is the augmented matrix of a consistent linear system.

(25) $\left[\begin{array}{rr|r} 1 & 3 & -2 \\ -4 & h & 8 \end{array}\right]$  (26) $\left[\begin{array}{rr|r} 3 & -4 & h \\ -6 & 8 & 9 \end{array}\right]$

#### 解答
(25) $R_2 \leftarrow R_2 + 4R_1$:$[\,0 \;\; h + 12 \mid 0\,]$。右邊是 0,不會矛盾,**所有 $h$** 都相容(書後解答:All $h$)。

(26) $R_2 \leftarrow R_2 + 2R_1$:$[\,0 \;\; 0 \mid 9 + 2h\,]$。左邊已經全是 0,要相容必須 $9 + 2h = 0$,所以 **$h = -\tfrac92$**。

### 變化 · Lay 1.1 Practice Problem 4
For what values of $h$ and $k$ is the following system consistent? $2x_1 - x_2 = h,\;\; -6x_1 + 3x_2 = k$.

#### 解答
把第 2 式加上第 1 式的 3 倍:$0 = k + 3h$。若 $k + 3h \neq 0$ 就無解。所以相容的條件是 **$k + 3h = 0$**(課本 p. 37)。

幾何上:兩條線斜率都是 2,只有在截距也相同(也就是同一條線)時才有共同點。

### 挑戰 · Lay 1.1 Exercise 35
Find an equation involving $g$, $h$, and $k$ that makes this augmented matrix correspond to a consistent system:

$$\left[\begin{array}{rrr|r} 1 & -3 & 5 & g \\ 0 & 2 & -3 & h \\ -3 & 5 & -9 & k \end{array}\right]$$

#### 解答
$R_3 \leftarrow R_3 + 3R_1$:$[\,0 \;\; {-4} \;\; 6 \mid k + 3g\,]$;$R_3 \leftarrow R_3 + 2R_2$:$[\,0 \;\; 0 \;\; 0 \mid k + 3g + 2h\,]$。要相容,這列不能是 $0 = $ 非零數,所以 **$k + 3g + 2h = 0$**(書後解答相同)。

### 挑戰 · Lay 1.1 Exercises 37–38
(37) Suppose the system $x_1 + 5x_2 = f,\;\; cx_1 + dx_2 = g$ is consistent for all possible values of $f$ and $g$. What can you say about the coefficients $c$ and $d$? Justify your answer.

(38) Suppose $a$, $b$, $c$, and $d$ are constants such that $a$ is not zero and the system $ax_1 + bx_2 = f,\;\; cx_1 + dx_2 = g$ is consistent for all possible values of $f$ and $g$. What can you say about the numbers $a$, $b$, $c$, and $d$? Justify your answer.

#### 解答
(37) $R_2 \leftarrow R_2 - cR_1$:$[\,0 \;\; d - 5c \mid g - cf\,]$。如果 $d - 5c = 0$,那麼只要選 $f, g$ 使 $g - cf \neq 0$,就會得到矛盾。題目要求「所有 $f, g$ 都相容」,所以必須 **$d \neq 5c$**(書後解答相同)。

(38) $R_2 \leftarrow R_2 - \tfrac{c}{a}R_1$(可以除以 $a$,因為 $a \neq 0$):$\left[\,0 \;\; d - \tfrac{bc}{a} \mid g - \tfrac{c}{a}f\,\right]$。同理必須 $d - \tfrac{bc}{a} \neq 0$,乘以 $a$ 得 **$ad - bc \neq 0$**。

#### 備註
$ad - bc$ 就是第 8 週的 $2 \times 2$ 行列式。這題可以當成行列式的第一個伏筆,之後回頭指給學生看。

## 驗算
```check
Matrix([[0, 1, -4, 8], [2, -3, 2, 1], [4, -8, 12, 1]]).rref()[1] == (0, 1, 3)
Matrix([[4, -8, 12, 1]]) - 2*Matrix([[2, -3, 2, 1]]) == Matrix([[0, -2, 8, -1]])
Matrix([[0, -2, 8, -1]]) + 2*Matrix([[0, 1, -4, 8]]) == Matrix([[0, 0, 0, 15]])
Matrix([[1, 5, 2, -6], [0, 4, -7, 2], [0, 0, 5, 0]]).rref()[1] == (0, 1, 2)
Matrix([[1, 7, 3, -4], [0, 1, -1, 3], [0, 0, 0, 1], [0, 0, 1, -2]]).rref()[1] == (0, 1, 2, 3)
Matrix([[1, 1, 5, 0], [0, 1, 9, 0], [0, 0, 7, -7]]).rref()[0][:, 3] == Matrix([-4, 9, -1])
Matrix([[1, -1, 0, 0, -4], [0, 1, -3, 0, -7], [0, 0, 1, -3, -1], [0, 0, 0, 0, 4]]).rref()[1][-1] == 4
Matrix([[1, -2, 0, 3, 0], [0, 1, 0, -4, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]]).rref()[0][:, 4] == zeros(4, 1)
Matrix([[1, 0, 3, 0, 2], [0, 1, 0, -3, 3], [0, -2, 3, 2, 1], [3, 0, 0, 7, -5]]).rref()[1] == (0, 1, 2, 3)
Matrix([[1, 0, 0, -2, -3], [0, 2, 2, 0, 0], [0, 0, 1, 3, 1], [-2, 3, 2, 1, 5]]).rref()[1] == (0, 1, 2)
Matrix([[1, h, 4], [3, 6, 8]]).echelon_form()[1, :] == Matrix([[0, 6 - 3*h, -4]])
Matrix([[1, h, -3], [-2, 4, 6]]).echelon_form()[1, 2] == 0
Matrix([[1, 3, -2], [-4, h, 8]]).echelon_form()[1, 2] == 0
solve(9 + 2*h, h) == [Rational(-9, 2)]
expand(Matrix([[1, -3, 5, g], [0, 2, -3, h], [-3, 5, -9, k]]).echelon_form()[2, 3] / 2) == 3*g + 2*h + k
Matrix([[c, d, g]]) - c*Matrix([[1, 5, f]]) == Matrix([[0, d - 5*c, g - c*f]])
expand(a*(Matrix([[c, d, g]]) - (c/a)*Matrix([[a, b, f]]))[1]) == a*d - b*c
```
