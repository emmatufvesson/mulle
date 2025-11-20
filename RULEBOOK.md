# Mulle — Regelbok

Version: Syncad med kodbas per 2025-11-20 (specialvärdesjustering integrerad).

## Notation
Kort skrivs som "FÄRG VALÖR" (ex: `KL 5`). Färger: KL=Klöver, SP=Spader, HJ=Hjärter, RU=Ruter.

## Översikt
- 2 spelare, två blandade standardlekar (duplikat möjliggör mulles).
- Aktuell implementation kör sessioner med omgångar och ronder (GUI & CLI prototyp). Klassisk fullversion kan utökas senare.
- På en tur spelas exakt ett kort som utför: Capture, Build, Trotta eller Discard.

## Specialvärden i hand vs bord
| Kort | Bordvärde | Handvärde |
|------|-----------|-----------|
| A    | 1         | 14        |
| SP 2 | 2         | 15        |
| RU 10| 10        | 16        |
Övriga kort: samma värde på bord och i hand (2–13, J=11, Q=12, K=13).

## Capture (Intag)
Spelat kort med HAND-värde T kan ta in en uppsättning högar vars BORD-värden summerar till T:
1. Specialvärden 14/15/16: endast builds med exakt värdet kan tas in (inga single-identiska captures). Dessa värden måste alltså först vara byggda.
2. Övriga värden: om exakt ett identiskt single-kort (samma färg+valör) ligger på bordet erbjuds endast den capture (mulle-scenario).
3. Annars beräknas subset-summor av single-piles och builds (värden < T) plus direkta matchningar (=T); en maximal disjunkt mängd väljs.
4. Valda högar + spelat kort flyttas till `captured`.

### Mulle-detektering
Efter capture räknas identiska par (suit+rank, count=2) i gruppen. Varje par ger en mulle (ett av korten förs till `mulles`, poäng = rangvärde; A=14, J=11, Q=12, K=13, siffra = tal). Fyra identiska → två mulles etc. För specialvärden krävs att paret kommer från ett build (kan ej skapas via direkt single-capture).

## Build (Skapa / Utöka)
Lägg handkort på single-pile eller öppet build. Nytt värde = summa av BORD-värden.

### Regelverk
Regler (`can_build`):
- Ej tillåtet att bygga på multi-kort vanlig hög.
- Ej tillåtet att ändra låst build.
- Får ej skapa/utöka till värde som motståndaren redan äger som build.
- Specialvärden 14/15/16 får byggas (krav för framtida capture/mulle).
- Måste ha reservation card (annat handkort med samma HAND-värde) för att få bygga.
- Kort som är enda möjliga capture-kort för eget build är reserverat; kan ej byggas bort.

### Bygga upp eller ner
När du bygger om ett ÖPPET bygge måste du explicit välja om du vill bygga upp eller ner:
- **Upp**: nytt värde = nuvarande byggvärde + tillagt korts bordvärde
- **Ner**: nytt värde = |nuvarande byggvärde - tillagt korts bordvärde|
- GUI visar dialog med båda alternativen
- Absorption kan fortfarande påverka slutgiltiga värdet (se nedan)

### Absorption vid build-skapande
Automatisk absorption av single-piles samt 2-korts-piles/builds vars värden kan packas till build-värdet (direkta matchningar + subset-summor). Buildet låses numera ENDAST om absorption faktiskt sker (extern material tas in) eller om merge med befintligt build sker.

## Låsta vs öppna builds (uppdaterad logik)
- Öppet: ägaren kan utöka (ändra värde) genom att lägga till kort; att bara öka kortantal eller byta värde låser inte längre.
- Låst uppstår ENDAST i dessa fall:
	1. Merge: du skapar/bygger till ett värde där ett annat build med samma värde finns → de slås ihop och låses.
	2. Absorption: vid skapande/ombyggnad absorberas minst en extern hög (single eller 2‑korts) till det deklarerade värdet.
	3. Trotta/Feed: när ett kort med samma BORD-värde läggs på buildet via trotta/feed låses buildet.
- Om inget av ovan inträffar förblir buildet öppet även med >2 kort.
- Låst: värdet och kortuppsättningen kan inte ändras (förutom ytterligare trotta-feed). Kan tas in av valfri spelare med matchande HAND-värde (inkl. 14/15/16).

## Trotta
Spela kort med BORD-värde V och konsolidera: single-piles med värde V, 2-korts-strukturer med summa V, samt par av singles som summerar till V → nytt LÅST build eller utökning av befintligt build (låses). Ingen reservation card krävs.

## Discard / Feed
Släng kort om ingen annan handling väljs. Om du har build med samma BORD-värde matas kortet in (låst eller öppet) via trotta-feed.

## Poäng
- Mulle: summan av alla mulle-kortens rangvärden.
- Tabbe: 1 p för att ta sista kortet från tomt bord.
- Intake: enligt `scoring.py` (1 p: SP 3–13,A; RU A; HJ A; KL A. 2 p: SP 2, SP A, RU 10).
- Bonus: (intake - 20)*2 om intake > 20.
- Total = mulle + tabbe + intake + bonus.

## Heuristik (auto_play_turn)
Prioritet: bästa capture (flest mulles, sedan flest kort) → identiskt single → single match → build → discard.

## Status & Tester
Kärnlogik färdig (capture/build/trotta/discard). Tester: `test_build.py`, `test_capture_locked_build.py`, `test_mulle.py` m.fl.

## Framtida utökning
- Save/Load, förbättrad GUI-captureval, full rond/omgångscykel, avancerad AI.

---
Dokumentet speglar aktuell kod inklusive specialvärdesregeln (bygga krävs innan capture av 14/15/16). Återkoppla vid frågor.
