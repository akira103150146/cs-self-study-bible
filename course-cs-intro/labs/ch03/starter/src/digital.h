/* digital.h — 任務 1(C3.1)類比與數位。這個檔案已經寫好,不要改。 */
#ifndef DIGITAL_H
#define DIGITAL_H
#include <stdint.h>

int bits_for_items(uint64_t k);
/* 要給 k(≥ 1)樣東西各一個不同的位元樣子,至少要幾個位元;k = 1 → 1 */

int digitize(double v, double vmax, int bits);
/* 把 0..vmax 均分成 2^bits 級(第 0 級 = 0、最高級 = vmax),回傳 v 最接近的等級:
 * floor(v / vmax * (2^bits − 1) + 0.5),超出範圍的夾到 0 或最高級。1 ≤ bits ≤ 30 */
#endif
