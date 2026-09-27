/* 任務 7 參考解(C3.8)。 */
#include "image.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "byteorder.h"

static int row_bytes(int w) { return (w * 3 + 3) / 4 * 4; }   /* 每列補齊到 4 的倍數 */

int bmp_read(const char *path, struct image *img) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    uint8_t h[54];
    if (fread(h, 1, 54, f) != 54 || h[0] != 'B' || h[1] != 'M') {
        fclose(f);
        return -1;
    }
    uint32_t offset = read_le32(h + 10), dib = read_le32(h + 14);
    int32_t w = (int32_t)read_le32(h + 18), hh = (int32_t)read_le32(h + 22);
    int bpp = h[28] | h[29] << 8;
    uint32_t compression = read_le32(h + 30);
    if (dib < 40 || bpp != 24 || compression != 0 || w <= 0 || hh == 0 || w > 1 << 15 || hh > 1 << 15 ||
        hh < -(1 << 15)) {
        fclose(f);
        return -1;
    }
    int top_down = hh < 0, height = top_down ? -hh : hh, rb = row_bytes(w);
    uint8_t *rgb = malloc((size_t)w * (size_t)height * 3), *row = malloc((size_t)rb);
    if (!rgb || !row || fseek(f, (long)offset, SEEK_SET) != 0) {
        free(rgb), free(row), fclose(f);
        return -1;
    }
    for (int r = 0; r < height; r++) {
        if (fread(row, 1, (size_t)rb, f) != (size_t)rb) {
            free(rgb), free(row), fclose(f);
            return -1;
        }
        int y = top_down ? r : height - 1 - r;   /* 預設由下而上 */
        for (int x = 0; x < w; x++) {
            uint8_t *p = rgb + ((size_t)y * (size_t)w + (size_t)x) * 3;
            p[0] = row[x * 3 + 2], p[1] = row[x * 3 + 1], p[2] = row[x * 3];   /* 檔案裡是 B G R */
        }
    }
    free(row);
    fclose(f);
    img->w = w, img->h = height, img->rgb = rgb;
    return 0;
}

int bmp_write(const char *path, const struct image *img) {
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    int rb = row_bytes(img->w);
    uint32_t data = (uint32_t)rb * (uint32_t)img->h;
    uint8_t h[54] = {'B', 'M'};
    write_le32(h + 2, 54 + data);
    write_le32(h + 10, 54);
    write_le32(h + 14, 40);
    write_le32(h + 18, (uint32_t)img->w);
    write_le32(h + 22, (uint32_t)img->h);
    h[26] = 1;                     /* planes */
    h[28] = 24;                    /* bits per pixel */
    write_le32(h + 34, data);
    write_le32(h + 38, 2835);      /* 72 DPI */
    write_le32(h + 42, 2835);
    fwrite(h, 1, 54, f);
    uint8_t *row = calloc((size_t)rb, 1);
    for (int y = img->h - 1; y >= 0; y--) {
        for (int x = 0; x < img->w; x++) {
            const uint8_t *p = img->rgb + ((size_t)y * (size_t)img->w + (size_t)x) * 3;
            row[x * 3] = p[2], row[x * 3 + 1] = p[1], row[x * 3 + 2] = p[0];
        }
        fwrite(row, 1, (size_t)rb, f);
    }
    free(row);
    return fclose(f) == 0 ? 0 : -1;
}

void image_free(struct image *img) {
    free(img->rgb);
    img->rgb = NULL;
}

void to_gray(struct image *img) {
    size_t n = (size_t)img->w * (size_t)img->h;
    for (size_t i = 0; i < n; i++) {
        uint8_t *p = img->rgb + i * 3;
        uint8_t y = (uint8_t)floor(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] + 0.5);
        p[0] = p[1] = p[2] = y;
    }
}

void invert(struct image *img) {
    size_t n = (size_t)img->w * (size_t)img->h * 3;
    for (size_t i = 0; i < n; i++) img->rgb[i] = (uint8_t)(255 - img->rgb[i]);
}

uint64_t raw_image_bytes(int w, int h, int bpp) { return (uint64_t)w * (uint64_t)h * (uint64_t)bpp / 8; }

int palette_index(const struct image *img, const uint8_t (*pal)[3], int n, uint8_t *idx) {
    if (n < 1) return -1;
    size_t count = (size_t)img->w * (size_t)img->h;
    for (size_t i = 0; i < count; i++) {
        const uint8_t *p = img->rgb + i * 3;
        long best = -1;
        for (int k = 0; k < n; k++) {
            long d = 0;
            for (int c = 0; c < 3; c++) d += (long)(p[c] - pal[k][c]) * (p[c] - pal[k][c]);
            if (best < 0 || d < best) best = d, idx[i] = (uint8_t)k;   /* 同距離保留編號小的 */
        }
    }
    return 0;
}

int svg_rect(char *buf, size_t cap, int x, int y, int w, int h, uint32_t rgb) {
    int n = snprintf(buf, cap, "<rect x=\"%d\" y=\"%d\" width=\"%d\" height=\"%d\" fill=\"#%06x\"/>", x, y, w, h,
                     (unsigned)(rgb & 0xFFFFFF));
    return (n < 0 || (size_t)n >= cap) ? -1 : n;
}
