import { Deck } from '../models/Deck';
import { Player } from '../models/Player';
import { Card } from '../models/Card';

export interface PlayerDefinition {
  id: string;
  name: string;
}

export interface GameState {
  players: Player[];
  deckSize: number;
  isStarted: boolean;
  currentPlayerIndex: number;
}

export class GameEngine {
  private deck: Deck;
  private players: Player[];
  private isStarted: boolean;
  private currentPlayerIndex: number;

  constructor(playerDefinitions: PlayerDefinition[]) {
    if (!playerDefinitions || playerDefinitions.length === 0) {
      throw new Error('At least one player is required');
    }

    this.players = playerDefinitions.map(
      (def) => new Player(def.id, def.name)
    );
    this.deck = new Deck();
    this.isStarted = false;
    this.currentPlayerIndex = 0;
  }

  shuffle(seedRandom?: () => number): void {
    this.deck.shuffle(seedRandom);
  }

  deal(cardsPerPlayer: number): void {
    if (cardsPerPlayer <= 0) {
      throw new Error('Cards per player must be greater than 0');
    }

    const totalCardsNeeded = cardsPerPlayer * this.players.length;
    if (totalCardsNeeded > this.deck.size()) {
      throw new Error(
        `Not enough cards in deck. Need ${totalCardsNeeded}, have ${this.deck.size()}`
      );
    }

    for (let i = 0; i < cardsPerPlayer; i++) {
      for (const player of this.players) {
        const cards = this.deck.draw(1);
        if (cards.length > 0) {
          player.hand.add(cards[0]);
        }
      }
    }
  }

  startGame(): void {
    if (this.isStarted) {
      throw new Error('Game has already been started');
    }
    this.isStarted = true;
    this.currentPlayerIndex = 0;
  }

  endTurn(): void {
    if (!this.isStarted) {
      throw new Error('Game has not been started');
    }
    this.currentPlayerIndex =
      (this.currentPlayerIndex + 1) % this.players.length;
  }

  getState(): GameState {
    return {
      players: this.players,
      deckSize: this.deck.size(),
      isStarted: this.isStarted,
      currentPlayerIndex: this.currentPlayerIndex,
    };
  }
}
