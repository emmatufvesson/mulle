import React from 'react';
import { Card as CardModel } from '@engine/models/Card';
import { SUIT_SYMBOLS, getRankLabel, isRedSuit } from '../constants';

interface CardProps {
  card?: CardModel;
  onClick?: () => void;
  isSelected?: boolean;
  isSmall?: boolean;
  className?: string;
}

/**
 * Card component - renders a playing card
 * Adapted from gemini_mulle with our Card model
 */
export const Card: React.FC<CardProps> = ({ 
  card, 
  onClick, 
  isSelected = false, 
  isSmall = false,
  className = '' 
}) => {
  // Render card back if no card provided
  if (!card) {
    return (
      <div 
        className={`card card-back ${isSmall ? 'card-small' : ''} ${className}`}
      >
        <div className="card-back-pattern"></div>
      </div>
    );
  }

  const isRed = isRedSuit(card.suit);
  const suitSymbol = SUIT_SYMBOLS[card.suit];
  const rankLabel = getRankLabel(card.rank);

  return (
    <div
      onClick={onClick}
      className={`
        card
        ${isSmall ? 'card-small' : ''}
        ${isSelected ? 'card-selected' : ''}
        ${isRed ? 'card-red' : 'card-black'}
        ${onClick ? 'card-clickable' : ''}
        ${className}
      `.trim()}
    >
      {/* Top Left */}
      <div className="card-corner card-corner-tl">
        <div className="card-rank">{rankLabel}</div>
        <div className="card-suit">{suitSymbol}</div>
      </div>

      {/* Center Symbol */}
      <div className="card-center">
        {suitSymbol}
      </div>

      {/* Bottom Right (upside down) */}
      <div className="card-corner card-corner-br">
        <div className="card-rank">{rankLabel}</div>
        <div className="card-suit">{suitSymbol}</div>
      </div>
    </div>
  );
};
