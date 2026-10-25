# data/mainline-projects.yaml:主線專題(任務線)的測試樹

這份 yaml 是書與「程式地下城」(9Jang)共用的**唯一來源**:任務線、驗收檢查(Boss 戰)、任務(零件)與任務目標(測試組)的名稱、說明、公開或隱藏、效能需求、`requiredBy`。

- **格式以 9Jang 的 Zod schema 為準**:`shared/src/schemas/mainline.schema.ts`(9Jang repo,撰寫中)。9Jang 用 `pnpm --filter @9jang/backend sync:mainlines --from <書>/data/mainline-projects.yaml` 驗證後轉成 `mainlines.generated.json`。schema 和本檔對不上時,改本檔。
- **隱藏測試的程式與資料不放在書裡**,只放在 9Jang 後端的任務套件。這裡只有名稱與一行說明。
- 書端的使用者:`_build_routes.py` 用它產生每份路線導讀頁的「本路線的主線專題」;各章的 Lab 方框照它抄任務名、任務目標與效能門檻。

## 形狀(9Jang 讀的欄位)

```yaml
version: 1
mainlines:
  - id: libds                 # 任務線 id:小寫英數字
    name: libds:自己的資料結構庫
    track: trunk              # tree.yaml 的路線 id
    lib: libds                # ~/零件庫/<lib>/
    project: proj-trunk-interview    # tree.yaml 的專題 id(多個檢查點時是第一個,見下面「決定」)
    acceptance:               # 驗收檢查＝Boss 戰
      - {id: boss.heap, name: …, description: …, consumes: [libds/heap]}
    tasks:                    # 任務＝零件
      - id: libds/heap        # 元件 id「<零件庫資料夾>/<名>」(不一定等於 lib,例 bookapi 線的 srv/http)
        order: 2              # 任務線內的順序
        name: 優先佇列
        files: [libds/heap.py]
        language: python      # python | c | cpp | hdl(另提議 asm、verilog、spice)
        chapter: "29-data-structures:本章 Lab:優先佇列 libds/heap.py"   # 「<章檔名>:<Lab 的 h3 全文>」
        evidenceFor: [t-adv-ds]          # tree.yaml 節點:通過這個任務算哪些節點的 Lab 證據
        consumes: []                     # 用到的上游元件 id
        groups:                          # 任務目標＝測試組
          - id: heap.order               # 「<名>.<組>」,同一條任務線內不重複
            name: 取出順序
            description: …
            visibility: public           # public(test／F5)| hidden(submit 的隱藏檢定)
            kind: function               # function | edge | perf | invariant | error | spec
            perf: {statement: …, seconds: 3, n: 100000}   # 只有 kind: perf 才有
            requiredBy: [boss.heap, graph.perf]           # 哪個 Boss 或下游測試組需要它
            book: …                      # 可省略:書的小節
```

- `chapter`:冒號前是章的檔名 id(`book.js` 的 id 或 `planned_chapters` 裡的新章);書裡還沒有章時寫缺口編號(例 `G17`)。冒號後是 Lab 的 h3 全文,一律是 `本章 Lab:<任務名> <檔案>`,章作者照抄。h3 的 id 是 `anchor`。
- `requiredBy` 與 `used_by` 的參照:同一條任務線直接寫 id;跨任務線寫 `<任務線 id>/<id>`(例 `puzzle/boss.solve-15`、`bookapi/cp3.cache-latency`)。任務 id(含 `/`)全書唯一,直接寫。
- `requiredBy` 可以指到:驗收檢查、測試組,或同一條(或別條)任務線的 `future_acceptance` 整合題(書端欄位,見下表)。
- **效能門檻由下游的數字推導**:效能組的 `requiredBy` 至少要有一個**寫了時限**的需求(有 `perf` 的驗收檢查、別的效能組,或有 `perf` 的整合題);只指到「重跑全套檢定」的 `boss.*`(沒有時限)不算推導。`seconds` 不能比它 `requiredBy` 的任何一個時限寬。指到別的效能組只算轉手:那一組自己的 `requiredBy` 鏈最後要走到有 `perf` 的驗收檢查或整合題。`requiredBy` 不能寫自己。需求(整合題、驗收檢查或下游效能組)的 `perf.budget: {<效能組 id>: 秒}` 把總時限拆給各零件:key 是效能組 id,跨任務線寫 `<任務線 id>/<組 id>`(例 `libds/heap.perf`),那一組的 `requiredBy` 要寫這個需求;零件的 `seconds` 改比它分到的秒數,分到的加起來不能超過總時限(例:路網導航 3.5 秒＝dijkstra 3 秒＋查詢 0.5 秒)。下游用到的工作量比零件測試大時,寫 `perf.usage: {<效能組 id>: 倍數}`(實測的操作數比),檢查改成「零件 `seconds` × 倍數 ≤ 分到的秒數」:每個零件都剛好卡在自己的門檻時,下游照樣在時限內。選修任務(`optional: true`)與 outline 任務沒有時限來源時只列資訊。
- `used_by`(書上的「之後會用在」)和對方的 `consumes` 要對稱:任務 X 的 `consumes` 有 C,C 的 `used_by` 就要列 X(同一條任務線的 Boss 不必列);C 的 `used_by` 列了 X,X 的 `consumes` 就要有 C。只要有一邊是 `detailed` 就報錯,兩邊都是 outline 只列資訊。整合題(`future_acceptance`)不寫進 `used_by`;章的 Lab 方框在「之後會用在」最後一句另外列出用到這個零件的整合題。

## 書端多加的欄位(9Jang 不讀;schema 若是 strict,sync 時請略過)

| 位置 | 欄位 | 用途 |
|---|---|---|
| 頂層 | `date` | 版本日期 |
| 頂層 | `planned_chapters` | 已定 id、還沒進 `book.js` 的新章:`{gap, title, appendix?}` |
| 頂層 | `node_extra` | 新章寫好後要加進哪些 tree.yaml 節點的閱讀清單 |
| 頂層 | `exam_lines` | 只有考試、沒有零件的主線(T1 APCS),只給路線頁 |
| mainline | `code` | 盤點表的編號(T2、H1、B1…) |
| mainline | `also_tracks` | 其他也要列出它的路線頁 |
| mainline | `checkpoints` | 依序的全部 tree.yaml 專題(第一個＝`project`) |
| mainline | `level`、`status`、`summary`、`note` | 程度;`detailed`(任務目標已設計)或 `outline`;說明 |
| mainline | `future_acceptance` | 之後才加的整合題(不是 v1 的 Boss 戰):`{id, name, description, consumes, perf?{statement, seconds, budget?, usage?}}`;`requiredBy` 可以指到它(9Jang 的 sync 要認得,見待決 5) |
| mainline | `steps` | 不產生零件的關卡或答題(例:CTF 的終端機尋寶) |
| acceptance | `visibility` | `public`/`hidden`(預設)/`teacher`(老師核可) |
| acceptance | `perf`、`perf_ref`、`checkpoint` | 驗收檢查的效能需求與參考解實測值;屬於哪個檢查點 |
| acceptance、task、future_acceptance | `requires_layer` | 判題映像要多裝的「層」(目前只有 `numpy`,見待決事項 12);沒寫＝一般沙盒就能判 |
| task | `lab_no`、`anchor`、`gap`、`gap_title`、`also_chapters`、`optional`、`status`、`used_by`、`note` | Lab 編號、h3 的 id、缺口、參考章、選修、覆寫狀態、誰接著用 |
| task | `interface`、`internal`、`provided` | **書端定的介面**(章的 Lab 方框照抄;9Jang 的 `task.yaml` `interface` 應一致)、規格規定的內部表示法、C 任務的規格標頭(起始碼給,判題用規格版;見待決事項 12) |
| task | `forbid`、`forbid_calls`、`forbidAttrTypes`、`require` | import 規則與限制(對應 9Jang `task.yaml` 的 `imports`) |
| task | `invariants` | 不變式(9Jang 設計 §3.3b):`{name, kind, symbol, sabotage?{attr, breaks}}`;`name` 也是一個 `kind: invariant` 的測試組 |
| group | `perf_ref`、`perf_basis`、`runner` | 參考解實測值;`estimate`＝還沒量;`py-io`/`service`(借書 API 一個任務有兩種 runner) |

## 書端決定的介面(libds;9Jang 計畫 Task 12–13 留給書定的部分)

- `libds/sort`:`stable_sort(a, key=None, reverse=False)`、`count_inversions(a)`、`bisect_left(a, x, key=None)`(key 只套在元素上,同 Python 3.10)。不能用 `sorted`、`list.sort`、`bisect`。
- `libds/heap`:`PriorityQueue(key=None)`(key 套在 priority 上,所有比較都用 `key(priority)`);`push(item, priority)`(item 已在 → `ValueError`)、`pop_min()`/`peek_min()` 回傳 `(item, priority)`、`decrease_key(item, priority)`(不在 → `KeyError`、變大 → `ValueError`)、`in`、`len`、`check()`;內部 `self.a=[(priority, item)]`、`self.pos`。
- `libds/lru`:`LRUCache(capacity, on_evict=None)`、`get(key, default=None)`、`put` 回傳被淘汰的 key 或 `None`、`resize(capacity)` 回傳 `None`、`keys_by_recency()`(最近的在前)、`len`;`on_evict(key, value)` 依淘汰順序呼叫。第一版沒有 `delete`。
- `libds/hashmap`:`HashMap()`、`put`、`get(key, default=None)`、`pop`(不在 → `KeyError`)、`len`、`iter`(插入順序)、`check()`;內部 `self.index`/`self.entries`/`self.size`;(live＋墓碑)/m > 0.7 擴容、live/m < 0.2 且 m > 8 縮容、最小 8。
- `libds/trie`:`insert` 記次數、`contains`、`remove(word) -> None`(整個字刪掉;字不在 → `KeyError`,什麼都不改)、`count_prefix`(經過前綴的插入次數)、`top_words(prefix, k)`(次數多到少、同次數依字典序)、`check()`(每個非根節點的經過數 ≥ 1、經過數＝結尾數＋子節點經過數的和;空的 Trie 也成立)。
- `libds/graph`:`Graph(directed=True)`、`add_edge(u, v, w=1)`、`bfs(s) -> dict`、`dfs_order(s) -> list`(迴圈版)、`topo_sort() -> list | None`(最小的先,用 `PriorityQueue`;自迴圈也算環)、`dijkstra(s) -> (dist, prev)`(用 `decrease_key`;dist、prev 只含走得到的點,`prev[s] = None`)、`shortest_path(s, t) -> (dist, path)`(走不到 `(None, None)`)。
- `libds/dsu`:`DSU(n)`、`find`(迴圈版、完整路徑壓縮)、`union -> bool`(依大小;一樣大時 b 的根接到 a 的根下)、`same`、`size_of`、`components()`、`check()`;`kruskal(n, edges)` 只依權重穩定排序(同權重依輸入順序),必須用 `libds.sort.stable_sort`。
- `libds/fenwick.hpp`:`libds::Fenwick(n)`,索引 1 起算,`range_add(l, r, v)`、`range_sum(l, r)`(兩棵 BIT)。
- `libds/segtree.hpp`:`libds::SegTree(vector<long long>)`,索引 0 起算,`update(i, v)`、`range_min(l, r)`、`argmin(l, r)`(同值取最左)。

## 待決事項的決定(書端先定,9Jang 可推翻)

1. 一條任務線對到多個 tree.yaml 專題(bookapi 三個檢查點、多數 outline 線):`project`＝第一個;全部依序列在 `checkpoints`;後面檢查點的驗收檢查加 `checkpoint` 欄,id 用 `cp2.`、`cp3.` 開頭。
2. `status: outline` 的任務線只列任務與 Boss,`groups: []`。建議 9Jang 的 `validateMainlines` 對 outline 線的「project 存在」(minidb 的 `proj-be-minidb` tree.yaml 還沒有)、「驗收檢查有人 requiredBy」、「跨線先修閉包」只警告不擋。
3. `language` 提議加 `asm`(Hack、RISC-V 組合語言)、`verilog`、`spice`。
4. 計畫寫的效能門檻有兩個在 CPython 參考解下做不到「參考解 ≤ 時限的 1/3」:heap(10^5 次 push＋decrease_key＋pop,計畫 1 秒,參考解 0.90 秒 → 改 3 秒)、sort(2×10^5,計畫 1 秒,參考解 0.38 秒 → 改 1.5 秒)。
5. 效能門檻一律照「參考解 ≤ 時限的 1/3」定;`perf_ref` 記參考解的實測值。另外,效能門檻要由下游的數字推導(老師規則「門檻由 requiredBy 決定」):v1 的面試 Boss 只是「重跑全套檢定」、沒有時限,所以 libds 的效能組改成也 `requiredBy` 有 `perf` 的 `future_acceptance` 整合題(路網導航、佈線預算、搜尋建議、快取重播、區間統計),整合題用 `perf.budget` 把總時限拆給零件。**請 9Jang**:`validateMainlines` 第 5 條把 `future_acceptance` 當成 `required_by` 的合法目標(sync 時帶進 `mainlines.generated.json`,只用來解析參照與比時限,不當 Boss 戰顯示、也不算進「每個驗收檢查至少被指到」);效能組的時限比 `budget` 分到的秒數(有 budget 時)或需求的 `seconds`。
6. `visibility: teacher`(老師核可)的驗收檢查不受「要有測試組 `requiredBy` 指到它」的檢查(例 `bookapi/cp3.deploy`)。
7. 任務層的 `status: outline` 即使在 `detailed` 任務線裡,也不擋「跨任務線先修閉包」的檢查,只列為資訊(例 `bookapi/auth` 用到 `webfix/passwords`)。
8. 書端多加的欄位(上面的表):建議 9Jang 的 Zod schema 用 `.passthrough()`,不要用 `.strict()`,sync 時略過不讀的欄位。
9. 和 9Jang spec 的命名:`invariants[].sabotage.attr` 照 spec §3.3b 的名稱,但我們允許寫成列表(例 `attr: [a, pos]`,spec 的例子是單一 `attr: a`);hashmap「不能用 dict 當底層儲存」的欄位照 plan Task 12 的驅動程式設定取名 `forbidAttrTypes`(spec 的 `task.yaml` 寫成 `imports.forbid` 的一條規則)。
10. 任務 id 的前綴是**零件庫資料夾**:`<零件庫資料夾>/<名>`,也就是 `~/零件庫/<資料夾>/`;不一定等於任務線的 `lib`(例 bookapi 線的 `srv/http`、`srv/pool`)。
11. 已知的順序例外:`srv/pool`(Lab 在 `24-operating-system`)用到 `srv/http`(Lab 在書裡比較後面的 `25-networking`)。算數的是任務線內的 `order`(http 是 1、pool 是 2),不是書的章序。
12. **已定:(b)**(老師 2026-10-26):`puzzle/astar`(節點 `ai-classical`)用 `libds/heap`,而 tree.yaml v3 的 `ai-classical` 沒有 `t-adv-ds` 先修。做法:`libds/heap` 的 `evidenceFor` 加 `t-graph`(`t-graph` 的 Lab `libds/graph` 本來就要先有 heap),`puzzle/astar` 的 `evidenceFor` 只留 `ai-classical`。`ai-classical` 的先修是 `t-graph`,跨任務線先修閉包檢查因此通過;A* 不會變成主幹節點的 Lab。另外考慮過的:(a) astar 多列 `t-graph-adv`(副作用是主幹學生要做 A* 才能完成 `t-graph-adv`);(c) A* 改回 heapq、不用 `libds/heap`。
13. **AI 層(未定,A1 nn 線)**:判題沙盒與學生容器都沒有 numpy(9Jang 設計 §5「不加 pytest、numpy」)。書端的處理:要 numpy 的任務與驗收檢查寫 `requires_layer: numpy`(目前是 `nn/arrays` 與驗收 `boss.knn`,以及 future_acceptance 的 `mnist-28`);A1 的其他任務(`nn/value`、`nn/linear`、`nn/optim`、`nn/mlp`)與 Boss `boss.mnist`、`boss.gradcheck`、`boss.report`、`boss.baseline` 都是純 Python,現在的沙盒就能判。**但解鎖會卡住(要老師決定)**:`nn/linear` 的節點 `ai-ml-basics` 與 `nn/value`、`nn/mlp` 的節點 `ai-mlp` 都在 `ai-numpy` 下游(`ai-ml-basics` 的先修有 `ai-numpy`),而 `ai-numpy` 唯一的 Lab 是要 numpy 的 `nn/arrays`;照「先修節點到 ◕ 才解鎖」的規則,AI 層定案以前 nn 線只有 `nn/optim`(節點 `ai-optim`)開得出來,專題的應考資格也拿不到。建議:AI 層定案前,`ai-numpy` 的 Lab 步驟先豁免(或改成不要 numpy 的形狀題卡片),定案後再補做 `nn/arrays`。另外 2026-10-26 拆掉了 `nn/optim` → `nn/value` 的依賴:原本 `nn/optim` consumes `nn/value`,而 `nn/value` 的節點 `ai-mlp` 要等 `ai-optim`(它的 Lab 就是 `nn/optim`)到 ◕ 才解鎖,是死結;現在 `nn/optim` 的測試用只有 `.data`、`.grad` 的 Param,整條 nn 線(arrays → ai-numpy;linear → ai-ml-basics;optim → ai-optim;value、mlp → ai-mlp,mlp 用到的 value／linear／optim 都在 ai-mlp 的先修閉包或同一個節點)沒有環。要 9Jang／老師決定:(a) 判題映像加不加 numpy 層(版本鎖定、套件鏡像、`OMP_NUM_THREADS=1`,否則 BLAS 多執行緒會讓 cgroup 的 CPU 時間變大);(b) 沒有這一層之前,`requires_layer` 的任務在 9Jang 顯示為 🚧(ai-numpy 節點暫時沒有 Lab 證據),還是先不算進任務線;(c) 有了之後,`mnist-28`(numpy 版 MLP、MNIST 子集)要不要取代 8×8 版當 Boss。建議 9Jang 的 schema 把 `requires_layer` 收成 `z.enum(['numpy']).optional()`。
14. **A1 的資料與判題時間**:v1 用 UCI 8×8 手寫數字(CC BY 4.0,出處寫在 yaml 的 nn `note`;書與任務 README 都要附出處)。公開 4,000 張放任務資料夾,隱藏 1,620 張只在 9Jang 的任務套件,切法的 seed 不寫進書。限制:這份資料整份在網路上公開,有心的人可以拿全部資料扣掉公開的 4,000 張、把答案寫死在程式裡;隱藏測試集只擋「不小心看到答案」,擋不住刻意查表。可以考慮:AST 檢查大型常數表、老師抽查,或改用老師班上收集的手寫數字(同樣的 8×8 前處理)當隱藏集。另外 `boss.mnist` 一個案例要在沙盒裡訓練(時限 180 秒 CPU,參考解 15 個 epoch 約 20 秒;時限照「每個 epoch 卡在 mlp.perf 的 6 秒 × 15 個 epoch ≤ 時限的一半」推出來),比一般案例長很多,請 9Jang 確認單一案例的時限上限(§5.4 的牆鐘是 2×tl+1)。tree.yaml 的專題名稱「只用 NumPy 手刻神經網路辨識手寫數字」與 verify「隱藏測試集準確率 ≥ 97%」:v1 不用 NumPy,門檻改成 96.5%(理由見 yaml nn 的 `note`:固定切法上參考 MLP 100 個 seed 最低 97.16%,原本的 97% 在隨機切法上有 8–21% 的組合過不了),**tree.yaml 的 verify 要同步改成 ≥ 96.5%(9Jang 的檔,要老師／9Jang 改)**;9Jang 的 `lab:verify` 請在實際的隱藏切法上用參考解跑多個 seed,確認最差的 seed 也比 96.5% 高 0.3 個百分點以上;建議 9Jang 改名「不用框架手刻神經網路辨識手寫數字」,或等 AI 層定案後用 `mnist-28`。
15. 理論任務線(hzip)的考卷:tree.yaml 專題 `verify` 裡的「英文參數化考卷」不判零件,寫成 `visibility: teacher` 的驗收檢查(`hzip/boss.exam`),由手算卡的考場出題;9Jang 有考卷型 Boss 之後改成自動。可以自動判的理論驗收(蒙地卡羅對公式、Huffman 對熵)照一般 Boss 寫(`hzip/boss.prob-final`)。
16. 零件檔不能和它的零件庫資料夾同名(例:`hzip/hzip.py`):用 `python3 hzip/hzip.py` 執行時,`import hzip` 會找到檔案自己而不是套件。命令列零件一律叫 `<資料夾>/cli.py`,用 `python3 -m <資料夾>.cli` 執行。
17. C 任務(emu 任務線)的規格標頭:任務多一個書端欄位 `provided`(例 `emu/bus.h`、`chip8/chip8.h`),是規格的一部分。起始碼給這些檔,判題一律用規格版(學生改了也不算);`files` 只列學生要寫的檔(`emu/bits.h`、`emu/bus.c`、`chip8/cpu.c`、`chip8/display.c`)。`require: ["emu/bus.h"]` 的意思是「必須 include 這個標頭,記憶體存取經過 emu/bus」(實際由 MMIO 探針的測試組 `cpu.uses-bus` 判斷)。
18. `bus.ub` 測試組要 9Jang 的 `c-io` runner 支援「同一組案例用 `-fsanitize=undefined,address -fno-sanitize-recover=all` 另外編譯一次」(task.yaml 的組設定加編譯參數);做不到之前,這組先標成只在 `lab:verify` 跑、或暫時拿掉。
19. `chip8/cpu` 的判題連結我們的參考 `display.c`(00E0、DXYN、按鍵事件),因為 `chip8/display` 是下一個任務;`chip8/display` 判題才換成學生的。9Jang 的 `compileSources` 要能放「上游元件以外的參考檔」(或把參考 display 併進驅動程式)。
20. tree.yaml 的 `em-emu-chip8` 先修沒有 `em-c-pointers`,`lab` 說學生用 Python 或 C++;書端定成 C 並且用到 `emu/bus`(同任務線的 order 檢查是過的)。建議 9Jang 把 `em-c-pointers` 加進 `em-emu-chip8` 的先修,並把 `lab` 改成 C。

## 檢查

```bash
python3 _build_routes.py --tree <9Jang>/docs/superpowers/specs/career-skill-tree/tree.yaml --check
```
結構錯誤(id 重複、參照對不到、詳細任務缺公開或隱藏組、效能組沒有 requiredBy 或 requiredBy 裡沒有時限、時限比需求或 budget 寬、order 顛倒、`used_by` 與 `consumes` 不對稱、章 Lab 方框的 `data-task`／`data-group` 不在 yaml、方框少列任務目標、方框的任務目標名稱／〔公開／隱藏檢定〕／效能門檻和 yaml 不同)會讓結束狀態碼非 0;方框的說明和 yaml 不同只列資訊;Lab 方框還沒寫、outline 線的待決只列為「資訊」。
