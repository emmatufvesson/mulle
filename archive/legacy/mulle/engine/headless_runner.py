"""Headless helpers for exercising the GameEngine without any GUI/CLI bindings."""

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from .game_service import ActionSelector, GameEngine, SessionResult
from ..models.board import Board
from ..models.player import Player


@dataclass
class ScriptedAction:
    player: str
    action: str
    card_index: Optional[int] = None
    target_piles: Optional[List[int]] = None
    declared_value: Optional[int] = None
    combo_index: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ScriptedAction":
        return cls(
            player=data.get("player", "Anna"),
            action=data.get("action", "auto"),
            card_index=data.get("card_index"),
            target_piles=data.get("target_piles"),
            declared_value=data.get("declared_value"),
            combo_index=data.get("combo_index"),
        )

    def matches(self, player: Player) -> bool:
        return player.name.lower() == self.player.lower()

    def _select_card(self, player: Player):
        if self.card_index is None:
            raise ValueError("card_index krävs för detta drag")
        if not 0 <= self.card_index < len(player.hand):
            raise ValueError(f"Ogiltigt kortindex {self.card_index} för {player.name}")
        return player.hand[self.card_index]

    def _select_capture_combo(self, board: Board, combinations, target_piles: Optional[List[int]]):
        if target_piles:
            target_set = frozenset(target_piles)
            for combo in combinations:
                indices = frozenset(board.piles.index(p) for p in combo)
                if indices == target_set:
                    return combo
        if self.combo_index is not None:
            try:
                return combinations[self.combo_index]
            except Exception as exc:  # pragma: no cover - defensive guard
                raise ValueError(f"Kan inte välja capture-kombination {self.combo_index}") from exc
        return combinations[0]

    def execute(self, engine: GameEngine, board: Board, player: Player, round_number: int):
        action = self.action.lower()
        if action == "auto":
            return engine.play_auto(player, round_number)
        card = self._select_card(player)
        if action == "discard":
            return engine.play_discard(player, card)
        if action == "trotta":
            return engine.play_trotta(player, card, round_number)
        if action == "build":
            if not self.target_piles:
                raise ValueError("target_piles krävs för build")
            pile = board.piles[self.target_piles[0]]
            return engine.play_build(player, pile, card, round_number, self.declared_value)
        if action == "capture":
            combos = engine.available_capture_combinations(card)
            if not combos:
                raise ValueError("Inga capture-kombinationer tillgängliga")
            chosen = self._select_capture_combo(board, combos, self.target_piles)
            return engine.play_capture(player, card, chosen)
        raise ValueError(f"Okänd handling: {self.action}")


def _selector_from_actions(actions: Iterable[ScriptedAction], engine: GameEngine) -> ActionSelector:
    queue = list(actions)

    def selector(board: Board, player: Player, round_number: int):
        if queue and queue[0].matches(player):
            action = queue.pop(0)
            return action.execute(engine, board, player, round_number)
        return engine.play_auto(player, round_number)

    return selector


def load_script(path: Path) -> List[ScriptedAction]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Scriptet måste vara en lista av åtgärder")
    return [ScriptedAction.from_dict(item) for item in data]


def run_headless_session(
    rounds: int = 1,
    seed: int = 42,
    scripted_actions: Optional[List[ScriptedAction]] = None,
) -> SessionResult:
    engine = GameEngine(seed=seed)
    selector = _selector_from_actions(scripted_actions, engine) if scripted_actions else None
    return engine.play_session(rounds=rounds, action_selector=selector)


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="Kör Mulle-motorn utan UI")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--rounds", type=int, default=1, help="Antal omgångar att spela")
    parser.add_argument(
        "--script",
        type=Path,
        help="Valfritt JSON-script med drag (lista med objekt: player, action, card_index, target_piles, declared_value, combo_index)",
    )
    args = parser.parse_args(argv)

    actions = load_script(args.script) if args.script else None
    result = run_headless_session(rounds=args.rounds, seed=args.seed, scripted_actions=actions)
    print(json.dumps({"cumulative": result.cumulative, "rounds": len(result.omgangen)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
