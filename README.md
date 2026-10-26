# CS 自學聖經 · The Self-Taught Computer Scientist

一本由淺入深、**中英對照**、Medium 寫作風格的計算機科學自學教科書,依據
[OSSU Computer Science](https://github.com/ossu/computer-science) 課程大綱打造,
並整合 AP325、APCS、TOI 等完整題庫作為附錄。

> **開始閱讀:** 用瀏覽器打開 [`index.html`](index.html)。

## 這本書有什麼

- **序章＋27 部、124 章**,外加 1 章不編號的橋接章(讀懂 C)、6 份附錄題庫與 1 份速查附錄(附錄 G:Hack HDL):從「什麼是計算」到 Python、資料結構與演算法、計算機系統
  (NAND→CPU→OS)、網路與資訊安全、資料庫、機器學習、編譯器、計算理論、線性代數……
  每章都有學習目標、由淺入深的敘事、**C / C++ / Python** 範例、手繪內嵌 SVG 圖,
  以及附可展開解答的練習。
- **專修軌道與進階延伸**:競賽程式設計與 APCS、電腦視覺與影像辨識、實戰資安 CTF,
  以及 SICP、Rust、容器與雲原生、LLM Agent、進階 AI、GPU 與 WASM、八個實戰專題。
- **完整題庫附錄(依章節)**:
  - AP325 題單(110 題)
  - APCS 觀念題(125 題)、實作題(120 題)、模擬考卷(90 題)
  - TOI 題庫(368 題,可依組別/年份/搜尋過濾,其中 306 題收錄 OCR 全文題敘、
    301 題附 C++ 參考解)

## 目錄結構

```
index.html              首頁與完整課程地圖
chapters/               各章節 HTML(檔名 00–128;src/ 是來源片段,build.py 產生外層)
assets/
  style.css             設計系統(淺/深雙主題)
  book.js               導覽引擎(側欄、目錄、進度、延遲載入)
  routes.js             「依路線」側欄的資料(_build_routes.py 產生)
  toi/                  TOI 題庫資料與渲染器(toi-index.js / toi-statements.js / toi-render.js)
_AUTHOR_GUIDE.md        章節撰寫規範
_build_toi_*.py         TOI 題庫的重建工具
_check_chapter_refs.py   章號與章際連結檢查(以 book.js 的顯示章號為準;擋裸寫的「第 N 章」與錯的記號)
_chapter_tokens.py       章號記號 {{ch:<id>}} 等的代入(build.py 用)與裸章號搜尋
_chapter_refs_allowlist.txt  刻意保留的裸章號(外部書目、附錄題庫的原書章次)
_tokenize_chapter_refs.py    一次性工具:把內文寫死的章號改成記號(2026-10 已執行)
_build_routes.py         由職業技能樹 tree.yaml 產生 assets/routes.js 與 8 份路線導讀(chapters/src/route-*.html)
_book_headings.py        上面兩支工具共用:讀 book.js、各章 h2/h3 錨點(sec-N)的計算
```

## 效能

字型以 `preconnect` + `display=swap` 精簡字重載入;長頁面用 `content-visibility`
跳過離屏排版;程式碼語法上色與數學公式(MathJax)採延遲處理(進視窗或展開才執行);
捲動進度條以 `requestAnimationFrame` 節流。離線亦可閱讀(字型、語法上色、數學公式會
優雅降級)。

## 授權與致謝

- 課程結構參考 **OSSU Computer Science**(MIT License)。
- 題庫與外部課程內容之著作權**歸原作者所有**(AP325 © 吳邦一教授;TOI © 官方;
  APCS © 大學程式設計先修檢測),本書僅為個人學習與教學用途整理彙整,請勿作公開散布或商業用途。
- 本書為教學用途之衍生著作。

### 第三方程式與資料

- **micrograd**(深度學習數學那一章〈動手實驗室:一百行寫出自動微分引擎〉的 `Value`、`Neuron`、`Layer`、`MLP` 改寫自它):<https://github.com/karpathy/micrograd>,MIT 授權。授權全文:

  ```text
  MIT License

  Copyright (c) 2020 Andrej Karpathy

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```
- **ML-For-Beginners**(NumPy 與 pandas 一章改寫了 `2-Regression` 的資料整理範例):<https://github.com/microsoft/ML-For-Beginners>,Copyright (c) Microsoft Corporation,MIT 授權:

  ```text
  MIT License

  Copyright (c) Microsoft Corporation.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```
- **Optical Recognition of Handwritten Digits**(任務線 nn 的 Boss 戰資料):E. Alpaydin、C. Kaynak,UCI Machine Learning Repository,doi:[10.24432/C50P49](https://doi.org/10.24432/C50P49),授權 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。改動:把原本的 `optdigits.tra` 與 `optdigits.tes` 合併成 5,620 張,再用固定的亂數重新切成公開的 4,000 張與隱藏的 1,620 張。程式地下城的任務資料夾 `data/` 也附同樣的出處說明。

以 ❤️ 與大量 `while True:` 寫成。
