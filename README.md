# 🃏 Mulle - TypeScript Implementation

Swedish card game "Mulle" implemented in TypeScript with React frontend.

## 🎯 Project Status

**Progress**: 85% Complete  
**Timeline**: 4 days ahead of 7-day deadline  
**Code**: 2,964 lines of TypeScript

### Completed ✅
- ✅ Complete game engine with AI
- ✅ All card game rules implemented
- ✅ React frontend with responsive UI
- ✅ 34 passing tests
- ✅ Capture, discard, build actions
- ✅ Score tracking and display

### In Progress ⏳
- Build UI integration
- Action hints
- Win/lose screens

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run tests
npm test

# Start development server
npm run dev

# Build for production
npm run build
```

## 📁 Project Structure

```
mulle/
├── src/                    # Backend logic
│   ├── models/            # Card, Deck, Player, Board, Build
│   ├── rules/             # Game rules and validation
│   └── engine/            # Game engine
├── client/                # Frontend
│   └── src/
│       ├── components/    # React components
│       └── styles/        # CSS
└── tests/                 # Jest tests
```

## 🎮 Game Rules

Mulle is a Swedish card game for 2+ players using 2 standard decks.

### Special Cards
- **Ace (A)**: Value 1 on board, 14 in hand
- **Spades 2 (SP2)**: Value 2 on board, 15 in hand  
- **Diamonds 10 (RU10)**: Value 10 on board, 16 in hand

### Actions
1. **Capture** - Take cards from board matching your card's value
2. **Build** - Combine cards to create a higher value
3. **Trotta** - Gather all matching singles into a locked build
4. **Discard** - Place card on board (only if no captures possible)

### Scoring
- **Mulle**: Capture identical cards (same suit + rank) = card value points
- **Tabbe**: Capture from empty board = 1 point per capture
- **Intake**: Spades + special cards = bonus points
- **Bonus**: If intake > 20, bonus = (intake - 20) × 2

## 🏗️ Architecture

### Models
- **Card**: Individual playing card with special value handling
- **Deck**: 104 cards (2 decks), shuffled with optional seed
- **Player**: Hand, captured cards, mulles, tabbe tracking
- **Board**: Piles and builds with absorption logic
- **Build**: Locked/unlocked builds with owner tracking

### Rules Engine
- **Capture**: Complex subset-sum algorithm for combinations
- **Validation**: Trail restrictions, build requirements
- **Scoring**: Intake tables, mulle detection
- **AI**: Heuristic prioritization (capture > build > discard)

### Game Engine
- Turn management
- Round/deal flow
- AI integration
- Action validation

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch
```

**Test Coverage**: 34 tests across models, rules, and engine

## 🎨 Frontend

Built with:
- React 19
- TypeScript
- Vite
- Custom CSS (no framework)

### Components
- **Card**: Visual card rendering
- **PlayerHand**: Hand display with selection
- **GameBoard**: Board piles and builds
- **ScorePanel**: Live scoring
- **App**: Main game controller

## 🔧 Development

### Tech Stack
- TypeScript 5.0
- React 19
- Vite 7
- Jest 29

### Code Quality
- Full TypeScript strict mode
- ESLint ready
- 100% passing tests
- No compilation errors

## 📝 Documentation

See detailed docs:
- [Progress Report](PROGRESS.md)
- [Implementation Notes](IMPLEMENTATION_NOTES.md)
- [Rule Book](RULEBOOK.md)
- [Gemini Analysis](GEMINI_MULLE_ANALYSIS.md)

## 🎯 Roadmap

- [x] Core game logic (100%)
- [x] AI opponent (100%)
- [x] Basic UI (85%)
- [ ] Build UI integration
- [ ] Polish and animations
- [ ] Deployment

## 📜 License

MIT

## 🙏 Credits

- Original Python implementation
- gemini_mulle for Card component inspiration
- Swedish card game tradition

---

**Built with ❤️ in TypeScript**
