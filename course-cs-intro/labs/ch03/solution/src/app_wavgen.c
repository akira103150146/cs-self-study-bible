/* wavgen — 產生一個正弦波 WAV 檔(已經寫好,不要改)。
 *   wavgen 頻率 取樣率 位元數 秒數 輸出檔     例:wavgen 440 44100 16 2 a440.wav
 */
#include <stdio.h>
#include <stdlib.h>

#include "audio.h"

int main(int argc, char **argv) {
    if (argc != 6) {
        fprintf(stderr, "usage: wavgen FREQ RATE BITS SECONDS OUT.wav\n");
        return 2;
    }
    double freq = atof(argv[1]), secs = atof(argv[4]);
    int rate = atoi(argv[2]), bits = atoi(argv[3]);
    size_t cap = (size_t)(rate * secs) + 2;
    int32_t *s = malloc(cap * sizeof *s);
    size_t n = synth_sine(freq, rate, secs, bits, s, cap);
    if (n == 0 || wav_write(argv[5], s, n, rate, bits) != 0) {
        fprintf(stderr, "wavgen: failed\n");
        return 1;
    }
    printf("%zu samples, %llu bytes of PCM; you should hear %.1f Hz\n", n,
           (unsigned long long)pcm_bytes(rate, bits, 1, secs), alias_freq(freq, rate));
    free(s);
    return 0;
}
