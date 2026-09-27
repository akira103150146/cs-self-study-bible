/* 任務 8 參考解(C3.9)。 */
#include "video.h"

#include <string.h>

long delta_encode(const uint8_t *prev, const uint8_t *cur, size_t n, uint8_t *out, size_t cap) {
    size_t len = 0, i = 0;
    while (i < n) {
        if (prev[i] == cur[i]) {
            i++;
            continue;
        }
        size_t j = i;
        while (j < n && prev[j] != cur[j] && j - i < 65535) j++;   /* 一段連續改變的位元組 */
        size_t run = j - i;
        if (len + 6 + run > cap) return -1;
        for (int k = 0; k < 4; k++) out[len++] = (uint8_t)(i >> (8 * k));
        out[len++] = (uint8_t)run;
        out[len++] = (uint8_t)(run >> 8);
        memcpy(out + len, cur + i, run);
        len += run;
        i = j;
    }
    return (long)len;
}

long delta_decode(const uint8_t *prev, const uint8_t *delta, size_t dn, uint8_t *cur, size_t n) {
    memcpy(cur, prev, n);
    size_t p = 0;
    while (p < dn) {
        if (dn - p < 6) return -1;
        size_t start = (size_t)delta[p] | (size_t)delta[p + 1] << 8 | (size_t)delta[p + 2] << 16 |
                       (size_t)delta[p + 3] << 24;
        size_t run = (size_t)delta[p + 4] | (size_t)delta[p + 5] << 8;
        p += 6;
        if (dn - p < run || start > n || run > n - start) return -1;
        memcpy(cur + start, delta + p, run);
        p += run;
    }
    return 0;
}

double compression_ratio(uint64_t original, uint64_t compressed) {
    return original ? (double)compressed / (double)original : 0.0;
}
