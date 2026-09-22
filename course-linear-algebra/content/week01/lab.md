## ① 預測 · 寫下你的預測
下面三個增廣矩陣都是理論課做過的題目。**先不要往下跑**,憑手算的經驗寫下:pivot 在哪幾行?解是哪一種情況?寫完才進下一步,讓電腦幫你對答案。

```python
M1 = Matrix([[1, -2, 1, 0],
             [0, 2, -8, 8],
             [5, 0, -5, 10]])    # 觀念 2 例 2(Lay 1.1 Example 1)
M2 = Matrix([[1, 0, -5, 1],
             [0, 1, 1, 4],
             [0, 0, 0, 0]])      # 觀念 5 例 1(Lay 1.2 p. 42)
M3 = Matrix([[0, 1, -4, 8],
             [2, -3, 2, 1],
             [4, -8, 12, 1]])    # 觀念 3 例 2(Lay 1.1 Example 3)
M1, M2, M3
```

```python todo
# TODO 預測:把 None 換成你的答案
# pivot_cols:行號從 1 開始數(和課本一樣);kind:填 "none"、"unique" 或 "infinite"
pred = {
    "M1": {"pivot_cols": None, "kind": None},
    "M2": {"pivot_cols": None, "kind": None},
    "M3": {"pivot_cols": None, "kind": None},
}
```

## ② 計算 · NumPy 暖身:矩陣就是二維陣列
在 NumPy 裡,矩陣就是一個二維陣列。先熟悉三件事:看形狀、取一列、取一行,然後做一次和理論課一模一樣的列運算。

**注意 Python 從 0 開始數**:課本的第 1 列是 `A[0]`,第 3 行是 `A[:, 2]`。`A.shape` 回傳 `(列數, 行數)`,和課本的 $m \times n$ 一樣是列數在前。

```python
A = np.array([[1, -2, 1, 0],
              [0, 2, -8, 8],
              [5, 0, -5, 10]], dtype=float)
print("形狀 (列數, 行數):", A.shape)
print("第 1 列 A[0]   :", A[0])
print("第 3 行 A[:, 2]:", A[:, 2])

B = A.copy()               # 先複製,不要改到原本的 A
B[2] = B[2] - 5 * B[0]     # R3 ← R3 + (−5)R1(觀念 2 例 2 的第一步)
print(B)
```

```text expected
形狀 (列數, 行數): (3, 4)
第 1 列 A[0]   : [ 1. -2.  1.  0.]
第 3 行 A[:, 2]: [ 1. -8. -5.]
[[  1.  -2.   1.   0.]
 [  0.   2.  -8.   8.]
 [  0.  10. -10.  10.]]
```

**會看到**:第 3 列變成 $[\,0 \;\; 10 \;\; {-10} \mid 10\,]$,和講義例 2 第一步完全一樣。程式碼 `B[2] = B[2] - 5 * B[0]` 就是 $R_3 \leftarrow R_3 + (-5)R_1$ 的逐字翻譯。

```python todo
# TODO 計算:接著做例 2 的第二步 R2 ← (1/2)R2,印出 B,和講義對照
# B[1] = ...
```

## ② 計算 · rref():電腦幫你化簡,對照你的預測
SymPy 的 `rref()` 回傳兩樣東西:RREF 矩陣,以及 pivot 所在的行(**從 0 開始數**)。

下面的 `kind_of` 是老師寫好的小函式,照觀念 5 的流程圖(也就是 Theorem 2)判斷解的情況。讀讀看——它就是流程圖那兩個問題。

```python
def kind_of(pivots, n_cols):
    """老師提供:照觀念 5 的流程圖判斷解的情況。n_cols 是增廣矩陣的行數。"""
    last = n_cols - 1                      # 常數那一行的索引
    if last in pivots:                     # 問題 1:最後一行是 pivot 行嗎?
        return "none"
    n_vars = n_cols - 1
    return "unique" if len(pivots) == n_vars else "infinite"   # 問題 2:有沒有自由變數?

for name, M in [("M1", M1), ("M2", M2), ("M3", M3)]:
    R, pivots = M.rref()
    cols = [p + 1 for p in pivots]         # 換成課本的數法(從 1 開始)
    print(f"{name}: pivot 行 = {cols}, 情況 = {kind_of(pivots, M.shape[1])}")
    print(f"    你的預測: pivot 行 = {pred[name]['pivot_cols']}, 情況 = {pred[name]['kind']}")
```

```text expected
M1: pivot 行 = [1, 2, 3], 情況 = unique
M2: pivot 行 = [1, 2], 情況 = infinite
M3: pivot 行 = [1, 2, 4], 情況 = none
```

**會看到**:M3 的 pivot 行包含第 4 行,也就是常數那一行,所以**無解**——和理論課讀出 $0 = 15$ 是同一件事。M2 只有兩個 pivot、三個未知數,$x_3$ 自由,所以無限多解。

## ② 計算 · np.linalg.solve:唯一解時直接解
確定 M1 是唯一解之後,就可以用 `np.linalg.solve(係數, 常數)` 直接求解。

```python
coef = A[:, :3]     # 前 3 行:係數矩陣
rhs = A[:, 3]       # 最後 1 行:常數
x = np.linalg.solve(coef, rhs)
print("x =", x)
print("代回檢查:", np.allclose(coef @ x, rhs))   # @ 是矩陣乘向量,下週正式學
```

```text expected
x = [ 1.  0. -1.]
代回檢查: True
```

**會看到**:$(1, 0, -1)$,和講義例 2 手算的答案一樣。「代回檢查」就是課本的 Reasonable Answers,只是交給電腦做。

## ③ 解讀 · 陷阱一:solve 報錯,不是程式壞掉
M2 有無限多解。把它丟給 `np.linalg.solve`,會發生什麼事?

```python
coef2 = np.array(M2[:, :3], dtype=float)
rhs2 = np.array(M2[:, 3], dtype=float).ravel()
try:
    np.linalg.solve(coef2, rhs2)
except np.linalg.LinAlgError as e:
    print("LinAlgError:", e)
```

```text expected
LinAlgError: Singular matrix
```

**會看到**:`Singular matrix`。先別急著上網查怎麼「修好」它——想想看 M2 是三種情況中的哪一種。

```python todo
# TODO 解讀:用一句話說明為什麼 solve 對 M2 會報錯
# 提示:solve 只處理三種情況中的哪一種?
why_error = ""
```

## ③ 解讀 · 陷阱二:印出來是 1,其實不是 1
電腦用浮點數計算(觀念 2 的數值筆記),結果常常差一點點,而且**印出來看不出來**。

```python
C = np.array([[0.1, 0.2],
              [0.3, 0.4]])
d = np.array([0.5, 1.1])        # 真正的解是 (1, 2)
x = np.linalg.solve(C, d)
print("x =", x)
print(f"x[0] 的完整數字: {x[0]:.20f}")
print("用 == 比對 [1, 2]:", np.array_equal(x, [1, 2]))
print("用 allclose 比對 :", np.allclose(x, [1, 2]))
```

```text expected
x = [1. 2.]
x[0] 的完整數字: 1.00000000000000133227
用 == 比對 [1, 2]: False
用 allclose 比對 : True
```

**會看到**:印出來是漂亮的 `[1. 2.]`,但 `x[0]` 其實是 $1.0000000000000013$。**結論:比較浮點數的答案不要用 `==`,要用 `np.allclose`**。這和微積分課第 1 週講的浮點數是同一件事。

## ③ 解讀 · 陷阱三:小 pivot 會放大誤差
觀念 4 的數值筆記說:電腦選 pivot 時會挑該行**絕對值最大**的數(partial pivoting)。為什麼?

下面兩個函式是老師寫好的,解同一個方程組 $\varepsilon x_1 + x_2 = 1,\;\; x_1 + x_2 = 2$(當 $\varepsilon$ 很小時,真正的解非常接近 $(1, 1)$)。一個直接拿很小的 $\varepsilon$ 當 pivot,一個先換列、拿 1 當 pivot。

```python
def solve_no_swap(eps):
    """老師提供:直接拿左上角的 eps 當 pivot(不換列)。"""
    m = 1 / eps                           # R2 ← R2 − (1/eps)·R1
    x2 = (2 - m) / (1 - m)
    x1 = (1 - x2) / eps
    return x1, x2

def solve_swap(eps):
    """老師提供:先換列,拿 1 當 pivot(partial pivoting)。"""
    m = eps                               # 換列後:R2 ← R2 − eps·R1
    x2 = (1 - 2 * m) / (1 - m)
    x1 = 2 - x2
    return x1, x2

for eps in [1e-3, 1e-8, 1e-12, 1e-17]:
    print(f"eps={eps:.0e}  不換列 x1 = {solve_no_swap(eps)[0]:.12f}   換列 x1 = {solve_swap(eps)[0]:.12f}")

print("np.linalg.solve:", np.linalg.solve([[1e-17, 1], [1, 1]], [1, 2]))
```

```text expected
eps=1e-03  不換列 x1 = 1.001001001001   換列 x1 = 1.001001001001
eps=1e-08  不換列 x1 = 1.000000005025   換列 x1 = 1.000000010000
eps=1e-12  不換列 x1 = 0.999977878280   換列 x1 = 1.000000000001
eps=1e-17  不換列 x1 = 0.000000000000   換列 x1 = 1.000000000000
np.linalg.solve: [1. 1.]
```

**會看到**:$\varepsilon$ 越小,不換列的答案越離譜,到 $10^{-17}$ 時算出 $x_1 = 0$,而真正的答案約是 1。先換列的版本一直都對;`np.linalg.solve` 內建就會換列,所以也對。

```python todo
# TODO 解讀:把 eps 換成 1e-15、1e-16 再跑一次,不換列的 x1 錯了多少?
# 再用一句話說明:為什麼「拿很小的數當 pivot」會出事
```

## ③ 解讀 · 陷阱四:n 變 2 倍,時間變幾倍?
觀念 5 的數值筆記說:化成梯形大約要 $\tfrac{2n^3}{3}$ 個 flop(Lay 1.2 Exercise 44)。$n$ 變成 2 倍,計算量變成約 $2^3 = 8$ 倍。實際量量看。

```python
import time

rng = np.random.default_rng(0)
prev = None
for n in [500, 1000, 2000]:
    A_big = rng.standard_normal((n, n))
    b_big = np.ones(n)
    t0 = time.perf_counter()
    np.linalg.solve(A_big, b_big)
    dt = time.perf_counter() - t0
    ratio = "" if prev is None else f"   是上一個的 {dt / prev:.1f} 倍"
    print(f"n = {n:5d}:{dt * 1000:8.1f} ms{ratio}")
    prev = dt
```

**會看到**:每台電腦的秒數不同,但 $n$ 加倍時,時間大約變成 5–8 倍。$n$ 很小時比例不準,因為呼叫函式本身的固定開銷佔了大部分時間;$n$ 越大,越接近理論上的 8 倍。

```python todo
# TODO 解讀:照你電腦上的倍數,估計 n = 8000 大約要多久?再用一句話說明你是怎麼估的
```

## ④ 應用 · 內插多項式:讓曲線穿過指定的點
動畫和遊戲常常要一條平滑的曲線穿過設計師指定的幾個點(關鍵影格)。這就是 **Lay 1.2 Exercise 45**:找 $p(t) = a_0 + a_1t + a_2t^2$ 穿過 $(1, 11)$、$(2, 16)$、$(3, 19)$。每個點代進去就是一條方程式,**未知數是係數** $a_0, a_1, a_2$。

```python
pts = [(1, 11), (2, 16), (3, 19)]
# 每個點 (t, y) 給一條方程式:a0 + a1·t + a2·t² = y
aug = Matrix([[1, pt, pt**2, py] for pt, py in pts])
print(aug.rref())                          # 先確認是唯一解

V = np.array([[1, pt, pt**2] for pt, py in pts], dtype=float)
yv = np.array([py for pt, py in pts], dtype=float)
a = np.linalg.solve(V, yv)
print("a0, a1, a2 =", a)

ts = np.linspace(0.5, 3.5, 200)
plt.plot(ts, a[0] + a[1] * ts + a[2] * ts**2, label="p(t)")
plt.plot([p[0] for p in pts], [p[1] for p in pts], "o", ms=9, label="data")
plt.xlabel("t"); plt.ylabel("y"); plt.legend(); plt.title("Interpolating polynomial through 3 points")
plt.show()
```

```text expected
(Matrix([
[1, 0, 0, 4],
[0, 1, 0, 8],
[0, 0, 1, -1]]), (0, 1, 2))
a0, a1, a2 = [ 4.  8. -1.]
```

**會看到**:$p(t) = 4 + 8t - t^2$,和課本書後解答一樣,曲線剛好穿過三個點。三個點、三個未知數,剛好唯一解。

```python todo
# TODO 應用:加上第 4 個點 (4, 15),一樣找二次多項式
# 4 條方程式、3 個未知數——用 rref() 判斷是哪一種情況,並說明在圖上代表什麼
# pts4 = [(1, 11), (2, 16), (3, 19), (4, 15)]
```

## ④ 應用 · 風洞資料:課本的電腦題
**Lay 1.2 Exercise 46**(課本標 **T**,設計給電腦做):風洞實驗量到拋射物在不同速度下的空氣阻力,單位是 100 ft/sec 與 100 lb。找一個內插多項式,估計速度 750 ft/sec(也就是 $v = 7.5$)時的阻力。六個資料點,用 5 次多項式 $p(v) = a_0 + a_1v + \cdots + a_5v^5$。

`np.vander(v, increasing=True)` 會一次做出每一列都是 $1, v, v^2, \dots$ 的係數矩陣。

```python
v = np.array([0, 2, 4, 6, 8, 10], dtype=float)           # 速度(100 ft/sec)
F = np.array([0, 2.90, 14.8, 39.6, 74.3, 119], dtype=float)  # 阻力(100 lb)

V = np.vander(v, increasing=True)          # 6×6,第 i 列是 1, v_i, v_i², …, v_i⁵
a = np.linalg.solve(V, F)
print("係數 a0..a5 =", np.round(a, 5))

p = lambda t: sum(a[i] * t**i for i in range(6))
print(f"p(7.5) = {p(7.5):.2f}  (約 {p(7.5) * 100:.0f} lb)")

ts = np.linspace(0, 10, 200)
plt.plot(ts, p(ts), label="degree-5 interpolant")
plt.plot(v, F, "o", label="wind tunnel data")
plt.plot(7.5, p(7.5), "s", label="estimate at v = 7.5")
plt.xlabel("velocity (100 ft/sec)"); plt.ylabel("force (100 lb)"); plt.legend()
plt.title("Lay 1.2 Exercise 46"); plt.show()
```

```text expected
係數 a0..a5 = [ 0.       1.7125  -1.19479  0.66146 -0.07005  0.0026 ]
p(7.5) = 64.84  (約 6484 lb)
```

**會看到**:在 750 ft/sec 時,阻力大約 6484 磅。題目最後問:「改用次數低於 5 的多項式(例如三次)會怎樣?」——六條方程式、只有四個未知數,通常**無解**。

```python todo
# TODO 應用:改用三次多項式(np.vander(v, 4, increasing=True)),用 rref() 看看發生什麼事
# 最後一行是不是 pivot 行?這代表什麼?(第 14 週的「最小平方法」就是在處理這種情況)
```

## 驗算
```check
Matrix([[1, 1, 1, 11], [1, 2, 4, 16], [1, 3, 9, 19]]).rref()[0][:, 3] == Matrix([4, 8, -1])
3 in Matrix([[1, 1, 1, 11], [1, 2, 4, 16], [1, 3, 9, 19], [1, 4, 16, 15]]).rref()[1]
Matrix([[0, 1, -4, 8], [2, -3, 2, 1], [4, -8, 12, 1]]).rref()[1] == (0, 1, 3)
4 in Matrix([[1, v, v**2, v**3, f] for v, f in [(0, 0), (2, Rational(29, 10)), (4, Rational(148, 10)), (6, Rational(396, 10)), (8, Rational(743, 10)), (10, 119)]]).rref()[1]
```
