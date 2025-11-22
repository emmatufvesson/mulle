from mulle.engine.learning_ai import SimpleLearningAI
from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player


def test_ai_value_update_monotonic_for_positive_reward():
    player = Player("Bo")
    ai = SimpleLearningAI(player)
    board = Board()
    # Give a guaranteed capture combo with mulle (two identical on board + hand identical)
    c1 = Card("SP","6",0)
    c2 = Card("SP","6",1)
    board.add_card(c1)
    board.add_card(c2)
    hand_card = Card("SP","6",2)
    player.add_to_hand([hand_card])
    before = ai.values['capture_combo_mulle']
    action = ai.select_action(board)
    result = action.execute()
    # Simulate reward learning (as in ai_turn)
    reward = len(result.captured) + 10 * len(result.mulle_pairs) + (2 if result.build_created else 0)
    ai.learn(action.category, reward)
    after = ai.values['capture_combo_mulle']
    assert after >= before  # should not decrease on positive reward


def test_ai_discard_no_reward_value_stable():
    player = Player("Bo")
    ai = SimpleLearningAI(player)
    board = Board()
    # Only discard candidate (empty board, one card hand)
    card = Card("KL","4",3)
    player.add_to_hand([card])
    action = ai.select_action(board)
    assert action.category == 'discard'
    result = action.execute()
    reward = len(result.captured) + 10 * len(result.mulle_pairs) + (2 if result.build_created else 0)
    ai.learn(action.category, reward)
    assert ai.values['discard'] == 0.0  # unchanged because reward = 0


