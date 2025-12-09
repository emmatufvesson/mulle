import { Card } from '../../src/models/Card';
import { Deck } from '../../src/models/Deck';


test('Card equality and toString', () => {
  const c1 = new Card('SP', '2', 0);
  const c2 = new Card('SP', '2', 0);
  expect(c1.equals(c2)).toBe(true);
  expect(c1.toString()).toBe('SP 2');
});

test('Deck standard size and draw', () => {
  const d = new Deck();
  expect(d.remaining()).toBe(104); // Two decks = 104 cards
  const drawn = d.drawMany(5);
  expect(drawn.length).toBe(5);
  expect(d.remaining()).toBe(99);
});
