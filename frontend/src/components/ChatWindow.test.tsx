import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, cleanup, act } from '@testing-library/react';
import { ChatWindow, type ChatMessageView } from './ChatWindow';
import App from '../App';

/** Scriptable WebSocket used by the App composition scenarios. */
class RecordingWebSocket {
  static instances: RecordingWebSocket[] = [];

  url: string;
  sent: string[] = [];
  closed = false;
  onopen: ((event: Event) => void) | null = null;
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  onclose: ((event: CloseEvent) => void) | null = null;

  constructor(url: string) {
    this.url = url;
    RecordingWebSocket.instances.push(this);
  }

  send(data: string): void {
    this.sent.push(data);
  }

  // Deliberately does not fire onclose: that keeps U3's reconnect timers out of
  // these U1 scenarios while still allowing teardown assertions.
  close(): void {
    this.closed = true;
  }

  open(): void {
    this.onopen?.(new Event('open'));
  }

  receive(data: string): void {
    this.onmessage?.(new MessageEvent('message', { data }));
  }

  static reset(): void {
    RecordingWebSocket.instances = [];
  }

  static chatSocket(): RecordingWebSocket {
    const socket = RecordingWebSocket.instances.find((candidate) =>
      candidate.url.includes('/ws/chat')
    );
    if (!socket) {
      throw new Error('No /ws/chat socket was opened');
    }
    return socket;
  }
}

const ACK = JSON.stringify({
  type: 'ack',
  message: 'Command forward accepted.',
  commandId: 'cmd-1',
  status: 'moving',
  timestamp: '2026-11-19T10:00:00Z',
});

describe('ChatWindow (U1 chat UI)', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  const messages: ChatMessageView[] = [
    { id: 'u1', text: 'roll forward', sender: 'user', timestamp: '2026-11-19T10:00:00Z' },
    {
      id: 'a1',
      text: 'Command forward accepted.',
      sender: 'agent',
      timestamp: '2026-11-19T10:00:01Z',
    },
  ];

  it('Given a conversation, When ChatWindow renders, Then messages appear in order with sender, text and timestamp', () => {
    render(<ChatWindow messages={messages} onSend={vi.fn()} />);

    const rendered = screen.getAllByTestId('chat-message');
    expect(rendered).toHaveLength(2);
    expect(rendered[0].textContent).toContain('roll forward');
    expect(rendered[0].textContent).toContain('user');
    expect(rendered[1].textContent).toContain('Command forward accepted.');
    expect(rendered[1].textContent).toContain('agent');
    expect(rendered[0].textContent).toContain('2026-11-19T10:00:00Z');
  });

  it('Given an empty draft, When the form is submitted, Then onSend is not called and a rephrase hint is shown', () => {
    const onSend = vi.fn();
    render(<ChatWindow messages={[]} onSend={onSend} />);

    fireEvent.submit(screen.getByTestId('chat-form'));

    expect(onSend).not.toHaveBeenCalled();
    expect(screen.getByTestId('chat-validation').textContent).toContain('type a command');
  });

  it('Given a typed command, When Send is clicked, Then onSend receives the trimmed text and the input clears', () => {
    const onSend = vi.fn();
    render(<ChatWindow messages={[]} onSend={onSend} />);
    const input = screen.getByTestId('chat-input') as HTMLInputElement;

    fireEvent.change(input, { target: { value: '  roll forward  ' } });
    fireEvent.click(screen.getByTestId('chat-send'));

    expect(onSend).toHaveBeenCalledWith('roll forward');
    expect(input.value).toBe('');
    expect(screen.queryByTestId('chat-validation')).toBeNull();
  });

  it('Given sending is true, When the user tries to submit again, Then the controls are disabled and no extra command is sent', () => {
    const onSend = vi.fn();
    render(<ChatWindow messages={[]} onSend={onSend} sending={true} />);

    expect(screen.getByTestId('chat-input')).toBeDisabled();
    expect(screen.getByTestId('chat-send')).toBeDisabled();
    fireEvent.submit(screen.getByTestId('chat-form'));
    expect(onSend).not.toHaveBeenCalled();
  });

  it('Given untrusted message text, When ChatWindow renders it, Then the text is escaped rather than interpreted as HTML', () => {
    render(
      <ChatWindow
        messages={[
          {
            id: 'x1',
            text: '<img src=x onerror="alert(1)">',
            sender: 'user',
            timestamp: '2026-11-19T10:00:00Z',
          },
        ]}
        onSend={vi.fn()}
      />
    );

    expect(screen.queryByText('', { selector: 'img' })).toBeNull();
    expect(screen.getByTestId('chat-message').textContent).toContain('<img src=x');
  });
});

describe('App composition — chat wired to U3 stats panel', () => {
  const originalWebSocket = globalThis.WebSocket;

  beforeEach(() => {
    RecordingWebSocket.reset();
    (globalThis as unknown as { WebSocket: unknown }).WebSocket = RecordingWebSocket;
    cleanup();
  });

  afterEach(() => {
    (globalThis as unknown as { WebSocket: unknown }).WebSocket = originalWebSocket;
    RecordingWebSocket.reset();
    cleanup();
  });

  it('Given App mounts, When a chat command is sent, Then it travels over /ws/chat and the ack is shown as an agent message', async () => {
    render(<App />);

    expect(screen.getByTestId('app')).toBeInTheDocument();
    expect(screen.getByTestId('stats-panel')).toBeInTheDocument();

    fireEvent.change(screen.getByTestId('chat-input'), {
      target: { value: 'roll forward' },
    });
    fireEvent.click(screen.getByTestId('chat-send'));

    const socket = RecordingWebSocket.chatSocket();
    socket.open();
    expect(JSON.parse(socket.sent[0])).toEqual({ text: 'roll forward' });

    await act(async () => {
      socket.receive(ACK);
    });

    expect(screen.getAllByTestId('chat-message')).toHaveLength(2);
    expect(screen.getAllByTestId('chat-message')[1].textContent).toContain(
      'Command forward accepted.'
    );
  });

  it('Given App mounts, When a U3 speed button is clicked, Then the selector is enabled and the exact chat command is sent', async () => {
    render(<App />);

    expect(screen.getByTestId('speed-btn-low')).not.toBeDisabled();
    fireEvent.click(screen.getByTestId('speed-btn-low'));

    const socket = RecordingWebSocket.chatSocket();
    socket.open();
    expect(JSON.parse(socket.sent[0])).toEqual({ text: 'set speed low' });

    await act(async () => {
      socket.receive(
        JSON.stringify({
          type: 'ack',
          message: 'Command setSpeed accepted.',
          commandId: 'cmd-2',
          status: 'stopped',
          timestamp: '2026-11-19T10:00:03Z',
        })
      );
    });

    expect(screen.getAllByTestId('chat-message')[1].textContent).toContain(
      'Command setSpeed accepted.'
    );
  });

  it('Given the backend returns an error envelope, When App handles it, Then U3 ErrorDisplay shows the report and chat keeps the message', async () => {
    render(<App />);

    fireEvent.change(screen.getByTestId('chat-input'), {
      target: { value: 'roll sideways' },
    });
    fireEvent.click(screen.getByTestId('chat-send'));

    const socket = RecordingWebSocket.chatSocket();
    await act(async () => {
      socket.open();
      socket.receive(
        JSON.stringify({
          type: 'error',
          errorType: 'validation',
          message: 'Please rephrase that command.',
          timestamp: '2026-11-19T10:00:04Z',
        })
      );
    });

    expect(screen.getByTestId('error-type').textContent).toBe('validation');
    expect(screen.getByTestId('error-message').textContent).toBe(
      'Please rephrase that command.'
    );
    expect(screen.getAllByTestId('chat-message')[1].textContent).toContain(
      'Please rephrase that command.'
    );
  });
});
