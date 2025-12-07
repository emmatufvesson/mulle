import tkinter as tk
from tkinter import messagebox, ttk, font
from ..engine.game_service import GameEngine
from ..models.board import Board
from ..models.build import Build
from ..rules.scoring import score_round

# Suit symbols
SUIT_SYMBOLS = {
    "SP": "♠",  # Spader
    "HJ": "♥",  # Hjärter
    "RU": "♦",  # Ruter
    "KL": "♣"   # Klöver
}

SUIT_COLORS = {
    "SP": "black",
    "HJ": "red",
    "RU": "red",
    "KL": "black"
}

# Suit order for sorting
SUIT_ORDER = {"KL": 0, "SP": 1, "HJ": 2, "RU": 3}


def sort_cards(cards):
    """Sort cards by suit then by rank"""
    def card_key(card):
        suit_order = SUIT_ORDER.get(card.suit, 99)
        rank_order = "23456789JQKA".index(card.rank) if card.rank in "23456789JQKA" else 99
        return (suit_order, rank_order)
    return sorted(cards, key=card_key)


class MulleGUI:
    def __init__(self, root, seed=42):
        self.root = root
        self.root.title("Mulle")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2d5016")

        # Game state
        self.seed = seed
        self.engine = GameEngine(seed=self.seed)
        self.deck = None
        self.board = None
        self.players = None
        self.current_player_idx = 0
        self.round_number = 0
        self.cumulative_scores = {"Anna": 0, "Bo": 0}
        # Track who starts each omgång (0=Anna,1=Bo)
        self.starting_player_idx = 0
        # Omgång-tally (accumulate scores across 6 rounds before summing)
        self.omgang_tally = {
            "Anna": {"mulle_points": 0, "intake": 0, "tabbe": 0, "total": 0},
            "Bo":   {"mulle_points": 0, "intake": 0, "tabbe": 0, "total": 0},
        }

        # UI state
        self.selected_hand_card = None
        self.action_mode = None  # 'capture', 'build', 'trotta', 'discard'

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        # Top frame - scores and controls
        top_frame = tk.Frame(self.root, bg="#2d5016")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.score_label = tk.Label(top_frame, text="", font=("Arial", 14, "bold"),
                                    bg="#2d5016", fg="white")
        self.score_label.pack(side=tk.LEFT, padx=10)

        tk.Button(top_frame, text="Ny Rond", command=self.new_round,
                 font=("Arial", 12), bg="#4a7c2e", fg="white").pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="Nytt Spel", command=self.new_game,
                 font=("Arial", 12), bg="#4a7c2e", fg="white").pack(side=tk.RIGHT, padx=5)

        # Board frame
        board_frame = tk.LabelFrame(self.root, text="Bord", font=("Arial", 12, "bold"),
                                   bg="#1a3d0a", fg="white", relief=tk.RIDGE, bd=3)
        board_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.board_canvas = tk.Canvas(board_frame, bg="#2d5016", highlightthickness=0)
        self.board_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Action buttons frame
        action_frame = tk.Frame(self.root, bg="#2d5016")
        action_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(action_frame, text="Åtgärd:", font=("Arial", 11, "bold"),
                bg="#2d5016", fg="white").pack(side=tk.LEFT, padx=5)

        self.capture_btn = tk.Button(action_frame, text="📥 Capture", command=lambda: self.set_action('capture'),
                                     font=("Arial", 10, "bold"), width=12, bg="#3d6b1f", fg="white")
        self.capture_btn.pack(side=tk.LEFT, padx=3)

        self.build_btn = tk.Button(action_frame, text="🏗️ Build", command=lambda: self.set_action('build'),
                                   font=("Arial", 10, "bold"), width=12, bg="#3d6b1f", fg="white")
        self.build_btn.pack(side=tk.LEFT, padx=3)

        self.trotta_btn = tk.Button(action_frame, text="🔒 Trotta", command=lambda: self.set_action('trotta'),
                                    font=("Arial", 10, "bold"), width=12, bg="#3d6b1f", fg="white")
        self.trotta_btn.pack(side=tk.LEFT, padx=3)

        self.discard_btn = tk.Button(action_frame, text="🗑️ Discard", command=lambda: self.set_action('discard'),
                                     font=("Arial", 10, "bold"), width=12, bg="#3d6b1f", fg="white")
        self.discard_btn.pack(side=tk.LEFT, padx=3)

        self.auto_btn = tk.Button(action_frame, text="🤖 Auto", command=self.auto_play,
                                  font=("Arial", 10, "bold"), width=12, bg="#6b4a1f", fg="white")
        self.auto_btn.pack(side=tk.LEFT, padx=3)

        self.status_label = tk.Label(action_frame, text="Välj åtgärd och kort",
                                     font=("Arial", 10, "bold"), bg="#2d5016", fg="yellow")
        self.status_label.pack(side=tk.LEFT, padx=20)

        # Hand frame
        hand_frame = tk.LabelFrame(self.root, text="👤 Din Hand (Anna)", font=("Arial", 12, "bold"),
                                  bg="#1a3d0a", fg="white", relief=tk.RIDGE, bd=3)
        hand_frame.pack(fill=tk.X, padx=10, pady=5)

        self.hand_canvas = tk.Canvas(hand_frame, bg="#2d5016", height=140, highlightthickness=0)
        self.hand_canvas.pack(fill=tk.X, padx=5, pady=5)

        # Score details frame (side by side for both players)
        score_detail_frame = tk.Frame(self.root, bg="#2d5016")
        score_detail_frame.pack(fill=tk.X, padx=10, pady=5)

        # Anna's score detail
        anna_score_frame = tk.LabelFrame(score_detail_frame, text="👤 Anna - Poäng", font=("Arial", 10, "bold"),
                                        bg="#1a3d0a", fg="white", relief=tk.RIDGE, bd=2)
        anna_score_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.anna_score_label = tk.Label(anna_score_frame, text="Mullar: 0\nTabbe: 0\nIntag: 0\nBonus: 0\n────\nTotalt: 0",
                                        font=("Arial", 9), bg="#2d5016", fg="white", justify=tk.LEFT)
        self.anna_score_label.pack(padx=5, pady=3)

        # Bo's score detail
        bo_score_frame = tk.LabelFrame(score_detail_frame, text="🤖 Bo - Poäng", font=("Arial", 10, "bold"),
                                      bg="#1a3d0a", fg="white", relief=tk.RIDGE, bd=2)
        bo_score_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.bo_score_label = tk.Label(bo_score_frame, text="Mullar: 0\nTabbe: 0\nIntag: 0\nBonus: 0\n────\nTotalt: 0",
                                      font=("Arial", 9), bg="#2d5016", fg="white", justify=tk.LEFT)
        self.bo_score_label.pack(padx=5, pady=3)

    def draw_card(self, canvas, x, y, card, width=70, height=100, selected=False):
        """Draw a playing card with proper graphics"""
        # Card background
        bg_color = "#90ee90" if selected else "white"
        outline_color = "#00aa00" if selected else "black"
        outline_width = 3 if selected else 2

        card_rect = canvas.create_rectangle(x, y, x+width, y+height,
                                           fill=bg_color, outline=outline_color,
                                           width=outline_width, tags="card")

        # Get suit and rank
        suit = card.suit
        rank = card.rank
        suit_symbol = SUIT_SYMBOLS.get(suit, suit)
        suit_color = SUIT_COLORS.get(suit, "black")

        # Top-left corner: rank and suit
        canvas.create_text(x+10, y+15, text=rank, font=("Arial", 14, "bold"),
                          fill=suit_color, anchor="nw")
        canvas.create_text(x+10, y+30, text=suit_symbol, font=("Arial", 16),
                          fill=suit_color, anchor="nw")

        # Center: large suit symbol
        canvas.create_text(x+width//2, y+height//2, text=suit_symbol,
                          font=("Arial", 36, "bold"), fill=suit_color)

        # Bottom-right corner: rank and suit (upside down)
        canvas.create_text(x+width-10, y+height-15, text=rank,
                          font=("Arial", 14, "bold"), fill=suit_color, anchor="se")
        canvas.create_text(x+width-10, y+height-30, text=suit_symbol,
                          font=("Arial", 16), fill=suit_color, anchor="se")

        # Values info (smaller)
        canvas.create_text(x+width//2, y+height-10,
                          text=f"B:{card.value_on_board()} H:{card.value_in_hand()}",
                          font=("Arial", 7), fill="gray")

        return card_rect

    def new_game(self):
        self.engine.start_omgang(0)
        self.engine.deal_hands()
        self.deck = self.engine.deck
        self.board = self.engine.board
        self.players = self.engine.players
        # Start omgång with configured starter
        self.current_player_idx = self.starting_player_idx
        self.round_number = 1
        # Reset tallies
        self.cumulative_scores = {"Anna": 0, "Bo": 0}
        self.omgang_tally = {
            "Anna": {"mulle_points": 0, "intake": 0, "tabbe": 0, "total": 0},
            "Bo":   {"mulle_points": 0, "intake": 0, "tabbe": 0, "total": 0},
        }
        self.selected_hand_card = None
        self.action_mode = None
        self.update_display()
        # If Bo starts, auto-play his first move after load
        if self.current_player_idx == 1:
            self.root.after(800, self.bo_auto_play)

    def new_round(self):
        if self.engine.deck.remaining() < 16:
            messagebox.showinfo("Slut på kort", "Inte nog kort för en ny rond!")
            return
        for p in self.players:
            p.hand.clear()
            p.captured.clear()
            p.mulles.clear()
            p.tabbe = 0
        self.engine.deal_hands()
        # Each round in an omgång starts with the omgång's starter
        self.current_player_idx = self.starting_player_idx
        self.round_number += 1
        self.selected_hand_card = None
        self.action_mode = None
        self.update_display()
        if self.current_player_idx == 1:
            self.root.after(800, self.bo_auto_play)

    def set_action(self, mode):
        self.action_mode = mode
        self.status_label.config(text=f"Läge: {mode.upper()} - Välj kort från hand")
        self.highlight_action_button()

    def highlight_action_button(self):
        for btn in [self.capture_btn, self.build_btn, self.trotta_btn, self.discard_btn]:
            btn.config(relief=tk.RAISED, bg="#3d6b1f")
        if self.action_mode == 'capture':
            self.capture_btn.config(relief=tk.SUNKEN, bg="#5a9b2f")
        elif self.action_mode == 'build':
            self.build_btn.config(relief=tk.SUNKEN, bg="#5a9b2f")
        elif self.action_mode == 'trotta':
            self.trotta_btn.config(relief=tk.SUNKEN, bg="#5a9b2f")
        elif self.action_mode == 'discard':
            self.discard_btn.config(relief=tk.SUNKEN, bg="#5a9b2f")

    def update_display(self):
        self.draw_board()
        self.draw_hand()
        self.update_scores()

    def draw_board(self):
        self.board_canvas.delete("all")
        x, y = 10, 10

        for i, pile in enumerate(self.board.piles):
            if hasattr(pile, 'owner'):  # Build
                # Draw build container
                num_cards = len(pile.cards)
                container_width = 80 + (num_cards - 1) * 20
                container_height = 120

                color = "#ffd700" if pile.locked else "#87ceeb"
                lock_text = "🔒 LÅST" if pile.locked else "🔓 ÖPPEN"

                # Build background
                build_rect = self.board_canvas.create_rectangle(
                    x, y, x+container_width, y+container_height,
                    fill=color, outline="black", width=3, tags=f"pile_{i}"
                )

                # Build info
                self.board_canvas.create_text(
                    x+container_width//2, y+10,
                    text=f"[{i}] {lock_text}", font=("Arial", 9, "bold")
                )
                self.board_canvas.create_text(
                    x+container_width//2, y+25,
                    text=f"{pile.owner} • Värde: {pile.value}",
                    font=("Arial", 8)
                )

                # Draw cards in build (stacked)
                card_x = x + 5
                card_y = y + 35
                sorted_cards = sort_cards(pile.cards)
                for j, card in enumerate(sorted_cards):
                    self.draw_card(self.board_canvas, card_x + j*15, card_y, card,
                                  width=60, height=75)

                self.board_canvas.tag_bind(build_rect, "<Button-1>",
                                          lambda e, idx=i: self.on_board_click(idx))

                x += container_width + 10
            else:  # Regular pile
                # Draw pile of cards
                pile_width = 80 + (len(pile) - 1) * 15

                # Pile background
                pile_bg = self.board_canvas.create_rectangle(
                    x, y, x+pile_width, y+120,
                    fill="#f0e68c", outline="black", width=2, tags=f"pile_{i}"
                )

                self.board_canvas.create_text(
                    x+10, y+10, text=f"[{i}]", font=("Arial", 9, "bold")
                )

                # Draw cards (stacked)
                card_x = x + 5
                card_y = y + 20
                sorted_pile = sort_cards(pile)
                for j, card in enumerate(sorted_pile):
                    self.draw_card(self.board_canvas, card_x + j*15, card_y, card,
                                  width=60, height=80)

                self.board_canvas.tag_bind(pile_bg, "<Button-1>",
                                          lambda e, idx=i: self.on_board_click(idx))

                x += pile_width + 10

            # Wrap to next line if needed
            if x > 1000:
                x = 10
                y += 130

    def draw_hand(self):
        self.hand_canvas.delete("all")
        current_player = self.players[self.current_player_idx]
        if current_player.name != "Anna":
            return

        # Sort hand by suit and rank
        sorted_hand = sort_cards(current_player.hand)

        x = 10
        for sorted_idx, card in enumerate(sorted_hand):
            # Find original index in unsorted hand
            original_idx = current_player.hand.index(card)
            selected = (self.selected_hand_card == original_idx)
            card_rect = self.draw_card(self.hand_canvas, x, 10, card,
                                      width=80, height=120, selected=selected)

            # Make entire card clickable
            self.hand_canvas.tag_bind(card_rect, "<Button-1>",
                                     lambda e, idx=original_idx: self.on_hand_click(idx))
            # Also bind to the card tag for text elements
            for item in self.hand_canvas.find_overlapping(x, 10, x+80, 130):
                self.hand_canvas.tag_bind(item, "<Button-1>",
                                         lambda e, idx=original_idx: self.on_hand_click(idx))

            x += 90

    def update_scores(self):
        anna_total = self.cumulative_scores["Anna"]
        bo_total = self.cumulative_scores["Bo"]
        anna_omg = self.omgang_tally["Anna"]["total"]
        bo_omg = self.omgang_tally["Bo"]["total"]
        self.score_label.config(text=f"Rond {self.round_number} | Omgång: Anna {anna_omg} • Bo {bo_omg} | Total: Anna {anna_total} • Bo {bo_total}")
        
        # Update detailed score breakdowns
        a_tally = self.omgang_tally["Anna"]
        b_tally = self.omgang_tally["Bo"]
        
        # Calculate bonus for each player
        a_bonus = (a_tally["intake"] - 20) * 2 if a_tally["intake"] > 20 else 0
        b_bonus = (b_tally["intake"] - 20) * 2 if b_tally["intake"] > 20 else 0
        
        # Get mulle card details
        anna_mulles = self.players[0].mulles if self.players else []
        bo_mulles = self.players[1].mulles if self.players else []
        anna_mulle_text = ", ".join(c.code() for c in anna_mulles) if anna_mulles else "inga"
        bo_mulle_text = ", ".join(c.code() for c in bo_mulles) if bo_mulles else "inga"
        
        self.anna_score_label.config(text=f"Mullar ({a_tally['mulle_points']}p): {anna_mulle_text}\n"
                                          f"Tabbe: {a_tally['tabbe']}p\n"
                                          f"Intag: {a_tally['intake']}p\n"
                                          f"Bonus: {a_bonus}p\n"
                                          f"────────\n"
                                          f"Totalt: {a_tally['total']}p")
        
        self.bo_score_label.config(text=f"Mullar ({b_tally['mulle_points']}p): {bo_mulle_text}\n"
                                        f"Tabbe: {b_tally['tabbe']}p\n"
                                        f"Intag: {b_tally['intake']}p\n"
                                        f"Bonus: {b_bonus}p\n"
                                        f"────────\n"
                                        f"Totalt: {b_tally['total']}p")

    def update_bo_info(self):
        # Removed - now handled in score panels
        pass

    def on_hand_click(self, idx):
        if self.current_player_idx != 0:  # Not Anna's turn
            return
        self.selected_hand_card = idx
        self.draw_hand()
        if self.action_mode:
            self.status_label.config(text=f"{self.action_mode.upper()}: Kort valt - Klicka på bord eller utför")
            if self.action_mode in ['trotta', 'discard']:
                self.execute_action()

    def on_board_click(self, pile_idx):
        if self.current_player_idx != 0 or self.selected_hand_card is None:
            return
        if self.action_mode == 'build':
            self.execute_build(pile_idx)
        elif self.action_mode == 'capture':
            self.execute_capture(pile_idx)

    def execute_action(self):
        if self.selected_hand_card is None:
            messagebox.showwarning("Inget kort", "Välj ett kort från hand först!")
            return

        player = self.players[0]
        card = player.hand[self.selected_hand_card]

        try:
            if self.action_mode == 'trotta':
                result = self.engine.play_trotta(player, card, self.round_number)
                self.status_label.config(text=f"Trotta utfört: {len(result.captured)} kort")
            elif self.action_mode == 'discard':
                result = self.engine.play_discard(player, card)
                self.status_label.config(text="Kort slängt")
            self.next_turn()
        except Exception as e:
            messagebox.showerror("Fel", str(e))

    def execute_build(self, pile_idx):
        player = self.players[0]
        card = player.hand[self.selected_hand_card]
        pile = self.board.piles[pile_idx]

        if not self.engine.can_build_on(player, pile, card):
            messagebox.showwarning("Ogiltigt drag", "Kan inte bygga här!")
            return

        # Check if rebuilding an open build - if so, ask for up/down choice
        declared_value = None
        if isinstance(pile, Build) and not pile.locked:
            current_value = pile.value
            card_board_value = card.value_on_board()
            value_up = current_value + card_board_value
            value_down = abs(current_value - card_board_value)
            
            # Create dialog to ask up or down
            dialog = tk.Toplevel(self.root)
            dialog.title("Bygg upp eller ner")
            dialog.geometry("300x150")
            dialog.configure(bg="#2d5016")
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text=f"Nuvarande bygge: {current_value}\nKort: {card.code()} (värde {card_board_value})\n\nVälj nytt värde:",
                    font=("Arial", 11), bg="#2d5016", fg="white").pack(pady=10)
            
            choice_frame = tk.Frame(dialog, bg="#2d5016")
            choice_frame.pack(pady=10)
            
            chosen = [None]  # Use list to capture value from button callback
            
            def choose_up():
                chosen[0] = value_up
                dialog.destroy()
            
            def choose_down():
                chosen[0] = value_down
                dialog.destroy()
            
            tk.Button(choice_frame, text=f"↑ Upp ({value_up})", command=choose_up,
                     font=("Arial", 12, "bold"), width=10, bg="#4a7c2e", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(choice_frame, text=f"↓ Ner ({value_down})", command=choose_down,
                     font=("Arial", 12, "bold"), width=10, bg="#4a7c2e", fg="white").pack(side=tk.LEFT, padx=5)
            
            self.root.wait_window(dialog)
            
            if chosen[0] is None:
                return  # User closed dialog without choosing
            
            declared_value = chosen[0]

        try:
            result = self.engine.play_build(player, pile, card, self.round_number, declared_value)
            self.status_label.config(text="Bygge skapat!")
            self.next_turn()
        except Exception as e:
            messagebox.showerror("Fel", str(e))

    def execute_capture(self, pile_idx=None):
        player = self.players[0]
        card = player.hand[self.selected_hand_card]

        combos = self.engine.available_capture_combinations(card)
        if not combos:
            messagebox.showwarning("Ingen capture", "Inget att ta in med detta kort!")
            return

        # Use first combo (simplified - could show dialog to choose)
        chosen = combos[0]
        try:
            result = self.engine.play_capture(player, card, chosen)
            mulle_details = ""
            if result.mulle_pairs:
                mulle_cards = [pair[0].code() for pair in result.mulle_pairs]
                mulle_details = f" (Mullar: {', '.join(mulle_cards)})"
            self.status_label.config(text=f"Intag: {len(result.captured)} kort{mulle_details}")
            self.next_turn()
        except Exception as e:
            messagebox.showerror("Fel", str(e))

    def auto_play(self):
        player = self.players[self.current_player_idx]
        try:
            result = self.engine.play_auto(player, self.round_number)
            self.status_label.config(text=f"{player.name} auto: {len(result.captured)} kort intagna")
            self.next_turn()
        except Exception as e:
            messagebox.showerror("Fel", str(e))

    def next_turn(self):
        self.selected_hand_card = None
        self.action_mode = None
        self.highlight_action_button()

        # Check for tabbe
        if not self.board.piles:
            self.players[self.current_player_idx].tabbe += 1

        # Switch player
        self.current_player_idx = (self.current_player_idx + 1) % 2

        # Check if round is over
        if not any(p.hand for p in self.players):
            self.end_round()
            return

        self.update_display()

        # If Bo's turn, auto play
        if self.current_player_idx == 1:
            self.root.after(1000, self.bo_auto_play)

    def bo_auto_play(self):
        bo = self.players[1]
        if bo.hand:
            try:
                result = self.engine.play_auto(bo, self.round_number)

                # Show Bo's move in a dialog
                captured_text = ", ".join(c.code() for c in result.captured) if result.captured else "inga"
                mulle_details = ""
                if result.mulle_pairs:
                    mulle_cards = [f"{pair[0].code()}" for pair in result.mulle_pairs]
                    mulle_details = f"\nMullar ({len(result.mulle_pairs)}): {', '.join(mulle_cards)}"

                move_text = f"Bo spelade: {result.played.code()}\n" \
                           f"Tog in: {captured_text}{mulle_details}\n" \
                           f"Bygge skapat: {'Ja' if result.build_created else 'Nej'}"

                # Create a custom dialog with OK button
                dialog = tk.Toplevel(self.root)
                dialog.title("Bos drag")
                dialog.geometry("400x200")
                dialog.configure(bg="#2d5016")

                tk.Label(dialog, text=move_text, font=("Arial", 12),
                        bg="#2d5016", fg="white", justify=tk.LEFT).pack(pady=20, padx=20)

                def on_ok():
                    dialog.destroy()
                    self.next_turn()

                tk.Button(dialog, text="OK", command=on_ok, font=("Arial", 12),
                         bg="#4a7c2e", fg="white", width=10).pack(pady=10)

                # Make dialog modal
                dialog.transient(self.root)
                dialog.grab_set()
                dialog.focus_set()

            except Exception as e:
                messagebox.showerror("Fel", str(e))

    def end_round(self):
        # Check if there are any builds left on the board
        remaining_builds = self.board.list_builds()
        if remaining_builds:
            # Warn the player that builds remain
            build_info = "\n".join([f"- {b.owner}'s bygge (värde {b.value})" for b in remaining_builds])
            messagebox.showwarning(
                "Byggen kvar på bordet!",
                f"Följande byggen togs inte in under ronden:\n\n{build_info}\n\n"
                f"OBS: Dessa byggen ska ha tagits in! Kontrollera reglerna."
            )
        # Compute this round's scores and accumulate into omgång-tally
        round_scores = score_round(self.players)
        for s in round_scores:
            self.omgang_tally[s.player.name]["mulle_points"] += s.mulle_points
            self.omgang_tally[s.player.name]["intake"] += s.intake
            self.omgang_tally[s.player.name]["tabbe"] += s.tabbe
            self.omgang_tally[s.player.name]["total"] += s.total
        # Update header with current tallies
        self.update_scores()

        # End-of-omgång check: 6 rounds
        if self.round_number >= 6:
            self.calculate_final_scores()  # will use the accumulated tally
            # Start next omgång automatically: toggle starter, reshuffle and redeal
            self.start_next_omgang()
            return
        else:
            self.new_round()

    def calculate_final_scores(self):
        # Build summary from accumulated omgång_tally
        a = self.omgang_tally["Anna"]
        b = self.omgang_tally["Bo"]
        
        # Calculate bonuses
        a_bonus = (a["intake"] - 20) * 2 if a["intake"] > 20 else 0
        b_bonus = (b["intake"] - 20) * 2 if b["intake"] > 20 else 0
        
        # Add to session cumulative totals
        self.cumulative_scores["Anna"] += a["total"]
        self.cumulative_scores["Bo"] += b["total"]
        
        result_text = "\n".join([
            f"=== SLUTRESULTAT EFTER 6 RONDER ===",
            f"",
            f"Anna:",
            f"  Mullar: {a['mulle_points']}p",
            f"  Tabbe: {a['tabbe']}p",
            f"  Intag: {a['intake']}p",
            f"  Bonus: {a_bonus}p" if a_bonus > 0 else f"  Bonus: 0p",
            f"  ─────────",
            f"  Totalt: {a['total']}p",
            f"",
            f"Bo:",
            f"  Mullar: {b['mulle_points']}p",
            f"  Tabbe: {b['tabbe']}p",
            f"  Intag: {b['intake']}p",
            f"  Bonus: {b_bonus}p" if b_bonus > 0 else f"  Bonus: 0p",
            f"  ─────────",
            f"  Totalt: {b['total']}p",
            f"",
            f"Kumulativt: Anna {self.cumulative_scores['Anna']}p • Bo {self.cumulative_scores['Bo']}p"
        ])
        messagebox.showinfo("Omgång slut", result_text)

    def start_next_omgang(self):
        # Toggle who starts the omgång
        self.starting_player_idx = 1 - self.starting_player_idx
        self.engine.start_omgang(self.engine.current_omgang + 1)
        self.engine.deal_hands()
        self.deck = self.engine.deck
        self.board = self.engine.board
        self.players = self.engine.players
        # Reset round and omgång tally
        self.round_number = 1
        self.omgang_tally = {
            "Anna": {"mulle_points": 0, "intake": 0, "tabbe": 0, "total": 0},
            "Bo":   {"mulle_points": 0, "intake": 0, "tabbe": 0, "total": 0},
        }
        self.current_player_idx = self.starting_player_idx
        self.selected_hand_card = None
        self.action_mode = None
        self.update_display()
        # If Bo starts this omgång, auto-play his first move
        if self.current_player_idx == 1:
            self.root.after(800, self.bo_auto_play)


def main():
    root = tk.Tk()
    app = MulleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
