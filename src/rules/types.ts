import { Card } from '../models/Card';
import { Build } from '../models/Build';

/**
 * Result of a game action (capture, build, discard, trotta)
 */
export class ActionResult {
  played: Card;
  captured: Card[];
  mullePairs: Card[][];
  buildCreated: boolean;

  constructor(
    played: Card,
    captured: Card[] = [],
    mullePairs: Card[][] = [],
    buildCreated: boolean = false
  ) {
    this.played = played;
    this.captured = captured;
    this.mullePairs = mullePairs;
    this.buildCreated = buildCreated;
  }

  toString(): string {
    const capturedCodes = this.captured.map(c => c.code()).join(',');
    const mulleStr = this.mullePairs.map(pair => 
      `[${pair.map(c => c.code()).join(',')}]`
    ).join(',');
    return `Action(played=${this.played.code()}, captured=[${capturedCodes}], mulles=[${mulleStr}], build=${this.buildCreated})`;
  }
}

/**
 * Candidate action for AI decision-making
 */
export class CandidateAction {
  category: string;
  predictedReward: number;
  private executor: () => ActionResult;

  constructor(
    category: string,
    predictedReward: number,
    executor: () => ActionResult
  ) {
    this.category = category;
    this.predictedReward = predictedReward;
    this.executor = executor;
  }

  /**
   * Execute this action
   */
  execute(): ActionResult {
    return this.executor();
  }

  toString(): string {
    return `CandidateAction(cat=${this.category}, reward=${this.predictedReward})`;
  }
}
