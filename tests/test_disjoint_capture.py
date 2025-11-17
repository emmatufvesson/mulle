from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.build import Build
from mulle.models.player import Player
from mulle.rules.capture import generate_capture_combinations, perform_capture


def test_disjoint_groups_captured_together():
    board = Board()
    # Build value 12
    build12 = Build([Card("RU","10",0), Card("SP","2",1)], owner="Bo", target_value=12)
    board.piles.append(build12)
    # Singles 3+5+4 = 12
    c3 = Card("SP","3",2)
    c5 = Card("KL","5",3)
    c4 = Card("HJ","4",4)
    board.add_card(c3)
    board.add_card(c5)
    board.add_card(c4)
    # Player hand Q (value 12)
    player = Player("Anna")
    queen = Card("SP","Q",5)
    player.add_to_hand([queen])

    combos = generate_capture_combinations(board, queen)
    assert combos, "Should have a capture option"
    chosen = combos[0]
    # Should include both the build and the three singles
    assert build12 in chosen
    singles_included = set(tuple(p) for p in chosen if not hasattr(p, 'owner'))
    assert any(len(p)==1 and p[0].code()=="SP 3" for p in chosen if not hasattr(p,'owner'))
    assert any(len(p)==1 and p[0].code()=="KL 5" for p in chosen if not hasattr(p,'owner'))
    assert any(len(p)==1 and p[0].code()=="HJ 4" for p in chosen if not hasattr(p,'owner'))

    res = perform_capture(board, player, queen, chosen)
    captured_codes = sorted(c.code() for c in res.captured)
    for code in ["RU 10","SP 2","SP 3","KL 5","HJ 4","SP Q"]:
        assert code in captured_codes

