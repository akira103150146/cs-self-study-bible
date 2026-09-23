---
title_en: Invertible Linear Transformations
title_zh: 可逆的線性變換:把動作倒回去的那個函數
sub: T is invertible exactly when its standard matrix is
level: mid
source: Lay 2.3
lab_hook: '滑鼠點在螢幕上 → 乘上管線矩陣的反矩陣 → 世界座標'
---
## 觀念
Recall from Section 2.1 that matrix multiplication corresponds to composition of linear transformations. When a matrix $A$ is invertible, the equation $A^{-1}A\mathbf{x} = \mathbf{x}$ can be viewed as a statement about linear transformations.

A linear transformation $T : \mathbb{R}^n \to \mathbb{R}^n$ is said to be **invertible** if there exists a function $S : \mathbb{R}^n \to \mathbb{R}^n$ such that

$$S(T(\mathbf{x})) = \mathbf{x} \quad \text{for all } \mathbf{x} \text{ in } \mathbb{R}^n \tag{1}$$
$$T(S(\mathbf{x})) = \mathbf{x} \quad \text{for all } \mathbf{x} \text{ in } \mathbb{R}^n \tag{2}$$

The next theorem shows that if such an $S$ exists, it is unique and must be a linear transformation. We call $S$ the **inverse** of $T$ and write it as $T^{-1}$.

**Theorem 9.** Let $T : \mathbb{R}^n \to \mathbb{R}^n$ be a linear transformation and let $A$ be the standard matrix for $T$. Then $T$ is invertible if and only if $A$ is an invertible matrix. In that case, the linear transformation $S$ given by $S(\mathbf{x}) = A^{-1}\mathbf{x}$ is the unique function satisfying equations (1) and (2).

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| invertible transformation | 可逆變換 | 存在另一個函數把它倒回去 |
| inverse of $T$ | $T$ 的反變換 | 寫成 $T^{-1}$,就是乘 $A^{-1}$ |
| standard matrix | 標準矩陣 | 第 4 週:$A = [\,T(\mathbf{e}_1) \cdots T(\mathbf{e}_n)\,]$ |
| unique function | 唯一的函數 | 滿足 (1)(2) 的 $S$ 只有一個 |

## 白話說
**一句話:變換可不可逆,完全由它的標準矩陣決定。**

上一個觀念處理的是矩陣,這一個觀念把同樣的話翻譯成「變換」的語言:

| 矩陣的說法 | 變換的說法 |
|---|---|
| $A$ 可逆 | $T$ 可逆 |
| $A^{-1}$ | $T^{-1}$,而且 $T^{-1}(\mathbf{x}) = A^{-1}\mathbf{x}$ |
| (f) 一對一 | 不同輸入給不同輸出 |
| (i) 映成 | 每個目標都到得了 |

**要求兩個方向**:定義要求 $S(T(\mathbf{x})) = \mathbf{x}$ **而且** $T(S(\mathbf{x})) = \mathbf{x}$——先做 $T$ 再做 $S$ 回到原點,先做 $S$ 再做 $T$ 也回到原點。這和第 5 週反矩陣的定義要求 $CA = I$ 且 $AC = I$ 是同一回事。

**為什麼 $S$ 一定唯一?** 因為 $T$ 可逆時是映成的,任何 $\mathbf{v}$ 都寫得成 $T(\mathbf{x})$;而 $S(\mathbf{v}) = S(T(\mathbf{x})) = \mathbf{x}$ 被 $\mathbf{x}$ 決定,沒有選擇的餘地(Exercise 47)。

**為什麼 $S$ 一定是線性的?** 這不是假設,是推出來的(Exercise 48)。也就是說:**倒回去的那個函數,自動也是矩陣乘法**。

## 幾何意義
第 5 週用過「穿鞋脫鞋」的比喻,這裡是同一件事的函數版:$T$ 把每個點搬到新位置,$T^{-1}$ 把它們搬回來。

![課本 2.3 Figure 2:乘 $A$ 把 $\mathbf{x}$ 送到 $A\mathbf{x}$,乘 $A^{-1}$ 再送回來。](inverse-transform.svg)

**什麼時候搬不回來?** 當 $T$ 把兩個不同的點搬到同一個位置(不是一對一),或搬完之後有些位置沒人佔(不是映成)。對方陣而言,這兩件事同時發生——這正是上一個觀念的 IMT。

旋轉、縮放(倍率非 0)、剪切都可逆;**投影不可逆**(壓扁了),$T(\mathbf{x}) = \mathbf{0}$ 也不可逆(全部壓成一點)。

## 在資工哪裡用
- **圖學的逆變換**:滑鼠點在螢幕的某個位置,要知道它對應世界座標的哪裡,就得把整條管線的矩陣求反再乘上去(第 5 週觀念 6 的管線倒著走)。遊戲引擎的 ray picking 就是這件事。
- **可逆 = 可解碼**:編碼是 $T$、解碼是 $T^{-1}$。設計編碼矩陣時,第一件要檢查的就是可逆性。
- **資料前處理的還原**:標準化 $\mathbf{z} = D^{-1}(\mathbf{x} - \boldsymbol{\mu})$ 之後要把預測值換回原單位,用的就是反變換。
- **不可逆代表資訊遺失**:壓縮、投影、量化都是不可逆的變換。第 16 週的 SVD 會量化「遺失了多少」。

## 原理
**Theorem 9 的證明**(課本 p. 147):

($\Rightarrow$)設 $T$ 可逆。由 (2),對任何 $\mathbf{b} \in \mathbb{R}^n$,取 $\mathbf{x} = S(\mathbf{b})$ 就有 $T(\mathbf{x}) = T(S(\mathbf{b})) = \mathbf{b}$,所以每個 $\mathbf{b}$ 都在 $T$ 的值域裡,$T$ 是**映成**的。由 IMT 的 (i),$A$ 可逆。

($\Leftarrow$)設 $A$ 可逆,令 $S(\mathbf{x}) = A^{-1}\mathbf{x}$。$S$ 顯然是線性變換,而且
$$S(T(\mathbf{x})) = S(A\mathbf{x}) = A^{-1}(A\mathbf{x}) = (A^{-1}A)\mathbf{x} = \mathbf{x}$$
同理 $T(S(\mathbf{x})) = \mathbf{x}$。所以 $T$ 可逆。$\blacksquare$

**唯一性**(Exercise 47):設 $S$、$U$ 都滿足 (1)。任給 $\mathbf{v}$,因為 $T$ 映成,可寫 $\mathbf{v} = T(\mathbf{x})$。於是
$$S(\mathbf{v}) = S(T(\mathbf{x})) = \mathbf{x} = U(T(\mathbf{x})) = U(\mathbf{v})$$
對每個 $\mathbf{v}$ 都成立,所以 $S = U$。注意這裡**沒有假設 $S$、$U$ 是線性的**,唯一性照樣成立。

**$S$ 必為線性**(Exercise 48):令 $\mathbf{x} = S(\mathbf{u})$、$\mathbf{y} = S(\mathbf{v})$,由 (2) 得 $T(\mathbf{x}) = \mathbf{u}$、$T(\mathbf{y}) = \mathbf{v}$。用 $T$ 的線性再套 (1):
$$S(\mathbf{u} + \mathbf{v}) = S(T(\mathbf{x}) + T(\mathbf{y})) = S(T(\mathbf{x} + \mathbf{y})) = \mathbf{x} + \mathbf{y} = S(\mathbf{u}) + S(\mathbf{v})$$
純量倍同理。所以 $S$ 是線性變換。

## 老師講解
### 例 1 · Lay 2.3 Example 2
What can you say about a one-to-one linear transformation $T$ from $\mathbb{R}^n$ into $\mathbb{R}^n$?

1. **一對一** ⇒ 由第 4 週 Theorem 12,標準矩陣 $A$ 的各行線性獨立。
2. **那是 IMT 的 (e)** ⇒ $A$ 可逆 ⇒ 十二條全成立。
3. **讀出 (i)**:$T$ 把 $\mathbb{R}^n$ **映成** $\mathbb{R}^n$。
4. **讀出 (a) 再配 Theorem 9**:$T$ 可逆,而且 $T^{-1}(\mathbf{x}) = A^{-1}\mathbf{x}$。
5. **這題的震撼點**:題目只說「一對一」,結論卻多了「映成」與「可逆」。**方陣的世界裡,一對一就送映成**。
6. **提醒**:$\mathbb{R}^2 \to \mathbb{R}^3$ 的一對一變換就沒有這個好處(標準矩陣不是方陣,IMT 不適用)。

### 例 2 · Lay 2.3 Exercise 41
$T$ is a linear transformation from $\mathbb{R}^2$ into $\mathbb{R}^2$. Show that $T$ is invertible and find a formula for $T^{-1}$.

$$T(x_1, x_2) = (-9x_1 + 7x_2,\; 4x_1 - 3x_2)$$

1. **先寫標準矩陣**(第 4 週的技巧:把係數抄下來):
   $$A = \begin{bmatrix} -9 & 7 \\ 4 & -3 \end{bmatrix}$$
2. **檢查可逆**:$\det A = (-9)(-3) - 7(4) = 27 - 28 = -1 \ne 0$,由第 5 週 Theorem 4,$A$ 可逆。
3. **由 Theorem 9**,$T$ 可逆——這一步要寫出來,不能只說「矩陣可逆所以變換可逆」。
4. **算 $A^{-1}$**(第 5 週的 $2 \times 2$ 公式):
   $$A^{-1} = \frac{1}{-1}\begin{bmatrix} -3 & -7 \\ -4 & -9 \end{bmatrix} = \begin{bmatrix} 3 & 7 \\ 4 & 9 \end{bmatrix}$$
5. **寫回變換的語言**:
   $$T^{-1}(x_1, x_2) = (3x_1 + 7x_2,\; 4x_1 + 9x_2)$$
6. **檢查**:$T^{-1}(T(1, 0)) = T^{-1}(-9, 4) = (-27 + 28, -36 + 36) = (1, 0)$ ✓。做一個點的檢查只要 10 秒,務必養成習慣。
7. **注意分母的負號**:$\det = -1$,所以整個伴隨矩陣都要變號。這是最常掉分的地方。

### 例 3 · Lay 2.3 Exercises 43–44
Let $T : \mathbb{R}^n \to \mathbb{R}^n$ be an invertible linear transformation. Explain why $T$ is both one-to-one and onto $\mathbb{R}^n$. Use equations (1) and (2). Then give a second explanation using one or more theorems.

1. **第一種寫法:純函數論證,只用 (1)(2)。**
2. **一對一**:設 $T(\mathbf{u}) = T(\mathbf{v})$。兩邊作用 $S$,由 (1):
   $$\mathbf{u} = S(T(\mathbf{u})) = S(T(\mathbf{v})) = \mathbf{v}$$
   所以不同輸入不會有相同輸出。
3. **映成**:任給 $\mathbf{y} \in \mathbb{R}^n$,取 $\mathbf{x} = S(\mathbf{y})$。由 (2):
   $$T(\mathbf{x}) = T(S(\mathbf{y})) = \mathbf{y}$$
   所以 $\mathbf{y}$ 在值域裡。
4. **第二種寫法:用定理。** 由 Theorem 9,$T$ 可逆 ⇒ 標準矩陣 $A$ 可逆 ⇒ 由 IMT 的 (f) 與 (i),$T$ 既一對一又映成。三行寫完。
5. **兩種寫法的差別**:第一種**完全不需要矩陣**,只用函數的性質,所以它在更一般的場合(例如無限維空間)也成立;第二種借用了 IMT,快得多但限定方陣。
6. **課本為什麼要求兩種都寫?** 因為它們訓練不同的能力:一種是「從定義推」,一種是「引用定理」。考試兩種都可能考。

#### 備註
例 3 的兩種寫法建議並排寫在黑板左右兩半,讓學生直接比較長度與依賴的工具。

## 易錯點
- **只驗一個方向就說可逆**。定義要求 (1) **和** (2)(不過對方陣的**矩陣**而言,第 5 週的方框說驗一邊就夠——別把這兩件事混在一起)。
- **忘了引用 Theorem 9**。寫「$A$ 可逆所以 $T$ 可逆」少了依據,要寫「由 Theorem 9」。
- **$2 \times 2$ 反矩陣的分母是負數時沒有全部變號**(Exercise 41 的典型錯誤)。
- **把 $T^{-1}$ 寫成 $1/T$**。沒有這種寫法。
- **在非方陣上用 Theorem 9**。$T : \mathbb{R}^2 \to \mathbb{R}^3$ 的標準矩陣是 $3 \times 2$,不是方陣,整套結論都不適用。

## 教學提示
這個觀念本身不難(15 分鐘),它的價值在於**把 IMT 翻譯成變換的語言**,並把第 4 週的內容接回來。

建議開場:「上週學的旋轉矩陣,它的反矩陣是什麼變換?」讓學生自己說出「轉回去」,再帶出正式定義。

例 2 是計算題,務必當堂做一次,因為它結合了第 4 週的標準矩陣與第 5 週的 $2 \times 2$ 反矩陣公式——這是期中考很可能出現的組合題。

課堂建議做:Exercise 41(計算);Exercise 43 的第二種寫法(用定理,三行)。Exercise 42 當作業。

Exercises 47、48 是 Theorem 9 的補證(唯一性與線性),難度偏高,標為選做或當加分題。

## 練習
### 照做 · Lay 2.3 Exercises 41–42
In Exercises 41 and 42, $T$ is a linear transformation from $\mathbb{R}^2$ into $\mathbb{R}^2$. Show that $T$ is invertible and find a formula for $T^{-1}$.

(41) $T(x_1, x_2) = (-9x_1 + 7x_2,\; 4x_1 - 3x_2)$

(42) $T(x_1, x_2) = (6x_1 - 8x_2,\; -5x_1 + 7x_2)$

#### 解答
(41) 標準矩陣 $A = \begin{bmatrix} -9 & 7 \\ 4 & -3 \end{bmatrix}$,$\det A = 27 - 28 = -1 \ne 0$ ⇒ $A$ 可逆 ⇒ 由 Theorem 9,$T$ 可逆。
$$A^{-1} = \frac{1}{-1}\begin{bmatrix} -3 & -7 \\ -4 & -9 \end{bmatrix} = \begin{bmatrix} 3 & 7 \\ 4 & 9 \end{bmatrix}$$
所以 $T^{-1}(x_1, x_2) = (3x_1 + 7x_2,\; 4x_1 + 9x_2)$。

(42) $A = \begin{bmatrix} 6 & -8 \\ -5 & 7 \end{bmatrix}$,$\det A = 42 - 40 = 2 \ne 0$ ⇒ 可逆。
$$A^{-1} = \frac{1}{2}\begin{bmatrix} 7 & 8 \\ 5 & 6 \end{bmatrix} = \begin{bmatrix} 7/2 & 4 \\ 5/2 & 3 \end{bmatrix}$$
所以 $T^{-1}(x_1, x_2) = \left(\tfrac72 x_1 + 4x_2,\; \tfrac52 x_1 + 3x_2\right)$,也可以寫成 $\tfrac12(7x_1 + 8x_2,\; 5x_1 + 6x_2)$。

#### 備註
書後對 (41) 給的是提示:「先證標準矩陣可逆,再用定理說明 $T^{-1}(\mathbf{x}) = B\mathbf{x}$,其中 $B = \begin{bmatrix} 3 & 7 \\ 4 & 9 \end{bmatrix}$」——和上面的答案一致。

批改重點:有沒有寫「由 Theorem 9」。只算出 $A^{-1}$ 不算完整作答。

### 變化 · Lay 2.3 Exercises 43–44
(43) Let $T : \mathbb{R}^n \to \mathbb{R}^n$ be an invertible linear transformation. Explain why $T$ is both one-to-one and onto $\mathbb{R}^n$. Use equations (1) and (2). Then give a second explanation using one or more theorems.

(44) Let $T$ be a linear transformation that maps $\mathbb{R}^n$ onto $\mathbb{R}^n$. Show that $T^{-1}$ exists and maps $\mathbb{R}^n$ onto $\mathbb{R}^n$. Is $T^{-1}$ also one-to-one?

#### 解答
(43) 見上方例 3:**一對一**用 (1)(兩邊作用 $S$),**映成**用 (2)(取 $\mathbf{x} = S(\mathbf{y})$)。第二種說法:由 Theorem 9,$T$ 可逆 ⇒ $A$ 可逆 ⇒ 由 IMT 的 (f)、(i),兩者都成立。

(44) $T$ 映成是 IMT 的 (i) ⇒ 標準矩陣 $A$ 可逆 ⇒ 由 Theorem 9,$T^{-1}$ 存在且 $T^{-1}(\mathbf{x}) = A^{-1}\mathbf{x}$。

$A^{-1}$ 也是可逆方陣,把 IMT 套在 $A^{-1}$ 上:(i) 成立 ⇒ $T^{-1}$ 也**映成** $\mathbb{R}^n$;(f) 成立 ⇒ $T^{-1}$ **也是一對一**,所以最後一問的答案是「**是**」。

#### 備註
(44) 最後一問「Is $T^{-1}$ also one-to-one?」要明確回答,不能只證映成。最快的說法是:$T^{-1}$ 的反函數就是 $T$,所以 $T^{-1}$ 也可逆,自然一對一。

### 應用 · Lay 2.3 Exercises 45–46
(45) Suppose $T$ and $U$ are linear transformations from $\mathbb{R}^n$ to $\mathbb{R}^n$ such that $T(U\mathbf{x}) = \mathbf{x}$ for all $\mathbf{x}$ in $\mathbb{R}^n$. Is it true that $U(T\mathbf{x}) = \mathbf{x}$ for all $\mathbf{x}$ in $\mathbb{R}^n$? Why or why not?

(46) Suppose a linear transformation $T : \mathbb{R}^n \to \mathbb{R}^n$ has the property that $T(\mathbf{u}) = T(\mathbf{v})$ for some pair of distinct vectors $\mathbf{u}$ and $\mathbf{v}$ in $\mathbb{R}^n$. Can $T$ map $\mathbb{R}^n$ onto $\mathbb{R}^n$? Why or why not?

#### 解答
(45) **是,成立。** 設 $A$、$B$ 分別是 $T$、$U$ 的標準矩陣。$T(U\mathbf{x}) = \mathbf{x}$ 對所有 $\mathbf{x}$ 成立 ⇒ $AB\mathbf{x} = I\mathbf{x}$ 對所有 $\mathbf{x}$ 成立 ⇒ $AB = I$。

由觀念 2 的方框($A$、$B$ 都是方陣):$A$、$B$ 都可逆且 $B = A^{-1}$。於是 $BA = A^{-1}A = I$,也就是 $U(T\mathbf{x}) = \mathbf{x}$ 對所有 $\mathbf{x}$ 成立。

(46) **不能。** $\mathbf{u} \ne \mathbf{v}$ 卻有相同的像 ⇒ $T$ 不是一對一 ⇒ (f) 不成立 ⇒ 十二條全不成立 ⇒ 特別是 (i) 不成立,$T$ 不可能映成 $\mathbb{R}^n$。

#### 備註
(45) 的關鍵仍是「方陣」。若 $T : \mathbb{R}^n \to \mathbb{R}^m$、$U : \mathbb{R}^m \to \mathbb{R}^n$ 且 $m \ne n$,結論就不成立——這正好呼應第 5 週的單邊反矩陣。

### 挑戰 · Lay 2.3 Exercises 47–48
(47) Let $T : \mathbb{R}^n \to \mathbb{R}^n$ be an invertible linear transformation, and let $S$ and $U$ be functions from $\mathbb{R}^n$ into $\mathbb{R}^n$ such that $S(T(\mathbf{x})) = \mathbf{x}$ and $U(T(\mathbf{x})) = \mathbf{x}$ for all $\mathbf{x}$ in $\mathbb{R}^n$. Show that $U(\mathbf{v}) = S(\mathbf{v})$ for all $\mathbf{v}$ in $\mathbb{R}^n$. This will show that $T$ has a unique inverse, as asserted in Theorem 9. [*Hint:* Given any $\mathbf{v}$ in $\mathbb{R}^n$, we can write $\mathbf{v} = T(\mathbf{x})$ for some $\mathbf{x}$. Why? Compute $S(\mathbf{v})$ and $U(\mathbf{v})$.]

(48) Suppose $T$ and $S$ satisfy the invertibility equations (1) and (2), where $T$ is a linear transformation. Show directly that $S$ is a linear transformation. [*Hint:* Given $\mathbf{u}, \mathbf{v}$ in $\mathbb{R}^n$, let $\mathbf{x} = S(\mathbf{u})$, $\mathbf{y} = S(\mathbf{v})$. Then $T(\mathbf{x}) = \mathbf{u}$, $T(\mathbf{y}) = \mathbf{v}$. Why? Apply $S$ to both sides of the equation $T(\mathbf{x}) + T(\mathbf{y}) = T(\mathbf{x} + \mathbf{y})$. Also, consider $T(c\mathbf{x}) = cT(\mathbf{x})$.]

#### 解答
(47) 任給 $\mathbf{v} \in \mathbb{R}^n$。因為 $T$ 可逆,由 Exercise 43 知 $T$ **映成**,所以存在 $\mathbf{x}$ 使 $\mathbf{v} = T(\mathbf{x})$。於是
$$S(\mathbf{v}) = S(T(\mathbf{x})) = \mathbf{x}, \qquad U(\mathbf{v}) = U(T(\mathbf{x})) = \mathbf{x}$$
兩者相等。對每個 $\mathbf{v}$ 都成立,所以 $S$ 與 $U$ 是同一個函數。$\blacksquare$

(48) 令 $\mathbf{x} = S(\mathbf{u})$、$\mathbf{y} = S(\mathbf{v})$。由 (2) 得 $T(\mathbf{x}) = \mathbf{u}$、$T(\mathbf{y}) = \mathbf{v}$。

**加法**:$T$ 線性 ⇒ $T(\mathbf{x} + \mathbf{y}) = T(\mathbf{x}) + T(\mathbf{y}) = \mathbf{u} + \mathbf{v}$。兩邊作用 $S$ 並用 (1):
$$S(\mathbf{u} + \mathbf{v}) = S(T(\mathbf{x} + \mathbf{y})) = \mathbf{x} + \mathbf{y} = S(\mathbf{u}) + S(\mathbf{v})$$

**純量倍**:$T(c\mathbf{x}) = cT(\mathbf{x}) = c\mathbf{u}$,兩邊作用 $S$:
$$S(c\mathbf{u}) = S(T(c\mathbf{x})) = c\mathbf{x} = cS(\mathbf{u})$$

兩條性質都成立,所以 $S$ 是線性變換。$\blacksquare$

#### 備註
這兩題補上了 Theorem 9 敘述裡「the **unique** function」與「must be a **linear** transformation」的證明——課本把它們留給習題。

(47) 特別值得一提:題目只假設 $S$、$U$ 是**函數**(沒有假設線性),唯一性照樣成立。

## 驗算
```check
Matrix([[-9, 7], [4, -3]]).det() == -1
Matrix([[-9, 7], [4, -3]]).inv() == Matrix([[3, 7], [4, 9]])
Matrix([[3, 7], [4, 9]]) * (Matrix([[-9, 7], [4, -3]]) * Matrix([1, 0])) == Matrix([1, 0])
Matrix([[6, -8], [-5, 7]]).det() == 2
Matrix([[6, -8], [-5, 7]]).inv() == Matrix([[Rational(7,2), 4], [Rational(5,2), 3]])
Matrix([[6, -8], [-5, 7]]).inv() * Matrix([[6, -8], [-5, 7]]) == eye(2)
(lambda p, q: p * q == eye(2) and q * p == eye(2))(Matrix([[1, 2], [3, 7]]), Matrix([[7, -2], [-3, 1]]))
Matrix([[1, 0], [0, 0]]).rank() < 2 and Matrix([[1, 0], [0, 0]]).nullspace() != []
(lambda a: a.inv().rank() == 2 and a.inv().nullspace() == [])(Matrix([[-9, 7], [4, -3]]))
```
