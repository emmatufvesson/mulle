import { Deck } from '../models/Deck';
import { Player } from '../models/Player';
import { Card } from '../models/Card';

export type PlayerDef = { id: string; name: string };

export interface GameState {
  players: { id: string; name: string; handSize: number }[];
  deckSize: number;
  currentPlayerIndex: number | null;
  started: boolean;
}

export class GameEngine {
  private deck: Deck;
  private players: Player[] = [];
  private currentPlayerIndex: number | null = null;
  private started = false;

  constructor(playerDefs: PlayerDef[], deck?: Deck) {
    this.deck = deck ?? new Deck();
    this.players = playerDefs.map(p => new Player(p.id, p.name));
  }

  // Allows injecting deterministic RNG for tests: function returning number in [0,1)
  shuffle(seedRandom?: () => number): void {
    this.deck.shuffle(seedRandom);
  }

  deal(cardsPerPlayer: number): void {
    for (let i = 0; i < cardsPerPlayer; i++) {
      for (const player of this.players) {
        const drawn = this.deck.draw(1)[0];
        if (drawn) player.hand.add(drawn);
      }
    }
  }

  startGame(): void {
    if (this.started) return;
    this.started = true;
    this.currentPlayerIndex = this.players.length > 0 ? 0 : null;
  }

  endTurn(): void {
    if (this.currentPlayerIndex === null) return;
    this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.players.length;
  }

  playCard(playerId: string, card: Card): boolean {
    const p = this.players.find(pl => pl.id === playerId);
    if (!p) return false;
    return p.playCard(card);
  }

  getState(): GameState {
    return {
      players: this.players.map(p => ({ id: p.id, name: p.name, handSize: p.hand.count() })),
      deckSize: this.deck.size(),
      currentPlayerIndex: this.currentPlayerIndex,
      started: this.started,
    };
  }

  // Expose minimal API for tests.
  // WARNING: This method exposes internal Player objects and allows external mutation.
  // Only use in trusted test code. For production, implement deep copy logic if needed.
  getPlayers(): Player[] {
    return this.players.map(p => p);
  }

  getDeck(): Deck {
    return this.deck;
  }
}
