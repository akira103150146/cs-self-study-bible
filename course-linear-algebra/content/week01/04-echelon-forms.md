---
title_en: Row Reduction and Echelon Forms
title_zh: 梯形、簡化梯形與 pivot
sub: Row reduction always aims at the same staircase
level: mid
source: Lay 1.2
lab_hook: "`Matrix(A).rref()` 回傳 `(RREF, pivot 所在的行)`"
---
## 觀念
A **leading entry** of a row is the leftmost nonzero entry (in a nonzero row). A rectangular matrix is in **echelon form** (or **row echelon form**) if it has the following three properties:

1. All nonzero rows are above any rows of all zeros.
2. Each leading entry of a row is in a column to the right of the leading entry of the row above it.
3. All entries in a column below a leading entry are zeros.

If a matrix in echelon form satisfies the following additional conditions, then it is in **reduced echelon form** (or **reduced row echelon form**):

4. The leading entry in each nonzero row is 1.
5. Each leading 1 is the only nonzero entry in its column.

**Theorem 1 (Uniqueness of the Reduced Echelon Form).** Each matrix is row equivalent to one and only one reduced echelon matrix.

A **pivot position** in a matrix $A$ is a location in $A$ that corresponds to a leading 1 in the reduced echelon form of $A$. A **pivot column** is a column of $A$ that contains a pivot position. A **pivot** is a nonzero number in a pivot position that is used as needed to create zeros via row operations.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| leading entry | 首項(領頭元素) | 一列最左邊的非 0 數 |
| echelon form / row echelon form | 列梯形 | 首項像樓梯一樣往右下走,首項底下全是 0 |
| reduced echelon form (RREF) | 簡化列梯形 | 再要求首項都是 1,且首項所在的行其他位置全是 0 |
| echelon matrix | 梯形矩陣 | 已經是列梯形的矩陣 |
| pivot position | 樞紐位置(pivot 位置) | RREF 裡首項 1 所在的位置 |
| pivot column | 樞紐行(pivot 行) | 含有 pivot 位置的行 |
| pivot | 樞紐(主元) | 放在 pivot 位置、拿來消去其他列的那個非 0 數 |
| row reduction algorithm | 列化簡演算法 | 課本的五個步驟;又叫高斯消去法(Gaussian elimination) |
| forward phase | 前進階段 | 步驟 1–4,做出列梯形 |
| backward phase | 回代階段 | 步驟 5,做出 RREF |
| partial pivoting | 部分樞紐選取 | 電腦挑該行絕對值最大的數當 pivot,減少捨入誤差 |

## 白話說
列化簡的目標永遠是同一個形狀:**像樓梯一樣往右下走**。

- **列梯形**:每一列第一個非 0 的數(首項)必須比上一列的首項更靠右,首項底下全是 0,全 0 的列放最下面。
- **簡化列梯形(RREF)**:再多兩個要求——首項都是 1,而且首項所在的那一行,其他位置全部是 0(上下都要清乾淨)。

![列梯形只要求樓梯形狀;簡化列梯形再要求 pivot 是 1、而且 pivot 所在的行其他位置都是 0。■ 代表任何非 0 的數,* 代表任何數。](staircase.svg)

同一個矩陣,化簡的路線不同,梯形可能長得不一樣;但 **RREF 只有一種**(Theorem 1)。所以「pivot 在哪些位置」是矩陣本身的性質,不管誰來化簡、怎麼化簡,答案都一樣。這就是為什麼後面十幾週的觀念,幾乎都要回到「pivot 在哪裡」。

## 幾何意義
在增廣矩陣裡,梯形的每一個**非 0 列**都代表一條「真正提供新限制」的方程式;化簡後變成**全 0 的列**,代表那條方程式其實是其他方程式的組合,沒有提供新資訊。

例如三個平面,如果化簡後只剩兩個非 0 列,表示其中一個平面是「多餘的」:它剛好通過另外兩個平面的交線。pivot 的個數,就是「真正獨立的限制條件」有幾條——這個想法到第 7 週會變成「秩(rank)」。

## 在資工哪裡用
SymPy 的 `Matrix(A).rref()` 會直接回傳 RREF 和 pivot 所在的行號。之後判斷方程組有沒有解、有幾個自由變數(觀念 5)、資料表有哪些欄位重複(第 3 週),全都是在「讀 pivot」。

數值計算函式庫(NumPy 底層的 LAPACK)解方程組用的就是這個演算法的變形,只是會做 partial pivoting 以減少誤差。

## 實際應用
**兩千年前的演算法。** 課本腳註提到,類似的消去法約在公元前 250 年就被中國數學家使用;西方直到 19 世紀由高斯重新發現,1888 年德國工程師 Jordan 在大地測量的書裡推廣。中國的《九章算術》「方程」章,正是把係數排成直行、用算籌做列運算——和本觀念的做法幾乎一樣,只是當時是「直的」寫。

## 數值筆記
課本步驟 2 可以任選該行一個非 0 的數當 pivot。電腦程式通常會挑該行**絕對值最大**的數,這個策略叫 **partial pivoting**,因為它能減少計算中的捨入誤差。實作課的「解讀」階段會親眼看到:拿很小的數當 pivot,答案可以錯得離譜。(改寫自 Lay 1.2 Numerical Note)

## 原理
**列化簡演算法**(課本 p. 40–42),前四步做出梯形,第五步做出 RREF:

1. 從最左邊**不全為 0 的行**開始。這是 pivot 行,pivot 位置在最上面。
2. 在 pivot 行選一個非 0 的數當 pivot;需要的話先換列,把它移到 pivot 位置。
3. 用 replacement 把 pivot **底下**全部消成 0。
4. 蓋住(忽略)pivot 所在的列以及上面所有列,對剩下的子矩陣重複步驟 1–3,直到沒有非 0 列可處理。
5. 從**最右邊**的 pivot 開始,往上、往左:把每個 pivot 上方消成 0;pivot 不是 1 就用 scaling 變成 1。

步驟 1–4 叫**前進階段**,步驟 5 叫**回代階段**。

**為什麼往回要從最右下角開始?** 最下面的列 0 最多,拿它去消上面的列,不會把已經清好的位置弄亂,計算量也最少。

**RREF 為什麼唯一**:證明在課本附錄 A,本課只陳述不證明。它的意義是讓「pivot 位置」有明確的定義,不會因為化簡路線不同而改變。

**注意**:pivot(拿來消去的那個數)不一定等於原矩陣在 pivot 位置上的數。例 2 的 pivot 是 1、2、$-5$,但原矩陣在那三個位置上的數是 0、$-2$、3(課本 p. 40)。

## 老師講解
### 例 1 · Lay 1.2(p. 37)
Which of the following matrices are in echelon form? Which are in reduced echelon form?

(a) $\begin{bmatrix} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 0 & 0 & 0 & 5/2 \end{bmatrix}$  (b) $\begin{bmatrix} 1 & 0 & 0 & 29 \\ 0 & 1 & 0 & 16 \\ 0 & 0 & 1 & 3 \end{bmatrix}$  (c) $\begin{bmatrix} 0 & 1 & 2 \\ 1 & 0 & 3 \end{bmatrix}$

1. 先找每一列的首項(最左邊的非 0 數),再檢查它們是不是一列比一列靠右、首項底下是不是都是 0。
2. (a) 首項是 $2$(第 1 行)、$1$(第 2 行)、$5/2$(第 4 行),一路往右,首項底下都是 0 → **是列梯形**。但首項 $2$ 和 $5/2$ 不是 1 → **不是 RREF**。這就是觀念 3 說的「三角形式」。
3. (b) 首項都是 1,分別在第 1、2、3 行,而且各自所在的行其他位置都是 0 → **是 RREF**(當然也是列梯形)。第 4 行的 29、16、3 不是首項,不受限制。
4. (c) 第 1 列的首項在第 2 行,第 2 列的首項卻在第 1 行,**往左退了**,違反條件 2 → **不是列梯形**。交換兩列就會是。

#### 備註
(a)(b) 是課本 p. 37 的兩個矩陣;(c) 是補充的反例,專門示範「往左退」。

### 例 2 · Lay 1.2 Example 2
Row reduce the matrix $A$ below to echelon form, and locate the pivot columns of $A$.

$$A = \begin{bmatrix} 0 & -3 & -6 & 4 & 9 \\ -1 & -2 & -1 & 3 & 1 \\ -2 & -3 & 0 & 3 & -1 \\ 1 & 4 & 5 & -9 & -7 \end{bmatrix}$$

1. **找第一個 pivot 行**:最左邊不全為 0 的行是第 1 行,pivot 位置在最上面。但那個位置是 0,不能當 pivot,必須換列。
2. **選 pivot**:第 1 行裡任何非 0 的數都可以。課本選**交換第 1、4 列**,讓 1 到最上面——因為用 1 去消,下一步不會出現分數:
   $$\begin{bmatrix} 1 & 4 & 5 & -9 & -7 \\ -1 & -2 & -1 & 3 & 1 \\ -2 & -3 & 0 & 3 & -1 \\ 0 & -3 & -6 & 4 & 9 \end{bmatrix}$$
3. **消掉 pivot 底下**:$R_2 \leftarrow R_2 + R_1$、$R_3 \leftarrow R_3 + 2R_1$(第 4 列本來就是 0,不用動):
   $$\begin{bmatrix} 1 & 4 & 5 & -9 & -7 \\ 0 & 2 & 4 & -6 & -6 \\ 0 & 5 & 10 & -15 & -15 \\ 0 & -3 & -6 & 4 & 9 \end{bmatrix}$$
4. **蓋住第 1 列,找下一個 pivot**:剩下的部分,最左邊不全為 0 的是第 2 行,pivot 位置在第 2 列。選那裡的 **2** 當 pivot。
5. **消掉 2 底下**:$R_3 \leftarrow R_3 + (-\tfrac52)R_2$、$R_4 \leftarrow R_4 + \tfrac32 R_2$:
   $$\begin{bmatrix} 1 & 4 & 5 & -9 & -7 \\ 0 & 2 & 4 & -6 & -6 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & -5 & 0 \end{bmatrix}$$
6. **卡住了?** 蓋住前兩列,第 3 行剩下的部分全是 0,**第 3 行沒辦法產生首項**(也不能拿第 1、2 列來用,那會破壞已經做好的樓梯)。跳過第 3 行,看第 4 行:第 4 列有 $-5$。**交換第 3、4 列**:
   $$\begin{bmatrix} 1 & 4 & 5 & -9 & -7 \\ 0 & 2 & 4 & -6 & -6 \\ 0 & 0 & 0 & -5 & 0 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$$
7. 現在是列梯形。首項在第 1、2、4 行,所以 **$A$ 的 pivot 行是第 1、2、4 行**。在原矩陣 $A$ 裡,pivot 位置是 $(1,1)$、$(2,2)$、$(3,4)$。
8. 這個例子用到的 pivot 是 1、2、$-5$,和原矩陣在那三個位置上的數(0、$-2$、3)不一樣——pivot 是化簡過程中「拿來消去的數」。

### 例 3 · Lay 1.2 Example 3
Apply elementary row operations to transform the following matrix first into echelon form and then into reduced echelon form:

$$\begin{bmatrix} 0 & 3 & -6 & 6 & 4 & -5 \\ 3 & -7 & 8 & -5 & 8 & 9 \\ 3 & -9 & 12 & -9 & 6 & 15 \end{bmatrix}$$

1. **步驟 1**:最左邊不全為 0 的是第 1 行,它是 pivot 行,pivot 位置在最上面。
2. **步驟 2**:最上面是 0,換列。課本**交換第 1、3 列**(換第 1、2 列也可以):
   $$\begin{bmatrix} 3 & -9 & 12 & -9 & 6 & 15 \\ 3 & -7 & 8 & -5 & 8 & 9 \\ 0 & 3 & -6 & 6 & 4 & -5 \end{bmatrix}$$
3. **步驟 3**:消掉 pivot 3 底下。第 2 列也是 3,直接 $R_2 \leftarrow R_2 + (-1)R_1$,得 $[\,0 \;\; 2 \;\; {-4} \;\; 4 \;\; 2 \;\; {-6}\,]$。(也可以先把第 1 列除以 3,但這裡直接減比較省事。)
4. **步驟 4**:蓋住第 1 列。剩下的部分最左邊不全為 0 的是第 2 行,選最上面的 **2** 當 pivot,$R_3 \leftarrow R_3 + (-\tfrac32)R_2$,第 3 列變成 $[\,0 \;\; 0 \;\; 0 \;\; 0 \;\; 1 \;\; 4\,]$:
   $$\begin{bmatrix} 3 & -9 & 12 & -9 & 6 & 15 \\ 0 & 2 & -4 & 4 & 2 & -6 \\ 0 & 0 & 0 & 0 & 1 & 4 \end{bmatrix}$$
5. 再蓋住第 2 列,只剩一列,它的首項在第 5 行,不用再做事。**列梯形完成**,pivot 行是第 1、2、5 行。
6. **步驟 5(往回)**:從最右邊的 pivot(第 3 列的 1)開始,把它上面消成 0:$R_1 \leftarrow R_1 + (-6)R_3$、$R_2 \leftarrow R_2 + (-2)R_3$:
   $$\begin{bmatrix} 3 & -9 & 12 & -9 & 0 & -9 \\ 0 & 2 & -4 & 4 & 0 & -14 \\ 0 & 0 & 0 & 0 & 1 & 4 \end{bmatrix}$$
7. 下一個 pivot 在第 2 列,是 2,先縮放成 1:$R_2 \leftarrow \tfrac12 R_2$,得 $[\,0 \;\; 1 \;\; {-2} \;\; 2 \;\; 0 \;\; {-7}\,]$。再消掉它上面:$R_1 \leftarrow R_1 + 9R_2$,得 $[\,3 \;\; 0 \;\; {-6} \;\; 9 \;\; 0 \;\; {-72}\,]$。
8. 最後把第 1 列的 pivot 3 變成 1:$R_1 \leftarrow \tfrac13 R_1$。得到 **RREF**:
   $$\begin{bmatrix} 1 & 0 & -2 & 3 & 0 & -24 \\ 0 & 1 & -2 & 2 & 0 & -7 \\ 0 & 0 & 0 & 0 & 1 & 4 \end{bmatrix}$$
9. 檢查 RREF 的五個條件:首項都是 1、一路往右、首項所在的行(第 1、2、5 行)其他位置都是 0 ✓。第 3、4、6 行不是 pivot 行,裡面的數不受限制。

#### 備註
例 3 很長,建議只完整做這一題,並在黑板上把「步驟 1–5」的框框一個一個貼出來。例 2 可以只做到第 7 步,強調「跳過全 0 的行」。

## 易錯點
- 在**原矩陣**上圈 pivot。pivot 位置要看化簡**之後**的梯形;原矩陣的左上角甚至可能是 0。
- 往前階段遇到「某一行剩下的部分全是 0」就卡住,或硬拿 0 當 pivot。正確做法是跳過這一行、往右找下一行。
- 往回階段從上往下做,把已經清好的 0 又弄亂。要從**最右下**的 pivot 開始往上。
- 以為 RREF 要求「不是 pivot 的行」也要清乾淨。只有 pivot 行需要。

## 教學提示
用「樓梯」比喻:每下一階至少往右一格,可以一次跨好幾格(像例 2 的第 3 行被跨過去)。學生最常卡在「某一行底下都是 0 時要跳過它」,例 2 的第 6 步就是專門示範這件事,請放慢速度。

往前、往回兩個階段在黑板上用兩種顏色寫,學生比較記得住「先消下面、再消上面」的順序。

課堂建議做:照做 1–3(判斷題快速過,Exercise 3 完整做);是非全部;Exercise 4 當作業。

## 練習
### 照做 · Lay 1.2 Exercise 1
Determine which matrices are in reduced echelon form and which others are only in echelon form.

(a) $\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \end{bmatrix}$  (b) $\begin{bmatrix} 1 & 0 & 1 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$  (c) $\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$  (d) $\begin{bmatrix} 1 & 1 & 0 & 1 & 1 \\ 0 & 2 & 0 & 2 & 2 \\ 0 & 0 & 0 & 3 & 3 \\ 0 & 0 & 0 & 0 & 4 \end{bmatrix}$

#### 解答
- (a) **RREF**:首項 1 在第 1、2、3 行,這三行其他位置都是 0;第 4 行不是 pivot 行,不受限制。
- (b) **只是列梯形**:首項在第 1、3、4 行,但第 3 行的首項 1 上方還有一個 1(第 1 列),違反條件 5。
- (c) **RREF**:首項 1 在第 1、2 行,乾淨;第 3 行的 1 不是首項,可以留著。
- (d) **只是列梯形**:首項 1、2、3、4 不全是 1,上方也沒清乾淨。

書後解答:Reduced echelon form: a and c. Echelon form: b and d.

### 照做 · Lay 1.2 Exercise 2
Determine which matrices are in reduced echelon form and which others are only in echelon form.

(a) $\begin{bmatrix} 1 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 0 \end{bmatrix}$  (b) $\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \end{bmatrix}$  (c) $\begin{bmatrix} 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \end{bmatrix}$  (d) $\begin{bmatrix} 0 & 1 & 1 & 1 & 1 \\ 0 & 0 & 2 & 2 & 2 \\ 0 & 0 & 0 & 0 & 3 \\ 0 & 0 & 0 & 0 & 0 \end{bmatrix}$

#### 解答
- (a) **RREF**:首項 1 在第 1、3 行,這兩行其他位置都是 0。
- (b) **RREF**。
- (c) **兩者都不是**:第 2 列的首項在第 1 行,和第 1 列同一行,沒有往右走(而且首項底下不是 0)。
- (d) **只是列梯形**:首項在第 2、3、5 行,往右走沒問題,但首項 2、3 不是 1,上方也沒清乾淨。

#### 備註
(c) 是「兩者都不是」的例子,提醒學生答案不只兩種。

### 照做 · Lay 1.2 Exercise 3
Row reduce the matrix to reduced echelon form. Circle the pivot positions in the final matrix and in the original matrix, and list the pivot columns.

$$\begin{bmatrix} 1 & 2 & 3 & 4 \\ 4 & 5 & 6 & 7 \\ 6 & 7 & 8 & 9 \end{bmatrix}$$

#### 解答
往前:$R_2 \leftarrow R_2 - 4R_1$ 得 $[\,0 \;\; {-3} \;\; {-6} \;\; {-9}\,]$;$R_3 \leftarrow R_3 - 6R_1$ 得 $[\,0 \;\; {-5} \;\; {-10} \;\; {-15}\,]$;$R_2 \leftarrow -\tfrac13 R_2$ 得 $[\,0 \;\; 1 \;\; 2 \;\; 3\,]$;$R_3 \leftarrow R_3 + 5R_2$ 得全 0 列。

往回:$R_1 \leftarrow R_1 - 2R_2$ 得 $[\,1 \;\; 0 \;\; {-1} \;\; {-2}\,]$。

$$\text{RREF} = \begin{bmatrix} 1 & 0 & -1 & -2 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

pivot 位置:RREF 與原矩陣都在 $(1,1)$、$(2,2)$。**pivot 行是第 1、2 行**(書後解答相同)。

### 照做 · Lay 1.2 Exercise 4
Row reduce the matrix to reduced echelon form. Circle the pivot positions in the final matrix and in the original matrix, and list the pivot columns.

$$\begin{bmatrix} 1 & 3 & 5 & 7 \\ 3 & 5 & 7 & 9 \\ 5 & 7 & 9 & 1 \end{bmatrix}$$

#### 解答
往前:$R_2 \leftarrow R_2 - 3R_1$ 得 $[\,0 \;\; {-4} \;\; {-8} \;\; {-12}\,]$;$R_3 \leftarrow R_3 - 5R_1$ 得 $[\,0 \;\; {-8} \;\; {-16} \;\; {-34}\,]$;$R_3 \leftarrow R_3 - 2R_2$ 得 $[\,0 \;\; 0 \;\; 0 \;\; {-10}\,]$。

往回:$R_3 \leftarrow -\tfrac{1}{10}R_3$;$R_2 \leftarrow -\tfrac14 R_2$ 得 $[\,0 \;\; 1 \;\; 2 \;\; 3\,]$;$R_2 \leftarrow R_2 - 3R_3$、$R_1 \leftarrow R_1 - 7R_3$;最後 $R_1 \leftarrow R_1 - 3R_2$。

$$\text{RREF} = \begin{bmatrix} 1 & 0 & -1 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

pivot 位置在 $(1,1)$、$(2,2)$、$(3,4)$,**pivot 行是第 1、2、4 行**(第 3 行被跨過去)。

### 是非 · Lay 1.2 Exercise 25
**(T/F)** In some cases, a matrix may be row reduced to more than one matrix in reduced echelon form, using different sequences of row operations.

#### 解答
**False.** Theorem 1:每個矩陣只列等價於唯一一個 RREF。

### 是非 · Lay 1.2 Exercise 26
**(T/F)** The echelon form of a matrix is unique.

#### 解答
**False.** 只有 **reduced** echelon form 是唯一的;一般的梯形可以不同(例如某一列多乘一個倍數)。課本 p. 38。

### 是非 · Lay 1.2 Exercise 27
**(T/F)** The row reduction algorithm applies only to augmented matrices for a linear system.

#### 解答
**False.** 演算法適用於任何矩陣,不管它是不是某個方程組的增廣矩陣(課本 p. 37)。

### 是非 · Lay 1.2 Exercise 28
**(T/F)** The pivot positions in a matrix depend on whether row interchanges are used in the row reduction process.

#### 解答
**False.** pivot 位置由唯一的 RREF 決定,和化簡過程用了哪些列運算(包括有沒有換列)無關(課本 p. 38–39)。

### 是非 · Lay 1.2 Exercise 30
**(T/F)** Reducing a matrix to echelon form is called the *forward phase* of the row reduction process.

#### 解答
**True.** 步驟 1–4 產生梯形,叫前進階段;步驟 5 叫回代階段(課本 p. 42)。

### 變化 · Lay 1.2 Exercise 5
Describe the possible echelon forms of a nonzero $2 \times 2$ matrix. Use the symbols $\blacksquare$, $*$, and $0$, as in the first part of Example 1.

#### 解答
依 pivot 的個數與位置,共三種:

$$\begin{bmatrix} \blacksquare & * \\ 0 & \blacksquare \end{bmatrix},\quad \begin{bmatrix} \blacksquare & * \\ 0 & 0 \end{bmatrix},\quad \begin{bmatrix} 0 & \blacksquare \\ 0 & 0 \end{bmatrix}$$

(題目說 nonzero,所以全 0 矩陣不算。書後解答相同。)

### 變化 · Lay 1.2 Exercise 6
Repeat Exercise 5 for a nonzero $3 \times 2$ matrix.

#### 解答
只有 2 行,最多 2 個 pivot:

$$\begin{bmatrix} \blacksquare & * \\ 0 & \blacksquare \\ 0 & 0 \end{bmatrix},\quad \begin{bmatrix} \blacksquare & * \\ 0 & 0 \\ 0 & 0 \end{bmatrix},\quad \begin{bmatrix} 0 & \blacksquare \\ 0 & 0 \\ 0 & 0 \end{bmatrix}$$

列比行多時,底下至少有一列全 0。

#### 備註
和 Exercise 5 對照可以帶出觀念 5 挑戰題的想法:pivot 個數不會超過列數,也不會超過行數。

## 驗算
```check
Matrix([[0, -3, -6, 4, 9], [-1, -2, -1, 3, 1], [-2, -3, 0, 3, -1], [1, 4, 5, -9, -7]]).rref()[1] == (0, 1, 3)
Matrix([[0, 5, 10, -15, -15]]) - Rational(5, 2)*Matrix([[0, 2, 4, -6, -6]]) == zeros(1, 5)
Matrix([[0, -3, -6, 4, 9]]) + Rational(3, 2)*Matrix([[0, 2, 4, -6, -6]]) == Matrix([[0, 0, 0, -5, 0]])
Matrix([[0, 3, -6, 6, 4, -5], [3, -7, 8, -5, 8, 9], [3, -9, 12, -9, 6, 15]]).rref() == (Matrix([[1, 0, -2, 3, 0, -24], [0, 1, -2, 2, 0, -7], [0, 0, 0, 0, 1, 4]]), (0, 1, 4))
Matrix([[0, 3, -6, 6, 4, -5]]) - Rational(3, 2)*Matrix([[0, 2, -4, 4, 2, -6]]) == Matrix([[0, 0, 0, 0, 1, 4]])
Matrix([[3, -9, 12, -9, 6, 15]]) - 6*Matrix([[0, 0, 0, 0, 1, 4]]) + 9*Matrix([[0, 1, -2, 2, 0, -7]]) == Matrix([[3, 0, -6, 9, 0, -72]])
Matrix([[1, 0, 0, 29], [0, 1, 0, 16], [0, 0, 1, 3]]).rref()[0] == Matrix([[1, 0, 0, 29], [0, 1, 0, 16], [0, 0, 1, 3]])
Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1]]).rref()[0] == Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1]])
Matrix([[1, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]).rref()[0] != Matrix([[1, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
Matrix([[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]).rref()[0] == Matrix([[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
Matrix([[1, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]]).rref()[0] == Matrix([[1, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]])
Matrix([[1, 2, 3, 4], [4, 5, 6, 7], [6, 7, 8, 9]]).rref() == (Matrix([[1, 0, -1, -2], [0, 1, 2, 3], [0, 0, 0, 0]]), (0, 1))
Matrix([[1, 3, 5, 7], [3, 5, 7, 9], [5, 7, 9, 1]]).rref() == (Matrix([[1, 0, -1, 0], [0, 1, 2, 0], [0, 0, 0, 1]]), (0, 1, 3))
```
