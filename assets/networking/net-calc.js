/*
 * NetCalc: calculation-drill generators for the networking exam-prep appendix.
 *
 * Units (global constraint, applies to every generator in this file, including
 * ones appended by later tasks):
 *   1 KB = 1,000 bytes, 1 MB = 1,000,000 bytes, 1 Mbps = 1,000,000 bits/sec.
 *   Decimal, not binary, throughout.
 *
 * Generator shape:
 *   { key, label, bonus,
 *     sample(rand?)  -> params (plain object, final numbers to display),
 *     solve(params)  -> { answer, unit, tolerance, ... },
 *     render(params, solved) -> { promptHTML, stepsHTML } }
 *   `tolerance` is a RELATIVE fraction (0.02 = +/-2%) when `answer` is numeric.
 *   `answer` is per-generator. c7-tdm is the one generator with a two-part
 *   answer: `answer` is [R_Mbps, slot_us] and `unit` is ["Mbps", "µs"].
 *
 * NetCalc.generators is a plain array; later tasks append with .push().
 * Do not freeze it.
 */
(function (global) {
  "use strict";

  function pick(array, rand) {
    return array[Math.floor(rand() * array.length)];
  }

  function fmt(x, digits) {
    return String(Number(x.toFixed(digits === undefined ? 3 : digits)));
  }

  // Relative tolerance check. Never throws; any empty or non-numeric input is false.
  function checkAnswer(userInput, correctAnswer, tolerance) {
    if (typeof userInput !== "string") return false;
    var trimmed = userInput.trim();
    if (trimmed === "") return false;
    var v = Number(trimmed);
    if (!isFinite(v)) return false;
    if (typeof correctAnswer !== "number" || !isFinite(correctAnswer)) return false;
    return Math.abs(v - correctAnswer) <= Math.abs(correctAnswer) * tolerance;
  }

  // ---- C1: Nyquist / Shannon channel capacity -----------------------------

  var B_MHZ = [1, 2, 3, 5, 10, 20];
  var L_VALUES = [2, 4, 8, 16];
  var SNR_DB = [10, 15, 20, 25, 30];

  var c1 = {
    key: "c1-nyquist-shannon",
    label: "C1 Nyquist / Shannon 通道容量",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      var mode = rand() < 0.5 ? "nyquist" : "shannon";
      var B = pick(B_MHZ, rand);
      if (mode === "nyquist") {
        return { mode: mode, B: B, L: pick(L_VALUES, rand) };
      }
      return { mode: mode, B: B, SNR_dB: pick(SNR_DB, rand) };
    },
    solve: function (p) {
      if (p.mode === "nyquist") {
        return {
          answer: 2 * p.B * Math.log2(p.L),
          unit: "Mbps",
          tolerance: 0.02
        };
      }
      var snrLinear = Math.pow(10, p.SNR_dB / 10);
      return {
        answer: p.B * Math.log2(1 + snrLinear),
        unit: "Mbps",
        tolerance: 0.02,
        snrLinear: snrLinear
      };
    },
    render: function (p, s) {
      if (p.mode === "nyquist") {
        return {
          promptHTML: "無雜訊理想通道,頻寬 B = " + p.B + " MHz,訊號有 L = " + p.L +
            " 個層次。求最大資料率(Mbps)。",
          stepsHTML: "Nyquist:2B·log₂L = 2 × " + p.B + " × log₂" + p.L +
            " = " + fmt(s.answer) + " Mbps"
        };
      }
      return {
        promptHTML: "有雜訊通道,頻寬 B = " + p.B + " MHz,SNR = " + p.SNR_dB +
          " dB。求通道容量(Mbps)。",
        stepsHTML: "Shannon:先換算 SNR_linear = 10^(" + p.SNR_dB + "/10) = " +
          fmt(s.snrLinear) + ";再 B·log₂(1+SNR) = " + p.B + " × log₂(1+" +
          fmt(s.snrLinear) + ") = " + fmt(s.answer) + " Mbps"
      };
    }
  };

  // ---- C7: TDM per-channel rate and slot time -----------------------------

  var C_MBPS = [10, 100, 1000];
  var N_CHANNELS = [4, 8, 16, 32];
  var S_BYTES = [64, 128, 256, 512];

  var c7 = {
    key: "c7-tdm",
    label: "C7 TDM 分時多工",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      return {
        C: pick(C_MBPS, rand),
        N: pick(N_CHANNELS, rand),
        s: pick(S_BYTES, rand)
      };
    },
    solve: function (p) {
      var rMbps = p.C / p.N;
      var slotUs = (p.s * 8) / (p.C * 1e6) * 1e6;
      return {
        answer: [rMbps, slotUs],
        unit: ["Mbps", "µs"],
        tolerance: 0.01
      };
    },
    render: function (p, s) {
      return {
        promptHTML: "鏈路容量 C = " + p.C + " Mbps,以 TDM 分給 N = " + p.N +
          " 個通道,每個 slot 大小 s = " + p.s + " bytes。求每個通道的資料率(Mbps)與每個 slot 的時間(µs)。",
        stepsHTML: "每通道速率 R = C / N = " + p.C + " / " + p.N + " = " +
          fmt(s.answer[0]) + " Mbps;slot 時間 = (s × 8) / C = (" + p.s + " × 8) / " +
          p.C + " Mbps = " + fmt(s.answer[1]) + " µs"
      };
    }
  };

  // ---- C8: Slotted ALOHA efficiency ---------------------------------------

  var N_STATIONS = [2, 3, 4, 5, 8];
  var P_FIXED = [0.1, 0.2, 0.25];

  var c8 = {
    key: "c8-slotted-aloha",
    label: "C8 Slotted ALOHA 效率",
    bonus: true,
    sample: function (rand) {
      rand = rand || Math.random;
      var N = pick(N_STATIONS, rand);
      var p = rand() < 0.5 ? pick(P_FIXED, rand) : 1 / N;
      return { N: N, p: p };
    },
    solve: function (p) {
      return {
        answer: p.N * p.p * Math.pow(1 - p.p, p.N - 1),
        unit: "",
        tolerance: 0.05
      };
    },
    render: function (p, s) {
      return {
        promptHTML: "Slotted ALOHA,N = " + p.N + " 個站台,每個站台每個 slot 傳送機率 p = " +
          fmt(p.p, 4) + "。求成功傳送的效率(每個 slot 成功機率)。",
        stepsHTML: "效率 = N·p·(1-p)^(N-1) = " + p.N + " × " + fmt(p.p, 4) +
          " × (1-" + fmt(p.p, 4) + ")^" + (p.N - 1) + " = " + fmt(s.answer, 4)
      };
    }
  };

  // ---- C4: Packet delay (store-and-forward, N hops) ----------------------

  var L_MB = [1, 2, 4, 8];
  var N_HOPS = [1, 2, 3, 4];
  var R_MBPS = [1, 10, 100];
  var DPROP_MS = [1, 2, 5, 10];

  var c4 = {
    key: "c4-packet-delay",
    label: "C4 封包延遲(store-and-forward)",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      return {
        L: pick(L_MB, rand),
        N: pick(N_HOPS, rand),
        R: pick(R_MBPS, rand),
        Dprop: pick(DPROP_MS, rand)
      };
    },
    solve: function (p) {
      // N hops => N+1 links, each contributing one transmission delay and one propagation delay.
      var lBits = p.L * 1e6 * 8;
      var rBps = p.R * 1e6;
      var tTransMs = (lBits / rBps) * 1000;
      return {
        answer: (p.N + 1) * tTransMs + (p.N + 1) * p.Dprop,
        unit: "ms",
        tolerance: 0.02
      };
    },
    render: function (p, s) {
      var tTransMs = (p.L * 1e6 * 8) / (p.R * 1e6) * 1000;
      return {
        promptHTML: "封包大小 L = " + p.L + " MB,經過 N = " + p.N + " 個路由器(hop)," +
          "每條鏈路頻寬 R = " + p.R + " Mbps,每條鏈路傳播延遲 Dprop = " + p.Dprop +
          " ms。求端到端總延遲(ms),忽略排隊延遲。",
        stepsHTML: "鏈路數 = N + 1 = " + (p.N + 1) + ";單鏈路傳輸延遲 = L/R = " +
          fmt(tTransMs) + " ms;總延遲 = (N+1)·(L/R + Dprop) = " + (p.N + 1) + " × (" +
          fmt(tTransMs) + " + " + p.Dprop + ") = " + fmt(s.answer) + " ms"
      };
    }
  };

  // ---- C5: Bandwidth-delay product --------------------------------------

  var R_MBPS_C5 = [1, 10, 100, 1000];
  var RTT_MS = [10, 20, 50, 100, 200];

  var c5 = {
    key: "c5-bdp",
    label: "C5 頻寬延遲乘積(BDP)",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      return {
        R: pick(R_MBPS_C5, rand),
        RTT: pick(RTT_MS, rand)
      };
    },
    solve: function (p) {
      return {
        answer: p.R * 1e6 * (p.RTT / 1000),
        unit: "bits",
        tolerance: 0.02
      };
    },
    render: function (p, s) {
      return {
        promptHTML: "鏈路頻寬 R = " + p.R + " Mbps,往返時間 RTT = " + p.RTT +
          " ms。求頻寬延遲乘積 BDP(bits),即管線中可同時在途的資料量。",
        stepsHTML: "BDP = R × RTT = " + p.R + " Mbps × " + p.RTT + " ms = " +
          p.R + " × 10⁶ bps × " + (p.RTT / 1000) + " s = " + fmt(s.answer, 0) + " bits"
      };
    }
  };

  // ---- C6: TCP window throughput / stop-and-wait efficiency ---------------
  //
  // Two variants share one generator because they share the RTT/R pools and
  // the same "how much of the link do I actually use" framing. `variant` on
  // params picks the formula branch in solve(). Only the "window" variant has
  // a meaningful `isBottleneck`: it answers whether the window size (not the
  // link rate) limits throughput. Stop-and-wait has no window, so the field
  // is intentionally absent there.

  var W_KB = [8, 16, 32, 64];
  var RTT_MS_C6 = [20, 50, 100, 150, 200];
  var R_MBPS_C6 = [1, 10, 100];
  var PACKET_BYTES = [500, 1000, 1500];

  var c6 = {
    key: "c6-tcp-window",
    label: "C6 TCP 視窗吞吐量 / Stop-and-wait 效率",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      if (rand() < 0.5) {
        return {
          variant: "window",
          RTT: pick(RTT_MS_C6, rand),
          W: pick(W_KB, rand),
          R: pick(R_MBPS_C6, rand)
        };
      }
      return {
        variant: "stopwait",
        packetBytes: pick(PACKET_BYTES, rand),
        R: pick(R_MBPS_C6, rand),
        RTT: pick(RTT_MS_C6, rand)
      };
    },
    solve: function (p) {
      if (p.variant === "stopwait") {
        var tTransMs = (p.packetBytes * 8) / (p.R * 1e6) * 1000;
        return {
          answer: tTransMs / (tTransMs + p.RTT),
          unit: "",
          tolerance: 0.02,
          tTransMs: tTransMs
        };
      }
      var throughputMbps = (p.W * 1000 * 8) / (p.RTT / 1000) / 1e6;
      return {
        answer: throughputMbps,
        unit: "Mbps",
        tolerance: 0.02,
        isBottleneck: throughputMbps < p.R
      };
    },
    render: function (p, s) {
      if (p.variant === "stopwait") {
        return {
          promptHTML: "Stop-and-wait,封包大小 = " + p.packetBytes + " bytes,鏈路頻寬 R = " +
            p.R + " Mbps,RTT = " + p.RTT + " ms。求傳送效率(有效傳輸時間佔比)。",
          stepsHTML: "T_trans = 8L/R = " + p.packetBytes + " × 8 / (" + p.R + " × 10⁶) = " +
            fmt(s.tTransMs, 4) + " ms;效率 = T_trans / (T_trans + RTT) = " + fmt(s.tTransMs, 4) +
            " / (" + fmt(s.tTransMs, 4) + " + " + p.RTT + ") = " + fmt(s.answer, 5)
        };
      }
      var bottleneckText = s.isBottleneck
        ? "吞吐量 < 鏈路頻寬,視窗大小是瓶頸"
        : "吞吐量 ≥ 鏈路頻寬,鏈路頻寬是瓶頸";
      return {
        promptHTML: "TCP 視窗 W = " + p.W + " KB,RTT = " + p.RTT + " ms,鏈路頻寬 R = " +
          p.R + " Mbps。求最大吞吐量(Mbps),並判斷瓶頸在視窗還是鏈路。",
        stepsHTML: "吞吐量 = W / RTT = " + p.W + " KB × 8 × 1000 / (" + p.RTT + " ms / 1000) = " +
          fmt(s.answer) + " Mbps;" + bottleneckText
      };
    }
  };

  // ---- C2: CRC remainder / verify (bit-serial GF(2) long division) --------
  //
  // Generator pool is fixed to three r = 3 polynomials. The design doc allows
  // r = 3 or 4; the plan narrows this to r = 3 for the drill.

  var G_CRC = ["1001", "1011", "1101"];

  // Bit-serial GF(2) long division. `bits` and `generator` are "0"/"1" strings.
  // Returns the remainder (last generator.length - 1 chars of the result) and
  // a stepsHTML trace of every XOR performed.
  function mod2Divide(bits, generator) {
    var work = bits.split("");
    var lines = [];
    for (var i = 0; i <= work.length - generator.length; i++) {
      if (work[i] !== "1") continue;
      var before = work.join("");
      for (var j = 0; j < generator.length; j++) {
        work[i + j] = work[i + j] === generator[j] ? "0" : "1";
      }
      lines.push("位置 " + i + ":" + before + " XOR G → " + work.join(""));
    }
    var remainder = work.slice(work.length - (generator.length - 1)).join("");
    return {
      remainder: remainder,
      stepsHTML: lines.length ? lines.join("<br>") : "(被除數開頭皆為 0,無 XOR 步驟)"
    };
  }

  var c2 = {
    key: "c2-crc",
    label: "C2 CRC 餘數 / 檢查",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      var mode = rand() < 0.5 ? "encode" : "verify";
      var G = pick(G_CRC, rand);
      var len = 8 + Math.floor(rand() * 5); // 8..12 data bits
      var D = "";
      for (var i = 0; i < len; i++) D += rand() < 0.5 ? "1" : "0";
      if (mode === "encode") return { mode: mode, D: D, G: G };
      // Verify: build a correct codeword T = D + R, then flip one random bit half the time.
      var R = mod2Divide(D + "0".repeat(G.length - 1), G).remainder;
      var T = D + R;
      if (rand() < 0.5) {
        var pos = Math.floor(rand() * T.length);
        T = T.slice(0, pos) + (T[pos] === "0" ? "1" : "0") + T.slice(pos + 1);
      }
      return { mode: mode, T: T, G: G };
    },
    solve: function (p) {
      var zeros = "0".repeat(p.G.length - 1);
      if (p.mode === "encode") {
        var enc = mod2Divide(p.D + zeros, p.G);
        return {
          answer: enc.remainder,
          unit: "",
          tolerance: 0,
          remainder: enc.remainder,
          stepsHTML: enc.stepsHTML
        };
      }
      var check = mod2Divide(p.T, p.G);
      return {
        answer: check.remainder !== zeros, // true = 有錯
        unit: "",
        tolerance: 0,
        remainder: check.remainder,
        stepsHTML: check.stepsHTML
      };
    },
    render: function (p, s) {
      var r = p.G.length - 1;
      if (p.mode === "encode") {
        return {
          promptHTML: "資料 D = " + p.D + ",生成多項式 G = " + p.G + "(r = " + r +
            ")。求 CRC 餘數 R(" + r + " 位)。",
          stepsHTML: "先在 D 後補 " + r + " 個 0 得 " + p.D + "0".repeat(r) +
            ";做 mod-2 長除法:<br>" + s.stepsHTML + "<br>餘數 R = " + s.remainder
        };
      }
      return {
        promptHTML: "收到的 T = " + p.T + ",生成多項式 G = " + p.G + "。有沒有錯?",
        stepsHTML: "T 除以 G:<br>" + s.stepsHTML + "<br>餘數 = " + s.remainder +
          (s.answer ? ",不為全 0 → 有錯" : ",為全 0 → 沒有錯")
      };
    }
  };

  // ---- C3: CIDR subnetting -------------------------------------------------

  // Standard dotted-quad <-> 32-bit unsigned int. Plain arithmetic (no bitwise
  // ops) so values above 2^31 never go negative.
  function ipToInt(ip) {
    var parts = ip.split(".").map(Number);
    return ((parts[0] * 256 + parts[1]) * 256 + parts[2]) * 256 + parts[3];
  }

  function intToIp(n) {
    return [
      Math.floor(n / 16777216) % 256,
      Math.floor(n / 65536) % 256,
      Math.floor(n / 256) % 256,
      n % 256
    ].join(".");
  }

  var C3_PREFIXES = [16, 20, 22, 24];
  var C3_SUBNET_COUNTS = [2, 4, 8, 16];
  var C3_OCTET1 = [10, 172, 192];

  var c3 = {
    key: "c3-cidr",
    label: "C3 CIDR 子網路劃分",
    bonus: false,
    sample: function (rand) {
      rand = rand || Math.random;
      var prefix = pick(C3_PREFIXES, rand);
      var n = pick(C3_SUBNET_COUNTS, rand);
      var k = 1 + Math.floor(rand() * n); // uniform in [1, n]
      // Random address in a private range, then mask off every host bit so
      // base lands exactly on a /prefix boundary (otherwise the problem is ambiguous).
      var raw = pick(C3_OCTET1, rand) * 16777216 + Math.floor(rand() * 16777216);
      var blockSize = Math.pow(2, 32 - prefix);
      var baseInt = raw - (raw % blockSize);
      return { base: intToIp(baseInt), prefix: prefix, n: n, k: k };
    },
    solve: function (p) {
      var newPrefix = p.prefix + Math.log2(p.n);
      var subnetSize = Math.pow(2, 32 - newPrefix);
      var networkInt = ipToInt(p.base) + (p.k - 1) * subnetSize;
      return {
        answer: {
          networkAddress: intToIp(networkInt),
          broadcastAddress: intToIp(networkInt + subnetSize - 1),
          newPrefix: newPrefix,
          usableHosts: subnetSize - 2
        },
        unit: "",
        tolerance: 0
      };
    },
    render: function (p, s) {
      var a = s.answer;
      return {
        promptHTML: "基底區塊 " + p.base + "/" + p.prefix + ",平均切成 n = " + p.n +
          " 個等大小子網路。求第 k = " + p.k + " 個子網路的網路位址與可用主機數。",
        stepsHTML: "新前綴 = " + p.prefix + " + log₂" + p.n + " = /" + a.newPrefix +
          ";每個子網路大小 = 2^(32-" + a.newPrefix + ") = " + Math.pow(2, 32 - a.newPrefix) +
          ";網路位址 = base + (k-1) × 大小 = " + p.base + " + " + (p.k - 1) + " × " +
          Math.pow(2, 32 - a.newPrefix) + " = " + a.networkAddress +
          ";可用主機 = 大小 - 2 = " + a.usableHosts
      };
    }
  };

  var NetCalc = {
    pick: pick,
    checkAnswer: checkAnswer,
    generators: [c1, c7, c8]
  };

  NetCalc.generators.push(c4, c5, c6);
  NetCalc.generators.push(c2);
  NetCalc.generators.push(c3);

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { NetCalc: NetCalc, mod2Divide: mod2Divide, ipToInt: ipToInt, intToIp: intToIp };
  } else {
    global.NetCalc = NetCalc;
    document.addEventListener("DOMContentLoaded", function () {
      var app = document.getElementById("net-calc-app");
      if (!app) return;

      // fmt/pick/checkAnswer below are the same functions the generators
      // themselves use (ordinary lexical closure access, not window globals).

      function esc(s) {
        return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      }

      var generators = NetCalc.generators;

      function newProblem(gen) {
        var params = gen.sample();
        var solved = gen.solve(params);
        var rendered = gen.render(params, solved);
        return { gen: gen, params: params, solved: solved, rendered: rendered, choice: null };
      }

      var state = { current: newProblem(generators[0]) };

      var bar = document.createElement("div");
      bar.className = "net-toolbar";
      bar.innerHTML =
        '<div class="net-row">' +
        generators.map(function (g, i) {
          return '<button class="net-chip' + (i === 0 ? " active" : "") +
            '" data-gen="' + g.key + '">' + esc(g.label) + (g.bonus ? " (加分)" : "") + "</button>";
        }).join("") +
        "</div>";
      app.appendChild(bar);

      var body = document.createElement("div");
      body.className = "net-calc-body";
      app.appendChild(body);

      // ---- answer-input layout, one branch per answer shape -------------

      function inputRowHTML(cur) {
        var key = cur.gen.key;
        if (key === "c7-tdm") {
          // Two-part answer: [R_Mbps, slot_us].
          return '<div class="net-answer-row">' +
            '<label>頻寬是多少?(Mbps)<input type="text" class="net-answer-input" id="net-ans-0"></label>' +
            '<label>time slot 長度是多少?(µs)<input type="text" class="net-answer-input" id="net-ans-1"></label>' +
            "</div>";
        }
        if (key === "c2-crc") {
          if (cur.params.mode === "encode") {
            // String answer: exact remainder bits.
            return '<div class="net-answer-row">' +
              '<label>CRC 餘數 R(bits)<input type="text" class="net-answer-input" id="net-ans-0" placeholder="例如 011"></label>' +
              "</div>";
          }
          // Boolean answer: yes/no choice, not a free-text input.
          return '<div class="net-answer-row net-choice-row">' +
            '<button class="net-choice-btn" data-choice="true">有錯</button>' +
            '<button class="net-choice-btn" data-choice="false">沒有錯</button>' +
            "</div>";
        }
        if (key === "c3-cidr") {
          // Object answer: {networkAddress, usableHosts}.
          return '<div class="net-answer-row">' +
            '<label>網路位址<input type="text" class="net-answer-input" id="net-ans-0" placeholder="例如 10.0.0.0"></label>' +
            '<label>可用主機數<input type="text" class="net-answer-input" id="net-ans-1"></label>' +
            "</div>";
        }
        // C1, C4, C5, C6, C8: plain-number answer, single input.
        return '<div class="net-answer-row">' +
          '<input type="text" class="net-answer-input" id="net-ans-0" placeholder="輸入答案">' +
          "</div>";
      }

      // ---- correct-answer text shown in the feedback banner -------------

      function answerText(cur) {
        var gen = cur.gen, solved = cur.solved;
        if (gen.key === "c7-tdm") {
          return "正確答案:頻寬 " + fmt(solved.answer[0]) + " Mbps,time slot " +
            fmt(solved.answer[1]) + " µs";
        }
        if (gen.key === "c2-crc") {
          if (typeof solved.answer === "string") return "正確答案:R = " + solved.answer;
          return "正確答案:" + (solved.answer ? "有錯" : "沒有錯");
        }
        if (gen.key === "c3-cidr") {
          return "正確答案:網路位址 " + solved.answer.networkAddress + ",可用主機 " +
            solved.answer.usableHosts;
        }
        return "正確答案:" + fmt(solved.answer) + (solved.unit ? " " + solved.unit : "");
      }

      function renderBody() {
        var cur = state.current;
        var stepsInner = cur.gen.key === "c2-crc"
          ? "<pre>" + cur.rendered.stepsHTML + "</pre>"
          : cur.rendered.stepsHTML;
        body.innerHTML =
          '<div class="net-prompt">' + cur.rendered.promptHTML + "</div>" +
          inputRowHTML(cur) +
          '<div class="net-calc-actions">' +
          '<button class="net-check-btn" data-action="check">檢查答案</button>' +
          '<button class="net-next-btn" data-action="next">🎲 換一題</button>' +
          "</div>" +
          '<div class="net-feedback-slot"></div>' +
          '<details class="solution"><summary>看逐步詳解</summary><div class="sol-body">' +
          stepsInner + "</div></details>";
        // Mirrors toi-render.js: csAddCopy only matters when a <pre> was just
        // inserted (the CRC step trace); it's a no-op otherwise. Deliberately
        // not calling csObserveMath/csObserveHL (not wired for this mount id,
        // no LaTeX/code blocks here).
        if (window.csAddCopy) window.csAddCopy(body);
      }

      renderBody();

      function val(id) {
        var el = document.getElementById(id);
        return el ? el.value : "";
      }

      function showFeedback(ok, extra) {
        var slot = body.querySelector(".net-feedback-slot");
        if (!slot) return;
        slot.innerHTML = '<div class="net-feedback ' + (ok ? "correct" : "wrong") + '">' +
          (ok ? "✅ 答對了!" : "❌ 答錯了,再檢查一下。") +
          (extra ? " " + extra : "") + "</div>";
      }

      function doCheck() {
        var cur = state.current;
        var gen = cur.gen;
        var solved = cur.solved;
        var ok, extra;

        if (gen.key === "c7-tdm") {
          var ok0 = NetCalc.checkAnswer(val("net-ans-0"), solved.answer[0], solved.tolerance);
          var ok1 = NetCalc.checkAnswer(val("net-ans-1"), solved.answer[1], solved.tolerance);
          ok = ok0 && ok1;
          extra = "(頻寬 " + (ok0 ? "✓" : "✗") + "、time slot " + (ok1 ? "✓" : "✗") + ") " + answerText(cur);
        } else if (gen.key === "c2-crc") {
          if (cur.params.mode === "encode") {
            var raw = val("net-ans-0");
            var normalized = (typeof raw === "string" ? raw : "").trim().replace(/\s+/g, "").toLowerCase();
            ok = normalized === String(solved.answer).toLowerCase();
          } else {
            // cur.choice is null until the student clicks a 有錯/沒有錯
            // button; null never equals the boolean answer, so an unanswered
            // check is just "wrong", never a throw.
            ok = cur.choice !== null && cur.choice === solved.answer;
          }
          extra = answerText(cur);
        } else if (gen.key === "c3-cidr") {
          var addrRaw = val("net-ans-0");
          var addrOk = (typeof addrRaw === "string" ? addrRaw : "").trim().toLowerCase() ===
            solved.answer.networkAddress.toLowerCase();
          var hostsOk = NetCalc.checkAnswer(val("net-ans-1"), solved.answer.usableHosts, 0);
          ok = addrOk && hostsOk;
          extra = "(網路位址 " + (addrOk ? "✓" : "✗") + "、可用主機 " + (hostsOk ? "✓" : "✗") + ") " + answerText(cur);
        } else {
          // C1, C4, C5, C6 (both variants), C8: checkAnswer already handles
          // empty/non-numeric input safely, never throws.
          ok = NetCalc.checkAnswer(val("net-ans-0"), solved.answer, solved.tolerance);
          extra = answerText(cur);
        }

        showFeedback(ok, extra);
      }

      bar.querySelectorAll(".net-chip[data-gen]").forEach(function (c) {
        c.addEventListener("click", function () {
          bar.querySelectorAll(".net-chip[data-gen]").forEach(function (x) { x.classList.remove("active"); });
          c.classList.add("active");
          var gen = generators.filter(function (g) { return g.key === c.dataset.gen; })[0];
          state.current = newProblem(gen);
          renderBody();
        });
      });

      body.addEventListener("click", function (e) {
        var btn = e.target.closest("button");
        if (!btn) return;
        if (btn.classList.contains("net-choice-btn")) {
          body.querySelectorAll(".net-choice-btn").forEach(function (b) { b.classList.remove("active"); });
          btn.classList.add("active");
          state.current.choice = btn.dataset.choice === "true";
          return;
        }
        var action = btn.dataset.action;
        if (action === "check") {
          doCheck();
        } else if (action === "next") {
          state.current = newProblem(state.current.gen);
          renderBody();
        }
      });
    });
  }
})(typeof window !== "undefined" ? window : globalThis);
