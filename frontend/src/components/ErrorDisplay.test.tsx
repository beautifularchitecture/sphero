import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { ErrorDisplay } from './ErrorDisplay';
import type { ErrorReport } from '../types';

const error: ErrorReport = {
  type: 'backend',
  message: 'Unrecognized message',
  timestamp: '2026-11-14T12:00:00Z',
};

describe('ErrorDisplay (BR1.5.4, NFR1.2)', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  it('Given an error report, When ErrorDisplay renders, Then escaped type, message and timestamp are shown', () => {
    render(<ErrorDisplay error={error} />);

    expect(screen.getByTestId('error-display')).toBeInTheDocument();
    expect(screen.getByTestId('error-type').textContent).toBe('backend');
    expect(screen.getByTestId('error-message').textContent).toBe(
      'Unrecognized message'
    );
    expect(screen.getByTestId('error-timestamp').textContent).toBe(
      '2026-11-14T12:00:00Z'
    );
  });

  it('Given no error, When ErrorDisplay renders, Then it renders nothing', () => {
    const { container } = render(<ErrorDisplay error={null} />);

    expect(container.querySelector('[data-testid="error-display"]')).toBeNull();
    expect(container.innerHTML).toBe('');
  });

  it('Given an error message containing HTML, When ErrorDisplay renders, Then the markup is escaped and never injected as raw HTML', () => {
    const htmlError: ErrorReport = {
      ...error,
      message: '<img src=x onerror=alert(1)>boom</img>',
    };
    render(<ErrorDisplay error={htmlError} />);

    const message = screen.getByTestId('error-message');
    expect(message.textContent).toContain('<img src=x onerror=alert(1)>boom</img>');
    expect(message.querySelector('img')).toBeNull();
    expect(message.innerHTML).not.toContain('<img');
  });

  it('Given an error with empty fields, When ErrorDisplay renders, Then fields render as-is (errors are not dashed like telemetry)', () => {
    const emptyError: ErrorReport = { type: '', message: '', timestamp: '' };
    render(<ErrorDisplay error={emptyError} />);

    expect(screen.getByTestId('error-type').textContent).toBe('');
    expect(screen.getByTestId('error-message').textContent).toBe('');
    expect(screen.getByTestId('error-timestamp').textContent).toBe('');
  });
});
