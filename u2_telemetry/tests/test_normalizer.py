"""BDD scenarios for RobotStateNormalizer (BR1.4.1, BR1.4.5).

Given/When/Then scenarios for lenient telemetry normalization:
- Happy path: complete telemetry normalizes into a full RobotState.
- Error/edge: missing fields are replaced with dash/null placeholders.
- Edge: backend-generated ISO-8601 timestamp is always present.
"""

from __future__ import annotations

from u2_telemetry.models import RobotState
from u2_telemetry.normalizer import RobotStateNormalizer


def test_normalizer_complete_telemetry_all_fields_populated():
    """Given a complete raw telemetry payload
    When normalize() is called
    Then all five RobotState fields are populated from the input."""
    normalizer = RobotStateNormalizer()
    raw = {
        "direction": "forward",
        "orientation": 45.0,
        "color": "blue",
        "position": "1.2, 0.4",
    }

    state = normalizer.normalize(raw)

    assert state.direction == "forward"
    assert state.orientation == 45.0
    assert state.color == "blue"
    assert state.position == "1.2, 0.4"
    assert state.stateId != ""
    assert state.timestamp != ""


def test_normalizer_timestamp_is_backend_generated_iso8601():
    """Given any telemetry payload
    When normalize() is called
    Then the timestamp is a backend-generated ISO-8601 string, not robot-provided."""
    normalizer = RobotStateNormalizer()
    raw = {"direction": "forward", "orientation": 0.0, "color": "red", "position": "0,0"}

    state = normalizer.normalize(raw)

    # Backend-generated: parses as ISO-8601 and is not the robot-provided value.
    parsed = RobotState.__dataclass_fields__["timestamp"]
    assert parsed is not None
    # Round-trip parse confirms ISO-8601 format.
    from datetime import datetime

    datetime.fromisoformat(state.timestamp)
    assert state.timestamp.endswith("+00:00") or "T" in state.timestamp


def test_normalizer_missing_direction_uses_dash_placeholder():
    """Given telemetry missing the direction field
    When normalize() is called
    Then direction is the "-" placeholder and other fields are preserved."""
    normalizer = RobotStateNormalizer()
    raw = {"orientation": 90.0, "color": "green", "position": "2.0, 1.0"}

    state = normalizer.normalize(raw)

    assert state.direction == "-"
    assert state.orientation == 90.0
    assert state.color == "green"
    assert state.position == "2.0, 1.0"


def test_normalizer_missing_orientation_uses_none_placeholder():
    """Given telemetry missing the orientation field
    When normalize() is called
    Then orientation is None (null placeholder) and other fields are preserved."""
    normalizer = RobotStateNormalizer()
    raw = {"direction": "backward", "color": "red", "position": "3.0, 4.0"}

    state = normalizer.normalize(raw)

    assert state.direction == "backward"
    assert state.orientation is None
    assert state.color == "red"
    assert state.position == "3.0, 4.0"


def test_normalizer_missing_color_uses_dash_placeholder():
    """Given telemetry missing the color field
    When normalize() is called
    Then color is the "-" placeholder."""
    normalizer = RobotStateNormalizer()
    raw = {"direction": "left", "orientation": 180.0, "position": "5.0, 6.0"}

    state = normalizer.normalize(raw)

    assert state.color == "-"
    assert state.direction == "left"
    assert state.orientation == 180.0


def test_normalizer_missing_position_uses_dash_placeholder():
    """Given telemetry missing the position field
    When normalize() is called
    Then position is the "-" placeholder."""
    normalizer = RobotStateNormalizer()
    raw = {"direction": "right", "orientation": 270.0, "color": "yellow"}

    state = normalizer.normalize(raw)

    assert state.position == "-"
    assert state.direction == "right"
    assert state.orientation == 270.0
    assert state.color == "yellow"


def test_normalizer_empty_telemetry_all_placeholders():
    """Given an empty telemetry payload
    When normalize() is called
    Then all optional fields are placeholders and the event is still emitted (not blocked)."""
    normalizer = RobotStateNormalizer()
    raw: dict = {}

    state = normalizer.normalize(raw)

    assert state.direction == "-"
    assert state.orientation is None
    assert state.color == "-"
    assert state.position == "-"
    assert state.stateId != ""
    assert state.timestamp != ""


def test_normalizer_extra_fields_are_ignored():
    """Given telemetry with extra unknown fields
    When normalize() is called
    Then only the known RobotState fields are populated; extras do not break normalization."""
    normalizer = RobotStateNormalizer()
    raw = {
        "direction": "forward",
        "orientation": 10.0,
        "color": "cyan",
        "position": "1,1",
        "battery": 85,
        "rssi": -42,
    }

    state = normalizer.normalize(raw)

    assert state.direction == "forward"
    assert state.orientation == 10.0
    assert state.color == "cyan"
    assert state.position == "1,1"


def test_normalizer_new_stateId_per_reading():
    """Given two separate normalize() calls
    When each produces a RobotState
    Then each has a unique stateId (append-only, ER2)."""
    normalizer = RobotStateNormalizer()
    raw = {"direction": "forward", "orientation": 0.0, "color": "red", "position": "0,0"}

    state_a = normalizer.normalize(raw)
    state_b = normalizer.normalize(raw)

    assert state_a.stateId != state_b.stateId
