import pytest

from mulle.engine.game_service import GameEngine


def test_discard_only_session_is_deterministic():
    engine = GameEngine(seed=1)

    def discard_selector(board, player, round_number):
        # Always discard the first card to avoid randomness
        return engine.play_discard(player, player.hand[0])

    result = engine.play_session(rounds=1, interactive_selector=discard_selector)
    assert result.cumulative == {"Anna": 42, "Bo": 35}
    assert len(result.omgangen[0].rounds) == 6

