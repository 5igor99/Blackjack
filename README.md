🃏 Blackjack Card Counter & Strategy Assistant (Tkinter)
<img width="1098" height="680" alt="combo" src="https://github.com/user-attachments/assets/f3755e77-70db-49c3-97c8-3186c257829e" />

Desktop application in Python + Tkinter combining:

Hi-Lo card counting

Basic Blackjack strategy engine

True count deviations (Illustrious 18 + common negatives)

Designed as an educational and training tool for Blackjack.

✨ Features
🔢 Card Counting (Hi-Lo)

Supports 1, 2, 6, or 8 decks

Automatically tracks:

Running Count (RC)

True Count (TC)

Cards seen, remaining, and total

Quick buttons for each card with color-coded values:

🟢 Positive cards (2–6)

⚪ Neutral cards (7–9)

🔴 Negative cards (10–A)

Reset counter instantly

♠️ Basic Strategy

Handles Hard hands, Soft hands, and Pairs

Decisions include:

Hit · Stand · Double · Split

Rules follow standard multi-deck Blackjack

📊 True Count Deviations

Includes common Index Plays (Illustrious 18 + negatives)

Automatically adjusts advice based on True Count

Highlights:

Base strategy

Deviations

True Count value

Insurance recommendations when TC ≥ +3

🖥️ User Interface (Tkinter)

Single-screen layout with two columns:

Left: Card counting

Right: Strategy & deviations

Interactive buttons for:

Dealer card

Player total

Hand type (Hard / Soft / Pair)

Real-time updates for counts and strategy

🧠 Internal Logic

BlackjackCardCounter: Manages Hi-Lo counting, RC, TC, and remaining decks

BasicStrategyEngine: Implements basic strategy (hard, soft, pairs)

INDEX_RULES: Contains deviation rules

BlackjackOneScreen: Complete GUI

▶️ How to Run
Requirements

Python 3.9+

Tkinter (included with Python)

Run
python blackjack.py


On Windows, if python is not recognized:

py blackjack.py

🎯 Purpose

Educational tool for studying Blackjack strategy

Mental training for card counting

Visualization of base strategy and deviations

Understand the impact of the True Count

📌 Future Extensions

Support for different rules (H17, no DAS, surrender)

Additional counting systems

Suggested bet sizing

Full hand simulation

Session saving

⚠️ Disclaimer

This software is for educational purposes only.
Gambling involves financial risk.
