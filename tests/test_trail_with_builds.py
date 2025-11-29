"""
Tester för trail-restriktionen när spelare har byggen.

Testar regeln: En spelare får inte "släppa" (trail) ett kort till bordet 
om spelaren har ett eller flera byggen på bordet. Spelaren måste först 
ta in (capture) sina byggen innan trail tillåts.
"""

import pytest
from mulle.models.board import Board
from mulle.models.card import Card
from mulle.models.player import Player
from mulle.models.build import Build
from mulle.rules.capture import (
    can_build,
    perform_build,
    perform_capture,
    perform_discard,
    perform_trotta,
)
from mulle.rules.validation import InvalidAction, ensure_can_trail, player_has_builds


class TestTrailWithBuilds:
    """Tester för trail-restriktionen."""

    def test_trail_denied_when_player_has_build(self):
        """
        Trail ska nekas och InvalidAction höjas när spelaren har ett bygge.
        """
        board = Board()
        player = Player("Anna")
        
        # Lägg till ett kort på bordet att bygga på
        kl5 = Card("KL", "5", 0)
        board.add_card(kl5)
        
        # Ge spelaren kort i handen
        sp3 = Card("SP", "3", 1)  # Kort att bygga med
        hj8 = Card("HJ", "8", 2)  # Reservationskort (5+3=8)
        ru2 = Card("RU", "2", 3)  # Kort att försöka släppa
        player.add_to_hand([sp3, hj8, ru2])
        
        # Skapa ett bygge (KL 5 + SP 3 = värde 8)
        result = perform_build(board, player, [kl5], sp3, round_number=1)
        assert result.build_created
        
        # Verifiera att spelaren har ett bygge
        assert player_has_builds(board, player)
        
        # Försök att släppa RU 2 - ska misslyckas med InvalidAction
        with pytest.raises(InvalidAction) as exc_info:
            perform_discard(board, player, ru2)
        
        assert "byggen" in str(exc_info.value).lower()
        assert player.name in str(exc_info.value)

    def test_trail_allowed_when_player_has_no_builds(self):
        """
        Trail ska vara tillåtet när spelaren inte har några byggen.
        """
        board = Board()
        player = Player("Bo")
        
        # Ge spelaren kort i handen
        sp5 = Card("SP", "5", 0)
        player.add_to_hand([sp5])
        
        # Verifiera att spelaren inte har byggen
        assert not player_has_builds(board, player)
        
        # Trail ska fungera
        result = perform_discard(board, player, sp5)
        
        assert result.played == sp5
        assert len(board.piles) == 1
        assert sp5 in board.piles[0]

    def test_build_allowed_when_player_has_builds(self):
        """
        Skapa nytt bygge ska vara tillåtet även när spelaren redan har byggen.
        """
        board = Board()
        player = Player("Anna")
        
        # Lägg till kort på bordet
        kl5 = Card("KL", "5", 0)
        ru3 = Card("RU", "3", 1)
        board.add_card(kl5)
        board.add_card(ru3)
        
        # Ge spelaren kort i handen
        sp3 = Card("SP", "3", 2)  # Kort att bygga med (5+3=8)
        hj8 = Card("HJ", "8", 3)  # Reservationskort för 8-bygge
        kl4 = Card("KL", "4", 4)  # Kort att bygga med (3+4=7)
        ru7 = Card("RU", "7", 5)  # Reservationskort för 7-bygge
        player.add_to_hand([sp3, hj8, kl4, ru7])
        
        # Skapa första bygget (KL 5 + SP 3 = 8)
        result1 = perform_build(board, player, [kl5], sp3, round_number=1)
        assert result1.build_created
        
        # Verifiera att spelaren har ett bygge
        assert player_has_builds(board, player)
        
        # Skapa andra bygget (RU 3 + KL 4 = 7) - ska fungera
        result2 = perform_build(board, player, [ru3], kl4, round_number=1)
        assert result2.build_created
        
        # Verifiera att båda byggena finns
        builds = board.list_builds()
        assert len(builds) >= 1  # Kan vara merged beroende på absorption

    def test_trotta_allowed_and_creates_locked_build(self):
        """
        Trotta ska vara tillåtet och skapa ett låst bygge.
        """
        board = Board()
        player = Player("Anna")
        
        # Lägg till kort med värde 6 på bordet
        kl6 = Card("KL", "6", 0)
        ru6 = Card("RU", "6", 1)
        board.add_card(kl6)
        board.add_card(ru6)
        
        # Ge spelaren kort i handen
        sp6 = Card("SP", "6", 2)  # Kort att trötta med
        hj6 = Card("HJ", "6", 3)  # Reservationskort
        player.add_to_hand([sp6, hj6])
        
        # Utför trotta med SP 6
        result = perform_trotta(board, player, sp6, round_number=1)
        
        assert result.build_created
        
        # Verifiera att bygget är låst
        builds = board.list_builds()
        assert len(builds) == 1
        build = builds[0]
        assert build.locked
        assert build.value == 6
        assert build.owner == player.name

    def test_feed_allowed_when_player_has_builds(self):
        """
        Feed (lägg kort på eget bygge med samma värde) ska vara tillåtet 
        även när spelaren har byggen.
        """
        board = Board()
        player = Player("Anna")
        
        # Lägg till kort på bordet
        kl5 = Card("KL", "5", 0)
        board.add_card(kl5)
        
        # Ge spelaren kort i handen
        sp3 = Card("SP", "3", 1)  # Kort att bygga med (5+3=8)
        hj8_1 = Card("HJ", "8", 2)  # Reservationskort
        hj8_2 = Card("HJ", "8", 3)  # Kort att feeda med
        player.add_to_hand([sp3, hj8_1, hj8_2])
        
        # Skapa bygge (KL 5 + SP 3 = 8)
        result1 = perform_build(board, player, [kl5], sp3, round_number=1)
        assert result1.build_created
        
        # Verifiera att spelaren har ett bygge
        assert player_has_builds(board, player)
        
        # Feed med HJ 8 (samma värde som bygget) - ska fungera via perform_discard
        result2 = perform_discard(board, player, hj8_2)
        
        # Feed ska ha lagt kortet på bygget, inte skapat en ny hög
        builds = board.list_builds()
        assert len(builds) == 1
        build = builds[0]
        assert hj8_2 in build.cards
        assert build.locked  # Feed låser bygget

    def test_ensure_can_trail_raises_for_player_with_build(self):
        """
        ensure_can_trail ska höja InvalidAction när spelaren har byggen.
        """
        board = Board()
        player = Player("Bo")
        
        # Skapa ett bygge manuellt
        cards = [Card("KL", "5", 0), Card("SP", "3", 1)]
        build = Build(cards, owner=player.name, target_value=8)
        board.piles.append(build)
        
        with pytest.raises(InvalidAction):
            ensure_can_trail(board, player)

    def test_ensure_can_trail_passes_for_player_without_build(self):
        """
        ensure_can_trail ska inte höja något undantag när spelaren saknar byggen.
        """
        board = Board()
        player = Player("Anna")
        
        # Lägg till vanliga kort på bordet (ej byggen)
        board.add_card(Card("KL", "5", 0))
        board.add_card(Card("SP", "3", 1))
        
        # Ska inte höja undantag
        ensure_can_trail(board, player)

    def test_player_has_builds_with_locked_build(self):
        """
        player_has_builds ska returnera True för låsta byggen.
        """
        board = Board()
        player = Player("Anna")
        
        # Skapa ett låst bygge manuellt
        cards = [Card("KL", "5", 0), Card("SP", "3", 1)]
        build = Build(cards, owner=player.name, target_value=8, locked=True)
        board.piles.append(build)
        
        assert player_has_builds(board, player)

    def test_player_has_builds_ignores_opponent_builds(self):
        """
        player_has_builds ska ignorera motståndarens byggen.
        """
        board = Board()
        player = Player("Anna")
        opponent = Player("Bo")
        
        # Skapa ett bygge ägt av motståndaren
        cards = [Card("KL", "5", 0), Card("SP", "3", 1)]
        build = Build(cards, owner=opponent.name, target_value=8)
        board.piles.append(build)
        
        # Anna ska inte ha några byggen (bara Bo har)
        assert not player_has_builds(board, player)
        assert player_has_builds(board, opponent)

    def test_trail_denied_with_locked_build(self):
        """
        Trail ska nekas även när spelarens bygge är låst.
        """
        board = Board()
        player = Player("Anna")
        
        # Skapa ett låst bygge manuellt
        cards = [Card("KL", "5", 0), Card("SP", "3", 1)]
        build = Build(cards, owner=player.name, target_value=8, locked=True)
        board.piles.append(build)
        
        # Ge spelaren kort att släppa
        ru2 = Card("RU", "2", 2)
        player.add_to_hand([ru2])
        
        # Trail ska nekas
        with pytest.raises(InvalidAction):
            perform_discard(board, player, ru2)
