# 內容檔寫法

**內容只在 `content/` 與 `labs/` 改,版面只在 `_layout/templates/` 與 `assets/handout.css` 改。** 產出的 `chNN/*.html`、`chNN/*.zip`、`index.html` 不要手改,重建會覆蓋。

```
python _generators/build.py 3            # 重建第 3 章(首頁一律重建)
python _generators/verify.py 3           # 閘門 1:產出結構(兩版一致、學生版不洩答案、zip 乾淨)
python _generators/verify_answers.py 3   # 閘門 2:執行每個 ## 驗算 / ### 驗算
python _generators/run_labs.py 3         # 閘門 3:在 Docker 裡跑參考解與起始碼
python _generators/verify_coverage.py 3  # 閘門 4:每個觀念都有筆試題、Lab 任務、測試
python _generators/build_exam.py --chapters 2,3 --total 100 --seed 1 --name midterm
python -m pytest _generators/tests -q    # 產生器自己的測試
```

格式寫錯時 `build.py` 會直接停下來,並告訴你是哪個檔案、缺了什麼。

## 通用規則

- **講解與題目全部自編**,不引用課本原題與頁碼。
- **中文敘述;術語、觀念名、程式識別字用英文**,第一次出現附中文(例:two's complement 二補數)。題幹可以中英混寫。
- **數學式照常寫**:`$x < y$`。`< > &` 不用自己跳脫,程式會處理。
- **程式碼**用 fenced code(```c、```python、```text);行內用反引號。
- **圖**:單獨一行寫 `![圖說](檔名.svg)`,圖檔放同一章的 `figures/`(只能引用自己這一章的圖)。SVG 標籤用英文。
- **小題清單**:寫成 `- **a.** …`,清單前空一行、項目之間不空行(作答區高度就是數這些標號)。
- **表格儲存格裡不能出現 `|`**:位元 OR 寫成 `\|` 或改用文字 OR。
- 每個檔案的 `##`、`###` 標題是固定的,拼錯會報錯(這是故意的,避免內容悄悄消失)。
- 用 Claude 寫內容檔時請用檔案寫入工具,不要用 shell heredoc:heredoc 會把 `\\` 吃成 `\`。

## 一章的檔案

```
content/chNN/
  chapter.md         章資訊(只有 front matter)
  01-xxx.md …        觀念,一個觀念一個檔;檔名前兩位數 = 觀念序號
  bank.md            筆試題庫
  lab.md             核心 Lab 規格書
  projects.md        延伸專案
  figures/*.svg
labs/chNN/
  Makefile           從 labs/common/Makefile.c 或 Makefile.py 複製
  lab.mk             選用:這個 Lab 額外的 make 規則
  starter/src/       學生拿到的起始碼(TODO)
  solution/src/      參考解(不會進學生 zip)
  tests/public/      公開測試(會進學生 zip)
  tests/hidden/      隱藏測試(不會進學生 zip)
  data/              選用:測試資料
```

### chapter.md

```yaml
---
num: 3
title: Data Representation
title_zh: 資料表示
subtitle: 一句話副標
part: The Information Layer
book: CSI 7e Ch3(3.1–3.6)
lang: c              # c / python / mixed
followups: [計算機組織, 演算法]
---
```

### 觀念檔 `NN-slug.md`

front matter:`id`(必須等於 `C{章}.{NN}`)、`title_en`、`title_zh`、`level`(basic/mid/hard)、`lab_hook`(例:`"任務 2:\`to_twos()\`"`),選填 `sub`、`supplement: true`。

| 段落 | 必填 | 誰看得到 |
|---|---|---|
| `## 觀念` | ✓ | 兩版 |
| `## 名詞對照`(三欄表 English \| 中文 \| 說明) | ✓ | 兩版 |
| `## 白話說` | ✓ | 兩版 |
| `## 後面會用到`(哪門必修、用在哪) | ✓ | 兩版 |
| `## 現代補充` | | 兩版 |
| `## 原理` | ✓ | 教師版 |
| `## 老師講解`:`### 例 1`,題幹 + 至少兩步的編號清單,可加 `#### 備註` | ✓ | 兩版(備註只教師) |
| `## 易錯點`、`## 教學提示` | ✓ | 教師版 |
| `## 練習`:`### 照做 / 是非 / 變化 / 應用 / 挑戰`,各有 `#### 解答`,可加 `#### 備註`;第一題照做、順序不倒退 | ✓ | 解答只教師 |
| `## 驗算`:```check 區塊,每行一個 Python 運算式,結果必須是 `True` | | — |

### bank.md(筆試題庫)

```markdown
---
chapter: 3
---
## Q1 · C3.2 · 計算 · basic · 4
Convert −37 to 8-bit two's complement.

### 答案
`11011011`

### 詳解
1. …
2. …

### 驗算
```check
twos(-37, 8) == ANS
```
```

- 標題:`## Q<n> · <觀念 ID> · <計算|選擇|簡答> · <basic|mid|hard> · <配分 1–20>`,題號從 1 連號。
- **計算題**:`### 答案`、`### 詳解`、`### 驗算` 必填;驗算至少一行用到 `ANS`(= 答案的純文字,已去掉反引號)。驗算可以用 `_generators/checklib.py` 的函式(`to_base`、`twos`、`f32_bits`、`utf8_hex`、`rle`、`huffman_bits`、`pcm_bytes`、`image_bytes`、`bits_for` …)與 `math`、`struct`。
- **選擇題**:題幹後寫 `- A. …`(從 A 連續);`### 答案` 寫字母;`### 迷思對照` 每個錯誤選項一條:`- **B** 迷思 → 回看 C3.2`。
- **簡答題**:`### 答案`、`### 詳解`、`### 評分要點` 必填。

### lab.md

front matter `lang`、`dir`(例 `labs/ch03`)。段落:`## 概要`、`## 環境`、`## 任務 N · 標題 · C3.2, C3.3`(N 從 1 連號;本文要有一個 ```c interface 或 ```python interface 區塊,放這個任務要實作的宣告)、`## 繳交`。

### projects.md

`## 專案 N · 標題 · C3.6`,底下 `### 目標`、`### 規格`、`### 評分規準`(表頭固定 `項目 | 配分 | 通過標準`)必填,`### 延伸方向` 選填。

## Lab 測試的命名

測試名稱**以觀念 ID 開頭**,涵蓋度檢查與起始碼檢查都靠它:

- C:`TEST(C3_2_twos_negative)`(用 `labs/common/ctest.h`)
- Python:`def test_C2_4_add_carry():`

`run_labs.py` 會確認:參考解通過全部公開與隱藏測試;起始碼能編譯,而且每個任務至少有一個對應觀念的測試失敗(證明測試真的在測東西)。
