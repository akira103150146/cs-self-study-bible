/* 任務 4 參考解(C3.5)。 */
#include "utf8.h"

static int is_surrogate(uint32_t cp) { return cp >= 0xD800 && cp <= 0xDFFF; }

int utf8_encode(uint32_t cp, uint8_t out[4]) {
    if (cp > 0x10FFFF || is_surrogate(cp)) return -1;
    if (cp < 0x80) {
        out[0] = (uint8_t)cp;
        return 1;
    }
    if (cp < 0x800) {
        out[0] = (uint8_t)(0xC0 | cp >> 6);
        out[1] = (uint8_t)(0x80 | (cp & 0x3F));
        return 2;
    }
    if (cp < 0x10000) {
        out[0] = (uint8_t)(0xE0 | cp >> 12);
        out[1] = (uint8_t)(0x80 | ((cp >> 6) & 0x3F));
        out[2] = (uint8_t)(0x80 | (cp & 0x3F));
        return 3;
    }
    out[0] = (uint8_t)(0xF0 | cp >> 18);
    out[1] = (uint8_t)(0x80 | ((cp >> 12) & 0x3F));
    out[2] = (uint8_t)(0x80 | ((cp >> 6) & 0x3F));
    out[3] = (uint8_t)(0x80 | (cp & 0x3F));
    return 4;
}

int utf8_decode(const uint8_t *s, size_t n, uint32_t *cp) {
    if (n == 0) return -1;
    uint8_t b = s[0];
    int len;
    uint32_t v, min;
    if (b < 0x80) {
        *cp = b;
        return 1;
    } else if ((b & 0xE0) == 0xC0) {
        len = 2, v = b & 0x1F, min = 0x80;
    } else if ((b & 0xF0) == 0xE0) {
        len = 3, v = b & 0x0F, min = 0x800;
    } else if ((b & 0xF8) == 0xF0) {
        len = 4, v = b & 0x07, min = 0x10000;
    } else {
        return -1;   /* 10xxxxxx 不能當開頭;F8–FF 不存在 */
    }
    if ((size_t)len > n) return -1;
    for (int k = 1; k < len; k++) {
        if ((s[k] & 0xC0) != 0x80) return -1;
        v = (v << 6) | (s[k] & 0x3F);
    }
    if (v < min || v > 0x10FFFF || is_surrogate(v)) return -1;   /* 過長、超出範圍、surrogate */
    *cp = v;
    return len;
}

long utf8_count(const uint8_t *s, size_t n) {
    long count = 0;
    size_t i = 0;
    while (i < n) {
        uint32_t cp;
        int k = utf8_decode(s + i, n - i, &cp);
        if (k < 0) return -1;
        i += (size_t)k;
        count++;
    }
    return count;
}

int ascii_toggle_case(int c) {
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) return c ^ 0x20;
    return c;
}
