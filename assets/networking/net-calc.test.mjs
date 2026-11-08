import test from "node:test";
import assert from "node:assert/strict";
import { NetCalc } from "./net-calc.js";

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
