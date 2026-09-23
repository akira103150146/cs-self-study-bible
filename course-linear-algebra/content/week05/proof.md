---
after: 2
title_zh: 矩陣乘法為什麼這樣定義
---
## 定理
If $A$ is an $m \times n$ matrix and $B$ is an $n \times p$ matrix with columns $\mathbf{b}_1, \dots, \mathbf{b}_p$, define

$$AB = [\,A\mathbf{b}_1 \;\; A\mathbf{b}_2 \;\; \cdots \;\; A\mathbf{b}_p\,]$$

Then for every $\mathbf{x}$ in $\mathbb{R}^p$,

$$A(B\mathbf{x}) = (AB)\mathbf{x} \tag{1}$$

Moreover, $A(BC) = (AB)C$ whenever the products are defined. (Theorem 2(a))

## 為什麼值得證
學生第一次看到矩陣乘法的規則,幾乎都會問:「為什麼要這樣乘?**為什麼不是逐格相乘就好?**」

答案是:因為我們要它滿足 $(1)$ 式。上週證過「每個線性變換都是矩陣乘法」;那麼「先做 $B$ 再做 $A$」這個合成變換,也應該是某個矩陣。$(1)$ 式就是在說「那個矩陣叫做 $AB$」。

**乘法的定義不是規定,是推出來的。** 這件事一旦想通,後面所有奇怪的性質($AB \ne BA$、沒有消去律、$(AB)^T = B^TA^T$)都有了解釋:它們反映的是「動作的合成」本來就有順序。

順便,結合律 $A(BC) = (AB)C$ 也就跟著成立了——因為函數的合成本來就是結合的:先做 $C$、再做 $B$、再做 $A$,怎麼分組都是同一串動作。

## 關鍵想法
只有三步,而且三步都是前兩週學過的:

1. **$B\mathbf{x}$ 是 $B$ 各行的線性組合**(第 2 週):$B\mathbf{x} = x_1\mathbf{b}_1 + \cdots + x_p\mathbf{b}_p$。
2. **乘以 $A$ 是線性的**(第 4 週):$A$ 可以「鑽進」線性組合裡。
3. **把結果重新讀成矩陣乘向量**:以 $A\mathbf{b}_j$ 為行、$x_j$ 為權重。

第 3 步之後,那個矩陣自己浮出來了——我們只是給它取名叫 $AB$。

## 證明
**第一部分:$(1)$ 式。**

設 $\mathbf{x} = (x_1, \dots, x_p)$。由矩陣乘向量的定義(第 2 週),
$$B\mathbf{x} = x_1\mathbf{b}_1 + \cdots + x_p\mathbf{b}_p$$

左乘 $A$,並用「乘以 $A$ 是線性變換」這個性質(第 4 週的 Theorem 10 之前就證過):
$$A(B\mathbf{x}) = A(x_1\mathbf{b}_1) + \cdots + A(x_p\mathbf{b}_p) = x_1(A\mathbf{b}_1) + \cdots + x_p(A\mathbf{b}_p)$$

右邊是「以 $A\mathbf{b}_1, \dots, A\mathbf{b}_p$ 為行、以 $x_1, \dots, x_p$ 為權重」的線性組合,依同一個定義讀回去:
$$A(B\mathbf{x}) = [\,A\mathbf{b}_1 \;\; \cdots \;\; A\mathbf{b}_p\,]\,\mathbf{x}$$

中括號裡那個矩陣,就是我們定義的 $AB$。所以 $A(B\mathbf{x}) = (AB)\mathbf{x}$。$\blacksquare$

**第二部分:結合律 $A(BC) = (AB)C$。**(課本 p. 128 的第二個證法)

設 $C = [\,\mathbf{c}_1 \;\; \cdots \;\; \mathbf{c}_p\,]$。依乘法的定義,
$$BC = [\,B\mathbf{c}_1 \;\; \cdots \;\; B\mathbf{c}_p\,], \qquad A(BC) = [\,A(B\mathbf{c}_1) \;\; \cdots \;\; A(B\mathbf{c}_p)\,]$$

對每一行用剛證好的 $(1)$ 式($\mathbf{x}$ 取成 $\mathbf{c}_j$):
$$A(B\mathbf{c}_j) = (AB)\mathbf{c}_j$$

所以
$$A(BC) = [\,(AB)\mathbf{c}_1 \;\; \cdots \;\; (AB)\mathbf{c}_p\,] = (AB)C$$

最後一個等號還是同一個定義。$\blacksquare$

**線性用在哪一步?** 只用在第一部分的第二行——把 $A$ 分配進線性組合。這也是為什麼「先平移再旋轉」不能直接寫成兩個 $2 \times 2$ 矩陣相乘:平移不是線性的,這一步就過不去(要等到觀念 6 的齊次座標才繞得過去)。

**課堂上配一個具體例子**:用觀念 2 的例 1($A$ 是 $2 \times 2$、$B$ 是 $2 \times 3$),先算 $B\mathbf{x}$ 再乘 $A$,然後算 $(AB)\mathbf{x}$,兩個答案一樣。學生親手驗過一次,比看證明有感。

**考試怎麼考**:不會要求默寫這個證明。會考的三種變形是——(a) 給兩個小矩陣,分別用 $A(B\mathbf{x})$ 與 $(AB)\mathbf{x}$ 算同一個答案;(b) 問「為什麼 $AB$ 的第 $j$ 行是 $A\mathbf{b}_j$」;(c) 問「為什麼矩陣乘法有結合律但沒有交換律」。
