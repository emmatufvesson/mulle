import random
from ..models.board import Board
from ..models.player import Player
from ..rules.capture import enumerate_candidate_actions


class SimpleLearningAI:
    def __init__(self, player: Player):
        self.player = player
        self.values = {
            'capture_combo_mulle': 10.0,
            'capture_combo': 5.0,
            'build': 1.0,
            'discard': 0.0,
        }
        self.learning_rate = 0.2
        self.exploration = 0.15

    def select_action(self, board: Board, round_number: int = 1):
        candidates = enumerate_candidate_actions(board, self.player, round_number)
        if not candidates:
            return None
        if random.random() < self.exploration:
            return random.choice(candidates)
        scored = []
        for c in candidates:
            if not hasattr(c, 'execute'):
                continue
            base_val = self.values.get(getattr(c, 'category', ''), 0.0)
            predicted = getattr(c, 'predicted_reward', 0.0)
            total_score = base_val + predicted
            scored.append((total_score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else None

    def learn(self, action_category: str, reward: float):
        old = self.values.get(action_category, 0.0)
        self.values[action_category] = old + self.learning_rate * (reward - old)
