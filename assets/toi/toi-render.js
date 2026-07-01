/* TOI 題庫渲染器:讀 window.TOI_PROBLEMS(索引+C++解)與 window.TOI_STMT(OCR 題敘),
   提供組別/年份/搜尋過濾,渲染成卡片。 */
(function () {
  function esc(s) {
    return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function yearOf(period) { return (period || "").slice(0, 4); }

  document.addEventListener("DOMContentLoaded", function () {
    var app = document.getElementById("toi-app");
    if (!app || !window.TOI_PROBLEMS) return;
    var P = window.TOI_PROBLEMS;
    var STMT = window.TOI_STMT || {};

    // 年份清單
    var years = []; P.forEach(function (p) { var y = yearOf(p.period); if (y && years.indexOf(y) < 0) years.push(y); });
    years.sort();

    var state = { group: "全部", year: "全部", q: "" };

    // 工具列
    var bar = document.createElement("div");
    bar.className = "toi-toolbar";
    var groups = ["全部", "新手組", "潛力組", "未分類"];
    var chips = groups.map(function (g) {
      return '<button class="toi-chip' + (g === "全部" ? " active" : "") + '" data-group="' + g + '">' + g + "</button>";
    }).join("");
    var yearOpts = ['<option value="全部">全部年份</option>'].concat(
      years.map(function (y) { return '<option value="' + y + '">' + y + "</option>"; })).join("");
    bar.innerHTML =
      '<div class="toi-row">' + chips +
      '<select id="toi-year">' + yearOpts + "</select>" +
      '<input type="text" id="toi-search" placeholder="搜尋題名或代碼…">' +
      "</div><div class='toi-stats' id='toi-stats'></div>";
    app.appendChild(bar);

    var list = document.createElement("div");
    list.id = "toi-list";
    app.appendChild(list);

    function statementHTML(p) {
      var s = STMT[p.key] || STMT[p.token] || STMT[p.code];
      if (s) return s;
      return '<p class="toi-fallback">完整題目敘述請見官方題目 PDF(下方連結)。本書已收錄參考解與分類索引。</p>';
    }

    function cardHTML(p) {
      var links = [];
      if (p.q) links.push('<a href="' + esc(p.q) + '" target="_blank" rel="noopener">📄 官方題目 PDF</a>');
      if (p.a) links.push('<a href="' + esc(p.a) + '" target="_blank" rel="noopener">📊 官方詳解</a>');
      if (p.cppurl) links.push('<a href="' + esc(p.cppurl) + '" target="_blank" rel="noopener">💾 參考解原檔</a>');
      var sol = p.sol
        ? '<details class="solution"><summary>參考解（C++）</summary><div class="sol-body"><pre><code class="language-cpp">' +
          esc(p.sol) + "</code></pre></div></details>"
        : "";
      var gcls = p.group ? "g-" + p.group : "";
      return (
        '<div class="toi-card">' +
        '<div class="toi-head">' +
        '<span class="toi-badge">' + esc(p.period || "—") + "</span>" +
        '<span class="toi-badge ' + gcls + '">' + esc(p.group || "未分類") + "</span>" +
        '<span class="toi-name">' + esc(p.name) + "</span>" +
        (p.token ? '<span class="toi-badge code">' + esc(p.token) + "</span>" : "") +
        "</div>" +
        '<div class="toi-body">' + statementHTML(p) +
        '<div class="toi-links">' + links.join("") + "</div>" +
        sol +
        "</div></div>"
      );
    }

    function render() {
      var q = state.q.trim().toLowerCase();
      var shown = P.filter(function (p) {
        if (state.group !== "全部") {
          var g = p.group || "未分類";
          if (state.group === "未分類" ? g !== "未分類" && g !== "" : g !== state.group) return false;
        }
        if (state.year !== "全部" && yearOf(p.period) !== state.year) return false;
        if (q) {
          var hay = (p.name + " " + p.code + " " + p.token).toLowerCase();
          if (hay.indexOf(q) < 0) return false;
        }
        return true;
      });
      var withStmt = shown.filter(function (p) { return STMT[p.key] || STMT[p.token] || STMT[p.code]; }).length;
      document.getElementById("toi-stats").innerHTML =
        "顯示 <b>" + shown.length + "</b> / " + P.length + " 題　·　其中 " + withStmt + " 題已收錄全文題敘　·　" +
        P.filter(function (p) { return p.sol; }).length + " 題附 C++ 參考解";
      list.innerHTML = shown.length
        ? shown.map(cardHTML).join("")
        : '<div class="toi-empty">沒有符合條件的題目。</div>';
      // 交給 book.js 的延遲系統處理新卡片:複製鈕、進視窗才排版數學、展開才上色程式碼
      if (window.csAddCopy) window.csAddCopy(list);
      if (window.csObserveMath) window.csObserveMath(list.querySelectorAll(".toi-card"));
      if (window.csObserveHL) window.csObserveHL(list);
    }

    bar.querySelectorAll(".toi-chip").forEach(function (c) {
      c.addEventListener("click", function () {
        bar.querySelectorAll(".toi-chip").forEach(function (x) { x.classList.remove("active"); });
        c.classList.add("active"); state.group = c.dataset.group; render();
      });
    });
    document.getElementById("toi-year").addEventListener("change", function (e) { state.year = e.target.value; render(); });
    // 搜尋去抖動(debounce):打字停頓 200ms 才重繪,避免每個字元都重建上百張卡片
    var searchTimer;
    document.getElementById("toi-search").addEventListener("input", function (e) {
      state.q = e.target.value;
      clearTimeout(searchTimer);
      searchTimer = setTimeout(render, 200);
    });

    render();
  });
})();
