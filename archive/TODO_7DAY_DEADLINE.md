# 7-Dagars Deadline Plan - Mulle TypeScript Port

**Deadline**: 2025-12-14 (7 dagar kvar)
**Mål**: Fungerande webb-app där man spelar mot AI

---

## Status (Efter 2 timmar arbete)

✅ **Klart**:
- [x] Discard-bugg fixad i Python
- [x] Card.ts - Komplett med specialvärden
- [x] Build.ts - Porterad från Python  
- [x] Board.ts - Porterad med absorption/merge-logik
- [x] Deck.ts - Två kortlekar, seeded shuffle
- [x] Player.ts - Hand, captured, mulles, tabbe

❌ **Återstår** (Kritisk path):
- [ ] **rules/capture.ts** (431 rader) - MEST KRITISKT! 3-4 dagar
- [ ] rules/scoring.ts + validation.ts - 1 dag
- [ ] Jest-tester - 2 dagar (parallellt med rules)
- [ ] GameEngine integration - 1 dag
- [ ] React frontend - 2 dagar

---

## Reviderad 7-dagars plan

### Dag 1 (Idag - onsdag): Rules portering START
**Mål**: Påbörja capture.ts med grundfunktioner

**Morgon** (4h):
- [x] Board + Build + Card fix (KLART!)
- [ ] Skapa src/rules/capture.ts
- [ ] Porta hjälpfunktioner:
  - `boardPileValue()`
  - `isCardReservedForBuild()`  
  - `canBuild()`

**Eftermiddag** (4h):
- [ ] Börja på subset-summa algoritm
- [ ] `generateCaptureCombinations()` - Basfunktionalitet
- [ ] Grundläggande tester för hjälpfunktioner

---

### Dag 2 (torsdag): Capture-algoritmer
**Mål**: Komplettera capture.ts algoritmer

**Hel dag** (8h):
- [ ] Komplettera `generateCaptureCombinations()`
  - Subset-generation
  - Backtracking för maximal disjunkt
  - Specialvärden 14/15/16
- [ ] `detectMulles()`
- [ ] Tester för kombinationsalgoritmer

---

### Dag 3 (fredag): Perform-funktioner
**Mål**: Alla spelåtgärder implementerade

**Hel dag** (8h):
- [ ] `performCapture()`
- [ ] `performBuild()`
- [ ] `performDiscard()` med korrekt validering
- [ ] `performTrotta()`
- [ ] Tester för alla perform-funktioner

---

### Dag 4 (lördag): AI + Scoring + Validation
**Mål**: Komplettera rules-modulen

**Morgon** (4h):
- [ ] `autoPlayTurn()`
- [ ] `enumerateCandidateActions()`
- [ ] AI-tester

**Eftermiddag** (4h):
- [ ] scoring.ts komplett
- [ ] validation.ts komplett
- [ ] Tester för scoring/validation
- [ ] **MILESTONE**: Hela rules-modulen klar!

---

### Dag 5 (söndag): GameEngine + Integration
**Mål**: Fungerande game engine med AI

**Hel dag** (8h):
- [ ] GameEngine integration med rules
- [ ] `playTurn()` implementation
- [ ] `scoreRound()` integration
- [ ] AI-spel fungerande
- [ ] Integration-tester
- [ ] **MILESTONE**: Headless game fungerande!

---

### Dag 6 (måndag): Frontend START
**Mål**: Grundläggande React-app

**Morgon** (4h):
- [ ] Kolla gemini_mulle för återanvändbara komponenter
- [ ] Sätt upp React-app (create-react-app)
- [ ] Grundläggande layout: Board + Hand + Score

**Eftermiddag** (4h):
- [ ] GameBoard komponent - Visa kort och byggen
- [ ] PlayerHand komponent - Klickbara kort
- [ ] Integration med GameEngine

---

### Dag 7 (tisdag): Frontend FINISH + Polish
**Mål**: Färdig spelbar app

**Morgon** (4h):
- [ ] Build up/down dialog
- [ ] ScorePanel med mulle-breakdown
- [ ] AI drag-animationer/delay
- [ ] Tur-indikator

**Eftermiddag** (4h):
- [ ] Bugfixar
- [ ] UI-polish
- [ ] Deploy till GitHub Pages / Vercel
- [ ] **MILESTONE**: KLAR APP!

---

## Risk-hantering

### Om vi hamnar efter:

**Dag 3-4**: Skippa AI-funktioner (`autoPlayTurn`, `enumerateCandidateActions`)
- Använd enkel random AI istället
- Fokusera på manuel spelbarhet

**Dag 5**: Minimal GameEngine
- Bara basic turn-hantering
- Skippa avancerade features

**Dag 6-7**: Minimal frontend
- Ingen fancy UI
- Text-baserat interface
- Fokusera på spelbarhet

### Kritisk path:
1. **capture.ts** (dag 1-3) - KAN EJ SKIPPAS
2. **scoring.ts + validation.ts** (dag 4) - KAN EJ SKIPPAS  
3. **GameEngine** (dag 5) - KAN FÖRENKLAS
4. **Frontend** (dag 6-7) - KAN FÖRENKLAS

---

## Nästa 4 timmar (Resten av idag)

### ✅ KLART (2h):
- Discard-bugg fixad
- Board + Build + Card porterade

### 🔄 NU (2h):
1. **Skapa rules-struktur** (15 min)
   ```bash
   mkdir -p src/rules
   touch src/rules/capture.ts
   touch src/rules/types.ts
   touch src/rules/index.ts
   ```

2. **Porta hjälpfunktioner** (1h 45min)
   - `boardPileValue()`
   - `isCardReservedForBuild()`
   - `canBuild()`
   - Skapa ActionResult, CandidateAction types

3. **Skapa basic tester** (30 min)
   ```bash
   mkdir -p tests/rules
   touch tests/rules/capture.test.ts
   ```

4. **Test basic funktioner** (30 min)

---

## Dagliga mål sammanfattat:

| Dag | Huvudmål | Timmar | Kritiskt? |
|-----|----------|--------|-----------|
| 1 (ons) | Rules start + hjälpfunktioner | 4h | ✅ JA |
| 2 (tor) | Capture-algoritmer | 8h | ✅ JA |
| 3 (fre) | Perform-funktioner | 8h | ✅ JA |
| 4 (lör) | AI + Scoring + Validation | 8h | ✅ JA |
| 5 (sön) | GameEngine + Integration | 8h | ⚠️ Kan förenklas |
| 6 (mån) | Frontend start | 8h | ⚠️ Kan förenklas |
| 7 (tis) | Frontend finish + deploy | 8h | ⚠️ Kan förenklas |

**Total tid**: ~50 timmar över 7 dagar = ~7h/dag i snitt

---

## Framgångskriterier

**Minimum Viable Product (MVP)**:
- ✅ Spelregler korrekt implementerade
- ✅ AI motståndare (även om enkel)
- ✅ Grundläggande UI (kan vara minimalistisk)
- ✅ Poängräkning fungerande
- ✅ Mulle-detektering korrekt

**Nice-to-have (om tid finns)**:
- Självlärande AI
- Snygg UI med animationer
- Build up/down dialog
- Detaljerad poängpanel
- Deploy till publik URL

---

**FOKUS**: Capture.ts är den mest kritiska komponenten. Allt annat kan förenklas, men spelreglerna måste vara korrekta!
