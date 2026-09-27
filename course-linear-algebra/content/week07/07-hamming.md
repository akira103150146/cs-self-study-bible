---
title_en: Hamming Codes as Null Spaces
title_zh: 漢明碼:零空間就是碼本
sub: A 4-dimensional null space that corrects one bit error
level: mid
supplement: true
lab_hook: '在 GF(2) 上算 Nul H:整個碼本就是一個零空間的基底組合'
---
## 觀念
補充內容(課本沒有,但這是「零空間」在資工最漂亮的應用:錯誤更正碼)。

先換一套算術。在 $\mathrm{GF}(2)$(只有 0 與 1 的體)裡,加法就是 **XOR**:

$$0 + 0 = 0, \quad 0 + 1 = 1, \quad 1 + 0 = 1, \quad \mathbf{1 + 1 = 0}$$

乘法照常($1 \cdot 1 = 1$,其餘為 0)。**本週學過的所有定理在 $\mathrm{GF}(2)$ 上一字不改地成立**——子空間、基底、rank、Rank Theorem 全都可以用,只是所有數字都 mod 2。

**Hamming(7, 4) code.** 取 **parity-check matrix**

$$H = \begin{bmatrix} 1 & 1 & 1 & 0 & 1 & 0 & 0 \\ 1 & 1 & 0 & 1 & 0 & 1 & 0 \\ 1 & 0 & 1 & 1 & 0 & 0 & 1 \end{bmatrix}$$

**碼本(所有合法字)就定義成 $H$ 的零空間**:

$$\mathcal{C} = \operatorname{Nul} H = \{\mathbf{x} \in \mathrm{GF}(2)^7 : H\mathbf{x} = \mathbf{0}\}$$

由 Rank Theorem,$\operatorname{rank} H = 3$、$H$ 有 7 行,所以

$$\dim \mathcal{C} = 7 - 3 = 4 \quad \Longrightarrow \quad \text{共有 } 2^4 = 16 \text{ 個合法字}$$

也就是:**用 7 個位元傳 4 個位元的資料**,多出來的 3 個位元換到「能更正任何一個位元的錯誤」。

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| GF(2) | 二元體 | 只有 0、1;加法是 XOR($1+1=0$) |
| parity bit | 校驗位元 | 湊出「1 的個數是偶數」的那個位元 |
| codeword | 碼字 | 合法的 7 位元字,即 $\operatorname{Nul} H$ 的元素 |
| parity-check matrix | 校驗矩陣 | $H$;$H\mathbf{x} = \mathbf{0}$ 就是合法 |
| generator matrix | 生成矩陣 | $G$;$\mathbf{x} = G\mathbf{d}$ 把 4 位元資料變成 7 位元碼字 |
| syndrome | 症狀向量 | $\mathbf{s} = H\mathbf{y}$;等於 $\mathbf{0}$ 表示沒抓到錯 |
| Hamming distance | 漢明距離 | 兩個字有幾個位元不同 |
| single error correcting | 單錯更正 | 任何一個位元翻掉都能找回來 |

## 白話說
![三個互相重疊的圈,每一圈裡有四個位元,1 的個數必須是偶數](hamming.svg)

**規則只有一句:每個圈裡的 4 個位元,1 的個數必須是偶數。**

- $d_1, d_2, d_3, d_4$ 是**資料**位元,愛填什麼就填什麼($2^4 = 16$ 種)。
- $p_1, p_2, p_3$ 是**校驗**位元,由「湊成偶數」這條規則**被迫決定**,沒有自由。

三個圈給出三條方程式(在 $\mathrm{GF}(2)$ 上):

$$p_1 = d_1 + d_2 + d_3, \qquad p_2 = d_1 + d_2 + d_4, \qquad p_3 = d_1 + d_3 + d_4$$

把它們搬到同一邊($\mathrm{GF}(2)$ 裡 $-1 = +1$,所以移項就是照抄),就得到 $H\mathbf{x} = \mathbf{0}$,其中 $\mathbf{x} = (d_1, d_2, d_3, d_4, p_1, p_2, p_3)$。

**這就是為什麼「碼本 = 零空間」**:合法字的條件本來就是一組齊次方程式。

**解錯誤的方法簡單到像魔術**:收到 7 個位元 $\mathbf{y}$,算 $\mathbf{s} = H\mathbf{y}$(三個圈各檢查一次)。

| syndrome $\mathbf{s}$ | 意思 |
|---|---|
| $\mathbf{0}$ | 三個圈都是偶數,沒抓到錯 |
| 非零 | $\mathbf{s}$ **就是** $H$ 的第 $j$ 行,那個 $j$ 就是出錯的位置 |

翻回那一位就修好了。**不必比對 16 個碼字,算一個 $3 \times 7$ 乘法就知道錯在哪。**

## 在資工哪裡用
- **ECC 記憶體**:伺服器的 DRAM 用的是 Hamming 的加強版(如 SEC-DED:$72$ 位元存 $64$ 位元資料),原理與這裡一模一樣,只是矩陣大一點。
- **快閃記憶體與硬碟**:SSD 的控制器每讀一個頁面都在算 syndrome;RAID 5 的 parity 磁碟就是「一個圈」的版本。
- **QR code、CD、深空通訊**:用的是更強的 Reed–Solomon(在 $\mathrm{GF}(256)$ 上),但「碼本 = 某個矩陣的零空間」這個結構完全相同。
- **網路封包的 CRC**:同樣是 $\mathrm{GF}(2)$ 上的線性代數(多項式版本),只做偵錯不做更正。
- **為什麼這一節值得放進線代課**:它讓「零空間」從抽象變成**一個每天在你電腦裡跑幾百萬次的東西**。

## 原理
**為什麼 $\dim \mathcal{C} = 4$?**

$H$ 的後三行就是 $\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3$,顯然有 3 個樞軸,所以 $\operatorname{rank} H = 3$。$H$ 有 7 行,由 **Rank Theorem**

$$\dim \operatorname{Nul} H = 7 - \operatorname{rank} H = 7 - 3 = 4$$

$\mathrm{GF}(2)$ 上每個座標只有 2 種選擇,所以 4 維空間有 $2^4 = 16$ 個元素。**這就是「4 個資料位元」的來源**——不是規定的,是算出來的。

**兩種描述碼本的方式,其實是同一個子空間。** 令

$$G = \begin{bmatrix} I_4 \\ P \end{bmatrix} \quad \text{其中} \quad P = \begin{bmatrix} 1 & 1 & 1 & 0 \\ 1 & 1 & 0 & 1 \\ 1 & 0 & 1 & 1 \end{bmatrix}$$

則編碼就是 $\mathbf{x} = G\mathbf{d}$,碼本是 $\operatorname{Col} G$。而 $H = [\,P \;\; I_3\,]$,所以

$$HG = P \cdot I_4 + I_3 \cdot P = P + P = \mathbf{0} \quad (\text{在 } \mathrm{GF}(2) \text{ 上 } 1 + 1 = 0)$$

於是 $\operatorname{Col} G \subseteq \operatorname{Nul} H$。又 $G$ 的上半是 $I_4$ ⇒ $\operatorname{rank} G = 4$ ⇒ $\dim \operatorname{Col} G = 4 = \dim \operatorname{Nul} H$。**一個 4 維子空間包含在另一個 4 維子空間裡,兩者必相等**(這正是基底定理的推論)。所以

$$\mathcal{C} = \operatorname{Col} G = \operatorname{Nul} H$$

**「生成矩陣的行空間」與「校驗矩陣的零空間」是同一個碼本**,一個用來編碼、一個用來檢查。

**為什麼一個錯誤一定抓得到、而且抓得準?**

設傳出合法字 $\mathbf{x}$,第 $j$ 位被翻掉,收到 $\mathbf{y} = \mathbf{x} + \mathbf{e}_j$。則

$$\mathbf{s} = H\mathbf{y} = H\mathbf{x} + H\mathbf{e}_j = \mathbf{0} + (H \text{ 的第 } j \text{ 行})$$

而 $H$ 的 7 行恰好是**全部 7 個非零的三位元向量**,兩兩不同:

$$(1,1,1), (1,1,0), (1,0,1), (0,1,1), (1,0,0), (0,1,0), (0,0,1)$$

所以 syndrome 非零(抓到錯)、而且**唯一決定** $j$(抓得準)。$\blacksquare$

**代價是什麼?** 兩個位元同時出錯時,$\mathbf{s} = H\mathbf{e}_i + H\mathbf{e}_j$ 又會等於某個**第三行**,程式會「更正」到錯誤的位置,反而多錯一位。Hamming(7,4) 的最小距離是 3:**能更正 1 個錯、或偵測 2 個錯,但不能同時做到**。

## 老師講解
### 例 1 · 補充:編碼
Encode the data bits $\mathbf{d} = (1, 0, 1, 1)$.

1. **算三個校驗位元**(在 $\mathrm{GF}(2)$ 上,也就是「數 1 的個數看奇偶」):
   - $p_1 = d_1 + d_2 + d_3 = 1 + 0 + 1 = 0$
   - $p_2 = d_1 + d_2 + d_4 = 1 + 0 + 1 = 0$
   - $p_3 = d_1 + d_3 + d_4 = 1 + 1 + 1 = 1$
2. **拼出碼字**:$\mathbf{x} = (1, 0, 1, 1, \; 0, 0, 1)$。
3. **用圖檢查**:上圈 $\{p_1, d_1, d_2, d_3\} = \{0, 1, 0, 1\}$ 有兩個 1 ✓;左圈 $\{p_2, d_1, d_2, d_4\} = \{0, 1, 0, 1\}$ ✓;右圈 $\{p_3, d_1, d_3, d_4\} = \{1, 1, 1, 1\}$ 有四個 1 ✓。**三圈都是偶數。**
4. **用矩陣檢查**:$H\mathbf{x} = \mathbf{0}$(mod 2)。每一列就是一個圈。
5. **另一種算法**:$\mathbf{x} = G\mathbf{d}$。$G$ 的第 1、3、4 行相加(mod 2)就是答案——**編碼只是「挑幾個基底向量加起來」**,而那些基底向量正是 $\operatorname{Nul} H$ 的基底。
6. **這一步值得停下來想**:碼本有 16 個字,但我們從來不需要把它們列出來。**只要記住 4 個基底向量**,任何碼字都是它們的線性組合。

### 例 2 · 補充:解碼(單一錯誤)
You receive $\mathbf{y} = (1, 0, 0, 1, 0, 0, 1)$. Decode it.

1. **算 syndrome**,一列一列來:
   - 第 1 列(上圈):$y_1 + y_2 + y_3 + y_5 = 1 + 0 + 0 + 0 = 1$
   - 第 2 列(左圈):$y_1 + y_2 + y_4 + y_6 = 1 + 0 + 1 + 0 = 0$
   - 第 3 列(右圈):$y_1 + y_3 + y_4 + y_7 = 1 + 0 + 1 + 1 = 1$
2. **$\mathbf{s} = (1, 0, 1) \ne \mathbf{0}$** ⇒ 有錯。
3. **對照 $H$ 的各行**:$(1,0,1)$ 是 $H$ 的**第 3 行** ⇒ **錯在第 3 位**。
4. **翻回來**:$y_3: 0 \to 1$,得 $\mathbf{x} = (1, 0, 1, 1, 0, 0, 1)$——正是例 1 的碼字。
5. **驗算**:再算一次 syndrome,應得 $\mathbf{0}$ ✓
6. **拿掉校驗位元**,資料是 $(1, 0, 1, 1)$。
7. **為什麼不用「跟 16 個碼字比對」?** 因為那要比 16 次;syndrome 只要算一次乘法。**碼越長,差距越懸殊**:Hamming(255, 247) 的碼本有 $2^{247}$ 個字,比對是天文數字,syndrome 仍然只是一次乘法。

### 例 3 · 補充:兩個錯誤會怎樣
Suppose bits 2 and 3 of the codeword in Example 1 are both flipped. What does the decoder do?

1. **收到**:$\mathbf{y} = (1, 1, 0, 1, 0, 0, 1)$(原本 $d_2 = 0 \to 1$、$d_3 = 1 \to 0$)。
2. **syndrome**:$\mathbf{s} = H\mathbf{e}_2 + H\mathbf{e}_3 = (1,1,0) + (1,0,1) = (0,1,1)$。
3. **$(0,1,1)$ 是 $H$ 的第 4 行** ⇒ 解碼器會判定「第 4 位錯」,把 $y_4$ 翻掉。
4. **結果錯了三位**:原本 2 位錯,現在變成 3 位錯。**解碼器不但沒救回來,還加了一刀。**
5. **這不是 bug,是設計的極限**。最小距離 3 只夠「更正 1 個」或「偵測 2 個」,不能兩者兼得。
6. **實務怎麼辦?** 加第 8 個位元 $p_4 = $ 全部 7 位元的總和(偶同位)。這樣兩個錯會讓 $p_4$ 的檢查通過、但 syndrome 非零,形成「矛盾」⇒ 知道是 2 個錯、放棄更正(SEC-DED)。這就是 ECC 記憶體的做法,也是挑戰題。

#### 備註
例 3 是本節最重要的一個例子:**它告訴學生「更正」不是萬能的**。很多人以為加了 ECC 就不會錯,實際上只是把錯誤率壓低。

若時間不夠,例 3 可以只講第 4 點的結論,把計算留給挑戰題。

## 易錯點
- **忘了在 $\mathrm{GF}(2)$ 上算**:$1 + 1 = 0$,不是 2。所有運算做完都要 mod 2。
- **把 syndrome 當成「錯了幾位」**。syndrome 是**位置**的編碼,不是個數。
- **校驗位元也會錯**。學生常以為只有資料位元會出錯;syndrome 指到第 5、6、7 位就是校驗位元錯了,照樣翻回來。
- **位元順序記錯**。本講義用 $(d_1, d_2, d_3, d_4, p_1, p_2, p_3)$;換順序 $H$ 的行也要跟著換。
- **以為 $\operatorname{rank} H = 3$ 是巧合**。它是設計出來的:3 個校驗位元 ⇒ 3 列 ⇒ 最多 $2^3 - 1 = 7$ 個非零 syndrome ⇒ 最多保護 7 個位元。
- **兩個錯誤時相信解碼器**(例 3)。

## 教學提示
**這是補充觀念,180 分鐘的節奏表裡沒有排它**(收尾時只給結論)。若某個班級對「這學到底有什麼用」特別無感,從觀念 4 或觀念 6 借 10 分鐘講例 1 與例 2,投資報酬率很高——它讓「零空間」落地。學生對 $\operatorname{Nul} A$ 通常沒有感覺,看到「它就是 ECC 記憶體的碼本」之後感覺完全不同。

**建議的上法**:先只畫三個圈、不寫矩陣,讓學生自己填 $p_1, p_2, p_3$(3 分鐘,人人做得出來)。等他們填完再說:「你們剛剛解的是 $H\mathbf{x} = \mathbf{0}$。」**先動手,再揭曉。**

然後當場示範解碼:老師寫一個碼字、偷偷翻掉一位、請學生算 syndrome 找出錯在哪。**這個互動幾乎不會失敗,效果很好。**

若借到 10 分鐘:只做例 1(編碼)與例 2(解碼);照做 (1)(2)、是非題與變化題一律當作業。應用題的「代價」計算($4/7$ 的碼率)值得口頭問一次:「為了修 1 個位元的錯,你願意多傳 75% 的資料量嗎?」

**與本週其他觀念的連結要講明**:$\dim \mathcal{C} = 7 - \operatorname{rank} H$ 是 Rank Theorem;$\operatorname{Col} G = \operatorname{Nul} H$ 用的是基底定理(同維度 + 包含 ⇒ 相等)。**這一節不是餘興節目,而是本週三個定理的合體練習。**

Lab 會用程式把 16 個碼字全列出來、逐一驗證,並隨機翻位元測試解碼器。

## 練習
### 照做 · 補充
All arithmetic is in $\mathrm{GF}(2)$, where $1 + 1 = 0$. Use $H = \begin{bmatrix} 1 & 1 & 1 & 0 & 1 & 0 & 0 \\ 1 & 1 & 0 & 1 & 0 & 1 & 0 \\ 1 & 0 & 1 & 1 & 0 & 0 & 1 \end{bmatrix}$ and $\mathbf{x} = (d_1, d_2, d_3, d_4, p_1, p_2, p_3)$.

(1) Encode the data bits $\mathbf{d} = (1, 1, 0, 1)$.

(2) Encode the data bits $\mathbf{d} = (0, 1, 1, 0)$.

(3) Is $\mathbf{y} = (1, 1, 1, 1, 1, 1, 1)$ a codeword? Compute $H\mathbf{y}$.

(4) A single bit of a codeword is flipped in position 6. What is the syndrome?

#### 解答
- (1) $p_1 = 1 + 1 + 0 = 0$、$p_2 = 1 + 1 + 1 = 1$、$p_3 = 1 + 0 + 1 = 0$ ⇒ $\mathbf{x} = (1, 1, 0, 1, 0, 1, 0)$。
- (2) $p_1 = 0 + 1 + 1 = 0$、$p_2 = 0 + 1 + 0 = 1$、$p_3 = 0 + 1 + 0 = 1$ ⇒ $\mathbf{x} = (0, 1, 1, 0, 0, 1, 1)$。
- (3) **是。** 每一列都有 4 個 1(上圈 $1+1+1+1$、左圈 $1+1+1+1$、右圈 $1+1+1+1$),全部是偶數,所以 $H\mathbf{y} = \mathbf{0}$。全 1 的字確實是合法碼字(它是 $\mathbf{d} = (1,1,1,1)$ 的編碼)。
- (4) syndrome $= H\mathbf{e}_6 = H$ 的第 6 行 $= (0, 1, 0)$。

#### 備註
(1)(2) 只是把三條方程式代進去,是人人做得到的暖身題;重點是讓學生習慣 $1+1=0$。

(3) 的全 1 字是個好例子:**它同時滿足三個圈**,而且是 $\mathbf{d} = (1,1,1,1)$ 的編碼,可以順便驗證 $G$ 的四行相加(mod 2)確實得到全 1。

(4) 要學生看出「syndrome 就是 $H$ 的那一行」,不必真的算乘法。

### 是非 · 補充
Mark each statement True or False. Justify each answer. All arithmetic is in $\mathrm{GF}(2)$.

(1) **(T/F)** The set of codewords $\mathcal{C} = \operatorname{Nul} H$ is a subspace of $\mathrm{GF}(2)^7$.

(2) **(T/F)** The sum of two codewords is again a codeword.

(3) **(T/F)** If the syndrome of a received word is $\mathbf{0}$, then no bits were flipped.

(4) **(T/F)** $\operatorname{rank} H + \dim \operatorname{Nul} H = 7$.

#### 解答
- (1) **True.** 它是一個齊次方程式的解集,由 Theorem 12(上上個觀念)它是子空間;維度 4。
- (2) **True.** 這正是 (1) 的「加法封閉」:$H\mathbf{x} = \mathbf{0}$ 且 $H\mathbf{z} = \mathbf{0}$ ⇒ $H(\mathbf{x} + \mathbf{z}) = \mathbf{0}$。**碼是線性的,這就是「線性碼」的意思。**
- (3) **False.** syndrome 為 $\mathbf{0}$ 只表示「收到的字是合法碼字」。若剛好翻了 3 個位元而變成**另一個**碼字,syndrome 仍然是 $\mathbf{0}$。(最小距離 3,所以 3 個錯就可能發生這種事。)
- (4) **True.** 這就是 Rank Theorem,$H$ 有 7 行;$3 + 4 = 7$。

#### 備註
(3) 是本組唯一的 False,也是最重要的一題:**「沒抓到錯」不等於「沒有錯」**。學生答錯時,請他們自己找一個距離 3 的例子:全 0 碼字翻掉**第 1、4、5 位**會得到另一個合法碼字 $(1,0,0,1,1,0,0)$,syndrome 仍然是 $\mathbf{0}$。(權重 3 的碼字共 7 個,位置分別是 {1,2,7}、{1,3,6}、{1,4,5}、{2,3,4}、{2,5,6}、{3,5,7}、{4,6,7};隨便挑一個都行。)

(1)(2) 合起來說明「線性碼」為什麼叫線性——這也是為什麼線代能處理編碼理論。

(4) 是本週定理在 $\mathrm{GF}(2)$ 上的直接套用,值得強調:**Rank Theorem 不限於實數。**

### 變化 · 補充
All arithmetic is in $\mathrm{GF}(2)$.

(1) You receive $\mathbf{y} = (0, 1, 1, 0, 0, 1, 0)$. Find the syndrome, locate the error, and give the four data bits.

(2) You receive $\mathbf{y} = (1, 0, 1, 1, 1, 0, 1)$. Find the syndrome, locate the error, and give the four data bits.

(3) Find a basis for $\mathcal{C} = \operatorname{Nul} H$ and state $\dim \mathcal{C}$. How many codewords are there?

#### 解答
(1) $\mathbf{s} = (0 + 1 + 1 + 0, \; 0 + 1 + 0 + 1, \; 0 + 1 + 0 + 0) = (0, 0, 1)$ ⇒ 是 $H$ 的第 **7** 行 ⇒ 第 7 位錯。翻回得 $\mathbf{x} = (0, 1, 1, 0, 0, 1, 1)$,資料為 $(0, 1, 1, 0)$。(這正是照做 (2) 的碼字。)

(2) $\mathbf{s} = (1 + 0 + 1 + 1, \; 1 + 0 + 1 + 0, \; 1 + 1 + 1 + 1) = (1, 0, 0)$ ⇒ 是 $H$ 的第 **5** 行 ⇒ 第 5 位(校驗位元 $p_1$)錯。翻回得 $\mathbf{x} = (1, 0, 1, 1, 0, 0, 1)$,資料為 $(1, 0, 1, 1)$。

(3) 取 $\mathbf{d} = \mathbf{e}_1, \dots, \mathbf{e}_4$ 編碼,得到 $G$ 的四行:
$$\left\{(1,0,0,0,1,1,1), \; (0,1,0,0,1,1,0), \; (0,0,1,0,1,0,1), \; (0,0,0,1,0,1,1)\right\}$$
它們線性獨立(前 4 個座標構成 $I_4$)且都在 $\operatorname{Nul} H$ 裡,個數 4 $= \dim \operatorname{Nul} H$ ⇒ 由**基底定理**它們是基底。$\dim \mathcal{C} = 4$,碼字共 $2^4 = 16$ 個。

#### 備註
(2) 刻意讓**校驗位元**出錯,打掉「只有資料會錯」的直覺。

(3) 是本節與本週理論接最緊的一題:**用基底定理省掉「驗張成」那一步**。若學生硬要解 $H\mathbf{x} = \mathbf{0}$ 的參數向量形式也完全可以,答案會是同一個子空間的另一組基底。

三題都可以用 Lab 的程式複驗。

### 應用 · 補充
(1) The code sends 4 data bits in 7 transmitted bits. What is the overhead, as a percentage of the data size? What would the overhead be for a Hamming code with 4 parity bits, which protects 15 bits in total?

(2) Two bits of a codeword are flipped. Explain, using $H$, why the decoder can make the result worse. Give an explicit example.

#### 解答
(1) 7 位元傳 4 位元資料,**多傳了 3 位元 = 資料的 75%**(碼率 $4/7 \approx 0.571$)。4 個校驗位元的版本是 Hamming(15, 11):15 位元傳 11 位元,**多傳 4/11 ≈ 36%**(碼率 $11/15 \approx 0.733$)。**碼越長,校驗的相對成本越低**——$k$ 個校驗位元可以保護 $2^k - 1$ 個位元。這就是 ECC 記憶體用 Hamming(72, 64)(overhead 12.5%)而不是 Hamming(7,4) 的原因。

(2) 若第 $i$、$j$ 位同時翻掉,$\mathbf{s} = H\mathbf{e}_i + H\mathbf{e}_j$。因為 $H$ 的 7 行是全部 7 個非零三位元向量,**兩行相加仍然是某一行**(例如 $(1,1,0) + (1,0,1) = (0,1,1)$),所以 syndrome 非零、而且看起來像「第三個位置出錯」。解碼器會去翻那個位置,結果從 2 個錯變成 3 個錯。

例:碼字 $(1,0,1,1,0,0,1)$ 的第 2、3 位翻掉 ⇒ $\mathbf{y} = (1,1,0,1,0,0,1)$,$\mathbf{s} = (0,1,1) = H$ 的第 4 行 ⇒ 解碼器翻掉第 4 位,得 $(1,1,0,0,0,0,1)$,與原碼字差 **3** 個位元。

#### 備註
(1) 的計算很簡單但結論很重要:**錯誤更正不是免費的**,而且成本隨碼長下降。順便可以提 $k$ 個校驗位元保護 $2^k - 1$ 位元的上限來自「非零 syndrome 只有 $2^k - 1$ 種」。

(2) 建議要求學生**自己找一組例子**,不要只抄答案;隨便挑兩個位置都會發生同樣的事。

### 挑戰 · 補充
(1) Add an eighth bit $p_4$ equal to the sum of all seven bits, giving the $8$-bit extended code with parity-check matrix $H' = \begin{bmatrix} H & \mathbf{0} \\ \mathbf{1}^T & 1 \end{bmatrix}$, where $\mathbf{1}^T = (1, 1, 1, 1, 1, 1, 1)$. Find $\operatorname{rank} H'$ and $\dim \operatorname{Nul} H'$. Explain how the decoder can now tell a single error from a double error.

(2) Let $G = \begin{bmatrix} I_4 \\ P \end{bmatrix}$ with $P$ equal to the first four columns of $H$. Show that $\operatorname{Col} G = \operatorname{Nul} H$ without listing any codewords.

#### 解答
(1) $H'$ 是 $4 \times 8$。它的後面幾行含 $H$ 的 $I_3$ 部分再加上最後一行的 1,列化簡可得 4 個樞軸,故 $\operatorname{rank} H' = 4$;由 Rank Theorem $\dim \operatorname{Nul} H' = 8 - 4 = 4$。**資料位元仍然是 4 個**,但總長變 8。

判斷方式看兩件事:前三列的 syndrome $\mathbf{s}$ 與最後一列的整體同位 $t$。

- $\mathbf{s} = \mathbf{0}$、$t = 0$:沒抓到錯。
- $\mathbf{s} = \mathbf{0}$、$t = 1$:**第 8 位($p_4$)自己錯**($H'$ 的第 8 行是 $(0,0,0,1)$,不影響前三個圈)⇒ 翻回第 8 位,仍是單錯。
- $\mathbf{s} \ne \mathbf{0}$、$t = 1$:**單一錯誤**(翻一位會同時破壞某些圈與整體同位)⇒ 依 $\mathbf{s}$ 更正。
- $\mathbf{s} \ne \mathbf{0}$、$t = 0$:**偵測到兩個錯誤**(翻兩位使整體同位復原,但圈的檢查仍失敗)⇒ 不更正,回報無法修復。

這就是 **SEC-DED**(single error correcting, double error detecting),伺服器 ECC 記憶體用的正是這個結構。

(2) 兩步:

1. **包含**:$H = [\,P \;\; I_3\,]$,所以 $HG = P \cdot I_4 + I_3 \cdot P = P + P = \mathbf{0}$(在 $\mathrm{GF}(2)$ 上)。因此 $G$ 的每一行都在 $\operatorname{Nul} H$ 裡,而 $\operatorname{Col} G$ 是這些行的所有線性組合、$\operatorname{Nul} H$ 是子空間(對加法與係數封閉),故 $\operatorname{Col} G \subseteq \operatorname{Nul} H$。
2. **維度相同**:$G$ 的上半是 $I_4$ ⇒ 4 行線性獨立 ⇒ $\dim \operatorname{Col} G = 4$;而 $\dim \operatorname{Nul} H = 7 - 3 = 4$。

一個 4 維子空間包含在一個 4 維子空間裡,兩者必相等(否則取 $\operatorname{Col} G$ 的基底,它是 $\operatorname{Nul} H$ 裡 4 個線性獨立的向量,由**基底定理**它已經是 $\operatorname{Nul} H$ 的基底,故張成整個 $\operatorname{Nul} H$)。所以 $\operatorname{Col} G = \operatorname{Nul} H$。$\blacksquare$

#### 備註
(2) 是本週最漂亮的一題:**Rank Theorem 與基底定理各出一次力,就證明了「編碼」與「檢查」描述同一個碼本**。強烈建議在課堂上講這一題,即使跳過 (1)。

「包含 + 同維度 ⇒ 相等」是之後(特徵空間、正交補)會反覆用到的套路,值得單獨強調一次。

(1) 的細節較繁,適合給程度好的學生;若當作業,可只要求前半(算 rank 與維度)。

## 驗算
```check
(lambda h, x: (h * x).applyfunc(lambda v: v % 2).is_zero_matrix)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([1, 0, 1, 1, 0, 0, 1]))
(lambda h, x: (h * x).applyfunc(lambda v: v % 2).is_zero_matrix)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([1, 1, 0, 1, 0, 1, 0]))
(lambda h, x: (h * x).applyfunc(lambda v: v % 2).is_zero_matrix)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([0, 1, 1, 0, 0, 1, 1]))
(lambda h, x: (h * x).applyfunc(lambda v: v % 2).is_zero_matrix)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([1, 1, 1, 1, 1, 1, 1]))
(lambda h, y: (h * y).applyfunc(lambda v: v % 2) == Matrix([1, 0, 1]))(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([1, 0, 0, 1, 0, 0, 1]))
(lambda h, y: (h * y).applyfunc(lambda v: v % 2) == Matrix([0, 0, 1]))(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([0, 1, 1, 0, 0, 1, 0]))
(lambda h, y: (h * y).applyfunc(lambda v: v % 2) == Matrix([1, 0, 0]))(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([1, 0, 1, 1, 1, 0, 1]))
(lambda h, y: (h * y).applyfunc(lambda v: v % 2) == Matrix([0, 1, 1]))(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([1, 1, 0, 1, 0, 0, 1]))
(lambda h: len({tuple((h * Matrix([int(b) for b in format(i, '07b')])).applyfunc(lambda v: v % 2)) for i in range(128)}) == 8 and sum(1 for i in range(128) if (h * Matrix([int(b) for b in format(i, '07b')])).applyfunc(lambda v: v % 2).is_zero_matrix) == 16)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]))
(lambda h: h.rank() == 3 and h.cols - h.rank() == 4 and 2 ** 4 == 16)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]))
(lambda h: len({tuple(h.col(j)) for j in range(7)}) == 7 and all(not h.col(j).is_zero_matrix for j in range(7)))(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]))
(lambda h, g: (h * g).applyfunc(lambda v: v % 2).is_zero_matrix and g.rank() == 4)(Matrix([[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]]), Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1]]))
(lambda h: h.rank() == 4 and h.cols - h.rank() == 4)(Matrix([[1, 1, 1, 0, 1, 0, 0, 0], [1, 1, 0, 1, 0, 1, 0, 0], [1, 0, 1, 1, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1]]))
Matrix([1, 1, 0]) + Matrix([1, 0, 1]) == Matrix([2, 1, 1]) and (Matrix([1, 1, 0]) + Matrix([1, 0, 1])).applyfunc(lambda v: v % 2) == Matrix([0, 1, 1])
```
