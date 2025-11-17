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

---

## Exempelomgång — uppdaterat med låsningsregeln (hel rond, alla 8 kort spelas)
Notera: vi använder två kortlekar, så identiska kort (samma färg och valör) kan förekomma.

Start (notation som KL/SP/HJ/RU):
- Bord (8 synliga kort):
  1) SP 5
  2) SP 5
  3) KL 9
  4) RU 10
  5) HJ A
  6) KL 5
  7) RU 3
  8) KL 2

- Anna (hand, 8 kort): KL 9, SP 6, SP 3, KL K, HJ 8, RU 4, KL 4, KL 7
- Bo (hand, 8 kort): RU 10, RU 6, HJ Q, SP 2, KL Q, RU 5, SP 7, HJ J

Spel (turn-by-turn, ett kort per tur):

Drag 1 — Anna
- Val: Anna kan ta in KL 9-mulle (KL 9 på bord + KL 9 i hand) eller välja annat.
- Handling: Anna spelar KL 9 och tar in KL 9 från bordet.
- Effekt: en KL 9 läggs i Annas mulle-hög (9 p). Övriga intagna (om några) hamnar i hennes intagna-hög.
- Anna kvar: 7 kort.

Drag 2 — Bo
- Val: RU 10 ligger på bordet och Bo har RU 10 och RU 6 på hand vilket innebär att han kan bygga 16.
- Handling: Bo spelar RU 6 på RU 10 och skapar ett bygge värde 16.
- Effekt: bygget innehåller RU 10 + RU 6. Eftersom det bara finns 2 kort av varje och Bo har den andra RU 10 i hand, vet han att anna inte kan ta in bygget, men hon kan bygga om det.
- Bo kvar: 7 kort.

Drag 3 — Anna
- Anna har SP 6, SP 3, KL K, HJ 8, RU 4, KL 4, KL 7 kvar.
- Anna bygger om 16-byget genom att spela KL K på det så att bygget nu är värt 3.
- Eftersom det finns andra kort och kortkombinationer på bordet som blir 3 så konsolideras dessa i bygget:
  - RU 3 (från bordet) läggs till bygget.
  - KL 2 och HJ A (från bordet) läggs till eftersom de också blir 3 tillsammans (2+1).
  - Bygget är nu låst, och består av KL K + RU 6 + RU 10 + SP 3 + KL 2 + HJ A.
  - Anna kvar: 6 kort.

Drag 4 — Bo
- Bo har RU 10, HJ Q, SP 2, KL Q, RU 5, SP 7, HJ J kvar.
- Bo tar in SP 5-mullen och KL 5 från bordet genom att spela RU 5 från handen.
- En SP 5 läggs i Bo's mulle-hög (5 p). Övriga intagna kort hamnar i hans intagna-hög.
- Bo kvar: 6 kort.

Drag 5 — Anna
- Anna har SP 6, SP 3, HJ 8, RU 4, KL 4, KL 7 kvar.
- Eftersom det bara är hennes bygge kvar på bordet så måste hon ta in det genom att spela SP 3 från handen.
- Anna får en tabbe (1 p) för att hon tar in det sista kortet på bordet.
- ett kort från bygget läggs uppochner i hennes mulle-hög, resten i intagna-högen.
- Anna kvar: 5 kort.

Drag 6 — Bo
- Bo har RU 10, HJ Q, SP 2, KL Q, SP 7, HJ J kvar.
- Bo kan inte ta in något eller bygga något (eftersom bordet är tomt efter annas drag).
- Bo slänger RU 10 på bordet.
- Bo kvar: 5 kort.

Drag 7 — Anna
- Anna har SP 6, HJ 8, RU 4, KL 4, KL 7 kvar.
- Anna kan inte ta in något eller bygga något (eftersom bordet bara har RU 10 som inte matchar något i hennes hand).
- Anna slänger RU 4 på bordet.
- Anna kvar: 4 kort.

Drag 8 — Bo
- Bo har HJ Q, SP 2, KL Q, SP 7, HJ J kvar.
- Bo lägger sin HJ J på RU 4 på bordet och bygger 15.
- Eftersom inga andra kort på bordet kan kombineras till 15 så är bygget inte låst
- Bo kvar: 4 kort.

Drag 9 — Anna
- Anna har SP 6, HJ 8, KL 4, KL 7 kvar.
- Anna bygger om 15-byget genom att spela KL 7 på det så att bygget nu är värt 8.
- Eftersom inga andra kort på bordet kan kombineras till 8 så är bygget inte låst.
- Anna kvar: 3 kort.

Drag 10 — Bo
- Bo har HJ Q, SP 2, KL Q, SP 7 kvar.
- Bo bygger tillbaka 8-bygget genom att spela SP 7 på det så att bygget nu är värt 15 igen.
- Eftersom inga andra kort på bordet kan kombineras till 15 så är bygget inte låst.
- Bo kvar: 3 kort.

Drag 11 — Anna
- Anna har SP 6, HJ 8, KL 4 kvar.
- Anna kan inte göra något åt 15-bygget, och hon kan inte ta in RU 10, så hon slänger KL 4 på bordet.
- Anna kvar: 2 kort.

Drag 12 — Bo
- Bo har HJ Q, SP 2 och KL Q kvar.
- Bo tar in 15-bygget genom att spela SP 2 från handen.
- alla kort från bygget läggs i hans intagna-hög.
- Bo kvar: 2 kort.

Drag 13 — Anna
- Anna har SP 6 och HJ 8 kvar.
- Anna kan inte ta in något eller bygga något, så hon slänger HJ 8 på bordet.
- Anna kvar: 1 kort.

Drag 14 — Bo
- Bo har HJ Q och KL Q kvar.
- Bo lägger KL Q på HJ 8 och KL 4 på bordet och bygger på så vis 12, låst.
- Bo kvar: 1 kort.

Drag 15 — Anna
- Anna har SP 6 kvar.
- Anna kan inte ta in något eller bygga något, så hon slänger SP 6 på bordet.
- Anna kvar: 0 kort.

Drag 16 — Bo
- Bo har HJ Q kvar.
- Bo tar in sitt 12-bygge genom att spela HJ Q från handen.
- alla kort från bygget läggs i hans intagna-hög.
- Bo kvar: 0 kort.

På bordet finns spader 6 kvar till nästa rond. 




### Datastrukturer
- Card: hanterar värden på bord (A=1) och i hand (A=14, SP 2=15, RU 10=16).
- Deck: två standardlekar blandas.
- Board: lista av högar (enkla listor av kort) och låsta byggen (klass Build).
- Build: högar med kort som låses när ett värde upprepas och läggs till högen. 
- Player: spårar hand, intagna kort, mulles, tabbe.

### Handlingar (automatisk turordning i prototyp)
Prioritetsordning per tur: ta låst bygge (matchande handvärde) → ta enkelkort (inkl. mulle-scenario) → skapa bygge → släng.

### Förenklingar / Antaganden
- Endast single-card capture implementerad (inga komplexa summor eller multi-pile intag utöver låsta byggen).
- Mulle uppstår bara vid exakt två identiska kort i samma intagstillfälle (fler än två identiska reduceras till ett par för poängräkning).
- Poäng för ess i mulle antas vara 14 (ej helt specificerat i kortversionen).
- Inga flera ronder/omgångar ännu; endast en rond körs via `python -m mulle.cli.game`.
- Ingen mänsklig interaktiv input; drag görs automatiskt enligt heuristik.

### Tester
Finns under `tests/`:
- `test_build.py`: verifierar konsolidering och låsning.
- `test_capture_locked_build.py`: verifierar att låst bygge kan tas in.
- `test_mulle.py`: verifierar mulle-scenario (ett kort på bord + identiskt i hand).

### Nästa steg / Möjliga utbyggnader
- Interaktiv CLI där spelaren väljer åtgärd.
- Fler intagsscenarier (kombinationssummor, flera högar samtidigt).
- Full flerstegs poängberäkning över 7 ronder * 2 omgångar.
- Loggning / replay av turer.
- Strategi-modul för AI (viktning av bygge vs capture).

--- End Appendix ---
