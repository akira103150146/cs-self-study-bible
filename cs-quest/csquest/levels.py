"""十五個關卡,依第 16 章的小節順序排列。

每關有兩種過關方式:
  kind="answer":玩家查到某個值,用 `quest answer <值>` 回報
  kind="check" :玩家把地下城改成某個狀態(或站到某個位置),用 `quest check` 驗收
check(ctx) 回傳 (是否過關, 給玩家看的訊息)。
"""

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .world import access_log, mode_of, spell_text


@dataclass
class Ctx:
    root: Path          # 地下城根目錄
    s: dict             # world.secrets(seed)
    cwd: Path           # 玩家下 quest 指令時所在的目錄
    env: dict           # 玩家 shell 匯出(export)的環境變數
    answer: str = ""    # quest answer 後面接的文字


@dataclass
class Level:
    id: int
    room: str
    title: str
    section: str        # 對應書中小節
    story: str
    task: list
    hints: list
    kind: str
    check: object = field(repr=False)


def same(a, b):
    return a.strip().strip("\"'").lower() == str(b).strip().lower()


def answer_is(key, show=None):
    def check(ctx):
        if not ctx.answer:
            return False, "這關要用 quest answer <你找到的值> 回報。"
        if same(ctx.answer, ctx.s[key]):
            return True, ""
        return False, f"「{ctx.answer}」不對。{show or ''}"
    return check


# ── 個別關卡的檢查 ─────────────────────────────────────────────

def check_pwd(ctx):
    want = (ctx.root / "gate").resolve()
    if not ctx.answer:
        return False, "用 quest answer <路徑> 回報你現在所在的完整路徑。"
    got = Path(os.path.expanduser(ctx.answer.strip())).resolve() if ctx.answer.startswith(("/", "~")) else None
    if got == want:
        return True, ""
    words = ctx.answer.split()
    if words and words[0] in ("echo", "pwd"):
        return False, (f"我收到的是「{ctx.answer}」:quest answer 後面的字會原封不動交給我,不會先幫你執行。"
                       ";先單獨打 pwd,把它印出的路徑貼在 quest answer 後面"
                       ";(變數大小寫有別:$PWD 才是目前目錄,$pwd 是一個沒設定的空變數)")
    return False, "那不是你現在的位置。要從根目錄 / 開始的完整路徑(絕對路徑)。"


def check_cd(ctx):
    want = (ctx.root / "hall" / "archive" / "vault" / "inner").resolve()
    if ctx.cwd.resolve() == want:
        return True, ""
    return False, f"你現在站在 {ctx.cwd},還沒走到卷軸所在的房間。"


def check_count_404(ctx):
    ok, msg = answer_is("count_404")(ctx)
    if ok or not ctx.answer.strip().isdigit():
        return ok, msg
    loose = sum("404" in line for line in access_log(ctx.s).splitlines())
    if int(ctx.answer) == loose:
        return False, (f"你數到的 {loose} 行裡,有些不是 404。"
                       ";grep \"404\" 只看這三個字有沒有出現,像「403 4047」這種傳輸大小裡剛好含 404 的行也會被算進去"
                       ";想想看:狀態碼 404 的前後各有什麼?")
    return False, msg


def check_camp(ctx):
    camp = ctx.root / "camp"
    problems = []
    if not (camp / "supplies" / "food").is_dir():
        problems.append("camp/supplies/food 這個資料夾還不存在")
    if not (camp / "supplies" / "torch.txt").is_file():
        problems.append("torch.txt 還沒搬進 supplies/")
    if (camp / "torch.txt").exists():
        problems.append("camp/ 底下還留著 torch.txt(是「搬」,不是「複製」)")
    if not (camp / "map.bak").is_file() or not (camp / "map.old").is_file():
        problems.append("需要同時有 map.old 和它的複本 map.bak")
    elif (camp / "map.bak").read_bytes() != (camp / "map.old").read_bytes():
        problems.append("map.bak 的內容和 map.old 不一樣")
    if (camp / "trap.txt").exists():
        problems.append("陷阱 trap.txt 還在")
    return (not problems), ";".join(problems)


def check_glob(ctx):
    chest = ctx.root / "mine" / "chest"
    if not chest.is_dir():
        return False, "mine/chest 資料夾還不存在。"
    want = {f"ore_{g:02d}.gem" for g in ctx.s["gems"]}
    got = {p.name for p in chest.iterdir()}
    if got == want:
        return True, ""
    missing, extra = want - got, got - want
    msg = []
    if missing:
        msg.append(f"還少 {len(missing)} 顆寶石")
    if extra:
        msg.append(f"箱子裡混進了不該放的東西:{', '.join(sorted(extra)[:3])}")
    return False, ";".join(msg)


def check_redirect(ctx):
    forge = ctx.root / "forge"
    report, err = forge / "report.txt", forge / "err.txt"
    if not report.is_file():
        return False, "forge/report.txt 還不存在。"
    lines = report.read_text(encoding="utf-8").splitlines()
    if lines != ["iron", "gold"]:
        return False, f"report.txt 要剛好兩行 iron、gold,現在是 {lines}。"
    if not err.is_file() or not err.read_text(encoding="utf-8").strip():
        return False, "err.txt 還是空的:它應該裝著一則錯誤訊息。"
    if "iron" in err.read_text(encoding="utf-8"):
        return False, "err.txt 裡只該有錯誤訊息。"
    return True, ""


def check_sed(ctx):
    room = ctx.root / "scriptorium"
    orig, light = room / "spell.txt", room / "light.txt"
    if orig.read_text(encoding="utf-8") != spell_text():
        return False, "原本的 spell.txt 被改掉了!這關要求原檔不動。(quest reset-room 可以還原這個房間)"
    if not light.is_file():
        return False, "scriptorium/light.txt 還不存在。"
    if light.read_text(encoding="utf-8") != spell_text().replace("darkness", "light"):
        if "darkness" in light.read_text(encoding="utf-8"):
            return False, "light.txt 裡還有 darkness。一行裡可能不只一個喔。"
        return False, "light.txt 的內容不對。"
    return True, ""


def check_oracle(ctx):
    if "SEAL" not in ctx.env:
        return False, "我看不到環境變數 SEAL:還沒設定,或是設了但沒有 export。"
    if ctx.env["SEAL"] != ctx.s["seal"]:
        return False, "SEAL 的值不是封印之名。"
    if not ctx.answer:
        return False, "封印對了。現在用 quest answer <數字> 回報神諭的結束狀態碼。"
    if same(ctx.answer, ctx.s["oracle_exit"]):
        return True, ""
    return False, "結束狀態碼不對。記住:$? 只記得「上一個」指令。"


def check_chmod(ctx):
    vault = ctx.root / "vault"
    d, k = mode_of(vault / "door.sh"), mode_of(vault / "secret.key")
    msg = []
    if d != 0o755:
        msg.append(f"door.sh 現在是 {d:03o},要 755")
    if k != 0o600:
        msg.append(f"secret.key 現在是 {k:03o},要 600")
    return (not msg), ";".join(msg)


def check_script(ctx):
    script = ctx.root / "throne" / "spell.sh"
    if not script.is_file():
        return False, "throne/spell.sh 還不存在。"
    if not script.read_text(encoding="utf-8").startswith("#!"):
        return False, "第一行少了 shebang(#!/bin/bash)。"
    if not mode_of(script) & 0o100:
        return False, "spell.sh 還不能執行(少了 x 權限)。"

    def run(*args):
        return subprocess.run([str(script), *args], capture_output=True, text=True,
                              timeout=5, cwd=script.parent)

    try:
        for name in ["Ada", "Ada Lovelace"]:
            p = run(name)
            if p.returncode != 0 or p.stdout.strip() != f"Hello, {name}!":
                hint = "(檔名或名字裡有空白時,變數要加雙引號)" if " " in name else ""
                return False, f"./spell.sh \"{name}\" 應該印 Hello, {name}! 並以 0 結束,實際印出 {p.stdout.strip()!r}、狀態碼 {p.returncode}。{hint}"
        p = run()
        if p.returncode == 0:
            return False, "不給名字時要以非 0 狀態碼結束(exit 1)。"
        if p.stdout.strip():
            return False, "不給名字時,用法訊息要寫到 stderr(>&2),stdout 要保持乾淨。"
        if not p.stderr.strip():
            return False, "不給名字時,要在 stderr 印出用法說明。"
    except subprocess.TimeoutExpired:
        return False, "spell.sh 跑超過 5 秒,是不是在等鍵盤輸入?"
    except OSError as e:
        return False, f"spell.sh 無法執行:{e}"
    return True, ""


# ── 關卡表 ─────────────────────────────────────────────────

LEVELS = [
    Level(1, "gate", "甦醒", "終端機、Shell、Bash",
          "你在一片漆黑中醒來,眼前只有一個閃爍的游標。\n"
          "一個聲音說:「我是接線生。你對我說的話,我會轉達給這台機器。先告訴我——你在哪?」",
          ["查出你目前所在資料夾的完整路徑(絕對路徑)",
           "回報:quest answer <路徑>"],
          ["「我在哪」的英文是 print working directory。",
           "指令是 pwd。它印出來的整串就是答案。"],
          "answer", check_pwd),
    Level(2, "gate", "看不見的鑰匙", "pwd、ls、cd",
          "大門緊閉。門上刻著:「看不見的東西,不代表不存在。」",
          ["在 gate/ 裡找出隱藏的鑰匙,讀出上面的符文",
           "回報:quest answer <符文>(例如 isa-123)"],
          ["ls 預設不顯示「以 . 開頭」的檔案。",
           "ls -a 會列出隱藏檔。",
           "cat .key 讀出內容,冒號後面那串就是符文。"],
          "answer", answer_is("key_rune")),
    Level(3, "hall", "深入大廳", "絕對路徑與相對路徑",
          "大門開了,通往大廳。傳說大廳的檔案庫深處,藏著一卷古老的卷軸。",
          ["走到 hall/archive/vault/inner 這個房間",
           "站在那裡打:quest check"],
          ["cd 可以一次走好幾層:cd ../hall/archive/vault/inner",
           "迷路了?cd ~ 回到地下城入口,再 cd hall/archive/vault/inner。",
           "Tab 鍵可以自動補完資料夾名稱。"],
          "check", check_cd),
    Level(4, "camp", "紮營", "建立、複製、移動、刪除",
          "你在 camp/ 停下來整理行囊。這裡有一支火把、一張舊地圖,還有一個陷阱。",
          ["建立 camp/supplies/food(一次建好兩層)",
           "把 torch.txt 搬進 camp/supplies/",
           "把 map.old 複製一份叫 map.bak(原檔保留)",
           "刪掉 trap.txt",
           "完成後:quest check"],
          ["mkdir -p 可以一次建好整條路徑。",
           "搬移用 mv,複製用 cp,刪除用 rm。",
           "mkdir -p supplies/food && mv torch.txt supplies/ && cp map.old map.bak && rm trap.txt"],
          "check", check_camp),
    Level(5, "library", "編年史", "查看檔案內容",
          "圖書館裡有一本上千行的編年史 chronicle.log。通關密語寫在最後一頁。",
          ["不要用 cat 把整本倒出來,找出最後一行的通關密語",
           "回報:quest answer <密語>"],
          ["head 看開頭,tail 看結尾。",
           "tail -n 1 chronicle.log"],
          "answer", answer_is("chronicle_word")),
    Level(6, "mine", "寶石礦坑", "萬用字元",
          "礦坑裡堆滿了礦石。副檔名 .gem 的是寶石,.rock 的只是石頭。",
          ["在 mine/ 裡建立 chest/ 資料夾",
           "一個指令把所有 .gem 檔複製進 chest/(不要放進 .rock 或其他檔)",
           "完成後:quest check"],
          ["* 代表任意長度的任意字元。",
           "*.gem 會被 Shell 展開成所有 .gem 結尾的檔名。",
           "mkdir chest && cp *.gem chest/"],
          "check", check_glob),
    Level(7, "maze", "迷宮", "find",
          "迷宮裡有幾十條岔路、好幾層深。某個角落藏著一張 treasure.map。",
          ["找出 treasure.map 在哪,讀出背面寫的字",
           "回報:quest answer <那串字>"],
          ["萬用字元只看得到目前這一層;要鑽進每一層子目錄,用 find。",
           "find . -name \"*.map\"",
           "找到路徑後,cat 那個路徑。"],
          "answer", answer_is("map_word")),
    Level(8, "forge", "熔爐報告", "重新導向",
          "鐵匠要你交一份報告,還要你把一次失敗的紀錄存下來。",
          ["在 forge/ 建立 report.txt,內容剛好兩行:第一行 iron,第二行 gold",
           "  (用 echo 加 > 寫第一行,再用 >> 附加第二行)",
           "對一個不存在的檔案下 ls,只把錯誤訊息存進 err.txt",
           "完成後:quest check"],
          ["> 會覆蓋,>> 會附加到結尾。",
           "錯誤訊息走 stderr(編號 2),所以用 2> 導向。",
           "echo iron > report.txt; echo gold >> report.txt; ls nope 2> err.txt"],
          "check", check_redirect),
    Level(9, "tower", "高塔的紀錄", "管線與 grep",
          "高塔守衛的存取紀錄 access.log 有上千行。有人一直在敲不存在的門(HTTP 404)。",
          ["算出 access.log 裡有幾行是 404",
           "回報:quest answer <行數>"],
          ["grep 可以篩出含某段文字的行;要小心別誤抓到含 404 的其他數字。",
           "狀態碼前後都有空白:grep \" 404 \"",
           "grep -c \" 404 \" access.log,或 grep \" 404 \" access.log | wc -l"],
          "answer", check_count_404),
    Level(10, "tower", "守衛的低語", "正規表示式",
          "whispers.txt 記錄了三百句低語。其中只有一句提到了真正的暗號:\n"
          "三個大寫字母、一個減號、四個數字(長得像 QRT-4821)。",
          ["用正規表示式找出那個暗號",
           "回報:quest answer <暗號>"],
          ["grep -E 啟用擴充正規表示式。",
           "[A-Z] 配一個大寫字母,{3} 表示剛好重複三次。",
           "grep -E \"[A-Z]{3}-[0-9]{4}\" whispers.txt"],
          "answer", answer_is("code")),
    Level(11, "scriptorium", "破除黑暗", "sed",
          "抄寫室的咒語 spell.txt 充滿了 darkness。你要抄一份新版本,把黑暗全換成光。",
          ["產生 scriptorium/light.txt:內容是 spell.txt 把「所有」darkness 換成 light",
           "spell.txt 本身不能改",
           "完成後:quest check"],
          ["sed 's/舊/新/' 只換每行第一個;加 g 才是全部。",
           "結果用 > 導進新檔,原檔就不會動。",
           "sed 's/darkness/light/g' spell.txt > light.txt"],
          "check", check_sed),
    Level(12, "tower", "誰在敲門", "awk、sort、uniq",
          "守衛想知道:到底是哪個 IP 敲最多次不存在的門?",
          ["從 access.log 找出 404 次數最多的 IP",
           "回報:quest answer <IP>"],
          ["先 grep 出 404 的行,再用 awk '{print $1}' 取出第一欄(IP)。",
           "sort | uniq -c 可以數每個 IP 出現幾次;sort 一定要在 uniq 前面。",
           "grep \" 404 \" access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -1"],
          "answer", answer_is("top_ip")),
    Level(13, "oracle", "神諭", "環境變數與 $?",
          "神諭是一支程式。它會說出封印之名,然後留下一個沉默的結束狀態碼。",
          ["執行 oracle/oracle,記下封印之名",
           "把封印之名設成環境變數 SEAL(要 export,我才看得到)",
           "查出 oracle 的結束狀態碼,回報:quest answer <數字>"],
          ["自己資料夾裡的程式要用 ./oracle 執行(它不在 PATH 裡)。",
           "export SEAL=封印之名",
           "執行完 ./oracle 後「立刻」echo $?;中間多跑一個指令,$? 就被蓋掉了。"],
          "answer", check_oracle),
    Level(14, "vault", "寶庫之門", "權限 rwx 與 chmod",
          "寶庫的門 door.sh 是一支打不開的腳本,龍的鑰匙 secret.key 則誰都能讀寫——太危險了。",
          ["把 door.sh 設成 755(rwxr-xr-x),然後試著 ./door.sh",
           "把 secret.key 設成 600(rw-------),只有你能碰",
           "用 ls -l 確認,然後:quest check"],
          ["r=4、w=2、x=1,三組(擁有者/群組/其他人)各自相加。",
           "chmod 755 door.sh",
           "chmod 600 secret.key"],
          "check", check_chmod),
    Level(15, "throne", "最後的咒語", "Shell 指令稿",
          "王座前,接線生說:「到目前為止,都是你一行一行告訴我。現在,寫一支咒語,讓它自己跑。」",
          ["在 throne/ 寫一支 spell.sh:",
           "  ./spell.sh Ada        → 印出 Hello, Ada!,狀態碼 0",
           "  ./spell.sh \"Ada Lovelace\" → 印出 Hello, Ada Lovelace!",
           "  ./spell.sh(沒給名字)→ 在 stderr 印用法,以 exit 1 結束",
           "記得 shebang 與執行權限,完成後:quest check"],
          ["可以用 nano spell.sh 編輯(Ctrl-O 存檔、Ctrl-X 離開)。",
           "第一個引數是 $1;檢查空字串用 [ -z \"$name\" ];寫到 stderr 用 >&2。",
           "骨架:#!/bin/bash ⏎ name=\"$1\" ⏎ if [ -z \"$name\" ]; then echo \"用法:$0 <名字>\" >&2; exit 1; fi ⏎ echo \"Hello, $name!\"",
           "別忘了 chmod +x spell.sh。"],
          "check", check_script),
]


# 每關對應的書本小節(標題開頭),quest book 會打開這些段落
BOOK = {
    1: ["終端機、Shell、Bash", "在檔案系統裡導航", "pwd、ls、cd"],
    2: ["pwd、ls、cd"],
    3: ["在檔案系統裡導航", "pwd、ls、cd"],
    4: ["動手操作檔案"],
    5: ["動手操作檔案"],
    6: ["萬用字元與尋找", "xargs:"],          # xargs:想用 ls *.gem | cp 的人會需要
    7: ["萬用字元與尋找"],
    8: ["重新導向與管線", "重新導向(redirection)"],
    9: ["管線(pipe)", "grep:", "更多好幫手"],   # 更多好幫手:wc -l
    10: ["grep:"],
    11: ["sed:"],
    12: ["管線(pipe)", "awk:", "更多好幫手"],
    13: ["環境變數、PATH 與引號", "PATH:", "$?:"],
    14: ["權限:rwx 與 chmod"],
    15: ["Shell 指令稿", "變數、引數與命令替換", "判斷:if", "引號:"],
}
