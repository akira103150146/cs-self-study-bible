---
after: 2
title_zh: Ax = b 的解集 = 特解 + 齊次解
---
## 定理
Suppose the equation $A\mathbf{x} = \mathbf{b}$ is consistent for some given $\mathbf{b}$, and let $\mathbf{p}$ be a solution. Then the solution set of $A\mathbf{x} = \mathbf{b}$ is the set of all vectors of the form $\mathbf{w} = \mathbf{p} + \mathbf{v}_h$, where $\mathbf{v}_h$ is any solution of the homogeneous equation $A\mathbf{x} = \mathbf{0}$. (Theorem 6)

## 為什麼值得證
這個定理把「解有無限多個」這件事變得有結構:所有解都是**同一個特解**加上**齊次方程的解**。從此只要解一次齊次方程,換任何右邊 $\mathbf{b}$,只需要再找一個特解就好。

證明本身也是一個重要的示範:要證明「兩個集合相等」,就要證明**兩個方向的包含**。

## 關鍵想法
兩個集合:$S$ = $A\mathbf{x} = \mathbf{b}$ 的所有解;$T$ = 所有形如 $\mathbf{p} + \mathbf{v}_h$ 的向量。要證 $S = T$,分兩步:

- $T \subseteq S$:每個 $\mathbf{p} + \mathbf{v}_h$ 都是解。
- $S \subseteq T$:每個解都能寫成 $\mathbf{p} + \mathbf{v}_h$。

兩步用的工具只有一個:上週的 Theorem 5,$A(\mathbf{u} \pm \mathbf{v}) = A\mathbf{u} \pm A\mathbf{v}$。

## 證明
已知 $A\mathbf{p} = \mathbf{b}$。

**第一步:$\mathbf{p} + \mathbf{v}_h$ 一定是解**(Practice Problem 3)。設 $\mathbf{v}_h$ 是任一個齊次解,即 $A\mathbf{v}_h = \mathbf{0}$。由 Theorem 5,
$$A(\mathbf{p} + \mathbf{v}_h) = A\mathbf{p} + A\mathbf{v}_h = \mathbf{b} + \mathbf{0} = \mathbf{b}.$$
所以 $\mathbf{p} + \mathbf{v}_h$ 是 $A\mathbf{x} = \mathbf{b}$ 的解。

**第二步:每個解都長這樣**(Exercise 37)。設 $\mathbf{w}$ 是 $A\mathbf{x} = \mathbf{b}$ 的任一個解,即 $A\mathbf{w} = \mathbf{b}$。**定義** $\mathbf{v}_h = \mathbf{w} - \mathbf{p}$。由 Theorem 5,
$$A\mathbf{v}_h = A(\mathbf{w} - \mathbf{p}) = A\mathbf{w} - A\mathbf{p} = \mathbf{b} - \mathbf{b} = \mathbf{0}.$$
所以 $\mathbf{v}_h$ 是齊次解,而且 $\mathbf{w} = \mathbf{p} + (\mathbf{w} - \mathbf{p}) = \mathbf{p} + \mathbf{v}_h$,正是定理說的形式。

兩個方向都成立,所以 $A\mathbf{x} = \mathbf{b}$ 的解集恰好是 $\{\mathbf{p} + \mathbf{v}_h : A\mathbf{v}_h = \mathbf{0}\}$。$\blacksquare$

**「相容」這個前提用在哪裡?** 在一開始:需要**有**一個解 $\mathbf{p}$ 才能出發。無解時沒有 $\mathbf{p}$,解集是空集合。

**課堂上用觀念 2 例 1 對照**:$\mathbf{p} = (-1, 2, 0)$、齊次解 $t(\tfrac43, 0, 1)$,正好一個是特解、一個是齊次解。考試不會要求寫出完整證明,會考「第二步為什麼要定義 $\mathbf{v}_h = \mathbf{w} - \mathbf{p}$」這類題目,或直接套用:「已知一個解和齊次解集,寫出全部的解」。
