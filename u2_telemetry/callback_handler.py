"""U1 CommandExecutionStatus sync callback handler (BR1.4.4, Contract 1).

Receives CommandExecutionStatus {commandId, status, timestamp} from U1 via a
synchronous callback. Records each status and correlates it with the
corresponding RobotCommand. If the downstream target is unavailable, telemetry
continues unaffected — best-effort correlation per Contract 1 (NFR2.4).
"""

from __future__ import annotations

import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class CommandStatusCallbackHandler:
    """Handles CommandExecutionStatus callbacks from U1 (Contract 1).

    Args:
        on_status: Optional downstream callable ``(command_id, status, timestamp)
            -> None``. If unavailable, statuses are still recorded locally.
    """

    def __init__(
        self,
        on_status: Optional[Callable[[str, str, str], None]] = None,
    ) -> None:
        self._on_status = on_status
        self.statuses: list[dict[str, str]] = []

    def handle_status(self, command_id: str, status: str, timestamp: str) -> None:
        """Record a CommandExecutionStatus from U1.

        Never raises — if the downstream target is unavailable the error is
        swallowed and telemetry continues (best-effort per Contract 1).
        """
        record = {"commandId": command_id, "status": status, "timestamp": timestamp}
        self.statuses.append(record)
        if self._on_status is not None:
            try:
                self._on_status(command_id, status, timestamp)
            except Exception:  # noqa: BLE001 - callback unavailable, continue
                logger.exception(
                    "U1 status callback failed for command %s", command_id
                )

    def get_status(self, command_id: str) -> Optional[dict[str, str]]:
        """Return the most recent status for a command, or None if not recorded."""
        for record in reversed(self.statuses):
            if record["commandId"] == command_id:
                return record
        return None
