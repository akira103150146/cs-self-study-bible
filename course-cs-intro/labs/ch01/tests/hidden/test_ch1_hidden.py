"""第 1 章 Lab 隱藏測試(不會發給學生)。"""
import os
import random
import re
import shutil
import subprocess
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(cmd, stdin="", env=None):
    return subprocess.run(cmd, cwd=ROOT, input=stdin, capture_output=True, text=True,
                          shell=isinstance(cmd, str), env=env, timeout=60)


# ---------------------------------------------------------------- 任務 1

def test_C1_1_sum_same_output():
    rnd = random.Random(2024)
    nums = [rnd.randint(-10**12, 10**12) for _ in range(200)]
    text = "\n".join(" ".join(map(str, nums[i:i + 7])) for i in range(0, 200, 7)) + "\n"
    c, py = sh(["./build/sum"], text), sh(["python3", "src/sum.py"], text)
    assert c.stdout.strip() == py.stdout.strip() == str(sum(nums))


def test_C1_1_sum_empty():
    assert sh(["./build/sum"], "").stdout.strip() == "0"
    assert sh(["python3", "src/sum.py"], "").stdout.strip() == "0"


# ---------------------------------------------------------------- 任務 2

@pytest.fixture(scope="module")
def pipeline():
    r = sh(["make", "-s", "pipeline"])
    assert r.returncode == 0, r.stdout + r.stderr
    return r


def test_C1_4_asm_has_main(pipeline):
    with open(os.path.join(ROOT, "build", "sum.s")) as f:
        s = f.read()
    assert re.search(r"\.globl\s+main", s)


SECTIONS = ["Application", "High-level language", "Assembly", "Machine code", "Operating system", "Hardware"]
QUOTES = {"High-level language": "src/sum.c", "Assembly": "build/sum.s", "Machine code": "build/sum.dis"}


def _sections(md):
    out, cur = {}, None
    for line in md.split("\n"):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = ""
        elif cur:
            out[cur] += line + "\n"
    return out


def _quoted_lines(text):
    lines = re.findall(r"`([^`\n]+)`", text)
    for block in re.findall(r"```[^\n]*\n(.*?)```", text, re.S):
        lines += block.split("\n")
    return [l.strip() for l in lines if len(l.strip()) >= 4]


def test_C1_1_layers_report(pipeline):
    with open(os.path.join(ROOT, "src", "layers.md"), encoding="utf-8") as f:
        secs = _sections(f.read())
    assert list(secs) == SECTIONS
    for name, body in secs.items():
        assert len(re.sub(r"\s", "", body)) >= 40, f"## {name} 內容太短"
    for name, rel in QUOTES.items():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            artifact = f.read()
        quoted = _quoted_lines(secs[name])
        assert any(q in artifact for q in quoted), f"## {name} 沒有引用 {rel} 裡真的出現的一行"


# ---------------------------------------------------------------- 任務 3

def _client(kv):
    """一段「使用者程式」:只用 KVStore 的介面。換一顆不同的 disk,它不該需要改。"""
    kv.put("a", b"x" * 3)
    kv.put("b", bytes(range(256)) * 4)
    kv.put("a", b"new")
    kv.delete("b")
    kv.put("c", "中文".encode("utf-8"))
    return kv.get("a"), sorted(kv.keys()), kv.get("c").decode("utf-8")


@pytest.mark.parametrize("block_size", [16, 64, 512])
def test_C1_2_block_size_change(block_size):
    from rawdisk import RawDisk
    from kvstore import KVStore
    assert _client(KVStore(RawDisk(n_blocks=512, block_size=block_size))) == (b"new", ["a", "c"], "中文")


def test_C1_2_value_spans_blocks():
    from rawdisk import RawDisk
    from kvstore import KVStore
    disk = RawDisk(n_blocks=256, block_size=64)
    kv = KVStore(disk)
    big = bytes(random.Random(1).randrange(256) for _ in range(1000))
    kv.put("big", big)
    assert kv.get("big") == big
    assert disk.writes > 0


def test_C1_2_overwrite_and_delete():
    from rawdisk import RawDisk
    from kvstore import KVStore
    kv = KVStore(RawDisk())
    kv.put("k", b"1")
    kv.put("k", b"22")
    assert kv.get("k") == b"22" and kv.keys() == ["k"]
    kv.delete("k")
    assert kv.keys() == []
    with pytest.raises(KeyError):
        kv.delete("k")


def test_C1_2_reopen_same_disk():
    """資料必須真的存在 disk 上:用同一顆 disk 開一個新的 KVStore,要讀得到。"""
    from rawdisk import RawDisk
    from kvstore import KVStore
    disk = RawDisk()
    KVStore(disk).put("persist", b"yes")
    assert KVStore(disk).get("persist") == b"yes"


# ---------------------------------------------------------------- 任務 4

def test_C1_3_by_generation_csv():
    from timeline import by_generation, load
    rows = load(os.path.join(ROOT, "data", "milestones.csv"))
    assert len(rows) >= 30
    hw = by_generation(rows, "hardware")
    assert set(hw) >= {0, 1, 2, 3, 4}
    assert "UNIVAC I" in hw[1] and "ENIAC" in hw[0]
    sw = by_generation(rows, "software")
    assert set(sw) >= {1, 2, 3, 4, 5}
    years = [r["year"] for r in rows if r["kind"] == "software" and r["name"] in sw[5]]
    assert years == sorted(years)                      # 每一代依年份排序


def test_C1_3_moore_matches_dataset():
    from timeline import load, moore
    cpus = [r for r in load(os.path.join(ROOT, "data", "milestones.csv")) if r["kind"] == "cpu"]
    assert len(cpus) >= 5
    for r in cpus:
        ratio = r["transistors"] / moore(r["year"])
        assert 0.1 <= ratio <= 10, (r["name"], ratio)


def test_C1_4_before_1951():
    from timeline import hardware_generation, software_generation
    assert hardware_generation(1946) == 0 and software_generation(1946) == 0


# ---------------------------------------------------------------- 任務 5

def test_C1_5_toolcheck_missing():
    """PATH 裡拿掉 gdb:要印 gdb: MISSING,並且 exit 1。"""
    d = tempfile.mkdtemp()
    try:
        for bindir in ("/usr/local/bin", "/usr/bin", "/bin"):
            for name in os.listdir(bindir):
                dst = os.path.join(d, name)
                if name != "gdb" and not os.path.exists(dst):
                    os.symlink(os.path.join(bindir, name), dst)
        r = sh(["sh", "src/toolcheck.sh"], env={"PATH": d})
    finally:
        shutil.rmtree(d, ignore_errors=True)
    lines = r.stdout.strip().split("\n")
    assert r.returncode == 1
    assert "gdb: MISSING" in lines
    assert len(lines) == 5 and sum("MISSING" in l for l in lines) == 1
