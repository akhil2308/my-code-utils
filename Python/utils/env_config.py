"""Environment / config loading. Two patterns: pydantic-settings and stdlib-only.

--- Pattern A: pydantic-settings (install: pip install pydantic-settings) ---

    from env_config import Settings
    cfg = Settings()
    print(cfg.database_url)

Reads from environment and optional .env file automatically.

--- Pattern B: stdlib-only ---

    from env_config import get_config
    cfg = get_config()
    print(cfg["DATABASE_URL"])
"""

from __future__ import annotations

import os

# ── Pattern B: stdlib-only (always available) ────────────────────────────────

_DEFAULTS = {
    "DATABASE_URL": "postgresql://localhost/mydb",
    "REDIS_URL": "redis://localhost:6379/0",
    "SECRET_KEY": "change-me",
    "DEBUG": "false",
    "LOG_LEVEL": "INFO",
    "PORT": "8000",
}


def get_config(defaults: dict | None = None) -> dict:
    """Return config dict merged from defaults → .env file → environment."""
    cfg = dict(_DEFAULTS)
    if defaults:
        cfg.update(defaults)
    _load_dotenv(cfg)
    for key in cfg:
        if key in os.environ:
            cfg[key] = os.environ[key]
    return cfg


def _load_dotenv(cfg: dict) -> None:
    """Minimal .env loader — no deps."""
    try:
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                cfg[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass


# ── Pattern A: pydantic-settings (optional) ──────────────────────────────────

try:
    from pydantic import Field
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        database_url: str = Field("postgresql://localhost/mydb", alias="DATABASE_URL")
        redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")
        secret_key: str = Field("change-me", alias="SECRET_KEY")
        debug: bool = Field(False, alias="DEBUG")
        log_level: str = Field("INFO", alias="LOG_LEVEL")
        port: int = Field(8000, alias="PORT")

        model_config = {"env_file": ".env", "populate_by_name": True}

except ImportError:
    Settings = None  # type: ignore[assignment,misc]  # ponytail: soft dep


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cfg = get_config()
    assert "DATABASE_URL" in cfg
    assert cfg["PORT"] == os.environ.get("PORT", "8000")
    print("stdlib config:", {k: cfg[k] for k in list(cfg)[:3]})

    if Settings is not None:
        s = Settings()
        assert s.port == int(os.environ.get("PORT", 8000))
        print("pydantic config:", s.model_dump())
    else:
        print("pydantic-settings not installed — stdlib path only")

    print("self-test passed")
