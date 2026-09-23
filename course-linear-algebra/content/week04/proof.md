---
after: 3
title_zh: 每個線性變換都是矩陣乘法
---
## 定理
Let $T : \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation. Then there exists a unique matrix $A$ such that $T(\mathbf{x}) = A\mathbf{x}$ for all $\mathbf{x}$ in $\mathbb{R}^n$. In fact, $A$ is the $m \times n$ matrix whose $j$th column is the vector $T(\mathbf{e}_j)$:

$$A = [\,T(\mathbf{e}_1) \;\; \cdots \;\; T(\mathbf{e}_n)\,]$$

(Theorem 10)

## 為什麼值得證
這個定理把兩個世界接起來:**「性質」的世界**(線性變換:保持加法與純量倍數)和**「計算」的世界**(矩陣乘法)。證完之後,任何用文字描述的線性變換——旋轉、反射、投影、剪切——都可以立刻寫成一個矩陣,交給電腦算。

它也解釋了為什麼整學期都在算矩陣:因為 $\mathbb{R}^n \to \mathbb{R}^m$ 的線性變換**就是**矩陣,沒有別的。

## 關鍵想法
只要兩步:

1. **任何 $\mathbf{x}$ 都能拆成 $\mathbf{e}_j$ 的組合**:$\mathbf{x} = x_1\mathbf{e}_1 + \cdots + x_n\mathbf{e}_n$(這就是 $I_n\mathbf{x} = \mathbf{x}$)。
2. **線性讓 $T$ 可以「鑽進去」**:$T$ 作用在組合上,等於分別作用再組合(觀念 2 的性質 5)。

於是 $T(\mathbf{x})$ 變成「以 $T(\mathbf{e}_j)$ 為行、以 $x_j$ 為權重」的線性組合——而這正是矩陣乘向量的定義(第 2 週)。

## 證明
**存在性。** 把 $\mathbf{x}$ 用單位矩陣拆開:
$$\mathbf{x} = I_n\mathbf{x} = [\,\mathbf{e}_1 \;\; \cdots \;\; \mathbf{e}_n\,]\mathbf{x} = x_1\mathbf{e}_1 + \cdots + x_n\mathbf{e}_n$$

用 $T$ 的線性(性質 5):
$$T(\mathbf{x}) = T(x_1\mathbf{e}_1 + \cdots + x_n\mathbf{e}_n) = x_1T(\mathbf{e}_1) + \cdots + x_nT(\mathbf{e}_n)$$

右邊是以 $T(\mathbf{e}_1), \dots, T(\mathbf{e}_n)$ 為行、$x_1, \dots, x_n$ 為權重的線性組合,依 $A\mathbf{x}$ 的定義:
$$= [\,T(\mathbf{e}_1) \;\; \cdots \;\; T(\mathbf{e}_n)\,]\begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix} = A\mathbf{x}$$

**唯一性**(Exercise 41)。假設還有一個矩陣 $B$ 也滿足 $T(\mathbf{x}) = B\mathbf{x}$ 對所有 $\mathbf{x}$ 成立。取 $\mathbf{x} = \mathbf{e}_j$:
$$B\mathbf{e}_j = T(\mathbf{e}_j) = A \text{ 的第 } j \text{ 行}$$
而 $B\mathbf{e}_j$ 正是 $B$ 的第 $j$ 行(權重只有第 $j$ 個是 1)。每一行都相同,所以 $A = B$。$\blacksquare$

**線性用在哪一步?** 只用在第二行——把 $T$ 分配進線性組合。沒有線性,這一步就垮了;這也是為什麼「平移」(不是線性)寫不成純粹的矩陣乘法。

**課堂上用觀念 3 例 1 當具體例子**:只知道 $T(\mathbf{e}_1) = (5, -7, 2)$、$T(\mathbf{e}_2) = (-3, 8, 0)$,就能寫出整個 $T$。考試不會要求寫出這個證明,會考「給你 $T(\mathbf{e}_1)$、$T(\mathbf{e}_2)$,寫出標準矩陣」或「為什麼平移不是矩陣變換」。
