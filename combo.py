import tkinter as tk
from tkinter import ttk

# ===============================
# LOGICA CONTEGGIO (Hi-Lo)
# ===============================
class BlackjackCardCounter:
    CARD_VALUES = {
        '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
        '7': 0, '8': 0, '9': 0,
        '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
    }

    def __init__(self, num_decks=1):
        self.num_decks = max(1, int(num_decks))
        self.running_count = 0
        self.cards_seen = 0

    def set_num_decks(self, num_decks: int):
        self.num_decks = max(1, int(num_decks))

    def total_cards(self) -> int:
        return self.num_decks * 52

    def cards_remaining(self) -> int:
        return max(0, self.total_cards() - self.cards_seen)

    def decks_remaining(self) -> float:
        return self.cards_remaining() / 52.0

    def add_card(self, rank: str):
        if rank in self.CARD_VALUES and self.cards_remaining() > 0:
            self.running_count += self.CARD_VALUES[rank]
            self.cards_seen += 1

    def reset(self):
        self.running_count = 0
        self.cards_seen = 0

    def get_running_count(self) -> int:
        return self.running_count

    def get_true_count(self) -> float:
        # clamp minimo 0.25 mazzi rimanenti per stabilità del TC
        decks_left = max(0.25, self.decks_remaining())
        return self.running_count / decks_left


# ===============================
# STRATEGIA BASE (come il tuo motore)
# ===============================
class BasicStrategyEngine:
    def strategy_decision(self, player_total, dealer_card, is_soft, is_pair=False):
        if is_pair:
            return self.pair_strategy(player_total, dealer_card)
        if is_soft:
            return self.soft_total_strategy(player_total, dealer_card)
        else:
            return self.hard_total_strategy(player_total, dealer_card)

    def pair_strategy(self, pv, d):
        pv = int(pv)
        if pv == 4:   return "Dividi" if d in ['2','3','4','5','6','7'] else "Chiedi Carta"   # 2,2
        if pv == 6:   return "Dividi" if d in ['2','3','4','5','6','7'] else "Chiedi Carta"   # 3,3
        if pv == 8:   return "Dividi" if d in ['5','6'] else "Chiedi Carta"                    # 4,4
        if pv == 10:  return "Raddoppia" if d in ['2','3','4','5','6','7','8','9'] else "Chiedi Carta"  # 5,5
        if pv == 12:  return "Dividi" if d in ['2','3','4','5','6'] else "Chiedi Carta"       # 6,6
        if pv == 14:  return "Dividi" if d in ['2','3','4','5','6','7'] else "Chiedi Carta"   # 7,7
        if pv == 16:  return "Dividi"                                                          # 8,8
        if pv == 18:  return "Dividi" if d in ['2','3','4','5','6','8','9'] else "Stai"       # 9,9
        if pv == 20:  return "Stai"                                                            # 10,10
        if pv == 22:  return "Dividi"                                                          # A,A
        return "Chiedi Carta"

    def soft_total_strategy(self, pv, d):
        if pv in [13,14]: return "Raddoppia" if d in ['5','6'] else "Chiedi Carta"
        if pv in [15,16]: return "Raddoppia" if d in ['4','5','6'] else "Chiedi Carta"
        if pv == 17:      return "Raddoppia" if d in ['3','4','5','6'] else "Chiedi Carta"
        if pv == 18:
            if d in ['3','4','5','6']: return "Raddoppia"
            if d in ['2','7','8']:     return "Stai"
            return "Chiedi Carta"
        if pv in [19,20,21]: return "Stai"
        return "Chiedi Carta"

    def hard_total_strategy(self, pv, d):
        pv = int(pv)
        if pv >= 17: return "Stai"
        if pv <= 8:  return "Chiedi Carta"
        if pv == 9:  return "Raddoppia" if d in ['3','4','5'] else "Chiedi Carta"
        if pv == 10: return "Raddoppia" if d in ['2','3','4','5','6','7','8','9'] else "Chiedi Carta"
        if pv == 11: return "Raddoppia" if d in ['2','3','4','5','6','7','8','9','10'] else "Chiedi Carta"
        if pv == 12: return "Stai"       if d in ['4','5','6'] else "Chiedi Carta"
        if 13 <= pv <= 16:
            return "Stai" if d in ['2','3','4','5','6'] else "Chiedi Carta"
        return "Chiedi Carta"


# ===============================
# INDICI (Hi-Lo) — multi-deck, S17, DAS (valori tipici)
# ===============================
INDEX_RULES = [
    # Insurance (se il mazziere mostra A)
    {'type':'insurance', 'cmp':'>=', 'index': 3, 'action':'Prendi Assicurazione'},

    # Illustrious 18 principali
    {'type':'hard','player':16,'dealer':'10','cmp':'>=', 'index': 0,'action':'Stai'},
    {'type':'hard','player':15,'dealer':'10','cmp':'>=', 'index': 4,'action':'Stai'},
    {'type':'hard','player':10,'dealer':'10','cmp':'>=', 'index': 4,'action':'Raddoppia'},
    {'type':'hard','player':12,'dealer':'3', 'cmp':'>=', 'index': 2,'action':'Stai'},
    {'type':'hard','player':12,'dealer':'2', 'cmp':'>=', 'index': 3,'action':'Stai'},
    {'type':'hard','player':11,'dealer':'A', 'cmp':'>=', 'index': 1,'action':'Raddoppia'},
    {'type':'hard','player':10,'dealer':'A', 'cmp':'>=', 'index': 4,'action':'Raddoppia'},
    {'type':'hard','player':9, 'dealer':'2', 'cmp':'>=', 'index': 1,'action':'Raddoppia'},
    {'type':'hard','player':9, 'dealer':'7', 'cmp':'>=', 'index': 3,'action':'Raddoppia'},

    # Negative comuni (quando il TC è basso si torna a "Chiedi Carta")
    {'type':'hard','player':12,'dealer':'4','cmp':'<',  'index': 0,  'action':'Chiedi Carta'},
    {'type':'hard','player':12,'dealer':'5','cmp':'<=', 'index': -2, 'action':'Chiedi Carta'},
    {'type':'hard','player':12,'dealer':'6','cmp':'<=', 'index': -1, 'action':'Chiedi Carta'},
    {'type':'hard','player':13,'dealer':'2','cmp':'<=', 'index': -1, 'action':'Chiedi Carta'},
    {'type':'hard','player':13,'dealer':'3','cmp':'<=', 'index': -2, 'action':'Chiedi Carta'},

    # Altro frequente
    {'type':'hard','player':16,'dealer':'9','cmp':'>=', 'index': 5,'action':'Stai'},
]


# ===============================
# INTERFACCIA — TUTTO SU UNA SCHERMATA
# ===============================
class BlackjackOneScreen:
    RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack — Conteggio + Strategia (schermata unica)")
        self.root.geometry("1100x650")

        self.counter = BlackjackCardCounter(num_decks=1)
        self.engine = BasicStrategyEngine()

        # Stato per strategia
        self.dealer_card = None
        self.player_total = None
        self.is_soft = False
        self.is_pair = False

        # Layout 2 colonne
        container = ttk.Frame(root, padding=10)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        self.build_left_counting(container)     # Colonna sinistra
        self.build_right_strategy(container)    # Colonna destra

        self.refresh_counts()
        self.update_outputs()

    # ---------- SINISTRA: CONTEGGIO ----------
    def build_left_counting(self, parent):
        left = ttk.LabelFrame(parent, text="Conteggio (Hi-Lo)", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        left.columnconfigure(0, weight=1)

        # RC / TC
        header = ttk.Frame(left)
        header.grid(row=0, column=0, sticky="w", pady=(0,8))
        self.lbl_rc = ttk.Label(header, text="Running Count: 0", font=("", 14, "bold"))
        self.lbl_tc = ttk.Label(header, text="True Count: 0.00", font=("", 14, "bold"))
        self.lbl_rc.grid(row=0, column=0, padx=(0,12))
        self.lbl_tc.grid(row=0, column=1)

        # Stats carte
        stats = ttk.Frame(left)
        stats.grid(row=1, column=0, sticky="w", pady=(0,8))
        self.lbl_seen = ttk.Label(stats, text="Carte viste: 0")
        self.lbl_rem  = ttk.Label(stats, text="Carte rimanenti: 52")
        self.lbl_tot  = ttk.Label(stats, text="Carte totali: 52")
        self.lbl_seen.grid(row=0, column=0, padx=(0,12))
        self.lbl_rem.grid(row=0, column=1, padx=(0,12))
        self.lbl_tot.grid(row=0, column=2, padx=(0,12))

        # Mazzi + Reset
        decks = ttk.Frame(left)
        decks.grid(row=2, column=0, sticky="w", pady=(0,8))
        ttk.Label(decks, text="Mazzi:").pack(side=tk.LEFT, padx=(0,6))
        for n in (1,2,6,8):
            ttk.Button(decks, text=str(n), width=4, command=lambda x=n: self.set_decks(x)).pack(side=tk.LEFT, padx=3)
        ttk.Button(decks, text="Reset", command=self.reset_counter).pack(side=tk.LEFT, padx=(12,0))

        # Combobox + Aggiungi
        entry = ttk.Frame(left)
        entry.grid(row=3, column=0, sticky="w", pady=(0,8))
        ttk.Label(entry, text="Carta:").pack(side=tk.LEFT, padx=(0,6))
        self.card_entry = ttk.Combobox(entry, values=self.RANKS, width=6, state="readonly")
        self.card_entry.set(self.RANKS[0])
        self.card_entry.pack(side=tk.LEFT)
        ttk.Button(entry, text="Aggiungi", command=self.add_from_entry).pack(side=tk.LEFT, padx=8)

        # Pulsanti 13 carte
        grid = ttk.Frame(left)
        grid.grid(row=4, column=0, sticky="w")
        ttk.Label(grid, text="Pulsanti rapidi:").grid(row=0, column=0, columnspan=7, sticky="w", pady=(0,6))
        cols = 7
        for i, r in enumerate(self.RANKS):
            rr = i // cols + 1
            cc = i % cols
            b = tk.Button(grid, text=r, width=6, command=lambda rk=r: self.add_card(rk))
            val = BlackjackCardCounter.CARD_VALUES[r]
            if val > 0:
                b.config(bg="#14833b", fg="white", activebackground="#0f6a2f")
            elif val < 0:
                b.config(bg="#b00020", fg="white", activebackground="#8c001a")
            else:
                b.config(bg="#6e6e6e", fg="white", activebackground="#5a5a5a")
            b.grid(row=rr, column=cc, padx=4, pady=4)

        # Invio = aggiungi da combobox
        self.root.bind("<Return>", lambda e: self.add_from_entry())

    # ---------- DESTRA: STRATEGIA + DEVIAZIONI ----------
    def build_right_strategy(self, parent):
        right = ttk.LabelFrame(parent, text="Strategia + Deviazioni (True Count)", padding=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        right.columnconfigure(0, weight=1)

        # Dealer
        ttk.Label(right, text="Carta del Mazziere:").grid(row=0, column=0, sticky="w")
        self.dealer_buttons = {}
        dealer_cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        dframe = ttk.Frame(right); dframe.grid(row=1, column=0, sticky="w", pady=(2,8))
        for i, c in enumerate(dealer_cards):
            b = tk.Button(dframe, text=c, width=5, command=lambda x=c: self.set_dealer(x))
            b.grid(row=i//8, column=i%8, padx=3, pady=3)
            self.dealer_buttons[c] = b

        # Player totals
        ttk.Label(right, text="Totale del Giocatore:").grid(row=2, column=0, sticky="w")
        self.player_buttons = {}
        player_vals = ['AA','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
        pframe = ttk.Frame(right); pframe.grid(row=3, column=0, sticky="w", pady=(2,8))
        for i, v in enumerate(player_vals):
            b = tk.Button(pframe, text=v, width=5, command=lambda x=v: self.set_player(x))
            b.grid(row=i//8, column=i%8, padx=3, pady=3)
            self.player_buttons[v] = b

        # Tipo mano (toggle)
        tframe = ttk.Frame(right); tframe.grid(row=4, column=0, sticky="w", pady=(4,8))
        ttk.Label(tframe, text="Tipo mano:").pack(side=tk.LEFT, padx=(0,8))
        self.btn_hard = tk.Button(tframe, text="Hard", width=10, command=lambda: self.set_hand_type('hard'))
        self.btn_soft = tk.Button(tframe, text="Soft", width=10, command=lambda: self.set_hand_type('soft'))
        self.btn_pair = tk.Button(tframe, text="Coppie", width=10, command=lambda: self.set_hand_type('pair'))
        self.btn_hard.pack(side=tk.LEFT, padx=4); self.btn_soft.pack(side=tk.LEFT, padx=4); self.btn_pair.pack(side=tk.LEFT, padx=4)

        # Output: Base + Deviazione + Assicurazione
        out = ttk.Frame(right); out.grid(row=5, column=0, sticky="we", pady=(8,6))
        self.lbl_base = ttk.Label(out, text="Base: —", font=("Helvetica", 13))
        self.lbl_dev  = ttk.Label(out, text="Deviazione: —", font=("Helvetica", 14, "bold"))
        self.lbl_ins  = ttk.Label(out, text="Assicurazione: —", font=("Helvetica", 11))
        self.lbl_base.grid(row=0, column=0, sticky="w", pady=(0,2))
        self.lbl_dev.grid(row=1, column=0, sticky="w", pady=(0,2))
        self.lbl_ins.grid(row=2, column=0, sticky="w")

        # Selezione iniziale: Hard
        self.set_hand_type('hard')

    # ---------- AZIONI CONTEGGIO ----------
    def add_from_entry(self):
        self.add_card(self.card_entry.get())

    def add_card(self, rank):
        self.counter.add_card(rank)
        self.refresh_counts()
        self.update_outputs()

    def set_decks(self, n):
        self.counter.set_num_decks(n)
        self.refresh_counts()
        self.update_outputs()

    def reset_counter(self):
        self.counter.reset()
        self.refresh_counts()
        self.update_outputs()

    def refresh_counts(self):
        rc = self.counter.get_running_count()
        tc = self.counter.get_true_count()
        seen = self.counter.cards_seen
        rem = self.counter.cards_remaining()
        tot = self.counter.total_cards()

        self.lbl_rc.config(text=f"Running Count: {rc}")
        self.lbl_tc.config(text=f"True Count: {tc:.2f}")
        self.lbl_seen.config(text=f"Carte viste: {seen}")
        self.lbl_rem.config(text=f"Carte rimanenti: {rem}")
        self.lbl_tot.config(text=f"Carte totali: {tot}")

        # colore RC/TC
        fg = "#14833b" if rc > 0 else ("#b00020" if rc < 0 else "#000000")
        self.lbl_rc.config(foreground=fg)
        self.lbl_tc.config(foreground=fg)

    # ---------- AZIONI STRATEGIA ----------
    def set_dealer(self, card):
        self.dealer_card = card
        for k,b in self.dealer_buttons.items(): b.config(bg='#d3d3d3')
        self.dealer_buttons[card].config(bg='green')
        self.update_outputs()

    def set_player(self, value):
        self.player_total = value
        for k,b in self.player_buttons.items(): b.config(bg='#d3d3d3')
        self.player_buttons[value].config(bg='green')
        self.update_outputs()

    def set_hand_type(self, typ):
        self.is_pair = (typ == 'pair')
        self.is_soft = (typ == 'soft')
        # evidenzia toggle
        self.btn_hard.config(bg='#d3d3d3'); self.btn_soft.config(bg='#d3d3d3'); self.btn_pair.config(bg='#d3d3d3')
        if typ == 'hard': self.btn_hard.config(bg='green')
        if typ == 'soft': self.btn_soft.config(bg='green')
        if typ == 'pair': self.btn_pair.config(bg='green')
        self.update_outputs()

    # ---------- OUTPUT BASE + DEVIAZIONI ----------
    def update_outputs(self):
        # Assicurazione (se A scoperto) — basata solo su TC
        tc = self.counter.get_true_count()
        if self.dealer_card == 'A':
            ins_text = "Assicurazione: Prendi (TC ≥ +3)" if tc >= 3 else "Assicurazione: Non prendere"
        else:
            ins_text = "Assicurazione: —"
        self.lbl_ins.config(text=ins_text)

        if not (self.player_total and self.dealer_card):
            self.lbl_base.config(text="Base: seleziona mano e carta del mazziere")
            self.lbl_dev.config(text="Deviazione: —")
            return

        # converte 'AA' a 22 per gestire la coppia di assi
        pv = int(self.player_total) if self.player_total.isdigit() else 22
        base = self.engine.strategy_decision(pv, self.dealer_card, self.is_soft, self.is_pair)
        self.lbl_base.config(text=f"Base: {base}")

        dev = self.compute_deviation(pv, self.dealer_card, self.is_soft, self.is_pair, tc)
        if dev and dev != base:
            self.lbl_dev.config(text=f"Deviazione: {dev}  (TC={tc:.2f})")
        else:
            self.lbl_dev.config(text=f"Deviazione: Nessuna (TC={tc:.2f})")

    def compute_deviation(self, player_val, dealer, is_soft, is_pair, tc):
        # Insurance (indipendente dal tipo mano)
        if dealer == 'A':
            for rule in INDEX_RULES:
                if rule['type'] == 'insurance' and self._cmp(tc, rule['cmp'], rule['index']):
                    return rule['action']
        # Deviazioni su coppie: (non incluse in questo set; si possono aggiungere)
        if is_pair:
            return None

        # Soft o Hard
        htype = 'soft' if is_soft else 'hard'
        for rule in INDEX_RULES:
            if rule.get('type') != htype:
                continue
            if rule.get('player') == player_val and rule.get('dealer') == dealer:
                if self._cmp(tc, rule['cmp'], rule['index']):
                    return rule['action']
        return None

    @staticmethod
    def _cmp(tc, op, idx):
        if op == '>=': return tc >= idx
        if op == '<=': return tc <= idx
        if op == '<':  return tc <  idx
        if op == '>':  return tc >  idx
        return False


# ===============================
# AVVIO
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackOneScreen(root)
    root.mainloop()
