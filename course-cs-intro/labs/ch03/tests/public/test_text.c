/* 第 3 章 Lab 公開測試:文字與壓縮(任務 4、5)。 */
#include <stdlib.h>
#include <string.h>

#include "compress.h"
#include "ctest.h"
#include "utf8.h"

/* ---------------- 任務 4:文字(C3.5) ---------------- */
TEST(C3_5_encode_three_bytes) {
    uint8_t out[4];
    ASSERT_EQ_INT(3, utf8_encode(0x4E2D, out));
    const uint8_t want[3] = {0xE4, 0xB8, 0xAD};
    ASSERT_EQ_MEM(want, out, 3);
}
TEST(C3_5_encode_ascii_and_emoji) {
    uint8_t out[4];
    ASSERT_EQ_INT(1, utf8_encode('A', out));
    ASSERT_EQ_INT(0x41, out[0]);
    ASSERT_EQ_INT(4, utf8_encode(0x1F600, out));
    const uint8_t want[4] = {0xF0, 0x9F, 0x98, 0x80};
    ASSERT_EQ_MEM(want, out, 4);
}
TEST(C3_5_decode_basic) {
    const uint8_t s[3] = {0xE4, 0xB8, 0xAD};
    uint32_t cp = 0;
    ASSERT_EQ_INT(3, utf8_decode(s, 3, &cp));
    ASSERT_EQ_UINT(0x4E2D, cp);
}
TEST(C3_5_count_basic) {
    const char *s = "abc\xE4\xB8\xAD";   /* abc中 */
    ASSERT_EQ_INT(4, utf8_count((const uint8_t *)s, strlen(s)));
}
TEST(C3_5_toggle_case) {
    ASSERT_EQ_INT('A', ascii_toggle_case('a'));
    ASSERT_EQ_INT('z', ascii_toggle_case('Z'));
}

/* ---------------- 任務 5:壓縮(C3.6) ---------------- */
TEST(C3_6_keyword_basic) {
    const struct keyword kw[] = {{"the", '~'}, {"and", '+'}};
    char out[64];
    ASSERT_EQ_INT(13, keyword_encode("the cat and the dog", kw, 2, out, sizeof out));
    ASSERT_EQ_STR("~ cat + ~ dog", out);
}
TEST(C3_6_rle_encode_basic) {
    char out[64];
    ASSERT_EQ_INT(13, rle_encode("AAAAAAAAAAAABBBCDDDDD", out, sizeof out));
    ASSERT_EQ_STR("*A9AAABBBC*D5", out);
}
TEST(C3_6_rle_decode_basic) {
    char out[64];
    ASSERT_EQ_INT(12, rle_decode("Q*R5ST*U4", out, sizeof out));
    ASSERT_EQ_STR("QRRRRRSTUUUU", out);
}
TEST(C3_6_huffman_lengths_optimal) {
    uint64_t freq[256] = {0};
    uint8_t len[256];
    freq['A'] = 5, freq['B'] = 2, freq['C'] = 1, freq['D'] = 1;
    ASSERT_EQ_INT(0, huff_code_lengths(freq, len));
    ASSERT_EQ_UINT(15, huff_total_bits(freq, len));
    ASSERT_EQ_INT(1, len['A']);
    ASSERT_EQ_INT(0, len['Z']);
}
TEST(C3_6_huffman_roundtrip_small) {
    const char *msg = "abracadabra abracadabra";
    size_t n = strlen(msg);
    uint8_t comp[1024], back[64];
    long c = huff_compress((const uint8_t *)msg, n, comp, sizeof comp);
    ASSERT_TRUE(c > 0);
    ASSERT_EQ_INT((long)n, huff_decompress(comp, (size_t)c, back, sizeof back));
    ASSERT_EQ_MEM(msg, back, n);
}
