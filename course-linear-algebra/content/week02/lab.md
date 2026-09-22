## ① 預測 · 寫下你的預測
下面的矩陣都是理論課做過的題目。**先不要往下跑**,憑手算的經驗寫下你的預測,寫完才進下一步,讓電腦幫你對答案。

- $A\mathbf{x}$ 的結果是什麼?($A$、$\mathbf{x}$ 是觀念 4 例 1(a),Lay 1.4 Example 1)
- A1、A2、A3 各有幾列有 pivot?$A\mathbf{x} = \mathbf{b}$ 是不是**對每個** $\mathbf{b}$ 都有解?

```python
A = np.array([[1, 2, -1],
              [0, -5, 3]], dtype=float)
x = np.array([4, 3, 7], dtype=float)

A1 = Matrix([[1, 3, 4], [-4, 2, -6], [-3, -2, -7]])      # 觀念 5 例 1(Lay 1.4 Example 3)
A2 = Matrix([[0, 0, 4], [0, -3, -1], [-2, 8, -5]])       # Lay 1.4 Exercise 22
A3 = Matrix([[1, 3, 0, 3], [-1, -1, -1, 1],
             [0, -4, 2, -8], [2, 0, 3, -1]])             # Lay 1.4 Exercise 17
A1, A2, A3
```

```python todo
# TODO 預測:把 None 換成你的答案
# Ax 填一個 list;A1~A3 填 True(每個 b 都有解)或 False
pred = {"Ax": None, "A1": None, "A2": None, "A3": None}
```

## ② 計算 · Ax 的兩種算法,和 A @ x
理論課講了兩種算 $A\mathbf{x}$ 的方法:**定義**(行的線性組合)和**列向量規則**。下面兩個函式是老師寫好的,逐字照著兩種方法寫。讀讀看,再和 NumPy 的 `A @ x` 比較。

**注意 Python 從 0 開始數**:`A[:, j]` 是課本的第 $j+1$ 行,`A[i, j]` 是第 $i+1$ 列、第 $j+1$ 行。

```python
def Ax_by_columns(A, x):
    """老師提供:照定義,Ax = x1·a1 + x2·a2 + … + xn·an(行的線性組合)。"""
    m, n = A.shape
    result = np.zeros(m)
    for j in range(n):
        result = result + x[j] * A[:, j]
    return result

def Ax_by_rows(A, x):
    """老師提供:列向量規則,第 i 個分量 = 第 i 列和 x 對應相乘再相加。"""
    m, n = A.shape
    result = np.zeros(m)
    for i in range(m):
        result[i] = sum(A[i, j] * x[j] for j in range(n))
    return result

print("行的線性組合:", Ax_by_columns(A, x))
print("列向量規則  :", Ax_by_rows(A, x))
print("A @ x       :", A @ x)
print("你的預測    :", pred["Ax"])
```

```text expected
行的線性組合: [3. 6.]
列向量規則  : [3. 6.]
A @ x       : [3. 6.]
```

**會看到**:三種算法都得到 $(3, 6)$,和講義例 1(a) 一樣。`@` 是 Python 的矩陣乘法運算子,以後都用它。

```python todo
# TODO 計算:把 x 換成 [1, 0, 0]、[0, 1, 0]、[0, 0, 1],各算一次 A @ x
# 結果剛好是 A 的哪一部分?為什麼?(提示:定義裡的權重)
```

## ② 計算 · Theorem 4:數 pivot,對答案
Theorem 4 說:「$A\mathbf{x} = \mathbf{b}$ 對每個 $\mathbf{b}$ 都有解」⇔「$A$ 的每一列都有 pivot」。`rref()` 回傳的第二樣東西是 pivot 所在的行,**有幾個 pivot,就有幾列有 pivot**。

```python
for name, M in [("A1", A1), ("A2", A2), ("A3", A3)]:
    R, pivots = M.rref()
    m = M.shape[0]                       # 列數
    ok = len(pivots) == m                # 每一列都有 pivot?
    print(f"{name}: {m} 列,其中 {len(pivots)} 列有 pivot → 每個 b 都有解? {ok}")
    print(f"    你的預測: {pred[name]}")
```

```text expected
A1: 3 列,其中 2 列有 pivot → 每個 b 都有解? False
A2: 3 列,其中 3 列有 pivot → 每個 b 都有解? True
A3: 4 列,其中 3 列有 pivot → 每個 b 都有解? False
```

**會看到**:A1 就是理論課的例 1,少一個 pivot,所以只有平面 $b_1 - \tfrac12 b_2 + b_3 = 0$ 上的 $\mathbf{b}$ 有解。A2 雖然第一行是 $(0, 0, -2)$ 看起來很「空」,3 列還是都有 pivot。A3 是 $4 \times 4$ 的方陣,行不比列少,**還是**不能生成 ℝ⁴——行數夠多不代表一定可以。

```python todo
# TODO 計算:A1 對 b = (1, 0, 0) 無解。用 Matrix.hstack(A1, b).rref() 確認
# 再找一個讓 A1 x = b 有解的 b(提示:b1 − b2/2 + b3 = 0)
```

## ② 計算 · b 在不在 Span 裡?
「$\mathbf{b}$ 在 $\operatorname{Span}\{\mathbf{a}_1, \mathbf{a}_2\}$ 裡嗎」就是「$[\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{b}\,]$ 的最後一行是不是 pivot 行」。`Matrix.hstack` 把幾個向量**直的**並排成矩陣。

```python
a1, a2 = Matrix([1, -2, -5]), Matrix([2, 5, 6])
b = Matrix([7, 4, -3])
R, piv = Matrix.hstack(a1, a2, b).rref()      # 觀念 2 例 2(Lay 1.3 Example 5)
print("Example 5:", R.tolist(), piv)

a1, a2 = Matrix([1, -2, 3]), Matrix([5, -13, -3])
b = Matrix([-3, 8, 1])
R, piv = Matrix.hstack(a1, a2, b).rref()      # 觀念 3 例 2(Lay 1.3 Example 6)
print("Example 6:", R.tolist(), piv)
```

```text expected
Example 5: [[1, 0, 3], [0, 1, 2], [0, 0, 0]] (0, 1)
Example 6: [[1, 0, 0], [0, 1, 0], [0, 0, 1]] (0, 1, 2)
```

**會看到**:Example 5 的 pivot 只在第 0、1 行,最後一行(索引 2)不是 pivot 行 → $\mathbf{b}$ 在 Span 裡,而且 RREF 直接給出權重 $\mathbf{b} = 3\mathbf{a}_1 + 2\mathbf{a}_2$。Example 6 的最後一行是 pivot 行,也就是理論課算到的 $0 = -2$ → $\mathbf{b}$ **不在**平面上。

```python todo
# TODO 計算:Lay 1.3 Practice Problem 2,v1=(1,-1,-2), v2=(5,-4,-7), v3=(-3,1,0)
# y = (-4, 3, h)。分別取 h = 5 和 h = 0,判斷 y 在不在 Span{v1, v2, v3} 裡
```

## ③ 解讀 · 陷阱一:A * x 不是 A @ x
在 NumPy 裡,`*` 是**逐元素**相乘。對一個矩陣和一個向量用 `*`,會發生什麼事?

```python
print("A * x =")
print(A * x)
print("(A * x).sum(axis=1) =", (A * x).sum(axis=1))
print("A @ x               =", A @ x)
```

```text expected
A * x =
[[  4.   6.  -7.]
 [  0. -15.  21.]]
(A * x).sum(axis=1) = [3. 6.]
A @ x               = [3. 6.]
```

**會看到**:`A * x` 沒有報錯,而是得到一個 $2 \times 3$ 的矩陣——NumPy 把 $\mathbf{x}$ 的第 $j$ 個分量乘到 $A$ 的第 $j$ **行**上(這叫 broadcasting)。這三行正是 $4\mathbf{a}_1$、$3\mathbf{a}_2$、$7\mathbf{a}_3$!把每一列加起來(`sum(axis=1)`)才得到 $A\mathbf{x}$。**最危險的是它不會報錯**,程式照跑、答案錯。

```python todo
# TODO 解讀:用「行的線性組合」解釋:為什麼把 A * x 每一列加起來就是 A @ x?
```

## ③ 解讀 · 陷阱二:形狀不合,乘不起來
Lay 1.4 Exercise 1:$3 \times 2$ 的矩陣乘上 3 個分量的向量。理論課說這「沒有定義」,電腦怎麼說?

```python
A_bad = np.array([[-4, 2], [1, 6], [0, 1]], dtype=float)
x_bad = np.array([3, 1, 7], dtype=float)
try:
    A_bad @ x_bad
except ValueError as e:
    print(f"ValueError:A 的形狀是 {A_bad.shape},x 的形狀是 {x_bad.shape}")
```

```text expected
ValueError:A 的形狀是 (3, 2),x 的形狀是 (3,)
```

**會看到**:NumPy 報 `ValueError`。`A_bad.shape` 是 `(3, 2)`:第二個數字(**行數** 2)要和 $\mathbf{x}$ 的分量數相等,這裡是 3,對不上。以後看到 shape 相關的錯誤,第一件事就是把兩邊的 `.shape` 印出來比。

```python todo
# TODO 解讀:A_bad 要乘上幾個分量的向量才有定義?自己造一個向量 x_ok,
# 算出 A_bad @ x_ok,結果有幾個分量?和 A_bad 的哪個數字一樣?
```

## ③ 解讀 · 陷阱三:迴圈 vs @,差多少?
老師寫的 `Ax_by_rows` 用 Python 迴圈一格一格算,邏輯完全正確。但實務上沒人這樣寫——量量看就知道為什麼。

```python
import time

rng = np.random.default_rng(0)
n = 300
A_big = rng.standard_normal((n, n))
x_big = rng.standard_normal(n)

t0 = time.perf_counter(); y_loop = Ax_by_rows(A_big, x_big); t_loop = time.perf_counter() - t0
t0 = time.perf_counter(); y_fast = A_big @ x_big;             t_fast = time.perf_counter() - t0

print(f"Python 迴圈:{t_loop * 1000:8.2f} ms")
print(f"A @ x     :{t_fast * 1000:8.3f} ms   快了約 {t_loop / t_fast:,.0f} 倍")
print("答案一樣嗎?", np.allclose(y_loop, y_fast))
```

**會看到**:每台電腦的秒數不同,但 `@` 通常快上**一百倍以上**,$n$ 越大差距越大,答案一樣(用 `allclose` 比,原因見第 1 週的浮點數陷阱)。`@` 背後是用 C/Fortran 寫、針對 CPU 最佳化的函式庫(BLAS)。**理解用自己寫的版本,實際計算用 `@`**。

```python todo
# TODO 解讀:把 n 改成 600,兩者的時間各變成大約幾倍?
# 提示:n×n 矩陣乘向量要做約 n² 次乘法
```

## ③ 解讀 · 陷阱四:記憶體怎麼存,影響速度
觀念 4 的數值筆記說:C 語言(和 NumPy 預設)把矩陣**一列一列**存,Fortran 一行一行存。沿著記憶體**連續**讀比跳著讀快,因為 CPU 會把相鄰的資料一起搬進快取(cache)。

```python
n = 3000
M = rng.standard_normal((n, n))           # NumPy 預設:一列一列存(C order)
print("一列一列存?", M.flags["C_CONTIGUOUS"])

t0 = time.perf_counter()
for i in range(n):
    M[i, :].sum()                         # 取第 i 列:在記憶體中是連續的
t_row = time.perf_counter() - t0

t0 = time.perf_counter()
for j in range(n):
    M[:, j].sum()                         # 取第 j 行:每個數字相隔 n 格
t_col = time.perf_counter() - t0

print(f"逐列讀:{t_row * 1000:7.1f} ms")
print(f"逐行讀:{t_col * 1000:7.1f} ms   慢了約 {t_col / t_row:.1f} 倍")
```

**會看到**:讀的數字一模一樣多,逐行讀卻比較慢(通常 2–10 倍,看電腦)。這就是課本數值筆記的意思:演算法的運算順序要配合資料的存法。

```python todo
# TODO 解讀:把 M 換成 np.asfortranarray(M)(改成一行一行存)再跑一次
# 哪一種讀法變快了?用一句話說明原因
```

## ④ 應用 · 畫出 Span:直線還是平面?
隨機取很多組權重 $c_1, c_2$,把 $c_1\mathbf{v}_1 + c_2\mathbf{v}_2$ 全部畫出來,就能「看到」Span。左圖是觀念 2 例 1 的 $\mathbf{v}_1 = (-1, 1)$、$\mathbf{v}_2 = (2, 1)$;右圖把 $\mathbf{v}_2$ 換成 $\mathbf{v}_1$ 的倍數。

```python
def span_points(v1, v2, k=2000, scale=3):
    """隨機取 k 組權重 c1, c2 ∈ [−scale, scale],回傳 c1·v1 + c2·v2(每一列一個點)。"""
    C = rng.uniform(-scale, scale, size=(k, 2))
    return C @ np.vstack([v1, v2])        # 第 i 列 = C[i,0]·v1 + C[i,1]·v2

v1 = np.array([-1, 1])
fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
for ax, v2, title in [(axes[0], np.array([2, 1]), "v2 = (2, 1): fills the plane"),
                      (axes[1], np.array([2, -2]), "v2 = (2, -2) = -2 v1: a line")]:
    P = span_points(v1, v2)
    ax.scatter(P[:, 0], P[:, 1], s=2, alpha=0.4)
    for v, c in [(v1, "C1"), (v2, "C3")]:
        ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=c, lw=2))
    ax.set_xlim(-8, 8); ax.set_ylim(-8, 8); ax.set_aspect("equal"); ax.grid(alpha=0.3)
    ax.set_title(title)
plt.show()
```

**會看到**:左圖的點鋪滿一整片(權重範圍再大就能鋪滿整個平面);右圖的點全部擠在一條通過原點的直線上——$\mathbf{v}_2$ 沒有帶來新方向。

接著看 ℝ³:兩個不平行的向量張成一個**平面**(觀念 3 的圖)。

```python todo
# TODO 應用:u = (1, 0, 1)、v = (0, 1, 1),用 span_points 產生點,
# 以 fig.add_subplot(projection="3d") 畫出來,轉一轉看它是不是一個通過原點的平面
```

## ④ 應用 · 課本電腦題:Lay 1.4 Exercises 47–52
**Lay 1.4 Exercises 47–50**(課本標 **T**):判斷矩陣的行能不能生成 ℝ⁴。手算 $4 \times 5$ 的矩陣很累,交給 `rref()`,再用 Theorem 4 判斷。

**Exercise 51**:Exercise 49 的矩陣可以刪掉哪一行,剩下的行**還能**生成 ℝ⁴?程式把每一行都刪刪看。

```python
mats = {
    47: [[7, 2, -5, 8], [-5, -3, 4, -9], [6, 10, -2, 7], [-7, 9, 2, 15]],
    48: [[5, -7, -4, 9], [6, -8, -7, 5], [4, -4, -9, -9], [-9, 11, 16, 7]],
    49: [[12, -7, 11, -9, 5], [-9, 4, -8, 7, -3], [-6, 11, -7, 3, -9], [4, -6, 10, -5, 12]],
    50: [[8, 11, -6, -7, 13], [-7, -8, 5, 6, -9], [11, 7, -7, -9, -6], [-3, 4, 1, 8, 7]],
}
for k, M in mats.items():
    R, pivots = Matrix(M).rref()
    print(f"Exercise {k}:pivot 在第 {[p + 1 for p in pivots]} 行 → 行向量生成 R^4? {len(pivots) == 4}")

M49 = Matrix(mats[49])
for j in range(5):
    rest = M49[:, [c for c in range(5) if c != j]]     # 刪掉第 j+1 行
    print(f"  刪掉第 {j + 1} 行後 pivot 個數 = {len(rest.rref()[1])}")
```

```text expected
Exercise 47:pivot 在第 [1, 2, 3] 行 → 行向量生成 R^4? False
Exercise 48:pivot 在第 [1, 2, 3] 行 → 行向量生成 R^4? False
Exercise 49:pivot 在第 [1, 2, 3, 5] 行 → 行向量生成 R^4? True
Exercise 50:pivot 在第 [1, 2, 4, 5] 行 → 行向量生成 R^4? True
  刪掉第 1 行後 pivot 個數 = 4
  刪掉第 2 行後 pivot 個數 = 4
  刪掉第 3 行後 pivot 個數 = 4
  刪掉第 4 行後 pivot 個數 = 4
  刪掉第 5 行後 pivot 個數 = 3
```

**會看到**:47、48 都只有 3 個 pivot,不能生成 ℝ⁴;49、50 可以。Exercise 51 的答案比書後解答更完整:刪掉第 1–4 行的任何一行都可以,**只有第 5 行不能刪**。為什麼第 5 行特別?第 3 週的「線性相依」會解釋。

```python todo
# TODO 應用:Exercise 52。對 Exercise 50 的矩陣做同樣的「刪一行」檢查
# 哪幾行可以刪?能不能一次刪掉兩行?(用 Theorem 4 說明)
```

## ④ 應用 · 課本電腦題:Lay 1.3 Exercises 35–36
**Lay 1.3 Exercise 35(c)**(課本標 **T**):礦場 1 每天產出 20 公噸銅、550 公斤銀;礦場 2 每天產出 30 公噸銅、500 公斤銀。要產出 150 公噸銅和 2825 公斤銀,兩座礦場各要運作幾天?向量方程式是 $x_1\mathbf{v}_1 + x_2\mathbf{v}_2 = \mathbf{b}$,排成增廣矩陣化簡。

```python
v1 = Matrix([20, 550])        # 礦場 1 每日產量(銅 公噸, 銀 公斤)
v2 = Matrix([30, 500])        # 礦場 2 每日產量
b = Matrix([150, 2825])
print("Exercise 35(c):", Matrix.hstack(v1, v2, b).rref()[0].tolist())
```

```text expected
Exercise 35(c): [[1, 0, 3/2], [0, 1, 4]]
```

**會看到**:$x_1 = \tfrac32$、$x_2 = 4$,礦場 1 運作 1.5 天、礦場 2 運作 4 天。SymPy 用分數精確計算,所以印出 `3/2`。

```python todo
# TODO 應用:Exercise 36(c),電廠燒了 x1 噸 A 煤、x2 噸 B 煤,產出
# (熱量, SO2, 微粒) = (162, 23610, 1623)。用 sp.Rational("27.6") 輸入小數,解出 x1, x2
```

## 驗算
```check
Matrix([[1, 2, -1], [0, -5, 3]]) * Matrix([4, 3, 7]) == Matrix([3, 6])
Matrix([[1, 3, 4, 1], [-4, 2, -6, 0], [-3, -2, -7, 0]]).rref()[1] == (0, 1, 3)
Matrix([[1, 3, 4, 2], [-4, 2, -6, 4], [-3, -2, -7, 0]]).rref()[1] == (0, 1)
Matrix([[1, 5, -3, -4], [-1, -4, 1, 3], [-2, -7, 0, h]]).subs(h, 5).rref()[1] == (0, 1)
3 in Matrix([[1, 5, -3, -4], [-1, -4, 1, 3], [-2, -7, 0, h]]).subs(h, 0).rref()[1]
Matrix([[-4, 2], [1, 6], [0, 1]]) * Matrix([1, 1]) == Matrix([-2, 7, 1])
max([Matrix([[8, 11, -6, -7, 13], [-7, -8, 5, 6, -9], [11, 7, -7, -9, -6], [-3, 4, 1, 8, 7]])[:, [c for c in range(5) if c not in (i, j)]].rank() for i in range(5) for j in range(i + 1, 5)]) < 4
Matrix([[Rational("27.6"), Rational("30.2"), 162], [3100, 6400, 23610], [250, 360, 1623]]).rref()[0][:2, 2] == Matrix([Rational(39, 10), Rational(9, 5)])
```
