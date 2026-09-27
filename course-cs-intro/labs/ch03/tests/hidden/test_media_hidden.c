/* 第 3 章 Lab 隱藏測試:聲音、影像、影片的邊界情況。 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "audio.h"
#include "ctest.h"
#include "byteorder.h"
#include "image.h"
#include "video.h"

/* ---------------- C3.7 ---------------- */
TEST(C3_7_quantize_clamp) {
    ASSERT_EQ_INT(127, quantize(2.0, 8));
    ASSERT_EQ_INT(-127, quantize(-3.0, 8));
    ASSERT_EQ_INT(0, quantize(0.0, 16));
    ASSERT_EQ_INT(32767, quantize(1.0, 16));
}
TEST(C3_7_snr_8bit_matches_theory) {
    enum { N = 48000 };
    static double orig[N], approx[N];
    for (int i = 0; i < N; i++) {
        orig[i] = sin(2 * M_PI * 997.0 * i / 48000.0);
        approx[i] = quantize(orig[i], 8) / 127.0;
    }
    double snr = snr_db(orig, approx, N);
    ASSERT_NEAR(6.02 * 8 + 1.76, snr, 1.0);
    ASSERT_TRUE(isinf(snr_db(orig, orig, N)));
}
TEST(C3_7_alias_edges) {
    ASSERT_NEAR(23000.0, alias_freq(25000.0, 48000), 1e-9);
    ASSERT_NEAR(0.0, alias_freq(44100.0, 44100), 1e-9);
    ASSERT_NEAR(5900.0, alias_freq(50000.0, 44100), 1e-9);
    ASSERT_NEAR(22050.0, alias_freq(22050.0, 44100), 1e-9);
}
TEST(C3_7_pcm_bytes_fraction) {
    ASSERT_EQ_UINT(132300u, pcm_bytes(44100, 16, 1, 1.5));
    ASSERT_EQ_UINT(80000u, pcm_bytes(8000, 8, 1, 10.0));
}
TEST(C3_7_synth_range_and_cap) {
    static int32_t s[8000];
    size_t n = synth_sine(100.0, 8000, 1.0, 8, s, 8000);
    ASSERT_EQ_UINT(8000, n);
    int crossings = 0;
    for (size_t i = 0; i < n; i++) {
        ASSERT_TRUE(s[i] >= -127 && s[i] <= 127);
        if (i && (s[i - 1] < 0) != (s[i] < 0)) crossings++;
    }
    ASSERT_TRUE(crossings >= 198 && crossings <= 202);   /* 100 Hz 一秒約 200 次過零 */
    ASSERT_EQ_UINT(0, synth_sine(100.0, 8000, 1.0, 8, s, 10));
}
TEST(C3_7_wav_header_16bit) {
    int32_t s[4] = {0, 1000, -1000, 32767};
    ASSERT_EQ_INT(0, wav_write("build/t16.wav", s, 4, 22050, 16));
    FILE *f = fopen("build/t16.wav", "rb");
    uint8_t h[52];
    ASSERT_EQ_INT(52, (long)fread(h, 1, 52, f));
    fclose(f);
    ASSERT_EQ_MEM("RIFF", h, 4);
    ASSERT_EQ_UINT(36 + 8, read_le32(h + 4));
    ASSERT_EQ_MEM("WAVEfmt ", h + 8, 8);
    ASSERT_EQ_UINT(16, read_le32(h + 16));
    ASSERT_EQ_INT(1, h[20] | h[21] << 8);            /* PCM */
    ASSERT_EQ_INT(1, h[22] | h[23] << 8);            /* mono */
    ASSERT_EQ_UINT(22050, read_le32(h + 24));
    ASSERT_EQ_UINT(44100, read_le32(h + 28));        /* byte rate */
    ASSERT_EQ_INT(2, h[32] | h[33] << 8);            /* block align */
    ASSERT_EQ_INT(16, h[34] | h[35] << 8);
    ASSERT_EQ_MEM("data", h + 36, 4);
    ASSERT_EQ_UINT(8, read_le32(h + 40));
    ASSERT_EQ_INT(1000, (int16_t)(h[46] | h[47] << 8));
    ASSERT_EQ_INT(-1000, (int16_t)(h[48] | h[49] << 8));
}
TEST(C3_7_wav_8bit_offset) {
    int32_t s[3] = {-127, 0, 127};
    ASSERT_EQ_INT(0, wav_write("build/t8.wav", s, 3, 8000, 8));
    FILE *f = fopen("build/t8.wav", "rb");
    uint8_t h[47];
    ASSERT_EQ_INT(47, (long)fread(h, 1, 47, f));
    fclose(f);
    ASSERT_EQ_INT(1, h[44]);
    ASSERT_EQ_INT(128, h[45]);
    ASSERT_EQ_INT(255, h[46]);
    ASSERT_EQ_INT(-1, wav_write("build/bad.wav", s, 3, 8000, 12));
}

/* ---------------- C3.8 ---------------- */
TEST(C3_8_read_known_file) {
    struct image img = {0, 0, NULL};
    ASSERT_EQ_INT(0, bmp_read("data/tiny3x2.bmp", &img));
    ASSERT_EQ_INT(3, img.w);
    ASSERT_EQ_INT(2, img.h);
    const uint8_t top_left[3] = {255, 0, 0}, bottom_right[3] = {255, 255, 255};
    ASSERT_EQ_MEM(top_left, img.rgb, 3);                 /* 第一列是最上面那一列 */
    ASSERT_EQ_MEM(bottom_right, img.rgb + (1 * 3 + 2) * 3, 3);
    image_free(&img);
}
TEST(C3_8_read_top_down_file) {
    struct image a = {0, 0, NULL}, b = {0, 0, NULL};
    ASSERT_EQ_INT(0, bmp_read("data/tiny3x2.bmp", &a));
    ASSERT_EQ_INT(0, bmp_read("data/topdown3x2.bmp", &b));   /* 高度為負的 BMP:列由上而下 */
    ASSERT_EQ_MEM(a.rgb, b.rgb, 18);
    image_free(&a), image_free(&b);
}
TEST(C3_8_padding_101_wide) {
    struct image img = {0, 0, NULL};
    ASSERT_EQ_INT(0, bmp_read("data/gradient.bmp", &img));
    ASSERT_EQ_INT(101, img.w);
    ASSERT_EQ_INT(50, img.h);
    for (int y = 0; y < 50; y++)
        for (int x = 0; x < 101; x++) {
            const uint8_t *p = img.rgb + (y * 101 + x) * 3;
            ASSERT_TRUE(p[0] == (uint8_t)(x * 2) && p[1] == (uint8_t)(y * 5) && p[2] == 128);
        }
    ASSERT_EQ_INT(0, bmp_write("build/g.bmp", &img));
    FILE *f = fopen("build/g.bmp", "rb");
    fseek(f, 0, SEEK_END);
    ASSERT_EQ_INT(54 + 304 * 50, ftell(f));
    fclose(f);
    image_free(&img);
}
TEST(C3_8_read_rejects_bad_files) {
    struct image img = {0, 0, NULL};
    ASSERT_EQ_INT(-1, bmp_read("data/does-not-exist.bmp", &img));
    ASSERT_EQ_INT(-1, bmp_read("data/english.txt", &img));
    ASSERT_EQ_INT(-1, bmp_read("data/bpp32.bmp", &img));
    FILE *f = fopen("build/short.bmp", "wb");
    fwrite("BM\x10\x00", 1, 4, f);
    fclose(f);
    ASSERT_EQ_INT(-1, bmp_read("build/short.bmp", &img));
}
TEST(C3_8_palette_nearest) {
    const uint8_t pal[3][3] = {{0, 0, 0}, {255, 255, 255}, {255, 0, 0}};
    uint8_t px[9] = {200, 30, 30, 100, 100, 100, 250, 250, 240};
    struct image img = {3, 1, px};
    uint8_t idx[3];
    ASSERT_EQ_INT(0, palette_index(&img, pal, 3, idx));
    ASSERT_EQ_INT(2, idx[0]);
    ASSERT_EQ_INT(0, idx[1]);
    ASSERT_EQ_INT(1, idx[2]);
    ASSERT_EQ_INT(-1, palette_index(&img, pal, 0, idx));
}
TEST(C3_8_svg_rect_cap) {
    char buf[10];
    ASSERT_EQ_INT(-1, svg_rect(buf, sizeof buf, 1, 2, 3, 4, 0x000000));
    char big[128];
    svg_rect(big, sizeof big, 0, 0, 5, 5, 0x0A0B0C);
    ASSERT_EQ_STR("<rect x=\"0\" y=\"0\" width=\"5\" height=\"5\" fill=\"#0a0b0c\"/>", big);
}

/* ---------------- C3.9 ---------------- */
TEST(C3_9_runs_and_gaps) {
    uint8_t a[20] = {0}, b[20] = {0}, out[64];
    b[2] = 1, b[3] = 2, b[4] = 3;   /* 一段連續 3 個 */
    b[10] = 7;                      /* 另一段 1 個 */
    ASSERT_EQ_INT(6 + 3 + 6 + 1, delta_encode(a, b, 20, out, sizeof out));
    ASSERT_EQ_INT(-1, delta_encode(a, b, 20, out, 8));
}
TEST(C3_9_roundtrip_random_frames) {
    enum { N = 10000 };
    static uint8_t prev[N], cur[N], back[N], out[4 * N];
    srand(7);
    for (int i = 0; i < N; i++) prev[i] = cur[i] = (uint8_t)rand();
    for (int k = 0; k < 500; k++) cur[rand() % N] = (uint8_t)rand();
    long d = delta_encode(prev, cur, N, out, sizeof out);
    ASSERT_TRUE(d > 0 && d < N / 2);
    ASSERT_EQ_INT(0, delta_decode(prev, out, (size_t)d, back, N));
    ASSERT_EQ_MEM(cur, back, N);
}
TEST(C3_9_decode_rejects_bad_delta) {
    uint8_t prev[8] = {0}, cur[8];
    const uint8_t past_end[7] = {6, 0, 0, 0, 5, 0, 1};    /* 起點 6、長度 5 超出 8 */
    ASSERT_EQ_INT(-1, delta_decode(prev, past_end, 7, cur, 8));
    const uint8_t truncated[5] = {1, 0, 0, 0, 2};
    ASSERT_EQ_INT(-1, delta_decode(prev, truncated, 5, cur, 8));
    const uint8_t missing_bytes[7] = {1, 0, 0, 0, 3, 0, 9};   /* 說有 3 個位元組,只給 1 個 */
    ASSERT_EQ_INT(-1, delta_decode(prev, missing_bytes, 7, cur, 8));
}
TEST(C3_9_long_run_split) {
    enum { N = 70000 };
    static uint8_t a[N], b[N], out[N + 64], back[N];
    memset(b, 1, N);
    long d = delta_encode(a, b, N, out, sizeof out);
    ASSERT_EQ_INT(6 + 65535 + 6 + (N - 65535), d);   /* 超過 65535 要切成兩段 */
    ASSERT_EQ_INT(0, delta_decode(a, out, (size_t)d, back, N));
    ASSERT_EQ_MEM(b, back, N);
}
TEST(C3_9_ratio_zero_original) { ASSERT_NEAR(0.0, compression_ratio(0, 10), 0.0); }
