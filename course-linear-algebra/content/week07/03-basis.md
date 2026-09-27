---
title_en: Bases for Nul A and Col A
title_zh: 基底:剛剛好的一組生成元
sub: Independent and spanning — no more, no less
level: hard
source: Lay 2.8
lab_hook: '`A.columnspace()` 回傳的是 **A 自己的**樞軸行,不是階梯形的行'
---
## 觀念
**Definition.** A **basis** for a subspace $H$ of $\mathbb{R}^n$ is a linearly independent set in $H$ that spans $H$.

**Theorem 13.** The pivot columns of a matrix $A$ form a basis for the column space of $A$.

> ***Warning:*** Be careful to use *pivot columns of $A$ itself* for the basis of $\operatorname{Col} A$. The columns of an echelon form $B$ are often not in the column space of $A$.

For $\operatorname{Nul} A$ there is no theorem to quote — the method is the one from Section 1.5: write the solution of $A\mathbf{x} = \mathbf{0}$ in parametric vector form. The vectors that appear in that form are automatically a basis for $\operatorname{Nul} A$.

The columns of an invertible $n \times n$ matrix form a basis for all of $\mathbb{R}^n$ because they are linearly independent and they span $\mathbb{R}^n$, by the Invertible Matrix Theorem. One such matrix is the identity matrix; its columns $\mathbf{e}_1, \dots, \mathbf{e}_n$ are called the **standard basis** for $\mathbb{R}^n$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| basis | 基底 | 既線性獨立、又張成整個子空間的一組向量 |
| standard basis | 標準基底 | $\{\mathbf{e}_1, \dots, \mathbf{e}_n\}$,單位矩陣的各行 |
| pivot column | 樞軸行 | 階梯形裡有樞軸的那幾行(位置由階梯形決定) |
| echelon form $B$ | 階梯形 $B$ | 化簡後的樣子;**它的行不是 $\operatorname{Col} A$ 的成員** |
| parametric vector form | 參數向量形式 | 第 3 週寫解集的方式 |
| spanning set | 生成集 | 張得出整個空間,但可能有多餘的 |

## 白話說
**基底 = 剛剛好的一組生成元:少一個就張不滿,多一個就有多餘。**

它同時要滿足兩件事:

| 條件 | 意思 | 少了會怎樣 |
|---|---|---|
| **張成** $H$ | $H$ 裡的每個向量都組得出來 | 張不滿,有些東西做不到 |
| **線性獨立** | 沒有多餘的向量 | 有重複,同一個向量有很多種寫法 |

**求 $\operatorname{Col} A$ 的基底**:列化簡找出樞軸在哪幾行,然後回去取 **$A$ 自己**的那幾行。

> ⚠️ **本節最大的陷阱**:取的是 **$A$ 的**樞軸行,**不是階梯形 $B$ 的行**。
>
> 為什麼?因為列運算**會改變行本身**。$B$ 的行通常根本不在 $\operatorname{Col} A$ 裡(例如 $B$ 的行末尾常常是 0,而 $A$ 的行不是)。
>
> 但列運算**不改變行之間的相依關係**,所以「哪幾行是樞軸行」這個資訊可以從 $B$ 讀出來,**再回去 $A$ 拿**。

**求 $\operatorname{Nul} A$ 的基底**:解 $A\mathbf{x} = \mathbf{0}$,寫成參數向量形式(第 3 週學過),每個自由變數對應一個基底向量。這樣得到的向量**自動線性獨立**——因為每個向量在「自己那個自由變數」的位置是 1、其他基底向量在那個位置是 0。

**兩種基底的對照:**

| | $\operatorname{Col} A$ 的基底 | $\operatorname{Nul} A$ 的基底 |
|---|---|---|
| 怎麼求 | 列化簡 → 找樞軸行 → **取 $A$ 的那幾行** | 解 $A\mathbf{x} = \mathbf{0}$ → 寫成參數向量形式 |
| 有幾個 | 樞軸行的個數 | 自由變數的個數 |
| 向量長度 | $m$(列數) | $n$(行數) |

## 在資工哪裡用
- **基底 = 最省的表示法**。存一個子空間不必存裡面所有向量(有無限多個),只要存一組基底。影像壓縮、字典學習、嵌入向量都在做這件事。
- **「取 $A$ 的行而不是 $B$ 的行」這件事在程式上也一樣**:`A.columnspace()` 回傳的是原矩陣的樞軸行。若自己寫程式,化簡完千萬要記得用原始行的索引回去取。
- **零空間的基底 = 系統的「自由度」**。機械手臂的冗餘自由度、方程組的參數解、碼字的所有可能,都是零空間的基底張出來的。
- **標準基底不一定最好用**。第 13 週的正交基底、第 16 週的 SVD 基底,都是為了某個目的挑出來的「更好的基底」。

## 原理
**為什麼樞軸行構成 $\operatorname{Col} A$ 的基底?**(Theorem 13,課本 p. 183)

兩件事要驗:樞軸行**線性獨立**、而且**張成** $\operatorname{Col} A$。

1. **列運算不改變行之間的相依關係。** 因為 $A\mathbf{x} = \mathbf{0}$ 與 $B\mathbf{x} = \mathbf{0}$($B$ 是 $A$ 的列等價矩陣)有**完全相同的解集**,而一組行的線性關係正是由這些解描述的(第 3 週)。
2. **$B$ 的樞軸行線性獨立**(階梯形的樞軸行長得像「階梯」,一眼可見),所以 **$A$ 的樞軸行也線性獨立**。
3. **$B$ 的非樞軸行都是它左邊那些樞軸行的線性組合**,所以 **$A$ 的非樞軸行也是 $A$ 的樞軸行的同樣組合**(同樣的係數!)。
4. 因此 $A$ 的每一行都可以由樞軸行組出來 ⇒ 樞軸行張成 $\operatorname{Col} A$。

兩條都有了,所以樞軸行是基底。$\blacksquare$

**第 3 步是這個定理最有用的地方**:非樞軸行怎麼由樞軸行組出來,**係數可以直接從最簡列梯形讀出來**。

**為什麼不能用 $B$ 的行?** 因為 (1) 只保證「相依關係一樣」,不保證「行本身一樣」。舉個具體例子:

$$A = \begin{bmatrix} 1 & 2 \\ 1 & 2 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 \\ 0 & 0 \end{bmatrix} = B$$

$\operatorname{Col} A$ 是 $(1,1)$ 張出的直線,但 $B$ 的第一行 $(1,0)$ **根本不在那條線上**。

**為什麼參數向量形式給出的向量自動獨立?** 設自由變數是 $x_3, x_5$,寫出來的基底向量是 $\mathbf{u}$(對應 $x_3$)與 $\mathbf{v}$(對應 $x_5$)。$\mathbf{u}$ 的第 3 格是 1、第 5 格是 0;$\mathbf{v}$ 的第 3 格是 0、第 5 格是 1。若 $c_1\mathbf{u} + c_2\mathbf{v} = \mathbf{0}$,看第 3 格得 $c_1 = 0$、看第 5 格得 $c_2 = 0$。所以線性獨立。

## 老師講解
### 例 1 · Lay 2.8 Example 6
Find a basis for $\operatorname{Nul} A$, where

$$A = \begin{bmatrix} -3 & 6 & -1 & 1 & -7 \\ 1 & -2 & 2 & 3 & -1 \\ 2 & -4 & 5 & 8 & -4 \end{bmatrix}$$

1. **要找零空間的基底,就是解 $A\mathbf{x} = \mathbf{0}$**,沒有別的路。
2. **列化簡到最簡列梯形**:
   $$[\,A \;\; \mathbf{0}\,] \sim \begin{bmatrix} 1 & -2 & 0 & -1 & 3 & 0 \\ 0 & 0 & 1 & 2 & -2 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$$
3. **讀出自由變數**:樞軸在第 1、3 行,所以 $x_2, x_4, x_5$ 是自由變數(**三個**)。
4. **把基本變數用自由變數表示**:$x_1 = 2x_2 + x_4 - 3x_5$、$x_3 = -2x_4 + 2x_5$。
5. **寫成參數向量形式**(第 3 週的技巧):
   $$\mathbf{x} = x_2\begin{bmatrix} 2 \\ 1 \\ 0 \\ 0 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} 1 \\ 0 \\ -2 \\ 1 \\ 0 \end{bmatrix} + x_5\begin{bmatrix} -3 \\ 0 \\ 2 \\ 0 \\ 1 \end{bmatrix}$$
6. **這三個向量就是基底**。張成:任何解都寫得成它們的組合(上式就是)。獨立:看第 2、4、5 格的「1 和 0」的位置就知道。
7. **檢查個數**:3 個自由變數 → 3 個基底向量。而樞軸有 2 個,$2 + 3 = 5 = $ 行數——這個巧合不是巧合,是下下個觀念的 Rank Theorem。

### 例 2 · Lay 2.8 Exercise 31
The matrix $A$ and an echelon form of $A$ are shown. Find a basis for $\operatorname{Col} A$ and a basis for $\operatorname{Nul} A$.

$$A = \begin{bmatrix} 4 & 5 & 9 & -2 \\ 6 & 5 & 1 & 12 \\ 3 & 4 & 8 & -3 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 & 6 & -5 \\ 0 & 1 & 5 & -6 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

1. **先從階梯形讀出樞軸在哪**:第 1、2 行。(只讀位置,不讀數值!)
2. **回去取 $A$ 自己的第 1、2 行**:
   $$\operatorname{Col} A \text{ 的基底} = \left\{\begin{bmatrix} 4 \\ 6 \\ 3 \end{bmatrix}, \begin{bmatrix} 5 \\ 5 \\ 4 \end{bmatrix}\right\}$$
3. **絕對不要寫成 $(1,0,0)$ 與 $(2,1,0)$**(那是階梯形的行)。用那兩個向量組不出 $A$ 的任何一行——它們的第三格都是 0,而 $A$ 的行不是。
4. **再求 $\operatorname{Nul} A$**:把 $A$ 化到**最簡**列梯形
   $$A \sim \begin{bmatrix} 1 & 0 & -4 & 7 \\ 0 & 1 & 5 & -6 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
5. **自由變數是 $x_3, x_4$**,基本變數 $x_1 = 4x_3 - 7x_4$、$x_2 = -5x_3 + 6x_4$。
6. **寫成參數向量形式**:
   $$\operatorname{Nul} A \text{ 的基底} = \left\{\begin{bmatrix} 4 \\ -5 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} -7 \\ 6 \\ 0 \\ 1 \end{bmatrix}\right\}$$
7. **驗算**:$A$ 乘這兩個向量都要得到 $\mathbf{0}$;而且 $2 + 2 = 4 = $ 行數 ✓。
8. **注意兩組基底的向量長度不同**:$\operatorname{Col} A$ 的是 3 維($A$ 有 3 列)、$\operatorname{Nul} A$ 的是 4 維($A$ 有 4 行)。

### 例 3 · Lay 2.8 Exercises 15、19 與 Example 5
Determine which sets are bases for $\mathbb{R}^2$ or $\mathbb{R}^3$: (a) $\begin{bmatrix} 5 \\ -2 \end{bmatrix}, \begin{bmatrix} 10 \\ -3 \end{bmatrix}$; (b) $\begin{bmatrix} 3 \\ -8 \\ 1 \end{bmatrix}, \begin{bmatrix} 6 \\ 2 \\ -5 \end{bmatrix}$.

1. **要判斷「是不是 $\mathbb{R}^n$ 的基底」,最快的路是可逆矩陣定理**(上週學的)。
2. **(a) 兩個 $\mathbb{R}^2$ 的向量**,湊成方陣:
   $$A = \begin{bmatrix} 5 & 10 \\ -2 & -3 \end{bmatrix}, \qquad \det A = -15 + 20 = 5 \ne 0$$
3. **$A$ 可逆** ⇒ 由 IMT,各行線性獨立((e))且張成 $\mathbb{R}^2$((h))⇒ **是基底**。
4. **(b) 只有兩個 $\mathbb{R}^3$ 的向量**,湊成的是 $3 \times 2$ 矩陣——**不是方陣,不能用 IMT**。
5. **用樞軸數論證**:$3 \times 2$ 矩陣最多 2 個樞軸,不可能每一列都有樞軸,所以各行**張不成** $\mathbb{R}^3$。⇒ **不是 $\mathbb{R}^3$ 的基底**。
6. **但它們是什麼?** 這兩個向量線性獨立,所以它們是 $\mathbb{R}^3$ 裡**某個平面**的基底——書後解答特別加了這一句。
7. **數量的通則**(先預告下下個觀念):$\mathbb{R}^n$ 的基底**恰好**要 $n$ 個向量。**少了張不滿、多了必相依**(Exercise 20 就是 4 個向量在 $\mathbb{R}^3$,必定相依)。

#### 備註
例 3 的第 7 點是 Basis Theorem 的雛形,這裡先當「數量檢查」用:看到 $\mathbb{R}^3$ 裡有 2 個或 4 個向量,不必計算就能判斷「不是基底」。

## 易錯點
- **拿階梯形 $B$ 的行當 $\operatorname{Col} A$ 的基底**。這是本節第一名的錯誤,課本專門加了 Warning。
- **求 $\operatorname{Nul} A$ 的基底時忘了化到「最簡」列梯形**。只化到階梯形會很難讀出基本變數。
- **把兩組基底的向量長度搞混**:$\operatorname{Col}$ 的長度 = 列數,$\operatorname{Nul}$ 的長度 = 行數。
- **用 IMT 判斷非方陣的基底**(例 3 的 (b))。向量個數 ≠ 空間維度時,IMT 不適用。
- **以為基底唯一**。同一個子空間有無限多組基底;$\operatorname{Nul} A$ 的基底向量乘個非零倍數還是基底。
- 忘記驗算:$A$ 乘零空間基底向量必須得 $\mathbf{0}$。

## 教學提示
這個觀念 25 分鐘,**Warning 要用板書強調**。建議這樣做:先寫出一個 $A$ 與它的階梯形 $B$,問「$\operatorname{Col} A$ 的基底怎麼取?」——多數學生會直覺答「取 $B$ 的樞軸行」,這時再用

$$A = \begin{bmatrix} 1 & 2 \\ 1 & 2 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 \\ 0 & 0 \end{bmatrix}$$

這個極小的反例打臉:$(1,0)$ 根本不在 $\operatorname{Col} A$ 那條線上。**撞過一次牆,學生就不會忘。**

$\operatorname{Nul} A$ 的基底其實是第 3 週的舊技巧(參數向量形式),可以快轉,重點放在「自由變數的個數 = 基底向量的個數」。

課堂建議做:Exercise 31(一次做兩種基底,最有代表性);Exercises 15、19(是不是 $\mathbb{R}^n$ 的基底);是非 Exercise 30(Warning 的直接考法)。Exercises 32–34 當作業。

T 題 Exercises 45–46 放進實作課——尤其 46 的零空間基底數字很大(三位數),正好示範「這種題目就是要用電腦」。

## 練習
### 照做 · Lay 2.8 Exercises 15–20
Determine which sets in Exercises 15–20 are bases for $\mathbb{R}^2$ or $\mathbb{R}^3$. Justify each answer.

(15) $\begin{bmatrix} 5 \\ -2 \end{bmatrix}$, $\begin{bmatrix} 10 \\ -3 \end{bmatrix}$

(16) $\begin{bmatrix} -4 \\ 6 \end{bmatrix}$, $\begin{bmatrix} 2 \\ -3 \end{bmatrix}$

(17) $\begin{bmatrix} 0 \\ 1 \\ -2 \end{bmatrix}$, $\begin{bmatrix} 5 \\ -7 \\ 4 \end{bmatrix}$, $\begin{bmatrix} 6 \\ 3 \\ 5 \end{bmatrix}$

(18) $\begin{bmatrix} 1 \\ 1 \\ -2 \end{bmatrix}$, $\begin{bmatrix} -5 \\ -1 \\ 2 \end{bmatrix}$, $\begin{bmatrix} 7 \\ 0 \\ -5 \end{bmatrix}$

(19) $\begin{bmatrix} 3 \\ -8 \\ 1 \end{bmatrix}$, $\begin{bmatrix} 6 \\ 2 \\ -5 \end{bmatrix}$

(20) $\begin{bmatrix} 1 \\ -6 \\ -7 \end{bmatrix}$, $\begin{bmatrix} 3 \\ -4 \\ 7 \end{bmatrix}$, $\begin{bmatrix} -2 \\ 7 \\ 5 \end{bmatrix}$, $\begin{bmatrix} 0 \\ 8 \\ 9 \end{bmatrix}$

#### 解答
- (15) **是** $\mathbb{R}^2$ 的基底。$\det\begin{bmatrix} 5 & 10 \\ -2 & -3 \end{bmatrix} = 5 \ne 0$ ⇒ 可逆 ⇒ 由 IMT,各行獨立且張成 $\mathbb{R}^2$。
- (16) **不是。** $\begin{bmatrix} -4 \\ 6 \end{bmatrix} = -2\begin{bmatrix} 2 \\ -3 \end{bmatrix}$,兩向量相依($\det = 0$),只張出一條直線。
- (17) **是** $\mathbb{R}^3$ 的基底。列化簡有 3 個樞軸($\det = -115 \ne 0$)⇒ 可逆 ⇒ IMT。
- (18) **是** $\mathbb{R}^3$ 的基底。$\det = -20 \ne 0$。
- (19) **不是。** 只有 2 個向量,對應 $3 \times 2$ 矩陣最多 2 個樞軸,不可能每一列都有樞軸 ⇒ 張不成 $\mathbb{R}^3$。(這兩個向量獨立,是 $\mathbb{R}^3$ 中某個**平面**的基底。)
- (20) **不是。** $\mathbb{R}^3$ 裡任 4 個向量必定線性相依($4 > 3$)。(它們確實張成 $\mathbb{R}^3$,但因為相依,不是基底。)

#### 備註
(19)(20) 是**數量檢查**:$\mathbb{R}^n$ 的基底恰好要 $n$ 個向量,少了張不滿、多了必相依。這兩題**不必計算**就能答,要讓學生看出這一點。

(15)(17)(18) 的書後解答都特別提到「Let $A$ be the matrix whose columns are the vectors given」——把向量排成矩陣再用 IMT,是本組題目的標準寫法。

### 是非 · Lay 2.8 Exercises 27、29–30
(27) **(T/F)** The columns of an invertible $n \times n$ matrix form a basis for $\mathbb{R}^n$.

(29) **(T/F)** Row operations do not affect linear dependence relations among the columns of a matrix.

(30) **(T/F)** If $B$ is an echelon form of a matrix $A$, then the pivot columns of $B$ form a basis for $\operatorname{Col} A$.

#### 解答
- (27) **True.** 由 IMT,可逆矩陣的各行線性獨立((e))且張成 $\mathbb{R}^n$((h)),兩條合起來就是基底的定義。
- (29) **True.** $A\mathbf{x} = \mathbf{0}$ 與 $B\mathbf{x} = \mathbf{0}$ 解集相同,而行之間的線性關係正是由這些解描述的,所以完全一樣。
- (30) **False.** 必須取 **$A$ 自己**的樞軸行(Theorem 13 後的 Warning)。$B$ 的行通常不在 $\operatorname{Col} A$ 裡。

#### 備註
(29) 與 (30) 必須連著看:列運算**保留相依關係**(所以可以從 $B$ 讀出「哪幾行是樞軸行」),但**改變行本身**(所以要回 $A$ 取)。這兩句話是 Theorem 13 的全部內容。

(30) 是本節最常見的陷阱題,幾乎每年必考。

### 變化 · Lay 2.8 Exercises 31–34
Exercises 31–34 display a matrix $A$ and an echelon form of $A$. Find a basis for $\operatorname{Col} A$ and a basis for $\operatorname{Nul} A$.

(31) $A = \begin{bmatrix} 4 & 5 & 9 & -2 \\ 6 & 5 & 1 & 12 \\ 3 & 4 & 8 & -3 \end{bmatrix} \sim \begin{bmatrix} 1 & 2 & 6 & -5 \\ 0 & 1 & 5 & -6 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

(32) $A = \begin{bmatrix} -3 & 9 & -2 & -7 \\ 2 & -6 & 4 & 8 \\ 3 & -9 & -2 & 2 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 6 & 9 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

(33) $A = \begin{bmatrix} 1 & 4 & 8 & -3 & -7 \\ -1 & 2 & 7 & 3 & 4 \\ -2 & 2 & 9 & 5 & 5 \\ 3 & 6 & 9 & -5 & -2 \end{bmatrix} \sim \begin{bmatrix} 1 & 4 & 8 & 0 & 5 \\ 0 & 2 & 5 & 0 & -1 \\ 0 & 0 & 0 & 1 & 4 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

(34) $A = \begin{bmatrix} 3 & -1 & 7 & 3 & 9 \\ -2 & 2 & -2 & 7 & 5 \\ -5 & 9 & 3 & 3 & 4 \\ -2 & 6 & 6 & 3 & 7 \end{bmatrix} \sim \begin{bmatrix} 3 & -1 & 7 & 0 & 6 \\ 0 & 2 & 4 & 0 & 3 \\ 0 & 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

#### 解答
(31) 樞軸在第 1、2 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 4 \\ 6 \\ 3 \end{bmatrix}, \begin{bmatrix} 5 \\ 5 \\ 4 \end{bmatrix}\right\}, \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} 4 \\ -5 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} -7 \\ 6 \\ 0 \\ 1 \end{bmatrix}\right\}$$

(32) 樞軸在第 1、3 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} -3 \\ 2 \\ 3 \end{bmatrix}, \begin{bmatrix} -2 \\ 4 \\ -2 \end{bmatrix}\right\}, \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} 3 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} -6 \\ 0 \\ -5 \\ 4 \end{bmatrix}\right\}$$
(第二個向量已乘 4 去分母;原始形式是 $(-3/2, 0, -5/4, 1)$。)

(33) 樞軸在第 1、2、4 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 1 \\ -1 \\ -2 \\ 3 \end{bmatrix}, \begin{bmatrix} 4 \\ 2 \\ 2 \\ 6 \end{bmatrix}, \begin{bmatrix} -3 \\ 3 \\ 5 \\ -5 \end{bmatrix}\right\}, \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} 2 \\ -5/2 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} -7 \\ 1/2 \\ 0 \\ -4 \\ 1 \end{bmatrix}\right\}$$

(34) 樞軸在第 1、2、4 行。
$$\operatorname{Col} A: \left\{\begin{bmatrix} 3 \\ -2 \\ -5 \\ -2 \end{bmatrix}, \begin{bmatrix} -1 \\ 2 \\ 9 \\ 6 \end{bmatrix}, \begin{bmatrix} 3 \\ 7 \\ 3 \\ 3 \end{bmatrix}\right\}, \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} -3 \\ -2 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} -5/2 \\ -3/2 \\ 0 \\ -1 \\ 1 \end{bmatrix}\right\}$$

#### 備註
四題的流程完全一樣:**從階梯形讀樞軸位置 → 回 $A$ 取行 → 把 $A$ 化到最簡列梯形求零空間**。批改時最該看的是 $\operatorname{Col} A$ 的基底有沒有誤用階梯形的行。

零空間基底**不唯一**:(32) 的第二個向量保留分數 $(-3/2, 0, -5/4, 1)$ 也完全正確;(33) 書上寫小數 $-2.5$、$.5$。

(34) 給的階梯形第一列首項是 3(不是最簡列梯形),但樞軸**位置**一樣——這正是「只讀位置、不讀數值」的好例子。

### 變化 · Lay 2.8 Exercise 38
Suppose the columns of a matrix $A = [\,\mathbf{a}_1 \;\cdots\; \mathbf{a}_p\,]$ are linearly independent. Explain why $\{\mathbf{a}_1, \dots, \mathbf{a}_p\}$ is a basis for $\operatorname{Col} A$.

#### 解答
依定義,$\operatorname{Col} A$ 是 $A$ 各行所有線性組合的集合,也就是
$$\operatorname{Col} A = \operatorname{Span}\{\mathbf{a}_1, \dots, \mathbf{a}_p\}$$
所以這組行**張成** $\operatorname{Col} A$;而題目已假設它們**線性獨立**。基底的定義就是「線性獨立 + 張成」,兩條都滿足,故 $\{\mathbf{a}_1, \dots, \mathbf{a}_p\}$ 是 $\operatorname{Col} A$ 的基底。$\blacksquare$

#### 備註
也可以走 Theorem 13:各行線性獨立 ⇒ 每一行都是樞軸行 ⇒ 全部的行構成 $\operatorname{Col} A$ 的基底。兩種寫法都對,前者更直接。

這題雖短,但它示範了「回到定義」這個最基本的證明方式。

### 應用 · Lay 2.8 Exercises 45–46(T 電腦題)
In Exercises 45 and 46, construct bases for the column space and the null space of the given matrix $A$. Justify your work.

(45) $A = \begin{bmatrix} 3 & -5 & 0 & -1 & 3 \\ -7 & 9 & -4 & 9 & -11 \\ -5 & 7 & -2 & 5 & -7 \\ 3 & -7 & -3 & 4 & 0 \end{bmatrix}$

(46) $A = \begin{bmatrix} 5 & 2 & 0 & -8 & -8 \\ 4 & 1 & 2 & -8 & -9 \\ 5 & 1 & 3 & 5 & 19 \\ -8 & -5 & 6 & 8 & 5 \end{bmatrix}$

#### 解答
(45) 最簡列梯形的樞軸在第 1、2 行,所以
$$\operatorname{Col} A: \left\{\begin{bmatrix} 3 \\ -7 \\ -5 \\ 3 \end{bmatrix}, \begin{bmatrix} -5 \\ 9 \\ 7 \\ -7 \end{bmatrix}\right\}$$
自由變數是 $x_3, x_4, x_5$,
$$\operatorname{Nul} A: \left\{\begin{bmatrix} -2.5 \\ -1.5 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 4.5 \\ 2.5 \\ 0 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} -3.5 \\ -1.5 \\ 0 \\ 0 \\ 1 \end{bmatrix}\right\}$$
$\operatorname{rank} A = 2$、$\dim \operatorname{Nul} A = 3$,$2 + 3 = 5$ = 行數。

(46) 樞軸在第 1、2、3 行,
$$\operatorname{Col} A: \left\{\begin{bmatrix} 5 \\ 4 \\ 5 \\ -8 \end{bmatrix}, \begin{bmatrix} 2 \\ 1 \\ 1 \\ -5 \end{bmatrix}, \begin{bmatrix} 0 \\ 2 \\ 3 \\ 6 \end{bmatrix}\right\}, \qquad \operatorname{Nul} A: \left\{\begin{bmatrix} -60 \\ 154 \\ 47 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} -122 \\ 309 \\ 94 \\ 0 \\ 1 \end{bmatrix}\right\}$$
$\operatorname{rank} A = 3$、$\dim \operatorname{Nul} A = 2$。

#### 備註
兩題都標 T,放進實作課。書後對 (45) 給的是做法而非只給答案:「Display the reduced echelon form of $A$, and select the pivot columns of $A$ as a basis for $\operatorname{Col} A$. For $\operatorname{Nul} A$, write the solution of $A\mathbf{x} = \mathbf{0}$ in parametric vector form.」

(46) 的零空間基底出現三位數(154、309),**手算幾乎一定會錯**——這正是它被標成電腦題的原因。實作課會用 `A.nullspace()` 算,並代回驗證。

## 驗算
```check
(lambda a: a.rref()[1] == (0, 2) and a.nullspace() == [Matrix([2, 1, 0, 0, 0]), Matrix([1, 0, -2, 1, 0]), Matrix([-3, 0, 2, 0, 1])])(Matrix([[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]]))
(lambda a, b, c: (a * b).is_zero_matrix and b.rank() == b.cols == a.cols - a.rank() and c.rank() == c.cols == a.rank() and a.row_join(c).rank() == a.rank())(Matrix([[4, 5, 9, -2], [6, 5, 1, 12], [3, 4, 8, -3]]), Matrix([[4, -7], [-5, 6], [1, 0], [0, 1]]), Matrix([[4, 5], [6, 5], [3, 4]]))
Matrix([[1, 2], [1, 2]]).rank() == 1 and Matrix([[1, 2], [1, 2]]).rank() < Matrix([[1, 2], [1, 2]]).row_join(Matrix([1, 0])).rank()
Matrix([[5, 10], [-2, -3]]).det() == 5
Matrix([[-4, 2], [6, -3]]).det() == 0
Matrix([[0, 5, 6], [1, -7, 3], [-2, 4, 5]]).det() == -115
Matrix([[1, -5, 7], [1, -1, 0], [-2, 2, -5]]).det() == -20
Matrix([[3, 6], [-8, 2], [1, -5]]).rank() < 3
Matrix([[1, 3, -2, 0], [-6, -4, 7, 8], [-7, 7, 5, 9]]).rank() < 4
(lambda a, b, c: (a * b).is_zero_matrix and b.rank() == b.cols == a.cols - a.rank() and c.rank() == c.cols == a.rank() and a.row_join(c).rank() == a.rank())(Matrix([[-3, 9, -2, -7], [2, -6, 4, 8], [3, -9, -2, 2]]), Matrix([[3, -6], [1, 0], [0, -5], [0, 4]]), Matrix([[-3, -2], [2, 4], [3, -2]]))
(lambda a, b, c: (a * b).is_zero_matrix and b.rank() == b.cols == a.cols - a.rank() and c.rank() == c.cols == a.rank() and a.row_join(c).rank() == a.rank())(Matrix([[1, 4, 8, -3, -7], [-1, 2, 7, 3, 4], [-2, 2, 9, 5, 5], [3, 6, 9, -5, -2]]), Matrix([[2, -7], [Rational(-5,2), Rational(1,2)], [1, 0], [0, -4], [0, 1]]), Matrix([[1, 4, -3], [-1, 2, 3], [-2, 2, 5], [3, 6, -5]]))
(lambda a, b, c: (a * b).is_zero_matrix and b.rank() == b.cols == a.cols - a.rank() and c.rank() == c.cols == a.rank() and a.row_join(c).rank() == a.rank())(Matrix([[3, -1, 7, 3, 9], [-2, 2, -2, 7, 5], [-5, 9, 3, 3, 4], [-2, 6, 6, 3, 7]]), Matrix([[-3, Rational(-5,2)], [-2, Rational(-3,2)], [1, 0], [0, -1], [0, 1]]), Matrix([[3, -1, 3], [-2, 2, 7], [-5, 9, 3], [-2, 6, 3]]))
(lambda a, b, c: (a * b).is_zero_matrix and b.rank() == b.cols == a.cols - a.rank() and c.rank() == c.cols == a.rank() and a.row_join(c).rank() == a.rank())(Matrix([[3, -5, 0, -1, 3], [-7, 9, -4, 9, -11], [-5, 7, -2, 5, -7], [3, -7, -3, 4, 0]]), Matrix([[Rational(-5,2), Rational(9,2), Rational(-7,2)], [Rational(-3,2), Rational(5,2), Rational(-3,2)], [1, 0, 0], [0, 1, 0], [0, 0, 1]]), Matrix([[3, -5], [-7, 9], [-5, 7], [3, -7]]))
(lambda a, b, c: (a * b).is_zero_matrix and b.rank() == b.cols == a.cols - a.rank() and c.rank() == c.cols == a.rank() and a.row_join(c).rank() == a.rank())(Matrix([[5, 2, 0, -8, -8], [4, 1, 2, -8, -9], [5, 1, 3, 5, 19], [-8, -5, 6, 8, 5]]), Matrix([[-60, -122], [154, 309], [47, 94], [1, 0], [0, 1]]), Matrix([[5, 2, 0], [4, 1, 2], [5, 1, 3], [-8, -5, 6]]))
Matrix([[4, 5, 9, -2], [6, 5, 1, 12], [3, 4, 8, -3]]).columnspace() == [Matrix([4, 6, 3]), Matrix([5, 5, 4])]
```
