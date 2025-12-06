import random
from typing import List
from .card import Card, SUITS, RANKS

class Deck:
    def __init__(self, seed: int | None = None):
        self._cards: List[Card] = []
        deck_id = 0
        # Two standard decks
        for duplicate in range(2):
            for suit in SUITS:
                for rank in RANKS:
                    self._cards.append(Card(suit, rank, deck_id))
                    deck_id += 1
        if seed is not None:
            random.seed(seed)
        random.shuffle(self._cards)

    def draw(self) -> Card:
        if not self._cards:
            raise RuntimeError("Deck empty")
        return self._cards.pop()

    def draw_many(self, n: int) -> List[Card]:
        return [self.draw() for _ in range(n)]

    def remaining(self) -> int:
        return len(self._cards)

