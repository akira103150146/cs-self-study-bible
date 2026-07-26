# -*- coding: utf-8 -*-
"""第 1 週｜極限的嚴格定義與浮點數現實

銜接課已把「怎麼算極限」練成反射。這一週不重教計算,做兩件銜接課沒空做的事:
把「越來越靠近」翻譯成 ε-δ 的精確語言,以及揭穿「電腦算不出真正的極限」。
證明時刻:用 ε-δ 證 lim(3x-1)=5(由 ε 反推 δ 的完整書寫格式)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

# ---------------------------------------------------------------- 觀念

C1 = Concept(
    title_en="Diagnostic Review", title_zh="銜接課回顧",
    sub="Read the form first — the form tells you which move to use",
    idea="Before anything new, re-run the decision tree from the bridge course: read the "
         "<em>form</em> of the limit first. Direct substitution → factoring → rationalization → "
         "compare leading degrees → conjugate for $\\infty-\\infty$. The form picks the move, "
         "not the other way round.",
    deep="<p>這一段是<strong>診斷</strong>,不是複習講解。先發下五題快測(15 分鐘),收回來當場檢討,"
         "你才知道這班的底子落在哪裡——後面十七週的配速全靠這一次校準。</p>"
         "<p class='step'>決策樹:代入 → $\\frac00$ 就找共同因式 → 卡根號就乘共軛 → "
         "$x\\to\\infty$ 就比最高次 → $\\infty-\\infty$ 先乘共軛轉成 $\\frac{\\infty}{\\infty}$。</p>"
         "<p>學生最容易忘的不是招式,是<strong>先看型態</strong>這個習慣。檢討時每題只問一句:"
         "「這題是什麼型?」答得出來,招式自然跟著出來。</p>",
    guide=["代入 $x=3$ 到 $\\dfrac{x^2-9}{x^2-2x-3}$,分子得 <span class=\"blank\"></span>、"
           "分母得 <span class=\"blank\"></span>。這是什麼型?",
           "分子分母都在 $x=3$ 為 $0$,依因式定理,兩邊都有哪個共同因式?",
           "約掉之後剩下什麼?現在能代入了嗎?",
           "如果改成 $x\\to\\infty$,你的第一步會換成哪一招?"],
    demo="Evaluate $\\displaystyle\\lim_{x\\to 3}\\frac{x^2-9}{x^2-2x-3}$.",
    demo_sol="<p>代入得 $\\frac00$,兩邊因式分解:</p>"
             "$$\\frac{(x-3)(x+3)}{(x-3)(x+1)}=\\frac{x+3}{x+1}\\xrightarrow{x\\to3}\\frac{6}{4}=\\frac32.$$",
    demo_hint="代入會變成什麼型?分子分母各有什麼共同因式?",
    misstep="約分前要說清楚「$x\\to3$ 但 $x\\ne3$,所以 $x-3\\ne0$,可以約」。少了這句,約分就是非法動作。",
    level="basic",
    drills=[
        ("Evaluate $\\displaystyle\\lim_{x\\to\\infty}\\frac{4x^2-x}{3x^2+5}$.",
         "<p>同為二次,比最高次係數:$\\dfrac43$。</p>"),
        ("Evaluate $\\displaystyle\\lim_{x\\to 0}\\frac{\\sqrt{9+x}-3}{x}$.",
         "<p>乘共軛 $\\sqrt{9+x}+3$:$\\dfrac{x}{x(\\sqrt{9+x}+3)}=\\dfrac{1}{\\sqrt{9+x}+3}"
         "\\to\\dfrac16$。</p>"),
        ("Evaluate $\\displaystyle\\lim_{x\\to\\infty}\\left(\\sqrt{x^2+4x}-x\\right)$.",
         "<p>$\\infty-\\infty$,乘共軛:$\\dfrac{4x}{\\sqrt{x^2+4x}+x}"
         "=\\dfrac{4}{\\sqrt{1+4/x}+1}\\to 2$。</p>"),
    ])

C2 = Concept(
    title_en="Formal Definition of a Limit", title_zh="極限的正式定義",
    sub="A challenge-and-response game: you name the tolerance, I find the window",
    idea="$\\displaystyle\\lim_{x\\to a}f(x)=L$ means: for every $\\varepsilon&gt;0$ there exists "
         "$\\delta&gt;0$ such that $0&lt;|x-a|&lt;\\delta$ implies $|f(x)-L|&lt;\\varepsilon$. "
         "Read it as a game — you name how close you want $f(x)$ to be to $L$; I must produce a "
         "window around $a$ that delivers it.",
    deep="<p>整段定義只有一件事要學生聽懂:<strong>誰先出手</strong>。</p>"
         "<p class='step'>$\\varepsilon$ 是<strong>對手先出</strong>的挑戰:「我要 $f(x)$ 距離 $L$ "
         "不超過這麼多。」$\\delta$ 是<strong>你的回應</strong>:「那你把 $x$ 圈進我這個框裡就達標。」</p>"
         "<p class='step'>順序不能反。若先給 $\\delta$ 再找 $\\varepsilon$,那叫「函數有界」,不是極限。</p>"
         "<p>兩個細節值得各花一分鐘:</p>"
         "<ul>"
         "<li><strong>為什麼是 $0&lt;|x-a|$</strong>:左邊那個嚴格不等號把 $x=a$ 排除掉。"
         "極限問的是「靠近時發生什麼」,和「到達時是什麼」無關——這正是可去間斷點能存在的原因。</li>"
         "<li><strong>為什麼是「存在 $\\delta$」不是「所有 $\\delta$」</strong>:你只需要<em>找到一個</em>"
         "可行的框。框更小一定也可行,所以找到一個就贏了。</li>"
         "</ul>"
         "<p>幾何圖:在 $y$ 軸畫出 $(L-\\varepsilon,\\,L+\\varepsilon)$ 的水平帶,問學生「$x$ 要限制在"
         "多寬,曲線才整段落在帶子裡」——那個寬度就是 $2\\delta$。<span class='qed'>∎</span></p>",
    guide=["定義裡是<strong>誰先出手</strong>?$\\varepsilon$ 和 $\\delta$ 哪一個是「對手的挑戰」、"
           "哪一個是「你的回應」?",
           "$|f(x)-L|&lt;\\varepsilon$ 在圖上是什麼?($y$ 軸的一條 <span class=\"blank\"></span>)",
           "$0&lt;|x-a|&lt;\\delta$ 在圖上是什麼?為什麼左邊要寫 $0&lt;$?",
           "如果某個 $\\delta$ 可行,比它更小的 $\\delta$ 還可行嗎?為什麼這讓「存在一個」就夠了?"],
    demo="State precisely, in $\\varepsilon$-$\\delta$ language, what "
         "$\\displaystyle\\lim_{x\\to 2}(3x-1)=5$ asserts.",
    demo_sol="<p>逐字翻譯,不要跳步:</p>"
             "<p class='step'>對每一個 $\\varepsilon&gt;0$,都存在一個 $\\delta&gt;0$,使得只要 "
             "$0&lt;|x-2|&lt;\\delta$,就有 $|(3x-1)-5|&lt;\\varepsilon$。</p>"
             "<p>注意這句話<strong>只是敘述</strong>,還沒有證明。要證明它成立,得真的把 $\\delta$ "
             "造出來——那是下一個觀念的事。</p>",
    demo_hint="把 $a$、$L$、$f(x)$ 各是什麼先標出來,再照定義填進去。",
    misstep="把 $0&lt;|x-a|$ 寫成 $|x-a|$,等於把 $x=a$ 也算進去——那就變成連續的定義,不是極限。",
    level="mid",
    drills=[
        ("Write the $\\varepsilon$-$\\delta$ statement for $\\displaystyle\\lim_{x\\to 1}(2x+3)=5$.",
         "<p>對每個 $\\varepsilon&gt;0$,存在 $\\delta&gt;0$,使 $0&lt;|x-1|&lt;\\delta$ 時 "
         "$|(2x+3)-5|&lt;\\varepsilon$。</p>"),
        ("Explain in one sentence why the definition uses $0&lt;|x-a|$ rather than $|x-a|$.",
         "<p>為了把 $x=a$ 本身排除:極限只關心 $a$ <strong>附近</strong>的行為,"
         "$f(a)$ 是否有定義、等於多少都不影響極限。</p>"),
        ("Does the definition require $f(a)$ to be defined? Justify your answer.",
         "<p>不需要。定義只用到 $0&lt;|x-a|&lt;\\delta$ 的那些 $x$,永遠不碰 $x=a$。"
         "$\\dfrac{x^2-9}{x-3}$ 在 $x=3$ 無定義,極限照樣存在且等於 $6$。</p>"),
    ])

C3 = Concept(
    title_en="Building δ from ε", title_zh="由 ε 反推 δ",
    sub="Work backwards from the target inequality — that is the whole trick",
    idea="To prove a limit from the definition, start at the <em>goal</em> $|f(x)-L|&lt;\\varepsilon$, "
         "algebraically massage it into the form $|x-a|&lt;(\\text{something involving }\\varepsilon)$, "
         "and then declare that something to be your $\\delta$. Scratch work first, clean write-up second.",
    deep="<p>ε-δ 證明有<strong>固定格式</strong>,學生怕的是格式不是數學。把它拆成兩欄板書:</p>"
         "<p class='step'><strong>左欄(草稿·反推)</strong>:從想要的結論出發。"
         "$|(3x-1)-5|=|3x-6|=3|x-2|&lt;\\varepsilon \\iff |x-2|&lt;\\dfrac{\\varepsilon}{3}$。"
         "看見了嗎?$\\delta$ 就這樣自己掉出來。</p>"
         "<p class='step'><strong>右欄(正式·順推)</strong>:「取 $\\delta=\\dfrac{\\varepsilon}{3}$。"
         "若 $0&lt;|x-2|&lt;\\delta$,則 $|(3x-1)-5|=3|x-2|&lt;3\\delta=\\varepsilon$。」得證。</p>"
         "<p><strong>為什麼要分兩欄</strong>:草稿是「怎麼想到的」,正式是「為什麼對的」。"
         "考卷只要右欄,但學生沒寫過左欄就永遠不知道 $\\delta$ 哪來的。</p>"
         "<p><strong>非線性的情況</strong>(如 $f(x)=x^2$)反推會卡住,因為會多出一個含 $x$ 的因子。"
         "標準手法是<strong>先限制 $\\delta\\le1$</strong>,把那個因子壓成常數上界,再取 "
         "$\\delta=\\min\\{1,\\ \\cdot\\}$。這招在觀念 8 會再用一次。<span class='qed'>∎</span></p>",
    guide=["先算 $|(3x-1)-5|$,化簡成 $\\;\\underline{\\ \\ }\\;\\cdot|x-2|$ 的形式,係數是 "
           "<span class=\"blank\"></span>。",
           "要讓它 $&lt;\\varepsilon$,$|x-2|$ 必須小於 <span class=\"blank\"></span>。",
           "所以 $\\delta$ 該取多少?你能不能取更小的?可以的話為什麼還是對的?",
           "正式書寫時,順序要反過來寫:先<strong>取</strong> $\\delta$,再<strong>推</strong>出結論。"
           "試著把它寫成完整一句。"],
    demo="Prove $\\displaystyle\\lim_{x\\to 2}(3x-1)=5$ directly from the "
         "$\\varepsilon$-$\\delta$ definition.",
    demo_sol="<p><strong>草稿(反推)</strong>:$|(3x-1)-5|=|3x-6|=3|x-2|$。"
             "要它 $&lt;\\varepsilon$,只需 $|x-2|&lt;\\dfrac{\\varepsilon}{3}$。</p>"
             "<p><strong>正式(順推)</strong>:給定 $\\varepsilon&gt;0$,取 "
             "$\\delta=\\dfrac{\\varepsilon}{3}&gt;0$。若 $0&lt;|x-2|&lt;\\delta$,則</p>"
             "$$|(3x-1)-5|=3|x-2|&lt;3\\delta=3\\cdot\\frac{\\varepsilon}{3}=\\varepsilon.$$"
             "<p>依定義,$\\displaystyle\\lim_{x\\to2}(3x-1)=5$。$\\;\\blacksquare$</p>",
    demo_hint="先把 $|f(x)-L|$ 化成「常數乘上 $|x-2|$」,那個常數就決定 $\\delta$。",
    misstep="只寫草稿就交卷。草稿是反推,不是證明;正式證明必須<strong>先取 $\\delta$、再推結論</strong>,"
            "方向不能顛倒。",
    level="hard",
    drills=[
        ("Prove $\\displaystyle\\lim_{x\\to 1}(2x+3)=5$ from the definition.",
         "<p>$|(2x+3)-5|=2|x-1|$。取 $\\delta=\\dfrac{\\varepsilon}{2}$:"
         "$0&lt;|x-1|&lt;\\delta\\Rightarrow 2|x-1|&lt;\\varepsilon$。$\\;\\blacksquare$</p>"),
        ("Prove $\\displaystyle\\lim_{x\\to 4}(5-2x)=-3$ from the definition.",
         "<p>$|(5-2x)-(-3)|=|8-2x|=2|x-4|$。取 $\\delta=\\dfrac{\\varepsilon}{2}$ 即得。"
         "負係數取絕對值後照樣是 $2$。$\\;\\blacksquare$</p>"),
        ("For $\\displaystyle\\lim_{x\\to 3}(7x+1)=22$, find the largest $\\delta$ that works "
         "for $\\varepsilon=0.01$.",
         "<p>$|(7x+1)-22|=7|x-3|&lt;0.01\\iff|x-3|&lt;\\dfrac{0.01}{7}=\\dfrac{1}{700}$。"
         "最大可取 $\\delta=\\dfrac{1}{700}\\approx0.00143$。</p>"),
    ])

C4 = Concept(
    title_en="Why the Formal Definition Matters", title_zh="為什麼需要嚴格定義",
    sub="A table of values can suggest a limit — and be completely wrong",
    idea="Sampling is not proof. There are functions whose values at $x=1,\\tfrac12,\\tfrac13,\\dots$ "
         "march neatly toward a number while the limit does not exist at all. The formal definition "
         "exists precisely to rule out being fooled by a finite table.",
    deep="<p>這一段是本週的<strong>說服環節</strong>。學生心裡的 OS 是「我用計算機代幾個數不就好了,"
         "幹嘛學這個」,不打掉這個念頭,ε-δ 對他們就永遠是廢話。</p>"
         "<p class='step'>反例:$f(x)=\\sin\\dfrac{\\pi}{x}$。在 $x=1,\\tfrac12,\\tfrac13,\\tfrac14,\\dots$ "
         "上,$\\dfrac{\\pi}{x}=\\pi,2\\pi,3\\pi,4\\pi,\\dots$,所以 $f$ <strong>每一個取樣點都恰好是 "
         "$0$</strong>。表格會漂亮地顯示「趨近 $0$」。</p>"
         "<p class='step'>但沿著 $x=\\dfrac{2}{4k+1}$ 取樣,$\\dfrac{\\pi}{x}=\\dfrac{(4k+1)\\pi}{2}$,"
         "$f$ <strong>每一點都是 $1$</strong>。同一個 $x\\to0$,兩條路給出兩個答案 → 極限不存在。</p>"
         "<p>結論一句話送給學生:<strong>表格只能否證,不能證明</strong>。看到表格亂跳可以下結論"
         "「不存在」,看到表格乖乖收斂卻什麼都不能保證——因為你永遠只取了有限多個點,"
         "而定義要求的是<strong>所有</strong>滿足 $0&lt;|x-a|&lt;\\delta$ 的 $x$。</p>",
    guide=["把 $x=1,\\tfrac12,\\tfrac13,\\tfrac14$ 代進 $\\sin\\dfrac{\\pi}{x}$,"
           "$\\dfrac{\\pi}{x}$ 分別是 <span class=\"blank\"></span>,函數值都是 "
           "<span class=\"blank\"></span>。",
           "光看這張表,你會猜極限是多少?",
           "現在試 $x=\\dfrac{2}{5}$:$\\dfrac{\\pi}{x}=\\dfrac{5\\pi}{2}$,$\\sin$ 值是 "
           "<span class=\"blank\"></span>。表格說謊了嗎?",
           "定義裡哪一個字眼(「對<strong>每一個</strong>」還是「<strong>存在</strong>」)"
           "擋住了這種被表格騙的情況?"],
    demo="Evaluate $f(x)=\\sin\\dfrac{\\pi}{x}$ at $x=1,\\tfrac12,\\tfrac13,\\tfrac14$. "
         "What does the table suggest, and is the suggestion correct?",
    demo_sol="<p>$\\dfrac{\\pi}{x}=\\pi,\\,2\\pi,\\,3\\pi,\\,4\\pi$,故四個函數值<strong>全是 $0$</strong>,"
             "表格看起來在說「極限是 $0$」。</p>"
             "<p>但沿 $x=\\dfrac25$ 得 $\\sin\\dfrac{5\\pi}{2}=1$;更一般地取 "
             "$x=\\dfrac{2}{4k+1}\\to0$,函數值恆為 $1$。</p>"
             "<p>兩條路徑趨近 $0$ 卻給出 $0$ 與 $1$ 兩個值 ⟹ "
             "$\\displaystyle\\lim_{x\\to0}\\sin\\frac{\\pi}{x}$ <strong>不存在</strong>。"
             "表格的建議是錯的。</p>",
    demo_hint="先算 $\\dfrac{\\pi}{x}$ 是 $\\pi$ 的幾倍,再想 $\\sin$ 在那些點的值。",
    misstep="用有限筆數值「證明」極限存在。數值可以幫你<strong>猜</strong>、可以幫你"
            "<strong>否證</strong>,但永遠不能當證明。",
    level="mid",
    drills=[
        ("Find a sequence $x_n\\to 0$ along which $\\sin\\dfrac{\\pi}{x}$ is always $1$.",
         "<p>取 $x_n=\\dfrac{2}{4n+1}$,則 $\\dfrac{\\pi}{x_n}=\\dfrac{(4n+1)\\pi}{2}$,"
         "$\\sin$ 值恆為 $1$,而 $x_n\\to0$。</p>"),
        ("Explain why a table of values can never prove that a limit exists.",
         "<p>表格只檢查有限多個 $x$,定義要求的是<strong>所有</strong>滿足 "
         "$0&lt;|x-a|&lt;\\delta$ 的 $x$。漏掉的點可能藏著完全不同的行為。</p>"),
        ("Does $\\displaystyle\\lim_{x\\to0}x\\sin\\dfrac{\\pi}{x}$ exist? Explain the difference "
         "from the previous case.",
         "<p>存在,等於 $0$。因為 $-|x|\\le x\\sin\\dfrac{\\pi}{x}\\le|x|$,被夾擠壓住;"
         "振盪還在,但振幅被 $|x|$ 掐掉了。</p>"),
    ])

C5 = Concept(
    title_en="One-Sided Limits, Formally", title_zh="單邊極限的正式定義",
    sub="Same game, but the window only opens on one side",
    idea="$\\displaystyle\\lim_{x\\to a^{+}}f(x)=L$ means: for every $\\varepsilon&gt;0$ there is "
         "$\\delta&gt;0$ with $a&lt;x&lt;a+\\delta \\Rightarrow |f(x)-L|&lt;\\varepsilon$. Only the "
         "window changes; the challenge-response structure is identical.",
    deep="<p>把雙邊定義的 $0&lt;|x-a|&lt;\\delta$ 換掉就好:</p>"
         "<p class='step'>右極限:$a&lt;x&lt;a+\\delta$。左極限:$a-\\delta&lt;x&lt;a$。</p>"
         "<p>兩個都把 $x=a$ 排除在外(不等號是嚴格的),和雙邊定義一致。</p>"
         "<p><strong>雙邊存在 $\\iff$ 左右都存在且相等</strong>,這件事在正式定義下有了證明:"
         "若雙邊成立,取同一個 $\\delta$ 顯然兩側各自成立;反之若左右各給出 $\\delta_1,\\delta_2$,"
         "取 $\\delta=\\min\\{\\delta_1,\\delta_2\\}$ 就同時滿足兩側。"
         "<strong>取 min</strong> 是 ε-δ 裡最常用的小動作,值得寫在黑板角落。"
         "<span class='qed'>∎</span></p>",
    guide=["把雙邊定義裡的 $0&lt;|x-a|&lt;\\delta$ 改成只允許「比 $a$ 大」,會寫成 "
           "<span class=\"blank\"></span>。",
           "左極限那一版呢?",
           "$f(x)=\\dfrac{|x|}{x}$ 在 $x&gt;0$ 恆為 <span class=\"blank\"></span>、"
           "$x&lt;0$ 恆為 <span class=\"blank\"></span>。兩邊極限各是多少?",
           "若有人主張雙邊極限存在,他必須為<strong>同一個</strong> $L$ 找到 $\\delta$。"
           "拿 $\\varepsilon=\\tfrac12$ 去挑戰他,他為什麼一定失敗?"],
    demo="State the $\\varepsilon$-$\\delta$ definition of $\\displaystyle\\lim_{x\\to a^{+}}f(x)=L$, "
         "then use it to justify $\\displaystyle\\lim_{x\\to 0^{+}}\\sqrt{x}=0$.",
    demo_sol="<p><strong>定義</strong>:對每個 $\\varepsilon&gt;0$,存在 $\\delta&gt;0$,使 "
             "$a&lt;x&lt;a+\\delta$ 時 $|f(x)-L|&lt;\\varepsilon$。</p>"
             "<p><strong>套用</strong>:要 $|\\sqrt{x}-0|=\\sqrt{x}&lt;\\varepsilon$,"
             "即 $x&lt;\\varepsilon^2$。取 $\\delta=\\varepsilon^{2}$:</p>"
             "$$0&lt;x&lt;\\delta=\\varepsilon^{2}\\ \\Longrightarrow\\ "
             "\\sqrt{x}&lt;\\varepsilon.$$"
             "<p>注意這裡<strong>只能</strong>談右極限——$\\sqrt{x}$ 在 $x&lt;0$ 沒有定義。"
             "$\\;\\blacksquare$</p>",
    demo_hint="要讓 $\\sqrt{x}$ 小於 $\\varepsilon$,$x$ 要小於什麼?兩邊平方看看。",
    misstep="$\\delta$ 取成 $\\varepsilon$ 而不是 $\\varepsilon^{2}$。牽涉根號時,反推要記得平方。",
    level="mid",
    drills=[
        ("Write the formal definition of $\\displaystyle\\lim_{x\\to a^{-}}f(x)=L$.",
         "<p>對每個 $\\varepsilon&gt;0$,存在 $\\delta&gt;0$,使 $a-\\delta&lt;x&lt;a$ 時 "
         "$|f(x)-L|&lt;\\varepsilon$。</p>"),
        ("For $f(x)=\\dfrac{|x|}{x}$, state both one-sided limits at $0$ and explain why the "
         "two-sided limit fails the definition.",
         "<p>右極限 $1$、左極限 $-1$。若雙邊極限為某個 $L$,取 $\\varepsilon=\\tfrac12$,"
         "則同一個 $\\delta$ 內必須同時有 $|1-L|&lt;\\tfrac12$ 與 $|-1-L|&lt;\\tfrac12$,"
         "但這兩個區間不相交 → 矛盾。</p>"),
        ("For $\\displaystyle\\lim_{x\\to 0^{+}}\\sqrt{x}=0$, express $\\delta$ in terms of "
         "$\\varepsilon$.",
         "<p>$\\delta=\\varepsilon^{2}$(或任何更小的正數)。</p>"),
    ])

C6 = Concept(
    title_en="Infinite Limits, Formally", title_zh="無窮極限的正式定義",
    sub="Replace ε with M: bigger than any bound you care to name",
    idea="$\\displaystyle\\lim_{x\\to a}f(x)=\\infty$ means: for every $M&gt;0$ there is "
         "$\\delta&gt;0$ such that $0&lt;|x-a|&lt;\\delta \\Rightarrow f(x)&gt;M$. Note that "
         "$\\infty$ is not a value being approached — the statement says the function eventually "
         "exceeds every bound.",
    deep="<p>學生從銜接課帶來一個壞習慣:把 $\\infty$ 當數字。正式定義正好治這個病——"
         "整句話裡<strong>沒有任何地方把 $f(x)$ 和 $\\infty$ 相減</strong>。</p>"
         "<p class='step'>挑戰不再是「離 $L$ 多近」($\\varepsilon$),而是「要衝多高」($M$)。"
         "回應一樣是 $\\delta$。</p>"
         "<p class='step'>$\\displaystyle\\lim_{x\\to a}f(x)=-\\infty$:對每個 $M&gt;0$,存在 "
         "$\\delta&gt;0$,使 $0&lt;|x-a|&lt;\\delta$ 時 $f(x)&lt;-M$。</p>"
         "<p>提醒:寫成 $=\\infty$ 是<strong>約定俗成的簡寫</strong>,嚴格說極限並不存在"
         "(存在的定義要求 $L$ 是實數)。台灣課本多半寫「趨近無窮」,考卷兩種寫法都要看得懂。"
         "<span class='qed'>∎</span></p>",
    guide=["把 $\\varepsilon$ 換成 $M$、把 $|f(x)-L|&lt;\\varepsilon$ 換成 "
           "<span class=\"blank\"></span>,就得到無窮極限的定義。",
           "要讓 $\\dfrac{1}{x^{2}}&gt;M$,$x^{2}$ 要小於 <span class=\"blank\"></span>,"
           "所以 $|x|$ 要小於 <span class=\"blank\"></span>。",
           "所以 $\\delta$ 取多少?",
           "$-\\infty$ 那一版要怎麼改?(想:哪個不等號要翻面)"],
    demo="Prove $\\displaystyle\\lim_{x\\to 0}\\frac{1}{x^{2}}=\\infty$ from the definition.",
    demo_sol="<p><strong>草稿</strong>:要 $\\dfrac{1}{x^{2}}&gt;M$,即 $x^{2}&lt;\\dfrac1M$,"
             "即 $|x|&lt;\\dfrac{1}{\\sqrt M}$。</p>"
             "<p><strong>正式</strong>:給定 $M&gt;0$,取 $\\delta=\\dfrac{1}{\\sqrt M}$。"
             "若 $0&lt;|x|&lt;\\delta$,則 $x^{2}&lt;\\dfrac1M$,故</p>"
             "$$\\frac{1}{x^{2}}&gt;M.$$"
             "<p>依定義,極限為 $\\infty$。$\\;\\blacksquare$</p>",
    demo_hint="從想要的 $\\dfrac{1}{x^2}&gt;M$ 反推,兩邊取倒數時不等號會翻面。",
    misstep="取倒數忘了翻不等號。$\\dfrac{1}{x^2}&gt;M \\iff x^2&lt;\\dfrac1M$,方向是相反的。",
    level="hard",
    drills=[
        ("For $\\displaystyle\\lim_{x\\to 0}\\frac{1}{x^{2}}=\\infty$, express $\\delta$ in terms "
         "of $M$.",
         "<p>$\\delta=\\dfrac{1}{\\sqrt M}$。</p>"),
        ("State the formal definition of $\\displaystyle\\lim_{x\\to a}f(x)=-\\infty$.",
         "<p>對每個 $M&gt;0$,存在 $\\delta&gt;0$,使 $0&lt;|x-a|&lt;\\delta$ 時 $f(x)&lt;-M$。</p>"),
        ("Prove $\\displaystyle\\lim_{x\\to 1^{+}}\\frac{1}{x-1}=\\infty$.",
         "<p>要 $\\dfrac{1}{x-1}&gt;M$ 且 $x&gt;1$,即 $0&lt;x-1&lt;\\dfrac1M$。"
         "取 $\\delta=\\dfrac1M$ 即得。$\\;\\blacksquare$</p>"),
    ])

C7 = Concept(
    title_en="Limits at Infinity, Formally", title_zh="趨向無窮的正式定義",
    sub="Replace δ with N: far enough to the right, the graph stays in the band",
    idea="$\\displaystyle\\lim_{x\\to\\infty}f(x)=L$ means: for every $\\varepsilon&gt;0$ there is "
         "a number $N$ such that $x&gt;N \\Rightarrow |f(x)-L|&lt;\\varepsilon$. The response is no "
         "longer a window around $a$ but a starting line $N$ beyond which the graph never leaves "
         "the band.",
    deep="<p>三個定義的家族關係一次講完,學生就不會覺得在背四套東西:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>極限型態</th><th>挑戰</th><th>回應</th></tr></thead>"
         "<tbody>"
         "<tr><td>$x\\to a$,$f\\to L$</td><td>$\\varepsilon$</td><td>$\\delta$(窗)</td></tr>"
         "<tr><td>$x\\to a$,$f\\to\\infty$</td><td>$M$</td><td>$\\delta$(窗)</td></tr>"
         "<tr><td>$x\\to\\infty$,$f\\to L$</td><td>$\\varepsilon$</td><td>$N$(起跑線)</td></tr>"
         "<tr><td>$x\\to\\infty$,$f\\to\\infty$</td><td>$M$</td><td>$N$(起跑線)</td></tr>"
         "</tbody></table></div>"
         "<p><strong>一句話總結</strong>:挑戰看「$y$ 方向要多準」,回應看「$x$ 方向要多嚴」。"
         "四個定義是同一個句型的四種填空。</p>"
         "<p>水平漸近線的嚴格意義就藏在這裡:$y=L$ 是漸近線,恰好是說「無論帶子多窄,"
         "夠遠之後曲線都待在裡面」。<span class='qed'>∎</span></p>",
    guide=["這次的挑戰還是 $\\varepsilon$,但回應不再是窗,而是一條 <span class=\"blank\"></span>。",
           "要 $\\left|\\dfrac1x-0\\right|&lt;\\varepsilon$(且 $x&gt;0$),$x$ 要大於 "
           "<span class=\"blank\"></span>。",
           "所以 $N$ 取多少?$N$ 需不需要是正整數?",
           "把這個定義和「水平漸近線」的說法對起來:$y=L$ 是漸近線,用這個定義怎麼講?"],
    demo="Prove $\\displaystyle\\lim_{x\\to\\infty}\\frac{1}{x}=0$ from the definition.",
    demo_sol="<p><strong>草稿</strong>:$\\left|\\dfrac1x-0\\right|=\\dfrac1x&lt;\\varepsilon "
             "\\iff x&gt;\\dfrac{1}{\\varepsilon}$(對 $x&gt;0$)。</p>"
             "<p><strong>正式</strong>:給定 $\\varepsilon&gt;0$,取 $N=\\dfrac{1}{\\varepsilon}$。"
             "若 $x&gt;N$,則</p>"
             "$$\\left|\\frac1x-0\\right|=\\frac1x&lt;\\frac1N=\\varepsilon.$$"
             "<p>依定義,極限為 $0$,且 $y=0$ 是水平漸近線。$\\;\\blacksquare$</p>",
    demo_hint="$\\left|\\dfrac1x\\right|&lt;\\varepsilon$ 兩邊取倒數會得到什麼?",
    misstep="忘記先假設 $x&gt;0$ 就把 $\\left|\\dfrac1x\\right|$ 寫成 $\\dfrac1x$。"
            "$x\\to\\infty$ 時可以放心假設 $x&gt;0$,但要寫出來。",
    level="hard",
    drills=[
        ("For $\\displaystyle\\lim_{x\\to\\infty}\\frac{1}{x^{2}}=0$, express $N$ in terms of "
         "$\\varepsilon$.",
         "<p>$\\dfrac{1}{x^{2}}&lt;\\varepsilon\\iff x&gt;\\dfrac{1}{\\sqrt\\varepsilon}$,"
         "取 $N=\\dfrac{1}{\\sqrt\\varepsilon}$。</p>"),
        ("Find $N$ in terms of $\\varepsilon$ for $\\displaystyle\\lim_{x\\to\\infty}"
         "\\frac{3x+1}{x}=3$.",
         "<p>$\\left|\\dfrac{3x+1}{x}-3\\right|=\\dfrac1x&lt;\\varepsilon\\iff "
         "x&gt;\\dfrac1\\varepsilon$,取 $N=\\dfrac{1}{\\varepsilon}$。</p>"),
        ("State the formal definition of $\\displaystyle\\lim_{x\\to-\\infty}f(x)=L$.",
         "<p>對每個 $\\varepsilon&gt;0$,存在 $N$,使 $x&lt;N$ 時 $|f(x)-L|&lt;\\varepsilon$。"
         "(起跑線換到左邊,不等號翻面。)</p>"),
    ])

C8 = Concept(
    title_en="Continuity Revisited", title_zh="用正式定義看連續",
    sub="Same inequality, one symbol removed — and that symbol is the whole difference",
    idea="$f$ is continuous at $a$ iff for every $\\varepsilon&gt;0$ there is $\\delta&gt;0$ with "
         "$|x-a|&lt;\\delta \\Rightarrow |f(x)-f(a)|&lt;\\varepsilon$. Compared with the limit "
         "definition, the $0&lt;$ is gone and $L$ has been replaced by $f(a)$ — that is exactly the "
         "content of the three-condition test.",
    deep="<p>把兩個定義並排寫在黑板上,只圈出兩個差異,學生會有「原來如此」的表情:</p>"
         "<p class='step'>極限:$\\;0&lt;|x-a|&lt;\\delta \\Rightarrow |f(x)-\\mathbf{L}|&lt;\\varepsilon$</p>"
         "<p class='step'>連續:$\\;\\ \\ \\ \\ |x-a|&lt;\\delta \\Rightarrow |f(x)-\\mathbf{f(a)}|&lt;\\varepsilon$</p>"
         "<p>兩處差異,正好對應銜接課的三條件:拿掉 $0&lt;$ ⟹ $x=a$ 也要算 ⟹ "
         "<strong>$f(a)$ 必須有定義</strong>;把 $L$ 換成 $f(a)$ ⟹ "
         "<strong>極限存在且等於函數值</strong>。</p>"
         "<p><strong>非線性的 δ 要先限制範圍</strong>。以 $f(x)=x^{2}$ 在 $a=1$ 為例:"
         "$|x^{2}-1|=|x-1|\\,|x+1|$。$|x+1|$ 還帶著 $x$,不能直接除。先規定 $\\delta\\le1$,"
         "則 $|x-1|&lt;1 \\Rightarrow 0&lt;x&lt;2 \\Rightarrow |x+1|&lt;3$,於是</p>"
         "<p class='step'>$|x^{2}-1|&lt;3|x-1|&lt;\\varepsilon$,只要 "
         "$|x-1|&lt;\\dfrac{\\varepsilon}{3}$。取 $\\delta=\\min\\left\\{1,\\dfrac{\\varepsilon}{3}\\right\\}$。</p>"
         "<p>這個 $\\min$ 的手法整個學期還會再遇到,值得學生抄進筆記本。<span class='qed'>∎</span></p>",
    guide=["把極限的定義寫出來,再把連續的定義寫在下面。圈出<strong>兩處</strong>不同:"
           "一是 <span class=\"blank\"></span>,二是 <span class=\"blank\"></span>。",
           "「拿掉 $0&lt;$」對應到銜接課三條件的哪一條?",
           "「$L$ 換成 $f(a)$」又對應哪一條?",
           "$f(x)=3x-1$ 在 $x=2$:$|f(x)-f(2)|=3|x-2|$,所以 $\\delta$ 取 "
           "<span class=\"blank\"></span> 就好。和觀念 3 的答案一樣嗎?"],
    demo="Using the $\\varepsilon$-$\\delta$ form of continuity, show that $f(x)=3x-1$ is "
         "continuous at $x=2$.",
    demo_sol="<p>$f(2)=5$。給定 $\\varepsilon&gt;0$,取 $\\delta=\\dfrac{\\varepsilon}{3}$。"
             "若 $|x-2|&lt;\\delta$(這次<strong>包含</strong> $x=2$),則</p>"
             "$$|f(x)-f(2)|=|3x-6|=3|x-2|&lt;3\\delta=\\varepsilon.$$"
             "<p>依定義,$f$ 在 $x=2$ 連續。注意 $x=2$ 時左式為 $0&lt;\\varepsilon$,"
             "自動成立——這正是「包含端點」不會出事的原因。$\\;\\blacksquare$</p>",
    demo_hint="和觀念 3 幾乎一模一樣,只有兩個地方要改。是哪兩個?",
    misstep="以為連續要另學一套。它就是極限的定義拿掉 $0&lt;$、把 $L$ 換成 $f(a)$,沒有第三件事。",
    level="mid",
    drills=[
        ("State the two differences between the $\\varepsilon$-$\\delta$ definition of a limit and "
         "that of continuity at $a$.",
         "<p>(1) 連續的條件是 $|x-a|&lt;\\delta$,沒有 $0&lt;$,故 $x=a$ 也納入;"
         "(2) 目標值由任意的 $L$ 指定成 $f(a)$。</p>"),
        ("Show $f(x)=x^{2}$ is continuous at $x=1$ by exhibiting a $\\delta$ that works for "
         "$\\varepsilon=0.01$.",
         "<p>先限制 $\\delta\\le1$,則 $|x+1|&lt;3$,故 $|x^2-1|&lt;3|x-1|$。"
         "取 $\\delta=\\min\\left\\{1,\\dfrac{0.01}{3}\\right\\}=\\dfrac{1}{300}$。</p>"),
        ("Is $f(x)=\\dfrac1x$ continuous at $x=0$? Answer using the definition.",
         "<p>不是——連續要求 $f(0)$ 有定義,但 $\\dfrac10$ 無定義,第一關就過不了,"
         "$\\varepsilon$-$\\delta$ 條件根本無從檢查。</p>"),
    ])

C9 = Concept(
    title_en="Floating-Point Reality", title_zh="浮點數下的極限",
    sub="A machine has no infinitesimals — below machine epsilon, h→0 stops meaning anything",
    idea="A double-precision number near $1$ has neighbours about $2.2\\times10^{-16}$ away "
         "(machine epsilon). Once $h$ falls below that spacing, $x+h$ rounds back to $x$ and the "
         "difference quotient collapses to exactly $0$. The mathematical limit and the computed "
         "limit part ways.",
    deep="<p>這是本週<strong>把數學接回 CS</strong> 的一段,也是《CS 自學聖經》第 107 章"
         "〈浮點數〉的入口。</p>"
         "<p class='step'>雙精度浮點數在 $1$ 附近的間距是 $\\varepsilon_{\\text{mach}}"
         "\\approx2.22\\times10^{-16}$。比這更小的差距,機器<strong>表示不出來</strong>。</p>"
         "<p class='step'>所以 $1+10^{-20}$ 在機器裡<strong>就是</strong> $1$。差商 "
         "$\\dfrac{f(1+h)-f(1)}{h}$ 在 $h=10^{-20}$ 時分子恰為 $0$,結果是 $0$——不是近似 $2$,"
         "是<strong>徹底錯</strong>。</p>"
         "<p><strong>兩種誤差在拔河</strong>:$h$ 變小,截斷誤差(數學上的近似誤差)$\\sim h$ 變小;"
         "但捨入誤差 $\\sim\\dfrac{\\varepsilon_{\\text{mach}}}{h}$ 變大。兩者相等時總誤差最小,"
         "解出 $h^{*}\\approx\\sqrt{\\varepsilon_{\\text{mach}}}\\approx1.5\\times10^{-8}$。</p>"
         "<p>這個 $\\sqrt{\\varepsilon_{\\text{mach}}}$ 是數值微分的<strong>經驗法則</strong>,"
         "實作課會親眼看到誤差曲線先降後升的 V 字形。<span class='qed'>∎</span></p>",
    guide=["雙精度在 $1$ 附近能分辨的最小差距叫 <span class=\"blank\"></span>,大約是 "
           "<span class=\"blank\"></span>。",
           "那 $1+10^{-20}$ 在機器裡等於多少?$\\;(1+10^{-20})-1$ 會算出什麼?",
           "所以 $\\dfrac{(1+h)^{2}-1^{2}}{h}$ 在 $h=10^{-20}$ 會得到 <span class=\"blank\"></span>,"
           "但數學上的答案是 <span class=\"blank\"></span>。",
           "$h$ 太大不準(截斷誤差)、太小也不準(捨入誤差),你猜最佳的 $h$ 大概在哪個數量級?"],
    demo="The difference quotient of $f(x)=x^{2}$ at $x=1$ is computed in double precision with "
         "$h=10^{-20}$. What does the machine return, and why?",
    demo_sol="<p>機器回傳 <strong>$0.0$</strong>。</p>"
             "<p>因為 $10^{-20}$ 遠小於 $1$ 附近的浮點間距 $\\varepsilon_{\\text{mach}}"
             "\\approx2.22\\times10^{-16}$,所以 $1+10^{-20}$ 捨入後<strong>就是 $1$</strong>。"
             "分子 $(1)^{2}-(1)^{2}=0$,整個差商是 $\\dfrac{0}{10^{-20}}=0$。</p>"
             "<p>數學上的答案是 $f'(1)=2$。這不是「不夠精確」,是<strong>完全錯誤</strong>——"
             "而且錯得很安靜,不會拋任何例外。</p>",
    demo_hint="先問:$1+10^{-20}$ 在雙精度裡存得下來嗎?分子會變成多少?",
    misstep="以為「$h$ 越小越準」。數值微分的誤差是 V 字形,過了 $\\sqrt{\\varepsilon_{\\text{mach}}}"
            "\\approx10^{-8}$ 之後越小越糟。",
    level="mid",
    drills=[
        ("Compute $(1+10^{-16})-1$ in double precision and explain the result.",
         "<p>得 $0.0$。因為 $10^{-16}&lt;\\dfrac{\\varepsilon_{\\text{mach}}}{2}"
         "\\approx1.11\\times10^{-16}$,$1+10^{-16}$ 捨入回 $1$。</p>"),
        ("Why does the forward difference $\\dfrac{f(x+h)-f(x)}{h}$ have an optimal $h$ near "
         "$\\sqrt{\\varepsilon_{\\text{mach}}}$?",
         "<p>截斷誤差 $\\sim h$、捨入誤差 $\\sim\\dfrac{\\varepsilon_{\\text{mach}}}{h}$,"
         "總誤差在兩者相等時最小,解 $h=\\dfrac{\\varepsilon_{\\text{mach}}}{h}$ 得 "
         "$h\\approx\\sqrt{\\varepsilon_{\\text{mach}}}\\approx1.5\\times10^{-8}$。</p>"),
        ("In exact mathematics, is there a smallest positive real number? In double precision, is "
         "there a smallest positive value? What does the difference imply for $h\\to0$?",
         "<p>實數沒有最小正數(任何正數除以 2 還是正數);雙精度有(次正規數約 "
         "$5\\times10^{-324}$)。所以「令 $h\\to0$」在機器上只能走有限步,"
         "極限的無限逼近在數值上根本不存在。</p>"),
    ])

C10 = Concept(
    title_en="Catastrophic Cancellation", title_zh="災難性消去",
    sub="Subtracting two nearly equal numbers throws away the digits you cared about",
    idea="When two nearly equal floating-point numbers are subtracted, the leading digits cancel "
         "and the surviving digits are mostly rounding noise — the relative error explodes. The "
         "algebraically equivalent rationalized form avoids the subtraction and stays accurate.",
    deep="<p>接續觀念 9:上一段是「$h$ 太小會歸零」,這一段是「就算沒歸零,答案也可能爛掉」。</p>"
         "<p class='step'>$\\sqrt{1+x}-1$ 在 $x$ 很小時,兩項幾乎相等。假設各自有 16 位有效數字,"
         "相減後<strong>前面十幾位全部抵消</strong>,只剩最後幾位——而那幾位本來就是捨入誤差。</p>"
         "<p class='step'>解法是<strong>消滅減法</strong>。乘共軛:</p>"
         "$$\\frac{\\sqrt{1+x}-1}{x}=\\frac{1}{\\sqrt{1+x}+1}.$$"
         "<p>右邊是<strong>加法</strong>,沒有抵消問題,在任何 $x$ 都穩。兩式代數上完全等價,"
         "數值上天差地遠。</p>"
         "<p><strong>這裡有個漂亮的教學點</strong>:銜接課教有理化是為了「消掉 $\\frac00$」,"
         "現在同一招變成「消掉數值不穩定」。同一個代數技巧,兩種完全不同的動機——"
         "這就是為什麼值得把式子變形學好。</p>"
         "<p>其他常見的穩定化改寫:$\\sqrt{x+1}-\\sqrt{x}=\\dfrac{1}{\\sqrt{x+1}+\\sqrt{x}}$;"
         "$1-\\cos x=2\\sin^{2}\\dfrac{x}{2}$。<span class='qed'>∎</span></p>",
    guide=["$x=10^{-12}$ 時,$\\sqrt{1+x}$ 和 $1$ 差多少?兩個數的前幾位一不一樣?",
           "相減之後,原本 16 位有效數字還剩下幾位是「真的」?",
           "把 $\\dfrac{\\sqrt{1+x}-1}{x}$ 乘共軛化簡,會變成 <span class=\"blank\"></span>。",
           "新式子裡還有減法嗎?為什麼這樣就安全了?"],
    demo="Evaluate $\\displaystyle\\frac{\\sqrt{1+x}-1}{x}$ at $x=10^{-12}$ both directly and via "
         "the rationalized form $\\dfrac{1}{\\sqrt{1+x}+1}$. Which one should you trust?",
    demo_sol="<p>直接算得 $0.5000444502911705$;有理化後得 $0.499999999999875$。"
             "真值是 $\\dfrac{1}{\\sqrt{1+10^{-12}}+1}\\approx0.4999999999999$。</p>"
             "<p>直接算的版本在<strong>第 4 位有效數字</strong>就開始錯,誤差約 "
             "$4.4\\times10^{-5}$——而輸入只有 $10^{-12}$ 的量級。相對誤差被放大了七、八個數量級。</p>"
             "<p>該相信有理化的版本。$x$ 再小一點(如 $10^{-16}$),直接算會直接歸零,"
             "有理化的版本依然給出 $0.5$。</p>",
    demo_hint="兩個算式代數上相同,但一個含減法、一個不含。哪一個會抵消掉有效數字?",
    misstep="以為「代數等價 ⟹ 數值等價」。浮點數下這是<strong>錯的</strong>,"
            "式子怎麼寫會直接決定答案準不準。",
    level="hard",
    drills=[
        ("What is the exact value of $\\displaystyle\\lim_{x\\to0}\\frac{\\sqrt{1+x}-1}{x}$?",
         "<p>乘共軛得 $\\dfrac{1}{\\sqrt{1+x}+1}\\to\\dfrac12$。</p>"),
        ("Rewrite $\\sqrt{x+1}-\\sqrt{x}$ in a numerically stable form for large $x$.",
         "<p>$\\sqrt{x+1}-\\sqrt{x}=\\dfrac{1}{\\sqrt{x+1}+\\sqrt{x}}$。"
         "大 $x$ 時兩根號幾乎相等,直接相減會嚴重抵消。</p>"),
        ("Rewrite $1-\\cos x$ in a numerically stable form for small $x$.",
         "<p>$1-\\cos x=2\\sin^{2}\\dfrac{x}{2}$。右式沒有相近數相減,"
         "小 $x$ 時穩定得多。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜數值探極限:先變準,再變爛",
    intro="銜接課用數值表猜極限。這次把 $h$ 一路縮到 $10^{-16}$,看那張表在什麼時候開始騙人。",
    code="""# f(x) = x^2 在 x = 1 的導數,真值 f'(1) = 2
f = lambda x: x**2
x0, exact = 1.0, 2.0

print(f"{'h':>10}  {'差商':>20}  {'誤差':>12}")
hs = [10.0**(-k) for k in range(1, 17)]
errs = []
for h in hs:
    q = (f(x0 + h) - f(x0)) / h
    err = abs(q - exact)
    errs.append(err)
    print(f"{h:10.0e}  {q:20.16f}  {err:12.3e}")

plt.loglog(hs, errs, 'o-')
plt.axvline(np.sqrt(np.finfo(float).eps), color='C3', ls='--',
            label='sqrt(machine eps)')
plt.gca().invert_xaxis()
plt.xlabel('h'); plt.ylabel('|error|'); plt.legend()
plt.title('Forward difference error: down, then up')
plt.show()

best = hs[int(np.argmin(errs))]
print("\\n最準的 h =", f"{best:.0e}", "  sqrt(eps) =", f"{np.sqrt(np.finfo(float).eps):.2e}")""",
    expected="最準的 h = 1e-08   sqrt(eps) = 1.49e-08",
    seealso="誤差先隨 $h$ 變小而下降(截斷誤差),過了 $\\sqrt{\\varepsilon_{\\text{mach}}}"
            "\\approx10^{-8}$ 之後反而上升(捨入誤差)——一個漂亮的 V 字。"
            "$h=10^{-16}$ 時差商直接變成 $0$。",
    todo="""# TODO 學生練習:把 f 換成 sin,x0 換成 0(真值 f'(0) = cos(0) = 1)
# 重跑一次,最佳的 h 還是落在 1e-8 附近嗎?
# f = lambda x: math.sin(x); x0, exact = 0.0, 1.0""")

LAB2 = Lab(
    title="Lab 2｜機器 epsilon:電腦的「最小可分辨距離」",
    intro="為什麼 $h$ 不能無限小?因為浮點數之間有間距。這格把那個間距量出來。",
    code="""eps = np.finfo(float).eps
print("machine epsilon =", eps)
print("eps / 2         =", eps / 2)

# 1 + h 什麼時候才不等於 1?
for k in [15, 16, 17]:
    h = 10.0**(-k)
    print(f"1 + 1e-{k} == 1 ?  {1 + h == 1}   (1+h)-1 = {(1 + h) - 1:.3e}")

# 浮點數的間距隨數字大小改變
for x in [1e-8, 1.0, 1e8, 1e16]:
    print(f"x = {x:8.0e}   相鄰浮點數間距 = {np.spacing(x):.3e}")

# 經典陷阱
print("\\n0.1 + 0.2 == 0.3 ?", 0.1 + 0.2 == 0.3)
print("0.1 + 0.2 =", f"{0.1 + 0.2:.20f}")""",
    expected="machine epsilon = 2.220446049250313e-16\n0.1 + 0.2 == 0.3 ? False",
    seealso="間距<strong>不是固定值</strong>——它隨數字大小成比例放大。在 $10^{16}$ 附近,"
            "相鄰浮點數已經差了 $2$,連整數都存不完整。",
    todo="")

LAB3 = Lab(
    title="Lab 3｜災難性消去:同一個式子,兩種寫法",
    intro="觀念 10 的數值版本。兩個代數上完全相同的式子,在浮點數下的表現差了好幾個數量級。",
    code="""def direct(x):
    return (np.sqrt(1 + x) - 1) / x          # 含相近數相減 → 危險

def stable(x):
    return 1 / (np.sqrt(1 + x) + 1)          # 有理化後只剩加法 → 安全

xs = np.array([10.0**(-k) for k in range(1, 17)])
print(f"{'x':>8}  {'直接算':>20}  {'有理化':>20}")
for x in xs:
    print(f"{x:8.0e}  {direct(x):20.16f}  {stable(x):20.16f}")

err_d = np.abs(direct(xs) - stable(xs))
plt.loglog(xs, np.maximum(err_d, 1e-18), 'o-', label='|direct - stable|')
plt.gca().invert_xaxis()
plt.xlabel('x'); plt.ylabel('discrepancy'); plt.legend()
plt.title('Catastrophic cancellation in (sqrt(1+x)-1)/x')
plt.show()

print("\\nx = 1e-16 時 直接算 =", direct(1e-16), " 有理化 =", stable(1e-16))""",
    expected="x = 1e-16 時 直接算 = 0.0  有理化 = 0.5",
    seealso="直接算的版本在 $x\\approx10^{-12}$ 就開始掉精度,到 $10^{-16}$ 直接崩成 $0$;"
            "有理化的版本從頭到尾穩穩地給 $0.5$。",
    todo="""# TODO 學生練習:對 sqrt(x+1) - sqrt(x) 做同樣的比較(x 取 1e8, 1e12, 1e16)
# 穩定形式是 1 / (sqrt(x+1) + sqrt(x))
# 兩者在 x = 1e16 差多少?""")

LAB4 = Lab(
    title="Lab 4｜ε-δ 視覺化:把定義畫出來",
    intro="定義講完之後,用圖把「你給 ε、我找 δ」這件事演一遍。程式會自己找出可行的 δ 並畫框。",
    code="""# f(x) = 3x - 1, a = 2, L = 5。理論上 delta = eps / 3
f = lambda x: 3 * x - 1
a, L = 2.0, 5.0

def find_delta(eps, hi=2.0, tol=1e-12):
    \"\"\"二分搜尋:最大的 delta 使 |x-a|<delta 都滿足 |f(x)-L|<eps\"\"\"
    lo = 0.0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        xs = np.linspace(a - mid, a + mid, 400)
        if np.all(np.abs(f(xs) - L) < eps):
            lo = mid
        else:
            hi = mid
    return lo

for eps in [1.0, 0.5, 0.1, 0.01]:
    d = find_delta(eps)
    print(f"eps = {eps:5.2f}  ->  delta ~ {d:.6f}   (理論值 eps/3 = {eps/3:.6f})")

eps = 0.5
d = find_delta(eps)
xs = np.linspace(a - 1, a + 1, 400)
plt.plot(xs, f(xs), lw=2)
plt.axhspan(L - eps, L + eps, alpha=0.2, color='C2', label='y band: 2*eps')
plt.axvspan(a - d, a + d, alpha=0.2, color='C1', label='x window: 2*delta')
plt.plot([a], [L], 'ko')
plt.xlabel('x'); plt.ylabel('f(x)'); plt.legend()
plt.title('Give me eps, I return delta')
plt.show()""",
    expected="eps =  0.50  ->  delta ~ 0.166667   (理論值 eps/3 = 0.166667)",
    seealso="黃色直框(寬 $2\\delta$)裡的曲線,整段都落在綠色橫帶(高 $2\\varepsilon$)內。"
            "把 $\\varepsilon$ 調小,黃框跟著變窄——而且永遠找得到,這就是極限存在的意思。",
    todo="""# TODO 學生練習:把 f 換成 x**2、a 換成 1、L 換成 1
# 對 eps = 0.1,程式找到的 delta 是多少?
# 和你用 min{1, eps/3} 手算的保守估計比,哪個大?為什麼手算的比較小?""")

LABS = [LAB1, LAB2, LAB3, LAB4]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="銜接課教會他們「怎麼算」,這一週回答那個他們從沒問出口的問題:"
         "「越來越靠近」到底是什麼意思?順便告訴他們一件不安的事——電腦其實算不出極限。",
    fastforward=[
        ("極限的計算四招(代入/因式/有理化/比最高次)", "銜接課練過,是舊功夫", "診斷考確認,別重教"),
        ("$\\varepsilon$-$\\delta$ 的語意與圖像", "<strong>全新</strong>", "大力踩煞車"),
        ("由 $\\varepsilon$ 反推 $\\delta$(線性)", "<strong>全新</strong>,但有固定格式", "踩煞車,練到會寫"),
        ("單邊 / 無窮 / 趨向無窮的正式定義", "全新,但是同一句型的變奏", "中速,用對照表帶"),
        ("非線性的 $\\delta$(取 $\\min$ 的技巧)", "最難的一塊", "示範一次,不強求人人會"),
        ("連續的 $\\varepsilon$-$\\delta$ 版", "接得上銜接課的三條件", "中速"),
        ("浮點數、機器 epsilon、災難性消去", "全新,而且他們會很有感", "中速,留給實作課發酵"),
    ],
    outcomes=[
        "用自己的話說出 $\\varepsilon$ 與 $\\delta$ <strong>誰先出手</strong>,並在圖上指出橫帶與直框。",
        "對<strong>線性函數</strong>完整寫出一個 $\\varepsilon$-$\\delta$ 證明(先草稿反推、再正式順推)。",
        "說出極限定義與連續定義的<strong>兩處</strong>差異,並對應回三條件。",
        "舉出一個「數值表看起來收斂、實際極限不存在」的例子,並解釋表格為何不能當證明。",
        "解釋為什麼數值微分的 $h$ 不是越小越好,以及 $\\sqrt{\\varepsilon_{\\text{mach}}}$ 這個經驗法則從哪來。",
    ],
    clock=[
        ("00:00–00:15", "診斷考(銜接課範圍五題,當場收)", "—"),
        ("00:15–00:40", "檢討 + 決策樹回顧,校準本學期配速", "觀念 1"),
        ("00:40–01:00", "$\\varepsilon$-$\\delta$ 的語意:挑戰與回應", "觀念 2"),
        ("01:00–01:05", "休息", "—"),
        ("01:05–01:40", "<strong>證明時刻</strong>:由 $\\varepsilon$ 反推 $\\delta$", "觀念 3"),
        ("01:40–02:05", "為什麼需要定義 + 單邊/無窮/趨向無窮", "觀念 4–7"),
        ("02:05–02:10", "休息", "—"),
        ("02:10–02:35", "用正式定義看連續(含取 $\\min$ 的技巧)", "觀念 8"),
        ("02:35–02:55", "浮點數現實與災難性消去", "觀念 9–10"),
        ("02:55–03:00", "收尾,接到實作課", "—"),
    ],
    proof_moment="用 $\\varepsilon$-$\\delta$ 證明 $\\displaystyle\\lim_{x\\to2}(3x-1)=5$——"
                 "重點不是這個結論(誰都知道它對),而是<strong>兩欄書寫格式</strong>:"
                 "左欄草稿反推出 $\\delta=\\frac{\\varepsilon}{3}$,右欄正式順推。"
                 "這個格式整學期只教這一次,後面十七週都靠它。",
    script=[
        ("開場:先考再說(15 分)",
         "<p>不要先講話,直接發診斷考。五題,銜接課範圍,15 分鐘,當場收。"
         "題目就用觀念 1 的示範與練習那四題再加一題分段函數連續。</p>"
         "<p><strong>為什麼要考</strong>:你需要知道這班暑假到底留下了多少。"
         "後面十七週的配速全靠這一次校準——考完你會知道該不該在積分技巧多留兩週。</p>"
         "<div class='callout tip'><div class='ico'>🔑</div><div><span class='c-title'>貼牆金句</span>"
         "<p>這學期不再問「怎麼算」,開始問「<strong>為什麼這樣算是對的</strong>」。</p></div></div>"),
        ("$\\varepsilon$-$\\delta$:一場挑戰與回應的遊戲(20 分)",
         "<p>千萬別直接把定義寫上黑板。先玩遊戲:</p>"
         "<p>「我說 $\\displaystyle\\lim_{x\\to2}(3x-1)=5$。你不信?那你出招——你要 $f(x)$ 離 $5$ 多近?」"
         "學生說「$0.1$」。你就在黑板上算:「那我把 $x$ 限制在離 $2$ 不到 $0.0333$ 的範圍,達標。」"
         "再讓他說 $0.01$、$0.001$,你每次都答得出來。</p>"
         "<p>玩三輪之後問:「如果我<strong>每一次</strong>都答得出來,是不是就證明了極限是 $5$?」"
         "——這就是定義。這時候再把符號寫上去,學生看到的是遊戲規則,不是天書。</p>"
         "<p>幾何圖一定要畫:$y$ 軸上的橫帶(高 $2\\varepsilon$)、$x$ 軸上的直框(寬 $2\\delta$)。"
         "實作課 Lab 4 會把這張圖跑出來。</p>"),
        ("證明時刻:反推的兩欄格式(35 分)",
         "<p>黑板切兩欄,左邊寫「草稿·怎麼想到的」,右邊寫「正式·為什麼對」。</p>"
         "<p><strong>左欄</strong>:從結論倒推。$|(3x-1)-5|=3|x-2|&lt;\\varepsilon$,"
         "所以 $|x-2|&lt;\\frac{\\varepsilon}{3}$。$\\delta$ 自己掉出來了。</p>"
         "<p><strong>右欄</strong>:「給定 $\\varepsilon&gt;0$,取 $\\delta=\\frac{\\varepsilon}{3}$。"
         "若 $0&lt;|x-2|&lt;\\delta$,則 $|(3x-1)-5|=3|x-2|&lt;3\\delta=\\varepsilon$。」</p>"
         "<p>強調<strong>方向</strong>:草稿是反推、正式是順推。學生最常犯的錯就是把草稿當答案交上來。"
         "讓他們當場練 $\\lim_{x\\to1}(2x+3)=5$,巡堂看誰把順序寫反。</p>"
         "<p>行有餘力再示範 $f(x)=x^2$ 的取 $\\min$ 手法,但<strong>不要求人人會</strong>——"
         "考卷只考線性的。</p>"),
        ("為什麼非要這麼囉唆(10 分)",
         "<p>這段是說服。學生心裡在想「代幾個數不就好了」。給他們 $\\sin\\frac{\\pi}{x}$:</p>"
         "<p>「$x=1,\\frac12,\\frac13,\\frac14$,函數值全是 $0$。表格說極限是 $0$。」停三秒。"
         "「但 $x=\\frac25$ 呢?$\\sin\\frac{5\\pi}{2}=1$。」</p>"
         "<p>結論送給他們:<strong>表格只能否證,不能證明</strong>。這句話一講完,"
         "前面 35 分鐘的囉唆就有了意義。</p>"),
        ("三個變奏:單邊、無窮、趨向無窮(15 分)",
         "<p>用對照表一次帶完,不要各講一遍。表格見教師版觀念 7 的原理區塊:"
         "挑戰只有 $\\varepsilon$ 或 $M$ 兩種,回應只有 $\\delta$ 或 $N$ 兩種,四種組合而已。</p>"
         "<p>重點提醒:$\\lim f=\\infty$ 是<strong>簡寫</strong>,嚴格說極限不存在。"
         "整句定義裡從來沒有把 $f(x)$ 和 $\\infty$ 相減——因為 $\\infty$ 不是數字。</p>"),
        ("連續:只差兩個符號(25 分)",
         "<p>把極限定義和連續定義上下並排,圈出兩處差異:$0&lt;$ 不見了、$L$ 變成 $f(a)$。</p>"
         "<p>然後把這兩處對應回銜接課的三條件——學生會發現「三條件」根本就是這一行不等式拆開講。"
         "這是本週最有「原來如此」感的一刻,別趕。</p>"
         "<p>取 $\\min$ 的技巧在這裡示範 $f(x)=x^2$ 在 $a=1$:先壓 $\\delta\\le1$ 讓 $|x+1|&lt;3$,"
         "再取 $\\delta=\\min\\{1,\\frac{\\varepsilon}{3}\\}$。</p>"),
        ("浮點數:電腦算不出極限(20 分)",
         "<p>收尾用一個會讓他們坐直的問題:「$1+10^{-20}$ 在電腦裡等於多少?」</p>"
         "<p>答案是 $1$。所以 $\\frac{(1+h)^2-1}{h}$ 在 $h=10^{-20}$ 算出來是 $0$,不是 $2$。"
         "而且不會報錯,安靜地給你一個錯答案。</p>"
         "<p>接著給災難性消去:$\\frac{\\sqrt{1+x}-1}{x}$ 直接算 vs 有理化算。"
         "點出那個漂亮的呼應——<strong>銜接課學有理化是為了消 $\\frac00$,"
         "現在同一招用來消數值不穩定</strong>。</p>"
         "<p>預告實作課會把這兩件事都跑出來、畫出來,那條 V 字形誤差曲線他們會印象深刻。</p>"),
    ],
    myths=[
        "把 $\\varepsilon$ 和 $\\delta$ 的順序搞反,變成「先給 $\\delta$ 再找 $\\varepsilon$」。",
        "把草稿(反推)當成證明交出去,沒有寫成「取 $\\delta=\\cdots$,則……」的順推格式。",
        "把 $0&lt;|x-a|$ 寫成 $|x-a|$,無意間變成連續的定義。",
        "以為 $\\lim f=\\infty$ 代表極限「存在且等於無窮」——$\\infty$ 不是數字。",
        "用數值表「證明」極限存在。表格只能否證。",
        "以為數值微分的 $h$ 越小越準。過了 $\\sqrt{\\varepsilon_{\\text{mach}}}$ 就開始變爛。",
        "以為代數等價就數值等價。浮點數下式子怎麼寫直接決定準不準。",
    ],
    exit_check=[
        ("$\\displaystyle\\lim_{x\\to3}(4x+2)=14$,請寫出 $\\delta$ 該取多少(用 $\\varepsilon$ 表示)。",
         "$|(4x+2)-14|=4|x-3|&lt;\\varepsilon \\Rightarrow \\delta=\\dfrac{\\varepsilon}{4}$。"),
        ("極限的定義與連續的定義,差在哪兩個地方?",
         "(1) 連續是 $|x-a|&lt;\\delta$,沒有 $0&lt;$,故含 $x=a$;(2) 目標值指定為 $f(a)$ 而非任意 $L$。"),
        ("為什麼 $h$ 取 $10^{-20}$ 算出來的導數是 $0$?",
         "$10^{-20}$ 小於 $1$ 附近的浮點間距 $2.2\\times10^{-16}$,$x+h$ 捨入回 $x$,分子恰為 $0$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W1-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "觀念 3 的三題一定要寫成完整的兩欄格式。",
        "<strong>預習</strong>:本書第 12 章「導數」段落——下週我們把反函數與雙曲函數補進來。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 lim (x^2-9)/(x^2-2x-3) at 3", "limit((x**2-9)/(x**2-2*x-3), x, 3)", "Rational(3,2)"),
    ("C1 D1 lim (4x^2-x)/(3x^2+5) at oo", "limit((4*x**2-x)/(3*x**2+5), x, oo)", "Rational(4,3)"),
    ("C1 D2 lim (sqrt(9+x)-3)/x at 0", "limit((sqrt(9+x)-3)/x, x, 0)", "Rational(1,6)"),
    ("C1 D3 lim sqrt(x^2+4x)-x at oo", "limit(sqrt(x**2+4*x)-x, x, oo)", "2"),
    # δ/N 的檢查一律寫成「把答案代回原不等式的臨界式」,避免 solve() 回傳順序造成的脆弱
    ("C3 示範 delta=eps/3 代回 3*delta 應得 eps", "3*(eps/3)", "eps"),
    ("C3 D1 delta=eps/2 代回 2*delta 應得 eps", "2*(eps/2)", "eps"),
    ("C3 D3 eps=0.01 時 delta = 1/700", "Rational(1,100)/7", "Rational(1,700)"),
    ("C4 sin(pi/x) at x=1/2 是 0", "sin(pi/Rational(1,2))", "0"),
    ("C4 sin(pi/x) at x=2/5 是 1", "sin(pi/Rational(2,5))", "1"),
    ("C4 D1 x=2/(4n+1) 時 sin(pi/x)=1", "simplify(sin(pi*(4*n+1)/2))", "1"),
    ("C4 D3 lim x*sin(pi/x) at 0", "limit(x*sin(pi/x), x, 0)", "0"),
    ("C5 D3 delta=eps^2 代回 sqrt(delta) 應得 eps", "sqrt(eps**2)", "eps"),
    ("C6 示範 delta=1/sqrt(M) 代回 1/delta^2 應得 M", "1/(1/sqrt(M))**2", "M"),
    ("C7 示範 N=1/eps 代回 1/N 應得 eps", "1/(1/eps)", "eps"),
    ("C7 D1 N=1/sqrt(eps) 代回 1/N^2 應得 eps", "1/(1/sqrt(eps))**2", "eps"),
    ("C7 D2 |(3x+1)/x - 3| = 1/x", "simplify((3*x+1)/x - 3)", "1/x"),
    ("C8 D2 delta = 0.01/3 = 1/300", "Rational(1,100)/3", "Rational(1,300)"),
    ("C10 D1 lim (sqrt(1+x)-1)/x at 0", "limit((sqrt(1+x)-1)/x, x, 0)", "Rational(1,2)"),
    ("C10 D2 穩定形式等價", "sqrt(x+1)-sqrt(x) - 1/(sqrt(x+1)+sqrt(x))", "0"),
    ("C10 D3 1-cos x = 2 sin^2(x/2)", "simplify(1-cos(x) - 2*sin(x/2)**2)", "0"),
]

WEEK = Week(
    num=1,
    title="極限的嚴格定義與浮點數現實",
    subtitle="銜接課教「怎麼算」,這一週回答「越來越靠近到底是什麼意思」——"
             "並且揭穿一件不安的事:電腦其實算不出真正的極限。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["學期地基"],
)
