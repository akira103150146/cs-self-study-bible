/* 第 3 章 Lab 隱藏測試:文字與壓縮的邊界情況。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "compress.h"
#include "ctest.h"
#include "utf8.h"

/* ---------------- C3.5 ---------------- */
TEST(C3_5_encode_boundaries) {
    uint8_t o[4];
    ASSERT_EQ_INT(1, utf8_encode(0x7F, o));
    ASSERT_EQ_INT(2, utf8_encode(0x80, o));
    ASSERT_EQ_INT(0xC2, o[0]);
    ASSERT_EQ_INT(0x80, o[1]);
    ASSERT_EQ_INT(2, utf8_encode(0x7FF, o));
    ASSERT_EQ_INT(0xDF, o[0]);
    ASSERT_EQ_INT(3, utf8_encode(0x800, o));
    ASSERT_EQ_INT(0xE0, o[0]);
    ASSERT_EQ_INT(0xA0, o[1]);
    ASSERT_EQ_INT(3, utf8_encode(0xFFFF, o));
    ASSERT_EQ_INT(4, utf8_encode(0x10000, o));
    ASSERT_EQ_INT(0x90, o[1]);
    ASSERT_EQ_INT(4, utf8_encode(0x10FFFF, o));
    const uint8_t want[4] = {0xF4, 0x8F, 0xBF, 0xBF};
    ASSERT_EQ_MEM(want, o, 4);
}
TEST(C3_5_encode_rejects_invalid) {
    uint8_t o[4];
    ASSERT_EQ_INT(-1, utf8_encode(0x110000, o));
    ASSERT_EQ_INT(-1, utf8_encode(0xD800, o));
    ASSERT_EQ_INT(-1, utf8_encode(0xDFFF, o));
}
static int dec(const char *hex_bytes, size_t n) {
    uint32_t cp;
    return utf8_decode((const uint8_t *)hex_bytes, n, &cp);
}
TEST(C3_5_decode_rejects_overlong_and_surrogate) {
    ASSERT_EQ_INT(-1, dec("\xC0\x80", 2));
    ASSERT_EQ_INT(-1, dec("\xC1\xBF", 2));
    ASSERT_EQ_INT(-1, dec("\xE0\x80\x80", 3));
    ASSERT_EQ_INT(-1, dec("\xF0\x80\x80\x80", 4));
    ASSERT_EQ_INT(-1, dec("\xED\xA0\x80", 3));
    ASSERT_EQ_INT(-1, dec("\xF4\x90\x80\x80", 4));
}
TEST(C3_5_decode_rejects_malformed) {
    ASSERT_EQ_INT(-1, dec("\xE4\xB8", 2));      /* 截斷 */
    ASSERT_EQ_INT(-1, dec("\xE4\x41\xAD", 3));  /* 延續位元組不是 10xxxxxx */
    ASSERT_EQ_INT(-1, dec("\x80", 1));          /* 延續位元組不能當開頭 */
    ASSERT_EQ_INT(-1, dec("\xFF", 1));
    ASSERT_EQ_INT(-1, dec("\xF8\x88\x80\x80\x80", 5));
    uint32_t cp;
    ASSERT_EQ_INT(-1, utf8_decode((const uint8_t *)"", 0, &cp));
}
TEST(C3_5_decode_only_first_char) {
    uint32_t cp = 0;
    ASSERT_EQ_INT(1, utf8_decode((const uint8_t *)"AB", 2, &cp));
    ASSERT_EQ_UINT('A', cp);
    ASSERT_EQ_INT(4, utf8_decode((const uint8_t *)"\xF0\x9F\x98\x80zz", 6, &cp));
    ASSERT_EQ_UINT(0x1F600, cp);
}
TEST(C3_5_count_mixed_and_invalid) {
    const char *s = "\xE4\xB8\xAD\xE6\x96\x87\xF0\x9F\x98\x80";   /* 中文😀 */
    ASSERT_EQ_INT(3, utf8_count((const uint8_t *)s, strlen(s)));
    ASSERT_EQ_INT(0, utf8_count((const uint8_t *)"", 0));
    ASSERT_EQ_INT(-1, utf8_count((const uint8_t *)"ab\xC0\x80", 4));
    ASSERT_EQ_INT(-1, utf8_count((const uint8_t *)"ab\xE4\xB8", 4));
}
TEST(C3_5_toggle_non_letters) {
    ASSERT_EQ_INT('@', ascii_toggle_case('@'));
    ASSERT_EQ_INT('1', ascii_toggle_case('1'));
    ASSERT_EQ_INT('[', ascii_toggle_case('['));
    ASSERT_EQ_INT('`', ascii_toggle_case('`'));
}

/* ---------------- C3.6 ---------------- */
TEST(C3_6_keyword_whole_words_only) {
    const struct keyword kw[] = {{"the", '~'}, {"and", '+'}};
    char out[64];
    keyword_encode("there and theme, the", kw, 2, out, sizeof out);
    ASSERT_EQ_STR("there + theme, ~", out);
    keyword_encode("The end", kw, 2, out, sizeof out);
    ASSERT_EQ_STR("The end", out);
    ASSERT_EQ_INT(-1, keyword_encode("the cat", kw, 2, out, 4));
}
TEST(C3_6_rle_long_runs_and_errors) {
    char out[64];
    rle_encode("XXXXYYYZZZZZZZZZZ", out, sizeof out);
    ASSERT_EQ_STR("*X4YYY*Z9Z", out);
    rle_encode("", out, sizeof out);
    ASSERT_EQ_STR("", out);
    ASSERT_EQ_INT(-1, rle_encode("a*b", out, sizeof out));
    ASSERT_EQ_INT(-1, rle_encode("AAAAAAA", out, 3));
    ASSERT_EQ_INT(-1, rle_decode("A*B", out, sizeof out));
    ASSERT_EQ_INT(-1, rle_decode("*A3", out, sizeof out));
    ASSERT_EQ_INT(-1, rle_decode("*Z9", out, 5));
}
TEST(C3_6_rle_roundtrip_many) {
    const char *cases[] = {"A", "AAAA", "ABABABAB", "BBBBBBBBBBBBBBBBBBBBBBBBB", "xyzzzzzzzzzzzzzq", "  hello   world"};
    for (size_t i = 0; i < sizeof cases / sizeof *cases; i++) {
        char enc[128], dec2[128];
        ASSERT_TRUE(rle_encode(cases[i], enc, sizeof enc) >= 0);
        ASSERT_EQ_INT((long)strlen(cases[i]), rle_decode(enc, dec2, sizeof dec2));
        ASSERT_EQ_STR(cases[i], dec2);
    }
}
TEST(C3_6_huffman_textbook_example) {
    uint64_t freq[256] = {0};
    uint8_t len[256];
    const char *sym = "abcdef";
    const uint64_t f[] = {45, 13, 12, 16, 9, 5};
    for (int i = 0; i < 6; i++) freq[(uint8_t)sym[i]] = f[i];
    huff_code_lengths(freq, len);
    ASSERT_EQ_UINT(224, huff_total_bits(freq, len));
}
TEST(C3_6_huffman_single_symbol) {
    uint64_t freq[256] = {0};
    uint8_t len[256];
    freq['Q'] = 7;
    huff_code_lengths(freq, len);
    ASSERT_EQ_INT(1, len['Q']);
}

static long file_bytes(const char *path, uint8_t **buf) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    long n = ftell(f);
    fseek(f, 0, SEEK_SET);
    *buf = malloc((size_t)n + 1);
    if (fread(*buf, 1, (size_t)n, f) != (size_t)n) n = -1;
    fclose(f);
    return n;
}
static void roundtrip_file(const char *path, double max_ratio) {
    uint8_t *in = NULL;
    long n = file_bytes(path, &in);
    ASSERT_TRUE(n >= 0);
    size_t cap = (size_t)n * 2 + 1024;
    uint8_t *comp = malloc(cap), *back = malloc((size_t)n + 1);
    long c = huff_compress(in, (size_t)n, comp, cap);
    ASSERT_TRUE(c > 0);
    ASSERT_EQ_INT(n, huff_decompress(comp, (size_t)c, back, (size_t)n + 1));
    ASSERT_EQ_MEM(in, back, (size_t)n);
    if (max_ratio > 0) ASSERT_TRUE((double)c / (double)n < max_ratio);
    free(in), free(comp), free(back);
}
TEST(C3_6_hzip_english_compresses) { roundtrip_file("data/english.txt", 0.7); }
TEST(C3_6_hzip_same_byte) { roundtrip_file("data/same.bin", 0.2); }   /* 1 位元/位元組 + 260 位元組檔頭 ≈ 0.19 */
TEST(C3_6_hzip_random) { roundtrip_file("data/random.bin", 0.0); }
TEST(C3_6_hzip_empty) {
    uint8_t comp[512], back[4];
    long c = huff_compress((const uint8_t *)"", 0, comp, sizeof comp);
    ASSERT_TRUE(c > 0);
    ASSERT_EQ_INT(0, huff_decompress(comp, (size_t)c, back, sizeof back));
}
TEST(C3_6_hzip_rejects_garbage) {
    uint8_t junk[300], back[16];
    memset(junk, 1, sizeof junk);   /* 256 個碼長都是 1:違反前綴碼的 Kraft 不等式 */
    ASSERT_EQ_INT(-1, huff_decompress(junk, sizeof junk, back, sizeof back));
    ASSERT_EQ_INT(-1, huff_decompress(junk, 10, back, sizeof back));   /* 檔頭不完整 */
}
TEST(C3_6_hzip_cli_roundtrip) {
    ASSERT_EQ_INT(0, system("./build/hzip c data/english.txt build/e.hz && ./build/hzip d build/e.hz build/e.txt"
                            " && cmp -s data/english.txt build/e.txt"));
}
