"""FastAPI dependency-injection patterns: settings, DB session, current user.

Dependencies are plain callables passed to `Depends(...)`. FastAPI resolves them
per request, caches the result within a request, and handles cleanup for
generator dependencies (code after `yield`).

    @app.get("/me")
    def me(user = Depends(get_current_user)):
        return user
"""
from functools import lru_cache

from fastapi import Depends, Header, HTTPException


# --- Settings dependency (cached: built once, reused everywhere) ---
class Settings:
    def __init__(self):
        import os
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
        self.api_token = os.getenv("API_TOKEN", "secret-token")


@lru_cache
def get_settings() -> Settings:
    return Settings()


# --- DB session dependency (generator => guaranteed cleanup) ---
def get_db(settings: Settings = Depends(get_settings)):
    # Replace with a real SQLAlchemy SessionLocal(); see Python/sqlalchemy/database.py
    session = {"url": settings.db_url, "open": True}
    try:
        yield session                 # handed to the endpoint
    finally:
        session["open"] = False       # close the session, even on error


# --- Current-user dependency from a bearer token ---
def get_current_user(
    authorization: str = Header(None),
    settings: Settings = Depends(get_settings),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.split(" ", 1)[1]

    # ponytail: static-token lookup. Decode/verify a JWT here for real auth.
    if token != settings.api_token:
        raise HTTPException(status_code=401, detail="invalid token")
    return {"id": 1, "name": "akhil"}


# --- Composed dependency: build on another dependency ---
def require_admin(user: dict = Depends(get_current_user)):
    if user.get("name") != "akhil":
        raise HTTPException(status_code=403, detail="admin only")
    return user
