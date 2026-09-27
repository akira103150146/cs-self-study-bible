/* video.h — 任務 8(C3.9)影片。這個檔案已經寫好,不要改。 */
#ifndef VIDEO_H
#define VIDEO_H
#include <stddef.h>
#include <stdint.h>

long delta_encode(const uint8_t *prev, const uint8_t *cur, size_t n, uint8_t *out, size_t cap);
/* 把 cur 相對於 prev 改變的地方編成一串區段:(起點 u32 LE)(長度 u16 LE)(新的位元組 × 長度)。
 * 每個區段是一段「連續改變」的位元組,長度最多 65535(更長就切開)。完全相同 → 0。cap 不夠 → -1 */

long delta_decode(const uint8_t *prev, const uint8_t *delta, size_t dn, uint8_t *cur, size_t n);
/* 先把 prev 複製到 cur,再套用 delta。成功 0;區段超出 n 或資料不完整 → -1 */

double compression_ratio(uint64_t original, uint64_t compressed);   /* compressed / original;original = 0 → 0 */
#endif
