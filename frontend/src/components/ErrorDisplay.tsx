import type { ErrorReport } from '../types';

/**
 * ErrorDisplay (BR1.5.4, NFR1.2).
 *
 * Renders an error report (type, message, timestamp) as React-escaped text.
 * No dangerouslySetInnerHTML and no raw HTML injection path: untrusted display
 * text is safe by construction. Renders nothing when there is no error.
 */
export function ErrorDisplay({ error }: { error: ErrorReport | null }) {
  if (!error) {
    return null;
  }

  return (
    <div
      className="p-3 mb-2 border border-red-200 bg-red-50 text-red-900 rounded"
      data-testid="error-display"
    >
      <div data-testid="error-type">{error.type}</div>
      <div data-testid="error-message">{error.message}</div>
      <div data-testid="error-timestamp">{error.timestamp}</div>
    </div>
  );
}
