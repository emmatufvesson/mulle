import { Player } from '../models/Player';

/**
 * Cards that give 1 intake point
 */
export const INTAKE_POINTS_1: Record<string, string[]> = {
  'SP': ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
  'RU': ['A'],
  'HJ': ['A'],
  'KL': ['A']
};

/**
 * Cards that give 2 intake points
 */
export const INTAKE_POINTS_2: Record<string, string[]> = {
  'SP': ['2', 'A'],
  'RU': ['10']
};

/**
 * Calculate intake points for a player.
 * Intake points are used for bonus calculation but NOT included in total score.
 */
export function intakePoints(player: Player): number {
  let pts = 0;
  
  for (const card of player.captured) {
    if (card.suit in INTAKE_POINTS_1 && INTAKE_POINTS_1[card.suit].includes(card.rank)) {
      pts += 1;
    }
    if (card.suit in INTAKE_POINTS_2 && INTAKE_POINTS_2[card.suit].includes(card.rank)) {
      pts += 2;
    }
  }
  
  return pts;
}

/**
 * Score breakdown for a player
 */
export class ScoreBreakdown {
  player: Player;
  mullePoints: number;
  tabbe: number;
  intake: number;
  bonus: number;
  total: number;

  constructor(
    player: Player,
    mullePoints: number,
    tabbe: number,
    intake: number,
    bonus: number,
    total: number
  ) {
    this.player = player;
    this.mullePoints = mullePoints;
    this.tabbe = tabbe;
    this.intake = intake;
    this.bonus = bonus;
    this.total = total;
  }

  toString(): string {
    return `Score(${this.player.name}: mulle=${this.mullePoints}, tabbe=${this.tabbe}, intake=${this.intake}, bonus=${this.bonus}, total=${this.total})`;
  }
}

/**
 * Score a round for all players.
 * 
 * Scoring:
 * - Mulle: Sum of all mulle pair values (A=14, J=11, Q=12, K=13, numbers=face value)
 * - Tabbe: Number of captures from empty board
 * - Intake: Sum of intake points (used for bonus, NOT in total)
 * - Bonus: (intake - 20) × 2 if intake > 20
 * - TOTAL: mulle + tabbe + bonus (intake NOT included)
 */
export function scoreRound(players: Player[]): ScoreBreakdown[] {
  const breakdowns: ScoreBreakdown[] = [];
  
  for (const p of players) {
    const mullePts = p.totalMullePoints();
    const tabbePts = p.tabbe;
    const intakePts = intakePoints(p);
    
    let bonus = 0;
    if (intakePts > 20) {
      bonus = (intakePts - 20) * 2;
    }
    
    // Total = mulle + tabbe + bonus (intake NOT counted in total)
    const total = mullePts + tabbePts + bonus;
    
    breakdowns.push(new ScoreBreakdown(p, mullePts, tabbePts, intakePts, bonus, total));
  }
  
  return breakdowns;
}
