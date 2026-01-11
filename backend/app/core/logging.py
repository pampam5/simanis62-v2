"""
Logging configuration untuk SIMANIS62 V2.

Menggunakan structured logging (JSON) untuk production,
human-readable format untuk development, dan correlation ID
untuk request tracing.
"""

import contextvars
import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, ClassVar

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from app.core.config import settings

# Context variable untuk correlation ID
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)


class StructuredFormatter(logging.Formatter):
    """JSON formatter untuk structured logging di production."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record sebagai JSON.

        Args:
            record: Log record yang akan diformat

        Returns:
            str: JSON string dari log data
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Tambahkan correlation ID jika ada
        correlation_id = correlation_id_var.get()
        if correlation_id:
            log_data["correlation_id"] = correlation_id

        # Tambahkan extra fields dari record
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Tambahkan exception info jika ada
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Tambahkan location info untuk errors
        if record.levelno >= logging.ERROR:
            log_data["location"] = {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            }

        return json.dumps(log_data, ensure_ascii=False, default=str)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter untuk development dengan colors."""

    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record untuk human-readable output.

        Args:
            record: Log record yang akan diformat

        Returns:
            str: Formatted log string dengan colors
        """
        color = self.COLORS.get(record.levelname, "")
        correlation_id = correlation_id_var.get()

        prefix = f"[{correlation_id[:8]}] " if correlation_id else ""

        return (
            f"{color}{record.levelname:8}{self.RESET} "
            f"{prefix}"
            f"{record.name}:{record.funcName}:{record.lineno} - "
            f"{record.getMessage()}"
        )


def setup_logging(
    level: str | None = None,
    log_file: str | None = None,
    json_format: bool = False,
) -> None:
    """Setup logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to settings.LOG_LEVEL
        log_file: Path ke log file. Defaults to settings.LOG_DIR/simanis62.log
        json_format: Gunakan JSON format (True) atau human-readable (False).
                     Defaults to not settings.DEBUG
    """
    level = level or settings.LOG_LEVEL
    json_format = not settings.DEBUG if json_format is None else json_format

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # === Console Handler ===
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    if json_format:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(HumanReadableFormatter())

    root_logger.addHandler(console_handler)

    # === File Handler dengan rotation ===
    if log_file is None:
        log_dir = Path(settings.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = str(log_dir / "simanis62.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(file_handler)

    # === Error File Handler (Errors only) ===
    error_log_file = Path(log_file).parent / "simanis62_error.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(error_handler)

    # === GlitchTip Integration ===
    if settings.glitchtip_dsn:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above
            event_level=logging.ERROR,  # Send errors to GlitchTip
        )

        sentry_sdk.init(
            dsn=settings.glitchtip_dsn,
            integrations=[sentry_logging],
            environment=settings.glitchtip_environment,
            before_send=filter_sensitive_data,
            traces_sample_rate=0.1,  # 10% performance monitoring
        )

        root_logger.info(
            "GlitchTip integration enabled",
            extra={"environment": settings.glitchtip_environment},
        )

    # === Reduce noise dari library ===
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    root_logger.info(
        "Logging configured",
        extra={
            "level": level,
            "log_file": log_file,
            "json_format": json_format,
            "glitchtip_enabled": bool(settings.glitchtip_dsn),
        },
    )


def filter_sensitive_data(
    event: dict[str, Any], hint: dict[str, Any]
) -> dict[str, Any]:
    """Filter data sensitif sebelum kirim ke GlitchTip.

    Args:
        event: Sentry event dict
        hint: Sentry hint dict

    Returns:
        dict: Filtered event
    """
    # Filter request data
    if "request" in event:
        if "data" in event["request"]:
            event["request"]["data"] = "[FILTERED]"
        if "cookies" in event["request"]:
            event["request"]["cookies"] = "[FILTERED]"
        if "headers" in event["request"]:
            # Keep only safe headers
            safe_headers = ["content-type", "user-agent", "x-correlation-id"]
            event["request"]["headers"] = {
                k: v
                for k, v in event["request"]["headers"].items()
                if k.lower() in safe_headers
            }

    # Filter user data
    if "user" in event:
        if "email" in event["user"]:
            event["user"]["email"] = "[FILTERED]"
        if "username" in event["user"]:
            event["user"]["username"] = "[FILTERED]"

    return event


def get_logger(name: str) -> logging.Logger:
    """Get logger dengan nama spesifik.

    Args:
        name: Nama logger (biasanya __name__)

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
