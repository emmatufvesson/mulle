import { Card } from './Card';

/**
 * Represents a build in the game.
 * A build is a collection of cards with a declared target value,
 * owned by a specific player.
 */
export class Build {
  cards: Card[];
  owner: string;
  targetValue: number;
  locked: boolean;
  createdRound: number;

  constructor(
    cards: Card[],
    owner: string,
    targetValue: number,
    locked: boolean = false,
    createdRound: number = 1
  ) {
    this.cards = [...cards]; // Create a copy
    this.owner = owner;
    this.targetValue = targetValue;
    this.locked = locked;
    this.createdRound = createdRound;
  }

  /**
   * The value of the build (alias for targetValue)
   */
  get value(): number {
    return this.targetValue;
  }

  /**
   * Add cards to the build (only if unlocked and by owner)
   */
  addCards(cards: Card[], actor: string): void {
    if (this.locked) {
      throw new Error('Cannot modify locked build');
    }
    if (actor !== this.owner) {
      throw new Error('Only owner may extend build');
    }
    this.cards.push(...cards);
  }

  /**
   * Add a card via trotta - allowed even on locked builds
   * Trotta always locks the build
   */
  addTrottaCard(card: Card): void {
    this.cards.push(card);
    this.locked = true;
  }

  /**
   * Lock the build
   */
  lock(): void {
    this.locked = true;
  }

  /**
   * String representation for debugging
   */
  toString(): string {
    const state = this.locked ? 'LOCK' : 'OPEN';
    const cardCodes = this.cards.map(c => c.code()).join(',');
    return `Build(${state},owner=${this.owner},v=${this.value},cards=[${cardCodes}])`;
  }
}
