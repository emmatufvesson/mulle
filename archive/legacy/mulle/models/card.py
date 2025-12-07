from dataclasses import dataclass
from typing import ClassVar

SUITS = ["KL", "SP", "HJ", "RU"]  # Clubs, Spades, Hearts, Diamonds (Swedish codes)
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

RANK_VALUES_BOARD = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13, "A": 1  # Ace=1 on board
}

@dataclass(frozen=True)
class Card:
    suit: str
    rank: str
    deck_id: int  # distinguish duplicates across two decks

    SPECIAL_HAND_VALUES: ClassVar[dict] = {
        ("SP", "2"): 15,  # Spader 2 = 15 i hand
        ("RU", "10"): 16  # Ruter 10 = 16 i hand
    }

    def value_on_board(self) -> int:
        return RANK_VALUES_BOARD[self.rank]

    def value_in_hand(self) -> int:
        # Ace=14 in hand
        if self.rank == "A":
            return 14
        return self.SPECIAL_HAND_VALUES.get((self.suit, self.rank), self.value_on_board())

    def code(self) -> str:
        return f"{self.suit} {self.rank}"

    def __str__(self) -> str:  # human friendly
        return self.code()

    def __repr__(self) -> str:
        return f"Card({self.suit},{self.rank},id={self.deck_id})"

