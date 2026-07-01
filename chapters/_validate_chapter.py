#!/usr/bin/env python3
"""章節結構驗證:檢查章節是否符合 _AUTHOR_GUIDE.md 骨架與跳脫規範。
用法:python _validate_chapter.py <chapter.html> [more.html ...]"""
import sys, re, os

REQUIRED = [
    ('<!DOCTYPE html>', 'DOCTYPE'),
    ('class="eyebrow"', 'eyebrow 區塊'),
    ('class="subtitle"', 'subtitle'),
    ('class="byline"', 'byline'),
    ('class="objectives"', 'objectives 區塊'),
    ('把這一章串起來', '章末總結小節'),
    ('../assets/style.css', 'CSS 連結'),
    ('../assets/book.js', 'book.js 連結'),
]

def check(path):
    src = open(path, encoding='utf-8').read()
    errs = []
    for needle, label in REQUIRED:
        if needle not in src:
            errs.append(f'缺少 {label}({needle})')
    h1 = len(re.findall(r'<h1[ >]', src))
    if h1 != 1:
        errs.append(f'<h1> 應恰好 1 個,實際 {h1}')
    h2 = len(re.findall(r'<h2[ >]', src))
    if h2 < 8:
        errs.append(f'<h2> 至少 8 個,實際 {h2}')
    if re.search(r'<style[ >]', src):
        errs.append('不得使用 <style> 區塊')
    for i, code in enumerate(re.findall(r'<code[^>]*>(.*?)</code>', src, re.S)):
        stripped = re.sub(r'&(lt|gt|amp|quot|apos|#\d+|#x[0-9a-fA-F]+);', '', code)
        if '<' in stripped or '>' in stripped or '&' in stripped:
            snippet = code[:60].replace('\n', ' ')
            errs.append(f'第 {i+1} 個 <code> 內有未跳脫的 < > 或 &:{snippet!r}')
    chdir = os.path.dirname(path) or '.'
    for href in re.findall(r'href="([0-9][^"]*\.html)"', src):
        if not os.path.exists(os.path.join(chdir, href)):
            errs.append(f'跨章連結目標不存在:{href}')
    return errs

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法:python _validate_chapter.py <chapter.html> ...'); sys.exit(2)
    bad = False
    for p in sys.argv[1:]:
        errs = check(p)
        if errs:
            bad = True
            print(f'✗ {p}')
            for e in errs:
                print(f'   - {e}')
        else:
            print(f'✓ {p}')
    sys.exit(1 if bad else 0)
