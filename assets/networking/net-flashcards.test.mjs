import test from "node:test";
import assert from "node:assert/strict";
import { NET_TERMS, NetFlashcards } from "./net-flashcards.js";

test("NET_TERMS has exactly 64 entries covering all 5 layers + cross-layer", () => {
  assert.equal(NET_TERMS.length, 64);
  const layers = new Set(NET_TERMS.map(t => t.layer));
  assert.deepEqual([...layers].sort(), ["app", "cross", "link", "network", "physical", "transport"]);
  assert.equal(new Set(NET_TERMS.map(t => t.id)).size, 64); // no duplicate ids
});

test("filterByLayer returns only the matching layer, 'all' returns everything", () => {
  const net = NetFlashcards.filterByLayer(NET_TERMS, "network");
  assert.ok(net.length > 0);
  assert.ok(net.every(t => t.layer === "network"));
  assert.equal(NetFlashcards.filterByLayer(NET_TERMS, "all").length, NET_TERMS.length);
});

test("markKnown removes the current card for good; markUnknown requeues it", () => {
  let q = NetFlashcards.createQueue(NET_TERMS.slice(0, 3));
  const first = NetFlashcards.current(q);
  q = NetFlashcards.markUnknown(q);
  assert.equal(q.pending.length, 3); // still 3 pending, just reordered
  assert.notEqual(NetFlashcards.current(q).id, first.id); // first card moved to the back
  q = NetFlashcards.markKnown(q); // mark whatever is now current
  assert.equal(q.pending.length, 2);
  assert.equal(q.mastered.length, 1);
});

test("a round cannot complete while any card is still unmastered", () => {
  let q = NetFlashcards.createQueue(NET_TERMS.slice(0, 2));
  assert.equal(NetFlashcards.isRoundComplete(q), false);
  q = NetFlashcards.markUnknown(q);
  assert.equal(NetFlashcards.isRoundComplete(q), false); // Review Focus: 不熟 never completes the round
  q = NetFlashcards.markKnown(q);
  q = NetFlashcards.markKnown(q);
  assert.equal(NetFlashcards.isRoundComplete(q), true);
});
