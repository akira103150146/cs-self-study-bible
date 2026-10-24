#!/usr/bin/env python3
"""一次性轉換:把 chapters/src/*.html 裡寫死的章號、部名改成 build 時代入的記號(見 _chapter_tokens.py)。

  章首 .eyebrow「第六部 · 演算法與資料結構」        → {{part:<本章 id>}}
  章首 .tag「第 30 章」                           → {{ch:<本章 id>}}
  <a href="30-graph-algorithms.html">第 30 章</a>  → 依 href 決定 id(連結文字的章號必須等於目標章的顯示章號)
  其他「第 30 章」「第 34–36 章」「第 52、53 章」   → 依 book.js 的顯示章號 → id
  內文「第六部」                                   → {{partnum:<該部第一章 id>}}

不轉:<pre>/<code>/<script>/<style>/註解裡的文字;_chapter_refs_allowlist.txt 放行的外部書目章號
(AP325、SICP、nand2tetris…)與附錄題庫;對不上任何一章的號碼;連結文字和 href 不一致的(列出來給人看)。
route-<track>.html 由 _build_routes.py 產生,不在這裡轉(改產生器);手寫的 route-security-redlines.html 照轉。

用法:
  python _tokenize_chapter_refs.py            轉換並寫回 src
  python _tokenize_chapter_refs.py --dry-run  只印統計
  python _tokenize_chapter_refs.py --review   列出疑似外部書目、需要人看的引用(不寫檔)
轉完務必:python build.py,並確認產出的 chapters/*.html 與轉換前逐位元組相同。
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from _book_headings import SRC, load_book  # noqa: E402
from _chapter_tokens import (NUM_IN_REF, allowed, bare_refs, book_context, covers,  # noqa: E402
                             load_allowlist, part_head, resolve, window)

LINK_RE = re.compile(r'<a\s[^>]*href="([^"#:/]+?)\.html(?:#[^"]*)?"[^>]*>(.*?)</a>', re.S)
EYEBROW_RE = re.compile(r'(<div class="eyebrow">)([^<]*)(</div>)')
TAG_RE = re.compile(r'(<span class="tag">)\s*第 (\d+) 章\s*(</span>)')
# 需要人看的訊號:外部書名、教材字眼、英文書名號
SUSPECT_RE = re.compile(r'AP325|APCS|TOI|SICP|[Nn]and2[Tt]etris|OSTEP|CLRS|CS:?APP|K&R|Rust Programming|'
                        r'[Bb]ook|Chapter|教材|講義|課本|原書|原著|該書|這本書|那本書|書中|教科書|論文|《|》|吳邦一')
# 白名單放行範圍裡、但其實是本書章號,要轉的(人工判讀;(章 id, 前後文片段))
FORCE = [
    ('74-bank-ap325', r'搭配:第 59–64 章'),
    ('74-bank-ap325', r'↔ 第[\d、 ]+章'),
    ('74-bank-ap325', r'則對應第 32、62 章\(DP\)與第 30、63 章'),
]
FORCE = [(f, re.compile(rx)) for f, rx in FORCE]
GENERATED = '本檔由 _build_routes.py 從職業技能樹 tree.yaml 產生'
RISKY_SMALL = re.compile(r'^(19|2[0-4]|59|6[0-4]|8[0-9]|90)-')   # 會引用外部書小章號的章


def numbered(book):
    return {c['num']: cid for cid, c in book.items() if c['num'].isdigit()}


def part_first(book, order):
    out = {}
    for cid in order:
        out.setdefault(part_head(book[cid]['part']), cid)
    return out


def link_targets(text, book):
    """[(label 起, label 訖, 目標 id)]:只收書內章節的連結。"""
    out = []
    for m in LINK_RE.finditer(text):
        if m.group(1) in book:
            out.append((m.start(2), m.end(2), m.group(1)))
    return out


def convert_file(name, text, book, by_num, by_part, rules, stats, review):
    links = link_targets(text, book)
    edits = []          # (起, 訖, 新文字)

    def note(kind, msg):
        stats.setdefault(kind, []).append(f'{name}: {msg}')

    me = book.get(name)
    if me:
        m = EYEBROW_RE.search(text)
        if m and m.group(2).strip() == me['part']:
            edits.append((m.start(2), m.end(2), m.group(2).replace(me['part'], '{{part:%s}}' % name)))
            stats['eyebrow'] = stats.get('eyebrow', 0) + 1
        m = TAG_RE.search(text)
        if m and m.group(2) == me['num']:
            edits.append((m.start(), m.end(), text[m.start():m.end()].replace(f'第 {me["num"]} 章', '{{ch:%s}}' % name)))
            stats['self-tag'] = stats.get('self-tag', 0) + 1
    taken = [(s, e) for s, e, _ in edits]

    for s, e, kind, got in bare_refs(text):
        if any(a <= s < b for a, b in taken):
            continue
        win, ws, we = window(text, s, e)
        mark = win[max(0, ws - 30):ws] + '⟦' + win[ws:we] + '⟧' + win[we:]
        target = next((t for a, b, t in links if a <= s < b), None) if kind == 'ch' else None
        hit = allowed(rules, name, text, s, e)
        if hit and not target and not (kind == 'ch' and book_context(text, s, e, book, by_num)) \
                and not any(f == name and covers(rx, win, ws, we) for f, rx in FORCE):
            stats['allowlisted'] = stats.get('allowlisted', 0) + 1
            if review:
                note('kept', f'「{mark}」')
            continue
        if kind == 'part':
            label = got
            cid = by_part.get(label)
            if not cid:
                note('skipped', f'「{win}」:{label} 不是 book.js 的部')
                continue
            if review and SUSPECT_RE.search(win):
                note('review', f'[部] 「{mark}」')
            edits.append((s, e, '{{partnum:%s}}' % cid))
            stats['part'] = stats.get('part', 0) + 1
            continue
        nums = [(m.start() + s, m.end() + s, m.group(0)) for m in NUM_IN_REF.finditer(got)]
        ids = []
        for i, (ns, ne, n) in enumerate(nums):
            if i == 0 and target:
                if book[target]['num'] != n:
                    ids = None
                    note('skipped', f'「{win}」:連到 {target}(第 {book[target]["num"]} 章)卻寫第 {n} 章')
                    break
                ids.append(target)
            else:
                cid = by_num.get(n)
                if not cid:
                    ids = None
                    note('skipped', f'「{win}」:第 {n} 章對不上本書任何一章')
                    break
                ids.append(cid)
        if ids is None:
            continue
        if review and not target and (SUSPECT_RE.search(win) or
                                       (RISKY_SMALL.match(name) and int(nums[0][2]) <= 12)):
            note('review', f'「{mark}」 → {",".join(ids)}')
        if re.fullmatch(r'第 \d+ 章', got):
            new = '{{ch:%s}}' % ids[0]
        else:
            parts, last = [], s
            for (ns, ne, n), cid in zip(nums, ids):
                parts.append(text[last:ns])
                parts.append('{{num:%s}}' % cid)
                last = ne
            parts.append(text[last:e])
            new = ''.join(parts)
        edits.append((s, e, new))
        key = 'linked' if target else 'bare'
        stats[key] = stats.get(key, 0) + 1

    edits.sort()
    out, last = [], 0
    for s, e, new in edits:
        assert s >= last, (name, s, last)
        out.append(text[last:s])
        out.append(new)
        last = e
    out.append(text[last:])
    new_text = ''.join(out)
    if resolve(new_text, book, name) != text:
        raise SystemExit(f'{name}: 轉換後代入的結果和原文不同,停止')
    return new_text


def main(argv):
    dry = '--dry-run' in argv
    review = '--review' in argv
    book, order = load_book()
    by_num = numbered(book)
    by_part = part_first(book, order)
    rules = load_allowlist()
    stats = {}
    changed = 0
    for path in sorted(glob.glob(os.path.join(SRC, '*.html'))):
        name = os.path.basename(path)[:-5]
        with open(path, encoding='utf-8', newline='') as f:
            text = f.read()
        if GENERATED in text:      # route-<track>.html:改 _build_routes.py 再重跑
            continue
        new = convert_file(name, text, book, by_num, by_part, rules, stats, review)
        if new != text:
            changed += 1
            if not (dry or review):
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(new)
    for kind in ('kept', 'review', 'skipped'):
        for line in stats.get(kind, []):
            print(f'[{kind}] {line}')
    counts = {k: (len(v) if isinstance(v, list) else v) for k, v in stats.items()}
    print('統計:', ', '.join(f'{k} {v}' for k, v in sorted(counts.items())), f'| 改動 {changed} 個檔案',
          '(未寫檔)' if dry or review else '')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
