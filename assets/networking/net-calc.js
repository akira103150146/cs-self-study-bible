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

  var NetCalc = {
    pick: pick,
    checkAnswer: checkAnswer,
    generators: [c1, c7, c8]
  };

  NetCalc.generators.push(c4, c5, c6);

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { NetCalc: NetCalc };
  } else {
    global.NetCalc = NetCalc;
    document.addEventListener("DOMContentLoaded", function () {
      var app = document.getElementById("net-calc-app");
      if (!app) return;
      // DOM mount implemented in Task 7.
    });
  }
})(typeof window !== "undefined" ? window : globalThis);
