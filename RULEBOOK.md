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
  - användas för att ta in ett kort eller en byggnad (intag), eller
  - användas för att bygga (lägga ett kort på en hög och därmed skapa/ändra ett bygge), eller
  - läggas på bordet som en släng (endast tillåtet om kortet i stunden inte skulle kunna ta in något).
  - Det är aldrig tillåtet att både ta in/byga och samtidigt slänga ett annat kort — endast ett kort lämnar handen per tur.

---

## Byggen, konsolidering och låsning (NYTT, giltigt globalt)
- När en spelare skapar eller ändrar ett bygge (genom att lägga ett kort på en annan hög så att byggets värde uppstår), så är följande tvingande:
  1. Alla andra 2-korts-kombinationer (högar som för närvarande består av exakt två kort) på bordet måste omedelbart flyttas in i det nybildade bygget.
  2. Efter denna sammanslagning blir hela bygget "låst".
- Låsta byggen:
  - Kan inte byggas om eller ändras av andra spelare (det går alltså inte att lägga kort på ett låst bygge för att ändra dess sammansättning).
  - Kan inte flyttas eller konsolideras ytterligare av motspelare.
  - Kan tas in av vem som helst: om en spelare (byggaren eller en motspelare) senare spelar ett kort från sin hand med exakt byggets värde, så kan den spelaren ta in hela den låsta byggnaden. Att bygget är låst påverkar alltså endast möjligheten att ändra/bygga på det — det hindrar inte intag om någon har ett matchande kort.
  - När någon tar in ett låst bygge gäller samma intagsregler som för vanliga byggen (det intagna fördelas enligt mulle- och intagningsreglerna).
- Denna regel gäller generellt för alla byggen (inte bara dam 12), dvs varje gång någon skapar ett bygge enligt ovan så konsolideras alla 2-korts-högar och låses.

Kommentar: Anledningen till denna regel är att spelaren som bygger både kan skydda värdefulla kombinationer från att bli förändrade och tvinga motspelaren till strategiska beslut. Men låsningen är inte ett totalt ägande — bygget kan fortfarande tas av vem som helst som har ett matchande kort.

---

## Mullar och intag
- En mulle uppstår när du tar in "två likadana kort" (med duplicering från två lekar möjlig).
- Du kan ta in en mulle i tre fall (exempel):
  a) Ett kort av valören ligger på bordet och du har ett kort av samma valör i handen → spela ditt kort och ta in paret.  
  b) Båda lika ligger på bordet och du har ett likadant på handen → spela ditt kort och ta in alla tre.  
  c) Det finns specialregler där ett kort med dubbla valören kan ta in två lika (specificera om du vill använda detta).
- När en mulle tas: endast ETT av de lika korten läggs i spelarens "mulle-hög" (this represents the poäng). Övriga intagna kort (inkl. det kort du spelade för att ta in) läggs i spelarens intagna-/övriga-hög.
- Specialkort: ess, SP 2, RU 10 räknas olika i hand vs bord:
  - På bordet: ess = 1.
  - På handen: ess = 14, SP 2 = 15, RU 10 = 16.
  - Dessa specialvärden påverkar vissa mullexempel och strategiska byggmöjligheter.

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
Notera: vi använder två kortlekar, så dubbla valörer förekommer.

Start (notation som KL/SP/HJ/RU):
- Bord (8 högar / synliga kort):
  1) SP 5
  2) SP 5
  3) [KL 9 + RU 7]  (2-korts-hög, värde 16)
  4) RU 10
  5) HJ A
  6) KL 5
  7) RU 3
  8) KL 2

- Anna (hand, 8 kort): KL 9, SP 6, SP 3, KL K, HJ 8, RU 4, KL 4, KL 7
- Bo (hand, 8 kort): RU 10, 6, HJ Q, SP 2, KL Q, RU 5, SP 7, HJ J

Spel (turn-by-turn, ett kort per tur):

Drag 1 — Anna
- Val: Anna kan take in KL 9-mullen (KL 9 på bord + KL 9 i hand) eller välja annat.
- Handling: Anna spelar KL 9 och tak in KL 9 från bordet.
- Effekt: en KL 9 läggs i Annas mulle-hög (9 p). Övriga intagna (om några) hamnar i hennes intagna-hög.
- Anna kvar: 7 kort.

Drag 2 — Bo
- Val: Bo har RU 10 på hand och noterar att det finns en 2-korts-hög [KL 9 + RU 7] värd 16 på bordet.
- Handling: Bo spelar 6 på RU 10 och skapar ett bygge värde 16. Enligt konsolideringsregeln flyttas alla 2-korts-högar in i det nya bygget och bygget blir låst.
- Effekt: bygget innehåller RU 10 + 6 + KL 9 + RU 7 och blir låst. Eftersom låsningen inte hindrar intag kan vem som helst senare ta in bygget om de spelar ett kort med värde 16.
- Kommentar: i detta scenario kan Anna inte ändra eller bygga på den låsta högen, men om hon senare får ett kort som motsvarar 16 kan hon spela det och ta in bygget trots låsningen.

Fortsatt spel: (resten av rundan fortsätter enligt tidigare exempel; låsning skyddar mot modifiering men inte mot intag när matchande värde finns.)