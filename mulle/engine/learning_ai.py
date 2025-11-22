from __future__ import annotations

from ..models.board import Board
from ..models.player import Player
from ..rules.capture import CandidateAction, enumerate_candidate_actions


class SimpleLearningAI:
    """Minimal learning layer around the heuristic candidate actions."""

    def __init__(self, player: Player, learning_rate: float = 0.1):
        self.player = player
        self.learning_rate = learning_rate
        self.values: dict[str, float] = {
            "capture_combo_mulle": 0.0,
            "capture_combo": 0.0,
            "build": 0.0,
            "discard": 0.0,
        }

    def select_action(self, board: Board, round_number: int = 1) -> CandidateAction:
        candidates = enumerate_candidate_actions(board, self.player, round_number)
        if not candidates:
            raise RuntimeError("No candidate actions available")

        def expected_reward(candidate: CandidateAction) -> float:
            base = self.values.get(candidate.category, 0.0)
            return base + candidate.predicted_reward

        return max(candidates, key=expected_reward)

    def learn(self, category: str, reward: float):
        current = self.values.get(category, 0.0)
        updated = current + self.learning_rate * reward
        # Never go below zero to keep weights non-negative
        self.values[category] = max(0.0, updated)
