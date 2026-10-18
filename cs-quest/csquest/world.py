"""地下城生成器:用一個 seed 決定所有亂數,同一個 seed 永遠長出同一座地下城。

答案不存檔,檢查時用 seed 重新算一次(見 secrets())。
"""

import os
import random
import stat
from pathlib import Path

RUNES = ["ansuz", "berkano", "dagaz", "ehwaz", "fehu", "gebo", "hagalaz",
         "isa", "jera", "kenaz", "laguz", "mannaz", "othala", "raido",
         "sowilo", "tiwaz", "uruz", "wunjo"]
WORDS = ["lantern", "ember", "falcon", "obsidian", "quartz", "harbor",
         "thistle", "cobalt", "meadow", "zephyr", "granite", "willow"]


def secrets(seed):
    """這座地下城的所有答案與隨機參數。"""
    r = random.Random(seed)
    s = {}
    s["key_rune"] = r.choice(RUNES) + "-" + str(r.randint(100, 999))
    s["chronicle_word"] = r.choice(WORDS) + str(r.randint(10, 99))
    s["chronicle_lines"] = r.randint(800, 1400)
    s["gems"] = sorted(r.sample(range(1, 60), 12))
    s["rocks"] = sorted(r.sample(range(1, 60), 15))
    s["map_word"] = r.choice(WORDS) + "-" + r.choice(RUNES)
    s["map_path"] = [r.choice(["north", "south", "east", "west", "down"]) + str(r.randint(1, 9))
                     for _ in range(4)]
    s["code"] = "".join(r.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(3)) + "-" + str(r.randint(1000, 9999))
    s["seal"] = r.choice(RUNES).upper()
    s["oracle_exit"] = r.randint(3, 120)

    # access.log:每個 IP 的 404 次數彼此不同,最多的那個就是答案
    ips = [f"{r.randint(11, 223)}.{r.randint(0, 255)}.{r.randint(0, 255)}.{r.randint(1, 254)}"
           for _ in range(8)]
    counts = r.sample(range(4, 40), len(ips))
    s["ips"] = dict(zip(ips, counts))
    s["top_ip"] = max(s["ips"], key=s["ips"].get)
    s["count_404"] = sum(counts)
    s["log_rng"] = r.randint(0, 10**9)
    return s


def _write(path, text, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    os.chmod(path, mode)


def access_log(s):
    r = random.Random(s["log_rng"])
    entries = []
    for ip, n in s["ips"].items():
        entries += [(ip, 404)] * n
    others = list(s["ips"]) + ["10.0.0.%d" % i for i in range(1, 30)]
    for _ in range(600):
        entries.append((r.choice(others), r.choice([200, 200, 200, 301, 302, 500, 403])))
    r.shuffle(entries)
    paths = ["/", "/index.html", "/login", "/api/v1/items", "/img/logo.png", "/old-page", "/admin"]
    lines = []
    for i, (ip, code) in enumerate(entries):
        lines.append(f'{ip} - - [13/Oct/2026:{i // 3600 % 24:02d}:{i // 60 % 60:02d}:{i % 60:02d} +0800] '
                     f'"GET {r.choice(paths)} HTTP/1.1" {code} {r.randint(200, 9000)}')
    return "\n".join(lines) + "\n"


SPELL = """darkness falls upon the tower
and darkness fills the hall
speak the words and break the darkness
light the lantern, one and all
where darkness was, let darkness end
"""


def spell_text():
    return SPELL


def build(root, seed):
    """在 root 底下長出整座地下城(root 必須是空的或不存在)。"""
    root = Path(root)
    s = secrets(seed)
    r = random.Random(seed + 1)

    _write(root / "README.txt",
           "這裡是殼(Shell)之地下城。\n打 quest 看目前任務,quest hint 拿提示,quest map 看地圖。\n")

    # 1–2 大門:隱藏檔
    _write(root / "gate" / "sign.txt", "大門上刻著:「看不見的東西,不代表不存在。」\n")
    _write(root / "gate" / ".key", f"符文鑰匙:{s['key_rune']}\n")

    # 3 大廳:深層目錄
    _write(root / "hall" / "archive" / "vault" / "inner" / "scroll.txt",
           "你走到了最深處。卷軸上寫著:路徑,就是你走過的每一層。\n")
    for d in ["hall/archive/dust", "hall/archive/vault/empty", "hall/lobby"]:
        (root / d).mkdir(parents=True, exist_ok=True)

    # 4 營地:檔案操作
    _write(root / "camp" / "torch.txt", "一支還能點燃的火把。\n")
    _write(root / "camp" / "map.old", "一張泛黃的舊地圖。\n")
    _write(root / "camp" / "trap.txt", "⚠ 這是陷阱。\n")

    # 5 圖書館:head / tail
    lines = []
    for i in range(1, s["chronicle_lines"]):
        lines.append(f"第 {i} 年:{r.choice(['風平浪靜', '豐收', '大雨', '旱災', '戰事', '節慶'])}。")
    lines.append(f"編年史的最後一頁寫著通關密語:{s['chronicle_word']}")
    _write(root / "library" / "chronicle.log", "\n".join(lines) + "\n")

    # 6 礦坑:萬用字元
    for g in s["gems"]:
        _write(root / "mine" / f"ore_{g:02d}.gem", "💎\n")
    for k in s["rocks"]:
        _write(root / "mine" / f"ore_{k:02d}.rock", "🪨\n")
    _write(root / "mine" / "gem_or_not.txt", "這不是寶石,只是一張紙條。\n")

    # 7 迷宮:find
    maze = root / "maze"
    for _ in range(40):
        depth = r.randint(1, 4)
        parts = [r.choice(["north", "south", "east", "west", "down"]) + str(r.randint(1, 9)) for _ in range(depth)]
        _write(maze.joinpath(*parts) / f"note{r.randint(1, 99)}.txt", "這裡什麼都沒有。\n")
    _write(maze.joinpath(*s["map_path"]) / "treasure.map", f"藏寶圖背面寫著:{s['map_word']}\n")

    # 8 熔爐:重新導向
    _write(root / "forge" / "README.txt", "熔爐需要一份報告。看任務說明。\n")

    # 9, 10, 12 高塔:grep、regex、管線
    _write(root / "tower" / "access.log", access_log(s))
    whispers = []
    for _ in range(300):
        whispers.append(r.choice([
            f"room {r.randint(1, 999)} is empty",
            f"call {r.randint(100, 999)}-{r.randint(100, 999)} for help",
            f"the code is not {r.choice('abcxyz')}{r.choice('abc')}-{r.randint(10, 99)}",
            f"AB-{r.randint(1000, 9999)} was a lie",
            f"{r.choice(WORDS)} {r.choice(WORDS)} {r.choice(WORDS)}",
        ]))
    whispers.insert(r.randint(50, 250), f"the guardian whispers {s['code']} and falls silent")
    _write(root / "tower" / "whispers.txt", "\n".join(whispers) + "\n")

    # 11 抄寫室:sed
    _write(root / "scriptorium" / "spell.txt", SPELL)

    # 13 神諭:環境變數與 $?
    _write(root / "oracle" / "oracle",
           "#!/bin/bash\n"
           f'echo "神諭低語:封印之名是 {s["seal"]}。"\n'
           'echo "神諭沉默了……但它留下了一個結束狀態碼。"\n'
           f"exit {s['oracle_exit']}\n", 0o755)

    # 14 寶庫:權限
    _write(root / "vault" / "door.sh",
           "#!/bin/bash\necho \"🚪 喀啦——寶庫的門打開了。\"\n", 0o644)
    _write(root / "vault" / "secret.key", "-----BEGIN DRAGON KEY-----\n", 0o666)

    # 15 王座
    _write(root / "throne" / "README.txt", "最後的考驗:親手寫一支咒語(腳本)。\n")
    return s


def mode_of(path):
    return stat.S_IMODE(os.stat(path).st_mode)
