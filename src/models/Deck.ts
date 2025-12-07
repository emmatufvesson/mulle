import { Card, Rank, Suit } from './Card';

export class Deck {
  private cards: Card[];

  constructor(cards?: Card[]) {
    this.cards = cards ? [...cards] : Deck.standard();
  }

  static standard(): Card[] {
    const suits: Suit[] = ['hearts', 'diamonds', 'clubs', 'spades'];
    const ranks: Rank[] = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
    const cards: Card[] = [];
    for (const s of suits) {
      for (const r of ranks) {
        cards.push(new Card(r, s));
      }
    }
    return cards;
  }

  shuffle(seedRandom?: () => number): void {
    // Fisher–Yates
    const rand = seedRandom ?? Math.random;
    for (let i = this.cards.length - 1; i > 0; i--) {
      const j = Math.floor(rand() * (i + 1));
      [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
    }
  }

  draw(count = 1): Card[] {
    const drawn: Card[] = [];
    for (let i = 0; i < count; i++) {
      const c = this.cards.shift();
      if (!c) break;
      drawn.push(c);
    }
    return drawn;
  }

  size(): number {
    return this.cards.length;
  }

  asArray(): Card[] {
    return [...this.cards];
  }
}