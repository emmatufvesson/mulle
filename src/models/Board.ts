import { Card } from './Card';
import { Build } from './Build';

/**
 * Type representing a pile on the board.
 * Can be either a list of cards or a Build object.
 */
export type Pile = Card[] | Build;

/**
 * Represents the game board with piles of cards and builds.
 */
export class Board {
  piles: Pile[];

  constructor() {
    this.piles = [];
  }

  /**
   * Add a single card to the board as a new pile
   */
  addCard(card: Card): void {
    this.piles.push([card]);
  }

  /**
   * Add a pile of cards to the board
   */
  addPile(cards: Card[]): void {
    this.piles.push(cards);
  }

  /**
   * Remove a pile from the board
   */
  removePile(pile: Pile): void {
    const index = this.piles.indexOf(pile);
    if (index > -1) {
      this.piles.splice(index, 1);
    }
  }

  /**
   * Create a build from a base pile and an added card.
   * Handles merging with existing builds, absorption of eligible piles.
   * 
   * @param basePile - The base pile (cards or build) to build upon
   * @param addedCard - The card to add to the build
   * @param owner - The player who owns the build
   * @param createdRound - The round number when created
   * @param declaredValue - Optional declared value for up/down building
   * @returns The created or merged build
   */
  createBuild(
    basePile: Pile,
    addedCard: Card,
    owner: string,
    createdRound: number = 1,
    declaredValue?: number
  ): Build {
    // Remove base from board
    const baseCards = basePile instanceof Build ? basePile.cards : basePile;
    this.removePile(basePile);
    const cards = [...baseCards, addedCard];

    // Use declaredValue if provided (for rebuilding open builds with up/down choice)
    // Otherwise calculate from card values
    const targetValue = declaredValue ?? cards.reduce((sum, c) => sum + c.valueOnBoard(), 0);

    // Check if build with this value already exists
    const existingBuilds = this.listBuildsByValue(targetValue);
    if (existingBuilds.length > 0) {
      // Merge into first existing build of same value
      const existing = existingBuilds[0];
      existing.cards.push(...cards);
      // New locking rule: merging piles to same value always locks (value consolidation)
      existing.lock();
      return existing;
    }

    // Initial build (no existing build with this value)
    const newBuild = new Build(cards, owner, targetValue, false, createdRound);

    // Absorb rule: ONLY single cards and 2-card piles/builds can be absorbed
    // 3+ card piles can only be used during capture, not absorbed into builds
    const eligible: Pile[] = [];
    for (const p of this.piles) {
      if (p instanceof Build) {
        // Only 2-card unlocked builds can be absorbed
        if (p.cards.length === 2 && !p.locked) {
          eligible.push(p);
        }
      } else {
        // Only single cards or 2-card piles, NOT 3+ card piles
        if (p.length === 1 || p.length === 2) {
          eligible.push(p);
        }
      }
    }

    const values = eligible.map(p =>
      (p instanceof Build ? p.cards : p).reduce((sum, c) => sum + c.valueOnBoard(), 0)
    );

    const direct = values
      .map((v, i) => (v === targetValue ? i : -1))
      .filter(i => i !== -1);

    const used = new Set(direct);
    const chosenSets: number[][] = direct.map(i => [i]);

    const cand = values
      .map((v, i) => (v < targetValue && !used.has(i) ? i : -1))
      .filter(i => i !== -1);

    // Generate subset masks that sum to targetValue
    const subsetMasks: number[][] = [];
    const generateCombinations = (arr: number[], r: number): number[][] => {
      const result: number[][] = [];
      const combine = (start: number, combo: number[]) => {
        if (combo.length === r) {
          result.push([...combo]);
          return;
        }
        for (let i = start; i < arr.length; i++) {
          combo.push(arr[i]);
          combine(i + 1, combo);
          combo.pop();
        }
      };
      combine(0, []);
      return result;
    };

    for (let r = 1; r <= cand.length; r++) {
      const combos = generateCombinations(cand, r);
      for (const combo of combos) {
        const sum = combo.reduce((s, i) => s + values[i], 0);
        if (sum === targetValue) {
          subsetMasks.push(combo);
        }
      }
    }

    // Backtracking to find maximum disjoint subset
    let bestCombo: number[][] = [];

    const backtrack = (idx: number, current: number[][], usedIndices: Set<number>) => {
      if (current.length > bestCombo.length) {
        bestCombo = current.map(c => [...c]);
      }
      if (idx >= subsetMasks.length) {
        return;
      }
      for (let j = idx; j < subsetMasks.length; j++) {
        const mask = subsetMasks[j];
        const hasOverlap = mask.some(m => usedIndices.has(m));
        if (hasOverlap) {
          continue;
        }
        current.push(mask);
        const newUsed = new Set([...Array.from(usedIndices), ...mask]);
        backtrack(j + 1, current, newUsed);
        current.pop();
      }
    };

    backtrack(0, [], new Set());

    for (const combo of bestCombo) {
      chosenSets.push(combo);
    }

    const absorbFlat = new Set<number>();
    for (const group of chosenSets) {
      for (const idx of group) {
        absorbFlat.add(idx);
      }
    }

    let absorbedAny = false;
    // Sort in reverse to avoid index issues when removing
    const sortedIndices = Array.from(absorbFlat).sort((a, b) => b - a);
    for (const idx of sortedIndices) {
      const pile = eligible[idx];
      const pileCards = pile instanceof Build ? pile.cards : pile;
      newBuild.cards.push(...pileCards);
      this.removePile(pile);
      absorbedAny = true;
    }

    // Lock only if absorption actually occurred (external material pulled in)
    if (absorbedAny) {
      newBuild.lock();
    }

    this.piles.push(newBuild);
    return newBuild;
  }

  /**
   * Get all builds on the board
   */
  listBuilds(): Build[] {
    return this.piles.filter((p): p is Build => p instanceof Build);
  }

  /**
   * Get all builds with a specific value
   */
  listBuildsByValue(value: number): Build[] {
    return this.listBuilds().filter(b => b.value === value);
  }

  /**
   * Check if the board is empty
   */
  isEmpty(): boolean {
    return this.piles.length === 0;
  }

  /**
   * String representation for debugging
   */
  toString(): string {
    return this.piles
      .map((p, idx) => {
        if (p instanceof Build) {
          const state = p.locked ? 'LOCK' : 'OPEN';
          const cards = p.cards.map(c => c.code()).join(',');
          return `[${idx}] BUILD(${state}) owner=${p.owner} v=${p.value} -> [${cards}]`;
        } else {
          const prefix = p.length > 1 ? '+' : '';
          const cards = p.map(c => c.code()).join(',');
          return `[${idx}] ${prefix}[${cards}]`;
        }
      })
      .join('\n');
  }
}
