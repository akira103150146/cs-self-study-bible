/* ctest.h — 計概 Lab 用的零依賴 C 單元測試。
 *
 * 每個測試在自己的子行程(fork)裡跑:當掉(segfault、ASan 報錯)或逾時,
 * 只會讓那一個測試 FAIL,其他測試照跑。
 *
 * 用法:
 *     #include "ctest.h"
 *     TEST(C3_2_twos_negative) { ASSERT_EQ_STR("11011011", buf); }
 *
 * 測試名稱請以觀念 ID 開頭(C3_2_ = 觀念 C3.2),涵蓋度檢查靠它。
 * 輸出:每個測試一行 PASS / FAIL,最後一行 "ctest: P passed, F failed";有失敗時 exit 1。
 * 只跑一個測試:./build/test_xxx C3_2_twos_negative
 */
#ifndef CTEST_H
#define CTEST_H
#include <math.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#ifndef CTEST_TIMEOUT
#define CTEST_TIMEOUT 5
#endif
#define CTEST_MAX 512
#define CTEST_ASSERT_EXIT 77   /* 斷言失敗用這個結束碼;其他非零 = 當掉(例如 sanitizer 報錯) */

typedef void (*ctest_fn)(void);
struct ctest_case {
    const char *name;
    ctest_fn fn;
};
static struct ctest_case ctest_cases[CTEST_MAX];
static int ctest_n;

#define TEST(name)                                                                        \
    static void name(void);                                                               \
    __attribute__((constructor)) static void ctest_reg_##name(void) {                     \
        if (ctest_n < CTEST_MAX) ctest_cases[ctest_n++] = (struct ctest_case){#name, name}; \
    }                                                                                     \
    static void name(void)

#define CTEST_FAIL(...)                                  \
    do {                                                 \
        printf("    %s:%d: ", __FILE__, __LINE__);       \
        printf(__VA_ARGS__);                             \
        printf("\n");                                    \
        fflush(stdout);                                  \
        _exit(CTEST_ASSERT_EXIT);                        \
    } while (0)

#define ASSERT_TRUE(c)                                   \
    do {                                                 \
        if (!(c)) CTEST_FAIL("expected true: %s", #c);   \
    } while (0)

#define ASSERT_EQ_INT(exp, got)                                                    \
    do {                                                                           \
        long long e_ = (long long)(exp), g_ = (long long)(got);                    \
        if (e_ != g_) CTEST_FAIL("%s: expected %lld, got %lld", #got, e_, g_);     \
    } while (0)

#define ASSERT_EQ_UINT(exp, got)                                                            \
    do {                                                                                    \
        unsigned long long e_ = (unsigned long long)(exp), g_ = (unsigned long long)(got);  \
        if (e_ != g_)                                                                       \
            CTEST_FAIL("%s: expected %llu (0x%llx), got %llu (0x%llx)", #got, e_, e_, g_, g_); \
    } while (0)

#define ASSERT_EQ_STR(exp, got)                                                            \
    do {                                                                                   \
        const char *e_ = (exp), *g_ = (got);                                               \
        if (!g_ || strcmp(e_, g_) != 0)                                                    \
            CTEST_FAIL("%s: expected \"%s\", got \"%s\"", #got, e_, g_ ? g_ : "(null)");  \
    } while (0)

#define ASSERT_NEAR(exp, got, tol)                                                           \
    do {                                                                                     \
        double e_ = (exp), g_ = (got);                                                       \
        if (!(fabs(e_ - g_) <= (tol)))                                                       \
            CTEST_FAIL("%s: expected %.10g +/- %g, got %.10g", #got, e_, (double)(tol), g_); \
    } while (0)

#define ASSERT_EQ_MEM(exp, got, n)                                                        \
    do {                                                                                  \
        const unsigned char *e_ = (const unsigned char *)(exp);                           \
        const unsigned char *g_ = (const unsigned char *)(got);                           \
        for (size_t i_ = 0; i_ < (size_t)(n); i_++)                                       \
            if (e_[i_] != g_[i_])                                                         \
                CTEST_FAIL("%s: byte %zu expected 0x%02x, got 0x%02x", #got, i_, e_[i_], g_[i_]); \
    } while (0)

#ifndef CTEST_NO_MAIN
int main(int argc, char **argv) {
    int passed = 0, failed = 0;
    setvbuf(stdout, NULL, _IOLBF, 0);
    for (int i = 0; i < ctest_n; i++) {
        if (argc > 1 && strcmp(argv[1], ctest_cases[i].name) != 0) continue;
        fflush(stdout);
        pid_t pid = fork();
        if (pid == 0) {
            alarm(CTEST_TIMEOUT);
            ctest_cases[i].fn();
            fflush(stdout);
            _exit(0);
        }
        int st = 0;
        waitpid(pid, &st, 0);
        if (WIFEXITED(st) && WEXITSTATUS(st) == 0) {
            printf("PASS %s\n", ctest_cases[i].name);
            passed++;
        } else if (WIFSIGNALED(st) && WTERMSIG(st) == SIGALRM) {
            printf("FAIL %s (timeout after %ds)\n", ctest_cases[i].name, CTEST_TIMEOUT);
            failed++;
        } else if (WIFSIGNALED(st)) {
            printf("FAIL %s (crashed: signal %d)\n", ctest_cases[i].name, WTERMSIG(st));
            failed++;
        } else if (WIFEXITED(st) && WEXITSTATUS(st) != CTEST_ASSERT_EXIT) {
            printf("FAIL %s (crashed: exit %d, see the sanitizer report above)\n", ctest_cases[i].name,
                   WEXITSTATUS(st));
            failed++;
        } else {
            printf("FAIL %s\n", ctest_cases[i].name);
            failed++;
        }
    }
    printf("ctest: %d passed, %d failed\n", passed, failed);
    return failed ? 1 : 0;
}
#endif
#endif
