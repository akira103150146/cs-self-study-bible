# -*- coding: utf-8 -*-
"""HTML 骨架與零件。只管排版,不含任何教學內容。"""
import html

FONTS = ("https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700"
         "&family=Noto+Sans+TC:wght@400;700&family=Lora:ital,wght@0,400;0,600;0,700;1,400"
         "&family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap")

TABS = [("理論教案", "理論教案"), ("例題-學生版", "例題·學生"),
        ("例題-教師版", "例題·教師"), ("實作", "實作")]


def esc(s):
    """內文的 < > & 跳脫(不動引號,數學式常有 ')。"""
    return html.escape(s, quote=False)


def chip(text, accent=False):
    return f'<span class="chip{" accent" if accent else ""}">{text}</span>'


def callout(kind, ico, title, body):
    return (f'<div class="callout {kind}"><div class="ico">{ico}</div>'
            f'<div><span class="c-title">{title}</span>{body}</div></div>')


def nav(wk, active, tabs=None):
    parts = [f'<a class="home" href="../index.html"><span class="dot">∫</span>微積分(一) · 第 {wk} 週</a>']
    for suffix, label in (tabs or TABS):
        cur = ' aria-current="page"' if suffix == active else ''
        parts.append(f'<a class="tab" href="W{wk}-{suffix}.html"{cur}>{label}</a>')
    parts.append('<span class="spacer"></span>')
    parts.append('<button class="theme-toggle" title="切換深淺色" aria-label="切換主題">☾</button>')
    return '<nav class="packet-nav">\n  ' + "\n  ".join(parts) + '\n</nav>'


THEME_JS = """<script>
(function(){var b=document.querySelector('.theme-toggle'),r=document.documentElement;
function e(){return r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');}
b.textContent=e()==='dark'?'☀':'☾';
b.addEventListener('click',function(){var n=e()==='dark'?'light':'dark';r.setAttribute('data-theme',n);
try{localStorage.setItem('handout-theme',n);}catch(x){}b.textContent=n==='dark'?'☀':'☾';});})();
</script>"""

MATHJAX = """<script>
window.MathJax = { tex: { inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }, svg: { fontCache: 'global' } };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>"""


def page(title, desc, wk, active, masthead_html, body, depth=1, tabs=None):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<script>(function(){{try{{var t=localStorage.getItem('handout-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/handout.css">
{MATHJAX}
</head>
<body>
{nav(wk, active, tabs)}

<main class="sheet">
{masthead_html}
{body}
  <footer class="foot">微積分(一) · 第 {wk} 週　|　風格延續《CS 自學聖經》設計系統</footer>
</main>
{THEME_JS}
</body>
</html>
"""


def masthead(eyebrow, h1, subtitle, chips):
    return (f'  <header class="masthead">\n'
            f'    <div class="eyebrow">{eyebrow}</div>\n'
            f'    <h1>{h1}</h1>\n'
            f'    <p class="subtitle">{subtitle}</p>\n'
            f'    <div class="chips">{"".join(chips)}</div>\n'
            f'  </header>')


def table(headers, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    attr = f' class="{cls}"' if cls else ""
    return (f'<div class="tbl-wrap"><table{attr}>'
            f"<thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>")
