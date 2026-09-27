/* floats.h — 任務 3(C3.4)IEEE 754 單精度。這個檔案已經寫好,不要改。 */
#ifndef FLOATS_H
#define FLOATS_H
#include <stddef.h>
#include <stdint.h>

enum fkind { F_ZERO, F_DENORMAL, F_NORMAL, F_INF, F_NAN };

struct f32info {
    int sign;          /* 0 或 1 */
    int exp_bits;      /* 指數欄位的值 0–255 */
    uint32_t frac;     /* 尾數欄位 23 位元 */
    int unbiased;      /* normal:exp_bits − 127;denormal:−126;其他:0 */
    enum fkind kind;
};

uint32_t f32_to_bits(float x);            /* 用 memcpy 取出 32 個位元 */
float f32_from_bits(uint32_t b);
struct f32info f32_decode(uint32_t b);
uint32_t f32_encode(int sign, int exp_bits, uint32_t frac);   /* 各欄位先遮罩到正確寬度 */

int f32_binary_sci(uint32_t b, char *out, size_t cap);
/* 寫成二進位科學記號,回傳長度;cap 不夠 → -1。格式:
 *   normal:  "-1.1001 x 2^2"(尾數去掉尾端的 0;全部是 0 時寫 "1.0";正數不加 "+")
 *   denormal:"0.00000000000000000000001 x 2^-126"(同樣去尾 0)
 *   零:"+0" / "-0";無限大:"+inf" / "-inf";NaN:"nan" */
#endif
