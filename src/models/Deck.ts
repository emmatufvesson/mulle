import { Card, Rank, Suit } from './Card';

/**
 * Deck class representing two standard 52-card decks (104 cards total)
 */
export class Deck {
  private cards: Card[];

  constructor(seed?: number) {
    this.cards = Deck.createTwoDecks();
    if (seed !== undefined) {
      this.shuffle(this.seededRandom(seed));
    } else {
      this.shuffle();
    }
  }

  /**
   * Create two standard 52-card decks with deck IDs
   */
  private static createTwoDecks(): Card[] {
    const suits: Suit[] = ['KL', 'SP', 'HJ', 'RU']; // Swedish suit codes
    const ranks: Rank[] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    const cards: Card[] = [];
    let deckId = 0;

    // Two decks
    for (let duplicate = 0; duplicate < 2; duplicate++) {
      for (const suit of suits) {
        for (const rank of ranks) {
          cards.push(new Card(suit, rank, deckId));
          deckId++;
        }
      }
    }
    return cards;
  }

  /**
   * Simple seeded random generator (LCG)
   */
  private seededRandom(seed: number): () => number {
    let s = seed;
    return () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  }

  /**
   * Shuffle the deck using Fisher-Yates algorithm
   */
  shuffle(seedRandom?: () => number): void {
    const rand = seedRandom ?? (() => Math.random());
    for (let i = this.cards.length - 1; i > 0; i--) {
      const j = Math.floor(rand() * (i + 1));
      [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
    }
  }

  /**
   * Draw a single card from the deck
   */
  draw(): Card {
    const card = this.cards.pop();
    if (!card) {
      throw new Error('Deck empty');
    }
    return card;
  }

  /**
   * Draw multiple cards from the deck
   */
  drawMany(count: number): Card[] {
    const drawn: Card[] = [];
    for (let i = 0; i < count; i++) {
      if (this.cards.length === 0) break;
      drawn.push(this.draw());
    }
    return drawn;
  }

  /**
   * Get the number of remaining cards
   */
  remaining(): number {
    return this.cards.length;
  }

  /**
   * Get a copy of all cards in the deck
   */
  asArray(): Card[] {
    return [...this.cards];
  }
}