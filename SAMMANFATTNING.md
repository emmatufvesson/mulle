# Mulle Project - Snabb Sammanfattning

## Var är vi nu?

✅ **Python-motorn**: Komplett och verifierad - 25/25 tester passerar  
⚠️ **TypeScript-portering**: ~30% klar (models + minimal engine)  
❌ **Webb-frontend**: Inte påbörjad än

## Vad fattas?

### 1. Models (50% klar)
- ✅ Card, Deck, Hand, Player
- ❌ **Board** - Kritisk!
- ❌ **Build** - Kritisk!

### 2. Rules (0% klar) 🔴 MEST KRITISKT
- ❌ **capture.ts** - 431 rader spellogik (subset-summa, kombinationer, trotta)
- ❌ **scoring.ts** - 43 rader poängräkning
- ❌ **validation.ts** - 53 rader validering

### 3. Tester (0% klar)
- ❌ Jest-tester - Behöver porta 25 Python-tester

### 4. Frontend (0% klar)
- ❌ Webb-GUI
- ❓ Undersök gemini_mulle för återanvändning

## Vad gör varje regel?

### Spelåtgärder (capture.py):

1. **Capture (Intag)** - Ta kort från bordet
   - Subset-summa algoritm för kombinationer
   - Specialhantering: A=14, SP 2=15, RU 10=16 måste tas via bygge
   - Mulle-detektering: Exakt 2 identiska kort = poäng

2. **Build (Bygge)** - Skapa/utöka bygge
   - Kräver reservationskort (annat kort i hand med samma värde)
   - Kan bygga "upp" eller "ner" (declared_value parameter)
   - Låses vid: merge, absorption, trotta (EJ automatiskt vid >2 kort)

3. **Discard (Släng)** - Lägg kort på bordet
   - **Validering**: Kan ENDAST discard om kortets värde INTE matchar:
     - Något enskilt kort på bordet
     - Någon kombination av kort på bordet
     - Något bygge på bordet (eget eller motståndarens)
   - Auto-feed: Om du har bygge med samma värde läggs kortet dit istället
   - Trail-restriktion: KAN EJ släppa om du har byggen på bordet (måste ta in dem först)

4. **Trotta** - Konsolidera matchande kort
   - Samlar ALLA kort/högar med samma värde
   - Skapar låst bygge
   - Kräver reservationskort

### Poängräkning (scoring.py):

- **Mulle**: Rangvärde per par (A=14, J=11, Q=12, K=13, siffror=nominellt)
- **Tabbe**: 1p per intag från tomt bord
- **Intake**: Special-kort ger 1-2p (används för bonus, EJ total)
- **Bonus**: (intake-20)×2 om intake>20
- **TOTAL**: mulle + tabbe + bonus

### Validering (validation.py):

- **Trail-restriktion**: Spelare med byggen kan EJ släppa kort
- **Reservationskort**: Förhindrar att du bygger något du inte kan ta

## Mest komplexa delar

### 1. Subset-Summa Algoritm (generate_capture_combinations)
Hittar alla kombinationer av högar som summerar till rätt värde:
- Direkt matchning (värde = target)
- Subset-generation (kombinationer som summerar till target)
- Backtracking (maximal disjunkt uppsättning utan överlapp)

Exempel:
- Bord: [3], [4], [5], [2]
- Hand: 7
- Resultat: [[3,4]] eller [[5,2]] eller [[3,4], [5,2]] (välj max = båda)

### 2. Mulle-Detektering (detect_mulles)
Räknar identiska kort i capture-grupp:
- Exakt 2 kort = 1 mulle
- 4 kort = 2 mulles
- 6 kort = 3 mulles

### 3. Auto-Play Heuristik (auto_play_turn)
AI prioritering:
1. Kombination med mulle
2. Kombination utan mulle (flest kort)
3. Singel identiskt (mulle)
4. Singel värdematching
5. Build
6. Trotta
7. Discard

## Nästa konkreta steg

### Imorgon (Dag 1):
```bash
# 1. Porta Board + Build
touch src/models/Board.ts
touch src/models/Build.ts
# Kopiera logik från legacy/mulle/models/

# 2. Skapa tester
touch tests/models/Board.test.ts
touch tests/models/Build.test.ts

# 3. Påbörja capture.ts
touch src/rules/capture.ts
# Börja med enkla funktioner: boardPileValue, canBuild
```

### Vecka 1:
- Dag 1-2: Board + Build
- Dag 3-5: capture.ts (kritisk!)
- Dag 6-7: scoring + validation

### Vecka 2:
- Dag 8-10: Jest-tester
- Dag 11-12: GameEngine integration

### Vecka 3:
- Dag 13-17: Webb-frontend

## Viktiga filer att känna till

### Python (referens):
- `legacy/mulle/rules/capture.py` - 431 rader KÄRNLOGIK
- `legacy/mulle/rules/scoring.py` - 43 rader poäng
- `legacy/mulle/models/board.py` - Board-klass
- `legacy/mulle/models/build.py` - Build-klass

### TypeScript (portera till):
- `src/models/Board.ts` - SAKNAS
- `src/models/Build.ts` - SAKNAS
- `src/rules/capture.ts` - SAKNAS
- `src/rules/scoring.ts` - SAKNAS

### Dokumentation:
- `RULEBOOK.md` - Komplett regelbok (300+ rader)
- `REGELÖVERSIKT.md` - Teknisk regelöversikt (ny!)
- `STATUS.md` - Detaljerad status (ny!)

## Frågor att svara på

1. **gemini_mulle**: Var finns detta repo? Kan vi återanvända frontend?
2. **Prioritet**: Mobilapp eller webb först?
3. **Tidram**: Hur snabbt behöver detta vara klart?
4. **Teknologi**: React, Vue, eller annat för frontend?

---

**TL;DR**: Python-motorn är klar och testad. TypeScript-portering är ~30% klar. Kritisk komponent som fattas: **rules-modulen** (capture.ts = 431 rader spellogik). Börja med att porta Board + Build, sedan capture.ts. Estimering: 2-3 veckor för komplett port + frontend.
