/* ints.h — 任務 2(C3.2 負數、C3.3 溢位)。這個檔案已經寫好,不要改。 */
#ifndef INTS_H
#define INTS_H
#include <stdint.h>

/* 把 v 寫成 bits 位元(2 ≤ bits ≤ 64)的 '0'/'1' 字串(out 至少 bits + 1 個位元組)。
 * 成功回傳 0;bits 不合法或 v 超出該表示法的範圍 → -1 */
int to_signmag(int64_t v, int bits, char *out);   /* 範圍 ±(2^(bits−1) − 1) */
int to_ones(int64_t v, int bits, char *out);      /* 範圍 ±(2^(bits−1) − 1) */
int to_twos(int64_t v, int bits, char *out);      /* 範圍 −2^(bits−1) .. 2^(bits−1) − 1 */

int64_t from_twos(const char *s);                 /* 長度 1–64 的 '0'/'1' 字串 → 二補數的值 */
int64_t sign_extend(uint64_t raw, int bits);      /* 取 raw 的低 bits 位(1–64)當二補數,延伸成 64 位元 */

int add_overflows(int64_t a, int64_t b, int bits);
/* a、b 都在 bits 位元二補數的範圍內;a + b 超出範圍 → 1,否則 0 */
int64_t wrap_add(int64_t a, int64_t b, int bits);
/* bits 位元二補數加法「繞回」之後的結果 */
#endif
