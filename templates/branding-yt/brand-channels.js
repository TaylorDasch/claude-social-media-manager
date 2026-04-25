/**
 * Channel branding config — single source of truth for YT banner, profile, outro renderers.
 * Palette mirrors claude-social-media-manager/thumbnails/brand.js
 */

const COLORS = {
  midnight: '#1e293b',
  midnightDeep: '#0f172a',
  emerald: '#059669',
  emeraldDim: '#047857',
  snow: '#f8fafc',
  gold: '#d4a853',
  goldDim: '#b7903d',
  slate: '#64748b',
};

const CHANNELS = {
  living: {
    slug: 'living-in-temple-tx',
    displayName: 'LIVING IN TEMPLE TX',
    eyebrow: 'YOUR TEMPLE, TEXAS LOCAL',
    heroLineA: 'LIVING IN',
    heroLineB: 'TEMPLE, ',
    heroTag: 'TX',
    tagline: 'HOMES · NEIGHBORHOODS · THE TRUTH',
    credential: 'TAYLOR DASCH  ·  EG REALTY  ·  $28.5M+ SOLD  ·  100+ TRANSACTIONS',
    schedule: 'NEW TOURS · WEEKLY',
    scheduleSub: 'Relocation tours · School breakdowns · Neighborhood truth',
    coverage: 'Bell County · Fort Hood · BSW · Texas A&M Central',
    verticalLeft: 'LIVING IN TEMPLE TX  ·  76502  ·  THE POWER ZIP',
    verticalRight: 'EST · TAYLOR DASCH  ·  EG REALTY  ·  TEMPLE TEXAS',
    accent: COLORS.emerald,
    accentDim: COLORS.emeraldDim,
    outroHeading: 'THANKS FOR WATCHING',
    outroSub: 'New Temple, Texas relocation tours every week',
    outroCTA: 'SUBSCRIBE',
  },
  investing: {
    slug: 'investing-in-temple-tx',
    displayName: 'INVESTING IN TEMPLE TX',
    eyebrow: 'ACTIVE INVESTOR · NEVER SALESY',
    heroLineA: 'INVESTING IN',
    heroLineB: 'TEMPLE, ',
    heroTag: 'TX',
    tagline: 'DEALS  ·  NUMBERS  ·  NO HYPE',
    credential: 'TAYLOR DASCH  ·  EG REALTY  ·  $28.5M+ SOLD  ·  BP FEATURED AGENT (3 YRS)',
    schedule: 'NEW DEALS · WEEKLY',
    scheduleSub: 'Flips · BRRRR · MTR · Creative finance breakdowns',
    coverage: 'Bell County · Central Texas · BSW Hospital District · Industrial Corridor',
    verticalLeft: 'INVESTING IN TEMPLE TX  ·  CASH FLOW  ·  TEXAS',
    verticalRight: 'EST · TAYLOR DASCH  ·  BIGGERPOCKETS FEATURED AGENT',
    accent: COLORS.emerald,
    accentDim: COLORS.emeraldDim,
    outroHeading: 'THANKS FOR WATCHING',
    outroSub: 'Real numbers on Temple, TX deals — every week',
    outroCTA: 'SUBSCRIBE',
  },
};

module.exports = { COLORS, CHANNELS };
