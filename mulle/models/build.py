from typing import List
from .card import Card

class Build:
    def __init__(self, cards: List[Card], owner: str, target_value: int, locked: bool=False):
        self.cards: List[Card] = list(cards)
        self.owner: str = owner  # name of player who owns/builds
        self.target_value: int = target_value  # the declared value of the build
        self.locked: bool = locked

    @property
    def value(self) -> int:
        return self.target_value

    def add_cards(self, cards: List[Card], actor: str):
        if self.locked:
            raise ValueError("Cannot modify locked build")
        if actor != self.owner:
            raise ValueError("Only owner may extend build")
        self.cards.extend(cards)

    def lock(self):
        self.locked = True

    def __repr__(self):
        state = 'LOCK' if self.locked else 'OPEN'
        return f"Build({state},owner={self.owner},v={self.value},cards={[c.code() for c in self.cards]})"
