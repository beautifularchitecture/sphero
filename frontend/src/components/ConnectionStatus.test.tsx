import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { ConnectionStatus, type ConnectionStatusValue } from './ConnectionStatus';

describe('ConnectionStatus (BR1.5.2, NFR3.4, NFR3.5)', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  it.each([
    ['connected', 'Connected'],
    ['disconnected', 'Disconnected'],
    ['pairing', 'Pairing'],
    ['error', 'Error'],
  ])('Given status %s, When ConnectionStatus renders, Then the label is %s', (status, expectedLabel) => {
    render(<ConnectionStatus status={status as ConnectionStatusValue} />);

    expect(screen.getByTestId('status-label').textContent).toBe(expectedLabel);
    expect(screen.getByTestId('connection-status')).toBeInTheDocument();
  });

  it('Given status reconnecting with attempt 3, When ConnectionStatus renders, Then the attempt counter shows in the label', () => {
    render(<ConnectionStatus status="reconnecting" reconnectAttempt={3} />);

    expect(screen.getByTestId('status-label').textContent).toBe(
      'Reconnecting (attempt 3)'
    );
  });

  it('Given isStale true while disconnected, When ConnectionStatus renders, Then a stale badge is shown', () => {
    render(
      <ConnectionStatus status="disconnected" reconnectAttempt={0} isStale />
    );

    expect(screen.getByTestId('stale-badge')).toBeInTheDocument();
    expect(screen.getByTestId('stale-badge').textContent).toBe('stale');
  });

  it('Given isStale true while reconnecting, When ConnectionStatus renders, Then no extra stale badge duplicates the reconnecting state', () => {
    const { container } = render(
      <ConnectionStatus status="reconnecting" reconnectAttempt={1} isStale />
    );

    expect(container.querySelectorAll('[data-testid="stale-badge"]')).toHaveLength(
      0
    );
  });
});
