from mulle.models.board import Board
from mulle.models.build import Build
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.rules.capture import generate_capture_combinations


def test_combo_capture_including_build():
    board = Board()
    # Create a build value 12 owned by Bo
    build = Build([Card("RU","10",0), Card("SP","2",1)], owner="Bo", target_value=12)
    board.piles.append(build)
    # Add single piles summing to value 12: 4+3+5
    board.add_card(Card("HJ","4",2))  # 4
    board.add_card(Card("KL","3",3))  # 3
    board.add_card(Card("SP","5",4))  # 5 (4+3+5=12 subset)
    player = Player("Anna")
    queen = Card("KL","Q",5)
    player.add_to_hand([queen])
    combos = generate_capture_combinations(board, queen)
    # Expect combination capturing build(12) + singles that sum to 12
    assert combos
    chosen = combos[0]
    assert build in chosen
