export type Rank =
  | 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K';

// Swedish suit codes
export type Suit = 'KL' | 'SP' | 'HJ' | 'RU'; // Klöver, Spader, Hjärter, Ruter

const RANK_VALUES_BOARD: Record<Rank, number> = {
  '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
  '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1  // Ace=1 on board
};

export class Card {
  readonly suit: Suit;
  readonly rank: Rank;
  readonly deckId: number; // distinguish duplicates across two decks
  readonly id: string;

  private static readonly SPECIAL_HAND_VALUES: Map<string, number> = new Map([
    ['SP:2', 15],   // Spader 2 = 15 in hand
    ['RU:10', 16]   // Ruter 10 = 16 in hand
  ]);

  constructor(suit: Suit, rank: Rank, deckId: number) {
    this.suit = suit;
    this.rank = rank;
    this.deckId = deckId;
    this.id = `${suit}${rank}${deckId}`;
  }

  /**
   * Get the value of this card when on the board
   */
  valueOnBoard(): number {
    return RANK_VALUES_BOARD[this.rank];
  }

  /**
   * Get the value of this card when in hand (for capture calculations)
   */
  valueInHand(): number {
    // Ace=14 in hand
    if (this.rank === 'A') {
      return 14;
    }
    const key = `${this.suit}:${this.rank}`;
    return Card.SPECIAL_HAND_VALUES.get(key) ?? this.valueOnBoard();
  }

  /**
   * Get the short code for this card (e.g. "SP A")
   */
  code(): string {
    return `${this.suit} ${this.rank}`;
  }

  /**
   * String representation for debugging
   */
  toString(): string {
    return this.code();
  }

  /**
   * Check if two cards are identical (same suit, rank, and deck)
   */
  equals(other: Card): boolean {
    return this.suit === other.suit && 
           this.rank === other.rank && 
           this.deckId === other.deckId;
  }

  /**
   * Check if two cards match (same suit and rank, ignoring deck)
   */
  matches(other: Card): boolean {
    return this.suit === other.suit && this.rank === other.rank;
  }
}