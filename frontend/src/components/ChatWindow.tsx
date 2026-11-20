import { useState, type FormEvent } from 'react';

/**
 * ChatWindow (U1). Presentational chat slice: renders the conversation supplied
 * by App and hands commands back through the injectable onSend callback. It does
 * not own the WebSocket transport or the stats panel; App wires both together.
 */
export interface ChatMessageView {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: string;
}

export interface ChatWindowProps {
  messages: ChatMessageView[];
  onSend: (command: string) => void;
  sending?: boolean;
}

export function ChatWindow({ messages, onSend, sending = false }: ChatWindowProps) {
  const [draft, setDraft] = useState('');
  const [validation, setValidation] = useState<string | null>(null);

  const submit = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    if (sending) {
      return;
    }
    const text = draft.trim();
    if (!text) {
      setValidation('Please type a command for the robot.');
      return;
    }
    setValidation(null);
    setDraft('');
    onSend(text);
  };

  return (
    <section
      className="flex flex-col gap-3 p-4 border border-gray-200 rounded-lg bg-white shadow-sm"
      data-testid="chat-window"
      aria-label="Robot chat"
    >
      <h2 className="text-sm font-semibold text-gray-700">Chat</h2>
      <ul className="flex flex-col gap-2 max-h-64 overflow-y-auto" data-testid="chat-messages" aria-live="polite">
        {messages.map((message) => (
          <li
            key={message.id}
            className="text-sm p-2 rounded bg-gray-50 border border-gray-100"
            data-testid="chat-message"
          >
            <span className="font-medium text-gray-600" data-testid="chat-sender">
              {message.sender}
            </span>
            <span data-testid="chat-message-text">: {message.text}</span>
            <time className="block text-xs text-gray-400" data-testid="chat-timestamp">
              {message.timestamp}
            </time>
          </li>
        ))}
      </ul>
      {validation !== null && (
        <p className="text-sm text-amber-700" role="alert" data-testid="chat-validation">
          {validation}
        </p>
      )}
      <form className="flex gap-2" onSubmit={submit} data-testid="chat-form">
        <input
          className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded"
          data-testid="chat-input"
          aria-label="Chat command"
          placeholder="Tell the robot what to do…"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          disabled={sending}
        />
        <button
          className="px-3 py-1 text-sm border border-gray-300 rounded bg-white disabled:opacity-50"
          type="submit"
          data-testid="chat-send"
          disabled={sending}
        >
          Send
        </button>
      </form>
    </section>
  );
}
