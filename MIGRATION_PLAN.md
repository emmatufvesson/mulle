# Mulle TypeScript Migration Plan

## Overview

This document outlines the plan for migrating the Mulle card game engine from Python to TypeScript.

## Migration Order

The migration follows a bottom-up approach, starting with core models and progressing to higher-level logic:

### Phase 1: Models (Foundation)

Port the data models from `mulle/models/` to `src/models/`:

1. `Card` - Card representation with suit, rank, and special properties
2. `Player` - Player state and hand management
3. `GameState` - Overall game state container
4. `Deck` - Deck management and shuffling

### Phase 2: Rules (Game Logic)

Port the game rules from `mulle/rules/` to `src/rules/`:

1. Card comparison and ranking rules
2. Turn validation rules
3. Special card rules (Trotta, etc.)
4. Win condition rules

### Phase 3: Engine (Orchestration)

Port the game engine from `mulle/engine/` to `src/engine/`:

1. Game initialization
2. Turn processing
3. State transitions
4. Event handling

### Phase 4: CLI (Optional)

Port the CLI interface from `mulle/cli/` if needed for testing and debugging.

## Testing Strategy

- Each ported module must have corresponding Jest tests
- Tests should mirror the existing Python tests in `tests/` and `test_*.py` files
- Use the legacy Python code as reference for expected behavior
- Run regression tests to ensure parity with Python implementation

## Current Status

- [x] Initial TypeScript project skeleton
- [x] Package.json with dev dependencies
- [x] TypeScript configuration
- [x] Directory structure for ported code
- [ ] Import Python sources to `legacy/` for reference
- [ ] Port models
- [ ] Add Jest tests for models
- [ ] Port rules
- [ ] Add Jest tests for rules
- [ ] Port engine
- [ ] Add Jest tests for engine
- [ ] Full regression testing

## Next Steps

1. **Import Legacy Sources**: Copy Python sources from `mulle/` into `legacy/` for reference during porting
2. **Start with Models**: Begin porting `mulle/models/` to `src/models/`
3. **Add Tests**: Create Jest tests that mirror the Python test cases
4. **Iterate**: Continue with rules and engine following the same pattern

## Notes

- The Python implementation remains the source of truth until the port is validated
- Breaking changes to the API should be minimized to maintain compatibility
- Document any intentional differences between Python and TypeScript implementations
