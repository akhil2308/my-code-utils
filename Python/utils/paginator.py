"""Cursor-based pagination loop. Stdlib only.

Works with any callable that returns (rows, next_cursor):
  - raw SQL via cursor.execute + fetchmany
  - SQLAlchemy queries
  - REST APIs with next-page tokens

Usage:
    from paginator import paginate

    def fetch_page(cursor=None, limit=100):
        # return (rows, next_cursor) — next_cursor=None on last page
        rows = db.query(User).filter(User.id > (cursor or 0)).limit(limit).all()
        next_cursor = rows[-1].id if len(rows) == limit else None
        return rows, next_cursor

    for page in paginate(fetch_page, limit=100):
        process(page)
"""

from collections.abc import Callable, Generator
from typing import Any


def paginate(
    fetch: Callable[..., tuple[list, Any]],
    *,
    limit: int = 100,
    start_cursor: Any = None,
) -> Generator[list, None, None]:
    """Yield pages from a cursor-paginated source.

    fetch(cursor, limit) must return (rows, next_cursor).
    Stops when next_cursor is None or rows is empty.
    """
    cursor = start_cursor
    while True:
        rows, cursor = fetch(cursor, limit)
        if not rows:
            break
        yield rows
        if cursor is None:
            break


def paginate_offset(
    fetch: Callable[..., list],
    *,
    limit: int = 100,
    start: int = 0,
) -> Generator[list, None, None]:
    """Yield pages using offset pagination. Use cursor pagination when possible."""
    offset = start
    while True:
        rows = fetch(offset, limit)
        if not rows:
            break
        yield rows
        if len(rows) < limit:
            break
        offset += limit


if __name__ == "__main__":
    # stub: 250 rows, pages of 100
    _data = list(range(250))

    def mock_fetch(cursor, limit):
        start = cursor or 0
        page = _data[start : start + limit]
        next_cursor = start + limit if start + limit < len(_data) else None
        return page, next_cursor

    pages = list(paginate(mock_fetch, limit=100))
    assert len(pages) == 3
    assert pages[0] == list(range(100))
    assert pages[2] == list(range(200, 250))

    flat = [item for page in pages for item in page]
    assert flat == _data

    # offset variant
    def mock_offset_fetch(offset, limit):
        return _data[offset : offset + limit]

    pages2 = list(paginate_offset(mock_offset_fetch, limit=100))
    assert len(pages2) == 3

    print("self-test passed")
