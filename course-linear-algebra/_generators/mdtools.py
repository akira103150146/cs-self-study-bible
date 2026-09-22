# -*- coding: utf-8 -*-
"""Markdown 工具:front matter、依標題切段、Markdown → HTML(保護數學式)。

作者在 Markdown 裡照常寫 $x<y$、$$\\begin{bmatrix}a&b\\end{bmatrix}$$。
轉 HTML 前先把數學式抽出來(否則 Markdown 會把 _ \\ * 當成格式吃掉),
轉完再把 < > & 跳脫後放回去——「數學式的 < > & 一律跳脫」由程式保證,作者不用記。
"""
import html
import os
import re

import markdown as _markdown
import yaml

_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

_FENCE_BLOCK = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[ \t]*$", re.M | re.S)
_INLINE_CODE = re.compile(r"(`+)(?!`).+?(?<!`)\1(?!`)")
_FIGURE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+\.svg)\)[ \t]*$", re.M)
_DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.S)
_INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)([^\n$]+?)(?<![\\$])\$(?!\$)")


class ContentError(Exception):
    """內容檔格式錯誤。訊息一律帶檔名,讓作者知道要改哪裡。"""


def split_front_matter(text, path):
    """'---\\nYAML\\n---\\n本文' → (dict, 本文)。沒有 front matter 回傳 ({}, 全文)。"""
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)", text, re.S)
    if not m:
        raise ContentError(f"{path}: front matter 沒有用 --- 收尾")
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise ContentError(f"{path}: front matter 不是合法 YAML:{e}")
    return meta, m.group(2)


def split_sections(body, level):
    """依 '#' * level 的標題切段,fenced code 裡的 # 行不算標題。

    回傳 [(標題, 內文)];第一個標題之前的文字以標題 None 放在最前面(若非空白)。
    """
    mark = "#" * level + " "
    out, title, buf, fence = [], None, [], None
    for line in body.split("\n"):
        f = re.match(r"^(```|~~~)", line)
        if f:
            fence = None if fence == f.group(1) else (fence or f.group(1))
        if fence is None and line.startswith(mark) and not f:
            if title is not None or "".join(buf).strip():
                out.append((title, "\n".join(buf).strip("\n")))
            title, buf = line[len(mark):].strip(), []
        else:
            buf.append(line)
    if title is not None or "".join(buf).strip():
        out.append((title, "\n".join(buf).strip("\n")))
    return out


def fenced_blocks(text):
    """[(info 字串, 程式碼)],依出現順序。"""
    return [(m.group(2).strip(), m.group(3))
            for m in re.finditer(r"^(```|~~~)([^\n]*)\n(.*?)^\1[ \t]*$", text, re.M | re.S)]


def strip_fences(text):
    return _FENCE_BLOCK.sub("", text).strip()


def render(md, figdir=None):
    """Markdown 區塊 → HTML。

    單獨一行的 ![圖說](檔名.svg) 會把 figdir 裡的 SVG 內嵌成 <figure>(SVG 內用 CSS 變數上色,
    所以必須內嵌、不能用 <img>)。
    """
    if not md or not md.strip():
        return ""
    code, math, figs = [], [], []

    def keep_code(m):
        code.append(m.group(0))
        return f"CODEPH{len(code) - 1}Z"

    def keep_math(m, display):
        tex = html.escape(m.group(1), quote=False)
        math.append(f"$${tex}$$" if display else f"${tex}$")
        return f"MATHPH{len(math) - 1}Z"

    def keep_fig(m):
        if figdir is None:
            raise ContentError(f"圖 {m.group(2)} 只能放在觀念檔裡")
        path = os.path.join(figdir, m.group(2))
        if not os.path.exists(path):
            raise ContentError(f"找不到圖檔 figures/{m.group(2)}")
        with open(path, encoding="utf-8") as f:
            svg = re.sub(r"<\?xml[^>]*>\s*", "", f.read()).strip()
        cap = render_inline(m.group(1)) if m.group(1).strip() else ""
        figs.append(f'<figure class="fig">{svg}'
                    + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
        return f"\n\nFIGPH{len(figs) - 1}Z\n\n"

    s = _FENCE_BLOCK.sub(keep_code, md)
    s = _INLINE_CODE.sub(keep_code, s)
    # Python-Markdown 的巢狀清單要縮排 4 格;作者常習慣縮 2–3 格,這裡統一補成 4 格,免得子項目被壓成一行
    s = re.sub(r"(?m)^ {2,3}(?=(?:[-*]|\d+\.)\s)", "    ", s)
    s = _FIGURE.sub(keep_fig, s)
    s = _DISPLAY_MATH.sub(lambda m: keep_math(m, True), s)
    s = _INLINE_MATH.sub(lambda m: keep_math(m, False), s)
    s = re.sub(r"CODEPH(\d+)Z", lambda m: code[int(m.group(1))], s)
    out = _markdown.markdown(s, extensions=_EXTENSIONS, output_format="html")
    out = re.sub(r"<p>FIGPH(\d+)Z</p>", lambda m: figs[int(m.group(1))], out)
    return re.sub(r"MATHPH(\d+)Z", lambda m: math[int(m.group(1))], out)


def render_inline(md):
    """單行/單段 Markdown → 去掉外層 <p> 的 HTML(用在標題、表格格子、清單項)。"""
    h = render(md).strip()
    m = re.fullmatch(r"<p>(.*)</p>", h, re.S)
    return m.group(1) if m and "<p>" not in m.group(1) else h


def list_items(md):
    """最外層的 '- ' 或 '1. ' 清單 → [每一項的 Markdown](續行併入該項)。"""
    items = []
    for line in md.split("\n"):
        m = re.match(r"^(?:[-*]|\d+\.)\s+(.*)", line)
        if m:
            items.append(m.group(1))
        elif items and line.strip():
            items[-1] += "\n" + line.strip()
    return items


def pipe_table(md, path, where):
    """Markdown 表格 → (表頭, [[格子 Markdown]])。"""
    rows = [l.strip() for l in md.split("\n") if l.strip().startswith("|")]
    if len(rows) < 2 or not re.fullmatch(r"\|[\s:|-]+\|", rows[1]):
        raise ContentError(f"{path}: 「{where}」必須是 Markdown 表格(含 |---| 分隔列)")

    def cells(r):
        return [c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))]

    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    for r in body:
        if len(r) != len(head):
            raise ContentError(f"{path}: 「{where}」有一列欄數 {len(r)} ≠ 表頭 {len(head)}:{r}")
    return head, body
