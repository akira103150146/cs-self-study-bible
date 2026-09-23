---
title_en: Transformations and Matrix Transformations
title_zh: 把矩陣看成一台機器:變換、定義域、值域
sub: x ↦ Ax turns one vector into another
level: basic
source: Lay 1.8
lab_hook: '`A @ x` 就是 $T(\mathbf{x})$;`A.shape` 告訴你定義域與對應域是 ℝⁿ、ℝᵐ'
---
## 觀念
A matrix equation $A\mathbf{x} = \mathbf{b}$ can arise in a way that is not directly connected with linear combinations of vectors. This happens when we think of the matrix $A$ as an object that "acts" on a vector $\mathbf{x}$ by multiplication to produce a new vector called $A\mathbf{x}$.

A **transformation** (or **function** or **mapping**) $T$ from $\mathbb{R}^n$ to $\mathbb{R}^m$ is a rule that assigns to each vector $\mathbf{x}$ in $\mathbb{R}^n$ a vector $T(\mathbf{x})$ in $\mathbb{R}^m$. The set $\mathbb{R}^n$ is called the **domain** of $T$, and $\mathbb{R}^m$ is called the **codomain** of $T$. The notation $T : \mathbb{R}^n \to \mathbb{R}^m$ indicates that the domain of $T$ is $\mathbb{R}^n$ and the codomain is $\mathbb{R}^m$. For $\mathbf{x}$ in $\mathbb{R}^n$, the vector $T(\mathbf{x})$ in $\mathbb{R}^m$ is called the **image** of $\mathbf{x}$ (under the action of $T$). The set of all images $T(\mathbf{x})$ is called the **range** of $T$.

**Matrix transformations.** For each $\mathbf{x}$ in $\mathbb{R}^n$, $T(\mathbf{x})$ is computed as $A\mathbf{x}$, where $A$ is an $m \times n$ matrix. We sometimes denote such a *matrix transformation* by $\mathbf{x} \mapsto A\mathbf{x}$. The domain of $T$ is $\mathbb{R}^n$ when $A$ has $n$ columns, and the codomain of $T$ is $\mathbb{R}^m$ when each column of $A$ has $m$ entries. The range of $T$ is the set of all linear combinations of the columns of $A$, because each image $T(\mathbf{x})$ is of the form $A\mathbf{x}$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| transformation / mapping | 變換 / 對應 | 一條規則:丟進一個向量,吐出一個向量 |
| domain | 定義域 | 可以丟進去的向量所在的空間 ℝⁿ($A$ 的**行數**) |
| codomain | 對應域 | 吐出來的向量所在的空間 ℝᵐ($A$ 的**列數**) |
| image of $\mathbf{x}$ | $\mathbf{x}$ 的像 | $T(\mathbf{x})$,丟進 $\mathbf{x}$ 吐出來的那個向量 |
| range | 值域 | **所有**的像收集起來;等於 $A$ 各行的 Span |
| $\mathbf{x} \mapsto A\mathbf{x}$ | $\mathbf{x}$ 對應到 $A\mathbf{x}$ | 矩陣變換的簡寫;$\mapsto$ 唸作 maps to |
| projection | 投影 | 把點壓到某個平面或直線上 |
| shear transformation | 剪切變換 | 把方形推歪成平行四邊形 |

## 白話說
前三週把矩陣當成「一組方程式的係數」。這週換個角度:**矩陣是一台機器**,丟進向量 $\mathbf{x}$,吐出向量 $A\mathbf{x}$。

- **定義域**:機器吃得下什麼(ℝⁿ,$n$ = $A$ 的行數)。
- **對應域**:機器吐出來的東西住在哪(ℝᵐ,$m$ = $A$ 的列數)。
- **值域**:機器**真正吐得出來**的所有東西——通常只是對應域的一部分。

值域和對應域的差別是這個觀念最容易混淆的地方:對應域是「可能的規格」,值域是「實際做得到的」。而值域就是 $A$ 各行的 **Span**(第 2 週),所以「$\mathbf{c}$ 在不在值域裡?」又是老問題:$A\mathbf{x} = \mathbf{c}$ 有沒有解。

**兩個老問題換上新語言**:

- 「$\mathbf{b}$ 是不是**唯一**一個 $\mathbf{x}$ 的像?」= 唯一性問題。
- 「$\mathbf{c}$ 在不在值域裡?」= 存在性問題。

## 幾何意義
矩陣變換可以「看得見」。剪切 $A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$ 把正方形推成平行四邊形——底邊固定不動,頂邊往右滑:

![課本 Figure 4:2 × 2 的正方形經過剪切變換後成為平行四邊形,u = (0, 2) 的像是 (4, 2)。](shear.svg)

投影 $A = \operatorname{diag}(1, 1, 0)$ 則把 ℝ³ 的點垂直壓到 $x_1x_2$ 平面上(課本 Figure 3):第三個分量被歸零。

## 在資工哪裡用
- **圖學的每一個動作**:旋轉、縮放、鏡射、剪切,都是一個矩陣乘上座標向量。遊戲引擎每一格畫面都在做幾百萬次 $A\mathbf{x}$。
- **投影**:3D 場景畫到 2D 螢幕,就是一個投影變換;陰影、反射也是。
- **神經網路的一層**:$\mathbf{x} \mapsto W\mathbf{x} + \mathbf{b}$。前半段就是矩陣變換(加上 $\mathbf{b}$ 的部分見觀念 2 的 Exercise 38:那叫仿射變換,不是線性的)。
- **值域 = 能力上限**:一個線性層「吐得出來」的向量只有 $W$ 各行的 Span。想輸出更多方向,就要更大的秩(第 7 週)。

## 原理
**為什麼值域就是各行的 Span?** 每個像都長成 $A\mathbf{x} = x_1\mathbf{a}_1 + \cdots + x_n\mathbf{a}_n$(第 2 週的定義),也就是各行的線性組合;反過來,每個線性組合也都是某個 $\mathbf{x}$ 的像。所以「值域 = $\operatorname{Span}\{\mathbf{a}_1, \dots, \mathbf{a}_n\}$」。

**三個問題,一套方法**:

| 問題 | 翻成方程式 | 怎麼判斷 |
|---|---|---|
| 求 $\mathbf{u}$ 的像 | 算 $A\mathbf{u}$ | 直接乘 |
| 哪個 $\mathbf{x}$ 的像是 $\mathbf{b}$ | 解 $A\mathbf{x} = \mathbf{b}$ | 化簡 $[\,A \;\; \mathbf{b}\,]$ |
| $\mathbf{c}$ 在值域裡嗎 | $A\mathbf{x} = \mathbf{c}$ 有解嗎 | 看最後一行是不是 pivot 行 |

## 老師講解
### 例 1 · Lay 1.8 Example 1
Let $A = \begin{bmatrix} 1 & -3 \\ 3 & 5 \\ -1 & 7 \end{bmatrix}$, $\mathbf{u} = \begin{bmatrix} 2 \\ -1 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} 3 \\ 2 \\ -5 \end{bmatrix}$, $\mathbf{c} = \begin{bmatrix} 3 \\ 2 \\ 5 \end{bmatrix}$, and define a transformation $T : \mathbb{R}^2 \to \mathbb{R}^3$ by $T(\mathbf{x}) = A\mathbf{x}$.

- **a.** Find $T(\mathbf{u})$, the image of $\mathbf{u}$ under the transformation $T$.
- **b.** Find an $\mathbf{x}$ in $\mathbb{R}^2$ whose image under $T$ is $\mathbf{b}$.
- **c.** Is there more than one $\mathbf{x}$ whose image under $T$ is $\mathbf{b}$?
- **d.** Determine if $\mathbf{c}$ is in the range of the transformation $T$.

1. **先確認形狀**:$A$ 是 $3 \times 2$,所以 $T : \mathbb{R}^2 \to \mathbb{R}^3$(吃 2 個分量、吐 3 個分量)。寫成公式:
   $$T(\mathbf{x}) = A\mathbf{x} = \begin{bmatrix} x_1 - 3x_2 \\ 3x_1 + 5x_2 \\ -x_1 + 7x_2 \end{bmatrix}$$
2. **(a) 求像就是直接乘**:$T(\mathbf{u}) = A\mathbf{u} = \begin{bmatrix} 2 + 3 \\ 6 - 5 \\ -2 - 7 \end{bmatrix} = \begin{bmatrix} 5 \\ 1 \\ -9 \end{bmatrix}$。
3. **(b) 反過來問「誰的像是 $\mathbf{b}$」就是解方程組**:化簡 $[\,A \;\; \mathbf{b}\,]$:
   $$\begin{bmatrix} 1 & -3 & 3 \\ 3 & 5 & 2 \\ -1 & 7 & -5 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 3 \\ 0 & 14 & -7 \\ 0 & 4 & -2 \end{bmatrix} \sim \begin{bmatrix} 1 & 0 & 1.5 \\ 0 & 1 & -.5 \\ 0 & 0 & 0 \end{bmatrix}$$
   得 $\mathbf{x} = (1.5, -.5)$。
4. **(c) 唯一嗎?** 兩行都是 pivot 行,沒有自由變數 → 解唯一 → 只有**一個** $\mathbf{x}$ 的像是 $\mathbf{b}$。這是**唯一性**問題。
5. **(d) $\mathbf{c}$ 在值域裡嗎?** 就是問 $A\mathbf{x} = \mathbf{c}$ 相不相容。化簡 $[\,A \;\; \mathbf{c}\,]$:
   $$\begin{bmatrix} 1 & -3 & 3 \\ 3 & 5 & 2 \\ -1 & 7 & 5 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 3 \\ 0 & 14 & -7 \\ 0 & 4 & 8 \end{bmatrix} \sim \begin{bmatrix} 1 & -3 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & -35 \end{bmatrix}$$
   第三列是 $0 = -35$,無解 → $\mathbf{c}$ **不在**值域裡。這是**存在性**問題。
6. **回顧**:(b)(c) 是第 1 週的唯一性、(d) 是第 2 週的存在性,只是換成「像」和「值域」的說法。

### 例 2 · Lay 1.8 Examples 2–3
If $A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$, then the transformation $\mathbf{x} \mapsto A\mathbf{x}$ *projects* points in $\mathbb{R}^3$ onto the $x_1x_2$-plane. Let $A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$. The transformation $T : \mathbb{R}^2 \to \mathbb{R}^2$ defined by $T(\mathbf{x}) = A\mathbf{x}$ is called a **shear transformation**. Find the images of $\mathbf{u} = \begin{bmatrix} 0 \\ 2 \end{bmatrix}$ and $\begin{bmatrix} 2 \\ 2 \end{bmatrix}$.

1. **投影**:$\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} \mapsto \begin{bmatrix} x_1 \\ x_2 \\ 0 \end{bmatrix}$。第三個分量被歸零,所有點都被壓到 $x_1x_2$ 平面上(課本 Figure 3)。
2. **投影的值域**:$A$ 三行的 Span 是 $x_1x_2$ 平面,只是 ℝ³ 的一部分——對應域是 ℝ³,值域只是一個平面。
3. **剪切**:$T(\mathbf{u}) = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 0 \\ 2 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}$,$\begin{bmatrix} 2 \\ 2 \end{bmatrix} \mapsto \begin{bmatrix} 6 \\ 2 \end{bmatrix}$。
4. **看規律**:第二個分量不變($x_2$),第一個分量加上 $2x_2$——**越高的點被推得越遠**,底邊($x_2 = 0$)完全不動。
5. **為什麼正方形會變成平行四邊形?** 因為 $T$ 把線段對應到線段(觀念 2 的 Exercise 35),所以只要算四個頂點的像:$(0,0) \mapsto (0,0)$、$(2,0) \mapsto (2,0)$、$(2,2) \mapsto (6,2)$、$(0,2) \mapsto (4,2)$(見「幾何意義」的圖)。
6. **應用**:剪切出現在物理、地質與結晶學;在圖學裡則是製造「斜體字」效果的變換。

## 易錯點
- 把**對應域**和**值域**混為一談。對應域是 ℝᵐ,值域可能只是其中一小塊(是非題 Exercises 24、25)。
- 定義域看錯:$3 \times 5$ 的矩陣,定義域是 **ℝ⁵**(行數),不是 ℝ³(是非題 Exercise 23)。
- 把「求 $\mathbf{u}$ 的像」和「求像是 $\mathbf{b}$ 的 $\mathbf{x}$」弄反:前者是乘法,後者是解方程組。
- 問「$\mathbf{c}$ 在不在值域」時忘了要把 $\mathbf{c}$ 放進增廣矩陣。

## 教學提示
一開始就把「機器」的比喻畫在黑板上:左邊一個框寫 ℝⁿ(定義域),右邊一個框寫 ℝᵐ(對應域),框裡再畫一小塊寫「值域」。整週都用這張圖。

例 1 的四小題要逐一標出「這是乘法」「這是解方程組」「這是唯一性」「這是存在性」。學生最容易在 (d) 忘記要化簡增廣矩陣。

課堂建議做:Exercises 1、3、7;是非 Exercises 23–25;Exercises 13 與 15 畫圖。T 題(Exercises 45–48)留給實作課。

## 練習
### 照做 · Lay 1.8 Exercises 1–2
Find the images under $T$.

(1) Let $A = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}$, and define $T : \mathbb{R}^2 \to \mathbb{R}^2$ by $T(\mathbf{x}) = A\mathbf{x}$. Find the images under $T$ of $\mathbf{u} = \begin{bmatrix} 1 \\ -3 \end{bmatrix}$ and $\mathbf{v} = \begin{bmatrix} a \\ b \end{bmatrix}$.

(2) Let $A = \begin{bmatrix} .5 & 0 & 0 \\ 0 & .5 & 0 \\ 0 & 0 & .5 \end{bmatrix}$, $\mathbf{u} = \begin{bmatrix} 1 \\ 0 \\ -4 \end{bmatrix}$, and $\mathbf{v} = \begin{bmatrix} a \\ b \\ c \end{bmatrix}$. Define $T : \mathbb{R}^3 \to \mathbb{R}^3$ by $T(\mathbf{x}) = A\mathbf{x}$. Find $T(\mathbf{u})$ and $T(\mathbf{v})$.

#### 解答
(1) $T(\mathbf{u}) = \begin{bmatrix} 2 \\ -6 \end{bmatrix}$、$T(\mathbf{v}) = \begin{bmatrix} 2a \\ 2b \end{bmatrix}$(書後解答相同)。$T$ 就是伸縮 $\mathbf{x} \mapsto 2\mathbf{x}$:每個向量拉長兩倍。

(2) $T(\mathbf{u}) = \begin{bmatrix} .5 \\ 0 \\ -2 \end{bmatrix}$、$T(\mathbf{v}) = \begin{bmatrix} .5a \\ .5b \\ .5c \end{bmatrix}$。$T$ 是收縮 $\mathbf{x} \mapsto .5\mathbf{x}$。

### 照做 · Lay 1.8 Exercises 3–6
With $T$ defined by $T(\mathbf{x}) = A\mathbf{x}$, find a vector $\mathbf{x}$ whose image under $T$ is $\mathbf{b}$, and determine whether $\mathbf{x}$ is unique.

(3) $A = \begin{bmatrix} 1 & 0 & -2 \\ -2 & 1 & 6 \\ 3 & -2 & -5 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} -1 \\ 7 \\ -3 \end{bmatrix}$  (4) $A = \begin{bmatrix} 1 & -3 & 2 \\ 0 & 1 & -4 \\ 3 & -5 & -9 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} 6 \\ -7 \\ -9 \end{bmatrix}$

(5) $A = \begin{bmatrix} 1 & -5 & -7 \\ -3 & 7 & 5 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} -2 \\ -2 \end{bmatrix}$  (6) $A = \begin{bmatrix} 1 & -2 & 1 \\ 3 & -4 & 5 \\ 0 & 1 & 1 \\ -3 & 5 & -4 \end{bmatrix}$, $\mathbf{b} = \begin{bmatrix} 1 \\ 9 \\ 3 \\ -6 \end{bmatrix}$

#### 解答
都是解 $A\mathbf{x} = \mathbf{b}$;**唯一** ⇔ 每一行都是 pivot 行(沒有自由變數)。

(3) $[\,A \;\; \mathbf{b}\,]$ 化簡後是 $\begin{bmatrix} 1 & 0 & 0 & 3 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 2 \end{bmatrix}$,$\mathbf{x} = (3, 1, 2)$,**唯一**(書後解答相同)。

(4) $\mathbf{x} = (-5, -3, 1)$,三行都是 pivot 行,**唯一**。

(5) 化簡得 $\begin{bmatrix} 1 & 0 & 3 & 3 \\ 0 & 1 & 2 & 1 \end{bmatrix}$:$x_3$ 自由,取 $x_3 = 0$ 得 $\mathbf{x} = (3, 1, 0)$,**不唯一**(書後解答相同)。一般解 $\mathbf{x} = (3, 1, 0) + x_3(-3, -2, 1)$。

(6) 化簡得 $\begin{bmatrix} 1 & 0 & 3 & 7 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$:取 $x_3 = 0$ 得 $\mathbf{x} = (7, 3, 0)$,**不唯一**。

### 照做 · Lay 1.8 Exercises 7–8
(7) Let $A$ be a $4 \times 6$ matrix. What must $a$ and $b$ be in order to define $T : \mathbb{R}^a \to \mathbb{R}^b$ by $T(\mathbf{x}) = A\mathbf{x}$? (8) How many rows and columns must a matrix $A$ have in order to define a mapping from $\mathbb{R}^3$ into $\mathbb{R}^6$ by the rule $T(\mathbf{x}) = A\mathbf{x}$?

#### 解答
(7) $a = 6$(定義域的維度 = $A$ 的**行數**)、$b = 4$(對應域的維度 = $A$ 的**列數**)(書後解答相同)。

(8) $A$ 要是 $6 \times 3$:3 行(才吃得下 ℝ³ 的向量)、6 列(吐出來才在 ℝ⁶)。

### 照做 · Lay 1.8 Practice Problem 1
Suppose $T : \mathbb{R}^5 \to \mathbb{R}^2$ and $T(\mathbf{x}) = A\mathbf{x}$ for some matrix $A$ and for each $\mathbf{x}$ in $\mathbb{R}^5$. How many rows and columns does $A$ have?

#### 解答
$A$ 要有 **5 行**($A\mathbf{x}$ 才有定義)、**2 列**(對應域才是 ℝ²),也就是 $2 \times 5$(課本 p. 99)。

### 是非 · Lay 1.8 Exercise 23
**(T/F)** If $A$ is a $3 \times 5$ matrix and $T$ is a transformation defined by $T(\mathbf{x}) = A\mathbf{x}$, then the domain of $T$ is $\mathbb{R}^3$.

#### 解答
**False.** $A\mathbf{x}$ 要求 $\mathbf{x}$ 有 5 個分量,所以定義域是 **ℝ⁵**;ℝ³ 是對應域。

### 是非 · Lay 1.8 Exercise 24
**(T/F)** The codomain of the transformation $\mathbf{x} \mapsto A\mathbf{x}$ is the set of all linear combinations of the columns of $A$.

#### 解答
**False.** 那是**值域**。對應域是 ℝᵐ($A$ 的列數),可能比值域大。

### 是非 · Lay 1.8 Exercise 25
**(T/F)** If $A$ is an $m \times n$ matrix, then the range of the transformation $\mathbf{x} \mapsto A\mathbf{x}$ is $\mathbb{R}^m$.

#### 解答
**False.** 值域是各行的 Span,只有在「每一列都有 pivot」時才等於 ℝᵐ(第 2 週 Theorem 4)。反例:$A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ 的值域只是 ℝ² 裡的一條直線。

### 是非 · Lay 1.8 Exercise 26
**(T/F)** If $T : \mathbb{R}^n \to \mathbb{R}^m$ is a linear transformation and if $\mathbf{c}$ is in $\mathbb{R}^m$, then a uniqueness question is "Is $\mathbf{c}$ in the range of $T$?"

#### 解答
**False.** 「$\mathbf{c}$ 在不在值域裡」問的是「**存不存在** $\mathbf{x}$ 使 $T(\mathbf{x}) = \mathbf{c}$」,是**存在性**問題(例 1(d))。唯一性問題問的是「這樣的 $\mathbf{x}$ 是不是只有一個」(例 1(c))。

### 變化 · Lay 1.8 Exercises 9–10
Find all $\mathbf{x}$ in $\mathbb{R}^4$ that are mapped into the zero vector by the transformation $\mathbf{x} \mapsto A\mathbf{x}$ for the given matrix $A$.

(9) $A = \begin{bmatrix} 1 & -4 & 7 & -5 \\ 0 & 1 & -4 & 3 \\ 2 & -6 & 6 & -4 \end{bmatrix}$  (10) $A = \begin{bmatrix} 1 & 3 & 9 & 2 \\ 1 & 0 & 3 & -4 \\ 0 & 1 & 2 & 3 \\ -2 & 3 & 0 & 5 \end{bmatrix}$

#### 解答
就是解齊次方程組(第 3 週觀念 1)。

(9) $A \sim \begin{bmatrix} 1 & 0 & -9 & 7 \\ 0 & 1 & -4 & 3 \\ 0 & 0 & 0 & 0 \end{bmatrix}$,$x_3, x_4$ 自由:
$$\mathbf{x} = x_3\begin{bmatrix} 9 \\ 4 \\ 1 \\ 0 \end{bmatrix} + x_4\begin{bmatrix} -7 \\ -3 \\ 0 \\ 1 \end{bmatrix}$$
(書後解答相同)。

(10) $A \sim \begin{bmatrix} 1 & 0 & 3 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \end{bmatrix}$:$x_4 = 0$、$x_3$ 自由,$\mathbf{x} = x_3(-3, -2, 1, 0)$。

### 變化 · Lay 1.8 Exercises 11–12
(11) Let $\mathbf{b} = \begin{bmatrix} -1 \\ 1 \\ 0 \end{bmatrix}$, and let $A$ be the matrix in Exercise 9. Is $\mathbf{b}$ in the range of the linear transformation $\mathbf{x} \mapsto A\mathbf{x}$? Why or why not?

(12) Let $\mathbf{b} = \begin{bmatrix} -1 \\ 3 \\ -1 \\ 4 \end{bmatrix}$, and let $A$ be the matrix in Exercise 10. Is $\mathbf{b}$ in the range of the linear transformation $\mathbf{x} \mapsto A\mathbf{x}$? Why or why not?

#### 解答
(11) **是**。$[\,A \;\; \mathbf{b}\,]$ 化簡後最後一行不是 pivot 行(方程組相容),所以 $\mathbf{b}$ 是某個 $\mathbf{x}$ 的像,例如 $\mathbf{x} = (3, 1, 0, 0)$(書後解答:因為 $[\,A \;\; \mathbf{b}\,]$ 代表的方程組相容)。

(12) **不是**。$[\,A \;\; \mathbf{b}\,]$ 化簡後最後一列是 $0 = 1$,無解,所以沒有任何 $\mathbf{x}$ 的像是 $\mathbf{b}$。

### 變化 · Lay 1.8 Exercises 13–16
Use a rectangular coordinate system to plot $\mathbf{u} = \begin{bmatrix} 5 \\ 2 \end{bmatrix}$, $\mathbf{v} = \begin{bmatrix} -2 \\ 4 \end{bmatrix}$, and their images under the given transformation $T$. (Make a separate and reasonably large sketch for each exercise.) Describe geometrically what $T$ does to each vector $\mathbf{x}$ in $\mathbb{R}^2$.

(13) $T(\mathbf{x}) = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$  (14) $T(\mathbf{x}) = \begin{bmatrix} .5 & 0 \\ 0 & .5 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$

(15) $T(\mathbf{x}) = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$  (16) $T(\mathbf{x}) = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$

#### 解答
(13) $T(\mathbf{u}) = (-5, -2)$、$T(\mathbf{v}) = (2, -4)$。$T(\mathbf{x}) = -\mathbf{x}$:**對原點的反射**(也就是旋轉 180°)(書後解答的圖說:a reflection through the origin)。

(14) $T(\mathbf{u}) = (2.5, 1)$、$T(\mathbf{v}) = (-1, 2)$。$T(\mathbf{x}) = .5\mathbf{x}$:**收縮**成一半長度,方向不變。

(15) $T(\mathbf{u}) = (0, 2)$、$T(\mathbf{v}) = (0, 4)$。$T(x_1, x_2) = (0, x_2)$:**投影到 $x_2$ 軸**(書後解答的圖說:a projection onto the $x_2$-axis)。

(16) $T(\mathbf{u}) = (2, 5)$、$T(\mathbf{v}) = (4, -2)$。$T(x_1, x_2) = (x_2, x_1)$:**對直線 $x_2 = x_1$ 的反射**。

#### 備註
這四題的變換都會在觀念 4 的表格裡再出現一次。學生畫圖時提醒:箭頭要從原點出發。

### 變化 · Lay 1.8 Practice Problem 2
Let $A = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$. Give a geometric description of the transformation $\mathbf{x} \mapsto A\mathbf{x}$.

#### 解答
在方格紙上隨便點幾個點看看:$(4, 1) \mapsto (4, -1)$。$T(x_1, x_2) = (x_1, -x_2)$,這是**對 $x_1$ 軸的反射**(課本 p. 99)。

### 應用 · Lay 1.8 Exercises 45–46
**[T]** The given matrix determines a linear transformation $T$. Find all $\mathbf{x}$ such that $T(\mathbf{x}) = \mathbf{0}$.

(45) $\begin{bmatrix} 4 & -2 & 5 & -5 \\ -9 & 7 & -8 & 0 \\ -6 & 4 & 5 & 3 \\ 5 & -3 & 8 & -4 \end{bmatrix}$  (46) $\begin{bmatrix} -9 & -4 & -9 & 4 \\ 5 & -8 & -7 & 6 \\ 7 & 11 & 16 & -9 \\ 9 & -7 & -4 & 5 \end{bmatrix}$

#### 解答
(45) 化簡得 $\begin{bmatrix} 1 & 0 & 0 & -7/2 \\ 0 & 1 & 0 & -9/2 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$:$\mathbf{x} = x_4\left(\tfrac72, \tfrac92, 0, 1\right)$,也就是 $(7, 9, 0, 2)$ 的所有倍數(書後解答相同)。

(46) 化簡得 $\begin{bmatrix} 1 & 0 & 0 & 3/4 \\ 0 & 1 & 0 & 5/4 \\ 0 & 0 & 1 & -7/4 \\ 0 & 0 & 0 & 0 \end{bmatrix}$:$\mathbf{x}$ 是 $(-3, -5, 7, 4)$ 的所有倍數。

#### 備註
課本標 T,實作課用 `nullspace()` 做。

### 應用 · Lay 1.8 Exercises 47–48
**[T]** (47) Let $\mathbf{b} = \begin{bmatrix} 7 \\ 5 \\ 9 \\ 7 \end{bmatrix}$ and let $A$ be the matrix in Exercise 45. Is $\mathbf{b}$ in the range of the transformation $\mathbf{x} \mapsto A\mathbf{x}$? If so, find an $\mathbf{x}$ whose image under the transformation is $\mathbf{b}$.

(48) Let $\mathbf{b} = \begin{bmatrix} -7 \\ -7 \\ 13 \\ -5 \end{bmatrix}$ and let $A$ be the matrix in Exercise 46. Is $\mathbf{b}$ in the range of the transformation $\mathbf{x} \mapsto A\mathbf{x}$? If so, find an $\mathbf{x}$ whose image under the transformation is $\mathbf{b}$.

#### 解答
(47) **是**。$[\,A \;\; \mathbf{b}\,]$ 相容,取 $x_4 = 0$ 得 $\mathbf{x} = (4, 7, 1, 0)$(書後解答相同)。一般解再加上 Exercise 45 的齊次解。

(48) **是**。取 $x_4 = 0$ 得 $\mathbf{x} = \left(-\tfrac54, -\tfrac{11}4, \tfrac{13}4, 0\right)$;取 $x_4 = 1$ 則有整數解 $\mathbf{x} = (-2, -4, 5, 1)$。

## 驗算
```check
Matrix([[1, -3], [3, 5], [-1, 7]]) * Matrix([2, -1]) == Matrix([5, 1, -9])
Matrix([[1, -3, 3], [3, 5, 2], [-1, 7, -5]]).rref()[0] == Matrix([[1, 0, Rational(3, 2)], [0, 1, Rational(-1, 2)], [0, 0, 0]])
3 in Matrix([[1, -3, 3], [3, 5, 2], [-1, 7, 5]]).rref()[1] or 2 in Matrix([[1, -3, 3], [3, 5, 2], [-1, 7, 5]]).rref()[1]
Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]]) * Matrix([x1, x2, x3]) == Matrix([x1, x2, 0])
Matrix([[1, 2], [0, 1]]) * Matrix([[0, 2, 2, 0], [0, 0, 2, 2]]) == Matrix([[0, 2, 6, 4], [0, 0, 2, 2]])
Matrix([[2, 0], [0, 2]]) * Matrix([a, b]) == Matrix([2*a, 2*b])
Rational(1, 2) * eye(3) * Matrix([1, 0, -4]) == Matrix([Rational(1, 2), 0, -2])
Matrix([[1, 0, -2], [-2, 1, 6], [3, -2, -5]]).solve(Matrix([-1, 7, -3])) == Matrix([3, 1, 2])
Matrix([[1, -3, 2], [0, 1, -4], [3, -5, -9]]).solve(Matrix([6, -7, -9])) == Matrix([-5, -3, 1])
Matrix([[1, -5, -7], [-3, 7, 5]]) * Matrix([3, 1, 0]) == Matrix([-2, -2]) and Matrix([[1, -5, -7], [-3, 7, 5]]) * Matrix([-3, -2, 1]) == zeros(2, 1)
Matrix([[1, -2, 1], [3, -4, 5], [0, 1, 1], [-3, 5, -4]]) * Matrix([7, 3, 0]) == Matrix([1, 9, 3, -6])
Matrix([[1, -4, 7, -5], [0, 1, -4, 3], [2, -6, 6, -4]]).nullspace() == [Matrix([9, 4, 1, 0]), Matrix([-7, -3, 0, 1])]
Matrix([[1, 3, 9, 2], [1, 0, 3, -4], [0, 1, 2, 3], [-2, 3, 0, 5]]).nullspace() == [Matrix([-3, -2, 1, 0])]
Matrix([[1, -4, 7, -5], [0, 1, -4, 3], [2, -6, 6, -4]]) * Matrix([3, 1, 0, 0]) == Matrix([-1, 1, 0])
4 in Matrix([[1, 3, 9, 2], [1, 0, 3, -4], [0, 1, 2, 3], [-2, 3, 0, 5]]).row_join(Matrix([-1, 3, -1, 4])).rref()[1]
Matrix([[-1, 0], [0, -1]]) * Matrix([5, 2]) == Matrix([-5, -2])
Rational(1, 2) * eye(2) * Matrix([-2, 4]) == Matrix([-1, 2])
Matrix([[0, 0], [0, 1]]) * Matrix([5, 2]) == Matrix([0, 2])
Matrix([[0, 1], [1, 0]]) * Matrix([-2, 4]) == Matrix([4, -2])
Matrix([[1, 0], [0, -1]]) * Matrix([4, 1]) == Matrix([4, -1])
Matrix([[1, 2], [2, 4]]).rank() == 1
Matrix([[4, -2, 5, -5], [-9, 7, -8, 0], [-6, 4, 5, 3], [5, -3, 8, -4]]) * Matrix([7, 9, 0, 2]) == zeros(4, 1)
Matrix([[-9, -4, -9, 4], [5, -8, -7, 6], [7, 11, 16, -9], [9, -7, -4, 5]]) * Matrix([-3, -5, 7, 4]) == zeros(4, 1)
Matrix([[4, -2, 5, -5], [-9, 7, -8, 0], [-6, 4, 5, 3], [5, -3, 8, -4]]) * Matrix([4, 7, 1, 0]) == Matrix([7, 5, 9, 7])
Matrix([[-9, -4, -9, 4], [5, -8, -7, 6], [7, 11, 16, -9], [9, -7, -4, 5]]) * Matrix([-2, -4, 5, 1]) == Matrix([-7, -7, 13, -5])
```
