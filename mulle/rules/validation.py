"""Validation-funktioner för spelarhandlingar i Mulle."""

from ..models.board import Board
from ..models.player import Player


class InvalidAction(Exception):
    """Undantag som höjs när en spelaråtgärd inte är tillåten."""
    pass


def player_has_builds(board: Board, player: Player) -> bool:
    """
    Kontrollerar om en spelare har några byggen (låsta eller olåsta) på bordet.
    
    Args:
        board: Spelbrädet
        player: Spelaren att kontrollera
        
    Returns:
        True om spelaren har minst ett bygge, False annars
    """
    for build in board.list_builds():
        if build.owner == player.name:
            return True
    return False


def ensure_can_trail(board: Board, player: Player, card: Card = None) -> None:
    """
    Kontrollerar om en spelare får 'släppa' (trail) ett kort till bordet.
    
    En spelare får INTE släppa kort om spelaren har ett eller flera byggen
    på bordet. Spelaren måste först ta in (capture) sina byggen.
    
    Args:
        board: Spelbrädet
        player: Spelaren som vill släppa kort
        
    Raises:
        InvalidAction: Om spelaren har byggen på bordet
    """
    if player_has_builds(board, player):
        if card:
            raise InvalidAction(
                f"Kan inte släppa {card.code()} - {player.name} har byggen på bordet som måste tas in först!"
            )
        else:
            raise InvalidAction(
                f"Kan inte släppa kort: {player.name} har byggen på bordet som måste tas in först"
            )
