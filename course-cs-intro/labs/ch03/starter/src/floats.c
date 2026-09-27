#include "floats.h"

#include <string.h>

uint32_t f32_to_bits(float x) {
    (void)x;
    return 0; /* TODO:用 memcpy */
}

float f32_from_bits(uint32_t b) {
    (void)b;
    return 0.0f; /* TODO */
}

struct f32info f32_decode(uint32_t b) {
    struct f32info i = {0, 0, 0, 0, F_ZERO};
    (void)b; /* TODO */
    return i;
}

uint32_t f32_encode(int sign, int exp_bits, uint32_t frac) {
    (void)sign, (void)exp_bits, (void)frac;
    return 0; /* TODO */
}

int f32_binary_sci(uint32_t b, char *out, size_t cap) {
    (void)b, (void)out, (void)cap;
    return -1; /* TODO */
}
