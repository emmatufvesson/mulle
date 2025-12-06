from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.rules.capture import generate_capture_combinations, perform_capture


def test_mulle_pair_in_combination_capture():
    board = Board()
    # Board has two identical KL 9 single piles
    kl9_a = Card("KL","9",0)
    kl9_b = Card("KL","9",1)
    board.add_card(kl9_a)
    board.add_card(kl9_b)
    # Player hand KL9 (captures both plus played -> but rule: mulle only when exactly two identical total captured? Here total would be 3 identical if we include played card.
    # For new rule we want scenario with exactly two identical captured including played card? We adjust: board has one KL9, hand has KL9.
    # Reset board for correct scenario
    board = Board()
    kl9_board = Card("KL","9",2)
    board.add_card(kl9_board)
    player = Player("Anna")
    kl9_hand = Card("KL","9",3)
    player.add_to_hand([kl9_hand])
    combos = generate_capture_combinations(board, kl9_hand)
    assert combos  # at least one combo (single pile)
    chosen = combos[0]
    res = perform_capture(board, player, kl9_hand, chosen)
    assert len(res.mulle_pairs) == 1
    assert len(player.mulles) == 1
    assert player.total_mulle_points() == 9
