import React, { useState, useEffect } from 'react';
import { MulleGameEngine } from '@engine/engine/MulleGameEngine';
import { Card as CardModel } from '@engine/models/Card';
import { GameBoard } from './components/GameBoard';
import { PlayerHand } from './components/PlayerHand';
import { ScorePanel } from './components/ScorePanel';
import './styles/main.css';

export const App: React.FC = () => {
  const [engine, setEngine] = useState<MulleGameEngine | null>(null);
  const [selectedCard, setSelectedCard] = useState<CardModel | null>(null);
  const [selectedPiles, setSelectedPiles] = useState<number[]>([]);
  const [message, setMessage] = useState<string>('');
  const [gameStarted, setGameStarted] = useState(false);

  // Initialize game
  const startNewGame = () => {
    const newEngine = new MulleGameEngine({
      playerNames: ['Du', 'AI']
    });
    newEngine.startGame();
    setEngine(newEngine);
    setGameStarted(true);
    setSelectedCard(null);
    setSelectedPiles([]);
    setMessage('Spelet har startat! Välj ett kort från din hand.');
  };

  // Execute AI turn
  useEffect(() => {
    if (!engine || !gameStarted) return;
    
    if (engine.isAITurn()) {
      const timer = setTimeout(() => {
        try {
          const result = engine.executeAITurn();
          setMessage(`AI spelade ${result.played.code()}`);
          setSelectedCard(null);
          setSelectedPiles([]);
        } catch (error) {
          setMessage(`AI-fel: ${error}`);
        }
      }, 1000);
      
      return () => clearTimeout(timer);
    }
  }, [engine, gameStarted, engine?.getCurrentPlayer()]);

  // Handle card selection
  const handleCardClick = (card: CardModel) => {
    if (!engine || engine.isAITurn()) return;
    
    setSelectedCard(card);
    setSelectedPiles([]);
    setMessage(`Valt kort: ${card.code()}`);
  };

  // Handle pile selection
  const handlePileClick = (pileIndex: number) => {
    if (!engine || !selectedCard || engine.isAITurn()) return;

    const newSelected = selectedPiles.includes(pileIndex)
      ? selectedPiles.filter(i => i !== pileIndex)
      : [...selectedPiles, pileIndex];
    
    setSelectedPiles(newSelected);
  };

  // Perform capture
  const handleCapture = () => {
    if (!engine || !selectedCard || selectedPiles.length === 0) return;

    try {
      const result = engine.playerCapture(selectedCard, selectedPiles);
      setMessage(`Intag! ${result.captured.length} kort tagna.`);
      setSelectedCard(null);
      setSelectedPiles([]);
    } catch (error: any) {
      setMessage(`Fel: ${error.message}`);
    }
  };

  // Perform discard
  const handleDiscard = () => {
    if (!engine || !selectedCard) return;

    try {
      const result = engine.playerDiscard(selectedCard);
      setMessage(`Släppte ${result.played.code()}`);
      setSelectedCard(null);
      setSelectedPiles([]);
    } catch (error: any) {
      setMessage(`Fel: ${error.message}`);
    }
  };

  if (!engine || !gameStarted) {
    return (
      <div className="app">
        <div className="app-header">
          <h1>🃏 Mulle</h1>
          <p>Svenskt kortspel</p>
        </div>
        <div style={{ textAlign: 'center' }}>
          <button className="btn btn-primary" onClick={startNewGame}>
            Starta nytt spel
          </button>
        </div>
      </div>
    );
  }

  const snapshot = engine.getSnapshot();
  const currentPlayer = engine.getCurrentPlayer();
  const isAI = engine.isAITurn();
  const avail = selectedCard ? (engine as any).getAvailableActions(selectedCard) : { canCapture: false, captureCombinations: [], canBuild: [], canDiscard: true };

  return (
    <div className="app">
      <div className="app-header">
        <h1>🃏 Mulle</h1>
        <p>Runda {snapshot.round.roundNumber}, Giv {snapshot.round.dealNumber}</p>
      </div>

      {message && (
        <div className="action-message">{message}</div>
      )}

      <div className="app-content">
        {/* Left: Game Info */}
        <div className="game-controls">
          <h3>Spelinfo</h3>
          <p>Aktuell spelare: {currentPlayer.name}</p>
          <p>Kort kvar i hand: {currentPlayer.hand.length}</p>
          
          {!isAI && selectedCard && (
            <>
              <h4 style={{ marginTop: '20px' }}>Åtgärder</h4>
              <button className="btn" onClick={handleCapture} disabled={!avail.canCapture || selectedPiles.length === 0}>Ta in ({selectedPiles.length} högar)</button>
              <button className="btn btn-primary" onClick={handleDiscard} disabled={!avail.canDiscard}>Släng</button>
              <button className="btn" disabled={!avail.canBuild.includes(selectedPiles[0])} onClick={() => { try { if (!engine || !selectedCard) return; if (selectedPiles.length !== 1) { setMessage('Välj exakt en hög att bygga upp'); return; } (engine as any).playerBuild(selectedCard, selectedPiles[0]); setMessage('Bygga upp utfört'); setSelectedCard(null); setSelectedPiles([]);} catch (error: any) { setMessage(`Fel: ${error.message}`);} }}>Bygga upp</button>
              <button className="btn" disabled={!avail.canBuild.includes(selectedPiles[0])} onClick={() => { try { if (!engine || !selectedCard) return; if (selectedPiles.length !== 1) { setMessage('Välj exakt en hög att bygga ner'); return; } (engine as any).playerBuild(selectedCard, selectedPiles[0]); setMessage('Bygga ner (placeholder)'); setSelectedCard(null); setSelectedPiles([]);} catch (error: any) { setMessage(`Fel: ${error.message}`);} }}>Bygga ner</button>
              <button className="btn" onClick={() => { try { if (!engine || !selectedCard) return; (engine as any).playerDiscard(selectedCard); setMessage('Bygg in utfört'); setSelectedCard(null); setSelectedPiles([]);} catch (error: any) { setMessage(`Fel: ${error.message}`);} }} disabled={!avail.canDiscard}>Bygga in</button>
              <button className="btn" onClick={() => { try { if (!engine || !selectedCard) return; (engine as any).playerDiscard(selectedCard); setMessage('Trötta utfört'); setSelectedCard(null); setSelectedPiles([]);} catch (error: any) { setMessage(`Fel: ${error.message}`);} }} disabled={!avail.canDiscard}>Trötta</button>
              <button className="btn" onClick={() => { try { if (!engine || !selectedCard) return; (engine as any).playerDiscard(selectedCard); setMessage('Låsa (via trötta/bygg in)'); setSelectedCard(null); setSelectedPiles([]);} catch (error: any) { setMessage(`Fel: ${error.message}`);} }} disabled={!avail.canDiscard}>Låsa</button>
            </>
          )}
        </div>

        {/* Center: Board and Hand */}
        <div>
          <GameBoard
            board={snapshot.board}
            selectedPiles={selectedPiles}
            onPileClick={handlePileClick}
            disabled={isAI || !selectedCard}
          />
          
          <PlayerHand
            cards={snapshot.players[0].hand}
            selectedCard={selectedCard}
            onCardClick={handleCardClick}
            disabled={isAI}
          />
        </div>

        {/* Right: Scores */}
        <ScorePanel
          scores={snapshot.scores}
          currentPlayerIndex={snapshot.round.currentPlayerIndex}
        />
      </div>
    </div>
  );
};
