import { Card } from '../../src/models/Card';
import { Board } from '../../src/models/Board';
import { Player } from '../../src/models/Player';
import { detectMulles, generateCaptureCombinations } from '../../src/rules/capture';
import { INTAKE_POINTS_1, INTAKE_POINTS_2 } from '../../src/rules/scoring';

describe('Rule Integrity Tests', () => {
  describe('Special card values', () => {
    test('Ace has different values on board vs in hand', () => {
      const ace = new Card('KL', 'A', 0);
      expect(ace.valueOnBoard()).toBe(1);
      expect(ace.valueInHand()).toBe(14);
    });

    test('SP 2 has special hand value', () => {
      const sp2 = new Card('SP', '2', 1);
      expect(sp2.valueOnBoard()).toBe(2);
      expect(sp2.valueInHand()).toBe(15);
    });

    test('RU 10 has special hand value', () => {
      const ru10 = new Card('RU', '10', 2);
      expect(ru10.valueOnBoard()).toBe(10);
      expect(ru10.valueInHand()).toBe(16);
    });
  });

  describe('Intake points tables', () => {
    test('INTAKE_POINTS_1 contains SP and other suits', () => {
      expect('SP' in INTAKE_POINTS_1).toBe(true);
      expect(INTAKE_POINTS_1['SP']).toContain('3');
      expect(INTAKE_POINTS_1['SP']).toContain('K');
    });

    test('INTAKE_POINTS_1 contains aces in RU, HJ, KL', () => {
      expect(INTAKE_POINTS_1['RU']).toContain('A');
      expect(INTAKE_POINTS_1['HJ']).toContain('A');
      expect(INTAKE_POINTS_1['KL']).toContain('A');
    });

    test('INTAKE_POINTS_2 contains special cards', () => {
      expect(INTAKE_POINTS_2['SP']).toContain('2');
      expect(INTAKE_POINTS_2['SP']).toContain('A');
      expect(INTAKE_POINTS_2['RU']).toContain('10');
    });
  });

  describe('Mulle detection', () => {
    test('Three identical cards do not form a mulle', () => {
      const cards = [
        new Card('KL', '5', 0),
        new Card('KL', '5', 1),
        new Card('KL', '5', 2)
      ];
      const pairs = detectMulles(cards, cards[0]);
      expect(pairs).toEqual([]);
    });

    test('Exactly two identical cards form one mulle', () => {
      const cards = [
        new Card('SP', '6', 3),
        new Card('SP', '6', 4)
      ];
      const pairs = detectMulles(cards, cards[0]);
      expect(pairs.length).toBe(1);
      expect(pairs[0].length).toBe(2);
      expect(pairs[0][0].matches(pairs[0][1])).toBe(true);
    });

    test('Four identical cards form NO mulles (must be exactly 2)', () => {
      const cards = [
        new Card('HJ', '7', 0),
        new Card('HJ', '7', 1),
        new Card('HJ', '7', 2),
        new Card('HJ', '7', 3)
      ];
      const pairs = detectMulles(cards, cards[0]);
      // 4 cards = no mulle (must be exactly 2)
      expect(pairs.length).toBe(0);
    });
  });

  describe('Capture combinations do not modify card values', () => {
    test('Card values remain unchanged after generating combinations', () => {
      const board = new Board();
      
      // Cards with total board value 12: 7+4+1 (Ace on board = 1)
      const c7 = new Card('SP', '7', 10);
      const c4 = new Card('HJ', '4', 11);
      const ca = new Card('KL', 'A', 12);
      
      board.addCard(c7);
      board.addCard(c4);
      board.addCard(ca);
      
      const player = new Player('Anna');
      const queen = new Card('RU', 'Q', 13);
      player.addToHand([queen]);
      
      const combos = generateCaptureCombinations(board, queen);
      
      // Verify values unchanged
      expect(c7.valueOnBoard()).toBe(7);
      expect(queen.valueInHand()).toBe(12);
      
      // Verify combination exists
      expect(combos.length).toBeGreaterThan(0);
    });
  });
});
