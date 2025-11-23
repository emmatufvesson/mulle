"""Simple CLI wrapper that uses GameEngine for gameplay.

The previous CLI version contained duplicated engine logic and an inline AI implementation
which caused import and duplication problems. This module now delegates to GameEngine
and keeps CLI-specific interactive behavior minimal.
"""
import argparse
import random
from typing import List

from ..engine.game_service import GameEngine
from ..models.deck import Deck
from ..models.board import Board
from ..models.player import Player


def _interactive_selector(engine: GameEngine):
    def selector(board, player, round_number):
        try:
            print(f"\n{player.name}'s hand:")
            for i, c in enumerate(player.hand):
                print(f"  [{i}] {c.code()}")
            raw = input("Välj index för kort att spela (enter för första): ").strip()
            idx = 0 if raw == '' else int(raw)
            if idx < 0 or idx >= len(player.hand):
                print("Ogiltigt index, spelar första kortet.")
                idx = 0
        except (ValueError, KeyboardInterrupt):
            print("Ogiltigt val eller avbrutet, spelar första kortet.")
            idx = 0
        return engine.play_discard(player, player.hand[idx])
    return selector


def run_session(seed: int, rounds: int, interactive: bool):
    engine = GameEngine(seed=seed, ai_enabled=True)
    action_selector = _interactive_selector(engine) if interactive else None
    result = engine.play_session(rounds=rounds, action_selector=action_selector)
    print("==== Session Summary ====")
    for name, total in result.cumulative.items():
        print(f"{name}: {total}")
    if result.ai_values:
        print("AI values:", result.ai_values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--interactive', action='store_true')
    args = parser.parse_args()
    run_session(seed=args.seed, rounds=args.rounds, interactive=args.interactive)
