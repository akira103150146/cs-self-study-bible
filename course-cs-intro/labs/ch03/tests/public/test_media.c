/* 第 3 章 Lab 公開測試:聲音、影像、影片(任務 6、7、8)。 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "audio.h"
#include "ctest.h"
#include "image.h"
#include "video.h"

/* ---------------- 任務 6:聲音(C3.7) ---------------- */
TEST(C3_7_quantize_basic) {
    ASSERT_EQ_INT(127, quantize(1.0, 8));
    ASSERT_EQ_INT(-127, quantize(-1.0, 8));
    ASSERT_EQ_INT(64, quantize(0.5, 8));
}
TEST(C3_7_pcm_bytes_cd) { ASSERT_EQ_UINT(10584000u, pcm_bytes(44100, 16, 2, 60.0)); }
TEST(C3_7_alias_basic) {
    ASSERT_NEAR(14100.0, alias_freq(30000.0, 44100), 1e-9);
    ASSERT_NEAR(1000.0, alias_freq(1000.0, 44100), 1e-9);
}
TEST(C3_7_synth_count) {
    int32_t s[100];
    ASSERT_EQ_UINT(80, synth_sine(440.0, 8000, 0.01, 16, s, 100));
    ASSERT_EQ_INT(0, s[0]);
}

/* ---------------- 任務 7:影像(C3.8) ---------------- */
TEST(C3_8_raw_bytes) { ASSERT_EQ_UINT(6220800u, raw_image_bytes(1920, 1080, 24)); }
TEST(C3_8_gray_and_invert) {
    uint8_t px[3] = {200, 100, 50};
    struct image img = {1, 1, px};
    invert(&img);
    ASSERT_EQ_INT(55, px[0]);
    ASSERT_EQ_INT(155, px[1]);
    ASSERT_EQ_INT(205, px[2]);
    px[0] = 200, px[1] = 100, px[2] = 50;
    to_gray(&img);
    ASSERT_EQ_INT(124, px[0]);
    ASSERT_EQ_INT(124, px[2]);
}
TEST(C3_8_bmp_roundtrip) {
    uint8_t px[3 * 2 * 3];
    for (int i = 0; i < 18; i++) px[i] = (uint8_t)(i * 13);
    struct image img = {3, 2, px}, back = {0, 0, NULL};
    ASSERT_EQ_INT(0, bmp_write("build/rt.bmp", &img));
    ASSERT_EQ_INT(0, bmp_read("build/rt.bmp", &back));
    ASSERT_EQ_INT(3, back.w);
    ASSERT_EQ_INT(2, back.h);
    ASSERT_EQ_MEM(px, back.rgb, 18);
    image_free(&back);
}
TEST(C3_8_svg_rect) {
    char buf[128];
    ASSERT_TRUE(svg_rect(buf, sizeof buf, 10, 20, 30, 40, 0xFF8800) > 0);
    ASSERT_EQ_STR("<rect x=\"10\" y=\"20\" width=\"30\" height=\"40\" fill=\"#ff8800\"/>", buf);
}

/* ---------------- 任務 8:影片(C3.9) ---------------- */
TEST(C3_9_identical_frames) {
    uint8_t a[16] = {0}, out[64];
    ASSERT_EQ_INT(0, delta_encode(a, a, 16, out, sizeof out));
}
TEST(C3_9_one_pixel) {
    uint8_t a[16] = {0}, b[16] = {0}, out[64];
    b[5] = 9;
    ASSERT_EQ_INT(7, delta_encode(a, b, 16, out, sizeof out));
    const uint8_t want[7] = {5, 0, 0, 0, 1, 0, 9};
    ASSERT_EQ_MEM(want, out, 7);
}
TEST(C3_9_ratio) { ASSERT_NEAR(0.235, compression_ratio(10000, 2350), 1e-12); }
