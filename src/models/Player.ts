import { Card } from './Card';

/**
 * Player class representing a game player with hand, captured cards, and score
 */
export class Player {
  name: string;
  hand: Card[];
  captured: Card[];  // All captured cards
  mulles: Card[];    // Cards representing mulle points (one per pair)
  tabbe: number;     // Number of captures from empty board

  constructor(name: string) {
    this.name = name;
    this.hand = [];
    this.captured = [];
    this.mulles = [];
    this.tabbe = 0;
  }

  /**
   * Add cards to hand
   */
  addToHand(cards: Card[]): void {
    this.hand.push(...cards);
  }

  /**
   * Remove a card from hand
   */
  removeFromHand(card: Card): void {
    const index = this.hand.indexOf(card);
    if (index > -1) {
      this.hand.splice(index, 1);
    }
  }

  /**
   * Record a mulle (one card per pair)
   */
  recordMulle(card: Card): void {
    this.mulles.push(card);
  }

  /**
   * Record captured cards
   */
  recordCapture(cards: Card[]): void {
    this.captured.push(...cards);
  }

  /**
   * Calculate total mulle points
   */
  totalMullePoints(): number {
    let points = 0;
    for (const card of this.mulles) {
      if (card.rank === 'A') {
        points += 14;
      } else if (['J', 'Q', 'K'].includes(card.rank)) {
        points += card.valueOnBoard();
      } else {
        points += parseInt(card.rank, 10);
      }
    }
    return points;
  }

  /**
   * String representation
   */
  toString(): string {
    return this.name;
  }
}