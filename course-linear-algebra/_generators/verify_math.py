# -*- coding: utf-8 -*-
"""用 sympy 驗算內容檔裡 ## 驗算 的每一行。用法: python _generators/verify_math.py [週次...]

每一行是一個會得到 True 的 Python 運算式,在 sympy 命名空間裡執行,例如:
    Matrix([[1, 1, 5], [1, -1, 1]]).rref()[0] == Matrix([[1, 0, 3], [0, 1, 2]])
    simplify(A*x - b) == zeros(2, 1)
可用的符號:x1..x6、x、y、z、t、s、h、k(實數)。
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
from mdtools import ContentError

NS = {k: getattr(sp, k) for k in dir(sp) if not k.startswith("_")}
NS.update({name: sp.Symbol(name, real=True)
           for name in ["x1", "x2", "x3", "x4", "x5", "x6", "x", "y", "z", "t", "s", "h", "k"]})


def run(label, expr):
    try:
        ok = eval(expr, dict(NS))
        ok = bool(ok)
    except Exception as e:                      # 運算式本身寫錯也算失敗,並印出原因
        print(f"  ❌ {label}\n     → 執行錯誤:{type(e).__name__}: {e}")
        return False
    print(f"  {'✅' if ok else '❌'} {label}")
    return ok


def main():
    try:
        weeks = [int(a) for a in sys.argv[1:]] or C.available_weeks()
        total = bad = 0
        for wk in weeks:
            checks = C.all_checks(C.load_week(wk))
            print(f"=== W{wk}: {len(checks)} 項驗算 ===")
            for label, expr in checks:
                total += 1
                bad += not run(label, expr)
    except ContentError as e:
        print(f"❌ 內容格式錯誤:{e}")
        return 1
    print(f"\n共驗算 {total} 項,失敗 {bad} 項")
    return 1 if bad or not total else 0


if __name__ == "__main__":
    sys.exit(main())
