import { GameEngine } from '../../src/engine/GameEngine';
import { Deck } from '../../src/models/Deck';
function makeDeterministicRng(values: number[]) {
  let i = 0;
  return () => {
    const v = values[i % values.length];
    i++;
    return v;
  };
}

test('constructs with N players and deals correctly', () => {
  const players = [{ id: 'p1', name: 'Alice' }, { id: 'p2', name: 'Bob' }];
  const engine = new GameEngine(players);
  expect(engine.getState().deckSize).toBe(52);
  engine.deal(5);
  const state = engine.getState();
  expect(state.players.find(p => p.id === 'p1')!.handSize).toBe(5);
  expect(state.players.find(p => p.id === 'p2')!.handSize).toBe(5);
  expect(state.deckSize).toBe(52 - 10);
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
  expect(state.deckSize).toBe(50);
});
