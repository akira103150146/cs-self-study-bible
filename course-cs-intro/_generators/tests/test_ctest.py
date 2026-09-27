import os
import shutil
import tempfile

import labkit

HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.join(HERE, "..", "..", "labs", "common")


def lf_copy(src, dst):
    with open(src, "rb") as f:
        data = f.read().replace(b"\r\n", b"\n")
    with open(dst, "wb") as f:
        f.write(data)


def run_selftest():
    d = tempfile.mkdtemp(prefix="csintro-")
    for sub in ("include", "src", "tests"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    lf_copy(os.path.join(HERE, "ctest_selftest", "tests", "test_selftest.c"),
            os.path.join(d, "tests", "test_selftest.c"))
    lf_copy(os.path.join(COMMON, "ctest.h"), os.path.join(d, "include", "ctest.h"))
    lf_copy(os.path.join(COMMON, "Makefile.c"), os.path.join(d, "Makefile"))
    try:
        return labkit.docker_make(d, "test CTEST_TIMEOUT=2", timeout=180)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_ctest_isolation():
    r = run_selftest()
    out = r.stdout
    assert "PASS C9_1_passes" in out, out + r.stderr
    assert "FAIL C9_1_fails_eq" in out and "expected 5, got 4" in out
    assert "FAIL C9_1_segfault" in out and "crashed" in out
    assert "FAIL C9_1_infinite" in out and "timeout" in out
    assert "PASS C9_1_after_crash" in out          # 前面當掉不影響後面
    assert "ctest: 2 passed, 3 failed" in out
    assert r.returncode != 0
