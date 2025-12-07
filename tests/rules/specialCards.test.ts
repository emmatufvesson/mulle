import { Board } from '../../src/models/Board';
import { Card } from '../../src/models/Card';
import { Player } from '../../src/models/Player';
import { generateCaptureCombinations } from '../../src/rules/capture';

describe('Special cards rules (A/Sp2/Ru10)', () => {
  test('specials can only be captured via builds of their hand value', () => {
    const board = new Board();
    const p = new Player('P');
    const aceSpades = new Card('SP', 'A', 0); // board value 1, hand 14
    const sp2 = new Card('SP', '2', 0); // board 2, hand 15
    const ru10 = new Card('RU', '10', 0); // board 10, hand 16
    board.addCard(aceSpades);
    board.addCard(sp2);
    board.addCard(ru10);

    // Play same exact singles should NOT be allowed as capture combos
    const combosA = generateCaptureCombinations(board, new Card('SP', 'A', 1));
    const combosSp2 = generateCaptureCombinations(board, new Card('SP', '2', 1));
    const combosRu10 = generateCaptureCombinations(board, new Card('RU', '10', 1));
    expect(combosA.length).toBe(0);
    expect(combosSp2.length).toBe(0);
    expect(combosRu10.length).toBe(0);
  });
});
