"""
LRU (Least Recently Used) Cache — worked example.

Theory: Notes/system-design-patterns.md -> "eviction policy".

The contract:
- get(key)      -> value or None. A hit makes the key the MOST recently used.
- put(key, val) -> insert/update. If the cache is over capacity, evict the
                   LEAST recently used key.
- Both operations must be O(1).

The classic trick: a hash map gives O(1) lookup but no ordering; a doubly
linked list gives O(1) reordering but no lookup. Combine them and you get
both. Python's OrderedDict is exactly that combination, so we use it here —
in an interview, say that out loud, then offer to build the linked list by
hand if they want to see it.
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: OrderedDict = OrderedDict()

    def get(self, key):
        if key not in self._store:
            return None
        # A read counts as a "use" — move the key to the most-recent end,
        # otherwise it would be evicted as if it were never touched.
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key, value) -> None:
        if key in self._store:
            # Updating an existing key also counts as a use.
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self.capacity:
            # last=False pops the OLDEST entry — the least recently used.
            self._store.popitem(last=False)

    def __len__(self) -> int:
        return len(self._store)

    def __repr__(self) -> str:
        return f"LRUCache({dict(self._store)})"


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    cache = LRUCache(capacity=2)

    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1, "basic get after put"

    # "a" was just read, so "b" is now the least recently used.
    cache.put("c", 3)  # over capacity -> evicts "b"
    assert cache.get("b") is None, "b should have been evicted, not a"
    assert cache.get("a") == 1, "a survived because the get() refreshed it"
    assert cache.get("c") == 3

    # Updating a key refreshes it too.
    cache.put("a", 100)
    cache.put("d", 4)  # evicts "c", not "a"
    assert cache.get("c") is None, "c should be evicted after a was updated"
    assert cache.get("a") == 100

    assert len(cache) == 2
    print("✅ all LRU cache tests passed")
