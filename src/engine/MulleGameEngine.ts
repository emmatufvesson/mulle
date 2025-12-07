import { Deck } from '../models/Deck';
import { Player } from '../models/Player';
import { Board } from '../models/Board';
import { Card } from '../models/Card';
import { ActionResult } from '../rules/types';
import { 
  autoPlayTurn, 
  performCapture, 
  performBuild, 
  performDiscard,
  generateCaptureCombinations
} from '../rules/capture';
import { scoreRound, ScoreBreakdown } from '../rules/scoring';

export interface GameConfig {
  playerNames: string[];
  cardsPerDeal?: number;
  roundsToWin?: number;
}

export interface RoundState {
  roundNumber: number;
  dealNumber: number;
  currentPlayerIndex: number;
  isRoundOver: boolean;
}

export interface GameSnapshot {
  board: Board;
  players: Player[];
  round: RoundState;
  scores: ScoreBreakdown[];
}

/**
 * Complete game engine for Mulle with full rule integration
 */
export class MulleGameEngine {
  private deck: Deck;
  private board: Board;
  private players: Player[];
  private roundNumber: number;
  private dealNumber: number;
  private currentPlayerIndex: number;
  private cardsPerDeal: number;
  private roundsToWin: number;
  private gameStarted: boolean;

  constructor(config: GameConfig) {
    this.deck = new Deck();
    this.board = new Board();
    this.players = config.playerNames.map(name => new Player(name));
    this.roundNumber = 1;
    this.dealNumber = 1;
    this.currentPlayerIndex = 0;
    this.cardsPerDeal = config.cardsPerDeal ?? 8;
    this.roundsToWin = config.roundsToWin ?? 3;
    this.gameStarted = false;
  }

  /**
   * Start a new game
   */
  startGame(): void {
    if (this.gameStarted) {
      throw new Error('Game already started');
    }
    this.gameStarted = true;
    this.dealCards();
  }

  /**
   * Deal cards to all players and board
   */
  private dealCards(): void {
    // Deal cards to each player
    for (const player of this.players) {
      const cards = this.deck.drawMany(this.cardsPerDeal);
      player.addToHand(cards);
    }

    // Deal 8 cards to the board on first deal
    if (this.dealNumber === 1) {
      for (let i = 0; i < 8; i++) {
        const card = this.deck.draw();
        this.board.addCard(card);
      }
    }
  }

  /**
   * Get current player
   */
  getCurrentPlayer(): Player {
    return this.players[this.currentPlayerIndex];
  }

  /**
   * Check if it's AI's turn
   */
  isAITurn(): boolean {
    // For now, player 0 is human, others are AI
    return this.currentPlayerIndex !== 0;
  }

  /**
   * Execute AI turn automatically
   */
  executeAITurn(): ActionResult {
    const player = this.getCurrentPlayer();
    const result = autoPlayTurn(this.board, player, this.roundNumber);
    this.endTurn();
    return result;
  }

  /**
   * Player performs a capture
   */
  playerCapture(card: Card, pileIndices: number[]): ActionResult {
    const player = this.getCurrentPlayer();
    
    // Validate card is in hand
    if (!player.hand.includes(card)) {
      throw new Error('Card not in player hand');
    }

    // Get piles to capture
    const piles = pileIndices.map(i => this.board.piles[i]);
    
    const result = performCapture(this.board, player, card, piles);
    
    // Check for tabbe (capture from empty board before this capture)
    if (this.board.piles.length + piles.length === piles.length) {
      player.tabbe += 1;
    }
    
    this.endTurn();
    return result;
  }

  /**
   * Player performs a build
   */
  playerBuild(card: Card, pileIndex: number, declaredValue?: number): ActionResult {
    const player = this.getCurrentPlayer();
    
    if (!player.hand.includes(card)) {
      throw new Error('Card not in player hand');
    }

    const pile = this.board.piles[pileIndex];
    const result = performBuild(this.board, player, pile, card, this.roundNumber, declaredValue);
    
    this.endTurn();
    return result;
  }

  /**
   * Player performs a discard
   */
  playerDiscard(card: Card): ActionResult {
    const player = this.getCurrentPlayer();
    
    if (!player.hand.includes(card)) {
      throw new Error('Card not in player hand');
    }

    const result = performDiscard(this.board, player, card);
    this.endTurn();
    return result;
  }

  /**
   * End current player's turn
   */
  private endTurn(): void {
    // Check if all players have empty hands
    const allHandsEmpty = this.players.every(p => p.hand.length === 0);
    
    if (allHandsEmpty) {
      // Check if deck has cards for another deal
      if (this.deck.remaining() >= this.players.length * this.cardsPerDeal) {
        this.dealNumber++;
        this.dealCards();
      } else {
        // Round is over
        this.endRound();
        return;
      }
    }

    // Move to next player
    this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.players.length;
  }

  /**
   * End current round and score
   */
  private endRound(): void {
    // Last player to capture gets remaining cards
    if (this.board.piles.length > 0) {
      const lastCapturer = this.findLastCapturer();
      if (lastCapturer) {
        for (const pile of this.board.piles) {
          const cards = pile instanceof Array ? pile : pile.cards;
          lastCapturer.recordCapture(cards);
        }
        this.board.piles = [];
      }
    }

    // Score the round
    const scores = scoreRound(this.players);
    
    // Check if game is over
    const winner = scores.find(s => s.total >= this.roundsToWin);
    if (winner) {
      // Game over
      return;
    }

    // Start new round
    this.roundNumber++;
    this.dealNumber = 1;
    
    // Reset for new round
    this.deck = new Deck();
    this.board = new Board();
    for (const player of this.players) {
      player.hand = [];
      player.captured = [];
      player.mulles = [];
      player.tabbe = 0;
    }
    
    this.dealCards();
    this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.players.length;
  }

  /**
   * Find the last player who made a capture (for end-of-round bonus)
   */
  private findLastCapturer(): Player | null {
    // Simple heuristic: player with most captures
    let maxCaptures = 0;
    let lastCapturer: Player | null = null;
    
    for (const player of this.players) {
      if (player.captured.length > maxCaptures) {
        maxCaptures = player.captured.length;
        lastCapturer = player;
      }
    }
    
    return lastCapturer;
  }

  /**
   * Get available actions for current player
   */
  getAvailableActions(card: Card): {
    canCapture: boolean;
    captureCombinations: number[][];
    canBuild: number[];
    canDiscard: boolean;
  } {
    // Check captures
    const combos = generateCaptureCombinations(this.board, card);
    const captureCombinations = combos.map(combo =>
      combo.map(pile => this.board.piles.indexOf(pile))
    );

    // Check builds
    const canBuild: number[] = [];
    for (let i = 0; i < this.board.piles.length; i++) {
      const pile = this.board.piles[i];
      // Check if can build - simplified check
      const baseCards = pile instanceof Array ? pile : pile.cards;
      if (baseCards.length === 1) {
        canBuild.push(i);
      }
    }

    return {
      canCapture: captureCombinations.length > 0,
      captureCombinations,
      canBuild,
      canDiscard: combos.length === 0
    };
  }

  /**
   * Get current game snapshot
   */
  getSnapshot(): GameSnapshot {
    return {
      board: this.board,
      players: this.players,
      round: {
        roundNumber: this.roundNumber,
        dealNumber: this.dealNumber,
        currentPlayerIndex: this.currentPlayerIndex,
        isRoundOver: false
      },
      scores: scoreRound(this.players)
    };
  }

  /**
   * Check if game is over
   */
  isGameOver(): boolean {
    const scores = scoreRound(this.players);
    return scores.some(s => s.total >= this.roundsToWin);
  }

  /**
   * Get final scores
   */
  getFinalScores(): ScoreBreakdown[] {
    return scoreRound(this.players);
  }
}
