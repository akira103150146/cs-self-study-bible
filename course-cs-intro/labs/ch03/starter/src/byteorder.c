#include "byteorder.h"

int host_is_little(void) {
    return -1; /* TODO */
}

uint32_t bswap32(uint32_t x) {
    (void)x;
    return 0; /* TODO */
}

uint32_t read_le32(const uint8_t *p) {
    (void)p;
    return 0; /* TODO:用移位組合 */
}

uint32_t read_be32(const uint8_t *p) {
    (void)p;
    return 0; /* TODO */
}

void write_le32(uint8_t *p, uint32_t x) {
    (void)p, (void)x; /* TODO */
}
