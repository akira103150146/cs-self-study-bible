/* 任務 1 參考解(C3.1)。 */
#include "digital.h"

#include <math.h>

int bits_for_items(uint64_t k) {
    /* 找最小的 n 使 2^n ≥ k,也就是 k − 1 需要幾個位元(k = 1 時算 1) */
    if (k <= 2) return 1;
    uint64_t m = k - 1;
    int n = 0;
    while (m) {
        n++;
        m >>= 1;
    }
    return n;
}

int digitize(double v, double vmax, int bits) {
    int top = (1 << bits) - 1;
    int level = (int)floor(v / vmax * top + 0.5);
    if (level < 0) return 0;
    if (level > top) return top;
    return level;
}
