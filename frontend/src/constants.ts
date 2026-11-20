export const WS_ROBOT_STATE_PATH = '/ws/robot-state';

/**
 * Build an absolute WebSocket URL for the robot-state stream. The browser
 * WebSocket constructor rejects a relative URL, so derive the scheme and host
 * from the current page location: `wss:` on https, `ws:` otherwise.
 */
export function robotStateWebSocketUrl(
  location: Pick<Location, 'protocol' | 'host'> = window.location
): string {
  const scheme = location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${scheme}//${location.host}${WS_ROBOT_STATE_PATH}`;
}

export const LAN_RISK_BANNER_TEXT =
  'LAN-only design: unauthenticated WebSocket. Anyone on this LAN can read robot telemetry and send movement commands.';

export const DASH = '-';

export const RECONNECT_BASE_DELAY_MS = 1000;
export const RECONNECT_MAX_DELAY_MS = 30000;
