import os

import pytest

import build_exam
from content import load_chapter
from helpers import fixture_root

FIXTURE_EXAM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures_exam")


def items():
    return load_chapter(FIXTURE_EXAM, 9).bank


def pts(xs):
    return sum(i.points for i in xs)


def test_total_within_tolerance():
    got = build_exam.select(items(), 60, seed=1)
    assert abs(pts(got) - 60) <= 3


def test_type_mix():
    got = build_exam.select(items(), 60, seed=1)
    calc = pts(i for i in got if i.qtype == "計算")
    assert 0.4 <= calc / pts(got) <= 0.6
    assert {i.qtype for i in got} == {"計算", "選擇", "簡答"}


def test_every_concept_represented():
    got = build_exam.select(items(), 40, seed=3)
    assert {i.concept for i in got} == {"C9.1", "C9.2"}


def test_deterministic_and_disjoint():
    a = build_exam.select(items(), 40, seed=7)
    assert [i.qid for i in a] == [i.qid for i in build_exam.select(items(), 40, seed=7)]
    b = build_exam.select(items(), 40, seed=7, exclude={build_exam.key(i) for i in a})
    assert not {build_exam.key(i) for i in a} & {build_exam.key(i) for i in b}


def test_impossible_total_raises():
    with pytest.raises(ValueError, match="題庫不足"):
        build_exam.select(items(), 10_000, seed=1)


def test_make_exam_writes_four_files():
    root = fixture_root(FIXTURE_EXAM)
    out = build_exam.make_exam(root, [9], 40, seed=1, name="demo")
    names = sorted(os.path.basename(p) for p in out)
    assert names == ["demo-A-考卷.html", "demo-A-詳解.html", "demo-B-考卷.html", "demo-B-詳解.html"]
    paper = open(os.path.join(root, "exams", "demo-A-考卷.html"), encoding="utf-8").read()
    key = open(os.path.join(root, "exams", "demo-A-詳解.html"), encoding="utf-8").read()
    assert "對應第 9 章" not in paper and "對應第 9 章" in key
    assert 'class="answer"' not in paper and 'class="answer"' in key
    assert 'data-height="' in paper
