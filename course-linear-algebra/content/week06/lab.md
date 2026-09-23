## ① 預測 · 先寫下你的預測
這週的實作有三個主題:用程式驗證可逆矩陣定理、看條件數如何毀掉答案、以及 LU 分解的實際用法。

**先不要往下跑。** 憑理論課學到的東西寫下四個預測:

1. 一個 $4 \times 4$ 矩陣的 $\det = 1$。它可逆嗎?它「好算」嗎?
2. 一個 $3 \times 2$ 矩陣的兩行線性獨立。它的行張成 $\mathbb{R}^3$ 嗎?
3. 用浮點數解 5 階 Hilbert 矩陣的方程組,答案大約有幾位可信?
4. `scipy.linalg.lu(A)` 回傳三個矩陣 `P, L, U`。那個 `P` 會是單位矩陣嗎?

```python todo
# TODO 預測:四個答案先寫在這裡,跑完再回來對照
pred = {
    "det1_invertible": None,   # True / False
    "det1_wellcond": None,     # True / False
    "cols_span_R3": None,      # True / False
    "hilbert_digits": None,    # 猜一個數字,例如 16
    "P_is_identity": None,     # True / False
}
```

## ② 計算 · 用程式驗證可逆矩陣定理
可逆矩陣定理說十二條同真同假。這一格用三種不同的方式問同一個問題(秩、行列式、最簡列梯形),看它們是不是真的一致;再用一個非方陣的例子說明「為什麼只對方陣」。

```python
import scipy.linalg as sla
from sympy import Rational

# ---- Lay 2.3 Exercises 9–10(T 題):三種判斷方式必須一致 ----
mats = {
    9: Matrix([[4, 0, -7, -7], [-6, 1, 11, 9], [7, -5, 10, 19], [-1, 2, 3, -1]]),
    10: Matrix([[5, 3, 1, 7, 9], [6, 4, 2, 8, -8], [7, 5, 3, 10, 9],
                [9, 6, 4, -9, -5], [8, 5, 2, 11, 4]]),
}
for k, M in mats.items():
    n = M.shape[0]
    print(f"Exercise {k}: {n}×{n}  rank = {M.rank()}  det = {M.det()}  "
          f"rref 是 I 嗎? {M.rref()[0] == sp.eye(n)}  可逆? {M.rank() == n}")

# ---- 課本 2.3 Example 1 的矩陣:一次檢查六條 ----
A = Matrix([[1, 0, -2], [3, 1, -2], [-5, -1, 9]])
n = 3
checks = {
    "(b) 與 I 列等價": A.rref()[0] == sp.eye(n),
    "(c) n 個樞軸": len(A.rref()[1]) == n,
    "(d) Ax=0 只有零解": A.nullspace() == [],
    "(e) 各行線性獨立": A.rank() == n,
    "(h) 各行張成 R^n": A.rank() == n,
    "(l) A 轉置可逆": A.T.rank() == n,
}
for name, ok in checks.items():
    print(f"  {name}: {ok}")

# ---- 非方陣:獨立與張成不再是同一件事 ----
B = Matrix([[1, 0], [0, 1], [0, 0]])
print("3×2 矩陣,各行獨立嗎?", B.rank() == B.cols)
print("            張成 R³ 嗎?", B.rank() == B.rows)
print("→ 非方陣時,獨立與張成是兩件事;IMT 不適用")
```

```text expected
Exercise 9: 4×4  rank = 4  det = 1  rref 是 I 嗎? True  可逆? True
Exercise 10: 5×5  rank = 5  det = 2  rref 是 I 嗎? True  可逆? True
  (b) 與 I 列等價: True
  (c) n 個樞軸: True
  (d) Ax=0 只有零解: True
  (e) 各行線性獨立: True
  (h) 各行張成 R^n: True
  (l) A 轉置可逆: True
3×2 矩陣,各行獨立嗎? True
            張成 R³ 嗎? False
→ 非方陣時,獨立與張成是兩件事;IMT 不適用
```

**會看到**:

- 兩個 T 題的矩陣都可逆,而且**三種判斷方式給出一致的答案**——這正是可逆矩陣定理保證的事。
- 六條條件同時成立。若手動把 $A$ 的某一行改成另一行的倍數,再跑一次,你會看到**六條同時變成 False**。
- $3 \times 2$ 的例子:各行獨立(True)但不張成 $\mathbb{R}^3$(False)。**非方陣時這兩件事可以分開**,所以 IMT 不適用。

## ③ 解讀 · 條件數:可逆不代表算得準
這一格是本週最重要的實驗。同一個「可逆」的矩陣,答案可以完全不能用。

```python
# ---- Lay 2.3 Exercise 49:右端動 0.05%,解動 300% ----
Ae = Matrix([[Rational(9, 2), Rational(31, 10)], [Rational(8, 5), Rational(11, 10)]])
b1 = Matrix([Rational(19249, 1000), Rational(6843, 1000)])     # 原始資料
b2 = Matrix([Rational(1925, 100), Rational(684, 100)])          # 四捨五入到小數兩位
x1, x2 = Ae.solve(b1), Ae.solve(b2)
print("det =", Ae.det())
print("精確解(原始資料)  :", [float(v) for v in x1])
print("精確解(四捨五入後):", [float(v) for v in x2])
print(f"x1 的相對誤差 = {float(abs(x2[0]-x1[0])/x1[0])*100:.0f}%")
print(f"x2 的相對誤差 = {float(abs(x2[1]-x1[1])/x1[1])*100:.0f}%")

# ---- Lay 2.3 Exercises 50–51:條件數與損失的位數 ----
for k, M in mats.items():
    Mf = Matrix(M.rows, M.cols, lambda i, j: float(M[i, j]))
    c = float(Mf.condition_number())
    print(f"Exercise {k}: det = {M.det()}  cond ≈ {c:.0f}  → 約損失 {np.log10(c):.1f} 位")

# 先造一個已知答案,再解回來,看掉了幾位
rng = np.random.default_rng(6)
An = np.array(mats[9].tolist(), dtype=float)
xtrue = rng.random(4)
xnum = np.linalg.solve(An, An @ xtrue)
agree = -np.log10(np.max(np.abs(xnum - xtrue)) / np.max(np.abs(xtrue)))
print(f"原本的 x 與解回來的 x 大約吻合到第 {agree:.0f} 位")

# ---- Lay 2.3 Exercise 52:5 階 Hilbert 矩陣 ----
H = Matrix(5, 5, lambda i, j: Rational(1, i + j + 1))
print("精確解(Rational):", list(H.solve(Matrix([0, 0, 0, 0, 1]))))
Hf = np.array([[1 / (i + j + 1) for j in range(5)] for i in range(5)])
xf = np.linalg.solve(Hf, [0, 0, 0, 0, 1])
exact = np.array([630., -12600, 56700, -88200, 44100])
print("和精確解最大的差 :", f"{np.abs(xf - exact).max():.3e}")
print("cond(H5) =", f"{np.linalg.cond(Hf):.3e}")

# ---- Lay 2.3 Exercise 53:12 階 Hilbert 矩陣,浮點完全失守 ----
H12 = np.array([[1 / (i + j + 1) for j in range(12)] for i in range(12)])
print("cond(H12) =", f"{np.linalg.cond(H12):.3e}")
E = H12 @ np.linalg.inv(H12) - np.eye(12)
print("A @ inv(A) 離單位矩陣最遠的一格 =", f"{np.abs(E).max():.3e}")
```

```text expected
det = -1/100
精確解(原始資料)  : [3.94, 0.49]
精確解(四捨五入後): [2.9, 2.0]
x1 的相對誤差 = 26%
x2 的相對誤差 = 308%
Exercise 9: det = 1  cond ≈ 23683  → 約損失 4.4 位
Exercise 10: det = 2  cond ≈ 68622  → 約損失 4.8 位
精確解(Rational): [630, -12600, 56700, -88200, 44100]
```

```python todo
# TODO 解讀:回答三個問題
obs = {
    "det_tells_stability": None,  # True / False:det 的大小能不能看出矩陣好不好算?
    "h12_worst_entry": None,      # 填 H12 @ inv(H12) 離單位矩陣最遠那一格的量級,例如 1e-2
    "why_rational": "",           # 一句話:Hilbert 矩陣為什麼一定要用 Rational?
}
```

**會看到**:

- **Exercise 49**:$\det = -1/100$,右端只動了不到 $0.05\%$,兩個未知數分別錯了 $26\%$ 與 $308\%$。這個系統**完全可逆**,但數值上不可信。
- **Exercise 9 的矩陣 $\det = 1$,條件數卻約 23,000**。行列式漂亮不代表矩陣健康——這是本週最重要的一句話。
- **「先造答案再解回來」**是很實用的測試手法:自己挑一個 $\mathbf{x}$、算出 $\mathbf{b}$、再叫程式解回來,就知道掉了幾位。這裡大約掉到第 12 位,和 $16 - \log_{10}(2.4 \times 10^4) \approx 11.6$ 吻合。
- **Hilbert(5)**:條件數約 $4.8 \times 10^5$,浮點解和精確解差了 $10^{-7}$ 這個量級——原本是整數的答案,已經看得到誤差了。
- **Hilbert(12)**:條件數超過 $10^{16}$,已經超出雙精度的能力。`A @ inv(A)` 應該是單位矩陣,實際上有某一格離 0 差了 $10^{-2}$——**整整 14 個數量級的失準**。

## ④ 應用 · LU 分解:電腦真正在做的事
最後一格做三件事:看 `scipy.linalg.lu` 回傳什麼、驗證課本的手算結果、以及 LU 在「同一個 $A$、很多個 $\mathbf{b}$」時的威力。

```python
import time

# ---- scipy 的 LU:那個 P 是什麼? ----
A4 = np.array([[2., 4, -1, 5, -2], [-4, -5, 3, -8, 1],
               [2, -5, -4, 1, 8], [-6, 0, 7, -3, 1]])
P, L, U = sla.lu(A4)
print("P 是單位矩陣嗎?", np.allclose(P, np.eye(4)))
print("P @ L @ U == A 嗎?", np.allclose(P @ L @ U, A4))

# ---- 課本 2.5 Example 2 的手算結果(不換列)----
Lh = np.array([[1., 0, 0, 0], [-2, 1, 0, 0], [1, -3, 1, 0], [-3, 4, 2, 1]])
Uh = np.array([[2., 4, -1, 5, -2], [0, 3, 1, 2, -3], [0, 0, 0, 2, 1], [0, 0, 0, 0, 5]])
print("課本 Example 2 的 L @ U 等於 A 嗎?", np.allclose(Lh @ Uh, A4))

# ---- 同一個 A、很多個 b:分解一次 vs 每次重解 ----
rng2 = np.random.default_rng(11)
n = 400
M = rng2.random((n, n)) + n * np.eye(n)
bs = rng2.random((n, 60))
lu_piv = sla.lu_factor(M)                       # 只分解一次
t0 = time.perf_counter()
X1 = np.column_stack([sla.lu_solve(lu_piv, bs[:, j]) for j in range(60)])
t1 = time.perf_counter()
t2 = time.perf_counter()
X2 = np.column_stack([np.linalg.solve(M, bs[:, j]) for j in range(60)])
t3 = time.perf_counter()
print(f"LU 分解一次、解 60 次   :{t1-t0:.4f} 秒")
print(f"每次都重新 solve(60 次):{t3-t2:.4f} 秒")
print("兩種做法答案一樣嗎?", np.allclose(X1, X2))

# ---- Lay 2.5 Exercise 31(T):平板的穩態熱傳導,帶狀矩陣 ----
Ap = np.array([
    [4, -1, -1, 0, 0, 0, 0, 0], [-1, 4, 0, -1, 0, 0, 0, 0],
    [-1, 0, 4, -1, -1, 0, 0, 0], [0, -1, -1, 4, 0, -1, 0, 0],
    [0, 0, -1, 0, 4, -1, -1, 0], [0, 0, 0, -1, -1, 4, 0, -1],
    [0, 0, 0, 0, -1, 0, 4, -1], [0, 0, 0, 0, 0, -1, -1, 4]], dtype=float)
bp = np.array([5., 15, 0, 10, 0, 10, 20, 30])
Pp, Lp, Up = sla.lu(Ap)
print("平板的解 =", np.round(np.linalg.solve(Ap, bp), 4))
print("A 有幾格非零?", int(np.count_nonzero(Ap)))
print("L、U 各有幾格非零?", int(np.count_nonzero(np.round(Lp, 12))),
      int(np.count_nonzero(np.round(Up, 12))))
print("A 的反矩陣有幾格非零?", int(np.count_nonzero(np.round(np.linalg.inv(Ap), 12))))

# ---- Lay 2.5 Exercise 32(T):桿上的非穩態熱傳導,同一個 A 解四次 ----
C = 1.0
Ar = np.diag([1 + 2 * C] * 5) + np.diag([-C] * 4, 1) + np.diag([-C] * 4, -1)
lu_rod = sla.lu_factor(Ar)                      # 分解一次
t = np.array([10., 12, 12, 12, 10])
for k in range(1, 5):
    t = sla.lu_solve(lu_rod, t)                 # 前代 + 回代,做四次
    print(f"t{k} =", np.round(t, 4))
```

```text expected
P 是單位矩陣嗎? False
P @ L @ U == A 嗎? True
課本 Example 2 的 L @ U 等於 A 嗎? True
兩種做法答案一樣嗎? True
平板的解 = [ 3.9569  6.5885  4.2392  7.3971  5.6029  8.7608  9.4115 12.0431]
A 有幾格非零? 28
L、U 各有幾格非零? 21 21
A 的反矩陣有幾格非零? 64
t1 = [ 6.5556  9.6667 10.4444  9.6667  6.5556]
t2 = [4.7407 7.6667 8.5926 7.6667 4.7407]
t3 = [3.5988 6.0556 6.9012 6.0556 3.5988]
t4 = [2.7922 4.7778 5.4856 4.7778 2.7922]
```

```python todo
# TODO 應用:三個問題
ans = {
    "why_P": "",          # scipy 為什麼要多回傳一個 P?
    "lu_speedup": None,   # 你量到的倍數(重解 60 次 ÷ LU 解 60 次)
    "why_not_inverse": "" # 平板那題:為什麼大型問題不存 A 的反矩陣?
}
```

**會看到**:

- **`P` 不是單位矩陣**。SciPy 為了數值穩定會做 partial pivoting(挑絕對值最大的當樞軸),所以它得到的是 permuted LU:$A = PLU$。課本 Example 2 的手算版本(不換列)也正確,兩者只是不同的分解。
- **同一個 $A$ 解 60 次**:`lu_factor` 只分解一次、`lu_solve` 做 60 次前代回代,比每次重新 `solve` 快很多。這正是課本開頭那個「一連串方程式」的場景。
- **平板那題最值得看**:$A$ 只有 **28** 格非零(帶狀),$L$、$U$ 各 21 格也是帶狀,但 $A^{-1}$ **64 格全部非零**。矩陣大的時候,存 $L$、$U$ 和存 $A^{-1}$ 的差別可以是幾個數量級——這就是課本 Numerical Note 第 4 點說的事。
- **桿子那題**:溫度隨時間單調下降、左右對稱,符合兩端固定 $0°$ 的物理直覺。而且四個時間點共用同一個分解。

**本週的兩條規矩**:要解方程組**不要算反矩陣**;矩陣大又稀疏時**更不要**。
