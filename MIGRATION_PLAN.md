# Migreringsplan (högnivå)

1) Initial setup (skapat package.json, tsconfig.json, README).
2) Branch ts-port skapad från main. Python-koden finns kvar i branchen (eftersom branchen skapades från main).
3) Portningsordning (iterationer):
   a) models -> src/models (typer & datastrukturer)
   b) core engine (turn management, deck/distribution) -> src/engine
   c) regler & speciella kort -> src/rules
   d) tests: skapa Jest-tester som speglar Python-tester
4) CI: kör både Python-regression (i legacy eller i main) och nya Jest-tester för att jämföra beteende.
5) När portningen är verifierad: rensa legacy/ eller flytta det till archive/ och gör PR mot main.

Observera: innan merge bestämmer vi om frontenden ska ligga i samma repo eller separat. För webben föreslås att vi återanvänder gemini_mulle-komponenter i en /client eller /web-mapp.