import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import { SpeedColorSelector } from './SpeedColorSelector';

describe('SpeedColorSelector (BR1.5.5)', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  it('Given a speed button click, When the user selects low/medium/high, Then onSendChatCommand is called with set speed <level> exactly', () => {
    const onSendChatCommand = vi.fn();
    render(<SpeedColorSelector onSendChatCommand={onSendChatCommand} />);

    fireEvent.click(screen.getByTestId('speed-btn-low'));
    expect(onSendChatCommand).toHaveBeenLastCalledWith('set speed low');

    fireEvent.click(screen.getByTestId('speed-btn-medium'));
    expect(onSendChatCommand).toHaveBeenLastCalledWith('set speed medium');

    fireEvent.click(screen.getByTestId('speed-btn-high'));
    expect(onSendChatCommand).toHaveBeenLastCalledWith('set speed high');
    expect(onSendChatCommand).toHaveBeenCalledTimes(3);
  });

  it('Given a color button click, When the user selects red/blue/green, Then onSendChatCommand is called with set color <color> exactly', () => {
    const onSendChatCommand = vi.fn();
    render(<SpeedColorSelector onSendChatCommand={onSendChatCommand} />);

    fireEvent.click(screen.getByTestId('color-btn-red'));
    expect(onSendChatCommand).toHaveBeenLastCalledWith('set color red');

    fireEvent.click(screen.getByTestId('color-btn-blue'));
    expect(onSendChatCommand).toHaveBeenLastCalledWith('set color blue');

    fireEvent.click(screen.getByTestId('color-btn-green'));
    expect(onSendChatCommand).toHaveBeenLastCalledWith('set color green');
    expect(onSendChatCommand).toHaveBeenCalledTimes(3);
  });

  it('Given the SpeedColorSelector renders, Then it does not call U1 directly — only the provided callback', () => {
    const onSendChatCommand = vi.fn();
    render(<SpeedColorSelector onSendChatCommand={onSendChatCommand} />);

    expect(onSendChatCommand).not.toHaveBeenCalled();
    expect(screen.getByTestId('speed-selector')).toBeInTheDocument();
    expect(screen.getByTestId('color-selector')).toBeInTheDocument();
  });

  it('Given disabled is true, When buttons are clicked, Then no chat command is emitted', () => {
    const onSendChatCommand = vi.fn();
    render(<SpeedColorSelector onSendChatCommand={onSendChatCommand} disabled />);

    fireEvent.click(screen.getByTestId('speed-btn-low'));
    fireEvent.click(screen.getByTestId('color-btn-blue'));
    expect(onSendChatCommand).not.toHaveBeenCalled();
    expect(screen.getByTestId('speed-btn-low')).toBeDisabled();
    expect(screen.getByTestId('color-btn-blue')).toBeDisabled();
  });
});
