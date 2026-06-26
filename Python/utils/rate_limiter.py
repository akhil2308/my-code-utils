"""Token-bucket rate limiter. Stdlib only.

A bucket holds up to `capacity` tokens and refills at `rate` tokens/sec.
Each call costs one token; no token means rate-limited.

Usage:
    rl = RateLimiter(rate=5, capacity=5)   # 5 req/s, burst of 5
    if rl.try_acquire():
        do_request()                       # allowed
    else:
        ...                                # throttled, drop or retry later

    rl.acquire()                           # blocks until a token is free
"""
import time


class RateLimiter:
    def __init__(self, rate, capacity=None):
        """rate = tokens added per second; capacity = max burst (defaults to rate)."""
        self.rate = float(rate)
        self.capacity = float(capacity if capacity is not None else rate)
        self.tokens = self.capacity
        self.updated = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now

    def try_acquire(self, n=1):
        """Take n tokens if available; return True on success, False if throttled."""
        self._refill()
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

    def acquire(self, n=1):
        """Block until n tokens are available, then take them."""
        while not self.try_acquire(n):
            deficit = n - self.tokens
            time.sleep(deficit / self.rate)   # sleep just long enough to refill the deficit

    # ponytail: not thread-safe. Wrap _refill/token math in a threading.Lock if
    # the same limiter is shared across threads.


if __name__ == "__main__":
    # Self-check: a full bucket allows `capacity` immediate calls, then throttles.
    rl = RateLimiter(rate=10, capacity=3)
    assert rl.try_acquire(), "1st should pass"
    assert rl.try_acquire(), "2nd should pass"
    assert rl.try_acquire(), "3rd should pass"
    assert not rl.try_acquire(), "4th should be throttled (bucket empty)"

    # After waiting one refill period, a token is available again.
    time.sleep(0.11)                          # 10 tokens/s -> ~1 token in 0.1s
    assert rl.try_acquire(), "should refill after waiting"

    # blocking acquire returns within a sane bound
    rl2 = RateLimiter(rate=100, capacity=1)
    rl2.try_acquire()                          # drain
    start = time.monotonic()
    rl2.acquire()                              # must wait ~0.01s for refill
    assert time.monotonic() - start < 0.5, "acquire should not hang"

    print("rate_limiter self-check passed")
