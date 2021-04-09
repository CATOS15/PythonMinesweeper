import { Difficulty } from "./enums";

export class Room{
    roomname = "";
    difficulty: Difficulty = Difficulty.EASY;
    width!: number;
    height!: number;
}