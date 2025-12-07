import { Card } from '../../src/models/Card';
import { Board } from '../../src/models/Board';
import { Player } from '../../src/models/Player';
import { 
  boardPileValue, 
  canBuild, 
  performCapture,
  performBuild,
  generateCaptureCombinations
} from '../../src/rules/capture';

describe('Capture Tests', () => {
  describe('boardPileValue', () => {
    test('calculates value for single card pile', () => {
      const board = new Board();
      const card = new Card('SP', '5', 0);
      board.addCard(card);
      
      const pile = board.piles[0];
      expect(boardPileValue(pile)).toBe(5);
    });

    test('calculates value for multi-card pile', () => {
      const pile = [
        new Card('SP', '3', 0),
        new Card('HJ', '4', 1)
      ];
      expect(boardPileValue(pile)).toBe(7);
    });
  });

  describe('generateCaptureCombinations', () => {
    test('finds single direct match', () => {
      const board = new Board();
      board.addCard(new Card('SP', '5', 0));
      
      const player = new Player('Anna');
      const card5 = new Card('HJ', '5', 1);
      
      const combos = generateCaptureCombinations(board, card5);
      
      expect(combos.length).toBe(1);
      expect(combos[0].length).toBe(1);
    });

    test('finds combination that sums to target', () => {
      const board = new Board();
      board.addCard(new Card('SP', '3', 0));
      board.addCard(new Card('HJ', '4', 1));
      
      const player = new Player('Anna');
      const card7 = new Card('KL', '7', 2);
      
      const combos = generateCaptureCombinations(board, card7);
      
      expect(combos.length).toBe(1);
      expect(combos[0].length).toBe(2); // Both piles captured
    });

    test('special values 14/15/16 cannot be captured without build', () => {
      const board = new Board();
      board.addCard(new Card('SP', '7', 0));
      board.addCard(new Card('HJ', '7', 1));
      
      const ace = new Card('KL', 'A', 2); // Hand value = 14
      const combos = generateCaptureCombinations(board, ace);
      
      // Should return empty because 14 requires a build
      expect(combos).toEqual([]);
    });
  });

  describe('canBuild', () => {
    test('can build on single card pile', () => {
      const board = new Board();
      const card3 = new Card('SP', '3', 0);
      board.addCard(card3);
      
      const player = new Player('Anna');
      const card4 = new Card('HJ', '4', 1);
      const card7 = new Card('KL', '7', 2); // Reservation card
      player.addToHand([card4, card7]);
      
      const pile = board.piles[0];
      expect(canBuild(board, player, pile, card4)).toBe(true);
    });

    test('cannot build without reservation card', () => {
      const board = new Board();
      const card3 = new Card('SP', '3', 0);
      board.addCard(card3);
      
      const player = new Player('Anna');
      const card4 = new Card('HJ', '4', 1);
      player.addToHand([card4]); // No reservation card!
      
      const pile = board.piles[0];
      expect(canBuild(board, player, pile, card4)).toBe(false);
    });

    test('cannot build on multi-card pile (non-build)', () => {
      const board = new Board();
      const pile = [
        new Card('SP', '3', 0),
        new Card('HJ', '4', 1)
      ];
      board.piles.push(pile);
      
      const player = new Player('Anna');
      const card5 = new Card('KL', '5', 2);
      const card12 = new Card('RU', 'Q', 3);
      player.addToHand([card5, card12]);
      
      expect(canBuild(board, player, pile, card5)).toBe(false);
    });
  });

  describe('performCapture', () => {
    test('captures single card and adds to player', () => {
      const board = new Board();
      const card5 = new Card('SP', '5', 0);
      board.addCard(card5);
      
      const player = new Player('Anna');
      const playerCard5 = new Card('HJ', '5', 1);
      player.addToHand([playerCard5]);
      
      const pile = board.piles[0];
      const result = performCapture(board, player, playerCard5, [pile]);
      
      expect(result.played).toBe(playerCard5);
      expect(result.captured.length).toBe(2); // Both cards
      expect(player.captured.length).toBe(2);
      expect(board.piles.length).toBe(0);
    });

    test('detects mulle when capturing identical card', () => {
      const board = new Board();
      const card5 = new Card('SP', '5', 0);
      board.addCard(card5);
      
      const player = new Player('Anna');
      const playerCard5 = new Card('SP', '5', 1);
      player.addToHand([playerCard5]);
      
      const pile = board.piles[0];
      const result = performCapture(board, player, playerCard5, [pile]);
      
      expect(result.mullePairs.length).toBe(1);
      expect(player.mulles.length).toBe(1);
    });
  });

  describe('performBuild', () => {
    test('creates a new build', () => {
      const board = new Board();
      const card3 = new Card('SP', '3', 0);
      board.addCard(card3);
      
      const player = new Player('Anna');
      const card4 = new Card('HJ', '4', 1);
      const card7 = new Card('KL', '7', 2);
      player.addToHand([card4, card7]);
      
      const pile = board.piles[0];
      const result = performBuild(board, player, pile, card4, 1);
      
      expect(result.buildCreated).toBe(true);
      expect(board.listBuilds().length).toBe(1);
      expect(board.listBuilds()[0].value).toBe(7);
      expect(board.listBuilds()[0].owner).toBe('Anna');
    });
  });
});
