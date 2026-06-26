"""Tiny retry decorator with exponential backoff + jitter. Stdlib only.

Usage:
    @retry(tries=4, base=0.5, exc=(ConnectionError,))
    def fetch(): ...
"""
import functools
import random
import time


def retry(tries=3, base=0.5, factor=2.0, max_delay=30.0, jitter=True, exc=(Exception,)):
    """Retry a function on `exc`, sleeping base * factor**attempt between tries.

    Re-raises the last exception once tries are exhausted.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except exc as e:
                    attempt += 1
                    if attempt >= tries:
                        raise
                    delay = min(base * (factor ** (attempt - 1)), max_delay)
                    if jitter:
                        delay *= random.uniform(0.5, 1.5)  # ponytail: full jitter if thundering herd matters
                    print(f"[retry] {fn.__name__} failed ({e!r}); attempt {attempt}/{tries}, sleeping {delay:.2f}s")
                    time.sleep(delay)
        return wrapper
    return decorator


if __name__ == "__main__":
    # Self-check: succeeds on the 3rd try, and exhausts after `tries`.
    calls = {"n": 0}

    @retry(tries=5, base=0.01, jitter=False)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("nope")
        return "ok"

    assert flaky() == "ok", "should eventually succeed"
    assert calls["n"] == 3, f"expected 3 calls, got {calls['n']}"

    @retry(tries=2, base=0.01, jitter=False, exc=(ValueError,))
    def always_fail():
        raise ValueError("boom")

    try:
        always_fail()
        assert False, "should have re-raised"
    except ValueError:
        pass

    print("retry_backoff self-check passed")
