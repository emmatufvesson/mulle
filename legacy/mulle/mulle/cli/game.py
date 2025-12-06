"""Simple CLI wrapper that uses GameEngine for gameplay.

The previous CLI version contained duplicated engine logic and an inline AI implementation
which caused import and duplication problems. This module now delegates to GameEngine
and keeps CLI-specific interactive behavior minimal.
"""
import argparse

from ..engine.game_service import GameEngine


def _interactive_selector(engine: GameEngine):
    """Return an action_selector that prompts the user to pick a card index to discard.

    NOTE: This is a minimal interactive selector. It assumes the player will choose a discard
    by entering the index of a card in their hand. If invalid input is provided, fallback to
    discarding the first card.
    """

    def selector(board, player, round_number):
        try:
            print(f"\n{player.name}'s hand:")
            for i, c in enumerate(player.hand):
                # assume Card has a human-readable repr or __str__
                print(f"  [{i}] {c}")
            raw = input("Välj index för kort att spela (enter för första): ").strip()
            if raw == "":
                idx = 0
            else:
                idx = int(raw)
            if idx < 0 or idx >= len(player.hand):
                print("Ogiltigt index, spelar första kortet.")
                idx = 0
        except (ValueError, KeyboardInterrupt):
            print("Ogiltigt val eller avbrutet, spelar första kortet.")
            idx = 0
        # For simplicity we play discard via engine wrapper
        return engine.play_discard(player, player.hand[idx])

    return selector


def run_session(seed: int, rounds: int, interactive: bool):
    engine = GameEngine(seed=seed, ai_enabled=True)
    action_selector = None
    if interactive:
        action_selector = _interactive_selector(engine)

    result = engine.play_session(rounds=rounds, action_selector=action_selector)

    print("==== Session Summary ====")
    for name, total in result.cumulative.items():
        print(f"{name}: {total}")
    if hasattr(result, "ai_values") and result.ai_values:
        print("AI values:", result.ai_values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--interactive', action='store_true')
    args = parser.parse_args()
    run_session(seed=args.seed, rounds=args.rounds, interactive=args.interactive)