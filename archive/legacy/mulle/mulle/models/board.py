from typing import List, Union
from .card import Card
from .build import Build

Pile = Union[List[Card], Build]

class Board:
    def __init__(self):
        self.piles: List[Pile] = []  # each pile: list of cards (len>=1) or Build

    def add_card(self, card: Card):
        self.piles.append([card])

    def add_pile(self, cards: List[Card]):
        self.piles.append(cards)

    def remove_pile(self, pile: Pile):
        self.piles.remove(pile)

    def create_build(self, base_pile: Pile, added_card: Card, owner: str, created_round: int=1, declared_value: int | None=None) -> Build:
        # Remove base from board
        base_cards = base_pile.cards if isinstance(base_pile, Build) else base_pile
        self.remove_pile(base_pile)
        cards = list(base_cards) + [added_card]
        
        # Use declared_value if provided (for rebuilding open builds with up/down choice)
        # Otherwise calculate from card values
        if declared_value is not None:
            target_value = declared_value
        else:
            target_value = sum(c.value_on_board() for c in cards)

        # Check if build with this value already exists
        existing_builds = self.list_builds_by_value(target_value)
        if existing_builds:
            # Merge into first existing build of same value
            existing = existing_builds[0]
            before_len = len(existing.cards)
            existing.cards.extend(cards)
            # New locking rule: merging piles to same value always locks (value consolidation)
            existing.lock()
            return existing

        # Initial build (no existing build with this value)
        new_build = Build(cards, owner=owner, target_value=target_value, locked=False, created_round=created_round)

        # Absorb rule: ONLY single cards and 2-card piles/builds can be absorbed
        # 3+ card piles can only be used during capture, not absorbed into builds
        from itertools import combinations
        eligible = []
        for p in self.piles:
            if isinstance(p, Build):
                # Only 2-card unlocked builds can be absorbed
                if len(p.cards) == 2 and not p.locked:
                    eligible.append(p)
            elif isinstance(p, list):
                # Only single cards or 2-card piles, NOT 3+ card piles
                if len(p) == 1 or len(p) == 2:
                    eligible.append(p)
        values = [sum(c.value_on_board() for c in (p.cards if isinstance(p, Build) else p)) for p in eligible]
        direct = [i for i, v in enumerate(values) if v == target_value]
        chosen_sets = []
        used = set(direct)
        for i in direct:
            chosen_sets.append([i])
        cand = [i for i in range(len(eligible)) if i not in used and values[i] < target_value]
        subset_masks = []
        for r in range(1, len(cand) + 1):
            for combo in combinations(cand, r):
                if sum(values[i] for i in combo) == target_value:
                    subset_masks.append(combo)
        best_combo = []

        def backtrack(idx, current, used_indices):
            nonlocal best_combo
            if len(current) > len(best_combo):
                best_combo = list(current)
            if idx >= len(subset_masks):
                return
            for j in range(idx, len(subset_masks)):
                mask = subset_masks[j]
                if any(m in used_indices for m in mask):
                    continue
                current.append(mask)
                backtrack(j + 1, current, used_indices | set(mask))
                current.pop()

        backtrack(0, [], set())
        for combo in best_combo:
            chosen_sets.append(list(combo))
        absorb_flat = set()
        for group in chosen_sets:
            for idx in group:
                absorb_flat.add(idx)
        absorbed_any = False
        for idx in sorted(absorb_flat, reverse=True):
            pile = eligible[idx]
            pile_cards = pile.cards if isinstance(pile, Build) else pile
            new_build.cards.extend(pile_cards)
            self.remove_pile(pile)
            absorbed_any = True

        # Lock only if absorption actually occurred (external material pulled in)
        if absorbed_any:
            new_build.lock()

        self.piles.append(new_build)
        return new_build

    def list_builds(self) -> List[Build]:
        return [p for p in self.piles if isinstance(p, Build)]

    def list_builds_by_value(self, value: int) -> List[Build]:
        return [b for b in self.list_builds() if b.value == value]

    def is_empty(self) -> bool:
        return len(self.piles) == 0

    def __repr__(self):
        rep = []
        for idx, p in enumerate(self.piles):
            if isinstance(p, Build):
                rep.append(f"[{idx}] BUILD({'LOCK' if p.locked else 'OPEN'}) owner={p.owner} v={p.value} -> {[c.code() for c in p.cards]}")
            else:
                rep.append(f"[{idx}] {'+' if len(p)>1 else ''}{[c.code() for c in p]}")
        return "\n".join(rep)
