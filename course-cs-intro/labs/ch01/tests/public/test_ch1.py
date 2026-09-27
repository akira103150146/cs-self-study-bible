"""第 1 章 Lab 公開測試。在 Lab 資料夾執行 make test(會先 make build)。"""
import os
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(cmd, stdin="", env=None):
    return subprocess.run(cmd, cwd=ROOT, input=stdin, capture_output=True, text=True,
                          shell=isinstance(cmd, str), env=env, timeout=60)


# ---------------------------------------------------------------- 任務 1:同一支程式,兩種語言

def test_C1_1_sum_c_basic():
    r = sh(["./build/sum"], "1 2 3\n-4 10\n")
    assert r.returncode == 0 and r.stdout.strip() == "12"


def test_C1_1_sum_py_basic():
    r = sh(["python3", "src/sum.py"], "1 2 3\n-4 10\n")
    assert r.returncode == 0 and r.stdout.strip() == "12"


# ---------------------------------------------------------------- 任務 2:往下看每一層

@pytest.fixture(scope="module")
def pipeline():
    r = sh(["make", "-s", "pipeline"])
    assert r.returncode == 0, r.stdout + r.stderr
    return r


def test_C1_4_pipeline_artifacts(pipeline):
    def file_kind(p):
        return sh(["file", "-b", p]).stdout
    with open(os.path.join(ROOT, "build", "sum.i")) as f:
        pre = f.read()
    assert "int main" in pre and "#include" not in pre           # 前處理後沒有 #include
    with open(os.path.join(ROOT, "build", "sum.s")) as f:
        assert "main:" in f.read()                               # 組合語言
    assert "relocatable" in file_kind("build/sum.o")             # 目的檔(還沒連結)
    assert "executable" in file_kind("build/sum.linked")         # 連結後的執行檔
    with open(os.path.join(ROOT, "build", "sum.dis")) as f:
        assert "<main>:" in f.read()                             # 反組譯
    with open(os.path.join(ROOT, "build", "sum.pyc.txt")) as f:
        assert "LOAD" in f.read()                                # Python bytecode


# ---------------------------------------------------------------- 任務 3:抽象的價值

def test_C1_2_put_get():
    from rawdisk import RawDisk
    from kvstore import KVStore
    kv = KVStore(RawDisk())
    kv.put("name", b"Ada")
    kv.put("year", b"1843")
    assert kv.get("name") == b"Ada" and kv.get("year") == b"1843"
    assert sorted(kv.keys()) == ["name", "year"]


def test_C1_2_missing_key():
    from rawdisk import RawDisk
    from kvstore import KVStore
    kv = KVStore(RawDisk())
    with pytest.raises(KeyError):
        kv.get("nope")


# ---------------------------------------------------------------- 任務 4:計算的歷史是資料

def test_C1_3_generation_bounds():
    from timeline import hardware_generation
    assert [hardware_generation(y) for y in (1950, 1951, 1958, 1959, 1965, 1970, 1971, 2024)] == \
           [0, 1, 1, 2, 3, 3, 4, 4]


def test_C1_4_software_generation():
    from timeline import software_generation
    assert [software_generation(y) for y in (1951, 1959, 1964, 1965, 1971, 1989, 1990, 2024)] == \
           [1, 2, 2, 3, 4, 4, 5, 5]


def test_C1_3_moore_1971_1981():
    from timeline import moore
    assert moore(1971) == 2300 and moore(1981) == 73600 and moore(1973) == 4600


# ---------------------------------------------------------------- 任務 5:你的工具鏈

def test_C1_5_toolcheck_all_present():
    r = sh(["sh", "src/toolcheck.sh"])
    lines = r.stdout.strip().split("\n")
    assert r.returncode == 0
    assert [l.split(":")[0] for l in lines] == ["gcc", "make", "python3", "git", "gdb"]
    assert all("MISSING" not in l and len(l.split(":", 1)[1].strip()) > 0 for l in lines)
