import { LAN_RISK_BANNER_TEXT } from '../constants';

/**
 * LanRiskBanner (NFR1.4).
 *
 * Always-visible, non-dismissible banner that documents the accepted risk of
 * the unauthenticated LAN WebSocket. Content is static in-repo copy — it is
 * never sourced from network payloads — and it has no dismiss/close control so
 * it remains visible for the lifetime of the page in every connection state.
 */
export function LanRiskBanner() {
  return (
    <div
      className="p-3 mb-2 border border-amber-200 bg-amber-50 text-amber-900 rounded"
      data-testid="lan-risk-banner"
      role="status"
      aria-live="polite"
    >
      {LAN_RISK_BANNER_TEXT}
    </div>
  );
}
