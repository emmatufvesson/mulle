"""
Comprehensive test for trotta rules fixes
"""
from mulle.models.board import Board
from mulle.models.player import Player
from mulle.models.card import Card
from mulle.models.build import Build
from mulle.rules.capture import can_build, perform_trotta, perform_build

def test_trotta_requires_reservation():
    """Test that trotta requires a reservation card"""
    print("\n" + "="*70)
    print("TEST 1: Trotta requires reservation card")
    print("="*70)

    board = Board()
    player = Player('Anna')

    # Scenario: Only one 4 on hand, one 4 on board
    c4_hand = Card('HJ', '4', 0)
    c4_board = Card('KL', '4', 0)
    player.add_to_hand([c4_hand])
    board.add_card(c4_board)

    print("Setup: Anna has HJ 4 in hand, KL 4 on board")
    print("Attempting to trotta without reservation card...")

    try:
        result = perform_trotta(board, player, c4_hand, round_number=1)
        print("❌ FAILED: Should not allow trotta without reservation card!")
        return False
    except ValueError as e:
        print(f"✅ PASSED: {e}")
        return True

def test_trotta_works_with_reservation():
    """Test that trotta works when you have a reservation card"""
    print("\n" + "="*70)
    print("TEST 2: Trotta works with reservation card")
    print("="*70)

    board = Board()
    player = Player('Anna')

    # Scenario: Two 4s on hand, one 4 on board
    c4_hand1 = Card('HJ', '4', 0)
    c4_hand2 = Card('SP', '4', 0)  # Reservation card
    c4_board = Card('KL', '4', 0)
    player.add_to_hand([c4_hand1, c4_hand2])
    board.add_card(c4_board)

    print("Setup: Anna has HJ 4 and SP 4 in hand, KL 4 on board")
    print("Attempting to trotta with reservation card...")

    try:
        result = perform_trotta(board, player, c4_hand1, round_number=1)
        print(f"✅ PASSED: Trotta succeeded - {len(result.captured)} cards captured, build created: {result.build_created}")

        # Verify the build was created and is locked
        builds = board.list_builds()
        if len(builds) == 1 and builds[0].locked:
            print(f"✅ Build is locked: {builds[0]}")
            return True
        else:
            print(f"❌ FAILED: Build should be locked!")
            return False
    except ValueError as e:
        print(f"❌ FAILED: Should allow trotta with reservation card! Error: {e}")
        return False

def test_cannot_rebuild_locked_build():
    """Test that locked builds cannot be rebuilt by opponent"""
    print("\n" + "="*70)
    print("TEST 3: Opponent cannot rebuild locked build")
    print("="*70)

    board = Board()
    anna = Player('Anna')
    bo = Player('Bo')

    # Anna has a locked 4-build (trotted)
    locked_build = Build(
        [Card('HJ', '4', 0), Card('KL', '4', 0)],
        owner='Anna',
        target_value=4,
        locked=True,
        created_round=1
    )
    board.piles.append(locked_build)

    # Bo tries to build on it with a 9 to make 13
    c9 = Card('SP', '9', 0)
    cK = Card('SP', 'K', 0)  # King = 13 in hand (reservation)
    bo.add_to_hand([c9, cK])

    print("Setup: Anna has locked 4-build, Bo has 9 and K")
    print("Bo attempts to build 9 on Anna's locked 4-build (4+9=13)...")

    can_rebuild = can_build(board, bo, locked_build, c9)

    if not can_rebuild:
        print(f"✅ PASSED: Cannot rebuild locked build (can_build returned {can_rebuild})")
        return True
    else:
        print(f"❌ FAILED: Should not allow rebuilding locked build!")
        return False

def test_can_rebuild_unlocked_build():
    """Test that unlocked builds CAN be rebuilt (for comparison)"""
    print("\n" + "="*70)
    print("TEST 4: Opponent CAN rebuild unlocked build (sanity check)")
    print("="*70)

    board = Board()
    anna = Player('Anna')
    bo = Player('Bo')

    # Anna has an UNLOCKED 4-build
    unlocked_build = Build(
        [Card('HJ', '2', 0), Card('KL', '2', 0)],
        owner='Anna',
        target_value=4,
        locked=False,  # NOT locked
        created_round=1
    )
    board.piles.append(unlocked_build)

    # Bo tries to build on it with a 9 to make 13
    c9 = Card('SP', '9', 0)
    cK = Card('SP', 'K', 0)  # King = 13 in hand (reservation)
    bo.add_to_hand([c9, cK])

    print("Setup: Anna has UNLOCKED 4-build, Bo has 9 and K")
    print("Bo attempts to build 9 on Anna's unlocked 4-build (4+9=13)...")

    can_rebuild = can_build(board, bo, unlocked_build, c9)

    if can_rebuild:
        print(f"✅ PASSED: Can rebuild unlocked build (can_build returned {can_rebuild})")
        return True
    else:
        print(f"❌ FAILED: Should allow rebuilding unlocked build!")
        return False

def test_add_to_own_locked_build():
    """Test that you CAN add cards to your own locked build via trotta"""
    print("\n" + "="*70)
    print("TEST 5: Can add card to own locked build via trotta")
    print("="*70)

    board = Board()
    anna = Player('Anna')

    # Anna has a locked 12-build
    locked_build = Build(
        [Card('HJ', 'Q', 0), Card('KL', 'Q', 0)],
        owner='Anna',
        target_value=12,
        locked=True,
        created_round=1
    )
    board.piles.append(locked_build)

    # Anna has another Queen to add
    cQ = Card('SP', 'Q', 0)
    anna.add_to_hand([cQ])

    print("Setup: Anna has locked 12-build, tries to add SP Q to it")
    print("Attempting to trotta on own locked build...")

    try:
        result = perform_trotta(board, anna, cQ, round_number=1)
        if len(locked_build.cards) == 3:
            print(f"✅ PASSED: Added card to own locked build - now has {len(locked_build.cards)} cards")
            return True
        else:
            print(f"❌ FAILED: Build should have 3 cards, has {len(locked_build.cards)}")
            return False
    except Exception as e:
        print(f"❌ FAILED: Should allow adding to own locked build! Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TROTTA RULES COMPREHENSIVE TEST SUITE")
    print("="*70)

    results = []

    results.append(("Trotta requires reservation", test_trotta_requires_reservation()))
    results.append(("Trotta works with reservation", test_trotta_works_with_reservation()))
    results.append(("Cannot rebuild locked build", test_cannot_rebuild_locked_build()))
    results.append(("Can rebuild unlocked build", test_can_rebuild_unlocked_build()))
    results.append(("Can add to own locked build", test_add_to_own_locked_build()))

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

