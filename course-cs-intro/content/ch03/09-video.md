---
id: C3.9
title_en: Representing Video
title_zh: 影片的表示
sub: Codecs, temporal and spatial compression
level: mid
lab_hook: "任務 8:`delta_encode()`、`delta_decode()`、`compression_ratio()`"
---
## 觀念
A video is a sequence of images (**frames**) shown quickly, typically 24–60 **frames per second (fps)**. Uncompressed video is enormous:

$$\text{bytes per second} = \text{width} \times \text{height} \times \frac{\text{bits per pixel}}{8} \times \text{fps}.$$

A **video codec** (COmpressor/DECompressor) shrinks it with two kinds of compression:

- **Temporal compression** exploits similarity **between consecutive frames**. A **key frame** is stored in full; the following frames store only the **differences (deltas)** from the previous frame. Key frames are repeated regularly so that playback can start or jump anywhere.
- **Spatial compression** exploits redundancy **within one frame**, like image compression (large areas of similar color, detail the eye barely notices).

Most codecs are **lossy** (H.264/AVC, H.265/HEVC, AV1).

![A stream of key frames and delta frames.](keyframe-delta.svg)

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| frame | 影格 | 影片中的一張影像 |
| frames per second (fps) | 每秒影格數 | 影格播放速率 |
| codec | 編解碼器 | 壓縮與解壓縮影片的方法 |
| temporal compression | 時間壓縮 | 利用影格之間的相似 |
| spatial compression | 空間壓縮 | 利用同一影格內的相似 |
| key frame | 關鍵影格 | 完整儲存的影格 |
| delta frame | 差異影格 | 只存與前一格不同之處 |
| bit rate | 位元率 | 每秒的資料量 |

## 白話說
連續兩格影像通常幾乎一樣:主播在說話,背景完全沒動。所以只要記「哪些像素變了、變成什麼」。但如果每一格都只存差異,想從影片中間開始看,就得從頭一路算上來——所以每隔一段就放一張完整的關鍵影格。

關鍵影格越密,跳轉越快、但檔案越大;越疏,檔案越小、但跳轉慢,而且一出錯會影響後面很多格。這是一個取捨。

## 後面會用到
- **多媒體**、**電腦圖學**:動作估計(motion estimation)、DCT。
- **計算機網路**:串流的位元率、緩衝、自適應串流(第 15 章)。
- **演算法**:「只存差異」的想法也用在版本控制(git 的 delta 壓縮)與檔案同步(rsync)。

## 現代補充
現代 codec 的差異影格不只是「像素變了」,還會找出「這一塊是從上一格的哪裡**移動**過來的」(motion vector),只存移動量與殘差。AV1 是由多家公司開發、免授權金的 codec,YouTube 與 Netflix 大量使用。

## 原理
**為什麼時間壓縮在影片中特別有效?** 攝影機拍的畫面,1/30 秒內大部分像素的變化非常小。若一格有 $N$ 個像素、只有比例 $p$ 改變,差異影格大約只需要 $pN$ 個像素的資料(加上位置資訊),而 $p$ 常常小於 0.1。

**key frame 的間隔怎麼取捨?** 設每 $G$ 格一張關鍵影格(GOP 大小),關鍵影格大小 $K$、差異影格平均大小 $D \ll K$。每格平均大小 $\approx (K + (G - 1) D) / G$,$G$ 越大越接近 $D$;但跳到任一格最多要從前一張關鍵影格重算 $G - 1$ 次差異。

## 老師講解
### 例 1
How many bytes per second does uncompressed 1080p video (1920 × 1080, 24-bit color, 30 fps) need? How big is one uncompressed minute?

1. 每格:$1920 \times 1080 \times 3 = 6{,}220{,}800$ 位元組。
2. 每秒:$\times 30 = 186{,}624{,}000$ 位元組 ≈ 178 MiB/s。
3. 一分鐘:$\times 60 = 11{,}197{,}440{,}000$ 位元組 ≈ 10.4 GiB。
4. 一般 1080p 串流約 5 Mbps = 625,000 位元組/秒,壓縮比約 $625000 / 186624000 \approx 0.0033$(約 1/300)。

### 例 2
A 100 × 100 grayscale video (1 byte per pixel) has a key frame every 10 frames. On average 5% of pixels change between consecutive frames, and each delta records a changed pixel with 3 bytes (a 2-byte position and the new value). Estimate the average bytes per frame.

1. 關鍵影格:$100 \times 100 = 10{,}000$ 位元組。
2. 差異影格:改變 $5\% \times 10000 = 500$ 個像素,每個 3 位元組 → $1{,}500$ 位元組。
3. 每 10 格:1 張關鍵影格 + 9 張差異影格 = $10000 + 9 \times 1500 = 23{,}500$ 位元組。
4. 平均每格 $2{,}350$ 位元組,壓縮比 $2350 / 10000 = 0.235$。

## 易錯點
- 位元與位元組混用(Mbps 是百萬**位元**每秒)。
- 以為差異影格一定比關鍵影格小:場景切換時,幾乎每個像素都變,差異影格可能比完整影格還大——好的 codec 會在這時直接插入關鍵影格。
- 把時間壓縮與空間壓縮搞反。

## 教學提示
可以用手機錄一段靜止畫面與一段快速搖晃的影片,比較檔案大小,直觀感受時間壓縮。Lab 任務 8 讓學生實作最簡單的差異編碼,延伸專案 3 做一個迷你 codec。

## 練習
### 照做
How many bytes does one uncompressed 640 × 480 frame with 24-bit color take? At 25 fps, how many bytes per second?

#### 解答
$640 \times 480 \times 3 = 921{,}600$ 位元組;每秒 $\times 25 = 23{,}040{,}000$ 位元組。

### 是非
True or false: Temporal compression reduces redundancy within a single frame.

#### 解答
False。那是空間壓縮;時間壓縮是利用影格**之間**的相似。

### 變化
In example 2, what is the average size per frame if a key frame appears every 5 frames instead of 10?

#### 解答
每 5 格:$10000 + 4 \times 1500 = 16{,}000$ → 平均 3,200 位元組/格。

### 應用
Explain why jumping to minute 42 of a movie is fast, even though most frames store only differences.

#### 解答
影片每隔固定時間(例如每 1–2 秒)有一張關鍵影格。播放器跳到 42 分前最近的關鍵影格,完整解出它,再往後套用少數幾張差異影格即可,不必從頭算起。

### 挑戰
When a scene cuts from an indoor shot to an outdoor shot, what happens to a delta frame, and what should the encoder do?

#### 解答
幾乎所有像素都改變,差異影格要記錄每個像素的位置與新值,比完整影格還大(位置資訊是額外成本)。編碼器應偵測到這種情況,直接在切換點插入一張關鍵影格。

## 驗算
```check
1920 * 1080 * 3 * 30 == 186624000 and 186624000 * 60 == 11197440000
round(5_000_000 / 8 / 186624000, 4) == 0.0033
10000 + 9 * 1500 == 23500 and 23500 / 10 / 10000 == 0.235
640 * 480 * 3 == 921600 and 921600 * 25 == 23040000
(10000 + 4 * 1500) / 5 == 3200
```
