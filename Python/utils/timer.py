"""Context-manager stopwatch. Stdlib only.

Usage:
    from timer import timer

    with timer("db query"):
        results = db.execute(query)

    # nested
    with timer("total"):
        with timer("step 1"):
            ...
        with timer("step 2"):
            ...
"""

import time
from contextlib import contextmanager


@contextmanager
def timer(label: str = ""):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        tag = f"[{label}] " if label else ""
        print(f"{tag}{elapsed:.4f}s")


if __name__ == "__main__":
    import time as _time

    with timer("sleep 0.1"):
        _time.sleep(0.1)

    results = []
    with timer("list build"):
        results = list(range(1_000_000))

    assert len(results) == 1_000_000
    print("self-test passed")
