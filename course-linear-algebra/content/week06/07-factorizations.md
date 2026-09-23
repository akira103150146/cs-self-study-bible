---
title_en: Other Factorizations and Ladder Networks
title_zh: 其他分解與梯形電路
sub: A preview of QR, SVD, and spectral factorizations
level: mid
supplement: true
source: Lay 2.5
lab_hook: '`np.linalg.qr`、`np.linalg.svd`:後面幾週的主角,這裡先看一眼'
---
## 觀念
Matrix factorizations and, later, factorizations of linear transformations will appear at a number of key points throughout the text. Several other factorizations, to be studied later, are introduced in the exercises:

- **Rank factorization** $A = CD$ ($C$ is $m \times r$, $D$ is $r \times n$) — Exercise 23, used again in Section 7.4.
- **QR factorization** $A = QR$ where $Q^TQ = I$ and $R$ is upper triangular — Exercise 24, studied in Section 6.4.
- **Singular value decomposition** $A = UDV^T$ — Exercise 25, studied in Section 7.4.
- **Spectral factorization** $A = PDP^{-1}$ with $D$ diagonal — Exercise 26, studied in Section 5.3.

**Ladder networks.** Suppose the box in Figure 3 represents some sort of electric circuit, with an input and output. Record the input voltage and current by $\begin{bmatrix} v_1 \\ i_1 \end{bmatrix}$ and the output by $\begin{bmatrix} v_2 \\ i_2 \end{bmatrix}$. Frequently, the transformation $\begin{bmatrix} v_1 \\ i_1 \end{bmatrix} \mapsto \begin{bmatrix} v_2 \\ i_2 \end{bmatrix}$ is linear. That is, there is a matrix $A$, called the *transfer matrix*, such that

$$\begin{bmatrix} v_2 \\ i_2 \end{bmatrix} = A\begin{bmatrix} v_1 \\ i_1 \end{bmatrix}$$

Using Ohm's law and Kirchhoff's laws, one can show that the transfer matrices of the series and shunt circuits are

$$\begin{bmatrix} 1 & -R_1 \\ 0 & 1 \end{bmatrix} \quad\text{(series)} \qquad\text{and}\qquad \begin{bmatrix} 1 & 0 \\ -1/R_2 & 1 \end{bmatrix} \quad\text{(shunt)}$$

The series connection of the circuits corresponds to composition of linear transformations, and the transfer matrix of the ladder network is (note the order)

$$A_2A_1 = \begin{bmatrix} 1 & 0 \\ -1/R_2 & 1 \end{bmatrix}\begin{bmatrix} 1 & -R_1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & -R_1 \\ -1/R_2 & 1 + R_1/R_2 \end{bmatrix} \tag{6}$$

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| rank factorization | 秩分解 | 把 $A$ 拆成「瘦」與「扁」兩個矩陣,省記憶體 |
| outer product | 外積 | $\mathbf{c}\mathbf{d}^T$,秩至多 1 的矩陣 |
| QR factorization | QR 分解 | $Q$ 的行互相垂直,$R$ 上三角(第 14 週) |
| singular value decomposition | 奇異值分解 | $A = UDV^T$(第 16 週,本課的終點) |
| spectral factorization | 譜分解 | $A = PDP^{-1}$,算 $A^k$ 的利器(第 11 週) |
| transfer matrix | 轉移矩陣 | 電路的「輸入 → 輸出」矩陣 |
| series / shunt circuit | 串聯 / 並聯電路 | 電阻接在主線上 / 接在兩線之間 |
| ladder network | 梯形網路 | 一段接一段的電路,像梯子 |

## 白話說
這個觀念是**補充**,做兩件事:**預告後面幾週的分解**,以及**看一個「把矩陣拆開就是在設計硬體」的應用**。

**分解是什麼?** 把一個矩陣寫成幾個「形狀特別」的矩陣相乘。為什麼值得做?因為特別的形狀讓計算變便宜:

| 分解 | 形狀 | 好處 | 本課哪一週 |
|---|---|---|---|
| $A = LU$ | 下三角 × 上三角 | 解方程組 $O(n^2)$ | 本週 |
| $A = CD$ | 瘦 × 扁 | 省記憶體(秩小時) | 第 16 週 |
| $A = QR$ | 正交 × 上三角 | 最小平方法、數值穩定 | 第 14 週 |
| $A = PDP^{-1}$ | 對角線在中間 | $A^k = PD^kP^{-1}$ | 第 11 週 |
| $A = UDV^T$ | 正交 × 對角 × 正交 | 壓縮、降維、萬用 | 第 16 週 |

**為什麼 $A = CD$ 省記憶體?**(Exercise 23)$A$ 是 $400 \times 100$ 有 40,000 個數字;若 $A = CD$ 且 $C$ 是 $400 \times 4$、$D$ 是 $4 \times 100$,只要存 $1600 + 400 = 2000$ 個數字——**5%**。這就是影像壓縮與推薦系統的基本想法。

**梯形電路**:一段電路把「輸入的電壓與電流」變成「輸出的電壓與電流」,而且這個變換是線性的,所以是一個 $2 \times 2$ 矩陣。

![課本 2.5 Figure 4:一個串聯電路接一個並聯電路。](ladder.svg)

**把好幾段接起來 = 矩陣相乘**,而且**先經過的電路寫在右邊**(又是第 5 週的順序規則)。於是:

- **分析**:給你電路,乘出轉移矩陣。
- **設計**:給你想要的轉移矩陣,**把它分解**成幾個基本電路的矩陣相乘——分解出來的每個因子就是一個零件。

**這就是「矩陣分解 = 設計」的具體例子**:分解不只是計算技巧,它告訴你「這個東西可以用哪些零件組出來」。

## 在資工哪裡用
- **低秩近似**:$A \approx CD$ 是推薦系統(把「使用者 × 商品」的大矩陣拆成兩個小的)、影像壓縮、模型壓縮(LoRA 微調大型語言模型用的就是低秩矩陣)的共同骨架。
- **$A^k$ 算長期行為**:譜分解讓 $A^{100}$ 只要兩次矩陣乘法(Exercise 26)。PageRank、Markov 鏈、費氏數列閉式都靠它。
- **訊號處理的級聯濾波器**:一串濾波器接起來,總效果是轉移矩陣相乘——和梯形電路完全同構。設計濾波器時做的就是「把目標矩陣分解成可實作的零件」。
- **電路模擬軟體**:SPICE 這類工具內部就是在組裝並求解這種矩陣。

## 原理
**Exercise 23(a):$A = CD$ 就是四個外積的和。** 把 $C$ 按行切、$D$ 按列切:

$$A = CD = [\,\mathbf{c}_1 \;\; \mathbf{c}_2 \;\; \mathbf{c}_3 \;\; \mathbf{c}_4\,]\begin{bmatrix} \mathbf{d}_1^T \\ \mathbf{d}_2^T \\ \mathbf{d}_3^T \\ \mathbf{d}_4^T \end{bmatrix} = \mathbf{c}_1\mathbf{d}_1^T + \mathbf{c}_2\mathbf{d}_2^T + \mathbf{c}_3\mathbf{d}_3^T + \mathbf{c}_4\mathbf{d}_4^T$$

每一項 $\mathbf{c}_j\mathbf{d}_j^T$ 都是第 5 週學過的**外積**,秩至多 1。所以「秩 4 的矩陣 = 四個秩 1 的矩陣相加」。第 16 週的 SVD 會把這件事做到極致:**用最好的 $k$ 個秩 1 矩陣逼近 $A$**。

**Exercise 26:為什麼 $A = PDP^{-1}$ 讓 $A^k$ 變簡單?**

$$A^2 = (PDP^{-1})(PDP^{-1}) = PD(P^{-1}P)DP^{-1} = PD^2P^{-1}$$

中間的 $P^{-1}P$ 消掉了。歸納可得

$$A^k = PD^kP^{-1}$$

而 $D$ 是對角矩陣,$D^k$ 只要把對角元各自取 $k$ 次方。所以算 $A^{100}$ 只需 **2 次矩陣乘法 + 3 個純量次方**,而不是 99 次矩陣乘法。

**Exercise 28:三個並聯電路接起來還是一個並聯電路。**

$$\begin{bmatrix} 1 & 0 \\ -1/R_3 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_2 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_1 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ -\left(\frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3}\right) & 1 \end{bmatrix}$$

這正是單一並聯電路的形狀,其中 $\dfrac1R = \dfrac1{R_1} + \dfrac1{R_2} + \dfrac1{R_3}$——**就是物理課學過的並聯電阻公式**。矩陣乘法自動把它算出來了。

## 老師講解
### 例 1 · Lay 2.5 Example 3
Compute the transfer matrix of the ladder network in Figure 4 (a series circuit with resistance $R_1$ followed by a shunt circuit with resistance $R_2$). Then design a ladder network whose transfer matrix is $\begin{bmatrix} 1 & -8 \\ -.5 & 5 \end{bmatrix}$.

1. **先確認順序**:電流先經過串聯電路($A_1$),再經過並聯電路($A_2$)。所以整體是 $A_2A_1$——**先做的寫右邊**。
2. **乘出來**:
   $$A_2A_1 = \begin{bmatrix} 1 & 0 \\ -1/R_2 & 1 \end{bmatrix}\begin{bmatrix} 1 & -R_1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & -R_1 \\ -1/R_2 & 1 + R_1/R_2 \end{bmatrix}$$
3. **設計題反過來做**:要湊出 $\begin{bmatrix} 1 & -8 \\ -.5 & 5 \end{bmatrix}$,就把它**分解**成上面那個形狀。
4. **比對右上角**:$-R_1 = -8 \Rightarrow R_1 = 8$ ohms。
5. **比對左下角**:$-1/R_2 = -.5 \Rightarrow R_2 = 2$ ohms。
6. **檢查右下角**:$1 + R_1/R_2 = 1 + 8/2 = 5$ ✓ 和目標一致。
7. **結論**:先接一個 8 ohms 的串聯電阻,再接一個 2 ohms 的並聯電阻。
8. **這題在示範什麼?** **分解 = 設計**。把目標矩陣拆成基本零件的乘積,拆出來的每個因子就對應一個實體零件。

### 例 2 · Lay 2.5 Exercise 29
(a) Compute the transfer matrix of the network in the figure (shunt $R_1$ → series $R_2$ → shunt $R_3$). (b) Let $A = \begin{bmatrix} 4/3 & -12 \\ -1/4 & 3 \end{bmatrix}$. Design a ladder network whose transfer matrix is $A$ by finding a suitable matrix factorization of $A$.

1. **(a) 三段,順序反過來乘**:
   $$\begin{bmatrix} 1 & 0 \\ -1/R_3 & 1 \end{bmatrix}\begin{bmatrix} 1 & -R_2 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_1 & 1 \end{bmatrix} = \begin{bmatrix} 1 + R_2/R_1 & -R_2 \\ -\dfrac{1}{R_1} - \dfrac{R_2}{R_1R_3} - \dfrac{1}{R_3} & 1 + \dfrac{R_2}{R_3} \end{bmatrix}$$
2. **(b) 比對右上角**:$-R_2 = -12 \Rightarrow R_2 = 12$。
3. **比對左上角**:$1 + 12/R_1 = 4/3 \Rightarrow 12/R_1 = 1/3 \Rightarrow R_1 = 36$。
4. **比對右下角**:$1 + 12/R_3 = 3 \Rightarrow R_3 = 6$。
5. **驗算左下角**(這一格沒用到,正好拿來檢查):
   $$-\frac{1}{36} - \frac{12}{36 \cdot 6} - \frac16 = -\frac{1}{36} - \frac{2}{36} - \frac{6}{36} = -\frac14 \;\checkmark$$
6. **答案**:shunt 36 ohms → series 12 ohms → shunt 6 ohms。
7. **教學重點**:四個格子只用了三個來解,**剩下那一格是免費的檢查**。設計題常常這樣——未知數比方程式少,多出來的式子就是驗算。

### 例 3 · Lay 2.5 Exercise 26
Suppose a $3 \times 3$ matrix $A$ admits a factorization as $A = PDP^{-1}$, where $P$ is some invertible $3 \times 3$ matrix and $D$ is the diagonal matrix

$$D = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1/2 & 0 \\ 0 & 0 & 1/3 \end{bmatrix}$$

Show that this factorization is useful when computing high powers of $A$. Find fairly simple formulas for $A^2$, $A^3$, and $A^k$.

1. **算 $A^2$,把括號重排**:
   $$A^2 = (PDP^{-1})(PDP^{-1}) = PD(P^{-1}P)DP^{-1} = PD \cdot I \cdot DP^{-1} = PD^2P^{-1}$$
2. **中間的 $P^{-1}P$ 消掉了**,這是全題的關鍵。
3. **同理** $A^3 = PD^3P^{-1}$,一般地 $A^k = PD^kP^{-1}$。
4. **$D^k$ 有多好算?** 對角矩陣的次方就是每個對角元各自取次方:
   $$D^k = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1/2^k & 0 \\ 0 & 0 & 1/3^k \end{bmatrix}$$
5. **所以**
   $$A^2 = P\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1/4 & 0 \\ 0 & 0 & 1/9 \end{bmatrix}P^{-1}, \qquad A^{100} = P\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1/2^{100} & 0 \\ 0 & 0 & 1/3^{100} \end{bmatrix}P^{-1}$$
6. **成本對比**:直接算 $A^{100}$ 要 99 次矩陣乘法;用這個分解只要 2 次矩陣乘法加幾個純量次方。
7. **順帶看出長期行為**:$k \to \infty$ 時 $D^k \to \operatorname{diag}(1, 0, 0)$,所以 $A^k$ 收斂到 $P\operatorname{diag}(1,0,0)P^{-1}$。**第 11、12 週的 Markov 鏈與 PageRank 就是這件事**,而找出 $P$ 與 $D$ 正是第 10 週「特徵值」要做的。

#### 備註
例 3 是第 11 週的預告,講了學生會對後面的課有期待感。若時間不夠,只講第 1、2、6 步(消掉中間、省很多次乘法)就夠。

## 易錯點
- **電路的順序寫反**:先經過的寫在**右邊**。和第 5 週的合成變換同一個規則。
- **把 "connected in series"(串接成梯形)當成「串聯電阻」**。Exercise 28 的三個 shunt 接成梯形,等效結果是三個電阻**並聯**——用語很容易混淆。
- **$A^k = P^kD^kP^{-k}$**。錯。中間的 $P^{-1}P$ 會消掉,正確的是 $PD^kP^{-1}$。
- **以為 $A = CD$ 一定省記憶體**。只有 $r$ 遠小於 $m, n$ 時才省。
- 設計題只比對到剛好夠的格子就收工,不做剩下那格的檢查。

## 教學提示
**這是補充觀念,180 分鐘的節奏表裡沒有排它。** 若時間允許(或某個班級對電路特別有感),挑例 1 與例 3 講 15 分鐘即可。

若完全略過,要記得跟學生說:Exercises 22–30 是自學題,Exercises 31–32 會在實作課做。

真的要講的話,**例 3(譜分解)的優先度高於電路**,因為它直接接到第 11 週,而且那個「中間消掉」的技巧在後面用非常多次。

電路的部分若要講,建議只做例 1(兩段),例 2 的三段留作業——它的代數比較繁瑣,課堂做會拖很久。

## 練習
### 照做 · Lay 2.5 Exercise 22
(*Reduced LU Factorization*) With $A$ as in the Practice Problem, find a $5 \times 3$ matrix $B$ and a $3 \times 4$ matrix $C$ such that $A = BC$. Generalize this idea to the case where $A$ is $m \times n$, $A = LU$, and $U$ has only three nonzero rows.

#### 解答
取 $B$ = Practice Problem 裡 $L$ 的**前三行**、$C$ = $U$ 的**前三列**:

$$B = \begin{bmatrix} 1 & 0 & 0 \\ 3 & 1 & 0 \\ 1 & -1 & 1 \\ 2 & 2 & -1 \\ -3 & -3 & 2 \end{bmatrix}, \qquad C = \begin{bmatrix} 2 & -4 & -2 & 3 \\ 0 & 3 & 1 & -1 \\ 0 & 0 & 0 & 5 \end{bmatrix}$$

**一般化**:若 $A = LU$ 而 $U$ 只有 3 個非零列,那麼 $U$ 的第 4 列以下全是 0,乘法時 $L$ 的第 4 行以後只會乘到 0,可以整批丟掉。取 $B$ = $L$ 的前 3 行($m \times 3$)、$C$ = $U$ 的前 3 列($3 \times n$),就有 $A = BC$。

#### 備註
必須先做完上一個觀念的 Practice Problem 才能做這題(題目明講 "With $A$ as in the Practice Problem")。

這題是**低秩表示**的第一個例子:原本 $5 \times 4 = 20$ 個數字,現在用 $15 + 12 = 27$ 個——這個例子沒省到,但矩陣大、秩小時就差很多(見 Exercise 23)。

### 變化 · Lay 2.5 Exercises 23–24
(23) (*Rank Factorization*) Suppose an $m \times n$ matrix $A$ admits a factorization $A = CD$ where $C$ is $m \times 4$ and $D$ is $4 \times n$.

- **a.** Show that $A$ is the sum of four outer products. (See Section 2.4.)
- **b.** Let $m = 400$ and $n = 100$. Explain why a computer programmer might prefer to store the data from $A$ in the form of two matrices $C$ and $D$.

(24) (*QR Factorization*) Suppose $A = QR$, where $Q$ and $R$ are $n \times n$, $R$ is invertible and upper triangular, and $Q$ has the property that $Q^TQ = I$. Show that for each $\mathbf{b}$ in $\mathbb{R}^n$, the equation $A\mathbf{x} = \mathbf{b}$ has a unique solution. What computations with $Q$ and $R$ will produce the solution?

#### 解答
(23) **a.** 把 $C$ 按行切、$D$ 按列切,由分塊乘法
$$A = CD = \mathbf{c}_1\mathbf{d}_1^T + \mathbf{c}_2\mathbf{d}_2^T + \mathbf{c}_3\mathbf{d}_3^T + \mathbf{c}_4\mathbf{d}_4^T$$
每一項都是外積,秩至多 1。

**b.** $A$ 有 $400 \times 100 = 40{,}000$ 個元素;$C$ 有 $1600$ 個、$D$ 有 $400$ 個,合計 $2000$ 個,只占 **5%**。用 $C$、$D$ 儲存可省下 95% 的記憶體。

(24) $Q$ 是 $n \times n$ 且 $Q^TQ = I$,由 IMT(觀念 1 的 (j))知 $Q$ 可逆且 $Q^{-1} = Q^T$。$R$ 依假設可逆,所以 $A = QR$ 是兩個可逆矩陣的乘積 ⇒ $A$ 可逆 ⇒ 對每個 $\mathbf{b}$ 有唯一解
$$\mathbf{x} = A^{-1}\mathbf{b} = R^{-1}Q^{-1}\mathbf{b} = R^{-1}Q^T\mathbf{b}$$
**實際計算**:先算 $\mathbf{y} = Q^T\mathbf{b}$(一次矩陣–向量乘法),再用**回代法**解上三角系統 $R\mathbf{x} = \mathbf{y}$。完全不必求反矩陣。

#### 備註
(23) 是第 16 週低秩近似的伏筆:SVD 會告訴我們「用 $k$ 個外積能逼近得多好」。

(24) 注意 $Q^{-1} = Q^T$ 這件事——**轉置就是反矩陣**,這是正交矩陣最好用的性質,第 13、14 週會大量使用。

### 變化 · Lay 2.5 Exercises 25–26
(25) (*Singular Value Decomposition*) Suppose $A = UDV^T$, where $U$ and $V$ are $n \times n$ matrices with the property that $U^TU = I$ and $V^TV = I$, and where $D$ is a diagonal matrix with positive numbers $\sigma_1, \dots, \sigma_n$ on the diagonal. Show that $A$ is invertible, and find a formula for $A^{-1}$.

(26) (*Spectral Factorization*) Suppose a $3 \times 3$ matrix $A$ admits a factorization as $A = PDP^{-1}$, where $P$ is some invertible $3 \times 3$ matrix and $D$ is the diagonal matrix $\operatorname{diag}(1,\ 1/2,\ 1/3)$. Show that this factorization is useful when computing high powers of $A$. Find fairly simple formulas for $A^2$, $A^3$, and $A^k$ ($k$ a positive integer), using $P$ and the entries in $D$.

#### 解答
(25) $U^TU = I$ 且 $U$ 是方陣 ⇒ $U$ 可逆、$U^{-1} = U^T$;同理 $V$ 可逆、$V^{-1} = V^T$,所以 $V^T$ 也可逆且 $(V^T)^{-1} = V$。$D$ 的對角元 $\sigma_i > 0$ 全非零 ⇒ $D$ 可逆,$D^{-1} = \operatorname{diag}(1/\sigma_1, \dots, 1/\sigma_n)$。

三個可逆矩陣的乘積可逆,所以 $A$ 可逆,而且(反序!)
$$A^{-1} = (UDV^T)^{-1} = (V^T)^{-1}D^{-1}U^{-1} = V\,D^{-1}\,U^T$$

(26) $A^k = PD^kP^{-1}$,因為中間的 $P^{-1}P$ 會消掉。而 $D^k$ 只要把對角元各取 $k$ 次方:
$$A^2 = P\operatorname{diag}(1,\ 1/4,\ 1/9)P^{-1}, \quad A^3 = P\operatorname{diag}(1,\ 1/8,\ 1/27)P^{-1}, \quad A^k = P\operatorname{diag}(1,\ 1/2^k,\ 1/3^k)P^{-1}$$
算 $A^k$ 只需 2 次矩陣乘法加 3 個純量次方,不必做 $k-1$ 次矩陣乘法。

#### 備註
(25) 的 $A^{-1} = VD^{-1}U^T$ 是第 16 週 pseudoinverse 的前身;注意反序與「轉置即反矩陣」兩件事都用上了。

(26) 順帶可以看出 $k \to \infty$ 時 $D^k \to \operatorname{diag}(1, 0, 0)$,這正是第 11、12 週 Markov 鏈收斂的機制。

### 應用 · Lay 2.5 Exercises 27–28
(27) Design two different ladder networks that each output 9 volts and 4 amps when the input is 12 volts and 6 amps.

(28) Show that if three shunt circuits (with resistances $R_1$, $R_2$, $R_3$) are connected in series, the resulting network has the same transfer matrix as a single shunt circuit. Find a formula for the resistance in that circuit.

#### 解答
(27) 要找轉移矩陣 $A$ 使 $A\begin{bmatrix} 12 \\ 6 \end{bmatrix} = \begin{bmatrix} 9 \\ 4 \end{bmatrix}$。答案不唯一,兩組是:

**網路一**:先 series $R_1 = \tfrac12$ ohm,再 shunt $R_2 = \tfrac92$ ohms。
$$A = \begin{bmatrix} 1 & 0 \\ -2/9 & 1 \end{bmatrix}\begin{bmatrix} 1 & -1/2 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & -1/2 \\ -2/9 & 10/9 \end{bmatrix}$$

**網路二**:先 shunt $R_1 = 6$ ohms,再 series $R_2 = \tfrac34$ ohm。
$$A = \begin{bmatrix} 1 & -3/4 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/6 & 1 \end{bmatrix} = \begin{bmatrix} 9/8 & -3/4 \\ -1/6 & 1 \end{bmatrix}$$

兩者都滿足 $A(12, 6) = (9, 4)$。

(28)
$$\begin{bmatrix} 1 & 0 \\ -1/R_3 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_2 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_1 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ -\left(\frac{1}{R_1}+\frac{1}{R_2}+\frac{1}{R_3}\right) & 1 \end{bmatrix}$$
正是單一 shunt circuit 的形狀,其中
$$\frac1R = \frac1{R_1} + \frac1{R_2} + \frac1{R_3}, \qquad R = \frac{R_1R_2R_3}{R_1R_2 + R_1R_3 + R_2R_3}$$

#### 備註
(27) 的答案不唯一,學生只要找到兩組不同且都正確的即可。注意**矩陣相乘的順序與電流經過的順序相反**。

(28) 算出來就是物理課的並聯電阻公式。題目用的 "connected in series" 指的是「一段接一段」的梯形連接,等效卻是電阻並聯——這個用語要特別說明,否則學生會以為算錯。

### 挑戰 · Lay 2.5 Exercises 29–30
(29)

- **a.** Compute the transfer matrix of the network in the figure (a shunt circuit with resistance $R_1$, then a series circuit with resistance $R_2$, then a shunt circuit with resistance $R_3$).
- **b.** Let $A = \begin{bmatrix} 4/3 & -12 \\ -1/4 & 3 \end{bmatrix}$. Design a ladder network whose transfer matrix is $A$ by finding a suitable matrix factorization of $A$.

(30) Find a different factorization of the $A$ in Exercise 29, and thereby design a different ladder network whose transfer matrix is $A$.

#### 解答
(29) **a.**
$$\begin{bmatrix} 1 & 0 \\ -1/R_3 & 1 \end{bmatrix}\begin{bmatrix} 1 & -R_2 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_1 & 1 \end{bmatrix} = \begin{bmatrix} 1 + R_2/R_1 & -R_2 \\ -\dfrac{1}{R_1} - \dfrac{R_2}{R_1R_3} - \dfrac{1}{R_3} & 1 + \dfrac{R_2}{R_3} \end{bmatrix}$$

**b.** 比對得 $R_2 = 12$、$R_1 = 36$、$R_3 = 6$:
$$A = \begin{bmatrix} 1 & 0 \\ -1/6 & 1 \end{bmatrix}\begin{bmatrix} 1 & -12 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/36 & 1 \end{bmatrix}$$
即 shunt 36 ohms → series 12 ohms → shunt 6 ohms。

(30) 改用 series–shunt–series 的排法。設先 series $R_a$、再 shunt $R_b$、再 series $R_c$:
$$\begin{bmatrix} 1 & -R_c \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/R_b & 1 \end{bmatrix}\begin{bmatrix} 1 & -R_a \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 + R_c/R_b & -R_a - R_c(1 + R_a/R_b) \\ -1/R_b & 1 + R_a/R_b \end{bmatrix}$$
比對 $A$:$-1/R_b = -1/4 \Rightarrow R_b = 4$;$1 + R_a/4 = 3 \Rightarrow R_a = 8$;$1 + R_c/4 = 4/3 \Rightarrow R_c = 4/3$。檢查右上角:$-8 - \tfrac43(1 + 2) = -12$ ✓
$$A = \begin{bmatrix} 1 & -4/3 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ -1/4 & 1 \end{bmatrix}\begin{bmatrix} 1 & -8 \\ 0 & 1 \end{bmatrix}$$
即 series 8 ohms → shunt 4 ohms → series 4/3 ohm。

#### 備註
(29a) 需要課本 p. 163 的電路圖才知道順序(shunt → series → shunt)。本講義的圖畫的是課本 Figure 4 的兩段版本,三段的順序已在題幹文字裡說明。

(30) 示範了**同一個轉移矩陣可以有不同的分解 = 不同的電路實作**。這正是工程設計的本質:規格固定,實作方式有很多種。

### 挑戰 · Lay 2.5 Exercises 31–32(T 電腦題)
(31) The solution to the steady-state heat flow problem for the plate in the figure is approximated by the solution to the equation $A\mathbf{x} = \mathbf{b}$, where $\mathbf{b} = (5, 15, 0, 10, 0, 10, 20, 30)$ and

$$A = \begin{bmatrix} 4 & -1 & -1 & 0 & 0 & 0 & 0 & 0 \\ -1 & 4 & 0 & -1 & 0 & 0 & 0 & 0 \\ -1 & 0 & 4 & -1 & -1 & 0 & 0 & 0 \\ 0 & -1 & -1 & 4 & 0 & -1 & 0 & 0 \\ 0 & 0 & -1 & 0 & 4 & -1 & -1 & 0 \\ 0 & 0 & 0 & -1 & -1 & 4 & 0 & -1 \\ 0 & 0 & 0 & 0 & -1 & 0 & 4 & -1 \\ 0 & 0 & 0 & 0 & 0 & -1 & -1 & 4 \end{bmatrix}$$

- **a.** Use the method of Example 2 to construct an LU factorization of $A$, and note that both factors are band matrices (with two nonzero diagonals below or above the main diagonal). Compute $LU - A$ to check your work.
- **b.** Use the LU factorization to solve $A\mathbf{x} = \mathbf{b}$.
- **c.** Obtain $A^{-1}$ and note that $A^{-1}$ is a dense matrix with no band structure. When $A$ is large, $L$ and $U$ can be stored in much less space than $A^{-1}$.

(32) The band matrix $A$ shown below can be used to estimate the unsteady conduction of heat in a rod. Suppose that for $k = 0, 1, 2, \dots$, a vector $\mathbf{t}_k$ in $\mathbb{R}^5$ lists the temperatures at time $k\,\Delta t$. If the two ends of the rod are maintained at $0°$, then the temperature vectors satisfy the equation $A\mathbf{t}_{k+1} = \mathbf{t}_k$, where

$$A = \begin{bmatrix} (1+2C) & -C & & & \\ -C & (1+2C) & -C & & \\ & -C & (1+2C) & -C & \\ & & -C & (1+2C) & -C \\ & & & -C & (1+2C) \end{bmatrix}$$

- **a.** Find the LU factorization of $A$ when $C = 1$.
- **b.** Suppose $C = 1$ and $\mathbf{t}_0 = (10, 12, 12, 12, 10)$. Use the LU factorization of $A$ to find the temperature distributions $\mathbf{t}_1$, $\mathbf{t}_2$, $\mathbf{t}_3$, and $\mathbf{t}_4$.

#### 解答
(31) **a.** $L$、$U$ 都是**帶狀矩陣**(主對角線上下各兩條非零對角線),例如 $L$ 的次對角線是 $-.25, -.0667, -.2857, \dots$,$U$ 的對角線是 $4, 3.75, 3.7333, 3.4286, \dots$。$LU - A = O$。

**b.** 精確解
$$\mathbf{x} = \tfrac{1}{209}(827,\, 1377,\, 886,\, 1546,\, 1171,\, 1831,\, 1967,\, 2517) \approx (3.9569,\, 6.5885,\, 4.2392,\, 7.3971,\, 5.6029,\, 8.7608,\, 9.4115,\, 12.0431)$$

**c.** $A$ 只有 28 個非零元素,$A^{-1}$ 卻是 64 格**全部非零**的稠密矩陣(第 1 列約 $.2953, .0866, .0945, \dots$)。大型帶狀矩陣用 $L$、$U$ 儲存遠比用 $A^{-1}$ 省。

(32) **a.** $C = 1$ 時
$$L = \begin{bmatrix} 1 & & & & \\ -1/3 & 1 & & & \\ & -3/8 & 1 & & \\ & & -8/21 & 1 & \\ & & & -21/55 & 1 \end{bmatrix}, \quad U = \begin{bmatrix} 3 & -1 & & & \\ & 8/3 & -1 & & \\ & & 21/8 & -1 & \\ & & & 55/21 & -1 \\ & & & & 144/55 \end{bmatrix}$$
兩者都是 **bidiagonal**(只有主對角線與一條副對角線)。

**b.** 反覆解 $A\mathbf{t}_{k+1} = \mathbf{t}_k$:
$$\mathbf{t}_1 \approx (6.5556,\, 9.6667,\, 10.4444,\, 9.6667,\, 6.5556)$$
$$\mathbf{t}_2 \approx (4.7407,\, 7.6667,\, 8.5926,\, 7.6667,\, 4.7407)$$
$$\mathbf{t}_3 \approx (3.5988,\, 6.0556,\, 6.9012,\, 6.0556,\, 3.5988)$$
$$\mathbf{t}_4 \approx (2.7922,\, 4.7778,\, 5.4856,\, 4.7778,\, 2.7922)$$
溫度隨時間單調下降並保持左右對稱,符合兩端固定 $0°$ 的物理直覺。

#### 備註
兩題都標 T,放進實作課。

(31) 是「稀疏 vs 稠密」最有說服力的例子:**$A$ 稀疏,$L$、$U$ 也稀疏,但 $A^{-1}$ 稠密**。這正是 Numerical Note 第 4 點說的事,也是大型工程計算不用反矩陣的真正理由。

(32) 是「同一個 $A$、很多個 $\mathbf{b}$」的標準場景:LU 只做一次,前代回代做四次。順帶一提,$L$、$U$ 裡的分母 $3, 8, 21, 55, 144$ 是費氏數列的偶數項,可以當有趣的補充。

## 驗算
```check
(lambda b, c, m: b.shape == (5, 3) and c.shape == (3, 4) and b * c == m)(Matrix([[1,0,0],[3,1,0],[1,-1,1],[2,2,-1],[-3,-3,2]]), Matrix([[2,-4,-2,3],[0,3,1,-1],[0,0,0,5]]), Matrix([[2,-4,-2,3],[6,-9,-5,8],[2,-7,-3,9],[4,-2,-2,-1],[-6,3,3,4]]))
(lambda c, d: c * d == c[:, 0] * d[0, :] + c[:, 1] * d[1, :])(Matrix([[1, 2], [3, 4], [5, 6]]), Matrix([[1, 0, 2], [0, 1, 3]]))
400 * 100 == 40000 and 400 * 4 + 4 * 100 == 2000 and Rational(2000, 40000) == Rational(1, 20)
(lambda q, r, b: simplify(q.T * q - eye(2)) == zeros(2, 2) and (q * r).solve(b) == r.solve(q.T * b))(Matrix([[Rational(3,5), Rational(-4,5)], [Rational(4,5), Rational(3,5)]]), Matrix([[2, 1], [0, 5]]), Matrix([7, -3]))
(lambda u, d, v: (u * d * v.T).inv() == v * d.inv() * u.T)(Matrix([[Rational(3,5), Rational(-4,5)], [Rational(4,5), Rational(3,5)]]), diag(2, 5), Matrix([[0, -1], [1, 0]]))
(lambda p, d: (p * d * p.inv())**2 == p * d**2 * p.inv() and (p * d * p.inv())**7 == p * d**7 * p.inv())(Matrix([[1,0,1],[0,1,1],[1,1,0]]), diag(1, Rational(1,2), Rational(1,3)))
(lambda a, b, c: a * c == Matrix([9, 4]) and b * c == Matrix([9, 4]) and a != b)(Matrix([[1,0],[Rational(-2,9),1]]) * Matrix([[1, Rational(-1,2)],[0,1]]), Matrix([[1, Rational(-3,4)],[0,1]]) * Matrix([[1,0],[Rational(-1,6),1]]), Matrix([12, 6]))
simplify(Matrix([[1,0],[-1/c,1]]) * Matrix([[1,0],[-1/b,1]]) * Matrix([[1,0],[-1/a,1]]) - Matrix([[1,0],[-(1/a + 1/b + 1/c),1]])) == zeros(2, 2)
Matrix([[1,0],[Rational(-1,6),1]]) * Matrix([[1,-12],[0,1]]) * Matrix([[1,0],[Rational(-1,36),1]]) == Matrix([[Rational(4,3),-12],[Rational(-1,4),3]])
Matrix([[1,Rational(-4,3)],[0,1]]) * Matrix([[1,0],[Rational(-1,4),1]]) * Matrix([[1,-8],[0,1]]) == Matrix([[Rational(4,3),-12],[Rational(-1,4),3]])
Matrix([[4,-1,-1,0,0,0,0,0],[-1,4,0,-1,0,0,0,0],[-1,0,4,-1,-1,0,0,0],[0,-1,-1,4,0,-1,0,0],[0,0,-1,0,4,-1,-1,0],[0,0,0,-1,-1,4,0,-1],[0,0,0,0,-1,0,4,-1],[0,0,0,0,0,-1,-1,4]]).solve(Matrix([5,15,0,10,0,10,20,30])) == Matrix([827,1377,886,1546,1171,1831,1967,2517]) / 209
(lambda l, u, m: l.is_lower and u.is_upper and l * u == m)(Matrix([[1,0,0,0,0],[Rational(-1,3),1,0,0,0],[0,Rational(-3,8),1,0,0],[0,0,Rational(-8,21),1,0],[0,0,0,Rational(-21,55),1]]), Matrix([[3,-1,0,0,0],[0,Rational(8,3),-1,0,0],[0,0,Rational(21,8),-1,0],[0,0,0,Rational(55,21),-1],[0,0,0,0,Rational(144,55)]]), Matrix([[3,-1,0,0,0],[-1,3,-1,0,0],[0,-1,3,-1,0],[0,0,-1,3,-1],[0,0,0,-1,3]]))
(lambda a, t: a.solve(t) == Matrix([59,87,94,87,59]) / 9)(Matrix([[3,-1,0,0,0],[-1,3,-1,0,0],[0,-1,3,-1,0],[0,0,-1,3,-1],[0,0,0,-1,3]]), Matrix([10,12,12,12,10]))
(lambda a, t: a.solve(a.solve(a.solve(a.solve(t)))) == Matrix([1357,2322,2666,2322,1357]) / 486)(Matrix([[3,-1,0,0,0],[-1,3,-1,0,0],[0,-1,3,-1,0],[0,0,-1,3,-1],[0,0,0,-1,3]]), Matrix([10,12,12,12,10]))
```
