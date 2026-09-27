---
lang: c
dir: labs/ch02
---
## 概要
你要用 C 寫一個進位轉換與運算的函式庫 `baseconv`,把第 2 章的每個觀念都親手實作一次:數字與位值、Horner 法、連除與連乘、各進位的直式四則運算、2 的冪次分組、位元與範圍。

**限制**:`src/base.c` 不能使用 `strtol`、`strtoul`、`sscanf`、`atoi` 與 `printf` 家族——`make` 會先檢查,用了就不給編譯。所有轉換都要靠你自己寫的位值記數。

介面在 `src/base.h`(已寫好,不要改);指令列工具 `src/app_baseconv.c` 也已寫好,做完後可以這樣玩:

```text
$ ./build/baseconv 255 10 2
11111111
$ ./build/baseconv add ff 1 16
100
```

## 環境
```text
docker run --rm -it -v "$PWD:/work" cs-intro-env bash
make build                           # 編譯(含禁用函式檢查)
make test                            # 跑全部公開測試
./build/test_base C2_4_add_carry_chain   # 只跑一個測試
```

編譯時開了 AddressSanitizer 與 UndefinedBehaviorSanitizer:陣列越界、未定義的移位都會讓測試直接失敗,並印出出錯的那一行。

## 任務 1 · 數字與位值 · C2.1
把一個字元換成它代表的數字,以及反過來。大小寫字母代表同一個值。

```c interface
int digit_value(char c);   /* '0'–'9'、'a'–'z'、'A'–'Z' → 0–35;其他字元 → -1 */
char digit_char(int v);    /* 0–35 → '0'–'9'、'a'–'z';超出範圍 → '?' */
```

## 任務 2 · 轉成十進位 · C2.2
用 **Horner 法**把 b 進位字串轉成 64 位元無號整數。必須在溢位**發生之前**就偵測到。

```c interface
int parse_base(const char *s, int base, uint64_t *out);
/* 0 成功;-1 基底不在 2–36、字串是空的、或有不屬於該基底的字元;-2 超過 64 位元 */
```

## 任務 3 · 從十進位轉出去 · C2.3
整數用**連除取餘數**,小數用**連乘取整數部分**。

```c interface
int to_base(uint64_t v, int base, char *buf, size_t cap);
/* 回傳長度(不含 '\0');cap 不夠或基底錯 → -1 */
int frac_to_base(double x, int base, int max_digits, char *buf, size_t cap);
/* 0 ≤ x < 1 → "0.xxx",最多 max_digits 位,小數變 0 就提前結束;x = 0 → "0.0"。成功回傳 0,錯誤 → -1 */
```

範例:`frac_to_base(0.1, 2, 8, …)` 得到 `"0.00011001"`。

## 任務 4 · 各進位的四則運算 · C2.4
直接在**數字字串**上做直式加、減、乘,不得先轉成整數(隱藏測試有 40 位數的大數,64 位元裝不下)。

```c interface
int add_in_base(const char *a, const char *b, int base, char *out, size_t cap);
int sub_in_base(const char *a, const char *b, int base, char *out, size_t cap);   /* a < b → -1 */
int mul_in_base(const char *a, const char *b, int base, char *out, size_t cap);
/* 結果去掉前導零(零是 "0"),回傳長度;不合法的數字、基底錯、或 cap 不夠 → -1 */
```

## 任務 5 · 2 的冪次進位 · C2.5
二進位字串轉成基底 $2^k$($k$ = 1–5),**靠分組**完成:從右邊每 $k$ 位一組,左邊不足補零,結果去掉前導零。

```c interface
int regroup(const char *bin, int k, char *out, size_t cap);   /* 錯誤 → -1 */
```

範例:`regroup("1011", 3, …)` 得到 `"13"`;`regroup("110101101", 5, …)` 得到 `"dd"`。

## 任務 6 · 位元與範圍 · C2.6
```c interface
int bits_needed(uint64_t n);      /* 用二進位表示 n 至少要幾位;n = 0 → 1 */
uint64_t max_unsigned(int bits);  /* 1 ≤ bits ≤ 64 → 2^bits − 1;超出範圍 → 0 */
```

提示:在 C 裡 `(uint64_t)1 << 64` 是未定義行為,UBSan 會抓到。

## 繳交
`make test` 全部通過後,把 `src/base.c` 提交到你的 git repo。老師的隱藏測試會檢查:大寫字母、剛好 $2^{64}-1$ 與超過一點點、`cap` 剛好不夠、前導零、連續借位、40 位數的加減乘、基底 36、k = 5 的分組,以及指令列工具的輸出。
