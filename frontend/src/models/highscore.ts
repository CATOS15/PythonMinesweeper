import { Difficulty } from "./enums";

export default class Highscore{
    highscoreId!: string;
    width!: number;
    height!: number;
    timer!: number;
    numberOfPlayers!: number;
    usernames!: string;
    difficulty!: Difficulty;
}