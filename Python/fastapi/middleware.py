"""FastAPI middleware patterns: request logging/timing + a simple auth gate.

    from middleware import add_middleware
    app = FastAPI()
    add_middleware(app)

    uvicorn middleware:app --reload   # run this file's demo app directly
"""
import time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")


class TimingMiddleware(BaseHTTPMiddleware):
    """Log every request with its status code and how long it took."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("%s %s -> %d (%.1fms)",
                    request.method, request.url.path, response.status_code, elapsed_ms)
        response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.1f}"
        return response


# ponytail: a static-token check, fine for internal services. Swap for real
# JWT/OAuth verification (see deps.py get_current_user) at a trust boundary.
API_TOKEN = "secret-token"
PUBLIC_PATHS = {"/", "/health", "/docs", "/openapi.json"}


class AuthMiddleware(BaseHTTPMiddleware):
    """Require `Authorization: Bearer <token>` on everything but PUBLIC_PATHS."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in PUBLIC_PATHS:
            auth = request.headers.get("authorization", "")
            if auth != f"Bearer {API_TOKEN}":
                return JSONResponse({"detail": "unauthorized"}, status_code=401)
        return await call_next(request)


def add_middleware(app: FastAPI):
    # Order matters: last added runs first (outermost). Auth before timing here.
    app.add_middleware(TimingMiddleware)
    app.add_middleware(AuthMiddleware)


app = FastAPI()
add_middleware(app)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/secure")
async def secure():
    return {"data": "you are authorized"}
