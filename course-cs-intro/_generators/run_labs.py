# -*- coding: utf-8 -*-
"""閘門 3:在 Docker(cs-intro-env)裡實跑每章的 Lab。

用法: python _generators/run_labs.py [章...]

1. 參考解 + 公開 + 隱藏測試:make test 必須成功,而且每個宣告的測試都有跑到、全部通過。
2. 起始碼 + 公開 + 隱藏測試:make build 必須成功(學生拿到就能編譯);
   而且 lab.md 的每個任務,至少有一個「觀念屬於該任務」的測試失敗——證明測試真的在測東西。
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labkit  # noqa: E402
from content import ROOT, available_chapters, load_chapter  # noqa: E402


def check_chapter(root, num):
    errs = []
    ch = load_chapter(root, num)
    if ch.lab is None:
        return errs
    ld = labkit.lab_dir(root, num)
    if not os.path.isdir(ld):
        return [f"第 {num} 章:lab.md 存在但沒有 labs/ch{num:02d}/"]
    declared = labkit.declared_tests(os.path.join(ld, "tests"))
    if not declared:
        return [f"第 {num} 章:labs/ch{num:02d}/tests 裡沒有任何測試"]

    sol = labkit.assemble(root, num, "solution", True)
    try:
        p = labkit.docker_make(sol, "test")
        res = labkit.parse_results(p.stdout)
        missing = sorted(declared - set(res))
        failed = sorted(t for t, ok in res.items() if not ok)
        if missing:
            errs.append(f"第 {num} 章 參考解:這些測試沒有跑到 {missing}")
        if failed:
            errs.append(f"第 {num} 章 參考解:這些測試失敗 {failed}")
        if p.returncode != 0 and not failed:
            errs.append(f"第 {num} 章 參考解:make test 失敗(exit {p.returncode})\n      {labkit.tail(p)}")
    finally:
        shutil.rmtree(sol, ignore_errors=True)

    st = labkit.assemble(root, num, "starter", True)
    try:
        b = labkit.docker_make(st, "build")
        if b.returncode != 0:
            errs.append(f"第 {num} 章 起始碼:make build 失敗,學生拿到無法編譯\n      {labkit.tail(b)}")
            return errs
        p = labkit.docker_make(st, "test")
        res = labkit.parse_results(p.stdout)
        for task in ch.lab.tasks:
            related = sorted(t for t in declared if labkit.concepts_of(t) & set(task.concepts))
            if not related:
                errs.append(f"第 {num} 章 任務 {task.num}:沒有任何測試對應它的觀念 {task.concepts}")
            elif all(res.get(t) is True for t in related):
                errs.append(f"第 {num} 章 任務 {task.num}:起始碼上對應觀念的測試全部通過"
                            f"(測試沒在測東西,或起始碼已經寫好了):{related}")
    finally:
        shutil.rmtree(st, ignore_errors=True)
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
    print(f"\n{'❌' if errs else '✅'} Lab 實跑:{len(errs)} 個錯誤")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
