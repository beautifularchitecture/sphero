"""BDD scenarios for configuration loading and secret protection (NFR9.2, NFR3.4).

These scenarios are the executable specification for ``backend/app/config.py``.
They use an injected environment mapping and a temporary ``.env`` path, so no real
OpenRouter key is required and nothing is read from the operator's environment.
"""

from __future__ import annotations

import json

import pytest

from backend.app import config as config_module
from backend.app.config import (
    ConfigError,
    Settings,
    configure_logging,
    load_settings,
    log_event,
)

VALID_ENVIRONMENT = {
    "OPENROUTER_API_KEY": "sk-or-test-secret-value",
    "OPENROUTER_MODEL": "openai/gpt-4o-mini",
    "SPHERO_DEVICE_ADDRESS": "AA:BB:CC:DD:EE:FF",
}


def test_given_no_api_key_when_loading_settings_then_config_error_names_the_key():
    """Given no OPENROUTER_API_KEY anywhere, When settings load, Then startup fails clearly."""
    # Given
    missing = {"HOME": "/tmp/not-a-key"}
    # When / Then
    with pytest.raises(ConfigError, match="OPENROUTER_API_KEY"):
        load_settings(environ=missing, env_path=None)


def test_given_api_key_in_environment_when_loading_settings_then_key_is_loaded_and_redacted():
    """Given a key in the environment, When settings load, Then it is kept but never rendered."""
    # Given
    environ = dict(VALID_ENVIRONMENT)
    # When
    settings = load_settings(environ=environ, env_path=None)
    # Then
    assert settings.openrouter_api_key == "sk-or-test-secret-value"
    assert "sk-or-test-secret-value" not in repr(settings)
    assert "sk-or-test-secret-value" not in str(settings.for_logging())
    assert "openrouter_api_key" not in settings.for_logging()


def test_given_dotenv_file_when_loading_settings_then_missing_environment_keys_are_filled(
    tmp_path,
):
    """Given a .env file, When the environment lacks the key, Then .env supplies it."""
    # Given
    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_API_KEY=sk-or-from-dotenv\n", encoding="utf-8")
    # When
    settings = load_settings(environ={}, env_path=env_file)
    # Then
    assert settings.openrouter_api_key == "sk-or-from-dotenv"
    assert settings.openrouter_model == config_module.DEFAULT_OPENROUTER_MODEL


def test_given_dotenv_values_when_loading_settings_then_values_are_parsed(
    tmp_path,
):
    """Given a .env with comments, quotes and overrides, When loaded, Then values are parsed."""
    # Given
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# operator secrets",
                "OPENROUTER_API_KEY='sk-or-from-dotenv'",
                'OPENROUTER_MODEL="openai/gpt-4o"',
                "BLE_RETRY_BASE_DELAY_S=0.25",
                "INVALID LINE WITHOUT EQUALS",
                "",
            ]
        ),
        encoding="utf-8",
    )
    # When
    settings = load_settings(environ={}, env_path=env_file)
    # Then
    assert settings.openrouter_api_key == "sk-or-from-dotenv"
    assert settings.openrouter_model == "openai/gpt-4o"
    assert settings.retry_base_delay_s == pytest.approx(0.25)


def test_given_environment_key_when_dotenv_disagrees_then_environment_wins(tmp_path):
    """Given the same key in both places, When settings load, Then the real environment wins."""
    # Given
    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_API_KEY=sk-or-from-file\n", encoding="utf-8")
    # When
    settings = load_settings(
        environ={"OPENROUTER_API_KEY": "sk-or-from-environment"}, env_path=env_file
    )
    # Then
    assert settings.openrouter_api_key == "sk-or-from-environment"


def test_given_invalid_numeric_override_when_loading_settings_then_config_error_names_field():
    """Given a non-numeric retry delay, When settings load, Then the field is named in the error."""
    # Given
    environ = dict(VALID_ENVIRONMENT)
    environ["BLE_RETRY_BASE_DELAY_S"] = "not-a-number"
    # When / Then
    with pytest.raises(ConfigError, match="BLE_RETRY_BASE_DELAY_S"):
        load_settings(environ=environ, env_path=None)


def test_given_api_key_when_structured_logging_is_configured_then_secret_is_absent(
    capsys,
):
    """Given a key in settings, When an event is logged, Then the JSON has no secret field."""
    # Given
    settings = load_settings(environ=dict(VALID_ENVIRONMENT), env_path=None)
    logger = configure_logging(level="DEBUG", logger_name="u1.test.secrets")
    # When
    log_event(logger, "chat_received", **settings.for_logging(), text_length=12)
    # Then
    captured = capsys.readouterr()
    output = captured.err or captured.out
    assert "sk-or-test-secret-value" not in output
    event = json.loads(output.strip().splitlines()[-1])
    assert event["event"] == "chat_received"
    assert event["text_length"] == 12
    assert event["level"] == "INFO"


def test_given_missing_dotenv_file_when_loading_settings_then_environment_only_is_used(
    tmp_path,
):
    """Given no .env on disk, When settings load, Then the environment alone is enough."""
    # Given
    absent = tmp_path / "does-not-exist.env"
    # When
    settings = load_settings(environ=dict(VALID_ENVIRONMENT), env_path=absent)
    # Then
    assert settings.sphero_device_address == "AA:BB:CC:DD:EE:FF"
    assert settings.max_chat_length == config_module.DEFAULT_MAX_CHAT_LENGTH
