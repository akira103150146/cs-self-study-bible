#!/usr/bin/env python3
"""章號記號:內文不寫死章號與部名,改寫記號,由 build.py 依 assets/book.js 代入。

記號(<id> 一律是章的檔名 id,例如 30-graph-algorithms;寫在 src 片段的內文或 meta 的 title/description 裡):
  {{ch:<id>}}       → 「第 30 章」(只能用在有數字章號的章)
  {{num:<id>}}      → 「30」(範圍與並列:「第 {{num:a}}–{{num:b}} 章」「第 {{num:a}}、{{num:b}} 章」)
  {{part:<id>}}     → 該章所屬部的完整名稱,例如「第六部 · 演算法與資料結構」(章首 .eyebrow 用)
  {{partnum:<id>}}  → 該章所屬部的部號,例如「第六部」(內文提到某一部時,用那一部任一章的 id)

章搬到別的位置或別的部,只要改 book.js,重跑 python build.py,所有章號與部名就會跟著變。
記號寫錯(未知的種類、不存在的 id、對沒有數字章號的章用 ch/num)時 build 直接失敗。

本模組也提供 _check_chapter_refs.py 與 _tokenize_chapter_refs.py 共用的「裸章號」搜尋:
<pre>、<code>、<script>、<style> 與 HTML 註解(檔首的 <!--meta--> 除外)裡的文字不算;外部書目(AP325、SICP…)的章號
由 _chapter_refs_allowlist.txt 放行。
"""
import fnmatch
import os
import re

from _book_headings import ROOT, load_book

TOKEN_RE = re.compile(r'\{\{([a-z]+):([^{}\s]+)\}\}')
KINDS = ('ch', 'num', 'part', 'partnum')

# 「第 N 章」以及範圍、並列:第 34–36 章、第 52、53 章、第 7 到第 11 章
REF_RE = re.compile(r'第(\s*)(\d+)((?:\s*(?:[–\-~、,，/／]|至|到|和|與|及|或)\s*(?:第\s*)?\d+)*)\s*章')
NUM_IN_REF = re.compile(r'\d+')
# 「第六部」(「第二部分」「第三部曲」不是本書的部)
PART_REF_RE = re.compile(r'第([一二三四五六七八九十]+)部(?![分曲])')
EXEMPT_RE = re.compile(r'<!--(?!meta\b).*?-->|<(pre|code|script|style)\b.*?</\1>', re.S)
ALLOWLIST = os.path.join(ROOT, '_chapter_refs_allowlist.txt')


class TokenError(ValueError):
    pass


def part_head(part):
    return (part or '').split(' · ')[0].strip()


def resolve(text, book, where=''):
    """把 text 裡的記號換成顯示文字。book 是 load_book() 的第一個回傳值。"""
    def sub(m):
        kind, cid = m.group(1), m.group(2)
        if kind not in KINDS:
            raise TokenError(f'{where}: 未知的記號種類 {m.group(0)}(可用:{", ".join(KINDS)})')
        c = book.get(cid)
        if c is None:
            raise TokenError(f'{where}: 記號 {m.group(0)} 指向 book.js 裡沒有的章 id')
        if kind in ('ch', 'num'):
            if not c['num'].isdigit():
                raise TokenError(f'{where}: 記號 {m.group(0)} 指向的章號是「{c["num"]}」,不是數字,不能用 {kind}')
            return f'第 {c["num"]} 章' if kind == 'ch' else c['num']
        if kind == 'part':
            return c['part']
        return part_head(c['part'])
    return TOKEN_RE.sub(sub, text)


def bad_tokens(text, book):
    """回傳 [(位置, 記號, 原因)]:未知種類或未知 id(給檢查器用,不丟例外)。"""
    out = []
    for m in TOKEN_RE.finditer(text):
        try:
            resolve(m.group(0), book)
        except TokenError as e:
            out.append((m.start(), m.group(0), str(e).split(': ', 1)[-1]))
    return out


def exempt_spans(text):
    return [(m.start(), m.end()) for m in EXEMPT_RE.finditer(text)]


def in_spans(pos, spans):
    for s, e in spans:
        if s <= pos < e:
            return True
        if s > pos:
            return False
    return False


def _plain(s):
    s = re.sub(r'<[^>]*>', '', s)
    return re.sub(r'\s+', ' ', s)


def window(text, start, end):
    """(純文字視窗, 該引用在視窗裡的起訖):前 60 字、後 20 字,已去標籤、空白摺成一格。"""
    pre = _plain(text[max(0, start - 600):start])[-60:]
    post = _plain(text[end:end + 300])[:20]
    mid = text[start:end]
    return pre + mid + post, len(pre), len(pre) + len(mid)


def load_allowlist(path=ALLOWLIST):
    """[(檔名 glob, 編好的正規式 或 None=整檔放行)]"""
    rules = []
    if not os.path.exists(path):
        return rules
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        glob_, _, rx = line.strip().partition(' ')
        rx = rx.strip()
        rules.append((glob_, None if rx == '*' else re.compile(rx), line))
    return rules


def covers(rx, win, s, e):
    """rx 在 win 裡有沒有一段比對(從 s 以前的任一位置開始)蓋住 [s, e)。逐一起點試,比對可以互相重疊。"""
    for pos in range(s + 1):
        m = rx.match(win, pos)
        if m and m.end() >= e:
            return True
    return False


def allowed(rules, name, text, start, end):
    """這個裸引用是否被白名單放行;回傳命中的那一行或 None。"""
    win, s, e = None, 0, 0
    for glob_, rx, line in rules:
        if not fnmatch.fnmatch(name, glob_):
            continue
        if rx is None:
            return line
        if win is None:
            win, s, e = window(text, start, end)
        if covers(rx, win, s, e):
            return line
    return None


CLAUSE_END = re.compile(r'[。！？；]|</?(?:p|li|td|th|tr|h[1-6]|div|br|summary|figcaption)\b[^>]*>')
THIS_BOOK = re.compile(r'(?<![這那該整])本書')
OTHER_SOURCE = re.compile(r'APCS|AP325|TOI|SICP|[Nn]and2[Tt]etris|CLRS|講義|教材|題庫|題本|原書|原著|上冊|下冊')
TITLED = re.compile(r'\s*[〈「《]([^〉」》]{2,40})[〉」》]')


def _grams(s):
    s = re.sub(r'[^0-9A-Za-z一-鿿]', '', re.sub(r'<[^>]+>', '', s)).lower()
    return {s[i:i + 2] for i in range(len(s) - 1)} or {s}


def book_context(text, start, end, book, by_num):
    """這個「第 N 章」看起來是不是在講本書的章(就算在白名單放行的範圍裡,也必須寫成記號):
    同一個子句裡前面寫了「本書」、而且「本書」之後沒有再提到別的書;
    或後面緊接著〈書名〉/「書名」,而書名和本書第 N 章的章名吻合。"""
    lo = max(0, start - 400)
    clause = text[lo:start]
    cut = [m.end() for m in CLAUSE_END.finditer(clause)]
    clause = re.sub(r'<[^>]*>', '', clause[cut[-1]:] if cut else clause)
    mine = [m.start() for m in THIS_BOOK.finditer(clause)]
    other = [m.start() for m in OTHER_SOURCE.finditer(clause)]
    if mine and (not other or other[-1] < mine[-1]):
        return True
    m = TITLED.match(text, end)
    n = NUM_IN_REF.search(text, start, end)
    if m and n and n.group(0) in by_num:
        a, b = _grams(m.group(1)), _grams(book[by_num[n.group(0)]]['title'])
        return len(a & b) / len(a) >= 0.5
    return False


def bare_refs(text):
    """內文裡沒有寫成記號的章號與部號:[(起, 訖, 'ch'|'part', 比對文字)]。"""
    spans = exempt_spans(text)
    out = []
    for m in REF_RE.finditer(text):
        if not in_spans(m.start(), spans):
            out.append((m.start(), m.end(), 'ch', m.group(0)))
    for m in PART_REF_RE.finditer(text):
        if not in_spans(m.start(), spans):
            out.append((m.start(), m.end(), 'part', m.group(0)))
    return sorted(out)


__all__ = ['TOKEN_RE', 'KINDS', 'REF_RE', 'NUM_IN_REF', 'PART_REF_RE', 'TokenError', 'resolve', 'bad_tokens',
           'bare_refs', 'book_context', 'load_allowlist', 'allowed', 'covers', 'window', 'exempt_spans',
           'in_spans', 'part_head', 'load_book']
