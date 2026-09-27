/* base.c — 第 2 章 Lab。把每個 TODO 換成你的實作,讓 make test 全部通過。
 * 不能用 strtol、strtoul、strtoull、sscanf 與 printf 家族。
 */
#include "base.h"

/* ---------------- 任務 1 ---------------- */
int digit_value(char c) {
    (void)c;
    return -1; /* TODO */
}

char digit_char(int v) {
    (void)v;
    return '?'; /* TODO */
}

/* ---------------- 任務 2 ---------------- */
int parse_base(const char *s, int base, uint64_t *out) {
    (void)s, (void)base, (void)out;
    return -1; /* TODO:用 Horner 法,每讀一位 v = v * base + d;注意溢位 */
}

/* ---------------- 任務 3 ---------------- */
int to_base(uint64_t v, int base, char *buf, size_t cap) {
    (void)v, (void)base, (void)buf, (void)cap;
    return -1; /* TODO:連除取餘數,餘數由下往上讀 */
}

int frac_to_base(double x, int base, int max_digits, char *buf, size_t cap) {
    (void)x, (void)base, (void)max_digits, (void)buf, (void)cap;
    return -1; /* TODO:連乘取整數部分 */
}

/* ---------------- 任務 4 ---------------- */
int add_in_base(const char *a, const char *b, int base, char *out, size_t cap) {
    (void)a, (void)b, (void)base, (void)out, (void)cap;
    return -1; /* TODO:從最右邊一位開始相加,記得進位 */
}

int sub_in_base(const char *a, const char *b, int base, char *out, size_t cap) {
    (void)a, (void)b, (void)base, (void)out, (void)cap;
    return -1; /* TODO:從最右邊一位開始相減,記得借位 */
}

int mul_in_base(const char *a, const char *b, int base, char *out, size_t cap) {
    (void)a, (void)b, (void)base, (void)out, (void)cap;
    return -1; /* TODO:直式乘法 */
}

/* ---------------- 任務 5 ---------------- */
int regroup(const char *bin, int k, char *out, size_t cap) {
    (void)bin, (void)k, (void)out, (void)cap;
    return -1; /* TODO:從右邊每 k 位一組 */
}

/* ---------------- 任務 6 ---------------- */
int bits_needed(uint64_t n) {
    (void)n;
    return 0; /* TODO */
}

uint64_t max_unsigned(int bits) {
    (void)bits;
    return 0; /* TODO */
}
