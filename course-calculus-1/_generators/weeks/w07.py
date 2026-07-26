# -*- coding: utf-8 -*-
"""第 7 週｜積分技巧總整理與數值積分

四招學完了,但有些積分沒有初等原函數(W4 已經預告過)。
這週轉向:不求公式,只求數字。而且要能保證數字有多準。
證明時刻:用泰勒展開證明 Simpson 法則的誤差是 O(h^4)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="When the Techniques Run Out", title_zh="四招都失效時",
    sub="Some integrals have no elementary antiderivative — that is a theorem, not a skill gap",
    idea="$\\displaystyle\\int e^{-x^{2}}dx$, $\\displaystyle\\int\\frac{\\sin x}{x}dx$ and "
         "$\\displaystyle\\int\\frac{dx}{\\ln x}$ have no elementary antiderivative — Liouville's "
         "theorem proves it. Yet their definite integrals are perfectly well-defined numbers. "
         "Numerical integration computes those numbers.",
    deep="<p><strong>先把話說清楚</strong>,免得學生以為是自己太笨。</p>"
         "<p class='step'>「沒有初等原函數」是一個<strong>被證明的定理</strong>"
         "(Liouville,1835),不是「還沒有人想出來」。就像 $\\sqrt2$ 是無理數一樣,"
         "是關於這個對象的事實。</p>"
         "<p><strong>但定積分照樣存在</strong>。$\\displaystyle\\int_{0}^{1}e^{-x^{2}}dx$ "
         "是一個確定的實數(約 $0.7468$),因為被積函數連續,黎曼和的極限存在。"
         "<strong>「積不出公式」和「這個數不存在」是兩回事</strong>。</p>"
         "<p><strong>三種情境需要數值積分</strong>:</p>"
         "<ol>"
         "<li>原函數不是初等函數(如 $e^{-x^{2}}$——而它正是常態分佈的核心)</li>"
         "<li>原函數存在但醜到不值得算(很多工程問題)</li>"
         "<li><strong>你根本沒有公式,只有資料點</strong>(感測器讀數、實驗數據)——"
         "這在 CS 裡最常見</li>"
         "</ol>"
         "<p>第三種特別值得強調:實務上你拿到的常常是一串數字,不是函數。"
         "那時候符號積分毫無用武之地,數值方法是<strong>唯一</strong>的選擇。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\displaystyle\\int e^{-x^{2}}dx$ 你會用哪一招?換元?分部?三角代換?部分分式?",
           "四招都試過都不行。這表示你不夠強,還是這題本來就沒有初等原函數?",
           "$\\displaystyle\\int_{0}^{1}e^{-x^{2}}dx$ 這個<strong>數字</strong>存在嗎?"
           "(想:被積函數連續嗎?黎曼和收斂嗎?)",
           "如果你手上只有一串感測器讀數,沒有函數公式,還能算積分嗎?"],
    demo="Explain why $\\displaystyle\\int_{0}^{1}e^{-x^{2}}dx$ is a well-defined number even "
         "though $e^{-x^{2}}$ has no elementary antiderivative.",
    demo_sol="<p><strong>存在性</strong>:$e^{-x^{2}}$ 在 $[0,1]$ 上連續。"
             "由定積分的定義(W1 的黎曼和取極限,銜接課教過),連續函數在閉區間上必可積,"
             "所以這個極限存在,是一個確定的實數。</p>"
             "<p><strong>算不出公式</strong>:Liouville 定理證明了它的原函數不能用"
             "有限多個初等函數(多項式、指數、對數、三角及其反函數)組合表示。"
             "數學家把它命名為 $\\operatorname{erf}$,那是<strong>定義</strong>,不是求解。</p>"
             "<p><strong>兩者不矛盾</strong>:「這個數存在」由定積分的定義保證;"
             "「找不到公式」是關於初等函數這個<em>集合</em>的限制。</p>"
             "<p>數值上,$\\displaystyle\\int_{0}^{1}e^{-x^{2}}dx\\approx0.746824132812$——"
             "本週結束時你會自己算出這 12 位數字。</p>",
    demo_hint="分開想兩件事:①這個數存不存在 ②能不能用公式表示。",
    misstep="以為「積不出來」代表「答案不存在」。定積分是黎曼和的極限,和有沒有公式無關。",
    level="basic",
    drills=[
        ("Which of these have elementary antiderivatives? "
         "(i) $xe^{-x^{2}}$ &nbsp; (ii) $e^{-x^{2}}$ &nbsp; (iii) $\\dfrac{\\sin x}{x}$",
         "<p>只有 (i):換元 $t=x^{2}$ 得 $-\\dfrac{e^{-x^{2}}}{2}+C$。"
         "(ii)(iii) 都沒有初等原函數。<strong>差一個 $x$,命運完全不同</strong>。</p>"),
        ("Give a situation in computing where you must integrate but have no formula at all.",
         "<p>例:感測器每 $0.1$ 秒回傳一個加速度讀數,要算總位移(積分兩次);"
         "或用蒙地卡羅估計高維積分。這時只有離散資料點,沒有函數。</p>"),
        ("Is $\\displaystyle\\int_{0}^{1}\\frac{\\sin x}{x}dx$ well-defined at $x=0$?",
         "<p>是。$\\dfrac{\\sin x}{x}$ 在 $x=0$ 雖無定義,但 $\\displaystyle\\lim_{x\\to0}"
         "\\dfrac{\\sin x}{x}=1$ 是可去間斷,補上 $f(0)=1$ 後連續,積分存在。</p>"),
    ])

C2 = Concept(
    title_en="The Trapezoid Rule", title_zh="梯形法",
    sub="Replace the curve by straight segments — the simplest honest approximation",
    idea="Partition $[a,b]$ into $n$ equal strips of width $h=\\frac{b-a}{n}$ and replace the "
         "curve on each strip by a straight chord: "
         "$$T_{n}=h\\left[\\frac{f_{0}}{2}+f_{1}+f_{2}+\\cdots+f_{n-1}+\\frac{f_{n}}{2}\\right].$$",
    deep="<p>銜接課教過黎曼和(左端點、右端點、中點)。梯形法就是<strong>左和與右和的平均</strong>:</p>"
         "$$T_{n}=\\frac{L_{n}+R_{n}}{2}.$$"
         "<p>幾何上,用左端點是把每段當成矩形(高取左邊),用右端點取右邊,"
         "平均起來就是<strong>梯形</strong>——上底 $f_{i}$、下底 $f_{i+1}$、高 $h$。</p>"
         "<p class='step'><strong>為什麼端點的係數是 $\\frac12$</strong>:把所有梯形面積加起來,</p>"
         "$$\\sum_{i=0}^{n-1}\\frac{h}{2}\\left(f_{i}+f_{i+1}\\right)"
         "=h\\left[\\frac{f_{0}}{2}+f_{1}+\\cdots+f_{n-1}+\\frac{f_{n}}{2}\\right],$$"
         "<p>中間每個 $f_{i}$ 被<strong>兩個相鄰梯形各用一次</strong>,所以係數是 $1$;"
         "頭尾各只被用一次,所以是 $\\frac12$。這個「數係數」的直覺對理解 Simpson 也有用。</p>"
         "<p><strong>凹凸決定高估或低估</strong>:凹向上時弦在曲線上方,梯形法<strong>高估</strong>;"
         "凹向下時低估。這件事等一下的誤差公式會用符號說一遍——"
         "而學生用圖就能先猜到答案。<span class='qed'>∎</span></p>",
    guide=["把 $[a,b]$ 切成 $n$ 段,每段寬 $h=$ <span class=\"blank\"></span>。",
           "每一段用梯形取代曲線,面積是 $\\dfrac{h}{2}\\left(f_{i}+f_{i+1}\\right)$。"
           "把 $n$ 段加起來,中間的 $f_{i}$ 各被算 <span class=\"blank\"></span> 次。",
           "所以頭尾的係數是 <span class=\"blank\"></span>、中間是 $1$。",
           "如果函數凹向上,梯形的弦在曲線上方還是下方?所以 $T_{n}$ 高估還是低估?"],
    demo="Estimate $\\displaystyle\\int_{0}^{1}\\frac{dx}{1+x^{2}}$ with the trapezoid rule using "
         "$n=4$, and compare with the exact value $\\frac{\\pi}{4}$.",
    demo_sol="<p>$h=0.25$,節點 $x=0,\\,0.25,\\,0.5,\\,0.75,\\,1$,函數值</p>"
             "$$f=1,\\ 0.941176,\\ 0.8,\\ 0.64,\\ 0.5.$$"
             "$$T_{4}=0.25\\left[\\frac{1}{2}+0.941176+0.8+0.64+\\frac{0.5}{2}\\right]"
             "=0.25\\times3.131176=0.782794.$$"
             "<p>精確值 $\\dfrac{\\pi}{4}=0.785398$,誤差 $2.60\\times10^{-3}$。</p>"
             "<p>$\\dfrac{1}{1+x^{2}}$ 在 $[0,1]$ 上凹向下(前半段)為主,"
             "整體結果<strong>低估</strong>——和圖形一致。</p>",
    demo_hint="先算 $h$ 和五個節點的函數值,頭尾記得乘 $\\frac12$。",
    misstep="忘記頭尾要乘 $\\frac12$,把所有點都當成係數 $1$。",
    level="mid",
    drills=[
        ("Estimate $\\displaystyle\\int_{0}^{1}x^{2}dx$ with $T_{2}$ and compare with the exact "
         "value $\\frac13$.",
         "<p>$h=0.5$,$f=0,0.25,1$。$T_{2}=0.5\\left[0+0.25+0.5\\right]=0.375$。"
         "精確 $0.3\\overline{3}$,誤差 $0.0417$,<strong>高估</strong>(因為 $x^{2}$ 凹向上)。</p>"),
        ("Why is $T_{n}$ the average of the left and right Riemann sums?",
         "<p>$L_{n}=h\\sum_{i=0}^{n-1}f_{i}$、$R_{n}=h\\sum_{i=1}^{n}f_{i}$,"
         "平均後頭尾各只剩一半,中間各為 $1$,恰為 $T_{n}$。</p>"),
        ("For a function that is concave up on $[a,b]$, does $T_{n}$ overestimate or "
         "underestimate?",
         "<p>高估。凹向上時弦(梯形的斜邊)在曲線<strong>上方</strong>,面積算多了。</p>"),
    ])

C3 = Concept(
    title_en="Error of the Trapezoid Rule", title_zh="梯形法的誤差",
    sub="O(h²): halve the step, quarter the error",
    idea="$$\\left|\\int_{a}^{b}f-T_{n}\\right|\\le\\frac{(b-a)h^{2}}{12}\\max|f''|.$$ "
         "The error is $O(h^{2})$: halving $h$ divides the error by four. The $f''$ tells you it "
         "is exact for straight lines.",
    deep="<p><strong>三件事要從公式讀出來</strong>:</p>"
         "<ul>"
         "<li><strong>$h^{2}$</strong> ⟹ 二階。$h$ 減半,誤差變 $\\frac14$。實作課會驗證這個比值。</li>"
         "<li><strong>$f''$</strong> ⟹ 對<strong>一次多項式</strong>完全精確"
         "($f''=0$,誤差為零)。合理:直線用梯形當然剛好。</li>"
         "<li><strong>$(b-a)$</strong> ⟹ 區間越長誤差越大。</li>"
         "</ul>"
         "<p class='step'><strong>單段的誤差怎麼來</strong>(泰勒,不必背):在一段 "
         "$[x_{i},x_{i+1}]$ 上,把 $f$ 在中點展開再積分,一次項因對稱而消掉,"
         "留下的主項正比於 $h^{3}f''$。$n$ 段加起來、$n=\\frac{b-a}{h}$,"
         "總誤差就是 $O(h^{2})$。</p>"
         "<p><strong>符號也有意義</strong>:精確版是 "
         "$\\int f-T_{n}=-\\frac{(b-a)h^{2}}{12}f''(\\xi)$。"
         "$f''&gt;0$(凹向上)時右邊為負,即 $T_{n}&gt;\\int f$——<strong>高估</strong>,"
         "和觀念 2 用圖看到的一致。<strong>公式和圖形對得上,才算真的懂</strong>。</p>"
         "<p><strong>實務用法</strong>:給定容許誤差 $\\tau$,解 "
         "$\\frac{(b-a)h^{2}}{12}M_{2}&lt;\\tau$ 得所需的 $h$,再換算 $n$。觀念 8 會練這個。"
         "<span class='qed'>∎</span></p>",
    guide=["誤差公式裡有 $h^{2}$。如果把 $h$ 減半,誤差大約變成原來的 <span class=\"blank\"></span>。",
           "公式裡有 $\\max|f''|$。如果 $f$ 是一次函數,$f''=$ <span class=\"blank\"></span>,"
           "誤差是多少?這合理嗎?",
           "精確版是 $\\int f-T_{n}=-\\dfrac{(b-a)h^{2}}{12}f''(\\xi)$。"
           "$f''&gt;0$ 時,$T_{n}$ 比真值大還是小?",
           "這和你在觀念 2 用圖形猜的答案一樣嗎?"],
    demo="Bound the error of $T_{4}$ for $\\displaystyle\\int_{0}^{1}x^{2}dx$, and compare with "
         "the actual error.",
    demo_sol="<p>$f=x^{2}$,$f''=2$,故 $\\max|f''|=2$。$h=0.25$、$b-a=1$:</p>"
             "$$\\left|\\text{誤差}\\right|\\le\\frac{1\\times(0.25)^{2}}{12}\\times2"
             "=\\frac{0.0625}{6}\\approx1.042\\times10^{-2}.$$"
             "<p><strong>實際誤差</strong>:$T_{4}=0.25\\left[0+0.0625+0.25+0.5625+0.5\\right]"
             "=0.34375$,精確 $\\frac13$,誤差 $=1.042\\times10^{-2}$。</p>"
             "<p><strong>界恰好等於實際誤差</strong>!因為 $f''$ 是常數,"
             "泰勒餘項裡的 $f''(\\xi)$ 不論 $\\xi$ 取哪裡都一樣,不等式變成等式。"
             "這是檢驗公式沒記錯的好方法。</p>",
    demo_hint="先找 $\\max|f''|$。$f=x^{2}$ 的二階導數是常數,所以界會很緊。",
    misstep="把 $h$ 和 $n$ 搞混。公式裡是 $h=\\frac{b-a}{n}$,不是 $n$。",
    level="mid",
    drills=[
        ("If $T_{10}$ has error $10^{-3}$, roughly what error does $T_{20}$ have?",
         "<p>$h$ 減半 ⟹ 誤差約 $\\dfrac14$,即 $2.5\\times10^{-4}$。</p>"),
        ("Why is the trapezoid rule exact for $f(x)=3x+1$?",
         "<p>$f''=0$,誤差界為零。幾何上直線的梯形就是它本身,一點誤差也沒有。</p>"),
        ("Bound the error of $T_{n}$ for $\\displaystyle\\int_{0}^{\\pi}\\sin x\\,dx$ with $n=6$.",
         "<p>$\\max|f''|=\\max|-\\sin x|=1$,$h=\\dfrac{\\pi}{6}$:"
         "$\\dfrac{\\pi\\cdot(\\pi/6)^{2}}{12}\\approx0.0718$。</p>"),
    ])

C4 = Concept(
    title_en="Simpson's Rule", title_zh="辛普森法則",
    sub="Fit parabolas through pairs of strips instead of chords",
    idea="Using $n$ strips with $n$ <em>even</em>, fit a parabola through each consecutive triple "
         "of points: "
         "$$S_{n}=\\frac{h}{3}\\left[f_{0}+4f_{1}+2f_{2}+4f_{3}+\\cdots+4f_{n-1}+f_{n}\\right].$$ "
         "The $1,4,2,4,\\ldots,4,1$ pattern is the signature.",
    deep="<p>梯形法用<strong>直線</strong>逼近,Simpson 用<strong>拋物線</strong>——"
         "多一階,準得多。</p>"
         "<p class='step'><strong>係數的來歷</strong>:在 $[-h,h]$ 上過三點 "
         "$(-h,f_{0})$、$(0,f_{1})$、$(h,f_{2})$ 配一條拋物線,積分後可得</p>"
         "$$\\int_{-h}^{h}p(x)dx=\\frac{h}{3}\\left(f_{0}+4f_{1}+f_{2}\\right).$$"
         "<p>把區間兩段兩段處理再串起來,中間的分界點被<strong>相鄰兩組各用一次</strong>,"
         "所以係數 $1+1=2$;每組的中點只被自己用,係數 $4$;頭尾各 $1$。"
         "這就是 $1,4,2,4,\\ldots,4,1$ 的由來。</p>"
         "<p><strong>$n$ 必須是偶數</strong>,因為要兩段配一條拋物線。這是最常見的踩雷點。</p>"
         "<p><strong>驚喜:對三次多項式也精確</strong>。拋物線只有二次,"
         "照理只能對二次以下精確,但實際上<strong>三次也剛好對</strong>——"
         "因為三次項的誤差在對稱區間上正負抵消。"
         "這件事讓 Simpson 的誤差直接跳到 $f^{(4)}$,也就是 $O(h^{4})$(觀念 5)。"
         "<span class='qed'>∎</span></p>",
    guide=["梯形法用直線逼近。如果改用<strong>拋物線</strong>,需要幾個點才決定一條?",
           "所以要<strong>兩段</strong>配一條拋物線。這表示 $n$ 必須是 <span class=\"blank\"></span> 數。",
           "把相鄰兩組的係數疊起來:分界點被算兩次,所以係數是 <span class=\"blank\"></span>;"
           "每組中點只算一次,係數 <span class=\"blank\"></span>。",
           "拋物線是二次的。你猜 Simpson 對三次多項式精不精確?"],
    demo="Estimate $\\displaystyle\\int_{0}^{1}\\frac{dx}{1+x^{2}}$ with $S_{4}$ and compare with "
         "$T_{4}$ from Concept 2.",
    demo_sol="<p>$h=0.25$,節點函數值 $f=1,\\,0.941176,\\,0.8,\\,0.64,\\,0.5$,係數 $1,4,2,4,1$:</p>"
             "$$S_{4}=\\frac{0.25}{3}\\left[1+4(0.941176)+2(0.8)+4(0.64)+0.5\\right]$$"
             "$$=\\frac{0.25}{3}\\times9.424706=0.785392.$$"
             "<p>精確值 $\\dfrac{\\pi}{4}=0.7853982$,誤差 $6.01\\times10^{-6}$。</p>"
             "<p><strong>對比</strong>:同樣 $n=4$、同樣五個函數值,"
             "梯形法誤差 $2.60\\times10^{-3}$、Simpson $6.01\\times10^{-6}$——"
             "<strong>準了 430 倍</strong>,計算量卻幾乎一樣。這就是為什麼實務上很少用梯形法。</p>",
    demo_hint="係數是 $1,4,2,4,1$,最後乘 $\\frac{h}{3}$。",
    misstep="$n$ 取奇數。Simpson 要兩段配一條拋物線,$n$ 必須是偶數。",
    level="mid",
    drills=[
        ("Estimate $\\displaystyle\\int_{0}^{2}\\left(x^{3}-2x+1\\right)dx$ with $S_{2}$ and "
         "compare with the exact value.",
         "<p>$h=1$,$f(0)=1,f(1)=0,f(2)=5$。$S_{2}=\\dfrac13\\left[1+0+5\\right]=2$。"
         "精確值也是 $2$——<strong>誤差為零</strong>,因為 Simpson 對三次多項式精確。</p>"),
        ("Why must $n$ be even in Simpson's rule?",
         "<p>每條拋物線需要三個點、跨兩段。段數必須能兩兩配對,故 $n$ 為偶數。</p>"),
        ("Estimate $\\displaystyle\\int_{0}^{1}x^{2}dx$ with $S_{2}$.",
         "<p>$h=0.5$,$f=0,0.25,1$:$\\dfrac{0.5}{3}\\left[0+1+1\\right]=\\dfrac13$。"
         "<strong>完全精確</strong>(二次多項式)。</p>"),
    ])

C5 = Concept(
    title_en="Why Simpson Is O(h⁴)", title_zh="為什麼 Simpson 是四階",
    sub="Taylor-expand about the midpoint; the odd terms cancel, and so does the cubic",
    idea="Expanding $f$ about the midpoint of a two-strip panel and integrating shows the local "
         "error is $-\\frac{h^{5}}{90}f^{(4)}(\\xi)$. Summing over $\\frac{n}{2}$ panels gives the "
         "global bound "
         "$$\\left|\\int_{a}^{b}f-S_{n}\\right|\\le\\frac{(b-a)h^{4}}{180}\\max\\left|f^{(4)}\\right|.$$",
    deep="<p>本週的<strong>證明時刻</strong>。用的工具是 W3 的泰勒展開——"
         "那時說「泰勒是拿來做有保證的近似」,現在兌現。</p>"
         "<p class='step'><strong>設定</strong>:看單一個兩段面板 $[x_{1}-h,\\ x_{1}+h]$,"
         "在中點 $x_{1}$ 展開:</p>"
         "$$f(x)=f_{1}+f_{1}'(x-x_{1})+\\frac{f_{1}''}{2}(x-x_{1})^{2}"
         "+\\frac{f_{1}'''}{6}(x-x_{1})^{3}+\\frac{f^{(4)}}{24}(x-x_{1})^{4}+\\cdots$$"
         "<p class='step'><strong>真值</strong>:逐項積分。令 $u=x-x_{1}$,"
         "<strong>奇次項在對稱區間 $[-h,h]$ 上積分為零</strong>:</p>"
         "$$\\int_{-h}^{h}f\\,du=2hf_{1}+\\frac{h^{3}}{3}f_{1}''"
         "+\\frac{h^{5}}{60}f_{1}^{(4)}+\\cdots$$"
         "<p class='step'><strong>Simpson 的估計值</strong>:把 $f_{0}=f(x_{1}-h)$、"
         "$f_{2}=f(x_{1}+h)$ 也用泰勒展開代入 $\\frac{h}{3}(f_{0}+4f_{1}+f_{2})$。"
         "$f_{0}+f_{2}$ 相加時奇次項成對消掉:</p>"
         "$$f_{0}+f_{2}=2f_{1}+h^{2}f_{1}''+\\frac{h^{4}}{12}f_{1}^{(4)}+\\cdots$$"
         "$$\\frac{h}{3}\\left(f_{0}+4f_{1}+f_{2}\\right)=2hf_{1}+\\frac{h^{3}}{3}f_{1}''"
         "+\\frac{h^{5}}{36}f_{1}^{(4)}+\\cdots$$"
         "<p class='step'><strong>相減</strong>:前兩項完全一樣、<strong>三次項本來就不在</strong>"
         "(奇次消掉了),第一個活下來的是四階:</p>"
         "$$\\int-S=\\left(\\frac{1}{60}-\\frac{1}{36}\\right)h^{5}f_{1}^{(4)}"
         "=-\\frac{h^{5}}{90}f_{1}^{(4)}.$$"
         "<p><strong>為什麼三次項不見了</strong>:這正是觀念 4 那個「驚喜」的來源。"
         "在對稱區間上,所有<strong>奇次項</strong>(包含三次)的積分都是零,"
         "而 Simpson 的公式也對稱,所以兩邊的奇次項同時消失。"
         "<strong>拋物線公式意外地對三次也精確</strong>,誤差直接跳到四階。</p>"
         "<p class='step'><strong>全域</strong>:$\\frac{n}{2}$ 個面板相加,"
         "$n=\\frac{b-a}{h}$,得</p>"
         "$$\\left|\\int_{a}^{b}f-S_{n}\\right|\\le\\frac{(b-a)h^{4}}{180}"
         "\\max\\left|f^{(4)}\\right|.\\;\\blacksquare$$"
         "<p>$h$ 減半 ⟹ 誤差變 $\\frac{1}{16}$。實作課會量出這個比值。</p>",
    guide=["在面板中點展開 $f$,積分 $\\int_{-h}^{h}u^{k}du$。$k$ 是奇數時等於 "
           "<span class=\"blank\"></span>。",
           "所以真值的展開裡,只剩下 <span class=\"blank\"></span> 次項。",
           "$f_{0}+f_{2}$(左右兩點相加)時,奇次項會怎樣?",
           "兩邊相減,前幾項都消掉,第一個活下來的是幾階?所以誤差是 $O(h^{?})$?"],
    demo="Derive the local error term $-\\dfrac{h^{5}}{90}f^{(4)}$ for Simpson's rule on one "
         "two-strip panel.",
    demo_sol="<p>在中點 $x_{1}$ 展開,令 $u=x-x_{1}$。<strong>真值</strong>(奇次項積分為零):</p>"
             "$$\\int_{-h}^{h}f\\,du=2hf_{1}+\\frac{h^{3}}{3}f_{1}''"
             "+\\frac{h^{5}}{60}f_{1}^{(4)}+O(h^{7}).$$"
             "<p><strong>Simpson 值</strong>:由 "
             "$f_{0}+f_{2}=2f_{1}+h^{2}f_{1}''+\\dfrac{h^{4}}{12}f_{1}^{(4)}+O(h^{6})$,</p>"
             "$$S=\\frac{h}{3}\\left(f_{0}+4f_{1}+f_{2}\\right)"
             "=2hf_{1}+\\frac{h^{3}}{3}f_{1}''+\\frac{h^{5}}{36}f_{1}^{(4)}+O(h^{7}).$$"
             "<p><strong>相減</strong>:</p>"
             "$$\\int-S=\\left(\\frac{1}{60}-\\frac{1}{36}\\right)h^{5}f_{1}^{(4)}"
             "=-\\frac{h^{5}}{90}f_{1}^{(4)}.$$"
             "<p>(檢查:$\\frac{1}{60}-\\frac{1}{36}=\\frac{3-5}{180}=-\\frac{1}{90}$ ✓)"
             "$\\;\\blacksquare$</p>",
    demo_hint="兩邊都用泰勒展開,注意奇次項在對稱區間上會消失。",
    misstep="忘了奇次項消失,以為誤差主項是三階。對稱性是這個證明的關鍵。",
    level="hard",
    drills=[
        ("If $S_{8}$ has error $10^{-6}$, roughly what error does $S_{16}$ have?",
         "<p>$h$ 減半、$O(h^{4})$ ⟹ 誤差約 $\\dfrac{1}{16}$,即 $6.25\\times10^{-8}$。</p>"),
        ("Why is Simpson's rule exact for cubic polynomials even though it fits parabolas?",
         "<p>因為在對稱面板上,三次項(奇次)的積分為零,而 Simpson 公式也對稱、"
         "同樣消掉三次項。兩邊都沒有三次貢獻,所以完全吻合。</p>"),
        ("Bound the error of $S_{4}$ for $\\displaystyle\\int_{0}^{1}e^{x}dx$.",
         "<p>$f^{(4)}=e^{x}$,$\\max=e\\approx2.718$,$h=0.25$:"
         "$\\dfrac{1\\times(0.25)^{4}}{180}\\times e\\approx5.90\\times10^{-5}$。"
         "(實際誤差約 $3.70\\times10^{-5}$,界成立且不算鬆。)</p>"),
    ])

C6 = Concept(
    title_en="Superconvergence", title_zh="超收斂",
    sub="When f‴(b) = f‴(a), the h⁴ term vanishes and Simpson does better than promised",
    idea="The sharper Euler–Maclaurin form of the composite Simpson error begins with a term "
         "proportional to $f'''(b)-f'''(a)$. When that difference is zero, the $h^{4}$ term "
         "disappears and the observed order jumps to $h^{6}$.",
    deep="<p>這一段是<strong>「理論能預測實驗」的示範</strong>,也是本週最好玩的地方。</p>"
         "<p class='step'>複合 Simpson 的誤差有更精細的形式(Euler–Maclaurin):</p>"
         "$$\\int_{a}^{b}f-S_{n}=-\\frac{h^{4}}{180}\\left[f'''(b)-f'''(a)\\right]+O\\!\\left(h^{6}\\right).$$"
         "<p>注意主項只依賴<strong>兩個端點</strong>的三階導數,和中間發生什麼無關。</p>"
         "<p class='step'><strong>所以:若 $f'''(b)=f'''(a)$,主項整個消失</strong>,"
         "誤差退到 $O(h^{6})$——$h$ 減半誤差變 $\\frac{1}{64}$ 而不是 $\\frac{1}{16}$。</p>"
         "<p><strong>一個可以親手驗證的例子</strong>:$f(x)=\\dfrac{1}{1+x^{2}}$ 在 $[0,1]$ 上。</p>"
         "$$f'''(x)=\\frac{-24x\\left(x^{2}-1\\right)}{\\left(1+x^{2}\\right)^{4}}.$$"
         "<p>$f'''(0)=0$(因為分子有 $x$);$f'''(1)=0$(因為分子有 $x^{2}-1$)。"
         "<strong>兩端都是零</strong>,所以這個積分的 Simpson 誤差是 $O(h^{6})$。</p>"
         "<p><strong>實測數據</strong>(實作課會重現):$n=8\\to16$ 誤差比值 $63.9$、"
         "$n=16\\to32$ 比值 $64.0$——<strong>不是 16,是 64</strong>。理論預測完全命中。</p>"
         "<p>對照組:$\\sin x$ 在 $\\left[0,\\frac{\\pi}{2}\\right]$ 的 $f'''(b)-f'''(a)=1\\ne0$,"
         "比值老老實實是 $16$。</p>"
         "<p><strong>這件事的意義</strong>:誤差公式不只給你「階數」,還給你「係數」。"
         "看懂係數,就能<strong>事先預測</strong>哪些題目會意外地準。"
         "這是理論的價值——不是事後解釋,是事前預測。<span class='qed'>∎</span></p>",
    guide=["更精細的誤差主項是 $-\\dfrac{h^{4}}{180}\\left[f'''(b)-f'''(a)\\right]$。"
           "它只跟哪些點有關?",
           "如果 $f'''(b)=f'''(a)$,這個主項會怎樣?那誤差就退到幾階?",
           "算 $f=\\dfrac{1}{1+x^{2}}$ 的三階導數,代 $x=0$ 得 <span class=\"blank\"></span>、"
           "代 $x=1$ 得 <span class=\"blank\"></span>。",
           "所以 $\\int_{0}^{1}\\dfrac{dx}{1+x^{2}}$ 用 Simpson,$h$ 減半誤差會變幾分之一?"],
    demo="Predict the convergence order of Simpson's rule for "
         "$\\displaystyle\\int_{0}^{1}\\frac{dx}{1+x^{2}}$, and verify against the measured error "
         "ratios.",
    demo_sol="<p><strong>預測</strong>:算 $f'''$。由 $f=\\left(1+x^{2}\\right)^{-1}$ 逐階微分得</p>"
             "$$f'''(x)=\\frac{-24x\\left(x^{2}-1\\right)}{\\left(1+x^{2}\\right)^{4}}.$$"
             "<p>$f'''(0)=0$、$f'''(1)=0$(分子的 $x$ 與 $x^{2}-1$ 各自歸零),"
             "故 $f'''(b)-f'''(a)=0$,$h^{4}$ 主項消失 ⟹ 應為 $O\\!\\left(h^{6}\\right)$,"
             "誤差比值應接近 $64$。</p>"
             "<p><strong>實測</strong>:</p>"
             "<div class='tbl-wrap'><table><thead><tr><th>$n$</th><th>誤差</th><th>比值</th>"
             "</tr></thead><tbody>"
             "<tr><td>8</td><td>$3.78\\times10^{-8}$</td><td>—</td></tr>"
             "<tr><td>16</td><td>$5.91\\times10^{-10}$</td><td>$63.9$</td></tr>"
             "<tr><td>32</td><td>$9.24\\times10^{-12}$</td><td>$64.0$</td></tr>"
             "</tbody></table></div>"
             "<p><strong>預測命中</strong>。對照 $\\displaystyle\\int_{0}^{\\pi/2}\\sin x\\,dx$"
             "($f'''(b)-f'''(a)=1\\ne0$),比值是 $16.0$。</p>",
    demo_hint="先算 $f'''$ 在兩個端點的值。相等的話 $h^4$ 項就消失了。",
    misstep="以為超收斂是「運氣好」。它完全可以<strong>事前預測</strong>——算兩個端點的三階導數就知道。",
    level="hard",
    drills=[
        ("For $\\displaystyle\\int_{0}^{2\\pi}\\sin x\\,dx$, compute $f'''(2\\pi)-f'''(0)$ and "
         "predict the behaviour of Simpson's rule.",
         "<p>$f'''=-\\cos x$,$f'''(2\\pi)-f'''(0)=-1-(-1)=0$ ⟹ 主項消失,超收斂。"
         "(事實上週期函數在整個週期上,<strong>所有</strong>階的端點差都為零,"
         "梯形法在這裡甚至是指數收斂。)</p>"),
        ("For $\\displaystyle\\int_{0}^{1}e^{x}dx$, is superconvergence expected?",
         "<p>不會。$f'''=e^{x}$,$f'''(1)-f'''(0)=e-1\\ne0$,主項不為零,標準 $O(h^{4})$,"
         "比值 $16$。</p>"),
        ("What does the Euler–Maclaurin form tell you about integrating a periodic function over "
         "one full period?",
         "<p>所有階的端點差都是零(週期性使 $f^{(k)}(b)=f^{(k)}(a)$),"
         "所有冪次項全部消失 ⟹ 收斂快得驚人。這是 FFT 與週期問題數值方法的理論基礎。</p>"),
    ])

C7 = Concept(
    title_en="Gaussian Quadrature", title_zh="高斯求積",
    sub="Choose the nodes as well as the weights — two points buy you cubic accuracy",
    idea="Instead of equally spaced nodes, choose both nodes and weights optimally. The two-point "
         "Gauss–Legendre rule on $[-1,1]$, "
         "$$\\int_{-1}^{1}f\\,dx\\approx f\\!\\left(-\\tfrac{1}{\\sqrt3}\\right)"
         "+f\\!\\left(\\tfrac{1}{\\sqrt3}\\right),$$ "
         "is exact for all cubics — with only two function evaluations.",
    deep="<p>梯形與 Simpson 都<strong>固定節點</strong>(等距),只調權重。"
         "高斯的洞見:<strong>節點也可以調</strong>。</p>"
         "<p class='step'><strong>數自由度</strong>:$n$ 個點有 $n$ 個節點 + $n$ 個權重 "
         "$=2n$ 個自由度。所以理論上可以讓公式對 $2n-1$ 次以下的多項式全部精確。"
         "$n=2$ ⟹ 三次以下精確,只要<strong>兩次</strong>函數求值。</p>"
         "<p class='step'><strong>兩點公式怎麼來</strong>:設 "
         "$\\int_{-1}^{1}f\\approx w_{1}f(x_{1})+w_{2}f(x_{2})$,要求對 $1,x,x^{2},x^{3}$ 精確:</p>"
         "$$w_{1}+w_{2}=2,\\quad w_{1}x_{1}+w_{2}x_{2}=0,$$"
         "$$w_{1}x_{1}^{2}+w_{2}x_{2}^{2}=\\frac23,\\quad w_{1}x_{1}^{3}+w_{2}x_{2}^{3}=0.$$"
         "<p>由對稱性猜 $w_{1}=w_{2}=1$、$x_{2}=-x_{1}$,代入第三式得 "
         "$2x_{1}^{2}=\\frac23$,即 $x_{1}=\\frac{1}{\\sqrt3}$。四條方程全部滿足。</p>"
         "<p><strong>換到一般區間</strong>:用線性變換 "
         "$x=\\frac{b-a}{2}t+\\frac{a+b}{2}$,則</p>"
         "$$\\int_{a}^{b}f(x)dx=\\frac{b-a}{2}\\int_{-1}^{1}f\\!\\left(\\tfrac{b-a}{2}t"
         "+\\tfrac{a+b}{2}\\right)dt.$$"
         "<p><strong>為什麼實務上到處都是</strong>:同樣的函數求值次數,精度遠高於等距法。"
         "在有限元素法、電腦圖學的光照積分、機器學習的期望值估計裡都是標準工具。"
         "節點看起來是「奇怪的無理數」,但那是<strong>算出來的最佳位置</strong>,不是隨便挑的。"
         "<span class='qed'>∎</span></p>",
    guide=["$n$ 個節點 + $n$ 個權重 = 幾個自由度?所以理論上能對幾次以下的多項式精確?",
           "設兩點公式 $w_{1}f(x_{1})+w_{2}f(x_{2})$,要對 $f=1$ 精確,得 "
           "$w_{1}+w_{2}=$ <span class=\"blank\"></span>。",
           "由對稱性猜 $w_{1}=w_{2}=1$、$x_{2}=-x_{1}$。對 $f=x^{2}$ 精確要求 "
           "$2x_{1}^{2}=$ <span class=\"blank\"></span>,解得 $x_{1}=$ <span class=\"blank\"></span>。",
           "檢查 $f=x^{3}$:$x_{1}^{3}+(-x_{1})^{3}=$ <span class=\"blank\"></span>,"
           "而真值也是 0。所以三次也精確!"],
    demo="Derive the two-point Gauss–Legendre rule on $[-1,1]$ and verify it is exact for "
         "$f(x)=x^{3}$ and $f(x)=x^{2}$.",
    demo_sol="<p><strong>推導</strong>:設 $\\displaystyle\\int_{-1}^{1}f\\approx "
             "w_{1}f(x_{1})+w_{2}f(x_{2})$。由對稱性取 $w_{1}=w_{2}=w$、$x_{2}=-x_{1}$。</p>"
             "<p>對 $f=1$:$2w=2\\Rightarrow w=1$。</p>"
             "<p>對 $f=x^{2}$:$x_{1}^{2}+x_{1}^{2}=\\displaystyle\\int_{-1}^{1}x^{2}dx"
             "=\\frac23\\Rightarrow x_{1}=\\frac{1}{\\sqrt3}$。</p>"
             "<p><strong>驗證</strong>:</p>"
             "<p class='step'>$f=x^{2}$:$\\left(\\frac{1}{\\sqrt3}\\right)^{2}"
             "+\\left(-\\frac{1}{\\sqrt3}\\right)^{2}=\\frac13+\\frac13=\\frac23$ ✓</p>"
             "<p class='step'>$f=x^{3}$:$\\left(\\frac{1}{\\sqrt3}\\right)^{3}"
             "+\\left(-\\frac{1}{\\sqrt3}\\right)^{3}=0$,而 "
             "$\\displaystyle\\int_{-1}^{1}x^{3}dx=0$ ✓</p>"
             "<p><strong>兩個點、三次精確</strong>。Simpson 要三個點才做到同樣的事。</p>",
    demo_hint="用對稱性簡化,再要求對 $1$ 和 $x^{2}$ 精確,就能解出節點與權重。",
    misstep="忘了換區間。$[-1,1]$ 的節點要經線性變換才能用在 $[a,b]$ 上。",
    level="hard",
    drills=[
        ("Use the two-point Gauss rule to estimate $\\displaystyle\\int_{-1}^{1}x^{4}dx$ and "
         "compare with the exact value $\\frac25$.",
         "<p>$2\\times\\left(\\frac{1}{\\sqrt3}\\right)^{4}=2\\times\\dfrac19=\\dfrac29"
         "\\approx0.2222$;精確 $0.4$。<strong>四次就不準了</strong>——"
         "兩點法只保證到三次。</p>"),
        ("How many function evaluations does the three-point Gauss rule need, and up to what "
         "degree is it exact?",
         "<p>三次求值,對<strong>五次</strong>以下精確($2n-1=5$)。"
         "同樣三個點,Simpson 只到三次。</p>"),
        ("Transform $\\displaystyle\\int_{0}^{1}f(x)dx$ into an integral over $[-1,1]$.",
         "<p>令 $x=\\dfrac{t+1}{2}$,$dx=\\dfrac{dt}{2}$:"
         "$\\displaystyle\\int_{0}^{1}f(x)dx=\\frac12\\int_{-1}^{1}"
         "f\\!\\left(\\frac{t+1}{2}\\right)dt$。</p>"),
    ])

C8 = Concept(
    title_en="Choosing n for a Required Accuracy", title_zh="給定精度反推 n",
    sub="Solve the error bound for h, then round n up to something valid",
    idea="Given a tolerance $\\tau$, solve the error bound for $h$ and convert to $n$. For "
         "Simpson: $\\frac{(b-a)h^{4}}{180}M_{4}&lt;\\tau$ where $M_{4}=\\max|f^{(4)}|$. Remember "
         "to round $n$ up, and to make it even.",
    deep="<p>這是<strong>工程上真正會用到</strong>的計算:不是「算完看誤差」,"
         "而是「事先決定要切幾段」。</p>"
         "<p class='step'><strong>步驟</strong>:①求 $M_{4}=\\max\\left|f^{(4)}\\right|$ "
         "②解不等式得 $h$ ③由 $n=\\frac{b-a}{h}$ 得 $n$ ④<strong>無條件進位</strong>並調成偶數。</p>"
         "<p><strong>$M_{4}$ 通常只能估上界</strong>,不必求精確最大值。"
         "例如 $f=e^{x}$ 在 $[0,1]$ 上 $f^{(4)}=e^{x}\\le e&lt;3$,取 $M_{4}=3$ 就夠——"
         "<strong>估寬一點只會讓 $n$ 稍大,不會出錯</strong>;估窄了才危險。</p>"
         "<p><strong>誤差界通常很保守</strong>。實測誤差往往比界小好幾倍(觀念 5 的練習就看到了),"
         "所以按界算出來的 $n$ 是<strong>安全的上限</strong>。實務上常先按界估,"
         "再用「$n$ 加倍看答案變不變」來確認。</p>"
         "<p><strong>四階的威力</strong>:要把精度提高 $10^{4}$ 倍,"
         "梯形法要 $n$ 變 $100$ 倍,Simpson 只要 $10$ 倍。"
         "這個差距在高維或昂貴的函數求值時是決定性的。<span class='qed'>∎</span></p>",
    guide=["Simpson 的誤差界是 $\\dfrac{(b-a)h^{4}}{180}M_{4}$。要它小於 $\\tau$,"
           "$h^{4}$ 要小於 <span class=\"blank\"></span>。",
           "算 $f=e^{x}$ 在 $[0,1]$ 的 $M_{4}$:$f^{(4)}=$ <span class=\"blank\"></span>,"
           "最大值在 $x=1$,約 <span class=\"blank\"></span>。",
           "解出 $h$ 之後,$n=\\dfrac{b-a}{h}$。要進位還是捨去?為什麼?",
           "Simpson 的 $n$ 還有一個額外要求,是什麼?"],
    demo="Find the smallest even $n$ such that Simpson's rule approximates "
         "$\\displaystyle\\int_{0}^{1}e^{x}dx$ with error below $10^{-6}$.",
    demo_sol="<p><strong>① $M_{4}$</strong>:$f^{(4)}=e^{x}$,在 $[0,1]$ 上最大為 "
             "$e\\approx2.719$,取 $M_{4}=2.72$。</p>"
             "<p><strong>② 解 $h$</strong>:</p>"
             "$$\\frac{1\\cdot h^{4}}{180}\\times2.72&lt;10^{-6}"
             "\\ \\Longrightarrow\\ h^{4}&lt;6.62\\times10^{-5}"
             "\\ \\Longrightarrow\\ h&lt;0.0903.$$"
             "<p><strong>③ 換算 $n$</strong>:$n=\\dfrac{1}{h}&gt;11.08$。</p>"
             "<p><strong>④ 進位並取偶數</strong>:$n=12$。</p>"
             "<p><strong>驗證</strong>:$n=12$ 的誤差界是 $7.3\\times10^{-7}$,"
             "實測誤差 $4.6\\times10^{-7}$——兩者都低於要求的 $10^{-6}$ ✓。</p>"
             "<p>注意界只比實際誤差大約 $1.6$ 倍,<strong>相當緊</strong>。"
             "所以按界反推的 $n$ 不會浪費太多計算量。</p>",
    demo_hint="先估 $M_4$ 的上界(寬一點沒關係),再解 $h$,最後 $n$ 進位取偶數。",
    misstep="$n$ 算出 $11.08$ 就取 $11$。要<strong>進位</strong>(不然誤差超標),"
            "而且 Simpson 要偶數,所以是 $12$。",
    level="mid",
    drills=[
        ("Find the smallest $n$ for the trapezoid rule to approximate "
         "$\\displaystyle\\int_{0}^{1}e^{x}dx$ within $10^{-6}$.",
         "<p>$M_{2}=e\\approx2.72$:$\\dfrac{h^{2}}{12}\\times2.72&lt;10^{-6}"
         "\\Rightarrow h&lt;2.10\\times10^{-3}\\Rightarrow n&gt;476$,取 $n=477$。"
         "<strong>對比 Simpson 只要 12</strong>。</p>"),
        ("Why round $n$ up rather than down?",
         "<p>$n$ 越大 $h$ 越小、誤差越小。取小的 $n$ 會讓 $h$ 超過上限,誤差可能超標。</p>"),
        ("For $\\displaystyle\\int_{0}^{\\pi}\\sin x\\,dx$ with Simpson, what is $M_{4}$?",
         "<p>$f^{(4)}=\\sin x$,$\\max|\\sin x|=1$,故 $M_{4}=1$。</p>"),
    ])

C9 = Concept(
    title_en="Using scipy.integrate", title_zh="用現成的工具",
    sub="quad is adaptive — it puts the effort where the function misbehaves",
    idea="<code>scipy.integrate.quad</code> uses adaptive Gauss–Kronrod quadrature: it subdivides "
         "only where the estimated error is large, and returns both the value and an error "
         "estimate. Knowing the theory tells you when to trust it and when to help it.",
    deep="<p>實務上不會自己寫積分器,但<strong>要知道它在做什麼</strong>,"
         "才知道什麼時候該懷疑它。</p>"
         "<p class='step'><strong>自適應(adaptive)是關鍵字</strong>:"
         "等距法在函數平坦的地方浪費了很多求值。自適應法先粗算,估計每個子區間的誤差,"
         "只在<strong>誤差大的地方繼續細分</strong>。</p>"
         "<p class='step'><strong>Gauss–Kronrod</strong>:用兩組節點(一組是另一組的擴充),"
         "兩個結果的差就是誤差估計——<strong>免費得到誤差資訊</strong>,不必多算一輪。</p>"
         "<p><strong>quad 回傳兩個值</strong>:$(\\text{積分值},\\ \\text{誤差估計})$。"
         "第二個值一定要看。如果它很大,表示 quad 自己也心虛。</p>"
         "<p><strong>什麼時候 quad 會出問題</strong>:</p>"
         "<ul>"
         "<li>被積函數有<strong>震盪</strong>(如 $\\sin(1000x)$)——取樣可能全部踩在同一相位</li>"
         "<li>有<strong>奇異點</strong>(如 $\\frac{1}{\\sqrt{x}}$ 在 $0$)——要用 "
         "<code>points=</code> 或 <code>weight=</code> 參數提示它</li>"
         "<li>區間<strong>無窮大</strong>——quad 支援 <code>np.inf</code>,但收斂慢的函數要小心"
         "(下週的主題)</li>"
         "</ul>"
         "<p><strong>一句話</strong>:工具很強,但<strong>你要知道它的假設</strong>。"
         "這正是學理論的實務價值。<span class='qed'>∎</span></p>",
    guide=["等距法在函數很平坦的區域,是不是浪費了很多計算?",
           "自適應法的策略是什麼?(在哪裡多花力氣)",
           "<code>quad</code> 回傳兩個東西,第二個是什麼?為什麼一定要看它?",
           "如果被積函數在 $x=0$ 有奇異點,直接丟給 quad 會怎樣?該怎麼幫它?"],
    demo="Explain what the two return values of <code>scipy.integrate.quad</code> mean, and give "
         "two situations where it can fail.",
    demo_sol="<p><strong>回傳值</strong>:<code>(value, abserr)</code> —— 積分估計值,"
             "以及<strong>絕對誤差的估計</strong>。後者由 Gauss–Kronrod 的兩組節點結果相減得到,"
             "幾乎不花額外成本。</p>"
             "<p><strong>失效情境一:高頻震盪</strong>。"
             "$\\displaystyle\\int_{0}^{1}\\sin(1000x)dx$——取樣點可能剛好落在相似的相位上,"
             "quad 誤以為函數很平滑。對策:提高 <code>limit</code>,或改用專門的震盪積分法。</p>"
             "<p><strong>失效情境二:端點奇異</strong>。"
             "$\\displaystyle\\int_{0}^{1}\\frac{dx}{\\sqrt x}$ 在 $0$ 發散(但積分收斂)。"
             "quad 通常還是算得出來,但會回傳較大的 <code>abserr</code>;"
             "用 <code>points=[0]</code> 提示奇異點位置會更穩。</p>"
             "<p><strong>準則</strong>:先看 <code>abserr</code>,再決定信不信。</p>",
    demo_hint="第二個回傳值是誤差估計。想想什麼樣的函數會騙過取樣。",
    misstep="只取 <code>quad</code> 的第一個回傳值,不看誤差估計。",
    level="mid",
    drills=[
        ("What does <code>quad(f, 0, 1)</code> return, and what should you check first?",
         "<p>回傳 <code>(積分值, 誤差估計)</code>。先檢查<strong>誤差估計</strong>——"
         "如果它比你要求的精度還大,結果就不能信。</p>"),
        ("Why does an adaptive method beat a fixed-grid method for "
         "$f(x)=e^{-1000x^{2}}$ on $[-1,1]$?",
         "<p>這個函數只在 $x\\approx0$ 附近有值,其餘幾乎是零。等距法把大部分求值浪費在平坦區;"
         "自適應法會自動把節點集中到中央的尖峰。</p>"),
        ("Name one situation where you should still write your own quadrature instead of using "
         "<code>quad</code>.",
         "<p>例如:需要在 GPU 上批次計算數百萬個積分(呼叫開銷太大)、"
         "或積分要對參數可微分(自動微分需要純 numpy/torch 的實作)。</p>"),
    ])

C10 = Concept(
    title_en="Numerical or Symbolic?", title_zh="數值還是符號",
    sub="A formula generalises; a number is concrete. Pick by what you need next.",
    idea="Symbolic integration gives a formula valid for all parameters — useful for further "
         "analysis. Numerical integration gives one number, fast and always available. Most real "
         "work uses both: symbolic to understand, numerical to compute.",
    deep="<p>本週收尾,也是給整個積分單元的<strong>方法論</strong>。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th></th><th>符號積分</th><th>數值積分</th>"
         "</tr></thead><tbody>"
         "<tr><td>產出</td><td>公式(對所有參數成立)</td><td>一個數字</td></tr>"
         "<tr><td>可行性</td><td>常常算不出來</td><td>幾乎永遠可行</td></tr>"
         "<tr><td>速度</td><td>可能很慢(或無解)</td><td>快且可預測</td></tr>"
         "<tr><td>後續分析</td><td>可微分、可取極限、可看趨勢</td><td>只能再算更多點</td></tr>"
         "<tr><td>只有資料點時</td><td>不能用</td><td>照常可用</td></tr>"
         "</tbody></table></div>"
         "<p><strong>實務上兩者合作</strong>:先用符號法看清楚結構"
         "(例如發現答案正比於 $\\sqrt{\\pi}$),再用數值法算出具體數字。"
         "或反過來:先數值算幾個點看趨勢,猜出公式,再用符號法證明。</p>"
         "<p><strong>ML 裡的例子</strong>:損失函數的期望值 "
         "$\\mathbb{E}[L]=\\int L(x)p(x)dx$ 幾乎不可能符號求解"
         "(高維、$p$ 複雜),所以用<strong>取樣</strong>近似——那是蒙地卡羅積分,"
         "本質上就是數值積分的隨機版本。W12 會正式處理。</p>"
         "<p><strong>一句話送給學生</strong>:符號法讓你<strong>理解</strong>,"
         "數值法讓你<strong>交付</strong>。兩者都要會。<span class='qed'>∎</span></p>",
    guide=["符號積分給你公式,數值積分給你數字。哪一種可以拿去對參數微分?",
           "如果你手上只有 1000 個感測器讀數,哪一種能用?",
           "$\\displaystyle\\int_{0}^{1}e^{-x^{2}}dx$ 用哪一種?為什麼?",
           "什麼情況下你會<strong>兩種都用</strong>?"],
    demo="For each task, decide symbolic or numerical: (a) find how "
         "$\\displaystyle\\int_{0}^{a}x^{2}dx$ depends on $a$; "
         "(b) compute $\\displaystyle\\int_{0}^{1}e^{-x^{2}}dx$ to 10 digits; "
         "(c) integrate a table of 500 sensor readings.",
    demo_sol="<p><strong>(a) 符號</strong>。要看「如何依賴 $a$」就需要公式:"
             "$\\displaystyle\\int_{0}^{a}x^{2}dx=\\frac{a^{3}}{3}$。"
             "有了它才能看出是三次成長、才能對 $a$ 微分。數值法只能一個 $a$ 算一次。</p>"
             "<p><strong>(b) 數值</strong>。沒有初等原函數,符號法給不出可用的公式"
             "(只會回傳 $\\operatorname{erf}$,那只是換個名字)。"
             "Simpson 或 <code>quad</code> 直接給 $0.746824132812$。</p>"
             "<p><strong>(c) 數值</strong>。根本沒有函數公式,只有離散點。"
             "用梯形法(資料點等距時最自然)或 <code>numpy.trapezoid</code>。</p>"
             "<p><strong>準則</strong>:問「我接下來要拿這個結果做什麼」。"
             "要做進一步的數學 → 符號;要一個數字 → 數值。</p>",
    demo_hint="問自己:我需要的是公式還是數字?我有沒有函數?",
    misstep="堅持要符號解。很多實務問題根本沒有,硬求會卡住整個專案。",
    level="mid",
    drills=[
        ("You need $\\displaystyle\\int_{0}^{T}e^{-kt}dt$ as a function of $T$ and $k$. Which "
         "approach?",
         "<p>符號:$\\dfrac{1-e^{-kT}}{k}$。因為要保留 $T,k$ 兩個參數,"
         "數值法只能對特定數值求值。</p>"),
        ("You have 500 equally spaced sensor readings and need the total. Which approach, and "
         "which rule?",
         "<p>數值。等距資料用梯形法最自然(<code>numpy.trapezoid</code>);"
         "若點數為奇數也可以用 Simpson。</p>"),
        ("Give an example where you would use numerical results to guess a formula, then prove it "
         "symbolically.",
         "<p>例:數值算出 $\\displaystyle\\int_{0}^{\\infty}e^{-x^{2}}dx\\approx0.8862269$,"
         "認出它等於 $\\dfrac{\\sqrt\\pi}{2}\\approx0.8862269$,再用極座標技巧證明。"
         "(下週會看到這個積分。)</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜手刻三種積分器,量它們的收斂階",
    intro="梯形 $O(h^2)$、Simpson $O(h^4)$——理論說的。這格把三種方法寫出來,"
          "用 log-log 圖<strong>量出斜率</strong>,看理論對不對。",
    code="""def trapezoid(f, a, b, n):
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    for i in range(1, n):
        s += f(a + i*h)
    return h * s

def simpson(f, a, b, n):
    assert n % 2 == 0, "Simpson 需要偶數段"
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i*h)
    return h * s / 3

def gauss2(f, a, b):
    \"\"\"兩點 Gauss-Legendre,先做區間變換\"\"\"
    c, r = (a + b)/2, (b - a)/2
    t = 1/math.sqrt(3)
    return r * (f(c - r*t) + f(c + r*t))

# 測試:∫_0^1 e^x dx = e - 1
f, a, b = math.exp, 0.0, 1.0
exact = math.e - 1

print(f"{'n':>4} {'梯形誤差':>12} {'比值':>7} {'Simpson誤差':>13} {'比值':>7}")
pt = ps = None
ns = [2, 4, 8, 16, 32, 64]
et, es = [], []
for n in ns:
    e1 = abs(trapezoid(f, a, b, n) - exact)
    e2 = abs(simpson(f, a, b, n) - exact)
    et.append(e1); es.append(e2)
    r1 = f"{pt/e1:7.2f}" if pt else "      -"
    r2 = f"{ps/e2:7.2f}" if ps else "      -"
    print(f"{n:4d} {e1:12.4e} {r1} {e2:13.4e} {r2}")
    pt, ps = e1, e2

print(f"\\nGauss 兩點(只用 2 次求值)誤差 = {abs(gauss2(f, a, b) - exact):.4e}")
print(f"對照 梯形 n=2 (3 次求值)   誤差 = {et[0]:.4e}")

hs = np.array([(b - a)/n for n in ns])
plt.loglog(hs, et, 'o-', label='trapezoid')
plt.loglog(hs, es, 's-', label='Simpson')
plt.loglog(hs, hs**2 * et[0]/hs[0]**2, 'k:', label='slope 2 ref')
plt.loglog(hs, hs**4 * es[0]/hs[0]**4, 'k--', label='slope 4 ref')
plt.xlabel('h'); plt.ylabel('|error|'); plt.legend(fontsize=8)
plt.title('Measured convergence orders')
plt.show()

for name, e in [('trapezoid', et), ('Simpson', es)]:
    slope = np.polyfit(np.log10(hs[:4]), np.log10(e[:4]), 1)[0]
    print(f"{name:10s} log-log 斜率 = {slope:.3f}")""",
    expected="trapezoid  log-log 斜率 = 2.000\nSimpson    log-log 斜率 = 3.996",
    seealso="誤差比值:梯形穩定在 $4$、Simpson 穩定在 $16$;log-log 斜率量出 $2.000$ 與 $3.996$——"
            "和理論的 $O(h^2)$、$O(h^4)$ 完全吻合。另外注意 Gauss 只用 <strong>2 次</strong>求值,"
            "誤差就比梯形用 3 次還小。",
    todo="""# TODO 學生練習:把 f 換成 lambda t: 1/(1+t*t),a=0, b=1(精確值 pi/4)
# 這次 Simpson 的誤差比值還是 16 嗎?如果不是,先別看下一個 Lab,自己猜猜為什麼""")

LAB2 = Lab(
    title="Lab 2｜超收斂:理論能不能事先預測",
    intro="觀念 6 說:若 $f'''(b)=f'''(a)$,Simpson 的 $h^4$ 主項會消失、變成 $O(h^6)$。"
          "這格<strong>先預測、再實測</strong>,檢驗理論。",
    code="""x = sp.Symbol('x', real=True)

def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i*h)
    return h * s / 3

cases = [
    ("1/(1+x^2) on [0,1]",  1/(1+x**2),    0, 1),
    ("sin x on [0,pi/2]",   sp.sin(x),     0, sp.pi/2),
    ("exp x on [0,1]",      sp.exp(x),     0, 1),
    ("sin x on [0,2pi]",    sp.sin(x),     0, 2*sp.pi),
]

for name, expr, a, b in cases:
    # --- 先預測 ---
    f3 = sp.diff(expr, x, 3)
    jump = sp.simplify(f3.subs(x, b) - f3.subs(x, a))
    predicted = "O(h^6) 超收斂,比值 ~64" if jump == 0 else "O(h^4) 標準,比值 ~16"
    # --- 再實測 ---
    fn = sp.lambdify(x, expr, 'math')
    av, bv = float(a), float(b)
    exact = float(sp.integrate(expr, (x, a, b)))
    errs = [abs(simpson(fn, av, bv, n) - exact) for n in [8, 16, 32]]
    ratios = [errs[0]/errs[1], errs[1]/errs[2]]
    print(f"{name:22s}  f'''(b)-f'''(a) = {str(jump):>12s}")
    print(f"    預測: {predicted}")
    print(f"    實測比值: {ratios[0]:8.2f}, {ratios[1]:8.2f}\\n")""",
    expected="1/(1+x^2) on [0,1]      f'''(b)-f'''(a) =            0\n    預測: O(h^6) 超收斂,比值 ~64\n    實測比值:    63.90,    63.99",
    seealso="四個案例的<strong>預測全部命中</strong>:$\\frac{1}{1+x^2}$ 與 $\\sin$ 在整週期上 "
            "$f'''$ 的端點差為零 → 比值 $\\approx64$;$\\sin$ 在 $[0,\\frac{\\pi}{2}]$ 與 "
            "$e^x$ 的端點差不為零 → 比值 $\\approx16$。"
            "<strong>誤差公式不只給階數,還能事前預測</strong>。",
    todo="""# TODO 學生練習:找一個你自己的 f 和區間,讓 f'''(b) = f'''(a)
# 提示:任何在 [0, 2*pi] 上的三角函數都符合。先預測,再實測驗證""")

LAB3 = Lab(
    title="Lab 3｜手刻 vs scipy:什麼時候該用現成的",
    intro="觀念 9 說 <code>quad</code> 是自適應的。這格用一個「尖峰」函數,"
          "看等距法和自適應法的差距有多大。",
    code="""from scipy.integrate import quad

def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i*h)
    return h * s / 3

# 一個又窄又高的尖峰:只有 x ~ 0 附近有值
spike = lambda t: math.exp(-1000 * t * t)
exact = math.sqrt(math.pi / 1000)          # ∫_-inf^inf,區間夠寬時近似成立

print("被積函數 exp(-1000 x^2) 在 [-1, 1] 上(尖峰只有 ~0.1 寬)")
print(f"{'方法':>22} {'結果':>16} {'誤差':>12} {'函數求值次數':>14}")
for n in [50, 200, 1000, 5000]:
    v = simpson(spike, -1, 1, n)
    print(f"{'等距 Simpson n=' + str(n):>22} {v:16.10f} {abs(v-exact):12.3e} {n+1:14d}")

v, err = quad(spike, -1, 1)
print(f"{'scipy quad(自適應)':>22} {v:16.10f} {abs(v-exact):12.3e} {'~200':>14}")
print(f"   quad 自己回報的誤差估計 = {err:.2e}")

xs = np.linspace(-1, 1, 1000)
plt.plot(xs, np.exp(-1000*xs**2))
plt.title('exp(-1000 x^2): almost all the area lives near 0')
plt.xlabel('x'); plt.show()

print("\\n→ 等距法把大部分求值浪費在函數幾乎為零的地方;")
print("  自適應法自動把節點集中到尖峰,少算很多還更準。")""",
    expected="scipy quad(自適應)   0.0560499122     ~1e-11           ~200",
    seealso="等距 Simpson 要 $n\\approx5000$ 才追得上 <code>quad</code> 用約 200 次求值的精度。"
            "尖峰越窄,差距越大——這就是自適應的價值。"
            "但注意:<strong>要先看懂 <code>quad</code> 回報的誤差估計</strong>,才知道能不能信。",
    todo="""# TODO 學生練習:把尖峰改成 exp(-100000 * t * t)(更窄)
# 等距 Simpson 需要多大的 n 才追得上 quad?quad 的誤差估計變了嗎?""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="四招學完了,但有些積分<strong>證明</strong>了算不出公式。"
         "這週轉向:不求公式,只求數字——而且要能<strong>保證</strong>那個數字有多準。",
    fastforward=[
        ("黎曼和(左/右/中點)", "銜接課教過", "快轉,但梯形法要接上去"),
        ("四招積分技巧", "W4–W6 剛學完", "快轉,只講「什麼時候會失效」"),
        ("梯形法與其誤差", "偏新", "中速"),
        ("<strong>Simpson 法則</strong>", "<strong>全新</strong>", "踩煞車"),
        ("<strong>Simpson 誤差的泰勒證明</strong>", "全新,本週最硬", "踩煞車(證明時刻)"),
        ("超收斂", "全新,但很有趣", "中速(實作課會驗證)"),
        ("高斯求積", "全新,概念漂亮", "中速,不必背節點"),
        ("給定精度反推 $n$", "工程實用", "務必練"),
        ("scipy.integrate", "全新,實務必備", "輕鬆帶"),
    ],
    outcomes=[
        "說出「沒有初等原函數」是<strong>定理</strong>,並解釋為什麼定積分照樣存在。",
        "手算梯形法與 Simpson 法則(記得 $\\frac12$ 與 $1,4,2,4,1$ 的係數)。",
        "用泰勒展開說明 Simpson 的誤差為何是 $O(h^{4})$,以及三次項為什麼消失。",
        "<strong>事先預測</strong>超收斂:算 $f'''$ 在兩端點的值。",
        "給定容許誤差,反推需要的 $n$(進位、偶數)。",
        "說明 <code>quad</code> 的兩個回傳值,以及什麼時候不能信它。",
    ],
    clock=[
        ("00:00–00:15", "四招回顧;宣告有些積分沒有初等原函數", "觀念 1"),
        ("00:15–00:40", "梯形法:黎曼和的平均 + 誤差 $O(h^{2})$", "觀念 2–3"),
        ("00:40–01:05", "Simpson:用拋物線,以及三次也精確的驚喜", "觀念 4"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:45", "<strong>證明時刻</strong>:Simpson 為何是四階", "觀念 5"),
        ("01:45–02:05", "超收斂:理論能事先預測", "觀念 6"),
        ("02:05–02:10", "休息", "—"),
        ("02:10–02:35", "高斯求積:節點也可以調", "觀念 7"),
        ("02:35–02:50", "給定精度反推 $n$", "觀念 8"),
        ("02:50–03:00", "scipy 與方法論:數值 vs 符號", "觀念 9–10"),
    ],
    proof_moment="用泰勒展開推導 Simpson 的局部誤差 $-\\frac{h^{5}}{90}f^{(4)}$。"
                 "關鍵是<strong>對稱性讓奇次項全部消失</strong>——"
                 "這同時解釋了「為什麼拋物線公式對三次也精確」與「為什麼誤差是四階而非三階」。"
                 "一個推導回答兩個問題,值得慢慢講。",
    script=[
        ("開場:承認有些題目算不出來(15 分)",
         "<p>黑板寫 $\\int e^{-x^{2}}dx$。「四招都試試看。」給三分鐘,讓他們真的卡住。</p>"
         "<p>然後說:「不是你們不會。<strong>Liouville 在 1835 年證明了它沒有初等原函數</strong>。」"
         "這句話要講得慢,學生需要時間接受。</p>"
         "<p>接著轉折:「但 $\\int_{0}^{1}e^{-x^{2}}dx$ 是一個確定的數字,約 $0.7468$。"
         "為什麼?」——回到定積分的定義。<strong>「沒有公式」和「數不存在」是兩回事</strong>。</p>"
         "<p>最後給第三個動機:「而且很多時候你根本沒有函數,只有一串感測器讀數。」"
         "這對資工系學生最有感。</p>"),
        ("梯形法:從黎曼和長出來(25 分)",
         "<p>「銜接課教過左和、右和。如果我把它們<strong>平均</strong>呢?」"
         "當場算,發現頭尾變 $\\frac12$、中間是 $1$——梯形法自己掉出來。</p>"
         "<p>誤差公式直接給,但要<strong>逐項解讀</strong>:$h^{2}$ 代表什麼、$f''$ 代表什麼、"
         "為什麼對直線精確。</p>"
         "<p>然後問:「凹向上時高估還是低估?」讓他們先用圖猜,再用公式的符號驗證。"
         "<strong>圖形直覺和符號結果對得上,才算懂</strong>。</p>"),
        ("Simpson:多一階的威力(25 分)",
         "<p>「直線不夠好,那用<strong>拋物線</strong>?」三點決定一條拋物線 ⟹ 兩段一組 ⟹ "
         "$n$ 必須偶數。</p>"
         "<p>係數 $1,4,2,4,1$ 用「數次數」的方式解釋(和梯形法的 $\\frac12$ 同一個邏輯)。</p>"
         "<p><strong>震撼點</strong>:同樣 $n=4$、同樣五個函數值,梯形誤差 $2.6\\times10^{-3}$、"
         "Simpson $6\\times10^{-6}$——<strong>準 430 倍,計算量一樣</strong>。"
         "當場算給他們看,這比講十遍有效。</p>"
         "<p>留一個懸念:「拋物線是二次的。你猜它對三次多項式準不準?」"
         "讓他們試 $\\int_{0}^{2}(x^{3}-2x+1)dx$——<strong>誤差是零</strong>。"
         "「為什麼?下一段告訴你。」</p>"),
        ("證明時刻:對稱性做掉了兩件事(35 分)",
         "<p>在面板中點展開,兩邊都用泰勒。<strong>關鍵一句話</strong>:"
         "「$\\int_{-h}^{h}u^{k}du$ 在 $k$ 是奇數時等於零。」</p>"
         "<p>真值的展開:奇次消失。Simpson 值的展開:$f_{0}+f_{2}$ 相加時奇次也消失。"
         "<strong>兩邊同時沒有三次項</strong>——所以三次多項式必然精確,懸念解開。</p>"
         "<p>相減,第一個活下來的是 $h^{5}f^{(4)}$。算那個係數 "
         "$\\frac{1}{60}-\\frac{1}{36}=-\\frac{1}{90}$ 時讓學生自己通分,"
         "小地方也要動手。</p>"
         "<p>全域加總得 $O(h^{4})$。「$h$ 減半,誤差變 $\\frac{1}{16}$。實作課去量給我看。」</p>"),
        ("超收斂:理論的真正價值(20 分)",
         "<p>「剛剛說誤差是 $O(h^{4})$,比值應該是 16。但我先給你們看一組數據。」"
         "亮出 $\\frac{1}{1+x^{2}}$ 的比值:$63.9$、$64.0$。「理論錯了嗎?」</p>"
         "<p>賣個關子,然後給更精細的誤差式:主項 $\\propto f'''(b)-f'''(a)$。"
         "當場算 $f'''$,發現兩端都是零。</p>"
         "<p>「所以不是理論錯,是<strong>理論比你以為的更精確</strong>——"
         "它甚至能<strong>事先預測</strong>哪些題目會意外地準。」</p>"
         "<p>這一段是本週的高潮。學生第一次看到「理論預測 → 實驗驗證」的完整循環。</p>"),
        ("高斯:節點也可以調(25 分)",
         "<p>「梯形和 Simpson 都固定節點等距。<strong>為什麼要等距?</strong>」</p>"
         "<p>數自由度:$n$ 個節點 + $n$ 個權重 = $2n$。所以能對 $2n-1$ 次精確。"
         "$n=2$ 就能對三次精確——<strong>只用兩個點</strong>。</p>"
         "<p>推導兩點公式(用對稱性簡化,五分鐘),然後驗證 $x^{3}$ 也對。"
         "節點 $\\pm\\frac{1}{\\sqrt3}$ 看起來奇怪,但<strong>那是算出來的最佳位置</strong>。</p>"
         "<p>不必背節點表,但要知道原理——實務上圖學、有限元素、ML 到處都是它。</p>"),
        ("收尾:工程與方法論(25 分)",
         "<p>反推 $n$ 練一題,強調<strong>進位 + 偶數</strong>。"
         "順便對比:同樣精度梯形要 $n=477$、Simpson 只要 $12$。</p>"
         "<p><code>quad</code> 的兩個回傳值,特別強調第二個。"
         "「工具很強,但你要知道它的假設。」</p>"
         "<p>最後給那張「符號 vs 數值」的表,收在一句話:"
         "<strong>符號法讓你理解,數值法讓你交付</strong>。</p>"
         "<p>預告下週:「還有一種積分,區間是無窮長,或被積函數在端點爆掉。"
         "那種能不能算?什麼時候算得出來?」</p>"),
    ],
    myths=[
        "以為「積不出來」代表「答案不存在」。",
        "梯形法忘記頭尾要乘 $\\frac12$。",
        "Simpson 的 $n$ 取奇數。",
        "以為 Simpson 只對二次精確(其實三次也精確,因為對稱性)。",
        "把誤差公式裡的 $h$ 和 $n$ 搞混。",
        "反推 $n$ 時捨去而不是進位。",
        "以為超收斂是運氣。它可以由 $f'''$ 的端點值<strong>事先預測</strong>。",
        "只看 <code>quad</code> 的第一個回傳值,不看誤差估計。",
    ],
    exit_check=[
        ("用 Simpson 法則估 $\\displaystyle\\int_{0}^{2}x^{3}dx$($n=2$)。誤差是多少?",
         "$h=1$,$\\frac13\\left[0+4(1)+8\\right]=4$。精確值也是 $4$,誤差為 <strong>0</strong>"
         "——Simpson 對三次多項式精確。"),
        ("梯形法的誤差是 $O(h^{2})$、Simpson 是 $O(h^{4})$。$h$ 減半,兩者的誤差各變成幾分之一?",
         "梯形 $\\frac14$、Simpson $\\frac{1}{16}$。"),
        ("什麼情況下 Simpson 的誤差會比 $O(h^{4})$ 更好?怎麼<strong>事先</strong>判斷?",
         "當 $f'''(b)=f'''(a)$ 時,$h^{4}$ 主項消失,變成 $O(h^{6})$。"
         "算兩個端點的三階導數就能事先判斷。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W7-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "觀念 5 的推導要能自己走一遍(至少講得出「奇次項為什麼消失」)。",
        "<strong>複習</strong>:期中考範圍 W1–W8,下週上完就考。"
        "把四招 + 數值方法整理成一張決策圖。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 D1 ∫x e^(-x^2) dx 有初等原函數",
     "simplify(diff(-exp(-x**2)/2, x) - x*exp(-x**2))", "0"),
    ("C1 示範 ∫_0^1 e^(-x^2) 的值",
     "floor(1000*integrate(exp(-x**2), (x, 0, 1)).evalf())", "746"),
    ("C2 示範 T_4 for 1/(1+x^2) = 5323/6800",
     "Rational(1,4)*(Rational(1,2) + Rational(16,17) + Rational(4,5) + Rational(16,25) "
     "+ Rational(1,4))", "Rational(5323,6800)"),
    ("C2 D1 T_2 for x^2 on [0,1] = 0.375", "Rational(1,2)*(0 + Rational(1,4) + Rational(1,2))",
     "Rational(3,8)"),
    ("C3 示範 誤差界 = 實際誤差", "Rational(1,4)**2/12*2", "Rational(1,96)"),
    ("C3 示範 T_4 for x^2 實際誤差",
     "Rational(1,4)*(0 + Rational(1,16) + Rational(1,4) + Rational(9,16) + Rational(1,2)) "
     "- Rational(1,3)", "Rational(1,96)"),
    ("C4 D1 S_2 for x^3-2x+1 on [0,2] 精確",
     "Rational(1,3)*(1 + 0 + 5) - integrate(x**3-2*x+1, (x, 0, 2))", "0"),
    ("C4 D3 S_2 for x^2 on [0,1] 精確",
     "Rational(1,2)/3*(0 + 4*Rational(1,4) + 1) - Rational(1,3)", "0"),
    ("C5 示範 誤差係數 1/60 - 1/36 = -1/90",
     "Rational(1,60) - Rational(1,36)", "Rational(-1,90)"),
    ("C5 D3 S_4 誤差界 for e^x ≈ 5.899e-5",
     "floor(100000000*Rational(1,4)**4/180*E)", "5899"),
    ("C6 示範 f'''(x) for 1/(1+x^2)",
     "simplify(diff(1/(1+x**2), x, 3) - (-24*x*(x**2-1)/(1+x**2)**4))", "0"),
    ("C6 示範 f'''(0) = 0", "diff(1/(1+x**2), x, 3).subs(x, 0)", "0"),
    ("C6 示範 f'''(1) = 0", "simplify(diff(1/(1+x**2), x, 3).subs(x, 1))", "0"),
    ("C6 D1 sin 在 [0,2pi] 的端點差 = 0",
     "simplify(diff(sin(x), x, 3).subs(x, 2*pi) - diff(sin(x), x, 3).subs(x, 0))", "0"),
    ("C6 D2 exp 在 [0,1] 的端點差 = e-1",
     "simplify(diff(exp(x), x, 3).subs(x, 1) - diff(exp(x), x, 3).subs(x, 0))", "E - 1"),
    ("C7 示範 Gauss2 節點滿足 2*x1^2 = 2/3",
     "2*(1/sqrt(3))**2 - Rational(2,3)", "0"),
    ("C7 示範 Gauss2 對 x^3 精確", "(1/sqrt(3))**3 + (-1/sqrt(3))**3", "0"),
    ("C7 示範 ∫_-1^1 x^2 dx = 2/3", "integrate(x**2, (x, -1, 1))", "Rational(2,3)"),
    ("C7 D1 Gauss2 對 x^4 = 2/9(不精確)",
     "2*(1/sqrt(3))**4", "Rational(2,9)"),
    ("C7 D1 ∫_-1^1 x^4 dx = 2/5", "integrate(x**4, (x, -1, 1))", "Rational(2,5)"),
    ("C8 示範 Simpson n=12 的界 < 1e-6",
     "floor((1*Rational(1,12)**4/180*E)*10**6)", "0"),
    ("C8 D3 M_4 for sin = 1", "Abs(diff(sin(x), x, 4).subs(x, pi/2))", "1"),
    ("C10 D1 ∫_0^T e^(-kt) dt",
     "simplify(integrate(exp(-Symbol('k', positive=True)*t), (t, 0, Symbol('T', positive=True))) "
     "- (1-exp(-Symbol('k', positive=True)*Symbol('T', positive=True)))"
     "/Symbol('k', positive=True))", "0"),
    ("C10 D3 ∫_0^oo e^(-x^2) = sqrt(pi)/2",
     "integrate(exp(-x**2), (x, 0, oo))", "sqrt(pi)/2"),
]

WEEK = Week(
    num=7,
    title="積分技巧總整理與數值積分",
    subtitle="四招學完了,但有些積分被<strong>證明</strong>算不出公式。"
             "這週轉向:不求公式、只求數字——而且要能保證那個數字有多準。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["期中考前最後一塊"],
)
