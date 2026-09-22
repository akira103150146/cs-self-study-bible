---
title_en: Matrix Notation and Elementary Row Operations
title_zh: 矩陣表示與基本列運算
sub: Drop the variable names, keep the numbers, operate on rows
level: basic
source: Lay 1.1
lab_hook: "`B[2] = B[2] - 5 * B[0]`(對 NumPy 陣列做一次列運算,就是例 2 的第一步)"
---
## 觀念
The essential information of a linear system can be recorded compactly in a rectangular array called a **matrix**. For the system

$$\begin{aligned} x_1 - 2x_2 + x_3 &= 0 \\ 2x_2 - 8x_3 &= 8 \\ 5x_1 - 5x_3 &= 10 \end{aligned}$$

the **coefficient matrix** and the **augmented matrix** are

$$\begin{bmatrix} 1 & -2 & 1 \\ 0 & 2 & -8 \\ 5 & 0 & -5 \end{bmatrix} \qquad \text{and} \qquad \left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 2 & -8 & 8 \\ 5 & 0 & -5 & 10 \end{array}\right].$$

The **size** of a matrix tells how many rows and columns it has; an $m \times n$ matrix has $m$ rows and $n$ columns (rows always come first).

The basic strategy for solving a linear system is *to replace one system with an equivalent system that is easier to solve*. Three **elementary row operations** are used:

1. **(Replacement)** Replace one row by the sum of itself and a multiple of another row.
2. **(Interchange)** Interchange two rows.
3. **(Scaling)** Multiply all entries in a row by a nonzero constant.

Two matrices are **row equivalent** if there is a sequence of elementary row operations that transforms one matrix into the other. Row operations are **reversible**, and so: *if the augmented matrices of two linear systems are row equivalent, then the two systems have the same solution set.*

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| matrix | 矩陣 | 長方形排列的一張數字表 |
| row / column | 列 / 行 | **列是橫的、行是直的**(臺灣用法;中國大陸的「行、列」剛好相反) |
| coefficient matrix | 係數矩陣 | 只放未知數的係數 |
| augmented matrix | 增廣矩陣 | 係數矩陣右邊再加上一行常數 |
| size, $m \times n$ matrix | 大小,$m \times n$ 矩陣 | $m$ 列、$n$ 行,**列數寫在前面** |
| elementary row operations | 基本列運算 | replacement、interchange、scaling 三種 |
| replacement | 列取代 | 某一列加上另一列的倍數 |
| interchange | 列交換 | 兩列對調 |
| scaling | 列伸縮 | 某一列乘上一個**不為 0** 的數 |
| row equivalent | 列等價 | 可以用一連串列運算互相轉換 |
| reversible | 可逆的 | 做完之後可以再用列運算變回去 |

## 白話說
解方程組的時候,變數名稱 $x_1, x_2, x_3$ 其實只是在佔位子。把它們拿掉,只留係數和常數,排成一張數字表,就是**增廣矩陣**:一列是一條方程式,每一行固定對應一個未知數,最後一行是等號右邊的常數,中間畫一條直線隔開。缺少的未知數,係數就填 0。

原本對方程式做的消去動作,現在變成對「列」做三種操作:把某列的倍數加到另一列、兩列對調、某列乘上一個**不是 0** 的數。這三招都**可以復原**,所以做完之後解不會變——這正是本週證明時刻要證的事。

解題的策略只有一句話:**一直把方程組換成「解一樣、但更好解」的方程組**,直到答案一眼就看得出來。

## 幾何意義
列運算會改變方程式,也就是改變圖上的線,但**不會移動交點**。以觀念 1 的例 3(a) 為例,做一次 $R_2 \leftarrow R_2 + R_1$,第二條方程式從 $-x_1 + 3x_2 = 3$ 變成 $x_2 = 2$:

![做完 replacement 之後,第二條線換成了水平線 x2 = 2,但兩條線仍然交在 (3, 2)。](row-op-geometry.svg)

橘色的線被換掉了,新的線更簡單(水平線),但它仍然通過 $(3, 2)$。消去法的每一步都在做同一件事:**把線換成更簡單的線,交點保持不動**,直到交點的座標可以直接讀出來。

## 在資工哪裡用
在程式裡,矩陣就是一個二維陣列(NumPy 的 `np.array`)。列運算就是對陣列的某一列做運算,例如 `B[2] = B[2] - 5 * B[0]` 就是 $R_3 \leftarrow R_3 - 5R_1$(Python 從 0 開始數)。實作課第一步就做這件事,而且你會看到它和手算的每一步一模一樣。

矩陣大小「$m \times n$、列數在前」也和 NumPy 的 `A.shape` 回傳 `(列數, 行數)` 完全一致。

## 數值筆記
實務上,方程組都是交給電腦解。電腦幾乎都用這一節和下一節的消去法,只是稍微修改以提高準確度。

大多數商業與工業上的線代問題,都是用**浮點數**運算:數字以 $\pm .d_1 \cdots d_p \times 10^r$ 的形式儲存,小數位數 $p$ 通常在 8 到 16 之間。所以運算結果通常不精確,要捨入到能儲存的位數;像 $1/3$ 這種數,一輸入電腦就已經有捨入誤差。幸好浮點數的誤差很少造成問題,本書的數值筆記會提醒你少數需要注意的情況。(改寫自 Lay 1.1 Numerical Note)

## 合理性檢查
求出解之後,**一定要代回原方程式檢查**。例如解方程組

$$x_1 - 2x_2 + x_3 = 2, \qquad x_1 - 2x_3 = -2, \qquad x_2 + x_3 = 3$$

若你算出 $(2, 1, -1)$,代回去:$2 - 2(1) + (-1) = -1 \neq 2$、$2 - 2(-1) = 4 \neq -2$、$1 + (-1) = 0 \neq 3$——一定有地方算錯了。重新檢查後若得到 $(2, 1, 2)$:$2 - 2 + 2 = 2$ ✓、$2 - 4 = -2$ ✓、$1 + 2 = 3$ ✓,現在你可以確定答案是對的。(改寫自 Lay 1.1 Reasonable Answers)

## 原理
三種列運算分別對應到解方程組時本來就在做的三件事:

- **Replacement**:「第 3 式加上第 1 式的 $-5$ 倍」——加減消去法。
- **Interchange**:把方程式換個順序寫——不影響任何一條方程式本身。
- **Scaling**:整條方程式兩邊同乘一個數——例如把 $2x_2 - 8x_3 = 8$ 乘以 $\tfrac12$。

**為什麼 scaling 要求不為 0?** 乘 0 會把方程式變成 $0 = 0$,原本的限制條件就消失了,解集可能變大,而且沒辦法復原(除以 0 沒有意義)。另外兩種運算天生就能復原:replacement 加了 $c$ 倍就再加 $-c$ 倍,interchange 再換一次就回來(課本 p. 31)。

**記號**:$R_3 \leftarrow R_3 + (-5)R_1$ 讀作「把第 3 列換成『第 3 列加上 $-5$ 倍的第 1 列』」。只有箭頭左邊那一列會被改寫,第 1 列保持不動。

**列運算可以用在任何矩陣上**,不一定要是某個方程組的增廣矩陣(課本 p. 31)。「列等價」是矩陣之間的關係。

## 老師講解
### 例 1 · Lay 1.1(p. 28,矩陣表示)
Write the coefficient matrix and the augmented matrix of the system $x_1 - 2x_2 + x_3 = 0,\;\; 2x_2 - 8x_3 = 8,\;\; 5x_1 - 5x_3 = 10$, and give the size of the augmented matrix.

1. **先對齊未知數**:把每條方程式的 $x_1$、$x_2$、$x_3$ 上下對齊,缺的補 0。第二條其實是 $0 \cdot x_1 + 2x_2 - 8x_3 = 8$,第三條是 $5x_1 + 0 \cdot x_2 - 5x_3 = 10$。
2. **係數矩陣**:一條方程式一列,依序放 $x_1, x_2, x_3$ 的係數:
   $$\begin{bmatrix} 1 & -2 & 1 \\ 0 & 2 & -8 \\ 5 & 0 & -5 \end{bmatrix}$$
3. **增廣矩陣**:係數矩陣右邊再加一行常數(等號右邊),中間畫直線提醒自己「這一行是常數,不是未知數」:
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 2 & -8 & 8 \\ 5 & 0 & -5 & 10 \end{array}\right]$$
4. **大小**:增廣矩陣有 3 列、4 行,是 $3 \times 4$ 矩陣(讀作「3 by 4」)。**列數永遠寫在前面**。

### 例 2 · Lay 1.1 Example 1
Solve the system $x_1 - 2x_2 + x_3 = 0,\;\; 2x_2 - 8x_3 = 8,\;\; 5x_1 - 5x_3 = 10$.

1. **策略**:保留第 1 式的 $x_1$,把其他方程式的 $x_1$ 消掉;再用第 2 式的 $x_2$ 消掉下面的 $x_2$。目標是讓矩陣左下角全變成 0(三角形)。
2. **消掉第 3 式的 $x_1$**:第 3 式的 $x_1$ 係數是 5,第 1 式是 1,所以把第 1 式乘 $-5$ 加到第 3 式:$R_3 \leftarrow R_3 + (-5)R_1$。用方程式看:$-5x_1 + 10x_2 - 5x_3 = 0$ 加上 $5x_1 - 5x_3 = 10$,得到新的第 3 式 $10x_2 - 10x_3 = 10$。
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 2 & -8 & 8 \\ 0 & 10 & -10 & 10 \end{array}\right]$$
3. **讓第 2 式的 $x_2$ 係數變成 1**:$R_2 \leftarrow \tfrac12 R_2$,第 2 式變成 $x_2 - 4x_3 = 4$。這一步不是必要的,但會讓下一步的算術比較簡單。
4. **消掉第 3 式的 $x_2$**:第 3 式的 $x_2$ 係數是 10,所以 $R_3 \leftarrow R_3 + (-10)R_2$:$-10x_2 + 40x_3 = -40$ 加上 $10x_2 - 10x_3 = 10$,得 $30x_3 = -30$。
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 1 & -4 & 4 \\ 0 & 0 & 30 & -30 \end{array}\right]$$
5. **讓 $x_3$ 的係數變成 1**:$R_3 \leftarrow \tfrac{1}{30} R_3$,得 $x_3 = -1$。現在是三角形:
   $$\left[\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\ 0 & 1 & -4 & 4 \\ 0 & 0 & 1 & -1 \end{array}\right]$$
6. **往上消**:課本不急著代回,而是先用第 3 式的 $x_3$ 把上面兩式的 $x_3$ 消掉,這樣比較有效率。$R_2 \leftarrow R_2 + 4R_3$(得 $x_2 = 0$)、$R_1 \leftarrow R_1 + (-1)R_3$(得 $x_1 - 2x_2 = 1$):
   $$\left[\begin{array}{rrr|r} 1 & -2 & 0 & 1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -1 \end{array}\right]$$
7. **再往上一層**:用第 2 式的 $x_2$ 消掉第 1 式的 $-2x_2$:$R_1 \leftarrow R_1 + 2R_2$。因為上一步已經把 $x_3$ 清乾淨,這一步不會再動到 $x_3$:
   $$\left[\begin{array}{rrr|r} 1 & 0 & 0 & 1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -1 \end{array}\right]$$
8. **讀出答案**:矩陣說的就是 $x_1 = 1$、$x_2 = 0$、$x_3 = -1$。
9. **代回原方程組檢查**(計算這麼多步,一定要驗算):$1(1) - 2(0) + 1(-1) = 0$ ✓;$2(0) - 8(-1) = 8$ ✓;$5(1) - 5(-1) = 10$ ✓。唯一解是 $(1, 0, -1)$。
10. **幾何上**:三條方程式各是空間中的一個平面,$(1, 0, -1)$ 是三個平面唯一的共同點(課本 p. 30 的立體圖)。

#### 備註
這是全書第一個完整的消去,建議在黑板左右兩欄同時寫「方程式」與「矩陣」,讓學生看到兩者一一對應(課本 p. 29–30 就是這樣排)。第 6、7 步「先往上消、最後才讀答案」正是觀念 4 往回階段的雛形。

## 易錯點
- 做 replacement 時改錯列:$R_3 \leftarrow R_3 + (-5)R_1$ 是改寫**第 3 列**,第 1 列保持不動。學生常把兩列都改掉,或把結果寫到第 1 列去。
- 缺少的未知數沒有補 0,導致係數跑到錯的行。
- 把矩陣大小寫反(寫成「行 × 列」)。
- 「列」和「行」搞混。臺灣教科書:列是橫的(row)、行是直的(column)。

## 教學提示
每一步都在右邊寫出操作記號($R_3 \leftarrow R_3 + (-5)R_1$),並要求學生照做。記號寫出來,錯了才找得到是哪一步;這也正是實作課程式碼的寫法,先在紙上養成習慣,實作課就很順。

例 2 做完一定要驗算,並把「合理性檢查」那個例子帶一遍:讓學生看到代回原題是確認答案的唯一方法。

課堂建議做:照做 1、2、3;是非全部(每題 30 秒);變化題挑一題 3×3 的完整消去。

## 練習
### 照做 · Lay 1.1 Exercise 1
Solve the system by using elementary row operations on the equations or on the augmented matrix. Follow the systematic elimination procedure described in this section.

$$x_1 + 5x_2 = 7, \qquad -2x_1 - 7x_2 = -5$$

#### 解答
$$\left[\begin{array}{rr|r} 1 & 5 & 7 \\ -2 & -7 & -5 \end{array}\right] \xrightarrow{R_2 + 2R_1} \left[\begin{array}{rr|r} 1 & 5 & 7 \\ 0 & 3 & 9 \end{array}\right] \xrightarrow{\frac13 R_2} \left[\begin{array}{rr|r} 1 & 5 & 7 \\ 0 & 1 & 3 \end{array}\right] \xrightarrow{R_1 - 5R_2} \left[\begin{array}{rr|r} 1 & 0 & -8 \\ 0 & 1 & 3 \end{array}\right]$$

解是 $(x_1, x_2) = (-8, 3)$(書後解答相同)。驗算:$-2(-8) - 7(3) = 16 - 21 = -5$ ✓。

#### 備註
建議課堂做,全班寫完再往下。

### 照做 · Lay 1.1 Exercise 2
Solve the system by using elementary row operations: $2x_1 + 4x_2 = -4,\;\; 5x_1 + 7x_2 = 11$.

#### 解答
$R_1 \leftarrow \tfrac12 R_1$:$[\,1 \;\; 2 \mid {-2}\,]$;$R_2 \leftarrow R_2 - 5R_1$:$[\,0 \;\; {-3} \mid 21\,]$;$R_2 \leftarrow -\tfrac13 R_2$:$x_2 = -7$;$R_1 \leftarrow R_1 - 2R_2$:$x_1 = 12$。

解是 $(12, -7)$。驗算:$2(12) + 4(-7) = -4$ ✓,$5(12) + 7(-7) = 11$ ✓。

### 照做 · Lay 1.1 Practice Problem 1
State in words the next elementary row operation that should be performed on the system in order to solve it. [More than one answer is possible in (a).]

(a) $x_1 + 4x_2 - 2x_3 + 8x_4 = 12,\;\; x_2 - 7x_3 + 2x_4 = -4,\;\; 5x_3 - x_4 = 7,\;\; x_3 + 3x_4 = -5$

(b) $x_1 - 3x_2 + 5x_3 - 2x_4 = 0,\;\; x_2 + 8x_3 = -4,\;\; 2x_3 = 3,\;\; x_4 = 1$

#### 解答
(a) 手算最好的選擇是**交換第 3、4 式**(讓 $x_3$ 係數為 1 的式子到上面)。也可以把第 3 式乘 $\tfrac15$,或把第 4 式加上第 3 式的 $-\tfrac15$ 倍。**不要**現在就用第 2 式的 $x_2$ 去消第 1 式的 $4x_2$——等到三角形完成、下面的 $x_3$、$x_4$ 都處理完再回頭。

(b) 已經是三角形。從最下面的 $x_4$ 開始往上消:下一步是**把第 1 式加上第 4 式的 2 倍**(消掉 $-2x_4$)。之後再把第 3 式乘 $\tfrac12$,用它消掉上面的 $x_3$。(課本 p. 36)

### 照做 · Lay 1.1 Exercise 5
Consider the matrix as the augmented matrix of a linear system. State in words the next two elementary row operations that should be performed in the process of solving the system.

$$\left[\begin{array}{rrrr|r} 1 & 3 & -4 & 0 & 9 \\ 0 & 1 & 5 & 0 & -8 \\ 0 & 0 & 1 & 0 & 7 \\ 0 & 0 & 0 & 1 & -6 \end{array}\right]$$

#### 解答
已經是三角形,接下來往上消 $x_3$:**把第 2 列加上第 3 列的 $-5$ 倍**,然後**把第 1 列加上第 3 列的 4 倍**(書後解答相同)。

#### 備註
原書(Global Edition)此題第 2 列印成 $[\,1 \;\; 1 \;\; 5 \;\; 0 \mid {-8}\,]$,與書後解答不合,疑為印刷錯誤;講義依書後解答改為 $[\,0 \;\; 1 \;\; 5 \;\; 0 \mid {-8}\,]$。學生若拿課本對照,請先說明。

### 照做 · Lay 1.1 Exercise 6
Consider the matrix as the augmented matrix of a linear system. State in words the next two elementary row operations that should be performed in the process of solving the system.

$$\left[\begin{array}{rrrr|r} 1 & -6 & 4 & 0 & -1 \\ 0 & 2 & -7 & 0 & 4 \\ 0 & 0 & 1 & 2 & -3 \\ 0 & 0 & 3 & 1 & 6 \end{array}\right]$$

#### 解答
第 4 列還有 $x_3$ 沒消掉,所以先**把第 4 列加上第 3 列的 $-3$ 倍**,得 $[\,0 \;\; 0 \;\; 0 \;\; {-5} \mid 15\,]$;再**把第 4 列乘 $-\tfrac15$**,得 $x_4 = -3$。

### 是非 · Lay 1.1 Exercise 27
**(T/F)** Every elementary row operation is reversible.

#### 解答
**True.** 交換可以再換回來、伸縮 $c$ 倍可以再乘 $1/c$、取代加了 $c$ 倍可以再加 $-c$ 倍(課本 p. 31)。

### 是非 · Lay 1.1 Exercise 28
**(T/F)** Elementary row operations on an augmented matrix never change the solution set of the associated linear system.

#### 解答
**True.** 這正是課本 p. 31 方框裡的敘述,也是本週的證明時刻。

### 是非 · Lay 1.1 Exercise 29
**(T/F)** A $5 \times 6$ matrix has six rows.

#### 解答
**False.** $m \times n$ 矩陣有 $m$ 列、$n$ 行,所以 $5 \times 6$ 矩陣有 **5 列**、6 行(課本 p. 28)。

### 是非 · Lay 1.1 Exercise 30
**(T/F)** Two matrices are row equivalent if they have the same number of rows.

#### 解答
**False.** 列等價的定義是「可以用一連串列運算互相轉換」(課本 p. 31),和列數相同無關。

### 變化 · Lay 1.1 Exercise 11
Solve the system: $x_2 + 4x_3 = -4,\;\; x_1 + 3x_2 + 3x_3 = -2,\;\; 3x_1 + 7x_2 + 5x_3 = 6$.

#### 解答
第 1 式沒有 $x_1$,先交換第 1、2 式。接著 $R_3 \leftarrow R_3 - 3R_1$ 得 $[\,0 \;\; {-2} \;\; {-4} \mid 12\,]$;$R_3 \leftarrow R_3 + 2R_2$ 得 $[\,0 \;\; 0 \;\; 4 \mid 4\,]$,$x_3 = 1$。往上:$x_2 = -4 - 4(1) = -8$;$x_1 = -2 - 3(-8) - 3(1) = 19$。

解是 $(19, -8, 1)$(書後解答相同)。代回驗算見 Exercise 15。

### 變化 · Lay 1.1 Exercise 12
Solve the system: $x_1 - 3x_2 + 4x_3 = -4,\;\; 3x_1 - 7x_2 + 7x_3 = -8,\;\; -4x_1 + 6x_2 + 2x_3 = 4$.

#### 解答
$R_2 \leftarrow R_2 - 3R_1$:$[\,0 \;\; 2 \;\; {-5} \mid 4\,]$;$R_3 \leftarrow R_3 + 4R_1$:$[\,0 \;\; {-6} \;\; 18 \mid {-12}\,]$;$R_3 \leftarrow R_3 + 3R_2$:$[\,0 \;\; 0 \;\; 3 \mid 0\,]$,$x_3 = 0$。往上:$2x_2 = 4$,$x_2 = 2$;$x_1 = -4 + 3(2) - 0 = 2$。

解是 $(2, 2, 0)$。代回驗算見 Exercise 16。

### 變化 · Lay 1.1 Exercise 13
Solve the system: $x_1 - 3x_3 = 8,\;\; 2x_1 + 2x_2 + 9x_3 = 7,\;\; x_2 + 5x_3 = -2$.

#### 解答
$R_2 \leftarrow R_2 - 2R_1$:$[\,0 \;\; 2 \;\; 15 \mid {-9}\,]$;交換第 2、3 列讓 $x_2$ 係數為 1:$[\,0 \;\; 1 \;\; 5 \mid {-2}\,]$、$[\,0 \;\; 2 \;\; 15 \mid {-9}\,]$;$R_3 \leftarrow R_3 - 2R_2$:$[\,0 \;\; 0 \;\; 5 \mid {-5}\,]$,$x_3 = -1$。往上:$x_2 = -2 - 5(-1) = 3$;$x_1 = 8 + 3(-1) = 5$。

解是 $(5, 3, -1)$(書後解答相同)。代回驗算見 Exercise 17。

### 變化 · Lay 1.1 Exercise 14
Solve the system: $x_1 - 3x_2 = 5,\;\; -x_1 + x_2 + 5x_3 = 2,\;\; x_2 + x_3 = 0$.

#### 解答
$R_2 \leftarrow R_2 + R_1$:$[\,0 \;\; {-2} \;\; 5 \mid 7\,]$;交換第 2、3 列:$[\,0 \;\; 1 \;\; 1 \mid 0\,]$、$[\,0 \;\; {-2} \;\; 5 \mid 7\,]$;$R_3 \leftarrow R_3 + 2R_2$:$[\,0 \;\; 0 \;\; 7 \mid 7\,]$,$x_3 = 1$。往上:$x_2 = -1$;$x_1 = 5 + 3(-1) = 2$。

解是 $(2, -1, 1)$。代回驗算見 Exercise 18。

#### 備註
Exercises 11–14 份量相同,課堂挑一題,其餘作業。

### 變化 · Lay 1.1 Exercises 15–18
(15) Verify that the solution you found to Exercise 11 is correct by substituting the values you obtained back into the original equations.

(16) Verify that the solution you found to Exercise 12 is correct by substituting the values you obtained back into the original equations.

(17) Verify that the solution you found to Exercise 13 is correct by substituting the values you obtained back into the original equations.

(18) Verify that the solution you found to Exercise 14 is correct by substituting the values you obtained back into the original equations.

#### 解答
每一條方程式都要代,負數記得加括號(這就是觀念 2 的「合理性檢查」)。

(15) $(x_1, x_2, x_3) = (19, -8, 1)$ 代入 Exercise 11:
$$\begin{aligned} (-8) + 4(1) &= -4 \;\checkmark \\ 19 + 3(-8) + 3(1) &= -2 \;\checkmark \\ 3(19) + 7(-8) + 5(1) &= 57 - 56 + 5 = 6 \;\checkmark \end{aligned}$$

(16) $(2, 2, 0)$ 代入 Exercise 12:$2 - 3(2) + 4(0) = -4$ ✓;$3(2) - 7(2) + 7(0) = -8$ ✓;$-4(2) + 6(2) + 2(0) = 4$ ✓。

(17) $(5, 3, -1)$ 代入 Exercise 13:$5 - 3(-1) = 8$ ✓;$2(5) + 2(3) + 9(-1) = 7$ ✓;$3 + 5(-1) = -2$ ✓(書後解答相同)。

(18) $(2, -1, 1)$ 代入 Exercise 14:$2 - 3(-1) = 5$ ✓;$-2 + (-1) + 5(1) = 2$ ✓;$(-1) + 1 = 0$ ✓。

#### 備註
建議和 Exercises 11–14 綁在一起出:算完一題就代回一題,讓「驗算」變成解題的最後一步,而不是額外的作業。

### 變化 · Lay 1.1 Exercises 39–40
Find the elementary row operation that transforms the first matrix into the second, and then find the reverse row operation that transforms the second matrix into the first.

(39) $\begin{bmatrix} 0 & -2 & 5 \\ 1 & 4 & -7 \\ 3 & -1 & 6 \end{bmatrix},\; \begin{bmatrix} 1 & 4 & -7 \\ 0 & -2 & 5 \\ 3 & -1 & 6 \end{bmatrix}$  (40) $\begin{bmatrix} 1 & 3 & -4 \\ 0 & -2 & 6 \\ 0 & -5 & 9 \end{bmatrix},\; \begin{bmatrix} 1 & 3 & -4 \\ 0 & 1 & -3 \\ 0 & -5 & 9 \end{bmatrix}$

#### 解答
(39) 交換第 1、2 列;反向運算:再交換一次第 1、2 列(書後解答相同)。

(40) 第 2 列乘 $-\tfrac12$;反向運算:第 2 列乘 $-2$。

### 變化 · Lay 1.1 Exercises 41–42
Find the elementary row operation that transforms the first matrix into the second, and then find the reverse row operation.

(41) $\begin{bmatrix} 1 & -3 & 2 & 0 \\ 0 & 4 & -5 & 6 \\ 5 & -7 & 8 & -9 \end{bmatrix},\; \begin{bmatrix} 1 & -3 & 2 & 0 \\ 0 & 4 & -5 & 6 \\ 0 & 8 & -2 & -9 \end{bmatrix}$  (42) $\begin{bmatrix} 1 & 2 & -5 & 0 \\ 0 & 1 & -3 & -2 \\ 0 & -3 & 9 & 5 \end{bmatrix},\; \begin{bmatrix} 1 & 2 & -5 & 0 \\ 0 & 1 & -3 & -2 \\ 0 & 0 & 0 & -1 \end{bmatrix}$

#### 解答
(41) 把第 3 列加上第 1 列的 $-5$ 倍;反向:把第 3 列加上第 1 列的 5 倍(書後解答相同)。

(42) 把第 3 列加上第 2 列的 3 倍;反向:把第 3 列加上第 2 列的 $-3$ 倍。

### 挑戰 · Lay 1.1 Exercise 36
Construct three different augmented matrices for linear systems whose solution set is $x_1 = -2$, $x_2 = 1$, $x_3 = 0$.

#### 解答
最直接的一個:$\left[\begin{array}{rrr|r} 1 & 0 & 0 & -2 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{array}\right]$。

對它做任何列運算,得到的矩陣都列等價,解集不變。例如把第 1 列加上第 2 列:$\left[\begin{array}{rrr|r} 1 & 1 & 0 & -1 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{array}\right]$;再把第 3 列加上第 1 列的 2 倍:$\left[\begin{array}{rrr|r} 1 & 1 & 0 & -1 \\ 0 & 1 & 0 & 1 \\ 2 & 2 & 1 & -2 \end{array}\right]$。

#### 備註
答案不唯一。這題正好反過來用「列運算不改變解集」:從答案出發,往回做列運算就能造題。

## 驗算
```check
Matrix([[1, -2, 1, 0], [0, 2, -8, 8], [5, 0, -5, 10]]).rref()[0] == Matrix([[1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, -1]])
Matrix([[5, 0, -5, 10]]) - 5*Matrix([[1, -2, 1, 0]]) == Matrix([[0, 10, -10, 10]])
Matrix([[0, 10, -10, 10]]) - 10*Matrix([[0, 1, -4, 4]]) == Matrix([[0, 0, 30, -30]])
Matrix([[0, 1, -4, 4]]) + 4*Matrix([[0, 0, 1, -1]]) == Matrix([[0, 1, 0, 0]])
[2 - 2*1 + (-1), 2 - 2*(-1), 1 + (-1)] == [-1, 4, 0]
[2 - 2*1 + 2, 2 - 2*2, 1 + 2] == [2, -2, 3]
Matrix([[1, 5, 7], [-2, -7, -5]]).rref()[0] == Matrix([[1, 0, -8], [0, 1, 3]])
Matrix([[2, 4, -4], [5, 7, 11]]).rref()[0] == Matrix([[1, 0, 12], [0, 1, -7]])
Matrix([[0, 0, 3, 1, 6]]) - 3*Matrix([[0, 0, 1, 2, -3]]) == Matrix([[0, 0, 0, -5, 15]])
Matrix([[0, 1, 4, -4], [1, 3, 3, -2], [3, 7, 5, 6]]).rref()[0][:, 3] == Matrix([19, -8, 1])
Matrix([[1, -3, 4, -4], [3, -7, 7, -8], [-4, 6, 2, 4]]).rref()[0][:, 3] == Matrix([2, 2, 0])
Matrix([[1, 0, -3, 8], [2, 2, 9, 7], [0, 1, 5, -2]]).rref()[0][:, 3] == Matrix([5, 3, -1])
Matrix([[1, -3, 0, 5], [-1, 1, 5, 2], [0, 1, 1, 0]]).rref()[0][:, 3] == Matrix([2, -1, 1])
# Exercises 15–18:代回驗算
[(-8) + 4*1, 19 + 3*(-8) + 3*1, 3*19 + 7*(-8) + 5*1] == [-4, -2, 6]
[2 - 3*2 + 4*0, 3*2 - 7*2 + 7*0, -4*2 + 6*2 + 2*0] == [-4, -8, 4]
[5 - 3*(-1), 2*5 + 2*3 + 9*(-1), 3 + 5*(-1)] == [8, 7, -2]
[2 - 3*(-1), -2 + (-1) + 5*1, (-1) + 1] == [5, 2, 0]
Matrix([[5, -7, 8, -9]]) - 5*Matrix([[1, -3, 2, 0]]) == Matrix([[0, 8, -2, -9]])
Matrix([[0, -3, 9, 5]]) + 3*Matrix([[0, 1, -3, -2]]) == Matrix([[0, 0, 0, -1]])
Matrix([[1, 1, 0, -1], [0, 1, 0, 1], [2, 2, 1, -2]]).rref()[0] == Matrix([[1, 0, 0, -2], [0, 1, 0, 1], [0, 0, 1, 0]])
```
