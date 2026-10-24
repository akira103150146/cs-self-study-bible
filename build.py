#!/usr/bin/env python3
"""由 chapters/src/*.html 片段 + chapters/_layout.html 模板,產生 chapters/*.html。
行尾全程 newline='' 不翻譯(保留 CRLF);字面代入,{{CONTENT}} 最後代入。
片段裡的章號記號({{ch:<id>}}、{{num:<id>}}、{{part:<id>}}、{{partnum:<id>}},見 _chapter_tokens.py)
在套模板之前依 assets/book.js 代入成「第 N 章」、部名等文字;記號寫錯時直接失敗。
用法:
  python build.py             產生全部 src/*.html
  python build.py 01-what-is-cs   只產生該章
  python build.py --verify    確認所有產出與 src 同步
  python build.py --check     對 chapters/*.html 跑驗證器,不寫檔
"""
import sys, os, re, glob, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)   # python -I 也找得到共用模組
from _chapter_tokens import TokenError, load_book, resolve  # noqa: E402
CH = os.path.join(ROOT, 'chapters')
SRC = os.path.join(CH, 'src')
LAYOUT_PATH = os.path.join(CH, '_layout.html')
VALIDATOR = os.path.join(CH, '_validate_chapter.py')

META_RE = re.compile(r'\A<!--meta\r?\n(.*?)\r?\n-->\r?\n', re.S)

def read(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return f.read()

def write(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)

def parse_fragment(text, name, book=None):
    """回傳 (meta, content);給了 book 就順便把章號記號代入(meta 的 title/description 與內文)。"""
    m = META_RE.match(text)
    if not m:
        raise ValueError(f'{name}: 片段開頭缺少 <!--meta ... --> 前置區')
    meta = {}
    for line in m.group(1).split('\n'):
        line = line.rstrip('\r')
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    for key in ('title', 'description'):
        if key not in meta:
            raise ValueError(f'{name}: meta 缺少必填欄位 {key}')
    content = text[m.end():]
    if book is not None:
        meta = {k: resolve(v, book, f'{name} meta {k}') for k, v in meta.items()}
        content = resolve(content, book, name)
    return meta, content

def scripts_html(meta):
    raw = meta.get('scripts', '').strip()
    if not raw:
        return ''
    parts = [p.strip() for p in raw.split(',') if p.strip()]
    return ''.join(f'<script src="../assets/{p}"></script>\r\n' for p in parts)

def render(layout, meta, content):
    out = layout
    out = out.replace('{{TITLE}}', meta['title'])
    out = out.replace('{{DESCRIPTION}}', meta['description'])
    out = out.replace('{{SCRIPTS}}', scripts_html(meta))
    out = out.replace('{{CONTENT}}', content)  # 最後代入,不再掃描
    return out

def build_one(src_path, layout, book):
    name = os.path.basename(src_path)
    meta, content = parse_fragment(read(src_path), name, book)
    # 防禦性:.gitattributes 已釘 CRLF,正常情況此分支不會觸發;萬一遇到 LF-only 片段仍能產生一致行尾的輸出
    if '\r\n' not in content:
        layout_used = layout.replace('\r\n', '\n')
    else:
        layout_used = layout
    out_path = os.path.join(CH, name)
    write(out_path, render(layout_used, meta, content))
    return out_path

def validate(paths):
    return subprocess.run([sys.executable, VALIDATOR, *paths]).returncode

def main(argv):
    try:
        return _main(argv)
    except TokenError as e:
        print(f'章號記號錯誤:{e}')
        sys.exit(2)

def _main(argv):
    book, _ = load_book()
    if argv and argv[0] == '--verify':
        layout = read(LAYOUT_PATH)
        stale = []
        for s in sorted(glob.glob(os.path.join(SRC, '*.html'))):
            name = os.path.basename(s)
            meta, content = parse_fragment(read(s), name, book)
            # 與 build_one 保持一致:LF-only 片段使用 LF 版 layout
            layout_used = layout if '\r\n' in content else layout.replace('\r\n', '\n')
            if not os.path.exists(os.path.join(CH, name)) or read(os.path.join(CH, name)) != render(layout_used, meta, content):
                stale.append(name)
        if stale:
            print('以下產出與 src 不同步(請執行 python build.py):')
            for n in stale:
                print('  -', n)
            sys.exit(1)
        print(f'所有產出與 src 同步({len(glob.glob(os.path.join(SRC, "*.html")))} 章)。')
        sys.exit(0)
    if argv and argv[0] == '--check':         # 選用的 lint;接受指定章或全部
        names = argv[1:]
        if names:
            outs = [os.path.join(CH, n if n.endswith('.html') else n + '.html') for n in names]
        else:
            outs = [p for p in sorted(glob.glob(os.path.join(CH, '*.html')))
                    if not os.path.basename(p).startswith('_')]
        sys.exit(validate(outs))
    layout = read(LAYOUT_PATH)
    if argv:
        srcs = [os.path.join(SRC, a if a.endswith('.html') else a + '.html') for a in argv]
    else:
        srcs = sorted(glob.glob(os.path.join(SRC, '*.html')))
    if not srcs:
        print('沒有找到任何 src 片段。'); sys.exit(0)
    outs = []
    for s in srcs:
        if not os.path.exists(s):
            print(f'找不到片段:{s}'); sys.exit(2)
        outs.append(build_one(s, layout, book))
    print(f'已產生 {len(outs)} 章。(結構/跳脫自檢為選用:python build.py --check [章])')
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
