#include "ints.h"

int to_signmag(int64_t v, int bits, char *out) {
    (void)v, (void)bits, (void)out;
    return -1; /* TODO */
}

int to_ones(int64_t v, int bits, char *out) {
    (void)v, (void)bits, (void)out;
    return -1; /* TODO */
}

int to_twos(int64_t v, int bits, char *out) {
    (void)v, (void)bits, (void)out;
    return -1; /* TODO:反轉加一,或直接取 v 的低 bits 位 */
}

int64_t from_twos(const char *s) {
    (void)s;
    return 0; /* TODO */
}

int64_t sign_extend(uint64_t raw, int bits) {
    (void)raw, (void)bits;
    return 0; /* TODO */
}

int add_overflows(int64_t a, int64_t b, int bits) {
    (void)a, (void)b, (void)bits;
    return 0; /* TODO:同號相加得異號 */
}

int64_t wrap_add(int64_t a, int64_t b, int bits) {
    (void)a, (void)b, (void)bits;
    return 0; /* TODO:注意 C 的有號溢位是未定義行為,先轉成無號再加 */
}
