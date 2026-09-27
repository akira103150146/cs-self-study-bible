/* floatdump — 拆解一個 float(已經寫好,不要改)。用法:floatdump -6.25 */
#include <stdio.h>
#include <stdlib.h>

#include "floats.h"

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: floatdump NUMBER   (e.g. floatdump -6.25, floatdump inf, floatdump nan)\n");
        return 2;
    }
    float x = strtof(argv[1], NULL);
    uint32_t b = f32_to_bits(x);
    struct f32info i = f32_decode(b);
    static const char *kinds[] = {"zero", "denormal", "normal", "inf", "nan"};
    char sci[80];
    if (f32_binary_sci(b, sci, sizeof sci) < 0) sci[0] = '\0';
    printf("value    %.9g\n", (double)x);
    printf("bits     %u ", (unsigned)(b >> 31));
    for (int k = 30; k >= 23; k--) putchar('0' + (int)((b >> k) & 1));
    putchar(' ');
    for (int k = 22; k >= 0; k--) putchar('0' + (int)((b >> k) & 1));
    printf("\nhex      0x%08X\n", (unsigned)b);
    printf("kind     %s\n", (i.kind >= F_ZERO && i.kind <= F_NAN) ? kinds[i.kind] : "?");
    printf("exponent field %d, unbiased %d\n", i.exp_bits, i.unbiased);
    printf("binary   %s\n", sci);
    return 0;
}
