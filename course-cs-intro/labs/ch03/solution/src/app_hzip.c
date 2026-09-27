/* hzip — 用你的 Huffman 壓縮/解壓縮檔案(已經寫好,不要改)。
 *   hzip c 輸入檔 輸出檔     壓縮
 *   hzip d 輸入檔 輸出檔     解壓縮
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "compress.h"

static uint8_t *slurp(const char *path, size_t *n) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    uint8_t *buf = malloc((size_t)len + 1);
    *n = fread(buf, 1, (size_t)len, f);
    fclose(f);
    return buf;
}

int main(int argc, char **argv) {
    if (argc != 4 || (strcmp(argv[1], "c") != 0 && strcmp(argv[1], "d") != 0)) {
        fprintf(stderr, "usage: hzip c|d INPUT OUTPUT\n");
        return 2;
    }
    size_t n;
    uint8_t *in = slurp(argv[2], &n);
    if (!in) {
        perror(argv[2]);
        return 1;
    }
    size_t cap;
    if (argv[1][0] == 'c') cap = n * 2 + 1024;
    else cap = n >= 4 ? (size_t)in[0] | (size_t)in[1] << 8 | (size_t)in[2] << 16 | (size_t)in[3] << 24 : 0;
    uint8_t *out = malloc(cap + 1);
    long m = argv[1][0] == 'c' ? huff_compress(in, n, out, cap) : huff_decompress(in, n, out, cap);
    if (m < 0) {
        fprintf(stderr, "hzip: failed\n");
        return 1;
    }
    FILE *f = fopen(argv[3], "wb");
    if (!f) {
        perror(argv[3]);
        return 1;
    }
    fwrite(out, 1, (size_t)m, f);
    fclose(f);
    if (argv[1][0] == 'c') fprintf(stderr, "%zu -> %ld bytes (ratio %.3f)\n", n, m, n ? (double)m / (double)n : 0.0);
    free(in);
    free(out);
    return 0;
}
