---
lang: c
dir: labs/ch03
---
## 概要
你要用 C 寫一個資料表示的函式庫 `datarep`,把第 3 章的每一種表示法都親手實作一次:數位化、負數與溢位、IEEE 754 浮點數、UTF-8、三種文字壓縮(其中 Huffman 要做成**真的能壓縮檔案**的 `hzip`)、聲音、BMP 影像、影片的差異影格、位元組順序。

每個任務對應一個標頭檔(`src/*.h`,已寫好,不要改)和一個你要完成的 `.c` 檔。另外有三個已經寫好的指令列工具,做完對應的任務就能用:

```text
$ ./build/floatdump -6.25                    # 任務 3
bits     1 10000001 10010000000000000000000
hex      0xC0C80000
binary   -1.1001 x 2^2
$ ./build/hzip c data/english.txt e.hz        # 任務 5
4389 -> 2632 bytes (ratio 0.600)
$ ./build/wavgen 440 44100 16 2 a440.wav      # 任務 6:用耳機聽聽看
```

`data/` 裡有測試用的檔案:一篇英文文章、全部同一個位元組的檔案、隨機位元組、幾張小 BMP。

## 環境
```text
docker run --rm -it -v "$PWD:/work" cs-intro-env bash
make build                                  # 編譯函式庫、三個工具與測試
make test                                   # 跑全部公開測試(三個測試檔)
./build/test_text C3_6_rle_encode_basic     # 只跑一個測試
```

編譯時開了 AddressSanitizer 與 UndefinedBehaviorSanitizer:越界、記憶體洩漏、**有號整數溢位**都會讓測試失敗。任務 2 要特別小心——模擬「繞回」時不能讓 C 的有號整數真的溢位。

## 任務 1 · 類比與數位 · C3.1
```c interface
int bits_for_items(uint64_t k);                  /* 要區分 k 樣東西至少要幾個位元;k = 1 → 1 */
int digitize(double v, double vmax, int bits);   /* 0..vmax 均分成 2^bits 級,回傳最接近的等級(夾在範圍內) */
```

等級的算法:`floor(v / vmax * (2^bits − 1) + 0.5)`。

## 任務 2 · 負數與溢位 · C3.2, C3.3
三種負數表示法,以及二補數的溢位偵測與繞回。

```c interface
int to_signmag(int64_t v, int bits, char *out);   /* 成功 0;v 超出範圍或 bits 不在 2–64 → -1 */
int to_ones(int64_t v, int bits, char *out);
int to_twos(int64_t v, int bits, char *out);
int64_t from_twos(const char *s);                 /* 1–64 位的 '0'/'1' 字串 */
int64_t sign_extend(uint64_t raw, int bits);      /* 取低 bits 位當二補數,延伸成 64 位元 */
int add_overflows(int64_t a, int64_t b, int bits);
int64_t wrap_add(int64_t a, int64_t b, int bits);
```

範例:`to_twos(-37, 8, buf)` → `"11011011"`;`wrap_add(100, 100, 8)` → −56;`add_overflows(127, 1, 8)` → 1。

提示:`(uint64_t)a + (uint64_t)b` 保證繞回,再用 `sign_extend` 取低 `bits` 位。

## 任務 3 · IEEE 754 浮點數 · C3.4
```c interface
uint32_t f32_to_bits(float x);
float f32_from_bits(uint32_t b);
struct f32info f32_decode(uint32_t b);                         /* 拆出 sign / exp_bits / frac / unbiased / kind */
uint32_t f32_encode(int sign, int exp_bits, uint32_t frac);
int f32_binary_sci(uint32_t b, char *out, size_t cap);         /* "-1.1001 x 2^2"、"+0"、"-inf"、"nan" … */
```

`kind` 是 `F_ZERO`、`F_DENORMAL`、`F_NORMAL`、`F_INF`、`F_NAN` 之一;非正規數的 `unbiased` 是 −126。取位元請用 `memcpy`,不要用 `*(uint32_t *)&x`(違反 strict aliasing)。完整的輸出格式寫在 `src/floats.h`。

## 任務 4 · UTF-8 · C3.5
```c interface
int utf8_encode(uint32_t cp, uint8_t out[4]);                  /* 回傳 1–4;surrogate 或 > U+10FFFF → -1 */
int utf8_decode(const uint8_t *s, size_t n, uint32_t *cp);     /* 回傳用掉的位元組數;不合法 → -1 */
long utf8_count(const uint8_t *s, size_t n);
int ascii_toggle_case(int c);
```

`utf8_decode` 必須拒絕:延續位元組當開頭、`F8`–`FF`、序列不完整、延續位元組不是 `10xxxxxx`、**過長編碼**(例如 `C0 80`)、surrogate、超過 U+10FFFF。

## 任務 5 · 文字壓縮與 hzip · C3.6
```c interface
long keyword_encode(const char *in, const struct keyword *kw, size_t nkw, char *out, size_t cap);
long rle_encode(const char *in, char *out, size_t cap);
long rle_decode(const char *in, char *out, size_t cap);
int huff_code_lengths(const uint64_t freq[256], uint8_t len[256]);
uint64_t huff_total_bits(const uint64_t freq[256], const uint8_t len[256]);
long huff_compress(const uint8_t *in, size_t n, uint8_t *out, size_t cap);
long huff_decompress(const uint8_t *in, size_t n, uint8_t *out, size_t cap);
```

- 關鍵字編碼只取代**完整的單字**(`the` 不取代 `there` 裡的 the)。
- RLE 照講義 C3.6 的規則(`*` + 字元 + 個數,4–9 個)。
- 壓縮檔格式:4 位元組原始長度(little-endian)+ 256 位元組的碼長表 + canonical Huffman 位元流(由每個位元組的最高位開始填)。canonical 碼只由碼長決定,所以只要存碼長表,解壓縮端就能重建出一模一樣的碼。碼長不會超過 32。
- 解壓縮要拒絕壞檔:檔頭不完整、碼長表不可能是前綴碼(Kraft 不等式不成立)、位元流不夠。

驗收:`data/english.txt` 壓縮後要小於原本的 70%;空檔案、只有一種位元組、隨機位元組都要能正確往返。

## 任務 6 · 聲音 · C3.7
```c interface
int32_t quantize(double x, int bits);
size_t synth_sine(double freq, int rate, double secs, int bits, int32_t *out, size_t cap);
double snr_db(const double *orig, const double *approx, size_t n);
uint64_t pcm_bytes(int rate, int bits, int channels, double secs);
double alias_freq(double f, int rate);
int wav_write(const char *path, const int32_t *s, size_t n, int rate, int bits);
```

WAV 檔頭(44 位元組,全部 little-endian):`"RIFF"`、`36 + 資料長度`、`"WAVE"`、`"fmt "`、`16`、格式 `1`(PCM,2 位元組)、聲道數(2 位元組)、取樣率、byte rate、block align(2 位元組)、位元數(2 位元組)、`"data"`、資料長度,然後是樣本。8 位元的樣本是**無號**的(存 `s + 128`)。

實驗:用 `wavgen` 產生 8 位元與 16 位元的同一個音,聽聽看差別;隱藏測試會檢查 8 位元量化的 SNR 是否接近理論值 $6.02 \times 8 + 1.76$ dB。

## 任務 7 · BMP 影像 · C3.8
```c interface
int bmp_read(const char *path, struct image *img);
int bmp_write(const char *path, const struct image *img);
void image_free(struct image *img);
void to_gray(struct image *img);
void invert(struct image *img);
uint64_t raw_image_bytes(int w, int h, int bpp);
int palette_index(const struct image *img, const uint8_t (*pal)[3], int n, uint8_t *idx);
int svg_rect(char *buf, size_t cap, int x, int y, int w, int h, uint32_t rgb);
```

`struct image` 的像素一律是**由上而下、RGB**;BMP 檔案裡是由下而上(高度為負時由上而下)、BGR、每列補齊到 4 的倍數。只需支援 24 位元未壓縮的 BMP,其他一律回傳 −1。

## 任務 8 · 影片的差異影格 · C3.9
```c interface
long delta_encode(const uint8_t *prev, const uint8_t *cur, size_t n, uint8_t *out, size_t cap);
long delta_decode(const uint8_t *prev, const uint8_t *delta, size_t dn, uint8_t *cur, size_t n);
double compression_ratio(uint64_t original, uint64_t compressed);
```

差異的格式是一串區段:起點(4 位元組 LE)、長度(2 位元組 LE)、新的位元組。一個區段是一段**連續改變**的位元組,長度超過 65535 要切開。解碼要拒絕超出範圍或不完整的區段。

## 任務 9 · 位元組順序 · C3.10
```c interface
int host_is_little(void);
uint32_t bswap32(uint32_t x);
uint32_t read_le32(const uint8_t *p);
uint32_t read_be32(const uint8_t *p);
void write_le32(uint8_t *p, uint32_t x);
```

任務 6、7 讀寫檔頭時就用這幾個函式。

## 繳交
`make test` 全部通過後,把 `src/*.c` 提交到你的 git repo。隱藏測試會檢查大量邊界情況,例如:`INT64_MIN`、`-128` 的一補數、最小的非正規數、`C0 80` 與 `ED A0 80`、一段 70,000 位元組的連續改變、寬 101 像素(每列要補 1 個位元組)的 BMP、高度為負的 BMP、壞掉的壓縮檔,以及三個指令列工具的輸出。
