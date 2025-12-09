import React from 'react';
import { Board as BoardModel } from '@engine/models/Board';
import { Build } from '@engine/models/Build';
import { Card } from './Card';

interface GameBoardProps {
  board: BoardModel;
  selectedPiles: number[];
  onPileClick: (pileIndex: number) => void;
  disabled?: boolean;
}

/**
 * GameBoard component - displays table with piles and builds
 */
export const GameBoard: React.FC<GameBoardProps> = ({ 
  board, 
  selectedPiles,
  onPileClick,
  disabled = false
}) => {
  return (
    <div className="game-board">
      <h3>Bord</h3>
      <div className="board-piles">
        {board.piles.length === 0 ? (
          <div className="board-empty">Bordet är tomt</div>
        ) : (
          board.piles.map((pile, index) => {
            const isBuild = pile instanceof Build;
            const cards = isBuild ? pile.cards : pile;
            const isSelected = selectedPiles.includes(index);

            return (
              <div
                key={index}
                className={`pile ${isSelected ? 'pile-selected' : ''} ${isBuild ? 'pile-build' : ''}`}
                onClick={disabled ? undefined : () => onPileClick(index)}
              >
                {isBuild && (
                  <div className="build-info">
                    <span className="build-value">Värde: {pile.value}</span>
                    {pile.locked && <span className="build-locked">🔒</span>}
                    <span className="build-owner">{pile.owner}</span>
                  </div>
                )}
                <div className="pile-cards">
                  {cards.map((card, cardIndex) => (
                    <Card
                      key={card.id}
                      card={card}
                      isSmall={cards.length > 1}
                      className={cardIndex > 0 ? 'pile-card-stacked' : ''}
                    />
                  ))}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
