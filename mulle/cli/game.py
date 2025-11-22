import argparse
from ..engine.game_service import ActionSelector, GameEngine
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


def run_session(seed: int, rounds: int, interactive: bool):
    engine = GameEngine(seed=seed)

    def selector(board: Board, player: Player, round_number: int):
        if interactive and player.name == "Anna":
            return interactive_turn(engine, board, player, round_number)
        return engine.play_auto(player, round_number)

    result = engine.play_session(rounds=rounds, interactive_selector=selector if interactive else None)

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
