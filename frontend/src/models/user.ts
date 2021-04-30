import { Difficulty, GameState } from "./enums";

export default class User {
  name = "";

  room: Room = new Room();
}

export class Room{
  roomname = "";
  difficulty: Difficulty = Difficulty.EASY;
  gamestate!: GameState;
  width!: number;
  height!: number;
  flags!: number;
  timer!: number;
}

export class UserCursor{
  name = "";
  roomname = "";
  left: number = 0;
  top: number = 0;
}

export class GameStateUser{
  name = "";
  gamestate!: GameState;
}