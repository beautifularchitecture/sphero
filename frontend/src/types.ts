export type RobotStateConnectionStatus =
  | 'connected'
  | 'disconnected'
  | 'pairing'
  | 'error';

export interface RobotStatePayload {
  timestamp: string;
  direction?: string | null;
  orientation?: number | null;
  color?: string | null;
  position?: string | null;
  connectionStatus?: RobotStateConnectionStatus | null;
}

export interface RobotStateView {
  direction: string;
  orientation: string;
  color: string;
  position: string;
  timestamp: string;
}

export interface ConnectionView {
  status: RobotStateConnectionStatus | 'reconnecting';
  reconnectAttempt: number;
  isStale: boolean;
}

export interface UseRobotStateConnectionResult {
  state: RobotStateView;
  connection: ConnectionView;
  eventCount: number;
  lastUpdatedAt: string | undefined;
}

export interface ErrorReport {
  type: string;
  message: string;
  timestamp: string;
}

export interface SpeedColorSelectorProps {
  onSendChatCommand: (command: string) => void;
  disabled?: boolean;
}

export interface StatsPanelProps {
  onSendChatCommand?: (command: string) => void;
  error?: ErrorReport | null;
}
