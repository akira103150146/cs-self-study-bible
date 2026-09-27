/* byteorder.h — 任務 9(C3.10)位元組順序。這個檔案已經寫好,不要改。 */
#ifndef BYTEORDER_H
#define BYTEORDER_H
#include <stdint.h>

int host_is_little(void);              /* 這台機器是小端序 → 1 */
uint32_t bswap32(uint32_t x);          /* 位元組順序顛倒 */
uint32_t read_le32(const uint8_t *p);  /* 用移位組合,不得用指標轉型 */
uint32_t read_be32(const uint8_t *p);
void write_le32(uint8_t *p, uint32_t x);
#endif
