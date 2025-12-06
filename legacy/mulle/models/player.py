from typing import List
from .card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.captured: List[Card] = []  # non-mulle captured
        self.mulles: List[Card] = []     # cards representing mulle points
        self.tabbe: int = 0

    def add_to_hand(self, cards: List[Card]):
        self.hand.extend(cards)

    def remove_from_hand(self, card: Card):
        self.hand.remove(card)

    def record_mulle(self, card: Card):
        self.mulles.append(card)

    def record_capture(self, cards: List[Card]):
        self.captured.extend(cards)

    def total_mulle_points(self) -> int:
        points = 0
        for c in self.mulles:
            if c.rank == "A":
                points += 14  # assumption
            elif c.rank in ["J", "Q", "K"]:
                # Face cards map to board values anyway
                points += c.value_on_board()
            else:
                points += int(c.rank)
        return points

    def __str__(self):
        return self.name

