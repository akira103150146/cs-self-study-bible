/* 任務 5 參考解(C3.6)。 */
#include "compress.h"

#include <ctype.h>
#include <string.h>

/* ---------------- keyword encoding ---------------- */
static int is_letter(char c) { return isalpha((unsigned char)c) != 0; }

long keyword_encode(const char *in, const struct keyword *kw, size_t nkw, char *out, size_t cap) {
    size_t n = 0;
    for (size_t i = 0; in[i];) {
        int matched = 0;
        if (i == 0 || !is_letter(in[i - 1])) {
            for (size_t k = 0; k < nkw; k++) {
                size_t len = strlen(kw[k].word);
                if (strncmp(in + i, kw[k].word, len) == 0 && !is_letter(in[i + len])) {
                    if (n + 1 >= cap) return -1;
                    out[n++] = kw[k].code;
                    i += len;
                    matched = 1;
                    break;
                }
            }
        }
        if (!matched) {
            if (n + 1 >= cap) return -1;
            out[n++] = in[i++];
        }
    }
    if (n >= cap) return -1;
    out[n] = '\0';
    return (long)n;
}

/* ---------------- run-length encoding ---------------- */
long rle_encode(const char *in, char *out, size_t cap) {
    if (strchr(in, '*')) return -1;
    size_t n = 0;
    for (size_t i = 0; in[i];) {
        size_t j = i;
        while (in[j] == in[i]) j++;
        size_t run = j - i;
        while (run > 0) {
            size_t k = run > 9 ? 9 : run;
            if (k >= 4) {
                if (n + 3 >= cap) return -1;
                out[n++] = '*';
                out[n++] = in[i];
                out[n++] = (char)('0' + (int)k);
            } else {
                for (size_t t = 0; t < k; t++) {
                    if (n + 1 >= cap) return -1;
                    out[n++] = in[i];
                }
            }
            run -= k;
        }
        i = j;
    }
    if (n >= cap) return -1;
    out[n] = '\0';
    return (long)n;
}

long rle_decode(const char *in, char *out, size_t cap) {
    size_t n = 0;
    for (size_t i = 0; in[i];) {
        size_t reps = 1;
        char c = in[i];
        if (c == '*') {
            if (!in[i + 1] || in[i + 2] < '4' || in[i + 2] > '9') return -1;
            c = in[i + 1];
            reps = (size_t)(in[i + 2] - '0');
            i += 3;
        } else {
            i++;
        }
        for (size_t t = 0; t < reps; t++) {
            if (n + 1 >= cap) return -1;
            out[n++] = c;
        }
    }
    if (n >= cap) return -1;
    out[n] = '\0';
    return (long)n;
}

/* ---------------- Huffman ---------------- */
#define MAXLEN 32   /* 碼長上限;本 Lab 的資料不會超過 */

int huff_code_lengths(const uint64_t freq[256], uint8_t len[256]) {
    uint64_t w[511];
    int parent[511], alive[511], nodes = 0, leaf_of[256];
    memset(len, 0, 256);
    for (int s = 0; s < 256; s++) {
        leaf_of[s] = -1;
        if (freq[s]) {
            leaf_of[s] = nodes;
            w[nodes] = freq[s];
            parent[nodes] = -1;
            alive[nodes++] = 1;
        }
    }
    if (nodes == 0) return 0;
    if (nodes == 1) {
        for (int s = 0; s < 256; s++)
            if (leaf_of[s] >= 0) len[s] = 1;
        return 0;
    }
    int remaining = nodes;
    while (remaining > 1) {   /* 每次合併權重最小的兩個節點(線性搜尋,最多 511 個節點) */
        int a = -1, b = -1;
        for (int i = 0; i < nodes; i++) {
            if (!alive[i]) continue;
            if (a < 0 || w[i] < w[a]) b = a, a = i;
            else if (b < 0 || w[i] < w[b]) b = i;
        }
        w[nodes] = w[a] + w[b];
        parent[nodes] = -1;
        alive[nodes] = 1;
        parent[a] = parent[b] = nodes;
        alive[a] = alive[b] = 0;
        nodes++;
        remaining--;
    }
    for (int s = 0; s < 256; s++) {
        if (leaf_of[s] < 0) continue;
        int d = 0;
        for (int v = leaf_of[s]; parent[v] >= 0; v = parent[v]) d++;
        len[s] = (uint8_t)d;
    }
    return 0;
}

uint64_t huff_total_bits(const uint64_t freq[256], const uint8_t len[256]) {
    uint64_t t = 0;
    for (int s = 0; s < 256; s++) t += freq[s] * len[s];
    return t;
}

/* canonical 碼:first[L] = 長度 L 的第一個碼;順序是(碼長, 符號值)。碼長不合法(Kraft 不等式不成立)→ -1 */
static int canonical(const uint8_t len[256], uint32_t code[256], uint32_t first[MAXLEN + 2], int count[MAXLEN + 2],
                     uint8_t order[256], int *nsym) {
    memset(count, 0, sizeof(int) * (MAXLEN + 2));
    for (int s = 0; s < 256; s++) {
        if (len[s] > MAXLEN) return -1;
        if (len[s]) count[len[s]]++;
    }
    uint64_t c = 0;
    int k = 0;
    for (int L = 1; L <= MAXLEN; L++) {
        if (L > 1) c = (c + (uint64_t)count[L - 1]) << 1;   /* 上一個長度用完之後,下一個碼補一位 0 */
        first[L] = (uint32_t)c;
        if (c + (uint64_t)count[L] > ((uint64_t)1 << L)) return -1;
        uint64_t next = c;
        for (int s = 0; s < 256; s++)
            if (len[s] == L) {
                code[s] = (uint32_t)next++;
                order[k++] = (uint8_t)s;
            }
    }
    *nsym = k;
    return 0;
}

long huff_compress(const uint8_t *in, size_t n, uint8_t *out, size_t cap) {
    uint64_t freq[256] = {0};
    uint8_t len[256];
    uint32_t code[256], first[MAXLEN + 2];
    int count[MAXLEN + 2], nsym;
    uint8_t order[256];
    for (size_t i = 0; i < n; i++) freq[in[i]]++;
    huff_code_lengths(freq, len);
    if (canonical(len, code, first, count, order, &nsym) < 0) return -1;
    uint64_t bits = huff_total_bits(freq, len);
    size_t total = 4 + 256 + (size_t)((bits + 7) / 8);
    if (total > cap || n > 0xFFFFFFFFu) return -1;
    for (int k = 0; k < 4; k++) out[k] = (uint8_t)(n >> (8 * k));
    memcpy(out + 4, len, 256);
    memset(out + 260, 0, total - 260);
    uint64_t pos = 0;
    for (size_t i = 0; i < n; i++) {
        int L = len[in[i]];
        for (int b = L - 1; b >= 0; b--, pos++)
            if ((code[in[i]] >> b) & 1) out[260 + pos / 8] |= (uint8_t)(0x80 >> (pos % 8));
    }
    return (long)total;
}

long huff_decompress(const uint8_t *in, size_t n, uint8_t *out, size_t cap) {
    if (n < 260) return -1;
    size_t orig = (size_t)in[0] | (size_t)in[1] << 8 | (size_t)in[2] << 16 | (size_t)in[3] << 24;
    uint8_t len[256];
    memcpy(len, in + 4, 256);
    uint32_t code[256], first[MAXLEN + 2];
    int count[MAXLEN + 2], nsym;
    uint8_t order[256];
    if (canonical(len, code, first, count, order, &nsym) < 0) return -1;
    if (orig > cap || (orig > 0 && nsym == 0)) return -1;
    uint64_t pos = 0, nbits = (uint64_t)(n - 260) * 8;
    for (size_t i = 0; i < orig; i++) {
        uint32_t c = 0;
        int index = 0, found = 0;
        for (int L = 1; L <= MAXLEN; L++) {
            if (pos >= nbits) return -1;
            c = (c << 1) | ((in[260 + pos / 8] >> (7 - pos % 8)) & 1);
            pos++;
            if (count[L] && c >= first[L] && c - first[L] < (uint32_t)count[L]) {
                out[i] = order[index + (int)(c - first[L])];
                found = 1;
                break;
            }
            index += count[L];
        }
        if (!found) return -1;
    }
    return (long)orig;
}
