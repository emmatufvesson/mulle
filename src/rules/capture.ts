import { Card } from '../models/Card';
import { Board, Pile } from '../models/Board';
import { Build } from '../models/Build';
import { Player } from '../models/Player';
import { ActionResult, CandidateAction } from './types';
import { InvalidAction, playerHasBuilds } from './validation';

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Calculate the board value of a pile (card array or Build)
 */
export function boardPileValue(pile: Pile): number {
  if (pile instanceof Build) {
    return pile.value;
  }
  return pile.reduce((sum, card) => sum + card.valueOnBoard(), 0);
}

/**
 * Check if a card is reserved as the only capture card for a player's build.
 * Returns the build if the card is reserved, null otherwise.
 */
export function isCardReservedForBuild(
  board: Board,
  player: Player,
  card: Card
): Build | null {
  const cardHandValue = card.valueInHand();

  // Check each build owned by the player
  for (const build of board.listBuilds()) {
    if (build.owner === player.name && build.value === cardHandValue) {
      // Count how many cards in hand can capture this build
      const matchingCards = player.hand.filter(c => c.valueInHand() === build.value);
      
      // If this is the only card that can capture the build, it's reserved
      if (matchingCards.length === 1 && matchingCards[0] === card) {
        return build;
      }
    }
  }
  return null;
}

/**
 * Check if a player may create a build with a given base pile and added card.
 * 
 * Rules:
 * - Building on non-build piles allowed only for single-card piles
 * - Cannot create/extend to a value X if opponent already has a build of value X
 * - Locked builds cannot be modified at all
 * - Card being used cannot be reserved for another build
 * - Need reservation card matching new build value
 */
export function canBuild(
  board: Board,
  player: Player,
  basePile: Pile,
  addedCard: Card
): boolean {
  const baseCards = basePile instanceof Build ? basePile.cards : basePile;
  
  // Restrict: building on non-build piles allowed only for single-card piles
  if (!(basePile instanceof Build) && baseCards.length !== 1) {
    return false;
  }

  const targetValue = baseCards.reduce((sum, c) => sum + c.valueOnBoard(), 0) + 
                      addedCard.valueOnBoard();

  // Enforce: cannot create/extend to a value X if opponent already has a build of value X
  const existingSameValue = board.listBuildsByValue(targetValue);
  for (const b of existingSameValue) {
    if (b.owner !== player.name) {
      return false;
    }
  }

  // Building on builds: locked builds cannot be modified at all
  if (basePile instanceof Build && basePile.locked) {
    return false;
  }

  // Check if the card being used to build is reserved for another build
  const reservedBuild = isCardReservedForBuild(board, player, addedCard);
  if (reservedBuild !== null) {
    return false;
  }

  // Need reservation card matching new build value
  for (const c of player.hand) {
    if (c !== addedCard && c.valueInHand() === targetValue) {
      return true;
    }
  }
  return false;
}

// ============================================================================
// PERFORM ACTIONS
// ============================================================================

/**
 * Create a build from a base pile and an added card
 */
export function performBuild(
  board: Board,
  player: Player,
  basePile: Pile,
  addedCard: Card,
  roundNumber: number = 1,
  declaredValue?: number
): ActionResult {
  const build = board.createBuild(basePile, addedCard, player.name, roundNumber, declaredValue);
  player.removeFromHand(addedCard);
  return new ActionResult(addedCard, [], [], true);
}

/**
 * Discard a card to the board
 * 
 * Rules:
 * 1. Cannot discard if card is reserved for a build
 * 2. Auto-feed to own build if card value matches build value
 * 3. Validate that no capture is possible before allowing discard
 * 4. Cannot trail if player has builds on the board
 */
export function performDiscard(
  board: Board,
  player: Player,
  card: Card
): ActionResult {
  // Check if this card is reserved for a build
  const reservedBuild = isCardReservedForBuild(board, player, card);
  if (reservedBuild !== null) {
    throw new Error(`Cannot discard ${card.code()} - it's reserved to capture your ${reservedBuild.value}-build!`);
  }

  // Check if player has a build with the same value as the card being discarded
  // If so, add the card to that build (trotta/feed)
  const cardValue = card.valueOnBoard();
  const playerBuilds = board.listBuilds().filter(
    b => b.owner === player.name && b.value === cardValue
  );

  if (playerBuilds.length > 0) {
    // Add card to the first matching build (even if locked)
    const build = playerBuilds[0];
    player.removeFromHand(card);
    build.addTrottaCard(card);
    return new ActionResult(card, [], [], false);
  }

  // Validate that no capture is possible before allowing discard
  const combos = generateCaptureCombinations(board, card);
  if (combos.length > 0 && combos[0].length > 0) {
    throw new InvalidAction(`Kan inte släppa ${card.code()} - intag är möjligt!`);
  }

  // Cannot trail/discard if player has any builds on the board
  if (playerHasBuilds(board, player)) {
    throw new InvalidAction(`Kan inte släppa ${card.code()} - du har byggen på bordet som måste tas in först!`);
  }

  // Otherwise, normal discard
  player.removeFromHand(card);
  board.addCard(card);
  return new ActionResult(card, [], [], false);
}

// ============================================================================
// CAPTURE COMBINATIONS (Subset-sum algorithm)
// ============================================================================

/**
 * Generate all possible capture combinations for a played card.
 * 
 * Special handling:
 * - Values 14/15/16 can ONLY be captured via existing builds
 * - Identical single cards are prioritized (mulle scenario)
 * - Uses subset-sum with backtracking for maximal disjoint sets
 */
export function generateCaptureCombinations(board: Board, card: Card): Pile[][] {
  const target = card.valueInHand();
  const piles = [...board.piles];
  const n = piles.length;

  // Special values (14=A, 15=SP 2, 16=RU 10) may ONLY be captured via an existing build
  if ([14, 15, 16].includes(target)) {
    const matchingBuilds = piles.filter(
      p => p instanceof Build && p.value === target
    );
    return matchingBuilds.length > 0 ? [[...matchingBuilds]] : [];
  }

  // Normal identical single capture (non-special values)
  // If exactly one identical single exists, return that as sole option
  const identicalSingle = piles.filter(
    p => !(p instanceof Build) && 
         p.length === 1 && 
         p[0].matches(card)
  );
  if (identicalSingle.length === 1) {
    return [[identicalSingle[0]]];
  }

  const values = piles.map(p => boardPileValue(p));

  // Direct matches (must be included)
  const directIndices = values
    .map((v, i) => v === target ? i : -1)
    .filter(i => i !== -1);
  
  const used = new Set(directIndices);

  // Candidate indices for subset packing (exclude already used)
  const candIndices = values
    .map((v, i) => !used.has(i) && v < target ? i : -1)
    .filter(i => i !== -1);

  // Precompute all subsets of candidates that sum to target
  const subsetMasks: number[][] = [];

  // Generate combinations helper
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

  for (let r = 1; r <= candIndices.length; r++) {
    const combos = generateCombinations(candIndices, r);
    for (const combo of combos) {
      const sum = combo.reduce((s, i) => s + values[i], 0);
      if (sum === target) {
        subsetMasks.push(combo);
      }
    }
  }

  // Backtracking to select maximum number of disjoint subsets
  let bestSelection: number[][] = [];

  // Sort by size descending for better pruning
  const sortedMasks = [...subsetMasks].sort((a, b) => {
    if (b.length !== a.length) return b.length - a.length;
    return a[0] - b[0]; // Tie-break by first element
  });

  const backtrack = (
    idx: number,
    usedNow: Set<number>,
    chosen: number[][]
  ): void => {
    // Prune if no better than current best (by pile count)
    const currentCount = chosen.reduce((sum, s) => sum + s.length, 0);
    const bestCount = bestSelection.reduce((sum, s) => sum + s.length, 0);
    
    if (currentCount > bestCount) {
      bestSelection = chosen.map(c => [...c]);
    }
    
    if (idx >= sortedMasks.length) {
      return;
    }
    
    for (let j = idx; j < sortedMasks.length; j++) {
      const mask = sortedMasks[j];
      // Check if any index in mask is already used
      if (!mask.some(m => usedNow.has(m))) {
        // Choose this mask
        chosen.push(mask);
        const newUsed = new Set([...usedNow, ...mask]);
        backtrack(j + 1, newUsed, chosen);
        chosen.pop();
      }
    }
  };

  backtrack(0, new Set(used), []);

  // Union of piles to capture = direct matches + all selected subsets
  const captureIndices = new Set(directIndices);
  for (const mask of bestSelection) {
    for (const idx of mask) {
      captureIndices.add(idx);
    }
  }

  if (captureIndices.size === 0) {
    return [];
  }

  const selectedPiles = Array.from(captureIndices)
    .sort((a, b) => a - b)
    .map(i => piles[i]);
  
  return [selectedPiles];
}

// ============================================================================
// MULLE DETECTION
// ============================================================================

/**
 * Detect mulle pairs among captured cards + played card.
 * A mulle is exactly 2 identical cards (same suit and rank).
 */
export function detectMulles(allCaptured: Card[], played: Card): Card[][] {
  // Count by (suit, rank)
  const counts = new Map<string, Card[]>();
  
  for (const c of allCaptured) {
    const key = `${c.suit}:${c.rank}`;
    if (!counts.has(key)) {
      counts.set(key, []);
    }
    counts.get(key)!.push(c);
  }

  const pairs: Card[][] = [];
  for (const [_, cards] of Array.from(counts.entries())) {
    if (cards.length === 2) {
      pairs.push(cards);
    }
  }
  
  return pairs;
}

/**
 * Perform capture using chosen combination
 */
export function performCapture(
  board: Board,
  player: Player,
  playedCard: Card,
  chosen: Pile[]
): ActionResult {
  // Gather captured cards
  const capturedCards: Card[] = [];
  
  for (const pile of chosen) {
    if (pile instanceof Build) {
      capturedCards.push(...pile.cards);
    } else {
      capturedCards.push(...pile);
    }
    board.removePile(pile);
  }
  
  player.removeFromHand(playedCard);
  
  // Played card also part of capture group
  const fullGroup = [...capturedCards, playedCard];
  
  // Mulle detection
  const mullePairs = detectMulles(fullGroup, playedCard);
  
  player.recordCapture(fullGroup);
  
  for (const pair of mullePairs) {
    // Register one card per pair for mulle points
    player.recordMulle(pair[0]);
  }
  
  return new ActionResult(playedCard, fullGroup, mullePairs, false);
}

// ============================================================================
// TODO: Additional functions to be ported
// ============================================================================

// export function performTrotta(...): ActionResult { ... }
// export function autoPlayTurn(...): ActionResult { ... }
// export function enumerateCandidateActions(...): CandidateAction[] { ... }
