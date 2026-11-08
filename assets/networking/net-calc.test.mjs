import test from "node:test";
import assert from "node:assert/strict";
import { NetCalc, mod2Divide, ipToInt, intToIp } from "./net-calc.js";

function byKey(key) { return NetCalc.generators.find(g => g.key === key); }

test("c1-nyquist-shannon: pinned Nyquist example B=3MHz L=8 -> 18 Mbps", () => {
  const g = byKey("c1-nyquist-shannon");
  const { answer } = g.solve({ mode: "nyquist", B: 3, L: 8 });
  assert.ok(Math.abs(answer - 18) < 1e-9);
});

test("c1-nyquist-shannon: pinned Shannon example B=2MHz SNR=20dB -> ~13.316 Mbps", () => {
  const g = byKey("c1-nyquist-shannon");
  const { answer } = g.solve({ mode: "shannon", B: 2, SNR_dB: 20 });
  assert.ok(Math.abs(answer - 13.3164) < 1e-3);
});

test("c1-nyquist-shannon: sample() params always stay within the declared pools", () => {
  const g = byKey("c1-nyquist-shannon");
  for (let i = 0; i < 200; i++) {
    const p = g.sample();
    assert.ok([1,2,3,5,10,20].includes(p.B));
    if (p.mode === "nyquist") assert.ok([2,4,8,16].includes(p.L));
    else assert.ok([10,15,20,25,30].includes(p.SNR_dB));
  }
});

test("c7-tdm: pinned example C=100Mbps N=8 s=512B -> R=12.5Mbps, slot=40.96us", () => {
  const g = byKey("c7-tdm");
  const { answer } = g.solve({ C: 100, N: 8, s: 512 });
  assert.ok(Math.abs(answer[0] - 12.5) < 1e-9);
  assert.ok(Math.abs(answer[1] - 40.96) < 1e-6);
});

test("c8-slotted-aloha: pinned example N=4 p=0.25 -> efficiency 0.421875", () => {
  const g = byKey("c8-slotted-aloha");
  const { answer } = g.solve({ N: 4, p: 0.25 });
  assert.ok(Math.abs(answer - 0.421875) < 1e-9);
  assert.equal(g.bonus, true);
});

test("c8-slotted-aloha: large N with p=1/N approaches 1/e per the design doc's claim", () => {
  const g = byKey("c8-slotted-aloha");
  const { answer } = g.solve({ N: 1000, p: 1 / 1000 });
  assert.ok(Math.abs(answer - 1 / Math.E) < 0.01);
});

test("checkAnswer: accepts within tolerance, rejects outside it, never throws on bad input (Review Focus)", () => {
  assert.equal(NetCalc.checkAnswer("510000", 500000, 0.02), true);   // +2% exactly at the edge
  assert.equal(NetCalc.checkAnswer("600000", 500000, 0.02), false);  // +20%, outside tolerance
  assert.equal(NetCalc.checkAnswer("abc", 500000, 0.02), false);
  assert.equal(NetCalc.checkAnswer("", 500000, 0.02), false);
  assert.equal(NetCalc.checkAnswer("   ", 500000, 0.02), false);
});

test("c4-packet-delay: pinned example L=2MB N=2 R=10Mbps Dprop=5ms -> 4815 ms", () => {
  const g = byKey("c4-packet-delay");
  const { answer } = g.solve({ L: 2, N: 2, R: 10, Dprop: 5 });
  assert.ok(Math.abs(answer - 4815) < 1e-6);
});

test("c5-bdp: pinned example R=10Mbps RTT=50ms -> 500000 bits", () => {
  const g = byKey("c5-bdp");
  const { answer } = g.solve({ R: 10, RTT: 50 });
  assert.ok(Math.abs(answer - 500000) < 1e-6);
});

test("c6-tcp-window: pinned main example RTT=100ms W=64KB R=10Mbps -> 5.12 Mbps, window IS the bottleneck", () => {
  const g = byKey("c6-tcp-window");
  const { answer, isBottleneck } = g.solve({ variant: "window", RTT: 100, W: 64, R: 10 });
  assert.ok(Math.abs(answer - 5.12) < 1e-6);
  assert.equal(isBottleneck, true);
});

test("c6-tcp-window: pinned stop-and-wait example packet=1500B R=10Mbps RTT=100ms -> efficiency ~0.01186", () => {
  const g = byKey("c6-tcp-window");
  const { answer } = g.solve({ variant: "stopwait", packetBytes: 1500, R: 10, RTT: 100 });
  assert.ok(Math.abs(answer - 0.011857) < 1e-5);
});

test("mod2Divide: pinned textbook example D=101110 G=1001 -> remainder 011", () => {
  const { remainder } = mod2Divide("101110" + "000", "1001");
  assert.equal(remainder, "011");
});

test("c2-crc encode mode: pinned example produces R=011", () => {
  const g = byKey("c2-crc");
  const { answer } = g.solve({ mode: "encode", D: "101110", G: "1001" });
  assert.equal(answer, "011");
});

test("c2-crc verify mode: an untouched codeword always verifies clean", () => {
  const g = byKey("c2-crc");
  const { answer } = g.solve({ mode: "verify", T: "101110011", G: "1001" });
  assert.equal(answer, false); // false = 沒有錯
});

test("c2-crc verify mode: flipping ANY single bit of the codeword is always detected (Review Focus)", () => {
  const g = byKey("c2-crc");
  const codeword = "101110011";
  for (let i = 0; i < codeword.length; i++) {
    const flipped = codeword.slice(0, i) + (codeword[i] === "0" ? "1" : "0") + codeword.slice(i + 1);
    const { answer } = g.solve({ mode: "verify", T: flipped, G: "1001" });
    assert.equal(answer, true, `bit ${i} flip should have been detected`);
  }
});

test("c2-crc sample(): D/T length always 8-12 bits and G from the fixed 3-option pool", () => {
  const g = byKey("c2-crc");
  for (let i = 0; i < 100; i++) {
    const p = g.sample();
    const bits = p.mode === "encode" ? p.D : p.T;
    assert.ok(bits.length >= 8 && bits.length <= 12 + 3); // T includes the r appended check bits
    assert.ok(["1001", "1011", "1101"].includes(p.G));
  }
});

test("ipToInt/intToIp round-trip", () => {
  assert.equal(ipToInt("192.168.17.0"), ipToInt("192.168.16.0") + 256);
  assert.equal(intToIp(ipToInt("10.0.0.1")), "10.0.0.1");
});

test("c3-cidr: pinned example base=192.168.16.0/22 n=8 k=3 -> 192.168.17.0, 126 usable hosts", () => {
  const g = byKey("c3-cidr");
  const { answer } = g.solve({ base: "192.168.16.0", prefix: 22, n: 8, k: 3 });
  assert.equal(answer.networkAddress, "192.168.17.0");
  assert.equal(answer.usableHosts, 126);
});

test("c3-cidr: k=1 (first subnet) equals the base address exactly (Review Focus boundary)", () => {
  const g = byKey("c3-cidr");
  const { answer } = g.solve({ base: "192.168.16.0", prefix: 22, n: 8, k: 1 });
  assert.equal(answer.networkAddress, "192.168.16.0");
});

test("c3-cidr: k=n (last subnet) stays inside the original block (Review Focus boundary)", () => {
  const g = byKey("c3-cidr");
  const { answer } = g.solve({ base: "192.168.16.0", prefix: 22, n: 8, k: 8 });
  assert.equal(answer.networkAddress, "192.168.19.128");
  const blockEnd = ipToInt("192.168.16.0") + 2 ** (32 - 22) - 1; // last address of the original /22
  assert.ok(ipToInt(answer.networkAddress) + 128 - 1 <= blockEnd);
});

test("c3-cidr: all n subnets from sample() are contiguous, non-overlapping, and within the base block", () => {
  const g = byKey("c3-cidr");
  for (let trial = 0; trial < 50; trial++) {
    const p = g.sample();
    const subnetSize = 2 ** (32 - (p.prefix + Math.log2(p.n)));
    let prevEnd = ipToInt(p.base) - 1;
    for (let k = 1; k <= p.n; k++) {
      const { answer } = g.solve({ ...p, k });
      const start = ipToInt(answer.networkAddress);
      assert.equal(start, prevEnd + 1); // contiguous, no gap or overlap
      prevEnd = start + subnetSize - 1;
    }
    assert.ok(prevEnd <= ipToInt(p.base) + 2 ** (32 - p.prefix) - 1); // stays inside the /prefix block
  }
});
