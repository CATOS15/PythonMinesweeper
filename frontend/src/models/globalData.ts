import { Socket } from 'socket.io-client';
import User from "./user";

export default class GlobalData {
    user: User = new User();
    socket!: Socket;
}