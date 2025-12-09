# Mulle TODO - Nästa Steg

## Omedelbart (Idag/Imorgon)

### 1. Fixa discard-bugg i Python (30 min)
```bash
# Fixa legacy/mulle/mulle/rules/capture.py
# Lägg till capture-validering i perform_discard()
```

**Kod att lägga till** (rad ~224 i capture.py):
```python
# Before trail-restriction check, add:
# Validate that no capture is possible
if not player_builds:  # Only check if NOT feeding to own build
    combos = generate_capture_combinations(board, card)
    if combos and len(combos[0]) > 0:
        raise InvalidAction(f"Cannot discard {card.code()} - capture is possible!")
```

**Test**: Kör `pytest legacy/tests/tests/test_trail_restriction.py -v`

---

### 2. Porta Board.ts + Build.ts (2-3 timmar)

**Board.ts** - Skapa från `legacy/mulle/mulle/models/board.py`:
- `piles: Pile[]` (Card[] | Build)
- `addCard(card: Card): void`
- `removePile(pile: Pile): void`
- `listBuilds(): Build[]`
- `listBuildsByValue(value: number): Build[]`
- `createBuild(...): Build`

**Build.ts** - Skapa från `legacy/mulle/mulle/models/build.py`:
- `cards: Card[]`
- `owner: string`
- `value: number`
- `locked: boolean`
- `createdRound: number`
- `addTrottaCard(card: Card): void`

**Filer att skapa**:
```bash
touch src/models/Board.ts
touch src/models/Build.ts
touch src/models/types.ts  # För Pile type
```

---

### 3. Skapa grundläggande tester (1 timme)

```bash
mkdir -p tests/models
touch tests/models/Board.test.ts
touch tests/models/Build.test.ts
```

**Testa**:
- Board.addCard() / removePile()
- Build.addTrottaCard()
- Build locking logic

---

## Denna vecka (Prioritet 1)

### 4. Porta rules/capture.ts (3-4 dagar) 🔴 KRITISK

**Steg-för-steg portering**:

**Dag 1**: Hjälpfunktioner
- `boardPileValue(pile: Pile): number`
- `isCardReservedForBuild(...): Build | null`
- `canBuild(...): boolean`

**Dag 2**: Capture-algoritmer
- `generateCaptureCombinations(board, card): Pile[][]`
  - Subset-summa med backtracking
  - Specialvärden 14/15/16
- `detectMulles(captured, played): Card[][]`

**Dag 3**: Perform-funktioner
- `performCapture(...): ActionResult`
- `performBuild(...): ActionResult`
- `performDiscard(...): ActionResult` ⚠️ Med korrekt validering!
- `performTrotta(...): ActionResult`

**Dag 4**: AI-funktioner
- `autoPlayTurn(...): ActionResult`
- `enumerateCandidateActions(...): CandidateAction[]`

**Filer**:
```bash
mkdir -p src/rules
touch src/rules/capture.ts
touch src/rules/types.ts  # ActionResult, CandidateAction
```

---

### 5. Porta rules/scoring.ts + validation.ts (1 dag)

**scoring.ts** (enkel):
```typescript
const INTAKE_POINTS_1 = { ... }
const INTAKE_POINTS_2 = { ... }

function intakePoints(player: Player): number
function scoreRound(players: Player[]): ScoreBreakdown[]
```

**validation.ts** (enkel):
```typescript
class InvalidAction extends Error { }
function playerHasBuilds(board, player): boolean
function ensureCanTrail(board, player, card?): void
```

---

### 6. Skapa Jest-tester för rules (2-3 dagar)

**Prioritet 1** - Regelintegritet:
```bash
touch tests/rules/capture.test.ts
touch tests/rules/scoring.test.ts
touch tests/rules/validation.test.ts
```

**Testa**:
- Subset-summa algoritm
- Specialvärden (14/15/16)
- Mulle-detektering
- Discard-validering ⚠️ Ny regel!
- Trail-restriktion
- Poängräkning

**Prioritet 2** - Avancerade:
```bash
touch tests/rules/trotta.test.ts
touch tests/rules/build.test.ts
```

---

## Nästa vecka (Prioritet 2)

### 7. Komplettera GameEngine (1-2 dagar)

**Integration**:
- Import rules från capture, scoring, validation
- `playTurn(player, action): ActionResult`
- `scoreRound(): ScoreBreakdown[]`
- Deterministisk körning med seed

**Test**:
```bash
touch tests/engine/GameEngine.test.ts
```

---

### 8. Undersök gemini_mulle frontend (½ dag)

**Frågor att besvara**:
1. Var finns repot? (GitHub URL?)
2. Vilken teknologi? (React Native, Flutter, Ionic?)
3. Kan komponenter återanvändas för webb?
4. Hur mycket arbete krävs för anpassning?

**TODO**:
```bash
# Om gemini_mulle finns:
# - Klona repo
# - Granska kod-struktur
# - Identifiera återanvändbara komponenter
# - Utvärdera portningsarbete
```

---

### 9. Webb-Frontend (3-5 dagar)

**Alternativ A**: Porta gemini_mulle
- Anpassa till TypeScript engine
- Uppdatera API-anrop
- Testa integration

**Alternativ B**: Ny React-frontend från scratch
```bash
# Skapa frontend-app
npx create-react-app client --template typescript
cd client

# Komponenter att skapa:
# - GameBoard.tsx - Visa bord med kort och byggen
# - PlayerHand.tsx - Visa spelarens hand
# - ScorePanel.tsx - Visa poäng (mulle, tabbe, bonus)
# - ActionDialog.tsx - Build up/down val
# - GameController.tsx - Hantera spellogik
```

**UI-features från Tkinter GUI**:
- Klickbara kort
- Visa byggen med ägare och värde
- Build up/down dialog
- Detaljerad poängpanel med mulle-breakdown
- Tur-indikator

---

## Framtida Förbättringar (Backlog)

### 10. Multiplayer (Senare)
- WebSocket server för realtid
- Lobby-system
- Matchmaking

### 11. AI Förbättringar (Senare)
- Monte Carlo Tree Search
- Neural Network-baserad AI
- Träning mot olika strategier

### 12. Mobil-app (Senare)
- React Native eller Flutter
- Touch-optimerad UI
- Offline-läge

---

## Checklista - Var är vi nu?

- [x] Python-motor komplett och testad
- [x] TypeScript models: Card, Deck, Hand, Player
- [x] Dokumentation: RULEBOOK, REGELÖVERSIKT, STATUS
- [x] **Fixa discard-bugg i Python** ✅ KLAR ⬅️ NÄSTA
- [ ] **Porta Board.ts + Build.ts** ⬅️ NÄSTA
- [ ] Porta rules/capture.ts (KRITISK)
- [ ] Porta rules/scoring.ts + validation.ts
- [ ] Jest-tester för rules
- [ ] Komplettera GameEngine
- [ ] Undersök gemini_mulle
- [ ] Webb-frontend

---

## Estimerad Tid Kvar

| Uppgift | Tid | När |
|---------|-----|-----|
| Fixa discard-bugg | 30 min | Idag |
| Board + Build | 2-3 tim | Idag/Imorgon |
| capture.ts | 3-4 dagar | Denna vecka |
| scoring + validation | 1 dag | Denna vecka |
| Jest-tester | 2-3 dagar | Denna vecka |
| GameEngine | 1-2 dagar | Nästa vecka |
| Frontend research | ½ dag | Nästa vecka |
| Frontend impl | 3-5 dagar | Nästa vecka |
| **TOTAL** | **~12-17 dagar** | **2-3 veckor** |

---

## Nästa 3 Konkreta Steg

### Steg 1: Fixa discard-bugg (30 min)
```bash
# Editera legacy/mulle/mulle/rules/capture.py
# Lägg till capture-validering i perform_discard()
pytest legacy/tests/tests/test_trail_restriction.py -v
```

### Steg 2: Porta Board.ts (1-2 tim)
```bash
touch src/models/Board.ts
touch src/models/types.ts
# Implementera från legacy/mulle/mulle/models/board.py
```

### Steg 3: Porta Build.ts (1 tim)
```bash
touch src/models/Build.ts
# Implementera från legacy/mulle/mulle/models/build.py
touch tests/models/Build.test.ts
npm test
```

---

## Frågor att besvara

1. **gemini_mulle**: Exakt var finns detta repo? GitHub URL eller lokal path?
2. **Prioritet**: Vill du ha webb-version eller mobilapp först?
3. **Teknologi för frontend**: React, Vue, Svelte, eller annat?
4. **Tidram**: Finns det en deadline eller är detta hobby-projekt?
5. **Multiplayer**: Är detta en must-have eller nice-to-have?

