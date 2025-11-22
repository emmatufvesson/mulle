from ..models.deck import Deck
from ..models.board import Board
from ..models.player import Player


def render_board(board: Board) -> str:
    lines = []
    for idx, p in enumerate(board.piles):
        if hasattr(p, "owner"):
            lines.append(f"[{idx}] BUILD(owner={p.owner}) v={p.value}: " + ", ".join(c.code() for c in p.cards))
        else:
            lines.append(f"[{idx}] " + ", ".join(c.code() for c in p))
    return "\n".join(lines)


def render_hand(player: Player) -> str:
    return ", ".join(f"({i}) {c.code()}" for i, c in enumerate(player.hand))


def _find_hand_card_by_token(player: Player, token_parts: list[str]):
    if token_parts:
        t0 = token_parts[0]
        try:
            idx = int(t0)
            if 0 <= idx < len(player.hand):
                return player.hand[idx]
        except ValueError:
            pass
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


def interactive_turn(engine: GameEngine, board: Board, player: Player, round_number: int = 1):
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
        if cmd in ("a", "auto"):
            res = engine.play_auto(player, round_number)
            print(f"Auto: {res}")
            return res
        if cmd in ("t", "trotta"):
            card = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if card is None:
                print("Ogiltigt val.")
                continue
            try:
                res = engine.play_trotta(player, card, round_number)
                print(f"Trotta: {res}")
                return res
            except ValueError as e:
                print(f"Kan inte trotta: {e}")
                continue
        if cmd in ("c", "capture"):
            card = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if card is None:
                print("Ogiltigt val.")
                continue
            combos = engine.available_capture_combinations(card)
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
                            if hasattr(p, "owner"):
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
            res = engine.play_capture(player, card, chosen)
            print(f"Capture: {res}")
            return res
        if cmd in ("b", "build"):
            card = None
            target = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if len(parts) >= 3:
                target = _find_board_pile_by_index(board, parts[2])
            if card is None:
                print("Ogiltigt val.")
                continue
            valid_targets = [p for p in board.piles if engine.can_build_on(player, p, card)]
            if not valid_targets:
                print("Ingen giltig build med detta kort.")
                continue
            for i, p in enumerate(valid_targets):
                idx = board.piles.index(p)
                if hasattr(p, "owner"):
                    print(f"  ({i}) [{idx}] BUILD(owner={p.owner}) v={p.value}")
                else:
                    print(f"  ({i}) [{idx}] " + "+".join(c.code() for c in p))
            if target is None or target not in valid_targets:
                try:
                    ti = int(input("Välj mål-index från listan ovan: ").strip())
                    target = valid_targets[ti]
                except Exception:
                    print("Ogiltigt val.")
                    continue
            res = engine.play_build(player, target, card, round_number)
            print(f"Build: {res}")
            return res
        if cmd in ("d", "discard"):
            card = None
            if len(parts) >= 2:
                card = _find_hand_card_by_token(player, parts[1:2] if parts[1].isdigit() else parts[1:])
            if card is None:
                print("Ogiltigt val.")
                continue
            res = engine.play_discard(player, card)
            print(f"Discard: {res}")
            return res
        print("Okänt val. Försök igen.")


def deal_hands(deck: Deck, players: list[Player]):
    if deck.remaining() < 16:
        raise RuntimeError("Inte nog kort kvar i leken för att dela ut händer (behöver 16)")
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


def play_round(round_index: int, board: Board, players: list[Player], ai: SimpleLearningAI | None, starter_idx: int = 0, interactive: bool = False):
    round_number = round_index + 1  # 1-based round number
    turn = starter_idx  # who starts this round
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
    """
    rounds = number of omgångar; each omgång has exactly 6 rounds.
    Each omgång uses a fresh 2-deck shoe (104 cards): 8 to board initially + 6*16 to hands = 104 exactly.
    The starting player alternates between omgångar.
    """
    random.seed(seed)
    players = [Player("Anna"), Player("Bo")]
    ai = SimpleLearningAI(players[1])  # Bo as AI
    cumulative = {p.name: 0 for p in players}
    starting_player_idx = 0  # 0=Anna, 1=Bo

    all_omgang_results = []

    for omg in range(rounds):
        print(f"==== Startar Omgång {omg+1} (startar: {players[starting_player_idx].name}) ====")
        # Fresh deck and initial board with 8 cards
        deck = Deck(seed=seed + omg)
        board = setup_initial_board(deck)

        omgang_results = []
        # Play 6 rounds per omgång
        for r in range(6):
            deal_hands(deck, players)
            scores = play_round(r, board, players, ai, starter_idx=starting_player_idx, interactive=interactive if r == 0 and omg == 0 else False)
            for s in scores:
                cumulative[s.player.name] += s.total
            # Clear per-round data but keep board until end of omgång
            for p in players:
                p.captured.clear()
                p.mulles.clear()
                p.tabbe = 0
            omgang_results.append(scores)
        # End of omgång: clear board
        board.piles.clear()
        print(f"==== Omgång {omg+1} klar. Bord rensat. ====")
        # Alternate starter for next omgång
        starting_player_idx = 1 - starting_player_idx
        all_omgang_results.append(omgang_results)

    print("==== Session Summary ====")
    for name, total in result.cumulative.items():
        print(f"{name}: kumulativt efter {rounds} omgång(ar) = {total}")
    if result.ai_values:
        print("AI-värden:", result.ai_values)
    return result


def main():
    parser = argparse.ArgumentParser(description="Mulle prototype")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--interactive", action="store_true", help="Interactive mode for Anna (first round of first omgång)")
    parser.add_argument("--rounds", type=int, default=1, help="Number of omgångar to play (each has 6 rounds)")
    args = parser.parse_args()
    run_session(seed=args.seed, rounds=args.rounds, interactive=args.interactive)


if __name__ == "__main__":
    main()
