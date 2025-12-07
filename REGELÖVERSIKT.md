# Mulle Regelöversikt - Python Implementation

**Status**: ✅ Alla 25 tester passerar - motorn är komplett och verifierad

## Sammanfattning av moduler

### 1. `mulle/rules/capture.py` (431 rader - KÄRNLOGIKEN)

Innehåller all spellogik för spelarhandlingar. Detta är den mest kritiska filen att porta till TypeScript.

#### Huvudfunktioner:

**Hjälpfunktioner:**
- `board_pile_value(pile)` - Beräknar värde för en hög/bygge
- `is_card_reserved_for_build(board, player, card)` - Kollar om kort är reserverat för bygge
- `can_build(board, player, base_pile, added_card)` - Validerar om bygge kan skapas

**Spelåtgärder:**
- `perform_capture(board, player, played_card, chosen)` - Utför intag
- `perform_build(board, player, base_pile, added_card, round_number, declared_value)` - Skapar/utökar bygge
- `perform_discard(board, player, card)` - Släpper kort (eller feed till eget bygge)
- `perform_trotta(board, player, card, round_number)` - Konsoliderar matchande kort till låst bygge

**Kombinationsalgoritmer:**
- `generate_capture_combinations(board, card)` - Genererar alla möjliga kombinationer för intag
  - Specialhantering för värden 14/15/16 (måste tas via bygge)
  - Identiskt kort-prioritering (mulle-scenario)
  - Subset-summa algoritm med backtracking för maximalt antal högar
- `detect_mulles(all_captured, played)` - Detekterar par med exakt 2 identiska kort

**AI-funktioner:**
- `auto_play_turn(board, player, round_number)` - Heuristisk prioritering av drag
- `enumerate_candidate_actions(board, player, round_number)` - Genererar alla möjliga åtgärder för AI

#### Viktiga regeldetaljer:

**Specialvärden (14/15/16):**
- A (Ess) = 14 i hand, 1 på bord
- SP 2 = 15 i hand, 2 på bord  
- RU 10 = 16 i hand, 10 på bord
- **KAN ENDAST** tas in via bygge, inte direkt

**Reservationskort:**
- När du skapar bygge måste du ha ett ANNAT kort i hand med samma värde
- Detta kort är "reserverat" och kan inte användas för andra åtgärder
- Förhindrar att du bygger något du inte kan ta in

**Låsningslogik (REVIDERAD i v0.3.0):**
Byggen låses ENDAST vid:
- Merge med annat bygge av samma värde
- Absorption av externa högar  
- Trotta/feed addition
- INTE längre automatisk låsning vid >2 kort

**Discard/Trail-regler:**
1. **Capture-validering**: Kan ENDAST discard om kortets värde INTE matchar något på bordet:
   - Inget enskilt kort
   - Ingen kombination av kort
   - Inget bygge (eget eller motståndarens)
2. **Trail-restriktion**: Spelare med byggen på bordet KAN INTE släppa kort
   - Måste först ta in sina byggen
   - UNDANTAG: Feed till eget bygge (om värdet matchar)
3. **Auto-feed**: Om discard-värde = eget byggvärde → läggs automatiskt till bygget

⚠️ **OBS**: Python-implementation validerar INTE punkt 1 - detta är en bugg som behöver fixas!

**Build Up/Down (v0.3.0):**
- Vid ombyggnad av öppet bygge måste spelaren deklarera målvärde
- Kan bygga "upp" (högre värde) eller "ner" (lägre värde)
- Parameter `declared_value` i `perform_build()`

**Discard Auto-Feed:**
- Om du släpper kort och har bygge med samma värde
- Läggs kortet automatiskt till bygget (via `build.add_trotta_card()`)
- Även för låsta byggen

**Trotta-logik:**
- Samlar ALLA matchande högar:
  - Singel-kort med exakt värde
  - 2-kort högar/byggen med totalt värde = target
  - Par av singel-kort som summerar till target
- Kräver reservationskort
- Skapar låst bygge

### 2. `mulle/rules/scoring.py` (43 rader)

**Poängsystem:**

```python
INTAKE_POINTS_1 = {
    "SP": ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"],
    "RU": ["A"], 
    "HJ": ["A"], 
    "KL": ["A"]
}  # = 1 poäng

INTAKE_POINTS_2 = {
    "SP": ["2", "A"],
    "RU": ["10"]
}  # = 2 poäng
```

**Poängräkning:**
- `mulle_points` = Summa av alla mulle-värden (A=14, J=11, Q=12, K=13, siffror=nominellt)
- `tabbe` = Antal intag från tomt bord
- `intake` = Summering av intake-poäng (används ENDAST för bonus)
- `bonus` = (intake - 20) × 2 om intake > 20
- **TOTAL = mulle + tabbe + bonus** (intake räknas EJ i totalen!)

### 3. `mulle/rules/validation.py` (53 rader)

**Valideringsfunktioner:**

- `player_has_builds(board, player)` - Kollar om spelare har byggen
- `ensure_can_trail(board, player, card)` - Validerar trail-restriktion
- `InvalidAction` - Exception för ogiltiga drag

**Trail-restriktion:**
- Spelare med byggen kan INTE släppa kort
- Kastas som `InvalidAction` exception

## Subset-Summa Algoritm (Kombinations-intag)

Den mest komplexa delen är kombinationsalgoritmen i `generate_capture_combinations()`:

1. **Direkt matchning**: Hitta alla högar med exakt rätt värde
2. **Subset-generation**: Generera alla kombinationer som summerar till target
3. **Backtracking**: Hitta maximal disjunkt uppsättning (flest högar utan överlapp)
4. **Sortering**: Prioritera större subset först för bättre pruning

Exempel:
- Bord: [3], [4], [5], [2]
- Kort i hand: 7 (handvärde)
- Möjliga kombinationer: [3,4], [5,2], [3,4] + [5,2] är disjunkta
- Välj den med flest högar: båda (4 högar totalt)

## AI Heuristik (auto_play_turn)

Prioriteringsordning:
1. **Kombinations-capture med mulle** (högst värde)
2. **Kombinations-capture utan mulle** (flest kort)
3. **Singel identiskt kort** (mulle)
4. **Singel värdematching**
5. **Build** (om möjligt)
6. **Trotta** (om möjligt)
7. **Discard** (sista utväg)

Metrisk: `(antal_mulles, totalt_antal_kort)` - prioriterar mulles först, sedan kortmängd

## Tester som validerar reglerna

### Kärnfunktionalitet (legacy/tests/tests/):
- `test_build.py` - Bygga, absorption, låsning
- `test_capture_locked_build.py` - Intag av låsta byggen
- `test_mulle.py` - Mulle-detektering och poäng
- `test_trotta.py` - Trotta-logik
- `test_disjoint_capture.py` - Kombinationsintag

### Regelintegritet:
- `test_rule_integrity.py` - Specialvärden, intake-tabeller, mulle-exakthet
- `test_trail_restriction.py` - Trail-restriktion med byggen (7 tester!)

### AI/Engine:
- `test_game_engine.py` - Deterministisk körning
- `test_headless_runner.py` - Script-driven spel
- `test_ai_learning_integrity.py` - AI-lärande
- `test_training_environment.py` - Tränings-miljö

## Portningsstrategi till TypeScript

### Prioritet 1 - Modeller (✅ KLART i src/models/):
- Card, Deck, Hand, Player
- Board, Build (behöver portas)

### Prioritet 2 - Regler (❌ SAKNAS i src/rules/):
**Kritisk komponent** - 431 rader komplex logik:
1. Port `capture.py` → `capture.ts`
   - `generateCaptureCombinations()` - subset-summa algoritm
   - `performCapture()`, `performBuild()`, `performDiscard()`, `performTrotta()`
   - `detectMulles()`, `canBuild()`, `isCardReservedForBuild()`
2. Port `scoring.py` → `scoring.ts`
   - Intake-tabeller
   - `scoreRound()` funktion
3. Port `validation.py` → `validation.ts`
   - `InvalidAction` exception
   - Trail-validering

### Prioritet 3 - Engine (⚠️ PÅBÖRJAD i src/engine/):
- GameEngine finns men behöver kompletteras
- Learning AI kan portas senare

### Prioritet 4 - Tester (❌ SAKNAS):
Skapa Jest-tester som speglar Python-testerna:
- Börja med `test_rule_integrity.ts` - grundläggande regelvalidering
- Sedan `test_capture.ts`, `test_build.ts`, `test_mulle.ts`
- Till sist AI/integration-tester

## Nästa steg

1. **Komplettera models** - Porta Board.py och Build.py till TypeScript
2. **Porta rules-modulen** - Kritiskt! Börja med capture.ts
3. **Skapa Jest-tester** - Parallellt med portering för verifiering
4. **Komplettera GameEngine** - Integration med porterade regler
5. **Frontend** - När engine är verifierad, skapa webb-frontend

## Gemini Mulle Repository

Du nämnde att `gemini_mulle` hade en tidigare frontend - detta kan återanvändas för webb-GUI när TypeScript-motorn är klar. Behöver undersöka separat repo.
