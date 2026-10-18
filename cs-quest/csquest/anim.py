"""終端機動畫與排版:只用 ANSI escape code 與標準函式庫。

設 CSQUEST_NOANIM=1(或輸出不是終端機)時,所有動畫退化成直接印出,
測試與管線裡用起來不會卡住。
"""

import os
import random
import shutil
import sys
import time
import unicodedata

ESC = "\x1b["
RESET = ESC + "0m"
HIDE_CURSOR = ESC + "?25l"
SHOW_CURSOR = ESC + "?25h"


def animated():
    return sys.stdout.isatty() and not os.environ.get("CSQUEST_NOANIM")


def rgb(r, g, b):
    return f"{ESC}38;2;{r};{g};{b}m"


def style(text, *codes):
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return "".join(f"{ESC}{c}m" for c in codes) + text + RESET


def bold(t):
    return style(t, "1")


def dim(t):
    return style(t, "2")


def green(t):
    return style(t, "1", "32")


def red(t):
    return style(t, "1", "31")


def yellow(t):
    return style(t, "1", "33")


def cyan(t):
    return style(t, "1", "36")


def magenta(t):
    return style(t, "1", "35")


def width(text):
    """顯示寬度:中文等全形字佔兩格。"""
    w = 0
    in_esc = False
    for ch in text:
        if ch == "\x1b":
            in_esc = True
        elif in_esc:
            if ch == "m":
                in_esc = False
        elif unicodedata.east_asian_width(ch) in ("W", "F"):
            w += 2
        elif not unicodedata.combining(ch):
            w += 1
    return w


def pad(text, w):
    return text + " " * max(0, w - width(text))


def sleep(sec):
    if animated():
        time.sleep(sec)


def out(text="", end="\n"):
    sys.stdout.write(text + end)
    sys.stdout.flush()


def typewriter(text, delay=0.018):
    """一個字一個字打出來;按 Ctrl-C 直接整段印完。"""
    if not animated():
        out(text)
        return
    try:
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            if ch not in " \n":
                time.sleep(delay * (6 if ch in "。!?…" else 1))
        out()
    except KeyboardInterrupt:
        out()


def box(lines, title="", color=cyan, min_width=0):
    """畫一個框線面板,中英混排也對得齊。"""
    inner = max([min_width, width(title) + 2] + [width(l) + 2 for l in lines])
    term = shutil.get_terminal_size((80, 24)).columns
    inner = min(inner, max(20, term - 4))
    top = "─" * inner
    if title:
        t = f" {title} "
        top = "─" + t + "─" * max(0, inner - width(t) - 1)
    rows = [color("┌" + top + "┐")]
    for l in lines:
        rows.append(color("│") + " " + pad(l, inner - 2) + " " + color("│"))
    rows.append(color("└" + "─" * inner + "┘"))
    out("\n".join(rows))


TITLE_ART = r"""
  ____ _____       ___                  _
 / ___/ ___/      / _ \ _   _  ___  ___| |_
| |   \___ \ ____| | | | | | |/ _ \/ __| __|
| |___ ___) |____| |_| | |_| |  __/\__ \ |_
 \____|____/      \__\_\\__,_|\___||___/\__|
""".strip("\n").splitlines()


def gradient(i, n):
    t = i / max(1, n - 1)
    return rgb(int(80 + 175 * t), int(220 - 120 * t), int(255 - 60 * t))


def title_screen():
    """開場:字元從雜訊裡「解碼」出標題,再打出副標。"""
    if not animated():
        out("\n".join(TITLE_ART))
        out("終端機與 Shell 的地下城 · 第 16 章")
        return
    noise = "01#@%&*+=<>/\\|$"
    rows = TITLE_ART
    w = max(len(r) for r in rows)
    rows = [r.ljust(w) for r in rows]
    cells = [(y, x) for y, r in enumerate(rows) for x, c in enumerate(r) if c != " "]
    rng = random.Random()
    reveal_at = {cell: rng.randint(3, 26) for cell in cells}
    out(HIDE_CURSOR, end="")
    try:
        out("\n" * len(rows), end="")
        for frame in range(30):
            sys.stdout.write(f"{ESC}{len(rows)}A")
            for y, r in enumerate(rows):
                line = []
                for x, c in enumerate(r):
                    if c == " ":
                        line.append(" ")
                    elif frame >= reveal_at[(y, x)]:
                        line.append(gradient(x, w) + c)
                    else:
                        line.append(rgb(60, 90, 60) + rng.choice(noise))
                sys.stdout.write("\r" + "".join(line) + RESET + "\n")
            sys.stdout.flush()
            time.sleep(0.045)
    finally:
        out(SHOW_CURSOR, end="")
    typewriter(dim("       終端機與 Shell 的地下城 · 第 16 章"), 0.03)


def spinner(label, seconds=0.9):
    if not animated():
        return
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end = time.time() + seconds
    i = 0
    out(HIDE_CURSOR, end="")
    try:
        while time.time() < end:
            sys.stdout.write(f"\r{cyan(frames[i % len(frames)])} {label}")
            sys.stdout.flush()
            time.sleep(0.07)
            i += 1
        sys.stdout.write("\r" + " " * (width(label) + 3) + "\r")
    finally:
        out(SHOW_CURSOR, end="")


def celebrate(text):
    """過關:一排星星從左邊炸開,然後印出訊息。"""
    if not animated():
        out(green(text))
        return
    sparks = "✦✧★☆·*+"
    rng = random.Random()
    cols = min(48, shutil.get_terminal_size((80, 24)).columns - 2)
    out(HIDE_CURSOR, end="")
    try:
        for f in range(14):
            row = []
            for x in range(cols):
                if abs(x - f * 4) < 6 and rng.random() < 0.6:
                    row.append(rgb(255, rng.randint(160, 255), rng.randint(40, 200)) + rng.choice(sparks))
                else:
                    row.append(" ")
            sys.stdout.write("\r" + "".join(row) + RESET)
            sys.stdout.flush()
            time.sleep(0.04)
        sys.stdout.write("\r" + " " * cols + "\r")
    finally:
        out(SHOW_CURSOR, end="")
    typewriter(green(text), 0.025)


def shake(text):
    """答錯:訊息左右抖兩下。"""
    if not animated():
        out(red(text))
        return
    out(HIDE_CURSOR, end="")
    try:
        for dx in (2, 0, 2, 0, 1, 0):
            sys.stdout.write("\r" + " " * dx + red(text) + "   ")
            sys.stdout.flush()
            time.sleep(0.05)
        out()
    finally:
        out(SHOW_CURSOR, end="")


def progress_bar(done, total, w=30):
    fill = round(w * done / total) if total else 0
    return green("█" * fill) + dim("░" * (w - fill)) + f" {done}/{total}"
