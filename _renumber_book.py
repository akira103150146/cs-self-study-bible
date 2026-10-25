#!/usr/bin/env python3
"""依 assets/book.js 的書序,把「數字章號」重新從 0 連續編號(序章 0、第一章 1……)。

用途:在 book.js 插入新章之後跑一次,後面各章的顯示章號自動往後推;附錄(附A…)、橋接章(橋A…)
這類非數字章號不動。內文的章號都是記號({{ch:<id>}} 等),接著跑 python build.py 就全書同步。

用法:
  python _renumber_book.py           改寫 assets/book.js,並列出章號有變的章
  python _renumber_book.py --check   只檢查(章號不連續就回傳 1),不寫檔
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK_JS = os.path.join(ROOT, 'assets', 'book.js')
ENTRY_RE = re.compile(r'(\{\s*id:\s*"([^"]+)",\s*num:\s*")([^"]+)(")')


def main(argv):
    check = '--check' in argv
    text = open(BOOK_JS, encoding='utf-8', newline='').read()
    start, end = text.index('parts:'), text.index('BOOK.flat')
    counter = 0
    changes = []

    def sub(m):
        nonlocal counter
        cid, num = m.group(2), m.group(3)
        if not num.isdigit():
            return m.group(0)
        new = str(counter)
        counter += 1
        if new != num:
            changes.append((cid, num, new))
        return m.group(1) + new + m.group(4)

    body = ENTRY_RE.sub(sub, text[start:end])
    for cid, old, new in changes:
        print(f'{cid}: 第 {old} 章 → 第 {new} 章')
    if check:
        print('章號連續。' if not changes else f'{len(changes)} 章的章號不連續(請執行 python _renumber_book.py)。')
        return 1 if changes else 0
    if changes:
        with open(BOOK_JS, 'w', encoding='utf-8', newline='') as f:
            f.write(text[:start] + body + text[end:])
        print(f'已改寫 assets/book.js({len(changes)} 章);接著請跑 python build.py')
    else:
        print('章號已經連續,不用改。')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
