export class MockWebSocket {
  static instances: MockWebSocket[] = [];

  url: string;
  onopen: ((ev: Event) => void) | null = null;
  onclose: ((ev: CloseEvent) => void) | null = null;
  onerror: ((ev: Event) => void) | null = null;
  onmessage: ((ev: MessageEvent) => void) | null = null;

  closed = false;
  // 1 = OPEN, 2 = CLOSING, 3 = CLOSED (WebSocket readyState constants).
  readyState = 1;

  constructor(url: string) {
    this.url = url;
    MockWebSocket.instances.push(this);
  }

  send(): void {
    // Fire-and-forget telemetry path: this unit never sends frames over the socket.
  }

  close(): void {
    this.closed = true;
    const handler = this.onclose;
    if (handler) {
      handler(new CloseEvent('close', { code: 1006, wasClean: false }));
    }
  }

  simulateOpen(): void {
    const handler = this.onopen;
    if (handler) {
      handler(new Event('open'));
    }
  }

  simulateMessage(data: string): void {
    const handler = this.onmessage;
    if (handler) {
      handler(new MessageEvent('message', { data }));
    }
  }

  simulateError(): void {
    const handler = this.onerror;
    if (handler) {
      handler(new Event('error'));
    }
  }

  static reset(): void {
    MockWebSocket.instances = [];
  }
}
