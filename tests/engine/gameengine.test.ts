import { GameEngine, PlayerDefinition } from '../../src/engine/GameEngine';

describe('GameEngine', () => {
  describe('Construction', () => {
    test('can be constructed with N players', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
        { id: '3', name: 'Charlie' },
      ];

      const engine = new GameEngine(players);
      const state = engine.getState();

      expect(state.players).toHaveLength(3);
      expect(state.players[0].id).toBe('1');
      expect(state.players[0].name).toBe('Alice');
      expect(state.players[1].id).toBe('2');
      expect(state.players[1].name).toBe('Bob');
      expect(state.players[2].id).toBe('3');
      expect(state.players[2].name).toBe('Charlie');
      expect(state.deckSize).toBe(52);
      expect(state.isStarted).toBe(false);
    });

    test('throws error with no players', () => {
      expect(() => new GameEngine([])).toThrow('At least one player is required');
    });

    test('can be constructed with a single player', () => {
      const players: PlayerDefinition[] = [{ id: '1', name: 'Solo' }];
      const engine = new GameEngine(players);
      const state = engine.getState();

      expect(state.players).toHaveLength(1);
      expect(state.deckSize).toBe(52);
    });
  });

  describe('Shuffle and Deal', () => {
    test('shuffle+deal gives each player correct number of cards and reduces deck size', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
      ];

      const engine = new GameEngine(players);
      engine.shuffle();
      engine.deal(7);

      const state = engine.getState();

      expect(state.players[0].hand.count()).toBe(7);
      expect(state.players[1].hand.count()).toBe(7);
      expect(state.deckSize).toBe(52 - 14);
    });

    test('deal with 3 players and 5 cards each', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
        { id: '3', name: 'Charlie' },
      ];

      const engine = new GameEngine(players);
      engine.shuffle();
      engine.deal(5);

      const state = engine.getState();

      expect(state.players[0].hand.count()).toBe(5);
      expect(state.players[1].hand.count()).toBe(5);
      expect(state.players[2].hand.count()).toBe(5);
      expect(state.deckSize).toBe(52 - 15);
    });

    test('throws error when dealing more cards than available', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
      ];

      const engine = new GameEngine(players);
      expect(() => engine.deal(30)).toThrow(/Not enough cards in deck/);
    });

    test('throws error when dealing zero or negative cards', () => {
      const players: PlayerDefinition[] = [{ id: '1', name: 'Alice' }];
      const engine = new GameEngine(players);

      expect(() => engine.deal(0)).toThrow('Cards per player must be greater than 0');
      expect(() => engine.deal(-1)).toThrow('Cards per player must be greater than 0');
    });
  });

  describe('Game Flow', () => {
    test('startGame initializes state as expected', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
      ];

      const engine = new GameEngine(players);
      engine.startGame();

      const state = engine.getState();

      expect(state.isStarted).toBe(true);
      expect(state.currentPlayerIndex).toBe(0);
    });

    test('throws error when starting game twice', () => {
      const players: PlayerDefinition[] = [{ id: '1', name: 'Alice' }];
      const engine = new GameEngine(players);

      engine.startGame();
      expect(() => engine.startGame()).toThrow('Game has already been started');
    });

    test('endTurn advances current player index', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
        { id: '3', name: 'Charlie' },
      ];

      const engine = new GameEngine(players);
      engine.startGame();

      expect(engine.getState().currentPlayerIndex).toBe(0);

      engine.endTurn();
      expect(engine.getState().currentPlayerIndex).toBe(1);

      engine.endTurn();
      expect(engine.getState().currentPlayerIndex).toBe(2);

      engine.endTurn();
      expect(engine.getState().currentPlayerIndex).toBe(0); // wraps around
    });

    test('throws error when ending turn before game starts', () => {
      const players: PlayerDefinition[] = [{ id: '1', name: 'Alice' }];
      const engine = new GameEngine(players);

      expect(() => engine.endTurn()).toThrow('Game has not been started');
    });
  });

  describe('Deterministic Shuffle', () => {
    test('deterministic shuffle via fake RNG yields predictable dealing', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
      ];

      // Create a simple deterministic RNG that returns 0.5 always
      const fakeRng = () => {
        return 0.5;
      };

      const engine1 = new GameEngine(players);
      engine1.shuffle(fakeRng);
      engine1.deal(5);

      const engine2 = new GameEngine(players);
      engine2.shuffle(fakeRng);
      engine2.deal(5);

      // Both engines should have dealt the same cards to players
      const state1 = engine1.getState();
      const state2 = engine2.getState();

      const alice1Cards = state1.players[0].hand.cardsArray();
      const alice2Cards = state2.players[0].hand.cardsArray();
      const bob1Cards = state1.players[1].hand.cardsArray();
      const bob2Cards = state2.players[1].hand.cardsArray();

      // Check that Alice got the same cards in both games
      for (let i = 0; i < 5; i++) {
        expect(alice1Cards[i].equals(alice2Cards[i])).toBe(true);
      }

      // Check that Bob got the same cards in both games
      for (let i = 0; i < 5; i++) {
        expect(bob1Cards[i].equals(bob2Cards[i])).toBe(true);
      }
    });

    test('different RNG functions produce different results', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
      ];

      const fakeRng1 = () => 0.3;
      const fakeRng2 = () => 0.7;

      const engine1 = new GameEngine(players);
      engine1.shuffle(fakeRng1);
      engine1.deal(5);

      const engine2 = new GameEngine(players);
      engine2.shuffle(fakeRng2);
      engine2.deal(5);

      const state1 = engine1.getState();
      const state2 = engine2.getState();

      const alice1Cards = state1.players[0].hand.cardsArray();
      const alice2Cards = state2.players[0].hand.cardsArray();

      // At least one card should be different
      let hasDifference = false;
      for (let i = 0; i < 5; i++) {
        if (!alice1Cards[i].equals(alice2Cards[i])) {
          hasDifference = true;
          break;
        }
      }

      expect(hasDifference).toBe(true);
    });
  });

  describe('Integration', () => {
    test('complete game flow: construct, shuffle, deal, start, play turns', () => {
      const players: PlayerDefinition[] = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
        { id: '3', name: 'Charlie' },
      ];

      const engine = new GameEngine(players);

      // Initial state
      let state = engine.getState();
      expect(state.isStarted).toBe(false);
      expect(state.deckSize).toBe(52);
      expect(state.players).toHaveLength(3);
      expect(state.players[0].hand.count()).toBe(0);

      // Shuffle and deal
      engine.shuffle();
      engine.deal(7);

      state = engine.getState();
      expect(state.deckSize).toBe(52 - 21);
      expect(state.players[0].hand.count()).toBe(7);
      expect(state.players[1].hand.count()).toBe(7);
      expect(state.players[2].hand.count()).toBe(7);

      // Start game
      engine.startGame();
      state = engine.getState();
      expect(state.isStarted).toBe(true);
      expect(state.currentPlayerIndex).toBe(0);

      // Play a few turns
      engine.endTurn();
      expect(engine.getState().currentPlayerIndex).toBe(1);

      engine.endTurn();
      expect(engine.getState().currentPlayerIndex).toBe(2);

      engine.endTurn();
      expect(engine.getState().currentPlayerIndex).toBe(0);
    });
  });
});
