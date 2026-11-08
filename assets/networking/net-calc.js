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

  var NetCalc = {
    pick: pick,
    checkAnswer: checkAnswer,
    generators: [c1, c7, c8]
  };

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
