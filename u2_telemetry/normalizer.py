"""Lenient RobotState normalizer (BR1.4.1, BR1.4.5).

Normalizes raw BLE telemetry from the Sphero Mini into a RobotState entity.
Missing or invalid fields are filled with placeholders rather than rejecting
the event (lenient normalization per BR1.4.1). The timestamp is
backend-generated ISO-8601 (BR1.4.5).
"""

from __future__ import annotations

from typing import Any

from .models import RobotState


class RobotStateNormalizer:
    """Normalizes raw BLE telemetry dicts into RobotState entities.

    Never raises on incomplete telemetry — missing fields become dash/null
    placeholders (BR1.4.1).
    """

    def normalize(self, raw_telemetry: dict[str, Any]) -> RobotState:
        """Normalize a raw BLE telemetry dict into a RobotState.

        Args:
            raw_telemetry: Raw telemetry fields from the BLE notification.
                May be partial or empty; missing fields are replaced with
                placeholders.

        Returns:
            A RobotState with all fields populated (placeholders for any
            missing input) and a backend-generated ISO-8601 timestamp.
        """
        return RobotState.create(
            direction=raw_telemetry.get("direction"),
            orientation=raw_telemetry.get("orientation"),
            color=raw_telemetry.get("color"),
            position=raw_telemetry.get("position"),
        )
