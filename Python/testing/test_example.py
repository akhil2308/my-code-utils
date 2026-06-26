"""pytest patterns by example. Fixtures come from conftest.py in this folder.

    pytest -q                       # quiet
    pytest -v                       # verbose, show each test
    pytest test_example.py::test_add  # run a single test
    pytest -k "raises"              # run tests matching a name
    pytest -x                       # stop at first failure
"""
import pytest


def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


# --- plain assertion ---
def test_add():
    assert add(2, 3) == 5


# --- parametrize: one test, many cases ---
@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (0, 5, 5),
    (-1, 1, 0),
])
def test_add_cases(a, b, expected):
    assert add(a, b) == expected


# --- asserting an exception is raised ---
def test_divide_by_zero():
    with pytest.raises(ValueError, match="divide by zero"):
        divide(1, 0)


# --- using a fixture from conftest.py ---
def test_uses_fixture(sample_user):
    assert sample_user["name"] == "akhil"


# --- setup/teardown fixture ---
def test_db_fixture(db):
    db["rows"].append({"x": 1})
    assert len(db["rows"]) == 1


# --- tmp file fixture ---
def test_tmp_config(tmp_config):
    assert "name = demo" in tmp_config.read_text()


# --- parametrized fixture runs this test once per backend ---
def test_backend(backend):
    assert backend in {"sqlite", "postgres"}


# --- monkeypatch: replace a function / env var for the duration of a test ---
def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test-token")
    import os
    assert os.environ["API_TOKEN"] == "test-token"


def test_monkeypatch_func(monkeypatch):
    monkeypatch.setattr("test_example.add", lambda a, b: 999)
    assert add(1, 2) == 999


# --- skip / xfail ---
@pytest.mark.skip(reason="example of skipping")
def test_skipped():
    assert False


@pytest.mark.xfail(reason="known bug, expected to fail")
def test_known_broken():
    assert divide(1, 0)
