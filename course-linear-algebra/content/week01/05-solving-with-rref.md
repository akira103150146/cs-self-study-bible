---
title_en: Solutions of Linear Systems and the Existence and Uniqueness Theorem
title_zh: 從 RREF 讀出解:一般解與存在唯一性定理
sub: Two questions decide everything — is the last column a pivot column? any free variables?
level: mid
source: Lay 1.2
lab_hook: "`rref()` 回傳的 pivots:最後一行的索引在不在裡面?pivot 個數等不等於未知數個數?"
---
## 觀念
In the reduced echelon form of an augmented matrix, the variables corresponding to pivot columns are called **basic variables**; the other variables are called **free variables**. Whenever a system is consistent, the solution set can be described explicitly by solving the reduced system of equations for the basic variables in terms of the free variables. Such a description, in which the free variables act as parameters, is a **parametric description** of the solution set, also called the **general solution**.

**Theorem 2 (Existence and Uniqueness Theorem).** A linear system is consistent if and only if the rightmost column of the augmented matrix is *not* a pivot column — that is, if and only if an echelon form of the augmented matrix has *no* row of the form

$$[\,0 \;\; \cdots \;\; 0 \;\; b\,] \quad \text{with } b \text{ nonzero.}$$

If a linear system is consistent, then the solution set contains either (i) a unique solution, when there are no free variables, or (ii) infinitely many solutions, when there is at least one free variable.

**Using row reduction to solve a linear system:**

1. Write the augmented matrix of the system.
2. Use the row reduction algorithm to obtain an equivalent augmented matrix in echelon form. Decide whether the system is consistent. If there is no solution, stop; otherwise, go to the next step.
3. Continue row reduction to obtain the reduced echelon form.
4. Write the system of equations corresponding to the matrix obtained in step 3.
5. Rewrite each nonzero equation from step 4 so that its one basic variable is expressed in terms of any free variables appearing in the equation.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| basic variable | 基本變數 | 對應 pivot 行的未知數(也有書叫 leading variable) |
| free variable | 自由變數 | 不在 pivot 行的未知數,可以任意取值 |
| general solution | 一般解(通解) | 用自由變數表示所有解的寫法 |
| parametric description | 參數表示 | 自由變數當參數;每給一組參數就得到一個解 |
| back-substitution | 回代 | 從梯形由下往上代入求解(電腦常用) |
| flop | 浮點運算 | 一次 $+,-,\times,\div$;用來衡量演算法的計算量 |
| underdetermined system | 欠定系統 | 方程式比未知數少 |
| overdetermined system | 超定系統 | 方程式比未知數多 |

## 白話說
化成 RREF 之後,解就寫在臉上。**照順序問兩個問題**:

![每一題都照這兩個問題的順序判斷。](decide.svg)

1. **最後一行(常數那一行)有沒有 pivot?** 有的話代表出現了「$0 = $ 非零數」這種列,**無解**,直接收工。
2. **有沒有自由變數?** pivot 行對應的未知數叫**基本變數**,其他的叫**自由變數**。自由變數可以任意取值,基本變數再跟著算出來。沒有自由變數 → **唯一解**;有任何一個 → **無限多解**。

一般解的寫法:每個基本變數寫成「常數 + 自由變數的組合」,自由變數旁邊寫 *is free*。**每個未知數都要交代**——包括 $x_5 = 7$ 這種已經定下來的,以及完全沒出現在方程式裡的(它也是自由變數)。

「$x_3$ is free」的意思是:你可以自由選 $x_3$ 的值;選定之後,其他未知數就被公式決定了。**每一個不同的 $x_3$ 都對應一個不同的解,而且每一個解都來自某個 $x_3$。**

## 幾何意義
一般解就是解集的「形狀」:

- 一個自由變數 → 解集是一條**直線**。例 1 的解 $x_1 = 1 + 5x_3$、$x_2 = 4 - x_3$ 在三維空間裡是一條線:$x_3 = 0$ 時在 $(1, 4, 0)$,$x_3 = 1$ 時在 $(6, 3, 1)$,每多 1,就往同一個方向走一步。這條線正是兩個平面 $x_1 - 5x_3 = 1$ 與 $x_2 + x_3 = 4$ 的**交線**(課本 p. 49 的立體圖)。
- 兩個自由變數 → 解集是一個**平面**。
- 沒有自由變數 → 解集是一個**點**。

自由變數的個數,就是解集的「維度」——這個想法到第 7 週會正式變成「維度」與「零空間」。

## 在資工哪裡用
程式解方程組時,要先判斷是哪一種情況,再決定怎麼回報。NumPy 的 `np.linalg.solve` **只處理唯一解**的情況,遇到無解或無限多解會直接報錯(實作課會親眼看到)。

未知數比方程式多的時候(例如模型參數比資料點多),一定會有自由變數——這正是機器學習裡「參數太多、答案不唯一」的根源。實務上會再加條件(例如要求參數越小越好)從無限多解裡挑一個,第 14 週會再遇到。

## 數值筆記
一般來說,列化簡的**前進階段比回代階段花更多時間**。演算法的計算量通常用 **flop**(浮點運算次數)衡量,一個 flop 是兩個浮點數的一次 $+, -, \times, \div$。

對一個 $n \times (n+1)$ 的矩陣,化成梯形大約需要 $\tfrac{2n^3}{3} + \tfrac{n^2}{2} - \tfrac{7n}{6}$ 個 flop;$n$ 稍大(例如 $n \geq 30$)時約為 $\tfrac{2n^3}{3}$。相比之下,再化成 RREF 最多只需要 $n^2$ 個 flop。(改寫自 Lay 1.2 Numerical Note)

$n$ 變成 10 倍,前進階段的計算量變成約 1000 倍——這就是「$O(n^3)$」。實作課會實際量給你看。

## 合理性檢查
每一個增廣矩陣都對應一個方程組。例如把 $\left[\begin{array}{rrr|r} 1 & -2 & 1 & 2 \\ 1 & -1 & 2 & 5 \\ 0 & 1 & 1 & 3 \end{array}\right]$ 化成 $\left[\begin{array}{rrr|r} 1 & 0 & 3 & 8 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right]$,得到一般解 $x_1 = 8 - 3x_3$、$x_2 = 3 - x_3$、$x_3$ is free。

檢查方法:**把一般解直接代回原方程式,自由變數留著不用代數字**。

$$\begin{aligned} (8 - 3x_3) - 2(3 - x_3) + x_3 &= 8 - 3x_3 - 6 + 2x_3 + x_3 = 2 \;\checkmark \\ (8 - 3x_3) - (3 - x_3) + 2x_3 &= 8 - 3x_3 - 3 + x_3 + 2x_3 = 5 \;\checkmark \\ (3 - x_3) + x_3 &= 3 \;\checkmark \end{aligned}$$

$x_3$ 全部消掉、三條都成立,就可以確定答案是對的。(改寫自 Lay 1.2 Reasonable Answers)

## 原理
**證明 Theorem 2**(看 RREF 就夠了,因為列運算不改變解集):

- **最後一行是 pivot 行**:那一列長得像 $[\,0 \;\cdots\; 0 \mid 1\,]$,代表 $0 = 1$,沒有任何解。
- **最後一行不是 pivot 行**:每一個非零列都恰好有一個基本變數(RREF 讓每個基本變數只出現在一條方程式裡),而且可以寫成「常數 + 自由變數的組合」。自由變數隨便給值(例如全給 0),基本變數就跟著確定,所以**至少有一個解**。
- 有解時,若**沒有自由變數**,每個未知數都被直接決定,解唯一;若**有自由變數**,它的每一個取值都對應一個不同的解,所以有無限多解。

**為什麼一定要用自由變數當參數?** 同一個解集可以有很多種參數表示(課本 p. 44 的例子:也可以拿 $x_2$ 當參數)。課本約定**一律用自由變數當參數**,書後解答也照這個慣例,這樣答案才比得起來。

**回代(back-substitution)**:電腦通常不做完整的 RREF,而是從梯形由下往上代入(課本 p. 44)。計算量和我們的回代階段一樣,但手算時用矩陣格式做回代階段比較不容易出錯。

**pivot 個數的上限**:每一列最多一個 pivot,每一行也最多一個 pivot。所以 pivot 個數 $\le$ 列數,也 $\le$ 行數。這是挑戰題 35–43 的共同工具。

## 老師講解
### 例 1 · Lay 1.2(p. 42–43)
Suppose the augmented matrix of a linear system has been changed into the equivalent reduced echelon form $\left[\begin{array}{rrr|r} 1 & 0 & -5 & 1 \\ 0 & 1 & 1 & 4 \\ 0 & 0 & 0 & 0 \end{array}\right]$. Describe the solution set.

1. **有幾個未知數?** 增廣矩陣有 4 行,最後一行是常數,所以有 3 個未知數 $x_1, x_2, x_3$。
2. **問題 1:最後一行有沒有 pivot?** 沒有。第 3 列全是 0,代表 $0 = 0$,永遠成立,不是矛盾。所以**有解**。
3. **問題 2:有沒有自由變數?** pivot 在第 1、2 行,所以 $x_1$、$x_2$ 是基本變數;第 3 行沒有 pivot,**$x_3$ 是自由變數**。有自由變數 → **無限多解**。
4. **翻回方程式**:$x_1 - 5x_3 = 1$、$x_2 + x_3 = 4$、$0 = 0$(第三條不提供任何限制,忽略)。
5. **每條方程式解出它的基本變數**(RREF 保證每個基本變數只出現在一條方程式裡):
   $$x_1 = 1 + 5x_3, \qquad x_2 = 4 - x_3, \qquad x_3 \text{ is free.}$$
6. **舉例驗證**:$x_3 = 0$ 得 $(1, 4, 0)$;$x_3 = 1$ 得 $(6, 3, 1)$。代回 $x_1 - 5x_3 = 1$:$6 - 5 = 1$ ✓;$x_2 + x_3 = 4$:$3 + 1 = 4$ ✓。每一個不同的 $x_3$ 都給出不同的解。

### 例 2 · Lay 1.2 Example 4
Find the general solution of the linear system whose augmented matrix has been reduced to

$$\left[\begin{array}{rrrrr|r} 1 & 6 & 2 & -5 & -2 & -4 \\ 0 & 0 & 2 & -8 & -1 & 3 \\ 0 & 0 & 0 & 0 & 1 & 7 \end{array}\right]$$

1. 這已經是梯形,但要解出基本變數,得先化成 **RREF**。有 6 行,所以有 5 個未知數。
2. **從最右邊的 pivot 開始往上消**:第 3 列的 pivot 在第 5 行,把上面兩列第 5 行消成 0:$R_1 \leftarrow R_1 + 2R_3$(第 1 列最後變成 $-4 + 14 = 10$)、$R_2 \leftarrow R_2 + R_3$(第 2 列最後變成 $3 + 7 = 10$):
   $$\left[\begin{array}{rrrrr|r} 1 & 6 & 2 & -5 & 0 & 10 \\ 0 & 0 & 2 & -8 & 0 & 10 \\ 0 & 0 & 0 & 0 & 1 & 7 \end{array}\right]$$
3. **下一個 pivot 在第 2 列第 3 行**,是 2,先縮放成 1:$R_2 \leftarrow \tfrac12 R_2$,得 $[\,0 \;\; 0 \;\; 1 \;\; {-4} \;\; 0 \mid 5\,]$。
4. **消掉它上面**:$R_1 \leftarrow R_1 - 2R_2$:$2 - 2 = 0$、$-5 + 8 = 3$、$10 - 10 = 0$:
   $$\left[\begin{array}{rrrrr|r} 1 & 6 & 0 & 3 & 0 & 0 \\ 0 & 0 & 1 & -4 & 0 & 5 \\ 0 & 0 & 0 & 0 & 1 & 7 \end{array}\right]$$
5. **找基本變數與自由變數**:pivot 行是第 1、3、5 行,所以 $x_1, x_3, x_5$ 是基本變數;**$x_2$、$x_4$ 是自由變數**。最後一行沒有 pivot → 有解;有自由變數 → 無限多解。
6. **翻回方程式**:$x_1 + 6x_2 + 3x_4 = 0$、$x_3 - 4x_4 = 5$、$x_5 = 7$。
7. **解出基本變數**,並把每個未知數都交代清楚:
   $$x_1 = -6x_2 - 3x_4, \quad x_2 \text{ is free}, \quad x_3 = 5 + 4x_4, \quad x_4 \text{ is free}, \quad x_5 = 7.$$
8. 注意 $x_5$ 已經被第三條方程式定死了,不含任何參數;兩個自由變數表示解集是五維空間裡的一個「平面」。

### 例 3 · Lay 1.2 Example 5
Determine the existence and uniqueness of the solutions to the system $3x_2 - 6x_3 + 6x_4 + 4x_5 = -5,\;\; 3x_1 - 7x_2 + 8x_3 - 5x_4 + 8x_5 = 9,\;\; 3x_1 - 9x_2 + 12x_3 - 9x_4 + 6x_5 = 15$.

1. 這個方程組的增廣矩陣,就是觀念 4 例 3 化簡過的那個矩陣。前進階段已經得到梯形:
   $$\left[\begin{array}{rrrrr|r} 3 & -9 & 12 & -9 & 6 & 15 \\ 0 & 2 & -4 & 4 & 2 & -6 \\ 0 & 0 & 0 & 0 & 1 & 4 \end{array}\right]$$
2. **存在性**:梯形裡沒有 $[\,0 \;\cdots\; 0 \mid b\,]$($b \neq 0$)這種列,最後一行不是 pivot 行 → **有解**。我們甚至不必做到 RREF 就知道。
3. **唯一性**:pivot 在第 1、2、5 行,基本變數是 $x_1, x_2, x_5$;**$x_3$、$x_4$ 是自由變數**。有自由變數 → **解不唯一**,有無限多解。
4. 重點:**非簡化的梯形拿來「解」方程組不好用,但拿來回答存在性與唯一性剛剛好**(課本 p. 45)。要完整寫出一般解,才需要繼續化到 RREF(觀念 4 例 3 已經做過)。

## 易錯點
- 把全 0 列 $[\,0 \;\; 0 \;\; 0 \mid 0\,]$ 誤當成無解。$0 = 0$ 永遠成立;真正的無解是 $[\,0 \;\cdots\; 0 \mid b\,]$ 而且 $b \neq 0$。
- 以為「有自由變數代表題目算錯了」。自由變數是很正常的結果,表示解有無限多個。
- 一般解漏掉某個未知數,尤其是完全沒出現在方程式裡的(Exercise 8 的 $x_3$)。
- 把自由變數寫成別的自由變數的函數,例如 $x_3 = 1 + x_2$(課本 p. 48 的「Incorrect solution」):這樣會讓人以為 $x_2$、$x_3$ 都是自由的。
- 在**梯形**(還沒化到 RREF)上直接寫一般解,基本變數還會互相牽連。

## 教學提示
把觀念的流程圖畫在黑板角落,整堂課都不要擦。每一題都照流程問兩句:「最後一行有沒有 pivot?」「有沒有自由變數?」數理弱的學生需要**固定的判斷順序**,而不是每一題重新想。

一般解寫完,一定要讓學生做一次「合理性檢查」:把一般解整個代回原方程式,自由變數留著,看它們會不會全部消掉。這會讓「自由變數真的可以隨便選」變得具體。

課堂建議做:照做 1–3;是非全部;變化挑 Exercises 19–20(符號題)與 21–24 其中兩題;挑戰題 35–38 很適合當討論題。

## 練習
### 照做 · Lay 1.2 Practice Problem 1
Find the general solution of the linear system whose augmented matrix is $\left[\begin{array}{rrr|r} 1 & -3 & -5 & 0 \\ 0 & 1 & -1 & -1 \end{array}\right]$.

#### 解答
$R_1 \leftarrow R_1 + 3R_2$:$[\,1 \;\; 0 \;\; {-8} \mid {-3}\,]$。RREF 對應 $x_1 - 8x_3 = -3$、$x_2 - x_3 = -1$,基本變數 $x_1, x_2$:

$$x_1 = -3 + 8x_3, \qquad x_2 = -1 + x_3, \qquad x_3 \text{ is free.}$$

幾何上,這是兩個平面的交線(課本 p. 49 的圖)。

### 照做 · Lay 1.2 Exercises 7–8
Find the general solutions of the systems whose augmented matrices are given.

(7) $\left[\begin{array}{rrr|r} 1 & 2 & 3 & 4 \\ 4 & 8 & 9 & 4 \end{array}\right]$  (8) $\left[\begin{array}{rrr|r} 1 & 4 & 0 & 7 \\ 2 & 7 & 0 & 11 \end{array}\right]$

#### 解答
(7) $R_2 \leftarrow R_2 - 4R_1$:$[\,0 \;\; 0 \;\; {-3} \mid {-12}\,]$,$R_2 \leftarrow -\tfrac13 R_2$:$x_3 = 4$;$R_1 \leftarrow R_1 - 3R_2$:$[\,1 \;\; 2 \;\; 0 \mid {-8}\,]$。pivot 在第 1、3 行:
$$x_1 = -8 - 2x_2, \quad x_2 \text{ is free}, \quad x_3 = 4.$$
(書後解答相同)

(8) $R_2 \leftarrow R_2 - 2R_1$:$[\,0 \;\; {-1} \;\; 0 \mid {-3}\,]$,得 $x_2 = 3$;$R_1 \leftarrow R_1 - 4R_2$:$x_1 = -5$。pivot 在第 1、2 行,**第 3 行全是 0,$x_3$ 沒出現在任何方程式裡,但它仍然是自由變數**:
$$x_1 = -5, \quad x_2 = 3, \quad x_3 \text{ is free.}$$

#### 備註
Exercise 8 是陷阱題:學生常忘了交代 $x_3$。

### 照做 · Lay 1.2 Exercises 9–10
Find the general solutions of the systems whose augmented matrices are given.

(9) $\left[\begin{array}{rrr|r} 0 & 1 & -6 & 5 \\ 1 & -2 & 7 & -4 \end{array}\right]$  (10) $\left[\begin{array}{rrr|r} 1 & -2 & -1 & 3 \\ 3 & -6 & -2 & 2 \end{array}\right]$

#### 解答
(9) 先交換兩列:$\left[\begin{array}{rrr|r} 1 & -2 & 7 & -4 \\ 0 & 1 & -6 & 5 \end{array}\right]$;$R_1 \leftarrow R_1 + 2R_2$:$[\,1 \;\; 0 \;\; {-5} \mid 6\,]$。
$$x_1 = 6 + 5x_3, \quad x_2 = 5 + 6x_3, \quad x_3 \text{ is free.}$$
(書後解答相同。代回驗算見 Exercise 15。)

(10) $R_2 \leftarrow R_2 - 3R_1$:$[\,0 \;\; 0 \;\; 1 \mid {-7}\,]$;$R_1 \leftarrow R_1 + R_2$:$[\,1 \;\; {-2} \;\; 0 \mid {-4}\,]$。pivot 在第 1、3 行:
$$x_1 = -4 + 2x_2, \quad x_2 \text{ is free}, \quad x_3 = -7.$$

### 是非 · Lay 1.2 Exercise 29
**(T/F)** A basic variable in a linear system is a variable that corresponds to a pivot column in the coefficient matrix.

#### 解答
**True.** 課本 p. 42:對應到 pivot 行的變數叫基本變數。

### 是非 · Lay 1.2 Exercise 31
**(T/F)** Finding a parametric description of the solution set of a linear system is the same as *solving* the system.

#### 解答
**False.** 課本 p. 44:「解方程組」是**找出解集的參數表示,或判定解集是空集合**。方程組不相容時沒有參數表示可寫,但仍然算是解完了。

#### 備註
這題有爭議空間,課堂上可以讓學生說出自己的理由;關鍵是有沒有想到「無解」的情況。

### 是非 · Lay 1.2 Exercise 32
**(T/F)** Whenever a system has free variables, the solution set contains a unique solution.

#### 解答
**False.** 若方程組相容又有自由變數,解集有**無限多**個解(Theorem 2)。

### 是非 · Lay 1.2 Exercise 33
**(T/F)** If one row in an echelon form of an augmented matrix is $[\,0 \;\; 0 \;\; 0 \;\; 0 \;\; 5\,]$, then the associated linear system is inconsistent.

#### 解答
**True.** 這一列代表 $0 = 5$,矛盾,方程組不相容(Theorem 2)。

### 是非 · Lay 1.2 Exercise 34
**(T/F)** A general solution of a system is an explicit description of all solutions of the system.

#### 解答
**True.** 一般解用參數明確描述**所有**的解(課本 p. 43–44)。

### 變化 · Lay 1.2 Exercises 11–12
Find the general solutions of the systems whose augmented matrices are given.

(11) $\left[\begin{array}{rrr|r} 3 & -4 & 2 & 0 \\ -9 & 12 & -6 & 0 \\ -6 & 8 & -4 & 0 \end{array}\right]$  (12) $\left[\begin{array}{rrrr|r} 1 & -7 & 0 & 6 & 5 \\ 0 & 0 & 1 & -2 & -3 \\ -1 & 7 & -4 & 2 & 7 \end{array}\right]$

#### 解答
(11) $R_2 \leftarrow R_2 + 3R_1$、$R_3 \leftarrow R_3 + 2R_1$ 都變成全 0;$R_1 \leftarrow \tfrac13 R_1$:$[\,1 \;\; {-\tfrac43} \;\; \tfrac23 \mid 0\,]$。只有一個 pivot,$x_2$、$x_3$ 都自由:
$$x_1 = \tfrac43 x_2 - \tfrac23 x_3, \quad x_2 \text{ is free}, \quad x_3 \text{ is free.}$$
(書後解答相同。三條方程式其實是同一個平面,解集就是那個平面。)

(12) $R_3 \leftarrow R_3 + R_1$:$[\,0 \;\; 0 \;\; {-4} \;\; 8 \mid 12\,]$;$R_3 \leftarrow R_3 + 4R_2$:全 0。pivot 在第 1、3 行:
$$x_1 = 5 + 7x_2 - 6x_4, \quad x_2 \text{ is free}, \quad x_3 = -3 + 2x_4, \quad x_4 \text{ is free.}$$

### 變化 · Lay 1.2 Exercises 13–14
Find the general solutions of the systems whose augmented matrices are given.

(13) $\left[\begin{array}{rrrrr|r} 1 & -3 & 0 & -1 & 0 & -2 \\ 0 & 1 & 0 & 0 & -4 & 1 \\ 0 & 0 & 0 & 1 & 9 & -4 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{array}\right]$  (14) $\left[\begin{array}{rrrrr|r} 1 & 2 & -5 & -4 & 0 & -5 \\ 0 & 1 & -6 & -4 & 0 & 2 \\ 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{array}\right]$

#### 解答
(13) $R_1 \leftarrow R_1 + R_3$:$[\,1 \;\; {-3} \;\; 0 \;\; 0 \;\; 9 \mid {-6}\,]$;$R_1 \leftarrow R_1 + 3R_2$:$[\,1 \;\; 0 \;\; 0 \;\; 0 \;\; {-3} \mid {-3}\,]$。pivot 在第 1、2、4 行:
$$x_1 = -3 + 3x_5, \quad x_2 = 1 + 4x_5, \quad x_3 \text{ is free}, \quad x_4 = -4 - 9x_5, \quad x_5 \text{ is free.}$$
(書後解答相同。$x_3$ 的那一行全是 0,和 Exercise 8 一樣容易漏掉。)

(14) $R_1 \leftarrow R_1 - 2R_2$:$[\,1 \;\; 0 \;\; 7 \;\; 4 \;\; 0 \mid {-9}\,]$。pivot 在第 1、2、5 行:
$$x_1 = -9 - 7x_3 - 4x_4, \quad x_2 = 2 + 6x_3 + 4x_4, \quad x_3 \text{ is free}, \quad x_4 \text{ is free}, \quad x_5 = 0.$$

### 變化 · Lay 1.2 Exercises 15–18
You may find it helpful to review the information in the Reasonable Answers box from this section before answering Exercises 15–18.

(15) Write down the equations corresponding to the augmented matrix in Exercise 9 and verify your answer to Exercise 9 is correct by substituting the solutions you obtained back into the original equations.

(16) Write down the equations corresponding to the augmented matrix in Exercise 10 and verify your answer to Exercise 10 is correct by substituting the solutions you obtained back into the original equations.

(17) Write down the equations corresponding to the augmented matrix in Exercise 11 and verify your answer to Exercise 11 is correct by substituting the solutions you obtained back into the original equations.

(18) Write down the equations corresponding to the augmented matrix in Exercise 12 and verify your answer to Exercise 12 is correct by substituting the solutions you obtained back into the original equations.

#### 解答
做法和本觀念的「合理性檢查」一樣:**把一般解整個代回原方程式,自由變數留著**,看它們會不會全部消掉。

(15) Exercise 9 的方程式是 $x_2 - 6x_3 = 5$、$x_1 - 2x_2 + 7x_3 = -4$。代入 $x_1 = 6 + 5x_3$、$x_2 = 5 + 6x_3$:
$$\begin{aligned} (5 + 6x_3) - 6x_3 &= 5 \;\checkmark \\ (6 + 5x_3) - 2(5 + 6x_3) + 7x_3 &= 6 + 5x_3 - 10 - 12x_3 + 7x_3 = -4 \;\checkmark \end{aligned}$$
(書後解答相同)

(16) Exercise 10 的方程式是 $x_1 - 2x_2 - x_3 = 3$、$3x_1 - 6x_2 - 2x_3 = 2$。代入 $x_1 = -4 + 2x_2$、$x_3 = -7$:
$$\begin{aligned} (-4 + 2x_2) - 2x_2 - (-7) &= 3 \;\checkmark \\ 3(-4 + 2x_2) - 6x_2 - 2(-7) &= -12 + 14 = 2 \;\checkmark \end{aligned}$$

(17) Exercise 11 的方程式是 $3x_1 - 4x_2 + 2x_3 = 0$、$-9x_1 + 12x_2 - 6x_3 = 0$、$-6x_1 + 8x_2 - 4x_3 = 0$。代入 $x_1 = \tfrac43 x_2 - \tfrac23 x_3$:
$$\begin{aligned} 3\left(\tfrac43 x_2 - \tfrac23 x_3\right) - 4x_2 + 2x_3 &= 4x_2 - 2x_3 - 4x_2 + 2x_3 = 0 \;\checkmark \\ -9\left(\tfrac43 x_2 - \tfrac23 x_3\right) + 12x_2 - 6x_3 &= -12x_2 + 6x_3 + 12x_2 - 6x_3 = 0 \;\checkmark \\ -6\left(\tfrac43 x_2 - \tfrac23 x_3\right) + 8x_2 - 4x_3 &= -8x_2 + 4x_3 + 8x_2 - 4x_3 = 0 \;\checkmark \end{aligned}$$
(書後解答相同)

(18) Exercise 12 的方程式是 $x_1 - 7x_2 + 6x_4 = 5$、$x_3 - 2x_4 = -3$、$-x_1 + 7x_2 - 4x_3 + 2x_4 = 7$。代入 $x_1 = 5 + 7x_2 - 6x_4$、$x_3 = -3 + 2x_4$:
$$\begin{aligned} (5 + 7x_2 - 6x_4) - 7x_2 + 6x_4 &= 5 \;\checkmark \\ (-3 + 2x_4) - 2x_4 &= -3 \;\checkmark \\ -(5 + 7x_2 - 6x_4) + 7x_2 - 4(-3 + 2x_4) + 2x_4 &= -5 + 12 = 7 \;\checkmark \end{aligned}$$

#### 備註
學生最常犯的錯是代入時只代一個數字(例如 $x_3 = 0$)就說驗完了。要強調:自由變數要**整個留著**,消得掉才代表對所有的解都成立。

### 變化 · Lay 1.2 Practice Problems 2–3
(2) Find the general solution of the system $x_1 - 2x_2 - x_3 + 3x_4 = 0,\;\; -2x_1 + 4x_2 + 5x_3 - 5x_4 = 3,\;\; 3x_1 - 6x_2 - 6x_3 + 8x_4 = 2$.

(3) Suppose a $4 \times 7$ coefficient matrix for a system of equations has 4 pivots. Is the system consistent? If the system is consistent, how many solutions are there?

#### 解答
(2) $R_2 \leftarrow R_2 + 2R_1$:$[\,0 \;\; 0 \;\; 3 \;\; 1 \mid 3\,]$;$R_3 \leftarrow R_3 - 3R_1$:$[\,0 \;\; 0 \;\; {-3} \;\; {-1} \mid 2\,]$;$R_3 \leftarrow R_3 + R_2$:$[\,0 \;\; 0 \;\; 0 \;\; 0 \mid 5\,]$。最後一列是 $0 = 5$,**不相容,沒有一般解**(課本 p. 49–50)。

(3) 係數矩陣 4 列、4 個 pivot → **每一列都有 pivot**,增廣矩陣的最後一行不可能是 pivot 行 → **相容**。7 個未知數、4 個 pivot → 3 個自由變數 → **無限多解**。

### 變化 · Lay 1.2 Exercises 19–20
Use the notation of Example 1 for matrices in echelon form ($\blacksquare$ = nonzero, $*$ = any value). Suppose each matrix represents the augmented matrix for a system of linear equations. In each case, determine if the system is consistent. If the system is consistent, determine if the solution is unique.

(19a) $\begin{bmatrix} \blacksquare & * & * & * \\ 0 & \blacksquare & * & * \\ 0 & 0 & \blacksquare & 0 \end{bmatrix}$  (19b) $\begin{bmatrix} 0 & \blacksquare & * & * & * \\ 0 & 0 & \blacksquare & * & * \\ 0 & 0 & 0 & 0 & \blacksquare \end{bmatrix}$  (20a) $\begin{bmatrix} \blacksquare & * & * \\ 0 & \blacksquare & * \\ 0 & 0 & 0 \end{bmatrix}$  (20b) $\begin{bmatrix} \blacksquare & * & * & * & * \\ 0 & 0 & \blacksquare & * & * \\ 0 & 0 & 0 & \blacksquare & * \end{bmatrix}$

#### 解答
最後一行是常數行。

- (19a) 最後一行不是 pivot 行 → 相容;3 個未知數都有 pivot → **唯一解**(書後解答相同)。
- (19b) 最後一行是 pivot 行(第 3 列是 $[\,0 \;\cdots\; 0 \mid \blacksquare\,]$)→ **不相容**。
- (20a) 最後一行不是 pivot 行 → 相容;2 個未知數都有 pivot → **唯一解**。
- (20b) 最後一行不是 pivot 行 → 相容;4 個未知數、pivot 在第 1、3、4 行,$x_2$ 自由 → **無限多解**。

### 變化 · Lay 1.2 Exercises 21–22
Determine the value(s) of $h$ such that the matrix is the augmented matrix of a consistent linear system.

(21) $\left[\begin{array}{rr|r} 2 & 3 & h \\ 4 & 6 & 7 \end{array}\right]$  (22) $\left[\begin{array}{rr|r} 1 & -4 & -3 \\ 6 & h & -9 \end{array}\right]$

#### 解答
(21) $R_2 \leftarrow R_2 - 2R_1$:$[\,0 \;\; 0 \mid 7 - 2h\,]$。要相容必須 $7 - 2h = 0$,**$h = \tfrac72$**(書後解答相同)。

(22) $R_2 \leftarrow R_2 - 6R_1$:$[\,0 \;\; h + 24 \mid 9\,]$。若 $h + 24 = 0$,這列是 $0 = 9$,矛盾。所以 **$h \neq -24$**。

### 變化 · Lay 1.2 Exercises 23–24
Choose $h$ and $k$ such that the system has (a) no solution, (b) a unique solution, and (c) many solutions. Give separate answers for each part.

(23) $x_1 + hx_2 = 2,\;\; 4x_1 + 8x_2 = k$  (24) $x_1 + 4x_2 = 5,\;\; 2x_1 + hx_2 = k$

#### 解答
(23) $R_2 \leftarrow R_2 - 4R_1$:$[\,0 \;\; 8 - 4h \mid k - 8\,]$。
- (a) 無解:$8 - 4h = 0$ 且 $k - 8 \neq 0$,即 **$h = 2$、$k \neq 8$**。
- (b) 唯一解:$8 - 4h \neq 0$,即 **$h \neq 2$**($k$ 任意)。
- (c) 無限多解:**$h = 2$、$k = 8$**。

(書後解答相同)

(24) $R_2 \leftarrow R_2 - 2R_1$:$[\,0 \;\; h - 8 \mid k - 10\,]$。
- (a) **$h = 8$、$k \neq 10$**;(b) **$h \neq 8$**;(c) **$h = 8$、$k = 10$**。

### 挑戰 · Lay 1.2 Exercises 35–38
(35) Suppose a $3 \times 5$ *coefficient* matrix for a system has three pivot columns. Is the system consistent? Why or why not?

(36) Suppose a system of linear equations has a $3 \times 5$ *augmented* matrix whose fifth column is a pivot column. Is the system consistent? Why (or why not)?

(37) Suppose the coefficient matrix of a system of linear equations has a pivot position in every row. Explain why the system is consistent.

(38) Suppose the coefficient matrix of a linear system of three equations in three variables has a pivot in each column. Explain why the system has a unique solution.

#### 解答
(35) **相容。** 3 列、3 個 pivot → 每一列都有 pivot(包括最下面一列)。增廣矩陣的 RREF 不可能出現 $[\,0 \;\; 0 \;\; 0 \;\; 0 \;\; 0 \mid 1\,]$,所以最後一行不是 pivot 行(書後解答相同)。

(36) **不相容。** 增廣矩陣的第 5 行就是常數行,它是 pivot 行代表出現 $[\,0 \;\cdots\; 0 \mid b\,]$($b \neq 0$),由 Theorem 2 無解。

(37) 係數矩陣每一列都有 pivot,最下面那一列的 pivot 已經佔掉,常數行沒有位置再放 pivot,所以最後一行不是 pivot 行,由 Theorem 2 相容(書後解答相同)。

(38) $3 \times 3$ 係數矩陣每一行都有 pivot → 3 個 pivot → 每一列也都有 pivot → 由 (37) 相容;又因為每一行都是 pivot 行,**沒有自由變數** → 解唯一。

### 挑戰 · Lay 1.2 Exercises 39–43
(39) Restate the last sentence in Theorem 2 using the concept of pivot columns: "If a linear system is consistent, then the solution is unique if and only if ______."

(40) What would you have to know about the pivot columns in an augmented matrix in order to know that the linear system is consistent and has a unique solution?

(41) A system of linear equations with fewer equations than unknowns is sometimes called an *underdetermined system*. Suppose that such a system happens to be consistent. Explain why there must be an infinite number of solutions.

(42) Give an example of an inconsistent underdetermined system of two equations in three unknowns.

(43) A system of linear equations with more equations than unknowns is sometimes called an *overdetermined system*. Can such a system be consistent? Illustrate your answer with a specific system of three equations in two unknowns.

#### 解答
(39) 「……the solution is unique if and only if **every column of the coefficient matrix is a pivot column**; otherwise, there are infinitely many solutions.」(書後解答相同)

(40) 要知道兩件事:**增廣矩陣的最後一行不是 pivot 行**(相容),而且**其他每一行都是 pivot 行**(沒有自由變數,解唯一)。

(41) 方程式比未知數少 → pivot 個數 ≤ 列數 < 未知數個數 → 至少有一個自由變數。相容時,自由變數的每一個值都給出不同的解,所以有無限多解(書後解答相同)。

(42) 例如 $x_1 + x_2 + x_3 = 1$、$x_1 + x_2 + x_3 = 2$:兩式相減得 $0 = 1$,不相容。(兩個平行的平面。)

(43) **可以。** 例如 $x_1 + x_2 = 2$、$x_1 - x_2 = 0$、$3x_1 + 2x_2 = 5$ 有解 $x_1 = x_2 = 1$(書後解答的例子)。三條線剛好交於同一點。但一般來說,超定系統通常無解——第 14 週的最小平方法就是處理這種情況。

### 挑戰 · Lay 1.2 Exercise 44
Suppose an $n \times (n+1)$ matrix is row reduced to reduced echelon form. Approximately what fraction of the total number of operations (flops) is involved in the backward phase of the reduction when $n = 30$? when $n = 300$?

#### 解答
用數值筆記的數字:前進階段 $\tfrac{2n^3}{3} + \tfrac{n^2}{2} - \tfrac{7n}{6}$ flop,回代階段最多 $n^2$ flop。

- $n = 30$:前進 $18000 + 450 - 35 = 18415$,回代 $900$。比例約 $\tfrac{900}{18415 + 900} \approx 4.7\%$。
- $n = 300$:前進 $18{,}000{,}000 + 45{,}000 - 350 = 18{,}044{,}650$,回代 $90{,}000$。比例約 $\tfrac{90000}{18134650} \approx 0.5\%$。

$n$ 越大,回代階段佔的比例越小(大約 $\tfrac{3}{2n}$):**計算時間幾乎全花在前進階段**。

#### 備註
實作課「解讀」階段會實際量 `np.linalg.solve` 的時間,看到 $n$ 變 2 倍、時間約變 8 倍。

## 驗算
```check
simplify(Matrix([[1, 0, -5], [0, 1, 1]]) * Matrix([1 + 5*t, 4 - t, t]) - Matrix([1, 4])) == zeros(2, 1)
Matrix([[1, 6, 2, -5, -2, -4], [0, 0, 2, -8, -1, 3], [0, 0, 0, 0, 1, 7]]).rref() == (Matrix([[1, 6, 0, 3, 0, 0], [0, 0, 1, -4, 0, 5], [0, 0, 0, 0, 1, 7]]), (0, 2, 4))
simplify(Matrix([[1, 6, 2, -5, -2], [0, 0, 2, -8, -1], [0, 0, 0, 0, 1]]) * Matrix([-6*s - 3*t, s, 5 + 4*t, t, 7]) - Matrix([-4, 3, 7])) == zeros(3, 1)
Matrix([[3, -9, 12, -9, 6, 15], [0, 2, -4, 4, 2, -6], [0, 0, 0, 0, 1, 4]]).rref()[1] == (0, 1, 4)
Matrix([[1, -2, 1, 2], [1, -1, 2, 5], [0, 1, 1, 3]]).rref()[0] == Matrix([[1, 0, 3, 8], [0, 1, 1, 3], [0, 0, 0, 0]])
simplify(Matrix([[1, -2, 1], [1, -1, 2], [0, 1, 1]]) * Matrix([8 - 3*t, 3 - t, t]) - Matrix([2, 5, 3])) == zeros(3, 1)
Matrix([[1, -3, -5, 0], [0, 1, -1, -1]]).rref()[0] == Matrix([[1, 0, -8, -3], [0, 1, -1, -1]])
Matrix([[1, 2, 3, 4], [4, 8, 9, 4]]).rref() == (Matrix([[1, 2, 0, -8], [0, 0, 1, 4]]), (0, 2))
Matrix([[1, 4, 0, 7], [2, 7, 0, 11]]).rref() == (Matrix([[1, 0, 0, -5], [0, 1, 0, 3]]), (0, 1))
Matrix([[0, 1, -6, 5], [1, -2, 7, -4]]).rref()[0] == Matrix([[1, 0, -5, 6], [0, 1, -6, 5]])
simplify(Matrix([[0, 1, -6], [1, -2, 7]]) * Matrix([6 + 5*t, 5 + 6*t, t]) - Matrix([5, -4])) == zeros(2, 1)
# Exercises 16–18:一般解整個代回,自由變數留著
simplify(Matrix([[1, -2, -1], [3, -6, -2]]) * Matrix([-4 + 2*s, s, -7]) - Matrix([3, 2])) == zeros(2, 1)
simplify(Matrix([[3, -4, 2], [-9, 12, -6], [-6, 8, -4]]) * Matrix([Rational(4, 3)*s - Rational(2, 3)*t, s, t])) == zeros(3, 1)
simplify(Matrix([[1, -7, 0, 6], [0, 0, 1, -2], [-1, 7, -4, 2]]) * Matrix([5 + 7*s - 6*t, s, -3 + 2*t, t]) - Matrix([5, -3, 7])) == zeros(3, 1)
Matrix([[1, -2, -1, 3], [3, -6, -2, 2]]).rref() == (Matrix([[1, -2, 0, -4], [0, 0, 1, -7]]), (0, 2))
Matrix([[3, -4, 2, 0], [-9, 12, -6, 0], [-6, 8, -4, 0]]).rref()[0][0, :] == Matrix([[1, Rational(-4, 3), Rational(2, 3), 0]])
Matrix([[1, -7, 0, 6, 5], [0, 0, 1, -2, -3], [-1, 7, -4, 2, 7]]).rref() == (Matrix([[1, -7, 0, 6, 5], [0, 0, 1, -2, -3], [0, 0, 0, 0, 0]]), (0, 2))
Matrix([[1, -3, 0, -1, 0, -2], [0, 1, 0, 0, -4, 1], [0, 0, 0, 1, 9, -4], [0, 0, 0, 0, 0, 0]]).rref()[0][:3, :] == Matrix([[1, 0, 0, 0, -3, -3], [0, 1, 0, 0, -4, 1], [0, 0, 0, 1, 9, -4]])
Matrix([[1, 2, -5, -4, 0, -5], [0, 1, -6, -4, 0, 2], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0]]).rref()[0][0, :] == Matrix([[1, 0, 7, 4, 0, -9]])
Matrix([[1, -2, -1, 3, 0], [-2, 4, 5, -5, 3], [3, -6, -6, 8, 2]]).rref()[1][-1] == 4
Matrix([[2, 3, h], [4, 6, 7]]).echelon_form()[1, :] == Matrix([[0, 0, 14 - 4*h]])
Matrix([[1, -4, -3], [6, h, -9]]).echelon_form()[1, :] == Matrix([[0, h + 24, 9]])
Matrix([[1, h, 2], [4, 8, k]]).echelon_form()[1, :] == Matrix([[0, 8 - 4*h, k - 8]])
Matrix([[1, 4, 5], [2, h, k]]).echelon_form()[1, :] == Matrix([[0, h - 8, k - 10]])
Matrix([[1, 1, 1, 1], [1, 1, 1, 2]]).rref()[1][-1] == 3
Matrix([[1, 1, 2], [1, -1, 0], [3, 2, 5]]).rref()[0][:, 2] == Matrix([1, 1, 0])
[Rational(2, 3)*n**3 + Rational(1, 2)*n**2 - Rational(7, 6)*n for n in (30, 300)] == [18415, 18044650]
```
