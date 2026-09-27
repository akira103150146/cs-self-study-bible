# -*- coding: utf-8 -*-
"""Lab 工具:組裝可執行的 Lab 資料夾、打包學生 zip、在 Docker 裡跑 make、解析測試結果。

labs/chNN/ 的原始佈局(starter/、solution/、tests/public/、tests/hidden/)和學生拿到的佈局不同;
assemble() 把它組成學生看到的樣子:

    Makefile  lab.mk  include/ctest.h  src/  tests/  data/

run_labs.py 與 build.py(打包 zip)都用同一個 assemble(),所以「老師驗過的」就是「學生拿到的」。
組裝一律放在系統暫存目錄(ASCII 路徑):repo 路徑含中文,直接掛進 Docker 不保險。
"""
import io
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import uuid
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
        paths = sorted(os.path.relpath(os.path.join(dp, fn), d).replace(os.sep, "/")
                       for dp, _, files in os.walk(d) for fn in files)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for rel in paths:
                # 固定時間戳記與權限:同樣的內容每次打包出一模一樣的 zip(git 才不會每次重建都顯示有變更)
                info = zipfile.ZipInfo(f"{top}/{rel}", date_time=(2026, 1, 1, 0, 0, 0))
                info.external_attr = (0o755 if rel.endswith(".sh") else 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(os.path.join(d, rel), "rb") as f:
                    z.writestr(info, f.read())
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return zip_path


def _tar_of(workdir):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as t:
        for name in sorted(os.listdir(workdir)):
            t.add(os.path.join(workdir, name), arcname=name)
    return buf.getvalue()


def docker_make(workdir, target, timeout=180, retries=1):
    """在 cs-intro-env 裡跑 make -s <target>。

    不用 -v 掛載:把整個資料夾打包成 tar 從標準輸入送進容器、在容器裡解開再 make
    (避開 Windows 檔案共享與中文路徑)。
    Windows 的 Docker Desktop 偶爾會讓容器整個卡住(實測:同一步驟平常 1 秒,偶爾卡到逾時),
    所以逾時就砍掉容器並重試;重試用完仍逾時才回傳 returncode 124。
    """
    for _ in range(retries + 1):
        p = _docker_make_once(workdir, target, timeout)
        if p.returncode != 124:
            return p
    return p


def _docker_make_once(workdir, target, timeout):
    name = f"csintro-{uuid.uuid4().hex[:12]}"
    cmd = ["docker", "run", "--rm", "-i", "--name", name, IMAGE, "sh", "-c",
           f"mkdir -p /work && cd /work && tar -xf - && make -s {target}"]
    try:
        p = subprocess.run(cmd, input=_tar_of(workdir), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        subprocess.run(["docker", "kill", name], capture_output=True)
        return subprocess.CompletedProcess(cmd, 124, (e.stdout or b"").decode("utf-8", "replace"),
                                           f"逾時 {timeout} 秒,容器已砍掉")
    return subprocess.CompletedProcess(cmd, p.returncode, p.stdout.decode("utf-8", "replace"),
                                       p.stderr.decode("utf-8", "replace"))


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
