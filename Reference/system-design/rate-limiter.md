# How I'd design a rate limiter

> _Make this yours: replace the defaults with the numbers and trade-offs you actually hit in your systems._

## The question I ask first

"Rate limit" hides three different questions — answer them before picking an algorithm:

1. **What am I protecting?** A downstream dependency (protect it from overload) vs. fairness between tenants vs. abuse/cost control. Different answers → different keys and limits.
2. **What's the key?** Per-IP, per-user, per-API-key, per-endpoint, or a combination. Abuse control wants IP; fairness wants tenant.
3. **Where does it run?** In-process (one node) is trivial but wrong under horizontal scaling — each replica gets its own bucket, so N replicas = N× the limit. Shared state (Redis) is the real answer once you're >1 box.

## Algorithms, shortest useful version

| Algorithm | Mental model | Burst? | Cost |
|---|---|---|---|
| **Token bucket** | Bucket refills at rate R, each request takes a token | Yes, up to bucket size | O(1), 2 numbers (tokens, last-refill) |
| **Leaky bucket** | Queue drains at fixed rate | Smooths bursts away | needs a queue |
| **Fixed window** | Count per wall-clock window | Double-rate at window edges | cheap, 1 counter |
| **Sliding window log** | Timestamps of recent requests | Exact | O(n) memory per key |
| **Sliding window counter** | Weighted blend of current+previous window | Approximates sliding log | O(1), 2 counters |

**Default choice:** token bucket for APIs (allows healthy bursts, simple), sliding-window-counter when you need accuracy without storing every timestamp. Fixed window only when the 2× edge burst is acceptable.

This repo already has a working token bucket: [Python/utils/rate_limiter.py](../../Python/utils/rate_limiter.py).

## Distributed: the actual hard part

- **Shared counter in Redis.** `INCR` + `EXPIRE` for fixed window; a Lua script for atomic token-bucket refill+take (avoids read-modify-write races). One round trip.
- **Clock & atomicity.** Do the time math inside the Lua script (server time) so all replicas agree and the check is atomic.
- **Failure mode — fail open or closed?** If Redis is down: fail *open* (allow) to protect availability, or fail *closed* (deny) to protect the downstream. Pick deliberately; default fail-open with an alarm.
- **Hot keys.** A single huge tenant can hot-spot one Redis shard. Mitigate with local token pre-allocation (grab N tokens at once, spend locally) — trades precision for throughput.

## What I'd actually ship

Token bucket in Redis via Lua, per-API-key, fail-open with alerting, return `429` + `Retry-After`. Add per-endpoint overrides only when one endpoint proves expensive. Skip the leaky-bucket queue and per-IP layer until abuse shows up.
