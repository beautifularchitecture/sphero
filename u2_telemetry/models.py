"""RobotState entity — normalized robot telemetry from the Sphero Mini.

Append-only: each reading creates a new stateId; states are never updated
in place (ER2). Missing fields are filled with dash/null placeholders per
BR1.4.1 lenient normalization (ER1).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid


@dataclass
class RobotState:
    """Normalized robot telemetry state at a point in time.

    Attributes:
        stateId: Unique identifier for this telemetry reading.
        direction: Robot direction (e.g. "forward", "north"). "-" when missing.
        orientation: Robot orientation in degrees (0-359). None when missing.
        color: LED color (e.g. "red", "blue"). "-" when missing.
        position: Robot position coordinates (e.g. "1.2, 0.4"). "-" when missing.
        timestamp: Backend-generated ISO-8601 timestamp of the reading.
    """

    stateId: str
    direction: str
    orientation: float | None
    color: str
    position: str
    timestamp: str

    @classmethod
    def create(
        cls,
        direction: str | None = None,
        orientation: float | None = None,
        color: str | None = None,
        position: str | None = None,
        timestamp: str | None = None,
        stateId: str | None = None,
    ) -> "RobotState":
        """Create a RobotState with lenient placeholder defaults.

        Missing fields become dash/None placeholders (BR1.4.1). The timestamp
        is backend-generated ISO-8601 when not supplied (BR1.4.5).
        """
        return cls(
            stateId=stateId or str(uuid.uuid4()),
            direction=direction if direction is not None else "-",
            orientation=orientation if orientation is not None else None,
            color=color if color is not None else "-",
            position=position if position is not None else "-",
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
        )
