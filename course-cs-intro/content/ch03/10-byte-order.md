---
id: C3.10
title_en: Byte Order (Endianness)
title_zh: 位元組順序
sub: Which byte of a multi-byte value comes first in memory
level: mid
supplement: true
lab_hook: "任務 9:`host_is_little()`、`bswap32()`、`read_le32()`、`read_be32()`、`write_le32()`"
---
## 觀念
A value wider than one byte (for example a 32-bit integer) occupies several consecutive memory addresses. **Byte order** (**endianness**) is the rule for which byte goes where:

- **Big-endian**: the **most** significant byte is stored at the lowest address. `0x12345678` is stored as `12 34 56 78`.
- **Little-endian**: the **least** significant byte is stored at the lowest address. `0x12345678` is stored as `78 56 34 12`.

x86 and (in practice) ARM CPUs are little-endian. Internet protocols use big-endian, called **network byte order**. File formats choose one and document it: BMP and WAV headers are little-endian; PNG is big-endian. Code that reads a binary file must assemble multi-byte fields in the file's byte order, not the CPU's.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| byte order / endianness | 位元組順序 | 多位元組的值在記憶體中的排列順序 |
| big-endian | 大端序 | 高位位元組放在低位址 |
| little-endian | 小端序 | 低位位元組放在低位址 |
| network byte order | 網路位元組順序 | 網路協定規定的大端序 |
| byte swap | 位元組交換 | 把位元組順序顛倒 |

## 白話說
寫「一千二百三十四」,我們先寫千位(1234)——這就像大端序。小端序則是先寫個位、倒著寫(4321)。兩種都行,只要讀寫雙方講好。

麻煩出在「沒講好」:你在 x86(小端)上把一個整數直接寫進檔案,拿到大端機器上讀就會變成完全不同的數。所以讀二進位檔一定要照**檔案規定的順序**一個位元組一個位元組組起來。

## 後面會用到
- **計算機組織**:記憶體排列、`objdump` 看到的立即值順序。
- **計算機網路**:`htonl` / `ntohl` 在主機與網路順序間轉換(第 15 章)。
- 本章 Lab:讀 BMP/WAV 的檔頭(小端序)。

## 原理
**用移位組合就不必管主機順序。** 從位元組陣列 `p` 讀小端 32 位元:

$$v = p_0 + p_1 \cdot 2^8 + p_2 \cdot 2^{16} + p_3 \cdot 2^{24}$$

在 C 裡寫成 `p[0] | p[1] << 8 | p[2] << 16 | (uint32_t)p[3] << 24`。這只用到算術,不管程式跑在大端或小端的 CPU 上,結果都一樣。反之,用 `*(uint32_t *)p` 直接讀,結果取決於主機的位元組順序(而且可能違反對齊規則)。

**如何判斷主機順序?** 存一個整數 1,看它的第一個位元組是不是 1:是 → 小端。

## 老師講解
### 例 1
Show how `0x0A0B0C0D` is laid out at addresses 100–103 on a big-endian and on a little-endian machine.

1. 最高位位元組是 `0A`,最低位是 `0D`。
2. **大端序**:位址 100 放最高位 → 100: `0A`、101: `0B`、102: `0C`、103: `0D`。
3. **小端序**:位址 100 放最低位 → 100: `0D`、101: `0C`、102: `0B`、103: `0A`。
4. 口訣:小端序「小的(低位)在小位址」。

### 例 2
The first bytes of a BMP file are `42 4D 36 00 0C 00 …`. Bytes 2–5 are the file size as a little-endian 32-bit integer. What is the file size?

1. 取第 2–5 個位元組:`36 00 0C 00`。
2. 小端序:第一個是最低位。值 $= \text{0x36} + \text{0x00} \cdot 2^8 + \text{0x0C} \cdot 2^{16} + \text{0x00} \cdot 2^{24}$。
3. $= 54 + 12 \times 65536 = 786{,}486$ 位元組。
4. 合理性檢查:$786486 - 54 = 786432 = 512 \times 512 \times 3$,正好是一張 512 × 512 全彩影像加上 54 位元組的檔頭。

## 易錯點
- 以為位元組內的**位元**順序也會顛倒:不會,位元組順序只影響位元組的排列。
- 用指標轉型直接讀檔案裡的多位元組欄位。
- 以為所有檔案格式都是小端序(PNG、JPEG、網路協定都是大端序)。

## 教學提示
這是補充觀念,但 Lab 讀 BMP/WAV 一定會碰到。可以現場用 `printf '\x01\x00\x00\x00' | od -An -t d4` 在 x86 上印出 1,換成 `od -t d4 --endian=big` 印出 16777216。

## 練習
### 照做
Write the bytes of `0x1234` (16 bits) in big-endian and in little-endian order.

#### 解答
大端:`12 34`;小端:`34 12`。

### 是非
True or false: On a little-endian machine, the bits inside each byte are also reversed.

#### 解答
False。位元組順序只決定多個位元組的排列,單一位元組內的位元順序不變。

### 變化
The bytes `78 56 34 12` are read as a 32-bit integer. What is its value (in hexadecimal) if interpreted as little-endian? As big-endian?

#### 解答
小端:`0x12345678`;大端:`0x78563412`。

### 應用
A WAV header stores the sample rate as the little-endian bytes `44 AC 00 00`. What is the sample rate?

#### 解答
`0x0000AC44` = 44,100 Hz。

### 挑戰
Write an expression in C that reverses the byte order of a 32-bit value `x` using only shifts, masks, and OR.

#### 解答
`(x >> 24) | ((x >> 8) & 0x0000FF00) | ((x << 8) & 0x00FF0000) | (x << 24)`(`x` 必須是無號型別,例如 `uint32_t`)。

## 驗算
```check
bytes.fromhex("0A0B0C0D") == (0x0A0B0C0D).to_bytes(4, "big")
int.from_bytes(bytes.fromhex("36000C00"), "little") == 786486 and 786486 - 54 == 512 * 512 * 3
int.from_bytes(bytes.fromhex("78563412"), "little") == 0x12345678
int.from_bytes(bytes.fromhex("78563412"), "big") == 0x78563412
int.from_bytes(bytes.fromhex("44AC0000"), "little") == 44100
```
