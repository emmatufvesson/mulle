from typing import List, Tuple, Callable
from itertools import combinations
from ..models.card import Card
from ..models.board import Board, Pile
from ..models.build import Build
from ..models.player import Player

class ActionResult:
    def __init__(self, played: Card, captured: List[Card], mulle_pairs: List[List[Card]], build_created: bool=False):
        self.played = played
        self.captured = captured
        self.mulle_pairs = mulle_pairs
        self.build_created = build_created

    def __repr__(self):
        return f"Action(played={self.played.code()}, captured={[c.code() for c in self.captured]}, mulles={[[c.code() for c in pair] for pair in self.mulle_pairs]}, build_created={self.build_created})"

class CandidateAction:
    def __init__(self, category: str, predicted_reward: float, executor: Callable[[], ActionResult]):
        self.category = category
        self.predicted_reward = predicted_reward
        self._executor = executor
    def execute(self) -> ActionResult:
        return self._executor()
    def __repr__(self):
        return f"CandidateAction(cat={self.category}, reward={self.predicted_reward})"

# --- Helper functions ---

def board_pile_value(pile: Pile) -> int:
    if isinstance(pile, Build):
        return pile.value
    return sum(c.value_on_board() for c in pile)

def is_card_reserved_for_build(board: Board, player: Player, card: Card) -> Build | None:
    """
    Check if a card is reserved as the only capture card for a player's build.
    Returns the build if the card is reserved, None otherwise.
    """
    card_hand_value = card.value_in_hand()

    # Check each build owned by the player
    for build in board.list_builds():
        if build.owner == player.name and build.value == card_hand_value:
            # Count how many cards in hand can capture this build
            matching_cards = [c for c in player.hand if c.value_in_hand() == build.value]
            # If this is the only card that can capture the build, it's reserved
            if len(matching_cards) == 1 and matching_cards[0] is card:
                return build
    return None

# Check if player may build (must own build or extend single pile) and have reservation card

def can_build(board: Board, player: Player, base_pile: Pile, added_card: Card) -> bool:
    base_cards = base_pile.cards if isinstance(base_pile, Build) else base_pile
    # Restrict: building on non-build piles allowed only for single-card piles
    if not isinstance(base_pile, Build) and len(base_cards) != 1:
        return False

    target_value = sum(c.value_on_board() for c in base_cards) + added_card.value_on_board()

    # Enforce: cannot create/extend to a value X if opponent already has a build of value X
    existing_same_value = board.list_builds_by_value(target_value)
    for b in existing_same_value:
        if b.owner != player.name:
            return False

    # Building on builds: locked builds cannot be modified at all
    if isinstance(base_pile, Build) and base_pile.locked:
        return False

    # Removed special-card build restriction: values 14 (A), 15 (SP 2), 16 (RU 10) are now allowed to be built.

    # Check if the card being used to build is reserved for another build
    reserved_build = is_card_reserved_for_build(board, player, added_card)
    if reserved_build is not None:
        # Cannot use this card to build - it's the only card that can capture another build
        return False

    # Need reservation card matching new build value
    for c in player.hand:
        if c is not added_card and c.value_in_hand() == target_value:
            return True
    return False

# Create build

def perform_build(board: Board, player: Player, base_pile: Pile, added_card: Card, round_number: int=1, declared_value: int | None=None) -> ActionResult:
    # Locked builds cannot be modified (already checked in can_build)
    # Open builds can be modified by anyone
    build = board.create_build(base_pile, added_card, owner=player.name, created_round=round_number, declared_value=declared_value)
    player.remove_from_hand(added_card)
    return ActionResult(played=added_card, captured=[], mulle_pairs=[], build_created=True)

# Generate all capture combinations given a played card

def generate_capture_combinations(board: Board, card: Card) -> List[List[Pile]]:
    target = card.value_in_hand()
    piles = list(board.piles)
    n = len(piles)
    # Special values (14=A, 15=SP 2, 16=RU 10) may ONLY be captured via an existing build of that value.
    # Identical single-card capture does NOT apply to these.
    if target in [14, 15, 16]:
        matching_builds = [p for p in piles if isinstance(p, Build) and p.value == target]
        return [matching_builds] if matching_builds else []

    # Normal identical single capture (non-special values): if exactly one identical single exists return that as sole option.
    identical_single = [p for p in piles if not isinstance(p, Build) and len(p)==1 and p[0].code()==card.code()]
    if len(identical_single) == 1:
        return [[identical_single[0]]]

    values = [board_pile_value(p) for p in piles]

    # Direct matches (must be included)
    direct_indices = [i for i, v in enumerate(values) if v == target]
    used = set(direct_indices)

    # Candidate indices for subset packing (exclude already used)
    cand_indices = [i for i in range(n) if i not in used and values[i] < target]

    # Precompute all subsets of candidates that sum to target
    subset_masks = []  # each mask is a frozenset of indices
    for r in range(1, len(cand_indices)+1):
        for combo in combinations(cand_indices, r):
            if sum(values[i] for i in combo) == target:
                subset_masks.append(frozenset(combo))

    # Backtracking to select maximum number of disjoint subsets
    best_selection: List[frozenset[int]] = []

    subset_masks_sorted = sorted(subset_masks, key=lambda s: (-len(s), tuple(sorted(s))))

    def backtrack(idx: int, used_now: set[int], chosen: List[frozenset[int]]):
        nonlocal best_selection
        # Prune if no better than current best (by pile count)
        current_count = sum(len(s) for s in chosen)
        best_count = sum(len(s) for s in best_selection)
        if current_count > best_count:
            best_selection = list(chosen)
        if idx >= len(subset_masks_sorted):
            return
        for j in range(idx, len(subset_masks_sorted)):
            mask = subset_masks_sorted[j]
            if not (mask & used_now):
                # choose
                chosen.append(mask)
                backtrack(j+1, used_now | set(mask), chosen)
                chosen.pop()
        # also consider skipping all remaining (already updated best if needed)

    backtrack(0, set(used), [])

    # Union of piles to capture = direct matches + all selected subsets
    capture_indices = set(direct_indices)
    for m in best_selection:
        capture_indices |= set(m)

    if not capture_indices:
        return []
    selected_piles = [piles[i] for i in sorted(capture_indices)]
    return [selected_piles]
# Detect mulle pairs among captured cards + played card (only pairs with exactly 2 identical cards in total capture group)

def detect_mulles(all_captured: List[Card], played: Card) -> List[List[Card]]:
    # Count by (suit, rank)
    counts = {}
    for c in all_captured:
        key = (c.suit, c.rank)
        counts[key] = counts.get(key, 0) + 1
    pairs = []
    for (suit, rank), count in counts.items():
        if count == 2:
            pair = [c for c in all_captured if c.suit == suit and c.rank == rank]
            pairs.append(pair)
    return pairs

# Perform capture using chosen combination

def perform_capture(board: Board, player: Player, played_card: Card, chosen: List[Pile]) -> ActionResult:
    # Gather captured cards
    captured_cards: List[Card] = []
    for pile in chosen:
        if isinstance(pile, Build):
            captured_cards.extend(pile.cards)
        else:
            captured_cards.extend(pile)  # list of cards
        board.remove_pile(pile)
    player.remove_from_hand(played_card)
    # Played card also part of capture group
    full_group = list(captured_cards) + [played_card]
    # Mulle detection
    mulle_pairs = detect_mulles(full_group, played_card)
    player.record_capture(full_group)
    for pair in mulle_pairs:
        # Register one card per pair for mulle points
        player.record_mulle(pair[0])
    return ActionResult(played=played_card, captured=full_group, mulle_pairs=mulle_pairs, build_created=False)

# Discard

def perform_discard(board: Board, player: Player, card: Card) -> ActionResult:
    # Check if this card is reserved for a build
    reserved_build = is_card_reserved_for_build(board, player, card)
    if reserved_build is not None:
        raise ValueError(f"Cannot discard {card.code()} - it's reserved to capture your {reserved_build.value}-build!")

    # Check if player has a build with the same value as the card being discarded
    # If so, add the card to that build (trotta)
    card_value = card.value_on_board()
    player_builds = [b for b in board.list_builds() if b.owner == player.name and b.value == card_value]

    if player_builds:
        # Add card to the first matching build (even if locked)
        build = player_builds[0]
        player.remove_from_hand(card)
        build.add_trotta_card(card)
        return ActionResult(played=card, captured=[], mulle_pairs=[], build_created=False)

    # Otherwise, normal discard
    player.remove_from_hand(card)
    board.add_card(card)
    return ActionResult(played=card, captured=[], mulle_pairs=[], build_created=False)

# Trotta: create a build by gathering all matching value singles and 2-card combinations
# OR add a card to an existing build with same value (even if locked)

def perform_trotta(board: Board, player: Player, card: Card, round_number: int=1) -> ActionResult:
    target_value = card.value_on_board()

    # First check if player already has a build with this value
    player_builds = [b for b in board.list_builds() if b.owner == player.name and b.value == target_value]

    if player_builds:
        # Add card to existing build (allowed even if locked)
        build = player_builds[0]
        player.remove_from_hand(card)
        build.add_trotta_card(card)
        return ActionResult(played=card, captured=[], mulle_pairs=[], build_created=False)

    # Find all single cards with exact value
    direct_singles = []
    for pile in board.piles:
        if not isinstance(pile, Build) and len(pile) == 1 and pile[0].value_on_board() == target_value:
            direct_singles.append(pile)

    # Find all 2-card piles/builds with total value equal to target
    two_card_matches = []
    for pile in board.piles:
        if isinstance(pile, Build) and len(pile.cards) == 2:
            if pile.value == target_value:
                two_card_matches.append(pile)
        elif isinstance(pile, list) and len(pile) == 2:
            if sum(c.value_on_board() for c in pile) == target_value:
                two_card_matches.append(pile)

    # Also find all pairs of single cards that sum to target
    single_piles = [p for p in board.piles if not isinstance(p, Build) and len(p) == 1]
    for i in range(len(single_piles)):
        for j in range(i+1, len(single_piles)):
            p1, p2 = single_piles[i], single_piles[j]
            if p1[0].value_on_board() + p2[0].value_on_board() == target_value:
                # Add both as separate matches (they'll be absorbed individually)
                if p1 not in two_card_matches and p1 not in direct_singles:
                    two_card_matches.append(p1)
                if p2 not in two_card_matches and p2 not in direct_singles:
                    two_card_matches.append(p2)

    # Must have at least one matching pile to trotta
    all_matches = direct_singles + two_card_matches
    if not all_matches:
        raise ValueError(f"No piles matching value {target_value} to trotta")

    # Collect all cards from matched piles
    cards = [card]  # Start with played card
    for pile in all_matches:
        if isinstance(pile, Build):
            cards.extend(pile.cards)
        else:
            cards.extend(pile)
        board.remove_pile(pile)

    # Create locked build
    new_build = Build(cards, owner=player.name, target_value=target_value, locked=True, created_round=round_number)
    board.piles.append(new_build)
    player.remove_from_hand(card)

    return ActionResult(played=card, captured=[], mulle_pairs=[], build_created=True)

# Heuristic priority: best combination with mulle > best largest combination > single identical (mulle) > single match > build > discard

def auto_play_turn(board: Board, player: Player, round_number: int=1) -> ActionResult:
    # Try each card for best combination capture
    best_combo: Tuple[int,int,List[Pile],Card, List[List[Card]]] | None = None  # (mulle_count, size, piles, card, mulles)
    for card in player.hand:
        combos = generate_capture_combinations(board, card)
        for combo in combos:
            # Evaluate combo
            captured_cards = []
            for pile in combo:
                if isinstance(pile, Build):
                    captured_cards.extend(pile.cards)
                else:
                    captured_cards.extend(pile)
            full_group = captured_cards + [card]
            mulles = detect_mulles(full_group, card)
            metric = (len(mulles), len(full_group))  # prioritize mulle count then total cards
            if best_combo is None or metric > (best_combo[0], best_combo[1]):
                best_combo = (len(mulles), len(full_group), combo, card, mulles)
    if best_combo:
        _, _, combo, card, _m = best_combo
        return perform_capture(board, player, card, combo)

    # Single identical (mulle) or single match
    for card in player.hand:
        # Find piles with single card matching board value and same code
        single_piles = [p for p in board.piles if not isinstance(p, Build) and len(p)==1]
        identical = [p for p in single_piles if p[0].code() == card.code()]
        if identical:
            return perform_capture(board, player, card, [identical[0]])
        # Any single value match (non-identical)
        value_match = [p for p in single_piles if p[0].value_on_board() == card.value_in_hand()]
        if value_match:
            return perform_capture(board, player, card, [value_match[0]])

    # Build attempt
    for card in player.hand:
        for pile in list(board.piles):
            if can_build(board, player, pile, card):
                return perform_build(board, player, pile, card, round_number)

    # Discard
    return perform_discard(board, player, player.hand[0])

def enumerate_candidate_actions(board: Board, player: Player, round_number: int=1) -> List[CandidateAction]:
    candidates: List[CandidateAction] = []
    # Capture combinations
    for card in list(player.hand):
        combos = generate_capture_combinations(board, card)
        for combo in combos:
            captured_cards = []
            for pile in combo:
                if isinstance(pile, Build):
                    captured_cards.extend(pile.cards)
                else:
                    captured_cards.extend(pile)
            full_group = captured_cards + [card]
            mulles = detect_mulles(full_group, card)
            cat = 'capture_combo_mulle' if mulles else 'capture_combo'
            reward = len(full_group) + 5 * len(mulles)
            def make_executor(card_local, combo_local):
                return lambda: perform_capture(board, player, card_local, combo_local)
            candidates.append(CandidateAction(cat, reward, make_executor(card, combo)))
    # Single captures (if not already covered as combos singleton) - we rely on combos; skip duplication.
    # Build actions
    for card in list(player.hand):
        for pile in list(board.piles):
            if can_build(board, player, pile, card):
                # Predicted reward modest (potential future capture); assign small heuristic value
                reward = 1.5
                def make_executor(card_local, pile_local):
                    return lambda: perform_build(board, player, pile_local, card_local, round_number)
                candidates.append(CandidateAction('build', reward, make_executor(card, pile)))
    # Discard fallback (choose one representative)
    if player.hand:
        card = player.hand[0]
        def discard_exec(card=card):
            return perform_discard(board, player, card)
        candidates.append(CandidateAction('discard', 0.0, discard_exec))
    return candidates
