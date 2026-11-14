import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useRobotStateConnection } from './useRobotStateConnection';
import { MockWebSocket } from '../test-utils/mockWebSocket';

describe('useRobotStateConnection (NFR3.1–NFR3.5, NFR1.2, NFR1.5)', () => {
  const originalWebSocket = globalThis.WebSocket;

  beforeEach(() => {
    MockWebSocket.reset();
    vi.spyOn(console, 'error').mockImplementation(() => {});
    // jsdom does not provide a native WebSocket; the hook under test uses the
    // global WebSocket, so tests install the mock before rendering.
    (globalThis as unknown as { WebSocket: unknown }).WebSocket = MockWebSocket;
  });

  afterEach(() => {
    act(() => {
      for (const socket of MockWebSocket.instances) {
        socket.close();
      }
    });
    MockWebSocket.reset();
    vi.restoreAllMocks();
    (globalThis as unknown as { WebSocket: unknown }).WebSocket = originalWebSocket;
  });

  function latestSocket(): MockWebSocket {
    const instances = MockWebSocket.instances;
    return instances[instances.length - 1];
  }

  it('Given a fresh mount, When the WebSocket opens, Then the connection shows connected with no reconnect attempts', () => {
    const { result } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
    });

    expect(result.current.connection.status).toBe('connected');
    expect(result.current.connection.reconnectAttempt).toBe(0);
    expect(result.current.connection.isStale).toBe(false);
  });

  it('Given a valid RobotStateChanged event, When it arrives on the socket, Then state is applied, the event counter increments and last-updated is set', () => {
    const { result } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage(
        JSON.stringify({
          timestamp: '2026-11-14T12:00:00Z',
          direction: 'forward',
          orientation: 45,
          color: 'blue',
          position: '[1, 2]',
          connectionStatus: 'connected',
        })
      );
    });

    expect(result.current.state.direction).toBe('forward');
    expect(result.current.state.orientation).toBe('45°');
    expect(result.current.state.color).toBe('blue');
    expect(result.current.state.position).toBe('[1, 2]');
    expect(result.current.state.timestamp).toBe('2026-11-14T12:00:00Z');
    expect(result.current.eventCount).toBe(1);
    expect(result.current.lastUpdatedAt).toBeDefined();
    expect(result.current.connection.status).toBe('connected');
    expect(result.current.connection.isStale).toBe(false);
  });

  it('Given a payload with missing and explicit-null fields, When the event is applied, Then those fields render as dashes', () => {
    const { result } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage(
        JSON.stringify({
          timestamp: '2026-11-14T12:00:00Z',
          direction: null,
          position: null,
        })
      );
    });

    expect(result.current.state.direction).toBe('-');
    expect(result.current.state.position).toBe('-');
    expect(result.current.state.color).toBe('-');
    expect(result.current.state.orientation).toBe('-');
    expect(result.current.eventCount).toBe(1);
  });

  it('Given a malformed non-JSON frame, When it arrives, Then the frame is dropped, state is untouched, the counter does not advance and console.error logs a non-payload diagnostic', () => {
    const { result } = renderHook(() => useRobotStateConnection());
    const consoleError = vi.mocked(console.error);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage('not json at all');
    });

    expect(result.current.eventCount).toBe(0);
    expect(result.current.state.direction).toBe('-');
    expect(consoleError).toHaveBeenCalledTimes(1);
    expect(String(consoleError.mock.calls[0][0])).toContain('Dropped malformed RobotState frame');
    expect(String(consoleError.mock.calls[0][0])).not.toContain('not json at all');
  });

  it('Given a schema-mismatched frame (timestamp missing), When it arrives, Then the frame is dropped and never rendered', () => {
    const { result } = renderHook(() => useRobotStateConnection());
    const consoleError = vi.mocked(console.error);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage(JSON.stringify({ direction: 'forward' }));
    });

    expect(result.current.eventCount).toBe(0);
    expect(result.current.state.direction).toBe('-');
    expect(consoleError).toHaveBeenCalledTimes(1);
    expect(String(consoleError.mock.calls[0][0])).toContain('Dropped malformed RobotState frame');
  });

  it('Given a frame whose orientation has the wrong type, When it arrives, Then the frame is dropped as shape-mismatched', () => {
    const { result } = renderHook(() => useRobotStateConnection());
    const consoleError = vi.mocked(console.error);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage(
        JSON.stringify({ timestamp: '2026-11-14T12:00:00Z', orientation: 'fast' })
      );
    });

    expect(result.current.eventCount).toBe(0);
    expect(consoleError).toHaveBeenCalledTimes(1);
  });

  it('Given the socket closes, When the first backoff elapses, Then a new socket is opened after 1s and the status shows reconnecting (attempt 1)', () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().close();
    });

    expect(result.current.connection.status).toBe('reconnecting');
    expect(result.current.connection.reconnectAttempt).toBe(1);
    expect(result.current.connection.isStale).toBe(true);
    expect(MockWebSocket.instances).toHaveLength(1);

    act(() => {
      vi.advanceTimersByTime(1000);
    });

    expect(MockWebSocket.instances).toHaveLength(2);
    vi.useRealTimers();
  });

  it('Given repeated socket losses, When reconnect backoff runs, Then the schedule is 1s, 2s, 4s, 8s capped at 30s', () => {
    vi.useFakeTimers();
    const delays: number[] = [];
    const originalSetTimeout = setTimeout;
    vi.spyOn(window, 'setTimeout').mockImplementation((handler: any, delay?: number) => {
      if (typeof delay === 'number') delays.push(delay);
      return originalSetTimeout(handler, delay);
    });

    const { result } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
      // Six successive losses: delays should be 1000, 2000, 4000, 8000, 16000, 30000 (capped).
      for (let i = 0; i < 6; i += 1) {
        latestSocket().close();
        act(() => {
          vi.advanceTimersByTime(30000);
        });
      }
    });

    expect(delays).toEqual([1000, 2000, 4000, 8000, 16000, 30000]);
    expect(result.current.connection.reconnectAttempt).toBe(6);
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it('Given a reconnect followed by the first valid event, When the event arrives, Then the stale marker clears (stale clears on first valid event, not on socket open)', () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage(
        JSON.stringify({ timestamp: '2026-11-14T12:00:00Z', direction: 'forward' })
      );
      latestSocket().close();
    });

    expect(result.current.connection.isStale).toBe(true);
    expect(result.current.state.direction).toBe('forward');

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    act(() => {
      const reconnected = MockWebSocket.instances[1];
      reconnected.simulateOpen();
      // Socket open alone does not clear the stale marker.
      expect(result.current.connection.isStale).toBe(true);
      reconnected.simulateMessage(
        JSON.stringify({ timestamp: '2026-11-14T12:01:00Z', direction: 'backward' })
      );
    });

    expect(result.current.connection.isStale).toBe(false);
    expect(result.current.state.direction).toBe('backward');
    expect(result.current.state.timestamp).toBe('2026-11-14T12:01:00Z');
    expect(result.current.eventCount).toBe(2);
    vi.useRealTimers();
  });

  it('Given a socket error, When it occurs, Then a non-payload diagnostic is logged and reconnect is scheduled', () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useRobotStateConnection());
    const consoleError = vi.mocked(console.error);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateError();
    });

    expect(consoleError).toHaveBeenCalledTimes(1);
    expect(String(consoleError.mock.calls[0][0])).toContain('WebSocket error');
    expect(String(consoleError.mock.calls[0][0])).not.toContain('telemetry');

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(MockWebSocket.instances).toHaveLength(2);
    vi.useRealTimers();
  });

  it('Given the component unmounts, When a close is pending, Then the socket is closed and no reconnect timer fires', () => {
    vi.useFakeTimers();
    const { result, unmount } = renderHook(() => useRobotStateConnection());

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().close();
    });

    unmount();

    expect(latestSocket().closed).toBe(true);
    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(MockWebSocket.instances).toHaveLength(1);
    vi.useRealTimers();
  });
});
