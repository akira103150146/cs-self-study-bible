# -*- coding: utf-8 -*-
"""閘門 3:逐格執行所有 notebook(Agg backend),並核對「預期輸出」。

用法: python _generators/run_notebooks.py [週次...]

- 任何一格丟例外 → 失敗。
- 有 metadata.expected_output 的格子:預期輸出的每一行(去掉頭尾空白)都必須依序
  出現在該格的實際輸出裡。實作頁上印給學生看的「預期輸出」因此不可能和實際結果不符。
"""
import contextlib
import glob
import io
import json
import os
import re
import sys
import traceback
import warnings

import matplotlib

matplotlib.use("Agg")
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lines(s):
    return [re.sub(r"\s+", " ", l).strip() for l in s.split("\n") if l.strip()]


def _in_order(expected, actual):
    """expected 的每一行依序出現在 actual 裡(中間可夾其他行,例如學生的預測)。"""
    it = iter(actual)
    return all(any(e == a for a in it) for e in expected)


def run(path):
    nb = json.load(io.open(path, encoding="utf-8"))
    g = {"__name__": "__main__"}
    rel = os.path.relpath(path, ROOT)
    ok, last = True, ""
    for i, c in enumerate(nb["cells"], 1):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if src.strip().startswith("!") or "input(" in src:
            continue
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src, f"{path}#cell{i}", "exec"), g)
        except Exception:
            print(f"❌ {rel} cell {i} 丟出例外")
            print("   源碼:", src[:300].replace("\n", "\n   "))
            print(traceback.format_exc(limit=3))
            return False
        out = buf.getvalue()
        last = out or last
        want = c.get("metadata", {}).get("expected_output")
        if want and not _in_order(_lines(want), _lines(out)):
            ok = False
            print(f"❌ {rel} cell {i}:實際輸出和頁面上的「預期輸出」不符")
            print("   預期:\n     " + "\n     ".join(_lines(want)))
            print("   實際:\n     " + "\n     ".join(_lines(out)))
    if ok:
        n = sum(1 for c in nb["cells"] if c.get("metadata", {}).get("expected_output"))
        print(f"✅ {rel}({n} 格預期輸出全部相符)")
    return ok


if __name__ == "__main__":
    weeks = [int(a) for a in sys.argv[1:]]
    nbs = sorted(glob.glob(os.path.join(ROOT, "week*", "*.ipynb")))
    if weeks:
        nbs = [p for p in nbs if int(re.search(r"week(\d+)", p).group(1)) in weeks]
    if not nbs:
        print("(尚無 notebook)")
        sys.exit(0)
    sys.exit(0 if all([run(p) for p in nbs]) else 1)
