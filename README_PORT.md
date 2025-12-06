# TypeScript Port of the Mulle Card Game Engine

## Purpose

This directory contains the TypeScript port of the Mulle card game engine, originally written in Python.

## Goals

1. **Faithful Port**: Maintain exact same game logic and rules as the Python implementation
2. **Type Safety**: Leverage TypeScript's type system for better code quality and developer experience
3. **Test Parity**: Ensure all existing Python tests have corresponding Jest tests
4. **Modern Tooling**: Use modern Node.js tooling (ts-node-dev, Jest, TypeScript 5.x)

## Project Structure

```
src/
├── index.ts      # Main entry point
├── models/       # Game models (Card, Player, GameState, etc.)
├── engine/       # Game engine logic
└── rules/        # Game rules implementation

legacy/           # Reference Python sources (not part of TS build)
```

## Development

### Prerequisites

- Node.js 18+ 
- npm 9+

### Setup

```bash
npm install
```

### Commands

- `npm run build` - Compile TypeScript to JavaScript
- `npm run dev` - Run with hot reload (ts-node-dev)
- `npm test` - Run Jest tests
- `npm run test:watch` - Run tests in watch mode
- `npm run lint` - Type-check without emitting

## Migration Status

See [MIGRATION_PLAN.md](./MIGRATION_PLAN.md) for the detailed migration plan and current status.

## Notes

- The Python sources in `mulle/` remain the source of truth until the port is complete
- Legacy Python code will be copied to `legacy/` for reference during porting
- Each ported module should have corresponding Jest tests before being considered complete
