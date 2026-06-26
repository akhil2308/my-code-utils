# Big-O — the stuff I keep re-deriving

> _Make this yours: add the cases that actually trip you up._

## Growth, slowest → fastest

`O(1)` < `O(log n)` < `O(n)` < `O(n log n)` < `O(n²)` < `O(2ⁿ)` < `O(n!)`

Rules of thumb:
- Drop constants and lower-order terms: `O(2n + 5)` → `O(n)`.
- Nested loops over the same input → multiply: two nested → `O(n²)`.
- Halving the problem each step → `log n`. Doing `O(n)` work at each of `log n` levels → `n log n` (that's mergesort / good comparison sorts).
- Recursion: cost = (number of nodes in the call tree) × (work per node). Branching factor `b`, depth `d` → roughly `O(bᵈ)`.

## "What does n look like?" sanity table

| n | An `O(n²)` algo is... |
|---|---|
| 1,000 | fine (~10⁶ ops) |
| 100,000 | borderline (~10¹⁰) — too slow |
| 1,000,000 | hopeless (~10¹²) |

If `n²` is too slow, the target is usually `n log n` (sort + scan) or `n` (hash/two-pointer).

## Data structure costs

| Structure | Access | Search | Insert | Delete | Note |
|---|---|---|---|---|---|
| Array / dynamic array | O(1) | O(n) | O(1)* amortized append | O(n) | *insert in middle is O(n) |
| Hash map | — | O(1) avg | O(1) avg | O(1) avg | O(n) worst (collisions); unordered |
| Balanced BST / tree map | O(log n) | O(log n) | O(log n) | O(log n) | ordered iteration |
| Binary heap | O(1) peek | O(n) | O(log n) | O(log n) pop | priority queue |
| Linked list | O(n) | O(n) | O(1) at known node | O(1) at known node | O(1) splice |
| Stack / queue | — | — | O(1) | O(1) | LIFO / FIFO |

## Space matters too

The recursion stack is space: deep recursion is `O(depth)` memory. Memoization trades space for time — say so out loud when you do it. An "O(n) time" solution that builds an `O(n)` hash isn't free.
