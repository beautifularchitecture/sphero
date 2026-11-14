import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { LanRiskBanner } from './LanRiskBanner';

describe('LanRiskBanner (NFR1.4)', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  it('Given the stats panel renders, When LanRiskBanner mounts, Then the static LAN risk text is visible', () => {
    render(<LanRiskBanner />);

    const banner = screen.getByTestId('lan-risk-banner');
    expect(banner).toBeInTheDocument();
    expect(banner.textContent).toContain(
      'LAN-only design: unauthenticated WebSocket.'
    );
    expect(banner.textContent).toContain(
      'Anyone on this LAN can read robot telemetry and send movement commands.'
    );
  });

  it('Given LanRiskBanner is rendered, When inspected, Then the banner is always visible and non-dismissible', () => {
    const { container } = render(<LanRiskBanner />);

    expect(container.firstChild).toHaveAttribute('data-testid', 'lan-risk-banner');
    expect(container.querySelector('button')).toBeNull();
    expect(container.querySelector('[aria-label*=dismiss]')).toBeNull();
    expect(container.querySelector('[data-testid*=dismiss]')).toBeNull();
    expect(container.querySelector('[data-testid*=close]')).toBeNull();
  });

  it('Given any connection state, When LanRiskBanner renders, Then the banner text never comes from a network payload', () => {
    render(<LanRiskBanner />);

    const banner = screen.getByTestId('lan-risk-banner');
    expect(banner.textContent).toBe(
      'LAN-only design: unauthenticated WebSocket. Anyone on this LAN can read robot telemetry and send movement commands.'
    );
  });
});
