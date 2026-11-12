"""BDD scenarios for CommandStatusCallbackHandler (Contract 1, BR1.4.4).

Given/When/Then scenarios:
- Happy path: handle_status records status and correlates by commandId.
- Error/edge: callback unavailable → status still recorded, no exception.
- Edge: multiple statuses for different commands; get_status returns latest.
"""

from __future__ import annotations

from u2_telemetry.callback_handler import CommandStatusCallbackHandler


def test_callback_handler_records_status_and_correlates_by_command_id():
    """Given a CommandStatusCallbackHandler
    When handle_status() is called with a commandId, status, timestamp
    Then the status is recorded and retrievable via get_status(commandId)."""
    handler = CommandStatusCallbackHandler()

    handler.handle_status("cmd-1", "moving", "2026-11-12T10:00:00+00:00")

    record = handler.get_status("cmd-1")
    assert record is not None
    assert record["commandId"] == "cmd-1"
    assert record["status"] == "moving"
    assert record["timestamp"] == "2026-11-12T10:00:00+00:00"


def test_callback_handler_unknown_command_returns_none():
    """Given a handler with no statuses recorded
    When get_status() is called for an unknown commandId
    Then None is returned."""
    handler = CommandStatusCallbackHandler()

    assert handler.get_status("cmd-unknown") is None


def test_callback_handler_callback_unavailable_still_records_status():
    """Given a handler with no downstream on_status callback
    When handle_status() is called
    Then the status is recorded locally and no exception is raised."""
    handler = CommandStatusCallbackHandler(on_status=None)

    handler.handle_status("cmd-2", "stopped", "2026-11-12T10:01:00+00:00")

    record = handler.get_status("cmd-2")
    assert record is not None
    assert record["status"] == "stopped"


def test_callback_handler_downstream_callback_failure_does_not_break_recording():
    """Given a downstream on_status callback that raises
    When handle_status() is called
    Then the status is still recorded and no exception propagates."""

    def failing_callback(command_id, status, timestamp):
        raise RuntimeError("downstream unavailable")

    handler = CommandStatusCallbackHandler(on_status=failing_callback)

    handler.handle_status("cmd-3", "error", "2026-11-12T10:02:00+00:00")

    record = handler.get_status("cmd-3")
    assert record is not None
    assert record["status"] == "error"


def test_callback_handler_multiple_commands_tracked_independently():
    """Given statuses for two different commands
    When get_status() is called for each
    Then each returns its own latest status."""
    handler = CommandStatusCallbackHandler()

    handler.handle_status("cmd-a", "moving", "2026-11-12T10:00:00+00:00")
    handler.handle_status("cmd-b", "stopped", "2026-11-12T10:01:00+00:00")

    assert handler.get_status("cmd-a")["status"] == "moving"
    assert handler.get_status("cmd-b")["status"] == "stopped"


def test_callback_handler_latest_status_wins_for_same_command():
    """Given two statuses for the same commandId
    When get_status() is called
    Then the most recent status is returned."""
    handler = CommandStatusCallbackHandler()

    handler.handle_status("cmd-x", "moving", "2026-11-12T10:00:00+00:00")
    handler.handle_status("cmd-x", "stopped", "2026-11-12T10:01:00+00:00")

    assert handler.get_status("cmd-x")["status"] == "stopped"
    assert handler.get_status("cmd-x")["timestamp"] == "2026-11-12T10:01:00+00:00"
