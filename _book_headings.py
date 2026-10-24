#!/usr/bin/env python3
"""_build_routes.py 與 _check_chapter_refs.py 共用的工具:讀 book.js、比對用的正規化、各章 h2/h3 錨點。

錨點規則與 assets/book.js 的 buildTOC 相同:.content 裡所有 h2/h3 依文件順序編號,
沒有 id 的標題得到 id="sec-N"。這裡先拿掉 HTML 註解與 <pre> 再數(<pre> 裡的 &lt;h2&gt; 不是標題)。
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'chapters', 'src')

ENTRY_RE = re.compile(r'\{\s*id:\s*"([^"]+)",\s*num:\s*"([^"]+)",\s*title:\s*"([^"]*)"')
PART_RE = re.compile(r'part:\s*"([^"]+)"')
HEAD_RE = re.compile(r'<(h[23])\b([^>]*)>(.*?)</\1>|<span class="c-title">(.*?)</span>', re.S)


def load_book():
    """回傳 ({章 id: {num, title, part}}, [章 id 依書序])。"""
    text = open(os.path.join(ROOT, 'assets', 'book.js'), encoding='utf-8').read()
    body = text[text.index('parts:'):text.index('BOOK.flat')]
    chapters, order, part = {}, [], None
    for line in body.splitlines():
        m = PART_RE.search(line)
        if m:
            part = m.group(1)
            continue
        m = ENTRY_RE.search(line)
        if m:
            chapters[m.group(1)] = {'num': m.group(2), 'title': m.group(3), 'part': part}
            order.append(m.group(1))
    return chapters, order


def norm(s):
    """比對用:去標籤、全形轉半形、去空白、轉小寫、去掉開頭的 emoji。"""
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    s = s.translate(str.maketrans('：（）／，、～＋', ':()/,,~+'))
    s = re.sub(r'[\s「」『』“”"]+', '', s).lower()
    return re.sub(r'^[^\w(「『]+', '', s)


def clean_title(raw):
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', raw))).strip()
    return re.sub(r'\s*[(（]呼應第[^)）]*[)）]$', '', t)   # 「(呼應第 41 章)」這種尾巴在導讀裡不需要


class Headings:
    """各章的 h2/h3(和 callout 標題)及對應錨點,錨點規則與 book.js buildTOC 相同。"""

    def __init__(self):
        self.cache = {}

    def get(self, cid):
        if cid not in self.cache:
            path = os.path.join(SRC, cid + '.html')
            text = open(path, encoding='utf-8-sig').read() if os.path.exists(path) else ''
            text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
            text = re.sub(r'<pre\b.*?</pre>', '', text, flags=re.S)
            items, idx, last = [], -1, None
            for m in HEAD_RE.finditer(text):
                if m.group(1):
                    idx += 1
                    idm = re.search(r'\bid="([^"]+)"', m.group(2))
                    anchor = idm.group(1) if idm else f'sec-{idx}'
                    raw = m.group(3)
                    items.append(('h', norm(raw), anchor, clean_title(raw)))
                    last = (anchor, clean_title(raw))
                elif last:
                    raw = m.group(4)
                    items.append(('c', norm(raw), last[0], clean_title(raw)))
            self.cache[cid] = items
        return self.cache[cid]

    def find(self, cid, section):
        """回傳 (anchor, 顯示標題) 或 None。"""
        cands = [section]
        for sep in ('、', '，', '（', '：', '(', ':'):
            if sep in section:
                cands.append(section.split(sep)[0])
        items = self.get(cid)
        bare = lambda x: re.sub(r'[^\w]', '', x)   # 第二輪:連標點都不看
        for key in (lambda x: x, bare):
            for cand in cands:
                c = key(norm(cand))
                if len(c) < 2:
                    continue
                for kind in ('h', 'c'):
                    for k, text, anchor, title in items:
                        if k == kind and key(text).startswith(c):
                            return anchor, title
        return None

    def count(self, cid):
        """該章 h2/h3 的數量(= 可用的 sec-N 個數)。"""
        return sum(1 for item in self.get(cid) if item[0] == 'h')

    def texts_at(self, cid, anchor):
        """錨點所在小節的標題,以及小節內 callout 標題(都已正規化)。"""
        return [text for _, text, a, _ in self.get(cid) if a == anchor]
