"""產生第 3 章 Lab 的測試資料(english.txt 是手寫的,不在這裡產生)。

執行:python make_data.py(在這個資料夾裡)。產出的檔案都進版控,學生不需要執行它。
"""
import os
import random
import struct

HERE = os.path.dirname(os.path.abspath(__file__))


def out(name, data):
    with open(os.path.join(HERE, name), "wb") as f:
        f.write(data)


def bmp(width, height, pixel, bpp=24, top_down=False):
    """pixel(x, y) → (R, G, B),y = 0 是最上面一列。"""
    bytes_pp = bpp // 8
    row = (width * bytes_pp + 3) // 4 * 4
    rows = []
    for y in range(height):
        r = bytearray()
        for x in range(width):
            R, G, B = pixel(x, y)
            r += bytes((B, G, R)) + (b"\xff" if bytes_pp == 4 else b"")
        rows.append(bytes(r) + bytes(row - len(r)))
    if not top_down:
        rows.reverse()                                  # BMP 預設由下而上存
    data = b"".join(rows)
    header = struct.pack("<2sIHHI", b"BM", 54 + len(data), 0, 0, 54)
    dib = struct.pack("<IiiHHIIiiII", 40, width, -height if top_down else height, 1, bpp, 0,
                      len(data), 2835, 2835, 0, 0)
    return header + dib + data


TINY = [[(255, 0, 0), (0, 255, 0), (0, 0, 255)],
        [(255, 255, 0), (0, 0, 0), (255, 255, 255)]]


def main():
    out("same.bin", b"\x41" * 4096)
    out("random.bin", random.Random(2024).randbytes(4096))
    out("tiny3x2.bmp", bmp(3, 2, lambda x, y: TINY[y][x]))
    out("topdown3x2.bmp", bmp(3, 2, lambda x, y: TINY[y][x], top_down=True))
    out("gradient.bmp", bmp(101, 50, lambda x, y: ((x * 2) % 256, y * 5, 128)))
    out("bpp32.bmp", bmp(2, 2, lambda x, y: (1, 2, 3), bpp=32))
    print("ok")


if __name__ == "__main__":
    main()
