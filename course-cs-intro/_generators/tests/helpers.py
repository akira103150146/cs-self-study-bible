"""產生器測試共用的小工具:把 fixture 複製成一個獨立的課程資料夾,以及把某個檔案「改壞」。"""
import os
import shutil
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.dirname(os.path.dirname(HERE))
FIX = os.path.join(HERE, "fixtures")


def fixture_root(src=FIX):
    """回傳一個暫存的課程資料夾:fixture 的 content/、labs/,再加上真正的 labs/common、版面與樣式。"""
    d = tempfile.mkdtemp(prefix="csintro-fix-")
    shutil.copytree(src, d, dirs_exist_ok=True)
    for rel in (os.path.join("labs", "common"), "_layout", "assets"):
        s = os.path.join(COURSE, rel)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(d, rel), dirs_exist_ok=True)
    return d


def break_file(root, rel, old, new, chapter="ch09"):
    """把 content/<chapter>/<rel> 裡第一個 old 換成 new(old 必須存在)。"""
    p = os.path.join(root, "content", chapter, rel)
    with open(p, encoding="utf-8") as f:
        s = f.read()
    assert old in s, f"{rel} 裡找不到 {old!r}"
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s.replace(old, new, 1))
