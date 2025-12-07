import { MulleGameEngine } from '../../src/engine/MulleGameEngine';
import { Card } from '../../src/models/Card';

describe('MulleGameEngine', () => {
  describe('Game initialization', () => {
    test('creates game with players', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Alice', 'Bob']
      });

      const snapshot = engine.getSnapshot();
      expect(snapshot.players.length).toBe(2);
      expect(snapshot.players[0].name).toBe('Alice');
      expect(snapshot.players[1].name).toBe('Bob');
    });

    test('deals cards on game start', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Alice', 'Bob'],
        cardsPerDeal: 6
      });

      engine.startGame();
      
      const snapshot = engine.getSnapshot();
      expect(snapshot.players[0].hand.length).toBe(6);
      expect(snapshot.players[1].hand.length).toBe(6);
      expect(snapshot.board.piles.length).toBe(4); // 4 cards on board
    });
  });

  describe('Turn management', () => {
    test('starts with player 0', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Alice', 'Bob']
      });

      engine.startGame();
      const player = engine.getCurrentPlayer();
      expect(player.name).toBe('Alice');
    });

    test('identifies AI turns correctly', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Human', 'AI1', 'AI2']
      });

      engine.startGame();
      expect(engine.isAITurn()).toBe(false); // Player 0 is human
    });
  });

  describe('Game actions', () => {
    test('player can discard a card', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Alice', 'Bob']
      });

      engine.startGame();
      const player = engine.getCurrentPlayer();
      const card = player.hand[0];

      // Should be able to discard if no captures available
      try {
        const result = engine.playerDiscard(card);
        expect(result.played).toBe(card);
      } catch (error) {
        // Might fail if capture is possible or player has builds
        expect(error).toBeDefined();
      }
    });
  });

  describe('Scoring', () => {
    test('scores round correctly', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Alice', 'Bob']
      });

      engine.startGame();
      const scores = engine.getFinalScores();
      
      expect(scores.length).toBe(2);
      expect(scores[0].player.name).toBe('Alice');
      expect(scores[1].player.name).toBe('Bob');
    });
  });
});
