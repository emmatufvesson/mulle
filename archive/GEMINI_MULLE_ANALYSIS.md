# Gemini Mulle - Frontend Analysis

**Repo**: https://github.com/emmatufvesson/gemini_mulle
**Tech Stack**: React + Vite + Capacitor (iOS)
**Status**: Mobile app (iOS focus)

---

## 🎯 Återanvändbara Komponenter

### 1. CardComponent.tsx ✅ Användbar!
**Funktionalitet**:
- Visar kort med suit/rank
- Selected state (gul ram, lyft upp)
- Small variant för piles
- Responsive (olika storlekar för mobile/desktop)
- Card back rendering

**Kan återanvändas**: JA - behöver bara anpassas från mobile-first till webb

### 2. gameLogic.ts ⚠️ Ofullständig
**Funktionalitet**:
- Deck creation och shuffle
- Value calculators (getHandValue, getTableValue)
- Mulle points calculation

**Problem**: Saknar komplex spellogik (capture combinations, builds, trotta)
**Status**: VÅR implementation är bättre - använd inte denna

### 3. types.ts 📋 Referens
**Innehåller**:
```typescript
export enum Suit {
  CLUBS, SPADES, HEARTS, DIAMONDS
}

export enum Rank {
  TWO = 2, THREE = 3, ..., ACE = 14
}

export interface Card {
  id: string;
  suit: Suit;
  rank: Rank;
  isRed: boolean;
}

export interface TablePile {
  id: string;
  cards: Card[];
  isBuild?: boolean;
  buildValue?: number;
  buildOwner?: string;
  isLocked?: boolean;
}

export interface PlayerState {
  hand: Card[];
  captured: Card[];
  mulles: number;
  tabbe: number;
}
```

**Status**: Bra referens men vår implementation är mer komplett

---

## 🛠️ Vad vi KAN ta

### Från gemini_mulle:

1. **CardComponent.tsx** - Visuellt kort-komponent
   - Anpassa från Tailwind mobile till våra behov
   - Behåll selected/hover states
   - Lägg till build-indikatorer

2. **UI Layout-idéer**:
   - Kort-rendering stil
   - Selected state animation
   - Responsive design pattern

3. **Suit/Rank symbols**:
```typescript
export const SUIT_SYMBOLS = {
  [Suit.CLUBS]: '♣',
  [Suit.SPADES]: '♠',
  [Suit.HEARTS]: '♥',
  [Suit.DIAMONDS]: '♦'
};
```

### Från vår implementation:

1. **ALL spellogik** - gemini_mulle saknar komplett implementation
2. **Models** - Mer komplett än gemini
3. **Rules** - Komplett subset-summa, builds, trotta
4. **AI** - gemini har ingen AI

---

## 📋 Rekommendation

**Strategi**: Cherry-pick från gemini_mulle

**TA**:
- ✅ CardComponent.tsx (visuell rendering)
- ✅ SUIT_SYMBOLS konstanter
- ✅ Layout-inspiration

**SKIPPA**:
- ❌ gameLogic.ts (ofullständig)
- ❌ Backend-logik (saknas)
- ❌ Capacitor/iOS stuff (vi gör webb)

**SKAPA NYTT**:
- 🆕 GameBoard.tsx - Visa board med piles och builds
- 🆕 PlayerHand.tsx - Klickbara kort från vår Player-model
- 🆕 ScorePanel.tsx - Visa mulle/tabbe/bonus
- 🆕 GameController.tsx - Integrera med vår GameEngine

---

## 🎨 Föreslagen Frontend-Struktur

```
client/
├── src/
│   ├── components/
│   │   ├── Card.tsx (från gemini, anpassad)
│   │   ├── Pile.tsx (ny)
│   │   ├── Build.tsx (ny)
│   │   ├── PlayerHand.tsx (ny)
│   │   ├── GameBoard.tsx (ny)
│   │   └── ScorePanel.tsx (ny)
│   ├── game/
│   │   └── engine.ts (importera från ../../../src/*)
│   ├── App.tsx
│   └── index.tsx
└── package.json
```

---

## ⏱️ Tidsestimering

**Med gemini_mulle som bas**:
- Card component anpassning: 1h
- Nya komponenter: 4h
- Integration med engine: 2h
- Styling/polish: 2h
- **Total: 9h** (sparar ~6h från scratch)

**Från scratch**:
- Alla komponenter: 8h
- Integration: 3h
- Styling: 4h
- **Total: 15h**

**Besparning**: ~6 timmar genom att återanvända CardComponent!

---

## 🚀 Nästa Steg

1. ✅ Kopiera CardComponent.tsx
2. ✅ Anpassa till våra Card-models
3. ⏳ Skapa GameBoard med piles
4. ⏳ PlayerHand med click handlers
5. ⏳ Integrera med vår GameEngine

**Start**: Efter GameEngine är färdig (Dag 3-4)
