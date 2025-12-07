export type Rank =
  | 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K';

export type Suit = 'hearts' | 'diamonds' | 'clubs' | 'spades';

export class Card {
  constructor(public readonly rank: Rank, public readonly suit: Suit) {}

  toString(): string {
    return `${this.rank} of ${this.suit}`;
  }

  equals(other: Card): boolean {
    return this.rank === other.rank && this.suit === other.suit;
  }
}