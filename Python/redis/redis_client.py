"""Redis basics: connect, get/set, expiry, and pub/sub.

Pairs with the redis-docker stack:  cd Docker/redis-docker && docker compose up -d
Requires:  pip install redis
"""
import redis

# decode_responses=True -> str instead of bytes
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def basics():
    r.set("name", "akhil")
    r.set("session", "token123", ex=60)          # expires in 60s
    print("name      ->", r.get("name"))
    print("session   ->", r.get("session"))
    print("ttl(session) ->", r.ttl("session"))

    r.incr("counter")                            # atomic counter
    r.incr("counter")
    print("counter   ->", r.get("counter"))

    r.rpush("queue", "a", "b", "c")              # list as a queue
    print("pop       ->", r.lpop("queue"))

    r.hset("user:1", mapping={"name": "akhil", "role": "dev"})  # hash
    print("hash      ->", r.hgetall("user:1"))

    r.sadd("tags", "py", "redis", "py")          # set (dedupes)
    print("set       ->", r.smembers("tags"))


def pubsub_demo():
    """Publish/subscribe — usually subscriber runs in a separate process."""
    pubsub = r.pubsub()
    pubsub.subscribe("events")
    r.publish("events", "hello")
    for msg in pubsub.listen():
        if msg["type"] == "message":
            print("received ->", msg["data"])
            break
    pubsub.close()


if __name__ == "__main__":
    try:
        r.ping()
    except redis.ConnectionError:
        raise SystemExit("Redis not reachable on localhost:6379 — start Docker/redis-docker first")
    basics()
    pubsub_demo()
    r.flushdb()  # clean up demo keys
    print("redis_client demo done")
