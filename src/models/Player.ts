import { Hand } from './Hand';
import { Card } from './Card';

export interface IPlayer {
  id: string;
  name: string;
  hand: Hand;
  playCard(card: Card): boolean;
}

export class Player implements IPlayer {
  constructor(public id: string, public name: string, public hand = new Hand()) {}

  playCard(card: Card): boolean {
    return this.hand.remove(card);
  }
}