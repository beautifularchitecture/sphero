import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import { SpeedColorSelector } from './components/SpeedColorSelector';

describe('Integration: SpeedColorSelector -> chat-command callback', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  it('Given SpeedColorSelector with a callback, When the user picks speed low then color blue, Then the callback receives set speed low / set color blue exactly', () => {
    const onSendChatCommand = vi.fn();
    render(<SpeedColorSelector onSendChatCommand={onSendChatCommand} />);

    fireEvent.click(screen.getByTestId('speed-btn-low'));
    fireEvent.click(screen.getByTestId('color-btn-blue'));

    expect(onSendChatCommand).toHaveBeenCalledWith('set speed low');
    expect(onSendChatCommand).toHaveBeenCalledWith('set color blue');
    expect(onSendChatCommand).toHaveBeenCalledTimes(2);
  });

  it('Given SpeedColorSelector inside StatsPanel, When a color button is clicked, Then onSendChatCommand is forwarded exactly', () => {
    // This boundary is exercised through StatsPanel too; the selector itself
    // owns the command text and never touches U1 directly.
    const onSendChatCommand = vi.fn();
    render(<SpeedColorSelector onSendChatCommand={onSendChatCommand} />);

    fireEvent.click(screen.getByTestId('color-btn-red'));
    expect(onSendChatCommand.mock.calls.map((args) => args[0])).toEqual([
      'set color red',
    ]);
  });
});
