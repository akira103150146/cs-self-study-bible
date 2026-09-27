---
id: C3.8
title_en: Representing Images and Graphics
title_zh: 影像與圖形的表示
sub: RGB, color depth, raster vs. vector, and image formats
level: mid
lab_hook: "任務 7:`bmp_read()`/`bmp_write()`、`to_gray()`、`invert()`、`raw_image_bytes()`、`palette_index()`、`svg_rect()`"
---
## 觀念
**Color** is represented with the **RGB** model: each color is a mix of red, green, and blue intensities. The number of bits per pixel is the **color depth**: **true color** uses 24 bits (8 per channel, $2^{24} \approx 16.7$ million colors), sometimes 32 bits with an extra alpha (transparency) channel. **Indexed color** stores a small **palette** (for example 256 colors) and gives each pixel just an index into it, saving space at the cost of fewer colors.

A **raster** (bitmap) image is a grid of **pixels**; its **resolution** is the number of pixels. Uncompressed size:

$$\text{bytes} = \text{width} \times \text{height} \times \frac{\text{bits per pixel}}{8}.$$

A **vector graphic** instead describes shapes (lines, rectangles, curves) with their positions and colors. It scales to any size without becoming blocky and is usually small for drawings, but it is poor for photographs.

Common formats:

| Format | Kind | Compression | Typical use |
|---|---|---|---|
| BMP | raster | none (usually) | simple, easy to read and write |
| GIF | raster, indexed (≤ 256 colors) | lossless (LZW) | simple graphics, animation |
| PNG | raster | lossless (DEFLATE) | screenshots, graphics, transparency |
| JPEG | raster | lossy (discards detail the eye barely sees) | photographs |
| SVG | vector | text (can be gzipped) | icons, diagrams, fonts |

A 24-bit BMP stores rows **bottom-up**, pixels as **B, G, R**, and pads each row to a multiple of 4 bytes.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| pixel | 像素 | 點陣影像的最小單位 |
| RGB | RGB 色彩模型 | 紅綠藍三原色光的強度 |
| color depth | 色彩深度 | 每個像素的位元數 |
| true color | 全彩 | 24 位元色彩,每個通道 8 位元 |
| indexed color / palette | 索引色/調色盤 | 像素存調色盤的編號 |
| raster / bitmap | 點陣圖 | 以像素格子表示的影像 |
| vector graphics | 向量圖 | 以幾何形狀描述的圖形 |
| resolution | 解析度 | 影像的像素數(寬 × 高) |

## 白話說
點陣圖就是一張方格紙,每一格塗一個顏色;方格越多(解析度越高)越細緻,檔案也越大。向量圖則是一份「畫圖指令」:「在 (10, 20) 畫一個 50×30 的紅色矩形」——放大十倍也只是把座標乘十,永遠清晰。

照片用 JPEG,因為它會丟掉人眼不太分辨得出的細節;螢幕截圖或文字用 PNG,因為 JPEG 會在銳利的邊緣產生雜點;圖示用 SVG。

## 後面會用到
- **電腦圖學**:光柵化(把向量畫成像素)、色彩空間、光線追蹤(第 14 章延伸)。
- **影像處理**、**電腦視覺**:濾鏡就是對每個像素的運算。
- **計算機網路**與**Web**:網頁圖片格式的選擇直接影響載入速度。

## 現代補充
- 新格式 **WebP**、**AVIF** 同時支援有損與無損,壓縮率比 JPEG/PNG 更好,現在的瀏覽器都支援。
- 螢幕越來越常用 **HDR** 與每通道 10 位元以上的色彩深度。

## 原理
**為什麼灰階轉換用 $0.299R + 0.587G + 0.114B$ 而不是平均?** 人眼對綠色最敏感、藍色最不敏感;這組權重(ITU-R BT.601)讓轉出來的亮度和人眼感受一致。

**為什麼 BMP 每列要補齊到 4 的倍數?** 早期硬體一次讀 32 位元(4 位元組)效率最好,讓每列都從 4 的倍數位址開始。寬度 $w$ 的 24 位元影像每列 $3w$ 位元組,補齊後是 $4 \lceil 3w / 4 \rceil$。

**為什麼索引色能省空間?** 256 色調色盤只要 256 × 3 = 768 位元組,每個像素從 24 位元變成 8 位元,影像越大越划算;代價是顏色超過 256 種時必須用最接近的顏色取代(或用抖色模擬)。

## 老師講解
### 例 1
How many bytes does an uncompressed 1920 × 1080 image take in true color? In 256-color indexed mode (including the palette)?

1. 全彩 24 位元 = 3 位元組/像素。
2. $1920 \times 1080 = 2{,}073{,}600$ 個像素 × 3 = $6{,}220{,}800$ 位元組 ≈ 5.93 MiB。
3. 索引色:每像素 1 位元組 → $2{,}073{,}600$ 位元組,加上調色盤 $256 \times 3 = 768$ 位元組。
4. 總共 $2{,}074{,}368$ 位元組,約全彩的 1/3。

### 例 2
A 24-bit BMP is 3 pixels wide and 2 pixels tall. How many bytes does each row take in the file, and how large is the pixel array?

1. 每像素 3 位元組,每列 $3 \times 3 = 9$ 位元組。
2. 補齊到 4 的倍數:$\lceil 9 / 4 \rceil \times 4 = 12$ 位元組,每列補 3 個 0。
3. 像素陣列 $12 \times 2 = 24$ 位元組(而不是 $9 \times 2 = 18$)。
4. 讀檔時若忘了跳過補齊的位元組,第二列開始每個像素都會錯位——這是 Lab 任務 7 的隱藏測試。

## 易錯點
- 忘了除以 8(位元→位元組)。
- BMP 的像素順序是 BGR、列由下而上,很多人讀出來影像上下顛倒或偏藍。
- 以為向量圖一定比點陣圖小:複雜的照片畫成向量反而非常大。
- 以為 PNG 是有損的。

## 教學提示
例 2 是寫 BMP 讀取程式最常見的 bug,務必在課堂算一次。可以用 `xxd` 看一個 2×2 BMP 的檔頭與像素資料,對照每個欄位。

## 練習
### 照做
How many bytes does an uncompressed 800 × 600 image with 24-bit color take?

#### 解答
$800 \times 600 \times 3 = 1{,}440{,}000$ 位元組。

### 是非
True or false: JPEG is a lossless format.

#### 解答
False。JPEG 是有損壓縮,會丟掉人眼不易察覺的細節。

### 變化
Convert the pixel $(R, G, B) = (200, 100, 50)$ to grayscale using $Y = 0.299R + 0.587G + 0.114B$, rounded to the nearest integer. What is its inverted color?

#### 解答
$Y = 59.8 + 58.7 + 5.7 = 124.2$ → 124。反相色 $(255 - 200, 255 - 100, 255 - 50) = (55, 155, 205)$。

### 應用
A 24-bit BMP is 101 pixels wide and 50 pixels tall. How many padding bytes does each row need, and how many bytes is the pixel array?

#### 解答
每列 $3 \times 101 = 303$ 位元組,補到 304,每列補 1 個位元組;像素陣列 $304 \times 50 = 15{,}200$ 位元組。

### 挑戰
Which format would you choose for (a) a company logo that must look sharp at any size, (b) a photo of a sunset, (c) a screenshot of source code? Justify each.

#### 解答
(a) SVG:向量圖任意縮放不失真,而且檔案小。(b) JPEG(或 WebP/AVIF):照片色彩連續,有損壓縮在肉眼幾乎看不出差別下大幅縮小檔案。(c) PNG:無損,文字邊緣銳利;JPEG 會在文字周圍產生雜點。

## 驗算
```check
image_bytes(1920, 1080, 24) == 6220800
1920 * 1080 + 256 * 3 == 2074368
math.ceil(9 / 4) * 4 * 2 == 24
image_bytes(800, 600, 24) == 1440000
round(0.299 * 200 + 0.587 * 100 + 0.114 * 50) == 124
math.ceil(303 / 4) * 4 == 304 and 304 * 50 == 15200
```
