import type { SpeedColorSelectorProps } from '../types';

type SpeedLevel = 'low' | 'medium' | 'high';
type ColorValue = 'red' | 'blue' | 'green';

const SPEED_LEVELS: SpeedLevel[] = ['low', 'medium', 'high'];
const COLOR_VALUES: ColorValue[] = ['red', 'blue', 'green'];

/**
 * SpeedColorSelector (BR1.5.5).
 *
 * Inline speed (low/medium/high) and color (red/blue/green) selector buttons.
 * On click it emits `set speed <level>` or `set color <color>` exactly through
 * the consumed onSendChatCommand callback. It does not call U1 directly and
 * does not own the chat-command transport.
 */
export function SpeedColorSelector({
  onSendChatCommand,
  disabled = false,
}: SpeedColorSelectorProps) {
  return (
    <div className="grid grid-cols-3 gap-2" data-testid="speed-color-selector">
      <fieldset disabled={disabled} data-testid="speed-selector">
        <legend className="text-xs font-semibold text-gray-700">Speed</legend>
        {SPEED_LEVELS.map((level) => (
          <button
            key={level}
            type="button"
            data-testid={`speed-btn-${level}`}
            className="px-2 py-1 text-sm border border-gray-300 rounded bg-white"
            disabled={disabled}
            onClick={() => onSendChatCommand(`set speed ${level}`)}
          >
            {level}
          </button>
        ))}
      </fieldset>
      <fieldset disabled={disabled} data-testid="color-selector">
        <legend className="text-xs font-semibold text-gray-700">Color</legend>
        {COLOR_VALUES.map((color) => (
          <button
            key={color}
            type="button"
            data-testid={`color-btn-${color}`}
            className="px-2 py-1 text-sm border border-gray-300 rounded bg-white"
            disabled={disabled}
            onClick={() => onSendChatCommand(`set color ${color}`)}
          >
            {color}
          </button>
        ))}
      </fieldset>
    </div>
  );
}
