---
id: C1.2
title_en: Abstraction
title_zh: 抽象
sub: Keep only the details you need right now
level: basic
lab_hook: "任務 3:`KVStore`(在 `RawDisk` 上蓋一層抽象)"
---
## 觀念
An **abstraction** is a mental model that removes complex details: it keeps only the information necessary to accomplish a goal and hides the rest.

In a computing system, every layer is an abstraction of the layers below it. A layer offers an **interface** (what you can ask it to do) and hides its **implementation** (how it actually does it). Users of the interface do not need — and should not rely on — the implementation details.

Examples:

- A **function** hides its body behind its name and parameters.
- A **file** hides disk blocks, sectors, and the physical location of bytes.
- A **high-level language** hides registers and machine instructions.
- A **network socket** hides packets, routing, and retransmission.

## 名詞對照
| English | 中文 | 說明 |
|---|---|---|
| abstraction | 抽象 | 只留下目前需要的細節,其他藏起來 |
| interface | 介面 | 外面看得到、可以使用的操作 |
| implementation | 實作 | 介面背後真正的做法 |
| information hiding | 資訊隱藏 | 刻意不讓使用者看到(或依賴)實作細節 |
| black box | 黑盒子 | 只看輸入輸出、不看內部的觀點 |

## 白話說
開車的人只需要方向盤、油門、煞車這組**介面**,不需要懂引擎怎麼噴油點火(**實作**)。車廠換了一顆引擎,你照樣會開——這就是抽象的價值:**底下可以換,上面不用改**。

寫程式也一樣。你呼叫 `open("a.txt")` 讀檔,不用知道檔案被切成哪幾個磁碟區塊;作業系統換了檔案系統,你的程式照跑。

## 後面會用到
- **資料結構**:抽象資料型別(ADT)就是「介面與實作分開」(本課第 8 章)。
- **物件導向程式設計**:封裝(encapsulation)是抽象的語言機制(第 9 章)。
- **作業系統**:行程、虛擬記憶體、檔案都是 OS 提供的抽象(第 10、11 章)。
- **計算機網路**:協定分層(TCP/IP)每一層都是下一層的抽象(第 15 章)。

## 原理
抽象讓人能處理複雜系統,是因為它**限制了相依性**:上層只依賴下層的介面,不依賴實作。形式上可以這樣想——若 A 只透過介面 I 使用 B,那麼任何滿足 I 的 B′ 都能替換 B,而 A 的正確性不受影響。

這也說明了抽象的兩個常見失敗:

1. **洩漏的抽象(leaky abstraction)**:下層的細節還是透出來影響上層。例:檔案「抽象」看起來是一串連續位元組,但隨機讀取在傳統硬碟上比循序讀取慢很多——效能細節洩漏了。
2. **使用者偷看實作**:如果上層直接依賴下層的內部(例如直接讀某個私有欄位),下層一換就壞。Lab 任務 3 的隱藏測試會換掉區塊大小,專門抓這種情況。

## 老師講解
### 例 1
A `RawDisk` can only read or write whole blocks of a fixed size (for example 64 bytes). Design the interface of a key-value store built on top of it, and explain which details the interface hides.

1. **先想使用者要什麼**:存一個值、拿回一個值、刪掉、列出所有 key。所以介面是 `put(key, value)`、`get(key)`、`delete(key)`、`keys()`。
2. **介面裡刻意不出現的東西**:區塊編號、區塊大小、值被切成幾塊、索引存在哪。這些都屬於實作。
3. **錯誤也要用抽象的語言表達**:找不到 key 時丟 `KeyError`,而不是「區塊 17 是空的」這種實作層的訊息。
4. **檢查抽象是否成立**:同一段使用者程式,換一顆區塊大小不同的 disk 還能跑嗎?能 → 介面沒有洩漏區塊大小。

### 例 2
Identify the interface and the hidden implementation in each: (a) `len(my_list)` in Python, (b) a car's gas pedal, (c) `printf("%d", x)` in C.

1. (a) 介面:「給我一個串列,回傳它的長度」。實作:CPython 的 list 物件內部存了一個長度欄位,`len` 直接讀它(O(1)),使用者不用知道。
2. (b) 介面:「踩越深、加速越快」。實作:電子油門、噴油量、點火時間由引擎控制電腦決定。
3. (c) 介面:「照格式把 x 印出來」。實作:把整數轉成十進位字元、放進緩衝區,最後透過 write 系統呼叫交給作業系統輸出。
4. 共通點:使用者只靠介面就能正確使用;實作可以更新(例如 C 函式庫改版)而不影響使用者。

## 易錯點
- 把「抽象」誤解成「模糊、不精確」:抽象的介面必須**很精確**(輸入什麼、回傳什麼、錯誤時怎樣),只是不談實作。
- 介面設計洩漏實作:例如 `get_block_for_key(key)` 這種名字就把區塊暴露給使用者了。

## 教學提示
可以讓學生先嘗試「直接用 RawDisk 存一個 1000 位元組的值」,體會沒有抽象有多痛苦,再引入 KVStore。延伸專案 3 讓學生量測抽象層的成本,可在課堂提一句「抽象不是免費的」。

## 練習
### 照做
In one sentence each, define *interface* and *implementation*.

#### 解答
介面:外部使用者可以呼叫的操作與其行為約定(輸入、輸出、錯誤)。實作:介面背後實際完成這些操作的程式碼或機制。

### 是非
True or false: If two implementations provide exactly the same interface and behavior, a program that uses only the interface cannot tell which one it is using (ignoring speed).

#### 解答
True。這正是抽象讓實作可以替換的原因;唯一可能透露差異的是效能等「洩漏」的細節。

### 變化
A file in an operating system is an abstraction. Name two details that the file abstraction hides from a program that calls `read()`.

#### 解答
例如:資料實際存在磁碟的哪些區塊/磁區、區塊是否連續、硬碟是 SSD 還是傳統硬碟、資料是否已經在快取裡、檔案系統的種類(ext4、NTFS)。任兩項。

### 應用
A teammate's code calls `kv._blocks[3]` to read data directly from the disk underneath your `KVStore`. Explain why this is a problem and what should happen instead.

#### 解答
這繞過了介面、依賴了實作細節(資料放在哪個區塊)。一旦 KVStore 改變存放方式或換一顆區塊大小不同的 disk,他的程式就會壞。應該只透過 `get()` 取資料;若介面不夠用,就擴充介面,而不是偷看實作。

### 挑戰
Give an example of a *leaky abstraction* in computing and explain what leaks.

#### 解答
參考:檔案抽象看起來是可隨機存取的一串位元組,但在傳統硬碟上隨機讀比循序讀慢百倍,效能細節洩漏出來;或 TCP 看起來是可靠的串流,但網路斷線時呼叫會卡住很久或失敗,底下「封包可能遺失」的本質洩漏了;或浮點數看起來是實數,但 `0.1 + 0.2 != 0.3` 洩漏了二進位表示的限制。
