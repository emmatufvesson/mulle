from mulle.models.deck import Deck
from mulle.models.board import Board
from mulle.models.player import Player
from mulle.models.card import Card
from mulle.rules.capture import can_build, perform_build

# Test 1: Build that should NOT lock (no absorption)
print("=== Test 1: Build without absorption (should stay OPEN) ===")
board = Board()
sp7 = Card("SP","7",0)
board.add_card(sp7)
player = Player("Anna")
sp5 = Card("SP","5",1)
queen = Card("SP","Q",2)
player.add_to_hand([sp5, queen])

# Build SP 5 on SP 7 = 12, with Q as reservation
res = perform_build(board, player, [sp7], sp5)
build = board.list_builds()[0]
print(f"Build value: {build.value}, Locked: {build.locked}, Cards: {[c.code() for c in build.cards]}")
assert not build.locked, "Build should be OPEN (no absorption)"
print("✓ PASS: Build is open\n")

# Test 2: Build that SHOULD lock (has absorption)
print("=== Test 2: Build with absorption (should LOCK) ===")
board2 = Board()
ru10 = Card("RU","10",10)
board2.add_card(ru10)
# Add a card with value 15 (will be absorbed)
sp5_board = Card("SP","5",11)
board2.add_card(sp5_board)
# Add a 2-card pile that sums to 15
board2.add_pile([Card("KL","7",12), Card("HJ","8",13)])

player2 = Player("Bo")
sp5_hand = Card("SP","5",14)
sp2 = Card("SP","2",15)  # reservation for value 15
player2.add_to_hand([sp5_hand, sp2])

res2 = perform_build(board2, player2, [ru10], sp5_hand)
build2 = board2.list_builds()[0]
print(f"Build value: {build2.value}, Locked: {build2.locked}, Cards: {[c.code() for c in build2.cards]}")
assert build2.locked, "Build should be LOCKED (absorbed other piles)"
print("✓ PASS: Build is locked\n")

# Test 3: Building on opponent's OPEN build
print("=== Test 3: Build on opponent's OPEN build (should be allowed) ===")
board3 = Board()
from mulle.models.build import Build
# Create an open build owned by Bo
open_build = Build([Card("HJ","7",20), Card("SP","2",21)], owner="Bo", target_value=9, locked=False)
board3.piles.append(open_build)

player3 = Player("Anna")
sp5_anna = Card("SP","5",22)
ace = Card("KL","A",23)  # reservation for 14
player3.add_to_hand([sp5_anna, ace])

can_rebuild = can_build(board3, player3, open_build, sp5_anna)
print(f"Can Anna rebuild Bo's OPEN build? {can_rebuild}")
assert can_rebuild, "Should be able to build on opponent's open build"
print("✓ PASS: Can rebuild opponent's open build\n")

# Test 4: Building on opponent's LOCKED build
print("=== Test 4: Build on opponent's LOCKED build (should be FORBIDDEN) ===")
board4 = Board()
locked_build = Build([Card("HJ","7",30), Card("SP","2",31)], owner="Bo", target_value=9, locked=True)
board4.piles.append(locked_build)

player4 = Player("Anna")
sp5_anna2 = Card("SP","5",32)
ace2 = Card("KL","A",33)
player4.add_to_hand([sp5_anna2, ace2])

cannot_rebuild = can_build(board4, player4, locked_build, sp5_anna2)
print(f"Can Anna rebuild Bo's LOCKED build? {cannot_rebuild}")
assert not cannot_rebuild, "Should NOT be able to build on locked build"
print("✓ PASS: Cannot rebuild locked build\n")

print("="*50)
print("ALL TESTS PASSED!")
print("="*50)

