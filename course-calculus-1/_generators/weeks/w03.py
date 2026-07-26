# -*- coding: utf-8 -*-
"""第 3 週｜Cauchy 均值定理、L'Hôpital 的證明與泰勒多項式

銜接課把 L'Hôpital 當工具用了一整週,但從沒說過它為什麼成立。這週補上——
而且要順便拆穿一個常見的循環論證:用 L'Hôpital 算 lim sin(x)/x 是不合法的。
證明時刻:由 Cauchy MVT 推出 L'Hôpital 法則。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Rolle and the Mean Value Theorem", title_zh="洛爾定理與均值定理回顧",
    sub="Rolle is the special case; MVT is Rolle with the picture tilted",
    idea="Rolle: if $f$ is continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a)=f(b)$, then "
         "$f'(c)=0$ for some $c\\in(a,b)$. MVT: drop the requirement $f(a)=f(b)$ and the "
         "conclusion becomes $f'(c)=\\dfrac{f(b)-f(a)}{b-a}$.",
    deep="<p>銜接課講過這兩條,這裡<strong>只複習兩件事</strong>,因為它們是本週證明的地基。</p>"
         "<p class='step'><strong>第一:MVT 就是傾斜版的 Rolle</strong>。把割線減掉:</p>"
         "$$g(x)=f(x)-\\left[f(a)+\\frac{f(b)-f(a)}{b-a}(x-a)\\right].$$"
         "<p>則 $g(a)=g(b)=0$,對 $g$ 用 Rolle 得 $g'(c)=0$,展開就是 MVT。"
         "<strong>「減掉割線」這個動作</strong>是本週的主角——等一下證 Cauchy MVT 還要再用一次。</p>"
         "<p class='step'><strong>第二:前提缺一不可</strong>。$f(x)=|x|$ 在 $[-1,1]$ 上 "
         "$f(-1)=f(1)$ 卻找不到 $f'(c)=0$,因為它在 $0$ 不可微。這不是反例,是前提沒滿足。</p>"
         "<p>提醒學生:接下來三個定理(Cauchy MVT、L'Hôpital、Taylor)"
         "<strong>全部</strong>是用同一招證出來的——造一個輔助函數,讓它兩端相等,套 Rolle。"
         "看穿這件事,本週就沒有難的東西了。<span class='qed'>∎</span></p>",
    guide=["Rolle 的三個前提是什麼?哪一個在 $f(x)=|x|$ 上不成立?",
           "要把 Rolle 推廣成 MVT,我們從 $f$ 減掉什麼?(想:讓兩端變成一樣高)",
           "令 $g(x)=f(x)-[\\,$割線$\\,]$,則 $g(a)=$ <span class=\"blank\"></span>、"
           "$g(b)=$ <span class=\"blank\"></span>。",
           "對 $g$ 用 Rolle 得 $g'(c)=0$,把它展開,會得到什麼式子?"],
    demo="Derive the Mean Value Theorem from Rolle's Theorem by constructing a suitable auxiliary "
         "function.",
    demo_sol="<p>令 $m=\\dfrac{f(b)-f(a)}{b-a}$(割線斜率),定義</p>"
             "$$g(x)=f(x)-f(a)-m(x-a).$$"
             "<p>則 $g(a)=0$,且 $g(b)=f(b)-f(a)-m(b-a)=0$。$g$ 承襲 $f$ 的連續與可微性,"
             "三個前提齊備,由 Rolle 存在 $c\\in(a,b)$ 使 $g'(c)=0$。而</p>"
             "$$g'(x)=f'(x)-m\\ \\Longrightarrow\\ f'(c)=m=\\frac{f(b)-f(a)}{b-a}.\\;\\blacksquare$$",
    demo_hint="想辦法造一個函數,讓它在 $a$ 和 $b$ 的值<strong>相等</strong>,這樣才能用 Rolle。",
    misstep="輔助函數造好後忘了檢查它<strong>也</strong>滿足連續與可微。$g$ 是 $f$ 減一個多項式,"
            "所以自動繼承,但要說出來。",
    level="basic",
    drills=[
        ("Find all $c$ guaranteed by the MVT for $f(x)=x^{2}$ on $[0,3]$.",
         "<p>割線斜率 $=\\dfrac{9-0}{3}=3$。$f'(x)=2x=3\\Rightarrow c=\\dfrac32\\in(0,3)$。</p>"),
        ("Verify Rolle's Theorem for $f(x)=x^{2}-4x+3$ on $[1,3]$ and find $c$.",
         "<p>$f(1)=f(3)=0$,多項式處處連續可微。$f'(x)=2x-4=0\\Rightarrow c=2\\in(1,3)$。</p>"),
        ("Explain why $f(x)=x^{2/3}$ on $[-1,1]$ has no $c$ with $f'(c)=0$, without contradicting "
         "Rolle.",
         "<p>$f(-1)=f(1)=1$,但 $f'(x)=\\dfrac{2}{3x^{1/3}}$ 在 $x=0$ 不存在,"
         "不滿足「在 $(a,b)$ 上可微」的前提,故定理不保證有 $c$。</p>"),
    ])

C2 = Concept(
    title_en="Cauchy's Mean Value Theorem", title_zh="柯西均值定理",
    sub="Two functions racing at once — the ratio of speeds equals the ratio of distances",
    idea="If $f,g$ are continuous on $[a,b]$, differentiable on $(a,b)$, and $g'\\ne0$ on $(a,b)$, "
         "then there is $c\\in(a,b)$ with "
         "$$\\frac{f'(c)}{g'(c)}=\\frac{f(b)-f(a)}{g(b)-g(a)}.$$ "
         "Taking $g(x)=x$ recovers the ordinary MVT.",
    deep="<p>Cauchy MVT 是 MVT 的<strong>雙函數版</strong>,而它存在的唯一理由,"
         "就是為了證 L'Hôpital。先把它證出來,下一個觀念就水到渠成。</p>"
         "<p><strong>證明</strong>,還是那一招——造一個兩端相等的輔助函數:</p>"
         "$$h(x)=\\bigl[f(b)-f(a)\\bigr]\\,g(x)-\\bigl[g(b)-g(a)\\bigr]\\,f(x).$$"
         "<p class='step'>算兩端:</p>"
         "$$h(a)=f(b)g(a)-f(a)g(a)-g(b)f(a)+g(a)f(a)=f(b)g(a)-g(b)f(a),$$"
         "$$h(b)=f(b)g(b)-f(a)g(b)-g(b)f(b)+g(a)f(b)=g(a)f(b)-f(a)g(b).$$"
         "<p class='step'>兩者相等!由 Rolle 存在 $c$ 使 $h'(c)=0$,即</p>"
         "$$\\bigl[f(b)-f(a)\\bigr]g'(c)=\\bigl[g(b)-g(a)\\bigr]f'(c).$$"
         "<p>因 $g'\\ne0$,由 Rolle 也可知 $g(b)\\ne g(a)$(否則 $g$ 會有 $g'=0$ 的點),"
         "兩邊同除即得結論。$\\;\\blacksquare$</p>"
         "<p><strong>直覺</strong>:兩台車同時跑,$f$ 跑的總距離比 $g$ 跑的總距離,"
         "等於<strong>某一瞬間</strong>兩車速度的比。這句話比公式好記。</p>"
         "<p><strong>注意不能偷懶</strong>:有人會想「對 $f$ 和 $g$ 各用一次 MVT 再相除」——"
         "那是<strong>錯的</strong>,因為兩次得到的 $c$ 不見得是同一個。Cauchy MVT 的價值就在"
         "「<strong>同一個</strong> $c$」。<span class='qed'>∎</span></p>",
    guide=["若取 $g(x)=x$,Cauchy MVT 會變成什麼?(算算看 $g'$ 和 $g(b)-g(a)$)",
           "為了用 Rolle,我們要造一個 $h$ 使 $h(a)=h(b)$。試試 "
           "$h=[f(b)-f(a)]g(x)-[g(b)-g(a)]f(x)$,算 $h(a)$ 與 $h(b)$。",
           "$h'(c)=0$ 展開後是 <span class=\"blank\"></span>,移項就得到結論。",
           "有人說「對 $f$、$g$ 各用一次 MVT 再相除」也行。哪裡錯了?"],
    demo="Prove Cauchy's Mean Value Theorem, and verify it for $f(x)=x^{2}$, $g(x)=x^{3}$ on "
         "$[1,2]$.",
    demo_sol="<p><strong>證明</strong>:令 $h(x)=[f(b)-f(a)]g(x)-[g(b)-g(a)]f(x)$。直接計算得 "
             "$h(a)=h(b)=f(b)g(a)-f(a)g(b)$,由 Rolle 存在 $c$ 使 $h'(c)=0$,即"
             "$[f(b)-f(a)]g'(c)=[g(b)-g(a)]f'(c)$,整理即得。</p>"
             "<p><strong>驗證</strong>:右式 $=\\dfrac{4-1}{8-1}=\\dfrac37$。左式 "
             "$\\dfrac{f'(c)}{g'(c)}=\\dfrac{2c}{3c^{2}}=\\dfrac{2}{3c}$。令兩者相等:</p>"
             "$$\\frac{2}{3c}=\\frac37\\ \\Longrightarrow\\ c=\\frac{14}{9}\\approx1.556\\in(1,2).\\;\\checkmark$$",
    demo_hint="輔助函數要湊到 $h(a)=h(b)$。驗證時把兩邊各自算出來再解 $c$。",
    misstep="以為可以對 $f$、$g$ 分別用 MVT 再相除。那樣得到的是<strong>兩個不同的</strong> $c$,"
            "不能相除。",
    level="mid",
    drills=[
        ("Verify Cauchy's MVT for $f(x)=x^{2}$, $g(x)=x$ on $[0,2]$ and find $c$.",
         "<p>右式 $=\\dfrac{4-0}{2-0}=2$;左式 $=\\dfrac{2c}{1}=2c$。故 $c=1\\in(0,2)$。"
         "($g=x$ 時就是普通 MVT。)</p>"),
        ("Verify Cauchy's MVT for $f(x)=x^{3}$, $g(x)=x^{2}$ on $[1,2]$.",
         "<p>右式 $=\\dfrac{8-1}{4-1}=\\dfrac73$;左式 $=\\dfrac{3c^{2}}{2c}=\\dfrac{3c}{2}$。"
         "故 $c=\\dfrac{14}{9}\\approx1.556\\in(1,2)$。</p>"),
        ("Why does Cauchy's MVT require $g'(x)\\ne0$ on $(a,b)$?",
         "<p>一來結論的左式有 $g'(c)$ 當分母;二來若某處 $g'=0$,可能導致 $g(a)=g(b)$,"
         "右式分母也會是零。$g'\\ne0$ 同時擋掉這兩種情況。</p>"),
    ])

C3 = Concept(
    title_en="Why L'Hôpital's Rule Works", title_zh="羅必達法則為何成立",
    sub="Cauchy's MVT, applied on the shrinking interval between a and x",
    idea="For the $\\tfrac00$ case: if $f(a)=g(a)=0$, then Cauchy's MVT on $[a,x]$ gives "
         "$\\dfrac{f(x)}{g(x)}=\\dfrac{f'(c_x)}{g'(c_x)}$ for some $c_x$ between $a$ and $x$. "
         "As $x\\to a$, $c_x$ is squeezed to $a$ too — so the two limits coincide.",
    deep="<p>這是本週的<strong>證明時刻</strong>。銜接課用了羅必達一整週卻不知道為什麼,今天補上。</p>"
         "<p><strong>設定</strong>:$f(a)=g(a)=0$,$f,g$ 在 $a$ 附近可微且 $g'\\ne0$,"
         "並假設 $\\displaystyle\\lim_{x\\to a}\\frac{f'(x)}{g'(x)}=L$ 存在。</p>"
         "<p class='step'><strong>第一步</strong>:在區間 $[a,x]$ 上用 Cauchy MVT。存在 $c_x$ 介於 "
         "$a$ 與 $x$ 之間,使</p>"
         "$$\\frac{f(x)-f(a)}{g(x)-g(a)}=\\frac{f'(c_x)}{g'(c_x)}.$$"
         "<p class='step'><strong>第二步</strong>:因為 $f(a)=g(a)=0$,左邊<strong>就是</strong> "
         "$\\dfrac{f(x)}{g(x)}$。這一步是整個證明的關鍵——$\\frac00$ 的條件在這裡被用掉了。</p>"
         "$$\\frac{f(x)}{g(x)}=\\frac{f'(c_x)}{g'(c_x)}.$$"
         "<p class='step'><strong>第三步</strong>:$c_x$ 被夾在 $a$ 與 $x$ 之間,所以 $x\\to a$ 時 "
         "$c_x\\to a$。取極限:</p>"
         "$$\\lim_{x\\to a}\\frac{f(x)}{g(x)}=\\lim_{x\\to a}\\frac{f'(c_x)}{g'(c_x)}=L.\\;\\blacksquare$$"
         "<p><strong>三個前提為什麼一個都不能少</strong>:</p>"
         "<ul>"
         "<li>沒有 $\\frac00$ ⟹ 第二步失效,左邊不等於 $\\dfrac{f}{g}$。這就是為什麼把羅必達"
         "用在非不定型上會得到錯答案。</li>"
         "<li>沒有 $g'\\ne0$ ⟹ Cauchy MVT 用不了。</li>"
         "<li>$\\lim\\dfrac{f'}{g'}$ 不存在 ⟹ 最後一步的等號沒有意義。注意這時"
         "<strong>不能</strong>反推說原極限不存在(觀念 4 有反例)。</li>"
         "</ul>"
         "<p>$\\frac{\\infty}{\\infty}$ 的版本證明更技術性,本課只講結論。<span class='qed'>∎</span></p>",
    guide=["在 $[a,x]$ 上對 $f$ 與 $g$ 用 Cauchy MVT,會得到 $\\dfrac{f(x)-f(a)}{g(x)-g(a)}=$ "
           "<span class=\"blank\"></span>。",
           "題目給了 $f(a)=g(a)=$ <span class=\"blank\"></span>,所以左邊可以簡化成 "
           "<span class=\"blank\"></span>。",
           "$c_x$ 被夾在 $a$ 與 $x$ 之間。當 $x\\to a$,$c_x$ 會怎樣?",
           "如果 $f(a)\\ne0$(不是 $\\frac00$ 型),上面哪一步會垮掉?"],
    demo="Prove L'Hôpital's Rule for the $\\tfrac00$ case using Cauchy's Mean Value Theorem.",
    demo_sol="<p>設 $f(a)=g(a)=0$,$f,g$ 在 $a$ 的去心鄰域可微,$g'\\ne0$,且 "
             "$\\displaystyle\\lim_{x\\to a}\\frac{f'(x)}{g'(x)}=L$。</p>"
             "<p>對任一 $x$(在該鄰域內),在 $[a,x]$ 上用 Cauchy MVT:存在 $c_x$ 介於兩者之間,</p>"
             "$$\\frac{f(x)-f(a)}{g(x)-g(a)}=\\frac{f'(c_x)}{g'(c_x)}.$$"
             "<p>代入 $f(a)=g(a)=0$:</p>"
             "$$\\frac{f(x)}{g(x)}=\\frac{f'(c_x)}{g'(c_x)}.$$"
             "<p>當 $x\\to a$ 時,由夾擠 $c_x\\to a$,故右式 $\\to L$。因此</p>"
             "$$\\lim_{x\\to a}\\frac{f(x)}{g(x)}=L.\\;\\blacksquare$$",
    demo_hint="關鍵是「$f(a)=g(a)=0$ 讓左邊變成 $\\dfrac{f(x)}{g(x)}$」這一步。",
    misstep="忘了說明 $c_x\\to a$。$c_x$ 隨 $x$ 變動,必須指出它被夾住,才能對它取極限。",
    level="hard",
    drills=[
        ("In the proof, exactly which step uses the hypothesis $f(a)=g(a)=0$?",
         "<p>第二步:把 Cauchy MVT 的左式 $\\dfrac{f(x)-f(a)}{g(x)-g(a)}$ 化簡成 "
         "$\\dfrac{f(x)}{g(x)}$ 時用掉。沒有這個條件,整個證明就斷了。</p>"),
        ("Apply L'Hôpital to $\\displaystyle\\lim_{x\\to0}\\frac{e^{x}-1-x}{x^{2}}$.",
         "<p>$\\frac00$ 型:$\\dfrac{e^{x}-1}{2x}$ 仍是 $\\frac00$,再一次得 "
         "$\\dfrac{e^{x}}{2}\\to\\dfrac12$。</p>"),
        ("Evaluate $\\displaystyle\\lim_{x\\to0}\\frac{\\cos x}{1+x}$. Should L'Hôpital be used?",
         "<p>不該。代入得 $\\dfrac{1}{1}=1$,不是不定型。若誤用羅必達會得到 "
         "$\\dfrac{-\\sin x}{1}\\to0$,<strong>錯誤答案</strong>——因為證明的第二步不成立。</p>"),
    ])

C4 = Concept(
    title_en="Circular Reasoning: the sin x / x Trap", title_zh="循環論證:sin x / x 的陷阱",
    sub="L'Hôpital 'proves' this limit only by assuming the answer",
    idea="Using L'Hôpital on $\\displaystyle\\lim_{x\\to0}\\frac{\\sin x}{x}$ requires knowing "
         "$(\\sin x)'=\\cos x$ — but that derivative is itself proved <em>from</em> this very "
         "limit. The argument is circular: it assumes what it sets out to prove.",
    deep="<p>這一段是本週最值得學生記一輩子的東西,而且很多課本會避開不談。</p>"
         "<p class='step'><strong>循環在哪</strong>:要用羅必達,得先知道 $(\\sin x)'=\\cos x$。"
         "而那條導數是怎麼來的?從定義:</p>"
         "$$(\\sin x)'=\\lim_{h\\to0}\\frac{\\sin(x+h)-\\sin x}{h}"
         "=\\sin x\\lim_{h\\to0}\\frac{\\cos h-1}{h}+\\cos x\\lim_{h\\to0}\\frac{\\sin h}{h}.$$"
         "<p>看到了嗎?<strong>右邊出現了 $\\lim\\frac{\\sin h}{h}$ 本身</strong>。"
         "所以「用羅必達證 $\\lim\\frac{\\sin x}{x}=1$」等於「用結論證結論」。</p>"
         "<p class='step'><strong>正確的證法</strong>是幾何的:單位圓上比較三塊面積 "
         "(三角形 $\\le$ 扇形 $\\le$ 三角形),得 $\\cos x\\le\\dfrac{\\sin x}{x}\\le 1$,"
         "再用夾擠。這是銜接課教過的,今天要強調它<strong>不可被取代</strong>。</p>"
         "<p><strong>但可以拿羅必達當驗算</strong>。這裡要跟學生講清楚分寸:</p>"
         "<ul>"
         "<li>當<strong>驗算工具</strong>:完全可以。答案對得上,表示前面沒算錯。</li>"
         "<li>當<strong>證明</strong>:不行。邏輯上是循環的。</li>"
         "</ul>"
         "<p><strong>另一個常見誤解</strong>:羅必達失效 $\\ne$ 極限不存在。看</p>"
         "$$\\lim_{x\\to\\infty}\\frac{x+\\sin x}{x}.$$"
         "<p>用羅必達得 $\\dfrac{1+\\cos x}{1}$,這個極限不存在——但原極限明明是 $1$"
         "(拆成 $1+\\frac{\\sin x}{x}$ 就看出來了)。所以羅必達算不出來時,"
         "只能說「這招沒用」,<strong>不能</strong>說「極限不存在」。<span class='qed'>∎</span></p>",
    guide=["要對 $\\dfrac{\\sin x}{x}$ 用羅必達,你必須先知道 $(\\sin x)'=$ "
           "<span class=\"blank\"></span>。",
           "那條導數是怎麼證出來的?用定義展開 $\\sin(x+h)$ 之後,式子裡會出現哪個極限?",
           "所以「用羅必達證 $\\lim\\frac{\\sin x}{x}=1$」的邏輯問題是什麼?",
           "那銜接課用的是什麼方法?(提示:單位圓、三塊面積、夾擠)"],
    demo="Explain precisely why applying L'Hôpital's Rule to "
         "$\\displaystyle\\lim_{x\\to0}\\frac{\\sin x}{x}$ is circular reasoning.",
    demo_sol="<p>要用羅必達,必須先有 $(\\sin x)'=\\cos x$。而這條導數由定義推出時:</p>"
             "$$(\\sin x)'=\\lim_{h\\to0}\\frac{\\sin(x+h)-\\sin x}{h}"
             "=\\sin x\\cdot\\lim_{h\\to0}\\frac{\\cos h-1}{h}"
             "+\\cos x\\cdot\\lim_{h\\to0}\\frac{\\sin h}{h},$$"
             "<p>右側<strong>用到了 $\\displaystyle\\lim_{h\\to0}\\frac{\\sin h}{h}=1$ 本身</strong>。"
             "因此以羅必達「證明」這個極限,是拿結論當前提——循環論證。</p>"
             "<p>合法的證法是幾何夾擠:在單位圓上比較三角形、扇形、三角形的面積,得</p>"
             "$$\\cos x\\le\\frac{\\sin x}{x}\\le1\\quad\\left(0&lt;|x|&lt;\\frac{\\pi}{2}\\right),$$"
             "<p>兩側皆 $\\to1$,由夾擠定理得證。</p>"
             "<p><strong>可以</strong>用羅必達<em>驗算</em>,但不能當證明。</p>",
    demo_hint="問自己:用羅必達需要哪個已知?那個已知又是怎麼證出來的?",
    misstep="以為「羅必達算得出來 ⟹ 證明完成」。工具能算出答案,不代表推理是合法的。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\lim_{x\\to\\infty}\\frac{x+\\sin x}{x}$ with L'Hôpital, then "
         "with algebra. What does the comparison show?",
         "<p>羅必達給 $\\dfrac{1+\\cos x}{1}$,無極限;代數給 $1+\\dfrac{\\sin x}{x}\\to1$。"
         "說明<strong>羅必達失效不代表原極限不存在</strong>,只代表這招不適用。</p>"),
        ("Which of these may legitimately be evaluated by L'Hôpital? "
         "(i) $\\lim_{x\\to0}\\frac{\\sin x}{x}$ &nbsp; "
         "(ii) $\\lim_{x\\to0}\\frac{e^{x}-1}{x}$ &nbsp; "
         "(iii) $\\lim_{x\\to0}\\frac{\\tan x - x}{x^{3}}$",
         "<p>(ii)(iii) 可以。(i) 循環論證,不可當證明(當驗算可以)。"
         "注意 (iii) 雖含 $\\tan$,但它的導數不依賴 $\\lim\\frac{\\tan x}{x}$ 這個結論,"
         "而是由 $\\sin,\\cos$ 的導數與商法則得來,不構成循環。</p>"),
        ("State the geometric proof of $\\displaystyle\\lim_{x\\to0}\\frac{\\sin x}{x}=1$ in three "
         "sentences.",
         "<p>在單位圓上,對 $0&lt;x&lt;\\frac{\\pi}{2}$ 比較面積:"
         "$\\frac12\\sin x\\le\\frac12 x\\le\\frac12\\tan x$。"
         "同除 $\\frac12\\sin x$ 並取倒數得 $\\cos x\\le\\frac{\\sin x}{x}\\le1$。"
         "兩側極限皆為 $1$,由夾擠定理得證。</p>"),
    ])

C5 = Concept(
    title_en="Taylor Polynomials", title_zh="泰勒多項式",
    sub="Match the value, the slope, the curvature — and keep going",
    idea="The $n$-th Taylor polynomial of $f$ at $a$ is "
         "$$P_{n}(x)=\\sum_{k=0}^{n}\\frac{f^{(k)}(a)}{k!}(x-a)^{k},$$ "
         "the unique degree-$n$ polynomial whose first $n$ derivatives at $a$ agree with those of "
         "$f$. Linear approximation is exactly the case $n=1$.",
    deep="<p><strong>從學生已經會的東西長出來</strong>:銜接課教過線性近似 "
         "$L(x)=f(a)+f'(a)(x-a)$——那條切線<strong>對齊了函數值與斜率</strong>。"
         "泰勒多項式只是問:為什麼停在斜率?再對齊凹凸(二階)呢?再對齊三階呢?</p>"
         "<p class='step'><strong>係數怎麼來</strong>:假設 $P(x)=c_{0}+c_{1}(x-a)+c_{2}(x-a)^{2}+\\cdots$,"
         "要求 $P^{(k)}(a)=f^{(k)}(a)$。逐次微分再代 $x=a$:</p>"
         "$$P(a)=c_{0},\\quad P'(a)=c_{1},\\quad P''(a)=2c_{2},\\quad P'''(a)=6c_{3},\\ \\dots$$"
         "<p>一般地 $P^{(k)}(a)=k!\\,c_{k}$,所以 $c_{k}=\\dfrac{f^{(k)}(a)}{k!}$。"
         "<strong>那個 $k!$ 不是憑空冒出來的,是微分 $k$ 次掉下來的</strong>——"
         "這句話能省下學生一半的困惑。</p>"
         "<p><strong>本週只談多項式,不談級數</strong>。$n$ 是有限的,沒有收斂問題。"
         "「$n\\to\\infty$ 會怎樣」留給微積分(二)——那時才需要處理收斂半徑。</p>"
         "<p>接下來三個觀念都圍著一個問題:<strong>用 $P_{n}$ 代替 $f$,誤差有多大?</strong>"
         "<span class='qed'>∎</span></p>",
    guide=["線性近似 $L(x)=f(a)+f'(a)(x-a)$ 對齊了 $f$ 的哪兩樣東西?",
           "如果還想對齊二階導數,要加上什麼項?係數該是多少?"
           "(把 $c_{2}(x-a)^{2}$ 微分兩次看看)",
           "微分 $k$ 次之後,$c_{k}(x-a)^{k}$ 會變成 <span class=\"blank\"></span>,"
           "所以 $c_{k}=$ <span class=\"blank\"></span>。",
           "$P_{1}$ 就是切線。那 $P_{0}$ 是什麼?(只對齊函數值的多項式)"],
    demo="Find the third-order Taylor polynomial $P_{3}$ of $f(x)=e^{x}$ at $a=0$, and of "
         "$g(x)=\\sin x$ at $a=0$.",
    demo_sol="<p><strong>$e^{x}$</strong>:所有階導數都是 $e^{x}$,在 $0$ 都等於 $1$。故</p>"
             "$$P_{3}(x)=1+x+\\frac{x^{2}}{2}+\\frac{x^{3}}{6}.$$"
             "<p><strong>$\\sin x$</strong>:導數循環為 $\\cos,-\\sin,-\\cos,\\sin$,"
             "在 $0$ 的值是 $1,0,-1,0$。故</p>"
             "$$P_{3}(x)=x-\\frac{x^{3}}{6}.$$"
             "<p>注意 $\\sin$ 是奇函數,展開式<strong>只有奇次項</strong>——"
             "偶階導數在 $0$ 全為零。這種對稱性可以省一半計算。</p>",
    demo_hint="先把 $f,f',f'',f'''$ 在 $a=0$ 的值列成一張表,再套公式。",
    misstep="漏掉分母的 $k!$。$P_{3}$ 的三次項是 $\\dfrac{f'''(0)}{6}x^{3}$,不是 $f'''(0)x^{3}$。",
    level="mid",
    drills=[
        ("Find $P_{2}$ of $f(x)=\\sqrt{x}$ at $a=4$.",
         "<p>$f(4)=2$、$f'(x)=\\dfrac{1}{2\\sqrt x}\\Rightarrow f'(4)=\\dfrac14$、"
         "$f''(x)=-\\dfrac{1}{4x^{3/2}}\\Rightarrow f''(4)=-\\dfrac{1}{32}$。故"
         "$P_{2}(x)=2+\\dfrac14(x-4)-\\dfrac{1}{64}(x-4)^{2}$。</p>"),
        ("Find $P_{4}$ of $f(x)=\\ln(1+x)$ at $a=0$.",
         "<p>導數在 $0$ 依次為 $0,1,-1,2,-6$,除以 $k!$ 得 "
         "$P_{4}(x)=x-\\dfrac{x^{2}}{2}+\\dfrac{x^{3}}{3}-\\dfrac{x^{4}}{4}$。</p>"),
        ("Find $P_{4}$ of $f(x)=\\cos x$ at $a=0$ and explain why only even powers appear.",
         "<p>$P_{4}(x)=1-\\dfrac{x^{2}}{2}+\\dfrac{x^{4}}{24}$。$\\cos$ 是偶函數,"
         "奇階導數在 $0$ 全為零,故只剩偶次項。</p>"),
    ])

C6 = Concept(
    title_en="Taylor Polynomials You Should Know", title_zh="必須記住的幾個展開",
    sub="Four expansions cover most of what you will ever need",
    idea="$$e^{x}=1+x+\\frac{x^{2}}{2!}+\\cdots,\\quad "
         "\\sin x=x-\\frac{x^{3}}{3!}+\\frac{x^{5}}{5!}-\\cdots,\\quad "
         "\\cos x=1-\\frac{x^{2}}{2!}+\\frac{x^{4}}{4!}-\\cdots,\\quad "
         "\\ln(1+x)=x-\\frac{x^{2}}{2}+\\frac{x^{3}}{3}-\\cdots$$ "
         "Substituting into these beats differentiating from scratch.",
    deep="<p>這四條要熟到反射,因為<strong>代換法</strong>幾乎能解決所有其他展開。</p>"
         "<p class='step'><strong>代換的威力</strong>:要 $e^{-x^{2}}$ 的展開?"
         "不必微分七次——直接把 $e^{u}$ 的展開裡的 $u$ 換成 $-x^{2}$:</p>"
         "$$e^{-x^{2}}=1-x^{2}+\\frac{x^{4}}{2}-\\frac{x^{6}}{6}+\\cdots$$"
         "<p>手算微分七次要十分鐘且容易錯,代換三十秒。這個技巧在微積分(二)的級數會天天用。</p>"
         "<p class='step'><strong>Euler 公式的預告</strong>:把 $e^{x}$ 展開的 $x$ 換成 $ix$,"
         "實部湊出 $\\cos x$、虛部湊出 $\\sin x$——這就是 $e^{ix}=\\cos x+i\\sin x$ 的來源。"
         "本課不深入,但值得寫在黑板上讓他們驚訝三十秒。</p>"
         "<p><strong>接到 CS</strong>:$\\ln(1+x)\\approx x$ 在 $x$ 很小時,"
         "是計算機科學裡處理小機率對數(log-probability)的標準手法;"
         "而 $e^{x}\\approx1+x$ 是複利與學習率衰減公式的根據。<span class='qed'>∎</span></p>",
    guide=["把 $e^{u}=1+u+\\dfrac{u^{2}}{2}+\\cdots$ 裡的 $u$ 換成 $-x^{2}$,前三項會變成什麼?",
           "這樣做比直接對 $e^{-x^{2}}$ 微分四次快多少?",
           "$\\sin x$ 的展開只有 <span class=\"blank\"></span> 次項,$\\cos x$ 只有 "
           "<span class=\"blank\"></span> 次項。為什麼?",
           "把 $e^{x}$ 展開裡的 $x$ 換成 $ix$,實部和虛部分別像什麼?"],
    demo="Find the Taylor polynomial of $f(x)=e^{-x^{2}}$ at $a=0$ up to $x^{4}$ by substitution.",
    demo_sol="<p>從 $e^{u}=1+u+\\dfrac{u^{2}}{2}+\\dfrac{u^{3}}{6}+\\cdots$ 出發,令 $u=-x^{2}$:</p>"
             "$$e^{-x^{2}}=1+(-x^{2})+\\frac{(-x^{2})^{2}}{2}+\\cdots"
             "=1-x^{2}+\\frac{x^{4}}{2}-\\cdots$$"
             "<p>取到 $x^{4}$:$P_{4}(x)=1-x^{2}+\\dfrac{x^{4}}{2}$。</p>"
             "<p>若硬幹,要算 $f^{(4)}(0)$——四次乘積法則,大約十分鐘且容易錯。代換三十秒。</p>",
    demo_hint="別微分。把已知展開裡的變數換掉就好。",
    misstep="代換後忘了處理次方:$(-x^{2})^{2}=+x^{4}$ 不是 $-x^{4}$。",
    level="mid",
    drills=[
        ("Find the expansion of $\\sin(x^{2})$ up to $x^{6}$.",
         "<p>$\\sin u=u-\\dfrac{u^{3}}{6}+\\cdots$,令 $u=x^{2}$:"
         "$\\sin(x^{2})=x^{2}-\\dfrac{x^{6}}{6}+\\cdots$</p>"),
        ("Find the expansion of $\\dfrac{1}{1-x}$ up to $x^{3}$ at $a=0$.",
         "<p>$f^{(k)}(0)=k!$,故係數全為 $1$:$1+x+x^{2}+x^{3}+\\cdots$"
         "(就是等比級數)。</p>"),
        ("Use $\\ln(1+x)\\approx x-\\dfrac{x^{2}}{2}$ to estimate $\\ln(1.1)$, and compare with "
         "the true value $0.0953102\\ldots$",
         "<p>$0.1-\\dfrac{0.01}{2}=0.095$,誤差約 $3.1\\times10^{-4}$。"
         "再加一項 $\\dfrac{x^{3}}{3}$ 得 $0.0953\\overline{3}$,誤差降到 $2\\times10^{-5}$。</p>"),
    ])

C7 = Concept(
    title_en="Taylor's Theorem with Remainder", title_zh="泰勒定理與餘項",
    sub="The error has an exact form — and it looks like the next term",
    idea="Taylor's theorem with the Lagrange remainder: "
         "$$f(x)=P_{n}(x)+\\frac{f^{(n+1)}(\\xi)}{(n+1)!}(x-a)^{n+1}$$ "
         "for some $\\xi$ between $a$ and $x$. The error term is exactly the shape of the next "
         "Taylor term, with the derivative evaluated at an unknown intermediate point.",
    deep="<p>這條定理讓泰勒多項式從「看起來很準」變成「<strong>可以保證多準</strong>」——"
         "這是工程上能不能用的分水嶺。</p>"
         "<p class='step'><strong>形式很好記</strong>:餘項 $R_{n}(x)=\\dfrac{f^{(n+1)}(\\xi)}{(n+1)!}"
         "(x-a)^{n+1}$,長得<strong>就像下一項</strong>,只是導數不是在 $a$ 取值,"
         "而是在某個未知的 $\\xi$ 取值。</p>"
         "<p class='step'><strong>$n=0$ 就是 MVT</strong>:$f(x)=f(a)+f'(\\xi)(x-a)$。"
         "所以泰勒定理是 MVT 的高階推廣——本週三個定理串成一條線:"
         "Rolle → MVT → Cauchy MVT → L'Hôpital,以及 Rolle → MVT → Taylor。"
         "同一個祖先。</p>"
         "<p><strong>怎麼用</strong>:$\\xi$ 不知道是多少,但只要能給 $|f^{(n+1)}|$ 在區間上一個"
         "<strong>上界</strong> $M$,就有</p>"
         "$$|R_{n}(x)|\\le\\frac{M}{(n+1)!}|x-a|^{n+1}.$$"
         "<p>對 $\\sin,\\cos$ 特別好用:所有階導數的絕對值都 $\\le1$,直接取 $M=1$。"
         "所以 $|R_{n}(x)|\\le\\dfrac{|x|^{n+1}}{(n+1)!}$——分母的階乘長得飛快,"
         "這就是為什麼幾項就夠準。</p>"
         "<p><strong>不必背證明</strong>(它是對輔助函數用 Rolle,和前面同一招),"
         "但要會<strong>用</strong>那個上界。考卷考的是後者。<span class='qed'>∎</span></p>",
    guide=["餘項的形狀和「下一項」$\\dfrac{f^{(n+1)}(a)}{(n+1)!}(x-a)^{n+1}$ 差在哪裡?",
           "取 $n=0$ 時,泰勒定理會變成哪一條你已經很熟的定理?",
           "$\\xi$ 我們不知道。那怎麼還能估誤差?(提示:找 $|f^{(n+1)}|$ 的 "
           "<span class=\"blank\"></span>)",
           "對 $f=\\sin$,所有階導數的絕對值最大是 <span class=\"blank\"></span>,"
           "所以 $M$ 可以取多少?"],
    demo="Use the Lagrange remainder to bound the error when $\\sin(0.5)$ is approximated by "
         "$P_{5}(x)=x-\\dfrac{x^{3}}{6}+\\dfrac{x^{5}}{120}$.",
    demo_sol="<p>$n=5$,餘項為 $R_{5}(x)=\\dfrac{f^{(6)}(\\xi)}{6!}x^{6}$。但 $\\sin$ 的展開沒有 "
             "$x^{6}$ 項($f^{(6)}(0)=0$),所以 $P_{5}=P_{6}$,可以改用 $n=6$ 的餘項估得更緊:</p>"
             "$$|R_{6}(0.5)|=\\left|\\frac{f^{(7)}(\\xi)}{7!}(0.5)^{7}\\right|"
             "\\le\\frac{1\\cdot(0.5)^{7}}{5040}\\approx1.55\\times10^{-6}.$$"
             "<p>因為 $\\left|f^{(7)}\\right|=|-\\cos\\xi|\\le1$。</p>"
             "<p><strong>實際驗證</strong>:$P_{5}(0.5)=0.4794270833\\ldots$、"
             "$\\sin(0.5)=0.4794255386\\ldots$,真實誤差 $\\approx1.54\\times10^{-6}$。"
             "誤差界 $1.55\\times10^{-6}$ 不但正確,而且<strong>非常緊</strong>。</p>",
    demo_hint="先找 $|f^{(n+1)}|$ 的上界。$\\sin$ 的各階導數都是 $\\pm\\sin$ 或 $\\pm\\cos$,"
              "絕對值都不超過 1。",
    misstep="把 $\\xi$ 當成 $a$ 代進去算。$\\xi$ 是未知的,只能用<strong>上界</strong>估計。",
    level="hard",
    drills=[
        ("Bound the error when $e^{0.1}$ is approximated by $P_{2}(x)=1+x+\\dfrac{x^{2}}{2}$.",
         "<p>$|R_{2}|=\\left|\\dfrac{e^{\\xi}}{6}(0.1)^{3}\\right|$,$\\xi\\in(0,0.1)$ 故 "
         "$e^{\\xi}&lt;e^{0.1}&lt;1.11$,得 $|R_{2}|&lt;\\dfrac{1.11\\times10^{-3}}{6}"
         "\\approx1.85\\times10^{-4}$。</p>"),
        ("How many terms of the expansion of $\\sin x$ are needed to compute $\\sin(1)$ with error "
         "below $10^{-6}$?",
         "<p>需 $\\dfrac{1}{(n+1)!}&lt;10^{-6}$,即 $(n+1)!&gt;10^{6}$。$9!=362880$、"
         "$10!=3628800$,故 $n+1=10$,即取到 $x^{9}$ 項(五個非零項)。</p>"),
        ("Explain why the remainder bound for $\\sin$ and $\\cos$ is always $\\dfrac{|x-a|^{n+1}}"
         "{(n+1)!}$.",
         "<p>因為它們的各階導數都是 $\\pm\\sin$ 或 $\\pm\\cos$,絕對值恆 $\\le1$,"
         "故可取 $M=1$。這是三角函數的展開特別好估的原因。</p>"),
    ])

C8 = Concept(
    title_en="Choosing the Degree in Practice", title_zh="實務上該取幾階",
    sub="Pick n so the bound clears your tolerance — then stop",
    idea="Given a required accuracy $\\tau$, choose the smallest $n$ with "
         "$\\dfrac{M\\,|x-a|^{n+1}}{(n+1)!}&lt;\\tau$. Because $(n+1)!$ grows faster than any "
         "power, a handful of terms usually suffices — provided $|x-a|$ is small.",
    deep="<p>這是<strong>工程視角</strong>的一段:不是「展開越多越好」,而是「夠用就停」。</p>"
         "<p class='step'><strong>兩個因素在拔河</strong>:分子 $|x-a|^{n+1}$ 隨 $n$ 變大而"
         "<em>可能</em>變大(若 $|x-a|&gt;1$),分母 $(n+1)!$ 一定變大而且快得多。"
         "階乘最後一定贏,但如果 $|x-a|$ 很大,要等很久才贏。</p>"
         "<p class='step'><strong>所以真正的訣竅是把 $|x-a|$ 弄小</strong>。"
         "算 $\\sin(1000)$ 不要在 $a=0$ 展開一千項——先用週期性把角度縮到 "
         "$[-\\pi,\\pi]$,甚至縮到 $[-\\frac{\\pi}{4},\\frac{\\pi}{4}]$,再展開幾項就好。"
         "這正是下一個觀念(函式庫怎麼做)的核心。</p>"
         "<p><strong>一張值得抄的表</strong>($\\sin$ 在 $a=0$,誤差界 "
         "$\\frac{|x|^{n+1}}{(n+1)!}$):</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>$|x|$</th><th>取到 $x^{3}$</th>"
         "<th>取到 $x^{5}$</th><th>取到 $x^{7}$</th></tr></thead><tbody>"
         "<tr><td>$0.1$</td><td>$4\\times10^{-6}$</td><td>$8\\times10^{-10}$</td>"
         "<td>$3\\times10^{-14}$</td></tr>"
         "<tr><td>$0.5$</td><td>$2.6\\times10^{-3}$</td><td>$1.6\\times10^{-5}$</td>"
         "<td>$4\\times10^{-8}$</td></tr>"
         "<tr><td>$1.0$</td><td>$4.2\\times10^{-2}$</td><td>$2.0\\times10^{-3}$</td>"
         "<td>$2.5\\times10^{-5}$</td></tr>"
         "</tbody></table></div>"
         "<p>看最後一欄:同樣取到七次,$|x|$ 從 $1$ 縮到 $0.1$,精度差了九個數量級。"
         "<strong>縮小區間比增加項數划算太多</strong>。<span class='qed'>∎</span></p>",
    guide=["誤差界是 $\\dfrac{M|x-a|^{n+1}}{(n+1)!}$。要它變小,你可以動哪兩個東西?",
           "$n$ 加一,分母乘上 <span class=\"blank\"></span>;$|x-a|$ 減半,分子乘上 "
           "<span class=\"blank\"></span>。哪一個效果快?",
           "如果 $|x-a|=10$,取 $n=5$ 的誤差界是 $\\dfrac{10^{6}}{720}\\approx1389$——"
           "這個近似有意義嗎?",
           "所以要算 $\\sin(1000)$,聰明的第一步是什麼?"],
    demo="Determine the smallest $n$ such that $P_{n}$ approximates $\\cos(0.3)$ at $a=0$ with "
         "error below $10^{-8}$.",
    demo_sol="<p>$\\cos$ 的各階導數絕對值 $\\le1$,取 $M=1$,誤差界為 "
             "$\\dfrac{(0.3)^{n+1}}{(n+1)!}$。逐一計算:</p>"
             "<p class='step'>$n=3$:$\\dfrac{0.3^{4}}{24}=3.4\\times10^{-4}$ — 不夠</p>"
             "<p class='step'>$n=5$:$\\dfrac{0.3^{6}}{720}=1.0\\times10^{-6}$ — 不夠</p>"
             "<p class='step'>$n=7$:$\\dfrac{0.3^{8}}{40320}=1.6\\times10^{-9}$ — <strong>達標</strong></p>"
             "<p>故取 $n=7$,即 $P_{7}(x)=1-\\dfrac{x^{2}}{2}+\\dfrac{x^{4}}{24}"
             "-\\dfrac{x^{6}}{720}$(七次項係數為零)。實際上只需四個非零項。</p>",
    demo_hint="把誤差界寫出來,從小的 $n$ 開始試,看哪個先低於 $10^{-8}$。",
    misstep="只看 $n$ 不看 $|x-a|$。$|x-a|$ 大的時候,增加項數的效果差得驚人。",
    level="hard",
    drills=[
        ("What is the error bound for $P_{3}$ of $\\sin x$ at $x=1$?",
         "<p>$\\dfrac{|1|^{4}}{4!}=\\dfrac{1}{24}\\approx4.2\\times10^{-2}$。"
         "(實際誤差約 $1.99\\times10^{-3}$,界是安全但寬鬆的。)</p>"),
        ("To compute $e^{5}$ from the expansion at $a=0$, roughly how many terms are needed for "
         "error below $10^{-6}$? What does this suggest?",
         "<p>需 $\\dfrac{e^{5}\\cdot5^{n+1}}{(n+1)!}&lt;10^{-6}$,約需 $n\\approx25$ 項。"
         "這說明<strong>離展開點太遠就該換做法</strong>——例如先用 "
         "$e^{5}=\\left(e^{0.5}\\right)^{10}$ 把指數縮小。</p>"),
        ("Between doubling $n$ and halving $|x-a|$, which usually reduces the error bound more? "
         "Why?",
         "<p>通常是<strong>減半 $|x-a|$</strong>:它讓分子乘上 $2^{-(n+1)}$,"
         "是指數級的改善;而增加 $n$ 雖然分母是階乘,但每加一項只多乘一個因子。"
         "實務上兩者併用,先縮區間再取幾項。</p>"),
    ])

C9 = Concept(
    title_en="How Libraries Compute sin", title_zh="函式庫怎麼算 sin",
    sub="Range reduction first, then a short polynomial — exactly what you just learned",
    idea="A real <code>sin()</code> implementation does two things: reduce the argument into a "
         "small interval using periodicity and symmetry, then evaluate a short minimax polynomial. "
         "Taylor is the idea; the production version just picks slightly better coefficients.",
    deep="<p>這是本週<strong>接回 CS</strong> 的一段。學生每天呼叫 <code>math.sin()</code>,"
         "從沒想過裡面是什麼。</p>"
         "<p class='step'><strong>第一步:區間縮減(range reduction)</strong>。"
         "利用 $\\sin(x+2k\\pi)=\\sin x$ 與各種對稱性,把任意 $x$ 縮到 "
         "$\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$。"
         "由觀念 8 的表可知,在這麼小的區間上,取到 $x^{7}$ 誤差就低於 $10^{-8}$。</p>"
         "<p class='step'><strong>第二步:多項式求值</strong>。用 Horner 法把"
         "$x-\\frac{x^{3}}{6}+\\frac{x^{5}}{120}-\\frac{x^{7}}{5040}$ 寫成</p>"
         "$$x\\left(1+x^{2}\\left(-\\tfrac16+x^{2}\\left(\\tfrac{1}{120}"
         "-\\tfrac{x^{2}}{5040}\\right)\\right)\\right),$$"
         "<p>只要 3 次乘法而不是 10 幾次冪運算。這是效能的關鍵。</p>"
         "<p><strong>和真實實作的差別</strong>:業界用的不是泰勒係數,而是 "
         "<strong>minimax 多項式</strong>——泰勒在展開點 $a$ 最準、越遠越差;"
         "minimax 則讓<em>整個區間</em>的最大誤差最小,同樣次數下更準。"
         "但概念完全一樣:<strong>用短多項式代替超越函數</strong>。</p>"
         "<p>順帶一提:區間縮減本身是個大坑。$x$ 很大時,$x-2k\\pi$ 會遇到"
         "災難性消去(W1 觀念 10!),所以真實實作要用高精度的 $\\pi$ 值。"
         "這兩週的東西在這裡合體了。<span class='qed'>∎</span></p>",
    guide=["要算 $\\sin(1000)$,直接在 $a=0$ 展開要幾項?(想觀念 8 的誤差界)",
           "利用週期性,$1000$ 可以先減掉多少個 $2\\pi$?縮到哪個區間最好?",
           "在 $\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$ 上取到 $x^{7}$,誤差界大約多少?",
           "$x$ 很大時,$x-2k\\pi$ 這個減法會遇到 W1 講過的什麼問題?"],
    demo="Explain the two stages a real <code>sin()</code> implementation uses, and estimate the "
         "error of a degree-7 Taylor polynomial on "
         "$\\left[-\\dfrac{\\pi}{4},\\dfrac{\\pi}{4}\\right]$.",
    demo_sol="<p><strong>階段一:區間縮減</strong>。用 $\\sin(x+2k\\pi)=\\sin x$ 及對稱性,"
             "把 $x$ 縮進 $\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$。</p>"
             "<p><strong>階段二:短多項式</strong>。在該區間求值(實作用 Horner 法)。</p>"
             "<p><strong>誤差估計</strong>:$|x|\\le\\dfrac{\\pi}{4}\\approx0.7854$,"
             "取到 $x^{7}$ 用 $n=8$ 的餘項界:</p>"
             "$$|R_{8}|\\le\\frac{(\\pi/4)^{9}}{9!}\\approx\\frac{0.1157}{362880}"
             "\\approx3.2\\times10^{-7}.$$"
             "<p>已接近單精度浮點的極限。雙精度實作會再多取兩項,或改用 minimax 係數。</p>",
    demo_hint="先縮區間、再展開。誤差界用 $\\dfrac{|x|^{n+1}}{(n+1)!}$,$M=1$。",
    misstep="以為函式庫是用查表或無窮級數硬算。實際上是<strong>縮區間 + 短多項式</strong>,"
            "兩者缺一不可。",
    level="mid",
    drills=[
        ("Write $x-\\dfrac{x^{3}}{6}+\\dfrac{x^{5}}{120}$ in Horner form and count the "
         "multiplications.",
         "<p>$x\\left(1+x^{2}\\left(-\\dfrac16+\\dfrac{x^{2}}{120}\\right)\\right)$。"
         "算一次 $x^{2}$、兩次乘加、最後乘 $x$,約 4 次乘法;直接算冪次要 7 次以上。</p>"),
        ("Why must range reduction use a high-precision value of $\\pi$?",
         "<p>$x$ 很大時 $x-2k\\pi$ 是兩個相近大數相減 → 災難性消去(W1 觀念 10)。"
         "$\\pi$ 的精度不足會讓縮減後的角度失去有效位數。</p>"),
        ("What is the advantage of a minimax polynomial over the Taylor polynomial of the same "
         "degree?",
         "<p>泰勒在展開點附近最準、遠處變差;minimax 讓<strong>整個區間</strong>的最大誤差最小,"
         "因此同次數下最壞情況更好——函式庫在意的正是最壞情況。</p>"),
    ])

C10 = Concept(
    title_en="Taylor Explains Numerical Differentiation", title_zh="用泰勒解釋數值微分",
    sub="Now you can prove what W1 only observed: why h ≈ 1e-8 is optimal",
    idea="Expanding $f(x+h)$ shows the forward difference has truncation error "
         "$\\dfrac{h}{2}f''(\\xi)=O(h)$, while the central difference has $O(h^{2})$. Combined "
         "with round-off $O(\\varepsilon_{\\text{mach}}/h)$, the optimal step follows.",
    deep="<p>W1 只是<strong>觀察</strong>到那條 V 字形誤差曲線。今天可以<strong>證明</strong>它。</p>"
         "<p class='step'><strong>前向差分</strong>。由泰勒定理,</p>"
         "$$f(x+h)=f(x)+hf'(x)+\\frac{h^{2}}{2}f''(\\xi).$$"
         "<p>移項同除 $h$:</p>"
         "$$\\frac{f(x+h)-f(x)}{h}=f'(x)+\\frac{h}{2}f''(\\xi).$$"
         "<p>所以截斷誤差是 $O(h)$——<strong>一階</strong>。</p>"
         "<p class='step'><strong>中央差分</strong>。分別展開 $f(x\\pm h)$ 到三階再相減,"
         "偶次項全部抵消:</p>"
         "$$\\frac{f(x+h)-f(x-h)}{2h}=f'(x)+\\frac{h^{2}}{6}f'''(\\xi).$$"
         "<p>截斷誤差 $O(h^{2})$——<strong>二階</strong>,同樣的 $h$ 準得多。"
         "這解釋了 W1 Lab 用中央差分的原因。</p>"
         "<p class='step'><strong>加上捨入誤差</strong>。分子的浮點誤差約 "
         "$\\varepsilon_{\\text{mach}}|f|$,除以 $h$ 後放大成 "
         "$\\dfrac{\\varepsilon_{\\text{mach}}}{h}$。總誤差</p>"
         "$$E(h)\\approx\\frac{h}{2}|f''|+\\frac{\\varepsilon_{\\text{mach}}}{h}.$$"
         "<p>對 $h$ 微分令為零(這是最佳化,W4 學過):"
         "$h^{*}=\\sqrt{\\dfrac{2\\varepsilon_{\\text{mach}}}{|f''|}}\\approx\\sqrt{\\varepsilon_{\\text{mach}}}"
         "\\approx1.5\\times10^{-8}$。</p>"
         "<p><strong>W1 的經驗法則,現在有了證明</strong>。同理中央差分的最佳步長是 "
         "$\\varepsilon_{\\text{mach}}^{1/3}\\approx6\\times10^{-6}$——實作課會驗證這個預測。"
         "<span class='qed'>∎</span></p>",
    guide=["把 $f(x+h)$ 展開到二階(含餘項),再移項同除 $h$,會得到 "
           "$\\dfrac{f(x+h)-f(x)}{h}=f'(x)+$ <span class=\"blank\"></span>。",
           "所以前向差分的截斷誤差是 $O($ <span class=\"blank\"></span> $)$。",
           "現在把 $f(x+h)$ 和 $f(x-h)$ 都展開到三階再相減。哪些項會抵消?",
           "總誤差 $\\dfrac{h}{2}|f''|+\\dfrac{\\varepsilon}{h}$ 對 $h$ 微分令零,解出 $h^{*}=$ "
           "<span class=\"blank\"></span>。"],
    demo="Use Taylor's theorem to show the central difference has truncation error $O(h^{2})$, "
         "and derive the optimal step size for the forward difference.",
    demo_sol="<p><strong>中央差分</strong>。展開兩式:</p>"
             "$$f(x+h)=f+hf'+\\frac{h^{2}}{2}f''+\\frac{h^{3}}{6}f''',\\qquad "
             "f(x-h)=f-hf'+\\frac{h^{2}}{2}f''-\\frac{h^{3}}{6}f'''.$$"
             "<p>相減時 $f$ 與 $f''$ 的項<strong>成對抵消</strong>:</p>"
             "$$f(x+h)-f(x-h)=2hf'+\\frac{h^{3}}{3}f''' \\Longrightarrow "
             "\\frac{f(x+h)-f(x-h)}{2h}=f'+\\frac{h^{2}}{6}f'''.$$"
             "<p>故截斷誤差為 $O(h^{2})$。</p>"
             "<p><strong>最佳步長(前向)</strong>。總誤差 "
             "$E(h)=\\dfrac{h}{2}|f''|+\\dfrac{\\varepsilon}{h}$,令 $E'(h)=0$:</p>"
             "$$\\frac{|f''|}{2}-\\frac{\\varepsilon}{h^{2}}=0\\ \\Longrightarrow\\ "
             "h^{*}=\\sqrt{\\frac{2\\varepsilon}{|f''|}}\\approx\\sqrt{\\varepsilon}"
             "\\approx1.5\\times10^{-8}.$$"
             "<p>與 W1 實測的最佳 $h$ 完全吻合。</p>",
    demo_hint="兩式相減時,注意哪些項是偶次(同號,抵消)、哪些是奇次(異號,加倍)。",
    misstep="以為中央差分「比較準」只是經驗。它有明確的階數保證:$O(h^{2})$ vs $O(h)$。",
    level="hard",
    drills=[
        ("Show that the forward difference has truncation error exactly "
         "$\\dfrac{h}{2}f''(\\xi)$.",
         "<p>由泰勒定理 $f(x+h)=f(x)+hf'(x)+\\dfrac{h^{2}}{2}f''(\\xi)$,"
         "移項同除 $h$ 即得 $\\dfrac{f(x+h)-f(x)}{h}-f'(x)=\\dfrac{h}{2}f''(\\xi)$。</p>"),
        ("For the central difference, total error is $\\dfrac{h^{2}}{6}|f'''|+"
         "\\dfrac{\\varepsilon}{h}$. Find the optimal $h$.",
         "<p>微分令零:$\\dfrac{h}{3}|f'''|=\\dfrac{\\varepsilon}{h^{2}}$,"
         "故 $h^{*}=\\left(\\dfrac{3\\varepsilon}{|f'''|}\\right)^{1/3}"
         "\\approx\\varepsilon^{1/3}\\approx6\\times10^{-6}$。</p>"),
        ("Why does the central difference cancel the $f''$ term while the forward difference does "
         "not?",
         "<p>中央差分把 $f(x-h)$ 減掉,$h$ 的奇次項變號、偶次項不變號,"
         "相減後偶次項(含 $f''$ 的 $h^{2}$ 項)成對消掉。前向差分沒有這個對稱結構。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜泰勒多項式:一階一階逼近上去",
    intro="把 $P_1,P_3,P_5,P_7,P_9$ 疊在 $\\sin x$ 上,親眼看它們怎麼一段一段「咬」住原函數。",
    code="""x = sp.Symbol('x')

def taylor_poly(f, n, a=0):
    \"\"\"回傳 f 在 a 的 n 階泰勒多項式(sympy 運算式)\"\"\"
    return sum(sp.diff(f, x, k).subs(x, a) / sp.factorial(k) * (x - a)**k
               for k in range(n + 1))

xs = np.linspace(-8, 8, 600)
plt.plot(xs, np.sin(xs), 'k', lw=2.5, label='sin x')
for n in [1, 3, 5, 7, 9]:
    P = taylor_poly(sp.sin(x), n)
    fn = sp.lambdify(x, P, 'numpy')
    plt.plot(xs, fn(xs), lw=1.2, label=f'P{n}')
    print(f"P{n} =", sp.expand(P))
plt.ylim(-2, 2); plt.legend(ncol=3, fontsize=8)
plt.title('Taylor polynomials of sin x at a = 0')
plt.show()""",
    expected="P1 = x\nP3 = -x**3/6 + x\nP5 = x**5/120 - x**3/6 + x",
    seealso="每加兩階,吻合的範圍就往外擴一段。$P_9$ 在 $[-5,5]$ 幾乎與 $\\sin x$ 重疊,"
            "但一出這個範圍就迅速發散——泰勒多項式是<strong>局部</strong>的。",
    todo="""# TODO 學生練習:把 sp.sin(x) 換成 sp.exp(x),範圍改 np.linspace(-3, 3, 400)
# exp 的泰勒多項式和 sin 的行為有什麼不同?(提示:看有沒有正負震盪)""")

LAB2 = Lab(
    title="Lab 2｜餘項界是真的嗎",
    intro="觀念 7 說誤差不超過 $\\dfrac{|x|^{n+1}}{(n+1)!}$。這格把「界」和「實際誤差」畫在一起,"
          "檢查界有沒有被突破、又有多緊。",
    code="""from math import factorial

def taylor_sin(x0, n):
    \"\"\"sin 在 0 的 n 階泰勒多項式,直接用級數係數\"\"\"
    return sum((-1)**k * x0**(2*k+1) / factorial(2*k+1)
               for k in range((n + 1) // 2))

print(f"{'x':>6} {'n':>3} {'P_n(x)':>14} {'sin(x)':>14} {'實際誤差':>12} {'餘項界':>12} {'界成立?':>8}")
for x0 in [0.5, 1.0, 2.0]:
    for n in [3, 5, 7]:
        approx = taylor_sin(x0, n)
        exact  = math.sin(x0)
        err    = abs(approx - exact)
        bound  = abs(x0)**(n+1) / factorial(n+1)
        print(f"{x0:6.1f} {n:3d} {approx:14.10f} {exact:14.10f} "
              f"{err:12.3e} {bound:12.3e} {'OK' if err <= bound else '突破!':>8}")

# 界 vs 實際誤差
ns = np.arange(1, 16, 2)
x0 = 1.0
errs   = [abs(taylor_sin(x0, n) - math.sin(x0)) for n in ns]
bounds = [x0**(n+1) / factorial(n+1) for n in ns]
plt.semilogy(ns, errs, 'o-', label='actual error')
plt.semilogy(ns, bounds, 's--', label='Lagrange bound')
plt.xlabel('n'); plt.ylabel('error at x = 1'); plt.legend()
plt.title('The bound is always above the error — and close')
plt.show()""",
    expected="   0.5   5   0.4794270833   0.4794255386    1.545e-06    1.550e-06       OK",
    seealso="每一列的界都<strong>大於等於</strong>實際誤差,定理沒被打破;"
            "而且 $x=0.5,n=5$ 那列界是 $1.550\\times10^{-6}$、實際 $1.545\\times10^{-6}$,"
            "只差 $0.3\\%$——這個界緊到幾乎沒有浪費。",
    todo="""# TODO 學生練習:把 sin 換成 cos(係數改 (-1)^k * x^(2k) / (2k)!)
# 對 x = 1,要取到幾階誤差才低於 1e-10?""")

LAB3 = Lab(
    title="Lab 3｜自己寫一個 sin:區間縮減 + Horner",
    intro="觀念 9 說函式庫用「縮區間 + 短多項式」。這格真的把它寫出來,和 <code>math.sin</code> 比。",
    code="""TWO_PI = 2 * math.pi

def my_sin(x0):
    \"\"\"階段一:區間縮減;階段二:7 次多項式(Horner)\"\"\"
    # --- 縮到 [-pi, pi] ---
    x0 = x0 - TWO_PI * round(x0 / TWO_PI)
    # --- 再用對稱性縮到 [-pi/2, pi/2] ---
    if x0 > math.pi / 2:
        x0 = math.pi - x0
    elif x0 < -math.pi / 2:
        x0 = -math.pi - x0
    # --- Horner 形式的 7 次泰勒 ---
    x2 = x0 * x0
    return x0 * (1 + x2 * (-1/6 + x2 * (1/120 - x2 / 5040)))

print(f"{'x':>10} {'my_sin':>18} {'math.sin':>18} {'誤差':>12}")
for x0 in [0.1, 0.5, 1.0, 3.0, 10.0, 1000.0]:
    m, t = my_sin(x0), math.sin(x0)
    print(f"{x0:10.1f} {m:18.12f} {t:18.12f} {abs(m-t):12.3e}")

xs = np.linspace(-20, 20, 800)
err = [abs(my_sin(v) - math.sin(v)) for v in xs]
plt.semilogy(xs, np.maximum(err, 1e-18))
plt.xlabel('x'); plt.ylabel('|my_sin - math.sin|')
plt.title('Range reduction keeps the error flat everywhere')
plt.show()
print("\\n最大誤差 =", max(err))""",
    expected="    1000.0     0.826877394331     0.826879540532    2.146e-06",
    seealso="沒有區間縮減的話,$x=1000$ 直接展開會完全失控;加了縮減之後,"
            "$x=1000$ 的誤差($2.1\\times10^{-6}$)和 $x=1$ 的誤差($2.7\\times10^{-6}$)"
            "<strong>同一個量級</strong>——誤差在整條實數線上幾乎是平的。"
            "剩下的誤差來自 7 次多項式本身,再多兩項就能壓到 $10^{-11}$ 以下。",
    todo="""# TODO 學生練習:把 my_sin 的多項式砍到 5 次(去掉 x2/5040 那項)
# 最大誤差變成多少?符合觀念 8 的誤差表嗎?""")

LAB4 = Lab(
    title="Lab 4｜泰勒證明的預測:中央差分真的是 O(h²) 嗎",
    intro="觀念 10 用泰勒算出前向差分是 $O(h)$、中央差分是 $O(h^2)$,"
          "最佳步長分別是 $\\sqrt{\\varepsilon}$ 與 $\\varepsilon^{1/3}$。這格檢驗這些預測。",
    code="""f, df = math.sin, math.cos
x0 = 1.0
exact = df(x0)

hs = np.array([10.0**(-k) for k in np.arange(1, 16, 0.5)])
fwd = np.array([abs((f(x0+h) - f(x0))/h - exact) for h in hs])
ctr = np.array([abs((f(x0+h) - f(x0-h))/(2*h) - exact) for h in hs])

plt.loglog(hs, np.maximum(fwd, 1e-18), 'o-', label='forward  O(h)')
plt.loglog(hs, np.maximum(ctr, 1e-18), 's-', label='central  O(h^2)')
eps = np.finfo(float).eps
plt.axvline(np.sqrt(eps),   color='C0', ls='--', label='sqrt(eps)')
plt.axvline(eps**(1/3),     color='C1', ls=':',  label='eps^(1/3)')
plt.gca().invert_xaxis(); plt.xlabel('h'); plt.ylabel('|error|'); plt.legend(fontsize=8)
plt.title('Taylor predicts both the slope and the optimum')
plt.show()

print("前向差分最佳 h =", f"{hs[np.argmin(fwd)]:.2e}", "  預測 sqrt(eps) =", f"{np.sqrt(eps):.2e}")
print("中央差分最佳 h =", f"{hs[np.argmin(ctr)]:.2e}", "  預測 eps^(1/3) =", f"{eps**(1/3):.2e}")

# 檢查斜率:在截斷誤差主導的區段,log-log 斜率應為 1 與 2
big = hs > 1e-4
for name, e in [('forward', fwd), ('central', ctr)]:
    slope = np.polyfit(np.log10(hs[big]), np.log10(e[big]), 1)[0]
    print(f"{name} 在大 h 區段的 log-log 斜率 = {slope:.3f}")""",
    expected="forward 在大 h 區段的 log-log 斜率 = 1.000\ncentral 在大 h 區段的 log-log 斜率 = 2.000",
    seealso="兩條線在截斷誤差主導的區段,斜率<strong>正好</strong>是 1 與 2,"
            "和泰勒推出的 $O(h)$、$O(h^2)$ 完全吻合;最佳步長也落在預測的 "
            "$\\sqrt{\\varepsilon}$ 與 $\\varepsilon^{1/3}$ 附近。",
    todo="")

LABS = [LAB1, LAB2, LAB3, LAB4]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="銜接課用了羅必達一整週,但從沒說它為什麼成立。今天補上——"
         "順便拆穿一件事:你們一直用它算 $\\lim\\frac{\\sin x}{x}$,那其實是<strong>違法的</strong>。",
    fastforward=[
        ("Rolle 與 MVT 的敘述", "銜接課講過", "快轉,但要複習「造輔助函數」這招"),
        ("Cauchy 均值定理", "<strong>全新</strong>", "中速(它只是 L'Hôpital 的墊腳石)"),
        ("<strong>L'Hôpital 的證明</strong>", "<strong>全新</strong>", "踩煞車(證明時刻)"),
        ("循環論證:$\\frac{\\sin x}{x}$ 的陷阱", "全新,而且顛覆認知", "務必講,學生會記一輩子"),
        ("泰勒多項式與係數的來源", "全新,但從線性近似長出來", "中速"),
        ("四個必背展開與代換技巧", "全新", "練到熟"),
        ("餘項與誤差估計", "最難,但最有用", "踩煞車"),
        ("函式庫怎麼算 sin", "全新,資工系會很有感", "輕鬆帶"),
    ],
    outcomes=[
        "從 Rolle 出發,造輔助函數推出 MVT 與 Cauchy MVT。",
        "完整說出 L'Hôpital 的證明,並指出<strong>哪一步</strong>用掉了 $\\frac00$ 的條件。",
        "解釋為什麼用 L'Hôpital 算 $\\lim\\frac{\\sin x}{x}$ 是循環論證,並說出正確的幾何證法。",
        "寫出 $e^{x},\\sin x,\\cos x,\\ln(1+x)$ 的展開,並用<strong>代換</strong>導出 "
        "$e^{-x^{2}}$ 之類的展開。",
        "用 Lagrange 餘項估計誤差,並決定「要取幾階才夠準」。",
    ],
    clock=[
        ("00:00–00:10", "收作業、回顧反函數微分公式", "—"),
        ("00:10–00:25", "Rolle → MVT:複習「造輔助函數」這一招", "觀念 1"),
        ("00:25–00:50", "Cauchy 均值定理(雙函數版 MVT)", "觀念 2"),
        ("00:50–00:55", "休息", "—"),
        ("00:55–01:30", "<strong>證明時刻</strong>:L'Hôpital 為何成立", "觀念 3"),
        ("01:30–01:50", "循環論證:$\\frac{\\sin x}{x}$ 的陷阱", "觀念 4"),
        ("01:50–01:55", "休息", "—"),
        ("01:55–02:25", "泰勒多項式:從切線再往上走一階", "觀念 5–6"),
        ("02:25–02:50", "餘項與「該取幾階」", "觀念 7–8"),
        ("02:50–03:00", "函式庫怎麼算 sin + 接回 W1 的浮點數", "觀念 9–10"),
    ],
    proof_moment="用 Cauchy MVT 證明 L'Hôpital 法則($\\frac00$ 情形)。"
                 "關鍵在<strong>第二步</strong>——因為 $f(a)=g(a)=0$,"
                 "Cauchy MVT 的左式才會塌縮成 $\\frac{f(x)}{g(x)}$。"
                 "把這一步圈起來:它就是「為什麼非不定型不能用羅必達」的答案。",
    script=[
        ("開場:你們一直在用一個沒證過的定理(10 分)",
         "<p>「上個暑假你們用羅必達用得很開心。有沒有人問過:它<strong>為什麼</strong>對?」</p>"
         "<p>停三秒。「今天證給你們看。而且證完之後,你們會發現有一題其實不能用它——"
         "而那題正是你們最常拿它算的。」</p>"
         "<p>懸念留著,先複習 Rolle 與 MVT——重點不是敘述,是<strong>造輔助函數</strong>那一招,"
         "今天要用三次。</p>"),
        ("Cauchy MVT:兩台車一起跑(25 分)",
         "<p>先給直覺:「兩台車同時出發同時到。$f$ 跑的距離比 $g$ 跑的距離,"
         "等於<strong>某一瞬間</strong>兩車速度的比。」</p>"
         "<p>然後造輔助函數。這裡不要讓學生自己想——直接給 "
         "$h=[f(b)-f(a)]g(x)-[g(b)-g(a)]f(x)$,讓他們<strong>驗證</strong> $h(a)=h(b)$。"
         "動手算一次比看你推十遍有效。</p>"
         "<p><strong>一定要問的問題</strong>:「為什麼不能對 $f$、$g$ 各用一次 MVT 再相除?」"
         "答案:兩次的 $c$ 不一樣。Cauchy MVT 的全部價值就在「同一個 $c$」。</p>"),
        ("證明時刻:L'Hôpital 為何成立(35 分)",
         "<p>三步驟寫在黑板上,每步各一行:</p>"
         "<p class='step'>① 在 $[a,x]$ 上用 Cauchy MVT ⟹ "
         "$\\dfrac{f(x)-f(a)}{g(x)-g(a)}=\\dfrac{f'(c_x)}{g'(c_x)}$</p>"
         "<p class='step'>② 代入 $f(a)=g(a)=0$ ⟹ $\\dfrac{f(x)}{g(x)}=\\dfrac{f'(c_x)}{g'(c_x)}$</p>"
         "<p class='step'>③ $x\\to a$ 時 $c_x$ 被夾住也 $\\to a$ ⟹ 兩邊取極限</p>"
         "<p><strong>把第 ② 步圈起來</strong>,用紅筆。「這裡,就這裡,用掉了 $\\frac00$ 的條件。"
         "所以非不定型用羅必達會錯——不是規定不准,是<strong>證明在這裡斷掉</strong>。」</p>"
         "<p>這句話講完,學生對「先檢查型態」這件事的態度會完全不一樣。</p>"),
        ("循環論證:今天最重要的十五分鐘(20 分)",
         "<p>「現在回到開場那個懸念。$\\lim_{x\\to0}\\frac{\\sin x}{x}$,能不能用羅必達?」</p>"
         "<p>大部分人會說能。那就在黑板上算一次:$\\frac{\\cos x}{1}\\to1$。「答案對啊。」</p>"
         "<p>然後問:「你怎麼知道 $(\\sin x)'=\\cos x$?」把定義展開寫出來,"
         "$\\lim\\frac{\\sin h}{h}$ 就<strong>浮在黑板上</strong>。</p>"
         "<p>「所以你用『$\\lim\\frac{\\sin x}{x}=1$』證明了『$\\lim\\frac{\\sin x}{x}=1$』。」</p>"
         "<p>讓這句話停留五秒。然後給分寸:<strong>當驗算可以,當證明不行</strong>。"
         "正確證法是單位圓夾擠,銜接課教過,那個證明<strong>不可被取代</strong>。</p>"
         "<p>補上另一個誤解:$\\lim_{x\\to\\infty}\\frac{x+\\sin x}{x}$——羅必達失效,"
         "但極限存在。<strong>算不出來 ≠ 不存在</strong>。</p>"),
        ("泰勒多項式:切線只是第一階(30 分)",
         "<p>從他們會的東西出發:「線性近似對齊了函數值和斜率。為什麼停在那?」</p>"
         "<p>推係數的時候,重點放在<strong>那個 $k!$ 是哪來的</strong>——"
         "把 $c_k(x-a)^k$ 微分 $k$ 次會掉出 $k!$。講清楚這件事,學生就不會背錯公式。</p>"
         "<p>四個必背展開寫在黑板上,然後<strong>示範代換</strong>:"
         "$e^{-x^2}$ 不要微分,把 $u$ 換掉就好。這個對比(十分鐘 vs 三十秒)很有說服力。</p>"
         "<p>順手寫一下 $e^{ix}$ 的實部虛部,讓他們驚訝三十秒,但不要深入——那是複變的事。</p>"),
        ("餘項:從「看起來準」到「保證多準」(25 分)",
         "<p>「近似很好,但工程上要能<strong>保證</strong>。」給 Lagrange 餘項。</p>"
         "<p>形狀好記:<strong>就是下一項,導數換個點取</strong>。$n=0$ 時就是 MVT——"
         "指出這件事,學生會發現今天所有定理都是一家人。</p>"
         "<p>$\\xi$ 不知道怎麼辦?找<strong>上界</strong>。$\\sin,\\cos$ 特別好:$M=1$。</p>"
         "<p>然後給那張表(觀念 8),重點是最後一欄:<strong>縮小區間比增加項數划算太多</strong>。"
         "這句話直接接到下一段。</p>"),
        ("收尾:你每天呼叫的 sin 長什麼樣(10 分)",
         "<p>「$\\sin(1000)$,要在 $a=0$ 展開幾項?」讓他們用誤差界估一下——大得離譜。</p>"
         "<p>「所以函式庫不這樣做。它先<strong>縮區間</strong>,再用<strong>短多項式</strong>。」"
         "兩階段講完,實作課 Lab 3 會真的寫一個出來。</p>"
         "<p>最後接回 W1:「縮區間時要算 $x-2k\\pi$,兩個相近大數相減——"
         "這是什麼問題?」(災難性消去)兩週的東西在這裡合體,收得漂亮。</p>"),
    ],
    myths=[
        "把羅必達用在非不定型上。證明的第二步需要 $\\frac00$,沒有它整條推理就斷了。",
        "用羅必達「證明」$\\lim\\frac{\\sin x}{x}=1$——循環論證。",
        "以為「羅必達算不出來」等於「極限不存在」。$\\frac{x+\\sin x}{x}$ 就是反例。",
        "對 $f$、$g$ 各用一次 MVT 再相除。兩個 $c$ 不同,不能這樣做。",
        "泰勒係數漏掉 $k!$。",
        "把餘項裡的 $\\xi$ 當成 $a$ 代進去。$\\xi$ 未知,只能取上界。",
        "以為展開越多項越好。$|x-a|$ 太大時,增加項數的效果差得驚人。",
    ],
    exit_check=[
        ("L'Hôpital 的證明中,哪一步用掉了 $f(a)=g(a)=0$ 這個條件?",
         "第二步——把 Cauchy MVT 的左式 $\\frac{f(x)-f(a)}{g(x)-g(a)}$ 化簡成 "
         "$\\frac{f(x)}{g(x)}$ 的時候。"),
        ("為什麼不能用 L'Hôpital 證明 $\\displaystyle\\lim_{x\\to0}\\frac{\\sin x}{x}=1$?",
         "因為要用它就得先知道 $(\\sin x)'=\\cos x$,而那條導數正是<strong>用這個極限</strong>"
         "推出來的——循環論證。"),
        ("用 $P_{3}$ 近似 $\\sin(0.5)$,誤差最多多少?",
         "$\\left|R_{3}\\right|\\le\\dfrac{(0.5)^{4}}{4!}=\\dfrac{0.0625}{24}"
         "\\approx2.6\\times10^{-3}$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W3-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "觀念 3 的證明要能默寫三步驟。",
        "<strong>預習</strong>:本書第 12 章的「積分」段落——下週開始進積分技巧,"
        "第一招是把乘積法則反過來走。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 D1 MVT c for x^2 on [0,3]", "solve(Eq(diff(x**2, x), 3), x)[0]", "Rational(3,2)"),
    ("C1 D2 Rolle c for x^2-4x+3", "solve(diff(x**2-4*x+3, x), x)[0]", "2"),
    ("C2 示範 Cauchy c for f=x^2,g=x^3 on [1,2]", "solve(Eq(2*x/(3*x**2), Rational(3,7)), x)[0]",
     "Rational(14,9)"),
    ("C2 D1 Cauchy c for f=x^2,g=x on [0,2]", "solve(Eq(2*x, 2), x)[0]", "1"),
    ("C2 D2 Cauchy c for f=x^3,g=x^2 on [1,2]", "solve(Eq(3*x/2, Rational(7,3)), x)[0]",
     "Rational(14,9)"),
    ("C3 D2 lim (e^x-1-x)/x^2", "limit((exp(x)-1-x)/x**2, x, 0)", "Rational(1,2)"),
    ("C3 D3 lim cos(x)/(1+x) 非不定型", "limit(cos(x)/(1+x), x, 0)", "1"),
    ("C4 D1 lim (x+sin x)/x at oo", "limit((x+sin(x))/x, x, oo)", "1"),
    ("C5 示範 P3 of exp", "series(exp(x), x, 0, 4).removeO()",
     "1 + x + x**2/2 + x**3/6"),
    ("C5 示範 P3 of sin", "series(sin(x), x, 0, 4).removeO()", "x - x**3/6"),
    ("C5 D1 P2 of sqrt(x) at 4 的二次係數 -1/64",
     "diff(sqrt(x), x, 2).subs(x, 4)/factorial(2)", "Rational(-1,64)"),
    ("C5 D2 P4 of ln(1+x)", "series(log(1+x), x, 0, 5).removeO()",
     "x - x**2/2 + x**3/3 - x**4/4"),
    ("C5 D3 P4 of cos", "series(cos(x), x, 0, 5).removeO()", "1 - x**2/2 + x**4/24"),
    ("C6 示範 exp(-x^2) 展開到 x^4", "series(exp(-x**2), x, 0, 5).removeO()",
     "1 - x**2 + x**4/2"),
    ("C6 D1 sin(x^2) 展開到 x^6", "series(sin(x**2), x, 0, 7).removeO()", "x**2 - x**6/6"),
    ("C6 D2 1/(1-x) 展開到 x^3", "series(1/(1-x), x, 0, 4).removeO()", "1 + x + x**2 + x**3"),
    ("C7 示範 sin(0.5) 餘項界 (0.5)^7/7!", "Rational(1,2)**7/factorial(7)",
     "Rational(1,645120)"),
    ("C7 D2 9! < 1e6 < 10!", "factorial(10) - 3628800", "0"),
    ("C8 示範 cos(0.3) n=7 誤差界 < 1e-8",
     "floor(log((Rational(3,10)**8/factorial(8)), 10))", "-9"),
    ("C10 中央差分 O(h^2):展開後 f'' 項抵消",
     "simplify(series(sin(x+h), h, 0, 4).removeO() - series(sin(x-h), h, 0, 4).removeO() "
     "- 2*h*cos(x) + h**3*cos(x)/3)", "0"),
]

WEEK = Week(
    num=3,
    title="Cauchy 均值定理、L'Hôpital 的證明與泰勒多項式",
    subtitle="銜接課用了羅必達一整週卻沒說它為什麼成立。這週補上證明,"
             "順便拆穿一個大家都在犯的循環論證,最後用泰勒多項式把「近似」變成「有保證的近似」。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["補上缺的證明"],
)
