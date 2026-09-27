/* baseconv — 指令列工具(已經寫好,不要改)。
 *   baseconv VALUE FROM TO        例:baseconv 255 10 2
 *   baseconv add|sub|mul A B BASE 例:baseconv add ff 1 16
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "base.h"

static int usage(void) {
    fprintf(stderr, "usage: baseconv VALUE FROM TO\n       baseconv add|sub|mul A B BASE\n");
    return 2;
}

int main(int argc, char **argv) {
    char out[4096];
    if (argc == 5) {
        int base = atoi(argv[4]), n = -1;
        if (strcmp(argv[1], "add") == 0) n = add_in_base(argv[2], argv[3], base, out, sizeof out);
        else if (strcmp(argv[1], "sub") == 0) n = sub_in_base(argv[2], argv[3], base, out, sizeof out);
        else if (strcmp(argv[1], "mul") == 0) n = mul_in_base(argv[2], argv[3], base, out, sizeof out);
        else return usage();
        if (n < 0) { fprintf(stderr, "error\n"); return 1; }
        printf("%s\n", out);
        return 0;
    }
    if (argc != 4) return usage();
    uint64_t v;
    int r = parse_base(argv[1], atoi(argv[2]), &v);
    if (r == -2) { fprintf(stderr, "overflow: more than 64 bits\n"); return 1; }
    if (r != 0) { fprintf(stderr, "invalid number or base\n"); return 1; }
    if (to_base(v, atoi(argv[3]), out, sizeof out) < 0) { fprintf(stderr, "invalid base\n"); return 1; }
    printf("%s\n", out);
    return 0;
}
