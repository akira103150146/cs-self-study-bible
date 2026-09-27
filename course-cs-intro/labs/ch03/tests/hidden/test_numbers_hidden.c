/* 第 3 章 Lab 隱藏測試:數字的邊界情況。 */
#include <stdio.h>
#include <string.h>

#include "ctest.h"
#include "digital.h"
#include "byteorder.h"
#include "floats.h"
#include "ints.h"

/* ---------------- C3.1 ---------------- */
TEST(C3_1_bits_for_items_edges) {
    ASSERT_EQ_INT(1, bits_for_items(1));
    ASSERT_EQ_INT(1, bits_for_items(2));
    ASSERT_EQ_INT(2, bits_for_items(3));
    ASSERT_EQ_INT(8, bits_for_items(256));
    ASSERT_EQ_INT(9, bits_for_items(257));
    ASSERT_EQ_INT(64, bits_for_items(UINT64_MAX));
}
TEST(C3_1_digitize_clamp_and_full_scale) {
    ASSERT_EQ_INT(0, digitize(-1.0, 5.0, 3));
    ASSERT_EQ_INT(7, digitize(6.0, 5.0, 3));
    ASSERT_EQ_INT(255, digitize(5.0, 5.0, 8));
    ASSERT_EQ_INT(0, digitize(0.0, 5.0, 8));
    ASSERT_EQ_INT(1, digitize(2.5, 5.0, 1));
}

/* ---------------- C3.2 ---------------- */
TEST(C3_2_range_limits_8bit) {
    char buf[80];
    ASSERT_EQ_INT(0, to_twos(127, 8, buf));
    ASSERT_EQ_STR("01111111", buf);
    ASSERT_EQ_INT(0, to_twos(-128, 8, buf));
    ASSERT_EQ_STR("10000000", buf);
    ASSERT_EQ_INT(-1, to_twos(128, 8, buf));
    ASSERT_EQ_INT(-1, to_twos(-129, 8, buf));
    ASSERT_EQ_INT(-1, to_ones(-128, 8, buf));
    ASSERT_EQ_INT(-1, to_signmag(-128, 8, buf));
    ASSERT_EQ_INT(0, to_signmag(0, 4, buf));
    ASSERT_EQ_STR("0000", buf);
}
TEST(C3_2_int64_extremes) {
    char buf[80], want[65];
    ASSERT_EQ_INT(0, to_twos(INT64_MIN, 64, buf));
    memset(want, '0', 64);
    want[0] = '1';
    want[64] = '\0';
    ASSERT_EQ_STR(want, buf);
    ASSERT_EQ_INT(0, to_twos(-1, 64, buf));
    memset(want, '1', 64);
    ASSERT_EQ_STR(want, buf);
    ASSERT_EQ_INT(-1, from_twos(want));
    ASSERT_EQ_INT(-1, to_twos(0, 65, buf));
    ASSERT_EQ_INT(-1, to_twos(0, 1, buf));
}
TEST(C3_2_from_twos_single_bit) {
    ASSERT_EQ_INT(0, from_twos("0"));
    ASSERT_EQ_INT(-1, from_twos("1"));
    ASSERT_EQ_INT(-32768, from_twos("1000000000000000"));
}
TEST(C3_2_sign_extend_ignores_high_bits) {
    ASSERT_EQ_INT(-128, sign_extend(0xFFFFFFFFFFFFFF80ull, 8));
    ASSERT_EQ_INT(-5, sign_extend(0xB, 4));
    ASSERT_EQ_INT(5, sign_extend(0xF5, 4));
    ASSERT_EQ_INT(INT64_MIN, sign_extend(0x8000000000000000ull, 64));
}

/* ---------------- C3.3 ---------------- */
TEST(C3_3_overflow_cases) {
    ASSERT_EQ_INT(1, add_overflows(-128, -1, 8));
    ASSERT_EQ_INT(0, add_overflows(100, -100, 8));
    ASSERT_EQ_INT(0, add_overflows(-128, 127, 8));
    ASSERT_EQ_INT(1, add_overflows(64, 64, 8));
    ASSERT_EQ_INT(0, add_overflows(63, 64, 8));
}
TEST(C3_3_overflow_64bit) {
    ASSERT_EQ_INT(1, add_overflows(INT64_MAX, 1, 64));
    ASSERT_EQ_INT(1, add_overflows(INT64_MIN, -1, 64));
    ASSERT_EQ_INT(0, add_overflows(INT64_MAX, INT64_MIN, 64));
}
TEST(C3_3_wrap_add_edges) {
    ASSERT_EQ_INT(-128, wrap_add(127, 1, 8));
    ASSERT_EQ_INT(127, wrap_add(-128, -1, 8));
    ASSERT_EQ_INT(INT64_MIN, wrap_add(INT64_MAX, 1, 64));
    ASSERT_EQ_INT(0, wrap_add(-128, -128, 8));
}

/* ---------------- C3.4 ---------------- */
TEST(C3_4_special_values) {
    struct f32info i;
    i = f32_decode(0x00000001u);
    ASSERT_EQ_INT(F_DENORMAL, i.kind);
    ASSERT_EQ_INT(-126, i.unbiased);
    ASSERT_EQ_UINT(1, i.frac);
    i = f32_decode(0x80000000u);
    ASSERT_EQ_INT(F_ZERO, i.kind);
    ASSERT_EQ_INT(1, i.sign);
    i = f32_decode(0xFF800000u);
    ASSERT_EQ_INT(F_INF, i.kind);
    ASSERT_EQ_INT(1, i.sign);
    i = f32_decode(0x7FC00000u);
    ASSERT_EQ_INT(F_NAN, i.kind);
    i = f32_decode(0x7F7FFFFFu);
    ASSERT_EQ_INT(F_NORMAL, i.kind);
    ASSERT_EQ_INT(127, i.unbiased);
    ASSERT_EQ_UINT(0x7FFFFFu, i.frac);
}
TEST(C3_4_encode_masks_fields) {
    ASSERT_EQ_UINT(0x7F800000u, f32_encode(0, 255, 0));
    ASSERT_EQ_UINT(0x80000000u, f32_encode(1, 0, 0));
    ASSERT_EQ_UINT(0x00000001u, f32_encode(0, 0, 1));
}
TEST(C3_4_binary_sci_forms) {
    char buf[80];
    f32_binary_sci(0x3F800000u, buf, sizeof buf);
    ASSERT_EQ_STR("1.0 x 2^0", buf);
    f32_binary_sci(0x3F400000u, buf, sizeof buf);
    ASSERT_EQ_STR("1.1 x 2^-1", buf);
    f32_binary_sci(0x00000001u, buf, sizeof buf);
    ASSERT_EQ_STR("0.00000000000000000000001 x 2^-126", buf);
    f32_binary_sci(0x80000000u, buf, sizeof buf);
    ASSERT_EQ_STR("-0", buf);
    f32_binary_sci(0x00000000u, buf, sizeof buf);
    ASSERT_EQ_STR("+0", buf);
    f32_binary_sci(0xFF800000u, buf, sizeof buf);
    ASSERT_EQ_STR("-inf", buf);
    f32_binary_sci(0x7FC00000u, buf, sizeof buf);
    ASSERT_EQ_STR("nan", buf);
}
TEST(C3_4_binary_sci_cap) {
    char buf[5];
    ASSERT_EQ_INT(-1, f32_binary_sci(0xC0C80000u, buf, sizeof buf));
}
TEST(C3_4_floatdump_cli) {
    FILE *p = popen("./build/floatdump -6.25", "r");
    ASSERT_TRUE(p != NULL);
    char line[256];
    int found = 0;
    while (fgets(line, sizeof line, p))
        if (strstr(line, "0xC0C80000")) found = 1;
    pclose(p);
    ASSERT_TRUE(found);
}

/* ---------------- C3.10 ---------------- */
TEST(C3_10_host_and_write) {
    ASSERT_EQ_INT(1, host_is_little());   /* 課程的 Docker 環境(x86-64 / arm64)都是小端 */
    uint8_t b[4];
    write_le32(b, 0xCAFEBABEu);
    const uint8_t want[4] = {0xBE, 0xBA, 0xFE, 0xCA};
    ASSERT_EQ_MEM(want, b, 4);
    ASSERT_EQ_UINT(0xCAFEBABEu, read_le32(b));
}
TEST(C3_10_bmp_header_size) {
    FILE *f = fopen("data/gradient.bmp", "rb");
    ASSERT_TRUE(f != NULL);
    uint8_t h[6];
    ASSERT_EQ_INT(6, (long)fread(h, 1, 6, f));
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fclose(f);
    ASSERT_EQ_UINT((uint32_t)size, read_le32(h + 2));
}
TEST(C3_10_bswap_involution) {
    ASSERT_EQ_UINT(0xDEADBEEFu, bswap32(bswap32(0xDEADBEEFu)));
    ASSERT_EQ_UINT(0x000000FFu, bswap32(0xFF000000u));
}
