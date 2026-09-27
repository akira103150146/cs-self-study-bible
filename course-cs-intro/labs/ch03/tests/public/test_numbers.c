/* 第 3 章 Lab 公開測試:數字(任務 1、2、3、9)。 */
#include <string.h>

#include "ctest.h"
#include "digital.h"
#include "byteorder.h"
#include "floats.h"
#include "ints.h"

/* ---------------- 任務 1:類比與數位(C3.1) ---------------- */
TEST(C3_1_bits_for_items_basic) {
    ASSERT_EQ_INT(3, bits_for_items(7));
    ASSERT_EQ_INT(5, bits_for_items(26));
    ASSERT_EQ_INT(10, bits_for_items(1000));
}
TEST(C3_1_digitize_basic) {
    ASSERT_EQ_INT(4, digitize(3.2, 5.0, 3));
    ASSERT_EQ_INT(3, digitize(1.9, 5.0, 3));
}

/* ---------------- 任務 2:負數與溢位(C3.2、C3.3) ---------------- */
TEST(C3_2_three_representations) {
    char buf[80];
    ASSERT_EQ_INT(0, to_signmag(-37, 8, buf));
    ASSERT_EQ_STR("10100101", buf);
    ASSERT_EQ_INT(0, to_ones(-37, 8, buf));
    ASSERT_EQ_STR("11011010", buf);
    ASSERT_EQ_INT(0, to_twos(-37, 8, buf));
    ASSERT_EQ_STR("11011011", buf);
}
TEST(C3_2_from_twos_basic) {
    ASSERT_EQ_INT(-25, from_twos("11100111"));
    ASSERT_EQ_INT(5, from_twos("0101"));
}
TEST(C3_2_sign_extend_basic) {
    ASSERT_EQ_INT(-128, sign_extend(0x80, 8));
    ASSERT_EQ_INT(127, sign_extend(0x7F, 8));
}
TEST(C3_3_add_overflows_basic) {
    ASSERT_EQ_INT(1, add_overflows(127, 1, 8));
    ASSERT_EQ_INT(0, add_overflows(-1, 1, 8));
}
TEST(C3_3_wrap_add_basic) {
    ASSERT_EQ_INT(-56, wrap_add(100, 100, 8));
    ASSERT_EQ_INT(2, wrap_add(5, -3, 4));
}

/* ---------------- 任務 3:浮點數(C3.4) ---------------- */
TEST(C3_4_bits_roundtrip) {
    ASSERT_EQ_UINT(0x3F800000u, f32_to_bits(1.0f));
    ASSERT_EQ_UINT(0xC0C80000u, f32_to_bits(-6.25f));
    ASSERT_NEAR(42.0, f32_from_bits(0x42280000u), 0.0);
}
TEST(C3_4_decode_normal) {
    struct f32info i = f32_decode(0xC0C80000u);
    ASSERT_EQ_INT(1, i.sign);
    ASSERT_EQ_INT(129, i.exp_bits);
    ASSERT_EQ_UINT(0x480000u, i.frac);
    ASSERT_EQ_INT(2, i.unbiased);
    ASSERT_EQ_INT(F_NORMAL, i.kind);
}
TEST(C3_4_encode_basic) {
    ASSERT_EQ_UINT(0xC0C80000u, f32_encode(1, 129, 0x480000u));
}
TEST(C3_4_binary_sci_basic) {
    char buf[64];
    ASSERT_TRUE(f32_binary_sci(0xC0C80000u, buf, sizeof buf) > 0);
    ASSERT_EQ_STR("-1.1001 x 2^2", buf);
}

/* ---------------- 任務 9:位元組順序(C3.10) ---------------- */
TEST(C3_10_bswap) { ASSERT_EQ_UINT(0x78563412u, bswap32(0x12345678u)); }
TEST(C3_10_read_le_be) {
    const uint8_t b[4] = {0x78, 0x56, 0x34, 0x12};
    ASSERT_EQ_UINT(0x12345678u, read_le32(b));
    ASSERT_EQ_UINT(0x78563412u, read_be32(b));
}
