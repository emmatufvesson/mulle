# Mulle Project Status - Var ska vi ta vid?

**Datum**: 2025-12-07  
**Branch**: `port-engine`  
**Python Engine**: ✅ Komplett och verifierad (25/25 tester passerar)  
**TypeScript Port**: ⚠️ ~30% klar (models + minimal engine)

---

## Nuvarande Status

### ✅ Komplett (Python)

**Engine & Models** (`legacy/mulle/`):
- ✅ Card, Deck, Player, Board, Build - Alla modeller funkar
- ✅ Capture-logik - 431 rader komplex spellogik
- ✅ Scoring - Mulle, tabbe, intake, bonus
- ✅ Validation - Trail-restriktion, reservationskort
- ✅ Game Engine - Headless runner, AI training
- ✅ GUI (Tkinter) - Fungerar men ej webb-baserad
- ✅ CLI - Interaktiv och automatisk körning

**Tester**:
- ✅ 25 pytest-tester - Alla passerar
- ✅ Regelintegritet verifierad
- ✅ AI-lärande testat
- ✅ Trail-restriktion (7 tester)

### ⚠️ Påbörjat (TypeScript)

**Models** (`src/models/`):
- ✅ Card.ts - Komplett med specialvärden
- ✅ Deck.ts - Blandning, shuffle med seed
- ✅ Hand.ts - Grundläggande
- ✅ Player.ts - Grundläggande
- ❌ Board.ts - SAKNAS
- ❌ Build.ts - SAKNAS

**Engine** (`src/engine/`):
- ⚠️ GameEngine.ts - Påbörjad men ofullständig (saknar rules-integration)

**Rules** (`src/rules/`):
- ❌ capture.ts - SAKNAS HELT
- ❌ scoring.ts - SAKNAS HELT
- ❌ validation.ts - SAKNAS HELT

**Tester**:
- ❌ Inga Jest-tester än (--passWithNoTests)

### ❌ Ej påbörjat

- ❌ Webb-frontend (React/Vue/etc)
- ❌ Integration med gemini_mulle frontend
- ❌ API/Server-layer
- ❌ Multiplayer

---

## Kritisk Path - Vad behöver göras?

### Fas 1: Komplettera TypeScript Models (1-2 dagar)

**Board.ts** - Kritisk komponent
```typescript
class Board {
  piles: Pile[]  // Array of Card[] or Build
  
  addCard(card: Card): void
  removePile(pile: Pile): void
  listBuilds(): Build[]
  listBuildsByValue(value: number): Build[]
  createBuild(basePile: Pile, addedCard: Card, owner: string, ...): Build
}
```

**Build.ts** - Bygge-logik
```typescript
class Build {
  cards: Card[]
  owner: string
  value: number
  locked: boolean
  createdRound: number
  
  addTrottaCard(card: Card): void  // För feed/trotta till låsta byggen
}
```

**Pile.ts** - Type definition
```typescript
type Pile = Card[] | Build
```

### Fas 2: Porta Rules-modulen (3-5 dagar) 🔴 MEST KRITISKT

**capture.ts** - 431 rader komplex logik:

Funktioner att porta:
1. `boardPileValue(pile: Pile): number`
2. `isCardReservedForBuild(board, player, card): Build | null`
3. `canBuild(board, player, basePile, addedCard): boolean`
4. `generateCaptureCombinations(board, card): Pile[][]` ⚠️ KOMPLEX
   - Subset-summa algoritm
   - Backtracking för maximal disjunkt uppsättning
   - Specialhantering för 14/15/16
5. `detectMulles(allCaptured, played): Card[][]`
6. `performCapture(board, player, playedCard, chosen): ActionResult`
7. `performBuild(board, player, basePile, addedCard, roundNumber, declaredValue): ActionResult`
8. `performDiscard(board, player, card): ActionResult`
9. `performTrotta(board, player, card, roundNumber): ActionResult`
10. `autoPlayTurn(board, player, roundNumber): ActionResult` - AI heuristik
11. `enumerateCandidateActions(board, player, roundNumber): CandidateAction[]`

**scoring.ts** - 43 rader, enklare:
```typescript
const INTAKE_POINTS_1 = { ... }
const INTAKE_POINTS_2 = { ... }

function intakePoints(player: Player): number
function scoreRound(players: Player[]): ScoreBreakdown[]
```

**validation.ts** - 53 rader, enkel:
```typescript
class InvalidAction extends Error { }

function playerHasBuilds(board, player): boolean
function ensureCanTrail(board, player, card?): void
```

### Fas 3: Skapa Jest-Tester (2-3 dagar)

Portera Python-tester till TypeScript:

**Prioritet 1 - Regelintegritet**:
- `test_rule_integrity.test.ts` - Specialvärden, intake-tabeller
- `test_capture.test.ts` - Kombinationsintag
- `test_build.test.ts` - Bygga, absorption, låsning
- `test_mulle.test.ts` - Mulle-detektering

**Prioritet 2 - Avancerade regler**:
- `test_trail_restriction.test.ts` - Trail-restriktion (7 tester)
- `test_trotta.test.ts` - Trotta-logik
- `test_disjoint_capture.test.ts` - Maximal disjunkt uppsättning

**Prioritet 3 - Integration**:
- `test_game_engine.test.ts` - Deterministisk körning
- `test_ai.test.ts` - AI-lärande

### Fas 4: Komplettera GameEngine (1-2 dagar)

Integrera rules-modulen:
```typescript
class GameEngine {
  board: Board
  players: Player[]
  deck: Deck
  
  playTurn(player: Player, action: Action): ActionResult
  scoreRound(): ScoreBreakdown[]
  // ... integration med capture/build/discard/trotta
}
```

### Fas 5: Webb-Frontend (3-5 dagar)

**Alternativ 1**: Porta gemini_mulle frontend
- Undersök gemini_mulle repo (separat)
- Anpassa till ny TypeScript engine

**Alternativ 2**: Ny React-frontend
- Använd Tkinter GUI som referens
- Implementera klickbara kort
- Build up/down dialog
- Poängpanel

---

## Estimerad Tidsplan

| Fas | Uppgift | Tid | Status |
|-----|---------|-----|--------|
| 1 | Board.ts + Build.ts | 1-2 dagar | ❌ Ej påbörjad |
| 2 | capture.ts (kritisk) | 3-4 dagar | ❌ Ej påbörjad |
| 2 | scoring.ts + validation.ts | 1 dag | ❌ Ej påbörjad |
| 3 | Jest-tester (grundläggande) | 2-3 dagar | ❌ Ej påbörjad |
| 4 | GameEngine integration | 1-2 dagar | ⚠️ Påbörjad |
| 5 | Webb-frontend | 3-5 dagar | ❌ Ej påbörjad |

**Total**: ~11-17 dagar (2-3 veckor fulltid)

---

## Rekommenderad Arbetsordning

### Vecka 1: Core Rules (Kritisk)

**Dag 1-2**: Board.ts + Build.ts
- Porta Python-klasser direkt
- Lägg till TypeScript types
- Skapa grundläggande tester

**Dag 3-5**: capture.ts
- Börja med enkla funktioner (boardPileValue, canBuild)
- Implementera subset-summa algoritm
- Testa varje funktion incrementellt

**Dag 6-7**: scoring.ts + validation.ts
- Enkla portningar
- Skapa tester för poängräkning

### Vecka 2: Integration & Testing

**Dag 8-10**: Jest-tester
- Port Python-tester till TypeScript
- Kör alla tester parallellt
- Fixa buggar

**Dag 11-12**: GameEngine
- Integrera rules-modulen
- Implementera turn-hantering
- Deterministisk körning med seed

### Vecka 3: Frontend

**Dag 13**: Undersök gemini_mulle
- Klona repo
- Utvärdera återanvändbarhet

**Dag 14-17**: Implementera frontend
- Antingen porta gemini_mulle
- Eller skapa ny React-frontend

---

## Gemini Mulle - Frontend Återanvändning

Du nämnde att `gemini_mulle` hade en tidigare mobilapp-frontend som skrotats. För att utvärdera:

**Behöver undersöka**:
1. Var finns gemini_mulle repo? (GitHub/lokal?)
2. Vilken teknologi? (React Native, Flutter, Ionic?)
3. Kan komponenter återanvändas för webb?

**Fördelar med återanvändning**:
- Redan designad UI/UX
- Sparar tid på frontend-utveckling
- Möjlig mobil-support

**Nackdelar**:
- Kan vara utdaterat
- Möjligt tekniskt skuld
- Anpassning till ny engine

---

## Nästa Konkreta Steg (Imorgon)

### Steg 1: Board.ts + Build.ts (2-3 timmar)
```bash
# Skapa filer
touch src/models/Board.ts
touch src/models/Build.ts

# Porta från Python
# legacy/mulle/models/board.py → src/models/Board.ts
# legacy/mulle/models/build.py → src/models/Build.ts
```

### Steg 2: Grundläggande Board-tester (1 timme)
```bash
touch tests/models/Board.test.ts
touch tests/models/Build.test.ts

# Testa:
# - Board.addCard()
# - Board.removePile()
# - Build.addTrottaCard()
```

### Steg 3: Påbörja capture.ts (2-3 timmar)
```bash
touch src/rules/capture.ts

# Implementera enkla funktioner först:
# - boardPileValue()
# - canBuild()
# - isCardReservedForBuild()
```

### Steg 4: Test-driven development (resten av dagen)
```bash
touch tests/rules/capture.test.ts

# Skriv tester FÖRST för varje funktion
# Implementera sedan funktionen tills testen passerar
```

---

## Frågor att besvara

1. **Finns gemini_mulle tillgängligt?** Var är repot?
2. **Prioritet**: Mobilapp eller webb först?
3. **Teknologi**: React, Vue, eller något annat för frontend?
4. **Tidram**: Hur snabbt behöver detta vara klart?
5. **Hjälp**: Jobbar du solo eller finns team?

---

## Kända Buggar i Python-Implementation

⚠️ **Discard-validering saknas**: `perform_discard()` validerar INTE att capture är omöjlig innan discard tillåts. Enligt korrekt regel ska discard endast vara tillåtet när kortets värde INTE matchar något kort, kombination, eller bygge på bordet.

**Fix krävs**:
```python
def perform_discard(board: Board, player: Player, card: Card) -> ActionResult:
    # 1. Check reservation
    # 2. Check auto-feed to own build
    # 3. Check trail-restriction (has builds)
    # 4. NEW: Validate that no capture is possible
    combos = generate_capture_combinations(board, card)
    if combos and len(combos[0]) > 0:
        raise InvalidAction(f"Cannot discard {card.code()} - capture is possible!")
    # 5. Allow discard
```

## Sammanfattning

**Python-motorn**: ⚠️ Komplett och testad men har bugg i discard-validering  
**TypeScript-portering**: ⚠️ 30% klar - **kritisk komponent är rules-modulen**  
**Nästa steg**: Porta Board/Build → Porta capture.ts (med korrekt discard-validering!) → Tester → Engine  
**Estimering**: 2-3 veckor för komplett port + webb-frontend

**Den mest kritiska filen att porta är `capture.py` (431 rader) - där ligger ALL spellogik!**
