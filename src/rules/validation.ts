import { Board } from '../models/Board';
import { Player } from '../models/Player';
import { Card } from '../models/Card';

/**
 * Exception thrown when a player action is not allowed
 */
export class InvalidAction extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'InvalidAction';
  }
}

/**
 * Check if a player has any builds on the board
 */
export function playerHasBuilds(board: Board, player: Player): boolean {
  for (const build of board.listBuilds()) {
    if (build.owner === player.name) {
      return true;
    }
  }
  return false;
}

/**
 * Ensure that a player can trail (discard to table).
 * A player cannot trail if they have builds on the board.
 */
export function ensureCanTrail(
  board: Board,
  player: Player,
  card?: Card
): void {
  if (playerHasBuilds(board, player)) {
    if (card) {
      throw new InvalidAction(
        `Kan inte släppa ${card.code()} - ${player.name} har byggen på bordet som måste tas in först!`
      );
    } else {
      throw new InvalidAction(
        `Kan inte släppa kort: ${player.name} har byggen på bordet som måste tas in först`
      );
    }
  }
}
