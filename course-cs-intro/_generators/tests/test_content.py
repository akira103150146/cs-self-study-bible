import pytest

from content import ContentError, all_checks, load_chapter, load_course
from helpers import break_file, fixture_root


def test_load_fixture_chapter():
    ch = load_chapter(fixture_root(), 9)
    assert ch.title == "Fixture Chapter" and ch.lang == "c"
    assert [c.id for c in ch.concepts] == ["C9.1"]
    assert [b.qtype for b in ch.bank] == ["計算", "選擇", "簡答"]
    assert [b.points for b in ch.bank] == [4, 3, 6]
    assert ch.bank[1].answer == "B" and [t.key for t in ch.bank[1].traps] == ["A", "C"]
    assert ch.lab.tasks[0].concepts == ["C9.1"]
    assert ch.projects[0].rubric[0] == ["項目", "配分", "通過標準"]


def test_load_course():
    c = load_course(fixture_root())
    assert c["name"] == "測試課程" and c["parts"][0][2] == [9]


def test_checks_carry_answer_text():
    ch = load_chapter(fixture_root(), 9)
    bank_checks = [c for c in all_checks(ch) if c.answer is not None]
    concept_checks = [c for c in all_checks(ch) if c.answer is None]
    assert [c.answer for c in bank_checks] == ["42"]
    assert [c.expr for c in concept_checks] == ["2 + 2 == 4"]


@pytest.mark.parametrize("rel,old,new,msg", [
    ("01-demo.md", "id: C9.1", "id: C9.2", "id"),
    ("01-demo.md", "## 後面會用到", "## 後面用到", "不認得的段落"),
    ("01-demo.md", 'lab_hook: "任務 1:`add()`"', "", "lab_hook"),
    ("bank.md", "· C9.1 · 選擇", "· C9.7 · 選擇", "C9.7"),
    ("bank.md", "### 迷思對照", "### 迷思", "迷思"),
    ("bank.md", "- **C** 多加了一 → 回看 C9.1", "", "錯誤選項"),
    ("bank.md", "== ANS", "== '42'", "ANS"),
    ("bank.md", "### 評分要點", "### 要點", "要點"),
    ("bank.md", "## Q2", "## Q5", "連號"),
    ("lab.md", "```c interface", "```c", "interface"),
    ("lab.md", " · C9.1", "", "任務"),
    ("projects.md", "### 評分規準", "### 評分", "評分"),
])
def test_format_errors_are_reported(rel, old, new, msg):
    root = fixture_root()
    break_file(root, rel, old, new)
    with pytest.raises(ContentError, match=msg):
        load_chapter(root, 9)


def test_course_outline_entries_must_be_pairs():
    import os
    root = fixture_root()
    p = os.path.join(root, "content", "course.yaml")
    s = open(p, encoding="utf-8").read().replace("9: [Fixture Chapter, 測試用]", "9: [Fixture, Chapter, 測試用]")
    open(p, "w", encoding="utf-8").write(s)
    with pytest.raises(ContentError, match="outline"):
        load_course(root)
