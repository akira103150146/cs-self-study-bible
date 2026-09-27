---
id: C1.5
title_en: Computing as a Tool and a Discipline
title_zh: 計算作為工具與學科
sub: Who uses computing, who builds it, and the big ideas behind it
level: basic
lab_hook: "任務 5:`toolcheck.sh`"
---
## 觀念
Computing is both a **tool** and a **discipline**.

As a **tool**, computers help people in every field solve problems: scientists simulate climate, doctors analyze scans, artists create images and music. Roughly three groups of people interact with computing systems:

- **Application users / specialists**: use applications (possibly highly technical ones) to solve problems in their own field.
- **Programmers**: build tools and applications for others.
- **Systems designers**: build the systems software and hardware that everything else runs on.

As a **discipline**, computer science is the systematic study of **algorithmic processes**: their theory, analysis, design, efficiency, implementation, and application. Computing draws on mathematics (theory), science (experiments and models), and engineering (building reliable systems).

**The big ideas of computing** (as organized in the AP Computer Science Principles framework that this book follows): **creative development**, **abstraction**, **data and information**, **algorithms**, **programming**, **computer systems and networks (the Internet)**, and **impact of computing** on society.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| discipline | 學科 | 有系統的知識領域 |
| algorithmic process | 演算法程序 | 可以用明確步驟描述、交給機器執行的程序 |
| application specialist | 應用專家 | 用電腦解決自己領域問題的人 |
| systems designer | 系統設計者 | 建造系統軟體與硬體的人 |
| toolchain | 工具鏈 | 開發程式所需的一整組工具:編輯器、編譯器、版本控制、除錯器… |
| version control | 版本控制 | 記錄程式每一次修改的系統,如 git |

## 白話說
會開車的人很多,會修車的人少一些,會設計引擎的人更少。電腦也一樣:大部分人是**使用者**,資工系要把你訓練成能**造工具**(程式設計師)、甚至**造出讓別人造工具的系統**(系統設計者)的人。

資訊科學不只是「寫程式」。它問的是:什麼問題可以用步驟解決?怎麼解最快?怎麼證明是對的?怎麼蓋一個不會壞的系統?這些問題橫跨數學、科學與工程。

## 後面會用到
- **程式設計**、**軟體工程**:工具鏈(編輯器、編譯器、git、除錯器、測試)是每天的工作環境。
- **演算法**、**計算理論**:「演算法程序」的理論與分析(第 7、18 章)。
- **資訊倫理**:本課每章結尾的倫理議題,對應「計算的影響」。

## 現代補充
今天專業的開發工具鏈包括:**git**(版本控制)、**容器**(Docker,讓每個人的環境完全一樣——本課的 Lab 就是這樣跑的)、**雲端**(程式跑在別人的機房)、**CI**(每次提交自動跑測試),以及 **AI 輔助寫程式**。AI 可以大幅加快速度,但它會很有自信地寫出錯的程式——**你一定要能讀懂、並用測試驗證它的產出**。這正是紮實基礎的價值。

## 原理
**為什麼資訊科學同時是數學、科學和工程?**

- **數學**:演算法的正確性可以被證明;有些問題被證明「不可能用任何程式解決」(第 18 章的停機問題)。
- **科學**:效能、使用者行為、網路流量常常只能用實驗與模型研究,就像物理學研究自然現象。
- **工程**:真實系統要在有限的預算、時間、可靠度要求下蓋出來,需要設計、取捨與測試。

三者的方法不同:數學重證明,科學重實驗,工程重建造與取捨。一個好的資訊工程師要三種都會用。

## 老師講解
### 例 1
Classify each person as an application user/specialist, a programmer, or a systems designer: (a) a biologist who runs sequence-alignment software, (b) someone who writes a mobile app for a bakery, (c) an engineer who writes the Linux memory manager, (d) an accountant who builds complex spreadsheets.

1. 判斷依據是「他主要在**使用**、**建造應用**,還是**建造系統**」。
2. (a) 生物學家用現成軟體解決自己領域的問題 → **應用專家**。
3. (b) 為別人寫 App → **程式設計師**。
4. (c) 寫作業系統的記憶體管理 → **系統設計者**。
5. (d) 會計師的試算表可能很複雜,甚至有公式邏輯,但仍是在使用應用程式解決本行問題 → **應用專家**。界線不絕對:如果他開始寫巨集給全公司用,就帶有程式設計師的角色。

### 例 2
For each big idea of computing, give one concrete example from this course: abstraction, data and information, algorithms, the Internet.

1. **Abstraction**:Lab 任務 3 的 KVStore 把磁碟區塊藏在 `put`/`get` 介面後面。
2. **Data and information**:第 3 章把文字、聲音、影像都變成位元,並學會壓縮。
3. **Algorithms**:第 7 章的搜尋與排序;第 3 章的 Huffman 編碼也是一個演算法。
4. **The Internet**:第 15 章的 TCP/IP 與 DNS。
5. 重點:七個大觀念不是七個獨立章節,而是貫穿整門課的視角。

## 易錯點
- 把資訊科學等同於「寫程式」:程式是工具,核心是演算法與系統。
- 以為用 AI 產生的程式可以不用看懂:產出可能有錯,驗證責任在你。

## 教學提示
第一堂課可以問學生「你以後想當這三種人中的哪一種?」,順勢介紹資工系各門必修分別在訓練什麼。Lab 任務 5 讓學生第一次在統一的 Docker 環境裡檢查工具鏈,建議課堂一起做完。

## 練習
### 照做
List the three groups of people who interact with computing systems, with one example each.

#### 解答
應用使用者/專家(例:用統計軟體的心理學家)、程式設計師(例:寫網頁應用的工程師)、系統設計者(例:設計 CPU 或寫作業系統的工程師)。

### 是非
True or false: Computer science is only about writing programs.

#### 解答
False。它研究演算法程序的理論、分析、設計、效率、實作與應用;寫程式只是其中實作的一部分。

### 變化
Explain in your own words why a course environment built with Docker helps a class of 60 students.

#### 解答
容器把作業系統、編譯器、函式庫的版本全部固定下來,每個人跑的是完全相同的環境;老師驗證過能跑的 Lab,學生拿到也一定能跑,避免「在我電腦上可以」的問題,也不用各自安裝設定。

### 應用
An AI assistant writes a function for you that passes the two examples you gave it. List two things you should do before trusting it.

#### 解答
例如:讀懂程式、確認邏輯與邊界情況(空輸入、負數、極大值);寫更多測試(包括邊界與錯誤情況)並執行;檢查它有沒有用到不存在或不安全的函式;看它是否符合題目的所有限制。任兩項。

### 挑戰
Give one example each of how computer science uses the methods of mathematics, science, and engineering.

#### 解答
參考:數學——證明二分搜尋一定在 $\lceil \log_2(n+1) \rceil$ 次比較內結束,或證明停機問題不可解;科學——用實驗量測排序演算法在真實資料上的執行時間、建立效能模型;工程——在時間與預算限制下設計並測試一個可靠的網路服務,做效能與成本的取捨。
