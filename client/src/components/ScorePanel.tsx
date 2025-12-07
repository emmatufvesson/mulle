import React from 'react';
import { ScoreBreakdown } from '@engine/rules/scoring';

interface ScorePanelProps {
  scores: ScoreBreakdown[];
  currentPlayerIndex: number;
}

/**
 * ScorePanel component - displays scores and game status
 */
export const ScorePanel: React.FC<ScorePanelProps> = ({ scores, currentPlayerIndex }) => {
  return (
    <div className="score-panel">
      <h3>Poäng</h3>
      {scores.map((score, index) => (
        <div 
          key={score.player.name}
          className={`player-score ${index === currentPlayerIndex ? 'current-player' : ''}`}
        >
          <div className="player-name">
            {score.player.name}
            {index === currentPlayerIndex && ' ⭐'}
          </div>
          <div className="score-details">
            <div className="score-row">
              <span>Mulle:</span>
              <span>{score.mullePoints}</span>
            </div>
            <div className="score-row">
              <span>Tabbe:</span>
              <span>{score.tabbe}</span>
            </div>
            <div className="score-row">
              <span>Intake:</span>
              <span>{score.intake}</span>
            </div>
            {score.bonus > 0 && (
              <div className="score-row score-bonus">
                <span>Bonus:</span>
                <span>{score.bonus}</span>
              </div>
            )}
            <div className="score-row score-total">
              <span>Total:</span>
              <span>{score.total}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
