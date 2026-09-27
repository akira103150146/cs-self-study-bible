import verify_answers
from helpers import break_file, fixture_root


def test_fixture_passes():
    assert verify_answers.run(fixture_root(), [9]) == []


def test_check_must_be_bool():
    root = fixture_root()
    break_file(root, "01-demo.md", "2 + 2 == 4", "2 + 2")
    errs = verify_answers.run(root, [9])
    assert len(errs) == 1 and "不是 True" in errs[0]


def test_wrong_answer_detected():
    root = fixture_root()
    break_file(root, "bank.md", "`42`", "`43`")
    errs = verify_answers.run(root, [9])
    assert len(errs) == 1 and "Q1" in errs[0]


def test_exception_reported():
    root = fixture_root()
    break_file(root, "01-demo.md", "2 + 2 == 4", "undefined_fn(2) == 4")
    errs = verify_answers.run(root, [9])
    assert len(errs) == 1 and "NameError" in errs[0]
