# Mulle Prototyp

En Python-prototyp av kortspelet Mulle. Nu uppdaterad mot mer ursprungliga regler:
- Öppna byggen med ägare (ingen automatisk låsning/konsolidering).
- Kombinationsintag: valfria högar (inkl. byggen) vars sammanlagda bordsvärde matchar spelat korts HAND-värde.
- Mulle: varje exakt par (två identiska kort suit+rank) i ett intag ger en mulle-poäng (ett kort registreras). Fler än två identiska ger ingen mulle för den gruppen.

## Körning

Installera beroenden och kör spelet (en rond, automatiska drag):

```powershell
pip install -r requirements.txt
python -m mulle.cli.game
```

Kör tester:

```powershell
pytest -q
```

Kör motorn headless (utan UI) med fördefinierade drag i ett JSON-script:

```powershell
python -m mulle.engine.headless_runner --seed 42 --rounds 1 --script scripted_moves.json
```

Utan script körs alla drag automatiskt av motorn:

```powershell
python -m mulle.engine.headless_runner --rounds 1
```

## Specialvärden
- Bord: A=1
- Hand: A=14, SP 2=15, RU 10=16

## Heuristik (auto-play)
1. Bästa kombinationsintag med flest mulles (primärt) och flest kort (sekundärt)
2. Enkelt identiskt kort (mulle)
3. Enkelt värdematchande kort
4. Bygge (reservationskort krävs)
5. Släng

## Förenklingar
- Brute force subsets för kombinationsintag (acceptabelt med få högar)
- Ingen full multi-rond/omgång ännu
- Ess i mulle räknas som 14

## Nästa steg
- Interaktivt CLI
- Fullt poängsystem över 7 ronder * 2 omgångar
- Optimerad sökning för kombinationsintag
