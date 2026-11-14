import { useRobotStateConnection } from '../hooks/useRobotStateConnection';
import { LanRiskBanner } from './LanRiskBanner';
import { ConnectionStatus } from './ConnectionStatus';
import { RobotStateDisplay } from './RobotStateDisplay';
import { SpeedColorSelector } from './SpeedColorSelector';
import { ErrorDisplay } from './ErrorDisplay';
import { DASH } from '../constants';
import type { StatsPanelProps } from '../types';

/**
 * StatsPanel (container, US1.4).
 *
 * Top-level stats UI container. Owns the useRobotStateConnection WebSocket
 * subscription and composes LanRiskBanner (always visible), ConnectionStatus,
 * telemetry fields, the event counter / last-updated / stale indicators,
 * SpeedColorSelector and (when provided) ErrorDisplay.
 */
export function StatsPanel({ onSendChatCommand, error }: StatsPanelProps) {
  const { state, connection, eventCount, lastUpdatedAt } = useRobotStateConnection();
  const hasCommandHandler = typeof onSendChatCommand === 'function';

  return (
    <section
      className="flex flex-col gap-4 p-4 border border-gray-200 rounded-lg bg-white shadow-sm"
      data-testid="stats-panel"
    >
      <LanRiskBanner />
      <ConnectionStatus
        status={connection.status}
        reconnectAttempt={connection.reconnectAttempt}
        isStale={connection.isStale}
      />
      <RobotStateDisplay
        direction={state.direction}
        orientation={state.orientation}
        color={state.color}
        position={state.position}
        timestamp={state.timestamp}
      />
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <span>Last updated:</span>
        <span data-testid="last-updated">{lastUpdatedAt ?? DASH}</span>
      </div>
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <span>Events received:</span>
        <span data-testid="event-counter">{eventCount}</span>
      </div>
      {connection.isStale && (
        <span className="text-xs font-medium text-amber-600" data-testid="stale-marker">
          stale
        </span>
      )}
      <SpeedColorSelector
        onSendChatCommand={onSendChatCommand ?? (() => {})}
        disabled={!hasCommandHandler}
      />
      {error !== null && error !== undefined && <ErrorDisplay error={error} />}
    </section>
  );
}
