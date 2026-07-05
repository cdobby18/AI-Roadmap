# 3 · Data Structures & Algorithms

The classic CS-fundamentals section — this is what technical interviews actually test, even at AI-focused companies. Every file follows an EASY → MEDIUM → HARD progression in-line (three implementations of the same idea, increasing in realism/optimization), so read top to bottom, not just the last block.

Covers three nested subfolders: `1-basic-structures/`, `2-sorting/`, `3-algorithms/`.

---

## Progress Checklist

### 1-basic-structures/
- [x] `stack.py` — LIFO via `list.append`/`.pop()`; MEDIUM: balanced-parentheses checker; HARD: postfix expression evaluator
- [x] `queue.py` — FIFO via `collections.deque`; MEDIUM: print-job simulation; HARD: circular queue with fixed-size array
- [x] `linkedList.py` — full singly linked list: insert (head/tail), search, delete, display, reverse, find middle (slow/fast pointer), cycle detection (Floyd's)
- [x] `bst.py` — binary search tree: recursive `insert`, `search`, in-order traversal (prints sorted output)
- [x] `heap.py` — `heapq`: push/pop (min-heap), `nlargest`, and a priority queue of `(priority, task)` tuples

### 2-sorting/
- [x] `bubbleSort.py` — naive O(n²) swap-adjacent, then optimized with an early-exit `swapped` flag
- [x] `selectionSort.py` — find min each pass; variant sorts descending; variant finds the kth-smallest via partial selection sort
- [x] `mergeSort.py` — merge two sorted arrays, then full recursive merge sort, then a merge-sort variant that counts inversions (classic interview twist)
- [x] `quickSort.py` — pivot = first element (functional style), then in-place Lomuto partition, then pivot = middle element with a 3-way split (`<`, `==`, `>`)

### 3-algorithms/
- [x] `bruteForce.py` — linear max-finding, brute-force two-sum (O(n²)), and brute-force permutations via `itertools.permutations`
- [x] `fibonacci.py` — three approaches to the same problem: bottom-up array DP, top-down memoized recursion, and O(1)-space iterative
- [x] `coinChange.py` — note: the EASY block is actually iterative Fibonacci (duplicate of `fibonacci.py`'s HARD approach); MEDIUM/HARD are the real coin-change DP — min coins to make an amount (with reconstruction via a `parent` array), and number of ways to make an amount
- [x] `knapsack.py` — 0/1 knapsack: full 2D DP table, then space-optimized 1D DP, then a variant that reconstructs which items were chosen
- [x] `greedyAlgo.py` — greedy coin change (largest-denomination-first), activity selection (sort by finish time), fractional knapsack (sort by value/weight ratio)
- [x] `dijsktraAlgo.py` — Dijkstra's shortest path with `heapq`: distances-only, then with a `previous` map for path reconstruction, then a version returning the actual shortest path to a specific target
- [x] `primsAlgo.py` — Prim's MST: adjacency-list version, adjacency-matrix version, then a version that returns the actual MST edges
- [x] `kruskalAlgo.py` — Kruskal's MST via sort-by-weight + `UnionFind` (disjoint set with path compression); HARD variant just sums MST cost
- [x] `tsp.py` — Traveling Salesman: brute-force over all permutations (exact, exponential), nearest-neighbor heuristic (fast, approximate), and DP with bitmask state (`@lru_cache`, exact but still exponential — just better than brute force)
- [x] `pop.py` — not a graph/search algorithm despite the folder — it's `list.pop()` usage: pop last element, pop by index, and pop-while-iterating (removing even numbers, iterating with a manual index so you don't skip elements after a pop)

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| Big-O of the sorts | Bubble/Selection = O(n²) always; Merge = O(n log n) guaranteed; Quick = O(n log n) average, O(n²) worst case (bad pivot) |
| DP vs Greedy | DP (knapsack, coin change) explores all choices and keeps the best; Greedy (activity selection, fractional knapsack) commits to the locally-best choice and never looks back — only correct when the problem has the greedy-choice property |
| Dijkstra vs Prim vs Kruskal | Dijkstra = shortest path from one source; Prim/Kruskal = minimum spanning tree (connect everything cheaply) — easy to mix up since all three use a min-heap + greedy edge relaxation |
| `heapq` | Python's heap is min-heap only — negate values for a max-heap |
| Fast/slow pointer | One classic trick (`linkedList.py`) solves both "find the middle" and "detect a cycle" |
| Bitmask DP | `tsp.py`'s HARD solution encodes "which cities visited" as bits in an int — a common trick once city/item counts get small (< ~20) |

---

## Gotcha

`pop.py`'s HARD example (`while i < len(arr): ... arr.pop(i) ... else: i += 1`) is the correct pattern for removing items from a list while iterating — incrementing `i` unconditionally after a `pop()` would skip the next element, since everything shifts left.
