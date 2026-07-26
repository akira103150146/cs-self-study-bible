# -*- coding: utf-8 -*-
"""第 9 週｜期中考

範圍 W1–W8。100 分,100 分鐘,6 大題。
配比:計算 ~60%、概念與前提判斷 ~25%、應用 ~15%。
ε-δ 只考直覺與「哪一步違反前提」,不考完整 δ 建構。
所有答案已用 sympy 驗證(見本檔 ANSWER_CHECKS)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Problem, ExamGroup, ExamPaper

# ---------------------------------------------------------------- 第 1 題

G1 = ExamGroup(
    num=1, title="Problem 1 · Limits and the Formal Definition", origin="對應第 1 週",
    problems=[
        Problem(
            label="1(a)", pts=5, level="basic",
            stem="For $\\displaystyle\\lim_{x\\to 2}5x=10$, find a $\\delta$ (in terms of "
                 "$\\varepsilon$) that satisfies the definition, and write the one-line "
                 "verification.",
            sol="<p>反推:$|5x-10|=5|x-2|&lt;\\varepsilon\\iff|x-2|&lt;\\dfrac{\\varepsilon}{5}$。"
                "<span style='color:#888'>[反推 2 分]</span></p>"
                "<p><strong>正式書寫</strong>:給定 $\\varepsilon&gt;0$,取 "
                "$\\delta=\\dfrac{\\varepsilon}{5}$。若 $0&lt;|x-2|&lt;\\delta$,則</p>"
                "$$|5x-10|=5|x-2|&lt;5\\delta=\\varepsilon.$$"
                "<p>依定義得證。<span style='color:#888'>[順推格式 3 分。"
                "只寫反推草稿最多給 2 分]</span></p>"),
        Problem(
            label="1(b)", pts=5, level="mid",
            stem="Evaluate $\\displaystyle\\lim_{x\\to\\infty}\\left(\\sqrt{x^{2}+3x}-x\\right)$.",
            sol="<p>$\\infty-\\infty$ 不定型,乘共軛:</p>"
                "$$\\sqrt{x^{2}+3x}-x=\\frac{\\left(x^{2}+3x\\right)-x^{2}}"
                "{\\sqrt{x^{2}+3x}+x}=\\frac{3x}{\\sqrt{x^{2}+3x}+x}.$$"
                "<span style='color:#888'>[乘共軛 2 分]</span>"
                "<p>上下同除 $x$(注意 $x&gt;0$ 故 $\\sqrt{x^{2}}=x$):</p>"
                "$$=\\frac{3}{\\sqrt{1+\\frac3x}+1}\\longrightarrow\\frac{3}{2}.$$"
                "<span style='color:#888'>[化簡與取極限 3 分]</span>"),
        Problem(
            label="1(c)", pts=4, level="mid",
            stem="A student computes $f(x)=\\sin\\dfrac{\\pi}{x}$ at "
                 "$x=1,\\tfrac12,\\tfrac13,\\tfrac14$, gets $0$ every time, and concludes "
                 "$\\displaystyle\\lim_{x\\to0}f(x)=0$. Is the conclusion correct? Justify.",
            sol="<p><strong>不正確。</strong><span style='color:#888'>[判斷 1 分]</span></p>"
                "<p>那四個取樣點確實都給 $0$($\\frac{\\pi}{x}=\\pi,2\\pi,3\\pi,4\\pi$),"
                "但沿另一條路徑 $x=\\dfrac{2}{4k+1}\\to0$,函數值<strong>恆為 $1$</strong>。"
                "<span style='color:#888'>[給出反例路徑 2 分]</span></p>"
                "<p>兩條路徑趨近 $0$ 給出不同的值,故極限不存在。根本原因:定義要求對"
                "<strong>所有</strong>滿足 $0&lt;|x|&lt;\\delta$ 的 $x$ 都成立,"
                "有限筆取樣永遠無法保證。<strong>表格只能否證,不能證明</strong>。"
                "<span style='color:#888'>[說明理由 1 分]</span></p>"),
    ])

# ---------------------------------------------------------------- 第 2 題

G2 = ExamGroup(
    num=2, title="Problem 2 · Inverse and Hyperbolic Functions", origin="對應第 2 週",
    problems=[
        Problem(
            label="2(a)", pts=4, level="basic",
            stem="Let $f(x)=x^{3}+2x$. Given $f(1)=3$, compute $\\left(f^{-1}\\right)'(3)$ "
                 "without finding a formula for $f^{-1}$.",
            sol="<p>$f'(x)=3x^{2}+2$,故 $f'(1)=5$。<span style='color:#888'>[求導並代值 2 分]</span></p>"
                "$$\\left(f^{-1}\\right)'(3)=\\frac{1}{f'(1)}=\\frac15.$$"
                "<span style='color:#888'>[套公式 2 分。代成 $\\frac{1}{f'(3)}$ 者 0 分]</span>"),
        Problem(
            label="2(b)", pts=4, level="mid",
            stem="Differentiate $f(x)=\\arctan\\!\\left(x^{2}\\right)$.",
            sol="<p>鏈鎖法則,外層 $\\arctan$、內層 $x^{2}$:</p>"
                "$$f'(x)=\\frac{1}{1+\\left(x^{2}\\right)^{2}}\\cdot 2x"
                "=\\frac{2x}{1+x^{4}}.$$"
                "<span style='color:#888'>[外層導數 2 分、內層導數 2 分。"
                "漏乘 $2x$ 者扣 2 分]</span>"),
        Problem(
            label="2(c)", pts=4, level="mid",
            stem="Differentiate $g(x)=\\tanh(3x)$ and express the answer using $\\tanh$ only.",
            sol="<p>$\\dfrac{d}{dx}\\tanh u=\\operatorname{sech}^{2}u$,內層導數 $3$:</p>"
                "$$g'(x)=3\\operatorname{sech}^{2}(3x)=3\\left(1-\\tanh^{2}(3x)\\right).$$"
                "<span style='color:#888'>[導數 2 分、改寫成 $\\tanh$ 2 分]</span>"
                "<p>(這正是神經網路反向傳播裡 <code>3 * (1 - a**2)</code> 那一行。)</p>"),
    ])

# ---------------------------------------------------------------- 第 3 題

G3 = ExamGroup(
    num=3, title="Problem 3 · L'Hôpital's Rule and Taylor Polynomials", origin="對應第 3 週",
    problems=[
        Problem(
            label="3(a)", pts=5, level="mid",
            stem="Evaluate $\\displaystyle\\lim_{x\\to0}"
                 "\\frac{e^{x}-1-x-\\frac{x^{2}}{2}}{x^{3}}$.",
            sol="<p>代入為 $\\dfrac00$,連用三次羅必達:</p>"
                "$$\\lim\\frac{e^{x}-1-x}{3x^{2}}=\\lim\\frac{e^{x}-1}{6x}"
                "=\\lim\\frac{e^{x}}{6}=\\frac16.$$"
                "<span style='color:#888'>[每次確認仍是 $\\frac00$ 各 1 分,共 3 分;"
                "最終答案 2 分]</span>"
                "<p><strong>另解</strong>(更快):由泰勒展開 "
                "$e^{x}=1+x+\\frac{x^{2}}{2}+\\frac{x^{3}}{6}+\\cdots$,分子 "
                "$=\\frac{x^{3}}{6}+O(x^{4})$,除以 $x^{3}$ 後極限為 $\\frac16$。同樣給滿分。</p>"),
        Problem(
            label="3(b)", pts=5, level="mid",
            stem="Find the third-order Taylor polynomial $P_{3}$ of $f(x)=\\ln(1+x)$ at $a=0$.",
            sol="<p>逐階導數在 $0$ 的值:$f(0)=0$、$f'=\\dfrac{1}{1+x}\\Rightarrow f'(0)=1$、"
                "$f''=-\\dfrac{1}{(1+x)^{2}}\\Rightarrow f''(0)=-1$、"
                "$f'''=\\dfrac{2}{(1+x)^{3}}\\Rightarrow f'''(0)=2$。"
                "<span style='color:#888'>[導數表 3 分]</span></p>"
                "$$P_{3}(x)=0+x-\\frac{x^{2}}{2}+\\frac{2x^{3}}{6}"
                "=x-\\frac{x^{2}}{2}+\\frac{x^{3}}{3}.$$"
                "<span style='color:#888'>[除以 $k!$ 並組合 2 分。漏掉 $k!$ 者扣 2 分]</span>"),
        Problem(
            label="3(c)", pts=6, level="hard",
            stem="(i) Using $P_{3}(x)=x-\\frac{x^{3}}{6}$ for $\\sin x$, bound the error in "
                 "approximating $\\sin(0.2)$. &nbsp;[3] &nbsp; "
                 "(ii) A classmate proves $\\displaystyle\\lim_{x\\to0}\\frac{\\sin x}{x}=1$ by "
                 "applying L'Hôpital's Rule. Explain precisely what is wrong. &nbsp;[3]",
            sol="<p><strong>(i)</strong> $\\sin$ 的展開無 $x^{4}$ 項,故可用 $n=4$ 的餘項界。"
                "各階導數的絕對值 $\\le1$,取 $M=1$:</p>"
                "$$\\left|R\\right|\\le\\frac{|0.2|^{5}}{5!}=\\frac{3.2\\times10^{-4}}{120}"
                "\\approx2.67\\times10^{-6}.$$"
                "<span style='color:#888'>[取 $M=1$ 1 分、寫出餘項式 1 分、算出數值 1 分]</span>"
                "<p>(實際誤差 $2.664\\times10^{-6}$,界成立且很緊。)</p>"
                "<p><strong>(ii)</strong> <strong>循環論證。</strong>要用羅必達必須先知道 "
                "$(\\sin x)'=\\cos x$;而該導數由定義推導時會出現</p>"
                "$$\\lim_{h\\to0}\\frac{\\sin h}{h},$$"
                "<p>正是待證的極限本身。因此這個「證明」是拿結論當前提。"
                "<span style='color:#888'>[指出循環 2 分]</span></p>"
                "<p>合法證法為單位圓的面積比較 + 夾擠定理。"
                "(用羅必達<strong>驗算</strong>可以,當<strong>證明</strong>不行。)"
                "<span style='color:#888'>[給出正確證法 1 分]</span></p>"),
    ])

# ---------------------------------------------------------------- 第 4 題

G4 = ExamGroup(
    num=4, title="Problem 4 · Techniques of Integration", origin="對應第 4–6 週",
    problems=[
        Problem(
            label="4(a)", pts=6, level="mid",
            stem="Evaluate $\\displaystyle\\int x^{2}e^{-x}\\,dx$.",
            sol="<p>表格法(或連續兩次分部)。左欄微分 $x^{2}$ 到 $0$、右欄積分 $e^{-x}$,"
                "符號 $+,-,+$ 交錯:</p>"
                "$$x^{2}\\cdot\\left(-e^{-x}\\right)-2x\\cdot e^{-x}"
                "+2\\cdot\\left(-e^{-x}\\right)$$"
                "$$=-\\left(x^{2}+2x+2\\right)e^{-x}+C.$$"
                "<span style='color:#888'>[方法 2 分、逐項 3 分、$+C$ 1 分]</span>"
                "<p><strong>驗算</strong>:微分右式得 "
                "$-(2x+2)e^{-x}+\\left(x^{2}+2x+2\\right)e^{-x}=x^{2}e^{-x}$ ✓</p>"),
        Problem(
            label="4(b)", pts=4, level="mid",
            stem="Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{4-x^{2}}}$.",
            sol="<p>形狀 $\\sqrt{a^{2}-x^{2}}$,令 $x=2\\sin\\theta$、"
                "$dx=2\\cos\\theta\\,d\\theta$,則 $\\sqrt{4-x^{2}}=2\\cos\\theta$"
                "(值域限制保證 $\\cos\\theta\\ge0$):</p>"
                "$$\\int\\frac{2\\cos\\theta}{2\\cos\\theta}d\\theta=\\theta+C"
                "=\\arcsin\\frac{x}{2}+C.$$"
                "<span style='color:#888'>[選對代換 2 分、化簡 2 分、換回 $x$ 1 分。"
                "停在 $\\theta$ 者扣 1 分]</span>"),
        Problem(
            label="4(c)", pts=4, level="mid",
            stem="Evaluate $\\displaystyle\\int\\frac{3x+1}{(x-1)(x+2)}\\,dx$.",
            sol="<p>部分分式。遮蓋法:$x=1$ 代入 $\\dfrac{3x+1}{x+2}$ 得 $\\dfrac43$;"
                "$x=-2$ 代入 $\\dfrac{3x+1}{x-1}$ 得 $\\dfrac{-5}{-3}=\\dfrac53$。"
                "<span style='color:#888'>[係數 3 分]</span></p>"
                "$$\\int\\left(\\frac{4}{3(x-1)}+\\frac{5}{3(x+2)}\\right)dx"
                "=\\frac43\\ln|x-1|+\\frac53\\ln|x+2|+C.$$"
                "<span style='color:#888'>[積分 2 分。絕對值漏寫不扣分]</span>"),
        Problem(
            label="4(d)", pts=4, level="mid",
            stem="Evaluate $\\displaystyle\\int\\frac{\\ln x}{x^{2}}\\,dx$.",
            sol="<p>分部,LIATE 取 $u=\\ln x$、$dv=x^{-2}dx$,則 $du=\\dfrac{dx}{x}$、"
                "$v=-\\dfrac1x$:</p>"
                "$$-\\frac{\\ln x}{x}+\\int\\frac{dx}{x^{2}}"
                "=-\\frac{\\ln x}{x}-\\frac1x+C=-\\frac{\\ln x+1}{x}+C.$$"
                "<span style='color:#888'>[選 $u$ 2 分、套公式 2 分、完成 1 分]</span>"),
        Problem(
            label="4(e)", pts=4, level="mid",
            stem="Evaluate $\\displaystyle\\int_{0}^{1}x e^{3x}\\,dx$.",
            sol="<p>分部,$u=x$、$dv=e^{3x}dx$ ⟹ $v=\\dfrac{e^{3x}}{3}$:</p>"
                "$$\\left[\\frac{xe^{3x}}{3}\\right]_{0}^{1}"
                "-\\frac13\\int_{0}^{1}e^{3x}dx"
                "=\\frac{e^{3}}{3}-\\frac13\\left[\\frac{e^{3x}}{3}\\right]_{0}^{1}$$"
                "$$=\\frac{e^{3}}{3}-\\frac{e^{3}-1}{9}=\\frac{2e^{3}+1}{9}.$$"
                "<span style='color:#888'>[邊界項 2 分、剩餘積分 2 分、化簡 1 分]</span>"
                "<p>(數值約 $4.577$。)</p>"),
        Problem(
            label="4(f)", pts=4, level="hard",
            stem="Evaluate $\\displaystyle\\int\\sin^{3}x\\cos x\\,dx$, and state which technique "
                 "you used and why.",
            sol="<p><strong>換元</strong>,不是分部也不是三角降冪——因為 $\\cos x\\,dx$ 恰是 "
                "$d(\\sin x)$,被積式是「某函數 × 它自己的導數」。"
                "<span style='color:#888'>[說出理由 2 分]</span></p>"
                "<p>令 $t=\\sin x$、$dt=\\cos x\\,dx$:</p>"
                "$$\\int t^{3}dt=\\frac{t^{4}}{4}+C=\\frac{\\sin^{4}x}{4}+C.$$"
                "<span style='color:#888'>[計算 3 分]</span>"
                "<p>(若用奇次拆項法也對,但繞了遠路。)</p>"),
    ])

# ---------------------------------------------------------------- 第 5 題

G5 = ExamGroup(
    num=5, title="Problem 5 · Numerical Integration", origin="對應第 7 週",
    problems=[
        Problem(
            label="5(a)", pts=6, level="mid",
            stem="Apply Simpson's rule with $n=2$ to $\\displaystyle\\int_{0}^{2}x^{3}dx$. "
                 "Compare with the exact value and explain the result.",
            sol="<p>$h=1$,節點 $0,1,2$,函數值 $0,1,8$,係數 $1,4,1$:</p>"
                "$$S_{2}=\\frac13\\left[0+4(1)+8\\right]=4.$$"
                "<span style='color:#888'>[計算 3 分]</span>"
                "<p>精確值 $\\displaystyle\\int_{0}^{2}x^{3}dx"
                "=\\left[\\frac{x^{4}}{4}\\right]_{0}^{2}=4$。"
                "<strong>誤差為零</strong>。</p>"
                "<p><strong>理由</strong>:Simpson 雖然只用拋物線(二次)逼近,但對"
                "<strong>三次多項式也完全精確</strong>。原因是在對稱面板上,"
                "三次項(奇次)的積分為零,而 Simpson 公式本身也對稱、同樣消掉三次項。"
                "誤差公式含 $f^{(4)}$,而三次多項式的四階導數為 $0$。"
                "<span style='color:#888'>[理由 3 分]</span></p>"),
        Problem(
            label="5(b)", pts=10, level="hard",
            stem="(i) Use Simpson's rule with $n=4$ to estimate "
                 "$\\displaystyle\\int_{1}^{2}\\frac{dx}{x}$, giving 6 decimal places. &nbsp;[5] "
                 "&nbsp; (ii) Bound the error using "
                 "$\\left|\\int-S_{n}\\right|\\le\\frac{(b-a)h^{4}}{180}\\max\\left|f^{(4)}\\right|$, "
                 "and check that the true error respects your bound. &nbsp;[5]",
            sol="<p><strong>(i)</strong> $h=0.25$,節點 $1,1.25,1.5,1.75,2$,"
                "$f=1,\\,0.8,\\,0.\\overline{6},\\,0.571429,\\,0.5$,係數 $1,4,2,4,1$:</p>"
                "$$S_{4}=\\frac{0.25}{3}\\left[1+3.2+1.3\\overline{3}+2.285714+0.5\\right]"
                "=0.693254.$$"
                "<span style='color:#888'>[節點與函數值 2 分、係數 1 分、計算 2 分]</span>"
                "<p><strong>(ii)</strong> $f=x^{-1}$ ⟹ $f^{(4)}=\\dfrac{24}{x^{5}}$,"
                "在 $[1,2]$ 上最大值在 $x=1$,故 $M_{4}=24$:</p>"
                "$$\\left|\\text{誤差}\\right|\\le\\frac{1\\times(0.25)^{4}}{180}\\times24"
                "=\\frac{24}{180}\\times0.00390625\\approx5.21\\times10^{-4}.$$"
                "<span style='color:#888'>[求 $f^{(4)}$ 與 $M_4$ 3 分、代公式 1 分]</span>"
                "<p><strong>檢查</strong>:精確值 $\\ln2=0.693147$,真實誤差 "
                "$|0.693254-0.693147|\\approx1.07\\times10^{-4}$,"
                "確實小於界 $5.21\\times10^{-4}$ ✓ "
                "<span style='color:#888'>[驗證 1 分]</span></p>"),
    ])

# ---------------------------------------------------------------- 第 6 題

G6 = ExamGroup(
    num=6, title="Problem 6 · Improper Integrals", origin="對應第 8 週",
    problems=[
        Problem(
            label="6(a)", pts=4, level="basic",
            stem="Evaluate $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{5/2}}$ or show it "
                 "diverges.",
            sol="<p>$p=\\dfrac52&gt;1$,由 $p$ 判別法收斂。"
                "<span style='color:#888'>[判定 1 分]</span></p>"
                "$$\\int_{1}^{\\infty}x^{-5/2}dx=\\lim_{b\\to\\infty}"
                "\\left[\\frac{x^{-3/2}}{-3/2}\\right]_{1}^{b}"
                "=\\lim_{b\\to\\infty}\\frac23\\left(1-b^{-3/2}\\right)=\\frac23.$$"
                "<span style='color:#888'>[寫成極限 1 分、計算 2 分。"
                "直接代 $\\infty$ 未寫極限者扣 1 分]</span>"
                "<p>(也可直接用公式 $\\dfrac{1}{p-1}=\\dfrac{1}{3/2}=\\dfrac23$。)</p>"),
        Problem(
            label="6(b)", pts=4, level="mid",
            stem="Evaluate $\\displaystyle\\int_{0}^{1}\\frac{dx}{x^{2/3}}$ or show it diverges.",
            sol="<p>奇異點在 $x=0$。此處是 $(0,1]$ 上的 $p$ 判別法,"
                "$p=\\dfrac23&lt;1$ ⟹ <strong>收斂</strong>"
                "(注意不等號方向與 $[1,\\infty)$ 相反)。"
                "<span style='color:#888'>[判定與方向 2 分]</span></p>"
                "$$\\lim_{t\\to0^{+}}\\left[3x^{1/3}\\right]_{t}^{1}"
                "=\\lim_{t\\to0^{+}}3\\left(1-t^{1/3}\\right)=3.$$"
                "<span style='color:#888'>[計算 2 分]</span>"),
        Problem(
            label="6(c)", pts=8, level="hard",
            stem="(i) Find the constant $c$ making $p(x)=\\dfrac{c}{1+x^{2}}$ a probability "
                 "density on $[0,\\infty)$. &nbsp;[4] &nbsp; "
                 "(ii) Determine whether $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{1+x^{4}}$ "
                 "converges. State the test you use and verify its hypotheses. &nbsp;[4]",
            sol="<p><strong>(i)</strong> 要求 $\\displaystyle\\int_{0}^{\\infty}p=1$:</p>"
                "$$\\int_{0}^{\\infty}\\frac{dx}{1+x^{2}}"
                "=\\lim_{b\\to\\infty}\\Big[\\arctan x\\Big]_{0}^{b}=\\frac{\\pi}{2}.$$"
                "<span style='color:#888'>[算出積分 3 分]</span>"
                "<p>故 $c\\cdot\\dfrac{\\pi}{2}=1\\Rightarrow c=\\dfrac{2}{\\pi}$。"
                "<span style='color:#888'>[求 $c$ 1 分]</span></p>"
                "<p><strong>(ii)</strong> <strong>收斂</strong>,用比較審斂法。</p>"
                "<p>驗證前提:在 $[1,\\infty)$ 上 $0&lt;\\dfrac{1}{1+x^{4}}"
                "&lt;\\dfrac{1}{x^{4}}$(被積式非負,且被上界壓住)。"
                "<span style='color:#888'>[不等式與非負性 2 分]</span></p>"
                "<p>而 $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{4}}$ 收斂"
                "($p=4&gt;1$,值為 $\\frac13$)。由比較審斂法,原積分收斂,且其值 "
                "$&lt;\\dfrac13$。<span style='color:#888'>[引用 $p$ 判別法並下結論 2 分]</span></p>"
                "<p>(用極限比較法取 $g=x^{-4}$、極限為 $1$ 亦可,同樣給滿分。)</p>"),
    ])

EXAM = ExamPaper(week=9, name="期中考", name_en="Midterm Examination",
                 minutes=100, groups=[G1, G2, G3, G4, G5, G6])

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("P1(a) delta=eps/5 代回 5*delta 得 eps", "5*(eps/5)", "eps"),
    ("P1(b) lim sqrt(x^2+3x)-x", "limit(sqrt(x**2+3*x)-x, x, oo)", "Rational(3,2)"),
    ("P1(c) sin(pi/x) at x=2/5 是 1", "sin(pi/Rational(2,5))", "1"),
    ("P2(a) (f^-1)'(3) = 1/f'(1) = 1/5", "1/diff(x**3+2*x, x).subs(x, 1)", "Rational(1,5)"),
    ("P2(b) d/dx arctan(x^2)", "simplify(diff(atan(x**2), x) - 2*x/(1+x**4))", "0"),
    ("P2(c) d/dx tanh(3x) = 3(1-tanh^2(3x))",
     "simplify(diff(tanh(3*x), x) - 3*(1-tanh(3*x)**2))", "0"),
    ("P3(a) lim (e^x-1-x-x^2/2)/x^3",
     "limit((exp(x)-1-x-x**2/2)/x**3, x, 0)", "Rational(1,6)"),
    ("P3(b) P3 of ln(1+x)", "series(log(1+x), x, 0, 4).removeO()", "x - x**2/2 + x**3/3"),
    ("P3(c)(i) 餘項界 0.2^5/120", "Rational(2,10)**5/factorial(5)", "Rational(1,375000)"),
    ("P3(c)(i) 實際誤差 < 界",
     "1 if Abs(Rational(2,10) - Rational(2,10)**3/6 - sin(Rational(2,10))).evalf() "
     "< (Rational(2,10)**5/factorial(5)).evalf() else 0", "1"),
    ("P4(a) ∫x^2 e^-x dx",
     "simplify(integrate(x**2*exp(-x), x) - (-(x**2+2*x+2)*exp(-x)))", "0"),
    ("P4(b) ∫dx/sqrt(4-x^2)", "simplify(integrate(1/sqrt(4-x**2), x) - asin(x/2))", "0"),
    ("P4(c) 遮蓋法係數 4/3", "((3*x+1)/(x+2)).subs(x, 1)", "Rational(4,3)"),
    ("P4(c) 遮蓋法係數 5/3", "((3*x+1)/(x-1)).subs(x, -2)", "Rational(5,3)"),
    ("P4(d) ∫ln(x)/x^2 dx",
     "simplify(integrate(log(x)/x**2, x) - (-(log(x)+1)/x))", "0"),
    ("P4(e) ∫_0^1 x e^(3x) dx = (2e^3+1)/9",
     "simplify(integrate(x*exp(3*x), (x, 0, 1)) - (2*exp(3)+1)/9)", "0"),
    ("P4(f) ∫sin^3 x cos x dx", "simplify(integrate(sin(x)**3*cos(x), x) - sin(x)**4/4)", "0"),
    ("P5(a) S_2 for x^3 on [0,2] = 4 = 精確值",
     "Rational(1,3)*(0 + 4*1 + 8) - integrate(x**3, (x, 0, 2))", "0"),
    ("P5(b)(i) S_4 for 1/x on [1,2] 的六位數",
     "floor(Rational(1,4)/3*(1 + 4*Rational(4,5) + 2*Rational(2,3) + 4*Rational(4,7) "
     "+ Rational(1,2)) * 10**6)", "693253"),
    ("P5(b)(ii) M_4 = 24", "Abs(diff(1/x, x, 4).subs(x, 1))", "24"),
    ("P5(b)(ii) 誤差界 = 24/180*(1/4)^4",
     "Rational(1,4)**4/180*24", "Rational(1,1920)"),
    ("P6(a) ∫_1^oo x^(-5/2) = 2/3", "integrate(x**Rational(-5,2), (x, 1, oo))", "Rational(2,3)"),
    ("P6(b) ∫_0^1 x^(-2/3) = 3", "integrate(x**Rational(-2,3), (x, 0, 1))", "3"),
    ("P6(c)(i) ∫_0^oo dx/(1+x^2) = pi/2", "integrate(1/(1+x**2), (x, 0, oo))", "pi/2"),
    ("P6(c)(i) c = 2/pi", "1/integrate(1/(1+x**2), (x, 0, oo))", "2/pi"),
    ("P6(c)(ii) ∫_1^oo dx/x^4 = 1/3", "integrate(1/x**4, (x, 1, oo))", "Rational(1,3)"),
]
