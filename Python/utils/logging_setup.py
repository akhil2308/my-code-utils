"""One-call logging setup. Stdlib only.

    from logging_setup import setup_logging
    log = setup_logging("myapp", level="INFO")        # human-readable
    log = setup_logging("myapp", json_logs=True)       # structured JSON (for log shippers)
"""
import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        out = {
            "ts": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            out["exc"] = self.formatException(record.exc_info)
        # include any extra={...} fields passed to the log call
        for k, v in record.__dict__.items():
            if k not in logging.LogRecord("", 0, "", 0, "", (), None).__dict__ and k != "message":
                out[k] = v
        return json.dumps(out)


def setup_logging(name=None, level="INFO", json_logs=False):
    """Configure the root (or named) logger with a single stdout handler. Idempotent."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()  # avoid duplicate handlers on re-call
    handler = logging.StreamHandler(sys.stdout)
    if json_logs:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


if __name__ == "__main__":
    log = setup_logging("demo", level="DEBUG")
    log.info("plain text logging")
    log.warning("with %s", "args")

    jlog = setup_logging("demo.json", json_logs=True)
    jlog.info("structured", extra={"user_id": 42, "action": "login"})

    # Self-check: re-calling doesn't stack handlers.
    again = setup_logging("demo", level="INFO")
    assert len(again.handlers) == 1, "setup should be idempotent"
    print("logging_setup self-check passed")
