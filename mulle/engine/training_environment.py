from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import argparse

from ..models.board import Board
from ..models.card import Card
from ..models.player import Player
from ..rules.capture import (
    ActionResult,
    CandidateAction,
    auto_play_turn,
    enumerate_candidate_actions,
)
from ..rules.scoring import score_round
from .game_service import GameEngine


@dataclass
class TrainingObservation:
    """A compact snapshot of the game state for learning purposes."""

    board: Board
    hand: List[Card]
    opponent_cards: int
    round_number: int
    legal_actions: List[CandidateAction] = field(default_factory=list)


class TrainingEnvironment:
    """Lightweight environment for experimenting with rule-learning agents.

    The environment exposes a simple ``reset``/``step`` API similar to RL libraries
    but keeps the game-flow logic from :class:`GameEngine`. The controlled player
    is always the first one ("Anna") while the opponent uses the built-in
    heuristic ``auto_play_turn``.
    """

    def __init__(self, seed: int = 42):
        self.engine = GameEngine(seed=seed, ai_enabled=False)
        self.round_number = 1
        self.done = False

    def start(self) -> TrainingObservation:
        """Alias for :meth:`reset` to make CLI usage more readable."""

        return self.reset()

    # --- public API ---
    def reset(self) -> TrainingObservation:
        """Start a new single-round training session and return the first observation."""

        self.engine.start_omgang(0)
        self.engine.deal_hands()
        self.round_number = 1
        self.done = False
        return self._build_observation()

    def legal_actions(self) -> List[CandidateAction]:
        """List candidate actions for the controlled player on the current board."""

        if self.done:
            return []
        player = self.engine.players[0]
        return enumerate_candidate_actions(self.engine.board, player, self.round_number)

    def step(
        self, action: Optional[CandidateAction] = None
    ) -> Tuple[TrainingObservation, float, bool, Dict[str, Any]]:
        """Play one turn for the controlled player and advance the environment.

        The optional ``action`` should be a ``CandidateAction`` from
        :meth:`legal_actions`. If omitted, the highest-predicted-reward action is
        chosen automatically. The opponent immediately plays one response turn via
        ``auto_play_turn``. Returns ``(observation, reward, done, info)``.
        """

        if self.done:
            raise RuntimeError("Environment is done. Call reset() to start again.")

        player = self.engine.players[0]
        opponent = self.engine.players[1]

        chosen_action = action or self._select_default_action()
        player_result = self._apply_action(player, chosen_action)
        if not self.engine.board.piles:
            player.tabbe += 1
        reward = self._reward_from_result(player_result)

        opponent_result: Optional[ActionResult] = None
        if opponent.hand:
            opponent_result = auto_play_turn(self.engine.board, opponent, self.round_number)
            if not self.engine.board.piles:
                opponent.tabbe += 1

        self.done = not any(p.hand for p in self.engine.players)

        info: Dict[str, Any] = {
            "player_action": player_result,
            "opponent_action": opponent_result,
        }
        if self.done:
            scores = score_round(self.engine.players)
            info["scores"] = {s.player.name: s.total for s in scores}

        observation = self._build_observation()
        return observation, reward, self.done, info

    # --- helpers ---
    def _select_default_action(self) -> Optional[CandidateAction]:
        actions = self.legal_actions()
        if not actions:
            return None
        return max(actions, key=lambda a: getattr(a, "predicted_reward", 0.0))

    def _apply_action(
        self, player: Player, action: Optional[CandidateAction]
    ) -> ActionResult:
        if action is None:
            return auto_play_turn(self.engine.board, player, self.round_number)
        if not hasattr(action, "execute"):
            raise ValueError("Action must provide an execute() method")
        return action.execute()

    def _reward_from_result(self, result: ActionResult) -> float:
        captured_len = len(getattr(result, "captured", []))
        mulle_pairs_len = len(getattr(result, "mulle_pairs", []))
        build_created = bool(getattr(result, "build_created", False))
        # Align reward calculation with enumerate_candidate_actions: include played card (+1), mulle multiplier 5
        return float(captured_len + 1 + 5 * mulle_pairs_len + (2 if build_created else 0))

    def _build_observation(self) -> TrainingObservation:
        player = self.engine.players[0]
        return TrainingObservation(
            board=self.engine.board,
            hand=list(player.hand),
            opponent_cards=len(self.engine.players[1].hand),
            round_number=self.round_number,
            legal_actions=self.legal_actions(),
        )


def _format_action(action: Optional[CandidateAction]) -> str:
    if action is None:
        return "AUTO"
    return f"{action.category} (reward≈{action.predicted_reward:.2f})"


def _run_cli(seed: int, max_steps: int):
    env = TrainingEnvironment(seed=seed)
    obs = env.start()
    print("Startar träningsomgång")
    print(f"- Kort på hand: {len(obs.hand)}")
    print(f"- Motståndaren har {obs.opponent_cards} kort")
    print()

    step = 0
    done = False
    while not done and step < max_steps:
        action = obs.legal_actions[0] if obs.legal_actions else None
        print(f"Steg {step+1}: spelar {_format_action(action)}")
        obs, reward, done, info = env.step(action)
        print(f"  Belöning: {reward}\n")
        step += 1

    if done and "scores" in info:
        print("Omgången är klar. Slutpoäng:")
        for name, total in info["scores"].items():
            print(f"- {name}: {total}")
    elif not done:
        print("Maxsteg uppnått innan omgången avslutades.")


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="Starta en enkel träningsmiljö")
    parser.add_argument("--seed", type=int, default=42, help="Slumpfrö för kortleken")
    parser.add_argument(
        "--max-steps", type=int, default=50, help="Maximalt antal steg att spela upp"
    )
    args = parser.parse_args(argv)
    _run_cli(seed=args.seed, max_steps=args.max_steps)


if __name__ == "__main__":
    main()
