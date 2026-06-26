# Caching: patterns and invalidation

> _Make this yours: note which of these you've actually run in prod and what bit you._

> "There are only two hard things in Computer Science: cache invalidation and naming things." — and the first one is why most cache bugs are staleness, not misses.

## First question: why am I caching?

- **Latency** (slow downstream) → cache near the reader.
- **Load** (protect a DB/service) → cache to absorb reads.
- **Cost** (expensive compute / paid API) → cache the result.

If none of these hurt yet, **don't cache** — it adds a consistency problem you didn't have. (YAGNI applies to caches.)

## Read patterns

| Pattern | Who fills the cache | Notes |
|---|---|---|
| **Cache-aside** (lazy) | App: miss → load from DB → put in cache | Default. Simple. Stale until TTL/evict. First read pays the miss. |
| **Read-through** | Cache library loads on miss | Same as aside but hidden behind the cache client. |
| **Write-through** | Write goes to cache + DB synchronously | Cache always fresh; writes slower. |
| **Write-behind** | Write to cache, flush to DB async | Fast writes, risk of loss on crash. Rarely worth it. |

**Default:** cache-aside with a TTL. It's the lazy correct choice for most read-heavy paths.

## Invalidation — pick one deliberately

1. **TTL only.** Simplest. Accept staleness up to the TTL. Great when "a few minutes old" is fine.
2. **Event-driven (explicit invalidation).** On write, delete/update the key. Fresh, but you must catch *every* write path — miss one and you serve stale forever. Combine with a TTL as a safety net.
3. **Versioned keys.** Bake a version into the key (`user:123:v7`); bump the version to invalidate. No deletes, no races; costs key churn.

**Default:** TTL + event-driven delete (delete, don't update — let the next read repopulate). TTL bounds the blast radius of a missed invalidation.

## Failure modes to design for

- **Thundering herd / cache stampede:** many misses hit the DB at once when a hot key expires. Mitigate with a per-key lock ("single-flight") or probabilistic early refresh.
- **Stale-on-error:** if the source is down, serving slightly stale beats erroring.
- **Cache penetration:** repeated misses for non-existent keys hammer the DB → cache the negative result (short TTL).

## What I'd ship

Redis, cache-aside, TTL + delete-on-write, single-flight on the few hottest keys. Skip write-through/behind and versioned keys until a specific consistency requirement forces them.
