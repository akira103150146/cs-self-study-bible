/* utf8.h — 任務 4(C3.5)文字。這個檔案已經寫好,不要改。 */
#ifndef UTF8_H
#define UTF8_H
#include <stddef.h>
#include <stdint.h>

int utf8_encode(uint32_t cp, uint8_t out[4]);
/* 回傳位元組數 1–4;surrogate(U+D800–U+DFFF)或超過 U+10FFFF → -1 */

int utf8_decode(const uint8_t *s, size_t n, uint32_t *cp);
/* 解出 s 開頭的第一個字元,回傳用掉的位元組數;
 * n = 0、開頭位元組不合法、序列不完整、延續位元組不是 10xxxxxx、過長編碼、surrogate、超過 U+10FFFF → -1 */

long utf8_count(const uint8_t *s, size_t n);   /* 有幾個碼位;任何一處不合法 → -1 */

int ascii_toggle_case(int c);                  /* ASCII 字母大小寫互換(用 XOR 0x20);其他字元原樣回傳 */
#endif
