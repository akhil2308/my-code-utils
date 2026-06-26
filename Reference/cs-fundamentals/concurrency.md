# Concurrency mental models

> _Make this yours: note the concurrency bug that cost you the most and what fixed it._

## Concurrency ≠ parallelism
- **Concurrency:** dealing with many things at once (structure — interleaving tasks).
- **Parallelism:** doing many things at once (execution — multiple cores).
You can be concurrent on one core (async I/O) and parallel without much concurrency (SIMD). Decide which you actually need.

## Pick the model by the bottleneck

| Workload | Use | Why |
|---|---|---|
| **I/O-bound** (network, disk, DB) | async / event loop, or threads | Tasks spend most time waiting; one thread juggles thousands of waits. |
| **CPU-bound** (compute) | multiple processes (or a native/threaded lib that releases the GIL) | Need real cores; one thread = one core of work. |
| **Mixed** | process pool of async workers | Processes for parallelism, async inside each for I/O. |

**Python specifically:** the **GIL** means threads don't give CPU parallelism for pure-Python code — threads help I/O-bound work, `multiprocessing` (or releasing the GIL in C extensions like numpy) helps CPU-bound work. async (`asyncio`) is the lightest tool for high-concurrency I/O. (This is shifting with free-threaded builds, but assume the GIL unless you've verified otherwise.)

## Coordination primitives, shortest version
- **Lock / mutex:** one holder at a time. Guard the *smallest* critical section. Two locks acquired in different orders → **deadlock**; always acquire in a consistent order.
- **Semaphore:** N holders — a bounded pool (e.g. limit concurrent DB connections).
- **Condition variable / event:** wait until something becomes true; signal waiters.
- **Queue:** the safest way to share data between workers — pass messages, don't share mutable state. "Don't communicate by sharing memory; share memory by communicating."

## Locks vs lock-free
- **Locks:** simple, correct, the default. Cost: contention and the risk of deadlock/priority inversion.
- **Lock-free** (atomics, CAS loops): higher throughput under contention, *much* harder to get right. Only reach for it when profiling proves lock contention is the bottleneck — otherwise it's premature.

## The bugs to expect
- **Race condition:** read-modify-write without a lock (the classic `count += 1` from two threads). Fix: make it atomic or guard it.
- **Deadlock:** circular waiting. Fix: lock ordering, or timeouts.
- **Starvation / livelock:** a task never makes progress. Fix: fairness, backoff.
- **Idempotency:** in distributed/at-least-once systems, design handlers to tolerate being run twice — concurrency's cousin.

## Default posture
Prefer **immutability and message-passing** over shared mutable state. When you must share, one lock, smallest section, consistent order. Reach for async for I/O concurrency, processes for CPU parallelism. Everything fancier earns its place with a profile.
