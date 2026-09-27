/* 任務 3 參考解(C3.4)。 */
#include "floats.h"

#include <stdio.h>
#include <string.h>

uint32_t f32_to_bits(float x) {
    uint32_t b;
    memcpy(&b, &x, sizeof b);   /* 不用指標轉型:那違反 strict aliasing */
    return b;
}

float f32_from_bits(uint32_t b) {
    float x;
    memcpy(&x, &b, sizeof x);
    return x;
}

struct f32info f32_decode(uint32_t b) {
    struct f32info i;
    i.sign = (int)(b >> 31);
    i.exp_bits = (int)((b >> 23) & 0xFF);
    i.frac = b & 0x7FFFFF;
    i.unbiased = 0;
    if (i.exp_bits == 0) {
        i.kind = i.frac ? F_DENORMAL : F_ZERO;
        if (i.frac) i.unbiased = -126;
    } else if (i.exp_bits == 255) {
        i.kind = i.frac ? F_NAN : F_INF;
    } else {
        i.kind = F_NORMAL;
        i.unbiased = i.exp_bits - 127;
    }
    return i;
}

uint32_t f32_encode(int sign, int exp_bits, uint32_t frac) {
    return ((uint32_t)(sign & 1) << 31) | ((uint32_t)(exp_bits & 0xFF) << 23) | (frac & 0x7FFFFF);
}

int f32_binary_sci(uint32_t b, char *out, size_t cap) {
    struct f32info i = f32_decode(b);
    char tmp[64];
    int n;
    if (i.kind == F_ZERO) n = snprintf(tmp, sizeof tmp, "%c0", i.sign ? '-' : '+');
    else if (i.kind == F_INF) n = snprintf(tmp, sizeof tmp, "%cinf", i.sign ? '-' : '+');
    else if (i.kind == F_NAN) n = snprintf(tmp, sizeof tmp, "nan");
    else {
        char digits[24];
        int k = 0;
        for (int bit = 22; bit >= 0; bit--) digits[k++] = (char)('0' + (int)((i.frac >> bit) & 1));
        while (k > 1 && digits[k - 1] == '0') k--;   /* 去掉尾端的 0,至少留一位 */
        digits[k] = '\0';
        n = snprintf(tmp, sizeof tmp, "%s%c.%s x 2^%d", i.sign ? "-" : "", i.kind == F_NORMAL ? '1' : '0',
                     digits, i.unbiased);
    }
    if (n < 0 || (size_t)n + 1 > cap) return -1;
    memcpy(out, tmp, (size_t)n + 1);
    return n;
}
