"""用書上的指令把十五關從頭打到尾,走的是玩家真正會走的路:bash + bin/quest。"""

import json
import os
import subprocess
from pathlib import Path

import pytest

from csquest.levels import LEVELS
from csquest.world import build, secrets

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261013

# 每關:(要先在哪個房間、玩家打的指令)。指令裡可以用 {s[...]} 取答案以外的參數。
SOLUTIONS = {
    1: ("gate", 'quest answer "$(pwd)"'),
    2: ("gate", 'quest answer "$(cat .key | cut -d: -f2)"'),
    3: ("gate", "cd ../hall/archive/vault/inner && quest check"),
    4: ("camp", "mkdir -p supplies/food && mv torch.txt supplies/ && cp map.old map.bak && rm trap.txt && quest check"),
    5: ("library", 'quest answer "$(tail -n 1 chronicle.log | cut -d: -f2)"'),
    6: ("mine", "mkdir chest && cp *.gem chest/ && quest check"),
    7: ("maze", 'quest answer "$(cat "$(find . -name "*.map")" | cut -d: -f2)"'),
    8: ("forge", "echo iron > report.txt; echo gold >> report.txt; ls nope 2> err.txt; quest check"),
    9: ("tower", 'quest answer "$(grep -c " 404 " access.log)"'),
    10: ("tower", 'quest answer "$(grep -oE "[A-Z]{3}-[0-9]{4}" whispers.txt)"'),
    11: ("scriptorium", "sed 's/darkness/light/g' spell.txt > light.txt && quest check"),
    12: ("tower", "quest answer \"$(grep ' 404 ' access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')\""),
    13: ("oracle", 'export SEAL="$(./oracle | head -1 | sed "s/.*是 //; s/。//")"; ./oracle > /dev/null; quest answer $?'),
    14: ("vault", "chmod 755 door.sh && chmod 600 secret.key && ./door.sh && quest check"),
    15: ("throne", """cat > spell.sh <<'EOF'
#!/bin/bash
name="$1"
if [ -z "$name" ]; then
    echo "用法:$0 <名字>" >&2
    exit 1
fi
echo "Hello, $name!"
EOF
chmod +x spell.sh && quest check"""),
}

# 會「做錯」的指令:跑完應該還是同一關
WRONG = {
    2: "quest answer isa-000",
    3: "cd ../hall/archive && quest check",
    4: "cp torch.txt torch2.txt; quest check",
    6: "mkdir chest && cp ore_* chest/ && quest check",
    8: "echo iron > report.txt; echo gold > report.txt; quest check",
    11: "sed 's/darkness/light/' spell.txt > light.txt && quest check",
    13: "SEAL=nope; quest answer 0",
    14: "chmod +x door.sh && quest check",
    15: "printf 'echo Hello, $1!\\n' > spell.sh && chmod +x spell.sh && quest check",
}


@pytest.fixture
def game(tmp_path):
    home = tmp_path / "q"
    build(home / "world", SEED)
    (home / "state.json").write_text(json.dumps({"seed": SEED, "level": 1, "hints": {}}))
    return home


def sh(game, room, cmd):
    env = dict(os.environ, HOME=str(game / "world"), CSQUEST_HOME=str(game),
               CSQUEST_NOANIM="1", PATH=f"{ROOT / 'bin'}:{os.environ['PATH']}")
    env.pop("SEAL", None)
    return subprocess.run(["bash", "-c", cmd], cwd=game / "world" / room, env=env,
                          capture_output=True, text=True, timeout=30)


def level(game):
    return json.loads((game / "state.json").read_text())["level"]


def test_every_level_has_a_solution():
    assert sorted(SOLUTIONS) == [lv.id for lv in LEVELS]


def test_full_playthrough(game):
    for lv in LEVELS:
        assert level(game) == lv.id
        room, cmd = SOLUTIONS[lv.id]
        if lv.id in WRONG:
            p = sh(game, room, WRONG[lv.id])
            assert level(game) == lv.id, f"第 {lv.id} 關的錯誤解法竟然過關了:\n{p.stdout}"
            assert "還沒過關" in p.stdout or "不對" in p.stdout
            sh(game, room, "quest reset-room")
        p = sh(game, room, cmd)
        assert level(game) == lv.id + 1, f"第 {lv.id} 關沒過:\n{p.stdout}\n{p.stderr}"
    p = sh(game, "", "quest")
    assert "走出了殼之地下城" in p.stdout


def test_hints_progress_and_cap(game):
    n = len(LEVELS[0].hints)
    outs = [sh(game, "gate", "quest hint").stdout for _ in range(n + 1)]
    assert f"提示 1/{n}" in outs[0]
    assert f"提示 {n}/{n}" in outs[n - 1]
    assert "用完" in outs[n]


def test_world_is_deterministic(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    build(a, 7)
    build(b, 7)
    for p in a.rglob("*"):
        if p.is_file():
            assert p.read_bytes() == (b / p.relative_to(a)).read_bytes()


def test_regex_level_has_exactly_one_match(tmp_path):
    for seed in range(30):
        build(tmp_path / str(seed), seed)
        p = subprocess.run(["grep", "-cE", "[A-Z]{3}-[0-9]{4}", "whispers.txt"],
                           cwd=tmp_path / str(seed) / "tower", capture_output=True, text=True)
        assert p.stdout.strip() == "1", seed


def test_top_ip_is_unique():
    for seed in range(200):
        counts = sorted(secrets(seed)["ips"].values())
        assert counts[-1] > counts[-2]


# ── quest book ──────────────────────────────────────────────

from csquest.book import parse, render, select
from csquest.levels import BOOK


def test_every_level_points_at_real_sections():
    titles = [t for _, t, _ in parse()]
    for n, prefixes in BOOK.items():
        for p in prefixes:
            assert any(t.startswith(p) for t in titles), f"第 {n} 關的「{p}」對不到書上任何小節"


def test_book_never_shows_exercise_solutions():
    text = render(parse(), 80, color=False)
    assert "tr -cs" not in text            # 練習 16.1 的解答
    assert "${f%.jpeg}" not in text        # 練習 16.4 的解答
    assert "解答收在書裡" in text
    assert "<svg" not in text and "viewBox" not in text


def test_quest_book_opens_current_section(game):
    p = sh(game, "gate", "quest book")
    assert "第 1 關" in p.stdout and "pwd" in p.stdout and "讀完按 q" in p.stdout
    assert "那一關你還沒走到" in sh(game, "gate", "quest book 5").stdout
    assert "權限" in sh(game, "gate", "quest book all").stdout


def test_wrong_answer_suggests_the_book(game):
    assert "quest book" in sh(game, "gate", "quest answer nope").stdout


def test_level6_book_explains_why_cp_ignores_pipes():
    text = render(select(parse(), BOOK[6]), 80, color=False)
    assert "是 Shell 在展開,不是指令" in text
    assert "xargs" in text and "從引數讀檔名" in text


def test_level9_book_covers_both_ways_to_count():
    text = render(select(parse(), BOOK[9]), 80, color=False)
    assert "grep -c" in text       # 一步到位
    assert "wc -l" in text         # grep ... | wc -l


def test_level9_explains_substring_overcount(tmp_path):
    from csquest.world import access_log
    seed = next(n for n in range(100)
                if sum("404" in l for l in access_log(secrets(n)).splitlines()) != secrets(n)["count_404"])
    home = tmp_path / "q"
    build(home / "world", seed)
    (home / "state.json").write_text(json.dumps({"seed": seed, "level": 9, "hints": {}}))
    p = sh(home, "tower", 'quest answer "$(grep -c 404 access.log)"')
    assert level(home) == 9
    assert "有些不是 404" in p.stdout
    p = sh(home, "tower", "quest answer 1")
    assert "有些不是 404" not in p.stdout
    sh(home, "tower", 'quest answer "$(grep -c " 404 " access.log)"')
    assert level(home) == 10
