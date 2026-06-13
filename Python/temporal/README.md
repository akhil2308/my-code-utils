# Temporal Sample

A minimal [Temporal](https://temporal.io/) example in Python: one activity, one workflow, a worker, and a starter client.

## Files

| File | Purpose |
|------|---------|
| `activities.py` | `say_hello` activity |
| `workflows.py` | `GreetingWorkflow` that calls the activity |
| `worker.py` | Worker polling the `greeting-task-queue` |
| `starter.py` | Client that triggers a workflow run |
| `pyproject.toml` | `uv` project config with `temporalio` dependency |

## Prerequisites

A running Temporal server on `localhost:7233`. Use the compose stack in
[`Docker/temporal-docker`](../../Docker/temporal-docker/docker-compose.yml):

```bash
cd ../../Docker/temporal-docker && docker compose --profile full up -d
```

Web UI: http://localhost:8080

## Run

```bash
uv sync

# terminal 1 — run the worker
uv run python worker.py

# terminal 2 — kick off a workflow
uv run python starter.py     # -> Workflow result: Hello, World!
```
