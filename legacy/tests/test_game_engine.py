import pytest

from mulle.engine.game_service import GameEngine


def test_discard_only_session_is_deterministic():
    engine_a = GameEngine(seed=1)
    engine_b = GameEngine(seed=1)

    def discard_selector(engine):
        def selector(board, player, round_number):
            # Always discard the first card to avoid randomness
            return engine.play_discard(player, player.hand[0])

        return selector

    result_a = engine_a.play_session(rounds=1, action_selector=discard_selector(engine_a))
    result_b = engine_b.play_session(rounds=1, action_selector=discard_selector(engine_b))

    assert result_a.cumulative == result_b.cumulative == {"Anna": 0, "Bo": 0}
    assert len(result_a.omgangen[0].rounds) == 6