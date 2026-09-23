## ① 預測 · 寫下你的預測
下面四個矩陣都是理論課做過的題目,每一個的**行**是一組向量。**先不要往下跑**,憑理論課的方法寫下:各行線性獨立嗎?

提示:先試「用看的」三招(有零向量?個數比分量多?兩個的話是倍數?),用不上再想列化簡。

```python
V1 = Matrix([[1, 4, 2], [2, 5, 1], [3, 6, 0]])          # 觀念 3 例 1(Lay 1.7 Example 1)
V2 = Matrix([[0, 1, 4], [1, 2, -1], [5, 8, 0]])         # 觀念 3 例 2(Lay 1.7 Example 2)
V3 = Matrix([[2, 4, -2], [1, -1, 2]])                    # 觀念 5 例 1(Lay 1.7 Example 5)
V4 = Matrix([[-2, 3], [4, -6], [6, -9], [10, 15]])       # 觀念 5 例 2(c)(Lay 1.7 Example 6)
V1, V2, V3, V4
```

```python todo
# TODO 預測:把 None 換成 True(各行線性獨立)或 False(相依)
pred = {"V1": None, "V2": None, "V3": None, "V4": None}
```

## ② 計算 · 秩(rank)等於行數 ⇔ 各行獨立
各行獨立 ⇔ 每一行都是 pivot 行 ⇔ pivot 的個數等於行數。pivot 的個數有個名字叫**秩**(rank),`M.rank()` 直接算出來。第 7 週會正式介紹秩,現在只要知道「秩 = pivot 個數」。

```python
for name, M in [("V1", V1), ("V2", V2), ("V3", V3), ("V4", V4)]:
    n = M.shape[1]                       # 行數 = 向量個數
    r = M.rank()                         # 秩 = pivot 個數
    print(f"{name}: {n} 行,rank = {r} → 各行線性獨立? {r == n}")
    print(f"    你的預測: {pred[name]}")
```

```text expected
V1: 3 行,rank = 2 → 各行線性獨立? False
V2: 3 行,rank = 3 → 各行線性獨立? True
V3: 3 行,rank = 2 → 各行線性獨立? False
V4: 2 行,rank = 2 → 各行線性獨立? True
```

**會看到**:V3 是 ℝ² 裡的 3 個向量,rank 最多 2,不可能等於 3——這就是 Theorem 8。V4 的兩個向量「幾乎」是倍數($-\tfrac32$ 倍),只差最後一個分量,rank 還是 2,獨立。

```python todo
# TODO 計算:用 np.linalg.matrix_rank 對 V1 再算一次(先轉成 np.array(V1, dtype=float))
# 結果和 SymPy 的 rank 一樣嗎?
```

## ② 計算 · nullspace():齊次解與相依關係
`M.nullspace()` 回傳一組向量,$M\mathbf{x} = \mathbf{0}$ 的解集就是它們的 Span。同一個指令有兩種讀法:

- **觀念 1 的讀法**:齊次方程組的解集。
- **觀念 3 的讀法**:每個向量都是一條**相依關係的權重**。回傳空的 `[]`,就代表各行獨立。

```python
A = Matrix([[3, 5, -4], [-3, -2, 4], [6, 1, -8]])    # 觀念 1 例 1(Lay 1.5 Example 1)
print("Ax = 0 的解集由這些向量生成:", [list(v) for v in A.nullspace()])
print("V1 各行的相依關係(權重):", [list(v) for v in V1.nullspace()])
```

```text expected
Ax = 0 的解集由這些向量生成: [[4/3, 0, 1]]
V1 各行的相依關係(權重): [[2, -1, 1]]
```

**會看到**:第一行就是理論課的 $\mathbf{v} = (\tfrac43, 0, 1)$。第二行的權重 $(2, -1, 1)$ 代表 $2\mathbf{v}_1 - \mathbf{v}_2 + \mathbf{v}_3 = \mathbf{0}$,和理論課取 $x_3 = 1$ 的結果一樣(理論課取 $x_3 = 5$ 得到 $10\mathbf{v}_1 - 5\mathbf{v}_2 + 5\mathbf{v}_3 = \mathbf{0}$,只差 5 倍)。

```python todo
# TODO 計算:對 V2 呼叫 nullspace(),結果是什麼?用一句話說明它代表 V2 的各行怎樣
```

## ② 計算 · 特解 + 齊次解:gauss_jordan_solve
`A.gauss_jordan_solve(b)` 回傳 $A\mathbf{x} = \mathbf{b}$ 的一般解,自由變數用參數 `tau0`、`tau1`… 表示。把參數設成 0 就是特解 $\mathbf{p}$;對參數微分就是齊次解的方向 $\mathbf{v}$。

```python
b = Matrix([7, -1, -4])                               # 觀念 2 例 1(Lay 1.5 Example 3)
sol, params = A.gauss_jordan_solve(b)
t = params[0]                                         # 唯一的自由參數
p = sol.subs(t, 0)                                    # 參數取 0 → 特解
v = sol.diff(t)                                       # 參數前面的係數 → 齊次解方向
print("特解 p:", list(p))
print("方向 v:", list(v))
print("A p =", list(A * p), "  A v =", list(A * v))
```

```text expected
特解 p: [-1, 2, 0]
方向 v: [4/3, 0, 1]
A p = [7, -1, -4]   A v = [0, 0, 0]
```

**會看到**:$\mathbf{p} = (-1, 2, 0)$、$\mathbf{v} = (\tfrac43, 0, 1)$,和理論課一模一樣。最後一行就是 Theorem 6 的驗算:$A\mathbf{p} = \mathbf{b}$、$A\mathbf{v} = \mathbf{0}$。

```python todo
# TODO 計算:Lay 1.5 Exercise 20 的方程組,用 gauss_jordan_solve 求出 p 與 v
# 係數 [[1,3,-5],[1,4,-8],[-3,-7,9]],右邊 (4, 7, -6);和理論課答案對照
```

## ③ 解讀 · 陷阱一:兩兩不是倍數,整組照樣相依
理論課說「看倍數」只適用於兩個向量。實際檢查 V3 的每一對:

```python
from itertools import combinations

cols = [V3[:, j] for j in range(3)]
for i, j in combinations(range(3), 2):
    print(f"第 {i + 1}、{j + 1} 行:rank = {Matrix.hstack(cols[i], cols[j]).rank()}")
print("三行一起:rank =", V3.rank())
```

```text expected
第 1、2 行:rank = 2
第 1、3 行:rank = 2
第 2、3 行:rank = 2
三行一起:rank = 2
```

**會看到**:每一對的 rank 都是 2(兩兩獨立),三個一起的 rank 還是 2,小於 3,整組相依。

```python todo
# TODO 解讀:用一句話說明為什麼「兩兩獨立」推不出「整組獨立」
# 提示:ℝ² 最多容得下幾個獨立的方向?
```

## ③ 解讀 · 陷阱二:有雜訊的資料,rank 會變
真實資料是浮點數,而且有量測誤差。「剛好相依」的欄位加上一點點雜訊,電腦就會說它們獨立。

```python
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)   # 第三行 = 2 × 第二行 − 第一行
print("原本的 X            :", np.linalg.matrix_rank(X))
Xn = X.copy()
Xn[0, 2] += 1e-10                                             # 加上一點點雜訊
print("加上 1e-10 的雜訊   :", np.linalg.matrix_rank(Xn))
print("放寬容忍度 tol=1e-8 :", np.linalg.matrix_rank(Xn, tol=1e-8))
```

```text expected
原本的 X            : 2
加上 1e-10 的雜訊   : 3
放寬容忍度 tol=1e-8 : 2
```

**會看到**:只改了一個數字的第十位小數,rank 就從 2 變成 3。`matrix_rank` 內部有一個「小於多少就當成 0」的容忍度(tolerance),放寬它才又得到 2。**對浮點數資料來說,「相依」是程度問題**:第 16 週的奇異值(SVD)會告訴你「差多少才算相依」。

```python todo
# TODO 解讀:印出 np.linalg.svd(Xn, compute_uv=False)(三個奇異值)
# 最小的那個大約多大?它和 tol 的大小有什麼關係?
```

## ④ 應用 · pandas:找出資料表裡多餘的欄位
一張學生資料表有 7 個數值欄位。哪些是多餘的(可以由其他欄算出來)?把每一欄當成矩陣的一行,**pivot 欄位就是要留的**,其他欄可以由 pivot 欄位組合出來,組合的權重就寫在 RREF 那一行裡(觀念 3 的 Exercises 49–50)。

注意:RREF 要用**精確的分數**算。`sp.nsimplify` 會把 `1.65` 這種浮點數轉成分數 `33/20`,避免浮點誤差。

```python
import io
import pandas as pd

csv = """name,chinese,english,math,total,average,height_cm,height_m
Amy,72,66,81,219,73,165,1.65
Ben,85,71,90,246,82,178,1.78
Cat,60,75,69,204,68,158,1.58
Dan,90,88,95,273,91,172,1.72
Eve,54,63,72,189,63,160,1.60
Fay,78,81,84,243,81,169,1.69
Gus,66,60,78,204,68,181,1.81
Hal,81,92,73,246,82,175,1.75
"""
df = pd.read_csv(io.StringIO(csv))          # 實務上是 pd.read_csv("檔名.csv")
X = df.drop(columns="name")                 # 只留數值欄位
print("形狀:", X.shape)
print("rank =", np.linalg.matrix_rank(X.to_numpy()))

M = Matrix(X.to_numpy()).applyfunc(sp.nsimplify)   # 轉成精確分數再化簡
R, piv = M.rref()
print("pivot 欄位:", [X.columns[j] for j in piv])
for j, col in enumerate(X.columns):
    if j not in piv:                            # 不是 pivot 欄位 → 可以由 pivot 欄位組合
        terms = [f"({R[i, j]})·{X.columns[q]}" for i, q in enumerate(piv) if R[i, j] != 0]
        print(f"{col} = " + " + ".join(terms))
```

```text expected
形狀: (8, 7)
rank = 4
pivot 欄位: ['chinese', 'english', 'math', 'height_cm']
total = (1)·chinese + (1)·english + (1)·math
average = (1/3)·chinese + (1/3)·english + (1/3)·math
height_m = (1/100)·height_cm
```

**會看到**:7 個欄位只有 4 個是「獨立的資訊」。電腦自己找出了三條關係:總分 = 三科相加、平均 = 總分的三分之一、公尺 = 公分的百分之一。機器學習前處理時,這三欄要刪掉,否則線性迴歸的係數會解不出唯一答案(多重共線性)。

```python todo
# TODO 應用:只留 pivot 欄位做出 X_clean,確認它的 rank 等於欄位數
# 再加一欄 bonus = total + 5,它和其他欄相依嗎?為什麼?(提示:+5 不是線性組合)
```

## ④ 應用 · 課本電腦題:Lay 1.7 Exercises 47–50
**Lay 1.7 Exercise 47**(課本標 **T**):盡可能多挑 $A$ 的行,組成矩陣 $B$,使 $B\mathbf{x} = \mathbf{0}$ 只有平凡解。**Exercise 49**:沒挑到的行,在不在 $B$ 各行的 Span 裡?

```python
A47 = Matrix([[8, -3, 0, -7, 2],
              [-9, 4, 5, 11, -7],
              [6, -2, 2, -4, 4],
              [5, -1, 7, 0, 10]])
R, piv = A47.rref()
print("pivot 行:", [q + 1 for q in piv])
B = A47[:, list(piv)]                           # 只留 pivot 行
print("B x = 0 的非平凡解:", B.nullspace())     # 空的 → 只有平凡解
for j in range(A47.shape[1]):
    if j not in piv:
        w = B.gauss_jordan_solve(A47[:, j])[0]  # 解 B w = 第 j 行
        print(f"第 {j + 1} 行 = B 各行的組合,權重 {list(w)}")
```

```text expected
pivot 行: [1, 2, 5]
B x = 0 的非平凡解: []
第 3 行 = B 各行的組合,權重 [3, 8, 0]
第 4 行 = B 各行的組合,權重 [1, 5, 0]
```

**會看到**:$B = [\,\mathbf{a}_1 \;\; \mathbf{a}_2 \;\; \mathbf{a}_5\,]$,和書後解答一樣。沒挑到的第 3、4 行都在 $B$ 各行的 Span 裡:$\mathbf{a}_3 = 3\mathbf{a}_1 + 8\mathbf{a}_2$、$\mathbf{a}_4 = \mathbf{a}_1 + 5\mathbf{a}_2$。

```python todo
# TODO 應用:對 Exercise 48 的 5×6 矩陣做同樣的事(Exercise 50),矩陣見例題講義觀念 3
# 最後用一句話說明:為什麼沒挑到的行一定在 B 各行的 Span 裡?
```

## 驗算
```check
Matrix([[1, 4, 2], [2, 5, 1], [3, 6, 0]]).nullspace() == [Matrix([2, -1, 1])]
Matrix([[3, 5, -4], [-3, -2, 4], [6, 1, -8]]).nullspace() == [Matrix([Rational(4, 3), 0, 1])]
Matrix([[-2, 3], [4, -6], [6, -9], [10, 15]]).rank() == 2
Matrix([[1, 3, -5], [1, 4, -8], [-3, -7, 9]]) * Matrix([-5, 3, 0]) == Matrix([4, 7, -6])
Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).rank() == 2
Matrix([[72, 66, 81], [85, 71, 90], [60, 75, 69], [90, 88, 95], [54, 63, 72], [78, 81, 84], [66, 60, 78], [81, 92, 73]]) * Matrix([1, 1, 1]) == Matrix([219, 246, 204, 273, 189, 243, 204, 246])
```
