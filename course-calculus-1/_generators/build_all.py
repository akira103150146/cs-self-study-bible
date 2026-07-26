# -*- coding: utf-8 -*-
"""一鍵重生。用法: python build_all.py [週次...]  (不給則全部)"""
import os, sys, importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_lesson, build_examples, build_lab

CAPSTONE_WEEKS = {17}


def main():
    weeks = [int(a) for a in sys.argv[1:]] or list(range(1, 19))
    made = 0
    for wk in weeks:
        try:
            mod = importlib.import_module(f"weeks.w{wk:02d}")
        except ModuleNotFoundError:
            print(f"—  W{wk} 尚無資料,跳過")
            continue
        w = getattr(mod, "WEEK", None)
        if w is not None:
            if w.lesson:
                build_lesson.render(w)
            if w.concepts:
                build_examples.render(w)
            if w.labs:
                build_lab.render(w, capstone=(wk in CAPSTONE_WEEKS))
        exam = getattr(mod, "EXAM", None)
        if exam is not None:
            import build_exam
            build_exam.render(exam, with_solutions=False)
            build_exam.render(exam, with_solutions=True)
        print(f"✅ W{wk} 產出完成")
        made += 1
    print(f"\n共產出 {made} 週")


if __name__ == "__main__":
    main()
