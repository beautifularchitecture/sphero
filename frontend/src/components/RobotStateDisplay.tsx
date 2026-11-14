import { DASH } from '../constants';

/**
 * RobotStateDisplay (BR1.5.1, BR1.5.3, NFR1.2).
 *
 * Displays direction, orientation, color, position and timestamp. Missing or
 * null fields render as dashes. All values are rendered as React-escaped text.
 */
interface RobotStateDisplayProps {
  direction: string;
  // Orientation is an angle; a numeric value is rendered with a degree suffix
  // (e.g. 45 -> "45°"). Pre-formatted strings (from the WebSocket hook) are
  // rendered as-is, so there is no double-formatting in the live subscription.
  orientation: string | number;
  color: string;
  position: string;
  timestamp: string;
}

function fieldValue(value: string): string {
  if (value == null || value === '') {
    return '-';
  }
  return value;
}

export function RobotStateDisplay({
  direction,
  orientation,
  color,
  position,
  timestamp,
}: RobotStateDisplayProps) {
  const field = (label: string, value: string) => (
    <div key={label} className="flex gap-2" data-testid={`field-${label.toLowerCase()}`}>
      <span className="font-medium text-gray-700">{label}</span>
      <span className="text-gray-900" data-testid={`value-${label.toLowerCase()}`}>
        {fieldValue(value)}
      </span>
    </div>
  );

  // Numeric orientation values get a degree suffix; pre-formatted strings
  // (e.g. "45°" from the WebSocket hook) are rendered as-is. Missing/empty
  // values fall back to a dash via fieldValue.
  const orientationDisplay =
    orientation == null || orientation === ''
      ? DASH
      : typeof orientation === 'number'
        ? `${orientation}°`
        : orientation;

  return (
    <div className="space-y-2" data-testid="robot-state-display">
      {field('Direction', direction)}
      {field('Orientation', orientationDisplay)}
      {field('Color', color)}
      {field('Position', position)}
      {field('Timestamp', timestamp)}
    </div>
  );
}
