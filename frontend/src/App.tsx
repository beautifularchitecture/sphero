import { useCallback, useState } from 'react';
import { ChatWindow, type ChatMessageView } from './components/ChatWindow';
import { StatsPanel } from './components/StatsPanel';
import { sendChatCommand } from './services/api';
import type { ErrorReport } from './types';

let messageSequence = 0;
function nextId(prefix: string): string {
  messageSequence += 1;
  return `${prefix}-${Date.now()}-${messageSequence}`;
}

/**
 * U1 composition root (walking skeleton): the chat window and U3's StatsPanel
 * share one command handler, so typed chat and the speed/colour buttons go over
 * the same /ws/chat transport. Errors are forwarded to U3's ErrorDisplay props.
 */
export default function App() {
  const [messages, setMessages] = useState<ChatMessageView[]>([]);
  const [error, setError] = useState<ErrorReport | null>(null);
  const [sending, setSending] = useState(false);

  const handleSendCommand = useCallback(
    (text: string) => {
      const command = text.trim();
      if (!command || sending) {
        return;
      }
      setError(null);
      setSending(true);
      setMessages((previous) => [
        ...previous,
        {
          id: nextId('user'),
          text: command,
          sender: 'user',
          timestamp: new Date().toISOString(),
        },
      ]);

      void sendChatCommand(command).then((result) => {
        if (result.ok) {
          setMessages((previous) => [
            ...previous,
            {
              id: nextId('agent'),
              text: result.message,
              sender: 'agent',
              timestamp: new Date().toISOString(),
            },
          ]);
        } else {
          setError(result.error);
          setMessages((previous) => [
            ...previous,
            {
              id: nextId('agent'),
              text: result.error.message,
              sender: 'agent',
              timestamp: result.error.timestamp,
            },
          ]);
        }
        setSending(false);
      });
    },
    [sending]
  );

  return (
    <div className="max-w-md mx-auto p-4 flex flex-col gap-4" data-testid="app">
      <ChatWindow messages={messages} onSend={handleSendCommand} sending={sending} />
      <StatsPanel onSendChatCommand={handleSendCommand} error={error} />
    </div>
  );
}
