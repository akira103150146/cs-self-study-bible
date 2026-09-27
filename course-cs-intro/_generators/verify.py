# -*- coding: utf-8 -*-
"""閘門 1:結構稽核(檢查「產出物」)。用法: python _generators/verify.py [章...]

內容格式的錯誤在 build 階段就會被 content.py 擋下;這裡查的是產出物本身:
兩版題幹一致、學生版不洩答案、作答區數量、數學式跳脫、連結、學生 zip 乾淨(沒有參考解、沒有隱藏測試、沒有 CR)。
"""
import html as _html
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labkit  # noqa: E402
from content import ROOT, available_chapters  # noqa: E402

TEACHER_ONLY_NOTES = ("ans-body", "deep", "misstep", "teach-tip", "t-note")
TEACHER_ONLY_BANK = ("answer", "ans-body", "traps", "rubric-note", "t-note")


def _rd(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def _text(s):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def problems(s):
    return [_text(x) for x in re.findall(r'<div class="problem">(.*?)</div>', s, re.S)]


class Checker:
    def __init__(self, root):
        self.root, self.errs = root, []

    def err(self, where, msg):
        self.errs.append(f"[{where}] {msg}")

    def exists(self, rel):
        return os.path.exists(os.path.join(self.root, rel))

    def pair(self, num, kind, teacher_only, n_items_marker):
        sp = f"ch{num:02d}/C{num}-{kind}-學生版.html"
        tp = f"ch{num:02d}/C{num}-{kind}-教師版.html"
        if not self.exists(sp):
            return
        if not self.exists(tp):
            self.err(sp, "有學生版但缺教師版")
            return
        s, t = _rd(self.root, sp), _rd(self.root, tp)
        if problems(s) != problems(t):
            self.err(f"C{num} {kind}", "兩版題幹不一致")
        for cls in teacher_only:
            if f'class="{cls}"' in s:
                self.err(sp, f"學生版出現教師專用區塊 .{cls}(洩答案)")
        n, ws = s.count(n_items_marker), s.count('class="workspace"')
        if n != ws:
            self.err(sp, f"{n} 題但作答區有 {ws} 個")

    def page(self, rel):
        s = _rd(self.root, rel)
        body = s.split("<body>", 1)[-1]
        prose = re.sub(r"<pre>.*?</pre>|<code>.*?</code>", "", body, flags=re.S)
        for m in re.finditer(r"(?<!\$)\$([^$]{1,400}?)\$(?!\$)", prose):
            if "<" in m.group(1) or ">" in m.group(1):
                self.err(rel, f"數學式裡有未跳脫的 < 或 >:${m.group(1)[:60]}$")
        d = os.path.dirname(os.path.join(self.root, rel))
        for h in re.findall(r'(?:href|src)="([^"#:]+\.(?:html|css|zip))"', s):
            if not os.path.exists(os.path.normpath(os.path.join(d, h))):
                self.err(rel, f"連結壞掉:{h}")

    def zipfile(self, num):
        ld = labkit.lab_dir(self.root, num)
        if not os.path.isdir(ld):
            return
        rel = f"ch{num:02d}/C{num}-starter.zip"
        if not self.exists(rel):
            self.err(rel, "有 labs/ 但沒有產出學生 zip")
            return
        top = f"ch{num:02d}/"
        hidden = set()
        hd = os.path.join(ld, "tests", "hidden")
        for dirpath, _, files in os.walk(hd):
            hidden |= {os.path.relpath(os.path.join(dirpath, f), hd).replace(os.sep, "/") for f in files}
        with zipfile.ZipFile(os.path.join(self.root, rel)) as z:
            names = z.namelist()
            if top + "Makefile" not in names or not any(n.startswith(top + "src/") for n in names):
                self.err(rel, "zip 缺 Makefile 或 src/")
            for n in names:
                if not n.startswith(top):
                    self.err(rel, f"zip 裡有不在 {top} 底下的檔案:{n}")
                if "solution" in n or "hidden" in n:
                    self.err(rel, f"zip 裡有參考解或隱藏測試的路徑:{n}")
                if n.startswith(top + "tests/") and n[len(top + "tests/"):] in hidden:
                    self.err(rel, f"zip 裡有隱藏測試檔 {n}")
                data = z.read(n)
                if b"\0" not in data[:8192] and b"\r" in data:
                    self.err(rel, f"zip 裡的 {n} 有 CR(Windows 行尾),Docker 裡的 make/sh 會壞")
            sd = os.path.join(ld, "starter")
            for dirpath, _, files in os.walk(sd):
                for f in files:
                    p = os.path.join(dirpath, f)
                    zn = top + os.path.relpath(p, sd).replace(os.sep, "/")
                    with open(p, "rb") as fh:
                        want = fh.read()
                    if b"\0" not in want[:8192]:
                        want = want.replace(b"\r\n", b"\n")
                    if zn not in names:
                        self.err(rel, f"zip 缺起始碼 {zn}")
                    elif z.read(zn) != want:
                        self.err(rel, f"zip 裡的 {zn} 和 labs/ 的起始碼不一致(zip 過期,請重建)")

    def css(self):
        css = _rd(self.root, "assets/handout.css")
        for sel, need in ((".workspace {", "min-height"), ('.workspace[data-size="short"]', "min-height")):
            i = css.find(sel)
            if i < 0 or need not in css[i:i + 300]:
                self.err("assets/handout.css", f"{sel} 缺 {need},印出來沒有作答空間")


def run(root=ROOT, chapters=None):
    c = Checker(root)
    for n in chapters or available_chapters(root):
        c.pair(n, "講義", TEACHER_ONLY_NOTES, '<span class="tier ')
        c.pair(n, "題庫", TEACHER_ONLY_BANK, '<div class="bank-card">')
        d = os.path.join(root, f"ch{n:02d}")
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.endswith(".html"):
                c.page(f"ch{n:02d}/{f}")
        c.zipfile(n)
    if c.exists("index.html"):
        c.page("index.html")
    c.css()
    return c.errs


def main():
    wanted = [int(a) for a in sys.argv[1:]] or None
    errs = run(ROOT, wanted)
    for e in errs:
        print("🔴", e)
    print(f"\n{'❌' if errs else '✅'} 結構:{len(errs)} 個錯誤")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
