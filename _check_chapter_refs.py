#!/usr/bin/env python3
"""章號與章際連結檢查器(只讀,不改檔)。

以 assets/book.js 的 BOOK.parts 為唯一真相(id → 顯示章號 num、所屬部),檢查 chapters/src/*.html:
  1. 章際連結 <a href="NN-slug.html">…第 N 章…</a>:連結文字裡的章號必須等於目標章在 book.js 的 num。
  2. 章際連結的目標檔必須存在(chapters/src/NN-slug.html),#錨點不檢查。
  3. 章首 byline 的 <span class="tag">第 N 章</span> 必須等於本章 num(附錄 / 序章 / 非數字章號略過)。
  4. 章首 .eyebrow「第 X 部 · …」必須等於本章在 book.js 所屬部的部名前綴。
  5. 「第 N 章〈標題〉/「標題」」這種寫法:若標題和第 N 章的書名完全對不上、卻和另一章的書名吻合,列為疑似錯號。
  6. 「第 N 章」的 N 是「檔名號」而不是顯示號(第一次重新編號留下的錯):N ≥ 74、檔名 N-* 和顯示第 N 章
     是不同章,而且前後文和檔名 N 那章的書名吻合、和顯示第 N 章的書名對不上。
  7. 連到 #sec-N 的小節錨點(book.js 自動目錄給 h2/h3 的 id):N 必須小於目標章的 h2/h3 數量;
     連結文字裡有「§小節名」時,小節名必須是第 N 個標題(或該小節內 callout 標題)的開頭。
     標題計數與 _build_routes.py 共用 _book_headings.Headings(同樣先拿掉註解與 <pre>)。
  8. 殘留的「(撰寫中)」「(即將撰寫)」標記(提醒用,不一定是錯)。

用法:python _check_chapter_refs.py          列出所有問題,有問題時 exit 1
      python _check_chapter_refs.py --quiet  只印摘要
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)   # python -I 也找得到共用模組
from _book_headings import SRC, Headings, load_book  # noqa: E402
from _book_headings import norm as head_norm  # noqa: E402

LINK_RE = re.compile(r'<a\s[^>]*href="([^"#:]+?)\.html(?:#([^"]*))?"[^>]*>(.*?)</a>', re.S)
CHNUM_RE = re.compile(r'第\s*(\d+)\s*章')
TAG_RE = re.compile(r'<span class="tag">\s*第\s*(\d+)\s*章\s*</span>')
EYEBROW_RE = re.compile(r'<div class="eyebrow">\s*([^<·]+?)\s*·')
TITLED_RE = re.compile(r'第\s*(\d+)\s*章\s*[〈「《]([^〉」》]{2,30})[〉」》]')
EXTERNAL_RE = re.compile(r'SICP|Nand2Tetris|nand2tetris|AP325|APCS|TOI|教材|原書|課本|的$')
TODO_RE = re.compile(r'[（(](?:撰寫中|即將撰寫)[）)]')


def norm(s):
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    s = s.translate(str.maketrans('：（）／，、', ':()/,,'))
    return re.sub(r'\s+', '', s)


def bigrams(s):
    s = re.sub(r'[^0-9A-Za-z\u4e00-\u9fff]', '', norm(s)).lower()
    return {s[i:i + 2] for i in range(len(s) - 1)} or {s}


def similarity(label, title):
    """label 的雙字組有多少比例出現在 title 裡(0–1)。"""
    a, b = bigrams(label), bigrams(title)
    return len(a & b) / len(a)


def coverage(title, ctx):
    """title 的雙字組有多少比例出現在 ctx 裡。"""
    a = bigrams(title)
    return len(a & bigrams(ctx)) / len(a)


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def main(argv):
    quiet = '--quiet' in argv
    book, _ = load_book()
    heads = Headings()
    by_num = {c['num']: cid for cid, c in book.items()}
    by_file = {cid.split('-')[0]: cid for cid in book if cid[0].isdigit()}
    problems = []

    for path in sorted(glob.glob(os.path.join(SRC, '*.html'))):
        name = os.path.basename(path)[:-5]
        text = open(path, encoding='utf-8-sig').read()
        me = book.get(name)

        for m in LINK_RE.finditer(text):
            target, frag, label = m.group(1), m.group(2), m.group(3)
            if '/' in target:      # ../index.html、../course-*/… 不是章際連結
                continue
            if not os.path.exists(os.path.join(SRC, target + '.html')):
                problems.append((name, line_of(text, m.start()), 'broken-link', f'{target}.html 不存在'))
                continue
            if frag and frag.startswith('sec-') and frag[4:].isdigit():
                total = heads.count(target)
                plain_label = html.unescape(re.sub(r'<[^>]+>', '', label))
                if int(frag[4:]) >= total:
                    problems.append((name, line_of(text, m.start()), 'anchor',
                                     f'{target}.html#{frag} 不存在(該章只有 {total} 個 h2/h3)'))
                elif '§' in plain_label:
                    want_sec = head_norm(plain_label.split('§', 1)[1])
                    here = heads.texts_at(target, frag)
                    if want_sec and not any(t.startswith(want_sec) or want_sec.startswith(t) for t in here):
                        got = heads.get(target)[[i for i, it in enumerate(heads.get(target)) if it[2] == frag][0]][3]
                        problems.append((name, line_of(text, m.start()), 'anchor',
                                         f'{target}.html#{frag} 是〈{got}〉,連結文字卻是「§{plain_label.split("§", 1)[1]}」'))
            if target not in book:
                continue
            want = book[target]['num']
            for n in CHNUM_RE.findall(re.sub(r'<[^>]+>', '', label))[:1]:   # 只看第一個,後面可能是「呼應第 N 章」
                if n != want:
                    problems.append((name, line_of(text, m.start()), 'link-num',
                                     f'連到 {target}(顯示第 {want} 章),文字卻寫「第 {n} 章」'))

        if me:
            m = TAG_RE.search(text)
            if m and me['num'].isdigit() and m.group(1) != me['num']:
                problems.append((name, line_of(text, m.start()), 'self-tag',
                                 f'章首寫第 {m.group(1)} 章,book.js 是 {me["num"]}'))
            m = EYEBROW_RE.search(text)
            part_head = (me['part'] or '').split('·')[0].strip()
            if m and part_head and m.group(1).strip() != part_head:
                problems.append((name, line_of(text, m.start()), 'eyebrow',
                                 f'eyebrow 寫「{m.group(1).strip()}」,book.js 是「{part_head}」'))

        for m in TITLED_RE.finditer(text):
            n, label = m.group(1), norm(m.group(2))
            cid = by_num.get(n)
            if not cid or EXTERNAL_RE.search(text[max(0, m.start() - 80):m.start()]):
                continue
            if similarity(label, book[cid]['title']) >= 0.2:
                continue
            others = sorted((c for c in book if c != cid and similarity(label, book[c]['title']) >= 0.6),
                            key=lambda c: -similarity(label, book[c]['title']))
            if others:
                hint = ', '.join(f'{c}(第 {book[c]["num"]} 章)' for c in others[:3])
                problems.append((name, line_of(text, m.start()), 'titled-num',
                                 f'「第 {n} 章〈{m.group(2)}〉」:第 {n} 章是〈{book[cid]["title"]}〉,疑似指 {hint}'))

        plain = re.sub(r'<[^>]+>', lambda t: '\n' * t.group(0).count('\n'), text)
        for m in CHNUM_RE.finditer(plain):
            n = m.group(1)
            fid, did = by_file.get(n), by_num.get(n)
            if int(n) < 74 or not fid or fid == did:
                continue
            ctx = plain[max(0, m.start() - 30):m.end() + 30]
            sf = coverage(book[fid]['title'], ctx)
            sd = coverage(book[did]['title'], ctx) if did else 0
            if sf >= 0.25 and sd < 0.15:
                snippet = plain[m.start():m.end() + 24].replace('\n', ' ').strip()
                problems.append((name, line_of(plain, m.start()), 'file-number',
                                 f'「{snippet}」像是指 {fid}(顯示第 {book[fid]["num"]} 章),不是顯示第 {n} 章'))

        for m in TODO_RE.finditer(text):
            problems.append((name, line_of(text, m.start()), 'todo-marker', f'殘留標記「{m.group(0)}」'))

    kinds = {}
    for p in problems:
        kinds[p[2]] = kinds.get(p[2], 0) + 1
    if not quiet:
        for name, ln, kind, msg in problems:
            print(f'{name}.html:{ln}: [{kind}] {msg}')
    summary = ', '.join(f'{k} {v}' for k, v in sorted(kinds.items())) or '無'
    print(f'檢查 {len(glob.glob(os.path.join(SRC, "*.html")))} 個片段、{len(book)} 個 book.js 條目;問題:{summary}')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
