Mulle - TypeScript port (branch: ts-port)

Syfte
- Portera spelmotor / regler från Python (original i root och mulle/) till TypeScript/Node.
- Behålla original-Python i main-branchen som källa tills TS-porten är verifierad.

Initialt mål
1. Lägga upp TS/Node-projekt-skelett.
2. Påbörja portering: models -> engine -> rules.
3. Skapa motsvarande Jest-tester från Python-testsviten.

Branch-policy
- Allt portningsarbete sker i ts-port.
- När grundläggande motor + tester är klara öppnas en PR mot main med tydlig checklista för verifiering.
