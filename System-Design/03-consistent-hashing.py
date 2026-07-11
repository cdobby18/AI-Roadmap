"""
Consistent Hashing Ring — guided exercise.

Theory: Notes/system-design-patterns.md -> "consistent hashing".

The problem it solves: with naive `hash(key) % num_nodes`, adding one node
changes `num_nodes`, which remaps almost EVERY key — a full cache wipe on
every scaling event. Consistent hashing places nodes on a circular hash
space (the "ring"); each key belongs to the first node clockwise from the
key's position. Adding/removing a node only moves the keys in its slice.

YOUR TASK — implement the three methods so that:
1. add_node(name): hash the node onto the ring. Use `virtual_nodes` replicas
   per physical node (hash "name#0", "name#1", ...) so keys spread evenly.
2. remove_node(name): remove all of that node's virtual points from the ring.
3. get_node(key): hash the key, then walk clockwise to the first node point
   at or after that position — wrapping around to the start of the ring if
   the key hashes past the last point. Return the PHYSICAL node name.

Hints:
- Keep the ring as a sorted list of (hash_value, node_name) tuples, or use
  a dict plus a sorted list of keys. The `bisect` module does the clockwise
  search in O(log n): `bisect.bisect_right(sorted_hashes, key_hash)`.
- An index equal to len(sorted_hashes) means "wrap to index 0".
- Use the provided `stable_hash` — Python's builtin hash() is randomized
  per process, which would make the self-test flaky.

Run `python 03-consistent-hashing.py` until the self-test passes.
"""

import bisect
import hashlib


def stable_hash(value: str) -> int:
    """Deterministic hash -> integer position on the ring."""
    return int(hashlib.md5(value.encode()).hexdigest(), 16)


class ConsistentHashRing:
    def __init__(self, virtual_nodes: int = 100):
        self.virtual_nodes = virtual_nodes
        # TODO: your ring state here

    def add_node(self, name: str) -> None:
        raise NotImplementedError("implement me — see module docstring")

    def remove_node(self, name: str) -> None:
        raise NotImplementedError("implement me — see module docstring")

    def get_node(self, key: str) -> str:
        raise NotImplementedError("implement me — see module docstring")


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    ring = ConsistentHashRing(virtual_nodes=100)
    for node in ("cache-a", "cache-b", "cache-c"):
        ring.add_node(node)

    keys = [f"user:{i}" for i in range(1000)]

    # Every key maps to some node, deterministically.
    before = {k: ring.get_node(k) for k in keys}
    assert set(before.values()) <= {"cache-a", "cache-b", "cache-c"}
    assert before == {k: ring.get_node(k) for k in keys}, "mapping must be deterministic"

    # Keys spread roughly evenly (virtual nodes make this work).
    counts = {n: list(before.values()).count(n) for n in ("cache-a", "cache-b", "cache-c")}
    assert all(c > 150 for c in counts.values()), f"distribution too skewed: {counts}"

    # THE point of consistent hashing: adding a node remaps only a fraction.
    ring.add_node("cache-d")
    after = {k: ring.get_node(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    assert moved > 0, "the new node should take over some keys"
    assert moved < 500, f"only ~1/4 of keys should move, but {moved}/1000 moved"
    # Keys that moved must have moved TO the new node, nowhere else.
    assert all(after[k] == "cache-d" for k in keys if before[k] != after[k])

    # Removing a node only remaps ITS keys.
    ring.remove_node("cache-d")
    restored = {k: ring.get_node(k) for k in keys}
    assert restored == before, "removing the node must restore the previous mapping"

    print("✅ all consistent-hashing tests passed")
