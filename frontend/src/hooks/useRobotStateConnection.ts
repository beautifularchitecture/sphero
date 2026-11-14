import { useCallback, useEffect, useRef, useState } from 'react';

import type {
  ConnectionView,
  RobotStatePayload,
  RobotStateView,
  UseRobotStateConnectionResult,
} from '../types';
import {
  DASH,
  RECONNECT_BASE_DELAY_MS,
  RECONNECT_MAX_DELAY_MS,
  WS_ROBOT_STATE_PATH,
} from '../constants';

function formatOrientation(value: number | null | undefined): string {
  if (value === null || value === undefined) {
    return DASH;
  }
  return `${value}°`;
}

function dashFor(value: string | null | undefined): string {
  if (value === null || value === undefined || value === '') {
    return DASH;
  }
  return value;
}

function emptyView(): RobotStateView {
  return {
    direction: DASH,
    orientation: DASH,
    color: DASH,
    position: DASH,
    timestamp: DASH,
  };
}

function initialConnection(): ConnectionView {
  return { status: 'disconnected', reconnectAttempt: 0, isStale: false };
}

function isValidRobotState(value: unknown): value is RobotStatePayload {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    return false;
  }
  const payload = value as RobotStatePayload;
  if (typeof payload.timestamp !== 'string') {
    return false;
  }
  if (
    payload.direction !== null &&
    payload.direction !== undefined &&
    typeof payload.direction !== 'string'
  ) {
    return false;
  }
  if (
    payload.color !== null &&
    payload.color !== undefined &&
    typeof payload.color !== 'string'
  ) {
    return false;
  }
  if (
    payload.position !== null &&
    payload.position !== undefined &&
    typeof payload.position !== 'string'
  ) {
    return false;
  }
  if (
    payload.orientation !== null &&
    payload.orientation !== undefined &&
    typeof payload.orientation !== 'number'
  ) {
    return false;
  }
  if (
    payload.connectionStatus !== null &&
    payload.connectionStatus !== undefined &&
    typeof payload.connectionStatus !== 'string'
  ) {
    return false;
  }
  return true;
}

function backoffDelayMs(attempt: number): number {
  return Math.min(RECONNECT_BASE_DELAY_MS * 2 ** (attempt - 1), RECONNECT_MAX_DELAY_MS);
}

/**
 * Manages the /ws/robot-state WebSocket lifecycle for the stats panel:
 * native WebSocket subscription initiated on mount, exponential reconnect
 * backoff (1s / 2s / 4s / 8s, capped at 30s), JSON parse + shape validation,
 * malformed-frame drop with a non-payload console.error, event counter, stale
 * marker and last-updated timestamp.
 *
 * Stale state clears on the first new valid RobotStateChanged event after a
 * reconnect — never on socket open alone.
 */
export function useRobotStateConnection(): UseRobotStateConnectionResult {
  const [state, setState] = useState<RobotStateView>(emptyView());
  const [connection, setConnection] = useState<ConnectionView>(initialConnection());
  // reconnectAttempt is tracked imperatively in a ref because socket close
  // events can fire outside React's act/sync flush (e.g. in test loops that
  // close between timer advances). Reading React state `connection` here would
  // always observe the stale last-rendered attempt, collapsing every backoff
  // delay to base * 2 ** -1.
  const reconnectAttemptRef = useRef(0);
  const [eventCount, setEventCount] = useState(0);
  const [lastUpdatedAt, setLastUpdatedAt] = useState<string | undefined>(undefined);

  const socketRef = useRef<WebSocket | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const cancelledRef = useRef(false);
  const connectRef = useRef(() => {});
  const scheduleReconnectRef = useRef(() => {});

  const clearReconnectTimer = useCallback(() => {
    if (timerRef.current !== null) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const closeSocket = useCallback(() => {
    clearReconnectTimer();
    const socket = socketRef.current;
    if (socket !== null) {
      socketRef.current = null;
      try {
        socket.close();
      } catch {
        // Socket teardown must never throw.
      }
    }
  }, [clearReconnectTimer]);

  connectRef.current = () => {
    if (cancelledRef.current) {
      return;
    }
    closeSocket();

    let socket: WebSocket;
    try {
      socket = new WebSocket(WS_ROBOT_STATE_PATH);
    } catch (error) {
      console.error('Failed to open robot-state WebSocket connection', error);
      scheduleReconnectRef.current();
      return;
    }
    socketRef.current = socket;

    socket.onopen = () => {
      if (cancelledRef.current) {
        return;
      }
      reconnectAttemptRef.current = 0;
      setConnection((prev) => ({
        ...prev,
        status: 'connected',
        reconnectAttempt: 0,
      }));
    };

    socket.onclose = () => {
      if (cancelledRef.current) {
        return;
      }
      if (socketRef.current !== socket) {
        // A superseded socket instance; ignore its close.
        return;
      }
      socketRef.current = null;
      const nextAttempt = reconnectAttemptRef.current + 1;
      reconnectAttemptRef.current = nextAttempt;
      setConnection((prev) => ({
        ...prev,
        status: 'reconnecting',
        reconnectAttempt: nextAttempt,
        isStale: true,
      }));
      scheduleReconnectRef.current();
    };

    socket.onerror = (error) => {
      if (cancelledRef.current) {
        return;
      }
      console.error('Robot-state WebSocket error', error);
      socket.close();
    };

    socket.onmessage = (event) => {
      if (cancelledRef.current) {
        return;
      }
      let parsed: unknown;
      try {
        parsed = JSON.parse(event.data);
      } catch {
        console.error('Dropped malformed RobotState frame: invalid JSON');
        return;
      }
      if (!isValidRobotState(parsed)) {
        console.error('Dropped malformed RobotState frame: invalid shape');
        return;
      }
      const payload = parsed as RobotStatePayload;
      setState({
        direction: dashFor(payload.direction),
        orientation: formatOrientation(payload.orientation),
        color: dashFor(payload.color),
        position: dashFor(payload.position),
        timestamp: payload.timestamp,
      });
      setEventCount((n) => n + 1);
      setLastUpdatedAt(new Date().toISOString());
      setConnection((prev) => ({
        ...prev,
        status: (payload.connectionStatus ?? 'connected') as
          | 'connected'
          | 'disconnected'
          | 'pairing'
          | 'error',
        isStale: false,
      }));
    };
  };

  scheduleReconnectRef.current = () => {
    if (cancelledRef.current) {
      return;
    }
    clearReconnectTimer();
    timerRef.current = setTimeout(() => {
      if (!cancelledRef.current) {
        connectRef.current();
      }
    }, backoffDelayMs(reconnectAttemptRef.current));
  };

  useEffect(() => {
    cancelledRef.current = false;
    connectRef.current();
    return () => {
      cancelledRef.current = true;
      clearReconnectTimer();
      const socket = socketRef.current;
      if (socket !== null) {
        socketRef.current = null;
        try {
          socket.close();
        } catch {
          // Unmount teardown must never throw.
        }
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    state,
    connection,
    eventCount,
    lastUpdatedAt,
  };
}
