# Mulle — Komplett Regelbok

Version: 2025-11-27 (Synkad med implementation)

---

## 1. Spelets Översikt

**Mulle** är ett kortspel för 2 spelare som spelas med två blandade standardlekar (104 kort totalt). Dubbletter av kort möjliggör "mulles" (par av identiska kort) vilket ger extra poäng.

### Spelstruktur
- **Session**: Består av flera omgångar
- **Omgång**: 6 ronder med samma lek (104 kort)
- **Rond**: Spelarna får 8 kort var, 8 kort läggs på bordet
- Efter varje rond får spelarna nya 8 kort (totalt 8+16+16+16+16+16+16=104 kort per omgång)
- Spelaren som börjar alternerar mellan omgångar

### Tur
På varje tur spelar du exakt ett kort från din hand och utför **en** av följande åtgärder:
1. **Capture** (Intag) — Ta in kort från bordet
2. **Build** (Bygge) — Skapa eller utöka ett bygge
3. **Trotta** — Konsolidera kort av samma värde till ett låst bygge
4. **Discard** (Släng) — Lägg kort på bordet

---

## 2. Kortnotation och Värden

### Notation
Kort skrivs: `FÄRG VALÖR`
- **Färger**: KL (Klöver ♣), SP (Spader ♠), HJ (Hjärter ♥), RU (Ruter ♦)
- **Valörer**: 2, 3, 4, 5, 6, 7, 8, 9, 10, J (Knekt), Q (Dam), K (Kung), A (Ess)

### Specialvärden
Vissa kort har olika värden beroende på om de ligger på bordet eller i hand:

| Kort  | Bordvärde | Handvärde | Kommentar |
|-------|-----------|-----------|-----------|
| A     | 1         | 14        | Alla ess |
| SP 2  | 2         | 15        | Endast Spader 2 |
| RU 10 | 10        | 16        | Endast Ruter 10 |

**Övriga kort**: Samma värde på bord och i hand
- Sifferkort: 2-10 = nominellt värde
- J (Knekt) = 11
- Q (Dam) = 12
- K (Kung) = 13

---

## 3. Capture (Intag)

Du kan ta in kort från bordet om deras sammanlagda **bordvärden** matchar ditt korts **handvärde**.

### Regler för Capture

#### 3.1 Specialvärden (A=14, SP 2=15, RU 10=16)
Kort med handvärde 14, 15 eller 16 kan **endast** tas in via byggen:
- Du kan **inte** ta ett identiskt ess direkt från bordet
- Du måste först **bygga** ett bygge med värde 14/15/16
- Sedan ta in bygget med ditt specialvärdeskort

**Exempel**: Du har SP A (handvärde 14) och det finns KL A (bordvärde 1) på bordet
- ❌ Du kan INTE ta KL A direkt med SP A
- ✅ Du måste först bygga ett 14-bygge (t.ex. med KL A + SP K)
- ✅ Sedan ta in 14-bygget med SP A

#### 3.2 Identiskt Kort (Mulle-scenario)
Om det finns **exakt ett** kort på bordet med samma färg och valör som ditt spelat kort:
- Detta är det **enda** alternativet som erbjuds
- Resulterar i en mulle (se Poängräkning)

**Exempel**: Du spelar RU 9 och det finns exakt en RU 9 på bordet
- Du tar automatiskt in RU 9 + RU 9 = mulle (9 poäng)

#### 3.3 Kombinationsintag
Om inga specialfall gäller, beräknas alla möjliga kombinationer:
1. Hitta alla högar (enskilda kort + byggen) vars bordvärde = ditt handvärde
2. Hitta alla kombinationer av högar vars bordvärden summerar till ditt handvärde
3. Välj den **maximala disjunkta mängden** (flest högar utan överlapp)

**Prioritering vid automatiskt spel**:
1. Kombination med flest mulles
2. Kombination med flest kort
3. Enskilt värdematchande kort

### 3.4 Mulle-detektering
Efter capture räknas alla identiska par i den insamlade gruppen (inkl. spelat kort):
- **Mulle**: Exakt 2 kort med samma färg + valör
- **Värde**: Ett av korten registreras i `mulles`, poäng = rangvärde
  - A = 14 poäng
  - J = 11, Q = 12, K = 13
  - Sifferkort = nominellt värde
- **Flera identiska**: 4 identiska kort = 2 mulles, 6 identiska = 3 mulles, etc.

**Viktigt**: För specialvärden (14/15/16) krävs att paret kommer från ett bygge — direkt single-capture blockeras.

---

## 4. Build (Bygge)

Ett bygge är en hög kort som reserveras för framtida intag. Byggen har en **ägare** och ett **målvärde**.

### 4.1 Skapa Bygge
Du kan lägga ett handkort på:
- En **enskild kort-hög** (single pile)
- Ett **öppet bygge** (du eller motståndaren äger)

**Nytt värde** = summa av kortens bordvärden

### 4.2 Regelverk för Bygge

Du **kan INTE** bygga om:
- ❌ Hög har >1 kort (måste vara single eller existerande bygge)
- ❌ Bygget är låst
- ❌ Motståndaren redan har bygge med samma värde
- ❌ Du saknar **reservationskort** (annat kort i hand med samma handvärde som bygget)
- ❌ Ditt enda reservationskort är reserverat för annat bygge

**Reservationskort**:
- Krävs för att skapa/utöka bygge
- Måste ha minst ett kort i hand som kan ta in bygget (handvärde = byggvärde)
- Om du bara har ett sådant kort och det är ditt enda sätt att ta in ett eget bygge, kan du inte använda det för annat bygge

**Specialvärden** (14/15/16):
- ✅ Tillåtet att bygga dessa värden (nödvändigt för mulles)
- Kräver fortfarande reservationskort

### 4.3 Bygga Upp eller Ner
När du bygger om ett **öppet bygge** måste du välja riktning:

- **Upp**: Nytt värde = nuvarande värde + tillagt korts bordvärde
- **Ner**: Nytt värde = |nuvarande värde - tillagt korts bordvärde|

I GUI visas dialog: "Bygg upp eller ner?" med båda beräknade värdena.

**Viktigt**: Absorption kan fortfarande ändra slutvärdet (se nedan).

### 4.4 Absorption
När du skapar/utökar bygge sker **automatisk absorption**:
- Systemet hittar alla **single-piles** och **2-korts högar/byggen** på bordet
- Beräknar vilka som kan packas ihop till ditt deklarerade byggvärde
- Absorberar maximalt antal högar via subset-summa algoritm

**Absorptionsregler**:
- Endast single (1 kort) eller 2-korts strukturer kan absorberas
- 3+ korts högar kan **inte** absorberas vid bygge (endast vid capture)
- Direkta matchningar (värde = byggvärde) prioriteras
- Subset-summor (kombinationer < byggvärde) beräknas

**Exempel**: 
- Bygger 7 med KL 3 + HJ 4
- Bordet har: SP 5, RU 2
- SP 5 absorberas (direktmatchning)
- RU 2 absorberas INTE (5+2=7 men 5 redan använd, 2 ensam < 7)
- Resultat: Bygge (KL 3, HJ 4, SP 5), RU 2 kvarstår

---

## 5. Låsta vs Öppna Byggen

### Öppet Bygge
- **Ägaren** kan utöka (lägga till kort, ändra värde)
- Motståndaren kan **inte** ändra bygget
- Enbart öka kortantal eller byta värde låser **inte** automatiskt

### Låsning Sker ENDAST vid:

#### 5.1 Merge (Sammanslagning)
- Du skapar/bygger till ett värde där ett annat bygge med samma värde redan finns
- De slås ihop automatiskt
- Resultatet **låses alltid**

**Exempel**:
- Bordet har 7-bygge (ägt av motståndaren)
- Du bygger KL 4 + HJ 3 = 7
- Ditt bygge mergar med motståndarens → låst 7-bygge

#### 5.2 Absorption
- Vid skapande/ombyggnad absorberas minst en extern hög
- Bygget låses eftersom externt material dragits in

**Exempel**:
- Du bygger RU 5 + SP 3 = 8
- Bordet har KL 8 (single)
- KL 8 absorberas → bygget låses

#### 5.3 Trotta/Feed
- Ett kort med samma **bordvärde** läggs till via trotta eller feed
- Bygget låses automatiskt

### Låst Bygge
- Kan **inte** ändras eller byggas om
- Kan tas in av **valfri spelare** med matchande handvärde
- Ytterligare trotta-kort kan läggas till (förblir låst)

---

## 6. Trotta

Konsolidera alla kort på bordet med samma bordvärde till ett låst bygge.

### Trotta-process
1. Spela kort med bordvärde V
2. Systemet samlar:
   - Alla single-piles med värde V
   - Alla 2-korts strukturer med summa V
   - Par av singles som summerar till V
3. Skapar **låst bygge** med värde V (eller lägger till befintligt)

**Specialfall**:
- Om du redan har bygge med värde V → kortet läggs till bygget (låses)
- Ingen reservationskort krävs för trotta
- Trottade byggen är **alltid låsta**

**Exempel**:
- Bordet: HJ 4 (single), KL 4 (single), bygge (RU 2 + SP 2)
- Du trottar med SP 4 (bordvärde 4)
- Resultat: Låst 4-bygge innehåller (HJ 4, KL 4, RU 2, SP 2, SP 4)

---

## 7. Discard / Feed

Om du inte vill (eller kan) göra capture/build/trotta, slänger du kortet till bordet.

### Feed (Automatisk Trotta)
Om du har ett bygge med samma bordvärde som kortet du slänger:
- Kortet läggs **automatiskt** till bygget (feed)
- Bygget låses
- Ingen ny hög skapas

**Exempel**:
- Du har ett 12-bygge
- Slänger HJ Q (bordvärde 12)
- HJ Q läggs automatiskt till 12-bygget (låses)

### Reserverat Kort
Du kan **inte** slänga ett kort som är reserverat för ditt bygge:
- Om kortet är ditt enda sätt att ta in ett eget bygge
- Systemet blockerar discard med felmeddelande

---

## 8. Poängräkning

### 8.1 Mulle
- Summan av alla mulle-korts rangvärden
- A = 14, J = 11, Q = 12, K = 13, sifferkort = nominellt värde

**Exempel**: Mulles RU 9 + KL A + SP 5 = 9 + 14 + 5 = 28 poäng

### 8.2 Tabbe
- 1 poäng för att ta sista kortet från ett tomt bord
- Om flera tabbe samma rond = flera poäng (1p per tabbe)

### 8.3 Intake (Intagspoäng)
Vissa kort ger extra poäng när de tas in:

**1 poäng per kort**:
- SP 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K (Spader 3-K)
- RU A (Ruter Ess)
- HJ A (Hjärter Ess)
- KL A (Klöver Ess)

**2 poäng per kort**:
- SP 2 (Spader 2)
- SP A (Spader Ess — får både 1p från första listan OCH 2p extra = 3p totalt)
- RU 10 (Ruter 10)

**Viktigt**: SP A räknas i båda kategorierna = 1 + 2 = 3 poäng

### 8.4 Bonus
Om dina intake-poäng > 20:
- Bonus = (intake - 20) × 2

**Exempel**: Intake = 24 → Bonus = (24-20) × 2 = 8 poäng

### 8.5 Total Poäng
**Total = Mulle + Tabbe + Bonus**

**Viktigt**: Intake-poäng räknas INTE in i totalen. De används endast för att beräkna bonus.

**Exempel**:
- Mulle: 28p
- Tabbe: 2p
- Intake: 24p (används för bonusberäkning, adderas EJ till total)
- Bonus: 8p (eftersom intake > 20)
- **Total: 28 + 2 + 8 = 38p**

---

## 9. Spelförlopp

### Session
1. Välj antal omgångar att spela
2. Spelaren som börjar alternerar mellan omgångar (Anna → Bo → Anna...)
3. Kumulativa poäng räknas över alla omgångar

### Omgång (6 Ronder)
1. Blanda två nya lekar (104 kort)
2. Lägg 8 kort på bordet
3. Dela ut 8 kort till varje spelare
4. Spela rond 1
5. Dela ut 8 nya kort till varje spelare
6. Spela rond 2
7. ... (totalt 6 ronder)
8. Summera poäng för omgången
9. Rensa bordet

### Rond
1. Spelaren i tur spelar ett kort (Capture/Build/Trotta/Discard)
2. Nästa spelare
3. Fortsätt tills båda spelarna har tomma händer
4. Räkna poäng (Mulle + Tabbe + Intake + Bonus)

**Varning**: Om byggen finns kvar på bordet vid rondens slut indikerar det felaktig spelning (byggen ska ha tagits in eller ägaren bröt reservationsregeln).

---

## 10. AI och Automatiskt Spel

### Heuristik (auto_play_turn)
Prioritering vid automatiska drag:
1. **Bästa Capture**: Flest mulles (primärt), sedan flest kort (sekundärt)
2. **Identiskt Kort**: Garanterad mulle
3. **Värdematchning**: Single kort med rätt värde
4. **Bygge**: Om reservationskort finns
5. **Discard**: Sista utvägen

### Learning AI (SimpleLearningAI)
- Utvärderar kandidatåtgärder med kategori-baserade värden
- Lär sig från belöningar: captured cards + 10×mulles + 2×build_created
- Exploration rate: 15% (testar slumpmässiga drag)
- Learning rate: 0.2 (viktuppdatering)

**Kategorier**:
- `capture_combo_mulle`: 10.0 (startvärde)
- `capture_combo`: 5.0
- `build`: 1.0
- `discard`: 0.0

---

## 11. Implementation och Tester

### Kärnlogik
- ✅ Capture med subset-summa algoritm
- ✅ Build med absorption och låsningsregler
- ✅ Trotta konsolidering
- ✅ Discard med feed
- ✅ Specialvärden (14/15/16) med build-krav
- ✅ Mulle-detektering (exakt 2 identiska)
- ✅ Reservationskort validering
- ✅ Bygga upp/ner val för öppna byggen

### Testsvit
- `test_build.py`: Byggregler och absorption
- `test_capture_locked_build.py`: Låsta byggen kan inte ändras
- `test_mulle.py`: Mulle-detektering och poängräkning
- `test_special_cards.py`: Specialvärden (A, SP 2, RU 10)
- `test_trotta.py`: Trotta-konsolidering
- `test_game_engine.py`: GameEngine integration

**Alla tester passar** (20 st)

---

## 12. GUI och CLI

### GUI (game_gui.py)
- Visuellt spelplan med kort
- Klickbara kort och högar
- Bygga upp/ner dialog för öppna byggen
- Detaljerad poängpanel (mullar med kortkoder, tabbe, intake, bonus)
- Auto-knapp för AI-drag (Bo)

### CLI (game.py)
- Headless körning via GameEngine
- Enkel interaktiv selector (discard-baserad)
- Session summary med AI-värden

### Headless Runner (headless_runner.py)
- Kör spel utan UI via JSON-script
- Automatisk körning med seed-kontroll
- Användbart för batch-testing

---

## 13. Framtida Utökningar

- Save/Load spelstatus
- Förbättrad capture-väljare i GUI (välj mellan kombinationer)
- Full rond/omgångscykel med automatisk delning
- Avancerad AI med djupare strategier
- Multiplayer över nätverk
- Statistik och replay-funktioner

---

**Dokumentversion**: 2025-11-27  
**Kodversion**: Synkad med commit bca3bc7 (GameEngine + learning_ai introduction)

För tekniska detaljer och implementation notes, se README.md och källkoden i `mulle/`-katalogen.
