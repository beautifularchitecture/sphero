import { describe, it, expect, afterEach, vi } from 'vitest';
import {
  buildChatWebSocketUrl,
  DEFAULT_CHAT_TIMEOUT_MS,
  sendChatCommand,
  WS_CHAT_PATH,
} from './api';

/**
 * Scriptable socket for the injectable transport boundary. No real WebSocket,
 * network, browser timer or backend is involved in these scenarios.
 */
class FakeSocket {
  static instances: FakeSocket[] = [];

  url: string;
  sent: string[] = [];
  closed = false;
  onopen: ((event: Event) => void) | null = null;
  onmessage: ((event: MessageEvent<string>) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  onclose: ((event: CloseEvent) => void) | null = null;

  constructor(url: string) {
    this.url = url;
    FakeSocket.instances.push(this);
  }

  send(data: string): void {
    this.sent.push(data);
  }

  close(): void {
    this.closed = true;
  }

  open(): void {
    this.onopen?.(new Event('open'));
  }

  receive(data: string): void {
    this.onmessage?.(new MessageEvent('message', { data }));
  }

  fail(): void {
    this.onerror?.(new Event('error'));
  }

  drop(): void {
    this.onclose?.(new CloseEvent('close', { code: 1006 }));
  }
}

function captureSocket() {
  let socket: FakeSocket | undefined;
  const socketFactory = (url: string): WebSocket => {
    socket = new FakeSocket(url);
    return socket as unknown as WebSocket;
  };
  return {
    socketFactory,
    get socket(): FakeSocket {
      return socket as FakeSocket;
    },
  };
}

const ACK = JSON.stringify({
  type: 'ack',
  message: 'Command forward accepted.',
  commandId: 'cmd-1',
  status: 'moving',
  timestamp: '2026-11-19T10:00:00Z',
});

afterEach(() => {
  FakeSocket.instances = [];
  vi.useRealTimers();
});

describe('buildChatWebSocketUrl', () => {
  it('Given an application origin, When the chat URL is built, Then it is an absolute ws/wss URL ending in /ws/chat', () => {
    expect(buildChatWebSocketUrl(WS_CHAT_PATH, 'http://localhost:5173')).toBe(
      'ws://localhost:5173/ws/chat'
    );
    expect(buildChatWebSocketUrl(WS_CHAT_PATH, 'https://sphero.test/')).toBe(
      'wss://sphero.test/ws/chat'
    );
    expect(buildChatWebSocketUrl('ws/chat', 'http://localhost:5173/')).toBe(
      'ws://localhost:5173/ws/chat'
    );
  });

  it('Given no browser or explicit origin, When the chat URL is built, Then it falls back to the local backend', () => {
    expect(buildChatWebSocketUrl(WS_CHAT_PATH, '')).toBe('ws://localhost:8000/ws/chat');
  });
});

describe('sendChatCommand (U1 chat transport)', () => {
  it('Given a command, When the backend acks it, Then the trimmed text is sent and an ok result with the ack is returned', async () => {
    const captured = captureSocket();

    const resultPromise = sendChatCommand('  roll forward  ', {
      socketFactory: captured.socketFactory,
    });
    captured.socket.open();
    captured.socket.receive(ACK);
    const result = await resultPromise;

    expect(captured.socket.url).toBeTruthy();
    expect(captured.socket.sent).toEqual([JSON.stringify({ text: 'roll forward' })]);
    expect(captured.socket.closed).toBe(true);
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.message).toBe('Command forward accepted.');
      expect(result.ack.commandId).toBe('cmd-1');
      expect(result.ack.status).toBe('moving');
    }
  });

  it('Given the backend sends an error envelope, When the message arrives, Then a failed result carrying the error report is returned', async () => {
    const captured = captureSocket();
    const resultPromise = sendChatCommand('roll sideways', {
      socketFactory: captured.socketFactory,
    });

    captured.socket.open();
    captured.socket.receive(
      JSON.stringify({
        type: 'error',
        errorType: 'validation',
        message: 'Please rephrase that command.',
        timestamp: '2026-11-19T10:00:02Z',
      })
    );
    const result = await resultPromise;

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error.type).toBe('validation');
      expect(result.error.message).toBe('Please rephrase that command.');
      expect(result.error.timestamp).toBe('2026-11-19T10:00:02Z');
    }
  });

  it('Given an empty command, When sendChatCommand is called, Then a validation result is returned and no socket is opened', async () => {
    const result = await sendChatCommand('   ', { socketFactory: captureSocket().socketFactory });

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error.type).toBe('validation');
      expect(result.error.message).toContain('type a command');
    }
    expect(FakeSocket.instances).toHaveLength(0);
  });

  it('Given a socket factory that throws, When sendChatCommand is called, Then a transport error is returned instead of a rejection', async () => {
    const result = await sendChatCommand('roll forward', {
      socketFactory: () => {
        throw new Error('no adapter');
      },
    });

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error.type).toBe('transport');
      expect(result.error.message).toContain('no adapter');
    }
  });

  it('Given the socket errors or closes before a reply, When either event fires, Then a transport error is returned', async () => {
    const first = captureSocket();
    const errorPromise = sendChatCommand('roll forward', { socketFactory: first.socketFactory });
    first.socket.fail();
    const errorResult = await errorPromise;
    expect(errorResult.ok).toBe(false);
    if (!errorResult.ok) {
      expect(errorResult.error.type).toBe('transport');
      expect(errorResult.error.message).toContain('connection failed');
    }

    const second = captureSocket();
    const closePromise = sendChatCommand('stop', { socketFactory: second.socketFactory });
    second.socket.drop();
    const closeResult = await closePromise;
    expect(closeResult.ok).toBe(false);
    if (!closeResult.ok) {
      expect(closeResult.error.type).toBe('transport');
      expect(closeResult.error.message).toContain('closed before a reply');
    }
  });

  it('Given a malformed or unknown frame, When it arrives, Then a protocol error is returned', async () => {
    const first = captureSocket();
    const malformedPromise = sendChatCommand('roll forward', {
      socketFactory: first.socketFactory,
    });
    first.socket.open();
    first.socket.receive('{not json');
    const malformed = await malformedPromise;
    expect(malformed.ok).toBe(false);
    if (!malformed.ok) {
      expect(malformed.error.type).toBe('protocol');
    }

    const second = captureSocket();
    const unknownPromise = sendChatCommand('stop', { socketFactory: second.socketFactory });
    second.socket.open();
    second.socket.receive(JSON.stringify({ type: 'telemetry', timestamp: 'now' }));
    const unknown = await unknownPromise;
    expect(unknown.ok).toBe(false);
    if (!unknown.ok) {
      expect(unknown.error.type).toBe('protocol');
    }
  });

  it('Given the robot never replies, When the timeout elapses, Then a timeout error is returned and the socket is closed', async () => {
    vi.useFakeTimers();
    const captured = captureSocket();

    const resultPromise = sendChatCommand('roll forward', {
      socketFactory: captured.socketFactory,
      timeoutMs: DEFAULT_CHAT_TIMEOUT_MS,
    });
    captured.socket.open();
    vi.advanceTimersByTime(DEFAULT_CHAT_TIMEOUT_MS);
    const result = await resultPromise;

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error.type).toBe('timeout');
      expect(result.error.message).toContain('did not respond in time');
    }
    expect(captured.socket.closed).toBe(true);
  });
});
