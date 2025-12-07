import { Player } from '../../src/models/Player';
import { Card } from '../../src/models/Card';
import { scoreRound } from '../../src/rules/scoring';

describe('Scoring rules', () => {
  test('mulle + tabbe + intake bonus totals', () => {
    const p1 = new Player('A');
    const p2 = new Player('B');
    // Register one mulle for p1
    p1.recordMulle(new Card('SP','A', 0));
    // Intake: give p1 >20 intake cards to trigger bonus (simulate by marking captured list)
    const intakeCards = [
      new Card('SP','3',0), new Card('SP','4',0), new Card('SP','5',0), new Card('SP','6',0), new Card('SP','7',0),
      new Card('SP','8',0), new Card('SP','9',0), new Card('SP','10',0), new Card('SP','J',0), new Card('SP','Q',0), new Card('SP','K',0),
      new Card('RU','A',0), new Card('HJ','A',0), new Card('KL','A',0), new Card('SP','2',0), new Card('SP','A',0), new Card('RU','10',0),
      // add extras to exceed 20
      new Card('SP','3',1), new Card('SP','4',1), new Card('SP','5',1), new Card('SP','6',1),
    ];
    p1.captured.push(...intakeCards);
    p1.tabbe = 2;
    const scores = scoreRound([p1,p2]);
    const s1 = scores.find(s => s.player.name==='A')!;
    expect(s1.mullePoints).toBe(14);
    expect(s1.tabbe).toBe(2);
    expect(s1.intake).toBeGreaterThan(20);
    expect(s1.bonus).toBeGreaterThan(0);
    expect(s1.total).toBe(s1.mullePoints + s1.tabbe + s1.bonus);
  });
});
