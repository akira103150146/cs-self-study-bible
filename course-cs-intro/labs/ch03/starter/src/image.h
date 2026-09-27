/* image.h — 任務 7(C3.8)影像。這個檔案已經寫好,不要改。 */
#ifndef IMAGE_H
#define IMAGE_H
#include <stddef.h>
#include <stdint.h>

struct image {
    int w, h;
    uint8_t *rgb;   /* w × h × 3 位元組:列由上而下,每列由左而右,每個像素 R G B */
};

int bmp_read(const char *path, struct image *img);
/* 只收 24 位元、未壓縮的 BMP;高度為正(列由下而上)或為負(由上而下)都要支援;每列補齊到 4 的倍數。
 * 成功 0(img->rgb 用 malloc 配置);任何錯誤 → -1 */
int bmp_write(const char *path, const struct image *img);   /* 24 位元、由下而上、54 位元組檔頭 */
void image_free(struct image *img);

void to_gray(struct image *img);   /* Y = floor(0.299R + 0.587G + 0.114B + 0.5),R = G = B = Y */
void invert(struct image *img);    /* 每個通道 v → 255 − v */
uint64_t raw_image_bytes(int w, int h, int bpp);

int palette_index(const struct image *img, const uint8_t (*pal)[3], int n, uint8_t *idx);
/* 每個像素找歐氏距離最近的調色盤顏色(同距離取編號小的),寫進 idx[w × h];n < 1 → -1,成功 0 */

int svg_rect(char *buf, size_t cap, int x, int y, int w, int h, uint32_t rgb);
/* 寫出 <rect x="10" y="20" width="30" height="40" fill="#ff8800"/>(小寫十六進位),回傳長度;cap 不夠 → -1 */
#endif
