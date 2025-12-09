Setup och giv: Varje omgång startar med 2 blandade kortlekar, 104 kort. Första given är 8 kort vardera och 8 kort synligt på bordet. Resterande 5 givar får varje spelare 8 nya kort. 6 givar per omgång, tills leken är slut.
Tillåtna drag: 
1. Bygga upp; Lägga ett kort på ett annat, bygget får då det sammanlagda värdet av korten som ingår. Värdet du bygger till måste du ha på handen
2. Bygga ner; Efter att motståndaren skapat eller byggt på ett bygge kan du välja att bygga neråt, det nya värdet blir då bygget minus värdet på kortet du använder för att bygga ner. Du måste ha ett kort av det nya värdet på handen
3. Trötta; Att lägga ett kort av samma värde på ett kort, 2-kortskombination eller ett bygge. Detta skapar ett låst bygge, dvs värdet kan inte längre ändras. Du måste ha ett kort av samma värde på handen.
4. Intag; enskilda kort och eller kortkombinationer kan tas in med kort från handen. Tvångsintag gör att du måste ta alla kortkombinationer av enskilda kort på bordet som uppgår till det värdet
5. Slänga; Om du inte vill eller kan göra något annat så kan du slänga ett kort till bordet, förutsatt att du inte har några byggen.
6. Bygga in; Du kan bygga in ett kort från handen med ett kort från bordet i ett bygge för att låsa det. Du måste ha ett kort av samma värde på handen.
7. Ta en Mulle; 2 exakt identiska kort bildar en mulle, om du tar in en mulle från bordet med ett kort på handen så får du endast ta mullen i det draget. Om båda mullarna ligger på bordet, eller om du skapar ett bygge med en eller båda mullarna så kan du ta fler kort samtidigt.
Det får bara finnas ett bygge av samma värde på bordet samtidigt. Alla byggen måste tas in under given. Kort kvar på bordet ligger kvar nästa giv, om given är den sista i omgången så får den som tagit in senast korten från bordet.
Låsta byggen får inte byggas om men kan tas in. Du får inte bygga vidare på ett bygge förän motståndaren byggt på det bygget emellan.
Kort med specialvärde är alla ess, spader 2 och ruter 10. Dessa har ett värde när de ligger på bordet, ess=1 spader 2=2 och ruter 10=10, och ett annat på hand, ess=14 spader 2=15 och ruter 10=16. För att ta in dem från handen måste man bygga till det högre värdet, och för att ta mulle på dem så måste ett av korten ligga på bordet så att du kan bygga det till det högre värdet och sen ta in. Ligger båda korten på bordet och du tar in dem samtidigt får du en tabbe för mulle 1, 2 tabbar för mulle 2 (spader) och 10 tabbar för mulle 10 (ruter). 
1 tabbe = 1 poäng, representeras av ett upp och nervänt kort som läggs i samma hög som mulle-korten. Tar du in de sista korten på bordet så får du också en tabbe.
Kort reserverat för annat bygge får inte användas till något annat om inte motståndaren tar in det ursprungliga bygget.
Mulle registreras för exakt par (2 identiska kort i hela intagsgruppen), ett kort per par ger poäng.

Poäng (scoring.score_round):
Mulle-poäng: antal registrerade mulle-kort.
Tabbe: +1 varje gång en spelare tar kort och bordet blir tomt (räknas i total).
Intake points: SP 3–K, RU A, HJ A, KL A ger +1; SP 2, SP A, RU 10 ger +2. Intake räknas separat; bonus: om intake >20, +2 per överstigande kort.
Total = mulle + tabbe + bonus.
Engine-flöde (engine/game_service.py):
start_omgang: ny lek, 8 kort öppet; nollställ fångster/mulles/tabbe.
Varje omgång: 6 givar; före varje rond deal_hands (8 kort per spelare); spela tills händerna är tomma; räkna poäng; nollställ rondsdata; växla startspelare nästa rond.
AI auto_play eller enkel lärande-AI; tabbe registreras när bordet blir tomt efter spelarens drag.