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
  
  // Verify the actual cards dealt are in deterministic order
  const enginePlayers = engine.getPlayers();
  const p1 = enginePlayers.find(p => p.id === 'p1');
  const p2 = enginePlayers.find(p => p.id === 'p2');
  expect(p1).toBeDefined();
  expect(p2).toBeDefined();
  
  const p1Cards = p1!.hand.cardsArray();
  const p2Cards = p2!.hand.cardsArray();
  
  // With the given seed sequence, we can verify the first cards dealt
  // The shuffle is deterministic, so the cards should always be the same
  // These hard-coded values are intentional - they verify the shuffle produces
  // the expected deterministic output for the given seed
  expect(p1Cards.length).toBe(1);
  expect(p2Cards.length).toBe(1);
  expect(p1Cards[0].toString()).toBe('3 of spades');
  expect(p2Cards[0].toString()).toBe('7 of clubs');
});
