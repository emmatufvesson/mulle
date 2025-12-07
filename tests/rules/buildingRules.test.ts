import { Board } from '../../src/models/Board';
import { Card } from '../../src/models/Card';
import { Player } from '../../src/models/Player';
import { canBuild, performBuild } from '../../src/rules/capture';

describe('Building rules', () => {
  test('requires reservation card and enforces one build per value', () => {
    const board = new Board();
    const p1 = new Player('A');
    const p2 = new Player('B');
    // Single pile: 5 of hearts
    const h5 = new Card('HJ', '5', 0);
    board.addCard(h5);
    // Player A hand: 9H for build to 14, and A hearts as reservation (14 in hand)
    const h9 = new Card('HJ', '9', 0);
    const aH = new Card('HJ', 'A', 1);
    p1.addToHand([h9, aH]);

    expect(canBuild(board, p1, board.piles[0], h9)).toBe(true);
    performBuild(board, p1, board.piles[0], h9, 1, undefined);

    // Player B cannot build another build of value 14
    const d7 = new Card('RU', '7', 0);
    const d7b = new Card('RU', '7', 1);
    board.addCard(d7);
    p2.addToHand([d7b, new Card('SP','A', 1)]);
    expect(canBuild(board, p2, board.piles[1], d7b)).toBe(false);
  });

  test('locked builds cannot be altered and trotta/build-in locks', () => {
    const board = new Board();
    const p = new Player('P');
    const base = new Card('KL','6', 0);
    board.addCard(base);
    const three = new Card('KL','3', 0);
    const five = new Card('KL','5', 2);
    const nine = new Card('KL','9', 1);
    // Build 6+3 -> 9 (reservation: 9 in hand)
    p.addToHand([three, nine]);
    expect(canBuild(board, p, board.piles[0], three)).toBe(true);
    performBuild(board, p, board.piles[0], three, 1);
    // Trotta: add matching value card to lock (simulate via discard rule handled elsewhere)
    // After locking, further canBuild on that build should be false
    const build = board.listBuilds()[0];
    build.locked = true;
    expect(canBuild(board, p, build as any, five)).toBe(false);
  });
});
