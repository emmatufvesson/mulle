# Bugfixar - Byggregler och Rundhantering

## Datum: 2025-11-18

### Problem som lösts:

#### 1. Trötta på låsta byggen
**Problem**: Man kunde inte lägga till ett kort (trötta) på sitt eget låsta bygge.

**Lösning**: 
- Lagt till `add_trotta_card()` metod i `Build` klassen som tillåter att lägga till kort även på låsta byggen
- Uppdaterat `perform_trotta()` för att först kontrollera om spelaren har ett existerande bygge med samma värde
- Om bygget finns, läggs kortet till via `add_trotta_card()` även om bygget är låst

**Filer ändrade**:
- `mulle/models/build.py`: Ny metod `add_trotta_card()`
- `mulle/rules/capture.py`: 
  - Uppdaterad `perform_trotta()` logik
  - Lagt till kontroll för reservationskort när nytt trotta-bygge skapas
  - Trottade byggen är alltid låsta och kan inte byggas om

**Viktiga regler**:
- För att trötta ett kort på bordet måste du ha minst 2 kort av samma värde (ett för att trötta, ett som reservationskort)
- Trottade byggen är låsta och kan inte byggas om av motståndaren
- Motståndaren kan endast ta in ett trottat bygge med exakt rätt värde

#### 2. Discard lägger till på eget bygge
**Problem**: När man släppte ett kort till bordet och hade ett bygge med samma värde, lades kortet inte till bygget utan skapade en ny hög.

**Lösning**:
- Uppdaterat `perform_discard()` för att kontrollera om spelaren har ett bygge med samma värde som kortet som släpps
- Om sådant bygge finns, läggs kortet automatiskt till bygget via `add_trotta_card()`
- Detta fungerar även på låsta byggen

**Filer ändrade**:
- `mulle/rules/capture.py`: Uppdaterad `perform_discard()`

#### 3. Byggen och reservationskort
**Regel**: När man skapar ett bygge måste man ha ett reservationskort på handen (ett kort som kan ta in bygget med sitt handvärde). Detta kort får inte användas till något annat, och bygget MÅSTE tas in aktivt under samma rond. Byggen samlas INTE in automatiskt.

**Lösning**:
- `can_build()` kontrollerar att spelaren har ett reservationskort innan bygget skapas
- Lagt till `is_card_reserved_for_build()` som kontrollerar om ett kort är det enda kortet som kan ta in ett bygge
- `can_build()` förhindrar nu användning av reserverade kort för att bygga nya byggen
- `perform_discard()` förhindrar att slänga ett reserverat kort (ger felmeddelande)
- `perform_trotta()` förhindrar användning av reserverade kort (om inte trottan är för det bygget kortet är reserverat för)
- Lagt till `created_round` parameter i `Build` klassen för diagnostik
- Vid rondens slut visas en varning om byggen finns kvar (detta indikerar felaktig spelning eller AI-bug)

**Filer ändrade**:
- `mulle/models/build.py`: Lagt till `created_round` parameter för diagnostik
- `mulle/models/board.py`: Uppdaterad `create_build()` för att spara `created_round`
- `mulle/rules/capture.py`: 
  - Ny funktion `is_card_reserved_for_build()` för att identifiera reserverade kort
  - `can_build()` kontrollerar reservationskort och förhindrar användning av reserverade kort
  - `perform_discard()` förhindrar discard av reserverade kort
  - `perform_trotta()` förhindrar användning av reserverade kort (med undantag)
  - Uppdaterade `perform_build()`, `perform_trotta()`, `auto_play_turn()`, `enumerate_candidate_actions()` för att skicka `round_number`
- `mulle/gui/game_gui.py`:
  - Uppdaterade `execute_build()`, `execute_action()`, `auto_play()`, `bo_auto_play()` för att skicka `round_number`
  - `end_round()` varnar om byggen finns kvar (ska inte hända vid korrekt spel)
- `mulle/cli/game.py`:
  - Uppdaterade `interactive_turn()`, `ai_turn()`, `SimpleLearningAI.select_action()`, `play_round()` för `round_number`
  - `play_round()` varnar om byggen finns kvar

### Testning:

För att testa ändringarna:

1. **Testa trötta på låst bygge**:
   - Bygg ett 12-bygge med en dam (kräver att du har minst 2 damer på hand)
   - Bygget låses
   - Försök trötta med en annan dam - ska nu fungera

2. **Testa discard till eget bygge**:
   - Skapa ett 12-bygge (kräver reservationskort)
   - Försök släppa en dam (värde 12 på bordet) med discard
   - Damen ska automatiskt läggas till 12-bygget istället för att skapa en ny hög

3. **Testa reservationskort och byggen**:
   - Försök bygga utan att ha reservationskort - ska förhindras
   - Bygg ett bygge med reservationskort
   - Ta in bygget med reservationskortet innan ronden slutar
   - Om bygget inte tas in: varning visas vid rondens slut

4. **Testa trotta utan reservationskort (NYTT)**:
   - Ha endast EN 4:a på hand
   - Det finns en 4:a på bordet
   - Försök trötta - ska förhindras med felmeddelande om reservationskort

5. **Testa att låsta byggen inte kan byggas om (NYTT)**:
   - Spelare A tröttar en 4:a (skapar låst 4-bygge)
   - Spelare B har en 9:a och en kung (13) på hand
   - Spelare B försöker bygga 9:an på 4-bygget för att göra ett 13-bygge
   - Ska förhindras - låsta byggen kan inte byggas om

### Regler som fortfarande gäller:

- Byggen låses efter absorption eller merge
- Ett bygge med 2 kort som inte matchas med fler kort eller kombinationer är öppet
- Trötta låser alltid bygget
- Endast ett bygge per värde tillåts på bordet
- Motståndaren kan inte skapa bygge med samma värde som redan finns

