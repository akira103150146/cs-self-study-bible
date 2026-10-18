"""把書的 HTML 章節轉成終端機文字,依小節切開,交給 less 翻閱。

一個小節 = 一個 <h2> 或 <h3> 到下一個標題之前。
SVG 圖換成圖說,練習題的解答(<details class="solution">)不顯示。
"""

import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

from .anim import width

BOOK = Path(__file__).resolve().parents[2] / "chapters" / "16-shell.html"

ESC = "\x1b["
RESET = ESC + "0m"
BOLD, DIM, ITALIC = "1", "2", "3"
HEAD2, HEAD3 = "1;38;2;120;200;255", "1;38;2;150;220;200"
CODE, PROMPT, COMMENT = "38;2;240;190;110", "1;38;2;140;220;140", "2"
CALLOUT, EXERCISE = "38;2;230;200;90", "1;38;2;210;150;255"

SKIP_TAGS = {"svg", "script", "style", "nav", "header", "footer"}
BLOCKS = {"p", "li", "h1", "h2", "h3", "h4", "figcaption", "tr", "summary", "pre", "ul", "ol", "table"}


def book_path():
    return Path(os.environ.get("CSQUEST_BOOK") or BOOK)


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = []          # [(level, title, [blocks])]
        self.skip = 0               # 在 SVG / 解答裡面
        self.skip_stack = []
        self.pre = False
        self.buf = []               # 目前段落的 (文字, 樣式) 片段
        self.styles = []
        self.kind = None            # 目前區塊種類
        self.title = None           # 正在收的標題 (level, [文字])
        self.boxes = []             # 巢狀 div 的種類:callout / exercise / 其他
        self.cells = None

    # ── 輸出 ──
    def emit(self, block):
        if self.sections:
            self.sections[-1][2].append(block)

    def flush(self):
        if not self.buf:
            return
        text = _join(self.buf)
        self.buf = []
        if not text.strip():
            return
        if self.cells is not None:
            self.cells.append(text.strip())
            return
        self.emit((self.kind or "p", text.strip(), self.box()))

    def box(self):
        for b in reversed(self.boxes):
            if b in ("callout", "exercise"):
                return b
        return None

    # ── 標籤 ──
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        if self.skip:
            if tag in ("svg", "details", "div"):
                self.skip_stack.append(tag)
            return
        if tag in SKIP_TAGS or (tag == "details" and "solution" in cls):
            self.flush()
            if tag == "details":
                self.emit(("note", "(解答收在書裡,先自己想想看)", self.box()))
            self.skip = 1
            self.skip_stack = [tag]
            return
        if tag in ("h2", "h3"):
            self.flush()
            self.title = (int(tag[1]), [])
            return
        if tag == "div":
            kind = "callout" if "callout" in cls else "exercise" if "exercise" in cls else (
                "ico" if cls == "ico" else "ctitle" if "ex-head" in cls else "div")
            if self.kind != "ctitle":
                self.flush()
            self.boxes.append(kind)
            if kind in ("ico", "ctitle"):
                self.kind = "ctitle"
            return
        if tag == "span" and "c-title" in cls:
            if self.kind != "ctitle":
                self.flush()
            self.kind = "ctitle"
            return
        if tag in BLOCKS or tag == "br":
            self.flush()
            if tag == "pre":
                self.pre = True
                self.kind = "pre"
            elif tag == "li":
                self.kind = "li"
            elif tag == "figcaption":
                self.kind = "fig"
            elif tag == "tr":
                self.cells = []
            elif tag != "br":
                self.kind = "p"
            return
        if tag in ("td", "th"):
            self.flush()
            return
        if tag in ("strong", "b"):
            self.styles.append(BOLD)
        elif tag == "em":
            self.styles.append(ITALIC)
        elif tag == "code" and not self.pre:
            self.styles.append(CODE)

    def handle_endtag(self, tag):
        if self.skip:
            if tag in ("svg", "details", "div") and self.skip_stack and self.skip_stack[-1] == tag:
                self.skip_stack.pop()
                if not self.skip_stack:
                    self.skip = 0
            return
        if self.title and tag in ("h2", "h3"):
            level, parts = self.title
            self.title = None
            self.sections.append((level, _plain("".join(t for t, _ in parts)), []))
            return
        if tag == "div":
            if self.boxes:
                kind = self.boxes.pop()
                if kind == "ico":
                    self.buf.append((" ", ""))
                    return          # 圖示跟標題放在同一行
            self.flush()
            self.kind = None
            return
        if tag == "span" and self.kind == "ctitle":
            self.flush()
            self.kind = None
            return
        if tag in BLOCKS:
            if tag == "pre":
                self.emit(("pre", "".join(t for t, _ in self.buf), self.box()))
                self.buf = []
                self.pre = False
            elif tag == "tr":
                self.flush()
                if self.cells:
                    self.emit(("row", self.cells, self.box()))
                self.cells = None
            else:
                self.flush()
            self.kind = None
            return
        if tag in ("td", "th"):
            self.flush()
            return
        if tag in ("strong", "b", "em", "code") and self.styles and not (tag == "code" and self.pre):
            self.styles.pop()

    def handle_data(self, data):
        if self.skip:
            return
        if self.title:
            self.title[1].append((data, ""))
            return
        if not self.pre:
            data = re.sub(r"\s*\n\s*", "\x00", data)
            data = re.sub(r"[ \t]+", " ", data)
        self.buf.append((data, ";".join(self.styles)))


def _plain(s):
    return re.sub(r"\s+", " ", s).strip()


def _join(parts):
    """接起片段;原始碼裡的換行,在中文字之間丟掉、在英文之間變空白。"""
    out = []
    for text, st in parts:
        out.append((f"{ESC}{st}m" if st else "") + text + (RESET if st else ""))
    s = "".join(out)

    def fix(m):
        before, after = m.group(1), m.group(2)
        wide = all(width(c) == 2 for c in (before + after) if c)
        return before + ("" if wide else " ") + after
    s = re.sub(r"(.?)\x00+(.?)", fix, s)
    return s.replace("\x00", "")


def parse(path=None):
    p = _Parser()
    p.feed(Path(path or book_path()).read_text(encoding="utf-8"))
    p.flush()
    return p.sections


# ── 排版 ─────────────────────────────────────────────────

NO_LINE_START = set(",.;:!?)」』】,。、;:!?)…—")
TOKEN = re.compile(r"\x1b\[[0-9;]*m|[A-Za-z0-9_\-./~$*?'\"=:,()<>|&+%@#!\[\]{}]+| |.", re.S)


def wrap(text, cols):
    """依顯示寬度換行;英文單字不拆開,樣式跨行時在每行重新開啟。"""
    lines, cur, w, active = [], "", 0, []
    for tok in TOKEN.findall(text):
        if tok.startswith("\x1b["):
            cur += tok
            active = [] if tok == RESET else active + [tok]
            continue
        tw = width(tok)
        if w + tw > cols and w > 0 and not (tok in NO_LINE_START and w + tw <= cols + 4):
            lines.append(cur + (RESET if active else ""))
            cur, w = "".join(active), 0
            if tok == " ":
                continue
        cur += tok
        w += tw
    lines.append(cur)
    return lines


def c(code, text, color):
    return f"{ESC}{code}m{text}{RESET}" if color else text


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def render(sections, cols=80, color=True):
    out = []
    for level, title, blocks in sections:
        out.append("")
        if level == 2:
            out.append(c(HEAD2, "■ " + title, color))
            out.append(c(DIM, "━" * min(cols, width(title) + 2), color))
        else:
            out.append(c(HEAD3, "▸ " + title, color))
        out.append("")
        prev = None
        for kind, body, box in blocks:
            bar = {"callout": c(CALLOUT, "┃ ", color), "exercise": c(EXERCISE, "┃ ", color)}.get(box, "")
            inner = cols - width(strip_ansi(bar))
            lines = []
            if kind == "pre":
                for ln in body.rstrip("\n").split("\n"):
                    if ln.startswith("$ "):
                        cmd, _, cmt = ln.partition("#")
                        ln = c(PROMPT, cmd, color) + (c(COMMENT, "#" + cmt, color) if cmt else "")
                    elif ln.lstrip().startswith("#"):
                        ln = c(COMMENT, ln, color)
                    lines.append(c(DIM, "│ ", color) + ln)
                lines = [""] + lines
            elif kind == "row":
                lines = wrap("  │  ".join(body), inner)
            elif kind == "li":
                w = wrap(body, inner - 2)
                lines = ["• " + w[0]] + ["  " + l for l in w[1:]]
            elif kind == "fig":
                lines = [""] + wrap(c(DIM, "〔圖〕" + strip_ansi(body), color), inner)
            elif kind == "ctitle":
                lines = wrap(c(EXERCISE if box == "exercise" else CALLOUT, strip_ansi(body), color), inner)
                if prev is not None:
                    out.append("")
            elif kind == "note":
                lines = [c(DIM, body, color)]
            else:
                lines = wrap(body, inner)
                if prev not in (None, "li", "ctitle", "row") or (prev == "li" and kind != "li"):
                    lines = [""] + lines
            out += [bar + l for l in lines]
            prev = kind
    text = "\n".join(out) + "\n"
    return text if color else strip_ansi(text)


def select(sections, titles):
    """依標題開頭挑出小節,保持書中順序。"""
    return [s for s in sections if any(s[1].startswith(t) for t in titles)]


def show(titles, heading):
    path = book_path()
    if not path.exists():
        print(f"找不到書本檔案 {path}(可以用 CSQUEST_BOOK 指定)。")
        return 1
    sections = parse(path)
    picked = select(sections, titles) if titles else sections
    tty = sys.stdout.isatty()
    cols = min(shutil.get_terminal_size((80, 24)).columns - 2, 86)
    text = (c("1;38;2;255;220;120", f"📖 {heading}", tty) + "\n"
            + render(picked, cols, color=tty)
            + "\n" + c(DIM, "── 讀完按 q 回到地下城 ──", tty) + "\n")
    if not tty or not shutil.which("less"):
        sys.stdout.write(text)
        return 0
    prompt = " 空白鍵 下一頁 · b 上一頁 · /關鍵字 搜尋 · q 回到地下城 "
    subprocess.run(["less", "-R", "-Ps" + prompt],
                   input=text, text=True, env=dict(os.environ, LESSCHARSET="utf-8"))
    return 0
