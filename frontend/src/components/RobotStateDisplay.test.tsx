import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { RobotStateDisplay } from './RobotStateDisplay';

describe('RobotStateDisplay (BR1.5.1, BR1.5.3, NFR1.2)', () => {
  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    cleanup();
  });

  it('Given a complete RobotState, When RobotStateDisplay renders, Then every telemetry value is shown', () => {
    render(
      <RobotStateDisplay
        direction="forward"
        orientation={45}
        color="blue"
        position="[1.2, 3.4]"
        timestamp="2026-11-14T12:00:00Z"
      />
    );

    expect(screen.getByTestId('value-direction').textContent).toBe('forward');
    expect(screen.getByTestId('value-orientation').textContent).toBe('45°');
    expect(screen.getByTestId('value-color').textContent).toBe('blue');
    expect(screen.getByTestId('value-position').textContent).toBe('[1.2, 3.4]');
    expect(screen.getByTestId('value-timestamp').textContent).toBe(
      '2026-11-14T12:00:00Z'
    );
  });

  it('Given missing fields (empty strings), When RobotStateDisplay renders, Then those fields show as dashes', () => {
    render(
      <RobotStateDisplay
        direction=""
        orientation=""
        color=""
        position=""
        timestamp="2026-11-14T12:00:00Z"
      />
    );

    expect(screen.getByTestId('value-direction').textContent).toBe('-');
    expect(screen.getByTestId('value-orientation').textContent).toBe('-');
    expect(screen.getByTestId('value-color').textContent).toBe('-');
    expect(screen.getByTestId('value-position').textContent).toBe('-');
  });

  it('Given undefined fields, When RobotStateDisplay renders, Then those fields show as dashes', () => {
    render(
      <RobotStateDisplay
        direction={undefined as unknown as string}
        orientation={undefined as unknown as string}
        color={undefined as unknown as string}
        position={undefined as unknown as string}
        timestamp="2026-11-14T12:00:00Z"
      />
    );

    expect(screen.getByTestId('value-direction').textContent).toBe('-');
    expect(screen.getByTestId('value-orientation').textContent).toBe('-');
    expect(screen.getByTestId('value-color').textContent).toBe('-');
    expect(screen.getByTestId('value-position').textContent).toBe('-');
  });

  it('Given telemetry text containing HTML, When RobotStateDisplay renders, Then the value is React-escaped and never rendered as raw HTML', () => {
    render(
      <RobotStateDisplay
        direction="<script>alert(1)</script>"
        orientation=""
        color=""
        position=""
        timestamp="2026-11-14T12:00:00Z"
      />
    );

    const directionValue = screen.getByTestId('value-direction');
    expect(directionValue.textContent).toContain('<script>alert(1)</script>');
    expect(directionValue.querySelector('script')).toBeNull();
    expect(directionValue.innerHTML).not.toContain('<script');
  });
});
