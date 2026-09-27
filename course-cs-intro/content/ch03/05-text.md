---
id: C3.5
title_en: Representing Text
title_zh: 文字的表示
sub: Character sets — ASCII, Unicode, and the UTF-8 encoding
level: mid
lab_hook: "任務 4:`utf8_encode()`、`utf8_decode()`、`utf8_count()`、`ascii_toggle_case()`"
---
## 觀念
To represent text, we list every character we need in a **character set** and give each one a number (its **code point**). The text is then stored as a sequence of those numbers.

**ASCII** uses 7 bits: 128 characters — control characters (0–31, e.g. 10 = newline), the space (32), digits `'0'`–`'9'` (48–57), uppercase `'A'`–`'Z'` (65–90), lowercase `'a'`–`'z'` (97–122), and punctuation. Upper- and lowercase letters differ by exactly 32, i.e. by one bit (`0x20`).

**Unicode** assigns a code point to every character of every writing system — over 150,000 characters, written `U+4E2D` (中), `U+1F600` (😀). The first 128 code points are the same as ASCII.

A code point must still be turned into bytes; that is the job of an **encoding**. **UTF-8** is the dominant encoding on the Web:

| Code point range | Bytes | Bit pattern |
|---|---|---|
| U+0000 – U+007F | 1 | `0xxxxxxx` |
| U+0080 – U+07FF | 2 | `110xxxxx 10xxxxxx` |
| U+0800 – U+FFFF | 3 | `1110xxxx 10xxxxxx 10xxxxxx` |
| U+10000 – U+10FFFF | 4 | `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx` |

The `x` bits are the code point's bits, most significant first. Rules: ASCII text is valid UTF-8 unchanged; every continuation byte starts with `10`; a character must use the **shortest** possible form (an **overlong** encoding such as `C0 80` for U+0000 is invalid); code points U+D800–U+DFFF (**surrogates**) are not allowed.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| character set | 字元集 | 所有字元與它們的編號 |
| code point | 碼位 | 一個字元在 Unicode 裡的編號,如 U+4E2D |
| encoding | 編碼方式 | 把碼位變成位元組的規則,如 UTF-8、UTF-16 |
| ASCII | ASCII | 7 位元、128 個字元的美國標準字元集 |
| Unicode | 萬國碼 | 涵蓋全世界文字的字元集 |
| UTF-8 | UTF-8 | 1–4 位元組的可變長度編碼,相容 ASCII |
| continuation byte | 延續位元組 | 多位元組字元中 `10` 開頭的後續位元組 |
| overlong encoding | 過長編碼 | 用比必要還多的位元組表示字元,不合法 |

## 白話說
「文字」在電腦裡就是一串數字。問題是:誰來規定「中」是幾號?這就是字元集(Unicode 說:U+4E2D)。第二個問題:4E2D 這個數字要存成哪幾個位元組?這就是編碼(UTF-8 說:`E4 B8 AD`)。

UTF-8 聰明的地方:英文字還是一個位元組、和 ASCII 一模一樣;中文字三個位元組;emoji 四個。而且每個位元組看開頭就知道自己是「字的開頭」還是「字的中間」,就算從中間開始讀也能重新對齊。

## 後面會用到
- **程式設計**:C 的 `strlen` 算的是位元組數,不是字數;Python 3 的 `str` 以碼位為單位。
- **計算機網路**、**Web**:HTTP 標頭的 `charset=utf-8`、網頁亂碼的來源(第 16 章)。
- **資訊安全**:接受過長編碼的解碼器曾被用來繞過 `../` 路徑檢查。

## 現代補充
- **UTF-16**(Java、JavaScript、Windows 內部使用)用 2 或 4 個位元組;超過 U+FFFF 的字元(例如 emoji)要用一對 **surrogate** 表示,這就是 JavaScript 的 `"😀".length` 是 2 的原因。
- 一個「看起來的字」(grapheme)可能由好幾個碼位組成:👨‍👩‍👧 是 5 個碼位(三個人 + 兩個 zero-width joiner)。延伸專案 4 會探討。

## 原理
**為什麼 UTF-8 可以自我同步(self-synchronizing)?** 開頭位元組的樣子(`0`、`110`、`1110`、`11110`)和延續位元組(`10`)互不相同。從任何位置開始讀,只要跳過 `10` 開頭的位元組,就一定落在某個字元的開頭。

**為什麼要禁止過長編碼?** 若允許 `C0 AF` 也代表 `/`(U+002F),檢查「字串裡有沒有 `/`」的程式可能只比對單一位元組 `2F` 而漏掉它,解碼後卻得到 `/`。規定每個字元只有唯一的最短編碼,比較位元組就等於比較字元。

**UTF-8 的排序性質**:把 UTF-8 位元組串當成無號位元組逐一比較,得到的順序和碼位順序相同——資料庫與搜尋很依賴這一點。

## 老師講解
### 例 1
Encode 中 (U+4E2D) in UTF-8.

1. **判斷長度**:U+0800 ≤ 0x4E2D ≤ U+FFFF → 3 個位元組,樣板 `1110xxxx 10xxxxxx 10xxxxxx`,共 16 個 x。
2. **寫出 16 位元**:0x4E2D = `0100 1110 0010 1101`。
3. **從高位依序填入**:前 4 位 `0100` → `11100100` = E4;接著 6 位 `111000` → `10111000` = B8;最後 6 位 `101101` → `10101101` = AD。
4. 結果 `E4 B8 AD`。用 Python 驗證:`"中".encode("utf-8").hex()` → `e4b8ad`。

### 例 2
Decode the bytes `F0 9F 98 80`, and explain why `C0 80` is rejected.

1. `F0` = `11110000` → 4 位元組字元,取出 `000`。
2. 三個延續位元組 `9F` = `10011111` → `011111`;`98` = `10011000` → `011000`;`80` = `10000000` → `000000`。
3. 串起來:`000 011111 011000 000000` = `0 0001 1111 0110 0000 0000` = 0x1F600 → 😀。
4. `C0 80`:`110 00000` + `10 000000` 算出來是 U+0000,但 U+0000 只需要 1 個位元組(`00`)。用 2 個位元組是**過長編碼**,依規定必須拒絕。

## 易錯點
- 從低位開始填 x:要從高位依序填。
- 以為中文字一定是 2 個位元組:在 UTF-8 是 3 個(那是 Big5 / UTF-16 的印象)。
- 把 `strlen` 當成字數。
- 大小寫互換用「加減 32」而沒有先判斷是不是字母。

## 教學提示
現場示範 `printf '中' | xxd`,再請學生手算例 1。Lab 任務 4 的隱藏測試包含過長編碼、surrogate、超過 U+10FFFF、截斷的序列——可以先讓學生列出「哪些位元組序列不合法」再開始寫。

## 練習
### 照做
Give the ASCII codes (in decimal) of `'A'`, `'a'`, `'0'`, and the space character.

#### 解答
65、97、48、32。

### 是非
True or false: Every valid ASCII file is also a valid UTF-8 file with the same meaning.

#### 解答
True。ASCII 的 0–127 在 UTF-8 中就是單一位元組 `0xxxxxxx`,完全相同。

### 變化
Encode é (U+00E9) in UTF-8.

#### 解答
U+0080–07FF → 2 位元組。0xE9 = `000 1110 1001` → 11 位元 `00011 101001` → `11000011` `10101001` = `C3 A9`。

### 應用
A C program calls `strlen("中文😀")` on a UTF-8 string. What does it return, and how many characters (code points) does the string have?

#### 解答
中 3 + 文 3 + 😀 4 = 10 個位元組,所以 `strlen` 回傳 10;碼位數是 3。

### 挑戰
Why does flipping bit 5 (`c ^ 0x20`) toggle the case of an ASCII letter? Why must you check that `c` is a letter first?

#### 解答
'A'–'Z' 是 0x41–0x5A,'a'–'z' 是 0x61–0x7A,兩者差 0x20,也就是只差第 5 位元。XOR 0x20 就在兩者之間切換。但對非字母也會改變它:'@'(0x40)會變成 '`'(0x60)、'1'(0x31)會變成 0x11(控制字元),所以必須先確認是字母。

## 驗算
```check
utf8_hex("中") == "E4 B8 AD" and utf8_hex("é") == "C3 A9" and utf8_hex("😀") == "F0 9F 98 80"
[ord(c) for c in "Aa0 "] == [65, 97, 48, 32]
len("中文😀".encode("utf-8")) == 10 and len("中文😀") == 3
chr(ord("A") ^ 0x20) == "a" and chr(ord("@") ^ 0x20) == "`"
0x4E2D == int("0100111000101101", 2)
```
