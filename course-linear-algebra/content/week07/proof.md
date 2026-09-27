---
after: 5
title_zh: Rank Theorem:一本帳,兩個欄位
---
## 定理
**The Rank Theorem (Lay Theorem 14).** If a matrix $A$ has $n$ columns, then

$$\operatorname{rank} A + \dim \operatorname{Nul} A = n$$

## 為什麼值得證
這個定理是**本章最好用的一句話**:兩個看起來完全不同的空間——$\operatorname{Col} A$(住在 $\mathbb{R}^m$)與 $\operatorname{Nul} A$(住在 $\mathbb{R}^n$)——維度居然被一條等式綁死。算出一個,另一個免費。

但它值得證的真正理由是:**證明本身只有一句話**。

> 列化簡之後,$A$ 的每一行**非此即彼**:要嘛是樞軸行、要嘛對應一個自由變數。沒有第三種,也沒有一行被算兩次。

整個定理就是在數這件事。**沒有任何技巧,只有「把帳記清楚」。** 這正是它適合當證明時刻的原因:學生會發現,一個看起來深刻的定理,可以由兩個已經學過的事實直接拼出來。

而且它馬上回收三筆本週的投資:

| 用到的東西 | 哪裡學的 |
|---|---|
| 樞軸行構成 $\operatorname{Col} A$ 的基底 | 觀念 3(Theorem 13) |
| 參數向量形式給出 $\operatorname{Nul} A$ 的基底 | 觀念 3(承第 3 週) |
| 維度 = 基底的向量個數 | 觀念 5 |

## 關鍵想法
把 $A$ 化到最簡列梯形 $B$,然後**替每一行貼一張標籤**:

$$\underbrace{n \text{ 行}}_{\text{全部}} = \underbrace{\text{樞軸行}}_{\to \; \operatorname{Col} A \text{ 的基底}} \; + \; \underbrace{\text{非樞軸行}}_{\to \; \text{自由變數} \; \to \; \operatorname{Nul} A \text{ 的基底}}$$

要讓這筆帳成立,必須確認**兩邊都是「一對一」**:

1. **每個樞軸行**貢獻**恰好一個** $\operatorname{Col} A$ 的基底向量。
2. **每個非樞軸行**貢獻**恰好一個** $\operatorname{Nul} A$ 的基底向量。

第 1 點是 Theorem 13(已證)。**第 2 點是這個證明真正要做的工作**:必須說明參數向量形式給出的那些向量,不但張成 $\operatorname{Nul} A$,而且**線性獨立**——否則它們不是基底,個數也就不能當維度。

**獨立性怎麼看出來?** 看「1 與 0 的位置」:對應自由變數 $x_j$ 的那個基底向量,在第 $j$ 格是 1,而其他基底向量在第 $j$ 格都是 0。

## 證明
設 $A$ 是 $m \times n$ 矩陣,$B$ 是 $A$ 的最簡列梯形,$r$ 是樞軸的個數。

**第一步:$\operatorname{rank} A = r$。**

由 Theorem 13,$A$ 的樞軸行構成 $\operatorname{Col} A$ 的一組基底。基底有 $r$ 個向量,所以

$$\operatorname{rank} A = \dim \operatorname{Col} A = r$$

**第二步:自由變數有 $n - r$ 個。**

$B$ 的每一行要嘛含樞軸、要嘛不含。含樞軸的有 $r$ 行,對應 $r$ 個基本變數;其餘 $n - r$ 行對應**自由**變數。這是一個行的分類,**每一行恰好落入一類**。

**第三步:$\dim \operatorname{Nul} A = n - r$。**

若 $r = n$(沒有自由變數),則 $A\mathbf{x} = \mathbf{0}$ 只有平凡解,$\operatorname{Nul} A = \{\mathbf{0}\}$,維度 0 $= n - r$ ✓。

以下設 $n - r \ge 1$。把自由變數記為 $x_{j_1}, \dots, x_{j_{n-r}}$。解 $B\mathbf{x} = \mathbf{0}$ 時,每個基本變數都被表示成自由變數的線性組合,於是通解可以寫成參數向量形式

$$\mathbf{x} = x_{j_1}\mathbf{u}_1 + x_{j_2}\mathbf{u}_2 + \cdots + x_{j_{n-r}}\mathbf{u}_{n-r}$$

其中 $\mathbf{u}_k$ 是「把 $x_{j_k}$ 設為 1、其他自由變數設為 0」所得到的解。要證 $\{\mathbf{u}_1, \dots, \mathbf{u}_{n-r}\}$ 是 $\operatorname{Nul} A$ 的基底:

- **張成**:上式對任何解都成立(自由變數可任意取值),所以每個 $\operatorname{Nul} A$ 的元素都是 $\mathbf{u}_k$ 的線性組合。反過來每個 $\mathbf{u}_k$ 本身也是解,所以 $\operatorname{Span}\{\mathbf{u}_1, \dots, \mathbf{u}_{n-r}\} = \operatorname{Nul} A$。
- **線性獨立**:設 $c_1\mathbf{u}_1 + \cdots + c_{n-r}\mathbf{u}_{n-r} = \mathbf{0}$。看第 $j_k$ 個座標:由建構方式,$\mathbf{u}_k$ 的第 $j_k$ 格是 **1**,而其他 $\mathbf{u}_i$($i \ne k$)的第 $j_k$ 格是 **0**。所以那一個座標的等式就是 $c_k = 0$。對每個 $k$ 都如此,故所有係數為 0。

兩條都成立,所以 $\{\mathbf{u}_1, \dots, \mathbf{u}_{n-r}\}$ 是基底,且

$$\dim \operatorname{Nul} A = n - r$$

**第四步:把帳加起來。**

$$\operatorname{rank} A + \dim \operatorname{Nul} A = r + (n - r) = n \qquad \blacksquare$$

**這個證明最重要的一行是第二步**:「每一行恰好落入一類」。所有內容都在那句話裡,其餘只是把「維度」的定義展開。

### 三個馬上可用的推論
**推論 1:$\operatorname{rank} A \le \min(m, n)$。**

樞軸每列至多一個、每行至多一個,所以 $r \le m$ 且 $r \le n$。**這是檢查答案的第一道關卡**——觀念 5 的 Exercise 28 就是因為算出 $\operatorname{rank} = 4$ 卻只有 3 列,才發現題目本身有問題。

**推論 2(IMT 的新條款):** 當 $A$ 是 $n \times n$ 時,

$$\operatorname{rank} A = n \iff \dim \operatorname{Nul} A = 0 \iff \operatorname{Nul} A = \{\mathbf{0}\} \iff A \text{ 可逆}$$

前兩個 $\iff$ 直接來自 Rank Theorem,最後一個接回上週的 (d)。**這就是觀念 6 裡 (o)、(p)、(q) 三條的全部證明。**

**推論 3:$m \times n$ 且 $m < n$ 的齊次方程式一定有非零解。**

$\operatorname{rank} A \le m < n$ ⇒ $\dim \operatorname{Nul} A = n - \operatorname{rank} A \ge n - m > 0$。第 3 週學過這件事(「未知數比方程式多就有自由變數」),現在有了**維度版本的證明**,而且順便得到「至少有 $n - m$ 維的解空間」這個更強的結論。

### 給學生的提醒
**這個定理的陷阱只有一個:$n$ 是行數。**

$$\operatorname{rank} A + \dim \operatorname{Nul} A = \text{行數}$$

因為 $\operatorname{Nul} A$ 裡的向量長度是 $n$(有 $n$ 個變數),而 $\operatorname{Col} A$ 裡的向量長度是 $m$。**這條等式記的是「變數的帳」,所以用行數。**

**考試怎麼考**:(a) 給矩陣尺寸與 rank,求 $\dim \operatorname{Nul} A$(或反過來);(b) 給一個不可能的組合,問哪裡矛盾(推論 1);(c) 要求說明為什麼參數向量形式給出的向量線性獨立(第三步的那一段);(d) 用 Rank Theorem 證明 IMT 的某一條。**不會要求默寫整個證明**,但第二步那句「每一行非此即彼」要能自己說出來。
