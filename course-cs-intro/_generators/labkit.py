# -*- coding: utf-8 -*-
"""Lab 工具:組裝可執行的 Lab 資料夾、打包學生 zip、在 Docker 裡跑 make、解析測試結果。

labs/chNN/ 的原始佈局(starter/、solution/、tests/public/、tests/hidden/)和學生拿到的佈局不同;
assemble() 把它組成學生看到的樣子:

    Makefile  lab.mk  include/ctest.h  src/  tests/  data/

run_labs.py 與 build.py(打包 zip)都用同一個 assemble(),所以「老師驗過的」就是「學生拿到的」。
組裝一律放在系統暫存目錄(ASCII 路徑):repo 路徑含中文,直接掛進 Docker 不保險。
"""
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

IMAGE = "cs-intro-env"
RESULT_CTEST = re.compile(r"^(PASS|FAIL) (\w+)", re.M)
RESULT_PYTEST = re.compile(r"^(PASSED|FAILED|ERROR) \S+::(\w+)", re.M)
TEST_C = re.compile(r"^\s*TEST\((\w+)\)", re.M)
TEST_PY = re.compile(r"^\s*def (test_\w+)\s*\(", re.M)
CONCEPT_IN_NAME = re.compile(r"C(\d+)_(\d+)_")


def lab_dir(root, num):
    return os.path.join(root, "labs", f"ch{num:02d}")


def _is_binary(data):
    return b"\0" in data[:8192]


def _copy_lf(src, dst):
    """複製檔案;文字檔一律轉成 LF(Makefile 有 CR 會報 missing separator)。"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, "rb") as f:
        data = f.read()
    if not _is_binary(data):
        data = data.replace(b"\r\n", b"\n")
    with open(dst, "wb") as f:
        f.write(data)


def _copy_tree_lf(src, dst):
    for dirpath, _, files in os.walk(src):
        for fn in files:
            s = os.path.join(dirpath, fn)
            _copy_lf(s, os.path.join(dst, os.path.relpath(s, src)))


def _test_files(d):
    out = []
    for dirpath, _, files in os.walk(d):
        out += [os.path.join(dirpath, f) for f in files if f.startswith("test_") and f.endswith((".c", ".py"))]
    return sorted(out)


def assemble(root, num, variant, include_hidden):
    """組出學生看到的 Lab 資料夾,回傳路徑(系統暫存目錄,ASCII)。variant = 'starter' 或 'solution'。"""
    if variant not in ("starter", "solution"):
        raise ValueError(variant)
    src = lab_dir(root, num)
    d = tempfile.mkdtemp(prefix="csintro-")
    for fn in ("Makefile", "lab.mk"):
        if os.path.exists(os.path.join(src, fn)):
            _copy_lf(os.path.join(src, fn), os.path.join(d, fn))
    _copy_tree_lf(os.path.join(src, variant), d)          # variant/src/… → src/…(以及 variant 底下其他檔案)
    subs = ["public"] + (["hidden"] if include_hidden else [])
    seen = set()
    for sub in subs:
        t = os.path.join(src, "tests", sub)
        if not os.path.isdir(t):
            continue
        for dirpath, _, files in os.walk(t):
            for fn in files:
                rel = os.path.relpath(os.path.join(dirpath, fn), t)
                if rel in seen:
                    raise ValueError(f"labs/ch{num:02d}/tests:public 與 hidden 有同名檔案 {rel}")
                seen.add(rel)
                _copy_lf(os.path.join(dirpath, fn), os.path.join(d, "tests", rel))
    if os.path.isdir(os.path.join(src, "data")):
        _copy_tree_lf(os.path.join(src, "data"), os.path.join(d, "data"))
    if any(p.endswith(".c") for p in _test_files(os.path.join(d, "tests"))):
        _copy_lf(os.path.join(root, "labs", "common", "ctest.h"), os.path.join(d, "include", "ctest.h"))
    return d


def make_zip(root, num, zip_path):
    """學生 zip:starter + 公開測試,頂層資料夾 chNN/。"""
    d = assemble(root, num, "starter", False)
    try:
        with open(os.path.join(d, ".gitignore"), "w", newline="\n") as f:
            f.write("build/\n__pycache__/\n")
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        top = f"ch{num:02d}"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for dirpath, _, files in os.walk(d):
                for fn in sorted(files):
                    p = os.path.join(dirpath, fn)
                    z.write(p, f"{top}/{os.path.relpath(p, d).replace(os.sep, '/')}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return zip_path


def docker_make(workdir, target, timeout=900):
    return subprocess.run(["docker", "run", "--rm", "-v", f"{workdir}:/work", IMAGE, "make", "-s", target],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)


def parse_results(stdout):
    """ctest(PASS/FAIL name)與 pytest -rA(PASSED/FAILED/ERROR file::name)的結果 → {測試名: 是否通過}。"""
    out = {}
    for status, name in RESULT_CTEST.findall(stdout):
        out[name] = status == "PASS"
    for status, name in RESULT_PYTEST.findall(stdout):
        out[name] = out.get(name, True) and status == "PASSED"
    return out


def declared_tests(tests_dir):
    """掃 test_*.c 的 TEST(name) 與 test_*.py 的 def test_xxx → 測試名集合。"""
    names = set()
    for p in _test_files(tests_dir):
        with open(p, encoding="utf-8") as f:
            s = f.read()
        names |= set((TEST_C if p.endswith(".c") else TEST_PY).findall(s))
    return names


def concepts_of(test_name):
    """'C3_2_twos' / 'test_C3_2_twos' → {'C3.2'}。"""
    return {f"C{a}.{b}" for a, b in CONCEPT_IN_NAME.findall(test_name)}


def tail(proc, n=30):
    lines = (proc.stdout + "\n" + proc.stderr).strip().split("\n")
    return "\n      ".join(lines[-n:])
