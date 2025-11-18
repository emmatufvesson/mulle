from mulle.models.board import Board
from mulle.models.player import Player
from mulle.models.card import Card
from mulle.models.build import Build
from mulle.rules.capture import can_build, perform_trotta

print('='*60)
print('Test 1: Cannot trotta without reservation card')
print('='*60)
board = Board()
player = Player('Anna')
c4_hand = Card('HJ', '4', 0)
c4_board = Card('KL', '4', 0)
player.add_to_hand([c4_hand])  # Only one 4
board.add_card(c4_board)

try:
    result = perform_trotta(board, player, c4_hand, round_number=1)
    print('✗ FAILED: Should not allow trotta without reservation card!')
except ValueError as e:
    print(f'✓ PASSED: {e}')

print()
print('='*60)
print('Test 2: Opponent cannot rebuild locked build')
print('='*60)
board2 = Board()
anna = Player('Anna')
bo = Player('Bo')

# Create a locked 4-build owned by Anna
locked_build = Build([Card('HJ', '4', 0), Card('KL', '4', 0)], owner='Anna', target_value=4, locked=True, created_round=1)
board2.piles.append(locked_build)

# Bo tries to build on it with a 9 (4+9=13)
c9 = Card('SP', '9', 0)
cK = Card('SP', 'K', 0)  # King = 13 in hand
bo.add_to_hand([c9, cK])

can_rebuild = can_build(board2, bo, locked_build, c9)
print(f'Can Bo rebuild locked 4-build with 9? {can_rebuild}')
if not can_rebuild:
    print('✓ PASSED: Cannot rebuild locked build')
else:
    print('✗ FAILED: Should not allow rebuilding locked build!')

print()
print('='*60)
print('SUMMARY: Both tests should pass')
print('='*60)

