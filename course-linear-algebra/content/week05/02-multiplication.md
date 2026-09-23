---
title_en: Matrix Multiplication
title_zh: 矩陣乘法:兩台機器接起來
sub: A(Bx) = (AB)x
level: mid
source: Lay 2.1
lab_hook: '`A @ B` 是矩陣乘法、`A * B` 是逐格相乘——搞混是 NumPy 最常見的錯'
---
## 觀念
When a matrix $B$ multiplies a vector $\mathbf{x}$, it transforms $\mathbf{x}$ into the vector $B\mathbf{x}$. If this vector is then multiplied in turn by a matrix $A$, the resulting vector is $A(B\mathbf{x})$.

![課本 2.1 Figure 2–3:先乘 B 再乘 A,和一次乘 AB 的效果相同。](compose.svg)

Thus $A(B\mathbf{x})$ is produced from $\mathbf{x}$ by a *composition* of mappings—the linear transformations studied in Section 1.8. Our goal is to represent this composite mapping as multiplication by a single matrix, denoted by $AB$, so that

$$A(B\mathbf{x}) = (AB)\mathbf{x} \tag{1}$$

**Definition.** If $A$ is an $m \times n$ matrix, and if $B$ is an $n \times p$ matrix with columns $\mathbf{b}_1, \dots, \mathbf{b}_p$, then the product $AB$ is the $m \times p$ matrix whose columns are $A\mathbf{b}_1, \dots, A\mathbf{b}_p$. That is,

$$AB = A[\,\mathbf{b}_1 \;\; \mathbf{b}_2 \;\; \cdots \;\; \mathbf{b}_p\,] = [\,A\mathbf{b}_1 \;\; A\mathbf{b}_2 \;\; \cdots \;\; A\mathbf{b}_p\,]$$

*Multiplication of matrices corresponds to composition of linear transformations.*

Each column of $AB$ is a linear combination of the columns of $A$ using weights from the corresponding column of $B$.

**Row–column rule for computing $AB$.** If the product $AB$ is defined, then the entry in row $i$ and column $j$ of $AB$ is the sum of the products of corresponding entries from row $i$ of $A$ and column $j$ of $B$. If $(AB)_{ij}$ denotes the $(i, j)$-entry in $AB$, and if $A$ is an $m \times n$ matrix, then

$$(AB)_{ij} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{in}b_{nj}$$

Also, $\operatorname{row}_i(AB) = \operatorname{row}_i(A) \cdot B$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| composition of mappings | 映射的合成 | 先做一個變換,再做另一個;乘法的真正來源 |
| product $AB$ | 乘積 $AB$ | $A$ 乘 $B$;第 $j$ 行是 $A\mathbf{b}_j$ |
| row–column rule | 列乘行規則 | 手算單一格的方法:第 $i$ 列 · 第 $j$ 行 |
| $\operatorname{row}_i(A)$ | $A$ 的第 $i$ 列 | 課本用來寫 $\operatorname{row}_i(AB) = \operatorname{row}_i(A) \cdot B$ |
| defined / undefined | 有定義 / 沒有定義 | 行數列數對不上時,這個乘積根本不存在 |
| right-multiplied by $B$ | 被 $B$ 右乘 | $AB$ 裡,$A$ 被 $B$ 右乘;$B$ 被 $A$ 左乘 |

## 白話說
**一句話:$AB$ 就是「先做 $B$ 這台機器,再做 $A$ 這台機器」所合成的那一台機器。**

上一週學過:每個線性變換都是「乘一個矩陣」。那麼「先旋轉再放大」這兩步,應該也是某個矩陣——就是 $AB$。課本的定義正是為了讓 $(1)$ 式 $A(B\mathbf{x}) = (AB)\mathbf{x}$ 成立而設計的,不是憑空規定。

**兩種算法,同一個答案:**

| 算法 | 怎麼做 | 什麼時候用 |
|---|---|---|
| 行的算法(定義) | $AB$ 的第 $j$ 行 = $A\mathbf{b}_j$ | 理解為什麼、寫程式、做證明 |
| 列乘行規則 | 第 $(i, j)$ 格 = 第 $i$ 列 · 第 $j$ 行 | 手算、只要算某一格時 |

**尺寸規則**:$A$ 是 $m \times n$、$B$ 是 $n \times p$,**中間的 $n$ 必須相同**,答案是 $m \times p$。

![課本 2.1 Example 4:內側兩個數要相同,外側兩個數就是答案的大小。](size-match.svg)

**順序不能換**:$AB$ 和 $BA$ 通常不一樣,甚至常常一個有定義、另一個沒有。這是矩陣代數和數字代數最大的差別,下一個觀念會專門講。

## 幾何意義
把 $A$、$B$ 想成兩個動作。「先轉 90°,再往 x 方向壓扁」和「先壓扁,再轉 90°」得到的圖形不一樣——所以 $AB \ne BA$。乘法的順序就是動作的順序,而且**寫在右邊的先做**($AB\mathbf{x}$ 裡,$\mathbf{x}$ 先碰到 $B$)。

這個「右邊先做」的順序在觀念 6(圖學管線)會再出現一次,也是實作課最容易搞錯的地方。

## 在資工哪裡用
- **圖學管線**:模型 → 世界 → 相機 → 投影,每一步是一個矩陣,整條管線就是它們的乘積。GPU 把整串乘成一個矩陣後,幾百萬個頂點各乘一次就好。
- **神經網路**:每一層是 $\mathbf{x} \mapsto W\mathbf{x} + \mathbf{b}$。若沒有中間的非線性函數,連續兩層就會塌成一層 $W_2W_1\mathbf{x}$——**這正是「必須加激活函數」的數學理由**。
- **矩陣乘法的成本**:$m \times n$ 乘 $n \times p$ 要做 $mnp$ 次乘法。這是深度學習算力需求的來源,也是為什麼課本腳註提醒「$A(BC)$ 和 $(AB)C$ 答案一樣,但計算量可能差很多」。
- **資料庫與圖論**:關聯矩陣相乘可以算「兩步能到的路徑數」(見補充觀念)。

## 數值筆記
課本在 2.1 的腳註提醒:當 $B$ 是方陣、而 $C$ 的行數比 $A$ 的列數少時,先算 $A(BC)$ 比先算 $(AB)C$ 有效率。答案一樣(結合律),但乘法次數可能差好幾倍。實作課會實際計時。

另外,NumPy 裡 `A @ B` 是矩陣乘法,`A * B` 是**逐格相乘**(Hadamard 乘積),兩者都不會報錯,但意義完全不同——這是本週實作課的第一個陷阱。

## 合理性檢查
算完 $AB$ 先檢查三件事:

1. **大小對不對**?應該是(A 的列數)× (B 的行數)。
2. **抽一格用列乘行重算一次**。例如檢查右下角那一格。
3. **有 0 行或 0 列嗎**?若 $B$ 的某一行全是 0,則 $AB$ 的那一行也必須全是 0。

## 原理
**乘法為什麼這樣定義?**(本週的證明時刻,課本 pp. 124–125)

設 $B$ 的行是 $\mathbf{b}_1, \dots, \mathbf{b}_p$,$\mathbf{x}$ 的分量是 $x_1, \dots, x_p$。第 2 週學過
$$B\mathbf{x} = x_1\mathbf{b}_1 + \cdots + x_p\mathbf{b}_p.$$
再用「乘以 $A$ 是線性的」(上週的性質):
$$A(B\mathbf{x}) = A(x_1\mathbf{b}_1) + \cdots + A(x_p\mathbf{b}_p) = x_1A\mathbf{b}_1 + \cdots + x_pA\mathbf{b}_p.$$
右邊是以 $A\mathbf{b}_1, \dots, A\mathbf{b}_p$ 為行、以 $x_j$ 為權重的線性組合,也就是
$$A(B\mathbf{x}) = [\,A\mathbf{b}_1 \;\; \cdots \;\; A\mathbf{b}_p\,]\mathbf{x}.$$
所以只要**定義** $AB = [\,A\mathbf{b}_1 \;\cdots\; A\mathbf{b}_p\,]$,$(1)$ 式就自動成立。定義不是規定,是推出來的。

**列乘行規則為什麼對?**(課本 p. 126)$AB$ 的第 $j$ 行是 $A\mathbf{b}_j$;第 2 週的列向量規則說,$A\mathbf{b}_j$ 的第 $i$ 個分量 = $A$ 的第 $i$ 列和 $\mathbf{b}_j$ 對應相乘再相加。這正是 $(AB)_{ij} = a_{i1}b_{1j} + \cdots + a_{in}b_{nj}$。

## 老師講解
### 例 1 · Lay 2.1 Example 3
Compute $AB$, where $A = \begin{bmatrix} 2 & 3 \\ 1 & -5 \end{bmatrix}$ and $B = \begin{bmatrix} 4 & 3 & 6 \\ 1 & -2 & 3 \end{bmatrix}$.

1. **先確認尺寸**:$A$ 是 $2 \times 2$、$B$ 是 $2 \times 3$。中間兩個數都是 2,合法;答案是 $2 \times 3$。
2. **把 $B$ 拆成三行**:$B = [\,\mathbf{b}_1 \;\; \mathbf{b}_2 \;\; \mathbf{b}_3\,]$,其中 $\mathbf{b}_1 = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$、$\mathbf{b}_2 = \begin{bmatrix} 3 \\ -2 \end{bmatrix}$、$\mathbf{b}_3 = \begin{bmatrix} 6 \\ 3 \end{bmatrix}$。
3. **一行一行算**(每個都是第 2 週的「矩陣乘向量」):
   $$A\mathbf{b}_1 = \begin{bmatrix} 2 & 3 \\ 1 & -5 \end{bmatrix}\begin{bmatrix} 4 \\ 1 \end{bmatrix} = 4\begin{bmatrix} 2 \\ 1 \end{bmatrix} + 1\begin{bmatrix} 3 \\ -5 \end{bmatrix} = \begin{bmatrix} 11 \\ -1 \end{bmatrix}$$
4. 同樣地
   $$A\mathbf{b}_2 = \begin{bmatrix} 0 \\ 13 \end{bmatrix}, \qquad A\mathbf{b}_3 = \begin{bmatrix} 21 \\ -9 \end{bmatrix}$$
5. **把三個答案並排**:
   $$AB = [\,A\mathbf{b}_1 \;\; A\mathbf{b}_2 \;\; A\mathbf{b}_3\,] = \begin{bmatrix} 11 & 0 & 21 \\ -1 & 13 & -9 \end{bmatrix}$$
6. **讀出意義**:$AB$ 的第一行 $\begin{bmatrix} 11 \\ -1 \end{bmatrix}$ 是「用 $\mathbf{b}_1$ 的分量 4、1 當權重,組合 $A$ 的兩行」。每一行都是這樣來的。

### 例 2 · Lay 2.1 Examples 5–6
Use the row–column rule to compute two of the entries in $AB$ for the matrices in Example 1. Then find the entries in the second row of $AB$, where

$$A = \begin{bmatrix} 2 & -5 & 0 \\ -1 & 3 & -4 \\ 6 & -8 & -7 \\ -3 & 0 & 9 \end{bmatrix}, \qquad B = \begin{bmatrix} 4 & -6 \\ 7 & 1 \\ 3 & 2 \end{bmatrix}$$

1. **只要一格時,不必整個算**。要第 1 列第 3 行:拿 $A$ 的第 1 列 $[\,2 \;\; 3\,]$ 和 $B$ 的第 3 行 $\begin{bmatrix} 6 \\ 3 \end{bmatrix}$,對應相乘再相加:$2(6) + 3(3) = 21$。和例 1 的答案一致。
2. 第 2 列第 2 行:$A$ 的第 2 列 $[\,1 \;\; {-5}\,]$、$B$ 的第 2 行 $\begin{bmatrix} 3 \\ -2 \end{bmatrix}$:$1(3) + (-5)(-2) = 13$。
3. **第二個矩陣先看尺寸**:$4 \times 3$ 乘 $3 \times 2$,中間都是 3,答案是 $4 \times 2$。
4. **題目只要第二列**,所以只拿 $A$ 的第 2 列 $[\,-1 \;\; 3 \;\; {-4}\,]$ 去乘 $B$ 的兩行:
   $$-1(4) + 3(7) + (-4)(3) = -4 + 21 - 12 = 5$$
   $$-1(-6) + 3(1) + (-4)(2) = 6 + 3 - 8 = 1$$
5. **答案**:$AB$ 的第二列是 $[\,5 \;\; 1\,]$。
6. **這說明一個通則**:$\operatorname{row}_i(AB) = \operatorname{row}_i(A) \cdot B$——要哪一列,就只拿那一列去乘 $B$。程式裡處理大矩陣、只要某幾列結果時,這招可以省下大量計算。

### 例 3 · Lay 2.1 Example 4
If $A$ is a $3 \times 5$ matrix and $B$ is a $5 \times 2$ matrix, what are the sizes of $AB$ and $BA$, if they are defined?

1. **$AB$**:$A$ 有 5 行、$B$ 有 5 列,中間相合。答案的大小 = 外側兩個數 = $3 \times 2$。
2. **$BA$**:$B$ 有 2 行、$A$ 有 3 列,$2 \ne 3$,**沒有定義**。
3. **結論**:$AB$ 有定義不代表 $BA$ 有定義。順序在矩陣代數裡是實質的,不是習慣問題。
4. **記法**:把兩個尺寸並排寫 $(3 \times 5)(5 \times 2)$,中間對上就消掉,剩下 $3 \times 2$。

#### 備註
例 3 這張尺寸圖值得在黑板上重畫一次,並當場問學生「$BA$ 呢?」——這是學生第一次真正感受到「乘法有方向」。

## 易錯點
- **用逐格相乘**($a_{ij}b_{ij}$)當成矩陣乘法。那是 NumPy 的 `A * B`,不是 `A @ B`。
- **尺寸不合硬乘**。先寫下 $(m \times n)(n \times p)$ 檢查,再動手。
- **算 $AB$ 卻拿 $B$ 的列去乘 $A$ 的行**(左右顛倒)。口訣:**左列乘右行**。
- **以為 $AB = BA$**。下一個觀念會用具體反例打破這個直覺。
- 只要某一格時整個矩陣都算出來,浪費時間(例 2 就是在練這件事)。

## 教學提示
這是本週最重要的 25 分鐘。建議這樣鋪:

1. 先用**上週的語言**開場:「先旋轉再放大,合起來是哪個矩陣?」把 $A(B\mathbf{x})$ 寫在黑板上。
2. 帶著推一次 $A(B\mathbf{x}) = [\,A\mathbf{b}_1 \cdots A\mathbf{b}_p\,]\mathbf{x}$(不必嚴謹,寫三行就好),再說「所以課本才這樣定義乘法」。這就是接下來證明時刻的主線。
3. 例 1 用**行的算法**做一次,例 2 再用**列乘行規則**算同一個矩陣的兩格,讓學生看到兩種算法答案相同。
4. 尺寸規則寫在黑板角落整堂課不要擦。

課堂建議做:Exercises 1–2(含「沒有定義」的判斷)、Exercise 5 的兩種算法;尺寸判斷的 Exercises 7–8;Exercise 9(什麼時候可交換)與 Exercise 10(消去律不成立)一定要做,它們是下一個觀念的伏筆。Exercises 26–28 適合口頭快問快答。

## 練習
### 照做 · Lay 2.1 Exercises 1–2
In Exercises 1 and 2, compute each matrix sum or product if it is defined. If an expression is undefined, explain why. Let

$$A = \begin{bmatrix} 2 & 0 & -1 \\ 4 & -3 & 2 \end{bmatrix}, \quad B = \begin{bmatrix} 7 & -5 & 1 \\ 1 & -4 & -3 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 2 \\ -2 & 1 \end{bmatrix}, \quad D = \begin{bmatrix} 3 & 5 \\ -1 & 4 \end{bmatrix}, \quad E = \begin{bmatrix} -5 \\ 3 \end{bmatrix}$$

(1) $-2A$, $B - 2A$, $AC$, $CD$

(2) $A + 2B$, $3C - E$, $CB$, $EB$

#### 解答
(1)
$$-2A = \begin{bmatrix} -4 & 0 & 2 \\ -8 & 6 & -4 \end{bmatrix}, \qquad B - 2A = \begin{bmatrix} 3 & -5 & 3 \\ -7 & 2 & -7 \end{bmatrix}$$
$AC$ **沒有定義**:$A$ 是 $2 \times 3$、$C$ 是 $2 \times 2$,$3 \ne 2$。
$$CD = \begin{bmatrix} 1 & 13 \\ -7 & -6 \end{bmatrix}$$

(2)
$$A + 2B = \begin{bmatrix} 16 & -10 & 1 \\ 6 & -11 & -4 \end{bmatrix}$$
$3C - E$ **沒有定義**:$3C$ 是 $2 \times 2$、$E$ 是 $2 \times 1$,大小不同不能相減。
$$CB = \begin{bmatrix} 9 & -13 & -5 \\ -13 & 6 & -5 \end{bmatrix}$$
$EB$ **沒有定義**:$E$ 是 $2 \times 1$、$B$ 有 2 列,$1 \ne 2$。

#### 備註
這兩題的價值在「沒有定義」那三個,不在算式本身。要求學生**寫出理由**(哪兩個數對不上),不能只寫「undefined」。

建議 (1) 課堂做、(2) 當作業。

### 照做 · Lay 2.1 Exercises 5–6
In Exercises 5 and 6, compute the product $AB$ in two ways: (a) by the definition, where $A\mathbf{b}_1$ and $A\mathbf{b}_2$ are computed separately, and (b) by the row–column rule for computing $AB$.

(5) $A = \begin{bmatrix} -1 & 2 \\ 5 & 4 \\ 2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 3 & -4 \\ -2 & 1 \end{bmatrix}$

(6) $A = \begin{bmatrix} 4 & -2 \\ -3 & 0 \\ 3 & 5 \end{bmatrix}$, $B = \begin{bmatrix} 1 & 3 \\ 4 & -1 \end{bmatrix}$

#### 解答
(5) **(a)** $A\mathbf{b}_1 = 3\begin{bmatrix} -1 \\ 5 \\ 2 \end{bmatrix} + (-2)\begin{bmatrix} 2 \\ 4 \\ -3 \end{bmatrix} = \begin{bmatrix} -7 \\ 7 \\ 12 \end{bmatrix}$,$A\mathbf{b}_2 = \begin{bmatrix} 6 \\ -16 \\ -11 \end{bmatrix}$。
**(b)** 逐格用列乘行:
$$AB = \begin{bmatrix} -1(3) + 2(-2) & -1(-4) + 2(1) \\ 5(3) + 4(-2) & 5(-4) + 4(1) \\ 2(3) - 3(-2) & 2(-4) - 3(1) \end{bmatrix} = \begin{bmatrix} -7 & 6 \\ 7 & -16 \\ 12 & -11 \end{bmatrix}$$

(6) **(a)** $A\mathbf{b}_1 = \begin{bmatrix} -4 \\ -3 \\ 23 \end{bmatrix}$,$A\mathbf{b}_2 = \begin{bmatrix} 14 \\ -9 \\ 4 \end{bmatrix}$。
**(b)**
$$AB = \begin{bmatrix} 4(1) - 2(4) & 4(3) - 2(-1) \\ -3(1) + 0(4) & -3(3) + 0(-1) \\ 3(1) + 5(4) & 3(3) + 5(-1) \end{bmatrix} = \begin{bmatrix} -4 & 14 \\ -3 & -9 \\ 23 & 4 \end{bmatrix}$$

#### 備註
重點是**兩種算法得到同一個矩陣**。要求兩種都寫、寫完自己比對;學生若只做 (b),等於沒學到乘法的定義。

課堂做 (5) 就好,(6) 留作業。

### 是非 · Lay 2.1 Exercises 15–18
Exercises 15–24 concern arbitrary matrices $A$, $B$, and $C$ for which the indicated sums and products are defined. Mark each statement True or False (T/F). Justify each answer.

(15) **(T/F)** If $A$ and $B$ are $2 \times 2$ with columns $\mathbf{a}_1, \mathbf{a}_2$, and $\mathbf{b}_1, \mathbf{b}_2$, respectively, then $AB = [\,\mathbf{a}_1\mathbf{b}_1 \;\; \mathbf{a}_2\mathbf{b}_2\,]$.

(16) **(T/F)** If $A$ and $B$ are $3 \times 3$ and $B = [\,\mathbf{b}_1 \;\; \mathbf{b}_2 \;\; \mathbf{b}_3\,]$, then $AB = [\,A\mathbf{b}_1 + A\mathbf{b}_2 + A\mathbf{b}_3\,]$.

(17) **(T/F)** Each column of $AB$ is a linear combination of the columns of $B$ using weights from the corresponding column of $A$.

(18) **(T/F)** The second row of $AB$ is the second row of $A$ multiplied on the right by $B$.

#### 解答
- (15) **False.** 正確的是 $AB = [\,A\mathbf{b}_1 \;\; A\mathbf{b}_2\,]$。而且 $\mathbf{a}_1\mathbf{b}_1$ 是 $2 \times 1$ 乘 $2 \times 1$,根本沒有定義。
- (16) **False.** 三個 $A\mathbf{b}_j$ 是**並排**成三行,不是相加成一行;右邊那個東西只有一行,大小也不對。
- (17) **False.** $A$ 和 $B$ 的角色顛倒了:$AB$ 的每一行是 **$A$ 的行**的線性組合,權重取自 **$B$ 的對應行**。
- (18) **True.** 這就是課本的式 (2):$\operatorname{row}_i(AB) = \operatorname{row}_i(A) \cdot B$,取 $i = 2$。

#### 備註
書後解答對 Exercises 15–23 只寫「Answer the questions before looking in the *Study Guide*.」,**沒有給 T/F**。上面的答案是本講義判定的,四題都可以用一句話的理由或一個 $2 \times 2$ 反例當場驗證。

(17) 是最有價值的一題:它把定義的兩個角色對調,學生若答 True,表示定義只背了一半。

### 變化 · Lay 2.1 Exercises 7–8
(7) If a matrix $A$ is $5 \times 3$ and the product $AB$ is $5 \times 7$, what is the size of $B$?

(8) How many rows does $B$ have if $BC$ is a $3 \times 4$ matrix?

#### 解答
(7) $B$ 是 $3 \times 7$。因為 $AB$ 有定義 ⇒ $B$ 的列數 = $A$ 的行數 = 3;$AB$ 的行數 7 就是 $B$ 的行數。

(8) $B$ 有 **3 列**。$BC$ 的列數就是 $B$ 的列數。(題目沒給 $C$ 的大小,所以 $B$ 的行數無法確定。)

### 變化 · Lay 2.1 Exercises 9–10
(9) Let $A = \begin{bmatrix} 3 & 4 \\ -2 & 1 \end{bmatrix}$ and $B = \begin{bmatrix} 5 & -6 \\ 3 & k \end{bmatrix}$. What value(s) of $k$, if any, will make $AB = BA$?

(10) Let $A = \begin{bmatrix} 3 & -6 \\ -4 & 8 \end{bmatrix}$, $B = \begin{bmatrix} 8 & 6 \\ 5 & 7 \end{bmatrix}$, $C = \begin{bmatrix} 6 & -2 \\ 4 & 3 \end{bmatrix}$. Verify that $AB = AC$ and yet $B \ne C$.

#### 解答
(9) 算出
$$AB - BA = \begin{bmatrix} 0 & 4k - 32 \\ 2k - 16 & 0 \end{bmatrix}$$
兩個非對角元素同時為 0 ⇒ $k = 8$。此時 $AB = BA = \begin{bmatrix} 27 & 14 \\ -7 & 20 \end{bmatrix}$。

(10) $AB = AC = \begin{bmatrix} -6 & -24 \\ 8 & 32 \end{bmatrix}$,但 $B \ne C$(例如左上角 $8 \ne 6$)。

這說明矩陣乘法**沒有消去律**:$AB = AC$ 推不出 $B = C$(課本 p. 128 的 Warning 2)。原因是 $A$ 的兩行線性相依($A$ 不可逆),這一點到觀念 4 會看得更清楚。

#### 備註
這兩題是「矩陣代數和數字代數不一樣」的核心證據,務必課堂做。做完可以問學生:「什麼時候 $AB = AC$ 才能消掉 $A$?」答案要等到觀念 4 的反矩陣。

### 變化 · Lay 2.1 Exercises 11–12
(11) Let $A = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \\ 1 & 4 & 5 \end{bmatrix}$ and $D = \begin{bmatrix} 2 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix}$. Compute $AD$ and $DA$. Explain how the columns or rows of $A$ change when $A$ is multiplied by $D$ on the right or on the left. Find a $3 \times 3$ matrix $B$, not the identity matrix or the zero matrix, such that $AB = BA$.

(12) Let $A = \begin{bmatrix} 2 & -8 \\ -1 & 4 \end{bmatrix}$. Construct a $2 \times 2$ matrix $B$ such that $AB$ is the zero matrix. Use two different nonzero columns for $B$.

#### 解答
(11)
$$AD = \begin{bmatrix} 2 & 3 & 5 \\ 2 & 6 & 15 \\ 2 & 12 & 25 \end{bmatrix}, \qquad DA = \begin{bmatrix} 2 & 2 & 2 \\ 3 & 6 & 9 \\ 5 & 20 & 25 \end{bmatrix}$$
**右乘 $D$**:把 $A$ 的**第 $j$ 行**乘上 $D$ 的第 $j$ 個對角元;**左乘 $D$**:把 $A$ 的**第 $i$ 列**乘上 $D$ 的第 $i$ 個對角元。

可交換的 $B$:取 $B = 2I_3$(任何 $cI_3$,$c \ne 0, 1$ 都可以),因為純量矩陣和任何矩陣都可交換。$B = A$ 或 $B = A^2$ 也是合法答案。

(12) 要讓 $AB = 0$,$B$ 的**每一行**都必須滿足 $A\mathbf{x} = \mathbf{0}$。解 $2x_1 - 8x_2 = 0$ 得 $x_1 = 4x_2$,所以取 $\begin{bmatrix} 4 \\ 1 \end{bmatrix}$ 的兩個相異非零倍數:
$$B = \begin{bmatrix} 4 & 8 \\ 1 & 2 \end{bmatrix} \quad\Longrightarrow\quad AB = \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$$
答案不唯一。

#### 備註
(11) 的「對角矩陣 = 逐行(或逐列)縮放」在後面很常用(第 11 週的對角化、第 16 週的 SVD 都靠這個直覺),值得多講兩句。$B$ 那一小題書上沒給答案,$2I_3$ 是最省事的;若想要非純量矩陣的例子,$B = A$ 即可。

(12) 對應課本 p. 128 的 Warning 3:$AB = 0$ 推不出 $A = 0$ 或 $B = 0$。

### 變化 · Lay 2.1 Exercise 25
If $A = \begin{bmatrix} 1 & -3 \\ -3 & 8 \end{bmatrix}$ and $AB = \begin{bmatrix} -1 & 3 & -2 \\ 1 & -7 & 3 \end{bmatrix}$, determine the first and second columns of $B$.

#### 解答
$AB$ 的第 $j$ 行就是 $A\mathbf{b}_j$,所以逐行解方程組:

$A\mathbf{b}_1 = \begin{bmatrix} -1 \\ 1 \end{bmatrix} \Rightarrow \mathbf{b}_1 = \begin{bmatrix} 5 \\ 2 \end{bmatrix}$;$A\mathbf{b}_2 = \begin{bmatrix} 3 \\ -7 \end{bmatrix} \Rightarrow \mathbf{b}_2 = \begin{bmatrix} -3 \\ -2 \end{bmatrix}$。

#### 備註
這題把乘法的行定義**反過來用**:已知乘積求因數。解法是解兩個 $2 \times 2$ 方程組(或到觀念 4 之後,直接乘 $A^{-1}$)。

順帶一提,第三行是 $\begin{bmatrix} 7 \\ 3 \end{bmatrix}$,但題目只問前兩行。

### 應用 · Lay 2.1 Exercises 13–14
(13) Let $\mathbf{r}_1, \dots, \mathbf{r}_p$ be vectors in $\mathbb{R}^n$, and let $Q$ be an $m \times n$ matrix. Write the matrix $[\,Q\mathbf{r}_1 \;\cdots\; Q\mathbf{r}_p\,]$ as a *product* of two matrices (neither of which is an identity matrix).

(14) Let $U$ be the $3 \times 2$ cost matrix described in Example 6 of Section 1.8. The first column of $U$ lists the costs per dollar of output for manufacturing product B, and the second column lists the costs per dollar of output for product C. (The costs are categorized as materials, labor, and overhead.) Let $\mathbf{q}_1$ be a vector in $\mathbb{R}^2$ that lists the output (measured in dollars) of products B and C manufactured during the first quarter of the year, and let $\mathbf{q}_2, \mathbf{q}_3$, and $\mathbf{q}_4$ be the analogous vectors that list the amounts of products B and C manufactured in the second, third, and fourth quarters, respectively. Give an economic description of the data in the matrix $UQ$, where $Q = [\,\mathbf{q}_1 \;\; \mathbf{q}_2 \;\; \mathbf{q}_3 \;\; \mathbf{q}_4\,]$.

#### 解答
(13) 令 $R = [\,\mathbf{r}_1 \;\cdots\; \mathbf{r}_p\,]$(這是 $n \times p$ 矩陣),則
$$[\,Q\mathbf{r}_1 \;\cdots\; Q\mathbf{r}_p\,] = QR$$
這正是乘法的行定義本身。

(14) $UQ$ 是 $3 \times 4$ 矩陣,第 $j$ 行 $= U\mathbf{q}_j$,也就是**第 $j$ 季**生產 B、C 兩種產品所花的總材料費、總人工費、總管銷費。整個矩陣就是一張「成本類別 × 季別」的年度成本報表:第 $(i, j)$ 格 = 第 $j$ 季第 $i$ 類成本的總金額。

#### 備註
(14) 要翻回第 4 週用過的 Lay 1.8 Example 6(書上 p. 96)才知道 $U = \begin{bmatrix} .45 & .40 \\ .25 & .30 \\ .15 & .15 \end{bmatrix}$(三列依序是 Materials、Labor、Overhead)。上課時把這個矩陣抄在黑板上再問學生 $UQ$ 是什麼,效果比直接講好。

這題是本週「矩陣乘法在做什麼」最貼近生活的例子:**一次算完四季、三種成本**。

### 應用 · Lay 2.1 Exercises 51–52(T 電腦題)
(51) Use the matrix $A = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ to switch the first and second rows of the matrix $M$ containing dates of accidents at the Montreal Trudeau Airport.

$$M = \begin{bmatrix} 2 & 3 & 16 & 24 & 25 & 26 & 6 & 7 & 19 & 26 \\ 1 & 1 & 1 & 1 & 1 & 1 & 2 & 2 & 2 & 2 \end{bmatrix}$$

This data in matrix $M$ has been scrubbed in matrix $AM$ and can be fed into the same machine as the other data from Example 10.

(52) Use the matrix $B = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$ to remove the last row from the matrix $N$ containing dates of accidents at the New York JFK Airport.

$$N = \begin{bmatrix} 1 & 1 & 1 & 1 & 2 & 2 & 2 \\ 1 & 12 & 21 & 22 & 3 & 20 & 21 \\ 2020 & 2020 & 2020 & 2020 & 2020 & 2020 & 2020 \end{bmatrix}$$

The data in matrix $N$ has been scrubbed in matrix $BN$ and can be fed into the same machine as the other data from Example 10.

#### 解答
(51)
$$AM = \begin{bmatrix} 1 & 1 & 1 & 1 & 1 & 1 & 2 & 2 & 2 & 2 \\ 2 & 3 & 16 & 24 & 25 & 26 & 6 & 7 & 19 & 26 \end{bmatrix}$$
左乘 $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ 就是把兩列對調,資料從「日/月」變成「月/日」。

(52)
$$BN = \begin{bmatrix} 1 & 1 & 1 & 1 & 2 & 2 & 2 \\ 1 & 12 & 21 & 22 & 3 & 20 & 21 \end{bmatrix}$$
$B$ 是「只取前兩列」的挑選矩陣,左乘之後第三列(年份)就被刪掉了。

#### 備註
這兩題其實是**資料清洗(data scrubbing)**:用矩陣乘法做「換列」與「刪列」,不必寫迴圈。放進實作課做,並順便講一句——pandas 的 `df[['month','day']]` 底層就是這種挑選運算。

課本說這是華盛頓州立大學資料分析課學生在真實專案裡遇到的第一步。

### 挑戰 · Lay 2.1 Exercises 26–30
(26) Suppose the first two columns, $\mathbf{b}_1$ and $\mathbf{b}_2$, of $B$ are equal. What can you say about the columns of $AB$ (if $AB$ is defined)? Why?

(27) Suppose the third column of $B$ is the sum of the first two columns. What can you say about the third column of $AB$? Why?

(28) Suppose the second column of $B$ is all zeros. What can you say about the second column of $AB$?

(29) Suppose the last column of $AB$ is all zeros, but $B$ itself has no column of zeros. What can you say about the columns of $A$?

(30) Show that if the columns of $B$ are linearly dependent, then so are the columns of $AB$.

#### 解答
- (26) $AB$ 的**前兩行也相等**:$AB = [\,A\mathbf{b}_1 \;\; A\mathbf{b}_2 \;\cdots]$,既然 $\mathbf{b}_1 = \mathbf{b}_2$,自然 $A\mathbf{b}_1 = A\mathbf{b}_2$。
- (27) $AB$ 的第三行等於**前兩行之和**:$A\mathbf{b}_3 = A(\mathbf{b}_1 + \mathbf{b}_2) = A\mathbf{b}_1 + A\mathbf{b}_2$。
- (28) $AB$ 的第二行**也全是零**:$A\mathbf{b}_2 = A\mathbf{0} = \mathbf{0}$。
- (29) $A$ 的**行線性相依**。設 $B$ 的最後一行是 $\mathbf{b}_p \ne \mathbf{0}$,則 $A\mathbf{b}_p = \mathbf{0}$ 表示 $A\mathbf{x} = \mathbf{0}$ 有非平凡解,所以 $A$ 的行線性相依(第 3 週)。
- (30) $B$ 的行線性相依 ⇒ 存在 $\mathbf{x} \ne \mathbf{0}$ 使 $B\mathbf{x} = \mathbf{0}$。那麼
  $$(AB)\mathbf{x} = A(B\mathbf{x}) = A\mathbf{0} = \mathbf{0}$$
  同一個非零 $\mathbf{x}$ 也讓 $(AB)\mathbf{x} = \mathbf{0}$,所以 $AB$ 的行也線性相依。∎

#### 備註
這五題全部只靠一句話:**$AB$ 的第 $j$ 行是 $A\mathbf{b}_j$**。適合當「一句話講完」的示範,五題連著做,學生會發現自己在重複同一個動作。

(30) 用到結合律 $(AB)\mathbf{x} = A(B\mathbf{x})$,正好接到證明時刻。

### 挑戰 · Lay 2.1 Exercises 37–40
(37) Prove Theorem 2(b) and 2(c). Use the row–column rule. The $(i, j)$-entry in $A(B + C)$ can be written as

$$a_{i1}(b_{1j} + c_{1j}) + \cdots + a_{in}(b_{nj} + c_{nj}) \quad\text{or}\quad \sum_{k=1}^{n} a_{ik}(b_{kj} + c_{kj})$$

(38) Prove Theorem 2(d). [*Hint:* The $(i, j)$-entry in $(rA)B$ is $(ra_{i1})b_{1j} + \cdots + (ra_{in})b_{nj}$.]

(39) Show that $I_mA = A$ when $A$ is an $m \times n$ matrix. You can assume $I_m\mathbf{x} = \mathbf{x}$ for all $\mathbf{x}$ in $\mathbb{R}^m$.

(40) Show that $AI_n = A$ when $A$ is an $m \times n$ matrix. [*Hint:* Use the (column) definition of $AI_n$.]

#### 解答
- (37) $A(B + C)$ 的 $(i, j)$ 格 $= \sum_k a_{ik}(b_{kj} + c_{kj}) = \sum_k a_{ik}b_{kj} + \sum_k a_{ik}c_{kj}$,前項是 $AB$ 的 $(i,j)$ 格、後項是 $AC$ 的,所以 $A(B+C) = AB + AC$。同理 $(B+C)A$ 的 $(i,j)$ 格 $= \sum_k (b_{ik} + c_{ik})a_{kj} = \sum_k b_{ik}a_{kj} + \sum_k c_{ik}a_{kj}$,得 $(B+C)A = BA + CA$。
- (38) $(rA)B$ 的 $(i,j)$ 格 $= \sum_k (ra_{ik})b_{kj} = r\sum_k a_{ik}b_{kj}$,即 $r(AB)$ 的 $(i,j)$ 格;又 $\sum_k (ra_{ik})b_{kj} = \sum_k a_{ik}(rb_{kj})$,即 $A(rB)$ 的 $(i,j)$ 格。故三者相等。
- (39) 把 $A$ 按行寫成 $[\,\mathbf{a}_1 \cdots \mathbf{a}_n\,]$,依乘法的行定義 $I_mA = [\,I_m\mathbf{a}_1 \cdots I_m\mathbf{a}_n\,] = [\,\mathbf{a}_1 \cdots \mathbf{a}_n\,] = A$。
- (40) $I_n = [\,\mathbf{e}_1 \cdots \mathbf{e}_n\,]$,所以 $AI_n = [\,A\mathbf{e}_1 \cdots A\mathbf{e}_n\,]$;而 $A\mathbf{e}_j$ 正是 $A$ 的第 $j$ 行(第 4 週),故 $AI_n = A$。

#### 備註
(37)(38) 是「逐格證明」的標準寫法,(39)(40) 是「逐行證明」的標準寫法。同一組結論、兩種證法,很適合讓學生比較哪一種好寫。

數理弱的班級可以只做 (39)(40),它們短、而且只用到第 4 週的 $A\mathbf{e}_j$ = 第 $j$ 行。

### 挑戰 · Lay 2.1 Exercise 45(T)與 Practice Problem 3
(45) Construct a random $4 \times 4$ matrix $A$ and test whether $(A + I)(A - I) = A^2 - I$. The best way to do this is to compute $(A + I)(A - I) - (A^2 - I)$ and verify that this difference is the zero matrix. Do this for three random matrices. Then test $(A + B)(A - B) = A^2 - B^2$ the same way for three pairs of random $4 \times 4$ matrices. Report your conclusions.

(Practice Problem 3) Suppose $A$ is an $m \times n$ matrix, all of whose rows are identical. Suppose $B$ is an $n \times p$ matrix, all of whose columns are identical. What can be said about the entries in $AB$?

#### 解答
(45) 第一條**恆成立**:
$$(A + I)(A - I) = A^2 - AI + IA - I^2 = A^2 - A + A - I = A^2 - I$$
關鍵是 $A$ 和 $I$ 一定可交換。三個隨機矩陣的差都會是零矩陣。

第二條**一般不成立**:
$$(A + B)(A - B) = A^2 - AB + BA - B^2$$
只有在 $AB = BA$ 時才等於 $A^2 - B^2$。隨機的 $A$、$B$ 幾乎不會可交換,所以三組測試的差都不是零矩陣,而且差正好是 $BA - AB$。

(Practice Problem 3) $AB$ 的**所有元素都相同**。理由兩步:$AB = [\,A\mathbf{b}_1 \cdots A\mathbf{b}_p\,]$,而 $B$ 的各行相同 ⇒ $AB$ 的各行相同;又 $\operatorname{row}_i(AB) = \operatorname{row}_i(A) \cdot B$,而 $A$ 的各列相同 ⇒ $AB$ 的各列相同。行全同加上列全同,就是整個矩陣每一格都一樣。

#### 備註
(45) 標了 T,放進實作課做——它示範了一件重要的事:**用隨機矩陣做實驗,可以很快看出一個式子是不是恆等式**。但要提醒學生:測三次都成立不算證明,測一次不成立卻足以否定。

Practice Problem 3 把「行的定義」和「列的規則」兩招合起來用,是本節最漂亮的一題。

## 驗算
```check
Matrix([[2, 3], [1, -5]]) * Matrix([[4, 3, 6], [1, -2, 3]]) == Matrix([[11, 0, 21], [-1, 13, -9]])
(Matrix([[2, -5, 0], [-1, 3, -4], [6, -8, -7], [-3, 0, 9]]) * Matrix([[4, -6], [7, 1], [3, 2]])).row(1) == Matrix([[5, 1]])
(Matrix([[2, 3], [1, -5]]) * Matrix([[4, 3, 6], [1, -2, 3]])).shape == (2, 3)
-2 * Matrix([[2, 0, -1], [4, -3, 2]]) == Matrix([[-4, 0, 2], [-8, 6, -4]])
Matrix([[7, -5, 1], [1, -4, -3]]) - 2 * Matrix([[2, 0, -1], [4, -3, 2]]) == Matrix([[3, -5, 3], [-7, 2, -7]])
Matrix([[1, 2], [-2, 1]]) * Matrix([[3, 5], [-1, 4]]) == Matrix([[1, 13], [-7, -6]])
Matrix([[2, 0, -1], [4, -3, 2]]) + 2 * Matrix([[7, -5, 1], [1, -4, -3]]) == Matrix([[16, -10, 1], [6, -11, -4]])
Matrix([[1, 2], [-2, 1]]) * Matrix([[7, -5, 1], [1, -4, -3]]) == Matrix([[9, -13, -5], [-13, 6, -5]])
Matrix([[2, 0, -1], [4, -3, 2]]).shape[1] != Matrix([[1, 2], [-2, 1]]).shape[0]
Matrix([[-1, 2], [5, 4], [2, -3]]) * Matrix([[3, -4], [-2, 1]]) == Matrix([[-7, 6], [7, -16], [12, -11]])
Matrix([[4, -2], [-3, 0], [3, 5]]) * Matrix([[1, 3], [4, -1]]) == Matrix([[-4, 14], [-3, -9], [23, 4]])
(zeros(5, 3) * zeros(3, 7)).shape == (5, 7)
(zeros(3, 2) * zeros(2, 4)).shape == (3, 4)
Matrix([[3, 4], [-2, 1]]) * Matrix([[5, -6], [3, 8]]) == Matrix([[5, -6], [3, 8]]) * Matrix([[3, 4], [-2, 1]]) == Matrix([[27, 14], [-7, 20]])
solve(list(Matrix([[3, 4], [-2, 1]]) * Matrix([[5, -6], [3, k]]) - Matrix([[5, -6], [3, k]]) * Matrix([[3, 4], [-2, 1]])), k) == {k: 8}
Matrix([[3, -6], [-4, 8]]) * Matrix([[8, 6], [5, 7]]) == Matrix([[3, -6], [-4, 8]]) * Matrix([[6, -2], [4, 3]]) == Matrix([[-6, -24], [8, 32]])
Matrix([[8, 6], [5, 7]]) != Matrix([[6, -2], [4, 3]])
Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]]) * diag(2, 3, 5) == Matrix([[2, 3, 5], [2, 6, 15], [2, 12, 25]])
diag(2, 3, 5) * Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]]) == Matrix([[2, 2, 2], [3, 6, 9], [5, 20, 25]])
Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]]) * (2 * eye(3)) == (2 * eye(3)) * Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]])
Matrix([[2, -8], [-1, 4]]) * Matrix([[4, 8], [1, 2]]) == zeros(2, 2)
Matrix.hstack(Matrix([[1, 2], [3, 4], [5, 6]]) * Matrix([1, 2]), Matrix([[1, 2], [3, 4], [5, 6]]) * Matrix([3, 4])) == Matrix([[1, 2], [3, 4], [5, 6]]) * Matrix([[1, 3], [2, 4]])
Matrix([[Rational(45,100), Rational(40,100)], [Rational(25,100), Rational(30,100)], [Rational(15,100), Rational(15,100)]]) * Matrix([1, 5]) == Matrix([Rational(245,100), Rational(175,100), Rational(90,100)])
Matrix([[1, -3], [-3, 8]]) * Matrix([[5, -3], [2, -2]]) == Matrix([[-1, 3], [1, -7]])
(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 5, 7], [6, 6, 8]]))[:, 0] == (Matrix([[1, 2], [3, 4]]) * Matrix([[5, 5, 7], [6, 6, 8]]))[:, 1]
(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 7, 12], [6, 8, 14]]))[:, 2] == (Matrix([[1, 2], [3, 4]]) * Matrix([[5, 7, 12], [6, 8, 14]]))[:, 0] + (Matrix([[1, 2], [3, 4]]) * Matrix([[5, 7, 12], [6, 8, 14]]))[:, 1]
(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 0, 7], [6, 0, 8]]))[:, 1] == zeros(2, 1)
Matrix([[1, 2], [2, 4]]) * Matrix([[1, 2], [0, -1]]) == Matrix([[1, 0], [2, 0]]) and Matrix([[1, 2], [2, 4]]).rank() < 2
(Matrix([[1, 2], [3, 4], [5, 6]]) * Matrix([[1, 2], [1, 2]])).rank() == Matrix([[1, 2], [1, 2]]).rank() == 1
expand(Matrix([[a, b], [c, d]]) * (Matrix([[x1, x2], [x3, x4]]) + Matrix([[h, k], [s, t]]))) == expand(Matrix([[a, b], [c, d]]) * Matrix([[x1, x2], [x3, x4]]) + Matrix([[a, b], [c, d]]) * Matrix([[h, k], [s, t]]))
expand((Matrix([[x1, x2], [x3, x4]]) + Matrix([[h, k], [s, t]])) * Matrix([[a, b], [c, d]])) == expand(Matrix([[x1, x2], [x3, x4]]) * Matrix([[a, b], [c, d]]) + Matrix([[h, k], [s, t]]) * Matrix([[a, b], [c, d]]))
expand(t * (Matrix([[a, b], [c, d]]) * Matrix([[x1, x2], [x3, x4]]))) == expand((t * Matrix([[a, b], [c, d]])) * Matrix([[x1, x2], [x3, x4]])) == expand(Matrix([[a, b], [c, d]]) * (t * Matrix([[x1, x2], [x3, x4]])))
eye(2) * Matrix([[a, b, c], [d, f, g]]) == Matrix([[a, b, c], [d, f, g]]) == Matrix([[a, b, c], [d, f, g]]) * eye(3)
expand((Matrix([[a, b], [c, d]]) + eye(2)) * (Matrix([[a, b], [c, d]]) - eye(2)) - (Matrix([[a, b], [c, d]])**2 - eye(2))) == zeros(2, 2)
expand((Matrix([[0, 1], [0, 0]]) + Matrix([[0, 0], [1, 0]])) * (Matrix([[0, 1], [0, 0]]) - Matrix([[0, 0], [1, 0]])) - (Matrix([[0, 1], [0, 0]])**2 - Matrix([[0, 0], [1, 0]])**2)) != zeros(2, 2)
Matrix([[0, 1], [1, 0]]) * Matrix([[2, 3, 16, 24, 25, 26, 6, 7, 19, 26], [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]]) == Matrix([[1, 1, 1, 1, 1, 1, 2, 2, 2, 2], [2, 3, 16, 24, 25, 26, 6, 7, 19, 26]])
Matrix([[1, 0, 0], [0, 1, 0]]) * Matrix([[1, 1, 1, 1, 2, 2, 2], [1, 12, 21, 22, 3, 20, 21], [2020, 2020, 2020, 2020, 2020, 2020, 2020]]) == Matrix([[1, 1, 1, 1, 2, 2, 2], [1, 12, 21, 22, 3, 20, 21]])
Matrix([[1, 2, 3], [1, 2, 3]]) * Matrix([[4, 4], [5, 5], [6, 6]]) == Matrix([[32, 32], [32, 32]])
```


