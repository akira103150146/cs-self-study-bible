#include "image.h"

#include <stdio.h>
#include <stdlib.h>

int bmp_read(const char *path, struct image *img) {
    (void)path, (void)img;
    return -1; /* TODO */
}

int bmp_write(const char *path, const struct image *img) {
    (void)path, (void)img;
    return -1; /* TODO */
}

void image_free(struct image *img) {
    free(img->rgb);
    img->rgb = NULL;
}

void to_gray(struct image *img) {
    (void)img; /* TODO */
}

void invert(struct image *img) {
    (void)img; /* TODO */
}

uint64_t raw_image_bytes(int w, int h, int bpp) {
    (void)w, (void)h, (void)bpp;
    return 0; /* TODO */
}

int palette_index(const struct image *img, const uint8_t (*pal)[3], int n, uint8_t *idx) {
    (void)img, (void)pal, (void)n, (void)idx;
    return -1; /* TODO */
}

int svg_rect(char *buf, size_t cap, int x, int y, int w, int h, uint32_t rgb) {
    (void)buf, (void)cap, (void)x, (void)y, (void)w, (void)h, (void)rgb;
    return -1; /* TODO:snprintf */
}
