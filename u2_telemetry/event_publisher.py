"""Async event publisher — fire-and-forget RobotStateChanged events (BR1.4.2, Contract 2).

Publishes RobotStateChanged events on the ``robot.state.changed`` topic using
an in-memory asyncio queue drained by a background publisher coroutine. This
keeps BLE reception non-blocking at up to 10 events/sec (NFR4.2).

Delivery is fire-and-forget: a failed publish is not retried and the next
event overwrites any missed one (Contract 2).
"""

from __future__ import annotations

import asyncio
import logging
from typing import Awaitable, Callable, Optional

from .models import RobotState

logger = logging.getLogger(__name__)

TOPIC = "robot.state.changed"


class EventPublisher:
    """Publishes RobotStateChanged events on the robot.state.changed topic.

    Args:
        topic: Event topic name (default ``robot.state.changed``).
        publish: Async callable ``(topic, state) -> None`` used to deliver
            events. Injected for testing; defaults to a no-op.
    """

    def __init__(
        self,
        topic: str = TOPIC,
        publish: Optional[Callable[[str, RobotState], Awaitable[None]]] = None,
    ) -> None:
        self.topic = topic
        self._publish = publish or self._default_publish
        self._queue: asyncio.Queue[RobotState] = asyncio.Queue()
        self._task: Optional[asyncio.Task[None]] = None
        self._running = False

    async def enqueue(self, state: RobotState) -> None:
        """Enqueue a RobotState for publishing."""
        await self._queue.put(state)

    async def run(self) -> None:
        """Background publisher loop — drains the queue and publishes each event."""
        self._running = True
        while self._running:
            state = await self._queue.get()
            try:
                await self._publish(self.topic, state)
            except Exception:  # noqa: BLE001 - fire-and-forget, no retry
                logger.exception("Publish failed for state %s; fire-and-forget", state.stateId)
            self._queue.task_done()

    async def start(self) -> None:
        """Start the background publisher task."""
        self._task = asyncio.create_task(self.run())

    async def stop(self) -> None:
        """Stop the publisher loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _default_publish(self, topic: str, state: RobotState) -> None:
        """Default no-op publish — overridden by the service wiring."""
        logger.debug("Default publish (no-op) on %s for %s", topic, state.stateId)
