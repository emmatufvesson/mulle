import React from 'react';
import { Card as CardModel } from '@engine/models/Card';
import { Card } from './Card';

interface PlayerHandProps {
  cards: CardModel[];
  selectedCard: CardModel | null;
  onCardClick: (card: CardModel) => void;
  disabled?: boolean;
}

/**
 * PlayerHand component - displays player's cards
 */
export const PlayerHand: React.FC<PlayerHandProps> = ({ 
  cards, 
  selectedCard, 
  onCardClick,
  disabled = false
}) => {
  return (
    <div className="player-hand">
      <h3>Din hand</h3>
      <div className="hand-cards">
        {cards.map((card) => (
          <Card
            key={card.id}
            card={card}
            isSelected={selectedCard === card}
            onClick={disabled ? undefined : () => onCardClick(card)}
          />
        ))}
      </div>
    </div>
  );
};
