# -*- coding: utf-8 -*-
"""第 18 週｜證明總整理與期末考

沒有例題、沒有 Lab。這一週只做兩件事:
 1. 理論教案:把全學期 15 個證明時刻串成一張地圖(誰用到誰)
 2. 期末考:考卷版 + 詳解版,主考 W10–W17,應用題自然用到 W4–W8 的技巧
所有答案已用 sympy 驗證。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Problem, ExamGroup, ExamPaper, LessonPlan, Week

# ================================================================ 證明地圖

PROOF_MAP = [
    (1, "用 $\\varepsilon$-$\\delta$ 證 $\\lim_{x\\to2}(3x-1)=5$",
     "由 $\\varepsilon$ 反推 $\\delta$ 的兩欄書寫格式", "W8 的比較審斂法也用同一種嚴謹度"),
    (2, "反函數微分公式 $\\left(f^{-1}\\right)'=\\dfrac{1}{f'}$",
     "對 $f(f^{-1}(x))=x$ 微分,用鏈鎖法則", "W5 的三角代換合法性、W11 的弧長參數化"),
    (3, "L'Hôpital 法則",
     "Cauchy MVT 在 $[a,x]$ 上,$f(a)=g(a)=0$ 讓左式塌縮", "W7 的 Simpson 誤差、W16 的線性化"),
    (4, "分部積分 $\\int u\\,dv=uv-\\int v\\,du$",
     "乘積法則兩邊積分,左邊用 FTC", "W12 的期望值計算、W15 的積分因子"),
    (5, "三角代換的合法性(需一對一 + 值域蓋住)",
     "換元要能換回去 ⟹ 需要反函數(收 W2)", "所有含根號的積分"),
    (6, "部分分式的分解定理(數維度)",
     "未知數個數 = 分母次數,係數矩陣可逆", "→ 線性代數的 $M\\mathbf{c}=\\mathbf{b}$"),
    (7, "Simpson 誤差是 $O(h^{4})$",
     "對稱面板上奇次項全消,三次項也一起消失", "W15 的 RK4($1,2,2,1$ 就是 $1,4,1$)"),
    (8, "比較審斂法",
     "單調有界必收斂(實數完備性)", "W12 的期望值存在性、W16 的穩定性"),
    (10, "旋轉體體積 $V=\\int\\pi f^{2}dx$",
     "切→近似成圓柱→加總→取極限", "W11 弧長、W12 功與期望值(同一心法)"),
    (11, "弧長 $L=\\int\\sqrt{1+(f')^{2}}dx$",
     "畢氏定理提出 $\\Delta x$,再用 MVT(收 W3)", "W13 參數式與極座標弧長"),
    (12, "期望值 $\\mathbb{E}[X]=\\int xp\\,dx$",
     "離散加權平均取極限;與質心公式同構", "W17 的 loss 是期望損失的 MC 估計"),
    (13, "極座標面積 $A=\\frac12\\int r^{2}d\\theta$",
     "切<strong>扇形</strong>不是矩形", "任何以原點為中心的對稱問題"),
    (14, "分離變數的合法性",
     "兩邊對 $t$ 積分 + 左邊換元;除法會吃掉平衡解", "W15 的積分因子(用它解出 $\\mu$)"),
    (15, "積分因子 $\\mu=e^{\\int p}$",
     "要讓左邊成為 $(\\mu y)'$ ⟹ 需 $\\mu'=\\mu p$ ⟹ 可分離", "W16 的梯度流解析解"),
    (16, "平衡點穩定性判準 $f'(y^{*})$ 的符號",
     "平衡點讓泰勒第一項消失,剩 $u'=f'(y^{*})u$", "W17 的 learning rate 上限 $2/L''$"),
]

# ================================================================ 期末考

G1 = ExamGroup(
    num=1, title="Problem 1 · Area and Volume", origin="對應第 10 週",
    problems=[
        Problem(
            label="1(a)", pts=5, level="basic",
            stem="Find the area of the region enclosed by $y=x^{2}$ and $y=2x$.",
            sol="<p>交點:$x^{2}=2x\\Rightarrow x=0,2$。在 $(0,2)$ 上 $2x&gt;x^{2}$。"
                "<span style='color:#888'>[求交點並判斷上下 2 分]</span></p>"
                "$$A=\\int_{0}^{2}\\left(2x-x^{2}\\right)dx"
                "=\\left[x^{2}-\\frac{x^{3}}{3}\\right]_{0}^{2}=4-\\frac83=\\frac43.$$"
                "<span style='color:#888'>[積分 3 分]</span>"),
        Problem(
            label="1(b)", pts=5, level="mid",
            stem="The region under $y=\\sqrt{x}$ on $[0,4]$ is rotated about the $x$-axis. Find "
                 "the volume.",
            sol="<p>圓盤法(繞 $x$ 軸、函數已是 $y=f(x)$,不必反解):</p>"
                "$$V=\\int_{0}^{4}\\pi\\left(\\sqrt x\\right)^{2}dx=\\pi\\int_{0}^{4}x\\,dx"
                "=\\pi\\left[\\frac{x^{2}}{2}\\right]_{0}^{4}=8\\pi.$$"
                "<span style='color:#888'>[選對方法 2 分、記得平方 1 分、積分 2 分]</span>"),
        Problem(
            label="1(c)", pts=6, level="hard",
            stem="The region under $y=x^{2}$ on $[0,2]$ is rotated about the $y$-axis. Find the "
                 "volume, and state which method you used and why.",
            sol="<p><strong>殼層法</strong>——繞 $y$ 軸但函數是 $y=f(x)$,"
                "用圓盤要先反解 $x=\\sqrt y$。"
                "<span style='color:#888'>[說出理由 2 分]</span></p>"
                "$$V=\\int_{0}^{2}2\\pi x\\cdot x^{2}dx=2\\pi\\int_{0}^{2}x^{3}dx"
                "=2\\pi\\left[\\frac{x^{4}}{4}\\right]_{0}^{2}=8\\pi.$$"
                "<span style='color:#888'>[列式 2 分、計算 2 分。漏掉半徑 $x$ 者扣 2 分]</span>"),
    ])

G2 = ExamGroup(
    num=2, title="Problem 2 · Arc Length and Surface Area", origin="對應第 11 週",
    problems=[
        Problem(
            label="2(a)", pts=6, level="mid",
            stem="Find the arc length of $y=\\tfrac{2}{3}x^{3/2}$ on $[0,3]$.",
            sol="<p>$f'=\\sqrt x$,故 $\\sqrt{1+\\left(f'\\right)^{2}}=\\sqrt{1+x}$:</p>"
                "$$L=\\int_{0}^{3}\\sqrt{1+x}\\,dx"
                "=\\left[\\frac23(1+x)^{3/2}\\right]_{0}^{3}=\\frac23(8-1)=\\frac{14}{3}.$$"
                "<span style='color:#888'>[被積式 3 分(裡面是<strong>導數</strong>的平方)、"
                "積分 3 分]</span>"),
        Problem(
            label="2(b)", pts=8, level="hard",
            stem="The line $y=x$ on $[0,2]$ is rotated about the $x$-axis. Find the surface area, "
                 "and explain why the width of each band is not $dx$.",
            sol="<p>$f'=1$,斜長因子 $\\sqrt{1+1}=\\sqrt2$:</p>"
                "$$S=\\int_{0}^{2}2\\pi x\\cdot\\sqrt2\\,dx"
                "=2\\sqrt2\\,\\pi\\left[\\frac{x^{2}}{2}\\right]_{0}^{2}=4\\sqrt2\\,\\pi.$$"
                "<span style='color:#888'>[被積式含斜長 3 分、積分 2 分]</span>"
                "<p><strong>為什麼不是 $dx$</strong>:曲面是沿著<strong>曲線</strong>展開的,"
                "不是沿 $x$ 軸的投影。曲線越陡,同樣的 $dx$ 對應越寬的曲面帶。"
                "用 $dx$ 會系統性低估(這裡會少 $\\sqrt2$ 倍)。"
                "<span style='color:#888'>[說明 3 分]</span></p>"
                "<p>(驗算:圓錐側面積 $\\pi r\\ell=\\pi\\cdot2\\cdot2\\sqrt2=4\\sqrt2\\pi$ ✓)</p>"),
    ])

G3 = ExamGroup(
    num=3, title="Problem 3 · Averages and Expected Value", origin="對應第 12 週",
    problems=[
        Problem(
            label="3(a)", pts=4, level="basic",
            stem="Find the average value of $f(x)=x^{3}$ on $[0,2]$.",
            sol="$$f_{\\text{avg}}=\\frac{1}{2-0}\\int_{0}^{2}x^{3}dx"
                "=\\frac12\\left[\\frac{x^{4}}{4}\\right]_{0}^{2}=\\frac12\\cdot4=2.$$"
                "<span style='color:#888'>[除以<strong>區間長度</strong> 2 分、積分 2 分]</span>"),
        Problem(
            label="3(b)", pts=5, level="mid",
            stem="Find the constant $c$ that makes $p(x)=ce^{-3x}$ a probability density on "
                 "$[0,\\infty)$.",
            sol="<p>$\\displaystyle\\int_{0}^{\\infty}e^{-3x}dx"
                "=\\lim_{b\\to\\infty}\\left[-\\frac{e^{-3x}}{3}\\right]_{0}^{b}=\\frac13$。"
                "<span style='color:#888'>[瑕積分寫成極限 3 分]</span></p>"
                "<p>要總積分為 1:$\\dfrac{c}{3}=1\\Rightarrow c=3$。"
                "<span style='color:#888'>[求 $c$ 2 分]</span></p>"),
        Problem(
            label="3(c)", pts=7, level="hard",
            stem="For the density $p(x)=3e^{-3x}$ on $[0,\\infty)$, compute $\\mathbb{E}[X]$ and "
                 "$\\operatorname{Var}(X)$.",
            sol="<p><strong>期望值</strong>(分部積分):</p>"
                "$$\\mathbb{E}[X]=\\int_{0}^{\\infty}3xe^{-3x}dx=\\frac13.$$"
                "<span style='color:#888'>[3 分]</span>"
                "<p><strong>二階矩</strong>(再分部一次):</p>"
                "$$\\mathbb{E}\\left[X^{2}\\right]=\\int_{0}^{\\infty}3x^{2}e^{-3x}dx"
                "=\\frac{2}{9}.$$"
                "<span style='color:#888'>[2 分]</span>"
                "<p><strong>變異數</strong>(用捷徑公式):</p>"
                "$$\\operatorname{Var}(X)=\\mathbb{E}\\left[X^{2}\\right]-\\mu^{2}"
                "=\\frac29-\\frac19=\\frac19.$$"
                "<span style='color:#888'>[2 分。寫成 $\\mu^{2}-\\mathbb{E}[X^{2}]$ 者 0 分]</span>"
                "<p>(指數分佈的 $\\mathbb{E}[X]=\\frac1\\lambda$、"
                "$\\operatorname{Var}=\\frac{1}{\\lambda^{2}}$,此處 $\\lambda=3$ ✓)</p>"),
    ])

G4 = ExamGroup(
    num=4, title="Problem 4 · Parametric Curves and Polar Coordinates", origin="對應第 13 週",
    problems=[
        Problem(
            label="4(a)", pts=4, level="basic",
            stem="For $x=t^{2}$, $y=t^{3}$, find $\\dfrac{dy}{dx}$ and the points where the "
                 "tangent is vertical.",
            sol="$$\\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}=\\frac{3t^{2}}{2t}=\\frac{3t}{2}"
                "\\quad(t\\ne0).$$"
                "<span style='color:#888'>[2 分]</span>"
                "<p><strong>鉛直切線</strong>需 $\\dfrac{dx}{dt}=2t=0$ 且 "
                "$\\dfrac{dy}{dt}\\ne0$。但 $t=0$ 時 $\\dfrac{dy}{dt}=3t^{2}=0$ <strong>也</strong>為零"
                "——這是<strong>尖點</strong>,不是鉛直切線。"
                "<span style='color:#888'>[2 分。答「$t=0$ 有鉛直切線」者只給 1 分]</span></p>"),
        Problem(
            label="4(b)", pts=6, level="mid",
            stem="Find the area enclosed by the polar curve $r=3\\cos\\theta$. State your range "
                 "of $\\theta$ and why.",
            sol="<p>$r=3\\cos\\theta$ 是通過原點、直徑 $3$ 的圓。"
                "$\\theta\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 就畫完一整圈"
                "(超過 $r$ 會變負、重畫一遍)。"
                "<span style='color:#888'>[範圍與理由 3 分]</span></p>"
                "$$A=\\frac12\\int_{-\\pi/2}^{\\pi/2}9\\cos^{2}\\theta\\,d\\theta"
                "=\\frac92\\cdot\\frac{\\pi}{2}=\\frac{9\\pi}{4}.$$"
                "<span style='color:#888'>[計算 3 分。取 $[0,2\\pi]$ 得 $\\frac{9\\pi}{2}$ 者扣 3 分]</span>"
                "<p>(驗算:半徑 $\\frac32$ 的圓面積 $=\\pi\\left(\\frac32\\right)^{2}"
                "=\\frac{9\\pi}{4}$ ✓)</p>"),
        Problem(
            label="4(c)", pts=6, level="mid",
            stem="Find the arc length of $x=\\cos t$, $y=\\sin t$ for $t\\in[0,\\pi]$, and explain "
                 "what the integrand represents physically.",
            sol="$$\\dot x^{2}+\\dot y^{2}=\\sin^{2}t+\\cos^{2}t=1"
                "\\ \\Longrightarrow\\ L=\\int_{0}^{\\pi}1\\,dt=\\pi.$$"
                "<span style='color:#888'>[3 分。這是單位圓的半周長 ✓]</span>"
                "<p><strong>物理意義</strong>:$\\sqrt{\\dot x^{2}+\\dot y^{2}}$ 是"
                "<strong>速率</strong>(速度向量的長度)。弧長 = 速率對時間積分 = <strong>總路程</strong>。"
                "此處速率恆為 1,走了 $\\pi$ 個時間單位,故路程 $\\pi$。"
                "<span style='color:#888'>[3 分]</span></p>"),
    ])

G5 = ExamGroup(
    num=5, title="Problem 5 · Differential Equations", origin="對應第 14–15 週",
    problems=[
        Problem(
            label="5(a)", pts=5, level="mid",
            stem="Solve $\\dfrac{dy}{dt}=2ty$ with $y(0)=3$.",
            sol="<p>可分離:$\\dfrac{dy}{y}=2t\\,dt$(暫設 $y\\ne0$)。積分:</p>"
                "$$\\ln|y|=t^{2}+C_{1}\\ \\Longrightarrow\\ y=Ce^{t^{2}}.$$"
                "<span style='color:#888'>[分離與積分 3 分]</span>"
                "<p>$y(0)=C=3$,故 $y=3e^{t^{2}}$。"
                "<span style='color:#888'>[初始條件 2 分]</span></p>"
                "<p>(平衡解 $y\\equiv0$ 對應 $C=0$,已含在通解中。)</p>"),
        Problem(
            label="5(b)", pts=7, level="hard",
            stem="Solve $y'+2y=e^{t}$ with $y(0)=0$ using an integrating factor.",
            sol="<p><strong>積分因子</strong>:$p=2$,故 $\\mu=e^{2t}$。"
                "<span style='color:#888'>[2 分]</span></p>"
                "<p>兩邊乘 $\\mu$,左邊成為 $\\left(e^{2t}y\\right)'$:</p>"
                "$$\\left(e^{2t}y\\right)'=e^{2t}e^{t}=e^{3t}"
                "\\ \\Longrightarrow\\ e^{2t}y=\\frac{e^{3t}}{3}+C.$$"
                "<span style='color:#888'>[3 分]</span>"
                "<p>除以 $\\mu$(<strong>$C$ 也要除</strong>):"
                "$y=\\dfrac{e^{t}}{3}+Ce^{-2t}$。</p>"
                "<p>$y(0)=\\dfrac13+C=0\\Rightarrow C=-\\dfrac13$,故</p>"
                "$$y=\\frac{e^{t}-e^{-2t}}{3}.$$"
                "<span style='color:#888'>[2 分。$C$ 沒除者扣 2 分]</span>"),
        Problem(
            label="5(c)", pts=4, level="mid",
            stem="A radioactive substance has a half-life of $8$ days. How long until only "
                 "$\\tfrac18$ of the original amount remains?",
            sol="<p>$\\dfrac18=\\left(\\dfrac12\\right)^{3}$——恰好 <strong>3 個半衰期</strong>:</p>"
                "$$t=3\\times8=24\\ \\text{days}.$$"
                "<span style='color:#888'>[認出是 3 個半衰期 3 分、答案 1 分]</span>"
                "<p>(硬算也可:$k=\\frac{\\ln2}{8}$,解 $e^{-kt}=\\frac18$ 得 "
                "$t=\\frac{8\\ln8}{\\ln2}=24$。)</p>"),
        Problem(
            label="5(d)", pts=6, level="mid",
            stem="Apply Euler's method with $h=0.5$ to $y'=y-t$, $y(0)=1$, for two steps. Then "
                 "state the order of the global error and justify it in one sentence.",
            sol="<p><strong>迭代</strong> $y_{n+1}=y_{n}+h\\left(y_{n}-t_{n}\\right)$:</p>"
                "<p class='step'>$y_{1}=1+0.5(1-0)=1.5$($t=0.5$)</p>"
                "<p class='step'>$y_{2}=1.5+0.5(1.5-0.5)=2.0$($t=1$)</p>"
                "<span style='color:#888'>[每步 2 分,共 4 分]</span>"
                "<p><strong>全域誤差 $O(h)$</strong>:單步誤差是 $O(h^{2})$(泰勒的二階項),"
                "但走到固定時刻需要 $n=\\frac{T}{h}$ 步,"
                "$\\frac{T}{h}\\times O(h^{2})=O(h)$——<strong>累積掉一階</strong>。"
                "<span style='color:#888'>[2 分]</span></p>"),
    ])

G6 = ExamGroup(
    num=6, title="Problem 6 · Gradient Flow and Stability", origin="對應第 16–17 週",
    problems=[
        Problem(
            label="6(a)", pts=6, level="mid",
            stem="For $L(\\theta)=\\tfrac14\\theta^{4}-\\tfrac12\\theta^{2}$, write the gradient "
                 "flow, find its equilibria, and classify each as stable or unstable.",
            sol="<p><strong>梯度流</strong>:$L'=\\theta^{3}-\\theta$,故</p>"
                "$$\\theta'=-L'(\\theta)=-\\theta^{3}+\\theta=-\\theta(\\theta-1)(\\theta+1).$$"
                "<span style='color:#888'>[2 分。忘記負號者扣 2 分]</span>"
                "<p><strong>平衡點</strong>:$\\theta=0,\\pm1$。"
                "<span style='color:#888'>[1 分]</span></p>"
                "<p><strong>分類</strong>(用 $L''=3\\theta^{2}-1$,穩定 $\\iff L''&gt;0$):</p>"
                "<div class='tbl-wrap'><table><thead><tr><th>$\\theta^{*}$</th><th>$L''$</th>"
                "<th>分類</th></tr></thead><tbody>"
                "<tr><td>$-1$</td><td>$2&gt;0$</td><td><strong>穩定</strong>(局部極小)</td></tr>"
                "<tr><td>$0$</td><td>$-1&lt;0$</td><td><strong>不穩定</strong>(局部極大)</td></tr>"
                "<tr><td>$1$</td><td>$2&gt;0$</td><td><strong>穩定</strong>(局部極小)</td></tr>"
                "</tbody></table></div>"
                "<span style='color:#888'>[3 分]</span>"
                "<p>(所以初始值的正負決定收斂到哪個極小——這就是<strong>吸引域</strong>。)</p>"),
        Problem(
            label="6(b)", pts=5, level="mid",
            stem="For $L(\\theta)=\\tfrac{10}{2}\\theta^{2}$, gradient descent uses "
                 "$\\theta\\leftarrow\\theta-\\eta L'(\\theta)$. Find the largest stable $\\eta$ "
                 "and the $\\eta$ that converges fastest.",
            sol="<p>$L'=10\\theta$,故迭代為</p>"
                "$$\\theta_{n+1}=\\theta_{n}-10\\eta\\,\\theta_{n}"
                "=\\left(1-10\\eta\\right)\\theta_{n}.$$"
                "<span style='color:#888'>[寫出公比 2 分]</span>"
                "<p><strong>穩定</strong>需 $\\left|1-10\\eta\\right|&lt;1$,即</p>"
                "$$0&lt;\\eta&lt;\\frac{2}{10}=0.2.$$"
                "<span style='color:#888'>[2 分]</span>"
                "<p><strong>最快</strong>:公比為 $0$ 時一步到位,即 "
                "$\\eta=\\dfrac{1}{10}=0.1=\\dfrac{1}{L''}$——那正是牛頓法。"
                "<span style='color:#888'>[1 分]</span></p>"),
        Problem(
            label="6(c)", pts=5, level="hard",
            stem="Explain in three sentences why gradient descent <em>is</em> Euler's method (not "
                 "merely analogous), and what $\\eta$ corresponds to.",
            sol="<p><strong>參考答案</strong>(三句,要點齊全即給滿分):</p>"
                "<p class='step'>① 梯度流是自治方程 $\\theta'=-\\nabla L(\\theta)$,"
                "描述「連續地往下坡走」。"
                "<span style='color:#888'>[2 分]</span></p>"
                "<p class='step'>② 把 Euler 法 $y_{n+1}=y_{n}+hf(y_{n})$ 套上去,得 "
                "$\\theta_{n+1}=\\theta_{n}-h\\nabla L(\\theta_{n})$,"
                "與梯度下降的更新式<strong>完全相同</strong>(不只形式相似,是同一個式子)。"
                "<span style='color:#888'>[2 分]</span></p>"
                "<p class='step'>③ 因此 <strong>learning rate $\\eta$ 就是步長 $h$</strong>;"
                "$\\eta$ 太大會違反 Euler 的穩定條件而發散,上限由曲率決定"
                "($\\eta&lt;\\frac{2}{L''}$)。"
                "<span style='color:#888'>[1 分]</span></p>"
                "<p><strong>批改提醒</strong>:只寫「很像」或「都是迭代」不給分;"
                "必須指出<strong>兩個式子相同</strong>,以及 $\\eta=h$。</p>"),
    ])

EXAM = ExamPaper(week=18, name="期末考", name_en="Final Examination",
                 minutes=120, groups=[G1, G2, G3, G4, G5, G6])

# ================================================================ 教案

def _proof_table():
    rows = "".join(
        f"<tr><td>W{w}</td><td>{what}</td><td>{how}</td><td>{used}</td></tr>"
        for w, what, how, used in PROOF_MAP)
    return ('<div class="tbl-wrap"><table><thead><tr>'
            '<th>週</th><th>證明了什麼</th><th>關鍵一步</th><th>後來被誰用到</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>')


LESSON = LessonPlan(
    hook="這學期做了 15 次「證明時刻」。今天把它們攤在同一張桌上,"
         "然後你會看到一件事:<strong>它們互相咬合</strong>。"
         "W3 的均值定理撐起 W11 的弧長公式,W14 的分離變數解出 W15 的積分因子,"
         "而 W16 的線性化又回頭用了 W3 的泰勒。這不是十五個孤立的技巧,是一張網。",
    fastforward=[
        ("15 個證明時刻", "全學期累積", "今天全部回顧,但只講「誰用到誰」"),
        ("四招積分技巧", "W4–W6", "期末考的應用題會用到,快速複習"),
        ("積分的應用(面積/體積/弧長/期望值)", "W10–W12", "重點在<strong>心法</strong>不是公式"),
        ("參數式與極座標", "W13", "提醒範圍陷阱"),
        ("微分方程", "W14–W15", "分離變數與積分因子各練一題"),
        ("梯度流與 GD=Euler", "W16–W17", "考卷會考,務必能默寫那三行"),
    ],
    outcomes=[
        "說出 15 個證明時刻各自證了什麼,以及<strong>哪一步是關鍵</strong>。",
        "指出至少三組「前面的證明被後面用到」的關係。",
        "在期末考的應用題中,正確選出四招積分技巧。",
        "默寫「梯度下降就是 Euler 法」的三行推導。",
    ],
    clock=[
        ("00:00–00:10", "開場:今天不學新東西,把網織起來", "—"),
        ("00:10–00:50", "證明地圖:前半學期(W1–W8)", "—"),
        ("00:50–00:55", "休息", "—"),
        ("00:55–01:35", "證明地圖:後半學期(W10–W17)", "—"),
        ("01:35–01:40", "休息", "—"),
        ("01:40–02:20", "期末考題型與配分說明;現場練三題", "—"),
        ("02:20–02:50", "答疑(依學生提問調整)", "—"),
        ("02:50–03:00", "收尾:接到微積分(二)與線性代數", "—"),
    ],
    proof_moment="今天沒有新的證明時刻。今天是<strong>把 15 個證明時刻連成一張網</strong>——"
                 "重點不是重複證明,而是指出<strong>誰用到誰</strong>。"
                 "學生若能講出三組依賴關係,這學期的數學就真的長在腦子裡了。",
    script=[
        ("開場:一張網,不是十五個技巧(10 分)",
         "<p>「這學期每週都有一個『證明時刻』。有人記得幾個?」讓他們數。"
         "通常會說出三四個。</p>"
         "<p>「今天不是要你們背這 15 個證明。今天要看的是<strong>它們怎麼互相咬合</strong>。」</p>"
         "<p>舉一個立刻有感的例子:「W3 學的均值定理,你們以為考完就沒用了。"
         "但 W11 推弧長公式時,把 $\\frac{\\Delta y}{\\Delta x}$ 換成 $f'(x^{*})$ 的那一步"
         "——<strong>就是均值定理</strong>。」</p>"),
        ("證明地圖:前半(40 分)",
         "<p>把地圖表投出來,前八列逐一走過。<strong>每一列只花三分鐘</strong>,"
         "重點在最後一欄「後來被誰用到」。</p>"
         "<p>特別停留在三處:</p>"
         "<p class='step'><strong>W2 → W5</strong>:反函數微分的「需要一對一」,"
         "在三角代換的合法性裡變成「值域限制是拿掉絕對值的許可證」。</p>"
         "<p class='step'><strong>W3 → W7</strong>:泰勒展開在 Simpson 誤差分析裡,"
         "靠對稱性一次消掉奇次項與三次項。</p>"
         "<p class='step'><strong>W6 → 線性代數</strong>:部分分式的「數維度」論證,"
         "就是 $M\\mathbf{c}=\\mathbf{b}$ 可逆性的雛形。</p>"),
        ("證明地圖:後半(40 分)",
         "<p>後七列。<strong>強調那個貫穿的心法</strong>:</p>"
         "<p class='step'>W10 體積、W11 弧長、W12 功與期望值、W13 極座標面積——"
         "<strong>全部是「切→近似一片→加總→取極限」</strong>。"
         "唯一的差別是「一片」長什麼樣子:薄餅、弦、位移、扇形。</p>"
         "<p>「所以你們不是背了四個公式,是<strong>學會一個動作</strong>用了四次。」</p>"
         "<p>然後是最後三列的接力:"
         "<strong>W14 的分離變數解出 W15 的積分因子;W15 的積分因子解出 W16 的梯度流;"
         "W16 的線性化用回 W3 的泰勒。</strong></p>"
         "<p>收在 W17 那張對應表:「learning rate 的每一個現象,都指回這張網的某一格。」</p>"),
        ("期末考說明與現場練習(40 分)",
         "<p>宣布範圍與配比:主考 W10–W17,但應用題<strong>一定會用到 W4–W8 的積分技巧</strong>"
         "(算體積要積分、算期望值要分部積分)。</p>"
         "<p><strong>三個最容易失分的地方</strong>,現場各練一題:</p>"
         "<p class='step'>① 曲面積的寬是<strong>斜長</strong>不是 $dx$</p>"
         "<p class='step'>② 極座標面積的<strong>範圍</strong>(算成兩倍)</p>"
         "<p class='step'>③ 線性方程除以 $\\mu$ 時<strong>$C$ 也要除</strong></p>"
         "<p>再要求全班默寫一次「GD = Euler」的三行。<strong>這題一定會考</strong>。</p>"),
        ("收尾:兩條路(10 分)",
         "<p>「這學期你們把<strong>一維</strong>的故事走完了。接下來兩個方向:」</p>"
         "<p><strong>微積分(二)</strong>:泰勒多項式 → 泰勒級數(收斂性);"
         "一維 → 多變數(偏導數、梯度、Hessian);單重積分 → 重積分。"
         "「W8 的高斯積分,我用了雙重積分當驚喜——下學期你們會真的會做。」</p>"
         "<p><strong>線性代數</strong>:那個 $\\eta&lt;\\frac{2}{\\lambda_{\\max}}$ 的 "
         "$\\lambda$ 是<strong>特徵值</strong>;W6 的部分分式是 $M\\mathbf{c}=\\mathbf{b}$;"
         "W15 的「通解 = 特解 + 齊次解」是線性系統的普遍結構。"
         "「三個伏筆,下學期一起收。」</p>"),
    ],
    myths=[
        "以為證明時刻是「考完就丟」的裝飾。這張地圖的最後一欄就是反證。",
        "把四個積分應用當成四個公式背。它們是<strong>同一個心法</strong>的四次應用。",
        "以為期末只考 W10 之後。應用題必然用到 W4–W8 的積分技巧。",
        "曲面積用 $dx$ 當寬度。",
        "極座標面積的範圍取太大(算成兩倍)。",
        "線性方程除以 $\\mu$ 時把 $C$ 留在外面。",
        "把「GD 像 Euler」當答案。要指出<strong>兩個式子相同</strong>。",
    ],
    exit_check=[
        ("舉出一組「前面的證明被後面用到」的例子。",
         "任一組皆可,例如:W3 的均值定理被 W11 的弧長公式用到;"
         "W14 的分離變數被 W15 用來解出積分因子;W3 的泰勒被 W16 的線性化用到。"),
        ("面積、體積、弧長、極座標面積,共同的心法是什麼?四者的「一片」各是什麼?",
         "心法:<strong>切→近似一片→加總→取極限</strong>。"
         "一片分別是:垂直薄條、薄餅(圓盤/墊圈/殼層)、一小段弦、細扇形。"),
        ("默寫「梯度下降就是 Euler 法」的三行。",
         "① 梯度流 $\\theta'=-\\nabla L$;② Euler:"
         "$\\theta_{n+1}=\\theta_{n}+h\\left(-\\nabla L\\right)$;"
         "③ 即 $\\theta_{n+1}=\\theta_{n}-\\eta\\nabla L$,故 $\\eta=h$。"),
    ],
    homework=[
        "<strong>複習</strong>:期末考範圍主考 W10–W17,應用題會用到 W4–W8 的積分技巧。"
        "把<a href=\"W18-期末考-考卷版.html\">考卷版</a>當模擬題先做一遍,再對"
        "<a href=\"W18-期末考-詳解版.html\">詳解版</a>。",
        "<strong>自我檢查</strong>:把 15 個證明時刻寫在紙上,"
        "在每一個旁邊寫「它被誰用到」。寫不出來的那幾個,就是要補的地方。",
    ],
)

WEEK = Week(
    num=18,
    title="證明總整理與期末複習",
    subtitle="這學期做了 15 次證明時刻。今天把它們攤在同一張桌上,"
             "然後你會看到:<strong>它們互相咬合,是一張網不是十五個技巧</strong>。",
    lesson=LESSON,
    chips=["期末總整理"],
    exam_name="期末考",
)

# 把證明地圖塞進教案的 script(放在第一段之後)
LESSON.script.insert(1, ("全學期證明地圖", _proof_table()))

# ================================================================ 驗算登記

ANSWER_CHECKS = [
    ("P1(a) x^2 與 2x 之間面積 = 4/3", "integrate(2*x - x**2, (x, 0, 2))", "Rational(4,3)"),
    ("P1(b) sqrt(x) 繞 x 軸 [0,4] = 8pi", "integrate(pi*x, (x, 0, 4))", "8*pi"),
    ("P1(c) x^2 繞 y 軸 [0,2] 殼層 = 8pi", "integrate(2*pi*x*x**2, (x, 0, 2))", "8*pi"),
    ("P2(a) (2/3)x^(3/2) 在 [0,3] 弧長 = 14/3",
     "integrate(sqrt(1+x), (x, 0, 3))", "Rational(14,3)"),
    ("P2(b) y=x 繞 x 軸 [0,2] 曲面積 = 4*sqrt(2)*pi",
     "simplify(integrate(2*pi*x*sqrt(2), (x, 0, 2)) - 4*sqrt(2)*pi)", "0"),
    ("P2(b) 圓錐側面積公式驗算 pi*r*l", "simplify(pi*2*2*sqrt(2) - 4*sqrt(2)*pi)", "0"),
    ("P3(a) x^3 在 [0,2] 平均 = 2", "integrate(x**3, (x, 0, 2))/2", "2"),
    ("P3(b) c = 3", "1/integrate(exp(-3*x), (x, 0, oo))", "3"),
    ("P3(c) E[X] = 1/3", "integrate(3*x*exp(-3*x), (x, 0, oo))", "Rational(1,3)"),
    ("P3(c) E[X^2] = 2/9", "integrate(3*x**2*exp(-3*x), (x, 0, oo))", "Rational(2,9)"),
    ("P3(c) Var = 1/9", "Rational(2,9) - Rational(1,3)**2", "Rational(1,9)"),
    ("P4(a) dy/dx = 3t/2", "simplify(diff(t**3, t)/diff(t**2, t) - 3*t/2)", "0"),
    ("P4(a) t=0 時 dy/dt 也為零(尖點)", "diff(t**3, t).subs(t, 0)", "0"),
    ("P4(b) r=3cos θ 面積 = 9pi/4",
     "integrate((3*cos(theta))**2/2, (theta, -pi/2, pi/2))", "9*pi/4"),
    ("P4(b) 對照圓面積 pi*(3/2)^2", "pi*Rational(3,2)**2", "9*pi/4"),
    ("P4(b) 若誤取 [0,2pi] 會得兩倍",
     "integrate((3*cos(theta))**2/2, (theta, 0, 2*pi))", "9*pi/2"),
    ("P4(c) 單位圓 [0,pi] 弧長 = pi", "integrate(1, (t, 0, pi))", "pi"),
    ("P5(a) y=3e^(t^2) 滿足 y'=2ty",
     "simplify(diff(3*exp(t**2), t) - 2*t*3*exp(t**2))", "0"),
    ("P5(a) y(0)=3", "(3*exp(t**2)).subs(t, 0)", "3"),
    ("P5(b) y=(e^t - e^(-2t))/3 滿足 y'+2y=e^t",
     "simplify(diff((exp(t)-exp(-2*t))/3, t) + 2*(exp(t)-exp(-2*t))/3 - exp(t))", "0"),
    ("P5(b) y(0)=0", "((exp(t)-exp(-2*t))/3).subs(t, 0)", "0"),
    ("P5(c) 剩 1/8 需 24 天",
     "solve(Eq(exp(-log(2)/8*t), Rational(1,8)), t)[0]", "24"),
    ("P5(d) Euler 第一步 = 1.5", "1 + Rational(1,2)*(1-0)", "Rational(3,2)"),
    ("P5(d) Euler 第二步 = 2.0",
     "Rational(3,2) + Rational(1,2)*(Rational(3,2) - Rational(1,2))", "2"),
    ("P6(a) L' = theta^3 - theta", "simplify(diff(x**4/4 - x**2/2, x) - (x**3 - x))", "0"),
    ("P6(a) 平衡點 0, ±1", "solve(Eq(x**3 - x, 0), x)[1]", "0"),
    ("P6(a) L''(1) = 2 > 0 穩定", "diff(x**4/4 - x**2/2, x, 2).subs(x, 1)", "2"),
    ("P6(a) L''(0) = -1 < 0 不穩定", "diff(x**4/4 - x**2/2, x, 2).subs(x, 0)", "-1"),
    ("P6(b) 最大穩定 eta = 0.2", "Rational(2,10)", "Rational(1,5)"),
    ("P6(b) 最快 eta = 0.1(公比 0)", "1 - Rational(1,10)*10", "0"),
]
