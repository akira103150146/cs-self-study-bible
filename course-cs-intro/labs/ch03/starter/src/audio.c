#include "audio.h"

#include <math.h>

int32_t quantize(double x, int bits) {
    (void)x, (void)bits;
    return 0; /* TODO */
}

size_t synth_sine(double freq, int rate, double secs, int bits, int32_t *out, size_t cap) {
    (void)freq, (void)rate, (void)secs, (void)bits, (void)out, (void)cap;
    return 0; /* TODO */
}

double snr_db(const double *orig, const double *approx, size_t n) {
    (void)orig, (void)approx, (void)n;
    return 0.0; /* TODO */
}

uint64_t pcm_bytes(int rate, int bits, int channels, double secs) {
    (void)rate, (void)bits, (void)channels, (void)secs;
    return 0; /* TODO */
}

double alias_freq(double f, int rate) {
    (void)f, (void)rate;
    return -1.0; /* TODO */
}

int wav_write(const char *path, const int32_t *s, size_t n, int rate, int bits) {
    (void)path, (void)s, (void)n, (void)rate, (void)bits;
    return -1; /* TODO:44 位元組檔頭(見 Lab 規格)+ 樣本 */
}
