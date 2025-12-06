import { Card } from '../../src/models/Card';
import { Deck } from '../../src/models/Deck';


test('Card equality and toString', () => {
  const c1 = new Card('A','hearts');
  const c2 = new Card('A','hearts');
  expect(c1.equals(c2)).toBe(true);
  expect(c1.toString()).toBe('A of hearts');
});

test('Deck standard size and draw', () => {
  const d = new Deck();
  expect(d.size()).toBe(52);
  const drawn = d.draw(5);
  expect(drawn.length).toBe(5);
  expect(d.size()).toBe(47);
});