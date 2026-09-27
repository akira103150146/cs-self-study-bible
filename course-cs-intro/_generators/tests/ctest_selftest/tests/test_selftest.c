#include "ctest.h"
#include <stdlib.h>

TEST(C9_1_passes) {
    ASSERT_EQ_INT(4, 2 + 2);
    ASSERT_EQ_STR("ab", "ab");
    ASSERT_NEAR(0.3, 0.1 + 0.2, 1e-12);
}
TEST(C9_1_fails_eq) { ASSERT_EQ_INT(5, 2 + 2); }
TEST(C9_1_segfault) {
    volatile int *p = NULL;
    *p = 1;
}
TEST(C9_1_infinite) {
    for (;;) {
    }
}
TEST(C9_1_after_crash) { ASSERT_TRUE(1); }
