---
title_en: An LU Factorization Algorithm
title_zh: 怎麼做出 L 與 U:把乘數記下來
sub: Divide the highlighted entries by the pivot
level: hard
source: Lay 2.5
lab_hook: '`scipy.linalg.lu(A)` 回傳 P、L、U——多出來的 P 就是換列的紀錄'
---
## 觀念
Suppose $A$ can be reduced to an echelon form $U$ using only row replacements that add a multiple of one row to another row *below it*. In this case, there exist unit lower triangular elementary matrices $E_1, \dots, E_p$ such that

$$E_p \cdots E_1 A = U \tag{3}$$

Then

$$A = (E_p \cdots E_1)^{-1}U = LU, \qquad\text{where}\qquad L = (E_p \cdots E_1)^{-1} \tag{4}$$

Note that the row operations in equation (3), which reduce $A$ to $U$, also reduce the $L$ in equation (4) to $I$, because $E_p \cdots E_1 L = (E_p \cdots E_1)(E_p \cdots E_1)^{-1} = I$. This observation is the key to *constructing* $L$.

> **ALGORITHM FOR AN LU FACTORIZATION**
>
> **1.** Reduce $A$ to an echelon form $U$ by a sequence of row replacement operations, if possible.
>
> **2.** Place entries in $L$ such that the *same sequence of row operations* reduces $L$ to $I$.

In practical work, row interchanges are nearly always needed, because partial pivoting is used for high accuracy. To handle row interchanges, the LU factorization above can be modified easily to produce an $L$ that is *permuted lower triangular*. A reference to an "LU factorization" usually includes the possibility that $L$ might be permuted lower triangular.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| row replacement | 列的取代運算 | 把某列的倍數加到另一列;三種列運算裡唯一用到的 |
| pivot column | 樞軸行 | 有樞軸的那幾行 |
| highlighted entries | 標記起來的元素 | 課本畫框的那些:每個樞軸與它下面的元素 |
| permuted lower triangular | 重排過的下三角 | 列的順序調過,調回來就是下三角 |
| partial pivoting | 部分樞軸選取 | 選絕對值最大的當樞軸,為了數值穩定(第 1 週學過) |

## 白話說
**做法只有一句話:化簡的時候,把每次用的乘數記進 $L$。**

具體的步驟(課本的 Example 2):

1. **只用「把某列的倍數加到下面的列」**把 $A$ 化成階梯形 $U$。不換列、不縮放。
2. **每到一個樞軸行**,把那一行從樞軸開始往下的元素(就是課本畫框的那些)**除以樞軸**,結果就是 $L$ 的那一行。
3. $L$ 的對角線填 1,對角線上方填 0。

**為什麼這樣就對?** 因為那串把 $A$ 化成 $U$ 的列運算,**同時也把 $L$ 化成 $I$**(上面的觀念已經證過)。所以只要讓「$L$ 被同一串運算化成 $I$」,$L$ 就是正確的。

**一個很好用的檢查**:$L$ 的第 $(i, j)$ 格(在對角線下方)就是「消去第 $i$ 列第 $j$ 行那個位置時用的乘數」,而且**符號和你做的運算相反**——若你做「第 3 列減 2 倍第 1 列」,$L$ 的 $(3,1)$ 格就是 $+2$。

**遇到秩不足怎麼辦?** 若 $A$ 的樞軸行不夠(例如 $5 \times 4$ 但只有 3 個樞軸),$L$ 只做得出前幾行,**剩下的行直接抄 $I$ 的對應行**(課本 Practice Problem 就是這種情形)。

**遇到需要換列怎麼辦?** 那就得到 **permuted LU**:$L$ 的列被重排過。實務上的程式(包括 NumPy 與 SciPy)幾乎一定會換列,因為要做 partial pivoting 保持數值穩定。`scipy.linalg.lu` 回傳的 `P, L, U` 裡,$P$ 就是那個重排。

## 在資工哪裡用
- **理解函式庫的回傳值**:`scipy.linalg.lu(A)` 給的是 $PA = LU$(或 $A = PLU$,看版本),多出來的 $P$ 常讓人困惑——知道它從哪來就不會慌。
- **稀疏矩陣的 fill-in 問題**:$A$ 稀疏時,LU 分解可能讓 $L$、$U$ 冒出很多非零元素(叫 fill-in)。實務上會先重排列與行來減少 fill-in——這是大型稀疏求解器的核心技術。
- **帶狀矩陣**:若 $A$ 的非零元素集中在對角線附近(band matrix),$L$、$U$ 也是帶狀的,儲存與計算都非常省(實作課的 Exercise 31 會實際看到)。
- **增量式更新**:某些應用裡 $A$ 只改了一點點,可以更新現有的 $L$、$U$ 而不必重算。

## 原理
**為什麼「把標記的元素除以樞軸」就得到 $L$?**

考慮第一行。設第一個樞軸是 $a_{11}$,要消去第 $i$ 列的首項 $a_{i1}$,用的運算是

$$\text{第 } i \text{ 列} \;-\; \frac{a_{i1}}{a_{11}} \times \text{第 1 列}$$

這個運算對應的基本矩陣是「$I$ 的 $(i,1)$ 格放 $-a_{i1}/a_{11}$」。把所有這些運算合起來,它們的**反矩陣**(也就是 $L$)第一行就是

$$\begin{bmatrix} 1 \\ a_{21}/a_{11} \\ \vdots \\ a_{m1}/a_{11} \end{bmatrix} = \frac{1}{a_{11}}\begin{bmatrix} a_{11} \\ a_{21} \\ \vdots \\ a_{m1} \end{bmatrix}$$

正是「第一行除以樞軸」。第二行以後在**已經消過的矩陣**上重複同一件事。

**為什麼可以直接把反矩陣寫成「乘數改號」?** 因為單位下三角的基本矩陣 $E$(在 $(i,j)$ 格放 $c$)的反矩陣就是同一個位置放 $-c$——做反向的列運算即可。而多個這種矩陣相乘時,在「由上往下、由左往右」的順序下,乘數不會互相干擾(這是 Exercise 19、20 在講的性質)。

**秩不足時為什麼可以抄 $I$?** 因為 $U$ 的那幾列全是 0,乘法時 $L$ 對應的那幾行乘到的都是 0,填什麼都不影響 $LU$ 的值——但為了讓 $L$ 可逆(單位下三角),就填 $I$ 的那幾行。

## 老師講解
### 例 1 · Lay 2.5 Example 2
Find an LU factorization of

$$A = \begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\ -4 & -5 & 3 & -8 & 1 \\ 2 & -5 & -4 & 1 & 8 \\ -6 & 0 & 7 & -3 & 1 \end{bmatrix}$$

1. **先決定 $L$ 的大小**:$A$ 有 4 列,所以 $L$ 是 $4 \times 4$、$U$ 是 $4 \times 5$。
2. **第一行的樞軸是 2**。把第一行整行除以 2,就得到 $L$ 的第一行:
   $$\begin{bmatrix} 2 \\ -4 \\ 2 \\ -6 \end{bmatrix} \div 2 = \begin{bmatrix} 1 \\ -2 \\ 1 \\ -3 \end{bmatrix}$$
3. **消去第一行**(第 2 列加 2 倍第 1 列、第 3 列減第 1 列、第 4 列加 3 倍第 1 列):
   $$A \sim \begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\ 0 & 3 & 1 & 2 & -3 \\ 0 & -9 & -3 & -4 & 10 \\ 0 & 12 & 4 & 12 & -5 \end{bmatrix}$$
4. **第二行的樞軸是 3**。把樞軸與它下面的元素 $(3, -9, 12)$ 除以 3,得到 $L$ 第二行的下半:$(1, -3, 4)$。
5. **繼續消**,得到
   $$\sim \begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\ 0 & 3 & 1 & 2 & -3 \\ 0 & 0 & 0 & 2 & 1 \\ 0 & 0 & 0 & 4 & 7 \end{bmatrix}$$
   **注意第三行沒有樞軸**(整行變成 0),樞軸跳到第四行。
6. **第四行的樞軸是 2**,標記的元素是 $(2, 4)$,除以 2 得 $(1, 2)$——這是 $L$ 的第三行。
7. **最後一次消去**得到 $U$:
   $$U = \begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\ 0 & 3 & 1 & 2 & -3 \\ 0 & 0 & 0 & 2 & 1 \\ 0 & 0 & 0 & 0 & 5 \end{bmatrix}$$
   最後一個樞軸 5 除以自己得 1,是 $L$ 的第四行。
8. **把四行拼起來**:
   $$L = \begin{bmatrix} 1 & 0 & 0 & 0 \\ -2 & 1 & 0 & 0 \\ 1 & -3 & 1 & 0 \\ -3 & 4 & 2 & 1 \end{bmatrix}$$
9. **驗算**:$LU = A$ ✓。**每次做完一定要乘回去檢查**,這是最容易出錯的計算之一。

### 例 2 · Lay 2.5 Practice Problem
Find an LU factorization of

$$A = \begin{bmatrix} 2 & -4 & -2 & 3 \\ 6 & -9 & -5 & 8 \\ 2 & -7 & -3 & 9 \\ 4 & -2 & -2 & -1 \\ -6 & 3 & 3 & 4 \end{bmatrix}$$

*[Note:* It will turn out that $A$ has only three pivot columns, so the method of Example 2 will produce only the first three columns of $L$. The remaining two columns of $L$ come from $I_5$.*]*

1. **尺寸**:$A$ 是 $5 \times 4$,所以 $L$ 是 $5 \times 5$、$U$ 是 $5 \times 4$。
2. **第一行樞軸 2**,整行除以 2 得 $L$ 第一行 $(1, 3, 1, 2, -3)$。
3. **消完第一行**:
   $$\sim \begin{bmatrix} 2 & -4 & -2 & 3 \\ 0 & 3 & 1 & -1 \\ 0 & -3 & -1 & 6 \\ 0 & 6 & 2 & -7 \\ 0 & -9 & -3 & 13 \end{bmatrix}$$
4. **第二行樞軸 3**,標記元素 $(3, -3, 6, -9)$ 除以 3 得 $(1, -1, 2, -3)$——$L$ 第二行的下半。
5. **消完第二行**:
   $$\sim \begin{bmatrix} 2 & -4 & -2 & 3 \\ 0 & 3 & 1 & -1 \\ 0 & 0 & 0 & 5 \\ 0 & 0 & 0 & -5 \\ 0 & 0 & 0 & 10 \end{bmatrix}$$
   **第三行整行變成 0**,不是樞軸行。
6. **第四行樞軸 5**,標記元素 $(5, -5, 10)$ 除以 5 得 $(1, -1, 2)$——$L$ 第三行的下半。
7. **消完得到**
   $$U = \begin{bmatrix} 2 & -4 & -2 & 3 \\ 0 & 3 & 1 & -1 \\ 0 & 0 & 0 & 5 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$
8. **只做出 $L$ 的前三行**,第 4、5 行直接抄 $I_5$:
   $$L = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 \\ 3 & 1 & 0 & 0 & 0 \\ 1 & -1 & 1 & 0 & 0 \\ 2 & 2 & -1 & 1 & 0 \\ -3 & -3 & 2 & 0 & 1 \end{bmatrix}$$
9. **為什麼可以隨便抄?** 因為 $U$ 的第 4、5 列全是 0,$L$ 的第 4、5 行在乘法裡只會乘到 0。填 $I$ 的那兩行是為了保證 $L$ 可逆。
10. **驗算**:$LU = A$ ✓。

### 例 3 · 補充:需要換列的時候
Show that the matrix $A = \begin{bmatrix} 0 & 1 \\ 2 & 3 \end{bmatrix}$ has no LU factorization with $L$ unit lower triangular, and explain what a matrix program does instead.

1. **先假設有**:$\begin{bmatrix} 1 & 0 \\ c & 1 \end{bmatrix}\begin{bmatrix} u_{11} & u_{12} \\ 0 & u_{22} \end{bmatrix} = \begin{bmatrix} u_{11} & u_{12} \\ cu_{11} & cu_{12} + u_{22} \end{bmatrix}$。
2. **比對左上角**:$u_{11} = 0$。
3. **比對左下角**:$cu_{11} = 2$,但 $u_{11} = 0$ ⇒ $0 = 2$,**矛盾**。所以這個 $A$ 沒有(不換列的)LU 分解。
4. **問題出在哪?** 第一個樞軸位置是 0,不換列就做不下去——而演算法規定「只用取代運算」。
5. **程式怎麼做?** 先換列:$PA = \begin{bmatrix} 2 & 3 \\ 0 & 1 \end{bmatrix}$,其中 $P = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$。換完就是上三角,$L = I$、$U = PA$。
6. **所以程式回傳的是 $PA = LU$**(或寫成 $A = P^{-1}LU$)。這就是 **permuted LU**。
7. **而且程式不只在「不得不換」時換列**:為了數值穩定,它會**主動**挑絕對值最大的元素當樞軸(partial pivoting,第 1 週學過小樞軸的災難)。所以即使 $a_{11} \ne 0$,程式也常常換列。
8. **實作課會看到**:`scipy.linalg.lu` 的 $P$ 幾乎不會是單位矩陣。

#### 備註
例 3 是補充的(課本只在正文提了一句 permuted LU,沒有例子),但一定要講——否則學生在實作課看到 `P` 會完全不知道那是什麼。

## 易錯點
- **乘數的符號寫反**。做「第 3 列**減** 2 倍第 1 列」時,$L$ 的 $(3,1)$ 格是 $+2$。記法:$L$ 記的是「怎麼還原」。
- **在已經消過的矩陣上忘了用新的數字**。第二行的標記元素要取**消完第一行之後**的值。
- **秩不足時 $L$ 的剩餘行亂填**。要填 $I$ 的對應行。
- **用了縮放或換列**。演算法只允許「把某列的倍數加到下面的列」。真要換列就得走 permuted LU。
- **忘記驗算 $LU = A$**。這個計算步驟多,務必乘回去檢查。
- $A$ 是 $m \times n$ 時,$L$ 是 $m \times m$、$U$ 是 $m \times n$——大小常搞錯。

## 教學提示
這是本週計算量最大的 25 分鐘。**例 1 的板書不能省**,而且要把「標記的那一行」用彩色筆圈起來,讓學生看清楚「除以樞軸」是在對哪些數字做。

建議節奏:例 1 完整做(12 分)→ 例 2 只講「秩不足時 $L$ 怎麼補」(5 分)→ 例 3 的換列(5 分)→ 學生練習 Exercise 7 或 9(3 分)。

一個有效的板書技巧:把 $A$ 與 $L$ **並排**畫,每消一行就在兩邊同步寫,學生才會相信「同一串運算把 $A$ 化成 $U$、把 $L$ 化成 $I$」。

課堂建議做:Exercises 7、9(一個 $2 \times 2$、一個 $3 \times 3$);Exercise 12(秩不足);Practice Problem。Exercises 8、10、11 當作業。Exercises 13–16 份量較大,選做。

## 練習
### 照做 · Lay 2.5 Exercises 7–10
Find an LU factorization of the matrices in Exercises 7–16 (with $L$ unit lower triangular). Note that MATLAB will usually produce a permuted LU factorization because it uses partial pivoting for numerical accuracy.

(7) $\begin{bmatrix} 2 & 5 \\ -3 & -4 \end{bmatrix}$

(8) $\begin{bmatrix} 6 & 9 \\ 4 & 5 \end{bmatrix}$

(9) $\begin{bmatrix} 3 & -1 & 2 \\ -3 & -2 & 10 \\ 9 & -5 & 6 \end{bmatrix}$

(10) $\begin{bmatrix} -5 & 3 & 4 \\ 10 & -8 & -9 \\ 15 & 1 & 2 \end{bmatrix}$

#### 解答
(7) $L = \begin{bmatrix} 1 & 0 \\ -3/2 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 2 & 5 \\ 0 & 7/2 \end{bmatrix}$。(第一行 $(2, -3)$ 除以 2 得 $(1, -3/2)$。)

(8) $L = \begin{bmatrix} 1 & 0 \\ 2/3 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 6 & 9 \\ 0 & -1 \end{bmatrix}$。

(9) $L = \begin{bmatrix} 1 & 0 & 0 \\ -1 & 1 & 0 \\ 3 & 2/3 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 3 & -1 & 2 \\ 0 & -3 & 12 \\ 0 & 0 & -8 \end{bmatrix}$。

(10) $L = \begin{bmatrix} 1 & 0 & 0 \\ -2 & 1 & 0 \\ -3 & -5 & 1 \end{bmatrix}$,$U = \begin{bmatrix} -5 & 3 & 4 \\ 0 & -2 & -1 \\ 0 & 0 & 9 \end{bmatrix}$。

#### 備註
(10) 的樞軸是負數($-5$),乘數的正負號最容易算錯,適合當課堂示範。

四題都要求學生**乘回去驗算**。$2 \times 2$ 的兩題只要 30 秒。

### 照做 · Lay 2.5 Exercises 11–12
(11) $\begin{bmatrix} 3 & -6 & 3 \\ 6 & -7 & 2 \\ -1 & 7 & 0 \end{bmatrix}$

(12) $\begin{bmatrix} 2 & -4 & 2 \\ 1 & 5 & -4 \\ -6 & -2 & 4 \end{bmatrix}$

#### 解答
(11) $L = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1/3 & 1 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 3 & -6 & 3 \\ 0 & 5 & -4 \\ 0 & 0 & 5 \end{bmatrix}$。

(12) $L = \begin{bmatrix} 1 & 0 & 0 \\ 1/2 & 1 & 0 \\ -3 & -2 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 2 & -4 & 2 \\ 0 & 7 & -5 \\ 0 & 0 & 0 \end{bmatrix}$。

$A$ 是奇異的(rank 2),所以 $U$ 的最後一列全是 0;$L$ 的第 3 行取 $I_3$ 的第 3 行。

#### 備註
(12) 是**秩不足的第一題**,建議接在 Practice Problem 之後做。重點是:$U$ 出現零列不代表做錯了,$L$ 照樣補完就是。

### 變化 · Lay 2.5 Exercises 13–16
(13) $\begin{bmatrix} 1 & 3 & -5 & -3 \\ -1 & -5 & 8 & 4 \\ 4 & 2 & -5 & -7 \\ -2 & -4 & 7 & 5 \end{bmatrix}$

(14) $\begin{bmatrix} 1 & 4 & -1 & 5 \\ 3 & 7 & -2 & 9 \\ -2 & -3 & 1 & -4 \\ -1 & 6 & -1 & 7 \end{bmatrix}$

(15) $\begin{bmatrix} 2 & -4 & 4 & -2 \\ 6 & -9 & 7 & -3 \\ -1 & -4 & 8 & 0 \end{bmatrix}$

(16) $\begin{bmatrix} 2 & -6 & 6 \\ -4 & 5 & -7 \\ 3 & 5 & -1 \\ -6 & 4 & -8 \\ 8 & -3 & 9 \end{bmatrix}$

#### 解答
(13) $L = \begin{bmatrix} 1 & 0 & 0 & 0 \\ -1 & 1 & 0 & 0 \\ 4 & 5 & 1 & 0 \\ -2 & -1 & 0 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 1 & 3 & -5 & -3 \\ 0 & -2 & 3 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$(rank 2,$L$ 的第 3、4 行取自 $I_4$)。

(14) $L = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 3 & 1 & 0 & 0 \\ -2 & -1 & 1 & 0 \\ -1 & -2 & 0 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 1 & 4 & -1 & 5 \\ 0 & -5 & 1 & -6 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$。

(15) $L = \begin{bmatrix} 1 & 0 & 0 \\ 3 & 1 & 0 \\ -1/2 & -2 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 2 & -4 & 4 & -2 \\ 0 & 3 & -5 & 3 \\ 0 & 0 & 0 & 5 \end{bmatrix}$($3 \times 4$:$L$ 是 $3 \times 3$、$U$ 是 $3 \times 4$,樞軸行是第 1、2、4 行)。

(16) $L = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 \\ -2 & 1 & 0 & 0 & 0 \\ 3/2 & -2 & 1 & 0 & 0 \\ -3 & 2 & 0 & 1 & 0 \\ 4 & -3 & 0 & 0 & 1 \end{bmatrix}$,$U = \begin{bmatrix} 2 & -6 & 6 \\ 0 & -7 & 5 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$($5 \times 3$,rank 2)。

#### 備註
(15) 是**非方陣**的例子,最適合用來講「$L$ 是 $m \times m$、$U$ 是 $m \times n$」。

(16) 是本節最「高瘦」的一題($5 \times 3$ 且秩不足),$L$ 有五行但只有前兩行是算出來的,其餘抄 $I_5$。

這四題份量大,建議選一兩題當作業,其餘標為選做。

### 應用 · Lay 2.5 Practice Problem
Find an LU factorization of

$$A = \begin{bmatrix} 2 & -4 & -2 & 3 \\ 6 & -9 & -5 & 8 \\ 2 & -7 & -3 & 9 \\ 4 & -2 & -2 & -1 \\ -6 & 3 & 3 & 4 \end{bmatrix}$$

*[Note:* It will turn out that $A$ has only three pivot columns, so the method of Example 2 will produce only the first three columns of $L$. The remaining two columns of $L$ come from $I_5$.*]*

#### 解答
見上方例 2 的完整過程:

$$L = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 \\ 3 & 1 & 0 & 0 & 0 \\ 1 & -1 & 1 & 0 & 0 \\ 2 & 2 & -1 & 1 & 0 \\ -3 & -3 & 2 & 0 & 1 \end{bmatrix}, \qquad U = \begin{bmatrix} 2 & -4 & -2 & 3 \\ 0 & 3 & 1 & -1 \\ 0 & 0 & 0 & 5 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

樞軸行是第 1、2、4 行(第 3 行不是),所以只做得出 $L$ 的前三行,第 4、5 行取自 $I_5$。

#### 備註
這題是「秩不足時 $L$ 怎麼補完」的標準示範,也是下一個觀念 Exercise 22(reduced LU)的前置題——那題要把 $L$ 的前三行與 $U$ 的前三列切出來。

### 挑戰 · 補充:沒有 LU 分解的矩陣
Show that $A = \begin{bmatrix} 0 & 1 \\ 2 & 3 \end{bmatrix}$ has no LU factorization with $L$ unit lower triangular. Then find a permutation matrix $P$ such that $PA$ does have one, and write down $P$, $L$, and $U$.

#### 解答
**沒有 LU 分解**:假設 $\begin{bmatrix} 1 & 0 \\ c & 1 \end{bmatrix}\begin{bmatrix} u_{11} & u_{12} \\ 0 & u_{22} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 2 & 3 \end{bmatrix}$。比對 $(1,1)$ 格得 $u_{11} = 0$;比對 $(2,1)$ 格得 $cu_{11} = 2$,即 $0 = 2$,矛盾。

**換列之後就有**:取
$$P = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \qquad PA = \begin{bmatrix} 2 & 3 \\ 0 & 1 \end{bmatrix}$$
已經是上三角,所以 $L = I_2$、$U = \begin{bmatrix} 2 & 3 \\ 0 & 1 \end{bmatrix}$,即 $PA = LU$。

#### 備註
這是本講義補充的題目(課本沒有),但它解釋了實作課會看到的東西:`scipy.linalg.lu` 回傳三個矩陣 `P, L, U`,那個 $P$ 就是這裡的換列紀錄。

而且程式**不是只在樞軸為 0 時才換列**——為了數值穩定(partial pivoting),它會主動挑絕對值最大的元素當樞軸。

## 驗算
```check
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0,0],[-2,1,0,0],[1,-3,1,0],[-3,4,2,1]]), Matrix([[2,4,-1,5,-2],[0,3,1,2,-3],[0,0,0,2,1],[0,0,0,0,5]]), Matrix([[2,4,-1,5,-2],[-4,-5,3,-8,1],[2,-5,-4,1,8],[-6,0,7,-3,1]]))
(lambda l, u, m: l.is_lower and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0,0,0],[3,1,0,0,0],[1,-1,1,0,0],[2,2,-1,1,0],[-3,-3,2,0,1]]), Matrix([[2,-4,-2,3],[0,3,1,-1],[0,0,0,5],[0,0,0,0],[0,0,0,0]]), Matrix([[2,-4,-2,3],[6,-9,-5,8],[2,-7,-3,9],[4,-2,-2,-1],[-6,3,3,4]]))
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0],[Rational(-3,2),1]]), Matrix([[2,5],[0,Rational(7,2)]]), Matrix([[2,5],[-3,-4]]))
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0],[Rational(2,3),1]]), Matrix([[6,9],[0,-1]]), Matrix([[6,9],[4,5]]))
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0],[-1,1,0],[3,Rational(2,3),1]]), Matrix([[3,-1,2],[0,-3,12],[0,0,-8]]), Matrix([[3,-1,2],[-3,-2,10],[9,-5,6]]))
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0],[-2,1,0],[-3,-5,1]]), Matrix([[-5,3,4],[0,-2,-1],[0,0,9]]), Matrix([[-5,3,4],[10,-8,-9],[15,1,2]]))
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0],[2,1,0],[Rational(-1,3),1,1]]), Matrix([[3,-6,3],[0,5,-4],[0,0,5]]), Matrix([[3,-6,3],[6,-7,2],[-1,7,0]]))
(lambda l, u, m: l.is_lower and u.is_upper and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0],[Rational(1,2),1,0],[-3,-2,1]]), Matrix([[2,-4,2],[0,7,-5],[0,0,0]]), Matrix([[2,-4,2],[1,5,-4],[-6,-2,4]]))
(lambda l, u, m: l.is_lower and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0,0],[-1,1,0,0],[4,5,1,0],[-2,-1,0,1]]), Matrix([[1,3,-5,-3],[0,-2,3,1],[0,0,0,0],[0,0,0,0]]), Matrix([[1,3,-5,-3],[-1,-5,8,4],[4,2,-5,-7],[-2,-4,7,5]]))
(lambda l, u, m: l.is_lower and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0,0],[3,1,0,0],[-2,-1,1,0],[-1,-2,0,1]]), Matrix([[1,4,-1,5],[0,-5,1,-6],[0,0,0,0],[0,0,0,0]]), Matrix([[1,4,-1,5],[3,7,-2,9],[-2,-3,1,-4],[-1,6,-1,7]]))
(lambda l, u, m: l.is_lower and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0],[3,1,0],[Rational(-1,2),-2,1]]), Matrix([[2,-4,4,-2],[0,3,-5,3],[0,0,0,5]]), Matrix([[2,-4,4,-2],[6,-9,7,-3],[-1,-4,8,0]]))
(lambda l, u, m: l.is_lower and all(l[i, i] == 1 for i in range(l.rows)) and l * u == m)(Matrix([[1,0,0,0,0],[-2,1,0,0,0],[Rational(3,2),-2,1,0,0],[-3,2,0,1,0],[4,-3,0,0,1]]), Matrix([[2,-6,6],[0,-7,5],[0,0,0],[0,0,0],[0,0,0]]), Matrix([[2,-6,6],[-4,5,-7],[3,5,-1],[-6,4,-8],[8,-3,9]]))
Matrix([[0, 1], [2, 3]])[0, 0] == 0 and Matrix([[0, 1], [1, 0]]) * Matrix([[0, 1], [2, 3]]) == Matrix([[2, 3], [0, 1]])
Matrix([[2, 3], [0, 1]]).is_upper
```
