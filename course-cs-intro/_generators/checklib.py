# -*- coding: utf-8 -*-
"""驗算用的獨立參考實作(給 ## 驗算 / ### 驗算 用)。

刻意**不** import 任何 Lab 的程式:題目答案要由另一份獨立寫的程式算一次來比對,
而不是拿 Lab 參考解驗證它自己。能用標準函式庫(struct、int(s, b)、str.encode)的地方都用標準函式庫。
"""
import heapq
import math
import struct

__all__ = ["to_base", "from_base", "twos", "ones", "signmag", "from_twos",
           "f32_bits", "f32_fields", "f32_from_bits", "utf8_hex", "rle", "huffman_bits",
           "pcm_bytes", "image_bytes", "bits_for"]

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, b):
    """非負整數 → 基底 b 的字串(小寫字母)。"""
    if not 2 <= b <= 36 or n < 0:
        raise ValueError("base 2–36, n ≥ 0")
    out = ""
    while True:
        n, r = divmod(n, b)
        out = _DIGITS[r] + out
        if n == 0:
            return out


def from_base(s, b):
    return int(s, b)


def _check_range(v, lo, hi, bits):
    if not lo <= v <= hi:
        raise ValueError(f"{v} 超出 {bits} 位元範圍 [{lo}, {hi}]")


def twos(v, bits):
    """整數 → bits 位元二補數字串。"""
    _check_range(v, -(1 << (bits - 1)), (1 << (bits - 1)) - 1, bits)
    return format(v & ((1 << bits) - 1), f"0{bits}b")


def ones(v, bits):
    """整數 → bits 位元一補數字串(負數 = 絕對值逐位元反轉)。"""
    _check_range(v, -((1 << (bits - 1)) - 1), (1 << (bits - 1)) - 1, bits)
    return format(v if v >= 0 else ((1 << bits) - 1) ^ (-v), f"0{bits}b")


def signmag(v, bits):
    """整數 → bits 位元符號大小字串。"""
    _check_range(v, -((1 << (bits - 1)) - 1), (1 << (bits - 1)) - 1, bits)
    return ("1" if v < 0 else "0") + format(abs(v), f"0{bits - 1}b")


def from_twos(s):
    v = int(s, 2)
    return v - (1 << len(s)) if s[0] == "1" else v


def f32_bits(x):
    """Python float → IEEE 754 單精度的 32 個位元(字串)。"""
    return format(struct.unpack(">I", struct.pack(">f", x))[0], "032b")


def f32_fields(x):
    """→ (sign, 指數欄位的值, fraction 欄位的值)。"""
    b = f32_bits(x)
    return int(b[0]), int(b[1:9], 2), int(b[9:], 2)


def f32_from_bits(s):
    return struct.unpack(">f", struct.pack(">I", int(s, 2)))[0]


def utf8_hex(s):
    """字串 → UTF-8 位元組的十六進位(大寫、空白分隔),例:'中' → 'E4 B8 AD'。"""
    return " ".join(f"{b:02X}" for b in s.encode("utf-8"))


def rle(s):
    """本課的 RLE:連續 4–9 個相同字元編成 * + 字元 + 個數;超過 9 個先切成 9 個一段;少於 4 個照原樣。"""
    if "*" in s:
        raise ValueError("RLE 原文不得含 *")
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        run = j - i
        while run > 0:
            k = min(run, 9)
            out.append(f"*{s[i]}{k}" if k >= 4 else s[i] * k)
            run -= k
        i = j
    return "".join(out)


def huffman_bits(freq):
    """{符號: 次數} → 最佳 Huffman 編碼的總位元數(與樹的平手順序無關)。只有一種符號時每個 1 位元。"""
    counts = [c for c in freq.values() if c > 0]
    if len(counts) == 1:
        return counts[0]
    heapq.heapify(counts)
    total = 0
    while len(counts) > 1:
        a, b = heapq.heappop(counts), heapq.heappop(counts)
        total += a + b
        heapq.heappush(counts, a + b)
    return total


def pcm_bytes(rate, bits, channels, seconds):
    """未壓縮 PCM 的位元組數。"""
    return int(rate * bits * channels * seconds) // 8


def image_bytes(w, h, bpp):
    """未壓縮點陣圖的位元組數(不含檔頭、不含每列補齊)。"""
    return w * h * bpp // 8


def bits_for(n_items):
    """要區分 n 種東西至少要幾個位元(n = 1 時算 1)。"""
    return max(1, math.ceil(math.log2(n_items)))
