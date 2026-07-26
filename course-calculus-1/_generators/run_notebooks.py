# -*- coding: utf-8 -*-
"""逐 cell 執行所有 notebook(Agg backend),任一失敗回傳 exit 1。"""
import io, os, sys, json, glob, traceback, warnings
import matplotlib

matplotlib.use("Agg")
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(path):
    nb = json.load(io.open(path, encoding="utf-8"))
    g = {"__name__": "__main__"}
    buf, old = io.StringIO(), sys.stdout
    for i, c in enumerate(nb["cells"], 1):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if src.strip().startswith("!") or "input(" in src:
            continue
        try:
            sys.stdout = buf
            exec(compile(src, f"{path}#cell{i}", "exec"), g)
        except Exception:
            sys.stdout = old
            print(f"❌ {os.path.relpath(path, ROOT)} cell {i} 失敗")
            print("   源碼:", src[:300].replace("\n", "\n   "))
            print(traceback.format_exc(limit=3))
            return False
        finally:
            sys.stdout = old
    tail = [l for l in buf.getvalue().strip().split("\n") if l.strip()][-2:]
    print(f"✅ {os.path.relpath(path, ROOT)}")
    for l in tail:
        print("      ", l[:140])
    return True


if __name__ == "__main__":
    nbs = sorted(glob.glob(os.path.join(ROOT, "week*", "*.ipynb")))
    if not nbs:
        print("(尚無 notebook)")
        sys.exit(0)
    sys.exit(0 if all([run(p) for p in nbs]) else 1)
