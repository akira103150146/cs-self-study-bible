---
title_en: Applications to Computer Graphics
title_zh: 齊次座標:讓平移也變成矩陣乘法
sub: Add a 1, and translation becomes a matrix
level: mid
source: Lay 2.7
lab_hook: '把頂點寫成 `np.vstack([D, np.ones(n)])`,整條管線就是連乘 3×3 矩陣'
---
## 觀念
Computer graphics are images displayed or animated on a computer screen. This section examines some of the basic mathematics used to manipulate and display graphical images such as a wire-frame model of an airplane. Such an image (or picture) consists of a number of points, connecting lines or curves, and information about how to fill in closed regions bounded by the lines and curves. Often, curved lines are approximated by short straight-line segments, and a figure is defined mathematically by a list of points.

The main reason graphical objects are described by collections of straight-line segments is that the standard transformations in computer graphics map line segments onto other line segments. Once the vertices that describe an object have been transformed, their images can be connected with the appropriate straight lines to produce the complete image of the original object.

Unfortunately, translating an object on a screen does not correspond directly to matrix multiplication because translation is not a linear transformation. The standard way to avoid this difficulty is to introduce what are called *homogeneous coordinates*.

**Homogeneous coordinates (2D).** Each point $(x, y)$ in $\mathbb{R}^2$ can be identified with the point $(x, y, 1)$ on the plane in $\mathbb{R}^3$ that lies one unit above the $xy$-plane. We say that $(x, y)$ has **homogeneous coordinates** $(x, y, 1)$. Homogeneous coordinates for points are not added or multiplied by scalars, but they can be transformed via multiplication by $3 \times 3$ matrices.

**Composite transformations.** The movement of a figure on a computer screen often requires two or more basic transformations. The composition of such transformations corresponds to matrix multiplication when homogeneous coordinates are used.

**Homogeneous 3D coordinates.** By analogy with the 2D case, we say that $(x, y, z, 1)$ are homogeneous coordinates for the point $(x, y, z)$ in $\mathbb{R}^3$. In general, $(X, Y, Z, H)$ are **homogeneous coordinates** for $(x, y, z)$ if $H \ne 0$ and

$$x = \frac{X}{H}, \qquad y = \frac{Y}{H}, \quad\text{and}\quad z = \frac{Z}{H} \tag{1}$$

Each nonzero scalar multiple of $(x, y, z, 1)$ gives a set of homogeneous coordinates for $(x, y, z)$.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| homogeneous coordinates | 齊次座標 | 平面上的 $(x, y)$ 寫成 $(x, y, 1)$;空間的 $(x,y,z)$ 寫成 $(x,y,z,1)$ |
| data matrix | 資料矩陣 | 一個圖形的所有頂點,一個頂點一行 |
| vertices | 頂點 | 圖形的轉折點,連起來就是線框圖 |
| composite transformation | 合成變換 | 好幾個變換接起來,對應矩陣相乘 |
| translation | 平移 | 整個圖形移動 $(h, k)$;**不是**線性變換 |
| viewing plane | 視平面 | 3D 物體被投影上去的那個平面,這裡就是螢幕 |
| perspective projection | 透視投影 | 近大遠小的投影方式 |
| center of projection | 投影中心 | 觀察者眼睛的位置 $(0, 0, d)$ |

## 白話說
**問題**:上週證過,線性變換一定滿足 $T(\mathbf{0}) = \mathbf{0}$。可是平移會把原點移走,所以**平移不是線性變換,寫不成 $2 \times 2$ 矩陣**。但螢幕上的圖形當然要能移動,怎麼辦?

**解法**:給每個點多加一個座標 1。

![平面上的每個點 $(x, y)$ 都對應到上方一單位那個平面的 $(x, y, 1)$。](homogeneous.svg)

點 $(x, y)$ 記成 $(x, y, 1)$ 之後,平移就變成一個 $3 \times 3$ 矩陣乘法:

$$\begin{bmatrix} 1 & 0 & h \\ 0 & 1 & k \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} x \\ y \\ 1 \end{bmatrix} = \begin{bmatrix} x + h \\ y + k \\ 1 \end{bmatrix}$$

**為什麼有效**:平移量 $(h, k)$ 被放在第三行,乘進去時和那個 1 相乘,就加到答案上。多加的那個 1 是個「常數輸入端」,把「加一個定值」偽裝成「乘一個矩陣」。

**原本的線性變換呢?** 照放在左上角就好:
$$\begin{bmatrix} A & \mathbf{0} \\ \mathbf{0} & 1 \end{bmatrix}, \quad A \text{ 是原來的 } 2 \times 2 \text{ 矩陣}$$

於是旋轉、縮放、鏡射、剪切、**平移**全都是 $3 \times 3$ 矩陣,可以自由相乘——這就是所有 2D 繪圖引擎的做法。

**順序**:$M_3M_2M_1\mathbf{x}$ 的意思是「先做 $M_1$、再做 $M_2$、最後做 $M_3$」。**寫在右邊的先做。**

## 幾何意義
第三個座標 1 不是「高度」,它是個記號。把平面搬到 $z = 1$ 這個高度之後,原點 $(0,0)$ 變成 $(0,0,1)$——**不再是空間中的原點**,所以「不能移動原點」這條限制就解除了。$\mathbb{R}^3$ 裡通過原點的線性變換,看在 $z = 1$ 那層平面上,就成了平面上的「線性變換 + 平移」。

3D 也一樣:$(x, y, z)$ 記成 $(x, y, z, 1)$,平移是 $4 \times 4$ 矩陣。而且 3D 的齊次座標更進一步——$(X, Y, Z, H)$ 代表 $(X/H, Y/H, Z/H)$,**整組座標乘上任何非零常數都代表同一個點**。下面的透視投影就靠這一點。

## 在資工哪裡用
- **這一節就是 OpenGL / DirectX / Unity 的座標系統**。繪圖 API 裡的 `Matrix4x4`、`glTranslatef`、`model-view-projection matrix`,用的全是這裡的齊次座標。
- **一次合成、重複套用**:一個模型有幾萬個頂點。先把整條管線的矩陣乘成一個 $4 \times 4$,再套到每個頂點上,比每個頂點各走一遍所有步驟快得多(Exercise 9 就在算這筆帳)。
- **繞自己的中心旋轉**:遊戲角色轉身不是繞世界原點轉。做法是「平移 $-\mathbf{p}$ → 旋轉 → 平移回 $\mathbf{p}$」三個矩陣相乘(Practice Problem)。
- **顏色空間轉換**:RGB 與 CIE XYZ、YIQ 之間的換算就是乘一個 $3 \times 3$ 矩陣;要反過來換,就是乘反矩陣(Exercises 21–22,正好用到這週的觀念 4–5)。
- **相機內參矩陣**:電腦視覺裡把 3D 點投到影像平面的 $K[R \mid \mathbf{t}]$,就是這裡的透視投影矩陣。

## 實際應用
課本這一節的開場提到 CAD(電腦輔助設計):飛機的線框模型存成好幾個矩陣,工程師要放大、旋轉、看被擋住的部分,每個動作都是矩陣乘法。分子模擬也一樣——生物學家把藥物分子旋轉、平移,試著讓它嵌進蛋白質的活性位點。

## 數值筆記
課本 2.7 的 Numerical Note:3D 物件的連續運動需要大量 $4 \times 4$ 矩陣運算,尤其在算光照與材質的時候。高階顯示卡把 $4 \times 4$ 矩陣運算直接做進晶片裡,每秒可以做幾十億次矩陣乘法——這就是為什麼 3D 遊戲需要 GPU,以及為什麼同一批硬體後來被拿來跑深度學習。

## 原理
**為什麼平移在齊次座標下是線性的?** 因為我們換了空間。在 $\mathbb{R}^2$ 裡,$\mathbf{x} \mapsto \mathbf{x} + \mathbf{p}$ 不是線性變換;但在 $\mathbb{R}^3$ 裡,$(x, y, 1) \mapsto (x + h, y + k, 1)$ 是某個 $3 \times 3$ 矩陣乘法的**限制**——這個矩陣作用在整個 $\mathbb{R}^3$ 上確實是線性的,我們只是恰好只看 $z = 1$ 那一層。

**一般的 2D 圖學矩陣**(Exercise 13):形如
$$\begin{bmatrix} A & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix} = \begin{bmatrix} I & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}\begin{bmatrix} A & \mathbf{0} \\ \mathbf{0}^T & 1 \end{bmatrix}$$
的矩陣,等於「先做線性變換 $A$,再平移 $\mathbf{p}$」。直接驗證更快:
$$\begin{bmatrix} A & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}\begin{bmatrix} \mathbf{x} \\ 1 \end{bmatrix} = \begin{bmatrix} A\mathbf{x} + \mathbf{p} \\ 1 \end{bmatrix}$$
這種「線性 + 平移」的變換叫做**仿射變換(affine transformation)**,是電腦圖學的基本磚塊。

**透視投影的推導**(課本 pp. 175–176):螢幕是 $xy$ 平面,眼睛在 $(0, 0, d)$。點 $(x, y, z)$ 的像 $(x^*, y^*, 0)$ 要和眼睛共線。

![由眼睛出發、穿過該點的直線打在螢幕上;相似三角形給出 $x^* = dx/(d - z)$。](perspective.svg)

由相似三角形
$$\frac{x^*}{d} = \frac{x}{d - z} \quad\Longrightarrow\quad x^* = \frac{dx}{d-z} = \frac{x}{1 - z/d}, \qquad y^* = \frac{y}{1 - z/d}$$

這裡有**除法**,看起來不可能寫成矩陣。但齊次座標可以差一個非零純量倍,所以把整組座標同乘 $1 - z/d$:
$$\left(\frac{x}{1 - z/d},\; \frac{y}{1 - z/d},\; 0,\; 1\right) \;\sim\; (x,\; y,\; 0,\; 1 - z/d)$$
右邊沒有分式了,於是矩陣直接讀得出來:
$$P\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & -1/d & 1 \end{bmatrix}\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} x \\ y \\ 0 \\ 1 - z/d \end{bmatrix}$$
第三列全 0,把所有點壓到螢幕平面;第四列的 $-1/d$ 製造「近大遠小」。最後用 (1) 式把前三個分量各除以第四個分量,才回到真實座標——**除法被延後到最後一步**,中間全是矩陣乘法。

## 老師講解
### 例 1 · Lay 2.7 Examples 1–3
The capital letter N is determined by eight points, or *vertices*. The coordinates of the points can be stored in a data matrix $D$:

$$D = \begin{bmatrix} 0 & .5 & .5 & 6 & 6 & 5.5 & 5.5 & 0 \\ 0 & 0 & 6.42 & 0 & 8 & 8 & 1.58 & 8 \end{bmatrix}$$

Given $A = \begin{bmatrix} 1 & .25 \\ 0 & 1 \end{bmatrix}$, describe the effect of the shear transformation $\mathbf{x} \mapsto A\mathbf{x}$ on the letter N. Then compute the matrix of the transformation that performs this shear and then scales all $x$-coordinates by a factor of .75.

1. **圖形 = 頂點清單**。上面那一列是 8 個頂點的 $x$ 座標,下面那一列是 $y$ 座標。一個頂點一行,所以 $D$ 是 $2 \times 8$。(另外還要記錄哪些頂點要連線,這裡省略。)
2. **一次變換所有頂點**:$AD$ 的第 $j$ 行就是 $A$ 乘上第 $j$ 個頂點。不必寫迴圈一個一個算,一次矩陣乘法就做完 8 個點——這正是觀念 2 的定義。
3. **算出來**:
   $$AD = \begin{bmatrix} 0 & .5 & 2.105 & 6 & 8 & 7.5 & 5.895 & 2 \\ 0 & 0 & 6.420 & 0 & 8 & 8 & 1.580 & 8 \end{bmatrix}$$
   例如第 3 個頂點 $(0.5,\, 6.42) \mapsto (0.5 + .25 \times 6.42,\; 6.42) = (2.105,\, 6.42)$:$y$ 越高的點,往右推越多,字就斜了。
4. **為什麼線段還是線段**:變換只作用在頂點上,但因為矩陣變換把線段映成線段(上週 Exercise 35 證過),所以把像連起來就是正確的圖形。
5. **斜體 N 看起來太寬**,所以再把 $x$ 座標乘 $.75$:$S = \begin{bmatrix} .75 & 0 \\ 0 & 1 \end{bmatrix}$。
6. **合成 = 相乘,後做的寫左邊**:
   $$SA = \begin{bmatrix} .75 & 0 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & .25 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} .75 & .1875 \\ 0 & 1 \end{bmatrix}$$
7. **結果**:
   ![課本 2.7 Figures 1–3:原本的 N、剪切後的斜體 N,以及再壓窄後的合成結果。](letter-n.svg)

### 例 2 · Lay 2.7 Examples 4–6
A translation of the form $(x, y) \mapsto (x + h, y + k)$ is written in homogeneous coordinates as $(x, y, 1) \mapsto (x + h, y + k, 1)$. Any linear transformation on $\mathbb{R}^2$ is represented with respect to homogeneous coordinates by a partitioned matrix of the form $\begin{bmatrix} A & \mathbf{0} \\ \mathbf{0} & 1 \end{bmatrix}$. Find the $3 \times 3$ matrix that corresponds to the composite transformation of a scaling by .3, a rotation of $90°$ about the origin, and finally a translation that adds $(-.5, 2)$ to each point of a figure.

1. **先把三個動作各寫成 $3 \times 3$ 矩陣**。縮放 $.3$:$\begin{bmatrix} .3 & 0 & 0 \\ 0 & .3 & 0 \\ 0 & 0 & 1 \end{bmatrix}$(線性變換,放左上角)。
2. **旋轉 $90°$**:$\varphi = \pi/2$,$\cos\varphi = 0$、$\sin\varphi = 1$,所以 $\begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}$(上週的旋轉矩陣放左上角)。
3. **平移 $(-.5, 2)$**:$\begin{bmatrix} 1 & 0 & -.5 \\ 0 & 1 & 2 \\ 0 & 0 & 1 \end{bmatrix}$(平移量放第三行)。
4. **照順序疊上去**。一個點先被縮放,所以縮放矩陣**最靠近點**(寫最右邊);接著旋轉,再接著平移:
   $$\begin{bmatrix} 1 & 0 & -.5 \\ 0 & 1 & 2 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} .3 & 0 & 0 \\ 0 & .3 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$
5. **由左往右乘兩次**(結合律保證怎麼括號都一樣):
   $$= \begin{bmatrix} 0 & -1 & -.5 \\ 1 & 0 & 2 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} .3 & 0 & 0 \\ 0 & .3 & 0 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 0 & -.3 & -.5 \\ .3 & 0 & 2 \\ 0 & 0 & 1 \end{bmatrix}$$
6. **讀懂這個答案**:左上角 $2 \times 2$ 是「縮放 + 旋轉」合起來的線性部分,第三行 $(-.5, 2)$ 是平移量。和 Exercise 13 的結論一致——任何這種矩陣都是「先線性、再平移」。
7. **圖上看**:
   ![課本 2.7 Example 6:三角形先縮小、再轉 90°、最後平移。](pipeline.svg)
8. **順序不能換**。若先平移再縮放,平移量也會被縮小 $.3$ 倍,結果完全不同(Exercise 10 會證這件事)。

#### 備註
第 4 步是整節最容易錯的地方。建議在黑板上畫一個點,讓它「由右往左」穿過三個矩陣,邊走邊問「現在做到哪一步了」。

### 例 3 · Lay 2.7 Example 8
Let $S$ be the box with vertices $(3, 1, 5)$, $(5, 1, 5)$, $(5, 0, 5)$, $(3, 0, 5)$, $(3, 1, 4)$, $(5, 1, 4)$, $(5, 0, 4)$, and $(3, 0, 4)$. Find the image of $S$ under the perspective projection with center of projection at $(0, 0, 10)$.

1. **眼睛在 $(0, 0, 10)$**,所以 $d = 10$,投影矩陣是
   $$P = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & -1/10 & 1 \end{bmatrix}$$
2. **頂點寫成齊次座標**,排成資料矩陣 $D$(第四列全是 1)。
3. **算 $PD$**:第一、二列照抄,第三列變成 0,第四列變成 $1 - z/10$。$z = 5$ 的頂點得到 $.5$,$z = 4$ 的得到 $.6$。
4. **最後一步是除法**:把每一行的前三個分量除以第四個分量(公式 (1))。例如 $(3, 1, 0, .5) \to (6, 2, 0)$;$(3, 1, 0, .6) \to (5, 1.7, 0)$。
5. **讀出幾何意義**:$z = 5$(離眼睛比較近)的那一面被放大成 $6 \times 2$ 的範圍,$z = 4$(比較遠)的那一面只有 $5 \times 1.7$——**近大遠小**就是這樣算出來的。
6. **整條管線只有最後一步有除法**。中間全是矩陣乘法,所以可以和旋轉、平移一起合成成單一個 $4 \times 4$ 矩陣,交給顯示卡去做。

## 易錯點
- **把齊次座標的 1 當成 $z$ 座標**。它只是記號;2D 圖形的齊次座標永遠是 $(x, y, 1)$。
- **順序寫反**。「先平移再旋轉」是 $RT$,不是 $TR$。右邊的先做。
- **平移矩陣的位置放錯**:平移量在**第三行**(最後一行),不是第三列。
- **忘記最後除以 $H$**。3D 齊次座標算完要用 $x = X/H$ 還原(Exercise 15 就在練這件事)。
- **把 Exercise 12 的 $-\tan \varphi/2$ 讀成 $-(\tan\varphi)/2$**。書上排版是 $-\tan\dfrac{\varphi}{2}$,半角。
- 資料矩陣忘了補第三列的 1,矩陣尺寸就對不上($3 \times 3$ 乘不了 $2 \times n$)。

## 教學提示
這個觀念的鉤子非常好用:先問「遊戲角色往右移動兩格,是乘上哪個矩陣?」讓學生試著寫 $2 \times 2$,發現寫不出來(因為原點會被移走),再引出齊次座標。**這個「卡住 → 加一個 1 → 解決」的過程一定要讓學生自己撞一次牆**,否則齊次座標看起來只是莫名其妙的規定。

例 2 的乘法順序建議用「接力棒」比喻:點從右邊出發,一棒一棒往左傳。

透視投影(例 3)如果時間不夠可以略過,或只講「除法藏進第四個分量」這個想法,不算完整的例子。Exercises 19–20 一樣可以移到作業。

課堂建議做:Exercises 1、3、5、6(5 和 6 一定要連著做,對照順序的影響);Exercise 15 當快問快答。Practice Problem 是「繞任意點旋轉」,務必課堂講解,因為 Exercises 7、8 都靠它。Exercise 9(計算量)很適合當本節收尾的討論題,並接到實作課。

T 題 Exercises 21–22 是顏色空間轉換,會用到反矩陣,放進實作課做。

## 練習
### 照做 · Lay 2.7 Exercises 1–2
(1) What $3 \times 3$ matrix will have the same effect on homogeneous coordinates for $\mathbb{R}^2$ that the shear matrix $A$ has in Example 2?

(2) Use matrix multiplication to find the image of the triangle with data matrix $D = \begin{bmatrix} 5 & 2 & 4 \\ 0 & 2 & 3 \end{bmatrix}$ under the transformation that reflects points through the $y$-axis. Sketch both the original triangle and its image.

#### 解答
(1) Example 2 的 $A = \begin{bmatrix} 1 & .25 \\ 0 & 1 \end{bmatrix}$ 是線性變換,放到左上角即可:
$$\begin{bmatrix} 1 & .25 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

(2) 對 $y$ 軸鏡射把 $x$ 座標變號:$A = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$,
$$AD = \begin{bmatrix} -5 & -2 & -4 \\ 0 & 2 & 3 \end{bmatrix}$$
原三角形頂點 $(5,0)$、$(2,2)$、$(4,3)$,像是 $(-5,0)$、$(-2,2)$、$(-4,3)$——左右翻過去。

#### 備註
第 (2) 題用的是 $2 \times 2$ 的做法(資料矩陣只有兩列),不必升成齊次座標。學生常問「什麼時候要加那個 1?」答案是:**有平移時才需要**。

### 是非 · Lay 2.7 Exercise 16
Are $(1, -2, 3, 4)$ and $(10, -20, 30, 40)$ homogeneous coordinates for the same point in $\mathbb{R}^3$? Why or why not?

#### 解答
**是(Yes)。** 因為 $(10, -20, 30, 40) = 10 \cdot (1, -2, 3, 4)$,是非零純量倍。用公式 (1) 還原,兩者都是
$$\left(\tfrac{1}{4},\; -\tfrac{1}{2},\; \tfrac{3}{4}\right).$$

#### 備註
這題是「齊次座標不唯一」的觀念題。可以順便問:$(0, 0, 0, 0)$ 是誰的齊次座標?答案是沒有——$H = 0$ 不合法。

### 變化 · Lay 2.7 Exercises 3–4
In Exercises 3–8, find the $3 \times 3$ matrices that produce the described composite 2D transformations, using homogeneous coordinates.

(3) Translate by $(3, 1)$, and then rotate $45°$ about the origin.

(4) Translate by $(-3, 4)$ and then scale the $x$-coordinate by $.7$ and the $y$-coordinated by $1.3$.

#### 解答
(3) 平移先做(寫右邊),旋轉後做(寫左邊):
$$\begin{bmatrix} \tfrac{\sqrt2}{2} & -\tfrac{\sqrt2}{2} & 0 \\ \tfrac{\sqrt2}{2} & \tfrac{\sqrt2}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & 3 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac{\sqrt2}{2} & -\tfrac{\sqrt2}{2} & \sqrt2 \\ \tfrac{\sqrt2}{2} & \tfrac{\sqrt2}{2} & 2\sqrt2 \\ 0 & 0 & 1 \end{bmatrix}$$
第三行是平移向量 $(3, 1)$ **被旋轉後**的像,這正是「先平移」的後果。

(4)
$$\begin{bmatrix} .7 & 0 & 0 \\ 0 & 1.3 & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & -3 \\ 0 & 1 & 4 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} .7 & 0 & -2.1 \\ 0 & 1.3 & 5.2 \\ 0 & 0 & 1 \end{bmatrix}$$
平移量也被縮放了:$-3 \times .7 = -2.1$、$4 \times 1.3 = 5.2$。

#### 備註
(4) 的題幹原文印成 "the $y$-coordinated by 1.3",是 Global Edition 的錯字,應為 "$y$-coordinate"。照原文出題即可,學生問起再說明。

### 變化 · Lay 2.7 Exercises 5–6
(5) Reflect points through the $x$-axis, and then rotate $30°$ about the origin.

(6) Rotate points $30°$, and then reflect through the $x$-axis.

#### 解答
(5) 鏡射先做:
$$\begin{bmatrix} \tfrac{\sqrt3}{2} & -\tfrac12 & 0 \\ \tfrac12 & \tfrac{\sqrt3}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac{\sqrt3}{2} & \tfrac12 & 0 \\ \tfrac12 & -\tfrac{\sqrt3}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

(6) 旋轉先做:
$$\begin{bmatrix} 1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} \tfrac{\sqrt3}{2} & -\tfrac12 & 0 \\ \tfrac12 & \tfrac{\sqrt3}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac{\sqrt3}{2} & -\tfrac12 & 0 \\ -\tfrac12 & -\tfrac{\sqrt3}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

**兩個答案不一樣**——同樣兩個動作,順序不同結果不同。這就是 $AB \ne BA$ 的具體例子。

#### 備註
這兩題一定要連著做並把答案並排寫在黑板上。這是本週「乘法不可交換」最有說服力的證據,比抽象的反例好用得多。

### 變化 · Lay 2.7 Practice Problem
Rotation of a figure about a point $\mathbf{p}$ in $\mathbb{R}^2$ is accomplished by first translating the figure by $-\mathbf{p}$, rotating about the origin, and then translating back by $\mathbf{p}$. See Figure 7. Construct the $3 \times 3$ matrix that rotates points $-30°$ about the point $(-2, 6)$, using homogeneous coordinates.

#### 解答
三個動作由右往左:平移 $-\mathbf{p} = (2, -6)$ → 繞原點轉 $-30°$($\cos(-30°) = \tfrac{\sqrt3}{2}$、$\sin(-30°) = -\tfrac12$)→ 平移回 $\mathbf{p} = (-2, 6)$:

$$\begin{bmatrix} 1 & 0 & -2 \\ 0 & 1 & 6 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} \tfrac{\sqrt3}{2} & \tfrac12 & 0 \\ -\tfrac12 & \tfrac{\sqrt3}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & 2 \\ 0 & 1 & -6 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac{\sqrt3}{2} & \tfrac12 & \sqrt3 - 5 \\ -\tfrac12 & \tfrac{\sqrt3}{2} & -3\sqrt3 + 5 \\ 0 & 0 & 1 \end{bmatrix}$$

#### 備註
這是本節最重要的一題,遊戲裡「角色繞自己轉」就是這個公式。Exercises 7、8 是同一招換數字,建議課堂做完這題,兩題當作業。

### 變化 · Lay 2.7 Exercises 7–8
(7) Rotate points through $60°$ about the point $(6, 8)$.

(8) Rotate points through $45°$ about the point $(3, 7)$.

#### 解答
(7)
$$\begin{bmatrix} 1 & 0 & 6 \\ 0 & 1 & 8 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} \tfrac12 & -\tfrac{\sqrt3}{2} & 0 \\ \tfrac{\sqrt3}{2} & \tfrac12 & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & -6 \\ 0 & 1 & -8 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac12 & -\tfrac{\sqrt3}{2} & 3 + 4\sqrt3 \\ \tfrac{\sqrt3}{2} & \tfrac12 & 4 - 3\sqrt3 \\ 0 & 0 & 1 \end{bmatrix}$$

(8)
$$\begin{bmatrix} 1 & 0 & 3 \\ 0 & 1 & 7 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} \tfrac{\sqrt2}{2} & -\tfrac{\sqrt2}{2} & 0 \\ \tfrac{\sqrt2}{2} & \tfrac{\sqrt2}{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & -3 \\ 0 & 1 & -7 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac{\sqrt2}{2} & -\tfrac{\sqrt2}{2} & 3 + 2\sqrt2 \\ \tfrac{\sqrt2}{2} & \tfrac{\sqrt2}{2} & 7 - 5\sqrt2 \\ 0 & 0 & 1 \end{bmatrix}$$

兩題的第三行都等於 $\mathbf{p} - R\mathbf{p}$。

### 變化 · Lay 2.7 Exercise 15
What vector in $\mathbb{R}^3$ has homogeneous coordinates $\left(\tfrac14, -\tfrac{1}{12}, \tfrac{1}{18}, \tfrac{1}{36}\right)$?

#### 解答
$H = \tfrac{1}{36}$,把前三個分量各除以 $H$(即各乘 36):
$$(9,\; -3,\; 2)$$

### 變化 · Lay 2.7 Exercises 17–18
(17) Give the $4 \times 4$ matrix that rotates points in $\mathbb{R}^3$ about the $x$-axis through an angle of $60°$. (See the figure.)

(18) Give the $4 \times 4$ matrix that rotates points in $\mathbb{R}^3$ about the $z$-axis through an angle of $-30°$, and then translates by $\mathbf{p} = (5, -2, 1)$.

#### 解答
(17) 繞 $x$ 軸轉,$\mathbf{e}_1$ 不動,$yz$ 平面上做 $2 \times 2$ 旋轉:
$$\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & \tfrac12 & -\tfrac{\sqrt3}{2} & 0 \\ 0 & \tfrac{\sqrt3}{2} & \tfrac12 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

(18) $\cos(-30°) = \tfrac{\sqrt3}{2}$、$\sin(-30°) = -\tfrac12$,旋轉先做、平移後做:
$$\begin{bmatrix} 1 & 0 & 0 & 5 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} \tfrac{\sqrt3}{2} & \tfrac12 & 0 & 0 \\ -\tfrac12 & \tfrac{\sqrt3}{2} & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \tfrac{\sqrt3}{2} & \tfrac12 & 0 & 5 \\ -\tfrac12 & \tfrac{\sqrt3}{2} & 0 & -2 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

#### 備註
(17) 題目說 "See the figure.",課本 p. 178 那張繞軸的圓環圖只是用來說明正角的方向慣例:**從旋轉軸的正半軸看向原點時,逆時針為正**(Example 7a)。沒有那張圖也能作答,老師講解時把慣例寫在黑板上即可。

### 應用 · Lay 2.7 Exercise 9
A $2 \times 200$ data matrix $D$ contains the coordinates of 200 points. Compute the number of multiplications required to transform these points using two arbitrary $2 \times 2$ matrices $A$ and $B$. Consider the two possibilities $A(BD)$ and $(AB)D$. Discuss the implications of your results for computer graphics calculations.

#### 解答
- $A(BD)$:先算 $BD$ 需要 $2 \times 2 \times 200 = 800$ 次乘法,再乘 $A$ 又 800 次,合計 **1600 次**。
- $(AB)D$:先算 $AB$ 只要 $2 \times 2 \times 2 = 8$ 次,再乘 $D$ 要 800 次,合計 **808 次**。

第一種做法大約要兩倍的乘法。若 $D$ 有 20,000 行,兩者分別是 160,000 與 80,008 次。

**結論**:圖學計算一律**先把所有變換矩陣合成一個**,再套到全部頂點上。

#### 備註
這題是實作課計時實驗的理論版,務必在課堂上算一次。書後解答連 20,000 行的數字都給了,可以直接引用。

### 應用 · Lay 2.7 Exercises 19–20
(19) Let $S$ be the triangle with vertices $(4.2, 1.2, 4)$, $(6, 4, 2)$, $(2, 2, 6)$. Find the image of $S$ under the perspective projection with center of projection at $(0, 0, 10)$.

(20) Let $S$ be the triangle with vertices $(9, 3, -5)$, $(12, 8, 2)$, $(1.8, 2.7, 1)$. Find the image of $S$ under the perspective projection with center of projection at $(0, 0, 10)$.

#### 解答
用 $x^* = \dfrac{x}{1 - z/10}$、$y^* = \dfrac{y}{1 - z/10}$:

(19) 分母依序是 $.6$、$.8$、$.4$,得到 $(7, 2, 0)$、$(7.5, 5, 0)$、$(5, 5, 0)$。

(20) 分母依序是 $1.5$、$.8$、$.9$,得到 $(6, 2, 0)$、$(15, 10, 0)$、$(2, 3, 0)$。

#### 備註
(20) 的第一個頂點 $z = -5 < 0$,在螢幕後面(離眼睛更遠),分母大於 1,所以像被**縮小**;(20) 的第二點 $z = 2 > 0$ 靠近眼睛,像被放大。這一對比很適合用來解釋「近大遠小」。

### 應用 · Lay 2.7 Exercises 21–22(T 電腦題)
Exercises 21 and 22 concern the way in which color is specified for display in computer graphics. A color on a computer screen is encoded by three numbers $(R, G, B)$ that list the amount of energy an electron gun must transmit to red, green, and blue phosphor dots on the computer screen.

(21) Each computer screen manufacturer must convert between the $(R, G, B)$ data and an international CIE standard for color, which uses three primary colors, called $X$, $Y$, and $Z$. A typical conversion for short-persistence phosphors is

$$\begin{bmatrix} .61 & .29 & .150 \\ .35 & .59 & .063 \\ .04 & .12 & .787 \end{bmatrix}\begin{bmatrix} R \\ G \\ B \end{bmatrix} = \begin{bmatrix} X \\ Y \\ Z \end{bmatrix}$$

A computer program will send a stream of color information to the screen, using standard CIE data $(X, Y, Z)$. Find the equation that converts these data to the $(R, G, B)$ data needed for the screen's electron gun.

(22) The signal broadcast by commercial television describes each color by a vector $(Y, I, Q)$. The correspondence between $YIQ$ and a "standard" $RGB$ color is given by

$$\begin{bmatrix} Y \\ I \\ Q \end{bmatrix} = \begin{bmatrix} .299 & .587 & .114 \\ .596 & -.275 & -.321 \\ .212 & -.528 & .311 \end{bmatrix}\begin{bmatrix} R \\ G \\ B \end{bmatrix}$$

Find the equation that converts the $YIQ$ data transmitted by the television station to the $RGB$ data needed for the television screen.

#### 解答
兩題都是「已知 $M\mathbf{c}_1 = \mathbf{c}_2$,求反過來的式子」,答案是左乘 $M^{-1}$。

(21)
$$\begin{bmatrix} 2.2586 & -1.0395 & -.3473 \\ -1.3495 & 2.3441 & .0696 \\ .0910 & -.3046 & 1.2777 \end{bmatrix}\begin{bmatrix} X \\ Y \\ Z \end{bmatrix} = \begin{bmatrix} R \\ G \\ B \end{bmatrix}$$

(22)
$$\begin{bmatrix} R \\ G \\ B \end{bmatrix} = \begin{bmatrix} 1.0031 & .9548 & .6179 \\ .9968 & -.2707 & -.6448 \\ 1.0085 & -1.1105 & 1.6996 \end{bmatrix}\begin{bmatrix} Y \\ I \\ Q \end{bmatrix}$$

#### 備註
兩題都標了 T,實作課會用 `np.linalg.inv` 或 `Matrix.inv()` 算。(22) 算出的矩陣第一行幾乎是 $(1, 1, 1)$——這正是「黑白電視只取 $Y$ 就能得到灰階畫面」的數學理由,值得在課堂上點一下。

書後只給 (21) 的答案(四位小數,與上式相同),(22) 無解答。

### 挑戰 · Lay 2.7 Exercise 10
Consider the following geometric 2D transformations: $D$, a dilation (in which $x$-coordinates and $y$-coordinates are scaled by the same factor); $R$, a rotation; and $T$, a translation. Does $D$ commute with $R$? That is, is $D(R(\mathbf{x})) = R(D(\mathbf{x}))$ for all $\mathbf{x}$ in $\mathbb{R}^2$? Does $D$ commute with $T$? Does $R$ commute with $T$?

#### 解答
- **$D$ 與 $R$:可交換。** 伸張的矩陣是 $kI_2$,和任何矩陣都可交換:$D(R(\mathbf{x})) = k(R\mathbf{x}) = R(k\mathbf{x}) = R(D(\mathbf{x}))$。
- **$D$ 與 $T$:不可交換。** 設平移量是 $(h, l)$,齊次座標下
  $$DT = \begin{bmatrix} k & 0 & kh \\ 0 & k & kl \\ 0 & 0 & 1 \end{bmatrix}, \qquad TD = \begin{bmatrix} k & 0 & h \\ 0 & k & l \\ 0 & 0 & 1 \end{bmatrix}$$
  除非 $k = 1$ 或平移量為 $\mathbf{0}$,兩者不同:先縮放再平移,平移量不會被縮;先平移再縮放,平移量也被縮了 $k$ 倍。
- **$R$ 與 $T$:不可交換。** $RT$ 的第三行是 $R\mathbf{p}$,$TR$ 的第三行是 $\mathbf{p}$;除非 $\mathbf{p} = \mathbf{0}$ 或 $R = I$,兩者不同。

#### 備註
書上沒有給平移量的符號,解答裡用 $(h, l)$ 以免和縮放倍率 $k$ 撞名。這題把 Exercises 3–8 的現象講成通則,很適合當作業。

### 挑戰 · Lay 2.7 Exercise 11
A rotation on a computer screen is sometimes implemented as the product of two shear-and-scale transformations, which can speed up calculations that determine how a graphic image actually appears in terms of screen pixels. (The screen consists of rows and columns of small dots, called *pixels*.) The first transformation $A_1$ shears vertically and then compresses each column of pixels; the second transformation $A_2$ shears horizontally and then stretches each row of pixels. Let

$$A_1 = \begin{bmatrix} 1 & 0 & 0 \\ \sin\varphi & \cos\varphi & 0 \\ 0 & 0 & 1 \end{bmatrix}, \qquad A_2 = \begin{bmatrix} \sec\varphi & -\tan\varphi & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

Show that the composition of the two transformations is a rotation in $\mathbb{R}^2$.

#### 解答
先做 $A_1$、後做 $A_2$,所以算 $A_2A_1$:
$$A_2A_1 = \begin{bmatrix} \sec\varphi - \tan\varphi\sin\varphi & -\tan\varphi\cos\varphi & 0 \\ \sin\varphi & \cos\varphi & 0 \\ 0 & 0 & 1 \end{bmatrix}$$
再用課本提示的恆等式
$$\sec\varphi - \tan\varphi\sin\varphi = \frac{1}{\cos\varphi} - \frac{\sin^2\varphi}{\cos\varphi} = \frac{1 - \sin^2\varphi}{\cos\varphi} = \cos\varphi,$$
以及 $\tan\varphi\cos\varphi = \sin\varphi$,得到
$$A_2A_1 = \begin{bmatrix} \cos\varphi & -\sin\varphi & 0 \\ \sin\varphi & \cos\varphi & 0 \\ 0 & 0 & 1 \end{bmatrix}$$
正是繞原點逆時針轉 $\varphi$ 的旋轉矩陣。(需 $\cos\varphi \ne 0$。)

### 挑戰 · Lay 2.7 Exercise 12
A rotation in $\mathbb{R}^2$ usually requires four multiplications. Compute the product below, and show that the matrix for a rotation can be factored into three shear transformations (each of which requires only one multiplication).

$$\begin{bmatrix} 1 & -\tan\tfrac{\varphi}{2} & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 & 0 \\ \sin\varphi & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & -\tan\tfrac{\varphi}{2} & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

#### 解答
令 $t = \tan\tfrac{\varphi}{2}$、$s = \sin\varphi$。前兩個相乘得 $\begin{bmatrix} 1 - ts & -t \\ s & 1 \end{bmatrix}$(左上 $2 \times 2$ 部分),其中
$$1 - ts = 1 - 2\sin^2\tfrac{\varphi}{2} = \cos\varphi.$$
再乘第三個矩陣,右上角為
$$-t(1 - ts) - t = -t(1 + \cos\varphi) = -2\sin\tfrac{\varphi}{2}\cos\tfrac{\varphi}{2} = -\sin\varphi.$$
所以乘積是
$$\begin{bmatrix} \cos\varphi & -\sin\varphi & 0 \\ \sin\varphi & \cos\varphi & 0 \\ 0 & 0 & 1 \end{bmatrix}$$
旋轉被拆成三個剪切,每個剪切只需 1 次乘法,共 3 次,比直接旋轉的 4 次少一次。

#### 備註
題幹的 $-\tan\varphi/2$ 在書上排版成 $-\tan\dfrac{\varphi}{2}$,是**半角**,不是 $-(\tan\varphi)/2$。上課前要先講清楚,否則整題算不出來。

這題與 Exercise 11 合起來說明了一件事:同一個旋轉可以用不同方式實作,而實作方式的選擇是效能問題。早年的繪圖硬體乘法很貴,所以寧可多做幾個剪切。

### 挑戰 · Lay 2.7 Exercises 13–14
(13) The usual transformations on homogeneous coordinates for 2D computer graphics involve $3 \times 3$ matrices of the form $\begin{bmatrix} A & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}$ where $A$ is a $2 \times 2$ matrix and $\mathbf{p}$ is in $\mathbb{R}^2$. Show that such a transformation amounts to a linear transformation on $\mathbb{R}^2$ followed by a translation. [*Hint:* Find an appropriate matrix factorization involving partitioned matrices.]

(14) Show that the transformation in Exercise 7 is equivalent to a rotation about the origin followed by a translation by $\mathbf{p}$. Find $\mathbf{p}$.

#### 解答
(13) 把矩陣拆成兩個:
$$\begin{bmatrix} A & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix} = \begin{bmatrix} I & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}\begin{bmatrix} A & \mathbf{0} \\ \mathbf{0}^T & 1 \end{bmatrix}$$
右邊(先做)是純線性變換 $A$,左邊(後做)是平移 $\mathbf{p}$。或者直接驗算:
$$\begin{bmatrix} A & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}\begin{bmatrix} \mathbf{x} \\ 1 \end{bmatrix} = \begin{bmatrix} A\mathbf{x} + \mathbf{p} \\ 1 \end{bmatrix}$$

(14) 把 Exercise 7 的答案照 (13) 拆開:
$$\begin{bmatrix} \tfrac12 & -\tfrac{\sqrt3}{2} & 3 + 4\sqrt3 \\ \tfrac{\sqrt3}{2} & \tfrac12 & 4 - 3\sqrt3 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 3 + 4\sqrt3 \\ 0 & 1 & 4 - 3\sqrt3 \\ 0 & 0 & 1 \end{bmatrix}\begin{bmatrix} \tfrac12 & -\tfrac{\sqrt3}{2} & 0 \\ \tfrac{\sqrt3}{2} & \tfrac12 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$
所以 $\mathbf{p} = (3 + 4\sqrt3,\; 4 - 3\sqrt3) \approx (9.93,\, -1.20)$,即 $\mathbf{p} = (6,8) - R_{60°}(6,8)$。

#### 備註
Exercise 13 就是「仿射變換 = 線性變換 + 平移」,是本節的收束定理,值得單獨講一次。Exercise 14 必須先做過 Exercise 7。

## 驗算
```check
Matrix([[1, Rational(1,4), 0], [0, 1, 0], [0, 0, 1]]) * Matrix([x, y, 1]) == Matrix([x + Rational(1,4)*y, y, 1])
Matrix([[-1, 0], [0, 1]]) * Matrix([[5, 2, 4], [0, 2, 3]]) == Matrix([[-5, -2, -4], [0, 2, 3]])
Matrix([[1, Rational(1,4)], [0, 1]]) * Matrix([[0, Rational(1,2), Rational(1,2), 6, 6, Rational(11,2), Rational(11,2), 0], [0, 0, Rational(321,50), 0, 8, 8, Rational(79,50), 8]]) == Matrix([[0, Rational(1,2), Rational(421,200), 6, 8, Rational(15,2), Rational(1179,200), 2], [0, 0, Rational(321,50), 0, 8, 8, Rational(79,50), 8]])
Matrix([[Rational(3,4), 0], [0, 1]]) * Matrix([[1, Rational(1,4)], [0, 1]]) == Matrix([[Rational(3,4), Rational(3,16)], [0, 1]])
Matrix([[1, 0, Rational(-1,2)], [0, 1, 2], [0, 0, 1]]) * Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) * Matrix([[Rational(3,10), 0, 0], [0, Rational(3,10), 0], [0, 0, 1]]) == Matrix([[0, Rational(-3,10), Rational(-1,2)], [Rational(3,10), 0, 2], [0, 0, 1]])
simplify(Matrix([[cos(pi/4), -sin(pi/4), 0], [sin(pi/4), cos(pi/4), 0], [0, 0, 1]]) * Matrix([[1, 0, 3], [0, 1, 1], [0, 0, 1]]) - Matrix([[sqrt(2)/2, -sqrt(2)/2, sqrt(2)], [sqrt(2)/2, sqrt(2)/2, 2*sqrt(2)], [0, 0, 1]])) == zeros(3, 3)
Matrix([[Rational(7,10), 0, 0], [0, Rational(13,10), 0], [0, 0, 1]]) * Matrix([[1, 0, -3], [0, 1, 4], [0, 0, 1]]) == Matrix([[Rational(7,10), 0, Rational(-21,10)], [0, Rational(13,10), Rational(26,5)], [0, 0, 1]])
simplify(Matrix([[cos(pi/6), -sin(pi/6), 0], [sin(pi/6), cos(pi/6), 0], [0, 0, 1]]) * Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]]) - Matrix([[sqrt(3)/2, Rational(1,2), 0], [Rational(1,2), -sqrt(3)/2, 0], [0, 0, 1]])) == zeros(3, 3)
simplify(Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]]) * Matrix([[cos(pi/6), -sin(pi/6), 0], [sin(pi/6), cos(pi/6), 0], [0, 0, 1]]) - Matrix([[sqrt(3)/2, -Rational(1,2), 0], [-Rational(1,2), -sqrt(3)/2, 0], [0, 0, 1]])) == zeros(3, 3)
simplify(Matrix([[1, 0, -2], [0, 1, 6], [0, 0, 1]]) * Matrix([[cos(-pi/6), -sin(-pi/6), 0], [sin(-pi/6), cos(-pi/6), 0], [0, 0, 1]]) * Matrix([[1, 0, 2], [0, 1, -6], [0, 0, 1]]) - Matrix([[sqrt(3)/2, Rational(1,2), sqrt(3)-5], [-Rational(1,2), sqrt(3)/2, 5-3*sqrt(3)], [0, 0, 1]])) == zeros(3, 3)
simplify(Matrix([[1, 0, 6], [0, 1, 8], [0, 0, 1]]) * Matrix([[cos(pi/3), -sin(pi/3), 0], [sin(pi/3), cos(pi/3), 0], [0, 0, 1]]) * Matrix([[1, 0, -6], [0, 1, -8], [0, 0, 1]]) - Matrix([[Rational(1,2), -sqrt(3)/2, 3+4*sqrt(3)], [sqrt(3)/2, Rational(1,2), 4-3*sqrt(3)], [0, 0, 1]])) == zeros(3, 3)
simplify(Matrix([[1, 0, 3], [0, 1, 7], [0, 0, 1]]) * Matrix([[cos(pi/4), -sin(pi/4), 0], [sin(pi/4), cos(pi/4), 0], [0, 0, 1]]) * Matrix([[1, 0, -3], [0, 1, -7], [0, 0, 1]]) - Matrix([[sqrt(2)/2, -sqrt(2)/2, 3+2*sqrt(2)], [sqrt(2)/2, sqrt(2)/2, 7-5*sqrt(2)], [0, 0, 1]])) == zeros(3, 3)
[Rational(1,4)/Rational(1,36), Rational(-1,12)/Rational(1,36), Rational(1,18)/Rational(1,36)] == [9, -3, 2]
[Rational(1,4), Rational(-2,4), Rational(3,4)] == [Rational(10,40), Rational(-20,40), Rational(30,40)]
simplify(Matrix([[1, 0, 0, 0], [0, cos(pi/3), -sin(pi/3), 0], [0, sin(pi/3), cos(pi/3), 0], [0, 0, 0, 1]]) - Matrix([[1, 0, 0, 0], [0, Rational(1,2), -sqrt(3)/2, 0], [0, sqrt(3)/2, Rational(1,2), 0], [0, 0, 0, 1]])) == zeros(4, 4)
simplify(Matrix([[1, 0, 0, 5], [0, 1, 0, -2], [0, 0, 1, 1], [0, 0, 0, 1]]) * Matrix([[cos(-pi/6), -sin(-pi/6), 0, 0], [sin(-pi/6), cos(-pi/6), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) - Matrix([[sqrt(3)/2, Rational(1,2), 0, 5], [-Rational(1,2), sqrt(3)/2, 0, -2], [0, 0, 1, 1], [0, 0, 0, 1]])) == zeros(4, 4)
(2*2*200 + 2*2*200 == 1600) and (2*2*2 + 2*2*200 == 808)
[[Rational(42,10)/(1-Rational(4,10)), Rational(12,10)/(1-Rational(4,10))], [6/(1-Rational(2,10)), 4/(1-Rational(2,10))], [2/(1-Rational(6,10)), 2/(1-Rational(6,10))]] == [[7, 2], [Rational(15,2), 5], [5, 5]]
[[9/(1+Rational(5,10)), 3/(1+Rational(5,10))], [12/(1-Rational(2,10)), 8/(1-Rational(2,10))], [Rational(18,10)/(1-Rational(1,10)), Rational(27,10)/(1-Rational(1,10))]] == [[6, 2], [15, 10], [2, 3]]
bool(max(abs(v) for v in (Matrix([[Rational(61,100), Rational(29,100), Rational(15,100)], [Rational(35,100), Rational(59,100), Rational(63,1000)], [Rational(4,100), Rational(12,100), Rational(787,1000)]]).inv() - Matrix([[Rational(22586,10000), Rational(-10395,10000), Rational(-3473,10000)], [Rational(-13495,10000), Rational(23441,10000), Rational(696,10000)], [Rational(910,10000), Rational(-3046,10000), Rational(12777,10000)]]))) < Rational(1,10000))
bool(max(abs(v) for v in (Matrix([[Rational(299,1000), Rational(587,1000), Rational(114,1000)], [Rational(596,1000), Rational(-275,1000), Rational(-321,1000)], [Rational(212,1000), Rational(-528,1000), Rational(311,1000)]]).inv() - Matrix([[Rational(10031,10000), Rational(9548,10000), Rational(6179,10000)], [Rational(9968,10000), Rational(-2707,10000), Rational(-6448,10000)], [Rational(10085,10000), Rational(-11105,10000), Rational(16996,10000)]]))) < Rational(1,10000))
simplify(Matrix([[k, 0, 0], [0, k, 0], [0, 0, 1]]) * Matrix([[cos(t), -sin(t), 0], [sin(t), cos(t), 0], [0, 0, 1]]) - Matrix([[cos(t), -sin(t), 0], [sin(t), cos(t), 0], [0, 0, 1]]) * Matrix([[k, 0, 0], [0, k, 0], [0, 0, 1]])) == zeros(3, 3)
simplify(Matrix([[sec(t), -tan(t), 0], [0, 1, 0], [0, 0, 1]]) * Matrix([[1, 0, 0], [sin(t), cos(t), 0], [0, 0, 1]]) - Matrix([[cos(t), -sin(t), 0], [sin(t), cos(t), 0], [0, 0, 1]])) == zeros(3, 3)
simplify(expand_trig(Matrix([[1, -tan(t), 0], [0, 1, 0], [0, 0, 1]]) * Matrix([[1, 0, 0], [sin(2*t), 1, 0], [0, 0, 1]]) * Matrix([[1, -tan(t), 0], [0, 1, 0], [0, 0, 1]]) - Matrix([[cos(2*t), -sin(2*t), 0], [sin(2*t), cos(2*t), 0], [0, 0, 1]]))) == zeros(3, 3)
Matrix([[1, 0, h], [0, 1, k], [0, 0, 1]]) * Matrix([[a, b, 0], [c, d, 0], [0, 0, 1]]) == Matrix([[a, b, h], [c, d, k], [0, 0, 1]])
simplify(Matrix([[1, 0, 3+4*sqrt(3)], [0, 1, 4-3*sqrt(3)], [0, 0, 1]]) * Matrix([[cos(pi/3), -sin(pi/3), 0], [sin(pi/3), cos(pi/3), 0], [0, 0, 1]]) - Matrix([[Rational(1,2), -sqrt(3)/2, 3+4*sqrt(3)], [sqrt(3)/2, Rational(1,2), 4-3*sqrt(3)], [0, 0, 1]])) == zeros(3, 3)
```
