/**
 * ConnectionStatus (BR1.5.2, NFR3.4, NFR3.5).
 *
 * Shows the BLE/stream connection state indicator: connected, disconnected,
 * pairing, error, or reconnecting (attempt N). An optional stale badge is
 * shown when last-known values are being displayed after stream loss.
 */
export type ConnectionStatusValue = 'connected' | 'disconnected' | 'pairing' | 'error' | 'reconnecting';

interface ConnectionStatusProps {
  status: ConnectionStatusValue;
  reconnectAttempt?: number;
  isStale?: boolean;
}

const labels: Record<Exclude<ConnectionStatusValue, 'reconnecting'>, string> = {
  connected: 'Connected',
  disconnected: 'Disconnected',
  pairing: 'Pairing',
  error: 'Error',
};

const reconnectingLabel = (attempt: number): string => `Reconnecting (attempt ${attempt})`;

const colorClasses: Record<ConnectionStatusValue, string> = {
  connected: 'text-green-600',
  disconnected: 'text-gray-500',
  pairing: 'text-amber-500',
  error: 'text-red-600',
  reconnecting: 'text-amber-600',
};

export function ConnectionStatus({
  status,
  reconnectAttempt = 0,
  isStale = false,
}: ConnectionStatusProps) {
  const label =
    status === 'reconnecting' ? reconnectingLabel(reconnectAttempt) : labels[status];

  return (
    <div className="flex items-center gap-2" data-testid="connection-status">
      <span
        data-testid="status-dot"
        className={`w-2 h-2 rounded-full ${colorClasses[status]}`}
        aria-hidden="true"
      />
      <span data-testid="status-label" className={`text-sm font-medium ${colorClasses[status]}`}>
        {label}
      </span>
      {isStale && status !== 'reconnecting' && (
        <span className="text-xs font-medium text-amber-600" data-testid="stale-badge">
          stale
        </span>
      )}
    </div>
  );
}
