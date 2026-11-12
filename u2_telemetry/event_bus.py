"""In-process event bus for Contract 2 RobotStateChanged delivery.

Broadcasts normalized ``RobotState`` events to registered subscribers so
events leave the publisher queue and reach U3 StatsDisplay over the WebSocket
endpoint. Pure standard library — no transport dependency — so the bus can be
unit-tested without a running FastAPI/uvicorn server (BR1.4.2, Contract 2).

Delivery is fire-and-forget: a failed publish is not retried and a dead
subscriber is dropped so it cannot stall delivery to others (Contract 2).
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Set

from .models import RobotState

logger = logging.getLogger(__name__)

TOPIC = "robot.state.changed"


class RobotStateEventBus:
    """Broadcasts RobotStateChanged events to registered subscribers.

    Subscribers are awaitable objects exposing ``send_text(str)`` (e.g.
    FastAPI WebSockets). A subscriber that raises is removed so a dead
    connection cannot block delivery to the remaining subscribers.
    """

    def __init__(self) -> None:
        self._subscribers: Set[object] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self, subscriber: object) -> None:
        """Register a subscriber to receive RobotStateChanged events."""
        async with self._lock:
            self._subscribers.add(subscriber)

    async def unsubscribe(self, subscriber: object) -> None:
        """Unregister a subscriber."""
        async with self._lock:
            self._subscribers.discard(subscriber)

    async def publish(self, topic: str, state: RobotState) -> None:
        """Publish a RobotStateChanged event to all subscribers."""
        if topic != TOPIC:
            return
        message = json.dumps({"topic": topic, "state": self._state_payload(state)})
        dead: list[object] = []
        async with self._lock:
            subscribers = list(self._subscribers)
        for subscriber in subscribers:
            try:
                await subscriber.send_text(message)  # type: ignore[attr-defined]
            except Exception:  # noqa: BLE001 - drop dead subscribers
                logger.exception("Event bus subscriber failed; removing")
                dead.append(subscriber)
        for subscriber in dead:
            await self.unsubscribe(subscriber)

    @staticmethod
    def _state_payload(state: RobotState) -> dict:
        return {
            "stateId": state.stateId,
            "correlation_id": state.correlation_id,
            "direction": state.direction,
            "orientation": state.orientation,
            "color": state.color,
            "position": state.position,
            "timestamp": state.timestamp,
        }
