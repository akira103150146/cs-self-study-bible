/* 任務 9 參考解(C3.10)。 */
#include "byteorder.h"

#include <string.h>

int host_is_little(void) {
    uint32_t one = 1;
    uint8_t first;
    memcpy(&first, &one, 1);   /* 整數 1 的第一個位元組是 1 → 低位放在低位址 */
    return first == 1;
}

uint32_t bswap32(uint32_t x) {
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) | ((x << 8) & 0x00FF0000u) | (x << 24);
}

uint32_t read_le32(const uint8_t *p) {
    return (uint32_t)p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24;
}

uint32_t read_be32(const uint8_t *p) {
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | (uint32_t)p[3];
}

void write_le32(uint8_t *p, uint32_t x) {
    for (int k = 0; k < 4; k++) p[k] = (uint8_t)(x >> (8 * k));
}
