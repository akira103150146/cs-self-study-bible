import os

import build
from helpers import fixture_root


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def test_build_fixture_writes_all_pages():
    root = fixture_root()
    out = build.build_all(root, [9])
    names = {os.path.basename(p) for p in out}
    assert {"C9-講義-學生版.html", "C9-講義-教師版.html", "C9-題庫-學生版.html",
            "C9-題庫-教師版.html", "C9-Lab.html", "C9-專案.html", "index.html"} <= names


def test_student_bank_hides_answers():
    root = fixture_root()
    build.build_all(root, [9])
    s, t = read(root, "ch09/C9-題庫-學生版.html"), read(root, "ch09/C9-題庫-教師版.html")
    for cls in ("answer", "ans-body", "traps", "rubric-note"):
        assert f'class="{cls}"' not in s
    assert 'class="answer"' in t and 'class="traps"' in t and 'class="rubric-note"' in t
    assert s.count('class="workspace"') == 3


def test_student_notes_hide_teacher_blocks():
    root = fixture_root()
    build.build_all(root, [9])
    s, t = read(root, "ch09/C9-講義-學生版.html"), read(root, "ch09/C9-講義-教師版.html")
    for cls in ("ans-body", "deep", "misstep", "teach-tip"):
        assert f'class="{cls}"' not in s and f'class="{cls}"' in t
    assert 'class="followup"' in s and "C9.1" in s


def test_lab_and_index_pages():
    root = fixture_root()
    build.build_all(root, [9])
    lab = read(root, "ch09/C9-Lab.html")
    assert "任務 1" in lab and "int add(int a, int b);" in lab and "C9-starter.zip" in lab
    idx = read(root, "index.html")
    assert "ch09/C9-講義-學生版.html" in idx and "Test Part" in idx
