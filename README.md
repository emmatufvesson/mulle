# Mulle — Kortspelprototyp

En Python-implementation av det svenska kortspelet **Mulle** för två spelare. Spelet använder två blandade standardlekar (104 kort) och innehåller strategiska element som byggen, kombinationsintag och mulles (identiska par).

---

## Snabbstart

### Installation

```bash
# Klona repository
git clone https://github.com/emmatufvesson/mulle.git
cd mulle

# Skapa virtuell miljö (rekommenderat)
python -m venv .venv
source .venv/bin/activate  # På Windows: .venv\Scripts\activate

# Installera beroenden
pip install -r requirements.txt
```

### Kör Spelet

**GUI (Grafiskt gränssnitt)**:
```bash
python -m mulle.gui.game_gui
```

**CLI (Kommandorad)**:
```bash
# Automatisk session (1 omgång = 6 ronder)
python -m mulle.cli.game --rounds 1 --seed 42

# Med enkel interaktiv prompt
python -m mulle.cli.game --rounds 1 --interactive
```

**Headless (Utan UI, för testing)**:
```bash
# Automatiskt spel
python -m mulle.engine.headless_runner --rounds 1 --seed 42

# Med fördefinierat script
python -m mulle.engine.headless_runner --script scripted_moves.json
```

### Kör Tester

```bash
# Alla tester
pytest

# Tyst läge (kort output)
pytest -q

# Specifikt test
pytest tests/test_special_cards.py -v
```

---

## Projektstruktur

```
mulle-1/
├── mulle/                    # Huvudkod
│   ├── models/              # Spelmodeller (Card, Deck, Board, Build, Player)
│   ├── rules/               # Spelets logik (capture, scoring)
│   ├── engine/              # GameEngine och AI
│   ├── gui/                 # Tkinter-baserat GUI
│   └── cli/                 # Kommandoradsgränssnitt
├── tests/                   # Testsvit (pytest)
├── RULEBOOK.md             # Komplett regelbok
├── README.md               # Denna fil
└── requirements.txt        # Python-beroenden
```

---

## Features

### Implementerade Funktioner

#### ✅ Kärnmekanik
- **Capture (Intag)**: Subset-summa algoritm för kombinationsintag
- **Build (Byggen)**: Öppna/låsta byggen med ägarsystem
- **Trotta**: Konsolidera kort av samma värde till låst bygge
- **Discard/Feed**: Automatisk feed till egna byggen
- **Trail-begränsning**: Kan ej släppa kort om du har byggen på bordet
- **Specialvärden**: A=14, SP 2=15, RU 10=16 (endast via byggen)
- **Mulle-detektering**: Exakt 2 identiska kort = mulle
- **Absorption**: Automatisk absorption av single/2-korts högar vid bygge

#### ✅ Regelimplementation
- **Reservationskort**: Krav för att skapa byggen
- **Låsningsregler**: Endast vid merge/absorption/trotta
- **Bygga upp/ner**: Explicit val vid ombyggnad av öppna byggen
- **Specialvärdeskrav**: 14/15/16 måste byggas innan capture
- **Trail-restriktion**: Måste ta in byggen innan man kan släppa kort

#### ✅ Poängräkning
- **Mulle**: Rangvärde per par (A=14, J=11, Q=12, K=13)
- **Tabbe**: 1p per intag från tomt bord
- **Intake**: Specifika kort ger 1-3 poäng (SP A=3p) — används endast för bonusberäkning
- **Bonus**: (intake-20)×2 vid >20 intake-poäng
- **Total**: Mulle + Tabbe + Bonus (OBS: Intake ingår EJ i totalen)

#### ✅ AI och Automation
- **SimpleLearningAI**: Lärande AI med exploration/exploitation
- **Heuristik**: Prioritering av mulles → flest kort → värdematchning
- **GameEngine**: UI-agnostisk spelmotor för batch-körningar
- **Headless Runner**: Scriptbar körning utan UI

#### ✅ Gränssnitt
- **GUI**: Tkinter-baserat med klickbara kort, bygga upp/ner dialog, detaljerad poängpanel
- **CLI**: Interaktiv och automatisk körning via terminal
- **Testsvit**: 20 pytest-tester för regelvalidering

---

## Versionshistorik

### Version 0.4.0 (2025-11-27) — Dokumentation och Engine
**Förändringar**:
- 📖 Komplett omskrivning av RULEBOOK.md (13 sektioner, 300+ rader)
- 📖 Uppdaterad README.md med versionshistorik och setup-instruktioner
- 🏗️ Introducerad GameEngine arkitektur (game_service.py)
- 🤖 Flyttat SimpleLearningAI till separat modul (learning_ai.py)
- 🔧 CLI uppdaterad att använda GameEngine

**Commit**: `bca3bc7` - "refactor: introduce GameEngine and learning_ai"

### Version 0.3.0 (2025-11-20) — Bygga Upp/Ner + Locking Fix
**Nya Features**:
- ⬆️⬇️ Bygga upp eller ner: Explicit val vid ombyggnad av öppna byggen
- 🔓 Reviderad låsningslogik: Endast merge/absorption/trotta (ej storleksbaserad)
- 📊 Detaljerade poängpaneler i GUI: Mullar med kortkoder, breakdown per kategori
- 📈 Uppdaterad intake scoring: SP 3-K, RU/HJ/KL A = 1p; SP 2/A, RU 10 = 2p

**Implementation**:
- `Board.create_build()`: Ny `declared_value` parameter
- `perform_build()`: Stöd för explicit värdedeklaration
- GUI: Dialog för upp/ner-val med beräknade alternativ
- Locking: Borttagen size>2 automatisk låsning

**Commit**: `7482c2d` - "feat: build up/down choice, revised locking, special value capture rules"

**Dokumentation**:
- `IMPLEMENTATION_NOTES.md`: Tekniska detaljer om up/down implementation
- `RULEBOOK.md`: Uppdaterad med nya regler

### Version 0.2.0 (2025-11-18) — Byggregler och Bugfixar
**Bugfixar**:
1. **Trotta på låsta byggen**: 
   - Problem: Kunde inte lägga till kort på eget låst bygge
   - Lösning: Ny `add_trotta_card()` metod i Build-klassen
   - Uppdaterad `perform_trotta()` för att hantera existerande byggen

2. **Discard feed**: 
   - Problem: Discard skapade ny hög istället för att lägga till eget bygge
   - Lösning: `perform_discard()` kontrollerar automatisk feed

3. **Reservationskort**: 
   - Problem: Kunde bygga utan reservationskort, byggen försvann vid rondens slut
   - Lösning: Validering i `can_build()`, `is_card_reserved_for_build()`
   - Förhindrar discard/användning av reserverade kort
   - Varning vid kvarvarande byggen efter rond

**Nya Funktioner**:
- `created_round` parameter i Build-klassen för diagnostik
- Förbättrad felhantering och användarmeddelanden

**Commit**: Se `CHANGELOG_BUGFIXES.md` för detaljer

**Dokumentation**:
- `CHANGELOG_BUGFIXES.md`: Detaljerad beskrivning av fixes

### Version 0.1.0 (Initial) — Grundläggande Prototyp
**Implementerat**:
- Grundläggande spellogik (capture, build, trotta, discard)
- Specialvärden (A, SP 2, RU 10)
- Mulle-detektering (exakt par)
- Enkel poängräkning
- GUI prototype med Tkinter
- CLI med automatisk AI
- Testsvit med pytest

---

## Tekniska Detaljer

### Arkitektur

**Models** (`mulle/models/`):
- `Card`: Immutable dataclass med suit/rank/deck_id, bordvärde vs handvärde
- `Deck`: Två blandade standardlekar (104 kort), shuffling med seed
- `Board`: Hanterar piles (list[Card]) och builds (Build objects)
- `Build`: Ägare, target_value, locked flag, created_round
- `Player`: Hand, captured, mulles, tabbe

**Rules** (`mulle/rules/`):
- `capture.py`: 
  - `generate_capture_combinations()`: Subset-summa för kombinationer
  - `perform_capture()`, `perform_build()`, `perform_trotta()`, `perform_discard()`
  - `detect_mulles()`: Identifiera par med count=2
  - `auto_play_turn()`: Heuristisk prioritering
  - `enumerate_candidate_actions()`: AI action generation
- `scoring.py`:
  - `INTAKE_POINTS_1` och `INTAKE_POINTS_2`: Definitioner
  - `score_round()`: Beräknar ScoreBreakdown för alla spelare

**Engine** (`mulle/engine/`):
- `GameEngine`: UI-agnostisk spelmotor, äger deck/board/players
- `SimpleLearningAI`: Lärande AI med Q-värden per action-kategori
- `headless_runner.py`: Scriptbar körning utan UI

**Interfaces**:
- `gui/game_gui.py`: Tkinter GUI med event-driven interaction
- `cli/game.py`: Terminal CLI med GameEngine wrapper

### Specialvärden och Logik

**Bordvärde vs Handvärde**:
```python
# Card.value_on_board() används för:
- Bygga summan i builds
- Trotta-matchning
- Absorption target

# Card.value_in_hand() används för:
- Capture target (måste matcha)
- Reservationskort validering
```

**A (Ess)**:
- Bord: 1
- Hand: 14
- Krävs bygge för mulle (kan ej ta identiskt ess direkt)

**SP 2 (Spader 2)**:
- Bord: 2
- Hand: 15
- Intake: 2p (special case)

**RU 10 (Ruter 10)**:
- Bord: 10
- Hand: 16
- Intake: 2p (special case)

### Tester

**Testfiler** (totalt 20 tester):
- `test_build.py`: Byggregler, absorption, multi-kort
- `test_capture_locked_build.py`: Låsta byggen immutable
- `test_mulle.py`: Mulle-detektering, poängräkning
- `test_special_cards.py`: Specialvärden (14/15/16) med builds
- `test_trotta.py`: Konsolidering, låsning
- `test_game_engine.py`: GameEngine integration

**Kör tester**:
```bash
pytest -v                    # Verbose output
pytest -q                    # Tyst läge
pytest --cov=mulle          # Coverage report
pytest tests/test_mulle.py  # Specifikt test
```

---

## Kända Begränsningar

### Funktionalitet
- ❌ Ingen save/load av spelstatus
- ❌ GUI capture-väljare visar ej alla kombinationer (väljer första)
- ❌ Ingen replay-funktion
- ❌ Ingen multiplayer över nätverk
- ⚠️ CLI interactive mode är minimal (endast discard)

### Performance
- Subset-summa algoritm är brute-force (OK för små bordstorlekar <20 högar)
- Ingen optimering av absorption backtracking
- GUI refresh kan vara långsam vid många kort

### AI
- SimpleLearningAI använder enkla heuristiska kategorier
- Ingen deep learning eller tree search
- Explorerar endast 15% av tiden
- Lär sig inte mellan sessioner (värden återställs)

---

## Utvecklingsroadmap

### Kort Sikt (Nästa Release)
- [ ] Dev panel i GUI (kort-injektion, build-manipulation, capture-inspector)
- [ ] Förbättrad capture-väljare (välj mellan kombinationer)
- [ ] Full rond/omgång-cykel med automatisk kortdelning
- [ ] Save/Load funktionalitet

### Medellång Sikt
- [ ] Nätverksmultiplayer (client/server arkitektur)
- [ ] Statistik och historik (vinstprocent, genomsnittliga poäng)
- [ ] Replay-funktionalitet med step-by-step
- [ ] Optimerad subset-summa algoritm (dynamic programming)

### Lång Sikt
- [ ] Avancerad AI (Monte Carlo Tree Search eller NN)
- [ ] Turnerings-läge (flera spelare, bracket system)
- [ ] Mobile app (React Native eller Flutter)
- [ ] Online leaderboard

---

## Bidra

Bidrag är välkomna! För större förändringar, öppna först en issue för att diskutera vad du vill ändra.

### Development Setup
```bash
# Fork och klona
git clone https://github.com/<your-username>/mulle.git
cd mulle

# Skapa branch
git checkout -b feature/min-nya-funktion

# Installera dev-beroenden
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Kör tester
pytest

# Formatera kod
black mulle/ tests/

# Commit och push
git commit -m "feat: lägg till min nya funktion"
git push origin feature/min-nya-funktion
```

### Guidelines
- Följ befintlig kodstil (black formatting)
- Lägg till tester för nya features
- Uppdatera RULEBOOK.md om spelregler ändras
- Dokumentera breaking changes i commit messages

---

## Licens

Detta projekt är för utbildningssyfte och personlig utveckling. Kontakta projektägaren för licensfrågor.

---

## Kontakt

**Projektägare**: Emma Tufvesson  
**Repository**: [github.com/emmatufvesson/mulle](https://github.com/emmatufvesson/mulle)

För spelregler, se [RULEBOOK.md](RULEBOOK.md).  
För bugfixes och ändringslogg, se [CHANGELOG_BUGFIXES.md](CHANGELOG_BUGFIXES.md).  
För implementation notes, se [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md).
