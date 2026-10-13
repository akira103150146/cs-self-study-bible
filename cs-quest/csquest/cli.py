"""兩個入口:
  play  :建地下城、播開場、開一個遊戲用的 bash(玩家在裡面用真的指令闖關)
  quest :遊戲 bash 裡的指令,負責任務說明、驗收、提示、地圖
"""

import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import anim
from .anim import bold, cyan, dim, green, magenta, out, yellow
from . import book
from .levels import BOOK, LEVELS, Ctx
from .world import build, secrets

BIN = Path(__file__).resolve().parent.parent / "bin"


def home():
    return Path(os.environ.get("CSQUEST_HOME") or Path.home() / ".cs-quest")


def world():
    return home() / "world"


def load():
    try:
        return json.loads((home() / "state.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def save(st):
    home().mkdir(parents=True, exist_ok=True)
    (home() / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def level_of(st):
    return LEVELS[st["level"] - 1] if st["level"] <= len(LEVELS) else None


# ── 畫面 ─────────────────────────────────────────────────

def show_story(lv):
    out()
    out(magenta(f"  ◆ 第 {lv.id} 關 · {lv.title}"))
    out()
    anim.typewriter("  " + lv.story.replace("\n", "\n  "))


def show_task(lv):
    lines = [dim(f"地點  ~/{lv.room}"), dim(f"書中  16 章 · {lv.section}"), ""]
    lines += [("  " + t[2:]) if t.startswith("  ") else f"▸ {t}" for t in lv.task]
    lines += ["", dim("quest book 翻書 · hint 提示 · map 地圖 · help 說明")]
    anim.box(lines, title=f"任務 {lv.id}/{len(LEVELS)} · {lv.title}", color=yellow)


def show_map(st):
    out()
    out(bold("  殼之地下城"))
    out("  " + anim.progress_bar(min(st["level"] - 1, len(LEVELS)), len(LEVELS)))
    out()
    for lv in LEVELS:
        if lv.id < st["level"]:
            mark, name = green("✔"), dim(f"{lv.title:<8}")
        elif lv.id == st["level"]:
            mark, name = yellow("▶"), yellow(lv.title)
        else:
            mark, name = dim("·"), dim("???")
        out(f"  {mark} {lv.id:>2}  {anim.pad(name, 14)} {dim('~/' + lv.room) if lv.id <= st['level'] else ''}")
    out()


def ending(st):
    hints = sum(st.get("hints", {}).values())
    out()
    anim.celebrate("  ★ 你走出了殼之地下城 ★")
    out()
    anim.typewriter(
        "  接線生說:「從今天起,你不再只是『使用電腦的人』。\n"
        "  你是『指揮電腦的人』了。」")
    out()
    anim.box([f"通過關卡  {len(LEVELS)}/{len(LEVELS)}",
              f"使用提示  {hints} 次",
              "",
              "下一站:第 17 章 編輯器、第 18 章 Git"],
             title="結算", color=green)


# ── quest 指令 ─────────────────────────────────────────────

HELP = """quest            看目前任務
quest answer X   回報你找到的答案
quest check      驗收(改檔案、走到某處的關卡)
quest book       打開書上跟這關有關的段落(讀完按 q 回來)
quest book N     重讀第 N 關的段落;quest book all 整章
quest hint       拿下一則提示(越後面越直接)
quest map        看地圖與進度
quest story      重看這關的劇情
quest reset-room 把這關的房間還原成初始狀態
exit             離開遊戲(進度會保存,下次 ./play 繼續)"""


def attempt(st, lv, answer):
    ctx = Ctx(root=world(), s=secrets(st["seed"]), cwd=Path(os.getcwd()),
              env=dict(os.environ), answer=answer)
    anim.spinner("接線生正在檢查……", 0.6)
    ok, msg = lv.check(ctx)
    if not ok:
        anim.shake("✘ 還沒過關")
        for m in filter(None, msg.split(";")):
            out("  • " + m)
        out(dim("  忘了怎麼做?quest book 翻到書上這一段。"))
        return 1
    anim.celebrate(f"✔ 第 {lv.id} 關「{lv.title}」通過!")
    st["level"] += 1
    save(st)
    nxt = level_of(st)
    if nxt is None:
        ending(st)
        return 0
    show_story(nxt)
    show_task(nxt)
    if nxt.room != lv.room:
        out(dim(f"  (下一個房間在 ~/{nxt.room},自己走過去吧)"))
    return 0


def open_book(st, lv, which):
    if which == "all":
        return book.show(None, "第 16 章 · 終端機與 Shell 指令稿(整章)")
    n = lv.id
    if which:
        if not which.isdigit() or not 1 <= int(which) <= len(LEVELS):
            out(f"用法:quest book、quest book <1–{len(LEVELS)}>、quest book all")
            return 1
        n = int(which)
        if n > st["level"]:
            out("那一關你還沒走到。先專心眼前的關卡吧。")
            return 1
    target = LEVELS[n - 1]
    return book.show(BOOK[n], f"第 {n} 關「{target.title}」· 書中 16 章")


def reset_room(st, lv):
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, st["seed"])
        dst = world() / lv.room
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(Path(tmp) / lv.room, dst, symlinks=True)
    out(green(f"~/{lv.room} 已還原。") + dim("(如果你正站在裡面,先 cd . 重新整理一下)"))


def quest_main(argv):
    st = load()
    if st is None:
        out("找不到遊戲存檔。請先在 cs-quest/ 執行 ./play。")
        return 1
    cmd, rest = (argv[0], argv[1:]) if argv else ("task", [])
    lv = level_of(st)
    if cmd in ("help", "-h", "--help"):
        out(HELP)
        return 0
    if cmd == "map":
        show_map(st)
        return 0
    if cmd == "book":
        return open_book(st, lv or LEVELS[-1], rest[0] if rest else "")
    if lv is None:
        ending(st)
        return 0
    if cmd in ("task", "status"):
        show_task(lv)
    elif cmd == "story":
        show_story(lv)
    elif cmd == "hint":
        used = st.setdefault("hints", {}).get(str(lv.id), 0)
        if used >= len(lv.hints):
            out(dim("提示已經用完了。最後一則:"))
            used = len(lv.hints) - 1
        else:
            st["hints"][str(lv.id)] = used + 1
            save(st)
        out(yellow(f"💡 提示 {used + 1}/{len(lv.hints)}:") + lv.hints[used])
    elif cmd == "answer":
        return attempt(st, lv, " ".join(rest))
    elif cmd == "check":
        return attempt(st, lv, "")
    elif cmd == "reset-room":
        reset_room(st, lv)
    else:
        out(f"接線生聽不懂「{cmd}」。打 quest help 看看能說什麼。")
        return 1
    return 0


# ── play:啟動遊戲 ───────────────────────────────────────────

RC = r"""
export BASH_SILENCE_DEPRECATION_WARNING=1
export PATH="{bin}:$PATH"
export HISTFILE="{home}/history"
PS1='\[\e[1;32m\]冒險者\[\e[0m\]@\[\e[1;35m\]殼\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ '
if ls --color=auto / >/dev/null 2>&1; then alias ls='ls --color=auto'; else alias ls='ls -G'; fi
cd "$HOME/{room}" 2>/dev/null || cd "$HOME"
quest
"""


def new_game():
    if world().exists():
        shutil.rmtree(world())
    st = {"seed": random.randint(1, 10**9), "level": 1, "hints": {}}
    anim.spinner("正在挖掘地下城……", 1.2)
    build(world(), st["seed"])
    save(st)
    return st


def play_main(argv):
    fresh = "--new" in argv
    st = None if fresh else load()
    if st is None or not world().exists():
        if fresh and load() is not None:
            ans = input("確定要放棄目前進度、重新開始嗎?[y/N] ").strip().lower()
            if ans != "y":
                return 0
        out()
        anim.title_screen()
        out()
        st = new_game()
        anim.typewriter(
            "  你即將進入一座由檔案與資料夾構成的地下城。\n"
            "  這裡沒有滑鼠。你唯一的武器,是指令。\n\n"
            "  在這裡打的每一個指令都是「真的」bash 指令——\n"
            "  書上第 16 章教的,在這裡全都用得上。")
        out()
        anim.box([f"地下城的位置  {world()}",
                  "在遊戲裡,~ 就是地下城入口,cd 不帶參數會回到這裡。",
                  "",
                  "⚠ 這是真的 shell。rm -rf 在這裡一樣不會手下留情,",
                  "  請只在地下城裡面動手。"],
                 title="注意", color=yellow)
        input(dim("\n  按 Enter 進入地下城…"))
    else:
        out(green(f"\n  歡迎回來,你在第 {st['level']} 關。"))

    lv = level_of(st)
    rc = home() / "bashrc"
    rc.write_text(RC.format(bin=BIN, home=home(), room=lv.room if lv else ""), encoding="utf-8")
    env = dict(os.environ,
               HOME=str(world()), CSQUEST_HOME=str(home()), CSQUEST_REAL_HOME=str(Path.home()))
    env.pop("SEAL", None)
    subprocess.call(["bash", "--rcfile", str(rc), "-i"], env=env)
    out(dim("\n  你離開了地下城。進度已保存,./play 回來繼續。\n"))
    return 0


def main():
    prog = Path(sys.argv[0]).name
    argv = sys.argv[1:]
    try:
        if prog == "quest" or (argv and argv[0] == "quest"):
            if argv and argv[0] == "quest":
                argv = argv[1:]
            return quest_main(argv)
        return play_main(argv)
    except KeyboardInterrupt:
        out()
        return 130
