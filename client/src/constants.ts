/**
 * Suit symbols for card display
 */
export const SUIT_SYMBOLS: Record<string, string> = {
  'SP': '♠',
  'HJ': '♥',
  'RU': '♦',
  'KL': '♣'
};

/**
 * Rank labels for display (J, Q, K, A)
 */
export const RANK_LABELS: Record<string, string> = {
  'J': 'J',
  'Q': 'Q',
  'K': 'K',
  'A': 'A'
};

/**
 * Get display label for a rank
 */
export function getRankLabel(rank: string): string {
  return RANK_LABELS[rank] || rank;
}

/**
 * Check if suit is red (Hearts or Diamonds)
 */
export function isRedSuit(suit: string): boolean {
  return suit === 'HJ' || suit === 'RU';
}
