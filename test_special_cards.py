from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.rules.capture import can_build, perform_build

print("=== Test: Cannot build with RU 10 without reservation ===")
board = Board()
kl6 = Card("KL","6",0)
board.add_card(kl6)

player = Player("Bo")
ru10 = Card("RU","10",1)
player.add_to_hand([ru10])  # Only RU 10, no reservation

# Try to build KL 6 + RU 10 = 16
# This should FAIL because player doesn't have another card with hand value 16
can = can_build(board, player, [kl6], ru10)
print(f"Can build KL 6 + RU 10 with only one RU 10? {can}")
assert not can, "Should NOT be able to build without reservation card"
print("✓ PASS: Cannot build without reservation\n")

print("=== Test: CANNOT build WITH RU 10 from hand even with two ===")
board2 = Board()
kl6_2 = Card("KL","6",2)
board2.add_card(kl6_2)

player2 = Player("Bo")
ru10_a = Card("RU","10",3)
ru10_b = Card("RU","10",4)  # Second RU 10 as reservation
player2.add_to_hand([ru10_a, ru10_b])

can2 = can_build(board2, player2, [kl6_2], ru10_a)
print(f"Can build KL 6 + RU 10 (from hand) even with TWO RU 10s? {can2}")
assert not can2, "Should NOT be able to build WITH RU 10 from hand"
print("✓ PASS: Cannot use RU 10 from hand to build\n")

print("=== Test: CAN build ON RU 10 (already on board) ===")
board2b = Board()
ru10_board = Card("RU","10",5)  # RU 10 already on board (value 10)
board2b.add_card(ru10_board)

player2b = Player("Bo")
kl6_hand = Card("KL","6",6)
ru10_reservation = Card("RU","10",7)  # Reservation
player2b.add_to_hand([kl6_hand, ru10_reservation])

can2b = can_build(board2b, player2b, [ru10_board], kl6_hand)
print(f"Can build ON RU 10 (on board) WITH 6 (from hand) to make 16? {can2b}")
assert can2b, "Should be able to build ON RU 10 that's on board"
print("✓ PASS: Can build on RU 10 that's on board\n")

print("=== Verify card values ===")
test_ru10 = Card("RU","10",99)
test_sp2 = Card("SP","2",98)
test_ace = Card("KL","A",97)

print(f"RU 10: board={test_ru10.value_on_board()}, hand={test_ru10.value_in_hand()}")
print(f"SP 2: board={test_sp2.value_on_board()}, hand={test_sp2.value_in_hand()}")
print(f"Ace: board={test_ace.value_on_board()}, hand={test_ace.value_in_hand()}")

assert test_ru10.value_on_board() == 10
assert test_ru10.value_in_hand() == 16
assert test_sp2.value_on_board() == 2
assert test_sp2.value_in_hand() == 15
assert test_ace.value_on_board() == 1
assert test_ace.value_in_hand() == 14

print("✓ All special values correct!\n")

print("=== Test: Cannot capture special value 16 without a BUILD ===")
from mulle.rules.capture import generate_capture_combinations
from mulle.models.build import Build

board3 = Board()
# Put cards that sum to 16 but are NOT a build
board3.add_card(Card("KL","6",10))
board3.add_card(Card("SP","10",11))  # 6 + 10 = 16 on board
player3 = Player("Anna")
ru10_hand = Card("RU","10",12)
player3.add_to_hand([ru10_hand])

combos = generate_capture_combinations(board3, ru10_hand)
print(f"Cards on board sum to 16 (6+10), can capture with RU 10 (value 16)? {len(combos) > 0}")
assert len(combos) == 0, "Should NOT be able to capture special value 16 without a build"
print("✓ PASS: Cannot capture 16 without build\n")

print("=== Test: CAN capture special value 16 with a BUILD ===")
board4 = Board()
# Create a build with value 16
build16 = Build([Card("KL","6",20), Card("SP","10",21)], owner="Bo", target_value=16, locked=False)
board4.piles.append(build16)
player4 = Player("Anna")
ru10_hand2 = Card("RU","10",22)
player4.add_to_hand([ru10_hand2])

combos2 = generate_capture_combinations(board4, ru10_hand2)
print(f"Build with value 16 exists, can capture with RU 10? {len(combos2) > 0}")
assert len(combos2) > 0, "Should be able to capture 16-build with RU 10"
print("✓ PASS: Can capture 16 via build\n")

print("=== Test: Same for Ace (14) and SP 2 (15) ===")
# Ace = 14
board5 = Board()
board5.add_card(Card("KL","7",30))
board5.add_card(Card("SP","7",31))  # 7+7=14 but not a build
player5 = Player("Test")
ace = Card("HJ","A",32)
player5.add_to_hand([ace])
combos_ace = generate_capture_combinations(board5, ace)
assert len(combos_ace) == 0, "Cannot capture 14 without build"
print("✓ Ace (14): Cannot capture without build")

# SP 2 = 15
board6 = Board()
board6.add_card(Card("KL","8",40))
board6.add_card(Card("SP","7",41))  # 8+7=15 but not a build
player6 = Player("Test")
sp2 = Card("SP","2",42)
player6.add_to_hand([sp2])
combos_sp2 = generate_capture_combinations(board6, sp2)
assert len(combos_sp2) == 0, "Cannot capture 15 without build"
print("✓ SP 2 (15): Cannot capture without build\n")

print("="*50)
print("ALL TESTS PASSED!")
print("Special value rule verified: 14/15/16 ONLY via builds!")
print("="*50)

