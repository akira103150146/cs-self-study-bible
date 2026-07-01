# CS 自學聖經 · The Self-Taught Computer Scientist

一本由淺入深、**中英對照**、Medium 寫作風格的計算機科學自學教科書,依據
[OSSU Computer Science](https://github.com/ossu/computer-science) 課程大綱打造,
並整合 AP325、APCS、TOI 等完整題庫作為附錄。

> **開始閱讀:** 用瀏覽器打開 [`index.html`](index.html)。

## 這本書有什麼

- **18 部、73 章**:從「什麼是計算」到 Python、資料結構與演算法、計算機系統
  (NAND→CPU→OS→網路)、資訊安全、資料庫、機器學習、編譯器、計算理論、線性代數……
  每章都有學習目標、由淺入深的敘事、**C / C++ / Python** 範例、手繪內嵌 SVG 圖,
  以及附可展開解答的練習。
- **三條專修軌道**:競賽程式設計與 APCS、電腦視覺與影像辨識、實戰資安 CTF。
- **完整題庫附錄(依章節)**:
  - AP325 題單(110 題)
  - APCS 觀念題(125 題)、實作題(120 題)、模擬考卷(90 題)
  - TOI 題庫(368 題,可依組別/年份/搜尋過濾,其中 306 題收錄 OCR 全文題敘、
    301 題附 C++ 參考解)

## 目錄結構

```
index.html              首頁與完整課程地圖
chapters/               各章節 HTML(00–79)
assets/
  style.css             設計系統(淺/深雙主題)
  book.js               導覽引擎(側欄、目錄、進度、延遲載入)
  toi/                  TOI 題庫資料與渲染器(toi-index.js / toi-statements.js / toi-render.js)
_AUTHOR_GUIDE.md        章節撰寫規範
_build_toi_*.py         TOI 題庫的重建工具
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

以 ❤️ 與大量 `while True:` 寫成。
