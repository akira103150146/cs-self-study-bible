#include "compress.h"

#include <string.h>

long keyword_encode(const char *in, const struct keyword *kw, size_t nkw, char *out, size_t cap) {
    (void)in, (void)kw, (void)nkw, (void)out, (void)cap;
    return -1; /* TODO */
}

long rle_encode(const char *in, char *out, size_t cap) {
    (void)in, (void)out, (void)cap;
    return -1; /* TODO */
}

long rle_decode(const char *in, char *out, size_t cap) {
    (void)in, (void)out, (void)cap;
    return -1; /* TODO */
}

int huff_code_lengths(const uint64_t freq[256], uint8_t len[256]) {
    (void)freq;
    memset(len, 0, 256); /* TODO:每次合併頻率最小的兩個節點 */
    return 0;
}

uint64_t huff_total_bits(const uint64_t freq[256], const uint8_t len[256]) {
    (void)freq, (void)len;
    return 0; /* TODO */
}

long huff_compress(const uint8_t *in, size_t n, uint8_t *out, size_t cap) {
    (void)in, (void)n, (void)out, (void)cap;
    return -1; /* TODO */
}

long huff_decompress(const uint8_t *in, size_t n, uint8_t *out, size_t cap) {
    (void)in, (void)n, (void)out, (void)cap;
    return -1; /* TODO */
}
