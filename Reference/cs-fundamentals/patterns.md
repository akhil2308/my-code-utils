# Algorithm patterns I keep re-deriving

> _Make this yours: add the trigger phrases that make each pattern click for you._

Most "hard" problems are one of a handful of patterns wearing a costume. Recognize the trigger, recall the template.

## Two pointers
**Trigger:** sorted array / linked list, find a pair/triplet, or compare from both ends.
**Idea:** one pointer from each end (or fast/slow), move based on a comparison. Turns `O(n²)` brute force into `O(n)`.
**Uses:** pair-sum in sorted array, reverse, palindrome check, dedupe in place, cycle detection (Floyd's fast/slow).

## Sliding window
**Trigger:** contiguous subarray/substring, "longest/shortest/at-most-k".
**Idea:** expand the right edge; when the window breaks a constraint, shrink the left edge. Each element enters and leaves once → `O(n)`.
**Uses:** longest substring without repeats, min window covering a set, max sum of size-k.

## Hashing for O(1) lookup
**Trigger:** "have I seen this?", counts, complements.
**Idea:** trade space for time — a set/map turns an inner loop into a lookup.
**Uses:** two-sum (unsorted), group anagrams, dedupe, frequency counts.

## Binary search (incl. on the answer)
**Trigger:** sorted input, OR a monotonic predicate ("is X feasible?" flips false→true once).
**Idea:** halve the search space each step → `O(log n)`. "On the answer": binary-search the *result value*, check feasibility in `O(n)`.
**Uses:** find element, first/last occurrence, "minimum capacity to ship in D days", sqrt.

## BFS / DFS (graphs & trees)
**Trigger:** anything reachability, shortest path in unweighted graph, connected components, levels.
**Idea:** BFS (queue) = shortest path / level order. DFS (stack/recursion) = paths, cycles, topological order, backtracking.
**Uses:** grid islands, shortest hops, dependency ordering (topo sort), tree traversals.

## Heap / top-k
**Trigger:** "k largest/smallest", "k-th", streaming "running median".
**Idea:** a size-k heap keeps the k best in `O(n log k)` instead of sorting everything `O(n log n)`.
**Uses:** top-k frequent, merge k sorted lists, median of a stream (two heaps).

## Dynamic programming
**Trigger:** "count the ways", "min/max cost", overlapping subproblems + optimal substructure.
**Idea:** define the state, the recurrence, and the base case. Memoize (top-down) or build a table (bottom-up).
**Uses:** knapsack, edit distance, longest common subsequence, coin change.

## Backtracking
**Trigger:** generate all combinations/permutations/valid configurations.
**Idea:** DFS the decision tree, prune branches that can't lead to a solution, undo the choice on the way back up.
**Uses:** subsets, permutations, N-queens, sudoku, word search.

## The recognition drill
1. Sorted? → two pointers or binary search.
2. Contiguous subarray/substring? → sliding window.
3. "Have I seen / how many"? → hashing.
4. Graph/tree/grid? → BFS/DFS.
5. "k-th / top-k"? → heap.
6. "Count ways / min cost" with reuse? → DP.
7. "All possible"? → backtracking.
