---
lang: mixed
dir: labs/ch01
---
## 概要
這個 Lab 讓你把第 1 章的每個觀念都親手做一次:用 C 與 Python 寫同一支程式,再把 C 程式**一層一層往下拆**直到機器碼;在一顆「很難用的硬體」上蓋一層**抽象**;把計算的**歷史當成資料**來分析;最後寫一支檢查**工具鏈**的腳本。

完成後你會有:`src/sum.c`、`src/sum.py`、`src/pipeline.mk`、`src/layers.md`、`src/kvstore.py`、`src/timeline.py`、`src/toolcheck.sh`。

## 環境
所有 Lab 都在課程的 Docker 映像檔裡執行(老師會提供 `cs-intro-env`,或用 `course-cs-intro/env/Dockerfile` 自己建):

```text
docker run --rm -it -v "$PWD:/work" cs-intro-env bash
make build     # 編譯 sum.c、檢查 Python 語法
make pipeline  # 任務 2
make test      # 跑全部公開測試
```

測試用 pytest。只跑一個任務的測試:`PYTHONPATH=src python3 -m pytest -q tests -k C1_2`。

## 任務 1 · 同一支程式,兩種語言 · C1.1
在 `src/sum.c` 與 `src/sum.py` 寫出**行為完全相同**的程式:從標準輸入讀進所有整數(以空白或換行分隔),印出總和;沒有輸入時印 `0`。數字可能是負數,也可能大到 $10^{12}$(C 要選對型別)。

```c interface
int main(void);   /* src/sum.c:讀 stdin 的所有整數,印出總和與換行 */
```

範例:

```text
$ printf "1 2 3\n-4 10\n" | ./build/sum
12
$ printf "" | python3 src/sum.py
0
```

## 任務 2 · 往下看每一層 · C1.1, C1.4
完成 `src/pipeline.mk` 的 `pipeline` 目標,把 `src/sum.c` 一步一步往下拆,每一步產生一個檔案:

```python interface
# make pipeline 必須產生:
#   build/sum.i        前處理(gcc -E)
#   build/sum.s        組合語言(gcc -S,從 sum.i 來)
#   build/sum.o        目的檔(gcc -c,從 sum.s 來)
#   build/sum.linked   連結後的執行檔(從 sum.o 來)
#   build/sum.dis      反組譯(objdump -d build/sum.o)
#   build/sum.pyc.txt  Python bytecode(python3 -m dis src/sum.py)
```

然後在 `src/layers.md` 的六個固定標題(Application、High-level language、Assembly、Machine code、Operating system、Hardware)底下,各寫至少 40 個字,說明你的程式在那一層長什麼樣子。High-level language、Assembly、Machine code 三段要各用反引號**引用一行真的出現在** `src/sum.c`、`build/sum.s`、`build/sum.dis` 裡的內容,並解釋它。

提示:用 `file build/sum.o build/sum.linked` 看兩者的差別;Makefile 的指令行開頭必須是 Tab。

## 任務 3 · 抽象的價值 · C1.2
`src/rawdisk.py` 模擬一顆很難用的「硬體」:只能一次讀寫一整個區塊,區塊大小每顆 disk 可能不同。請在 `src/kvstore.py` 實作 `KVStore`,讓使用者完全不用知道區塊的存在。

```python interface
class KVStore:
    def __init__(self, disk: RawDisk): ...
    def put(self, key: str, value: bytes) -> None: ...
    def get(self, key: str) -> bytes: ...        # 不存在:KeyError
    def delete(self, key: str) -> None: ...      # 不存在:KeyError
    def keys(self) -> list: ...
```

要求:

- 資料必須**真的存在 disk 上**:用同一顆 disk 再建一個 `KVStore`,要讀得到之前存的東西。
- **不能假設區塊大小**:同一段使用者程式,換一顆 `block_size` 不同的 disk 也要能跑。
- 值可能比一個區塊大很多。

## 任務 4 · 計算的歷史是資料 · C1.3, C1.4
在 `src/timeline.py` 實作下列函式,世代的定義見講義 C1.3、C1.4(邊界年份屬於新世代,1951 之前為 0):

```python interface
def hardware_generation(year: int) -> int: ...          # 0–4
def software_generation(year: int) -> int: ...          # 0–5
def load(path: str) -> list: ...                        # 讀 data/milestones.csv
def by_generation(rows: list, kind: str) -> dict: ...   # {世代: [名稱…]},依年份排序
def moore(year: int, base_year: int = 1971, base: int = 2300) -> int: ...
```

`data/milestones.csv` 的欄位是 `year,name,kind,transistors`,`kind` 是 `hardware`、`software` 或 `cpu`(只有 `cpu` 列有電晶體數)。`moore()` 用「每兩年加倍」的模型,回傳四捨五入的整數。

## 任務 5 · 你的工具鏈 · C1.5
寫 `src/toolcheck.sh`:依序檢查 `gcc`、`make`、`python3`、`git`、`gdb`。找得到就印 `工具名: 版本資訊的第一行`,找不到就印 `工具名: MISSING`;五個都檢查完才結束,有任何一個 MISSING 就 `exit 1`,否則 `exit 0`。

```python interface
# sh src/toolcheck.sh 的輸出(五行,順序固定):
#   gcc: gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
#   make: GNU Make 4.3
#   python3: Python 3.12.3
#   git: git version 2.43.0
#   gdb: GNU gdb (Ubuntu 15.0.50.20240403-0ubuntu1) 15.0.50.20240403-git
```

## 繳交
把整個資料夾(不含 `build/`)推到你的 git repo,並在 `make test` 全部通過後提交。老師會用**隱藏測試**再跑一次(例如:200 個大數字、換區塊大小、重新開啟同一顆 disk、PATH 裡沒有 gdb),所以請自己多想邊界情況。
