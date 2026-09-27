/* base.h — 第 2 章 Lab「baseconv」的介面。這個檔案已經寫好,不要改。
 *
 * 限制:src/base.c 不能使用 strtol、strtoul、strtoull、sscanf 與 printf 家族(make 會檢查)。
 * 所有的轉換都要自己用位值記數的方法做出來。
 */
#ifndef BASE_H
#define BASE_H
#include <stddef.h>
#include <stdint.h>

/* 任務 1(C2.1)數字與位值 */
int digit_value(char c);          /* '0'–'9'、'a'–'z'、'A'–'Z' → 0–35;其他字元 → -1 */
char digit_char(int v);           /* 0–35 → '0'–'9'、'a'–'z';超出範圍 → '?' */

/* 任務 2(C2.2)轉成十進位 */
int parse_base(const char *s, int base, uint64_t *out);
/* 0 成功;-1 基底不在 2–36、字串是空的、或有不屬於該基底的字元;-2 超過 64 位元能表示的範圍 */

/* 任務 3(C2.3)從十進位轉出去 */
int to_base(uint64_t v, int base, char *buf, size_t cap);
/* 寫入以 '\0' 結尾的字串,回傳長度(不含 '\0');cap 不夠或基底錯 → -1 */
int frac_to_base(double x, int base, int max_digits, char *buf, size_t cap);
/* 0 ≤ x < 1 → "0.xxx",最多 max_digits 位;剩下的小數變成 0 就提前結束;x = 0 → "0.0"。
 * 成功回傳 0;x 不在 [0, 1)、基底錯、max_digits < 1、或 cap 不夠 → -1 */

/* 任務 4(C2.4)各進位的四則運算:直接在數字字串上做直式運算,不得先轉成整數 */
int add_in_base(const char *a, const char *b, int base, char *out, size_t cap);
int sub_in_base(const char *a, const char *b, int base, char *out, size_t cap);   /* a < b → -1 */
int mul_in_base(const char *a, const char *b, int base, char *out, size_t cap);
/* 結果去掉前導零(結果為零時是 "0"),回傳長度;有不合法的數字、基底錯、或 cap 不夠 → -1 */

/* 任務 5(C2.5)2 的冪次進位 */
int regroup(const char *bin, int k, char *out, size_t cap);
/* 二進位字串 → 基底 2^k(k = 1–5):從右邊每 k 位一組,左邊不足補零;結果去掉前導零。
 * 必須靠分組完成,不得先轉成整數(字串可能很長)。回傳長度;錯誤 → -1 */

/* 任務 6(C2.6)位元與範圍 */
int bits_needed(uint64_t n);      /* 用二進位表示 n 至少要幾位;n = 0 → 1 */
uint64_t max_unsigned(int bits);  /* 1 ≤ bits ≤ 64 → 2^bits − 1;超出範圍 → 0 */

#endif
