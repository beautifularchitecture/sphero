import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, cleanup, act } from '@testing-library/react';
import { StatsPanel } from './components/StatsPanel';
import { MockWebSocket } from './test-utils/mockWebSocket';

describe('Integration: WebSocket telemetry -> UI render (StatsPanel)', () => {
  const originalWebSocket = globalThis.WebSocket;

  beforeEach(() => {
    MockWebSocket.reset();
    vi.spyOn(console, 'error').mockImplementation(() => {});
    (globalThis as unknown as { WebSocket: unknown }).WebSocket = MockWebSocket;
    cleanup();
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
    cleanup();
  });

  function latestSocket() {
    const instances = MockWebSocket.instances;
    return instances[instances.length - 1];
  }

  it('Given a valid RobotStateChanged event over /ws/robot-state, When it arrives, Then telemetry renders, the counter advances and connection shows connected', () => {
    render(<StatsPanel />);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage(
        JSON.stringify({
          timestamp: '2026-11-14T12:00:00Z',
          direction: 'forward',
          orientation: 90,
          color: 'green',
          position: '[2.5, -1.0]',
          connectionStatus: 'connected',
        })
      );
    });

    expect(screen.getByTestId('value-direction').textContent).toBe('forward');
    expect(screen.getByTestId('value-orientation').textContent).toBe('90°');
    expect(screen.getByTestId('value-color').textContent).toBe('green');
    expect(screen.getByTestId('value-position').textContent).toBe('[2.5, -1.0]');
    expect(screen.getByTestId('value-timestamp').textContent).toBe(
      '2026-11-14T12:00:00Z'
    );
    expect(screen.getByTestId('event-counter').textContent).toBe('1');
    expect(screen.getByTestId('last-updated').textContent).not.toBe('-');
    expect(screen.getByTestId('status-label').textContent).toBe('Connected');
  });

  it('Given the socket closes, When the first backoff elapses and a new socket opens, Then the UI shows reconnecting (attempt 1) then connected again', () => {
    vi.useFakeTimers();
    render(<StatsPanel />);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().close();
    });

    expect(screen.getByTestId('status-label').textContent).toBe(
      'Reconnecting (attempt 1)'
    );
    expect(screen.getByTestId('lan-risk-banner')).toBeInTheDocument();
    expect(screen.queryByTestId('stale-marker')).toBeInTheDocument();

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    act(() => {
      latestSocket().simulateOpen();
    });

    expect(screen.getByTestId('status-label').textContent).toBe('Connected');
    vi.useRealTimers();
  });

  it('Given a malformed frame on the socket, When it arrives, Then nothing on the panel changes and no payload is logged', () => {
    const consoleError = vi.mocked(console.error);
    render(<StatsPanel />);

    act(() => {
      latestSocket().simulateOpen();
      latestSocket().simulateMessage('{broken json');
    });

    expect(screen.getByTestId('event-counter').textContent).toBe('0');
    expect(screen.getByTestId('value-direction').textContent).toBe('-');
    expect(consoleError).toHaveBeenCalledTimes(1);
    expect(String(consoleError.mock.calls[0][0])).toContain(
      'Dropped malformed RobotState frame'
    );
    expect(String(consoleError.mock.calls[0][0])).not.toContain('{broken json');
  });
});
