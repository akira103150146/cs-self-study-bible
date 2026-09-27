/* 第 2 章 Lab 公開測試。make test 會編譯並執行。 */
#include "base.h"
#include "ctest.h"

/* ---------------- 任務 1:數字與位值(C2.1) ---------------- */
TEST(C2_1_digit_value_basic) {
    ASSERT_EQ_INT(0, digit_value('0'));
    ASSERT_EQ_INT(9, digit_value('9'));
    ASSERT_EQ_INT(10, digit_value('a'));
    ASSERT_EQ_INT(35, digit_value('z'));
}
TEST(C2_1_digit_char_basic) {
    ASSERT_EQ_INT('0', digit_char(0));
    ASSERT_EQ_INT('f', digit_char(15));
    ASSERT_EQ_INT('z', digit_char(35));
}

/* ---------------- 任務 2:轉成十進位(C2.2) ---------------- */
TEST(C2_2_parse_hex) {
    uint64_t v = 0;
    ASSERT_EQ_INT(0, parse_base("ff", 16, &v));
    ASSERT_EQ_UINT(255, v);
}
TEST(C2_2_parse_octal_binary) {
    uint64_t v = 0;
    ASSERT_EQ_INT(0, parse_base("777", 8, &v));
    ASSERT_EQ_UINT(511, v);
    ASSERT_EQ_INT(0, parse_base("101101", 2, &v));
    ASSERT_EQ_UINT(45, v);
}
TEST(C2_2_parse_bad_digit) {
    uint64_t v = 0;
    ASSERT_EQ_INT(-1, parse_base("102", 2, &v));
}

/* ---------------- 任務 3:從十進位轉出去(C2.3) ---------------- */
TEST(C2_3_to_base_hex_bin) {
    char buf[80];
    ASSERT_EQ_INT(2, to_base(255, 16, buf, sizeof buf));
    ASSERT_EQ_STR("ff", buf);
    ASSERT_EQ_INT(8, to_base(255, 2, buf, sizeof buf));
    ASSERT_EQ_STR("11111111", buf);
}
TEST(C2_3_to_base_zero) {
    char buf[8];
    ASSERT_EQ_INT(1, to_base(0, 2, buf, sizeof buf));
    ASSERT_EQ_STR("0", buf);
}
TEST(C2_3_frac_point1_binary) {
    char buf[32];
    ASSERT_EQ_INT(0, frac_to_base(0.1, 2, 8, buf, sizeof buf));
    ASSERT_EQ_STR("0.00011001", buf);
}

/* ---------------- 任務 4:各進位的四則運算(C2.4) ---------------- */
TEST(C2_4_add_carry_chain) {
    char out[32];
    ASSERT_EQ_INT(4, add_in_base("fff", "1", 16, out, sizeof out));
    ASSERT_EQ_STR("1000", out);
}
TEST(C2_4_add_binary) {
    char out[32];
    add_in_base("1011", "11", 2, out, sizeof out);
    ASSERT_EQ_STR("1110", out);
}
TEST(C2_4_sub_borrow) {
    char out[32];
    ASSERT_EQ_INT(3, sub_in_base("1000", "1", 16, out, sizeof out));
    ASSERT_EQ_STR("fff", out);
}
TEST(C2_4_mul_small) {
    char out[32];
    mul_in_base("12", "12", 10, out, sizeof out);
    ASSERT_EQ_STR("144", out);
    mul_in_base("101", "11", 2, out, sizeof out);
    ASSERT_EQ_STR("1111", out);
}

/* ---------------- 任務 5:2 的冪次進位(C2.5) ---------------- */
TEST(C2_5_regroup_hex) {
    char out[32];
    ASSERT_EQ_INT(2, regroup("11111111", 4, out, sizeof out));
    ASSERT_EQ_STR("ff", out);
}
TEST(C2_5_regroup_pad) {
    char out[32];
    regroup("1011", 3, out, sizeof out);
    ASSERT_EQ_STR("13", out);
}

/* ---------------- 任務 6:位元與範圍(C2.6) ---------------- */
TEST(C2_6_bits_needed_basic) {
    ASSERT_EQ_INT(8, bits_needed(255));
    ASSERT_EQ_INT(9, bits_needed(256));
}
TEST(C2_6_max_unsigned_byte) {
    ASSERT_EQ_UINT(255, max_unsigned(8));
    ASSERT_EQ_UINT(1, max_unsigned(1));
}
