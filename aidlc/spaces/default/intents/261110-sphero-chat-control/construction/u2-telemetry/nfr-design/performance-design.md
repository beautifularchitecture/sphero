# Performance Design — u2-telemetry

Grounded in NFR requirements [performance-requirements], functional-spec [functional-spec], tech-stack-decisions [tech-stack-decisions], and nfr-design questions [nfr-design-questions] (Q2: A — asynchronous publish).

## Performance Design

### Caching Strategy

A short-lived in-memory cache holds the most recent RobotState per robot so the stats panel can render immediately on connect without waiting for the next BLE telemetry event. Cache TTL is 10 seconds; entries are invalidated on each new RobotStateChanged publish. No cross-request strong consistency is required (NFR4.3 leaves 400ms of the 500ms budget after normalization).

### Async Event Publishing (Q2: A)

U2 publishes RobotStateChanged events asynchronously. Raw BLE telemetry is received on a dedicated receive loop, normalized into a RobotState, and enqueued. A background publisher drains the queue and publishes each event on the `robot.state.changed` topic per Contract 2 (fire-and-forget, no retry). This keeps BLE reception non-blocking even at NFR4.2's sustained 10 events/sec.

Illustrative interface (≤15 lines):

```python
class TelemetryPublisher:
    def __init__(self, topic: str = "robot.state.changed"):
        self.topic = topic
        self._queue: asyncio.Queue[RobotState] = asyncio.Queue()

    async def enqueue(self, state: RobotState) -> None:
        await self._queue.put(state)

    async def run(self) -> None:
        while True:
            state = await self._queue.get()
            await self._publish(state)

    async def _publish(self, state: RobotState) -> None:
        # Fire-and-forget per Contract 2; no retry, next event overwrites.
        await event_bus.publish(self.topic, state)
```

### Performance Budgets

| Budget | Target | Source |
|--------|--------|--------|
| BLE receipt → RobotState normalization | 100ms | NFR4.3 |
| RobotState → RobotStateChanged publish | 400ms (within 500ms total) | NFR4.1 |
| Sustained event throughput | 10 events/sec | NFR4.2 |

### Resource Pooling

- A single bleak BLE client connection is shared with U1's command sending (multiplexed, per the functional-spec assumptions). One connection avoids concurrent GATT contention.
- The asyncio event loop runs one publisher coroutine; no thread pool is needed for I/O-bound BLE and event publishing.

## Assumptions & Open Questions

None.
