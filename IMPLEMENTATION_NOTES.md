# Implementation Notes - Build Up/Down Choice

## Changes Made (2025-11-20)

### 1. Locking Logic Update
- Builds now lock ONLY on:
  - Merge with existing build of same value
  - Absorption of external piles
  - Trotta/feed addition
- Removed automatic locking based on card count >2

### 2. Build Up/Down Choice (NEW)
When rebuilding an OPEN build, player must declare target value:
- GUI: Dialog asks "Bygg upp eller ner?" with calculated options
- CLI: Prompt shows possible values based on added card
- Validation: Ensures declared value matches card addition math

Implementation approach:
- Add `declared_value` parameter to `Board.create_build()` 
- When base_pile is Build and not locked, use declared_value instead of auto-calculating
- GUI: Show dialog before calling perform_build with chosen value
- CLI: Prompt and validate before build action

### Files to modify:
1. `mulle/models/board.py` - add declared_value param to create_build
2. `mulle/rules/capture.py` - add declared_value param to perform_build
3. `mulle/gui/game_gui.py` - add dialog for up/down choice
4. `mulle/cli/game.py` - add prompt for up/down choice
5. `RULEBOOK.md` - document up/down rule

### 3. Intake Scoring Update
Updated to exact specification:
- 1p: SP 3-K, RU A, KL A, HJ A
- 2p: SP 2, SP A, RU 10
