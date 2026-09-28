---
title_en: The Column Space and the Null Space of a Matrix
title_zh: 行空間與零空間:一個矩陣帶來的兩個子空間
sub: Col A lives in Rᵐ, Nul A lives in Rⁿ
level: mid
source: Lay 2.8
lab_hook: '`A.columnspace()` 與 `A.nullspace()`:注意兩者的向量長度不一樣'
---
## 觀念
**Definition.** The **column space** of a matrix $A$ is the set $\operatorname{Col} A$ of all linear combinations of the columns of $A$.

If $A = [\,\mathbf{a}_1 \;\cdots\; \mathbf{a}_n\,]$ with the columns in $\mathbb{R}^m$, then $\operatorname{Col} A$ is the same as $\operatorname{Span}\{\mathbf{a}_1, \dots, \mathbf{a}_n\}$. So $\operatorname{Col} A$ is a subspace of $\mathbb{R}^m$.

Example 4 shows that the column space of an $m \times n$ matrix is a subspace of $\mathbb{R}^m$. Note that $\operatorname{Col} A$ equals $\mathbb{R}^m$ only when the columns of $A$ span $\mathbb{R}^m$. Otherwise, $\operatorname{Col} A$ is only part of $\mathbb{R}^m$.

The solution of Example 4 shows that when a system of linear equations is written in the form $A\mathbf{x} = \mathbf{b}$, the column space of $A$ is the set of all $\mathbf{b}$ for which the system has a solution.

寫成集合就是下面這個式子(這個寫法出自課本 4.2 節,本講義先借用,因為它最好記):

$$\operatorname{Col} A = \{\mathbf{b} : \mathbf{b} = A\mathbf{x} \text{ for some } \mathbf{x} \text{ in } \mathbb{R}^n\}$$

**Definition.** The **null space** of a matrix $A$ is the set $\operatorname{Nul} A$ of all solutions of the homogeneous equation $A\mathbf{x} = \mathbf{0}$.

**Theorem 12.** The null space of an $m \times n$ matrix $A$ is a subspace of $\mathbb{R}^n$. Equivalently, the set of all solutions of a system $A\mathbf{x} = \mathbf{0}$ of $m$ homogeneous linear equations in $n$ unknowns is a subspace of $\mathbb{R}^n$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| column space $\operatorname{Col} A$ | 行空間 | 各行所有線性組合的集合,住在 $\mathbb{R}^m$ |
| null space $\operatorname{Nul} A$ | 零空間 | $A\mathbf{x} = \mathbf{0}$ 的所有解,住在 $\mathbb{R}^n$ |
| homogeneous equation | 齊次方程 | 右端是 $\mathbf{0}$ 的方程(第 3 週) |
| implicitly defined | 隱式定義 | $\operatorname{Nul} A$ 只給條件,不直接列出元素 |
| explicitly defined | 顯式定義 | $\operatorname{Col} A$ 直接給出生成元(各行) |

## 白話說
**一個矩陣 $A$ 會帶出兩個子空間,而且它們住在不同的空間裡。**

![$\operatorname{Nul} A$ 在輸入側($\mathbb{R}^n$),$\operatorname{Col} A$ 在輸出側($\mathbb{R}^m$)。](col-nul.svg)

| | $\operatorname{Col} A$ | $\operatorname{Nul} A$ |
|---|---|---|
| 是什麼 | 各行的所有線性組合 | $A\mathbf{x} = \mathbf{0}$ 的所有解 |
| 住在哪 | $\mathbb{R}^m$(**列**數) | $\mathbb{R}^n$(**行**數) |
| 用機器的話說 | **到得了的所有輸出** | **被壓成 0 的所有輸入** |
| 怎麼給的 | 顯式:直接給生成元(各行) | 隱式:只給條件 $A\mathbf{x} = \mathbf{0}$ |
| 判斷 $\mathbf{v}$ 在不在 | 要**解方程組** $A\mathbf{x} = \mathbf{v}$ | 只要**乘一次** $A\mathbf{v}$ 看是不是 $\mathbf{0}$ |

**口訣**:$m \times n$ 矩陣 → $\operatorname{Col} A \subseteq \mathbb{R}^m$、$\operatorname{Nul} A \subseteq \mathbb{R}^n$。

**為什麼 $\operatorname{Col} A$ 就是「有解的那些 $\mathbf{b}$」?** 因為 $A\mathbf{x}$ 永遠是各行的線性組合(第 2 週)。所以

$$\mathbf{b} \in \operatorname{Col} A \iff A\mathbf{x} = \mathbf{b} \text{ 有解}$$

這句話把「行空間」和「方程組有沒有解」綁在一起——第 2 週的老問題,換了一個名字。

**兩個空間毫不相干。** 同一個向量可能在其中一個裡而不在另一個裡(Practice Problem 1 就是這樣)。對 $n \times n$ 矩陣而言,唯一同時屬於兩者的向量通常只有 $\mathbf{0}$。

## 幾何意義
用第 4 週「矩陣是一台機器」的說法:

- $\operatorname{Col} A$ 是**輸出端的可達範圍**。機器再怎麼調輸入,輸出只能落在這個集合裡。
- $\operatorname{Nul} A$ 是**輸入端的盲區**。這些輸入全部被壓成 $\mathbf{0}$,機器「看不見」它們。

$\operatorname{Nul} A$ 越大,表示機器壓掉的資訊越多;$\operatorname{Col} A$ 越小,表示輸出的花樣越少。**這兩件事有一個精確的關係,就是下下個觀念的 Rank Theorem。**

## 在資工哪裡用
- **$\operatorname{Col} A$ = 系統做得到的事**。控制系統的可達狀態、圖學管線能畫出的所有位置、線性模型能表示的所有預測值,都是某個矩陣的行空間。
- **$\operatorname{Nul} A$ = 被丟掉的資訊**。投影把一整條線壓成一點,那條線就是零空間;壓縮、降維、量化都在製造非零的零空間。
- **錯誤更正碼的核心**:Hamming 碼的合法碼字集合正是某個檢查矩陣 $H$ 的零空間 $\operatorname{Nul} H$(見補充觀念)。「收到的字合不合法」就是在問「它在不在 $\operatorname{Nul} H$ 裡」——**而這只要乘一次矩陣**。
- **判斷成本差很多**:檢查 $\operatorname{Nul}$ 只要一次乘法($O(mn)$),檢查 $\operatorname{Col}$ 要解方程組($O(mn^2)$)。設計系統時,把「要常常檢查」的那件事放在零空間這一側。

## 原理
**Theorem 12 的證明**(課本 p. 181):要證 $\operatorname{Nul} A$ 是子空間,就逐條驗上一個觀念的三個條件。

1. **含 $\mathbf{0}$**:$A\mathbf{0} = \mathbf{0}$,所以 $\mathbf{0} \in \operatorname{Nul} A$。✓
2. **對加法封閉**:設 $\mathbf{u}, \mathbf{v} \in \operatorname{Nul} A$,即 $A\mathbf{u} = \mathbf{0}$、$A\mathbf{v} = \mathbf{0}$。由矩陣乘法的性質(第 5 週 Theorem 2),
   $$A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v} = \mathbf{0} + \mathbf{0} = \mathbf{0}$$
   所以 $\mathbf{u} + \mathbf{v} \in \operatorname{Nul} A$。✓
3. **對純量乘法封閉**:$A(c\mathbf{u}) = c(A\mathbf{u}) = c\mathbf{0} = \mathbf{0}$,所以 $c\mathbf{u} \in \operatorname{Nul} A$。✓

$\blacksquare$

**注意這個證明只用到「乘以 $A$ 是線性的」**。所以同樣的論證對任何線性變換都成立——這是為什麼線性代數裡到處都是子空間。

**$\operatorname{Col} A$ 為什麼是子空間?** 不必重證:$\operatorname{Col} A = \operatorname{Span}\{\mathbf{a}_1, \dots, \mathbf{a}_n\}$,而上一個觀念已經證過 Span 一定是子空間。

**兩種定義方式的差別**(課本 p. 181 特別點出):

- $\operatorname{Col} A$ 是**顯式**定義的:給你生成元,要列出成員很容易(隨便取線性組合),但要判斷某個 $\mathbf{b}$ 在不在裡面,得解方程組。
- $\operatorname{Nul} A$ 是**隱式**定義的:只給條件。判斷某個 $\mathbf{v}$ 在不在裡面很容易(乘一次就知道),但要列出成員得解 $A\mathbf{x} = \mathbf{0}$。

**兩者的難易恰好相反**,這一點在實務上很重要。

## 老師講解
### 例 1 · Lay 2.8 Practice Problem 1
Let $A = \begin{bmatrix} 1 & -1 & 5 \\ 2 & 0 & 7 \\ -3 & -5 & -3 \end{bmatrix}$ and $\mathbf{u} = \begin{bmatrix} -7 \\ 3 \\ 2 \end{bmatrix}$. Is $\mathbf{u}$ in $\operatorname{Nul} A$? Is $\mathbf{u}$ in $\operatorname{Col} A$? Justify each answer.

1. **先問 $\operatorname{Nul} A$,因為它比較快**——只要乘一次。
   $$A\mathbf{u} = \begin{bmatrix} 1 & -1 & 5 \\ 2 & 0 & 7 \\ -3 & -5 & -3 \end{bmatrix}\begin{bmatrix} -7 \\ 3 \\ 2 \end{bmatrix} = \begin{bmatrix} -7 - 3 + 10 \\ -14 + 0 + 14 \\ 21 - 15 - 6 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$$
2. **是 $\mathbf{0}$**,所以 $\mathbf{u} \in \operatorname{Nul} A$。✓
3. **再問 $\operatorname{Col} A$。** 這次要解方程組 $A\mathbf{x} = \mathbf{u}$,也就是看增廣矩陣 $[\,A \;\; \mathbf{u}\,]$ 相不相容。
4. **列化簡**:
   $$[\,A \;\; \mathbf{u}\,] \sim \begin{bmatrix} 1 & -1 & 5 & -7 \\ 0 & 2 & -3 & 17 \\ 0 & 0 & 0 & 49 \end{bmatrix}$$
5. **最後一列是 $0 = 49$**,矛盾,方程組無解。所以 $\mathbf{u} \notin \operatorname{Col} A$。
6. **這題的重點**:同一個向量,**在一個子空間裡、不在另一個裡**。兩個空間毫不相干,不要以為「在 $\operatorname{Nul}$ 裡就一定在 $\operatorname{Col}$ 裡」。
7. **順便記下兩種判斷的成本**:$\operatorname{Nul}$ 乘一次就好,$\operatorname{Col}$ 要列化簡。考試時先做便宜的那個。

### 例 2 · Lay 2.8 Example 4(書上 p. 180)
Let $A = \begin{bmatrix} 1 & -3 & -4 \\ -4 & 6 & -2 \\ -3 & 7 & 6 \end{bmatrix}$ and $\mathbf{b} = \begin{bmatrix} 3 \\ 3 \\ -4 \end{bmatrix}$. Determine whether $\mathbf{b}$ is in the column space of $A$.

1. **先把問題翻譯成方程式**。$\mathbf{b} \in \operatorname{Col} A$ 的意思是「$\mathbf{b}$ 是各行的線性組合」,也就是**存在** $\mathbf{x}$ 使 $A\mathbf{x} = \mathbf{b}$。
2. **所以這題等於在問:$A\mathbf{x} = \mathbf{b}$ 相容嗎?** 不必解出 $\mathbf{x}$,只要判斷有沒有解。
3. **列化簡增廣矩陣**:
   $$[\,A \;\; \mathbf{b}\,] = \begin{bmatrix} 1 & -3 & -4 & 3 \\ -4 & 6 & -2 & 3 \\ -3 & 7 & 6 & -4 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & -4 & 3 \\ 0 & -6 & -18 & 15 \\ 0 & -2 & -6 & 5 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & -4 & 3 \\ 0 & -6 & -18 & 15 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
4. **讀結論**:最後一列是全 0(不是 $[0\ 0\ 0\ \ast]$ 那種矛盾列)⇒ **相容** ⇒ $\mathbf{b} \in \operatorname{Col} A$ ✓
5. **注意我們沒有算出 $\mathbf{x}$**。題目只問「在不在」,**判斷相容性就夠了**,這是最省力的做法。
6. **如果最後一列變成 $[\,0\ 0\ 0\ \ast\,]$($\ast \ne 0$)呢?** 那就不相容,$\mathbf{b}$ 不在 $\operatorname{Col} A$ 裡——這正是課本圖裡「$\mathbf{b}$ 落在平面外面」的情形。
7. **對比一下**:如果題目問的是「$\mathbf{b}$ 在不在 $\operatorname{Nul} A$ 裡」,做法完全不同——直接算 $A\mathbf{b}$ 看是不是 $\mathbf{0}$,一次乘法就結束。**兩個空間,兩種檢查。**

### 例 3 · 補充:同一個矩陣,兩個空間各找一個向量
For $A = \begin{bmatrix} 2 & 4 & -2 \\ -1 & -2 & 1 \\ 3 & 6 & -3 \end{bmatrix}$, find a nonzero vector in $\operatorname{Nul} A$ and a nonzero vector in $\operatorname{Col} A$, and state which space each one lives in.

1. **先看形狀**:$A$ 是 $3 \times 3$,所以兩個空間都是 $\mathbb{R}^3$ 的子空間——但它們**不是同一個子空間**。
2. **$\operatorname{Col} A$ 的向量最好找**:隨便取一行就是,例如 $\mathbf{a}_1 = (2, -1, 3)$。**各行依定義就在 $\operatorname{Col} A$ 裡**,不必算。
3. **看出這個矩陣的特別之處了嗎?** 第 2 行 $= 2 \times$ 第 1 行,第 3 行 $= -1 \times$ 第 1 行。**三行都在同一條直線上**,所以 $\operatorname{Col} A$ 只是一條直線(不是平面,更不是 $\mathbb{R}^3$)。
4. **$\operatorname{Nul} A$ 要解 $A\mathbf{x} = \mathbf{0}$**。因為三行成比例,相依關係一眼可見:
   $$\mathbf{a}_2 - 2\mathbf{a}_1 = \mathbf{0} \quad \Longrightarrow \quad (-2)\mathbf{a}_1 + 1 \cdot \mathbf{a}_2 + 0 \cdot \mathbf{a}_3 = \mathbf{0}$$
   **係數就是零空間的向量**:$\mathbf{u} = (-2, 1, 0)$。
5. **驗算**:$A\mathbf{u} = -2(2,-1,3) + 1(4,-2,6) = (0,0,0)$ ✓
6. **再找一個**:$\mathbf{a}_3 + \mathbf{a}_1 = \mathbf{0}$ ⇒ $\mathbf{v} = (1, 0, 1)$ 也在 $\operatorname{Nul} A$ 裡。
7. **這題的心法**:**$\operatorname{Col} A$ 看「行張出什麼」,$\operatorname{Nul} A$ 看「行之間有什麼相依關係」**——相依關係的係數直接就是零空間的向量,連列化簡都不必。
8. **最後確認兩者不同**:$(2,-1,3)$ 乘進去得 $A(2,-1,3)^T = (2 \cdot 2 - 4 - 6, \dots) = (-6, 3, -9) \ne \mathbf{0}$,所以它**不在** $\operatorname{Nul} A$ 裡。兩個空間確實是不同的集合。

#### 備註
例 2 是課本的原例,示範「判斷相容性」這個最省力的檢查法;例 3 是自編的,刻意挑**三行全部成比例**的矩陣,讓 $\operatorname{Col} A$ 塌成一條直線、相依關係一眼可見。

兩例合起來涵蓋了本節所有題型的做法,但**都不是練習卡上的題目**——練習時學生要自己再走一次流程。

若時間不夠,例 3 可以只做第 2、4 兩步(各找一個向量),第 8 步的「兩者不同」留給練習。

## 易錯點
- **把 $\operatorname{Col}$ 與 $\operatorname{Nul}$ 住的空間弄反**。$m \times n$ 矩陣:$\operatorname{Col} A \subseteq \mathbb{R}^m$、$\operatorname{Nul} A \subseteq \mathbb{R}^n$。
- **以為 $\operatorname{Col} A$ 是解集合**(Exercise 28 的陷阱)。$\operatorname{Col} A$ 裝的是**右端 $\mathbf{b}$**,不是解 $\mathbf{x}$。
- **判斷「在不在 $\operatorname{Col} A$ 裡」時只看一眼就說不在**。必須解方程組(或檢查 rank 有沒有變)。
- **以為兩個空間有包含關係**。它們通常連住的空間都不同,談包含沒有意義。
- **非方陣還用 IMT**(Exercises 43、44 的考點)。
- 算完 $\operatorname{Nul}$ 的向量不驗算。乘回去只要幾秒。

## 教學提示
這個觀念 25 分鐘,**最重要的是那張「兩個空間住不同地方」的圖**,建議直接畫在黑板上,左右各一個平面,中間一支箭頭寫「乘 A」。

開場可以先問:「一台機器,你會想知道它哪些事?」引導學生講出「做得到什麼」(值域 = $\operatorname{Col}$)與「什麼輸入沒效果」($\operatorname{Nul}$)。這兩個問題就是本節的全部。

那張對照表(誰住哪、怎麼判斷、成本)一定要抄黑板,學生的錯誤 80% 來自這張表。

課堂建議做:Practice Problem 1(一個向量、兩個判斷,最有代表性);Exercises 5、7、11、13;是非 Exercises 25、26(把 $m$、$n$ 寫反的對照題)。Exercises 39–44 建議挑兩題當堂寫,格式沿用上週的 IMT 寫法。

## 練習
### 照做 · Lay 2.8 Exercises 5–8
(5) Let $\mathbf{v}_1 = \begin{bmatrix} 2 \\ 3 \\ -5 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} -4 \\ -5 \\ 8 \end{bmatrix}$, and $\mathbf{w} = \begin{bmatrix} 8 \\ 2 \\ -9 \end{bmatrix}$. Determine if $\mathbf{w}$ is in the subspace of $\mathbb{R}^3$ generated by $\mathbf{v}_1$ and $\mathbf{v}_2$.

(6) Let $\mathbf{v}_1 = \begin{bmatrix} 1 \\ -2 \\ 4 \\ 3 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} 4 \\ -7 \\ 9 \\ 7 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} 5 \\ -8 \\ 6 \\ 5 \end{bmatrix}$, and $\mathbf{u} = \begin{bmatrix} -4 \\ 10 \\ -7 \\ -5 \end{bmatrix}$. Determine if $\mathbf{u}$ is in the subspace of $\mathbb{R}^4$ generated by $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$.

(7) Let $\mathbf{v}_1 = \begin{bmatrix} 2 \\ -8 \\ 6 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} -3 \\ 8 \\ -7 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} -4 \\ 6 \\ -7 \end{bmatrix}$, $\mathbf{p} = \begin{bmatrix} 6 \\ -10 \\ 11 \end{bmatrix}$, and $A = [\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]$.

- **a.** How many vectors are in $\{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$?
- **b.** How many vectors are in $\operatorname{Col} A$?
- **c.** Is $\mathbf{p}$ in $\operatorname{Col} A$? Why or why not?

(8) Let $\mathbf{v}_1 = \begin{bmatrix} -3 \\ 0 \\ 6 \end{bmatrix}$, $\mathbf{v}_2 = \begin{bmatrix} -2 \\ 2 \\ 3 \end{bmatrix}$, $\mathbf{v}_3 = \begin{bmatrix} 0 \\ -6 \\ 3 \end{bmatrix}$, and $\mathbf{p} = \begin{bmatrix} 1 \\ 14 \\ -9 \end{bmatrix}$. Determine if $\mathbf{p}$ is in $\operatorname{Col} A$, where $A = [\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{v}_3\,]$.

#### 解答
(5) **不在。** 列化簡 $[\,\mathbf{v}_1 \;\; \mathbf{v}_2 \;\; \mathbf{w}\,]$ 得 $I_3$,第三行成為樞軸行,表示方程組不相容。

(6) **不在。** 列化簡得
$$\begin{bmatrix} 1 & 0 & -3 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
最後一行是樞軸行,不相容。(順帶可看出 $\mathbf{v}_3 = -3\mathbf{v}_1 + 2\mathbf{v}_2$,三個 $\mathbf{v}$ 其實只張出一個平面。)

(7) **a.** 3 個(就是 $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3$)。
**b.** **無限多個**。$\operatorname{Col} A$ 是子空間,含非零向量,乘任意實數都還在裡面。
**c.** **在。** 列化簡 $[\,A \;\; \mathbf{p}\,]$ 得 $\begin{bmatrix} 1 & 0 & 7/4 & -9/4 \\ 0 & 1 & 5/2 & -7/2 \\ 0 & 0 & 0 & 0 \end{bmatrix}$,相容;例如 $\mathbf{p} = -\tfrac94\mathbf{v}_1 - \tfrac72\mathbf{v}_2$。

(8) **在。** 列化簡 $[\,A \;\; \mathbf{p}\,]$ 得相容系統,取 $x_3 = 0$ 得
$$\mathbf{p} = -5\mathbf{v}_1 + 7\mathbf{v}_2$$

#### 備註
(7) 的 a、b 兩小題是在考**「集合裡有幾個向量」與「子空間裡有幾個向量」的差別**,不是計算陷阱。很多學生會答 b 為 3,要特別點出來。

建議課堂做 (5)(7),(6)(8) 當作業。

### 照做 · Lay 2.8 Exercises 9–14
(9) With $A$ and $\mathbf{p}$ as in Exercise 7, determine if $\mathbf{p}$ is in $\operatorname{Nul} A$.

(10) With $\mathbf{u} = (-2, 3, 1)$ and $A$ as in Exercise 8, determine if $\mathbf{u}$ is in $\operatorname{Nul} A$.

In Exercises 11 and 12, give integers $p$ and $q$ such that $\operatorname{Nul} A$ is a subspace of $\mathbb{R}^p$ and $\operatorname{Col} A$ is a subspace of $\mathbb{R}^q$.

(11) $A = \begin{bmatrix} 3 & 2 & 1 & -5 \\ -9 & -4 & 1 & 7 \\ 9 & 2 & -5 & 1 \end{bmatrix}$

(12) $A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 7 \\ -5 & -1 & 0 \\ 2 & 7 & 11 \end{bmatrix}$

(13) For $A$ as in Exercise 11, find a nonzero vector in $\operatorname{Nul} A$ and a nonzero vector in $\operatorname{Col} A$.

(14) For $A$ as in Exercise 12, find a nonzero vector in $\operatorname{Nul} A$ and a nonzero vector in $\operatorname{Col} A$.

#### 解答
(9) **不在。** $A\mathbf{p} = (-2, -62, 29) \ne \mathbf{0}$。

(10) **在。** $A\mathbf{u} = \mathbf{0}$。

(11) $p = 4$、$q = 3$($A$ 是 $3 \times 4$:解向量有 4 個分量,每一行有 3 個分量)。

(12) $p = 3$、$q = 4$($A$ 是 $4 \times 3$)。

(13) $\operatorname{Nul} A$:$(1, -2, 1, 0)$ 或 $(-1, 4, 0, 1)$。$\operatorname{Col} A$:隨便取 $A$ 的一行,例如 $(3, -9, 9)$。

(14) $\operatorname{Nul} A$:$(1, -5, 3)$。$\operatorname{Col} A$:例如第一行 $(1, 4, -5, 2)$。

#### 備註
(9) 和 (7c) 用的是同一個 $A$ 與 $\mathbf{p}$:$\mathbf{p}$ **在 $\operatorname{Col} A$ 裡卻不在 $\operatorname{Nul} A$ 裡**。這一對題目最能說明「兩個空間毫不相干」,務必連著做。

(13)(14) 的零空間向量**不唯一**(任何非零倍數或組合都可以):(14) 寫成 $(1/3, -5/3, 1)$ 一樣對,本講義取整數倍比較好檢查。(14) 是偶數題,**書後無解答**。

$\operatorname{Col} A$ 的向量「取一行就好」是本題最該學到的偷懶技巧。

### 是非 · Lay 2.8 Exercises 25–26、28
(25) **(T/F)** The set of all solutions of a system of $m$ homogeneous equations in $n$ unknowns is a subspace of $\mathbb{R}^m$.

(26) **(T/F)** The null space of an $m \times n$ matrix is a subspace of $\mathbb{R}^n$.

(28) **(T/F)** The column space of a matrix $A$ is the set of solutions of $A\mathbf{x} = \mathbf{b}$.

#### 解答
- (25) **False.** 解向量有 $n$ 個分量,所以是 $\mathbb{R}^n$(不是 $\mathbb{R}^m$)的子空間。
- (26) **True.** 這就是 Theorem 12。
- (28) **False.** $\operatorname{Col} A$ 裝的是**所有使 $A\mathbf{x} = \mathbf{b}$ 有解的 $\mathbf{b}$**,不是解 $\mathbf{x}$ 的集合。$A\mathbf{x} = \mathbf{b}$ 的解集是 $\operatorname{Nul} A$ 的平移(第 3 週);只有齊次時才恰好是 $\operatorname{Nul} A$。

#### 備註
(25) 與 (26) 是刻意設計的對照題:一個把 $m$、$n$ 寫反,一個寫對。建議並排出在考卷上。

書後對 Exercises 21–29 不給答案,上面的答案是本講義判定的。

### 變化 · Lay 2.8 Exercises 39–42
In Exercises 39–44, respond as comprehensively as possible, and justify your answer.

(39) Suppose $F$ is a $5 \times 5$ matrix whose column space is not equal to $\mathbb{R}^5$. What can you say about $\operatorname{Nul} F$?

(40) If $R$ is a $6 \times 6$ matrix and $\operatorname{Nul} R$ is *not* the zero subspace, what can you say about $\operatorname{Col} R$?

(41) If $Q$ is a $4 \times 4$ matrix and $\operatorname{Col} Q = \mathbb{R}^4$, what can you say about solutions of equations of the form $Q\mathbf{x} = \mathbf{b}$ for $\mathbf{b}$ in $\mathbb{R}^4$?

(42) If $P$ is a $5 \times 5$ matrix and $\operatorname{Nul} P$ is the zero subspace, what can you say about solutions of equations of the form $P\mathbf{x} = \mathbf{b}$ for $\mathbf{b}$ in $\mathbb{R}^5$?

#### 解答
- (39) 各行不張成 $\mathbb{R}^5$ ⇒ IMT 的 (h) 不成立 ⇒ $F$ 不可逆 ⇒ (d) 不成立 ⇒ $F\mathbf{x} = \mathbf{0}$ 有非平凡解,即 $\operatorname{Nul} F$ 含非零向量,$\operatorname{Nul} F \ne \{\mathbf{0}\}$。
- (40) $\operatorname{Nul} R \ne \{\mathbf{0}\}$ ⇒ (d) 不成立 ⇒ $R$ 不可逆 ⇒ (h) 不成立,各行不張成 $\mathbb{R}^6$,即 $\operatorname{Col} R \ne \mathbb{R}^6$(是 $\mathbb{R}^6$ 的**真**子空間),而且存在 $\mathbf{b}$ 使 $R\mathbf{x} = \mathbf{b}$ 無解。
- (41) $\operatorname{Col} Q = \mathbb{R}^4$ ⇒ (h) 成立 ⇒ $Q$ 可逆 ⇒ 由 (g) 每個 $\mathbf{b}$ 都有解,再由第 5 週 Theorem 5,解**唯一**($\mathbf{x} = Q^{-1}\mathbf{b}$)。
- (42) $\operatorname{Nul} P = \{\mathbf{0}\}$ ⇒ (d) 成立 ⇒ $P$ 可逆 ⇒ 每個 $\mathbf{b}$ 都**恰有一個解** $\mathbf{x} = P^{-1}\mathbf{b}$。

#### 備註
這四題全部是**方陣**,所以能用 IMT;(39)(40) 互為逆敘述,(41)(42) 也是。四題的答題格式完全一樣,適合當堂練手。

題目說「respond as comprehensively as possible」,所以 (41)(42) 只寫「有解」不夠,要寫到「唯一」。

### 變化 · Lay 2.8 Exercises 43–44 與 Practice Problems 2–3
(43) What can you say about $\operatorname{Nul} B$ when $B$ is a $5 \times 4$ matrix with linearly independent columns?

(44) What can you say about the shape of an $m \times n$ matrix $A$ when the columns of $A$ form a basis for $\mathbb{R}^m$?

(Practice Problem 2) Given $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$, find a vector in $\operatorname{Nul} A$ and a vector in $\operatorname{Col} A$.

(Practice Problem 3) Suppose an $n \times n$ matrix $A$ is invertible. What can you say about $\operatorname{Col} A$? About $\operatorname{Nul} A$?

#### 解答
(43) 各行線性獨立 ⇒ $B\mathbf{x} = \mathbf{0}$ 只有平凡解 ⇒ $\operatorname{Nul} B = \{\mathbf{0}\}$($\mathbb{R}^4$ 的零子空間)。

**注意 $B$ 不是方陣,不能用 IMT**;這裡用的是「線性獨立 ⇔ 齊次方程只有平凡解」,那對任何矩陣都成立。

(44) 各行張成 $\mathbb{R}^m$ ⇒ 每一列都有樞軸 ⇒ 樞軸數 $= m$;各行線性獨立 ⇒ 每一行都是樞軸行 ⇒ 樞軸數 $= n$。兩者相等,得 $m = n$:$A$ 是**方陣**,而且由 IMT 它**可逆**。

(PP2) $A$ 已是最簡列梯形,$A\mathbf{x} = \mathbf{0}$ 給出 $x_2 = x_3 = 0$、$x_1$ 自由,所以 $\operatorname{Nul} A$ 的一個非零向量是 $(1, 0, 0)$。$\operatorname{Col} A$ 隨便取一行,例如第 2 行 $(1, 0, 0)$。

**這個例子裡同一個 $(1,0,0)$ 同時落在兩個空間裡**——書後解答特別指出,一般的 $n \times n$ 矩陣只有零向量會同時在兩者中。

(PP3) $A$ 可逆 ⇒ 由 IMT,各行張成 $\mathbb{R}^n$,所以 $\operatorname{Col} A = \mathbb{R}^n$;又 $A\mathbf{x} = \mathbf{0}$ 只有平凡解,所以 $\operatorname{Nul} A = \{\mathbf{0}\}$。

#### 備註
(43) 是本組唯一的**非方陣**題,刻意放在方陣題之後,考學生會不會亂用 IMT。

PP3 的兩個結論就是下下個觀念要加進 IMT 的條款 (n) 與 (q),可以先預告。

## 驗算
```check
(lambda a, u: (a * u).is_zero_matrix and a.rank() < a.row_join(u).rank())(Matrix([[1, -1, 5], [2, 0, 7], [-3, -5, -3]]), Matrix([-7, 3, 2]))
Matrix([[1, -1, 5, -7], [2, 0, 7, 3], [-3, -5, -3, 2]]).rref()[1] == (0, 1, 3)
(lambda a, b: a.rank() < a.row_join(b).rank())(Matrix([[2, -4], [3, -5], [-5, 8]]), Matrix([8, 2, -9]))
(lambda a, b: a.rank() < a.row_join(b).rank())(Matrix([[1, 4, 5], [-2, -7, -8], [4, 9, 6], [3, 7, 5]]), Matrix([-4, 10, -7, -5]))
(lambda a, b: a.rank() == a.row_join(b).rank())(Matrix([[2, -3, -4], [-8, 8, 6], [6, -7, -7]]), Matrix([6, -10, 11]))
Matrix([[2, -3, -4], [-8, 8, 6], [6, -7, -7]]) * Matrix([Rational(-9,4), Rational(-7,2), 0]) == Matrix([6, -10, 11])
Matrix([[-3, -2, 0], [0, 2, -6], [6, 3, 3]]) * Matrix([-5, 7, 0]) == Matrix([1, 14, -9])
not (Matrix([[2, -3, -4], [-8, 8, 6], [6, -7, -7]]) * Matrix([6, -10, 11])).is_zero_matrix
(Matrix([[-3, -2, 0], [0, 2, -6], [6, 3, 3]]) * Matrix([-2, 3, 1])).is_zero_matrix
(lambda a: (a.cols, a.rows) == (4, 3))(Matrix([[3, 2, 1, -5], [-9, -4, 1, 7], [9, 2, -5, 1]]))
(lambda a: (a.cols, a.rows) == (3, 4))(Matrix([[1, 2, 3], [4, 5, 7], [-5, -1, 0], [2, 7, 11]]))
(Matrix([[3, 2, 1, -5], [-9, -4, 1, 7], [9, 2, -5, 1]]) * Matrix([1, -2, 1, 0])).is_zero_matrix
(Matrix([[3, 2, 1, -5], [-9, -4, 1, 7], [9, 2, -5, 1]]) * Matrix([-1, 4, 0, 1])).is_zero_matrix
(Matrix([[1, 2, 3], [4, 5, 7], [-5, -1, 0], [2, 7, 11]]) * Matrix([1, -5, 3])).is_zero_matrix
(lambda a: a.nullspace() == [Matrix([1, 0, 0])] and a.col(1) == Matrix([1, 0, 0]))(Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]]))
(lambda a: a.rank() == 3 and a.nullspace() == [])(Matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]]))
(lambda b: b.rank() == b.cols and b.nullspace() == [])(Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]))
(lambda a, u, v: (a * (u + v)).is_zero_matrix and (a * (3 * u)).is_zero_matrix)(Matrix([[3, 2, 1, -5], [-9, -4, 1, 7], [9, 2, -5, 1]]), Matrix([1, -2, 1, 0]), Matrix([-1, 4, 0, 1]))
(lambda a, b: a.rank() == a.row_join(b).rank())(Matrix([[1, -3, -4], [-4, 6, -2], [-3, 7, 6]]), Matrix([3, 3, -4]))
(lambda a: a.rank() == 1 and (a * Matrix([-2, 1, 0])).is_zero_matrix and (a * Matrix([1, 0, 1])).is_zero_matrix and not (a * Matrix([2, -1, 3])).is_zero_matrix)(Matrix([[2, 4, -2], [-1, -2, 1], [3, 6, -3]]))
```
