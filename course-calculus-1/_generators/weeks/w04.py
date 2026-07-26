# -*- coding: utf-8 -*-
"""第 4 週｜分部積分

積分技巧第一招。銜接課只教過換元(鏈鎖法則反過來走),
這週補上另一半:乘積法則反過來走。
證明時刻:分部積分公式如何從乘積法則導出。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Integration by Parts", title_zh="分部積分",
    sub="The product rule, integrated back",
    idea="$$\\int u\\,dv=uv-\\int v\\,du.$$ "
         "This is the product rule read backwards. Substitution undoes the chain rule; "
         "integration by parts undoes the product rule. Together they cover most integrals you "
         "will meet.",
    deep="<p><strong>推導只有三行</strong>,而且學生已經會全部零件。從乘積法則出發:</p>"
         "$$\\frac{d}{dx}(uv)=u'v+uv'.$$"
         "<p class='step'>兩邊對 $x$ 積分。左邊由 FTC 直接得 $uv$:</p>"
         "$$uv=\\int u'v\\,dx+\\int uv'\\,dx.$$"
         "<p class='step'>移項:</p>"
         "$$\\int uv'\\,dx=uv-\\int u'v\\,dx,$$"
         "<p>寫成微分形式就是 $\\displaystyle\\int u\\,dv=uv-\\int v\\,du$。$\\;\\blacksquare$</p>"
         "<p><strong>這條公式在做什麼</strong>:它把一個積分<strong>換成另一個積分</strong>。"
         "注意它不保證新的比較好算——選錯 $u$ 和 $dv$,新積分可能比原來更糟。"
         "所以「怎麼選」才是這一週真正的技術(觀念 2)。</p>"
         "<p><strong>兩招的分工</strong>,寫在黑板上讓學生對照:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>技巧</th><th>反過來走的法則</th>"
         "<th>看到什麼形狀就用</th></tr></thead><tbody>"
         "<tr><td>換元 $u$-sub</td><td>鏈鎖法則</td><td>被積式含「某函數 × 它自己的導數」</td></tr>"
         "<tr><td>分部積分</td><td>乘積法則</td><td>被積式是<strong>兩類不同函數的乘積</strong></td></tr>"
         "</tbody></table></div><span class='qed'>∎</span>",
    guide=["把乘積法則 $(uv)'=u'v+uv'$ 兩邊對 $x$ 積分。左邊會變成 <span class=\"blank\"></span>"
           "(用 FTC)。",
           "右邊是兩個積分的和。把其中一個移到左邊,得到 $\\int uv'\\,dx=$ "
           "<span class=\"blank\"></span>。",
           "換元法反過來走的是哪一條微分法則?分部積分呢?",
           "這條公式把「一個積分」換成「另一個積分」。它保證新的比較好算嗎?"],
    demo="Evaluate $\\displaystyle\\int x e^{x}\\,dx$.",
    demo_sol="<p>取 $u=x$、$dv=e^{x}dx$,則 $du=dx$、$v=e^{x}$:</p>"
             "$$\\int xe^{x}\\,dx=xe^{x}-\\int e^{x}\\,dx=xe^{x}-e^{x}+C=(x-1)e^{x}+C.$$"
             "<p><strong>驗算</strong>:$\\dfrac{d}{dx}\\left[(x-1)e^{x}\\right]"
             "=e^{x}+(x-1)e^{x}=xe^{x}$。✓</p>"
             "<p>為什麼取 $u=x$?因為 $x$ 微分一次就變成 $1$——"
             "新積分裡的多項式<strong>降了一次</strong>,問題變簡單了。</p>",
    demo_hint="哪一部分微分之後會變簡單?那部分就當 $u$。",
    misstep="忘記最後的 $+C$;或是套完公式後把 $-\\int v\\,du$ 的<strong>負號</strong>吃掉。",
    level="basic",
    drills=[
        ("Evaluate $\\displaystyle\\int x\\sin x\\,dx$.",
         "<p>$u=x$、$dv=\\sin x\\,dx$ ⟹ $v=-\\cos x$:"
         "$-x\\cos x+\\displaystyle\\int\\cos x\\,dx=-x\\cos x+\\sin x+C$。</p>"),
        ("Evaluate $\\displaystyle\\int x\\ln x\\,dx$.",
         "<p>$u=\\ln x$、$dv=x\\,dx$ ⟹ $v=\\dfrac{x^{2}}{2}$:"
         "$\\dfrac{x^{2}\\ln x}{2}-\\displaystyle\\int\\dfrac{x}{2}dx"
         "=\\dfrac{x^{2}\\ln x}{2}-\\dfrac{x^{2}}{4}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int x\\cos(2x)\\,dx$.",
         "<p>$u=x$、$dv=\\cos(2x)dx$ ⟹ $v=\\dfrac{\\sin 2x}{2}$:"
         "$\\dfrac{x\\sin 2x}{2}-\\displaystyle\\int\\dfrac{\\sin 2x}{2}dx"
         "=\\dfrac{x\\sin 2x}{2}+\\dfrac{\\cos 2x}{4}+C$。</p>"),
    ])

C2 = Concept(
    title_en="Choosing u and dv", title_zh="怎麼選 u 和 dv",
    sub="LIATE: pick u from the earliest category that appears",
    idea="Choose $u$ from the first category present in <strong>LIATE</strong>: "
         "<u>L</u>ogarithmic, <u>I</u>nverse trig, <u>A</u>lgebraic, <u>T</u>rigonometric, "
         "<u>E</u>xponential. Whatever is left becomes $dv$. The rule works because earlier "
         "categories simplify when differentiated.",
    deep="<p>LIATE 不是魔法,是<strong>經驗排序</strong>——把「微分之後會變簡單」的排前面。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>字母</th><th>類型</th>"
         "<th>微分後</th></tr></thead><tbody>"
         "<tr><td>L</td><td>對數 $\\ln x$</td><td>變成 $\\frac1x$,<strong>完全脫離對數</strong></td></tr>"
         "<tr><td>I</td><td>反三角 $\\arctan x$</td><td>變成有理式,脫離反三角</td></tr>"
         "<tr><td>A</td><td>代數 $x^{n}$</td><td>降一次</td></tr>"
         "<tr><td>T</td><td>三角 $\\sin x$</td><td>還是三角(不變好也不變壞)</td></tr>"
         "<tr><td>E</td><td>指數 $e^{x}$</td><td>完全不變</td></tr>"
         "</tbody></table></div>"
         "<p><strong>邏輯很簡單</strong>:$u$ 會被微分,所以選「微分後改善最多」的;"
         "$dv$ 會被積分,所以剩下那個必須<strong>積得出來</strong>。</p>"
         "<p class='step'><strong>兩個判準要同時滿足</strong>:①$u$ 微分後變簡單;"
         "②$dv$ 積得出來。LIATE 只保證①,②要自己檢查。"
         "例如 $\\int x\\ln x\\,dx$,LIATE 說取 $u=\\ln x$——而剩下的 $x\\,dx$ 確實好積,兩個條件都過。</p>"
         "<p><strong>LIATE 不是定律</strong>。它在 $95\\%$ 的課本題目上有效,"
         "但遇到 $\\int x^{3}e^{x^{2}}dx$ 這種就要先換元(令 $t=x^{2}$)再分部。"
         "把它當<strong>預設選擇</strong>,不是不可違逆的規則。<span class='qed'>∎</span></p>",
    guide=["$u$ 會被<strong>微分</strong>,$dv$ 會被<strong>積分</strong>。所以 $u$ 應該選"
           "「微分後變 <span class=\"blank\"></span>」的那個。",
           "$\\ln x$ 微分後變成 <span class=\"blank\"></span>,完全脫離了對數——"
           "所以 L 排第一。",
           "$e^{x}$ 微分後還是 $e^{x}$,毫無改善,所以排 <span class=\"blank\"></span>。",
           "$\\int x^{2}\\ln x\\,dx$:LIATE 說 $u=$ <span class=\"blank\"></span>。"
           "剩下的 $dv$ 積得出來嗎?"],
    demo="Use LIATE to evaluate $\\displaystyle\\int x^{2}\\ln x\\,dx$.",
    demo_sol="<p>被積式含 <strong>L</strong>(對數)與 <strong>A</strong>(代數),L 排前面,"
             "故取 $u=\\ln x$、$dv=x^{2}dx$。則 $du=\\dfrac{dx}{x}$、$v=\\dfrac{x^{3}}{3}$:</p>"
             "$$\\int x^{2}\\ln x\\,dx=\\frac{x^{3}\\ln x}{3}-\\int\\frac{x^{3}}{3}\\cdot\\frac{dx}{x}"
             "=\\frac{x^{3}\\ln x}{3}-\\frac13\\int x^{2}dx.$$"
             "$$=\\frac{x^{3}\\ln x}{3}-\\frac{x^{3}}{9}+C=\\frac{x^{3}(3\\ln x-1)}{9}+C.$$"
             "<p>如果反過來選 $u=x^{2}$、$dv=\\ln x\\,dx$,你會先卡在「$\\ln x$ 怎麼積」——"
             "那本身就要用一次分部。選錯不是算不出來,是繞遠路。</p>",
    demo_hint="LIATE 裡哪個字母先出現?那個就是 $u$。",
    misstep="選了一個 $dv$ 卻積不出來。LIATE 只保證 $u$ 選得好,$dv$ 能不能積要自己確認。",
    level="mid",
    drills=[
        ("Which should be $u$ in $\\displaystyle\\int x\\arctan x\\,dx$? Then evaluate it.",
         "<p>I 比 A 前面,故 $u=\\arctan x$、$dv=x\\,dx$。"
         "$=\\dfrac{x^{2}\\arctan x}{2}-\\dfrac12\\displaystyle\\int\\dfrac{x^{2}}{1+x^{2}}dx"
         "=\\dfrac{x^{2}\\arctan x}{2}-\\dfrac{x}{2}+\\dfrac{\\arctan x}{2}+C$。"
         "(中間用了 $\\dfrac{x^{2}}{1+x^{2}}=1-\\dfrac{1}{1+x^{2}}$。)</p>"),
        ("Evaluate $\\displaystyle\\int x e^{-x}\\,dx$.",
         "<p>A 比 E 前面,$u=x$、$dv=e^{-x}dx$ ⟹ $v=-e^{-x}$:"
         "$-xe^{-x}+\\displaystyle\\int e^{-x}dx=-xe^{-x}-e^{-x}+C=-(x+1)e^{-x}+C$。</p>"),
        ("Why does LIATE suggest $u=\\ln x$ rather than $u=x$ in "
         "$\\displaystyle\\int x\\ln x\\,dx$?",
         "<p>因為 $\\ln x$ 微分後變成 $\\dfrac1x$,<strong>完全脫離對數</strong>,改善最大;"
         "而 $x$ 微分只降一次。另外若取 $dv=\\ln x\\,dx$,還得先會積 $\\ln x$,反而更麻煩。</p>"),
    ])

C3 = Concept(
    title_en="Integrating ln and Inverse Trig", title_zh="對數與反三角的積分",
    sub="Take dv = dx — the trick is that there is nothing else to take",
    idea="For a lone $\\ln x$ or $\\arctan x$, write the integrand as "
         "$(\\ln x)\\cdot 1$ and take $u=\\ln x$, $dv=dx$. Differentiating $u$ removes the "
         "transcendental function entirely, leaving an algebraic integral.",
    deep="<p>這是分部積分最漂亮的用法之一,因為<strong>看起來根本沒有乘積</strong>。</p>"
         "<p class='step'>訣竅:把 $\\ln x$ 看成 $\\ln x\\cdot 1$,取 $dv=1\\,dx$,故 $v=x$。</p>"
         "$$\\int\\ln x\\,dx=x\\ln x-\\int x\\cdot\\frac1x\\,dx=x\\ln x-x+C.$$"
         "<p><strong>為什麼有效</strong>:$\\ln x$ 微分後是 $\\frac1x$,和 $v=x$ 相乘剛好抵消成 $1$。"
         "這種「乘完剛好消掉」是 LIATE 把 L 排第一的實質原因。</p>"
         "<p class='step'>$\\arctan$ 同理:</p>"
         "$$\\int\\arctan x\\,dx=x\\arctan x-\\int\\frac{x}{1+x^{2}}dx"
         "=x\\arctan x-\\frac12\\ln(1+x^{2})+C,$$"
         "<p>後面那個積分用換元 $t=1+x^{2}$ 就好。</p>"
         "<p>驗算習慣要養成:$\\dfrac{d}{dx}(x\\ln x-x)=\\ln x+1-1=\\ln x$ ✓。"
         "積分的好處就是<strong>答案可以自己驗</strong>,微分回去就知道對不對。"
         "考卷上多花 20 秒驗算,勝過檢查三遍。<span class='qed'>∎</span></p>",
    guide=["$\\int\\ln x\\,dx$ 看起來沒有乘積,怎麼用分部?"
           "(提示:把它寫成 $\\ln x\\times$ <span class=\"blank\"></span>)",
           "取 $u=\\ln x$、$dv=dx$,則 $du=$ <span class=\"blank\"></span>、$v=$ "
           "<span class=\"blank\"></span>。",
           "代進公式:$x\\ln x-\\int x\\cdot\\dfrac1x\\,dx$。剩下的積分是 "
           "<span class=\"blank\"></span>,超好算。",
           "驗算:把答案微分回去,得到 $\\ln x$ 了嗎?"],
    demo="Evaluate $\\displaystyle\\int\\ln x\\,dx$ and $\\displaystyle\\int\\arctan x\\,dx$.",
    demo_sol="<p><strong>對數</strong>:$u=\\ln x$、$dv=dx$ ⟹ $du=\\frac{dx}{x}$、$v=x$:</p>"
             "$$\\int\\ln x\\,dx=x\\ln x-\\int x\\cdot\\frac1x\\,dx=x\\ln x-x+C.$$"
             "<p><strong>反正切</strong>:$u=\\arctan x$、$dv=dx$ ⟹ "
             "$du=\\dfrac{dx}{1+x^{2}}$、$v=x$:</p>"
             "$$\\int\\arctan x\\,dx=x\\arctan x-\\int\\frac{x\\,dx}{1+x^{2}}"
             "=x\\arctan x-\\frac12\\ln\\left(1+x^{2}\\right)+C.$$"
             "<p>(第二個積分令 $t=1+x^{2}$,$dt=2x\\,dx$。)</p>",
    demo_hint="把單獨的函數寫成「它 × 1」,取 $dv=1\\,dx$。",
    misstep="$\\int\\ln x\\,dx$ 答成 $\\dfrac1x$ 或 $\\dfrac{(\\ln x)^{2}}{2}$。"
            "前者是微分、後者是把 $\\ln x$ 當成 $u$ 在做換元——都不對。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int\\arcsin x\\,dx$.",
         "<p>$u=\\arcsin x$、$dv=dx$:$x\\arcsin x-\\displaystyle\\int\\dfrac{x\\,dx}"
         "{\\sqrt{1-x^{2}}}=x\\arcsin x+\\sqrt{1-x^{2}}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int_{1}^{e}\\ln x\\,dx$.",
         "<p>$\\Big[x\\ln x-x\\Big]_{1}^{e}=(e-e)-(0-1)=1$。</p>"),
        ("Evaluate $\\displaystyle\\int\\ln(2x)\\,dx$.",
         "<p>$\\ln(2x)=\\ln 2+\\ln x$,故積分為 $x\\ln 2+x\\ln x-x+C=x\\ln(2x)-x+C$。</p>"),
    ])

C4 = Concept(
    title_en="Repeated Integration by Parts", title_zh="重複分部積分",
    sub="Each pass drops the polynomial degree by one — repeat until it vanishes",
    idea="When the algebraic factor has degree $n$, applying integration by parts $n$ times "
         "reduces it to degree $0$ and the integral closes. The tabular layout keeps the "
         "bookkeeping (and the alternating signs) under control.",
    deep="<p>$\\int x^{2}e^{x}dx$ 做一次分部會剩 $\\int 2xe^{x}dx$——還是同一型,但<strong>次數降了</strong>。"
         "再做一次就結束。</p>"
         "<p class='step'><strong>表格法</strong>(考試救命技)。左欄反覆微分 $u$ 直到 $0$,"
         "右欄反覆積分 $dv$,再<strong>斜向相乘、正負交錯</strong>相加:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>符號</th><th>微分:$u$</th>"
         "<th>積分:$dv$</th></tr></thead><tbody>"
         "<tr><td>$+$</td><td>$x^{2}$</td><td>$e^{x}$</td></tr>"
         "<tr><td>$-$</td><td>$2x$</td><td>$e^{x}$</td></tr>"
         "<tr><td>$+$</td><td>$2$</td><td>$e^{x}$</td></tr>"
         "<tr><td></td><td>$0$</td><td>$e^{x}$</td></tr>"
         "</tbody></table></div>"
         "<p>斜著相乘:$+x^{2}e^{x}-2xe^{x}+2e^{x}$,即 $(x^{2}-2x+2)e^{x}+C$。"
         "<strong>三次分部,三十秒解決</strong>,而且不會漏負號。</p>"
         "<p><strong>什麼時候能用表格法</strong>:$u$ 反覆微分後會<strong>歸零</strong>"
         "(也就是 $u$ 是多項式)。若 $u$ 微分不會歸零(如 $e^{x}\\sin x$),"
         "表格會無限延伸——那時要改用觀念 5 的迴力鏢技巧。<span class='qed'>∎</span></p>",
    guide=["$\\int x^{2}e^{x}dx$ 做一次分部後,新的積分是 <span class=\"blank\"></span>。"
           "它和原式比,什麼變了?",
           "再做一次會剩什麼?第三次呢?什麼時候會停?",
           "表格法:左欄一直微分 $x^{2}$ 得 $x^{2},2x,2,$ <span class=\"blank\"></span>;"
           "右欄一直積分 $e^{x}$ 得 $e^{x},e^{x},e^{x}$。",
           "斜向相乘、符號 $+,-,+$ 交錯相加,得到 <span class=\"blank\"></span>。"],
    demo="Evaluate $\\displaystyle\\int x^{2}e^{x}\\,dx$ using the tabular method.",
    demo_sol="<p>左欄微分 $x^{2}$ 到 $0$,右欄積分 $e^{x}$,斜向相乘、正負交錯:</p>"
             "$$+\\,x^{2}\\cdot e^{x}\\ \\ -\\ \\ 2x\\cdot e^{x}\\ \\ +\\ \\ 2\\cdot e^{x}.$$"
             "$$\\int x^{2}e^{x}\\,dx=\\left(x^{2}-2x+2\\right)e^{x}+C.$$"
             "<p><strong>驗算</strong>:$\\dfrac{d}{dx}\\left[(x^{2}-2x+2)e^{x}\\right]"
             "=(2x-2)e^{x}+(x^{2}-2x+2)e^{x}=x^{2}e^{x}$ ✓</p>",
    demo_hint="用表格:左欄一直微分到 0,右欄一直積分,斜著乘、符號交錯。",
    misstep="表格法的符號忘了交錯,全部相加。第一項是 $+$,之後 $-,+,-$ 輪流。",
    level="hard",
    drills=[
        ("Evaluate $\\displaystyle\\int x^{2}\\sin x\\,dx$.",
         "<p>表格:$x^{2},2x,2,0$ 對 $\\sin x,-\\cos x,-\\sin x,\\cos x$。"
         "$-x^{2}\\cos x+2x\\sin x+2\\cos x+C$。</p>"),
        ("Evaluate $\\displaystyle\\int x^{3}e^{x}\\,dx$.",
         "<p>$\\left(x^{3}-3x^{2}+6x-6\\right)e^{x}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int_{0}^{1}x e^{x}\\,dx$.",
         "<p>$\\Big[(x-1)e^{x}\\Big]_{0}^{1}=0-(-1)=1$。</p>"),
    ])

C5 = Concept(
    title_en="The Boomerang Trick", title_zh="迴力鏢技巧",
    sub="When the original integral comes back, solve for it algebraically",
    idea="For $\\int e^{x}\\sin x\\,dx$, two rounds of integration by parts return the original "
         "integral. Call it $I$, and the equation $I=\\text{stuff}-I$ can be solved for $I$ by "
         "algebra — no further integration needed.",
    deep="<p>這是全週最好玩的一招。$e^{x}$ 和 $\\sin x$ 微分都不會變簡單,"
         "所以表格法會無限延伸——但正因為它<strong>循環</strong>,反而有別的出路。</p>"
         "<p class='step'>令 $I=\\displaystyle\\int e^{x}\\sin x\\,dx$。取 $u=\\sin x$、$dv=e^{x}dx$:</p>"
         "$$I=e^{x}\\sin x-\\int e^{x}\\cos x\\,dx.$$"
         "<p class='step'>再對右邊的積分做一次分部($u=\\cos x$、$dv=e^{x}dx$):</p>"
         "$$\\int e^{x}\\cos x\\,dx=e^{x}\\cos x+\\int e^{x}\\sin x\\,dx=e^{x}\\cos x+I.$$"
         "<p class='step'>代回去:</p>"
         "$$I=e^{x}\\sin x-e^{x}\\cos x-I\\ \\Longrightarrow\\ 2I=e^{x}(\\sin x-\\cos x).$$"
         "$$I=\\frac{e^{x}(\\sin x-\\cos x)}{2}+C.$$"
         "<p><strong>兩個關鍵細節</strong>:</p>"
         "<ul>"
         "<li><strong>兩次都要選同一類當 $u$</strong>。第一次選三角、第二次也選三角。"
         "若第二次改選指數,會原地繞回起點,得到 $I=I$ 這種廢話。</li>"
         "<li><strong>$+C$ 最後才加</strong>。移項時 $I$ 是不定積分,常數在最後補上就好。</li>"
         "</ul>"
         "<p>這招的精神值得講:<strong>當工具繞回原點,就把它當方程式解</strong>。"
         "這是數學裡很常見的一種漂亮手法。<span class='qed'>∎</span></p>",
    guide=["$\\int e^{x}\\sin x\\,dx$ 用表格法會怎樣?(左欄微分 $\\sin x$ 會歸零嗎)",
           "令 $I=\\int e^{x}\\sin x\\,dx$,做一次分部(取 $u=\\sin x$),得 "
           "$I=e^{x}\\sin x-\\int$ <span class=\"blank\"></span>。",
           "對新的積分<strong>再做一次</strong>分部(還是取三角當 $u$)。你會看到什麼熟悉的東西回來?",
           "現在式子變成 $I=\\cdots-I$。這是一個關於 $I$ 的 <span class=\"blank\"></span>,"
           "直接解出 $I$ 就好。"],
    demo="Evaluate $\\displaystyle\\int e^{x}\\sin x\\,dx$.",
    demo_sol="<p>令 $I=\\displaystyle\\int e^{x}\\sin x\\,dx$。取 $u=\\sin x$、$dv=e^{x}dx$:</p>"
             "$$I=e^{x}\\sin x-\\int e^{x}\\cos x\\,dx.$$"
             "<p>再對右積分分部,<strong>同樣取三角當 $u$</strong>($u=\\cos x$):</p>"
             "$$\\int e^{x}\\cos x\\,dx=e^{x}\\cos x-\\int e^{x}(-\\sin x)\\,dx"
             "=e^{x}\\cos x+I.$$"
             "<p>代回:$I=e^{x}\\sin x-e^{x}\\cos x-I$,故</p>"
             "$$2I=e^{x}(\\sin x-\\cos x)\\ \\Longrightarrow\\ "
             "I=\\frac{e^{x}(\\sin x-\\cos x)}{2}+C.$$"
             "<p><strong>驗算</strong>:微分右式得 "
             "$\\dfrac{e^{x}(\\sin x-\\cos x)+e^{x}(\\cos x+\\sin x)}{2}=e^{x}\\sin x$ ✓</p>",
    demo_hint="做兩次分部,原積分會自己回來。把它當未知數解方程式。",
    misstep="第二次分部選了<strong>另一類</strong>當 $u$,結果繞回 $I=I$。兩次要選同一類。",
    level="hard",
    drills=[
        ("Evaluate $\\displaystyle\\int e^{x}\\cos x\\,dx$.",
         "<p>同樣手法:$I=\\dfrac{e^{x}(\\sin x+\\cos x)}{2}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int e^{2x}\\sin x\\,dx$.",
         "<p>兩次分部得 $I=\\dfrac{e^{2x}(2\\sin x-\\cos x)}{5}+C$。"
         "(係數 $5=2^{2}+1$——一般地 $\\int e^{ax}\\sin bx\\,dx$ 的分母是 $a^{2}+b^{2}$。)</p>"),
        ("In the boomerang trick, what goes wrong if the second application of parts chooses the "
         "other factor as $u$?",
         "<p>會把第一次的動作反過來做,回到原式,得到恆等式 $I=I$,毫無資訊。"
         "兩次必須選同一類函數當 $u$。</p>"),
    ])

C6 = Concept(
    title_en="Reduction Formulas", title_zh="遞迴公式",
    sub="One round of parts, written once, valid for every n",
    idea="Integration by parts applied to $\\int x^{n}e^{x}dx$ or $\\int\\sin^{n}x\\,dx$ produces "
         "the same integral with $n$ lowered. Writing that relation once gives a "
         "<em>reduction formula</em> you can iterate mechanically.",
    deep="<p>觀念 4 對 $n=2,3$ 手動做了幾次。與其每次重做,不如<strong>做一次、記下關係式</strong>。</p>"
         "<p class='step'>$I_{n}=\\displaystyle\\int x^{n}e^{x}dx$,取 $u=x^{n}$、$dv=e^{x}dx$:</p>"
         "$$I_{n}=x^{n}e^{x}-n\\int x^{n-1}e^{x}dx=x^{n}e^{x}-n\\,I_{n-1}.$$"
         "<p>配上 $I_{0}=\\displaystyle\\int e^{x}dx=e^{x}$,就能機械式往下算:</p>"
         "$$I_{1}=xe^{x}-e^{x},\\quad I_{2}=x^{2}e^{x}-2I_{1}=(x^{2}-2x+2)e^{x},\\ \\dots$$"
         "<p class='step'><strong>三角版</strong>(考卷常客),對 "
         "$J_{n}=\\displaystyle\\int\\sin^{n}x\\,dx$ 取 $u=\\sin^{n-1}x$、$dv=\\sin x\\,dx$,"
         "再用 $\\cos^{2}=1-\\sin^{2}$ 整理:</p>"
         "$$J_{n}=-\\frac{\\sin^{n-1}x\\cos x}{n}+\\frac{n-1}{n}J_{n-2}.$$"
         "<p>注意它是<strong>降兩階</strong>,所以奇數 $n$ 收到 $J_{1}$、偶數收到 $J_{0}$。</p>"
         "<p><strong>為什麼資工系該喜歡遞迴公式</strong>:這就是<strong>遞迴函式</strong>——"
         "有 base case($I_{0}$)、有遞迴關係($I_{n}=\\cdots I_{n-1}$)。"
         "實作課會把它寫成三行 Python,和數學式一模一樣。<span class='qed'>∎</span></p>",
    guide=["對 $I_{n}=\\int x^{n}e^{x}dx$ 做一次分部,取 $u=x^{n}$,新的積分裡多項式的次數是 "
           "<span class=\"blank\"></span>。",
           "所以 $I_{n}=x^{n}e^{x}-$ <span class=\"blank\"></span>$\\cdot I_{n-1}$。",
           "base case 是 $I_{0}=$ <span class=\"blank\"></span>。",
           "這個結構(base case + 遞迴關係)你在程式課學過嗎?叫什麼?"],
    demo="Derive the reduction formula for $I_{n}=\\displaystyle\\int x^{n}e^{x}\\,dx$ and use it "
         "to compute $I_{3}$.",
    demo_sol="<p><strong>推導</strong>:取 $u=x^{n}$、$dv=e^{x}dx$,則 $du=nx^{n-1}dx$、$v=e^{x}$:</p>"
             "$$I_{n}=x^{n}e^{x}-n\\int x^{n-1}e^{x}dx=x^{n}e^{x}-n\\,I_{n-1}.$$"
             "<p><strong>迭代</strong>,由 $I_{0}=e^{x}$ 開始:</p>"
             "$$I_{1}=xe^{x}-1\\cdot e^{x}=(x-1)e^{x},$$"
             "$$I_{2}=x^{2}e^{x}-2(x-1)e^{x}=\\left(x^{2}-2x+2\\right)e^{x},$$"
             "$$I_{3}=x^{3}e^{x}-3\\left(x^{2}-2x+2\\right)e^{x}"
             "=\\left(x^{3}-3x^{2}+6x-6\\right)e^{x}+C.$$"
             "<p>和觀念 4 用表格法算的完全一致。</p>",
    demo_hint="做一次分部,把結果寫成「$I_{n}$ 和 $I_{n-1}$ 的關係」。",
    misstep="遞迴關係的係數 $n$ 漏掉。$\\dfrac{d}{dx}x^{n}=nx^{n-1}$,那個 $n$ 要帶進去。",
    level="hard",
    drills=[
        ("Use the reduction formula to compute $I_{2}=\\displaystyle\\int x^{2}e^{x}dx$ from "
         "$I_{1}$.",
         "<p>$I_{2}=x^{2}e^{x}-2I_{1}=x^{2}e^{x}-2(x-1)e^{x}=(x^{2}-2x+2)e^{x}+C$。</p>"),
        ("Given $J_{n}=-\\dfrac{\\sin^{n-1}x\\cos x}{n}+\\dfrac{n-1}{n}J_{n-2}$ and "
         "$J_{0}=x$, compute $J_{2}=\\displaystyle\\int\\sin^{2}x\\,dx$.",
         "<p>$J_{2}=-\\dfrac{\\sin x\\cos x}{2}+\\dfrac12 x+C=\\dfrac{x}{2}-\\dfrac{\\sin 2x}{4}+C$"
         "(用了 $2\\sin x\\cos x=\\sin 2x$)。</p>"),
        ("Why does the reduction formula for $\\int\\sin^{n}x\\,dx$ drop $n$ by two rather than "
         "one?",
         "<p>因為分部後會出現 $\\cos^{2}x$,用 $\\cos^{2}=1-\\sin^{2}$ 換掉時,"
         "產生的是 $\\sin^{n-2}$ 與 $\\sin^{n}$,整理後降的是兩階。</p>"),
    ])

C7 = Concept(
    title_en="Definite Integrals by Parts", title_zh="定積分的分部積分",
    sub="Evaluate the uv term at both endpoints as you go — do not save it for the end",
    idea="$$\\int_{a}^{b}u\\,dv=\\Big[uv\\Big]_{a}^{b}-\\int_{a}^{b}v\\,du.$$ "
         "Substituting the limits into $uv$ immediately often simplifies the remaining work — "
         "sometimes the boundary term vanishes entirely.",
    deep="<p>公式和不定版一樣,只是 $uv$ 那項<strong>當場代上下限</strong>。"
         "很多學生習慣「先算不定積分,最後才代」——那樣做不是錯,但常常白算一堆。</p>"
         "<p class='step'><strong>邊界項消失是常態</strong>。例如 "
         "$\\displaystyle\\int_{0}^{\\pi}x\\sin x\\,dx$:</p>"
         "$$\\Big[-x\\cos x\\Big]_{0}^{\\pi}+\\int_{0}^{\\pi}\\cos x\\,dx"
         "=\\pi+\\Big[\\sin x\\Big]_{0}^{\\pi}=\\pi+0=\\pi.$$"
         "<p>第二項整個是零。若先算不定積分再代,你會多寫兩行才發現。</p>"
         "<p><strong>常見錯誤</strong>:只把上下限代到 $uv$,忘了後面的積分<strong>也是定積分</strong>;"
         "或反過來,把 $uv$ 留成不定形式卻對後面的積分代了限。"
         "寫的時候兩邊都標上 $a,b$,不要偷懶。</p>"
         "<p><strong>一個漂亮的結果</strong>:$\\displaystyle\\int_{0}^{1}x^{n}e^{x}dx$ 的邊界項是 "
         "$e-0=e$,遞迴下去可以得到 $n!$ 的組合恆等式——這是 Gamma 函數的入口,"
         "本課不深入,但值得提一句。<span class='qed'>∎</span></p>",
    guide=["定積分版的公式和不定版差在哪裡?($uv$ 那一項要怎麼處理)",
           "算 $\\int_{0}^{\\pi}x\\sin x\\,dx$:取 $u=x$、$dv=\\sin x\\,dx$,則 $v=$ "
           "<span class=\"blank\"></span>。",
           "$\\Big[-x\\cos x\\Big]_{0}^{\\pi}=$ <span class=\"blank\"></span>"
           "(記得 $\\cos\\pi=-1$)。",
           "剩下的 $\\int_{0}^{\\pi}\\cos x\\,dx$ 等於多少?整題答案是?"],
    demo="Evaluate $\\displaystyle\\int_{0}^{\\pi}x\\sin x\\,dx$.",
    demo_sol="<p>取 $u=x$、$dv=\\sin x\\,dx$ ⟹ $du=dx$、$v=-\\cos x$:</p>"
             "$$\\int_{0}^{\\pi}x\\sin x\\,dx=\\Big[-x\\cos x\\Big]_{0}^{\\pi}"
             "+\\int_{0}^{\\pi}\\cos x\\,dx.$$"
             "<p>邊界項:$-\\pi\\cos\\pi-0=-\\pi(-1)=\\pi$。"
             "剩下的積分:$\\Big[\\sin x\\Big]_{0}^{\\pi}=0-0=0$。故</p>"
             "$$\\int_{0}^{\\pi}x\\sin x\\,dx=\\pi.$$"
             "<p>幾何意義:$x\\sin x$ 在 $[0,\\pi]$ 上全部非負,曲線下面積恰為 $\\pi$。</p>",
    demo_hint="邊界項當場代上下限,剩下的積分也記得帶著上下限。",
    misstep="$uv$ 項代了上下限,但後面的 $\\int v\\,du$ 忘了代,或反之。兩邊都要標。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int_{0}^{1}x e^{2x}\\,dx$.",
         "<p>$u=x$、$v=\\dfrac{e^{2x}}{2}$:$\\Big[\\dfrac{xe^{2x}}{2}\\Big]_{0}^{1}"
         "-\\dfrac12\\displaystyle\\int_{0}^{1}e^{2x}dx=\\dfrac{e^{2}}{2}"
         "-\\dfrac{e^{2}-1}{4}=\\dfrac{e^{2}+1}{4}$。</p>"),
        ("Evaluate $\\displaystyle\\int_{1}^{2}\\ln x\\,dx$.",
         "<p>$\\Big[x\\ln x-x\\Big]_{1}^{2}=(2\\ln2-2)-(0-1)=2\\ln2-1\\approx0.386$。</p>"),
        ("Evaluate $\\displaystyle\\int_{0}^{\\pi/2}x\\cos x\\,dx$.",
         "<p>$\\Big[x\\sin x\\Big]_{0}^{\\pi/2}-\\displaystyle\\int_{0}^{\\pi/2}\\sin x\\,dx"
         "=\\dfrac{\\pi}{2}-1$。</p>"),
    ])

C8 = Concept(
    title_en="Parts Combined with Substitution", title_zh="分部與換元的合作",
    sub="Sometimes you must substitute first before parts becomes possible",
    idea="Integrals like $\\int x^{3}e^{x^{2}}dx$ resist parts directly, but the substitution "
         "$t=x^{2}$ turns them into a standard parts problem. Reading the integrand for "
         "\"function times its own derivative\" tells you which to try first.",
    deep="<p>本週收尾:<strong>兩招不是二選一,常常要合作</strong>。</p>"
         "<p class='step'>$\\displaystyle\\int x^{3}e^{x^{2}}dx$ 直接分部會很慘——"
         "$e^{x^{2}}$ 積不出來(它的原函數不是初等函數!)。</p>"
         "<p class='step'>但注意 $x^{3}=x^{2}\\cdot x$,而 $x$ 正是 $x^{2}$ 的導數的一半。"
         "令 $t=x^{2}$,$dt=2x\\,dx$:</p>"
         "$$\\int x^{3}e^{x^{2}}dx=\\int x^{2}\\cdot e^{x^{2}}\\cdot x\\,dx"
         "=\\frac12\\int t\\,e^{t}\\,dt.$$"
         "<p>剩下的就是本週第一題!答案 $\\dfrac{(t-1)e^{t}}{2}=\\dfrac{(x^{2}-1)e^{x^{2}}}{2}+C$。</p>"
         "<p><strong>判斷順序的口訣</strong>:</p>"
         "<ol>"
         "<li>先找「某函數 × 它自己的導數」的結構 → 有的話先<strong>換元</strong></li>"
         "<li>換完之後看是不是「兩類函數相乘」 → 是的話再<strong>分部</strong></li>"
         "</ol>"
         "<p><strong>誠實的提醒</strong>:有些積分<strong>沒有初等原函數</strong>,"
         "$\\int e^{x^{2}}dx$、$\\int\\frac{\\sin x}{x}dx$、$\\int\\frac{dx}{\\ln x}$ 都是。"
         "不是你不會算,是真的算不出來(這件事可以被證明)。遇到它們要改用數值方法——W7 的主題。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\int x^{3}e^{x^{2}}dx$ 直接分部,$dv=e^{x^{2}}dx$ 積得出來嗎?",
           "把 $x^{3}$ 拆成 $x^{2}\\cdot x$。注意 $x$ 和 $\\dfrac{d}{dx}x^{2}$ 差幾倍?",
           "令 $t=x^{2}$,整個積分變成 $\\dfrac12\\int$ <span class=\"blank\"></span> $dt$。"
           "這個式子你今天算過嗎?",
           "所以判斷順序是:先找 <span class=\"blank\"></span> 的結構,再看要不要分部。"],
    demo="Evaluate $\\displaystyle\\int x^{3}e^{x^{2}}\\,dx$.",
    demo_sol="<p>先換元。令 $t=x^{2}$,則 $dt=2x\\,dx$,即 $x\\,dx=\\dfrac{dt}{2}$:</p>"
             "$$\\int x^{3}e^{x^{2}}dx=\\int x^{2}e^{x^{2}}\\cdot x\\,dx"
             "=\\frac12\\int t\\,e^{t}\\,dt.$$"
             "<p>再分部(本週第一題):$\\displaystyle\\int te^{t}dt=(t-1)e^{t}$。故</p>"
             "$$\\int x^{3}e^{x^{2}}dx=\\frac{(t-1)e^{t}}{2}+C"
             "=\\frac{\\left(x^{2}-1\\right)e^{x^{2}}}{2}+C.$$"
             "<p><strong>驗算</strong>:微分右式得 "
             "$\\dfrac{2xe^{x^{2}}+(x^{2}-1)\\cdot 2xe^{x^{2}}}{2}=x^{3}e^{x^{2}}$ ✓</p>",
    demo_hint="直接分部會卡在積不出來的東西。先想想有沒有可以換元的結構。",
    misstep="換元後忘了把 $x$ 換回來。不定積分的答案必須用原變數表示。",
    level="hard",
    drills=[
        ("Evaluate $\\displaystyle\\int x\\ln\\left(x^{2}\\right)dx$.",
         "<p>$\\ln(x^{2})=2\\ln|x|$,故 $=2\\displaystyle\\int x\\ln|x|\\,dx"
         "=\\dfrac{x^{2}\\ln(x^{2})}{2}-\\dfrac{x^{2}}{2}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int e^{\\sqrt{x}}\\,dx$.",
         "<p>令 $t=\\sqrt x$,$x=t^{2}$,$dx=2t\\,dt$:$2\\displaystyle\\int te^{t}dt"
         "=2(t-1)e^{t}+C=2\\left(\\sqrt x-1\\right)e^{\\sqrt x}+C$。</p>"),
        ("Explain why $\\displaystyle\\int e^{x^{2}}dx$ cannot be done by parts (or by any "
         "elementary method).",
         "<p>它<strong>沒有初等原函數</strong>——這是 Liouville 定理可證的事實,"
         "不是技巧不夠。遇到這種積分只能用數值方法(W7)或特殊函數(erf)。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜遞迴公式寫成遞迴函式",
    intro="觀念 6 的遞迴公式 $I_n=x^n e^x-n I_{n-1}$ 有 base case、有遞迴關係——"
          "這就是程式課的遞迴。三行寫出來,再和 SymPy 對答案。",
    code="""x = sp.Symbol('x')

def I(n):
    \"\"\"∫ x^n e^x dx —— 遞迴公式的直譯\"\"\"
    if n == 0:
        return sp.exp(x)                    # base case
    return x**n * sp.exp(x) - n * I(n - 1)  # 遞迴關係

print(f"{'n':>3}  {'遞迴公式':>42}  {'SymPy':>42}  一致?")
for n in range(5):
    mine = sp.simplify(sp.expand(I(n)))
    ref  = sp.simplify(sp.integrate(x**n * sp.exp(x), x))
    same = sp.simplify(mine - ref) == 0
    print(f"{n:3d}  {str(sp.factor(mine)):>42}  {str(sp.factor(ref)):>42}  {same}")

# 三角版的遞迴:J_n = -sin^(n-1)x cos x / n + (n-1)/n * J_(n-2)
def J(n):
    if n == 0:
        return x
    if n == 1:
        return -sp.cos(x)
    return -sp.sin(x)**(n-1) * sp.cos(x) / n + sp.Rational(n-1, n) * J(n-2)

print("\\n∫ sin^n x dx:")
for n in range(2, 6):
    mine = sp.simplify(J(n))
    ref  = sp.simplify(sp.integrate(sp.sin(x)**n, x))
    print(f"  n={n}  一致? {sp.simplify(mine - ref) == 0}")""",
    expected="  0                                  exp(x)                                  exp(x)  True",
    seealso="五個 $n$ 值全部與 SymPy 一致。遞迴公式和遞迴函式是同一件事——"
            "base case 對應 $I_0$、遞迴關係對應那一行減法。",
    todo="""# TODO 學生練習:寫出 ∫ x^n sin(x) dx 的遞迴公式並實作
# 提示:要做兩次分部才會降 1 階(會先冒出 cos)""")

LAB2 = Lab(
    title="Lab 2｜哪些積分「算不出來」",
    intro="觀念 8 說某些積分沒有初等原函數。SymPy 遇到它們會怎樣?這格讓你親眼看見界線在哪。",
    code="""x = sp.Symbol('x')

cases = [
    ("x*exp(x)",      x*sp.exp(x)),
    ("exp(x**2)",     sp.exp(x**2)),
    ("sin(x)/x",      sp.sin(x)/x),
    ("exp(-x**2)",    sp.exp(-x**2)),
    ("x*exp(x**2)",   x*sp.exp(x**2)),
    ("1/log(x)",      1/sp.log(x)),
]
for name, f in cases:
    r = sp.integrate(f, x)
    elementary = not r.has(sp.Integral, sp.erf, sp.Si, sp.li, sp.erfi)
    print(f"  ∫ {name:14s} dx = {str(r)[:46]:46s}  初等? {elementary}")

# 算不出原函數,不代表算不出定積分 —— 數值方法照樣可行
from scipy.integrate import quad
val, err = quad(lambda t: math.exp(-t**2), 0, 1)
print(f"\\n∫_0^1 exp(-x^2) dx 數值 = {val:.12f}  (誤差估計 {err:.1e})")
print(f"對照 sympy 的精確值      = {float(sp.integrate(sp.exp(-x**2), (x, 0, 1))):.12f}")""",
    expected="∫_0^1 exp(-x^2) dx 數值 = 0.746824132812  (誤差估計 8.3e-15)",
    seealso="$xe^{x}$、$xe^{x^2}$ 有初等原函數;$e^{x^2}$、$\\frac{\\sin x}{x}$、$\\frac{1}{\\ln x}$ "
            "沒有——SymPy 只能回傳 <code>erfi</code>、<code>Si</code>、<code>li</code> 這些特殊函數。"
            "但注意最後兩行:<strong>算不出原函數,不代表算不出定積分</strong>,"
            "數值方法照樣給你 12 位有效數字。這正是 W7 的主題。",
    todo="")

LABS = [LAB1, LAB2]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="銜接課教的換元是「鏈鎖法則反過來走」。這週補上另一半:"
         "<strong>乘積法則反過來走</strong>。有了這兩招,課本上大部分的積分都能對付。",
    fastforward=[
        ("換元積分(銜接課教過)", "舊功夫", "快轉,但要對照著講"),
        ("<strong>分部積分公式與推導</strong>", "<strong>全新</strong>", "踩煞車(證明時刻)"),
        ("LIATE 選 $u$ 的策略", "全新,但好記", "中速,多練幾題"),
        ("$\\int\\ln x\\,dx$ 這類「看似沒乘積」的題", "全新,學生會驚訝", "中速"),
        ("重複分部與表格法", "全新,考試救命技", "踩煞車,一定要練熟"),
        ("迴力鏢技巧($e^{x}\\sin x$)", "全新,最有趣", "踩煞車"),
        ("遞迴公式", "偏難,但資工系有感(＝遞迴函式)", "中速"),
        ("定積分版本", "只差代上下限", "快轉"),
    ],
    outcomes=[
        "從乘積法則推出分部積分公式。",
        "用 LIATE 選 $u$,並說明<strong>為什麼</strong>是這個順序(微分後改善程度)。",
        "算出 $\\int\\ln x\\,dx$、$\\int\\arctan x\\,dx$ 這類「看不出乘積」的積分。",
        "用<strong>表格法</strong>快速處理 $\\int x^{n}e^{x}dx$、$\\int x^{n}\\sin x\\,dx$。",
        "用<strong>迴力鏢技巧</strong>處理 $\\int e^{x}\\sin x\\,dx$,並解釋為何兩次要選同一類。",
        "積完之後<strong>微分驗算</strong>——這週開始養成習慣。",
    ],
    clock=[
        ("00:00–00:10", "收作業;複習換元是「鏈鎖反走」", "—"),
        ("00:10–00:40", "<strong>證明時刻</strong>:從乘積法則推出分部積分", "觀念 1"),
        ("00:40–01:05", "LIATE:為什麼是這個順序", "觀念 2"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:30", "$\\int\\ln x$、$\\int\\arctan x$:$dv=dx$ 的妙用", "觀念 3"),
        ("01:30–02:00", "重複分部與<strong>表格法</strong>", "觀念 4"),
        ("02:00–02:05", "休息", "—"),
        ("02:05–02:30", "迴力鏢技巧:讓積分自己回來", "觀念 5"),
        ("02:30–02:50", "遞迴公式(＝遞迴函式)", "觀念 6"),
        ("02:50–03:00", "定積分版 + 換元與分部的合作", "觀念 7–8"),
    ],
    proof_moment="從乘積法則 $(uv)'=u'v+uv'$ 兩邊積分,推出 "
                 "$\\int u\\,dv=uv-\\int v\\,du$。只有三行,但要讓學生看清楚:"
                 "<strong>左邊用 FTC 直接得 $uv$</strong>——這是整個推導唯一的技術點,"
                 "也是 FTC 第一次被拿來當工具用。",
    script=[
        ("開場:另外半邊的鏡子(10 分)",
         "<p>黑板上寫兩行:</p>"
         "<p class='step'>鏈鎖法則 $\\xrightarrow{\\text{反過來}}$ 換元積分 ✓(暑假學過)</p>"
         "<p class='step'>乘積法則 $\\xrightarrow{\\text{反過來}}$ ?</p>"
         "<p>「今天就是把這個問號填起來。」這個框架讓學生知道自己在整張地圖的哪裡。</p>"),
        ("證明時刻:三行推導(30 分)",
         "<p>讓學生自己動手:「把 $(uv)'=u'v+uv'$ 兩邊對 $x$ 積分。左邊是什麼?」</p>"
         "<p>大部分人會卡住。提示:「$\\int(uv)'dx$——這不就是 FTC 嗎?」"
         "$\\int F'=F$,所以左邊就是 $uv$。<strong>這一刻要停下來強調</strong>:"
         "FTC 不只是拿來算定積分的,它是「積分與微分互逆」這件事本身。</p>"
         "<p>移項完成。然後<strong>立刻用它算一題</strong>($\\int xe^{x}dx$),"
         "趁熱讓公式落地,並示範微分驗算。</p>"),
        ("LIATE:不是背,是理解(25 分)",
         "<p>先問:「$u$ 會被怎麼樣?$dv$ 會被怎麼樣?」($u$ 被微分、$dv$ 被積分)</p>"
         "<p>「所以 $u$ 該選什麼?」——微分後<strong>改善最多</strong>的。"
         "然後把五類函數各微分一次列在黑板上,順序自己就浮現了。</p>"
         "<p>強調第二個判準:$dv$ <strong>必須積得出來</strong>。LIATE 不管這個,要自己看。</p>"),
        ("看不出乘積的乘積(20 分)",
         "<p>丟 $\\int\\ln x\\,dx$。學生會說「這沒有乘積啊」。</p>"
         "<p>「誰說的?$\\ln x=\\ln x\\times 1$。」取 $dv=1\\,dx$。"
         "算完之後那個 $x\\cdot\\frac1x=1$ 的抵消會讓學生「喔!」一聲。</p>"
         "<p>順手算 $\\int\\arctan x\\,dx$,並示範微分驗算。"
         "<strong>驗算習慣從這週開始要求</strong>:積分的答案永遠可以自己檢查。</p>"),
        ("表格法:考試救命技(30 分)",
         "<p>先手動做 $\\int x^{2}e^{x}dx$ 兩次分部,讓他們感受到「機械但囉唆」。</p>"
         "<p>然後畫表格:左欄微分到 0、右欄積分、斜著乘、符號交錯。"
         "同一題三十秒解決。<strong>這一招他們會用一輩子</strong>,值得多練兩題。</p>"
         "<p>提醒界線:$u$ 微分要能歸零(多項式)才能用表格。$e^{x}\\sin x$ 不行——下一段處理。</p>"),
        ("迴力鏢:當工具繞回原點(25 分)",
         "<p>丟 $\\int e^{x}\\sin x\\,dx$,問「表格法行嗎?」——左欄永遠不歸零。</p>"
         "<p>那就硬做兩次分部。做到第二次時,原積分自己回來了。"
         "<strong>停在這裡</strong>,問:「$I=\\cdots-I$,這是什麼?」</p>"
         "<p>「一個方程式。解它。」這一刻通常會有人笑出來——數學居然可以這樣賴皮。</p>"
         "<p>提醒兩次要選同一類當 $u$,否則會繞回 $I=I$。這是最常見的失敗。</p>"),
        ("遞迴公式與收尾(20 分)",
         "<p>「剛剛表格法對 $n=2,3$ 各做了一次。$n=10$ 呢?」"
         "與其重做,不如寫下 $I_{n}=x^{n}e^{x}-nI_{n-1}$。</p>"
         "<p>指出它的結構:<strong>base case + 遞迴關係</strong>。"
         "「這在程式課叫什麼?」實作課會把它寫成三行 Python。</p>"
         "<p>最後 10 分鐘講定積分版(只差代上下限)與換元+分部的合作,"
         "並誠實告訴他們:<strong>有些積分真的算不出來</strong>($\\int e^{x^{2}}dx$),"
         "那不是能力問題。實作課會看到界線在哪,W7 會給出對策。</p>"),
    ],
    myths=[
        "套完公式後把 $-\\int v\\,du$ 的負號吃掉。",
        "選了積不出來的 $dv$。LIATE 只管 $u$,$dv$ 要自己檢查。",
        "表格法的符號沒有交錯,全部相加。",
        "迴力鏢時第二次分部選了另一類當 $u$,繞回 $I=I$。",
        "$\\int\\ln x\\,dx$ 答成 $\\frac1x$(那是微分)或 $\\frac{(\\ln x)^{2}}{2}$。",
        "定積分版只對 $uv$ 代上下限,忘了後面的積分也要代。",
        "以為所有積分都算得出來。$\\int e^{x^{2}}dx$ 沒有初等原函數,這是定理不是藉口。",
    ],
    exit_check=[
        ("$\\displaystyle\\int x\\cos x\\,dx=?$",
         "$u=x$、$dv=\\cos x\\,dx$:$x\\sin x+\\cos x+C$。"),
        ("$\\displaystyle\\int\\ln x\\,dx=?$ 為什麼可以用分部?",
         "$x\\ln x-x+C$。把 $\\ln x$ 看成 $\\ln x\\times1$,取 $dv=1\\,dx$。"),
        ("$\\displaystyle\\int e^{x}\\sin x\\,dx$ 為什麼不能用表格法?那該用什麼?",
         "因為 $\\sin x$ 反覆微分不會歸零,表格無限延伸。改用迴力鏢:做兩次分部讓原積分回來,"
         "再當方程式解。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W4-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "<strong>每一題都要微分驗算</strong>,這週開始這是硬性要求。",
        "<strong>預習</strong>:本書第 12 章的積分段落——下週處理三角函數的積分與三角代換。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 ∫x e^x dx", "integrate(x*exp(x), x)", "(x-1)*exp(x)"),
    ("C1 D1 ∫x sin x dx", "simplify(integrate(x*sin(x), x) - (-x*cos(x)+sin(x)))", "0"),
    ("C1 D2 ∫x ln x dx", "simplify(integrate(x*log(x), x) - (x**2*log(x)/2 - x**2/4))", "0"),
    ("C1 D3 ∫x cos(2x) dx",
     "simplify(integrate(x*cos(2*x), x) - (x*sin(2*x)/2 + cos(2*x)/4))", "0"),
    ("C2 示範 ∫x^2 ln x dx",
     "simplify(integrate(x**2*log(x), x) - x**3*(3*log(x)-1)/9)", "0"),
    ("C2 D2 ∫x e^(-x) dx", "simplify(integrate(x*exp(-x), x) - (-(x+1)*exp(-x)))", "0"),
    ("C3 示範 ∫ln x dx", "simplify(integrate(log(x), x) - (x*log(x)-x))", "0"),
    ("C3 示範 ∫arctan x dx",
     "simplify(integrate(atan(x), x) - (x*atan(x) - log(1+x**2)/2))", "0"),
    ("C3 D1 ∫arcsin x dx",
     "simplify(integrate(asin(x), x) - (x*asin(x) + sqrt(1-x**2)))", "0"),
    ("C3 D2 ∫_1^e ln x dx", "integrate(log(x), (x, 1, E))", "1"),
    ("C4 示範 ∫x^2 e^x dx",
     "simplify(integrate(x**2*exp(x), x) - (x**2-2*x+2)*exp(x))", "0"),
    ("C4 D1 ∫x^2 sin x dx",
     "simplify(integrate(x**2*sin(x), x) - (-x**2*cos(x)+2*x*sin(x)+2*cos(x)))", "0"),
    ("C4 D2 ∫x^3 e^x dx",
     "simplify(integrate(x**3*exp(x), x) - (x**3-3*x**2+6*x-6)*exp(x))", "0"),
    ("C4 D3 ∫_0^1 x e^x dx", "integrate(x*exp(x), (x, 0, 1))", "1"),
    ("C5 示範 ∫e^x sin x dx",
     "simplify(integrate(exp(x)*sin(x), x) - exp(x)*(sin(x)-cos(x))/2)", "0"),
    ("C5 D1 ∫e^x cos x dx",
     "simplify(integrate(exp(x)*cos(x), x) - exp(x)*(sin(x)+cos(x))/2)", "0"),
    ("C5 D2 ∫e^(2x) sin x dx",
     "simplify(integrate(exp(2*x)*sin(x), x) - exp(2*x)*(2*sin(x)-cos(x))/5)", "0"),
    ("C6 示範 遞迴 I_3", "simplify(integrate(x**3*exp(x), x) - (x**3-3*x**2+6*x-6)*exp(x))", "0"),
    ("C6 D2 J_2 = x/2 - sin(2x)/4",
     "simplify(integrate(sin(x)**2, x) - (x/2 - sin(2*x)/4))", "0"),
    ("C7 示範 ∫_0^pi x sin x dx", "integrate(x*sin(x), (x, 0, pi))", "pi"),
    ("C7 D1 ∫_0^1 x e^(2x) dx", "simplify(integrate(x*exp(2*x), (x, 0, 1)) - (exp(2)+1)/4)", "0"),
    ("C7 D2 ∫_1^2 ln x dx", "simplify(integrate(log(x), (x, 1, 2)) - (2*log(2)-1))", "0"),
    ("C7 D3 ∫_0^(pi/2) x cos x dx",
     "simplify(integrate(x*cos(x), (x, 0, pi/2)) - (pi/2 - 1))", "0"),
    ("C8 示範 ∫x^3 e^(x^2) dx",
     "simplify(integrate(x**3*exp(x**2), x) - (x**2-1)*exp(x**2)/2)", "0"),
    ("C8 D2 ∫e^sqrt(x) dx",
     "simplify(diff(2*(sqrt(x)-1)*exp(sqrt(x)), x) - exp(sqrt(x)))", "0"),
]

WEEK = Week(
    num=4,
    title="分部積分",
    subtitle="換元是鏈鎖法則反過來走,分部是<strong>乘積法則反過來走</strong>。"
             "有了這兩招,課本上大部分的積分都對付得了——但也會第一次遇到「真的算不出來」的積分。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["積分技巧 I"],
)
