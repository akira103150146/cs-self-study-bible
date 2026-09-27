# -*- coding: utf-8 -*-
"""閘門 4:觀念涵蓋度。

用法: python _generators/verify_coverage.py [章...]

每個觀念 ID 都要有:至少 1 題筆試(bank.md)、至少 1 個核心 Lab 任務(lab.md)、至少 1 個測試(名稱帶 C3_2_)。
反過來,題庫、任務、測試裡出現本章不存在的觀念 ID 也算錯。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labkit  # noqa: E402
from content import ROOT, available_chapters, load_chapter  # noqa: E402


def check_chapter(root, num):
    ch = load_chapter(root, num)
    ids = [c.id for c in ch.concepts]
    bank = {q.concept for q in ch.bank}
    tasks = {i for t in (ch.lab.tasks if ch.lab else []) for i in t.concepts}
    tests = {}
    tdir = os.path.join(labkit.lab_dir(root, num), "tests")
    for name in (labkit.declared_tests(tdir) if os.path.isdir(tdir) else set()):
        for cid in labkit.concepts_of(name):
            tests.setdefault(cid, []).append(name)
    errs = []
    for cid in ids:
        lacks = [what for what, have in (("筆試題", cid in bank), ("Lab 任務", cid in tasks),
                                         ("測試", cid in tests)) if not have]
        if lacks:
            errs.append(f"第 {num} 章 {cid}:缺 {'、'.join(lacks)}")
    for what, found in (("題庫", bank), ("Lab 任務", tasks), ("測試", set(tests))):
        for cid in sorted(found - set(ids)):
            extra = f"({', '.join(sorted(tests[cid]))})" if what == "測試" else ""
            errs.append(f"第 {num} 章 {what}出現不存在的觀念 {cid}{extra}")
    return errs


def run(root=ROOT, chapters=None):
    errs = []
    for n in chapters or available_chapters(root):
        errs += check_chapter(root, n)
    return errs


def main():
    wanted = [int(a) for a in sys.argv[1:]] or None
    errs = run(ROOT, wanted)
    for e in errs:
        print("🔴", e)
    print(f"\n{'❌' if errs else '✅'} 涵蓋度:{len(errs)} 個錯誤")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
