# Mulle — Regelbok (uppdaterad)

Version: Utkast — uppdaterad med låsningsregel och färgnotation
Källmaterial: Innehåll extraherat från projektfilen, kompletterat med dina senaste instruktioner.

---

## Notation
Kort anges som "<FÄRG> <VALÖR>" där färger skrivs som:
- KL = Klöver
- SP = Spader
- HJ = Hjärter
- RU = Ruter

Exempel: "KL 5", "SP 2", "RU 10", "HJ A".

---

## Snabbregler (viktigaste ändringar)
- Spelare: 2 spelare, två standardkortlekar (duplicerade valörer förekommer).
- En rond: varje spelare spelar 8 kort (en hand). En omgång = 7 ronder. Spelet avslutas efter 2 omgångar.
- Per tur: spelaren måste spela exakt ett kort från handen. Det kortet kan antingen:
  - användas för att ta in ett kort eller ett bygge (intag), eller
  - användas för att bygga (lägga ett kort på en hög och därmed skapa/ändra ett bygge), eller
  - läggas på bordet som en släng (endast tillåtet om kortet i stunden inte skulle kunna ta in något).
  - Det är aldrig tillåtet att både ta in/bygga och samtidigt slänga ett annat kort — endast ett kort lämnar handen per tur.

---

## Byggen, konsolidering och låsning (NYTT, giltigt globalt)
- När en spelare skapar eller ändrar ett bygge (genom att lägga ett kort på ett annat kort eller ett annat bygge), så är följande tvingande:
  1. Alla andra kort av samma valör som bygget samt alla 2-korts-kombinationer (högar som för närvarande består av exakt två kort) på bordet måste omedelbart flyttas in i det nybildade bygget.
  2. Efter denna sammanslagning blir hela bygget "låst".
- Låsta byggen:
  - Kan inte byggas om eller ändras (det går alltså inte att lägga kort på ett låst bygge för att ändra dess sammansättning).
  - Det går bra att fortsätta "trötta" bygget genom att lägga kort av samma valör på bygget (det påverkar inte låsningen).
  - Kan tas in av vem som helst: om en spelare (byggaren eller en motspelare) senare spelar ett kort från sin hand med exakt byggets värde, så kan den spelaren ta in hela det låsta bygget. Att bygget är låst påverkar alltså endast möjligheten att ändra bygget — det hindrar inte intag om någon har ett matchande kort.
  - När någon tar in ett låst bygge gäller samma intagsregler som för vanliga byggen (det intagna fördelas enligt mulle- och intagningsreglerna).
- Denna regel gäller generellt för alla byggen (inte bara dam 12), dvs varje gång någon skapar ett bygge enligt ovan så konsolideras alla kort av samma valör samt alla 2-korts-högar och låses.

Kommentar: Anledningen till denna regel är att spelaren som bygger både kan skydda värdefulla kombinationer från att bli förändrade och tvinga motspelaren till strategiska beslut. Men låsningen är inte ett totalt ägande — bygget kan fortfarande tas av vem som helst som har ett matchande kort.

---

## Mullar och intag
- Definition: En mulle uppstår enbart när du tar in TVÅ IDENTISKA kort — samma färg och samma valör (t.ex. KL 9 + KL 9). Eftersom två lekar används kan identiska kort förekomma.
- Du kan ta in en mulle i tre typfall (exempel):
  a) Ett KL 9 ligger på bordet och du spelar KL 9 från handen → du tar in båda; en av KL 9 läggs i din mulle-hög.
    - I detta fall får du endast in de två KL 9:orna (det spelade kortet + det på bordet).
  b) Två identiska KL 9 ligger på bordet och du spelar ex HJ 9 från handen → du tar in alla tre; en (endast en) KL 9 läggs i din mulle-hög.
  c) Om en av KL 9 ingår i ett bygge så går det bra att ta in fler kort samtidigt.
- Viktig mot-exempel: RU Q + HJ Q är INTE en mulle (olika färg). Du tar in båda korten, men inget läggs i mulle-högen.
- När en mulle tas: endast ETT av de identiska korten läggs i spelarens "mulle-hög" (detta representerar poängen). Övriga intagna kort (inkl. det kort du spelade) läggs i spelarens intagna-/övriga-hög.
- Specialkort: ess, SP 2, RU 10 räknas olika i hand vs bord:
  - På bordet: ess = 1, SP 2 = 2, RU 10 = 10.
  - På handen: ess = 14, SP 2 = 15, RU 10 = 16.
  - Dessa specialvärden påverkar intag och strategiska byggmöjligheter.

---

## Poäng (kortversion)
- Mulle-poäng: värdet på det kort som ligger i mulle-högen (ex. KL 5 = 5 p).
- Tabbe: den som tar in det sista kortet på bordet får en "tabbe" = 1 p (läggs i tabbe-högen).
- Intagningspoäng (räknas efter mullarna/tabbarna):
  - 1 p för: SP 3–13, RU A, HJ A, KL A.
  - 2 p för: SP 2, SP A, RU 10.
- Om en spelares intagningspoäng > 20 → poängen som överstiger 20 dubblas och läggs till spelarens mull/tabbe-poäng. Kvittning sker enligt regelbokens avsnitt om rund- och omgångsberäkning.

# Mulle — Regelbok

Version: Syncad med kodbas per 2025-11-20.

## Notation
Kort skrivs som "FÄRG VALÖR" (t.ex. `KL 5`). Färger:
- KL = Klöver
- SP = Spader
- HJ = Hjärter
- RU = Ruter

## Översikt
- 2 spelare, två blandade standardlekar (duplikat möjliggör mulles).
- Aktuell implementation kör EN rond (8 kort per spelare); fler ronder/omgångar enligt klassisk regel (7 ronder * 2 omgångar) är ännu ej implementerat.
- På en tur måste spelaren spela exakt ett kort och utför då en (1) handling: Capture (intag), Build (bygga), Trotta (specialbygg), eller Discard (släng / värde-"feed" till eget bygge).

## Specialvärden i hand vs bord
| Kort | Värde på bord | Värde i hand |
|------|---------------|--------------|
| A    | 1             | 14           |
| SP 2 | 2             | 15           |
| RU 10| 10            | 16           |
Övriga kort har samma värde på bord och i hand (2–13 resp. J=11, Q=12, K=13).

## Capture (Intag)
När ett kort spelas kan spelaren ta in EN kombination av högar vars sammanlagda värde (summerat med kortets HAND-värde) matchar HAND-värdet på det spelade kortet. Algoritmen i `capture.generate_capture_combinations`:
1. Om exakt ett identiskt single-kort (samma färg + valör) finns: endast den mullen erbjuds (prioriterad regel).
2. Om värdet är special (14,15,16) får man bara ta in builds med exakt det värdet (inga summekombinationer av fria kort).
3. Annars beräknas alla subset-summor av single-piles och builds vars värden summerar till målvärdet; en maximal mängd disjunkta delmängder plus alla direkta matcher väljs (heuristik: maximerar antal tagna kort).
4. Alla kort i valda högar + spelade kortet förs till spelarens `captured`.

### Mulle-detektering
Efter intag räknas antal (färg,valör)-par bland intagna + spelat kort. Varje exakt par (antal=2) ger en mulle: ett av korten förs till `mulles` och ger poäng lika med kortets rang (A=14, J=11, Q=12, K=13, sifferkort = talvärdet). Fler än två identiska genererar flera par (ex. fyra identiska ger två mulles).

## Build (Skapa / Utöka bygge)
Bygg sker genom att lägga ett handkort på antingen:
1. Ett single-pile (1 kort) för att skapa nytt build-värde = summan av kortens BORD-värden.
2. Ett öppet build som ännu inte är låst.

Regler kontrolleras i `can_build`:
- Man får inte bygga på en multi-kort vanlig hög (endast single eller build).
- Man får inte ändra (bygga på) ett låst build.
- Man får inte skapa/utöka till ett värde som motståndaren redan äger som build.
- Specialrestriktion: kan ej skapa värden 14 (A), 15 (SP 2), 16 (RU 10) direkt via motsvarande specialkortkombination (de reserveras för capture-scenarier).
- Måste ha ett "reservation card" i hand (ett annat kort vars HAND-värde matchar nya build-värdet) för att säkerställa framtida möjlighet att ta in.
- Ett kort som är enda möjliga capture-kort för ett eget befintligt build är reserverat och kan inte användas för att bygga annat.

### Absorption vid build-skapande
`Board.create_build` utför följande:
1. Bas-högen tas bort och kombineras med det spelade kortet.
2. Alla single-piles och alla 2-korts-piles/builds på bordet samlas som kandidater.
3. Direkta matchningar (värde == build-värdet) tas alltid med.
4. En backtracking-algoritm väljer disjunkta subsets av kandidater vars SUMMA == build-värdet för att maximera antal absorberade högar.
5. Alla korten läggs in i byggestacken.
6. Build låses om det nu innehåller fler än 2 kort eller om absorption skedde.

Resultat: ett 2-korts build utan absorption förblir öppet; alla större eller sammanslagna builds blir låsta.

## Låsta vs öppna builds
- Öppet: kan byggas vidare av ägaren (ingen annan får lägga på) så länge det är olåst.
- Låst: kan inte ändras, men kan få kort av samma värde via Trotta/"feed" (se nedan). Kan tas in av ANY spelare som spelar ett kort med exakt HAND-värdet.

## Trotta
Trotta-action (special): spela ett kort vars BORD-värde = målvärdet du vill konsolidera.
1. Om du redan har ett build med det värdet: kortet adderas (`add_trotta_card`), buildet låses (om inte redan låst).
2. Annars: alla single-piles med exakt BORD-värdet, alla 2-korts-piles/builds med total BORD-summa = värdet, samt alla par av single-piles som tillsammans SUMMERAR till värdet absorberas. Ett nytt LÅST build skapas.
Trotta kan alltså skapa låst build utan krav på reservationskort.

## Discard (Släng / Feed)
Om inget capture/build är möjligt (eller valt) läggs kortet som discard:
- Om spelaren äger ett build med samma BORD-värde som kortet läggs kortet in i buildet via trotta-feed (även låsta builds accepterar detta) och låsningen kvarstår.
- Annars placeras kortet som ny single-pile på bordet.

## Poäng
- Mulle-poäng: summa av alla mulle-kortens rangvärden (A=14, J=11, Q=12, K=13, sifferkort = talet).
- Tabbe: 1 poäng till den som tar sista kortet på tomt bord.
- Intagningspoäng (scoring.py):
  - 1 p: SP 3–13 + A; RU A; HJ A; KL A.
  - 2 p: SP 2, SP A, RU 10.
- Bonus: Intake > 20 ger (intake - 20)*2 extra.
- Total: mulle + tabbe + intake + bonus.

## Automatiserad turordning (heuristik)
`auto_play_turn` prioriterar: bästa capture-kombination (flest mulles, sedan flest kort) → identiskt single (mulle) → single match → build → discard.

## Implementationsstatus / Ej klart
- Fler ronder & omgångar: inte implementerat ännu.
- Interaktiv input: ej (automatiskt heuristiskt spel).
- Avancerade strategier: reservationslogik & enkel heuristik finns; ingen djup AI.

## Tester (urval)
- `test_build.py`: absorption & låsning.
- `test_capture_locked_build.py`: capture av låst build.
- `test_mulle.py`: mulle-par.
- Övriga tester täcker specialkort, integritet och lärande.

## Framtida utvidgning
- Full omgångscykel (7 ronder * 2 omgångar) med kumulativ poäng.
- Mer avancerad AI-viktning (risk/nytta av öppna vs låsta builds).
- UI (CLI + GUI) med val av handling.
- Replay/loggning av drag.

---
Detta dokument är nu synkroniserat med den faktiska kodlogiken. Återkoppla gärna om ytterligare klargöranden behövs.
- Bo kvar: 1 kort.
