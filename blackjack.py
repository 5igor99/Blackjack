import tkinter as tk
from tkinter import ttk
from math import ceil

# -------------------------------
# LOGICA DI CONTEGGIO (Hi-Lo)
# -------------------------------
class BlackjackCardCounter:
    def __init__(self, decks=6):
        self.card_values = {
            '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
            '7': 0, '8': 0, '9': 0,
            '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
        }
        self.decks_total = decks
        self.reset()

    def reset(self):
        self.running_count = 0
        self.cards_seen = 0
        self.history = []  # stack per undo

    def set_decks(self, decks: int):
        self.decks_total = max(1, int(decks))
        # non resettiamo automaticamente il conteggio

    def update_count(self, card: str):
        if card in self.card_values:
            self.running_count += self.card_values[card]
            self.cards_seen += 1
            self.history.append(card)

    def undo(self):
        if not self.history:
            return
        last = self.history.pop()
        self.running_count -= self.card_values[last]
        self.cards_seen -= 1

    def decks_remaining(self) -> float:
        # Evita zero: arrotonda a quarti di mazzo per stabilità del true count
        cards_total = self.decks_total * 52
        cards_left = max(0, cards_total - self.cards_seen)
        decks_left = cards_left / 52.0
        # clamp minimo a 0.25 mazzi rimanenti per evitare esplosioni del true count
        return max(0.25, round(decks_left, 2))

    def true_count(self) -> float:
        return round(self.running_count / self.decks_remaining(), 2)

    def get_running_count(self) -> int:
        return self.running_count


# -------------------------------
# INTERFACCIA GRAFICA
# -------------------------------
class BlackjackGUI:
    RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self, root):
        self.root = root
        self.root.title("Conteggio Carte Blackjack — Hi-Lo")

        self.counter = BlackjackCardCounter(decks=6)

        # ---- Controlli superiori ----
        top = ttk.Frame(root, padding=10)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(5, weight=1)

        ttk.Label(top, text="Carta:").grid(row=0, column=0, padx=(0,6))
        self.card_entry = ttk.Combobox(top, width=6, values=self.RANKS, state="readonly")
        self.card_entry.grid(row=0, column=1)
        self.card_entry.set(self.RANKS[0])

        self.add_btn = ttk.Button(top, text="Aggiungi", command=self.add_card)
        self.add_btn.grid(row=0, column=2, padx=6)

        ttk.Label(top, text="Mazzi:").grid(row=0, column=3, padx=(12,6))
        self.decks_spin = tk.Spinbox(top, from_=1, to=12, width=5, command=self.on_decks_change)
        self.decks_spin.delete(0, tk.END)
        self.decks_spin.insert(0, "6")
        self.decks_spin.grid(row=0, column=4)

        self.reset_btn = ttk.Button(top, text="Reset", command=self.reset_count)
        self.reset_btn.grid(row=0, column=6, padx=(12,0))

        self.undo_btn = ttk.Button(top, text="Annulla", command=self.undo_last)
        self.undo_btn.grid(row=0, column=7, padx=(6,0))

        # ---- Pannello conteggi ----
        stats = ttk.Frame(root, padding=(10,0,10,10))
        stats.grid(row=1, column=0, sticky="ew")
        for i in range(4):
            stats.columnconfigure(i, weight=1)

        self.running_label_title = ttk.Label(stats, text="Running Count", font=("", 10))
        self.running_label_title.grid(row=0, column=0, sticky="w")
        self.running_label = tk.Label(stats, text="0", font=("", 16, "bold"))
        self.running_label.grid(row=1, column=0, sticky="w")

        ttk.Label(stats, text="True Count", font=("", 10)).grid(row=0, column=1, sticky="w")
        self.true_label = tk.Label(stats, text="0.00", font=("", 16, "bold"))
        self.true_label.grid(row=1, column=1, sticky="w")

        ttk.Label(stats, text="Carte viste", font=("", 10)).grid(row=0, column=2, sticky="w")
        self.seen_label = tk.Label(stats, text="0", font=("", 16, "bold"))
        self.seen_label.grid(row=1, column=2, sticky="w")

        ttk.Label(stats, text="Mazzi rimanenti (≈)", font=("", 10)).grid(row=0, column=3, sticky="w")
        self.decks_left_label = tk.Label(stats, text=f"{self.counter.decks_remaining():.2f}", font=("", 16, "bold"))
        self.decks_left_label.grid(row=1, column=3, sticky="w")

        # ---- Griglia pulsanti carte ----
        grid = ttk.Frame(root, padding=(10,0,10,10))
        grid.grid(row=2, column=0, sticky="ew")
        cols = 7
        for idx, rank in enumerate(self.RANKS):
            r = idx // cols
            c = idx % cols
            b = ttk.Button(grid, text=rank, width=6, command=lambda rk=rank: self.quick_add(rk))
            b.grid(row=r, column=c, padx=4, pady=4)

        # ---- Bind tastiera ----
        self.root.bind("<Return>", lambda e: self.add_card())
        self.root.bind("<Control-z>", lambda e: self.undo_last())
        self.root.bind("<Control-Z>", lambda e: self.undo_last())
        self.root.bind("<Control-r>", lambda e: self.reset_count())
        self.root.bind("<Control-R>", lambda e: self.reset_count())

        # Aggiorna UI iniziale
        self.update_display()

    # --- Azioni ---
    def on_decks_change(self):
        try:
            decks = int(self.decks_spin.get())
        except ValueError:
            decks = 6
            self.decks_spin.delete(0, tk.END)
            self.decks_spin.insert(0, "6")
        self.counter.set_decks(decks)
        self.update_display()

    def add_card(self):
        card = self.card_entry.get()
        if card in self.counter.card_values:
            self.counter.update_count(card)
            self.update_display()

    def quick_add(self, rank):
        self.card_entry.set(rank)
        self.add_card()

    def undo_last(self):
        self.counter.undo()
        self.update_display()

    def reset_count(self):
        self.counter.reset()
        self.update_display()

    # --- UI helper ---
    def update_display(self):
        rc = self.counter.get_running_count()
        tc = self.counter.true_count()
        decks_left = self.counter.decks_remaining()

        # Colori: verde positivo, rosso negativo, neutro nero
        if rc > 0:
            fg = "#0a7d15"
        elif rc < 0:
            fg = "#b00020"
        else:
            fg = "#000000"

        self.running_label.config(text=str(rc), fg=fg)
        self.true_label.config(text=f"{tc:.2f}", fg=fg)
        self.seen_label.config(text=str(self.counter.cards_seen))
        self.decks_left_label.config(text=f"{decks_left:.2f}")

        # Aggiorna titolo dinamico
        self.running_label_title.config(text=f"Running Count (mazzi: {self.counter.decks_total})")


# -------------------------------
# AVVIO APP
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap(default="")  # opzionale: evita warning su alcune piattaforme
    except Exception:
        pass
    # Tema nativo se disponibile
    try:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app = BlackjackGUI(root)
    root.mainloop()
