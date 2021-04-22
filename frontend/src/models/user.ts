import { Difficulty } from "./enums";

export default class User {
  name = "";

  room: Room = new Room();
}

export class Room{
  roomname = "";
  difficulty: Difficulty = Difficulty.EASY;
  width!: number;
  height!: number;
  totalMines!: number;
}

export class UserCursor{
  name = "";
  roomname = "";
  left: number = 0;
  top: number = 0;
}