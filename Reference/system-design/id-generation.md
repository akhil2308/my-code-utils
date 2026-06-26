# Distributed ID generation

> _Make this yours: record which ID scheme your services actually use and why._

## The trade-off triangle

You usually can't have all three; pick the two that matter:

- **Sortable** (k-sortable by time) — helps DB index locality and "newest first" queries.
- **Decentralized** (generate without coordination) — no single bottleneck.
- **Compact / opaque** — short, and doesn't leak count or timing.

## Options

| Scheme | Bits | Sortable? | Coordination | Leaks |
|---|---|---|---|---|
| **Auto-increment** | DB | Yes | Central (the DB) | Count, sequence |
| **UUIDv4** | 128 | No | None | Nothing |
| **UUIDv7** | 128 | Yes (time-prefixed) | None | Rough timestamp |
| **ULID** | 128 (26-char) | Yes | None | Rough timestamp |
| **Snowflake** | 64 | Yes | Needs worker-id assignment | Timestamp, worker, count |

## How I choose

- **Single DB, no scale concerns?** Auto-increment. Don't invent a distributed ID for a problem you don't have.
- **Need random PKs to avoid index hotspots, don't care about order?** UUIDv4.
- **Want UUID's decentralization *and* time-sortability** (better B-tree locality than v4, "recent" queries)? **UUIDv7** — this is my default for new systems now that it's standardized. ULID if you want the shorter base32 string form.
- **64-bit IDs at very high volume** (storage/index size matters, e.g. tweets)? **Snowflake** — but now you own worker-id assignment and clock-skew handling.

## Gotchas

- **UUIDv4 as a clustered primary key kills write performance** — random inserts fragment the B-tree. v7/ULID/Snowflake fix this by time-prefixing.
- **Snowflake clock skew:** if the clock goes backwards, you can mint duplicate IDs. Need NTP + a refusal-to-go-backwards guard.
- **Don't expose auto-increment IDs externally** — they leak how many records/customers you have and enable enumeration. Use an opaque ID (or a separate public slug) at the boundary.

**Default:** UUIDv7 primary keys. Reach for Snowflake only when 64-bit width or sub-millisecond mint rate genuinely matters.
