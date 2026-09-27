/* 任務 6 參考解(C3.7)。 */
#include "audio.h"

#include <math.h>
#include <stdio.h>

int32_t quantize(double x, int bits) {
    int64_t m = ((int64_t)1 << (bits - 1)) - 1;
    double v = floor(x * (double)m + 0.5);
    if (v > (double)m) v = (double)m;
    if (v < -(double)m) v = -(double)m;
    return (int32_t)v;
}

size_t synth_sine(double freq, int rate, double secs, int bits, int32_t *out, size_t cap) {
    size_t n = (size_t)floor(rate * secs + 0.5);
    if (cap < n) return 0;
    for (size_t i = 0; i < n; i++) out[i] = quantize(sin(2 * M_PI * freq * (double)i / rate), bits);
    return n;
}

double snr_db(const double *orig, const double *approx, size_t n) {
    double sig = 0, noise = 0;
    for (size_t i = 0; i < n; i++) {
        sig += orig[i] * orig[i];
        noise += (orig[i] - approx[i]) * (orig[i] - approx[i]);
    }
    if (noise == 0) return INFINITY;
    return 10 * log10(sig / noise);
}

uint64_t pcm_bytes(int rate, int bits, int channels, double secs) {
    uint64_t samples = (uint64_t)floor(rate * secs + 0.5);
    return samples * (uint64_t)channels * (uint64_t)bits / 8;
}

double alias_freq(double f, int rate) {
    double r = fmod(f, (double)rate);   /* 取樣後 f 與 f ± k·rate 無法分辨 */
    return r > rate / 2.0 ? rate - r : r;
}

static void put16(FILE *f, unsigned v) {
    fputc((int)(v & 0xFF), f);
    fputc((int)((v >> 8) & 0xFF), f);
}
static void put32(FILE *f, uint32_t v) {
    put16(f, v & 0xFFFF);
    put16(f, v >> 16);
}

int wav_write(const char *path, const int32_t *s, size_t n, int rate, int bits) {
    if (bits != 8 && bits != 16) return -1;
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    uint32_t bytes_ps = (uint32_t)(bits / 8), data = (uint32_t)(n * bytes_ps);
    fwrite("RIFF", 1, 4, f);
    put32(f, 36 + data);
    fwrite("WAVEfmt ", 1, 8, f);
    put32(f, 16);                              /* fmt 區塊長度 */
    put16(f, 1);                               /* PCM */
    put16(f, 1);                               /* mono */
    put32(f, (uint32_t)rate);
    put32(f, (uint32_t)rate * bytes_ps);       /* byte rate */
    put16(f, bytes_ps);                        /* block align */
    put16(f, (unsigned)bits);
    fwrite("data", 1, 4, f);
    put32(f, data);
    for (size_t i = 0; i < n; i++) {
        if (bits == 8) fputc(s[i] + 128, f);   /* 8 位元 WAV 是無號的 */
        else put16(f, (unsigned)(uint16_t)(int16_t)s[i]);
    }
    return fclose(f) == 0 ? 0 : -1;
}
