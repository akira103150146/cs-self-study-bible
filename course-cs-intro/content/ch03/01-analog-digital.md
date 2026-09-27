---
id: C3.1
title_en: Analog and Digital Data
title_zh: 類比與數位資料
sub: Continuous vs. discrete — and how many bits a set of things needs
level: basic
lab_hook: "任務 1:`bits_for_items()`、`digitize()`"
---
## 觀念
**Analog data** is a continuous representation, analogous to the actual information it represents (a mercury thermometer, a vinyl groove, a voltage that varies smoothly). **Digital data** is a discrete representation: the information is broken into separate elements.

Computers store data digitally because digital signals can be **regenerated**. An electronic signal degrades as it travels (**signal degradation**) and picks up noise. With only two meaningful levels — high voltage for 1 and low voltage for 0 — a receiver can decide which level was meant and send out a fresh, clean pulse (**pulse-code modulation**). An analog signal cannot be restored this way, because every value between is meaningful.

**Binary representations.** $n$ bits give $2^n$ distinct patterns. To give a unique pattern to each of $k$ items we need

$$\lceil \log_2 k \rceil \ \text{bits}.$$

Digitizing an analog value means choosing one of $2^n$ levels: a range $[0, V_{\max}]$ split into $2^n$ levels has a step of $V_{\max} / (2^n - 1)$.

![An analog signal varies continuously; a digital signal has only two meaningful levels.](analog-digital.svg)

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| analog data | 類比資料 | 連續變化、和真實量成比例的表示 |
| digital data | 數位資料 | 離散的表示,只取有限個值 |
| digitize | 數位化 | 把連續的量換成有限個離散值 |
| signal degradation | 訊號衰減 | 訊號傳遞時失真、變弱 |
| regenerate | 再生 | 依門檻判斷 0/1 後,重新送出乾淨的訊號 |
| pulse-code modulation (PCM) | 脈碼調變 | 用離散的脈波表示資料 |

## 白話說
類比就像用尺量:任何長度都可能出現。數位就像數顆數:只有 0、1、2……這些值。數位的好處是**抗雜訊**:訊號被干擾一點點,0 還是看得出是 0,只要重新整形就恢復原狀;類比訊號被干擾了,你永遠不知道原本是多少。

至於「要幾個位元」,就是問 2 的幾次方才夠:表示 5 種東西,2 位元只有 4 種不夠,3 位元有 8 種才夠。

## 後面會用到
- **數位邏輯**:高低電位與門檻、雜訊邊界(noise margin)。
- **計算機網路**:訊號在線路上衰減、中繼器(repeater)負責再生(第 15 章)。
- **多媒體**:C3.7 的聲音取樣就是把類比聲波數位化。

## 原理
**為什麼需要 $\lceil \log_2 k \rceil$ 位?** $n$ 位只有 $2^n$ 種樣子,要給 $k$ 樣東西各一個不同的樣子,需要 $2^n \ge k$,也就是 $n \ge \log_2 k$;位元數是整數,所以取上界。

**為什麼數位訊號可以無限次傳遞而不失真?** 每經過一次再生,接收端只問「電壓高於門檻嗎?」只要雜訊沒有大到把訊號推過門檻,判斷就正確,再送出一個全新的標準脈波。誤差不會累積。類比訊號每次放大也會把雜訊一起放大,誤差一路累積。

## 老師講解
### 例 1
How many bits are needed to represent (a) the 7 days of the week, (b) 52 playing cards, (c) 1000 different sensor readings?

1. 找最小的 $n$ 使 $2^n \ge k$。
2. (a) $k = 7$:$2^2 = 4$ 不夠,$2^3 = 8$ 夠 → **3 位元**(會有 1 個樣子用不到)。
3. (b) $k = 52$:$2^5 = 32$ 不夠,$2^6 = 64$ 夠 → **6 位元**。
4. (c) $k = 1000$:$2^9 = 512$ 不夠,$2^{10} = 1024$ 夠 → **10 位元**。
5. 注意:位元數只和「有幾種」有關,和這些東西本身的數值大小無關。

### 例 2
A sensor outputs 0 V to 5 V. It is digitized with 3 bits (levels 0–7, evenly spaced). Which level represents 3.2 V, and what voltage does that level stand for?

1. 3 位元有 $2^3 = 8$ 個等級,編號 0 到 7;第 0 級是 0 V、第 7 級是 5 V。
2. 相鄰等級差 $5 / 7 \approx 0.714$ V。
3. $3.2 / 0.714 \approx 4.48$,四捨五入到 **第 4 級**(二進位 100)。
4. 第 4 級代表 $4 \times 5/7 \approx 2.86$ V。原本是 3.2 V,誤差約 0.34 V——這就是**量化誤差**,位元越多、誤差越小。

## 易錯點
- 用 $\log_2 k$ 但忘了無條件進位。
- 以為 $n$ 位能表示的最大數是 $2^n$(其實是 $2^n - 1$,但種類是 $2^n$)。
- 以為數位訊號完全不受雜訊影響:雜訊太大仍會判斷錯,只是誤差不會累積。

## 教學提示
例 2 可以請學生猜「用 8 位元時誤差最大是多少」($5/255/2 \approx 0.01$ V),連到 C3.7 的聲音量化。Lab 任務 1 的 `digitize()` 就是例 2 的程式版。

## 練習
### 照做
How many bits are needed to give a unique code to each of 26 letters?

#### 解答
$2^4 = 16 < 26 \le 32 = 2^5$ → 5 位元。

### 是非
True or false: A digital signal can be regenerated because it only needs to be recognized as one of two levels.

#### 解答
True。接收端只要判斷高或低,就能送出全新的乾淨脈波。

### 變化
A system must distinguish 300 different colors. How many bits does it need, and how many patterns will be unused?

#### 解答
$2^8 = 256 < 300 \le 512 = 2^9$ → 9 位元;$512 - 300 = 212$ 個樣子用不到。

### 應用
A 0–10 V signal is digitized with 4 bits (16 evenly spaced levels, level 0 = 0 V, level 15 = 10 V). Which level represents 7.2 V, and what is the quantization error?

#### 解答
步長 $10/15 \approx 0.667$ V;$7.2 / 0.667 = 10.8$ → 四捨五入第 11 級(二進位 1011)。第 11 級代表 $11 \times 10/15 \approx 7.33$ V,誤差約 0.13 V。

#### 備註
Lab 的 `digitize()` 規定用 `floor(x + 0.5)` 四捨五入;若題目剛好落在 .5,浮點誤差可能讓結果往任一邊偏,出題時避開。

### 挑戰
Explain why copying a digital file 1000 times gives an identical file, but copying an analog tape 1000 times does not.

#### 解答
數位複製是讀出每個位元(判斷 0 或 1)再寫出,只要每次判斷都對,位元完全相同,誤差不累積。類比複製是把連續的訊號放大再錄下,每次都會加入一點雜訊與失真,而且無法分辨哪部分是原訊號、哪部分是雜訊,1000 次後累積的誤差很大。

## 驗算
```check
bits_for(7) == 3 and bits_for(52) == 6 and bits_for(1000) == 10
bits_for(26) == 5 and bits_for(300) == 9 and 2**9 - 300 == 212
math.floor(3.2 / (5 / 7) + 0.5) == 4
math.floor(7.2 / (10 / 15) + 0.5) == 11
round(11 * 10 / 15 - 7.2, 2) == 0.13
```
