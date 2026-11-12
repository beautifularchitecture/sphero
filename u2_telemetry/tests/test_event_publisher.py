"""BDD scenarios for EventPublisher (Contract 2, fire-and-forget publish).

Given/When/Then scenarios:
- Happy path: enqueue → background publisher drains queue → publish on topic.
- Error/edge: publish failure is fire-and-forget (no retry, next event still published).
- Edge: start/stop lifecycle; multiple events published in order.
"""

from __future__ import annotations

import asyncio

import pytest

from u2_telemetry.event_publisher import EventPublisher, TOPIC
from u2_telemetry.models import RobotState


def make_state(direction: str = "forward") -> RobotState:
    return RobotState(
        stateId="state-1",
        direction=direction,
        orientation=0.0,
        color="red",
        position="0,0",
        timestamp="2026-11-12T00:00:00+00:00",
    )


@pytest.fixture
def published_events():
    return []


@pytest.mark.asyncio
async def test_event_publisher_enqueue_drains_and_publishes_on_topic(published_events):
    """Given an EventPublisher with a capture publish callable
    When a state is enqueued and the publisher loop runs
    Then the event is published on the robot.state.changed topic."""

    async def publish(topic, state):
        published_events.append((topic, state))

    pub = EventPublisher(topic=TOPIC, publish=publish)
    await pub.start()
    await pub.enqueue(make_state())
    await asyncio.sleep(0.05)  # let the publisher loop drain
    await pub.stop()

    assert len(published_events) == 1
    topic, state = published_events[0]
    assert topic == TOPIC
    assert state.direction == "forward"


@pytest.mark.asyncio
async def test_event_publisher_multiple_events_published_in_order(published_events):
    """Given several states enqueued in sequence
    When the publisher loop drains the queue
    Then events are published in the same order they were enqueued."""

    async def publish(topic, state):
        published_events.append((topic, state.direction))

    pub = EventPublisher(topic=TOPIC, publish=publish)
    await pub.start()
    await pub.enqueue(make_state("forward"))
    await pub.enqueue(make_state("backward"))
    await pub.enqueue(make_state("left"))
    await asyncio.sleep(0.05)
    await pub.stop()

    assert [d for _, d in published_events] == ["forward", "backward", "left"]


@pytest.mark.asyncio
async def test_event_publisher_publish_failure_is_fire_and_forget(published_events):
    """Given a publish callable that raises on the first call
    When the first event fails to publish
    Then no exception propagates and the next event is still published (no retry)."""

    call_count = {"n": 0}

    async def publish(topic, state):
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise RuntimeError("broker down")
        published_events.append(state.direction)

    pub = EventPublisher(topic=TOPIC, publish=publish)
    await pub.start()
    await pub.enqueue(make_state("forward"))
    await pub.enqueue(make_state("backward"))
    await asyncio.sleep(0.1)
    await pub.stop()

    assert call_count["n"] == 2  # first failed, second attempted
    assert published_events == ["backward"]  # only the second succeeded


@pytest.mark.asyncio
async def test_event_publisher_start_stop_lifecycle():
    """Given an EventPublisher
    When start() then stop() is called
    Then the publisher task starts and is cleanly cancelled."""

    async def publish(topic, state):
        pass

    pub = EventPublisher(topic=TOPIC, publish=publish)
    assert pub._task is None
    await pub.start()
    assert pub._task is not None
    await pub.stop()
    assert pub._task.cancelled()


@pytest.mark.asyncio
async def test_event_publisher_default_publish_is_noop():
    """Given an EventPublisher with no publish callable wired
    When an event is enqueued and the loop runs
    Then the default publish is a no-op and no exception is raised."""

    pub = EventPublisher(topic=TOPIC)
    await pub.start()
    await pub.enqueue(make_state())
    await asyncio.sleep(0.05)
    await pub.stop()
    # No exception raised — fire-and-forget default publish does not fail.


@pytest.mark.asyncio
async def test_event_publisher_topic_is_robot_state_changed():
    """Given an EventPublisher
    When events are published
    Then the topic is always robot.state.changed (Contract 2)."""

    topics = []

    async def publish(topic, state):
        topics.append(topic)

    pub = EventPublisher(topic=TOPIC, publish=publish)
    await pub.start()
    await pub.enqueue(make_state())
    await asyncio.sleep(0.05)
    await pub.stop()

    assert all(t == "robot.state.changed" for t in topics)
