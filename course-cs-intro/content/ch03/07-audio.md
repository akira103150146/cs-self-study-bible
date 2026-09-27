---
id: C3.7
title_en: Representing Audio
title_zh: 聲音的表示
sub: Sampling rate, bit depth, Nyquist, and MP3
level: mid
lab_hook: "任務 6:`quantize()`、`synth_sine()`、`snr_db()`、`pcm_bytes()`、`alias_freq()`、`wav_write()`"
---
## 觀念
Sound is a continuous pressure wave. To store it digitally we **sample** it: measure its amplitude at regular intervals. Two numbers describe the result:

- **Sampling rate**: samples per second (Hz). Audio CDs use 44,100 samples per second.
- **Bit depth** (**quantization**): how many bits each sample uses. CDs use 16 bits, i.e. 65,536 levels.

The **Nyquist–Shannon sampling theorem** says that to capture frequencies up to $f_{\max}$ we must sample at a rate of more than $2 f_{\max}$. Humans hear up to about 20 kHz, which is why 44.1 kHz was chosen. A frequency above half the sampling rate is not lost silently — it shows up as a false lower frequency (**aliasing**): sampled at rate $r$, a tone of frequency $f$ is heard as the distance from $f$ to the nearest multiple of $r$.

The uncompressed (**PCM**) data size is

$$\text{bytes} = \text{rate} \times \frac{\text{bit depth}}{8} \times \text{channels} \times \text{seconds}.$$

**Quantization noise**: rounding each sample adds error. For an $n$-bit quantizer and a full-scale sine wave, the signal-to-noise ratio is about $6.02n + 1.76$ dB — each extra bit adds about 6 dB.

**Audio formats**: WAV stores PCM samples (with a small header); **MP3** is lossy: it uses a **psychoacoustic model** to discard sounds humans cannot hear (too high, too quiet, or masked by louder sounds nearby) and then applies Huffman coding, reaching about 10:1 compression.

![Sampling at regular times and rounding each sample to one of 8 levels (3 bits).](sampling.svg)

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| sampling | 取樣 | 每隔固定時間量一次振幅 |
| sampling rate | 取樣率 | 每秒取樣次數,單位 Hz |
| bit depth / quantization | 位元深度/量化 | 每個樣本的位元數;把連續值捨入到有限等級 |
| Nyquist rate | 奈奎斯特頻率 | 取樣率至少要是最高頻率的兩倍 |
| aliasing | 混疊 | 取樣不足時,高頻被誤認成低頻 |
| PCM | 脈碼調變 | 未壓縮的原始樣本序列 |
| SNR | 訊雜比 | 訊號與雜訊的功率比,以 dB 表示 |
| psychoacoustics | 心理聲學 | 研究人耳聽得到/聽不到什麼 |

## 白話說
數位錄音就是「每秒拍 44,100 張照片,記下那一瞬間的音量」。拍得太慢,快速變化的聲音(高頻)就抓不到,甚至會被誤認成另一個較低的音——就像電影裡車輪看起來倒轉。

每張「照片」用幾個位元記錄音量,決定了細緻程度:8 位元只有 256 級,聽得出沙沙的雜音;16 位元有 65,536 級,人耳已經聽不出差別。

## 後面會用到
- **訊號與系統**、**數位訊號處理**:取樣定理、混疊、濾波。
- **計算機網路**:串流的位元率決定頻寬需求(第 15 章)。
- **演算法**:MP3 的最後一步是 Huffman(C3.6)。

## 原理
**為什麼要兩倍?** 一個頻率 $f$ 的正弦波每週期上升一次、下降一次;每週期至少要兩個樣本才能看出它「有起伏」。更精確地說,取樣後頻率 $f$ 和 $r - f$、$r + f$、… 產生完全相同的樣本(因為 $\cos(2\pi f k / r) = \cos(2\pi (r - f) k / r)$),所以只有 $[0, r/2]$ 內的頻率能被唯一辨認;超出的會被「摺」回這個區間。

**為什麼每多一位元 SNR 多約 6 dB?** 量化誤差大約均勻分布在 $\pm \Delta / 2$,功率 $\Delta^2 / 12$;每多一位元,$\Delta$ 減半、雜訊功率變成 1/4,即 $10 \log_{10} 4 \approx 6.02$ dB。

## 老師講解
### 例 1
How many bytes does one minute of CD-quality stereo audio take uncompressed? What bit rate is that, and roughly how big is a 128 kbps MP3 of the same minute?

1. CD:44,100 Hz、16 位元、2 聲道。
2. 每秒:$44100 \times 2 \times 2 = 176{,}400$ 位元組。
3. 一分鐘:$176400 \times 60 = 10{,}584{,}000$ 位元組 ≈ 10.1 MiB。
4. 位元率:$176400 \times 8 = 1{,}411{,}200$ bps ≈ 1411 kbps。
5. 128 kbps 的 MP3:$128000 \times 60 / 8 = 960{,}000$ 位元組,約為 PCM 的 $1/11$。

### 例 2
A 30 kHz tone is sampled at 44.1 kHz. What frequency will you hear on playback? What about a 25 kHz tone sampled at 48 kHz?

1. 取樣後只能表示 $[0, r/2]$ 的頻率;$r/2 = 22.05$ kHz,30 kHz 超出。
2. 找最接近的 $r$ 的倍數:$44.1$ kHz。距離 $|30 - 44.1| = 14.1$ kHz。
3. 播放時聽到 **14.1 kHz**——一個原本不存在的音。
4. 25 kHz、$r = 48$ kHz:$|25 - 48| = 23$ kHz,聽到 23 kHz(超出人耳範圍,但仍是錯的)。
5. 這就是錄音設備在取樣前要先用低通濾波器濾掉高頻的原因。

## 易錯點
- 資料量公式忘了除以 8(位元 → 位元組)或忘了乘聲道數。
- 以為取樣率剛好等於 $2 f_{\max}$ 就一定夠:定理要求**大於**兩倍。
- 以為高於 Nyquist 的頻率會「消失」:它會混疊成假的低頻。

## 教學提示
可以用 Lab 任務 6 的 `wavgen` 產生 8 位元與 16 位元的 440 Hz,讓學生戴耳機聽差別;再產生一個超過 Nyquist 的音,聽聽混疊。

## 練習
### 照做
How many bytes does 10 seconds of mono audio at 8,000 Hz and 8 bits take?

#### 解答
$8000 \times 1 \times 1 \times 10 = 80{,}000$ 位元組。

### 是非
True or false: Sampling at 40 kHz is enough to capture a 25 kHz tone.

#### 解答
False。需要大於 $2 \times 25 = 50$ kHz。

### 變化
What is the approximate SNR of 8-bit and 24-bit quantization?

#### 解答
8 位元:$6.02 \times 8 + 1.76 \approx 49.9$ dB;24 位元:$6.02 \times 24 + 1.76 \approx 146.2$ dB。

### 應用
A podcast is recorded at 48 kHz, 24 bits, stereo, for 30 minutes. How many bytes is the raw recording?

#### 解答
$48000 \times 3 \times 2 \times 1800 = 518{,}400{,}000$ 位元組(約 494 MiB)。

### 挑戰
Show that a tone of frequency $f$ and a tone of frequency $r - f$ produce identical samples when sampled at rate $r$ (use cosines).

#### 解答
第 $k$ 個樣本:$\cos(2\pi (r - f) k / r) = \cos(2\pi k - 2\pi f k / r) = \cos(2\pi f k / r)$,因為 $\cos$ 的週期是 $2\pi$ 且是偶函數。所以每個樣本都相同,取樣後無法分辨。

## 驗算
```check
pcm_bytes(44100, 16, 2, 60) == 10584000
pcm_bytes(44100, 16, 2, 1) * 8 == 1411200
128000 * 60 // 8 == 960000
pcm_bytes(8000, 8, 1, 10) == 80000
round(6.02 * 8 + 1.76, 1) == 49.9 and round(6.02 * 24 + 1.76, 1) == 146.2
pcm_bytes(48000, 24, 2, 1800) == 518400000
abs(30000 - 44100) == 14100
```
