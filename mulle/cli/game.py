from ..models.deck import Deck
from ..models.board import Board
from ..models.player import Player
from ..rules.capture import auto_play_turn, enumerate_candidate_actions, generate_capture_combinations, perform_capture, can_build, perform_build, perform_discard, perform_trotta
from ..rules.scoring import score_round

import argparse
import random


def setup_initial_board(deck: Deck) -> Board:
    board = Board()
    for _ in range(8):
        board.add_card(deck.draw())
    return board


def setup_round(deck: Deck, deck_seed: int | None = None):
    # If deck_seed provided and deck empty create new deck (fallback)
    if deck.remaining() < 24:
        raise RuntimeError("Not enough cards left in deck for a new round")
    board = Board()
    for _ in range(8):
        board.add_card(deck.draw())
    players = [Player("Anna"), Player("Bo")]  # new hands per round
    for p in players:
        p.add_to_hand(deck.draw_many(8))
    return board, players


def render_board(board: Board) -> str:
    lines = []
    for idx, p in enumerate(board.piles):
        if hasattr(p, 'owner'):
            # Build
            lines.append(f"[{idx}] BUILD(owner={p.owner}) v={p.value}: " + ", ".join(c.code() for c in p.cards))
        else:
            lines.append(f"[{idx}] " + ", ".join(c.code() for c in p))
    return "\n".join(lines)


def render_hand(player: Player) -> str:
    return ", ".join(f"({i}) {c.code()}" for i, c in enumerate(player.hand))


def _find_hand_card_by_token(player: Player, token_parts: list[str]):
    # Try integer index first
    if token_parts:
        t0 = token_parts[0]
        try:
            idx = int(t0)
            if 0 <= idx < len(player.hand):
                return player.hand[idx]
        except ValueError:
            pass
        # Try code match: join remaining as code, e.g., ["SP","6"] -> "SP 6"
        code = " ".join(token_parts)
        for c in player.hand:
            if c.code().lower() == code.lower():
                return c
    return None


def _find_board_pile_by_index(board: Board, token: str):
    try:
        idx = int(token)
        if 0 <= idx < len(board.piles):
            return board.piles[idx]
    except ValueError:
        return None
    return None


def interactive_turn(board: Board, player: Player, round_number: int = 1) -> None:
    # Loop until a valid action is executed
    while True:
        print("\n--- Din tur:", player.name)
        print("Bord:")
        print(render_board(board))
        print("Hand:")
        print(render_hand(player))
        raw = input("Välj [c]apture, [b]uild, [t]rotta, [d]iscard eller [a]uto (ex: 'c 3 0' eller 't SP 8'): ").strip()
        if not raw:
            print("Ogiltigt val.")
            continue
        parts = raw.split()
        cmd = parts[0].lower()
        if cmd in ('a','auto'):
            res = auto_play_turn(board, player, round_number)
            print(f"Auto: {res}")
            return
        if cmd in ('t','trotta'):
            # Trotta: t <handIndex|CODE>
            card = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if card is None:
                if not player.hand:
                    print("Tom hand.")
                    continue
                try:
                    ci = int(input("Välj kortindex från handen att trotta: ").strip())
                    card = player.hand[ci]
                except Exception:
                    print("Ogiltigt val.")
                    continue
            try:
                res = perform_trotta(board, player, card, round_number)
                print(f"Trotta: {res}")
                return
            except ValueError as e:
                print(f"Kan inte trotta: {e}")
                continue
        if cmd in ('c','capture'):
            # Optional one-line: c <handIndex|CODE> [comboIndex]
            card = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if card is None:
                if not player.hand:
                    print("Tom hand.")
                    continue
                try:
                    ci = int(input("Välj kortindex från handen att spela för capture: ").strip())
                    card = player.hand[ci]
                except Exception:
                    print("Ogiltigt val.")
                    continue
            combos = generate_capture_combinations(board, card)
            if not combos:
                print("Inga möjliga capture-kombinationer för detta kort.")
                continue
            chosen = None
            if len(parts) >= 3:
                try:
                    sel = int(parts[2])
                    chosen = combos[sel]
                except Exception:
                    chosen = None
            if chosen is None:
                if len(combos) == 1:
                    chosen = combos[0]
                else:
                    for i, combo in enumerate(combos):
                        pile_idxs = [board.piles.index(p) for p in combo]
                        desc = []
                        for p in combo:
                            if hasattr(p, 'owner'):
                                desc.append(f"BUILD v={p.value}")
                            else:
                                desc.append("+".join(c.code() for c in p))
                        print(f"  ({i}) Piles {pile_idxs}: {' | '.join(desc)}")
                    try:
                        sel = int(input("Välj kombinationsindex att ta in: ").strip())
                        chosen = combos[sel]
                    except Exception:
                        print("Ogiltigt val.")
                        continue
            res = perform_capture(board, player, card, chosen)
            print(f"Capture: {res}")
            return
        if cmd in ('b','build'):
            # Optional one-line: b <handIndex|CODE> <boardIndex>
            card = None
            target = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if len(parts) >= 3:
                target = _find_board_pile_by_index(board, parts[2])
            if card is None:
                try:
                    ci = int(input("Välj kortindex från handen att lägga på en hög (build): ").strip())
                    card = player.hand[ci]
                except Exception:
                    print("Ogiltigt val.")
                    continue
            valid_targets = [p for p in board.piles if can_build(board, player, p, card)]
            if not valid_targets:
                print("Ingen giltig build med detta kort.")
                continue
            # ALWAYS show list and ask which to build on (never auto-select)
            for i, p in enumerate(valid_targets):
                idx = board.piles.index(p)
                if hasattr(p, 'owner'):
                    print(f"  ({i}) [{idx}] BUILD(owner={p.owner}) v={p.value}")
                else:
                    print(f"  ({i}) [{idx}] " + "+".join(c.code() for c in p))
            if target is not None and target in valid_targets:
                # Use provided target
                pass
            else:
                try:
                    ti = int(input("Välj mål-index från listan ovan: ").strip())
                    target = valid_targets[ti]
                except Exception:
                    print("Ogiltigt val.")
                    continue
            res = perform_build(board, player, target, card, round_number)
            print(f"Build: {res}")
            return
        if cmd in ('d','discard'):
            # Optional one-line: d <handIndex|CODE>
            card = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if card is None:
                if not player.hand:
                    print("Tom hand.")
                    continue
                try:
                    ci = int(input("Välj kortindex att slänga: ").strip())
                    card = player.hand[ci]
                except Exception:
                    print("Ogiltigt val.")
                    continue
            res = perform_discard(board, player, card)
            print(f"Discard: {res}")
            return
        print("Okänt val. Försök igen.")


def deal_hands(deck: Deck, players: list[Player]):
    for p in players:
        p.hand.clear()
        p.add_to_hand(deck.draw_many(8))


class SimpleLearningAI:
    def __init__(self, player: Player):
        self.player = player
        # value estimates per action category
        self.values = {
            'capture_combo_mulle': 10.0,
            'capture_combo': 5.0,
            'build': 1.0,
            'discard': 0.0
        }
        self.learning_rate = 0.2
        self.exploration = 0.15  # chance to explore

    def select_action(self, board: Board, round_number: int = 1):
        candidates = enumerate_candidate_actions(board, self.player, round_number)
        if not candidates:
            return None
        # Exploration
        if random.random() < self.exploration:
            return random.choice(candidates)
        # Score by current value * predicted_reward weight
        scored = []
        for c in candidates:
            base_val = self.values.get(c.category, 0.0)
            total_score = base_val + c.predicted_reward
            scored.append((total_score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def learn(self, action_category: str, reward: float):
        old = self.values.get(action_category, 0.0)
        self.values[action_category] = old + self.learning_rate * (reward - old)


def ai_turn(board: Board, ai: SimpleLearningAI, round_number: int = 1):
    action = ai.select_action(board, round_number)
    if not action:
        return None
    result = action.execute()
    # Reward heuristic: captured cards + 10 per mulle + build small bonus
    reward = len(result.captured) + 10 * len(result.mulle_pairs) + (2 if result.build_created else 0)
    ai.learn(action.category, reward)
    return result


def play_round(round_index: int, board: Board, players: list[Player], ai: SimpleLearningAI | None, interactive: bool = False):
    round_number = round_index + 1  # 1-based round number
    turn = 0
    while any(p.hand for p in players):
        current = players[turn % 2]
        if interactive and current.name == "Anna":
            interactive_turn(board, current, round_number)
        else:
            if ai and current is ai.player:
                res = ai_turn(board, ai, round_number)
            else:
                res = auto_play_turn(board, current, round_number)
            print(f"Auto ({current.name}): {res}")
        if not board.piles:
            current.tabbe += 1
        turn += 1

    # Check if there are any builds left on the board (this should not happen!)
    remaining_builds = board.list_builds()
    if remaining_builds:
        print("WARNING: Builds left on board at end of round!")
        for build in remaining_builds:
            print(f"  - {build.owner}'s build (value {build.value}, {len(build.cards)} cards)")
        print("  These builds should have been captured during the round!")

    scores = score_round(players)
    print(f"==== Round {round_number} Finished ====")
    print("Board empty:", len(board.piles) == 0)
    for p in players:
        print(f"{p.name} captured {len(p.captured)} cards, mulles: {[c.code() for c in p.mulles]}, tabbe={p.tabbe}")
    for s in scores:
        print(s)
    return scores


def play_session(seed: int, rounds: int, interactive: bool):
    random.seed(seed)
    deck = Deck(seed=seed)
    board = setup_initial_board(deck)  # only first round gets 8 board cards
    players = [Player("Anna"), Player("Bo")]
    ai = SimpleLearningAI(players[1])  # Bo as AI
    cumulative = {p.name: 0 for p in players}
    round_results = []
    for r in range(rounds):
        if deck.remaining() < 16:  # need 8+8 for hands
            print("Avbryter: för få kort kvar för ytterligare rond.")
            break
        deal_hands(deck, players)
        scores = play_round(r, board, players, ai, interactive if r == 0 else interactive)
        for s in scores:
            cumulative[s.player.name] += s.total
        # Rensa per-rond data (captured/mulles/tabbe) men behåll board TILLS sista ronden klar
        for p in players:
            p.captured.clear()
            p.mulles.clear()
            p.tabbe = 0
        round_results.append(scores)
    # Clear board AFTER final round per requirement
    board.piles.clear()
    print("==== Session Summary ====")
    print("Bordet rensat efter sista ronden. Högar kvar:", len(board.piles))
    for name, total in cumulative.items():
        print(f"{name}: total efter {len(round_results)} ronder = {total}")
    print("AI-värden:", ai.values)
    return round_results, cumulative, board, ai


def main():
    parser = argparse.ArgumentParser(description="Mulle prototype")
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--interactive', action='store_true', help='Interactive mode for Anna')
    parser.add_argument('--rounds', type=int, default=1, help='Number of rounds to play in session')
    args = parser.parse_args()
    play_session(seed=args.seed, rounds=args.rounds, interactive=args.interactive)

if __name__ == "__main__":
    main()
