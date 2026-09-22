# 內容檔寫法

**內容只在 `content/` 改,版面只在 `_layout/templates/` 與 `assets/handout.css` 改。** 產出的 `weekNN/*.html` 不要手改,重建會覆蓋。

```
python _generators/build.py 1        # 重建第 1 週(首頁一律重建)
python _generators/verify.py         # 閘門 1:結構(兩版一致、學生版不洩答案、作答區、TODO 數)
python _generators/verify_math.py    # 閘門 2:執行每個檔案 ## 驗算 裡的 sympy 式子
python _generators/run_notebooks.py  # 閘門 3:notebook 逐格實跑
```

格式寫錯時 `build.py` 會直接停下來,並告訴你是哪個檔案、缺了什麼。

## 通用規則

- **題目一律英文**:觀念陳述、例題題幹、練習題幹、診斷考題幹與選項。講解、解答、白話說明用中文。
- **數學式照常寫**:`$x < y$`、`$$\begin{bmatrix}1 & 2\\ 3 & 4\end{bmatrix}$$`。`< > &` 不用自己跳脫,程式會處理。
- 圖表(SVG、matplotlib)的標籤用英文,避免豆腐字。
- 每個檔案的 `##` 標題是固定的,拼錯會報錯(這是故意的,避免內容悄悄消失)。

## 一週的檔案

```
weekNN/
  week.md            本週標題、副標、Lay 節次
  lesson.md          理論教案
  01-xxx.md …        觀念,一個觀念一個檔,檔名前兩位數決定順序
  proof.md           證明時刻
  prereq.md          先備檢測(只有 W1)
  quiz.md            診斷考
  lab.md             實作
  figures/*.svg      觀念檔用 figure: 引用的圖
```

## week.md

```markdown
---
num: 1
title: 線性方程組與列化簡
subtitle: 一句話副標(可用 Markdown)
sections: Lay 1.1–1.2
chips: [學期地基]
---
```

## 觀念檔(01-xxx.md)

```markdown
---
title_en: Linear Systems and Their Solution Sets
title_zh: 線性方程組與解的三種情況
sub: 英文一句副標(選填)
level: basic                 # basic / mid / hard
lab_hook: "`np.linalg.solve`"   # 實作課會用到什麼(選填)
figure: three-cases.svg      # figures/ 裡的檔名(選填)
figure_caption: 圖說(選填)
---
## 觀念
英文核心陳述。

## 白話說
中文白話解釋,盡量不用符號。

## 在資工哪裡用
一兩句。

## 原理
只出現在教師版:為什麼成立、推導。

## 老師講解
### 例 1
英文題幹。

1. 第一步:在做什麼、為什麼。
2. 第二步……

### 例 2
……

## 易錯點
只出現在教師版。

## 教學提示
只出現在教師版:怎麼講給數理弱的學生聽。

## 練習
### 照做
英文題幹。

#### 解答
中文解答(只出現在教師版)。

### 變化
……

### 挑戰
……

## 驗算
```check
Matrix([[1, 1, 5], [1, -1, 1]]).rref()[0] == Matrix([[1, 0, 3], [0, 1, 2]])
```
```

- 老師講解每題至少兩步(`1.` `2.` 編號清單)。
- 練習第一題必須是「照做」,順序必須是 照做 → 變化 → 挑戰。
- `## 驗算` 每一行是一個會得到 `True` 的式子;可用 `x1`…`x6`、`x`、`y`、`z`、`t`、`s`、`h`、`k`。

## proof.md

```markdown
---
after: 2            # 放在第幾個觀念之後
title_zh: 列運算不改變解集
---
## 定理
英文敘述。
## 為什麼值得證
## 關鍵想法
## 證明
(只出現在教師版)
```

## quiz.md / prereq.md

```markdown
---
kind: 診斷考        # 或 先備檢測
when: 實作課開頭
minutes: 10
---
## Q1 · 觀念 1       # 先備檢測寫「## Q1 · 先備」
英文題幹。

- A. 選項
- B. 選項
- C. 選項

### 答案
A

### 為什麼
中文說明。

### 迷思對照
- **B** 以為兩條線一定會相交 → 觀念 1 的圖
- **C** 以為兩條方程式就有兩個解 → 觀念 1 的白話說
```

- 選擇題:**每個錯誤選項都要有一條迷思對照**,少一個就報錯。
- 簡答題:不寫選項,`### 答案` 寫答案;迷思對照的粗體寫「常見錯答」。

## lab.md

````markdown
## ① 預測 · 寫下你的預測
引言(Markdown)。

```python todo
# TODO 預測:……(每個 todo 區塊剛好一行 # TODO 開頭)
pred = None
```

## ② 計算 · 標題
引言。

```python
程式碼
```

```text expected
預期輸出
```

**會看到**:說明(第一個程式區塊之後的文字都放在這)。
````

- 標題的 ①②③④ 對應 預測/計算/解讀/應用,順序不能倒,四個階段都要有。
- 每個步驟最多一個 ```python 和一個 ```python todo。
- 學生不手刻演算法;需要示範機制時,由老師寫好短函式放在 ```python 裡。
