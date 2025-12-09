import { GameEngine } from '../../src/engine/GameEngine';

function makeDeterministicRng(values: number[]) {
  let i = 0;
  return () => {
    const v = values[i % values.length];
    i++;
    return v;
  };
}

test('constructs with 2 players and deals 5 cards each', () => {
  const players = [{ id: 'p1', name: 'Alice' }, { id: 'p2', name: 'Bob' }];
  const engine = new GameEngine(players);
  expect(engine.getState().deckSize).toBe(104); // Two decks = 104 cards
  engine.deal(5);
  const state = engine.getState();
  expect(state.players.find(p => p.id === 'Alice')!.handSize).toBe(5);
  expect(state.players.find(p => p.id === 'Bob')!.handSize).toBe(5);
  expect(state.deckSize).toBe(104 - 10);
});

test('startGame sets current player and endTurn rotates', () => {
  const players = [{ id: 'p1', name: 'Alice' }, { id: 'p2', name: 'Bob' }, { id: 'p3', name: 'Eve' }];
  const engine = new GameEngine(players);
  expect(engine.getState().started).toBe(false);
  engine.startGame();
  expect(engine.getState().started).toBe(true);
  expect(engine.getState().currentPlayerIndex).toBe(0);
  engine.endTurn();
  expect(engine.getState().currentPlayerIndex).toBe(1);
  engine.endTurn();
  expect(engine.getState().currentPlayerIndex).toBe(2);
  engine.endTurn();
  expect(engine.getState().currentPlayerIndex).toBe(0);
});

test('deterministic shuffle results in predictable dealing', () => {
  const players = [{ id: 'p1', name: 'Alice' }, { id: 'p2', name: 'Bob' }];
  const seed = makeDeterministicRng([0.1, 0.2, 0.3, 0.4]); // predictable sequence
  const engine = new GameEngine(players);
  engine.shuffle(seed);
  engine.deal(1);
  const state = engine.getState();
  expect(state.players.reduce((s, p) => s + p.handSize, 0)).toBe(2);
  expect(state.deckSize).toBe(104 - 2);
});

test('deal throws error when not enough cards in deck', () => {
  const players = [{ id: 'p1', name: 'Alice' }, { id: 'p2', name: 'Bob' }];
  const engine = new GameEngine(players);
  // Try to deal 53 cards per player (106 total) but deck only has 104
  expect(() => engine.deal(53)).toThrow('Not enough cards in deck: need 106 but only 104 available');
});

test('deal throws error when exactly one card short', () => {
  const players = [{ id: 'p1', name: 'Alice' }, { id: 'p2', name: 'Bob' }];
  const engine = new GameEngine(players);
  // Deal 51 cards per player (102 total), leaving 2 in deck
  engine.deal(51);
  // Try to deal 2 more cards per player (4 total) but only 2 remain
  expect(() => engine.deal(2)).toThrow('Not enough cards in deck: need 4 but only 2 available');
});

