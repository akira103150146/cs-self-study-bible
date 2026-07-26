# -*- coding: utf-8 -*-
"""第 6 週｜部分分式分解

積分技巧最後一招:有理函數。核心動作是把一個分母複雜的分式,
拆成一堆分母簡單的分式之和 —— 而「拆」這件事本質上是解線性方程組,
這是線性代數的第一個伏筆。
證明時刻:為什麼任何真分式都拆得開(分解定理的直覺與可行性)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Why Partial Fractions", title_zh="為什麼要拆",
    sub="You can integrate 1/(x−a). You cannot integrate a messy quotient directly.",
    idea="$\\displaystyle\\int\\frac{dx}{x-a}=\\ln|x-a|+C$ is easy; "
         "$\\displaystyle\\int\\frac{dx}{x^{2}-1}$ is not obvious. But "
         "$\\frac{1}{x^{2}-1}=\\frac{1/2}{x-1}-\\frac{1/2}{x+1}$ — and suddenly it is two easy "
         "integrals. Partial fractions is the art of finding that decomposition.",
    deep="<p><strong>動機先講清楚</strong>,不然學生會覺得這是無聊的代數練習。</p>"
         "<p class='step'>你已經會積 $\\dfrac{1}{x-a}$、$\\dfrac{1}{(x-a)^{n}}$、"
         "$\\dfrac{1}{x^{2}+a^{2}}$ 這三種簡單分式。</p>"
         "<p class='step'>問題是 $\\dfrac{3x+5}{(x-1)(x+2)}$ 這種——分母一複雜就卡住。</p>"
         "<p class='step'><strong>策略:把難的拆成幾個簡單的和</strong>。"
         "拆完之後逐項積,每一項都是你會的。</p>"
         "<p><strong>先驗證方向是對的</strong>。給學生 $\\dfrac{1}{2(x-1)}-\\dfrac{1}{2(x+1)}$,"
         "叫他們通分回去:</p>"
         "$$\\frac{(x+1)-(x-1)}{2(x-1)(x+1)}=\\frac{2}{2\\left(x^{2}-1\\right)}=\\frac{1}{x^{2}-1}.$$"
         "<p>「所以確實拆得開。問題只剩:<strong>怎麼找到那兩個係數</strong>?」"
         "這個順序(先驗證可行、再學方法)比直接教步驟有效得多。</p>"
         "<p><strong>兩個前提條件</strong>,先講在前面:</p>"
         "<ul>"
         "<li><strong>必須是真分式</strong>(分子次數 &lt; 分母次數)。否則先長除(觀念 6)。</li>"
         "<li><strong>分母要先因式分解</strong>。拆的形式完全由分母的因式決定。</li>"
         "</ul><span class='qed'>∎</span>",
    guide=["你會積 $\\dfrac{1}{x-1}$ 嗎?答案是 <span class=\"blank\"></span>。",
           "那 $\\dfrac{1}{x^{2}-1}$ 呢?直覺上會不會是 $\\ln|x^{2}-1|$?"
           "(微分回去檢查看看)",
           "把 $\\dfrac{1/2}{x-1}-\\dfrac{1/2}{x+1}$ 通分,你會得到 <span class=\"blank\"></span>。",
           "所以策略是什麼?拆完之後每一項都會積了嗎?"],
    demo="Verify that $\\dfrac{1}{x^{2}-1}=\\dfrac{1/2}{x-1}-\\dfrac{1/2}{x+1}$, then use it to "
         "evaluate $\\displaystyle\\int\\frac{dx}{x^{2}-1}$.",
    demo_sol="<p><strong>驗證</strong>(通分回去):</p>"
             "$$\\frac{1/2}{x-1}-\\frac{1/2}{x+1}=\\frac{(x+1)-(x-1)}{2(x-1)(x+1)}"
             "=\\frac{2}{2\\left(x^{2}-1\\right)}=\\frac{1}{x^{2}-1}.\\ \\checkmark$$"
             "<p><strong>積分</strong>,逐項處理:</p>"
             "$$\\int\\frac{dx}{x^{2}-1}=\\frac12\\ln|x-1|-\\frac12\\ln|x+1|+C"
             "=\\frac12\\ln\\left|\\frac{x-1}{x+1}\\right|+C.$$"
             "<p>注意<strong>不是</strong> $\\ln\\left|x^{2}-1\\right|$——"
             "微分回去會多出一個 $2x$,差很多。</p>",
    demo_hint="先通分驗證那個分解是對的,再逐項積分。",
    misstep="以為 $\\displaystyle\\int\\frac{dx}{x^{2}-1}=\\ln\\left|x^{2}-1\\right|+C$。"
            "微分回去是 $\\dfrac{2x}{x^{2}-1}$,多了 $2x$。",
    level="basic",
    drills=[
        ("Verify that $\\dfrac{1}{x(x+1)}=\\dfrac1x-\\dfrac{1}{x+1}$.",
         "<p>通分:$\\dfrac{(x+1)-x}{x(x+1)}=\\dfrac{1}{x(x+1)}$ ✓</p>"),
        ("Use the previous decomposition to evaluate "
         "$\\displaystyle\\int\\frac{dx}{x(x+1)}$.",
         "<p>$\\ln|x|-\\ln|x+1|+C=\\ln\\left|\\dfrac{x}{x+1}\\right|+C$。</p>"),
        ("Why can $\\displaystyle\\int\\frac{dx}{x^{2}+1}$ not be handled by partial fractions "
         "over the reals?",
         "<p>因為 $x^{2}+1$ 在實數範圍<strong>不可分解</strong>(判別式 $&lt;0$)。"
         "它本身就是最簡形式,答案是 $\\arctan x+C$。</p>"),
    ])

C2 = Concept(
    title_en="Distinct Linear Factors", title_zh="相異一次因式",
    sub="One term per factor — then match coefficients",
    idea="If the denominator factors into distinct linear factors, write "
         "$$\\frac{P(x)}{(x-a)(x-b)}=\\frac{A}{x-a}+\\frac{B}{x-b},$$ "
         "clear denominators, and solve for $A,B$ by matching coefficients or substituting "
         "convenient values of $x$.",
    deep="<p><strong>形式由分母決定</strong>:每一個相異的一次因式,配一個常數分子。</p>"
         "<p class='step'><strong>步驟</strong>:①寫出待定形式 ②兩邊乘上分母(清分母)"
         "③解出未知數。</p>"
         "<p>以 $\\dfrac{3x+5}{(x-1)(x+2)}=\\dfrac{A}{x-1}+\\dfrac{B}{x+2}$ 為例,清分母得</p>"
         "$$3x+5=A(x+2)+B(x-1).$$"
         "<p><strong>解法有兩種,都要會</strong>:</p>"
         "<ul>"
         "<li><strong>代特殊值</strong>(快):令 $x=1$ 得 $8=3A$,故 $A=\\frac83$;"
         "令 $x=-2$ 得 $-1=-3B$,故 $B=\\frac13$。"
         "<em>選的值就是讓某個因式歸零的那些根</em>。</li>"
         "<li><strong>比較係數</strong>(通用):展開右邊得 $(A+B)x+(2A-B)$,"
         "對照左邊 $3x+5$ 得聯立 $A+B=3$、$2A-B=5$,解得同樣答案。</li>"
         "</ul>"
         "<p><strong>什麼時候該用哪種</strong>:相異一次因式用代值最快;"
         "遇到重根或不可約二次(觀念 4、5),代值只能解出部分,剩下的還是要比較係數。"
         "所以<strong>兩種都要熟</strong>。</p>"
         "<p>比較係數的本質是<strong>解線性方程組</strong>——觀念 7 會把這件事講透,"
         "那也是線性代數的入口。<span class='qed'>∎</span></p>",
    guide=["分母是 $(x-1)(x+2)$,兩個相異一次因式。所以待定形式要寫成 $\\dfrac{A}{?}+\\dfrac{B}{?}$,"
           "分母各填什麼?",
           "兩邊乘上 $(x-1)(x+2)$ 清分母,得 $3x+5=$ <span class=\"blank\"></span>。",
           "令 $x=1$(讓 $B$ 那項歸零),得 $A=$ <span class=\"blank\"></span>。"
           "再令 $x=-2$ 求 $B$。",
           "另一條路:展開右邊比較 $x$ 的係數與常數項,列出聯立。答案一樣嗎?"],
    demo="Decompose $\\dfrac{3x+5}{(x-1)(x+2)}$ and evaluate its integral.",
    demo_sol="<p>設 $\\dfrac{3x+5}{(x-1)(x+2)}=\\dfrac{A}{x-1}+\\dfrac{B}{x+2}$,清分母:</p>"
             "$$3x+5=A(x+2)+B(x-1).$$"
             "<p><strong>代值</strong>:$x=1\\Rightarrow 8=3A\\Rightarrow A=\\dfrac83$;"
             "$x=-2\\Rightarrow-1=-3B\\Rightarrow B=\\dfrac13$。</p>"
             "$$\\frac{3x+5}{(x-1)(x+2)}=\\frac{8}{3(x-1)}+\\frac{1}{3(x+2)}.$$"
             "<p>逐項積分:</p>"
             "$$\\int\\frac{3x+5}{(x-1)(x+2)}dx=\\frac83\\ln|x-1|+\\frac13\\ln|x+2|+C.$$",
    demo_hint="代入讓某個因式歸零的 $x$ 值,一次解一個未知數。",
    misstep="清分母後忘了乘完整:$A$ 要乘 $(x+2)$、$B$ 要乘 $(x-1)$,"
            "<strong>各自乘的是「另一個」因式</strong>。",
    level="mid",
    drills=[
        ("Decompose $\\dfrac{1}{x(x+1)}$.",
         "<p>$\\dfrac{A}{x}+\\dfrac{B}{x+1}$,清分母 $1=A(x+1)+Bx$。"
         "$x=0\\Rightarrow A=1$;$x=-1\\Rightarrow B=-1$。故 $\\dfrac1x-\\dfrac{1}{x+1}$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{dx}{x^{2}-4}$.",
         "<p>$\\dfrac{1}{(x-2)(x+2)}=\\dfrac{1/4}{x-2}-\\dfrac{1/4}{x+2}$,"
         "積分得 $\\dfrac14\\ln\\left|\\dfrac{x-2}{x+2}\\right|+C$。</p>"),
        ("Evaluate $\\displaystyle\\int_{2}^{3}\\frac{dx}{x^{2}-1}$.",
         "<p>$\\Big[\\dfrac12\\ln\\left|\\dfrac{x-1}{x+1}\\right|\\Big]_{2}^{3}"
         "=\\dfrac12\\left(\\ln\\dfrac12-\\ln\\dfrac13\\right)=\\dfrac12\\ln\\dfrac32$。</p>"),
    ])

C3 = Concept(
    title_en="The Cover-Up Method", title_zh="遮蓋法",
    sub="Cover the factor, plug in its root — the coefficient falls out",
    idea="For a distinct linear factor $(x-a)$, its coefficient is obtained by covering that "
         "factor in the denominator and evaluating what remains at $x=a$. It is the "
         "substitution trick, done mentally.",
    deep="<p>遮蓋法是觀念 2「代值法」的<strong>心算版</strong>,考試時能省下大量時間。</p>"
         "<p class='step'><strong>做法</strong>:要求 $(x-a)$ 對應的係數,就用手<strong>遮住</strong> "
         "分母裡的 $(x-a)$,把 $x=a$ 代進<strong>剩下的部分</strong>。</p>"
         "<p>例:$\\dfrac{3x+5}{(x-1)(x+2)}$。求 $A$(對應 $x-1$):遮住 $(x-1)$,"
         "剩下 $\\dfrac{3x+5}{x+2}$,代 $x=1$ 得 $\\dfrac{8}{3}$。<strong>三秒鐘</strong>。</p>"
         "<p>求 $B$:遮住 $(x+2)$,剩下 $\\dfrac{3x+5}{x-1}$,代 $x=-2$ 得 "
         "$\\dfrac{-1}{-3}=\\dfrac13$。</p>"
         "<p><strong>為什麼有效</strong>(值得講,不然像魔術):清分母後的式子是</p>"
         "$$P(x)=A(x+2)+B(x-1).$$"
         "<p>代 $x=1$ 時 $B$ 那項自動歸零,只剩 $A\\cdot(1+2)$——"
         "而 $(1+2)$ 正是「遮住 $(x-1)$ 之後剩下的分母」在 $x=1$ 的值。"
         "所以遮蓋法就是把這個過程壓縮成一步。</p>"
         "<p><strong>限制</strong>:只對<strong>相異一次因式</strong>有效。"
         "重根的最高次項可以用(觀念 4),但低次項不行;不可約二次完全不能用。"
         "<span class='qed'>∎</span></p>",
    guide=["要求 $\\dfrac{3x+5}{(x-1)(x+2)}$ 裡 $\\dfrac{A}{x-1}$ 的 $A$,把分母的 "
           "<span class=\"blank\"></span> 遮住。",
           "剩下 $\\dfrac{3x+5}{x+2}$,代 $x=$ <span class=\"blank\"></span>,得 "
           "<span class=\"blank\"></span>。",
           "同樣手法求 $B$:遮住 $(x+2)$,代 $x=-2$,得多少?",
           "為什麼這樣做是對的?(想:清分母後代 $x=1$,$B$ 那一項會怎樣)"],
    demo="Use the cover-up method to decompose $\\dfrac{x+7}{(x-2)(x+3)}$.",
    demo_sol="<p><strong>求 $x-2$ 的係數</strong>:遮住 $(x-2)$,剩 $\\dfrac{x+7}{x+3}$,"
             "代 $x=2$:$\\dfrac{9}{5}$。</p>"
             "<p><strong>求 $x+3$ 的係數</strong>:遮住 $(x+3)$,剩 $\\dfrac{x+7}{x-2}$,"
             "代 $x=-3$:$\\dfrac{4}{-5}=-\\dfrac45$。</p>"
             "$$\\frac{x+7}{(x-2)(x+3)}=\\frac{9}{5(x-2)}-\\frac{4}{5(x+3)}.$$"
             "<p><strong>驗算</strong>(通分):$\\dfrac{9(x+3)-4(x-2)}{5(x-2)(x+3)}"
             "=\\dfrac{5x+35}{5(x-2)(x+3)}=\\dfrac{x+7}{(x-2)(x+3)}$ ✓</p>",
    demo_hint="遮住要求的那個因式,把它的根代進剩下的式子。",
    misstep="對重根或不可約二次用遮蓋法。它只保證對<strong>相異一次因式</strong>有效。",
    level="mid",
    drills=[
        ("Use cover-up to decompose $\\dfrac{5}{(x-1)(x-4)}$.",
         "<p>$x=1$:$\\dfrac{5}{1-4}=-\\dfrac53$;$x=4$:$\\dfrac{5}{4-1}=\\dfrac53$。"
         "故 $-\\dfrac{5}{3(x-1)}+\\dfrac{5}{3(x-4)}$。</p>"),
        ("Use cover-up to decompose $\\dfrac{2x}{(x+1)(x-3)}$.",
         "<p>$x=-1$:$\\dfrac{-2}{-4}=\\dfrac12$;$x=3$:$\\dfrac{6}{4}=\\dfrac32$。"
         "故 $\\dfrac{1}{2(x+1)}+\\dfrac{3}{2(x-3)}$。</p>"),
        ("Explain why cover-up fails for the $\\dfrac{B}{x-1}$ term in "
         "$\\dfrac{P(x)}{(x-1)^{2}(x+1)}$.",
         "<p>清分母後 $B$ 那一項會乘上 $(x-1)$,代 $x=1$ 時它<strong>也</strong>歸零,"
         "所以代值只能求出 $(x-1)^{2}$ 的係數,$B$ 求不出來,要靠比較係數。</p>"),
    ])

C4 = Concept(
    title_en="Repeated Linear Factors", title_zh="重複的一次因式",
    sub="A factor of multiplicity k needs k terms, one for each power",
    idea="For $(x-a)^{k}$ in the denominator, the decomposition needs all $k$ terms: "
         "$$\\frac{A_{1}}{x-a}+\\frac{A_{2}}{(x-a)^{2}}+\\cdots+\\frac{A_{k}}{(x-a)^{k}}.$$ "
         "Omitting the lower powers makes the system unsolvable.",
    deep="<p>學生最常犯的錯:$(x-1)^{2}$ 只寫一項 $\\dfrac{A}{(x-1)^{2}}$。"
         "<strong>這樣一定解不出來</strong>,而且很多人會卡到懷疑人生。</p>"
         "<p><strong>為什麼需要全部 $k$ 項</strong>:數一數自由度。"
         "分母 $(x-a)^{k}$ 的真分式,分子最多 $k-1$ 次,有 $k$ 個自由係數。"
         "所以拆開後也<strong>必須有 $k$ 個</strong>待定係數,少一個就湊不出所有可能的分子。</p>"
         "<p class='step'><strong>示範</strong>:$\\dfrac{x^{2}+1}{x(x-1)^{2}}"
         "=\\dfrac{A}{x}+\\dfrac{B}{x-1}+\\dfrac{C}{(x-1)^{2}}$。清分母:</p>"
         "$$x^{2}+1=A(x-1)^{2}+Bx(x-1)+Cx.$$"
         "<p class='step'>代 $x=0$:$1=A$。代 $x=1$:$2=C$。"
         "$B$ 代值求不出來(兩個特殊值都用完了),比較 $x^{2}$ 係數:$1=A+B$,故 $B=0$。</p>"
         "$$\\frac{x^{2}+1}{x(x-1)^{2}}=\\frac1x+\\frac{2}{(x-1)^{2}}.$$"
         "<p><strong>$B=0$ 這件事很有教育意義</strong>:"
         "「那我一開始不寫 $B$ 不就好了?」——不行,因為你<strong>事前不知道它是零</strong>。"
         "寫完整、解出來發現是零,和一開始就漏掉,是兩回事。</p>"
         "<p><strong>積分時注意</strong>:$\\dfrac{1}{(x-a)^{2}}$ 積出來是 "
         "$-\\dfrac{1}{x-a}$,<strong>不是對數</strong>。只有一次方才給對數。"
         "<span class='qed'>∎</span></p>",
    guide=["分母有 $(x-1)^{2}$。如果只寫一項 $\\dfrac{C}{(x-1)^{2}}$,自由度夠嗎?"
           "(分子最多幾次?有幾個係數?)",
           "所以要寫幾項?分別是 $\\dfrac{B}{?}$ 和 $\\dfrac{C}{?}$。",
           "清分母後代 $x=1$,只有哪一項活下來?所以能求出哪個係數?",
           "$B$ 要怎麼求?(提示:比較某個次方的係數)"],
    demo="Decompose $\\dfrac{x^{2}+1}{x(x-1)^{2}}$.",
    demo_sol="<p>設 $\\dfrac{x^{2}+1}{x(x-1)^{2}}=\\dfrac{A}{x}+\\dfrac{B}{x-1}"
             "+\\dfrac{C}{(x-1)^{2}}$,清分母:</p>"
             "$$x^{2}+1=A(x-1)^{2}+Bx(x-1)+Cx.$$"
             "<p><strong>代值</strong>:$x=0\\Rightarrow 1=A$;$x=1\\Rightarrow 2=C$。</p>"
             "<p><strong>比較係數求 $B$</strong>:右邊 $x^{2}$ 的係數是 $A+B$,左邊是 $1$,"
             "故 $B=1-A=0$。</p>"
             "$$\\frac{x^{2}+1}{x(x-1)^{2}}=\\frac1x+\\frac{2}{(x-1)^{2}}.$$"
             "<p>$B$ 恰好是零——但<strong>不寫它就解不出來</strong>,因為你事前不知道。</p>",
    demo_hint="$(x-1)^{2}$ 要寫兩項。代值能求兩個,剩下的比較係數。",
    misstep="$(x-a)^{k}$ 只寫最高次那一項。少了低次項,聯立方程組會無解。",
    level="hard",
    drills=[
        ("Decompose $\\dfrac{1}{x(x+1)^{2}}$.",
         "<p>$\\dfrac{A}{x}+\\dfrac{B}{x+1}+\\dfrac{C}{(x+1)^{2}}$,清分母 "
         "$1=A(x+1)^{2}+Bx(x+1)+Cx$。$x=0\\Rightarrow A=1$;$x=-1\\Rightarrow C=-1$;"
         "比較 $x^{2}$:$0=A+B\\Rightarrow B=-1$。故 $\\dfrac1x-\\dfrac{1}{x+1}"
         "-\\dfrac{1}{(x+1)^{2}}$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{dx}{(x-1)^{2}}$.",
         "<p>$-\\dfrac{1}{x-1}+C$。<strong>不是</strong>對數——只有一次方才給對數。</p>"),
        ("How many undetermined coefficients does "
         "$\\dfrac{P(x)}{(x-1)^{3}(x+2)}$ require?",
         "<p>四個:$(x-1)$ 的三次重根貢獻 $3$ 個(一次、二次、三次方各一),"
         "$(x+2)$ 貢獻 $1$ 個。總共 $4$,恰等於分母的次數。</p>"),
    ])

C5 = Concept(
    title_en="Irreducible Quadratic Factors", title_zh="不可約的二次因式",
    sub="A quadratic that will not factor gets a linear numerator Ax + B",
    idea="For an irreducible quadratic $x^{2}+px+q$ (discriminant $&lt;0$), the corresponding term "
         "is $\\dfrac{Ax+B}{x^{2}+px+q}$ — a <em>linear</em> numerator, not a constant. Its "
         "integral splits into a logarithm plus an arctangent.",
    deep="<p><strong>為什麼分子是一次而不是常數</strong>:還是數自由度。"
         "分母二次的真分式,分子最多一次,有<strong>兩個</strong>自由係數,"
         "所以分子必須寫成 $Ax+B$。</p>"
         "<p class='step'><strong>怎麼判斷不可約</strong>:判別式 $p^{2}-4q&lt;0$。"
         "例如 $x^{2}+1$($-4&lt;0$)、$x^{2}+x+1$($1-4&lt;0$)都是。</p>"
         "<p class='step'><strong>積分怎麼處理</strong>:把分子拆成「分母的導數」加「常數」。"
         "以 $\\dfrac{Ax+B}{x^{2}+a^{2}}$ 為例:</p>"
         "$$\\int\\frac{Ax+B}{x^{2}+a^{2}}dx"
         "=\\underbrace{\\frac{A}{2}\\ln\\left(x^{2}+a^{2}\\right)}_{\\text{換元 }t=x^{2}+a^{2}}"
         "+\\underbrace{\\frac{B}{a}\\arctan\\frac{x}{a}}_{\\text{標準公式}}+C.$$"
         "<p><strong>兩個零件、兩種招式</strong>:$x$ 的部分用換元(因為 $x\\,dx$ 是 "
         "$d(x^{2})$ 的一半),常數的部分套 arctan 公式。"
         "<strong>看到 $Ax+B$ 就想「拆成兩塊分開處理」</strong>。</p>"
         "<p class='step'><strong>示範</strong>:$\\dfrac{1}{x^{3}+x}=\\dfrac{1}{x(x^{2}+1)}"
         "=\\dfrac{A}{x}+\\dfrac{Bx+C}{x^{2}+1}$。清分母 $1=A(x^{2}+1)+(Bx+C)x$。"
         "$x=0\\Rightarrow A=1$;比較 $x^{2}$:$0=A+B\\Rightarrow B=-1$;"
         "比較 $x$:$0=C$。得 $\\dfrac1x-\\dfrac{x}{x^{2}+1}$。</p>"
         "<p>若分母是 $(x^{2}+px+q)$ 但 $p\\ne0$,先<strong>配方</strong>(W5 學過)"
         "再套 arctan。兩週的技巧又接上了。<span class='qed'>∎</span></p>",
    guide=["$x^{2}+1$ 在實數範圍能不能因式分解?判別式是多少?",
           "分母是二次的真分式,分子最多幾次?所以有幾個自由係數?"
           "分子要寫成 <span class=\"blank\"></span>。",
           "$\\displaystyle\\int\\dfrac{x}{x^{2}+1}dx$ 用哪一招?"
           "($x\\,dx$ 和 $d(x^{2}+1)$ 差幾倍)",
           "$\\displaystyle\\int\\dfrac{1}{x^{2}+1}dx$ 呢?答案是 <span class=\"blank\"></span>。"],
    demo="Decompose $\\dfrac{1}{x^{3}+x}$ and evaluate "
         "$\\displaystyle\\int\\frac{dx}{x^{3}+x}$.",
    demo_sol="<p>分母 $x^{3}+x=x\\left(x^{2}+1\\right)$,其中 $x^{2}+1$ 不可約。設</p>"
             "$$\\frac{1}{x\\left(x^{2}+1\\right)}=\\frac{A}{x}+\\frac{Bx+C}{x^{2}+1}.$$"
             "<p>清分母:$1=A\\left(x^{2}+1\\right)+(Bx+C)x$。"
             "$x=0\\Rightarrow A=1$;比較 $x^{2}$ 係數:$0=A+B\\Rightarrow B=-1$;"
             "比較 $x$ 係數:$0=C$。</p>"
             "$$\\frac{1}{x^{3}+x}=\\frac1x-\\frac{x}{x^{2}+1}.$$"
             "<p>積分(第二項用換元 $t=x^{2}+1$):</p>"
             "$$\\int\\frac{dx}{x^{3}+x}=\\ln|x|-\\frac12\\ln\\left(x^{2}+1\\right)+C"
             "=\\ln\\frac{|x|}{\\sqrt{x^{2}+1}}+C.$$",
    demo_hint="不可約二次的分子要寫 $Bx+C$。積分時 $x$ 的部分用換元、常數部分套 arctan。",
    misstep="不可約二次的分子只寫一個常數。自由度不夠,一定解不出來。",
    level="hard",
    drills=[
        ("Decompose $\\dfrac{1}{x\\left(x^{2}+4\\right)}$.",
         "<p>$\\dfrac{A}{x}+\\dfrac{Bx+C}{x^{2}+4}$:$A=\\dfrac14$、$B=-\\dfrac14$、$C=0$。"
         "故 $\\dfrac{1}{4x}-\\dfrac{x}{4\\left(x^{2}+4\\right)}$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{2x+3}{x^{2}+1}\\,dx$.",
         "<p>拆兩塊:$\\displaystyle\\int\\dfrac{2x}{x^{2}+1}dx+3\\int\\dfrac{dx}{x^{2}+1}"
         "=\\ln\\left(x^{2}+1\\right)+3\\arctan x+C$。</p>"),
        ("Is $x^{2}+x+1$ irreducible over the reals? What about $x^{2}-x-2$?",
         "<p>$x^{2}+x+1$ 的判別式 $1-4=-3&lt;0$,<strong>不可約</strong>;"
         "$x^{2}-x-2=(x-2)(x+1)$,可分解成兩個相異一次因式。</p>"),
    ])

C6 = Concept(
    title_en="Improper Fractions: Divide First", title_zh="假分式:先長除",
    sub="Numerator degree ≥ denominator degree? Long division comes first.",
    idea="Partial fractions requires a <em>proper</em> fraction. If $\\deg P\\ge\\deg Q$, first "
         "perform polynomial long division to write $\\frac{P}{Q}=S+\\frac{R}{Q}$ with "
         "$\\deg R&lt;\\deg Q$, then decompose only the remainder part.",
    deep="<p>這是<strong>第一步就該檢查</strong>的事,很多人跳過然後卡住。</p>"
         "<p class='step'>$\\dfrac{x^{2}}{x^{2}-1}$ 是假分式(分子分母同次)。"
         "直接設 $\\dfrac{A}{x-1}+\\dfrac{B}{x+1}$ 會<strong>解不出來</strong>——"
         "因為那個形式的通分結果分子最多一次,湊不出二次。</p>"
         "<p class='step'><strong>先長除</strong>:</p>"
         "$$\\frac{x^{2}}{x^{2}-1}=1+\\frac{1}{x^{2}-1},$$"
         "<p>再對餘式部分 $\\dfrac{1}{x^{2}-1}$ 做部分分式(觀念 1 已經拆過)。</p>"
         "<p><strong>長除的快速做法</strong>:分子加減同一個東西湊出分母。"
         "$x^{2}=(x^{2}-1)+1$,所以 $\\dfrac{x^{2}}{x^{2}-1}=\\dfrac{(x^{2}-1)+1}{x^{2}-1}"
         "=1+\\dfrac{1}{x^{2}-1}$。<strong>不必真的做直式除法</strong>,這招快得多。</p>"
         "<p><strong>怎麼判斷是假分式</strong>:比較最高次。"
         "$\\deg P\\ge\\deg Q$ 就是假分式,必須先除。這個檢查花三秒,"
         "省下十分鐘的鬼打牆。<span class='qed'>∎</span></p>",
    guide=["$\\dfrac{x^{2}}{x^{2}-1}$:分子幾次?分母幾次?這是真分式還是假分式?",
           "如果硬設 $\\dfrac{A}{x-1}+\\dfrac{B}{x+1}$,通分後分子最多幾次?湊得出 $x^{2}$ 嗎?",
           "把分子寫成 $x^{2}=(x^{2}-1)+$ <span class=\"blank\"></span>,整個分式就變成 "
           "$1+$ <span class=\"blank\"></span>。",
           "現在剩下的部分是真分式了嗎?可以開始拆了嗎?"],
    demo="Evaluate $\\displaystyle\\int\\frac{x^{2}}{x^{2}-1}\\,dx$.",
    demo_sol="<p><strong>檢查</strong>:分子二次、分母二次 ⟹ 假分式,先除。</p>"
             "$$\\frac{x^{2}}{x^{2}-1}=\\frac{\\left(x^{2}-1\\right)+1}{x^{2}-1}"
             "=1+\\frac{1}{x^{2}-1}.$$"
             "<p>餘式部分用觀念 1 的結果 $\\dfrac{1}{x^{2}-1}=\\dfrac{1/2}{x-1}-\\dfrac{1/2}{x+1}$:</p>"
             "$$\\int\\frac{x^{2}}{x^{2}-1}dx=x+\\frac12\\ln\\left|\\frac{x-1}{x+1}\\right|+C.$$"
             "<p>那個單獨的 $x$ 就是長除的商——<strong>漏掉它是常見錯誤</strong>。</p>",
    demo_hint="先比較分子分母的次數。是假分式的話,把分子湊出分母來。",
    misstep="沒檢查就直接拆,解出矛盾的方程組。或長除後<strong>忘了把商加回去</strong>。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int\\frac{x+1}{x}\\,dx$.",
         "<p>假分式:$\\dfrac{x+1}{x}=1+\\dfrac1x$,積分得 $x+\\ln|x|+C$。</p>"),
        ("Rewrite $\\dfrac{x^{3}}{x^{2}+1}$ as a polynomial plus a proper fraction.",
         "<p>$x^{3}=x\\left(x^{2}+1\\right)-x$,故 $\\dfrac{x^{3}}{x^{2}+1}"
         "=x-\\dfrac{x}{x^{2}+1}$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{x^{3}}{x^{2}+1}\\,dx$.",
         "<p>由上題:$\\displaystyle\\int\\left(x-\\dfrac{x}{x^{2}+1}\\right)dx"
         "=\\dfrac{x^{2}}{2}-\\dfrac12\\ln\\left(x^{2}+1\\right)+C$。</p>"),
    ])

C7 = Concept(
    title_en="The Coefficients Are a Linear System", title_zh="係數就是一組線性方程組",
    sub="Matching coefficients is solving Ax = b — your first linear algebra problem",
    idea="Clearing denominators and matching coefficients produces a system of linear equations in "
         "the unknowns $A,B,C,\\ldots$. Written in matrix form it is $M\\mathbf{c}=\\mathbf{b}$ — "
         "exactly the object linear algebra is built to study.",
    deep="<p>本週的<strong>證明時刻</strong>,也是<strong>線性代數的第一個伏筆</strong>。</p>"
         "<p class='step'>以 $\\dfrac{3x+5}{(x-1)(x+2)}=\\dfrac{A}{x-1}+\\dfrac{B}{x+2}$ 為例。"
         "清分母展開:</p>"
         "$$3x+5=(A+B)x+(2A-B).$$"
         "<p class='step'>兩個多項式相等 $\\iff$ <strong>對應係數相等</strong>,得</p>"
         "$$\\begin{cases}A+B=3\\\\ 2A-B=5\\end{cases}"
         "\\quad\\Longleftrightarrow\\quad"
         "\\begin{bmatrix}1&amp;1\\\\2&amp;-1\\end{bmatrix}"
         "\\begin{bmatrix}A\\\\B\\end{bmatrix}=\\begin{bmatrix}3\\\\5\\end{bmatrix}.$$"
         "<p><strong>這就是 $M\\mathbf{c}=\\mathbf{b}$</strong>。部分分式的每一題,"
         "背後都是一個小型線性系統。</p>"
         "<p><strong>為什麼一定有唯一解</strong>(分解定理的可行性,直覺版):"
         "未知數的個數恰好等於分母的次數 $n$,而「所有次數 $&lt;n$ 的多項式」"
         "構成一個 $n$ 維空間;拆開後的那些簡單分式通分回去,恰好張成整個空間。"
         "<strong>維度對上了,所以係數矩陣可逆,解存在且唯一</strong>。"
         "嚴格證明留給線性代數,但這個「數維度」的直覺現在就能懂。</p>"
         "<p><strong>實務意義</strong>:一旦看成線性系統,就可以<strong>交給電腦解</strong>。"
         "實作課會用 <code>numpy.linalg.solve</code> 寫一個自動分解器——"
         "十行程式取代所有手算。這正是線性代數在 CS 裡無所不在的原因。"
         "<span class='qed'>∎</span></p>",
    guide=["把 $3x+5=A(x+2)+B(x-1)$ 的右邊展開,整理成 $(\\ )x+(\\ )$ 的形式。",
           "兩個多項式相等,表示對應的係數要 <span class=\"blank\"></span>。列出兩條方程式。",
           "把它寫成矩陣形式 $M\\mathbf{c}=\\mathbf{b}$,$M=$ ?、$\\mathbf{b}=$ ?",
           "未知數有幾個?分母是幾次?兩者的關係是什麼?"],
    demo="Write the partial-fraction problem for $\\dfrac{3x+5}{(x-1)(x+2)}$ as a matrix equation "
         "and solve it.",
    demo_sol="<p>清分母展開:$3x+5=A(x+2)+B(x-1)=(A+B)x+(2A-B)$。</p>"
             "<p>對應係數相等:</p>"
             "$$\\begin{bmatrix}1&amp;1\\\\2&amp;-1\\end{bmatrix}"
             "\\begin{bmatrix}A\\\\B\\end{bmatrix}=\\begin{bmatrix}3\\\\5\\end{bmatrix}.$$"
             "<p>解之(消去法):由第一式 $B=3-A$ 代入第二式,"
             "$2A-(3-A)=5\\Rightarrow 3A=8\\Rightarrow A=\\dfrac83$,$B=\\dfrac13$。</p>"
             "<p>與觀念 2 用代值法得到的答案一致。<strong>兩條路殊途同歸</strong>——"
             "代值法是聰明的捷徑,線性系統是通用的框架。</p>"
             "<p>係數矩陣的行列式 $=1\\cdot(-1)-1\\cdot2=-3\\ne0$,故可逆,解唯一。</p>",
    demo_hint="展開、對應係數、寫成矩陣。解法用消去法就好。",
    misstep="以為代值法和比較係數是「兩種不同的答案」。它們解的是<strong>同一個</strong>線性系統。",
    level="mid",
    drills=[
        ("Write the system for $\\dfrac{1}{x(x+1)}=\\dfrac{A}{x}+\\dfrac{B}{x+1}$ in matrix form.",
         "<p>$1=A(x+1)+Bx=(A+B)x+A$,故 $\\begin{bmatrix}1&amp;1\\\\1&amp;0\\end{bmatrix}"
         "\\begin{bmatrix}A\\\\B\\end{bmatrix}=\\begin{bmatrix}0\\\\1\\end{bmatrix}$,"
         "解得 $A=1,B=-1$。</p>"),
        ("For $\\dfrac{P(x)}{(x-1)(x-2)(x-3)}$, how many unknowns and how many equations?",
         "<p>三個未知數($A,B,C$),比較 $x^{2},x^{1},x^{0}$ 三個係數得三條方程式。"
         "個數相等,恰好可解。</p>"),
        ("Why does the number of unknowns always equal the degree of the denominator?",
         "<p>因為真分式的分子最多 $n-1$ 次,有 $n$ 個自由係數;"
         "拆開後的待定係數也必須有 $n$ 個,才能湊出所有可能的分子。"
         "(重根與不可約二次的計數也符合:$k$ 重根貢獻 $k$ 個、不可約二次貢獻 $2$ 個。)</p>"),
    ])

C8 = Concept(
    title_en="Putting It All Together", title_zh="完整流程",
    sub="Check proper → factor → set up → solve → integrate term by term",
    idea="The full procedure: (1) is it proper? divide if not; (2) factor the denominator "
         "completely; (3) write the correct form (one term per power of each linear factor, "
         "$Ax+B$ over each irreducible quadratic); (4) solve for the coefficients; "
         "(5) integrate term by term.",
    deep="<p>五個步驟,<strong>順序不能亂</strong>。學生的錯誤幾乎都來自跳步。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>步驟</th><th>做什麼</th>"
         "<th>跳過的下場</th></tr></thead><tbody>"
         "<tr><td>①</td><td>檢查真分式</td><td>方程組無解,鬼打牆</td></tr>"
         "<tr><td>②</td><td>分母完全因式分解</td><td>拆的形式一開始就錯</td></tr>"
         "<tr><td>③</td><td>寫對待定形式</td><td>重根漏項、二次分子只寫常數</td></tr>"
         "<tr><td>④</td><td>解係數(代值 + 比較)</td><td>—</td></tr>"
         "<tr><td>⑤</td><td>逐項積分</td><td>把 $\\frac{1}{(x-a)^{2}}$ 積成對數</td></tr>"
         "</tbody></table></div>"
         "<p><strong>三種基本項的積分,要能反射</strong>:</p>"
         "$$\\int\\frac{dx}{x-a}=\\ln|x-a|,\\qquad"
         "\\int\\frac{dx}{(x-a)^{n}}=\\frac{(x-a)^{1-n}}{1-n}\\ (n\\ge2),$$"
         "$$\\int\\frac{Ax+B}{x^{2}+a^{2}}dx=\\frac{A}{2}\\ln\\left(x^{2}+a^{2}\\right)"
         "+\\frac{B}{a}\\arctan\\frac{x}{a}.$$"
         "<p><strong>本週結束,決策樹完整了</strong>:換元 → 分部 → 三角代換 → 部分分式。"
         "期中考的積分題,四招之內一定解得掉。</p>"
         "<p><strong>下週轉向</strong>:當四招都失效(如 $\\int e^{x^{2}}dx$),"
         "或當你只需要一個數字而不是公式時,就換數值方法上場。"
         "<span class='qed'>∎</span></p>",
    guide=["拿到 $\\displaystyle\\int\\dfrac{x^{3}+1}{x^{2}-x}dx$,第一件事該檢查什麼?",
           "分母 $x^{2}-x$ 完全分解是 <span class=\"blank\"></span>。",
           "待定形式要寫幾項?每一項的分子是常數還是一次式?",
           "積分時 $\\dfrac{1}{x-1}$ 給對數;那 $\\dfrac{1}{(x-1)^{2}}$ 給什麼?"],
    demo="Evaluate $\\displaystyle\\int\\frac{x^{3}+1}{x^{2}-x}\\,dx$ following the full "
         "five-step procedure.",
    demo_sol="<p><strong>① 真分式?</strong> 分子三次、分母二次 ⟹ 假分式,先長除。</p>"
             "$$\\frac{x^{3}+1}{x^{2}-x}=x+1+\\frac{x+1}{x^{2}-x}.$$"
             "<p>(驗算:$(x+1)\\left(x^{2}-x\\right)=x^{3}-x$,加上 $x+1$ 得 $x^{3}+1$ ✓)</p>"
             "<p><strong>② 分解分母</strong>:$x^{2}-x=x(x-1)$。</p>"
             "<p><strong>③ 待定形式</strong>:$\\dfrac{x+1}{x(x-1)}=\\dfrac{A}{x}+\\dfrac{B}{x-1}$。</p>"
             "<p><strong>④ 解係數</strong>(遮蓋法):$x=0$ 代入 $\\dfrac{x+1}{x-1}$ 得 $A=-1$;"
             "$x=1$ 代入 $\\dfrac{x+1}{x}$ 得 $B=2$。</p>"
             "<p><strong>⑤ 逐項積分</strong>:</p>"
             "$$\\int\\frac{x^{3}+1}{x^{2}-x}dx=\\frac{x^{2}}{2}+x-\\ln|x|+2\\ln|x-1|+C.$$",
    demo_hint="五步驟照順序走。第一步一定是檢查次數。",
    misstep="長除後忘了把商 $x+1$ 一起積分,只積了餘式部分。",
    level="hard",
    drills=[
        ("Evaluate $\\displaystyle\\int\\frac{2x+1}{x^{2}+x}\\,dx$.",
         "<p>真分式。$x^{2}+x=x(x+1)$,而分子恰為分母的導數!"
         "直接換元:$\\ln\\left|x^{2}+x\\right|+C$。"
         "(<strong>先看有沒有捷徑</strong>,不一定要拆。)</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{dx}{x^{2}+x}$.",
         "<p>$\\dfrac{1}{x(x+1)}=\\dfrac1x-\\dfrac{1}{x+1}$,積分得 "
         "$\\ln\\left|\\dfrac{x}{x+1}\\right|+C$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{x^{2}+1}{x(x-1)^{2}}\\,dx$.",
         "<p>由觀念 4 的分解 $\\dfrac1x+\\dfrac{2}{(x-1)^{2}}$:"
         "$\\ln|x|-\\dfrac{2}{x-1}+C$。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜手刻部分分式分解器:解一個線性系統",
    intro="觀念 7 說「比較係數＝解 $M\\mathbf{c}=\\mathbf{b}$」。這格把它寫成程式——"
          "十行 numpy 取代所有手算,也是你的第一支線性代數程式。",
    code="""x = sp.Symbol('x')

def decompose_distinct_linear(numer_coeffs, roots):
    \"\"\"把 P(x) / prod(x - r_i) 拆開(相異一次因式)。

    做法:設 P(x)/prod = sum_i A_i/(x - r_i),清分母後比較係數,
    得線性系統 M c = b,用 numpy 解。
    numer_coeffs: 分子係數,由高次到低次
    roots: 分母各一次因式的根
    \"\"\"
    n = len(roots)
    # 第 i 個未知數對應的多項式 = prod_{j != i} (x - r_j)
    basis = []
    for i in range(n):
        p = np.poly1d([1.0])
        for j, r in enumerate(roots):
            if j != i:
                p = p * np.poly1d([1.0, -r])
        basis.append(np.pad(p.coefficients, (n - 1 - len(p.coefficients) + 1, 0)))
    M = np.array(basis).T                      # 每一行是一個基底多項式的係數
    b = np.pad(np.array(numer_coeffs, dtype=float),
               (M.shape[0] - len(numer_coeffs), 0))
    return np.linalg.solve(M, b)

# 例 1: (3x + 5) / ((x-1)(x+2))
coef = decompose_distinct_linear([3, 5], [1, -2])
print("(3x+5)/((x-1)(x+2)) 的係數:", np.round(coef, 6), "  理論值 [8/3, 1/3] =",
      np.round([8/3, 1/3], 6))

# 例 2: 1 / ((x-1)(x-4))
coef2 = decompose_distinct_linear([5], [1, 4])
print("5/((x-1)(x-4))     的係數:", np.round(coef2, 6), "  理論值 [-5/3, 5/3]")

# 用 sympy 交叉驗證
print("\\nSymPy apart() 的答案:")
print("  ", sp.apart((3*x + 5)/((x - 1)*(x + 2)), x))
print("  ", sp.apart(5/((x - 1)*(x - 4)), x))""",
    expected="(3x+5)/((x-1)(x+2)) 的係數: [2.666667 0.333333]   理論值 [8/3, 1/3] = [2.666667 0.333333]",
    seealso="手刻的線性系統解出 $\\left[\\frac83,\\frac13\\right]$,和手算、和 SymPy 的 "
            "<code>apart()</code> 完全一致。<strong>部分分式的本質就是解 "
            "$M\\mathbf{c}=\\mathbf{b}$</strong>——這是你第一次真的用到線性代數。",
    todo="""# TODO 學生練習:用這支程式解 (2x - 1) / ((x+1)(x-2)) 的係數
# 再手算驗證(遮蓋法):x=-1 代入 (2x-1)/(x-2),x=2 代入 (2x-1)/(x+1)""")

LAB2 = Lab(
    title="Lab 2｜四招決策樹:讓程式幫你選",
    intro="期中考前的整理。把本學期學過的四招寫成一張表,"
          "用 SymPy 檢查每一題的答案,並看清楚「哪一題該用哪一招」。",
    code="""x = sp.Symbol('x', real=True)

problems = [
    ("∫ x·sqrt(1-x²) dx",   x*sp.sqrt(1-x**2),          "換元 t=1-x²"),
    ("∫ sqrt(1-x²) dx",     sp.sqrt(1-x**2),            "三角代換 x=sinθ"),
    ("∫ x·ln x dx",         x*sp.log(x),                "分部 (LIATE: u=ln x)"),
    ("∫ x·e^x dx",          x*sp.exp(x),                "分部 (u=x)"),
    ("∫ dx/(x²-1)",         1/(x**2-1),                 "部分分式"),
    ("∫ dx/(x²+1)",         1/(x**2+1),                 "標準公式 → arctan"),
    ("∫ (2x+1)/(x²+x) dx",  (2*x+1)/(x**2+x),           "換元(分子=分母導數!)"),
    ("∫ sin³x·cos²x dx",    sp.sin(x)**3*sp.cos(x)**2,  "奇次拆一個"),
]

print(f"{'積分':24s} {'建議招式':26s} {'SymPy 的答案'}")
for name, f, method in problems:
    r = sp.simplify(sp.integrate(f, x))
    print(f"{name:24s} {method:26s} {str(r)[:44]}")

print("\\n注意第 7 題:分子 2x+1 恰好是分母 x²+x 的導數 —— 不必拆,直接換元。")
print("      拿到有理函數先看這個,可以省一大段。")""",
    expected="∫ (2x+1)/(x²+x) dx       換元(分子=分母導數!)      log(x**2 + x)",
    seealso="八題涵蓋本學期四招。特別注意第七題:<strong>分子恰好是分母的導數</strong>,"
            "換元一行解決,完全不必做部分分式。決策樹的順序有意義——"
            "永遠先找最省力的路。",
    todo="""# TODO 學生練習:再加三題到 problems 裡,分別對應
# (1) 需要先長除的假分式 (2) 需要先配方的 (3) 含不可約二次因式的
# 跑跑看 SymPy 給什麼答案,和你手算的對不對得上""")

LABS = [LAB1, LAB2]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="積分技巧最後一招。有理函數看起來最無害,但直接積不動——"
         "要先把它<strong>拆開</strong>。而「拆」這件事,骨子裡是在解一組線性方程組,"
         "這是他們第一次真的碰到線性代數。",
    fastforward=[
        ("$\\int\\frac{dx}{x-a}=\\ln|x-a|$ 等基本積分", "銜接課會了", "快轉"),
        ("因式分解、通分", "高職學過,但生疏", "快速複習"),
        ("相異一次因式的拆法", "全新,但機械", "中速"),
        ("<strong>遮蓋法</strong>", "全新,考試神器", "務必練熟"),
        ("重根要寫幾項", "全新,最常錯", "踩煞車"),
        ("不可約二次的 $Ax+B$", "全新", "踩煞車"),
        ("假分式先長除", "偏新,但三秒就能檢查", "中速"),
        ("<strong>係數＝線性方程組</strong>", "全新,線代預告", "踩煞車(證明時刻)"),
    ],
    outcomes=[
        "拿到有理函數,<strong>第一步先檢查真分式</strong>,必要時長除。",
        "依分母的因式寫出<strong>正確的待定形式</strong>:重根要 $k$ 項、不可約二次要 $Ax+B$。",
        "熟練<strong>遮蓋法</strong>求相異一次因式的係數。",
        "說明比較係數就是解 $M\\mathbf{c}=\\mathbf{b}$,並解釋為什麼未知數個數 = 分母次數。",
        "逐項積分,並分清楚哪些項給對數、哪些給冪次、哪些給 arctan。",
    ],
    clock=[
        ("00:00–00:10", "收作業;複習三招決策樹,今天補最後一招", "—"),
        ("00:10–00:30", "動機:為什麼要拆(先驗證拆得開)", "觀念 1"),
        ("00:30–00:55", "相異一次因式:代值 vs 比較係數", "觀念 2"),
        ("00:55–01:00", "休息", "—"),
        ("01:00–01:20", "<strong>遮蓋法</strong>:三秒求一個係數", "觀念 3"),
        ("01:20–01:50", "重根與不可約二次(最常錯的兩塊)", "觀念 4–5"),
        ("01:50–01:55", "休息", "—"),
        ("01:55–02:15", "假分式先長除", "觀念 6"),
        ("02:15–02:45", "<strong>證明時刻</strong>:係數就是線性方程組", "觀念 7"),
        ("02:45–03:00", "完整流程五步驟 + 期中考範圍預告", "觀念 8"),
    ],
    proof_moment="把比較係數的過程寫成矩陣方程 $M\\mathbf{c}=\\mathbf{b}$,"
                 "並用「數維度」說明為什麼一定有<strong>唯一解</strong>:"
                 "未知數個數恰等於分母次數 $n$,而次數 $&lt;n$ 的多項式構成 $n$ 維空間,"
                 "拆開的那些基底恰好張成它。嚴格證明留給線代,但維度的直覺現在就給。",
    script=[
        ("開場:最後一招(10 分)",
         "<p>把三週累積的決策樹畫在黑板上,最後一格空著:「有理函數 → ?」</p>"
         "<p>「今天把它填滿。填完之後,期中考的積分題你們四招之內一定解得掉。」</p>"),
        ("動機:先證明拆得開(20 分)",
         "<p>不要一開始就教步驟。先問:「$\\int\\frac{dx}{x-1}$ 會嗎?」會。"
         "「$\\int\\frac{dx}{x^{2}-1}$ 呢?」卡住。</p>"
         "<p>然後<strong>直接給答案的一半</strong>:把 $\\frac{1/2}{x-1}-\\frac{1/2}{x+1}$ "
         "寫上去,叫他們通分回去。通出 $\\frac{1}{x^{2}-1}$ 的那一刻,動機就建立了。</p>"
         "<p>「所以確實拆得開。剩下的問題只有一個:<strong>怎麼找到那兩個數</strong>?」</p>"),
        ("兩種解法都要會(25 分)",
         "<p>代值法快、比較係數通用。<strong>兩種都示範同一題</strong>,讓他們看到答案一樣。</p>"
         "<p>強調適用範圍:代值法在相異一次因式時最強,但遇到重根就只能解出一部分——"
         "這個伏筆等一下會回收。</p>"),
        ("遮蓋法:考試神器(20 分)",
         "<p>直接示範:用手遮住 $(x-1)$,代 $x=1$ 進剩下的,答案就出來了。三秒。</p>"
         "<p>學生會覺得像魔術,所以<strong>一定要解釋為什麼</strong>:"
         "清分母後代 $x=1$,另一項自動歸零,剩下的就是「遮住之後的分母」在 $x=1$ 的值。</p>"
         "<p>然後練三題,練到反射。這一招他們考試會用到爛。</p>"),
        ("兩個最常錯的地方(30 分)",
         "<p><strong>重根</strong>:先讓他們對 $\\frac{x^{2}+1}{x(x-1)^{2}}$ 只寫兩項,"
         "解到矛盾為止。<strong>親自撞牆比聽你講有效</strong>。</p>"
         "<p>然後說明為什麼要 $k$ 項——數自由度。解出來發現 $B=0$,"
         "順勢問:「那我不寫 $B$ 不就好了?」答案:你<strong>事前不知道</strong>它是零。</p>"
         "<p><strong>不可約二次</strong>:判別式先講,再說明分子為什麼是 $Ax+B$(還是數自由度)。"
         "積分時拆成兩塊:$x$ 那塊換元、常數那塊 arctan。</p>"),
        ("三秒鐘的檢查(20 分)",
         "<p>假分式。先讓他們對 $\\frac{x^{2}}{x^{2}-1}$ 硬拆,發現湊不出二次項。</p>"
         "<p>然後給快速長除法:$x^{2}=(x^{2}-1)+1$。「不必做直式,湊就好。」</p>"
         "<p>強調:<strong>這個檢查花三秒,能省十分鐘的鬼打牆</strong>。</p>"),
        ("證明時刻:你們正在解線性方程組(30 分)",
         "<p>把 $3x+5=(A+B)x+(2A-B)$ 的係數比較寫成聯立,再寫成矩陣。</p>"
         "<p>「這個東西叫 $M\\mathbf{c}=\\mathbf{b}$。下學期有一整門課在研究它,叫線性代數。」</p>"
         "<p>然後給維度直覺:未知數個數 = 分母次數,不是巧合。"
         "「次數小於 $n$ 的多項式構成一個 $n$ 維空間」——這句話他們現在只能半懂,"
         "但下學期會恍然大悟。<strong>先種下,不必收成</strong>。</p>"
         "<p>實務收尾:「既然是線性系統,就能交給電腦。實作課用十行 numpy 寫一個分解器。」</p>"),
        ("收尾:決策樹完整了(15 分)",
         "<p>五步驟流程表寫上去,強調順序不能亂。三種基本項的積分要能反射。</p>"
         "<p>最後把四招決策樹補完,宣布期中考範圍 W1–W8,"
         "並預告下週:「當四招都失效怎麼辦?或者你根本不需要公式、只要一個數字?"
         "下週講數值積分。」</p>"),
    ],
    myths=[
        "$\\displaystyle\\int\\frac{dx}{x^{2}-1}$ 答成 $\\ln\\left|x^{2}-1\\right|$。",
        "沒檢查真分式就開始拆,解出矛盾的方程組。",
        "長除之後忘了把商加回去積分。",
        "$(x-a)^{k}$ 只寫最高次那一項,漏掉低次項。",
        "不可約二次的分子只寫常數,沒寫 $Ax+B$。",
        "對重根或不可約二次用遮蓋法。",
        "$\\displaystyle\\int\\frac{dx}{(x-a)^{2}}$ 積成對數。只有一次方才給對數。",
        "拿到有理函數就無腦拆,沒先看分子是不是分母的導數。",
    ],
    exit_check=[
        ("$\\dfrac{5}{(x-1)(x+4)}$ 拆開後,$\\dfrac{A}{x-1}$ 的 $A$ 是多少?(用遮蓋法)",
         "遮住 $(x-1)$,代 $x=1$ 進 $\\dfrac{5}{x+4}$,得 $A=1$。"),
        ("$\\dfrac{P(x)}{(x-2)^{3}\\left(x^{2}+1\\right)}$ 的待定形式要寫幾項?各是什麼分子?",
         "五項:$\\dfrac{A}{x-2}+\\dfrac{B}{(x-2)^{2}}+\\dfrac{C}{(x-2)^{3}}"
         "+\\dfrac{Dx+E}{x^{2}+1}$。共 5 個未知數 = 分母次數 5。"),
        ("$\\displaystyle\\int\\frac{2x+1}{x^{2}+x}\\,dx$ 最快的做法是什麼?",
         "分子恰為分母的導數 → 直接換元,答案 $\\ln\\left|x^{2}+x\\right|+C$。不必做部分分式。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W6-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "每題都要先寫出<strong>待定形式</strong>再動手解係數。",
        "<strong>複習</strong>:期中考範圍 W1–W8。這週先把四招決策樹整理成一張自己的筆記。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 1/(x^2-1) 的分解", "simplify(1/(x**2-1) - (Rational(1,2)/(x-1) - Rational(1,2)/(x+1)))", "0"),
    ("C1 示範 ∫dx/(x^2-1)(在 x>1 上驗)",
     "simplify(diff(log((x-1)/(x+1))/2, x) - 1/(x**2-1))", "0"),
    ("C1 D1 1/(x(x+1)) 的分解", "simplify(1/(x*(x+1)) - (1/x - 1/(x+1)))", "0"),
    ("C2 示範 A=8/3", "((3*x+5)/(x+2)).subs(x, 1)", "Rational(8,3)"),
    ("C2 示範 B=1/3", "((3*x+5)/(x-1)).subs(x, -2)", "Rational(1,3)"),
    ("C2 示範 分解正確",
     "simplify((3*x+5)/((x-1)*(x+2)) - (Rational(8,3)/(x-1) + Rational(1,3)/(x+2)))", "0"),
    ("C2 D2 ∫dx/(x^2-4)(在 x>2 上驗)", "simplify(diff(log((x-2)/(x+2))/4, x) - 1/(x**2-4))", "0"),
    ("C2 D3 ∫_2^3 dx/(x^2-1)", "simplify(integrate(1/(x**2-1), (x, 2, 3)) - log(Rational(3,2))/2)", "0"),
    ("C3 示範 遮蓋法 x=2 得 9/5", "((x+7)/(x+3)).subs(x, 2)", "Rational(9,5)"),
    ("C3 示範 遮蓋法 x=-3 得 -4/5", "((x+7)/(x-2)).subs(x, -3)", "Rational(-4,5)"),
    ("C3 D1 5/((x-1)(x-4)) 係數", "(5/(x-4)).subs(x, 1)", "Rational(-5,3)"),
    ("C3 D2 2x/((x+1)(x-3)) 係數", "((2*x)/(x-3)).subs(x, -1)", "Rational(1,2)"),
    ("C4 示範 (x^2+1)/(x(x-1)^2) 的分解",
     "simplify((x**2+1)/(x*(x-1)**2) - (1/x + 2/(x-1)**2))", "0"),
    ("C4 D1 1/(x(x+1)^2) 的分解",
     "simplify(1/(x*(x+1)**2) - (1/x - 1/(x+1) - 1/(x+1)**2))", "0"),
    ("C4 D2 ∫dx/(x-1)^2", "simplify(diff(-1/(x-1), x) - 1/(x-1)**2)", "0"),
    ("C5 示範 1/(x^3+x) 的分解", "simplify(1/(x**3+x) - (1/x - x/(x**2+1)))", "0"),
    ("C5 示範 ∫dx/(x^3+x)(在 x>0 上驗)",
     "simplify(diff(log(x) - log(x**2+1)/2, x) - 1/(x**3+x))", "0"),
    ("C5 D1 1/(x(x^2+4)) 的分解",
     "simplify(1/(x*(x**2+4)) - (Rational(1,4)/x - x/(4*(x**2+4))))", "0"),
    ("C5 D2 ∫(2x+3)/(x^2+1)",
     "simplify(diff(log(x**2+1) + 3*atan(x), x) - (2*x+3)/(x**2+1))", "0"),
    ("C6 示範 x^2/(x^2-1) 長除", "simplify(x**2/(x**2-1) - (1 + 1/(x**2-1)))", "0"),
    ("C6 D2 x^3/(x^2+1) 長除", "simplify(x**3/(x**2+1) - (x - x/(x**2+1)))", "0"),
    ("C6 D3 ∫x^3/(x^2+1)",
     "simplify(diff(x**2/2 - log(x**2+1)/2, x) - x**3/(x**2+1))", "0"),
    ("C7 示範 線性系統解 A=8/3", "solve([Eq(A+B, 3), Eq(2*A-B, 5)], [A, B])[A]", "Rational(8,3)"),
    ("C8 示範 (x^3+1)/(x^2-x) 長除",
     "simplify((x**3+1)/(x**2-x) - (x + 1 + (x+1)/(x**2-x)))", "0"),
    ("C8 示範 完整積分(在 x>1 上驗)",
     "simplify(diff(x**2/2 + x - log(x) + 2*log(x-1), x) - (x**3+1)/(x**2-x))", "0"),
    ("C8 D1 分子是分母的導數", "simplify(diff(x**2+x, x) - (2*x+1))", "0"),
]

WEEK = Week(
    num=6,
    title="部分分式分解",
    subtitle="積分技巧最後一招。有理函數看起來最無害卻積不動——要先把它拆開。"
             "而「拆」這件事骨子裡是在解一組線性方程組:這是線性代數的第一個伏筆。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["積分技巧 III", "線代預告"],
)
