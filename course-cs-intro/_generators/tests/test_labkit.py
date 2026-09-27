import os
import zipfile

import build
import labkit
import run_labs
import verify
import verify_coverage
from helpers import break_file, fixture_root


def test_assemble_uses_ascii_tmp():
    d = labkit.assemble(fixture_root(), 9, "solution", True)
    assert d.isascii() and os.path.exists(os.path.join(d, "include", "ctest.h"))
    assert sorted(os.listdir(os.path.join(d, "tests"))) == ["test_demo.c", "test_demo_hidden.c"]
    with open(os.path.join(d, "src", "demo.c")) as f:
        assert "a + b" in f.read()


def test_parse_results_both_formats():
    out = ("PASS C9_1_a\nFAIL C9_1_b\n    x.c:3: boom\n"
           "PASSED tests/t.py::test_C9_1_c\nFAILED tests/t.py::test_C9_1_d - x\n"
           "ERROR tests/t.py::test_C9_1_e - y\n")
    assert labkit.parse_results(out) == {"C9_1_a": True, "C9_1_b": False, "test_C9_1_c": True,
                                         "test_C9_1_d": False, "test_C9_1_e": False}


def test_declared_tests_and_concepts():
    root = fixture_root()
    names = labkit.declared_tests(os.path.join(root, "labs", "ch09", "tests"))
    assert names == {"C9_1_add_small", "C9_1_add_negative"}
    assert labkit.concepts_of("C9_1_add_small") == {"C9.1"}
    assert labkit.concepts_of("test_C12_3_x") == {"C12.3"}


def test_run_labs_fixture_ok():
    assert run_labs.run(fixture_root(), [9]) == []


def test_run_labs_catches_starter_that_already_passes():
    root = fixture_root()
    p = os.path.join(root, "labs", "ch09", "starter", "src", "demo.c")
    with open(p, "w", newline="\n") as f:
        f.write('#include "demo.h"\nint add(int a, int b) { return a + b; }\n')
    errs = run_labs.run(root, [9])
    assert any("任務 1" in e for e in errs), errs


def test_run_labs_catches_wrong_solution():
    root = fixture_root()
    p = os.path.join(root, "labs", "ch09", "solution", "src", "demo.c")
    with open(p, "w", newline="\n") as f:
        f.write('#include "demo.h"\nint add(int a, int b) { return a - b; }\n')
    errs = run_labs.run(root, [9])
    assert any("參考解" in e for e in errs), errs


def test_coverage_ok_then_missing_test():
    root = fixture_root()
    assert verify_coverage.run(root, [9]) == []
    for sub in ("public", "hidden"):
        d = os.path.join(root, "labs", "ch09", "tests", sub)
        for f in os.listdir(d):
            p = os.path.join(d, f)
            s = open(p).read().replace("C9_1_", "X_")
            open(p, "w", newline="\n").write(s)
    errs = verify_coverage.run(root, [9])
    assert any("C9.1" in e and "測試" in e for e in errs), errs


def test_coverage_unknown_id_in_tests():
    root = fixture_root()
    p = os.path.join(root, "labs", "ch09", "tests", "public", "test_demo.c")
    s = open(p).read().replace("C9_1_add_small", "C9_4_add_small")
    open(p, "w", newline="\n").write(s)
    errs = verify_coverage.run(root, [9])
    assert any("C9.4" in e for e in errs), errs


def test_zip_is_lf_and_has_no_hidden():
    root = fixture_root()
    p = os.path.join(root, "labs", "ch09", "Makefile")
    data = open(p, "rb").read().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    open(p, "wb").write(data)
    build.build_all(root, [9])
    z = zipfile.ZipFile(os.path.join(root, "ch09", "C9-starter.zip"))
    names = z.namelist()
    assert "ch09/Makefile" in names and "ch09/include/ctest.h" in names and "ch09/src/demo.c" in names
    assert not any("hidden" in n or "solution" in n for n in names)
    assert b"\r" not in z.read("ch09/Makefile")
    assert verify.run(root, [9]) == []


def test_verify_catches_leaky_student_bank():
    root = fixture_root()
    build.build_all(root, [9])
    p = os.path.join(root, "ch09", "C9-題庫-學生版.html")
    s = open(p, encoding="utf-8").read().replace('<div class="workspace"', '<div class="answer">42</div><div class="workspace"', 1)
    open(p, "w", encoding="utf-8").write(s)
    errs = verify.run(root, [9])
    assert any("answer" in e for e in errs), errs


def test_verify_catches_zip_with_hidden_test():
    root = fixture_root()
    build.build_all(root, [9])
    zp = os.path.join(root, "ch09", "C9-starter.zip")
    with zipfile.ZipFile(zp, "a") as z:
        z.writestr("ch09/tests/test_demo_hidden.c", "x")
    errs = verify.run(root, [9])
    assert any("hidden" in e or "隱藏" in e for e in errs), errs


def test_docker_make_timeout_kills_container():
    import subprocess
    import tempfile
    d = tempfile.mkdtemp(prefix="csintro-")
    with open(os.path.join(d, "Makefile"), "w", newline="\n") as f:
        f.write("slow:\n\tsleep 60\n")
    p = labkit.docker_make(d, "slow", timeout=5)
    assert p.returncode == 124 and "逾時" in p.stderr
    ps = subprocess.run(["docker", "ps", "--filter", "name=csintro-", "-q"],
                        capture_output=True, text=True).stdout.strip()
    assert ps == ""
