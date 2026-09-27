# -*- coding: utf-8 -*-
"""閘門 2:執行觀念檔 ## 驗算 與題庫 ### 驗算 裡的每一行。

用法: python _generators/verify_answers.py [章...]

每一行是一個 Python 運算式,結果必須**恰好是 True**(False、非布林值、例外都算錯)。
題庫計算題的驗算可以用 ANS(= 該題 ### 答案 的純文字),拿題目印出來的答案和獨立算出的值比對。
可用的名稱:math、struct、itertools、collections、fractions,以及 checklib 的全部函式。
"""
import collections
import fractions
import itertools
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checklib  # noqa: E402
from content import ROOT, all_checks, available_chapters, load_chapter  # noqa: E402

BASE_NS = {"math": math, "struct": struct, "itertools": itertools,
           "collections": collections, "fractions": fractions,
           **{k: getattr(checklib, k) for k in checklib.__all__}}


def run(root=ROOT, chapters=None):
    errs = []
    for n in chapters or available_chapters(root):
        for c in all_checks(load_chapter(root, n)):
            ns = dict(BASE_NS)
            if c.answer is not None:
                ns["ANS"] = c.answer
            try:
                got = eval(c.expr, ns)   # noqa: S307 — 只執行本 repo 內容檔裡的驗算式
            except Exception as e:
                errs.append(f"{c.label}:執行錯誤 {type(e).__name__}: {e}")
                continue
            if got is not True:
                errs.append(f"{c.label}:結果不是 True(得到 {got!r})")
    return errs


def main():
    wanted = [int(a) for a in sys.argv[1:]] or None
    errs = run(ROOT, wanted)
    for e in errs:
        print("🔴", e)
    print(f"\n{'❌' if errs else '✅'} 驗算:{len(errs)} 個錯誤")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
