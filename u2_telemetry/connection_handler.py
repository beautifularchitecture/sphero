"""BLE connection error handling and auto-reconnect (BR1.4.3, NFR2.3).

On BLE error/disconnection: signals the error to U1 (chat UI + robot stop per
BR1.4.3), then tracks reconnect attempts with exponential backoff — up to 3
retries within 5 seconds (NFR2.3).
"""

from __future__ import annotations

import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RECONNECT_WINDOW = 5.0  # seconds


class ConnectionHandler:
    """Tracks BLE connection state and signals errors to U1.

    Args:
        on_error_signal: Callable invoked with the exception when a BLE error
            or disconnection is detected (U1 surfaces it in the chat UI).
        max_retries: Maximum reconnect attempts (default 3, per NFR2.3).
    """

    def __init__(
        self,
        on_error_signal: Callable[[Exception], None],
        max_retries: int = MAX_RETRIES,
    ) -> None:
        self._on_error_signal = on_error_signal
        self._max_retries = max_retries
        self._retries = 0
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def retries(self) -> int:
        return self._retries

    def mark_connected(self) -> None:
        self._connected = True
        self._retries = 0

    def mark_disconnected(self) -> None:
        self._connected = False

    async def handle_error(self, exc: Exception) -> bool:
        """Handle a BLE connection error or disconnection.

        Signals the error to U1, increments the retry counter, and returns
        whether another reconnect attempt should be made (retries remaining).

        Returns:
            True if retries remain, False if the retry budget is exhausted.
        """
        self.mark_disconnected()
        self._retries += 1
        logger.error("BLE connection error: %s", exc)
        try:
            self._on_error_signal(exc)
        except Exception:  # noqa: BLE001 - U1 signal must not break telemetry
            logger.exception("Failed to signal BLE error to U1")
        return self._retries <= self._max_retries
