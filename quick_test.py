from mulle.models.board import Board
from mulle.models.player import Player  
from mulle.models.card import Card
from mulle.rules.capture import perform_discard
board = Board()
player = Player("Anna")
q1 = Card("HJ", "Q", 0)
q2 = Card("KL", "Q", 0)
player.add_to_hand([q1, q2])
board.add_card(Card("RU", "4", 0))
pile = board.piles[0]
build = board.create_build(pile, q1, owner="Anna", created_round=1)
print(f"Build has {len(build.cards)} cards, value={build.value}")
perform_discard(board, player, q2)
print(f"After discard: {len(build.cards)} cards")
print("Test PASSED!" if len(build.cards) == 2 else "Test FAILED!")
