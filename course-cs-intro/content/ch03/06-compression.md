---
id: C3.6
title_en: Text Compression
title_zh: 文字壓縮
sub: Keyword encoding, run-length encoding, and Huffman codes
level: hard
lab_hook: "任務 5:`keyword_encode()`、`rle_encode()`/`rle_decode()`、`huff_compress()`/`huff_decompress()`"
---
## 觀念
**Data compression** reduces the amount of space needed to store a piece of data. The **compression ratio** is the size of the compressed data divided by the size of the original (smaller is better; 0.6 means 40% saved).

- **Lossless** compression can recover the original exactly (needed for text and programs).
- **Lossy** compression throws away some information that people are unlikely to notice (used for audio, images, video).

Three lossless techniques for text:

1. **Keyword encoding**: replace frequently used words with single characters that do not otherwise appear (for example `the` → `~`, `and` → `+`).
2. **Run-length encoding (RLE)**: replace a long run of a repeated character by a flag, the character, and the count. This course's rule: a run of 4–9 identical characters becomes `*` + the character + the count digit (`AAAAAAA` → `*A7`); longer runs are split into pieces of 9; runs shorter than 4 are left alone, because the code itself costs 3 characters.
3. **Huffman encoding**: give **shorter bit strings to more frequent characters**. Build the code by repeatedly merging the two least frequent nodes into a tree; the path from the root (0 = left, 1 = right) is each character's code. Huffman codes are **prefix codes**: no code is a prefix of another, so a bit stream can be decoded without separators.

![Huffman tree for frequencies A:5, B:2, C:1, D:1.](huffman-tree.svg)

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| data compression | 資料壓縮 | 用較少空間表示同樣的資料 |
| compression ratio | 壓縮比 | 壓縮後大小 ÷ 原大小 |
| lossless / lossy | 無損/有損 | 能否完全還原原始資料 |
| keyword encoding | 關鍵字編碼 | 常見的字換成單一符號 |
| run-length encoding (RLE) | 連續長度編碼 | 一串重複字元換成「字元 + 次數」 |
| Huffman encoding | 霍夫曼編碼 | 依出現頻率給變長編碼 |
| prefix code | 前綴碼 | 沒有任何碼是另一個碼的前綴 |

## 白話說
壓縮的本質是**找出重複與偏頗**。重複的整個字(keyword)、連續重複的字元(RLE)、某些字元特別常見(Huffman)——各抓一種。

Huffman 的直覺像摩斯電碼:最常用的字母 E 只有一個點。越常出現的字,碼越短,整體平均就短。建樹的方法很機械:每次把最不常見的兩個合成一組,直到剩一棵樹。

## 後面會用到
- **演算法**:Huffman 是**貪婪演算法**的經典例子,建樹要用**優先佇列**(heap)。
- **資料結構**:二元樹的走訪、位元層級的輸入輸出。
- **多媒體與網路**:ZIP、gzip、PNG 用 DEFLATE(LZ77 + Huffman);JPEG 與 MP3 最後一步也是 Huffman(延伸專案 1 會做 LZ77)。

## 原理
**為什麼前綴碼可以直接解碼?** 從根出發,讀一個位元走一步;碰到葉子就輸出那個字元、回到根。因為字元只在葉子,任何碼都不會是另一個碼的前綴,所以一走到葉子就可以確定。

**為什麼 Huffman 是最佳的?**(大意)編碼總長 $= \sum f_i \cdot \ell_i$($\ell_i$ 是深度)。最佳的前綴碼樹裡,兩個頻率最小的字元可以放在最深的一對兄弟葉子上(交換只會讓總長變短或不變)。把它們合成一個頻率為 $f_1 + f_2$ 的新字元後,原問題的最佳解等於「新問題的最佳解再加上 $f_1 + f_2$」。遞迴下去就是 Huffman 的做法。

由此也得到一個好算的公式:**總位元數 = 每次合併時兩個頻率之和的總和**(每次合併,子樹裡所有字元的碼都多一位)。

## 老師講解
### 例 1
Build a Huffman code for the text `AAAAABBCD` (A:5, B:2, C:1, D:1), and compute the encoded length. Compare with a fixed-length code.

1. **合併最小的兩個**:C(1) + D(1) → 2。剩 A5、B2、[CD]2。
2. 再合併最小的兩個:B(2) + [CD](2) → 4。剩 A5、[B CD]4。
3. 最後合併:A(5) + 4 → 9(根)。
4. **讀碼**(左 0 右 1):A = `0`、B = `10`、C = `110`、D = `111`。
5. **總長**:$5 \cdot 1 + 2 \cdot 2 + 1 \cdot 3 + 1 \cdot 3 = 15$ 位元。用合併公式驗算:$2 + 4 + 9 = 15$ ✓。
6. 固定長度:4 種字元要 2 位元,$9 \times 2 = 18$ 位元。Huffman 省了 3 位元(壓縮比 $15/18 \approx 0.83$)。

### 例 2
Apply this course's RLE to `AAAAAAAAAAAABBBCDDDDD` and compute the compression ratio.

1. 12 個 A:超過 9,切成 9 + 3。9 個 → `*A9`;剩 3 個少於 4,照原樣 `AAA`。
2. 3 個 B:少於 4 → `BBB`。1 個 C → `C`。
3. 5 個 D → `*D5`。
4. 結果 `*A9AAABBBC*D5`,長度 13;原文長度 21。
5. 壓縮比 $13 / 21 \approx 0.62$。

## 易錯點
- Huffman 合併時沒有每次都挑**當下**最小的兩個(新合成的節點也要參與比較)。
- 以為 Huffman 碼唯一:平手時可以有不同的樹,但**總位元數**相同。
- RLE 把少於 4 個的也編碼:`*B3` 比 `BBB` 還長。
- 壓縮比算反(原/壓縮)。

## 教學提示
例 1 可以讓學生用不同的平手選擇各建一棵樹,發現碼不同但總長一樣。Lab 任務 5 的 `hzip` 是真的能壓縮檔案的工具,隱藏測試包含空檔案、只有一種位元組、隨機位元組(壓不下去)——很好的邊界情況討論。

## 練習
### 照做
Encode `WWWWWWBWWWWB` with this course's RLE.

#### 解答
6 個 W → `*W6`;B;4 個 W → `*W4`;B。結果 `*W6B*W4B`。

### 是非
True or false: In a Huffman code, the most frequent character always gets the shortest code (or ties for shortest).

#### 解答
True。最常見的字元最晚被合併,深度最淺。

### 變化
For frequencies A:4, B:3, C:2, D:1, compute the total number of bits of the Huffman encoding.

#### 解答
合併:D1 + C2 = 3;B3 + [DC]3 = 6;A4 + 6 = 10。總位元 $3 + 6 + 10 = 19$。(碼長 A1、B2、C3、D3:$4 + 6 + 6 + 3 = 19$ ✓。)

### 應用
Which technique would work best for each: (a) a black-and-white fax page, (b) English prose, (c) a file of random bytes?

#### 解答
(a) RLE:大量連續的白點。(b) Huffman(或關鍵字編碼):字母頻率很不平均。(c) 都壓不下去:隨機資料沒有重複也沒有偏頗,壓縮後甚至會變大(要多存編碼表)。

### 挑戰
Let X = `0`, Y = `01`, Z = `10`. Show that this is not a prefix code, and give a bit string that can be decoded in two different ways.

#### 解答
`0`(X)是 `01`(Y)的前綴,所以不是前綴碼。字串 `010` 可以切成 `0|10` = XZ,也可以切成 `01|0` = YX——兩種都完全合法,解碼有歧義。前綴碼保證這種事不會發生。

#### 備註
注意:不是前綴碼不一定就有歧義(例如 `0`、`01`、`11` 從右邊解碼是唯一的),但前綴碼一定沒有歧義,而且可以一邊讀一邊解碼。

## 驗算
```check
huffman_bits({"A": 5, "B": 2, "C": 1, "D": 1}) == 15
rle("AAAAAAAAAAAABBBCDDDDD") == "*A9AAABBBC*D5" and len("*A9AAABBBC*D5") == 13
round(13 / 21, 2) == 0.62
rle("WWWWWWBWWWWB") == "*W6B*W4B"
huffman_bits({"A": 4, "B": 3, "C": 2, "D": 1}) == 19
```
