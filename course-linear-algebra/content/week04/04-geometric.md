---
title_en: Geometric Linear Transformations of R²
title_zh: 平面上的幾何變換:反射、伸縮、剪切、投影
sub: Watch what happens to the unit square
level: mid
source: Lay 1.9
lab_hook: '把圖形的頂點排成矩陣 `P`,`A @ P` 一次變換所有頂點,再用 matplotlib 畫出來'
---
## 觀念
Examples 2 and 3 illustrate linear transformations that are described geometrically. Tables 1–4 illustrate other common geometric linear transformations of the plane. Because the transformations are linear, they are determined completely by what they do to the columns of $I_2$. Instead of showing only the images of $\mathbf{e}_1$ and $\mathbf{e}_2$, the tables show what a transformation does to the **unit square**.

Other transformations can be constructed from those listed in Tables 1–4 by applying one transformation after another. For instance, a horizontal shear could be followed by a reflection in the $x_2$-axis. Section 2.1 will show that such a *composition* of linear transformations is linear.

| Transformation | Standard matrix |
|---|---|
| Reflection through the $x_1$-axis | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ |
| Reflection through the $x_2$-axis | $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ |
| Reflection through the line $x_2 = x_1$ | $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ |
| Reflection through the line $x_2 = -x_1$ | $\begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}$ |
| Reflection through the origin | $\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$ |
| Horizontal contraction and expansion | $\begin{bmatrix} k & 0 \\ 0 & 1 \end{bmatrix}$ |
| Vertical contraction and expansion | $\begin{bmatrix} 1 & 0 \\ 0 & k \end{bmatrix}$ |
| Horizontal shear | $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ |
| Vertical shear | $\begin{bmatrix} 1 & 0 \\ k & 1 \end{bmatrix}$ |
| Projection onto the $x_1$-axis | $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ |
| Projection onto the $x_2$-axis | $\begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$ |

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| unit square | 單位正方形 | 由 $\mathbf{e}_1$、$\mathbf{e}_2$ 張成的 $1 \times 1$ 正方形 |
| reflection through … | 對……的反射 | 像照鏡子,鏡面是那條線或那個點 |
| contraction / expansion | 收縮 / 伸張 | 只在某個方向拉長或壓扁($k$ 倍) |
| horizontal / vertical shear | 水平 / 垂直剪切 | 越高推得越右(或越右推得越高) |
| projection onto … | 投影到…… | 把整個平面壓到一條軸上 |
| composition | 合成 | 先做一個變換,再做另一個 |

## 白話說
表格看起來有十一種變換,其實**只要記一招**:問「$\mathbf{e}_1$ 跑到哪、$\mathbf{e}_2$ 跑到哪」,答案直的排好就是矩陣(上一個觀念)。

- **反射到 $x_1$ 軸**:$\mathbf{e}_1$ 不動、$\mathbf{e}_2 \mapsto -\mathbf{e}_2$ → $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$。
- **反射到直線 $x_2 = x_1$**:兩個座標對調,$\mathbf{e}_1 \mapsto \mathbf{e}_2$、$\mathbf{e}_2 \mapsto \mathbf{e}_1$ → $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$。
- **水平剪切**:$\mathbf{e}_1$ 不動、$\mathbf{e}_2 \mapsto (k, 1)$ → $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$。
- **投影到 $x_1$ 軸**:$\mathbf{e}_1$ 不動、$\mathbf{e}_2 \mapsto \mathbf{0}$ → $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$。

**合成**(先做 $S$、再做 $T$)也一樣:讓 $\mathbf{e}_1$ **依序走完兩步**,看最後停在哪裡。注意順序——先做的那個先作用,像穿衣服:先穿襪子再穿鞋,反過來就不對了。

## 幾何意義
表格的畫法是看**單位正方形**被變成什麼形狀。為了看出有沒有「翻面」,圖裡放了一個不對稱的 F。

![課本 Table 1:五種反射,以及各自的標準矩陣。虛線是原本的單位正方形。](reflections.svg)

![課本 Table 2:水平與垂直的收縮($k < 1$)與伸張($k > 1$)。](contractions.svg)

![課本 Table 3:水平剪切與垂直剪切,$k$ 可正可負。](shears.svg)

![課本 Table 4:投影到 $x_1$ 軸與 $x_2$ 軸——整個正方形被壓成一條線段。](projections.svg)

看圖的重點:**反射會讓 F 變成鏡像**(翻面);**剪切與伸縮不會翻面**;**投影把面積壓成 0**,這就是它「救不回來」(不可逆)的原因(第 6 週)。

## 在資工哪裡用
- **影像編輯**:水平翻轉、垂直翻轉、旋轉、傾斜(剪切),每個按鈕背後都是這張表的一個矩陣。
- **遊戲的角色鏡像**:角色往左走時把貼圖做 $x_2$ 軸反射,只要一個 $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$。
- **資料視覺化**:把資料縮放到畫布座標,就是一個對角矩陣的伸縮。
- **合成的順序很重要**:「先旋轉再平移」和「先平移再旋轉」結果不同——這在第 5 週會變成「矩陣乘法不可交換」。

## 原理
**為什麼看單位正方形就夠?** 單位正方形的兩個邊就是 $\mathbf{e}_1$、$\mathbf{e}_2$。線性變換把它們送到 $T(\mathbf{e}_1)$、$T(\mathbf{e}_2)$,而正方形裡的每個點 $a\mathbf{e}_1 + b\mathbf{e}_2$($0 \le a, b \le 1$)被送到 $aT(\mathbf{e}_1) + bT(\mathbf{e}_2)$(上一個觀念的 Exercise 36)——也就是 $T(\mathbf{e}_1)$、$T(\mathbf{e}_2)$ 張成的平行四邊形。

**合成為什麼還是線性?**(Exercise 44)設 $S$、$T$ 都線性,則
$$T(S(c\mathbf{u} + d\mathbf{v})) = T(cS(\mathbf{u}) + dS(\mathbf{v})) = cT(S(\mathbf{u})) + dT(S(\mathbf{v})),$$
滿足性質 (4),所以 $\mathbf{x} \mapsto T(S(\mathbf{x}))$ 也是線性變換,一樣有標準矩陣。第 5 週會看到那個矩陣就是兩個矩陣的乘積。

## 老師講解
### 例 1 · Lay 1.9 Tables 1–4
Read off the standard matrices for: the reflection through the line $x_2 = x_1$, the horizontal shear with factor $k$, and the projection onto the $x_1$-axis.

1. **反射到 $x_2 = x_1$:先看 $\mathbf{e}_1$**。$(1, 0)$ 對直線 $x_2 = x_1$ 的鏡像是 $(0, 1)$,也就是 $\mathbf{e}_2$。
2. **再看 $\mathbf{e}_2$**:$(0, 1)$ 的鏡像是 $(1, 0) = \mathbf{e}_1$。
3. **排成行**:$A = [\,T(\mathbf{e}_1) \;\; T(\mathbf{e}_2)\,] = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$。驗證:$A(x_1, x_2) = (x_2, x_1)$,兩個座標對調 ✓。
4. **水平剪切**:定義是「$\mathbf{e}_1$ 不動,$\mathbf{e}_2$ 往水平方向推 $k$」,也就是 $T(\mathbf{e}_1) = (1, 0)$、$T(\mathbf{e}_2) = (k, 1)$。矩陣 $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$。
5. **看圖確認**:$k > 0$ 時正方形往右倒、$k < 0$ 時往左倒(見「幾何意義」的圖);底邊($x_2 = 0$)完全不動。
6. **投影到 $x_1$ 軸**:$\mathbf{e}_1$ 不動,$\mathbf{e}_2$ 被壓到原點:$T(\mathbf{e}_2) = \mathbf{0}$。矩陣 $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$。
7. **注意投影的特別之處**:整個正方形被壓成一條線段,面積變 0。它的值域只是一條直線,而且**不同的點會被送到同一個地方**——下一個觀念會說這叫「不是一對一」。

### 例 2 · 補充:合成兩個變換
Let $T$ be the transformation that first rotates points through $\pi/2$ radians (counterclockwise) and then reflects them through the $x_1$-axis. Find the standard matrix of $T$ by following $\mathbf{e}_1$ and $\mathbf{e}_2$.

1. **拆成兩步,依序做**。先旋轉、再反射。
2. **追 $\mathbf{e}_1 = (1, 0)$**:旋轉 90° 後到 $(0, 1)$;再對 $x_1$ 軸反射(第二個分量變號)到 $(0, -1)$。所以 $T(\mathbf{e}_1) = (0, -1)$。
3. **追 $\mathbf{e}_2 = (0, 1)$**:旋轉 90° 後到 $(-1, 0)$;反射後第二個分量是 0,不變,還是 $(-1, 0)$。所以 $T(\mathbf{e}_2) = (-1, 0)$。
4. **排成行**:$A = \begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}$。
5. **認出它是什麼**:查表格——這是「對直線 $x_2 = -x_1$ 的反射」。兩個變換合起來,變成表上的另一個變換。
6. **換順序試試**:先反射、再旋轉,則 $\mathbf{e}_1 \mapsto (1, 0) \mapsto (0, 1)$、$\mathbf{e}_2 \mapsto (0, -1) \mapsto (1, 0)$,矩陣是 $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$——**不一樣**!順序會改變結果。
7. **預告**:第 5 週會把「合成」寫成矩陣乘法,而「順序有差」就是「$AB \neq BA$」。

#### 備註
第 6 步的順序對照很重要,學生在 Exercises 7–10 最常犯的錯就是把順序做反。

## 易錯點
- 合成時順序做反。**先做的先作用在 $\mathbf{e}_j$ 上**。
- 把「投影到 $x_1$ 軸」寫成 $\begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$。投影到 $x_1$ 軸保留第一個分量,矩陣是 $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$。
- 剪切的 $k$ 放錯位置:水平剪切的 $k$ 在**右上角**,垂直剪切在**左下角**。
- 旋轉角是負的時候忘了 $\sin(-\varphi) = -\sin\varphi$,矩陣的正負號寫錯(Exercises 4、7)。

## 教學提示
用一張投影片放四個表格的圖,讓學生**先猜矩陣再對答案**。猜錯最多的是「反射到 $x_2 = -x_1$」和垂直剪切。

例 2 的第 6 步(換順序)一定要做,這是第 5 週矩陣乘法不可交換的伏筆。

Exercises 7–10 都是合成題,建議課堂做一題、作業做其餘。Exercises 11–12 反過來問「這個合成其實是哪個旋轉」,很適合當討論。

課堂建議做:Exercises 3、5、7;是非 Exercises 25、30;Practice Problem 1。

## 練習
### 照做 · Lay 1.9 Exercises 3–6
Assume that $T$ is a linear transformation. Find the standard matrix of $T$.

(3) $T : \mathbb{R}^2 \to \mathbb{R}^2$ rotates points (about the origin) through $3\pi/2$ radians (in the counterclockwise direction). (4) $T : \mathbb{R}^2 \to \mathbb{R}^2$ rotates points (about the origin) through $-\pi/4$ radians (since the number is negative, the actual rotation is clockwise). [*Hint:* $T(\mathbf{e}_1) = (1/\sqrt{2},\ -1/\sqrt{2})$.]

(5) $T : \mathbb{R}^2 \to \mathbb{R}^2$ is a vertical shear transformation that maps $\mathbf{e}_1$ into $\mathbf{e}_1 - 2\mathbf{e}_2$ but leaves the vector $\mathbf{e}_2$ unchanged. (6) $T : \mathbb{R}^2 \to \mathbb{R}^2$ is a horizontal shear transformation that leaves $\mathbf{e}_1$ unchanged and maps $\mathbf{e}_2$ into $\mathbf{e}_2 + 5\mathbf{e}_1$.

#### 解答
(3) 旋轉 $\tfrac{3\pi}2$:$\mathbf{e}_1 \mapsto (\cos\tfrac{3\pi}2, \sin\tfrac{3\pi}2) = (0, -1)$、$\mathbf{e}_2 \mapsto (-\sin\tfrac{3\pi}2, \cos\tfrac{3\pi}2) = (1, 0)$,所以 $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$(書後解答相同)。

(4) $A = \begin{bmatrix} \cos(-\pi/4) & -\sin(-\pi/4) \\ \sin(-\pi/4) & \cos(-\pi/4) \end{bmatrix} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ -1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix}$。

(5) $T(\mathbf{e}_1) = (1, -2)$、$T(\mathbf{e}_2) = (0, 1)$,所以 $A = \begin{bmatrix} 1 & 0 \\ -2 & 1 \end{bmatrix}$(書後解答相同)。$k$ 在左下角,是**垂直**剪切。

(6) $T(\mathbf{e}_1) = (1, 0)$、$T(\mathbf{e}_2) = (5, 1)$,所以 $A = \begin{bmatrix} 1 & 5 \\ 0 & 1 \end{bmatrix}$。$k$ 在右上角,是**水平**剪切。

### 照做 · Lay 1.9 Exercises 7–10
Assume that $T$ is a linear transformation. Find the standard matrix of $T$.

(7) $T : \mathbb{R}^2 \to \mathbb{R}^2$ first rotates points through $-3\pi/4$ radians (clockwise) and then reflects points through the horizontal $x_1$-axis. [*Hint:* $T(\mathbf{e}_1) = (-1/\sqrt{2},\ 1/\sqrt{2})$.] (8) $T : \mathbb{R}^2 \to \mathbb{R}^2$ first reflects points through the vertical $x_2$-axis and then reflects points through the line $x_2 = x_1$.

(9) $T : \mathbb{R}^2 \to \mathbb{R}^2$ first performs a horizontal shear that transforms $\mathbf{e}_2$ into $\mathbf{e}_2 - 3\mathbf{e}_1$ (leaving $\mathbf{e}_1$ unchanged) and then reflects points through the line $x_2 = -x_1$. (10) $T : \mathbb{R}^2 \to \mathbb{R}^2$ first reflects points through the vertical $x_2$-axis and then rotates points $3\pi/2$ radians.

#### 解答
做法一律是「讓 $\mathbf{e}_1$、$\mathbf{e}_2$ **依序**走完兩步」。

(7) 旋轉 $-\tfrac{3\pi}4$:$\mathbf{e}_1 \mapsto (-\tfrac1{\sqrt2}, -\tfrac1{\sqrt2})$、$\mathbf{e}_2 \mapsto (\tfrac1{\sqrt2}, -\tfrac1{\sqrt2})$。再對 $x_1$ 軸反射(第二個分量變號):$T(\mathbf{e}_1) = (-\tfrac1{\sqrt2}, \tfrac1{\sqrt2})$、$T(\mathbf{e}_2) = (\tfrac1{\sqrt2}, \tfrac1{\sqrt2})$。所以 $A = \begin{bmatrix} -1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix}$(書後解答相同)。

(8) $\mathbf{e}_1 \mapsto (-1, 0) \mapsto (0, -1)$;$\mathbf{e}_2 \mapsto (0, 1) \mapsto (1, 0)$。所以 $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$。

(9) 對 $x_2 = -x_1$ 的反射是 $(u, v) \mapsto (-v, -u)$。$\mathbf{e}_1 \mapsto (1, 0) \mapsto (0, -1)$;$\mathbf{e}_2 \mapsto (-3, 1) \mapsto (-1, 3)$。所以 $A = \begin{bmatrix} 0 & -1 \\ -1 & 3 \end{bmatrix}$(書後解答相同)。

(10) $\mathbf{e}_1 \mapsto (-1, 0) \mapsto (0, 1)$;$\mathbf{e}_2 \mapsto (0, 1) \mapsto (1, 0)$。所以 $A = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$,剛好是「對直線 $x_2 = x_1$ 的反射」。

### 是非 · Lay 1.9 Exercise 25
**(T/F)** If $T : \mathbb{R}^2 \to \mathbb{R}^2$ rotates vectors about the origin through an angle $\phi$, then $T$ is a linear transformation.

#### 解答
**True.** 旋轉就是矩陣變換 $\mathbf{x} \mapsto \begin{bmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{bmatrix}\mathbf{x}$(上一個觀念的例 2),矩陣變換都是線性的。

### 是非 · Lay 1.9 Exercise 27
**(T/F)** When two linear transformations are performed one after another, the combined effect may not always be a linear transformation.

#### 解答
**False.** 合成一定還是線性(Exercise 44):$T(S(c\mathbf{u} + d\mathbf{v})) = cT(S(\mathbf{u})) + dT(S(\mathbf{v}))$。

### 是非 · Lay 1.9 Exercise 30
**(T/F)** The standard matrix of a linear transformation from $\mathbb{R}^2$ to $\mathbb{R}^2$ that reflects points through the horizontal axis, the vertical axis, or the origin has the form $\begin{bmatrix} a & 0 \\ 0 & d \end{bmatrix}$, where $a$ and $d$ are $\pm 1$.

#### 解答
**True.** 查表格:三個矩陣分別是 $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$、$\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$、$\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$,都是這個形式。

#### 備註
注意另外兩個反射(對 $x_2 = x_1$ 與 $x_2 = -x_1$)**不是**對角矩陣,題目也沒把它們列進去。

### 變化 · Lay 1.9 Exercises 11–12
(11) A linear transformation $T : \mathbb{R}^2 \to \mathbb{R}^2$ first reflects points through the $x_1$-axis and then reflects points through the $x_2$-axis. Show that $T$ can also be described as a linear transformation that rotates points about the origin. What is the angle of that rotation?

(12) Show that the transformation in Exercise 8 is merely a rotation about the origin. What is the angle of the rotation?

#### 解答
(11) $\mathbf{e}_1 \mapsto \mathbf{e}_1 \mapsto -\mathbf{e}_1$、$\mathbf{e}_2 \mapsto -\mathbf{e}_2 \mapsto -\mathbf{e}_2$,所以標準矩陣是 $\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix} = \begin{bmatrix} \cos\pi & -\sin\pi \\ \sin\pi & \cos\pi \end{bmatrix}$:**旋轉 $\pi$ 弧度(180°)**。書後解答的說法:線性變換完全由 $\mathbf{e}_1$、$\mathbf{e}_2$ 的像決定,兩者一致,所以對每個向量的作用都相同。

(12) Exercise 8 的矩陣是 $\begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$。和旋轉矩陣比對:$\cos\varphi = 0$、$\sin\varphi = -1$,所以 $\varphi = -\pi/2$——**順時針旋轉 90°**(等於逆時針 $3\pi/2$)。

### 變化 · Lay 1.9 Practice Problem 1
Let $T : \mathbb{R}^2 \to \mathbb{R}^2$ be the transformation that first performs a horizontal shear that maps $\mathbf{e}_2$ into $\mathbf{e}_2 - .5\mathbf{e}_1$ (but leaves $\mathbf{e}_1$ unchanged) and then reflects the result through the $x_2$-axis. Assuming that $T$ is linear, find its standard matrix. [*Hint:* Determine the final location of the images of $\mathbf{e}_1$ and $\mathbf{e}_2$.]

#### 解答
**追 $\mathbf{e}_1$**:剪切不動它;再對 $x_2$ 軸反射變成 $-\mathbf{e}_1$。所以 $T(\mathbf{e}_1) = -\mathbf{e}_1$。

**追 $\mathbf{e}_2$**:剪切把它送到 $\mathbf{e}_2 - .5\mathbf{e}_1$;反射把 $\mathbf{e}_1$ 變號、$\mathbf{e}_2$ 不變,所以變成 $\mathbf{e}_2 + .5\mathbf{e}_1$。

排成行:
$$A = [\,T(\mathbf{e}_1) \;\; T(\mathbf{e}_2)\,] = \begin{bmatrix} -1 & .5 \\ 0 & 1 \end{bmatrix}$$
(課本 p. 108–109)。

### 挑戰 · Lay 1.9 Exercise 44
Let $S : \mathbb{R}^p \to \mathbb{R}^n$ and $T : \mathbb{R}^n \to \mathbb{R}^m$ be linear transformations. Show that the mapping $\mathbf{x} \mapsto T(S(\mathbf{x}))$ is a linear transformation (from $\mathbb{R}^p$ to $\mathbb{R}^m$). [*Hint:* Compute $T(S(c\mathbf{u} + d\mathbf{v}))$ for $\mathbf{u}, \mathbf{v}$ in $\mathbb{R}^p$ and scalars $c$ and $d$. Justify each step of the computation, and explain why this computation gives the desired conclusion.]

#### 解答
取 $\mathbf{u}, \mathbf{v}$ 與純量 $c, d$:
$$T(S(c\mathbf{u} + d\mathbf{v})) = T(cS(\mathbf{u}) + dS(\mathbf{v})) \quad (S \text{ 線性}) = cT(S(\mathbf{u})) + dT(S(\mathbf{v})) \quad (T \text{ 線性}).$$
這正是性質 (4),而滿足 (4) 的變換一定線性(取 $c = d = 1$ 得加法、取 $d = 0$ 得純量倍數)。所以合成 $\mathbf{x} \mapsto T(S(\mathbf{x}))$ 是從 ℝᵖ 到 ℝᵐ 的線性變換。

#### 備註
既然合成也是線性,它也有標準矩陣。第 5 週(Lay 2.1)會證明:那個矩陣就是兩個標準矩陣的**乘積**,而且順序不能換。

## 驗算
```check
Matrix([[0, 1], [1, 0]]) * Matrix([x1, x2]) == Matrix([x2, x1])
Matrix([[1, k], [0, 1]]) * Matrix([0, 1]) == Matrix([k, 1])
Matrix([[1, 0], [0, 0]]) * Matrix([x1, x2]) == Matrix([x1, 0])
Matrix([[1, 0], [0, -1]]) * Matrix([[cos(pi/2), -sin(pi/2)], [sin(pi/2), cos(pi/2)]]) == Matrix([[0, -1], [-1, 0]])
Matrix([[cos(pi/2), -sin(pi/2)], [sin(pi/2), cos(pi/2)]]) * Matrix([[1, 0], [0, -1]]) == Matrix([[0, 1], [1, 0]])
Matrix([[cos(3*pi/2), -sin(3*pi/2)], [sin(3*pi/2), cos(3*pi/2)]]) == Matrix([[0, 1], [-1, 0]])
simplify(Matrix([[cos(-pi/4), -sin(-pi/4)], [sin(-pi/4), cos(-pi/4)]]) - Matrix([[1/sqrt(2), 1/sqrt(2)], [-1/sqrt(2), 1/sqrt(2)]])) == zeros(2, 2)
Matrix([[1, 0], [-2, 1]]) * Matrix([1, 0]) == Matrix([1, -2]) and Matrix([[1, 0], [-2, 1]]) * Matrix([0, 1]) == Matrix([0, 1])
Matrix([[1, 5], [0, 1]]) * Matrix([0, 1]) == Matrix([0, 1]) + 5 * Matrix([1, 0])
simplify(Matrix([[1, 0], [0, -1]]) * Matrix([[cos(-3*pi/4), -sin(-3*pi/4)], [sin(-3*pi/4), cos(-3*pi/4)]]) - Matrix([[-1/sqrt(2), 1/sqrt(2)], [1/sqrt(2), 1/sqrt(2)]])) == zeros(2, 2)
Matrix([[0, 1], [1, 0]]) * Matrix([[-1, 0], [0, 1]]) == Matrix([[0, 1], [-1, 0]])
Matrix([[0, -1], [-1, 0]]) * Matrix([[1, -3], [0, 1]]) == Matrix([[0, -1], [-1, 3]])
Matrix([[cos(3*pi/2), -sin(3*pi/2)], [sin(3*pi/2), cos(3*pi/2)]]) * Matrix([[-1, 0], [0, 1]]) == Matrix([[0, 1], [1, 0]])
Matrix([[-1, 0], [0, 1]]) * Matrix([[1, 0], [0, -1]]) == Matrix([[cos(pi), -sin(pi)], [sin(pi), cos(pi)]])
Matrix([[0, 1], [-1, 0]]) == Matrix([[cos(-pi/2), -sin(-pi/2)], [sin(-pi/2), cos(-pi/2)]])
Matrix([[-1, 0], [0, 1]]) * Matrix([[1, Rational(-1, 2)], [0, 1]]) == Matrix([[-1, Rational(1, 2)], [0, 1]])
all(M.is_diagonal() and set(M.diagonal()) <= {1, -1} for M in [Matrix([[1, 0], [0, -1]]), Matrix([[-1, 0], [0, 1]]), Matrix([[-1, 0], [0, -1]])])
expand(Matrix([[a, b], [c, d]]) * (Matrix([[f, g], [h, k]]) * (s * Matrix([x1, x2]) + t * Matrix([x3, x4]))) - s * Matrix([[a, b], [c, d]]) * Matrix([[f, g], [h, k]]) * Matrix([x1, x2]) - t * Matrix([[a, b], [c, d]]) * Matrix([[f, g], [h, k]]) * Matrix([x3, x4])) == zeros(2, 1)
```
