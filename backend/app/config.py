"""Configuration loading and structured logging for the chat-command backend.

The OpenRouter key is read from the environment (or a project-root ``.env``) at
startup, never logged, and never included in :meth:`Settings.for_logging`.
``python-dotenv`` is deliberately not required: a small, strict KEY=VALUE reader
keeps the runtime dependency surface minimal.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, fields, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

DEFAULT_OPENROUTER_MODEL = "openai/gpt-4o-mini"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MAX_CHAT_LENGTH = 500
DEFAULT_RETRY_BASE_DELAY_S = 0.1
DEFAULT_RETRY_MAX_DELAY_S = 0.5
DEFAULT_COMMAND_TIMEOUT_S = 5.0
DEFAULT_BLE_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
DEFAULT_BLE_COMMAND_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

_PROJECT_ROOT = Path(__file__).resolve().parents[2]

_NUMERIC_ENV_KEYS = {
    "BLE_RETRY_BASE_DELAY_S": "retry_base_delay_s",
    "BLE_RETRY_MAX_DELAY_S": "retry_max_delay_s",
    "CHAT_COMMAND_TIMEOUT_S": "command_timeout_s",
    "MAX_CHAT_LENGTH": "max_chat_length",
}
_STRING_ENV_KEYS = {
    "OPENROUTER_API_KEY": "openrouter_api_key",
    "OPENROUTER_MODEL": "openrouter_model",
    "OPENROUTER_BASE_URL": "openrouter_base_url",
    "SPHERO_DEVICE_ADDRESS": "sphero_device_address",
    "BLE_SERVICE_UUID": "ble_service_uuid",
    "BLE_COMMAND_CHARACTERISTIC_UUID": "ble_command_characteristic_uuid",
    "LOG_LEVEL": "log_level",
}


class ConfigError(RuntimeError):
    """Raised when startup configuration is missing or malformed."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated runtime configuration. Secret fields are excluded from logging."""

    openrouter_api_key: str
    openrouter_model: str = DEFAULT_OPENROUTER_MODEL
    openrouter_base_url: str = DEFAULT_OPENROUTER_BASE_URL
    sphero_device_address: str = ""
    ble_service_uuid: str = DEFAULT_BLE_SERVICE_UUID
    ble_command_characteristic_uuid: str = DEFAULT_BLE_COMMAND_CHARACTERISTIC_UUID
    retry_base_delay_s: float = DEFAULT_RETRY_BASE_DELAY_S
    retry_max_delay_s: float = DEFAULT_RETRY_MAX_DELAY_S
    command_timeout_s: float = DEFAULT_COMMAND_TIMEOUT_S
    max_chat_length: int = DEFAULT_MAX_CHAT_LENGTH
    log_level: str = "INFO"

    def for_logging(self) -> dict[str, object]:
        """Return a redacted view safe for structured logs and error messages."""
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if field.name != "openrouter_api_key"
        }

    def __repr__(self) -> str:
        return f"Settings(openrouter_api_key='***', model={self.openrouter_model!r})"

    __str__ = __repr__


def _parse_dotenv(path: Path) -> dict[str, str]:
    """Parse a minimal ``KEY=VALUE`` .env file; comments and blank lines are ignored."""
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return values
    except OSError as exc:
        raise ConfigError(f"could not read .env file {path}: {exc}") from exc

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        values[key] = value.strip().strip('"').strip("'")
    return values


def _coerce_number(key: str, value: str, *, as_int: bool) -> int | float:
    try:
        return int(value) if as_int else float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{key} must be a number, got {value!r}") from exc


def load_settings(
    environ: Mapping[str, str] | None = None,
    env_path: Path | None = None,
    project_root: Path | None = None,
) -> Settings:
    """Build :class:`Settings`, failing fast when the OpenRouter key is absent.

    Values already present in ``environ`` take precedence over ``.env`` values.
    Pass ``env_path=None`` to use ``<project_root>/.env`` (the operator's file).
    """
    root = project_root or _PROJECT_ROOT
    env_file = env_path if env_path is not None else root / ".env"
    environment = dict(os.environ if environ is None else environ)
    file_values = _parse_dotenv(env_file)
    merged = {**file_values, **environment}

    api_key = merged.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise ConfigError(
            "OPENROUTER_API_KEY is missing. Set it in the environment or in .env "
            "at the project root before starting the backend."
        )

    overrides: dict[str, object] = {"openrouter_api_key": api_key}
    for env_key, field_name in _STRING_ENV_KEYS.items():
        if env_key == "OPENROUTER_API_KEY":
            continue
        if env_key in merged:
            overrides[field_name] = merged[env_key]

    for env_key, field_name in _NUMERIC_ENV_KEYS.items():
        if env_key in merged:
            overrides[field_name] = _coerce_number(
                env_key, merged[env_key], as_int=(env_key == "MAX_CHAT_LENGTH")
            )

    settings = replace(Settings(openrouter_api_key=api_key), **overrides)
    if settings.retry_max_delay_s < settings.retry_base_delay_s:
        raise ConfigError("BLE_RETRY_MAX_DELAY_S must be >= BLE_RETRY_BASE_DELAY_S")
    if settings.max_chat_length <= 0:
        raise ConfigError("MAX_CHAT_LENGTH must be positive")
    return settings


_RESERVED_LOG_RECORD_KEYS = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "event",
    "message",
    "asctime",
}


class StructuredJsonFormatter(logging.Formatter):
    """Render log records as one JSON object per line (NFR3.4)."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": getattr(record, "event", None) or record.getMessage(),
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _RESERVED_LOG_RECORD_KEYS and key not in payload:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(level: str = "INFO", logger_name: str = "u1.chat") -> logging.Logger:
    """Attach a single structured handler to ``logger_name`` and return the logger."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level.upper())
    logger.propagate = False
    if not any(isinstance(handler.formatter, StructuredJsonFormatter) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredJsonFormatter())
        logger.addHandler(handler)
    return logger


def log_event(logger: logging.Logger, event: str, **fields: object) -> None:
    """Log a named event with structured context. Never pass secrets as fields."""
    logger.info(event, extra={"event": event, **fields})
