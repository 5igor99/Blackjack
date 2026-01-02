🃏 Blackjack Card Counter & Strategy Assistant (Tkinter)
<img width="1098" height="680" alt="combo" src="https://github.com/user-attachments/assets/f3755e77-70db-49c3-97c8-3186c257829e" />

Applicazione desktop in Python + Tkinter che combina:

Conteggio carte Hi-Lo

Strategia base del Blackjack

Deviazioni da strategia basate sul True Count

Interfaccia grafica completa su un’unica schermata

Pensata come assistente didattico e di allenamento per il Blackjack multi-deck.

✨ Funzionalità principali
🔢 Conteggio Carte (Hi-Lo)

Supporto per 1, 2, 6 o 8 mazzi

Calcolo automatico di:

Running Count (RC)

True Count (TC)

Carte viste, rimanenti e totali

Pulsanti rapidi per inserire ogni carta (color-coded):

🟢 Carte positive (2–6)

⚪ Carte neutre (7–9)

🔴 Carte negative (10–A)

Reset immediato del conteggio

♠️ Strategia Base Integrata

Motore di Basic Strategy completo che gestisce:

Mani Hard

Mani Soft

Coppie

Decisioni:
Chiedi Carta · Stai · Raddoppia · Dividi

Le regole sono coerenti con Blackjack standard multi-deck.

📊 Deviazioni con True Count (Hi-Lo)

Include un set di Index Plays tipici (Illustrious 18 + negativi comuni):

Deviazioni automatiche dalla strategia base

Assicurazione consigliata quando TC ≥ +3

Evidenzia chiaramente:

Decisione di Strategia Base

Eventuale Deviazione consigliata

True Count corrente

🖥️ Interfaccia Grafica (Tkinter)

Tutto su una sola schermata

Layout a due colonne:

Sinistra → Conteggio carte

Destra → Strategia e deviazioni

Selezione tramite pulsanti:

Carta del mazziere

Totale del giocatore

Tipo di mano (Hard / Soft / Coppie)

Aggiornamento in tempo reale

🧠 Logica interna
Moduli principali

BlackjackCardCounter
Gestisce conteggio Hi-Lo, RC, TC e mazzi rimanenti

BasicStrategyEngine
Implementa la strategia base (hard, soft, coppie)

INDEX_RULES
Tabelle di deviazione basate sul True Count

BlackjackOneScreen
Interfaccia grafica completa

▶️ Avvio dell’applicazione
Requisiti

Python 3.9+

Tkinter (incluso di default in Python)

Avvio
python blackjack.py


Su Windows, se python non è riconosciuto:

py blackjack.py

🎯 Obiettivo del progetto

Questo progetto NON è pensato per il gioco reale nei casinò, ma come:

Strumento di studio

Allenamento mentale al conteggio

Visualizzazione immediata di strategia e deviazioni

Supporto per comprendere l’impatto del True Count

📌 Possibili estensioni future

Supporto regole specifiche (H17, no DAS, surrender)

Altri sistemi di conteggio

Bet sizing suggerito

Modalità simulazione mano completa

Salvataggio sessioni

⚠️ Disclaimer

Questo software è solo a scopo educativo.
Il gioco d’azzardo comporta rischi finanziari.
