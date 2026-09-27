/* base.c — 第 2 章 Lab 參考解。 */
#include "base.h"

#include <string.h>

/* ---------------- 任務 1 ---------------- */
int digit_value(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'z') return c - 'a' + 10;
    if (c >= 'A' && c <= 'Z') return c - 'A' + 10;
    return -1;
}

char digit_char(int v) {
    if (v >= 0 && v <= 9) return (char)('0' + v);
    if (v >= 10 && v <= 35) return (char)('a' + v - 10);
    return '?';
}

static int valid_base(int base) { return base >= 2 && base <= 36; }

/* s 的每個字元都是 base 進位的合法數字,且非空 */
static int valid_digits(const char *s, int base) {
    if (!s || !*s) return 0;
    for (; *s; s++) {
        int d = digit_value(*s);
        if (d < 0 || d >= base) return 0;
    }
    return 1;
}

/* ---------------- 任務 2 ---------------- */
int parse_base(const char *s, int base, uint64_t *out) {
    if (!valid_base(base) || !valid_digits(s, base)) return -1;
    uint64_t v = 0;
    for (; *s; s++) {
        uint64_t d = (uint64_t)digit_value(*s);
        if (v > (UINT64_MAX - d) / (uint64_t)base) return -2;   /* v * base + d 會超過 64 位元 */
        v = v * (uint64_t)base + d;                              /* Horner 法 */
    }
    *out = v;
    return 0;
}

/* ---------------- 任務 3 ---------------- */
int to_base(uint64_t v, int base, char *buf, size_t cap) {
    if (!valid_base(base)) return -1;
    char tmp[65];
    int n = 0;
    do {                                   /* 連除取餘數:先得到的是最低位 */
        tmp[n++] = digit_char((int)(v % (uint64_t)base));
        v /= (uint64_t)base;
    } while (v > 0);
    if ((size_t)n + 1 > cap) return -1;
    for (int i = 0; i < n; i++) buf[i] = tmp[n - 1 - i];   /* 由下往上讀 */
    buf[n] = '\0';
    return n;
}

int frac_to_base(double x, int base, int max_digits, char *buf, size_t cap) {
    if (!valid_base(base) || !(x >= 0.0 && x < 1.0) || max_digits < 1 || cap < 4) return -1;
    size_t n = 0;
    buf[n++] = '0';
    buf[n++] = '.';
    int produced = 0;
    do {                                   /* 連乘取整數部分 */
        if (n + 1 >= cap) return -1;
        x *= base;
        int d = (int)x;
        x -= d;
        buf[n++] = digit_char(d);
        produced++;
    } while (x > 0.0 && produced < max_digits);
    buf[n] = '\0';
    return 0;
}

/* ---------------- 任務 4 ---------------- */

/* 去掉前導零後的起點(全部是零時留一個 '0') */
static const char *skip_zeros(const char *s) {
    while (s[0] == '0' && s[1] != '\0') s++;
    return s;
}

/* 把倒著放的數字陣列 rev[0..n-1](rev[0] 是最低位)寫成字串,去掉前導零 */
static int emit(const int *rev, int n, char *out, size_t cap) {
    while (n > 1 && rev[n - 1] == 0) n--;
    if ((size_t)n + 1 > cap) return -1;
    for (int i = 0; i < n; i++) out[i] = digit_char(rev[n - 1 - i]);
    out[n] = '\0';
    return n;
}

/* 比較兩個(已去前導零的)數字字串的大小 */
static int cmp_digits(const char *a, const char *b) {
    size_t la = strlen(a), lb = strlen(b);
    if (la != lb) return la < lb ? -1 : 1;
    for (size_t i = 0; i < la; i++) {
        int da = digit_value(a[i]), db = digit_value(b[i]);
        if (da != db) return da < db ? -1 : 1;
    }
    return 0;
}

#define MAXD 4096

int add_in_base(const char *a, const char *b, int base, char *out, size_t cap) {
    if (!valid_base(base) || !valid_digits(a, base) || !valid_digits(b, base)) return -1;
    int la = (int)strlen(a), lb = (int)strlen(b), n = (la > lb ? la : lb) + 1;
    if (n > MAXD) return -1;
    int rev[MAXD], carry = 0;
    for (int i = 0; i < n; i++) {
        int da = i < la ? digit_value(a[la - 1 - i]) : 0;
        int db = i < lb ? digit_value(b[lb - 1 - i]) : 0;
        int s = da + db + carry;
        rev[i] = s % base;
        carry = s / base;
    }
    return emit(rev, n, out, cap);
}

int sub_in_base(const char *a, const char *b, int base, char *out, size_t cap) {
    if (!valid_base(base) || !valid_digits(a, base) || !valid_digits(b, base)) return -1;
    a = skip_zeros(a);
    b = skip_zeros(b);
    if (cmp_digits(a, b) < 0) return -1;
    int la = (int)strlen(a), lb = (int)strlen(b);
    if (la > MAXD) return -1;
    int rev[MAXD], borrow = 0;
    for (int i = 0; i < la; i++) {
        int d = digit_value(a[la - 1 - i]) - borrow - (i < lb ? digit_value(b[lb - 1 - i]) : 0);
        borrow = d < 0;
        rev[i] = d < 0 ? d + base : d;
    }
    return emit(rev, la, out, cap);
}

int mul_in_base(const char *a, const char *b, int base, char *out, size_t cap) {
    if (!valid_base(base) || !valid_digits(a, base) || !valid_digits(b, base)) return -1;
    int la = (int)strlen(a), lb = (int)strlen(b), n = la + lb;
    if (n > MAXD) return -1;
    int rev[MAXD] = {0};
    for (int i = 0; i < la; i++) {         /* 直式乘法:a 的第 i 位乘上 b 的每一位,加到對應的位置 */
        int da = digit_value(a[la - 1 - i]), carry = 0;
        for (int j = 0; j < lb; j++) {
            int t = rev[i + j] + da * digit_value(b[lb - 1 - j]) + carry;
            rev[i + j] = t % base;
            carry = t / base;
        }
        for (int k = i + lb; carry; k++) {
            int t = rev[k] + carry;
            rev[k] = t % base;
            carry = t / base;
        }
    }
    return emit(rev, n, out, cap);
}

/* ---------------- 任務 5 ---------------- */
int regroup(const char *bin, int k, char *out, size_t cap) {
    if (k < 1 || k > 5 || !valid_digits(bin, 2)) return -1;
    int len = (int)strlen(bin), groups = (len + k - 1) / k;
    if (groups > MAXD) return -1;
    int rev[MAXD];
    for (int g = 0; g < groups; g++) {     /* 第 g 組 = 從右邊數來第 g*k 到 g*k+k-1 位 */
        int v = 0;
        for (int b = k - 1; b >= 0; b--) {
            int pos = len - 1 - (g * k + b);
            v = v * 2 + (pos >= 0 ? bin[pos] - '0' : 0);   /* 左邊不足補零 */
        }
        rev[g] = v;
    }
    return emit(rev, groups, out, cap);
}

/* ---------------- 任務 6 ---------------- */
int bits_needed(uint64_t n) {
    int bits = 1;
    while (n >>= 1) bits++;
    return bits;
}

uint64_t max_unsigned(int bits) {
    if (bits < 1 || bits > 64) return 0;
    return bits == 64 ? UINT64_MAX : ((uint64_t)1 << bits) - 1;   /* 1 << 64 是未定義行為 */
}
