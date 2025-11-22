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


def run_session(seed: int, rounds: int, interactive: bool):
    engine = GameEngine(seed=seed, ai_enabled=True)
    result = engine.play_session(rounds=rounds)

    print("==== Session Summary ====")
    for name, total in result.cumulative.items():
        print(f"{name}: {total}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--interactive', action='store_true')
    args = parser.parse_args()
    run_session(seed=args.seed, rounds=args.rounds, interactive=args.interactive)
