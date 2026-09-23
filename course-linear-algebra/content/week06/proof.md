---
after: 1
title_zh: 可逆矩陣定理的一段等價鏈
---
## 定理
Let $A$ be a square $n \times n$ matrix. Then the following statements are equivalent:

- **(a)** $A$ is an invertible matrix.
- **(j)** There is an $n \times n$ matrix $C$ such that $CA = I$.
- **(d)** The equation $A\mathbf{x} = \mathbf{0}$ has only the trivial solution.
- **(c)** $A$ has $n$ pivot positions.
- **(b)** $A$ is row equivalent to the $n \times n$ identity matrix.

(Theorem 8 的中央五條;其餘七條由這五條掛上去)

## 為什麼值得證
十二條敘述兩兩互推要 $12 \times 11 = 132$ 次證明。課本只用了**五個箭頭**就把中央五條全部串起來——這個技巧本身比定理更值得學:

> **要證明很多件事等價,不要兩兩互證,把它們排成一個圈。**

繞完一圈,任兩條之間都有路可走。$n$ 條敘述只要 $n$ 個箭頭,不是 $n(n-1)$ 個。

而且這一圈用到的**每一步都是前五週學過的東西**:第 2 週的樞軸與 Theorem 4、第 3 週的自由變數、第 5 週的 Theorem 7 與 Exercises 31、33。證完這個圈,等於把整個前半學期複習了一遍。

## 關鍵想法
圈的走法是

$$\text{(a)} \Rightarrow \text{(j)} \Rightarrow \text{(d)} \Rightarrow \text{(c)} \Rightarrow \text{(b)} \Rightarrow \text{(a)}$$

四個箭頭各靠一件事:

| 箭頭 | 靠什麼 |
|---|---|
| (a) ⇒ (j) | $A^{-1}$ 本身就是那個 $C$ |
| (j) ⇒ (d) | 左乘 $C$ 把 $A\mathbf{x} = \mathbf{0}$ 變成 $\mathbf{x} = \mathbf{0}$(第 5 週 Exercise 31) |
| (d) ⇒ (c) | 沒有自由變數 ⇒ 每一行都是樞軸行(第 5 週 Exercise 33) |
| (c) ⇒ (b) | **方陣**的 $n$ 個樞軸只能排在對角線上 ⇒ RREF 是 $I_n$ |
| (b) ⇒ (a) | 第 5 週的 Theorem 7 |

**「方陣」用在哪裡?** 用在 (c) ⇒ (b) 這一步。$n$ 個樞軸分布在 $n$ 個相異的列與 $n$ 個相異的行——只有行數等於列數時,這兩件事才會同時逼滿。這就是整個定理只對方陣成立的原因。

## 證明
**(a) ⇒ (j)**:若 $A$ 可逆,取 $C = A^{-1}$,則 $CA = A^{-1}A = I$。✓

**(j) ⇒ (d)**:設存在 $C$ 使 $CA = I$。若 $A\mathbf{x} = \mathbf{0}$,兩邊左乘 $C$:
$$C(A\mathbf{x}) = (CA)\mathbf{x} = I\mathbf{x} = \mathbf{x}$$
但同時 $C(A\mathbf{x}) = C\mathbf{0} = \mathbf{0}$。所以 $\mathbf{x} = \mathbf{0}$,只有平凡解。(這正是第 5 週的 Exercise 31。)

**(d) ⇒ (c)**:$A\mathbf{x} = \mathbf{0}$ 只有平凡解 ⇒ **沒有自由變數**(若有自由變數,把它設成 1 就造出非零解)⇒ $A$ 的每一行都是樞軸行 ⇒ 樞軸數 $= n$。(第 5 週的 Exercise 33。)

**(c) ⇒ (b)**:$A$ 是 $n \times n$ 且有 $n$ 個樞軸位置。樞軸在每一列至多一個、每一行至多一個;$n$ 個樞軸要塞進 $n$ 列 $n$ 行,只能**每列恰好一個、每行恰好一個**,而且依階梯形的規則(樞軸位置由左上往右下遞進),它們只能落在主對角線上。把每個樞軸化成 1、上下都消乾淨,最簡列梯形就是 $I_n$。所以 $A \sim I_n$。

**(b) ⇒ (a)**:第 5 週的 Theorem 7 直接給出:$n \times n$ 矩陣與 $I_n$ 列等價 ⇒ $A$ 可逆。$\blacksquare$

**圈完成了**,所以 (a)、(j)、(d)、(c)、(b) 五條互相等價。

**其餘七條怎麼掛上去?**(課本 p. 145,這部分課堂上講過程即可,不必寫完整)

- $\text{(a)} \Rightarrow \text{(k)}$:$A^{-1}$ 就是那個 $D$。$\text{(k)} \Rightarrow \text{(g)}$:第 5 週 Exercise 32。$\text{(g)} \Rightarrow \text{(a)}$:第 5 週 Exercise 34。於是 (k)、(g) 接上圈。
- (g)、(h)、(i) 對**任何**矩陣都等價(第 2 週 Theorem 4、第 4 週 Theorem 12(a)),所以 (h)、(i) 透過 (g) 連上。
- (d)、(e)、(f) 對**任何**矩陣都等價(第 3 週、第 4 週 Theorem 12(b)),所以 (e)、(f) 透過 (d) 連上。
- 最後 (a) ⟺ (l) 由第 5 週 Theorem 6(c)(若 $A$ 可逆則 $A^T$ 可逆,反之亦然)。

**課堂上一定要問的一句話**:「如果 $A$ 是 $4 \times 3$,哪一步會垮?」答案是 (c) ⇒ (b)——3 個樞軸不可能讓 $4 \times 3$ 的矩陣變成方的單位矩陣。這一問可以檢驗學生有沒有真的懂。

**考試怎麼考**:不會要求默寫整個圈。會考的三種變形是——(a) 給兩三條敘述,問怎麼從一條推到另一條(要寫出引用的定理);(b) 問「為什麼 IMT 只對方陣成立」;(c) 給一個具體矩陣,用最少的計算判斷可逆並說明引用哪一條。
