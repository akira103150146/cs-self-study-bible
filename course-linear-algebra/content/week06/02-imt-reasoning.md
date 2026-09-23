---
title_en: Reasoning with the Invertible Matrix Theorem
title_zh: 用可逆矩陣定理推論:一條倒,全部倒
sub: One statement fails, they all fail
level: hard
source: Lay 2.3
lab_hook: '`A.rank() == n` 一次回答十二個問題;非方陣時要分開問'
---
## 觀念
The power of the Invertible Matrix Theorem lies in the connections it provides among so many important concepts, such as linear independence of columns of a matrix $A$ and the existence of solutions to equations of the form $A\mathbf{x} = \mathbf{b}$.

The *negation* of a statement in the theorem describes a property of every $n \times n$ singular matrix. For instance, an $n \times n$ singular matrix is *not* row equivalent to $I_n$, does *not* have $n$ pivot positions, and has linearly *dependent* columns.

The next fact follows from Theorem 8 and Exercise 10 in Section 2.2.

> Let $A$ and $B$ be square matrices. If $AB = I$, then $A$ and $B$ are both invertible, with $B = A^{-1}$ and $A = B^{-1}$.

The Invertible Matrix Theorem can be applied to *any* square matrix — not only to a matrix called $A$. For instance, applying it to $AB$, or to $A^{-1}$, or to $A^2$ gives information about those matrices.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| negation | 否定 | 把敘述反過來說;IMT 的否定描述所有奇異矩陣 |
| singular matrix | 奇異矩陣 | 不可逆的方陣 |
| implication | 蘊涵 | 「若 P 則 Q」;IMT 的題目大多是這種形式 |
| apply the IMT to $AB$ | 把 IMT 套在 $AB$ 上 | 定理對任何方陣都成立,不限於叫 $A$ 的那個 |
| justify your answer | 說明理由 | 本節幾乎每題都要求;要寫出引用哪一條 |

## 白話說
上一個觀念學會了「怎麼判斷可逆」。這一個觀念學的是**怎麼用它做推論**,也就是本節大部分題目的樣子。

**核心技巧只有三個:**

**技巧一:一條倒,全部倒。** 題目告訴你某一條不成立(例如「$A\mathbf{x} = \mathbf{b}$ 對某個 $\mathbf{b}$ 無解」),你就能一次推出**其他十一條也不成立**。所以答案往往比題目問的還多——問「各行會不會張成 $\mathbb{R}^n$?」你其實同時知道了「不是一對一」「$A\mathbf{x} = \mathbf{0}$ 有非零解」「$\det = 0$」。

**技巧二:IMT 可以套在任何方陣上。** 題目裡的矩陣叫 $K$、$G$、$AB$、$A^{-1}$ 都一樣。看到「$AB\mathbf{x} = \mathbf{0}$ 有非零解」,就把 $AB$ 當成 IMT 裡的那個方陣,立刻知道 $AB$ 不可逆。

**技巧三:$AB = I$ 就夠了。** 方陣只要驗一個方向,兩個矩陣就都可逆,而且互為反矩陣。這條在證明題裡非常好用(Exercises 35、36 就靠它)。

**寫答案的格式**(本節幾乎每題都要 justify):

> 由題意,IMT 的 (?) 成立/不成立 ⇒ $M$ 可逆/不可逆 ⇒ 由 (?),得到結論。

只要指出引用的條款編號,兩三行就能寫完一題。

## 在資工哪裡用
- **從一個檢查推出很多結論**:程式裡檢查完 `rank(A) == n`,就同時知道了「解唯一」「可以還原」「欄位無多餘」——不必逐項測試。
- **除錯時的推理**:模型訓練出現「參數不唯一」的症狀,等於 (d) 不成立,於是立刻知道設計矩陣的欄位線性相依——去找重複的特徵。
- **單邊反矩陣就夠**:實作可逆的編碼/解碼時,只要驗證 $DE = I$(方陣),就不必再驗 $ED = I$。這省掉一半的測試。
- **「只對方陣」的實務意義**:資料筆數 ≠ 特徵數時(絕大多數情況),存在與唯一是兩個獨立的問題——這正是第 14 週最小平方法要處理的事。

## 原理
**為什麼「一條倒,全部倒」?** 因為十二條是**等價**的,不只是「有些推得出有些」。等價的意思是:$P \Leftrightarrow Q$,所以 $\lnot P \Leftrightarrow \lnot Q$。把 IMT 寫成十二個等價的敘述,它們的否定也就自動全部等價。

**為什麼 $AB = I$(方陣)就保證兩者可逆?**(課本 p. 146 的方框,Exercise 33)

設 $A$、$B$ 都是 $n \times n$ 且 $AB = I$。把 $B$ 當成 IMT 敘述 (k) 裡的那個 $D$:「存在 $D$ 使 $AD = I$」成立,所以 (k) 成立 ⇒ (a) 成立,$A$ 可逆。

兩邊左乘 $A^{-1}$:$A^{-1}(AB) = A^{-1}$,左邊 $= (A^{-1}A)B = B$,所以 $B = A^{-1}$。

既然 $B$ 是可逆矩陣的反矩陣,$B$ 本身也可逆(第 5 週 Theorem 6(a)),而且 $B^{-1} = (A^{-1})^{-1} = A$。$\blacksquare$

**注意「方陣」用在哪裡**:用在「(k) ⇒ (a)」這一步,而 IMT 只對方陣成立。第 5 週的 Exercises 47–48 已經給過反例:$3 \times 2$ 的 $A$ 可以有 $CA = I_2$,但 $AC \ne I_3$。

**$AB$ 可逆 ⟺ $A$、$B$ 都可逆**(Exercises 35–36):

($\Leftarrow$)第 5 週 Theorem 6(b)。
($\Rightarrow$)令 $W = (AB)^{-1}$。由 $(AB)W = I$ 與結合律得 $A(BW) = I$,所以 (k) 對 $A$ 成立 ⇒ $A$ 可逆。另一邊,由 $W(AB) = I$ 得 $(WA)B = I$,所以 (j) 對 $B$ 成立 ⇒ $B$ 可逆。

**這裡有個值得講的細節**:$A(BW) = I$ 本身只說「$A$ 有右反矩陣」,對一般矩陣**不足以**推出可逆——必須靠 IMT 的 (k) ⇒ (a),而那一步需要方陣。課本在 Exercise 35 的解答特別反問 "Why not?",問的就是這件事。

## 老師講解
### 例 1 · Lay 2.3 Practice Problems 2–3
Suppose that for a certain $n \times n$ matrix $A$, statement (g) of the Invertible Matrix Theorem is *not* true. What can you say about equations of the form $A\mathbf{x} = \mathbf{b}$? Then: suppose that $A$ and $B$ are $n \times n$ matrices and the equation $AB\mathbf{x} = \mathbf{0}$ has a nontrivial solution. What can you say about the matrix $AB$?

1. **先把 (g) 唸出來**:「$A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b} \in \mathbb{R}^n$ 至少有一解」。
2. **它不成立,意思是什麼?** 「不是對每個 $\mathbf{b}$ 都有解」,也就是**至少存在一個 $\mathbf{b}$ 使 $A\mathbf{x} = \mathbf{b}$ 無解(不相容)**。這就是書後給的答案。
3. **還能多說什麼?** (g) 不成立 ⇒ $A$ 不可逆 ⇒ (d) 也不成立 ⇒ $A\mathbf{x} = \mathbf{0}$ 有非零解。所以對那些**有解**的 $\mathbf{b}$,解一定不唯一(特解加上整條零空間)。
4. **結論一句話**:$A\mathbf{x} = \mathbf{b}$ 不是無解、就是有無窮多解,**永遠不會恰好一解**。
5. **第二題:$AB\mathbf{x} = \mathbf{0}$ 有非零解。** 關鍵是把 $AB$ **當成一個方陣**,套 IMT。
6. **(d) 對 $AB$ 不成立** ⇒ 十二條對 $AB$ 全部不成立 ⇒ **$AB$ 不可逆**。
7. **可以再多推一步**(Exercises 35–36):$AB$ 不可逆 ⇒ $A$、$B$ 至少有一個不可逆。

### 例 2 · Lay 2.3 Exercises 35–36
Show that if $AB$ is invertible, so is $A$. You cannot use Theorem 6(b), because you cannot *assume* that $A$ and $B$ are invertible. [*Hint:* There is a matrix $W$ such that $ABW = I$. Why?] Then show that if $AB$ is invertible, so is $B$.

1. **為什麼不能用 Theorem 6(b)?** 那條說的是「$A$、$B$ 都可逆 ⇒ $AB$ 可逆」,方向相反。這題要走回頭路。
2. **先造出提示裡的 $W$**:$AB$ 可逆,所以 $W = (AB)^{-1}$ 存在,且 $(AB)W = I$。
3. **用結合律換括號**:
   $$(AB)W = A(BW) = I$$
4. **讀出這是 IMT 的哪一條**:存在一個 $n \times n$ 矩陣(就是 $BW$)使 $A \cdot (BW) = I$——這正是 **(k)**。
5. **由 IMT,(k) ⇒ (a)**,所以 $A$ 可逆。$\blacksquare$
6. **第二半用左邊**:由 $W(AB) = I$ 與結合律得 $(WA)B = I$,這是 IMT 的 **(j)** 對 $B$ 成立 ⇒ $B$ 可逆。$\blacksquare$
7. **最容易被扣分的地方**:只寫到第 3 步就說「所以 $A$ 可逆」。$A(BW) = I$ 只是右反矩陣,**必須引用 IMT 的 (k) ⇒ (a)**,而這一步用到了「方陣」。書後解答特別問 "Why not?" 就是在提醒這件事。

### 例 3 · Lay 2.3 Exercises 39–40
Suppose $A$ is an $n \times n$ matrix with the property that the equation $A\mathbf{x} = \mathbf{b}$ has at least one solution for each $\mathbf{b}$ in $\mathbb{R}^n$. **Without using Theorems 5 or 8**, explain why each equation $A\mathbf{x} = \mathbf{b}$ has in fact exactly one solution.

1. **題目不准用 IMT**,所以要回到第 1 章的工具,一步一步走。
2. **先用第 2 週的 Theorem 4**:「$A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b}$ 都相容 ⟺ $A$ 的**每一列**都有樞軸位置」。所以 $A$ 有 $n$ 個樞軸(列數是 $n$)。
3. **樞軸分布在相異的行**,而 $A$ 只有 $n$ 行,所以**每一行都是樞軸行**。
4. **沒有非樞軸行 ⇒ 沒有自由變數**(第 3 週)。
5. **增廣矩陣化簡後每個變數都被唯一決定**,所以解存在且唯一。$\blacksquare$
6. **反過來的 Exercise 40** 走同一條路的反方向:「只有平凡解 ⇒ 無自由變數 ⇒ 每一行都是樞軸行 ⇒ $n$ 個樞軸 ⇒ 每一列都有樞軸 ⇒ 對每個 $\mathbf{b}$ 都有解」。
7. **這兩題在做什麼?** 它們手工重走了 IMT 中 (d) ⟺ (g) 這一段,也就是**「唯一」與「存在」在方陣上為什麼會連動**。理解了這兩題,就理解了 IMT 為什麼只對方陣成立——關鍵是第 3 步的「$n$ 個樞軸塞進 $n$ 行」。

#### 備註
例 3 是本週最值得講的證明之一,建議在黑板上畫一個 $n \times n$ 的方格,把「每列一個樞軸」與「每行一個樞軸」畫出來,學生會馬上看懂為什麼方陣時兩者等價。

## 易錯點
- **推論只寫一半**。(g) 不成立時,不只是「有些 $\mathbf{b}$ 無解」,還包括「有解時解不唯一」。
- **忘了 IMT 可以套在別的矩陣上**。$AB$、$A^{-1}$、$A^2$ 都是方陣,都能套。
- **把右反矩陣當成可逆**。$A(BW) = I$ 要再引用 (k) ⇒ (a) 才能說 $A$ 可逆,而這需要方陣。
- **Exercise 32 的陷阱**:「$A\mathbf{x} = \mathbf{0}$ **有**平凡解」是廢話(永遠成立),不能推出任何事。IMT 要的是「**只有**平凡解」。
- **寫答案不引用條款**。「因為 $A$ 不可逆所以行相依」——中間少了「由 (e)」這一步,批改時會被扣分。
- Exercises 39–40 偷用 IMT。題目明講不准用,要回到樞軸的語言。

## 教學提示
這個觀念是**寫作訓練**,不是計算訓練。25 分鐘裡至少留 10 分鐘讓學生自己寫一題、再互相看。

建議的節奏:例 1 示範「一條倒全部倒」(5 分)→ 例 2 示範「套在別的矩陣上 + 為什麼需要方陣」(8 分)→ 例 3 示範「不准用 IMT 時怎麼走」(7 分)→ 學生練習(5 分)。

**板書一個答題範本**,整堂課不要擦:

> 「由題意,(x) 不成立 ⇒ $M$ 不可逆 ⇒ 由 (y),得到 ___。」

課堂建議做:Exercises 25、27、29、31(四題寫作,格式一樣);Exercise 35(證明,一定要講為什麼需要 IMT);Practice Problems 2、3。Exercises 39–40 建議留作業,或只講其中一題。

Exercises 33、34、37、38 難度較高,標為選做。

## 練習
### 照做 · Lay 2.3 Exercises 25–28
(25) If $A$ is invertible, then the columns of $A^{-1}$ are linearly independent. Explain why.

(26) If $C$ is $6 \times 6$ and the equation $C\mathbf{x} = \mathbf{v}$ is consistent for every $\mathbf{v}$ in $\mathbb{R}^6$, is it possible that for some $\mathbf{v}$, the equation $C\mathbf{x} = \mathbf{v}$ has more than one solution? Why or why not?

(27) If the columns of a $7 \times 7$ matrix $D$ are linearly independent, what can you say about solutions of $D\mathbf{x} = \mathbf{b}$? Why?

(28) If $n \times n$ matrices $E$ and $F$ have the property that $EF = I$, then $E$ and $F$ commute. Explain why.

#### 解答
- (25) $A$ 可逆 ⇒ $A^{-1}$ 也可逆(第 5 週 Theorem 6(a))。把 IMT 套在方陣 $A^{-1}$ 上:(a) 成立 ⇒ (e) 成立,所以 $A^{-1}$ 的各行線性獨立。
- (26) **不可能。** 「對每個 $\mathbf{v}$ 都相容」是 (g),$C$ 是方陣 ⇒ $C$ 可逆 ⇒ 由第 5 週 Theorem 5(或 IMT (d)),每個 $\mathbf{v}$ 恰有一解 $\mathbf{x} = C^{-1}\mathbf{v}$。
- (27) 行線性獨立是 (e) ⇒ $D$ 可逆 ⇒ 由 (g),$D\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b} \in \mathbb{R}^7$ **都有解**;再由 (d) 或 Theorem 5,這個解還**唯一**,$\mathbf{x} = D^{-1}\mathbf{b}$。
- (28) 由 p. 146 的方框(或把 (k) 套在 $E$ 上):$EF = I$ ⇒ $E$ 可逆且 $F = E^{-1}$。於是
  $$FE = E^{-1}E = I = EF$$
  兩者可交換。

#### 備註
(27) 書後的答案最後問了一句 "Can you say more?",提示要補上「而且解唯一」。批改時要看學生有沒有寫到唯一性。

(28) 的關鍵是「方陣」。非方陣時 $EF = I$ 推不出 $FE = I$(第 5 週 Exercises 47–48)。

### 是非 · Lay 2.3 Exercise 32
If $L$ is $n \times n$ and the equation $L\mathbf{x} = \mathbf{0}$ has the trivial solution, do the columns of $L$ span $\mathbb{R}^n$? Why?

#### 解答
**無法判斷。** 題目說的是「有平凡解」,但**任何**齊次方程 $L\mathbf{x} = \mathbf{0}$ 都有平凡解 $\mathbf{x} = \mathbf{0}$,所以這個條件沒有提供任何資訊。

兩個反例就能說明:$L = O$(零矩陣)滿足條件,但各行不張成 $\mathbb{R}^n$;$L = I$ 也滿足條件,而且各行張成 $\mathbb{R}^n$。

要能推出「張成」,條件必須是 IMT 的 (d):「**只有**平凡解(has *only* the trivial solution)」。

#### 備註
這題和 Exercise 18 的 into/onto 一樣是**文字陷阱題**,考的是 "only" 這個字。建議和 Exercise 11 並排出在同一張考卷上。

### 變化 · Lay 2.3 Exercises 29–31
(29) If the equation $G\mathbf{x} = \mathbf{y}$ has more than one solution for some $\mathbf{y}$ in $\mathbb{R}^n$, can the columns of $G$ span $\mathbb{R}^n$? Why or why not?

(30) If the equation $H\mathbf{x} = \mathbf{c}$ is inconsistent for some $\mathbf{c}$ in $\mathbb{R}^n$, what can you say about the equation $H\mathbf{x} = \mathbf{0}$? Why?

(31) If an $n \times n$ matrix $K$ cannot be row reduced to $I_n$, what can you say about the columns of $K$? Why?

#### 解答
- (29) **不能。** 有兩個相異解 $\mathbf{u} \ne \mathbf{v}$ ⇒ $G(\mathbf{u} - \mathbf{v}) = \mathbf{0}$ 且 $\mathbf{u} - \mathbf{v} \ne \mathbf{0}$ ⇒ (d) 不成立 ⇒ $G$ 不可逆 ⇒ (h) 也不成立,各行不張成 $\mathbb{R}^n$。
- (30) $H\mathbf{x} = \mathbf{c}$ 對某個 $\mathbf{c}$ 無解 ⇒ (g) 不成立 ⇒ $H$ 不可逆 ⇒ (d) 不成立,也就是 **$H\mathbf{x} = \mathbf{0}$ 有非平凡解**(因而有無窮多解)。
- (31) 不能化成 $I_n$ 就是 (b) 不成立 ⇒ $K$ 不可逆 ⇒ (e) 與 (h) 都不成立:$K$ 的各行**線性相依**,而且**不張成** $\mathbb{R}^n$。

#### 備註
(30) 要提醒學生:$H\mathbf{x} = \mathbf{0}$ 永遠有零解,所以答案的重點是「還有**非零**解」。

(31) 的完整答案要同時講「相依」與「不張成」兩件事,只寫一件不完整。

### 變化 · Lay 2.3 Exercises 33–34
(33) Verify the boxed statement preceding Example 1.

(34) Explain why the columns of $A^2$ span $\mathbb{R}^n$ whenever the columns of $A$ are linearly independent.

#### 解答
(33) 要證的是:**Let $A$ and $B$ be square matrices. If $AB = I$, then $A$ and $B$ are both invertible, with $B = A^{-1}$ and $A = B^{-1}$.**

把 $B$ 當成 (k) 裡的 $D$:存在 $D$ 使 $AD = I$ ⇒ (k) 成立 ⇒ (a) 成立,$A$ 可逆。兩邊左乘 $A^{-1}$:
$$A^{-1}(AB) = A^{-1} \implies B = A^{-1}$$
$B$ 是可逆矩陣的反矩陣,所以自己也可逆(第 5 週 Theorem 6(a)),且 $B^{-1} = (A^{-1})^{-1} = A$。$\blacksquare$

(34) $A$ 的各行線性獨立 ⇒ (e) ⇒ $A$ 可逆。由第 5 週 Theorem 6(b),兩個可逆矩陣的乘積可逆,所以 $A^2 = AA$ 可逆。把 IMT 套在方陣 $A^2$ 上:(a) 成立 ⇒ (h) 成立,$A^2$ 的各行張成 $\mathbb{R}^n$。$\blacksquare$

#### 備註
(33) 就是課本 p. 146 那個方框的證明,書後只給 "*Hint:* Use the IMT first."。這個結論本週一直在用,值得單獨講一次。

(34) 的骨架是「$A$ 可逆 ⇒ $A^2$ 可逆 ⇒ 套 IMT」,示範了技巧二(套在別的方陣上)。

### 應用 · Lay 2.3 Exercises 37–38 與 Practice Problems 2–3
(37) If $A$ is an $n \times n$ matrix and the equation $A\mathbf{x} = \mathbf{b}$ has more than one solution for some $\mathbf{b}$, then the transformation $\mathbf{x} \mapsto A\mathbf{x}$ is not one-to-one. What else can you say about this transformation? Justify your answer.

(38) If $A$ is an $n \times n$ matrix and the transformation $\mathbf{x} \mapsto A\mathbf{x}$ is one-to-one, what else can you say about this transformation? Justify your answer.

(Practice Problem 2) Suppose that for a certain $n \times n$ matrix $A$, statement (g) of the Invertible Matrix Theorem is *not* true. What can you say about equations of the form $A\mathbf{x} = \mathbf{b}$?

(Practice Problem 3) Suppose that $A$ and $B$ are $n \times n$ matrices and the equation $AB\mathbf{x} = \mathbf{0}$ has a nontrivial solution. What can you say about the matrix $AB$?

#### 解答
- (37) 不是一對一 ⇒ (f) 不成立 ⇒ 全部不成立。特別是 **(i) 不成立:這個變換不把 $\mathbb{R}^n$ 映成 $\mathbb{R}^n$**(值域是真子集)。又 (a) 不成立,由下一個觀念的 Theorem 9,**這個線性變換不可逆**。
- (38) 一對一 ⇒ (f) 成立 ⇒ 全部成立。特別是 **(i):這個變換映成 $\mathbb{R}^n$**;又 (a) 成立,由 Theorem 9,**這個變換可逆**,其反函數是 $S(\mathbf{x}) = A^{-1}\mathbf{x}$,也是線性變換。
- (PP2) (g) 不成立 ⇒ **至少存在一個 $\mathbf{b}$ 使 $A\mathbf{x} = \mathbf{b}$ 無解**。再由 (d) 也不成立,有解的那些 $\mathbf{b}$ 解不唯一。所以每個方程式不是無解就是無窮多解。
- (PP3) 把 IMT 套在方陣 $AB$ 上:(d) 說「$(AB)\mathbf{x} = \mathbf{0}$ 只有零解」,題目說有非零解 ⇒ (d) 不成立 ⇒ **$AB$ 不可逆**。(再配合 Exercises 35–36,$A$、$B$ 至少有一個不可逆。)

#### 備註
(37)(38) 是完全對稱的一對:一個全假、一個全真。很適合並排出在考卷上。

PP3 示範了「IMT 套在 $AB$ 上」這個技巧,是本觀念的代表題。

### 挑戰 · Lay 2.3 Exercises 35–36、39–40
(35) Show that if $AB$ is invertible, so is $A$. You cannot use Theorem 6(b), because you cannot *assume* that $A$ and $B$ are invertible. [*Hint:* There is a matrix $W$ such that $ABW = I$. Why?]

(36) Show that if $AB$ is invertible, so is $B$.

(39) Suppose $A$ is an $n \times n$ matrix with the property that the equation $A\mathbf{x} = \mathbf{b}$ has at least one solution for each $\mathbf{b}$ in $\mathbb{R}^n$. Without using Theorems 5 or 8, explain why each equation $A\mathbf{x} = \mathbf{b}$ has in fact exactly one solution.

(40) Suppose $A$ is an $n \times n$ matrix with the property that the equation $A\mathbf{x} = \mathbf{0}$ has only the trivial solution. Without using the Invertible Matrix Theorem, explain directly why the equation $A\mathbf{x} = \mathbf{b}$ must have a solution for each $\mathbf{b}$ in $\mathbb{R}^n$.

#### 解答
- (35) 取 $W = (AB)^{-1}$,則 $(AB)W = I$。由結合律 $A(BW) = I$,所以「存在 $n \times n$ 矩陣 $BW$ 使 $A(BW) = I$」,這是 (k);由 IMT,(k) ⇒ (a),$A$ 可逆。$\blacksquare$
- (36) 同一個 $W$ 滿足 $W(AB) = I$,由結合律 $(WA)B = I$,這是 (j) 對 $B$ 成立;由 IMT,(j) ⇒ (a),$B$ 可逆。$\blacksquare$
- (39) 由第 2 週 Theorem 4:對每個 $\mathbf{b}$ 都有解 ⟺ 每一列都有樞軸 ⇒ 共 $n$ 個樞軸。樞軸落在相異的行,而 $A$ 只有 $n$ 行 ⇒ 每一行都是樞軸行 ⇒ 沒有自由變數 ⇒ 解唯一。$\blacksquare$
- (40) 只有平凡解 ⇒ 沒有自由變數 ⇒ 每一行都是樞軸行 ⇒ 共 $n$ 個樞軸 ⇒ 分布在 $n$ 個相異的列 ⇒ 每一列都有樞軸 ⇒ 由第 2 週 Theorem 4,對每個 $\mathbf{b}$ 都有解。$\blacksquare$

#### 備註
(35)(36) 一個用右乘走 (k)、一個用左乘走 (j),合起來得到「$AB$ 可逆 ⟺ $A$、$B$ 都可逆」(方陣)。

(39)(40) 是一對逆向題,手工重走 IMT 的 (d) ⟺ (g)。**它們不准用 IMT**,所以要回到「樞軸的位置」這個層次——這也是理解 IMT 為什麼只對方陣成立的最佳練習。

## 驗算
```check
(lambda p, q: (p*q).rank() < 2 and min(p.rank(), q.rank()) < 2)(Matrix([[1, 2], [2, 4]]), Matrix([[1, 0], [0, 1]]))
(lambda p: p.inv().rank() == 2)(Matrix([[1, 2], [3, 7]]))
(lambda p, q: p*q == eye(2) and q*p == eye(2))(Matrix([[1, 2], [3, 7]]), Matrix([[7, -2], [-3, 1]]))
Matrix([[1, 2], [3, 7]])**2 == Matrix([[1, 2], [3, 7]]) * Matrix([[1, 2], [3, 7]]) and (Matrix([[1, 2], [3, 7]])**2).rank() == 2
zeros(2, 2) * Matrix([1, 0]) == zeros(2, 1) and zeros(2, 2).rank() == 0
eye(2) * Matrix([1, 0]) == Matrix([1, 0]) and eye(2).rank() == 2
(lambda g: (g * Matrix([-2, 1])).is_zero_matrix and g.rank() < 2 and g.nullspace() != [])(Matrix([[1, 2], [2, 4]]))
(lambda h: h.rank() < 2 and h.nullspace() != [])(Matrix([[1, 2], [2, 4]]))
(lambda k: k.rref()[0] != eye(2) and k.rank() < 2)(Matrix([[1, 2], [2, 4]]))
(lambda a, b: ((a*b).rank() == 2) and a.rank() == 2 and b.rank() == 2)(Matrix([[1, 2], [3, 7]]), Matrix([[2, 1], [1, 1]]))
Matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]]).rank() == 3 and Matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]]).nullspace() == []
```
