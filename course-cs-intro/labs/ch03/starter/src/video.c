#include "video.h"

long delta_encode(const uint8_t *prev, const uint8_t *cur, size_t n, uint8_t *out, size_t cap) {
    (void)prev, (void)cur, (void)n, (void)out, (void)cap;
    return -1; /* TODO */
}

long delta_decode(const uint8_t *prev, const uint8_t *delta, size_t dn, uint8_t *cur, size_t n) {
    (void)prev, (void)delta, (void)dn, (void)cur, (void)n;
    return -1; /* TODO */
}

double compression_ratio(uint64_t original, uint64_t compressed) {
    (void)original, (void)compressed;
    return -1.0; /* TODO */
}
