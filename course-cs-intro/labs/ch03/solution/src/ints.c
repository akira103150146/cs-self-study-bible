/* 任務 2 參考解(C3.2 負數、C3.3 溢位)。
 * 原則:需要「繞回」的運算一律先轉成 uint64_t 再做——C 的有號溢位是未定義行為,無號才保證繞回。 */
#include "ints.h"

/* bits 位元二補數的範圍 */
static int64_t tmin(int bits) { return bits == 64 ? INT64_MIN : -((int64_t)1 << (bits - 1)); }
static int64_t tmax(int bits) { return bits == 64 ? INT64_MAX : ((int64_t)1 << (bits - 1)) - 1; }

/* 把 x 的低 bits 位寫成字串 */
static void write_bits(uint64_t x, int bits, char *out) {
    for (int i = 0; i < bits; i++) out[i] = (char)('0' + (int)((x >> (bits - 1 - i)) & 1));
    out[bits] = '\0';
}

int to_signmag(int64_t v, int bits, char *out) {
    if (bits < 2 || bits > 64 || v < -tmax(bits) || v > tmax(bits)) return -1;
    uint64_t mag = v < 0 ? (uint64_t)(-v) : (uint64_t)v;   /* v ≥ -tmax,取負不會溢位 */
    write_bits(mag | (v < 0 ? (uint64_t)1 << (bits - 1) : 0), bits, out);
    return 0;
}

int to_ones(int64_t v, int bits, char *out) {
    if (bits < 2 || bits > 64 || v < -tmax(bits) || v > tmax(bits)) return -1;
    uint64_t x = v < 0 ? ~(uint64_t)(-v) : (uint64_t)v;   /* 負數 = 絕對值逐位元反轉 */
    write_bits(x, bits, out);
    return 0;
}

int to_twos(int64_t v, int bits, char *out) {
    if (bits < 2 || bits > 64 || v < tmin(bits) || v > tmax(bits)) return -1;
    write_bits((uint64_t)v, bits, out);   /* 轉成 uint64_t 就是模 2^64 的值,低 bits 位正是二補數 */
    return 0;
}

int64_t sign_extend(uint64_t raw, int bits) {
    if (bits < 64) {
        raw &= ((uint64_t)1 << bits) - 1;
        if (raw >> (bits - 1)) raw |= ~(((uint64_t)1 << bits) - 1);   /* 符號位是 1:高位全部補 1 */
    }
    int64_t r;
    __builtin_memcpy(&r, &raw, sizeof r);   /* 位元樣子原封不動地當成有號數解讀 */
    return r;
}

int64_t from_twos(const char *s) {
    uint64_t x = 0;
    int bits = 0;
    for (; *s; s++, bits++) x = (x << 1) | (uint64_t)(*s - '0');
    return sign_extend(x, bits);
}

int add_overflows(int64_t a, int64_t b, int bits) {
    int64_t s = wrap_add(a, b, bits);
    return (a >= 0) == (b >= 0) && (s >= 0) != (a >= 0);   /* 同號相加得異號 */
}

int64_t wrap_add(int64_t a, int64_t b, int bits) {
    return sign_extend((uint64_t)a + (uint64_t)b, bits);
}
