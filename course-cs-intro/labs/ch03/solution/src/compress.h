/* compress.h — 任務 5(C3.6)文字壓縮。這個檔案已經寫好,不要改。 */
#ifndef COMPRESS_H
#define COMPRESS_H
#include <stddef.h>
#include <stdint.h>

struct keyword {
    const char *word;
    char code;
};
long keyword_encode(const char *in, const struct keyword *kw, size_t nkw, char *out, size_t cap);
/* 把「完整的單字」(前後不是英文字母)換成代碼,大小寫要完全相同;回傳長度,cap 不夠 → -1 */

long rle_encode(const char *in, char *out, size_t cap);
/* 本課 RLE:連續 4–9 個相同字元 → '*' 字元 個數;超過 9 個先切成 9 個一段;少於 4 個照原樣。
 * 原文含 '*' 或 cap 不夠 → -1;成功回傳長度 */
long rle_decode(const char *in, char *out, size_t cap);
/* rle_encode 的反向;'*' 後面缺字元、個數不是 '4'–'9'、或 cap 不夠 → -1 */

int huff_code_lengths(const uint64_t freq[256], uint8_t len[256]);
/* 最佳(Huffman)碼長:出現過的符號長度 ≥ 1,沒出現的是 0;只有一種符號時長度 1。回傳 0 */
uint64_t huff_total_bits(const uint64_t freq[256], const uint8_t len[256]);   /* Σ freq × len */

long huff_compress(const uint8_t *in, size_t n, uint8_t *out, size_t cap);
long huff_decompress(const uint8_t *in, size_t n, uint8_t *out, size_t cap);
/* 格式:4 位元組原始長度(little-endian)+ 256 位元組碼長 + canonical Huffman 位元流(每個位元組由最高位開始填)。
 * canonical 碼:依(碼長, 符號值)排序,第一個碼是 0,之後每個碼 = (前一個碼 + 1) << (這個碼長 − 前一個碼長)。
 * 成功回傳輸出長度;壞檔(檔頭不完整、碼長不合法、位元流不夠)或 cap 不夠 → -1 */
#endif
