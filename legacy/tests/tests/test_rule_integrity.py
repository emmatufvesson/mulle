from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.rules.capture import detect_mulles, generate_capture_combinations, perform_capture
from mulle.rules.scoring import INTAKE_POINTS_1, INTAKE_POINTS_2


def test_special_values_unchanged():
    ace_board = Card("KL","A",0)
    sp2 = Card("SP","2",1)
    ru10 = Card("RU","10",2)
    assert ace_board.value_on_board() == 1
    assert ace_board.value_in_hand() == 14
    assert sp2.value_on_board() == 2 and sp2.value_in_hand() == 15
    assert ru10.value_on_board() == 10 and ru10.value_in_hand() == 16


def test_intake_points_tables_constant():
    assert "SP" in INTAKE_POINTS_1 and "SP" in INTAKE_POINTS_2
    assert "A" in INTAKE_POINTS_1["KL"]
    assert "2" in INTAKE_POINTS_2["SP"] and "A" in INTAKE_POINTS_2["SP"]
    assert "10" in INTAKE_POINTS_2["RU"]


def test_mulle_detection_exact_pairs_only():
    cards = [Card("KL","5",0), Card("KL","5",1), Card("KL","5",2)]
    pairs = detect_mulles(cards, cards[0])
    assert pairs == []
    cards2 = [Card("SP","6",3), Card("SP","6",4)]
    pairs2 = detect_mulles(cards2, cards2[0])
    assert len(pairs2) == 1 and len(pairs2[0]) == 2


def test_capture_combination_does_not_modify_values():
    board = Board()
    # Put cards with total board value 12: 7+4+1 (Ace on board = 1)
    c7 = Card("SP","7",10)
    c4 = Card("HJ","4",11)
    ca = Card("KL","A",12)
    board.add_card(c7)
    board.add_card(c4)
    board.add_card(ca)
    player = Player("Anna")
    queen = Card("RU","Q",13)
    player.add_to_hand([queen])
    combos = generate_capture_combinations(board, queen)
    # Queen hand value = 12
    assert c7.value_on_board() == 7 and queen.value_in_hand() == 12
    assert any(sum(pile[0].value_on_board() for pile in combo if not hasattr(pile,'owner')) == 12 for combo in combos)
    chosen = combos[0]
    before_values = [pile[0].value_on_board() for pile in chosen if not hasattr(pile,'owner')]
    res = perform_capture(board, player, queen, chosen)
    after_values = [card.value_on_board() for card in res.captured if card.code() in [c7.code(), c4.code(), ca.code()]]
    assert before_values == after_values[:len(before_values)]
