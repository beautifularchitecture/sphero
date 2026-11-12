"""BDD scenarios for ConnectionHandler (BR1.4.3, NFR2.3).

Given/When/Then scenarios:
- Happy path: mark_connected sets connected=True, resets retries.
- Error/edge: handle_error signals to U1, marks disconnected, retries exhausted → no more retries.
- Edge: retry count increments; max retries boundary; U1 signal failure doesn't break tracking.
"""

from __future__ import annotations

import asyncio

import pytest

from u2_telemetry.connection_handler import ConnectionHandler, MAX_RETRIES


def test_connection_handler_mark_connected_sets_state():
    """Given a ConnectionHandler
    When mark_connected() is called
    Then connected is True and retries are reset to 0."""
    signals = []

    handler = ConnectionHandler(on_error_signal=lambda exc: signals.append(exc))
    handler.mark_disconnected()
    handler._retries = 2
    handler.mark_connected()

    assert handler.connected is True
    assert handler.retries == 0


@pytest.mark.asyncio
async def test_connection_handler_handle_error_signals_u1_and_marks_disconnected():
    """Given a connected ConnectionHandler
    When handle_error() is called with a BLE exception
    Then the error is signaled to U1 and connected becomes False."""
    signals = []

    handler = ConnectionHandler(on_error_signal=lambda exc: signals.append(exc))
    handler.mark_connected()

    result = await handler.handle_error(ConnectionError("link lost"))

    assert handler.connected is False
    assert handler.retries == 1
    assert len(signals) == 1
    assert isinstance(signals[0], ConnectionError)
    assert "link lost" in str(signals[0])
    # Retries remain (1 <= 3) → True.
    assert result is True


@pytest.mark.asyncio
async def test_connection_handler_handle_error_exceeds_max_retries_returns_false():
    """Given a ConnectionHandler at max retries
    When handle_error() is called again
    Then connected is False and the method returns False (no more retries)."""
    signals = []

    handler = ConnectionHandler(on_error_signal=lambda exc: signals.append(exc))
    handler._retries = MAX_RETRIES  # already exhausted

    result = await handler.handle_error(ConnectionError("gone"))

    assert handler.connected is False
    assert handler.retries == MAX_RETRIES + 1
    assert result is False  # no retries remain


@pytest.mark.asyncio
async def test_connection_handler_retries_increment_on_each_error():
    """Given a ConnectionHandler
    When handle_error() is called multiple times
    Then retries increment on each call."""
    handler = ConnectionHandler(on_error_signal=lambda exc: None)

    await handler.handle_error(ConnectionError("e1"))
    await handler.handle_error(ConnectionError("e2"))

    assert handler.retries == 2
    assert handler.connected is False


@pytest.mark.asyncio
async def test_connection_handler_u1_signal_failure_does_not_break_error_handling():
    """Given an on_error_signal that raises
    When handle_error() is called
    Then the error is still tracked (retries increment, connected=False) and no exception propagates."""
    def failing_signal(exc):
        raise RuntimeError("u1 down")

    handler = ConnectionHandler(on_error_signal=failing_signal)

    result = await handler.handle_error(ConnectionError("ble error"))

    assert handler.connected is False
    assert handler.retries == 1
    assert result is True
