"""Shared pytest fixtures. pytest auto-discovers this file — no import needed.

    pip install pytest
    pytest -q          # run all tests in this dir

Fixtures defined here are available to every test_*.py in this folder and below.
"""
import pytest


@pytest.fixture
def sample_user():
    """A plain fixture: return a value tests can request by name."""
    return {"id": 1, "name": "akhil", "active": True}


@pytest.fixture
def db():
    """Setup/teardown fixture: code before `yield` runs first, code after runs last."""
    conn = {"rows": []}          # stand-in for a real DB connection
    yield conn                   # the test runs here
    conn["rows"].clear()         # teardown — runs even if the test fails


@pytest.fixture
def tmp_config(tmp_path):
    """Use pytest's built-in tmp_path to write a throwaway file per test."""
    path = tmp_path / "config.ini"
    path.write_text("[app]\nname = demo\n")
    return path


@pytest.fixture(params=["sqlite", "postgres"])
def backend(request):
    """Parametrized fixture: every test using it runs once per param."""
    return request.param
