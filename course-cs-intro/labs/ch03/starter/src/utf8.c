#include "utf8.h"

int utf8_encode(uint32_t cp, uint8_t out[4]) {
    (void)cp, (void)out;
    return -1; /* TODO */
}

int utf8_decode(const uint8_t *s, size_t n, uint32_t *cp) {
    (void)s, (void)n, (void)cp;
    return -1; /* TODO */
}

long utf8_count(const uint8_t *s, size_t n) {
    (void)s, (void)n;
    return -1; /* TODO */
}

int ascii_toggle_case(int c) {
    return c; /* TODO */
}
