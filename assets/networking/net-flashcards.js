(function (global) {
  "use strict";

  var NET_TERMS = [
    // 應用層
    { id: "t01", layer: "app", term: "HTTP", definition: "全球資訊網的應用層協定,採用請求-回應(request-response)模式傳遞網頁內容。" },
    { id: "t02", layer: "app", term: "無狀態協定(Stateless protocol)", definition: "伺服器不會記住先前請求的任何資訊,每個請求都獨立處理;HTTP 本身無狀態,需靠 Cookie 維持狀態。" },
    { id: "t03", layer: "app", term: "Cookie", definition: "伺服器要求瀏覽器儲存的一小段資料,之後每次請求會附帶回傳,用來辨識使用者、維持登入狀態等。" },
    { id: "t04", layer: "app", term: "DNS(網域名稱系統)", definition: "將人類易記的網域名稱轉換成 IP 位址的分散式資料庫系統。" },
    { id: "t05", layer: "app", term: "遞迴查詢 vs 迭代查詢", definition: "遞迴查詢:被問到的伺服器代為向下一台問,直到拿到答案才回覆;迭代查詢:被問到的伺服器只回「下一個該問誰」,由發問端自己繼續問。" },
    { id: "t06", layer: "app", term: "Root / TLD / 權威名稱伺服器", definition: "三層階層式架構:root 伺服器知道各 TLD 伺服器在哪,TLD 伺服器知道該網域的權威伺服器在哪,權威伺服器儲存真正的 DNS 記錄。" },
    { id: "t07", layer: "app", term: "Resolver:stub resolver vs recursive resolver", definition: "stub resolver 是主機上簡單的查詢用戶端,只把問題轉給設定好的 recursive resolver;recursive resolver 代替使用者完整執行查詢流程。" },
    { id: "t08", layer: "app", term: "資源記錄(Resource Record)類型:A / NS / MX / PTR / CNAME", definition: "A 記錄是網域對應的 IPv4 位址;NS 記錄指出該網域的權威伺服器;MX 記錄指出該網域的郵件伺服器;PTR 記錄用於反向查詢(IP 找網域名);CNAME 記錄是別名、指向另一個網域名。" },
    { id: "t09", layer: "app", term: "Zone 與 zone transfer", definition: "zone 是 DNS 階層中由同一組織管理的一段命名空間;zone transfer 是主要伺服器把 zone 資料同步給次要伺服器的過程。" },
    { id: "t10", layer: "app", term: "正向快取 vs 負向快取與 NXDOMAIN", definition: "正向快取存「查到的答案」;負向快取存「查不到」的結果(NXDOMAIN,表示該名稱不存在),避免重複查詢同一個不存在的名稱。" },
    { id: "t11", layer: "app", term: "in-addr.arpa 反向查詢", definition: "把 IP 位址反過來寫成特殊網域名稱,用一般的 DNS 查詢機制查出對應的主機名稱。" },
    { id: "t12", layer: "app", term: "URL", definition: "統一資源定位器,指出資源在網路上的位置(協定、主機、路徑等)。" },
    { id: "t13", layer: "app", term: "Web 快取(代理伺服器)", definition: "代替客戶端儲存先前取得的網頁內容,之後相同請求可直接回應,減少延遲與流量。" },
    { id: "t14", layer: "app", term: "SMTP", definition: "電子郵件在伺服器之間傳遞所使用的應用層協定。" },
    { id: "t15", layer: "app", term: "P2P 架構 vs Client-Server 架構", definition: "P2P 每個節點同時是客戶端與伺服器、沒有一直在線的中心伺服器;Client-Server 客戶端向固定的伺服器請求服務。" },

    // 傳輸層
    { id: "t16", layer: "transport", term: "TCP", definition: "傳輸控制協定,提供可靠、有序、位元流導向、具流量與壅塞控制的連接導向服務。" },
    { id: "t17", layer: "transport", term: "UDP", definition: "使用者資料包協定,無連接、不保證送達與順序,但開銷小、延遲低。" },
    { id: "t18", layer: "transport", term: "連接埠號與多工/解多工", definition: "連接埠號區分同一台主機上不同的應用程式;多工是傳送端把多個 process 的資料加上埠號送出,解多工是接收端依埠號送回正確 process。" },
    { id: "t19", layer: "transport", term: "三向交握(Three-way handshake)", definition: "TCP 建立連線的過程:SYN → SYN+ACK → ACK,雙方交換初始序號以同步。" },
    { id: "t20", layer: "transport", term: "滑動視窗(Sliding window)", definition: "允許傳送端在收到確認前連續送出多個封包,視窗大小決定可同時在途的資料量。" },
    { id: "t21", layer: "transport", term: "流量控制 vs 壅塞控制", definition: "流量控制避免傳送太快讓接收端來不及處理(考慮接收端);壅塞控制避免傳送太快讓網路本身塞住(考慮網路狀況)。" },
    { id: "t22", layer: "transport", term: "累積確認(Cumulative ACK)", definition: "ACK 號碼表示「這個號碼之前的資料都已收到」,不是逐筆確認。" },
    { id: "t23", layer: "transport", term: "Go-Back-N vs Selective Repeat", definition: "Go-Back-N 一旦有封包遺失或逾時,從該封包開始後面全部重傳;Selective Repeat 只重傳真正遺失的那個封包。" },
    { id: "t24", layer: "transport", term: "壅塞視窗(cwnd)與慢啟動(Slow start)", definition: "cwnd 是傳送端依網路壅塞狀況自行調整的視窗;慢啟動階段 cwnd 指數成長,過門檻值後轉線性成長(AIMD)。" },
    { id: "t25", layer: "transport", term: "RTT 與逾時重傳", definition: "RTT 是封包來回一趟的時間;逾時時間依估計 RTT 與其變異動態調整,逾時沒收到 ACK 就重傳。" },
    { id: "t26", layer: "transport", term: "Segment(區段)", definition: "傳輸層的資料單位,TCP/UDP 標頭加上酬載後稱為 segment。" },

    // 網路層
    { id: "t27", layer: "network", term: "IP 位址與子網遮罩", definition: "IP 位址分網路部分與主機部分,子網遮罩決定兩者的分界。" },
    { id: "t28", layer: "network", term: "CIDR", definition: "跳脫傳統 A/B/C 類別的定長網路部分,改用「位址/前綴長度」表示,更彈性地分配位址空間。" },
    { id: "t29", layer: "network", term: "路由(Routing) vs 轉送(Forwarding)", definition: "路由是決定封包該走哪條路徑的全域/長期決策(建立路由表);轉送是路由器收到封包後依路由表送到正確出口的本地/即時動作。" },
    { id: "t30", layer: "network", term: "距離向量 vs 連結狀態", definition: "距離向量:每個節點只跟鄰居交換「自己到各目的地的距離」逐漸收斂(如 RIP);連結狀態:每個節點先取得全網拓樸,再各自用 Dijkstra 算出最短路徑(如 OSPF)。" },
    { id: "t31", layer: "network", term: "自治系統(AS)", definition: "由同一個組織管理、使用同一套內部路由政策的一群網路集合。" },
    { id: "t32", layer: "network", term: "NAT", definition: "網路位址轉換,讓多台使用私有位址的主機共用一個公開 IP 對外連線。" },
    { id: "t33", layer: "network", term: "DHCP", definition: "動態主機設定協定,自動幫新加入網路的主機分配 IP 等設定。" },
    { id: "t34", layer: "network", term: "封包交換 vs 電路交換", definition: "封包交換:資料切成封包各自獨立選路、共享頻寬;電路交換:傳送前先建立專用通道,整段期間獨占頻寬。" },
    { id: "t35", layer: "network", term: "資料包式路由 vs 虛擬電路", definition: "資料包式(datagram routing):每個封包獨立帶完整位址、各自選路(如 IP);虛擬電路(virtual circuit):先建立一條邏輯路徑,之後封包沿同一路徑走、標頭只需簡短的電路編號。" },
    { id: "t36", layer: "network", term: "VC 識別碼:VPI/VCI", definition: "虛擬電路中標示「這個封包屬於哪條虛擬電路」的編號,交換器依此查表轉送,類似簡化版的位址。" },
    { id: "t37", layer: "network", term: "來源路由(Source routing)", definition: "由傳送端事先決定完整路徑,並把整條路徑資訊放進封包標頭,中間節點只需照著走。" },
    { id: "t38", layer: "network", term: "MPLS", definition: "標籤交換技術,在 IP 封包前加一個簡短標籤,讓核心路由器用標籤查表轉送而不必查完整 IP 路由表,兼具電路交換的效率與封包交換的彈性。" },
    { id: "t39", layer: "network", term: "分片(Fragmentation)", definition: "封包大小超過連結 MTU 時,切成多個較小片段分別傳送,到達目的地後再重組。" },
    { id: "t40", layer: "network", term: "TTL", definition: "封包每經過一個路由器就遞減的欄位,到 0 就丟棄,避免封包在迴圈中無限繞行。" },
    { id: "t41", layer: "network", term: "ICMP", definition: "用於回報網路錯誤與診斷(如 ping、traceroute)的網路層輔助協定。" },

    // 資料鏈結層
    { id: "t42", layer: "link", term: "MAC 位址", definition: "燒錄在網路卡上、全球唯一的實體位址,用於同一區域網路內辨識裝置。" },
    { id: "t43", layer: "link", term: "ARP", definition: "位址解析協定,把已知的 IP 位址查出同網段內對應的 MAC 位址。" },
    { id: "t44", layer: "link", term: "CSMA/CD", definition: "載波感測多重存取/碰撞偵測,傳統乙太網路處理共用線路碰撞的機制:先聽再送、邊送邊聽、偵測到碰撞就停止並隨機延遲重送。" },
    { id: "t45", layer: "link", term: "交換器 vs 集線器", definition: "集線器把訊號複製廣播到所有埠;交換器會學習 MAC 位址,只把訊框送到正確的埠。" },
    { id: "t46", layer: "link", term: "Learning bridge(自學習橋接器)", definition: "交換器觀察收到訊框的來源 MAC 位址,記錄「這個位址在哪個埠」,之後同一目的位址就不用再廣播,只送到學到的那個埠。" },
    { id: "t47", layer: "link", term: "Spanning tree algorithm(展開樹演算法)", definition: "多台交換器相連可能形成迴圈導致廣播風暴,展開樹演算法讓交換器們協調出一棵沒有迴圈的樹狀拓樸來轉送訊框(概念上與 Dijkstra 都是「找一棵樹」,但目標不同:一個是最短路徑樹,一個是避免迴圈的生成樹)。" },
    { id: "t48", layer: "link", term: "錯誤偵測:同位檢查 / CRC / Checksum", definition: "同位檢查只能抓奇數個錯誤;CRC 用生成多項式做二進位除法得到餘數,偵錯能力強(乙太網路使用);Checksum 用補數加法,運算簡單但偵錯能力較弱(TCP/IP/UDP 使用)。" },
    { id: "t49", layer: "link", term: "錯誤恢復:FEC vs ARQ", definition: "FEC(前向錯誤更正):傳送端多送冗餘資訊,接收端自己就能更正錯誤,不用重傳;ARQ(自動重傳請求):接收端只偵測錯誤,發現錯就要求重傳。" },
    { id: "t50", layer: "link", term: "訊框(Frame)", definition: "資料鏈結層的資料單位,封包加上鏈結層標頭(含來源/目的 MAC)後稱為訊框。" },
    { id: "t51", layer: "link", term: "位元填塞(Bit stuffing)", definition: "當資料本身恰好出現跟訊框起始/結束標記相同的位元組合時,故意插入額外位元打斷它,避免接收端誤判訊框邊界。" },
    { id: "t52", layer: "link", term: "VLAN", definition: "虛擬區域網路,用邏輯方式把實體交換器的埠劃分成多個獨立的廣播網域。" },

    // 實體層
    { id: "t53", layer: "physical", term: "類比訊號 vs 數位訊號", definition: "類比是連續變化的訊號;數位是離散(通常 0/1)的訊號。" },
    { id: "t54", layer: "physical", term: "導引媒介 vs 非導引媒介", definition: "導引:訊號沿實體介質傳遞(雙絞線、光纖);非導引:訊號透過空間傳播(無線電波)。" },
    { id: "t55", layer: "physical", term: "位元率 vs 鮑率", definition: "鮑率是每秒傳送的訊號符號數;位元率是每秒傳送的位元數,位元率 = 鮑率 × 每符號位元數。" },
    { id: "t56", layer: "physical", term: "數位訊號編碼:NRZ / NRZI / Manchester / 4B/5B", definition: "NRZ(不歸零):0/1 直接對應高/低電壓,長串相同位元時難同步;NRZI:用「訊號是否反轉」表示 0/1;Manchester:每個位元中間一定有一次電壓轉換,方便同步但頻寬效率較低;4B/5B:把 4 個資料位元編碼成 5 個傳輸位元,保證有足夠的訊號轉換次數。" },
    { id: "t57", layer: "physical", term: "Nyquist 定理", definition: "無噪音理想通道下,頻寬 B、L 個訊號層次時,最大資料率為 2B·log₂L。" },
    { id: "t58", layer: "physical", term: "Shannon 定理", definition: "有噪音通道下,頻寬 B、訊號對雜訊比 SNR 時,理論通道容量為 B·log₂(1+SNR)。" },
    { id: "t59", layer: "physical", term: "衰減 vs 雜訊", definition: "衰減是訊號強度隨距離減弱;雜訊是傳輸過程中混入的非預期干擾訊號。" },
    { id: "t60", layer: "physical", term: "多工:TDM / FDM / WDM / CDM", definition: "TDM 分時、FDM 分頻;WDM(分波多工)是光纖世界的 FDM(用不同波長的光同時傳輸);CDM(分碼多工)讓所有使用者同時共用全部頻寬與時間,靠不同的編碼序列區分(行動通訊 CDMA 的基礎)。" },

    // 跨層共用概念
    { id: "t61", layer: "cross", term: "OSI 七層 vs TCP/IP 模型", definition: "OSI 分七層(多展示層、會議層);TCP/IP 實務上簡化成四或五層,兩者在網路層、傳輸層概念基本對應。" },
    { id: "t62", layer: "cross", term: "封裝(Encapsulation)", definition: "資料往下層傳遞時,每層都加上自己的標頭,形成訊息→區段→封包→訊框的過程。" },
    { id: "t63", layer: "cross", term: "端到端原則(End-to-end principle)", definition: "只要功能能由端點正確、完整實作,就不放進網路核心(路由器)做,讓網路保持簡單。" },
    { id: "t64", layer: "cross", term: "延遲的四個組成", definition: "節點處理延遲、佇列延遲、傳輸延遲(= 封包大小/頻寬)、傳播延遲(= 距離/傳播速度)。" }
  ];

  function filterByLayer(terms, layer) {
    if (layer === "all") return terms;
    return terms.filter(function (t) { return t.layer === layer; });
  }

  function createQueue(terms) {
    var pending = terms.slice();
    for (var i = pending.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = pending[i];
      pending[i] = pending[j];
      pending[j] = tmp;
    }
    return { pending: pending, mastered: [] };
  }

  function current(queue) {
    return queue.pending.length > 0 ? queue.pending[0] : null;
  }

  function markKnown(queue) {
    var cur = current(queue);
    if (!cur) return { pending: queue.pending.slice(), mastered: queue.mastered.slice() };
    return {
      pending: queue.pending.slice(1),
      mastered: queue.mastered.concat([cur])
    };
  }

  function markUnknown(queue) {
    var cur = current(queue);
    if (!cur) return { pending: queue.pending.slice(), mastered: queue.mastered.slice() };
    return {
      pending: queue.pending.slice(1).concat([cur]),
      mastered: queue.mastered.slice()
    };
  }

  function isRoundComplete(queue) {
    return queue.pending.length === 0;
  }

  var NetFlashcards = {
    filterByLayer: filterByLayer,
    createQueue: createQueue,
    current: current,
    markKnown: markKnown,
    markUnknown: markUnknown,
    isRoundComplete: isRoundComplete
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { NET_TERMS: NET_TERMS, NetFlashcards: NetFlashcards };
  } else {
    global.NET_TERMS = NET_TERMS;
    global.NetFlashcards = NetFlashcards;
    document.addEventListener("DOMContentLoaded", function () {
      var app = document.getElementById("net-flashcards-app");
      if (!app) return;
      // DOM mount implemented in Task 7.
    });
  }
})(typeof window !== "undefined" ? window : globalThis);
