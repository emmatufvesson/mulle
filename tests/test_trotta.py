from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.rules.capture import perform_trotta


def test_trotta_creates_locked_build():
    board = Board()
    # Board: RU 7 single, KL A single, and a 2-card pile [HJ 4 + SP 4] = 8
    ru7 = Card("RU","7",0)
    kla = Card("KL","A",1)
    board.add_card(ru7)
    board.add_card(kla)
    board.add_pile([Card("HJ","4",2), Card("SP","4",3)])

    player = Player("Anna")
    sp8 = Card("SP","8",4)
    player.add_to_hand([sp8])

    # Trotta with SP 8 (value 8)
    res = perform_trotta(board, player, sp8)

    assert res.build_created
    # Should have created a locked build
    builds = [p for p in board.piles if hasattr(p, 'locked')]
    assert len(builds) == 1
    build = builds[0]
    assert build.locked
    assert build.value == 8
    assert build.owner == "Anna"

    # Build should contain: SP 8 (played), RU 7, KL A, HJ 4, SP 4
    codes = sorted(c.code() for c in build.cards)
    expected = sorted(["SP 8", "RU 7", "KL A", "HJ 4", "SP 4"])
    assert codes == expected

    # Board should have no other piles
    assert len(board.piles) == 1


def test_trotta_fails_without_matches():
    board = Board()
    # Board has no cards matching value 8
    board.add_card(Card("KL","5",0))

    player = Player("Bo")
    sp8 = Card("SP","8",1)
    player.add_to_hand([sp8])

    # Should raise error
    try:
        perform_trotta(board, player, sp8)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "No piles matching value 8" in str(e)

