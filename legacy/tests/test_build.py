from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.rules.capture import can_build, perform_build


def test_build_absorbs_and_locks():
    board = Board()
    # Base pile single RU 10
    ru10 = Card("RU","10",0)
    board.add_card(ru10)
    # Other eligible piles: SP5 single, plus two-card pile KL3+HJ7 summing 10
    sp5 = Card("SP","5",1)
    board.add_card(sp5)
    board.add_pile([Card("KL","3",2), Card("HJ","7",3)])
    player = Player("Bo")
    # Hand: SP5 (to build to 15) and reservation card SP2 (value 15 in hand)
    sp5_hand = Card("SP","5",4)
    sp2_hand = Card("SP","2",5)
    player.add_to_hand([sp5_hand, sp2_hand])
    base_pile = [ru10]
    assert can_build(board, player, base_pile, sp5_hand)
    res = perform_build(board, player, base_pile, sp5_hand)
    assert res.build_created
    builds = board.list_builds()
    assert len(builds) == 1
    build = builds[0]
    # Build now has absorbed SP5 and KL3+HJ7 and should be LOCKED (more than 2 cards)
    assert build.locked
    assert build.value == 15
    assert build.owner == player.name
    codes = sorted(c.code() for c in build.cards)
    for expected in ["RU 10","SP 5","SP 5","KL 3","HJ 7"]:
        assert expected in codes
