/* 任務 1 參考解:從標準輸入讀進所有整數,印出總和(沒有輸入時印 0)。 */
#include <stdio.h>

int main(void) {
    long long x, total = 0;
    while (scanf("%lld", &x) == 1) total += x;
    printf("%lld\n", total);
    return 0;
}
