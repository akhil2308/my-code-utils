# When to use Kafka vs a task queue

> _Make this yours: anchor the trade-offs to the volumes and latencies you run at._

The mistake is treating these as interchangeable "async things." They have different shapes.

## The one-line distinction

- **Task queue** (Celery/RQ/SQS): "do this unit of work, once, then forget it." Job-centric. The message is consumed and gone.
- **Log** (Kafka): "append this event to an ordered, replayable stream that many independent consumers read at their own pace." Event-centric. The message stays.

## Pick a task queue when

- You have **discrete jobs**: send email, resize image, run a report.
- **One logical worker** handles each job; you don't need other systems to also see it.
- You want **per-message ops**: ack/nack, retry, dead-letter, delay/ETA, priority.
- Throughput is moderate (thousands/sec, not millions).
- Example in this repo: [Python/celery/](../../Python/celery/).

## Pick a log (Kafka) when

- You have a **stream of events** many consumers care about (analytics, search index, cache invalidation, audit) — fan-out without the producer knowing the consumers.
- You need **ordering** within a key (partition) and **replay** (a new consumer can read history; reprocess after a bug).
- **High throughput** and durable retention are first-class.
- You're doing **event sourcing / CDC / stream processing**.

## Delivery semantics (the part people get wrong)

- Both default to **at-least-once** → consumers must be **idempotent**. This is non-negotiable; design the consumer to tolerate duplicates (dedupe key, upsert).
- **Exactly-once** is possible in Kafka (transactions) but expensive and narrow; usually "at-least-once + idempotent consumer" is the right, cheaper target.
- Ordering: Kafka guarantees order **per partition**, not globally. Choose the partition key to match the ordering you actually need (e.g. by `user_id`).

## Heuristic

> Need to *run work*? Task queue. Need to *distribute facts* that several systems independently react to, with replay and ordering? Kafka.

If you're reaching for Kafka just to background one job, you've over-built — a task queue (or even SQS) is the lazy correct answer. Reach for Kafka when fan-out, replay, or ordered high-volume streams appear.
