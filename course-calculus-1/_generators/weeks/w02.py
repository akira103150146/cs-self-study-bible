# -*- coding: utf-8 -*-
"""第 2 週｜反函數微分、反三角與雙曲函數

銜接課把「正向」的微分法則練熟了。這一週補的是反方向:
已知 f 的導數,能不能直接寫出 f⁻¹ 的導數?答案是可以,而且只要一張圖就講得通。
證明時刻:反函數微分公式 (f⁻¹)'(b) = 1/f'(a)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Inverse Functions", title_zh="反函數",
    sub="One-to-one is the price of admission; the graph is a mirror across y = x",
    idea="$f$ has an inverse exactly when it is one-to-one. Then $f^{-1}(f(x))=x$, and the graph of "
         "$f^{-1}$ is the reflection of the graph of $f$ across the line $y=x$. A strictly "
         "increasing (or strictly decreasing) function is automatically one-to-one.",
    deep="<p>先把「什麼時候有反函數」講死,後面的微分公式才站得住。</p>"
         "<p class='step'><strong>水平線檢驗</strong>:任一條水平線最多只能碰圖形一次。"
         "等價地說,$f$ 必須是一對一。</p>"
         "<p class='step'><strong>單調 ⟹ 一對一</strong>:若 $f'&gt;0$ 在整個區間成立,$f$ 嚴格遞增,"
         "自動一對一。這是實務上最好用的判準——而且它把「反函數存在」和「導數」接了起來,"
         "正好是下一個觀念的引子。</p>"
         "<p><strong>對稱的幾何意義</strong>:$(a,b)$ 在 $f$ 上 $\\iff$ $(b,a)$ 在 $f^{-1}$ 上。"
         "把紙沿 $y=x$ 對摺,兩條曲線會疊在一起。這張圖是本週所有公式的來源,一定要畫。</p>"
         "<p>$\\sin x$ 在 $\\mathbb{R}$ 上不是一對一,所以談 $\\arcsin$ 之前必須先"
         "<strong>限制定義域</strong>到 $\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$。"
         "這個「切一段下來」的動作,是觀念 3 的全部麻煩來源。<span class='qed'>∎</span></p>",
    guide=["$f(x)=x^{3}$ 有沒有反函數?$f(x)=x^{2}$ 呢?差別在哪裡?",
           "若 $f'(x)&gt;0$ 恆成立,$f$ 是遞增還是遞減?這保證了什麼?",
           "點 $(2,8)$ 在 $y=x^{3}$ 上。那 $y=\\sqrt[3]{x}$ 上一定有哪個點?",
           "把兩條曲線畫在同一張圖上,它們對稱於哪一條直線?"],
    demo="Show that $f(x)=x^{3}+x$ has an inverse on $\\mathbb{R}$, and find $f^{-1}(2)$.",
    demo_sol="<p>$f'(x)=3x^{2}+1&gt;0$ 恆成立 ⟹ $f$ 嚴格遞增 ⟹ 一對一 ⟹ 反函數存在。</p>"
             "<p>求 $f^{-1}(2)$ 就是解 $f(x)=2$:</p>"
             "$$x^{3}+x=2\\ \\Longrightarrow\\ x^{3}+x-2=(x-1)(x^{2}+x+2)=0.$$"
             "<p>二次因式判別式 $1-8&lt;0$ 無實根,故 $x=1$。因此 $f^{-1}(2)=1$。</p>",
    demo_hint="先用導數說明它一對一,再解 $f(x)=2$。",
    misstep="以為「有反函數」要真的把 $f^{-1}$ 的公式解出來。多數情況解不出來,"
            "但<strong>存在性</strong>只靠單調就夠了。",
    level="basic",
    drills=[
        ("Does $f(x)=x^{2}$ have an inverse on $\\mathbb{R}$? On $[0,\\infty)$?",
         "<p>在 $\\mathbb{R}$ 上沒有($f(-2)=f(2)$,不是一對一);限制到 $[0,\\infty)$ 就有,"
         "反函數是 $\\sqrt{x}$。</p>"),
        ("Show $f(x)=x^{5}+2x+1$ is one-to-one on $\\mathbb{R}$.",
         "<p>$f'(x)=5x^{4}+2&gt;0$ 恆成立 ⟹ 嚴格遞增 ⟹ 一對一。</p>"),
        ("The point $(3,10)$ lies on the graph of $f$. Which point must lie on the graph of "
         "$f^{-1}$? What is $f^{-1}(10)$?",
         "<p>$(10,3)$ 在 $f^{-1}$ 上,故 $f^{-1}(10)=3$。</p>"),
    ])

C2 = Concept(
    title_en="Derivative of an Inverse", title_zh="反函數的導數",
    sub="Reflecting a graph swaps rise and run — so the slope flips over",
    idea="If $f$ is differentiable and one-to-one with $f(a)=b$ and $f'(a)\\ne0$, then "
         "$$\\left(f^{-1}\\right)'(b)=\\frac{1}{f'(a)}=\\frac{1}{f'\\!\\left(f^{-1}(b)\\right)}.$$ "
         "You never need a formula for $f^{-1}$ itself — only the point.",
    deep="<p><strong>先給圖像,再給代數</strong>。反射把 $x$ 與 $y$ 對調,所以「上升/水平」變成"
         "「水平/上升」——斜率取倒數。學生看懂這句話,公式就背不掉了。</p>"
         "<p><strong>代數證明</strong>(本週的證明時刻):由定義出發,對</p>"
         "$$f\\!\\left(f^{-1}(x)\\right)=x$$"
         "<p class='step'>兩邊對 $x$ 微分,左邊用<strong>鏈鎖法則</strong>:</p>"
         "$$f'\\!\\left(f^{-1}(x)\\right)\\cdot\\left(f^{-1}\\right)'(x)=1.$$"
         "<p class='step'>只要 $f'\\!\\left(f^{-1}(x)\\right)\\ne0$,兩邊同除即得</p>"
         "$$\\left(f^{-1}\\right)'(x)=\\frac{1}{f'\\!\\left(f^{-1}(x)\\right)}.$$"
         "<p><strong>三個前提缺一不可</strong>,考卷最愛在這裡挖洞:</p>"
         "<ul>"
         "<li>$f$ 一對一(否則 $f^{-1}$ 根本不存在)</li>"
         "<li>$f$ 在 $a$ 可微</li>"
         "<li>$f'(a)\\ne0$——若 $f'(a)=0$,反射後切線變成<strong>鉛直</strong>,$f^{-1}$ 在該點不可微。"
         "$f(x)=x^{3}$ 在 $x=0$ 就是活例子:$f'(0)=0$,而 $\\sqrt[3]{x}$ 在 $0$ 的切線是鉛直的。</li>"
         "</ul>"
         "<p>本週後面所有反三角、反雙曲的導數公式,<strong>全部</strong>是這一條的特例。"
         "<span class='qed'>∎</span></p>",
    guide=["把 $f\\!\\left(f^{-1}(x)\\right)=x$ 兩邊對 $x$ 微分。左邊要用哪一條法則?",
           "微分後左邊變成 $f'\\!\\left(f^{-1}(x)\\right)\\cdot$ <span class=\"blank\"></span>,右邊是 "
           "<span class=\"blank\"></span>。",
           "移項後 $\\left(f^{-1}\\right)'(x)=$ <span class=\"blank\"></span>。什麼時候這個式子會壞掉?",
           "從圖形想:反射把上升與水平對調,所以斜率會 <span class=\"blank\"></span>。"],
    demo="Let $f(x)=x^{3}+x$. Given $f(1)=2$, compute $\\left(f^{-1}\\right)'(2)$ without finding "
         "a formula for $f^{-1}$.",
    demo_sol="<p>$f'(x)=3x^{2}+1$,故 $f'(1)=4$。由公式:</p>"
             "$$\\left(f^{-1}\\right)'(2)=\\frac{1}{f'(1)}=\\frac14.$$"
             "<p>注意整個過程<strong>完全沒有用到 $f^{-1}$ 的公式</strong>——事實上 "
             "$x^{3}+x=y$ 解 $x$ 相當醜。這正是這條公式的價值。</p>",
    demo_hint="要用 $\\left(f^{-1}\\right)'(b)=\\dfrac{1}{f'(a)}$,你需要先知道哪一個 $a$?",
    misstep="把 $\\dfrac{1}{f'(a)}$ 寫成 $\\dfrac{1}{f'(b)}$。導數要代在<strong>原函數的</strong>"
            "那個點 $a=f^{-1}(b)$,不是 $b$。",
    level="mid",
    drills=[
        ("Let $f(x)=x^{5}+2x+1$ with $f(1)=4$. Find $\\left(f^{-1}\\right)'(4)$.",
         "<p>$f'(x)=5x^{4}+2$,$f'(1)=7$,故 $\\left(f^{-1}\\right)'(4)=\\dfrac17$。</p>"),
        ("Let $f(x)=x^{3}$. Explain why $f^{-1}$ fails to be differentiable at $0$.",
         "<p>$f'(0)=0$,公式的分母為零。幾何上 $\\sqrt[3]{x}$ 在 $0$ 的切線是鉛直線,斜率不存在。</p>"),
        ("Suppose $g$ is the inverse of $f$, $f(2)=5$, and $f'(2)=3$. Find $g'(5)$.",
         "<p>$g'(5)=\\dfrac{1}{f'(2)}=\\dfrac13$。</p>"),
    ])

C3 = Concept(
    title_en="Inverse Sine and Cosine", title_zh="反正弦與反餘弦",
    sub="Cut a monotone slice first — that slice is the range of the inverse",
    idea="$\\sin$ is not one-to-one on $\\mathbb{R}$, so $\\arcsin$ is defined by restricting the "
         "domain to $\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$; that interval becomes the "
         "<em>range</em> of $\\arcsin$. Similarly $\\arccos$ has range $[0,\\pi]$.",
    deep="<p>學生在這裡最常出的錯不是計算,是<strong>值域</strong>。把兩個值域寫在黑板右上角,"
         "整週不要擦掉:</p>"
         "<p class='step'>$\\arcsin:[-1,1]\\to\\left[-\\dfrac{\\pi}{2},\\dfrac{\\pi}{2}\\right]$、"
         "$\\arccos:[-1,1]\\to[0,\\pi]$、$\\arctan:\\mathbb{R}\\to"
         "\\left(-\\dfrac{\\pi}{2},\\dfrac{\\pi}{2}\\right)$。</p>"
         "<p><strong>為什麼 $\\arccos$ 的值域不是對稱區間</strong>:$\\cos$ 在 "
         "$\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 上不是一對一(它在 $0$ 有最大值),"
         "必須改切 $[0,\\pi]$ 這段遞減的部分。這不是數學家任性,是被單調性逼的。</p>"
         "<p><strong>經典陷阱</strong>:$\\arcsin\\left(\\sin\\frac{5\\pi}{6}\\right)$ 不是 "
         "$\\frac{5\\pi}{6}$,因為 $\\frac{5\\pi}{6}$ 不在值域內。正解:"
         "$\\sin\\frac{5\\pi}{6}=\\frac12$,而 $\\arcsin\\frac12=\\frac{\\pi}{6}$。</p>"
         "<p>一句話:<strong>$\\arcsin(\\sin\\theta)=\\theta$ 只在 $\\theta$ 落在值域內才成立</strong>,"
         "反過來 $\\sin(\\arcsin x)=x$ 則對所有 $x\\in[-1,1]$ 都對。"
         "兩個方向不對稱,這是本觀念的核心。<span class='qed'>∎</span></p>",
    guide=["$\\sin x$ 在整個 $\\mathbb{R}$ 上是一對一嗎?要切哪一段才會是?",
           "所以 $\\arcsin$ 的值域是 <span class=\"blank\"></span>,定義域是 "
           "<span class=\"blank\"></span>。",
           "$\\cos$ 為什麼不能切同一段?(想它在 $0$ 附近的形狀)所以 $\\arccos$ 的值域是 "
           "<span class=\"blank\"></span>。",
           "$\\arcsin\\left(\\sin\\dfrac{5\\pi}{6}\\right)$ 等於 $\\dfrac{5\\pi}{6}$ 嗎?"
           "先問:$\\dfrac{5\\pi}{6}$ 在值域裡嗎?"],
    demo="Evaluate $\\arcsin\\!\\left(\\sin\\dfrac{5\\pi}{6}\\right)$ and "
         "$\\arccos\\!\\left(\\cos\\dfrac{7\\pi}{6}\\right)$.",
    demo_sol="<p><strong>第一個</strong>:$\\dfrac{5\\pi}{6}\\notin\\left[-\\dfrac{\\pi}{2},"
             "\\dfrac{\\pi}{2}\\right]$,不能直接消掉。先算內層:"
             "$\\sin\\dfrac{5\\pi}{6}=\\dfrac12$,再取 $\\arcsin\\dfrac12=\\dfrac{\\pi}{6}$。</p>"
             "<p><strong>第二個</strong>:$\\dfrac{7\\pi}{6}\\notin[0,\\pi]$。"
             "$\\cos\\dfrac{7\\pi}{6}=-\\dfrac{\\sqrt3}{2}$,而 "
             "$\\arccos\\!\\left(-\\dfrac{\\sqrt3}{2}\\right)=\\dfrac{5\\pi}{6}$。</p>"
             "<p>兩題的答案都<strong>不等於</strong>原本的角——這就是值域限制的代價。</p>",
    demo_hint="先問:裡面那個角落在值域內嗎?不在的話就不能直接消掉。",
    misstep="無腦約掉:$\\arcsin(\\sin\\theta)=\\theta$。只有 $\\theta$ 在值域內才成立。",
    level="mid",
    drills=[
        ("Evaluate $\\arcsin\\!\\left(-\\dfrac{1}{2}\\right)$ and $\\arccos(0)$.",
         "<p>$\\arcsin\\!\\left(-\\dfrac12\\right)=-\\dfrac{\\pi}{6}$(落在 "
         "$\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$);$\\arccos 0=\\dfrac{\\pi}{2}$。</p>"),
        ("Evaluate $\\arcsin\\!\\left(\\sin\\dfrac{3\\pi}{4}\\right)$.",
         "<p>$\\dfrac{3\\pi}{4}$ 不在值域。$\\sin\\dfrac{3\\pi}{4}=\\dfrac{\\sqrt2}{2}$,"
         "故答案為 $\\dfrac{\\pi}{4}$。</p>"),
        ("Simplify $\\cos(\\arcsin x)$ for $x\\in[-1,1]$.",
         "<p>令 $\\theta=\\arcsin x$,則 $\\sin\\theta=x$ 且 $\\theta\\in\\left[-\\frac{\\pi}{2},"
         "\\frac{\\pi}{2}\\right]$,該區間上 $\\cos\\theta\\ge0$,故 "
         "$\\cos\\theta=\\sqrt{1-x^{2}}$。</p>"),
    ])

C4 = Concept(
    title_en="Derivatives of Inverse Trig Functions", title_zh="反三角函數的導數",
    sub="Every one of them falls out of the inverse-derivative formula plus one triangle",
    idea="$$\\frac{d}{dx}\\arcsin x=\\frac{1}{\\sqrt{1-x^{2}}},\\qquad "
         "\\frac{d}{dx}\\arccos x=\\frac{-1}{\\sqrt{1-x^{2}}},\\qquad "
         "\\frac{d}{dx}\\arctan x=\\frac{1}{1+x^{2}}.$$ "
         "Notice the algebraic results — no trigonometric functions survive.",
    deep="<p>不要叫學生背。<strong>當場推一次</strong>,他們會發現三條公式是同一個動作。</p>"
         "<p class='step'>令 $y=\\arcsin x$,則 $\\sin y=x$。兩邊對 $x$ 微分(隱函數):</p>"
         "$$\\cos y\\cdot\\frac{dy}{dx}=1\\ \\Longrightarrow\\ \\frac{dy}{dx}=\\frac{1}{\\cos y}.$$"
         "<p class='step'>剩下要把 $\\cos y$ 換成 $x$。畫直角三角形:對邊 $x$、斜邊 $1$,"
         "鄰邊就是 $\\sqrt{1-x^{2}}$,故 $\\cos y=\\sqrt{1-x^{2}}$。</p>"
         "<p><strong>為什麼取正根</strong>:因為 $y\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$,"
         "在這個區間 $\\cos y\\ge0$。這一步<strong>用到了值域</strong>——觀念 3 的限制在這裡回收,"
         "不是白講的。</p>"
         "<p class='step'>$\\arctan$ 同理:$\\tan y=x$,$\\sec^{2}y\\cdot y'=1$,"
         "而 $\\sec^{2}y=1+\\tan^{2}y=1+x^{2}$,故 $y'=\\dfrac{1}{1+x^{2}}$。這一條連三角形都不用畫。</p>"
         "<p><strong>最值得驚訝的地方</strong>:三角函數的反函數,導數竟然是<strong>純代數式</strong>。"
         "這件事在積分時會大有用處——$\\displaystyle\\int\\frac{dx}{1+x^{2}}=\\arctan x+C$,"
         "一個看起來毫無三角味的積分,答案是反三角。W5 會再遇到。<span class='qed'>∎</span></p>",
    guide=["令 $y=\\arcsin x$,把它改寫成不含 arcsin 的式子:<span class=\"blank\"></span>$=x$。",
           "兩邊對 $x$ 微分(左邊 $y$ 是 $x$ 的函數,要用鏈鎖):得 "
           "<span class=\"blank\"></span>$\\cdot y'=1$。",
           "畫一個直角三角形:$\\sin y=x$ 表示對邊 $x$、斜邊 $1$,那鄰邊是 "
           "<span class=\"blank\"></span>,所以 $\\cos y=$ <span class=\"blank\"></span>。",
           "為什麼可以放心取<strong>正</strong>根?(想 $y$ 的範圍)"],
    demo="Derive $\\dfrac{d}{dx}\\arctan x$ from the inverse-derivative formula, then compute "
         "$\\dfrac{d}{dx}\\arcsin(2x)$.",
    demo_sol="<p><strong>推導</strong>:令 $y=\\arctan x$,則 $\\tan y=x$。微分得 "
             "$\\sec^{2}y\\cdot y'=1$。由 $\\sec^{2}y=1+\\tan^{2}y=1+x^{2}$:</p>"
             "$$\\frac{d}{dx}\\arctan x=\\frac{1}{1+x^{2}}.$$"
             "<p><strong>套用鏈鎖</strong>:外層 $\\arcsin$、內層 $2x$:</p>"
             "$$\\frac{d}{dx}\\arcsin(2x)=\\frac{1}{\\sqrt{1-(2x)^{2}}}\\cdot 2"
             "=\\frac{2}{\\sqrt{1-4x^{2}}}.$$",
    demo_hint="先把 $y=\\arctan x$ 改寫成 $\\tan y=x$,再隱函數微分。第二題別忘了內層導數。",
    misstep="鏈鎖的內層導數漏掉,寫成 $\\dfrac{1}{\\sqrt{1-4x^{2}}}$。內層 $2x$ 的導數 $2$ 要乘上去。",
    level="hard",
    drills=[
        ("Differentiate $f(x)=x\\arctan x$.",
         "<p>乘積法則:$\\arctan x+x\\cdot\\dfrac{1}{1+x^{2}}"
         "=\\arctan x+\\dfrac{x}{1+x^{2}}$。</p>"),
        ("Differentiate $f(x)=\\arctan\\!\\left(\\dfrac1x\\right)$ for $x&gt;0$ and simplify.",
         "<p>$\\dfrac{1}{1+1/x^{2}}\\cdot\\left(-\\dfrac{1}{x^{2}}\\right)"
         "=-\\dfrac{1}{x^{2}+1}$。有趣的是它恰為 $-\\dfrac{d}{dx}\\arctan x$——"
         "因為 $\\arctan x+\\arctan\\frac1x$ 在 $x&gt;0$ 是常數 $\\dfrac{\\pi}{2}$。</p>"),
        ("Differentiate $f(x)=\\arcsin x+\\arccos x$. Explain the answer.",
         "<p>$\\dfrac{1}{\\sqrt{1-x^{2}}}-\\dfrac{1}{\\sqrt{1-x^{2}}}=0$。導數為零表示它是常數;"
         "代 $x=0$ 得 $\\dfrac{\\pi}{2}$,故恆等於 $\\dfrac{\\pi}{2}$。</p>"),
    ])

C5 = Concept(
    title_en="Hyperbolic Functions", title_zh="雙曲函數",
    sub="Built from exponentials, but they behave like trig with one sign flipped",
    idea="$$\\sinh x=\\frac{e^{x}-e^{-x}}{2},\\qquad \\cosh x=\\frac{e^{x}+e^{-x}}{2},\\qquad "
         "\\tanh x=\\frac{\\sinh x}{\\cosh x}.$$ "
         "The signature identity is $\\cosh^{2}x-\\sinh^{2}x=1$ — a minus sign where the "
         "trigonometric identity has a plus.",
    deep="<p><strong>為什麼資工系要學這個</strong>:$\\tanh$ 是神經網路最早的 activation function 之一,"
         "W6 的 capstone(銜接課那個 2 層網路)用的就是它。今天把它的來歷講清楚。</p>"
         "<p class='step'>名字裡的「雙曲」來自:$(\\cosh t,\\sinh t)$ 描出雙曲線 $x^{2}-y^{2}=1$,"
         "正如 $(\\cos t,\\sin t)$ 描出圓 $x^{2}+y^{2}=1$。差別只在那個減號。</p>"
         "<p class='step'>驗證招牌恆等式,直接展開就好:</p>"
         "$$\\cosh^{2}x-\\sinh^{2}x=\\frac{(e^{x}+e^{-x})^{2}-(e^{x}-e^{-x})^{2}}{4}"
         "=\\frac{4}{4}=1.$$"
         "<p><strong>圖形要點</strong>:$\\cosh$ 是偶函數、最小值 $\\cosh 0=1$、形狀像懸掛的鏈條"
         "(觀念 9 會證);$\\sinh$ 是奇函數、嚴格遞增(所以有反函數);"
         "$\\tanh$ 是奇函數、值域 $(-1,1)$、兩側水平漸近線 $y=\\pm1$——"
         "<strong>這正是它適合當 activation 的原因:把任意實數壓進 $(-1,1)$</strong>。</p>"
         "<p>順帶一提 $\\tanh$ 的飽和問題:$|x|$ 大時 $\\tanh'(x)=\\operatorname{sech}^{2}x\\to0$,"
         "梯度消失。這個現象 W17 的 capstone 會再碰到。<span class='qed'>∎</span></p>",
    guide=["把 $\\sinh x=\\dfrac{e^{x}-e^{-x}}{2}$ 代入 $x=0$,得 <span class=\"blank\"></span>;"
           "$\\cosh 0=$ <span class=\"blank\"></span>。",
           "$\\sinh(-x)$ 和 $\\sinh x$ 什麼關係?$\\cosh(-x)$ 呢?(奇函數還是偶函數)",
           "把 $\\cosh^{2}x-\\sinh^{2}x$ 直接展開算算看,結果是 <span class=\"blank\"></span>。",
           "$x\\to\\infty$ 時 $\\tanh x\\to$ <span class=\"blank\"></span>。"
           "這件事對神經網路的 activation 有什麼好處?"],
    demo="Verify $\\cosh^{2}x-\\sinh^{2}x=1$ from the definitions, and find "
         "$\\displaystyle\\lim_{x\\to\\infty}\\tanh x$.",
    demo_sol="<p><strong>恆等式</strong>:</p>"
             "$$\\cosh^{2}x-\\sinh^{2}x=\\frac{(e^{x}+e^{-x})^{2}-(e^{x}-e^{-x})^{2}}{4}"
             "=\\frac{\\left(e^{2x}+2+e^{-2x}\\right)-\\left(e^{2x}-2+e^{-2x}\\right)}{4}"
             "=\\frac{4}{4}=1.$$"
             "<p><strong>極限</strong>:分子分母同除 $e^{x}$:</p>"
             "$$\\tanh x=\\frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}=\\frac{1-e^{-2x}}{1+e^{-2x}}"
             "\\xrightarrow{x\\to\\infty}\\frac{1-0}{1+0}=1.$$"
             "<p>同理 $x\\to-\\infty$ 時趨近 $-1$。所以 $\\tanh$ 把整條實數線壓進 $(-1,1)$。</p>",
    demo_hint="恆等式直接展開平方就好;極限記得上下同除 $e^{x}$。",
    misstep="把 $\\cosh^{2}-\\sinh^{2}$ 記成 $\\sinh^{2}-\\cosh^{2}$。順序反了會得到 $-1$。",
    level="mid",
    drills=[
        ("Show that $\\sinh$ is odd and $\\cosh$ is even.",
         "<p>$\\sinh(-x)=\\dfrac{e^{-x}-e^{x}}{2}=-\\sinh x$(奇);"
         "$\\cosh(-x)=\\dfrac{e^{-x}+e^{x}}{2}=\\cosh x$(偶)。</p>"),
        ("Find $\\displaystyle\\lim_{x\\to-\\infty}\\tanh x$ and state the horizontal asymptotes "
         "of $y=\\tanh x$.",
         "<p>$-1$。水平漸近線為 $y=1$ 與 $y=-1$。</p>"),
        ("Prove $\\sinh(2x)=2\\sinh x\\cosh x$.",
         "<p>$2\\cdot\\dfrac{e^{x}-e^{-x}}{2}\\cdot\\dfrac{e^{x}+e^{-x}}{2}"
         "=\\dfrac{e^{2x}-e^{-2x}}{2}=\\sinh 2x$。和三角的倍角公式長得一模一樣。</p>"),
    ])

C6 = Concept(
    title_en="Derivatives of Hyperbolic Functions", title_zh="雙曲函數的導數",
    sub="Almost the trig rules — but cosh differentiates without the minus sign",
    idea="$$\\frac{d}{dx}\\sinh x=\\cosh x,\\qquad \\frac{d}{dx}\\cosh x=\\sinh x,\\qquad "
         "\\frac{d}{dx}\\tanh x=\\operatorname{sech}^{2}x.$$ "
         "The pattern mirrors $\\sin$ and $\\cos$ except that no minus sign appears.",
    deep="<p>不用背,直接微分定義式:</p>"
         "$$\\frac{d}{dx}\\sinh x=\\frac{d}{dx}\\frac{e^{x}-e^{-x}}{2}"
         "=\\frac{e^{x}+e^{-x}}{2}=\\cosh x.$$"
         "<p class='step'>$\\cosh$ 同理得 $\\sinh x$——注意 $-e^{-x}$ 微分後是 $+e^{-x}$,"
         "<strong>負負得正</strong>,所以沒有那個惱人的負號。這是雙曲比三角好記的地方。</p>"
         "<p class='step'>$\\tanh$ 用商法則:</p>"
         "$$\\frac{d}{dx}\\tanh x=\\frac{\\cosh^{2}x-\\sinh^{2}x}{\\cosh^{2}x}"
         "=\\frac{1}{\\cosh^{2}x}=\\operatorname{sech}^{2}x.$$"
         "<p><strong>接到 ML</strong>:$\\operatorname{sech}^{2}x=1-\\tanh^{2}x$,所以若已經算出 "
         "$a=\\tanh x$,導數就是 $1-a^{2}$——<strong>不必重算 $\\tanh$</strong>。"
         "這正是銜接課 capstone 裡 <code>dZ1 = dA1 * (1 - A1**2)</code> 那一行的來歷。"
         "當時只是照抄,今天他們知道為什麼了。<span class='qed'>∎</span></p>",
    guide=["把 $\\sinh x=\\dfrac{e^{x}-e^{-x}}{2}$ 直接微分。$-e^{-x}$ 微分後變成 "
           "<span class=\"blank\"></span>(注意負負得正)。",
           "所以 $\\dfrac{d}{dx}\\sinh x=$ <span class=\"blank\"></span>。",
           "同樣手法算 $\\dfrac{d}{dx}\\cosh x=$ <span class=\"blank\"></span>。"
           "和 $\\dfrac{d}{dx}\\cos x$ 差在哪裡?",
           "用商法則算 $\\tanh'$,分子會用到哪一條恆等式?"],
    demo="Differentiate $f(x)=\\tanh x$ using the quotient rule, and rewrite the answer in terms "
         "of $\\tanh x$ alone.",
    demo_sol="<p>商法則,分子 $=\\cosh x\\cdot\\cosh x-\\sinh x\\cdot\\sinh x"
             "=\\cosh^{2}x-\\sinh^{2}x=1$:</p>"
             "$$\\frac{d}{dx}\\tanh x=\\frac{1}{\\cosh^{2}x}=\\operatorname{sech}^{2}x.$$"
             "<p>再用 $\\operatorname{sech}^{2}x=1-\\tanh^{2}x$(把恆等式除以 $\\cosh^{2}x$):</p>"
             "$$\\frac{d}{dx}\\tanh x=1-\\tanh^{2}x.$$"
             "<p>這個寫法在程式裡特別好用:算過 $a=\\tanh x$ 之後,導數就是 $1-a^{2}$,"
             "不必再呼叫一次 $\\tanh$。</p>",
    demo_hint="商法則的分子會湊出招牌恆等式。最後把 $\\operatorname{sech}^{2}$ 換成 $\\tanh$ 的式子。",
    misstep="套用三角的記憶寫成 $\\dfrac{d}{dx}\\cosh x=-\\sinh x$。雙曲版<strong>沒有</strong>負號。",
    level="mid",
    drills=[
        ("Differentiate $f(x)=\\cosh(3x)$.",
         "<p>鏈鎖:$\\sinh(3x)\\cdot3=3\\sinh(3x)$。</p>"),
        ("Differentiate $f(x)=x\\sinh x$.",
         "<p>乘積法則:$\\sinh x+x\\cosh x$。</p>"),
        ("Verify that $y=\\cosh x$ satisfies $y''=y$.",
         "<p>$y'=\\sinh x$,$y''=\\cosh x=y$。(順帶一提 $y=\\sinh x$ 也滿足——"
         "它們是 $y''=y$ 的兩個基本解,W15 解 ODE 時會再見面。)</p>"),
    ])

C7 = Concept(
    title_en="Inverse Hyperbolic Functions", title_zh="反雙曲函數",
    sub="Because they are built from exponentials, their inverses are logarithms",
    idea="Solving $\\sinh y=x$ for $y$ gives an explicit logarithm: "
         "$$\\operatorname{arcsinh} x=\\ln\\!\\left(x+\\sqrt{x^{2}+1}\\right),\\qquad "
         "\\frac{d}{dx}\\operatorname{arcsinh} x=\\frac{1}{\\sqrt{x^{2}+1}}.$$ "
         "Unlike the inverse trig functions, these have closed forms.",
    deep="<p>這裡有個反三角做不到的漂亮之處:<strong>反雙曲函數可以解出顯式公式</strong>。</p>"
         "<p class='step'>解 $\\sinh y=x$:令 $u=e^{y}$,則 $\\dfrac{u-u^{-1}}{2}=x$,"
         "兩邊乘 $2u$ 得二次式 $u^{2}-2xu-1=0$,故</p>"
         "$$u=x\\pm\\sqrt{x^{2}+1}.$$"
         "<p class='step'>因為 $u=e^{y}&gt;0$ 而 $x-\\sqrt{x^{2}+1}&lt;0$,只能取正號:"
         "$e^{y}=x+\\sqrt{x^{2}+1}$,即 $y=\\ln\\!\\left(x+\\sqrt{x^{2}+1}\\right)$。</p>"
         "<p><strong>兩條路都能算導數</strong>,值得都示範一次:</p>"
         "<ul>"
         "<li><strong>用反函數公式</strong>:$\\left(\\operatorname{arcsinh}\\right)'"
         "=\\dfrac{1}{\\cosh y}=\\dfrac{1}{\\sqrt{1+\\sinh^{2}y}}=\\dfrac{1}{\\sqrt{1+x^{2}}}$。</li>"
         "<li><strong>直接微分對數式</strong>:$\\dfrac{1}{x+\\sqrt{x^{2}+1}}\\cdot"
         "\\left(1+\\dfrac{x}{\\sqrt{x^{2}+1}}\\right)$,化簡後同樣得 $\\dfrac{1}{\\sqrt{x^{2}+1}}$。</li>"
         "</ul>"
         "<p>兩條路殊途同歸,是檢驗學生有沒有真的懂反函數公式的好題目。</p>"
         "<p>另外兩個:$\\operatorname{arccosh} x=\\ln\\!\\left(x+\\sqrt{x^{2}-1}\\right)\\ (x\\ge1)$、"
         "$\\operatorname{arctanh} x=\\dfrac12\\ln\\dfrac{1+x}{1-x}\\ (|x|&lt;1)$。"
         "後者的導數 $\\dfrac{1}{1-x^{2}}$ 在 W6 的部分分式會再出現。<span class='qed'>∎</span></p>",
    guide=["要解 $\\sinh y=x$,先把 $\\sinh$ 用指數寫開:$\\dfrac{e^{y}-e^{-y}}{2}=x$。",
           "令 $u=e^{y}$,兩邊乘 $2u$,會得到一個關於 $u$ 的 <span class=\"blank\"></span> 次方程式。",
           "解出 $u=x\\pm\\sqrt{x^{2}+1}$。為什麼只能取 <span class=\"blank\"></span> 號?"
           "(想 $e^{y}$ 的正負)",
           "所以 $y=$ <span class=\"blank\"></span>。反三角函數有這種顯式公式嗎?"],
    demo="Derive the explicit formula for $\\operatorname{arcsinh} x$, then find its derivative "
         "in two different ways.",
    demo_sol="<p><strong>顯式公式</strong>:令 $u=e^{y}$,由 $\\dfrac{u-u^{-1}}{2}=x$ 得 "
             "$u^{2}-2xu-1=0$,故 $u=x\\pm\\sqrt{x^{2}+1}$。因 $u&gt;0$ 取正號:</p>"
             "$$\\operatorname{arcsinh} x=\\ln\\!\\left(x+\\sqrt{x^{2}+1}\\right).$$"
             "<p><strong>法一(反函數公式)</strong>:$\\dfrac{1}{\\cosh y}"
             "=\\dfrac{1}{\\sqrt{1+\\sinh^{2}y}}=\\dfrac{1}{\\sqrt{1+x^{2}}}$。</p>"
             "<p><strong>法二(直接微分)</strong>:</p>"
             "$$\\frac{1}{x+\\sqrt{x^{2}+1}}\\left(1+\\frac{x}{\\sqrt{x^{2}+1}}\\right)"
             "=\\frac{1}{x+\\sqrt{x^{2}+1}}\\cdot\\frac{\\sqrt{x^{2}+1}+x}{\\sqrt{x^{2}+1}}"
             "=\\frac{1}{\\sqrt{x^{2}+1}}.$$"
             "<p>兩法一致。$\\;\\blacksquare$</p>",
    demo_hint="先令 $u=e^{y}$ 把式子變成二次方程式;導數可以用反函數公式,也可以直接微分對數式。",
    misstep="解二次式時把負根也留下。$e^{y}$ 恆正,$x-\\sqrt{x^{2}+1}$ 恆負,必須捨去。",
    level="hard",
    drills=[
        ("Differentiate $f(x)=\\operatorname{arctanh} x$ using the inverse-derivative formula.",
         "<p>令 $y=\\operatorname{arctanh}x$,則 $\\tanh y=x$,"
         "$\\operatorname{sech}^{2}y\\cdot y'=1$,而 $\\operatorname{sech}^{2}y=1-\\tanh^{2}y"
         "=1-x^{2}$,故 $y'=\\dfrac{1}{1-x^{2}}$。</p>"),
        ("Show that $\\operatorname{arctanh} x=\\dfrac12\\ln\\dfrac{1+x}{1-x}$ for $|x|&lt;1$.",
         "<p>解 $\\dfrac{u-u^{-1}}{u+u^{-1}}=x$($u=e^{y}$)得 $\\dfrac{u^{2}-1}{u^{2}+1}=x$,"
         "解出 $u^{2}=\\dfrac{1+x}{1-x}$,取對數再除以 2 即得。</p>"),
        ("Compute $\\dfrac{d}{dx}\\ln\\!\\left(x+\\sqrt{x^{2}+1}\\right)$ directly and confirm it "
         "matches $\\dfrac{1}{\\sqrt{x^{2}+1}}$.",
         "<p>$\\dfrac{1+\\frac{x}{\\sqrt{x^{2}+1}}}{x+\\sqrt{x^{2}+1}}"
         "=\\dfrac{\\frac{\\sqrt{x^{2}+1}+x}{\\sqrt{x^{2}+1}}}{x+\\sqrt{x^{2}+1}}"
         "=\\dfrac{1}{\\sqrt{x^{2}+1}}$。吻合。</p>"),
    ])

C8 = Concept(
    title_en="The Catenary", title_zh="懸鏈線",
    sub="A hanging chain is a cosh — not a parabola, though it looks like one",
    idea="A flexible chain hanging under its own weight takes the shape "
         "$y=a\\cosh\\dfrac{x}{a}$, called a catenary. It is visually close to a parabola but "
         "genuinely different — and the difference is measurable.",
    deep="<p>這是本週的<strong>應用收尾</strong>,也是一個很好的「數學不是憑空發明」的故事。</p>"
         "<p class='step'>伽利略猜懸鏈是拋物線,猜錯了。正確答案 $y=a\\cosh\\frac{x}{a}$ 要等到 "
         "微積分發明之後(1691 年,由 Bernoulli 等人解出)。</p>"
         "<p><strong>為什麼是 $\\cosh$</strong>(直覺版,不必嚴格推):取鏈條的一小段做受力分析,"
         "水平張力 $H$ 為常數、鉛直方向承擔的重量正比於<strong>弧長</strong>。列出來會得到</p>"
         "$$y''=\\frac{1}{a}\\sqrt{1+(y')^{2}},$$"
         "<p>而 $y=a\\cosh\\frac{x}{a}$ 恰好滿足它(可以直接代入驗證,見示範)。這是本課第一次遇到"
         "<strong>微分方程</strong>——W14 起會正式處理這類問題。</p>"
         "<p><strong>弧長特別漂亮</strong>:</p>"
         "$$\\sqrt{1+(y')^{2}}=\\sqrt{1+\\sinh^{2}\\frac{x}{a}}=\\cosh\\frac{x}{a},$$"
         "<p>根號自動消失。W11 算弧長時會發現,能這樣乾淨消掉的函數屈指可數,"
         "$\\cosh$ 是其中最漂亮的一個。<span class='qed'>∎</span></p>",
    guide=["先算 $y=a\\cosh\\dfrac{x}{a}$ 的一階導數:$y'=$ <span class=\"blank\"></span>。",
           "再算二階:$y''=$ <span class=\"blank\"></span>。",
           "計算 $\\sqrt{1+(y')^{2}}=\\sqrt{1+\\sinh^{2}\\frac{x}{a}}$,用招牌恆等式化簡得 "
           "<span class=\"blank\"></span>。根號消失了!",
           "比較 $y''$ 和 $\\dfrac{1}{a}\\sqrt{1+(y')^{2}}$,兩者相等嗎?"],
    demo="Verify that $y=a\\cosh\\dfrac{x}{a}$ satisfies the catenary equation "
         "$y''=\\dfrac{1}{a}\\sqrt{1+(y')^{2}}$.",
    demo_sol="<p>逐階微分:</p>"
             "$$y'=\\sinh\\frac{x}{a},\\qquad y''=\\frac{1}{a}\\cosh\\frac{x}{a}.$$"
             "<p>再算右式,用 $1+\\sinh^{2}t=\\cosh^{2}t$:</p>"
             "$$\\frac{1}{a}\\sqrt{1+\\sinh^{2}\\frac{x}{a}}"
             "=\\frac{1}{a}\\sqrt{\\cosh^{2}\\frac{x}{a}}=\\frac{1}{a}\\cosh\\frac{x}{a}.$$"
             "<p>兩邊相同,故 $y=a\\cosh\\frac{x}{a}$ 確為該微分方程的解。"
             "($\\cosh&gt;0$,開根號不必加絕對值。)$\\;\\blacksquare$</p>",
    demo_hint="兩階導數都算出來,再把恆等式套進根號裡——根號會整個消失。",
    misstep="$\\sqrt{\\cosh^{2}t}$ 寫成 $|\\cosh t|$ 後就停住。$\\cosh t\\ge1&gt;0$,絕對值可以直接拿掉。",
    level="mid",
    drills=[
        ("Compute the arc-length integrand $\\sqrt{1+(y')^{2}}$ for $y=\\cosh x$.",
         "<p>$y'=\\sinh x$,故 $\\sqrt{1+\\sinh^{2}x}=\\cosh x$。根號消失——"
         "這讓 $\\cosh$ 的弧長積分特別好算(W11 會用到)。</p>"),
        ("Find the minimum value of $y=a\\cosh\\dfrac{x}{a}$ (for $a&gt;0$) and where it occurs.",
         "<p>$y'=\\sinh\\dfrac{x}{a}=0\\Rightarrow x=0$;$y''(0)=\\dfrac1a&gt;0$ 為極小。"
         "最小值 $y(0)=a\\cosh 0=a$。</p>"),
        ("Compare $\\cosh x$ with $1+\\dfrac{x^{2}}{2}$ at $x=1$. Why are a catenary and a "
         "parabola easy to confuse?",
         "<p>$\\cosh 1\\approx1.5431$,$1+\\dfrac12=1.5$,差約 $0.043$。因為 "
         "$\\cosh x=1+\\dfrac{x^{2}}{2}+\\dfrac{x^{4}}{24}+\\cdots$,前兩項就是拋物線,"
         "小 $x$ 時幾乎重合——伽利略就是這樣被騙的。(泰勒展開是下週的主題。)</p>"),
    ])

C9 = Concept(
    title_en="Putting the Inverse Rule to Work", title_zh="反函數公式的綜合應用",
    sub="Mixed practice: chain rule on top of inverse functions",
    idea="Real problems stack the inverse-function derivative with the chain, product and "
         "quotient rules. The strategy never changes: identify the outermost operation first, "
         "then work inwards.",
    deep="<p>這一段沒有新公式,是<strong>把本週所有零件混起來練</strong>。"
         "學生單獨每條都會,湊在一起就亂——所以要練。</p>"
         "<p class='step'><strong>拆解順序</strong>:永遠先問「最外層是什麼運算」。"
         "是乘積?先乘積法則。是合成?先鏈鎖。一層一層剝,不要想一步到位。</p>"
         "<p class='step'><strong>常見組合</strong>:</p>"
         "<ul>"
         "<li>$\\arctan(\\text{某個式子})$ → 鏈鎖,外層 $\\dfrac{1}{1+u^{2}}$</li>"
         "<li>$x\\cdot\\arcsin x$ → 乘積,其中一項要用反三角導數</li>"
         "<li>$\\tanh(\\text{線性})$ → 鏈鎖,這就是神經網路裡每個神經元在做的事</li>"
         "</ul>"
         "<p><strong>接到下週</strong>:$\\arctan$ 的導數 $\\dfrac{1}{1+x^{2}}$ 是個有理函數,"
         "而 W6 的部分分式會告訴我們怎麼把有理函數積回去。今天種下的種子,下個月收成。"
         "<span class='qed'>∎</span></p>",
    guide=["$f(x)=\\arctan(e^{x})$ 的最外層是什麼運算?所以第一步用哪條法則?",
           "外層 $\\arctan$ 的導數是 $\\dfrac{1}{1+u^{2}}$,這裡 $u=$ <span class=\"blank\"></span>。",
           "內層 $e^{x}$ 的導數是 <span class=\"blank\"></span>,把兩者相乘。",
           "換成 $f(x)=\\tanh(2x+1)$ 呢?這個式子在神經網路裡叫什麼?"],
    demo="Differentiate $f(x)=\\arctan\\!\\left(e^{x}\\right)$ and "
         "$g(x)=\\tanh(2x+1)$.",
    demo_sol="<p><strong>第一個</strong>,外層 $\\arctan$、內層 $e^{x}$:</p>"
             "$$f'(x)=\\frac{1}{1+\\left(e^{x}\\right)^{2}}\\cdot e^{x}"
             "=\\frac{e^{x}}{1+e^{2x}}.$$"
             "<p><strong>第二個</strong>,外層 $\\tanh$、內層 $2x+1$:</p>"
             "$$g'(x)=\\operatorname{sech}^{2}(2x+1)\\cdot 2=2\\left(1-\\tanh^{2}(2x+1)\\right).$$"
             "<p>第二式就是神經網路裡一個神經元的反向傳播:"
             "<code>權重 × (1 - a**2)</code>,其中 $a$ 是這個神經元的輸出。</p>",
    demo_hint="兩題都是合成。先認出外層是誰,寫下它的導數,再乘內層導數。",
    misstep="鏈鎖只做了一半——寫出外層導數就收工,忘了乘內層。這是本週失分第一名。",
    level="hard",
    drills=[
        ("Differentiate $f(x)=\\arcsin\\!\\left(x^{2}\\right)$.",
         "<p>$\\dfrac{1}{\\sqrt{1-x^{4}}}\\cdot 2x=\\dfrac{2x}{\\sqrt{1-x^{4}}}$。</p>"),
        ("Differentiate $f(x)=\\cosh\\!\\left(x^{2}\\right)$.",
         "<p>$\\sinh\\!\\left(x^{2}\\right)\\cdot 2x=2x\\sinh\\!\\left(x^{2}\\right)$。</p>"),
        ("Differentiate $f(x)=\\dfrac{\\arctan x}{x}$ for $x\\ne0$.",
         "<p>商法則:$\\dfrac{\\frac{x}{1+x^{2}}-\\arctan x}{x^{2}}$。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜反函數的導數:不解 f⁻¹ 也能算",
    intro="觀念 2 說「不必求出 $f^{-1}$ 的公式」。這格用數值方法驗證這句話是真的。",
    code="""from scipy.optimize import brentq

f  = lambda x: x**3 + x          # 嚴格遞增 → 一對一
df = lambda x: 3*x**2 + 1

def f_inv(y, lo=-10, hi=10):
    \"\"\"數值解 f(x) = y,不用任何解析公式\"\"\"
    return brentq(lambda x: f(x) - y, lo, hi)

for b in [2.0, 10.0, -4.0]:
    a = f_inv(b)
    by_formula = 1 / df(a)                       # 反函數公式
    h = 1e-6
    numeric = (f_inv(b + h) - f_inv(b - h)) / (2*h)   # 直接對 f_inv 數值微分
    print(f"b={b:6.1f}  a=f^-1(b)={a: .6f}   1/f'(a)={by_formula:.8f}   "
          f"數值微分={numeric:.8f}   差={abs(by_formula-numeric):.2e}")

# 圖:f 與 f^-1 對稱於 y = x
xs = np.linspace(-2, 2, 300)
ys = f(xs)
plt.plot(xs, ys, label='f(x) = x^3 + x')
plt.plot(ys, xs, label='f inverse')
plt.plot(xs, xs, 'k:', lw=1, label='y = x')
plt.xlim(-4, 4); plt.ylim(-4, 4); plt.gca().set_aspect('equal')
plt.legend(); plt.title('A function and its inverse mirror across y = x')
plt.show()""",
    expected="b=   2.0  a=f^-1(b)= 1.000000   1/f'(a)=0.25000000   數值微分=0.25000000   差=1.11e-11",
    seealso="三個測試點的「公式值」與「直接對 $f^{-1}$ 數值微分」吻合到小數第 10 位以上。"
            "圖上兩條曲線沿 $y=x$ 完全對稱。",
    todo="""# TODO 學生練習:把 f 換成 x**5 + 2*x + 1(仍嚴格遞增)
# 驗證 (f^-1)'(4) = 1/7。提示:先確認 f(1) = 4""")

LAB2 = Lab(
    title="Lab 2｜雙曲函數:為什麼 tanh 適合當 activation",
    intro="畫出三個雙曲函數,並看 $\\tanh$ 的導數 $1-\\tanh^{2}$ 如何在兩端趨近 0——"
          "這就是深度學習裡「梯度消失」的最小範例。",
    code="""xs = np.linspace(-4, 4, 400)

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(xs, np.sinh(xs), label='sinh')
ax[0].plot(xs, np.cosh(xs), label='cosh')
ax[0].plot(xs, np.tanh(xs), label='tanh')
ax[0].axhline(1, color='gray', ls=':'); ax[0].axhline(-1, color='gray', ls=':')
ax[0].set_ylim(-4, 4); ax[0].legend(); ax[0].set_title('Hyperbolic functions')

a = np.tanh(xs)
ax[1].plot(xs, 1 - a**2, 'C3')
ax[1].set_title("d/dx tanh = 1 - tanh^2  (gradient dies at the ends)")
ax[1].set_xlabel('x')
plt.tight_layout(); plt.show()

print("cosh^2 - sinh^2 (應恆為 1):")
for x in [0.0, 1.0, 5.0, 10.0]:
    print(f"  x={x:5.1f}   {np.cosh(x)**2 - np.sinh(x)**2:.12f}")

print("\\ntanh 的導數在兩端有多小:")
for x in [0.0, 1.0, 3.0, 5.0]:
    print(f"  x={x:5.1f}   1 - tanh^2 = {1 - np.tanh(x)**2:.6e}")""",
    expected="x=  5.0   1 - tanh^2 = 8.244614e-05",
    seealso="$x=5$ 時導數已經只剩 $8\\times10^{-5}$。反向傳播要把梯度一層層乘下去,"
            "幾層之後就幾乎歸零——這就是梯度消失,也是後來 ReLU 取代 tanh 的原因。",
    todo="")

LAB3 = Lab(
    title="Lab 3｜懸鏈線 vs 拋物線:伽利略錯在哪",
    intro="觀念 8 說懸鏈線是 $\\cosh$ 不是拋物線。兩者到底差多少?把它量出來。",
    code="""a = 1.0
xs = np.linspace(-2, 2, 400)
cat  = a * np.cosh(xs / a)          # 懸鏈線
para = 1 + xs**2 / 2                # 同曲率的拋物線(cosh 的前兩項泰勒)

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(xs, cat, label='catenary: cosh(x)')
ax[0].plot(xs, para, '--', label='parabola: 1 + x^2/2')
ax[0].legend(); ax[0].set_title('Nearly identical near 0')

ax[1].semilogy(xs, np.abs(cat - para) + 1e-18)
ax[1].set_title('|difference| grows fast away from 0')
ax[1].set_xlabel('x')
plt.tight_layout(); plt.show()

print(f"{'x':>5}  {'cosh(x)':>12}  {'1+x^2/2':>12}  {'差':>12}")
for x in [0.1, 0.5, 1.0, 2.0, 3.0]:
    c, p = math.cosh(x), 1 + x**2/2
    print(f"{x:5.1f}  {c:12.6f}  {p:12.6f}  {abs(c-p):12.6f}")

# 弧長被積式:根號自動消失
x = sp.Symbol('x', real=True)
y = sp.cosh(x)
integrand = sp.simplify(sp.sqrt(1 + sp.diff(y, x)**2))
print("\\nsqrt(1 + y'^2) =", integrand, "  (根號消掉了)")""",
    expected="  1.0      1.543081      1.500000      0.043081",
    seealso="$x=1$ 時差 $0.043$、$x=3$ 時差到 $5.5$。小範圍內幾乎重合,"
            "難怪伽利略會猜錯——但只要拉遠一點,差距就藏不住了。",
    todo="""# TODO 學生練習:把 a 改成 2 和 0.5,看懸鏈線的形狀怎麼變
# a 是什麼的物理意義?(提示:最低點的高度就是 a)""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="銜接課只教過「正向」微分。這週問一個他們沒想過的問題:"
         "已知 $f$ 的導數,能不能<strong>不解出 $f^{-1}$</strong> 就寫出它的導數?"
         "答案是可以,而且只要沿 $y=x$ 翻一張圖就講得通。",
    fastforward=[
        ("鏈鎖法則、隱函數微分", "銜接課練過", "快轉,但本週會一直用"),
        ("反函數存在的條件(單調 ⟹ 一對一)", "偏新", "中速"),
        ("<strong>反函數微分公式</strong>與其證明", "<strong>全新</strong>", "踩煞車(證明時刻)"),
        ("反三角的值域限制與陷阱題", "全新,最容易錯", "踩煞車"),
        ("反三角的導數(三條)", "全新,但可當場推出來", "中速,推一次勝過背十次"),
        ("雙曲函數與其導數", "全新,但定義簡單", "中速"),
        ("反雙曲函數的顯式對數公式", "最難的一塊", "示範一次,不強求"),
        ("懸鏈線應用", "全新,故事性強", "輕鬆帶,當收尾"),
    ],
    outcomes=[
        "說明為什麼「$f'&gt;0$ 恆成立」就保證反函數存在。",
        "背後不看筆記,把 $\\left(f^{-1}\\right)'(b)=\\dfrac{1}{f'(a)}$ 從 "
        "$f\\!\\left(f^{-1}(x)\\right)=x$ 推出來,並說出三個前提。",
        "正確處理 $\\arcsin(\\sin\\theta)$ 這類值域陷阱題。",
        "當場推導 $\\dfrac{d}{dx}\\arcsin x$ 與 $\\dfrac{d}{dx}\\arctan x$,而不是背。",
        "說出 $\\tanh'=1-\\tanh^{2}$,並解釋它和神經網路 <code>1 - A**2</code> 那行程式的關係。",
    ],
    clock=[
        ("00:00–00:10", "回顧上週證明時刻,收作業", "—"),
        ("00:10–00:30", "反函數:存在條件與 $y=x$ 對稱", "觀念 1"),
        ("00:30–01:05", "<strong>證明時刻</strong>:反函數微分公式", "觀念 2"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:35", "反三角的值域限制與陷阱題", "觀念 3"),
        ("01:35–02:05", "當場推導三條反三角導數", "觀念 4"),
        ("02:05–02:10", "休息", "—"),
        ("02:10–02:35", "雙曲函數與其導數(接到 tanh activation)", "觀念 5–6"),
        ("02:35–02:50", "反雙曲的顯式公式(示範,不強求)", "觀念 7"),
        ("02:50–03:00", "懸鏈線故事 + 綜合練習", "觀念 8–9"),
    ],
    proof_moment="從 $f\\!\\left(f^{-1}(x)\\right)=x$ 兩邊微分,用鏈鎖法則推出 "
                 "$\\left(f^{-1}\\right)'(x)=\\dfrac{1}{f'\\!\\left(f^{-1}(x)\\right)}$。"
                 "重點在<strong>三個前提</strong>(一對一、可微、$f'\\ne0$)以及 $f'(a)=0$ 時"
                 "為什麼會壞掉——$\\sqrt[3]{x}$ 在原點的鉛直切線就是活教材。",
    script=[
        ("開場:一個解不出來的反函數(10 分)",
         "<p>黑板寫 $f(x)=x^{3}+x$,問:「它的反函數是什麼?」讓學生試著解 $x^{3}+x=y$。"
         "試個一分鐘就會放棄——三次方程的公式解醜到不能看。</p>"
         "<p>然後說:「解不出來沒關係。我還是可以告訴你 $f^{-1}$ 在 $x=2$ 的斜率是 $\\frac14$。」"
         "這個懸念撐起整堂課。</p>"),
        ("反函數存在:單調就夠了(20 分)",
         "<p>水平線檢驗 → 一對一 → 反函數存在。然後把它接到導數:"
         "<strong>$f'&gt;0$ 恆成立 ⟹ 嚴格遞增 ⟹ 一對一</strong>。</p>"
         "<p>畫 $y=x^{3}$ 與 $y=\\sqrt[3]{x}$,沿 $y=x$ 對摺。"
         "這張圖等一下要用來解釋「斜率取倒數」,先讓它留在黑板上。</p>"),
        ("證明時刻:斜率為什麼會翻過來(35 分)",
         "<p><strong>先講圖像</strong>:反射把 $x$ 與 $y$ 對調,「上升/水平」變成「水平/上升」,"
         "所以斜率取倒數。學生點頭之後再上代數。</p>"
         "<p><strong>代數</strong>:$f\\!\\left(f^{-1}(x)\\right)=x$ 兩邊微分,左邊鏈鎖:"
         "$f'\\!\\left(f^{-1}(x)\\right)\\cdot\\left(f^{-1}\\right)'(x)=1$。移項就得到公式。</p>"
         "<p><strong>三個前提各花一分鐘</strong>,特別是 $f'(a)\\ne0$:"
         "問「$f(x)=x^{3}$ 在 $x=0$ 會怎樣?」畫 $\\sqrt[3]{x}$ 在原點的鉛直切線,一目了然。</p>"
         "<p>回到開場的懸念:$f'(1)=4$,所以 $\\left(f^{-1}\\right)'(2)=\\frac14$。"
         "全程沒解過那個三次方程。</p>"),
        ("反三角:值域才是重點(25 分)",
         "<p>先問「$\\sin$ 有反函數嗎?」——沒有,不是一對一。所以要<strong>切一段</strong>。</p>"
         "<p>三個值域寫在黑板右上角,整週不擦。然後直接丟陷阱題:"
         "$\\arcsin\\left(\\sin\\frac{5\\pi}{6}\\right)$。讓他們先寫,大部分人會答 $\\frac{5\\pi}{6}$。"
         "訂正時強調:<strong>先看角在不在值域內</strong>。</p>"),
        ("反三角的導數:推一次勝過背十次(30 分)",
         "<p>令 $y=\\arcsin x$ ⟹ $\\sin y=x$ ⟹ 隱函數微分 ⟹ $y'=\\frac{1}{\\cos y}$ ⟹ 畫三角形換成 $x$。</p>"
         "<p>那個「為什麼取正根」的問題一定要問,因為答案是<strong>值域</strong>——"
         "剛剛講的限制在這裡回收,學生會覺得前面沒白聽。</p>"
         "<p>$\\arctan$ 更快,連三角形都不用畫,用 $\\sec^{2}=1+\\tan^{2}$ 就好。</p>"
         "<p>收尾丟一句:「注意三角函數的反函數,導數是<strong>純代數式</strong>。"
         "這件事在積分的時候會變成大禮物。」</p>"),
        ("雙曲函數:tanh 是從哪來的(25 分)",
         "<p>資工系學生對 $\\tanh$ 有感——銜接課的 capstone 用過它。今天講它的來歷。</p>"
         "<p>定義寫出來,當場驗 $\\cosh^{2}-\\sinh^{2}=1$(展開就好,30 秒)。"
         "強調那個減號:圓 vs 雙曲線。</p>"
         "<p>導數直接微分定義式,重點提醒<strong>沒有負號</strong>。"
         "然後把 $\\tanh'=1-\\tanh^{2}$ 寫大一點,告訴他們:"
         "「銜接課那行 <code>dZ1 = dA1 * (1 - A1**2)</code>,就是這條。」"
         "這一刻通常會有人「喔——」出聲。</p>"),
        ("反雙曲與懸鏈線(25 分)",
         "<p>反雙曲的顯式公式示範一次就好($\\operatorname{arcsinh}$ 那個二次方程很漂亮),"
         "考卷不會考解法,但要知道「它跟反三角不一樣,是解得出來的」。</p>"
         "<p>懸鏈線當收尾故事:伽利略猜拋物線、猜錯了。代入驗證那個微分方程只要兩行,"
         "順便預告:「這叫微分方程,第 14 週開始我們會正式學怎麼解它。」</p>"
         "<p>最後留 5 分鐘做觀念 9 的綜合題,確認鏈鎖沒有做一半。</p>"),
    ],
    myths=[
        "把 $\\left(f^{-1}\\right)'(b)$ 算成 $\\dfrac{1}{f'(b)}$。導數要代在 $a=f^{-1}(b)$。",
        "以為要先解出 $f^{-1}$ 的公式才能算它的導數。",
        "無腦約掉 $\\arcsin(\\sin\\theta)=\\theta$,不檢查 $\\theta$ 在不在值域。",
        "把 $\\dfrac{d}{dx}\\cosh x$ 寫成 $-\\sinh x$(誤套三角的負號)。",
        "反三角/雙曲的鏈鎖只做一半,忘了乘內層導數。",
        "解 $\\operatorname{arcsinh}$ 的二次式時保留負根,忘了 $e^{y}&gt;0$。",
    ],
    exit_check=[
        ("$f(x)=x^{5}+2x+1$,已知 $f(1)=4$。求 $\\left(f^{-1}\\right)'(4)$。",
         "$f'(x)=5x^{4}+2$,$f'(1)=7$,故答案為 $\\dfrac17$。"),
        ("$\\arcsin\\!\\left(\\sin\\dfrac{3\\pi}{4}\\right)=?$",
         "$\\dfrac{3\\pi}{4}$ 不在值域;$\\sin\\dfrac{3\\pi}{4}=\\dfrac{\\sqrt2}{2}$,故答案為 "
         "$\\dfrac{\\pi}{4}$。"),
        ("$\\dfrac{d}{dx}\\tanh x$ 用 $\\tanh$ 自己表示是什麼?這和程式裡哪一行有關?",
         "$1-\\tanh^{2}x$。對應反向傳播的 <code>dA * (1 - A**2)</code>,"
         "算過輸出 $A$ 之後不必重算 $\\tanh$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W2-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "觀念 4 的三題一定要自己推一次,不要背公式。",
        "<strong>預習</strong>:本書第 12 章的「近似」段落——下週要用泰勒多項式,"
        "把函數換成多項式來算。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 x^3+x=2 的實根是 1", "solve(x**3+x-2, x)[0]", "1"),
    ("C1 D2 f'=5x^4+2 恆正", "diff(x**5+2*x+1, x)", "5*x**4+2"),
    ("C2 示範 (f^-1)'(2)=1/f'(1)=1/4", "1/diff(x**3+x, x).subs(x, 1)", "Rational(1,4)"),
    ("C2 D1 (f^-1)'(4)=1/f'(1)=1/7", "1/diff(x**5+2*x+1, x).subs(x, 1)", "Rational(1,7)"),
    ("C3 示範 arcsin(sin(5pi/6))=pi/6", "asin(sin(5*pi/6))", "pi/6"),
    ("C3 示範 arccos(cos(7pi/6))=5pi/6", "acos(cos(7*pi/6))", "5*pi/6"),
    ("C3 D2 arcsin(sin(3pi/4))=pi/4", "asin(sin(3*pi/4))", "pi/4"),
    ("C3 D3 cos(arcsin x)=sqrt(1-x^2)", "simplify(cos(asin(x)) - sqrt(1-x**2))", "0"),
    ("C4 d/dx arcsin x", "diff(asin(x), x)", "1/sqrt(1-x**2)"),
    ("C4 d/dx arctan x", "diff(atan(x), x)", "1/(1+x**2)"),
    ("C4 示範 d/dx arcsin(2x)", "diff(asin(2*x), x)", "2/sqrt(1-4*x**2)"),
    ("C4 D2 d/dx arctan(1/x)", "simplify(diff(atan(1/x), x))", "-1/(1+x**2)"),
    ("C4 D3 d/dx (arcsin+arccos)=0", "simplify(diff(asin(x)+acos(x), x))", "0"),
    ("C5 cosh^2-sinh^2=1", "simplify(cosh(x)**2 - sinh(x)**2)", "1"),
    ("C5 D3 sinh(2x)=2 sinh cosh", "simplify(sinh(2*x) - 2*sinh(x)*cosh(x))", "0"),
    ("C6 d/dx sinh = cosh", "diff(sinh(x), x)", "cosh(x)"),
    ("C6 d/dx cosh = sinh(無負號)", "diff(cosh(x), x)", "sinh(x)"),
    ("C6 d/dx tanh = 1 - tanh^2", "simplify(diff(tanh(x), x) - (1 - tanh(x)**2))", "0"),
    ("C6 D3 y=cosh 滿足 y''=y", "simplify(diff(cosh(x), x, 2) - cosh(x))", "0"),
    ("C7 arcsinh 的顯式對數公式", "simplify(asinh(x).rewrite(log) - log(x + sqrt(x**2+1)))", "0"),
    ("C7 d/dx arcsinh", "simplify(diff(asinh(x), x) - 1/sqrt(x**2+1))", "0"),
    ("C7 D1 d/dx arctanh = 1/(1-x^2)", "simplify(diff(atanh(x), x) - 1/(1-x**2))", "0"),
    ("C8 示範 懸鏈線滿足 y''=(1/a)sqrt(1+y'^2)", "simplify(sqrt(1+sinh(x)**2) - cosh(x))", "0"),
    ("C8 D2 cosh 最小值在 x=0 為 1", "cosh(0)", "1"),
    ("C9 示範 d/dx arctan(e^x)", "simplify(diff(atan(exp(x)), x) - exp(x)/(1+exp(2*x)))", "0"),
    ("C9 D1 d/dx arcsin(x^2)", "simplify(diff(asin(x**2), x) - 2*x/sqrt(1-x**4))", "0"),
]

WEEK = Week(
    num=2,
    title="反函數微分、反三角與雙曲函數",
    subtitle="已知 $f$ 的導數,能不能不解出 $f^{-1}$ 就寫出它的導數?"
             "答案是可以——而且本週所有的反三角、反雙曲公式,全都是同一條規則的特例。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["補完導數工具箱"],
)
