# -*- coding: utf-8 -*-
"""用 sympy 驗算答案。每週資料模組在 ANSWER_CHECKS 登記 (描述, 算式, 期望值)。

用法: python verify_math.py [週次...]   (在 _generators/ 底下執行)
"""
import os, sys, importlib
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# 固定的符號命名空間。刻意不用 e / N —— 它們在 sympy 是 E(自然底數)與 N()(數值化),
# 直接寫會被解析成別的東西。用 eps / Nn。
NS = {
    # x 宣告為實數:這是微積分課,不宣告的話 sympy 為了顧慮複數,
    # 連 sqrt(cosh(x)**2) = cosh(x) 這種顯然的化簡都不敢做。
    "x": sp.Symbol("x", real=True),
    "h": sp.Symbol("h", real=True),
    "d": sp.Symbol("d", positive=True),      # delta
    "eps": sp.Symbol("eps", positive=True),  # epsilon
    "M": sp.Symbol("M", positive=True),
    "Nn": sp.Symbol("Nn", positive=True),
    "a": sp.Symbol("a"),
    "n": sp.Symbol("n", integer=True, positive=True),
    "t": sp.Symbol("t"),
    "y": sp.Symbol("y"),
}


def check(expr, expected, label=""):
    """expr/expected 為 sympy 可解析字串或 sympy 物件。相等回 True。"""
    try:
        a = sp.sympify(expr, locals=NS) if isinstance(expr, str) else expr
        b = sp.sympify(expected, locals=NS) if isinstance(expected, str) else expected
    except (sp.SympifyError, SyntaxError, TypeError, AttributeError) as e:
        print(f"  ❌ {label or expr}  ->  無法解析: {e}")
        return False
    ok = sp.simplify(a - b) == 0
    if not ok:
        try:
            ok = abs(complex(a) - complex(b)) < 1e-9
        except (TypeError, ValueError):
            ok = False
    print(f"  {'✅' if ok else '❌'} {label or expr}  ->  got {a}, want {b}")
    return ok


def main():
    weeks = [int(a) for a in sys.argv[1:]] or list(range(1, 19))
    bad = total = 0
    for wk in weeks:
        try:
            mod = importlib.import_module(f"weeks.w{wk:02d}")
        except ModuleNotFoundError:
            continue
        checks = getattr(mod, "ANSWER_CHECKS", [])
        print(f"=== W{wk}: {len(checks)} 項驗算 ===")
        for label, expr, expected in checks:
            total += 1
            if not check(expr, expected, label):
                bad += 1
    print(f"\n共驗算 {total} 項,失敗 {bad} 項")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
