/* audio.h — 任務 6(C3.7)聲音。這個檔案已經寫好,不要改。 */
#ifndef AUDIO_H
#define AUDIO_H
#include <stddef.h>
#include <stdint.h>

int32_t quantize(double x, int bits);
/* x ∈ [−1, 1] → floor(x × M + 0.5),M = 2^(bits−1) − 1,結果夾在 [−M, M]。2 ≤ bits ≤ 32 */

size_t synth_sine(double freq, int rate, double secs, int bits, int32_t *out, size_t cap);
/* 產生 n = floor(rate × secs + 0.5) 個樣本:out[i] = quantize(sin(2π × freq × i / rate), bits)。
 * 回傳 n;cap < n → 什麼都不寫,回傳 0 */

double snr_db(const double *orig, const double *approx, size_t n);
/* 10 log10(Σ orig² / Σ (orig − approx)²);沒有誤差時回傳 INFINITY */

uint64_t pcm_bytes(int rate, int bits, int channels, double secs);
/* 樣本數 floor(rate × secs + 0.5) × channels × bits / 8 */

double alias_freq(double f, int rate);   /* 取樣後聽到的頻率,落在 [0, rate / 2] */

int wav_write(const char *path, const int32_t *s, size_t n, int rate, int bits);
/* 單聲道 PCM WAV。bits = 16:有號 little-endian;bits = 8:無號,存 s[i] + 128。其他 bits → -1。成功 0 */
#endif
