/* 第 2 章 Lab 隱藏測試(不會發給學生):邊界情況。 */
#include <stdio.h>
#include <string.h>

#include "base.h"
#include "ctest.h"

/* ---------------- C2.1 ---------------- */
TEST(C2_1_digit_value_upper_and_bad) {
    ASSERT_EQ_INT(35, digit_value('Z'));
    ASSERT_EQ_INT(10, digit_value('A'));
    ASSERT_EQ_INT(-1, digit_value('!'));
    ASSERT_EQ_INT(-1, digit_value(':'));   /* '9' 的下一個字元 */
    ASSERT_EQ_INT(-1, digit_value('/'));   /* '0' 的前一個字元 */
    ASSERT_EQ_INT(-1, digit_value('{'));
}
TEST(C2_1_digit_char_out_of_range) {
    ASSERT_EQ_INT('?', digit_char(36));
    ASSERT_EQ_INT('?', digit_char(-1));
}

/* ---------------- C2.2 ---------------- */
TEST(C2_2_parse_hex_upper) {
    uint64_t v = 0;
    ASSERT_EQ_INT(0, parse_base("FF", 16, &v));
    ASSERT_EQ_UINT(255, v);
    ASSERT_EQ_INT(0, parse_base("z", 36, &v));
    ASSERT_EQ_UINT(35, v);
}
TEST(C2_2_parse_max_and_overflow) {
    uint64_t v = 0;
    ASSERT_EQ_INT(0, parse_base("ffffffffffffffff", 16, &v));
    ASSERT_EQ_UINT(UINT64_MAX, v);
    ASSERT_EQ_INT(0, parse_base("18446744073709551615", 10, &v));
    ASSERT_EQ_UINT(UINT64_MAX, v);
    ASSERT_EQ_INT(-2, parse_base("10000000000000000", 16, &v));
    ASSERT_EQ_INT(-2, parse_base("18446744073709551616", 10, &v));
}
TEST(C2_2_parse_bad_input) {
    uint64_t v = 0;
    ASSERT_EQ_INT(-1, parse_base("", 10, &v));
    ASSERT_EQ_INT(-1, parse_base("12", 1, &v));
    ASSERT_EQ_INT(-1, parse_base("12", 37, &v));
    ASSERT_EQ_INT(-1, parse_base("-5", 10, &v));
    ASSERT_EQ_INT(-1, parse_base("1 2", 10, &v));
}

/* ---------------- C2.3 ---------------- */
TEST(C2_3_to_base_cap_too_small) {
    char buf[9];
    ASSERT_EQ_INT(-1, to_base(255, 2, buf, 8));   /* 8 位數 + '\0' 要 9 */
    ASSERT_EQ_INT(8, to_base(255, 2, buf, 9));
    ASSERT_EQ_STR("11111111", buf);
    ASSERT_EQ_INT(-1, to_base(10, 37, buf, 9));
}
TEST(C2_3_to_base_max_and_36) {
    char buf[80];
    ASSERT_EQ_INT(64, to_base(UINT64_MAX, 2, buf, sizeof buf));
    for (int i = 0; i < 64; i++) ASSERT_TRUE(buf[i] == '1');
    to_base(1295, 36, buf, sizeof buf);
    ASSERT_EQ_STR("zz", buf);
}
TEST(C2_3_frac_stops_early) {
    char buf[32];
    frac_to_base(0.5, 2, 8, buf, sizeof buf);
    ASSERT_EQ_STR("0.1", buf);
    frac_to_base(0.75, 16, 4, buf, sizeof buf);
    ASSERT_EQ_STR("0.c", buf);
    frac_to_base(0.625, 8, 4, buf, sizeof buf);
    ASSERT_EQ_STR("0.5", buf);
    frac_to_base(0.0, 2, 4, buf, sizeof buf);
    ASSERT_EQ_STR("0.0", buf);
}
TEST(C2_3_frac_bad_input) {
    char buf[32];
    ASSERT_EQ_INT(-1, frac_to_base(1.0, 2, 4, buf, sizeof buf));
    ASSERT_EQ_INT(-1, frac_to_base(-0.25, 2, 4, buf, sizeof buf));
    ASSERT_EQ_INT(-1, frac_to_base(0.5, 2, 0, buf, sizeof buf));
    ASSERT_EQ_INT(-1, frac_to_base(0.1, 2, 20, buf, 8));   /* 放不下 */
}
TEST(C2_3_cli_roundtrip) {
    FILE *p = popen("./build/baseconv 255 10 2", "r");
    ASSERT_TRUE(p != NULL);
    char line[128] = {0};
    ASSERT_TRUE(fgets(line, sizeof line, p) != NULL);
    pclose(p);
    line[strcspn(line, "\n")] = '\0';
    ASSERT_EQ_STR("11111111", line);
}

/* ---------------- C2.4 ---------------- */
TEST(C2_4_add_leading_zeros_and_octal) {
    char out[32];
    add_in_base("007", "3", 8, out, sizeof out);
    ASSERT_EQ_STR("12", out);
    add_in_base("0", "0", 2, out, sizeof out);
    ASSERT_EQ_STR("0", out);
    add_in_base("999", "1", 10, out, sizeof out);
    ASSERT_EQ_STR("1000", out);
}
TEST(C2_4_add_long) {
    char out[64];
    add_in_base("1234567890123456789012345678901234567890", "9876543210987654321098765432109876543210", 10,
                out, sizeof out);
    ASSERT_EQ_STR("11111111101111111110111111111011111111100", out);
}
TEST(C2_4_add_errors) {
    char out[4];
    ASSERT_EQ_INT(-1, add_in_base("12", "9", 8, out, sizeof out));   /* 9 不是八進位數字 */
    ASSERT_EQ_INT(-1, add_in_base("999", "1", 10, out, 4));          /* "1000" 放不下 */
}
TEST(C2_4_sub_negative_rejected) {
    char out[32];
    ASSERT_EQ_INT(-1, sub_in_base("1", "2", 10, out, sizeof out));
    ASSERT_EQ_INT(-1, sub_in_base("001", "10", 2, out, sizeof out));
}
TEST(C2_4_sub_to_zero_and_long) {
    char out[64];
    sub_in_base("5", "5", 10, out, sizeof out);
    ASSERT_EQ_STR("0", out);
    sub_in_base("0010", "10", 2, out, sizeof out);
    ASSERT_EQ_STR("0", out);
    sub_in_base("100", "1", 8, out, sizeof out);
    ASSERT_EQ_STR("77", out);
    sub_in_base("9876543210987654321098765432109876543210", "1234567890123456789012345678901234567890", 10,
                out, sizeof out);
    ASSERT_EQ_STR("8641975320864197532086419753208641975320", out);
}
TEST(C2_4_mul_long) {
    char out[128];
    mul_in_base("1234567890123456789012345678901234567890", "9876543210987654321098765432109876543210", 10,
                out, sizeof out);
    ASSERT_EQ_STR("12193263113702179522618503273386678859448712086533622923332237463801111263526900", out);
}
TEST(C2_4_mul_zero_and_hex) {
    char out[32];
    mul_in_base("0", "12345", 10, out, sizeof out);
    ASSERT_EQ_STR("0", out);
    mul_in_base("ff", "ff", 16, out, sizeof out);
    ASSERT_EQ_STR("fe01", out);
    mul_in_base("zz", "zz", 36, out, sizeof out);
    ASSERT_EQ_STR("zy01", out);
}

/* ---------------- C2.5 ---------------- */
TEST(C2_5_regroup_leading_zeros) {
    char out[32];
    regroup("000101", 3, out, sizeof out);
    ASSERT_EQ_STR("5", out);
    regroup("0", 3, out, sizeof out);
    ASSERT_EQ_STR("0", out);
    regroup("0011", 1, out, sizeof out);
    ASSERT_EQ_STR("11", out);
}
TEST(C2_5_regroup_base32) {
    char out[32];
    regroup("110101101", 5, out, sizeof out);
    ASSERT_EQ_STR("dd", out);
}
TEST(C2_5_regroup_errors) {
    char out[32];
    ASSERT_EQ_INT(-1, regroup("102", 3, out, sizeof out));
    ASSERT_EQ_INT(-1, regroup("101", 0, out, sizeof out));
    ASSERT_EQ_INT(-1, regroup("101", 6, out, sizeof out));
    ASSERT_EQ_INT(-1, regroup("", 3, out, sizeof out));
}

/* ---------------- C2.6 ---------------- */
TEST(C2_6_bits_needed_edges) {
    ASSERT_EQ_INT(1, bits_needed(0));
    ASSERT_EQ_INT(1, bits_needed(1));
    ASSERT_EQ_INT(2, bits_needed(2));
    ASSERT_EQ_INT(64, bits_needed(UINT64_MAX));
}
TEST(C2_6_max_unsigned_64) {
    ASSERT_EQ_UINT(UINT64_MAX, max_unsigned(64));
    ASSERT_EQ_UINT(0, max_unsigned(0));
    ASSERT_EQ_UINT(0, max_unsigned(65));
}
