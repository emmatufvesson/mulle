import { MulleGameEngine } from '../../src/engine/MulleGameEngine';

describe('Deal flow per MULLE_REGLER.md', () => {
  test('first deal: 8 to each player and 8 open on board', () => {
    const engine = new MulleGameEngine({ playerNames: ['A','B'], cardsPerDeal: 8 });
    engine.startGame();
    const snap = engine.getSnapshot();
    expect(snap.players[0].hand.length).toBe(8);
    expect(snap.players[1].hand.length).toBe(8);
    expect(snap.board.piles.length).toBe(8);
    expect(snap.round.dealNumber).toBe(1);
  });
});
