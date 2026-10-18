# cs-quest · 殼之地下城

把第 16 章〈終端機與 Shell 指令稿〉做成在終端機裡玩的闖關遊戲。
玩家在**真的 bash** 裡用書上的指令探索一座由資料夾構成的地下城，`quest` 指令負責劇情、驗收、提示。

```
./play          # 開始或繼續
./play --new    # 放棄進度、重新生一座地下城
```

遊戲裡：

```
quest            看目前任務
quest answer X   回報找到的答案
quest check      驗收（改檔案、走到某處的關卡）
quest book       打開書上跟這關有關的段落（less 翻閱，q 回來）
quest book N     重讀第 N 關的段落；quest book all 整章
quest hint       下一則提示（越後面越直接）
quest map        地圖與進度
quest reset-room 還原這關的房間
exit             離開（進度保存）
```

## 十五關對照書中小節

| 關 | 房間 | 練的東西 |
|---|---|---|
| 1 | gate | `pwd`、絕對路徑 |
| 2 | gate | `ls -a`、`cat` 隱藏檔 |
| 3 | hall | `cd`、相對路徑（站到指定房間驗收） |
| 4 | camp | `mkdir -p`、`mv`、`cp`、`rm` |
| 5 | library | `tail` |
| 6 | mine | 萬用字元 `*.gem` |
| 7 | maze | `find` |
| 8 | forge | `>`、`>>`、`2>` |
| 9 | tower | `grep -c`、`wc -l` |
| 10 | tower | `grep -E` 正規表示式 |
| 11 | scriptorium | `sed 's///g'` |
| 12 | tower | `awk`、`sort`、`uniq -c` 管線 |
| 13 | oracle | `export`、`./程式`、`$?` |
| 14 | vault | `chmod 755 / 600` |
| 15 | throne | 寫腳本：shebang、`$1`、`if`、`>&2`、`exit` |

## 怎麼運作

- `csquest/world.py`：用一個 seed 生出整座地下城（檔案內容、答案都由 seed 決定，每個玩家的答案不同）。答案不存檔，檢查時用 seed 重算。
- `csquest/levels.py`：關卡表。每關是劇情、任務、提示加上一個 `check()`；`quest` 是玩家 shell 的子程序，所以能讀到玩家的目前目錄和 `export` 過的變數。
- `csquest/cli.py`：`./play` 生地下城、播開場，然後開一個 `bash --rcfile`，把 `HOME` 設成地下城入口；`quest` 指令也在這裡。
- `csquest/book.py`：讀 `../chapters/16-shell.html`，依 `<h2>`/`<h3>` 切成小節、轉成終端機文字交給 `less -R`。圖換成圖說，練習題解答不顯示。每關對應哪些小節寫在 `levels.py` 的 `BOOK`。書的位置可用 `CSQUEST_BOOK` 改。
- `csquest/anim.py`：純 ANSI escape code 的動畫（解碼標題、打字機、過關煙火）。`CSQUEST_NOANIM=1` 關閉。
- 存檔與地下城在 `~/.cs-quest/`（可用 `CSQUEST_HOME` 改）。

只用 Python 3 標準函式庫和系統內建的 bash。

## 測試

```
python3 -m pytest -q
```

`tests/test_playthrough.py` 用書上的指令透過 bash 加 `bin/quest` 把十五關從頭打到尾，並確認常見的錯誤做法不會過關。
