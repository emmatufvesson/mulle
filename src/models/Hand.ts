import { Card } from './Card';

export class Hand {
  private cards: Card[] = [];

  constructor(cards?: Card[]) {
    if (cards) this.cards = [...cards];
  }

  add(card: Card): void {
    this.cards.push(card);
  }

  remove(card: Card): boolean {
    const idx = this.cards.findIndex(c => c.equals(card));
    if (idx === -1) return false;
    this.cards.splice(idx, 1);
    return true;
  }

  count(): number {
    return this.cards.length;
  }

  cardsArray(): Card[] {
    return [...this.cards];
  }

  clear(): void {
    this.cards = [];
  }
}