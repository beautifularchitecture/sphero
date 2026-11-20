import type { ErrorReport } from '../types';

/**
 * Chat command transport for U1. The socket factory is injectable so unit tests
 * never open a real WebSocket. The URL is always absolute (the browser's
 * WebSocket constructor throws on a path-only URL).
 */

export const WS_CHAT_PATH = '/ws/chat';

/**
 * One-shot chat commands must outlive the backend's worst case before it can
 * ack: two OpenRouter model attempts (2 x 5 s) + retry backoff (~0.1 s) + two
 * BLE send attempts with reconnect (~0.1 s) = ~10.2 s. Leave headroom so a
 * legitimately retrying command is never surfaced as a frontend timeout.
 * Callers can still override this per request via `ChatTransportOptions.timeoutMs`.
 */
export const DEFAULT_CHAT_TIMEOUT_MS = 15000;

export interface ChatAck {
  type: 'ack';
  message: string;
  commandId: string;
  status: string;
  timestamp: string;
}

export type ChatResult =
  | { ok: true; message: string; ack: ChatAck }
  | { ok: false; error: ErrorReport };

export interface ChatTransportOptions {
  url?: string;
  socketFactory?: (url: string) => WebSocket;
  timeoutMs?: number;
}

export function buildChatWebSocketUrl(path: string = WS_CHAT_PATH, base?: string): string {
  const origin =
    base ??
    (typeof window !== 'undefined' && window.location
      ? `${window.location.protocol}//${window.location.host}`
      : undefined);

  if (!origin) {
    return `ws://localhost:8000${path}`;
  }
  const normalized = origin.endsWith('/') ? origin.slice(0, -1) : origin;
  const wsOrigin = normalized.replace(/^http/, 'ws');
  return `${wsOrigin}${path.startsWith('/') ? path : `/${path}`}`;
}

function makeError(type: string, message: string): ErrorReport {
  return { type, message, timestamp: new Date().toISOString() };
}

function messageOf(value: unknown): string {
  return value instanceof Error ? value.message : String(value);
}

/**
 * Send one chat command and resolve when the backend acks it or reports an
 * error. Always resolves with a discriminated result; it never rejects.
 */
export function sendChatCommand(
  command: string,
  options: ChatTransportOptions = {},
): Promise<ChatResult> {
  const text = command.trim();
  if (!text) {
    return Promise.resolve({
      ok: false,
      error: makeError('validation', 'Please type a command for the robot.'),
    });
  }

  const url = options.url ?? buildChatWebSocketUrl();
  const socketFactory =
    options.socketFactory ?? ((target: string): WebSocket => new WebSocket(target));
  const timeoutMs = options.timeoutMs ?? DEFAULT_CHAT_TIMEOUT_MS;

  return new Promise<ChatResult>((resolve) => {
    let settled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let socket: WebSocket;

    const finish = (result: ChatResult): void => {
      if (settled) {
        return;
      }
      settled = true;
      if (timer !== undefined) {
        clearTimeout(timer);
      }
      try {
        socket?.close();
      } catch {
        // Closing an already-closed socket is not a command failure.
      }
      resolve(result);
    };
    const failure = (type: string, message: string, timestamp?: string): ChatResult => ({
      ok: false,
      error: timestamp ? { type, message, timestamp } : makeError(type, message),
    });

    try {
      socket = socketFactory(url);
    } catch (error) {
      finish(failure('transport', `Could not open the chat connection: ${messageOf(error)}`));
      return;
    }

    timer = setTimeout(() => {
      finish(failure('timeout', 'The robot did not respond in time. Please try again.'));
    }, timeoutMs);

    socket.onopen = () => {
      try {
        socket.send(JSON.stringify({ text }));
      } catch (error) {
        finish(failure('transport', `Could not send the command: ${messageOf(error)}`));
      }
    };

    socket.onmessage = (event: MessageEvent<string>) => {
      let payload: unknown;
      try {
        payload = JSON.parse(String(event.data));
      } catch {
        finish(failure('protocol', 'The robot sent an unreadable response.'));
        return;
      }
      if (typeof payload !== 'object' || payload === null) {
        finish(failure('protocol', 'Unexpected response from the robot.'));
        return;
      }
      const response = payload as Record<string, unknown>;
      if (response.type === 'ack') {
        finish({
          ok: true,
          message: String(response.message ?? 'Command accepted.'),
          ack: response as unknown as ChatAck,
        });
        return;
      }
      if (response.type === 'error') {
        finish(
          failure(
            String(response.errorType ?? 'server'),
            String(response.message ?? 'The robot could not run that command.'),
            typeof response.timestamp === 'string' ? response.timestamp : undefined,
          ),
        );
        return;
      }
      finish(failure('protocol', 'Unexpected response from the robot.'));
    };

    socket.onerror = () => {
      finish(failure('transport', 'Chat connection failed. Check the backend is running.'));
    };

    socket.onclose = () => {
      finish(failure('transport', 'Chat connection closed before a reply arrived.'));
    };
  });
}
