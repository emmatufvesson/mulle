import random
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple

from ..models.board import Board
from ..models.deck import Deck
from ..models.player import Player
from ..rules.capture import (
    ActionResult,
    auto_play_turn,
    can_build,
    generate_capture_combinations,
    perform_build,
    perform_capture,
    perform_discard,
    perform_trotta,
)
from ..rules.scoring import ScoreBreakdown, score_round
from .learning_ai import SimpleLearningAI


ActionSelector = Callable[[Board, Player, int], ActionResult]


@dataclass
class RoundResult:
    round_index: int
    scores: List[ScoreBreakdown]
    actions: List[Tuple[str, ActionResult]] = field(default_factory=list)


@dataclass
class OmgangResult:
    index: int
    rounds: List[RoundResult] = field(default_factory=list)


@dataclass
class SessionResult:
    omgangen: List[OmgangResult]
    cumulative: dict
    ai_values: Optional[dict]


class GameEngine:
    """UI-agnostic game engine that owns deck, board and players."""

    def __init__(self, seed: int = 42, ai_enabled: bool = True):
        self.seed = seed
        random.seed(seed)
        self.players = [Player("Anna"), Player("Bo")]
        self.board = Board()
        # Use Optional[Deck] for compatibility with Python < 3.10
        self.deck: Optional[Deck] = None
        self.ai = SimpleLearningAI(self.players[1]) if ai_enabled else None
        self.current_omgang = 0

    # --- setup helpers ---
    def setup_initial_board(self) -> Board:
        if self.deck is None:
            raise RuntimeError("Deck not initialized. Call start_omgang() before setup_initial_board().")
        self.board = Board()
        for _ in range(8):
            self.board.add_card(self.deck.draw())
        return self.board

    def deal_hands(self):
        if self.deck is None:
            raise RuntimeError("Deck not initialized. Cannot deal hands.")
        if self.deck.remaining() < 16:
            raise RuntimeError("Inte nog kort kvar i leken för att dela ut händer (behöver 16)")
        for p in self.players:
            p.hand.clear()
            p.add_to_hand(self.deck.draw_many(8))

    def start_omgang(self, omgang_index: int):
        self.current_omgang = omgang_index
        self.deck = Deck(seed=self.seed + omgang_index)
        self.setup_initial_board()
        for p in self.players:
            p.captured.clear()
            p.mulles.clear()
            p.tabbe = 0

    # --- action wrappers ---
    def play_capture(self, player: Player, card, chosen):
        return perform_capture(self.board, player, card, chosen)

    def play_build(self, player: Player, pile, card, round_number: int, declared_value=None):
        return perform_build(self.board, player, pile, card, round_number, declared_value)

    def play_trotta(self, player: Player, card, round_number: int):
        return perform_trotta(self.board, player, card, round_number)

    def play_discard(self, player: Player, card):
        return perform_discard(self.board, player, card)

    def play_auto(self, player: Player, round_number: int):
        # If ai not configured or this player isn't the ai player, fall back to auto_play_turn
        if not self.ai or player is not self.players[1]:
            return auto_play_turn(self.board, player, round_number)

        action = self.ai.select_action(self.board, round_number)
        # If AI had no candidate actions, fallback to auto_play_turn
        if action is None:
            return auto_play_turn(self.board, player, round_number)

        result = action.execute()
        # Defensive: ensure result has expected attributes; otherwise don't fail noisily
        captured_len = len(getattr(result, "captured", []))
        mulle_pairs_len = len(getattr(result, "mulle_pairs", []))
        build_created = bool(getattr(result, "build_created", False))
        reward = captured_len + 10 * mulle_pairs_len + (2 if build_created else 0)
        self.ai.learn(getattr(action, "category", ""), reward)
        return result

    # --- gameplay ---
    def _default_action_selector(self, board: Board, player: Player, round_number: int) -> ActionResult:
        return self.play_auto(player, round_number)

    def play_round(
        self,
        round_index: int,
        starter_idx: int = 0,
        action_selector: Optional[ActionSelector] = None,
    ) -> RoundResult:
        selector = action_selector or self._default_action_selector
        round_number = round_index + 1
        turn = starter_idx
        executed_actions: List[Tuple[str, ActionResult]] = []

        while any(p.hand for p in self.players):
            current = self.players[turn % 2]
            result = selector(self.board, current, round_number)
            executed_actions.append((current.name, result))
            if not self.board.piles:
                current.tabbe += 1
            turn += 1

        scores = score_round(self.players)
        return RoundResult(round_index=round_index, scores=scores, actions=executed_actions)

    def play_session(
        self,
        rounds: int,
        action_selector: Optional[ActionSelector] = None,
        starter_idx: int = 0,
    ) -> SessionResult:
        cumulative = {p.name: 0 for p in self.players}
        starting_player_idx = starter_idx
        omgangen: List[OmgangResult] = []

        for omg in range(rounds):
            self.start_omgang(omg)
            omgang_result = OmgangResult(index=omg)

            for r in range(6):
                self.deal_hands()
                round_result = self.play_round(
                    r,
                    starter_idx=starting_player_idx,
                    action_selector=action_selector,
                )
                for s in round_result.scores:
                    cumulative[s.player.name] += s.total
                # clear round data
                for p in self.players:
                    p.captured.clear()
                    p.mulles.clear()
                    p.tabbe = 0
                omgang_result.rounds.append(round_result)
            self.board.piles.clear()
            starting_player_idx = 1 - starting_player_idx
            omgangen.append(omgang_result)

        ai_values = getattr(self.ai, "values", None)
        return SessionResult(omgangen=omgangen, cumulative=cumulative, ai_values=ai_values)

    # convenience helpers for UIs
    def available_capture_combinations(self, card):
        return generate_capture_combinations(self.board, card)

    def can_build_on(self, player: Player, pile, card) -> bool:
        return can_build(self.board, player, pile, card)