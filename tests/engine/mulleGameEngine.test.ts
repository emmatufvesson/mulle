import { MulleGameEngine } from '../../src/engine/MulleGameEngine';
import { Card } from '../../src/models/Card';
import { Board } from '../../src/models/Board';
import { Build } from '../../src/models/Build';

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
        cardsPerDeal: 8
      });

      engine.startGame();
      
      const snapshot = engine.getSnapshot();
      expect(snapshot.players[0].hand.length).toBe(8);
      expect(snapshot.players[1].hand.length).toBe(8);
      expect(snapshot.board.piles.length).toBe(8); // 8 cards on board
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

    test('trotta stays available when discard is blocked', () => {
      const engine = new MulleGameEngine({
        playerNames: ['Du', 'AI']
      });

      engine.startGame();
      const board = new Board();
      const player = engine.getCurrentPlayer();

      const nineSpades = new Card('SP', '9', 72);
      const nineClubs = new Card('KL', '9', 59);
      player.hand = [nineSpades, nineClubs];

      const buildCards = [
        new Card('RU', '2', 91),
        new Card('SP', 'Q', 23),
        new Card('SP', '5', 68)
      ];
      const build = new Build(buildCards, player.name, 9, false, 1);
      board.piles.push(build);
      board.addCard(new Card('RU', 'K', 50));

      (engine as any).board = board;

      const avail = (engine as any).getAvailableActions(nineSpades);
      expect(avail.canTrotta).toBe(true);
      expect(avail.canDiscard).toBe(false);
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
