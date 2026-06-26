"""Async HTTP client with retries, timeout, and JSON shorthand.

Requires: pip install httpx

Usage:
    from http_client import AsyncClient

    async with AsyncClient(base_url="https://api.example.com", token="...") as client:
        data = await client.get_json("/users/1")
        await client.post_json("/users", {"name": "Alice"})
"""

import asyncio
from typing import Any

import httpx


class AsyncClient:
    def __init__(
        self,
        *,
        base_url: str = "",
        token: str | None = None,
        timeout: float = 30.0,
        retries: int = 3,
    ):
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        transport = httpx.AsyncHTTPTransport(retries=retries)
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            transport=transport,
        )

    async def get_json(self, path: str, **kwargs) -> Any:
        r = await self._client.get(path, **kwargs)
        r.raise_for_status()
        return r.json()

    async def post_json(self, path: str, body: Any, **kwargs) -> Any:
        r = await self._client.post(path, json=body, **kwargs)
        r.raise_for_status()
        return r.json()

    async def put_json(self, path: str, body: Any, **kwargs) -> Any:
        r = await self._client.put(path, json=body, **kwargs)
        r.raise_for_status()
        return r.json()

    async def delete(self, path: str, **kwargs) -> httpx.Response:
        r = await self._client.delete(path, **kwargs)
        r.raise_for_status()
        return r

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)


if __name__ == "__main__":
    async def _demo():
        # smoke-test: instantiation and context manager work (no network needed)
        async with AsyncClient(base_url="https://httpbin.org", timeout=5) as client:
            data = await client.get_json("/get")
            assert data["url"] == "https://httpbin.org/get"
            print("GET /get OK:", data["url"])

        print("self-test passed")

    asyncio.run(_demo())
